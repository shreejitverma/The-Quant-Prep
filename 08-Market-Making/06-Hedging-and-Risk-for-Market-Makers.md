---
type: concept
track: [quant-trader]
tier: core
status: solid
prereqs: [quote-management-skew-width-and-size, the-greeks]
est_hours: 3
sources: [Lebron (2019) The Laws of Trading. Wiley, Sinclair (2013) Volatility Trading. 2nd edition. Wiley, Hull. Options Futures and Other Derivatives. Pearson (minimum-variance hedge ratio), Whalley and Wilmott (1997) An asymptotic analysis of an optimal hedging model for option pricing with transaction costs. Mathematical Finance 7(3) 307-324, SEC Rule 15c3-5 (17 CFR 240.15c3-5) Risk management controls for brokers or dealers with market access, SEC (2013) In the Matter of Knight Capital Americas LLC. Release No. 34-70694]
---

# Hedging and Risk for Market Makers

## TL;DR

- A market maker wants to earn spread, not to hold a view, so it hedges the inventory that quoting leaves behind, first by netting across its own book and then with the cheapest well-correlated instrument.
- The minimum-variance hedge ratio is $h^* = \rho\,\sigma_A/\sigma_H$ (the regression beta) and the residual volatility is $\sigma_A\sqrt{1 - \rho^2}$: a hedge with $\rho = 0.6$ removes only 20% of the risk.
- Hedge aggressively when the cost of crossing is smaller than the risk of waiting; hedge passively (or skew) when the position is small relative to the cost; use bands rather than continuous rebalancing.
- Limits come in layers: soft limits change quoting, hard limits block risk-increasing orders, and stop limits flatten and escalate to a human.
- Kill switches must be automatic, independent of the strategy process, fail closed, and cover losses, positions, order and fill rates, stale data and position mismatches.

## Learning objectives

- Hedge inventory with correlated instruments and quantify basis risk.
- Set position, Greek and loss limits and design kill switches.
- Decide between passive and aggressive hedging.

## Core concepts

### What needs hedging

- Delta or inventory: the net directional exposure left by fills.
- For options books, gamma, vega by expiry and strike bucket, and higher-order Greeks; see [The Greeks](../05-Derivatives-and-Volatility/05-The-Greeks.md) and [Delta Hedging and Gamma Scalping](../05-Derivatives-and-Volatility/06-Delta-Hedging-and-Gamma-Scalping.md).
- Basis: the difference between the thing you hold and the thing you hedge with.
- Factor and correlation exposure across a book of many names.

The first hedge is free: offsetting positions inside the book (long one stock, short a correlated one; long calls from one client, short calls to another) net before any external trade.
Then choose external hedges on three criteria: correlation to the risk, cost to trade (spread, fees, market impact) and capacity.

### Minimum-variance hedge

Hold one unit of asset $A$ and short $h$ units of hedge $H$.
The variance of the hedged position is $\sigma_A^2 - 2h\rho\sigma_A\sigma_H + h^2\sigma_H^2$, minimised at

$$
h^* = \rho\frac{\sigma_A}{\sigma_H} = \frac{\operatorname{Cov}(A, H)}{\operatorname{Var}(H)}, \qquad
\sigma_{\text{resid}} = \sigma_A\sqrt{1 - \rho^2}.
$$

That is the regression beta of $A$ on $H$.
The fraction of volatility removed is $1 - \sqrt{1 - \rho^2}$, which is small unless $\rho$ is high: 20% at $\rho = 0.6$, 56% at 0.9, 69% at 0.95 and 86% at 0.99.
With several hedge instruments the ratios come from a multiple regression, $h^* = \Sigma_{HH}^{-1}\Sigma_{HA}$.
Estimate on returns sampled slowly enough to avoid asynchronous-price bias, and re-estimate: correlations fall in some stress regimes, exactly when you need the hedge.

### Passive versus aggressive hedging

Crossing the spread costs the half-spread plus the taker fee now.
Waiting to hedge passively earns the half-spread and rebate if filled, but leaves the position exposed to price risk and to adverse selection on the passive hedge fill.
With CARA-style risk pricing the cost of waiting $T$ seconds with $n$ shares is about $\frac12\gamma n^2\sigma^2 T$ (plus any expected drift your signals predict against you), so the break-even waiting time is

$$
T^* = \frac{\text{aggressive cost} + \text{passive edge}}{\tfrac12\gamma n^2 \sigma^2}.
$$

Because the risk term grows with $n^2$, small positions are hedged passively or by skewing and large ones aggressively.
Most desks use a band: do nothing inside $|\Delta| < b$, skew quotes as $|\Delta|$ approaches $b$, and hedge back toward the band edge (not to zero) when outside it.
Whalley and Wilmott (1997) show that for an option hedger with proportional costs the optimal no-trade band scales with the cube root of the transaction cost, so doubling costs widens the band by only about 26%.

### Limits

Limits encode the firm's risk appetite and live at several levels.

- Position: per instrument, per underlying, net delta, gross notional, concentration.
- Greeks: delta, gamma, vega per expiry bucket, and scenario losses (for example the book's P&L under a 10% move or a vol shock).
- Loss: daily, rolling intraday windows (such as 5 minutes), and drawdown from the day's peak.
- Order-level (pre-trade): maximum order size and notional, price bands against theo or the NBBO, maximum message and order rates, self-trade prevention.

Tier them.
A soft limit changes behaviour (more skew, less size, wider quotes).
A hard limit blocks orders that would increase risk while still allowing risk-reducing ones.
A stop limit cancels all quotes, may flatten, and requires a human to restart.
Size limits from the risk they allow: for example a one-day 99% value-at-risk budget divided by $z_{0.99}\,\sigma_{\text{1d}}$ per share gives a position limit; see [VaR and Expected Shortfall](../11-Risk-and-Trading/03-VaR-and-Expected-Shortfall.md) and [Drawdowns and Risk Limits](../11-Risk-and-Trading/05-Drawdowns-and-Risk-Limits.md).

### Kill switches

A kill switch stops trading automatically when the system is doing something it should not.
Common triggers:

- Loss beyond a threshold in a rolling window, or total daily loss.
- Position or Greek beyond a hard limit.
- Fill rate or order rate far outside normal (a runaway loop or a stale quote being picked off repeatedly).
- Market data stale, gapped or crossed; loss of a session; unacknowledged orders piling up.
- Internal position disagreeing with the exchange drop copy or clearing records.
- High reject rate from the venue.

Design rules: the switch runs outside the strategy process (in a risk gateway or separate service) so a bug in the strategy cannot disable it; it fails closed (if the risk service cannot confirm state, orders stop); it uses exchange-side tools where available (mass cancel, cancel-on-disconnect); and it needs deliberate human action to reset.
In the US, SEC Rule 15c3-5 (the market access rule, adopted in 2010) requires broker-dealers with market access to maintain pre-trade risk controls such as credit and capital thresholds and erroneous-order checks.
The standard cautionary case is Knight Capital in August 2012: the SEC's 2013 order describes a deployment error that sent millions of unintended orders in about 45 minutes and a loss of more than 460 million dollars, with inadequate automated controls to stop it.
See [Risk Checks and Order Management](../12-Quant-Development/13-Risk-Checks-and-Order-Management.md).

## Worked examples

### Example 1: hedging a stock with index futures

You are long 1,000,000 dollars of a stock with 2% daily volatility and want to hedge with index futures of 1% daily volatility; the correlation is 0.6.
$h^* = 0.6 \times 2\% / 1\% = 1.2$, so short 1,200,000 dollars of futures.
Unhedged daily standard deviation: 20,000 dollars.
Hedged: $2\% \times \sqrt{1 - 0.36} = 1.6\%$, or 16,000 dollars.
The hedge removes only a fifth of the risk; the remaining 16,000 dollars is idiosyncratic and can only be reduced by selling the stock itself, a closer hedge (a sector ETF or a highly correlated peer), or skewing quotes to work the position out.

### Example 2: when to cross to hedge

You need to sell 10,000 shares of a one-cent-wide 40 dollar stock with per-second volatility 0.00392 dollars.
Aggressive: pay the half-spread 0.005 plus a 0.003 taker fee, 80 dollars.
Passive: earn the 0.005 half-spread plus a 0.002 rebate but lose 0.004 of adverse selection on the passive fill, a net 30 dollars.
The swing between the two is 110 dollars.
With $\gamma = 0.001$ per dollar the risk cost per second of waiting is $\frac12 \times 0.001 \times 10{,}000^2 \times 0.00392^2 \approx 0.77$ dollars.
Break-even waiting time is $110 / 0.77 \approx 143$ seconds.
If you expect a passive fill well within about two minutes, work the order passively; if the queue is long, your signal says the price is about to fall, or the position is ten times larger (risk cost grows 100 times), cross.

### Example 3: delta and gamma of a short call position

You sold 100 calls, each on 100 shares, with delta 0.40 and gamma 0.05 per dollar.
Position delta is $-100 \times 100 \times 0.40 = -4{,}000$ shares, so buy 4,000 shares to hedge.
Position gamma is $-100 \times 100 \times 0.05 = -500$ shares per dollar.
If the stock rises 2 dollars, delta becomes about $-4{,}000 - 1{,}000 = -5{,}000$ and you must buy 1,000 more shares, after the price has risen.
Short gamma means your hedging buys high and sells low; the option premium (theta) is what pays for that, and a vega and gamma limit caps how much of it you run.

### Example 4: a position limit from a VaR budget

A desk allows a one-day 99% VaR of 50,000 dollars in a 50 dollar stock with 2% daily volatility.
One-day standard deviation per share is 1 dollar, and $z_{0.99} \approx 2.326$.
Maximum position: $50{,}000 / (2.326 \times 1) \approx 21{,}500$ shares; set the hard limit at 21,000 and a soft limit (where skew intensifies) around 15,000.

### Example 5: calibrating a daily stop

A strategy's daily P&L has mean 20,000 dollars and standard deviation 15,000 dollars.
A stop at $-40{,}000$ is 4 standard deviations below the mean; under a normal model that happens with probability about $3.2 \times 10^{-5}$, once in roughly 125 years of 252 trading days.
A stop at $-25{,}000$ is 3 standard deviations below: probability about 0.135%, roughly once every 740 trading days.
Real P&L has fat tails, so expect breaches more often than the normal model says; but if the $-40{,}000$ stop fires twice in a quarter, assume the strategy or its environment has changed, not bad luck.

## Pitfalls

- Hedging a single stock with index futures and believing the risk is gone; at $\rho = 0.6$ 80% of the volatility remains.
- Estimating hedge ratios on tick data, where asynchronous prices bias correlations toward zero.
- Rebalancing continuously; transaction costs dominate, and bands are cheaper for the same risk.
- Hedging every option fill in the underlying and ignoring gamma and vega accumulation.
- Kill switches inside the strategy process, or switches that fail open when the risk service is unreachable.
- Limits that block risk-reducing orders as well as risk-increasing ones.
- Automatically restarting after a kill switch without a human understanding why it fired.
- Setting loss limits from a normal model and treating fat-tailed breaches as impossible.

## Interview questions

> [!question]- mm-hedge-min-variance-ratio | What is the minimum-variance hedge ratio and the residual volatility?
> $h^* = \rho\,\sigma_A/\sigma_H$, the regression beta, with residual volatility $\sigma_A\sqrt{1 - \rho^2}$.
> It minimises $\sigma_A^2 - 2h\rho\sigma_A\sigma_H + h^2\sigma_H^2$.

> [!question]- mm-hedge-rho-06-reduction | A hedge has correlation 0.6 with your position. What fraction of volatility does the best hedge remove?
> 20%.
> Residual volatility is $\sqrt{1 - 0.36} = 0.8$ of the original.

> [!question]- mm-hedge-futures-example | Long 1 million dollars of a 2% daily vol stock, futures vol 1%, correlation 0.6. Hedge and residual risk?
> Short 1.2 million dollars of futures; residual daily sd 16,000 dollars versus 20,000 unhedged.
> $h^* = 0.6 \times 2/1 = 1.2$ and $2\% \times 0.8 = 1.6\%$.

> [!question]- mm-hedge-passive-vs-aggressive | How do you decide whether to cross the spread to hedge?
> Cross when the risk cost of waiting for a passive fill exceeds the cost difference between crossing and posting.
> The risk cost grows like $\frac12\gamma n^2\sigma^2 T$, so large positions, high volatility, long queues or adverse signals favour crossing.

> [!question]- mm-hedge-bands | Why do market makers hedge with bands rather than continuously?
> Continuous rebalancing pays transaction costs on every small move; a no-trade band trades risk for cost efficiently.
> For option hedging with proportional costs the optimal band scales with the cube root of the cost (Whalley and Wilmott).

> [!question]- mm-hedge-short-gamma-rehedge | Short 100 calls on 100 shares each, gamma 0.05. The stock rises 2 dollars. What hedge trade?
> Buy about 1,000 more shares.
> Position gamma is $-500$ shares per dollar, so delta falls by 1,000; short gamma forces buying after rises and selling after falls.

> [!question]- mm-hedge-var-position-limit | VaR budget 50,000 dollars at 99% one-day, 50 dollar stock with 2% daily vol. Position limit?
> About 21,500 shares.
> $50{,}000 / (2.326 \times 1)$, since daily sd per share is 1 dollar.

> [!question]- mm-hedge-limit-tiers | Describe a tiered limit structure for a market maker.
> Soft limits change quoting (more skew, less size, wider), hard limits block risk-increasing orders but allow reducing ones, and stop limits cancel everything and need a human restart.
> Apply them to position, Greeks, losses and order-level checks.

> [!question]- mm-hedge-kill-switch-triggers | List kill-switch triggers for an automated market maker.
> Rolling or daily loss breach, position or Greek breach, abnormal fill or order rate, stale or crossed market data, session loss or unacknowledged orders, high reject rate, and internal position disagreeing with the drop copy.

> [!question]- mm-hedge-kill-switch-design | What design properties must a kill switch have?
> It runs outside the strategy process, fails closed, uses exchange mass-cancel or cancel-on-disconnect, is tested regularly, and requires deliberate human reset.
> A switch the strategy can disable or that fails open protects nothing.

> [!question]- mm-hedge-netting-first | Why net inside the book before hedging externally?
> Internal offsets are free, while every external hedge pays spread, fees and impact and adds basis risk.
> Hedge the net residual exposure, not each fill.

> [!question]- mm-hedge-stop-calibration | Daily P&L has mean 20,000 and sd 15,000. How often does a -40,000 stop fire under normality?
> About once in 125 years (probability about $3.2 \times 10^{-5}$ per day).
> It is 4 sd below the mean; fat tails make it more frequent, but repeated breaches signal a regime change.

## In this repo and SDE-Interview-Prep

- Position-limit tiers in the systems companion: [Quantitative Models and Strategies](Quant-Dev-MM-Guide/03_Quantitative_Models_and_Strategies.md), section 2.3.
- Engineering of pre-trade checks: [Risk Checks and Order Management](../12-Quant-Development/13-Risk-Checks-and-Order-Management.md).

## Further reading

- Agustin Lebron, *The Laws of Trading* (2019).
- Euan Sinclair, *Volatility Trading*, 2nd edition (2013), chapters on hedging and risk management.
- John Hull, *Options, Futures, and Other Derivatives*, chapter on hedging strategies using futures.
- Whalley and Wilmott (1997), An asymptotic analysis of an optimal hedging model for option pricing with transaction costs, *Mathematical Finance* 7(3).
- SEC Rule 15c3-5, Risk management controls for brokers or dealers with market access.
- SEC (2013), In the Matter of Knight Capital Americas LLC, Release No. 34-70694.
