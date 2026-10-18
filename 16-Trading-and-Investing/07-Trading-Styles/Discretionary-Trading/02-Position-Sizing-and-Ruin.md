---
type: concept
title: "Position Sizing, Volatility Targeting, and Risk of Ruin"
track: [quant-trader, quant-research]
tier: core
status: solid
est_hours: 1.5
tags: [position-sizing, kelly-criterion, risk-of-ruin, volatility-targeting, drawdowns, risk-management]
prereqs: []
---

# Position Sizing, Volatility Targeting, and Risk of Ruin

The single most significant determinant of whether a trader achieves long-term compounding or catastrophic ruin is not their setup selection or entry timing.
It is their position sizing model.
A trader with an exceptional predictive edge who bets too large will inevitably suffer mathematical bankruptcy due to variance drag and sequence of returns risk.
Conversely, a trader with a modest edge who rigorously applies fractional sizing and volatility targeting will survive drawdowns and compound capital systematically.

---

## TL;DR

Position sizing dictates how much capital is committed to an idea based on the distance to the invalidation stop.
The Kelly Criterion maximizes the expected log-wealth growth rate but induces catastrophic drawdowns when parameters are estimated with error; professional desks deploy Fractional Kelly ($0.25f^*$ to $0.50f^*$).
Risk of ruin decreases exponentially with the ratio of edge to risk units:
$$R = \left(\frac{1 - A}{1 + A}\right)^{C}$$
Drawdown recovery requires asymmetric percentage gains: a 50% loss demands a 100% gain just to break even.
Volatility targeting scales position size inversely to asset volatility, stabilizing portfolio risk across changing regimes.

---

## Learning objectives

- Formulate the classical Kelly Criterion and derive the geometric growth rate curve $g(f)$.
- Calculate the exact classical risk of ruin under Bernoulli payoff distributions.
- Implement fixed fractional sizing and ATR-based volatility targeting models.
- Quantify the asymmetric mathematical penalty of drawdowns and time-under-water (TUW).
- Calibrate fractional Kelly boundaries to defend against fat-tailed return shocks and parameter estimation error.

---

## Core concepts

### 1. The Position Sizing Spectrum

Professional market participants utilize three primary position sizing paradigms:

1. **Fixed Dollar Sizing**:
   - Commits an identical dollar value to every position (e.g. $\$10,000$ per trade).
   - Fatal flaw: High-volatility small-cap stocks contribute wildly disproportionate risk compared to low-volatility large caps.

2. **Fixed Fractional Risk Sizing**:
   - Limits the risk of any single trade to a fixed percentage $f$ of current account equity (typically $1.0\%$ to $2.0\%$):
     $$\text{Dollar Risk} = \text{Equity}_t \times f$$
     $$\text{Position Size } Q = \frac{\text{Equity}_t \times f}{|P_{\text{entry}} - P_{\text{stop}}|}$$
   - Automatically scales position size downward during drawdowns (preserving capital) and upward during winning streaks.

3. **Volatility Targeting (Risk Parity at the Trade Level)**:
   - Sizes positions such that each trade contributes an identical daily dollar volatility:
     $$Q_t = \frac{\text{Target Dollar Volatility}}{\text{ATR}_t \times \text{Multiplier}}$$
   - Prevents calm market positions from being dominated by sudden high-volatility trades.

### 2. The Kelly Criterion and Growth Curve

John L. Kelly Jr. (1956) formulated the optimal fraction of wealth to wager on an edge-positive bet to maximize the long-term geometric compounding growth rate of wealth:

$$\max_f \mathbb{E}[\ln(W_T)]$$

For a discrete binomial trade with win probability $p$, loss probability $q = 1 - p$, and win/loss payoff ratio $b = \frac{\bar{W}}{\bar{L}}$:

$$f^* = \frac{p(b + 1) - 1}{b} = p - \frac{q}{b}$$

The expected geometric growth rate per trade $g(f)$ as a function of the fraction bet $f$ is:

$$g(f) = p \ln(1 + b f) + (1 - p) \ln(1 - f)$$

**Critical Properties of the Kelly Growth Curve**:
- **Peak at $f^*$**: The maximum compound growth rate occurs uniquely at $f = f^*$.
- **The Danger Zone ($f > f^*$)**:
  Betting more than $f^*$ decreases expected compound growth while increasing volatility.
- **The Zero-Growth Threshold (near $2 f^*$)**:
  In the small-edge continuous approximation $g(f) \approx \mu f - \frac{1}{2}\sigma^2 f^2$, growth falls to exactly zero at $f = 2 f^*$ and is negative beyond it.
  For a discrete bet the exact crossing must be solved numerically: for Example 1 below ($p = 0.40$, $b = 2.50$, $f^* = 0.16$) it is $f \approx 0.331$, about $2.07 f^*$, so $g(2 f^*) = g(0.32)$ is still slightly positive.
  Beyond the crossing, expected log growth is negative and wealth converges to zero with probability 1 despite the positive edge per trade.
- **Fractional Kelly**:
  Because real-world parameters $p$ and $b$ are estimated with error and returns exhibit fat tails, professional funds deploy "Half-Kelly" ($0.50f^*$) or "Quarter-Kelly" ($0.25f^*$).
  In the continuous approximation a bet of $c f^*$ earns $(2c - c^2)$ of the maximum growth rate, so Half-Kelly captures $2(0.5) - 0.5^2 = 75\%$ of it.
  Return volatility scales with $f$, so Half-Kelly halves volatility, cuts variance to $25\%$ of full Kelly, and drastically reduces peak-to-trough drawdown.

### 3. The Mathematics of Risk of Ruin

Risk of ruin $R$ is the probability that an account's equity falls to or below an absorbing bankruptcy threshold before reaching a target profit boundary.
For independent even-money bets ($b = 1$) of a fixed dollar size, with win probability $p$, loss probability $q = 1 - p$, and edge $A = p - q > 0$, the exact probability of ever losing $C$ capital risk units over an infinite horizon is:

$$R = \left(\frac{q}{p}\right)^C = \left(\frac{1 - A}{1 + A}\right)^C$$

Where:
- $C = \frac{\text{Capital}}{\text{Dollar Risk per Trade}} = \frac{1}{f}$ is the number of risk units the trader can lose before total exhaustion.

When $p = 0.50$ (zero edge), $R = 1.00$ ($100\%$ certainty of ruin over an infinite horizon).
When $p > 0.50$, the probability of ruin decreases exponentially as capital units $C$ increase.
With $C = 50$ (risking $2.0\%$ of starting equity per trade), ruin is $(0.45/0.55)^{50} = 0.0044\%$ at $p = 0.55$ and $(0.48/0.52)^{50} = 1.8\%$ at $p = 0.52$, but still $(0.49/0.51)^{50} = 13.5\%$ at $p = 0.51$, so thin edges need far more risk units.
The formula does not apply to fixed fractional sizing, under which equity shrinks geometrically and never reaches zero; there ruin has to be redefined as hitting a drawdown floor.

### 4. The Asymmetric Drawdown Law

Drawdown $D \in [0, 1)$ is the peak-to-trough percentage decline in account equity:

$$D = \frac{\text{Equity}_{\text{peak}} - \text{Equity}_{\text{trough}}}{\text{Equity}_{\text{peak}}}$$

The percentage gain required to recover from a drawdown back to the previous equity peak is highly non-linear:

$$\text{Recovery Gain } G = \frac{D}{1 - D}$$

| Drawdown ($D$) | Recovery Gain Required ($G$) | Operational Impact |
|----------------|------------------------------|--------------------|
| **5.0%** | **5.26%** | Negligible; normal daily fluctuation |
| **10.0%** | **11.11%** | Manageable within 1-2 standard weeks |
| **20.0%** | **25.00%** | Requires substantial alpha outperformance |
| **30.0%** | **42.86%** | Severe psychological stress and risk reduction |
| **50.0%** | **100.00%** | Must double capital just to break even |
| **75.0%** | **300.00%** | Catastrophic; account survival virtually impossible |
| **90.0%** | **900.00%** | Total structural liquidation |

---

## Worked examples

### Example 1: Full Kelly vs Half Kelly vs Over-Betting

A trader develops a trend-following setup with:
- Win rate: $p = 40\%$ ($0.40$).
- Loss rate: $q = 60\%$ ($0.60$).
- Average win/loss payoff ratio: $b = 2.50$ (wins average $2.5\times$ losses).

1. **Calculate the Optimal Kelly Fraction $f^*$**:
   $$f^* = \frac{0.40(2.50 + 1) - 1}{2.50} = \frac{0.40(3.50) - 1}{2.50} = \frac{1.40 - 1.00}{2.50} = \frac{0.40}{2.50} = 0.160\text{ (16.0% of equity)}$$

2. **Evaluate Expected Growth Rate at Full Kelly ($f = 0.16$)**:
   $$g(0.16) = 0.40 \ln(1 + 2.5 \times 0.16) + 0.60 \ln(1 - 0.16)$$
   $$= 0.40 \ln(1.40) + 0.60 \ln(0.84) = 0.40(0.3365) + 0.60(-0.1744) = 0.1346 - 0.1046 = +0.0300\text{ (3.00% per trade)}$$

3. **Evaluate Expected Growth Rate at Half Kelly ($f = 0.08$)**:
   $$g(0.08) = 0.40 \ln(1 + 2.5 \times 0.08) + 0.60 \ln(1 - 0.08)$$
   $$= 0.40 \ln(1.20) + 0.60 \ln(0.92) = 0.40(0.1823) + 0.60(-0.0834) = 0.0729 - 0.0500 = +0.0229\text{ (2.29% per trade)}$$
   - Half Kelly captures $\frac{2.29\%}{3.00\%} = 76.3\%$ of the maximum theoretical growth rate while reducing exposure and volatility by $50\%$.

4. **Evaluate the Catastrophic Penalty of Over-Betting ($f = 2 f^* = 0.32$)**:
   $$g(0.32) = 0.40 \ln(1 + 2.5 \times 0.32) + 0.60 \ln(1 - 0.32)$$
   $$= 0.40 \ln(1.80) + 0.60 \ln(0.68) = 0.40(0.5878) + 0.60(-0.3857) = 0.2351 - 0.2314 = +0.0037\text{ (0.37% per trade)}$$
   If the trader bets $35\%$ ($f = 0.35$):
   $$g(0.35) = 0.40 \ln(1.875) + 0.60 \ln(0.65) = 0.40(0.6286) + 0.60(-0.4308) = 0.25144 - 0.25847 = -0.0070\text{ (-0.70% per trade)}$$
   Doubling Kelly to $32\%$ leaves only $0.37\%$ growth per trade, about one eighth of full Kelly's $3.00\%$, and growth turns negative past $f \approx 0.331$.
   The trader has an edge ($p=0.40, b=2.50$), yet betting $35\%$ drives wealth toward zero with probability 1 over time.

### Example 2: ATR Volatility-Targeted Position Sizing

An account with $\$100,000$ equity limits risk to $1.5\%$ per trade ($\$1,500$ risk budget).
The trader enters stock XYZ at $\$150.00$.
- Current 14-period Average True Range: $\text{ATR}_{14} = \$3.50$.
- Invalidation stop is placed at $2 \times \text{ATR}$ below entry:
  $$P_{\text{stop}} = \$150.00 - (2 \times \$3.50) = \$150.00 - \$7.00 = \$143.00$$
- Stop distance per share: $\$7.00$.

1. **Calculate Share Quantity**:
   $$Q = \frac{\text{Dollar Risk Budget}}{\text{Stop Distance}} = \frac{\$1,500}{\$7.00} = 214.28 \implies 214\text{ shares}$$
2. **Calculate Total Position Value**:
   $$\text{Position Value} = 214 \times \$150.00 = \$32,100\text{ (32.1% of account equity)}$$
3. **Verify Dollar Risk on Invalidation**:
   $$\text{Actual Realized Risk} = 214 \times (\$150.00 - \$143.00) = 214 \times \$7.00 = \$1,498.00$$
   The dollar risk is locked to exactly $\$1,500$ (1.5% of capital) regardless of the stock's volatility.

---

## Pitfalls

- **Confusing Kelly with Maximum Comfort**:
  Full Kelly strategies regularly suffer peak-to-trough drawdowns exceeding $50\%$ to $70\%$.
  Almost no human trader or institutional capital allocator can emotionally or legally endure a $50\%$ drawdown without liquidating the manager.
- **Correlation Blindness (Total Portfolio Heat)**:
  Opening five distinct trades risking $1.5\%$ each in Apple, Microsoft, Nvidia, Google, and Amazon does not represent five independent bets.
  High cross-asset correlation creates an aggregate systemic portfolio risk of $7.5\%$ on a single tech macro factor.
- **Static Share Sizing**:
  Trading a static "1,000 shares" on a $\$20$ stock risks $\$500$ on a $\$0.50$ stop, but trading 1,000 shares on a $\$400$ stock with a $\$10$ stop risks $\$10,000$.
  Static share sizing exposes capital to random volatility shocks.
- **Ignoring Overnight Gap Risk**:
  A stop-loss order placed at $\$143.00$ does not protect against a disastrous overnight earnings report opening at $\$130.00$.
  Position sizes must be capped such that a catastrophic $20\%$ overnight gap does not exceed maximum acceptable portfolio loss.

---

## Interview questions

> [!question]- mkt-trd-033 | What is the fundamental objective of the Kelly Criterion?
> To determine the optimal fraction of wealth to wager on an edge-positive bet in order to maximize the long-term expected geometric compounding rate of capital.
> It maximizes E[ln(W_T)] over an infinite horizon.

> [!question]- mkt-trd-034 | State the formula for the single-asset discrete Kelly fraction f*.
> f* = (p * (b + 1) - 1) / b, which can also be written as p - (q / b).
> Here p is win probability, q = 1 - p is loss probability, and b is the average win/loss payoff ratio.

> [!question]- mkt-trd-035 | What happens to expected geometric compounding growth if a trader bets more than 2 * f*?
> In the small-edge continuous approximation growth is zero at 2 * f* and negative beyond it: g(f) < 0.
> For a discrete bet the exact zero crossing sits near but not at 2 * f* (about 0.331 versus 2 * f* = 0.32 for p = 0.40 and b = 2.50).
> Past the crossing, despite a positive edge per trade, wealth converges to zero with probability 1 because variance drag outweighs the edge.

> [!question]- mkt-trd-036 | Why do quantitative prop desks deploy Fractional Kelly (e.g. Half-Kelly or Quarter-Kelly)?
> Real-world win rates and payoff ratios are estimated with statistical uncertainty, and market returns exhibit fat-tailed jump risks.
> Half-Kelly captures 75% of maximum growth while cutting return volatility by 50% and dramatically reducing catastrophic drawdown risk.

> [!question]- mkt-trd-037 | State the classical risk of ruin equation for an account risking a fixed dollar amount on independent even-money bets.
> Ruin Probability R = ((1 - A) / (1 + A))^C, where A = p - q is the trader's net directional edge and C is the total number of risk units in the account.
> Ruin decays exponentially as the number of risk units C increases.

> [!question]- mkt-trd-038 | Why is the percentage recovery required after a drawdown asymmetric?
> Capital losses reduce the remaining equity base from which subsequent returns are compounded.
> A drawdown of D requires a recovery gain of G = D / (1 - D); thus a 50% loss requires a 100% gain, and an 80% loss requires a 400% gain.

> [!question]- mkt-trd-039 | What is Time Under Water (TUW) in quantitative risk analytics?
> The total duration of time an investment or portfolio spends below its previous high-water mark equity peak.
> TUW measures the psychological and operational drag of enduring extended, non-productive recovery periods.

> [!question]- mkt-trd-040 | Explain fixed fractional position sizing.
> Sizing every position such that the maximum loss upon hitting the stop-loss equals a fixed percentage f of total account equity (e.g. 1%): Q = (Equity * f) / |Entry - Stop|.
> Position size contracts automatically after losses and expands after gains, protecting capital during drawdowns.

> [!question]- mkt-trd-041 | How does volatility targeting normalize risk across diverse instruments?
> It calculates position size inversely to an asset's rolling volatility (e.g. 14-day ATR): Q = Target_Dollar_Risk / (ATR * Multiplier).
> A high-volatility instrument receives a small share size, while a low-volatility instrument receives a larger size, equalizing their dollar risk contributions.

> [!question]- mkt-trd-042 | What is portfolio heat?
> The total aggregate dollar risk committed across all open positions in an account: Total Heat = Sum(Risk_i) / Equity.
> Professional desks strictly cap total portfolio heat (typically between 5% and 8% of equity) to prevent multi-asset correlated liquidations.

> [!question]- mkt-trd-043 | Why is variance drag higher for volatile assets than for stable assets?
> Geometric growth approximates arithmetic mean minus half the variance: R_geo ~ mu - 0.5 * sigma^2.
> As volatility sigma rises, the variance drag penalty scales quadratically, severely suppressing net compounding returns.

> [!question]- mkt-trd-044 | How does an unhedged overnight gap violate standard intraday position sizing models?
> Standard position sizing assumes continuous price action where orders can exit at the predetermined stop price.
> An overnight gap bypasses the stop order completely, executing at the market open and incurring a loss significantly larger than 1R.

> [!question]- mkt-trd-045 | What is Martingale betting and why is it fatal in financial markets?
> Doubling the position size after every losing trade in an attempt to recover past losses on the first subsequent win.
> Because market drawdowns exhibit serial clustering, Martingale betting rapidly reaches capital limits, resulting in instantaneous account blowup.

> [!question]- mkt-trd-046 | What is Anti-Martingale sizing?
> Increasing position size as capital grows and decreasing size as capital shrinks (the foundational principle of fixed fractional and Kelly sizing).
> It maximizes capital compounding during favorable regimes while insulating the account during adverse streaks.

> [!question]- mkt-trd-047 | What is the Maximum Adverse Excursion (MAE)?
> The maximum unrealized peak-to-trough paper loss experienced by a trade from its entry point to its eventual exit.
> Analyzing MAE distributions helps traders set optimal stop-loss distances that avoid premature stop-outs on profitable setups.

> [!question]- mkt-trd-048 | What is the Maximum Favorable Excursion (MFE)?
> The maximum unrealized paper profit reached by a trade during its holding period before exit.
> Comparing MFE to realized profit reveals whether a trader is leaving excessive gains on the table through delayed profit-taking.

> [!question]- mkt-trd-049 | In continuous-time portfolio theory, what is the Merton optimal fraction of wealth invested in a risky asset?
> f* = (mu - r) / (gamma * sigma^2), where mu is expected asset return, r is risk-free rate, gamma is risk aversion, and sigma^2 is return variance.
> It represents the continuous-time generalization of the Kelly Criterion for risk-averse investors.

> [!question]- mkt-trd-050 | Why does the Kelly Criterion assume logarithmic utility U(W) = ln(W)?
> Logarithmic utility is the unique utility function that makes the optimal decision in a multi-period game independent of future opportunities.
> It naturally penalizes zero wealth with negative infinite utility, mathematically preventing voluntary bankruptcy.

> [!question]- mkt-trd-051 | How does fat-tailed (Student-t) kurtosis affect the optimal Kelly fraction?
> High kurtosis and negative skewness increase the frequency of extreme left-tail losses.
> To account for fat tails, the optimal fraction must be scaled down substantially below the Gaussian Kelly formula to avoid ruin.

> [!question]- mkt-trd-052 | What is a Chande Kroll stop and how does it incorporate volatility?
> An adaptive trailing stop that calculates the high/low over an N-period window and offsets stops by a multiple of the Average True Range.
> It trails price closely during quiet periods while automatically widening during high-volatility expansions to prevent shakeouts.

> [!question]- mkt-trd-053 | Explain the concept of asymmetric risk-to-reward calibration.
> Ensuring that the expected reward on winning trades is a multiple of the initial risk (e.g. 2R or 3R).
> Asymmetric payoffs allow a trader to maintain robust profitability even with a modest win rate of 35% to 45%.

> [!question]- mkt-trd-054 | What is a trailing stop and what is its operational trade-off?
> A dynamic stop-loss that ratchets in the direction of a winning trade as price advances, locking in unrealized gains.
> The trade-off: Trailing stops protect capital, but tight trailing parameters frequently stop out positions prematurely before major trend runs.

> [!question]- mkt-trd-055 | What is time-based invalidation (a time stop)?
> Exiting a trade if price fails to move in the expected direction within a predetermined number of bars or hours.
> It frees up capital and eliminates ongoing exposure when market momentum fails to confirm the entry thesis.

> [!question]- mkt-trd-056 | What is scaling in (pyramiding) and how should risk be managed during additions?
> Adding size to an existing position only after it has moved favorably and the stop-loss has been trailed to break-even.
> Pyramiding expands position size without ever increasing total open account risk beyond the initial 1R allocation.

> [!question]- mkt-trd-057 | Why does scaling into a losing position (averaging down) violate institutional risk rules?
> Averaging down increases dollar exposure precisely when the market has disproven the entry thesis.
> It exponentially increases the probability of an absorbing catastrophic drawdown on a single trade.

> [!question]- mkt-trd-058 | What is the difference between accounting stop and structural stop?
> An accounting stop is an arbitrary dollar or percentage loss (e.g. "I will risk $500" or "2%").
> A structural stop is placed at a technical market invalidation level (e.g. below a swing low or support shelf); position size is derived from this distance.

> [!question]- mkt-trd-059 | What is a circuit breaker in exchange trading?
> A regulatory mechanism that temporarily halts all trading across a market or individual stock following an extreme price drop (e.g. S&P 500 Level 1 halt at 7% decline).
> It prevents systemic panic cascade liquidations and provides a cooling-off period for order books to replenish.

> [!question]- mkt-trd-060 | What is the relationship between the Sharpe Ratio and the optimal Kelly fraction?
> In continuous time, the optimal Kelly fraction equals the Sharpe ratio divided by volatility: f* = Sharpe / sigma = (mu - r) / sigma^2.
> Higher Sharpe strategies allow greater capital commitment per unit of risk.

> [!question]- mkt-trd-061 | Why does liquidity constrain position sizing in small-cap equities?
> Position size must not exceed a small fraction (e.g. 1% to 2%) of Average Daily Volume (ADV).
> Exceeding volume limits causes severe market impact on entry and makes emergency liquidation during a panic impossible without devastating slippage.

> [!question]- mkt-trd-062 | What is a hard stop versus a mental stop?
> A hard stop is a resting stop-loss order placed in the exchange matching engine or broker server.
> A mental stop is an internal intention to exit manually when price reaches a level; mental stops routinely fail due to psychological hesitation during sudden drops.

> [!question]- mkt-trd-063 | What is cross-position diversification benefit in multi-asset sizing?
> If two uncorrelated assets each have daily volatility sigma, an equal-weight portfolio has volatility sigma / sqrt(2) = 0.707 * sigma.
> Diversification reduces portfolio variance without reducing expected return, allowing larger aggregate position sizing under a given risk budget.

> [!question]- mkt-trd-064 | What is the maximum acceptable drawdown threshold for an institutional discretionary trader?
> Most institutional prop desks enforce a hard drawdown stop between 5% and 10% of allocated capital.
> Breaching the 10% threshold triggers mandatory position de-risking, desk review, or temporary trading suspension.

---

## Further reading

- Kelly, J. L. (1956). *A new interpretation of information rate*. Bell System Technical Journal, 35(4), 917-926.
- Thorp, E. O. (2006). *The Kelly criterion in blackjack, sports betting, and the stock market*. In Handbook of asset and liability management (pp. 385-428). North-Holland.
- Vince, R. (1992). *The Mathematics of Money Management: Risk Analysis Techniques for Traders*. John Wiley & Sons.
- Chande, T. S., & Kroll, S. (1994). *The New Technical Trader: Boost Your Profit by Plugging into the Latest Indicators*. John Wiley & Sons.
