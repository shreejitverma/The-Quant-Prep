---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 4
title: "Norvald State Fund: Manager Return and Risk Attribution"
los: [los-09-04-e, los-09-04-g]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Norvald State Fund: Manager Return and Risk Attribution

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

The Norvald State Investment Fund, a sovereign wealth fund, is reviewing two external managers of its US large-cap equity allocation before renewing their mandates.
Both managers are benchmarked to the same large-cap index.
The fund's guidelines require each active manager to deliver an information ratio of at least 0.30 and to keep tracking risk at or below 4.5% per year, both measured over the trailing five years.
Signe Haugland, CFA, heads external manager selection, and Kofi Mensah is the analyst assigned to the review.

Aurelia Capital describes itself as a bottom-up stock picker with no deliberate factor bets.
Mensah decomposes Aurelia's most recent annual performance using a Carhart four-factor model.
Sensitivities are measured at the start of the year.

**Exhibit 1: Aurelia Capital, most recent year**

| Factor | Portfolio sensitivity | Benchmark sensitivity | Factor return |
|---|---|---|---|
| RMRF | 1.10 | 1.00 | 7.20% |
| SMB | 0.35 | 0.10 | -1.80% |
| HML | -0.20 | 0.05 | 2.40% |
| WML | 0.30 | 0.00 | 4.50% |

Aurelia's portfolio returned 12.35% and the benchmark returned 10.60%.
The one-month Treasury bill averaged 4.80% over the year.

Mensah then obtains a fundamental factor model risk decomposition for both managers over the trailing five years.
Industry and style factor covariances are assumed negligible.

**Exhibit 2: Active risk decomposition, trailing five years**

| Manager | Active industry risk (% squared) | Active style risk (% squared) | Active specific risk (% squared) | Mean annual active return |
|---|---|---|---|---|
| Aurelia Capital | 3.24 | 9.00 | 3.76 | 1.40% |
| Bramwell Partners | 0.50 | 3.50 | 21.00 | 1.80% |

Bramwell Partners runs a concentrated portfolio of about 45 stocks.
Mensah examines Bramwell's three largest active positions to see how much of its active specific risk they explain.

**Exhibit 3: Bramwell Partners, three largest active positions**

| Stock | Portfolio weight | Benchmark weight | Residual (specific) standard deviation |
|---|---|---|---|
| Stock X | 4.60% | 0.60% | 38% |
| Stock Y | 3.20% | 0.20% | 30% |
| Stock Z | 0.00% | 2.50% | 26% |

At the review meeting, two trustees comment.

Trustee Lund: "Our internal S&P 500 index sleeve has a tracking error of only 0.08% a year, so it must have the highest information ratio of anything we own."

Trustee Brekke: "Bramwell's HML sensitivity is zero. Because it holds no HML exposure, the HML factor cannot contribute to its active risk, even though the benchmark's HML sensitivity is 0.05."

Haugland asks Mensah to state whether Aurelia's results are consistent with its description of itself and which managers satisfy both guideline limits.

## Questions

1. For Aurelia's most recent year, the return from factor tilts and the return from security selection are closest to: (LOS: los-09-04-e)
   - A. 1.02% and 0.73%.
   - B. 1.92% and -0.17%.
   - C. 8.16% and -6.41%.
2. Which statement best characterizes Aurelia's most recent year? (LOS: los-09-04-e)
   - A. Security selection produced about 42% of active return, and the momentum tilt was the largest single source of active return.
   - B. The value tilt added return because HML was positive, which suggests a value-oriented stock picker.
   - C. The small-cap tilt was the largest positive contributor, because the portfolio's SMB sensitivity exceeds the benchmark's.
3. For Aurelia, the proportion of active risk squared attributable to active factor risk, and the annual tracking error, are closest to: (LOS: los-09-04-g)
   - A. 76.5% and 4.00%.
   - B. 23.5% and 4.00%.
   - C. 76.5% and 16.00%.
4. Which managers satisfy both the information ratio and the tracking risk guidelines? (LOS: los-09-04-g)
   - A. Aurelia only.
   - B. Bramwell only.
   - C. Neither manager.
5. The contribution of the three positions in Exhibit 3 to Bramwell's active specific risk is closest to: (LOS: los-09-04-g)
   - A. 1.88 (% squared).
   - B. 3.54 (% squared).
   - C. 10.41 (% squared).
6. Regarding the trustees' comments, which is correct? (LOS: los-09-04-g)
   - A. Lund's only.
   - B. Brekke's only.
   - C. Neither.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Each tilt contribution is (portfolio sensitivity minus benchmark sensitivity) times the factor return.
> RMRF: $(1.10 - 1.00)(7.20) = 0.7200\%$; SMB: $(0.35 - 0.10)(-1.80) = -0.4500\%$; HML: $(-0.20 - 0.05)(2.40) = -0.6000\%$; WML: $(0.30 - 0.00)(4.50) = 1.3500\%$.
> Return from factor tilts $= 0.7200 - 0.4500 - 0.6000 + 1.3500 = 1.0200\%$.
> Active return $= 12.35 - 10.60 = 1.7500\%$, so security selection $= 1.7500 - 1.0200 = 0.7300\%$.
> B is wrong because it treats the SMB factor return as $+1.80\%$, a sign error that turns the SMB contribution into $+0.4500\%$ and gives tilts of $1.9200\%$ and selection of $-0.1700\%$.
> C is wrong because it multiplies the portfolio's own sensitivities, not the differences from the benchmark, by the factor returns: $7.92 - 0.63 - 0.48 + 1.35 = 8.1600\%$ and selection $1.75 - 8.16 = -6.4100\%$.
> 2. **A.** Security selection is $0.73/1.75 = 41.71\%$ of active return, and the WML tilt contributed $1.35/1.75 = 77.14\%$, the largest single source.
> The result only partly supports the stock-picker description: more than half of active return ($1.02/1.75 = 58.29\%$) came from factor tilts, mainly a momentum bet the manager says it does not make.
> B is wrong because Aurelia's HML sensitivity is below the benchmark's (a growth tilt), so the positive HML return cost $0.60\%$.
> C is wrong because small caps underperformed (SMB of $-1.80\%$), so the overweight in SMB cost $0.45\%$.
> The Treasury bill rate is a decoy; the decomposition uses only sensitivities and factor returns.
> 3. **A.** Active factor risk $= 3.24 + 9.00 = 12.24$; active risk squared $= 12.24 + 3.76 = 16.00$.
> Factor proportion $= 12.24/16.00 = 76.50\%$, and tracking error $= \sqrt{16.00} = 4.00\%$.
> B is wrong because $3.76/16.00 = 23.50\%$ is the active specific share, not the factor share.
> C is wrong because it reports active risk squared as the tracking error, forgetting the square root.
> 4. **A.** Aurelia: TE $= 4.00\%$ and $IR = 1.40/4.00 = 0.35$, so both guidelines are met.
> Bramwell: active risk squared $= 0.50 + 3.50 + 21.00 = 25.00$, TE $= 5.00\%$, and $IR = 1.80/5.00 = 0.36$; the IR passes but TE exceeds the 4.5% limit.
> B is wrong because it picks the higher IR and ignores the tracking risk limit.
> C is wrong because it divides mean active return by active risk squared: $1.40/16.00 = 0.0875$ and $1.80/25.00 = 0.0720$, both below 0.30.
> 5. **B.** Active weights are $4.60 - 0.60 = +4.00\%$, $3.20 - 0.20 = +3.00\%$, and $0.00 - 2.50 = -2.50\%$.
> Active specific risk $= \sum (w_i^a)^2 \sigma_{\varepsilon_i}^2 = (0.04)^2(0.38)^2 + (0.03)^2(0.30)^2 + (0.025)^2(0.26)^2$.
> That is $0.00023104 + 0.00008100 + 0.00004225 = 0.00035429$, or $3.5429$ (% squared), about 17% of Bramwell's 21.00.
> A is wrong because it takes the square root, $\sqrt{0.00035429} = 1.88\%$, reporting a standard deviation where a variance is asked for.
> C is wrong because it uses residual standard deviations instead of residual variances: $0.0016(0.38) + 0.0009(0.30) + 0.000625(0.26) = 0.0010405$, or $10.41$.
> 6. **C.** Lund is wrong: a well-run index fund has an active return of about zero, so its information ratio is about zero regardless of how small its tracking error is.
> Brekke is wrong: any sensitivity that differs from the benchmark's is an active exposure, so a zero HML sensitivity against a benchmark sensitivity of 0.05 is an active bet of $-0.05$ that contributes to active risk.
> A is wrong because low tracking error does not make the ratio large when the numerator is zero.
> B is wrong because a zero portfolio sensitivity is not the same as a zero active sensitivity.

## Distractor design

- Q1: B = sign error on the SMB factor return; C = portfolio sensitivities used instead of differences from the benchmark.
- Q2: B = growth tilt misread as value tilt; C = SMB overweight credited despite a negative factor return.
- Q3: B = specific share reported as factor share; C = variance reported as tracking error (square root omitted).
- Q4: B = IR limit checked but tracking risk limit ignored; C = IR computed with active risk squared in the denominator.
- Q5: A = standard deviation reported instead of variance; C = residual standard deviation used instead of residual variance.
- Q6: A = low tracking error confused with high IR; B = zero portfolio sensitivity confused with zero active exposure.
