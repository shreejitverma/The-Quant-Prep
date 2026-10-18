---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: solid
prereqs: []
est_hours: 4
sources: [Litterman and Scheinkman (1991) - Common Factors Affecting Bond Returns, Nelson and Siegel (1987) - Parsimonious Modeling of Yield Curves, Du Tepper and Verdelhan (2018) - Deviations from Covered Interest Rate Parity, Brunnermeier Nagel and Pedersen (2008) - Carry Trades and Currency Crashes]
---

# Yield Curve Dynamics and Rates Trading

## TL;DR

- The sovereign yield curve is the foundational discount mechanism for global capital markets; its shape reflects market expectations of future short-term interest rates, inflation risk premiums, and term premiums.
- Litterman and Scheinkman (1991) proved via Principal Component Analysis (PCA) that three orthogonal factors explain over 98% of yield curve variations: Level (parallel shift, ~85-90%), Slope (steepening/flattening, ~8-12%), and Curvature (hump, ~2-4%).
- Rates traders construct DV01-neutral relative-value trades across the curve, including 2s10s steepeners/flatteners, box spreads, and barbell-bullet butterfly spreads (e.g., 2Y/5Y/10Y).
- Covered Interest Parity (CIP) has persistently failed since the 2008 financial crisis, giving rise to the cross-currency basis spread driven by bank regulatory balance sheet constraints (Supplementary Leverage Ratio) and non-US dollar demand.
- Systematic FX carry trades harvest structural interest rate differentials by borrowing low-yielding funding currencies (such as JPY or CHF) to purchase high-yielding target currencies, but remain exposed to sudden flight-to-safety liquidation crashes.

## Learning objectives

- Bootstrap zero-coupon spot yield curves and instantaneous forward rate curves from coupon-bearing par instruments.
- Deconstruct yield curve transformations into Level, Slope, and Curvature using Principal Component Analysis.
- Calculate Dollar Value of a Basis Point (DV01) and design duration-neutral curve spread and butterfly positions.
- Quantify deviations from Covered Interest Parity (CIP) and model the economic determinants of cross-currency basis spreads.
- Formulate systematic FX carry trade models with dynamic volatility scaling and crash-risk protection.

## Core concepts

### 1. Yield Curve Geometry and Bootstrapping

The yield curve can be represented in three mathematically distinct forms:

```
+-----------------------------------------------------------------------+
|                    THE THREE YIELD CURVE REPRESENTATIONS              |
+-----------------------------------------------------------------------+
| 1. Par Yield Curve: Coupon rate that prices a newly issued bond at 100|
| 2. Spot (Zero-Coupon) Curve y(t): Yield on pure zero-coupon discount  |
|    bonds P(0, t) = exp(-y(t) * t)                                     |
| 3. Instantaneous Forward Curve f(t): Marginal rate for borrowing over |
|    instantaneous period [t, t+dt]: f(t) = y(t) + t * y'(t)            |
+-----------------------------------------------------------------------+
```

To extract pure zero-coupon discount factors $P(0, T)$ from coupon-paying bonds trading at par, quants deploy sequential bootstrapping:

$$P(0, T) = \frac{1 - c \sum_{i=1}^{n-1} P(0, t_i)}{1 + c}$$

where $c$ is the semi-annual coupon rate of the maturing par bond.
Continuous spot yields $y(T)$ are obtained via:

$$y(T) = -\frac{\ln P(0, T)}{T}$$

The instantaneous forward rate $f(T)$ reflects the slope of the discount function:

$$f(T) = -\frac{\partial \ln P(0, T)}{\partial T} = y(T) + T \frac{\partial y(T)}{\partial T}$$

When the spot yield curve is upward-sloping ($\frac{\partial y}{\partial T} > 0$), forward rates sit strictly above spot rates ($f(T) > y(T)$).

### 2. PCA Decomposition: Level, Slope, and Curvature

In their seminal 1991 paper, Robert Litterman and José Scheinkman conducted Principal Component Analysis on daily Treasury yield changes across maturities from 1 to 30 years:

```
+-----------------------------------------------------------------------+
|                    THE THREE PCA FACTORS OF THE YIELD CURVE           |
+-----------------------------------------------------------------------+
| Factor    | Variance Expl | Geometric Shape  | Economic Driver        |
|-----------+---------------+------------------+------------------------|
| PC1: Level| ~85.0% - 90%  | Flat Shift (+,+) | Inflation / Fed Stance |
| PC2: Slope| ~8.0% - 12%   | Rotation (+, -)  | Growth Cycle / Hikes   |
| PC3: Curve| ~2.0% - 4%    | Hump (+, -, +)   | Term Premium / Liquidity|
+-----------------------------------------------------------------------+
```

```
Factor Loadings across Maturity (Years):
Loadings
   ^
   |  [PC1: Level]  ---------------------------------- (+0.40)
   |
   |  [PC2: Slope]  \
   |                 \
   |                  \
   |  -----------------\-----------------------------> Maturity
   |                    \
   |                     \  (-0.40)
   |
   |  [PC3: Curvature]   /\
   |                    /  \
   |                   /    \
   +------------------/------\------------------------
```

1. **PC1 (Level)**: A parallel shock across all maturities.
   A 50 bps surprise in macroeconomic inflation raises short, intermediate, and long yields uniformly.
2. **PC2 (Slope)**: Short-end yields move in the opposite direction of long-end yields.
   Central bank rate hikes raise short rates while lowering long rates due to expected future growth slowdown (flattening the curve).
3. **PC3 (Curvature)**: Intermediate maturities (3-7 years) move while short and long ends remain anchored, altering the hump of the curve.

### 3. Rates Trading: DV01-Neutral Spreads and Butterflies

The foundational risk metric in fixed income trading is the **Dollar Value of a Basis Point (DV01)**, representing the change in market value for a 1 basis point (0.01%) parallel shift in yield:

$$\text{DV01} = -\frac{\partial P}{\partial y} \times 0.0001 \approx P \times \text{Modified Duration} \times 0.0001$$

#### The 2s10s Steepener / Flattener Trade
To trade the slope between 2-year and 10-year Treasuries without taking unhedged directional duration risk, the trader equates the DV01 of both legs:

$$\text{DV01}_{\text{Leg 1}} = \text{DV01}_{\text{Leg 2}}$$

$$\text{Notional}_{2Y} \times \text{DV01}_{2Y} = \text{Notional}_{10Y} \times \text{DV01}_{10Y}$$

$$\frac{\text{Notional}_{2Y}}{\text{Notional}_{10Y}} = \frac{\text{DV01}_{10Y}}{\text{DV01}_{2Y}} \approx \frac{8.2}{1.9} \approx 4.32$$

To execute a **Bull Steepener** (expecting the Fed to slash short rates):
- Long $43.2 million 2-year notes.
- Short $10.0 million 10-year bonds.
The net portfolio has zero exposure to parallel level shifts ($\text{DV01}_{\text{net}} = 0$), but generates pure alpha if the 2s10s spread widens.

#### The 2s5s10s Butterfly Spread
Butterfly trades isolate pure curvature (PC3) while hedging both Level (PC1) and Slope (PC2).
A butterfly consists of two "wings" (2Y and 10Y) and a "body" (5Y):
- Long Wing 1 (2Y) + Long Wing 2 (10Y) vs Short Body (5Y).

Weights $w_1, w_2, w_3$ satisfy:
$$\text{DV01}_1 + \text{DV01}_2 = \text{DV01}_{\text{body}}$$
$$\text{Slope Weighting}: \text{DV01}_1 \cdot \Delta y_1 + \text{DV01}_2 \cdot \Delta y_2 = \text{DV01}_{\text{body}} \cdot \Delta y_{\text{body}}$$

```
+-----------------------------------------------------------------------+
|                    YIELD CURVE BUTTERFLY STRUCTURE                    |
+-----------------------------------------------------------------------+
| Wing 1 (2-Year): Long $25M DV01                                       |
| Body (5-Year):   Short $50M DV01  <--- Belly of the Curve             |
| Wing 2 (10-Year): Long $25M DV01                                      |
+-----------------------------------------------------------------------+
```

### 4. Covered Interest Parity (CIP) and The Cross-Currency Basis

Covered Interest Parity states that the forward exchange rate $F$ between domestic currency $d$ and foreign currency $f$ must equate synthetic borrowing costs:

$$\frac{F}{S} = \frac{1 + r_d}{1 + r_f}$$

In continuous compounding:
$$F = S \cdot e^{(r_d - r_f) T}$$

Prior to 2008, CIP held to within transaction costs.
However, since 2008, significant and persistent deviations have existed, measured by the **Cross-Currency Basis Spread ($\Delta$)**:

$$F = S \cdot e^{(r_d - r_f - \Delta) T}$$

```
+-----------------------------------------------------------------------+
|                    WHY COVERED INTEREST PARITY FAILS POST-2008        |
+-----------------------------------------------------------------------+
| 1. Basel III Supplementary Leverage Ratio (SLR):                      |
|    Banks are penalized on total balance sheet size, regardless of risk|
| 2. Non-US Dollar Demand: Global corporates and foreign central banks  |
|    need USD funding to service USD-denominated debt                   |
| 3. Limited Arbitrage Capital: Hedge funds cannot borrow unlimited cash|
|    to close the CIP gap without consuming scarce prime broker balance |
+-----------------------------------------------------------------------+
```

A negative EUR/USD cross-currency basis indicates that non-US institutions are willing to pay a premium to borrow US dollars via FX swaps, offering fixed income quants an arbitrage premium.

### 5. Systematic Foreign Exchange Carry Trades

The Uncovered Interest Parity (UIP) puzzle documents that high-interest-rate currencies do not depreciate to offset their interest rate advantage over medium horizons.
Systematic macro funds exploit this through the **FX Carry Trade**:

$$\text{Strategy}: \text{Long Currencies with } r_i > r_{\text{median}} \quad \text{Financed by Short Currencies with } r_j < r_{\text{median}}$$

```
+-----------------------------------------------------------------------+
|                    THE FX CARRY RETURN DECOMPOSITION                  |
+-----------------------------------------------------------------------+
| Total Carry Return = Interest Rate Differential (Carry)               |
|                    + Spot FX Movement (\Delta S)                      |
|                    - Financing / Repo Spread                          |
+-----------------------------------------------------------------------+
```

#### The Volatility Asymmetry and "Going Up the Stairs, Coming Down the Elevator"
Carry strategies exhibit steady positive returns during periods of low market volatility, but suffer catastrophic, non-linear drawdowns during global liquidity squeezes (Brunnermeier et al. 2008).
When global risk appetite collapses, investors unwind carry trades simultaneously, driving rapid appreciation in funding currencies (e.g., JPY short-covering surges).
Modern systematic managers apply dynamic volatility targeting: scaling position sizes inversely to realized currency basket volatility and liquidating carry exposure when the VIX breaches threshold barriers.

---

## Worked examples

### Example 1: DV01-Neutral 2s10s Flattener Sizing
A fixed income quant expects the Federal Reserve to implement unexpected policy rate hikes, causing a bear flattening of the yield curve.
The trader wants to short 2-year Treasury notes and go long 10-year Treasury notes in a DV01-neutral ratio with a total target risk of $50,000 per basis point.
Market parameters:
- 2-Year Treasury Note: Price = $100.00, Modified Duration = 1.90 years $\implies \text{DV01} = \$1.90$ per $10,000 notional (0.0190% of notional).
- 10-Year Treasury Note: Price = $100.00, Modified Duration = 8.20 years $\implies \text{DV01} = \$8.20$ per $10,000 notional (0.0820% of notional).

To allocate $50,000 of DV01 risk per leg:
$$\text{Notional}_{2Y} = \frac{\$50,000}{0.000190} \approx \$263,157,895 \text{ (Short)}$$
$$\text{Notional}_{10Y} = \frac{\$50,000}{0.000820} \approx \$60,975,610 \text{ (Long)}$$

If the 2-year yield rises by 25 bps while the 10-year yield rises by only 10 bps (a 15 bps flattening):
$$\Delta \text{PnL}_{2Y} = \text{Notional}_{2Y} \times \text{DV01\%} \times \Delta y_{2Y} = \$263.16\text{M} \times 0.000190 \times 25 = +\$1,250,000$$
$$\Delta \text{PnL}_{10Y} = \text{Notional}_{10Y} \times \text{DV01\%} \times (-\Delta y_{10Y}) = \$60.98\text{M} \times 0.000820 \times (-10) = -\$500,000$$
$$\text{Net Trade PnL} = \$1,250,000 - \$500,000 = +\$750,000$$
The trade successfully generated $750,000 of profit by capturing 15 bps of flattening on $50,000 DV01 ($15 \times \$50,000 = \$750,000$), completely immune to the parallel level shift.

---

## Pitfalls

- **Ignoring Negative Convexity in Mortgage-Backed Securities**: MBS duration shortens as rates fall and lengthens as rates rise, breaking linear DV01 hedges during sharp market rallies.
- **Overlooking Unhedged Currency Basis Swaps**: Entering synthetic foreign currency loans without accounting for cross-currency basis fluctuations, triggering unexpected financing cash drains.
- **Sizing Curve Trades by Nominal Notional Instead of DV01**: Holding equal dollar amounts of 2-year and 10-year bonds creates massive unintended directional duration risk dominated by the 10-year leg.
- **Assuming Uncovered Interest Parity Holds in the Short Run**: Relying on economic models to predict currency depreciation rather than recognizing persistent structural carry returns.
- **Neglecting Flight-to-Safety Liquidity Spikes in FX Carry**: Holding unhedged long carry positions during a macro shock, suffering extreme drawdowns as funding currencies rapidly appreciate.

---

## Interview questions

> [!question]- mkt-mac-001 | What is a zero-coupon spot yield?
> The internal rate of return on a pure discount bond that makes a single payment at maturity with no periodic coupons.

> [!question]- mkt-mac-002 | What is a par yield?
> The coupon rate that causes a newly issued bond to trade at exactly its face value (100 par).

> [!question]- mkt-mac-003 | What is an instantaneous forward rate?
> The marginal interest rate agreed upon today for borrowing over an infinitesimal time interval in the future.

> [!question]- mkt-mac-004 | What is bootstrapping in fixed income analytics?
> The recursive procedure used to extract zero-coupon spot rates from a sequence of coupon-bearing par bonds.

> [!question]- mkt-mac-005 | In an upward-sloping yield curve, what is the geometric relationship between forward rates and spot rates?
> Forward rates sit strictly above spot rates: f(T) > y(T).

> [!question]- mkt-mac-006 | What did Litterman and Scheinkman (1991) prove regarding yield curve dynamics?
> That three principal component factors (Level, Slope, and Curvature) account for over 98% of total yield curve variance.

> [!question]- mkt-mac-007 | What proportion of yield curve variance is typically explained by the Level factor (PC1)?
> Approximately 85% to 90% of total variance.

> [!question]- mkt-mac-008 | What is the geometric movement of the yield curve represented by the Slope factor (PC2)?
> A rotation where short-term yields and long-term yields move in opposite directions (steepening or flattening).

> [!question]- mkt-mac-009 | What is the geometric movement of the yield curve represented by the Curvature factor (PC3)?
> A movement in intermediate (belly) yields relative to anchored short and long maturities, altering the hump of the curve.

> [!question]- mkt-mac-010 | What is DV01 (Dollar Value of a Basis Point)?
> The monetary change in the value of a fixed income instrument resulting from a one basis point (0.01%) change in yield.

> [!question]- mkt-mac-011 | What is the mathematical definition of DV01 in terms of Modified Duration?
> DV01 = Price * Modified Duration * 0.0001.

> [!question]- mkt-mac-012 | What defines a DV01-neutral curve trade?
> Sizing position notionals such that the net DV01 of long and short legs equals zero, neutralizing parallel level shifts.

> [!question]- mkt-mac-013 | What is a Bull Steepener in the yield curve?
> Short-term rates fall faster than long-term rates, steepening the curve as central banks rapidly cut rates.

> [!question]- mkt-mac-014 | What is a Bear Steepener in the yield curve?
> Long-term rates rise faster than short-term rates, steepening the curve driven by rising inflation expectations or bond supply.

> [!question]- mkt-mac-015 | What is a Bull Flattener in the yield curve?
> Long-term rates fall faster than short-term rates, flattening the curve as growth expectations cool and disinflation sets in.

> [!question]- mkt-mac-016 | What is a Bear Flattener in the yield curve?
> Short-term rates rise faster than long-term rates, flattening the curve during active central bank monetary tightening campaigns.

> [!question]- mkt-mac-017 | In a 2s10s DV01-neutral steepener, why is the notional size of the 2-year note much larger than the 10-year note?
> Because 2-year notes have much lower duration; higher notional is required to match the dollar risk of the 10-year leg.

> [!question]- mkt-mac-018 | What is a yield curve butterfly trade structure?
> Long two wings (short and long maturities) and short the body (intermediate maturity), or vice versa.

> [!question]- mkt-mac-019 | What yield curve factor does a DV01-neutral, slope-neutral butterfly trade isolate?
> Curvature (PC3).

> [!question]- mkt-mac-020 | What is Covered Interest Parity (CIP)?
> The arbitrage relationship stating that the forward FX rate must equal the spot rate adjusted for the interest rate differential between two currencies.

> [!question]- mkt-mac-021 | What is the mathematical formula for Covered Interest Parity with continuous compounding?
> F = S * exp((r_d - r_f) * T).

> [!question]- mkt-mac-022 | What is the Cross-Currency Basis Spread?
> The empirical premium or discount added to foreign currency rates in the FX swap market, reflecting deviations from pure CIP.

> [!question]- mkt-mac-023 | Why has the cross-currency basis spread persisted since the 2008 financial crisis?
> Post-crisis banking regulations (such as the Supplementary Leverage Ratio) penalize bank balance sheet expansion, restricting arbitrage capital.

> [!question]- mkt-mac-024 | What does a negative cross-currency basis for EUR/USD signify?
> Non-US institutions are paying a premium above normal CIP rates to borrow US dollars through the foreign exchange swap market.

> [!question]- mkt-mac-025 | What is the Uncovered Interest Parity (UIP) condition?
> The economic hypothesis that high-yielding currencies will depreciate by an amount equal to their interest rate differential.

> [!question]- mkt-mac-026 | What is the FX Carry Trade?
> An investment strategy that borrows in low-interest-rate funding currencies and invests in high-interest-rate target currencies.

> [!question]- mkt-mac-027 | Why does the FX Carry Trade succeed over long periods despite UIP theory?
> Because the empirical UIP puzzle shows that high-yielding currencies often fail to depreciate or even appreciate over medium horizons.

> [!question]- mkt-mac-028 | What is the primary structural tail risk of an FX carry strategy?
> Severe crash risk: sudden global market panics trigger rapid unwinding of short funding positions, causing steep liquidation drawdowns.

> [!question]- mkt-mac-029 | What are the classic funding currencies historically used in global carry trades?
> The Japanese Yen (JPY) and Swiss Franc (CHF), due to their multi-decade near-zero or negative interest rate policies.

> [!question]- mkt-mac-030 | How do quantitative carry managers protect against sudden carry crashes?
> By dynamically reducing leverage when market volatility (e.g. VIX, FX implied volatility) spikes.

> [!question]- mkt-mac-031 | What is an FX swap?
> A transaction where two counterparties exchange currencies at the spot rate today and simultaneously agree to reverse the exchange at a forward rate on a future date.

> [!question]- mkt-mac-032 | What is the primary golden rule of rates and macro trading?
> Always isolate the exact factor exposure (Level, Slope, or Curvature) using DV01 weighting before deploying capital.

---

## Further reading

- Brunnermeier, M. K., Nagel, S., & Pedersen, L. H. (2008). *Carry Trades and Currency Crashes*. NBER Macroeconomics Annual, 23(1), 313-347.
- Du, W., Tepper, A., & Verdelhan, A. (2018). *Deviations from Covered Interest Rate Parity*. Journal of Finance, 73(3), 915-957.
- Litterman, R., & Scheinkman, J. (1991). *Common Factors Affecting Bond Returns*. Journal of Fixed Income, 1(1), 54-61.
- Nelson, C. R., & Siegel, A. F. (1987). *Parsimonious Modeling of Yield Curves*. Journal of Business, 60(4), 473-489.
