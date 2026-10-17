---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Magdon-Ismail et al. (2004) - On the Maximum Drawdown of a Brownian Motion, Taleb (2007) - The Black Swan, Vince (1992) - The Mathematics of Money Management, Feller (1968) - An Introduction to Probability Theory and Its Applications]
---

# Drawdown Mathematics and Risk of Ruin

## TL;DR

- Loss asymmetry is non-linear: a 50% drawdown requires a 100% gain to break even, while a 90% drawdown requires a 900% gain, making capital preservation the mathematical prerequisite for compounding.
- Sequence of returns risk (SRR) dictates that the timing of losses matters decisively when external cash flows or withdrawals occur; early drawdowns permanently impair long-term terminal capital.
- The classical probability of gambler's ruin in a biased random walk is $P(\text{ruin}) = ((1-p)/p)^k$, demonstrating that even positive-expectancy systems face mathematical certainty of ruin when position sizing is reckless.
- In continuous diffusion models with drift $\mu > 0$ and volatility $\sigma$, the probability of hitting an absorbing barrier at drawdown level $D$ scales as $\exp(-2\mu D / \sigma^2)$.
- Leverage creates path-dependent volatility drag through variance decay ($-\frac{1}{2}\sigma^2$), ensuring that levered volatility without sufficient drift erodes capital over time.

## Learning objectives

- Derive the non-linear relationship between portfolio drawdown percentage and required breakeven return.
- Calculate and interpret path-dependent metrics: Maximum Drawdown (MDD), Average Drawdown, Underwater Duration, and Ulcer Index.
- Compute the probability of ruin across discrete Bernoulli trials and continuous Brownian motion paths.
- Quantify sequence of returns risk (SRR) under continuous capital extraction schedules.
- Formulate dynamic portfolio protection mechanisms including Constant Proportion Portfolio Insurance (CPPI) and volatility targeting.

## Core concepts

### 1. The Asymmetry of Losses and Mathematical Non-Linearity

Portfolio drawdowns exhibit strict mathematical asymmetry governed by the harmonic relation:

$$R_{\text{rec}} = \frac{D}{1 - D}$$

where $D \in [0, 1)$ is the percentage drawdown from the peak, and $R_{\text{rec}}$ is the rate of return required to return to the previous high-water mark.

```
+-----------------------------------------------------------------------+
|                    THE NON-LINEAR RECOVERY TRAP                       |
+-----------------------------------------------------------------------+
| Drawdown (D)  | Loss Factor | Required Gain (R_rec) | Relative Effort |
|---------------+-------------+-----------------------+-----------------|
| -10.0%        | 0.90x       | +11.11%               | 1.1x            |
| -20.0%        | 0.80x       | +25.00%               | 1.25x           |
| -30.0%        | 0.70x       | +42.86%               | 1.43x           |
| -40.0%        | 0.60x       | +66.67%               | 1.67x           |
| -50.0%        | 0.50x       | +100.00%              | 2.0x            |
| -60.0%        | 0.40x       | +150.00%              | 2.5x            |
| -75.0%        | 0.25x       | +300.00%              | 4.0x            |
| -90.0%        | 0.10x       | +900.00%              | 10.0x           |
| -95.0%        | 0.05x       | +1,900.00%            | 20.0x           |
| -99.0%        | 0.01x       | +9,900.00%            | 100.0x          |
+-----------------------------------------------------------------------+
```

Between 0% and 20% drawdown, the recovery curve appears roughly linear.
Beyond 30%, the second derivative $\frac{d^2 R_{\text{rec}}}{dD^2} = \frac{2}{(1 - D)^3}$ explodes.
Once a fund enters a 50% drawdown, it must double its remaining equity merely to break even.
At an annualized return of 10%, recovering from a 50% loss takes approximately 7.27 years of flawless compounding without subsequent setbacks.

### 2. Maximum Drawdown and Path-Dependent Risk Metrics

Standard deviation $\sigma$ treats upside volatility and downside volatility symmetrically, obscuring path-dependent catastrophic risk.
Quantitative risk management uses drawdown metrics defined on the wealth path $W(t)$:

The running high-water mark $M(t)$ is defined as:

$$M(t) = \sup_{0 \le s \le t} W(s)$$

The instantaneous drawdown percentage $D(t)$ is:

$$D(t) = \frac{M(t) - W(t)}{M(t)} \in [0, 1]$$

The Maximum Drawdown over horizon $T$ is:

$$\text{MDD}(T) = \sup_{0 \le t \le T} D(t) = \sup_{0 \le t \le T} \left( \frac{M(t) - W(t)}{M(t)} \right)$$

Key drawdown-adjusted performance ratios include:

1. **Calmar Ratio**:
   $$\text{Calmar} = \frac{\text{CAGR}}{\text{MDD}}$$
   Measures annualized compound return relative to historical maximum peak-to-trough drawdown over a specified window (typically 36 months).

2. **Sterling Ratio**:
   $$\text{Sterling} = \frac{\text{CAGR}}{\text{Average Annual Drawdown} - 10\%}$$
   Normalizes return by average annual drawdowns rather than a single outlier event.

3. **Burke Ratio**:
   $$\text{Burke} = \frac{R_p - R_f}{\sqrt{\sum_{i=1}^n D_i^2}}$$
   Penalizes both the depth and frequency of all drawdowns by summing squared drawdown excursions.

4. **Ulcer Index (UI)**:
   $$\text{UI} = \sqrt{\frac{1}{N} \sum_{t=1}^N (100 \times D(t))^2}$$
   Measures the quadratic mean of percentage drawdowns across every single trading day, capturing the psychological stress and capital impairment of being underwater.

### 3. Continuous Brownian Motion Drawdown Dynamics

Consider a portfolio value $W(t)$ following Geometric Brownian Motion with drift $\mu$ and volatility $\sigma$:

$$d\ln W(t) = \left(\mu - \frac{1}{2}\sigma^2\right)dt + \sigma dZ(t)$$

Let $\alpha = \mu - \frac{1}{2}\sigma^2$ be the geometric drift.
Magdon-Ismail et al. (2004) proved that for an arithmetic Brownian motion with drift $\alpha$ and diffusion $\sigma$, the expected maximum drawdown over time $T$ behaves asymptotically:

- When $\alpha = 0$ (zero drift):
  $$\mathbb{E}[\text{MDD}(T)] \approx 1.2533 \sigma \sqrt{T}$$

- When $\alpha > 0$ (positive drift):
  $$\mathbb{E}[\text{MDD}(T)] \approx \frac{\sigma^2}{2\alpha} \left( \ln\left(\frac{2\alpha^2 T}{\sigma^2}\right) + 0.5772 \right)$$

This demonstrates that even with positive expected return ($\alpha > 0$), maximum drawdown grows logarithmically with time.
In the absence of positive drift, drawdown scales with $\sqrt{T}$, guaranteeing that unhedged zero-alpha trading systems eventually suffer unbounded drawdowns.

### 4. Classical Gambler's Ruin and Finite Capital Boundaries

In discrete time, consider an investor starting with capital $C$ who wagers unit stake $1$ on independent bets with win probability $p$ and loss probability $q = 1 - p$.
Let the absorbing boundary of ruin be capital $0$, and target wealth be $B > C$.

The probability of ruin $P(\text{Ruin} \mid C)$ is derived from the difference equation:

$$P(C) = p \cdot P(C + 1) + q \cdot P(C - 1)$$

with boundary conditions $P(0) = 1$ and $P(B) = 0$.
The general solution for $p \ne q$ is:

$$P(\text{Ruin} \mid C) = \frac{\left(\frac{q}{p}\right)^B - \left(\frac{q}{p}\right)^C}{\left(\frac{q}{p}\right)^B - 1}$$

As the target boundary $B \to \infty$ (investing without an upper cap):

$$P(\text{Ruin} \mid C) = \begin{cases} 1 & \text{if } p \le \frac{1}{2} \\ \left(\frac{q}{p}\right)^C & \text{if } p > \frac{1}{2} \end{cases}$$

```
+-----------------------------------------------------------------------+
|                    PROBABILITY OF RUIN P(Ruin)                        |
+-----------------------------------------------------------------------+
| Win Prob (p) | Ratio (q/p) | Units C = 10 | Units C = 25 | Units C = 50 |
|--------------+-------------+--------------+--------------+--------------|
| 0.48         | 1.0833      | 100.00%      | 100.00%      | 100.00%      |
| 0.50         | 1.0000      | 100.00%      | 100.00%      | 100.00%      |
| 0.52         | 0.9231      | 44.64%       | 13.06%       | 1.70%        |
| 0.55         | 0.8182      | 13.44%       | 0.69%        | 0.005%       |
| 0.60         | 0.6667      | 1.73%        | 0.004%       | ~0.00%       |
+-----------------------------------------------------------------------+
```

When $p \le 0.50$, the probability of ruin is exactly 1.0 (certainty), regardless of starting capital.
When $p > 0.50$, ruin probability decays exponentially with starting capital $C$.
However, if the bet size is variable or proportional to wealth, the continuous boundary condition shifts.

### 5. Sequence of Returns Risk (SRR)

Sequence of returns risk is the danger that the order of returns impairs portfolio longevity, even when long-term average returns match expectations.
SRR becomes destructive when capital is being withdrawn (e.g., retirement decumulation, hedge fund redemptions, management fee extractions).

Consider two portfolios starting with $1,000,000 with annual withdrawals of $60,000 (adjusted 2% for inflation):

```
+-----------------------------------------------------------------------+
|              SEQUENCE OF RETURNS: BEAR FIRST VS BULL FIRST            |
+-----------------------------------------------------------------------+
| Year | Market Sequence A (Bear First)  | Market Sequence B (Bull First)|
|------+---------------------------------+-------------------------------|
| Y1   | -25.0% -> Capital: $690,000     | +25.0% -> Capital: $1,190,000 |
| Y2   | -15.0% -> Capital: $525,300     | +15.0% -> Capital: $1,307,300 |
| Y3   | -5.0%  -> Capital: $436,635     | +5.0%  -> Capital: $1,309,865 |
| Y4   | +5.0%  -> Capital: $394,867     | -5.0%  -> Capital: $1,180,772 |
| Y5   | +15.0% -> Capital: $388,497     | -15.0% -> Capital: $938,056   |
| Y6   | +25.0% -> Capital: $418,021     | -25.0% -> Capital: $634,942   |
+-----------------------------------------------------------------------+
```

Although both sequences have the exact same geometric compound return before withdrawals (+0.54% annualized), Portfolio A is crippled by withdrawing capital while asset prices are depressed.
The liquidated units can never recover during the subsequent bull market.

### 6. Constant Proportion Portfolio Insurance (CPPI)

CPPI is a dynamic hedging algorithm designed to guarantee a capital floor $F(t)$ while maintaining upside equity participation.

Let total portfolio wealth be $W(t)$ and guaranteed minimum floor be $F(t)$.
The cushion $C(t)$ is defined as:

$$C(t) = \max(0, W(t) - F(t))$$

The equity allocation $E(t)$ is determined by a multiplier $m > 1$:

$$E(t) = m \cdot C(t)$$

The remainder of the portfolio is invested in safe risk-free debt:

$$B(t) = W(t) - E(t) = W(t) - m \cdot C(t)$$

```
        CUSHION-BASED DYNAMIC ALLOCATION
        
Total Wealth W(t) --------------------------->
                      |
                      v
      +-------------------------------+
      |  Cushion C(t) = W(t) - F(t)  |
      +-------------------------------+
            |                   |
            v                   v
      Equity E(t) = m*C   Bonds B(t) = W - E
```

To guarantee that wealth never breaches floor $F(t)$, the maximum sudden market drop $\Delta S / S$ between rebalancing intervals must not exceed $1/m$:

$$\Delta S_{\text{crash}} \le \frac{1}{m}$$

If multiplier $m = 4$, the floor is preserved as long as the market does not gap down by more than $25\%$ before the manager can rebalance.
If cushion $C(t) \to 0$, the portfolio shifts 100% to risk-free cash/bonds, triggering the "cash lock" trap where the portfolio can never recover if equity markets subsequently rally.

---

## Flashcard drill bank

> [!question] mkt-pf-097 | What is the formula for the recovery return required to offset a drawdown D?
> R_rec = D / (1 - D).

> [!question] mkt-pf-098 | Why is a 50% drawdown fundamentally more dangerous than two consecutive 25% drawdowns?
> Two 25% drawdowns compound to a 43.75% cumulative loss (1 - 0.75 * 0.75), which requires a 77.8% recovery, whereas a single 50% loss requires a 100% recovery.

> [!question] mkt-pf-099 | What is a high-water mark (HWM) in portfolio management?
> The highest historical peak value achieved by a portfolio or fund, used as the baseline for calculating drawdowns and incentive fees.

> [!question] mkt-pf-100 | What is the definition of Maximum Drawdown (MDD)?
> The maximum observed peak-to-trough percentage decline in portfolio equity over a specified historical horizon.

> [!question] mkt-pf-101 | How is the Calmar ratio calculated?
> Annualized Compound Growth Rate (CAGR) divided by Maximum Drawdown (MDD) over a specified period.

> [!question] mkt-pf-102 | What is the Ulcer Index?
> A path-dependent volatility metric that computes the quadratic mean (RMS) of percentage drawdowns from the high-water mark across all time steps.

> [!question] mkt-pf-103 | What is underwater duration?
> The total length of time a portfolio spends below its previous peak before establishing a new high-water mark.

> [!question] mkt-pf-104 | What is the Sterling ratio?
> CAGR divided by the average annual drawdown minus an arbitrary threshold (conventionally 10%).

> [!question] mkt-pf-105 | What is the Burke ratio?
> Excess portfolio return divided by the square root of the sum of squared drawdowns.

> [!question] mkt-pf-106 | In classical gambler's ruin with win probability p = 0.50 and unlimited target, what is the ruin probability?
> Exactly 1.0 (certainty of ruin), because a fair random walk is recurrent and hits zero with probability one.

> [!question] mkt-pf-107 | What is the gambler's ruin formula for p > 0.5 with initial units C and no upper ceiling?
> P(Ruin) = (q / p)^C, where q = 1 - p.

> [!question] mkt-pf-108 | In continuous geometric Brownian motion, how does expected MDD scale with time T when drift is zero?
> It scales proportionally to sigma * sqrt(T).

> [!question] mkt-pf-109 | How does expected MDD scale with time T when geometric drift is positive (alpha > 0)?
> It scales logarithmically with time: proportional to (sigma^2 / (2 * alpha)) * ln(T).

> [!question] mkt-pf-110 | What is Sequence of Returns Risk (SRR)?
> The risk that the chronological ordering of investment returns negatively impacts terminal wealth when capital withdrawals or additions occur.

> [!question] mkt-pf-111 | Why does SRR not matter if there are zero cash inflows or outflows?
> Because portfolio compounding without cash flows is commutative: multiplication of returns yields the identical final wealth regardless of order.

> [!question] mkt-pf-112 | What is variance decay or volatility drag in levered instruments?
> The mathematical reduction in compound growth caused by volatility: geometric growth rate equals arithmetic mean minus one-half variance (mu - 0.5 * sigma^2).

> [!question] mkt-pf-113 | In Constant Proportion Portfolio Insurance (CPPI), what is the cushion C(t)?
> Total portfolio wealth minus the predetermined guaranteed capital floor: C(t) = max(0, W(t) - F(t)).

> [!question] mkt-pf-114 | What is the CPPI multiplier m?
> A constant scaling factor applied to the cushion to determine the dollar equity allocation: E(t) = m * C(t).

> [!question] mkt-pf-115 | What is the maximum market gap drop a CPPI portfolio can tolerate before breaching its floor?
> Delta S / S <= 1 / m.

> [!question] mkt-pf-116 | What is the 'cash lock' problem in CPPI structures?
> If asset prices drop so severely that the cushion hits zero, the algorithm shifts 100% into cash and bonds, preventing participation in subsequent market recoveries.

> [!question] mkt-pf-117 | How does volatility targeting reduce extreme portfolio drawdowns?
> By dynamically scaling position leverage inversely to forecasted volatility, reducing risk exposure when market volatility spikes.

> [!question] mkt-pf-118 | Why does a fixed-fraction position sizing model prevent absolute mathematical ruin in discrete terms?
> Because risking a fixed fraction f of equity mathematically never reaches zero in continuous theory (W_n = W_0 * (1 - f)^n > 0 for all finite n).

> [!question] mkt-pf-119 | What is 'effective ruin' in commercial quantitative management?
> Reaching a drawdown threshold (e.g., -25% or -30%) where investors redeem capital and the fund is involuntarily liquidated, regardless of theoretical asymptotic survival.

> [!question] mkt-pf-120 | What is the difference between a trailing stop-loss and a hard price stop?
> A hard stop executes at a fixed nominal price, while a trailing stop moves upward with the high-water mark, locking in gains and capping peak-to-trough drawdowns.

> [!question] mkt-pf-121 | What is an absorbing barrier in stochastic calculus?
> A state boundary that, once reached by a stochastic process, terminates the process with zero probability of exit.

> [!question] mkt-pf-122 | How does fat-tailed (leptokurtic) return distribution affect empirical ruin probabilities?
> Extreme negative jump events vastly increase ruin probabilities compared to Gaussian normal models.

> [!question] mkt-pf-123 | What is the Pain Index in portfolio performance measurement?
> The mean depth of drawdowns over a specified period, calculated as the integral of the drawdown curve divided by total time.

> [!question] mkt-pf-124 | What is the primary operational cause of sudden hedge fund blowups?
> Excessive leverage combined with illiquid collateral during margin calls, forcing asset sales at liquidation prices.

> [!question] mkt-pf-125 | What is the Martingale betting system, and why does it lead to ruin?
> Doubling the bet size after every loss; with finite bankrolls or table limits, an inevitable string of consecutive losses causes total ruin.

> [!question] mkt-pf-126 | What is the Anti-Martingale betting strategy?
> Increasing position size as equity grows and decreasing position size during drawdowns, preserving capital during losing streaks.

> [!question] mkt-pf-127 | How does cross-sectional diversification protect against portfolio drawdowns?
> Uncorrelated asset returns allow gains in unaffected assets to offset losses in declining assets, dampening the portfolio-level high-water mark drawdown.

> [!question] mkt-pf-128 | What is the primary golden rule of drawdown risk management?
> Capital preservation comes first: avoid catastrophic losses that move the portfolio into the steep right-tail of the non-linear recovery curve.

---

## Further reading

- Feller, W. (1968). *An Introduction to Probability Theory and Its Applications* (Vol. 1, 3rd ed.). John Wiley & Sons.
- Magdon-Ismail, M., Atiya, A. F., Pratap, A., & Abu-Mostafa, Y. S. (2004). *On the Maximum Drawdown of a Brownian Motion*. Journal of Applied Probability, 41(1), 147-161.
- Taleb, N. N. (2007). *The Black Swan: The Impact of the Highly Improbable*. Random House.
- Vince, R. (1992). *The Mathematics of Money Management: Risk Analysis Techniques for Traders*. John Wiley & Sons.
