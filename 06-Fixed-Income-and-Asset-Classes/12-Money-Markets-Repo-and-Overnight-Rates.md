---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: draft
prereqs: [day-counts-calendars-and-schedules]
est_hours: 5
sources: [Federal Reserve Bank of New York - Secured Overnight Financing Rate data and about pages at newyorkfed.org, ARRC - SOFR transition and fallbacks at newyorkfed.org/arrc, ISDA - IBOR fallbacks supplement and protocol 2020, Tuckman and Serrat - Fixed Income Securities chapter 11 on repo, Duffie - Special repo rates]
---

# Money Markets, Repo and Overnight Rates

> [!info] Draft
> Written in this session; numbers computed by `code/bond_pricing.py` or shown arithmetic.
> The NY Fed pages fetched in this session were JavaScript shells with little text, and the ISDA fallback figure was confirmed only through a secondary search summary.
> Before `solid`: re-read the NY Fed and ISDA primary documents for every sourced statement below and have an independent reviewer check them.

## TL;DR

- Repo is a collateralised loan: cash for securities now, reverse later at a rate; interest is $N\cdot r\cdot d/360$ (USD).
- SOFR is the Federal Reserve Bank of New York's broad, transaction-based measure of overnight borrowing collateralised by Treasuries.
- Overnight rates are compounded in arrears: $\left(\prod(1+r_id_i/360)-1\right)\cdot360/D$.
- A special trades below general collateral because the security is in demand; the borrower of cash gets the lower rate.
- LIBOR cessation replaced a forward-looking term rate with a backward-looking compounded overnight rate plus a fixed fallback spread.

## Learning objectives

- Compute repo interest, haircut cash and the carry of a repo-funded bond.
- Compound an overnight rate over an accrual period and compare to a simple average.
- Explain general collateral versus special and the effect on funding.
- Describe the LIBOR transition mechanics: fallback rate, spread adjustment, timing of the fixing.

## Core concepts

### Repo

In a repurchase agreement one party sells a security and agrees to repurchase it at a later date for a higher price.
Economically it is a secured loan: the seller borrows cash, the buyer lends cash and holds the security as collateral.
Cash lent is the market value less a haircut: $\text{cash}=(1-h)\,V$.
Interest: $\text{cash}\cdot r\cdot d/360$ for USD repo (ACT/360; check the market).
The rate is the repo rate; the borrower of cash is a repo seller and the lender is a reverse-repo buyer.

### General collateral versus specials

General collateral (GC) is the rate on any acceptable Treasury collateral.
A security in unusual demand, for example because many are short it, trades special: the borrower of that security (the cash lender) accepts a lower rate on its cash.
So a short seller borrowing a special bond pays by receiving less interest on cash, and the extra return to the security holder is the specialness $=r_{GC}-r_{special}$.

### Funding a bond position

Carry of a bond financed in repo $\approx$ coupon income $-$ repo interest, per unit time on the dirty value.
Positive carry when the coupon yield exceeds the repo rate; negative carry means the position bleeds unless prices rise.
Funding risk is repricing at each roll; term repo locks it for the term.

### Overnight rates and compounding in arrears

Overnight rates such as SOFR (USD), SONIA (GBP), ESTR (EUR) are fixed daily and published after the day.
Over an interest period split into business-day intervals with rates $r_i$ applying for $d_i$ calendar days, the compounded rate is
$$R=\frac{1}{\tau}\left(\prod_i\left(1+\frac{r_id_i}{B}\right)-1\right),\quad \tau=\frac{\sum_i d_i}{B},$$
with $B=360$ for SOFR and ESTR and $B=365$ for SONIA.
The rate is known only at period end, so the payment is made after, possibly with a lookback or observation shift to publish the amount a few days before payment.
Versus term LIBOR, which was set in advance, the in-arrears structure removes the need to forecast credit-sensitive expectations and ties the coupon to actual overnight transactions.

### The SOFR definition

Per the New York Fed, SOFR measures the cost of borrowing cash overnight collateralised by Treasury securities, calculated as a volume-weighted median of transactions from tri-party repo, FICC-cleared GCF repo and FICC-cleared bilateral DVP repo, published each business day around 8:00 a.m. Eastern for the previous business day (NY Fed SOFR pages; see the status box above for sourcing limits).

### LIBOR cessation and fallbacks

For legacy derivatives, ISDA's IBOR fallbacks replace a ceased IBOR with a compounded overnight risk-free rate plus a fixed spread adjustment, set from the historical median difference between the IBOR and the compounded risk-free rate.
For 3-month USD LIBOR the fixed spread was reported as 0.26161% and fixed on 5 March 2021; USD LIBOR panel settings for key tenors ended on 30 June 2023 (ISDA and Bloomberg announcements as relayed in secondary sources in this session; verify against the primary ISDA document).
The structural consequence for systems: a legacy trade now needs a schedule of daily fixings, a spread, and a rule for which index applies on which date.

### How it is implemented

- Inputs: daily overnight fixings, an accrual schedule, lookback or lockout rule, spread.
- Output: coupon amount and accrual for each period; forward projection of the compounded rate off the OIS curve.
- Algorithm: product over daily growth factors; for forecasting use the discount-curve identity $\prod(1+r_id_i/B)\approx P(0,T_1)/P(0,T_2)$.
- Complexity: $O(D)$ for $D$ business days per coupon; forecasting is $O(1)$ from the curve.
- Pitfalls: weekend and holiday day counts, SONIA 365 versus SOFR 360, publication lag, revised or late fixings.
- Code: [`code/bond_pricing.py`](code/bond_pricing.py) implements `compound_in_arrears`.
- System context: market and reference data platform (planned section).

## Worked examples

### Example 1: repo interest and haircut cash

Pledge 100,000,000 of bonds at a 2% haircut for 7 days at 5.30%.
Cash lent $=98{,}000{,}000$.
Interest $=98{,}000{,}000\times0.053\times7/360=100{,}994.44$.

### Example 2: compounding versus simple average

Daily SOFR-style fixings (illustrative): 5.00% on three days, 5.10% on Thursday (1 day) and 5.10% on Friday applying 3 days over the weekend: total 7 days.
Day-weighted simple average: $(0.05\cdot3+0.051\cdot4)/7=5.0571\%$.
Compounded: $\big[(1+0.05/360)^3(1+0.051/360)(1+0.051\cdot3/360)-1\big]\cdot360/7=5.058965\%$.
Compounding adds about 0.18 bp over seven days at these levels, and the effect scales with the length of the period and the rate level.

### Example 3: negative carry on a repo-financed bond

A 4% annual-pay bond held 30 days with dirty value 100, financed at 5% repo ACT/360: coupon accrual $=4\times30/365=0.3288$ per 100, repo cost $=100\times0.05\times30/360=0.4167$; carry $=-0.0879$ per 100.
Negative carry: a rising price of at least 0.0879 over the month is needed to break even.

### Example 4: real-world case, the LIBOR fixing manipulation and its replacement

Regulators found banks had manipulated LIBOR submissions, and the UK FCA announced on 5 March 2021 the dates after which LIBOR settings would cease or lose representativeness; this triggered the ISDA fallbacks (source: FCA announcement of 5 March 2021 and ISDA statements; not fetched in this session, verify).
The structural problem was that a panel-based, judgement-driven rate underpinned vast contracts while the unsecured interbank term market had thinned.
That is why replacement rates are transaction-based overnight rates, and why the compounded-in-arrears fallback needed the fixed spread to preserve value at the switch.

## Pitfalls

- Applying ACT/360 to SONIA, which is ACT/365.
- Treating weekend fixings as one day instead of three days.
- Comparing a simple average of fixings to the compounded rate in a reconciliation.
- Ignoring haircut in repo carry: cash is below market value.
- Assuming GC repo funds a special bond.
- Using a stale or restated overnight fixing.
- Forgetting the spread adjustment when migrating a legacy LIBOR trade.

## Interview questions

> [!question]- fi-repo-interest | Compute repo interest on cash 98,000,000 at 5.30% for 7 days (ACT/360).
> $98{,}000{,}000\times0.053\times7/360=100{,}994.44$.

> [!question]- fi-repo-haircut | A 100,000,000 bond is repoed at a 2% haircut. How much cash is lent and why a haircut?
> 98,000,000.
> The haircut protects the lender against a fall in collateral value between margin calls.

> [!question]- fi-sofr-definition | What is SOFR and which markets feed it?
> A broad overnight Treasury-repo rate published by the NY Fed: volume-weighted median over tri-party, FICC-cleared GCF and FICC-cleared bilateral DVP repo transactions.
> Published about 8:00 a.m. ET for the prior business day.

> [!question]- fi-compound-arrears | Write the compounded-in-arrears formula for an overnight rate and say what $d_i$ is.
> $R=\frac{B}{\sum d_i}\left(\prod(1+r_id_i/B)-1\right)$.
> $d_i$ is the number of calendar days the fixing $r_i$ applies, three over a weekend.

> [!question]- fi-compound-vs-average | Why does compounding differ from the simple day-weighted average of fixings?
> Interest on interest: the product of growth factors exceeds one plus the sum, by cross terms of order $r^2d_id_j/B^2$.
> Over a week at 5% it is about 0.18 bp.

> [!question]- fi-gc-special | What is a special and who benefits?
> A security whose repo rate is below GC because demand to borrow it is high.
> The holder of the security who lends it receives cheaper cash funding; the borrower of the security accepts a lower cash rate.

> [!question]- fi-negative-carry | A 4% bond financed at 5% repo for a month has what carry sign and what does it imply?
> Negative: coupon yield is below the repo rate.
> The trade needs price appreciation of about 0.088 per 100 per month to break even.

> [!question]- fi-sonia-vs-sofr-basis | What day-count basis do SOFR and SONIA use?
> SOFR is ACT/360, SONIA is ACT/365.
> Mixing them is a 1.4% error on every accrual.

> [!question]- fi-ibor-fallback-structure | Describe the ISDA IBOR fallback for a legacy USD LIBOR swap.
> Replace LIBOR with compounded SOFR in arrears plus a fixed spread adjustment equal to the historical median IBOR minus RFR difference, fixed at the announcement date.
> For 3m USD LIBOR the spread was reported as 0.26161%.

> [!question]- fi-libor-why-replaced | Why was term LIBOR replaced by overnight transaction rates?
> LIBOR rested on panel submissions that were manipulated and on a thin unsecured interbank term market.
> Overnight secured rates are based on large volumes of real transactions.

> [!question]- fi-repo-funding-risk | What is rollover risk in funding a long bond with overnight repo?
> The repo rate and the availability of funding reset daily, so a rate spike or a haircut increase raises financing cost or forces liquidation.
> Term repo trades that risk for a known cost.

> [!question]- fi-forward-from-compounded | How is a future compounded overnight rate forecast from the curve?
> Over a period $[T_1,T_2]$ the compounded growth factor equals $P(0,T_1)/P(0,T_2)$ on the OIS curve, so the forward compounded rate is $\frac1\tau(P(0,T_1)/P(0,T_2)-1)$.

## Further reading

- Federal Reserve Bank of New York, SOFR pages and ARRC publications at newyorkfed.org.
- ISDA, *IBOR Fallbacks Supplement* and *IBOR Fallbacks Protocol* (2020).
- Tuckman and Serrat, *Fixed Income Securities*, chapter on repo and securities financing.
- Duffie, "Special Repo Rates", *Journal of Finance*, 1996.

## In this repo and SDE-Interview-Prep

- Code: [`code/bond_pricing.py`](code/bond_pricing.py).
- Related: [Day Counts, Calendars and Schedules](11-Day-Counts-Calendars-and-Schedules.md), [Discounting and Yield Curves](01-Discounting-and-Yield-Curves.md).
