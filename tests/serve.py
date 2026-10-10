"""Serve the repo over HTTP for the tests. The app fetches its question banks (data/*.json) and 3D files at
runtime, which file:// pages cannot do. Text, JS, JSON and models are gzipped, like GitHub Pages does.

    from serve import start
    URL = start() + "index.html"
"""
import gzip
import http.server
import io
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_gz = {}   # path -> (mtime, size, gzipped bytes): the 3D tests fetch the same multi-megabyte models many times


def gzipped(path):
    st = path.stat()
    hit = _gz.get(path)
    if hit and hit[0] == st.st_mtime and hit[1] == st.st_size:
        return hit[2]
    body = gzip.compress(path.read_bytes(), 6)
    _gz[path] = (st.st_mtime, st.st_size, body)
    return body


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".js": "text/javascript", ".json": "application/json",
                      ".glb": "model/gltf-binary", ".html": "text/html; charset=utf-8"}

    def __init__(self, *args, **kw):
        super().__init__(*args, directory=str(ROOT), **kw)

    def log_message(self, *args):
        pass

    def send_head(self):
        path = Path(self.translate_path(self.path))
        if path.is_dir():
            path = path / "index.html"
        if "gzip" not in self.headers.get("Accept-Encoding", "") or not path.is_file() or path.suffix not in (".html", ".js", ".json", ".glb"):
            return super().send_head()
        body = gzipped(path)
        self.send_response(200)
        self.send_header("Content-Type", self.guess_type(str(path)))
        self.send_header("Content-Encoding", "gzip")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        return io.BytesIO(body)


class Server(http.server.ThreadingHTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        # The browser cancels downloads it no longer needs (a route abort, a reload mid-fetch). That is normal; keep quiet.
        import sys
        err = sys.exc_info()[1]
        if isinstance(err, (ConnectionAbortedError, ConnectionResetError, BrokenPipeError)):
            return
        super().handle_error(request, client_address)


def start():
    """Start a background server on a free port and return its base URL (ends with /)."""
    srv = Server(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{srv.server_address[1]}/"
