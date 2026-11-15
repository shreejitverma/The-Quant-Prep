---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Fama and French (1993) - Common Risk Factors in the Returns on Stocks and Bonds, Fama and French (2015) - A Five-Factor Asset Pricing Model, Carhart (1997) - On Persistence in Mutual Fund Performance, Asness Moskowitz and Pedersen (2013) - Value and Momentum Everywhere, Asness Frazzini and Pedersen (2019) - Quality Minus Junk, Frazzini and Pedersen (2014) - Betting Against Beta, Harvey Liu and Zhu (2016) - ...and the Cross-Section of Expected Returns, McLean and Pontiff (2016) - Does Academic Research Destroy Stock Return Predictability?, Hou Xue and Zhang (2020) - Replicating Anomalies]
---

# Factor Investing: Evidence, Replication, and Factor Decay

## TL;DR

- Factor investing systematically harvests return premiums that are documented across long samples and many markets, whether they are compensation for risk or the residue of behavioral and institutional frictions.
- The canonical equity factors are Market, Size (SMB), Value (HML), Momentum (UMD or WML), Profitability (RMW), Investment (CMA), Quality (QMJ) and Low Beta (BAB), each with its own original paper.
- Harvey, Liu and Zhu (2016) catalogued 316 factors and argued that, after accounting for multiple testing, a new factor needs a t-statistic above 3.0 (a two-sided p-value of 0.0027).
- Hou, Xue and Zhang (2020) found that 65% of 452 anomalies fail a $|t| > 1.96$ test once microcaps are controlled with NYSE breakpoints and value weights, and 82% fail a multiple-testing hurdle of 2.78.
- McLean and Pontiff (2016) found anomaly returns 26% lower out of sample and 58% lower after publication, implying a 32% decline attributable to publication-informed trading.
- Value and momentum are negatively correlated in every asset class Asness, Moskowitz and Pedersen (2013) study (-0.53 for their average stock strategies), which is why a combination of the two has a higher Sharpe ratio than either alone.

## Learning objectives

- Differentiate risk-based factor explanations from behavioral anomaly models.
- Formulate and estimate the Fama-French 3-factor and 5-factor multi-factor regressions.
- Analyze the Low Volatility (Betting Against Beta) anomaly and leverage constraint theory.
- Apply multiple-testing statistical haircuts to filter spurious factors out of the "factor zoo".
- Quantify factor decay mechanisms: publication arbitrage, capacity limits, and factor crowding.
- Construct integrated multi-factor portfolios combining Value, Momentum, Quality, and Low Beta.

## Core concepts

### 1. What is an Asset Pricing Factor?

A genuine asset pricing factor is an underlying, systematic driver of risk and return across a broad universe of assets.
Berkin and Swedroe (2016, *Your Complete Guide to Factor-Based Investing*) ask that a factor be:
1. **Persistent**: Holds across long historical periods and diverse economic regimes.
2. **Pervasive**: Holds across multiple asset classes, market capitalizations, and global geographic regions.
3. **Robust**: Not sensitive to the exact definition (e.g. value holds across P/B, P/E, EV/EBITDA, and cash flow yields).
4. **Implementable**: Survives realistic trading costs, turnover, bid-ask spreads, and borrowing costs.
5. **Intuitive**: Has a logical risk-based or behavioral explanation for why it should persist.

```
+-----------------------------------------------------------------------+
|                    FACTOR EXPLANATION DICHOTOMY                       |
+-----------------------------------------------------------------------+
| RISK-BASED THEORIES                    BEHAVIORAL THEORIES            |
| - Investors are compensated for        - Persistent cognitive biases  |
|   bearing non-diversifiable distress   (overreaction, recency bias,   |
|   or liquidity risk.                   anchoring, loss aversion).     |
| - Cannot be arbitraged away because    - Institutional constraints    |
|   investors demand a risk premium.     (benchmarks, leverage caps).   |
| - Example: Fama-French Value (HML) as  - Example: Momentum (UMD) as   |
|   compensation for distress risk.      underreaction to news.         |
+-----------------------------------------------------------------------+
```

### 2. The Canonical Equity Factors

```
+-----------------------------------------------------------------------+
|                    THE CANONICAL FACTOR TAXONOMY                      |
+-------------------+-----------------------+---------------------------+
| Factor Name       | Academic Origin       | Long / Short Construction |
+-------------------+-----------------------+---------------------------+
| Market Beta       | Sharpe (1964),        | Broad equity market index |
| (MKT)             | Lintner (1965)        | minus 1-month T-Bills.    |
+-------------------+-----------------------+---------------------------+
| Size              | Banz (1981),          | Long small-cap stocks;    |
| (SMB)             | Fama-French (1993)    | Short large-cap stocks.   |
+-------------------+-----------------------+---------------------------+
| Value             | Fama-French (1993)    | Long high Book-to-Market; |
| (HML)             |                       | Short low Book-to-Market. |
+-------------------+-----------------------+---------------------------+
| Momentum          | Jegadeesh-Titman(1993)| Long past winners, short  |
| (WML / UMD)       | Carhart (1997)        | past losers (t-12 to t-2).|
+-------------------+-----------------------+---------------------------+
| Profitability     | Novy-Marx (2013),     | Long robust operating     |
| (RMW)             | Fama-French (2015)    | profitability; short weak.|
+-------------------+-----------------------+---------------------------+
| Investment        | Titman et al. (2004), | Long low asset growth;    |
| (CMA)             | Fama-French (2015)    | short high asset growth.  |
+-------------------+-----------------------+---------------------------+
| Quality           | Asness, Frazzini,     | Long profitable, growing, |
| (QMJ)             | Pedersen (2019)       | safe, high-payout; short  |
|                   |                       | junk.                     |
+-------------------+-----------------------+---------------------------+
| Low Beta          | Baker et al. (2011),  | Long leveraged low-beta;  |
| (BAB)             | Frazzini-Pedersen(2014| Short de-leveraged high.  |
+-------------------+-----------------------+---------------------------+
```

The Carhart (1997) four-factor model adds a one-year momentum factor to the Fama-French three factors.

### 3. The Low Volatility / Betting Against Beta (BAB) Anomaly

The CAPM predicts that expected excess return rises one for one with beta.
Empirically the security market line is too flat: low-beta stocks have earned higher risk-adjusted returns (alphas and Sharpe ratios) than high-beta stocks.

```
+-----------------------------------------------------------------------+
|                    THE FLAT SECURITY MARKET LINE                      |
+-----------------------------------------------------------------------+
| Expected Return                                                       |
|   ^                                                                   |
|   |                       Theoretical CAPM Line (Steep)               |
|   |                      /                                            |
|   |                     /      Realized Empirical Line (Flat!)        |
|   |                    /----------------------------------            |
|   |                   /                                               |
|   |                  /   Low-beta equities generate alpha;            |
|   |                 /    High-beta equities underperform.             |
|   |                /                                                  |
|   +-------------------------------------------------------------->    |
|   Rf              Beta = 1.0                              Beta = 2.0  |
+-----------------------------------------------------------------------+
```

Why does the Low Volatility Anomaly persist?
1. **Leverage Constraints**: Frazzini and Pedersen (2014) argue that many investors cannot or will not use leverage, so to reach a high expected return they overweight high-beta assets instead, bidding up their prices.
2. **Agency Incentives**: Baker, Bradley and Wurgler (2011) argue that benchmarked managers face tracking-error limits that discourage them from buying low-beta stocks, which limits arbitrage of the anomaly.
3. **The BAB Portfolio**: Frazzini and Pedersen (2014, Journal of Financial Economics) construct Betting Against Beta: a long position in low-beta stocks levered to a beta of one, against a short position in high-beta stocks de-levered to a beta of one, and document positive risk-adjusted returns in US equities, international equity markets, Treasury bonds, corporate bonds and futures.

### 4. The Factor Zoo and Multiple-Testing Haircuts

Cochrane (2011, Journal of Finance presidential address) described the "zoo" of new factors.
Harvey, Liu and Zhu (2016) catalogued 316 factors from published articles and working papers through 2012, and argued that most claimed findings are likely false once multiple testing is accounted for:
- With one test, the usual threshold is $|t| > 1.96$ for a two-sided p-value of 0.05 (using $|t| > 2.00$ gives 0.0455).
- If 1,000 researchers each test one useless signal, about 50 will pass $|t| > 1.96$ by chance alone, and about 45.5 will pass $|t| > 2$.

```
+-----------------------------------------------------------------------+
|                    MULTIPLE TESTING SIGNIFICANCE THRESHOLDS           |
+------------------------+---------------+------------------------------+
| Testing Framework      | |t| cutoff    | two-sided p-value            |
+------------------------+---------------+------------------------------+
| Standard Single Test   | 1.96          | 0.0500                       |
| Harvey-Liu-Zhu Cutoff  | 3.00          | 0.0027                       |
| Bonferroni, 316 tests  | 3.78          | 0.05 / 316 = 0.000158        |
+------------------------+---------------+------------------------------+
```

A factor proposed today with $|t| < 3$ should be treated as unproven until it replicates out of sample.

Hou, Xue and Zhang (2020, Review of Financial Studies) replicated 452 anomalies with NYSE breakpoints and value-weighted returns to limit the influence of microcaps.
65% of them, including 96% of the trading-frictions category, fail the single-test hurdle of $|t| > 1.96$, and 82% fail a multiple-test hurdle of 2.78; even the survivors are typically smaller than originally reported.

### 5. Factor Decay: Publication Arbitrage and Crowding

McLean and Pontiff (2016, Journal of Finance) studied 97 published return predictors across three periods:

```
+-----------------------------------------------------------------------+
|                    THE FACTOR DECAY TIMELINE                          |
+-----------------------------------------------------------------------+
| 1. In-Sample Period (original study):                                 |
|    - Average long-short return 0.582% a month.                        |
|                                                                       |
| 2. Post-Sample, Pre-Publication Period:                               |
|    - Regression decline of 0.150% a month: 26% of the in-sample mean, |
|      an upper bound on data mining (raw average 0.402% a month).      |
|                                                                       |
| 3. Post-Publication Period:                                           |
|    - Regression decline of 0.337% a month: 58% of the in-sample mean  |
|      (raw average 0.264% a month).                                    |
|    - The 32% gap (58% - 26%) is attributed to publication-informed    |
|      trading.                                                         |
+-----------------------------------------------------------------------+
```

The paper also finds larger post-publication declines for predictors with higher in-sample returns, and rising correlations with other published predictors after publication.

Why Factors Decay:
1. **Arbitrage Inflows**: Once a predictor is published, investors trade on it, which moves prices and shrinks the remaining premium.
2. **Transaction Cost Drag**: Academic long-short returns usually ignore trading and shorting costs; high-turnover and small-cap anomalies lose the most once those costs are paid.
3. **Crowding and Liquidation Cascades**: When many funds hold similar factor positions, forced selling by one can hit all of them at once; Khandani and Lo (2011) analyze the August 2007 quant losses in these terms.

### 6. The Value-Momentum Negative Correlation

Asness, Moskowitz and Pedersen (2013, Journal of Finance) find that value and momentum are negatively correlated within and across eight markets and asset classes.
For their average stock strategies the correlation is -0.53 (Table II), and it is still -0.28 when book-to-market uses year-old prices so that it does not overlap with the momentum signal.

Why are Value and Momentum negatively correlated?
- Value buys assets that are cheap, which are often assets whose prices have recently fallen.
- Momentum buys assets whose prices have recently risen.
- The two signals therefore tend to hold opposite sides of recent winners and losers.

For two strategies with equal volatility and equal Sharpe ratio $S$, a 50/50 mix has Sharpe ratio $S\sqrt{2/(1+\rho)}$.
With these hypothetical equal inputs, $\rho = -0.53$ multiplies the Sharpe ratio by 2.063 and $\rho = -0.28$ by 1.667; real factors have unequal Sharpe ratios and volatilities, so the gain is smaller in practice.

```
+-----------------------------------------------------------------------+
|                    MULTI-FACTOR PORTFOLIO INTEGRATION                 |
+-----------------------------------------------------------------------+
| Blended Multi-Factor (50% Value + 50% Momentum):                      |
| - Negative covariance offsets part of each factor's volatility.       |
| - Equal-Sharpe, equal-volatility case: Sharpe x sqrt(2 / (1 + rho)). |
| - Each factor's worst periods are partly offset by the other.        |
+-----------------------------------------------------------------------+
```

## Worked numerical case study

Estimate a Fama-French 3-Factor regression for a hypothetical fund, QuantAlpha, over a 60-month sample:
$$\text{Fund Excess Return}: \quad R_t - R_f = \alpha + \beta_{\text{mkt}} (R_{m,t} - R_f) + \beta_{\text{smb}} \text{SMB}_t + \beta_{\text{hml}} \text{HML}_t + \epsilon_t$$

### OLS Regression Output (hypothetical):
- Dependent Variable: QuantAlpha Monthly Excess Return ($R_t - R_f$)
- Observations ($N$): 60 months, 4 estimated coefficients, so 56 residual degrees of freedom

| Variable | Coefficient ($\beta$) | Standard Error ($SE$) | $t$-statistic | $p$-value |
|---|---|---|---|---|
| Intercept ($\alpha$) | +0.25% / month | 0.08% | **+3.125** | 0.0028 |
| Market Beta ($\text{MKT}$) | 0.850 | 0.035 | **+24.29** | < 0.0001 |
| Size Factor ($\text{SMB}$) | +0.420 | 0.060 | **+7.00** | < 0.0001 |
| Value Factor ($\text{HML}$) | -0.310 | 0.055 | **-5.64** | < 0.0001 |
| Model $R^2$ | 0.885 | - | - | - |

### Factor Exposure Interpretation:
1. **Market Beta ($\beta_{\text{mkt}} = 0.85$)**:
   - The fund carries below-market exposure; when the market's excess return is 1.0%, the fund's fitted excess return rises by 0.85%.
2. **Size Exposure ($\beta_{\text{smb}} = +0.42$)**:
   - $t = 7.00$, so the fund has a clear tilt toward small and mid-cap stocks.
3. **Value Exposure ($\beta_{\text{hml}} = -0.31$)**:
   - $t = -5.64$, so the fund leans toward growth stocks (low book-to-market).
4. **Alpha ($\alpha = +0.25\%$ / month)**:
   - Annualized Alpha = $0.25\% \times 12 = \mathbf{+3.00\% \text{ per year}}$ (3.04% compounded).
   - $t$-statistic = $+3.125$, just above the Harvey-Liu-Zhu hurdle of 3.0; the two-sided p-value with 56 degrees of freedom is 0.0028.
   - Conclusion: the alpha is not explained by market, size or value exposure, but it is one 60-month sample, the model omits momentum, profitability and investment, and a t-statistic barely above 3 is evidence to monitor, not proof of skill.

## Practice questions

> [!question]- mkt-pf-033 | What is an asset pricing factor?
> A systematic, persistent driver of risk and return across a broad universe of securities that explains cross-sectional return variations.

> [!question]- mkt-pf-034 | What are the three factors in the original Fama-French 1993 model?
> Market Excess Return (MKT), Size (SMB - Small Minus Big), and Value (HML - High Minus Low).

> [!question]- mkt-pf-035 | What two factors were added to create the Fama-French 5-Factor model in 2015?
> Profitability (RMW - Robust Minus Weak operating profitability) and Investment (CMA - Conservative Minus Aggressive, sorted on asset growth).

> [!question]- mkt-pf-036 | What is the Carhart 4-Factor model?
> The Fama-French 3-factor model plus the Momentum factor (WML / UMD - Winners Minus Losers).

> [!question]- mkt-pf-037 | What is the Low Volatility / Betting Against Beta (BAB) anomaly?
> The empirical finding that low-volatility and low-beta equities generate higher risk-adjusted returns (higher Sharpe ratios) than high-beta equities.

> [!question]- mkt-pf-038 | Why does the Low Volatility anomaly exist according to leverage constraint theory?
> Frazzini and Pedersen (2014): investors who cannot or will not borrow reach for return by overweighting high-beta stocks, which bids their prices up and their future risk-adjusted returns down.

> [!question]- mkt-pf-039 | What is the 'Factor Zoo' described by Campbell Harvey, Yan Liu, and Heqing Zhu?
> The proliferation of claimed return predictors (Cochrane's 2011 "zoo" of factors); Harvey, Liu and Zhu (2016) catalogued 316 and argued that most are likely false discoveries from multiple testing.

> [!question]- mkt-pf-040 | What statistical significance hurdle did Harvey, Liu, and Zhu recommend for new factor discovery?
> A t-statistic hurdle of t > 3.0 (p < 0.0027), replacing the traditional t > 2.0 cutoff to account for multiple testing snooping.

> [!question]- mkt-pf-041 | What is the empirical post-publication decay rate of factors documented by McLean and Pontiff?
> Returns of 97 published predictors are 58% lower after publication and 26% lower out of sample before publication, so about 32% is attributed to publication-informed trading.

> [!question]- mkt-pf-042 | What is the structural correlation between the Value factor (HML) and the Momentum factor (WML)?
> Negative in every asset class Asness, Moskowitz and Pedersen (2013) study: -0.53 for their average stock strategies, and -0.28 when book-to-market uses year-old prices.

> [!question]- mkt-pf-043 | Why does blending Value and Momentum in a multi-factor portfolio increase the Sharpe ratio?
> Their negative correlation offsets part of each strategy's volatility while both premiums add; with equal Sharpe ratios and volatilities the mix has Sharpe ratio S sqrt(2 / (1 + rho)).

> [!question]- mkt-pf-044 | What is the Quality Minus Junk (QMJ) factor formulated by Asness, Frazzini, and Pedersen?
> Long high-quality stocks (profitable, growing, safe and high-payout) and short low-quality "junk" stocks (Asness, Frazzini and Pedersen 2019, Review of Accounting Studies).

> [!question]- mkt-pf-045 | Why did the classic Fama-French Size factor (SMB) weaken post-1980?
> The size premium has been weak since Banz (1981) was published and is concentrated in illiquid microcaps; Asness, Frazzini, Israel, Moskowitz and Pedersen (2018) find that it becomes robust again once you control for quality ("junk").

> [!question]- mkt-pf-046 | What is factor crowding?
> When large quantities of quantitative capital hold identical long/short factor positions, creating liquidity risk and sharp unwinding cascades during redemptions.

> [!question]- mkt-pf-047 | What was the August 2007 Quant Meltdown?
> Sharp losses in quantitative long/short equity portfolios in early August 2007, which Khandani and Lo (2011) attribute to the rapid unwinding of similar, crowded positions.

> [!question]- mkt-pf-048 | What is the difference between top-down factor combination and bottom-up factor integration?
> Combination blends separate single-factor portfolios (causing redundant cross-trading); integration calculates a unified multi-factor score per stock before weighting.

> [!question]- mkt-pf-049 | What is the Capital Investment Anomaly (CMA)?
> Firms with high asset growth (aggressive investment) have earned lower subsequent returns than firms with low asset growth (Titman, Wei and Xie 2004; Cooper, Gulen and Schill 2008).

> [!question]- mkt-pf-050 | What is the Gross Profitability premium documented by Robert Novy-Marx?
> Gross Profit divided by Total Assets is a powerful predictor of future cross-sectional stock returns, operating as a clean quality factor that complements value.

> [!question]- mkt-pf-051 | Why does the traditional Book-to-Market value metric struggle in technology sectors?
> Because software and knowledge companies invest via expensed R&D rather than capitalized plant assets, causing book value to severely understate economic capital.

> [!question]- mkt-pf-052 | How should an analyst measure true Value in modern markets?
> By combining multiple value metrics: EV/EBITDA, Free Cash Flow Yield, and Intangible-Adjusted Book Value.

> [!question]- mkt-pf-053 | What is time-series momentum (trend following) versus cross-sectional momentum?
> Cross-sectional momentum ranks assets against each other (relative winners); time-series momentum evaluates an asset's absolute return against its own past history.

> [!question]- mkt-pf-054 | What is the Momentum Crash phenomenon documented by Daniel and Moskowitz?
> Momentum strategies occasionally suffer severe, persistent losses; Daniel and Moskowitz (2016) show these crashes are partly forecastable, occur in panic states after market declines and high volatility, and coincide with market rebounds when past losers jump.

> [!question]- mkt-pf-055 | What is the optimal lookback window for cross-sectional price momentum?
> The standard signal is the 12-month return skipping the most recent month (months t-12 to t-2), because one-month returns tend to reverse.

> [!question]- mkt-pf-056 | What is a 'smart beta' ETF?
> A rules-based, non-market-cap-weighted exchange-traded fund designed to provide systematic exposure to specific factors (such as Value, Quality, or Low Volatility).

> [!question]- mkt-pf-057 | What is the primary execution friction in small-cap factor strategies?
> Bid-ask spread costs, market impact on rebalancing, and high stock loan borrow fees for the short leg of the portfolio.

> [!question]- mkt-pf-058 | What is the Bonferroni correction in multiple-testing adjustments?
> Adjusting the statistical significance threshold alpha to alpha / N, where N is the total number of tested hypotheses.

> [!question]- mkt-pf-059 | Why do factor premiums vary across economic regimes?
> Factors load on different macro risks, so their returns differ by regime; treat claims such as "quality wins in recessions" as hypotheses to test on your own data rather than settled facts.

> [!question]- mkt-pf-060 | What is factor timing and why is it notoriously difficult?
> Attempting to dynamically rotate between factors based on valuation or macro indicators; timing often generates high turnover without consistent predictive alpha.

> [!question]- mkt-pf-061 | What is the difference between raw factor returns and style-neutral factor returns?
> Raw returns may contain unhedged industry or sector biases; style-neutral returns neutralize sector weights to isolate pure idiosyncratic factor exposure.

> [!question]- mkt-pf-062 | How does shorting friction limit the arbitrage of anomalies?
> Hard-to-borrow fees, borrow recall risk, and margin requirements prevent quantitative hedge funds from fully arbitraging away overpriced junk securities.

> [!question]- mkt-pf-063 | What is idiosyncratic volatility and is it priced in equity markets?
> Firm-specific risk unrelated to systematic factors; standard theory says it is not rewarded, while Ang, Hodrick, Xing and Zhang (2006) find that high idiosyncratic volatility stocks have earned low subsequent returns.

> [!question]- mkt-pf-064 | What is the ultimate takeaway for quantitative factor investors?
> Rely only on factors with robust empirical evidence (t > 3.0), maintain multi-factor diversification across Value and Momentum, and account for real-world transaction costs.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_pm_02_factor_evidence.py`](../../code/mkt_pm_02_factor_evidence.py) prints and asserts every computed number on this page: normal tail probabilities from erfc against Simpson integration and a seeded simulation of 1,000 null tests, the Bonferroni cutoff by bisection checked by integrating back, the McLean-Pontiff declines from their published coefficients, the regression p-value by Simpson integration of the Student-t density against a seeded simulation, and the value-momentum Sharpe multiplier against a seeded simulation of correlated factors.
- Related notes: [Asset Allocation and The Benchmark to Beat](01-Asset-Allocation-and-The-Benchmark-to-Beat.md) (the benchmark a factor portfolio must beat), [Risk Parity and The All-Weather Framework](06-Risk-Parity-and-The-All-Weather-Framework.md) (Betting Against Beta and leverage aversion).

## Further reading

- Ang, A., Hodrick, R. J., Xing, Y., & Zhang, X. (2006). *The Cross-Section of Volatility and Expected Returns*. The Journal of Finance, 61(1), 259-299.
- Asness, C. S., Frazzini, A., Israel, R., Moskowitz, T. J., & Pedersen, L. H. (2018). *Size Matters, If You Control Your Junk*. Journal of Financial Economics, 129(3), 479-509.
- Asness, C. S., Frazzini, A., & Pedersen, L. H. (2019). *Quality Minus Junk*. Review of Accounting Studies, 24(1), 34-112.
- Asness, C. S., Moskowitz, T. J., & Pedersen, L. H. (2013). *Value and Momentum Everywhere*. The Journal of Finance, 68(3), 929-985.
- Baker, M., Bradley, B., & Wurgler, J. (2011). *Benchmarks as Limits to Arbitrage: Understanding the Low-Volatility Anomaly*. Financial Analysts Journal, 67(1), 40-54.
- Berkin, A. L., & Swedroe, L. E. (2016). *Your Complete Guide to Factor-Based Investing*. BAM Alliance Press.
- Carhart, M. M. (1997). *On Persistence in Mutual Fund Performance*. The Journal of Finance, 52(1), 57-82.
- Cochrane, J. H. (2011). *Presidential Address: Discount Rates*. The Journal of Finance, 66(4), 1047-1108.
- Cooper, M. J., Gulen, H., & Schill, M. J. (2008). *Asset Growth and the Cross-Section of Stock Returns*. The Journal of Finance, 63(4), 1609-1651.
- Daniel, K., & Moskowitz, T. J. (2016). *Momentum Crashes*. Journal of Financial Economics, 122(2), 221-247.
- Fama, E. F., & French, K. R. (1993). *Common Risk Factors in the Returns on Stocks and Bonds*. Journal of Financial Economics, 33(1), 3-56.
- Fama, E. F., & French, K. R. (2015). *A Five-Factor Asset Pricing Model*. Journal of Financial Economics, 116(1), 1-22.
- Frazzini, A., & Pedersen, L. H. (2014). *Betting Against Beta*. Journal of Financial Economics, 111(1), 1-25.
- Harvey, C. R., Liu, Y., & Zhu, H. (2016). *...and the Cross-Section of Expected Returns*. The Review of Financial Studies, 29(1), 5-68.
- Hou, K., Xue, C., & Zhang, L. (2020). *Replicating Anomalies*. The Review of Financial Studies, 33(5), 2019-2133.
- Khandani, A. E., & Lo, A. W. (2011). *What Happened to the Quants in August 2007? Evidence from Factors and Transactions Data*. Journal of Financial Markets, 14(1), 1-46.
- McLean, R. D., & Pontiff, J. (2016). *Does Academic Research Destroy Stock Return Predictability?* The Journal of Finance, 71(1), 5-32.
- Novy-Marx, R. (2013). *The Other Side of Value: The Gross Profitability Premium*. Journal of Financial Economics, 108(1), 1-28.
- Titman, S., Wei, K. C. J., & Xie, F. (2004). *Capital Investments and Stock Returns*. Journal of Financial and Quantitative Analysis, 39(4), 677-700.
