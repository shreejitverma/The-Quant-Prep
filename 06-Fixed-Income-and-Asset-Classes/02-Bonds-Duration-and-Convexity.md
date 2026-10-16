---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: core
status: draft
prereqs: [discounting-and-yield-curves]
est_hours: 4
sources: [Tuckman and Serrat - Fixed Income Securities 4th ed. chapters 3 to 5, Fabozzi - Handbook of Fixed Income Securities]
---

# Bonds, Duration and Convexity

> [!info] Draft
> Written and computed in this session; the independent review required for `solid` has not happened.

## TL;DR

- Price is a decreasing, convex function of yield: $P(y)=\sum_i c_i(1+y/m)^{-mt_i}$.
- Modified duration $D_{mod}=-\frac1P\frac{dP}{dy}=D_{Mac}/(1+y/m)$ and DV01 $=P\,D_{mod}\times10^{-4}$.
- Convexity $C=\frac1P\frac{d^2P}{dy^2}$ gives the second-order fix: $\frac{\Delta P}{P}\approx -D_{mod}\Delta y+\frac12C\,\Delta y^2$.
- Duration is the weighted average time of cash flows, weights being present-value shares.
- Clean price excludes accrued interest; settlement is the dirty price.

## Learning objectives

- Price a bond from yield and compute accrued interest, clean and dirty price.
- Derive Macaulay and modified duration and convexity, and use the second-order approximation.
- Compute DV01 and hedge ratios between two bonds.
- Know when duration breaks: large shocks, non-parallel moves, embedded options.

## Core concepts

### Price, yield, accrued

With $m$ coupons per year and yield $y$ (compounded $m$ times a year), price is $P=\sum_i c_i(1+y/m)^{-m t_i}$.
Between coupons, the dirty price is the clean price plus accrued interest, and accrued is coupon times the day-count fraction of the elapsed period.
The quoted (clean) price is smooth in time; the dirty price jumps down by the coupon on the coupon date.

### Duration

Differentiate: $\dfrac{dP}{dy}=-\dfrac{1}{1+y/m}\sum_i t_i\,c_i(1+y/m)^{-mt_i}$.
So $D_{mod}=-\dfrac1P\dfrac{dP}{dy}=\dfrac{D_{Mac}}{1+y/m}$ where $D_{Mac}=\sum_i t_i\,w_i$ and $w_i=c_i(1+y/m)^{-mt_i}/P$ are PV weights summing to 1.
A zero-coupon bond has $D_{Mac}$ equal to its maturity.
DV01 is the price change for one basis point: $DV01\approx P\cdot D_{mod}\cdot10^{-4}$.

### Convexity

Second derivative: $\dfrac{d^2P}{dy^2}=\sum_i c_i\,t_i\!\left(t_i+\tfrac1m\right)(1+y/m)^{-mt_i-2}$.
Convexity $C=\frac1P\frac{d^2P}{dy^2}$, and the Taylor expansion gives
$$\frac{\Delta P}{P}\approx -D_{mod}\,\Delta y+\tfrac12\,C\,(\Delta y)^2.$$
Convexity is positive for bullets, so for a symmetric yield move the bond gains more than it loses; it grows roughly with the square of maturity.
For a long position convexity is valuable and is paid for in lower yield; a barbell has more convexity than a bullet of the same duration.

### Limits of duration

- Duration assumes a parallel move of one yield; real curves twist, so use key-rate risk (curve risk note, planned).
- Callable and prepayable bonds have negative convexity; effective duration needs a model (callable and mortgage notes, planned).
- Hedging two bonds by DV01 is exact only for a parallel yield change.

### How it is implemented

- Inputs: cash-flow schedule from the conventions note, a yield or a curve, settlement date.
- Output: clean and dirty price, accrued, duration, convexity, DV01.
- Algorithm: sum over flows; yield from price by bisection or Newton, using DV01 as the derivative; $O(n)$ per evaluation.
- Pitfalls: yield solver bracket must include negative yields; duration for a curve-priced bond is a bump-and-revalue number, not a formula; date arithmetic must match the day-count convention.
- Reference: [`code/bond_pricing.py`](code/bond_pricing.py).
- System context: risk and PnL controls in the [front-to-back architecture](../18-Pricing-and-Risk-Systems/01-Front-to-Back-Architecture.md).

## Worked examples

Examples 1 to 3 are checked by `code/bond_pricing.py`, run in this session; Example 4 is the arithmetic shown.

### Example 1: 2-year 5% annual bond at a 4% yield

$P=5/1.04+105/1.04^2=101.886095$.
$D_{Mac}=(5/1.04+2\cdot105/1.04^2)/P=1.952813$ years, $D_{mod}=1.952813/1.04=1.877705$.
Convexity $=(5\cdot1\cdot2/1.04^3+105\cdot2\cdot3/1.04^4)/P=5.372829$.
DV01 $=101.886095\times1.877705\times10^{-4}=0.019131$ per 100 face.
For $+100$ bp the full repricing gives $100-101.886095=-1.886095$; the duration-convexity estimate is $-1.885749$, error $0.00035$ (third-order).

### Example 2: par 10-year 4% annual bond

At $y=4\%$ price is exactly 100.
$D_{mod}=8.1109$, $D_{Mac}=8.4353$, convexity $=80.754$, DV01 $=0.081109$.
Reprice: at 5% the price is 92.2783 ($-7.7217$); at 3% it is 108.5302 ($+8.5302$).
Duration-convexity predicts $-7.707$ and $+8.515$; the asymmetry is convexity: the gain from a fall (8.53) exceeds the loss from a rise (7.72).

### Example 3: convexity versus a zero

A 10-year zero at 4% has price 67.5564, $D_{Mac}=10$ exactly and convexity 101.70, against 8.4353 and 80.75 for the 10-year 4% coupon bond.
The zero has both higher duration and higher convexity because all of its value sits at the far end; a barbell of short and long zeros carries more convexity than a bullet of the same duration.

### Example 4: accrued interest

A 5% semiannual bond with the last coupon 60 days ago on a 180-day 30/360 period has accrued $=2.5\times60/180=0.8333$ per 100.
A clean price of 99.50 settles at a dirty price of 100.3333.

### Example 5: real-world case, March 2020 Treasury market stress

In March 2020 Treasury yields moved sharply and market liquidity deteriorated, with the Federal Reserve starting large Treasury purchases (source: Federal Reserve FOMC statement of 15 March 2020 and the Fed's March 2020 market functioning reports; not re-fetched this session, verify before citing).
Lesson for risk: duration-based hedges assume liquid, continuous trading; during stress the bid-ask on off-the-run bonds widened and DV01-neutral books carried basis risk between on-the-run and off-the-run issues.

## Pitfalls

- Using Macaulay duration as the price sensitivity: divide by $(1+y/m)$ first.
- Comparing durations of bonds quoted with different compounding.
- Hedging a long bond with a short one by DV01 and ignoring the curve slope between them.
- Quoting duration for a callable bond without an option-adjusted model.
- Using clean prices in P&L without carrying the accrued: P&L jumps at coupon dates.
- Computing convexity per unit of $y^2$ in one system and per unit of bp$^2$ in another.

## Interview questions

> [!question]- fi-modified-duration-def | Define modified duration and relate it to Macaulay duration.
> $D_{mod}=-\frac1P\frac{dP}{dy}=D_{Mac}/(1+y/m)$.
> It is the percentage price change for a unit change in the periodically compounded yield.

> [!question]- fi-zero-duration | What is the Macaulay duration of a zero-coupon bond?
> Its maturity, since the whole PV sits at time $T$ and the PV-weighted average time is $T$.

> [!question]- fi-dv01-formula | A bond has price 101.886 and modified duration 1.8777. What is its DV01 per 100 face?
> $0.019131$, from $P\cdot D_{mod}\times10^{-4}=101.886\times1.8777\times10^{-4}$.

> [!question]- fi-duration-convexity-approx | Write the second-order price approximation and compute it for a 10y 4% par bond at +100bp ($D_{mod}=8.1109$, $C=80.754$).
> $\Delta P/P\approx-D_{mod}\Delta y+\frac12C\Delta y^2=-0.081109+0.004038=-7.707\%$.
> The exact repricing is $-7.7217\%$.

> [!question]- fi-convexity-positive | Why is convexity positive for a plain bullet bond and who pays for it?
> $d^2P/dy^2=\sum c_it_i(t_i+1/m)(1+y/m)^{-mt_i-2}>0$.
> Buyers pay for it through a lower yield; it benefits a long position in both rate directions.

> [!question]- fi-barbell-bullet | A barbell and a bullet have the same duration. Which has higher convexity and what does the trade bet on?
> The barbell, since convexity grows faster than linearly in maturity.
> The barbell-minus-bullet trade is long convexity: it wins on large parallel moves and loses carry in quiet markets.

> [!question]- fi-clean-dirty | Define clean price, dirty price and accrued interest. A 5% semiannual bond is 60 days into a 180-day 30/360 period; clean 99.50. Dirty?
> Dirty is clean plus accrued; accrued $=2.5\times60/180=0.8333$, so dirty $=100.3333$.
> Settlement cash is the dirty price.

> [!question]- fi-duration-hedge | How do you hedge a 10y bond with a 2y bond by DV01 and what risk remains?
> Hedge ratio $=DV01_{10}/DV01_{2}$ of the 2y per unit of the 10y.
> It is neutral only to a parallel yield shift; slope changes and curve twists remain.

> [!question]- fi-duration-limits | Name three situations where duration misprices the price move.
> Large yield changes (convexity), non-parallel curve moves, and instruments with embedded options (callables, mortgages) where cash flows depend on yield.

> [!question]- fi-par-bond-price | What is the price of a bond whose coupon equals its yield on a coupon date?
> Par: 100 per 100 face, since the coupons discount at the same rate as their yield.

> [!question]- fi-ytm-solve | How do you solve for yield from price and what bracket do you need?
> Root finding on a strictly decreasing function: bisection or Newton with DV01 as slope.
> Allow negative yields in the bracket.

> [!question]- fi-coupon-duration-effect | Why does a higher coupon reduce duration at the same maturity and yield?
> More PV weight sits at early dates, shifting the weighted average time of cash flows earlier.

## Further reading

- Tuckman and Serrat, *Fixed Income Securities*, chapters 3 to 5.
- Fabozzi, *The Handbook of Fixed Income Securities*.
- U.S. Treasury and TMPG documentation on market conventions.

## In this repo and SDE-Interview-Prep

- Code: [`code/bond_pricing.py`](code/bond_pricing.py).
- Related: [Discounting and Yield Curves](01-Discounting-and-Yield-Curves.md), [Day Counts, Calendars and Schedules](11-Day-Counts-Calendars-and-Schedules.md).
