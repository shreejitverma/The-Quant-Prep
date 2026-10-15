---
type: cfa-lm
topic: "Economics"
topic_code: "02"
topic_slug: "02-Economics"
volume: 2
lm: 1
title: "Currency Exchange Rates: Understanding Equilibrium Value"
pages: "3-79"
weight_band: "5-10%"
difficulty: 4
los_count: 13
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/economics]
---

# LM1: Currency Exchange Rates: Understanding Equilibrium Value

Difficulty 4 of 5: the calculations (bid-offer cross rates, triangular arbitrage, forward points, mark-to-market) are mechanical but unforgiving about which side of the quote you use, and the second half piles on qualitative model taxonomy (parity relations, BOP channels, Mundell-Fleming, portfolio balance, crisis signs) that the exam tests with precisely swapped statements.

## LOS map

- **calculate** and interpret the bid-offer spread on a spot or forward currency quotation and describe the factors that affect the bid-offer spread (V2 p.3) ^los-02-01-a
    - Examiner asks: given a two-sided quote, state which side a client deals at for a given trade, or rank three transactions' spreads by currency pair liquidity, time of day, size, and dealer-client relationship.
- **identify** a triangular arbitrage opportunity and calculate its profit, given the bid-offer quotations for three currencies (V2 p.3) ^los-02-01-b
    - Examiner asks: build the implied cross-rate bid-offer from two interbank pairs (inverting one and swapping bid and offer), compare it with a dealer's cross quote, and compute the profit per unit from buying at the cheap source and selling at the dear one.
- **explain** spot and forward rates and calculate the forward premium/ discount for a given currency (V2 p.3) ^los-02-01-c
    - Examiner asks: compute F minus S from a spot rate and two MRRs with Actual/360 scaling, or convert quoted forward points by dividing by 10,000 and adding them to the correct side of the spot quote.
- **calculate** the mark-to-market value of a forward contract (V2 p.3) ^los-02-01-d
    - Examiner asks: offset the original forward with an equal-and-opposite position at the correct bid or offer all-in rate, take the rate difference times contract size, and discount at the MRR of the cash-flow currency.
- **explain** international parity conditions (covered and uncovered interest rate parity, forward rate parity, purchasing power parity, and the international Fisher effect) (V2 p.3) ^los-02-01-e
    - Examiner asks: identify covered interest rate parity as the only arbitrage-enforced condition, compute an expected spot rate from UIRP or ex ante PPP, and match each parity to its assumption (risk neutrality, law of one price, real rate equality).
- **describe** relations among the international parity conditions (V2 p.3) ^los-02-01-f
    - Examiner asks: which two conditions combine into forward rate parity (covered plus uncovered interest rate parity), and which two produce the international Fisher effect (ex ante PPP plus uncovered parity, equivalently real interest rate parity).
- **evaluate** the use of the current spot rate, the forward rate, purchasing power parity, and uncovered interest parity to forecast future spot exchange rates (V2 p.3) ^los-02-01-g
    - Examiner asks: match each forecasting method to its hidden assumption, e.g. today's spot assumes a random walk, the forward rate assumes risk-neutral investors and unbiasedness, PPP assumes a long-horizon anchor.
- **explain** approaches to assessing the long-run fair value of an exchange rate (V2 p.3) ^los-02-01-h
    - Examiner asks: why PPP works at long horizons but not short ones (Exhibit 2 evidence), and how debt accumulation and risk premiums shift the market's estimate of long-run equilibrium value.
- **describe** the carry trade and its relation to uncovered interest rate parity and calculate the profit from a carry trade (V2 p.3) ^los-02-01-i
    - Examiner asks: compute the all-in return through cross rates (convert, earn the high yield, convert back, subtract funding), and characterize the return distribution as peaked with fat tails and negative skew.
- **explain** how flows in the balance of payment accounts affect currency exchange rates (V2 p.3) ^los-02-01-j
    - Examiner asks: name the channel described in the vignette (flow supply/demand, portfolio balance, or debt sustainability) and predict the currency effect of persistent surpluses, deficits, or capital-inflow surges.
- **explain** the potential effects of monetary and fiscal policy on exchange rates (V2 p.3) ^los-02-01-k
    - Examiner asks: read the capital-mobility assumption first, then pick the correct Mundell-Fleming policy-mix cell (appreciate, depreciate, indeterminate), or distinguish the monetary approach, Dornbusch overshooting, and the portfolio balance long-run fiscal result.
- **describe** objectives of central bank or government intervention and capital controls and describe the effectiveness of intervention and capital controls (V2 p.3) ^los-02-01-l
    - Examiner asks: why emerging market intervention is more effective than developed market intervention (reserves large relative to daily FX turnover), and what intervention and controls are meant to achieve.
- **describe** warning signs of a currency crisis (V2 p.3) ^los-02-01-m
    - Examiner asks: pick the statement that is not a warning sign, most often "foreign exchange reserves are rising" (they fall before a crisis) or "the currency is below its historical mean" (it is typically above it).

## Core intuition

Start from what an exchange rate is: the price of the base currency expressed in units of the price currency, so USD/EUR 1.1650 means one euro costs 1.1650 dollars (V2 p.4, p.5).
Every quoted price in this market is two-sided, and both sides are the dealer's prices for the base currency: the bid is what the dealer pays to buy one unit of the base, the offer is what the dealer charges to sell one unit of the base (V2 p.5).
The client who requested the quote therefore always transacts at the side that is worse for the client: sell the base currency by hitting the bid, buy the base currency by paying the offer (V2 p.5, p.6).
The spread is the dealer's compensation for standing ready to trade, and the dealer expects to lay the position off in the interbank market inside the tighter interbank spread, pocketing roughly a pip per unit (V2 p.6).

> [!abstract] Idea 1: the quote is always about the base currency, and you always get the bad side
> Bid and offer refer to the currency in the denominator of the quote (V2 p.9).
> Every calculation in this module - cross rates, forward points, mark-to-market - reduces to two questions: am I buying or selling the base currency, and therefore do I use the bid or the offer (V2 p.9, p.16, p.18)?
> When a quote must be inverted to line up a cross rate, the inverse of the offer becomes the new bid and the inverse of the bid becomes the new offer, because buying one currency of a pair is selling the other (V2 p.10).

Spreads are not constant.
The client's spread is built on the interbank spread, which depends on the currency pair (majors tight, obscure crosses wide), the time of day (tightest in the London-New York overlap, roughly 8:00 a.m. to 11:00 a.m. New York time), and market volatility (spreads widen when uncertainty rises) (V2 p.6, p.7).
On top of that sit the transaction size (larger deals are harder to offset, so they price further from the current rate; retail sizes also price wide) and the dealer-client relationship (competition for a client's broader business tightens quotes; poor credit widens them, though credit matters little for T+2 settlement) (V2 p.7, p.8).
For forward quotes a fourth factor appears: the longer the term, the wider the spread, because liquidity falls while counterparty credit exposure and interest rate risk grow (V2 p.18).

Two arbitrage constraints discipline all spot quotes (V2 p.8).
First, a dealer's bid cannot sit above the interbank offer, and a dealer's offer cannot sit below the interbank bid, or the market buys cheap from one and sells dear to the other (V2 p.8).
Second, the same constraint applies to a dealer's cross-rate quote against the cross rate implied by two interbank pairs; a violation is a triangular arbitrage, so called because the money travels through three currencies and comes home larger (V2 p.8, p.9).
The mechanics never change: compute the implied cross bid by multiplying the two aligned bids, the implied cross offer by multiplying the two aligned offers, inverting one pair first if its base currency is on the wrong side (V2 p.9, p.10).

The forward market is the same machinery pushed through time.
A forward is any FX transaction settling later than T+2, and its price is forced by covered interest rate parity: investing at home must equal converting at spot, investing abroad, and converting back at the forward rate, because both round trips are riskless (V2 p.13, p.14).
This is the single parity condition enforced by actual arbitrage, which is why it holds essentially always while every other parity condition is a statement about expectations (V2 p.22, p.23).
Dealers quote forwards as points, the scaled difference between forward and spot; divide by 10,000 (100 for yen quotes) and add to the spot rate, keeping bid with bid and offer with offer (V2 p.15, p.16).
A forward position acquires mark-to-market value the moment rates move: close it with an equal-and-opposite forward to the same date, net the price-currency cash flows at settlement, and discount that single cash flow at the MRR of its own currency (V2 p.17, p.18).

> [!abstract] Idea 2: covered interest rate parity is arbitrage; everything else is an expectation that can fail
> CIP links S, F, and the two interest rates by a riskless round trip, so the currency with the higher interest rate always trades at a forward discount that exactly offsets its yield advantage (V2 p.14).
> UIRP replaces the forward contract with an unhedged expectation: the high-yield currency should depreciate by the yield spread, but nothing forces this, because no riskless trade locks it in (V2 p.23, p.24, p.26).
> If CIP and UIRP both hold, the forward rate equals the expected future spot rate (forward rate parity), which is why using forward points as a forecast silently assumes risk-neutral investors (V2 p.25, p.26, p.27).

The parity family then closes on itself.
The law of one price extended to national price levels gives absolute PPP, S equal to the ratio of price levels, which fails because not everything is tradable (V2 p.29).
Holding trade frictions constant gives relative PPP, exchange rate changes offsetting inflation differentials, and pushing it into the future gives ex ante PPP, expected depreciation of the high-expected-inflation currency (V2 p.30).
Layer on the Fisher effect (nominal rate = real rate + expected inflation) in each country: if UIRP and ex ante PPP both hold, real rates are equal across markets (real interest rate parity), and the nominal yield spread equals the expected inflation differential, which the curriculum calls the international Fisher effect (V2 p.32, p.33).
If every condition held at once, the expected change in the spot rate would simultaneously equal the forward premium, the nominal yield spread, and the expected inflation differential, and no one could earn consistent currency profits (V2 p.35, p.36).
Empirically the parities are long-run anchors, not short-run forecasts: the one-year PPP scatter is a cloud, but at five-year horizons and beyond the relationship becomes strongly positive, and PPP even works short-run when inflation differentials are enormous, as with Brazil in the 1980s (V2 p.31, p.32).

The carry trade is the monetization of UIRP's failure.
Because high-yield currencies have historically not depreciated by the full yield spread (and often strengthened), going long high-yield and short low-yield funding currencies has earned positive average returns (V2 p.24, p.25, p.37).
The reward accrues gradually as the interest differential; the risk arrives suddenly as an adverse exchange rate move, and when volatility spikes, crowded, leveraged carry positions unwind at once, stop-losses fire, and the flight to quality turns a smooth income stream into a crash (V2 p.38).
That is why carry returns are peaked with fat tails and negative skew relative to a normal distribution: many small gains, occasional large losses (V2 p.39).

Beyond the parities, the balance of payments and policy determine the path.
A current account deficit must be financed by a capital account surplus, and while persistent deficits weaken a currency over the long run, investment and financing flows dominate in the short run because asset prices adjust instantly while trade in goods adjusts with long lags (V2 p.40, p.41).
Current account effects travel through three channels: flow supply/demand (surplus countries see currency demand rise, though weak pass-through of exchange rates into traded-goods prices and sluggish demand responses mean the required adjustment can be large and slow), portfolio balance (surplus countries accumulate the deficit country's assets and may eventually rebalance away from them), and debt sustainability (markets revise the long-run equilibrium value down as a deficit country's external debt to GDP ratio climbs) (V2 p.41, p.42, p.43).
Surging capital inflows into emerging markets plant crisis seeds: currency overvaluation, external debt buildup, asset bubbles, credit booms, and overinvestment (V2 p.44).

> [!abstract] Idea 3: read the capital-mobility switch before answering any policy question
> Under high capital mobility (developed markets), Mundell-Fleming works through capital flows: restrictive monetary plus expansionary fiscal policy raises real rates and the currency appreciates; expansionary monetary plus restrictive fiscal policy lowers real rates and the currency depreciates; same-direction combinations are indeterminate (V2 p.49).
> Under low capital mobility (emerging markets with controls), the model works through the trade balance: twin expansion worsens the trade balance and the currency depreciates; twin restriction improves it and the currency appreciates; mixed combinations are indeterminate (V2 p.50).
> The two tables are mirror images along the diagonal, and the exam's favorite trick is quoting one table's cell under the other table's mobility assumption (V2 p.49, p.50).

The remaining models fill in what Mundell-Fleming ignores.
Monetary models fix output and let money move prices: a money supply increase raises the price level and, via PPP, depreciates the currency proportionally; Dornbusch adds sticky short-run prices, so the same easing first drops interest rates, triggers capital outflow, and pushes the exchange rate below its long-run PPP path before it recovers - overshooting (V2 p.50, p.51).
The portfolio balance approach supplies the long-run fiscal story: a growing bond supply from sustained deficits is held only for extra expected return, via higher rates, a higher risk premium, or currency depreciation, so fiscal expansion that appreciates a currency in the short run (Mundell-Fleming) tends to depreciate it in the long run as debt mounts and markets anticipate monetization or forced consolidation (V2 p.53, p.54).
Germany 1990-1992 is the canonical policy-mix case: expansionary unification fiscal policy plus a fiercely restrictive Bundesbank drove rates and the currency up (V2 p.50).

Finally, the public sector acts directly.
Capital inflows are pulled by better domestic management (lower inflation, flexible regimes, better fiscal positions, liberalization) and pushed by conditions abroad (low industrial-country rates, secular EM allocation trends) (V2 p.56, p.57).
Intervention and capital controls aim to prevent excessive appreciation, cap the volume of inflows, and preserve monetary independence; the IMF now accepts that controls can be justified (V2 p.57, p.58).
Effectiveness hinges on firepower: developed market reserves are negligible next to daily turnover in their currencies, so their intervention has limited effect, while emerging market central banks hold reserves that are sizable relative to turnover and can lean on the level and path of their exchange rates (V2 p.58).
When defenses fail, crises follow a recognizable prodrome: liberalized capital markets, heavy foreign-currency short-term inflows, a banking crisis, a fixed or partially fixed regime, plunging FX reserves, a currency well above its historical mean, deteriorating terms of trade, rapid money growth and a rising M2-to-reserves ratio, and elevated inflation (V2 p.59, p.60).
Iceland 2008 ticked nearly every box: bank assets at fourteen times GDP funded by short-term foreign deposits, a 40% currency appreciation, a consumption boom, then collapse, a 60%-plus depreciation, 18% interest rates, and capital controls (V2 p.60, p.61).

## Formulas and derivations

**Cross-rate bid-offer rule** (V2 p.9, p.10)
$$
\left(\frac{A}{C}\right)_{\!bid} = \left(\frac{A}{B}\right)_{\!bid}\times\left(\frac{B}{C}\right)_{\!bid},
\qquad
\left(\frac{A}{C}\right)_{\!offer} = \left(\frac{A}{B}\right)_{\!offer}\times\left(\frac{B}{C}\right)_{\!offer}
$$
^f-02-01-1

- A/B means "price of B in units of A"; the intermediate currency must cancel, so align the pairs before multiplying.
- If a needed pair is quoted the wrong way up, invert it and swap the sides: $(B/A)_{bid} = 1/(A/B)_{offer}$ and $(B/A)_{offer} = 1/(A/B)_{bid}$, because buying the base of one quote is selling the base of the inverse quote (V2 p.10).
- Why it holds: buying C with A through B means selling A for B and B for C; each leg happens at the side unfavorable to you, so the worst-case product is the implied offer, and no-arbitrage forces a dealer's posted cross bid (offer) below (above) the implied interbank offer (bid) (V2 p.8, p.9).

> [!tip] Calculator
> Implied JPY/EUR offer from JPY/USD 105.41 and USD/EUR 1.1651: `105.41 x 1.1651 =` gives 122.81; for an inverse leg first do `1.3201 1/x =` (0.75752) then multiply.

**Covered interest rate parity (exact forward rate)** (V2 p.14)
$$
F_{f/d} = S_{f/d}\,\frac{1 + i_f\left[\tfrac{Actual}{360}\right]}{1 + i_d\left[\tfrac{Actual}{360}\right]}
$$
^f-02-01-2

- $S_{f/d}$, $F_{f/d}$: spot and forward price of the domestic (base) currency in foreign currency units; $i_f$, $i_d$: foreign and domestic MRRs, annualized, Actual/360 day count (GBP uses Actual/365) (V2 p.13, p.14).
- Derivation: $(1+i_d) = S_{f/d}(1+i_f)(1/F_{f/d})$ equates two riskless one-period investments, domestic deposit versus convert-at-spot, invest abroad, convert back at the locked forward; solve for F (V2 p.13, p.14).
- In price/base notation the identical formula reads $F_{P/B} = S_{P/B}\,(1+i_P\tau)/(1+i_B\tau)$: price-currency rate on top, base-currency rate on the bottom (V2 p.14).
- This is the only parity enforced by pure arbitrage, so it holds whenever capital flows freely and markets are unstressed (V2 p.22, p.23).

**Forward premium or discount (exact)** (V2 p.14)
$$
F_{f/d} - S_{f/d} = S_{f/d}\,\frac{\left[\tfrac{Actual}{360}\right]}{1 + i_d\left[\tfrac{Actual}{360}\right]}\,(i_f - i_d)
$$
^f-02-01-3

- Positive when $i_f > i_d$: the base (domestic) currency trades at a forward premium exactly when the other currency has the higher interest rate (V2 p.14).
- The premium is proportional to the spot rate and the rate differential and approximately proportional to time to maturity (V2 p.14).
- Derivation: subtract S from both sides of CIP and factor; the $1+i_d\tau$ denominator is the only difference from the naive $S(i_f-i_d)\tau$ (V2 p.14).

> [!tip] Calculator
> Example 2 numbers: `0.0041 - 0.0147 = x 0.9000 = x 0.75 = / 1.011025 =` gives -0.0071 (0.75 is 270/360, 1.011025 is 1 + 0.0147 x 0.75).

**Forward points conversion** (V2 p.15, p.16)
$$
F = S + \frac{\text{points}}{10{,}000} \qquad (\text{JPY quotes: divide by } 100)
$$
^f-02-01-4

- Points are the forward-spot difference scaled to the last decimal of the spot quote (a pip: 0.0001, or 0.01 for yen); they are already scaled to the contract maturity, never annualize them (V2 p.15, p.16).
- Keep sides aligned: forward bid = spot bid + bid points, forward offer = spot offer + offer points; with negative points the bid is the more negative number so the forward bid stays below the forward offer (V2 p.16).
- The all-in rate is this sum; longer terms carry proportionally larger point magnitudes (V2 p.16, p.17).

**Mark-to-market value of a forward position** (V2 p.17, p.18)
$$
V_t = \frac{(F_t - F_0)\times \text{contract size}}{1 + i\left[\tfrac{days}{360}\right]}
$$
^f-02-01-5

- $F_0$: original all-in forward rate; $F_t$: all-in rate today on the offsetting forward to the same settlement date; size in units of the base currency; $i$: the MRR of the currency the cash flow is denominated in, for the remaining days (V2 p.17, p.18).
- Four steps: (1) create the equal-and-opposite forward position, (2) price it on the correct side (selling the base uses the bid, buying the base uses the offer, for spot and points alike), (3) net the settlement cash flow, (4) discount at the cash-flow currency's MRR (V2 p.18).
- Sign logic: a long base-currency forward gains when the base subsequently appreciates ($F_t > F_0$); a short position gains when it depreciates (V2 p.17, p.19).
- At initiation $F_t = F_0$, so a new forward has zero value; value accrues as spot and the two interest rates move (V2 p.17).

**Return on an unhedged foreign money market investment** (V2 p.23)
$$
R_{dc} = (1 + i_f)\,(1 - \%\Delta S_{f/d}) - 1 \;\cong\; i_f - \%\Delta S_{f/d}
$$
^f-02-01-6

- $\%\Delta S_{f/d}$ enters with a minus sign because a rise in $S_{f/d}$ (more foreign units per domestic unit) means the foreign currency fell, cutting the domestic-currency return (V2 p.23).
- The approximation drops the cross-product $i_f\times\%\Delta S$, which is second-order small (V2 p.24).

**Uncovered interest rate parity** (V2 p.24)
$$
\%\Delta S^{e}_{f/d} = i_f - i_d
$$
^f-02-01-7

- The expected change in the spot rate equals the nominal yield spread: a 6% foreign yield advantage embeds an expected 6% domestic-currency appreciation (equivalently, depreciation of the high-yield foreign currency) (V2 p.24).
- Holds only if enough risk-neutral investors force expected returns to equalize; no arbitrage enforces it, and short- to medium-run evidence rejects it, with high-yield currencies often strengthening (V2 p.24, p.25).
- Note the approximation cannot hold for $S_{f/d}$ and $S_{d/f}$ simultaneously since percentage changes of reciprocals differ (V2 p.24).

**Forward premium as a percentage and forward rate parity** (V2 p.25, p.26)
$$
\frac{F_{f/d} - S_{f/d}}{S_{f/d}} \cong i_f - i_d = \%\Delta S^{e}_{f/d}
\quad\Longrightarrow\quad
F_{f/d} = S^{e}_{f/d}
$$
^f-02-01-8

- The first equality is CIP with the $1+i_d$ denominator approximated to 1; the second is UIRP; together they make the forward an unbiased (not perfect) predictor of the future spot rate, which is forward rate parity (V2 p.25, p.26).
- Since CIP is guaranteed by arbitrage, forward rate parity stands or falls with UIRP alone (V2 p.26).

**Law of one price and absolute PPP** (V2 p.29)
$$
P^{x}_{f} = S_{f/d}\times P^{x}_{d}
\qquad\Longrightarrow\qquad
S_{f/d} = \frac{P_f}{P_d}
$$
^f-02-01-9

- Identical goods must cost the same in a common currency; aggregating over all goods makes the equilibrium exchange rate the ratio of national price levels (V2 p.29).
- Fails in practice because transaction costs exist, many goods are non-tradable, and index weights differ across countries (V2 p.29).

**Relative PPP** (V2 p.30)
$$
\%\Delta S_{f/d} \cong \pi_f - \pi_d
$$
^f-02-01-10

- Actual exchange rate changes offset actual inflation differentials, preserving competitiveness; the high-inflation country's currency depreciates (V2 p.30).
- Derivation: if $X = Y/Z$ then $\%\Delta X \approx \%\Delta Y - \%\Delta Z$ because the cross-product is small; apply to $S = P_f/P_d$ (V2 p.30).

**Ex ante PPP** (V2 p.30)
$$
\%\Delta S^{e}_{f/d} = \pi^{e}_f - \pi^{e}_d
$$
^f-02-01-11

- Expected depreciation equals the expected inflation differential; countries expected to run persistently high inflation should expect depreciating currencies (V2 p.30).
- Empirically a long-horizon anchor: no relationship at one year, strong at five years and beyond, and visible even short-run when differentials are huge (Brazil 1980-1993) (V2 p.31, p.32).

**Fisher effect and the real yield spread** (V2 p.32, p.33)
$$
i = r + \pi^{e},
\qquad
(r_f - r_d) = (i_f - i_d) - (\pi^{e}_f - \pi^{e}_d)
$$
^f-02-01-12

- Each nominal rate decomposes into a real rate plus expected inflation; subtracting the domestic from the foreign equation splits the nominal spread into a real spread plus an expected inflation differential (V2 p.32, p.33).
- Risk caveat: risky currencies carry a premium, so naive Fisher arithmetic overstates their real rates; economists add a currency risk premium as a third component (V2 p.33, p.34).

**Real interest rate parity and the international Fisher effect** (V2 p.33)
$$
r_f = r_d
\qquad\Longrightarrow\qquad
i_f - i_d = \pi^{e}_f - \pi^{e}_d
$$
^f-02-01-13

- If UIRP ($\%\Delta S^e = i_f - i_d$) and ex ante PPP ($\%\Delta S^e = \pi^e_f - \pi^e_d$) both hold, the two right sides are equal, so real rates converge across markets (real interest rate parity) and the nominal spread is purely an expected inflation spread (the international Fisher effect) (V2 p.33).
- The curriculum reserves "international Fisher effect" for this nominal-spread-equals-inflation-spread statement; some authors misuse it for UIRP (V2 p.33).
- Both require currency risk to be equal worldwide; an indebted emerging market violates that via its risk premium (V2 p.33, p.34).

**Carry trade return** (V2 p.38, p.40)
$$
R_{carry} \cong (i_{high} - i_{fund}) + \%\Delta S_{\text{investment currency}}
\qquad
R_{exact} = \frac{1}{S_0}\,(1 + i_{high})\,S_1 - 1 - i_{fund}
$$
^f-02-01-14

- $S_0$, $S_1$: spot prices of the investment currency in funding-currency units at entry and exit (build them as cross rates if quoted through USD); the additive form ignores the FX effect on the interest differential (V2 p.38, p.40).
- The trade earns the yield spread if the high-yield currency does not depreciate by the UIRP-implied amount; it loses when the investment currency falls by more than the spread (V2 p.38).
- Return distribution: more peaked than normal, fat tails, negative skew, because unwinds, stop-losses, leverage, and flight to quality bunch the losses (V2 p.38, p.39).

> [!tip] Calculator
> Example 7 Q4: `105.40 x 0.6810 = STO 1` (71.78), `104.60 x 0.6850 =` (71.65), `/ RCL 1 = x 1.017 = - 1 =` gives 0.0152, then `- 0.001 =` gives 0.0142.

**Monetary approach and Dornbusch overshooting (qualitative)** (V2 p.50, p.51)
$$
\%\Delta M \Rightarrow \%\Delta P \Rightarrow \%\Delta S \quad (\text{via PPP});
\qquad
\text{sticky prices} \Rightarrow S \text{ overshoots its long-run PPP path}
$$
^f-02-01-15

- Pure monetary model: an X% money supply rise lifts prices X% and, through PPP, depreciates the currency proportionally; weak because PPP fails short-run (V2 p.50, p.51).
- Dornbusch: with short-run price stickiness, easing first cuts nominal rates, capital flees, and the currency falls below its new long-run equilibrium, then appreciates back to the PPP path as prices adjust (V2 p.51).

The Mundell-Fleming policy-mix results are the module's mandatory table (V2 p.49, p.50).

| Capital mobility | Monetary policy | Fiscal policy | Currency effect |
|---|---|---|---|
| High | Expansionary | Expansionary | Indeterminate |
| High | Expansionary | Restrictive | Depreciates |
| High | Restrictive | Expansionary | Appreciates |
| High | Restrictive | Restrictive | Indeterminate |
| Low | Expansionary | Expansionary | Depreciates |
| Low | Expansionary | Restrictive | Indeterminate |
| Low | Restrictive | Expansionary | Indeterminate |
| Low | Restrictive | Restrictive | Appreciates |

- High mobility transmits through interest-sensitive capital flows (real rates up means currency up); low mobility transmits through the trade balance (aggregate demand up means imports up means currency down) (V2 p.48, p.49, p.50).
- High mobility fits the G-10; low mobility fits emerging markets that restrict capital (V2 p.50).
- Portfolio balance overlay: the high-mobility "expansionary fiscal appreciates" cell is short-run only; sustained deficits raise debt, risk premiums, and monetization fears, turning the long-run effect to depreciation (V2 p.53, p.54).

## Worked examples

**Text demonstration: implied cross-rate bid-offer, JPY/EUR and GBP/EUR** (V2 p.9, p.10)
Interbank quotes: USD/EUR 1.1649/1.1651, JPY/USD 105.39/105.41, USD/GBP 1.2302/1.2304.
JPY/EUR needs no inversion because JPY/EUR = (JPY/USD)(USD/EUR) and USD cancels.
Offer (sell JPY, buy EUR, so buy the base of each quote at its offer): $105.41 \times 1.1651 = 122.813191 \approx 122.81$.
Bid (buy JPY, sell EUR): $105.39 \times 1.1649 = 122.768811 \approx 122.77$ (Python confirms both products).
GBP/EUR needs GBP/USD, but USD/GBP is quoted, so invert and swap sides: GBP/USD bid $= 1/1.2304 = 0.81274$, GBP/USD offer $= 1/1.2302 = 0.81288$ (five decimals kept to avoid truncation error).
GBP/EUR bid $= 0.81274 \times 1.1649 = 0.94676 \approx 0.9468$; offer $= 0.81288 \times 1.1651 = 0.94709 \approx 0.9471$ (Python: 0.946765 and 0.947082).
The implied bid sits below the implied offer, as no-arbitrage requires. ^ex-02-01-1

**Example 1: Bid-Offer Rates** (V2 p.11, p.12)
Interbank spot quotes: USD/EUR 1.1649/1.1651, JPY/USD 105.39/105.41, CAD/USD 1.3199/1.3201, SEK/USD 9.6300/9.6302.
Q1: SEK/EUR = (SEK/USD)(USD/EUR), USD cancels, no inversion.
Bid: $9.6300 \times 1.1649 = 11.2180$; offer: $9.6302 \times 1.1651 = 11.2201$ (Python: 11.217987 and 11.220146), answer C.
A takes the reciprocal pair; B divides instead of multiplying.
Q2: JPY/CAD = (JPY/USD)(USD/CAD), but CAD/USD is quoted, so invert and swap: USD/CAD bid $= 1/1.3201 = 0.75752$, offer $= 1/1.3199 = 0.75763$.
Bid: $105.39 \times 0.75752 = 79.84$; offer: $105.41 \times 0.75763 = 79.86$, answer C.
Python at full precision gives bid $105.39/1.3201 = 79.834861$ and offer $105.41/1.3199 = 79.862111$; the curriculum's 79.84 bid comes from rounding the inverse to five decimals first (79.835026 rounds up), while full precision rounds to 79.83; the 0.01-level answer C is unaffected, but carry five decimals exactly as the curriculum does to reproduce its digits.
Q3: a dealer quotes JPY/CAD 79.81/79.83 against the implied 79.84/79.86.
The dealer's offer (79.83) is below the interbank bid (79.84): CAD is being sold too cheaply.
Buy CAD from the dealer at 79.83, sell CAD in the interbank market at 79.84, profit JPY $79.84 - 79.83 = 0.01$ per CAD, answer C.
A reverses the direction (you cannot sell CAD to the dealer above the dealer's own bid), and B misstates the profit currency.
Q4: dealer quote 79.82/79.87 versus implied 79.84/79.86: the dealer bid (79.82) is not above the interbank offer (79.86) and the dealer offer (79.87) is not below the interbank bid (79.84), so no arbitrage exists, answer A.
Q5: spread ranking for buy CAD 100m vs USD at 15:30 London, sell CAD 100m vs KRW at 21:30 London, sell CAD 10m vs USD at 15:30 London.
Tightest is the small CAD/USD trade in the liquid London-New York overlap (Transaction 3), then the large CAD/USD trade at the same time (Transaction 1), then the large, illiquid-cross, after-hours KRW trade (Transaction 2), answer C. ^ex-02-01-2

**Example 2: Calculating the Forward Premium (Discount)** (V2 p.15)
Mid-market CAD/AUD spot 0.9000; 270-day MRR: AUD 1.47%, CAD 0.41%.
AUD is the base, so $i_B = 1.47\%$ and $i_P = 0.41\%$ in the P/B version of formula 3.
$F - S = 0.9000 \times \dfrac{270/360}{1 + 0.0147(270/360)} \times (0.0041 - 0.0147)$.
Step by step: $270/360 = 0.75$; $0.0147 \times 0.75 = 0.011025$; $0.9000 \times 0.75 = 0.675$; $0.675/1.011025 = 0.667639$; $0.0041 - 0.0147 = -0.0106$; $0.667639 \times (-0.0106) = -0.007077$.
So the discount is $-0.0071$ (Python: -0.0070770), answer B.
A ($-0.0094$) omits the denominator and misapplies the day count; C flips the sign by putting the AUD rate first.
The negative sign says the AUD (higher yield) trades at a forward discount against the CAD, exactly as CIP requires. ^ex-02-01-3

**Text demonstration: forward points and the AUD/GBP mark-to-market** (V2 p.16, p.17)
Exhibit 1 quotes USD/EUR spot 1.1649/1.1651 with 3-month points $-15.9/-15.3$.
Selling EUR (the base) three months forward uses the bid on both spot and points: $1.1649 + (-15.9/10{,}000) = 1.1649 - 0.00159 = 1.16331$ (Python confirms).
Mark-to-market walkthrough: a participant bought GBP 10m six months forward at all-in AUD/GBP 1.8100; three months later the quotes are spot 1.8210/1.8215, 3-month points 130/140, 3-month AUD MRR 2.40%.
Closing out means selling GBP 10m three months forward, so use the bid side: $1.8210 + 130/10{,}000 = 1.8210 + 0.0130 = 1.8340$.
Settlement cash flow: $(1.8340 - 1.8100) \times 10{,}000{,}000 = 0.0240 \times 10{,}000{,}000 = +\text{AUD } 240{,}000$, an inflow because the long GBP appreciated.
Present value: $240{,}000 / (1 + 0.024 \times 90/360) = 240{,}000/1.006 = \text{AUD } 238{,}569$ (Python: 238,568.59). ^ex-02-01-4

**Example 3: Forward Rates and the Mark-to-Market Value of Forward Positions** (V2 p.18, p.19, p.20)
CHF/GBP spot 1.2939/1.2941; points: 3-month $-25.4/-24.6$, 6-month $-56.5/-54.0$; USD/NZD spot 0.7825/0.7830 with 3-month points $-12.1/-10.0$, 3-month MRR NZD 3.31%, USD 0.31%.
Q1: all-in bid for delivering GBP in three months: $1.2939 + (-25.4/10{,}000) = 1.2939 - 0.00254 = 1.29136$ (Python confirms), answer A.
B averages the sides; C uses the offer points on the bid spot.
Q2: selling CHF six months forward is buying GBP (the base), so pay the offer on spot and points: $1.2941 + (-54.0/10{,}000) = 1.2941 - 0.0054 = 1.28870$ (Python confirms), answer C.
A and B use bid-side combinations that belong to a GBP seller.
Q3: Laurier Bay sold NZD 10m forward at all-in 0.7900 USD/NZD; to close, it buys NZD 10m three months forward, paying the offer on both: $0.7830 + (-10.0/10{,}000) = 0.7830 - 0.0010 = 0.7820$.
Settlement cash flow: receive $10{,}000{,}000 \times 0.7900 = \text{USD }7{,}900{,}000$, pay $10{,}000{,}000 \times 0.7820 = \text{USD }7{,}820{,}000$, net $+\text{USD }80{,}000$ (short NZD gained because NZD fell).
Discount at USD MRR (the cash flow is in USD): $80{,}000/(1 + 0.0031 \times 90/360) = 80{,}000/1.000775 = \text{USD }79{,}938$ (Python: 79,938.05), answer C.
A wrongly discounts an NZD-style loss; B discounts at the NZD rate ($80{,}000/1.008275 = 79{,}343$ is not even offered, so B's 77,437 embeds further errors; the tested distinction is currency-matched discounting).
Q4: now the fund sold USD 10m forward at 0.7900 and must buy USD, which means selling NZD (the base), so use the bid: $0.7825 + (-12.1/10{,}000) = 0.7825 - 0.00121 = 0.78129$.
Original contract delivers NZD $10{,}000{,}000/0.7900 = 12{,}658{,}228$; the offset pays NZD $10{,}000{,}000/0.78129 = 12{,}799{,}345$ (Python: 12,658,227.85 and 12,799,344.67).
Net: $12{,}658{,}228 - 12{,}799{,}345 = -\text{NZD }141{,}117$, an outflow because the USD (which the fund was short) appreciated.
Discount at NZD MRR: $-141{,}117/(1 + 0.0331 \times 90/360) = -141{,}117/1.008275 = -\text{NZD }139{,}959$ (Python: -139,958.67), answer B.
A forgets to discount; C converts the loss at the wrong rate. ^ex-02-01-5

**Example 4: Covered and Uncovered Interest Rate Parity: Predictors of Future Spot Rates** (V2 p.26, p.27, p.28)
JPY/AUD spot 71.78 (mid), one-year forward points $-139.4$, one-year deposit rates: AUD 3.00%, JPY 1.00%; the AUD is the manager's domestic currency.
Q1: UIRP expected change in JPY/AUD $= i_f - i_d = 1\% - 3\% = -2\%$, a 2% decrease (AUD depreciation), answer B.
A uses the sum of rates; C flips the sign.
Q2: the forecast is unreliable because no arbitrage forces UIRP, answer C; the $-139.4$ points are themselves the CIP arbitrage output (Python: $71.78 \times 1.01/1.03 - 71.78 = -1.394$, i.e. $-139.4$ points on a two-decimal JPY quote).
Q3: using forward points as the forecast assumes UIRP and forward rate parity, i.e. risk-neutral investors, answer A.
Q4: forecasting an unchanged spot (71.78) assumes a random walk, answer B; that contradicts UIRP unless the rate differential is zero.
Q5: a fully hedged JPY deposit must return the AUD rate, 3%, by covered interest parity, answer C, no computation needed.
Q6: JPY investor fully hedged into GBP MRR earns the JPY rate, 0.10%, answer A, again pure CIP.
Q7: if UIRP holds, expected spot equals the forward: $S^e = F = 129.67 \times \dfrac{1 + 0.001}{1 + 0.03} = 129.67 \times 0.971845 = 126.02$ (Python: 126.0191), answer A.
B is the random walk; C moves the rate the wrong way.
Q8: expected change in JPY/USD under UIRP $= i_{JPY} - i_{USD} = 0.10\% - 0.10\% = 0$, answer B. ^ex-02-01-6

**Example 5: PPP and the International Fisher Effect** (V2 p.34, p.35)
Australia one-year deposit 3%, Japan 1%; the AUD is judged 10% overvalued versus JPY on PPP.
Q1: with all else equal, a 10% decline in JPY/AUD restores PPP value, answer C; changing one country's inflation by 2% or 10% (A, B) alters the future path, not today's 10% gap.
Q2: with equal real rates, the international Fisher effect attributes the whole nominal spread to expected inflation: $3\% - 1\% = 2\%$, answer B.
Q3: the statement that would NOT be true under long-run PPP is that high-inflation countries see their currencies appreciate, answer C; PPP says they depreciate to restore purchasing power.
Q4: absolute PPP fails because trade barriers exist and consumption bundles differ across countries, answer C; inflation variation (A) is relative PPP's subject and real-rate convergence (B) is a different parity. ^ex-02-01-7

**Example 6: The Relationships among the International Parity Conditions** (V2 p.36, p.37)
Q1: the no-arbitrage condition is covered interest rate parity, answer B; real interest rate parity and UIRP are expectation conditions.
Q2: forward rate parity needs CIP and UIRP; the one NOT required is real interest rate parity, answer A.
Q3: the international Fisher effect rests on real interest rate parity and ex ante PPP; it does NOT require absolute PPP, answer B.
Q4: the forward premium/discount is set by covered interest parity (arbitrage), answer B, not by the Fisher effect or real rate parity.
Q5: if all parity conditions held, the expected spot change would equal the forward premium, the nominal yield spread, and the expected inflation differential, but NOT the real yield spread, which would be zero, answer A. ^ex-02-01-8

**Example 7: Carry Trade Strategies** (V2 p.39, p.40)
Q1: carry trades are profitable when uncovered interest rate parity fails, answer B; CIP failing would mean forward mispricing, not carry.
Q2: the return distribution has fat tails and negative skew, answer B; crash risk rules out thin tails or positive skew.
Q3: the volatility of returns relative to the equity base is explained by leverage (borrow the funding currency, invest the proceeds), answer A.
Q4: Tokyo manager borrows JPY at 0.10%, invests in one-year AUD MRR at 1.70%; JPY/USD 105.40 now, 104.60 in a year; USD/AUD 0.6810 now, 0.6850 in a year.
Cross rates: today JPY/AUD $= 105.40 \times 0.6810 = 71.7774 \approx 71.78$; one year later $104.60 \times 0.6850 = 71.6510 \approx 71.65$ (Python confirms both).
Gross unhedged AUD return in JPY: $(1/71.78) \times 1.017 \times 71.65 - 1 = 0.015158 \approx 1.52\%$; net of 0.10% funding: $1.52\% - 0.10\% = 1.42\%$.
Transactional check on JPY 100: buy AUD $100/71.78 = 1.3931$; grow to $1.3931 \times 1.017 = 1.4168$; convert to $1.4168 \times 71.65 = \text{JPY }101.51$; repay $100 \times 1.001 = 100.10$; profit JPY 1.41, i.e. 1.41 to 1.42% (Python: 1.5209% gross and 1.4209% net at full precision, 1.5158% gross with the rounded crosses).
The curriculum keys B (+1.53%) as "closest to" 1.42%, which is nearer to B than to C (+1.63%, the answer if you forget the funding cost); A (+0.03%) nets the two deposit rates against the unrelated JPY/USD move. ^ex-02-01-9

**Example 8: Capital Flows and Exchange Rates** (V2 p.46, p.47, p.48)
Strategist Kwan compares a low-yield safe haven DM currency with a high-yield EM currency.
Q1: the EM currency most likely depreciates if the expected inflation differential (EM minus DM) is revised upward, answer C, straight ex ante PPP; an upward-revised equilibrium value (A) or a wider yield spread (B) supports the currency.
Q2: an increase in safe haven demand raises the risk premium demanded for holding EM assets, answer A; it lowers carry returns and pressures the EM currency down, not up.
Q3: a persistent DM current account deficit against the EM raises DM external debt, and via the debt sustainability channel markets revise the DM currency's long-run value down, equivalently the EM currency's long-run value up, answer C; the asset buildup runs toward the EM country (not A), and the surplus (EM) country's competitiveness eventually erodes as its currency strengthens (not B).
Q4: with boom-like conditions, near-term capital inflows most likely appreciate the EM currency, answer C; inflation expectations are rising (not A) and the risk premium is falling (not B).
Q5: to fight unwanted real appreciation the government most likely imposes capital controls, answer A; cutting consumption taxes (B) fuels the boom and buying its own currency (C) appreciates it further, the exact opposite of the goal (selling its own currency is the intervention that resists appreciation).
Q6: when the bubble bursts, the reversal shows up as a jump in the EM risk premium, answer A; neither the spot value (B) nor the long-run equilibrium value (C) rises in a bust.
Q7: the claim that equity-FX correlation is "highly positive over time" is incorrect because the correlation is unstable and tends toward zero in the long run, answer C; since the global financial crisis the USD-equity correlation has actually been negative (safe haven behavior), so neither a stable positive nor a stable negative statement survives (V2 p.45, p.46). ^ex-02-01-10

**Example 9: Monetary Policy and Exchange Rates** (V2 p.52, p.53)
A DM country with high capital mobility, flexible rates, and low debt.
Q1: more monetary easing most likely depreciates the currency, answer B: lower rates push capital toward higher-yielding markets (Mundell-Fleming, high mobility).
Q2: expansionary fiscal policy in the short run most likely appreciates the currency, answer A: deficits push rates up and attract inflows; the long-run debt buildup caveat is exactly the portfolio balance reversal.
Q3: an EM pegging its currency while easing monetary policy must buy its own currency in the FX market to hold the peg, answer C; tightening fiscal policy (A) or cutting rates (B) adds to the downward pressure.
Q4: with capital controls replacing the peg, monetary tightening still moves the exchange rate, answer B (appreciation): controls mute capital flows, so policy transmits through aggregate demand and the trade balance, and tighter policy cuts imports, modestly supporting the currency.
Q5: tight monetary plus highly expansionary fiscal policy under low capital mobility is indeterminate, answer C: weak rate-driven inflows, an ambiguous net effect on aggregate demand, and offsetting trade-balance pressure. ^ex-02-01-11

**Example 10: Fiscal Policy and Exchange Rates** (V2 p.54, p.55, p.56)
A high-mobility, floating-rate DM country with low but rapidly rising government debt.
Q1: short-run expectation is currency appreciation, answer A (Mundell-Fleming: fiscal expansion, higher real rates, capital inflow); higher rates depress local asset prices (not B) and the rising debt raises, not lowers, the risk premium (not C).
Q2: over the medium term, as debt becomes harder to finance, the likely response is more accommodative monetary policy (debt monetization pressure), answer C; fiscal policy cannot easily ease further when financing is the problem (not A), and the mark-to-market value of the debt falls as required returns rise (not B).
Q3: with no monetary accommodation, the eventual fiscal consolidation issues fewer bonds, yields decline, and the currency depreciates over the longer term, answer B; appreciation alongside a financing crisis (A) contradicts the rising risk premium, and the direction is not indeterminate (C) because depreciation is part of restoring equilibrium under the portfolio balance approach. ^ex-02-01-12

**Example 11: Currency Crises** (V2 p.61, p.62, p.63)
Q1: the claim that most crises were not well anticipated by investors, bond markets, rating agencies, or economists is correct, answer A.
Q2: the conclusion that even countries with sound fundamentals can be attacked, via self-fulfilling sentiment shifts and contagion, is correct, answer A; this is the second school of thought.
Q3: the early warning system is LEAST likely to flash when FX reserves are rising, answer C; reserves fall precipitously before crises, while easy money (A) and an over-appreciated currency (B) are classic warning signs.
Q4: a better early warning system flashes well before the crisis so portfolios can be adjusted or hedged, answer C; tolerating false alarms (A) and using long-lagged data (B) are defects, not features (V2 p.59). ^ex-02-01-13

## Item-set patterns

> [!warning] Trap 1: which side of the quote
> The vignette hands you a bid-offer quote and a client trade ("convert JPY receivables to GBP", "buy USD to pay a supplier") and asks for the proceeds.
> Correct: identify the base currency, then buy the base at the offer or sell the base at the bid; converting JPY 225m into GBP at JPY/GBP 129.65/129.69 means buying GBP at 129.69 (V2 p.5, p.71, p.77).
> Distractors price the trade at the bid (1,735,442) or the midpoint (1,735,174); the three options typically bracket the answer so the wrong side looks plausible (V2 p.77).

> [!warning] Trap 2: cross rates without (or with botched) inversion
> Two interbank pairs share a common currency on the same side, and a cross-rate bid-offer is requested.
> Correct: invert the misaligned pair and swap its bid and offer (the inverse of the offer is the new bid), then multiply bid with bid and offer with offer (V2 p.9, p.10).
> Distractors multiply the raw quotes without inverting, invert without swapping sides, or pair a bid with an offer; the giveaway is an implied bid above the implied offer, which is impossible (V2 p.10).

> [!warning] Trap 3: declaring arbitrage that is not there
> A dealer cross quote is compared with the implied interbank cross, and the question asks for the profitable trade.
> Correct: arbitrage exists only if the dealer bid exceeds the interbank offer (sell to the dealer, buy interbank) or the dealer offer is below the interbank bid (buy from the dealer, sell interbank); a dealer quote that merely straddles or overlaps the implied quote is clean (V2 p.8, p.11, p.12).
> Distractors offer the reverse trade direction and a "no arbitrage" option; Example 1 Q4 (79.82/79.87 versus 79.84/79.86) shows an overlapping quote with no profit, the exact configuration the exam reuses (V2 p.12).

> [!warning] Trap 4: forward points mishandled
> A points table (some negative) accompanies a spot bid-offer, and an all-in rate is requested for a specific trade.
> Correct: divide points by 10,000 (100 for JPY quotes), add to the same side of the spot quote as the trade requires, and remember the quoted points are already maturity-scaled (V2 p.16).
> Distractors annualize the points, add offer points to the bid spot, or add unscaled points; with negative points, remember the bid is the more negative number (V2 p.16).

> [!warning] Trap 5: mark-to-market side, sign, and discount rate
> A months-old forward must be valued today given spot, points, and two MRRs.
> Correct: offset the original position (long base closes by selling the base at the bid; short base closes by buying at the offer), net the settlement cash flow in the price currency (or invert for base-currency flows), and discount at the MRR of the cash-flow currency for the remaining days (V2 p.18, p.19, p.20).
> Distractors skip the discounting, discount at the other currency's MRR, use the wrong quote side, or flip the gain into a loss; option sets usually include the undiscounted number and the wrong-currency PV (V2 p.20, p.78).

> [!warning] Trap 6: which parity is which
> Statements attribute properties (arbitrage-enforced, assumes risk neutrality, unbiased forecast, real-rate equality) to named parity conditions.
> Correct: CIP is the only arbitrage-enforced condition; UIRP assumes enough risk-neutral investors; CIP plus UIRP gives forward rate parity; UIRP plus ex ante PPP gives real interest rate parity and the international Fisher effect ($i_f - i_d = \pi^e_f - \pi^e_d$) (V2 p.22, p.24, p.26, p.33).
> Distractors call UIRP the international Fisher effect (the curriculum explicitly warns about this), require real rate parity for forward unbiasedness, or claim absolute PPP underlies the Fisher relations (V2 p.33, p.36, p.37).

> [!warning] Trap 7: carry trade profit and distribution
> A funding rate, an investment rate, and beginning and ending spot (often via crosses) are given.
> Correct: build the cross rates, compute $(1/S_0)(1+i_{high})S_1 - 1$, subtract the funding rate; describe returns as peaked, fat-tailed, negatively skewed (V2 p.39, p.40).
> Distractors report the gross return (funding cost forgotten), the raw yield spread (FX move forgotten), run the trade through the wrong currency leg, or describe a "normal distribution with fat tails" (a contradiction) or positive skew (V2 p.39, p.77).

> [!warning] Trap 8: the policy-mix cell under the wrong mobility
> A vignette states capital controls or free capital flows, then asks the currency effect of a monetary-fiscal combination.
> Correct: pick the table that matches mobility first; high mobility rewards high real rates (restrictive monetary + expansionary fiscal appreciates), low mobility rewards trade-balance improvement (restrictive both appreciates, expansionary both depreciates), and the remaining cells are indeterminate (V2 p.49, p.50).
> Distractors apply the high-mobility logic to a capital-controls country or treat "indeterminate" cells as determinate; Example 9 Q5 and practice Q17 both live in this trap (V2 p.53, p.75).

> [!warning] Trap 9: crisis warning signs reversed
> A list of "predictions" before a crisis mixes true and inverted warning signs.
> Correct: before crises, reserves FALL, the currency sits ABOVE its historical mean, money growth and M2/reserves RISE, inflation is HIGHER, terms of trade DETERIORATE, and fixed regimes are more vulnerable (V2 p.59, p.60).
> The standard wrong statement is rising reserves or an undervalued currency; Example 11 Q3 and practice Q20 both key on the reserves inversion (V2 p.62, p.76).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM01-Currency-Exchange-Rates-Understanding-Equilibrium-Value-Practice-Problems]]

## Cross-links

- [[LM02-Economic-Growth]]: growth theory supplies the long-run fundamentals behind this module's anchors; relative productivity trends and potential growth drive the real rates, expected inflation, and capital attractiveness that the parity conditions and capital-flow channels convert into currency paths.
- [[LM01-Pricing-and-Valuation-of-Forward-Commitments]]: the derivatives reading prices currency forwards with the identical covered interest rate parity carry argument and values seasoned forwards with the same offset-and-discount logic as this module's mark-to-market; recognizing the shared machinery halves the formula load.
- [[LM03-Multinational-Operations]]: FSA's translation of foreign subsidiaries consumes the spot rates modeled here; whether a currency's path follows PPP or overshoots determines the translation gains and losses and the choice-of-method effects tested there.
- [[LM01-Economics-and-Investment-Markets]]: the portfolio management reading generalizes this module's mechanics, linking policy, inflation expectations, and risk premiums to discount rates across all asset classes; the currency risk premium here is one instance of its framework.

## Self-test

Vignette A for Q1 to Q4: A dealer's desk observes interbank quotes USD/EUR 1.0780/1.0784 and JPY/USD 152.40/152.44.
Another dealer posts JPY/EUR 164.20/164.26.
Separately, the desk sees CAD/USD spot 1.3650 (mid) with 180-day MRRs of 4.50% (CAD) and 5.30% (USD).
Two months ago a client bought EUR 20 million six months forward against the USD at an all-in rate of 1.0900; today's USD/EUR spot is 1.0940/1.0944, the 120-day forward points are 20/24, and 120-day USD MRR is 5.10%.

> [!question] Q1
> The implied interbank JPY/EUR bid is closest to:
> A. 164.26.
> B. 164.29.
> C. 164.39.

> [!question] Q2
> Given the posted JPY/EUR quote of 164.20/164.26, the desk should:
> A. do nothing, because the quote does not violate the arbitrage constraints.
> B. sell EUR to the posting dealer at 164.20 and buy EUR in the interbank market.
> C. buy EUR from the posting dealer at 164.26 and sell EUR in the interbank market, for about JPY 0.03 per EUR.

> [!question] Q3
> The 180-day forward premium (discount) on CAD/USD is closest to:
> A. -0.0104.
> B. -0.0053.
> C. +0.0053.

> [!question] Q4
> The mark-to-market value of the client's long EUR forward is closest to:
> A. +USD 117,994.
> B. +USD 120,000.
> C. +USD 133,727.

Vignette B for Q5 to Q8: One-year MRRs are 5.00% (USD), 11.00% (MXN), and 0.30% (JPY).
Spot rates today are MXN/USD 17.20 and JPY/USD 152.00.
One year later the spots are MXN/USD 17.80 and JPY/USD 148.00.
A macro fund borrowed JPY one year ago to invest in one-year MXN deposits.

> [!question] Q5
> Under uncovered interest rate parity, the expected MXN/USD rate in one year (as of today) is closest to:
> A. 16.27.
> B. 17.20.
> C. 18.18.

> [!question] Q6
> For the forward rate to be an unbiased predictor of the future spot rate, which pair of conditions must hold?
> A. Covered interest rate parity and ex ante PPP
> B. Covered and uncovered interest rate parity
> C. Uncovered interest rate parity and real interest rate parity

> [!question] Q7
> The realized all-in one-year return on the fund's JPY-funded MXN carry trade, in JPY terms, is closest to:
> A. 4.14%.
> B. 4.44%.
> C. 10.70%.

> [!question] Q8
> Relative to a normal distribution, the long-run return profile of repeating this strategy is best described as:
> A. thin-tailed with positive skew.
> B. normal, but with higher variance due to leverage.
> C. more peaked, fat-tailed, and negatively skewed.

Vignette C for Q9 to Q10: An emerging market country with extensive capital controls (low capital mobility) simultaneously runs an expansionary fiscal policy and an expansionary monetary policy.
A developed market country with high capital mobility runs a restrictive monetary policy alongside an expansionary fiscal policy.
An analyst also screens EM currencies for crisis risk.

> [!question] Q9
> Under the Mundell-Fleming framework, the EM currency and the DM currency, respectively, are most likely to:
> A. depreciate; appreciate.
> B. appreciate; depreciate.
> C. be indeterminate; appreciate.

> [!question] Q10
> The screening indicator least consistent with an impending currency crisis is:
> A. the ratio of M2 to bank reserves rising.
> B. foreign exchange reserves rising sharply.
> C. the real exchange rate well above its historical mean.

> [!success]- Answer key
> Q1: B.
> JPY/EUR bid $= (\text{JPY/USD})_{bid} \times (\text{USD/EUR})_{bid} = 152.40 \times 1.0780 = 164.2872 \approx 164.29$ (Python: 164.2872); no inversion is needed since USD cancels; A is the posting dealer's offer, C is the implied interbank offer ($152.44 \times 1.0784 = 164.3913$).
> Q2: C.
> The posted offer 164.26 sits below the implied interbank bid 164.29, so EUR is for sale too cheaply: pay the dealer's offer 164.26, sell EUR interbank at 164.29, profit JPY $164.2872 - 164.26 = 0.0272 \approx 0.03$ per EUR (Python: 0.0272); B trades in the losing direction, and A misses that the constraint (dealer offer below interbank bid) is violated.
> Q3: B.
> $F - S = 1.3650 \times \dfrac{180/360}{1 + 0.053(180/360)} \times (0.045 - 0.053) = 1.3650 \times 0.48706 \times (-0.008) = -0.00532$ (Python: -0.005319); the USD (base) carries the higher rate, so it trades at a forward discount; A skips the 180/360 scaling (Python: -0.01037), C flips which rate is the base currency's.
> Q4: A.
> Close the long EUR by selling EUR at the bid on spot and points: $1.0940 + 20/10{,}000 = 1.0960$; cash flow $= (1.0960 - 1.0900) \times 20{,}000{,}000 = \text{USD }120{,}000$; discount 120 days at USD MRR: $120{,}000/(1 + 0.051 \times 120/360) = 120{,}000/1.017 = 117{,}994$ (Python: 117,994.10); B forgets the discounting, C uses the offer side ($1.0944 + 0.0024 = 1.0968$, giving 133,727), the side a EUR buyer would pay.
> Q5: C.
> Approximating UIRP with the exact ratio, $S^e = 17.20 \times 1.11/1.05 = 18.18$ (Python: 18.1829), i.e. the high-yield MXN is expected to depreciate by roughly the 6% spread; B is the random-walk answer, A inverts the ratio ($17.20 \times 1.05/1.11 = 16.27$), strengthening the wrong currency.
> Q6: B.
> Forward rate parity $F = S^e$ follows from CIP (F equals the rate-ratio-adjusted spot) plus UIRP (the expected spot change equals the rate differential) (V2 p.26); ex ante PPP and real interest rate parity are not required.
> Q7: A.
> Build the crosses: JPY/MXN today $= 152.00/17.20 = 8.8372$; one year later $= 148.00/17.80 = 8.3146$ (Python: 8.837209 and 8.314607); gross $= (1/8.8372) \times 1.11 \times 8.3146 - 1 = 4.44\%$; net of JPY funding at 0.30%: $4.44\% - 0.30\% = 4.14\%$ (Python: 4.4358% and 4.1358%); B forgets the funding cost, C is the raw yield spread $11.00\% - 0.30\% = 10.70\%$, ignoring the 5.9% MXN depreciation against JPY.
> Q8: C.
> Carry crash risk produces many small gains punctuated by occasional large losses: peaked center, fat tails, negative skew (V2 p.39); A describes the opposite, and B is a contradiction because the empirical distribution is not normal at any variance.
> Q9: A.
> Low mobility, twin expansion: demand and imports surge, the trade balance worsens, the EM currency depreciates; high mobility, restrictive monetary plus expansionary fiscal: real rates rise, capital floods in, the DM currency appreciates (V2 p.49, p.50); B reverses both cells and C wrongly treats the EM combination as a mixed (indeterminate) cell.
> Q10: B.
> Reserves fall precipitously before crises, so rising reserves argue against one (V2 p.60); A and C are documented warning signs (rising M2/reserves, currency substantially above its historical mean).

## Flashcards

#flashcards/cfa-l2/02-Economics/lm01

Bid price in a P/B quote::The price, in price-currency units, at which the counterparty will buy one unit of the base currency (V2 p.5).
Offer price in a P/B quote::The price at which the counterparty will sell one unit of the base currency; always above the bid (V2 p.5).
Hit the bid vs pay the offer::Selling the base currency hits the bid; buying the base currency pays the offer (V2 p.5, p.6).
A pip::The last standard decimal of the quote, 0.0001 for most pairs and 0.01 for yen quotes (V2 p.6).
Three drivers of the client's bid-offer spread::The interbank spread for the pair, the transaction size, and the dealer-client relationship (V2 p.6).
Three drivers of interbank liquidity::The currency pair, the time of day (London-New York overlap is most liquid), and market volatility (V2 p.7).
Extra factor widening forward spreads::Contract term: longer terms mean thinner liquidity, more counterparty credit risk, and more interest rate risk (V2 p.18).
First arbitrage constraint on dealer quotes::A dealer bid cannot exceed the interbank offer and a dealer offer cannot sit below the interbank bid (V2 p.8).
Rule of thumb for bids and offers::A bid or offer always refers to the currency in the denominator, the base currency (V2 p.9).
Implied cross-rate bid::{{Multiply the two aligned bid rates}} after inverting any misaligned pair (V2 p.9, p.10).
Inverting a bid-offer quote::The new bid is one over the old offer and the new offer is one over the old bid (V2 p.10).
When does triangular arbitrage exist?::When a dealer's cross bid exceeds the implied interbank offer, or the dealer's cross offer is below the implied interbank bid (V2 p.8, p.11).
Micro-problem: JPY/USD 105.39/105.41, CAD/USD 1.3199/1.3201; JPY/CAD bid?::Invert CAD/USD and swap sides, then 105.39 x (1/1.3201) = 79.84 as the curriculum rounds it; keystrokes 1.3201 1/x x 105.39 = (V2 p.11).
Spot settlement convention::T+2 for most pairs, T+1 for CAD/USD (V2 p.5).
Forward contract definition::Any FX transaction settling later than T+2 at a rate agreed today (V2 p.13).
Covered interest rate parity::{{F equals S times (1 + price-currency rate x tau) over (1 + base-currency rate x tau)}} with Actual/360 day counts (V2 p.14).
Which currency trades at a forward premium?::The base (domestic) currency, exactly when the other (price, foreign) currency has the higher interest rate (V2 p.14).
Forward points conversion::Divide the points by 10,000 (100 for yen quotes) and add to the correct side of the spot quote; points are already maturity-scaled (V2 p.16).
Micro-problem: spot CHF/GBP 1.2939/1.2941, 3-month points -25.4/-24.6; all-in bid?::1.2939 - 0.00254 = 1.29136; keystrokes 25.4 +/- / 10000 = + 1.2939 = (V2 p.19).
Mark-to-market of a forward in four steps::Offset with an equal-and-opposite forward, price it on the correct bid or offer side, net the settlement cash flow, discount at the MRR of the cash-flow currency (V2 p.18).
Which discount rate for a forward's MTM?::The MRR of the currency in which the net settlement cash flow is denominated, for the remaining days (V2 p.18).
Micro-problem: sold EUR 5m at 0.9526, offset at 0.9486, 90-day GBP MRR 0.58%; MTM?::5,000,000 x 0.0040 = GBP 20,000, then 20,000 / 1.00145 = GBP 19,971 (V2 p.79).
The only parity condition enforced by arbitrage::Covered interest rate parity (V2 p.22).
Uncovered interest rate parity::{{The expected percentage change in the spot rate equals the interest rate differential, foreign minus domestic}} (V2 p.24).
What UIRP predicts for high-yield currencies::They should depreciate by the yield spread; empirically they often fail to, which funds the carry trade (V2 p.24, p.25).
Forward rate parity::The forward rate is an unbiased predictor of the future spot rate; requires both CIP and UIRP (V2 p.25, p.26).
Assumption behind using the forward rate as a forecast::Enough risk-neutral investors that UIRP holds (V2 p.24, p.27).
Assumption behind using today's spot as the forecast::Exchange rates follow a random walk (V2 p.27).
Law of one price::Identical goods trade at the same common-currency price across countries (V2 p.29).
Absolute PPP::The equilibrium exchange rate equals the ratio of national price levels; fails because of trade frictions and non-tradables (V2 p.29).
Relative PPP::Percentage exchange rate changes equal the inflation differential, foreign minus domestic (V2 p.30).
Ex ante PPP::Expected exchange rate changes equal expected inflation differentials (V2 p.30).
At what horizon does PPP have power?::Little at one year, strong at five-plus years; also short-run when inflation differentials are enormous (V2 p.31, p.32).
Fisher effect::Nominal interest rate equals the real rate plus expected inflation (V2 p.32).
Real interest rate parity::Real rates converge across markets; follows if UIRP and ex ante PPP both hold (V2 p.33).
International Fisher effect::The nominal yield spread equals the expected inflation differential; requires real rate parity, not absolute PPP (V2 p.33).
Carry trade recipe::Borrow the low-yield funding currency, buy and invest in the high-yield currency, unwind at the future spot rate (V2 p.37, p.38).
Carry trade profit approximation::Yield spread plus the percentage change in the investment currency; exact form runs the round trip through the cross rates (V2 p.38, p.40).
Carry trade return distribution::More peaked than normal, fat tails, negative skew: frequent small gains, occasional crashes (V2 p.39).
Why do carry crashes happen?::Volatility spikes trigger simultaneous unwinds, stop-losses, deleveraging, and flight to quality, amplifying the adverse move (V2 p.38).
Three channels from current accounts to exchange rates::Flow supply/demand, portfolio balance, and debt sustainability (V2 p.41).
Why capital flows dominate short-run exchange rates::Asset prices and portfolios adjust instantly while goods prices, production, and trade demand adjust with long lags (V2 p.41).
Pass-through finding::A 1% currency decline raises import prices by only about 0.5%, so trade imbalances correct slowly (V2 p.42).
Five dangers of EM capital inflow surges::Currency overvaluation, external debt buildup, asset bubbles, credit or consumption booms, and overinvestment (V2 p.44).
Mundell-Fleming, high mobility, restrictive monetary + expansionary fiscal::Currency appreciates: higher real rates attract capital (V2 p.49).
Mundell-Fleming, high mobility, expansionary monetary + restrictive fiscal::Currency depreciates: lower real rates repel capital (V2 p.49).
Mundell-Fleming, low mobility, both policies expansionary::Currency depreciates through a worsening trade balance (V2 p.50).
Mundell-Fleming, low mobility, both policies restrictive::Currency appreciates through an improving trade balance (V2 p.50).
Which policy-mix cells are indeterminate?::Same-direction combinations under high mobility; mixed combinations under low mobility (V2 p.49, p.50).
Pure monetary approach::Money supply growth raises prices one-for-one and, via PPP, depreciates the currency proportionally (V2 p.50, p.51).
Dornbusch overshooting::With sticky short-run prices, monetary easing drops rates, capital flees, and the currency falls below its long-run PPP level before recovering (V2 p.51).
Portfolio balance approach in one line::Growing government bond supply is held only for higher expected return: higher yields, a higher risk premium, or currency depreciation (V2 p.53, p.54).
Integrated fiscal result::Expansionary fiscal policy under high mobility appreciates the currency short-run but depreciates it long-run as debt mounts (V2 p.54).
Germany 1990-1992 policy mix::Expansionary unification fiscal policy plus restrictive Bundesbank monetary policy drove rates and the currency up (V2 p.50).
Pull vs push factors for capital inflows::Pull: better domestic management (low inflation, flexible regimes, liberalization); push: external conditions such as low industrial-country rates (V2 p.56).
Three goals of intervention and capital controls::Prevent excessive currency appreciation, reduce the volume of inflows, and preserve independent monetary policy (V2 p.58).
Why EM intervention beats DM intervention::EM reserves are sizable relative to daily FX turnover in their currencies; DM reserves are negligible relative to turnover (V2 p.58).
Name three of the nine currency crisis warning signs::Any of: liberalized capital markets, large foreign-currency short-term inflows, banking crisis, fixed or partly fixed regime, plunging reserves, currency above its historical mean, deteriorating terms of trade, rising money growth and M2/reserves, elevated inflation (V2 p.60).
Which reserve behavior precedes crises?::Foreign exchange reserves decline precipitously; rising reserves are the classic non-sign distractor (V2 p.60).
Ideal early warning system traits::Predicts real crises without false alarms, uses timely data, and spans a broad set of indicators (V2 p.59).

## Common mistakes

1. Trading on the wrong side of the quote: clients buy the base at the offer and sell at the bid; midpoint and wrong-side proceeds are always among the answer options (V2 p.5, p.77, p.78).
2. Building a cross rate without inverting the misaligned pair, or inverting without swapping bid and offer; an implied bid above the implied offer means you did this (V2 p.10).
3. Declaring triangular arbitrage from any quote mismatch; the constraint is violated only when a bid stands above an offer across sources, so overlapping quotes (Example 1 Q4, practice Q8) yield zero profit (V2 p.12, p.78).
4. Mishandling forward points: forgetting to divide by 10,000 (100 for yen), annualizing maturity-scaled points, or attaching offer points to bid spot (V2 p.16).
5. Getting the premium/discount direction backward: positive $F_{f/d} - S_{f/d}$ means the base currency is at a premium, which requires the price (foreign) currency to carry the higher interest rate (V2 p.14, p.79).
6. Mark-to-market errors: skipping the discounting step, discounting at the wrong currency's MRR, or offsetting on the wrong side of the market (V2 p.18, p.20, p.78).
7. Forgetting the funding cost in carry trade returns (the gross-return distractor) or ignoring the currency move entirely (the raw-spread distractor) (V2 p.40, p.77).
8. Swapping the parity conditions' properties: only CIP is arbitrage-enforced, forward unbiasedness needs CIP plus UIRP (not real rate parity), and the international Fisher effect is the nominal-spread-equals-inflation-spread statement, not UIRP (V2 p.22, p.26, p.33, p.36).
9. Using $\%\Delta S_{f/d}$ with the wrong sign: a rise in $S_{f/d}$ is a depreciation of the foreign currency and an appreciation of the domestic base (V2 p.23, p.24).
10. Applying the high-capital-mobility policy table to a country with capital controls, or vice versa; always locate the mobility assumption before choosing appreciate, depreciate, or indeterminate (V2 p.49, p.50, p.80).
11. Extending the Mundell-Fleming short-run fiscal appreciation into the long run; the portfolio balance approach reverses it as debt accumulates (V2 p.54, p.80).
12. Treating rising FX reserves or an undervalued currency as crisis warnings; pre-crisis reserves fall and the currency sits above its historical mean (V2 p.60, p.80).
13. Assuming DM central bank intervention controls exchange rate levels; DM reserves are trivial next to turnover, and even for EM the solid evidence is lower volatility more than level control (V2 p.58).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "02-01" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
