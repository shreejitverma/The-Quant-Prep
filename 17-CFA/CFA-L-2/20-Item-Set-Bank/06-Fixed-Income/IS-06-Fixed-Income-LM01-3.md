---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 1
title: "Brightwater Retirement System: Yield Curve Risk Report"
los: [los-06-01-i, los-06-01-j, los-06-01-k]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Brightwater Retirement System: Yield Curve Risk Report

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Priya Ramanathan, CFA, is head of risk at the Brightwater County Employees' Retirement System, a US public pension plan.
Each quarter she presents a yield curve risk report on the plan's USD 850 million government bond portfolio to the board's investment committee.
Her analyst, Devon Park, prepares the exhibits.

Exhibit 1: Government bond portfolio risk profile

| Measure | Value |
|---|---|
| Market value | USD 850 million |
| Key rate duration, 2-year | 0.45 |
| Key rate duration, 5-year | 1.30 |
| Key rate duration, 10-year | 2.95 |
| Benchmark effective duration | 4.90 |

The committee's first stress scenario is a twist: the 2-year key rate rises 35 bps, the 5-year key rate rises 10 bps, and the 10-year key rate falls 15 bps.

Ramanathan also reports sensitivities to three yield curve factors.
Park defines the unit movements at the 2-, 5- and 10-year key rates as follows: level $(+1, +1, +1)$, steepness $(-1, 0, +1)$, and curvature $(+1, 0, +1)$.
He derives the portfolio's level, steepness and curvature durations from the key rate durations in Exhibit 1.
The second stress scenario specifies factor changes of $\Delta x_L = +0.0040$, $\Delta x_S = -0.0020$ and $\Delta x_C = +0.0010$.

For communicating scenarios in standard-deviation terms, Park uses a statistical factor model.

Exhibit 2: Yield change per one standard deviation increase in each factor

| Maturity | Level | Steepness | Curvature |
|---|---|---|---|
| 5-year | -0.4180% | -0.0620% | 0.4050% |
| 10-year | -0.4610% | -0.2740% | 0.3380% |

The third scenario combines a 1.5 standard deviation decrease in the level factor with a 2.0 standard deviation increase in the steepness factor, with curvature unchanged.

Exhibit 3 reports the volatility of proportional monthly changes in government zero-coupon yields over the past five years.

Exhibit 3: Monthly standard deviation of proportional yield changes

| Maturity | 3-month | 2-year | 10-year | 30-year |
|---|---|---|---|---|
| Monthly standard deviation | 11.20% | 7.80% | 5.45% | 4.60% |

The committee wants annualized figures, and Park adds a note to Exhibit 3.

Park's note: "Because the 30-year yield has the lowest volatility in Exhibit 3, a 30-year bond would have the lowest price volatility of any holding in the portfolio."
"Volatility at the long end is driven mainly by uncertainty about monetary policy."

Ramanathan closes with the plan's economic outlook.
The chief investment officer expects the economy to keep expanding strongly, with inflation above target, and believes the central bank will raise its policy rate several times over the next year.
The plan's investment policy requires any yield curve trade to be duration neutral against the benchmark.

## Questions

1. Using Exhibit 1, the change in portfolio value under the first stress scenario is closest to: (LOS: los-06-01-i)
   - A. -USD 4.00 million.
   - B. -USD 1.32 million.
   - C. +USD 1.32 million.
2. Under the second stress scenario, the predicted percentage change in portfolio value is closest to: (LOS: los-06-01-i)
   - A. -2.72%.
   - B. -1.72%.
   - C. -1.38%.
3. Under the third scenario, the change in the 10-year yield is closest to: (LOS: los-06-01-i)
   - A. a decrease of 1.2395%.
   - B. an increase of 0.1435%.
   - C. an increase of 0.1870%.
4. The annualized volatility of the 2-year yield implied by Exhibit 3 is closest to: (LOS: los-06-01-j)
   - A. 2.25%.
   - B. 27.02%.
   - C. 93.60%.
5. Park's note is: (LOS: los-06-01-j)
   - A. correct.
   - B. incorrect with respect to price volatility only.
   - C. incorrect with respect to both price volatility and the driver of long-end volatility.
6. Given the chief investment officer's outlook, the yield curve change and investment-policy-compliant trade most consistent with that view are: (LOS: los-06-01-k)
   - A. bear flattening; a duration-neutral flattener that is long long-maturity bonds and short short-maturity bonds.
   - B. bear steepening; a duration-neutral steepener that is long short-maturity bonds and short long-maturity bonds.
   - C. bull steepening; an extension of portfolio duration beyond the benchmark.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** $\%\Delta P = -\sum KeyDur_k \Delta z_k = -[0.45(0.0035) + 1.30(0.0010) + 2.95(-0.0015)]$.
> The terms are $-0.001575 - 0.001300 + 0.004425 = +0.001550$, or $+0.155\%$.
> Value change $= 0.00155 \times 850 = +\text{USD } 1.3175$ million, about $+1.32$ million: the gain on the heavily weighted 10-year segment outweighs the losses at the short end.
> A is wrong because it applies the effective duration ($0.45 + 1.30 + 2.95 = 4.70$) to the average shift of $(35 + 10 - 15)/3 = 10$ bps, $-4.70 \times 0.0010 \times 850 = -4.00$ million, which ignores shaping risk.
> B is wrong because it drops the minus sign in the key rate duration model, reversing the direction.
> 2. **B.** From the unit movements, $D_L = 0.45 + 1.30 + 2.95 = 4.70$, $D_S = -0.45 + 2.95 = 2.50$, $D_C = 0.45 + 2.95 = 3.40$.
> $\%\Delta P = -[4.70(0.0040) + 2.50(-0.0020) + 3.40(0.0010)] = -[0.0188 - 0.0050 + 0.0034] = -0.0172$, or $-1.72\%$.
> A is wrong because it reverses the steepness sensitivity, $D_S = 0.45 - 2.95 = -2.50$, giving $-[0.0188 + 0.0050 + 0.0034] = -2.72\%$; the steepness movement lowers the short rate and raises the long rate.
> C is wrong because it omits the curvature term, $-[0.0188 - 0.0050] = -1.38\%$.
> 3. **B.** Exhibit 2 entries are yield changes per one standard deviation increase, so scale by the number of standard deviations and flip the sign for a decrease.
> Level: $-1.5 \times (-0.4610\%) = +0.6915\%$; steepness: $+2.0 \times (-0.2740\%) = -0.5480\%$; total $= +0.1435\%$.
> A is wrong because it does not flip the sign for the level decrease: $1.5(-0.4610\%) + 2.0(-0.2740\%) = -1.2395\%$.
> C is wrong because it flips the sign but ignores the number of standard deviations: $+0.4610\% - 0.2740\% = +0.1870\%$.
> 4. **B.** $\sigma_{annual} = \sigma_{monthly} / \sqrt{\Delta t} = 0.0780 / \sqrt{1/12} = 0.0780 \times 3.4641 = 27.02\%$.
> A is wrong because it multiplies by $\sqrt{1/12}$ instead of dividing, $0.0780 \times 0.2887 = 2.25\%$.
> C is wrong because it scales volatility linearly with time, $0.0780 \times 12 = 93.60\%$; variance, not standard deviation, scales linearly.
> 5. **C.** Yield volatility declines with maturity, as Exhibit 3 shows, but price volatility still rises with maturity because duration multiplies the smaller yield changes, so the 30-year bond would not have the lowest price volatility.
> Long-end yield volatility is driven mainly by uncertainty about the real economy and inflation; monetary policy uncertainty drives the short end.
> A is wrong because both sentences in the note are incorrect.
> B is wrong because it misses the second error, the reversal of the short-end and long-end drivers.
> 6. **A.** Tightening in a strong expansion pushes short yields up more than long yields: rising yields (bearish) with a smaller term spread (flattening).
> A duration-neutral flattener, long the long end and short the short end, gains when the spread narrows and complies with the duration-neutral policy.
> B is wrong because a hiking cycle is associated with bear flattening, not bear steepening, and the steepener loses as the spread narrows.
> C is wrong because bull steepening is the easing pattern of a recession, and extending duration beyond the benchmark breaches the duration-neutral requirement and loses when yields rise.

## Distractor design

1. A: effective duration applied to the average shift (shaping risk ignored); B: minus sign in the key rate duration model dropped (sign).
2. A: steepness sensitivity sign reversed (wrong formula variant); C: curvature term omitted (misread scenario).
3. A: no sign flip for a standard deviation decrease (sign); C: no scaling by the number of standard deviations (period/scale).
4. A: multiplied by the square root of the interval instead of dividing (wrong formula variant); C: linear time scaling of standard deviation (wrong formula variant).
5. A: yield volatility confused with price volatility; B: only one of two errors detected (drivers of short-end and long-end volatility swapped).
6. B: hiking cycle mapped to steepening (which end moves more); C: easing pattern and a non-duration-neutral trade (direction and constraint).
