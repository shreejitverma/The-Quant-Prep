---
type: cfa-lm
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
volume: 6
lm: 5
title: "Credit Default Swaps"
pages: "275-308"
weight_band: "10-15%"
difficulty: 2
los_count: 5
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/fixed-income]
---

# LM5: Credit Default Swaps

Difficulty 2 of 5: the arithmetic is one-step multiplication, but the module is dense with direction conventions (buyer versus seller, single-name versus index, steepener versus flattener, negative versus positive basis) that the exam tests by flipping signs, so the risk is a wrong direction, not a hard calculation.

## LOS map

- **describe** credit default swaps (CDS), single-name and index CDS, and the parameters that define a given CDS product (V6 p.275) ^los-06-05-a
    - Examiner asks: identify the cheapest-to-deliver obligation among bonds of mixed seniority, compute the per-entity notional of an equally weighted index CDS, or pick which contract feature (notional, maturity, standardized 1% or 5% coupon, reference obligation) a vignette statement describes.
- **describe** credit events and settlement protocols with respect to CDS (V6 p.275) ^los-06-05-b
    - Examiner asks: decide whether a described event (missed coupon after a grace period, US restructuring, bankruptcy filing) triggers the CDS, then compute the cash payout as (1 - recovery rate) x notional and state whether the holder should prefer cash or physical settlement given the bond he actually owns.
- **explain** the principles underlying and factors that influence the market's pricing of CDS (V6 p.275) ^los-06-05-c
    - Examiner asks: chain hazard rates into a survival probability and a lifetime probability of default, approximate the upfront premium as (credit spread - fixed coupon) x duration, convert it to a price per 100 par, or read a curve shape (upward, flat, inverted) into a statement about when default is expected.
- **describe** the use of CDS to manage credit exposures and to express views regarding changes in the shape and/or level of the credit curve (V6 p.275) ^los-06-05-d
    - Examiner asks: build the long/short or curve trade that matches a stated macro or ESG view (which name to buy protection on, which to sell), or compute the profit on an unwound position as change in spread x duration x notional with the correct sign for the protection buyer or seller.
- **describe** the use of CDS to take advantage of valuation disparities among separate markets, such as bonds, loans, equities, and equity-linked instruments (V6 p.275) ^los-06-05-e
    - Examiner asks: compute the bond's credit spread as yield minus MRR, compare it with the CDS spread, label the basis negative or positive, state the two legs of the basis trade, and give the profit captured on convergence.

## Core intuition

A credit derivative is a derivative whose underlying is a measure of a borrower's credit quality, and of the four types (total return swaps, credit spread options, credit-linked notes, credit default swaps) the CDS is by far the most liquid and the only one that matters here (V6 p.276).
A credit default swap is a contract between a credit protection buyer and a credit protection seller in which the buyer makes a series of cash payments to the seller and receives a promise of compensation for credit losses resulting from a credit event in an underlying (V6 p.276).
The economics are those of insurance written on someone else's debt: the buyer pays premiums, and if the reference entity suffers a defined credit event, the seller pays the buyer roughly the loss a creditor would suffer.
Structurally, though, a CDS behaves like a put option on the borrower's credit standing, because the seller's payment is contingent and the contract's market value moves continuously with the market's opinion of default likelihood and severity long before any default happens (V6 p.277, p.285).
A CDS does not eliminate credit risk; it transfers it, leaves a residual mismatch between the contract's definition of default and economic default, and substitutes counterparty risk on the protection seller (V6 p.277).

> [!abstract] Idea 1: the buyer of single-name protection is short the credit
> In single-name CDS the protection buyer is short credit exposure and the seller is long credit exposure, because shorts profit when things go badly: spreads widen, the promised protection becomes more valuable, and the buyer gains (V6 p.280).
> The convention flips for index products, where the buyer of a CDX is long credit exposure and the seller is short, which is why the curriculum (and a safe candidate) speaks only of buying protection and selling protection (V6 p.280, p.283).
> Every valuation, unwind, and strategy question in this module is at bottom a question about which side of this table you are on.

| Position | Credit exposure | Gains when | Analogous cash position |
| --- | --- | --- | --- |
| Protection buyer (single-name CDS) | Short | Spreads widen, credit deteriorates | Short the bond (V6 p.291) |
| Protection seller (single-name CDS) | Long | Spreads narrow, credit improves | Long the bond (V6 p.291) |
| Buyer of a CDX index | Long | Spreads narrow | Long a bond portfolio (V6 p.280) |
| Seller of a CDX index | Short | Spreads widen | Short a bond portfolio (V6 p.280) |

There are three product types (V6 p.277, p.278).
A single-name CDS references one borrower (the reference entity) and one designated debt issue (the reference obligation), usually a senior unsecured bond; the contract actually covers every obligation of equal or higher seniority, and the payoff is set by the cheapest-to-deliver obligation of the covered set (V6 p.277).
An index CDS is a portfolio of single-name CDS that trades in size because it is standardized: CDX for North America and iTraxx for Europe, Asia, and Australia, split into investment-grade (CDX IG and iTraxx Main, 125 entities each) and high-yield (CDX HY with 100, iTraxx Crossover with up to 75) (V6 p.278, p.282).
All indexes are equally weighted, so one default settles as a single-name CDS on 1/125 (or 1/100) of the notional and the index rolls forward with a smaller notional; Markit creates a new on-the-run series every six months (V6 p.282, p.283).
Credit correlation is the key pricing input unique to the index product: the more correlated the constituents' defaults, the more protection on the combination costs (V6 p.278).
Tranche CDS, which cover losses only up to pre-specified levels, are named and then excluded from the reading (V6 p.278).

The market runs on ISDA plumbing (V6 p.278, p.279).
Parties sign the ISDA Master Agreement, and standard contracts exist by region (Standard North American Contract, Standard Europe Contract) (V6 p.278, p.279).
Each contract specifies a notional amount, the size of protection purchased, which can exceed the entity's outstanding debt because buyers need not be creditors at all (V6 p.279).
Maturities run 1 to 10 years with 5 years most liquid, and maturity dates fall on the 20th of March, June, September, and December, with March and September the roll dates (V6 p.279).
The buyer's periodic payment rate is the CDS spread, conceptually the same compensation for bearing credit risk as a bond's credit spread (V6 p.279).

> [!abstract] Idea 2: standardized coupons make the upfront premium the price of credit
> Coupons on CDS are standardized at 1% for investment-grade and 5% for high-yield reference entities, so the running payment almost never equals the credit spread the risk deserves (V6 p.279).
> The difference is settled at initiation as an upfront premium: present value of (credit spread - fixed coupon), paid by the buyer when the spread exceeds the coupon and paid by the seller when the coupon exceeds the spread (V6 p.279, p.289).
> Everything the exam asks about CDS pricing (upfront premium, price per 100, mark-to-market profit) is this one present-value wedge, approximated as a spread difference times an effective spread duration.

A credit event is what makes the seller pay, and it must be unambiguous (V6 p.280).
The three common events are bankruptcy (a legal filing that freezes creditor claims while the firm reorganizes), failure to pay (a missed scheduled principal or interest payment after the grace period, with no bankruptcy filing needed), and restructuring (reduction or deferral of principal or interest, change in seniority, or change of currency, but only when involuntary or coercive) (V6 p.280).
Restructuring is not a credit event in the United States, where issuers restructure through bankruptcy; it is recognized in jurisdictions where bankruptcy reorganization is less common, the Greek sovereign restructuring being the standard example (V6 p.280).
Sovereign and municipal contracts can add a moratorium or repudiation of debt as events (V6 p.276).
Whether an event occurred is decided by a regional 15-member ISDA Determinations Committee of 10 sell-side and 5 buy-side members, and declaring a credit event requires a supermajority of 12 (V6 p.280).
The same committees rule on succession events, corporate reorganizations (mergers, spinoffs, divestitures) that leave it unclear who owes the referenced debt, and the CDS can be modified or even split across successor entities (V6 p.281).

Settlement follows about 30 days after the DC declaration, and the parties have the right but not the obligation to settle (V6 p.281).
Physical settlement is the rarer route: the buyer delivers a covered debt instrument and receives the full notional (V6 p.281).
Cash settlement pays the buyer the loss given default, where LGD = 1 - recovery rate, so the payout amount is (1 - RR) x notional (V6 p.281).
Because actual recovery takes years, the market's recovery estimate is set by an auction in which major dealers bid for the cheapest-to-deliver defaulted debt, and both parties accept the auction outcome even though realized recovery can differ (V6 p.281).
The cheapest-to-deliver logic creates the classic settlement-preference question: a holder of the cheapest deliverable is indifferent between settlement methods, while a holder of any richer covered bond prefers cash, because he collects the same CDS payout and sells his bond for more than the auction price implies (V6 p.281, p.282).

Pricing rests on the same expected-loss machinery as the credit models module (V6 p.285).
The credit valuation adjustment is the present value of credit risk: expected exposure times (1 - RR) gives LGD, LGD times the probability of default gives expected loss, and CVA is the sum of discounted expected losses (V6 p.285).
For a one-period CDS, ignoring discounting, the fair spread is approximately (1 - RR) x POD; a 2% default probability with 60% recovery prices at 80 bps (V6 p.286).
The POD is conditional: the probability of defaulting in period two assumes survival through period one, and this conditional default probability is the hazard rate (V6 p.286).
Survival over a horizon is the product of one minus each period's hazard rate, and lifetime POD is one minus that product, which is how a modest 2% annual hazard compounds into an 18.3% ten-year default probability (V6 p.286).

> [!abstract] Idea 3: a CDS is two legs, and the upfront payment is the difference in their present values
> The protection leg is the contingent payment the seller may have to make (discounted expected losses on the reference obligation), and the premium leg is the stream of standardized coupons the buyer promises, each contingent on survival (V6 p.287).
> Upfront payment = PV(protection leg) - PV(premium leg); if positive the buyer pays the seller, if negative the seller pays the buyer (V6 p.288).
> Real models are more mathematical, but every exam number comes from the industry shortcut: upfront premium roughly equals (credit spread - fixed coupon) x effective spread duration, and price per 100 par = 100 - upfront premium% (V6 p.288, p.289).

The credit curve is the set of the borrower's credit spreads across maturities, analogous to the term structure of interest rates, and in practice CDS rates determine it (V6 p.288).
A constant hazard rate gives a roughly flat curve (not exactly flat, because discounting still differs across maturities); upward-sloping curves mean default is more likely in later years; downward-sloping curves mean near-term distress and are rare (V6 p.288).
Spreads, not prices, carry the information, exactly as with bonds: investment-grade index CDS quote in spread terms and high-yield index CDS quote in price terms, but both describe the same object (V6 p.282, p.289).
Duration matters because the coupon leg's cash flows are contingent on survival, so the sensitivity measure is an effective spread duration, and it shortens as the CDS ages (V6 p.289, p.290).

Value moves over the CDS's life exactly as at initiation, just with new inputs (V6 p.290).
If credit quality deteriorates, the buyer paying a fixed coupon holds protection now worth more, so the buyer gains and the seller loses; improvement reverses the signs (V6 p.279, p.290).
The buyer's mark-to-market profit is approximately the spread change in bps times duration times notional, and the percentage price change is spread change times duration (V6 p.291).
Gains and losses are monetized in three ways: exercise on default, unwind by entering an offsetting CDS at the now-prevailing upfront premium (the usual route, eased by central clearing), or hold to expiration as the spread converges to zero the way a bond pulls to par (V6 p.291, p.292).

Applications split into managing credit exposures and exploiting valuation disparities (V6 p.292, p.293).
Lenders buy protection to shed risk temporarily without selling illiquid loans; bondholders who want credit risk without interest rate risk sell protection instead of buying bonds; dealers sell protection and hedge (V6 p.293).
A naked CDS position, protection bought with no exposure to the reference entity, is a pure bet on deterioration; it is controversial, banned in Europe for sovereign debt, but defended as no different from puts or short sales and as a source of liquidity (V6 p.293, p.294).
A long/short credit trade sells protection on one name and buys protection on another, betting on relative improvement, including on ESG grounds (buy protection on the weak-ESG name, sell on the strong) (V6 p.294).
A curve trade is a long/short across maturities of the same name: expecting steepening (long-term risk rising relative to short-term), buy long-term protection and sell short-term protection; a steepener is near-term bullish, a flattener near-term bearish (V6 p.295, p.296).
For parallel level shifts, longer-term CDS move more, so a trader expecting spreads to rise everywhere buys long-dated protection and can hedge with short-dated sales, sizing the legs by volatility (V6 p.296, p.297).

The basis trade exploits the fact that credit risk on the same borrower is priced twice, once in the bond's yield and once in the CDS spread (V6 p.297).
Decompose the bond yield into MRR (risk-free plus funding spread) plus the credit spread; if the bond's credit spread exceeds the CDS spread the basis is negative, and if the CDS spread is higher the basis is positive (V6 p.297, p.298).
With a negative basis, buy the bond (credit is cheap there, price too low) and buy CDS protection (protection is cheap), hedge rates with duration tools, and collect the differential if the two spreads converge (V6 p.297, p.298).
The same convergence logic drives capital-structure trades within one issuer (priority of claims makes them harder), equity-versus-credit trades such as buying stock and buying protection ahead of an LBO that levers the firm, and index arbitrage between an index and its components, where transaction costs eat most of the profit (V6 p.298, p.299).

## Formulas and derivations

**1. Loss given default** (V6 p.281)
$$
\text{LGD} = 1 - \text{RR}
$$
^f-06-05-1

- $\text{RR}$: recovery rate, the percentage of the loss recovered in default, set for settlement by the dealer auction; $\text{LGD}$: loss given default as a percentage, the expected credit loss per unit of notional.
- Recovery applies to principal in most models, and whatever is not recovered is by definition lost, so the two shares must sum to one (V6 p.281).
- As a percentage of notional this LGD is also called the payout ratio, the fraction of notional the seller pays on a credit event.

**2. Payout amount on a credit event** (V6 p.281)
$$
\text{Payout amount} = \text{LGD} \times \text{Notional} = (1 - \text{RR}) \times \text{Notional}
$$
^f-06-05-2

- Notional: the amount of protection purchased, in currency; the payout is what the seller pays the buyer in cash settlement.
- The auction price of the cheapest-to-deliver defaulted debt fixes RR, so the payout equals the market's estimate of the creditor's loss (V6 p.281).
- Physical settlement pays the full notional against delivery of the debt, which is the same economics when the delivered bond is worth RR x notional.

**3. Per-entity exposure of an equally weighted index CDS** (V6 p.282)
$$
\text{Per-entity notional} = \frac{\text{Index notional}}{N}
$$
^f-06-05-3

- $N$: number of index constituents (125 for CDX IG and iTraxx Main, 100 for CDX HY, up to 75 for iTraxx Crossover).
- All CDS indexes are equally weighted, so a constituent default settles as a single-name CDS on notional/$N$ and the index continues with the remaining notional (V6 p.282, p.283).

**4. Credit valuation adjustment (expected-loss chain)** (V6 p.285)
$$
\text{EE} \times (1-\text{RR}) = \text{LGD}, \qquad \text{LGD} \times \text{POD} = \text{EL}, \qquad \text{CVA} = \sum \text{PV}(\text{EL})
$$
^f-06-05-4

- $\text{EE}$: expected exposure, the total projected exposure at default (the notional for a CDS); $\text{POD}$: conditional probability of default assuming no earlier default; $\text{EL}$: expected loss; discounting is at the risk-free rate.
- CVA is the present value of credit risk, so it approximates what a fully offsetting CDS hedge should cost, which is why it anchors CDS pricing (V6 p.285).

**5. One-period CDS spread approximation** (V6 p.286)
$$
\text{CDS spread} \approx (1 - \text{RR}) \times \text{POD}
$$
^f-06-05-5

- One-period contract, no upfront payment, time value ignored, default only at maturity.
- The seller's expected payout per unit notional is LGD x POD, and a fair premium must equal expected loss, so the spread is the expected-loss rate: 2% POD with 60% recovery gives 0.40 x 0.02 = 80 bps (V6 p.286).

**6. Survival and lifetime default probability from hazard rates** (V6 p.286)
$$
\text{POS} = \prod_{t=1}^{T} (1 - h_t), \qquad \text{POD}_{\text{life}} = 1 - \text{POS}
$$
^f-06-05-6

- $h_t$: hazard rate for period $t$, the conditional probability of default in $t$ given survival to $t$; $\text{POS}$: probability of survival through $T$.
- Each period's survival is conditional on all earlier survivals, so probabilities multiply; a constant 2% annual hazard gives $0.98^{10} = 0.817$ ten-year survival and an 18.3% lifetime POD (V6 p.286).
- Small per-period hazards compound into large lifetime PODs, the module's own warning (V6 p.286).

> [!tip] Calculator
> Lifetime POD from hazard rates 0.22%, 0.35%, 0.50%: `.9978 x .9965 x .995 =` displays 0.98934, then `+/- + 1 =` gives 0.01066, about 1.07%.
> For a constant hazard: `.98 y^x 10 =` gives 0.8171, so POD is 18.29%.

**7. Upfront payment as the difference of the two legs** (V6 p.288)
$$
\text{Upfront payment} = \text{PV}(\text{Protection leg}) - \text{PV}(\text{Premium leg})
$$
^f-06-05-7

- Protection leg: $\sum \text{PV}(\text{EL})$ on the reference obligation, the seller's contingent liability; premium leg: $\sum \text{PV}(\text{contingent coupon payments})$, each coupon weighted by survival (V6 p.287).
- If the result is positive the protection buyer pays the seller; if negative the seller pays the buyer (V6 p.288).
- This is the exact statement of which the spread-times-duration formula below is the industry approximation.

**8. Present value of the credit spread split into upfront and coupon** (V6 p.289)
$$
\text{PV}(\text{Credit spread}) = \text{Upfront premium} + \text{PV}(\text{Fixed coupon})
$$
^f-06-05-8

- The reference entity's true credit spread rarely equals the standardized 1% or 5% coupon, so the running coupon plus the upfront settlement together deliver the full spread's value (V6 p.289).
- Rearranged per year of duration: credit spread = fixed coupon + upfront premium% / duration, the form used to back a spread out of a quoted upfront (V6 p.290).

**9. Upfront premium approximation** (V6 p.289)
$$
\text{Upfront premium} \approx (\text{Credit spread} - \text{Fixed coupon}) \times \text{EffSpreadDur}_{CDS}
$$
^f-06-05-9

- Spread and coupon in decimal or bps per year; EffSpreadDur: the CDS's effective spread duration in years, effective because coupon-leg cash flows are contingent on survival (V6 p.289).
- Each year of the contract the buyer underpays or overpays by (spread - coupon), and duration converts that annuity of differences into a present value, signed from the buyer's viewpoint: positive means the buyer pays (V6 p.289).

> [!tip] Calculator
> Upfront premium for a 700 bps spread, 5% coupon, 7-year duration: `.07 - .05 = x 7 =` gives 0.14, so the buyer pays 14% of notional.
> Backing out a spread from a -2% upfront over duration 4: `2 +/- / 4 = + 1 =` in percent terms gives 0.5%, i.e. 100 bps coupon - 50 bps = 50 bps spread.

**10. Price of a CDS per 100 par** (V6 p.289)
$$
\text{Price of CDS per 100 par} = 100 - \text{Upfront premium \%}
$$
^f-06-05-10

- Quoting convention that converts the upfront into a price; a positive upfront (buyer pays) gives a price below 100, and a negative upfront (seller pays) gives a price above 100, e.g. 100 - (-2) = 102 (V6 p.289, p.290).
- High-yield index CDS are quoted this way, investment-grade in spread terms, but the two quotes carry the same information (V6 p.282).

**11. Profit or loss for the protection buyer** (V6 p.291)
$$
\text{Profit}_{\text{buyer}} \approx \Delta \text{Spread (bps)} \times \text{EffSpreadDur}_{CDS} \times \text{Notional}
$$
^f-06-05-11

- $\Delta$Spread: spread change in bps (converted to decimal), positive when spreads widen; the seller's profit is the negative of the buyer's.
- The buyer is short credit, so widening raises the value of protection bought at the old spread; the duration scales the annuity of spread improvement into value, exactly as modified duration scales a bond's yield change (V6 p.291).

**12. Percentage change in CDS price** (V6 p.291)
$$
\%\Delta \text{CDS price} = \Delta \text{Spread (bps)} \times \text{EffSpreadDur}_{CDS}
$$
^f-06-05-12

- Same logic per 100 of notional: a 300 bps widening on a duration-4 CDS moves the price about 12% (V6 p.291).
- Multiply by notional to get the currency profit in formula 11.

> [!tip] Calculator
> Spread widens 500 to 800 bps, duration 4, $10 million notional: `.03 x 4 = x 10,000,000 =` gives $1,200,000 profit to the buyer.

**13. Bond credit spread and the CDS-bond basis** (V6 p.297, p.298)
$$
\text{Bond credit spread} = \text{Bond yield} - \text{MRR}, \qquad \text{Basis} = \text{CDS spread} - \text{Bond credit spread}
$$
^f-06-05-13

- MRR: market reference rate, the risk-free rate plus the funding spread; both spreads price the same borrower's credit risk in different markets (V6 p.297).
- Negative basis: spread higher in the bond market than in the CDS market; positive basis: spread higher in the CDS market (V6 p.298).
- Negative-basis trade: buy the bond and buy CDS protection (both legs are where credit is cheap to buy), hedge interest rate risk, and earn the differential on convergence; embedded options or prices far from par complicate the decomposition (V6 p.297, p.298).

## Worked examples

**Example 1: Cheapest-to-Deliver Obligation** (V6 p.278)
A bankrupt company has several issues trading; the CDS reference bond is a five-year senior unsecured bond.
Choices: a subordinated unsecured bond at 20% of par, a five-year senior unsecured bond at 50%, a two-year senior unsecured bond at 45%.
The CDS covers only obligations ranked equal to or higher than the reference obligation, so the subordinated bond at 20 does not qualify despite its lowest price.
Among the qualifying senior unsecured bonds, the lowest-priced is the two-year at 45% of par, so it is the cheapest to deliver (answer C).
The holder receives payment based on this cheapest-to-deliver bond even if he owns the five-year issue. ^ex-06-05-1

**Example 2: Settlement Preference** (V6 p.281, p.282)
A French company goes bankrupt with two senior bond series: Bond A at 30% of par, Bond B at 40%.
Investor X owns EUR 10 million of Bond A and EUR 10 million of CDS protection; Investor Y owns EUR 10 million of Bond B and the same protection.
1. Recovery rate: Bond A is the cheapest-to-deliver senior obligation at 30% of par, so RR = 30% for both contracts.
2. Investor X is indifferent.
Cash: payout = (1 - 0.30) x EUR 10m = EUR 7m, plus sale of Bond A at 30 for EUR 3m, total EUR 10m (Python: 0.70 x 10 = 7).
Physical: deliver the full EUR 10m face and receive EUR 10m.
Both routes give EUR 10m.
3. Investor Y prefers cash settlement.
Cash: the same EUR 7m payout, plus sale of Bond B at 40 for EUR 4m, total EUR 11m.
Physical: delivering Bond B brings only the EUR 10m notional.
Owning a bond richer than the cheapest to deliver makes cash settlement worth EUR 1m more. ^ex-06-05-2

**Example 3: Hedging and Exposure Using Index CDS** (V6 p.283)
An investor sells $500 million of protection on the 125-name CDX IG, then buys $3 million of single-name protection on constituent Company A, which defaults.
1. Net notional exposure to Company A: long $500m/125 = $4m through the index, short $3m through the single-name hedge, net long $1m (Python: 500/125 = 4).
2. Proportion hedged: $3m of $4m = 75%.
3. Remaining index notional: $500m - $4m = $496m, since the defaulted name settles and leaves the index. ^ex-06-05-3

**Example 4: Hazard Rate and Probability of Survival** (V6 p.286, p.287)
A company's hazard rate is a constant 8% per year, 2% per quarter; an investor sells five-year protection with quarterly premiums.
1. Probability of survival for the first quarter: 100% - 2% = 98%.
2. Conditional probability of survival for the second quarter: also 98%, because the hazard rate is constant; conditional on surviving quarter one, default probability in quarter two is 2%.
3. Probability of survival through the second quarter: 0.98 x 0.98 = 96.04% (Python: 0.9604).
Equivalently, 1 - 96.04% = 3.96% is the probability of default at some point during the first two quarters. ^ex-06-05-4

**Example 5: Change in Credit Curve** (V6 p.288, p.289)
A company's 5-year CDS trades at 300 bps and its 10-year CDS at 500 bps, an upward-sloping curve.
1. The 10-year spread widens 100 bps with the 5-year unchanged: near-term risk is unchanged but long-term creditworthiness has deteriorated, e.g. adequate liquidity now but repayment pressure after year five.
2. The 5-year spread widens 500 bps with the 10-year unchanged: near-term risk has jumped, and the conditional probability of default actually falls if the firm survives five years, the signature of a liquidity crisis that either resolves or kills the company soon. ^ex-06-05-5

**Example 6: Premiums and Credit Spreads** (V6 p.290)
1. High-yield company, 10-year credit spread 600 bps, CDS duration 8 years, high-yield fixed coupon 5%.
Upfront premium to buy protection = (600 - 500) bps x 8 = 100 bps x 8 = 8% of notional (Python: 0.01 x 8 = 0.08).
The buyer pays the 500 bps running coupon plus 8% upfront.
2. Investment-grade company: an investor sells five-year protection and pays a 2% upfront premium to the buyer; duration is 4.
Per-year value of the upfront: -2% / 4 = -50 bps (negative because the seller pays).
Credit spread = fixed coupon + amortized upfront = 100 bps - 50 bps = 50 bps (Python: -0.02/4 = -0.005).
Price per 100 par = 100 - upfront premium% = 100 - (-2) = 102.
The seller pays upfront precisely because the spread (50 bps) is below the standardized 100 bps coupon. ^ex-06-05-6

**Example 7: Profit and Loss from Change in Credit Spread** (V6 p.291)
An investor buys $10 million of five-year protection with duration 4; the spread widens from 500 bps to 800 bps.
1. The buyer benefits: she is short credit, and widening spreads make the protection she owns more valuable.
2. Percentage price change = 300 bps x 4 = 12%.
Profit = 12% x $10m = $1.2 million (Python: 0.03 x 4 x 10,000,000 = 1,200,000). ^ex-06-05-7

**Example 8: Long/Short Trade with ESG Considerations** (V6 p.294, p.295)
Two US apparel companies: Atelier (large, profitable, strong governance, signed the fire-safety accord after a supplier factory fire) and Trapp (smaller, less profitable, founder-controlled board with minimal industry expertise, did not sign).
Pre-fire five-year CDS spreads: Atelier 150 bps, Trapp 250 bps; after the fire they widen to 210 bps and 325 bps.
The analyst expects Atelier to recover to 150 bps but Trapp to stay above its pre-fire 250 bps because of its weaker safety practices and governance.
Trade: buy protection on Trapp (short the weak-ESG credit) and sell protection on Atelier (long the strong-ESG credit).
If Atelier returns to 150 bps and Trapp narrows only to 300 bps, the spread differential widens from 325 - 210 = 115 bps to 300 - 150 = 150 bps (Python: 115, 150).
The 35 bps of relative widening is the trade's profit before costs. ^ex-06-05-8

**Example 9: Curve Trading** (V6 p.296)
An investor owns intermediate-term bonds of a company and fears near-term default but not long-term default; two-year CDS trades at 350 bps, four-year at 600 bps.
1. He expects the curve to flatten with short-end spreads rising, so he buys protection on the two-year CDS and sells protection on the four-year CDS.
2. The short leg's premium income offsets the cost of the near-term protection, making the hedge cheaper than buying protection outright; the saving survives only if the relative view (near-term risk, long-term calm) proves right. ^ex-06-05-9

**Example 10: Bonds vs. Credit Default Swaps** (V6 p.298)
An investor wants long credit exposure; the company's five-year bond yields 6%, the five-year CDS spread is 3.25%, and MRR is 2.5%.
1. Bond credit spread = 6% - 2.5% = 3.5% (Python: 0.035).
2. Credit is cheap in the CDS market (3.25%) relative to the bond market (3.5%), a negative basis of -25 bps.
Basis trade: buy the bond (earn the rich 3.5% spread) and buy CDS protection (pay the cheap 3.25%), netting 25 bps with default risk hedged (Python: 0.0025). ^ex-06-05-10

**Example 11: Using CDS to Trade on a Leveraged Buyout** (V6 p.298, p.299)
An investor expects a company to undergo an LBO, issuing large amounts of debt to repurchase all public equity.
1. The CDS spread should widen: the added leverage raises the probability of default.
2. Equity-versus-credit trade: buy the stock and buy CDS protection.
Both legs win if the LBO happens, the stock through the buyout premium and the CDS through the spread widening. ^ex-06-05-11

## Item-set patterns

> [!warning] Trap 1: who gains when spreads move
> The vignette moves a spread and asks which counterparty profits, or has an investor "sell protection" and then asks the effect of widening.
> Correct: the single-name protection buyer is short credit and gains on widening; the seller is long credit and gains on narrowing; for index products the buyer of the CDX is long credit (V6 p.280, p.291).
> Distractors flip the sign or apply bond-market long/short intuition to a single-name CDS; the "seller gains on widening" option tempts anyone who thinks of the seller as collecting a bigger coupon.

> [!warning] Trap 2: upfront premium arithmetic
> Exhibit gives credit spread, standardized coupon, and duration, and asks for the upfront premium.
> Correct: (spread - coupon) x duration, e.g. (700 - 500) bps x 7 = 14% (V6 p.289).
> Distractors are the raw difference with no duration (2%) and a ratio-based number such as (700/500) x 7 = 9.8%, both taken straight from the official solution's incorrect choices (V6 p.306).

> [!warning] Trap 3: who pays the upfront, and the price above 100
> A spread below the standardized coupon appears (e.g. 50 bps versus a 1% coupon) and the question asks who pays whom or what the price per 100 is.
> Correct: spread < coupon means the seller pays the buyer upfront, the upfront premium % is negative, and price = 100 - (negative) > 100, e.g. 102 (V6 p.289, p.290).
> Distractors keep the buyer as payer regardless, or subtract the absolute premium to get 98, which is why remembering price = 100 - upfront% with its sign matters.

> [!warning] Trap 4: settlement preference and the cheapest to deliver
> The holder owns one bond, several deliverables trade at different prices, and the question asks cash versus physical.
> Correct: the payout rides on the cheapest-to-deliver covered obligation; a holder of exactly that bond is indifferent, a holder of any higher-priced covered bond prefers cash (same payout plus a richer bond sale) (V6 p.281, p.282).
> Distractors include the subordinated bond as the CTD (it is not covered when the reference obligation is senior unsecured) and "indifferent" for a holder whose bond trades above the CTD price (V6 p.278, p.306).

> [!warning] Trap 5: is it a credit event?
> A borrower misses a payment on some obligation, or restructures, and the question asks whether the CDS triggers.
> Correct: failure to pay after the grace period is a credit event with no bankruptcy filing needed, on any outstanding obligation; restructuring counts only where recognized (not in the United States) and only if involuntary or coercive; the DC declares the event by a 12-of-15 supermajority (V6 p.280).
> Distractors require a bankruptcy filing or argue the missed payment was on a subordinated bond; deliverability into settlement is restricted by seniority, but the failure-to-pay trigger is not (V6 p.306).

> [!warning] Trap 6: hazard rates add instead of multiply
> A table of per-year hazard rates is given and the question asks the probability of default over several years.
> Correct: multiply survivals, POS = product of (1 - h_t), then POD = 1 - POS, e.g. 0.9978 x 0.9965 x 0.9950 = 0.9893, POD = 1.07% (V6 p.286, p.307).
> The tempting distractor sums hazard rates over the wrong horizon (adding all five years' rates gives 2.52%, the exam's 2.50% choice) or quotes the survival probability itself; the sum of the correct three hazard rates lands close to the right answer here only because the rates are tiny, so the products barely differ from the sums (V6 p.307).

> [!warning] Trap 7: curve trade direction
> A steepening or flattening view is stated and the question asks which maturities to buy and sell protection on.
> Correct: steepening (long-term risk up relative to short-term) means buy long-dated protection and sell short-dated protection; flattening means the reverse; a steepener is short-run bullish, a flattener short-run bearish (V6 p.295, p.296).
> Distractors buy protection at both maturities (a level trade, not a curve trade) or swap the legs; check each leg against the words "long-term credit risk increases relative to short-term."

> [!warning] Trap 8: basis trade spread comparison
> A bond yield, an MRR, and a CDS spread appear, and the question asks the basis or the convergence profit.
> Correct: bond credit spread = yield - MRR first, then compare with the CDS spread; profit on convergence is the absolute difference of the two credit spreads (V6 p.297, p.298).
> Distractors subtract MRR from the CDS spread (4.25% - 2.50% = 1.75%) or subtract the CDS spread from the raw bond yield (7% - 4.25% = 2.75%), both lifted from the official incorrect choices (V6 p.307).

> [!warning] Trap 9: monetizing a gain with an offsetting contract
> An investor bought or sold protection, the spread moved, and the question asks how to close and whether the result is a gain or loss.
> Correct: unwind by entering the opposite position at the current upfront premium; a protection seller closes by buying protection, gaining when the spread has narrowed, and a buyer closes by selling protection, gaining when the spread has widened (V6 p.291, p.292).
> Distractors describe selling protection "at a higher premium" when the position was originally short protection, or promise a profit with the spread moving against the position; anchor on the direction table before reading the options.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM05-Credit-Default-Swaps-Practice-Problems]]

## Cross-links

- [[LM04-Credit-Analysis-Models]]: supplies the machinery this module reuses without re-deriving it, expected exposure, recovery rate, LGD, POD, POS, hazard rates, expected loss, and CVA; CDS pricing is that expected-loss chain applied to a two-leg contract.
- [[LM01-The-Term-Structure-and-Interest-Rate-Dynamics]]: the credit curve is built by analogy to the benchmark term structure from LM1, and the discounting logic that keeps a constant-hazard credit curve from being perfectly flat is LM1's spot-rate machinery.
- [[LM01-Pricing-and-Valuation-of-Forward-Commitments]]: the derivatives reading prices swaps as the difference in present values of two legs at initiation and marks them to market afterward, exactly the protection-leg-minus-premium-leg logic used here for the upfront payment and monetization.

## Self-test

Vignette A for Q1 to Q5: Marisol Vega manages credit at a hedge fund.
Corvid Freight is a high-yield issuer whose five-year CDS carries the standard high-yield coupon; its five-year credit spread is 620 bps, and the CDS has an effective spread duration of 4.2 years.
Vega buys $20 million of five-year protection on Corvid, whose reference obligation is a senior unsecured note.
One year later Corvid's five-year spread has narrowed to 500 bps and the CDS duration has declined to 3.6, and Vega considers unwinding.
Later still, Corvid misses an interest payment on a subordinated note after the grace period expires, without filing for bankruptcy, and the DC declares a credit event.
Corvid's traded debt at settlement: a three-year senior unsecured bond at 45% of par, a seven-year senior unsecured bond at 40%, and a subordinated note at 25%.
Vega also holds $20 million face of the three-year senior unsecured bond.

> [!question] Q1
> The upfront premium Vega pays at initiation is closest to:
> A. 1.20% of notional.
> B. 5.04% of notional.
> C. 26.04% of notional.

> [!question] Q2
> The price of the Corvid CDS per 100 par at initiation is closest to:
> A. 94.96.
> B. 98.80.
> C. 105.04.

> [!question] Q3
> If Vega unwinds after one year at the 500 bps spread with duration 3.6, the result on the CDS position is closest to:
> A. a gain of $864,000.
> B. a loss of $864,000.
> C. a loss of $1,008,000.

> [!question] Q4
> The cash settlement payout on Vega's CDS after the credit event is closest to:
> A. $11.0 million.
> B. $12.0 million.
> C. $15.0 million.

> [!question] Q5
> Given her bond holding, Vega should:
> A. prefer cash settlement.
> B. prefer physical settlement.
> C. be indifferent between the two.

> [!success]- Answer key
> Q1: B.
> Corvid is high yield, so the fixed coupon is 5%; upfront = (620 - 500) bps x 4.2 = 120 bps x 4.2 = 5.04% (Python: 0.012 x 4.2 = 0.0504).
> A ignores duration (the raw 1.20% difference); C multiplies the full 620 bps spread by duration, forgetting the standardized coupon absorbs 500 bps.
> Q2: A.
> Price = 100 - upfront premium% = 100 - 5.04 = 94.96.
> B subtracts the duration-free 1.20; C adds the premium instead of subtracting, which would be the price only if the seller had paid the upfront.
> Q3: B.
> Vega bought protection, so narrowing spreads hurt her; loss = 120 bps x 3.6 x $20m = 0.012 x 3.6 x 20,000,000 = $864,000 (Python: 864,000).
> A has the sign wrong (the protection seller gains on narrowing); C incorrectly reuses the initiation duration of 4.2 instead of the current 3.6.
> Q4: B.
> The subordinated note at 25 is not deliverable against a senior unsecured reference obligation, so the cheapest-to-deliver covered bond is the seven-year senior at 40, RR = 40%.
> Payout = (1 - 0.40) x $20m = $12m (Python: 12,000,000).
> A uses the three-year bond's 45 price (not the cheapest deliverable); C uses the subordinated note's 25 price, which does not qualify.
> Q5: A.
> Cash: $12m payout plus sale of her three-year bond at 45 for $9m, total $21m; physical: deliver the bond and receive the $20m notional.
> Cash is worth $1m more, so A; C (indifference) would hold only if she owned the cheapest-to-deliver seven-year bond, and B collects strictly less.

Vignette B for Q6 to Q10: Nikos Pallis, a strategist, evaluates several CDS opportunities.
Issuer Thera Logistics has annual hazard rates of 1.0%, 1.5%, and 2.0% for the next three years.
A one-year CDS on issuer Wexford is being priced informally with a 3% probability of default and a 55% expected recovery rate, ignoring time value.
Issuer Brant Materials is investment grade; its five-year credit spread is 80 bps and the five-year CDS has an effective spread duration of 4.5.
Pallis expects issuer Corfu Marine to face severe funding pressure over the next 18 months but to be sound thereafter.
Finally, Pallis observes that Halden Foods' five-year bond yields 5.6%, MRR is 2.6%, and the five-year Halden CDS spread is 3.4%.

> [!question] Q6
> The probability that Thera defaults at some point during the next three years is closest to:
> A. 2.00%.
> B. 4.44%.
> C. 4.50%.

> [!question] Q7
> The fair one-year CDS spread for Wexford is closest to:
> A. 135 bps.
> B. 165 bps.
> C. 300 bps.

> [!question] Q8
> At initiation of a five-year CDS on Brant Materials:
> A. the buyer pays an upfront premium of about 0.9%, and the price is about 99.1.
> B. the seller pays an upfront premium of about 0.9%, and the price is about 100.9.
> C. the seller pays an upfront premium of about 3.6%, and the price is about 103.6.

> [!question] Q9
> The curve trade most consistent with Pallis's view on Corfu Marine is to:
> A. buy 1.5-year protection on Corfu and sell 5-year protection on Corfu.
> B. sell 1.5-year protection on Corfu and buy 5-year protection on Corfu.
> C. buy protection on Corfu at both 1.5 and 5 years.

> [!question] Q10
> The trade that exploits the Halden Foods pricing, and its convergence profit, is:
> A. buy the bond and buy protection, capturing 40 bps.
> B. sell protection and short the bond, capturing 40 bps.
> C. sell protection and short the bond, capturing 80 bps.

> [!success]- Answer key
> Q6: B.
> POS = 0.99 x 0.985 x 0.98 = 0.95565, POD = 1 - 0.95565 = 4.44% (Python: 0.044352).
> C adds the hazard rates (4.50%), ignoring conditionality; A quotes only the final-year hazard rate as if it were the lifetime probability.
> Q7: A.
> Spread = (1 - RR) x POD = 0.45 x 3% = 1.35% = 135 bps (Python: 0.0135).
> B multiplies by the recovery rate instead of the loss rate (0.55 x 3%); C ignores recovery entirely (3%).
> Q8: B.
> Brant is investment grade, so the fixed coupon is 1%; upfront = (80 - 100) bps x 4.5 = -0.90%, negative, so the seller pays the buyer 0.9%, and price = 100 - (-0.9) = 100.9 (Python: -0.002 x 4.5 = -0.009).
> A has the payer backwards (the buyer pays only when spread exceeds coupon); C multiplies the raw 80 bps spread by duration and misassigns the result.
> Q9: A.
> Near-term stress with long-term soundness is a flattening-then-inverting view concentrated at the short end: buy short-dated protection where risk is rising and sell long-dated protection to finance it, mirroring the curriculum's Example 9 (V6 p.296).
> B is the steepener, betting long-term risk rises relative to short-term; C is a level trade that pays double premium and expresses no curve view.
> Q10: B.
> Halden's bond credit spread = 5.6% - 2.6% = 3.0%, below the 3.4% CDS spread, so the basis is positive: credit pays more in the CDS market.
> Sell protection (collect the rich 3.4%) and short the bond (give up the cheap 3.0% spread), hedging rates, for 40 bps on convergence (Python: 0.004).
> A is the negative-basis trade and would lock in a negative carry here; C computes 80 bps by subtracting MRR from the CDS spread and comparing with the wrong quantity.

## Flashcards

#flashcards/cfa-l2/06-Fixed-Income/lm05

Credit default swap definition::A derivative contract in which a protection buyer makes a series of payments to a protection seller and receives a promise of compensation for credit losses from a credit event in an underlying (V6 p.276).
Four types of credit derivatives::Total return swaps, credit spread options, credit-linked notes, and credit default swaps, with CDS by far the most liquid (V6 p.276).
Reference entity vs reference obligation::The reference entity is the borrower the single-name CDS is written on; the reference obligation is the specific debt issue named in the contract, usually a senior unsecured bond (V6 p.277).
Which obligations does a single-name CDS cover?::Every debt obligation of the reference entity ranked equal to or higher than the reference obligation in priority of claims (V6 p.277).
Cheapest-to-deliver obligation::The lowest-priced debt instrument with the same seniority as the reference obligation, which determines the CDS payoff (V6 p.277).
In single-name CDS, who is short the credit?::The protection buyer is short credit exposure; the protection seller is long (V6 p.280).
Direction convention for index CDS::The buyer of a CDX index is long credit exposure and the seller is short, the reverse of single-name terminology (V6 p.280).
The two most common CDS index families::CDX for North America and iTraxx for Europe, Asia, and Australia (V6 p.278, p.282).
Constituent counts: CDX IG, iTraxx Main, CDX HY, iTraxx Crossover::125, 125, 100, and up to 75 entities respectively, all equally weighted (V6 p.282).
Key extra pricing factor for index CDS::Credit correlation; the more correlated the constituents' defaults, the more index protection costs (V6 p.278).
What happens when an index constituent defaults?::It is settled as a single-name CDS on notional/N and removed, and the index continues with a smaller notional (V6 p.283).
On-the-run index series::The latest six-monthly series created by Markit; moving from an old series to the new one is called a roll (V6 p.282).
Tranche CDS::A CDS on a combination of borrowers that covers losses only up to pre-specified levels (V6 p.278).
ISDA Master Agreement::The document parties sign agreeing their CDS conforms to ISDA specifications; regional standard contracts include the Standard North American Contract (V6 p.278, p.279).
Typical CDS maturities and dates::1 to 10 years, 5 years most liquid, maturing on the 20th of March, June, September, or December (V6 p.279).
Standardized CDS coupons::{{1%}} for investment-grade and {{5%}} for high-yield reference entities or indexes (V6 p.279).
Why does an upfront premium exist?::The standardized coupon rarely equals the credit spread the risk deserves, so the present value of the difference changes hands at initiation (V6 p.279, p.289).
Who pays upfront when the credit spread exceeds the fixed coupon?::The protection buyer pays the protection seller (V6 p.279).
Three most common credit events::Bankruptcy, failure to pay, and restructuring (V6 p.276, p.280).
Failure to pay::A missed scheduled principal or interest payment after the grace period, with no bankruptcy filing required (V6 p.280).
When does restructuring qualify as a credit event?::When it is involuntary or coercive, and only in jurisdictions that recognize it; it is not a credit event in the United States (V6 p.280).
Sovereign-specific credit events::Moratorium or repudiation of debt by the governmental authority (V6 p.276).
Determinations Committee composition and vote::15 members per region, 10 sell-side and 5 buy-side; declaring a credit event needs a supermajority of 12 (V6 p.280).
Succession event::A merger, spinoff, or divestiture that leaves responsibility for the referenced debt unclear; the DC can modify or split the CDS across successors (V6 p.281).
When does CDS settlement occur after a credit event?::Typically 30 days after the DC declaration, and the parties have the right but not the obligation to settle (V6 p.281).
Physical settlement mechanics::The buyer delivers a covered debt instrument and receives the full notional from the seller (V6 p.281).
Cash settlement payout formula::Payout = (1 - recovery rate) x notional, i.e. LGD x notional (V6 p.281).
How is the settlement recovery rate determined?::By an auction in which major banks and dealers bid for the cheapest-to-deliver defaulted debt; both parties accept the result (V6 p.281).
When is a bondholder indifferent between cash and physical settlement?::When the bond he holds is itself the cheapest-to-deliver obligation (V6 p.281, p.282).
Hazard rate (CDS pricing)::The conditional probability that default occurs in a period given that it has not already occurred (V6 p.286).
Probability of survival over T periods::The product of (1 - hazard rate) across the periods; lifetime POD is one minus that product (V6 p.286).
One-period CDS spread approximation::{{CDS spread = (1 - RR) x POD}}, expected loss per unit notional (V6 p.286).
Protection leg::The contingent payment the seller may make: the sum of discounted expected losses on the reference obligation (V6 p.287).
Premium leg::The buyer's promised coupon stream, each payment contingent on survival, discounted at the risk-free rate (V6 p.287).
Upfront payment in terms of the two legs::PV(protection leg) minus PV(premium leg); positive means the buyer pays (V6 p.288).
Upfront premium industry approximation::{{(Credit spread - Fixed coupon) x effective spread duration}} of the CDS (V6 p.289).
Why effective duration for a CDS?::Because the coupon-leg cash flows are contingent on the reference entity not defaulting (V6 p.289).
Price of CDS per 100 par::100 minus the upfront premium percentage; a negative upfront gives a price above 100 (V6 p.289, p.290).
Credit spread from a quoted upfront::Fixed coupon plus the upfront premium percent amortized over (divided by) the CDS duration (V6 p.290).
Percent change in CDS price for a spread change::Change in spread in bps times the CDS duration (V6 p.291).
Protection buyer's profit formula::Change in spread (bps) x duration x notional, positive when spreads widen (V6 p.291).
Three ways to monetize a CDS gain or loss::Exercise on default, unwind with an offsetting CDS at the current upfront premium, or hold to expiration as the spread decays to zero (V6 p.291, p.292).
What does the CDS spread do as maturity approaches with no default?::It converges to zero, as a bond converges to par (V6 p.292).
Credit curve::The set of a single borrower's credit spreads across maturities, essentially determined by CDS rates (V6 p.288).
What does an upward-sloping credit curve imply?::A greater likelihood of default in later years; downward-sloping implies greater near-term default probability, usually severe near-term stress (V6 p.288).
Why is the credit curve not flat under a constant hazard rate?::Discounting differs across maturities even when default probabilities are level (V6 p.288).
Naked CDS::Buying protection with no exposure to the reference entity; banned in Europe for sovereign debt (V6 p.293, p.294).
Long/short credit trade::Selling protection on one reference entity and buying protection on another, betting on relative credit improvement (V6 p.294).
ESG long/short construction::Buy protection on the weak-ESG company and sell protection on the strong-ESG company (V6 p.294).
Curve steepener trade and its short-run stance::Buy long-term protection and sell short-term protection; it is bullish on the reference entity in the short run (V6 p.295, p.296).
Curve flattener trade and its short-run stance::Buy short-term protection and sell long-term protection; it is bearish in the short run, expecting near-term problems (V6 p.296).
Which maturities move more in a parallel spread shift?::Longer-term CDS, exactly as long-duration bonds move more for a yield change (V6 p.296).
Negative basis::The credit spread is higher in the bond market than in the CDS market (V6 p.298).
Negative-basis trade legs::Buy the bond and buy CDS protection, hedging interest rate risk, to capture the spread differential on convergence (V6 p.297, p.298).
Equity-versus-credit LBO trade::Buy the target's stock and buy CDS protection on the issuer taking on the debt; both legs profit if the deal happens (V6 p.298, p.299).
30-second drill: spread 425 bps, coupon 500 bps, duration 6. Who pays upfront and how much?
?
Upfront = (425 - 500) bps x 6 = -4.5%, so the protection seller pays the buyer 4.5% of notional, and the CDS price is 100 - (-4.5) = 104.5 (V6 p.289, p.290).

30-second drill: you sold $8m of protection at 300 bps, duration 5; the spread gaps to 450 bps. P&L?
?
The seller is long credit and loses on widening: 150 bps x 5 x $8m = 0.015 x 5 x 8,000,000 = $600,000 loss (V6 p.291).

## Common mistakes

1. Flipping the direction table: in single-name CDS the protection buyer is short credit and gains when spreads widen, and the index convention is the opposite, so answer options exploiting bond-market intuition are traps (V6 p.280).
2. Computing the upfront premium without the duration, or multiplying the whole credit spread (instead of spread minus standardized coupon) by duration (V6 p.289, p.306).
3. Getting the upfront payer wrong when the spread is below the coupon: the seller pays the buyer, the upfront premium is negative, and the price per 100 exceeds 100 (V6 p.289, p.290).
4. Treating the subordinated bond as cheapest to deliver when the reference obligation is senior unsecured; only equal-or-higher-ranked obligations are deliverable (V6 p.277, p.278).
5. Concluding no credit event occurred because there was no bankruptcy filing; failure to pay after the grace period is itself a credit event, on any outstanding obligation (V6 p.280, p.306).
6. Calling the settlement holder indifferent between cash and physical when his bond trades above the cheapest-to-deliver price; indifference holds only for the CTD holder (V6 p.281, p.282).
7. Adding hazard rates over periods instead of multiplying survival probabilities and subtracting from one (V6 p.286, p.307).
8. Forgetting that the recovery rate scales the CDS spread: spread is (1 - RR) x POD, not POD alone and not RR x POD (V6 p.286).
9. Reversing curve trades: steepening means buy long-dated protection and sell short-dated, and a steepener is short-run bullish, not bearish (V6 p.295, p.296).
10. Computing the basis with mismatched quantities, e.g. CDS spread minus MRR or bond yield minus CDS spread, instead of comparing the two credit spreads after stripping MRR from the bond yield (V6 p.297, p.298, p.307).
11. Using the initiation duration to mark an aged CDS to market when the vignette supplies the current, shorter duration (V6 p.290).
12. Unwinding logic backwards: a protection seller closes by buying protection and gains only if spreads narrowed; a buyer closes by selling and gains only if spreads widened (V6 p.291, p.292, p.307).
13. Assuming total CDS notional is capped by the entity's outstanding debt, or that protection buyers must own the underlying; naked positions are allowed except for European sovereign debt (V6 p.279, p.293, p.294).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "06-05" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
