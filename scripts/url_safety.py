#!/usr/bin/env python3
"""url_safety.py, one answer to "may this process fetch that URL".

WHY THIS EXISTS (2026-09-23, run No.66, after two rounds of review).

Run No.66 gave the research scout a narrow Bash capability so it could run
scripts/fetch_pdf_text.py on a primary source that happens to be a PDF. The
first version of that guard pinned the COMMAND and not the TARGET, so
`fetch_pdf_text.py /etc/passwd` was allowed and the reader turned it into a
file:// read by itself. The second version added a scheme allowlist and an
address check, and review found two ways straight through it:

  1. LEGACY NUMERIC HOSTS. `ipaddress.ip_address()` rejects `2852039166`,
     `127.1`, `0x7f000001` and `017700000001`, and the guard treated every
     rejected value as an ordinary hostname. `socket` resolves all four, and
     the first is 169.254.169.254, the cloud metadata endpoint. Measured on
     this container, not argued.
  2. REDIRECTS. Only the command's own URL was ever inspected. `urlopen`
     follows redirects by default, so a public URL that answers 302 to
     `http://127.0.0.1/` recovered exactly the internal-request capability the
     guard existed to remove.

Both have the same root cause: the check was on the STRING a caller typed
rather than on the ADDRESS a socket would actually open. So this module is
about addresses, and it lives beside the fetch rather than only in the hook.

WHERE IT IS ENFORCED, and why in two places. scripts/fetch_pdf_text.py calls
`check_url` before the first request and again on EVERY redirect hop, which is
the real boundary: it is the process that opens the socket, and it is the only
place a redirect chain is visible. scripts/scout_bash_guard.py calls the same
function as a cheap pre-check, so a scout is told no before a process starts.
The hook is a convenience; the reader is the guarantee.

WHAT IT DOES NOT PROMISE, stated rather than implied. A name is resolved once
here and again by the connect, so a DNS answer that changes between the two
is not caught. Defeating that needs the socket pinned to the address that was
checked, which urllib does not expose. This narrows the reachable surface to
public addresses at check time; it is not a sandbox, and the capability it
guards is deliberately one read-only command.

Stdlib only. No network beyond name resolution.
"""
from __future__ import annotations

import ipaddress
import socket

ALLOWED_SCHEMES = ("http://", "https://")

# Names that never point at a published document, matched on the host alone.
BLOCKED_HOSTS = ("localhost", "localhost.localdomain", "ip6-localhost",
                 "metadata", "metadata.google.internal", "instance-data")
BLOCKED_HOST_SUFFIXES = (".localhost", ".local", ".internal", ".localdomain")


def host_of(url):
    """The bare host of an http(s) URL, lowercased, or '' if there is none.

    Credentials and the port are stripped and a bracketed IPv6 literal is
    unwrapped, because the checks below are about the host and an attacker
    gets to choose everything around it.
    """
    rest = url.split("://", 1)[1] if "://" in url else url
    host = rest.split("/", 1)[0].split("?", 1)[0].split("#", 1)[0]
    if "@" in host:
        host = host.rsplit("@", 1)[1]
    if host.startswith("["):
        host = host[1:].split("]", 1)[0]
    else:
        host = host.split(":", 1)[0]
    return host.strip().rstrip(".").lower()


def is_public(addr):
    """True when this ipaddress object is a routable public address."""
    return not (addr.is_loopback or addr.is_private or addr.is_link_local
                or addr.is_reserved or addr.is_multicast
                or addr.is_unspecified)


def literal_address(host):
    """The address this host IS, written any way a resolver accepts, or None.

    ipaddress.ip_address only accepts the dotted-quad spelling. inet_aton also
    accepts the decimal, octal and hex forms and the short 127.1 form, which is
    exactly the gap review found, so both are tried and a hit from either is
    treated as a literal rather than as a name.
    """
    try:
        return ipaddress.ip_address(host)
    except ValueError:
        pass
    try:
        return ipaddress.ip_address(socket.inet_ntoa(socket.inet_aton(host)))
    except (OSError, ValueError):
        return None


def resolved_addresses(host):
    """Every address this host resolves to, as ipaddress objects."""
    try:
        infos = socket.getaddrinfo(host, None)
    except (OSError, UnicodeError):
        return []
    out = []
    for info in infos:
        try:
            out.append(ipaddress.ip_address(info[4][0].split("%", 1)[0]))
        except ValueError:
            continue
    return out


def check_url(url, resolve=True):
    """Why this URL may not be fetched, or None when it may be.

    `resolve=False` skips name resolution and checks only what the string
    itself says, which is what a caller wants when it has no network or is
    only pre-screening.
    """
    if not isinstance(url, str) or not url.strip():
        return "there is no URL here."
    if not url.lower().startswith(ALLOWED_SCHEMES):
        return ("%r is not an http or https URL. Only published documents are "
                "fetchable here, so a local path, a file:// URL or any other "
                "scheme is refused." % url)
    host = host_of(url)
    if not host:
        return "%r has no host." % url
    if host in BLOCKED_HOSTS or host.endswith(BLOCKED_HOST_SUFFIXES):
        return ("%r points at this machine or its metadata service, not at a "
                "published document." % url)

    literal = literal_address(host)
    if literal is not None:
        if not is_public(literal):
            return ("%r is a loopback, private or otherwise non-public "
                    "address (%s)." % (url, literal))
        return None

    if not resolve:
        return None
    addrs = resolved_addresses(host)
    if not addrs:
        return "%r does not resolve to any address." % url
    bad = [a for a in addrs if not is_public(a)]
    if bad:
        return ("%r resolves to a non-public address (%s), so it names "
                "something inside this machine or its network rather than a "
                "published document." % (url, bad[0]))
    return None


def self_test():
    ok = [True]

    def check(label, cond, detail=""):
        print("  %s  %s%s" % ("PASS" if cond else "FAIL", label,
                              "  " + detail if detail else ""))
        if not cond:
            ok[0] = False

    print("it refuses everything that is not a published http(s) document")
    for u in ["/etc/passwd", "file:///etc/passwd", "FILE:///etc/shadow",
              "ftp://x.gov/d.pdf", "data:application/pdf;base64,AAAA",
              "ledger/gaswatch.jsonl", "../../etc/passwd", "", "   "]:
        check("refuses %r" % u, check_url(u, resolve=False) is not None)

    print("it refuses this machine and its network, however the host is spelt")
    for u in ["http://localhost/d.pdf", "http://LOCALHOST:8080/d.pdf",
              "http://127.0.0.1/d.pdf", "http://0.0.0.0/d.pdf",
              "http://10.0.0.5/d.pdf", "http://192.168.1.1/d.pdf",
              "http://169.254.169.254/latest/meta-data/",
              "http://metadata.google.internal/x", "http://[::1]/d.pdf",
              "http://user:pw@127.0.0.1/d.pdf", "http://build.internal/d.pdf"]:
        check("refuses %r" % u, check_url(u, resolve=False) is not None)

    print("and the legacy numeric spellings review found, which are the point")
    for u, means in [("http://2852039166/latest/meta-data/", "169.254.169.254"),
                     ("http://127.1/d.pdf", "127.0.0.1"),
                     ("http://0x7f000001/d.pdf", "127.0.0.1"),
                     ("http://017700000001/d.pdf", "127.0.0.1")]:
        check("refuses %r, which is %s" % (u, means),
              check_url(u, resolve=False) is not None)

    print("it still allows an ordinary public document")
    for u in ["https://matanuska.legistar1.com/a.pdf",
              "https://dnr.alaska.gov/doc.pdf", "https://x.gov:8443/d.pdf",
              "HTTPS://X.GOV/D.PDF", "https://8.8.8.8/d.pdf"]:
        check("allows %r" % u, check_url(u, resolve=False) is None,
              str(check_url(u, resolve=False) or ""))

    print("and the address helpers agree with the stdlib")
    check("a public literal is public", is_public(ipaddress.ip_address("8.8.8.8")))
    check("a private literal is not", not is_public(ipaddress.ip_address("10.1.2.3")))
    check("127.1 reads as an address", str(literal_address("127.1")) == "127.0.0.1")
    check("a real name is not a literal", literal_address("example.gov") is None)

    print()
    print("url_safety self-test: %s" % ("PASS" if ok[0] else "FAIL"))
    return 0 if ok[0] else 1


if __name__ == "__main__":
    raise SystemExit(self_test())
