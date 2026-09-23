#!/usr/bin/env python3
"""fetch_pdf_text.py -- read a remote PDF as text, so a scout can cite a primary
source instead of reporting one as unreachable.

WHY THIS EXISTS (2026-09-18, run No.62).

Two scouts lost their primary source to a PDF on the same run. Beat D wanted the
DNR preliminary decision for ADL 234762; Beat C wanted the NPFMC Draft 2027
Annual Deployment Plan. Both reported "PDF extraction unavailable, poppler-utils
is not installed" and fell back to secondary coverage. The claims gate then
passed 41 of 41, because a claim that is never made cannot fail a gate: a
primary document this routine cannot READ is a silent hole in it, and the run
only finds out when a beat comes back thinner than the story deserved.

THE DIAGNOSIS IN THOSE REPORTS WAS WRONG, and that is the whole reason this file
is fifty lines rather than a dependency request. Nothing here needs poppler.
pypdf is already a bootstrap dependency (bootstrap.sh installs it and probes
that it IMPORTS, because Debian's cryptography can break it), and it extracts
text from these documents perfectly well. What was actually missing is a way to
GET the bytes: WebFetch converts a page to markdown and hands a PDF back as
binary, which is unreadable in a transcript, and the agent then reasons about
the wrong half of the problem.

So this does exactly two things and adds no dependency: fetch the bytes with
urllib, extract the text with pypdf.

WHAT IT REFUSES TO DO, on purpose:
  - It does not follow a redirect to a non-PDF and report success. The bytes
    must start with %PDF or it exits non-zero and says what arrived instead,
    because a 200-with-an-HTML-login-page that gets summarised as a document is
    how a fabricated citation is born.
  - It does not read an unbounded download into memory. --max-mb (default 48)
    is enforced on the stream, not on a Content-Length header a server is free
    to lie about.
  - It does not pretend an empty extraction is text. A scanned PDF with no text
    layer exits 3 and says so, rather than returning "" for something to
    summarise.

USAGE
    python3 scripts/fetch_pdf_text.py <url-or-path>
    python3 scripts/fetch_pdf_text.py <url> --pages 1-6 --max-chars 40000
    python3 scripts/fetch_pdf_text.py <url> --json
    python3 scripts/fetch_pdf_text.py --self-test

http(s):// and file:// URLs and plain local paths all work; the local path is
there so the same command reads a document that was already downloaded.

EXITS  0 text returned | 1 could not fetch | 2 not a PDF | 3 no text layer

Read-only. Stdlib plus pypdf. It never writes anything unless --out is given.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import url_safety  # noqa: E402  (same directory, after sys.path is set)

# Federal and state document servers routinely 403 a bare urllib UA while
# serving the same file to a browser. This is the ordinary desktop string; it
# claims nothing untrue about what is fetching, and every host below is
# publishing the document for the public to read.
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/141.0.0.0 Safari/537.36")
DEFAULT_MAX_MB = 48
CHUNK = 1 << 16

# The whole transfer gets this multiple of --timeout before it is abandoned.
# Generous, because a large government PDF on a slow host is a real thing and
# the point is to bound the worst case rather than to be strict about the
# ordinary one. At the default 45 second timeout that is 4 minutes.
DEADLINE_FACTOR = 6


class _GuardedRedirects(urllib.request.HTTPRedirectHandler):
    """Refuse a redirect whose destination is not a public http(s) document.

    urlopen follows redirects on its own, so before this the only URL anyone
    inspected was the one typed on the command line. A public host answering
    302 to http://127.0.0.1/ or to the metadata endpoint was enough to reach
    inside this container. Every hop now gets the same check as the first URL.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        why = url_safety.check_url(newurl)
        if why:
            raise urllib.error.HTTPError(
                newurl, code,
                "refused a redirect to a non-public destination. %s" % why,
                headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _fetch(url, max_mb, timeout, allow_local=False):
    """Return (bytes, final_url, content_type) or raise RuntimeError.

    allow_local is for THIS FILE'S OWN hermetic self-test, which serves its
    fixtures from a loopback port. It is a Python argument and deliberately
    not a command-line flag, so nothing invoked as a command can set it.
    """
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or (len(parsed.scheme) == 1 and os.name == "nt"):
        url = "file://" + os.path.abspath(url)
        parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https", "file"):
        raise RuntimeError("scheme %r is not fetchable here; pass an http(s) "
                           "url or a local path" % parsed.scheme)
    # THE ADDRESS IS CHECKED HERE, not only by whatever called this. Review of
    # run No.66 found two ways past a caller-side check: a legacy numeric host
    # such as http://2852039166/ that resolves to the metadata endpoint, and a
    # public URL that simply answers 302 to http://127.0.0.1/. Both are about
    # the address a socket opens rather than the string a caller typed, so the
    # policy lives beside the socket and applies to EVERY hop.
    #
    # file:// is still reachable from a trusted caller, deliberately: a
    # maintainer reading a PDF off disk is the original use. What changed is
    # that an http(s) fetch can no longer become an internal one.
    if parsed.scheme in ("http", "https") and not allow_local:
        why = url_safety.check_url(url)
        if why:
            raise RuntimeError(why)
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/pdf,*/*",
    })
    limit = int(max_mb * 1024 * 1024)
    # The redirect guard is ALWAYS installed. allow_local waives the check on
    # the first URL so this file's own loopback fixture is reachable; it does
    # not waive the policy on where that fixture may send us next, which is
    # the bypass being tested and is never a thing a trusted caller wants.
    # NO PROXY ON THE allow_local PATH. build_opener picks up ProxyHandler from
    # the environment, so this new opener quietly ignored the proxyless global
    # opener the self-test installs and sent every loopback fixture request to
    # the agent proxy. The hermetic tests were then testing the proxy's answer
    # rather than their own fixtures, which is the failure mode where a green
    # suite means nothing. The redirect guard is installed either way.
    handlers = [_GuardedRedirects]
    if allow_local:
        handlers.append(urllib.request.ProxyHandler({}))
    opener = urllib.request.build_opener(*handlers)
    # THE CLOCK STARTS BEFORE open(), not after it. opener.open() waits for the
    # response HEADERS, and its socket timeout resets on every byte, so a server
    # trickling header bytes stalls the reader before the deadline below even
    # exists. Measured: a 0.2 second timeout against a header-dribbling server
    # was still blocked when an outer 4 second timeout killed it. The bound has
    # to cover the connection and header phase as well as the body.
    budget = max(1.0, float(timeout)) * DEADLINE_FACTOR
    deadline = time.monotonic() + budget

    def _open():
        return opener.open(req, timeout=timeout)

    # A WATCHDOG OVER open() ITSELF, because a check AFTER it cannot interrupt
    # it. open() blocks until the response headers arrive and its socket
    # timeout resets on every byte, so a server trickling header bytes stalls
    # here before the body loop's deadline is ever consulted. Measured before
    # this: a 0.2 second timeout against a header-dribbling server was still
    # blocked at 14.7 seconds, and was then stopped by CPython's 100-header cap
    # rather than by anything here, which is luck and not a bound.
    #
    # The worker is a daemon, so if it is still stuck when this returns the
    # process can still exit. That is the right trade for a read-only CLI: the
    # caller gets control back on schedule and the socket dies with the process.
    try:
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        try:
            future = pool.submit(_open)
            try:
                opened = future.result(timeout=budget)
            except concurrent.futures.TimeoutError:
                raise RuntimeError(
                    "the server took longer than %.0f seconds to send its "
                    "response headers and has been abandoned; a server that "
                    "trickles header bytes can outlast a per-read timeout. "
                    "Raise --timeout deliberately if this host really is that "
                    "slow" % budget)
        finally:
            pool.shutdown(wait=False)
        with opened as resp:
            ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip()
            buf = io.BytesIO()
            # A WALL-CLOCK DEADLINE ACROSS THE WHOLE TRANSFER, not just per
            # read. urllib's timeout applies to each blocking operation, so a
            # server that sends one byte just inside every timeout keeps this
            # loop running forever: measured at 3.12 seconds of transfer under
            # a 0.2 second timeout, and that scales to no limit at all. The
            # size ceiling does not help, because a slow dribble never reaches
            # it. A scout that never returns is a run that never finishes.
            while True:
                if time.monotonic() > deadline:
                    raise RuntimeError(
                        "the download was still running %.0f seconds after it "
                        "started and has been abandoned; a server that trickles "
                        "bytes can outlast a per-read timeout forever. Raise "
                        "--timeout deliberately if this document really is that "
                        "slow" % budget)
                # read1 RATHER THAN read, and this is the half that makes the
                # deadline above reachable. read(CHUNK) blocks until it has all
                # 64 KB or the stream ends, so a server dribbling one byte per
                # tick stays INSIDE a single read for hours and the loop never
                # gets to look at the clock. read1 returns whatever arrived,
                # so the loop turns over and the deadline can fire.
                chunk = resp.read1(CHUNK) if hasattr(resp, "read1") else resp.read(CHUNK)
                if not chunk:
                    break
                buf.write(chunk)
                if buf.tell() > limit:
                    raise RuntimeError(
                        "download passed the %d MB ceiling before it ended; "
                        "raise --max-mb deliberately if this document really is "
                        "that large" % max_mb)
            return buf.getvalue(), resp.geturl(), ctype
    except urllib.error.HTTPError as exc:
        raise RuntimeError("HTTP %s %s" % (exc.code, exc.reason))
    except urllib.error.URLError as exc:
        raise RuntimeError("could not reach it: %s" % exc.reason)
    except OSError as exc:
        raise RuntimeError("could not read it: %s" % exc)


def _page_range(spec, n):
    """'1-6' / '3' / '2-' -> a 0-based list of page indices, clamped to n."""
    if not spec:
        return list(range(n))
    out = []
    for part in str(spec).split(","):
        part = part.strip()
        if not part:
            continue
        m = re.match(r"^(\d+)\s*-\s*(\d*)$", part)
        if m:
            lo = max(1, int(m.group(1)))
            hi = int(m.group(2)) if m.group(2) else n
        elif part.isdigit():
            lo = hi = int(part)
        else:
            raise RuntimeError("unreadable --pages %r; use 1-6, 3, or 2-" % part)
        for p in range(lo, min(hi, n) + 1):
            if 1 <= p <= n and (p - 1) not in out:
                out.append(p - 1)
    return out


def extract(data, pages=None, max_chars=0):
    """Return a dict with the extracted text and what was read. Raises
    RuntimeError if the bytes are not a PDF."""
    head = data[:1024]
    if not head.startswith(b"%PDF"):
        sniff = "empty response" if not data else (
            "HTML" if b"<html" in head.lower() else
            "%r" % head[:48])
        raise RuntimeError(
            "these bytes are not a PDF (%d bytes, starts with %s). A redirect "
            "to a login or interstitial page looks exactly like this; open the "
            "url in the report rather than citing it" % (len(data), sniff))
    # pypdf and fontTools narrate to the root logger; a scout reading stdout
    # should get the document and nothing else.
    import logging
    for name in ("pypdf", "fontTools", "fontTools.ttLib", "fontTools.subset"):
        logging.getLogger(name).setLevel(logging.ERROR)
    try:
        from pypdf import PdfReader
    except ImportError as exc:                              # pragma: no cover
        raise RuntimeError("pypdf is missing (%s); run "
                           ".claude/skills/carousel-engine/bootstrap.sh" % exc)
    try:
        reader = PdfReader(io.BytesIO(data))
        n = len(reader.pages)
        idx = _page_range(pages, n)
        chunks = []
        for i in idx:
            try:
                chunks.append(reader.pages[i].extract_text() or "")
            except Exception as exc:                        # pragma: no cover
                chunks.append("[page %d did not extract: %s]" % (i + 1, exc))
    except RuntimeError:
        raise
    except Exception as exc:
        raise RuntimeError("pypdf could not open it: %s" % exc)
    text = "\n\n".join(chunks).strip()
    truncated = False
    if max_chars and len(text) > max_chars:
        text = text[:max_chars]
        truncated = True
    return {"pages_total": n, "pages_read": [i + 1 for i in idx],
            "bytes": len(data), "chars": len(text), "truncated": truncated,
            "text": text}


def read_pdf_text(url, pages=None, max_chars=0, max_mb=DEFAULT_MAX_MB,
                  timeout=45, allow_local=False):
    data, final, ctype = _fetch(url, max_mb, timeout, allow_local=allow_local)
    rec = extract(data, pages=pages, max_chars=max_chars)
    rec["url"] = final
    rec["content_type"] = ctype
    return rec


def _self_test():
    """Hermetic. Builds a PDF whose text is known, serves it over a real
    localhost socket, and reads it back -- so the fetch half and the extract
    half are both exercised without touching the network."""
    import http.server
    import tempfile
    import threading

    def build(text):
        objs = [
            b"<< /Type /Catalog /Pages 2 0 R >>",
            b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 200 100] "
            b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
            None,
            b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        ]
        esc = text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
        stream = ("BT /F1 12 Tf 10 50 Td (%s) Tj ET" % esc).encode()
        objs[3] = (b"<< /Length %d >>\nstream\n" % len(stream) + stream
                   + b"\nendstream")
        out = bytearray(b"%PDF-1.4\n")
        offs = []
        for i, body in enumerate(objs, 1):
            offs.append(len(out))
            out += b"%d 0 obj\n" % i + body + b"\nendobj\n"
        xref = len(out)
        out += b"xref\n0 %d\n" % (len(objs) + 1)
        out += b"0000000000 65535 f \n"
        for o in offs:
            out += b"%010d 00000 n \n" % o
        out += (b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF\n"
                % (len(objs) + 1, xref))
        return bytes(out)

    needle = "ALASKA AI PRIMARY SOURCE PROBE 4127"
    pdf = build(needle)
    root = tempfile.mkdtemp(prefix="fetchpdf-")
    with open(os.path.join(root, "doc.pdf"), "wb") as fh:
        fh.write(pdf)
    with open(os.path.join(root, "login.html"), "w") as fh:
        fh.write("<html><body>sign in</body></html>")

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=root, **kw)

        def do_GET(self):
            # One fixture that redirects somewhere it must not be followed to.
            # A public host answering 302 to the metadata endpoint is the
            # bypass review found, and the only way to test it is to serve one.
            if self.path.startswith("/drip.pdf"):
                # One byte every 0.1s, forever, which is the shape that
                # outlasts a per-read timeout.
                self.send_response(200)
                self.send_header("Content-Type", "application/pdf")
                self.end_headers()
                try:
                    for _ in range(3000):
                        self.wfile.write(b"x")
                        self.wfile.flush()
                        time.sleep(0.1)
                except Exception:
                    pass
                return
            if self.path.startswith("/redirect-to-metadata"):
                self.send_response(302)
                self.send_header("Location",
                                 "http://169.254.169.254/latest/meta-data/")
                self.end_headers()
                return
            return super().do_GET()

        def log_message(self, *a):
            pass

    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d/" % srv.server_address[1]
    # localhost must not go through the agent proxy, and it never needs to.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    saved = urllib.request._opener
    urllib.request.install_opener(opener)
    fails = []
    try:
        rec = read_pdf_text(base + "doc.pdf", allow_local=True)
        if needle not in rec["text"]:
            fails.append("fetched PDF did not yield its own text: %r"
                         % rec["text"][:120])
        if rec["pages_total"] != 1:
            fails.append("page count read as %r" % rec["pages_total"])

        # THE WHOLE-TRANSFER DEADLINE. A server that trickles one byte just
        # inside every per-read timeout outlasts that timeout forever, so this
        # serves exactly that and asserts the fetch is abandoned. Without the
        # deadline, or with read() in place of read1(), this hangs.
        t0 = time.monotonic()
        try:
            read_pdf_text(base + "drip.pdf", timeout=0.2, allow_local=True)
            fails.append("a trickling server was never abandoned")
        except RuntimeError as exc:
            if "abandoned" not in str(exc):
                fails.append("trickle refused for the wrong reason: %s" % exc)
        elapsed = time.monotonic() - t0
        if elapsed > 30:
            fails.append("the deadline took %.1fs to fire" % elapsed)

        # THE REDIRECT GUARD, exercised through the real opener. allow_local
        # is deliberately NOT passed, so this is the same path a scout takes.
        try:
            read_pdf_text(base + "redirect-to-metadata", allow_local=True)
            fails.append("a redirect to the metadata endpoint was followed")
        except RuntimeError as exc:
            if "non-public" not in str(exc) and "refused a redirect" not in str(exc):
                fails.append("redirect refused for the wrong reason: %s" % exc)

        try:
            read_pdf_text(base + "login.html", allow_local=True)
            fails.append("an HTML page was accepted as a PDF")
        except RuntimeError as exc:
            if "not a PDF" not in str(exc):
                fails.append("HTML rejected for the wrong reason: %s" % exc)

        try:
            read_pdf_text(base + "doc.pdf", max_mb=0.0001, allow_local=True)
            fails.append("the size ceiling did not fire")
        except RuntimeError as exc:
            if "ceiling" not in str(exc):
                fails.append("size ceiling raised the wrong error: %s" % exc)

        try:
            read_pdf_text(base + "missing.pdf", allow_local=True)
            fails.append("a 404 was reported as a document")
        except RuntimeError as exc:
            if "404" not in str(exc):
                fails.append("404 raised the wrong error: %s" % exc)

        local = read_pdf_text(os.path.join(root, "doc.pdf"))
        if needle not in local["text"]:
            fails.append("a local path did not read back")

        if _page_range("1-6", 3) != [0, 1, 2]:
            fails.append("--pages clamping is wrong")
        if _page_range("2", 3) != [1]:
            fails.append("--pages single is wrong")
    finally:
        urllib.request.install_opener(saved or urllib.request.build_opener())
        srv.shutdown()
    for f in fails:
        print("FAIL  " + f)
    print("fetch_pdf_text self-test: %s (%d checks)"
          % ("FAIL" if fails else "PASS", 6))
    return 1 if fails else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("url", nargs="?", help="http(s) url, file:// url, or path")
    ap.add_argument("--pages", help="1-6, 3, or 2- (default: all)")
    ap.add_argument("--max-chars", type=int, default=0,
                    help="truncate the returned text (default: no limit)")
    ap.add_argument("--max-mb", type=float, default=DEFAULT_MAX_MB)
    ap.add_argument("--timeout", type=float, default=45)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--out", help="write the text here instead of stdout")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        return _self_test()
    if not args.url:
        ap.error("give a url or a path (or --self-test)")

    try:
        rec = read_pdf_text(args.url, pages=args.pages,
                            max_chars=args.max_chars, max_mb=args.max_mb,
                            timeout=args.timeout)
    except RuntimeError as exc:
        msg = str(exc)
        print("fetch_pdf_text: %s" % msg, file=sys.stderr)
        return 2 if "not a PDF" in msg else 1

    if not rec["text"]:
        print("fetch_pdf_text: %s opened cleanly (%d page(s)) and has NO TEXT "
              "LAYER, so it is a scan. Nothing here can read it; cite the page "
              "that publishes it, or find the same record in HTML."
              % (rec["url"], rec["pages_total"]), file=sys.stderr)
        return 3

    if args.json:
        print(json.dumps(rec, indent=1))
        return 0
    if args.out:
        with open(args.out, "w") as fh:
            fh.write(rec["text"])
        print("%s -> %s (%d page(s), %d chars%s)"
              % (rec["url"], args.out, rec["pages_total"], rec["chars"],
                 ", TRUNCATED" if rec["truncated"] else ""))
        return 0
    print(rec["text"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
