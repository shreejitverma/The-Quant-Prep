---
type: problem-set
track: [quant-trader, quant-research, quant-risk]
tier: core
status: draft
prereqs: [kelly-criterion-and-position-sizing, var-and-expected-shortfall, xva, liquidity-and-model-risk]
est_hours: 8
sources: [Philippe Jorion - Value at Risk, Jon Gregory - Counterparty Credit Risk and Credit Value Adjustment, Robert Carver - Systematic Trading, Robert Almgren and Neil Chriss - Optimal Execution of Portfolio Transactions (2000), Sheldon Natenberg - Option Volatility and Pricing]
---

# Risk and Trading Problem Set

## TL;DR

Quantitative risk management and trading interviews demand rapid, error-free computational proficiency across betting decisions, portfolio tail risk, stress testing, drawdown mechanics, Greek attribution, counterparty exposure profiles, XVA pricing, and market impact.
This problem set presents sixteen comprehensive, fully worked computational problems spanning the entire risk analytics and trading curriculum.
Every problem contains exact analytical derivations, intermediate equations, numerical calculations, and real-world sanity checks.
Mastering these problems equips researchers, risk managers, and quantitative traders to evaluate Kelly leverage, compute VaR and Expected Shortfall, decompose Euler risk, analyze Almgren-Chriss market impact, model CVA/DVA exposure integrals, and stress test complex multi-asset portfolios.

## Learning objectives

- Calculate optimal position sizing under the discrete and continuous Kelly criterion, applying fractional Kelly scaling.
- Formulate and compute Parametric VaR and Expected Shortfall (CVaR) under normal and Student-t distributions.
- Implement Filtered Historical Simulation (FHS) to scale historical returns to prevailing volatility regimes.
- Execute forward and reverse stress testing across multi-asset portfolios.
- Evaluate expected maximum drawdown as an analytical function of annual Sharpe ratio, volatility, and trading horizon.
- Attribute derivatives portfolio P&L across Delta, Gamma, Theta, Vega, Vanna, and Volga, isolating unexplained residuals.
- Derive the break-even daily asset move for delta-hedged options under the Black-Scholes PDE.
- Execute Euler risk decomposition into Marginal VaR, Component VaR, and Equal Risk Contribution (Risk Parity).
- Generate counterparty exposure profiles: Expected Exposure (EE), Potential Future Exposure (PFE), and Effective EPE.
- Calculate bilateral Credit Valuation Adjustment (CVA) and Debit Valuation Adjustment (DVA) via numerical quadrature.
- Optimize execution trajectories under the Almgren-Chriss framework and compute Liquidity-Adjusted VaR (L-VaR).

## Core concepts

Key analytical formulas applied across this problem set:

- **Continuous Kelly Optimal Leverage:**

$$f^* = \frac{\mu - r}{\sigma^2} = \frac{S}{\sigma}$$

- **Parametric VaR and Expected Shortfall (Gaussian):**

$$\text{VaR}_{\alpha} = z_{\alpha} \sigma_p, \quad \text{ES}_{\alpha} = \frac{\phi(z_{\alpha})}{1 - \alpha} \sigma_p$$

- **Filtered Historical Simulation Scaling:**

$$r_{\tau}^{\text{filtered}} = r_{\tau} \times \frac{\sigma_{\text{current}}}{\sigma_{\tau}}$$

- **Expected Maximum Drawdown (Magdon-Ismail & Atiya):**

$$\mathbb{E}[\text{MDD}(T)] \approx \frac{\sigma}{2S} \left[ \ln\left( \frac{S^2 T}{2} \right) + 1.9635 \right]$$

- **Derivatives Greek P&L Attribution:**

$$\Delta \Pi = \Delta \cdot \Delta S + \frac{1}{2}\Gamma (\Delta S)^2 + \Theta \Delta t + \mathcal{V} \Delta \sigma + \text{Vanna} \Delta S \Delta \sigma + \frac{1}{2}\text{Volga} (\Delta \sigma)^2 + \epsilon$$

- **Black-Scholes Daily Break-Even Move:**

$$|\Delta S_{\text{break-even}}| = \sigma_{\text{imp}} S \sqrt{\Delta t} \approx \frac{\sigma_{\text{imp}}}{16} \times S$$

- **Euler Allocation: Marginal and Component VaR:**

$$\text{MVaR}_i = \beta_i \text{VaR}_p, \quad \text{CVaR}_i = w_i \text{MVaR}_i = w_i \beta_i \text{VaR}_p, \quad \sum_{i=1}^N \text{CVaR}_i = \text{VaR}_p$$

- **Counterparty Effective EPE:**

$$\text{EEE}(t_k) = \max(\text{EEE}(t_{k-1}), \text{EE}(t_k)), \quad \text{EEPE} = \frac{1}{1.0} \int_0^1 \text{EEE}(t) dt$$

- **Unilateral Credit Valuation Adjustment (CVA):**

$$\text{CVA} = (1 - R_C) \int_0^T P(0, t) \text{EE}^*(t) d\text{PD}_C(t)$$

- **Almgren-Chriss Optimal Trajectory:**

$$x(t) = X_0 \frac{\sinh(\kappa (T - t))}{\sinh(\kappa T)}, \quad \kappa = \sqrt{\frac{\lambda_{\text{risk}} \sigma^2}{\eta}}$$

- **Liquidity-Adjusted VaR (L-VaR):**

$$\text{L-VaR} = \text{VaR} \times \sqrt{1 + \frac{1}{3}(L - 1)} + \frac{1}{2}(\bar{S} + z_{\alpha}\sigma_S) V$$

## Worked examples

### Problem 1: Kelly Criterion and Position Sizing

A quantitative statistical arbitrage strategy has an expected annualized excess return of $\mu - r = 12.0\%$ ($0.120$) and an annualized return volatility of $\sigma = 16.0\%$ ($0.160$).
1. Compute the full Kelly optimal leverage fraction $f^*$.
2. To avoid high drawdown risk and parameter estimation error, the fund manager mandates a half-Kelly policy ($f_{\text{half}} = 0.5 f^*$). Compute the resulting portfolio expected return and volatility.
3. If an unconstrained trader uses full Kelly versus half Kelly, calculate the theoretical probability of suffering a $50\%$ drawdown before doubling capital.

**Solution:**

Step 1: Compute Full Kelly Leverage:

$$f^* = \frac{\mu - r}{\sigma^2} = \frac{0.120}{(0.160)^2} = \frac{0.120}{0.0256} = 4.6875 \quad (4.69\times \text{ leverage})$$

The strategy's annual Sharpe ratio is $S = 0.120 / 0.160 = 0.75$.
Full Kelly leverage equals $S / \sigma = 0.75 / 0.160 = 4.6875$.

Step 2: Half-Kelly Allocation and Portfolio Metrics:

$$f_{\text{half}} = 0.5 \times 4.6875 = 2.34375 \quad (2.34\times \text{ leverage})$$

Expected excess portfolio return:

$$\mu_p = f_{\text{half}} (\mu - r) = 2.34375 \times 0.120 = 0.28125 \quad (28.13\%)$$

Portfolio volatility:

$$\sigma_p = f_{\text{half}} \sigma = 2.34375 \times 0.160 = 0.3750 \quad (37.50\%)$$

Notice that expected excess growth rate is $g(f) = f \mu - \frac{1}{2} f^2 \sigma^2$:
- Full Kelly growth rate: $g(f^*) = \frac{S^2}{2} = \frac{0.75^2}{2} = 0.28125$ ($28.13\%$).
- Half-Kelly growth rate: $g(0.5 f^*) = \frac{3}{4} g(f^*) = 0.75 \times 0.28125 \approx 0.21094$ ($21.09\%$).
Half-Kelly captures $75\%$ of maximum compound growth while slashing variance by $75\%$ (volatility and leverage by $50\%$, since $\text{Var}(0.5 f^* \cdot r) = 0.25 \text{Var}(f^* \cdot r)$).

Step 3: Probability of a 50% Drawdown:
For a geometric Brownian motion under continuous trading at fraction $c = f / f^*$, the scale function exponent is $a = \frac{2}{c} - 1$:
- For full Kelly ($c = 1.0$), $a = 2(1) - 1 = 1$.
- For half-Kelly ($c = 0.5$), $a = \frac{2}{0.5} - 1 = 4 - 1 = 3$.

The probability of ever suffering a $50\%$ drawdown ($D = 0.50$) over an infinite horizon is $(1 - D)^a = (0.50)^a$:
- Full Kelly ($a = 1$): $(0.50)^1 = 50\%$.
- Half-Kelly ($a = 3$): $(0.50)^3 = 12.5\%$.

The probability of suffering a $50\%$ drawdown before doubling capital ($W \to 2 W_0$) satisfies the scale function ratio:

$$P(\text{Halving before Doubling}) = \frac{2^{-a} - 1}{2^{-a} - 2^a} = \frac{1}{2^a + 1}$$

- For full Kelly ($a = 1$): $P = \frac{1}{2^1 + 1} = \frac{1}{3} \approx 33.33\%$.
- For half-Kelly ($a = 3$): $P = \frac{1}{2^3 + 1} = \frac{1}{8 + 1} = \frac{1}{9} \approx 11.11\%$.

Trading half-Kelly slashes the probability of ever suffering a $50\%$ drawdown from $50\%$ down to $12.5\%$, and cuts the probability of halving before doubling from $33.3\%$ down to $11.1\%$.

---

### Problem 2: Parametric VaR vs. Expected Shortfall (CVaR)

A trading portfolio has a market value of $\$50,000,000$ and a daily return volatility of $\sigma_d = 1.20\%$ ($0.0120$).
Assume daily returns are normally distributed with zero mean ($\mu = 0$).
Compute the 1-day 99% Value at Risk (VaR) and the 1-day 99% Expected Shortfall (ES).

**Solution:**

Step 1: Daily standard deviation in dollars:

$$\sigma_{\$} = \$50,000,000 \times 0.0120 = \$600,000$$

Step 2: 99% VaR:
For confidence level $\alpha = 0.99$, the standard normal critical value is $z_{0.99} \approx 2.32635$:

$$\text{VaR}_{0.99} = z_{0.99} \times \sigma_{\$} = 2.32635 \times \$600,000 \approx \$1,395,810 \quad (2.79\%)$$

Step 3: 99% Expected Shortfall (ES):
For a standard normal distribution, Expected Shortfall is given by:

$$\text{ES}_{\alpha} = \frac{\phi(z_{\alpha})}{1 - \alpha} \times \sigma_{\$}$$

Evaluate standard normal density at $z = 2.32635$:

$$\phi(2.32635) = \frac{1}{\sqrt{2\pi}} e^{-0.5 \times (2.32635)^2} = 0.398942 \times e^{-2.70595} = 0.398942 \times 0.066807 \approx 0.026652$$

Evaluate multiplier:

$$\frac{\phi(z_{0.99})}{1 - 0.99} = \frac{0.026652}{0.0100} = 2.6652$$

Step 4: Compute dollar Expected Shortfall:

$$\text{ES}_{0.99} = 2.6652 \times \$600,000 = \$1,599,120 \quad (3.20\%)$$

Expected Shortfall exceeds VaR by $\$203,310$ ($14.6\%$), capturing the average severity of tail losses beyond the 99th percentile.

---

### Problem 3: Filtered Historical Simulation (FHS) Volatility Updating

A risk system evaluates an equity portfolio on valuation date $T$.
Today's prevailing market volatility estimated by EWMA is $\sigma_{\text{current}} = 2.20\%$ per day.
In the 250-day historical lookback window:
- Historical Day A: Observed return was $r_A = -3.00\%$, and estimated volatility was $\sigma_A = 1.00\%$.
- Historical Day B: Observed return was $r_B = -4.50\%$, and estimated volatility was $\sigma_B = 3.00\%$.
Compute the volatility-scaled filtered scenario returns $r_A^{\text{FHS}}$ and $r_B^{\text{FHS}}$, and contrast them with unscaled historical simulation.

**Solution:**

Step 1: Day A Filtered Return:
The historical event occurred during a low-volatility regime ($\sigma_A = 1.00\%$ vs current $2.20\%$):

$$r_A^{\text{FHS}} = r_A \times \frac{\sigma_{\text{current}}}{\sigma_A} = -0.0300 \times \frac{0.0220}{0.0100} = -0.0300 \times 2.20 = -0.0660 \quad (-6.60\%)$$

Step 2: Day B Filtered Return:
The historical event occurred during a high-volatility regime ($\sigma_B = 3.00\%$ vs current $2.20\%$):

$$r_B^{\text{FHS}} = r_B \times \frac{\sigma_{\text{current}}}{\sigma_B} = -0.0450 \times \frac{0.0220}{0.0300} = -0.0450 \times 0.7333 \approx -0.0330 \quad (-3.30\%)$$

Step 3: Comparison:
- Under unscaled historical simulation, Day B would be treated as the more severe risk scenario ($-4.50\%$ vs $-3.00\%$).
- Under Filtered Historical Simulation, Day A produces a dramatically larger shock ($-6.60\%$) because its historical $3$-sigma move is appropriately amplified to reflect today's volatile market conditions.

---

### Problem 4: Reverse Stress Testing

A proprietary trading desk has equity capital of $\$10,000,000$ and a mandatory firm liquidation stop if losses reach $\$2,500,000$ ($25\%$).
The portfolio has sensitivities to two principal risk factors:
- S&P 500 Equity Index return ($x_1$, daily vol $\sigma_1 = 1.0\%$).
- 10-year Treasury yield change in bps ($x_2$, daily vol $\sigma_2 = 8 \text{ bps}$).
- Correlation between S&P 500 and 10y yields: $\rho = +0.20$.
The portfolio P&L function is:

$$\text{P\&L}(x_1, x_2) = \$20,000,000 \cdot x_1 - \$50,000 \cdot x_2$$

Find the most plausible shock vector $(x_1^*, x_2^*)$ (minimizing Mahalanobis statistical distance $d^2 = \mathbf{x}^T \mathbf{\Sigma}^{-1} \mathbf{x}$) that triggers the $\$2,500,000$ liquidation stop.

**Solution:**

Step 1: Express standardized variables:
Let $u_1 = x_1 / \sigma_1 = x_1 / 0.010$ and $u_2 = x_2 / \sigma_2 = x_2 / 8.0$.
The correlation matrix is:

$$\mathbf{R} = \begin{pmatrix} 1.0 & 0.20 \\ 0.20 & 1.0 \end{pmatrix} \implies \mathbf{R}^{-1} = \frac{1}{1 - 0.20^2} \begin{pmatrix} 1.0 & -0.20 \\ -0.20 & 1.0 \end{pmatrix} = \frac{1}{0.96} \begin{pmatrix} 1.0 & -0.20 \\ -0.20 & 1.0 \end{pmatrix}$$

The P&L constraint is:

$$\text{P\&L} = \$20,000,000(0.010 u_1) - \$50,000(8.0 u_2) = \$200,000 u_1 - \$400,000 u_2 = -\$2,500,000$$

Dividing by $\$100,000$:

$$2 u_1 - 4 u_2 = -25 \implies u_1 - 2 u_2 = -12.5$$

Step 2: Solve constrained optimization using Lagrange multipliers:
Minimize $\frac{1}{2}\mathbf{u}^T \mathbf{R}^{-1} \mathbf{u}$ subject to $\mathbf{c}^T \mathbf{u} = -12.5$ where $\mathbf{c} = [1.0, -2.0]^T$:
The optimal shock vector satisfies:

$$\mathbf{u}^* = \lambda \mathbf{R} \mathbf{c} = \lambda \begin{pmatrix} 1.0 & 0.20 \\ 0.20 & 1.0 \end{pmatrix} \begin{pmatrix} 1.0 \\ -2.0 \end{pmatrix} = \lambda \begin{pmatrix} 1.0 - 0.40 \\ 0.20 - 2.0 \end{pmatrix} = \lambda \begin{pmatrix} 0.60 \\ -1.80 \end{pmatrix}$$

Substitute into constraint $\mathbf{c}^T \mathbf{u}^* = -12.5$:

$$\begin{pmatrix} 1.0 & -2.0 \end{pmatrix} \left[ \lambda \begin{pmatrix} 0.60 \\ -1.80 \end{pmatrix} \right] = \lambda (0.60 + 3.60) = 4.20 \lambda = -12.5 \implies \lambda = \frac{-12.5}{4.20} \approx -2.97619$$

Step 3: Compute standardized shocks:

$$u_1^* = -2.97619 \times 0.60 \approx -1.7857$$

$$u_2^* = -2.97619 \times (-1.80) \approx +5.3571$$

Step 4: Convert back to actual financial market variables:

$$x_1^* = u_1^* \times \sigma_1 = -1.7857 \times 0.010 \approx -0.01786 \quad (-1.79\% \text{ S\&P 500 drop})$$

$$x_2^* = u_2^* \times \sigma_2 = +5.3571 \times 8.0 \approx +42.86 \text{ bps} \quad (+42.9 \text{ bp yield jump})$$

Reverse stress testing reveals that the path of least statistical resistance to firm insolvency is not a pure stock crash, but a simultaneous $-1.79\%$ equity decline paired with an acute $+42.9$ bp surge in 10-year yields (e.g., an unexpected inflation shock).

---

### Problem 5: Expected Maximum Drawdown Analytics

A quantitative macro hedge fund achieves an annualized Sharpe ratio of $S = 1.20$ with annualized volatility $\sigma = 12.0\%$.
1. Compute the expected maximum drawdown over a 2-year horizon ($T = 2.0$).
2. Compute the expected maximum drawdown over a 10-year horizon ($T = 10.0$).
3. If strategy drift drops to zero ($\mu = 0$, unhedged random walk), compute the expected drawdown over 2 years.

**Solution:**

Step 1: Compute 2-Year Expected Maximum Drawdown:
Using the Magdon-Ismail and Atiya (2004) asymptotic formula with positive drift:

$$\mathbb{E}[\text{MDD}] \approx \frac{\sigma}{2S} \left[ \ln\left( \frac{S^2 T}{2} \right) + 1.9635 \right]$$

where $\frac{\sigma}{2S} = \frac{0.120}{2 \times 1.20} = \frac{0.120}{2.40} = 0.050 \quad (5.0\%)$.
For $T = 2.0$:

$$\frac{S^2 T}{2} = \frac{1.20^2 \times 2.0}{2} = 1.44 \implies \ln(1.44) \approx 0.36464$$

$$\mathbb{E}[\text{MDD}(2y)] \approx 0.050 \times (0.36464 + 1.9635) = 0.050 \times 2.32814 \approx 0.11641 \quad (11.64\%)$$

Step 2: Compute 10-Year Expected Maximum Drawdown:
For $T = 10.0$:

$$\frac{S^2 T}{2} = \frac{1.20^2 \times 10.0}{2} = 7.20 \implies \ln(7.20) \approx 1.97408$$

$$\mathbb{E}[\text{MDD}(10y)] \approx 0.050 \times (1.97408 + 1.9635) = 0.050 \times 3.93758 \approx 0.19688 \quad (19.69\%)$$

Step 3: Zero-Drift Regime ($\mu = 0$):

$$\mathbb{E}[\text{MDD}_{\mu=0}(2y)] \approx \sqrt{\frac{\pi}{2}} \cdot \sigma \sqrt{T} \approx 1.2533 \times 0.120 \times \sqrt{2.0} \approx 1.2533 \times 0.120 \times 1.4142 \approx 0.2127 \quad (21.27\%)$$

Without positive drift, expected drawdown jumps from $11.6\%$ to $21.3\%$.

---

### Problem 6: Derivatives Greek P&L Attribution

An equity options portfolio on stock $ABC$ ($S = \$50.00$) has the following Greeks at start of day:
- $\Delta = +10,000$ shares ($+\$500,000$ delta notional)
- $\Gamma = +2,500$ per $\$1$ stock move
- $\Theta = -\$850$ per day ($\Delta t = 1/252$)
- $\mathcal{V} = +\$4,000$ per $1\%$ vol point ($+\$400,000$ per unit vol)
- $\text{Vanna} = +\$15,000$ per $\$1$ stock move per unit vol
- $\text{Volga} = +\$800,000$ per unit vol squared
During the trading session:
- Stock price increases by $+\$2.00$ ($\Delta S = +2.00$).
- Implied volatility drops by $-2.50$ percentage points ($\Delta \sigma = -0.0250$).
- Total actual realized P&L is $\Delta \Pi_{\text{actual}} = +\$14,200$.
Decompose P&L across all Greek components and compute the unexplained residual $\epsilon$.

**Solution:**

Step 1: Compute Greek contributions:
- Delta P&L:

$$\Delta \Pi_{\text{Delta}} = 10,000 \times (+2.00) = +\$20,000.00$$

- Gamma P&L:

$$\Delta \Pi_{\text{Gamma}} = \frac{1}{2} \times 2,500 \times (2.00)^2 = 1,250 \times 4.0 = +\$5,000.00$$

- Theta P&L:

$$\Delta \Pi_{\text{Theta}} = -\$850.00$$

- Vega P&L:

$$\Delta \Pi_{\text{Vega}} = \$400,000 \times (-0.0250) = -\$10,000.00$$

- Vanna P&L:

$$\Delta \Pi_{\text{Vanna}} = \$15,000 \times (+2.00) \times (-0.0250) = -\$750.00$$

- Volga P&L:

$$\Delta \Pi_{\text{Volga}} = \frac{1}{2} \times \$800,000 \times (-0.0250)^2 = \$400,000 \times 0.000625 = +\$250.00$$

Step 2: Sum Predicted P&L:

$$\Delta \Pi_{\text{predicted}} = \$20,000 + \$5,000 - \$850 - \$10,000 - \$750 + \$250 = +\$13,650.00$$

Step 3: Compute Unexplained Residual ($\epsilon$):

$$\epsilon = \Delta \Pi_{\text{actual}} - \Delta \Pi_{\text{predicted}} = \$14,200.00 - \$13,650.00 = +\$550.00$$

The unexplained residual is $+\$550$ (only $3.9\%$ of total P&L), confirming accurate attribution.

---

### Problem 7: Black-Scholes PDE Theta vs. Gamma Break-Even

A quantitative options trader holds a delta-neutral, long gamma position on the S&P 500 index ETF ($SPY$, trading at $S = \$500.00$).
The position gamma is $\Gamma = +800$ per $\$1$ move.
The implied volatility of the options is $\sigma_{\text{imp}} = 18.0\%$ ($0.180$).
1. Using the Black-Scholes PDE identity ($\Theta + \frac{1}{2}\sigma_{\text{imp}}^2 S^2 \Gamma = 0$), compute the daily dollar theta decay ($\Delta t = 1/252$).
2. Compute the exact 1-day break-even move $|\Delta S_{\text{break-even}}|$ required to offset theta.
3. Verify the Rule of 16 approximation $|\Delta S| \approx \frac{\sigma_{\text{imp}}}{16} S$.

**Solution:**

Step 1: Compute Daily Theta Decay:

$$\Theta_{\text{annual}} = -\frac{1}{2}\sigma_{\text{imp}}^2 S^2 \Gamma = -\frac{1}{2}(0.180)^2 \times (500)^2 \times 800$$

$$(0.180)^2 = 0.0324, \quad 500^2 = 250,000$$

$$\Theta_{\text{annual}} = -\frac{1}{2} \times 0.0324 \times 250,000 \times 800 = -0.5 \times 8,100 \times 800 = -\$3,240,000 \text{ per year}$$

Daily theta decay ($\Delta t = 1/252$):

$$\Theta_{\text{daily}} = \frac{-\$3,240,000}{252} \approx -\$12,857.14 \text{ per day}$$

Step 2: Compute Exact Break-Even Price Move:
Setting $\frac{1}{2}\Gamma (\Delta S)^2 + \Theta_{\text{daily}} = 0$:

$$\frac{1}{2} \times 800 \times (\Delta S)^2 = \$12,857.14 \implies 400 (\Delta S)^2 = \$12,857.14$$

$$(\Delta S)^2 = \frac{12,857.14}{400} \approx 32.14285 \implies |\Delta S_{\text{break-even}}| = \sqrt{32.14285} \approx \$5.6695$$

Step 3: Verify Rule of 16:

$$|\Delta S_{\text{Rule of 16}}| \approx \frac{\sigma_{\text{imp}}}{16} \times S = \frac{0.180}{16} \times \$500.00 = 0.01125 \times \$500.00 = \$5.6250$$

The Rule of 16 estimate ($\$5.63$) matches the exact PDE break-even move ($\$5.67$) within $0.8\%$.

---

### Problem 8: Euler Risk Allocation and Component VaR

A portfolio consists of two asset classes:
- Asset 1: Value $w_1 = \$80,000,000$, annual volatility $\sigma_1 = 15.0\%$.
- Asset 2: Value $w_2 = \$20,000,000$, annual volatility $\sigma_2 = 25.0\%$.
- Correlation: $\rho = +0.40$.
- Confidence level: 95% ($z_{0.95} = 1.6449$).
Compute total portfolio volatility, 95% portfolio VaR, Marginal VaRs, Component VaRs, and verify that the sum of Component VaRs equals total VaR.

**Solution:**

Step 1: Portfolio weights and variance:
Total portfolio value $V = \$100,000,000$, weights $x_1 = 0.80$, $x_2 = 0.20$:

$$\sigma_p^2 = x_1^2 \sigma_1^2 + x_2^2 \sigma_2^2 + 2 x_1 x_2 \rho \sigma_1 \sigma_2$$

$$x_1^2 \sigma_1^2 = 0.80^2 \times 0.15^2 = 0.64 \times 0.0225 = 0.014400$$

$$x_2^2 \sigma_2^2 = 0.20^2 \times 0.25^2 = 0.04 \times 0.0625 = 0.002500$$

$$2 x_1 x_2 \rho \sigma_1 \sigma_2 = 2(0.80)(0.20)(0.40)(0.15)(0.25) = 0.128 \times 0.0375 = 0.004800$$

$$\sigma_p^2 = 0.014400 + 0.002500 + 0.004800 = 0.021700$$

$$\sigma_p = \sqrt{0.021700} \approx 0.147309 \quad (14.73\%)$$

Total portfolio VaR:

$$\text{VaR}_p = \$100,000,000 \times 1.6449 \times \sqrt{0.021700} \approx \$24,230,890 \quad (24.23\%)$$

Step 2: Covariances and Betas:

$$\text{Cov}(r_1, r_p) = x_1 \sigma_1^2 + x_2 \rho \sigma_1 \sigma_2 = (0.80 \times 0.0225) + (0.20 \times 0.40 \times 0.15 \times 0.25) = 0.01800 + 0.00300 = 0.02100$$

$$\text{Cov}(r_2, r_p) = x_2 \sigma_2^2 + x_1 \rho \sigma_1 \sigma_2 = (0.20 \times 0.0625) + (0.80 \times 0.40 \times 0.15 \times 0.25) = 0.01250 + 0.01200 = 0.02450$$

$$\beta_1 = \frac{0.02100}{0.021700} \approx 0.967742$$

$$\beta_2 = \frac{0.02450}{0.021700} \approx 1.129032$$

Step 3: Marginal VaRs:

$$\text{MVaR}_1 = \beta_1 \text{VaR}_p = 0.967742 \times \$24,230,890 \approx \$23,449,248 \quad (23.45\%)$$

$$\text{MVaR}_2 = \beta_2 \text{VaR}_p = 1.129032 \times \$24,230,890 \approx \$27,357,457 \quad (27.36\%)$$

Step 4: Component VaRs:

$$\text{CVaR}_1 = x_1 \times \text{MVaR}_1 = 0.80 \times \$23,449,248 \approx \$18,759,399$$

$$\text{CVaR}_2 = x_2 \times \text{MVaR}_2 = 0.20 \times \$27,357,457 \approx \$5,471,491$$

Step 5: Euler Verification:

$$\text{Sum} = \$18,759,399 + \$5,471,491 = \$24,230,890 = \text{VaR}_p$$

The Euler condition holds with exact equality.

---

### Problem 9: Almgren-Chriss Optimal Liquidation Trajectory

A hedge fund must liquidate $X_0 = 500,000$ shares of a stock over $T = 3$ days.
Parameters:
- Price $S_0 = \$100.00$.
- Daily volatility $\sigma = \$2.00$ ($2.0\%$).
- Temporary impact parameter $\eta = 2.0 \times 10^{-6}$ per share per day.
- Risk aversion parameter $\lambda_{\text{risk}} = 2.0 \times 10^{-6}$.
1. Compute the urgency parameter $\kappa$.
2. Calculate the optimal shares remaining at the end of Day 1 and Day 2.
3. Compute the shares sold each day.

**Solution:**

Step 1: Compute $\kappa$:

$$\kappa = \sqrt{\frac{\lambda_{\text{risk}} \sigma^2}{\eta}} = \sqrt{\frac{2.0 \times 10^{-6} \times (2.0)^2}{2.0 \times 10^{-6}}} = \sqrt{4.0} = 2.00 \text{ day}^{-1}$$

Step 2: Compute Hyperbolic Sines:

$$\sinh(\kappa T) = \sinh(2.0 \times 3) = \sinh(6.0) = \frac{e^6 - e^{-6}}{2} = \frac{403.428793 - 0.002479}{2} \approx 201.7132$$

- At $t = 1$ (end of Day 1): $\kappa(T - t) = 2.0(3 - 1) = 4.0$:

$$\sinh(4.0) = \frac{e^4 - e^{-4}}{2} = \frac{54.598150 - 0.018316}{2} \approx 27.2899$$

$$x(1) = 500,000 \times \frac{27.2899}{201.7132} \approx 67,645 \text{ shares remaining}$$

- At $t = 2$ (end of Day 2): $\kappa(T - t) = 2.0(3 - 2) = 2.0$:

$$\sinh(2.0) = \frac{e^2 - e^{-2}}{2} = \frac{7.389056 - 0.135335}{2} \approx 3.6269$$

$$x(2) = 500,000 \times \frac{3.6269}{201.7132} \approx 8,990 \text{ shares remaining}$$

Step 3: Daily Execution Quantities:
- Day 1 Sales: $500,000 - 67,645 = 432,355$ shares ($86.5\%$ of position).
- Day 2 Sales: $67,645 - 8,990 = 58,655$ shares ($11.7\%$ of position).
- Day 3 Sales: $8,990 - 0 = 8,990$ shares ($1.8\%$ of position).
Due to high risk aversion ($\kappa = 2.0$), the trader aggressively front-loads execution to eliminate market risk.

---

### Problem 10: Liquidity-Adjusted VaR (L-VaR)

A fund holds $\$30,000,000$ in an emerging market sovereign bond.
- Standard 1-day 99% VaR: $\text{VaR}_{1\text{d}} = \$1,500,000$.
- Average bid-ask spread: $\bar{S} = 1.20\%$ ($0.0120$).
- Standard deviation of bid-ask spread: $\sigma_S = 0.60\%$ ($0.0060$).
- Confidence level: 99% ($z_{0.99} = 2.326$).
- Position represents 3 days of orderly liquidation ($L = 3$).
Compute total Liquidity-Adjusted VaR.

**Solution:**

Step 1: Compute Exogenous Bid-Ask Spread Cost:

$$\text{Spread Cost} = \frac{1}{2} (\bar{S} + z_{0.99} \sigma_S) \times \text{Portfolio Value}$$

$$\bar{S} + z_{0.99} \sigma_S = 0.0120 + 2.326(0.0060) = 0.0120 + 0.013956 = 0.025956 \quad (2.60\%)$$

$$\text{Spread Cost} = \frac{1}{2} \times 0.025956 \times \$30,000,000 = \$389,340$$

Step 2: Liquidation Horizon Scaling ($L = 3$ days):

$$\text{Multiplier} = \sqrt{1 + \frac{1}{3}(L - 1)} = \sqrt{1 + \frac{1}{3}(2)} = \sqrt{\frac{5}{3}} \approx 1.29099$$

$$\text{Scaled VaR} = \$1,500,000 \times 1.29099 \approx \$1,936,492$$

Step 3: Total Liquidity-Adjusted VaR:

$$\text{L-VaR} = \$1,936,492 + \$389,340 = \$2,325,832$$

Liquidity friction and multi-day execution expand calculated risk by $\$825,832$ ($+55.1\%$).

---

### Problem 11: Counterparty Exposure Profiles and Effective EPE

A 5-year payer interest rate swap has the following simulated Expected Exposure (EE) profile:
- Year 0.0: $EE(0) = \$0$
- Year 0.5: $EE(0.5) = \$80,000$
- Year 1.0: $EE(1.0) = \$120,000$
- Year 2.0: $EE(2.0) = \$160,000$ (Peak hump)
- Year 3.0: $EE(3.0) = \$130,000$
- Year 4.0: $EE(4.0) = \$80,000$
- Year 5.0: $EE(5.0) = \$0$
1. Construct the Effective Expected Exposure (EEE) profile across all years.
2. Compute the 1-year Effective EPE ($\text{EEPE}$).
3. Compute the Basel IMM Exposure at Default ($\text{EAD} = 1.4 \times \text{EEPE}$).

**Solution:**

Step 1: Construct Effective EE (non-decreasing envelope):
- Year 0.0: $EEE(0) = \$0$
- Year 0.5: $\max(0, 80,000) = \$80,000$
- Year 1.0: $\max(80k, 120k) = \$120,000$
- Year 2.0: $\max(120k, 160k) = \$160,000$
- Year 3.0: $\max(160k, 130k) = \$160,000$ (pinned at peak)
- Year 4.0: $\max(160k, 80k) = \$160,000$ (pinned at peak)
- Year 5.0: $\max(160k, 0) = \$160,000$ (pinned at peak)

Step 2: Compute 1-Year Effective EPE ($\text{EEPE}$):
Integrating EEE over $[0, 1.0]$ using trapezoidal approximation:

$$\text{EEPE} = \frac{1}{1.0} \left[ 0.5 \times \frac{0 + 80,000}{2} + 0.5 \times \frac{80,000 + 120,000}{2} \right] = 0.5(40,000) + 0.5(100,000) = 20,000 + 50,000 = \$70,000$$

Step 3: Compute Regulatory EAD:

$$\text{EAD} = 1.4 \times \text{EEPE} = 1.4 \times \$70,000 = \$98,000$$

---

### Problem 12: Bilateral CVA and DVA Calculation

An uncollateralized 1-year derivative contract has average Expected Exposure $\text{EE} = \$500,000$ and average Expected Negative Exposure $\text{ENE} = \$300,000$.
- Flat risk-free rate: $r = 4.00\%$ ($P(0, 0.5) = e^{-0.02} \approx 0.9802$).
- Counterparty hazard rate: $\lambda_C = 3.00\%$ per annum, recovery $R_C = 40\%$ ($LGD_C = 0.60$).
- Bank hazard rate: $\lambda_B = 1.50\%$ per annum, recovery $R_B = 40\%$ ($LGD_B = 0.60$).
Calculate unilateral CVA, DVA, and Net Bilateral Adjustment over the 1-year horizon.

**Solution:**

Step 1: Compute 1-year default probabilities:

$$\text{PD}_C(1) = 1 - e^{-\lambda_C \times 1} = 1 - e^{-0.030} \approx 1 - 0.970446 = 0.029554 \quad (2.96\%)$$

$$\text{PD}_B(1) = 1 - e^{-\lambda_B \times 1} = 1 - e^{-0.015} \approx 1 - 0.985112 = 0.014888 \quad (1.49\%)$$

Step 2: Compute Unilateral CVA:

$$\text{CVA} \approx (1 - R_C) \times P(0, 0.5) \times \text{EE} \times \text{PD}_C(1)$$

$$\text{CVA} \approx 0.60 \times 0.9802 \times \$500,000 \times 0.029554 \approx \$294.06 \times 29.554 \approx \$8,690.65$$

Step 3: Compute DVA:

$$\text{DVA} \approx (1 - R_B) \times P(0, 0.5) \times \text{ENE} \times \text{PD}_B(1)$$

$$\text{DVA} \approx 0.60 \times 0.9802 \times \$300,000 \times 0.014888 \approx \$176.436 \times 14.888 \approx \$2,626.78$$

Step 4: Net Bilateral Adjustment:

$$\text{Net Adjustment} = \text{DVA} - \text{CVA} = \$2,626.78 - \$8,690.65 = -\$6,063.87$$

The net fair value deduction is $\$6,063.87$.

---

### Problem 13: PCA Yield Curve Factor Shocks

A 3-factor PCA decomposition of a yield curve produces eigenvalues $\lambda_1 = 0.000180$, $\lambda_2 = 0.000018$, $\lambda_3 = 0.000002$.
1. Compute the percentage of total yield curve variance explained by each principal component.
2. The Level eigenvector is $\mathbf{v}_1 = [0.577, 0.577, 0.577]^T$. Compute the basis point shock across all three tenors for a $+1.5$-standard-deviation Level move.

**Solution:**

Step 1: Percentage Variance Explained:
Total variance:

$$\Lambda_{\text{total}} = 0.000180 + 0.000018 + 0.000002 = 0.000200$$

- PC1 (Level): $\frac{0.000180}{0.000200} = 0.9000$ ($90.0\%$)
- PC2 (Slope): $\frac{0.000018}{0.000200} = 0.0900$ ($9.0\%$)
- PC3 (Curvature): $\frac{0.000002}{0.000200} = 0.0100$ ($1.0\%$)
Together, the three components explain 100% of the variance.

Step 2: Level Factor Shock:
Standard deviation of Level factor:

$$\sigma_1 = \sqrt{\lambda_1} = \sqrt{0.000180} \approx 0.013416 \quad (134.16 \text{ bps})$$

For $z_1 = +1.50$:

$$\Delta \mathbf{y} = z_1 \sigma_1 \mathbf{v}_1 = 1.50 \times 0.013416 \times \begin{pmatrix} 0.577 \\ 0.577 \\ 0.577 \end{pmatrix} \approx 0.020125 \times \begin{pmatrix} 0.577 \\ 0.577 \\ 0.577 \end{pmatrix} \approx \begin{pmatrix} 0.01161 \\ 0.01161 \\ 0.01161 \end{pmatrix}$$

The $+1.5$-sigma level shock produces a uniform parallel upward shift of $+116.1$ basis points across all tenors.

---

### Problem 14: Funding Valuation Adjustment (FVA)

A dealer enters an uncollateralized 3-year interest rate swap with a corporate client having Expected Exposure $\text{EE} = \$400,000$.
The dealer hedges in the interdealer market under a zero-threshold CSA requiring cash variation margin.
The dealer's unsecured borrowing funding spread over OIS is $s_{\text{funding}} = 75 \text{ bps/year} = 0.0075$.
The average 3-year discount factor is $P(0, 1.5) \approx 0.945$.
Compute the Funding Cost Adjustment (FCA).

**Solution:**

Step 1: Compute FCA:

$$\text{FCA} \approx s_{\text{funding}} \times \text{EE} \times P(0, T/2) \times T$$

$$\text{FCA} \approx 0.0075 \times \$400,000 \times 0.945 \times 3.0 = \$3,000 \times 2.835 = \$8,505.00$$

The dealer must deduct $\$8,505$ from the trade's present value to cover the funding cost of posting collateral on the offsetting hedge.

---

### Problem 15: Margin Valuation Adjustment (MVA)

Under Uncleared Margin Rules (UMR), a bank must post bilateral segregated Initial Margin on an uncollateralized exotic derivative portfolio.
- Average simulated Initial Margin over 5 years: $\mathbb{E}[\text{IM}] = \$2,000,000$.
- Cost of raising term liquidity to fund segregated IM: $s_{\text{margin}} = 1.20\%$ per annum ($0.0120$).
- Average discount factor: $P(0, 2.5) \approx 0.910$.
Compute the lifetime Margin Valuation Adjustment (MVA).

**Solution:**

Step 1: Compute MVA:

$$\text{MVA} \approx s_{\text{margin}} \times \mathbb{E}[\text{IM}] \times P(0, 2.5) \times T$$

$$\text{MVA} \approx 0.0120 \times \$2,000,000 \times 0.910 \times 5.0 = \$24,000 \times 4.550 = \$109,200.00$$

The dealer charges $\$109,200$ upfront to cover the lifetime interest drag of funding the regulatory initial margin requirement.

---

### Problem 16: Capital Valuation Adjustment (KVA)

A 5-year derivative trade requires the bank to hold an average regulatory capital balance of $\mathbb{E}[\text{Capital}] = \$500,000$ to cover SA-CCR credit risk and CVA capital.
The bank's equity shareholders demand a hurdle return on equity (Cost of Capital) of $\text{CoC} = 10.0\%$ per annum ($0.100$).
Average discount factor is $P(0, 2.5) \approx 0.910$.
Calculate the Capital Valuation Adjustment (KVA).

**Solution:**

Step 1: Compute KVA:

$$\text{KVA} \approx \text{CoC} \times \mathbb{E}[\text{Capital}] \times P(0, 2.5) \times T$$

$$\text{KVA} \approx 0.100 \times \$500,000 \times 0.910 \times 5.0 = \$50,000 \times 4.550 = \$227,500.00$$

The bank must charge $\$227,500$ upfront to provide shareholders with their required 10% return on regulatory capital over the trade life.

## Pitfalls

- **Confusing Full Kelly with Realistic Sizing:** Applying full Kelly leverage without parameter uncertainty buffers leads to catastrophic drawdowns and near-certain ruin in fat-tailed markets.
- **Assuming Constant Exposure in CVA Calculations:** Using current mark-to-market instead of full stochastic Expected Exposure profiles drastically misstates CVA on amortizing or diffusing swaps.
- **Ignoring Netting Set Boundaries in XVA Pricing:** Pricing XVA trade by trade rather than on an incremental netting set basis miscalculates risk and leads to uncompetitive client quotes.
- **Treating Model Output as Ground Truth:** Assuming mathematical models fully capture market reality without independent validation and boundary testing invites catastrophic model risk.
- **Ignoring Margin Liquidity in Delta-Hedged Portfolios:** Assuming a delta-neutral book has zero risk while ignoring variation margin cash drains during market gaps leads to forced liquidation.

## Interview questions

> [!question]- risk-full-vs-half-kelly-drawdown | Why do professional quants recommend trading at half-Kelly rather than full Kelly?
> Full Kelly maximizes the expected compound growth rate of capital in the infinite horizon, but suffers from extreme volatility: it has a 50% probability of ever suffering a 50% drawdown and a 33.3% probability of halving before doubling capital. Half-Kelly achieves 75% of maximum compound growth rate while cutting variance by 75% (volatility and leverage by 50%), slashes the probability of ever suffering a 50% drawdown down to 12.5%, and reduces the probability of halving before doubling to 11.1%, providing a massive safety buffer against parameter estimation error.

> [!question]- risk-var-vs-es-coherence | Why is Expected Shortfall (ES) a coherent risk measure while Value at Risk (VaR) is not?
> Value at Risk fails the subadditivity axiom: the VaR of a combined portfolio can exceed the sum of individual VaRs ($\text{VaR}(X + Y) > \text{VaR}(X) + \text{VaR}(Y)$) for non-normal or skewed distributions, meaning VaR can penalize diversification. Expected Shortfall (CVaR) satisfies subadditivity, translation invariance, positive homogeneity, and monotonicity, making it a mathematically coherent risk measure that accurately captures tail risk.

> [!question]- risk-euler-allocation-homogeneity | State the mathematical condition required for Euler risk allocation to hold, and identify which risk measures qualify.
> Euler allocation requires that the risk measure $\rho(\mathbf{w})$ be linearly homogeneous of degree 1: $\rho(c \mathbf{w}) = c \rho(\mathbf{w})$ for any $c > 0$. Portfolio standard deviation, Parametric VaR, and Expected Shortfall are degree-1 homogeneous, guaranteeing that the sum of Component Risks equals total portfolio risk exactly: $\sum w_i \frac{\partial \rho}{\partial w_i} = \rho(\mathbf{w})$.

> [!question]- risk-almgren-chriss-urgency-parameter | In the Almgren-Chriss framework, what does the urgency parameter $\kappa = \sqrt{\lambda_{\text{risk}} \sigma^2 / \eta}$ dictate?
> The urgency parameter $\kappa$ dictates the rate of trade liquidation. When risk aversion $\lambda_{\text{risk}}$ or asset volatility $\sigma^2$ is high relative to temporary impact cost $\eta$, $\kappa$ is large: the execution schedule aggressively front-loads sales to eliminate price volatility timing risk. When risk aversion is zero, $\kappa \to 0$ and the schedule collapses to a linear TWAP execution.

> [!question]- risk-swap-vs-forward-exposure-geometry | Contrast the Expected Exposure profile of an interest rate swap with that of an FX forward contract.
> An FX forward contract exhibits monotonically expanding exposure over time because no interim payments occur and underlying exchange rate variance grows proportional to $\sqrt{t}$. An interest rate swap exhibits a "hump-shaped" exposure profile: rate diffusion expands uncertainty early, but the remaining coupon annuity $A(t)$ amortizes toward zero at maturity, causing exposure to peak mid-life and drop to zero at final maturity.

> [!question]- risk-effective-epe-definition | What is Effective EPE under the Basel framework, and why was it introduced?
> Effective EPE is the time-weighted average of Effective Expected Exposure ($\text{EEE}$) over the first year of a derivative contract, where $\text{EEE}(t) = \max(\text{EEE}(t - \Delta t), \text{EE}(t))$ enforces a non-decreasing envelope. It was introduced to prevent banks from artificially understating regulatory capital as short-dated contracts roll off, reflecting the commercial reality that banks continually replace maturing client hedges.

> [!question]- risk-dva-paradox-accounting | Explain the DVA paradox and why it creates controversial accounting profits.
> Debit Valuation Adjustment (DVA) measures the expected profit to a bank if it defaults on its own negative mark-to-market liabilities. When a bank's credit rating is downgraded and its CDS spread widens, its cumulative default probability increases, causing DVA to expand. Under fair-value accounting (IFRS 13), this requires the bank to record mark-to-market accounting profits, artificially inflating earnings precisely when the institution is in severe distress.

> [!question]- risk-fva-mechanics-dealer | Why does an uncollateralized client swap hedged with a collateralized interdealer swap generate FVA?
> When market rates move against the street hedge, the dealer must post cash variation margin to the clearing broker. Because the uncollateralized corporate client posts no collateral, the dealer must borrow cash from its internal treasury at an unsecured funding spread over OIS ($r_{\text{OIS}} + s_{\text{funding}}$). The dealer posts this cash and earns only OIS, incurring a continuous funding drag equal to $s_{\text{funding}} \times \text{Exposure}$, which is priced as FVA.

> [!question]- risk-mva-regulatory-driver | What regulatory development made Margin Valuation Adjustment (MVA) an essential pricing component?
> The implementation of the global Uncleared Margin Rules (UMR) by the BCBS-IOSCO framework mandated that financial institutions post bilateral, segregated Initial Margin (IM) on non-cleared derivatives. Because initial margin is locked in third-party custodian accounts and cannot be reused, dealers must raise term funding to maintain these multi-million dollar reserves, creating lifetime financing costs priced as MVA.

> [!question]- risk-sr-11-7-three-lines-of-defense | What are the responsibilities of the Second Line of Defense under Federal Reserve SR 11-7?
> Under SR 11-7, the Second Line of Defense is the independent Model Risk Management / Validation group. It is organizationally separate from trading desks and is responsible for providing unbiased "effective challenge" to model designs, independently verifying mathematical derivations, replicating code, benchmarking against challenger models, testing boundary stress conditions, and maintaining the firm's authoritative Model Inventory.

## Further reading

- Philippe Jorion, *Value at Risk: The New Benchmark for Managing Financial Risk*, Chapters 1-15.
- Jon Gregory, *Counterparty Credit Risk and Credit Value Adjustment*, 3rd Edition, Chapters 1-12.
- Robert Carver, *Systematic Trading: A Unique New Method for Designing Trading and Investing Systems*.
- Robert Almgren and Neil Chriss (2000), "Optimal Execution of Portfolio Transactions", *Journal of Risk*.
- Sheldon Natenberg, *Option Volatility and Pricing*, Chapters 6-12.

## In this repo and SDE-Interview-Prep

- Python reference implementation of exposure profiles and XVA: [exposure_xva.py](code/exposure_xva.py).
- Python reference implementation of risk analytics and bumping: [risk_analytics.py](code/risk_analytics.py).
- Counterparty credit risk analytics: [Counterparty Credit Risk Analytics](14-Counterparty-Credit-Risk-Analytics.md).
- XVA framework: [XVA](15-XVA.md).
- Liquidity and model risk: [Liquidity and Model Risk](16-Liquidity-and-Model-Risk.md).
