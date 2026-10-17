---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: []
est_hours: 3
sources: [Wilmott - Paul Wilmott Introduces Quantitative Finance 2nd ed, Hull - Options Futures and Other Derivatives 11th ed ch 4 and 19, Apostol - Calculus Vol 1 2nd ed ch 7 and 10 and Vol 2 ch 8-9, Breeden and Litzenberger - Prices of State-Contingent Claims Implicit in Option Prices (Journal of Business 1978), Petersen and Pedersen - The Matrix Cookbook (2012), Zhou - A Practical Guide to Quantitative Finance Interviews ch 3]
---

# Calculus and Taylor Expansions

## TL;DR

- $f(x + h) = f(x) + f'(x)h + \tfrac12f''(x)h^2 + \tfrac16f'''(\xi)h^3$ for some $\xi$ between $x$ and $x + h$ (Lagrange remainder); in several variables $f(x + h) \approx f + \nabla f^\top h + \tfrac12h^\top Hh$.
- Delta-gamma-theta-vega P&L is a second-order Taylor expansion of the option price; duration-convexity is the same expansion of a bond price in yield.
- Cross-gammas are the off-diagonal Hessian: a foreign stock held in domestic currency, $V = NSX$, has P&L $NX\Delta S + NS\Delta X + N\Delta S\Delta X$ exactly.
- Leibniz's rule gives $\partial C/\partial K = -e^{-rT}Q(S_T > K)$ and $\partial^2C/\partial K^2 = e^{-rT}f_{S_T}(K)$: option prices across strikes encode the risk-neutral density (Breeden-Litzenberger).
- Gaussian toolkit: $E[e^{aZ}] = e^{a^2/2}$, Stein's lemma $E[Zf(Z)] = E[f'(Z)]$, $E[Z^4] = 3$, $E[Z^+] = 1/\sqrt{2\pi}$, $\Gamma(1/2) = \sqrt\pi$.

## Learning objectives

- Use multivariate Taylor expansions to approximate prices and P&L.
- Differentiate under the integral sign and apply Leibniz's rule.
- Evaluate common integrals (Gaussian, integration by parts) quickly.
- Bound approximation errors with the Lagrange remainder.
- Answer standard limit, series and mental-maths questions with the right expansion.

## Core concepts

### Taylor's theorem and the expansions to know

If $f$ is $n + 1$ times differentiable,

$$
f(x + h) = \sum_{k=0}^n\frac{f^{(k)}(x)}{k!}h^k + \frac{f^{(n+1)}(\xi)}{(n + 1)!}h^{n+1}
$$

for some $\xi$ between $x$ and $x + h$.
The remainder gives error bars, not just "higher-order terms": bound $\lvert f^{(n+1)}\rvert$ on the interval.

| Expansion around 0 | Series | Quant use |
| :--- | :--- | :--- |
| $e^x$ | $1 + x + x^2/2 + x^3/6 + \dots$ | compounding, $E[e^{\sigma Z}]$ |
| $\ln(1 + x)$ | $x - x^2/2 + x^3/3 - \dots$ | log versus simple returns |
| $(1 + x)^\alpha$ | $1 + \alpha x + \frac{\alpha(\alpha - 1)}{2}x^2 + \dots$ | $\sqrt{1 + x} \approx 1 + x/2 - x^2/8$ |
| $1/(1 - x)$ | $1 + x + x^2 + \dots$ for $\lvert x\rvert < 1$ | discount factors, geometric sums |
| $\cos x$, $\sin x$ | $1 - x^2/2$, $x - x^3/6$ | characteristic functions, limits |

Return conventions follow directly:

- a simple return $r$ has log return $\ln(1 + r) = r - r^2/2 + r^3/3 - \dots$, so log returns are smaller and their arithmetic mean understates the simple mean;
- for a GBM the median growth rate is $\mu - \sigma^2/2$ (volatility drag): an 8% drift with 20% vol compounds at a 6% median rate ([SDEs](../04-Stochastic-Calculus/03-Stochastic-Differential-Equations.md));
- a 50% loss followed by a 100% gain is a zero log return: log returns add, simple returns do not.

### Limits and series that interviewers ask

| Fact | Value |
| :--- | :--- |
| $(1 + x/n)^n \to e^x$ | daily compounding of 100% for a year gives $2.7146$ against $e = 2.7183$ |
| $(1 - 1/n)^n \to e^{-1}$ | $0.99^{100} = 0.3660$ against $0.3679$; "probability a given item is never picked in $n$ draws" |
| $\lim_{x \to 0}(1 - \cos x)/x^2$, $\lim(e^x - 1 - x)/x^2$ | $1/2$ and $1/2$ (read the second-order term) |
| $\lim_{x \to 0^+}x^x$, $\lim n^{1/n}$ | 1 and 1 (take logs: $x\ln x \to 0$, $\ln n/n \to 0$) |
| Stirling | $n! \approx \sqrt{2\pi n}(n/e)^ne^{1/(12n)}$ |
| $\sum_{k \ge 1}kx^k = x/(1 - x)^2$ | at $x = 1/2$: 2; and $\sum k^2/2^k = 6$ |
| $\sum 1/k^2 = \pi^2/6 = 1.6449$, $\sum(-1)^{k+1}/k = \ln 2$ | |
| $H_n = \sum_{k \le n}1/k \approx \ln n + \gamma + 1/(2n)$, $\gamma = 0.5772$ | coupon collector, records |

### Multivariate Taylor, gradients and Hessians

For $f: \mathbb{R}^n \to \mathbb{R}$,

$$
f(x + h) = f(x) + \nabla f(x)^\top h + \tfrac12h^\top\nabla^2f(x)\,h + o(\lVert h\rVert^2).
$$

At a critical point ($\nabla f = 0$) the Hessian decides: PD means local minimum, ND local maximum, indefinite a saddle (for example $f = x_1x_2$, Hessian eigenvalues $\pm1$).
Convexity is a global statement about the Hessian being PSD everywhere ([Convex Optimization and KKT](08-Convex-Optimization-and-KKT.md)).

Matrix-calculus identities used in portfolio and likelihood work:

| Function | Gradient |
| :--- | :--- |
| $a^\top x$ | $a$ |
| $x^\top Ax$ | $(A + A^\top)x$, which is $2Ax$ for symmetric $A$ |
| $\tfrac12x^\top Ax - b^\top x$ | $Ax - b$, Hessian $A$ |
| $\lVert Ax - b\rVert^2$ | $2A^\top(Ax - b)$ |
| $\log\det\Sigma$ (in $\Sigma$) | $\Sigma^{-1}$ |
| $\text{tr}(A\Sigma)$ (in $\Sigma$) | $A^\top$ |

### Greeks are Taylor coefficients

For an option $V(S, \sigma, t)$ over a short interval,

$$
\Delta V \approx \underbrace{\Delta\,\delta S}_{\text{delta}} + \underbrace{\tfrac12\Gamma\,\delta S^2}_{\text{gamma}} + \underbrace{\Theta\,\delta t}_{\text{theta}} + \underbrace{\mathcal{V}\,\delta\sigma}_{\text{vega}} + \underbrace{\text{vanna}\,\delta S\,\delta\sigma + \tfrac12\text{volga}\,\delta\sigma^2}_{\text{second-order vol terms}}.
$$

In Black-Scholes the coefficients are tied by the pricing PDE $\Theta + \tfrac12\sigma^2S^2\Gamma + rS\Delta - rV = 0$ ([Black-Scholes Derivation](../04-Stochastic-Calculus/07-Black-Scholes-Derivation.md)), so a delta-hedged long option earns $\tfrac12\Gamma(\delta S^2 - \sigma^2S^2\delta t)$ up to financing terms: gamma pays when realised moves beat implied, theta charges the rent when they do not ([Delta Hedging and Gamma Scalping](../05-Derivatives-and-Volatility/06-Delta-Hedging-and-Gamma-Scalping.md)).

With several underlyings the gamma term is $\tfrac12\delta S^\top\Gamma\,\delta S$ with a full Hessian; the off-diagonal cross-gammas matter for quantos, spread and basket options, and FX-translated positions.
Delta-gamma VaR uses exactly this quadratic form ([VaR and Expected Shortfall](../11-Risk-and-Trading/03-VaR-and-Expected-Shortfall.md)), and risk systems call the residual between full revaluation and the Taylor estimate "unexplained P&L" ([Sensitivities and Revaluation](../11-Risk-and-Trading/12-Sensitivities-and-Revaluation.md)).

Bonds are the same expansion in yield:

$$
\frac{\Delta P}{P} \approx -D_{\text{mod}}\,\Delta y + \tfrac12C\,\Delta y^2,
$$

with modified duration $D_{\text{mod}} = -P'/P$ and convexity $C = P''/P$; positive convexity means the linear estimate always underprices the bond ([Bonds, Duration and Convexity](../06-Fixed-Income-and-Asset-Classes/02-Bonds-Duration-and-Convexity.md)).

### Differentiating under the integral sign

Leibniz's rule:

$$
\frac{d}{d\alpha}\int_{a(\alpha)}^{b(\alpha)}g(x, \alpha)\,dx = g(b, \alpha)b'(\alpha) - g(a, \alpha)a'(\alpha) + \int_{a(\alpha)}^{b(\alpha)}\frac{\partial g}{\partial\alpha}\,dx.
$$

Apply it to $C(K) = e^{-rT}\int_K^\infty(s - K)f(s)\,ds$: the boundary term vanishes because the integrand is 0 at $s = K$, so

$$
\frac{\partial C}{\partial K} = -e^{-rT}\int_K^\infty f(s)\,ds = -e^{-rT}Q(S_T > K), \qquad \frac{\partial^2C}{\partial K^2} = e^{-rT}f(K).
$$

A call spread prices a digital and a butterfly prices the density; a negative butterfly price is an arbitrage, which is why volatility-surface fitters enforce convexity in strike ([Volatility Surface Construction](../05-Derivatives-and-Volatility/08-Volatility-Surface-Construction.md)).

Feynman's trick turns hard integrals into easy ones: $I(a) = \int_0^1\frac{x^a - 1}{\ln x}dx$ has $I'(a) = \int_0^1x^a\,dx = 1/(a + 1)$ and $I(0) = 0$, so $I(a) = \ln(1 + a)$.

### Gaussian integrals and integration by parts

- $\int e^{-x^2/2}dx = \sqrt{2\pi}$; completing the square gives $E[e^{aZ}] = e^{a^2/2}$ and, more generally, $E[e^{aZ}g(Z)] = e^{a^2/2}E[g(Z + a)]$, the change of measure behind Black-Scholes ([Girsanov](../04-Stochastic-Calculus/05-Change-of-Measure-and-Girsanov.md)).
- Moments: $E[Z^{2k}] = (2k - 1)!!$, so $E[Z^2] = 1$, $E[Z^4] = 3$; $E\lvert Z\rvert = \sqrt{2/\pi}$, $E[Z^+] = 1/\sqrt{2\pi}$.
- Stein's lemma, from integration by parts with $\varphi'(z) = -z\varphi(z)$: $E[Zf(Z)] = E[f'(Z)]$.
  Example: $E[Z^2e^Z] = E[Z\cdot Ze^Z] = E[(1 + Z)e^Z] = e^{1/2} + e^{1/2} = 2e^{1/2}$.
- $\Gamma(n + 1) = \int_0^\infty x^ne^{-x}dx = n!$ by repeated integration by parts, and $\Gamma(1/2) = \sqrt\pi$.

## Worked examples

### Delta-gamma against full revaluation

Call with $S = K = 100$, $T = 0.5$, $r = 3\%$, $\sigma = 20\%$: price $6.3710$, $\Delta = 0.5702$, $\Gamma = 0.027772$, vega $0.2777$ per vol point, $\Theta = -7.0738$ per year.

| Move $\delta S$ | Full revaluation | Delta only | Delta-gamma |
| ---: | ---: | ---: | ---: |
| $-10$ | $-4.2667$ | $-5.7016$ | $-4.3130$ |
| $-5$ | $-2.4940$ | $-2.8508$ | $-2.5036$ |
| $-1$ | $-0.5562$ | $-0.5702$ | $-0.5563$ |
| $+1$ | $0.5839$ | $0.5702$ | $0.5840$ |
| $+5$ | $3.1822$ | $2.8508$ | $3.1979$ |
| $+10$ | $6.9479$ | $5.7016$ | $7.0902$ |

"For 1% moves delta-gamma is accurate to about $10^{-4}$; at 10% the error is $0.14$ and comes mostly from speed, $\partial\Gamma/\partial S = -0.000625$, whose term $\text{speed}\cdot\delta S^3/6$ brings the up-move estimate to $6.9860$ and removes about $73\%$ of the gap, leaving $0.038$."
Theta check: one day of decay is $-0.0194$ by full repricing and by $\Theta/365$.
Breakeven move: $\tfrac12\Gamma\delta S^2 = -\Theta/365$ gives $\lvert\delta S\rvert = 1.1814$, slightly above $\sigma S/\sqrt{365} = 1.0468$ because $\Theta$ also contains the financing terms $rS\Delta - rV$; the PDE residual $\Theta + \tfrac12\sigma^2S^2\Gamma + rS\Delta - rC$ is zero to rounding, with gamma rent $\tfrac12\sigma^2S^2\Gamma = 5.5544$ per year.

### A cross-gamma that is exactly second order

"You hold 1000 shares of a euro stock at 50 with EURUSD at 1.10. The stock rises to 55 and EURUSD falls to 1.045. Decompose the USD P&L."
$V = NSX$ is bilinear, so the second-order expansion is exact:
equity delta $NX\delta S = 1000 \times 1.10 \times 5 = 5500$, FX delta $NS\delta X = 1000 \times 50 \times (-0.055) = -2750$, cross-gamma $N\,\delta S\,\delta X = -275$.
Total $2475$, matching $1000 \times 55 \times 1.045 - 55{,}000$.
"The cross term is the quanto effect; an attribution with only first-order terms leaves $-275$ unexplained."

### Duration and convexity of a par bond

10-year 5% annual-coupon bond at a 5% yield: price 100, Macaulay duration $8.1078$, modified duration $7.7217$, convexity $75.00$ (in years squared), DV01 $0.0772$ per 100 face.

| Yield change | Exact price | Duration only | Duration + convexity |
| :--- | ---: | ---: | ---: |
| $+100$ bp | 92.6399 | 92.2783 | 92.6533 |
| $-100$ bp | 108.1109 | 107.7217 | 108.0967 |
| $+200$ bp | 85.9528 | 84.5565 | 86.0565 |

Convexity closes most of the gap; the third-order term (negative for rising yields) explains the remaining overestimate at $+200$ bp.

### Limits, Stirling and the harmonic numbers

- $(1 - 1/100)^{100} = 0.3660$ against $e^{-1} = 0.3679$.
- $10! = 3{,}628{,}800$; Stirling gives $3{,}598{,}695.6$ (ratio $0.9917$), and with the $e^{1/(12n)}$ correction $3{,}628{,}810.1$.
- $H_{100} = 5.1874$ against $\ln 100 + \gamma = 5.1824$, and adding $1/(2n)$ gives $5.1874$.
- $\sqrt{1.1} = 1.048809$ against $1 + 0.05 - 0.00125 = 1.04875$; $\ln 1.1 = 0.09531$ against $0.095$ from two terms and $0.09533$ from three.

### A Lagrange error bar

"Approximate $e^{0.1}$ by $1 + x + x^2/2$ and bound the error."
The approximation is $1.105$; the remainder is $e^\xi(0.1)^3/6$ with $0 < \xi < 0.1$, so it lies between $0.1^3/6 = 0.00016667$ and $1.106 \times 0.1^3/6 = 0.00018433$.
The actual error is $0.00017092$, inside the bracket.

### Strike derivatives and the implied density

With $S = 100$, $T = 0.5$, $r = 3\%$, $\sigma = 20\%$: a finite difference of the call price in strike at $K = 100$ gives $-0.5064 = -e^{-rT}N(d_2)$, minus the discounted probability of finishing in the money.
Differencing twice on a strike grid and integrating $e^{rT}C_{KK}$ recovers total probability 1 and mean $101.5113 = Se^{rT}$: the risk-neutral density and the forward are both in the call prices.

### Feynman's trick and Gaussian integrals

- $\int_0^1\frac{x^2 - 1}{\ln x}dx = \ln 3 = 1.0986$, confirmed by quadrature.
- $E[Z^2e^Z] = 2e^{1/2} = 3.2974$ by Stein's lemma; $E[Z\sin Z] = E[\cos Z] = e^{-1/2} = 0.6065$.
- $E[Z^+] = 0.3989$ and $E\lvert Z\rvert = 0.7979$, the constants behind ATM option approximations and mean absolute deviation.

## Pitfalls

- Treating delta-gamma as exact for large moves or long horizons; speed, vanna and volga terms grow, and path-dependent or barrier products can have discontinuous Greeks.
- Forgetting cross-gammas in multi-asset or FX-translated books; first-order attribution leaves the product term unexplained.
- Mixing return conventions: averaging log returns and calling it the mean simple return, or compounding simple returns additively.
- Quoting duration-only price changes for large rate moves; convexity is always in the holder's favour for an option-free bond, and the linear estimate is biased low.
- Dropping the boundary terms in Leibniz's rule when the limits depend on the parameter (they vanish for a call only because the payoff is zero at the strike).
- Using finite differences with a step that is too small; rounding error grows like $u/h$ for a first derivative and $u/h^2$ for a second, so balance it against truncation error.
- Reading the Taylor remainder as "small": it is $f^{(n+1)}(\xi)h^{n+1}/(n + 1)!$, and a large derivative (gamma near expiry at the strike) makes it large.

## Interview questions

> [!question]- la-calc-lagrange-remainder | Approximate $e^{0.1}$ to second order and bound the error.
> $1.105$; the Lagrange remainder $e^\xi(0.1)^3/6$ with $0 < \xi < 0.1$ lies in $[0.000167, 0.000184]$, and the actual error is $0.000171$.

> [!question]- la-calc-log-vs-simple | A stock returns 10%. What is the log return to three terms, and why does it matter?
> $\ln 1.1 = 0.1 - 0.005 + 0.000333 = 0.09533$ (exact $0.09531$). Log returns add over time and are smaller than simple returns by about $r^2/2$, so mixing the two biases means and Sharpe ratios.

> [!question]- la-calc-vol-drag | Drift 8%, volatility 20%: what is the median compound growth rate of a GBM?
> $\mu - \sigma^2/2 = 6\%$. Itô (or the second-order Taylor term of $\ln S$) subtracts half the variance; the mean grows at 8% but the typical path at 6%.

> [!question]- la-calc-delta-gamma | Write the delta-gamma-theta approximation of option P&L and say when it fails.
> $\delta V \approx \Delta\delta S + \tfrac12\Gamma\delta S^2 + \Theta\delta t$ (plus vega $\delta\sigma$). It fails for large moves (speed and higher terms), near expiry at the strike (gamma explodes), and for products with discontinuous payoffs such as barriers and digitals.

> [!question]- la-calc-delta-gamma-numbers | ATM 6-month call, $S = 100$, vol 20%, $r = 3\%$, $\Delta = 0.5702$, $\Gamma = 0.02777$. Estimate the P&L for a $+5$ move.
> $0.5702 \times 5 + \tfrac12 \times 0.02777 \times 25 = 2.851 + 0.347 = 3.198$ (more precisely $3.1979$); full repricing gives $3.1822$, the difference being mostly the negative speed term.

> [!question]- la-calc-gamma-theta | How are theta and gamma linked in Black-Scholes, and what does it mean for a delta-hedged option?
> $\Theta + \tfrac12\sigma^2S^2\Gamma + rS\Delta - rV = 0$. Ignoring financing, a delta-hedged long option earns $\tfrac12\Gamma(\delta S^2 - \sigma^2S^2\delta t)$: it makes money when realised variance beats implied and pays theta otherwise.

> [!question]- la-calc-breakeven-move | One-day breakeven move for the 6-month ATM call with $\Gamma = 0.02777$ and $\Theta = -7.07$ per year?
> Solve $\tfrac12\Gamma\delta S^2 = 7.07/365$: $\delta S = 1.18$. It is a little above $\sigma S/\sqrt{365} = 1.05$ because Black-Scholes theta also includes the financing terms.

> [!question]- la-calc-cross-gamma | 1000 shares of a euro stock at 50, EURUSD 1.10. Stock goes to 55, EURUSD to 1.045. P&L and its decomposition?
> $+2475$ USD: equity delta $+5500$, FX delta $-2750$, cross-gamma $N\delta S\delta X = -275$. $V = NSX$ is bilinear, so the second-order expansion is exact.

> [!question]- la-calc-duration-convexity | A 10-year 5% par bond has modified duration 7.72 and convexity 75. Estimate the price after $+100$ bp.
> $100(1 - 0.0772 + \tfrac12 \times 75 \times 0.0001) = 92.65$; exact $92.64$. Duration alone gives $92.28$, too low by convexity.

> [!question]- la-calc-hessian-classify | Classify the critical point of $f(x, y) = xy$ at the origin.
> Saddle: the Hessian $\begin{pmatrix} 0 & 1 \\ 1 & 0\end{pmatrix}$ has eigenvalues $+1$ and $-1$, so $f$ rises along $(1, 1)$ and falls along $(1, -1)$.

> [!question]- la-calc-matrix-gradients | Gradients of $w^\top\Sigma w$, $\mu^\top w$ and $\log\det\Sigma$?
> $2\Sigma w$ (for symmetric $\Sigma$), $\mu$, and $\Sigma^{-1}$ (with respect to $\Sigma$). These give the first-order conditions of mean-variance and the Gaussian maximum-likelihood covariance.

> [!question]- la-calc-leibniz-call | Differentiate a call price with respect to strike.
> $\partial C/\partial K = -e^{-rT}Q(S_T > K)$ by Leibniz (the boundary term vanishes at $s = K$). In Black-Scholes it is $-e^{-rT}N(d_2)$; at the money with 6 months, 20% vol and 3% rates, $-0.5064$.

> [!question]- la-calc-breeden-litzenberger | How do you get the risk-neutral density from option prices?
> $f(K) = e^{rT}\partial^2C/\partial K^2$: the price of a tight butterfly divided by the squared strike spacing, grossed up by the discount factor. Negative butterflies mean the quoted surface admits arbitrage.

> [!question]- la-calc-feynman | Evaluate $\int_0^1\frac{x^2 - 1}{\ln x}dx$.
> $\ln 3$. Let $I(a) = \int_0^1(x^a - 1)/\ln x\,dx$; then $I'(a) = \int_0^1x^a\,dx = 1/(a + 1)$ and $I(0) = 0$, so $I(a) = \ln(1 + a)$.

> [!question]- la-calc-gaussian-mgf | Compute $E[e^{aZ}]$ for standard normal $Z$, and $E[S_T]$ for lognormal $S_T = S_0e^{(r - \sigma^2/2)T + \sigma\sqrt{T}Z}$.
> $e^{a^2/2}$ by completing the square. So $E[S_T] = S_0e^{(r - \sigma^2/2)T}e^{\sigma^2T/2} = S_0e^{rT}$.

> [!question]- la-calc-stein | State Stein's lemma and use it to compute $E[Z^2e^Z]$.
> $E[Zf(Z)] = E[f'(Z)]$ for standard normal $Z$ (integration by parts, $\varphi' = -z\varphi$). With $f(z) = ze^z$: $E[(1 + Z)e^Z] = e^{1/2} + e^{1/2} = 2e^{1/2} \approx 3.297$.

> [!question]- la-calc-limit-e | What is $(1 - 1/n)^n$ for large $n$, and where does it show up?
> $\to e^{-1} \approx 0.368$ (at $n = 100$, $0.366$). It is the chance a given item is never chosen in $n$ uniform draws from $n$, for example the out-of-bag fraction of a bootstrap sample.

> [!question]- la-calc-stirling | Approximate $10!$ with Stirling and say how good it is.
> $\sqrt{20\pi}(10/e)^{10} \approx 3{,}598{,}696$ against $3{,}628{,}800$, 0.83% low; multiplying by $e^{1/120}$ gives $3{,}628{,}810$, off by about 10.

> [!question]- la-calc-harmonic | Approximate $H_{100} = \sum_{k=1}^{100}1/k$.
> $\ln 100 + \gamma + 1/200 \approx 5.1874$, matching the exact value to four decimals; without the $1/(2n)$ term the estimate is $5.1824$.

> [!question]- la-calc-series-kx | Evaluate $\sum_{k \ge 1}k/2^k$.
> 2. Differentiate $\sum x^k = 1/(1 - x)$ to get $\sum kx^{k-1} = 1/(1 - x)^2$, multiply by $x$, and set $x = 1/2$: $(1/2)/(1/4) = 2$. It is the mean of a Geometric(1/2) number of trials.

## In this repo and SDE-Interview-Prep

- Code: [calculus_taylor.py](code/calculus_taylor.py) computes and asserts every number above (Greeks and the delta-gamma table, the quanto decomposition, bond duration and convexity, limits and series, the Breeden-Litzenberger and Gaussian quadratures).
- SDE bridge: [Black-Scholes](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/05-Quantitative-Finance/01-Mathematics/Option-Pricing/black_scholes.py) and [Greeks](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/05-Quantitative-Finance/01-Mathematics/Option-Pricing/greeks.py) implementations.
- Related: [The Greeks](../05-Derivatives-and-Volatility/05-The-Greeks.md), [PnL Attribution and Greek Risk](../11-Risk-and-Trading/06-PnL-Attribution-and-Greek-Risk.md), [Mental Math](../13-Interview-Playbook/02-Mental-Math.md).

## Further reading

- Paul Wilmott, *Paul Wilmott Introduces Quantitative Finance*, 2nd edition, the chapters on the Black-Scholes formulae and the Greeks.
- John Hull, *Options, Futures, and Other Derivatives*, 11th edition, chapters 4 (duration and convexity) and 19 (the Greek letters).
- Tom Apostol, *Calculus*, Volume 1, 2nd edition, chapters 7 and 10 (Taylor polynomials, series), and Volume 2, chapters 8-9 (multivariable differential calculus).
- Douglas Breeden and Robert Litzenberger, "Prices of State-Contingent Claims Implicit in Option Prices", *Journal of Business* 51(4) (1978).
- Kaare Brandt Petersen and Michael Syskind Pedersen, *The Matrix Cookbook* (2012 version), section 2 (derivatives).
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 3 (calculus and linear algebra).
