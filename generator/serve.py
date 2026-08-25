#!/usr/bin/env python3
"""コード通訳: ビュー配信サーバー。静的配信+回答/コメントの保存(POST /save)を行う。

保存先はビューディレクトリ内の review.json のみ(それ以外のパスへは書かない)。
"""
import http.server
import json
import sys
from pathlib import Path

DIR = Path(sys.argv[1]).expanduser().resolve()
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8931
MAX_BYTES = 1_000_000


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIR), **kwargs)

    def do_POST(self):
        if self.path != "/save":
            self.send_error(404)
            return
        n = int(self.headers.get("Content-Length", 0))
        if n > MAX_BYTES:
            self.send_error(413)
            return
        try:
            data = json.loads(self.rfile.read(n))
            assert isinstance(data, dict)
        except Exception:
            self.send_error(400)
            return
        (DIR / "review.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok":true}')

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
