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
- Total return for a fully collateralised commodity futures position is conventionally decomposed into Spot Return, Roll Return, and Collateral Yield (see Erb and Harvey 2006).
- Rolling long futures through contango charges a roll cost every cycle, so the returns of front-month commodity funds (such as USO or UNG) can diverge widely from the spot price over long holding periods.
- Energy processing margins are modeled via refinery Crack Spreads (such as the 3:2:1 spread between Crude Oil, Gasoline, and Heating Oil), reflecting the net processing margin of modern cracking facilities.

## Learning objectives

- Formulate the cost-of-carry model for storable commodities including physical warehousing, insurance, and convenience yields.
- Deconstruct commodity futures total returns into spot return, roll yield, and collateral yield.
- Analyze the physical mechanics behind the negative settlement of the May 2020 WTI crude oil futures contract (-$37.63/bbl) on April 20, 2020.
- Calculate refinery processing margins using the 3:2:1 Crack Spread formula.
- Design cash-and-carry and reverse cash-and-carry spatial and temporal commodity storage arbitrage trades.

## Core concepts

### 1. The Theory of Storage and Cost-of-Carry Model

The Theory of Storage was developed by Holbrook Working (1949) and Michael Brennan (1958), among others.
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
If $F(T) > S e^{(r + u) T}$, a trader buys physical commodity, stores it in an accredited warehouse, and sells the forward contract, locking in a profit that is riskless apart from storage, delivery and counterparty risk.
However, in backwardation, an inverted arbitrage bound does not exist: if physical inventories are exhausted, one cannot borrow physical crude or wheat from the future to sell short today.
Consequently, backwardation can reach extreme price dislocations.

### 2. The Decomposition of Commodity Returns

The total return of a fully collateralised long commodity futures position is conventionally split into three sources (Erb and Harvey 2006 discuss the decomposition; Gorton and Rouwenhorst 2006 study the returns of such positions):

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

Because the drag compounds every cycle, a long-only front-month fund in persistent contango can lose money even over periods when the spot price rises.

### 3. The Negative Pricing Anomaly: April 20, 2020

On April 20, 2020, the May 2020 NYMEX WTI Crude Oil futures contract settled at **-$37.63 per barrel**, down from $17.73 the previous day (CFTC press release 8315-20, November 23, 2020); EIA noted it was the first negative price since the contract began trading in 1983:

```
+-----------------------------------------------------------------------+
|                    ANATOMY OF THE APRIL 2020 WTI COLLAPSE             |
+-----------------------------------------------------------------------+
| 1. Demand Destruction: the IEA (April 2020 Oil Market Report)        |
|    estimated April 2020 demand 29 mb/d below a year earlier          |
| 2. Physical Delivery Point: WTI futures are physically delivered at   |
|    pipeline and storage facilities in Cushing, Oklahoma               |
| 3. Storage Tightness: EIA put Cushing tank farms at about 76% of      |
|    working capacity on April 17, 2020 (58 of 76 million barrels),     |
|    with much of the rest already contracted                           |
| 4. Contract Expiration: the May contract expired on April 21, so      |
|    longs without storage or pipeline access had one day to exit       |
| 5. Low Liquidity: with few buyers able to take barrels, longs paid    |
|    to close, and the price fell through zero                          |
+-----------------------------------------------------------------------+
```

The contract terms matter here: per CME Group's NYMEX WTI Light Sweet Crude Oil (CL) specifications (as of November 2026), one contract is 1,000 barrels, the minimum tick is $0.01 per barrel ($10 per contract), delivery is physical at Cushing, and trading ends three business days before the 25th calendar day of the month before delivery (four if the 25th is not a business day).
Because financial futures contracts with physical delivery require actual pipeline off-take, an absolute physical constraint overrides financial arbitrage.
The cost-of-carry formula $F(T) = S e^{(r + u - y) T}$ cannot produce a negative price, because it assumes storage is available at some finite cost.
When a long without storage access cannot find anyone to take the barrels at a positive price, it must pay to be relieved of them, so the expiring futures price can fall below zero; storage need not be physically full for this, only unavailable to the marginal seller.

### 4. Refinery Crack Spreads: The 3:2:1 Model

Refineries operate by purchasing raw crude oil and refining it into refined petroleum products: gasoline and distillate fuels (diesel and heating oil).
A widely used benchmark for refinery gross margin is the **3:2:1 Crack Spread**:

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
Suppose spot crude oil is trading at $70.00 per barrel (all inputs hypothetical).
The 6-month forward futures contract ($T = 0.5$ years) trades at $76.00 per barrel.
Financing interest rate is $r = 5.0\%$ annually (continuously compounded), and physical storage plus insurance costs a fixed $\$0.60$ per barrel per month, invoiced at maturity ($U_T = 6 \times \$0.60 = \$3.60$).
Convenience yield is $y = 0.0\%$ due to physical inventory surplus.

Because storage is a fixed dollar amount paid at $T$, the theoretical no-arbitrage futures price adds it to the financed spot price:
$$F_{\text{theo}} = S \cdot e^{r T} + U_T = 70.00 \times e^{0.05 \times 0.5} + 3.60 = 70.00 \times 1.02532 + 3.60 = 71.77 + 3.60 = \$75.37 \text{ per barrel}$$
Quoting the storage as a simple $7.20 / 70.00 = 10.29\%$ annual rate and plugging it into $S e^{(r + u) T}$ would give $70.00 \times e^{0.07643} = \$75.56$, which overstates the carry by compounding and financing the storage charge.
The continuously compounded storage rate consistent with $\$3.60$ paid at maturity is $u = 2 \ln(75.372 / 70.00) - 0.05 = 9.79\%$.

Because the market futures price ($76.00) exceeds theoretical cost-of-carry ($75.37):
1. **Borrow cash** at 5.0% and purchase physical crude at $70.00.
2. **Contract commercial storage** for 6 months at $3.60 ($0.60 \times 6).
3. **Sell 6-month futures** at $76.00.

Total cash outflow at maturity $T$:
$$\text{Principal + Interest} = 70.00 \times e^{0.05 \times 0.5} = \$71.77$$
$$\text{Storage Outflow} = \$3.60$$
$$\text{Total Cost} = 71.77 + 3.60 = \$75.37$$
$$\text{Arbitrage Net Profit} = \$76.00 - \$75.37 = +\$0.63 \text{ per barrel}$$
By leasing storage capacity and shorting the futures, the trader locks in $0.63 per barrel above financing and storage costs, exposed only to storage, delivery and counterparty risk.

---

## Pitfalls

- **Ignoring Negative Roll Drag in Long Commodity ETFs**: Holding passive long commodity ETFs during sustained contango regimes erodes portfolio capital through continuous negative roll yield.
- **Underestimating Storage Bottlenecks During Physical Delivery**: Assuming financial arbitrage can always bridge futures and spot prices, even when physical pipeline and tank capacity are exhausted (such as April 2020 WTI).
- **Neglecting Quality Grade Differentials in Agricultural Contracts**: Failing to account for protein discounts, moisture penalties, and delivery elevator basis risk when trading grains.
- **Assuming a Stable Gold Driver**: Treating gold as a generic inflation hedge, or assuming its often-cited inverse relation with real Treasury yields is stable; the relation varies over time and should be measured, not assumed.
- **Treating Crack Spreads as Symmetrical Arbitrage**: Overlooking refinery maintenance outages, environmental regulations, and seasonal fuel blending mandates that decouple product margins.

---

## Interview questions

> [!question]- mkt-cmd-001 | What is the fundamental difference between a commodity futures contract and an equity forward?
> Commodities are physical consumption assets subject to storage costs, transportation constraints, and convenience yields.

> [!question]- mkt-cmd-002 | What is the cost-of-carry formula for a storable commodity forward price?
> F(t, T) = S(t) * exp((r + u - y) * (T - t)).

> [!question]- mkt-cmd-003 | What is Convenience Yield in the Theory of Storage?
> The operational and business benefit associated with holding physical inventory rather than a paper futures contract.

> [!question]- mkt-cmd-004 | What is Contango in a commodity forward curve?
> A market structure where futures prices exceed current spot prices (F > S), resulting in an upward-sloping forward curve.

> [!question]- mkt-cmd-005 | What is Backwardation in a commodity forward curve?
> A market structure where current spot prices exceed futures prices (S > F), resulting in a downward-sloping forward curve.

> [!question]- mkt-cmd-006 | What economic condition causes a commodity to enter deep backwardation?
> Immediate physical supply scarcity and inventory depletion, driving the convenience yield above financing and storage costs (y > r + u).

> [!question]- mkt-cmd-007 | What are the three components of total return for an unlevered long commodity futures position?
> Spot Return, Roll Yield, and Collateral Yield.

> [!question]- mkt-cmd-008 | What is Roll Yield (Roll Return)?
> The price change experienced as a futures contract converges toward spot price over time along the term structure curve.

> [!question]- mkt-cmd-009 | Why does continuous rolling in a contango market create negative roll yield for long investors?
> The fund must sell expiring near-month contracts at lower prices and buy next-month contracts at higher prices (selling low, buying high).

> [!question]- mkt-cmd-010 | Why is the backwardation arbitrage bound asymmetric compared to contango?
> In backwardation, traders cannot borrow physical commodities from future periods to sell short if existing inventories are depleted.

> [!question]- mkt-cmd-011 | What delivery hub serves as the official physical settlement point for NYMEX WTI Crude Oil?
> Cushing, Oklahoma.

> [!question]- mkt-cmd-012 | Why did WTI Crude Oil futures trade at negative $37.63 per barrel on April 20, 2020?
> With the May contract expiring the next day and Cushing storage tight (EIA: tank farms about 76% of working capacity on April 17, much of the rest committed), longs who could not take delivery had to pay buyers to take their contracts.
> Storage did not have to be literally full; it only had to be unavailable to the longs who needed to exit.

> [!question]- mkt-cmd-013 | What is a Crack Spread?
> The pricing spread simulating the gross refining margin earned by converting raw crude oil into refined petroleum products.

> [!question]- mkt-cmd-014 | What are the volumetric proportions in a standard 3:2:1 refinery crack spread?
> Three barrels of crude oil yield two barrels of gasoline and one barrel of distillate (diesel/heating oil).

> [!question]- mkt-cmd-015 | How many US gallons are in one standardized barrel of crude oil?
> Exactly 42 gallons.

> [!question]- mkt-cmd-016 | How is gasoline quoted on futures exchanges versus crude oil?
> Gasoline is quoted in dollars per gallon; crude oil is quoted in dollars per barrel.

> [!question]- mkt-cmd-017 | What is the formula for calculating the 3:2:1 Crack Margin in dollars per barrel?
> [2 * (Gasoline Price * 42) + 1 * (Heating Oil Price * 42) - 3 * Crude Price] / 3.

> [!question]- mkt-cmd-018 | What is the primary benchmark for European and international waterborne crude oil?
> Brent Crude, sourced from the North Sea.

> [!question]- mkt-cmd-019 | Why does Gold typically trade in a permanent contango market structure?
> Gold stocks are huge relative to annual consumption and cheap to store, so its convenience yield (the gold lease rate) is usually small relative to interest rates and the curve sits near full carry.
> "Permanent" overstates it: when lease rates rise above interest rates the gold curve can briefly backwardate.

> [!question]- mkt-cmd-020 | What macro factor exhibits the strongest negative correlation with the price of Gold?
> Real interest rates (TIPS yields) are the most commonly cited driver, with higher real yields raising the opportunity cost of holding gold; the strength of the relation varies across periods, so measure it rather than assume it.

> [!question]- mkt-cmd-021 | What is the Gold-to-Silver Ratio?
> The price of an ounce of gold divided by the price of an ounce of silver, tracking monetary hedge demand versus industrial demand.

> [!question]- mkt-cmd-022 | What commodity is known as 'Doctor Copper' and why?
> Copper, because its wide industrial use makes its price sensitive to global manufacturing and construction activity; the nickname overstates its reliability as a forecaster.

> [!question]- mkt-cmd-023 | What is Henry Hub?
> The Sabine Pipe Line Henry Hub in Erath, Louisiana, the delivery point for NYMEX Henry Hub Natural Gas futures (10,000 MMBtu per contract).

> [!question]- mkt-cmd-024 | What is the injection season versus withdrawal season for US Natural Gas storage?
> By EIA convention the injection season runs April to October and the withdrawal season November to March; actual weekly flows can deviate at either end.

> [!question]- mkt-cmd-025 | What are Heating Degree Days (HDD) and Cooling Degree Days (CDD)?
> Weather metrics measuring the extent to which daily temperatures deviate from 65 degrees Fahrenheit, driving natural gas and electricity demand.

> [!question]- mkt-cmd-026 | What is the USDA WASDE report?
> The World Agricultural Supply and Demand Estimates, a monthly report detailing global crop production, consumption, and ending stocks.

> [!question]- mkt-cmd-027 | What is the 'stocks-to-use ratio' in agricultural commodity analysis?
> Carryover ending inventory divided by total annual consumption, measuring the cushion against harvest failure.

> [!question]- mkt-cmd-028 | What is cash-and-carry storage arbitrage in commodities?
> Buying spot physical commodity, financing the purchase, storing it in a warehouse, and selling forward futures to capture the carry spread.

> [!question]- mkt-cmd-029 | What is 'local basis' in agricultural grain trading?
> The difference between the local grain elevator cash price and the Chicago Board of Trade (CBOT) futures price.

> [!question]- mkt-cmd-030 | What is the Spark Spread in energy trading?
> The theoretical gross margin of a gas-fired power plant from selling wholesale electricity and purchasing natural gas fuel.

> [!question]- mkt-cmd-031 | What is Keynes's Theory of Normal Backwardation?
> Keynes's proposition (A Treatise on Money, 1930) that hedgers who are net short futures pay speculators a risk premium, so futures trade below the expected future spot price and drift up toward it.

> [!question]- mkt-cmd-032 | What is the primary operational lesson for commodity portfolio allocation?
> Never hold passive long commodity futures without factoring in the drag of term structure contango and roll yield.

## In this repo and The-Distinguished-Engineer

- Code: [mkt_cmdty_01_storage.py](../code/mkt_cmdty_01_storage.py) prints and asserts every number in this note; the crack spread is computed per barrel and per gallon, and the carry arbitrage by an explicit cash-flow ledger; event facts are cited to CFTC, EIA and IEA; run it with `uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_cmdty_01_storage.py`.
- Syllabus: [Commodities and Futures Curves](../../06-Fixed-Income-and-Asset-Classes/09-Commodities-and-Futures-Curves.md).

---

## Further reading

- Brennan, M. J. (1958). *The Supply of Storage*. American Economic Review, 48(1), 50-72.
- Commodity Futures Trading Commission. (2020). *Interim Staff Report: Trading in NYMEX WTI Crude Oil Futures Contract Leading up to, on, and around April 20, 2020*. CFTC, November 2020.
- Energy Information Administration. (2020). *Low liquidity and limited available storage pushed WTI crude oil futures prices below zero*. Today in Energy, April 27, 2020.
- Erb, C. B., & Harvey, C. R. (2006). *The Strategic and Tactical Value of Commodity Futures*. Financial Analysts Journal, 62(2), 69-97.
- International Energy Agency. (2020). *Oil Market Report - April 2020*. IEA.
- Gorton, G., & Rouwenhorst, K. G. (2006). *Facts and Fantasies about Commodity Futures*. Financial Analysts Journal, 62(2), 47-68.
- Working, H. (1949). *The Theory of the Price of Storage*. American Economic Review, 39(6), 1254-1262.
