---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 5
title: "Brightwater Balanced Fund: Sensitivities, Overlay, and Stress Design"
los: [los-09-05-f, los-09-05-g, los-09-05-h, los-09-05-i]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Brightwater Balanced Fund: Sensitivities, Overlay, and Stress Design

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Leona Abara, CFA, is the risk manager of the Brightwater Balanced Fund, a USD 300 million long-only multi-asset mutual fund.
She is preparing the quarterly risk report for the fund's chief investment officer, Paul Wren, and for its board.
The fund's equity sleeve holds USD 80 million of a broad equity index ETF, which has a delta of 1 with respect to the index.
The fixed-income sleeve includes a USD 45 million position in a single option-free corporate bond with a duration of 8.4, a convexity of 95, and a yield of 4.0%.
A small tactical sleeve holds call options on the same equity index.

Exhibit 1: Sensitivities of one tactical call option

| Measure | Value |
|---|---|
| Option price | 6.20 |
| Delta | 0.48 |
| Gamma | 0.035 |
| Vega (per 1 percentage point of implied volatility) | 0.14 |
| Theta (per calendar day) | -0.02 |

For the overnight sensitivity check, Abara assumes the index falls by 3.00 points and implied volatility rises by 2 percentage points.
For the fixed-income sleeve, she assumes the bond's yield falls by 75 basis points.

Wren considers the equity sleeve too aggressive for the fund's current mandate.
He asks Abara to bring the equity sleeve's delta down to 0.85 using listed three-month index options, while keeping the ETF position unchanged.
The exchange quotes the contracts in Exhibit 2, and Wren decides to use the puts.

Exhibit 2: Three-month index options available for the overlay

| Contract | Delta |
|---|---|
| Call, strike 5% out of the money | 0.60 |
| Put, strike 5% out of the money | -0.40 |

Abara and Wren then discuss the stress testing program.
Abara says: "For the 1987-crash historical scenario, we should reprice today's corporate bond using the yield and spread changes observed in that period, not the historical prices of a comparable bond."
Wren replies: "We already have delta, gamma, and vega for the tactical sleeve, so for the crash scenario the delta-gamma-vega approximation will be accurate enough, and we can skip full revaluation."

Abara also presents a hypothetical "stagflation shock" scenario in which equities fall 25%, yields rise 150 basis points, and the correlation between stocks and bonds turns strongly positive.
A board member, Nadia Ferro, asks whether such hypothetical scenarios have weaknesses that the board should keep in mind.

Finally, Ferro reads the sensitivity page of the report, which shows the bond's duration and the equity sleeve's beta, and states: "These sensitivities tell us everything the fund's 5% monthly VaR tells us, so the VaR page is redundant."

## Questions

1. Using Exhibit 1 and Abara's overnight assumptions, and ignoring time decay, the estimated new price of the tactical call is closest to: (LOS: los-09-05-g)
   - A. 4.76.
   - B. 4.92.
   - C. 5.20.
2. Using duration and convexity, the estimated return on the corporate bond under Abara's yield assumption is closest to: (LOS: los-09-05-g)
   - A. +5.81%.
   - B. +6.06%.
   - C. +6.30%.
3. To meet Wren's delta target, the fund should buy puts on an underlying notional amount closest to: (LOS: los-09-05-g)
   - A. USD 30.0 million.
   - B. USD 20.0 million.
   - C. USD 12.0 million.
4. Regarding the stress testing statements, which is correct? (LOS: los-09-05-h)
   - A. Abara's statement only.
   - B. Wren's statement only.
   - C. Both statements.
5. Which of the following is least likely a limitation of Abara's stagflation scenario? (LOS: los-09-05-i)
   - A. It is difficult to assign a probability to the scenario.
   - B. It relies on the assumption that returns are normally distributed.
   - C. Pressure to appear plausible may lead to movements that are too small.
6. The best response to Ferro's statement is that, compared with the fund's VaR, the duration and beta measures: (LOS: los-09-05-f)
   - A. are based on market returns from a particular historical period, as VaR is, so they add no new information.
   - B. capture simultaneous large moves in many risk factors, which VaR cannot.
   - C. describe the response to a change in a single factor but carry no information on the probability of that change, which VaR does.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Delta-gamma-vega approximation: $\Delta c \approx \Delta_c \Delta S + \tfrac{1}{2}\Gamma_c (\Delta S)^2 + \text{vega}(\Delta\sigma)$.
> Terms: $0.48 \times (-3.00) = -1.4400$; $\tfrac{1}{2}(0.035)(-3.00)^2 = 0.1575$; $0.14 \times 2 = 0.2800$; total $-1.0025$.
> New price $= 6.20 - 1.0025 = 5.1975$, about 5.20.
> A is wrong because it uses delta only: $6.20 - 1.44 = 4.76$.
> B is wrong because it omits vega: $6.20 - 1.44 + 0.1575 = 4.9175$, about 4.92; option values respond to volatility even when the underlying moves.
> Theta is a decoy; it plays no role in the overnight shock as specified.
> 2. **C.** $\Delta B/B \approx -D\,\Delta y/(1+y) + \tfrac{1}{2} C (\Delta y)^2/(1+y)^2$.
> Duration term: $-8.4 \times (-0.0075)/1.04 = +0.060577$.
> Convexity term: $\tfrac{1}{2}(95)(0.0075)^2/1.04^2 = 0.002470$.
> Total $= 0.060577 + 0.002470 = 0.063047$, about $+6.30\%$ (a gain of about USD 2.84 million on the USD 45 million position).
> A is wrong because it subtracts the convexity term: $0.060577 - 0.002470 = +5.81\%$; convexity always adds for an option-free bond because $(\Delta y)^2 > 0$.
> B is wrong because it stops at the duration term, $+6.06\%$, understating the gain from a large yield decline.
> 3. **A.** The ETF gives delta exposure of $1 \times 80 = \text{USD } 80$ million; the target is $0.85 \times 80 = 68$ million, so delta must fall by USD 12.0 million.
> Each USD 1 of put notional adds $-0.40$ of delta, so the notional required is $12.0/0.40 = \text{USD } 30.0$ million.
> B is wrong because it divides by the call delta from Exhibit 2, $12.0/0.60 = 20.0$, which would be the answer only for selling calls, not buying puts.
> C is wrong because it ignores delta and buys puts on USD 12.0 million of notional, which removes only $0.40 \times 12 = 4.8$ million of delta.
> 4. **A.** Abara is correct: a historical scenario on today's holdings should be driven by the historical yield and spread changes fed into valuation models, because historical prices of an instrument reflect its old maturity and characteristics.
> Wren is incorrect: delta-gamma-vega is a small-move approximation, and scenario-sized shocks require full revaluation of options.
> B is wrong because it accepts the approximation at crash scale; C is wrong because only Abara's statement holds.
> 5. **B.** Scenario measures do not assume any distribution, so reliance on normality is not one of their limitations (it is a limitation of parametric VaR).
> A is a genuine limitation: hypothetical scenarios are hard to calibrate and to assign a probability to.
> C is a genuine limitation: the need to appear plausible biases hypothetical scenarios toward moves that are too small.
> 6. **C.** Sensitivities such as duration and beta measure the response to a small change in one risk factor but say nothing about how likely that change is; VaR is the probabilistic measure, so the two are complements.
> A is wrong because sensitivities are applied to current rates and prices rather than drawn from a historical period; VaR and historical scenarios are the history-based measures.
> B is wrong because moving many factors at once by large amounts describes scenario analysis, not sensitivities.

## Distractor design

1. A: gamma and vega terms dropped (first-order only); B: vega term dropped (volatility exposure ignored).
2. A: convexity term sign reversed; B: duration only, second-order term omitted for a large move.
3. B: misread exhibit (call delta used for a put trade); C: delta ignored (notional set equal to the delta reduction).
4. B: small-move approximation accepted for a scenario-sized shock; C: both accepted without checking the full revaluation rule.
5. A and C: genuine limitations of hypothetical scenarios offered as the non-limitation (normality belongs to parametric VaR, not scenarios).
6. A: sensitivities misclassified as history-based measures; B: scenario-analysis property attributed to sensitivities.
