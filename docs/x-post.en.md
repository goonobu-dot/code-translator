# X post draft (English, long-form)

---

[Open Source] I built a tool that lets you READ and REVIEW AI-generated code — even if you can't read code.

Vibe coding is everywhere now. Non-engineers (me included) are shipping real apps with AI. But there's a problem nobody solved:

"The AI wrote my entire app. I can't read a single line of it. Should I really ship this?"

That fear is justified. Independent testing found that roughly 45% of AI-generated code contains known security flaws (Veracode). We've all seen the incidents — production databases deleted, apps shipped with their user data wide open. The AI can build it. But there was no way for the person who asked for it to check it.

So I built one. It's called Code Interpreter (コード通訳), and it's open source as of today.

▼ What it does

It splits your code into small "units of meaning" (a few lines each) and shows a plain-English explanation next to the actual code — like a bilingual book. Then you review each unit with three buttons:

✓ Looks right (this is what I asked for)
✗ Wrong (I never asked for this)
? Not sure

It's not a quiz. You're just answering: "is this what I wanted?"

▼ Every feature

- Press a file name → that file appears, already translated (translation is pre-generated, so it's instant)
- Risky spots — money, personal data, deletion — get a ⚠ Caution mark with an amber explanation of what could go wrong. A floating button tours only the ⚠ spots
- Hover any line of code for its one-line translation; hover keywords like `if` and `const` for hints
- Write free comments in ordinary language ("add a confirmation screen before sending")
- Your ✗ answers and comments are saved to a file. Tell the AI "fix the flagged items" in chat and it fixes them in bulk
- A verdict at the bottom: it turns green ONLY when every unit is marked ✓, every file was read, and nothing critical was detected
- When the code changes, all answers auto-expire — approvals of old code are never recycled for new code
- Learning mode: explanations are hidden, you guess what the code does, then click to check. Flashcard-style active recall — you actually learn to read code by reviewing your own app
- Works in English (--lang en) and Japanese

▼ The design principle I care about most

This tool never says "your code is safe."

Unread files are shown in red. AI explanations can be wrong, so the real code always sits right next to them. The verdict won't turn green while anything is unanswered or unverified. What it gives you is not reassurance — it's an honest record of what YOU reviewed and what remains unchecked.

Polished reports make people careless. So I built the opposite.

▼ Getting started (3 steps)

1. git clone (see README)
2. code-translate your-app --open --lang en
3. Your browser opens. From then on, just double-click the launcher file it drops in your folder

Works standalone or with Claude Code (~$0.1–0.3 per translation for a small app; unchanged code is never re-translated).

If you're vibe coding anything real — or reviewing what an AI or contractor shipped you — I'd love your feedback. Stars appreciated more than you know.

GitHub: https://github.com/goonobu-dot/code-translator
English manual (with screenshots): https://github.com/goonobu-dot/code-translator/blob/main/docs/manual.en.md
日本語マニュアル: https://github.com/goonobu-dot/code-translator/blob/main/docs/manual.md

#OpenSource #VibeCoding #AIcoding #BuildInPublic #ClaudeCode
