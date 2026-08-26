#!/usr/bin/env python3
"""view-data.json を埋め込んだ自己完結ページ(Artifact用)を生成する。"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    target = Path(sys.argv[1]).expanduser().resolve()
    data_file = target / ".code-translate" / "view" / "view-data.json"
    out_file = target / ".code-translate" / "artifact.html"
    data = data_file.read_text().replace("�", "")
    # コード中の "</script>" や "<!--" はページ内のデータを途中で断ち切るため無害化する
    # (JSONの文字列としては \/ も ! も同じ文字を表すので、中身は一切変わらない)
    data = data.replace("</", "<\\/").replace("<!--", "<\\u0021--")
    src = (ROOT / "view-app.html").read_text()

    style = re.search(r"<style>.*?</style>", src, re.S).group(0)
    body = re.search(r"<body>(.*)</body>", src, re.S).group(1)
    title = json.loads(data).get("project_name", "view")

    out = (
        '<meta charset="utf-8">\n'
        f"<title>コード通訳 {title}</title>\n"
        + style + "\n"
        + f"<script>window.EMBEDDED_DATA = {data};</script>\n"
        + body
    )
    out_file.write_text(out)
    print(out_file)


if __name__ == "__main__":
    main()
