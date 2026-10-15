---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 3
title: "Halvorsen Mutual Life Agency Bond Review"
los: [los-06-03-a, los-06-03-b, los-06-03-d, los-06-03-e, los-06-03-f]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Halvorsen Mutual Life Agency Bond Review

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Ingrid Solberg, CFA, is a fixed-income analyst at Halvorsen Mutual Life, a life insurer that matches long-dated annuity liabilities with high-quality bonds.
The investment committee has asked her to value three new bonds issued by Nordhavn Export Finance, an agency whose debt carries an explicit and unconditional sovereign guarantee.
Solberg therefore treats all three bonds as default-free and values them directly off the sovereign curve.
All three bonds pay a 4.60% annual coupon, have a par value of 100, and settle today.

- Bond A is a three-year option-free bond.
- Bond B is a three-year bond that the issuer may redeem at 101 at the end of Year 1 or at 100 at the end of Year 2, with no other redemption dates.
- Bond C is a two-year bond that gives the holder the right, at the end of Year 2, to extend the maturity by one year at the same 4.60% coupon.

**Exhibit 1: Sovereign par curve (annual coupon)**

| Maturity | Par rate |
|---|---|
| 1 year | 3.200% |
| 2 years | 3.700% |
| 3 years | 4.100% |
| 5 years | 4.450% |

Solberg builds a binomial interest rate tree calibrated to Exhibit 1 with an interest rate volatility of 12%.
She confirms that the tree reprices each par bond at 100 and that adjacent rates within a year differ by the factor $e^{0.24} = 1.2712$.

**Exhibit 2: One-year forward rates at 12% volatility**

| Node | Year 0 | Year 1 | Year 2 |
|---|---|---|---|
| Upper | 3.2000% | 4.7280% | 6.2242% |
| Middle | | | 4.8961% |
| Lower | | 3.7191% | 3.8514% |

On the tree, Solberg values Bond A at 101.392.
Halvorsen's internal hurdle yield for agency paper is 4.25%, which the committee uses only for asset-liability matching and not for valuation.

Tomas Weir, the chief investment officer, reviews her draft on 2 September and makes two statements.

Statement 1: "Bond C is really just a three-year bond with a put attached, so you can value it with the same tree you used for Bond B."

Statement 2: "If our risk team raises the volatility assumption from 12% to 18%, neither Bond B nor Bond C will change in value, because the par curve that calibrates the tree has not changed."

Solberg replies on 3 September with a view on the shape of the curve.

Statement 3: "Our economists expect the curve to flatten, with the one-year rate unchanged and the two-year and three-year par rates falling. That should make the options in both Bond B and Bond C more valuable, because lower forward rates raise both bonds' values."

Weir asks Solberg to report the value of each embedded option separately so that the committee can see what Halvorsen is paying for, or being paid for, in each structure.
He specifies that every embedded option is to be measured as the difference between that bond's own tree value and the value of Bond A, since Bond C is value-equivalent to a three-year bond carrying an investor option.
He also reminds her that the committee will only buy Bond B if it is priced below Bond A by at least the value of the call it gives away.

## Questions

1. Bond C is most accurately described as equivalent to a three-year 4.60% bond that is: (LOS: los-06-03-a)
   - A. putable at par at the end of Year 2 only.
   - B. putable at par at the end of Year 1 and at the end of Year 2.
   - C. callable at par at the end of Year 2 only.
2. The value of Bond B is closest to: (LOS: los-06-03-f)
   - A. 100.878
   - B. 101.224
   - C. 101.392
3. The value of Bond C is closest to: (LOS: los-06-03-f)
   - A. 101.392
   - B. 101.877
   - C. 101.936
4. Using Weir's measurement convention, the value of the extension option embedded in Bond C is closest to: (LOS: los-06-03-b)
   - A. 0.168
   - B. 0.485
   - C. 0.653
5. Regarding Statement 2, if the volatility assumption rises from 12% to 18%, the values of Bond B and Bond C most likely: (LOS: los-06-03-d)
   - A. fall and rise, respectively.
   - B. remain unchanged, because the par curve is unchanged.
   - C. both rise, because option values increase with volatility.
6. If the flattening described in Statement 3 occurs, then under Weir's measurement convention the value of the call option in Bond B and the value of the extension option in Bond C will most likely: (LOS: los-06-03-e)
   - A. increase and decrease, respectively.
   - B. both increase.
   - C. decrease and increase, respectively.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Extending a 4.60% bond at the end of Year 2 is the same cash-flow decision as declining to put a three-year 4.60% bond at par at the end of Year 2: the holder extends (keeps the bond) exactly when the Year 2 value of the final year exceeds 100, and otherwise takes par (V6 p.122).
> The extension right belongs to the investor, so it is a put, and there is only one decision date.
> B is wrong because it adds a Year 1 exercise date that the indenture does not grant; that structure is worth more (101.936 on the tree).
> C is wrong because a call is an issuer option, whereas the extension is exercised by the holder.
> 2. **B.** Year 2 values: $104.60/1.062242 = 98.4710$; $104.60/1.048961 = 99.7177$; $104.60/1.038514 = 100.7208 \to$ called at 100.
> Year 1 upper: $(4.60 + 0.5 \times (98.4710 + 99.7177))/1.047280 = 99.0130$, below 101, not called.
> Year 1 lower: $(4.60 + 0.5 \times (99.7177 + 100))/1.037191 = 100.7132$, below the Year 1 call price of 101, so not called.
> Year 0: $(4.60 + 0.5 \times (99.0130 + 100.7132))/1.032 = 101.2239$, about 101.224.
> A is wrong because it applies a call price of 100 at Year 1, resetting the 100.7132 node to 100: $(4.60 + 0.5 \times (99.0130 + 100))/1.032 = 100.878$.
> C is wrong because it is the straight value of Bond A, obtained by never applying the call rule.
> 3. **B.** Value Bond C as a three-year bond putable at par at Year 2 only.
> Year 2: $98.4710 \to 100$ (put) and $99.7177 \to 100$ (put); $100.7208$ stays (the holder extends).
> Year 1 upper: $(4.60 + 0.5 \times (100 + 100))/1.047280 = 99.8778$, and there is no put at Year 1.
> Year 1 lower: $(4.60 + 0.5 \times (100 + 100.7208))/1.037191 = 101.1967$.
> Year 0: $(4.60 + 0.5 \times (99.8778 + 101.1967))/1.032 = 101.8772$, about 101.877.
> A is wrong because it is the straight value, obtained by skipping the Year 2 exercise test.
> C is wrong because it also puts the 99.8778 node at Year 1: $(4.60 + 0.5 \times (100 + 101.1967))/1.032 = 101.936$.
> 4. **B.** $V_{\text{put}} = V_{\text{putable}} - V_{\text{straight}} = 101.8772 - 101.3923 = 0.4849$, about 0.485 (V6 p.125).
> A is wrong because 0.168 measures Bond C against the two-year option-free note (101.7089) instead of against Bond A, which is not the convention Weir specified; on this tree that figure is also exactly the call option in Bond B, $101.3923 - 101.2239 = 0.1684$, because the Year 1 call at 101 never binds and both options pay off only at the Year 2 nodes.
> C is wrong because $101.8772 - 101.2239 = 0.653$ uses the callable Bond B as the base instead of the straight Bond A, which adds the two option values together.
> 5. **A.** Volatility raises the value of every embedded option while the straight value (101.392) is unaffected (V6 p.130, p.131).
> The call is subtracted, so Bond B falls; the extension (put) is added, so Bond C rises.
> Recalibrating at 18% gives Year 1 rates of 4.9792% and 3.4739%, a callable value of 101.112 and an extendible value of 101.989, confirming both directions.
> B is wrong because the straight bond is insensitive to volatility but the option values are not.
> C is wrong because it applies the option's direction to the bond without the sign: a more valuable call lowers the callable bond.
> 6. **A.** Flattening lowers the one-period forward rates on the tree, which creates more nodes where calling pays and fewer where extending (declining the put) is valuable relative to taking par (V6 p.134, p.136).
> Recalibrating to par rates of 3.20%, 3.50% and 3.70% at 12% volatility: straight 102.519, Bond B 101.867, Bond C 102.646, so, each measured against the straight bond as Weir specified, the call rises from 0.168 to 0.651 and the extension option falls from 0.485 to 0.127.
> B is wrong because it applies level logic (both bond prices rise) to option values, which move in opposite directions under a shape change.
> C is wrong because it reverses both directions, which is the effect of steepening.

## Distractor design

- Q1: B converts a single extension date into a Bermudan put (wrong exercise schedule); C assigns the investor's option to the issuer (option holder confusion).
- Q2: A misreads the call schedule and calls at 100 in Year 1 (misread exhibit); C omits the exercise rule and returns the straight value.
- Q3: A omits the exercise rule (straight value); C adds a Year 1 put date (wrong exercise schedule).
- Q4: A uses the two-year option-free note as the base instead of Bond A, which is also numerically the call value in Bond B (wrong base bond); C nets the putable against the callable instead of the straight bond (wrong formula variant).
- Q5: B treats the tree as volatility-invariant because the curve is fixed; C forgets that a call is subtracted (sign error).
- Q6: B applies level logic to a shape change; C reverses the shape effect (sign error).
