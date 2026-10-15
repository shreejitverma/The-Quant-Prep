---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 5
title: "Oakhurst Capital Advisors: Relative Risk and Sensitivity Scenarios"
los: [los-09-05-a, los-09-05-e, los-09-05-g, los-09-05-i]
difficulty: 3
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Oakhurst Capital Advisors: Relative Risk and Sensitivity Scenarios

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Mireille Fontaine, CFA, is head of investment risk at Oakhurst Capital Advisors, a long-only asset manager.
She reports to Rafael Okonkwo, the firm's chief investment officer.
Fontaine is preparing risk reports for two client accounts.

The first account is a USD 800 million global equity mandate for a university endowment, managed against a global equity index.
The endowment's investment committee wants a forward-looking estimate of how far the mandate could lag its benchmark over the next year.
Fontaine runs Oakhurst's risk model on the current holdings and obtains the annual estimates in Exhibit 1.
She assumes the expected active return is zero and that active returns are normally distributed.

Exhibit 1: Global equity mandate, forward-looking annual estimates

| Item | Value |
|---|---|
| Standard deviation of portfolio returns | 17.4% |
| Standard deviation of benchmark returns | 15.2% |
| Correlation between portfolio and benchmark returns | 0.95 |
| Realized tracking error, last three years | 2.10% |
| Expected return of the benchmark | 7.5% |

The committee chair asks for the mandate's 5% annual relative VaR in US dollars, together with a plain-language interpretation.

The second account is a USD 400 million balanced account for a family office.
It holds USD 240 million in an equity sleeve and USD 160 million in an option-free, investment-grade bond sleeve.
Fontaine applies the sensitivities in Exhibit 2 to a scenario the family office has asked about: the broad equity index falls 15% and bond yields rise by 80 basis points.

Exhibit 2: Balanced account sensitivities

| Sleeve | Market value (USD millions) | Sensitivity |
|---|---|---|
| Equity | 240 | Beta of 1.09 relative to the broad equity index |
| Bonds | 160 | Duration 6.8, convexity 58, yield 4.5% |

Oakhurst also manages two bond mandates that the family office is considering, a high-yield corporate mandate and an investment-grade corporate mandate.
The firm's report shows sensitivities for both, grouped into maturity buckets.
Fontaine and Okonkwo discuss what these sensitivity reports can and cannot show.

Fontaine: "Our reports place all bonds maturing between 7 and 15 years into one bucket and show a single duration for it; doing so implicitly assumes that yield changes are perfectly correlated within the bucket, so the report can hide exposure to changes in the shape of the curve inside that range."

Okonkwo: "The high-yield and investment-grade mandates both have a spread duration of 4.2, so the family office can treat them as carrying the same credit spread risk."

Okonkwo also notes that the family office's advisers are used to bank risk reports expressed in currency units at 99% confidence, and he asks Fontaine to explain Oakhurst's convention of reporting risk as a percentage of assets and relative to benchmarks.

## Questions

1. Based on Exhibit 1, the global equity mandate's annualized ex ante tracking error is closest to: (LOS: los-09-05-e)
   - A. 2.10%.
   - B. 2.20%.
   - C. 5.59%.
2. Using the sensitivities in Exhibit 2, the estimated change in the value of the balanced account under the family office's scenario is closest to: (LOS: los-09-05-g)
   - A. a loss of USD 44.1 million.
   - B. a loss of USD 47.3 million.
   - C. a loss of USD 47.6 million.
3. Regarding the statements on sensitivity reports, which is correct? (LOS: los-09-05-i)
   - A. Fontaine's statement only.
   - B. Okonkwo's statement only.
   - C. Both statements.
4. The response to the committee chair's request that Fontaine should give is closest to: (LOS: los-09-05-a)
   - A. USD 44.7 million; the mandate should be expected to underperform its benchmark by at least this amount in about one year in 20.
   - B. USD 73.8 million; this is the maximum amount by which the mandate should be expected to underperform its benchmark in 19 years out of 20.
   - C. USD 73.8 million; the mandate should be expected to underperform its benchmark by at least this amount in about one year in 20.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Ex ante tracking error is VaR machinery run on the portfolio minus the benchmark, so it is the standard deviation of the return difference, quoted as one standard deviation annualized.
> Terms: $0.174^2 = 0.030276$; $0.152^2 = 0.023104$; $2(0.95)(0.174)(0.152) = 0.050251$.
> Variance of active return $= 0.030276 + 0.023104 - 0.050251 = 0.003129$, so tracking error $= \sqrt{0.003129} = 0.055936$, about 5.59%.
> A is wrong because 2.10% is the realized (ex post) tracking error of the past holdings, which is backward-looking and does not reflect the current holdings the committee asked about.
> B is wrong because it subtracts the two volatilities, $17.4\% - 15.2\% = 2.20\%$, which would be correct only if the correlation were exactly 1.
> 2. **B.** Equity sleeve: $240 \times 1.09 \times (-0.15) = -39.2400$ million.
> Bond sleeve: duration term $-6.8 \times 0.0080/1.045 = -0.052057$; convexity term $\tfrac{1}{2}(58)(0.0080)^2/1.045^2 = 0.001700$; return $= -0.050358$, so the change is $160 \times (-0.050358) = -8.0573$ million.
> Total $= -39.2400 - 8.0573 = -47.2973$ million, a loss of about USD 47.3 million, or 11.82% of the account.
> A is wrong because it ignores beta and applies the index move directly to the equity sleeve: $240 \times (-0.15) - 8.0573 = -44.0573$ million.
> C is wrong because it omits the convexity term: $160 \times (-0.052057) = -8.3292$ million, total $-47.5692$ million; for a large yield change the positive convexity term should be included.
> 3. **A.** Fontaine is correct: aggregating sensitivities into a bucket assumes perfect correlation of the rate changes inside it, so broad buckets can conceal curve risk, which is the granularity trade-off of sensitivity reporting.
> Okonkwo is incorrect: sensitivity measures say nothing about how volatile the underlying factor is, and high-yield spreads are far more volatile than investment-grade spreads, so equal spread durations do not mean equal spread risk.
> B and C are wrong because each accepts Okonkwo's statement.
> 4. **C.** With zero expected active return, the 5% relative VaR is $1.65 \times 0.055936 = 0.092294$ of assets, and $0.092294 \times 800{,}000{,}000 = \text{USD } 73{,}835{,}094$, about USD 73.8 million.
> Like any VaR, it is a minimum shortfall at the stated frequency: underperformance of at least USD 73.8 million should occur in about 5% of years, or one year in 20, and the shortfall in those years can be larger.
> A is wrong because it reports the one standard deviation tracking error in dollars, $0.055936 \times 800\text{m} = \text{USD } 44.7$ million, which corresponds to a 16% relative VaR (about one year in six), not a 5% one.
> B is wrong because it reads VaR as a maximum; VaR places no upper bound on the shortfall.
> Expressing the result as 9.23% of assets and relative to the benchmark is the long-only convention Okonkwo asked about, because an unleveraged manager's key risk is underperformance rather than insolvency.

## Distractor design

1. A: misread exhibit (ex post realized tracking error used for the ex ante measure); B: wrong formula variant (volatility difference, which assumes a correlation of 1).
2. A: beta ignored (index move applied to the equity sleeve); C: convexity term omitted for a large yield change.
3. B: sensitivity treated as a risk measure that captures factor volatility; C: both statements accepted without checking the spread-volatility limitation.
4. A: wrong threshold (one-sigma, 16% figure reported as the 5% relative VaR); B: VaR misread as a maximum shortfall.
