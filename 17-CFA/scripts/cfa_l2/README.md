# CFA Level II Pipeline

Turns the ten 2026 curriculum volumes into an Obsidian study platform under `17-CFA/CFA-L-2/` and keeps it verified.
Exam date is 24 November 2026.
Run every script from the repository root: `python3 17-CFA/scripts/cfa_l2/<script>.py`.
The pipeline moved here from the author's private Obsidian vault on 2026-10-15; it is unchanged apart from paths.

## Layers

```text
PDFs  -->  extract.py  -->  build/cfa_l2/<topic>/LM<nn>.txt + manifest.json
              |
              v
          parse.py     -->  build/cfa_l2/<topic>/LM<nn>.json + los_index.json
              |
              v
     verify_extraction.py   gate: every module has LOS, examples, problems with solutions
              |
              v
   LM notes written by agents per NOTE_SPEC.md  -->  17-CFA/CFA-L-2/<topic>/LM<nn>-<Title>.md
              |
              v
       verify_notes.py      gate: 11 sections, LOS block IDs, formula IDs, no emoji, em dash or draft leftover
              |
              v
   build_plan.py  build_formula_sheet.py  build_canvases.py  build_slides.py  build_diagrams.py
              |
              v
   item sets and mocks written by agents per ITEMSET_SPEC.md and MOCK_SPEC.md; build_mocks.py assembles Mocks 1 to 6
              |
              v
      verify_practice.py    gate: item sets per LM, mock composition inside weight bands, SRS decks parse
              |
              v
          mastery.py        attempts and errors -> mastery in frontmatter, study board rebuilt
```

## Inputs and environment

| Variable | Default | Meaning |
|---|---|---|
| `CFA_PDF_DIR` | `17-CFA/Private/Curriculum-PDF` (gitignored) | Where `cfa-program2026L2V<n>.pdf` for volumes 1 to 10 live |
| `CFA_VAULT` | the repository root inferred from the script location | Override only when running against another checkout |
| `CFA_BUILD` | `build/cfa_l2` under `CFA_VAULT` | The curriculum extracts; point a worktree at the main checkout's copy |
| `CFA_PRIVATE` | `17-CFA/Private` under `CFA_VAULT` | The private overlay; point a worktree at the main checkout's copy |

The curriculum PDFs and everything `extract.py` and `parse.py` derive from them are copyrighted by CFA Institute.
They stay out of git: the PDFs in `17-CFA/Private/` or wherever `CFA_PDF_DIR` points, the extracts in `build/cfa_l2/` (both gitignored).
Each LM note's Practice problems section restates the curriculum's end-of-module problems, so its body lives in `17-CFA/Private/CFA-L-2/Practice-Problems/` and the public note embeds it; `verify_notes.py` and `notes_todo.py` follow the embed, and accept it unchecked when the overlay is absent.
The gates need the extracts, so they run from the main checkout, or from a worktree with `CFA_BUILD` and `CFA_PRIVATE` set to the main checkout's copies; without the extracts they stop with `FileNotFoundError`.

`extract.py` shells out to `pdftotext -layout` (poppler); install it with `brew install poppler`.
No third-party Python packages are used.

Topic codes, slugs, volumes, and official weight bands are defined once in `cfa_common.py` (`TOPICS`) and imported everywhere:

| Code | Folder | Weight |
|---|---|---|
| 01 | 01-Quantitative-Methods | 5-10% |
| 02 | 02-Economics | 5-10% |
| 03 | 03-Financial-Statement-Analysis | 10-15% |
| 04 | 04-Corporate-Issuers | 5-10% |
| 05 | 05-Equity-Valuation | 10-15% |
| 06 | 06-Fixed-Income | 10-15% |
| 07 | 07-Derivatives | 5-10% |
| 08 | 08-Alternative-Investments | 5-10% |
| 09 | 09-Portfolio-Management | 10-15% |
| 10 | 10-Ethics | 10-15% |

## Scripts

| Script | What it does | Writes |
|---|---|---|
| `extract.py` | Splits each volume into learning-module text files with form feeds between pages and records the printed-page offset per module | `build/cfa_l2/<topic>/LM<nn>.txt`, `build/cfa_l2/manifest.json` |
| `parse.py` | Turns module text into structured JSON: LOS, examples, knowledge checks, practice problems, solutions, equation candidates; anything it cannot read cleanly is flagged `needs_review` with a page | `build/cfa_l2/<topic>/LM<nn>.json`, `build/cfa_l2/los_index.json` |
| `verify_extraction.py` | Gate for the extraction layer, 45 of 45 modules must pass | stdout, exit code |
| `notes_todo.py [--json] [--topic NN]` | Lists modules that still need a note, or whose note is too thin in a required section, with every path, LOS ID, and cross-link name an author needs | stdout |
| `verify_notes.py [NN]` | Gate for the LM notes: 11 sections present and substantive, every LOS from extraction present with a block ID, formula IDs unique and embedded in the formula sheet, no emoji, em dash or draft leftover (author reasoning left in the text, such as `wait:`, a line starting `Correction:`, `scratch that` or `let me recompute`) under `CFA-L-2` | stdout, exit code |
| `build_plan.py` | Regenerates the study plan from the manifest and the hour assumptions in the plan's frontmatter; Pass 1 hours are proportional to module length with a 3-hour floor, distributed by water-filling | `00-Strategy/Study-Plan.md` with `[due:: ]` tasks |
| `build_formula_sheet.py` | Master and per-topic sheets made entirely of block embeds of `^f-<code>-<lm>-<n>` from the notes; no formula is retyped | `40-Formula-Sheets/*.md` |
| `build_canvases.py` | One dependency canvas per topic plus a master canvas, edges labelled from each note's Cross-links section | `50-Canvases/*.canvas` |
| `build_diagrams.py` | Excalidraw drawings of the mechanisms the exam rewards drawing from memory | `51-Diagrams/*.md` |
| `build_slides.py` | One formula-drill deck per topic, prompt slide then answer slide per formula, for the core Slides plugin | `70-Slides/<topic>-Formula-Drill.md` |
| `build_mocks.py` | Assembles all six mocks inside the weight bands (22 sets: Quant 2, Econ 1, FSA 3, Corporate 2, Equity 3, FI 3, Deriv 2, Alts 1, PM 3, Ethics 2): Mocks 1 and 2 embed `source: bank` sets with no module repeated, Mocks 3 to 6 inline the fresh sets tagged `source: mock-0<n>`; rerun after editing any item set | `21-Mocks/Mock-01.md` to `Mock-06.md` |
| `verify_practice.py` | Gate for the practice layer: at least 3 bank sets per LM; per set the frontmatter keys, LOS IDs valid for the module, one LOS tag and one keyed answer per question, 4 to 6 questions (exactly 4 for mock sets), all four sections, no emoji or em dash; fresh mocks have no repeated module and at least 6 difficulty-4 sets; mock composition inside the bands; spaced-repetition decks parse with no duplicate prompts | stdout, exit code |
| `mastery.py` | Computes mastery per module from attempts and the error log, rewrites only `mastery`, `status`, `last_reviewed`, `next_review` in each note's frontmatter, and regenerates the Kanban board | LM note frontmatter, `00-Strategy/Study-Board.md` |

### Mastery model

Score 0 to 100 per module.

- Accuracy: recency-weighted over attempts touching the module, half-life 14 days; 0 with no attempts.
- Errors: each unresolved error on the module subtracts 4 points, capped at 20.
- Calibration: if mean confidence exceeds accuracy by more than 10 points, the excess is subtracted, capped at 15.
- Teach-back: a Teach-back section with 200 or fewer characters of prose caps mastery at 60.
- Status: not-started, learning (below 50), practicing (50 to 84), mastered (85 and above).
- Next review: 1, 3, 7, 14, or 30 days after the last attempt depending on mastery.

## Agent specifications

Notes, item sets, and fresh mocks are written by AI agents, one module at a time, following these specifications verbatim:

- `NOTE_SPEC.md`: the 11-section learning-module note, its frontmatter, block-ID scheme, and minimum sizes. One note costs roughly 100k to 200k tokens.
- `ITEMSET_SPEC.md`: original vignettes with 4 to 6 questions, plausible distractors derived from named errors, every number recomputed in Python.
- `MOCK_SPEC.md`: Mocks 3 to 6, 22 fresh item sets each inside the official bands.

Identifiers the specs rely on:

- LOS: `los-<code>-<lm>-<letter>` from `build/cfa_l2/los_index.json`, attached as block IDs `^los-...` on the LOS map lines.
- Formulas: `^f-<code>-<lm>-<n>`, directly after the closing `$$` of the display block.
- Examples: `^ex-<code>-<lm>-<n>`.
- Flashcard decks: `#flashcards/cfa-l2/<topic-slug>/lm<nn>`.

## Folders the pipeline owns

| Folder | Content |
|---|---|
| `00-Strategy` | Build checklist (source of truth for progress), study plan, study board, playbooks, prerequisites |
| `01-` to `10-` | One folder per topic holding the LM notes |
| `20-Item-Set-Bank` | Item sets per topic slug, `type: cfa-itemset`, `source: bank` or `mock-0n` |
| `21-Mocks` | `Mock-01` to `Mock-06` |
| `22-Attempts`, `23-Error-Log` | Created from the CFA Attempt and CFA Error templates through Templater folder templates; read by `mastery.py`; personal, gitignored |
| `24-Weekly-Reviews` | Created from the CFA Weekly Review template; personal, gitignored |
| `40-Formula-Sheets`, `50-Canvases`, `51-Diagrams`, `60-Bases`, `70-Slides` | Generated artifacts; regenerate, do not hand-edit |

## Resuming a build

1. Read `17-CFA/CFA-L-2/00-Strategy/Build-Checklist.md`.
2. Run `notes_todo.py` to see which modules lack a note.
3. Spawn one authoring agent per module with `NOTE_SPEC.md` as the prompt, then run `verify_notes.py <code>`.
4. Rebuild the derived artifacts (formula sheets, canvases, slides) and run `verify_practice.py` before shipping.

The build is larger than one session's quota by design; resume from the checklist, never restart.
