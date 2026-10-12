#!/usr/bin/env python3
"""本地预览 README.md：python3 preview/serve.py [port]"""
import http.server
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(ROOT, "README.md")
INDEX = os.path.join(ROOT, "preview", "index.html")
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, body, ctype):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/":
            with open(INDEX, "rb") as f:
                self._send(f.read(), "text/html; charset=utf-8")
        elif path == "/README.md":
            with open(README, "rb") as f:
                self._send(f.read(), "text/markdown; charset=utf-8")
        elif path == "/__mtime":
            svg = os.path.join(ROOT, "assets", "terminal.svg")
            m = max(os.stat(p).st_mtime_ns for p in (README, svg) if os.path.exists(p))
            self._send(str(m).encode(), "text/plain")
        elif path.startswith("/assets/"):
            f = os.path.realpath(os.path.join(ROOT, path.lstrip("/")))
            if not f.startswith(os.path.join(ROOT, "assets") + os.sep) or not os.path.isfile(f):
                return self.send_error(404)
            ctype = "image/svg+xml" if f.endswith(".svg") else "application/octet-stream"
            with open(f, "rb") as fh:
                self._send(fh.read(), ctype)
        else:
            self.send_error(404)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    print(f"Preview: http://127.0.0.1:{PORT}")
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
