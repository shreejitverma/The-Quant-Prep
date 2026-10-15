---
type: concept
track: [quant-trader, quant-research]
tier: advanced
status: draft
prereqs: [bonds-duration-and-convexity, money-markets-repo-and-overnight-rates]
est_hours: 4
sources: [CME Group - Treasury Futures Delivery Process and Conversion Factor Specifications, Tuckman and Serrat - Fixed Income Securities 4th ed. chapter 13, Burghardt and Belton - The Treasury Bond Basis 3rd ed., Federal Reserve Board - The Treasury Market in Spring 2020 and the Response of the Federal Reserve 2021]
---

# Treasury Futures and the Basis

> [!info] Draft
> Written in this session with computed examples matching `code/curve_bootstrap.py`.
> Missing for `solid`: formal independent reviewer check of all equations and parameter citations.

## TL;DR

- US Treasury futures (TU, FV, TY, US, WN) standardize interest rate risk across benchmark maturities through physical delivery of eligible Treasury securities.
- The CME conversion factor (CF) normalizes coupon and maturity differences by pricing each deliverable bond to yield a hypothetical $6.00\%$.
- The cheapest-to-deliver (CTD) bond minimizes net basis (or maximizes the Implied Repo Rate) and dictates futures price movements.
- Delivery options embedded in futures contracts (quality, timing, wild card) give the short position flexibility, causing futures to trade at a discount to theoretical forward prices.
- The cash-futures basis trade buys cash Treasuries, shorts futures, and finances the position in repo; in March 2020, extreme repo and liquidity dislocations caused severe basis blowouts.

## Learning objectives

- Identify CME Treasury futures contract specifications across the 2-year (TU), 5-year (FV), 10-year (TY), 30-year (US), and Ultra (WN) contracts.
- Calculate conversion factors using the CME formula and explain the mathematical rule determining which bond is cheapest to deliver.
- Compute gross basis, carry, net basis (basis net of carry), and the Implied Repo Rate (IRR).
- Describe the three delivery options: quality/switch option, timing option, and wild card option.
- Analyze the mechanics, leverage structure, and funding risk of the hedge fund basis trade during the March 2020 market dislocation.

## Core concepts

### Contract specifications and the delivery basket

CME Group lists standardized Treasury futures covering distinct sectors of the yield curve:
- 2-Year Treasury Note (TU): Deliverable maturity between $1$ year $9$ months and $2$ years.
- 5-Year Treasury Note (FV): Deliverable maturity between $4$ years $2$ months and $5$ years $3$ months.
- 10-Year Treasury Note (TY): Deliverable maturity between $6$ years $6$ months and $7$ years $11$ months (short 10y) or $9$ years $5$ months and $10$ years (standard 10y).
- Treasury Bond (US): Deliverable maturity between $15$ years and $25$ years.
- Ultra Treasury Bond (WN): Deliverable maturity of at least $25$ years.
A single futures contract does not reference one specific bond; instead, the short party may choose to deliver any Treasury issue satisfying the contract's maturity criteria.

### The conversion factor system

Because deliverable bonds have different coupon rates and maturities, the exchange applies a conversion factor (CF) to equalize pricing.
The conversion factor is the clean price per dollar of face value at which a deliverable bond would trade on the first day of the delivery month if it yielded exactly $6.00\%$ compounded semiannually.
For a bond with whole years to maturity $Y$ and annual coupon $c$, when delivery coincides with a coupon date:
$$\text{CF} = \frac{c / 2}{0.03} \left[ 1 - \frac{1}{(1.03)^{2Y}} \right] + \frac{1}{(1.03)^{2Y}}.$$
Properties of the conversion factor:
- If coupon $c = 6.00\%$, $\text{CF} = 1.0000$ exactly, regardless of maturity.
- If coupon $c < 6.00\%$, $\text{CF} < 1.0000$, and decreases as maturity increases.
- If coupon $c > 6.00\%$, $\text{CF} > 1.0000$, and increases as maturity increases.
When the short party delivers a bond, the invoice amount paid by the long party is:
$$\text{Invoice Price} = \text{Futures Settlement Price} \times \text{CF} + \text{Accrued Interest at Delivery}.$$

### Cheapest-to-deliver determination

The short party chooses which bond to deliver to maximize profit (or minimize delivery cost).
The gross basis measures the clean price difference between the cash bond and the converted futures price:
$$\text{Gross Basis} = P_{\text{spot}}^{\text{clean}} - F \times \text{CF}.$$
Holding the cash bond to delivery generates carry:
$$\text{Carry} = \text{Coupon Accrued to Delivery} - \text{Financing Cost} = AI_{\text{delivery}} - AI_{\text{spot}} - P_{\text{spot}}^{\text{dirty}} \cdot r_{\text{repo}} \cdot \frac{d}{360}.$$
The net basis (basis net of carry) subtracts carry from gross basis:
$$\text{Net Basis} = \text{Gross Basis} - \text{Carry} = P_{\text{spot}}^{\text{dirty}} - \left( F \times \text{CF} + AI_{\text{delivery}} \right) P_{\text{disc}}(0, T_{\text{del}}).$$
The cheapest-to-deliver (CTD) bond is the issue with the lowest net basis.
Alternatively, the CTD maximizes the Implied Repo Rate (IRR):
$$\text{IRR} = \frac{F \times \text{CF} + AI_{\text{delivery}} - P_{\text{spot}}^{\text{dirty}}}{P_{\text{spot}}^{\text{dirty}}} \times \frac{360}{d}.$$
General CTD selection rules based on the level of market yields:
1. When market yields exceed $6.00\%$, the conversion factor system under-adjusts long-maturity, low-coupon bonds, making the highest-duration bond in the basket CTD.
2. When market yields are below $6.00\%$, the system favors short-maturity, high-coupon bonds, making the shortest-duration bond in the basket CTD.

### Delivery options embedded in futures

Because the short position holds several strategic choices, the futures contract trades at a discount to the theoretical forward price of the CTD bond:
1. Quality option (switch option): The short party can switch delivery to a different bond if market yields move or if a specific issue becomes cheap in repo.
2. Timing option: The short party can choose to deliver on any business day during the delivery month, choosing whether to collect carry on the cash bond or deliver early.
3. Wild card option: CME futures trading halts at 2:00 p.m. Central Time, fixing the futures settlement price, but the short party has until 8:00 p.m. to submit a notice of intention to deliver.
If cash Treasury prices fall sharply after 2:00 p.m., the short party can buy depressed cash bonds and immediately deliver them at the locked-in 2:00 p.m. futures price.
The value of these options is reflected in the positive net basis of the CTD bond.

### The cash-futures basis trade and funding risk

The basis trade is an arbitrage strategy executed by hedge funds and relative value desks:
- Long the cash Treasury bond (CTD).
- Short the Treasury futures contract sized by the conversion factor: $N_{\text{fut}} = \frac{N_{\text{cash}}}{\text{CF}}$.
- Finance the cash bond in the bilateral or cleared repo market.
Because net basis represents the value of delivery options, the trade captures carry and basis convergence towards expiration.
Because gross margins are thin (a few basis points), hedge funds typically lever the trade $20\text{x}$ to $50\text{x}$ via overnight or short-term repo.
The critical vulnerability is funding liquidity risk: if overnight repo rates spike, haircuts increase, or cash Treasury bid-ask spreads widen, the trader faces margin calls on both the cash bond and the futures contract, triggering forced liquidation.

### How it is implemented

- Inputs: deliverable bond prices, accrued interest, repo rates, futures price, CME conversion factors, delivery calendar.
- Outputs: gross basis, net basis, IRR per deliverable bond, CTD identification, hedge ratios.
- Algorithm: compute CF using CME analytical formula; evaluate invoice price for each deliverable; calculate IRR; sort bonds descending by IRR.
- Complexity: $O(M)$ where $M$ is the number of bonds in the deliverable basket (typically 15 to 30 bonds).
- Reference implementation: [`code/curve_bootstrap.py`](code/curve_bootstrap.py) provides `cme_conversion_factor` and `treasury_futures_basis`.
- System context: intraday risk and pre-trade limits (planned section 18) (planned section).

## Worked examples

All calculations below match the verified assertions in `code/curve_bootstrap.py`.

### Example 1: conversion factor calculation

Calculate the CME conversion factor for two 10-year Treasury notes:
Bond A: $4.00\%$ coupon, 10 years to maturity ($Y = 10$).
Bond B: $6.00\%$ coupon, 10 years to maturity ($Y = 10$).

For Bond B ($c = 6.00\%$):
$$\text{CF}_B = \frac{0.06 / 2}{0.03} \left[ 1 - \frac{1}{(1.03)^{20}} \right] + \frac{1}{(1.03)^{20}} = 1.0 \times [1 - (1.03)^{-20}] + (1.03)^{-20} = 1.000000.$$

For Bond A ($c = 4.00\%$):
$$\text{CF}_A = \frac{0.04 / 2}{0.03} \left[ 1 - \frac{1}{(1.03)^{20}} \right] + \frac{1}{(1.03)^{20}}.$$
$(1.03)^{-20} = \frac{1}{1.806111} = 0.553676$.
$$\text{CF}_A = \frac{0.02}{0.03} [1 - 0.553676] + 0.553676 = \frac{2}{3} [0.446324] + 0.553676 = 0.297549 + 0.553676 = 0.851225.$$
Because Bond A has a coupon below the $6\%$ benchmark, its conversion factor is $0.851225 < 1.0$.

### Example 2: gross basis, invoice price, and implied repo rate

Current 10-year Treasury futures price: $F = 110.00$.
Delivery takes place in $d = 90\text{ days}$.
Evaluate Bond A ($4\%$ coupon, $\text{CF} = 0.851225$):
Clean spot price: $P_{\text{spot}}^{\text{clean}} = 94.00$.
Spot accrued interest: $AI_{\text{spot}} = 0.50 \implies P_{\text{spot}}^{\text{dirty}} = 94.50$.
Accrued interest at delivery: $AI_{\text{delivery}} = 1.50$.

Gross basis:
$$\text{Gross Basis} = P_{\text{spot}}^{\text{clean}} - F \cdot \text{CF} = 94.00 - 110.00 \times 0.851225 = 94.00 - 93.6348 = 0.3652.$$

Invoice price:
$$\text{Invoice Price} = F \cdot \text{CF} + AI_{\text{delivery}} = 110.00 \times 0.851225 + 1.50 = 93.6348 + 1.50 = 95.1348.$$

Implied Repo Rate (IRR):
$$\text{IRR} = \frac{\text{Invoice Price} - P_{\text{spot}}^{\text{dirty}}}{P_{\text{spot}}^{\text{dirty}}} \times \frac{360}{d} = \frac{95.1348 - 94.5000}{94.5000} \times \frac{360}{90} = \frac{0.6348}{94.5000} \times 4 = 0.02687 = 2.687\%.$$

If the prevailing actual financing rate for Bond A in general collateral repo is $r_{\text{repo}} = 2.25\%$, the trader can borrow cash at $2.25\%$ to buy Bond A and lock in a sale at an effective return of $2.687\%$, earning an annualized arbitrage spread of $2.687\% - 2.250\% = 43.7\text{ bps}$.

### Example 3: identifying the cheapest-to-deliver bond

Compare Bond A against Bond C ($6\%$ coupon, $\text{CF} = 1.0000$):
Clean spot price: $P_{\text{spot}}^{\text{clean}} = 111.00$, dirty spot $111.50$.
Accrued interest at delivery: $1.50$.
Invoice price for Bond C:
$$\text{Invoice Price}_C = 110.00 \times 1.0000 + 1.50 = 111.50.$$
Gross basis for Bond C:
$$\text{Gross Basis}_C = 111.00 - 110.00 = 1.0000.$$
Implied Repo Rate for Bond C:
$$\text{IRR}_C = \frac{111.50 - 111.50}{111.50} \times \frac{360}{90} = 0.000\%.$$
Comparing the two issues:
Bond A offers an IRR of $2.687\%$, whereas Bond C offers an IRR of $0.000\%$.
Because Bond A has the higher IRR (and lower gross basis), Bond A is significantly cheaper to deliver than Bond C.

### Example 4: real-world case, the March 2020 Treasury basis blowout

In early March 2020, extreme economic uncertainty surrounding the spread of COVID-19 triggered a massive flight to safety across global asset markets.
Large macro asset managers rapidly reallocated billions of dollars out of equities and into Treasury futures, pushing futures prices to substantial premiums relative to cash Treasuries.
Relative-value hedge funds aggressively scaled up their cash-futures basis positions, purchasing cheap cash Treasuries and shorting expensive futures contracts, funding their positions with up to $40\text{x}$ to $60\text{x}$ leverage via the bilateral repo market (source: Federal Reserve Board, "The Treasury Market in Spring 2020 and the Response of the Federal Reserve", FEDS Notes, June 2021).
However, as prime broker dealers faced their own balance sheet limits under the Supplementary Leverage Ratio (SLR), repo haircuts expanded and overnight liquidity dried up.
Simultaneously, bid-ask spreads on off-the-run Treasuries exploded from fractions of a basis point to over $10\text{ to }20\text{ basis points}$.
Unable to finance their cash bond inventory, hedge funds were hit with cascading margin calls and forced into fire-sales of cash Treasuries, causing cash yields to spike even as equity markets crashed.
The basis trade unwound violently until the Federal Reserve intervened on March 15, 2020, committing to purchase over $\$1.6\text{ trillion}$ in Treasuries and offering unlimited repo liquidity.

## Pitfalls

- Using clean prices instead of dirty prices in the Implied Repo Rate calculation, miscalculating financing costs.
- Assuming the CTD bond is fixed: yield shifts can cause the CTD to switch abruptly to a different issue in the basket.
- Neglecting the delivery options embedded in futures contracts, leading to overestimation of theoretical futures values.
- Miscalculating hedge ratios: hedging a cash bond with futures requires scaling notional by the conversion factor: $N_{\text{fut}} = \frac{N_{\text{cash}}}{\text{CF}}$.
- Assuming repo funding is permanent: funding cash bonds with overnight repo creates catastrophic rollover and liquidity risk during market stress.

## Interview questions

> [!question]- fi-cme-conversion-factor-concept | What is the purpose of the CME conversion factor in Treasury futures?
> The conversion factor normalizes pricing across different bonds in the deliverable basket by pricing each bond to yield a hypothetical $6.00\%$.
> It ensures that the invoice amount reflects the coupon and maturity differences of the specific bond delivered.

> [!question]- fi-cf-coupon-rule | If a bond's coupon is 4.00%, will its conversion factor be greater than, equal to, or less than 1.0? Explain why.
> Less than 1.0.
> A 4.00% coupon bond priced to yield 6.00% trades at a discount to par, resulting in a conversion factor below 1.0.

> [!question]- fi-implied-repo-rate-def | Define the Implied Repo Rate (IRR) of a deliverable Treasury bond.
> The annualized rate of return earned by buying the cash bond today, shorting the futures contract, and delivering the bond at maturity.
> $\text{IRR} = \frac{\text{Invoice Price} - P_{\text{spot}}^{\text{dirty}}}{P_{\text{spot}}^{\text{dirty}}} \times \frac{360}{\text{days}}$.

> [!question]- fi-ctd-selection-yield-rule | If prevailing Treasury yields are 3.00% (well below 6.00%), which bonds in the basket tend to be cheapest to deliver?
> Short-maturity, high-coupon bonds.
> When yields are below 6%, the conversion factor system overprices long-duration issues, making the shortest-duration bond the cheapest to deliver.

> [!question]- fi-gross-basis-vs-net-basis | What is the difference between gross basis and net basis?
> Gross basis is the clean cash price minus converted futures price: $P_{\text{spot}}^{\text{clean}} - F \cdot \text{CF}$.
> Net basis subtracts the carry (coupon earned minus repo financing cost) to delivery: $\text{Net Basis} = \text{Gross Basis} - \text{Carry}$.

> [!question]- fi-futures-wild-card-option | Explain the wild card delivery option embedded in Treasury futures.
> CME futures settlement prices lock at 2:00 p.m. Central Time, but the short party has until 8:00 p.m. to issue a delivery notice.
> If cash bond prices plunge between 2:00 p.m. and 8:00 p.m., the short can purchase cheap cash bonds and deliver them at the higher 2:00 p.m. price.

> [!question]- fi-basis-trade-leverage-hazard | Why do cash-futures basis trades rely on high leverage and what makes this risky?
> The basis spread between cash and futures is only a few basis points, requiring 20x to 50x leverage to achieve attractive returns.
> If repo funding rates spike or haircuts increase, the desk faces margin calls on both cash and futures, risking forced liquidation.

> [!question]- fi-futures-hedge-ratio-cf | If you hold $\$10\text{M}$ of a cash bond with $\text{CF} = 0.85$, how many futures contracts (face value $\$100{,}000$) do you short to hedge?
> Notional required: $\frac{\$10{,}000{,}000}{0.85} = \$11{,}764{,}706$.
> Short $\frac{\$11{,}764{,}706}{\$100{,}000} \approx 118$ contracts.

> [!question]- fi-march-2020-basis-dislocation | What caused the Treasury basis trade to blow out in March 2020?
> Heavy asset manager buying pushed futures to large premiums, but repo market dislocations and bank balance sheet constraints prevented arbitrageurs from financing cash bonds.
> Hedge funds faced margin spirals and fire-sold cash Treasuries, driving cash prices down and futures up.

> [!question]- fi-ctd-switch-risk | What is switch risk for a trader running a cash-futures basis trade?
> The risk that yield curve shifts or repo rate moves cause the CTD bond to switch to a different issue in the basket.
> The trader's cash bond is no longer tracking the futures contract, resulting in sudden basis widening losses.

## Further reading

- CME Group, *Treasury Futures Delivery Process and Conversion Factor Specifications*.
- Tuckman and Serrat, *Fixed Income Securities*, chapter 13.
- Burghardt and Belton, *The Treasury Bond Basis: An In-Depth Guide to the US Treasury Markets*, 3rd ed.
- Federal Reserve Board, *The Treasury Market in Spring 2020 and the Response of the Federal Reserve*, FEDS Notes, 2021.

## In this repo and SDE-Interview-Prep

- Code: [`code/curve_bootstrap.py`](code/curve_bootstrap.py) (`cme_conversion_factor`, `treasury_futures_basis`).
- Related notes: [Bonds, Duration and Convexity](02-Bonds-Duration-and-Convexity.md), [Curve Risk and Hedging](15-Curve-Risk-and-Hedging.md), [Money Markets, Repo and Overnight Rates](12-Money-Markets-Repo-and-Overnight-Rates.md).
