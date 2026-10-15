---
type: cfa-itemset
topic: "Ethical and Professional Standards"
topic_code: "10"
topic_slug: "10-Ethics"
lm: 3
title: "Brightwater Systematic: The Units Mismatch"
los: [los-10-03-a, los-10-03-b]
difficulty: 3
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/ethics]
---

# Brightwater Systematic: The Units Mismatch

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Brightwater Systematic is a quantitative equity manager in Toronto that runs its Global Equity Alpha (GEA) strategy for 18 pension and endowment clients.
Tove Lindqvist, CFA, is the lead researcher on GEA and reports to the chief investment officer, Marcus Adeyemi, CFA.
The GEA model has three components, summarized in Exhibit 1.

Exhibit 1: GEA model components and review practice

| Component | How often inputs or parameters change | How often reviewed and tested |
|---|---|---|
| Signal library | Re-estimated monthly | Monthly, component by component |
| Currency overlay | Hedge ratios reset quarterly | Quarterly |
| Portfolio optimizer | Receives new signals monthly | Every 24 months, including the only test of the full model |

In January, the signal library team began expressing return forecasts in basis points instead of percentages.
The optimizer was not changed and continued to read the forecasts as percentages, so several signals received weights far larger than intended.
Lindqvist confirmed the signal library changes met Brightwater's written guidelines, which require only component-level testing between the 24-month reviews.

In the second week of April, Lindqvist traced three months of GEA underperformance to the units mismatch.
She estimated the cost of leaving it uncorrected, as shown in Exhibit 2.

Exhibit 2: Lindqvist's estimate of the uncorrected error

| Item | Value |
|---|---|
| Assets in GEA accounts | USD 2.4 billion |
| Estimated performance drag while uncorrected | 3.5 basis points per week |
| Weeks until the next scheduled model release | 10 |
| GEA management fee | 45 basis points per year |
| Time needed to correct and test the fix | 2 days |

Lindqvist told Adeyemi the fix could be tested and released within two days.
Adeyemi replied: "A mid-quarter release will draw questions from consultants. Switch off the currency overlay so the positions look less extreme, and put the fix in the scheduled release in 10 weeks."
Lindqvist switched off the overlay as instructed and scheduled the fix for the release.

In late April, Adeyemi sent all GEA clients a letter stating: "First-quarter underperformance reflected unusually sharp currency moves. We have suspended our currency overlay while volatility persists."
Currency markets had been more volatile than usual during the quarter.

In May, Brightwater's marketing team prepared a GEA pitch book for prospective clients.
It shows the calendar-year returns in Exhibit 3 and a single headline figure: "GEA ten-year annualized return: 9.79%."
A footnote in small type reads: "Figures for 2016 to 2019 include model results."

Exhibit 3: GEA calendar-year returns, net of fees (%)

| Year | Return | Basis |
|---|---|---|
| 2016 | 14.8 | Backtested |
| 2017 | 19.6 | Backtested |
| 2018 | -1.2 | Backtested |
| 2019 | 22.4 | Backtested |
| 2020 | 9.1 | Actual |
| 2021 | 17.3 | Actual |
| 2022 | -12.6 | Actual |
| 2023 | 15.2 | Actual |
| 2024 | 11.8 | Actual |
| 2025 | 6.4 | Actual |

The pitch book does not show the backtested and actual periods separately, and the column labeled "Basis" appears only in Brightwater's internal version of Exhibit 3.

## Questions

1. The estimated cost to GEA clients of waiting for the scheduled release, and the most accurate evaluation of Lindqvist's decision to wait, are: (LOS: los-10-03-a)
   - A. USD 8.4 million; she violates Standard III(A) Loyalty, Prudence, and Care.
   - B. USD 0.84 million, which is immaterial for USD 2.4 billion of assets, so she does not violate the Code and Standards.
   - C. USD 8.4 million; she does not violate the Code and Standards, because she switched off the currency overlay as her supervisor ordered.
2. With respect to the GEA review practice in Exhibit 1, Lindqvist most likely: (LOS: los-10-03-b)
   - A. complies with Standard V(A) Diligence and Reasonable Basis, because every component is tested at least as often as its own inputs change, as Brightwater's guidelines require.
   - B. violates Standard V(A), because the optimizer and the full model, which use inputs that change monthly, are tested only every 24 months.
   - C. violates Standard V(A), because the currency overlay should be reviewed monthly, like the signal library.
3. Adeyemi's April letter to GEA clients most likely: (LOS: los-10-03-b)
   - A. does not violate the Code and Standards, because currency markets were in fact unusually volatile during the quarter.
   - B. violates Standard V(B) Communication with Clients and Prospective Clients only, because suspending the overlay is a process change that must be disclosed in advance.
   - C. violates Standard I(C) Misrepresentation, because he attributes the underperformance to currency moves when he knows the cause is the model error.
4. With respect to Standard III(D) Performance Presentation, the pitch book's headline figure most likely: (LOS: los-10-03-a)
   - A. complies, because the footnote discloses that the figures include model results.
   - B. violates the Standard; the annualized return on GEA's actual record alone is about 7.38%.
   - C. violates the Standard; the annualized return on GEA's actual record alone is about 7.87%.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Weekly drag in dollars $= 2.4 \text{ billion} \times 0.00035 = 0.84$ million.
> Cost of waiting 10 weeks $= 0.84 \times 10 = 8.4$ million, against a fix that takes 2 days.
> Standard III(A) requires members to act for the benefit of clients; leaving a known, correctable error in client portfolios for 10 weeks to avoid consultant questions puts the firm's image ahead of clients, and a supervisor's instruction does not excuse it (V10 p.246, p.247).
> Switching off the overlay changes how the positions look but does not correct the mismatch.
> B is wrong because it counts one week of drag instead of 10, and in any case the size of a known harm relative to assets is not a defense for leaving it in place.
> C is wrong because following an order does not discharge the duty to clients, and the overlay switch masks rather than fixes the error.
> The management fee and the two-day repair time are not inputs to the cost; the repair time shows only that the fix was available at once.
> 2. **B.** Standard V(A) requires understanding and testing a model at a frequency that matches how it changes, including how its components work together (V10 p.245, p.246).
> The optimizer receives new signals every month, yet the optimizer and the full model are tested only every 24 months, which is exactly where the units mismatch between the signal library and the optimizer went undetected for three months.
> Meeting Brightwater's written guidelines does not cap what the Standard requires.
> A is wrong because component-by-component testing misses errors in the linkage between components, and firm guidelines do not set the Standard's bar.
> C is wrong because the overlay's hedge ratios change quarterly and are tested quarterly, which matches its change frequency.
> 3. **C.** Adeyemi knows the underperformance comes from the units mismatch, yet he tells clients it reflects currency moves and presents the overlay suspension as a response to volatility, a knowing misrepresentation under Standard I(C) (V10 p.247).
> A is wrong because a statement built from a true fact (currency volatility) is still misleading when it is offered as the cause and the real, known cause is concealed.
> B is wrong because it names a lesser issue and misses the misstatement itself; the letter is a violation because what it says about the cause is false.
> 4. **B.** Standard III(D) permits backtested results only when they are clearly identified and kept distinct from actual results (V10 p.248).
> The 9.79% headline links four backtested years to six actual years into one figure, and a small-type footnote does not separate them.
> Actual record, 2020 to 2025: growth factor $= 1.091 \times 1.173 \times 0.874 \times 1.152 \times 1.118 \times 1.064 = 1.5327$.
> Annualized actual return $= 1.5327^{1/6} - 1 = 0.073771$, about 7.38%.
> For comparison, the backtested years alone annualize to 13.5149%, and linking all ten years gives $0.097914$, the 9.79% headline.
> A is wrong because a footnote that the figures "include model results" does not tell prospects which years are simulated or show actual and backtested results separately.
> C is wrong because it takes the arithmetic mean of the six actual returns, $47.2 / 6 = 7.8667\%$, instead of the geometric (annualized) return.

## Distractor design

1. B: one week of drag used instead of 10 (period error) plus a materiality rationalization; C: supervisor's order and the cosmetic overlay switch treated as a defense.
2. A: component-level testing and compliance with firm guidelines treated as meeting V(A); C: misread exhibit, a component whose testing already matches its change frequency flagged.
3. A: true fact used to mislead accepted as a defense (the character's own rationalization); B: lesser, wrong standard (V(B)) substituted for I(C).
4. A: small-type footnote mistaken for clear separation of backtested and actual results; C: arithmetic mean used instead of the geometric annualized return.
