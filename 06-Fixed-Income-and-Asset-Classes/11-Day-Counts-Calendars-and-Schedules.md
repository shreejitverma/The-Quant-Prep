---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: draft
prereqs: [discounting-and-yield-curves]
est_hours: 4
sources: [ISDA 2006 Definitions section 4.16 day count fractions - licensed text not re-read this session, Tuckman and Serrat - Fixed Income Securities chapter 3, QuantLib documentation at quantlib.org on day counters and calendars, Ametrano and Bianchetti - Everything you always wanted to know about multiple interest rate curve bootstrapping]
---

# Day Counts, Calendars and Schedules

> [!info] Draft
> Written and computed in this session; the independent review required for `solid` has not happened.
> The ISDA Definitions are licensed and were not re-read here: the exact wording of 30/360 variants and end-of-month rules must be checked against the licensed text or a term sheet before use.

## TL;DR

- A cash flow is (amount, date): the date comes from a calendar, a roll rule and a schedule; the accrual comes from a day-count fraction.
- Day-count conventions change the money: 5% on 1,000,000 over 182 days is 25,277.78 under ACT/360 and 24,931.51 under ACT/365F.
- Schedule generation (frequency, stub, end-of-month, business-day roll) is deterministic but fiddly; most production pricing breaks come from here.
- IMM dates (third Wednesday of March, June, September, December) anchor futures and standardised swaps.
- Dates must be generated once, unrolled and rolled versions kept, and carried into both the pricer and the risk engine.

## Learning objectives

- Compute accrual fractions under ACT/360, ACT/365F, 30/360 and ACT/ACT.
- Generate a schedule with a roll convention, end-of-month rule and stubs.
- List the calendar and date-adjustment choices that move a swap's PV.
- Explain why conventions are product, currency and leg specific.

## Core concepts

### Day-count fractions

A day-count fraction $\tau(d_1,d_2)$ turns two dates into an accrual factor: interest $=N\cdot r\cdot\tau$.

| Convention | Rule | Typical use (check the product) |
| :--- | :--- | :--- |
| ACT/360 | actual days / 360 | USD and EUR money markets, floating legs |
| ACT/365F | actual days / 365 | GBP money markets, many bond markets |
| 30/360 (US bond basis) | $\frac{360\Delta Y+30\Delta M+(D_2-D_1)}{360}$ with day-31 adjustments | US corporates and agencies, USD swap fixed legs |
| ACT/ACT (ISDA) | actual days in each calendar year over that year's length (365 or 366) | Treasury-style bonds |

Typical uses vary by product and are set in the term sheet; never infer a convention from the currency alone.
Day-count conventions are part of the rate: a quoted 5% is only a number once the convention is stated.

### Calendars and business-day adjustment

A calendar lists non-business days (weekends and holidays for a financial centre).
Common adjustments: Following (next business day), Modified Following (Following unless it crosses a month end, then Preceding), Preceding.
Swap and bond schedules usually use Modified Following; some products fix payment dates on one calendar and fixing dates on another.
A schedule is a function of: start, end, frequency, roll day, end-of-month flag, calendars, adjustment rule, stub rule.

### Stubs and end-of-month

If the term is not a whole number of periods, a short or long stub exists at the front or back.
End-of-month: if the start date is the last business day of a month, subsequent dates roll to the last business day of their months.
Without this flag, a semiannual schedule starting on Friday 28 February 2025 steps from the anchor to 28 August 2025 instead of 31 August, and one starting on 30 April steps to 30 October instead of 31 October.

### IMM dates

IMM dates are the third Wednesday of March, June, September and December.
Futures and standardised CDS and swap contracts reference them; the 2026 dates are 18 March, 17 June, 16 September and 16 December (checked by `code/bond_pricing.py`).

### How it is implemented

- Inputs: a schedule specification (above) and calendar objects.
- Output: arrays of unadjusted dates, adjusted dates, payment dates, accrual start and end, and day-count fractions.
- Algorithm: generate unadjusted dates by stepping months from the anchor, apply the end-of-month rule, roll each date, compute fractions.
- Complexity: $O(n)$ per schedule; cache by specification hash.
- Pitfalls: leap years, holiday calendar versions, dates in the wrong timezone, fixing dates versus accrual dates, regenerating a schedule differently between the pricer and the risk engine.
- Code: [`code/bond_pricing.py`](code/bond_pricing.py) implements the four conventions, month stepping and Modified Following.
- System context: the trade representation and curve service (planned section).

## Worked examples

The fractions and dates below are checked by `code/bond_pricing.py`, run in this session; interest amounts are the arithmetic shown.

### Example 1: same rate, four conventions

Notional 1,000,000, 5%, 15 Feb 2024 to 15 Aug 2024 (182 actual days, 2024 is a leap year).

| Convention | Fraction | Interest |
| :--- | :--- | :--- |
| ACT/360 | $182/360=0.505556$ | 25,277.78 |
| ACT/365F | $182/365=0.498630$ | 24,931.51 |
| 30/360 | $180/360=0.5$ | 25,000.00 |
| ACT/ACT | $182/366=0.497268$ | 24,863.39 |

The spread between the highest and lowest is 414.39 on one million, so a convention mismatch on a 5bn book is real money.

### Example 2: ACT/ACT across a leap year

1 July 2023 to 1 July 2024 has 366 actual days, split 184 days in 2023 (365-day year) and 182 days in 2024 (366-day year): $184/365+182/366=1.001377$.
Under ACT/365F the same period is $366/365=1.002740$.

### Example 3: 30/360 and month ends

31 January 2024 to 31 March 2024 under US 30/360: $D_1=31\to30$, $D_2=31\to30$, so $360\cdot0+30\cdot2+0=60$ days, a fraction of $1/6$.
Actual days are 60 as well here, but over February the two diverge.

### Example 4: Modified Following

Saturday 30 November 2024 rolls to Friday 29 November 2024 under Modified Following without holidays, because Following would cross into December.
Saturday 31 May 2025 likewise rolls to Friday 30 May 2025.

### Example 5: real-world case, the LIBOR-to-SOFR convention change

Legacy USD LIBOR floating legs accrued ACT/360 on a term rate; SOFR-based legs compound a daily overnight rate in arrears, still ACT/360 per day, but the accrual period and payment lag now come with new conventions (source: ARRC conventions and the NY Fed SOFR pages; see the money markets note for details; not re-fetched this session, verify).
Migrating a trade changes the schedule, the lookback or lockout, and the payment lag, so every system that held a single accrual period per coupon needed to hold a daily schedule.

## Pitfalls

- Using ACT/365 for a leg that is ACT/360, a roughly 1.4% error in every coupon.
- Forgetting leap-year effects in ACT/ACT versus ACT/365F.
- Implementing 30/360 without the day-31 rule or confusing US and European variants.
- Dropping the end-of-month flag, so schedules drift from month ends.
- Using one calendar for both fixing and payment when the product specifies two.
- Rolling dates in the pricer but not in the risk or cash-flow projection code.
- Hardcoding holiday lists with no versioning, so a restated historical date changes old valuations.

## Interview questions

> [!question]- fi-daycount-act360-vs-365 | 5% on 1,000,000 over 182 days: interest under ACT/360 versus ACT/365F?
> ACT/360: $1{,}000{,}000\cdot0.05\cdot182/360=25{,}277.78$.
> ACT/365F: $24{,}931.51$.
> The 1.4% gap is $365/360-1$.

> [!question]- fi-daycount-30360-rule | State the US 30/360 formula and compute 31 Jan to 31 Mar.
> $\frac{360\Delta Y+30\Delta M+(D_2-D_1)}{360}$ with $D_1=\min(D_1,30)$ and $D_2=30$ if $D_2=31$ and $D_1=30$.
> 31 Jan to 31 Mar is $60/360=1/6$.

> [!question]- fi-daycount-actact-split | How does ACT/ACT (ISDA) handle a period spanning two years?
> Split the period by calendar year: days in each year divided by that year's length (365 or 366), summed.
> Example: 184/365 + 182/366 = 1.001377.

> [!question]- fi-bdc-modified-following | Define Modified Following and give an example.
> Roll to the next business day unless that moves into the next month, then roll to the previous business day.
> Saturday 30 Nov 2024 rolls to Friday 29 Nov 2024.

> [!question]- fi-eom-rule | What does the end-of-month rule do and why is it needed?
> If the start date is the last business day of a month, all subsequent unadjusted dates sit at month end.
> Without it, a 28 Feb 2025 start steps to 28 Aug 2025 instead of 31 Aug, so dates sit off month end.

> [!question]- fi-imm-dates | What are IMM dates and what are the 2026 ones?
> Third Wednesday of March, June, September and December.
> 2026: 18 March, 17 June, 16 September, 16 December.

> [!question]- fi-stub-types | What is a stub period and which kinds exist?
> A first or last accrual period shorter or longer than the regular period.
> Types: short front, long front, short back, long back.

> [!question]- fi-daycount-is-rate | Why are day count and compounding part of a rate quote?
> A rate is an accrual-factor-scaled amount: the same 5% produces different cash under different conventions, so (rate, convention) is the quantity, not the rate alone.

> [!question]- fi-schedule-production-breaks | List four ways schedule generation breaks production pricing.
> Wrong day count on a leg; missing end-of-month flag; holiday calendar mismatch between systems; fixing and payment dates mixed up.
> Also: leap years and regenerating the schedule differently in pricer and risk.

> [!question]- fi-actact-vs-act365 | Why is ACT/ACT over 1 July 2023 to 1 July 2024 not exactly 1.0 and how does it compare to ACT/365F?
> The period is 366 days across a leap year; ISDA ACT/ACT gives 1.001377, ACT/365F gives 366/365 = 1.002740.

> [!question]- fi-calendar-versioning | Why version holiday calendars in a trading system?
> Holiday lists change, and restating a past date set changes historical accruals and valuations; versioned calendars with an as-of date keep old trades reproducible.

## Further reading

- ISDA, *2006 ISDA Definitions*, section 4.16 (day count fractions); licensed text, verify wording.
- Tuckman and Serrat, *Fixed Income Securities*, chapter 3.
- QuantLib documentation on `DayCounter`, `Calendar` and `Schedule` at quantlib.org.
- Ballabio, *Implementing QuantLib*.

## In this repo and SDE-Interview-Prep

- Code: [`code/bond_pricing.py`](code/bond_pricing.py).
- Related: [Discounting and Yield Curves](01-Discounting-and-Yield-Curves.md), [Money Markets, Repo and Overnight Rates](12-Money-Markets-Repo-and-Overnight-Rates.md).
