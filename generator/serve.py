#!/usr/bin/env python3
"""コード通訳: ビュー配信サーバー。静的配信+回答/コメントの保存(POST /save)を行う。

セキュリティ方針:
- 127.0.0.1 のみで待ち受け、Host/Origin ヘッダを検証する(DNSリバインディング/CSRF対策)
- 書き込みはビューディレクトリ内の review.json のみ。シンボリックリンクなら拒否
- 書き込みは一時ファイル+原子的置換、スレッドロック付き(破損・逆転防止)
"""
import http.server
import json
import os
import sys
import tempfile
import threading
from pathlib import Path

DIR = Path(sys.argv[1]).expanduser().resolve()
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8931
MAX_BYTES = 1_000_000
ALLOWED_HOSTS = {f"127.0.0.1:{PORT}", f"localhost:{PORT}", "127.0.0.1", "localhost"}
ALLOWED_ORIGINS = {f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}"}
_lock = threading.Lock()


class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map,
                      ".html": "text/html; charset=utf-8",
                      ".json": "application/json; charset=utf-8"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIR), **kwargs)

    def _reject(self, code, msg):
        self.send_error(code, msg)

    def do_POST(self):
        if self.path != "/save":
            return self._reject(404, "not found")
        host = self.headers.get("Host", "")
        if host not in ALLOWED_HOSTS:
            return self._reject(403, "bad host")
        origin = self.headers.get("Origin")
        if origin and origin not in ALLOWED_ORIGINS:
            return self._reject(403, "bad origin")
        if "application/json" not in (self.headers.get("Content-Type") or ""):
            return self._reject(415, "json only")
        n = int(self.headers.get("Content-Length", 0))
        if n > MAX_BYTES:
            return self._reject(413, "too large")
        try:
            data = json.loads(self.rfile.read(n))
            assert isinstance(data, dict)
        except Exception:
            return self._reject(400, "bad json")
        target = DIR / "review.json"
        if target.is_symlink():
            return self._reject(403, "refusing symlink")
        with _lock:
            fd, tmp = tempfile.mkstemp(dir=str(DIR), prefix=".review-", suffix=".tmp")
            try:
                with os.fdopen(fd, "w") as f:
                    f.write(json.dumps(data, ensure_ascii=False, indent=1))
                os.replace(tmp, target)
            finally:
                if os.path.exists(tmp):
                    os.unlink(tmp)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
