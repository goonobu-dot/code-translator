# コード通訳 (code-translator)

**コードを読めない人が、AIの書いたコードを日本語で読んで、確認できるツール。**

> **English**: A tool for non-engineers to read and review AI-generated code in plain language —
> code is shown in few-line "units of meaning" with parallel explanations, and you review each unit
> with ✓ (looks right) / ✗ (wrong) / ? (not sure) plus free comments. Answers are saved to a file the AI
> can read to apply fixes. **English output and English UI**: run with `--lang en`.
> **[English manual (with screenshots)](docs/manual.en.md)**

コードを数行の「意味のまとまり」ごとに日本語対訳で表示し、それぞれに
**✓ 問題ない / ✗ おかしい / ? わからない** とコメントで答えるだけで、
「公開してよいか」を自分の言葉で判断した記録が残ります。

**📘 [操作マニュアル(スクリーンショット付き・5分)](docs/manual.md)** · **[English manual](docs/manual.en.md)**

## 使い方は3ステップ

```bash
# 1. 取得(Claude Codeスキル連携のため、この場所に置くのがおすすめ)
git clone https://github.com/goonobu-dot/code-translator.git ~/Projects/code-translator
cd ~/Projects/code-translator

# 2. コマンド登録(初回のみ)
mkdir -p ~/.local/bin && ln -sf "$PWD/bin/code-translate" ~/.local/bin/code-translate

# 3. 翻訳して開く(ブラウザが自動で開きます)
code-translate ~/あなたのアプリのフォルダ --open
```

英語で使う場合(English output + English UI): `code-translate <project> --open --lang en`

初回実行時、対象フォルダに **「コード通訳を開く.command」** が置かれます。
**次からはこのファイルをダブルクリックするだけ**で画面が開きます。

Claude Codeを使っている場合は、`skill/` を `~/.claude/skills/code-translate/` に
コピーすると、チャットで「**コードを翻訳して**」と言うだけで動きます。

## 画面でできること

- **読む**: 左に日本語の見出し+説明、右に該当コード(数行の意味のまとまり単位)
- **答える**: 各まとまりに ✓/✗/? を押す。全部✓なら一番下が「✅確認できました」に
- **コメント**: 「ここは確認画面を挟んで」など自由に書ける。回答とコメントは
  `対象/.code-translate/view/review.json` に保存され、AIが読んで修正に使える
- **学習モード**: 説明を伏せて「コードを読んで予想→クリックで答え合わせ」
- ⚠の付いたまとまりは要注意箇所(自動チェック+AIの読み取り)。右下のボタンで順に巡れます

## 前提・設計方針

- 必要なもの: Python 3 / Git / [Claude Code CLI](https://claude.com/claude-code)(翻訳の生成に使用。目安: 小さいアプリで1回 約2分・$0.1〜0.3)
- コードに変更がなければ再翻訳せずスキップ(費用ゼロ)
- **翻訳は実装とは別プロセスで行い、開発を止めない**(完全分離・非ブロッキング)
- **「安全です」とは言わない**: 読めていないファイルは「未読」と赤で表示し、
  未回答・✗・?が残る限り判定は緑になりません(証跡を安心材料として誇張しない)

## 構成

- `bin/code-translate` — 翻訳〜画面表示までの一発コマンド
- `analyzer/analyze.py` — 機械検査(簡易)+AI翻訳 → view-data.json
- `generator/view-app.html` — 画面本体 / `generator/serve.py` — 配信+回答保存サーバー
- `skill/` — Claude Code用スキル(「コードを翻訳して」/翻訳モード/作業履歴)
- `examples/sample-app/` — デモ用サンプル

## 既知の限界

- 機械検査は簡易(候補発見用)。AST・動的解析は未実装
- 翻訳はAI生成のため誤りうる。コードとの突き合わせ(対訳表示)を前提とする
- 判定は表示であり、デプロイを物理的に止める仕組み(release-gate)は今後の課題
