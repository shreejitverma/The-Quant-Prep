# Fresh mock specification (Mocks 3 to 6)

A fresh mock is 22 original item sets written to ITEMSET_SPEC.md standards, assembled into one note.
Mocks 1 and 2 are built from the bank by build_mocks.py; do not reuse bank item sets in fresh mocks.

## Composition (22 sets, inside the official bands)

| Topic | Code | Sets | Band |
|---|---|---|---|
| Quantitative Methods | 01 | 2 | 5-10% |
| Economics | 02 | 1 | 5-10% |
| Financial Statement Analysis | 03 | 3 | 10-15% |
| Corporate Issuers | 04 | 2 | 5-10% |
| Equity Valuation | 05 | 3 | 10-15% |
| Fixed Income | 06 | 3 | 10-15% |
| Derivatives | 07 | 2 | 5-10% |
| Alternative Investments | 08 | 1 | 5-10% |
| Portfolio Management | 09 | 3 | 10-15% |
| Ethics | 10 | 2 | 10-15% |

Each set has exactly 4 questions (88 total), mixed order across topics, 11 sets per session.
Difficulty: at least 6 sets at difficulty 4; the rest at 3.
Every module in a topic should appear across Mocks 3 to 6; do not test the same LM twice in one mock.

## File

`17-CFA/CFA-L-2/21-Mocks/Mock-0<n>.md`, frontmatter `type: cfa-mock`, `mock: <n>`, `sessions: 2`, `minutes_per_session: 132`, `tags: [cfa/l2, cfa/mock]`.
Sections: `## Session 1`, then `## Item set <i> (<code>-<lm>)` blocks each containing `### Vignette`, `### Questions`; `## Session 2` likewise; then `## Answer keys` with one foldable `> [!success]- Item set <i>` per set holding answers, reasoning, and the distractor design line.
Store each set's item-set body also as its own bank note with `source: mock-0<n>` so it can be reused in Pass 3 repair days.

## Rules

Same as ITEMSET_SPEC.md: recompute every number in Python, plausible distractors from named errors, no emojis, no em dashes, one sentence per line.
After writing, run `python3 17-CFA/scripts/cfa_l2/verify_practice.py` and report the lines mentioning the mock.
