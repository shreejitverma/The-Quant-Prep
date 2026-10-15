# Item-set specification (read fully before writing)

You are writing original CFA Level II item sets (vignette plus questions) for one learning module.
They must be indistinguishable in style and difficulty from the curriculum's own practice problems, or harder.

## Inputs

- The LM note: `17-CFA/CFA-L-2/<topic-slug>/<note-name>.md` (LOS map with IDs, formulas, item-set patterns, practice problems). Read it fully; the item sets must test its LOS and use its formulas.
- The module JSON for the curriculum's own practice problems (style reference only; do not copy): `build/cfa_l2/<topic-slug>/LM<nn>.json`.

## Output

Three or more files: `17-CFA/CFA-L-2/20-Item-Set-Bank/<topic-slug>/IS-<topic-slug>-LM<nn>-<k>.md` for k = 1, 2, 3 (more for FSA, Equity, Fixed Income, Ethics, Portfolio Management, Quant: write 4).

Frontmatter (exact keys):

```
---
type: cfa-itemset
topic: "<topic name>"
topic_code: "<code>"
topic_slug: "<topic-slug>"
lm: <n>
title: "<short vignette title>"
los: [los-<code>-<lm>-<a>, ...]
difficulty: <1-5>
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/<topic-slug-without-number-prefix-lowercase>]
---
```

Body:

```
# <Title>

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

<400 to 600 words. A named analyst or client, a realistic firm or portfolio, exhibits as markdown tables with the numbers needed and one or two decoy numbers, dated statements by two people where the exam style calls for "most likely correct". Written in exam register.>

## Questions

1. <stem> (LOS: los-<code>-<lm>-<x>)
   - A. ...
   - B. ...
   - C. ...
2. ...

(4 to 6 questions; at least half must require a calculation or a multi-step judgment; every question maps to one LOS in parentheses.)

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** <full computation or reasoning> A is wrong because <the specific error that produces A>. C is wrong because <...>.
> 2. ...

## Distractor design

<one line per question naming the error each wrong option encodes, so the candidate can audit their own mistake type: sign, period, before-tax vs after-tax, spot vs forward, IFRS vs US GAAP, wrong formula variant, misread exhibit.>
```

## Rules

- Every number in the answer key must be recomputed in Python before writing; show intermediate values to 4 decimals where relevant.
- Options must be numerically plausible and derived from specific errors; never a random spread.
- No two item sets for the same module may test the same LOS mix in the same way; vary the scenario (valuation vs reporting vs decision), the entity type, and which LOS carry the calculations.
- Difficulty 3 = curriculum level; 4 = harder; write at least one difficulty-4 set per module.
- No emojis, no em dash character, one sentence per line in prose, LaTeX for math.
- Do not modify any other file. When done run `python3 17-CFA/scripts/cfa_l2/verify_practice.py` from the repository root and report the lines that mention your module.
