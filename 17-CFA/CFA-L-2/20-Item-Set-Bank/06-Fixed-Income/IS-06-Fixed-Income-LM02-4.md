---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 2
title: "Harrow Capital: Term Structure Model Governance"
los: [los-06-02-i, los-06-02-f]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Harrow Capital: Term Structure Model Governance

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Harrow Capital is an asset manager that runs several fixed-income funds, including a fund that holds callable and putable corporate bonds.
Under Harrow's model governance policy, every interest rate model used for valuation must be approved by the model risk committee and documented by the compliance function.
Rachel Adeyemi, CFA, is the model risk officer, and she is preparing a review of three term structure models proposed by the fixed-income desk.

The desk has estimated parameters for two equilibrium models, which it wants to use for scenario analysis, and it has submitted the parameters shown in Exhibit 1.

Exhibit 1: Proposed model parameters (annualized)

| Parameter | Vasicek | Cox-Ingersoll-Ross (CIR) |
|---|---|---|
| Speed of mean reversion, $k$ | 0.25 | 0.25 |
| Long-run mean rate, $\theta$ | 3.50% | 3.50% |
| Volatility parameter, $\sigma$ | 0.90% | 6.00% |
| Current short rate, $r$ | 5.00% | 5.00% |

For each model, the desk's documentation writes the short-rate process as $dr = \text{drift} \times dt + \text{stochastic term}$.
Adeyemi asks the desk to report two quantities for the committee: the expected change in the short rate per year implied by the drift term, and the volatility of the short rate at today's level implied by the stochastic term.

For the valuation of the fund's bonds with embedded options, the desk wants a third model.
The head of the desk, Tomasz Nowak, sets out two requirements.
First, the model must reproduce today's observed benchmark curve exactly, because the fund's bonds must be marked consistently with market prices.
Second, because the fund's documentation prohibits valuations that rely on negative interest rates, the model must be incapable of generating negative short rates.

Before approving the valuation model, Adeyemi runs a consistency test.
She asks the desk to value a two-year, 6.00% annual-coupon, option-free agency bond whose credit risk matches the benchmark curve.
The benchmark par curve is 3.25% for one year and 3.50% for two years, and the three-year par rate is 3.80%.
The desk values the bond on a lognormal binomial lattice calibrated to the benchmark curve at a 30% volatility assumption, which the desk says reflects current conditions better than the 15% it used last year.
Adeyemi writes in her review that she expects the lattice value to agree with a value computed directly from the benchmark curve, and that any disagreement will be escalated to compliance as a model error.

Nowak argues that the lattice value should differ from the spot-curve value because 30% volatility is very high.
Adeyemi disagrees and asks the desk for the value that a correctly calibrated lattice must produce.
She adds that the answer will determine whether the lattice is released for use on the fund's callable and putable holdings.

## Questions

1. Using Exhibit 1, the expected change in the short rate over the next year implied by the Vasicek drift term is closest to: (LOS: los-06-02-i)
   - A. -1.5000%.
   - B. -0.3750%.
   - C. +0.3750%.
2. Using Exhibit 1, the volatility of the short rate at today's level implied by the CIR stochastic term is closest to: (LOS: los-06-02-i)
   - A. 0.3000%.
   - B. 1.3416%.
   - C. 6.0000%.
3. The model that best meets both of Nowak's requirements, and its classification, is: (LOS: los-06-02-i)
   - A. Ho-Lee, an arbitrage-free model.
   - B. Kalotay-Williams-Fabozzi (KWF), an arbitrage-free model.
   - C. Cox-Ingersoll-Ross (CIR), an equilibrium model.
4. The value of the 6.00% agency bond that a correctly calibrated lattice at 30% volatility must produce is closest to: (LOS: los-06-02-f)
   - A. 104.7406.
   - B. 104.7492.
   - C. 104.7549.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The Vasicek drift is $k(\theta - r_t) = 0.25 \times (3.50\% - 5.00\%) = 0.25 \times (-1.50\%) = -0.3750\%$ per year.
> The rate is above its long-run mean, so mean reversion pulls it down.
> A is wrong because it omits the speed of mean reversion $k$ and reports the full gap $\theta - r_t = -1.5000\%$.
> C is wrong because it reverses the sign by computing $k(r_t - \theta)$, which would push the rate away from its long-run mean.
> 2. **B.** The CIR stochastic term is $\sigma\sqrt{r_t}\,dZ$, so the volatility at today's rate is $0.06 \times \sqrt{0.05} = 0.06 \times 0.223607 = 0.013416$, or 1.3416%.
> A is wrong because it scales $\sigma$ by the rate level itself, $0.06 \times 0.05 = 0.3000\%$, a proportional (lognormal-style) volatility rather than square-root scaling.
> C is wrong because it treats $\sigma$ as a constant volatility, as in the Vasicek model, ignoring the $\sqrt{r_t}$ term.
> 3. **B.** Reproducing today's curve exactly requires an arbitrage-free model, which takes market prices as given and uses a time-dependent drift; of the arbitrage-free models, KWF models $d\ln(r_t)$, so the short rate is lognormal and cannot become negative.
> A is wrong because Ho-Lee fits the curve but models $dr_t$ with a normally distributed stochastic term, so negative rates are possible.
> C is wrong because CIR cannot produce negative rates but is an equilibrium model with few parameters that generally does not match the observed curve.
> 4. **C.** For an option-free bond, a lattice calibrated to the benchmark curve must return the spot-curve value at any volatility, because both methods are arbitrage free.
> Spot rates: $z_1 = 3.2500\%$; $1 = 0.035/1.0325 + 1.035/(1+z_2)^2$ gives $z_2 = 3.5044\%$.
> Value: $6/1.0325 + 106/1.035044^2 = 5.81114 + 98.94372 = 104.7549$.
> A check calibration at 30% gives Time 1 rates of 4.8696% and 2.6725%, and $[6 + 0.5(106/1.048696 + 106/1.026725)]/1.0325 = 104.7549$, the same value.
> A is wrong because it discounts both cash flows at the two-year spot rate, $6/1.035044 + 106/1.035044^2 = 104.7406$, over-discounting the first coupon.
> B is wrong because it discounts both cash flows at the 3.50% two-year par yield, $6/1.035 + 106/1.035^2 = 104.7492$, the single-YTM error; Nowak's claim that high volatility changes the value is also wrong, since calibration absorbs the volatility assumption for option-free bonds.

## Distractor design

1. A: speed of mean reversion $k$ omitted; C: sign of the mean-reversion drift reversed.
2. A: proportional ($\sigma r$) volatility used instead of square-root ($\sigma\sqrt{r}$) scaling; C: CIR treated as a constant-volatility model like Vasicek.
3. A: curve-fitting requirement met but negative rates possible (normal versus lognormal short rate); C: non-negativity met but equilibrium model does not fit the observed curve.
4. A: every cash flow discounted at the longest spot rate; B: single-YTM discounting at the par yield instead of spot rates.
