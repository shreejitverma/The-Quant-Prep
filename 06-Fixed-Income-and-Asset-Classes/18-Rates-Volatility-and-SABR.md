---
type: concept
track: [quant-research]
tier: senior
status: draft
prereqs: [rates-options-caps-and-swaptions, stochastic-volatility-heston-and-sabr]
est_hours: 5
sources: [Patrick Hagan et al. - Managing Smile Risk 2002, Damiano Brigo and Fabio Mercurio - Interest Rate Models chapter 13]
---

# Rates Volatility and SABR

## TL;DR

The volatility surface in fixed income markets is a three-dimensional cube parameterized by strike, option expiry, and underlying swap tenor.
Because flat Black-76 and Bachelier models fail to reproduce the volatility smile and skew observed across strikes, the fixed income market universally calibrates to the SABR model of Hagan et al. (2002).
SABR models the forward rate as a constant elasticity of variance (CEV) process driven by stochastic volatility.
Its parameters directly map to intuitive market features: $\alpha$ sets the volatility level, $\beta$ controls the backbone, $\rho$ determines skew, and $\nu$ controls smile curvature.
To price derivatives in negative-rate environments, shifted SABR translates rates by a positive constant shift.
While Hagan's asymptotic formula provides instantaneous calibration, practitioners must monitor wing densities to prevent butterfly arbitrage.

## Learning objectives

- Map the structure of the fixed income volatility cube across strike, expiry, and tenor dimensions.
- Formulate the SABR stochastic differential equations and identify the role of each parameter ($\alpha, \beta, \rho, \nu$).
- Evaluate Hagan's asymptotic formula for implied Black and normal volatility.
- Implement shifted SABR for negative and near-zero forward interest rates.
- Execute a production calibration workflow: fixing $\beta$, solving for $\alpha$ at ATM, and fitting $(\rho, \nu)$ to out-of-the-money quotes.
- Diagnose and remediate negative density and wing arbitrage in the asymptotic Hagan expansion.

## Core concepts

### 1. The Fixed Income Volatility Cube

Unlike equity or FX markets where volatility surfaces have two dimensions (strike and expiration), fixed income swaption markets are three-dimensional:
1. **Option Expiry ($T$):** The time until the option can be exercised (e.g., 1 month to 30 years).
2. **Swap Tenor ($S$):** The length of the underlying interest rate swap delivered upon exercise (e.g., 1 year to 30 years).
3. **Strike ($K$):** The fixed rate of the underlying swap, typically parameterized as moneyness or basis point offsets from the at-the-money forward rate ($K - S(0)$).

For interest rate caps and floors, the surface collapses to two dimensions (strike vs cap maturity), but requires stripping into spot caplet volatilities.
The swaption volatility cube is the primary pricing and risk-management input for callable bonds, Bermudan swaptions, CMS products, and multi-factor term structure models.

### 2. The SABR Model Formulation

Patrick Hagan, Deep Kumar, Andrew Lesniewski, and Diana Woodward (2002) introduced the SABR (Stochastic Alpha, Beta, Rho) model to provide a parsimonious, arbitrage-free representation of forward price smiles.
Under the forward measure $\mathbb{Q}^T$ associated with the settlement of forward rate $F(t)$, the SABR dynamics are:
$$dF(t) = \alpha(t) F(t)^\beta dW_1(t)$$
$$d\alpha(t) = \nu \alpha(t) dW_2(t)$$
with correlation:
$$dW_1(t) dW_2(t) = \rho dt$$
and initial conditions $F(0) = f_0 > 0$, $\alpha(0) = \alpha > 0$.

#### Parameter Interpretation
1. **Initial Volatility $\alpha$:** Controls the overall level of implied volatility.
It acts as a vertical scale factor for the smile.
2. **Backbone Exponent $\beta \in [0, 1]$:** Governs the elasticity between the forward rate level and its local volatility:
   - $\beta = 1$: Lognormal dynamics (Black-76 backbone, percentage volatility is constant as rates shift).
   - $\beta = 0$: Normal dynamics (Bachelier backbone, absolute basis point volatility is constant).
   - $\beta = 0.5$: Square-root diffusion (CIR backbone).
   In practice, $\beta$ is not calibrated dynamically; it is fixed structurally based on market regime (e.g. $\beta = 0.5$ historically for USD Libor, $\beta = 0$ for modern EUR/SOFR normal curves).
3. **Correlation $\rho \in (-1, 1)$:** Governs the **skew** (slope of implied volatility around the ATM strike).
   - $\rho < 0$: When rates fall, volatility rises (downward-sloping skew).
   - $\rho > 0$: When rates rise, volatility rises (upward-sloping skew).
   - $\rho = 0$: Symmetric smile around the ATM rate.
4. **Vol-of-Vol $\nu \ge 0$:** Governs the **curvature / convexity** of the smile.
   Higher $\nu$ fattens the wings, increasing implied volatility for out-of-the-money payer and receiver strikes.

### 3. Hagan's Asymptotic Implied Volatility Formula

Hagan et al. applied singular perturbation techniques to derive an explicit, closed-form asymptotic approximation for implied Black volatility $\sigma_B(K, F)$.
For $F \neq K$:
$$\sigma_B(K, F) = \frac{\alpha}{(F K)^{(1-\beta)/2} \left[ 1 + \frac{(1-\beta)^2}{24} \ln^2(F/K) + \frac{(1-\beta)^4}{1920} \ln^4(F/K) \right]} \cdot \frac{z}{\chi(z)} \cdot \left[ 1 + \Gamma T \right]$$
where:
$$z = \frac{\nu}{\alpha} (F K)^{(1-\beta)/2} \ln(F / K)$$
$$\chi(z) = \ln\left( \frac{\sqrt{1 - 2\rho z + z^2} + z - \rho}{1 - \rho} \right)$$
$$\Gamma = \frac{(1-\beta)^2}{24} \frac{\alpha^2}{(FK)^{1-\beta}} + \frac{1}{4} \frac{\rho \beta \nu \alpha}{(FK)^{(1-\beta)/2}} + \frac{2 - 3\rho^2}{24} \nu^2$$

#### At-The-Money (ATM) Formula
In the limit as strike $K \to F$, $z \to 0$ and $\frac{z}{\chi(z)} \to 1$.
The ATM Black volatility simplifies to:
$$\sigma_{B, \text{ATM}} = \frac{\alpha}{F^{1-\beta}} \left[ 1 + \left( \frac{(1-\beta)^2}{24} \frac{\alpha^2}{F^{2(1-\beta)}} + \frac{1}{4} \frac{\rho \beta \nu \alpha}{F^{1-\beta}} + \frac{2 - 3\rho^2}{24} \nu^2 \right) T \right]$$
This equation allows $\alpha$ to be solved directly from the market ATM quote given $(\beta, \rho, \nu)$.

### 4. Shifted SABR for Negative Rates

In standard SABR, $F(t)^\beta$ requires $F(t) > 0$.
When interest rates become negative, standard SABR breaks down.
To support negative rates, the industry utilizes **Shifted SABR** (or Displaced Diffusion SABR):
$$d(F(t) + s) = \alpha(t) (F(t) + s)^\beta dW_1(t)$$
$$d\alpha(t) = \nu \alpha(t) dW_2(t)$$
where $s > 0$ is a fixed, deterministic shift parameter chosen such that $F(t) + s > 0$ across all plausible market scenarios (e.g., $s = 2.0\%$ or $s = 3.0\%$).

All calculations for implied volatility proceed using shifted forward $F' = F + s$ and shifted strike $K' = K + s$.
The resulting Black volatility $\sigma_B'$ is converted into option prices using the shifted Black formula:
$$\text{Call}(0) = A(0) [(F + s)\Phi(d_1) - (K + s)\Phi(d_2)]$$
Alternatively, the shifted SABR model can be converted to normal Bachelier volatility $\sigma_N$ via root-finding inversion.

### 5. Calibration Workflow

In production trading systems, calibrating the SABR surface follows a robust sequential protocol:
1. **Fix $\beta$:** Set $\beta$ globally across the entire swaption matrix (e.g. $\beta = 0.5$ or $\beta = 0.0$).
Allowing $\beta$ to float creates an over-determined system where $\alpha$ and $\beta$ compensate for each other, causing wild day-to-day jumps in Greeks.
2. **Fit ATM Volatility:** For each expiry-tenor pair, extract the liquid ATM market volatility quote $\sigma_{\text{ATM}}$.
Use the ATM cubic equation in $\alpha$ to solve for $\alpha$ analytically or via Newton-Raphson.
3. **Calibrate $(\rho, \nu)$ to Out-of-the-Money Strikes:**
Minimize the weighted sum of squared pricing errors across available market strikes $\{K_i\}$:
$$\min_{\rho, \nu} \sum_{i=1}^M w_i \left( \sigma_{\text{SABR}}(K_i; \alpha(\rho, \nu), \beta, \rho, \nu) - \sigma_{\text{market}}(K_i) \right)^2$$
subject to constraints $-0.999 \le \rho \le 0.999$ and $\nu \ge 0$.
Weights $w_i$ are inversely proportional to bid-ask spreads, prioritizing liquid near-the-money strikes over illiquid far wings.

### 6. Wing Arbitrage and Negative Probabilities

Hagan's formula is an asymptotic approximation rather than the exact solution of the underlying PDE.
At extreme strikes ($K \to 0$ or $K \to \infty$) and long maturities $T > 10\text{y}$, the formula can produce:
1. **Negative Implied Probability Density:**
The Breeden-Litzenberger risk-neutral density is:
$$q(K) = \frac{\partial^2 \text{Price}}{\partial K^2}$$
If $q(K) < 0$ for any strike $K$, butterfly spreads ($\text{Call}(K - \epsilon) - 2\text{Call}(K) + \text{Call}(K + \epsilon)$) yield negative prices, permitting costless arbitrage.
2. **Negative Implied Volatilities:** At extreme wings, $1 + \Gamma T$ can become negative if $\rho$ or $\nu$ are large.

To eliminate wing arbitrage in production:
- **Asymptotic Wing Extrapolation:** Replace Hagan's formula outside liquid strike bounds $[\underline{K}, \overline{K}]$ with smooth linear or SABR-free tail extrapolations that guarantee $q(K) > 0$.
- **PDE Solutions:** Solve the 2D SABR Kolmogorov forward equation using finite difference schemes with absorbing or reflecting boundary conditions.

## Worked examples

### Example 1: Hagan SABR Volatility Calculation
Evaluate the implied Black volatility for an annual swaption with forward rate $F = 4.0\%$, expiry $T = 1.0\text{ year}$, and SABR parameters:
$$\alpha = 0.035, \quad \beta = 0.5, \quad \rho = -0.25, \quad \nu = 0.40$$
Compute implied volatilities for $K = 2.0\%$, $K = 4.0\%$ (ATM), and $K = 6.0\%$.

1. **ATM Strike ($K = 0.04$):**
$$1 - \beta = 0.5$$
$$F^{1-\beta} = \sqrt{0.04} = 0.20$$
$$\frac{\alpha}{F^{1-\beta}} = \frac{0.035}{0.20} = 0.1750$$
Compute $\Gamma$:
$$\Gamma = \frac{(0.5)^2}{24}\frac{(0.035)^2}{(0.04)} + \frac{1}{4}\frac{(-0.25)(0.5)(0.40)(0.035)}{\sqrt{0.04}} + \frac{2 - 3(-0.25)^2}{24}(0.40)^2$$
$$\Gamma = 0.000319 - 0.002187 + 0.012083 = 0.010215$$
$$\sigma_{B, \text{ATM}} = 0.1750 \times (1 + 0.010215 \times 1.0) = 0.176788 = 17.68\%$$

2. **Low Strike ($K = 0.02$):**
Evaluating Hagan's formula via [`rates_models.py`](code/rates_models.py):
$$\sigma_B(0.02) = 27.54\%$$

3. **High Strike ($K = 0.06$):**
Evaluating Hagan's formula via [`rates_models.py`](code/rates_models.py):
$$\sigma_B(0.06) = 16.54\%$$

Because $\rho = -0.25 < 0$, the smile exhibits pronounced negative skew: the 2% strike volatility ($27.54\%$) is significantly higher than the 6% strike volatility ($16.54\%$).

### Example 2: Parameter Sensitivity of the SABR Smile
Consider how changing SABR parameters affects the volatility smile generated in Example 1:
1. **Increasing $\nu$ from $0.40$ to $0.80$:** Increases the curvature of the wings.
The 2% strike vol rises from $27.54\%$ to $33.20\%$, and the 6% strike vol rises from $16.54\%$ to $20.15\%$, while the ATM vol changes only marginally (by the $\nu^2 T$ term).
2. **Changing $\rho$ from $-0.25$ to $0.0$:** Eliminates the directional skew, centering the minimum of the smile close to the ATM forward rate ($F = 4\%$).
3. **Changing $\rho$ to $+0.30$:** Inverts the skew, causing out-of-the-money payer swaptions ($K = 6\%$) to trade at a higher volatility than out-of-the-money receiver swaptions ($K = 2\%$).

### Example 3: Shifted SABR for a Negative Rate
Suppose the 2-year EUR forward swap rate is $F = -0.50\% = -0.0050$.
We configure a shifted SABR model with shift $s = 3.0\% = 0.0300$.
The shifted forward rate is:
$$F' = F + s = -0.0050 + 0.0300 = 0.0250 \quad (2.50\%)$$
For an ATM strike $K = -0.0050$, the shifted strike is $K' = 0.0250$.
Using parameters $\alpha = 0.035, \beta = 0.5, \rho = -0.25, \nu = 0.40$:
The shifted forward rate $F' = 0.0250$ is strictly positive, enabling direct application of Hagan's formula.
Our reference implementation [`rates_models.py`](code/rates_models.py) yields a valid implied volatility of $22.25\%$ on shifted coordinates.

## Pitfalls

- **Floating $\beta$ in daily recalibration:** Allowing the optimization algorithm to find $\beta$ alongside $(\alpha, \rho, \nu)$ produces unstable parameters; $\alpha$ and $\beta$ exhibit strong linear collinearity at ATM, causing hedge ratios to swing violently between resets.
- **Asymptotic wing breakdown for long expiries:** Using Hagan's formula for $T > 15\text{y}$ with high $\nu$ often produces negative probability densities in the far wings; risk engines must validate Breeden-Litzenberger second derivatives ($\partial^2 V / \partial K^2 \ge 0$).
- **Calibrating to unadjusted cash-settled swaption quotes:** Cash-settled swaptions trade at prices distorted by the annuity discounting convention; calibrating SABR directly to cash quotes without convexity adjustments corrupts the physical swaption surface.
- **Ignoring the shift parameter boundary:** If rates plunge below $-s$, the shifted forward $F + s$ turns negative, crashing the pricing library; shifts must be chosen wide enough to accommodate extreme negative scenarios (e.g. $s \ge 5\%$).
- **Confusing normal SABR with lognormal SABR:** Quoting desks that trade in normal basis points calibrate normal SABR ($\beta = 0$); mixing normal $\alpha$ (quoted in bps) with lognormal formulas yields catastrophic pricing errors.

## Interview questions

> [!question]- fi-rates-vol-sabr-sde | Write the SABR model stochastic differential equations and identify all parameters.
> The equations are $dF(t) = \alpha(t) F(t)^\beta dW_1(t)$ and $d\alpha(t) = \nu \alpha(t) dW_2(t)$, with $dW_1(t) dW_2(t) = \rho dt$.
> $F$ is the forward rate, $\alpha$ is volatility level, $\beta$ is elasticity, $\nu$ is vol-of-vol, and $\rho$ is the correlation between rate shocks and volatility shocks.

> [!question]- fi-rates-vol-sabr-param-roles | What are the qualitative market roles of $\alpha, \beta, \rho,$ and $\nu$?
> $\alpha$ controls overall volatility level (vertical shift of the curve).
> $\beta$ governs the backbone (relationship between rate level and volatility).
> $\rho$ controls skew (slope of implied volatility around the ATM strike).
> $\nu$ controls smile curvature (convexity and wing height).

> [!question]- fi-rates-vol-sabr-why-fix-beta | Why do quants fix $\beta$ instead of calibrating it from market prices?
> $\alpha$ and $\beta$ are collinear at the money: multiple $(\alpha, \beta)$ pairs produce almost identical ATM volatilities.
> Letting $\beta$ float leads to unstable parameters, poor out-of-sample extrapolation, and noisy Greeks; quants fix $\beta$ based on historical backbone regressions or market convention.

> [!question]- fi-rates-vol-sabr-negative-rates | How does shifted SABR handle negative interest rates?
> It introduces a constant positive shift $s$ so that $F(t) + s > 0$.
> The dynamics become $d(F + s) = \alpha (F + s)^\beta dW_1$ and $d\alpha = \nu \alpha dW_2$, allowing Hagan's formula to operate on shifted positive coordinates $F' = F + s$ and $K' = K + s$.

> [!question]- fi-rates-vol-sabr-wing-arbitrage | What is wing arbitrage in Hagan's asymptotic formula?
> Hagan's formula is an asymptotic approximation ($T \to 0$ or small $\nu$).
> For deep out-of-the-money strikes or long maturities, the formula can produce a non-convex price curve where the second derivative $\partial^2 V / \partial K^2 < 0$, implying negative probability densities and enabling butterfly arbitrage.

> [!question]- fi-rates-vol-sabr-atm-alpha-solve | How is $\alpha$ determined during calibration once $(\beta, \rho, \nu)$ are specified?
> It is solved from the ATM market quote using Hagan's ATM formula: $\sigma_{\text{ATM}} = \frac{\alpha}{F^{1-\beta}} [1 + \Gamma(\alpha, \beta, \rho, \nu) T]$.
> This is a cubic polynomial in $\alpha$, which can be inverted analytically or via a fast 1D Newton-Raphson iteration.

> [!question]- fi-rates-vol-sabr-cube-dims | What are the three dimensions of the fixed income swaption volatility cube?
> Expiry (time until swaption exercise), Tenor (length of the underlying swap), and Strike (or moneyness relative to ATM forward swap rate).

> [!question]- fi-rates-vol-sabr-rho-sign | If swaption volatility is higher for low strikes than for high strikes, what is the sign of $\rho$?
> $\rho$ is negative ($\rho < 0$).
> Negative correlation between rate shocks and volatility shocks produces a downward-sloping implied volatility skew where low strikes trade at a volatility premium.

> [!question]- fi-rates-vol-sabr-breeden-litzenberger | How do you check if a calibrated SABR smile is arbitrage-free?
> By verifying the Breeden-Litzenberger condition: the risk-neutral probability density function $q(K) = \frac{\partial^2 C}{\partial K^2}$ must be strictly non-negative ($q(K) \ge 0$) for all strikes $K \in (0, \infty)$, and call prices must be monotonically decreasing in strike.

> [!question]- fi-rates-vol-sabr-normal-vs-lognormal | What is the difference between normal SABR and lognormal SABR?
> Normal SABR sets $\beta = 0$, modeling rates with arithmetic diffusion where volatility is quoted in basis points per year.
> Lognormal SABR sets $\beta = 1$, modeling rates with geometric diffusion where volatility is quoted as a percentage of the rate level.

## Further reading

- Patrick Hagan, Deep Kumar, Andrew Lesniewski, and Diana Woodward, *Managing Smile Risk*, Wilmott Magazine, 2002.
- Patrick Hagan, *Arbitrage-Free SABR*, Wilmott Magazine, 2014.
- Damiano Brigo and Fabio Mercurio, *Interest Rate Models - Theory and Practice*, Chapter 13: "SABR Model".
- Paulot Louis, *Asymptotic Implied Volatility in Stochastic Volatility Models*, Applied Mathematical Finance, 2015.

## In this repo and SDE-Interview-Prep

- Code: [`code/rates_models.py`](code/rates_models.py) (Hagan SABR lognormal and normal implied vol, shifted SABR).
- Prereq: [Rates Options: Caps and Swaptions](05-Rates-Options-Caps-and-Swaptions.md).
- Next: [Term Structure Models: HJM, LGM, and LMM](19-Term-Structure-Models-HJM-LGM-LMM.md).
