---
type: cfa-itemset
topic: "Financial Statement Analysis"
topic_code: "03"
topic_slug: "03-Financial-Statement-Analysis"
lm: 5
title: "Kestrel Fabrication: A Short Screen on the Beneish Cutoff"
los: [los-03-05-c, los-03-05-d, los-03-05-e, los-03-05-h]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/financial-statement-analysis]
---

# Kestrel Fabrication: A Short Screen on the Beneish Cutoff

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Dana Okafor, CFA, is an analyst at Hollis Creek Capital, a long/short equity fund.
The fund's quantitative screen has flagged Kestrel Fabrication Inc., a US manufacturer of machined industrial components that reports under US GAAP with a December year end, as a possible short candidate.
Okafor must decide whether to recommend a position to the investment committee.

Kestrel's 2025 annual report discloses that management lengthened the estimated useful lives of its machining centers from 8 to 10 years effective 1 January 2025.
The CEO's annual bonus is based on growth in diluted EPS.
Okafor gathers the data in Exhibits 1 to 3.

Exhibit 1: Kestrel Fabrication, selected data ($ millions)

| Item | FY2024 | FY2025 |
|---|---|---|
| Sales | 1,840.0 | 2,208.0 |
| Accounts receivable, net | 276.0 | 405.0 |
| Depreciation expense | 96.0 | 102.0 |
| Property, plant, and equipment, net | 704.0 | 918.0 |
| Income before extraordinary items | 131.0 | 138.0 |
| Cash flow from operations | 118.0 | 12.0 |
| Total assets | 2,190.0 | 2,520.0 |

Exhibit 2: Beneish indices for FY2025 already computed by the fund's screen

| GMI | AQI | SGAI | LEVI |
|---|---|---|---|
| 1.08 | 1.15 | 0.92 | 1.10 |

Exhibit 3: Kestrel Fabrication, 31 December 2025 ($ millions unless noted)

| Item | Amount |
|---|---|
| Current assets | 900.0 |
| Current liabilities | 820.0 |
| Retained earnings | 360.0 |
| Earnings before interest and taxes | 196.0 |
| Total liabilities | 1,470.0 |
| Book value of equity | 1,050.0 |
| Shares outstanding (millions) | 60.0 |
| Share price ($) | 29.00 |

Okafor computes the four remaining Beneish indices (DSR, SGI, DEPI, and Accruals) from Exhibit 1 and uses the fund's standard cutoff of $-1.78$.
Her colleague Marcus Lindgren reviews her work and makes two statements.

Statement 1: "If we raised our cutoff from $-1.78$ to $-1.49$, we would misclassify fewer manipulators as non-manipulators."

Statement 2: "Even if Kestrel is flagged, the model only tells us that Kestrel's profile is associated with past manipulators, not that manipulation caused it, and its predictive power has declined as managers have learned to test their reports against it."

Because the investment committee will also ask whether Kestrel is at risk of financial distress, Okafor also computes Altman's Z-score using the ratio-form coefficients.

While reading the segment note, Okafor observes that the Aerospace segment, which the sell side values at the highest multiple, has reported stable operating margins since Kestrel began allocating a larger share of corporate overhead to its slower-growing Industrial segment in 2024.

Finally, Okafor notes that Kestrel's reported EPS has equaled the consensus estimate or exceeded it by exactly $0.01 in 11 of the last 12 quarters.
Lindgren comments: "That record shows management's forecasts are reliable, which is a sign of high earnings quality."

## Questions

1. Kestrel's FY2025 depreciation index (DEPI) is closest to: (LOS: los-03-05-d)
   - A. 0.83.
   - B. 1.20.
   - C. 1.23.
2. Kestrel's FY2025 Beneish M-score, and the conclusion at the fund's cutoff, are closest to: (LOS: los-03-05-d)
   - A. $-1.80$; not flagged as a likely manipulator.
   - B. $-1.76$; flagged as a likely manipulator.
   - C. $-0.72$; flagged as a likely manipulator.
3. Which of Lindgren's statements about the Beneish model is correct? (LOS: los-03-05-d)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both statements.
4. Kestrel's Altman Z-score at 31 December 2025, and its interpretation, are closest to: (LOS: los-03-05-h)
   - A. 1.80; high probability of bankruptcy.
   - B. 2.08; bankruptcy probability unclear.
   - C. 2.20; bankruptcy probability unclear.
5. Okafor's observation about the Aerospace and Industrial segments is most closely associated with which step in evaluating the quality of financial reports? (LOS: los-03-05-c)
   - A. Checking for signs that costs or revenues are being shifted between segments.
   - B. Identifying the accounting areas that require significant management judgment.
   - C. Comparing the company's financial statements and policies with prior years and with peers.
6. Okafor should most likely regard Kestrel's record against consensus EPS as: (LOS: los-03-05-e)
   - A. evidence of high earnings quality, because earnings that consistently meet expectations are persistent.
   - B. uninformative about earnings quality until an enforcement action or restatement confirms a problem.
   - C. a possible indicator of low earnings quality, because exactly meeting or narrowly beating benchmarks occurs more often than chance would suggest.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The depreciation rate is $\text{Depreciation}/(\text{Depreciation} + PPE)$.
> FY2024: $96.0/(96.0 + 704.0) = 96.0/800.0 = 0.1200$; FY2025: $102.0/(102.0 + 918.0) = 102.0/1{,}020.0 = 0.1000$.
> $DEPI = 0.1200/0.1000 = 1.2000$, consistent with the lengthened useful lives: the rate fell, so depreciation expense may be understated.
> A is wrong because it puts the current year in the numerator ($0.1000/0.1200 = 0.8333$); DEPI, like GMI, has the prior year on top.
> C is wrong because it omits depreciation from the denominator of each rate ($(96.0/704.0)/(102.0/918.0) = 0.1364/0.1111 = 1.2273$).
> 2. **B.** $DSR = (405.0/2{,}208.0)/(276.0/1{,}840.0) = 0.1834/0.1500 = 1.2228$; $SGI = 2{,}208.0/1{,}840.0 = 1.2000$; $DEPI = 1.2000$; $\text{Accruals} = (138.0 - 12.0)/2{,}520.0 = 0.0500$.
> Products: $0.920 \times 1.2228 = 1.1250$; $0.528 \times 1.08 = 0.5702$; $0.404 \times 1.15 = 0.4646$; $0.892 \times 1.2000 = 1.0704$; $0.115 \times 1.2000 = 0.1380$; $-0.172 \times 0.92 = -0.1582$; $4.679 \times 0.0500 = 0.2340$; $-0.327 \times 1.10 = -0.3597$.
> Sum $= 3.0843$, so $M = 3.0843 - 4.84 = -1.7557$, and $N(-1.7557) = 3.96\%$.
> Because $-1.76 > -1.78$, Kestrel is above the cutoff and is flagged, although only narrowly.
> A is wrong because it uses the inverted DEPI of 0.8333 from Question 1, which lowers the DEPI product to 0.0958 and gives $M = -1.7979$, just below the cutoff.
> C is wrong because it adds the SGAI and LEVI products instead of subtracting them ($-1.7557 + 2 \times (0.1582 + 0.3597) = -0.7199$).
> 3. **B.** Statement 2 is correct: accounting-based models establish association, not cause and effect, and their predictive power has declined because managers test the detectability of their tactics against the model.
> Statement 1 is incorrect: raising the cutoff to $-1.49$ flags fewer companies, so more manipulators are classified as non-manipulators, which increases Type I errors rather than reducing them.
> A is wrong because it reverses the trade-off between Type I and Type II errors.
> C is wrong because Statement 1 gets the direction of the trade-off wrong.
> 4. **B.** $NWC = 900.0 - 820.0 = 80.0$; market value of equity $= 60.0 \times 29.00 = 1{,}740.0$.
> Ratios: $NWC/TA = 80.0/2{,}520.0 = 0.0317$; $RE/TA = 360.0/2{,}520.0 = 0.1429$; $EBIT/TA = 196.0/2{,}520.0 = 0.0778$; $MVE/BVL = 1{,}740.0/1{,}470.0 = 1.1837$; $\text{Sales}/TA = 2{,}208.0/2{,}520.0 = 0.8762$.
> $Z = 1.2(0.0317) + 1.4(0.1429) + 3.3(0.0778) + 0.6(1.1837) + 1.0(0.8762) = 0.0381 + 0.2000 + 0.2567 + 0.7102 + 0.8762 = 2.0812$.
> $1.81 < 2.08 < 3.00$, so the probability of bankruptcy is unclear (the grey zone).
> A is wrong because it uses the book value of equity instead of the market value in the fourth ratio ($0.6 \times 1{,}050.0/1{,}470.0 = 0.4286$, $Z = 1.7995$), which moves Kestrel into the high-probability zone.
> C is wrong because it swaps the weights on retained earnings and EBIT ($1.2(0.0317) + 3.3(0.1429) + 1.4(0.0778) + 0.7102 + 0.8762 = 2.2048$).
> 5. **A.** Stable margins in the segment investors value most, coinciding with a shift of corporate overhead to a less closely watched segment, is the pattern the segment-shifting step looks for in a multi-segment company.
> B is wrong because identifying judgment-heavy areas (such as useful lives) is a separate step; the observation is about where costs are reported, not how they are estimated.
> C is wrong because the comparison step concerns changes in policies and ratios against prior periods and peers, not the allocation of costs across segments.
> 6. **C.** Exactly meeting or narrowly beating consensus is one of the curriculum's earnings quality indicators; the frequency of such results is higher than would be expected, which suggests earnings are being managed to the benchmark, and 11 of 12 quarters at a margin of zero or $0.01 is exactly that pattern.
> A is wrong because meeting expectations says nothing about the cash versus accruals composition that drives persistence, and Kestrel's accruals are large (OCF of 12.0 against income of 138.0).
> B is wrong because enforcement actions and restatements are external confirmations that arrive too late to be useful; the benchmark pattern is an indicator in its own right.

## Distractor design

1. A: prior year and current year inverted in the index (wrong formula variant); C: depreciation omitted from the rate denominator (wrong formula variant).
2. A: carries the inverted DEPI through, which flips the cutoff conclusion (misread index); C: SGAI and LEVI coefficients given positive signs (sign error).
3. A: Type I and Type II error trade-off reversed (direction error); C: accepts the reversed trade-off alongside the correct limitations.
4. A: book value of equity used instead of market value (misread exhibit, decoy number); C: weights on RE/TA and EBIT/TA swapped (wrong formula variant).
5. B: judgment-areas step confused with segment shifting (wrong step); C: comparison step confused with segment shifting (wrong step).
6. A: benchmark-meeting read as persistence (sign of the indicator reversed); B: external confirmations treated as the only indicator (timeliness error).
