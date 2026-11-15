---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Barroso and Santa-Clara (2015) - Momentum Has Its Moments - Journal of Financial Economics 116(1), Engle (1982) - Autoregressive Conditional Heteroscedasticity - Econometrica 50(4), Garman and Klass (1980) - On the Estimation of Security Price Volatilities from Historical Data - Journal of Business 53(1), Harvey Hoyle Korgaonkar Rattray Sargaison and Van Hemert (2018) - The Impact of Volatility Targeting - Journal of Portfolio Management 45(1), Moreira and Muir (2017) - Volatility-Managed Portfolios - Journal of Finance 72(4), Parkinson (1980) - The Extreme Value Method for Estimating the Variance of the Rate of Return - Journal of Business 53(1), Rogers and Satchell (1991) - Estimating Variance from High Low and Closing Prices - Annals of Applied Probability 1(4), Yang and Zhang (2000) - Drift-Independent Volatility Estimation Based on High Low Open and Close Prices - Journal of Business 73(3), Bollerslev (1986) - Generalized Autoregressive Conditional Heteroskedasticity - Journal of Econometrics 31(3), Black (1976) - Studies of Stock Price Volatility Changes - Proceedings of the American Statistical Association]
---

# Volatility Targeting and Dynamic Leverage

## TL;DR

- Volatility targeting dynamically scales portfolio gross exposure inversely to forecast volatility, aiming at a constant level of risk over time.
- By scaling down exposure during high-volatility regimes and scaling up during calm regimes, volatility targeting exploits volatility clustering (Engle 1982).
- Harvey et al. (2018) find that volatility targeting raises Sharpe ratios for risk assets (equities and credit) but has a negligible effect for bonds, currencies and commodities, while reducing extreme returns across all 60+ assets they study; Moreira and Muir (2017) find higher Sharpe ratios for variance-managed equity and factor portfolios.
- Realized volatility estimators range from standard close-to-close rolling standard deviations to high-efficiency range estimators (Parkinson, Garman-Klass).
- Dynamic leverage requires strict maximum leverage caps ($L_{\max}$), cash collateral buffers, and explicit accounting for financing rate spreads.
- Systematic risk governors can add automated drawdown circuit breakers that cut risk at predefined drawdown tiers and halt trading at a terminal stop level.

## Learning objectives

- Formulate the mathematical mechanics of volatility-targeted exposure scaling.
- Understand the statistical foundation: volatility clustering (ARCH) and the weak link between volatility and future expected returns.
- Compare the efficiency of Close-to-Close, Parkinson, and Garman-Klass volatility estimators.
- Calculate margin requirements, cash buffer thresholds, and financing costs under dynamic leverage.
- Design multi-tiered systematic drawdown governors and circuit breaker protocols.

## Core concepts

### 1. The Volatility Targeting Framework

Standard static-weight portfolios experience wild fluctuations in risk.
During market panics (e.g. the 2008 crisis after Lehman's failure, March 2020), equity volatility rises to several times its calm level, so a static portfolio's risk rises with it.
Conversely, during calm markets, volatility falls well below average, leaving the risk budget underused.

Volatility targeting stabilizes portfolio risk by dynamically adjusting gross exposure $k_t$:

$$w_{i, t}^* = w_{i, t} \cdot k_t$$

$$k_t = \min\left( L_{\max}, \frac{\sigma_{\text{target}}}{\hat{\sigma}_t} \right)$$

Where:
- $\sigma_{\text{target}}$: Predetermined annualized target volatility (e.g. $10.0\%$ or $12.0\%$).
- $\hat{\sigma}_t$: Forecast of annualized portfolio volatility at timestamp $t$, using only data available at $t$.
- $L_{\max}$: Maximum allowable leverage cap (e.g. $2.0\times$ or $3.0\times$) to prevent excessive leverage during very calm markets.

Moreira and Muir (2017) scale by the inverse of last month's realized variance instead, $f^{\sigma}_{t+1} = \frac{c}{\hat{\sigma}^2_t} f_{t+1}$, with $c$ chosen so the managed portfolio has the same unconditional volatility as the original; Harvey et al. (2018) scale by inverse volatility as above.

```
Market Regime:      [ Calm / Bull Market ]       [ Volatility Spike / Crisis ]
Realized Vol:                 8%                                 40%
Target Vol:                  10%                                 10%
Multiplier k_t:         10 / 8 = 1.25x                      10 / 40 = 0.25x
Gross Exposure:             125%                                 25%
Portfolio Action:      Modest Leverage                  Aggressive De-risking
```

### 2. Statistical Foundation: Volatility Clustering and the Leverage Effect

Why can volatility targeting raise risk-adjusted returns rather than simply dampening risk?

The argument rests on two properties:
1. **Volatility Clustering (Mandelbrot 1963, Engle 1982)**:
   High-volatility days tend to be followed by high-volatility days, and low-volatility days by low-volatility days.
   Because volatility is forecastable with GARCH or EWMA models, a fund can scale down exposure early in a persistent high-volatility episode.
2. **The Risk-Return Disconnect (Moreira and Muir 2017)**:
   For the equity market and many factors, expected returns do not rise in proportion to variance when volatility rises.
   Then scaling down when volatility is high gives up little expected return per unit of risk removed, so the Sharpe ratio rises; Example 3 isolates this effect.
3. **The Leverage Effect (Black 1976)**:
   Equity volatility tends to rise after prices fall, so scaling down after volatility rises behaves partly like a trend-following rule; Harvey et al. (2018) give this as a reason the gains concentrate in risk assets.

### 3. Estimating Realized Volatility: Efficiency Comparison

The accuracy of the scaling factor $k_t$ depends directly on the volatility estimator:

```
+-----------------------------------------------------------------------+
|                    REALIZED VOLATILITY ESTIMATORS                     |
+-----------------------------------------------------------------------+
| ESTIMATOR          | DATA USED       | RELATIVE EFFICIENCY (vs C-to-C)|
+--------------------+-----------------+--------------------------------+
| Close-to-Close     | Close prices    | 1.0 (Baseline)                 |
| Parkinson (1980)   | High, Low       | 4.91 (exact)                   |
| Garman-Klass (1980)| Open, High, Low,| about 7.4                      |
|                    | Close           |                                |
| Rogers-Satchell    | Open, High, Low,| about 6.0 (robust to drift)    |
| (1991)             | Close           |                                |
+-----------------------------------------------------------------------+
```

Efficiency is the variance ratio $\text{Var}(r^2)/\text{Var}(\hat{\sigma}^2)$ for one day of driftless Brownian motion with no overnight gap.
Parkinson's value is exact from the range moments $E[R^2] = 4 \ln 2 \, \sigma^2$ and $E[R^4] = 9\zeta(3)\sigma^4$; the other two are by seeded simulation in the script.
Real data has opening gaps and discrete trading, which lower all range-based efficiencies.

1. **Standard Close-to-Close Exponentially Weighted Moving Average (EWMA)**:
   $$\sigma_t^2 = \lambda \sigma_{t-1}^2 + (1 - \lambda) r_{t-1}^2 \quad (\text{RiskMetrics } \lambda = 0.94)$$
2. **Parkinson High-Low Estimator (1980)**:
   Uses the intraday high and low, giving $4.91$ times the efficiency of squared close-to-close returns:
   $$\sigma_{\text{Parkinson}}^2 = \frac{1}{4 \ln(2) N} \sum_{i=1}^N \left( \ln\left(\frac{H_i}{L_i}\right) \right)^2$$
3. **Garman-Klass Estimator (1980)**:
   Combines the intraday range with the open-to-close return, giving about $7.4$ times the efficiency of squared close-to-close returns (it does not handle the overnight gap; Yang and Zhang 2000 add it):
   $$\sigma_{\text{GK}}^2 = \frac{1}{N} \sum_{i=1}^N \left[ 0.5 \left(\ln\frac{H_i}{L_i}\right)^2 - (2\ln 2 - 1)\left(\ln\frac{C_i}{O_i}\right)^2 \right]$$

### 4. Leverage Constraints, Margin, and Financing Spreads

Dynamic leverage introduces financing frictions that must be modeled:
- **Cash Collateral Buffer**: A levered fund holds unencumbered cash to meet variation margin calls without forced liquidation; size it from stressed margin scenarios rather than a fixed percentage.
- **Financing Cost Drag**: Borrowed capital incurs borrowing interest:
  $$\text{Financing Cost} = \max(0, \text{Gross Exposure} - 1.0) \times (r_{\text{benchmark}} + \text{Spread})$$
  At a hypothetical $5\%$ benchmark rate plus spread, each unit of leverage above $1.0$ costs more than $5\%$ a year, which can exceed the excess return it buys.
- **Margin Haircuts**: Prime brokers adjust initial margin requirements dynamically during stressed conditions, creating liquidity squeezes for highly levered strategies.

### 5. Multi-Tiered Systematic Drawdown Governors

Even with volatility targeting, sudden market gap openings (e.g. weekend geopolitical shocks or overnight earnings crashes) can breach risk limits.
Systematic trading systems can layer **Drawdown Governors** (step-down position governors) over portfolio optimizers; the tiers below are an illustrative design, not a standard:

```
+-----------------------------------------------------------------------+
|                    SYSTEMATIC DRAWDOWN GOVERNOR TIERS                 |
+-----------------------------------------------------------------------+
| DRAWDOWN FROM PEAK  | SYSTEMATIC ACTION                               |
+---------------------+-------------------------------------------------+
| 0.0% to 4.9%        | Normal Operations (100% Target Volatility)      |
| 5.0% to 7.4%        | Tier 1 Warning: Reduce Target Vol by 25%        |
| 7.5% to 9.9%        | Tier 2 Throttle: Cut Gross Exposure by 50%      |
| >= 10.0%            | Tier 3 Circuit Breaker: Flatten 100% to Cash;   |
|                     | Lock Trading Engine pending post-mortem audit   |
+-----------------------------------------------------------------------+
```

Reset rules must be strictly defined: the governor does not re-engage full leverage upon a 1-day bounce.
It requires a sustained recovery above drawdown thresholds or a minimum cooling-off period (e.g. 10 trading days) to avoid "whipsaw de-risking".

---

## Worked examples

### Example 1: Dynamic Exposure Sizing Across Market Regimes

A systematic trend-following CTA targets an annualized portfolio volatility of $\sigma_{\text{target}} = 12.0\%$, with maximum leverage cap $L_{\max} = 2.50\times$.
Unlevered portfolio baseline capital is $\$10,000,000$.

Evaluate portfolio sizing across three market environments:
1. **Calm Environment (Bull Market)**:
   - Rolling realized volatility: $\hat{\sigma}_t = 6.0\%$.
   - Sizing Multiplier:
     $$k_t = \min\left(2.50, \frac{12.0\%}{6.0\%}\right) = \min(2.50, 2.00) = 2.00\times$$
   - Target Gross Exposure: $2.00 \times \$10,000,000 = \$20,000,000$.
2. **Elevated Volatility (Correction)**:
   - Rolling realized volatility: $\hat{\sigma}_t = 16.0\%$.
   - Sizing Multiplier:
     $$k_t = \min\left(2.50, \frac{12.0\%}{16.0\%}\right) = 0.75\times$$
   - Target Gross Exposure: $0.75 \times \$10,000,000 = \$7,500,000$.
3. **Severe Panic (Market Shock)**:
   - Rolling realized volatility: $\hat{\sigma}_t = 48.0\%$.
   - Sizing Multiplier:
     $$k_t = \min\left(2.50, \frac{12.0\%}{48.0\%}\right) = 0.25\times$$
   - Target Gross Exposure: $0.25 \times \$10,000,000 = \$2,500,000$.

By reducing exposure from $\$20\text{M}$ to $\$2.5\text{M}$ as volatility rises from $6\%$ to $48\%$, the portfolio keeps its forecast risk at the $12\%$ target, provided the volatility forecast is right and the trades can be executed.

### Example 2: Garman-Klass Volatility Calculation

A stock registers the following prices on Day $t$:
- Open ($O$): $\$100.00$
- High ($H$): $\$104.00$
- Low ($L$): $\$98.00$
- Close ($C$): $\$102.00$

1. **Calculate Log Ratios**:
   $$\ln\left(\frac{H}{L}\right) = \ln\left(\frac{104}{98}\right) = \ln(1.06122) = 0.05942$$
   $$\ln\left(\frac{C}{O}\right) = \ln\left(\frac{102}{100}\right) = \ln(1.02000) = 0.01980$$
2. **Compute Garman-Klass Daily Variance**:
   $$\sigma_{\text{GK}}^2 = 0.5 \times (0.05942)^2 - (2\ln 2 - 1) \times (0.01980)^2$$
   $$\sigma_{\text{GK}}^2 = 0.5 \times 0.003531 - (2 \times 0.69315 - 1) \times 0.0003921$$
   $$\sigma_{\text{GK}}^2 = 0.0017656 - (0.38629 \times 0.0003921) = 0.0017656 - 0.0001515 = 0.0016141$$
3. **Daily and Annualized Volatility**:
   $$\sigma_{\text{daily}} = \sqrt{0.0016141} = 0.04018 \quad (4.02\%)$$
   $$\sigma_{\text{ann}} = 0.04018 \times \sqrt{252} = 0.04018 \times 15.8745 = 63.8\%$$

Garman-Klass captures the wide intraday range ($H/L = 1.061$) even though the open-to-close change was only $+2.0\%$.

### Example 3: Why Volatility Management Can Raise the Sharpe Ratio

A hypothetical asset has a constant expected return of $0.5\%$ a month, and each month is calm ($\sigma = 2\%$) or turbulent ($\sigma = 6\%$) with equal probability, known at the start of the month (normal shocks within a month).
- Unmanaged (weight 1): annualized Sharpe ratio $0.39$, monthly return kurtosis $4.92$.
- Volatility-targeted (weight $\propto 1/\sigma$): Sharpe $0.58$, kurtosis $3.00$.
- Variance-managed as in Moreira and Muir (weight $\propto 1/\sigma^2$): Sharpe $0.64$.

Now change one thing: make the expected return proportional to variance (same average, $0.5\%$), so turbulent months pay for their risk.
The unmanaged Sharpe ratio stays $0.39$, but the variance-managed one falls to $0.23$.
The gain comes entirely from expected returns not keeping pace with variance, which is the empirical finding of Moreira and Muir, not from volatility targeting as such; the script computes these values exactly from Gaussian moments and checks two of them by simulation.

---

## Pitfalls

- **Lagged Volatility Reaction**: Using a simple 60-day moving average of volatility; by the time the moving average recognizes a crash, the drawdown has already occurred.
- **Uncapped Leverage During Volatility Deserts**: Allowing $k_t$ to float without a hard cap $L_{\max}$; when volatility drops to $4\%$, an uncapped system with a $12\%$ target takes $3.0\times$ leverage, creating large exposure if volatility jumps.
- **Ignoring Financing Costs at Elevated Rates**: Failing to incorporate short-term borrow rates; paying $6.0\%$ financing to lever an asset with a $7.0\%$ expected return leaves $1.0\%$ of expected return per unit of leverage, while adding the asset's full volatility (hypothetical rates).
- **Whipsaw De-risking**: De-leveraging at the exact bottom of a crash when volatility peaks, and failing to re-lever in time to capture the sharp V-shaped recovery.
- **Liquidity Illusion in Real-Time Scaling**: Assuming that a fund can scale down $\$500\text{M}$ of gross exposure within minutes during a volatility spike without incurring massive market impact.

---

## Interview questions

> [!question]- mkt-sys-193 | What is volatility targeting in systematic portfolio management?
> Volatility targeting dynamically scales portfolio gross exposure inversely to rolling realized volatility to maintain constant annualized risk over time: k_t = min(L_max, sigma_target / sigma_hat_t).

> [!question]- mkt-sys-194 | What econometric property provides the foundation for volatility targeting?
> Volatility clustering (Engle 1982), where high-volatility periods persist, allowing models to forecast upcoming risk and proactively de-risk before drawdowns compound.

> [!question]- mkt-sys-195 | Why does volatility targeting improve Sharpe ratio and compress tail risk (Moreira & Muir 2017)?
> Because, empirically, expected returns do not rise in proportion to variance when volatility rises; scaling down in high-volatility periods removes more risk than return.
> In a two-regime model with a constant mean the variance-managed Sharpe ratio rises from 0.39 to 0.64, but if the mean were proportional to variance it would fall to 0.23.

> [!question]- mkt-sys-196 | Why is a maximum leverage cap L_max essential in volatility targeting?
> To prevent excessive over-leveraging during extreme market lulls (volatility deserts) that would leave the portfolio vulnerable to flash crashes or sudden volatility spikes.

> [!question]- mkt-sys-197 | What is the relative statistical efficiency of the Parkinson (1980) volatility estimator?
> 4.91 times squared close-to-close returns for driftless Brownian motion, exactly from the range moments: Var = (9 zeta(3) / (4 ln 2)^2 - 1) sigma^4 = 0.4073 sigma^4 against 2 sigma^4.
> It uses the intraday high and low; real data with gaps and discrete trading does worse.

> [!question]- mkt-sys-198 | What is the relative efficiency of the Garman-Klass (1980) volatility estimator?
> About 7.4 times squared close-to-close returns for driftless Brownian motion, because it combines the intraday range with the open-to-close return.
> It does not include the overnight (close-to-open) gap, which must be added separately.

> [!question]- mkt-sys-199 | How does the RiskMetrics EWMA volatility model calculate rolling variance?
> Using exponential decay: sigma_t^2 = lambda * sigma_{t-1}^2 + (1 - lambda) * r_{t-1}^2, typically with decay factor lambda = 0.94 for daily returns.

> [!question]- mkt-sys-200 | What is a systematic drawdown governor?
> A rule-based risk control system that automatically reduces target volatility or cuts gross exposure by predefined percentages when peak-to-trough drawdowns breach specific tiers.

> [!question]- mkt-sys-201 | What is the risk of whipsaw de-risking in volatility-targeted systems?
> Selling assets into liquidity vacuums as volatility spikes at the bottom of a panic, then lagging to re-enter, missing the high-return initial recovery phase.

> [!question]- mkt-sys-202 | How do rising financing benchmark rates affect leveraged volatility-targeted portfolios?
> Leverage requires borrowing cash; higher financing rates directly widen borrowing drag: Cost = max(0, Exposure - 1) * (r_f + spread), eating into net excess returns.

> [!question]- mkt-sys-203 | What is an unencumbered cash buffer and why is it maintained?
> Liquid cash capital held uncommitted to margin to satisfy prime broker variation margin calls during market moves without forcing emergency asset liquidations.

> [!question]- mkt-sys-204 | What is the leverage effect (Black 1976) in equity markets?
> The negative correlation between stock returns and subsequent volatility.
> Black (1976) proposed financial leverage as one explanation: a falling share price raises debt-to-equity and so equity volatility; the effect is larger than leverage alone explains.

> [!question]- mkt-sys-205 | How does volatility targeting affect portfolio return kurtosis?
> When volatility is forecastable, it reduces kurtosis by removing the mixing of calm and turbulent periods.
> In the two-regime example kurtosis falls from 4.92 to 3.00; Harvey et al. (2018) find it reduces extreme returns across their 60+ assets, but surprise jumps remain.

> [!question]- mkt-sys-206 | What is the Rogers-Satchell volatility estimator?
> sigma^2 = ln(H/C) ln(H/O) + ln(L/C) ln(L/O) (Rogers and Satchell 1991): unbiased whatever the drift, so it suits trending markets.
> Its efficiency is about 6.0 for driftless Brownian motion, below Garman-Klass's 7.4.

> [!question]- mkt-sys-207 | Why does cross-asset trend following (CTA) rely heavily on volatility targeting?
> Because commodities, FX, rates, and equities have very different volatilities; scaling each position inversely to its volatility gives each contract a similar standalone risk (Moskowitz, Ooi and Pedersen 2012 scale by ex-ante volatility).

> [!question]- mkt-sys-208 | What is margin call contagion in multi-strategy funds?
> When a spike in volatility on one asset forces margin calls that require liquidating completely unrelated, profitable positions to raise required cash.

> [!question]- mkt-sys-209 | What is the difference between slow vol lookbacks and fast vol lookbacks?
> Fast lookbacks (e.g. 10-day EWMA) react immediately to emerging crises but induce high turnover and whipsaw; slow lookbacks (e.g. 60-day) are stable but lag market shocks.

> [!question]- mkt-sys-210 | How can a hybrid volatility estimator combine fast and slow lookbacks?
> By defining estimated volatility as the maximum of a fast-reacting short-term estimate and a stable long-term estimate: sigma_hat = max(sigma_{fast}, sigma_{slow}).

> [!question]- mkt-sys-211 | What is the effect of volatility targeting on momentum crashes (Barroso & Santa-Clara 2015)?
> Scaling momentum by the inverse of its recent realized volatility (six months of daily returns) virtually eliminates its crashes and nearly doubles its Sharpe ratio, from 0.53 to 0.97 over 1927-2011 (Barroso and Santa-Clara 2015).

> [!question]- mkt-sys-212 | What is a terminal stop-out circuit breaker in a systematic fund?
> A pre-committed rule (e.g. at a 10% or 15% drawdown, illustrative levels) that liquidates all positions to cash and disables trading until a review is completed.

> [!question]- mkt-sys-213 | How does correlation breakdown during crises affect portfolio volatility estimation?
> In crises, asset correlations often surge toward 1.0; a volatility model assuming calm-period correlations will severely underestimate portfolio risk.

> [!question]- mkt-sys-214 | What is the GARCH(1,1) volatility model?
> Bollerslev's (1986) generalized ARCH model: sigma_t^2 = omega + alpha * epsilon_{t-1}^2 + beta * sigma_{t-1}^2, with alpha + beta < 1 for a finite unconditional variance omega / (1 - alpha - beta); it captures clustering and mean reversion.

> [!question]- mkt-sys-215 | Why should volatility scaling multipliers be updated incrementally rather than instantaneously?
> Applying a smoothing filter on k_t prevents erratic day-to-day position rebalancing and dampens execution turnover costs.

> [!question]- mkt-sys-216 | What is liquidity-adjusted volatility targeting?
> Scaling exposure inversely to volatility while simultaneously constraining maximum order size to a safe percentage of daily volume (e.g. <= 5% ADV).

> [!question]- mkt-sys-217 | How does short gamma exposure distort volatility targeting?
> Strategies with negative gamma (e.g. option selling) experience accelerating losses as volatility surges; volatility targeting must account for non-linear delta changes.

> [!question]- mkt-sys-218 | What is variation margin in futures execution?
> Daily cash settlement of unrealized gains and losses paid between clearinghouse members to reflect daily mark-to-market price changes.

> [!question]- mkt-sys-219 | Why does volatility targeting fail during instantaneous gap openings?
> Because gaps happen while the market is closed, so no de-risking trade can be executed at pre-gap prices.
> After the 11 September 2001 attacks the NYSE stayed closed until 17 September, and positions reopened at the new prices.

> [!question]- mkt-sys-220 | What is the Yang-Zhang (2000) volatility estimator?
> A weighted sum of the overnight variance, the open-to-close variance and the Rogers-Satchell estimator over n days (Yang and Zhang 2000).
> It is unbiased for any drift, handles opening jumps, and has minimum variance within that class of multi-day estimators.

> [!question]- mkt-sys-221 | How does portfolio volatility targeting interact with asset-level stop losses?
> Portfolio volatility targeting manages aggregate macro exposure top-down, while asset-level stop losses protect against idiosyncratic single-name company collapses.

> [!question]- mkt-sys-222 | What is the difference between gross leverage and net leverage?
> Gross leverage is the sum of absolute long and short exposures (|Long| + |Short|) / NAV; net leverage is the directional difference (Long - Short) / NAV.

> [!question]- mkt-sys-223 | Why should reset rules for drawdown governors require a cooling-off period?
> To prevent re-leveraging into the middle of a choppy, volatile bear market rally that could immediately reverse and trigger a secondary drawdown.

> [!question]- mkt-sys-224 | What is the ultimate objective of volatility targeting?
> To deliver a stable, predictable return-to-risk profile across decades of varying macroeconomic, monetary, and geopolitical market environments.

> [!question]- mkt-sys-265 | In a model where each month is calm (2% vol) or turbulent (6%) with a constant 0.5% expected return, what does variance management do to the Sharpe ratio, and what reverses it?
> It raises the annualized Sharpe ratio from 0.39 to 0.64, because weight 1/sigma^2 removes more risk than expected return.
> If the expected return were proportional to variance, the managed Sharpe ratio would fall to 0.23 while the unmanaged one stays 0.39.

> [!question]- mkt-sys-266 | Rank the Parkinson, Garman-Klass and Rogers-Satchell estimators by efficiency for driftless Brownian motion.
> Garman-Klass (about 7.4), then Rogers-Satchell (about 6.0), then Parkinson (4.91, exact).
> Rogers-Satchell gives up some efficiency to stay unbiased under drift.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../code/mkt_sys_07_vol_targeting.py`](../code/mkt_sys_07_vol_targeting.py) prints and asserts every number on this page: exposure multipliers in exact fractions, the Garman-Klass example, Parkinson efficiency exactly from the range moments, Garman-Klass and Rogers-Satchell efficiency by simulating Brownian days with exact per-step bridge extremes (tolerances of four computed standard errors), and the two-regime Sharpe ratios and kurtosis from Gaussian moments checked by simulation.
- Related notes: [Volatility Models: EWMA and GARCH](../../02-Statistics-and-Econometrics/09-Volatility-Models-GARCH.md).

## Further reading

- Barroso, P., & Santa-Clara, P. (2015). Momentum has its moments. *Journal of Financial Economics*, 116(1), 111-120.
- Black, F. (1976). Studies of stock price volatility changes. *Proceedings of the 1976 Meetings of the American Statistical Association, Business and Economic Statistics Section*, 177-181.
- Bollerslev, T. (1986). Generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics*, 31(3), 307-327.
- Engle, R. F. (1982). Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. *Econometrica*, 50(4), 987-1007.
- Garman, M. B., & Klass, M. J. (1980). On the estimation of security price volatilities from historical data. *The Journal of Business*, 53(1), 67-78.
- Harvey, C. R., Hoyle, E., Korgaonkar, R., Rattray, S., Sargaison, M., & Van Hemert, O. (2018). The impact of volatility targeting. *The Journal of Portfolio Management*, 45(1), 14-33.
- Moreira, A., & Muir, T. (2017). Volatility-managed portfolios. *The Journal of Finance*, 72(4), 1611-1644.
- Parkinson, M. (1980). The extreme value method for estimating the variance of the rate of return. *The Journal of Business*, 53(1), 61-65.
- Rogers, L. C. G., & Satchell, S. E. (1991). Estimating variance from high, low and closing prices. *The Annals of Applied Probability*, 1(4), 504-512.
- Yang, D., & Zhang, Q. (2000). Drift-independent volatility estimation based on high, low, open, and close prices. *The Journal of Business*, 73(3), 477-491.
