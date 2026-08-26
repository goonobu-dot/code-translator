# X投稿(アップデート告知・2026-08-26)

添付画像(推奨順): `docs/images/12-split-screen.png`(使い方の全体像・1枚目)、
`docs/images/09-risk-colors.png`(危険度の色分け・2枚目)、`docs/images/10-risk-only.png`(危ない所だけ・3枚目)

※ 画像はすべてリポジトリ同梱のデモ用アプリ。実案件のコードや未公開プロダクト名は写っていない。

---

## 本文(日本語)

【アップデート】非エンジニア向けコード翻訳ツール「コード通訳」に、**危険度の色分け**を入れました。

まず1枚目の画像が、僕の実際の使い方です。**Claude Codeの画面を半分に割って、左をチャット、右を翻訳画面**にしています。

左で「コードを翻訳して」と頼む → 右に日本語の対訳が出る → 気になった所をその場で「✗おかしい」と答える → 左のチャットでAIが直す。**画面を行き来しないで、読むと直すが1つの窓で完結します。**

2枚目・3枚目を見てください。左が日本語の説明、右が実際のコード。そして今回、**赤・橙・青の色**が付きました。

バイブコーディングで作ったアプリのコードって、全部が同じ重さに見えるんですよね。でも実際は違う。**お金を動かす場所、データを消す場所、外部に情報を送る場所**——ここだけは、作った本人が意味を分かっていないとまずい。

そこで4段階に分けました。

🔴 重大 — 外部への送信・課金・削除・個人情報
🟠 要確認 — 異常時の動作、外部の部品
🔵 知っておく — 軽微な注意点
無色 — ふつうの処理

判定はAIが6分類×重大度で自動算出。ただし**外部送信・課金削除・個人情報の3つは「中程度」でも赤に格上げ**しています。非エンジニアが一番知りたいのがそこだから。

「🔴 危ない所だけ」ボタンを押すと、そこだけに絞られます。実測で374か所→45か所。1/8の分量で急所を確認できる。

気になった箇所には ✓問題ない / ✗おかしい / ?わからない で答えられて、**「📮 指摘をAIへ送る」を押せばAIがそのまま直しにいきます。**

---

**ここからが正直な話で、まだ解けていない課題があります。**

翻訳はできる。色も付けられる。でも——

「プレイヤーIDと住所と名前をサーバーに送信します」

これを読んだ非エンジニアは、**それが良いことなのか悪いことなのかを判断できない**んです。事実は分かった。でも「で、どうすればいいの?」が残る。

AIに「安全です/危険です」と判定させるのは簡単ですが、それは違うと思っています。外れたときに信頼が全部飛ぶし、何より**判断の枠組み自体が人の決定を誘導してしまう**。作り手が「これが最良の見せ方だ」と決め打ちした時点で、結論も半分決まってしまう。

だから今は、あえて実装していません。使う人が実際にどこで迷い、何を材料に決めるのかが見えるまで待つつもりです。

**もし「こう見せてくれたら判断できる」というアイディアがあれば、ぜひ教えてください。** ここが解けたら、このツールは本当に意味のあるものになると思っています。

MIT ライセンスで公開中です。

GitHub: https://github.com/goonobu-dot/code-translator
使い方(5分・画像つき): https://github.com/goonobu-dot/code-translator/blob/main/docs/manual.md

#バイブコーディング #ClaudeCode #個人開発

---

## 本文(English)

**Update:** Code Interpreter — the tool that translates code into plain language for non-engineers — now has **risk-based color coding**.

The first image is how I actually use it: **Claude Code split in half — chat on the left, the translated code on the right.**

Ask "translate the code" on the left → the plain-language pairing appears on the right → mark anything that bothers you with ✗ → the AI fixes it back in the chat. **Reading and fixing happen in one window.**

Images 2 and 3: plain-language explanation on the left, real code on the right. New in this update: red, orange and blue markers.

When you vibe-code an app, every line looks equally important. It isn't. **The places that move money, delete data, or send information outside** — those are the ones you need to actually understand.

So there are now four levels:

🔴 Serious — sends data out, charges, deletes, personal data
🟠 Check this — failure handling, outside components
🔵 Good to know — minor notes
none — ordinary code

The AI classifies by category × severity, but **sending data out, charging/deleting, and personal data get promoted to red even at medium severity** — that's what non-engineers most need to see.

Press "🔴 Risky parts only" and the page narrows to just those: 374 units → 45 in a real project. One eighth of the reading, all of the risk.

You answer each unit with ✓ fine / ✗ wrong / ? unsure, and **"📮 Send flags to the AI" hands them straight back to the AI to fix.**

---

**Now the honest part — the problem I have not solved.**

The translation works. The colors work. But then you read:

"Sends the player ID, address and partner name to a server."

And if you are not an engineer, **you still cannot tell whether that is fine or not.** You know the fact. You don't know the decision.

Making the AI declare "this is safe / this is dangerous" would be easy, and I think it would be wrong. One bad call destroys the trust — and more importantly, **the framing itself steers the human's decision.** The moment the builder decides "this is the best way to present it", half the conclusion is already made.

So I deliberately left it unbuilt, until I can actually observe where real users hesitate and what they decide on.

**If you have an idea for how to present this so a non-engineer can genuinely decide, I would love to hear it.** Solve that, and this tool becomes something that really matters.

MIT licensed.

GitHub: https://github.com/goonobu-dot/code-translator
Manual (5 min, with screenshots): https://github.com/goonobu-dot/code-translator/blob/main/docs/manual.en.md

#vibecoding #ClaudeCode #buildinpublic
