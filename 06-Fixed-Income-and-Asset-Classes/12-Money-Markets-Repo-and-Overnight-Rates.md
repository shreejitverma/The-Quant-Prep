---
type: concept
track: [quant-trader, quant-research, quant-dev, quant-risk]
tier: core
status: solid
prereqs: [day-counts-calendars-and-schedules]
est_hours: 5
sources: [Federal Reserve Bank of New York - Additional Information about Reference Rates Administered by the New York Fed (retrieved 2026-10-18), Bank of England - SONIA key features and policies (retrieved 2026-10-18), European Central Bank - The euro short-term rate (€STR) methodology and policies (June 2019) and €STR page (retrieved 2026-10-18), Bank of Japan - Uncollateralized overnight call rate statistics page (retrieved 2026-10-18), Treasury Market Practices Group - FAQ on proposed modifications to the fails charge (28 February 2018), ISDA - Statement on UK FCA LIBOR Announcement (5 March 2021), FCA - remaining synthetic US dollar LIBOR settings cease after 30 September 2024 (5 September 2024), 31 CFR Part 356 Appendix B, Darrell Duffie - Special Repo Rates (Journal of Finance 51(2) 1996), Bruce Tuckman and Angel Serrat - Fixed Income Securities 3rd ed. (Wiley 2011)]
---

# Money Markets, Repo and Overnight Rates

## TL;DR

- Repo is a sale and repurchase that works as a secured loan: 100mm of Treasuries at a 2% haircut raise 98mm of cash, and 7 days at 5.30% ACT/360 cost 100,994.44 USD of interest.
- A bond in demand trades special: its repo rate falls below general collateral (GC), and the owner earns the specialness as a funding subsidy; the fails charge (3% minus the fed funds target floor, per the Treasury Market Practices Group) caps how special a Treasury can get.
- Carry on a repo-financed bond is coupon accrual minus repo interest on the dirty price, and equals spot minus the repo-implied forward price: a 4% Treasury financed at 5% for 30 days carries -0.085820 per 100.
- The overnight benchmarks differ in what they measure: SOFR is a secured median, SONIA and €STR are unsecured trimmed means, TONA is the unsecured call rate; SONIA and TONA accrue ACT/365F, SOFR and €STR ACT/360.
- Legacy USD LIBOR derivatives fell back after 30 June 2023 to compounded SOFR plus spreads fixed on 5 March 2021, 26.161 bp for 3-month.

## Learning objectives

- Calculate repo haircut cash, interest accrual, and termination settlement amounts.
- Derive the carry and roll-down of repo-financed bond inventory across discordant day-count conventions.
- Formulate the exact compounded-in-arrears overnight rate algorithm and contrast it with simple day-weighted averaging.
- Analyze the microeconomics of general collateral (GC) versus special repo rates and quantify collateralized funding advantages.
- Evaluate the institutional architecture of SOFR volume-weighted median transaction pools across tri-party, GCF, and bilateral DVP segments.
- Master ISDA IBOR fallback protocols, fixed spread adjustments, and backward-looking observation shift mechanics.

## Core concepts

### 1. Repo mechanics

In a repo the cash borrower sells securities and agrees to buy them back at a fixed price on a later date; the cash lender does a reverse repo.
Legally it is a sale with title transfer under a master agreement (the SIFMA Master Repurchase Agreement in the US, the GMRA internationally), so the lender can sell the collateral if the borrower defaults.

- Haircut $h$: cash lent $= (1 - h) V$, so the cushion is $hV$.
- Initial margin ratio $m$: collateral $= (1 + m) \times$ cash, so cash $= V/(1 + m)$; a 2% haircut and a 102% margin are close but not equal.
- Interest: cash $\times r \times d/360$ in USD and EUR, $d/365$ in GBP; repurchase price = cash plus interest.
- Maximum leverage on a position financed entirely in repo is $1/h$: 50 times at a 2% haircut.

Settlement venues in US Treasury repo: tri-party (a clearing bank holds and allocates collateral), FICC's General Collateral Finance (GCF) service, and bilateral delivery-versus-payment (DVP), cleared through FICC or uncleared.
These are exactly the segments SOFR is built from.

### 2. General collateral, specials and fails

A GC repo accepts any security from a basket (any Treasury); a special repo names one security.
When a security is in demand (shorts need it, often the on-the-run issue or a futures CTD), lenders of that bond accept a low cash rate to get it: specialness $S = r_{GC} - r_{special} > 0$.
The owner of the bond borrows cash at $r_{special}$ and earns $S$ on the financed amount; Duffie (1996) shows the specialness is capitalised in the bond's price, which is why on-the-run bonds trade rich to off-the-run bonds.
A short who cannot borrow the bond fails to deliver; the Treasury Market Practices Group fails charge is
$$C = P \times \frac{\max(3 - R, F)}{100} \times \frac{1}{360} \text{ per day},$$
with $P$ the trade proceeds, $R$ the fed funds target (or the lower limit of the target range) in percent, and $F$ a floor that was 0 when the TMPG proposed raising it to 1 in February 2018 (TMPG FAQ, 28 February 2018; check the TMPG site for the current floor).
Failing costs at most $\max(3 - R, F)$% a year, so a special repo rate cannot sit much below $-\max(3 - R, F)$%: a borrower would rather fail.

### 3. Carry and the repo-implied forward price

Buy a bond at dirty price $P^d_0 = P_0 + AI_0$ and finance it in repo at $r$ for $d$ days; at the horizon you owe $P^d_0(1 + r d/360)$ and own a bond with accrued $AI_d$.
The break-even (forward) clean price is
$$F = P^d_0\left(1 + r\frac{d}{360}\right) - AI_d,$$
and carry $= P_0 - F = (AI_d - AI_0) - P^d_0 \, r \, d/360$: coupon accrual (on the bond's own day count, ACT/ACT for Treasuries) minus repo interest on the dirty price (ACT/360).
Negative carry (repo above the running yield) is paid for by expected price gains or roll-down; it is the funding cost of a long and the funding gain of a short.

### 4. Overnight benchmark rates

| | SOFR | SONIA | €STR | TONA |
| :--- | :--- | :--- | :--- | :--- |
| Administrator | NY Fed | Bank of England | ECB | Bank of Japan |
| Market | secured overnight Treasury repo: tri-party, GCF, FICC DVP | unsecured sterling deposits of one business day, at least 25mm GBP | unsecured overnight fixed-rate deposits over 1mm EUR borrowed by euro area banks | unsecured overnight call money |
| Statistic | volume-weighted median, after removing the 20% lowest-rate DVP volume as specials | volume-weighted mean of the central 50% | volume-weighted mean after trimming 25% at each end | transaction-based call rate |
| Publication | next business day, around 8:00 a.m. ET | 9:00 a.m. on the next London business day | next TARGET2 business day | provisional around 5:15 p.m., final around 10:00 a.m. next business day |
| Rounding | nearest basis point | 4 decimals | 3 decimals | |
| OIS day count | ACT/360 | ACT/365F | ACT/360 | ACT/365F |

Sources: NY Fed, Bank of England, ECB (methodology, June 2019) and Bank of Japan pages, retrieved 2026-10-18.
The €STR was first published on 2 October 2019 for 1 October 2019 (ECB).
SOFR being secured matters: in stress, unsecured rates rise with bank credit risk while secured rates can fall (a flight to collateral), so SOFR and an unsecured bank funding rate can move in opposite directions.

### 5. Compounding in arrears

Over business days $i$ with fixings $r_i$ and calendar-day weights $n_i$ (until the next business day),
$$R = \left[\prod_i \left(1 + \frac{r_i n_i}{B}\right) - 1\right]\frac{B}{\sum_i n_i}, \qquad B = 360 \text{ (SOFR, €STR)}, \; 365 \text{ (SONIA, TONA)}.$$
The day-weighted average $\bar r = \sum r_i n_i / \sum n_i$ ignores interest on interest; expanding the product, compounding at a constant rate $r$ is higher by about $r^2 \frac{(\sum n_i)^2 - \sum n_i^2}{2B\sum n_i}$, because interest compounds only across business days: 0.18 bp for a Monday-to-Monday week at 5%.
Observation conventions (lookback, observation shift, lockout, payment delay) are in [Day Counts, Calendars and Schedules](11-Day-Counts-Calendars-and-Schedules.md), the replication and telescoping argument in [Swaps and Curve Building](03-Swaps-and-Curve-Building.md).

### 6. LIBOR cessation and fallbacks

LIBOR was a panel survey of unsecured term borrowing in a market with few real transactions; the overnight RFRs above are computed from large transaction volumes.
On 5 March 2021 the UK FCA announced the end of all LIBOR settings: most after 31 December 2021, and overnight, 1, 3, 6 and 12-month USD LIBOR after 30 June 2023.
ISDA said the announcement was an index cessation event for all 35 settings, which fixed the fallback spread adjustments published by Bloomberg as of that date (ISDA statement, 5 March 2021): the five-year historical median of LIBOR minus the compounded RFR, 26.161 bp for 3-month USD and 71.513 bp for 12-month USD.
Derivatives under the 2020 IBOR Fallbacks Protocol or Supplement now pay compounded SOFR in arrears over the LIBOR tenor (Bloomberg computes it with a two-business-day backward shift) plus that spread.
Synthetic 1, 3 and 6-month USD LIBOR, published for legacy cash products, ceased after 30 September 2024 (FCA, 5 September 2024).

## Worked examples

Rates are hypothetical; conventions are the sourced ones above.
Every number is computed, printed and asserted by [fi_money_markets.py](code/fi_money_markets.py).

### Example 1: a 7-day repo

100mm market value of Treasuries, 2% haircut, 7 days at 5.30% ACT/360.
Cash lent $= 0.98 \times 100{,}000{,}000 = 98{,}000{,}000$.
Interest $= 98{,}000{,}000 \times 0.053 \times 7/360 = 100{,}994.44$; repurchase price 98,100,994.44 USD.
The cushion is 2,000,000 USD; quoted instead as a 102% initial margin, cash would be $100{,}000{,}000/1.02 = 98{,}039{,}215.69$ and the cushion 1,960,784.31: 2% of the cash, not of the collateral.

### Example 2: compounding a week of SOFR

Fixings 5.00% Monday to Wednesday and 5.10% Thursday and Friday, Friday's rate applying for 3 days.
Day-weighted average $= (3 \times 5.00 + 5.10 + 3 \times 5.10)/7 = 5.0571\%$.
Growth $= (1 + 0.05/360)^3 (1 + 0.051/360)(1 + 0.153/360) = 1.000983688$, so $R = 0.000983688 \times 360/7 = 5.0590\%$.
"Compounding adds 0.18 bp in a week; a constant 5% week also compounds to 0.18 bp above 5%."
On a 365 basis (SONIA style) the same fixings compound to 5.0589%: the basis changes the compounding term, not just the quote.

### Example 3: carry on a repo-financed Treasury

Buy a 4% Treasury (coupons 15 Feb and 15 Aug 2026) at 100 clean on 1 Mar 2026, finance it at 5% repo, sell on 31 Mar.
The half-year has 181 days; accrued interest is $2 \times 14/181 = 0.154696$ at purchase and $2 \times 44/181 = 0.486188$ at sale, so coupon accrual is 0.331492.
Repo interest on the dirty price is $100.154696 \times 0.05 \times 30/360 = 0.417311$.
Carry $= 0.331492 - 0.417311 = -0.085820$ per 100, -85,820 USD on 100mm face.
Cross-check: the forward clean price is $100.154696 \times (1 + 0.05 \times 30/360) - 0.486188 = 100.085820$, so the bond must be 0.085820 points higher in a month to break even.

### Example 4: specialness and the fails charge

GC 5.30%, special 3.80%: specialness 150 bp, worth $100{,}000{,}000 \times 0.015 \times 30/360 = 125{,}000$ USD a month to the owner of 100mm.
A one-day fail on 100mm of proceeds costs $100{,}000{,}000 \times 3\%/360 = 8{,}333.33$ USD when the reference rate is 0, nothing when it is 4% with a zero floor, and 2,777.78 USD with the proposed 1% floor.
"That is why a special repo rate can go negative when the reference rate is near zero, but not far below minus the fails charge."

### Example 5: a 3-month LIBOR fallback

Period 1 Jul to 1 Oct 2026: 92 calendar days, 64 SOFR business days (3 Jul and 7 Sep are holidays).
With every fixing at a hypothetical 4.30%, compounded SOFR is 4.32320%, and the fallback rate is $4.32320\% + 0.26161\% = 4.58481\%$.

## Pitfalls

- Using ACT/360 for SONIA or TONA (ACT/365F) or ACT/365F for SOFR or €STR: a 1.39% error in every coupon.
- Giving a Friday fixing weight 1 instead of 3, which drops two-thirds of its weekend interest.
- Computing repo interest on the clean price, or carry without the haircut equity the position ties up.
- Pricing a special bond's position with GC funding, or a short's cost without the specialness it pays.
- Treating haircut and initial margin ratio as the same number.
- Assuming SOFR moves with bank credit spreads: it is secured, and can fall in stress while unsecured rates rise.
- Valuing a legacy LIBOR trade on compounded SOFR without its fixed spread adjustment.
- Rollover risk: overnight repo funding of a long-dated position can be repriced, re-haircut or withdrawn every day.

## Interview questions

> [!question]- fi-repo-interest | Calculate the repo interest on $98,000,000 cash at 5.30% for 7 days under ACT/360.
> $100{,}994.44$ USD.
> $98{,}000{,}000 \times 0.053 \times 7/360$; the repurchase price is 98,100,994.44 USD.

> [!question]- fi-repo-haircut | Why do repo agreements require a collateral haircut and how is cash lent computed?
> The haircut protects the cash lender against a fall in collateral value between margin calls and during liquidation after a default.
> Cash lent $= (1 - h)V$: 98mm against 100mm at a 2% haircut.

> [!question]- fi-sofr-definition | What transactions comprise the Secured Overnight Financing Rate (SOFR)?
> Overnight Treasury repo in three segments: tri-party, FICC's GCF service, and FICC-cleared bilateral DVP, with the 20% lowest-rate DVP volume removed as specials.
> SOFR is the volume-weighted median, rounded to a basis point and published by the NY Fed the next business day.

> [!question]- fi-compound-arrears | What is the formula for compounding overnight rates in arrears and what does $d_i$ represent?
> $R = \frac{B}{\sum d_i}\left[\prod_i (1 + r_i d_i/B) - 1\right]$ with $B = 360$ for SOFR and €STR and 365 for SONIA and TONA.
> $d_i$ is the number of calendar days fixing $r_i$ applies: 1 on a normal weekday, 3 for a Friday, more before a holiday.

> [!question]- fi-compound-vs-average | How does compounded SOFR compare with the simple day-weighted average of daily fixings?
> For positive rates it is higher, by about $r^2 [(\sum d_i)^2 - \sum d_i^2]/(2B \sum d_i)$ at a constant rate, because interest earns interest from one business day to the next.
> At a constant 5% for a week the gap is 0.18 bp; with negative or mixed fixings the sign and size depend on the path.

> [!question]- fi-gc-special | What does it mean for a bond to trade "on special" and who benefits economically?
> Its repo rate is below the GC rate because many want to borrow that specific bond.
> The owner benefits: it borrows cash cheaply against the bond and earns the specialness $r_{GC} - r_{special}$, which is why such bonds trade rich.

> [!question]- fi-negative-carry | What is negative carry on a bond position and what are its trading implications?
> The repo cost on the dirty price exceeds the coupon accrual: a 4% Treasury financed at 5% for 30 days carries -0.085820 per 100.
> The position needs the price to rise by that much (the forward minus spot) or roll-down to break even.

> [!question]- fi-sonia-vs-sofr-basis | What day-count conventions govern SOFR and SONIA money market instruments?
> SOFR: ACT/360.
> SONIA: ACT/365F; €STR is ACT/360 and TONA ACT/365F.

> [!question]- fi-ibor-fallback-structure | What is the permanent ISDA fallback spread for 3-Month USD LIBOR?
> $26.161$ bp, fixed on 5 March 2021 as the five-year historical median of 3M LIBOR minus compounded SOFR.
> The fallback rate is compounded SOFR in arrears over the 3-month tenor plus that spread.

> [!question]- fi-libor-why-replaced | Why did global regulators mandate the replacement of LIBOR with overnight risk-free rates?
> LIBOR was a panel estimate of unsecured term bank borrowing, a market with few transactions, and it was manipulated.
> The replacements are computed from large daily transaction volumes; SOFR is secured, while SONIA and €STR are unsecured but transaction-based.

> [!question]- fi-repo-funding-risk | What is rollover risk when financing long bond positions via overnight repo?
> The lender can reprice, raise the haircut or refuse to roll every day, while the asset is long-dated.
> In stress the position must then be cut at the worst time, as in the March 2020 Treasury basis unwind.

> [!question]- fi-forward-from-compounded | How do quantitative curve engines forecast forward compounded overnight rates from OIS curves?
> Because rolling an overnight deposit replicates the compounded rate, the expected growth over $[T_1, T_2]$ is $P(0,T_1)/P(0,T_2)$ on the OIS curve.
> So $F(T_1, T_2) = \frac{B}{\sum d_i}\left[\frac{P(0,T_1)}{P(0,T_2)} - 1\right]$, with no convexity adjustment when paid at $T_2$.

> [!question]- fi-repo-margin-vs-haircut | A lender asks for 102% initial margin on 100mm of collateral; how much cash does it lend, and how does that differ from a 2% haircut?
> $98{,}039{,}215.69$ USD, versus 98,000,000 with a 2% haircut.
> Margin is a percentage of the cash ($V = 1.02 \times$ cash); the haircut is a percentage of the collateral.

> [!question]- fi-repo-fails-charge | What is the Treasury fails charge and how does it bound special repo rates?
> A penalty of $\max(3 - R, F)$% a year on the proceeds for each day a seller fails, with $R$ the fed funds target floor and $F$ a floor.
> Since failing costs at most that rate, a special repo rate cannot fall much below its negative: shorts would rather fail than lend cash at a lower rate.

> [!question]- fi-carry-forward-price | Show that carry on a repo-financed bond equals spot minus the forward clean price.
> The forward clean price is $F = P^d_0(1 + r d/360) - AI_d$, the price that leaves the financed position flat.
> $P_0 - F = (AI_d - AI_0) - P^d_0 r d/360$, coupon accrual minus repo interest, which is carry.

> [!question]- fi-rfr-secured-vs-unsecured | Which overnight benchmarks are secured and why does it matter in a crisis?
> SOFR is secured (Treasury repo); SONIA, €STR and TONA are unsecured.
> In stress unsecured rates include rising bank credit risk while secured rates can fall on demand for collateral, so a hedge of bank funding with SOFR can fail when it is most needed.

> [!question]- fi-libor-cessation-dates | When did USD LIBOR end for derivatives and for legacy cash products?
> Panel USD LIBOR ended after 30 June 2023, triggering ISDA fallbacks to compounded SOFR plus the 5 March 2021 spreads.
> Synthetic 1, 3 and 6-month USD LIBOR for legacy cash contracts ceased after 30 September 2024.

## In this repo and SDE-Interview-Prep

- Code: [`code/fi_money_markets.py`](code/fi_money_markets.py) (repo, carry, specials and fails, compounded RFRs, fallbacks).
- Related notes: [Day Counts, Calendars and Schedules](11-Day-Counts-Calendars-and-Schedules.md), [Swaps and Curve Building](03-Swaps-and-Curve-Building.md), [Treasury Futures and the Basis](16-Treasury-Futures-and-the-Basis.md).

## Further reading

- Federal Reserve Bank of New York, "Additional Information about Reference Rates Administered by the New York Fed", retrieved 2026-10-18.
- Bank of England, "SONIA key features and policies", retrieved 2026-10-18.
- European Central Bank, *The euro short-term rate (€STR) methodology and policies*, June 2019.
- Bank of Japan, uncollateralized overnight call rate statistics page, retrieved 2026-10-18.
- Treasury Market Practices Group, "Frequently Asked Questions: Proposed Modifications to the TMPG Fails Charges", 28 February 2018.
- ISDA, "ISDA Statement on UK FCA LIBOR Announcement", 5 March 2021.
- Financial Conduct Authority, announcement on the end of the remaining synthetic US dollar LIBOR settings, 5 September 2024.
- Darrell Duffie, "Special Repo Rates", *Journal of Finance* 51(2), 1996.
- Bruce Tuckman and Angel Serrat, *Fixed Income Securities: Tools for Today's Markets*, 3rd edition (Wiley 2011).
