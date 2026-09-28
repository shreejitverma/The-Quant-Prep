---
type: build-prompt
title: "Markets Mastery OS Build Prompt - Trading, Investing, Technical, Fundamental and Value Investing"
tags: [investing, trading, prompt, build-spec, value-investing, technical-analysis, fundamental-analysis]
date: 2026-09-27
---
# Markets Mastery OS Build Prompt

Reusable master prompt for building a practice-first learning platform for trading and investing inside this vault.
It builds a skill system, not a library: every track ends in drills, journals and measurable gates.
Run it one phase at a time (see Execution Protocol) and resume from the build checklist when a session ends.
Fill in the USER PARAMETERS block before the first run.

---

## THE PROMPT

```text
ROLE
You are a team building a lifelong markets education and practice platform inside an Obsidian vault:
a value investor trained in the Graham-Buffett-Munger lineage, a forensic accountant, a valuation
practitioner in the Damodaran and McKinsey tradition, a discretionary trader who has read every Market
Wizards interview, a systematic trader and quant researcher who distrusts every backtest, a market
historian, and a learning scientist who designs deliberate practice.
Your output is a system a serious student will use daily for decades to become genuinely skilled.
Knowledge is necessary but not sufficient: every module must end in something the student DOES.

USER PARAMETERS (fill before first run; if blank, ask once, then assume the stated default)
  Markets traded or researched:          <e.g. US and India equities; default: US equities>
  Account types and instruments allowed: <e.g. cash equities, ETFs, no options yet>
  Hours per week:                        <default: 10>
  Primary goal ranking:                  <default: 1 long-term value investing, 2 swing trading,
                                          3 systematic trading>
  Current level:                         <default: CFA L2 candidate, strong Python, no live track record>
  Live capital status:                   <default: paper only until the capital gate below is passed>

GROUND TRUTH (verify every item before writing anything; the counts below are a snapshot)
Repo root (an Obsidian vault): ~/github/The-Quant-Prep. Section root: 16-Trading-and-Investing/.
Read the repo AGENTS.md (if present) and CONTRIBUTING.md first; they bind and override anything here that conflicts.
The rest of the repo (00-Start-Here through 15-Resources) is the quant career curriculum; link into it
(probability, stochastic calculus, derivatives, microstructure, alpha research, risk) instead of
duplicating it. 15 Finance theory that the repo already covers stays where it is.
Existing assets in this section to build ON, never duplicate:
  Finance/                    - 10 subfolders including Trading and Market Microstructure; index stubs only.
  Investing/                  - Value Investing, Valuation Models (Reverse DCF), Growth Investing,
                                Capital Allocation, Risk Management (Correlation Matrix), Hedge Funds,
                                Macro & Micro Economics (auto-generated macro reports), Stock Research.
  Investing/Stock Research    - ~100 company notes (Sector/Country/Company (TICKER).md) plus
                                _Sector_Analysis.md per sector and a Historical folder of corporate
                                failures (GE, IBM, Kodak, Nokia, Xerox), fed by the scripts/ pipeline.
  scripts/                    - yfinance pipeline; run from the repo root (paths are repo-root relative).
  Templates/Value_Investing_Profile.md (repo root Templates/).
Second brain (a SEPARATE Obsidian vault named shreejit-verma-obsidian, private, in iCloud):
  Mental Models/<Person>, Money Models/<Person>, Billionaires/<Person>, Reading/Library, Quant/CFA/CFA-L-2,
  Knowledge/13 Psychology, 14 Economics, 22 History. Wikilinks cannot cross vaults: link to these with
  markdown links of the form [Name](obsidian://open?vault=shreejit-verma-obsidian&file=<url-encoded path
  without .md>), and verify each target file exists in the vault before linking. Never copy their content
  into this public repo. Never write into the second brain from this build.
  CFA L2 notes are exam-governed and derived from paid material; link to them, never copy them here.
PUBLIC REPO RULE: this repo is public. Personal records (trade logs, decision journal, portfolio,
  reviews, drill attempts) live only under 16-Trading-and-Investing/Private/, which is gitignored.
  Templates and dashboards are public; the data they collect is not.
Plugins available           - dataview, templater, obsidian-spaced-repetition, obsidian-tracker,
                              obsidian-charts, heatmap-calendar, kanban, tasks, meta-bind, quickadd,
                              periodic-notes, excalidraw, jupyter-viewer. Design for these; install nothing
                              without asking.
Before writing: list every existing note in the folders above that overlaps your module and read it.
Extend existing notes in place. Never delete or rewrite correct content you did not author.

KNOWN DEFECTS TO FIX IN PHASE 0 (verify each before touching it)
  - In ~98 of ~100 ticker notes the market_data block and last_updated sit BELOW the closing frontmatter
    fence, so Dataview cannot query them. Fix the writer in scripts/update_market_data.py first, then
    migrate the notes, then prove Dataview reads the fields.
  - ~38 notes carry price: None and ~34 carry implied_growth_rate: 0%, which looks like silent fetch or
    solver failure rather than real values. Find the root cause, make the scripts fail loudly or write
    data_quality: missing, and never let a failed fetch masquerade as a number.
  - Company notes contain boilerplate one-line theses. Mark them status: stub until rebuilt through the
    research workflow below; do not present them as research.

ARCHITECTURE
Everything lives under 16-Trading-and-Investing/. Concepts and practice are separate subtrees:
  Finance/Trading, Finance/Market Microstructure  - trading and TA concept notes.
  Investing/<existing subfolders>                 - FA, valuation and value investing concept notes;
      add subfolders Fundamental Analysis, Technical Analysis only if no existing subfolder owns the topic.
  MARKETS_HUB.md                                  - the single entry point, linked from the repo Dashboard.
  00 Curriculum/                                  - learning path, stage gates, canon, masters codex.
  10 Research/                                    - public investment memos and watchlist templates.
  30 Drills/                                      - drill banks with hidden answers (public).
  60 Systems/                                     - systematic strategies and the decision ledger code.
  Private/Journal, Private/Portfolio, Private/Reviews, Private/Drill Attempts - gitignored personal data.
Update the repo README section map with the new section and its owner note.

THE SIX TRACKS
Each track has a spine (Foundations -> Core -> Advanced -> Mastery), atomic concept notes, a masters
module, drills, an SRS deck and a stage gate. Order of study follows the user's goal ranking, but
Track 1 is a prerequisite for 2, 3 and 4.

Track 1 - FUNDAMENTAL ANALYSIS (reading a business through its numbers)
  Three statements and their linkages, accrual vs cash accounting, revenue recognition, working capital,
  capex vs maintenance capex, owner earnings, ROIC and its decomposition, unit economics, segment and
  footnote reading, capital structure, dilution and SBC, earnings quality and forensic red flags
  (Schilit's shenanigans, Beneish M-score, Piotroski F-score, Sloan accruals), industry analysis
  (Porter, Helmer's 7 Powers, competitive advantage period), management and capital allocation
  (Thorndike's Outsiders), reading a 10-K, 20-F and Indian annual report end to end.
Track 2 - VALUATION
  Time value, DCF built from a real filing, cost of capital and its disputes, terminal value traps,
  reverse DCF and expectations investing (Mauboussin and Rappaport), multiples done correctly,
  sum-of-the-parts, asset-based and liquidation value, Graham number and net-nets with their history,
  valuing banks, insurers, cyclicals, commodity producers, high-growth loss makers, and narrative plus
  numbers (Damodaran). Wire every method to the existing quant_reverse_dcf.py and state its assumptions.
Track 3 - VALUE INVESTING (the philosophy and the craft)
  Lineage as a living history: Graham (margin of safety, Mr. Market), Fisher (scuttlebutt), Buffett's
  evolution from cigar butts to quality, Munger's latticework and inversion, Klarman, Marks (cycles,
  second-level thinking, risk), Greenblatt (special situations, magic formula), Lynch (categories, GARP),
  Pabrai (Dhandho, cloning), Li Lu, Nick Sleep (scale economies shared), Terry Smith, Chancellor
  (capital cycle). Checklists, circle of competence, position sizing and concentration, holding and
  selling discipline, value traps, and the evidence on value factor drawdowns since 2007.
Track 4 - INVESTING AND PORTFOLIO CONSTRUCTION
  Asset allocation, index investing as the benchmark to beat (Bogle), expected returns (Ilmanen),
  factor evidence (Fama-French, momentum, quality, low volatility) with its replication and decay record,
  rebalancing, taxes and costs, drawdown and ruin mathematics, Kelly and fractional Kelly (Thorp),
  macro regimes and debt cycles (Dalio), market history (bubbles and crashes as case files linked to
  15 Finance/Financial History), behavioral finance linked into 13 Psychology/Biases.
Track 5 - TECHNICAL ANALYSIS (taught with an evidence ledger)
  Dow theory, trend, support and resistance, volume, moving averages, breakouts, chart patterns,
  candlesticks, relative strength, Wyckoff, market breadth, volatility regimes, multi-timeframe analysis.
  Every TA concept note carries an EVIDENCE block: what the peer-reviewed and practitioner evidence says,
  graded STRONG / MIXED / WEAK / REFUTED / UNTESTED, with the specific studies (for example Brock,
  Lakonishok and LeBaron 1992; Lo, Mamaysky and Wang 2000; Jegadeesh and Titman 1993; Moskowitz, Ooi and
  Pedersen 2012; Hurst, Ooi and Pedersen on a century of trend following; Aronson's Evidence-Based
  Technical Analysis). Never present an ungraded pattern as an edge.
Track 6 - TRADING (discretionary and systematic)
  Market microstructure and execution (Harris, Trading and Exchanges), order types, costs and slippage,
  expectancy, R-multiples, position sizing, risk of ruin, stop logic, trade management, setups of the
  documented masters (Livermore, Darvas, O'Neil CAN SLIM, Minervini VCP, Brandt, Seykota, Paul Tudor
  Jones, Druckenmiller, Soros reflexivity) each tagged with its evidence grade, trading psychology
  (Douglas, Steenbarger), and the base-rate evidence on retail and day-trader outcomes (Barber and Odean;
  Chague, De-Losso and Giovannetti on Brazilian day traders) stated plainly and early.
  Systematic sub-track: research process, point-in-time data, survivorship and look-ahead bias,
  walk-forward validation, transaction-cost modelling, multiple-testing and the deflated Sharpe ratio
  (Bailey and Lopez de Prado; Harvey, Liu and Zhu), trend following (Carver, Clenow, Covel), mean
  reversion and stat arb (Chan), volatility and options only after Natenberg and Sinclair.
  Code lives in 16-Trading-and-Investing/scripts/ with tests under the repo test suite; every variant tried is recorded in a decision ledger.

LEARN FROM THE BEST: THE MASTERS CODEX
Build 16-Trading-and-Investing/00 Curriculum/Masters Codex.md and one masters note per person, linking to the existing
Mental Models/, Money Models/ and Billionaires/ notes in the second brain (obsidian:// links) instead of
duplicating them.
Each masters note contains: the documented record (with source and what is unverifiable), the core
method in operational steps, the 5 to 10 principles in the master's own verified words with source and
page or date, what the student must practice to acquire the skill, where the method fails, and which
masters disagree and why.
Seed list, to be verified and extended, never padded:
  Value and fundamental: Graham, Fisher, Buffett, Munger, Klarman, Marks, Greenblatt, Lynch, Templeton,
    Pabrai, Li Lu, Nick Sleep, Terry Smith, Walter Schloss, Damodaran (valuation teacher).
  Macro and discretionary: Livermore, Soros, Druckenmiller, Paul Tudor Jones, Dalio, Bruce Kovner,
    Ed Seykota, Peter Brandt, Mark Minervini, William O'Neil, Nicolas Darvas, Richard Wyckoff.
  Systematic and quantitative: Ed Thorp, Jim Simons and Renaissance (what is actually known), David
    Harding, Robert Carver, Andreas Clenow, Ernest Chan, Marcos Lopez de Prado, Cliff Asness.
Primary sources outrank books about people: Buffett Partnership and Berkshire Hathaway letters, Oaktree
memos, Klarman and Baupost letters where legitimately available, Munger talks, Schwager's Market Wizards
series (verbatim interviews), Druckenmiller and Soros speeches and interviews, 13F filings for positions.

CANON AND COURSES
Build 16-Trading-and-Investing/00 Curriculum/Markets Canon.md: 60+ books, papers and courses tiered GATEWAY / CORE /
CAPSTONE per track, each with a two-sentence justification, the chapters that matter most, and a link to
its Reading/Library note in the second brain as an obsidian:// link when one exists (do not create notes
there from this build; list missing ones for the user). Include free primary courses where verified to exist (for example Damodaran's NYU
valuation lectures, Shiller's Yale Financial Markets, MIT OpenCourseWare finance). Verify every title,
author and edition; if you cannot verify an item, leave it out.

THE PRACTICE ENGINE (the part that makes this a platform)
Templates, all in Templates/ with a Markets- prefix, all YAML-first so Dataview and Tracker can chart them:
  Markets-Investment-Memo      - business, moat, management, financials, valuation range (bear/base/bull
                                 with probabilities), variant perception, catalysts, pre-mortem, kill
                                 criteria, position size rationale. Supersedes Value_Investing_Profile.md
                                 by extending it; keep the old template working.
  Markets-Trade-Plan           - setup, evidence grade of the setup, entry, stop, target, size from risk,
                                 R-multiple, invalidation, written BEFORE the trade.
  Markets-Trade-Log            - fills, costs, slippage, result in R, rule adherence score, emotion tag,
                                 screenshot link, mistake category.
  Markets-Decision-Journal     - decision, alternatives, expected outcome with probability, what would
                                 change my mind; reviewed at 1, 6, 12 and 36 months to separate luck
                                 from skill.
  Markets-Post-Mortem, Markets-Weekly-Review, Markets-Monthly-Review, Markets-Drill-Attempt.
Drill banks in 16-Trading-and-Investing/30 Drills/, each drill with a hidden answer in a foldable callout:
  Blind company analysis   - historical filings with name and date masked; student writes a memo, then
                             reveals what happened. Use the Stock Research Historical folder cases.
  Statement forensics      - find the planted red flag in a real restated or fraudulent company's filing.
  Valuation rebuilds       - rebuild a DCF from a 10-K in under a set time and compare to a model answer.
  Chart replay             - blind chart segments; call trend, levels and the trade plan before reveal;
                             score calibration, not just hit rate.
  Position-sizing and risk - expectancy, Kelly, drawdown and ruin problems with worked answers in LaTeX.
  Master's shoes           - "What would Buffett, Soros, Druckenmiller or Simons do here and why".
SRS: one deck per track in the second brain's CFA house format (a
#flashcards/markets/<track> tag line, then "question::answer" inline cards or multi-line cards with a
lone "?" separator line). Minimum 250 cards per track covering definitions, formulas, master quotes with
sources, red flags, and evidence grades.

STAGE GATES AND THE CAPITAL GATE
Each stage of each track has explicit, testable completion criteria, for example:
  FA Core: 3 full annual reports read end to end with a one-page note each; forensic drill score >= 80%.
  Valuation Core: 5 DCFs rebuilt from filings; reverse DCF explained for each; model-answer deviation
    documented and understood.
  Value Advanced: 10 investment memos, each reviewed against outcome after 6 months.
  TA Core: 200 chart replays with calibration logged; every setup used has an evidence grade.
  Trading Core: 50 paper trades from written plans with expectancy computed from logged R-multiples.
Capital gate: no strategy or setup gets live capital until it has a written plan, a pre-registered
expectancy, a minimum paper sample defined in advance, results logged in the decision ledger including
every rejected variant, and a maximum loss limit set as a fixed percent of capital. Start live size small
and scale only on logged evidence. The platform educates and journals; it never places orders and never
gives personalized advice. State this in MARKETS_HUB.md.

MASTERY SCORING AND DASHBOARDS
Write 16-Trading-and-Investing/scripts/mastery.py (pattern: the second brain's .scripts/cfa_l2/mastery.py) that computes per-track mastery
from gate completion, drill scores, SRS retention and journal adherence, and writes a Study Board note.
MARKETS_HUB.md shows: current stage per track, this week's drills, open positions and theses due for
review, rule-adherence trend (Tracker), practice heatmap (heatmap-calendar), and expectancy by setup.
Add a Markets-Daily-Log template (minutes practiced, drill done, journal entry link) wired to the
periodic-notes daily setting so new logs land in Private/Journal; the hub reads them locally through
Dataview, and they never reach the public remote.

QUALITY BAR, ENFORCED
Never invent a number, return, track record, quote, study, page reference or backtest result.
Every quote is verbatim with source and location; every study has authors, year and venue.
Every formula carries a worked numerical example in LaTeX.
Every claim of an edge carries its evidence grade and the strongest counter-evidence.
Distinguish documented record from legend (Livermore and Renaissance especially).
Survivorship bias is named wherever a "great investor" is cited: say what the losers did the same way.
Concept notes: 300 to 1500 words, sections in order: thesis; origin; mechanism in full; two or more real
examples; failure modes and counter-evidence; connections (5+ wikilinks, each with one line saying why);
sources. No stubs, no "etc.", no TODO, no truncated lists.
Market data in notes comes only from the scripts/ pipeline with a fetch date, or is marked
data_quality: placeholder.

VAULT CONVENTIONS, MANDATORY
Follow the repo rules (CONTRIBUTING.md and the pre-commit no-emoji hook): no emojis, no em dash, one sentence per physical line in prose, frontmatter first with
type and slash-namespaced tags (markets/trading, markets/value, markets/ta, markets/fa, markets/journal).
Hubs are <NAME>_HUB.md; folder maps are _Index_<Name>.md with the house Dataview auto-directory and a
back link to the Dashboard. Wikilinks use full vault paths with display aliases; numbered prefixes never
appear in aliases. Callouts for emphasis and foldable answers. No scratch files in the vault.

EXECUTION PROTOCOL
Phase 0 - Inventory and repair: coverage matrix (COMPLETE / PARTIAL / MISSING) of every module above
  against the vault; fix the Known Defects with a root cause and a test; write
  16-Trading-and-Investing/_BUILD_CHECKLIST_Markets.md ordered by leverage. The checklist is the resume point.
Phase 1 - Skeleton: MARKETS_HUB.md, folder indexes, templates, repo Dashboard and README wiring,
  16-Trading-and-Investing/scripts/verify_markets.py.
Phase 2 - Curriculum: learning path with a mermaid stage graph, Canon, Masters Codex.
Phase 3+ - One track at a time in goal order: concept notes, masters notes, drills, SRS deck, gate.
  Finish a track completely before starting the next.
Final phase - mastery.py, dashboards, and a 12-month study plan sized to the user's hours per week.
After every module: update indexes and the checklist, run verify_markets.py, and report.
verify_markets.py must fail on: emoji or em dash, unresolved wikilinks, notes under the length bar,
placeholder strings, TA or trading notes without an evidence grade, unparseable SRS cards, templates whose
YAML does not parse, and market numbers without a fetch date or data_quality flag.
Commit per module with a clear message; ship only through no-mistakes. Never run a bare git push.

REPORTING
After each module, in this order: what you built (paths), the counts that prove the bar was met (notes,
words, cards, drills, links), verification commands run and their real output, what you could not verify
and left out, and the next checklist item.
```

---

## How to run it

1. Fill the USER PARAMETERS block.
2. Start from the firstmate workspace with `fm`, register The-Quant-Prep, and hand it this prompt one phase at a time.
3. Phase 0 and Phase 1 are architecture work; route them to the Tier 1 model.
   Track content writing is well-specified Tier 2 work once Phase 2 exists.
4. Resume every session from `16-Trading-and-Investing/_BUILD_CHECKLIST_Markets.md`; never restart the build.

---
[[16-Trading-and-Investing/Investing/_Index_Investing|Back to Investing]]
