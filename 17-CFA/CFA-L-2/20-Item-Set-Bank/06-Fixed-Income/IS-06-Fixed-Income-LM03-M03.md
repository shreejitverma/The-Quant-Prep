---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 3
title: "Quillon Endowment Putable Rail Note"
los: [los-06-03-b, los-06-03-d, los-06-03-f, los-06-03-l]
difficulty: 3
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Quillon Endowment Putable Rail Note

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Keiko Varga, CFA, is a fixed-income analyst at the Quillon University Endowment.
The endowment keeps a liquidity sleeve of high-grade bonds to meet capital calls from its private equity managers.
The sleeve's guidelines emphasize protection against rising interest rates, because capital calls tend to cluster when rates are high and bond prices are depressed.
A dealer has offered Quillon a new three-year note issued by the Sarnath Rail Authority, a state agency whose debt carries an unconditional government guarantee.
Varga therefore treats the note as default-free and values it directly off the government curve.

The note pays a 3.75% annual coupon on a par value of 100.
The holder may sell the note back to Sarnath at par at the end of Year 1 and at the end of Year 2, and on no other dates.
The dealer's offer price is 100.60.

**Exhibit 1: Government par curve (annual coupon)**

| Maturity | Par rate |
|---|---|
| 1 year | 3.100% |
| 2 years | 3.600% |
| 3 years | 4.000% |
| 5 years | 4.350% |

Varga calibrates a binomial interest rate tree to Exhibit 1 at an interest rate volatility of 14%, so adjacent rates within a year differ by the factor $e^{0.28} = 1.3231$.

**Exhibit 2: One-year forward rates at 14% volatility**

| Node | Year 0 | Year 1 | Year 2 |
|---|---|---|---|
| Upper | 3.1000% | 4.6973% | 6.3172% |
| Middle | | | 4.7745% |
| Lower | | 3.5502% | 3.6085% |

On the same tree, an otherwise identical option-free Sarnath note is worth 99.3025.

To assess rate risk, Varga shifts the par curve in Exhibit 1 up and down by 30 bps in parallel, recalibrates the tree at 14% volatility each time, and revalues both notes.

**Exhibit 3: Values after parallel shifts of the par curve (per 100 of par)**

| Note | $PV_0$ | $PV_-$ (curve down 30 bps) | $PV_+$ (curve up 30 bps) |
|---|---|---|---|
| Putable note | to be determined | 101.2244 | 100.3385 |
| Option-free note | 99.3025 | 100.1403 | 98.4743 |

Varga's supervisor, Declan Moreau, the endowment's deputy chief investment officer, reviews her draft on 10 September and makes two statements.

Statement 1: "The put is only worth something if rates rise, and the tree shows rates rising in the upper nodes, so the value of the put is simply the amount by which the note's value exceeds par."

Statement 2: "The risk committee plans to raise our volatility assumption from 14% to 20%. That will reduce the note's value, because wider rate dispersion pushes the upper-node discount rates higher."

Varga replies that she will report the note's value, the value of the embedded put, and the note's effective convexity, and that she will address the volatility question separately.
She adds that the dealer's offer price is not an input to the tree valuation, although she will compare it with her model value before recommending a purchase.

## Questions

1. The value of the Sarnath putable note is closest to: (LOS: los-06-03-f)
   - A. 99.303
   - B. 100.317
   - C. 100.756
2. The value of the put option embedded in the Sarnath note is closest to: (LOS: los-06-03-b)
   - A. 0.76
   - B. 1.01
   - C. 1.45
3. The effective convexity of the Sarnath putable note is closest to: (LOS: los-06-03-l)
   - A. -56.13
   - B. 10.74
   - C. 56.13
4. Regarding Statement 2, if the volatility assumption rises from 14% to 20%, the value of the Sarnath putable note will most likely: (LOS: los-06-03-d)
   - A. decrease, as Moreau states.
   - B. remain unchanged, because the par curve and the option-free value are unchanged.
   - C. increase, because the value of the put rises with volatility.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Work backward through Exhibit 2, replacing any node value below the put price of 100 with 100 at Years 1 and 2 (V6 p.139).
> Year 2: $103.75/1.063172 = 97.5853 \to$ put at 100; $103.75/1.047745 = 99.0222 \to$ put at 100; $103.75/1.036085 = 100.1366$, not put.
> Year 1 upper: $(3.75 + 0.5 \times (100 + 100))/1.046973 = 99.0952 \to$ put at 100.
> Year 1 lower: $(3.75 + 0.5 \times (100 + 100.1366))/1.035502 = 100.2589$, not put.
> Year 0: $(3.75 + 0.5 \times (100 + 100.2589))/1.031 = 100.7560$.
> A is wrong because it never applies the put rule and returns the option-free value, 99.3025.
> B is wrong because it applies the put only at Year 2 and leaves the Year 1 upper node at 99.0952: $(3.75 + 0.5 \times (99.0952 + 100.2589))/1.031 = 100.3172$.
> 2. **C.** $V_{\text{put}} = V_{\text{putable}} - V_{\text{straight}} = 100.7560 - 99.3025 = 1.4535$, about 1.45 (V6 p.125).
> Statement 1 is wrong: the put is measured against the identical option-free note, not against par.
> A is wrong because it follows Statement 1 and computes $100.7560 - 100 = 0.7560$.
> B is wrong because it uses the Year-2-only value from the Question 1 error: $100.3172 - 99.3025 = 1.0147$.
> 3. **C.** $PV_0 = 100.7560$ from Question 1.
> $\text{EffCon} = (PV_- + PV_+ - 2 PV_0)/(\Delta\text{Curve}^2 \times PV_0) = (101.2244 + 100.3385 - 201.5120)/(0.003^2 \times 100.7560) = 0.0509/0.00090680 = 56.13$ (V6 p.158).
> The positive sign is expected: a putable bond's convexity is always positive, and it is large here because the put is near the money, so the put price cushions losses when rates rise while gains are uncapped.
> A is wrong because it computes $2 PV_0 - PV_- - PV_+$ in the numerator, reversing the sign and describing a callable-like profile.
> B is wrong because it reads the option-free row of Exhibit 3: $(100.1403 + 98.4743 - 198.6050)/(0.003^2 \times 99.3025) = 0.0096/0.00089372 = 10.74$.
> 4. **C.** Higher volatility widens the dispersion of future rates and raises the value of every embedded option, while the option-free value on a calibrated tree does not change (V6 p.130, p.132).
> The put is added to the straight value, so the putable note gains: recalibrating at 20% volatility gives 100.9736 against 100.7560 at 14%, with the option-free note still at 99.3025.
> A is wrong because it looks only at the upper nodes; wider dispersion also lowers the rates at the lower nodes, and because the put floors the note at 100 in the high-rate states, the holder keeps the gains in the low-rate states without bearing the full losses in the high-rate states.
> B is wrong because the straight value is volatility-invariant but the option value is not.

## Distractor design

- Q1: A omits the exercise rule (straight value); B applies the put at only one of the two exercise dates (partial exercise schedule).
- Q2: A measures the option against par instead of the straight bond (wrong formula variant, Statement 1); B carries the partial-exercise error from Question 1 (chained misread).
- Q3: A flips the numerator (sign); B uses the option-free row of the exhibit (misread exhibit).
- Q4: A attributes the volatility effect to discount rates rather than option value (wrong mechanism); B treats the bond as volatility-invariant because the curve is fixed.
