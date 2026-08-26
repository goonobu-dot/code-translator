# X投稿(アップデート告知・2026-08-26)

添付画像(この順番で):
1. `docs/images/16-whats-new.png` — 更新内容の要約(1枚で全体が分かる)
2. `docs/images/09-risk-colors.png` — 危険度の色分け(赤・橙・青)
3. `docs/images/13-progress-map.png` — 進み具合の色分け(どこまで見たか)
4. `docs/images/12-split-screen.png` — 使い方の全体像(左=チャット / 右=翻訳)

※ 画像はすべてリポジトリ同梱のデモ用アプリ。実案件のコードや未公開プロダクト名は写っていない。

---

## 本文(日本語)

【大型アップデート】非エンジニア向けコード翻訳ツール「**コード通訳**」を更新しました。

AIが書いたコードを**日本語で読んで、「✓問題ない / ✗おかしい」で答えるだけ**のツールです。コードが読めなくても使えます。

今回の更新点を全部説明します。

---

**① 危険度で色分けしました**(画像2枚目)

バイブコーディングで作ったコードって、全部が同じ重さに見えるんですよね。でも実際は違う。**お金を動かす場所、データを消す場所、外部に情報を送る場所**——ここだけは、作った本人が意味を分かっていないとまずい。

そこで4段階に分けました。

🔴 重大 — 外部への送信・課金・削除・個人情報
🟠 要確認 — 異常時の動作、外部の部品
🔵 知っておく — 軽微な注意点
無色 — ふつうの処理

判定はAIが6分類×重大度で自動算出。ただし**外部送信・課金削除・個人情報の3つは「中程度」でも赤に格上げ**しています。非エンジニアが一番知りたいのがそこだから。

「🔴 危ない所だけ」を押すと、そこだけに絞られます。実測で**374か所→45か所**。1/8の分量で急所を確認できます。

実際にAIはこういう指摘を出します(デモアプリより):

・「カードから先にお金を引き落とし、その後で記録を保存します。**もし記録の保存に失敗すると、お金だけ引かれて記録が残らない事態が起こり得ます**」
・「削除可否の確認やバックアップが見当たりません。**削除ではなく『取り消し済み』フラグを立てる設計が一般的です**」

翻訳だけでなく、**危険と代案**まで出してくれます。

---

**② 読んだ記録が積み上がるようになりました**(画像3枚目)

以前は1文字コードを直すと、それまで付けた「✓確認済み」が**全部消えていました**。これだとレビューが永遠に終わらない。致命的な設計ミスでした。

今は:
・触っていない所の ✓ は**そのまま残る**
・変わった所だけ「🔄 再確認」に戻る
・**「▶ 続きから」**を押すと、答えていない所だけが並ぶ

さらに画面の上に**四角が並んだ帯**を置きました。四角1つがファイル1つで、**緑=確認済み / 黄=途中 / 灰=未着手 / 赤枠=重大あり**。押せばそのファイルが開きます。**選ぶ前に「どこまで見たか」が一目で分かります。**

「10か所読んでやめる」が普通にできるようになりました。

---

**③ 翻訳が速くなりました**

変更のあったファイルだけ訳し直す方式に変えました。

・2,800行のプロジェクト: **約9分 → 数十秒**(変更1ファイルの場合)
・AI呼び出し回数: **35回 → 1回**

処理量を増やしたのではなく、**今まで無駄に全部訳し直していたのをやめた**だけです。これで「こまめに読む」が現実的になりました。

---

**④ 入口を1つにしました**(ホーム画面)

`ctrl` + `]` を押すと、翻訳したプロジェクトの一覧が出ます。各項目に「🔴 重大◯件」「◯ファイル / ◯か所」が表示されるので、どれを見るべきか選べます。

**覚えるのは「◯◯のコードを見せて」の一言だけ**にしました。モードもフラグもコマンドも覚えなくていい。

---

**⑤ 読みやすさを徹底的に直しました**

・**1行も飛ばさず全部訳す**——以前は説明の切れ目に挟まれた行(閉じ括弧など)が画面から消えていました。71行の欠落を発見して修正
・**説明がコードに寄り添って留まる**——長いコードでも、日本語の説明が上に流れて消えません
・**長い行も折り返して全文表示**——横スクロールしないと読めない状態を無くしました
・**読んでいる最中に画面が入れ替わらない**——新しい翻訳ができても知らせるだけ。押したときに切り替わります

---

**その他の機能**

・**📮 指摘をAIへ送る** — ✗やコメントを付けると左下にボタンが出る。押してチャットで「指摘を直して」と言えばAIが直します
・**▶ 順番に読む** — 「アプリが立ち上がる → 相棒を作る → 庭で暮らしが始まる」のように、**紙芝居形式でコードを巡れます**。初めて見るシステムの入口として最適
・**学習モード** — 説明を隠して、先に自分でコードを読んで答え合わせ。読む力を付けたい人向け
・**日本語・英語の両対応** — `--lang en` で英語の解説になります
・**リンクで特定の箇所へ直接ジャンプ** — チャットに貼ったリンクから、翻訳画面のその行へ飛んで光ります

---

**使い方**(画像4枚目)

**Claude Codeの画面を半分に割って、左をチャット、右を翻訳画面**にしています。

左で「◯◯のコードを見せて」と頼む → 右に日本語の対訳が出る → 気になった所を「✗おかしい」と答える → 「📮 指摘をAIへ送る」→ 左のチャットでAIが直す。

**画面を行き来せず、1つの窓で完結します。**

---

**ここからが正直な話で、まだ解けていない課題があります。**

翻訳はできる。色も付けられる。でも——

「プレイヤーIDと住所と名前をサーバーに送信します」

これを読んだ非エンジニアは、**それが良いことなのか悪いことなのかを判断できない**んです。事実は分かった。でも「で、どうすればいいの?」が残る。

AIに「安全です/危険です」と判定させるのは簡単ですが、それは違うと思っています。外れたときに信頼が全部飛ぶし、何より**判断の枠組み自体が人の決定を誘導してしまう**。作り手が「これが最良の見せ方だ」と決め打ちした時点で、結論も半分決まってしまう。

だから今は、あえて実装していません。使う人が実際にどこで迷い、何を材料に決めるのかが見えるまで待つつもりです。

**もし「こう見せてくれたら判断できる」というアイディアがあれば、ぜひ教えてください。** ここが解けたら、このツールは本当に意味のあるものになると思っています。

MIT ライセンスで公開中です。翻訳はClaude Codeの利用枠内で動くので追加請求もありません。

GitHub: https://github.com/goonobu-dot/code-translator
使い方(5分・画像つき手順書): https://github.com/goonobu-dot/code-translator/blob/main/docs/manual.md

#バイブコーディング #ClaudeCode #個人開発

---

## 本文(English)

**Major update** to **Code Interpreter** — the tool that lets non-engineers read AI-written code in plain language.

You read a plain-English explanation next to the real code, and answer **"✓ looks right / ✗ wrong"**. That's the whole interaction. You never have to read code yourself.

Here is everything that changed.

---

**1. Risk-based color coding** (image 2)

When you vibe-code an app, every line looks equally important. It isn't. **The places that move money, delete data, or send information outside** — those are the ones you need to actually understand.

So there are now four levels:

🔴 Serious — sends data out, charges, deletes, personal data
🟠 Check this — failure handling, outside components
🔵 Good to know — minor notes
none — ordinary code

The AI classifies by category × severity, but **sending data out, charging/deleting, and personal data get promoted to red even at medium severity** — that's what non-engineers most need to see.

Press "🔴 Risky parts only" and a real project narrows from **374 units to 45**. One eighth of the reading, all of the risk.

Real examples the AI produced on a demo app:

・"It charges the card first, then saves the record. **If saving fails, the customer is charged with no record of it.**"
・"No confirmation or backup before deletion. **A 'cancelled' flag is the usual design instead of deleting.**"

It doesn't just translate — it names the risk and suggests the fix.

---

**2. Your review now accumulates** (image 3)

Before, changing a single character wiped every "✓ reviewed" mark. Review could never finish. That was a real design flaw.

Now:
・untouched units **keep their ✓**
・only changed units return to "🔄 Re-check"
・**"▶ Continue"** shows only what you haven't answered yet

And a strip of small squares sits at the top — one square per file: **green = reviewed, amber = partial, grey = untouched, red outline = contains something serious**. Click one to open that file. **You see how far you got before you even pick a file.**

Reading ten units and stopping is now a perfectly normal thing to do.

---

**3. Translation got much faster**

Only changed files are re-translated.

・A 2,800-line project: **~9 minutes → a few dozen seconds** (one changed file)
・AI calls: **35 → 1**

This isn't more processing — it's the removal of waste that was there all along. "Read it often" finally became practical.

---

**4. One way in** (home screen)

Press `ctrl` + `]` and you get a list of every translated project, each showing "🔴 N serious" and its size, so you can choose what deserves attention.

**One phrase to remember: "show me the code for X."** No modes, no flags, no commands.

---

**5. Readability fixes, thoroughly**

・**Not a single line is skipped** — lines caught between explanation boundaries (closing braces and such) used to vanish from the page. I found 71 missing lines and fixed it
・**The explanation stays beside the code** — in long units, the plain-language text no longer scrolls away
・**Long lines wrap** — nothing is hidden behind horizontal scroll any more
・**The page never swaps under you while reading** — a new translation only announces itself; you switch when you're ready

---

**Also in this release**

・**📮 Send flags to the AI** — mark ✗ or write a comment, press one button, then say "fix the flagged items" in chat
・**▶ Read in order** — walks you through the code as a story ("the app starts → you build your companion → life in the garden begins"). The best entry point for a codebase you've never seen
・**Learning mode** — hides the explanation so you can guess first, then reveal
・**Japanese and English** — `--lang en` produces English explanations and an English UI
・**Deep links** — a link in chat jumps straight to that spot in the translated view and highlights it

---

**How I actually use it** (image 4)

**Claude Code split in half — chat on the left, the translated code on the right.**

Ask on the left → read the pairing on the right → mark anything odd with ✗ → press "📮 Send flags to the AI" → the AI fixes it back in the chat. **One window, no switching.**

---

**Now the honest part — the problem I have not solved.**

The translation works. The colors work. But then you read:

"Sends the player ID, address and partner name to a server."

And if you are not an engineer, **you still cannot tell whether that is fine or not.** You know the fact. You don't know the decision.

Making the AI declare "this is safe / this is dangerous" would be easy, and I think it would be wrong. One bad call destroys the trust — and more importantly, **the framing itself steers the human's decision.** The moment the builder decides "this is the best way to present it", half the conclusion is already made.

So I deliberately left it unbuilt, until I can observe where real users hesitate and what they actually decide on.

**If you have an idea for how to present this so a non-engineer can genuinely decide, I would love to hear it.** Solve that, and this tool becomes something that really matters.

MIT licensed. Translation runs inside your existing Claude Code plan — no extra charge.

GitHub: https://github.com/goonobu-dot/code-translator
Manual (5 min, with screenshots): https://github.com/goonobu-dot/code-translator/blob/main/docs/manual.en.md

#vibecoding #ClaudeCode #buildinpublic
