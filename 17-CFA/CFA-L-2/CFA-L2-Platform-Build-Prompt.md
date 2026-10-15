---
type: prompt
tags: [cfa-l-2, prompt, study-platform]
created: 2026-08-26
updated: 2026-08-26
---
# CFA Level II Study Platform: Build Prompt (Obsidian-native)

> [!note] Provenance
> Written on 2026-08-26 for the author's private Obsidian vault, where the platform lived under `Quant/CFA/CFA-L-2/` with the pipeline in `.scripts/cfa_l2/`.
> It moved to this repository on 2026-10-15; paths below were rewritten to `17-CFA/CFA-L-2/` and `17-CFA/scripts/cfa_l2/`, and the rest is the original prompt.
> The `Kaplan/` slides and the official ratio and abbreviation lists are third-party copyrighted material and live only in the gitignored `17-CFA/Private/`.

Paste everything below the line into a fresh Claude Code session started from the vault root.

---

You are building my complete CFA Level II study platform inside my Obsidian vault.
My exam is on 24 November 2026.
Today is 2026-08-26, which leaves 90 days (12.9 weeks).
The goal is to score in the top band on every topic area and pass with distinction, not merely to pass.
The platform must be the single place I study from: it reads the official curriculum, teaches every learning outcome to first-principles depth, drills me with exam-realistic item sets, schedules my reviews, tracks my mastery per LOS, and tells me every morning exactly what to do.
Treat this as a production system whose failure mode is a wrong formula, a shallow explanation, or a weak area that stays invisible until exam day.

## 1. Ground truth (verified, do not re-derive)

### Source material

Official CFA Institute 2026 Level II curriculum, 19 PDFs, text-extractable with `pdftotext` (installed at /opt/homebrew/bin):

`$CFA_PDF_DIR` (a private cloud-drive folder `CFA/CFA L2/Books/2026/PDF/`; never committed)

| File | Topic | Pages | Learning modules |
|---|---|---|---|
| cfa-program2026L2V1.pdf | Quantitative Methods | 380 | LM1 Basics of Multiple Regression, LM2 Evaluating Regression Model Fit, LM3 Model Misspecification, LM4 Extensions of Multiple Regression, LM5 Time-Series Analysis, LM6 Machine Learning, LM7 Big Data Projects, plus Appendices A-E |
| cfa-program2026L2V2.pdf | Economics | 172 | LM1 Currency Exchange Rates: Understanding Equilibrium Value, LM2 Economic Growth |
| cfa-program2026L2V3.pdf | Financial Statement Analysis | 420 | LM1 Intercorporate Investments, LM2 Employee Compensation, LM3 Multinational Operations, LM4 Analysis of Financial Institutions, LM5 Evaluating Quality of Financial Reports, LM6 Integration of FSA Techniques |
| cfa-program2026L2V4.pdf | Corporate Issuers | 232 | LM1 Dividends and Share Repurchases, LM2 ESG Considerations in Investment Analysis, LM3 Cost of Capital: Advanced Topics, LM4 Corporate Restructuring |
| cfa-program2026L2V5.pdf | Equity Valuation | 474 | LM1 Applications and Processes, LM2 Discounted Dividend Valuation, LM3 Free Cash Flow Valuation, LM4 Market-Based Valuation, LM5 Residual Income Valuation, LM6 Private Company Valuation |
| cfa-program2026L2V6.pdf | Fixed Income | 316 | LM1 Term Structure and Interest Rate Dynamics, LM2 Arbitrage-Free Valuation Framework, LM3 Bonds with Embedded Options, LM4 Credit Analysis Models, LM5 Credit Default Swaps |
| cfa-program2026L2V7.pdf | Derivatives | 162 | LM1 Pricing and Valuation of Forward Commitments, LM2 Valuation of Contingent Claims |
| cfa-program2026L2V8.pdf | Alternative Investments | 274 | LM1 Commodities and Commodity Derivatives, LM2 Types of Real Estate Investment, LM3 Real Estate through Publicly Traded Securities, LM4 Hedge Fund Strategies |
| cfa-program2026L2V9.pdf | Portfolio Management | 388 | LM1 Economics and Investment Markets, LM2 Analysis of Active Portfolio Management, LM3 ETFs, LM4 Using Multifactor Models, LM5 Measuring and Managing Market Risk, LM6 Backtesting and Simulation |
| cfa-program2026L2V10.pdf | Ethical and Professional Standards | 286 | LM1 Code of Ethics and Standards, LM2 Guidance for Standards I-VII, plus any further modules; confirm from the TOC |
| cfa-program2026L2PrereqRead-Quantitative Methods.pdf | Prerequisite | 340 | Level I refresher |
| cfa-program2026L2PrereqRead-Financial Statement Analysis.pdf | Prerequisite | 310 | Level I refresher |
| cfa-program2026L2PrereqRead-Economics.pdf | Prerequisite | 242 | Level I refresher |
| cfa-program2026L2glossary.pdf, cfa-program2026L2PrereqRead-Glossary.pdf | Glossary | | |
| cfa-program-level-ii-common-abbreviations.pdf, cfa_program_level_ii_financial_ratio_list_2.pdf | Reference | | |
| mastering-your-calculator-for-the-cfa-exam.pdf | Calculator | | BA II Plus workflows |
| technical-append-to-analysis-of-active-portfolio-mgmt.pdf | Appendix | | Supports V9 LM2 |

Total: 44 learning modules, 3,104 curriculum pages, 892 prerequisite pages.
V1 front matter contains a "Topic area weights" section and "Designing Your Personal Study Program"; read it and use the official weights rather than assuming them.
The exam is 88 multiple-choice questions in 22 item sets (vignettes of 4 questions), two sessions of 2 hours 12 minutes, which is 3 minutes per question.

### The vault (current working directory)

- Domain hubs are the pattern: `Dashboard.md` links `Languages/POLYGLOT_HUB`, `Music/MUSIC_HUB`, `Health/HEALTH_HUB`.
  The CFA platform gets `17-CFA/CFA-L-2/CFA_L2_HUB.md` and a link in `Dashboard.md`.
- Core plugins enabled: bases, canvas, daily-notes, templates, slides, backlinks, outline, tag-pane, bookmarks, workspaces, graph, properties view is off.
- Community plugins installed: dataview, obsidian-tasks-plugin, templater-obsidian, quickadd (no choices configured yet), obsidian-kanban, obsidian-excalidraw-plugin, calendar, omnisearch, table-editor-obsidian, obsidian-git, remotely-save (mobile sync), obsidian-icon-folder.
  No spaced-repetition plugin is installed.
- Templates live in `Templates/` and use Templater syntax; `Templates/Daily-Note-Template.md` has a `## Quant/AI/Prog Progress` section that is the hook for CFA.
- The Languages system uses an inline `#flashcard` tag convention with a master bank note; do not break it.
- Scripts live in `.scripts/` (Python, one file per job).
- Existing CFA content: `17-CFA/CFA-L-2/` has `_Index_CFA-L-2.md` (its dataview queries the stale path `"17-CFA/CFA-L-2"`; the real path is `17-CFA/CFA-L-2`), a `Kaplan/IFT-Slides` folder of third-party slides, and 44 notes.
  There are iCloud conflict duplicates named `* 2.md` throughout `Quant/CFA/`; the old indexes use emojis.
- Python packages `pymupdf` and `pypdf` are not installed; `pdftotext -layout` is the extraction tool.
  Install anything else into a project venv, never globally.

## 2. Architecture: use every Obsidian feature that earns its place

Design principle: the curriculum content is written once, addressed by stable block IDs, and every other surface (formula sheet, flashcards, dashboards, canvases, mocks) is a query or an embed over it.
Nothing is duplicated by hand.

### 2.1 Folder layout

```
17-CFA/CFA-L-2/
  CFA_L2_HUB.md                      the front door: today block, mastery heatmap, countdown, links
  00-Strategy/
    Study-Plan.md                    90-day plan with Tasks due dates and weekly milestones
    Distinction-Strategy.md          what top-band candidates do differently, per topic
    Exam-Day-Playbook.md
    Calculator-Playbook.md           BA II Plus keystrokes per formula family
    Build-Checklist.md               your own progress on this build
  01-Quantitative-Methods/ ... 10-Ethics/
    _Index.md                        topic MOC with weight, LM table (Bases embed), dependency canvas embed
    LM01-<Title>.md                  one note per learning module (spec in 2.3)
    LOS/LM01-<a>.md ... optional only if a LOS is large enough to deserve its own note
  20-Item-Set-Bank/<topic>/IS-<topic>-LM<nn>-<k>.md
  21-Mocks/Mock-01.md ... Mock-06.md
  22-Attempts/<date>-<source>.md     one note per attempt, created by QuickAdd
  23-Error-Log/<date>-<slug>.md      one note per miss, created by QuickAdd
  30-Flashcards/<topic>.md           SRS decks
  40-Formula-Sheets/                 generated by script from block embeds
  50-Canvases/*.canvas               dependency maps and mind maps
  51-Diagrams/*.excalidraw.md        term structure, binomial trees, payoff diagrams, consolidation flows
  60-Bases/*.base                    LOS mastery, LM status, item-set log, error taxonomy
  70-Slides/*.md                     formula drill decks for the Slides core plugin
  Kaplan/                            leave as is
```

### 2.2 Data model (frontmatter properties are the database)

Every note carries typed properties so Bases and Dataview can query it.

LM note: `type: cfa-lm`, `topic`, `topic_code` (01-10), `volume`, `lm`, `title`, `pages`, `weight_band` (from V1), `difficulty` (1-5 with a one-line reason in the note), `los_count`, `status` (not-started, learning, practicing, mastered), `mastery` (0-100, computed by script from attempts), `next_review` (date), `last_reviewed`, `tags: [cfa/l2, cfa/<topic>]`.

Item set: `type: cfa-itemset`, `topic`, `lm`, `los: [ids]`, `difficulty`, `minutes: 18`, `source` (bank or mock-nn), `attempts` (count).

Attempt: `type: cfa-attempt`, `date`, `source` (item set or mock link), `score`, `max`, `minutes_used`, `confidence` (1-5, before seeing the answers), `los_hit: [ids]`, `los_missed: [ids]`.

Error: `type: cfa-error`, `date`, `topic`, `lm`, `los`, `question` (link), `picked`, `correct`, `cause` (one of: concept, formula, calculation, reading, timing, trap, guess), `rule` (the one-line rule I will apply next time), `resolved: false`.

LOS identity: every LOS gets a stable block ID on its line in the LM note, of the form `^los-<topic_code>-<lm>-<letter>` (for example `^los-06-03-c`).
Every formula gets `^f-<topic_code>-<lm>-<n>`.
Every worked example gets `^ex-<topic_code>-<lm>-<n>`.
All downstream surfaces reference these IDs, so a fix in the LM note propagates everywhere.

### 2.3 LM note spec (every section substantive, none a placeholder)

1. `## LOS map`: every LOS verbatim on its own line with its block ID, a one-line "what the examiner can ask" note, the command verb (calculate, evaluate, compare, explain) highlighted, and a link to the section that covers it.
2. `## Core intuition`: the module from first principles in your own words, as a strong tutor would explain it to someone who has passed Level I, before any formula appears; name the economic reason behind each mechanism; use `> [!abstract]` callouts for the two or three ideas everything else hangs on.
3. `## Formulas and derivations`: every formula in `$$` with its block ID, variable definitions, units, sign conventions, and a two-to-four-line derivation or the reason it holds; BA II Plus keystrokes in a `> [!tip] Calculator` callout where the exam expects computation.
4. `## Worked examples`: every curriculum example reworked step by step with the arithmetic shown, block ID, page reference, and result checked against the curriculum solution; recompute numeric examples in Python before writing them.
5. `## Item-set patterns`: the 5-10 ways this module appears in vignettes, the typical distractors, and the trap each sets (sign, annual vs semiannual, IFRS vs US GAAP, before vs after tax, spot vs forward, and so on) in `> [!warning] Trap` callouts.
6. `## Practice problems`: every end-of-module problem with the full reasoning behind the answer and each rejected option, inside `> [!question]` and foldable `> [!success]- Solution` callouts so I can attempt before revealing.
7. `## Cross-links`: `[[...]]` links to every module this one depends on or feeds; these drive the Canvas and graph view.
8. `## Self-test`: 10 hard original questions in item-set style with a foldable answer key.
9. `## Flashcards`: 30-60 cards for this module in the SRS plugin format (section 2.5), tagged `#flashcards/cfa-l2/<topic>/lm<nn>`.
10. `## Common mistakes`: numbered list, seeded from item-set patterns and appended to by the error-log workflow via a `dataview` list of unresolved errors for this LM.
11. `## Teach-back`: an empty callout where I write the module in my own words after Pass 1; the mastery script treats an empty teach-back as a cap of 60 on mastery.

Formatting: no emojis, no em dashes (plain dash), one sentence per line, LaTeX for all math, tables for comparisons, callouts as specified, `%% %%` comments for build notes.

### 2.4 Surfaces built on top of the LM notes

- `CFA_L2_HUB.md`: a `dataviewjs` block that computes days remaining, current pass and week from `Study-Plan.md`, and a "Today" list: due SRS decks, LM notes with `next_review <= today`, item sets scheduled by the plan, unresolved errors older than 7 days.
  Below it: a mastery heatmap (one cell per LM, colored by `mastery`), topic-weight vs mastery table (weight from V1, mastery as the mean of its LMs), mock score trend, error causes histogram, and the Kanban board embed.
- Bases (`60-Bases/`): `LM-Status.base` (all LM notes with status, mastery, next_review, filterable by topic), `LOS-Mastery.base` (one row per LOS, derived from attempts), `Attempts.base`, `Errors.base` (group by cause and by LM).
  Embed the relevant Base view in each topic `_Index.md`.
- Canvas (`50-Canvases/`): one dependency canvas per topic and one master canvas linking topic canvases, built from the `Cross-links` sections by a script that writes the `.canvas` JSON; edges labeled with what flows (for example "spot rates" from Term Structure to Arbitrage-Free Valuation).
- Excalidraw (`51-Diagrams/`): the diagrams that Level II rewards being able to draw from memory: binomial interest-rate tree with backward induction, callable and putable bond price vs yield, option payoff and profit diagrams, swap cash-flow timelines, consolidation vs equity method flows, translation vs remeasurement flows, term-structure shapes under each theory, pension cost components.
  Embed each in its LM note.
- Kanban (`00-Strategy/Study-Board.md`): columns Not Started, Reading, Practicing, Teach-Back Done, Mastered; one card per LM linking to the note; the mastery script moves cards.
- Tasks: every study-plan item is a `- [ ]` task carrying a due date in the Tasks plugin's dataview-style format (`[due:: YYYY-MM-DD]`), never the emoji format; set the plugin's global filter to `#cfa/plan` for these notes, so `tasks` queries in the daily note and the hub show what is due.
- Templater templates in `Templates/`: `CFA-Attempt-Template.md`, `CFA-Error-Template.md`, `CFA-Teach-Back-Template.md`, `CFA-Weekly-Review-Template.md`.
- QuickAdd choices: "CFA: log attempt", "CFA: log error", "CFA: weekly review", each creating the note in the right folder from its template with prompts for the properties; write the QuickAdd `data.json` entries and tell me the hotkeys to bind.
- Daily note integration: extend `Templates/Daily-Note-Template.md` under `## Quant/AI/Prog Progress` with a `dataviewjs` embed of the hub's Today block plus a `tasks` query for `#cfa/plan due today`, so the daily note is the study cockpit.
- Slides (`70-Slides/`): one formula-drill deck per topic, one formula per slide, answer on the next slide, for the last three days.
- Weekly review note (Templater): auto-filled with the week's attempts, score by topic, new errors by cause, LMs whose mastery fell, and the plan delta for next week.
- Graph view: define a graph group color per `cfa/<topic>` tag in the workspace so the dependency structure is visible; bookmarks for the hub, the study board, and the error log.
- Mobile: everything must render without dataviewjs where possible (Bases and plain dataview) so SRS review and item sets work on the phone through remotely-save; note which views are desktop-only.

### 2.5 Retention and mastery engine

- Install `obsidian-spaced-repetition`, configure the deck tag root `#flashcards`, and generate decks under `#flashcards/cfa-l2/<topic>/lm<nn>` inside each LM note's `## Flashcards` section plus a topic deck note in `30-Flashcards/` that embeds them.
  Card types: formula recall (cloze on the formula), definition, "which standard is violated and why", "which answer is the trap and why", "compute in 30 seconds" numeric micro-problems with calculator keystrokes.
  Keep the Languages system's `#flashcard` (singular) convention untouched.
- `17-CFA/scripts/cfa_l2/mastery.py`: computes per-LOS and per-LM mastery from attempts and errors (recency-weighted accuracy, confidence calibration penalty when confidence exceeds accuracy, teach-back cap), writes `mastery`, `status`, and `next_review` back to LM frontmatter, moves Kanban cards, and refreshes the heatmap data.
  Run it by a QuickAdd command that calls the script, and by a git pre-commit hook.
- Interleaving: the plan mixes topics from week 3 on; item-set sessions are never single-topic after Pass 1.
- Calibration: every attempt records confidence before revealing answers; the hub shows calibration by topic so over-confidence is visible.

### 2.6 Extraction pipeline (`17-CFA/scripts/cfa_l2/`)

1. `extract.py`: for each volume, `pdftotext -layout`, split into LMs using the TOC page numbers, write `build/cfa_l2/<topic>/<LM##>.txt` and `manifest.json` (volume, module, title, page range, characters).
2. `parse.py`: per module, extract to JSON: LOS, every numbered example with solution, every practice problem with solution and LOS mapping, every equation, every bolded glossary term.
   Where layout extraction mangles a formula, set `needs_review: true` with the page number instead of guessing.
3. `verify_extraction.py`: assert every LM has non-empty LOS, examples, and problems; print a coverage table; exit non-zero on any gap.
4. `build_formula_sheet.py`: generates `40-Formula-Sheets/Master-Formula-Sheet.md` and per-topic sheets purely from `![[LM#^f-...]]` embeds, grouped by topic and LM, never hand-edited.
5. `build_canvases.py`: generates the `.canvas` files from `Cross-links`.
6. `verify_notes.py`: every LM note has all 11 sections non-empty, every LOS from Layer A appears with a block ID, every formula ID is unique and embedded in the sheet, every item set links to valid LOS IDs, no emoji or em dash anywhere in `17-CFA/CFA-L-2/`.
7. `verify_practice.py`: item-set counts per LM, each mock has exactly 22 item sets with topic counts inside the official weight bands, SRS decks parse (no card without a separator, no duplicate cards).

## 3. Content requirements

- Item-set bank: at least 3 original item sets per LM (minimum 132), each a 400-600 word vignette with 4-6 questions, plausible distractors, full reasoning for every option, LOS IDs per question, and a 18-minute timer note; weight the count toward FSA, Equity, Fixed Income, Ethics, PM, and Quant.
- Mocks: 6 full mocks of 22 item sets, topic mix inside the official weight bands, difficulty at or above the curriculum's practice problems; Mocks 1-2 draw from the bank, Mocks 3-6 are fresh; each mock has an answer-entry table that a QuickAdd command turns into an attempt note.
- `Distinction-Strategy.md`: per topic, what separates top-band scripts: the LOS verbs that appear most, the computations that must be automatic, the qualitative traps (Ethics standard boundaries, FSA IFRS vs US GAAP, PM active-management definitions), the time allocation per item set, and the guessing policy.
- `Calculator-Playbook.md`: built from the calculator PDF plus every formula the exam expects on the BA II Plus, as keystroke tables, with the worksheet resets and the common mode errors (P/Y, BGN, AOS).
- Prerequisite readers: a short refresher note per prerequisite PDF with links from the Level II modules that assume them.

## 4. The 90-day plan (write it into `00-Strategy/Study-Plan.md` as Tasks with due dates)

Three passes, overlapping on purpose.

- Pass 1, weeks 1-7 (26 Aug to 13 Oct): learn all 44 modules in this order: Quant, FSA, Equity, Fixed Income, Derivatives, Corporate Issuers, Economics, Alternatives, Portfolio Management, Ethics last but with the Standards read once in week 1.
  Order is dependency first, weight second; justify any deviation.
  Each module: read the note, rework every example, do the practice problems, do one item set, write the teach-back, start its SRS deck.
  Daily SRS from day 1; interleaved item sets from week 3.
- Pass 2, weeks 8-10 (14 Oct to 3 Nov): item sets only, 6-8 per day, mixed topics, timed at 18 minutes; every miss becomes an error note; Mock 1 end of week 8, Mock 2 end of week 10.
- Pass 3, weeks 11-13 (4 Nov to 23 Nov): Mocks 3-6 on alternating days at full timing; off days on the error log, formula sheet, Slides drill, Ethics rereads; final 3 days formula and calculator drill only.

Assume 3.5 hours on weekdays and 7 hours on weekend days (about 450 hours), state it in the plan as editable properties, and set weekly milestones: mastery targets per topic, attempts per week, and a target of 85 percent or higher on Mock 6.
The hub must show, every day, whether I am ahead or behind plan.

## 5. Quality bar and non-negotiables

- Every formula, number, and standard traceable to a volume and page, cited inline as `(V6 p.143)`.
- Never invent a formula, standard number, or answer; when extraction is unclear, reopen the pages with `pdftotext -f N -l M` and read them.
- Recompute every numeric example in Python; if it disagrees with the curriculum, investigate until you know why and record which is right.
- Explain like a tutor who wants me to derive the formula under pressure, not a summarizer.
- Full depth on every module; do not thin out later topics to finish.
- Fix the vault hygiene issues in section 1 first: correct the stale dataview path, remove the ` 2.md` duplicates after confirming they are byte-identical or older than the originals, replace the old emoji indexes.
- No emojis, no em dashes, one sentence per line, consistent with the rest of my instructions.
- Every plugin configuration you write (QuickAdd, Templater folder templates, Tasks, spaced repetition) must be tested by opening the vault feature it drives; if you cannot test a plugin behavior, say so explicitly rather than claiming it works.

## 6. How to execute

1. Read this prompt, read the V1 front matter for the official weights and study guidance, then write `00-Strategy/Build-Checklist.md` with every LM, every surface in section 2.4, and every gate; keep it updated.
2. Fix vault hygiene, create the folder skeleton, the hub, the templates, the QuickAdd choices, and the Bases, all with placeholder-free structure, and confirm they render.
3. Build the extraction pipeline end to end; run `verify_extraction.py`; show me the coverage table before writing any LM note.
4. Write LM notes topic by topic, one subagent per LM in parallel within a topic, each given the full note spec and the module's extracted JSON; after each topic run `verify_notes.py`, `build_formula_sheet.py`, `build_canvases.py`, and `mastery.py`, and commit.
5. Generate item sets and flashcards per LM the same way, then assemble the mocks, then run `verify_practice.py`.
6. Write the study plan, the distinction strategy, the calculator playbook, the prerequisite refreshers, the Excalidraw diagrams, and the Slides decks.
7. Commit at every gate with a message naming the layer, the topic, and the verification output; ship through `no-mistakes`, never a bare push.
8. Final report: what was built, all verification outputs, counts (LM notes, LOS IDs, formulas, examples, problems, item sets, mocks, cards, canvases, diagrams, bases), the hotkeys to bind, which views are desktop-only, and the first three days of the plan so I can start immediately.

Start with step 1.
