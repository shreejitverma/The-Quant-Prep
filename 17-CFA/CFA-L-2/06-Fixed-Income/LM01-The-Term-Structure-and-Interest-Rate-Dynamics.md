---
type: cfa-lm
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
volume: 6
lm: 1
title: "The Term Structure and Interest Rate Dynamics"
pages: "3-67"
weight_band: "10-15%"
difficulty: 3
los_count: 11
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/fixed-income]
---

# LM1: The Term Structure and Interest Rate Dynamics

Difficulty 3 of 5: the math is one identity (the forward rate model) applied many times, but the exam wraps it in notation traps (f with two subscripts), asks for prices as well as rates, and mixes in a large qualitative block on spreads, term structure theories, factor models and macro views that must be recalled precisely.

## LOS map

- **describe** relationships among spot rates, forward rates, yield to maturity, expected and realized returns on bonds, and the shape of the yield curve (V6 p.3) ^los-06-01-a
    - Examiner asks: given two spot rates, compute the implied forward rate or forward price, state whether the forward curve lies above or below an upward-sloping spot curve, and explain why YTM is a weighted average of spot rates that equals expected return only under restrictive assumptions.
- **describe** how zero-coupon rates (spot rates) may be obtained from the par curve by bootstrapping (V6 p.3) ^los-06-01-b
    - Examiner asks: bootstrap z2 or z3 from a table of par rates by forward substitution, or spot the error in a description of bootstrapping (backward substitution and latest-to-earliest ordering are both wrong).
- **describe** the assumptions concerning the evolution of spot rates in relation to forward rates implicit in active bond portfolio management (V6 p.3) ^los-06-01-c
    - Examiner asks: an investor projects future spot rates above or below today's forward curve; decide whether the bond is overvalued, fairly valued or undervalued, and what return the trade earns if the projection is right.
- **describe** the strategy of rolling down the yield curve (V6 p.3) ^los-06-01-d
    - Examiner asks: which curve shape and which rate expectation justify buying a bond longer than the horizon, and compute the horizon return of the rolldown versus the maturity-matched bond under a static curve.
- **explain** the swap rate curve and why and how market participants use it in valuation (V6 p.3) ^los-06-01-e
    - Examiner asks: why the swap curve is the preferred benchmark where government markets are illiquid or the private sector dominates, and how swap rates, spot rates and discount factors convert into one another through the par swap equation.
- **calculate** and interpret the swap spread for a given maturity (V6 p.3) ^los-06-01-f
    - Examiner asks: swap rate minus the on-the-run government yield of the same maturity, including the case where the government yield is negative, and build a bond yield as government yield plus swap spread.
- **describe** short-term interest rate spreads used to gauge economy-wide credit risk and liquidity risk (V6 p.3) ^los-06-01-g
    - Examiner asks: define the TED spread and the MRR-OIS spread, state which direction each moves when T-bill rates fall or bank credit worsens, and pick the right spread for pricing a corporate bond (Z-spread) versus judging money market stress (MRR-OIS).
- **explain** traditional theories of the term structure of interest rates and describe the implications of each theory for forward rates and the shape of the yield curve (V6 p.3) ^los-06-01-h
    - Examiner asks: match a scenario (fallen angels, yield-induced maturity switching, risk-neutral investors, liquidity premiums) to unbiased expectations, local expectations, liquidity preference, segmented markets or preferred habitat, and state what each implies about forward rates as predictors.
- **explain** how a bond's exposure to each of the factors driving the yield curve can be measured and how these exposures can be used to manage yield curve risks (V6 p.3) ^los-06-01-i
    - Examiner asks: compute the portfolio value change from key rate durations or from level, steepness and curvature sensitivities, respecting the signs in the exhibit and the number of standard deviations.
- **explain** the maturity structure of yield volatilities and their effect on price volatility (V6 p.3) ^los-06-01-j
    - Examiner asks: short rates are more volatile than long rates, short volatility is driven by monetary policy while long volatility is driven by the real economy and inflation, and annualize a monthly standard deviation by dividing by the square root of the interval.
- **explain** how key economic factors are used to establish a view on benchmark rates, spreads, and yield curve changes (V6 p.3) ^los-06-01-k
    - Examiner asks: map rate hikes to bear flattening, rate cuts to bull steepening, flight to quality to bull flattening, falling deficits to lower yields, and choose the duration, steepener/flattener or bullet/barbell trade for a given view.

## Core intuition

Every default-free promise of one currency unit at a future date has a price today, the discount factor.
The full menu of those prices across maturities, the discount function, is the market's complete statement about the time value of money (V6 p.4).
Quoting the same information as annualized yields on zero-coupon bonds gives the spot curve, and nothing is lost in translation: discount function and spot curve identify each other exactly (V6 p.5).
The spot rate is the cleanest yield concept because a zero held to maturity has no coupons to reinvest, so the stated yield is the realized return (V6 p.5).

A forward rate is the answer to a different question: at what rate can I contract today for a loan that starts at time A and repays at time B?
No money changes hands at inception, so no-arbitrage forces the forward price of the deferred zero to be the ratio of two of today's discount factors, F = DF_B divided by DF_A (V6 p.5).
Everything else in this module is that one ratio, restated in rates: (1+z_B)^B = (1+z_A)^A (1+f_{A,B-A})^(B-A) (V6 p.7).
The long investment must end up in exactly the same place as the short investment rolled over at the pre-agreed forward rate.

> [!abstract] Idea 1: the spot curve is an average and the forward curve is the margin
> The T-period spot rate is the geometric mean of the first-period rate and the chain of one-period forward rates (V6 p.9).
> When an average is rising, the marginal data point sits above it; when it is falling, the margin sits below (V6 p.12).
> So an upward-sloping spot curve puts the forward curve above it, a downward-sloping spot curve puts the forward curve below it, and a flat curve makes every forward equal the spot rate (V6 p.10, p.12).
> The forward curve also gets steeper and further away the later the start date A, and it never extends beyond the longest maturity quoted today (V6 p.11, p.12).

A forward rate carries two equivalent interpretations that the exam tests verbatim (V6 p.8).
It is the breakeven reinvestment rate that makes an investor indifferent between buying the long zero and rolling the short zero, and it is the rate that can be locked in today by extending maturity.

![[Term-Structure-Shapes.excalidraw]]

The government par curve reports the coupon rates at which fresh bonds would price exactly at par (V6 p.12).
On-the-run issues are used because they are liquid and near par.
A coupon bond is a portfolio of zeros, so par yields can be unzipped into spot rates one maturity at a time, earliest to latest, by forward substitution: this is bootstrapping (V6 p.12, p.13).
The one-year par rate is already a spot rate; each later spot rate is whatever discount rate makes the par bond's final cash flow close the pricing identity given the spot rates already found (V6 p.13).

Yield to maturity compresses a whole spot curve into one number.
Because a bond has only one price, its YTM must be a cash-flow-weighted average of the spot rates that discount it, pulled toward the spot rate of the largest (final) cash flow (V6 p.14, p.15).
The YTM equals the expected return only under severe assumptions: held to maturity, no default, and every coupon reinvested at the original YTM (V6 p.15).
Volatile rates, a sloped curve, default risk or embedded options each break the equality (V6 p.15).
Even assuming forward rates are realized, the expected return of a coupon bond differs from its YTM; only a flat curve makes YTM a realistic expected return (V6 p.16).

> [!abstract] Idea 2: if spot rates evolve exactly as the forward curve implies, every default-free bond earns the one-period risk-free rate, so active management is a bet against the forward curve
> The forward contract price stays unchanged when future spot rates equal today's implied forwards, and every zero, whatever its maturity, returns the first-period spot rate over the first period (V6 p.17, p.18, p.19).
> Forward rates are the market's most accessible proxy for expected future spot rates, so the manager's edge is a projection that differs from them (V6 p.9, p.18).
> Expect future spots below the forwards and the bond is undervalued: the market is discounting harder than you believe it should, and you buy (V6 p.20).
> Expect future spots above the forwards and the bond is overvalued, and your realized return falls short of the one-period rate if you hold it (V6 p.20).

Riding (rolling down) the yield curve is the flagship application (V6 p.20, p.21).
With an upward-sloping curve that is expected to stay put, a bond bought with maturity beyond the horizon is revalued at ever lower yields as it ages, adding a capital gain to its higher coupon.
The trade beats maturity matching precisely because static rates are below the forward rates the market has priced in; it is a deliberate short position against the forward curve, and its cousin, the maturity spread carry trade (borrow short, lend long), carries the same exposure to an unexpected rise in rates (V6 p.21, p.22).

The swap curve is the second benchmark for the time value of money (V6 p.23).
The swap rate is the fixed rate that makes a fixed-for-floating swap worth zero at inception, so the swap curve is a par curve built from short-term bank lending rates (MRR) rather than sovereign rates (V6 p.23).
It matters because swaps are enormously liquid, need no underlying bond supply, offer more maturities, and are comparable across countries; wholesale banks that hedge with swaps value their balance sheets off it, and in countries with thin government markets or dominant private sectors it is the only credible benchmark (V6 p.24).
The swap spread, swap rate minus the same-maturity on-the-run government yield, prices the credit and liquidity premium of bank-quality risk over the sovereign and widens in recessions (V6 p.26, p.27).
The I-spread quotes a bond's YTM net of the interpolated swap rate; the Z-spread is the single constant spread added to every point of the benchmark spot curve that reprices the risky bond exactly (V6 p.27, p.28).
For economy-wide stress the market watches short rates: the TED spread (MRR minus the T-bill of the same maturity) and the MRR-OIS spread (MRR minus the overnight indexed swap rate) both widen when bank credit or liquidity deteriorates (V6 p.29, p.30).
SOFR, a volume-weighted index of Treasury repo transactions, is the secured overnight rate replacing survey-based Libor (V6 p.30).

The traditional theories answer why the curve has its shape (V6 p.30 to p.33).
Unbiased (pure) expectations makes forwards unbiased predictors of future spots, which requires risk neutrality; local expectations only requires every bond to earn the risk-free rate over the next instant, so it survives in a risky world, yet even it is refuted because short-horizon returns on long bonds exceed those on short bonds.
Liquidity preference adds a maturity-increasing premium, so forwards are upward-biased predictors and the curve is typically upward sloping even with flat rate expectations.
Segmented markets lets supply and demand within each maturity silo set yields independently, driven by asset/liability matching; preferred habitat keeps the preferences but lets big enough yield differentials pull investors out of their habitat, which is the theory that best fits reality and episodes like QE (V6 p.32, p.33).

> [!abstract] Idea 3: yield curve movements compress into level, steepness and curvature, and durations to those factors are the risk handles
> Litterman and Scheinkman found three independent movements explain historical curve changes: level (parallel shift, the dominant factor), steepness (short moves versus long), and curvature (the twist of the middle against the ends) (V6 p.37, p.38).
> Key rate durations measure price sensitivity to a change at one maturity segment; they sum to effective duration, and linear combinations of them give the level, steepness and curvature sensitivities, so either set manages shaping risk that effective duration alone cannot see (V6 p.39, p.40, p.41).

Interest rate volatility has its own term structure: short rates are more volatile than long rates, yet long bond prices swing more because duration amplifies their smaller yield moves (V6 p.39).
Short-end volatility traces to monetary policy uncertainty, long-end volatility to uncertainty about the real economy and inflation (V6 p.39).
The same split governs yield levels: monetary policy explains about two-thirds of short and intermediate yield variation, and inflation about two-thirds of long yield variation (V6 p.43).
The bond risk premium, the expected excess return of the long default-free bond over the short one, is forward looking and must be estimated (V6 p.43).
Policy tightening in expansions produces bear flattening; easing in recessions produces bull steepening; flight to quality produces bull flattening as long yields collapse (V6 p.43, p.44).
Bigger deficits, longer government debt maturity structures and weaker investor demand raise yields and the premium; QE-style asset purchases and strong pension or foreign demand compress it (V6 p.44).
The trades follow the view: extend duration if rates will fall, shorten if they will rise, duration-neutral steepeners and flatteners for slope views, and a shift from bullet to barbell to profit from an expected bull flattening (V6 p.45).

## Formulas and derivations

**Discount factor and spot rate** (V6 p.4)
$$
DF_N = \frac{1}{(1+z_N)^N}
$$
^f-06-01-1

- $DF_N$: price today of a default-risk-free unit payment in $N$ periods (a pure number below 1 for positive rates); $z_N$: annualized $N$-period spot (zero-coupon) rate.
- The set $\{DF_N\}$ is the discount function and $\{z_N\}$ is the spot curve; each fully determines the other (V6 p.5).
- Holds by definition: a zero pays one unit at $N$, so its price is that unit discounted at its own yield, with no reinvestment assumption needed.

> [!tip] Calculator
> $z$ from $DF$: `1 ÷ DF =` then `y^x` with exponent `1/N`, then `- 1 =`. Example for N = 4: `1 ÷ 0.7350 = y^x 0.25 = - 1 =` gives 0.0800 (V6 p.26).

**Forward pricing model** (V6 p.5)
$$
DF_B = DF_A \times F_{A,B-A}
$$
^f-06-01-2

- $F_{A,B-A}$: price agreed today, paid at time $A$, for a zero maturing at $B$ (tenor $B-A$); $DF_A$, $DF_B$: today's discount factors.
- Derivation: buying the $B$-period zero today and buying the forward on the $(B-A)$-period zero both deliver one unit at $B$; identical payoffs must cost the same today, so $DF_B$ must equal the cost of setting aside $DF_A \times F$ today to fund the forward payment (V6 p.5).
- Rearranged: $F_{A,B-A} = DF_B / DF_A$ (Equation 8 of the reading) (V6 p.17).

> [!tip] Calculator
> `DF_B ÷ DF_A =`. Example: `0.8890 ÷ 0.9246 =` gives 0.9615 (V6 p.17).

**Forward price and forward rate of a deferred zero** (V6 p.7)
$$
F_{A,B-A} = \frac{1}{(1+f_{A,B-A})^{B-A}}
$$
^f-06-01-3

- $f_{A,B-A}$: forward rate agreed today for a loan starting at $A$ with tenor $B-A$; the first subscript is the start date, the second is the length.
- Holds by definition: the forward contract price is the present value at $A$ of the unit payment at $B$, discounted at the contracted forward rate.
- Misreading the subscripts (using $B$ as the end date in the exponent) is the single most common mechanical error in this module.

**Forward rate model** (V6 p.7)
$$
(1+z_B)^B = (1+z_A)^A\,(1+f_{A,B-A})^{B-A}
$$
^f-06-01-4

- $z_A$, $z_B$: spot rates for $A$ and $B$ periods ($B > A$); $f_{A,B-A}$: forward rate bridging them; all per period, decimals.
- Derivation: substitute Formula 1 and Formula 3 into Formula 2 and invert; investing to $B$ directly must equal investing to $A$ and rolling at the locked forward rate (V6 p.7).
- Two interpretations of $f$: breakeven reinvestment rate, and the rate locked in today by extending maturity (V6 p.8).

**Extracting a forward rate from two spot rates** (V6 p.7, p.8)
$$
f_{A,B-A} = \left[\frac{(1+z_B)^B}{(1+z_A)^A}\right]^{\frac{1}{B-A}} - 1
$$
^f-06-01-5

- Direct rearrangement of Formula 4; the root is needed only when the tenor $B-A$ exceeds one period.
- Example: $z_1 = 9\%$, $z_3 = 11\%$ give $f_{1,2} = [(1.11)^3/(1.09)]^{1/2} - 1 = 12.01\%$ (V6 p.9).

> [!tip] Calculator
> `1.11 y^x 3 = ÷ 1.09 = y^x 0.5 = - 1 =` gives 0.1201. For one-period tenors skip the root: `1.10 x^2 ÷ 1.09 = - 1 =` gives 0.1101.

**Spot rate as a geometric mean of forward rates** (V6 p.9)
$$
(1+z_T)^T = (1+z_1)(1+f_{1,1})(1+f_{2,1})\cdots(1+f_{T-1,1}), \qquad z_T = \left[\prod\right]^{1/T} - 1
$$
^f-06-01-6

- $f_{t,1}$: one-period forward rates starting at $t = 1, \dots, T-1$.
- Derivation: apply Formula 4 successively for $A = 1, 2, \dots, T-1$ and multiply the chain (Equations 5 and 6 of the reading).
- This is why the spot curve is an average and the forward curve is the margin, and why forwards proxy market expectations of future spot rates for active managers (V6 p.9).

**Spot-forward relation in ratio form** (V6 p.10)
$$
\left(\frac{1+z_B}{1+z_A}\right)^{\frac{A}{B-A}} (1+z_B) = 1 + f_{A,B-A}
$$
^f-06-01-7

- Algebraic restatement of Formula 4 (Equation 7 of the reading) used to sign the spot-forward gap.
- If $z_B > z_A$ (upward slope), the bracket exceeds a pure discount and $f_{A,B-A} > z_B$; if $z_B < z_A$, then $f_{A,B-A} < z_B$; flat curve gives $f = z$ (V6 p.10).
- Example: $A=1$, $B=5$, $z_1 = 2\%$, $z_5 = 3\%$ gives $f_{1,4} = (1.03/1.02)^{1/4}(1.03) - 1 = 3.25\% > 3\%$ (V6 p.10).

**Bootstrapping a spot rate from the par curve** (V6 p.13)
$$
1 = \frac{c_N}{(1+z_1)} + \frac{c_N}{(1+z_2)^2} + \cdots + \frac{1+c_N}{(1+z_N)^N}
$$
^f-06-01-8

- $c_N$: $N$-period par rate (coupon per unit of par that prices the bond at 1); $z_1, \dots, z_{N-1}$: spot rates already bootstrapped.
- Forward substitution, earliest to latest: $z_1 = c_1$, then each equation has one unknown, $z_N$, in the final term (V6 p.13).
- Solve: $(1+z_N)^N = (1+c_N) \Big/ \left(1 - \sum_{t=1}^{N-1} c_N DF_t\right)$.

> [!tip] Calculator
> For $z_2$ with $c_2 = 5.97\%$, $z_1 = 5\%$: `0.0597 ÷ 1.05 = +/- + 1 =` (store) then `1.0597 ÷ RCL =` `y^x 0.5 = - 1 =` gives 0.0600 (V6 p.13).

**Bond price via spot rates and via YTM** (V6 p.14)
$$
P = \sum_{t=1}^{T} \frac{CF_t}{(1+z_t)^t} = \sum_{t=1}^{T} \frac{CF_t}{(1+y_T)^t}
$$
^f-06-01-9

- $CF_t$: coupon (plus principal at $T$); $y_T$: yield to maturity, the single rate that reprices the same $P$.
- Because both must give the one market price, $y_T$ is a weighted average of $z_1, \dots, z_T$, weighted toward the spot rate of the largest cash flow (the final one) (V6 p.14, p.15).
- YTM equals expected return only if held to maturity, no default, and coupons reinvested at the original YTM (V6 p.15).

> [!tip] Calculator
> YTM after pricing off spots: enter `N`, `PV` (negative price), `PMT`, `FV`, `CPT I/Y`. Example: N=2, PV=-931.08, PMT=60, FV=1000 gives I/Y = 9.97 (V6 p.14).

**Expected bond return with forward-rate reinvestment** (V6 p.15, p.16)
$$
E[R_{ann}] = \left(\frac{\text{expected terminal wealth}}{P_0}\right)^{1/T} - 1, \quad \text{terminal wealth} = \sum_t CF_t \prod_{s=t}^{T-1}(1+f_{s,1})
$$
^f-06-01-10

- Each coupon is compounded forward to $T$ at the one-period forward rates assumed to be the future spot rates.
- Even under that assumption the expected return differs from YTM (9.00% versus 8.62% in the reading's five-year 10% coupon example); they coincide only for a flat curve (V6 p.16).

**Forward price invariance under forward-consistent evolution** (V6 p.17)
$$
F^{new}_{A-t,B-A} = \frac{DF^{new}_{B-t}}{DF^{new}_{A-t}} = \frac{DF_B/DF_t}{DF_A/DF_t} = F_{A,B-A} \quad \text{if } DF^{new}_T = \frac{DF_{t+T}}{DF_t}
$$
^f-06-01-11

- $DF^{new}_T$: discount function after $t$ periods; the condition says it equals today's implied forward discount function (Equations 9 to 11 of the reading).
- Consequence: the forward contract price changes only when the spot curve deviates from today's forward curve; expect future spots below the forwards and you buy the forward, above and you sell (V6 p.17).

**Rolldown identity: return when forwards are realized** (V6 p.18)
$$
\frac{(1+z_B)^B}{(1+f_{A,B-A})^{B-A}} = (1+z_A)^A
$$
^f-06-01-12

- Rearrangement of Formula 4 (Equation 12 of the reading) with horizon $A$: a $B$-period bond held $A$ periods, repriced at the forward rates, grows at the $A$-period spot rate.
- With $A = 1$: every bond earns the one-period risk-free rate over one period if spot rates evolve as the forward curve implies; each zero "rolls down" and earns the forward rate that rolls out of its pricing (V6 p.18, p.19).
- If the investor's expected future spot rate is below the quoted forward rate, the bond is undervalued and expected return exceeds the one-period rate; above, overvalued and it falls short (V6 p.20).

**Bond return decomposition** (V6 p.21)
$$
\text{Bond return} = \text{Coupons and principal} + \text{Reinvestment of coupons} \pm \text{Capital gain or loss on sale}
$$
^f-06-01-13

- The rolldown strategy's edge comes from the last term: under a static upward-sloping curve, the aged bond is sold at a lower yield and higher price (V6 p.21, p.22).

**Horizon return of a rolldown trade** (V6 p.21)
$$
r = \left(\frac{\text{total proceeds at horizon}}{P_0}\right)^{1/h} - 1
$$
^f-06-01-14

- Proceeds: coupons reinvested at the short rates plus sale price of the aged bond at the (unchanged) yield for its remaining maturity; $h$: horizon in years.
- Reading example: 7% six-year par bond over two years returns $(121.23/100)^{1/2} - 1 = 10.10\%$ versus 8.48% for the maturity-matched five-year 6% bond (V6 p.21).

> [!tip] Calculator
> Sale price: `N` = remaining years, `I/Y` = unchanged yield, `PMT`, `FV`, `CPT PV`. Then proceeds ÷ cost, `y^x (1 ÷ h) = - 1 =`.

**Par swap (swap rate) equation** (V6 p.25)
$$
\sum_{t=1}^{T} \frac{s_T}{(1+z_t)^t} + \frac{1}{(1+z_T)^T} = 1
$$
^f-06-01-15

- $s_T$: $T$-period swap rate (fixed leg); $z_t$: spot rates of the same curve; the right side is the floating leg's value at reset, always 1 at origination.
- Derivation: a par swap has zero value at inception, so the fixed leg (an annuity of $s_T$ plus notional) must be worth par; hence the swap curve is a par curve built off MRR-based rates (V6 p.23, p.25).
- Solve: $s_T = \left(1 - DF_T\right) / \sum_{t=1}^{T} DF_t$; swap rates, spot rates and discount factors are mutually recoverable (V6 p.26).

> [!tip] Calculator
> With discount factors listed: `1 - DF_T =` then `÷ (DF_1 + DF_2 + ... + DF_T) =`. Example: `1 - 0.8900 = ÷ (0.9524 + 0.8900) =` gives 0.0597 (V6 p.26).

**Swap spread** (V6 p.26, p.27)
$$
\text{Swap spread}_T = s_T - y^{govt,OTR}_T
$$
^f-06-01-16

- $s_T$: fixed rate of the $T$-maturity fixed-for-floating swap; $y^{govt,OTR}_T$: yield of the on-the-run government bond of the same maturity; quoted in bps.
- It prices bank-sector credit and liquidity premia over the sovereign, widens countercyclically, and has been zero to negative in the US since 2008 because of dealer capital requirements (V6 p.27, p.28, p.29).
- Watch negative government yields: spread = $0.16\% - (-0.10\%) = 0.26\%$ (V6 p.65, Q32).

**I-spread (interpolated spread)** (V6 p.27)
$$
ISPRD = y_{bond} - s_{interp}
$$
^f-06-01-17

- $y_{bond}$: bond YTM; $s_{interp}$: swap rate at the bond's maturity from straight-line interpolation of the swap curve.
- Sign convention flip versus the swap spread: the I-spread is the bond over the swap curve, the swap spread is the swap over the government curve (V6 p.27, p.29).
- A quoted bond yield can be rebuilt as same-maturity government yield plus swap spread (plus I-spread if nonzero) (V6 p.27, p.28).

**Z-spread pricing equation** (V6 p.28, p.29)
$$
P = \sum_{t=1}^{T} \frac{CF_t}{(1+z_t+Z)^t}
$$
^f-06-01-18

- $Z$: the single constant (zero-volatility) spread added to every point of the benchmark spot curve that makes discounted cash flows equal the bond's price.
- Preferred over the swap spread for pricing a specific risky bond off the government zero curve because it respects the whole term structure rather than one maturity point (V6 p.62, Q17).
- Example: 65 bps on spots of 2.25% and 2.70% prices a 4.15% two-year coupon bond at $4.15/1.029 + 104.15/(1.0335)^2 = 101.54$ (V6 p.64, Q28).

**TED spread** (V6 p.29, p.30)
$$
TED = MRR_{3m} - y^{T\text{-}bill}_{3m}
$$
^f-06-01-19

- Difference between the market reference rate (historically Libor) and the T-bill yield of matching maturity.
- A rise signals greater perceived counterparty credit and liquidity risk in the banking sector; it widens if the T-bill rate falls with MRR unchanged (V6 p.30, p.62).

**MRR-OIS spread** (V6 p.30)
$$
\text{MRR-OIS} = MRR - r_{OIS}
$$
^f-06-01-20

- $r_{OIS}$: fixed rate of an overnight indexed swap whose floating leg compounds a daily unsecured overnight rate (fed funds, Eonia).
- The market's standard barometer of money market risk and liquidity; SOFR (volume-weighted Treasury repo index, secured) is the transaction-based successor to survey-based Libor (V6 p.30).

**Term structure of yield volatility** (V6 p.39)
$$
\sigma(t,T) = \frac{\sigma\left[\Delta r(t,T)/r(t,T)\right]}{\sqrt{\Delta t}}
$$
^f-06-01-21

- Annualized standard deviation of the proportional change in the yield of the $T$-maturity zero over interval $\Delta t$ (lognormal convention).
- Example: monthly sd 10.15% annualizes as $0.1015/\sqrt{1/12} = 35.15\%$ (V6 p.39).
- Short rates are more volatile than long rates, but long bond prices move more because of duration; short vol is tied to monetary policy, long vol to the real economy and inflation (V6 p.39).

> [!tip] Calculator
> `12 √x × 0.1015 =` gives 0.3516; dividing by the square root of 1/12 is multiplying by the square root of 12.

**Portfolio effective duration and key rate durations** (V6 p.40)
$$
EffDur_{ptf} = \sum_i w_i\, EffDur_i, \qquad \sum_k KeyDur_k = EffDur_{ptf}
$$
^f-06-01-22

- $KeyDur_k$: sensitivity to a change in the benchmark curve at maturity segment $k$ only; a zero's effective duration equals its maturity.
- The key rate durations sum to effective duration because moving every key rate equally is a parallel shift (V6 p.40).
- Reading example: USD 100 each in 1-, 5-, 10-year zeros gives $EffDur = (1+5+10)/3 = 5.333$ and $KeyDur = 0.3333, 1.6667, 3.3333$ (V6 p.40).

**Key rate duration model of yield curve risk** (V6 p.40)
$$
\%\Delta P = \frac{\Delta P}{P} \approx -\,KeyDur_1 \Delta z_1 - KeyDur_5 \Delta z_5 - KeyDur_{10} \Delta z_{10}
$$
^f-06-01-23

- $\Delta z_k$: change in the key rate at segment $k$ (decimal); the minus signs carry the usual duration convention.
- Equation 15 of the reading; it captures shaping risk that a single effective duration misses (V6 p.40).

> [!tip] Calculator
> For a parallel 50 bp fall with KeyDurs 0.5, 0.7, 0.9: `0.5 + 0.7 + 0.9 = × 0.005 =` gives 0.0105 = +1.05%; falling yields raise value (V6 p.42).

**Factor model of yield curve risk** (V6 p.40)
$$
\%\Delta P \approx -\,D_L \Delta x_L - D_S \Delta x_S - D_C \Delta x_C
$$
^f-06-01-24

- $D_L, D_S, D_C$: sensitivities to the level, steepness and curvature factor movements; $\Delta x$: factor changes (Equation 16 of the reading).
- Reading example: $D_L = 5.3333$, $D_S = 3.0$, $D_C = 3.6667$; with $\Delta x_L = -0.0050$, $\Delta x_S = 0.002$, $\Delta x_C = 0.001$ the predicted change is $+1.7\%$ (V6 p.40, p.41).
- In exam exhibits the factor entries are often yield changes per one standard deviation move; then the yield change is (entry) x (number of sds), with the sign flipped for decreases (V6 p.58, p.67).

**Key rate durations to factor sensitivities** (V6 p.41)
$$
D_L = KeyDur_1 + KeyDur_5 + KeyDur_{10}, \quad D_S = -KeyDur_1 + KeyDur_{10}, \quad D_C = KeyDur_1 + KeyDur_{10}
$$
^f-06-01-25

- Follows from the definitions of the unit movements: parallel (all +1), steepness (short -1, long +1), curvature (short +1, mid 0, long +1); the three must not be linear combinations of each other (V6 p.40, p.41).
- Check with the reading's numbers: $D_L = 0.3333 + 1.6667 + 3.3333 = 5.3333$, $D_S = -0.3333 + 3.3333 = 3.0$, $D_C = 0.3333 + 3.3333 = 3.6667$ (V6 p.41).

**Bond risk premium** (V6 p.43)
$$
BRP = E[R_{long}] - R_{short}
$$
^f-06-01-26

- Expected excess return of a default-free long-term bond over an equivalent short-term bond or the one-period risk-free rate; also called the term or duration premium.
- Forward looking, estimated (not observed); measured on government bonds so that credit and liquidity premia are excluded (V6 p.43).
- Compressed by central bank asset purchases and strong domestic or foreign investor demand; raised by deficits and longer debt maturity structures (V6 p.44).

## Worked examples

### Example 1: Spot and forward prices and rates (1) (V6 p.5, p.6)

Setup: a two-year loan beginning in one year ($A = 1$, $B = 3$); $z_1 = 7\%$, $z_3 = 9\%$.

1. One-year discount factor (Formula 1): $DF_1 = 1/1.07 = 0.9346$.
2. Three-year discount factor: $DF_3 = 1/(1.09)^3 = 0.7722$.
3. Forward price (Formula 2): $0.7722 = 0.9346 \times F_{1,2}$, so $F_{1,2} = 0.7722/0.9346 = 0.8262$.
4. Interpretation: 0.8262 is the price agreed today, paid one year from today, for a two-year unit-principal zero maturing in three years; it is $DF_3/DF_1$.

Python check: `1/1.07 = 0.93458`, `1/1.09**3 = 0.77218`, `0.77218/0.93458 = 0.82624`. ^ex-06-01-1

### Example 2: Spot and forward prices and rates (2) (V6 p.8, p.9)

Setup: $z_1 = 9\%$, $z_2 = 10\%$, $z_3 = 11\%$.

1. $f_{1,1}$ (Formula 5): $(1.10)^2/1.09 - 1 = 1.2100/1.09 - 1 = 11.01\%$.
2. $f_{2,1}$: $(1.11)^3/(1.10)^2 - 1 = 1.367631/1.2100 - 1 = 13.03\%$.
3. $f_{1,2}$: $[(1.11)^3/1.09]^{1/2} - 1 = (1.254707)^{1/2} - 1 = 12.01\%$.
4. Relationship: the upward-sloping spot curve produces an upward-sloping forward curve, with the one-year forwards rising with the start date ($13.03\% > 11.01\%$).

Python check: `1.10**2/1.09 - 1 = 0.110092`, `1.11**3/1.10**2 - 1 = 0.130274`, `(1.11**3/1.09)**0.5 - 1 = 0.120137`. ^ex-06-01-2

### Example 3: Spot and forward prices and rates (3) (V6 p.9, p.10)

Setup: verify that $z_2$ and $z_3$ are geometric averages of $z_1$ and the forwards (Formula 6).

- $z_2 = [(1.09)(1.1101)]^{1/2} - 1 = (1.210009)^{1/2} - 1 \approx 10\%$.
- $z_3 = [(1.09)(1.1101)(1.1303)]^{1/3} - 1 = (1.367676)^{1/3} - 1 \approx 11\%$.

The tiny residuals come only from rounding the forwards to four decimals.
Python check: `(1.09*1.1101)**0.5 - 1 = 0.100004`, `(1.09*1.1101*1.1303)**(1/3) - 1 = 0.110011`. ^ex-06-01-3

### Example 4: Spot and forward prices and rates (4) (V6 p.10, p.11)

Setup: same spot curve, $z_1 = 9\% < z_2 = 10\% < z_3 = 11\%$.

1. Is $f_{1,2}$ above or below $z_3$? Upward slope means $f_{A,B-A} > z_B$ (Formula 7): indeed $f_{1,2} = 12.01\% > z_3 = 11\%$.
2. Do forwards rise with the start date $A$? Yes, for an upward-sloping curve: $f_{1,1} = 11.01\% < f_{2,1} = 13.03\%$.

Side check from the reading's own illustration of Formula 7: $z_1 = 2\%$, $z_5 = 3\%$ gives $f_{1,4} = (1.03/1.02)^{1/4}(1.03) - 1 = 3.25\%$; Python: `(1.03**5/1.02)**0.25 - 1 = 0.032515`. ^ex-06-01-4

### Example 5 (sidebar): What is bootstrapping? (V6 p.13)

Setup: annual-coupon par rates 5%, 5.97%, 6.91%, 7.81% for one to four years.

- $z_1 = c_1 = 5\%$ (single cash flow).
- $z_2$: $1 = 0.0597/1.05 + 1.0597/(1+z_2)^2$; the first term is 0.056857, so $(1+z_2)^2 = 1.0597/0.943143 = 1.123585$ and $z_2 = 6.00\%$.
- $z_3$: $1 = 0.0691/1.05 + 0.0691/(1.06)^2 + 1.0691/(1+z_3)^3$ gives $z_3 = 7.00\%$.
- $z_4$: $1 = 0.0781/1.05 + 0.0781/(1.06)^2 + 0.0781/(1.07)^3 + 1.0781/(1+z_4)^4$ gives $z_4 = 8.00\%$.

Spot rates sit above par rates at every maturity beyond one year because the coupons of a par bond are discounted at the lower earlier spots.
Python check: solving each equation gives 6.00%, 7.00%, 8.00% to two decimals. ^ex-06-01-5

### Example 6: Spot rate and yield-to-maturity (V6 p.14, p.15)

Setup: $z_1 = 9\%$, $z_2 = 10\%$, $z_3 = 11\%$.

Part 1: two-year 6% annual coupon bond, face USD 1,000 (Formula 9).
$P = 60/1.09 + 1060/(1.10)^2 = 55.05 + 876.03 = 931.08$.
Solving $931.08 = 60/(1+y_2) + 1060/(1+y_2)^2$ gives $y_2 = 9.97\%$.
So $z_1 < y_2 < z_2$, and $y_2$ hugs $z_2$ because the dominant cash flow is at year 2.

Part 2: three-year 5% annual coupon bond, face £100.
$P = 5/1.09 + 5/(1.10)^2 + 105/(1.11)^3 = 4.59 + 4.13 + 76.78 = 85.49$.
Solving gives $y_3 = 10.93\% < z_3 = 11\%$, again a weighted average tilted toward the final spot rate.

Python check: `60/1.09 + 1060/1.10**2 = 931.079`, root $y_2 = 9.970\%$; `5/1.09 + 5/1.1**2 + 105/1.11**3 = 85.494`, root $y_3 = 10.928\%$. ^ex-06-01-6

### Example 7 (in text): YTM versus expected return on a five-year bond (V6 p.15, p.16)

Setup: $z_1 \dots z_5 = 5, 6, 7, 8, 9\%$; five-year annual 10% coupon bond.

Step 1: price off spots: $P = 10/1.05 + 10/(1.06)^2 + 10/(1.07)^3 + 10/(1.08)^4 + 110/(1.09)^5 = 105.43$.
Step 2: forwards (Formula 5): $f_{1,1} = 7.0\%$, $f_{2,1} = 9.0\%$, $f_{3,1} = 11.1\%$, $f_{4,1} = 13.1\%$.
Step 3: YTM: solving the five-flow equation gives $y_5 = 8.62\%$.
Step 4: expected terminal wealth reinvesting each coupon at the forwards (Formula 10):
$10(1.07)(1.09)(1.111)(1.131) + 10(1.09)(1.111)(1.131) + 10(1.111)(1.131) + 10(1.131) + 110 \approx 162.22$.
Step 5: expected 5-year return $= 162.22/105.43 - 1 = 53.87\%$, annualized $(1.5387)^{1/5} - 1 = 9.00\%$.

The curriculum text prints one factor as $(1+0.011)$; that is a typo for $(1+0.111)$, and 162.22 is only reproduced with 0.111.
Even with forwards realized, expected return (9.00%) is not the YTM (8.62%): YTM is a realistic expected return only for a flat curve.
Python check: price `105.4295`, YTM `8.618%`, terminal `162.216`, annualized `9.000%`. ^ex-06-01-7

### Example 8: Yield and return concepts (V6 p.16)

1. Upward-sloping spot curve: the forward curve lies above it (A). Spots are averages; forwards are the marginal rates between future periods.
2. YTM of a default-risk-free bond: it is a weighted average of the spot rates applying to its cash flows (B). It equals expected return only under the restrictive reinvestment and holding assumptions, so A is wrong; a sloped curve makes YTM a worse, not better, estimate, so C is wrong.
3. Downward-sloping spot curve with a later initiation date: the forward curve is a greater distance below the spot curve (C), mirroring the upward-sloping case in Exhibit 2. ^ex-06-01-8

### Example 9 (in text): forward price invariance on a flat 4% curve (V6 p.17, p.18)

Setup: flat 4% curve.
$DF_1 = 0.9615$, $DF_2 = 0.9246$, $DF_3 = 0.8890$.

Forward price of a one-year zero delivered at year 2 (Formula 2 rearranged): $F_{2,1} = DF_3/DF_2 = 0.8890/0.9246 = 0.9615$.
One year later, if the new discount function equals today's forward discount function (Formula 11): $DF^{new}_1 = 0.9246/0.9615 = 0.9615$, $DF^{new}_2 = 0.8890/0.9615 = 0.9246$.
New forward price: $F^{new}_{1,1} = 0.9246/0.9615 = 0.9615$: unchanged.
Rolldown reading: after one year the three-year bond returned $(0.9246 - 0.8890)/0.8890 = 4\%$, the spot rate; the next year it returns $(0.9615 - 0.9246)/0.9246 = 4\%$, the implied forward rate.
Python check: `1/1.04 = 0.96154`, `1/1.04**2 = 0.92456`, `1/1.04**3 = 0.88900`, ratios all `0.96154`, returns both `4.000%`. ^ex-06-01-9

### Example 10 (sidebar): when spot rates evolve as implied by the forward curve (V6 p.18, p.19)

Setup: $z_1 = 9\%$, $z_2 = 10\%$, $z_3 = 11\%$, so $f_{1,1} = 11.01\%$ and $f_{1,2} = 12.01\%$; par 100.

- One-year zero: buy at $100/1.09 = 91.74$, worth 100 at maturity: return 9%.
- Two-year zero: buy at $100/(1.10)^2 = 82.64$; in one year it is a one-year zero priced at $100/1.1101 = 90.08$: return $90.08/82.64 - 1 = 9\%$.
- Three-year zero: buy at $100/(1.11)^3 = 73.12$; in one year priced at $100/(1.1201)^2 = 79.71$: return $79.71/73.12 - 1 \approx 9\%$.

If instead the year-1 curve is flat at 10%, the returns become 9%, 10% and 13.03%: only a deviation from the forwards separates bond returns from the one-year rate.
Python check: prices `91.743, 82.645, 73.119`; year-1 prices `90.082, 79.705`; returns `9.00%, 9.00%, 9.01%` (rounding), and `9%, 10.00%, 13.03%` in the flat-10% case. ^ex-06-01-10

### Example 11 (in text): projecting the curve above or below the forwards (V6 p.20)

Setup: flat 8% curve; three-year 8% annual coupon bond at par 100; one-year horizon.

- Forwards realized (flat 8% stays): return 8%.
- Projected flat 9% (spots above forwards): proceeds $= 8 + 8/1.09 + 108/(1.09)^2 = 106.24$, return $6.24\% < 8\%$.
- Projected flat 7% (spots below forwards): proceeds $= 8 + 8/1.07 + 108/(1.07)^2 = 109.81$, return $9.81\% > 8\%$.

The wider the gap between projected spots and the forwards, the further realized return drifts from the original YTM.
Python check: `(8 + 8/1.09 + 108/1.09**2)/100 - 1 = 6.241%`, `(8 + 8/1.07 + 108/1.07**2)/100 - 1 = 9.808%`. ^ex-06-01-11

### Example 12 (in text): riding the yield curve over a two-year horizon (V6 p.21)

Setup: par yields 2% (1y), 4% (3y), 5% (4y), 6% (5y), 7% (6y); two-year horizon within a five-year maturity target; curve assumed static.

Maturity-matched five-year 6% par bond:
- Year-1 coupon reinvested one year at 2%: $6 \times 1.02 = 6.12$; year-2 coupon 6.
- Sale price with three years left at an unchanged 4%: $6/1.04 + 6/(1.04)^2 + 106/(1.04)^3 = 105.55$.
- Proceeds $117.67$; annualized $(1.1767)^{1/2} - 1 = 8.48\%$.

Rolldown six-year 7% par bond:
- $7 \times 1.02 + 7 = 14.14$; sale with four years left at an unchanged 5%: $7/1.05 + 7/(1.05)^2 + 7/(1.05)^3 + 107/(1.05)^4 = 107.09$.
- Proceeds $121.23$; annualized $(1.2123)^{1/2} - 1 = 10.10\%$.

The extra 1.6 points per year come from the higher coupon and the larger price gain as the bond rolls to a lower yield.
Python check: `105.550`, `117.670`, `8.476%`; `107.092`, `121.232`, `10.105%`. ^ex-06-01-12

### Example 13: Active bond portfolio management (V6 p.22, p.23)

1. Rolldown is executed by buying maturities longer than the horizon (B); the bond is sold before maturity at a lower yield if the upward-sloping curve is static.
2. A bond is overvalued if the expected spot rate is higher than the current forward rate (C): the market discounts more gently than the investor believes is right.
3. Flat 6% curve, three-year 6% par bond, projected flat 7% in one year: proceeds $= 6 + 6/1.07 + 106/(1.07)^2 = 104.19$, return $4.19\%$ (A). B ignores the yield change; C would need yields to fall.
4. A forward contract price increases if future spot rates are lower than predicted by current forwards (B): the delivered bond is discounted at a lower rate than was priced in.

Python check for 3: `(6 + 6/1.07 + 106/1.07**2)/100 - 1 = 4.192%`. ^ex-06-01-13

### Example 14: Determining the swap rate curve (V6 p.25, p.26)

Setup: government discount factors $DF_1 = 0.9524$, $DF_2 = 0.8900$, $DF_3 = 0.8163$, $DF_4 = 0.7350$.

Step 1: spot rates (Formula 1 inverted): $z_1 = 1/0.9524 - 1 = 5.00\%$; $z_2 = (1/0.8900)^{1/2} - 1 = 6.00\%$; $z_3 = (1/0.8163)^{1/3} - 1 = 7.00\%$; $z_4 = (1/0.7350)^{1/4} - 1 = 8.00\%$.
Step 2: swap rates (Formula 15, solved as $s_T = (1 - DF_T)/\sum DF_t$):
- $s_1 = (1 - 0.9524)/0.9524 = 5.00\%$.
- $s_2 = (1 - 0.8900)/(0.9524 + 0.8900) = 0.1100/1.8424 = 5.97\%$.
- $s_3 = (1 - 0.8163)/(0.9524 + 0.8900 + 0.8163) = 0.1837/2.6587 = 6.91\%$.
- $s_4 = (1 - 0.7350)/(2.6587 + 0.7350) = 0.2650/3.3937 = 7.81\%$.

Swap rates, spot rates and discount factors are one data set in three costumes; note these swap rates equal the par rates of the bootstrapping sidebar because the inputs are the same curve.
Python check: `z = 4.998%, 6.000%, 7.000%, 8.001%`; `s = 5.00%, 5.97%, 6.91%, 7.81%`. ^ex-06-01-14

### Example 15 (in text): pricing off the swap spread, GECC notes (V6 p.28)

Setup: USD 1 million of 1.625% semiannual notes maturing 2 July 2024, evaluated 12 July 2021; remaining maturity $2 + 350/360 = 2.97$ years; two- and three-year Treasuries 0.525% and 0.588%; swap spread 0.918%; I-spread zero.

Step 1: interpolate the Treasury: $0.525\% + (350/360)(0.588\% - 0.525\%) = 0.586\%$.
Step 2: YTM $= 0.586\% + 0.918\% = 1.504\%$.
Step 3: invoice price: discount the six semiannual coupons of USD 8,125 and principal at $1.504\%/2$ per half-year with exponents $(n - 10/180)$ for $n = 1, \dots, 6$: $1{,}003{,}954.12$.
Step 4: accrued interest $= 1{,}000{,}000 \times (0.01625/2)(10/180) = 451.39$; clean price $= 1{,}003{,}954.12 - 451.39 = 1{,}003{,}502.73$.

Python check: interpolated rate `0.58625%`, invoice `1,003,954.12`, AI `451.39`, clean `1,003,502.73`. ^ex-06-01-15

### Example 16: Traditional term structure theories (V6 p.34, p.35)

1. Fallen angels' depressed prices from forced pension selling: segmented markets theory (B); the constraint is a hard prohibition, not a yield-induced preference (A) and has nothing to do with short-horizon returns (C).
2. Investors induced by attractive yields to leave their maturity match: preferred habitat theory (A); segmented markets does not allow the move, unbiased expectations assumes no preferences at all.
3. Unbiased expectations assumes investors are risk neutral (B): equal expected returns across maturity strategies only price if risk does not matter.
4. Market evidence shows forwards are upwardly biased predictors of future spot rates (B): liquidity premiums exist, refuting unbiasedness.
5. Short holding-period returns on short-maturity bonds are usually less than on long-maturity bonds (A): the evidence against local expectations. ^ex-06-01-16

### Example 17 (in text): key rate durations and factor durations of a zero portfolio (V6 p.40, p.41)

Setup: USD 100 each in 1-, 5-, 10-year zeros; portfolio USD 300; movements per the table: parallel (+1, +1, +1), steepness (-1, 0, +1), curvature (+1, 0, +1).

- Effective duration: $\tfrac{1}{3}(1 + 5 + 10) = 5.333$.
- Key rate durations (Formula 23): a 100 bp move in one rate changes value by that bond's duration in dollars: $KeyDur_1 = 1/(300 \times 0.01) = 0.3333$, $KeyDur_5 = 5/3 = 1.6667$, $KeyDur_{10} = 10/3 = 3.3333$; they sum to 5.333.
- Factor durations (Formula 25): $D_L = 5.3333$; a unit steepness move loses USD 10 on the long zero and gains USD 1 on the short zero, so $D_S = -(1 - 10)/(300 \times 0.01) = 3.0$; curvature: $D_C = (1 + 10)/(300 \times 0.01) = 3.6667$.
- Scenario $\Delta x_L = -0.0050$, $\Delta x_S = 0.002$, $\Delta x_C = 0.001$ (Formula 24): $\%\Delta P = -5.3333(-0.005) - 3.0(0.002) - 3.6667(0.001) = 0.02667 - 0.006 - 0.00367 = +1.70\%$.

Python check: `+0.017000`. ^ex-06-01-17

### Example 18: Term structure dynamics (V6 p.41, p.42)

1. Most important factor in yield curve changes: level (A); parallel shifts explain more than 75% of total variation.
2. Short rate down 150 bps, long rate down 50 bps: steepening from changes in level and steepness (B); both fell (level), the short end fell more (steeper).
3. Flat curve, intermediate yields fall 10 bps, ends unchanged: curvature only (B); the ends pin the level and slope.
4. Short-term rates are more volatile than long-term rates (B); long-horizon inflation and growth expectations move slowly.
5. KeyDurs 0.50, 0.70, 0.90, all yields down 50 bps: $\%\Delta P = -(0.50 + 0.70 + 0.90)(-0.005) = +1.05\%$ (B); A flips the sign, C doubles it.

Python check for 5: `+0.0105`. ^ex-06-01-18

### Example 19: Building a rate view from economic forecasts (V6 p.45, p.46)

Setup: recession today, low flat curve; the firm forecasts a quick return to growth within 12 months.

1. Consistent curve change: an increase in the term spread of long over short rates (C); growth expectations steepen the long end while the policy rate is still low.
2. The Fed also tapers long-bond purchases: reduced demand for long bonds raises their yields, so tapering amplifies the term-spread widening (A); it works in the same direction as the growth effect, not against it. ^ex-06-01-19

## Item-set patterns

> [!warning] Trap 1: the two subscripts of the forward rate
> The vignette asks for "the rate on a two-year loan beginning in one year" and gives $z_1, z_2, z_3$.
> Correct: $f_{1,2}$ links $z_1$ and $z_3$ with a square root: $[(1+z_3)^3/(1+z_1)]^{1/2} - 1$ (V6 p.9).
> Distractors: $f_{2,1} = (1+z_3)^3/(1+z_2)^2 - 1$ (subscripts swapped), and forgetting the root so the two-year rate is double-counted.
> Also tested in reverse: which forward cannot be computed; a loan ending beyond the longest quoted spot rate ($f_{2,3}$ from four spots) is uncomputable (V6 p.61).

> [!warning] Trap 2: bootstrapping direction and inputs
> A staff member "explains" bootstrapping with one wrong word: backward substitution, or latest-to-earliest, or "from forward rates".
> Correct: forward substitution, par yields as inputs, earliest to latest, one unknown spot per equation (V6 p.13, p.64).
> Distractor: accepting the description because "substitution" sounds right; the exam grades the direction words.

> [!warning] Trap 3: riding the yield curve conditions
> A manager with a two-year horizon buys a longer bond and the question asks when this beats maturity matching.
> Correct: upward-sloping curve expected to be static; the return edge is the higher coupon plus the capital gain from selling at the lower yield of a shorter maturity (V6 p.21).
> Distractors: "hold to maturity" (the strategy requires selling early), "the forward curve is below the spot curve" (it is above when the curve slopes up), and picking the country whose curve is inverted (V6 p.65).

> [!warning] Trap 4: expected spots versus forwards, valuation direction
> The investor projects future spot rates below (above) today's forward curve.
> Correct: below forwards means the market discounts too hard, price is below intrinsic value, the bond is undervalued and buying it earns more than the one-period rate if the view is right (V6 p.20, p.63).
> Distractors: reversing the direction, or concluding "fairly valued" whenever the curve is expected to be unchanged (unchanged spot curve is not the same as spots following the forwards).

> [!warning] Trap 5: which spread for which job
> Correct mapping: swap spread = swap rate minus on-the-run government yield (market credit barometer and quoting convention); I-spread = bond yield minus interpolated swap rate; Z-spread = constant addition to the whole spot curve that reprices one risky bond; TED and MRR-OIS = money market credit and liquidity stress (V6 p.27 to p.30).
> Distractors: using the TED or MRR-OIS spread to price a corporate bond (Z-spread is the answer), or the Z-spread to describe economy-wide bank risk (V6 p.62, p.64).

> [!warning] Trap 6: negative yields in swap spread arithmetic
> The exhibit shows a government yield of -0.08% and a swap rate of 0.01%.
> Correct: spread $= 0.01\% - (-0.08\%) = 0.09\%$; subtracting a negative adds (V6 p.65).
> Distractors: 0.07% (sign dropped) or -0.09% (order flipped); also ranking periods by swap rate alone instead of by spread.

> [!warning] Trap 7: factor exhibit signs and standard deviations
> The exhibit lists yield changes per one standard deviation increase in level, steepness, curvature; the question asks for a two-sd increase or a one-sd decrease.
> Correct: multiply the table entry by the number of sds, flip the sign for decreases, and add contributions; a steepness entry of -0.3015% doubled is -0.6030% (V6 p.58, p.67).
> Distractors: forgetting to double, not flipping signs for decreases (the 0.0389% versus -0.0389% pair), or summing all three factors when only two moved.

> [!warning] Trap 8: KRD arithmetic and the minus sign
> Correct: $\%\Delta P = -\sum KeyDur_k \Delta z_k$; falling yields raise value; key rate durations sum to effective duration, and only KRDs or factor durations capture shaping risk, never effective duration alone (V6 p.40, p.42, p.67).
> Distractors: answer choices with the sign flipped, or "effective duration" offered as a shaping-risk measure.

> [!warning] Trap 9: bull/bear, flattening/steepening mapping
> Correct: rate hikes in expansions = bear flattening (short end up more); rate cuts in recessions = bull steepening (short end down more); flight to quality = bull flattening (long end down more); growth and taper views widen the term spread (V6 p.43, p.44, p.45).
> Distractors: bear steepening for a hiking cycle, or bearish flattening for flight to quality; anchor on which end moves more and in which direction.

> [!warning] Trap 10: volatility term structure double inversion
> The vignette notes short rates are more volatile, then asks about price volatility or the drivers.
> Correct: yield vol falls with maturity, but price vol still rises with maturity because duration multiplies the smaller yield moves; short vol is monetary policy uncertainty, long vol is real economy and inflation uncertainty (V6 p.39, p.67).
> Distractors: "long rates are more volatile" (confusing price with yield vol) and swapping the two uncertainty drivers.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM01-The-Term-Structure-and-Interest-Rate-Dynamics-Practice-Problems]]

## Cross-links

- [[LM02-The-Arbitrage-Free-Valuation-Framework]]: the spot curve, discount function and forward rates built here are the calibration targets for the binomial interest rate tree; arbitrage-free valuation is this module's no-arbitrage principle made operational.
- [[LM03-Valuation-and-Analysis-of-Bonds-with-Embedded-Options]]: option values in callable and putable bonds depend on the interest rate volatility whose term structure is introduced here, and OAS extends the Z-spread idea once optionality is stripped.
- [[LM04-Credit-Analysis-Models]]: credit spread measures build on the benchmark curves and the Z-spread defined here; the swap spread's credit content previews spread decomposition into default and liquidity components.
- [[LM05-Credit-Default-Swaps]]: CDS spreads join the swap spread, TED and MRR-OIS in the toolkit of market-implied credit risk barometers, and CDS pricing discounts off the swap curve.
- [[LM01-Pricing-and-Valuation-of-Forward-Commitments]]: the par swap equation (fixed leg PV = floating leg PV = 1) is exactly how Derivatives prices interest rate swaps, and forward rate extraction here is the input to FRA pricing.
- [[LM01-Economics-and-Investment-Markets]]: the bond risk premium, the policy-driven short rate, and the business cycle behavior of the curve (bear flattening, bull steepening, flight to quality) are developed there as part of the economics of asset pricing.

## Self-test

Vignette A for Q1 to Q4: Kessler observes annual-coupon government spot rates of $z_1 = 3.0\%$, $z_2 = 3.6\%$ and $z_3 = 4.2\%$.
Her investment horizon is one year, and she expects the curve to be unchanged in one year.
Her colleague Braun instead projects that the one-year spot rate two years from today will be 5.00%.

> [!question] Q1
> The forward rate for a one-year loan beginning in one year is closest to:
> A. 3.60%.
> B. 4.20%.
> C. 5.41%.

> [!question] Q2
> The forward rate for a one-year loan beginning in two years is closest to:
> A. 4.20%.
> B. 4.81%.
> C. 5.41%.

> [!question] Q3
> If the spot curve is unchanged in one year, the one-year holding-period return on a three-year zero-coupon bond is closest to:
> A. 3.00%.
> B. 4.20%.
> C. 5.41%.

> [!question] Q4
> Based on Braun's projection, the three-year zero-coupon bond is most likely:
> A. undervalued.
> B. fairly valued.
> C. overvalued.

Vignette B for Q5 to Q7: Osei has annual-coupon sovereign par rates of 2.00% (one year) and 2.50% (two years).
The two-year fixed-for-floating MRR swap rate is 2.95% and the two-year on-the-run government bond yields 2.48%.
A two-year corporate bond with a 3.00% annual coupon trades with a Z-spread of 80 bps to the government spot curve.

> [!question] Q5
> The two-year government spot rate is closest to:
> A. 2.25%.
> B. 2.51%.
> C. 3.02%.

> [!question] Q6
> The two-year swap spread is closest to:
> A. 0.44%.
> B. 0.47%.
> C. 0.95%.

> [!question] Q7
> The price of the corporate bond per 100 of par is closest to:
> A. 97.93.
> B. 99.43.
> C. 100.97.

Vignette C for Q8 to Q10: Duval manages a government bond portfolio with key rate durations of 0.8 (1-year), 1.5 (5-year) and 2.7 (10-year).
Her factor model reports yield changes per one standard deviation increase in each factor: for the 20-year bond, level -0.50%, steepness -0.30%, curvature +0.52%.
Duval expects an equity market selloff to trigger a flight into government bonds.

> [!question] Q8
> A two-standard-deviation decrease in the level factor changes the 20-year yield by:
> A. -1.00%.
> B. +0.50%.
> C. +1.00%.

> [!question] Q9
> If the 1-year key rate rises 40 bps, the 5-year key rate is unchanged, and the 10-year key rate falls 20 bps, the percentage change in portfolio value is closest to:
> A. -0.22%.
> B. +0.22%.
> C. +0.86%.

> [!question] Q10
> Given her flight-to-quality expectation, Duval's best-positioned trade is to:
> A. shift from a barbell to a bullet portfolio of the same duration.
> B. shift from a bullet to a barbell portfolio of the same duration.
> C. shorten portfolio duration against the benchmark.

> [!success]- Answer key
> Q1: B.
> $f_{1,1} = (1.036)^2/1.03 - 1 = 4.20\%$ (Python: `1.036**2/1.03 - 1 = 4.203%`).
> A repeats $z_2$; C is $f_{2,1}$, the forward starting one year later.
> Q2: C.
> $f_{2,1} = (1.042)^3/(1.036)^2 - 1 = 5.41\%$ (Python: `1.042**3/1.036**2 - 1 = 5.410%`).
> A repeats $z_3$; B is $f_{1,2} = [(1.042)^3/1.03]^{1/2} - 1 = 4.81\%$, the two-year-tenor forward.
> Q3: C.
> Buy at $100/(1.042)^3 = 88.39$; in one year the bond is a two-year zero at the unchanged $z_2 = 3.6\%$, worth $100/(1.036)^2 = 93.17$; return $= 93.17/88.39 - 1 = 5.41\%$, exactly $f_{2,1}$, the forward that rolls out of the pricing.
> A is the return if spots evolve as the forwards imply (the one-year rate); B repeats $z_3$.
> Q4: A.
> Braun's expected future spot (5.00%) is below the implied forward $f_{2,1} = 5.41\%$, so the market is discounting the year-3 cash flow harder than he believes is warranted: the bond is undervalued to him.
> B needs expectations equal to the forwards; C needs expectations above them.
> Q5: B.
> Bootstrap: $1 = 0.025/1.02 + 1.025/(1+z_2)^2$ gives $z_2 = 2.51\%$ (Python: `2.5063%`).
> A is the average of the par rates; C is the implied forward $f_{1,1} = (1.0251)^2/1.02 - 1 = 3.02\%$, not a spot rate.
> Q6: B.
> Swap spread $=$ swap rate minus same-maturity on-the-run government yield $= 2.95\% - 2.48\% = 0.47\%$.
> A wrongly uses the bootstrapped spot (2.51%) instead of the on-the-run yield; C halves-and-doubles into the sum of the spreads.
> Q7: B.
> Add 80 bps to each spot: $3/1.028 + 103/(1.033063)^2 = 99.43$ (Python: `99.431`).
> A adds the spread twice (160 bps, giving 97.93); C prices at the bare government spots with no Z-spread (100.97).
> Q8: C.
> Entries are per one sd increase; a two-sd decrease flips the sign and doubles: $-2 \times (-0.50\%) = +1.00\%$.
> A forgets to flip the sign for a decrease; B forgets to double.
> Q9: B.
> $\%\Delta P = -0.8(0.004) - 1.5(0) - 2.7(-0.002) = -0.0032 + 0.0054 = +0.22\%$ (Python: `+0.0022`).
> A flips the overall sign; C multiplies total duration by 20 bps, ignoring which rates moved and in which direction.
> Q10: B.
> Flight to quality produces bullish flattening: long yields fall more than short yields.
> A barbell of the same duration loads more exposure onto the long end that rallies most, so shifting bullet to barbell captures the flattening; A is the flattening-loser, and C is positioned for rising rates, the opposite of the view.

## Flashcards

#flashcards/cfa-l2/06-Fixed-Income/lm01

Discount factor with maturity N::Price today of a default-risk-free unit payment in N periods; DF_N = 1/(1+z_N)^N (V6 p.4).
Why the spot rate avoids a reinvestment assumption::A zero-coupon bond has a single payment at maturity, so the stated yield is the realized return if held to maturity (V6 p.5).
Forward pricing model::DF_B = DF_A x F, so the forward price of a deferred zero is F = DF_B / DF_A (V6 p.5, p.17).
Forward rate model::(1+z_B)^B = (1+z_A)^A (1+f)^(B-A), with f the rate for a loan starting at A with tenor B-A (V6 p.7).
Two interpretations of a forward rate::Breakeven reinvestment rate between long and rolled-over short zeros, and the rate locked in today by extending maturity (V6 p.8).
Micro-problem: z1 9%, z2 10%; f1,1?::1.10 squared over 1.09 minus 1 = 11.01%; keystrokes 1.10 x^2 / 1.09 = - 1 = (V6 p.8).
Micro-problem: z1 9%, z3 11%; f1,2?::(1.11^3 / 1.09) to the one-half minus 1 = 12.01%; do not forget the square root for the two-year tenor (V6 p.9).
Spot rate as a function of forward rates::Geometric mean of the first-period spot rate and the chain of one-period forwards (V6 p.9).
Forward curve position when the spot curve slopes upward::Above the spot curve, rising and steepening with later start dates (V6 p.10, p.11).
Forward curve position when the spot curve slopes downward::Below the spot curve, lower for later start dates (V6 p.12).
When do forward rates equal spot rates?::When the yield curve is flat (V6 p.10).
The par curve::Yields to maturity on coupon-paying government bonds priced at par across maturities, built from on-the-run issues (V6 p.12).
Bootstrapping entails {{forward}} substitution using {{par}} yields to solve for zero-coupon rates one by one from {{earliest to latest}} maturities (V6 p.13).
Micro-problem: par rates 5% and 5.97%; z2?::Solve 1 = 0.0597/1.05 + 1.0597/(1+z2)^2, giving z2 = 6.00% (V6 p.13).
YTM in terms of spot rates::A weighted average of the spot rates discounting the bond's cash flows, tilted toward the spot rate of the largest (final) cash flow (V6 p.14, p.15).
Assumptions under which YTM equals expected return::Held to maturity, no default, all coupons reinvested at the original YTM (V6 p.15).
Four conditions that make YTM a poor expected-return estimate::Volatile rates, a sloped yield curve, significant default risk, embedded options (V6 p.15).
When is YTM a realistic expected return even with forwards realized?::Only when the yield curve is flat (V6 p.16).
What must happen for a forward contract price to change?::The spot curve must deviate from what today's forward curve predicted (V6 p.17).
Return on every default-free bond if spots evolve as forwards imply::The one-period risk-free rate, regardless of maturity (V6 p.18, p.19).
A bond is undervalued when the investor's expected spot rates are::Below the quoted forward rates; the market discounts harder than the investor believes right (V6 p.20).
Trader expects future spots above the forward curve; expected return versus YTM?::Below the original YTM; prices fall relative to the forward-implied path (V6 p.20).
Conditions for riding the yield curve to beat maturity matching::Upward-sloping yield curve expected to be static over the horizon; buy longer than the horizon and sell at the horizon (V6 p.21).
Sources of the rolldown trade's excess return::Higher coupon income plus the capital gain from revaluation at the lower yield of a shorter maturity (V6 p.21).
Maturity spread carry trade::Borrow short term, lend long term in the same currency; profitable on a steep static curve, exposed to unexpected rate rises (V6 p.21, p.22).
Micro-problem: static par curve, 6-year 7% par bond held 2 years, sale yield 5%?::Proceeds 7(1.02) + 7 + 107.09 = 121.23; return (1.2123)^0.5 - 1 = 10.10% (V6 p.21).
The swap rate::The fixed rate of an interest rate swap that gives the swap zero value at initiation (V6 p.23).
Why the swap curve is a par curve::Par swaps set the fixed-leg PV equal to the floating-leg PV, which is 1 at origination (V6 p.23, p.25).
Par swap equation::Sum of s_T/(1+z_t)^t for t = 1..T plus 1/(1+z_T)^T equals 1; solve s_T = (1 - DF_T)/sum of DF_t (V6 p.25).
Micro-problem: DF1 0.9524, DF2 0.8900; s2?::(1 - 0.8900)/(0.9524 + 0.8900) = 5.97% (V6 p.26).
Why use the swap curve as benchmark?::More maturities, high liquidity, no dependence on government supply, comparable across countries, matches how wholesale banks hedge (V6 p.24, p.27).
Swap spread definition::Swap fixed rate minus the yield of the on-the-run government bond of the same maturity (V6 p.26, p.27).
Micro-problem: swap 0.16%, government yield -0.10%; swap spread?::0.16 - (-0.10) = 0.26%; subtracting a negative adds (V6 p.65).
Why have US swap spreads been negative since 2008?::Strong duration demand, tighter liquidity, counterparty risk, and higher regulatory capital requirements for swap dealers (V6 p.27, p.29).
I-spread::Bond YTM minus the swap rate interpolated to the bond's maturity (V6 p.27).
Z-spread::The constant spread added to every point of the benchmark spot curve that makes discounted cash flows equal the risky bond's price (V6 p.28, p.29).
Which spread prices a specific corporate bond off the Treasury zero curve?::The Z-spread; TED and MRR-OIS are economy-wide money market gauges (V6 p.62).
TED spread::MRR (historically 3-month Libor) minus the matching-maturity T-bill rate; gauges banking sector credit and liquidity risk (V6 p.29, p.30).
MRR-OIS spread::MRR minus the overnight indexed swap rate; the standard money market risk and liquidity barometer (V6 p.30).
SOFR::Secured overnight financing rate; volume-weighted index of Treasury repo transactions, reflecting secured funding supply and demand (V6 p.30).
Unbiased (pure) expectations theory::Forward rates are unbiased predictors of future spot rates; maturities are perfect substitutes; requires risk neutrality (V6 p.31).
Local expectations theory::Every bond earns the risk-free rate over short holding periods; extends to risky worlds but is refuted because long bonds out-earn short bonds even over short horizons (V6 p.31).
Liquidity preference theory::Liquidity premiums rising with maturity compensate interest rate risk; forwards are upward-biased predictors of future spots (V6 p.31, p.32).
Segmented markets theory::Yields set independently by supply and demand within each maturity segment, driven by asset/liability matching constraints (V6 p.32).
Preferred habitat theory::Participants have preferred maturities but leave them when expected extra return is sufficient; best fits real phenomena such as QE effects on MBS yields (V6 p.32, p.33).
The three Litterman-Scheinkman factors::Level (parallel shift, dominant), steepness (short versus long), curvature (middle versus ends) (V6 p.37, p.38).
Yield volatility term structure::Annualized sd of proportional yield changes by maturity; short rates more volatile than long rates (V6 p.39).
Micro-problem: monthly yield sd 10.15%; annualized?::0.1015 divided by the square root of 1/12 = 35.15% (V6 p.39).
Drivers of short-term versus long-term yield volatility::Short is monetary policy uncertainty; long is real economy and inflation uncertainty (V6 p.39).
Key rate duration::Sensitivity of value to a small change in the benchmark curve at one maturity segment; KRDs sum to effective duration (V6 p.39, p.40).
Which risk measures capture shaping risk?::Key rate durations and level/steepness/curvature sensitivities; effective duration cannot (V6 p.67).
Micro-problem: KeyDurs 0.5, 0.7, 0.9; all yields -50 bps; %change?::-(0.5+0.7+0.9)(-0.005) = +1.05%; keystrokes 0.5 + 0.7 + 0.9 = x 0.005 = (V6 p.42).
Bond risk premium::Expected excess return of a default-free long-term bond over an equivalent short-term bond; forward looking, must be estimated (V6 p.43).
Which factor dominates short and intermediate yield variation? Long-term?::Monetary policy explains about two-thirds of short and intermediate variation; inflation about two-thirds of long-term variation (V6 p.43).
Bear flattening::Short yields rise more than long yields; typical of policy tightening in expansions (V6 p.43).
Bull steepening::Short yields fall more than long yields; typical of policy easing in recessions (V6 p.43).
Bull flattening::Long yields fall more than short yields; the flight-to-quality signature (V6 p.44).
Trade for an expected bullish flattening under a long-only mandate::Shift from a bullet to a same-duration barbell to weight the rallying long end (V6 p.45).
Duration positioning for a rate view::Extend duration if rates are expected to fall, shorten if expected to rise; steepener/flattener trades are built duration neutral (V6 p.45).

## Common mistakes

1. Misreading forward rate subscripts: in $f_{A,B-A}$ the first index is the start date and the second is the tenor, so $f_{1,2}$ ends at year 3, not year 2 (V6 p.5, p.9).
2. Forgetting the root when the forward tenor exceeds one period, or the power when annualizing a multi-period return (V6 p.9, p.61).
3. Trying to compute a forward whose end date runs beyond the longest available spot rate (V6 p.12, p.61).
4. Describing bootstrapping as backward substitution or latest-to-earliest; it is forward substitution on par yields, earliest to latest (V6 p.13, p.64).
5. Treating YTM as expected return without the held-to-maturity, no-default, reinvest-at-YTM assumptions, or forgetting that only a flat curve makes YTM realistic even with forwards realized (V6 p.15, p.16).
6. Reversing the valuation rule: expected spots below the forwards means undervalued (buy); above means overvalued (V6 p.20, p.63).
7. Claiming an unchanged upward-sloping curve gives every bond the one-period rate; that outcome needs spots to follow the forward curve, while a static curve delivers the rolldown premium (V6 p.18, p.21).
8. Mixing up spread directions: swap spread = swap minus government; I-spread = bond minus swap; and mishandling negative government yields in the subtraction (V6 p.27, p.65).
9. Pricing a corporate bond with the TED or MRR-OIS spread instead of the Z-spread, or judging money market stress with a Z-spread (V6 p.62, p.64).
10. Matching theories loosely: forced constraints are segmented markets, yield-induced migration is preferred habitat, risk neutrality belongs to unbiased expectations, and only local expectations survives risk while still failing empirically (V6 p.31 to p.35).
11. Ignoring the per-standard-deviation convention in factor exhibits: multiply by the number of sds and flip signs for decreases (V6 p.58, p.67).
12. Dropping the minus sign in $\%\Delta P = -\sum KeyDur_k \Delta z_k$, or expecting effective duration to measure shaping risk (V6 p.40, p.67).
13. Concluding long rates are more volatile because long bond prices move more; yield vol falls with maturity while duration amplifies price vol (V6 p.39).
14. Mapping a hiking cycle to bear steepening or a flight to quality to bear flattening; anchor on which end moves more and whether yields rise or fall (V6 p.43, p.44).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "06-01" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
