# X投稿(アップデート告知・2026-08-26)

添付画像(推奨順):
1. `docs/images/16-whats-new.png` — 更新内容の要約(1枚で全体が分かる)
2. `docs/images/09-risk-colors.png` — 危険度の色分け(赤・橙・青)
3. `docs/images/13-progress-map.png` — 進み具合の色分け(どこまで見たか)
4. `docs/images/12-split-screen.png` — 使い方の全体像(左=チャット / 右=翻訳)
5. `docs/images/15-home.png` — ホーム画面(一覧)

※ 画像はすべてリポジトリ同梱のデモ用アプリ。実案件のコードや未公開プロダクト名は写っていない。

---

## 本文(日本語)

【アップデート】非エンジニア向けコード翻訳ツール「コード通訳」を大きく更新しました。

バイブコーディングで作ったアプリのコードって、全部が同じ重さに見えるんですよね。でも実際は違う。**お金を動かす場所、データを消す場所、外部に情報を送る場所**——ここだけは、作った本人が意味を分かっていないとまずい。

そこで今回、**危険度で色分け**しました(画像2枚目)。

🔴 重大 — 外部への送信・課金・削除・個人情報
🟠 要確認 — 異常時の動作、外部の部品
🔵 知っておく — 軽微な注意点
無色 — ふつうの処理

判定はAIが6分類×重大度で自動算出。ただし**外部送信・課金削除・個人情報の3つは「中程度」でも赤に格上げ**しています。非エンジニアが一番知りたいのがそこだから。

「🔴 危ない所だけ」を押すと、そこだけに絞られます。実測で374か所→45か所。**1/8の分量で急所を確認できる。**

---

**もう一つの大きな変更が「読んだ記録が積み上がる」ようになったこと**(画像3枚目)。

以前は1文字コードを直すと、それまで付けた「✓確認済み」が全部消えていました。これだとレビューが永遠に終わらない。

今は:
・触っていない所の ✓ は**そのまま残る**
・変わった所だけ「🔄 再確認」に戻る
・「▶ 続きから」で、答えていない所だけを表示

さらに画面上部に**四角が並んだ帯**を置きました。四角1つがファイル1つで、緑=確認済み / 黄=途中 / 灰=未着手 / 赤枠=重大あり。**選ぶ前に「どこまで見たか」が一目で分かります。**

翻訳も速くなりました。変更のあったファイルだけ訳し直すので、実測で**2,800行のプロジェクトが9分→1ファイル分(数十秒)**に。

---

使い方は、画像4枚目のとおりです。**Claude Codeの画面を半分に割って、左をチャット、右を翻訳画面**にしています。左で「◯◯のコードを見せて」と頼む → 右に日本語の対訳が出る → 気になった所を「✗おかしい」と答える → 「📮 指摘をAIへ送る」→ 左のチャットでAIが直す。

**覚えるのは「◯◯のコードを見せて」の一言だけです。**

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
使い方(5分・画像つき手順書): https://github.com/goonobu-dot/code-translator/blob/main/docs/manual.md

#バイブコーディング #ClaudeCode #個人開発

---

## 本文(English)

**Update:** Code Interpreter — the tool that translates code into plain language for non-engineers — got a major update.

When you vibe-code an app, every line looks equally important. It isn't. **The places that move money, delete data, or send information outside** — those are the ones you need to actually understand.

So now there is **risk-based color coding** (image 2):

🔴 Serious — sends data out, charges, deletes, personal data
🟠 Check this — failure handling, outside components
🔵 Good to know — minor notes
none — ordinary code

The AI classifies by category × severity, but **sending data out, charging/deleting, and personal data get promoted to red even at medium severity** — that's what non-engineers most need to see.

Press "🔴 Risky parts only" and a real project narrows from 374 units to 45. **One eighth of the reading, all of the risk.**

---

**The second big change: your review now accumulates** (image 3).

Before, changing a single character wiped every "✓ reviewed" mark you had made. That made review impossible to ever finish.

Now:
・untouched units **keep their ✓**
・only changed units return to "🔄 Re-check"
・"▶ Continue" shows only what you haven't answered

And a strip of small squares sits at the top — one square per file: green = reviewed, amber = partial, grey = untouched, red outline = contains something serious. **You can see how far you got before you even pick a file.**

Translation got faster too: only changed files are re-translated. A 2,800-line project went from ~9 minutes to a few dozen seconds.

---

How I actually use it (image 4): **Claude Code split in half — chat on the left, the translated code on the right.** Ask on the left, read on the right, mark anything odd with ✗, press "📮 Send flags to the AI", and the AI fixes it back in the chat.

**One phrase to remember: "show me the code for X".**

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
