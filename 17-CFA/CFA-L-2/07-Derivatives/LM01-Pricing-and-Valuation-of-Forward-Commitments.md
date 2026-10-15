---
type: cfa-lm
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
volume: 7
lm: 1
title: "Pricing and Valuation of Forward Commitments"
pages: "3-79"
weight_band: "5-10%"
difficulty: 4
los_count: 7
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/derivatives]
---

# LM1: Pricing and Valuation of Forward Commitments

Difficulty 4 of 5: one idea (carry arbitrage) generates a dozen instrument-specific formulas, and the item sets punish every convention slip, the FRA discounting step, the conversion factor division, day counts, annualization of periodic swap rates, and sign errors on pay versus receive positions.

## LOS map

- **describe** how equity forwards and futures are priced, and calculate and interpret their no-arbitrage value (V7 p.3) ^los-07-01-a
    - Examiner asks: compute $F_0 = \text{FV}(S_0) - \text{FV}(D)$ for a dividend-paying stock or index (discrete or continuous), then value an existing position as $V_t = \text{PV}[F_t - F_0]$, watching the sign for the short.
- **describe** the carry arbitrage model without underlying cashflows and with underlying cashflows (V7 p.3) ^los-07-01-b
    - Examiner asks: given a market forward price above or below $\text{FV}(S_0 + CC_0 - CB_0)$, name the trade (carry arbitrage: sell forward, borrow, buy asset; reverse carry: buy forward, short asset, lend) and state how carry costs and benefits shift $F_0$.
- **describe** how interest rate forwards and futures are priced, and calculate and interpret their no-arbitrage value (V7 p.3) ^los-07-01-c
    - Examiner asks: read an "X x Y" FRA quote, derive $FRA_0$ from two spot MRRs, compute the advanced-settled payment with its discount factor, and value a seasoned FRA from the new offsetting FRA rate.
- **describe** how fixed-income forwards and futures are priced, and calculate and interpret their no-arbitrage value (V7 p.3) ^los-07-01-d
    - Examiner asks: build the full price $B_0 + AI_0$, compute $Q_0 = [1/CF]\{\text{FV}[B_0 + AI_0] - AI_T - FVCI\}$, or find the arbitrage profit when the quoted futures price is off.
- **describe** how interest rate swaps are priced, and calculate and interpret their no-arbitrage value (V7 p.3) ^los-07-01-e
    - Examiner asks: compute $r_{FIX} = (1 - PV_n)/\sum PV_i$ from a table of PV factors (annualizing with $1/AP$ when resets are quarterly), then value a seasoned swap as $NA \times (FS_0 - FS_t) \sum PV_i$ with the right sign for the pay-fixed party.
- **describe** how currency swaps are priced, and calculate and interpret their no-arbitrage value (V7 p.3) ^los-07-01-f
    - Examiner asks: solve the three unknowns (two fixed rates, one notional via $NA_a = S_0 NA_b$), or revalue the swap after rates and the exchange rate move, identifying which party receives currency a from how the quote is stated.
- **describe** how equity swaps are priced, and calculate and interpret their no-arbitrage value (V7 p.3) ^los-07-01-g
    - Examiner asks: net a quarterly equity return against an annualized fixed rate, or value a seasoned swap as $V_{FIX}(C_0) - (S_t/S_{t-1})NA_E$ and find the index level that zeroes it.

## Core intuition

Everything in this module comes from thinking like an arbitrageur who obeys two rules: do not use your own money, and do not take any price risk (V7 p.4).
Under those rules any position must be financed by borrowing or short-sale proceeds, and any exposure must be hedged, so every completed strategy is riskless and self-financing.
The no-arbitrage principle then says such a strategy must earn exactly zero, because a riskless profit on zero investment would be traded away instantly (V7 p.5).
The law of one price does the work: two positions with identical future cash flows in every state must have the same price today, and value additivity lets us price a package as the sum of its parts (V7 p.5).
Four standing assumptions make the machinery clean: replicating instruments are identifiable and investable, market frictions are nil, short selling is allowed with full use of proceeds, and borrowing and lending happen at a known risk-free rate (V7 p.5).

Pricing and valuation are different tasks and the exam tests the distinction.
Pricing means finding the forward price or fixed rate at initiation such that the contract value is zero; valuation means marking an existing contract to market later, when it is generally worth something (V7 p.4).
At initiation $V_0 = 0$ by construction of an at-market contract; at expiration the long forward is worth $V_T = S_T - F_0$, the sale price minus the locked purchase price (V7 p.9).
In between, value is found without executing anything: hypothetically offset the old contract with a new one at today's price and discount the now-riskless difference (V7 p.16).

> [!abstract] Idea 1: the forward price is the future value of carrying the asset, nothing more
> To offset a short forward, buy the asset now with borrowed money and carry it to delivery; the all-in cost at time T is $\text{FV}(S_0)$ plus any storage-type costs minus any income the asset throws off, so no arbitrage forces $F_0 = \text{FV}(S_0 + CC_0 - CB_0)$ (V7 p.11, p.18).
> Expectations of where the spot price is headed appear nowhere; only the spot price, the financing rate, the carry cash flows, and time matter (V7 p.15).
> Carry costs raise the burden of holding, so they raise $F_0$; carry benefits (dividends, coupons, foreign interest) lower it, which is why an index with a dividend yield above the financing rate has a forward price below spot that converges to spot from below (V7 p.7, p.8).

The convergence property anchors both ends of the contract's life: at expiration $F_T = f_T = S_T$, because the price to transact one instant ahead must equal the spot price, and the basis between futures and spot shrinks to zero as maturity nears (V7 p.7, p.8).
If the forward price sits above the carry model value, the arbitrageur sells the forward, borrows, and buys the asset (carry arbitrage); if below, buys the forward, shorts the asset, and lends the proceeds (reverse carry arbitrage); either way the mispricing is captured in full with zero net investment and zero risk (V7 p.13, p.14).
The illustration with $S_0 = 100$, $r = 5\%$, and a forward quoted at 106 against the model's 105 pays exactly +1 at T whether the stock finishes at 90 or at 110, and its time 0 value is $1/1.05 = 0.9524$ (V7 p.13).

> [!abstract] Idea 2: valuation is always the present value of a difference in prices or rates
> A long forward entered at $F_0$ and offset at $t$ with a short at $F_t$ locks the time T cash flow $F_t - F_0$, so $V_t = \text{PV}[F_t - F_0]$; the same one-liner values FRAs (difference in FRA rates), swaps (difference in fixed swap rates times the annuity of PV factors), currency swaps (difference of two bond values through the current spot rate), and equity swaps (bond value against the grown equity leg) (V7 p.16, p.31, p.46, p.53, p.59).
> Futures break the pattern only because daily marking to market sweeps the value into the margin account, so a futures contract is worth zero again right after each settlement (V7 p.10, p.23).
> Every valuation answer on the exam is therefore built in two steps: find today's replacement price or rate for the remaining contract, then discount the locked-in difference back.

The interest rate leg of the module runs on the MRR spot market conventions: add-on interest, actual/360, so a 90-day deposit of $50{,}000$ at 2% repays $50{,}000 \times [1 + 0.02(90/360)]$ (V7 p.24).
An FRA is a forward on an m-day MRR that expires in h days; the "3 x 9" label means the FRA expires in 3 months and the underlying deposit runs from month 3 to month 9, so the underlying is a six-month rate (V7 p.25).
The long (fixed payer, floating receiver) gains when rates rise; the short (fixed receiver) is the natural hedge for a lender wanting to lock a future lending rate (V7 p.25).
FRAs are advanced set, advanced settled: the rate is fixed at expiration h and the payoff is paid at h, but the interest it compensates for would only be due at h + m, so the settlement is discounted from T back to h by $1 + D_m t_m$ (V7 p.26, p.27).
The FRA rate itself is nothing but the implied forward rate between the two spot MRRs bracketing the deposit period, from $[1 + L_h t_h][1 + FRA_0 t_m] = [1 + L_T t_T]$ (V7 p.29).

Fixed-income forwards add three market conventions rather than new theory (V7 p.33).
Bonds quote clean ($B_0$); you trade at the full price $B_0 + AI_0$, with accrued interest growing linearly through the coupon period (V7 p.33).
Futures let the short deliver any of several bonds, so each bond gets a conversion factor that restates it as a 6% yield equivalent, the quoted futures price satisfies $F_0 = Q_0 \times CF$, and because the adjustment is imperfect a cheapest-to-deliver bond emerges (V7 p.33, p.34).
The carry model then prices the contract off the full price minus the PV of coupons paid over the contract's life, and the equilibrium quoted price strips out the accrued interest that will exist at expiration (V7 p.34, p.35, p.36).

> [!abstract] Idea 3: a swap is a portfolio of bonds, so swap pricing is bond pricing
> A receive-fixed, pay-floating swap replicates a long fixed-rate bond plus a short floating-rate bond of equal par; the floater is worth par at every reset because its coupon resets to its own discount rate, so setting $V_{FIX} = 1$ yields the swap rate $r_{FIX} = (1 - PV_n)/\sum PV_i$, one minus the last discount factor over the annuity of discount factors (V7 p.40, p.43, p.45).
> A currency swap is a bond in currency a against a bond in currency b joined by one spot exchange rate at initiation; an equity swap is a bond against an equity position that is trued back to notional at every reset (V7 p.49, p.57, p.58).
> Whenever a swap question looks new, ask which pair of instruments replicates the legs and price those; that is also why the equity swap's fixed rate is identical to the interest rate swap's (V7 p.59).

![[Swap-Cash-Flow-Timeline.excalidraw]]

The swap sections all follow the same two-step rhythm as forwards.
Price: choose the fixed rate so both legs have equal present value at initiation and the swap is worth zero (V7 p.42, p.45).
Value: after rates move, receive-fixed is worth the present value of the fixed-rate annuity you hold above the fixed rate you could get now, $NA \times (FS_0 - FS_t)\sum PV_i$, because offsetting with a new pay-fixed swap cancels every floating cash flow and leaves the difference in fixed coupons (V7 p.46).
Currency swaps exchange notionals at both ends (set by the initial spot rate, $NA_a = S_0 NA_b$), pay in two currencies without netting, and are revalued as the difference of the two bond values with the foreign one translated at the current spot rate (V7 p.48, p.50, p.53).
Equity swaps net an equity return (which can be negative, making the receive-equity party pay both legs) against a fixed or floating rate, and a seasoned position is the fixed bond's current value minus the notional grown by the equity's return since the last reset (V7 p.57, p.58, p.59).
Currency forwards themselves are the same carry story with the foreign interest rate as the carry benefit; the resulting relation is covered interest rate parity, developed fully in the Economics reading on exchange rates.

## Formulas and derivations

**Forward value at expiration** (V7 p.9)
$$
V_T = S_T - F_0 \ \ (\text{long}), \qquad -V_T = F_0 - S_T \ \ (\text{short})
$$
^f-07-01-1

- $S_T$: spot price at expiration; $F_0$: forward price fixed at initiation; value is per unit of underlying.
- Profit on any completed transaction is sale price minus purchase price; the long buys at $F_0$ and can sell at $S_T$, the short is the mirror image (V7 p.9).
- Convergence guarantees $F_T = f_T = S_T$, so the same expression prices the expiring futures (V7 p.7).

**Futures mark-to-market value during the trading day** (V7 p.9, p.10)
$$
v_t = N_f \times (f_t - f_{t-1}), \qquad v_t = 0 \ \text{after daily settlement}
$$
^f-07-01-2

- $N_f$: contract multiplier (standard size); $f_{t-1}$: previous settlement price.
- Gains and losses are swept into the margin account at settlement and the contract reprices to the settlement price, so value resets to zero each day (V7 p.10).
- This is the only structural valuation difference between futures and forwards in this module (V7 p.38, p.39).

**Carry arbitrage forward price, no underlying cash flows** (V7 p.13)
$$
F_0 = \text{FV}(S_0) = S_0 (1 + r)^T
$$
^f-07-01-3

- $r$: annually compounded risk-free rate; $T$: years to expiration; with continuous compounding $F_0 = S_0 e^{r_c T}$ (V7 p.11).
- Buy the asset with borrowed $S_0$ and sell it forward: the combined position has zero cash flow at 0 and $F_0 - \text{FV}(S_0)$ at T with no risk, so the bracket must be zero (V7 p.11, p.13).
- $\text{FV}(S_0)$ is a financing number, not an expectation of $S_T$; forecasts of the underlying never enter (V7 p.13, p.15).

> [!tip] Calculator
> Three-month forward on 63.31 at 2.75%: `1.0275 y^x 0.25 = x 63.31 =` gives 63.7408.

**Forward value prior to expiration** (V7 p.16, p.17)
$$
V_t = \text{PV}[F_t - F_0] = \frac{F_t - F_0}{(1+r)^{T-t}} = S_t - \frac{F_0}{(1+r)^{T-t}}
$$
^f-07-01-4

- $F_t$: forward price of a new contract at $t$ with the same expiration; short value is $-V_t = \text{PV}[F_0 - F_t]$ (V7 p.17).
- Offsetting the long at $F_0$ with a short at $F_t$ cancels $S_T$ and locks the riskless cash flow $F_t - F_0$ at T, whose PV is the value (V7 p.16).
- The second form follows because $F_t = S_t(1+r)^{T-t}$, so $\text{PV}[F_t] = S_t$; when the underlying has carry cash flows both $F_t$ and $F_0$ already reflect them, so the difference form still applies (V7 p.17, p.20).

> [!tip] Calculator
> $F_0 = 105$, $S_{0.75} = 110$, $r = 5\%$, 3 months left: `110 x 1.05 y^x 0.25 = - 105 = / 1.05 y^x 0.25 =` gives 6.2729.

**Carry arbitrage forward price with carry costs and benefits** (V7 p.18, p.19)
$$
F_0 = \text{FV}(S_0 + CC_0 - CB_0); \qquad F_0 = \text{FV}(S_0) - \text{FV}(D) \ \ (\text{dividend-paying stock})
$$
^f-07-01-5

- $CC_0$, $CB_0$: present values at 0 of carry costs and carry benefits; $D$: dividend, compounded only from its payment date to T, so $\text{FV}(D) = D(1+r)^{T-t_D}$ (V7 p.19).
- Costs add to the burden of carrying and raise $F_0$; benefits are income collected while carrying and lower it (V7 p.18).
- Financing cost is already in the FV operator; storage, insurance, and spoilage enter $CC$, dividends, coupons, and foreign interest enter $CB$ (V7 p.18).

**Continuous-compounding carry model (index futures)** (V7 p.21)
$$
F_0 = S_0\, e^{(r_c + CC - CB)T}
$$
^f-07-01-6

- $r_c$, $CC$, $CB$: continuously compounded rates (the dividend yield enters as CB); used for stock indexes where discrete dividends are impractical to track (V7 p.20, p.21).
- A dividend yield above the financing rate makes the exponent negative and the futures price sits below spot, converging to it from below (V7 p.8, p.22).

> [!tip] Calculator
> EURO STOXX 50 at 3,500, $r_c = 0.15\%$, yield 3%, 3 months: `0.0015 - 0.03 = x 0.25 = 2nd e^x x 3500 =` gives 3,475.15.

**Currency forward via carry (covered interest rate parity)** (V7 p.18)
$$
F_0 = S_0 \times \frac{(1 + r_d)^T}{(1 + r_f)^T}
$$
^f-07-01-7

- $S_0$: spot rate in domestic units per foreign unit; $r_d$: domestic risk-free rate (financing cost); $r_f$: foreign risk-free rate (carry benefit earned on the foreign currency held).
- This is the carry model of (V7 p.18) applied to a currency position: interest on the foreign balance is the carry benefit, so the higher-rate currency trades at a forward discount.
- The Economics reading derives the same relation as covered interest rate parity; here it is the reason currency swap pricing can push all FX considerations into the single initial spot rate (V7 p.52).

**MRR deposit terminal amount (add-on interest)** (V7 p.24)
$$
TA = NA \times [1 + L_m t_m], \qquad t_m = m / 360
$$
^f-07-01-8

- $L_m$: m-day MRR set at deposit; $NA$: notional deposited; interest is $NA \times L_m t_m$, paid at maturity (settled in arrears) on an actual/360 count (V7 p.24).
- This spot-market convention is the benchmark from which FRA payoffs are computed; the FRA parties need not hold any deposit (V7 p.25).

**FRA settlement at expiration (advanced set, advanced settled)** (V7 p.26, p.27)
$$
\text{Long (pay-fixed): } NA \times \frac{[L_m - FRA_0]\, t_m}{1 + D_m t_m}, \qquad \text{Short: } NA \times \frac{[FRA_0 - L_m]\, t_m}{1 + D_m t_m}
$$
^f-07-01-9

- $L_m$: m-day MRR observed at FRA expiration h; $D_m$: discount rate for the settlement (often assumed equal to $L_m$, but the vignette can set it differently, as in Example 8).
- The rate difference would naturally be paid at T = h + m (in arrears); paying it early at h requires discounting over m days, because the recipient can earn interest on the advanced payment (V7 p.27).
- The long is the floating receiver and gains when rates rise; the short gains when rates fall (V7 p.25, p.28).

> [!tip] Calculator
> 10m notional, $L_{90} = 2.55\%$, $FRA_0 = 2.60\%$, $D = 2.40\%$, short: `0.026 - 0.0255 = x 0.25 = x 10000000 = / 1.006 =` gives 1,242.54.

**FRA fixed rate (implied forward rate)** (V7 p.29)
$$
FRA_0 = \frac{1}{t_m}\left[\frac{1 + L_T t_T}{1 + L_h t_h} - 1\right]
$$
^f-07-01-10

- $L_h$: spot MRR to FRA expiration ($t_h = h/360$); $L_T$: spot MRR to underlying maturity ($t_T = T/360$, $T = h + m$); result is annualized by dividing by $t_m$.
- Borrowing to T directly must cost the same as borrowing to h and rolling at the forward rate: $[1 + L_h t_h][1 + FRA_0 t_m] = [1 + L_T t_T]$ (V7 p.29).
- Quick check: the time-weighted average of $L_h$ and $FRA_0$ must roughly equal $L_T$, and the arithmetic-average shortcut is always biased slightly high (V7 p.29, p.30).

> [!tip] Calculator
> 3 x 6 with $L_{180} = 2.0\%$, $L_{90} = 1.5\%$: `1 + 0.02 x 0.5 = / (1 + 0.015 x 0.25) = - 1 = x 4 =` gives 0.024907.

**FRA value at time g before expiration** (V7 p.31, p.32)
$$
V_g = NA \times \frac{[FRA_g - FRA_0]\, t_m}{1 + D_{(T-g)}\, t_{(T-g)}} \ \ (\text{long}); \qquad -V_g = NA \times \frac{[FRA_0 - FRA_g]\, t_m}{1 + D_{(T-g)} t_{(T-g)}} \ \ (\text{short})
$$
^f-07-01-11

- $FRA_g$: rate on a new offsetting FRA expiring at the same h with the same m-day underlying, computed from the current spot rates for h - g and T - g days.
- The offsetting FRA cancels $L_m$ at T, leaving the known cash flow $[FRA_g - FRA_0] t_m$ at T, discounted all the way from T back to g (V7 p.31).
- Two traps live here: compute $FRA_g$ from the shortened tenors, and discount over T - g days, not m days (V7 p.31, p.32).

**Accrued interest** (V7 p.33)
$$
AI = \frac{NAD}{NTD} \times \frac{C}{n}
$$
^f-07-01-12

- $NAD$: days accrued since the last coupon; $NTD$: days in the coupon period (180 for semiannual on a 360-day year); $C$: annual coupon amount; $n$: coupons per year.
- Full (dirty) price = quoted (clean) price + AI: $S_0 = B_0 + AI_0$; you always pay the full price (V7 p.33, p.34).
- Linear interpolation within the period; expressed in currency units, not percent (V7 p.33).

**Fixed-income forward or futures price (conversion factor form)** (V7 p.34, p.35)
$$
F_0 = Q_0 \times CF = \text{FV}[S_0 + CC_0 - CB_0] = \text{FV}[B_0 + AI_0 - PVCI]
$$
^f-07-01-13

- $Q_0$: quoted futures price; $CF$: conversion factor (approximate price of $1 par at a 6% yield to maturity, standardizing the deliverable basket); $PVCI$: PV of coupon interest paid over the contract's life (the carry benefit); $CC = 0$ for bonds (V7 p.33, p.34).
- Multiple deliverable bonds make the quoted price trade in CF-adjusted terms, and the imprecision of CF creates the cheapest-to-deliver bond (V7 p.33).
- The long's profit at expiration settles against the quoted bond price: $v_T = B_T - F_0 = (S_T - AI_T) - F_0$ (V7 p.34, p.35).

**Equilibrium quoted futures price** (V7 p.36)
$$
Q_0 = \frac{1}{CF}\left\{\text{FV}[B_0 + AI_0] - AI_T - FVCI\right\}
$$
^f-07-01-14

- $AI_T$: accrued interest at contract expiration (subtracted because the futures settles on the quoted, clean price); $FVCI$: future value at T of coupons received during the contract.
- Derivation: no arbitrage requires $F_0 + AI_T = \text{FV}[B_0 + AI_0 - PVCI]$, i.e. the locked-in full sale proceeds must equal the cost of buying and carrying the bond; solve for $Q_0 = F_0/CF$ (V7 p.36).
- If the quoted price is higher, sell the futures, borrow, buy the bond, deliver, and keep the difference; if lower, run reverse carry arbitrage (V7 p.35, p.36).

> [!tip] Calculator
> Euro-bund: `108 + 0.083 = x 1.001 y^x (1/12) = - 0.25 = / 0.729535 =` gives 147.82.

**Interest rate swap as a pair of bonds** (V7 p.43)
$$
V_{swap}(\text{receive-fixed}) = V_{FIX} - V_{FLT}, \qquad V_{FLT} = \text{par} = 1 \ \text{at any reset date}
$$
^f-07-01-15

- Receive-fixed, pay-floating replicates long a fixed-rate bond and short (issuer of) a floating-rate bond; par payments at maturity offset (V7 p.40, p.43).
- The floater prices at par at each reset because its coupon is set equal to its own discount rate (V7 p.45).
- Pricing the swap means choosing $r_{FIX}$ so $V_{FIX} = V_{FLT} = 1$ and the swap value is zero at initiation (V7 p.42, p.44).

**Present value factor from a spot rate** (V7 p.44)
$$
PV_i(1) = \frac{1}{1 + R_{spot,i}\,(NAD_i / NTD)}
$$
^f-07-01-16

- Simple (add-on) interest on the money-market convention; e.g. 90-day 2.10% gives $1/[1 + 0.0210(90/360)] = 0.994777$ (V7 p.44).
- These factors are the atoms of every swap computation: sum them for the coupon annuity, use the last one for par (V7 p.44).

**Value of a fixed-rate bond from PV factors** (V7 p.44)
$$
V_{FIX} = C \sum_{i=1}^{n} PV_i(1) + PV_n(1)
$$
^f-07-01-17

- $C$: periodic coupon per 1 of par (annual rate times AP); the final PV factor is used twice, once inside the annuity sum and once for par (V7 p.44, p.46).
- Example check: quarterly 4% coupon on the Exhibit 16 curve gives $0.01(3.941199) + 0.975229 = 1.014641$, i.e. 101.464% of par (V7 p.44).

**Swap pricing equation (fixed swap rate)** (V7 p.45)
$$
r_{FIX} = \frac{1 - PV_n(1)}{\sum_{i=1}^{n} PV_i(1)} \times \frac{1}{AP}
$$
^f-07-01-18

- $AP$: accrual period (360/360 = 1 for annual resets, 90/360 for quarterly); the raw ratio is the periodic rate, and dividing by AP annualizes it.
- Derivation: set $V_{FIX} = r_{FIX} \times AP \sum PV_i + PV_n = 1$ (the floater's par value) and solve (V7 p.45).
- The fixed swap cash flow per unit notional is $FS = AP \times r_{FIX}$ (V7 p.45).

> [!tip] Calculator
> Annual resets, $PV_5 = 0.937467$, sum 4.822107: `1 - 0.937467 = / 4.822107 =` gives 0.012968.

**Interest rate swap value after initiation** (V7 p.46, p.47)
$$
V_{SWAP,t} = NA \times (FS_0 - FS_t) \sum_{i=1}^{n} PV_i \ \ (\text{receive-fixed}); \qquad -V_{SWAP,t} = NA \times (FS_t - FS_0) \sum_{i=1}^{n} PV_i \ \ (\text{pay-fixed})
$$
^f-07-01-19

- $FS_0 = AP \times r_{FIX,0}$: original fixed cash flow; $FS_t = AP \times r_{FIX,t}$: fixed cash flow on a new at-market swap over the remaining term; $n$: remaining resets; $PV_i$: current PV factors.
- Offsetting the swap at t cancels the floating legs date by date, leaving an annuity of $FS_0 - FS_t$ per period, valued with the current discount factors (V7 p.46).
- Receive-fixed gains when rates have fallen ($FS_0 > FS_t$); pay-fixed gains when rates have risen (V7 p.46, p.47).

**Currency swap pricing: notional and two fixed rates** (V7 p.50, p.51)
$$
NA_a = S_0 \times NA_b; \qquad r_a = \frac{1 - PV_{n,a}(1)}{\sum_{i=1}^{n} PV_{i,a}(1)} \times \frac{1}{AP}, \quad r_b = \frac{1 - PV_{n,b}(1)}{\sum_{i=1}^{n} PV_{i,b}(1)} \times \frac{1}{AP}
$$
^f-07-01-20

- $S_0$: spot rate in units of currency a per unit of currency b; each fixed rate comes from its own currency's term structure, independent of the notionals (V7 p.50).
- Matching notionals through $S_0$ makes the initial exchange (and the swap value) zero: $V_{CS} = V_a - S_0 V_b = 0$ with both bonds at par (V7 p.49, p.50).
- Notionals are exchanged at initiation and at maturity, payments are in different currencies and are not netted (V7 p.48).

**Currency swap value after initiation** (V7 p.53)
$$
V_{CS} = NA_a\left[AP \cdot r_{Fix,a} \sum_{i=1}^{n} PV_i(1) + PV_n(1)\right] - S_t\, NA_b\left[AP \cdot r_{Fix,b} \sum_{i=1}^{n} PV_i(1) + PV_n(1)\right]
$$
^f-07-01-21

- First bracket: value of the currency a bond (per 1 of par) on currency a's current curve; second bracket: same for currency b, translated at the current spot rate $S_t$ (units of a per unit of b).
- $V_{CS}$ is the value to the party receiving currency a; the counterparty's value is $-V_{CS}$, convertible to currency b at $S_t$ (V7 p.53).
- Identify currency a from how the exchange rate is quoted (numerator currency), not from who is domestic; Example 16 hinges on this (V7 p.53, p.54).

**Equity swap cash flows and fixed rate** (V7 p.57, p.59)
$$
S_i = NA_E\, R_E; \qquad S_i - FS = NA_E \left[R_E - AP \cdot r_{FIX}\right]; \qquad r_{FIX} = \frac{1 - PV_n(1)}{\sum_{i=1}^{n} PV_i(1)} \times \frac{1}{AP}
$$
^f-07-01-22

- $R_E$: periodic (not annualized) equity return over the reset period, with or without dividends per the contract; the fixed leg is quoted annualized and accrues by AP (V7 p.57).
- The fixed rate on an equity swap equals the fixed rate on a comparable interest rate swap because the replicating bond leg is identical (V7 p.59, p.60).
- A negative equity return means the receive-equity party pays both the equity decline and the fixed rate, a liquidity risk the curriculum flags (V7 p.58).

**Equity swap value after initiation** (V7 p.59)
$$
V_{EQ,t} = V_{FIX}(C_0) - \frac{S_t}{S_{t-1}} NA_E - \text{PV}(\text{Par} - NA_E)
$$
^f-07-01-23

- $V_{FIX}(C_0)$: current value of the implied fixed-rate bond with the original coupon $C_0$, discounted on today's curve; $S_t/S_{t-1}$: equity growth since the last reset (not since initiation); the last term is zero when Par $= NA_E$ (V7 p.59).
- This values the receive-fixed, pay-equity party; negate for receive-equity (V7 p.59).
- Setting $V_{EQ,t} = 0$ and solving for $S_t$ gives the equity level at which the swap is worth zero, a favorite question form (V7 p.61).

## Worked examples

**Example 1: forward contract price** (V7 p.15)
Australian stock, no dividends, $S_0 = A\$63.31$, $r = 2.75\%$ annual compounding, three-month forward.
$F_0 = 63.31(1.0275)^{0.25} = A\$63.7408$ (Python: 63.7408), answer B.
If the rate falls 50 bps to 2.25%: $F_0 = 63.31(1.0225)^{0.25} = A\$63.6632$ (Python: 63.6632), so the forward price decreases (answer A); forward prices move with the financing rate as long as the underlying itself is not rate-driven. ^ex-07-01-1

**Example 2: forward contract value** (V7 p.17, p.18)
Long one-year forward at $F_0 = 105$; nine months later $S_{0.75} = 110$, $r = 5\%$, $T - t = 0.25$.
New forward price: $F_t = 110(1.05)^{0.25} = 111.3499$ (Python: 111.3499).
$V_t = (111.3499 - 105)/(1.05)^{0.25} = 6.2729$, or equivalently $110 - 105/(1.05)^{0.25} = 6.2729$ (Python confirms both routes), answer B.
The in-text mispricing illustration is the same machinery: with the model price 105 and a market forward of 106, the short forward plus carry position is worth $V_0 = (106 - 105)/1.05 = 0.9524$ today (V7 p.13). ^ex-07-01-2

**Example 3: forward price with underlying cash flows** (V7 p.19, p.20)
US stock at \$1,000 pays a \$10 dividend in two months; $r = 5\%$; three-month forward.
$F_0 = \text{FV}(S_0) - \text{FV}(D) = 1{,}000(1.05)^{3/12} - 10(1.05)^{1/12} = 1{,}012.2722 - 10.0407 = \$1{,}002.2315$ (Python: 1,002.2315), answer A.
Equation 4 route: $CB_0 = 10/(1.05)^{2/12} = 9.9190$, and $(1{,}000 - 9.9190)(1.05)^{3/12} = 1{,}002.23$ (Python: 1,002.2315).
If the dividend moves to one month, it earns interest for two months, $\text{FV}(D) = 10(1.05)^{2/12} = 10.0816$, and $F_0$ falls to 1,002.1906 (Python: 1,002.1906), answer A. ^ex-07-01-3

**Example 4: forward price with carry costs and benefits** (V7 p.20)
Long one-year forward at $F_0 = 1{,}000$; seven months later $S_t = 1{,}050$, PV of remaining costs $CC_t = 4$, PV of remaining income $CB_t = 28$, $r = 2\%$, 5 months left.
$F_t = (1{,}050 + 4 - 28)(1.02)^{5/12} = 1{,}034.50$ (Python: 1,034.5006).
$V_t = (1{,}034.50 - 1{,}000)/(1.02)^{5/12} = 34.22$ (Python: 34.2171), answer A. ^ex-07-01-4

**Example 5: equity futures price with continuous compounding** (V7 p.22)
EURO STOXX 50 at 3,500, continuous dividend yield 3%, $r_c = 0.15\%$, three months.
$f_0 = 3{,}500\, e^{(0.0015 + 0 - 0.03)(3/12)} = 3{,}475.15$ (Python: 3,475.1511), answer B.
The yield exceeds the financing rate, so the futures price sits below spot. ^ex-07-01-5

**Example 6: equity forward with discrete dividend** (V7 p.22)
Nestle at CHF70, CHF2.20 dividend at the one-month expiration (so $\text{FV}(CB_0) = 2.20$), $r = 1\%$.
$F_0 = 70(1.01)^{1/12} - 2.20 = \text{CHF}67.86$ (Python: 67.8581), answer B. ^ex-07-01-6

**Example 7: equity forward valuation** (V7 p.23, p.24)
Bought a one-year forward at 102; now three months to expiration, $S_t = 110$, $r = 5\%$, no carry cash flows.
$F_t = 110(1.05)^{0.25} = 111.3499$; $V_t = (111.3499 - 102)/(1.05)^{0.25} = 9.2366$ (Python: 9.2366), answer B; the value exceeds $110 - 102 = 8$ because interest costs push the new forward price above spot.
A newly announced dividend before expiration lowers $F_t$ and therefore lowers the long forward's value (answer A).
The parallel futures contract at 102 with today's futures price 112.35 is worth zero after marking to market (answer B): daily settlement has already paid out the gain (V7 p.24). ^ex-07-01-7

**Example 8: interest on MRR spot deposit and FRA payments** (V7 p.27, p.28)
UK company will deposit 10m pounds for 90 days starting in 30 days and shorts (receives fixed on) a 1 x 4 FRA; discount rate for settlement 2.40%; after 30 days, 90-day MRR is 2.55%.
Deposit interest: $TA = 10{,}000{,}000[1 + 0.0255(0.25)] = 10{,}063{,}750$, so interest is 63,750 (Python: 63,750), answer B.
If $FRA_0 = 2.60\%$: receive-fixed settlement $= 10{,}000{,}000 \times (0.0260 - 0.0255)(0.25)/[1 + 0.0240(0.25)] = 1{,}242.54$ (Python: 1,242.54), answer B; note $D_m \ne L_m$ here.
If $FRA_0 = 2.50\%$: same computation gives $-1{,}242.54$ (Python: -1,242.54), answer A; the short pays floating and loses when rates rise above the locked fixed rate. ^ex-07-01-8

**Example 9: FRA fixed rate** (V7 p.30, p.31)
Canadian 6 x 9: $L_{180} = 1.50\%$, $L_{270} = 1.75\%$.
$FRA_0 = \{[1 + 0.0175(270/360)]/[1 + 0.015(180/360)] - 1\}/(90/360) = (1.013125/1.0075 - 1) \times 4 = 2.2333\%$ (Python: 2.2333%), answer B.
Four spot rates (1, 3, 6, 12 months) allow six FRA rates: 1 x 3, 1 x 6, 1 x 12, 3 x 6, 3 x 12, 6 x 12 (answer B), one per ordered pair of maturities.
1 x 3 from $L_{30} = 2.48\%$, $L_{90} = 2.58\%$: $\{[1 + 0.0258(90/360)]/[1 + 0.0248(30/360)] - 1\}/(60/360) = 2.62\%$ (Python with exact fractions: 2.6246%; the printed 2.6220% reflects intermediate rounding, both round to answer C). ^ex-07-01-9

**Example 10: FRA valuation** (V7 p.32)
Long (receive-floating) 6 x 9 FRA, C\$10m notional, priced at $FRA_0 = 0.877\%$; 90 days later $L_{90} = 1.25\%$, $L_{180} = 1.35\%$.
The offsetting FRA is now a 3 x 6: $FRA_g = \{[1 + 0.0135(180/360)]/[1 + 0.0125(90/360)] - 1\}/(90/360) = 1.4455\%$ (Python: 1.44548%).
$V_g = 10{,}000{,}000 \times (0.01445 - 0.00877)(90/360)/[1 + 0.0135(180/360)] = 14{,}105$ (Python with the curriculum's rounded 1.445%: 14,105; with the unrounded rate: 14,117), answer A.
Rates rose, so the receive-floating position gained; the discount runs over $T - g = 180$ days at the 180-day rate. ^ex-07-01-10

**Example 11: Euro-bund futures price** (V7 p.37)
2% semiannual bund quoted at 108, $AI_0 = (15/180)(2/2) = 0.083$, $AI_T = (45/180)(2/2) = 0.25$, no interim coupons, $r = 0.1\%$, one month, $CF = 0.729535$.
$Q_0 = [1/0.729535]\{(1.001)^{1/12}(108 + 0.083) - 0.25 - 0\} = 147.82$ (Python: 147.8229), answer B.
Equivalently $F_0 = (1.001)^{1/12}(108.083) - 0.25 = 107.84$ (Python: 107.8420) and $Q_0 = F_0/CF$.
The in-text disequilibrium demo runs the same numbers the other way: with $B_0 = 107$, $AI_0 = 0.07$, $Q_0 = 135$, $CF = 0.80$, the adjusted futures price plus $AI_T$ (108.20) exceeds the carry cost $\text{FV}(107.07) = 107.12$, so selling the futures and carrying the bond locks in 1.08 at T (PV 1.0795), and the equilibrium quoted price is $(1/0.8)\{107.12 - 0.20\} = 133.65$ (Python: 133.6544) (V7 p.35, p.36). ^ex-07-01-11

**Example 12: value of a Euro-bund forward position** (V7 p.38)
Bought five contracts (EUR 100,000 each) at $F_0 = 145$ one month ago; now $F_t = 148$, one month to expiration, $r = 0.1\%$.
$V_t = (148 - 145)/(1.001)^{1/12} = 2.99975$ per 100 par (Python: 2.99975).
Position value $= 0.0299975 \times 100{,}000 \times 5 = \text{EUR }14{,}998.75$ (Python: 14,998.75), answer B; the discounting effect is only about EUR 1.25 at these rates.
The one-month in-text warm-up is identical: long at 119.12, offset at 119.92, $V_t = 0.80/(1.005)^{1/12} = 0.7997$ (Python: 0.7997) (V7 p.38). ^ex-07-01-12

**Example 13: fixed swap rate from PV factors** (V7 p.45, p.46)
Five-year annual-reset swap; PV factors 0.990099, 0.977876, 0.965136, 0.951529, 0.937467, summing to 4.822107 (Python: 4.822107).
$r_{FIX} = (1 - 0.937467)/4.822107 \times (360/360) = 1.2968\%$ (Python: 1.29680%), answer B.
The last PV factor is used twice: in the annuity sum and against par in the numerator. ^ex-07-01-13

**Example 14: receive-fixed swap value from PV factors** (V7 p.47, p.48)
Two years into a EUR 100m seven-year receive-fixed swap at 2.0%; current five-year swap rate 1.3% (from Example 13); same PV factors.
$V_{SWAP,t} = 100{,}000{,}000 \times (0.02 - 0.013) \times 4.822107 = \text{EUR }3{,}375{,}000$ (Python: 3,375,475 using 1.3% exactly as the curriculum does after rounding; with the unrounded 1.29680% rate the value is 3,390,914, and the printed answer keys off the rounded rate), answer B.
The pay-fixed counterparty's value is the negative, $-3{,}375{,}000$ (answer B); rates fell, so receive-fixed won. ^ex-07-01-14

**Example 15: currency swap pricing with spot rates** (V7 p.51, p.52)
US company needs A\$100m for one year, quarterly resets; A\$ PV factors 0.993789, 0.987167, 0.980152, 0.972763 (sum 3.933870), US\$ PV factors 0.999750, 0.999251, 0.998502, 0.997506 (sum 3.995009); $S_0 = A\$1.140$ per US\$1 (Python reproduces every factor and both sums).
Fixed rates: $r_{A\$} = (1 - 0.972763)/3.933870 \times (360/90) = 2.7695\%$ and $r_{US\$} = (1 - 0.997506)/3.995009 \times (360/90) = 0.2497\%$ (Python: 2.76952% and 0.24969%), answer B.
Notional: $NA_{US\$} = A\$100{,}000{,}000 / (A\$1.14/US\$1) = US\$87{,}719{,}298$ (Python: 87,719,298), answer A.
Quarterly payments: $A\$100\text{m} \times (90/360)(0.027695) = A\$692{,}375$ and $US\$87{,}719{,}298 \times (90/360)(0.002497) = US\$54{,}759$ (Python: 692,375 and 54,759), answer A. ^ex-07-01-15

**Example 16: currency swap valuation with spot rates** (V7 p.54, p.55, p.56)
Sixty days on, new A\$ PV factors sum to 3.967683 with $PV_n = 0.986031$, new US\$ PV factors sum to 3.994841 with $PV_n = 0.998336$, and $S_t = A\$1.13$ per US\$1 (Python reproduces all factors and sums).
The exchange rate is quoted in A\$ per US\$, so currency a is A\$ and the swap dealer is the party receiving A\$.
$V_{CS} = 100{,}000{,}000[0.00692375(3.967683) + 0.986031] - 1.13 \times 87{,}719{,}298[0.00062425(3.994841) + 0.998336] = A\$2{,}145{,}167$ (Python: 2,145,180; the A\$13 gap is PV-factor rounding), answer C (closest 2,145,200).
Value to the US firm is $-V_{CS}$ converted at $S_t$: $-2{,}145{,}167/1.13 = -US\$1{,}898{,}378$ (Python: -1,898,389), answer B; the A\$ strengthened and A\$ rates fell, both against the A\$ payer. ^ex-07-01-16

**Example 17: equity swap cash flows** (V7 p.57, p.58)
Receive-equity, pay-fixed swap, quarterly reset, EUR 5m notional, fixed 1.6% annualized (0.4% per quarter).
Quarterly equity return +4.0%: cash flow $= 5{,}000{,}000 \times (0.040 - 0.004) = +\text{EUR }180{,}000$ (Python: 180,000), answer C; the equity return is already quarterly, only the fixed leg needs the AP adjustment.
Quarterly equity return -6.0%: $5{,}000{,}000 \times (-0.060 - 0.004) = -\text{EUR }320{,}000$ (Python: -320,000), answer A; with a negative equity leg the equity receiver pays both legs, the liquidity risk the curriculum flags. ^ex-07-01-17

**Example 18: equity swap pricing** (V7 p.60)
Same five annual PV factors as Example 13 (sum 4.822107), floating bond at par.
The EURO STOXX 50 equity swap's fixed rate equals the interest rate swap's: $r_{FIX} = (1 - 0.937467)/4.822107 = 1.2968\%$ (Python: 1.29680%), answer C; the replicating bond leg is identical, so the price is identical. ^ex-07-01-18

**Example 19: equity swap valuation** (V7 p.60, p.61)
Six months ago: receive-fixed, pay-equity five-year annual-reset swap, fixed 1.5%, equity at 100, $NA_E = 10{,}000{,}000$, Par $= NA_E$; now the curve is flat at 1.2% and the equity trades at 105.
Remaining fixed flows: 150,000 at 0.5, 1.5, 2.5, 3.5 years and 10,150,000 at 4.5 years; PV factors $1/[1 + 0.012 t]$ are 0.994036, 0.982318, 0.970874, 0.959693, 0.948767.
$V_{FIX} = 10{,}216{,}019$ (Python: 10,216,019).
$V_{EQ,t} = 10{,}216{,}019 - (105/100)(10{,}000{,}000) - 0 = -283{,}981$ (Python: -283,981), closest to A (-300,000); the equity rose 5% while the bond leg gained only 2.16%.
Zero value requires $S_t = (10{,}216{,}019/10{,}000{,}000) \times 100 = 102.16$ (Python: 102.1602), answer B. ^ex-07-01-19

## Item-set patterns

> [!warning] Trap 1: the undiscounted FRA settlement
> The vignette gives $L_m$ at expiration and asks for the advanced-settled payment, with one option equal to $NA[L_m - FRA_0]t_m$ undiscounted.
> Correct: divide by $1 + D_m t_m$ because the payoff compensates for interest due only at T but is paid at h (V7 p.27).
> Distractors also use the wrong deposit tenor for $t_m$ (Practice Problem 20's 39,781 uses 180 days for a 90-day deposit) or a different rate for $D_m$ when the stem sets $D_m \ne L_m$ as in Example 8.

> [!warning] Trap 2: misreading the X x Y notation
> A "6 x 9" FRA question offers rates computed from the wrong pair of spot rates or annualized over the wrong period.
> Correct: expiry at 6 months ($L_h = L_{180}$), underlying 90-day rate maturing at 9 months ($L_T = L_{270}$), annualize by dividing by $t_m = 90/360$ (V7 p.25, p.29).
> Distractors annualize over $t_T$ instead of $t_m$ (Practice Problem 19's 0.61%) or, when valuing at g, rebuild $FRA_g$ from the original tenors instead of the shortened ones (Practice Problem 17's 19,647 uses today's 180- and 270-day rates instead of the 90- and 180-day rates).

> [!warning] Trap 3: clean versus full price and the missing $AI_T$
> A bond futures stem quotes a clean price, accrued interest at 0 and T, a conversion factor, and possibly an interim coupon.
> Correct: carry the full price forward, then subtract $AI_T$ and $FVCI$, then divide by CF: $Q_0 = [1/CF]\{\text{FV}[B_0 + AI_0] - AI_T - FVCI\}$ (V7 p.36).
> Distractors skip $AI_T$ (Practice Problem 3's 148.89), skip the fractional exponent on the FV (149.78), skip the 1/CF division, or hand you the dirty price and tempt you to add accrued interest a second time (Practice Problem 3 gives the dirty price 104.17 and the distractor path re-derives 104 + 0.17).

> [!warning] Trap 4: forward valuation with a phantom carry flow
> A seasoned equity forward is valued after a dividend has been announced or paid.
> Correct: rebuild the new forward price $F_t = \text{FV}(S_t + CC_t - CB_t)$ with only the carry flows remaining between t and T, then $V_t = \text{PV}[F_t - F_0]$ (V7 p.20).
> Distractors ignore the dividend entirely (Practice Problem 11's 5.1561 versus the correct 6.6549), skip the final discounting, or compute $S_t - F_0$ as if the contract expired today.

> [!warning] Trap 5: swap rate numerator and denominator surgery
> The swap-pricing table of PV factors invites three specific errors.
> Correct: $r_{FIX} = (1 - PV_n)/\sum PV_i \times 1/AP$, using the final PV factor in the numerator and all n factors (including the final one) in the sum (V7 p.45).
> Distractors use the first PV factor in the numerator (Practice Problem 5's 0.48%), drop the final factor from the sum (2.88%), divide by n instead of the sum (Practice Problem 12's 1.16%), or forget the $1/AP$ annualization on quarterly swaps (Practice Problem 14 answers 0.0624% periodic versus 0.2496% annualized, both offered).

> [!warning] Trap 6: whose swap value is it
> A swap valuation stem asks for the value "from the bank's perspective" after quoting the receive-fixed formula.
> Correct: compute $NA(FS_0 - FS_t)\sum PV_i$ over the remaining resets, then flip the sign if the party in question pays fixed (V7 p.46, p.47).
> Distractors present the correct magnitude with the wrong sign, replace $FS_t$ with an arithmetic average of spot rates (Practice Problem 6's 6,491,550), value with $FS_0$ alone (Practice Problem 13's 2,951,963), or skip the $\sum PV_i$ multiplication (994,793).

> [!warning] Trap 7: currency swap identification and translation
> The currency swap stem states the exchange rate one way (A\$1.14 per US\$1) and asks for value to a named party.
> Correct: currency a is the quote's numerator currency; $V_{CS}$ values the receiver of currency a, and the other party's value is $-V_{CS}$ converted at the current $S_t$ (V7 p.53, p.54).
> Distractors multiply instead of divide when solving $NA_b = NA_a/S_0$ (Example 15 offers 114m), quote the periodic swap rate where the annualized one is asked, or translate at $S_0$ instead of $S_t$.

> [!warning] Trap 8: equity swap resets and return conventions
> Equity swap questions mix an annualized fixed rate with a periodic equity return, or a seasoned valuation with the index level at initiation and at the last reset.
> Correct: never annualize the equity return; net $NA_E[R_E - AP \cdot r_{FIX}]$ per period, and in $V_{EQ,t}$ grow the notional by $S_t/S_{t-1}$ from the last reset (which is initiation only if no reset has passed) (V7 p.57, p.59).
> Distractors annualize the equity return (Example 17 shows 0.160 versus 0.040), forget that a negative equity return makes the equity receiver pay both legs, or drop the $-\text{PV}(\text{Par} - NA_E)$ test by reflex when Par $\ne NA_E$.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM01-Pricing-and-Valuation-of-Forward-Commitments-Practice-Problems]]

## Cross-links

- [[LM02-Valuation-of-Contingent-Claims]]: consumes this module's no-arbitrage toolkit; the binomial option lattice reuses the self-financed, fully hedged portfolio logic, and put-call-forward parity leans directly on $F_0 = \text{FV}(S_0)$.
- [[LM01-The-Term-Structure-and-Interest-Rate-Dynamics]]: supplies the spot and forward curve machinery; the FRA fixed rate is exactly that reading's implied forward rate restated in money-market (add-on, actual/360) convention, and swap PV factors are its discount factors.
- [[LM01-Currency-Exchange-Rates-Understanding-Equilibrium-Value]]: develops covered interest rate parity in full; here the same relation appears as the carry model with foreign interest as the carry benefit, and it underpins why currency swap pricing needs only the initial spot rate.
- [[LM01-Introduction-to-Commodities-and-Commodity-Derivatives]]: takes the carry cost side seriously; storage, insurance, and convenience yield generalize this module's $CC$ and $CB$ terms into commodity futures curves (contango, backwardation).

## Self-test

Vignette A for Q1 to Q4: A stock trades at 80.00 and will pay a 1.00 dividend in exactly three months.
The risk-free rate is 4% (annual compounding).
An analyst prices a six-month forward today, then revisits the position three months later, immediately after the dividend is paid, when the stock trades at 84.00.
Separately, she prices a 2 x 8 FRA off 60-day MRR of 2.40% and 240-day MRR of 3.00%, and later settles a \$30,000,000 pay-fixed position in that FRA when the 180-day MRR fixes at 3.30% (discount rate 3.30%).

> [!question] Q1
> The no-arbitrage six-month forward price at initiation is closest to:
> A. 80.57.
> B. 81.58.
> C. 82.59.

> [!question] Q2
> Three months later, the value of the long forward position is closest to:
> A. 3.43.
> B. 4.21.
> C. 4.25.

> [!question] Q3
> The 2 x 8 FRA fixed rate at initiation is closest to:
> A. 2.39%.
> B. 2.70%.
> C. 3.19%.

> [!question] Q4
> The settlement received by the pay-fixed party at FRA expiration is closest to:
> A. -$16,638.
> B. $16,638.
> C. $16,912.

Vignette B for Q5 to Q7: A trader analyzes a bond futures contract on a 4% semiannual bond quoted at 98.50, 36 days into the 180-day coupon period.
The futures expires in six months; at expiration the deliverable will have accrued interest of 0.10; a coupon paid during the contract's life will have a future value at expiration of 1.50; the six-month risk-free rate is 3% (annual compounding); the conversion factor is 0.92.
He also prices a three-year annual-reset interest rate swap from PV factors 0.980392 (1y), 0.955034 (2y), 0.928599 (3y).

> [!question] Q5
> The full price of the underlying bond is closest to:
> A. 98.50.
> B. 98.90.
> C. 100.10.

> [!question] Q6
> The equilibrium quoted futures price is closest to:
> A. 98.77.
> B. 107.36.
> C. 108.99.

> [!question] Q7
> The three-year swap's fixed rate is closest to:
> A. 0.68%.
> B. 2.38%.
> C. 2.49%.

Vignette C for Q8 to Q10: Two years ago a fund entered a four-year annual-reset receive-fixed swap at 2.80% on \$25,000,000.
The current two-year swap rate is 1.90% and the current PV factors are 0.985 (1y) and 0.966 (2y).
The fund also considers a fixed-for-fixed currency swap when the spot rate is 1.25 units of currency a per unit of currency b with a currency b notional of 40,000,000, and reviews a three-year annual-reset receive-fixed (2.4%), pay-equity swap on \$15,000,000 (Par equals notional) entered at the last reset with the index at 100; the index now trades at 108 and the curve is flat at 2% with money-market discounting, so the PV factors are 0.980392, 0.961538, 0.943396.

> [!question] Q8
> The value of the swap to the counterparty paying fixed is closest to:
> A. -$438,975.
> B. -$225,000.
> C. $438,975.

> [!question] Q9
> The notional amount in currency a for the currency swap is closest to:
> A. 32,000,000.
> B. 40,000,000.
> C. 50,000,000.

> [!question] Q10
> The value of the equity swap to the receive-fixed party is closest to:
> A. -$1,200,000.
> B. -$1,010,339.
> C. $1,010,339.

> [!success]- Answer key
> Q1: A.
> $F_0 = 80(1.04)^{0.5} - 1.00(1.04)^{0.25} = 81.5843 - 1.0099 = 80.5745$ (Python: 80.5745); B ignores the dividend (81.5843); C adds the dividend's future value instead of subtracting it (82.5942).
> Q2: B.
> With the dividend paid, $F_t = 84(1.04)^{0.25} = 84.8277$ and $V_t = (84.8277 - 80.5745)/(1.04)^{0.25} = 4.2117$ (Python: 4.2117); C skips the final discounting (4.2532); A is $S_t - F_0 = 3.4255$, which values the contract as if it expired today.
> Q3: C.
> $FRA_0 = \{[1 + 0.030(240/360)]/[1 + 0.024(60/360)] - 1\}/(180/360) = 3.1873\%$ (Python: 3.1873%); the weighted-average check $(60 \times 2.4 + 180 \times X)/240 = 3.0$ gives $X = 3.2\%$, and the true forward must sit just below that biased-high approximation (V7 p.30); A annualizes over 240 days (2.3904%); B is the arithmetic average of the two spot rates.
> Q4: B.
> Pay-fixed receives $30{,}000{,}000 \times (0.033 - 0.031873)(180/360)/[1 + 0.033(180/360)] = 16{,}638$ (Python: 16,637.83); C skips the advanced-settlement discounting (16,912); A flips the sign, but rates rose above the locked fixed rate, so the fixed payer must gain.
> Q5: B.
> $AI_0 = (36/180)(4/2) = 0.40$, so $S_0 = 98.50 + 0.40 = 98.90$; A is the clean price; C accrues over the remaining 144 days, $(144/180)(2) = 1.60$.
> Q6: B.
> $Q_0 = (1/0.92)[(1.03)^{0.5}(98.90) - 0.10 - 1.50] = (1/0.92)(98.7725) = 107.36$ (Python: 107.3615); A forgets the 1/CF division (98.77); C forgets to remove the coupon's future value (Python: 108.99).
> Q7: C.
> $\sum PV_i = 2.864025$; $r_{FIX} = (1 - 0.928599)/2.864025 = 2.4930\%$ (Python: 2.4930%); B divides by n = 3 (2.3800%); A uses the first PV factor in the numerator (0.6846%).
> Q8: A.
> Receive-fixed value $= 25{,}000{,}000 \times (0.028 - 0.019)(0.985 + 0.966) = 438{,}975$ (Python: 438,975); the pay-fixed party holds the negative, $-438{,}975$; C answers for the wrong party; B forgets the two-period annuity ($25\text{m} \times 0.009 = 225{,}000$).
> Q9: C.
> $NA_a = S_0 \times NA_b = 1.25 \times 40{,}000{,}000 = 50{,}000{,}000$ (Python: 50,000,000); A divides by the spot rate (32m), the classic direction error; B ignores the exchange rate entirely.
> Q10: B.
> $V_{FIX} = 360{,}000(0.980392 + 0.961538) + 15{,}360{,}000(0.943396) = 15{,}189{,}661$ (Python: 15,189,661); $V_{EQ,t} = 15{,}189{,}661 - (108/100)(15{,}000{,}000) - 0 = -1{,}010{,}339$ (Python: -1,010,339); A charges only the 8% equity gain ($-1{,}200{,}000$) and ignores the bond leg's repricing above par; C flips the sign, but the equity leg the party must pay grew faster than the fixed leg it holds.

## Flashcards

#flashcards/cfa-l2/07-Derivatives/lm01

Arbitrageur's two rules::Do not use your own money, and do not take any price risk (V7 p.4).
Law of one price (forward commitments)::Two investments with identical future cash flows in every state must have the same current price (V7 p.5).
Four standing assumptions of the carry models::Replicating instruments identifiable and investable, no market frictions, short selling with full use of proceeds, borrowing and lending at a known risk-free rate (V7 p.5).
Pricing versus valuation of a forward commitment::Pricing sets the fixed price or rate that makes initial value zero; valuation marks the existing contract to market afterward (V7 p.4).
Convergence property::{{F_T = f_T = S_T}} at expiration; the basis shrinks to zero as maturity nears (V7 p.7).
Value of a long forward at expiration::VT equals ST minus F0, the sale price minus the locked purchase price (V7 p.9).
Value of a futures contract after daily settlement::Zero; marking to market sweeps gains and losses into the margin account each day (V7 p.10).
Carry arbitrage price, no cash flows::F0 equals FV(S0), the spot price grown at the risk-free rate; expectations of ST never enter (V7 p.13, p.15).
Trade when the market forward price is too high::Carry arbitrage; sell the forward, borrow funds, buy the underlying (V7 p.13).
Trade when the market forward price is too low::Reverse carry arbitrage; buy the forward, short the underlying, lend the proceeds (V7 p.14).
Forward value before expiration (long)::Vt equals PV of (Ft minus F0), or equivalently St minus PV(F0) (V7 p.17).
Forward price with carry costs and benefits::{{F0 = FV(S0 + CC0 - CB0)}}; costs raise the forward price, benefits lower it (V7 p.18).
Dividend-paying stock forward price::F0 equals FV(S0) minus FV(D), with the dividend compounded only from its payment date to expiration (V7 p.19).
Continuous-compounding index futures price::F0 equals S0 times exp((rc + CC - CB)T), with the dividend yield as CB (V7 p.21).
When does a forward price converge to spot from below?::When carry benefits (dividends) exceed carry costs (financing), as for a high-yield index (V7 p.8).
Currency forward direction under covered interest parity::The higher-rate currency trades at a forward discount; the foreign rate is the carry benefit in F0 = S0 (1+rd)^T / (1+rf)^T (V7 p.18).
MRR deposit conventions::Add-on interest, actual/360; TA = NA times (1 + Lm tm) paid at maturity (V7 p.24).
What does 3 x 9 FRA mean?
?
The FRA expires in 3 months, the underlying deposit runs from month 3 to month 9, so the underlying is the 180-day MRR observed at expiration (V7 p.25).

Who is long an FRA and when does it gain?::The fixed payer and floating receiver; it gains when MRR rises above the locked rate (V7 p.25).
FRA settlement convention::Advanced set, advanced settled; the rate is set and paid at expiration h, with the payoff discounted by 1 + Dm tm (V7 p.26, p.27).
Why is the FRA payoff discounted?::The rate difference compensates for interest due at T = h + m but is paid early at h, where it can earn m days of interest (V7 p.27).
FRA fixed rate formula::{{FRA0 = ([1 + LT tT]/[1 + Lh th] - 1)/tm}}, the implied forward rate between the two spot MRRs (V7 p.29).
Quick sanity check on an FRA rate::The time-weighted average of Lh and FRA0 should roughly equal LT; the arithmetic-average shortcut is biased slightly high (V7 p.30).
FRA value at time g::NA times (FRAg - FRA0) tm, discounted at D(T-g) over T - g days; FRAg comes from the shortened tenors h - g and T - g (V7 p.31, p.32).
Accrued interest formula::AI = (NAD/NTD) times (C/n), in currency units; full price = clean price + AI (V7 p.33).
Conversion factor::Approximate price of one unit of par if the deliverable bond yielded 6%; standardizes the deliverable basket so F0 = Q0 x CF (V7 p.33, p.34).
Why does a cheapest-to-deliver bond exist?::The conversion factor adjustment is imprecise, so one deliverable bond is least expensive for the short to buy and deliver (V7 p.33).
Fixed-income futures price (adjusted)::F0 = Q0 x CF = FV(B0 + AI0 - PVCI); coupons over the contract's life are the carry benefit (V7 p.34, p.35).
Equilibrium quoted bond futures price
?
Q0 = (1/CF) x (FV(B0 + AI0) - AIT - FVCI); carry the full price forward, strip expiration accrued interest and coupon FV, divide by the conversion factor (V7 p.36).

30-second micro-problem: B0 108, AI0 0.083, AIT 0.25, r 0.1%, 1 month, CF 0.729535; Q0?::108.083 x 1.001^(1/12) = 108.092, minus 0.25 = 107.842, divided by 0.729535 = 147.82; keystrokes 108 + 0.083 = x 1.001 y^x (1 / 12) = - 0.25 = / 0.729535 = (V7 p.37).
Receive-fixed swap as bonds::Long a fixed-rate bond, short a floating-rate bond of equal par; Vswap = VFIX - VFLT (V7 p.43).
Why is a floating-rate bond worth par at reset?::Its coupon resets to its own discount rate, so it prices like a bond whose coupon equals its yield (V7 p.45).
Swap pricing equation::{{rFIX = (1 - PVn)/(sum of PVi) x 1/AP}}; the final PV factor appears in both numerator and the annuity sum (V7 p.45).
PV factor from a money-market spot rate::PVi(1) = 1/(1 + Rspot,i x NADi/NTD), simple add-on discounting (V7 p.44).
Seasoned interest rate swap value (receive-fixed)::NA times (FS0 - FSt) times the sum of current PV factors over the remaining resets (V7 p.46).
Which swap party gains when rates rise?::The pay-fixed (receive-floating) party; it is long a floater and short a fixed bond now trading at a discount (V7 p.46, p.47).
Three unknowns priced in a fixed-for-fixed currency swap::Two fixed rates, one from each currency's own curve, plus one notional set by NAa = S0 x NAb (V7 p.50, p.51).
Currency swap notional exchanges::Exchanged at initiation and again at maturity; periodic payments are in different currencies and are not netted (V7 p.48).
Seasoned currency swap value::VCS = value of the currency a bond minus St times the value of the currency b bond; it values the receiver of currency a (V7 p.53).
How to identify currency a in a swap problem?::It is the numerator currency of the quoted exchange rate, e.g. A$1.14 per US$1 makes A$ currency a (V7 p.53, p.54).
Equity swap fixed rate::Identical to the fixed rate on a comparable interest rate swap, because the replicating bond leg is the same (V7 p.59, p.60).
Equity swap periodic cash flow (receive-equity, pay-fixed)::NA times (RE - AP x rFIX), where RE is the periodic return, never annualized (V7 p.57).
What happens when the equity return is negative?::The receive-equity party pays both the equity decline and the fixed rate, creating liquidity risk (V7 p.58).
Seasoned equity swap value (receive-fixed, pay-equity)::{{VEQ,t = VFIX(C0) - (St/St-1) NAE - PV(Par - NAE)}}, with St-1 the price at the last reset (V7 p.59).
Index level that zeroes an equity swap::St = St-1 times VFIX per unit of notional; e.g. bond leg at 102.16% of notional gives St = 102.16 from 100 (V7 p.61).
30-second micro-problem: receive-fixed 2.0% swap, new rate 1.3%, 5 annual resets left, sum PV 4.822107, NA 100m; value?::100m x (0.020 - 0.013) x 4.822107 = 3,375,000; keystrokes 0.02 - 0.013 = x 4.822107 = x 100000000 = (V7 p.48).
The trap answer that skips 1 + Dm tm in an FRA problem signals what?::Forgetting that advanced-settled payoffs must be discounted from T back to h (V7 p.27).
Futures versus forward pricing in this module::Prices are treated as the same; only values differ, because futures values reset to zero at each daily settlement (V7 p.7, p.39).

## Common mistakes

1. Forgetting the FRA settlement discount factor $1 + D_m t_m$, or discounting a seasoned FRA over m days instead of T - g days (V7 p.27, p.31).
2. Misreading X x Y: using the wrong spot-rate pair, or annualizing the forward ratio over the total period $t_T$ instead of the underlying's $t_m$, as in the 0.61% and 0.73% distractors of Practice Problems 18 and 19 (V7 p.25, p.79, p.80).
3. Rebuilding $FRA_g$ from the original tenors when valuing a seasoned FRA instead of the shortened h - g and T - g tenors (V7 p.31, p.79).
4. Adding accrued interest twice (when the dirty price is given) or not at all (when the clean price is given); always form $S_0 = B_0 + AI_0$ once (V7 p.33, p.73).
5. Dropping $AI_T$ or $FVCI$ from the quoted futures price, or forgetting the 1/CF division entirely (V7 p.36, p.73).
6. Skipping the fractional exponent on the future value factor, compounding a full year for a three-month contract (V7 p.74).
7. Ignoring an announced dividend when rebuilding $F_t$ for forward valuation, the 5.1561 trap in Practice Problem 11 (V7 p.20, p.76).
8. Using the first PV factor in the swap-rate numerator, excluding the final PV factor from the annuity sum, or dividing by n instead of the sum (V7 p.45, p.75, p.77).
9. Forgetting the $1/AP$ annualization on quarterly swaps, or reporting a periodic rate where an annualized rate is asked (V7 p.45, p.77).
10. Valuing a seasoned swap with the original fixed rate alone, with an arithmetic average of spot rates, or without multiplying by $\sum PV_i$ (V7 p.75, p.77).
11. Reporting the swap value with the wrong sign for the party named in the question; compute receive-fixed first, then negate for pay-fixed (V7 p.47).
12. Solving $NA_a = S_0 NA_b$ in the wrong direction, or translating a currency swap value at $S_0$ instead of the current $S_t$ (V7 p.50, p.53).
13. Annualizing the equity return in an equity swap, or growing the equity leg from initiation instead of the last reset in $S_t/S_{t-1}$ (V7 p.57, p.59).
14. Treating a futures position like a forward when asked for value: after the daily mark to market, the futures value is zero (V7 p.10, p.24).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "07-01" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
