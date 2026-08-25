# Code Interpreter (コード通訳) — User Manual

**Read and review AI-generated code in plain language, even if you can't read code.**
This manual takes 5 minutes. No jargon.

> Note: The tool's UI text is currently Japanese (v1). An English UI is on the roadmap.
> This manual explains every element so non-Japanese readers can follow along.

---

## What you get

![Overview](images/01-overview.png)

Your code is displayed in "units of meaning" (a few lines each): **plain-language explanation on the left, the actual code on the right**.
All you do is read the explanation and **press one of three buttons**.

On narrow screens (a side panel next to Claude Code, or a phone) the layout automatically
stacks vertically — explanation above, code below. Same features either way.

<img src="images/portrait/01-overview.png" alt="Narrow layout" width="360">

---

## 0. Open it (first time only)

Three ways, same screen:

| How | Steps |
|---|---|
| **A. Ask in chat** (Claude Code users) | Type "コードを翻訳して" (translate the code) |
| **B. Double-click** | Double-click "コード通訳を開く.command" in your project folder (created automatically on first run) |
| **C. Command line** | `code-translate <your-project> --open` |

The first run generates the translation with AI (~2 minutes and ~$0.1–0.3 for a small app).
**From the second time on, it opens instantly** — the translation is already there.

---

## 1. Press the file you want to see

![File buttons](images/02-filebar.png)

File-name buttons sit at the top. Press one and that file appears, already translated.
"残り◯" (= "N left") shows how many units you haven't reviewed; it turns "✓" when done.
"すべて" (= "All") shows every file in order.

![File selected](images/08-file-selected.png)

---

## 2. Read

![A unit of meaning](images/03-section.png)

Each card is a **few-line unit of meaning**:

- **Bold heading (left)** — what these lines do, in one phrase
- **Left paragraph** — the detailed plain-language explanation
- **Dark area (right)** — the actual code; **hover a line to see its line-by-line translation**

Cards marked **⚠ (注意 = caution)** touch money, personal data, or deletion — the places where accidents happen.
The amber box explains what to watch for. The floating "⚠ 次の注意箇所へ" button (= "next caution spot") tours only the ⚠ cards.

---

## 3. Answer

This is **not a quiz**. You are only answering: "is this what I asked for?"

| Button | Press when | Then |
|---|---|---|
| **✓ 問題ない** (looks right) | The behavior matches your intent | Recorded; move on |
| **✗ おかしい** (wrong) | You never asked for this / it looks wrong | Say "たまった指摘を直して" (fix the flagged items) in chat and the AI fixes them |
| **? わからない** (not sure) | You can't judge | Ask in chat and the AI explains further |

![After answering](images/04-answered.png)

"取り消す" (undo) reverts a mis-press. **Pressing a button never changes the code** — it only records your judgment. Fixes happen only when you ask for them in chat.

---

## 4. Write comments

![Comment](images/05-comment.png)

Open "コメントを書く" (write a comment) and type in ordinary language,
e.g. "add a confirmation screen before sending". Like ✗ answers, comments are picked up
by the AI when you say "たまった指摘を直して" in chat.

---

## 5. Check the verdict at the bottom

![Verdict](images/07-verdict.png)

When every unit is answered "✓", no file is unread, nothing critical was detected, and the code
is committed, the bottom turns green: "✅ 全部確認できました" (all reviewed).
While red, the reasons are listed. **This tool never says "it's safe."**
It only shows, honestly, what you reviewed and what remains unverified.

---

## Bonus: Learning mode

![Learning mode](images/06-learning.png)

Press "学習モード" (learning mode) in the header: explanations are hidden and replaced by
"❓ what do these lines do?" — **read the code, make a guess, click to check the answer**.
The same active-recall loop as language flashcards. (⚠ cards stay visible for safety.)

---

## FAQ

**Q. What happens to my answers when the code changes?**
They are invalidated automatically and every card resets — approvals of old code are never carried over to new code. The screen switches to the new translation on its own.

**Q. What does it cost?**
Only translation generation costs money (~$0.1–0.3 per run for a small app, via Claude CLI). Unchanged code is never re-translated.

**Q. Can the translation be wrong?**
Yes — it is AI-generated. That's why the real code always sits next to the explanation, and unread files are shown in red. Use the ⚠ marks and the verdict, not the translation alone.

**Q. Where are my answers and comments stored?**
In `.code-translate/view/review.json` inside your project. The AI reads this file to apply fixes. Nothing is sent anywhere else.
