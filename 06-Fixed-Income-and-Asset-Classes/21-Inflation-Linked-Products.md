---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: solid
prereqs: [swaps-and-curve-building]
est_hours: 4
sources: [31 CFR Part 356 Appendix B and 356.30 - TIPS index ratio and payments, Damiano Brigo and Fabio Mercurio - Interest Rate Models 2nd edition chapters 15 to 17, Robert Jarrow and Yildiray Yildirim - Pricing Treasury Inflation Protected Securities and Related Derivatives Using an HJM Model - JFQA 2003, Michael Fleming and John Sporn - Trading Activity and Price Transparency in the Inflation Swap Market - FRBNY Economic Policy Review 2013, BLS series CUUR0000SA0 CPI-U not seasonally adjusted]
---

# Inflation-Linked Products

## TL;DR

- Fisher: $1 + y_{\text{nom}} = (1 + y_{\text{real}})(1 + \pi)$; the nominal-real spread (breakeven) is expected inflation plus an inflation risk premium minus a TIPS liquidity premium, so it is not a pure forecast.
- TIPS principal is indexed to non-seasonally adjusted CPI-U through a Ref CPI that lags three months and interpolates daily (31 CFR Part 356 Appendix B); coupons are paid on the adjusted principal, and at maturity the principal is floored at par (31 CFR 356.30).
- A zero-coupon inflation swap exchanges $N[I(T)/I(0) - 1]$ for $N[(1 + K)^T - 1]$ at maturity; $(1 + K)^T$ is the $T$-forward expectation of the index ratio, which builds the inflation curve.
- Year-on-year swaps pay ratios over intermediate periods and need a convexity adjustment relative to the zero-coupon curve; Jarrow-Yildirim prices them by treating the CPI as an exchange rate between a nominal and a real economy.
- NSA CPI is strongly seasonal: from 2006 to 2024 it rose on average $0.54\%$ in March and fell on average $0.18\%$ in November, so short-dated inflation forwards must carry a seasonal adjustment.

## Learning objectives

- Formulate the Fisher relation connecting nominal yields, real yields, and inflation.
- Calculate TIPS daily index ratios, inflation-adjusted coupon cash flows, and terminal redemption with the deflation floor.
- Structure Zero-Coupon Inflation Swaps (ZCIS) and Year-on-Year (YoY) inflation swaps.
- Decompose the breakeven inflation rate into expected inflation, inflation risk premium, and liquidity premium.
- Explain the Jarrow-Yildirim (JY) foreign-currency analogy for modeling inflation term structures.
- Analyze how CPI seasonality and publication lags distort short-dated inflation pricing.

## Core concepts

### 1. Nominal and real rates

Fisher's relation, $1 + y_{\text{nom}} = (1 + y_{\text{real}})(1 + \pi)$, expands to $y_{\text{nom}} = y_{\text{real}} + \pi + y_{\text{real}} \pi$; dropping the cross term gives $y_{\text{nom}} \approx y_{\text{real}} + \pi$.
The breakeven inflation rate (BEIR) is the inflation rate that equates the returns on a nominal and an inflation-linked bond; decomposed,
$$\text{BEIR}(T) \approx \mathbb{E}^{\mathbb{P}}[\pi(T)] + \text{IRP}(T) - \text{LP}(T),$$
with IRP the inflation risk premium nominal bondholders demand and LP the premium TIPS holders demand for TIPS being less liquid than nominal Treasuries.
Both premia vary over time, so a fall in breakevens can be a rise in the liquidity premium rather than lower expected inflation.

### 2. TIPS mechanics (31 CFR Part 356)

TIPS, first auctioned by the US Treasury in 1997, index principal to the CPI for All Urban Consumers (CPI-U), not seasonally adjusted.

**Ref CPI (Appendix B).**
The Ref CPI for the first day of a month is the CPI of the third preceding month; for any other day it interpolates linearly toward the second preceding month:
$$\text{Ref CPI}(t) = \text{CPI}_{m-3} + \frac{d - 1}{D} \left( \text{CPI}_{m-2} - \text{CPI}_{m-3} \right),$$
with $d$ the calendar day and $D$ the number of days in month $m$.
The rule truncates Ref CPI and the index ratio to six decimals and rounds to five.
Because CPI for month $m - 2$ is published during month $m - 1$, both CPIs needed for any day of month $m$ are known before the month starts.
Appendix B uses the CPI as first published (later revisions are ignored; the NSA series is normally not revised), keeps the base period in effect at issue if the BLS rebases, and specifies a fallback index if a month is not reported.

**Index ratio, coupons and floor.**
$$\text{Index Ratio}(t) = \frac{\text{Ref CPI}(t)}{\text{Ref CPI}(\text{dated date})}, \qquad \text{Coupon} = \frac{c}{2} \times \text{Par} \times \text{Index Ratio}(t_i).$$
At maturity Treasury pays the inflation-adjusted principal, and if it is below par it pays an additional amount so the total equals par (31 CFR 356.30); the final coupon is still computed on the adjusted principal.
The floor is a put on the cumulative index ratio struck at 1, paid only at maturity and only on principal.
It is worth most for newly issued TIPS, whose index ratio is near 1, and little for seasoned TIPS that have accrued years of inflation.

**Tax.**
For US federal income tax, upward principal adjustments are taxable in the year they occur although they are paid only at maturity ("phantom income"), which is why TIPS are often held in tax-deferred accounts.

### 3. Inflation swaps

**Zero-coupon inflation swap.**
In the US the index is NSA CPI-U, the same as for TIPS, and the floating leg uses the index three months before the start and end dates (Fleming and Sporn 2013).
At maturity only the net amount is paid:
$$\text{Payoff to the inflation receiver} = N \left[ \frac{I(T)}{I(0)} - (1 + K)^T \right],$$
the inflation receiver paying fixed and the inflation payer receiving fixed.
With stochastic rates the fair $K$ comes from the $T$-forward measure:
$$0 = P(0, T)\, \mathbb{E}^{\mathbb{Q}^T}\left[\frac{I(T)}{I(0)}\right] - P(0, T)(1 + K)^T \implies (1 + K)^T = \mathbb{E}^{\mathbb{Q}^T}\left[\frac{I(T)}{I(0)}\right].$$
The left side is model-free: ZCIS quotes give the forward index $I(0) (1 + K_T)^T$ for each maturity directly, the inflation analogue of discount factors.

**Year-on-year swap.**
Each period pays $N[I(t_i)/I(t_{i-1}) - 1]$ at $t_i$.
$\mathbb{E}^{\mathbb{Q}^{t_i}}[I(t_i)/I(t_{i-1})]$ is not the ratio of the two forward indices: $I(t_{i-1})$ is a $t_{i-1}$ quantity paid at $t_i$, so the expectation picks up a covariance between the index and real and nominal rates, a convexity adjustment that needs a model.

### 4. The Jarrow-Yildirim model

Jarrow and Yildirim (2003) treat the CPI as the exchange rate between a nominal economy (domestic currency) and a real economy (foreign currency), with Gaussian (Hull-White type) nominal and real short rates $r_n$, $r_r$.
Under the nominal risk-neutral measure:
$$\frac{dI}{I} = (r_n - r_r) dt + \sigma_I dW_I, \qquad dr_r = \left[\theta_r(t) - a_r r_r - \rho_{r,I}\sigma_r \sigma_I\right] dt + \sigma_r dW_r.$$
The index drift $r_n - r_r$ is the no-arbitrage drift of an exchange rate (the real bond converted to nominal must earn $r_n$), and the real rate picks up a quanto term $-\rho_{r,I}\sigma_r\sigma_I$ when written under the nominal measure.
With correlations among $r_n$, $r_r$ and $I$, the model prices ZC and YoY swaps, caps and floors in closed form (Brigo and Mercurio, chapters 15 to 17).

### 5. Seasonality

The NSA CPI has a stable seasonal pattern.
From 2006 to 2024 the average month-on-month change was $0.42\%$ in January, $0.44\%$ in February and $0.54\%$ in March, against $-0.18\%$ in November and $-0.15\%$ in December; February never fell, while November fell in 14 of the 19 years and December in 13 (Example 6).
Writing $\text{CPI}(t) = \text{CPI}_{\text{trend}}(t) \times S(t)$ with monthly factors whose product over a year is 1, an inflation curve built from annual ZCIS quotes is interpolated in the trend and multiplied back by $S$; without it, a 6-month forward from January and one from July imply the same inflation, which the data say they should not.

## Worked examples

### Example 1: Ref CPI and index ratio from published CPI-U
CPI-U NSA was $314.540$ for July 2024 and $314.796$ for August 2024.
For settlement on 16 October 2024 ($d = 16$, $D = 31$):
$$\text{Ref CPI} = 314.540 + \frac{15}{31}(314.796 - 314.540) = 314.66387.$$
For a TIPS dated 15 July 2024, the base is $313.548 + \frac{14}{31}(314.069 - 313.548) = 313.78329$ (April and May 2024 CPI), so the index ratio is $314.66387 / 313.78329 = 1.00281$ after Treasury's truncation and rounding.
On 1 October 2024 the Ref CPI is exactly the July CPI, $314.54000$.

### Example 2: coupon with inflation accrual
$\$1,000$ par, $2.0\%$ real coupon, Ref CPI from $300.0$ at the dated date to $315.0$ on the coupon date: index ratio $1.0500$, adjusted principal $\$1,050.00$, coupon $1\% \times 1,050 = \$10.50$.
If this were the maturity date the payment would be $\$10.50 + \$1,050.00 = \$1,060.50$.

### Example 3: the deflation floor
Same bond, Ref CPI $285.0$ at maturity: index ratio $0.9500$.
The final coupon is on the adjusted principal, $1\% \times 950 = \$9.50$; the principal is floored, $\$1,000 \times \max(1, 0.95) = \$1,000.00$; the final payment is $\$1,009.50$.

### Example 4: breakeven
Nominal 10-year yield $4.25\%$, TIPS real yield $1.85\%$:
$$\text{BEIR}_{\text{exact}} = \frac{1.0425}{1.0185} - 1 = 2.3564\%, \qquad \text{BEIR}_{\text{approx}} = 4.25\% - 1.85\% = 2.4000\%.$$
The approximation is higher by $4.36$ bp, which is exactly the cross term $y_{\text{real}} \times \text{BEIR}_{\text{exact}}$, so it overstates when both are positive and understates when real yields are negative.

### Example 5: zero-coupon inflation swap
$\$10$ million notional, 5 years, $K = 2.40\%$: the fixed leg compounds to $(1.024)^5 = 1.125900$.
If the index ratio at maturity is $1.13$ the inflation receiver gets $10{,}000{,}000 \times (1.13 - 1.125900) = \$41,000.93$; at $1.10$ it pays $\$258,999.07$.

### Example 6: seasonality in the data
Using BLS series CUUR0000SA0 for December 2005 to December 2024, the mean month-on-month changes are $0.42\%$ (January), $0.44\%$ (February), $0.54\%$ (March), $-0.18\%$ (November) and $-0.15\%$ (December); November fell in 14 of 19 years, December in 13, February in none.
The twelve monthly means sum to $2.50\%$, close to the $2.52\%$ annualized inflation of the period, so the seasonal swing within a year is large relative to the trend for any horizon under a year.

## Pitfalls

- **Ignoring the indexation lag:** a TIPS or ZCIS cash flow depends on CPI three months earlier; matching it to a contemporaneous inflation forecast misstates accrual and carry.
- **Treating breakevens as forecasts:** breakevens include an inflation risk premium and a TIPS liquidity premium, both time-varying; in liquidity squeezes the liquidity premium can dominate the move.
- **Forgetting the floor is on principal only, at maturity:** coupons are not floored, and the floor on a seasoned TIPS with an index ratio well above 1 is nearly worthless.
- **No seasonal adjustment on short forwards:** the March and November mean changes differ by $0.72\%$ in our sample; unadjusted short-dated forwards and carry estimates inherit that error.
- **Pricing YoY from the ZC curve without a convexity adjustment:** the YoY expectation differs from the ratio of forward indices by a model-dependent covariance term.
- **Phantom income:** taxable holders owe tax on principal accretion before receiving it.

## Interview questions

> [!question]- fi-inflation-fisher-equation | State the exact and approximate Fisher equations for interest rates.
> Exact: $1 + y_{\text{nom}} = (1 + y_{\text{real}})(1 + \pi)$; approximate: $y_{\text{nom}} \approx y_{\text{real}} + \pi$.
> The approximation drops the cross term $y_{\text{real}}\pi$, $4.36$ bp in Example 4.

> [!question]- fi-inflation-index-ratio | How is the TIPS index ratio defined?
> $\text{Ref CPI}(t) / \text{Ref CPI}(\text{dated date})$, where Ref CPI is the NSA CPI-U of the third preceding month interpolated daily toward the second preceding month, truncated to six decimals and rounded to five (31 CFR Part 356 Appendix B).
> For 16 October 2024 against a 15 July 2024 base: $314.66387 / 313.78329 = 1.00281$.

> [!question]- fi-inflation-deflation-floor | What is the TIPS deflation floor and when is it valuable?
> At maturity Treasury pays the larger of the inflation-adjusted principal and par (31 CFR 356.30); coupons are not floored.
> It is a put on the cumulative index ratio struck at 1, priced into the real yield rather than free, and valuable for new issues (index ratio near 1) when cumulative deflation over the remaining life is plausible.

> [!question]- fi-inflation-breakeven-components | What economic components make up the Breakeven Inflation Rate (BEIR)?
> Expected inflation, plus the inflation risk premium demanded by nominal bondholders, minus the liquidity premium demanded by TIPS holders.
> Because both premia move, breakevens are not pure inflation forecasts.

> [!question]- fi-inflation-zcis-structure | Describe the cash flow structure of a Zero-Coupon Inflation Swap (ZCIS).
> One net payment at maturity: the inflation receiver gets $N[I(T)/I(0) - 1]$ and pays $N[(1 + K)^T - 1]$, with the index lagged three months in the US.
> On $\$10$ million for 5 years at $K = 2.40\%$ and a realized ratio of $1.13$, the inflation receiver nets $\$41,000.93$.

> [!question]- fi-inflation-lag-rationale | Why do TIPS use a 3-month indexation lag instead of contemporaneous CPI?
> CPI for a month is published in the following month, so a three-month lag with interpolation toward the second preceding month guarantees that both CPIs needed for every day of a month are known before that month starts.
> Accrued interest and settlement amounts are therefore known in advance; the rule also uses CPI as first published, so revisions cannot change cash flows.

> [!question]- fi-inflation-phantom-income | What is phantom income on TIPS and who is affected by it?
> The annual upward adjustment of TIPS principal, which is taxable for US federal income tax in the year it occurs although it is paid only at maturity.
> Taxable holders pay tax before receiving the cash; tax-deferred accounts avoid the mismatch.

> [!question]- fi-inflation-jy-model | What is the Jarrow-Yildirim (JY) model and what analogy does it use?
> A three-factor model in which the CPI is the exchange rate between a nominal (domestic) and a real (foreign) economy, with Gaussian nominal and real short rates and a lognormal index.
> Under the nominal measure the index drifts at $r_n - r_r$ and the real short rate picks up a quanto term $-\rho_{r,I}\sigma_r\sigma_I$, exactly as a foreign rate does in an FX model.

> [!question]- fi-inflation-seasonality-impact | Why does CPI seasonality matter for inflation derivatives?
> NSA CPI rises much more in some months than others: from 2006 to 2024 the mean change was $0.54\%$ in March and $-0.18\%$ in November.
> A curve built from annual ZCIS quotes must be interpolated in trend inflation and multiplied by seasonal factors, or short-dated forwards, carry and fixings on different months are mispriced.

> [!question]- fi-inflation-yoy-convexity | Why do Year-on-Year inflation swaps require a convexity adjustment?
> Each YoY payment $I(t_i)/I(t_{i-1})$ at $t_i$ involves $I(t_{i-1})$, which is not a $t_i$-forward martingale quantity, so its expectation is not the ratio of forward indices from the ZC curve.
> The difference is a covariance between the index and real and nominal rates over $[t_{i-1}, t_i]$, which models such as Jarrow-Yildirim quantify.

> [!question]- fi-inflation-ref-cpi-calc | CPI-U was 314.540 for July 2024 and 314.796 for August 2024. What is the Ref CPI for 16 October 2024?
> $314.540 + \frac{15}{31} \times 0.256 = 314.66387$.
> October uses July (third preceding month) and August (second preceding), with weight $(d - 1)/D = 15/31$.

> [!question]- fi-inflation-zcis-forward-measure | Why is the fair ZCIS rate an expectation under the $T$-forward measure rather than the risk-neutral measure?
> The payoff is paid at $T$, so its value is $P(0, T) \mathbb{E}^{\mathbb{Q}^T}[\cdot]$; under the money-market measure the stochastic discount factor would multiply the index inside the expectation.
> The forward index $I(0)(1 + K)^T$ is therefore $\mathbb{E}^{\mathbb{Q}^T}[I(T)]$, model-free, while YoY payments need a model.

> [!question]- fi-inflation-breakeven-bias-sign | Does $y_{\text{nom}} - y_{\text{real}}$ overstate or understate the exact breakeven?
> It differs by exactly $y_{\text{real}} \times \text{BEIR}_{\text{exact}}$: it overstates when the real yield and breakeven are both positive ($4.36$ bp at $4.25\%$ and $1.85\%$) and understates when real yields are negative.

> [!question]- fi-inflation-floor-new-vs-seasoned | Two TIPS mature on the same date; one was issued last month, the other 10 years ago. Which has the more valuable deflation floor?
> The new issue: its index ratio is near 1, so modest cumulative deflation puts the floor in the money.
> The seasoned bond's index ratio already reflects 10 years of inflation, so prices would have to fall by that much before maturity for its floor to pay.

> [!question]- fi-inflation-cpi-revisions | What happens to TIPS cash flows if the BLS revises a CPI number or rebases the index?
> Nothing: 31 CFR Part 356 Appendix B uses the CPI as first published, and after a rebasing continues with the base period in effect when the security was issued.
> If a month is not reported in time, Treasury announces a substitute index number based on the last available twelve-month change.

## Further reading

- 31 CFR Part 356, Appendix B (Methods for computing inflation-protected securities) and section 356.30 (payments), via the Electronic Code of Federal Regulations.
- Robert Jarrow and Yildiray Yildirim, *Pricing Treasury Inflation Protected Securities and Related Derivatives Using an HJM Model*, Journal of Financial and Quantitative Analysis, 2003.
- Damiano Brigo and Fabio Mercurio, *Interest Rate Models - Theory and Practice*, 2nd edition, Springer, 2006, chapters 15 (pricing of inflation-indexed derivatives), 16 (inflation-indexed swaps) and 17 (inflation-indexed caplets and floorlets).
- Michael Fleming and John Sporn, *Trading Activity and Price Transparency in the Inflation Swap Market*, Federal Reserve Bank of New York Economic Policy Review, May 2013.
- US Bureau of Labor Statistics, CPI-U all items, not seasonally adjusted, series CUUR0000SA0.

## In this repo and SDE-Interview-Prep

- Code: [`code/fi_inflation.py`](code/fi_inflation.py) asserts every number here, including the Ref CPI rule on published CPI-U and the seasonality statistics computed from the embedded BLS series.
- Prereqs: [Swaps and Curve Building](03-Swaps-and-Curve-Building.md), [Day Counts, Calendars and Schedules](11-Day-Counts-Calendars-and-Schedules.md).
- Next: [Mortgages and Securitized Products](22-Mortgages-and-Securitized-Products.md).
