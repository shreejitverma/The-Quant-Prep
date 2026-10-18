---
type: concept
track: [quant-trader, quant-research, quant-dev, quant-risk]
tier: core
status: solid
prereqs: [discounting-and-yield-curves]
est_hours: 4
sources: [International Swaps and Derivatives Association - 2006 ISDA Definitions: Section 4.16 Day Count Fractions (ISDA 2006), Bruce Tuckman and Angel Serrat - Fixed Income Securities: Tools for Today's Markets (3rd Edition John Wiley & Sons 2011), Luigi Ballabio - Implementing QuantLib: Quantitative Finance in C++ (Leanpub 2017), Ferdinando Ametrano and Marco Bianchetti - Everything You Always Wanted to Know About Multiple Interest Rate Curve Bootstrapping but Were Afraid to Ask (SSRN Working Paper 2013), Alternative Reference Rates Committee - ARRC Recommendations for More Robust Fallback Language for New Issuances or Collateralized Debt (Federal Reserve Bank of New York 2021)]
---

# Day Counts, Calendars and Schedules

## TL;DR

A cash flow is a pair consisting of a financial amount and a value date: the payment date originates from a holiday calendar, a business-day roll convention, and a schedule generator, while the accrual fraction originates from a day-count convention.
Day-count conventions directly impact dollar cash flows: a $5.0\%$ coupon on $\$1,000,000$ over $182$ days generates $\$25,277.78$ under ACT/360, but only $\$24,931.51$ under ACT/365F.
Across a $\$5,000,000,000$ dealer book, this convention spread accumulates to $\$2,071,949.00$.
Schedule generation (coupon frequency, stub rules, end-of-month alignment, and business-day rolling) is fully deterministic, yet constitutes the single largest source of trade booking breaks between front-office pricing engines and back-office clearing systems.
IMM dates (the third Wednesday of March, June, September, and December) anchor standardized interest rate futures.
Standard North American and European CDS index coupon dates are the 20th of March, June, September, and December, subject to the applicable business-day adjustment.
All numerical models in this note are verified by [fi_day_counts.py](code/fi_day_counts.py).

## Learning objectives

- Compute exact accrual fractions under ACT/360, ACT/365F, US 30/360 (Bond Basis), European 30E/360, and ACT/ACT (ISDA and ICMA).
- Formulate deterministic schedule generation algorithms incorporating stub conventions, end-of-month rules, and holiday calendars.
- Differentiate Following, Preceding, Modified Following, and Modified Preceding business-day conventions.
- Evaluate the monetary impact of leap-year splits on multi-year interest rate swap and bond cash flows.
- Contrast legacy term LIBOR single-period accruals with backward-looking compounded overnight SOFR schedules.
- Identify and mitigate the core operational pitfalls that trigger trade booking breaks across institutional trading systems.

## Core concepts

### 1. Day-Count Fractions

A day-count fraction $\tau(d_1, d_2)$ maps two calendar dates $(d_1, d_2)$ into an annual accrual fraction such that simple interest is given by:

$$\text{Interest} = N \times r \times \tau(d_1, d_2)$$

```
+----------------------------------------------------------------------------------------------------+
| Convention        | Mathematical Definition                  | Primary Market Standards            |
+----------------------------------------------------------------------------------------------------+
| ACT/360           | \text{Actual Days} / 360                 | USD & EUR money markets, SOFR OIS   |
| ACT/365F          | \text{Actual Days} / 365                 | GBP money markets, SONIA swaps, CAD |
| 30/360 (US Basis) | [360\Delta Y + 30\Delta M + \Delta D]/360| US corporate and agency bonds       |
| 30E/360 (Eurobond)| [360\Delta Y + 30\Delta M + \Delta D]/360| Eurobonds and international debt    |
| ACT/ACT (ISDA)    | \text{Days}_1 / Y_1 + \text{Days}_2 / Y_2| Cross-currency and OTC derivatives  |
| ACT/ACT (ICMA)    | \text{Actual Days} / [f \times L]        | US Treasuries and sovereign bonds   |
+----------------------------------------------------------------------------------------------------+
```

#### Detailed 30/360 Conventions:
- **US 30/360 (Bond Basis):**
  If $D_1 = 31$, then change $D_1$ to $30$.
  If $D_2 = 31$ and $D_1 = 30$, then change $D_2$ to $30$.
  $$\tau = \frac{360(Y_2 - Y_1) + 30(M_2 - M_1) + (D_2 - D_1)}{360}$$
- **European 30E/360 (ISMA / Eurobond):**
  If $D_1 = 31$, then change $D_1$ to $30$.
  If $D_2 = 31$, then change $D_2$ to $30$.
- **ACT/ACT (ISDA):**
  If the accrual period spans multiple calendar years, the calculation splits actual days into each respective calendar year:
  $$\tau = \frac{\text{Days in } Y_1}{\text{Days in Year } Y_1} + \frac{\text{Days in } Y_2}{\text{Days in Year } Y_2}$$
  Leap years ($Y_k$) divide by $366$, while standard years divide by $365$.

### 2. Holiday Calendars and Business-Day Conventions

A holiday calendar defines an indicator function $B(d) \in \{0, 1\}$ identifying whether date $d$ is an active trading session (excluding weekends and statutory bank holidays for a financial centre like New York, London, or TARGET2).
When an unadjusted coupon date falls on a non-business day ($B(d) = 0$), a business-day convention shifts the date:
1. **Following:** Rolls forward to the nearest subsequent business day.
2. **Preceding:** Rolls backward to the nearest preceding business day.
3. **Modified Following:** Rolls forward to the next business day unless that day falls in the next calendar month, in which case it rolls backward to the nearest preceding business day.
4. **Modified Preceding:** Rolls backward to the prior business day unless that day falls in the previous calendar month, in which case it rolls forward to the nearest subsequent business day.

### 3. End-of-Month (EOM) Rule and Schedule Generation

- **The End-of-Month Rule:** If the start date of a contract is the final business day of a month, all subsequent unadjusted dates in the schedule must be pegged to the final calendar day of their respective target months before business-day rolling is applied.
- **Drift Without EOM:** If a semi-annual schedule starts on Friday, 28 February 2025, stepping forward six calendar months without the EOM flag targets 28 August 2025.
- Because 28 August is a Thursday, Modified Following leaves it untouched, causing the schedule to permanently drift three days away from month-end.
- Under the EOM rule, the unadjusted target is 31 August 2025 (Sunday), which Modified Following rolls to Friday, 29 August 2025, properly preserving month-end alignment.

### 4. International Monetary Market (IMM) Dates

Standardized financial futures (including CME SOFR futures) use International Monetary Market (IMM) dates, strictly defined as the **third Wednesday** of March, June, September, and December.
Standard North American and European CDS index coupons (including CDX and iTraxx) fall on the 20th of March, June, September, and December, subject to the applicable business-day adjustment; these are not futures IMM dates.
For the 2026 calendar cycle:
- March IMM: 18 March 2026
- June IMM: 17 June 2026
- September IMM: 16 September 2026
- December IMM: 16 December 2026

## Worked examples

### Example 1: Same Nominal Rate Across Four Day-Count Conventions

An institution enters a $\$1,000,000$ notional contract at a fixed rate of $r = 5.0\%$ spanning 15 February 2024 to 15 August 2024:
- The actual elapsed duration is $182$ days.
- Note that 2024 is a leap year (February has 29 days).

```
+----------------------------------------------------------------------------------------------------+
| Day-Count Convention | Accrual Fraction Formula            | Accrual Fraction | Coupon Interest ($)|
+----------------------------------------------------------------------------------------------------+
| ACT/360              | 182 / 360                           | 0.505556         | $25,277.78         |
| ACT/365F             | 182 / 365                           | 0.498630         | $24,931.51         |
| 30/360 (US Basis)    | [360(0) + 30(6) + 0] / 360 = 180/360| 0.500000         | $25,000.00         |
| ACT/ACT (ISDA)       | 182 / 366                           | 0.497268         | $24,863.39         |
+----------------------------------------------------------------------------------------------------+
```

- **Monetary Discrepancy:**
  $$\Delta\text{Interest} = \$25,277.78 - \$24,863.39 = \$414.39\text{ per } \$1,000,000\text{ notional}$$
- Across a $\$5,000,000,000$ dealer swap book:
  $$\text{Firm-Wide Exposure Spread} = 5,000 \times \$414.39 = \$2,071,949.00$$

Mismatches in day-count convention booking between front-office pricing libraries and clearing confirmations directly create multi-million dollar economic reconciliation breaks.

### Example 2: ACT/ACT (ISDA) Multi-Year Leap Year Boundary

Consider an interest rate swap leg accruing from 1 July 2023 to 1 July 2024:
- Total actual calendar duration: $366$ days.
- Year 2023 portion (non-leap year, 365 days):
  $$\text{Days in 2023} = 31\text{ (Jul)} + 31\text{ (Aug)} + 30\text{ (Sep)} + 31\text{ (Oct)} + 30\text{ (Nov)} + 31\text{ (Dec)} = 184\text{ days}$$
  $$\tau_{2023} = \frac{184}{365} = 0.504110$$
- Year 2024 portion (leap year, 366 days):
  $$\text{Days in 2024} = 31\text{ (Jan)} + 29\text{ (Feb)} + 31\text{ (Mar)} + 30\text{ (Apr)} + 31\text{ (May)} + 30\text{ (Jun)} = 182\text{ days}$$
  $$\tau_{2024} = \frac{182}{366} = 0.497268$$
- Total ISDA Day-Count Fraction:
  $$\tau_{\text{ISDA}} = \frac{184}{365} + \frac{182}{366} = 1.001377$$
- Under ACT/365F:
  $$\tau_{\text{ACT/365F}} = \frac{366}{365} = 1.002740$$

The difference between ACT/365F and ACT/ACT (ISDA) across the leap-year boundary is $1.002740 - 1.001377 = 0.001363$ ($13.6\text{ basis points}$).

### Example 3: Month-End Date Adjustments under Modified Following

Examine two month-end dates falling on Saturdays:
1. **Saturday, 30 November 2024:**
   - Under Following: Shifts to Monday, 2 December 2024.
   - Because 2 December crosses into the next calendar month, Modified Following triggers the boundary rule and shifts backward to **Friday, 29 November 2024**.
2. **Saturday, 31 May 2025:**
   - Under Following: Shifts to Monday, 2 June 2025.
   - Because 2 June crosses into June, Modified Following shifts backward to **Friday, 30 May 2025**.

## Pitfalls

- **Confusing ACT/360 and ACT/365F:** Applying ACT/365F to an ACT/360 money market leg introduces a systematic $\frac{365}{360} - 1 = 1.39\%$ pricing distortion across all coupon payments.
- **Ignoring Leap-Year Splits in ACT/ACT ISDA:** Calculating multi-year periods by dividing the total days by 365 or 366 introduces multi-basis-point valuation errors when periods cross 1 January.
- **Neglecting the End-of-Month Rule:** Failing to activate the EOM flag causes standard monthly and quarterly schedules anchored at month-end to drift onto arbitrary days (such as 28 or 30).
- **Hardcoding Static Holiday Lists:** Using unversioned holiday calendars creates non-reproducible historical PnL when governments retroactively declare public holidays or market closures.
- **Conflating Fixing Dates with Accrual Dates:** In compounded overnight SOFR swaps, the rate observation window (with lookback or observation shift) differs by several business days from the contractual cash-flow accrual period.

## Interview questions

> [!question]- fi-daycount-act360-vs-365 | What is the dollar interest difference on $1,000,000 at 5% over 182 days between ACT/360 and ACT/365F?
> Under ACT/360, the interest is $\$1,000,000 \times 0.05 \times \frac{182}{360} = \$25,277.78$.
> Under ACT/365F, the interest is $\$1,000,000 \times 0.05 \times \frac{182}{365} = \$24,931.51$.
> The difference is $\$346.27$, reflecting the $\frac{365}{360} - 1 \approx 1.39\%$ convention spread.

> [!question]- fi-daycount-30360-rule | State the US 30/360 formula and calculate the accrual fraction from 31 January 2024 to 31 March 2024.
> Under US 30/360, if $D_1 = 31$, it changes to $30$. If $D_2 = 31$ and $D_1 = 30$, $D_2$ changes to $30$.
> Thus, $D_1 = 30$, $D_2 = 30$, $M_1 = 1$, $M_2 = 3$, and $\Delta Y = 0$.
> The fraction is $\frac{360(0) + 30(2) + (30 - 30)}{360} = \frac{60}{360} = \frac{1}{6} \approx 0.166667$.

> [!question]- fi-daycount-actact-split | How does ACT/ACT (ISDA) evaluate an accrual period spanning across a calendar year boundary?
> ACT/ACT ISDA decomposes the actual elapsed days into their respective calendar years.
> Days falling in each year are divided by that year's actual length (365 days for standard years, 366 days for leap years) and summed.
> For example, from 1 July 2023 to 1 July 2024, the fraction is $\frac{184}{365} + \frac{182}{366} = 1.001377$.

> [!question]- fi-bdc-modified-following | What is the operational definition of the Modified Following business-day convention?
> Modified Following shifts a cash flow to the nearest subsequent business day, unless that day falls in the following calendar month, in which case it shifts backward to the nearest preceding business day.
> For example, Saturday, 30 November 2024 shifts backward to Friday, 29 November 2024 to avoid crossing into December.

> [!question]- fi-eom-rule | Why is the End-of-Month (EOM) convention necessary in schedule generation algorithms?
> If an instrument is issued on the final business day of a month (e.g., 28 February), stepping forward calendar months without EOM anchors future dates to day 28.
> The EOM rule forces all target unadjusted dates to the final day of their respective target months before business-day rolling, preserving month-end alignment.

> [!question]- fi-imm-dates | What are International Monetary Market (IMM) futures dates and what are the 2026 dates?
> IMM futures dates are strictly defined as the third Wednesday of March, June, September, and December.
> For 2026, the dates are: 18 March, 17 June, 16 September, and 16 December.

> [!question]- fi-stub-types | What is a stub period in an interest rate swap and what variants exist?
> A stub occurs when a contract's total tenor is not an exact integer multiple of the payment frequency, creating an irregular first or last coupon period.
> The four standard variants are: short front, long front, short back, and long back stubs.

> [!question]- fi-daycount-is-rate | Why must an interest rate quote always specify its underlying day-count convention?
> An interest rate is meaningless without an accrual fraction, because identical percentage rates yield different cash amounts depending on whether they divide by 360, 365, or 366.
> The legally binding financial quantity is the tuple $(r, \text{convention})$.

> [!question]- fi-schedule-production-breaks | What are the primary causes of trade booking reconciliation breaks in production schedules?
> Key causes include mismatched day-count fractions between counterparties, omitting the EOM flag, discrepancies in bank holiday calendar versioning, and confusing fixing observation dates with cash settlement dates.

> [!question]- fi-calendar-versioning | Why do enterprise trading platforms enforce immutable, versioned holiday calendars?
> Governments and central banks periodically declare unscheduled bank holidays or alter market closures.
> If historical calendars were modified in place, all historical mark-to-market valuations and risk reports would drift retroactively, violating BCBS 239 auditability.

## Further reading

- International Swaps and Derivatives Association. *2006 ISDA Definitions: Section 4.16 Day Count Fractions*. ISDA, 2006.
- Tuckman, Bruce and Serrat, Angel. *Fixed Income Securities: Tools for Today's Markets*. 3rd Edition, John Wiley & Sons, 2011.
- Ballabio, Luigi. *Implementing QuantLib: Quantitative Finance in C++*. Leanpub, 2017.
- Ametrano, Ferdinando and Bianchetti, Marco. *Everything You Always Wanted to Know About Multiple Interest Rate Curve Bootstrapping but Were Afraid to Ask*. SSRN Working Paper, 2013.
