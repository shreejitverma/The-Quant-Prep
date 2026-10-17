---
type: concept
title: "Inventory Risk, Avellaneda-Stoikov, and Skew Optimization"
track: [quant-trader, quant-research]
tier: core
status: solid
est_hours: 1.5
tags: [inventory-risk, avellaneda-stoikov, reservation-price, quote-shading, hedging, optimal-control]
prereqs: []
---

# Inventory Risk, Avellaneda-Stoikov, and Skew Optimization

A market maker cannot operate as a purely passive statistical machine that captures spreads without absorbing inventory.
Whenever liquidity demand is one-sided, a market maker accumulates a non-zero inventory position.
Holding inventory exposes the desk to uncompensated directional price volatility.
The foundational framework for solving this multi-objective problem - balancing spread capture against inventory risk - was established by Ho and Stoll (1981) and formulated in closed form by Avellaneda and Stoikov (2008).

---

## TL;DR

A market maker holding non-zero inventory must shade quotes away from the mid-price to induce rebalancing order flow.
The Avellaneda-Stoikov reservation price (indifference price) subtracts a penalty proportional to risk aversion $\gamma$, variance $\sigma^2$, inventory $q$, and remaining time horizon $T - t$:
$$r(s, q, t) = s - q \gamma \sigma^2 (T - t)$$
When holding long inventory ($q > 0$), the reservation price drops below mid, lowering both the bid (deterring incoming sellers) and ask (attracting incoming buyers).
Residual risk that cannot be unloaded passively within the inventory half-life must be hedged actively using correlated liquid proxies.

---

## Learning objectives

- Derive the Avellaneda-Stoikov (2008) reservation price and optimal bid-ask quotes.
- Formulate the inventory decay dynamics and calculate the inventory half-life under mean-reverting fills.
- Implement optimal quote skewing as a function of inventory levels, terminal horizons, and volatility regimes.
- Design cross-asset proxy hedging algorithms to manage residual portfolio delta.
- Calibrate risk aversion $\gamma$ and order arrival intensity $\kappa$ to prevent inventory runaway.

---

## Core concepts

### 1. The Market Maker's Utility Optimization Problem

Consider a risk-averse market maker operating on a finite trading horizon $t \in [0, T]$ in a single asset with mid-price $S_t$ following an arithmetic Brownian motion:

$$dS_t = \sigma \, dW_t$$

The desk holds cash $X_t$ and inventory $q_t$.
At terminal horizon $T$, the desk liquidates any residual inventory at the terminal price $S_T$.
The market maker possesses constant absolute risk aversion (CARA) exponential utility over terminal wealth:

$$U(W_T) = -\exp\left(-\gamma (X_T + q_T S_T)\right)$$

Where $\gamma > 0$ is the absolute risk aversion parameter.

### 2. The Avellaneda-Stoikov Closed-Form Solution (2008)

The reservation price $r(s, q, t)$ is the subjective price at which the market maker is completely indifferent between holding inventory $q$ and holding $q - 1$ shares:

$$r(s, q, t) = s - q \gamma \sigma^2 (T - t)$$

Where:
- $s$ is the prevailing asset mid-price.
- $q$ is the current inventory in shares or contracts.
- $\gamma$ is the desk's risk aversion coefficient.
- $\sigma^2$ is the annualized or session variance of the asset's price returns.
- $(T - t)$ is the remaining time until the mandatory inventory liquidation horizon.

#### Optimal Quoting Spreads
Order execution probabilities follow an exponential intensity model governed by market liquidity parameter $\kappa$:

$$\lambda^a(\delta^a) = A \exp(-\kappa \delta^a), \quad \lambda^b(\delta^b) = A \exp(-\kappa \delta^b)$$

Where $\delta^a = P_a - s$ is the ask spread from mid, and $\delta^b = s - P_b$ is the bid spread from mid.
Avellaneda and Stoikov proved that the optimal total quoted spread $s^*(q, t) = \delta^a + \delta^b$ decomposes into:

$$s^*(q, t) = \gamma \sigma^2 (T - t) + \frac{2}{\gamma} \ln\left(1 + \frac{\gamma}{\kappa}\right)$$

The optimal individual quote distances relative to mid are:

$$\delta^a = (r(s, q, t) - s) + \frac{1}{2} s^*(q, t)$$
$$\delta^b = (s - r(s, q, t)) + \frac{1}{2} s^*(q, t)$$

Equivalently, the quotes are placed symmetrically around the subjective reservation price $r(s, q, t)$ rather than the objective mid-price $s$:

$$P_a^* = r(s, q, t) + \frac{1}{2} s^*(q, t)$$
$$P_b^* = r(s, q, t) - \frac{1}{2} s^*(q, t)$$

### 3. Economic Behavior Under Asymmetric Inventory

The operational mechanics of Avellaneda-Stoikov quote shading behave as follows:

- **Flat Inventory ($q = 0$)**:
  The reservation price equals the mid-price ($r = s$).
  Quotes are placed symmetrically around mid: $P_a = s + \frac{1}{2} s^*$, $P_b = s - \frac{1}{2} s^*$.
- **Long Inventory ($q > 0$)**:
  The reservation price shifts downward ($r < s$).
  Both quotes drop:
  - $P_b$ moves further away from mid, drastically reducing the probability of receiving another buy fill.
  - $P_a$ moves closer to mid (or inside mid), making the desk's ask the most competitive quote in the market and accelerating an inventory-reducing sale.
- **Short Inventory ($q < 0$)**:
  The reservation price shifts upward ($r > s$).
  Both quotes rise:
  - $P_a$ moves higher away from mid, discouraging buyers.
  - $P_b$ moves closer to mid, attracting sellers to relieve the short position.

### 4. Inventory Mean-Reversion and Half-Life

Under optimal quote shading, the arrival rate of rebalancing trades exceeds the arrival rate of inventory-accumulating trades.
The expected change in inventory follows an Ornstein-Uhlenbeck drift:

$$\mathbb{E}[dq_t \mid q_t] = -\kappa_{\text{inv}} q_t \, dt$$

Where $\kappa_{\text{inv}} \approx A \kappa \exp(-\kappa s^* / 2) \cdot \gamma \sigma^2 (T - t)$ represents the inventory mean-reversion speed.
The inventory half-life $t_{1/2}$ is the expected time required for the desk to unwind 50% of an accumulated inventory shock passively:

$$t_{1/2} = \frac{\ln(2)}{\kappa_{\text{inv}}}$$

If $t_{1/2}$ exceeds the desk's maximum holding tolerance (e.g. 5 minutes for an intraday HFT desk), passive quote shading is insufficient, and active proxy hedging must be initiated.

### 5. Cross-Asset Proxy Hedging

When inventory exceeds risk limits $q_{\text{max}}$, the desk executes an aggressive market order in a highly correlated hedging instrument $H$ (such as an index future):

$$N_H = -\beta \cdot q \cdot \left(\frac{S_t}{S_{H,t}}\right)$$

Where $\beta = \frac{\text{Cov}(\Delta S, \Delta S_H)}{\text{Var}(\Delta S_H)}$ is the rolling statistical beta between the primary asset and the hedge instrument.
Active proxy hedging completely neutralizes systemic market delta, converting directional inventory risk into residual basis risk:

$$\sigma_{\text{residual}}^2 = \sigma_S^2 (1 - \rho^2)$$

Where $\rho$ is the correlation between the asset and the proxy.
If $\rho = 0.95$, residual variance drops by $1 - 0.95^2 = 9.75\%$, eliminating over $90\%$ of directional variance.

---

## Worked examples

### Example 1: Avellaneda-Stoikov Quoting with Long vs Short Inventory

A market maker operates on a stock with:
- Current Mid-price: $S_t = \$100.00$.
- Risk aversion: $\gamma = 0.1$.
- Volatility: $\sigma = \$0.50$ per day ($0.50^2 = 0.25$).
- Remaining horizon: $T - t = 1.0$ day.
- Market liquidity parameter: $\kappa = 1.5$.
- Asymptotic spread component: $\frac{2}{\gamma} \ln(1 + \frac{\gamma}{\kappa}) = \frac{2}{0.1} \ln(1 + \frac{0.1}{1.5}) = 20 \times \ln(1.0667) = 20 \times 0.06454 = \$1.2908$.

1. **Calculate the Total Optimal Spread**:
   $$s^*(t) = \gamma \sigma^2 (T - t) + \frac{2}{\gamma} \ln\left(1 + \frac{\gamma}{\kappa}\right) = (0.1 \times 0.25 \times 1.0) + \$1.2908 = \$0.0250 + \$1.2908 = \$1.3158$$
   The half-spread is:
   $$\frac{1}{2} s^* = \frac{\$1.3158}{2} = \$0.6579$$

2. **Scenario A: Neutral Inventory ($q = 0$)**:
   - Reservation price: $r(100, 0, 1) = \$100.00 - 0 = \$100.00$.
   - Optimal Bid: $P_b^* = \$100.00 - \$0.6579 = \$99.3421$.
   - Optimal Ask: $P_a^* = \$100.00 + \$0.6579 = \$100.6579$.
   - Quoted spread is centered exactly at the mid-price.

3. **Scenario B: Long Inventory ($q = +10\text{ units}$)**:
   - Reservation price:
     $$r(100, 10, 1) = \$100.00 - (10 \times 0.1 \times 0.25 \times 1.0) = \$100.00 - \$0.2500 = \$99.7500$$
   - Optimal Bid: $P_b^* = \$99.7500 - \$0.6579 = \$99.0921$.
   - Optimal Ask: $P_a^* = \$99.7500 + \$0.6579 = \$100.4079$.
   - **Result**: Both quotes drop by 25 cents. The ask is now significantly more attractive to market buyers, while the bid is insulated from further selling.

4. **Scenario C: Short Inventory ($q = -10\text{ units}$)**:
   - Reservation price:
     $$r(100, -10, 1) = \$100.00 - (-10 \times 0.1 \times 0.25 \times 1.0) = \$100.00 + \$0.2500 = \$100.2500$$
   - Optimal Bid: $P_b^* = \$100.2500 - \$0.6579 = \$99.5921$.
   - Optimal Ask: $P_a^* = \$100.2500 + \$0.6579 = \$100.9079$.
   - **Result**: Both quotes rise by 25 cents. The bid is now competitive to attract sellers, while the ask is shaded upward.

### Example 2: Proxy Hedging Residual Delta

A market maker is long 50,000 shares of a tech stock priced at $S_1 = \$200.00$ ($GMV = \$10,000,000$).
The desk risk manager limits unhedged exposure to $\$2,000,000$.
The desk uses the E-mini Nasdaq 100 futures contract ($NQ$) priced at $\$18,000$ (multiplier $\$20$, contract value $\$360,000$) with estimated stock beta $\beta = 1.35$.
Correlation $\rho = 0.90$.

1. **Calculate the Position to be Hedged**:
   $$\text{Excess Value} = \$10,000,000 - \$2,000,000 = \$8,000,000$$
2. **Calculate the Required Futures Contracts**:
   $$N_{NQ} = -\frac{\beta \times \text{Excess Value}}{\text{Contract Value}} = -\frac{1.35 \times \$8,000,000}{\$360,000} = -\frac{\$10,800,000}{\$360,000} = -30.0\text{ contracts}$$
3. **Desk Action**:
   The desk sells 30 NQ futures contracts short.
   The directional delta is neutralized, reducing portfolio variance by $1 - 0.90^2 = 81\%$.

---

## Pitfalls

- **Setting Risk Aversion $\gamma$ Too Low**:
  If $\gamma$ is under-calibrated, the reservation price barely moves as inventory accumulates.
  In a strong trending market, the desk will continuously buy all the way down, suffering devastating drawdowns (inventory runaway).
- **Quote Crossing Under Extreme Inventory**:
  If $\gamma$ or inventory $q$ is extremely large, the calculated bid $P_b^*$ can exceed the market best offer, resulting in an immediate unintentional crossed order.
  Production quoting engines must enforce hard boundary clamps: $P_b^* \le P_a^{\text{NBBO}} - \text{tick}$.
- **Assuming Static Volatility**:
  Volatility $\sigma$ typically spikes precisely when inventory accumulates during a one-sided market selloff.
  Failing to scale $\sigma^2$ dynamically in real time leaves the reservation price under-penalized during panics.
- **Basis Breakdown in Proxy Hedging**:
  Hedging single-stock inventory with broad index futures leaves the desk exposed to idiosyncratic earnings gap risk and borrow recall costs.

---

## Interview questions

> [!question] mkt-pqt-097 | What is the Avellaneda-Stoikov (2008) reservation price equation?
> r(s, q, t) = s - q * gamma * sigma^2 * (T - t).
> It represents the indifference price at which a market maker is neutral to adding or subtracting a unit of inventory.

> [!question] mkt-pqt-098 | What happens to the reservation price when a market maker accumulates a long inventory position?
> The reservation price falls strictly below the prevailing market mid-price: r < s.
> This downward shift causes the desk to shade both its bid and ask lower, discouraging sellers and attracting buyers.

> [!question] mkt-pqt-099 | In the Avellaneda-Stoikov model, how do optimal quotes relate to the reservation price?
> Optimal quotes are placed symmetrically around the reservation price r rather than the market mid s: P_a = r + s*/2 and P_b = r - s*/2.
> The quoted spread width s* is determined by risk aversion, price variance, and market liquidity depth.

> [!question] mkt-pqt-100 | What role does the parameter gamma play in the Avellaneda-Stoikov framework?
> Gamma represents the market maker's constant absolute risk aversion (CARA) parameter.
> Higher gamma increases the inventory penalty, forcing faster quote skewing and wider defensive spreads.

> [!question] mkt-pqt-101 | What role does kappa play in the Avellaneda-Stoikov model?
> Kappa measures the price sensitivity of order arrivals: lambda(delta) = A * exp(-kappa * delta).
> Higher kappa signifies a thick, highly competitive market where order fill probability drops off sharply as quotes move away from mid.

> [!question] mkt-pqt-102 | What is the terminal horizon T in intraday market making models?
> T represents the end of the trading session or mandatory inventory liquidation time.
> As t approaches T, (T - t) approaches zero, causing the inventory penalty to vanish as the desk faces hard liquidation.

> [!question] mkt-pqt-103 | What is inventory half-life and why is it monitored by risk managers?
> Inventory half-life is the expected time required for an accumulated inventory position to decay by 50% through passive quoting.
> If half-life exceeds risk limits, the desk cannot rely on passive rebalancing and must actively cross the spread to hedge.

> [!question] mkt-pqt-104 | How does an Ornstein-Uhlenbeck process model inventory mean reversion?
> dq_t = -kappa_inv * q_t * dt + sigma_q * dW_t.
> The negative drift ensures that positive inventory creates downward pressure and negative inventory creates upward pressure toward zero.

> [!question] mkt-pqt-105 | What is cross-asset proxy hedging?
> Offsetting directional inventory exposure in an illiquid primary asset by taking an offsetting position in a highly correlated liquid instrument.
> For example, hedging single-stock long inventory by shorting an index future or sector ETF.

> [!question] mkt-pqt-106 | State the beta-adjusted proxy hedge ratio formula.
> Hedge Qty = -beta * (Primary Qty * Price_primary) / Price_hedge.
> It equates the dollar systematic delta of the hedge instrument to the systematic risk of the primary position.

> [!question] mkt-pqt-107 | What is basis risk in a proxy-hedged market-making book?
> The risk that the spread between the primary asset and the proxy hedge widens due to idiosyncratic shocks.
> While market risk is eliminated, residual basis variance remains: Var(residual) = sigma_primary^2 * (1 - rho^2).

> [!question] mkt-pqt-108 | Why does correlation breakdown during market crashes impair proxy hedging?
> During liquidity crises, idiosyncratic liquidations cause historical correlations rho to decouple toward zero or flip sign.
> The market maker's long inventory drops while the short hedge rises, compounding losses across both legs.

> [!question] mkt-pqt-109 | What is inventory runaway and what causes it?
> The continuous accumulation of inventory in one direction as an asset trends persistently through quoted price levels.
> It occurs when quote shading is insufficiently aggressive relative to the strength of informed market order flow.

> [!question] mkt-pqt-110 | How do hard inventory boundaries (position limits) modify the Avellaneda-Stoikov problem?
> When inventory reaches the maximum limit +Q_max, the market maker completely withdraws its bid quote (setting P_b = -infinity).
> The desk only quotes an ask, eliminating the risk of accumulating further inventory.

> [!question] mkt-pqt-111 | Explain the concept of asymmetric spread quoting.
> Setting the bid distance delta_b and ask distance delta_a unequally relative to mid: delta_b != delta_a.
> Asymmetry is driven directly by inventory skew: delta_a - delta_b = 2 * (r - s) = -2 * q * gamma * sigma^2 * (T - t).

> [!question] mkt-pqt-112 | What is an internalizer's inventory netting benefit across multiple market makers?
> An internalizer matching flow across multiple internal prop desks nets offsetting inventories before routing residual risk to the street.
> Netting dramatically reduces external exchange execution fees and gross collateral requirements.

> [!question] mkt-pqt-113 | Why does the Avellaneda-Stoikov spread widen when volatility sigma increases?
> Spread s* contains the term gamma * sigma^2 * (T - t).
> Higher volatility expands the variance of terminal inventory value, forcing the desk to demand a wider compensation spread.

> [!question] mkt-pqt-114 | What is the Guéant-Tapia-Manziadi (2012) extension to Avellaneda-Stoikov?
> It solves the optimal quoting problem under general utility functions and multi-asset books without requiring CARA approximations.
> It yields exact Hamilton-Jacobi-Bellman (HJB) viscosity solutions for execution and market making.

> [!question] mkt-pqt-115 | How does overnight inventory financing impact market-making economics?
> Carrying long inventory requires financing at SOFR plus a prime broker spread; carrying short inventory incurs stock borrow fees.
> Financing drag creates a daily hurdle rate that penalizes slow-moving or low-turnover inventory.

> [!question] mkt-pqt-116 | What is the difference between active inventory shedding and passive quote shading?
> Passive shading adjusts limit quotes to entice incoming retail orders to trade at favorable prices over time.
> Active shedding aggressively crosses the spread with market orders, paying taker fees to eliminate risk instantly.

> [!question] mkt-pqt-117 | When should a market maker transition from passive shading to active aggressive liquidation?
> When inventory breaches critical stop limits, when inventory half-life exceeds time to close, or when market volatility spikes abruptly.
> Active liquidation pays guaranteed spread costs to prevent catastrophic ruin from overnight gap risk.

> [!question] mkt-pqt-118 | What is the impact of dividend ex-dates on equity market maker inventory?
> Holding short equity inventory overnight on an ex-dividend date obligates the desk to pay the cash dividend to the share lender.
> Market makers aggressively bid to close short inventory before the ex-date to avoid dividend liability.

> [!question] mkt-pqt-119 | In options market making, how does delta inventory relate to underlying stock quoting?
> An options desk with net positive delta inventory shades its underlying stock quotes lower to sell stock and restore delta neutrality.
> Alternatively, the desk shades its options quotes by bidding higher for puts and asking lower for calls.

> [!question] mkt-pqt-120 | What is gamma scalping in the context of options inventory management?
> Dynamically buying underlying stock when it falls and selling when it rises to maintain delta neutrality on a long gamma options position.
> Realized gamma scalping gains offset the continuous theta time decay of the options inventory.

> [!question] mkt-pqt-121 | Why is inventory risk non-linear in total position size?
> The variance of inventory holding cost scales with q^2: Cost ~ 0.5 * gamma * q^2 * sigma^2.
> Doubling inventory quadruples the total dollar risk penalty, requiring exponentially aggressive quote shading.

> [!question] mkt-pqt-122 | What is the effect of order arrival intensity A on quoting spreads?
> Higher baseline arrival intensity A means more frequent trades, allowing the market maker to quote tighter spreads.
> Frequent trading increases turnover, enabling rapid inventory turnover and lower required margin per trade.

> [!question] mkt-pqt-123 | How does tick size discretisation constrain the theoretical Avellaneda-Stoikov quotes?
> Theoretical continuous quotes P_a* and P_b* must be rounded to discrete exchange tick grids (e.g. $0.01 increments).
> Rounding errors can prevent subtle quote shading on low-priced stocks, forcing binary queue position choices.

> [!question] mkt-pqt-124 | What is queue priority jumping via quote improvement?
> Bidding one tick above the existing NBBO bid to establish a new price priority tier and jump ahead of a long queue.
> The market maker sacrifices one tick of spread to guarantee immediate execution on incoming seller flow.

> [!question] mkt-pqt-125 | How does high book depth at the NBBO influence optimal reservation price skew?
> In deep books, incoming orders rarely sweep past the best quote, making it harder to attract rebalancing flow by shading.
> The market maker must either join the front of the queue early or shade quotes across multiple ticks into Level 2 depth.

> [!question] mkt-pqt-126 | What is liquidity black hole risk in inventory management?
> A catastrophic feedback loop where falling prices force multiple market makers to shed long inventory simultaneously.
> Mutual aggressive selling exhausts all available bids, causing prices to collapse vertically without liquidity.

> [!question] mkt-pqt-127 | Explain the difference between portfolio-level VAR and asset-level inventory limits.
> Asset-level limits cap the maximum position in each individual stock to protect against idiosyncratic firm-specific news.
> Portfolio VAR caps aggregate systematic exposure across all assets, accounting for cross-asset correlations.

> [!question] mkt-pqt-128 | Why do quantitative prop firms mandate that traders flatten all intraday inventory before market close?
> Overnight trading pauses eliminate liquidity and prevent dynamic hedging while exposing capital to unhedgeable earnings gaps and macro shocks.
> Complete flattening resets inventory to zero, ensuring that daily PnL reflects pure intraday statistical edge.

---

## Further reading

- Ho, T., & Stoll, H. R. (1981). *Optimal dealer pricing under transactions and return uncertainty*. Journal of Financial Economics, 9(1), 47-73.
- Avellaneda, M., & Stoikov, S. (2008). *High-frequency trading in a limit order book*. Quantitative Finance, 8(3), 217-224.
- Guéant, O., Tapia, C. A., & Manziadi, Z. (2012). *Dealing with the inventory risk: a solution to the market making problem*. Mathematics and Financial Economics, 6(4), 259-277.
- Cartea, Á., Jaimungal, S., & Penalva, J. (2015). *Algorithmic and High-Frequency Trading*. Cambridge University Press.
