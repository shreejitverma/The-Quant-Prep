---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 1
title: "Halvard Re: Testing a Reserve Bond Against the Forward Curve"
los: [los-06-01-b, los-06-01-a, los-06-01-c, los-06-01-f]
difficulty: 4
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Halvard Re: Testing a Reserve Bond Against the Forward Curve

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tomas Berg, CFA, is a fixed-income analyst at Halvard Re, a Norwegian reinsurer that backs its claims reserves with default-free government bonds.
Halvard values its reserve portfolio off the government curve; the swap curve is used only by Halvard's treasury desk for hedging reports.
Berg's supervisor, Liv Aasen, has asked him to review Bond G, a holding that the reserving team plans to keep to maturity.

Exhibit 1: Government on-the-run par yields and swap rates (annual compounding, annual payments)

| Maturity (years) | Government par yield | Fixed-for-floating swap rate |
|---|---|---|
| 1 | 1.60% | 1.85% |
| 2 | 2.55% | 2.90% |
| 3 | 3.30% | 3.68% |
| 4 | 3.85% | 4.20% |

Exhibit 2: Other data collected by Berg

| Item | Value |
|---|---|
| Bond G: default-free government bond, annual coupon | 5.25% |
| Bond G: remaining maturity | exactly 3 years |
| Three-month government bill yield | 1.42% |
| Vesta Bank three-year senior note, yield to maturity | 4.15% |
| Duration of the reserve block Bond G supports | 2.8 years |

Berg first needs government spot rates, because Halvard's valuation system discounts every cash flow at its own spot rate.
He bootstraps them from the par yields in Exhibit 1.

Aasen then asks two questions about Bond G.
First, she wants the annualized return Halvard should expect on Bond G if it is held to maturity, every payment is made on time, each coupon is reinvested until maturity at the one-year rates implied by today's government forward curve, and those forward rates are realized.
Second, she wants to know how Bond G would perform over the next year under Berg's own rate projection.

Berg projects that one year from today the government one-year spot rate will be 4.00% and the government two-year spot rate will be 4.10%.
He plans to compute Bond G's one-year holding-period return under that projection, with the Year 1 coupon received at the end of the year and the bond sold immediately afterward.

Aasen makes the following comment.
"Your projected one-year rate of 4.00% is well above the one-year rate the forward curve implies for next year."
"So under your projection Bond G must be overvalued, and we should consider selling it."

Berg replies that he will check the comment against a full repricing of the bond before the reserving committee meets.

Finally, the treasury desk asks Berg for the current three-year swap spread, which it reports monthly as a barometer of bank credit and liquidity risk.
The desk also tracks the Vesta Bank note as a reference for bank funding costs.
Berg notes that the desk's template defines every spread in basis points and takes all government inputs from the on-the-run par curve rather than from bootstrapped rates.

## Questions

1. The three-year government spot rate Berg bootstraps from Exhibit 1 is closest to: (LOS: los-06-01-b)
   - A. 3.30%.
   - B. 3.34%.
   - C. 3.72%.
2. The expected annualized return on Bond G that answers Aasen's first question is closest to: (LOS: los-06-01-a)
   - A. 3.13%.
   - B. 3.28%.
   - C. 3.34%.
3. Under Berg's projection, Bond G's one-year holding-period return and the most appropriate valuation conclusion are: (LOS: los-06-01-c)
   - A. 1.78%; Bond G is undervalued.
   - B. 1.78%; Bond G is overvalued.
   - C. 4.68%; Bond G is undervalued.
4. The three-year swap spread Berg should report to the treasury desk is closest to: (LOS: los-06-01-f)
   - A. 34 bps.
   - B. 38 bps.
   - C. 47 bps.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Bootstrap by forward substitution, earliest to latest, using the government par yields: $z_1 = c_1 = 1.60\%$, so $DF_1 = 1/1.016 = 0.984252$.
> Two years: $1 = \frac{0.0255}{1.016} + \frac{1.0255}{(1+z_2)^2}$; the coupon term is $0.025098$, so $(1+z_2)^2 = 1.0255/0.974902 = 1.051901$, $z_2 = 2.5622\%$ and $DF_2 = 0.950660$.
> Three years: the coupon terms are $0.033 \times 0.984252 = 0.032480$ and $0.033 \times 0.950660 = 0.031372$, which sum to $0.063852$.
> $(1+z_3)^3 = 1.033/(1 - 0.063852) = 1.033/0.936148 = 1.103458$, so $z_3 = 1.103458^{1/3} - 1 = 3.3361\%$, about 3.34%.
> A is wrong because it takes the three-year par yield as the spot rate; on an upward-sloping curve the spot rate exceeds the par yield because the par bond's coupons are discounted at the lower early spot rates.
> C is wrong because it bootstraps the swap par rates instead of the government par yields, giving $z_3 = 3.7227\%$; Halvard values its reserve bonds off the government curve.
> 2. **C.** Price Bond G off the spot rates: $P = 5.25 \times 0.984252 + 5.25 \times 0.950660 + 105.25 \times 0.906242 = 5.1673 + 4.9910 + 95.3820 = 105.5402$.
> Implied one-year forwards: $f_{1,1} = (1.025622)^2/1.016 - 1 = 3.5336\%$ and $f_{2,1} = (1.033361)^3/(1.025622)^2 - 1 = 4.9013\%$.
> Terminal wealth with coupons reinvested at the forwards: $5.25(1.035336)(1.049013) + 5.25(1.049013) + 105.25 = 5.7019 + 5.5073 + 105.25 = 116.4592$.
> Expected return $= (116.4592/105.5402)^{1/3} - 1 = (1.103458)^{1/3} - 1 = 3.3361\%$, about 3.34%.
> The growth factor $1.103458$ is exactly $(1+z_3)^3$ from Question 1: compounding each cash flow forward at the implied forwards undoes its spot discounting, so a default-free bond held to maturity with forwards realized earns the spot rate of its maturity, not its yield to maturity.
> A is wrong because it ignores reinvestment income: $(3 \times 5.25 + 100)/105.5402 = 115.75/105.5402$, giving $3.1259\%$.
> B is wrong because it is Bond G's yield to maturity, $3.2808\%$, the rate that solves $105.5402 = \frac{5.25}{1+y} + \frac{5.25}{(1+y)^2} + \frac{105.25}{(1+y)^3}$; YTM equals expected return only if coupons are reinvested at the YTM, which the sloped forward curve contradicts.
> 3. **A.** In one year Bond G is a two-year bond; under Berg's projection its price is $\frac{5.25}{1.04} + \frac{105.25}{(1.041)^2} = 5.0481 + 97.1227 = 102.1708$.
> Holding-period return $= (5.25 + 102.1708)/105.5402 - 1 = 1.7818\%$, about 1.78%.
> If spot rates evolved as the forwards imply ($f_{1,1} = 3.5336\%$, $f_{1,2} = [(1.033361)^3/1.016]^{1/2} - 1 = 4.2152\%$), the price would be $5.0708 + 96.9081 = 101.9789$ and the return would equal $z_1 = 1.60\%$.
> Berg's projected return of 1.78% exceeds the 1.60% forward-consistent return, so his projection values the bond above its market-implied path and Bond G is undervalued: his higher projected one-year rate is outweighed by a projected two-year rate below $f_{1,2}$, which governs the 105.25 final cash flow.
> B is wrong because it adopts Aasen's reasoning, which compares only the one-year projection with $f_{1,1}$ and ignores the larger cash flow discounted at the two-year rate.
> C is wrong because it assumes the curve stays static: $\frac{5.25}{1.016} + \frac{105.25}{1.051901} = 105.2243$, and $(5.25 + 105.2243)/105.5402 - 1 = 4.6750\%$, which is the rolldown return, not Berg's projection.
> 4. **B.** Swap spread $=$ swap rate $-$ on-the-run government yield of the same maturity $= 3.68\% - 3.30\% = 0.38\%$, or 38 bps.
> A is wrong because it subtracts the bootstrapped three-year spot rate, $3.68\% - 3.3361\% = 0.3439\%$, instead of the on-the-run par yield the definition requires.
> C is wrong because it is the Vesta Bank note's I-spread, $4.15\% - 3.68\% = 0.47\%$, a bond yield over the swap curve rather than the swap rate over the government curve.
> The three-month bill yield and the reserve-block duration are not needed.

## Distractor design

1. A: par yield read as the spot rate (par vs spot); C: bootstrapped from the swap curve instead of the government curve (wrong benchmark).
2. A: coupons not reinvested (reinvestment term dropped); B: YTM taken as expected return despite a sloped forward curve (restrictive YTM assumptions ignored).
3. B: valuation judged on the one-year projection alone against $f_{1,1}$ (partial comparison planted in Aasen's comment); C: static-curve rolldown return used instead of the projection (wrong scenario).
4. A: spot rate used in place of the on-the-run par yield (spot vs par); C: I-spread of a bank bond reported as the swap spread (wrong spread definition).
