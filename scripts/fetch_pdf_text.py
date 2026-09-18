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
import io
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

# Federal and state document servers routinely 403 a bare urllib UA while
# serving the same file to a browser. This is the ordinary desktop string; it
# claims nothing untrue about what is fetching, and every host below is
# publishing the document for the public to read.
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/141.0.0.0 Safari/537.36")
DEFAULT_MAX_MB = 48
CHUNK = 1 << 16


def _fetch(url, max_mb, timeout):
    """Return (bytes, final_url, content_type) or raise RuntimeError."""
    parsed = urllib.parse.urlparse(url)
    if not parsed.scheme or (len(parsed.scheme) == 1 and os.name == "nt"):
        url = "file://" + os.path.abspath(url)
        parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in ("http", "https", "file"):
        raise RuntimeError("scheme %r is not fetchable here; pass an http(s) "
                           "url or a local path" % parsed.scheme)
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "application/pdf,*/*",
    })
    limit = int(max_mb * 1024 * 1024)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            ctype = (resp.headers.get("Content-Type") or "").split(";")[0].strip()
            buf = io.BytesIO()
            while True:
                chunk = resp.read(CHUNK)
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
                  timeout=45):
    data, final, ctype = _fetch(url, max_mb, timeout)
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
        rec = read_pdf_text(base + "doc.pdf")
        if needle not in rec["text"]:
            fails.append("fetched PDF did not yield its own text: %r"
                         % rec["text"][:120])
        if rec["pages_total"] != 1:
            fails.append("page count read as %r" % rec["pages_total"])

        try:
            read_pdf_text(base + "login.html")
            fails.append("an HTML page was accepted as a PDF")
        except RuntimeError as exc:
            if "not a PDF" not in str(exc):
                fails.append("HTML rejected for the wrong reason: %s" % exc)

        try:
            read_pdf_text(base + "doc.pdf", max_mb=0.0001)
            fails.append("the size ceiling did not fire")
        except RuntimeError as exc:
            if "ceiling" not in str(exc):
                fails.append("size ceiling raised the wrong error: %s" % exc)

        try:
            read_pdf_text(base + "missing.pdf")
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
