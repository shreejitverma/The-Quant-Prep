---
type: cfa-lm
topic: "Alternative Investments"
topic_code: "08"
topic_slug: "08-Alternative-Investments"
volume: 8
lm: 1
title: "Introduction to Commodities and Commodity Derivatives"
pages: "3-61"
weight_band: "5-10%"
difficulty: 2
los_count: 10
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/alternative-investments]
---

# LM1: Introduction to Commodities and Commodity Derivatives

Difficulty 2 of 5: the arithmetic (price, roll, collateral, total return) is short division, but the exam swaps definitions relentlessly (basis vs calendar spread, contango vs backwardation signs, the three theories, the five swap types, the five indexes), so the risk is taxonomy confusion under time pressure, not computation.

## LOS map

- **compare** characteristics of commodity sectors (V8 p.3) ^los-08-01-a
    - Examiner asks: match a sector (energy, grains, industrial metals, livestock, precious metals, softs) to its dominant supply or demand driver, for example which sector is least affected by weather (precious metals) or which responds to industrial activity (copper).
- **compare** the life cycle of commodity sectors from production through trading or consumption (V8 p.3) ^los-08-01-b
    - Examiner asks: which sector's life cycle is most flexible (metals, storable for years), why crude oil differs from natural gas (crude must be refined), why livestock was historically least export oriented (spoilage), and why metal producers cannot cut capacity quickly (economies of scale).
- **contrast** the valuation of commodities with the valuation of equities and bonds (V8 p.3) ^los-08-01-c
    - Examiner asks: identify the factor that prices stocks and bonds but not commodities (expected future cash flows); commodities are valued as a discounted forecast of future prices and incur storage and transport costs instead of paying income.
- **describe** types of participants in commodity futures markets (V8 p.3) ^los-08-01-d
    - Examiner asks: classify a fund from vignette clues as hedger, speculator/liquidity provider, or arbitrageur (access to storage facilities plus spot-futures mispricing means arbitrageur), or name the trader type that provides insurance to hedgers (liquidity providers).
- **analyze** the relationship between spot prices and futures prices in markets in contango and markets in backwardation (V8 p.3) ^los-08-01-e
    - Examiner asks: from a table of spot, near and far futures prices, identify which market is in backwardation, then compute the basis (spot minus near futures) and the calendar spread (near minus far futures) without mixing the two up.
- **compare** theories of commodity futures returns (V8 p.3) ^los-08-01-f
    - Examiner asks: match vignette facts to insurance theory (producers sell forward at a discount), hedging pressure hypothesis (whichever side hedges more pushes the curve), or theory of storage (futures = spot + storage costs - convenience yield), including the trap where a contango curve with convenience yield above storage costs can only be hedging pressure.
- **describe, calculate,** and interpret the components of total return for a fully collateralized commodity futures contract (V8 p.3) ^los-08-01-g
    - Examiner asks: compute total return = price return + roll return + collateral return, scaling the collateral rate (and only the annualized inputs) to the holding period, as in the soybean (0.85%) and natural gas (1.46%) problems.
- **contrast** roll return in markets in contango and markets in backwardation (V8 p.3) ^los-08-01-h
    - Examiner asks: sign of the roll return (positive in backwardation, negative in contango), and whether maintaining constant dollar exposure on the roll requires buying more contracts (backwardation, cheaper far contract) or fewer (contango).
- **describe** how commodity swaps are used to obtain or modify exposure to commodities (V8 p.3) ^los-08-01-i
    - Examiner asks: pick the right swap for a stated view (excess return, total return, basis, variance, volatility) and compute the reset payments on a total return swap, including who pays when the index falls.
- **describe** how the construction of commodity indexes affects index returns (V8 p.3) ^los-08-01-j
    - Examiner asks: contrast S&P GSCI (production weighted, energy heavy, monthly roll to nearby) with BCOM (production and liquidity weighted, 33% sector cap, 2% commodity floor) and predict which construction wins in a trending versus mean-reverting market or with backwardation-heavy contracts.

## Core intuition

A commodity is a physical good attributable to a natural resource, tradable and supplied without substantial differentiation by the general public (V8 p.4).
That physicality is the source of everything in this module.
Stocks and bonds are claims on future cash flows, so their intrinsic value is a present discounted value of expected cash flows (V8 p.5, p.14).
A pile of copper pays no coupon and never will.
Its value comes from use, as a consumable or as an input to production, so a commodity is valued as a discounted forecast of future possible prices, driven by supply, demand and expected price volatility (V8 p.14).
Owning the physical good costs money rather than paying it: storage, insurance, transport, spoilage (V8 p.14).
Those carrying costs, and the occasional desperation of users who need the material today, are what shape the futures curve.

> [!abstract] Idea 1: commodities are valued off forecast prices, not cash flows, and are held mostly through derivatives
> The one factor that prices financial assets but not commodities is expected future cash flows (V8 p.14, p.58).
> Because storing hogs or crude is costly and specialized, investors take exposure through futures, swaps and index products rather than the physical good, which is why the whole module is really about the futures curve (V8 p.3, p.15).
> Some newer commodity classes (electricity, weather) are not even storable physical assets, and arbitrage between spot and futures is only a boundary condition, not an equality, when participants cannot make or take delivery (V8 p.14, p.15).

The curriculum segments the asset class the way the Bloomberg Commodity Index does: energy, grains, industrial (base) metals, livestock, precious metals, and softs (cash crops) (V8 p.6).
Each sector is a different mix of stocks (potential production: fields, arable land, herd size, smelter capacity) and flows (utilization: weather, GDP growth, policy, disease), overlaid with timing and seasonality and with money flow from sentiment and monetary conditions (V8 p.5, p.6).
The exam versions of this are pattern matches: energy demand swings with weather and GDP, grains and softs with weather and disease, industrial metals with GDP and infrastructure, livestock with feed cost and disease, and precious metals with central bank policy and inflation expectations because they are monetary stores of value (V8 p.7).
Life cycle length then determines how fast supply can react (V8 p.8, p.9).
Natural gas is consumable at extraction while crude oil is useless until refined through cracking, refineries cost billions, and pipelines get blown up more often than refineries (V8 p.9, p.10).
Metals have the most flexible life cycle because ore and finished metal store for years, but smelters have such economies of scale that producers keep overproducing in downturns until weaker competitors die, and new capacity tends to arrive exactly as demand rolls over (V8 p.11).
Livestock matures on a biological clock (poultry in weeks, hogs in about six months, cattle in years), and until cryogenics the slaughtered product spoiled too fast to export (V8 p.12).
Grains follow planting, growth, pod/ear/head formation, harvest, with hemispheres out of phase, and are stored in silos against year-round demand (V8 p.13).
Softs are income crops grown around the Equator; coffee comes in robusta (London futures) and arabica (New York futures) varieties that are not interchangeable for delivery (V8 p.13, p.14, p.22).

The futures market itself is a zero-sum, margin-secured insurance exchange (V8 p.16, p.17).
Longs equal shorts in aggregate, unlike stocks and bonds where the market is net long the outstanding securities, and shorting a future is symmetric in margin, unlike shorting a stock (V8 p.17).
Participants come in five groups: hedgers (producers and consumers transferring price risk), traders and investors (informed investors, liquidity providers, arbitrageurs), the exchanges themselves, analysts, and regulators (CFTC delegating to the NFA in the United States, unified regulators elsewhere, IOSCO harmonizing) (V8 p.17, p.18, p.19).
Hedging and long/short are independent axes: a food manufacturer hedges long corn, a gold miner hedges short gold, an oil major speculates long or short on its own information, a CTA speculates for clients (V8 p.18).
Liquidity providers are the traders selling insurance, buying when producers must sell and selling when consumers must buy, for an expected but not guaranteed profit (V8 p.18).
Arbitrageurs are the ones with warehouses, silos and feedlots, monetizing mispricing between the physical (plus storage and financing) and the future (V8 p.18).

> [!abstract] Idea 2: the shape of the futures curve is the price of insurance and storage
> Basis = spot - futures; backwardation means spot above futures (positive basis, positive calendar spread), contango the reverse (V8 p.20, p.21).
> Three theories explain the shape: Keynes's insurance theory says producers sell forward at a discount so speculators can earn a risk premium, predicting "normal backwardation" (V8 p.25); the hedging pressure hypothesis generalizes it so that whichever side has the greater need for insurance pushes the curve away from itself, contango when consumer hedging dominates, backwardation when producer hedging dominates, flat when balanced (V8 p.26, p.27, p.28); the theory of storage says Futures = Spot + Direct storage costs - Convenience yield, so heavily stored commodities trade in contango and just-in-time commodities with scarce inventories trade in backwardation (V8 p.29).
> All three have unobservable components (storage costs are proprietary, convenience yield jumps with events, hedging asymmetry is unmeasurable), so the exam tests matching facts to theories, not estimating them (V8 p.28, p.29).

Convenience yield deserves its own sentence because it is the only genuinely new variable.
Holding inventory is convenient: it buffers a bread company or refiner against a supply disruption that would shut its operations, so the benefit is large when inventories are scarce and small when stock is abundant (V8 p.29).
The Libya 2011 case shows the mechanics: constricted supply of high-quality crude raised the spot price and the convenience yield in near contracts while deferred months stayed calm, pushing the curve into backwardation (V8 p.29).
Kolb's verdict that "normal backwardation is not normal" is the empirical warning: backwardation does not statistically guarantee positive returns, which is why the more nuanced theories exist (V8 p.26).

> [!abstract] Idea 3: futures total return decomposes into price, roll and collateral, and roll return is accounting, not a harvestable asset
> Total return on a fully collateralized futures position = price return + roll return + collateral return, plus a rebalance return at index level (V8 p.34).
> The roll return is the percentage gap between the near contract sold and the farther contract bought, weighted by the fraction of the position rolled; it is positive in backwardation (buying the cheaper far contract) and negative in contango, and you cannot build a portfolio of only roll returns (V8 p.32, p.33).
> Historically for the S&P GSCI (1970-2019) total return was 6.8% = 3.0% spot - 1.3% roll + 5.0% collateral, with nearly all the volatility (19.8%) coming from the spot component, so collateral, not commodity prices, supplied most of the long-run return (V8 p.34).

The roll mechanics are where candidates lose easy points.
In backwardation the far contract is cheaper, so maintaining constant dollar exposure requires buying more contracts (the pound 110 wheat example rolls 11 near contracts into 12 far ones); in contango the far contract is dearer, so fewer contracts are needed (the pound 108 gasoline example rolls 12 into 11) (V8 p.32).
Sector history matters: industrial metals, agriculture, livestock, precious metals and softs all show statistically strong negative mean roll returns because they are stored at length (gold's perpetual storage makes precious metals persistently negative), while energy alone has had a shot at positive roll return because it is consumed nearly in real time, though shale supply after 2010 raised oil's convenience of availability and eroded that edge (V8 p.37).
Roll return matters in any single period but has been modest against price return over long horizons, and its correlation with price return is roughly 3%, so it is not a directional signal (V8 p.36, p.38).

Swaps replace a stack of futures with one negotiated contract: customized quality, quantity and timing, with a dealer who lays the risk off in futures, an offsetting swap, or a physical purchase contract (V8 p.39).
The exam's five types: excess return swap (payments driven by the change in the futures-based index price versus a benchmark level), total return swap (excess return plus collateral interest, the institutional access vehicle), basis swap (difference between two imperfectly correlated reference prices, liquid Brent versus illiquid heavy crude), variance swap (realized versus fixed variance, often capped), and volatility swap (realized versus expected volatility, a pure bet on how volatile, not which direction) (V8 p.40, p.41, p.42).

Indexes make commodities an asset class: benchmark, macro indicator, and investment basis (V8 p.43).
Five constructions differ on breadth, weighting, roll methodology, rebalancing frequency, and governance (V8 p.43, p.44).
S&P GSCI: 24 commodities, world production value weighted (energy historically up to 80%), rolls monthly into the nearby most liquid contract, rebalances annually (V8 p.44, p.45).
BCOM: 23 commodities, production and liquidity weighted with a 33% sector cap and 2% commodity floor, selection based, so natural gas gets about 9% versus about 3% in the GSCI and drags roughly 19% annualized roll cost (V8 p.44, p.45).
DBLCI: 14 commodities, fixed weights, and the one active roll rule, optimizing across the next 12 months for maximum backwardation or minimum contango per month (V8 p.44, p.46).
TR/CC CRB: 19 commodities, committee-set fixed weights in tiers, front-month roll, monthly rebalance (V8 p.44, p.46).
RICI: 38 commodities including exotics, fixed weights in tiers, front-month roll, monthly rebalance, with some non-USD contracts adding FX exposure (V8 p.44, p.46).
Rebalancing frequency is a bet on market character: frequent rebalancing harvests mean reversion but bleeds in trends, and production-value weighting drifts with prices so it rebalances less violently than fixed weights, letting GSCI and BCOM outperform fixed-weight monthly rebalancers in trending markets (V8 p.46, p.47).
All the major indexes correlate above 70% with each other and near 0% with stocks and bonds, so no methodology dominates (V8 p.47).

## Formulas and derivations

**Basis** (V8 p.20)
$$
\text{Basis} = \text{Spot price} - \text{Futures price}
$$
^f-08-01-1

- Spot price: current price for physical delivery at a specific location; futures price: exchange price for deferred delivery; same units (per barrel, per bushel).
- Positive basis (spot above futures) is backwardation; negative basis is contango (V8 p.20).
- It measures the reward to owning the physical good now versus a claim on it later, so it moves with convenience yield and storage costs.

**Calendar spread** (V8 p.21)
$$
\text{Calendar spread} = F_{\text{near}} - F_{\text{far}}
$$
^f-08-01-2

- $F_{\text{near}}$: closing price of the futures contract nearer to expiration; $F_{\text{far}}$: closing price of the longer-dated contract.
- Positive spread means backwardation, negative means contango; the curriculum's examples are crude oil $65.50 - 64.00 = +1.50$ per barrel and lean hogs $95 - 96 = -1.0$ cent per pound (V8 p.21).
- Do not confuse it with the basis: the basis compares spot with futures, the calendar spread compares two futures.

**Theory of storage futures price** (V8 p.29)
$$
\text{Futures price} = \text{Spot price} + \text{Direct storage costs} - \text{Convenience yield}
$$
^f-08-01-3

- Direct storage costs: rent, insurance and similar cash outlays over the contract term; convenience yield: the non-cash benefit of holding available inventory as a buffer against supply disruption.
- Holds because a stored commodity must compensate the holder for carry, while scarce inventory makes immediate possession worth a premium; convenience yield is low when stock is abundant and rises as inventories shrink (V8 p.29).
- Contango when storage costs dominate; backwardation when convenience yield exceeds storage costs.

**Price return (spot yield)** (V8 p.32)
$$
\text{Price return} = \frac{\text{Current price} - \text{Previous price}}{\text{Previous price}}
$$
^f-08-01-4

- Prices are futures prices, generally the front-month contract, not physical spot quotes, because physical markets lack standardization (V8 p.32).
- It is the component that carries essentially all the volatility of a commodity index (19.8% annualized for the S&P GSCI, 0.97 correlation with total return) (V8 p.34).

**Roll return (roll yield)** (V8 p.32, p.33)
$$
\text{Roll return} = \frac{F_{\text{near}} - F_{\text{far}}}{F_{\text{near}}} \times \text{Percentage of position rolled}
$$
^f-08-01-5

- $F_{\text{near}}$: closing price of the expiring contract being sold; $F_{\text{far}}$: closing price of the contract being bought; the divisor is the near price; the weight is the fraction of the position rolled that period (an index rolling over five days uses 20% per day) (V8 p.33).
- Positive in backwardation ($F_{\text{near}} > F_{\text{far}}$), negative in contango; it is an accounting attribution inside total return, not a return capturable on its own (V8 p.32).
- Sometimes quoted in monetary rather than percentage terms; curriculum example: $(52.64 - 53.00)/52.64 = -0.68\%$ gross, times $20\%$ rolled that day $= -0.13\%$ net (V8 p.33, Python confirms $-0.6839\%$ and $-0.1368\%$).

> [!tip] Calculator
> WTI daily roll: `52.64 - 53 = / 52.64 = x 0.2 =` displays -0.00137, i.e. -0.137%.

**Collateral return (collateral yield)** (V8 p.33)
$$
\text{Collateral return} = \text{Annualized rate} \times \frac{\text{Holding period in months}}{12}
$$
^f-08-01-6

- Rate: yield on the cash or bonds posted against the position; full collateralization means collateral equals the notional value of the futures, so there is no leverage (V8 p.33).
- Indexes use short-term US T-bills; for an n-year forecast the matching constant maturity government bond is the right rate (V8 p.33).
- The period scaling is the exam trap: an annual 0.60% earned for three months contributes 0.15%.

**Total return of a fully collateralized futures position** (V8 p.34)
$$
\text{Total return} = \text{Price return} + \text{Roll return} + \text{Collateral return}
$$
^f-08-01-7

- All three components must be stated over the same holding period before adding; at index level a rebalance return is added as a fourth component (V8 p.34).
- S&P GSCI 1970-2019 decomposition: $6.8\% = 3.0\% + (-1.3\%) + 5.0\%$ annualized (V8 p.34).

> [!tip] Calculator
> Natural gas problem: `2.99 - 2.93 = / 2.93 = STO 1` (0.0205), `2.99 - 3.03 = / 2.99 = STO 2` (-0.0134), `0.03 x 0.25 = + RCL 1 + RCL 2 =` gives 0.0146, i.e. 1.46%.

**Contracts needed to maintain constant dollar exposure on a roll** (V8 p.32)
$$
N = \frac{\text{Dollar exposure}}{F \times \text{Contract size}}
$$
^f-08-01-8

- $F$: futures price of the contract being entered; round to the nearest whole contract.
- In backwardation the far contract is cheaper, so $N$ rises (pound 110 exposure: $110/10 = 11$ near contracts become $110/9 = 12.2 \approx 12$); in contango it falls ($108/9 = 12$ become $108/10 = 10.8 \approx 11$) (V8 p.32, Python confirms 12.22 and 10.8).
- Same logic drives Example 19: a $10{,}000$ position at $4.00 is 2,500 contracts and at $2.50 is 4,000 contracts (V8 p.35).

**Total return swap reset payment** (V8 p.41)
$$
\text{Payment} = \text{Notional} \times \frac{\text{Index}_{t} - \text{Index}_{t-1}}{\text{Index}_{t-1}}
$$
^f-08-01-9

- Reset base is the previous valuation date's level, not the initiation level; a rise pays the swap buyer (long), net of the fee, and a fall obligates the buyer to pay the seller (V8 p.40, p.41).
- Total return = excess return (change in prices of the index's futures contracts) plus interest on the cash collateral; an excess return swap pays on the futures price change alone (V8 p.40).
- Curriculum check: CFCI up 1% on GBP 100 million pays the manager GBP 1 million; down 5% next day costs the manager GBP 5 million (V8 p.41).

**Variance and volatility swap payoff direction** (V8 p.41, p.42)
$$
\text{Variance swap payoff} \propto \sigma^2_{\text{realized}} - \sigma^2_{\text{fixed}}, \qquad \text{Volatility swap payoff} \propto \sigma_{\text{realized}} - \sigma_{\text{expected}}
$$
^f-08-01-10

- Positive difference pays the buyer, negative pays the seller; variance differences are often capped to limit upside and losses (V8 p.41).
- These are bets on how volatile prices are versus expectations, not on level or direction; a volatility seller profits when realized volatility comes in under expectations (V8 p.42).

## Worked examples

**Example 1: Commodity Sector Demand** (V8 p.8)
Industrial activity most likely affects the demand for which commodity: copper, natural gas, or softs?
A (copper) is correct: construction, infrastructure and durable goods manufacture are the economically sensitive uses.
B fails because natural gas demand is driven primarily by weather (heating and cooling) and only secondarily by industrial activity.
C fails because softs demand is driven primarily by global income. ^ex-08-01-1

**Example 2: Commodity Sector Risks** (V8 p.8)
Which sector is least affected in the short term by weather-related risks: energy, livestock, or precious metals?
C (precious metals) is correct: they store easily, so weather barely touches availability; inflation expectations, fund flows and industrial production matter more.
A fails because energy demand swings with winter heating and summer transportation.
B fails because extreme cold, wet and heat raise livestock death and disease risk. ^ex-08-01-2

**Example 3: Energy Life Cycle** (V8 p.10)
Primary production life cycle difference between crude oil and natural gas?
C is correct: natural gas needs very little processing after extraction, while crude is useless until refined.
A fails because both oil and natural gas are stored before use (summer gas is injected into storage for winter).
B fails because many countries store crude both commercially and strategically, not only European companies. ^ex-08-01-3

**Example 4: Industrial Metals Life Cycle** (V8 p.11)
Because of large economies of scale in processing, industrial metal producers:
C is correct: they find it difficult to cut production or capacity even when supply exceeds demand, because marginal cost falls with scale and utilization; overproduction persists until weaker competitors shut down.
A fails because time lags prevent immediate shutdowns.
B fails because running at maximum into falling demand creates financial losses, so it is not an incentive. ^ex-08-01-4

**Example 5: Livestock Life Cycle** (V8 p.12)
The US livestock sector has been among the least export oriented because of:
B is correct: high spoilage risk once animals are slaughtered, unless frozen.
A fails because cryogenics advances have actually improved export ability, so technology is not the constraint the question describes.
C fails because international demand for US livestock has grown, particularly from emerging markets. ^ex-08-01-5

**Example 6: Commodities versus Stocks and Bonds** (V8 p.15)
In contrast to financial assets:
C is correct: commodity investment is primarily via derivatives.
A fails because electricity and weather are commodity classes that are not physical goods you can touch or store.
B fails because commodities incur, rather than generate, periodic cash flows (storage and transport costs) when physically owned. ^ex-08-01-6

**Example 7: Spot Commodity Valuation** (V8 p.16)
Key valuation distinction versus stocks and bonds?
B is correct: commodity valuation focuses on supply and demand (a discounted forecast of future prices plus expected volatility), while stock and bond valuation focuses on discounted cash flows.
A fails because technical analysis is in fact sometimes applied to commodities.
C fails because it reverses the two frameworks. ^ex-08-01-7

**Example 8: Commodity Market Participants** (V8 p.19)
Traders that often provide insurance to hedgers are best described as:
B is correct: liquidity providers step in, at the right price, to absorb the price risk hedgers want to shed.
A fails because arbitrageurs profit from spot-futures mispricing using storage, not from insuring hedgers.
C fails because informed investors keep markets efficient by trading on information advantages. ^ex-08-01-8

**Example 9: Spot and Futures Pricing (1)** (V8 p.23)
Nearest WTI contract $65.00, six-month contract $60.75.
B is correct: near above far means backwardation.
A fails because contango requires the deferred price to exceed the nearby price.
C fails because the $65.00 - 60.75 = 4.25$ gap is not a shipping cost; delivery cost is only one component of a futures price, alongside geopolitical, seasonal and other factors (Python confirms the difference is 4.25). ^ex-08-01-9

**Example 10: Spot and Futures Pricing (2)** (V8 p.23)
Distinction between spot and futures prices:
C is correct: spot prices vary across regions with quality, composition and local supply and demand.
A fails because it is backwards: spot is local, futures are standardized.
B fails because futures contracts do assign premiums or discounts for quality and origin on delivery (arabica coffee adjusts for country of origin and warehouse location). ^ex-08-01-10

**Example 11: Spot and Futures Pricing (3)** (V8 p.24)
Lean hogs calendar spread quoted at -50 cents; natural gas calendar spread at +$1.10 per million BTU.
C is correct: a negative calendar spread (near below far) means contango for lean hogs, and a positive spread means backwardation for natural gas.
A fails because both individual contract prices and spreads trade, each with its own order book.
B fails because it assigns the states backwards. ^ex-08-01-11

**Example 12: Spot and Futures Pricing (4)** (V8 p.24)
A futures curve in backwardation:
B is correct: curves can fluctuate between contango and backwardation, sometimes rapidly under market stress or structural change.
A fails because no state persists indefinitely.
C fails because the curve reflects both long-term industry factors and dynamic expectations of supply and demand. ^ex-08-01-12

**Text demonstration: normal backwardation in cotton** (V8 p.26)
Pre-harvest curve: March 76.75, May 76.50, July 76.00 cents; post-harvest October 74.50, December 73.75 cents.
If the front price holds at 76.75, a speculator buys October at 74.50 and lets it become the front contract.
Convergence profit: $76.75 - 74.50 = 2.25$ cents per pound, and at 50,000 pounds per contract that is $0.0225 \times 50{,}000 = \$1{,}125$ per contract (Python confirms both).
This is Keynes's risk premium: payment to the speculator for insuring the farmer's sales price, and Kolb's data (29 contracts) showed it is not statistically reliable, "normal backwardation is not normal" (V8 p.26). ^ex-08-01-13

**Example 13: Theories of Commodity Futures Returns (1)** (V8 p.30)
Best description of insurance theory:
B is correct: producers accept a futures price below the expected/current spot in exchange for certainty (locking in revenue).
A fails because insurance theory requires the futures price below the spot (normal backwardation), not above.
C fails because the theory implies backwardation, not contango. ^ex-08-01-14

**Example 14: Theories of Commodity Futures Returns (2)** (V8 p.30)
Under hedging pressure, when buyers' hedging exceeds sellers':
B is correct: excess demand for price insurance from consumers bids the futures price up until speculators will take the other side, which is contango.
A fails because a flat curve needs balanced hedging on the two sides.
C fails because backwardation is the producer-dominated case. ^ex-08-01-15

**Example 15: Theories of Commodity Futures Returns (3)** (V8 p.31)
Under the theory of storage, the convenience yield is:
C is correct: high when supply is scarce, because inventory scarcity makes holding the physical good more valuable as a disruption buffer.
A fails because supply levels have a discernible effect on convenience yield.
B fails because scarcity raises, not lowers, the yield. ^ex-08-01-16

**Example 16: Theories of Commodity Futures Returns (4)** (V8 p.31)
Theory of storage formula:
A is correct: Futures price = Spot price + Direct storage costs - Convenience yield.
B fails by adding the convenience yield, which is a benefit of holding the physical good and therefore reduces the futures premium.
C fails by flipping both signs. ^ex-08-01-17

**Text demonstration: rolling in backwardation and in contango** (V8 p.32)
Wheat (backwardation): pound 110 exposure at pound 10 per near contract is $110/10 = 11$ contracts; the far contract is worth pound 9, so constant exposure needs $110/9 = 12.2 \approx 12$ contracts, one more than before (Python: 12.222).
Gasoline (contango): pound 108 at pound 9 is $108/9 = 12$ contracts; the far contract is pound 10, so $108/10 = 10.8 \approx 11$ contracts, one fewer (Python: 10.8).
Cheaper far contracts (backwardation) mean buying more; dearer far contracts (contango) mean buying fewer. ^ex-08-01-18

**Text demonstration: S&P GSCI five-day roll in WTI** (V8 p.33)
7 February 2019, March contract $52.64, April contract $53.00, rolling 20% per day.
Gross roll return: $(52.64 - 53.00)/52.64 = -0.68\%$ (Python: $-0.6839\%$).
Net roll return that day: $-0.6839\% \times 20\% = -0.14\%$, printed as $-0.13\%$ from the rounded $-0.68\%$ (Python: $-0.1368\%$).
Negative, as expected in contango; Ilmanen's claim that roll return approximates a risk premium is challenged because 40% of his commodities had negative roll but positive total returns (V8 p.33). ^ex-08-01-19

**Example 17: Total Returns for Futures Contracts (1)** (V8 p.34)
A market in backwardation will exhibit:
B is correct: rolling forward requires buying more contracts to keep the same dollar position, because the far contract is cheaper.
A fails because roll return is usually positive, not negative, in backwardation.
C fails because fewer contracts is the contango case. ^ex-08-01-20

**Example 18: Total Returns for Futures Contracts (2)** (V8 p.35)
Price return 5%, roll return 2.5%, one-year hold, collateral 100% at 2%.
C is correct: Total return $= 5\% + 2.5\% + 2\% = 9.5\%$ (Python confirms 9.5).
A (5.5%) ignores the price or roll component; B (7.3%) mixes the pieces; every component is already annual, so no scaling is needed. ^ex-08-01-21

**Example 19: Total Returns for Futures Contracts (3)** (V8 p.35)
$10,000 long position, near contract $4.00, far contract $2.50.
A is correct: sell $10{,}000/4.00 = 2{,}500$ near contracts and buy $10{,}000/2.50 = 4{,}000$ far contracts (Python confirms both).
B fails because a long roll sells the expiring contract and buys the far one, not the reverse.
C fails because rolling 2,500 into only 2,500 far contracts leaves exposure of $2{,}500 \times 2.50 = \$6{,}250$, well short of $10,000. ^ex-08-01-22

**Example 20: Roll Return** (V8 p.38)
Contribution of roll return to total return:
B is correct: important in any single period, relatively modest over multiple periods (S&P GSCI: -1.3% annualized against 6.8% total, but single-year swings of tens of percent).
A fails because the long-run contribution is modest.
C fails because roll returns are decidedly nonzero, positive or negative with the curve. ^ex-08-01-23

**Text demonstration: refiner's excess return swap, flow of funds** (V8 p.40)
At end-December an oil refiner goes long a swap paying the excess over $70 per barrel each month-end through September, paying a $25 premium, effectively a strip of call options.
Reference prices Jan through Sep: 70, 75, 71, 66, 65, 63, 66, 72, 78.
Monthly receipts above $70: 0, 5, 1, 0, 0, 0, 0, 2, 8, summing to $16 (Python confirms).
Net outcome: $16 - 25 = -\$9$, raising the refiner's effective cost about $1 per barrel over nine months, but the premium bought protection against a cash squeeze from a price spike and made costs predictable up front (V8 p.40). ^ex-08-01-24

**Text demonstration: pension plan total return swap on the CFCI** (V8 p.41)
A GBP 2 billion plan wants 5% commodity exposure, so GBP 100 million of the hypothetical China Futures Commodity Index via a five-year total return swap with a Swiss bank.
Day 1, index +1%: dealer owes the manager GBP $100\text{m} \times 1\% = 1$ million.
Day 2, index -5%: manager owes the dealer GBP 5 million (Python confirms both).
The dealer typically hedges its short index exposure with futures or physicals; the manager deliberately stays unhedged because the commodity risk-return exposure is the point. ^ex-08-01-25

**Example 21: Commodity Swaps (1)** (V8 p.42)
$100 million notional total return swap, monthly resets: Month 1 index +3%, Month 2 index -2%.
B is correct: the dealer pays the manager $100\text{m} \times 3\% = \$3$ million after Month 1, and the manager pays $100\text{m} \times 2\% = \$2$ million after Month 2 (Python confirms).
A fails because resets settle monthly, not at expiration.
C fails because it reverses the direction of both payments. ^ex-08-01-26

**Example 22: Commodity Swaps (2)** (V8 p.42)
In a volatility swap, payments are determined relative to observed versus reference:
C is correct: volatility for the commodity's price.
A fails because volatility swaps do not bet on price direction.
B fails because variance (volatility squared) is the payoff variable of a variance swap, a different contract. ^ex-08-01-27

**Example 23: Commodity Indexes (1)** (V8 p.47)
Versus an equally weighted index, a production value-weighted index (S&P GSCI) will be:
B is correct: more sensitive to energy, because energy's huge production value gives it a dominant weight (historically up to 80%).
A and C fail because production weighting concentrates, it does not dilute or equalize, the energy exposure. ^ex-08-01-28

**Example 24: Commodity Indexes (2)** (V8 p.47)
Which statement is NOT correct about commodity futures indexes?
B is the answer: investing across several futures exchanges does not deliver much diversification because global commodity exchanges are highly correlated.
A is a true statement: backwardation sectors typically add positive roll yield to index returns (though total return can still be negative if price return is).
C is a true statement: major index total returns have low correlation with equities and bonds. ^ex-08-01-29

## Item-set patterns

> [!warning] Trap: basis quoted where the calendar spread belongs
> The vignette gives spot, near futures and far futures for one commodity and asks for "the calendar spread" or "the basis" among the answer choices.
> Correct approach: basis = spot - near futures; calendar spread = near futures - far futures (V8 p.20, p.21).
> Distractors compute the other quantity or subtract in the wrong order; in the Brent problem the $3.92 basis and $0.05 calendar spread both appear as choices, and the $3.97 spot-minus-far difference is the third lure.

> [!warning] Trap: sign language for contango
> A quoted calendar spread of "-50 cents" looks like backwardation to candidates who anchor on "negative = down = backward."
> Correct approach: negative spread means near below far, which is contango; positive spread is backwardation (V8 p.24).
> The distractor is always the mirror-image assignment, and a second distractor claims only spreads (not individual contracts) can be traded.

> [!warning] Trap: collateral return left annualized
> A three-month holding period with an annualized collateral rate (0.60% or 3%) invites adding the full annual rate.
> Correct approach: multiply the annual rate by the fraction of the year (0.60% times 3/12 = 0.15%; 3% times 0.25 = 0.75%) before summing with price and roll returns computed over the same period (V8 p.59, p.60).
> The wrong choices are built from the unscaled rate or from dropping the roll return's sign.

> [!warning] Trap: roll return denominator
> Roll return divides by the near-term (expiring) contract price, not the far price, and is multiplied by the fraction of the position rolled.
> Correct approach: $(F_{near} - F_{far})/F_{near} \times \%$ rolled; with the whole position rolled the weight is 100% (V8 p.33).
> Distractors divide by the far price or ignore the partial-roll weighting an index applies (20% per day over five days for the S&P GSCI).

> [!warning] Trap: which theory fits the curve
> A curve in contango plus a fact like "convenience yield exceeds direct storage costs" or "producers hedge less than consumers."
> Correct approach: convenience yield above storage costs would force backwardation under the theory of storage, so a contango curve with that fact can only be hedging pressure from consumer-dominated hedging; balanced hedging gives a flat curve; insurance theory only ever predicts backwardation (V8 p.25, p.27, p.29, p.59).
> Distractors offer the theory of storage because the vignette mentioned storage, or insurance theory because producers appear in the story.

> [!warning] Trap: storable commodity, so storage theory
> When the vignette stresses that a commodity is regularly stored (coffee, grains) and its curve is in contango, the theory of storage is the answer; when it stresses just-in-time consumption and minimal storage (energy) with backwardation, storage theory again explains it via demand dominance.
> Correct approach: read whether the fact pattern is about inventories (storage theory) or about which side hedges more (hedging pressure) (V8 p.58, p.60).
> The distractor pairs the right curve shape with the wrong causal story.

> [!warning] Trap: total return swap payment direction and base
> A long total return swap with monthly resets and an index that rose then fell.
> Correct approach: each reset compares with the previous reset level, and a decline means the long pays the dealer (notional times the percentage change); the May-June decline of 2.2082% on $25 million means the long owes $552,042.23 (V8 p.59, Python confirms).
> Distractors have the long receiving on a decline, use the initiation level as the base, or net multiple months into one payment.

> [!warning] Trap: avoid all negative roll returns
> A committee member (or the C choice) argues positions with negative roll returns should be avoided.
> Correct approach: positions are judged on total return; negative roll can be more than offset by price and collateral returns, so a negative-roll position can outperform a positive-roll one (V8 p.60).
> The distractors assert roll and price returns are strongly negatively correlated (the actual correlation is about 3%) or blame backwardation for negative rolls (contango causes them).

> [!warning] Trap: index construction consequences
> Two indexes differ only in that one holds contracts typically in backwardation, or rebalances monthly instead of annually.
> Correct approach: backwardation-heavy contracts add positive roll return, improving performance; frequent rebalancing wins in mean-reverting markets and loses in trending markets, and production-value weights drift with prices so they rebalance more cheaply than fixed weights (V8 p.44, p.46, p.61).
> Distractors claim rebalancing frequency is irrelevant or reverse the trending/mean-reverting conclusion.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM01-Introduction-to-Commodities-and-Commodity-Derivatives-Practice-Problems]]

## Cross-links

- [[LM01-Pricing-and-Valuation-of-Forward-Commitments]]: supplies the cost-of-carry pricing of futures that this module's contango/backwardation and theory-of-storage equation (spot plus storage costs minus convenience yield) specialize to physical commodities; understanding carry there makes the roll return here a corollary rather than a new fact.
- [[LM02-Overview-of-Types-of-Real-Estate-Investment]]: the next real-asset class in this topic; contrasts usefully because real estate, unlike commodities, does generate periodic cash flows, so its valuation returns to discounted cash flow machinery.
- [[LM04-Hedge-Fund-Strategies]]: managed futures and global macro strategies trade these commodity futures and harvest (or suffer) the roll and collateral returns decomposed here; the index construction issues (weighting, roll methodology) reappear as benchmark and replication questions.

## Self-test

Vignette A for Q1 to Q5: An analyst reviews two markets on the same day.
WTI crude: spot $82.40, near futures $81.60, far futures $80.90 (per barrel, 1,000 barrels per contract).
Cocoa: spot $2,410, near futures $2,450, far futures $2,495 (per metric ton).
Her fund holds a fully collateralized long WTI position of $12,240,000 established three months ago at a futures price of $80.00; collateral earns 4% annualized.
Today she rolls the entire WTI position from the near into the far contract.
WTI inventories are near record lows and refiners run just-in-time; cocoa is warehoused for months after harvest.

> [!question] Q1
> The WTI basis and calendar spread, respectively, are closest to:
> A. $0.80 and $0.70.
> B. $0.70 and $0.80.
> C. $1.50 and $0.80.

> [!question] Q2
> The roll return on today's WTI roll is closest to:
> A. -0.858%.
> B. +0.858%.
> C. +0.865%.

> [!question] Q3
> The three-month total return on the WTI position is closest to:
> A. 2.14%.
> B. 3.86%.
> C. 6.86%.

> [!question] Q4
> To maintain constant dollar exposure after the roll, the number of WTI contracts held should:
> A. fall from 151 to 150.
> B. stay at 150.
> C. rise from 150 to 151.

> [!question] Q5
> The two curve shapes are jointly most consistent with:
> A. insurance theory for WTI and hedging pressure for cocoa.
> B. the theory of storage for both markets.
> C. hedging pressure for WTI and insurance theory for cocoa.

Vignette B for Q6 to Q10: A pension CIO enters a $40 million notional long total return swap on the BCOM with monthly resets.
Index levels: 210.00 at initiation, 214.20 at the first reset, 209.916 at the second reset.
She also compares the BCOM (production and liquidity weighted, 33% sector cap, 2% commodity floor, annual rebalance) with the S&P GSCI (production weighted, annual rebalance) and with a fixed-weight monthly-rebalanced index, noting BCOM's natural gas weight of about 9% versus about 3% in the GSCI and natural gas's roughly 19% annualized roll cost.
Her strategist believes commodity consumers will hedge much more aggressively than producers next year, and that realized volatility in crude will come in below the level implied in swap quotes.

> [!question] Q6
> Relative to an excess return swap on the same index, the total return swap differs by:
> A. paying only when the swap expires.
> B. adding the interest earned on cash collateral to the futures price change.
> C. paying on two related but imperfectly correlated reference prices.

> [!question] Q7
> At the second reset, the CIO will:
> A. pay $800,000.
> B. receive $800,000.
> C. pay $77,600.

> [!question] Q8
> Holding everything else constant, the natural gas positions imply that relative to the GSCI the BCOM must:
> A. earn a higher collateral return to offset roll drag.
> B. find more price and rebalance return to overcome a larger negative roll contribution.
> C. benefit from a positive roll contribution three times larger.

> [!question] Q9
> If the strategist's hedging forecast is right, futures curves should tend toward:
> A. backwardation, because producer selling dominates.
> B. contango, because consumer buying pressure lifts futures prices.
> C. flatness, because hedging needs offset.

> [!question] Q10
> The position that best monetizes the volatility view is:
> A. a long variance swap on crude.
> B. a short volatility swap on crude.
> C. a long volatility swap on crude.

> [!success]- Answer key
> Q1: A.
> Basis = spot - near = $82.40 - 81.60 = 0.80$; calendar spread = near - far = $81.60 - 80.90 = 0.70$ (Python confirms).
> B swaps the two definitions; C uses spot minus far (1.50) for the basis.
> Q2: B.
> Roll return = $(81.60 - 80.90)/81.60 \times 100\% = +0.858\%$ (Python: 0.8578%), positive because the market is in backwardation.
> A flips the sign (contango logic); C divides by the far price ($0.70/80.90 = 0.865\%$), the wrong denominator.
> Q3: B.
> Price return $(81.60 - 80.00)/80.00 = 2.00\%$; roll $+0.858\%$; collateral $4\% \times 3/12 = 1.00\%$; total $= 3.86\%$ (Python: 3.8578%).
> A subtracts the roll return; C uses the unscaled 4% collateral rate ($2.00 + 0.86 + 4.00 = 6.86$).
> Q4: C.
> Near contracts: $12{,}240{,}000/(81.60 \times 1{,}000) = 150$; far contracts: $12{,}240{,}000/(80.90 \times 1{,}000) = 151.3 \approx 151$ (Python confirms), so backwardation requires buying more contracts.
> A reverses the direction (contango logic); B ignores the price difference.
> Q5: B.
> WTI: minimal storage, scarce inventories, high convenience yield, so futures = spot + storage - convenience yield sits below spot (backwardation); cocoa: warehoused for months, storage costs push futures above spot (contango); one theory, the theory of storage, explains both.
> A and C invoke hedging-side stories the vignette gives no evidence for, and insurance theory can never explain cocoa's contango.
> Q6: B.
> A total return swap pays the excess return (futures price changes of the index) plus interest on the cash collateral; that collateral interest is the difference.
> A is wrong because both swaps reset periodically; C describes a basis swap.
> Q7: A.
> Second reset: $(209.916 - 214.20)/214.20 = -2.00\%$ (Python confirms), and on a $40 million notional the long pays $40\text{m} \times 2\% = \$800{,}000$.
> B has the direction wrong on a falling index; C wrongly measures the change from the initiation level ($(209.916 - 210)/210 = -0.04\%$, $16{,}000$, and even then mis-scales).
> Q8: B.
> Natural gas has a large negative roll (about 19% annualized), and BCOM holds three times the GSCI's weight, so BCOM needs other sources (price return, rebalance return) to overcome the larger roll drag; the curriculum states exactly this (V8 p.45).
> A is wrong because collateral return is the same T-bill yield for both; C is wrong because natural gas's roll contribution is negative.
> Q9: B.
> Consumer-dominated hedging pressure bids futures above spot to induce speculators to sell insurance, which is contango.
> A is the producer-dominated (backwardation) case; C requires balanced pressure.
> Q10: B.
> Expecting realized volatility below expectations, she should sell volatility: the volatility seller profits when realized volatility comes in under the expected level.
> A and C are long volatility or variance and lose if the forecast is right.

## Flashcards

#flashcards/cfa-l2/08-Alternative-Investments/lm01

Commodity definition::A physical good attributable to a natural resource, tradable and supplied without substantial differentiation by the general public (V8 p.4).
The six commodity sectors (BCOM segmentation)::Energy, grains, industrial (base) metals, livestock, precious metals, softs (V8 p.6).
Sector least affected by short-term weather::Precious metals, because they store easily; their drivers are inflation expectations, fund flows and monetary policy (V8 p.8).
Commodity whose demand is most tied to industrial activity::Copper, via construction, infrastructure and durable goods (V8 p.8).
Stock vs flow in commodity analysis::Stock is potential production or demand (arable land, field capacity, herd size); flow is utilization of that stock (yields, tanker traffic, piglets per sow) (V8 p.5).
Four tools of commodity fundamental analysis::Direct announcements, component (stock and flow) analysis, timing considerations, money flow (V8 p.5, p.6).
Why crude oil differs from natural gas in its life cycle::Natural gas is consumable almost immediately after extraction; crude must be refined (cracked) into products first (V8 p.9).
Sector with the most flexible life cycle::Metals, because ore and finished metal can be stored for months or years without spoilage (V8 p.11).
Why metal producers keep overproducing in downturns::Huge economies of scale make marginal cost fall with utilization, so cutting or halting production is costly until weaker competitors shut down (V8 p.11).
Livestock maturation ladder::Poultry in weeks, hogs in about six months, cattle in years (feeder cattle on pasture 1-2 years, then 6-12 months in a feed lot) (V8 p.12).
Why US livestock was historically least export oriented::High spoilage risk after slaughter, until cryogenic freezing enabled exports (V8 p.12).
Grain growth cycle steps::Planting, growth, pod/ear/head formation, harvest, with opposite timing across hemispheres (V8 p.13).
Two coffee varieties and their futures venues::Robusta trades in London, arabica in New York; they are not deliverable against each other (V8 p.14, p.22).
The valuation factor that prices stocks and bonds but not commodities::Expected future cash flows (V8 p.14).
How commodities are valued::As a discounted forecast of future possible prices driven by supply, demand and expected price volatility, not by cash flow estimates (V8 p.14).
Why spot-futures arbitrage is only a boundary in some commodities::Some participants cannot make or take physical delivery, so the spot-futures link is a range, not an equality (V8 p.15).
Aggregate net position of commodity futures markets::Zero; longs equal shorts, unlike stocks and bonds where the market is net long the outstanding securities (V8 p.17).
Five participant groups in commodity futures markets::Hedgers, traders and investors, exchanges/clearing houses, analysts, regulators (V8 p.17).
Three types in the commodity trading community::Informed investors, liquidity providers, arbitrageurs (V8 p.18).
Which trader type provides insurance to hedgers::Liquidity providers, buying when producers must sell and selling when consumers must buy, for an expected profit (V8 p.18).
What lets a fund act as a commodity arbitrageur::The ability to inventory physical commodities (warehouses, silos, feedlots) against futures mispricing (V8 p.18).
Is hedging synonymous with being short?::No; a food manufacturer hedges long (input costs) and a gold miner hedges short (output prices), and speculators take either side (V8 p.18).
US commodity futures regulator and its delegate::The CFTC, delegating direct monitoring to the National Futures Association, a self-regulatory body (V8 p.19).
Basis (commodities)::Spot price minus futures price (V8 p.20).
Backwardation definition::Spot above the futures price, or near-term futures above longer-term futures; positive calendar spread (V8 p.20, p.21).
Contango definition::Spot below the futures price, or near-term futures below longer-term futures; negative calendar spread (V8 p.20, p.21).
Calendar spread::Near-term futures price minus longer-term futures price of the same commodity (V8 p.21).
Which settlement type guarantees spot-futures convergence?::Physical delivery; cash-settled markets may not fully converge because of trading costs and other factors (V8 p.22).
Insurance theory (Keynes)::Producers sell forward at a discount to lock in revenue, so futures sit below expected spot, creating normal backwardation and a speculator risk premium (V8 p.25).
Kolb's verdict on normal backwardation::"Normal backwardation is not normal"; backwardation does not reliably generate positive returns across 29 contracts (V8 p.26).
Hedging pressure hypothesis::Whichever side (producers or consumers) hedges more pushes the futures price away from itself; producer dominance gives backwardation, consumer dominance gives contango, balance gives a flat curve (V8 p.26, p.27, p.28).
Why the hedging pressure hypothesis is hard to apply::The asymmetry in hedging pressure between buyers and sellers is very difficult to measure (V8 p.29).
Theory of storage equation::{{Futures price = Spot price + Direct storage costs - Convenience yield}} (V8 p.29).
Convenience yield::The benefit of holding available physical inventory as a buffer against supply disruption; low when stock is abundant, high when inventories are scarce (V8 p.29).
Three components of futures total return::Price return, roll return, collateral return; an index adds a rebalance return (V8 p.32, p.34).
Price return formula::(Current price - Previous price) / Previous price, using front-month futures prices (V8 p.32).
Roll return formula::(Near-term futures price - Farther-term futures price) / Near-term futures price, times the percentage of the position rolled (V8 p.33).
Roll return sign in backwardation and contango::Positive in backwardation, negative in contango, zero on a flat curve (V8 p.32, p.58).
Rolling in backwardation: more or fewer contracts?::More contracts, because the farther contract is cheaper and constant dollar exposure requires additional units (V8 p.32).
Collateral return::The yield on the cash or bonds posted against the position, scaled to the holding period; full collateralization equals the notional, so no leverage (V8 p.33).
S&P GSCI 1970-2019 return decomposition::Total 6.8% = spot 3.0% - roll 1.3% + collateral 5.0%, with 19.8% volatility almost entirely from the spot component (V8 p.34).
Which sectors show persistently negative mean roll returns?::Industrial metals, agriculture, livestock, precious metals and softs (all stored at length); only energy has had a statistical shot at positive roll (V8 p.37).
Is roll return independently capturable?::No; it is an accounting attribution within total return, and no portfolio of pure roll returns exists (V8 p.32).
Excess return swap::Payments driven by the change in prices of the index's futures contracts versus a benchmark level, times notional (V8 p.40).
Total return swap (commodities)::Pays the futures-based index return plus interest on cash collateral; a rise pays the buyer, a fall obligates the buyer, reset against the previous valuation date (V8 p.40, p.41).
Basis swap (commodities)::Periodic payments on the difference between two related but imperfectly correlated reference prices, such as liquid Brent versus illiquid heavy crude (V8 p.41).
Variance swap vs volatility swap (commodity volatility)::Variance swaps pay on realized minus fixed variance (often capped); volatility swaps pay on realized minus expected volatility (V8 p.41, p.42).
Who profits when realized volatility is below expectations?::The volatility seller in a volatility swap (V8 p.42).
Three roles of commodity indexes::Benchmark for commodity pricing, macroeconomic/forecasting indicator, basis for investment vehicles (V8 p.43).
Five differentiators of commodity index construction::Breadth of coverage, component weighting method, rolling methodology, rebalancing methodology and frequency, governance (V8 p.43, p.44).
S&P GSCI construction::24 commodities, world production value weighted (energy up to 80%), monthly roll into the nearby most liquid contract, annual rebalance (V8 p.44, p.45).
BCOM construction::23 commodities, production and liquidity weighted, selection based, 33% sector cap and 2% commodity floor, front-month roll, annual rebalance (V8 p.44, p.45).
DBLCI's unique feature::Roll methodology optimized over the next 12 months for maximum backwardation or minimum contango, an active roll decision (V8 p.46).
Which indexes rebalance monthly and what does that imply?::TR/CC CRB and RICI; monthly rebalancing wins in mean-reverting markets and underperforms in trending markets (V8 p.44, p.46).
Why do production-weighted indexes rebalance more cheaply?::Weights drift with prices, so post-rebalance weights stay near current portfolio weights, unlike fixed-weight schemes (V8 p.46).
Correlations among major commodity indexes and with traditional assets::Above 70% with each other, roughly 0% with stocks and bonds (V8 p.47).
A 6-month position: price return 4%, roll -1%, collateral 3% annualized; total?::4% - 1% + 3% x 6/12 = 4.5% (V8 p.34).

## Common mistakes

1. Computing the basis as near futures minus far futures; the basis is spot minus futures, and near minus far is the calendar spread (V8 p.20, p.21).
2. Reading a negative calendar spread as backwardation; negative spread means near below far, which is contango (V8 p.24).
3. Adding an annualized collateral rate to period returns without scaling by the holding period fraction (0.60% annual for three months is 0.15%) (V8 p.59).
4. Dividing the roll return by the farther-term price instead of the near-term price, or forgetting to weight by the fraction of the position rolled (V8 p.33).
5. Assuming backwardation guarantees positive total returns; Kolb showed normal backwardation is not normal, and 40% of Ilmanen's negative-roll commodities still had positive total returns (V8 p.26, p.33).
6. Matching a contango curve to the theory of storage when the vignette says convenience yield exceeds storage costs; that combination forces backwardation under storage theory, so contango must come from consumer-dominated hedging pressure (V8 p.59).
7. Having the long total return swap receive a payment when the index falls, or measuring resets from the initiation level instead of the previous reset (V8 p.59).
8. Concluding that positions or indexes with negative roll returns must be avoided or must underperform; total return, not roll return, is the criterion (V8 p.60).
9. Saying rolling in backwardation requires fewer contracts; the far contract is cheaper, so constant dollar exposure needs more contracts (V8 p.32, p.35).
10. Treating roll return as a harvestable stand-alone return or as a strong predictor of price return; it is an accounting attribution with about 3% correlation to price return (V8 p.32, p.36).
11. Confusing variance swaps with volatility swaps, or buying volatility when the view is that realized volatility will undershoot expectations (V8 p.41, p.42, p.61).
12. Claiming multi-exchange commodity index investing gives strong diversification; global commodity exchanges are highly correlated (V8 p.47).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "08-01" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
