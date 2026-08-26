#!/usr/bin/env python3
"""翻訳済みプロジェクトの一覧(ホーム画面)を作る。

使い方: build_home.py <出力先.html> "<表示名>=<URL>=<プロジェクトのパス>" ...
リンク先は各プロジェクトの公開ページ。件数などは view-data.json から読む。
"""
import html
import json
import sys
from datetime import datetime
from pathlib import Path

STYLE = """
:root { --bg:#F7F8F7; --surface:#FFF; --ink:#242B2E; --muted:#67736F; --line:#E2E5E0;
  --accent:#0E7C66; --crit-bg:#FBEAE8; --crit-fg:#791F1F; --warn-bg:#FBF3E1; --warn-fg:#633806; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg:#14181A; --surface:#1D2326; --ink:#E4E8E4; --muted:#96A29E; --line:#2C3538;
  --accent:#3FB392; --crit-bg:#331E1C; --crit-fg:#E88B81; --warn-bg:#2E2718; --warn-fg:#E0B45E; } }
:root[data-theme="dark"] { --bg:#14181A; --surface:#1D2326; --ink:#E4E8E4; --muted:#96A29E;
  --line:#2C3538; --accent:#3FB392; --crit-bg:#331E1C; --crit-fg:#E88B81; --warn-bg:#2E2718; --warn-fg:#E0B45E; }
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--ink);
  font-family:"Hiragino Kaku Gothic ProN","Noto Sans JP",sans-serif; font-size:14px; line-height:1.8; }
main { max-width:760px; margin:0 auto; padding:28px 20px 60px; }
h1 { font-size:19px; margin:0 0 4px; }
.sub { color:var(--muted); font-size:12.5px; margin-bottom:22px; }
a.card { display:block; text-decoration:none; color:inherit; background:var(--surface);
  border:1px solid var(--line); border-radius:12px; padding:14px 18px; margin-bottom:12px; }
a.card:hover { border-color:var(--accent); }
.name { font-weight:700; font-size:16px; }
.meta { color:var(--muted); font-size:12.5px; margin-top:3px; }
.tags { margin-top:8px; display:flex; gap:6px; flex-wrap:wrap; }
.tag { font-size:11.5px; padding:1px 10px; border-radius:999px; background:var(--warn-bg); color:var(--warn-fg); }
.tag.red { background:var(--crit-bg); color:var(--crit-fg); font-weight:700; }
.tag.plain { background:transparent; color:var(--muted); border:1px solid var(--line); }
.how { background:var(--surface); border-left:3px solid var(--accent); border-radius:8px;
  padding:12px 16px; margin-top:24px; font-size:13px; }
.how b { color:var(--accent); }
.how ol { margin:8px 0 0; padding-left:1.4em; }
"""


def risk_level(c):
    sev = {"high": 3, "medium": 2, "low": 1}.get(c.get("severity"), 1)
    heavy = c.get("category") in (1, 2, 3)
    return 3 if sev == 3 or (heavy and sev == 2) else 2 if sev == 2 or heavy else 1


def main():
    out = Path(sys.argv[1]).expanduser()
    cards = []
    for spec in sys.argv[2:]:
        name, url, path = spec.split("=", 2)
        data_file = Path(path).expanduser() / ".code-translate" / "view" / "view-data.json"
        files = secs = red = 0
        when = ""
        if data_file.exists():
            d = json.loads(data_file.read_text())
            files, secs = len(d.get("files", [])), len(d.get("sections", []))
            red = sum(1 for c in d.get("cards", []) if risk_level(c) == 3)
            try:
                when = datetime.fromisoformat(d["generated_at"].replace("Z", "+00:00")).astimezone().strftime("%m/%d %H:%M")
            except Exception:
                when = ""
        tags = [f'<span class="tag red">🔴 重大 {red}件</span>'] if red else []
        tags.append(f'<span class="tag plain">{files}ファイル / {secs}か所</span>')
        cards.append(
            f'<a class="card" href="{html.escape(url)}">'
            f'<div class="name">{html.escape(name)}</div>'
            f'<div class="meta">最後に読めるようにした日時: {when or "—"}</div>'
            f'<div class="tags">{"".join(tags)}</div></a>'
        )

    body = (
        '<meta charset="utf-8">\n<title>コード通訳 ホーム</title>\n'
        f"<style>{STYLE}</style>\n<main>"
        "<h1>📖 コード通訳</h1>"
        '<div class="sub">読みたいプロジェクトを押してください。</div>'
        + "".join(cards)
        + '<div class="how"><b>使い方はこれだけ</b>'
          "<ol><li>上から読みたいものを押す</li>"
          "<li><b>🔴 危ない所だけ</b> を押すと要点だけ見えます</li>"
          "<li>気になった所は <b>✗</b> を押して <b>📮 指摘をAIへ送る</b></li>"
          "<li>チャットで「<b>指摘を直して</b>」と言えばAIが直します</li></ol>"
          '<div style="margin-top:10px;color:var(--muted);font-size:12.5px">'
          "新しく読めるようにしたいときは、チャットで「<b>◯◯のコードを見せて</b>」と言ってください。</div></div>"
        "</main>"
    )
    out.write_text(body)
    print(out)


if __name__ == "__main__":
    main()
