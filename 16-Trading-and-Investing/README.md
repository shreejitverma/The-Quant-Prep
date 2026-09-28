---
type: moc
track: [quant-trader, quant-research]
tier: advanced
status: draft
curriculum: false
sources: []
---

# Trading and Investing Library

Discretionary markets knowledge that complements the quant syllabus: finance fundamentals, valuation, value and growth investing, macro, capital allocation, hedge funds, private markets, and about 100 single-stock research notes.
It came over from the author's private Obsidian second brain in September 2026 and is written Obsidian-first: notes use wikilinks and Dataview, and some link back to the private vault through `obsidian://` URIs that only resolve on the author's machine.

This section is a library, not part of the tracked syllabus (`curriculum: false`): `qp` lists it but does not validate or track it.
About 150 wikilinks point at concept notes that are not written yet; they are this library's writing backlog.

## Contents

- [Finance index](Finance/_Index_Finance.md): asset pricing, corporate finance, fixed income, microstructure, portfolio theory, risk, trading.
- [Investing index](Investing/_Index_Investing.md): value, growth, valuation models, macro, capital allocation, hedge funds, private equity, venture capital, real estate, stock research.
- [Build prompt](Investing/_PROMPT_Markets_Mastery_OS_Build.md): the phased plan for turning this library into a practice-first markets platform.
- `scripts/`: the stock and macro data pipeline (Yahoo Finance via yfinance). Run from the repo root; the scripts rewrite notes in place, so commit or stash first. `generate_stocks.py` skips existing notes unless given `--force`.

## Private journals

Personal trade journals, positions and portfolio notes go in [Private/](Private/README.md), which is gitignored except for its README, so they never reach the public repository.
That folder has no backup by default; keep a separate private backup.
