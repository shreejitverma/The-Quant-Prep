---
type: concept
track: [quant-trader, quant-research]
tier: advanced
status: solid
prereqs: []
est_hours: 4
sources: [Brennan (1958) - The Supply of Storage, Working (1949) - The Theory of the Price of Storage, Gorton and Rouwenhorst (2006) - Facts and Fantasies about Commodity Futures, Erb and Harvey (2006) - The Strategic and Tactical Value of Commodity Futures]
---

# Commodity Term Structures and Storage Arbitrage

## TL;DR

- Unlike financial securities, physical commodities are consumption and production assets governed by the Theory of Storage: the forward price relationship is $F(t, T) = S(t) e^{(r + u - y)(T - t)}$, where $r$ is interest, $u$ is physical storage/insurance, and $y$ is the convenience yield.
- Contango ($F > S$) indicates physical inventory abundance and creates negative roll yield for long futures holders, while Backwardation ($F < S$) reflects physical scarcity, yielding a high convenience yield and positive roll yield.
- Total return for an unlevered commodity futures strategy decomposes into three additive components: Spot Return, Roll Return, and Collateral Yield.
- Continuous rolling in contango creates severe compounding decay in passive retail commodity ETFs (such as USO or UNG), causing long-term investment performance to decouple dramatically from underlying spot commodity prices.
- Energy processing margins are modeled via refinery Crack Spreads (such as the 3:2:1 spread between Crude Oil, Gasoline, and Heating Oil), reflecting the net processing margin of modern cracking facilities.

## Learning objectives

- Formulate the cost-of-carry model for storable commodities including physical warehousing, insurance, and convenience yields.
- Deconstruct commodity futures total returns into spot return, roll yield, and collateral yield.
- Analyze the physical mechanics that triggered negative WTI crude oil futures prices (-$37.63/bbl) on April 20, 2020.
- Calculate refinery processing margins using the 3:2:1 Crack Spread formula.
- Design cash-and-carry and reverse cash-and-carry spatial and temporal commodity storage arbitrage trades.

## Core concepts

### 1. The Theory of Storage and Cost-of-Carry Model

The modern Theory of Storage was established by Holbrook Working (1949) and Michael Brennan (1958).
The relationship between current spot price $S(t)$ and the futures price $F(t, T)$ for delivery at time $T$ is governed by three carrying costs:

$$F(t, T) = S(t) e^{(r + u - y)(T - t)}$$

where:
- $r$: Annualized financing cost (interest rate to borrow purchase capital).
- $u$: Physical carrying cost (storage warehousing, evaporation loss, tankering, and insurance) as a percentage of spot price.
- $y$: **Convenience Yield**, representing the implicit operational benefit of holding physical inventory in hand rather than a paper futures contract.

```
+-----------------------------------------------------------------------+
|                    THE DUAL REGIMES OF COMMODITY CURVES               |
+-----------------------------------------------------------------------+
| CONTANGO (Surplus Regime)             BACKWARDATION (Scarcity Regime) |
| F(T) > S                              F(T) < S                        |
| Net Carry > 0 (r + u > y)             Net Carry < 0 (y > r + u)       |
| Physical inventories abundant         Inventories severely depleted   |
| High storage tank utilization         Immediate physical supply crunch|
| Upward-sloping forward curve          Downward-sloping forward curve  |
| Roll yield for longs: NEGATIVE        Roll yield for longs: POSITIVE  |
+-----------------------------------------------------------------------+
```

```
Futures Curve Geometry:
Price ($)
   ^
   |        /  [CONTANGO CURVE: Upward Sloping]
   |       /
   |  Spot S -----------------------------
   |       \
   |        \  [BACKWARDATION CURVE: Downward Sloping]
   +-------------------------------------------> Expiration (Months)
```

In deep contango, the futures price is capped by the **Cash-and-Carry Arbitrage Bound**:
If $F(T) > S e^{(r + u) T}$, a trader buys physical commodity, stores it in an accredited warehouse, and sells the forward contract, locking in risk-free profit.
However, in backwardation, an inverted arbitrage bound does not exist: if physical inventories are exhausted, one cannot borrow physical crude or wheat from the future to sell short today.
Consequently, backwardation can reach extreme price dislocations.

### 2. The Decomposition of Commodity Returns

Gorton and Rouwenhorst (2006) proved that the total return of a fully collateralized long commodity futures position decomposes into three distinct sources:

$$R_{\text{total}} = R_{\text{spot}} + R_{\text{roll}} + R_{\text{collateral}}$$

```
+-----------------------------------------------------------------------+
|                    COMMODITY TOTAL RETURN DECOMPOSITION               |
+-----------------------------------------------------------------------+
| 1. Spot Return (R_spot):                                              |
|    Price appreciation of the underlying physical commodity.           |
| 2. Roll Return / Roll Yield (R_roll):                                 |
|    Convergence of futures price to spot as maturity approaches:       |
|    R_roll = - [F(T_2) - F(T_1)] / F(T_1)                              |
| 3. Collateral Yield (R_collateral):                                   |
|    Interest earned on cash margin held in short-term US Treasuries.   |
+-----------------------------------------------------------------------+
```

#### The Contango Roll Trap in Commodity ETFs
A retail exchange-traded fund (such as the United States Oil Fund, USO) that holds front-month futures must sell the expiring near-month contract ($F_1$) and buy the next-month contract ($F_2$) every month.
When the curve is in contango ($F_2 > F_1$), the fund sells cheap and buys expensive:

$$\text{Roll Drag per Cycle} = \frac{F_1 - F_2}{F_1} < 0$$

Over multiple years, persistent contango roll drag can completely destroy investor capital even if spot commodity prices double.

### 3. The Negative Pricing Anomaly: April 20, 2020

On April 20, 2020, the May 2020 WTI Crude Oil futures contract settled at **-$37.63 per barrel**, the first negative price in commodity market history:

```
+-----------------------------------------------------------------------+
|                    ANATOMY OF THE APRIL 2020 WTI COLLAPSE             |
+-----------------------------------------------------------------------+
| 1. Demand Destruction: COVID-19 lockdowns eliminated 30M bpd of demand|
| 2. Physical Delivery Point: WTI settles via mandatory physical delivery|
|    at pipeline terminals in Cushing, Oklahoma                         |
| 3. Storage Tank Capacity: Cushing storage tanks reached 100% capacity |
| 4. Contract Expiration: Speculative financial longs faced physical    |
|    delivery within 24 hours without storage tanks or pipeline access  |
| 5. Forced Liquidation: Commercial storage operators demanded $30-$40  |
|    per barrel to take delivery, forcing sellers to pay to shed crude  |
+-----------------------------------------------------------------------+
```

Because financial futures contracts with physical delivery require actual pipeline off-take, an absolute physical constraint overrides financial arbitrage.
When physical storage cost $u \to +\infty$, the theoretical forward price $F(T) = S e^{(r + u) T}$ can drop below zero if disposal costs are positive.

### 4. Refinery Crack Spreads: The 3:2:1 Model

Refineries operate by purchasing raw crude oil and refining it into refined petroleum products: gasoline and distillate fuels (diesel and heating oil).
The industry-standard metric for refinery gross margin is the **3:2:1 Crack Spread**:

$$\text{Inputs}: 3 \text{ barrels of Crude Oil} \implies \text{Outputs}: 2 \text{ barrels of Gasoline} + 1 \text{ barrel of Distillate}$$

Because crude oil is priced in dollars per barrel ($/bbl) while gasoline and heating oil are quoted in dollars per gallon ($/gal), unit conversion is required (1 barrel = 42 US gallons):

$$\text{Crack Margin ($/bbl)} = \frac{2 \times (P_{\text{Gasoline}} \times 42) + 1 \times (P_{\text{Heating Oil}} \times 42) - 3 \times P_{\text{Crude}}}{3}$$

```
+-----------------------------------------------------------------------+
|                    3:2:1 CRACK SPREAD CALCULATION EXAMPLE             |
+-----------------------------------------------------------------------+
| WTI Crude Oil: $75.00 / barrel                                        |
| RBOB Gasoline: $2.50 / gallon ($2.50 * 42 = $105.00 / barrel)         |
| Heating Oil:   $2.80 / gallon ($2.80 * 42 = $117.60 / barrel)         |
|                                                                       |
| Product Output Value = (2 * $105.00) + (1 * $117.60) = $327.60        |
| Crude Feedstock Cost = 3 * $75.00 = $225.00                           |
| Net Crack Value (3 barrels) = $327.60 - $225.00 = $102.60             |
| 3:2:1 Crack Spread Margin = $102.60 / 3 = $34.20 per barrel           |
+-----------------------------------------------------------------------+
```

When refinery margins expand, refineries bid aggressively for crude oil, raising feedstock demand.
When crack spreads collapse below operating costs, refineries curtail utilization runs, dampening crude demand.

---

## Worked examples

### Example 1: Cash-and-Carry Storage Arbitrage in Crude Oil
Suppose spot crude oil is trading at $70.00 per barrel.
The 6-month forward futures contract ($T = 0.5$ years) trades at $76.00 per barrel.
Financing interest rate is $r = 5.0\%$ annually, and physical storage plus insurance costs $u = \$0.60$ per barrel per month ($10.28\%$ annualized rate of spot price).
Convenience yield is $y = 0.0\%$ due to physical inventory surplus.

The theoretical no-arbitrage futures price is:
$$F_{\text{theo}} = S \cdot e^{(r + u) T} = 70.00 \times e^{(0.05 + 0.1028) \times 0.5} = 70.00 \times e^{0.0764} = 70.00 \times 1.0794 = \$75.56 \text{ per barrel}$$

Because the market futures price ($76.00) exceeds theoretical cost-of-carry ($75.56):
1. **Borrow cash** at 5.0% and purchase physical crude at $70.00.
2. **Contract commercial storage** for 6 months at $3.60 ($0.60 \times 6).
3. **Sell 6-month futures** at $76.00.

Total cash outflow at maturity $T$:
$$\text{Principal + Interest} = 70.00 \times e^{0.05 \times 0.5} = \$71.77$$
$$\text{Storage Outflow} = \$3.60$$
$$\text{Total Cost} = 71.77 + 3.60 = \$75.37$$
$$\text{Arbitrage Net Profit} = \$76.00 - \$75.37 = +\$0.63 \text{ per barrel}$$
By leasing storage capacity and shorting forward futures, the trader locks in a riskless annualized return above the risk-free benchmark.

---

## Pitfalls

- **Ignoring Negative Roll Drag in Long Commodity ETFs**: Holding passive long commodity ETFs during sustained contango regimes erodes portfolio capital through continuous negative roll yield.
- **Underestimating Storage Bottlenecks During Physical Delivery**: Assuming financial arbitrage can always bridge futures and spot prices, even when physical pipeline and tank capacity are exhausted (such as April 2020 WTI).
- **Neglecting Quality Grade Differentials in Agricultural Contracts**: Failing to account for protein discounts, moisture penalties, and delivery elevator basis risk when trading grains.
- **Confusing Nominal Gold Prices with Real Gold Drivers**: Treating gold as a generic inflation hedge rather than recognizing its tight structural inverse relationship with real Treasury yields.
- **Treating Crack Spreads as Symmetrical Arbitrage**: Overlooking refinery maintenance outages, environmental regulations, and seasonal fuel blending mandates that decouple product margins.

---

## Interview questions

> [!question] mkt-cmd-001 | What is the fundamental difference between a commodity futures contract and an equity forward?
> Commodities are physical consumption assets subject to storage costs, transportation constraints, and convenience yields.

> [!question] mkt-cmd-002 | What is the cost-of-carry formula for a storable commodity forward price?
> F(t, T) = S(t) * exp((r + u - y) * (T - t)).

> [!question] mkt-cmd-003 | What is Convenience Yield in the Theory of Storage?
> The operational and business benefit associated with holding physical inventory rather than a paper futures contract.

> [!question] mkt-cmd-004 | What is Contango in a commodity forward curve?
> A market structure where futures prices exceed current spot prices (F > S), resulting in an upward-sloping forward curve.

> [!question] mkt-cmd-005 | What is Backwardation in a commodity forward curve?
> A market structure where current spot prices exceed futures prices (S > F), resulting in a downward-sloping forward curve.

> [!question] mkt-cmd-006 | What economic condition causes a commodity to enter deep backwardation?
> Immediate physical supply scarcity and inventory depletion, driving the convenience yield above financing and storage costs (y > r + u).

> [!question] mkt-cmd-007 | What are the three components of total return for an unlevered long commodity futures position?
> Spot Return, Roll Yield, and Collateral Yield.

> [!question] mkt-cmd-008 | What is Roll Yield (Roll Return)?
> The price change experienced as a futures contract converges toward spot price over time along the term structure curve.

> [!question] mkt-cmd-009 | Why does continuous rolling in a contango market create negative roll yield for long investors?
> The fund must sell expiring near-month contracts at lower prices and buy next-month contracts at higher prices (selling low, buying high).

> [!question] mkt-cmd-010 | Why is the backwardation arbitrage bound asymmetric compared to contango?
> In backwardation, traders cannot borrow physical commodities from future periods to sell short if existing inventories are depleted.

> [!question] mkt-cmd-011 | What delivery hub serves as the official physical settlement point for NYMEX WTI Crude Oil?
> Cushing, Oklahoma.

> [!question] mkt-cmd-012 | Why did WTI Crude Oil futures trade at negative $37.63 per barrel on April 20, 2020?
> Physical storage capacity at Cushing was completely full, forcing financial longs facing physical delivery to pay to unload contracts.

> [!question] mkt-cmd-013 | What is a Crack Spread?
> The pricing spread simulating the gross refining margin earned by converting raw crude oil into refined petroleum products.

> [!question] mkt-cmd-014 | What are the volumetric proportions in a standard 3:2:1 refinery crack spread?
> Three barrels of crude oil yield two barrels of gasoline and one barrel of distillate (diesel/heating oil).

> [!question] mkt-cmd-015 | How many US gallons are in one standardized barrel of crude oil?
> Exactly 42 gallons.

> [!question] mkt-cmd-016 | How is gasoline quoted on futures exchanges versus crude oil?
> Gasoline is quoted in dollars per gallon; crude oil is quoted in dollars per barrel.

> [!question] mkt-cmd-017 | What is the formula for calculating the 3:2:1 Crack Margin in dollars per barrel?
> [2 * (Gasoline Price * 42) + 1 * (Heating Oil Price * 42) - 3 * Crude Price] / 3.

> [!question] mkt-cmd-018 | What is the primary benchmark for European and international waterborne crude oil?
> Brent Crude, sourced from the North Sea.

> [!question] mkt-cmd-019 | Why does Gold typically trade in a permanent contango market structure?
> Gold is a monetary store of value with virtually zero industrial consumption, low storage costs, and zero convenience yield.

> [!question] mkt-cmd-020 | What macro factor exhibits the strongest negative correlation with the price of Gold?
> Real interest rates (TIPS yields).

> [!question] mkt-cmd-021 | What is the Gold-to-Silver Ratio?
> The price of an ounce of gold divided by the price of an ounce of silver, tracking monetary hedge demand versus industrial demand.

> [!question] mkt-cmd-022 | What commodity is known as 'Doctor Copper' and why?
> Copper, because its widespread industrial use makes its price a reliable diagnostic of global manufacturing and GDP health.

> [!question] mkt-cmd-023 | What is Henry Hub?
> The pipeline distribution hub in Erath, Louisiana, that serves as the official delivery point for NYMEX Natural Gas futures.

> [!question] mkt-cmd-024 | What is the injection season versus withdrawal season for US Natural Gas storage?
> Injection occurs during mild weather from April to October; withdrawal occurs during winter heating demand from November to March.

> [!question] mkt-cmd-025 | What are Heating Degree Days (HDD) and Cooling Degree Days (CDD)?
> Weather metrics measuring the extent to which daily temperatures deviate from 65 degrees Fahrenheit, driving natural gas and electricity demand.

> [!question] mkt-cmd-026 | What is the USDA WASDE report?
> The World Agricultural Supply and Demand Estimates, a monthly report detailing global crop production, consumption, and ending stocks.

> [!question] mkt-cmd-027 | What is the 'stocks-to-use ratio' in agricultural commodity analysis?
> Carryover ending inventory divided by total annual consumption, measuring the cushion against harvest failure.

> [!question] mkt-cmd-028 | What is cash-and-carry storage arbitrage in commodities?
> Buying spot physical commodity, financing the purchase, storing it in a warehouse, and selling forward futures to capture the carry spread.

> [!question] mkt-cmd-029 | What is 'local basis' in agricultural grain trading?
> The difference between the local grain elevator cash price and the Chicago Board of Trade (CBOT) futures price.

> [!question] mkt-cmd-030 | What is the Spark Spread in energy trading?
> The theoretical gross margin of a gas-fired power plant from selling wholesale electricity and purchasing natural gas fuel.

> [!question] mkt-cmd-031 | What is Keynes's Theory of Normal Backwardation?
> The proposition that commodity producers sell forward futures at a discount to induce risk-bearing speculators to provide insurance.

> [!question] mkt-cmd-032 | What is the primary operational lesson for commodity portfolio allocation?
> Never hold passive long commodity futures without factoring in the drag of term structure contango and roll yield.

---

## Further reading

- Brennan, M. J. (1958). *The Supply of Storage*. American Economic Review, 48(1), 50-72.
- Erb, C. B., & Harvey, C. R. (2006). *The Strategic and Tactical Value of Commodity Futures*. Financial Analysts Journal, 62(2), 69-97.
- Gorton, G., & Rouwenhorst, K. G. (2006). *Facts and Fantasies about Commodity Futures*. Financial Analysts Journal, 62(2), 47-68.
- Working, H. (1949). *The Theory of the Price of Storage*. American Economic Review, 39(6), 1254-1262.
