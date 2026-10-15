---
type: concept
track: [quant-trader, quant-research]
tier: core
status: draft
prereqs: []
est_hours: 4
sources: [Tuckman and Serrat - Fixed Income Securities 4th ed. chapters 1 to 3, Brigo and Mercurio - Interest Rate Models chapter 1, ECB monetary policy decisions at ecb.europa.eu]
---

# Discounting and Yield Curves

> [!info] Draft
> Written and computed in this session; the independent review required for `solid` has not happened.
> Missing for `solid`: reviewer re-derivation, the ECB negative-rate case was not re-fetched this session.

## TL;DR

- A discount factor $P(0,T)$ is today's price of one unit paid at $T$; every other curve quantity is a transformation of it.
- Zero rate, forward rate and par yield are three views of the same curve: $P(0,T)=e^{-z(T)T}=\exp\!\big(-\int_0^T f(0,u)\,du\big)$.
- The forward rate between $T_1$ and $T_2$ is fixed by no-arbitrage: $1+F\,\tau = P(0,T_1)/P(0,T_2)$.
- A coupon bond is a portfolio of zero-coupon bonds; its price is the sum of cash flows times discount factors.
- Always state compounding and day count with any quoted rate; a rate without them is not a number.

## Learning objectives

- Convert between discount factors, zero rates (any compounding), forward rates and par yields.
- Derive forward rates from discount factors by no-arbitrage and explain why they are not forecasts.
- Price a fixed-rate bond off a zero curve and bootstrap a zero curve from par yields.
- Name the production failure modes: compounding mismatch, day-count mismatch, extrapolation.

## Core concepts

### Discount factors and the no-arbitrage curve

Let $P(0,T)$ be the price today of a zero-coupon bond paying 1 at $T$.
Absence of arbitrage means any cash-flow stream is worth $\sum_i c_i P(0,T_i)$: replicate each payment with a zero.
If two streams have identical cash flows they must have identical prices, so the curve $T\mapsto P(0,T)$ is the only state needed to value any deterministic stream.

### Rates are quoting conventions on $P$

| Quote | Definition | Link to $P(0,T)$ |
| :--- | :--- | :--- |
| Annual compounding | $z_a(T)$ | $P=(1+z_a)^{-T}$ |
| $m$ times a year | $z_m(T)$ | $P=(1+z_m/m)^{-mT}$ |
| Continuous | $z_c(T)$ | $P=e^{-z_c T}$ |
| Simple (money market) | $L(T)$ with accrual $\tau$ | $P=1/(1+L\tau)$ |

Conversion between compounding bases: $z_c=m\ln(1+z_m/m)$.
Example: $3\%$ annual is $\ln 1.03=2.9559\%$ continuous.

### Forward rates

Buy one zero maturing at $T_2$ and sell $P(0,T_2)/P(0,T_1)$ units of a zero maturing at $T_1$: the net cost today is zero, and the position pays $-P(0,T_2)/P(0,T_1)$ at $T_1$ and receives 1 at $T_2$, which is a locked-in loan over $[T_1,T_2]$.
No arbitrage forces the simply compounded forward over $[T_1,T_2]$ with accrual $\tau=T_2-T_1$ to be
$$F(0;T_1,T_2)=\frac{1}{\tau}\left(\frac{P(0,T_1)}{P(0,T_2)}-1\right).$$
The instantaneous forward is $f(0,T)=-\partial_T\ln P(0,T)$, hence $P(0,T)=\exp(-\int_0^T f(0,u)du)$ and $z_c(T)=\frac1T\int_0^T f$.
A zero curve that is rising has forwards above zeros; the zero rate is an average of forwards.
Forwards are the break-even rates for locking in today, not predictions: under the $T$-forward measure they are expectations of future rates, under the real-world measure they embed term premia.

### Par yield and bond pricing

For a bond with annual coupon $c$ and maturity $n$, price on a curve is $\sum_{i=1}^{n} c\,P(0,i)+P(0,n)$ per unit face.
The par coupon makes the price equal to 1: $c_n=\dfrac{1-P(0,n)}{\sum_{i=1}^n P(0,i)}$.
The yield to maturity $y$ is the single rate that discounts all flows to the market price; it is a summary statistic, not a curve, and two bonds with the same maturity and different coupons have different yields.

### Bootstrapping, first pass

Given par yields $c_1,c_2,\dots$ solve sequentially: $P(0,1)=1/(1+c_1)$, then $P(0,n)=\dfrac{1-c_n\sum_{i=1}^{n-1}P(0,i)}{1+c_n}$.
Each step uses only shorter-maturity discount factors, so the system is triangular.
Real curve construction (instrument choice, interpolation, multi-curve) is in later notes.

### How it is implemented

- Inputs: market quotes with their conventions, a valuation date, a calendar.
- Output: an object answering $P(0,T)$ for any $T$, with $z$, $F$ and par yield derived from it, never stored independently.
- Storage: store discount factors or log-discount factors at pillar dates; interpolate log-linearly in $P$ (flat forwards) as a baseline.
- Complexity: bootstrap is $O(n)$ per instrument with a closed form, $O(n\cdot\text{iter})$ with a root solver; evaluation is $O(\log n)$ by binary search over pillars.
- Numerical pitfalls: extrapolation beyond the last pillar, negative discount-factor ratios from bad interpolation, mixing year fractions from different conventions.
- System design: the curve and surface service (planned section).

## Worked examples

Numbers below come from `code/bond_pricing.py` or the arithmetic shown, and were run in this session.

### Example 1: zero curve to discount factors and forwards

Annual zero rates: $z(1)=3\%$, $z(2)=3.5\%$, $z(3)=4\%$.

$$P(0,1)=1.03^{-1}=0.970874,\quad P(0,2)=1.035^{-2}=0.933511,\quad P(0,3)=1.04^{-3}=0.888996.$$

Forwards: $F(1,2)=0.970874/0.933511-1=4.0024\%$, $F(2,3)=0.933511/0.888996-1=5.0073\%$.
The forwards sit above the zeros because the zero curve slopes up; check: $(1.03)(1.040024)(1.050073)=1.1249\approx1.04^3=1.1249$.

### Example 2: price a 3-year 4% annual bond on that curve

Price $=4(0.970874)+4(0.933511)+104(0.888996)=100.0732$.
The par coupon is $(1-0.888996)/(0.970874+0.933511+0.888996)=3.974\%$, slightly under 4%, which is why the 4% bond prices above par.

### Example 3: bootstrap from par yields

Par yields $c_1=3\%$, $c_2=3.5\%$.
$P(0,1)=1/1.03=0.970874$.
$P(0,2)=(1-0.035\times0.970874)/1.035=0.933352$, so the 2-year zero rate is $0.933352^{-1/2}-1=3.5088\%$.
Par rate $3.5\%$ is below the zero rate $3.5088\%$: coupon bonds pay early flows at lower zero rates.

### Example 4: real-world case, negative rates

Sovereign and money-market rates went below zero in the euro area from 2014 when the ECB's deposit facility rate became negative (source: ECB monetary policy decisions, ecb.europa.eu; not re-fetched this session, verify the dates).
Consequences for systems: a discount factor above 1 is legal, log-linear interpolation still works because $P>0$, but any model assuming positive rates (lognormal, CIR) and any code that floors rates at zero breaks.
That is why the industry moved toward shifted-lognormal and normal volatility conventions (see the rates volatility note, planned).

## Pitfalls

- Quoting or comparing rates without compounding and day count; $3\%$ annual and $3\%$ continuous differ by 4.4 bp at one year.
- Treating yield to maturity as the curve: it ignores the shape and reinvestment structure.
- Extrapolating the last zero rate flat instead of flat forward, which changes long-dated PVs.
- Interpolating zero rates linearly and getting discontinuous or negative forwards.
- Pricing a 4% bond at a "4% yield" and calling it a curve-consistent price: curve-consistent pricing uses the zero curve.
- Double counting accrual: dirty price versus clean price.

## Interview questions

> [!question]- fi-discount-factor-definition | What is a discount factor and why can any deterministic cash-flow stream be priced from the discount curve alone?
> $P(0,T)$ is today's price of 1 paid at $T$.
> Any stream is a portfolio of zero-coupon bonds, so no arbitrage forces its price to be $\sum c_iP(0,T_i)$.

> [!question]- fi-compounding-conversion | Convert a 3% annually compounded zero rate to continuous compounding.
> $z_c=\ln(1.03)=2.9559\%$.
> Equating discount factors: $(1.03)^{-T}=e^{-z_cT}$.

> [!question]- fi-forward-from-discount | Given $P(0,1)=0.970874$ and $P(0,2)=0.933511$, what is the 1y1y forward rate (annual compounding)?
> $F=P(0,1)/P(0,2)-1=4.0024\%$.
> Lock it in by buying the 2y zero and selling $0.933511/0.970874$ of the 1y zero.

> [!question]- fi-forward-not-forecast | Are forward rates forecasts of future spot rates?
> No.
> They are the no-arbitrage break-even rates for locking in a future period today; realised spots differ by term premia and by news, and forwards are expectations only under the corresponding forward measure.

> [!question]- fi-zero-forward-relation | Express the zero rate as an average of forwards and say what an upward sloping zero curve implies for forwards.
> $z_c(T)=\frac1T\int_0^T f(0,u)du$.
> If $z_c$ is rising, forwards lie above zeros, because the average is dragged up by higher late forwards.

> [!question]- fi-par-coupon-formula | Derive the par coupon for an $n$-year annual bond from discount factors.
> Set price to 1: $c\sum_{i=1}^nP(0,i)+P(0,n)=1$, so $c=(1-P(0,n))/\sum_{i=1}^nP(0,i)$.

> [!question]- fi-bootstrap-par-yields | Bootstrap the 2-year discount factor from annual par yields 3% (1y) and 3.5% (2y).
> $P(0,1)=1/1.03=0.970874$.
> $P(0,2)=(1-0.035\cdot0.970874)/1.035=0.933352$, a 2y zero rate of 3.5088%.

> [!question]- fi-ytm-vs-curve | Why is yield to maturity not a curve and when does it mislead?
> It is one rate that reprices a single bond, so it hides the shape of the curve.
> Two bonds with the same maturity and different coupons have different yields, and comparing yields across different durations or coupons misleads relative value.

> [!question]- fi-log-linear-interp | What does log-linear interpolation of discount factors imply for forwards?
> Piecewise-constant instantaneous forwards, since $\ln P$ linear in $T$ means $f=-\partial_T\ln P$ is constant on each interval.
> Forwards jump at pillars, which causes jagged hedge ratios.

> [!question]- fi-negative-rates-impact | What breaks in a pricing library when rates go negative?
> Lognormal rate models and Black formulas (undefined for negative forwards), CIR, and any code flooring rates at zero.
> Discount factors above 1 are fine mathematically; the fix is normal or shifted-lognormal volatility conventions.

> [!question]- fi-par-vs-zero | A 2y par rate is 3.5% and the 2y zero is 3.5088%. Why is the par rate lower?
> The coupon bond pays an early flow discounted at the lower 1y zero rate, so its blended yield is below the 2y zero rate on an upward sloping curve.

## Further reading

- Tuckman and Serrat, *Fixed Income Securities: Tools for Today's Markets*, chapters 1 to 3.
- Brigo and Mercurio, *Interest Rate Models - Theory and Practice*, chapter 1.
- Hull, *Options, Futures, and Other Derivatives*, chapter on interest rates.

## In this repo and SDE-Interview-Prep

- Code: [`code/bond_pricing.py`](code/bond_pricing.py) (price, duration, convexity, DV01).
- Next: [Bonds, Duration and Convexity](02-Bonds-Duration-and-Convexity.md), [Day Counts, Calendars and Schedules](11-Day-Counts-Calendars-and-Schedules.md).
