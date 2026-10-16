---
type: concept
track: [quant-trader, quant-research, quant-dev, quant-risk]
tier: advanced
status: draft
prereqs: [bonds-duration-and-convexity]
est_hours: 5
sources: [Tuckman and Serrat - Fixed Income Securities 4th ed. chapter 7, Brigo and Mercurio - Interest Rate Models chapters 1 and 2, Ametrano and Bianchetti - Everything you always wanted to know about multiple interest rate curve bootstrapping, ISDA Interest Rate Derivatives Definitions]
---

# Swaps and Curve Building

> [!info] Draft
> Written in this session with computed examples matching `code/curve_bootstrap.py`.
> Missing for `solid`: formal independent reviewer check of all equations and parameter citations.

## TL;DR

- A vanilla interest rate swap exchanges fixed coupon payments for floating reference rate fixings on a specified notional without exchanging principal.
- The par swap rate $S$ equates the present value of the fixed leg to the present value of the floating leg: $S = \frac{P(0, T_0) - P(0, T_n)}{\sum_{i=1}^n \tau_i P(0, T_i)}$.
- The swap annuity $A = \sum_{i=1}^n \tau_i P(0, T_i)$ is the swap's value sensitivity per unit notional to a unit change in the par rate; $A \times 10^{-4}$ is the per-basis-point figure (PV01).
- In a single-curve setting, the floating leg telescopes to $P(0, T_0) - P(0, T_n)$, which equals par minus the terminal zero-coupon bond.
- Yield curve bootstrapping inverts market par swap quotes into zero-coupon discount factors sequentially from short to long maturities.

## Learning objectives

- Value a fixed-for-floating interest rate swap from discount factors and compute its mark-to-market.
- Derive the par swap rate formula and explain why the floating leg cash flows telescope in single-curve pricing.
- Calculate swap DV01 and explain how dealers manage directional swap risk using the annuity.
- Execute a sequential bootstrap to extract zero rates and discount factors from market swap rates.
- Identify production pricing breaks arising from day-count differences between fixed and floating legs.

## Core concepts

### Anatomy of an interest rate swap

A fixed-for-floating interest rate swap is an agreement between two counterparties to exchange interest payments on a fixed notional $N$ over $n$ periods.
The payer of the fixed rate (payer swap) pays a predetermined fixed coupon $K$ and receives floating reference fixings.
The receiver of the fixed rate (receiver swap) receives the fixed rate $K$ and pays floating.
Payment frequencies frequently differ between legs: a standard USD swap historically had semiannual fixed payments on 30/360 and quarterly floating fixings on ACT/360.
Principal is never exchanged at inception or maturity, making the swap an off-balance-sheet synthetic commitment.

### Single-curve swap valuation and the telescoping float leg

Let $P(0, T)$ denote the discount factor to maturity $T$.
The present value of the fixed leg paying coupon $K$ at times $T_1, \dots, T_n$ with accrual fractions $\tau_i$ is
$$PV_{\text{fixed}} = N \sum_{i=1}^n \tau_i P(0, T_i) K = N \cdot K \cdot A(0, T_n),$$
where $A(0, T_n) = \sum_{i=1}^n \tau_i P(0, T_i)$ is the swap annuity (PV01 per unit notional is $A \times 10^{-4}$).
On the floating leg, the forward rate covering $[T_{i-1}, T_i]$ in a single-curve model is $F(0; T_{i-1}, T_i) = \frac{1}{\tau_i} \left( \frac{P(0, T_{i-1})}{P(0, T_i)} - 1 \right)$.
The present value of each floating payment is $\tau_i P(0, T_i) F(0; T_{i-1}, T_i) = P(0, T_{i-1}) - P(0, T_i)$.
Summing across all $n$ periods yields a telescoping series:
$$PV_{\text{float}} = N \sum_{i=1}^n [P(0, T_{i-1}) - P(0, T_i)] = N [P(0, T_0) - P(0, T_n)].$$
For a spot-starting swap where $T_0 = 0$, $P(0, 0) = 1.0$, reducing the floating leg value to $N [1 - P(0, T_n)]$.
Economically, receiving floating is equivalent to holding a floating-rate note that resets to par at each coupon date, financed by borrowing par.

### The par swap rate

The par swap rate $S(T_n)$ is the fixed coupon $K$ that sets the initial net present value of the swap to zero ($PV_{\text{fixed}} = PV_{\text{float}}$):
$$S(T_n) = \frac{P(0, T_0) - P(0, T_n)}{\sum_{i=1}^n \tau_i P(0, T_i)} = \frac{P(0, T_0) - P(0, T_n)}{A(0, T_n)}.$$
Once market rates shift, an existing swap with fixed coupon $K$ has mark-to-market value
$$V_{\text{payer}} = PV_{\text{float}} - PV_{\text{fixed}} = N (S - K) A(0, T_n).$$
The value of a swap is therefore the spread between the current market par swap rate $S$ and the contract coupon $K$, scaled by the annuity.

### Swap DV01 and sensitivity

The dollar value of a basis point (DV01) measures the change in swap present value for a 1 basis point (0.0001) shift in the par swap rate:
$$\text{DV01}_{\text{swap}} = \frac{\partial V}{\partial S} \times 10^{-4} = N \cdot A(0, T_n) \times 10^{-4}.$$
Because the annuity $A$ is the sum of discount factors weighted by accrual fractions, it increases with swap maturity but decreases as interest rates rise.
A trader hedging a 10-year swap position with a 2-year swap matches total DV01 by sizing notional in inverse proportion to their respective annuities: $N_2 = N_{10} \frac{A_{10}}{A_2}$.

### Curve bootstrapping from swaps

The par swap rate equation allows sequential extraction of zero-coupon discount factors.
Given par swap quotes $s_1, s_2, \dots, s_k$ at annual maturities $1, 2, \dots, k$:
For a 1-year swap with single payment: $s_1 P(0, 1) + P(0, 1) = 1 \implies P(0, 1) = \frac{1}{1 + s_1}$.
For an $m$-year swap, assuming discount factors $P(0, 1), \dots, P(0, m-1)$ are already determined:
$$s_m \sum_{i=1}^{m-1} P(0, i) + (1 + s_m) P(0, m) = 1 \implies P(0, m) = \frac{1 - s_m \sum_{i=1}^{m-1} P(0, i)}{1 + s_m}.$$
This recursive algorithm is triangular and solves in $O(m)$ operations without iterative optimization.

### How it is implemented

- Inputs: swap term sheet (notional, fixed rate, start date, tenor, payment frequencies, day count conventions, calendars), zero or discount curve.
- Outputs: clean mark-to-market, fixed leg PV, floating leg PV, annuity, swap DV01, par swap rate.
- Algorithm: generate cash flow schedule for both legs, lookup discount factors for payment dates, project forward rates on floating dates, multiply and sum.
- Complexity: $O(n)$ where $n$ is the number of payment periods in the swap.
- Reference implementation: [`code/curve_bootstrap.py`](code/curve_bootstrap.py) provides `par_swap_rate_single_curve`, `swap_annuity`, and `bootstrap_single_curve`.
- System context: [the curve and surface service](../18-Pricing-and-Risk-Systems/04-Curve-and-Surface-Service.md).

## Worked examples

All calculations below match the verified assertions in `code/curve_bootstrap.py`.

### Example 1: single-curve bootstrap from three annual swaps

Market quotes for annual-pay par interest rate swaps:
$s_1 = 3.00\%$, $s_2 = 3.50\%$, $s_3 = 4.00\%$.

Pillar 1:
$$P(0, 1) = \frac{1}{1 + 0.030} = 0.970874.$$
Continuous zero rate: $z(1) = -\ln(0.970874) / 1 = 2.9559\%$.

Pillar 2:
$$P(0, 2) = \frac{1 - 0.035 \times 0.970874}{1 + 0.035} = \frac{1 - 0.033981}{1.035} = \frac{0.966019}{1.035} = 0.933352.$$
Continuous zero rate: $z(2) = -\ln(0.933352) / 2 = 3.4486\%$.
Annual compounding zero rate: $0.933352^{-1/2} - 1 = 3.5088\%$.

Pillar 3:
Sum of prior discount factors: $P(0, 1) + P(0, 2) = 0.970874 + 0.933352 = 1.904226$.
$$P(0, 3) = \frac{1 - 0.040 \times 1.904226}{1 + 0.040} = \frac{1 - 0.076169}{1.040} = \frac{0.923831}{1.040} = 0.888299.$$
Continuous zero rate: $z(3) = -\ln(0.888299) / 3 = 3.9482\%$.

Check par rate reconstruction for 3-year swap:
Annuity $A(0, 3) = 0.970874 + 0.933352 + 0.888299 = 2.792525$.
Par rate $S_3 = (1 - 0.888299) / 2.792525 = 0.111701 / 2.792525 = 4.0000\%$.

### Example 2: mark-to-market and DV01 of an off-market swap

Consider an existing 3-year payer swap with notional $N = 100{,}000{,}000$ and fixed coupon $K = 3.50\%$.
Current market par rate for 3-year maturity has risen to $S = 4.00\%$.
Annuity $A(0, 3) = 2.792525$.
Mark-to-market value to the payer:
$$V_{\text{payer}} = N \cdot (S - K) \cdot A(0, 3) = 100{,}000{,}000 \cdot (0.040 - 0.035) \cdot 2.792525 = 1{,}396{,}262.50.$$
DV01 of the swap:
$$\text{DV01} = N \cdot A(0, 3) \times 10^{-4} = 100{,}000{,}000 \cdot 2.792525 \times 10^{-4} = 27{,}925.25.$$
If market par rates rise by 1 bp to 4.01%, the new MTM is $100{,}000{,}000 \cdot (0.0401 - 0.035) \cdot 2.792525 = 1{,}424{,}187.75$, a gain of exactly $27{,}925.25$.

### Example 3: DV01 hedge between 3-year and 1-year swap

A desk is long $100{,}000{,}000$ of a 3-year receiver swap ($K = 4.00\%$).
The desk is exposed to rising rates and wants to hedge directional curve risk using 1-year swaps.
Annuity of 3-year swap: $A_3 = 2.792525 \implies \text{DV01}_3 = 27{,}925.25$.
Annuity of 1-year swap: $A_1 = P(0, 1) = 0.970874 \implies \text{DV01}_1 = 9{,}708.74$ per $100{,}000{,}000$ notional.
Hedge ratio:
$$N_1 = N_3 \cdot \frac{A_3}{A_1} = 100{,}000{,}000 \cdot \frac{2.792525}{0.970874} = 287{,}630{,}063.$$
The trader pays fixed on $287.63$ million of 1-year swaps to neutralize parallel curve exposure.
Residual curve risk remains: if the curve steepens (1-year rate falls while 3-year rate rises), the position suffers losses on both legs.

### Example 4: real-world case, the 2008 Lehman collapse and single-curve breakdown

Prior to August 2007, the spread between 3-month USD LIBOR and the overnight Fed Funds OIS rate was small and stable.
Single-curve swap models treated the Libor forwarding rate and the discounting rate as identical.
During the global financial crisis of 2008 and following Lehman Brothers' default in September 2008, the 3-month Libor-OIS spread blew out to about 365 basis points on 10 October 2008 (source: Sengupta and Tam, "The LIBOR-OIS Spread as a Summary Indicator", Federal Reserve Bank of St. Louis Economic Synopses, 2008).
Because swap collateral posted under standard Credit Support Annexes earned the overnight rate, discounting future swap cash flows at Libor significantly mispriced counterparty and replacement costs.
The crisis forced the global derivatives industry to abandon single-curve pricing and adopt the multi-curve framework.

## Pitfalls

- Assuming floating leg cash flows telescope in modern multi-curve markets: telescoping occurs only when forwarding and discounting curves are identical.
- Overlooking payment frequency mismatches between legs: an annual fixed leg versus quarterly floating leg requires separate schedule generators.
- Using clean par rates without adjusting for differing day-count conventions on the fixed leg (30/360) and floating leg (ACT/360).
- Confusing payer and receiver conventions: a payer swap is short duration (benefits when rates rise): $\frac{\partial V}{\partial y} > 0$, so its dollar duration and DV01 have the opposite sign to a long bond's.
- Extrapolating the curve beyond the longest liquid swap pillar with flat zero rates instead of flat forward rates.

## Interview questions

> [!question]- fi-swap-par-rate-derivation | Derive the formula for the par swap rate $S$ of a spot-starting vanilla fixed-for-floating swap in a single-curve setting.
> Set $PV_{\text{fixed}} = PV_{\text{float}}$.
> $PV_{\text{fixed}} = S \sum_{i=1}^n \tau_i P(0, T_i)$ and $PV_{\text{float}} = \sum_{i=1}^n [P(0, T_{i-1}) - P(0, T_i)] = 1 - P(0, T_n)$.
> Solving for $S$ yields $S = \frac{1 - P(0, T_n)}{\sum_{i=1}^n \tau_i P(0, T_i)}$.

> [!question]- fi-floating-leg-par | Why is the floating leg of an interest rate swap worth par at every coupon reset date under single-curve pricing?
> A floating leg pays forward interest that exactly compensates for the time value of money over the coupon period.
> Holding a floating leg is economically equivalent to buying a floating-rate note for 100, receiving coupon interest, and having principal returned at maturity.

> [!question]- fi-swap-annuity-def | Define the swap annuity and explain its relationship to swap DV01.
> The annuity $A(0, T_n) = \sum_{i=1}^n \tau_i P(0, T_i)$ represents the present value of receiving 1 basis currency unit per period.
> Swap DV01 is the dollar value change for a 1 basis point shift in par swap rate: $\text{DV01} = N \cdot A(0, T_n) \times 10^{-4}$.

> [!question]- fi-swap-payer-vs-receiver | Does a payer swap gain or lose value when interest rates rise? Explain why.
> A payer swap gains value when interest rates rise.
> The payer pays a fixed coupon $K$ and receives floating; as rates rise, floating cash receipts increase while fixed obligations remain unchanged.

> [!question]- fi-bootstrap-p3-calc | Given $P(0, 1) = 0.970874$, $P(0, 2) = 0.933352$, and 3-year par swap rate $s_3 = 4.00\%$, compute $P(0, 3)$.
> $P(0, 3) = \frac{1 - s_3 [P(0, 1) + P(0, 2)]}{1 + s_3} = \frac{1 - 0.040 \cdot 1.904226}{1.040} = \frac{0.923831}{1.040} = 0.888299$.

> [!question]- fi-swap-mtm-formula | An investor is long a $100\text{M}$ payer swap at fixed rate $3.50\%$. The current 3-year par swap rate is $4.00\%$ and the annuity is $2.7925$. What is its mark-to-market?
> $V_{\text{payer}} = N \cdot (S - K) \cdot A = 100{,}000{,}000 \cdot (0.040 - 0.035) \cdot 2.7925 = 1{,}396{,}250$.

> [!question]- fi-swap-dv01-hedge-ratio | How do you hedge a 10-year swap with DV01 of $85{,}000$ using a 2-year swap with DV01 of $19{,}000$?
> Notional ratio equals $\frac{\text{DV01}_{10}}{\text{DV01}_2} = \frac{85{,}000}{19{,}000} \approx 4.474$.
> Execute 4.474 times the notional in the 2-year swap with the opposite direction.

> [!question]- fi-single-curve-breakdown | Why did single-curve swap pricing break down during the 2008 financial crisis?
> Credit and liquidity risk drove the 3-month Libor-OIS spread from a small, stable level to about 365 bps in October 2008.
> Swap collateral posted under CSAs earned the overnight rate, requiring overnight OIS discounting while floating cash flows reflected Libor risk.

> [!question]- fi-bootstrap-triangular | Why is standard swap bootstrapping triangular rather than requiring an iterative multi-dimensional solver?
> Each $m$-year swap instrument introduces only one new unknown discount factor $P(0, m)$ while all earlier discount factors $P(0, 1), \dots, P(0, m-1)$ were solved at earlier maturities.

> [!question]- fi-swap-daycount-friction | How does day count convention mismatch between fixed leg (30/360) and floating leg (ACT/360) affect par rate quoting?
> $1$ year on 30/360 is $\frac{360}{360} = 1.0$, whereas on ACT/360 it is $\frac{365}{360} \approx 1.0139$.
> Ignoring the mismatch misstates a year's accrual by $\frac{365}{360} - 1 = 1.39\%$, which on a $4\%$ coupon is $0.04 \times \frac{5}{360} = 5.56$ bps of running rate.

## Further reading

- Tuckman and Serrat, *Fixed Income Securities: Tools for Today's Markets*, chapter 7.
- Brigo and Mercurio, *Interest Rate Models - Theory and Practice*, chapter 1.
- Ametrano and Bianchetti, *Everything You Always Wanted to Know About Multiple Interest Rate Curve Bootstrapping but Were Afraid to Ask*.
- ISDA 2006 / 2021 Interest Rate Derivatives Definitions.

## In this repo and SDE-Interview-Prep

- Code: [`code/curve_bootstrap.py`](code/curve_bootstrap.py) (`bootstrap_single_curve`, `par_swap_rate_single_curve`, `swap_annuity`).
- Related notes: [Discounting and Yield Curves](01-Discounting-and-Yield-Curves.md), [Bonds, Duration and Convexity](02-Bonds-Duration-and-Convexity.md), [Multi-Curve and CSA Discounting](13-Multi-Curve-and-CSA-Discounting.md).
