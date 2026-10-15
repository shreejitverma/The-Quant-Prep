---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 4
title: "Pasir Ridge Life: Market-Level Multiples for an Equity Sleeve"
los: [los-05-04-l, los-05-04-m, los-05-04-p, los-05-04-r]
difficulty: 3
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Pasir Ridge Life: Market-Level Multiples for an Equity Sleeve

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Teo Kah Wei, CFA, heads equities at Pasir Ridge Life Assurance, a Singapore insurer that runs a global equity sleeve for its participating fund.
On 30 June 2026 he prepares a note for the investment committee on three questions: whether the US equity market is attractively priced, how two emerging-market holdings should be valued in an inflationary setting, and whether one industrial holding is still cheap.

Exhibit 1: US market data, 30 June 2026

| Item | Value |
|---|---|
| Broad US equity index level | 5,600 |
| Index EPS, next 12 months (consensus) | 280 |
| Index EPS, trailing 12 months | 256 |
| Yield on 10-year US Treasury note | 4.30% |
| Yield on A-rated US corporate bonds | 5.50% |
| Consensus five-year index EPS growth | 9.50% |

Teo applies the Yardeni model with a weight on long-term growth of 0.10, the historical estimate, and compares the result with the index's forward multiple.

For the emerging-market holdings, Teo uses a justified P/E that allows for incomplete pass-through of cost inflation to earnings.
Both holdings pay out essentially all their earnings, and he assigns each a real required return of 4.5%.

Exhibit 2: Inflation inputs

| Holding | Country | Expected inflation | Pass-through rate |
|---|---|---|---|
| Orchid Consumer Holdings | Singapore | 2.0% | 70% |
| Verano Energia SA | Brazil | 6.0% | 70% |

Verano's nominal required return, 10.5%, appears in the risk team's model, which adds expected inflation to the real rate.

Teo also reports the aggregate valuation of the sleeve's five largest positions, which make up the whole of a concentrated sub-portfolio.
The investment committee wants a single forward P/E that equals the sub-portfolio's total market value divided by its total forecast earnings.

Exhibit 3: Concentrated sub-portfolio, 30 June 2026

| Holding | Portfolio weight (by market value) | Forward P/E |
|---|---|---|
| Holding 1 | 30% | 14.0 |
| Holding 2 | 25% | 18.0 |
| Holding 3 | 20% | 25.0 |
| Holding 4 | 15% | 9.0 |
| Holding 5 | 10% | 40.0 |

Finally, Teo reviews Brightwater Industrial Corp., a US machinery maker whose fiscal year ends on 30 September.
Brightwater's shares trade at USD 85.10.
Consensus EPS is USD 4.00 for fiscal 2026 and USD 4.80 for fiscal 2027.
Over the past five years Brightwater's forward P/E has averaged 95% of the index's forward P/E, and Teo sees no change in its business mix, leverage or growth outlook relative to the index.
To make Brightwater's multiple comparable with the index's next-12-month multiple, he calendarizes its EPS by weighting the two fiscal-year estimates by the months of each that fall within the next 12 months.

His colleague Farah Iskandar, who manages the fund's fixed income book, reads the draft on 2 July 2026.
She notes that the Yardeni model uses a corporate bond yield, which contains a default premium but no equity risk premium, and that its five-year growth input may not be sustainable forever.
She asks Teo to keep the model as one input among several, not as a standalone signal.
Teo agrees to present each answer with the benchmark it rests on, so that the committee can see where a relative conclusion depends on the benchmark being fairly priced.

## Questions

1. The Yardeni model's justified forward P/E for the index, and the valuation it indicates for the US market, are closest to: (LOS: los-05-04-l)
   - A. 22.0; undervalued.
   - B. 23.3; undervalued.
   - C. 22.0; overvalued.
2. Verano's justified P/E is closest to: (LOS: los-05-04-p)
   - A. 8.1.
   - B. 11.5.
   - C. 15.9.
3. The forward P/E the investment committee requests for the sub-portfolio in Exhibit 3 is closest to: (LOS: los-05-04-r)
   - A. 16.0.
   - B. 16.5.
   - C. 19.1.
4. Based on its own historical relationship with the index, Brightwater's forward P/E and valuation are best described as: (LOS: los-05-04-m)
   - A. 18.5; undervalued.
   - B. 21.3; overvalued.
   - C. 20.3; overvalued.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The Yardeni model sets the earnings yield equal to the A-rated corporate bond yield less the growth weight times consensus long-term growth: $0.0550 - 0.10 \times 0.0950 = 0.0455$.
> Justified P/E $= 1/0.0455 = 21.9780$, or 22.0.
> The index's forward P/E is $5{,}600/280 = 20.0000$ (earnings yield 5.00%, above the justified 4.55%), so the market is undervalued by this model.
> B is wrong because it is the Fed model, $1/0.0430 = 23.2558$, which uses the Treasury yield and ignores growth.
> C is wrong because it reverses the direction: a justified P/E above the actual P/E indicates undervaluation.
> The trailing index P/E of $5{,}600/256 = 21.8750$ is also below 22.0, so the decoy trailing figure does not change the verdict.
> 2. **C.** Justified P/E $= 1/[\rho + (1-\lambda)I] = 1/(0.045 + 0.30 \times 0.060) = 1/0.0630 = 15.8730$, or 15.9.
> A is wrong because it uses the nominal required return in place of the real rate ($1/(0.105 + 0.018) = 1/0.1230 = 8.1301$), counting inflation twice.
> B is wrong because it multiplies inflation by the pass-through rate instead of by the fraction not passed through ($1/(0.045 + 0.70 \times 0.060) = 1/0.0870 = 11.4943$).
> For comparison, Orchid's justified P/E is $1/(0.045 + 0.30 \times 0.020) = 1/0.0510 = 19.6078$: with equal pass-through, the higher-inflation company earns the lower multiple.
> 3. **A.** The aggregate portfolio multiple is the weighted harmonic mean of the holdings' multiples, using market value weights.
> $\sum w_i/X_i = 0.30/14 + 0.25/18 + 0.20/25 + 0.15/9 + 0.10/40 = 0.0214 + 0.0139 + 0.0080 + 0.0167 + 0.0025 = 0.0625$ (unrounded 0.062484).
> Weighted harmonic mean $= 1/0.062484 = 16.0041$, or 16.0.
> B is wrong because it is the unweighted harmonic mean ($5/0.303095 = 16.4965$), which ignores the portfolio weights.
> C is wrong because it is the weighted arithmetic mean ($0.30 \times 14 + 0.25 \times 18 + 0.20 \times 25 + 0.15 \times 9 + 0.10 \times 40 = 19.05$), which is pulled up by the 40.0 multiple and does not equal total value over total earnings.
> 4. **A.** On 30 June, 3 months of fiscal 2026 remain, so NTM EPS $= (3/12) \times 4.00 + (9/12) \times 4.80 = 1.0000 + 3.6000 = 4.6000$.
> Forward P/E $= 85.10/4.6000 = 18.5000$.
> The historical benchmark is $0.95 \times 20.0 = 19.00$, so Brightwater trades about 2.6% below its customary relative multiple and appears undervalued; the justified price is $19.00 \times 4.60 = 87.40$.
> The conclusion relies on the historical relative relationship being stable, which Teo has checked, and on the index itself being fairly priced.
> B is wrong because it uses fiscal 2026 EPS alone ($85.10/4.00 = 21.2750$), a year that is three-quarters complete and mostly in the past.
> C is wrong because it reverses the weights ($(9/12) \times 4.00 + (3/12) \times 4.80 = 4.2000$, $85.10/4.2000 = 20.2619$).

## Distractor design

1. B: Fed model (Treasury yield, no growth) substituted for Yardeni; C: direction of misvaluation reversed.
2. A: nominal required return used where the real return belongs; B: pass-through rate used in place of one minus the pass-through rate.
3. B: unweighted harmonic mean that ignores portfolio weights; C: weighted arithmetic mean, which does not reproduce the aggregate multiple.
4. B: current fiscal-year EPS used instead of NTM EPS (period mismatch with the index's forward multiple); C: NTM month weights reversed.
