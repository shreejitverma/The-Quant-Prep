---
type: cfa-strategy
tags: [cfa/l2, cfa/strategy]
updated: 2026-08-26
---
# Distinction Strategy: what top-band Level II scripts do differently

Level II is a vignette exam.
The scored exam is 20 item sets of 4 questions (2 more are unscored trials), 88 questions in two sessions of 2 hours 12 minutes, so 3 minutes per question and 18 minutes per item set on average (V1 front matter; weights from CFA Institute).
Top-band candidates are not the ones who know the most; they are the ones who convert vignette data into the right computation fast and refuse the designed distractor.

## The three skills that separate the top band

1. Extraction speed: reading a 500-word vignette and pulling the six numbers that matter in under four minutes, ignoring the decoys.
   Practice: for every item set, write the input list before touching any question.
2. Automatic computation: the 60 or so formulas that recur are done without thinking, with the calculator in the right mode.
   Practice: the Slides decks and the 30-second flashcards; anything that takes more than 30 seconds to set up is not yet automatic.
3. Distractor recognition: every wrong option was built from a specific error (wrong sign, wrong period, before-tax vs after-tax, spot vs forward, IFRS vs US GAAP).
   Practice: in every self-test and practice problem, name the error behind each rejected option out loud; that is what the `Item-set patterns` sections train.

## Command verbs and what they cost

| Verb in the LOS | What the question does | Time budget |
|---|---|---|
| calculate, estimate | a number, three options that differ by one specific error | 3-4 minutes |
| interpret, evaluate, justify | a conclusion from numbers already in the vignette | 2-3 minutes |
| compare, contrast, distinguish | which of two statements is correct, often about two analysts' claims | 2 minutes |
| describe, explain, identify | recognition; should be under 90 seconds | 1-2 minutes |

Bank time on describe and identify questions to spend it on calculate questions.

## Per-topic playbook

| Topic | Weight | What is actually tested | Must be automatic | Traps that recur |
|---|---|---|---|---|
| Quant | 5-10% | reading regression output, choosing the right test, AR model diagnostics, ML concept classification | t and F tests from output, adjusted R squared, Durbin-Watson bounds, AR(1) mean reversion level, log-odds to odds | wrong degrees of freedom, treating serial correlation as heteroskedasticity, unit root when the coefficient is near 1, interpreting a dummy coefficient as a slope |
| Economics | 5-10% | FX bid-offer and cross rates, forward premium, parity conditions, carry trade, growth accounting | cross-rate with bid-offer (multiply or divide, and which side), forward points to rate, covered interest parity, Solow growth decomposition | using the wrong side of the quote, points scaled wrongly, mixing up uncovered parity and forward rate parity, labor productivity vs TFP |
| FSA | 10-15% | equity method vs consolidation vs fair value, pension cost components, translation vs remeasurement, bank ratios, quality flags | equity method carrying value, goodwill (full vs partial), pension expense under IFRS and US GAAP, current-rate vs temporal method effects on ratios, CAMELS | which method applies at which ownership level, where remeasurement gains go (income statement) vs translation (OCI), net pension asset limit, treating a one-off as recurring |
| Corporate Issuers | 5-10% | dividend policy signals, repurchase EPS and book value effects, cost of capital build-ups, restructuring valuation | EPS after buyback with borrowed funds, effective tax rate on dividends under imputation, ERP methods, WACC for a private target, synergy value | buyback funded by debt with after-tax cost above earnings yield reduces EPS, double taxation vs imputation arithmetic, using book weights instead of market |
| Equity | 10-15% | DDM variants, FCFF and FCFE from any starting point, multiples (justified P/E, P/B, EV/EBITDA), residual income, private company discounts | Gordon growth, H-model, two-stage, FCFF from EBIT and from NI, FCFE from FCFF, justified leading and trailing P/E, RI = NI - equity charge, DLOC and DLOM chained | trailing vs leading multiple, dividends vs FCFE for a firm changing leverage, forgetting working capital and FCInv, RI continuing value persistence factor, applying discounts additively instead of multiplicatively |
| Fixed Income | 10-15% | spot and forward rates, binomial trees, callable and putable valuation, OAS, effective duration, credit models, CDS pricing | forward from spots, bootstrapping, backward induction on a tree, OAS interpretation with volatility, effective duration formula, expected loss = PD x LGD x exposure, CDS upfront from spread differential | volatility raises call value so callable price falls and OAS falls, using yield instead of spot, key rate durations for callables near the call price, CDS protection buyer gains when spread widens |
| Derivatives | 5-10% | forward and futures pricing, FRA settlement, swap rates from spots, binomial option values, BSM inputs, Greeks, delta hedging | forward price with carry, FRA payoff discounted, swap fixed rate from discount factors, risk-neutral probability, put-call parity, hedge ratio | discounting FRA settlement at the wrong rate, using the coupon instead of the spot curve for swap rates, sign of the delta hedge, Black vs BSM for futures options |
| Alternatives | 5-10% | commodity term structure and roll return, real estate valuation approaches, REIT NAV, hedge fund strategies and metrics | total return decomposition (price, roll, collateral), direct cap rate, DCF for property, NAV per share, funds-of-funds fee layers | backwardation vs contango roll sign, cap rate vs discount rate, AFFO adjustments, hedge fund returns net of both fee layers |
| Portfolio Management | 10-15% | business cycle and asset pricing, active risk decomposition, information ratio, fundamental law, ETF mechanics, multifactor models, VaR, backtesting | IR = IC x sqrt(BR) x TC, Sharpe of the combined portfolio, active return and active risk, VaR under three methods, factor return attribution, tracking error sources | confusing information ratio and Sharpe, forgetting the transfer coefficient, VaR sign and horizon scaling, creation basket vs ETF price arbitrage direction, look-ahead bias |
| Ethics | 10-15% | which standard is violated, by whom, and what would have prevented it; ROS; GIPS basics if present | the seven Standards and every sub-standard boundary, the Professional Conduct Program mechanics, disclosure vs prohibition | III(A) loyalty vs VI(A) disclosure of conflicts, I(B) independence vs VI(B) priority of transactions, II(A) material nonpublic vs II(B) manipulation, "reasonable basis" vs "suitability", assuming a violation when the standard only requires disclosure |

## Scoring targets

- Mock 6 at 85 percent or higher across both sessions with no topic below 70 percent.
- Every item set attempted in under 18 minutes; no item set abandoned.
- Zero unresolved errors older than 7 days in the last three weeks.
- Every LM note's teach-back written; empty teach-backs cap mastery at 60 by design.

## Guessing and time policy

- Never leave a question blank; there is no penalty for wrong answers.
- If a calculate question exceeds 5 minutes, pick the option closest to a sanity estimate, flag it, and move on; return only after the session's last item set.
- Answer the qualitative questions in an item set first if the vignette is long; they load the context for the calculations.
- Read the question stem before the vignette for the second and later questions in a set; the vignette does not change.

## Weekly cadence that supports these skills

- Pass 1: one module at a time with the full note, teach-back, and one item set; this builds the formula base and the SRS decks.
- Pass 2: only mixed-topic timed item sets; this builds extraction speed and distractor recognition.
- Pass 3: mocks at full timing on alternating days; this builds endurance and reveals pacing problems, which the error log turns into rules.

Related: [[Study-Plan]], [[Calculator-Playbook]], [[Exam-Day-Playbook]], [[17-CFA/CFA-L-2/CFA_L2_HUB|Hub]].
