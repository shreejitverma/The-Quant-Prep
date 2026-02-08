# Quantitative Models & Strategies in Market Making

**Focus:** Mathematical frameworks for quoting, inventory management, and alpha signals.
**Prerequisites:** Probability theory, stochastic calculus basics, convex optimization.

---

## 1. The Market Maker's Problem

The fundamental goal is to maximize terminal wealth utility while managing inventory risk. This is often modeled as a stochastic optimal control problem.

### 1.1 The Avellaneda-Stoikov Model (2008)
This is the seminal paper for high-frequency market making.

**Core Assumptions:**
*   **Mid-price ($S_t$)** follows a geometric Brownian motion or arithmetic Brownian motion:
    $$dS_t = \sigma dW_t$$
*   **Arrival Rates ($\lambda$)**: The probability of a limit order being filled follows a Poisson process with intensity decaying exponentially with distance ($\delta$) from the mid-price:
    $$\lambda(\delta) = A e^{-k\delta}$$
    Where:
    *   $\delta$: Spread (Distance from mid-price)
    *   $A$: Base arrival intensity
    *   $k$: Order book liquidity parameter (higher $k$ = thinner book)

**The Objective Function:**
Maximize expected exponential utility of terminal wealth:
$$u(w) = -e^{-\gamma w}$$
Where $\gamma$ is the risk aversion parameter.

**The Solution (Optimal Quotes):**
The optimal bid ($r_b^*$) and ask ($r_a^*$) prices are:

$$r_a^* = S_t + \frac{1}{2}\delta^* + (2q - 1)\frac{\gamma \sigma^2 (T-t)}{2}$$
$$r_b^* = S_t - \frac{1}{2}\delta^* + (2q + 1)\frac{\gamma \sigma^2 (T-t)}{2}$$

**Key Interpretations:**
1.  **Reservation Price ($r^*$)**: The price at which the MM is indifferent between buying and selling.
    $$r^*(S, q, t) = S_t - q \gamma \sigma^2 (T-t)$$
    *   If inventory $q > 0$ (Long): Reservation price shifts *down*. You are eager to sell, reluctant to buy.
    *   If inventory $q < 0$ (Short): Reservation price shifts *up*.
    *   **Term:** $q \gamma \sigma^2 (T-t)$ is the inventory risk premium.

2.  **Optimal Spread ($\delta^*$)**:
    $$\delta^* = \frac{2}{\gamma} \ln(1 + \frac{\gamma}{k})$$
    *   The spread is independent of inventory in the standard model.
    *   It depends on risk aversion ($\gamma$) and market liquidity ($k$).

---

## 2. Inventory Management Strategies

Managing $q$ (inventory) is the single most critical risk task.

### 2.1 Skewing (Asymmetric Quoting)
As derived above, quotes should be centered around the Reservation Price, not the Mid-Price.

**Logic:**
*   **Current Inventory:** +1000 shares (Long Limit Reached).
*   **Action:**
    *   **Ask:** Aggressive. $S_t$ or even $S_t - \epsilon$. We *need* to sell.
    *   **Bid:** Passive. $S_t - 5\text{ticks}$. We do *not* want to buy more.
*   **Effect:** Increases probability of Ask fill, decreases probability of Bid fill.

### 2.2 Damping Factor
In practice, linear inventory penalties can be too volatile. Firms often use a sigmoid or cubic dampener:
$$\text{Skew} = \alpha \cdot \tanh(\beta \cdot \frac{q}{Q_{max}})$$

### 2.3 Position Limits & Liquidation
*   **Soft Limit:** Begin skewing aggressively.
*   **Hard Limit:** Block new opening orders.
*   **Liquidation Limit:** Send Immediate-or-Cancel (IOC) market orders to dump inventory if it exceeds critical thresholds (Stop Loss).

---

## 3. Alpha Signals (Short-Term Predictors)

Market making is not just passive. You need "Micro-Alpha" to avoid adverse selection (Toxic Flow).

### 3.1 Order Book Imbalance (OBI)
The ratio of volume at the Best Bid ($V_b$) vs. Best Ask ($V_a$).

$$OBI = \frac{V_b - V_a}{V_b + V_a}$$

*   **Logic:** If $OBI \to +1$ (Huge Bid, Tiny Ask), price is likely to tick up.
*   **Action:** Skew quotes upward. Lean on the bid.

### 3.2 Order Flow Toxicity (VPIN)
Volume-Synchronized Probability of Informed Trading.
*   Measures order flow imbalance relative to volume.
*   High VPIN $\implies$ High probability of informed trader presence.
*   **Action:** Widen spreads.

### 3.3 Cross-Asset Correlations (Lead-Lag)
*   **Scenario:** SPY (S&P 500 ETF) is the most liquid instrument.
*   **Signal:** SPY ticks up.
*   **Effect:** Less liquid constituents (e.g., AAPL, MSFT) will likely tick up 5-50ms later.
*   **Action:** Immediately cancel/re-price AAPL asks upwards before latency arbitrageurs hit them.

---

## 4. Backtesting Market Making Strategies

Backtesting limit order strategies is notoriously difficult due to "fill simulation."

### 4.1 Assumptions & Pitfalls
1.  **Queue Position:** You cannot assume you are at the front of the queue.
    *   *Conservative:* Assume you are at the back (Last in, First Out - LIFO logic for fills).
    *   *Realistic:* Estimate queue depletion.
2.  **Market Impact:** Your orders affect the market.
    *   If you post a huge bid, others might front-run you ("Pennying").
3.  **Latency:** You see a price $S_t$, but by the time your order reaches the exchange, the price is $S_{t+\Delta}$.

### 4.2 Simulator Design
*   **Input:** Tick-by-tick data (MBO preferred).
*   **State:** Reconstructed Order Book.
*   **Matching Engine:** Replicates exchange matching logic (Price-Time Priority).
*   **Latency Model:** Adds random jitter + constant delay to all order actions.

---

## 5. Practical Exercise: Python Prototype

```python
import numpy as np

def calculate_optimal_quotes(mid_price, inventory, volatility, risk_aversion, time_horizon):
    """
    Avellaneda-Stoikov Reservation Price & Spread Calculation
    """
    # 1. Reservation Price
    # r* = s - q * gamma * sigma^2 * (T - t)
    reservation_price = mid_price - (inventory * risk_aversion * (volatility**2) * time_horizon)
    
    # 2. Optimal Half-Spread (Simplified approximation)
    # Assumes k (liquidity parameter) is constant derived from market data
    k = 1.5  # Example value fitted from trade intensity
    spread = (2 / risk_aversion) * np.log(1 + (risk_aversion / k))
    
    half_spread = spread / 2
    
    optimal_bid = reservation_price - half_spread
    optimal_ask = reservation_price + half_spread
    
    return optimal_bid, optimal_ask

# Example
current_price = 100.00
current_inventory = 500  # Long 500 shares
sigma = 2.0  # Daily vol
gamma = 0.1  # Risk aversion
T = 1.0     # End of day (normalized)

bid, ask = calculate_optimal_quotes(current_price, current_inventory, sigma, gamma, T)

print(f"Mid Price: {current_price}")
print(f"Inventory: {current_inventory}")
print(f"Optimal Bid: {bid:.2f}")
print(f"Optimal Ask: {ask:.2f}")
print(f"Skew: {(bid+ask)/2 - current_price:.4f}") 
# Expect negative skew (lower prices) to shed long inventory
```

