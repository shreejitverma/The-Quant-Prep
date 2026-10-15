---
type: cfa-itemset
topic: "Alternative Investments"
topic_code: "08"
topic_slug: "08-Alternative-Investments"
lm: 2
title: "Tallis Foundation: Real Estate Reporting and Index Review"
los: [los-08-02-b, los-08-02-c, los-08-02-e]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/alternative-investments]
---

# Tallis Foundation: Real Estate Reporting and Index Review

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Elena Marsh, CFA, is a consultant hired by the Tallis Foundation, a US private foundation, to review the real estate section of its annual investment policy compliance report.
The foundation owns two properties directly and benchmarks its private real estate sleeve against an appraisal-based private property index.

The first property is Juniper Flats, a 180-unit multifamily complex in Denver with an average unit size of 950 square feet.
Current market rent for comparable units is USD2.10 per square foot per month.
Exhibit 1 shows the rent roll data for the coming year.

Exhibit 1: Juniper Flats rental data (USD)

| Item | Amount |
|---|---|
| Gross rental income at in-place rents | 4,190,000 |
| Vacancy and collection loss | 6% of gross rental income |
| Concessions | 85,000 |
| Other income (parking and laundry) | 212,000 |
| Operating expenses (not recoverable) | 1,640,000 |

Marsh observes that Denver apartment occupancy has risen for six consecutive quarters and that few new apartment projects are under construction.

The second property is a suburban office building in Phoenix.
There, leases signed two years ago carry rents above today's market rents, vacancy has risen for three quarters, and several office towers begun during the last boom are still being completed nearby.

Exhibit 2 reports the Phoenix building's most recent annual appraisal data.

Exhibit 2: Phoenix office appraisal data (USD)

| Item | Amount |
|---|---|
| Beginning appraised value | 62,000,000 |
| Ending appraised value | 63,400,000 |
| NOI for the year | 3,100,000 |
| Capital expenditures for the year | 450,000 |
| Mortgage principal repaid during the year | 1,200,000 |

The foundation's benchmark index reported quarterly returns of 2.40% last quarter and -1.20% this quarter.
Marsh models appraisal smoothing as $R_t^{*} = a R_t + (1-a) R_{t-1}^{*}$ and estimates $a = 0.40$ for the index.

The foundation's mean-variance optimizer uses the appraisal-based index history as its real estate input and recommends raising the real estate weight from 12% to 18%.
Two members of the investment committee comment on the recommendation.

Hugo Lindqvist: "The appraisal index lags transactions, so in a rising market it overstates returns, which is why the optimizer likes real estate."

Amara Osei: "Because the index is smoothed, the optimizer sees too little volatility and too little correlation with our equities, so the Sharpe ratio it uses for real estate is too high and the 18% weight is probably excessive."

To reduce the smoothing problem, the committee asks Marsh to recommend a transaction-based index for Denver apartments.
Marsh notes that Denver apartment properties differ widely in size, age, and quality, and that most of them have sold only once in the past decade.

## Questions

1. Juniper Flats' net rental income for the coming year is closest to: (LOS: los-08-02-c)
   - A. USD3,853,600.
   - B. USD3,938,600.
   - C. USD3,965,648.
2. Based on the office market conditions Marsh observed, the Phoenix office building's NOI and loan-to-value ratio are most likely: (LOS: los-08-02-b)
   - A. near their lowest NOI and highest LTV of the cycle.
   - B. near their highest NOI and lowest LTV of the cycle.
   - C. rising NOI and falling LTV, as in the expansion phase.
3. The Phoenix building's holding period return for the year, as it would enter an appraisal-based index, is closest to: (LOS: los-08-02-e)
   - A. 6.39%.
   - B. 6.53%.
   - C. 7.26%.
4. The unsmoothed (actual) return for the benchmark index this quarter is closest to: (LOS: los-08-02-e)
   - A. -6.60%.
   - B. -3.60%.
   - C. 0.60%.
5. Regarding the two committee members' comments, which is most accurate? (LOS: los-08-02-e)
   - A. Only Lindqvist's comment is correct.
   - B. Only Osei's comment is correct.
   - C. Both comments are correct.
6. For Denver apartments, the transaction-based index Marsh should most likely recommend is a: (LOS: los-08-02-e)
   - A. repeat sales index, because it controls for size, age, and quality through regression variables.
   - B. repeat sales index, because it uses every transaction in the market.
   - C. hedonic index, because it uses all transactions and controls for property characteristics.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Gross potential rental income: $180 \times 950 \times 2.10 \times 12 = 4{,}309{,}200$.
> Loss to lease: $4{,}309{,}200 - 4{,}190{,}000 = 119{,}200$, positive because in-place rents are below market.
> Vacancy and collection: $0.06 \times 4{,}190{,}000 = 251{,}400$.
> Net rental income: $4{,}190{,}000 - 251{,}400 - 85{,}000 = 3{,}853{,}600$.
> Other income and operating expenses come after net rental income in the pro forma and do not enter this figure.
> B is wrong because it omits concessions, $4{,}190{,}000 - 251{,}400 = 3{,}938{,}600$.
> C is wrong because it starts from GPRI and skips the loss to lease, applying vacancy to GPRI: $4{,}309{,}200 - 0.06 \times 4{,}309{,}200 - 85{,}000 = 3{,}965{,}648$.
> 2. **B.** In-place leases above market (a negative loss to lease), rising vacancy, and completions from projects started in the boom describe the oversupply phase.
> In the curriculum's cycle, NOI and DSC peak in oversupply and LTV reaches its bottom there; they then deteriorate in recession.
> A is wrong because it describes the recovery phase, when NOI bottoms and LTV peaks.
> C is wrong because it describes the expansion phase, which Denver apartments (rising occupancy, little new construction) resemble more than Phoenix office.
> 3. **B.** $\text{HPR} = [3{,}100{,}000 - 450{,}000 + (63{,}400{,}000 - 62{,}000{,}000)] / 62{,}000{,}000 = 4{,}050{,}000 / 62{,}000{,}000 = 6.5323\%$.
> The mortgage principal repayment is a financing flow and does not enter the property-level return.
> A is wrong because it divides by the ending appraised value, $4{,}050{,}000 / 63{,}400{,}000 = 6.3880\%$.
> C is wrong because it ignores capital expenditures, $4{,}500{,}000 / 62{,}000{,}000 = 7.2581\%$.
> 4. **A.** Invert the smoothing model: $R_t = [R_t^{*} - (1-a)R_{t-1}^{*}] / a = [-1.20 - 0.60 \times 2.40] / 0.40 = (-1.20 - 1.44) / 0.40 = -6.60\%$.
> The actual decline is more than five times the reported -1.20%, which is exactly the understated volatility of a smoothed index.
> B is wrong because it swaps $a$ and $1-a$: $[-1.20 - 0.40 \times 2.40] / 0.60 = -3.60\%$.
> C is wrong because it adds the lagged term instead of subtracting it, $-1.20/0.40 + (0.60/0.40) \times 2.40 = 0.60\%$, the sign error that appears in the curriculum's printed worked example but does not follow from the smoothing model.
> 5. **B.** Osei is correct: smoothing understates volatility and correlation with other asset classes, overstates the Sharpe ratio, and biases an optimizer toward too much real estate.
> Lindqvist is wrong on the direction: because appraisals lag transactions, an appraisal index understates returns in a rising market and overstates them in a falling one.
> A reverses the two comments, and C accepts Lindqvist's reversed claim.
> 6. **C.** A hedonic index uses every transaction and includes regression variables for characteristics such as size, age, quality, and location, which suits a heterogeneous market where most properties have sold only once.
> A is wrong because it attributes the hedonic method (characteristic regressors) to the repeat sales index.
> B is wrong because a repeat sales index requires the same property to sell at least twice and discards single sales, which would throw away most of the Denver data.

## Distractor design

1. B: concessions omitted (line item skipped); C: loss to lease skipped and vacancy applied to GPRI (wrong base, misread exhibit).
2. A: recovery-phase pattern (cycle phase swapped); C: expansion-phase pattern taken from the Denver clues (misread vignette).
3. A: ending value used as the denominator (wrong base); C: capex ignored (income leg misstated); decoy: principal repayment.
4. B: $a$ and $1-a$ swapped (wrong formula variant); C: lagged term added instead of subtracted (sign).
5. A and C: appraisal lag direction reversed in a rising market (sign of the bias).
6. A: hedonic construction attributed to repeat sales (methods swapped); B: repeat sales credited with using every transaction (data requirement misread).
