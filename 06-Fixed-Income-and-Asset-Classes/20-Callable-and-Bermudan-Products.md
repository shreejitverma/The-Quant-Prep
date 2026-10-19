---
type: concept
track: [quant-research, quant-risk]
tier: senior
status: solid
prereqs: [term-structure-models-hjm-lgm-lmm, monte-carlo-pricing-and-variance-reduction]
est_hours: 5
sources: [Francis Longstaff and Eduardo Schwartz - Valuing American Options by Simulation - Review of Financial Studies 2001, Leif Andersen and Mark Broadie - Primal-Dual Simulation Algorithm for Pricing Multidimensional American Options - Management Science 2004, Leif Andersen and Jesper Andreasen - Factor Dependence of Bermudan Swaptions - Journal of Financial Economics 2001, Leif Andersen and Vladimir Piterbarg - Interest Rate Modeling volume 3 - 2010, Damiano Brigo and Fabio Mercurio - Interest Rate Models 2nd edition sections 3.11.4 and 13.15]
---

# Callable and Bermudan Products

## TL;DR

- A Bermudan swaption can be exercised on a schedule of dates; a callable bond is a straight bond minus the issuer's Bermudan call, so the holder is short the option and short convexity.
- Pricing is backward induction: at each exercise date take the larger (for the holder) of exercise value and continuation value.
- In one-factor Gaussian models (Hull-White, LGM) use a tree, a PDE or Gaussian convolution; in multi-factor models use Longstaff-Schwartz regression, which is low-biased when the exercise rule is applied to fresh paths, plus a duality upper bound.
- On a 5-year co-terminal example the Bermudan is worth $0.023232$ against $0.017794$ for the best single European; the exercise boundary falls from a $4.74\%$ critical swap rate at year 1 to the $4.00\%$ strike at year 4.
- A model-priced 10-year 5% callable has effective convexity of $-84$ at a 5% curve and $+48$ at a 9% curve: negative convexity is a low-rate phenomenon.

## Learning objectives

- Decompose callable bonds into straight bonds and embedded options and quantify their negative convexity profile.
- Define the Option-Adjusted Spread (OAS) and explain why OAS is model-dependent.
- Formulate the backward induction dynamic programming equation for Bermudan swaptions and read off the exercise boundary.
- Compare co-terminal swaption structures with fixed-tenor Bermudan swaptions.
- Implement the Longstaff-Schwartz (LSMC) regression algorithm and explain its bias.
- Design vega hedging strategies for Bermudan swaptions using co-terminal European swaptions.

## Core concepts

### 1. Callable bonds and negative convexity

A callable bond lets the issuer redeem at a call price (often par) on call dates:
$$P_{\text{callable}} = P_{\text{straight}} - V_{\text{call}}.$$
When rates are high the call is far out of the money and the bond behaves like the straight bond, with positive convexity.
When rates fall the issuer is likely to refinance, the price is held near the call price and the bond behaves like a short bond to the expected call date: duration shortens as rates fall and lengthens as they rise, which is negative convexity.
Measuring it needs a model: yield-to-worst (pricing to the cheaper of maturity and call date) ignores the option's time value, and each branch of it is a convex function of yield.
Effective duration and convexity bump the curve and reprice in the model:
$$D_{\text{eff}} = \frac{P_- - P_+}{2 P_0 \Delta y}, \qquad C_{\text{eff}} = \frac{P_+ + P_- - 2 P_0}{P_0 \Delta y^2}.$$

Holders of negatively convex assets (callable agencies, MBS) who keep their duration constant must buy duration as rates fall and sell it as rates rise, buying after rallies and selling after sell-offs, which loses money in volatile markets: they are short gamma, compensated by a higher spread.

### 2. Option-adjusted spread (OAS)

The Z-spread discounts the promised cash flows as if no one would exercise, so for a callable it mixes credit and liquidity compensation with the value of the option the holder is short.
The OAS is the constant spread added to every short-rate path (or every node) of a calibrated model so that the model price, with optimal exercise inside the model, equals the market price:
$$P_{\text{mkt}} = \mathbb{E}^{\mathbb{Q}}\left[ \sum_i C_i \mathbf{1}_{\{t_i \le \tau\}} e^{-\int_0^{t_i} (r(u) + \text{OAS}) du} \right],$$
with $\tau$ the exercise time and $C_i$ including the call price paid at $\tau$.
OAS is model output: it depends on the term structure model and the volatilities used, so it is comparable only across bonds valued with the same model and inputs, and it also absorbs model error.
The option cost is $\text{Z-spread} - \text{OAS}$ in spread terms.

### 3. Bermudan swaptions

A European swaption has one exercise date; a Bermudan has several, $T_1 < \dots < T_K$.
- **Co-terminal:** every exercise enters a swap ending at the same $T_N$, so the underlying shortens over time; this matches the call option in fixed-rate debt that has been swapped to floating.
- **Fixed-tenor:** each exercise enters a swap of the same length (for example always 5 years).

Dynamic programming with state $x$ and numeraire $N$:
$$\frac{V(T_m, x)}{N(T_m, x)} = \max\left( \frac{E(T_m, x)}{N(T_m, x)},\; \mathbb{E}^N\left[ \frac{V(T_{m+1}, x_{T_{m+1}})}{N(T_{m+1}, x_{T_{m+1}})} \,\Big|\, x_{T_m} = x \right] \right), \qquad V(T_K, x) = \max(E(T_K, x), 0),$$
where $E$ is the value of the swap delivered on exercise.
The exercise region at each date in a one-factor model is one-sided (for a payer: rates above a critical level), so the policy is a sequence of critical swap rates, the exercise boundary.
Bounds: a Bermudan is worth at least its most valuable co-terminal European and at most the sum of them.

### 4. Valuation methods

**Trees.**
A Hull-White trinomial tree (Brigo and Mercurio section 3.3.3) is fitted to the discount curve by forward induction, then rolled back with the max at exercise nodes.
Errors are of order $\Delta t$ and oscillate with the alignment of nodes and the exercise kink; check against Jamshidian's closed form for Europeans.

**PDE and Gaussian convolution in LGM.**
In LGM coordinates ([Term Structure Models](19-Term-Structure-Models-HJM-LGM-LMM.md)) the deflated value $U = V/N$ satisfies $\partial_t U + \frac{1}{2}\sigma(t)^2 \partial_{xx} U = 0$ between exercise dates, with no drift and no discount term.
Between dates the solution is a Gaussian convolution, $U(T_m, x) = \int U(T_{m+1}, y)\, \phi_{\zeta(T_{m+1}) - \zeta(T_m)}(y - x) dy$, which can be computed on a grid by direct quadrature, as in the code, or by Crank-Nicolson; exercise is applied as a max at the dates only.
Grid methods scale badly with dimension (a grid with $M$ points per factor has $M^d$ nodes).

**Longstaff-Schwartz (2001).**
1. Simulate paths of the state to all exercise dates.
2. At the last date set each path's cash flow to its exercise value.
3. Going backwards, on in-the-money paths regress the discounted realized future cash flow of each path on basis functions of today's state (for example powers of the swap rate) to estimate continuation, and exercise where the exercise value exceeds the estimate, replacing that path's cash flow.
4. Average the discounted cash flows.

Regressing realized cash flows rather than fitted values keeps the estimate from accumulating regression error; the rule found is sub-optimal, so applying it on independent paths gives a low-biased price.
The in-sample number (same paths for fitting and pricing) can be biased either way.
Andersen and Broadie (2004) turn any exercise rule into an upper bound by duality (Rogers 2002; Haugh and Kogan 2004), so the gap between the two bounds measures the quality of the rule.

### 5. Hedging and model choice

1. **Delta:** as rates rise a payer Bermudan's expected exercise moves earlier and its delta shifts from long-dated to shorter key rates; risk is reported per bucket.
2. **Vega:** calibrate the model to the co-terminal European swaptions (the diagonal), so each exercise date's marginal distribution matches the market, and hedge vega by those swaptions.
3. **What the diagonal does not pin:** the value of switching between exercise dates depends on how forward swap rates for different dates move relative to each other, through mean reversion in one-factor models and correlation in multi-factor ones; lower correlation between them gives a higher Bermudan value for fixed European vols.
Andersen and Andreasen (Journal of Financial Economics, 2001) found that Bermudan prices change only moderately from one to two factors when both models are well calibrated, supporting recalibrated one-factor models; Longstaff, Santa-Clara and Schwartz (same journal and issue) argued that one-factor exercise rules are sub-optimal in a multi-factor world.

## Worked examples

### Example 1: Bermudan payer by two independent methods
Flat continuously compounded curve $P(0, t) = e^{-0.04 t}$, strike $4.0\%$ annual, exercise at $1, 2, 3, 4$ into a swap ending at $5$; Hull-White $a = 0.03$, $\sigma = 1.2\%$.
The 4% strike is slightly in the money for a payer because the annual par rate of this curve is $e^{0.04} - 1 = 4.08\%$.

| Instrument | Value per unit notional |
| :--- | :--- |
| 1y into 4y, Jamshidian | $0.017568$ |
| 2y into 3y, Jamshidian | $0.017794$ |
| 3y into 2y, Jamshidian | $0.014075$ |
| 4y into 1y, Jamshidian | $0.007912$ |
| 1y into 4y, tree with $\Delta t = 0.05$ | $0.0176082$ ($0.23\%$ above Jamshidian) |
| Bermudan, tree with $\Delta t = 0.05$ | $0.0232815$ |
| 1y into 4y, Gaussian convolution in LGM | $0.017568$ |
| Bermudan, Gaussian convolution in LGM | $0.023232$ |

The convolution reproduces Jamshidian for the European, so it is the reference: the tree overstates the Bermudan by $0.21\%$, consistent with its European error.
The early exercise premium over the 1y into 4y European is $56.6$ bp of notional, $32.2\%$ of the European.
Sanity bounds hold: $0.023232$ exceeds the best European ($0.017794$, 2y into 3y) and is below the sum of the four ($0.057350$).

### Example 2: the exercise boundary
From the convolution, the payer should exercise when the par rate of the remaining swap is above:

| Date | 1 | 2 | 3 | 4 |
| :--- | :--- | :--- | :--- | :--- |
| Critical swap rate | $4.74\%$ | $4.56\%$ | $4.33\%$ | $4.00\%$ |

At the last date the boundary is the strike (exercise whenever in the money).
Earlier, the holder needs a margin above the strike to give up the option to wait, and the margin shrinks as fewer exercise dates remain.

### Example 3: Longstaff-Schwartz, in and out of sample
Simulating LGM exactly at the exercise dates (100,000 paths per set), regressing deflated realized cash flows on $1, S, S^2$ of the swap rate on set 1 (seed 1), then applying the frozen rule to set 2 (seed 2):
the in-sample estimate is about $0.0231$, the out-of-sample estimate about $0.0232$ with a standard error of about $0.0001$, both consistent with the convolution value $0.023232$.
The script asserts that the out-of-sample estimate does not exceed the reference by more than three standard errors, as it cannot for any fixed rule.

### Example 4: negative convexity, yield-to-worst and the model
A 30-year 6% annual bond at an 8% yield trades at $77.48$ with modified duration $11.79$; at 7% it is $87.59$, a $13.0\%$ gain, more than the $11.79\%$ duration estimate because of positive convexity.
At a 4% yield the straight bond would be $134.58$; if it is callable at par in 5 years, the yield-to-worst convention prices it to the call date at $108.90$ with modified duration $4.32$.
That convention says when the call matters but not what the option is worth.

A 10-year 5% annual bond callable at par on each coupon date from year 2 to year 9, priced in the Example 1 model on flat curves (25 bp bumps for duration and convexity):

| Curve | Straight | Callable | Call option | Effective duration | Effective convexity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 3% | $116.63$ | $102.61$ | $14.03$ | $3.10$ | $-80$ |
| 5% | $99.02$ | $94.39$ | $4.63$ | $5.33$ | $-84$ |
| 7% | $84.37$ | $83.28$ | $1.09$ | $6.97$ | $-1$ |
| 9% | $72.16$ | $71.97$ | $0.20$ | $7.48$ | $48$ |

Duration falls from $7.48$ to $3.10$ as rates fall, and convexity is negative wherever the call has meaningful value.
The convolution also reprices the non-callable bond exactly off the curve (asserted), which validates the engine.

### Example 5: one regression step by hand
Four paths at $T_1$ with state $x = (0.02, 0.03, 0.035, 0.05)$ and exercise values $(0.06, 0.03, 0.02, -0.02)$; paths 1 to 3 are in the money, with discounted realized future cash flows $Y = (0.045, 0.038, 0.037)$.
Least squares of $Y$ on $(1, x)$ gives $\hat{V}_{\text{cont}}(x) = 0.0558 - 0.5571 x$, so the fitted continuation values are $0.0446$, $0.0391$ and $0.0363$.
Path 1 exercises ($0.06 > 0.0446$); paths 2 and 3 continue ($0.03 < 0.0391$, $0.02 < 0.0363$) and keep their realized future cash flows.
With only two in-the-money paths a linear fit would interpolate them exactly and every decision would be noise, which is why real runs use many paths and few basis functions.

## Pitfalls

- **Max of Europeans is a lower bound, not a price:** in Example 1 it misses $23.4\%$ of the Bermudan value ($0.017794$ against $0.023232$).
- **Quoting in-sample LSM as a lower bound:** only a rule fitted on one set and priced on another is low-biased; report a duality upper bound when the gap matters.
- **Over-rich regressions:** many basis functions fit noise, producing worse exercise decisions out of sample.
- **Unconverged trees:** tree errors of a few tenths of a percent oscillate with $\Delta t$; check Europeans against closed forms and refine.
- **Comparing OAS across models:** OAS absorbs model differences and errors, so OAS from a one-factor tree and from a two-factor Monte Carlo are not comparable.
- **Ignoring notice periods:** exercise is decided on a notification date before the swap start (for swaptions usually the spot lag; for callable bonds the notice period set in the indenture), so the model's exercise dates must be the notification dates.

## Interview questions

> [!question]- fi-callable-bermudan-definition | What is a Bermudan swaption and how does it differ from American and European swaptions?
> A European swaption has one exercise date and an American can be exercised at any time; a Bermudan can be exercised on a discrete schedule, usually the coupon or reset dates of the underlying swap.
> Its value lies between its most valuable European and the sum of the co-terminal Europeans.

> [!question]- fi-callable-bermudan-negative-convexity | Why do callable bonds exhibit negative convexity at low interest rates?
> The bond is a straight bond minus the issuer's call: as rates fall the call gains value and the price is held near the call price, so duration falls as rates fall.
> In a model-priced 10-year 5% callable, effective convexity is $-84$ at a 5% curve and $+48$ at a 9% curve, where the call is almost worthless.

> [!question]- fi-callable-bermudan-oas-meaning | What is Option-Adjusted Spread (OAS) and what risk does it isolate?
> The constant spread added to every rate path or node of a calibrated model so that the model price, with optimal exercise, equals the market price.
> It removes the option value that a Z-spread mixes in, leaving compensation for credit, liquidity and funding plus model error, so it is comparable only within one model and set of volatility inputs.

> [!question]- fi-callable-bermudan-lsmc-algorithm | Explain the core mechanism of the Longstaff-Schwartz algorithm.
> Simulate forward; then, from the last date backwards, regress each in-the-money path's discounted realized future cash flow on basis functions of the current state to estimate continuation, exercise where exercise value exceeds the estimate, and update that path's cash flow.
> The price is the average discounted cash flow; the regression replaces the conditional expectation that a forward simulation cannot compute directly.

> [!question]- fi-callable-bermudan-continuation-vs-intrinsic | What is the decision rule at each exercise date in dynamic programming for Bermudans?
> Exercise if and only if the exercise value exceeds the continuation value, the risk-neutral expectation (in the numeraire) of the option's value at the next date.
> In a one-factor model this is a threshold on the state: in Example 2 a payer exercises above critical swap rates of $4.74\%$, $4.56\%$, $4.33\%$ and $4.00\%$ at years 1 to 4.

> [!question]- fi-callable-bermudan-coterminal-vs-fixed | Distinguish between a co-terminal and a fixed-tenor Bermudan swaption.
> Co-terminal: every exercise enters a swap ending on the same final date, so the underlying shortens over time, matching swapped callable debt.
> Fixed-tenor: every exercise enters a swap of the same length, for example always 5 years.

> [!question]- fi-callable-bermudan-lsmc-bias | Is the basic Longstaff-Schwartz price estimate a lower bound or an upper bound on the true price?
> Applied to independent paths, it is low-biased: any fixed exercise rule is at best optimal, so its expected payoff cannot exceed the true value.
> The in-sample estimate (same paths for fitting and pricing) has no guaranteed sign, because the rule is fitted to those paths' noise; a duality method (Andersen-Broadie) gives the matching upper bound.

> [!question]- fi-callable-bermudan-vega-hedging | How is a Bermudan swaption typically vega hedged in practice?
> Calibrate the model to the co-terminal European swaptions so each exercise date's marginal distribution is right, then hedge the bucketed vega with those Europeans.
> What remains unhedged is the dependence between exercise dates (mean reversion or correlation), which no set of Europeans pins.

> [!question]- fi-callable-bermudan-correlation-impact | If the correlation between short and long rates increases, does a Bermudan swaption increase or decrease in value?
> It decreases, holding the European vols fixed.
> The Bermudan's extra value is the option to choose the best date; when the forward swap rates for different dates move together the choice is worth less, and in the limit of identical moves the best date is known in advance.

> [!question]- fi-callable-bermudan-notice-period | What is an exercise notice period and how does it affect Bermudan pricing?
> The holder must decide on a notification date before the swap or redemption starts: for swaptions usually the spot lag before the effective date, for callable bonds the notice period in the indenture.
> The model should place the decision on the notification date with the payoff valued from there; using the start date gives the holder information it will not have.

> [!question]- fi-callable-bermudan-exercise-boundary | On a flat 4% curve, why is the critical swap rate for exercising a 4% payer Bermudan above 4% at year 1 but equal to 4% at the last date?
> At the last date there is nothing to wait for, so the payer exercises whenever the swap is in the money.
> Earlier, exercising kills the option to exercise later on better terms, so the holder needs a margin above the strike; in Example 2 the margin falls from 74 bp at year 1 to zero at year 4.

> [!question]- fi-callable-bermudan-two-methods | How would you check a Bermudan price from a tree?
> Price the Europeans on the same engine and compare with Jamshidian, then reprice the Bermudan with an independent method on the same model, for example Gaussian convolution in LGM coordinates or a PDE.
> In Example 1 the convolution matches Jamshidian to six decimals and puts the Bermudan at $0.023232$, $0.21\%$ below the $\Delta t = 0.05$ tree, the same order as the tree's European error.

> [!question]- fi-callable-bermudan-bounds | Give model-free bounds for a co-terminal Bermudan swaption in terms of the co-terminal Europeans.
> At least the most valuable European, because holding the Bermudan and committing to that date replicates it; at most the sum of the Europeans, because exercise can happen only once.
> In Example 1: $0.017794 \le 0.023232 \le 0.057350$.

> [!question]- fi-callable-bermudan-ytw-vs-oas | Why is yield-to-worst not a substitute for an option model on a callable bond?
> It prices to whichever of maturity and call date gives the lower price, which values the call at its intrinsic value and ignores its time value.
> Each branch is a straight bond, so yield-to-worst cannot show the negative convexity that the model shows ($-84$ at a 5% curve in Example 4).

> [!question]- fi-callable-bermudan-factor-debate | Do you need a two-factor model to price Bermudan swaptions?
> Not necessarily: Andersen and Andreasen (2001) found prices change only moderately from one to two factors when both are well calibrated to the co-terminal swaptions, while Longstaff, Santa-Clara and Schwartz (2001) argued one-factor exercise rules are sub-optimal.
> The decisive inputs are calibration to the diagonal and the inter-date dependence (mean reversion or correlation), which should be set deliberately and stress-tested.

## Further reading

- Francis Longstaff and Eduardo Schwartz, *Valuing American Options by Simulation: A Simple Least-Squares Approach*, Review of Financial Studies, 2001.
- Leif Andersen and Mark Broadie, *Primal-Dual Simulation Algorithm for Pricing Multidimensional American Options*, Management Science, 2004.
- Leif Andersen and Jesper Andreasen, *Factor Dependence of Bermudan Swaptions: Fact or Fiction?*, Journal of Financial Economics, 2001.
- Francis Longstaff, Pedro Santa-Clara, and Eduardo Schwartz, *Throwing Away a Billion Dollars: The Cost of Suboptimal Exercise Strategies in the Swaptions Market*, Journal of Financial Economics, 2001.
- Leif Andersen and Vladimir Piterbarg, *Interest Rate Modeling*, Volume 3: Products and Risk Management, Atlantic Financial Press, 2010.
- Damiano Brigo and Fabio Mercurio, *Interest Rate Models - Theory and Practice*, 2nd edition, Springer, 2006, sections 3.11.4 (Bermudan swaptions on a tree) and 13.15 (Bermudan swaptions in the LIBOR market model).
- Mark Broadie and Paul Glasserman, *Pricing American-Style Securities Using Simulation*, Journal of Economic Dynamics and Control, 1997.

## In this repo and SDE-Interview-Prep

- Code: [`code/fi_callable_bermudan.py`](code/fi_callable_bermudan.py) asserts every number here (tree, Gaussian convolution, Jamshidian, exercise boundary, LSM, callable bond table); [`code/rates_models.py`](code/rates_models.py) holds the Hull-White tree and Jamshidian pricers.
- Prereqs: [Term Structure Models: HJM, LGM, and LMM](19-Term-Structure-Models-HJM-LGM-LMM.md), [Short-Rate Models](04-Short-Rate-Models.md).
- Next: [Inflation-Linked Products](21-Inflation-Linked-Products.md).
