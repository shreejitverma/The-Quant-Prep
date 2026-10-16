---
type: moc
track: [quant-research, quant-trader]
tier: advanced
status: draft
curriculum: false
sources: []
---

# CFA Library

A complete CFA Level II study platform for the 2026 curriculum (exam 24 November 2026), with its build pipeline.
It came over from the author's private Obsidian second brain in October 2026 and is written Obsidian-first: notes use wikilinks, Dataview, Bases, Excalidraw, Templater, QuickAdd and the Spaced Repetition plugin.
Install the pinned plugins with `python3 tools/obsidian/bootstrap.py` before opening it in Obsidian.

This section is a library, not part of the tracked syllabus (`curriculum: false`): `qp` lists it but does not validate or track it.
Its own gates are the pipeline's verify scripts, below.

## Contents

- [CFA Level II hub](CFA-L-2/CFA_L2_HUB.md): the front door; reviews due, unresolved errors, mastery heatmap, weight against mastery, attempts and calibration, errors by cause, study board.
- [Build checklist](CFA-L-2/00-Strategy/Build-Checklist.md), [study plan](CFA-L-2/00-Strategy/Study-Plan.md), [distinction strategy](CFA-L-2/00-Strategy/Distinction-Strategy.md), [exam-day playbook](CFA-L-2/00-Strategy/Exam-Day-Playbook.md) and [calculator playbook](CFA-L-2/00-Strategy/Calculator-Playbook.md).
- `CFA-L-2/01-` to `10-`: one note per learning module, 45 in all, each with the LOS map, intuition, formulas with block IDs, worked examples, item-set patterns, practice problems, self-test, flashcards, common mistakes and a teach-back.
- `CFA-L-2/20-Item-Set-Bank/` (256 original item sets: 168 bank sets and 88 fresh sets for Mocks 3 to 6) and `CFA-L-2/21-Mocks/` (six mocks inside the official topic weight bands).
- `CFA-L-2/40-Formula-Sheets/`, `50-Canvases/`, `51-Diagrams/`, `60-Bases/`, `70-Slides/`: generated artifacts; regenerate them, do not hand-edit.
- [Pipeline](scripts/cfa_l2/README.md): extraction, verification, plan, formula sheets, canvases, slides, diagrams, mocks and mastery, plus the agent specifications for notes, item sets and mocks.
- Templates `CFA-Attempt`, `CFA-Error`, `CFA-Teach-Back` and `CFA-Weekly-Review` in the repository's `Templates/`; the QuickAdd commands "CFA: log attempt", "CFA: log error" and "CFA: weekly review" create notes from them.

## Run the gates

From the repository root:

```sh
python3 17-CFA/scripts/cfa_l2/notes_todo.py        # learning-module notes still missing or too thin
python3 17-CFA/scripts/cfa_l2/verify_notes.py      # gate: sections, LOS coverage, formula IDs, style
python3 17-CFA/scripts/cfa_l2/verify_practice.py   # gate: item sets, mocks vs their item sets, flashcard decks
python3 17-CFA/scripts/cfa_l2/mastery.py           # recompute mastery and rebuild the study board
```

The gates read the curriculum extracts in `build/cfa_l2/`, which `extract.py` and `parse.py` produce from the curriculum PDFs; neither the PDFs nor the extracts are committed.
Run them from the main checkout, or from a worktree with `CFA_BUILD` and `CFA_PRIVATE` pointing at the main checkout's `build/cfa_l2` and `17-CFA/Private`.

## What is not published

The CFA Institute curriculum and third-party prep material are copyrighted, so they stay on the author's machine:

- `Private/` (gitignored except its [README](Private/README.md)): the CFA Level I notes, the Kaplan and IFT slide notes with their images, the official ratio and abbreviation lists, and every LM note's Practice problems section (the curriculum's end-of-module problems restated), all of which reproduce copyrighted text. The public notes embed their Practice problems, so those render only where `Private/` exists.
- `build/cfa_l2/` (gitignored): the curriculum text and structure extracted from the PDFs.
- `CFA-L-2/22-Attempts/`, `23-Error-Log/` and `24-Weekly-Reviews/` (gitignored except a placeholder): personal study logs.

Everything committed here is the author's own work: notes paraphrase the curriculum and cite volume and page, worked examples are reworked step by step, item sets and mocks are original, and learning outcome statements are quoted with their source.
By the author's choice, the Ethics notes and item sets quote the freely published CFA Institute Code of Ethics and Standards of Professional Conduct verbatim, with volume and page cites.
Derived study progress is published deliberately: `mastery.py` writes mastery, status and review dates into each note's frontmatter and rebuilds the study board.
