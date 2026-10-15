---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 4
title: "Fenwick Mutual: Migration Drag Across the Maturity Spectrum"
los: [los-06-04-c, los-06-04-d, los-06-04-h]
difficulty: 3
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Fenwick Mutual: Migration Drag Across the Maturity Spectrum

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Ruth Okonkwo, CFA, is a fixed-income analyst at Fenwick Mutual Insurance, a property and casualty insurer with a large portfolio of investment-grade corporate bonds.
The chief investment officer, Paolo Grieco, is deciding where on the maturity curve to place a new allocation to Tarrant Chemicals, an issuer currently rated BBB.
Tarrant has two senior unsecured bonds outstanding, and Okonkwo compares them over a one-year horizon.

Exhibit 1: Tarrant Chemicals bonds

| Bond | Maturity | Yield to maturity | Expected modified duration at the one-year horizon | Coupon |
|---|---|---|---|---|
| S | 5 years | 4.60% | 3.70 | 4.25% |
| L | 10 years | 5.05% | 7.30 | 4.75% |

Okonkwo uses the one-year transition probabilities for BBB issuers in Exhibit 2 and the credit spreads by rating and maturity bucket in Exhibit 3.
She assumes that the Exhibit 3 spreads apply at the one-year horizon and that each bond's current spread equals the BBB spread for its maturity bucket.
Fenwick's policy ignores the probability of default in migration calculations for investment-grade bonds.

Exhibit 2: One-year transition probabilities from BBB (%)

| AAA | AA | A | BBB | BB | B | CCC, CC, C | D |
|---|---|---|---|---|---|---|---|
| 0.02 | 0.35 | 5.20 | 86.10 | 5.80 | 1.40 | 0.83 | 0.30 |

Exhibit 3: Credit spreads by rating and maturity bucket

| Rating | AAA | AA | A | BBB | BB | B | CCC, CC, C |
|---|---|---|---|---|---|---|---|
| Five-year bucket | 0.45% | 0.65% | 0.90% | 1.35% | 2.90% | 5.20% | 8.60% |
| Ten-year bucket | 0.60% | 0.85% | 1.15% | 1.70% | 3.50% | 6.30% | 9.90% |

Grieco comments, "Bond L pays 45 bps more than Bond S, so on a one-year view the long bond is the better use of the allocation."

Okonkwo also reviews a default model that Fenwick's risk department applies to Wexford Components, a smaller holding.
The model treats Wexford's equity as a call option on the company's assets, with a strike price equal to the face value of its zero-coupon debt, and it estimates the probability of default as the portion of the asset value distribution at debt maturity that lies below that face value.
Wexford recently entered a volatile new business line, and the risk department expects the volatility of its assets to rise sharply while the asset value and the face value of debt stay unchanged.

Finally, Grieco asks Okonkwo to compare two instruments backed by the same type of collateral, both offered by Sundby Hypotek Bank.
The first is a residential mortgage-backed security (RMBS) issued by a special purpose entity (SPE) that bought a static pool of mortgages from Sundby in a true sale.
The second is a Sundby covered bond backed by a cover pool of residential mortgages, with a conditional pass-through redemption structure.
Sundby services the mortgages in both structures.

## Questions

1. Ignoring the probability of default, the expected one-year return on Bond L, adjusted for credit migration, is closest to: (LOS: los-06-04-c)
   - A. 3.55%.
   - B. 3.75%.
   - C. 6.55%.
2. Regarding Grieco's comment, after adjusting for credit migration: (LOS: los-06-04-c)
   - A. Bond L offers the higher expected return, by about 45 bps.
   - B. Bond S offers the higher expected return, by about 19 bps.
   - C. Bond S offers the higher expected return, by about 39 bps.
3. Under the risk department's model for Wexford, the expected rise in asset volatility will most likely: (LOS: los-06-04-d)
   - A. increase the value of equity, decrease the value of debt, and increase the probability of default.
   - B. decrease the value of equity, decrease the value of debt, and increase the probability of default.
   - C. increase the value of equity, leave the value of debt unchanged because its face value is fixed, and increase the probability of default.
4. Which statement comparing the two Sundby instruments is most accurate? (LOS: los-06-04-h)
   - A. The RMBS investors have recourse to both Sundby and the mortgage pool, because Sundby continues to service the loans.
   - B. The covered bond investors have recourse to both Sundby and the cover pool, and Sundby must replace nonperforming mortgages in the cover pool, whereas the RMBS investors rely on the SPE's static pool.
   - C. If Sundby misses the covered bond's scheduled final payment, the bond defaults and payments are accelerated immediately.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Use the BBB row and the ten-year bucket, where Bond L's current spread is 1.70%.
> Price change for each migration $= -7.30 \times (s_i - 1.70\%)$: AAA $+8.0300\%$; AA $+6.2050\%$; A $+4.0150\%$; BBB $0$; BB $-13.1400\%$; B $-33.5800\%$; CCC, CC, C $-59.8600\%$.
> Weighted: $(0.0002)(8.0300) + (0.0035)(6.2050) + (0.0520)(4.0150) + (0.8610)(0) + (0.0580)(-13.1400) + (0.0140)(-33.5800) + (0.0083)(-59.8600)$.
> $= 0.0016 + 0.0217 + 0.2088 + 0 - 0.7621 - 0.4701 - 0.4968 = -1.4970\%$ (full precision; the rounded terms sum to $-1.4969\%$).
> Expected return $= 5.05\% - 1.4970\% = 3.5530\%$, about 3.55%.
> The 0.30% default probability is excluded under Fenwick's policy, so the transition probabilities used sum to 99.70%.
> B is wrong because it uses the five-year spread bucket for the ten-year bond (current spread 1.35%, drag $-1.2990\%$, return $3.7510\%$).
> C is wrong because it adds the migration drag to the yield instead of subtracting it ($5.05\% + 1.4970\% = 6.5470\%$).
> 2. **C.** Bond S uses the five-year bucket, current spread 1.35%, and price change $-3.70 \times (s_i - 1.35\%)$: AAA $+3.3300\%$; AA $+2.5900\%$; A $+1.6650\%$; BBB $0$; BB $-5.7350\%$; B $-14.2450\%$; CCC, CC, C $-26.8250\%$.
> Weighted: $0.0007 + 0.0091 + 0.0866 + 0 - 0.3326 - 0.1994 - 0.2226 = -0.6584\%$ (full precision; the rounded terms sum to $-0.6582\%$).
> Expected return on Bond S $= 4.60\% - 0.6584\% = 3.9416\%$.
> Difference: $3.9416\% - 3.5530\% = 0.3886\%$, so Bond S is ahead by about 39 bps.
> The longer duration of Bond L magnifies the downgrade-skewed spread changes, and its larger migration drag (1.50% versus 0.66%) more than offsets its 45 bp yield advantage, so Grieco's comment is wrong.
> A is wrong because it compares the yields to maturity only, which is Grieco's reasoning and ignores migration.
> B is wrong because it values both bonds with the five-year spread bucket, so Bond L's return is $3.7510\%$ and the gap is $3.9416\% - 3.7510\% = 0.1906\%$.
> 3. **A.** In the structural model, equity is a long call on the assets struck at the face value of debt, and debt equals a default-free bond minus a put on the assets struck at the same face value.
> Higher asset volatility raises the value of both options, so equity (the call) gains, debt (which is short the put) loses, and the probability mass of the asset distribution below the default barrier grows, so the probability of default rises.
> B is wrong because it treats equity as losing value with higher risk; limited liability caps the shareholders' downside, so the option value of equity rises with volatility.
> C is wrong because a fixed face value does not make the debt's value fixed; the debtholders have written the put to shareholders, and the value of that put rises with volatility.
> 4. **B.** A covered bond is a senior obligation of the bank with dual recourse to Sundby and the cover pool, and the cover pool is dynamic: nonperforming assets must be replaced.
> The mortgages stay on Sundby's balance sheet, whereas in the RMBS the true sale to a bankruptcy-remote SPE leaves the investors dependent on the pool and the deal structure, with the servicer creating operational and counterparty risk but no claim on Sundby.
> A is wrong because servicing the loans does not give investors recourse to the originator; the true sale is designed to separate the pool from Sundby's credit.
> C is wrong because it describes a hard bullet; under a conditional pass-through structure, a missed scheduled payment converts the covered bond into a pass-through security after the original maturity date, and payments are passed through as the cover pool generates cash.

## Distractor design

1. B: wrong spread bucket used (five-year spreads for a ten-year bond, misread exhibit); C: migration drag added to YTM instead of subtracted (sign).
2. A: yield comparison without the migration adjustment; B: five-year bucket applied to both bonds (misread exhibit carried from Question 1).
3. B: equity treated as a risky claim that loses value with volatility instead of a call option; C: debt treated as a fixed claim, ignoring the written put.
4. A: servicer role confused with recourse to the originator; C: hard bullet confused with conditional pass-through.
