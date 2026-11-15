---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Magdon-Ismail Atiya Pratap and Abu-Mostafa (2004) - On the Maximum Drawdown of a Brownian Motion, Feller (1968) - An Introduction to Probability Theory and Its Applications Vol 1, Black and Perold (1992) - Theory of Constant Proportion Portfolio Insurance, Young (1991) - Calmar Ratio: A Smoother Tool, Vince (1992) - The Mathematics of Money Management]
---

# Drawdown Mathematics and Risk of Ruin

## TL;DR

- Loss asymmetry is non-linear: a 50% drawdown requires a 100% gain to break even, while a 90% drawdown requires a 900% gain, making capital preservation the mathematical prerequisite for compounding.
- Sequence of returns risk (SRR) dictates that the timing of losses matters decisively when external cash flows or withdrawals occur; early drawdowns permanently impair long-term terminal capital.
- With unit bets, no profit target and win probability $p > 1/2$, the classical probability of gambler's ruin from $k$ units is $((1-p)/p)^k$; for $p \le 1/2$ ruin is certain, so a small edge only protects you if the bet is small relative to capital.
- For log wealth following Brownian motion with drift $\alpha > 0$ and volatility $\sigma$, the probability of ever falling by $D$ (in log terms) is exactly $\exp(-2\alpha D / \sigma^2)$.
- Leverage scales volatility drag quadratically: the log growth rate is $\mu - \frac{1}{2}\sigma^2$, so levered volatility without enough drift erodes capital over time.

## Learning objectives

- Derive the non-linear relationship between portfolio drawdown percentage and required breakeven return.
- Calculate and interpret path-dependent metrics: Maximum Drawdown (MDD), Average Drawdown, Underwater Duration, and Ulcer Index.
- Compute the probability of ruin across discrete Bernoulli trials and continuous Brownian motion paths.
- Quantify sequence of returns risk (SRR) under continuous capital extraction schedules.
- Formulate dynamic portfolio protection mechanisms including Constant Proportion Portfolio Insurance (CPPI) and volatility targeting.

## Core concepts

### 1. The Asymmetry of Losses and Mathematical Non-Linearity

Portfolio drawdowns exhibit strict mathematical asymmetry:

$$R_{\text{rec}} = \frac{D}{1 - D}$$

where $D \in [0, 1)$ is the percentage drawdown from the peak, and $R_{\text{rec}}$ is the rate of return required to return to the previous high-water mark.

```
+-----------------------------------------------------------------------+
|                    THE NON-LINEAR RECOVERY TRAP                       |
+-----------------------------------------------------------------------+
| Drawdown (D)  | Loss Factor | Required Gain (R_rec) | 1 / (1 - D)     |
|---------------+-------------+-----------------------+-----------------|
| -10.0%        | 0.90x       | +11.11%               | 1.11x           |
| -20.0%        | 0.80x       | +25.00%               | 1.25x           |
| -30.0%        | 0.70x       | +42.86%               | 1.43x           |
| -40.0%        | 0.60x       | +66.67%               | 1.67x           |
| -50.0%        | 0.50x       | +100.00%              | 2.00x           |
| -60.0%        | 0.40x       | +150.00%              | 2.50x           |
| -75.0%        | 0.25x       | +300.00%              | 4.00x           |
| -90.0%        | 0.10x       | +900.00%              | 10.00x          |
| -95.0%        | 0.05x       | +1,900.00%            | 20.00x          |
| -99.0%        | 0.01x       | +9,900.00%            | 100.00x         |
+-----------------------------------------------------------------------+
```

Between 0% and 20% drawdown, the recovery curve appears roughly linear.
The curvature $\frac{d^2 R_{\text{rec}}}{dD^2} = \frac{2}{(1 - D)^3}$ grows without bound as $D \to 1$: it is 5.83 at $D = 30\%$ and 16 at $D = 50\%$.
Once a fund enters a 50% drawdown, it must double its remaining equity merely to break even.
At an annualized return of 10%, recovering from a 50% loss takes $\ln 2 / \ln 1.1 = 7.27$ years of uninterrupted compounding.

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
   Measures annualized compound return relative to the maximum peak-to-trough drawdown over a window; Young (1991, Futures) originally used the trailing 36 months.

2. **Sterling Ratio**:
   $$\text{Sterling} = \frac{\text{CAGR}}{|\text{Average Annual Maximum Drawdown}| + 10\%}$$
   Normalizes return by the average of the yearly maximum drawdowns rather than a single outlier event.
   It is often written as "average drawdown minus 10%" with drawdowns as negative numbers, which is the same thing; variants exist, so state the one you use.

3. **Burke Ratio**:
   $$\text{Burke} = \frac{R_p - R_f}{\sqrt{\sum_{i=1}^n D_i^2}}$$
   Penalizes both the depth and frequency of all drawdowns by summing squared drawdown excursions.

4. **Ulcer Index (UI)**:
   $$\text{UI} = \sqrt{\frac{1}{N} \sum_{t=1}^N (100 \times D(t))^2}$$
   Measures the quadratic mean of percentage drawdowns across every observation, capturing both the depth and the duration of time spent underwater.

### 3. Continuous Brownian Motion Drawdown Dynamics

Consider a portfolio value $W(t)$ following Geometric Brownian Motion with drift $\mu$ and volatility $\sigma$:

$$d\ln W(t) = \left(\mu - \frac{1}{2}\sigma^2\right)dt + \sigma dZ(t)$$

Let $\alpha = \mu - \frac{1}{2}\sigma^2$ be the geometric drift.
Magdon-Ismail, Atiya, Pratap and Abu-Mostafa (2004) derived the expected maximum drawdown over time $T$ of a Brownian motion with drift $\alpha$ and diffusion $\sigma$; for log wealth this is the maximum drawdown measured in log terms:

- When $\alpha = 0$ (zero drift), exactly:
  $$\mathbb{E}[\text{MDD}(T)] = \sqrt{\pi/2}\, \sigma \sqrt{T} = 1.2533 \sigma \sqrt{T}$$

- When $\alpha > 0$ (positive drift), as $T \to \infty$:
  $$\mathbb{E}[\text{MDD}(T)] \approx \frac{\sigma^2}{2\alpha} \left( \ln\left(\frac{2\alpha^2 T}{\sigma^2}\right) + 0.5772 \right)$$
  where 0.5772 is the Euler-Mascheroni constant; for example $\alpha = \sigma = 1$ and $T = 50$ gives 2.591.

Even with positive drift ($\alpha > 0$), the expected maximum drawdown keeps growing, but only logarithmically in time.
With zero drift it grows like $\sqrt{T}$ without bound, so a zero-edge strategy run long enough will eventually see arbitrarily deep drawdowns.

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
| 0.52         | 0.9231      | 44.91%       | 13.52%       | 1.83%        |
| 0.55         | 0.8182      | 13.44%       | 0.66%        | 0.0044%      |
| 0.60         | 0.6667      | 1.73%        | 0.0040%      | 0.00%        |
+-----------------------------------------------------------------------+
```

When $p \le 0.50$, the probability of ruin is exactly 1.0 (certainty), regardless of starting capital.
When $p > 0.50$, ruin probability decays exponentially with starting capital $C$.
If instead the bet is a fixed fraction of current wealth, wealth can never reach exactly zero, and the relevant question becomes the probability of ever falling to a given fraction of current wealth, which for log wealth with drift $\alpha > 0$ and volatility $\sigma$ is $\exp(-2\alpha D / \sigma^2)$ for a log decline $D$ (see the TL;DR and the Kelly note).

### 5. Sequence of Returns Risk (SRR)

Sequence of returns risk is the danger that the order of returns impairs portfolio longevity, even when long-term average returns match expectations.
SRR becomes destructive when capital is being withdrawn (e.g., retirement decumulation, hedge fund redemptions, management fee extractions).

Consider two hypothetical portfolios starting with $1,000,000, with $60,000 withdrawn at the end of the first year and the withdrawal raised 2% a year for inflation:

```
+-----------------------------------------------------------------------+
|              SEQUENCE OF RETURNS: BEAR FIRST VS BULL FIRST            |
+-----------------------------------------------------------------------+
| Year | Market Sequence A (Bear First)  | Market Sequence B (Bull First)|
|------+---------------------------------+-------------------------------|
| Y1   | -25.0% -> Capital: $690,000     | +25.0% -> Capital: $1,190,000 |
| Y2   | -15.0% -> Capital: $525,300     | +15.0% -> Capital: $1,307,300 |
| Y3   | -5.0%  -> Capital: $436,611     | +5.0%  -> Capital: $1,310,241 |
| Y4   | +5.0%  -> Capital: $394,769     | -5.0%  -> Capital: $1,181,056 |
| Y5   | +15.0% -> Capital: $389,039     | -15.0% -> Capital: $938,952   |
| Y6   | +25.0% -> Capital: $420,053     | -25.0% -> Capital: $637,969   |
+-----------------------------------------------------------------------+
```

Both sequences contain the same six returns, so without withdrawals they would end at the same wealth (a geometric mean of -1.49% a year).
Portfolio A ends with $420,053 against $637,969 for Portfolio B because it sells assets to fund withdrawals while prices are depressed, and the units sold cannot share in the later recovery.

### 6. Constant Proportion Portfolio Insurance (CPPI)

CPPI (Black and Perold 1992) is a dynamic allocation rule designed to protect a capital floor $F(t)$ while keeping upside equity participation.

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

To keep wealth at or above the floor $F(t)$, the largest sudden market drop $\Delta S / S$ between rebalancing intervals must not exceed $1/m$:

$$\Delta S_{\text{crash}} \le \frac{1}{m}$$

In a hypothetical example with $W = 100$, $F = 80$ and $m = 4$, the equity exposure is $4 \times 20 = 80$.
A 25% gap ($1/m$) takes wealth to $100 - 0.25 \times 80 = 80$, exactly the floor, while a 30% gap takes it to 76, below the floor.
If cushion $C(t) \to 0$, the portfolio shifts 100% to risk-free cash/bonds, triggering the "cash lock" trap where the portfolio can never recover if equity markets subsequently rally.

---

## Flashcard drill bank

> [!question]- mkt-pf-097 | What is the formula for the recovery return required to offset a drawdown D?
> R_rec = D / (1 - D).

> [!question]- mkt-pf-098 | Why is a 50% drawdown fundamentally more dangerous than two consecutive 25% drawdowns?
> Two 25% drawdowns compound to a 43.75% cumulative loss (1 - 0.75 * 0.75), which requires a 77.8% recovery, whereas a single 50% loss requires a 100% recovery; the deeper single loss sits further up the convex recovery curve.

> [!question]- mkt-pf-099 | What is a high-water mark (HWM) in portfolio management?
> The highest historical peak value achieved by a portfolio or fund, used as the baseline for calculating drawdowns and incentive fees.

> [!question]- mkt-pf-100 | What is the definition of Maximum Drawdown (MDD)?
> The maximum observed peak-to-trough percentage decline in portfolio equity over a specified historical horizon.

> [!question]- mkt-pf-101 | How is the Calmar ratio calculated?
> Annualized Compound Growth Rate (CAGR) divided by Maximum Drawdown (MDD) over a specified period (originally the trailing 36 months).

> [!question]- mkt-pf-102 | What is the Ulcer Index?
> A path-dependent volatility metric that computes the quadratic mean (RMS) of percentage drawdowns from the high-water mark across all time steps.

> [!question]- mkt-pf-103 | What is underwater duration?
> The total length of time a portfolio spends below its previous peak before establishing a new high-water mark.

> [!question]- mkt-pf-104 | What is the Sterling ratio?
> CAGR divided by the magnitude of the average annual maximum drawdown plus 10 percentage points (written "average drawdown minus 10%" when drawdowns are negative numbers).

> [!question]- mkt-pf-105 | What is the Burke ratio?
> Excess portfolio return divided by the square root of the sum of squared drawdowns.

> [!question]- mkt-pf-106 | In classical gambler's ruin with win probability p = 0.50 and unlimited target, what is the ruin probability?
> Exactly 1.0 (certainty of ruin), because a fair random walk is recurrent and hits zero with probability one.

> [!question]- mkt-pf-107 | What is the gambler's ruin formula for p > 0.5 with initial units C and no upper ceiling?
> P(Ruin) = (q / p)^C, where q = 1 - p.

> [!question]- mkt-pf-108 | In continuous geometric Brownian motion, how does expected MDD scale with time T when drift is zero?
> Exactly sqrt(pi / 2) * sigma * sqrt(T), about 1.2533 sigma sqrt(T) (Magdon-Ismail et al. 2004).

> [!question]- mkt-pf-109 | How does expected MDD scale with time T when geometric drift is positive (alpha > 0)?
> Logarithmically: for large T it is about (sigma^2 / (2 alpha)) (ln(2 alpha^2 T / sigma^2) + 0.5772).

> [!question]- mkt-pf-110 | What is Sequence of Returns Risk (SRR)?
> The risk that the chronological ordering of investment returns negatively impacts terminal wealth when capital withdrawals or additions occur.

> [!question]- mkt-pf-111 | Why does SRR not matter if there are zero cash inflows or outflows?
> Because portfolio compounding without cash flows is commutative: multiplication of returns yields the identical final wealth regardless of order.

> [!question]- mkt-pf-112 | What is variance decay or volatility drag in levered instruments?
> The reduction in compound growth caused by volatility: for lognormal returns the log growth rate is the arithmetic mean minus half the variance (mu - 0.5 * sigma^2), and leverage L scales the variance term by L^2.

> [!question]- mkt-pf-113 | In Constant Proportion Portfolio Insurance (CPPI), what is the cushion C(t)?
> Total portfolio wealth minus the predetermined guaranteed capital floor: C(t) = max(0, W(t) - F(t)).

> [!question]- mkt-pf-114 | What is the CPPI multiplier m?
> A constant scaling factor applied to the cushion to determine the dollar equity allocation: E(t) = m * C(t).

> [!question]- mkt-pf-115 | What is the maximum market gap drop a CPPI portfolio can tolerate before breaching its floor?
> Delta S / S <= 1 / m; e.g. 25% for m = 4.

> [!question]- mkt-pf-116 | What is the 'cash lock' problem in CPPI structures?
> If asset prices drop so severely that the cushion hits zero, the algorithm shifts 100% into cash and bonds, preventing participation in subsequent market recoveries.

> [!question]- mkt-pf-117 | How does volatility targeting reduce extreme portfolio drawdowns?
> By dynamically scaling position leverage inversely to forecasted volatility, reducing risk exposure when market volatility spikes.

> [!question]- mkt-pf-118 | Why does a fixed-fraction position sizing model prevent absolute mathematical ruin in discrete terms?
> Because losing a fixed fraction f of current equity on each loss never reaches exactly zero: after n straight losses W_n = W_0 * (1 - f)^n > 0, although it can fall to a fraction that is ruin in practice.

> [!question]- mkt-pf-119 | What is 'effective ruin' in commercial quantitative management?
> Reaching a drawdown at which investors redeem or lenders pull financing and the fund is forced to stop (the threshold varies by fund and mandate), regardless of theoretical asymptotic survival.

> [!question]- mkt-pf-120 | What is the difference between a trailing stop-loss and a hard price stop?
> A hard stop executes at a fixed nominal price, while a trailing stop moves upward with the high-water mark, locking in gains and capping peak-to-trough drawdowns.

> [!question]- mkt-pf-121 | What is an absorbing barrier in stochastic calculus?
> A state boundary that, once reached by a stochastic process, terminates the process with zero probability of exit.

> [!question]- mkt-pf-122 | How does fat-tailed (leptokurtic) return distribution affect empirical ruin probabilities?
> Extreme negative jump events vastly increase ruin probabilities compared to Gaussian normal models.

> [!question]- mkt-pf-123 | What is the Pain Index in portfolio performance measurement?
> The mean depth of drawdowns over a specified period, calculated as the integral of the drawdown curve divided by total time.

> [!question]- mkt-pf-124 | What is the primary operational cause of sudden hedge fund blowups?
> Excessive leverage combined with illiquid collateral during margin calls, forcing asset sales at liquidation prices.

> [!question]- mkt-pf-125 | What is the Martingale betting system, and why does it lead to ruin?
> Doubling the bet size after every loss; with finite bankrolls or table limits, an inevitable string of consecutive losses causes total ruin.

> [!question]- mkt-pf-126 | What is the Anti-Martingale betting strategy?
> Increasing position size as equity grows and decreasing position size during drawdowns, preserving capital during losing streaks.

> [!question]- mkt-pf-127 | How does cross-sectional diversification protect against portfolio drawdowns?
> Uncorrelated asset returns allow gains in unaffected assets to offset losses in declining assets, dampening the portfolio-level high-water mark drawdown.

> [!question]- mkt-pf-128 | What is the primary golden rule of drawdown risk management?
> Capital preservation comes first: avoid catastrophic losses that move the portfolio into the steep right-tail of the non-linear recovery curve.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_pm_04_drawdown_ruin.py`](../../code/mkt_pm_04_drawdown_ruin.py) prints and asserts every computed number on this page: recovery returns in exact fractions against bisection, the ruin table against an exact rational solve with a far barrier, a numerical solve of the difference equation and a seeded simulation, the Magdon-Ismail drawdown formulas against a seeded simulation extrapolated to zero step size, the sequence-of-returns table by recursion against a closed-form sum, and the CPPI gap test.
- Related notes: [Kelly Criterion and Capital Growth Theory](05-Kelly-Criterion-and-Capital-Growth-Theory.md) (drawdown probabilities under fractional Kelly), [Portfolio Rebalancing, Tax Drag, and Execution Friction](03-Portfolio-Rebalancing-Tax-Drag-and-Execution-Friction.md).

## Further reading

- Black, F., & Perold, A. F. (1992). *Theory of Constant Proportion Portfolio Insurance*. Journal of Economic Dynamics and Control, 16(3-4), 403-426.
- Feller, W. (1968). *An Introduction to Probability Theory and Its Applications* (Vol. 1, 3rd ed.), chapter XIV (random walk and ruin problems). John Wiley & Sons.
- Magdon-Ismail, M., Atiya, A. F., Pratap, A., & Abu-Mostafa, Y. S. (2004). *On the Maximum Drawdown of a Brownian Motion*. Journal of Applied Probability, 41(1), 147-161.
- Vince, R. (1992). *The Mathematics of Money Management: Risk Analysis Techniques for Traders*. John Wiley & Sons.
- Young, T. W. (1991). *Calmar Ratio: A Smoother Tool*. Futures, October 1991.
