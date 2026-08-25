#!/usr/bin/env python3
"""コード通訳: 解析器。対象リポジトリを読み、機械検査(簡易)とAI翻訳を行い view-data.json を出力する。

実装AIのセッションには一切触れない(完全分離)。読むのはファイルとGit履歴のみ。
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

CODE_EXTS = {".js", ".ts", ".jsx", ".tsx", ".py", ".swift", ".rb", ".go", ".java", ".php", ".mjs"}
CONFIG_EXTS = {".yml", ".yaml", ".env", ".toml", ".ini", ".plist", ".xml"}
SKIP_DIRS = {".git", "node_modules", ".code-translate", "__pycache__", "dist", "build", ".venv"}
MAX_FILE_BYTES = 60_000
MAX_TOTAL_CHARS = 60_000
MAX_LINES = 300

MSGS = {
    "ja": {
        "encoding": "文字コードを読めませんでした",
        "symlink": "リンク(シンボリックリンク)のため未解析",
        "too_long": "300行を超えるため未解析(この版の上限)",
        "web_asset": "HTML/CSS/JSON類はこの版では解析対象外",
        "gap": "(AIの分割から漏れた行)",
        "gap_prose": "この数行はAIの自動分割に含まれませんでした。右のコードを直接確認してください。",
        "too_large": "ファイルが大きすぎるため未解析",
        "config": "設定ファイル(この版では解析対象外)",
        "unsupported": "この形式は未対応のため未解析",
        "truncated": "容量上限のため未解析",
        "secret": "秘密の値(APIキー等)の直書きを検出",
        "sql": "命令文の文字列連結を検出(不正な命令混入の恐れ)",
        "pii": "個人情報らしき値のログ出力を検出",
        "delete": "削除系の操作を検出",
        "url": "外部ホストへの参照",
    },
    "en": {
        "encoding": "Could not decode the file",
        "symlink": "Skipped: symbolic link",
        "too_long": "Skipped: over 300 lines (limit of this version)",
        "web_asset": "HTML/CSS/JSON files are not analyzed in this version",
        "gap": "(lines missed by the AI split)",
        "gap_prose": "These lines were not covered by the AI's split. Check the code on the right directly.",
        "too_large": "Skipped: file too large",
        "config": "Config file (not analyzed in this version)",
        "unsupported": "Skipped: unsupported file type",
        "truncated": "Skipped: size limit reached",
        "secret": "Hardcoded secret (API key etc.) detected",
        "sql": "String-concatenated query detected (injection risk)",
        "pii": "Personal data written to logs detected",
        "delete": "Delete operation detected",
        "url": "Reference to external host",
    },
}

SECRET_RE = re.compile(
    r"""(?i)(\w*(api[_-]?key|secret|token|passw(or)?d)\w*\s*[:=]\s*['"][^'"]{8,}['"]"""
    r"""|['"](sk_live_|sk_test_|AKIA|ghp_|xox[bp]-)[A-Za-z0-9_\-]{6,}['"])""")
URL_RE = re.compile(r"https?://[\w.\-]+")
DELETE_RE = re.compile(r"(?i)(delete|drop|destroy|remove|truncate)\w*\s*\(")
SQL_CONCAT_RE = re.compile(r"""['"][^'"]*(<|>|=|where|select|delete)[^'"]*['"]\s*\+""", re.I)
LOG_PII_RE = re.compile(r"(?i)log\w*\.\w+\([^)]*(email|phone|address|name|tel|card)")


def sh(cmd, cwd=None, timeout=300):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def collect_files(root: Path, lang="ja"):
    M = MSGS[lang]
    analyzed, unanalyzed = [], []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        rel = str(p.relative_to(root))
        ext = p.suffix.lower()
        if p.is_symlink():
            if ext in CODE_EXTS or ext in CONFIG_EXTS:
                unanalyzed.append({"path": rel, "reason": M["symlink"]})
            continue
        if ext in CODE_EXTS and p.stat().st_size <= MAX_FILE_BYTES:
            try:
                text = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                unanalyzed.append({"path": rel, "reason": M["encoding"]})
                continue
            if len(text.splitlines()) > MAX_LINES:
                unanalyzed.append({"path": rel, "reason": M["too_long"]})
                continue
            analyzed.append({"path": rel, "text": text})
        elif ext in CODE_EXTS:
            unanalyzed.append({"path": rel, "reason": M["too_large"]})
        elif ext in CONFIG_EXTS:
            unanalyzed.append({"path": rel, "reason": M["config"]})
        elif ext in {".html", ".css", ".json"}:
            unanalyzed.append({"path": rel, "reason": M["web_asset"]})
        elif ext in {".md", ".txt", ".lock", ".png", ".jpg", ".gitignore"} or p.name.startswith("."):
            continue  # 文書・画像類は台帳に載せない
        else:
            unanalyzed.append({"path": rel, "reason": M["unsupported"]})
    return analyzed, unanalyzed


def machine_scan(files, lang="ja"):
    M = MSGS[lang]
    findings = []
    for f in files:
        for i, line in enumerate(f["text"].splitlines(), 1):
            if SECRET_RE.search(line):
                findings.append({"file": f["path"], "line": i, "kind": "secret",
                                 "severity": "critical", "note": M["secret"]})
            if SQL_CONCAT_RE.search(line):
                findings.append({"file": f["path"], "line": i, "kind": "sql-concat",
                                 "severity": "high", "note": M["sql"]})
            if LOG_PII_RE.search(line):
                findings.append({"file": f["path"], "line": i, "kind": "log-pii",
                                 "severity": "high", "note": M["pii"]})
            if DELETE_RE.search(line):
                findings.append({"file": f["path"], "line": i, "kind": "delete",
                                 "severity": "medium", "note": M["delete"]})
            for m in URL_RE.findall(line):
                findings.append({"file": f["path"], "line": i, "kind": "external-url",
                                 "severity": "info", "note": f"{M['url']}: {m}"})
    return findings


def git_info(root: Path, paths):
    info = {"is_repo": False, "commit": None, "dirty": False, "authors": {}}
    r = sh(["git", "rev-parse", "HEAD"], cwd=root)
    if r.returncode != 0:
        return info
    info["is_repo"] = True
    info["commit"] = r.stdout.strip()
    status = [l for l in sh(["git", "status", "--porcelain"], cwd=root).stdout.splitlines()
              if l[3:] and not l[3:].startswith(".code-translate")]
    info["dirty"] = bool(status)
    for p in paths:
        a = sh(["git", "log", "-1", "--format=%an", "--", p], cwd=root).stdout.strip()
        if a:
            info["authors"][p] = a
    return info


def compute_seal(files, git):
    h = hashlib.sha256()
    for f in files:
        h.update(f["path"].encode())
        h.update(hashlib.sha256(f["text"].encode()).digest())
    digest = h.hexdigest()[:12]
    if git["is_repo"]:
        return {"kind": "git+hash", "commit": git["commit"][:12], "hash": digest, "dirty": git["dirty"]}
    return {"kind": "hash", "commit": None, "hash": digest, "dirty": False}


def numbered(text, limit=300):
    lines = text.splitlines()[:limit]
    return "\n".join(f"{i}: {l}" for i, l in enumerate(lines, 1))


PROMPT_HEAD = """あなたは「コード通訳」——コードを読めない発注者のために、コードの意味とリスクを日本語で翻訳する独立監査者です。実装者の説明は一切参照せず、以下のコードだけを根拠にしてください。

出力は次のスキーマのJSONオブジェクト1個のみ。前後に文章・コードフェンスを付けないこと。
{
  "app_summary": "このシステム全体が何をするものかの平易な説明(2〜3文、業務の言葉で)",
  "file_roles": {"ファイルパス": "そのファイルの役割ひとこと"},
  "cards": [
    {
      "id": "c1",
      "category": 1〜6の整数,
      "file": "ファイルパス",
      "lines": "開始-終了 (単一行なら同じ数字)",
      "title": "見出し(体言止め、20字以内)",
      "body": "何が起きるかの説明。業務の言葉で2〜3文。クラス名や専門用語を使わない。断定できないことは断定しない",
      "severity": "high|medium|low",
      "learn_note": "この箇所のコードの読み方を1〜2文で(構文の目印つき、学習者向け)"
    }
  ],
  "line_translations": [
    {"file": "ファイルパス", "line": 行番号, "translation": "その行の読み下し(平易な日本語)", "marks": "構文の目印(例: if=もし〜なら)。無ければ空文字"}
  ],
  "sections": [
    {"file": "ファイルパス", "lines": "開始-終了", "heading": "このまとまりの一行見出し(20字以内・体言止め)", "prose": "このまとまりが何をするかの説明。業務の言葉で1〜3文、最大120字。"}
  ]
}

カテゴリ定義(急所6分類): 1=外部への送信・出口 2=高影響な外部作用(課金・削除・本番反映・通知) 3=機密・個人データの扱い 4=権限・認証の境界 5=異常時の安全動作・二重実行 6=依存・供給網

規律:
- カードは「事故につながり得る箇所」を優先し、該当が無いカテゴリは無理に作らない(最大8枚)。
- 機械検査の検出結果を下に添付する。対応するカードには必ずその内容を反映する。
- 分からないこと・コードから読み取れないことは「コードからは確認できません」と書く。安心させる誇張をしない。
- line_translations は各ファイルの全行(空行・閉じ括弧のみの行は省略可)。
- sections は各ファイルを先頭から順に、2〜8行の「意味のまとまり」で漏れなく分割する
  (空行・閉じ括弧は前のまとまりに含める。まとまり同士は重複しない)。
  見出しは「何をする数行か」を先に言い切る要約でよい。
"""


def build_prompt(files, findings, lang="ja"):
    parts = [PROMPT_HEAD]
    if lang == "en":
        parts.append(
            "\n## 出力言語の指定(最重要)\n"
            "すべての出力テキスト(app_summary, file_roles, cards の title/body/learn_note, "
            "line_translations の translation/marks, sections の heading/prose)を"
            "**平易な英語(plain English)**で書くこと。読者は英語話者の非エンジニア。\n")
    parts.append("\n## 機械検査(簡易)の検出結果\n")
    if findings:
        for f in findings:
            parts.append(f"- {f['file']}:{f['line']} [{f['kind']}/{f['severity']}] {f['note']}\n")
    else:
        parts.append("- 検出なし\n")
    parts.append("\n## 対象コード\n")
    total = 0
    for f in files:
        body = numbered(f["text"])
        total += len(body)
        if total > MAX_TOTAL_CHARS:
            parts.append(f"\n### {f['path']}\n(容量上限のため本文省略——このファイルのカードは作らず、未解析として扱う)\n")
            f["truncated"] = True
            continue
        parts.append(f"\n### {f['path']}\n```\n{body}\n```\n")
    return "".join(parts)


def call_claude(prompt, model):
    import shutil
    if not shutil.which("claude"):
        print("エラー: Claude Code CLI(claudeコマンド)が見つかりません。\n"
              "翻訳の生成に必要です。https://claude.com/claude-code からインストールし、"
              "一度 `claude` を起動してログインしてから再実行してください。", file=sys.stderr)
        sys.exit(2)
    cmd = ["claude", "-p", prompt, "--output-format", "json", "--model", model]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        print("エラー: AI翻訳が時間内に完了しませんでした(10分)。ネットワークを確認して再実行してください。", file=sys.stderr)
        sys.exit(2)
    if r.returncode != 0:
        print("エラー: AI翻訳の実行に失敗しました。`claude` に一度ログインできているか確認してください。\n"
              f"詳細: {r.stderr[:300]}", file=sys.stderr)
        sys.exit(2)
    try:
        outer = json.loads(r.stdout)
        text = outer.get("result", "")
        meta = {"cost_usd": outer.get("total_cost_usd"), "duration_ms": outer.get("duration_ms"), "model": model}
        m = re.search(r"\{.*\}", text, re.S)
        if not m:
            raise ValueError("no json")
        return json.loads(m.group(0)), meta
    except (json.JSONDecodeError, ValueError):
        print("エラー: AIの応答を読み取れませんでした(一時的な不調の可能性)。--force を付けて再実行してください。", file=sys.stderr)
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--model", default="claude-sonnet-4-5")
    ap.add_argument("--out", default=None)
    ap.add_argument("--force", action="store_true", help="封印一致でも再翻訳する")
    ap.add_argument("--lang", default="ja", choices=["ja", "en"], help="翻訳の出力言語")
    args = ap.parse_args()

    root = Path(args.target).expanduser().resolve()
    out_dir = Path(args.out).expanduser() if args.out else root / ".code-translate" / "view"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "view-data.json"

    t0 = time.time()
    analyzed, unanalyzed = collect_files(root, args.lang)
    if not analyzed:
        print("解析対象のコードファイルが見つかりません", file=sys.stderr)
        sys.exit(1)
    findings = machine_scan(analyzed, args.lang)
    git = git_info(root, [f["path"] for f in analyzed])
    seal = compute_seal(analyzed, git)

    prev = None
    if out_file.exists():
        try:
            prev = json.loads(out_file.read_text())
        except Exception:
            prev = None
    if prev and not args.force and prev.get("seal", {}).get("hash") == seal["hash"] and prev.get("lang") == args.lang:
        if prev.get("seal") != seal:
            prev["seal"] = seal
            prev["generated_at"] = datetime.now(timezone.utc).isoformat()
            out_file.write_text(json.dumps(prev, ensure_ascii=False, indent=1))
            print("コードは変更なし。封印情報のみ更新しました。")
        else:
            print("変更なし(封印一致)。再翻訳をスキップしました。")
        return

    prompt = build_prompt(analyzed, findings, args.lang)
    ai, meta = call_claude(prompt, args.model)

    for f in analyzed:
        if f.pop("truncated", False):
            unanalyzed.append({"path": f["path"], "reason": MSGS[args.lang]["truncated"]})

    # AI出力の検証: 「意味のまとまり」が無ければ失敗として扱い、分割から漏れた行は正直に台帳へ載せる
    sections = ai.get("sections", [])
    if not sections:
        print("エラー: AI出力に『意味のまとまり』が含まれていません。--force を付けて再実行してください。", file=sys.stderr)
        sys.exit(2)
    for f in analyzed:
        lines = f["text"].splitlines()
        covered = set()
        for s in sections:
            if s.get("file") != f["path"]:
                continue
            m = re.match(r"^(\d+)(?:-(\d+))?$", str(s.get("lines", "")).strip())
            if not m:
                continue
            covered.update(range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1))
        gap_start = None
        for i in range(1, len(lines) + 2):
            missing = i <= len(lines) and i not in covered and lines[i - 1].strip() != ""
            if missing and gap_start is None:
                gap_start = i
            elif not missing and gap_start is not None:
                sections.append({"file": f["path"], "lines": f"{gap_start}-{i - 1}",
                                 "heading": MSGS[args.lang]["gap"], "prose": MSGS[args.lang]["gap_prose"]})
                gap_start = None
    sections.sort(key=lambda s: (s.get("file", ""), int(str(s.get("lines", "1")).split("-")[0] or 1)))
    ai["sections"] = sections

    data = {
        "lang": args.lang,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": str(root),
        "project_name": root.name,
        "seal": seal,
        "app_summary": ai.get("app_summary", ""),
        "files": [
            {
                "path": f["path"],
                "role": ai.get("file_roles", {}).get(f["path"], ""),
                "author": git["authors"].get(f["path"], ""),
                "lines": f["text"].splitlines()[:300],
            }
            for f in analyzed
        ],
        "unanalyzed": unanalyzed,
        "cards": ai.get("cards", []),
        "line_translations": ai.get("line_translations", []),
        "sections": ai.get("sections", []),
        "machine_findings": findings,
        "meta": {**meta, "elapsed_s": round(time.time() - t0, 1)},
    }
    out_file.write_text(json.dumps(data, ensure_ascii=False, indent=1).replace("�", ""))
    print(f"OK: {out_file}  cards={len(data['cards'])} 未解析={len(unanalyzed)} "
          f"cost=${meta['cost_usd']} elapsed={data['meta']['elapsed_s']}s")


if __name__ == "__main__":
    main()
