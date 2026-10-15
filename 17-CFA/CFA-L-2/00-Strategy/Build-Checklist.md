---
type: cfa-build-checklist
tags: [cfa/l2, cfa/build]
created: 2026-08-26
updated: 2026-08-26
---
# CFA Level II Platform: Build Checklist

Source of truth for the build described in [[CFA-L2-Platform-Build-Prompt]].
Status values: todo, doing, done, blocked.

## Official exam facts (CFA Institute, fetched 2026-08-26)

| Topic | Code | Weight |
|---|---|---|
| Quantitative Methods | 01 | 5-10% |
| Economics | 02 | 5-10% |
| Financial Statement Analysis | 03 | 10-15% |
| Corporate Issuers | 04 | 5-10% |
| Equity Valuation | 05 | 10-15% |
| Fixed Income | 06 | 10-15% |
| Derivatives | 07 | 5-10% |
| Alternative Investments | 08 | 5-10% |
| Portfolio Management | 09 | 10-15% |
| Ethical and Professional Standards | 10 | 10-15% |

Structure: 22 item sets, 88 questions, 20 item sets scored and 2 trialed, two sessions of 2 hours 12 minutes.
The curriculum front matter does not print the weights; it points to the CFA Institute site, which is where the table above comes from.

## Step 1: Preflight

- [x] Read prompt, V1 front matter, fetch official weights
- [x] Quota check: Claude 7-day window at 12 percent on 2026-08-26, reset 2026-08-30

## Step 2: Hygiene and skeleton

- [x] Delete 52 iCloud ` 2.md` duplicates (35 byte-identical, 17 older importer-format copies)
- [x] Fix stale dataview path `05 Quant/...` in the old indexes
- [x] Install obsidian-spaced-repetition 1.15.4 and register it (untested until Obsidian is opened)
- [x] Folder skeleton
- [x] `CFA_L2_HUB.md` with Today block, heatmap, weight vs mastery, calibration, mock trend (dataviewjs untested until Obsidian opens)
- [x] Replace emoji indexes (`_Index_CFA-L-2.md`, Kaplan indexes)
- [x] Link hub from `Dashboard.md`
- [x] Templates: Attempt, Error, Teach-Back, Weekly-Review (Templater prompts untested headlessly)
- [x] QuickAdd choices written to plugin data.json (3 choices; verify they appear in QuickAdd settings, then bind hotkeys)
- [x] Bases: LM-Status, Item-Sets, Attempts, Errors (LOS-Mastery deferred: per-LOS rows need attempt data first)
- [x] Kanban study board (cards moved by mastery.py)
- [x] Daily note template hook

## Step 3: Extraction pipeline (`17-CFA/scripts/cfa_l2/`)

- [x] `extract.py`
- [x] `parse.py`
- [x] `verify_extraction.py` gate: 45 of 45 with LOS, examples, problems (extract.py found Ethics LM3, missed by the TOC scan)
- [x] `build_formula_sheet.py`
- [x] `build_canvases.py`
- [x] `mastery.py`
- [x] `verify_notes.py`
- [x] `verify_practice.py`

## Step 4: LM notes (11-section spec)

| Code | LM | Note | Verified |
|---|---|---|---|
| 01 | LM1 Basics of Multiple Regression | done | 2026-08-26 |
| 01 | LM2 Evaluating Regression Model Fit | done | 2026-08-26 |
| 01 | LM3 Model Misspecification | done | 2026-08-26 |
| 01 | LM4 Extensions of Multiple Regression | done | 2026-08-26 |
| 01 | LM5 Time-Series Analysis | done | 2026-08-26 |
| 01 | LM6 Machine Learning | done | 2026-08-26 |
| 01 | LM7 Big Data Projects | done | 2026-08-30 |
| 02 | LM1 Currency Exchange Rates | done | 2026-09-05 |
| 02 | LM2 Economic Growth | done | 2026-09-05 |
| 03 | LM1 Intercorporate Investments | done | 2026-08-30 |
| 03 | LM2 Employee Compensation | done | 2026-08-30 |
| 03 | LM3 Multinational Operations | done | 2026-08-30 |
| 03 | LM4 Analysis of Financial Institutions | done | 2026-08-30 |
| 03 | LM5 Evaluating Quality of Financial Reports | done | 2026-08-30 |
| 03 | LM6 Integration of FSA Techniques | done | 2026-08-30 |
| 04 | LM1 Dividends and Share Repurchases | done | 2026-09-05 |
| 04 | LM2 ESG Considerations | done | 2026-09-05 |
| 04 | LM3 Cost of Capital: Advanced Topics | done | 2026-09-05 |
| 04 | LM4 Corporate Restructuring | done | 2026-09-05 |
| 05 | LM1 Equity Valuation: Applications and Processes | done | 2026-08-30 |
| 05 | LM2 Discounted Dividend Valuation | done | 2026-09-05 |
| 05 | LM3 Free Cash Flow Valuation | done | 2026-09-05 |
| 05 | LM4 Market-Based Valuation | done | 2026-09-05 |
| 05 | LM5 Residual Income Valuation | done | 2026-09-05 |
| 05 | LM6 Private Company Valuation | done | 2026-09-05 |
| 06 | LM1 Term Structure and Interest Rate Dynamics | done | 2026-09-05 |
| 06 | LM2 Arbitrage-Free Valuation Framework | done | 2026-09-05 |
| 06 | LM3 Bonds with Embedded Options | done | 2026-09-05 |
| 06 | LM4 Credit Analysis Models | done | 2026-09-05 |
| 06 | LM5 Credit Default Swaps | done | 2026-09-05 |
| 07 | LM1 Forward Commitments | done | 2026-09-05 |
| 07 | LM2 Contingent Claims | done | 2026-09-05 |
| 08 | LM1 Commodities and Commodity Derivatives | done | 2026-09-05 |
| 08 | LM2 Types of Real Estate Investment | done | 2026-09-05 |
| 08 | LM3 Real Estate through Publicly Traded Securities | done | 2026-09-05 |
| 08 | LM4 Hedge Fund Strategies | done | 2026-09-05 |
| 09 | LM1 Economics and Investment Markets | done | 2026-09-05 |
| 09 | LM2 Analysis of Active Portfolio Management | done | 2026-09-05 |
| 09 | LM3 ETFs | done | 2026-09-05 |
| 09 | LM4 Using Multifactor Models | done | 2026-09-05 |
| 09 | LM5 Measuring and Managing Market Risk | done | 2026-09-05 |
| 09 | LM6 Backtesting and Simulation | done | 2026-09-05 |
| 10 | LM1 Code of Ethics and Standards | done | 2026-08-26 |
| 10 | LM2 Guidance for Standards I-VII | done | 2026-09-05 |
| 10 | LM3 Application of the Code and Standards: Level II | done | 2026-09-05 |

## Resume point (2026-08-26 session end)

All 45 LM notes complete and verified (2026-09-05). Next: practice layer (item sets, mocks) per Step 5.
To resume: `python3 17-CFA/scripts/cfa_l2/verify_notes.py` lists missing notes; spawn one agent per module with the NOTE_SPEC prompt pattern (see git history for the exact prompt shape), then run build_formula_sheet.py, build_canvases.py, build_slides.py, mastery.py, and commit.
After notes: item sets per ITEMSET_SPEC.md, then build_mocks.py for Mocks 1-2, fresh Mocks 3-6 per MOCK_SPEC.md, then verify_practice.py.

## Step 5: Practice

- [ ] Item-set bank, minimum 3 per LM
- [ ] Flashcards, 30-60 per LM
- [ ] Mocks 1-6
- [x] `verify_practice.py` gate

## Step 6: Strategy documents

- [x] Study-Plan.md (Tasks with due dates, regenerable via build_plan.py)
- [x] Distinction-Strategy.md
- [x] Calculator-Playbook.md
- [x] Exam-Day-Playbook.md
- [x] Prerequisite refreshers (3)
- [x] Excalidraw diagrams (8, generated by build_diagrams.py; open once in Excalidraw view to confirm rendering)
- [x] Slides decks (generated by build_slides.py from formula blocks; regenerate after each topic)

## Step 7: Ship

- [x] Commit at each gate, ship via no-mistakes
- [ ] Final report
