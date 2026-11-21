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

Whether a trader with an edge compounds capital or goes broke depends as much on position sizing as on setup selection or entry timing.
A trader with a genuine edge who bets beyond the zero-growth fraction (about twice the Kelly fraction) sees log wealth drift down, and wealth goes to zero with probability 1 despite the edge.
A trader with a modest edge who sizes fractionally keeps positive growth and far smaller drawdowns.

---

## TL;DR

Position sizing dictates how much capital is committed to an idea based on the distance to the invalidation stop.
The Kelly Criterion maximizes the expected log-wealth growth rate, but full Kelly has deep drawdowns (in continuous time it halves wealth at some point with probability 1/2) and overshoots when parameters are estimated with error, so fractional Kelly (for example half Kelly) is the standard remedy (Thorp 2006).
For fixed-size even-money bets, risk of ruin decreases exponentially with the number of risk units:
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
   - Limits the risk of any single trade to a fixed percentage $f$ of current account equity (for example $1.0\%$):
     $$\text{Dollar Risk} = \text{Equity}_t \times f$$
     $$\text{Position Size } Q = \frac{\text{Equity}_t \times f}{|P_{\text{entry}} - P_{\text{stop}}|}$$
   - Automatically scales position size downward during drawdowns (preserving capital) and upward during winning streaks.

3. **Volatility Targeting (Risk Parity at the Trade Level)**:
   - Sizes positions such that each trade contributes an identical daily dollar volatility:
     $$Q_t = \frac{\text{Target Dollar Volatility}}{\text{ATR}_t \times \text{Multiplier}}$$
   - Prevents a single high-volatility position from dominating the risk of the book.

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
  Because real-world parameters $p$ and $b$ are estimated with error and returns exhibit fat tails, the usual remedy is to bet a fraction $c$ of Kelly, such as "Half-Kelly" ($0.50f^*$) or "Quarter-Kelly" ($0.25f^*$).
  In the continuous approximation a bet of $c f^*$ earns $(2c - c^2)$ of the maximum growth rate, so Half-Kelly captures $2(0.5) - 0.5^2 = 75\%$ of it.
  Return volatility scales with $f$, so Half-Kelly halves volatility and cuts variance to $25\%$ of full Kelly.
  Drawdowns shrink much faster: in continuous time (log wealth a Brownian motion with drift), the probability that wealth ever falls to a fraction $x$ of its starting value is $x^{2/c - 1}$, so full Kelly ($c = 1$) halves wealth at some point with probability $50\%$ and Half-Kelly with probability $0.5^3 = 12.5\%$.

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

The last column assumes a hypothetical steady 10% annual return after the drawdown, so recovery takes $\ln(1/(1-D)) / \ln(1.10)$ years.

| Drawdown ($D$) | Recovery Gain Required ($G$) | Years to recover at 10% a year |
|----------------|------------------------------|--------------------------------|
| **5.0%** | **5.26%** | 0.54 |
| **10.0%** | **11.11%** | 1.11 |
| **20.0%** | **25.00%** | 2.34 |
| **30.0%** | **42.86%** | 3.74 |
| **50.0%** | **100.00%** | 7.27 |
| **75.0%** | **300.00%** | 14.55 |
| **90.0%** | **900.00%** | 24.16 |

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
   - Half Kelly captures $\frac{0.022900}{0.029977} = 76.4\%$ of the maximum growth rate (close to the continuous approximation's 75%) while halving exposure and volatility.

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
   $$Q = \frac{\text{Dollar Risk Budget}}{\text{Stop Distance}} = \frac{\$1,500}{\$7.00} = 214.29 \implies 214\text{ shares (rounded down)}$$
2. **Calculate Total Position Value**:
   $$\text{Position Value} = 214 \times \$150.00 = \$32,100\text{ (32.1% of account equity)}$$
3. **Verify Dollar Risk on Invalidation**:
   $$\text{Actual Realized Risk} = 214 \times (\$150.00 - \$143.00) = 214 \times \$7.00 = \$1,498.00$$
   Rounding down keeps the dollar risk at $\$1,498$, within the $\$1,500$ (1.5%) budget, and because the stop is set in ATR units the budget holds whatever the stock's volatility.

---

## Pitfalls

- **Confusing Kelly with Maximum Comfort**:
  In the continuous-time model, full Kelly sees wealth fall to half its starting value at some point with probability $50\%$, and to a tenth with probability $10\%$.
  Few traders or capital allocators will sit through a $50\%$ drawdown, so the growth-optimal bet is rarely the bet that survives in practice.
- **Correlation Blindness (Total Portfolio Heat)**:
  Opening five trades risking $1.5\%$ each in five large technology stocks does not represent five independent bets.
  If they move together and all hit their stops, the combined loss is $5 \times 1.5\% = 7.5\%$ of equity on one factor.
- **Static Share Sizing**:
  Trading a static "1,000 shares" on a $\$20$ stock risks $\$500$ on a $\$0.50$ stop, but trading 1,000 shares on a $\$400$ stock with a $\$10$ stop risks $\$10,000$.
  Static share sizing exposes capital to random volatility shocks.
- **Ignoring Overnight Gap Risk**:
  A stop-loss order placed at $\$143.00$ does not protect against an overnight earnings report opening at $\$130.00$: the loss is $\$20$ per share instead of $\$7$, or $2.86R$.
  Cap position size so that a stated worst-case gap (for example $20\%$) stays within the maximum acceptable portfolio loss.

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

> [!question]- mkt-trd-036 | Why might a trader size at Fractional Kelly (e.g. Half-Kelly or Quarter-Kelly) rather than Full Kelly?
> Real-world win rates and payoff ratios are estimated with statistical uncertainty, and market returns exhibit fat-tailed jump risks.
> In the continuous approximation Half-Kelly keeps 75% of maximum growth while halving return volatility, and it cuts the probability of ever halving wealth from 50% to 12.5%.

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
> A heat cap is a policy choice, not a market standard; it bounds the loss if correlated positions all hit their stops together (five 1.5% risks are 7.5% of heat).

> [!question]- mkt-trd-043 | Why is variance drag higher for volatile assets than for stable assets?
> Geometric growth approximates arithmetic mean minus half the variance: R_geo ~ mu - 0.5 * sigma^2.
> As volatility sigma rises, the variance drag penalty scales quadratically, severely suppressing net compounding returns.

> [!question]- mkt-trd-044 | How does an unhedged overnight gap violate standard intraday position sizing models?
> Standard position sizing assumes continuous price action where orders can exit at the predetermined stop price.
> An overnight gap bypasses the stop order completely, executing at the market open and incurring a loss significantly larger than 1R.

> [!question]- mkt-trd-045 | What is Martingale betting and why is it fatal in financial markets?
> Doubling the position size after every losing trade in an attempt to recover past losses on the first subsequent win.
> Long losing streaks are certain to occur eventually and the stake grows as 2^k: in 1,000 fair even-money bets a run of 10 or more losses happens with probability 38.5%, by which point 1,023 units are lost and the next stake is 1,024 units.

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
> Kelly does not need a utility assumption: maximizing the long-run growth rate of wealth is the same as maximizing E[ln(W)] per bet, because log wealth is a sum of independent log returns (law of large numbers).
> Log utility also makes the policy myopic (the same bet each period whatever lies ahead), and ln(0) = -infinity means it never stakes everything on a bet that can lose it all.

> [!question]- mkt-trd-051 | How does fat-tailed (Student-t) kurtosis affect the optimal Kelly fraction?
> High kurtosis and negative skewness increase the frequency of extreme left-tail losses.
> A Gaussian approximation then overstates the growth-optimal fraction, so the fraction should come from the full return distribution or be scaled down below the Gaussian value.

> [!question]- mkt-trd-052 | What is a Chande Kroll stop and how does it incorporate volatility?
> An adaptive trailing stop that calculates the high/low over an N-period window and offsets stops by a multiple of the Average True Range.
> It trails price closely during quiet periods while automatically widening during high-volatility expansions to prevent shakeouts.

> [!question]- mkt-trd-053 | Explain the concept of asymmetric risk-to-reward calibration.
> Ensuring that the expected reward on winning trades is a multiple of the initial risk (e.g. 2R or 3R).
> At 2R the break-even win rate before costs is 1/3 (33.3%), so a 35% to 45% win rate is profitable before costs.

> [!question]- mkt-trd-054 | What is a trailing stop and what is its operational trade-off?
> A dynamic stop-loss that ratchets in the direction of a winning trade as price advances, locking in unrealized gains.
> The trade-off: Trailing stops protect capital, but tight trailing parameters frequently stop out positions prematurely before major trend runs.

> [!question]- mkt-trd-055 | What is time-based invalidation (a time stop)?
> Exiting a trade if price fails to move in the expected direction within a predetermined number of bars or hours.
> It frees up capital and eliminates ongoing exposure when market momentum fails to confirm the entry thesis.

> [!question]- mkt-trd-056 | What is scaling in (pyramiding) and how should risk be managed during additions?
> Adding size to an existing position after it has moved favorably.
> One common discipline is to add only once the stop on the existing size has been trailed far enough that total open risk, including the new unit, stays within the initial 1R allocation.

> [!question]- mkt-trd-057 | Why does scaling into a losing position (averaging down) violate institutional risk rules?
> Averaging down increases dollar exposure precisely when the market has disproven the entry thesis.
> It raises the loss if the thesis keeps failing, concentrating more capital in a single trade the further it goes against you.

> [!question]- mkt-trd-058 | What is the difference between accounting stop and structural stop?
> An accounting stop is an arbitrary dollar or percentage loss (e.g. "I will risk $500" or "2%").
> A structural stop is placed at a technical market invalidation level (e.g. below a swing low or support shelf); position size is derived from this distance.

> [!question]- mkt-trd-059 | What is a circuit breaker in exchange trading?
> A rule that halts trading after an extreme move; in the US (as of November 2026) the market-wide circuit breakers halt all equity trading for 15 minutes when the S&P 500 falls 7% (Level 1) or 13% (Level 2) from the prior close before 3:25 pm, and for the rest of the day at 20% (Level 3) under NYSE Rule 7.12, with single stocks governed by Limit Up-Limit Down pauses (NYSE Rule 7.11, in this form since 2013).
> It is intended to interrupt panic cascades and give order books time to refill.

> [!question]- mkt-trd-060 | What is the relationship between the Sharpe Ratio and the optimal Kelly fraction?
> In continuous time, the optimal Kelly fraction equals the Sharpe ratio divided by volatility: f* = Sharpe / sigma = (mu - r) / sigma^2.
> Higher Sharpe strategies allow greater capital commitment per unit of risk.

> [!question]- mkt-trd-061 | Why does liquidity constrain position sizing in small-cap equities?
> Market impact rises with order size relative to Average Daily Volume (ADV), so desks set a participation cap as a policy choice (for example a hypothetical 1% of ADV).
> A position that is many days of volume cannot be exited in a panic without large slippage.

> [!question]- mkt-trd-062 | What is a hard stop versus a mental stop?
> A hard stop is a resting stop-loss order placed in the exchange matching engine or broker server.
> A mental stop is an internal intention to exit manually when price reaches a level; mental stops routinely fail due to psychological hesitation during sudden drops.

> [!question]- mkt-trd-063 | What is cross-position diversification benefit in multi-asset sizing?
> If two uncorrelated assets each have daily volatility sigma, an equal-weight portfolio has volatility sigma / sqrt(2) = 0.707 * sigma.
> Diversification reduces portfolio variance without reducing expected return, allowing larger aggregate position sizing under a given risk budget.

> [!question]- mkt-trd-064 | What is the maximum acceptable drawdown threshold for an institutional discretionary trader?
> There is no public industry standard; each firm sets its own limits in the trader's mandate.
> The design principle is to cut risk well before a drawdown needs an implausible recovery: a 10% drawdown needs an 11.1% gain, a 20% drawdown 25%, a 50% drawdown 100%.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_trd_02_sizing_ruin.py`](../../code/mkt_trd_02_sizing_ruin.py) prints and asserts every number on this page: Kelly fractions by a grid search of the growth curve against the closed form, growth rates by compounding an explicit trade ledger and by seeded simulation within five standard errors, zero crossings by bisection, ruin probabilities by solving the absorbing Markov chain numerically, the Kelly drawdown probabilities by a finite-difference solution of the hitting-probability equation, recovery gains in exact fractions, and the martingale streak probability by dynamic programming checked by simulation.
- Related notes: [Retail Base Rates and Costs](01-Retail-Base-Rates-and-Costs.md), [Stop Logic and Trade Management](03-Stop-Logic-and-Trade-Management.md), [Probability and Decision Making](06-Probability-and-Decision-Making.md).

## Further reading

- Kelly, J. L. (1956). *A new interpretation of information rate*. Bell System Technical Journal, 35(4), 917-926.
- Thorp, E. O. (2006). *The Kelly criterion in blackjack, sports betting, and the stock market*. In Handbook of asset and liability management (pp. 385-428). North-Holland.
- Merton, R. C. (1969). *Lifetime portfolio selection under uncertainty: The continuous-time case*. The Review of Economics and Statistics, 51(3), 247-257.
- Vince, R. (1992). *The Mathematics of Money Management: Risk Analysis Techniques for Traders*. John Wiley & Sons.
- Chande, T. S., & Kroll, S. (1994). *The New Technical Trader: Boost Your Profit by Plugging into the Latest Indicators*. John Wiley & Sons.
