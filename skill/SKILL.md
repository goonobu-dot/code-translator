---
name: code-translate
description: 非エンジニア向け「コード通訳」。コードを数行の意味のまとまりごとに日本語対訳で表示し、各まとまりに「✓問題ない/✗おかしい/?わからない」とコメントで答えられる1画面ビューを提供する。ユーザーが「コードを翻訳して」「翻訳ビューを開いて」「コード通訳」「/code-translate」と言ったとき必ず使用する。「翻訳モードON/OFF」(編集差分の自動対訳)、「作業履歴を翻訳して」(Git履歴の日本語タイムライン)、「たまった指摘を直して」(review.jsonの✗とコメントの一括対応)もこのスキルが扱う。コード全体の地図はcode-atlas、証拠付き監査報告書はai-auditを使う。Use when a non-engineer user asks to translate project code into plain Japanese with per-section approve/reject/unknown review and comments.
---

# code-translate — コード通訳

ツール本体: `~/Projects/code-translator/`(README.md参照)。設計の憲法:
**完全分離**(実装セッションに触れない)・**非ブロッキング**(開発を止めない)・
**証跡を麻酔にしない**(未読・未回答・✗・?が残る限り判定を緑にしない)。

## 起動(「コードを翻訳して」)

1. 対象=指定がなければ現在の作業ディレクトリ(コードが無ければ確認する)。
2. `<対象>/.code-translate/paused` があれば「一時停止中。再開する?」と確認。
3. 実行(数十秒〜数分かかるのでバックグラウンド推奨。完了時にコスト・所要を報告):
   `~/Projects/code-translator/bin/code-translate <対象>`
   - 封印一致なら再翻訳せずスキップ(費用ゼロ)。
4. 表示(ユーザーの好みで。迷ったらa):
   a. **チャットに直接**: view-data.json の sections を「見出し+説明|コード」で
      ウィジェット表示(⚠は警告色)。short questions には該当部分だけでよい。
   b. **ブラウザで開く**: `code-translate <対象> --open`(サーバー起動+ブラウザ表示+
      対象フォルダに「コード通訳を開く.command」ボタンを設置。以後ユーザーはダブルクリックで開ける)。
   c. **Artifact**: `python3 ~/Projects/code-translator/generator/build_artifact.py <対象>` で
      self-containedページを作り同一URLへ再公開(ctrl+]・スマホ向け。回答保存は端末内のみ)。

## 画面の回答を修正につなげる(「たまった指摘を直して」)

回答とコメントは `<対象>/.code-translate/view/review.json` に保存される
(現在の封印hashのキー配下。v: ok|ng|uk、comment)。
「たまった指摘を直して」と言われたら: review.json を読み、✗(ng)とコメントの各項目を
ユーザーに要約提示 → 承認を得て修正 → コミット → `code-translate <対象>` で再翻訳
(封印が変わると古い回答は自動失効する。これは仕様)。

## 翻訳モード(差分の自動対訳)— ON/OFF

グローバルPostToolUseフック(Edit|Write → translate-mode-hook)導入済み。
`.code-translate/live` フラグがあるプロジェクトでのみ発動し、編集のたび
「変更行の対訳をターン末尾に表示せよ」の指示が入る。
- 「翻訳モードON」→ `touch <対象>/.code-translate/live`
- 「翻訳モードOFF」→ そのファイルを削除
- 表示は変更行だけ・コードファイルのみ(日本語文書の編集には対訳不要)。

## 作業履歴の翻訳(後から振り返る)

「作業履歴を翻訳して」→ `git log`(必要なら `git show -p`)を読み、コミットごとに
時刻・書き手・何をしたか(業務語彙1〜2文)のタイムラインをウィジェット表示。
重大な修正は強調。特定コミットの深掘りは差分を対訳表示。範囲指定は日付で対応。

## 規律(必ず守る)

- 翻訳生成は必ず別プロセス(bin/code-translate)。実装ターン内で全体翻訳を作らない。
- ✗やコメントへの修正は、ユーザーの指示(「直して」)を受けてから行う。
- 判定条件(全まとまり✓・未読ゼロ・critical検出ゼロ・コミット済み)を依頼で緩めない。
- 「安全です」と言わない。未検証・不確実は隠さず表示する。
