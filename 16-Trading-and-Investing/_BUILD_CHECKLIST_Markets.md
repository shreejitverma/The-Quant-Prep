---
type: build-checklist
title: "Markets Mastery OS Build Checklist"
tags: [markets, trading, investing, checklist, roadmap]
date: 2026-10-16
status: in-progress
---

# Markets Mastery OS Build Checklist

This document is the master resume point and execution ledger for the Markets Mastery platform.
It tracks inventory coverage across the vault, records defect resolution, and governs progression through all fourteen delivery phases.

---

## 1. Phase 0 Defect Resolution Ledger

All three known defects identified in the Markets Mastery build specification have been isolated, root-caused, repaired, and verified with automated tests.

### Defect 1: Misplaced Blocks Below the Closing Fence
- **Root cause**: `update_market_data.py` previously embedded `---` delimiters inside its replacement metadata string.
  Subsequent executions of `fetch_historical_value.py` used `split('---', 2)`, which partitioned the note into an opening fence, a frontmatter block, and body text containing the misplaced `last_updated` and `market_data` blocks.
  Regex cleaners only purged the frontmatter block, stranding metadata in the body text across 98 of 103 notes.
  Dataview queries could not access these fields because they were outside YAML frontmatter.
- **Repair**: Created `16-Trading-and-Investing/scripts/stock_notes.py` using standard-library frontmatter parsing and manipulation.
  Wrote `16-Trading-and-Investing/scripts/migrate_stock_notes.py` to relocate misplaced blocks into frontmatter.
  Updated `update_market_data.py` to use `stock_notes.set_block` so misplaced fences can never recur.
- **Verification**: Verified across all 123 notes in `16-Trading-and-Investing/Investing/Stock Research`.
  Misplaced blocks below the closing fence dropped from 98 to exactly 0.

### Defect 2: Silent Fetch Failures Masquerading as Numbers
- **Root cause**: Non-US tickers and share classes lacked mapping to exchange-qualified symbols in `update_market_data.py` and `quant_reverse_dcf.py`.
  When fetches returned None or empty cash flow, scripts wrote `price: None`, `market_cap: None`, or executed a naive loop in `solve_implied_growth` that defaulted to `0%`.
  This produced 38 notes with `price: None` and 34 notes with `implied_growth_rate: 0%`.
- **Repair**: Consolidated global ticker mappings into `stock_notes.TICKER_MAP`.
  Implemented bisection root-finding in `stock_notes.solve_implied_growth` and `implied_growth_from_fcf_yield`.
  When price or free cash flow is missing or non-positive, the solver explicitly returns status codes (`missing_price`, `missing_fcf`, `non_positive_fcf`) rather than a numerical 0%.
  Market data blocks now strip None and zero placeholders and record `data_quality: missing` with an explicit list of missing fields.
- **Verification**: Zero notes carry `price: None` (dropped from 38 to 0).
  Zero notes carry `implied_growth_rate: 0%` (dropped from 34 to 0).
  83 notes have verified, mathematically solved implied growth rates; 15 notes have documented `non_positive_fcf` status.

### Defect 3: Boilerplate Company Notes Marked Complete
- **Root cause**: Generator scripts created initial company notes with boilerplate one-line theses while hardcoding `status: complete` in frontmatter.
- **Repair**: Migrated all 98 active ticker notes to `status: stub`.
  Migrated 5 corporate failure case studies in `Historical/` to clean case-study frontmatter with `status: historical-case`.
- **Verification**: 98 notes set to `status: stub`; 5 notes set to `status: historical-case`.
  Unit test suite in `tools/tests/test_stock_notes.py` covers frontmatter manipulation, ticker extraction, block relocation, and reverse DCF bisection.

---

## 2. Vault Coverage Matrix

Status key:
- **COMPLETE**: Concept notes, formulas, and code already exist in the syllabus (`01` through `15`).
  Section 16 links into them rather than duplicating content.
- **PARTIAL**: Stubs, indexes, or foundational implementations exist, but require systematic curriculum expansion, drills, or simulator integration.
- **MISSING**: No structured content or simulator engine exists yet; scheduled in delivery phases.

| Domain / Module | Current Vault Asset | Status | Plan Resolution |
| :--- | :--- | :--- | :--- |
| **Track 0: Pro Quant Trading** | `07-Market-Microstructure` (12 notes), `08-Market-Making` (12 notes), `11-Risk-and-Trading` (17 notes) | PARTIAL | Add desk practice notes; wire to LOB, MM, and interview games labs (Phase 6) |
| **Track 1: Fundamental Analysis** | `16-Trading-and-Investing/Investing/Stock Research` (98 notes), `Templates/Value_Investing_Profile.md` | PARTIAL | Build 10-K, 3-statement linkage, forensic accounting notes and statement drills (Phase 11) |
| **Track 2: Valuation** | `16-Trading-and-Investing/Investing/Valuation Models/Reverse DCF.md`, `scripts/quant_reverse_dcf.py` | PARTIAL | Add DCF rebuilds, SOTP, multiples, expectations investing notes and valuation drills (Phase 11) |
| **Track 3: Value Investing** | `16-Trading-and-Investing/Investing/Value Investing/_Index_Value Investing.md` (stub) | PARTIAL | Build Graham-to-Buffett lineage, checklists, capital allocation, moat notes (Phase 11) |
| **Track 4: Portfolio Construction** | `09-Alpha-Research-and-Portfolio` (10-12), `16-Trading-and-Investing/Investing/Risk Management/Correlation Matrix.md` | PARTIAL | Build asset allocation, factor decay, drawdown maths, rebalancing notes (Phase 11) |
| **Track 5: Technical Analysis** | `16-Trading-and-Investing/Finance/Trading/_Index_Trading.md` (stub) | MISSING | Build TA curriculum with peer-reviewed evidence blocks and grades (Phase 8) |
| **Track 6: Trading (Discretionary & Systematic)** | `11-Risk-and-Trading` (01-02, 05-09), `09-Alpha-Research-and-Portfolio` (01-08) | PARTIAL | Build retail base rates, trade planning, setup taxonomy, decision ledger (Phase 6, 9) |
| **Asset Class: US Equities & ETFs** | `07-Market-Microstructure` (01-09), `06-Fixed-Income` (08) | COMPLETE | Cross-linked from Track 0 and 6; wired to LOB Lab (Phase 4) |
| **Asset Class: India Equities & F&O** | None | MISSING | Add NSE/BSE structure, settlement, margin, SEBI retail study citations (Phase 12) |
| **Asset Class: Options & Volatility** | `05-Derivatives-and-Volatility` (16 notes, `code/`) | COMPLETE | Cross-link syllabus; build options desk simulator and volatility trading notes (Phase 7) |
| **Asset Class: Rates & Fixed Income** | `06-Fixed-Income-and-Asset-Classes` (25 notes, `code/`) | COMPLETE | Cross-link syllabus; build curve, basis, and DV01 drills (Phase 12) |
| **Asset Class: FX & Interest Rate Parity** | `06-Fixed-Income-and-Asset-Classes/07-FX-Markets-and-Interest-Rate-Parity.md` | COMPLETE | Cross-link syllabus; build FX forward and carry trade drills (Phase 12) |
| **Asset Class: Commodities & Curves** | `06-Fixed-Income-and-Asset-Classes/09-Commodities-and-Futures-Curves.md` | COMPLETE | Cross-link syllabus; build contango/backwardation and storage drills (Phase 12) |
| **Asset Class: Crypto Market Structure** | `06-Fixed-Income-and-Asset-Classes/10-Crypto-Market-Structure.md` | COMPLETE | Cross-link syllabus; build perp funding, basis, and liquidation drills (Phase 12) |
| **Asset Class: Event-Driven & Special Situations** | None | MISSING | Build merger arb, spinoff, index inclusion, capital structure arbitrage notes (Phase 12) |
| **Cross-Cutting: Trading Psychology** | `11-Risk-and-Trading/09-Trading-Intuition-and-Judgement.md` | PARTIAL | Build cognitive biases, tilt detection, discipline and review systems (Phase 13) |
| **Cross-Cutting: Probability & Decisions** | `01-Probability`, `11-Risk-and-Trading` (01-02) | COMPLETE | Cross-link syllabus; wire calibration scoring into Replay Lab (Phase 8) |
| **Cross-Cutting: Market History Case Files** | `16-Trading-and-Investing/Finance/Financial History/_Index_Financial History.md` (stub) | PARTIAL | Build 10 historical crisis case files with primary-source citations (Phase 13) |
| **Cross-Cutting: Regulation, Tax, Operations** | `07-Market-Microstructure/Regulation` | PARTIAL | Build PDT, wash sale, Reg SHO, Indian STT/tax, margin framework notes (Phase 13) |
| **Cross-Cutting: Quant & Trading Careers** | `13-Interview-Playbook` (01, 10-12), `14-Firms` | COMPLETE | Cross-link firm profiles and interview expectations (Phase 13) |
| **Masters Codex** | None | MISSING | Build 30+ verified master profiles with primary sources and failure modes (Phase 2) |
| **Markets Canon** | None | MISSING | Build 60+ tiered literature syllabus with verified references (Phase 2) |
| **Interactive Simulators** | `MarketMakingGame` in `tools/qp/drills.py` | PARTIAL | Build `tools/qp/lab/` suite across 12 distinct engines (Phases 3, 4, 5, 7, 8, 9, 10, 12, 14) |
| **Trade Journal & Ledger** | None | MISSING | Build schema v2 journal, trade log, decision ledger, and analytics (Phase 1, 10) |

---

## 3. Phased Execution Roadmap

Progress is tracked sequentially.
Each phase produces working software, tested content, and passing verification commands before merging.

### Phase 0: Inventory, Defect Repair, and Master Checklist
- [x] Reproduce and document root causes for misplaced blocks and numerical failures.
- [x] Create standard-library frontmatter helper `16-Trading-and-Investing/scripts/stock_notes.py`.
- [x] Write and pass unit test suite `tools/tests/test_stock_notes.py`.
- [x] Execute migration across all 103 stock research notes; relocate misplaced blocks and normalize values.
- [x] Refactor `update_market_data.py`, `quant_reverse_dcf.py`, `fetch_historical_value.py`, `quant_sector_benchmarker.py`, and `generate_stock_moc.py`.
- [x] Compile comprehensive coverage matrix and write `16-Trading-and-Investing/_BUILD_CHECKLIST_Markets.md`.

### Phase 1: Hub, Templates, Verifier, and Platform Shell
- [ ] Create `16-Trading-and-Investing/MARKETS_HUB.md` with links to tracks, labs, disclaimers, and dashboard.
- [ ] Create folder index maps for all `Finance/` and `Investing/` subdirectories.
- [ ] Author standard YAML templates in `Templates/` (`Markets-Investment-Memo.md`, `Markets-Trade-Plan.md`, `Markets-Trade-Log.md`, `Markets-Decision-Journal.md`, `Markets-Post-Mortem.md`, `Markets-Weekly-Review.md`, `Markets-Monthly-Review.md`, `Markets-Drill-Attempt.md`).
- [ ] Build content verifier `16-Trading-and-Investing/scripts/verify_markets.py`.
- [ ] Register `mkt-` card prefix in `00-Start-Here/Note-Conventions.md` and `tools/qp/check.py`.
- [ ] Implement State Schema v2 with atomic migration in `tools/qp/state.py`.
- [ ] Scaffold `tools/qp/lab/` package, `/api/lab/catalog` route in `server.py`, and Trading Lab navigation in web app.

### Phase 2: Curriculum Structure, Markets Canon, and Masters Codex
- [ ] Author `16-Trading-and-Investing/00 Curriculum/Learning Path.md` with Mermaid progression graph.
- [ ] Author `16-Trading-and-Investing/00 Curriculum/Markets Canon.md` with 60+ verified publications across Gateway, Core, and Capstone tiers.
- [ ] Author `16-Trading-and-Investing/00 Curriculum/Masters Codex.md` and initial 10 verified master profiles.
- [ ] Wire curriculum navigation into `MARKETS_HUB.md` and repo `README.md`.

### Phase 3: Synthetic Market Engine & Sizing / Ruin Lab
- [ ] Implement synthetic price-path generator `tools/qp/lab/market.py` with analytical and Monte Carlo oracle.
- [ ] Implement Sizing and Risk of Ruin simulator `tools/qp/lab/sizing.py`.
- [ ] Add unit tests for generator statistical moments, regime transitions, and Kelly growth peaks.
- [ ] Build web UI for Sizing Lab with Monte Carlo equity fan charts.

### Phase 4: Limit Order Book & Execution Lab
- [ ] Implement price-time priority matching engine `tools/qp/lab/book.py`.
- [ ] Implement execution simulator `tools/qp/lab/execution.py` with zero-intelligence and informed Poisson arrivals.
- [ ] Implement Almgren-Chriss, TWAP, and VWAP benchmarks with implementation shortfall scoring.
- [ ] Add unit tests verifying order conservation, price priority, and no crossed books.
- [ ] Build web UI with interactive depth ladder, time and sales tape, and execution report.

### Phase 5: Market Making Upgrade & Interview Games Lab
- [x] Refactor and upgrade market-making engine into `tools/qp/lab/mm_quote.py` with multi-level progression.
- [x] Implement exact PnL attribution (spread capture, inventory carry, adverse selection, transaction fees).
- [x] Implement interview trading games engine `tools/qp/lab/games.py` (card and dice quoting games).
- [x] Ensure backward compatibility with existing `/api/mm/*` endpoints and Trading Lab shell.
- [x] Test MM quoting engine and games with automated test suite.

### Phase 6: Professional Quant & Trading Track Foundations
- [x] Author Track 0 (Pro Quant Trading) Foundations and Core concept notes (Desk Roles, Fair Value, Order Flow, Inventory Risk).
- [x] Author Track 6 (Trading) Foundations and Core concept notes with retail base-rate evidence (Base Rates, Sizing, Stops, Setups).
- [x] Author 256 `mkt-trd-` and `mkt-pqt-` cards conforming to QP callout schema (128 PQT + 128 TRD).
- [x] Define and implement automated stage gates for Track 0 and Track 6 in `tools/qp/markets.py` and `./qp markets gates`.

### Phase 7: Options Volatility Desk Simulator & Options Track
- [x] Implement options pricing, analytical Greeks, and surface model in `tools/qp/lab/opt_desk.py`.
- [x] Build multi-scenario volatility desk simulator (gamma scalping, earnings crush, skew steepening, dispersion).
- [x] Add unit tests validating Greeks against finite differences and attribution consistency in `tools/tests/test_opt_desk.py`.
- [x] Author 4 advanced options volatility concept notes with 128 cards (`mkt-opt-001` through `128`) cross-linking `05-Derivatives-and-Volatility`.
- [x] Expose Options Desk in Trading Lab catalog and engine registry.

### Phase 8: Chart Replay, Calibration Lab, & Technical Analysis
- [x] Implement blind chart replay engine `tools/qp/lab/replay_chart.py` with analytical oracle, multi-regime simulation, and Murphy Brier score decomposition.
- [x] Add automated unit tests verifying Brier score mathematics, log loss, calibration error, and determinism in `tools/tests/test_replay_chart.py`.
- [x] Author 8 Track 5 (Technical Analysis) concept notes with academic evidence grades and peer-reviewed citations.
- [x] Author 256 `mkt-ta-` cards conforming to QP callout schema (`mkt-ta-001` through `mkt-ta-256`).
- [x] Expose `replay_chart` engine in Trading Lab CLI and catalog.

### Phase 9: Backtest Overfitting Trap & Systematic Research
- [x] Implement overfitting engine `tools/qp/lab/overfit_trap.py` with Deflated Sharpe Ratio (DSR), Harvey-Liu haircuts, and CSCV PBO.
- [x] Author systematic strategy research curriculum cross-linking `09-Alpha-Research-and-Portfolio` across 8 comprehensive concept notes.
- [x] Author 256 `mkt-sys-` cards conforming to QP callout schema (`mkt-sys-001` through `mkt-sys-256`).
- [x] Expose `overfit_trap` engine in Trading Lab CLI and test suite (`tools/tests/test_overfit_trap.py`).

### Phase 10: Trade Journal Analytics & Capital Gate
- [x] Implement journal analytics engine `tools/qp/lab/journal_stats.py` (expectancy by setup, adherence gap, tilt detection, MAE/MFE forensics).
- [x] Wire immutable trade planning and logging API in `tools/qp/server.py` (`/api/journal/stats`, `/api/journal/log`, `/api/lab/catalog`, `/api/lab/run`).
- [x] Implement Capital Gate validator enforcing paper sample size, risk limits, and pre-registered expectancy in `tools/qp/markets.py` and `./qp markets gates`.
- [x] Add automated unit tests for journal analytics and Capital Gate verification in `tools/tests/test_journal_stats.py`.

### Phase 11: Fundamental Analysis, Valuation, & Value Investing
- [x] Author Track 1 (Fundamental Analysis), Track 2 (Valuation), Track 3 (Value Investing), and Track 4 (Portfolio) notes.
- [x] Build hidden-answer drill banks in `30 Drills/` (statement forensics, valuation rebuilds, blind company memos).
- [x] Author 1000+ cards across `mkt-fa-`, `mkt-val-`, `mkt-vi-`, and `mkt-pf-`.
- [x] Implement stage gates for fundamental analysis and valuation.

### Phase 12: Multi-Asset Class Modules & Portfolio Manager Lab
- [x] Implement synthetic multi-asset portfolio allocator and risk parity simulator `tools/qp/lab/port_alloc.py`.
- [x] Implement futures term structure, cost-of-carry, roll yield, and basis arbitrage desk `tools/qp/lab/fut_desk.py`.
- [x] Author specialized asset-class notes (India equities & F&O, Rates curve trading, Commodities term structure, Crypto perps).
- [x] Author 128 flashcards across `mkt-ind-`, `mkt-mac-`, `mkt-cmd-`, and `mkt-cry-`.
- [x] Wire `fut_desk` and `port_alloc` into Trading Lab catalog and automated unit test suite (`tools/tests/test_fut_port.py`).

### Phase 13: Event Case Files, Market History, Psychology, & Regulation
- [ ] Implement structured event simulation engine `tools/qp/lab/events.py`.
- [ ] Author 10 historical market crisis case files with primary-source citations and dates.
- [ ] Author trading psychology, decision making, regulatory, and career curriculum notes.
- [ ] Build web UI for historical event replays and pre-mortem analysis.

### Phase 14: Mastery Engine, Study Board, & Persona Planner
- [ ] Implement holistic mastery scoring formula in `tools/qp/markets.py`.
- [ ] Implement Study Board writer script `16-Trading-and-Investing/scripts/mastery.py`.
- [ ] Implement persona-aware study planner in `tools/qp/planner.py` sized to user weekly hours.
- [ ] Build unified Mastery Dashboard in `MARKETS_HUB.md` and QP web app.
- [ ] Execute comprehensive end-to-end verification, browser testing, and final audit.

---

## 4. Verification Protocol

Run the following suite after every phase before proposing or merging changes:

```sh
# 1. Platform unit tests and test suite
python3 -m unittest discover -s tools/tests -t .

# 2. Vault and syllabus conventions check
./qp check

# 3. Market content and quality gate (active from Phase 1)
python3 16-Trading-and-Investing/scripts/verify_markets.py

# 4. Code quality and formatting
ruff check . && ruff format --check .

# 5. Secret scanning
tools/scan-secrets.sh
```

Every delivery must pass all five checks cleanly with zero warnings or errors.
All commits must follow repository standards and ship exclusively through the `no-mistakes` gate pipeline.
