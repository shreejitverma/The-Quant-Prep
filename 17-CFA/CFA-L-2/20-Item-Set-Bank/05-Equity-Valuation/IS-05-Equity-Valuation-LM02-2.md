---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 2
title: "Kestrel Diagnostics: Multistage Models for a Medtech Long Book"
los: [los-05-02-i, los-05-02-k, los-05-02-l, los-05-02-m, los-05-02-n]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Kestrel Diagnostics: Multistage Models for a Medtech Long Book

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Rafael Ortiz, CFA, is a portfolio manager at Tamsin Growth Partners, a US long/short equity fund specializing in medical technology.
On 15 May 2026 he is valuing Kestrel Diagnostics Inc., a maker of point-of-care molecular testing instruments and the single-use cartridges they consume.
Kestrel initiated a dividend in 2022 and paid its most recent annual dividend of USD 0.80 per share last month.
Kestrel's shares trade at USD 38.75.

Ortiz expects Kestrel's dividends to grow at 16% a year for the next three years while its new cartridge platform gains share in hospital laboratories.
From the end of year 3, rival platforms are expected to reach the market, and Ortiz forecasts that dividend growth will decline linearly over six years to a mature rate of 5%, which it will then maintain indefinitely.
He estimates Kestrel's required return with the CAPM.

Exhibit 1: Kestrel valuation inputs

| Input | Value |
|---|---|
| Risk-free rate | 3.0% |
| Equity risk premium | 5.0% |
| Kestrel beta | 1.20 |
| Kestrel pretax cost of debt | 6.4% |
| Expected dividend payout ratio, year 3 | 40% |
| Expected trailing P/E at the end of year 3 (peer median) | 15.0 |

Ortiz's colleague Mei Hashimoto challenges the terminal value.
She argues that a price multiple is a better anchor than a growth assumption, and proposes valuing Kestrel at the end of year 3 by applying the expected peer trailing P/E in Exhibit 1 to Kestrel's year-3 earnings.
She also asks Ortiz to show what the valuation would be if Kestrel's growth dropped abruptly from 16% to 5% at the end of year 3 instead of declining gradually.

Ortiz then reviews three smaller companies that Tamsin may pair against Kestrel.

Exhibit 2: Peer profiles

| Company | Profile |
|---|---|
| Brightwater Imaging | EPS growth has slowed from 25% to 11% over three years as rivals entered its market; free cash flow to equity turned positive two years ago; the payout ratio has risen from 0% to 22%; ROE has fallen from 21% to 14%, against a required return of 10% |
| Norbeck Surgical | Earnings and dividends are expected to grow at 20% a year until its core patent expires at the end of year 4; generic competition is then expected to cut growth immediately to a permanent 4% |
| Castellan Labs | Most recent annual dividend of USD 1.10; share price USD 38.50; dividend growth of 12% is expected to decline linearly over eight years to a mature 4% |

Ortiz wants the market-implied expected return on Castellan to compare with his own estimates for the sector.
Tamsin's risk committee requires every multistage valuation to state which model is used and why, and to report the share of value that comes from the terminal value.

## Questions

1. Based on Exhibit 2, Brightwater Imaging is most likely in its: (LOS: los-05-02-k)
   - A. growth phase.
   - B. transition phase.
   - C. mature phase.
2. The most appropriate dividend discount model for valuing Norbeck Surgical is the: (LOS: los-05-02-l)
   - A. two-stage DDM.
   - B. H-model.
   - C. Gordon growth model.
3. Using Ortiz's growth forecast, the value of a Kestrel share today is closest to: (LOS: los-05-02-n)
   - A. USD 33.24.
   - B. USD 35.99.
   - C. USD 43.94.
4. Hashimoto's terminal value for Kestrel at the end of year 3 is closest to: (LOS: los-05-02-m)
   - A. USD 18.73.
   - B. USD 31.22.
   - C. USD 46.83.
5. The expected return on Castellan Labs implied by its current share price is closest to: (LOS: los-05-02-i)
   - A. 6.97%.
   - B. 7.89%.
   - C. 8.80%.
6. Under Hashimoto's alternative growth assumption, the value of a Kestrel share today is closest to: (LOS: los-05-02-n)
   - A. USD 25.94.
   - B. USD 26.83.
   - C. USD 28.03.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Slowing growth as competitors enter, FCFE turning positive, a payout rising from zero and ROE falling toward the required return are the signatures of the transition phase.
> A is wrong because the growth phase has negative FCFE and low or zero payout, whereas Brightwater's FCFE has been positive for two years and it now pays out 22%.
> C is wrong because in the mature phase ROE has converged to about the required return and growth, payout and ROE are stable; Brightwater's ROE (14%) is still above $r$ (10%) and still falling.
> 2. **A.** Norbeck has a constant 20% stage that ends at a known date (patent expiry) and then steps down abruptly to a permanent 4%, which is the two-stage DDM's assumption.
> B is wrong because the H-model assumes growth declines linearly, not abruptly.
> C is wrong because four years of 20% growth cannot be represented by one perpetual rate.
> 3. **B.** $r = 3.0\% + 1.20 \times 5.0\% = 9.0\%$.
> Stage 1: $D_1 = 0.9280$, $D_2 = 1.0765$, $D_3 = 1.2487$, with PVs $0.8514 + 0.9061 + 0.9642 = 2.7217$.
> Stages 2 and 3 are an H-model at $t = 3$ with $H = 6/2 = 3$ and $D_3$ in place of $D_0$: $V_3 = [1.2487 \times 1.05 + 1.2487 \times 3 \times (0.16 - 0.05)]/(0.09 - 0.05) = (1.3112 + 0.4121)/0.04 = 32.7788 + 10.3019 = 43.0807$.
> PV of $V_3 = 43.0807/1.09^3 = 43.0807/1.2950 = 33.2662$; $V_0 = 2.7217 + 33.2662 = 35.9879$, or USD 35.99.
> The terminal value is $33.2662/35.9879 = 92.4\%$ of value, the figure the risk committee requires.
> Calculator: C01 = 0.9280, C02 = 1.0765, C03 = 1.2487 + 43.0807 = 44.3294, I = 9, NPV = 35.99.
> A is wrong because it discounts $V_3$ four periods ($43.0807/1.4116 = 30.5195$, total 33.24).
> C is wrong because it sets $H$ equal to the full six-year transition: $V_3 = 1.2487 \times (1.05 + 0.66)/0.04 = 53.3826$, PV 41.2212, total 43.94.
> 4. **C.** $E_3 = D_3/\text{payout} = 1.2487/0.40 = 3.1218$; $V_3 = 15.0 \times 3.1218 = 46.83$.
> A trailing multiple is applied to the earnings of the terminal year itself, so $E_3$ is the correct base.
> A is wrong because it applies the P/E to the dividend, $15.0 \times 1.2487 = 18.73$.
> B is wrong because it backs out earnings with the retention ratio, $1.2487/0.60 = 2.0812$ and $15.0 \times 2.0812 = 31.22$.
> 5. **B.** Eight-year decline, so $H = 4$: $r = (D_0/P_0)[(1 + g_L) + H(g_S - g_L)] + g_L = (1.10/38.50)[1.04 + 4 \times 0.08] + 0.04 = 0.028571 \times 1.36 + 0.04 = 0.038857 + 0.04 = 7.89\%$.
> A is wrong because it is the Gordon expected return at the mature rate, $1.10 \times 1.04/38.50 + 0.04 = 0.029714 + 0.04 = 6.97\%$, which ignores the supernormal years.
> C is wrong because it uses $H = 8$, the full transition length: $0.028571 \times 1.68 + 0.04 = 8.80\%$.
> 6. **C.** Two-stage: $V_3 = D_4/(r - g_L) = 1.2487 \times 1.05/0.04 = 1.3112/0.04 = 32.7788$; PV $= 32.7788/1.2950 = 25.3113$.
> $V_0 = 2.7217 + 25.3113 = 28.03$.
> The abrupt drop removes the gradual decline years, so value falls by about 7.96 relative to Question 3.
> A is wrong because it discounts $V_3$ four periods ($32.7788/1.4116 = 23.2213$, total 25.94).
> B is wrong because it builds the terminal value from $D_3$ instead of $D_4$ ($1.2487/0.04 = 31.2179$, PV 24.1060, total 26.83).

## Distractor design

1. A: positive FCFE and rising payout overlooked; C: ROE above $r$ and still falling read as mature.
2. B: abrupt step confused with linear decline; C: supernormal stage ignored.
3. A: terminal value discounted $n + 1$ periods; C: $H$ set to the full transition length instead of half.
4. A: multiple applied to the dividend instead of earnings; B: retention used instead of payout to back out $E_n$.
5. A: Gordon return at $g_L$ ignores the H-model add-on; C: $H$ set to the full transition length.
6. A: terminal value discounted $n + 1$ periods; B: terminal value built from $D_n$ instead of $D_{n+1}$.
