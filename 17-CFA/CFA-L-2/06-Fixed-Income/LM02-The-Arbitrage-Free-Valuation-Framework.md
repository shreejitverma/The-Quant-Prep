---
type: cfa-lm
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
volume: 6
lm: 2
title: "The Arbitrage-Free Valuation Framework"
pages: "69-117"
weight_band: "10-15%"
difficulty: 3
los_count: 9
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/fixed-income]
---

# LM2: The Arbitrage-Free Valuation Framework

Difficulty 3 of 5: the ideas are few (one price, one tree, one node formula), but the item sets demand fast, error-free backward induction and calibration arithmetic under time pressure, and the term-structure-model taxonomy at the end is pure memorization that the exam tests with swapped definitions.

## LOS map

- **explain** what is meant by arbitrage-free valuation of a fixed-income instrument (V6 p.69) ^los-06-02-a
    - Examiner asks: given prices and payoffs for two risk-free assets, or one bond quoted on three exchanges, identify whether an arbitrage exists, name the violated principle (value additivity or dominance), and state the trade that captures it.
- **calculate** the arbitrage-free value of an option-free, fixed-rate coupon bond (V6 p.69) ^los-06-02-b
    - Examiner asks: bootstrap spot rates from a par curve, discount each cash flow at its own spot rate, and quantify the mispricing versus the market or YTM-based price.
- **describe** a binomial interest rate tree framework (V6 p.69) ^los-06-02-c
    - Examiner asks: which three inputs the tree needs (interest rate model, volatility, benchmark curve), why the lognormal model keeps rates positive, and how adjacent nodes relate through $e^{2\sigma}$.
- **describe** the process of calibrating a binomial interest rate tree to match a specific term structure (V6 p.69) ^los-06-02-d
    - Examiner asks: given the higher rate at a node, compute the lower rate as $i_H e^{-2\sigma}$, or explain that rates are found iteratively so the tree reprices the benchmark par bonds, or predict what happens to the tree when volatility changes.
- **describe** the backward induction valuation methodology and calculate the value of a fixed-income instrument given its cash flow at each node (V6 p.69) ^los-06-02-e
    - Examiner asks: fill in a missing node value or the Time 0 price with the node formula, discounting coupon plus the average of the two next-period values at the node's own one-year rate.
- **compare** pricing using the zero-coupon yield curve with pricing using an arbitrage-free binomial lattice (V6 p.69) ^los-06-02-f
    - Examiner asks: whether the tree value of an option-free bond differs from the spot-rate value at a different volatility (it never does), and why calibration is worth doing at all (it lets the tree price embedded options).
- **describe** pathwise valuation in a binomial interest rate framework and calculate the value of a fixed-income instrument given its cash flows along each path (V6 p.69) ^los-06-02-g
    - Examiner asks: count the paths through an n-period tree ($2^{n-1}$), then discount a bond's cash flows along one specified path using the cumulative product of the path's forward rates.
- **describe** a Monte Carlo forward-rate simulation and its application (V6 p.69) ^los-06-02-h
    - Examiner asks: when Monte Carlo is required instead of a tree (path-dependent cash flows such as MBS), what the drift adjustment accomplishes, and whether more paths bring the estimate closer to fundamental value (statistical accuracy only).
- **describe** term structure models and how they are used (V6 p.69) ^los-06-02-i
    - Examiner asks: classify CIR, Vasicek, Ho-Lee and KWF as equilibrium or arbitrage-free, match each to its drift and volatility terms, and say which can produce negative rates and which fits the observed curve.

## Core intuition

The whole module is one economic idea worked out with increasing machinery: if two positions deliver identical cash flows, they must trade at the same price, or free money exists and traders will take it until it is gone (V6 p.71).
An arbitrage opportunity is a transaction with no cash outlay that produces a riskless profit, and the principle of no arbitrage says well-functioning markets price such opportunities away (V6 p.70, p.71).
The corollary that runs through every calculation here is blunt: if you put up no money and take no risk, your expected return is zero (V6 p.71).

The curriculum names two ways an arbitrage can appear (V6 p.71, p.72).
Value additivity is violated when the whole trades away from the sum of its parts: a package of 105 one-dollar zeros worth 100 sells as a portfolio for 97, so you sell the parts, buy the package, and pocket 3 today with zero net cash flow in one year (V6 p.71).
Dominance is violated when two risk-free claims imply different discount rates: an asset paying 220 priced at 200 (10% implied) next to an asset paying 105 priced at 100 (5% implied) lets you sell two of the expensive one and buy the cheap one, collecting 10 in one year for nothing today (V6 p.72).
The exam names these principles explicitly, so learn the labels, not just the trades.

> [!abstract] Idea 1: a coupon bond is a package of zero-coupon bonds
> Every fixed-income security should be viewed as a portfolio of zeros, one per cash flow, each discounted at the spot rate matching its own date (V6 p.71, p.73).
> The market enforces this through stripping (dealers separating cash flows into tradable zeros) and reconstitution (recombining zeros into the coupon bond), so value additivity holds between a bond and its stripped pieces (V6 p.73).
> Discounting every cash flow at the bond's single YTM instead of the spot curve over-discounts early coupons when the curve slopes up and under-discounts them when it slopes down, which is precisely the mispricing the exam asks you to quantify (V6 p.74).

Spot-rate discounting settles the option-free case completely.
The reason the module does not stop there is that a bond with an embedded option has cash flows that depend on future interest rates: whether the issuer calls or the holder puts is decided later, at rate levels not yet known (V6 p.75).
To value such bonds we must let future rates take multiple values, disciplined by an assumed volatility, and the vehicle for that is the binomial interest rate tree, a lattice of possible one-year forward rates (V6 p.75, p.76).
The tree does two jobs at once: it generates the rate-dependent cash flows, and it supplies the discount rates that convert them to present value (V6 p.75).

> [!abstract] Idea 2: the lognormal tree spreads rates around the forward curve, two standard deviations between adjacent nodes
> The one-factor lognormal random walk gives two possible next-period rates at each node, roughly one standard deviation above and below the implied forward rate, so $i_H = i_L e^{2\sigma}$ and, more generally, any two adjacent nodes at a date differ by the multiplier $e^{2\sigma}$ (V6 p.77, p.78).
> Lognormality buys two properties for free: rates can never go negative, and rate moves are proportional to the level of rates, since the standard deviation of the one-year rate is $i_0\sigma$ (V6 p.77, p.79).
> The tree recombines (up-down equals down-up), so the number of nodes grows linearly, not exponentially, which is what makes the lattice computable (V6 p.78).

The tree is useless until it is calibrated, and calibration is where the arbitrage-free discipline bites.
We choose the node rates so that the tree exactly reprices the benchmark par bonds, one maturity at a time: guess the lowest rate for a date, set the others as $e^{2\sigma}$ multiples, discount the benchmark bond backward through the tree, and adjust (by Solver or iteration) until the model price equals par (V6 p.82, p.83).
Three constraints pin the rates down: the interest rate model, the volatility assumption, and the current benchmark yield curve (V6 p.75, p.84).
Once calibrated, the tree is tied to the same economic reality as the spot curve, and the average of the two Time 1 rates sits just above the implied forward rate (1.4032% versus 1.4028% in the text's example) because of the lognormal spread (V6 p.84).
Volatility controls the fan: at 20% the rates spread wider around the forward curve, and at 0.01% the tree collapses onto the implied forward rates, so with zero volatility the tree is the forward curve (V6 p.86).

![[Binomial-Interest-Rate-Tree.excalidraw]]

Valuation on the tree runs backward.
At maturity the bond is worth par plus the final coupon, so those values are known; each earlier node discounts the coupon plus the equal-weighted average of the two next-period values at that node's own one-year rate, and the recursion walks right to left until Time 0 (V6 p.80).
The probabilities are 0.5 and 0.5 by construction of the lognormal model, so no probability inputs ever appear in the arithmetic (V6 p.80).
The payoff for all this work is a consistency check the exam loves: an option-free bond valued on a correctly calibrated tree gives exactly the spot-rate price, at any volatility, because both methods are arbitrage free (V6 p.89, p.90).
Calibration therefore does not improve the pricing of option-free bonds at all; its entire value is that the verified tree can then price bonds with embedded options, which spot rates cannot (V6 p.114).

> [!abstract] Idea 3: backward induction, pathwise valuation and Monte Carlo are three routes to the same present value
> Pathwise valuation enumerates every route through the tree ($2^{n-1}$ paths for n periods, counted with Pascal's Triangle), discounts the bond's cash flows along each path with the cumulative product of that path's forward rates, and averages; the answer equals the backward induction value (V6 p.91, p.92, p.93).
> Monte Carlo replaces the enumerated paths with a large random sample, which is the only practical route when cash flows are path dependent, as with mortgage prepayments that depend on where rates have been, not just where they are (V6 p.94, p.95).
> A Monte Carlo model is not automatically arbitrage free: a constant drift term is added to all rates on all paths until each benchmark bond's average present value equals its market price (V6 p.95).

Monte Carlo details matter for the item sets.
The mortgage application simulates hundreds of monthly short-rate paths under a volatility assumption, builds spot rates from them, projects path-dependent cash flows, discounts each path, and averages (V6 p.95).
More paths tighten the statistical estimate but do not move it closer to fundamental value, because the output is only as good as the model and inputs (V6 p.95, p.117).
Modelers often impose mean reversion through bounds on the rate process, pulling simulated rates toward the implied forwards (V6 p.95).

The final section asks where the node-generating assumptions come from: term structure models, stochastic processes $dr = \theta_t dt + \sigma_t dZ$ whose drift and volatility terms define each named model (V6 p.97).
Equilibrium models (CIR, Vasicek) derive rates from fundamental economic variables with few parameters, use real probabilities, and generally do not match today's observed curve (V6 p.98).
Arbitrage-free models (Ho-Lee, KWF) take today's prices as correct and let parameters vary with time, so they fit the market curve precisely, which is why practitioners use them to price bonds with embedded options (V6 p.98, p.99).
The differentiators to memorize are mean reversion (CIR and Vasicek yes, Ho-Lee and KWF no), volatility (CIR proportional to $\sqrt{r_t}$, the others constant), and negative rates (possible under Vasicek and Ho-Lee, impossible under CIR and KWF) (V6 p.98, p.99, p.100).
The Gauss+ extension adds short, medium and long factors, with a mean-reverting long rate, a non-random central-bank-controlled short rate, and a hump-shaped volatility curve peaking at medium tenors (V6 p.100).

## Formulas and derivations

**Arbitrage-free value of an option-free bond (spot-rate pricing)** (V6 p.71, p.74)
$$
P_0 = \frac{PMT}{(1+z_1)^1} + \frac{PMT}{(1+z_2)^2} + \cdots + \frac{PMT + 100}{(1+z_N)^N}
$$
^f-06-02-1

- $z_t$: spot (zero-coupon) rate for a cash flow at year $t$, annual compounding; $PMT$: annual coupon per 100 of par.
- Each cash flow is a zero-coupon bond and must be discounted at the zero rate maturing on its own date; any other discounting leaves a stripping or reconstitution profit (V6 p.71, p.73).
- Discounting everything at the single YTM matches $P_0$ only for the benchmark bond that defined that YTM; for other coupons it misprices, too much discounting of early coupons when the curve slopes up (V6 p.74).

> [!tip] Calculator
> Three-year 5% bond on spots 2%, 3.015%, 4.055%: `5 / 1.02 = STO 1`, `5 / 1.03015 x^2 = STO 2` (use `1.03015 y^x 2`), `105 / 1.04055 y^x 3 =`, then `+ RCL 1 + RCL 2 =` gives 102.81.

**Bootstrapping spot rates from the par curve** (V6 p.74)
$$
1 = \frac{\text{Par rate}}{(1+z_1)^1} + \frac{\text{Par rate}}{(1+z_2)^2} + \cdots + \frac{\text{Par rate} + 1}{(1+z_N)^N}
$$
^f-06-02-2

- Par rate: coupon rate of the benchmark bond priced at par, expressed as a decimal; solve maturity by maturity, each equation containing exactly one unknown $z_N$.
- Holds because a par bond's price of 100 must equal the spot-rate value of its cash flows; $z_1$ equals the one-year par rate since a one-year bond has a single cash flow (V6 p.74).
- Isolate the last term: $(1+z_N)^N = (\text{Par rate}+1) / (1 - \sum_{t=1}^{N-1} \text{Par rate}/(1+z_t)^t)$, then take the Nth root.

> [!tip] Calculator
> Two-year spot from par rates 2% and 3%: `0.03 / 1.02 = +/- + 1 = 1/x x 1.03 = sqrt(x) - 1 =` gives 0.03015.

**Lognormal tree node relations** (V6 p.77, p.78)
$$
i_{1,H} = i_{1,L}\,e^{2\sigma}, \qquad i_{t,\,k \text{ nodes above lowest}} = i_{t,\text{lowest}}\,e^{2k\sigma}
$$
^f-06-02-3

- $\sigma$: assumed annual volatility of the one-year rate (decimal); $e \approx 2.7183$; $k$: number of node steps above the lowest rate at time $t$.
- The forward rate is (nearly) the mean of the possible rates, with $i_L$ one standard deviation below and $i_H$ one above, so the ratio of adjacent rates is $e^{2\sigma}$; at Time 2, $i_{2,HH} = i_{2,LL}e^{4\sigma}$ and $i_{2,HL} = i_{2,LL}e^{2\sigma}$ (V6 p.77, p.78).
- The tree recombines because up-down and down-up land on the same middle rate, so nodes grow linearly with time (V6 p.78).
- The middle node at any date approximates the implied one-year forward rate for that date from the spot curve (V6 p.78, p.113).

> [!tip] Calculator
> Given $i_H = 5.8365\%$ and $\sigma = 25\%$: `0.5 +/- 2nd e^x x 5.8365 =` gives 3.5400 ($e^{-0.5} = 0.6065$).

**Standard deviation of the one-year rate under lognormality** (V6 p.79)
$$
\text{StdDev}(\Delta i) = i_0 \sigma
$$
^f-06-02-4

- $i_0$: current level of the one-year rate; $\sigma$: proportional volatility, e.g. 2% rate and 10% volatility give 20 bps.
- Rate moves are proportional to the level of rates, so moves shrink as rates approach zero and negative rates cannot occur (V6 p.79).
- Volatility is estimated either from historical rate data or as implied volatility from interest rate derivative prices (swaptions, caps, floors) (V6 p.79).

**Backward induction value at a node** (V6 p.80)
$$
V_{\text{node}} = \frac{C + \left(0.5 \times V_H + 0.5 \times V_L\right)}{1 + i}
$$
^f-06-02-5

- $C$: coupon paid at the end of the period; $V_H$, $V_L$: bond values at the next-period higher-rate and lower-rate nodes; $i$: the one-year forward rate at this node.
- The weights are exactly 0.5 because the lognormal model assigns equal probability to up and down moves; start at maturity, where value is par plus final coupon, and roll right to left (V6 p.80).
- The same expression is the calibration engine: node rates are adjusted until the Time 0 output equals the benchmark bond's market price (V6 p.83).

> [!tip] Calculator
> Node with $V_H = 97.2222$, $V_L = 99.0566$, $C = 5$, $i = 5\%$: `97.2222 + 99.0566 = / 2 = + 5 = / 1.05 =` gives 98.2280.

**Pathwise valuation** (V6 p.91, p.92)
$$
\text{Paths} = 2^{\,n-1}, \qquad V_0 = \frac{1}{2^{\,n-1}} \sum_{p=1}^{2^{n-1}} \sum_{t=1}^{n} \frac{CF_t}{\prod_{s=0}^{t-1}\left(1 + i_s^{(p)}\right)}
$$
^f-06-02-6

- $n$: number of annual periods to maturity; $i_s^{(p)}$: the one-year forward rate at time $s$ along path $p$ ($i_0$ is common to all paths); $CF_t$: cash flow at year $t$.
- A path fixes one rate per period, so a three-year bond has $2^2 = 4$ paths; path counts per terminal node come from Pascal's Triangle (V6 p.91, p.92).
- Each path's present value discounts every cash flow by the cumulative product of the forward rates up to its date, and the average across paths equals the backward induction value for an option-free bond (V6 p.92, p.93).

**General one-factor interest rate process** (V6 p.97)
$$
dr = \theta_t\,dt + \sigma_t\,dZ
$$
^f-06-02-7

- $\theta_t dt$: drift term, the expected (zero-volatility) rate path; $\sigma_t dZ$: stochastic term with $Z$ a Wiener process, normally distributed.
- One-factor models drive the whole curve off the short rate: all rates move in the same direction but not by the same amount; multi-factor models add factors such as slope (V6 p.97).
- Normal randomness makes negative rates possible unless the model structure prevents them (V6 p.97).

**Cox-Ingersoll-Ross (CIR) model** (V6 p.98)
$$
dr_t = k\left(\theta - r_t\right)dt + \sigma \sqrt{r_t}\,dZ
$$
^f-06-02-8

- $\theta$: long-run mean rate; $k$: speed of mean reversion; drift is zero when $r_t = \theta$.
- Equilibrium model; volatility is proportional to $\sqrt{r_t}$, so the random term shrinks at low rates and rates cannot turn negative (V6 p.98, p.99).

**Vasicek model** (V6 p.99)
$$
dr_t = k\left(\theta - r_t\right)dt + \sigma\,dZ
$$
^f-06-02-9

- Same mean-reverting drift as CIR, but constant volatility; the standard normal stochastic term means negative rates are theoretically possible (V6 p.99).
- Equilibrium model with a single factor, the short rate (V6 p.99, p.101).

**Ho-Lee model** (V6 p.99)
$$
dr_t = \theta_t\,dt + \sigma\,dZ
$$
^f-06-02-10

- First arbitrage-free model; the drift $\theta_t$ is time dependent, one value per time step, which is what lets the model reproduce current market prices exactly (V6 p.99).
- Constant volatility, no mean reversion, negative rates possible; calibrated to market data on a binomial lattice (V6 p.99).

**Kalotay-Williams-Fabozzi (KWF) model** (V6 p.100)
$$
d\ln\left(r_t\right) = \theta_t\,dt + \sigma\,dZ
$$
^f-06-02-11

- Identical structure to Ho-Lee (time-dependent drift, constant volatility, no mean reversion) but applied to the log of the short rate, so the short rate is lognormal and cannot go negative (V6 p.100).
- The lognormal tail changes interest rate option values relative to normal-rate models (V6 p.100).

Model summary for recall (V6 p.100):

| Model | Type | Models | Drift | Volatility | Negative rates |
| --- | --- | --- | --- | --- | --- |
| CIR | Equilibrium | $dr_t$ | Mean reversion, speed $k$ | $\sigma\sqrt{r_t}$ | No |
| Vasicek | Equilibrium | $dr_t$ | Mean reversion, speed $k$ | Constant | Possible |
| Ho-Lee | Arbitrage-free | $dr_t$ | Time dependent | Constant | Possible |
| KWF | Arbitrage-free | $d\ln(r_t)$ | Time dependent | Constant | No |

## Worked examples

**Example 1: arbitrage opportunities** (V6 p.72, p.73)
Which alternative includes an arbitrage: Bond A, a 3% annual 10-year bond yielding 2.5% in New York and selling for 104.376 in Chicago, or Bond B, the same structure yielding 3.2% in Hong Kong SAR and selling for RMB97.220 in Shanghai?
Price each bond off its quoted yield and compare with the second market's price.
Bond A: $\sum_{t=1}^{9} 3/1.025^t + 103/1.025^{10} = 104.376$ (Python confirms 104.376), which equals the Chicago price, so no arbitrage.
Bond B: $\sum_{t=1}^{9} 3/1.032^t + 103/1.032^{10} = 98.311$ (Python confirms 98.311), above the Shanghai price of 97.220.
Buy in Shanghai at 97.220, sell in Hong Kong SAR at 98.311, and collect RMB1.091 per RMB100 of par. ^ex-06-02-1

**Example 2: the arbitrage-free value of an option-free bond** (V6 p.74)
Par rates are 2% (1yr), 3% (2yr), 4% (3yr); a three-year 5% annual coupon bond of equal risk sells at 102.7751 to yield 4%; is that price correct?
Bootstrap the spots with formula 2.
$z_1 = 2\%$ because the one-year par bond has one cash flow.
$1 = 0.03/1.02 + 1.03/(1+z_2)^2$ gives $z_2 = 3.015\%$ (Python: 3.0152%).
$1 = 0.04/1.02 + 0.04/1.03015^2 + 1.04/(1+z_3)^3$ gives $z_3 = 4.055\%$ (Python: 4.0550%).
Arbitrage-free price: $5/1.02 + 5/1.03015^2 + 105/1.04055^3 = 102.8102$ (Python with unrounded spots: 102.8103; the curriculum's 102.8102 reflects spot rounding, an immaterial difference).
The bond is cheap by 0.0351 per 100: discounting the early coupons at the 4% YTM over-discounts them on this upward-sloping curve. ^ex-06-02-2

**Example 3: pricing a bond using a binomial tree** (V6 p.81)
Value a three-year 5% annual-pay bond on a tree with Time 0 rate 2.0%, Time 1 rates 5.0% and 3.0%, Time 2 rates 8.0%, 6.0%, 4.0%.
Time 3 cash flow is 105 at every terminal node.
Time 2 values: $105/1.08 = 97.2222$, $105/1.06 = 99.0566$, $105/1.04 = 100.9615$ (Python confirms all three).
Time 1, upper node: $[5 + 0.5(97.2222 + 99.0566)]/1.05 = 98.2280$.
Time 1, lower node: $[5 + 0.5(99.0566 + 100.9615)]/1.03 = 101.9506$.
Time 0: $[5 + 0.5(98.2280 + 101.9506)]/1.02 = 103.0287$ (Python confirms 98.2280, 101.9506, 103.0287). ^ex-06-02-3

**Text demonstration: calibrating the two-year and three-year segments of the tree** (V6 p.83, p.84, p.85)
The benchmark par curve is 1.00%, 1.20%, 1.25%, 1.40%, 1.80% for years 1 to 5; spots bootstrap to 1.0000%, 1.2012%, 1.2515%, 1.4045%, 1.8194% and implied one-year forwards are 1.0000%, 1.4028%, 1.3521%, 1.8647%, 3.4965% (Python reproduces every rate to the fourth decimal; the four-year spot computes to 1.4044%, a last-digit rounding difference from the printed 1.4045%).
With $\sigma = 15\%$, calibrate Time 1 to the 1.20% two-year par bond.
Trial $i_{1,L} = 1.2500\%$ implies $i_{1,H} = 1.25\% \times e^{0.30} = 1.6873\%$; then $101.20/1.016873 = 99.5208$, $101.20/1.0125 = 99.9506$, and $[1.20 + 0.5(99.5208 + 99.9506)]/1.01 = 99.9363 < 100$, so the trial rates are too high (Python confirms all four numbers).
Iterating (Solver) gives $i_{1,L} = 1.1943\%$ and $i_{1,H} = 1.1943\% \times e^{0.30} = 1.6121\%$; check: $101.20/1.016121 = 99.5944$, $101.20/1.011943 = 100.0056$, $[1.20 + 0.5(99.5944 + 100.0056)]/1.01 = 100.0000$ (Python: brentq solve returns 1.1943%, tree reprices at exactly 100).
The average $(1.6121\% + 1.1943\%)/2 = 1.4032\%$ sits just above the 1.4028% forward because of lognormality.
For Time 2, start the middle rate at the implied forward 1.3521%, set the neighbors as $e^{\pm 0.30}$ multiples, and iterate on the 1.25% three-year bond; the solution is 1.7863%, 1.3233%, 0.9803% (Python solve: 1.7863%, 1.3233%, 0.9803%), and the completed tree's node values are 99.4731, 99.9277, 100.2671 at Time 2 and 99.3488, 100.1513 at Time 1 (Python: 99.4732, 99.9277, 100.2671, 99.3488, 100.1512; the two last-digit differences are rounding).
Repeating with the 1.40% four-year bond fills Time 3 with 2.8338%, 2.0994%, 1.5552%, 1.1521% (Python solve: 2.8338%, 2.0993%, 1.5552%, 1.1521%), which is Exhibit 10.
At $\sigma = 20\%$ the calibrated rates spread out (Time 3 becomes 3.2134%, 2.1540%, 1.4439%, 0.9678%), and at $\sigma = 0.01\%$ they collapse onto the implied forwards (Python recalibration reproduces both trees in Exhibits 15 and 16). ^ex-06-02-4

**Example 4: calibrating a binomial tree to match a specific term structure** (V6 p.86, p.87, p.88)
Par rates 2%, 3%, 4% give spots 2.000%, 3.015%, 4.055% and forwards 2.000%, 4.040%, 6.166%; $\sigma = 15\%$; calibrate the three-period tree.
Time 0: par, spot, and forward rates coincide, so $i_0 = 2.000\%$.
Time 1: trial $i_{1,L} = 3.500\%$ implies $i_{1,H} = 3.5\% \times e^{0.30} = 4.725\%$ and prices the 3% two-year bond at 99.936, too low, so lower the trial (Python: 99.936).
The calibrated rates are 4.646% and 3.442%: $103/1.04646 = 98.427$, $103/1.03442 = 99.573$, $[3 + 0.5(98.427 + 99.573)]/1.02 = 100.000$ (Python confirms).
Time 2: trial middle rate 6.166% (the implied forward) with neighbors $6.166\% \times e^{0.30} = 8.323\%$ and $6.166\%/e^{0.30} = 4.568\%$ prices the 4% three-year bond at 99.898, slightly low (Python: Time 2 values 96.009, 97.960, 99.457; Time 1 values 96.501, 99.291; Time 0 value 99.898).
Lowering the middle rate calibrates Time 2 at 8.167%, 6.050%, 4.482% (Python solve: 8.1671%, 6.0504%, 4.4822%).
Check: $104/1.08167 = 96.148$, $104/1.06050 = 98.067$, $104/1.04482 = 99.538$; $[4 + 0.5(96.148 + 98.067)]/1.04646 = 96.618$; $[4 + 0.5(98.067 + 99.539)]/1.03442 = 99.382$; $[4 + 0.5(96.618 + 99.382)]/1.02 = 100.000$ (Python confirms every node). ^ex-06-02-5

**Text demonstration: spot pricing versus the calibrated tree for a four-year 2% bond** (V6 p.89, p.90)
Spot pricing: $2/1.01 + 2/1.012012^2 + 2/1.012515^3 + 102/1.014044^4 = 102.3254$ (Python: 102.3255 using the printed four-decimal spots; the fifth decimal of the spots explains the digit).
Tree pricing on Exhibit 10: Time 3 values $102/1.028338 = 99.1892$, $102/1.020994 = 99.9026$, $102/1.015552 = 100.4380$, $102/1.011521 = 100.8382$; Time 2 values 99.7638, 100.8360, 101.6417; Time 1 values 100.6769, 102.0204; Time 0 value 102.3254 (Python confirms every node to the fourth decimal).
The lattice reproduces the spot-rate price exactly, which is the point of LOS f: both are arbitrage free, so they cannot disagree for an option-free bond. ^ex-06-02-6

**Example 5: confirming the arbitrage-free value of a bond** (V6 p.90, p.91)
Value the three-year 5% bond of Example 2 on the tree calibrated in Example 4; the price should be 102.8105.
Time 2: $105/1.08167 = 97.0721$, $105/1.06050 = 99.0099$, $105/1.04482 = 100.4958$.
Time 1: $[5 + 0.5(97.0721 + 99.0099)]/1.04646 = 98.4663$ and $[5 + 0.5(99.0099 + 100.4958)]/1.03442 = 101.2672$.
Time 0: $[5 + 0.5(98.4663 + 101.2672)]/1.02 = 102.8105$ (Python confirms all six values).
This matches the spot-rate price 102.8102 of Example 2 up to rounding, confirming the calibration. ^ex-06-02-7

**Text demonstration: pathwise valuation of a three-year zero** (V6 p.92, p.93)
A three-year bond has $2^{3-1} = 4$ paths; on the Exhibit 10 tree the paths and present values for a three-year zero are: HH path $100/(1.01 \times 1.016121 \times 1.017863) = 95.7291$; HL path 96.1665; LH path 96.5636; LL path 96.8916; average 96.3377 (Python confirms all five numbers).
Backward induction on the same tree gives Time 2 values 98.2451, 98.6940, 99.0292, Time 1 values 96.9073, 97.6948, and Time 0 value 96.3377 (Python: 98.2450, 98.6940, 99.0292, 96.9073, 97.6948, 96.3377), the same answer by the other route. ^ex-06-02-8

**Example 6: pathwise valuation based on a binomial interest rate tree** (V6 p.93, p.94)
Value the three-year 5% bond on the Example 4 tree by paths; the target is 102.8105.
The four discount-rate paths are (2.000%, 4.646%, 8.167%), (2.000%, 4.646%, 6.050%), (2.000%, 3.442%, 6.050%), (2.000%, 3.442%, 4.482%).
Path 1: $5/1.02 + 5/(1.02 \times 1.04646) + 105/(1.02 \times 1.04646 \times 1.08167) = 100.5298$.
Path 3: $5/1.02 + 5/(1.02 \times 1.03442) + 105/(1.02 \times 1.03442 \times 1.06050) = 103.4794$.
All four values are 100.5298, 102.3452, 103.4794, 104.8877, and the average is 102.8105 (Python confirms every path and the average), matching backward induction. ^ex-06-02-9

**Example 7: the application of Monte Carlo simulation to bond pricing** (V6 p.95, p.96)
Replace the four tree paths with eight randomly generated paths calibrated to the same par and spot curves, for example (2.000%, 2.500%, 4.548%) through (2.000%, 4.000%, 8.233%).
Discounting the three-year 5% bond's cash flows along each path gives 105.7459, 103.2708, 100.9104, 103.8543, 101.9075, 102.4236, 103.3020, 101.0680, and the average is 102.8103 (Python confirms all eight path values and the average).
Recovering (almost exactly) the arbitrage-free price 102.8105 shows the simulation is calibrated; the value of the method is that these paths, unlike the tree's, can drive path-dependent cash flows such as prepayments (V6 p.96). ^ex-06-02-10

**Example 8: term structure models** (V6 p.100, p.101)
Q1: which model most accurately fits the observed term structure among CIR, Ho-Lee, Vasicek?
B (Ho-Lee): it is the only arbitrage-free model listed, calibrated to current market prices, while the two equilibrium models frequently generate curves inconsistent with market data (V6 p.101).
Q2: the Vasicek model has a single factor, the short rate (B); longer yields follow from the expected short-rate path (V6 p.101).
Q3: the CIR model assumes volatility increases with the level of rates (C); its drift term is identical to Vasicek's and both models mean revert (V6 p.101). ^ex-06-02-11

## Item-set patterns

> [!warning] Trap 1: same bond, three exchanges
> The vignette quotes one bond at three prices and asks for the best arbitrage trade or the arbitrage-free venue.
> Correct: buy at the lowest price, sell at the highest, and identify the arbitrage-free price as the one equal to the spot-rate value of the cash flows (V6 p.113).
> Distractors pair the highest price with a middle price (a real but smaller profit) or label as arbitrage-free the price built by discounting each cash flow at its maturity's par YTM or by discounting everything at the longest spot rate; both reproduce the wrong exchange prices exactly (V6 p.113).

> [!warning] Trap 2: value additivity versus dominance
> Two risk-free assets with different implied one-period returns are shown and the question asks which principle the arbitrage rests on.
> Correct: different discount rates on two risk-free claims is dominance; a package priced away from the sum of its parts is value additivity (V6 p.71, p.72).
> The distractor is the other label, and "no arbitrage available" tempts anyone who compares only prices, not implied returns (V6 p.116).

> [!warning] Trap 3: node relations on a partially blank tree
> The exhibit hides several tree rates and asks which statement about the missing nodes is correct.
> Correct: adjacent rates at a date differ by $e^{2\sigma}$, rates $k$ nodes apart differ by $e^{2k\sigma}$, the middle node approximates the implied one-year forward rate for that date, and no node can be derived from a node at a different date (V6 p.78, p.113).
> Distractors use $e^{\sigma}$ or the wrong $k$ (e.g. $e^{0.4}$ where four steps require $e^{0.8}$) or derive a Time 3 rate from a Time 2 rate (V6 p.113).

> [!warning] Trap 4: backward induction arithmetic
> A tree and a coupon bond are given and one node value or the Time 0 price is requested.
> Correct: value $= [C + 0.5(V_H + V_L)]/(1+i)$ with $i$ the rate at the node being valued, terminal cash flow par plus final coupon (V6 p.80).
> Distractors omit the coupon in the numerator, subtract it, add a coupon at Time 0 (there is none), or discount at the next period's rate; answer choices 6 apart signal the phantom Time 0 coupon (V6 p.115, p.116).

> [!warning] Trap 5: what changing volatility does
> The vignette doubles or halves $\sigma$ and asks what happens to the tree and to bond values.
> Correct: higher volatility spreads the calibrated forward rates apart; near-zero volatility collapses them onto the implied forward curve; and the value of an option-free bond is unchanged because the calibrated tree always reproduces the spot-rate price (V6 p.86, p.114).
> Distractors claim rates converge when volatility rises or that the option-free bond's tree value drifts away from its spot value at high volatility (V6 p.114, p.116).

> [!warning] Trap 6: pathwise mechanics
> A path table is given and one path's present value is requested.
> Correct: discount each cash flow by the cumulative product of the forward rates along that path, starting from the common Time 0 rate; count paths as $2^{n-1}$ (V6 p.91, p.92).
> Distractors discount each cash flow at the single rate for its period (no compounding across the path), drop the final coupon, or add the coupon at Time 0, again producing options that differ by one coupon (V6 p.117).

> [!warning] Trap 7: Monte Carlo claims
> Statements assert that more paths improve accuracy and that the simulated value approaches fundamental value.
> Correct: more paths improve only statistical accuracy; closeness to fundamental value depends on the model and inputs, and the drift adjustment (a constant added to all rates on all paths) is what makes the simulation arbitrage free (V6 p.95, p.117).
> The paired statement about fundamental value is the trap, and "use Monte Carlo" is correct only for path-dependent cash flows such as MBS (V6 p.94, p.95).

> [!warning] Trap 8: equilibrium versus arbitrage-free definitions
> Two statements swap the definitions of equilibrium and arbitrage-free models, or a question mislabels Ho-Lee and KWF.
> Correct: equilibrium models (CIR, Vasicek) build from fundamental economic variables, need few parameters, and rarely match today's curve; arbitrage-free models (Ho-Lee, KWF) take market prices as given, use time-varying parameters, and fit the curve precisely (V6 p.98, p.99).
> Distractors reverse the definitions, reverse which class needs fewer parameters, or attach mean reversion to Ho-Lee or KWF; only CIR and Vasicek mean revert, and only CIR has level-dependent volatility (V6 p.100, p.117).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM02-The-Arbitrage-Free-Valuation-Framework-Practice-Problems]]

## Cross-links

- [[LM01-The-Term-Structure-and-Interest-Rate-Dynamics]]: supplies the raw material this module consumes, the par, spot and forward curves, bootstrapping, and the forward pricing model; the tree's middle nodes converge on LM1's implied forwards as volatility falls.
- [[LM03-Valuation-and-Analysis-of-Bonds-with-Embedded-Options]]: the entire payoff of calibration; LM3 takes the calibrated tree and backward induction built here and adds call and put exercise decisions at each node.
- [[LM04-Credit-Analysis-Models]]: reuses the arbitrage-free framework with credit-risky cash flows, discounting expected exposures and losses on the same benchmark curve machinery.
- [[LM02-Valuation-of-Contingent-Claims]]: the derivatives reading applies the same binomial lattice logic to options, with risk-neutral probabilities replacing this module's fixed 0.5/0.5 weights; recognizing the shared backward induction halves the learning load.

## Self-test

Vignette A for Q1 to Q4: An analyst observes an annual-pay benchmark par curve of 2.00% (1yr), 2.50% (2yr), 3.00% (3yr), all bonds priced at par.
She assumes a lognormal binomial tree with 20% volatility and calibrates it: the Time 1 rates come out at 3.6143% and 2.4227%, and the Time 2 rates at 5.8402%, 3.9148%, 2.6242%.
She is valuing an option-free three-year 4% annual coupon bond.

> [!question] Q1
> The two-year spot rate is closest to:
> A. 2.5000%.
> B. 2.5063%.
> C. 3.0151%.

> [!question] Q2
> The arbitrage-free price of the 4% bond using spot rates is closest to:
> A. 102.7700.
> B. 102.8286.
> C. 102.8467.

> [!question] Q3
> If the calibrated lower Time 1 rate is 2.4227%, the upper rate must be closest to:
> A. 2.9591%.
> B. 3.3918%.
> C. 3.6143%.

> [!question] Q4
> Using backward induction, the value of the 4% bond at the upper Time 1 node is closest to:
> A. 98.2613.
> B. 99.5728.
> C. 102.2344.

Vignette B for Q5 to Q7: Using the same calibrated tree, the analyst values the 4% bond pathwise and checks consistency with her spot-rate price.
She also considers extending the tree one more year for a four-year bond.

> [!question] Q5
> Compared with the spot-rate price, the backward induction value of the option-free 4% bond on the calibrated tree will be:
> A. equal.
> B. higher, because volatility adds option value.
> C. lower, because lognormal rates average above the forwards.

> [!question] Q6
> The number of interest rate paths for the four-year bond is closest to:
> A. 4.
> B. 8.
> C. 16.

> [!question] Q7
> The present value of the 4% bond's cash flows along the path taking the lower rate at Time 1 and the middle rate at Time 2 (2.000%, 2.4227%, 3.9148%) is closest to:
> A. 102.4033.
> B. 103.5490.
> C. 104.7538.

Vignette C for Q8 to Q10: A quantitative team debates methodology for valuing a portfolio of mortgage-backed securities and callable corporates.
One member proposes full pathwise enumeration; another proposes Monte Carlo with 500 paths and notes the raw simulation prices the benchmark bonds above their market values.
A third member wants a rate model in which volatility rises with the rate level, and a fourth wants a model that both fits today's curve exactly and cannot generate negative rates.

> [!question] Q8
> The most appropriate fix for the benchmark mispricing inside the Monte Carlo model is to:
> A. increase the number of simulated paths to improve accuracy.
> B. add a constant drift term to all rates on all paths until benchmarks reprice.
> C. raise the volatility assumption so the paths spread out around the forward curve.

> [!question] Q9
> The models satisfying the third and fourth members' requirements, respectively, are:
> A. CIR; KWF.
> B. Vasicek; Ho-Lee.
> C. CIR; Ho-Lee.

> [!question] Q10
> Monte Carlo rather than backward induction on a tree is required for the MBS portfolio because:
> A. the tree cannot handle monthly time steps.
> B. prepayment cash flows depend on the path rates took, not just their current level.
> C. Monte Carlo values converge to fundamental value as paths are added.

> [!success]- Answer key
> Q1: B.
> Bootstrap: $1 = 0.025/1.02 + 1.025/(1+z_2)^2$ gives $z_2 = 2.5063\%$ (Python: 2.5063%); A is the par rate unadjusted, C is the implied one-year forward rate one year ahead (3.0151%), the classic spot-versus-forward switch.
> Q2: C.
> $z_3 = 3.0204\%$ and $4/1.02 + 4/1.025063^2 + 104/1.030204^3 = 102.8467$ (Python: 102.8467); B discounts everything at the 3% YTM (102.8286), A discounts everything at the three-year spot (102.7700), both under-price the early coupons on this upward-sloping curve.
> Q3: C.
> $i_H = i_L e^{2\sigma} = 2.4227\% \times e^{0.40} = 3.6143\%$ (Python: 3.6143%); A uses $e^{\sigma}$ (2.9591%), B uses a linear $1 + 2\sigma$ multiplier (3.3918%), neither is the lognormal relation.
> Q4: B.
> Time 2 values are $104/1.058402 = 98.2613$, $104/1.039148 = 100.0820$, $104/1.026242 = 101.3406$; upper Time 1 node: $[4 + 0.5(98.2613 + 100.0820)]/1.036143 = 99.5728$ (Python: 99.5728); A is a Time 2 value one period too far right, C is the lower Time 1 node (102.2344), the up/down mix-up.
> Q5: A.
> Both methods are arbitrage free, so the calibrated tree must return the spot-rate price for an option-free bond at any volatility (Python: the tree's Time 0 value is 102.8467, identical to Q2); B smuggles in option value the bond does not have, and C misreads the lognormal averaging, which calibration already absorbs.
> Q6: B.
> Paths $= 2^{n-1} = 2^3 = 8$ for four periods; A is the three-year count, C is $2^4$, forgetting that the Time 0 rate is common to all paths.
> Q7: B.
> $4/1.02 + 4/(1.02 \times 1.024227) + 104/(1.02 \times 1.024227 \times 1.039148) = 103.5490$ (Python: 103.5490); A is the higher-then-middle path (102.4033), C is the lower-lower path (104.7538); the full four-path average is 102.8467, matching Q2, which is the built-in check.
> Q8: B.
> The drift adjustment, a constant added to all short rates on all paths until each benchmark's average present value equals its market price, is what renders the simulation arbitrage free (V6 p.95); A improves precision, not calibration, and C changes dispersion, not the level bias.
> Q9: A.
> Volatility rising with the rate level is CIR's $\sigma\sqrt{r_t}$ term; fitting today's curve exactly while barring negative rates is KWF, whose lognormal short rate stays positive (V6 p.98, p.100); Vasicek does not fit the current curve, and Ho-Lee fits it but allows negative rates.
> Q10: B.
> Prepayments make MBS cash flows path dependent, which a recombining tree cannot represent because it collapses histories into single nodes (V6 p.94, p.95); A is not the binding constraint, and C is false, since more paths buy statistical accuracy only.

## Flashcards

#flashcards/cfa-l2/06-Fixed-Income/lm02

Arbitrage opportunity definition::A transaction involving no cash outlay that results in a riskless profit (V6 p.71).
Law of one price (arbitrage-free bond valuation)::Two goods that are perfect substitutes must sell for the same current price absent transaction costs (V6 p.71).
Value additivity principle::The value of the whole must equal the sum of the values of the parts; violated when a package trades away from its components (V6 p.71).
Dominance principle::A financial asset with a risk-free payoff in the future must have a positive price today, and two risk-free claims must imply the same discount rate (V6 p.72).
Stripping::Dealers separating a coupon bond's individual cash flows and trading them as zero-coupon securities (V6 p.73).
Reconstitution::Dealers recombining zero-coupon securities to reproduce the underlying coupon bond (V6 p.73).
How many zeros make up a five-year 2% semiannual Treasury?::Eleven, ten coupon payments plus one principal payment (V6 p.73).
Arbitrage-free value of an option-free bond::The sum of each cash flow discounted at the spot rate matching that cash flow's own date (V6 p.71, p.74).
Why does YTM discounting misprice on an upward-sloping curve?::It over-discounts early coupons, which spot rates would discount less heavily (V6 p.74).
Benchmark securities::Liquid safe securities (sovereign debt, or the swap curve where sovereigns are illiquid) whose yields anchor other rates and are assumed correctly priced (V6 p.73).
Three conditions the tree's rates must satisfy::An interest rate model, an assumed volatility, and consistency with the current benchmark yield curve (V6 p.75).
Two functions of the interest rate tree in valuation::Generate rate-dependent cash flows and supply the discount rates for present value (V6 p.75).
Two properties guaranteed by the lognormal rate model::Non-negative rates and higher volatility at higher rate levels (V6 p.77).
Relation between the two Time 1 rates in a lognormal tree::{{i_H = i_L e^(2 sigma)}} (V6 p.77).
Multiplier between tree rates k nodes apart at the same date::e^(2k sigma) (V6 p.78).
Recombining tree::Up-down and down-up reach the same middle node, so outcomes grow linearly and computation stays fast (V6 p.78).
What does the middle node at any date approximate?::The implied one-year forward rate for that date from the spot curve (V6 p.78).
Standard deviation of the one-year rate under lognormality::i0 times sigma; 2% rate at 10% volatility is 20 bps (V6 p.79).
Two ways to estimate interest rate volatility::Historical rate volatility, or implied volatility from interest rate derivatives such as swaptions, caps, floors (V6 p.79).
Backward induction node formula::Value equals coupon plus half of VH plus half of VL, all divided by one plus the node's own one-year rate (V6 p.80).
Why are the tree's probabilities exactly 0.5 and 0.5?::The lognormal model places the two outcomes symmetrically around the forward rate with equal probability by construction (V6 p.77, p.80).
Calibration procedure in one sentence::Guess the lowest rate at a date, set neighbors as e^(2 sigma) multiples, discount the benchmark par bond backward, and iterate until the model returns par (V6 p.83).
Why is the average of the calibrated Time 1 rates slightly above the implied forward?::Lognormality spreads the rates multiplicatively around the forward curve (V6 p.84).
What happens to the tree when volatility rises?::Calibrated rates spread farther around the implied forward curve (V6 p.86).
What does the tree become when volatility approaches zero?::The implied forward curve itself (V6 p.86).
Tree value versus spot value for an option-free bond::Always equal on a correctly calibrated tree, at any volatility, because both are arbitrage free (V6 p.89, p.90).
Real payoff of calibrating a tree::A verified tree can price bonds with embedded options, which spot-rate discounting cannot (V6 p.114).
Number of paths through an n-period binomial tree::{{2^(n-1)}} paths, counted with Pascal's Triangle (V6 p.91, p.92).
Pathwise valuation in three steps::List all paths, discount the bond's cash flows along each path with cumulative forward factors, average across paths (V6 p.91).
Path-dependent cash flows::Cash flows that depend on the route rates took to their current level, such as mortgage prepayments (V6 p.94).
Five steps of Monte Carlo bond valuation::Simulate many short-rate paths, build spot rates from them, project cash flows per path, discount each path, average across paths (V6 p.95).
Drift adjustment (drift term) in Monte Carlo::A constant added to all rates on all paths so each benchmark's average present value equals its market price, making the model arbitrage free (V6 p.95).
Effect of adding Monte Carlo paths::Better statistical accuracy only; no closer to fundamental value (V6 p.95, p.117).
How is mean reversion implemented in Monte Carlo?::Upper and lower bounds on the rate process, pulling rates toward the implied forwards (V6 p.95).
General one-factor short-rate process::dr equals theta_t dt plus sigma_t dZ, drift plus a normally distributed stochastic term (V6 p.97).
Equilibrium term structure models::Describe rate dynamics with fundamental economic variables, few parameters, real probabilities; usually do not fit today's curve; CIR and Vasicek (V6 p.98).
Arbitrage-free term structure models::Take market prices of a reference set as correct, use time-varying parameters and risk-neutral probabilities, fit the curve precisely; Ho-Lee and KWF (V6 p.98, p.99).
CIR stochastic term::sigma times the square root of r_t times dZ, so volatility rises with rates and rates cannot go negative (V6 p.98).
Vasicek model traits::Mean-reverting drift k(theta minus r), constant volatility, single short-rate factor, negative rates possible (V6 p.99).
Ho-Lee model traits::First arbitrage-free model, time-dependent drift, constant volatility, no mean reversion, negative rates possible (V6 p.99).
KWF model traits::Ho-Lee structure applied to ln(r), lognormal short rate, no negative rates, no mean reversion, constant volatility (V6 p.100).
Which two models mean revert and which two fit today's curve?::CIR and Vasicek mean revert; Ho-Lee and KWF fit the current term structure (V6 p.98, p.99, p.100).
Gauss+ model::Multi-factor model with short, medium, long rates; long factor mean reverting, short rate non-random (central bank), hump-shaped volatility peaking at medium tenors (V6 p.100).
Micro-problem: iH is 5.8365% and sigma is 25%; find iL::iL equals 5.8365% times e^(-0.5) equals 3.5400%; keystrokes 0.5 +/- 2nd e^x x 5.8365 = (V6 p.117).
Micro-problem: node has VH 100.2742, VL 101.3294, coupon 3, rate 2.8853%; value?::(3 + 0.5 x 100.2742 + 0.5 x 101.3294) / 1.028853 = 100.8908; keystrokes 100.2742 + 101.3294 = / 2 + 3 = / 1.028853 = (V6 p.117).
Micro-problem: three-year path rates 1.5%, 2.8853%, 1.6487%, coupon 3; path PV?::3/1.015 + 3/(1.015 x 1.028853) + 103/(1.015 x 1.028853 x 1.016487) = 102.8607 (V6 p.117).
The trap answer one coupon above the correct bond price signals what error?::A phantom coupon added at Time 0; no coupon is received at valuation date (V6 p.116, p.117).

## Common mistakes

1. Discounting every cash flow at the bond's YTM or at a single spot rate instead of matching each cash flow to its own spot rate; both wrong methods appear as priced distractors on the exchanges in Practice Problem 2 (V6 p.74, p.113).
2. Picking a genuine but smaller arbitrage (second-widest price gap) when the question asks for the best trade (V6 p.113).
3. Labeling a dominance violation as value additivity or vice versa; different implied risk-free returns is dominance, package versus parts is value additivity (V6 p.71, p.72, p.116).
4. Using $e^{\sigma}$ instead of $e^{2\sigma}$ between adjacent nodes, or the wrong multiple for non-adjacent nodes (four steps apart needs $e^{8\sigma}$, not $e^{4\sigma}$) (V6 p.78, p.113).
5. Trying to derive a node from a node at a different date; tree relations hold only within a date (V6 p.113).
6. Forgetting the coupon in the backward induction numerator, subtracting it, or adding a coupon at Time 0; watch for answer options exactly one coupon apart (V6 p.115, p.116, p.117).
7. Discounting a node at the next period's rate instead of the rate at the node being valued (V6 p.80).
8. Believing a higher volatility assumption changes the tree value of an option-free bond; calibration forces the tree back to the spot-rate price at every volatility (V6 p.114, p.117).
9. Forgetting the third tree requirement, the interest rate model, alongside benchmark rates and volatility (V6 p.75, p.117).
10. Pathwise discounting with per-period rates applied independently instead of the cumulative product of forward rates along the path (V6 p.92, p.117).
11. Claiming more Monte Carlo paths move the value toward fundamental value; they only tighten the statistical estimate (V6 p.95, p.117).
12. Swapping the definitions of equilibrium and arbitrage-free models, or their parameter counts; equilibrium uses economic fundamentals and few parameters, arbitrage-free uses market prices and time-varying parameters (V6 p.98, p.117).
13. Assigning mean reversion to Ho-Lee or KWF, level-dependent volatility to anyone but CIR, or negative-rate risk to CIR or KWF (V6 p.98, p.99, p.100).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "06-02" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
