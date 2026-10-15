---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 4
title: "Aurelian Sovereign Fund: Spread Curves, Distress and Securitized Debt"
los: [los-06-04-a, los-06-04-f, los-06-04-g, los-06-04-h]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Aurelian Sovereign Fund: Spread Curves, Distress and Securitized Debt

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Hana Kobayashi, CFA, is a credit strategist at Aurelian Sovereign Fund, which invests surplus reserves in global fixed income.
Her senior portfolio manager, Lucas Brandt, asks for input on four positions ahead of a rebalancing decision.
For all calculations, Kobayashi assumes a benchmark government curve flat at 2.50%, no interest rate volatility, and default only at year ends.

Solvene Chemicals has two senior unsecured zero-coupon bonds outstanding, maturing in two years and four years.
Aurelian's research team expects Solvene's risk-neutral annual (hazard) probability of default to be 0.80% in Years 1 and 2, rising to 1.60% in Years 3 and 4 as a large debt-funded plant expansion comes on line.
Recovery is assumed to be 40% of the exposure.
Kobayashi has already valued the two-year bond at 94.2714, a yield of 2.9936% and a credit spread of 49.36 bps.

Exhibit 1: Solvene four-year zero, value assuming no default

| Item | Value |
|---|---|
| VND ($100/1.025^4$) | 90.5951 |
| Cumulative POD through Year 4 | not yet computed |

Marrow Retail is in severe distress.
Its three-year and seven-year zero-coupon bonds both trade at 35 per 100 of par, and every Marrow bond carries cross-default provisions.
Brandt remarks, "The seven-year spread is far below the three-year spread, so the market plainly regards Marrow's long bond as the safer credit."

Tervo Paper has a one-year, 4.50% annual coupon bond priced at 99.20.
Kobayashi assumes that in default Tervo bondholders would recover 45% of the exposure.
Tervo's historical one-year default rate, from agency data for its rating category, is 1.10%.

Last month, the spread on Solvene's four-year bond widened by 35 bps.
Over the same period, Solvene's rating, outlook and five-year CDS spread were unchanged, and the government curve did not move.
The bond is a small issue, the main dealer cut its inventory of Solvene bonds, and the quoted bid-offer spread doubled.

Aurelian is also offered two securitized positions.
Pool X backs an asset-backed security with 180,000 revolving credit card receivables from one bank's customers, all with similar terms, balances and short maturities.
Pool Y backs a commercial mortgage-backed security with 14 loans on office buildings, hotels and warehouses in different cities, each with its own lease profile.

Finally, Brandt considers a covered bond issued by Nordhavn Bank, which is rated BBB+; the covered bond is rated AA.
The prospectus describes the bond as a soft bullet.
Brandt wants one-line conclusions on each position before the committee votes on the rebalancing.

## Questions

1. The credit spread on the Solvene four-year zero-coupon bond is closest to: (LOS: los-06-04-g)
   - A. 49.20 bps.
   - B. 73.84 bps.
   - C. 98.38 bps.
2. The credit spread on Marrow's three-year bond, and the best interpretation of Marrow's spread curve, are closest to: (LOS: los-06-04-g)
   - A. 39.40%; the inversion is an optical effect of annualizing the same recovery-based loss over a shorter horizon.
   - B. 41.90%; the market expects default sooner on the three-year bond.
   - C. 39.40%; as Brandt says, the market regards the seven-year bond as the safer credit.
3. The risk-neutral probability of default implied by the price of the Tervo bond is closest to: (LOS: los-06-04-a)
   - A. 1.10%.
   - B. 4.74%.
   - C. 4.91%.
4. The widening in Solvene's four-year spread last month is most likely attributable to a change in: (LOS: los-06-04-f)
   - A. the expected default loss.
   - B. liquidity.
   - C. the expected real rate.
5. The most appropriate credit analysis approaches for Pool X and Pool Y, respectively, are: (LOS: los-06-04-h)
   - A. statistics-based analysis of the existing book, and loan-by-loan analysis.
   - B. portfolio-based analysis, and loan-by-loan analysis.
   - C. loan-by-loan analysis, and portfolio-based analysis.
6. Which statement about the Nordhavn covered bond is most accurate? (LOS: los-06-04-h)
   - A. If Nordhavn misses the scheduled final payment, the bond defaults and payments are accelerated immediately.
   - B. The cover pool is fixed at issuance, which is the main reason the bond is rated above Nordhavn.
   - C. Investors have recourse to both Nordhavn and the cover pool, and a missed scheduled final payment defers default to a new final maturity, typically up to one year later.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Build the CVA table with the stepped hazard; exposure is $100/1.025^{4-t}$ and LGD is 60% of exposure.
> PODs: $0.80\%$; $0.80\% \times 99.2000\% = 0.7936\%$; $1.60\% \times 98.4064\% = 1.5745\%$; $1.60\% \times 96.8319\% = 1.5493\%$ (cumulative 4.7174%).
> Date 1: exposure 92.8599, LGD 55.7160, expected loss 0.4457, PV $0.4457 \times 0.975610 = 0.4349$.
> Date 2: exposure 95.1814, LGD 57.1089, expected loss 0.4532, PV 0.4314.
> Date 3: exposure 97.5610, LGD 58.5366, expected loss 0.9217, PV 0.8559.
> Date 4: exposure 100.0000, LGD 60.0000, expected loss 0.9296, PV 0.8422.
> $CVA = 2.5642$; fair value $= 90.5951 - 2.5642 = 88.0308$; yield $= (100/88.0308)^{1/4} - 1 = 3.2384\%$; spread $= 3.2384\% - 2.50\% = 73.84$ bps.
> The spread rises from 49.36 bps at two years to 73.84 bps at four years because the expected hazard rises with maturity, the classic upward-sloping curve.
> A is wrong because it applies the 0.80% hazard in all four years (CVA 1.7187, spread 49.20 bps), ignoring the step-up.
> C is wrong because it applies the 1.60% hazard in all four years (CVA 3.3962, spread 98.38 bps).
> 2. **A.** With default near-certain and cross-default provisions, each bond trades at the recovery value regardless of maturity, so CVA $= VND - 35$.
> Three-year yield $= (100/35)^{1/3} - 1 = 41.8983\%$, spread $= 41.8983\% - 2.50\% = 39.3983\%$.
> Seven-year yield $= (100/35)^{1/7} - 1 = 16.1805\%$, spread $= 13.6805\%$.
> The steep inversion comes from annualizing the same dollar outcome over three years versus seven; it is not a view that the long bond is safer.
> B is wrong because 41.90% is the yield, not the spread, and the inversion does not reflect a different expected default date across maturities, since cross-default links all of them.
> C is wrong because it takes Brandt's reading at face value, treating the optical inversion as a ranking of credit risk.
> 3. **C.** Exposure $= 104.50$; recovery $= 0.45 \times 104.50 = 47.025$.
> Discount risk-neutral expected payoffs at the risk-free rate: $99.20 = [104.50(1 - P^*) + 47.025P^*]/1.025$.
> $101.68 = 104.50 - 57.475P^*$, so $P^* = 2.82/57.475 = 4.9065\%$.
> A is wrong because 1.10% is the historical (actual) default rate, which excludes the default timing risk premium and the liquidity and tax effects built into the risk-neutral probability.
> B is wrong because it sets recovery at 45% of par (45.00) instead of 45% of the exposure: $P^* = 2.82/59.50 = 4.7395\%$.
> 4. **B.** The benchmark did not move, and the unchanged rating, outlook and CDS spread point to no change in the expected default loss.
> A small issue, reduced dealer inventory and a doubled bid-offer spread identify the liquidity component of the spread, the LVA piece of the XVA family.
> A is wrong because the credit signals (rating, outlook, CDS) show no change in the probability of default or the loss given default.
> C is wrong because the expected real rate is a macro factor in the benchmark yield, not in the spread, and the benchmark curve was unchanged.
> 5. **A.** Pool X is granular (180,000 obligations), homogeneous and short-term, which suits a statistics-based analysis of the existing book.
> Pool Y is non-granular (14 loans) and heterogeneous (mixed property types and locations), which requires loan-by-loan analysis.
> B is wrong because the portfolio-based approach is for medium-term, granular, homogeneous pools whose composition changes over time, such as auto loans; the short-term card receivables are analyzed from the book.
> C is wrong because loan-by-loan analysis of 180,000 similar receivables is inefficient, and a 14-loan heterogeneous CMBS pool cannot be modeled as a statistical portfolio.
> 6. **C.** Covered bonds are senior obligations with dual recourse to the issuing bank and a dynamic cover pool.
> Under a soft bullet, a missed scheduled final payment delays default to a new final maturity, usually up to one year later.
> Dual recourse, cover pool maintenance and regulation lift the rating several notches above the bank's.
> A is wrong because it describes a hard bullet.
> B is wrong because the cover pool is dynamic: nonperforming assets must be replaced, which is part of why the rating exceeds the issuer's.

## Distractor design

1. A: low-hazard years extended to the full maturity (step ignored); C: high-hazard years extended to the full maturity.
2. B: yield reported as spread plus a timing story the cross-default feature rules out; C: optical inversion misread as a risk ranking.
3. A: actual default rate substituted for the risk-neutral rate; B: recovery applied to par instead of to the exposure.
4. A: spread move attributed to credit despite stable credit signals; C: macro factor of the benchmark attributed to the spread.
5. B: portfolio approach applied to a short-term book; C: approaches reversed (granularity and homogeneity misread).
6. A: hard bullet confused with soft bullet; B: dynamic cover pool described as static.
