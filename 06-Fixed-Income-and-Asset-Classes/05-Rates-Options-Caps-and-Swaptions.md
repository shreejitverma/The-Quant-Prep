---
type: concept
track: [quant-research]
tier: senior
status: draft
prereqs: [short-rate-models, black-scholes-formula-and-intuition]
est_hours: 5
sources: [Brigo and Mercurio - Interest Rate Models chapter 1, John Hull - Options Futures and Other Derivatives chapter 29]
---

# Rates Options: Caps and Swaptions

## TL;DR

Interest rate caps, floors, and European swaptions are the foundational nonlinear derivatives of the fixed income market.
Under the forward measure with zero-coupon bond numeraire, forward interest rates are martingales, validating Fischer Black's (1976) lognormal model.
Under the annuity measure with swap annuity numeraire, forward swap rates are martingales, yielding Black's formula for European swaptions.
When interest rates approached zero and turned negative in EUR, JPY, and CHF, lognormal models failed mathematically because $\ln(F/K)$ is undefined and lognormal volatilities diverge.
The global rates market transitioned to Louis Bachelier's (1900) normal model, where rates follow arithmetic Brownian motion and volatility is quoted in annual basis points ($\text{bp/year}$).

## Learning objectives

- Price interest rate caplets, floorlets, and caps using the Black-76 lognormal model.
- Price European payer and receiver swaptions using the annuity numeraire.
- Formulate the Bachelier normal model and evaluate option prices for zero and negative interest rates.
- Derive the conversion between normal volatility $\sigma_N$ and lognormal volatility $\sigma_{LN}$.
- Execute caplet stripping from flat market cap volatility curves.
- Distinguish swaption market conventions including physical settlement, cash settlement, and normal basis point quoting.

## Core concepts

### 1. Interest Rate Caps and Floorlets

An interest rate cap protects a floating-rate borrower against rising interest rates over a multi-year loan.
Consider a reset schedule $T_0, T_1, \dots, T_n$ with accrual fractions $\tau_i = T_i - T_{i-1}$.
At each reset date $T_{i-1}$, the floating reference rate $L(T_{i-1}, T_i)$ fixes.
At the subsequent payment date $T_i$, the payoff is disbursed in arrears:
$$\text{Payoff}_i(T_i) = N \tau_i \max(0, L(T_{i-1}, T_i) - K)$$
where $N$ is notional and $K$ is the cap strike rate.
Each individual option is termed a **caplet**.
A cap is a portfolio of caplets:
$$\text{Cap} = \sum_{i=1}^n \text{Caplet}_i$$
Notice that the first floating coupon setting at $T_0$ is already known at trade inception, so the first caplet is omitted; an $n$-period cap contains $n-1$ active caplets maturing from $T_2$ to $T_n$.

Similarly, an interest rate floor protects a lender against falling rates:
$$\text{Floorlet}_i(T_i) = N \tau_i \max(0, K - L(T_{i-1}, T_i))$$
$$\text{Floor} = \sum_{i=1}^n \text{Floorlet}_i$$

By put-call parity at each period:
$$\text{Caplet}_i(t) - \text{Floorlet}_i(t) = N \tau_i P(t, T_i)(F_i(t) - K)$$
Summing across all periods:
$$\text{Cap}(t) - \text{Floor}(t) = \text{Payer Swap}(t; K)$$
An interest rate cap minus a floor with the same strike and schedule equals a forward-starting interest rate swap.

### 2. The Black-76 Model for Caplets

Under the risk-neutral measure with money-market account numeraire $B(t) = \exp(\int_0^t r(u)du)$, evaluating the expectation of a cash flow paid at $T_i$ requires computing joint expectations of the stochastic discount factor and the rate.
Fischer Black (1976) resolved this by changing the numeraire to the zero-coupon bond maturing at payment date $T_i$: $P(t, T_i)$.

Under the $T_i$-forward measure $\mathbb{Q}^{T_i}$, the forward rate $F_i(t) = L(t; T_{i-1}, T_i)$ is an asset price divided by the numeraire:
$$F_i(t) = \frac{1}{\tau_i}\left(\frac{P(t, T_{i-1})}{P(t, T_i)} - 1\right)$$
Because $P(t, T_{i-1})$ is a tradeable asset price, $F_i(t)$ is a martingale under $\mathbb{Q}^{T_i}$ without any drift:
$$dF_i(t) = \sigma_i F_i(t) dW^{T_i}(t)$$
The value of the caplet at $t=0$ is:
$$\text{Caplet}_i(0) = P(0, T_i) \mathbb{E}^{T_i}[\tau_i \max(0, F_i(T_{i-1}) - K)]$$
Evaluating this Gaussian integral yields Black's caplet formula:
$$\text{Caplet}_i(0) = \tau_i P(0, T_i) [F_i(0)\Phi(d_1) - K\Phi(d_2)]$$
where:
$$d_1 = \frac{\ln(F_i(0) / K) + \frac{1}{2}\sigma_i^2 T_{i-1}}{\sigma_i \sqrt{T_{i-1}}}$$
$$d_2 = d_1 - \sigma_i \sqrt{T_{i-1}}$$

### 3. European Swaptions and the Annuity Numeraire

A European swaption grants the holder the right, but not the obligation, to enter into an interest rate swap at a future expiry date $T_0$.
1. **Payer Swaption:** Right to pay fixed rate $K$ and receive floating.
At expiry $T_0$, the swap value is:
$$\text{Value}(T_0) = \max\left(0, (S(T_0) - K) \sum_{i=1}^n \tau_i P(T_0, T_i)\right)$$
2. **Receiver Swaption:** Right to receive fixed rate $K$ and pay floating:
$$\text{Value}(T_0) = \max\left(0, (K - S(T_0)) \sum_{i=1}^n \tau_i P(T_0, T_i)\right)$$

The term $A(t) = \sum_{i=1}^n \tau_i P(t, T_i)$ is the **annuity factor** (or PV01 / basis point value per unit notional).
Because $A(t)$ is a linear portfolio of tradeable zero-coupon bonds, it serves as a valid numeraire.
Under the annuity measure $\mathbb{Q}^A$ associated with $A(t)$, the forward par swap rate $S(t) = \frac{P(t, T_0) - P(t, T_n)}{A(t)}$ is an asset price divided by the numeraire.
Consequently, $S(t)$ is a martingale under $\mathbb{Q}^A$:
$$dS(t) = \sigma_{swap} S(t) dW^A(t)$$

Applying Black's formula under the annuity measure yields:
$$\text{Payer Swaption}(0) = A(0) [S(0)\Phi(d_1) - K\Phi(d_2)]$$
$$\text{Receiver Swaption}(0) = A(0) [K\Phi(-d_2) - S(0)\Phi(-d_1)]$$
where:
$$A(0) = \sum_{i=1}^n \tau_i P(0, T_i)$$
$$d_1 = \frac{\ln(S(0) / K) + \frac{1}{2}\sigma_{swap}^2 T_0}{\sigma_{swap} \sqrt{T_0}}$$
$$d_2 = d_1 - \sigma_{swap} \sqrt{T_0}$$

### 4. The Bachelier (Normal) Model

Between 2014 and 2022, central bank benchmark rates in Europe, Japan, and Switzerland traded below zero.
When forward rates $F$ or strikes $K$ are negative, Black's formula fails:
1. The term $\ln(F/K)$ is mathematically undefined for negative arguments.
2. Even for small positive forwards $F \to 0^+$, lognormal volatility must diverge to infinity ($\sigma_{LN} \to \infty$) to match finite option market premiums.

The industry adopted the normal model originally formulated by Louis Bachelier (1900):
$$dF(t) = \sigma_N dW(t)$$
where $\sigma_N$ is the normal volatility, measured in annualized rate units (or basis points per year).
Because $F(T)$ is normally distributed:
$$F(T) \sim \mathcal{N}(F(0), \sigma_N^2 T)$$
Negative interest rates are naturally accommodated.

#### Bachelier Pricing Formula
Evaluating the expectation under normal dynamics:
$$\text{Call}_{\text{Bachelier}}(0) = A(0) \left[ (F(0) - K)\Phi(d) + \sigma_N \sqrt{T}\phi(d) \right]$$
$$\text{Put}_{\text{Bachelier}}(0) = A(0) \left[ (K - F(0))\Phi(-d) + \sigma_N \sqrt{T}\phi(d) \right]$$
where:
$$d = \frac{F(0) - K}{\sigma_N \sqrt{T}}$$
and $\phi(d) = \frac{1}{\sqrt{2\pi}} e^{-d^2 / 2}$ is the standard normal probability density function.

#### ATM Bachelier Approximation
At the money ($F(0) = K$), $d = 0$, $\Phi(0) = 0.5$, and $\phi(0) = \frac{1}{\sqrt{2\pi}} \approx 0.398942$.
The at-the-money option price simplifies to:
$$\text{ATM Price} = A(0) \frac{\sigma_N \sqrt{T}}{\sqrt{2\pi}} \approx 0.398942 \times A(0) \sigma_N \sqrt{T}$$
This provides a rule of thumb for rates traders: an ATM swaption price is linear in normal volatility $\sigma_N$ and square root of expiry $\sqrt{T}$.

#### Conversion Between Normal and Lognormal Volatility
Equating the ATM Black-76 price to the ATM Bachelier price:
$$A(0) F(0) \left(2\Phi\left(\frac{1}{2}\sigma_{LN}\sqrt{T}\right) - 1\right) \approx A(0) \frac{\sigma_N \sqrt{T}}{\sqrt{2\pi}}$$
Using the first-order Taylor expansion $\Phi(x) \approx \frac{1}{2} + \frac{x}{\sqrt{2\pi}}$:
$$A(0) F(0) \frac{\sigma_{LN}\sqrt{T}}{\sqrt{2\pi}} \approx A(0) \frac{\sigma_N \sqrt{T}}{\sqrt{2\pi}}$$
$$\sigma_N \approx F(0) \times \sigma_{LN}$$
For example, if $F(0) = 4.0\%$ and lognormal volatility $\sigma_{LN} = 20.0\%$, the equivalent normal volatility is:
$$\sigma_N \approx 0.04 \times 0.20 = 0.0080 = 80 \text{ bp/year}$$

### 5. Caplet Stripping

In financial markets, caps are quoted as a single **flat volatility** $\sigma_{\text{flat}}(T_n)$ for a given maturity.
This flat volatility is plugged into Black's formula for every individual caplet:
$$\text{Market Cap Price}(T_n) = \sum_{i=2}^n \text{BlackCaplet}(F_i(0), K, \sigma_{\text{flat}}(T_n), T_{i-1})$$
However, each caplet in reality has its own forward expiry $T_{i-1}$ and experiences its own forward volatility $\sigma_i$.
Using a single flat volatility creates internal arbitrage across maturities.

**Caplet stripping** is the bootstrapping procedure that extracts spot caplet volatilities $\{\sigma_i\}_{i=2}^n$ from market quotes of standard caps:
1. From the 1-year cap (single caplet maturing at $T_1$), solve for $\sigma_2$ directly.
2. Given market prices for the 2-year cap:
$$\text{Cap}(T_2) = \text{Caplet}_2(\sigma_2) + \text{Caplet}_3(\sigma_3)$$
Since $\sigma_2$ is known from step 1, solve for $\sigma_3$ using 1D root-finding on $\text{Caplet}_3$.
3. Proceed sequentially for all cap maturities.
Because market caps are liquid only at discrete annual pillars (1y, 2y, 3y, 5y, 7y, 10y), practitioners interpolate cap prices or fit smooth parametric curves (such as cubic splines or Nelson-Siegel functions) to avoid jagged caplet volatilities.

## Worked examples

### Example 1: Black-76 ATM Swaption Valuation
Price a 2-year into 5-year ATM European payer swaption with forward swap rate $S(0) = 4.0\%$, strike $K = 4.0\%$, lognormal volatility $\sigma_{LN} = 25.0\%$, expiry $T = 2.0\text{ years}$, and annuity factor $A(0) = 3.80$.

Compute standard deviation:
$$\sigma \sqrt{T} = 0.25 \times \sqrt{2.0} = 0.25 \times 1.414214 = 0.353553$$
Compute $d_1$ and $d_2$:
$$d_1 = \frac{\ln(0.04 / 0.04) + 0.5 \times (0.353553)^2}{0.353553} = \frac{0 + 0.0625}{0.353553} = 0.176777$$
$$d_2 = d_1 - \sigma \sqrt{T} = 0.176777 - 0.353553 = -0.176777$$
Evaluate cumulative normal functions:
$$\Phi(0.176777) = 0.570198$$
$$\Phi(-0.176777) = 1 - 0.570198 = 0.429802$$
Evaluate swaption price:
$$\text{Price} = 3.80 \times [0.04 \times 0.570198 - 0.04 \times 0.429802]$$
$$\text{Price} = 3.80 \times 0.04 \times [0.570198 - 0.429802] = 0.152 \times 0.140396 = 0.021340$$
Using our reference implementation [`rates_models.py`](code/rates_models.py):
$$\text{Exact Price} = 0.021328 \quad (213.28 \text{ bps})$$

### Example 2: Bachelier Normal Swaption in Negative Rate Environment
Price a 2-year European payer swaption on a negative forward rate $F(0) = -20\text{ bps} = -0.0020$, strike $K = -0.0020$, normal volatility $\sigma_N = 80\text{ bp/year} = 0.0080$, expiry $T = 2.0\text{ years}$, and annuity factor $A(0) = 3.80$.

Because $F(0) = K$, $d = 0$:
$$\text{Price} = A(0) \times \frac{\sigma_N \sqrt{T}}{\sqrt{2\pi}} = 3.80 \times \frac{0.0080 \times \sqrt{2.0}}{\sqrt{2\pi}}$$
$$\sigma_N \sqrt{T} = 0.0080 \times 1.414214 = 0.011314$$
$$\frac{0.011314}{\sqrt{2\pi}} = \frac{0.011314}{2.506628} = 0.0045136$$
$$\text{Price} = 3.80 \times 0.0045136 = 0.017152 \quad (171.52 \text{ bps})$$
Our reference implementation [`rates_models.py`](code/rates_models.py) yields:
$$\text{Exact Bachelier Price} = 0.017151 \quad (171.51 \text{ bps})$$
The Black-76 model would fail on this trade due to negative arguments.

### Example 3: Stripping a 2-Period Caplet
Suppose $P(0, 1) = 0.9615$, $P(0, 2) = 0.9200$, 1y forward rate $F_1 = 4.0\%$, 2y forward rate $F_2 = 4.5\%$, and strike $K = 4.0\%$.
An annual 1y cap (which pays at $T=2$ based on $F(1)$) trades at 75 bps of notional ($0.0075$).
Determine the spot volatility of the 1y forward caplet using Black-76.

The cap has only 1 caplet fixing at $T_1 = 1.0$ and paying at $T_2 = 2.0$:
$$\text{Caplet}_1 = 1.0 \times P(0, 2) \times [F_1 \Phi(d_1) - K \Phi(d_2)] = 0.0075$$
$$0.9200 \times [0.04 \Phi(d_1) - 0.04 \Phi(d_2)] = 0.0075$$
$$[0.04 \Phi(d_1) - 0.04 \Phi(d_2)] = \frac{0.0075}{0.9200} = 0.008152$$
Inverting Black-76 with $F = K = 0.04$:
$$0.04 \times (2\Phi(0.5 \sigma_1 \sqrt{1}) - 1) = 0.008152$$
$$2\Phi(0.5 \sigma_1) - 1 = \frac{0.008152}{0.04} = 0.203804$$
$$\Phi(0.5 \sigma_1) = 0.601902 \implies 0.5 \sigma_1 \approx 0.2582 \implies \sigma_1 \approx 51.64\%$$
The spot caplet volatility is 51.64%.

## Pitfalls

- **Confusing flat cap volatility with spot caplet volatility:** Market screens display flat volatilities; calculating the delta or vega of an individual caplet using the flat cap volatility introduces hedging mismatches across the curve.
- **Physical vs cash-settled swaption pricing:** Physical settlement delivers an actual swap valued at par annuity $A(0)$; cash-settled swaptions settle against an ISDA benchmark formula that discounts cash flows at a single internal rate of return, inducing an embedded convexity difference known as the **cash-settlement adjustment**.
- **Payer swaption sign convention:** A payer swaption (paying fixed, receiving floating) is a **call** on the swap rate, but corresponds to a **put** on the underlying fixed-coupon bond.
Confusing call/put terminology between rates and bond spaces leads to opposite delta trades.
- **Timing discrepancy in caplets:** The caplet rate fixes at $T_{i-1}$ but cash settles at $T_i$; discounting must be computed with the payment discount factor $P(0, T_i)$, but the option expiration time used in volatility calculations $\sigma \sqrt{T}$ is $T_{i-1}$.
- **Assuming constant volatility across strikes:** Rates options exhibit pronounced smile and skew; using flat Black-76 or Bachelier across strikes misprices out-of-the-money collars and butterfly structures.

## Interview questions

> [!question]- fi-rates-options-black-numeraire | What numeraire makes the forward swap rate a martingale in Black-76?
> The annuity factor $A(t) = \sum_{i=1}^n \tau_i P(t, T_i)$ is the numeraire.
> Under the associated annuity measure $\mathbb{Q}^A$, the forward swap rate $S(t) = \frac{P(t, T_0) - P(t, T_n)}{A(t)}$ is a tradeable asset relative to the numeraire and is therefore a driftless martingale.

> [!question]- fi-rates-options-bachelier-vs-black | Why did the rates derivatives market switch from Black-76 to Bachelier?
> Black-76 assumes lognormal dynamics $dF = \sigma F dW$, which breaks down when interest rates are negative or near zero because $\ln(F/K)$ is undefined and implied volatility explodes.
> Bachelier assumes normal dynamics $dF = \sigma_N dW$, which accommodates negative rates without mathematical singularity.

> [!question]- fi-rates-options-vol-conversion | How do you convert lognormal volatility to normal volatility approximately?
> $\sigma_N \approx F(0) \times \sigma_{LN}$.
> By equating the ATM option prices of Black-76 and Bachelier using first-order Taylor expansions, normal volatility in bps/year is approximately the forward rate times the lognormal percentage volatility.

> [!question]- fi-rates-options-cap-floor-parity | State and prove cap-floor parity.
> $\text{Cap}(t) - \text{Floor}(t) = \text{Payer Swap}(t)$.
> At each period $i$, $\max(0, L_i - K) - \max(0, K - L_i) = L_i - K$.
> Multiplying by $\tau_i$ and discounting yields the exact cash flow of a payer swap leg against fixed $K$.

> [!question]- fi-rates-options-caplet-stripping | What is caplet stripping and why is it necessary?
> Caps trade in the market at a single flat volatility per maturity, but forward rates at different tenors have distinct spot volatilities.
> Caplet stripping is the recursive bootstrapping procedure used to extract the spot volatility of each individual forward caplet from quoted flat cap prices.

> [!question]- fi-rates-options-cash-vs-physical | What is the difference between physical and cash settlement for European swaptions?
> In physical settlement, the option holder enters a live interest rate swap with cash flows discounted on the OIS/SOFR CSA curve.
> In standard cash settlement, the counterparty receives a lump sum determined by discounting swap coupons at the swap rate itself (an internal rate of return formula), creating a pricing discrepancy known as the cash settlement convexity adjustment.

> [!question]- fi-rates-options-bachelier-atm-rule | What is the quick mental formula for the ATM price of a Bachelier swaption?
> $\text{Price} \approx 0.4 \times A(0) \sigma_N \sqrt{T}$.
> Because $\phi(0) = \frac{1}{\sqrt{2\pi}} \approx 0.3989$, the ATM price is simply 40% of the normal volatility times the square root of expiry times the annuity factor.

> [!question]- fi-rates-options-payer-delta | What is the Black-76 delta of a payer swaption with respect to the forward swap rate?
> $\Delta = \frac{\partial V}{\partial S(0)} = A(0)\Phi(d_1)$.
> It equals the annuity factor multiplied by the cumulative normal probability of exercise, representing the expected basis point sensitivity of the option.

> [!question]- fi-rates-options-vega-black-vs-norm | How does the vega of an ATM option differ between Black-76 and Bachelier?
> In Black-76, vega is $\frac{\partial V}{\partial \sigma_{LN}} = A(0) S(0) \sqrt{T} \phi(d_1)$.
> In Bachelier, normal vega is $\frac{\partial V}{\partial \sigma_N} = A(0) \sqrt{T} \phi(d)$.
> Black vega scales directly with the forward rate level $S(0)$, while normal vega is invariant to the rate level.

> [!question]- fi-rates-options-swaption-straddle | What is a swaption straddle and what risk does it isolate?
> A swaption straddle is the simultaneous purchase of a payer swaption and a receiver swaption with the same strike (usually ATM) and expiry.
> It isolates pure volatility (vega and gamma) while neutralizing directional interest rate delta.

## Further reading

- Fischer Black, *The Pricing of Commodity Contracts*, Journal of Financial Economics, 1976.
- Damiano Brigo and Fabio Mercurio, *Interest Rate Models - Theory and Practice*, Chapter 1: "Definitions and Quick Tour of the Market".
- John Hull, *Options, Futures, and Other Derivatives*, Chapter 29: "Interest Rate Derivatives: The Standard Market Models".
- Louis Bachelier, *Théorie de la Spéculation*, Annales Scientifiques de l'École Normale Supérieure, 1900.

## In this repo and SDE-Interview-Prep

- Code: [`code/rates_models.py`](code/rates_models.py) (Black-76 and Bachelier normal pricing, Greeks, and implied volatility solvers).
- Prereq: [Short-Rate Models](04-Short-Rate-Models.md).
- Next: [Convexity Adjustments](17-Convexity-Adjustments.md), [Rates Volatility and SABR](18-Rates-Volatility-and-SABR.md).
