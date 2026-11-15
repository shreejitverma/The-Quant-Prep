---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Brinson Hood and Beebower (1986) - Determinants of Portfolio Performance, Brinson Singer and Beebower (1991) - Determinants of Portfolio Performance II: An Update, Ibbotson and Kaplan (2000) - Does Asset Allocation Policy Explain 40 90 or 100 Percent of Performance?, Sharpe (1991) - The Arithmetic of Active Management, Bogle (2005) - The Relentless Rules of Humble Arithmetic, Ilmanen (2011) - Expected Returns, S&P Dow Jones Indices - SPIVA US Mid-Year 2025 Scorecard]
---

# Asset Allocation and The Benchmark to Beat

## TL;DR

- In the pension-plan studies of Brinson, Hood and Beebower (1986) and Brinson, Singer and Beebower (1991), the policy asset mix explained about 90% of the variation of a plan's quarterly returns over time.
- Ibbotson and Kaplan (2000) showed that this is a statement about time-series variation, not about why funds differ: policy explains about 40% of the differences in returns between funds and about 100% of the average return level.
- Sharpe's "Arithmetic of Active Management" (1991) is an accounting identity: before costs the average actively managed dollar earns the market return, so after costs it must earn less than the average passively managed dollar.
- A low-cost broad index fund is the benchmark a strategy has to beat after fees, costs and taxes, and as of June 2025 SPIVA reports that 88.29% of US large-cap funds lagged the S&P 500 over 15 years and 91.03% over 20 years.
- Strategic Asset Allocation (SAA) sets long-run policy weights from risk tolerance and liabilities; Tactical Asset Allocation (TAA) makes bounded tilts around them inside a tracking-error budget.
- Building-block expected returns (income yield plus growth plus inflation plus repricing, as used in Ilmanen 2011) turn valuation into a forecast that can be checked against a spending target.

## Learning objectives

- Prove William Sharpe's Arithmetic of Active Management and quantify the cumulative compounding drag of expense ratios and turnover.
- Analyze the Brinson, Singer, and Beebower empirical findings on the determinants of portfolio performance, and state precisely what they do and do not show.
- Construct a Strategic Asset Allocation (SAA) policy portfolio across global equities, government bonds, inflation-protected assets, and real estate.
- Deconstruct expected returns into income yield, real growth, inflation, and valuation multiple changes using a building-block framework.
- Formulate and test Tactical Asset Allocation (TAA) tilt models constrained by tracking error budgets.

## Core concepts

### 1. What the asset allocation studies actually measured

Brinson, Hood, and Beebower (1986) found that investment policy explained on average 93.6% of the variation in quarterly returns of 91 large US pension plans (1974-1983).
The 1991 update by Brinson, Singer, and Beebower studied 82 large US pension plans over December 1977 to December 1987 and reported, in its Figure G, the average R-squared of each plan's actual quarterly return on three constructed return series:

```
+-----------------------------------------------------------------------+
|     BRINSON, SINGER AND BEEBOWER (1991), FIGURE G: AVERAGE R-SQUARED  |
+-----------------------------------------------------------------------+
| Policy alone                                     91.5%                |
| Policy and active allocation (timing)            93.3%   (+1.8 pp)    |
| Policy and security selection                    96.1%   (+4.6 pp)    |
| Actual portfolio                                100.0%   (+2.1 pp     |
|                                                           residual)   |
+-----------------------------------------------------------------------+
```

The increments are differences of R-squared values, not shares of return, and they are not a decomposition the paper itself reports.
The same paper's Table III shows the average plan earning 13.41% a year against 13.49% for its policy benchmark, so active decisions cost 0.08 percentage points a year on average.

Ibbotson and Kaplan (2000) separated three questions that are often run together, using 10 years of monthly returns on 94 balanced mutual funds and 5 years of quarterly returns on 58 pension funds:

- **Across time:** policy explains about 90% of the variability of a fund's returns, which is the Brinson result.
- **Across funds:** policy explains only about 40% of the differences in returns between funds (about 35% for the pension sample).
- **Return level:** on average the policy return accounts for about 100% of the return level, because active management adds roughly nothing on average.

The practical lesson is narrower than the slogan: the policy mix sets most of a portfolio's risk and return path, so it deserves the most deliberate decision, but the 90% figure does not say that security selection cannot matter for one fund relative to another.

### 2. The Arithmetic of Active Management: Sharpe's Law

Sharpe (1991, Financial Analysts Journal 47(1)) gave the argument in three short pages:

```
+-----------------------------------------------------------------------+
|                    SHARPE'S ARITHMETIC                                |
+-----------------------------------------------------------------------+
| 1. The market is the value-weighted sum of all holdings.              |
| 2. A passive investor holds every security in market proportions,     |
|    so before costs passive dollars earn the market return.            |
| 3. Active dollars are the market minus the passive dollars, so as a   |
|    group they also hold the market and also earn the market return    |
|    before costs.                                                      |
| 4. Active management costs more (fees, trading, research).            |
|                                                                       |
| CONCLUSION: AFTER COSTS, THE AVERAGE ACTIVELY MANAGED DOLLAR MUST     |
| UNDERPERFORM THE AVERAGE PASSIVELY MANAGED DOLLAR.                    |
+-----------------------------------------------------------------------+
```

The identity holds for averages weighted by dollars over any period; it says nothing about whether a particular manager can outperform.

Over a 30-year horizon an annual fee of 1.5% does not reduce terminal wealth by 1.5%; it compounds:

$$\text{Share of terminal wealth lost} = 1 - \left( \frac{1 + R - \text{Fee}}{1 + R} \right)^T$$

With Fee = 1.5% and T = 30, the loss is at most $1 - 0.985^{30} = 36.5\%$ (the R = 0 limit), and it is 34.5% at a 7% gross return $R$, because a higher $R$ shrinks the fee as a fraction of $1 + R$.

### 3. John Bogle and the Low-Cost Index Benchmark

John C. Bogle, founder of The Vanguard Group, launched First Index Investment Trust, an S&P 500 index mutual fund for individual investors, on August 31, 1976 (it is now the Vanguard 500 Index Fund).
Bogle (2005, Financial Analysts Journal 61(6)) named the Cost Matters Hypothesis:

- Gross returns earned in the financial markets, minus the costs of financial intermediation, equal the net returns that investors actually receive.
- Investors do not need markets to be efficient for this to bite; they only need costs to be positive.

The empirical record is consistent with the arithmetic.
As of June 30, 2025, the SPIVA US Mid-Year 2025 Scorecard (Report 1a) shows that 88.29% of all US large-cap funds underperformed the S&P 500 over 15 years and 91.03% over 20 years, on absolute returns and with survivorship bias removed.

Any proprietary quantitative or discretionary strategy should be benchmarked against a low-cost passive index on the same risk.
In a hypothetical example, a strategy earning 9.5% gross with 2.0% of costs and taxes nets 7.5%, which loses to an index fund earning 9.0% for a 0.03% fee, which nets 8.97%.

### 4. Strategic (SAA) vs Tactical (TAA) Asset Allocation

Modern portfolio management decouples asset allocation into two operational horizons.
The ranges in the table are illustrative policy choices, not market conventions:

```
+-----------------------------------------------------------------------+
|                    SAA VS TAA FRAMEWORK MATRIX                        |
+--------------------+---------------------------+----------------------+
| Dimension          | Strategic Asset Allocation| Tactical Allocation  |
+--------------------+---------------------------+----------------------+
| Time Horizon       | Long-Term (10 to 30 years)| Short-Term (1 to 12m)|
| Primary Driver     | Investor risk tolerance,  | Relative asset class |
|                    | time horizon, liabilities | valuation, macro skew|
| Target Benchmark   | Fixed policy portfolio    | Dynamic overlay      |
|                    | (e.g. 60% Eq / 40% Bonds) | around policy weights|
| Permissible Bands  | Hard rebalancing bands    | Bounded tilt limits  |
|                    | (e.g. +/- 5% corridor)    | (e.g. +/- 3% to 10%) |
| Alpha Objective    | Zero (Beta capture)       | Positive active alpha|
+--------------------+---------------------------+----------------------+
```

### 5. Building-Block Expected Returns

Ilmanen (2011) estimates forward-looking returns by adding up simple, observable components rather than extrapolating past returns.
A common building-block form is:

```
+-----------------------------------------------------------------------+
|                    EXPECTED RETURN BUILDING BLOCKS                    |
+-----------------------------------------------------------------------+
| EXPECTED RETURN = Income Yield + Real Growth + Inflation              |
|                   +/- Valuation Multiple Change                       |
+-----------------------------------------------------------------------+
```

1. **Equities Expected Return**:
   $$E[R_{\text{equity}}] = \text{Dividend Yield} + \text{Real Earnings Growth Rate} + \text{Expected Inflation} + \Delta \text{Valuation Multiple (P/E)}$$
2. **Fixed Income Expected Return**:
   $$E[R_{\text{bond}}] = \text{Initial Yield to Maturity (YTM)} + \text{Roll-Down Return} - \text{Expected Credit Default Losses}$$
3. **Real Estate / Real Assets**:
   $$E[R_{\text{real}}] = \text{Net Operating Income Yield (Cap Rate)} + \text{Inflation Growth} + \text{Real Value Appreciation}$$

Valuation multiple mean reversion:
In a hypothetical example, if an index trades at a Shiller CAPE of 36 and you assume it reverts to 18 over 10 years, the repricing term is $(18/36)^{1/10} - 1 = -6.70\%$ a year.
Assuming only a partial reversion to 30 gives $(30/36)^{1/10} - 1 = -1.81\%$ a year, so the forecast is dominated by the assumed end multiple.

## Worked numerical case study

Evaluate a long-term portfolio allocation for an endowment foundation (all inputs are hypothetical):
- Total Capital: $100.0M
- Investment Horizon: Perpetual (30+ years)
- Required Annual Spending Distribution: 4.5% net of all fees and inflation
- Expected Long-Term Inflation: 2.5%
- Required Nominal Return Target: $4.5\% + 2.5\% = \mathbf{7.0\% \text{ per annum}}$ (the additive approximation; compounding gives $1.045 \times 1.025 - 1 = 7.1125\%$)

### Building-block estimates (10-year forward horizon, hypothetical):
- Global Equities: Dividend Yield 2.2% + Real Earnings Growth 2.0% + Inflation 2.5% + Valuation Drag -0.7% = **6.0% Expected Nominal Return** ($\sigma = 16.0\%$).
- US Intermediate Treasuries: YTM = **4.2% Expected Nominal Return** ($\sigma = 5.5\%$).
- Treasury Inflation-Protected Securities (TIPS): Real Yield 2.0% + Inflation 2.5% = **4.5% Expected Nominal Return** ($\sigma = 6.0\%$).
- Real Estate (Global REITs): Cap Rate 5.0% + Real Growth 1.0% + Inflation 2.5% = **8.5% Expected Nominal Return** ($\sigma = 18.0\%$).

### Portfolio Candidates:
1. **Traditional 60/40 Portfolio**:
   - 60% Global Equities, 40% Treasuries.
   - Expected Return: $(0.60 \times 6.0\%) + (0.40 \times 4.2\%) = 3.60\% + 1.68\% = \mathbf{5.28\%}$.
   - Result: **Fails the 7.0% target** by 1.72% annually; spending will erode purchasing power.
2. **Diversified Real-Asset SAA Portfolio**:
   - 50% Global Equities ($0.50 \times 6.0\% = 3.00\%$)
   - 20% Global Real Estate / Infrastructure ($0.20 \times 8.5\% = 1.70\%$)
   - 15% TIPS ($0.15 \times 4.5\% = 0.675\%$)
   - 15% Intermediate Treasuries ($0.15 \times 4.2\% = 0.63\%$)
   - Gross Expected Return: $3.00\% + 1.70\% + 0.675\% + 0.63\% = \mathbf{6.005\%}$, still 0.995% short of the target.
   - Gap: with these inputs, traditional asset classes do not deliver 7.0% nominal when the starting bond yield is 4.2% and the equity estimate includes a valuation drag.

### The Decision Engineering Solution:
The endowment cannot meet its 7.0% mandate with these inputs without either:
1. Lowering its spending distribution from 4.5% to 3.5%, which lowers the additive target to 6.0%;
2. Adding return sources with their own evidence and risks, such as systematic factor premiums (see the factor note); or
3. Using modest leverage on a risk-balanced portfolio (see the risk parity note) rather than concentrating in equity beta.

## Practice questions

> [!question]- mkt-pf-001 | What percentage of the long-term variability in portfolio returns is explained by Strategic Asset Allocation (SAA)?
> About 90% of the variation of a plan's own returns over time: 93.6% in Brinson, Hood, and Beebower (1986) and 91.5% in Brinson, Singer, and Beebower (1991).
> Ibbotson and Kaplan (2000) showed that policy explains only about 40% of the differences in returns between funds, so the 90% figure is about time-series variation, not about cross-fund performance.

> [!question]- mkt-pf-002 | What is William Sharpe's 'Arithmetic of Active Management'?
> Before costs, the return on the average actively managed dollar equals the return on the average passively managed dollar (the market); after costs, the average active dollar must therefore underperform the average passive dollar.

> [!question]- mkt-pf-003 | Why does a 1.5% annual management fee reduce 30-year terminal wealth by far more than 1.5%?
> Fees compound; over 30 years a 1.5% fee removes 1 - ((1 + R - 0.015) / (1 + R))^30 of terminal wealth, which is 34.5% at a 7% gross return and at most 36.5% (the R = 0 limit).

> [!question]- mkt-pf-004 | What is the Cost Matters Hypothesis (CMH) formulated by John Bogle?
> Gross market returns minus the costs of financial intermediation equal the net returns investors receive (Bogle 2005, Financial Analysts Journal).
> Because investors as a group earn the market before costs, lower costs are the one return advantage an investor fully controls.

> [!question]- mkt-pf-005 | What is Strategic Asset Allocation (SAA)?
> Establishing target portfolio weights across asset classes designed to achieve long-term financial goals anchored in risk tolerance and liability matching.

> [!question]- mkt-pf-006 | What is Tactical Asset Allocation (TAA)?
> Making temporary, bounded tilts around strategic policy weights to exploit short-term valuation mispricings or macroeconomic risk skews.

> [!question]- mkt-pf-007 | What are the four core building blocks of Antti Ilmanen's expected return framework?
> Income yield, real growth, inflation, and the change in the valuation multiple (repricing); bonds swap growth for roll-down and default losses.

> [!question]- mkt-pf-008 | What is the equity building-block expected return equation?
> E[R] = Dividend Yield + Real Earnings Growth + Inflation +/- Multiple Mean Reversion.

> [!question]- mkt-pf-009 | What is the primary determinant of long-term government bond expected returns?
> The initial starting Yield to Maturity (YTM) at the time of purchase.

> [!question]- mkt-pf-010 | What is the Shiller CAPE ratio and how does it affect 10-year equity expected returns?
> Price divided by the 10-year average of inflation-adjusted earnings; a high CAPE lowers a building-block forecast through an assumed multiple contraction, e.g. 36 to 18 over 10 years is -6.70% a year, so the forecast depends heavily on the assumed end multiple.

> [!question]- mkt-pf-011 | What is the classic 60/40 portfolio?
> A balanced portfolio allocating 60% to diversified equities (growth engine) and 40% to investment-grade government bonds (deflation hedge and income).

> [!question]- mkt-pf-012 | Why does the 60/40 portfolio carry unbalanced risk?
> Equities are far more volatile than bonds; with hypothetical volatilities of 16% and 5% (a ratio of 3.2), equities contribute 95.8% of portfolio variance at zero correlation, 88.2% at a correlation of 0.5 and 99.8% at -0.2.

> [!question]- mkt-pf-013 | What are Treasury Inflation-Protected Securities (TIPS)?
> US Treasury bonds whose principal is indexed to the CPI-U, so a TIPS held to maturity locks in its real yield at purchase (with par protected against deflation at maturity).

> [!question]- mkt-pf-014 | What is the 'equity risk premium puzzle' (Mehra and Prescott 1985)?
> Historical equity returns were so high relative to bonds that standard neoclassical economic models cannot explain them without assuming implausibly high risk aversion.

> [!question]- mkt-pf-015 | What is the difference between home country bias and global asset allocation?
> Home country bias is disproportionately overweighting domestic equities; global allocation diversifies across worldwide market-capitalization weights.

> [!question]- mkt-pf-016 | What is tracking error in portfolio management?
> The standard deviation of the difference between portfolio returns and benchmark returns, measuring the volatility of active bets.

> [!question]- mkt-pf-017 | Why do active fund managers suffer from 'closet indexing'?
> To minimize tracking error and avoid career risk, managers hold portfolios that mimic the benchmark while charging active management fees.

> [!question]- mkt-pf-018 | What is the 'rebalancing bonus' in an uncorrelated asset allocation?
> The extra growth of a rebalanced portfolio over the weighted average of its assets' own growth rates; for two assets it is about 0.5 w1 w2 (sigma1^2 + sigma2^2 - 2 sigma12), derived in the rebalancing note.

> [!question]- mkt-pf-019 | How does asset allocation differ for defined benefit pensions versus individual retirees?
> Pensions focus on liability-driven investing (matching asset duration to pensioner payouts); individuals manage sequence of returns risk and personal lifespan.

> [!question]- mkt-pf-020 | What is the 'endowment model' pioneered by David Swensen at Yale?
> Shifting away from public equities and fixed income into illiquid, alternative assets: private equity, venture capital, real estate, and timberland.

> [!question]- mkt-pf-021 | What is the primary liquidity risk of the Yale Endowment model?
> Private assets are illiquid with multi-year capital calls; during market crises, endowments face cash crunches and can sell private stakes only at deep discounts.

> [!question]- mkt-pf-022 | What is cash drag in a rising bull market?
> The performance underperformance caused by holding uninvested cash when risky assets appreciate at high rates.

> [!question]- mkt-pf-023 | What is a glide path in target-date retirement funds?
> The predetermined asset allocation schedule that automatically shifts from high equity allocations in youth to conservative bond allocations near retirement.

> [!question]- mkt-pf-024 | What is duration in fixed income asset allocation?
> A measure of the sensitivity of bond prices to changes in interest rates, representing the weighted average time until cash flows are received.

> [!question]- mkt-pf-025 | Why do commodities provide diversification benefits in an equity portfolio?
> Gorton and Rouwenhorst (2006, Financial Analysts Journal) found commodity futures returns positively correlated with inflation and unexpected inflation and negatively correlated with stock and bond returns, so they tend to help in the inflationary episodes that hurt both.

> [!question]- mkt-pf-026 | What is the difference between real returns and nominal returns?
> Real returns are adjusted for inflation, representing the actual expansion of economic purchasing power; nominal returns ignore inflation.

> [!question]- mkt-pf-027 | What was the performance failure rate of active equity managers over 20-year horizons?
> As of June 30, 2025, SPIVA (US Mid-Year 2025, Report 1a) reports that 91.03% of US large-cap funds underperformed the S&P 500 over 20 years, and 88.29% over 15 years.

> [!question]- mkt-pf-028 | How should an analyst establish a benchmark for an unconstrained multi-strategy fund?
> Use a blended benchmark of global equities, bonds, and cash matching the fund's historical average beta and factor exposures.

> [!question]- mkt-pf-029 | What is the role of currency risk in international equity asset allocation?
> Currency fluctuations can amplify or mute foreign equity returns; unhedged currency exposure adds volatility but can provide macro diversification.

> [!question]- mkt-pf-030 | What is survivor bias in mutual fund performance databases?
> Poorly performing active funds are liquidated or merged into sister funds, leaving only successful funds in historical databases and overstating average active returns.

> [!question]- mkt-pf-031 | What is an Investment Policy Statement (IPS)?
> The foundational governance document outlining an investor's return objectives, risk tolerance, liquidity constraints, tax status, and permissible asset allocations.

> [!question]- mkt-pf-032 | What is the ultimate takeaway of modern asset allocation theory?
> Get the top-level asset allocation right, minimize investment fees and taxes, and enforce disciplined rebalancing before pursuing active alpha.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_pm_01_asset_allocation.py`](../../code/mkt_pm_01_asset_allocation.py) prints and asserts every computed number on this page: the Brinson, Singer and Beebower increments from the published R-squared values in exact decimals, fee drag by compounding both wealth paths year by year in exact rationals against the closed form, the case-study sums in exact fractions against floating-point dot products, the CAPE drag by bisection against the closed-form root, and the 60/40 equity variance share from Euler contributions against a finite-difference gradient and a seeded simulation with batch standard errors.
- Related notes: [Portfolio Rebalancing, Tax Drag, and Execution Friction](03-Portfolio-Rebalancing-Tax-Drag-and-Execution-Friction.md) (the rebalancing bonus), [Risk Parity and The All-Weather Framework](06-Risk-Parity-and-The-All-Weather-Framework.md) (the 60/40 risk concentration in full).

## Further reading

- Bogle, J. C. (2005). *The Relentless Rules of Humble Arithmetic*. Financial Analysts Journal, 61(6), 22-35.
- Bogle, J. C. (2007). *The Little Book of Common Sense Investing*. John Wiley & Sons.
- Brinson, G. P., Hood, L. R., & Beebower, G. L. (1986). *Determinants of Portfolio Performance*. Financial Analysts Journal, 42(4), 39-44.
- Brinson, G. P., Singer, B. D., & Beebower, G. L. (1991). *Determinants of Portfolio Performance II: An Update*. Financial Analysts Journal, 47(3), 40-48 (Figure G and Table III).
- Gorton, G., & Rouwenhorst, K. G. (2006). *Facts and Fantasies about Commodity Futures*. Financial Analysts Journal, 62(2), 47-68.
- Ibbotson, R. G., & Kaplan, P. D. (2000). *Does Asset Allocation Policy Explain 40, 90, or 100 Percent of Performance?* Financial Analysts Journal, 56(1), 26-33.
- Ilmanen, A. (2011). *Expected Returns: An Investor's Guide to Harvesting Market Rewards*. John Wiley & Sons.
- Mehra, R., & Prescott, E. C. (1985). *The Equity Premium: A Puzzle*. Journal of Monetary Economics, 15(2), 145-161.
- S&P Dow Jones Indices (2025). *SPIVA U.S. Mid-Year 2025 Scorecard*, Report 1a (data as of June 30, 2025).
- Sharpe, W. F. (1991). *The Arithmetic of Active Management*. Financial Analysts Journal, 47(1), 7-9.
