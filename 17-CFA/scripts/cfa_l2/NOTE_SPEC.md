# LM note specification (read fully before writing a note)

You are writing one learning-module note for a CFA Level II candidate whose goal is a top-band score.
Write as a tutor who wants the candidate to derive every formula under pressure, not as a summarizer.
The note is the single study source for this module; the candidate will not open the PDF.

## Inputs

- Extracted module JSON: `build/cfa_l2/<topic-slug>/LM<nn>.json` (LOS list, examples and knowledge checks with text, practice problems and solutions, equation candidates with printed pages).
- Raw module text with page breaks: `build/cfa_l2/<topic-slug>/LM<nn>.txt` (form feed separates pages; printed page = pdf page - page_offset from the manifest).
- LOS IDs: `build/cfa_l2/los_index.json` (use exactly these IDs).
- If something in the JSON is unclear, read the raw text for that page range. Never invent a formula, a number, or an answer.

## Output

Path: `17-CFA/CFA-L-2/<topic-slug>/<note-name>.md` where note-name is given to you.

Frontmatter (exact keys):

```
---
type: cfa-lm
topic: "<topic name>"
topic_code: "<code>"
topic_slug: "<topic-slug>"
volume: <n>
lm: <n>
title: "<title>"
pages: "<printed start>-<printed end>"
weight_band: "<band>"
difficulty: <1-5>
los_count: <n>
status: not-started
mastery: 0
next_review: ""
last_reviewed: ""
tags: [cfa/l2, cfa/<topic-slug-without-number-prefix-lowercase>]
---
```

Then `# LM<n>: <title>` and a one-line difficulty rationale, then exactly these 11 `##` sections in this order.

1. `## LOS map`: one line per LOS, verbatim text, ending with the block ID on the same line: `- **calculate** and interpret ... (V6 p.121) ^los-06-03-f`. Bold the command verb. After each LOS line add an indented sub-bullet "Examiner asks: ..." with the one concrete way it is tested. Block IDs must be the last thing on the line with a space before the caret.
2. `## Core intuition`: at least 1,500 characters and typically 4,000 to 9,000. First principles, in your own words, the economic reason behind each mechanism, before any formula. Use `> [!abstract]` callouts for the two or three ideas everything hangs on. Cite pages inline as `(V6 p.143)`.
3. `## Formulas and derivations`: every formula the module uses. Each formula is a display block:
   ```
   **Name** (V6 p.130)
   $$ ... $$
   ^f-06-03-1
   ```
   The `^f-` line must directly follow the closing `$$` line with no blank line between (so the block ID attaches to the math block). Below it: variables with units and sign conventions, then a 2 to 4 line derivation or the reason it holds. Where the exam expects a calculator, add `> [!tip] Calculator` with BA II Plus keystrokes. Number formulas sequentially from 1 within the module.
4. `## Worked examples`: every curriculum example and knowledge check, in order, reworked step by step with arithmetic shown, each ending with a block ID `^ex-<code>-<lm>-<n>`. Recompute every number in Python before writing it (python3 is available); if your result differs from the curriculum solution, say so and explain which is right.
5. `## Item-set patterns`: 5 to 10 patterns. Each is a `> [!warning] Trap` callout: how the vignette presents it, what the correct approach is, what the distractors are and why each is tempting.
6. `## Practice problems`: every end-of-module problem. Format: `> [!question] Q<n>` with the question (vignette context summarized once per vignette group), then `> [!success]- Solution` (foldable) with the full reasoning for the correct option and why each rejected option is wrong.
   The restated problems are CFA Institute copyright, so they go in the private companion note `17-CFA/Private/CFA-L-2/Practice-Problems/<note-name>-Practice-Problems.md` (frontmatter `type: cfa-practice-private`, then the section body); the public section holds only the "Kept private" callout and the embed `![[<note-name>-Practice-Problems]]` on its own line. `verify_notes.py` follows the embed.
7. `## Cross-links`: bullets `- [[<note-name>]]: <what flows and why>` for every module this one depends on or feeds. Use the note names from the manifest (format `LM<nn>-<Slugified-Title>`). Only link real modules.
8. `## Self-test`: 10 original item-set style questions of exam difficulty or harder, with a short vignette, then a foldable `> [!success]- Answer key` with reasoning for every option.
9. `## Flashcards`: start the section with the tag line `#flashcards/cfa-l2/<topic-slug>/lm<nn>` on its own line, then 30 to 60 cards. Single-line cards use `Question::Answer`. Multi-line cards use the question, a line with `?`, the answer, and a blank line. Cloze cards use `{{text}}`. Mix: formula recall, definitions, "which standard or rule applies", "which answer is the trap and why", 30-second numeric micro-problems with the keystrokes. Do not use `::` inside answers.
10. `## Common mistakes`: numbered list of 8 or more, seeded from the traps and from the curriculum's own warnings, then this exact dataview block:
    ````
    ```dataview
    LIST rule
    FROM "17-CFA/CFA-L-2/23-Error-Log"
    WHERE type = "cfa-error" AND lm = "<code>-<lm>" AND resolved != true
    ```
    ````
11. `## Teach-back`: exactly this and nothing else:
    ```
    > [!note] Teach-back
    > Write the module in your own words after Pass 1. Empty caps mastery at 60.
    >
    ```

## Rules

- No emojis anywhere. No em dash character; use a plain dash. One sentence per line in prose. LaTeX for all math. Tables for comparisons.
- Every formula, number and standard cites a printed page as `(V<vol> p.<n>)`.
- Do not thin out later sections to finish; every section must meet its minimum.
- Do not write anything outside the note file (no scratch files in the repository; use the scratchpad if needed).
- After writing, run `python3 17-CFA/scripts/cfa_l2/verify_notes.py <code>` from the repository root and fix every failure that concerns your note, then run it again. Return the final verify line and the counts: LOS, formulas, examples, problems, self-test, flashcards.
