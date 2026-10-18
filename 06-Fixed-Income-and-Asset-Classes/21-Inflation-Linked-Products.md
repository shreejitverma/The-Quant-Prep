---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: solid
prereqs: [swaps-and-curve-building]
est_hours: 4
sources: [Damiano Brigo and Fabio Mercurio - Interest Rate Models chapter 18, US Treasury TIPS Guidelines at treasurydirect.gov]
---

# Inflation-Linked Products

## TL;DR

Inflation-linked debt and derivatives protect purchasing power by indexing cash flows to headline consumer price indices (such as US CPI-U or Eurozone HICP).
Under the Fisher hypothesis, nominal yields decompose into real yields plus expected inflation and an inflation risk premium.
Treasury Inflation-Protected Securities (TIPS) adjust bond principal daily via an index ratio with a 3-month publication lag, paying coupons on the adjusted principal and guaranteeing par redemption via an embedded deflation floor.
Zero-Coupon Inflation Swaps (ZCIS) isolate pure market-implied cumulative inflation without liquidity distortions, establishing the zero-coupon inflation curve.
The breakeven inflation rate measures the yield spread between nominal Treasuries and TIPS, capturing market inflation expectations adjusted for liquidity and risk premia.

## Learning objectives

- Formulate the Fisher relation connecting nominal yields, real yields, and inflation.
- Calculate TIPS daily index ratios, inflation-adjusted coupon cash flows, and terminal redemption with the deflation floor.
- Structure Zero-Coupon Inflation Swaps (ZCIS) and Year-on-Year (YoY) inflation swaps.
- Decompose the breakeven inflation rate into expected inflation, inflation risk premium, and liquidity premium.
- Explain the Jarrow-Yildirim (JY) foreign-currency analogy for modeling inflation term structures.
- Analyze how CPI seasonality and publication lags distort short-dated inflation pricing.

## Core concepts

### 1. Nominal vs Real Interest Rates and the Fisher Equation

Inflation erodes the purchasing power of money over time.
An investor who receives a $5\%$ return in a $3\%$ inflation environment earns an effective purchasing power increase of approximately $2\%$.

Irving Fisher (1930) formalized the relationship between nominal interest rate $y_{\text{nom}}$, real interest rate $y_{\text{real}}$, and inflation rate $\pi$:
$$1 + y_{\text{nom}} = (1 + y_{\text{real}})(1 + \pi)$$
Expanding the product:
$$y_{\text{nom}} = y_{\text{real}} + \pi + y_{\text{real}} \pi$$
For small rates, the cross-product $y_{\text{real}} \pi$ is negligible, yielding the standard first-order Fisher equation:
$$y_{\text{nom}} \approx y_{\text{real}} + \pi$$

In market equilibrium, the spread between nominal and real bond yields contains additional risk premia:
$$y_{\text{nom}}(T) - y_{\text{real}}(T) = \mathbb{E}[\pi(T)] + \text{IRP}(T) - \text{LP}(T)$$
where:
- $\mathbb{E}[\pi(T)]$ is the expected annualized inflation rate over horizon $T$.
- $\text{IRP}(T)$ is the **Inflation Risk Premium** (compensation demanded by nominal bondholders for bearing uncertain future inflation).
- $\text{LP}(T)$ is the **TIPS Liquidity Premium** (compensation demanded by TIPS holders because the TIPS market is less liquid than the nominal Treasury market).

The difference $y_{\text{nom}}(T) - y_{\text{real}}(T)$ is termed the **Breakeven Inflation Rate (BEIR)**.

### 2. Treasury Inflation-Protected Securities (TIPS) Mechanics

First issued by the US Treasury in 1997, TIPS are government bonds whose principal is indexed to the non-seasonally adjusted Consumer Price Index for All Urban Consumers (CPI-U).

#### The Index Ratio
The inflation accrual of a TIPS bond on settlement date $t$ is governed by the **Index Ratio**:
$$\text{Index Ratio}(t) = \frac{\text{Ref CPI}(t)}{\text{Base CPI}}$$
where:
- $\text{Base CPI}$ is the reference CPI value on the original dated date of the bond.
- $\text{Ref CPI}(t)$ is the reference CPI for date $t$.

#### The 3-Month Indexation Lag
Because monthly CPI numbers are published by the Bureau of Labor Statistics (BLS) roughly mid-month for the preceding month, cash flow amounts cannot rely on unreleased contemporaneous CPI data.
TIPS utilize a standardized 3-month interpolation lag:
- On the first day of calendar month $m$, the reference CPI equals the headline CPI published for month $m - 3$:
$$\text{Ref CPI}(\text{First Day of Month } m) = \text{CPI}_{m-3}$$
- For date $t$ falling on day $d$ of a month with $D$ calendar days, $\text{Ref CPI}(t)$ is linearly interpolated between $\text{CPI}_{m-3}$ and $\text{CPI}_{m-2}$:
$$\text{Ref CPI}(t) = \text{CPI}_{m-3} + \frac{d - 1}{D} \left( \text{CPI}_{m-2} - \text{CPI}_{m-3} \right)$$

#### Cash Flow Calculations
1. **Semi-Annual Coupon Payments:** The fixed real coupon rate $c$ is paid semi-annually on the inflation-adjusted principal:
$$\text{Coupon Payment}(t_i) = \frac{c}{2} \times \text{Base Principal} \times \text{Index Ratio}(t_i)$$
When inflation occurs ($\text{Index Ratio} > 1.0$), dollar coupon payments increase proportionately.
2. **Principal Redemption at Maturity:** At maturity $T$, the investor receives the adjusted principal, but protected by a **Deflation Floor**:
$$\text{Redemption Payment}(T) = \text{Base Principal} \times \max\left(1.0, \text{Index Ratio}(T)\right)$$
If cumulative inflation over the bond's lifetime is negative ($\text{Index Ratio} < 1.0$), the investor is guaranteed to receive 100% of the original par value.
The deflation floor is an embedded European put option on the consumer price index with strike equal to the base CPI.

### 3. Inflation Swaps

While TIPS combine real yield risk, nominal discount risk, and inflation optionality, inflation swaps isolate pure forward inflation expectations.

#### Zero-Coupon Inflation Swap (ZCIS)
The Zero-Coupon Inflation Swap is the fundamental benchmark contract of the inflation derivatives market.
At trade inception ($t = 0$), party A and party B agree on a fixed inflation rate $K$ for maturity $T$.
No cash flows occur until maturity $T$.

At maturity $T$, a single net payment is exchanged on notional $N$:
$$\text{Payoff}_{\text{Inflation Receiver}} = N \times \left[ \left(\frac{\text{CPI}(T)}{\text{CPI}(0)}\right) - (1 + K)^T \right]$$
- **Inflation Receiver (fixed payer):** Pays the fixed compounded rate $(1 + K)^T - 1$ and receives realized inflation, so the payoff above is positive when realized inflation exceeds $K$.
- **Inflation Payer (fixed receiver):** Pays the floating realized cumulative percentage inflation return $\frac{\text{CPI}(T)}{\text{CPI}(0)} - 1$; its payoff is the negative of the payoff above.

The fair breakeven swap rate $K$ equates the present value of the two legs to zero:
$$(1 + K)^T = \mathbb{E}_{\mathbb{Q}}\left[ \frac{\text{CPI}(T)}{\text{CPI}(0)} \right]$$
The term structure of ZCIS rates directly establishes the zero-coupon market inflation curve.

#### Year-on-Year (YoY) Inflation Swaps
In a Year-on-Year inflation swap, cash flows occur annually.
At each annual date $t_i$, the floating leg pays annual realized inflation:
$$\text{Floating Payment}(t_i) = N \times \left[ \frac{\text{CPI}(t_i)}{\text{CPI}(t_{i-1})} - 1 \right]$$
against a fixed rate $K_{\text{YoY}}$.
Unlike ZCIS, which compounds the fixed rate annually to a single terminal payment, YoY swaps pay individual one-year forward inflation rates discounted on intermediate dates.
Because the payment dates differ from the terminal measure, YoY swap rates require a convexity adjustment relative to forward rates extracted from ZCIS curves.

### 4. The Jarrow-Yildirim (JY) Foreign-Currency Model

Robert Jarrow and Yildiray Yildirim (2002) formulated a 3-factor term structure model by establishing a mathematical equivalence between inflation and foreign exchange:
- **Nominal Economy:** Analogous to the domestic currency (US Dollars).
- **Real Economy:** Analogous to a foreign currency (Goods / Baskets of consumption).
- **Price Index $I(t)$:** Analogous to the nominal exchange rate (Dollars per basket of goods).

Under the nominal risk-neutral measure $\mathbb{Q}$:
1. The nominal short rate $r_n(t)$ follows Hull-White or HJM dynamics.
2. The real short rate $r_r(t)$ follows Hull-White dynamics.
3. The price index $I(t)$ evolves as a geometric process:
$$\frac{dI(t)}{I(t)} = (r_n(t) - r_r(t)) dt + \sigma_I dW_I(t)$$
This drift condition satisfies uncovered interest parity: the expected inflation rate under the nominal pricing measure equals the nominal interest rate minus the real interest rate.
The model accounts for correlation between nominal rates, real rates, and the price index ($\rho_{n, r}, \rho_{n, I}, \rho_{r, I}$), providing the standard framework for pricing inflation caps, floors, and YoY options.

### 5. CPI Seasonality

Headline CPI exhibits strong seasonal patterns driven by consumer spending cycles, energy demand, and agriculture:
- CPI rises rapidly in the spring (March, April, May) due to post-holiday price resets and summer travel demand.
- CPI slows or contracts in the late autumn and winter (November, December, January).

Because TIPS index to non-seasonally adjusted CPI, short-dated TIPS yields and inflation forwards are heavily distorted by seasonal swings:
$$\text{CPI}(t) = \text{CPI}_{\text{trend}}(t) \times S(t)$$
where $S(t)$ is a seasonal adjustment factor satisfying $\prod_{m=1}^{12} S(m) = 1$.
Desks trading short-dated inflation swaps must strip out seasonal multipliers to prevent mispricing 6-month vs 12-month forward contracts.

## Worked examples

### Example 1: TIPS Cash Flow Calculation with Inflation Accrual
An investor purchases $\$1,000$ base par value of a 10-year TIPS with a $2.0\%$ real coupon (paid semi-annually).
At coupon date $t$, the reference CPI has risen from base value $300.0$ to $315.0$.
Calculate the index ratio and the semi-annual coupon payment.

1. Compute the Index Ratio:
$$\text{Index Ratio} = \frac{\text{Ref CPI}}{\text{Base CPI}} = \frac{315.0}{300.0} = 1.0500 \quad (105\%)$$
2. Compute the adjusted principal:
$$\text{Adjusted Principal} = \$1,000 \times 1.0500 = \$1,050.00$$
3. Compute the semi-annual coupon:
$$\text{Coupon} = \frac{2.0\%}{2} \times \$1,050.00 = 1.0\% \times \$1,050.00 = \$10.50$$
Our reference code [`code/fi_inflation.py`](code/fi_inflation.py) confirms:
`tips_cash_flow(0.02, 1000.0, 1.05, is_maturity=False) == 10.50`.
If the bond matured on this date, terminal cash flow would be $\$10.50 + \$1,050.00 = \$1,060.50$.

### Example 2: TIPS Deflation Floor Protection
Consider the same TIPS bond as in Example 1, but assume severe deflation over the bond's life causes the terminal reference CPI to fall to $285.0$ at maturity.
Calculate the final cash flow received by the investor.

1. Compute the Index Ratio:
$$\text{Index Ratio} = \frac{285.0}{300.0} = 0.9500 \quad (95\%)$$
2. Compute the final coupon payment:
$$\text{Coupon} = 1.0\% \times (\$1,000 \times 0.95) = 1.0\% \times \$950.00 = \$9.50$$
3. Evaluate terminal principal redemption under the deflation floor:
$$\text{Principal} = \$1,000 \times \max(1.0, 0.9500) = \$1,000.00$$
4. Total terminal cash flow:
$$\text{Total} = \$9.50 + \$1,000.00 = \$1,009.50$$
Our reference implementation [`code/fi_inflation.py`](code/fi_inflation.py) verifies:
`tips_cash_flow(0.02, 1000.0, 0.95, is_maturity=True) == 1009.50`.
The deflation floor preserves full par value against cumulative deflation.

### Example 3: Breakeven Inflation Rate Calculation
A 10-year nominal Treasury bond trades at a yield of $4.25\%$, while a 10-year TIPS trades at a real yield of $1.85\%$.
Calculate the exact and approximate breakeven inflation rates.

1. Exact Fisher breakeven:
$$\text{BEIR}_{\text{exact}} = \frac{1 + y_{\text{nom}}}{1 + y_{\text{real}}} - 1 = \frac{1 + 0.0425}{1 + 0.0185} - 1 = \frac{1.0425}{1.0185} - 1 = 1.023564 - 1 = 2.3564\% \quad (235.64 \text{ bps})$$
2. Approximate breakeven:
$$\text{BEIR}_{\text{approx}} = y_{\text{nom}} - y_{\text{real}} = 4.25\% - 1.85\% = 2.4000\% \quad (240.00 \text{ bps})$$
Our reference implementation [`code/fi_inflation.py`](code/fi_inflation.py) yields:
`breakeven_inflation_rate(0.0425, 0.0185) == 0.023564`.
The approximation overstates the exact compound breakeven inflation rate by $4.36\text{ bps}$.

## Pitfalls

- **Ignoring the 3-month CPI indexation lag:** Using contemporaneous CPI to price daily TIPS accrual introduces mark-to-market tracking errors; pricing engines must interpolate historical CPI numbers from months $m-3$ and $m-2$.
- **Taxation of phantom income:** In taxable US accounts, annual upward principal adjustments on TIPS are taxed as ordinary income in the year they occur, even though the cash is locked until bond maturity.
- **Conflating Breakeven Inflation with Inflation Forecasts:** Assuming the TIPS breakeven rate is a pure forecast of future inflation ignores the inflation risk premium and the TIPS liquidity premium; during market liquidity squeezes, breakeven rates plummet due to liquidity discounts rather than deflation expectations.
- **Seasonality distortion in short-dated inflation:** Quoting 6-month or 1-year inflation forward rates without seasonal adjustment corrupts carry calculations, as non-seasonally adjusted CPI predictably peaks in early summer and dips in winter.
- **Pricing YoY swaps directly from ZCIS curves without convexity corrections:** Year-on-Year inflation swaps pay individual forward inflation rates, requiring convexity adjustments analogous to CMS adjustments due to the change of numeraire.

## Interview questions

> [!question]- fi-inflation-fisher-equation | State the exact and approximate Fisher equations for interest rates.
> Exact: $1 + y_{\text{nom}} = (1 + y_{\text{real}})(1 + \pi)$.
> Approximate: $y_{\text{nom}} \approx y_{\text{real}} + \pi$.
> The nominal rate equals the real rate plus inflation, plus a cross-product term $y_{\text{real}}\pi$ that is omitted in the linear approximation.

> [!question]- fi-inflation-index-ratio | How is the TIPS index ratio defined?
> $\text{Index Ratio}(t) = \frac{\text{Ref CPI}(t)}{\text{Base CPI}}$.
> It is the ratio of the interpolated 3-month lagged reference CPI for date $t$ to the baseline CPI fixed at the bond's original dated date.

> [!question]- fi-inflation-deflation-floor | What is the TIPS deflation floor and when is it valuable?
> The deflation floor guarantees that the redemption principal at maturity cannot fall below 100% of par: $\text{Redemption} = \text{Base Principal} \times \max(1.0, \text{Index Ratio}(T))$.
> It acts as a free European put option on the price index with strike equal to base CPI, becoming valuable in prolonged deflationary environments.

> [!question]- fi-inflation-breakeven-components | What economic components make up the Breakeven Inflation Rate (BEIR)?
> $\text{BEIR} = y_{\text{nom}} - y_{\text{real}} = \mathbb{E}[\pi] + \text{Inflation Risk Premium} - \text{TIPS Liquidity Premium}$.
> It reflects market expected inflation plus compensation for inflation volatility minus compensation for lower TIPS market liquidity.

> [!question]- fi-inflation-zcis-structure | Describe the cash flow structure of a Zero-Coupon Inflation Swap (ZCIS).
> A single net cash flow occurs at maturity $T$.
> One party pays realized cumulative inflation $(\text{CPI}(T)/\text{CPI}(0) - 1) \times N$, while the counterparty pays a fixed compounded rate $((1 + K)^T - 1) \times N$.

> [!question]- fi-inflation-lag-rationale | Why do TIPS use a 3-month indexation lag instead of contemporaneous CPI?
> Monthly CPI is published with a delay (roughly mid-month for the prior month) and is subject to revisions.
> The 3-month lag ensures that all parties know the exact coupon and settlement amounts well in advance of payment dates, eliminating settlement uncertainty.

> [!question]- fi-inflation-phantom-income | What is phantom income on TIPS and who is affected by it?
> Phantom income is the taxable inflation adjustment applied to the bond principal each year.
> In taxable retail or corporate accounts, investors must pay taxes on principal gains annually before any cash principal is disbursed.

> [!question]- fi-inflation-jy-model | What is the Jarrow-Yildirim (JY) model and what analogy does it use?
> The JY model is a 3-factor term structure model that treats inflation using a foreign-currency analogy.
> The nominal economy is the domestic currency, the real economy is the foreign currency, and the consumer price index acts as the exchange rate between the two.

> [!question]- fi-inflation-seasonality-impact | Why does CPI seasonality matter for inflation derivatives?
> Non-seasonally adjusted CPI predictably rises in the spring and falls in winter.
> Derivatives expiring at different months (e.g. 6-month vs 12-month contracts) will misprice relative value unless seasonal multipliers are removed from the baseline inflation curve.

> [!question]- fi-inflation-yoy-convexity | Why do Year-on-Year inflation swaps require a convexity adjustment?
> YoY swaps pay individual annual inflation increments on intermediate payment dates rather than compounding to a single terminal date.
> The change of numeraire between intermediate discount factors and the terminal measure induces a covariance term with interest rates.

## Further reading

- Damiano Brigo and Fabio Mercurio, *Interest Rate Models - Theory and Practice*, Chapter 18: "Inflation Models".
- Robert Jarrow and Yildiray Yildirim, *Pricing Treasury Inflation Protected Securities and Related Derivative Contracts Using an HJM Model*, The Journal of Financial and Quantitative Analysis, 2003.
- US Department of the Treasury, *TIPS: Treasury Inflation-Protected Securities - In Depth*, TreasuryDirect.
- Frank Fabozzi, *Handbook of Fixed Income Securities*, Chapter on Inflation-Indexed Bonds.

## In this repo and SDE-Interview-Prep

- Code: [`code/fi_inflation.py`](code/fi_inflation.py) (numerical verification of TIPS index ratio, deflation floor, and breakeven inflation), [`code/credit_bootstrap.py`](code/credit_bootstrap.py) (TIPS index ratio, deflation floor, and breakeven inflation rate).
- Prereqs: [Swaps and Curve Building](03-Swaps-and-Curve-Building.md), [Day Counts, Calendars and Schedules](11-Day-Counts-Calendars-and-Schedules.md).
- Next: [Mortgages and Securitized Products](22-Mortgages-and-Securitized-Products.md).
