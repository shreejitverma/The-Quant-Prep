---
type: concept
track: [quant-research, quant-risk]
tier: senior
status: solid
prereqs: [short-rate-models, forwards-futures-and-carry]
est_hours: 4
sources: [Brigo and Mercurio - Interest Rate Models chapter 13, Patrick Hagan - Convexity Conundrums Pricing CMS Swaps Caps and Floors]
---

# Convexity Adjustments

## TL;DR

A convexity adjustment is a correction added to a forward rate or expected cash flow when its payment timing, payment frequency, settlement currency, or margining mechanism differs from the natural martingale measure of the underlying rate.
Because daily variation margining in futures contracts yields positive covariance with financing rates, interest rate futures trade at higher rates than forward contracts: $R_{\text{fut}} - R_{\text{fwd}} \approx \frac{1}{2}\sigma^2 T_1 T_2$.
Constant Maturity Swap (CMS) products pay long-term swap rates under a single-period discount measure, requiring a change of numeraire from the swap annuity to a zero-coupon bond that induces a large positive adjustment.
Pricing CMS products requires static replication across the entire swaption volatility smile to capture tail convexity.
Quanto products and in-arrears fixings similarly introduce cross-asset and payment-lag drift adjustments proportional to volatility and correlation.

## Learning objectives

- Explain the change-of-numeraire mechanism that generates convexity adjustments via Radon-Nikodym derivatives.
- Derive the Ho-Lee / Hull-White convexity adjustment between interest rate futures and forward rate agreements (FRAs).
- Formulate the CMS convexity adjustment via annuity duration approximations and Carr-Madan static swaption replication.
- Calculate the in-arrears rate adjustment for floating rates paid at non-standard settlement dates.
- Evaluate the quanto adjustment for domestic payoffs linked to foreign interest rates.
- Identify how improper convexity handling distorts curve bootstrapping and relative value trading.

## Core concepts

### 1. Mathematical Foundation: Change of Numeraire

In modern derivative pricing, a financial asset $S(t)$ is a martingale only when denominated in terms of an appropriate numeraire asset $N(t)$.
Let $\mathbb{Q}^N$ be the pricing measure associated with numeraire $N(t)$, and let $\mathbb{Q}^M$ be the measure associated with an alternative numeraire $M(t)$.
By the Radon-Nikodym theorem, the change-of-measure density is:
$$\frac{d\mathbb{Q}^M}{d\mathbb{Q}^N}\Bigg|_t = \frac{M(t) / M(0)}{N(t) / N(0)}$$

Suppose we wish to evaluate the expected value of an underlying rate $X(T)$ under measure $\mathbb{Q}^M$, where $X(t)$ is known to be a martingale under $\mathbb{Q}^N$ ($\mathbb{E}^N[X(T)] = X(0)$).
By the abstract Bayes formula:
$$\mathbb{E}^M[X(T)] = \frac{\mathbb{E}^N\left[ X(T) \frac{M(T)}{N(T)} \right]}{\mathbb{E}^N\left[ \frac{M(T)}{N(T)} \right]} = \mathbb{E}^N[X(T)] + \frac{\text{Cov}^N\left( X(T), \frac{M(T)}{N(T)} \right)}{\mathbb{E}^N\left[ \frac{M(T)}{N(T)} \right]}$$
The difference $\mathbb{E}^M[X(T)] - \mathbb{E}^N[X(T)]$ is the **convexity adjustment**.
Whenever the payoff weight or numeraire ratio $\frac{M(T)}{N(T)}$ is correlated with the underlying rate $X(T)$, the expectation under the payment measure deviates from the forward rate.

### 2. Futures vs Forward Rate Adjustment

A forward rate agreement (FRA) is an over-the-counter forward contract settled once at maturity without interim cash flows.
Under the forward measure $\mathbb{Q}^{T_2}$ with numeraire $P(t, T_2)$, the forward rate $F(t; T_1, T_2)$ is a martingale:
$$\mathbb{E}^{T_2}[F(T_1; T_1, T_2)] = F(0; T_1, T_2)$$

An interest rate futures contract (such as 3-Month SOFR futures or historical Eurodollar futures) is an exchange-traded contract settled daily through variation margin.
Variation margin is received or paid in cash each business day and immediately invested or borrowed at the prevailing overnight interest rate $r(t)$.
1. When interest rates rise, a long futures position gains cash, which is immediately reinvested at higher overnight rates.
2. When interest rates fall, a long futures position loses cash, which is financed by borrowing at lower overnight rates.

This positive correlation between mark-to-market profits and financing rates makes the futures contract strictly more advantageous to a long holder than a static forward contract.
In equilibrium, arbitrageurs short futures and buy forwards, forcing the futures rate $R_{\text{fut}}$ to trade above the forward rate $R_{\text{fwd}}$:
$$R_{\text{fut}} > R_{\text{fwd}}$$

Under the 1-factor Hull-White Gaussian model with short-rate volatility $\sigma$ and mean reversion $a$, the theoretical difference between continuously compounded rates is (Hull, *Options, Futures, and Other Derivatives*):
$$\text{Adj}_{\text{fut}} = R_{\text{fut}}(0) - R_{\text{fwd}}(0) = \frac{B(T_1, T_2)}{T_2 - T_1}\left[B(T_1, T_2)\left(1 - e^{-2 a T_1}\right) + 2 a B(0, T_1)^2\right]\frac{\sigma^2}{4 a}$$
with $B(t, T) = \frac{1 - e^{-a(T - t)}}{a}$.
In the limit as mean reversion $a \to 0$ (Ho-Lee dynamics), $B(t, T) \to T - t$ and:
$$\text{Adj}_{\text{fut}} = \frac{1}{2} \sigma^2 T_1 T_2$$
where $T_1$ is the futures contract expiration and $T_2$ is the maturity of the underlying reference rate.
The adjustment grows with the square of maturity: for a 3-month rate with a 5-year expiry ($T_1 = 5$, $T_2 = 5.25$) and $\sigma = 1.2\%$, Ho-Lee gives $\frac{1}{2} \times 0.012^2 \times 5 \times 5.25 = 18.9$ bps, and Hull-White with $a = 0.03$ gives 16.2 bps.
Failure to subtract this adjustment when bootstrapping yield curves causes significant overestimation of long-term zero rates.

### 3. Constant Maturity Swap (CMS) Adjustments

A Constant Maturity Swap (CMS) is an interest rate swap where one leg pays a fixed or floating rate, and the other leg pays a long-term swap rate (such as the 10-year or 30-year swap rate $S_{10y}(t)$) reset periodically.
Consider a single CMS payment of the swap rate fixing at $T_1$, paid at $T_1$ (a payment delay adds a further timing adjustment; see Pitfalls).
Under the zero-coupon bond measure $\mathbb{Q}^{T_1}$ associated with payment numeraire $P(t, T_1)$, the expected CMS payoff is:
$$\mathbb{E}^{T_1}[S(T_1)]$$

However, the swap rate $S(t)$ is naturally a martingale only under the **annuity measure** $\mathbb{Q}^A$, where the numeraire is the multi-year swap annuity:
$$A(t) = \sum_{i=1}^n \tau_i P(t, T_i)$$
The ratio of numeraires between the payment measure $\mathbb{Q}^{T_1}$ and the annuity measure $\mathbb{Q}^A$ is:
$$\frac{P(T_1, T_1)}{A(T_1)} = \frac{1}{A(T_1)}$$

Because the swap annuity $A(S)$ is an inverse, decreasing function of the swap rate $S$ ($A'(S) < 0$), the ratio $\frac{1}{A(S)}$ is an increasing function of $S$.
When the swap rate $S(T_1)$ increases, the annuity $A(T_1)$ shrinks, which amplifies the relative weight $\frac{1}{A(T_1)}$.
This positive covariance induces a substantial positive convexity adjustment:
$$\mathbb{E}^{T_1}[S(T_1)] > S(0)$$

#### Linear Duration Approximation
Under a lognormal model with swap rate volatility $\sigma_S$, Taylor expanding $\frac{1}{A(S)}$ around forward swap rate $S(0)$ yields:
$$\text{Adj}_{\text{CMS}} = \mathbb{E}^{T_1}[S(T_1)] - S(0) \approx S(0)^2 \sigma_S^2 T_1 \left( -\frac{A'(S(0))}{A(S(0))} \right)$$
where $-\frac{A'(S(0))}{A(S(0))}$ is the modified duration of the underlying swap annuity.

#### Static Replication via Swaptions (Hagan 2003)
In practice, the linear approximation underestimates tail risk because CMS payoffs depend on extreme rates.
Patrick Hagan (2003) demonstrated that any European CMS payoff $g(S)$ can be statically replicated using a portfolio of European payer and receiver swaptions using the Carr-Madan spanning identity.
Write the payoff's price under the annuity measure, $V_{\text{CMS}}(0) = P(0, T_1)\,\mathbb{E}^{T_1}[g(S(T_1))] = A(0)\,\mathbb{E}^A[h(S(T_1))]$ with $h(s) = \frac{g(s)}{A(s)}$, where $A(s)$ maps the swap rate to the annuity (for example the flat-yield annuity of the Linear Duration Approximation above).
Spanning $h$ around $S(0)$ and using $A(0)\,\mathbb{E}^A[(S - K)^+] = \text{Payer}(K)$, $A(0)\,\mathbb{E}^A[(K - S)^+] = \text{Receiver}(K)$ and $\mathbb{E}^A[S(T_1)] = S(0)$:
$$V_{\text{CMS}}(0) = A(0)\,h(S(0)) + \int_0^{S(0)} h''(K) \text{Receiver}(K) dK + \int_{S(0)}^\infty h''(K) \text{Payer}(K) dK$$
Because the replication spans strikes $K \in (0, \infty)$, pricing CMS derivatives accurately requires integrating across the entire market swaption volatility smile (typically calibrated via SABR).

### 4. In-Arrears Rate Adjustments

In standard interest rate contracts, a forward rate $L(T_1, T_2)$ fixing at $T_1$ pays in arrears at $T_2 = T_1 + \tau$.
The natural payment measure is $\mathbb{Q}^{T_2}$, where $\mathbb{E}^{T_2}[L(T_1)] = L(0)$.

In an **in-arrears swap**, the floating coupon fixing at $T_1$ pays immediately at $T_1$ (in-advance payment of an in-arrears fixing) or is paid at $T_2$ without the standard discounting factor $(1 + \tau L(T_1))^{-1}$.
Under the payment measure $\mathbb{Q}^{T_1}$, the change of numeraire from $P(t, T_2)$ to $P(t, T_1)$ introduces an adjustment:
$$\frac{P(T_1, T_1)}{P(T_1, T_2)} = 1 + \tau L(T_1)$$
The expected rate is:
$$\mathbb{E}^{T_1}[L(T_1)] = L(0) + \frac{\text{Cov}^{T_2}(L(T_1), 1 + \tau L(T_1))}{\mathbb{E}^{T_2}[P(T_1, T_1) / P(T_1, T_2)]} = L(0) + \frac{\tau \text{Var}^{T_2}(L(T_1))}{1 + \tau L(0)}$$
Under a lognormal model with volatility $\sigma_L$, $\text{Var}^{T_2}(L(T_1)) = L(0)^2 (e^{\sigma_L^2 T_1} - 1) \approx L(0)^2 \sigma_L^2 T_1$, so to first order:
$$\text{Adj}_{\text{arrears}} = \frac{\tau L(0)^2 \sigma_L^2 T_1}{1 + \tau L(0)}$$
Because the adjustment is strictly positive, an in-arrears floating leg always has a higher forward value than a standard floating leg.

### 5. Quanto Convexity Adjustments

A **quanto derivative** has a payoff determined by an underlying asset or rate in a foreign currency, but cash-settled in a domestic currency at a fixed exchange rate (e.g., paying the 3-month EURIBOR rate in USD with 1 EUR = 1 USD notional).

Let $S_f(t)$ be the foreign rate, and let $X(t)$ be the exchange rate (domestic currency per unit of foreign currency).
Under the foreign pricing measure $\mathbb{Q}^f$, $S_f(t)$ follows a lognormal process with relative drift $\mu_f$ ($\mu_f = 0$ for a forward rate under its own foreign forward measure).
However, domestic pricing must be conducted under the domestic risk-neutral measure $\mathbb{Q}^d$.
The change of measure from foreign to domestic involves the stochastic exchange rate:
$$\frac{d\mathbb{Q}^d}{d\mathbb{Q}^f}\Bigg|_t = \frac{X(t) B_f(t)}{X(0) B_d(t)}$$
Applying Girsanov's theorem, the relative drift of the foreign rate under the domestic measure acquires an adjustment:
$$\frac{dS_f(t)}{S_f(t)} = \left(\mu_f - \rho_{S, X} \sigma_S \sigma_X\right) dt + \sigma_S dW^d(t)$$
where:
- $\sigma_S$ is the foreign rate's lognormal volatility.
- $\sigma_X$ is the FX volatility.
- $\rho_{S, X}$ is the correlation between the foreign rate and the exchange rate.

With constant parameters, $\mathbb{E}^d[S_f(T)] = \mathbb{E}^f[S_f(T)] e^{-\rho_{S, X} \sigma_S \sigma_X T}$, so for a forward rate ($\mu_f = 0$) the quanto adjustment is:
$$\text{Adj}_{\text{quanto}} = S_f(0)\left(e^{-\rho_{S, X} \sigma_S \sigma_X T} - 1\right) \approx -\rho_{S, X} \sigma_S \sigma_X S_f(0) T$$
If a foreign interest rate is positively correlated with the foreign currency strengthening against the dollar ($\rho > 0$), the expected foreign rate under the domestic USD measure is depressed by the covariance term.

## Worked examples

### Example 1: Eurodollar / SOFR Futures Convexity Adjustment
Calculate the convexity adjustment between a 2-year futures contract on a 3-month rate ($T_1 = 2.0\text{ years}$, $T_2 = 2.25\text{ years}$) assuming short-rate volatility $\sigma = 1.20\%$ (120 bps) under Ho-Lee dynamics ($a \to 0$).

Using the Ho-Lee formula:
$$\text{Adj}_{\text{fut}} = \frac{1}{2} \sigma^2 T_1 T_2$$
Substitute the values:
$$\text{Adj}_{\text{fut}} = \frac{1}{2} \times (0.012)^2 \times 2.0 \times 2.25$$
$$\sigma^2 = 0.000144$$
$$\text{Adj}_{\text{fut}} = 0.5 \times 0.000144 \times 4.5 = 0.000324$$
$$\text{Adj}_{\text{fut}} = 3.24 \text{ bps}$$
Our reference code [`code/fi_convexity.py`](code/fi_convexity.py) and [`code/rates_models.py`](code/rates_models.py) confirm:
`futures_rate_convexity_adjustment(0.012, 2.0, 2.25) == 0.000324` ($3.24\text{ bps}$).
If the quoted futures rate is $4.5000\%$, the fair forward rate is $4.5000\% - 0.0324\% = 4.4676\%$.

### Example 2: 10-Year CMS Fixing in 5 Years
Calculate the CMS convexity adjustment for a 10-year swap rate fixing in 5 years ($T_1 = 5.0$).
Assume forward swap rate $S(0) = 4.0\%$, annual payment frequency ($freq = 1$), lognormal swap rate volatility $\sigma_S = 20.0\%$, and swap tenor 10 years.

1. Compute the annuity factor $A(S(0))$ for a 10-year swap at $4\%$:
$$A(0.04) = \sum_{i=1}^{10} \frac{1}{(1.04)^i} = \frac{1 - (1.04)^{-10}}{0.04} = \frac{1 - 0.675564}{0.04} = 8.110896$$
2. Compute the derivative of annuity $A'(S(0))$:
$$A'(0.04) = -\sum_{i=1}^{10} \frac{i}{(1.04)^{i+1}} = -40.37716$$
3. Compute the relative duration:
$$\text{Dur}_{\text{rel}} = -\frac{A'(0.04)}{A(0.04)} = \frac{40.37716}{8.110896} = 4.97814$$
4. Evaluate the convexity adjustment:
$$\text{Adj}_{\text{CMS}} \approx S(0)^2 \sigma_S^2 T_1 \times \text{Dur}_{\text{rel}}$$
$$S(0)^2 \sigma_S^2 T_1 = (0.04)^2 \times (0.20)^2 \times 5.0 = 0.0016 \times 0.04 \times 5.0 = 0.000320$$
$$\text{Adj}_{\text{CMS}} = 0.000320 \times 4.97814 = 0.00159300 = 15.93 \text{ bps}$$
Our reference implementation [`code/fi_convexity.py`](code/fi_convexity.py) and [`code/rates_models.py`](code/rates_models.py) yield:
`cms_rate_annuity_adjustment(0.04, 0.20, 5.0, 10, 1) == 0.001593` ($15.93\text{ bps}$).
The expected 10-year CMS fixing is $4.0000\% + 0.1593\% = 4.1593\%$.

### Example 3: Quanto Interest Rate Swap Adjustment
A US bank enters a quanto swap paying USD floating against the 10-year German Bund swap rate in USD notional with 3-year maturity ($T = 3.0$).
The forward EUR swap rate is $S_f(0) = 3.0\%$, its lognormal volatility is $\sigma_S = 18.0\%$, EUR/USD exchange rate volatility is $\sigma_{FX} = 12.0\%$, and correlation between the Bund rate and EUR/USD is $\rho = 0.40$.
Calculate the quanto drift and the adjustment to the rate fixing in 3 years.

The relative drift adjustment is:
$$-\rho \sigma_S \sigma_{FX} = -0.40 \times 0.18 \times 0.12 = -0.00864 \text{ per year}$$
In rate units this is $-0.00864 \times S_f(0) = -0.00864 \times 0.03 = -0.0002592$, a downward drift of about 2.59 bps per year.
Over the 3-year term:
$$\text{Adj}_{\text{quanto}} = 0.03 \times \left(e^{-0.00864 \times 3} - 1\right) = 0.03 \times (-0.025587) = -0.0007676 = -7.68 \text{ bps}$$
The linear approximation $-\rho \sigma_S \sigma_{FX} S_f(0) T = -7.78$ bps is close.
The expected Bund swap rate under the domestic USD measure is $3.0\% - 0.0768\% = 2.9232\%$.

## Pitfalls

- **Neglecting the futures convexity adjustment in curve construction:** Inserting raw futures quotes directly into discount curve bootstrapping without subtracting $\frac{1}{2}\sigma^2 T_1 T_2$ artificially raises forward rates at the 2y to 5y sector, mispricing interest rate swaps and swaptions.
- **Using normal volatility in lognormal adjustment formulas:** Substituting a normal volatility (e.g., 80 bps = 0.0080) into a lognormal convexity formula ($S^2 \sigma^2 T$) understates the adjustment by a factor of $(0.20 / 0.0080)^2 = 625$, nearly three orders of magnitude; the lognormal formula requires dimensionless percentage volatility (e.g., 0.20).
- **Truncating the swaption smile in CMS replication:** Integrating swaption prices over a narrow strike range (e.g. $\pm 100\text{ bps}$) misses significant mass in the far wings; because CMS payoffs are linear in the rate, tail swaption prices contribute significantly to the integral.
- **Assuming correlation $\rho$ is constant in quanto pricing:** Correlation between exchange rates and interest rates is notoriously unstable across economic cycles; stress testing quanto portfolios requires bumping correlation across the entire $[-1, 1]$ interval.
- **Ignoring the payment delay in CMS:** CMS fixings often occur at $T_1$ with payment delayed to $T_2$; this introduces a secondary timing adjustment that partially offsets the positive annuity adjustment.

## Interview questions

> [!question]- fi-convexity-definition | What is a convexity adjustment and why does it arise?
> A convexity adjustment is the difference between the forward expectation of an asset under a pricing measure and its forward price under its natural measure.
> It arises whenever the payment timing, margining mechanism, or currency of a derivative requires a change of numeraire whose Radon-Nikodym derivative correlates with the underlying asset.

> [!question]- fi-convexity-futures-vs-fra | Why is the futures rate higher than the forward rate for interest rates?
> Futures settle daily in cash via variation margin.
> When rates rise, a long futures position receives cash that can be immediately reinvested at higher overnight rates; when rates fall, losses are financed at lower rates.
> This positive covariance between profits and financing rates makes futures more desirable than static forwards, driving the equilibrium futures rate above the forward rate.

> [!question]- fi-convexity-ho-lee-formula | State the Ho-Lee formula for the futures convexity adjustment and define terms.
> $\text{Adj} = R_{\text{fut}} - R_{\text{fwd}} = \frac{1}{2}\sigma^2 T_1 T_2$.
> $\sigma$ is the short-rate volatility, $T_1$ is the futures contract expiry, and $T_2$ is the maturity of the underlying forward rate.

> [!question]- fi-convexity-cms-numeraire | What change of numeraire generates the CMS convexity adjustment?
> The change from the swap annuity measure $\mathbb{Q}^A$ (numeraire $A(t) = \sum \tau_i P(t, T_i)$) to the zero-coupon bond payment measure $\mathbb{Q}^{T_1}$ (numeraire $P(t, T_1)$).
> Because the annuity factor is inversely related to the swap rate, the numeraire ratio $P(t, T_1)/A(t)$ correlates positively with the swap rate, driving a positive adjustment.

> [!question]- fi-convexity-cms-duration-approx | Give the linear duration approximation for the CMS convexity adjustment.
> $\text{Adj}_{\text{CMS}} \approx S(0)^2 \sigma_S^2 T_1 \left(-\frac{A'(S(0))}{A(S(0))}\right)$.
> It equals the forward swap rate squared, times swap rate variance, times the modified duration of the underlying swap annuity.

> [!question]- fi-convexity-carr-madan-cms | Why is Carr-Madan static replication preferred over linear approximation for CMS derivatives?
> Linear approximations assume a single volatility and ignore skew, smile, and higher-order moments.
> Carr-Madan static replication expresses the nonlinear CMS payoff as an exact integral over a continuum of market swaptions across all strikes, capturing the full market volatility smile.

> [!question]- fi-convexity-in-arrears-sign | Is the convexity adjustment for an in-arrears floating rate positive or negative?
> It is strictly positive.
> Paying a rate fixing at $T_1$ at $T_1$ instead of $T_2$ removes the discount factor $(1 + \tau L)^{-1}$; because higher rates reduce the discount factor, paying without discounting increases the expected payoff.

> [!question]- fi-convexity-quanto-drift | Write the drift adjustment for a quanto interest rate under the domestic measure.
> The relative drift $dS_f / S_f$ gains $-\rho_{S, X} \sigma_S \sigma_X$, so the absolute drift adjustment is $-\rho_{S, X} \sigma_S \sigma_X S_f$.
> $\rho_{S, X}$ is the correlation between the foreign rate and the exchange rate, $\sigma_S$ is the foreign rate volatility, and $\sigma_X$ is the FX volatility.

> [!question]- fi-convexity-curve-bootstrap-impact | What happens if a desk bootstraps a discount curve using futures quotes without convexity adjustments?
> The bootstrapped zero rates will be systematically biased upward, especially in the 2y to 5y sector.
> This makes the desk overestimate forward rates, resulting in mispriced swaps, miscalculated hedge ratios, and negative carry on fixed-rate hedges.

> [!question]- fi-convexity-jensens-inequality | How is Jensen's inequality related to convexity adjustments?
> Jensen's inequality states that for a convex function $g$, $\mathbb{E}[g(X)] \ge g(\mathbb{E}[X])$.
> Bond prices and annuities are convex functions of interest rates, so expected bond prices exceed the bond price evaluated at the expected interest rate; convexity adjustments quantify this Jensen gap under measure changes.

## Further reading

- Patrick Hagan, *Convexity Conundrums: Pricing CMS Swaps, Caps, and Floors*, Wilmott Magazine, 2003.
- Damiano Brigo and Fabio Mercurio, *Interest Rate Models - Theory and Practice*, Chapter 13: "Convexity Adjustments".
- Peter Carr and Dilip Madan, *Towards a Theory of Volatility Trading*, Risk Books, 1998.
- Darrell Duffie and Rui Kan, *A Yield-Factor Model of Interest Rates*, Mathematical Finance, 1996.

## In this repo and SDE-Interview-Prep

- Code: [`code/fi_convexity.py`](code/fi_convexity.py) (numerical verification of futures convexity, CMS adjustment, and quanto drift), [`code/rates_models.py`](code/rates_models.py) (Futures convexity, CMS duration adjustment, and in-arrears functions).
- Prereqs: [Short-Rate Models](04-Short-Rate-Models.md), [Swaps and Curve Building](03-Swaps-and-Curve-Building.md).
- Next: [Rates Volatility and SABR](18-Rates-Volatility-and-SABR.md), [Term Structure Models: HJM, LGM, and LMM](19-Term-Structure-Models-HJM-LGM-LMM.md).
