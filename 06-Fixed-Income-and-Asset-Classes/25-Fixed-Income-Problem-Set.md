---
type: problem-set
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: solid
prereqs: [credit-advanced-cds-indices-and-tranches, fixed-income-pnl-and-relative-value]
est_hours: 8
sources: [Bruce Tuckman and Angel Serrat - Fixed Income Securities 3rd edition - Wiley 2012, Damiano Brigo and Fabio Mercurio - Interest Rate Models 2nd edition - Springer 2006, John Hull - Options Futures and Other Derivatives, David X. Li - On Default Correlation - A Copula Function Approach - Journal of Fixed Income 2000]
---

# Fixed Income Comprehensive Problem Set

## TL;DR

- Twenty-two worked problems across cash bonds, curves, swaps, short-rate and term structure models, options and SABR, CDS and tranches, inflation, mortgages and relative value.
- Each problem shows the working as you would say it in an interview, and [`code/fi_problem_set.py`](code/fi_problem_set.py) recomputes and asserts every number, with an independent check where one exists (repricing, parity, quadrature, round trips).
- The habits that matter: state the compounding and day-count convention, sanity-check the sign and size, and know which shortcut (credit triangle, ATM normal-vol conversion, carry over DV01) is accurate to what.

## Learning objectives

- Price fixed-coupon bonds, distinguish clean from dirty prices, and calculate accrued interest under Actual/Actual conventions.
- Derive and calculate Macaulay duration, modified duration, DV01, and dollar convexity for linear and non-linear yield shocks.
- Bootstrap spot discount factors from par yield curves and price interest rate swaps and swap DV01.
- Value zero-coupon bonds under the Vasicek and Hull-White one-factor short-rate term structure models.
- Price caplets under Black-76 and swaptions under the Bachelier normal model.
- Bootstrap piecewise constant hazard rates from market CDS spreads and compute CDS upfront fees and RPV01.
- Identify the Cheapest-to-Deliver (CTD) bond in a Treasury futures basket using conversion factors and implied repo rates.
- Calculate convexity adjustments for SOFR in arrears and CMS forward rates.
- Calibrate SABR model parameters ($\alpha, \beta, \rho, \nu$) to market volatility smiles using Hagan's formula.
- Value inflation-linked bonds (TIPS) and compute the Fisher breakeven inflation rate.
- Convert prepayment speeds between Single Monthly Mortality (SMM), Constant Prepayment Rate (CPR), and the PSA benchmark.
- Compute synthetic CDO tranche expected losses using the one-factor Gaussian copula.
- Execute daily fixed income P&L attribution across carry, roll-down, delta, twist, and gamma.
- Solve SABR $\alpha$ from an ATM quote, convert lognormal to normal vols, value asset swaps, and compute carry breakevens and pool WAL.

## Core concepts

Key analytical formulas applied across this problem set:

- **Bond Pricing and Clean/Dirty Price:**

$$P_{\text{dirty}} = P_{\text{clean}} + \text{AI} = \sum_{k=1}^n \frac{C/m}{(1 + y/m)^k} + \frac{M}{(1 + y/m)^n}$$

- **Duration and Convexity Price Approximation:**

$$\frac{\Delta P}{P} \approx -D_{\text{mod}} \cdot \Delta y + \frac{1}{2} C \cdot (\Delta y)^2, \quad \text{DV01} = P_{\text{dirty}} \cdot D_{\text{mod}} \cdot 0.0001$$

- **Par Swap Rate from Discount Factors (single curve):**

$$S_n = \frac{1 - P(0, T_n)}{\sum_{i=1}^n \tau_i P(0, T_i)}$$

- **Vasicek Zero-Coupon Bond Price:**

$$P(t, T) = A(t, T) e^{-B(t, T) r(t)}, \quad B(t, T) = \frac{1 - e^{-a(T - t)}}{a}$$

- **Black-76 Caplet Pricing:**

$$\text{Caplet} = P(0, T_{k+1}) \tau_k [F_k \Phi(d_1) - K \Phi(d_2)], \quad d_1 = \frac{\ln(F_k/K) + \frac{1}{2}\sigma^2 T_k}{\sigma \sqrt{T_k}}$$

- **Bachelier Normal Swaption Pricing:**

$$\text{Swaption}_{\text{payer}} = A_n \left[ (S_0 - K) \Phi\left(\frac{S_0 - K}{\sigma_N \sqrt{T}}\right) + \sigma_N \sqrt{T} \phi\left(\frac{S_0 - K}{\sigma_N \sqrt{T}}\right) \right]$$

- **CDS Hazard Rate and Survival Probability:**

$$\lambda \approx \frac{S_{\text{par}}}{1 - R}, \quad Q(t) = e^{-\lambda t}$$

- **One-Factor Gaussian Copula Conditional Default Probability:**

$$p(M=m) = \Phi\left(\frac{\Phi^{-1}(p) - \sqrt{\rho} m}{\sqrt{1 - \rho}}\right)$$

- **TIPS Breakeven Inflation Rate:**

$$\text{BEIR} = \frac{1 + y_{\text{nominal}}}{1 + y_{\text{real}}} - 1$$

- **Mortgage Prepayment Conversion:**

$$\text{CPR} = 1 - (1 - \text{SMM})^{12}, \quad \text{SMM} = 1 - (1 - \text{CPR})^{1/12}$$

## Worked examples

### Problem 1: Bond Pricing, Accrued Interest, and Dirty Price

A US Treasury bond pays a $4.50\%$ annual coupon semi-annually ($m = 2$) on May 15 and November 15.
Today is July 15 (settlement date).
The bond matures on May 15 in exactly 5 years.
Between May 15 and November 15, there are 184 actual days, and exactly 61 days have elapsed since the last coupon.
The bond trades at a clean price of $99.250$ per $\$100$ par.
Compute the accrued interest, the dirty price, and the semi-annual yield to maturity (YTM).

**Solution:**

Step 1: Compute Accrued Interest (AI).
Under US Treasury Actual/Actual conventions:

$$\text{Accrual Fraction } f = \frac{61}{184} \approx 0.331522$$

The semi-annual coupon payment is $C/2 = \$4.50 / 2 = \$2.25$.

$$\text{AI} = \$2.25 \times \frac{61}{184} \approx \$0.745924 \text{ per } \$100 \text{ par}$$

Step 2: Compute Dirty Price.

$$P_{\text{dirty}} = P_{\text{clean}} + \text{AI} = 99.250 + 0.745924 = \$99.995924 \text{ per } \$100 \text{ par}$$

Step 3: Calculate Semi-Annual Yield to Maturity ($y$).
Remaining coupon dates: 10 semi-annual periods.
The first coupon occurs in $1 - f = 123/184 = 0.668478$ periods.
Solving the discounted cash flow equation:

$$99.995924 = \frac{2.25}{(1 + y/2)^{0.6685}} + \sum_{k=2}^{10} \frac{2.25}{(1 + y/2)^{k - 1 + 0.6685}} + \frac{100}{(1 + y/2)^{9.6685}}$$

Evaluating numerically yields a semi-annual compounded yield of $y = 4.674\%$ per annum ($y/2 = 2.337\%$).

---

### Problem 2: Macaulay Duration, Modified Duration, and DV01

A 3-year annual pay bond with par $\$1,000$ pays a $5.00\%$ annual coupon.
The yield to maturity is flat at $5.00\%$ per annum compounded annually.
Calculate the exact Macaulay duration, modified duration, and the DV01 per $\$10,000,000$ notional.

**Solution:**

Step 1: Cash flows and discount factors at $y = 5.00\%$:
Because coupon rate equals yield, the bond trades at par: $P = \$1,000.00$.
- Year 1: Cash flow $CF_1 = \$50$, $PV = \$50 / 1.05 = \$47.6190$
- Year 2: Cash flow $CF_2 = \$50$, $PV = \$50 / 1.05^2 = \$45.3515$
- Year 3: Cash flow $CF_3 = \$1,050$, $PV = \$1,050 / 1.05^3 = \$907.0295$

Step 2: Macaulay Duration:

$$D_{\text{mac}} = \frac{1 \times 47.6190 + 2 \times 45.3515 + 3 \times 907.0295}{1,000.00} = \frac{47.6190 + 90.7029 + 2,721.0884}{1,000.00} = \frac{2,859.4104}{1,000.00} \approx 2.8594 \text{ years}$$

Step 3: Modified Duration:

$$D_{\text{mod}} = \frac{D_{\text{mac}}}{1 + y} = \frac{2.85941}{1.05} \approx 2.72325 \text{ years}$$

Step 4: DV01 per $\$10,000,000$ notional:

$$\text{DV01} = P \times D_{\text{mod}} \times 0.0001 = \$10,000,000 \times 2.72325 \times 0.0001 = \$2,723.25 \text{ per bp}$$

---

### Problem 3: Convexity and Taylor Series Price Approximation

A 10-year bond has modified duration $D_{\text{mod}} = 7.50$ years and annual convexity $C = 68.0$.
The bond price is $P = 100.00$.
Estimate the price change for:
1. An upward yield shift of $+150$ basis points ($\Delta y = +0.0150$).
2. A downward yield shift of $-150$ basis points ($\Delta y = -0.0150$).
Compare the duration-only approximation versus the duration-plus-convexity approximation.

**Solution:**

Step 1: Duration-only approximation:
For $\Delta y = +0.0150$:

$$\Delta P_{\text{dur}} = -D_{\text{mod}} \cdot P \cdot \Delta y = -7.50 \times 100 \times 0.0150 = -11.250$$

For $\Delta y = -0.0150$:

$$\Delta P_{\text{dur}} = -7.50 \times 100 \times (-0.0150) = +11.250$$

Step 2: Convexity correction:

$$\Delta P_{\text{conv}} = \frac{1}{2} C \cdot P \cdot (\Delta y)^2 = \frac{1}{2} \times 68.0 \times 100 \times (0.0150)^2 = 3400 \times 0.000225 = +0.765$$

Convexity is always positive for non-callable bonds, buffering losses when yields rise and boosting gains when yields fall.

Step 3: Total estimated price change:
- Upward shift ($+150$ bps): $\Delta P \approx -11.250 + 0.765 = -10.485$ (Estimated price $= 89.515$).
- Downward shift ($-150$ bps): $\Delta P \approx +11.250 + 0.765 = +12.015$ (Estimated price $= 112.015$).

---

### Problem 4: Zero-Coupon Curve Bootstrapping

You are given the following annual par bond yields:
- 1-year par bond: $y_1 = 3.00\%$
- 2-year par bond: $y_2 = 3.50\%$
- 3-year par bond: $y_3 = 4.00\%$
Bootstrap the zero-coupon discount factors $P(0, 1)$, $P(0, 2)$, and $P(0, 3)$, and find the 3-year zero rate $z_3$ (continuously compounded).

**Solution:**

Step 1: 1-year discount factor:
The 1-year par bond pays coupon $\$3$ and principal $\$100$ at $t = 1$:

$$100 = \frac{103}{1 + 0.03} \implies P(0, 1) = \frac{1}{1.03} \approx 0.970874$$

Step 2: 2-year discount factor:
The 2-year par bond pays $\$3.50$ at $t=1$ and $\$103.50$ at $t=2$:

$$100 = 3.50 \times P(0, 1) + 103.50 \times P(0, 2)$$

$$100 = 3.50 \times 0.970874 + 103.50 \times P(0, 2) = 3.398058 + 103.50 \times P(0, 2)$$

$$P(0, 2) = \frac{100 - 3.398058}{103.50} = \frac{96.601942}{103.50} \approx 0.933352$$

Step 3: 3-year discount factor:
The 3-year par bond pays $\$4.00$ at $t=1, 2$ and $\$104.00$ at $t=3$:

$$100 = 4.00 \times [P(0, 1) + P(0, 2)] + 104.00 \times P(0, 3)$$

$$100 = 4.00 \times [0.970874 + 0.933352] + 104.00 \times P(0, 3) = 4.00 \times 1.904226 + 104.00 \times P(0, 3)$$

$$100 = 7.616904 + 104.00 \times P(0, 3) \implies P(0, 3) = \frac{92.383096}{104.00} \approx 0.888299$$

Step 4: Continuously compounded 3-year zero rate:

$$P(0, 3) = e^{-z_3 \times 3} \implies z_3 = -\frac{\ln(0.888299)}{3} = -\frac{-0.118447}{3} \approx 0.039482 \quad (3.948\%)$$

---

### Problem 5: Par Interest Rate Swap Rate & Swap DV01

Using the bootstrapped discount factors from Problem 4 ($P(0, 1) = 0.970874$, $P(0, 2) = 0.933352$, $P(0, 3) = 0.888299$):
Calculate the 3-year annual par swap rate $S_3$ and the swap DV01 per $\$100,000,000$ notional for a payer swap.

**Solution:**

Step 1: Compute the swap annuity factor (DV01 annuity):

$$A_3 = \sum_{i=1}^3 \tau_i P(0, T_i) = 1.0 \times (0.970874 + 0.933352 + 0.888299) = 2.792525$$

Step 2: Par Swap Rate:

$$S_3 = \frac{1 - P(0, 3)}{A_3} = \frac{1 - 0.888299}{2.792525} = \frac{0.111701}{2.792525} \approx 0.040000 \quad (4.000\%)$$

As expected, the 3-year par swap rate matches the 3-year annual par bond yield of $4.00\%$.

Step 3: Swap DV01 per $\$100,000,000$ notional:

$$\text{Swap DV01} = N \times A_3 \times 0.0001 = \$100,000,000 \times 2.792525 \times 0.0001 = \$27,925.25 \text{ per bp}$$

---

### Problem 6: Vasicek Short-Rate Model Analytics

In a Vasicek model $dr(t) = a(b - r(t))dt + \sigma dW(t)$, parameters are:
Speed of reversion $a = 0.15$, long-term mean $b = 0.050$, short-rate volatility $\sigma = 0.015$.
The current short rate is $r(0) = 0.035$.
Calculate the price of a 5-year zero-coupon bond $P(0, 5)$ and its continuously compounded yield $y(0, 5)$.

**Solution:**

Step 1: Compute $B(0, 5)$:

$$B(0, 5) = \frac{1 - e^{-0.15 \times 5}}{0.15} = \frac{1 - e^{-0.75}}{0.15} = \frac{1 - 0.472367}{0.15} = \frac{0.527633}{0.15} \approx 3.517556$$

Step 2: Compute $A(0, 5)$:
The Vasicek formula for $\ln A(0, T)$ is:

$$\ln A(0, T) = (B(0, T) - T)\left(b - \frac{\sigma^2}{2a^2}\right) - \frac{\sigma^2 B(0, T)^2}{4a}$$

$$\frac{\sigma^2}{2a^2} = \frac{0.015^2}{2 \times 0.15^2} = \frac{0.000225}{0.0450} = 0.0050$$

$$b - \frac{\sigma^2}{2a^2} = 0.050 - 0.0050 = 0.0450$$

$$(B(0, 5) - 5) = 3.517556 - 5 = -1.482444$$

$$\text{First term} = -1.482444 \times 0.0450 \approx -0.066710$$

$$\text{Second term} = -\frac{0.015^2 \times 3.517556^2}{4 \times 0.15} = -\frac{0.000225 \times 12.3732}{0.60} = -\frac{0.002784}{0.60} \approx -0.004640$$

$$\ln A(0, 5) = -0.066710 - 0.004640 = -0.071350 \implies A(0, 5) = e^{-0.071350} \approx 0.931136$$

Step 3: Compute $P(0, 5)$:

$$P(0, 5) = A(0, 5) e^{-B(0, 5) r(0)} = 0.931136 \times e^{-3.517556 \times 0.035} = 0.931136 \times e^{-0.123114} = 0.931136 \times 0.884162 = 0.823275 \quad (0.82328, \text{ carrying full precision})$$

Step 4: Yield $y(0, 5)$:

$$y(0, 5) = -\frac{\ln P(0, 5)}{5} = -\frac{-0.194464}{5} \approx 0.038893 \quad (3.889\%)$$

---

### Problem 7: Hull-White European Option on a Zero-Coupon Bond

In a Hull-White model with $a = 0.10$ and $\sigma = 0.012$, a European call option with maturity $T_1 = 1.0$ year and strike $K = 0.950$ is written on a zero-coupon bond maturing at $T_2 = 4.0$ years.
Market discount factors are $P(0, 1) = 0.9600$ and $P(0, 4) = 0.8400$.
Price the option using the Hull-White closed-form formula.

**Solution:**

Step 1: Compute bond volatility $\sigma_P$:

$$\sigma_P = \frac{\sigma}{a}\left(1 - e^{-a(T_2 - T_1)}\right)\sqrt{\frac{1 - e^{-2a T_1}}{2a}}$$

$$T_2 - T_1 = 3.0 \implies 1 - e^{-0.10 \times 3} = 1 - e^{-0.30} = 1 - 0.740818 = 0.259182$$

$$\sqrt{\frac{1 - e^{-0.20}}{0.20}} = \sqrt{\frac{1 - 0.818731}{0.20}} = \sqrt{\frac{0.181269}{0.20}} = \sqrt{0.906346} \approx 0.952022$$

$$\sigma_P = \frac{0.012}{0.10} \times 0.259182 \times 0.952022 = 0.12 \times 0.259182 \times 0.952022 \approx 0.029610$$

Step 2: Forward bond price:

$$F_B = \frac{P(0, 4)}{P(0, 1)} = \frac{0.8400}{0.9600} = 0.8750$$

Step 3: Compute $d_1$ and $d_2$:

$$d_1 = \frac{\ln(F_B / K) + \frac{1}{2}\sigma_P^2}{\sigma_P} = \frac{\ln(0.8750 / 0.9500) + \frac{1}{2}(0.029610)^2}{0.029610}$$

$$\ln(0.921053) \approx -0.082238$$

$$d_1 = \frac{-0.082238 + 0.000438}{0.029610} = \frac{-0.081800}{0.029610} \approx -2.7626$$

$$d_2 = d_1 - \sigma_P = -2.7626 - 0.0296 = -2.7922$$

Step 4: Standard normal CDF values:
$\Phi(-2.7626) \approx 0.0028671$ and $\Phi(-2.7922) \approx 0.0026174$.

Step 5: Call option price:

$$\text{Call} = P(0, 1) [F_B \Phi(d_1) - K \Phi(d_2)] = 0.9600 \times [0.8750 \times 0.0028671 - 0.9500 \times 0.0026174]$$

$$0.8750 \times 0.0028671 \approx 0.0025087$$

$$0.9500 \times 0.0026174 \approx 0.0024865$$

$$\text{Call} = 0.9600 \times (0.0025087 - 0.0024865) = 0.9600 \times 0.00002216 \approx \$0.0000213 \text{ per } \$1 \text{ notional}$$

Carrying full precision through $\Phi(d_1)$ and $\Phi(d_2)$ gives $\$2.127 \times 10^{-5}$.

The call is deep out-of-the-money ($F_B = 0.875$ vs $K = 0.950$), yielding a tiny premium.

---

### Problem 8: Black-76 Caplet Pricing

A 6-month caplet on a 6-month forward-looking term rate (for example 6M Term SOFR) has fixing at $T = 1.0$ year and settlement at $T + \tau = 1.5$ years ($\tau = 0.50$).
The current forward rate is $F = 4.50\%$ ($0.0450$).
The strike rate is $K = 4.25\%$ ($0.0425$).
The Black implied volatility is $\sigma = 22.0\%$ ($0.220$).
The discount factor to settlement is $P(0, 1.5) = 0.9350$.
Compute the caplet price for $\$10,000,000$ notional.

**Solution:**

Step 1: Compute $d_1$ and $d_2$:

$$\sigma \sqrt{T} = 0.220 \times \sqrt{1.0} = 0.220$$

$$\ln(F / K) = \ln(0.0450 / 0.0425) = \ln(1.058824) \approx 0.057158$$

$$d_1 = \frac{0.057158 + \frac{1}{2}(0.220)^2 \times 1.0}{0.220} = \frac{0.057158 + 0.024200}{0.220} = \frac{0.081358}{0.220} \approx 0.3698$$

$$d_2 = d_1 - 0.220 = 0.3698 - 0.2200 = 0.1498$$

Step 2: Normal probabilities:
$\Phi(0.3698) \approx 0.6442383$, $\Phi(0.1498) \approx 0.5595431$.

Step 3: Caplet payout in forward terms:

$$F \Phi(d_1) - K \Phi(d_2) = 0.0450 \times \Phi(d_1) - 0.0425 \times \Phi(d_2) = 0.028990725 - 0.023780583 = 0.005210142$$

Step 4: Present value per $\$10,000,000$ notional:

$$\text{Caplet} = \$10,000,000 \times 0.9350 \times 0.50 \times 0.005210142 = \$4,675,000 \times 0.005210142 \approx \$24,357.41$$

---

### Problem 9: Bachelier Normal Swaption Pricing

A 1-year into 5-year payer swaption has strike $K = 3.75\%$.
The current 5-year forward swap rate is $S_0 = 3.75\%$ (at-the-money).
The swap annuity is $A = 4.45$.
The normal volatility is $\sigma_N = 65 \text{ bps/year} = 0.0065$.
Option expiry is $T = 1.0$ year.
Calculate the ATM payer swaption price for $\$50,000,000$ notional.

**Solution:**

Step 1: ATM Bachelier pricing formula:
Because $S_0 = K$, $(S_0 - K) = 0$.
The normal pricing formula simplifies to:

$$\text{Swaption}_{\text{payer}} = N \times A \times \sigma_N \sqrt{T} \times \frac{1}{\sqrt{2\pi}}$$

Step 2: Calculate numerical value:

$$\frac{1}{\sqrt{2\pi}} \approx 0.398942$$

$$\sigma_N \sqrt{T} \times \frac{1}{\sqrt{2\pi}} = 0.0065 \times 1.0 \times 0.398942 \approx 0.0025931 \quad (25.93 \text{ bps})$$

Step 3: Total dollar premium, carrying full precision (rounding the factor to $0.0025931$ first would cost about $\$5$):

$$\text{Swaption Premium} = \$50,000,000 \times 4.45 \times 0.0065 \times \frac{1}{\sqrt{2\pi}} \approx \$576,970.27$$

---

### Problem 10: CDS Hazard Rate Bootstrapping and Upfront Fee

A firm trades 5-year CDS at a par spread of 150 bps ($S = 0.0150$).
The recovery rate is $R = 40\%$ ($LGD = 0.60$).
The risk-free discount rate is flat at $r = 4.00\%$.
1. Compute the constant hazard rate $\lambda$ under the par spread approximation rule.
2. Calculate the exact 5-year survival probability $Q(5)$.
3. If the contract trades on the standard 100 bps fixed coupon, compute the upfront fee as a percentage of notional.

**Solution:**

Step 1: Hazard rate approximation:

$$\lambda \approx \frac{S}{1 - R} = \frac{0.0150}{1 - 0.40} = \frac{0.0150}{0.60} = 0.0250 \quad (2.50\% \text{ per annum})$$

(Solving the premium and protection legs exactly in [`code/fi_problem_set.py`](code/fi_problem_set.py), with quarterly premiums, half-period accrual on default, default settled mid-period and continuous discounting at 4%, gives $\lambda = 2.4875\%$, so the shortcut is off by about $0.5\%$ of its value.)

Step 2: 5-year survival probability:

$$Q(5) = e^{-0.0250 \times 5} \approx 0.8825 \quad (88.25\%)$$

Under exact bootstrapping, $Q(5) = e^{-0.024875 \times 5} = 88.30\%$.

Step 3: Upfront fee calculation:
Market spread is $150$ bps, standard coupon is $100$ bps:

The exact single-quote curve gives $\text{RPV01} = 4.2487$.
Because that flat curve reprices the 150 bp quote to par, $\text{PV}_{\text{protection}} = S \times \text{RPV01}$ and the upfront is exactly:

$$\text{Upfront Fee (\%)} = (S - C) \times \text{RPV01} = (0.0150 - 0.0100) \times 4.2487 = 0.0050 \times 4.2487 = 0.021244 \quad (2.12\%)$$

The protection buyer pays an upfront fee of $2.12\%$ of notional ($\$212,437$ per $\$10,000,000$).

---

### Problem 11: Treasury Futures Conversion Factor and Cheapest-to-Deliver (CTD)

A Treasury futures contract has a settlement price of $108.50$.
Two deliverable bonds have the following characteristics:
- Bond A: Clean Price $= 118.25$, Conversion Factor $CF_A = 1.0850$.
- Bond B: Clean Price $= 132.50$, Conversion Factor $CF_B = 1.2150$.
Determine which bond has the lower gross basis (clean price minus futures price times conversion factor).

**Solution:**

Step 1: Compute implied futures invoice price for each bond:

$$\text{Invoice Price} = \text{Futures Price} \times CF$$

$$\text{Invoice}_A = 108.50 \times 1.0850 = 117.7225$$

$$\text{Invoice}_B = 108.50 \times 1.2150 = 131.8275$$

Step 2: Compute the gross basis ($\text{Clean Price} - \text{Invoice Price}$):

$$\text{Basis}_A = 118.25 - 117.7225 = +0.5275$$

$$\text{Basis}_B = 132.50 - 131.8275 = +0.6725$$

Step 3: Compare:
Bond A has the lower gross basis ($+0.5275 < +0.6725$), so on this screen it is the cheaper to deliver.
The full test subtracts carry to delivery (net basis) or, equivalently, picks the highest implied repo rate; with different coupons and financing the two bonds' carry can reorder them.

---

### Problem 12: Convexity Adjustment for a Rate Paid at Its Fixing Date

A swap leg pays a term SOFR rate that fixes at $T_1$ for the accrual period $[T_1, T_2]$, but pays it at the fixing date $T_1$ instead of at the natural payment date $T_2$ (the in-arrears timing mismatch).
$T_1 = 2.0$ years, $T_2 = 2.5$ years ($\tau = 0.50$).
The forward SOFR rate is $F = 4.00\%$ ($0.0400$).
The annual volatility of forward SOFR is $\sigma = 20.0\%$ ($0.200$).
Compute the convexity adjustment and the adjusted forward coupon rate.

**Solution:**

Step 1: Apply the standard Black-76 convexity adjustment formula:

$$\Delta F \approx \frac{F^2 \sigma^2 \tau T_1}{1 + \tau F}$$

Step 2: Calculate numerator:

$$F^2 = 0.0400^2 = 0.0016$$

$$\sigma^2 = 0.200^2 = 0.0400$$

$$\tau T_1 = 0.50 \times 2.0 = 1.0$$

$$\text{Numerator} = 0.0016 \times 0.0400 \times 1.0 = 0.000064$$

Step 3: Calculate denominator:

$$1 + \tau F = 1 + 0.50 \times 0.0400 = 1.020$$

Step 4: Convexity adjustment:

$$\Delta F = \frac{0.000064}{1.020} \approx 0.00006275 \quad (0.63 \text{ bps})$$

Step 5: Adjusted forward rate:

$$F_{\text{adjusted}} = 4.00\% + 0.0063\% = 4.0063\%$$

---

### Problem 13: SABR ATM Implied Volatility

Consider a SABR model with parameters:
Forward rate $f = 0.0400$, expiry $T = 2.0$ years.
Parameters: $\alpha = 0.020$, $\beta = 0.50$, $\rho = -0.25$, $\nu = 0.40$.
Calculate the ATM Black implied volatility $\sigma_{\text{B}}(f, f)$ using Hagan's formula.

**Solution:**

Step 1: ATM formula for Hagan's SABR expansion:

$$\sigma_{\text{B}}(f, f) \approx \frac{\alpha}{f^{1 - \beta}} \left[ 1 + \left( \frac{(1 - \beta)^2}{24} \frac{\alpha^2}{f^{2(1 - \beta)}} + \frac{1}{4} \frac{\rho \beta \nu \alpha}{f^{1 - \beta}} + \frac{2 - 3\rho^2}{24} \nu^2 \right) T \right]$$

Step 2: Base volatility:

$$f^{1 - \beta} = 0.0400^{0.50} = 0.200$$

$$\frac{\alpha}{f^{1 - \beta}} = \frac{0.020}{0.200} = 0.100 \quad (10.0\%)$$

Step 3: Correction terms:
- Term 1:

$$\frac{(1 - 0.5)^2}{24} \times \frac{0.020^2}{0.200^2} = \frac{0.25}{24} \times \frac{0.0004}{0.0400} = 0.010417 \times 0.010 = 0.000104$$

- Term 2:

$$\frac{1}{4} \times (-0.25) \times 0.50 \times 0.40 \times \frac{0.020}{0.200} = -0.0125 \times 0.100 = -0.001250$$

- Term 3:

$$\frac{2 - 3(-0.25)^2}{24} \times 0.40^2 = \frac{2 - 0.1875}{24} \times 0.160 = \frac{1.8125}{24} \times 0.160 = 0.075521 \times 0.160 = 0.012083$$

Step 4: Sum of correction terms multiplied by $T = 2.0$:

$$\text{Sum} = 0.000104 - 0.001250 + 0.012083 = 0.0109375 \text{ (unrounded)}$$

$$\text{Multiplier} = 1 + (0.0109375 \times 2.0) = 1.021875$$

Step 5: ATM Implied Volatility:

$$\sigma_{\text{B}} = 0.100 \times 1.021875 \approx 10.22\%$$

---

### Problem 14: TIPS Indexation and Breakeven Inflation Rate

A 10-year Treasury nominal bond yields $y_{\text{nom}} = 4.25\%$.
A 10-year Treasury Inflation-Protected Security (TIPS) yields $y_{\text{real}} = 1.85\%$.
1. Compute the exact Fisher Breakeven Inflation Rate (BEIR).
2. A TIPS bond with a $2.00\%$ annual coupon was issued when reference CPI was $300.0$. Today, reference CPI is $315.0$. Compute the current inflation index ratio and the semi-annual coupon payment on a $\$100,000$ base par bond.

**Solution:**

Step 1: Exact Fisher Breakeven Inflation Rate:

$$\text{BEIR} = \frac{1 + y_{\text{nom}}}{1 + y_{\text{real}}} - 1 = \frac{1.0425}{1.0185} - 1 = 1.023564 - 1 \approx 0.023564 \quad (2.36\%)$$

Step 2: Index Ratio:

$$\text{Index Ratio} = \frac{\text{CPI}_{\text{ref}}}{\text{CPI}_{\text{base}}} = \frac{315.0}{300.0} = 1.0500$$

Step 3: Adjusted principal and semi-annual coupon:

$$\text{Adjusted Principal} = \$100,000 \times 1.0500 = \$105,000$$

$$\text{Semi-annual Coupon} = \frac{0.0200}{2} \times \$105,000 = 0.0100 \times \$105,000 = \$1,050.00$$

---

### Problem 15: Mortgage Prepayment Metrics (SMM, CPR, PSA)

An Agency MBS pool exhibits a Single Monthly Mortality of $\text{SMM} = 0.50\%$ ($0.0050$).
1. Compute the equivalent annualized Constant Prepayment Rate (CPR).
2. In month 10 of a newly originated mortgage pool, what is the CPR corresponding to a $100\%$ PSA benchmark?
3. In month 30, what is the CPR corresponding to a $150\%$ PSA benchmark?

**Solution:**

Step 1: Annualized CPR:

$$\text{CPR} = 1 - (1 - \text{SMM})^{12} = 1 - (1 - 0.0050)^{12} = 1 - (0.9950)^{12} \approx 1 - 0.941623 = 0.058377 \quad (5.84\%)$$

Step 2: 100% PSA at Month 10:
The PSA benchmark ramps up by $0.2\%$ CPR per month for the first 30 months:

$$\text{CPR}_{100\% \text{ PSA}}(10) = 6.0\% \times \frac{10}{30} = 2.0\%$$

Step 3: 150% PSA at Month 30:
At month 30, the 100% PSA schedule reaches its cap of $6.0\%$:

$$\text{CPR}_{150\% \text{ PSA}}(30) = 1.50 \times 6.0\% = 9.0\%$$

---

### Problem 16: Gaussian Copula CDO Tranche Loss and P&L Attribution

A large homogeneous portfolio (the $N \to \infty$ limit of identical credits) has default probability $p = 5.0\%$, correlation $\rho = 0.30$, and recovery $R = 40\%$ ($LGD = 0.60$).
Using the one-factor Gaussian copula:
1. Calculate the conditional default probability under an extreme market factor realization of $M = -2.0$ standard deviations.
2. Given the large homogeneous portfolio (LHP) loss distribution (computed and asserted in [`code/fi_credit_tranches.py`](code/fi_credit_tranches.py)), compare the expected loss of an Equity Tranche $[0\%, 3\%]$ with a Senior Tranche $[7\%, 10\%]$.
3. A fund holds $\$50,000,000$ notional of a bond portfolio with $\text{DV01} = \$35,000$, dollar convexity $C_{\$} = \$3,500,000,000$, and daily carry of $+\$1,200$. Over 1 day, yields rise by $+8$ bps ($\Delta y = +0.0008$). Compute the total predicted daily P&L.

**Solution:**

Step 1: Conditional default probability at $M = -2.0$:
Threshold $c = \Phi^{-1}(0.05) \approx -1.6449$:

$$p(M = -2.0) = \Phi\left(\frac{-1.6449 - \sqrt{0.30} \times (-2.0)}{\sqrt{1 - 0.30}}\right) = \Phi\left(\frac{-1.644854 + 1.095445}{0.836660}\right) = \Phi\left(\frac{-0.549409}{0.836660}\right) = \Phi(-0.656669) \approx 0.2557 \quad (25.57\%)$$

Conditional portfolio credit loss is $0.60 \times 25.57\% = 15.34\%$.

Step 2: Tranche expected loss verification:
- Equity Tranche $[0\%, 3\%]$ absorbs the first $3\%$ of portfolio losses. Expected loss is $54.11\%$ of tranche notional.
- Senior Tranche $[7\%, 10\%]$ absorbs losses between $7\%$ and $10\%$. Expected loss is $8.78\%$ of tranche notional.
Senior loss is dramatically lower due to subordination shielding.

Step 3: P&L Attribution:

$$\text{P\&L}_{\text{Delta}} = -\text{DV01} \times 8 = -\$35,000 \times 8 = -\$280,000$$

$$\text{P\&L}_{\text{Gamma}} = \frac{1}{2} C_{\$} (\Delta y)^2 = \frac{1}{2} \times \$3,500,000,000 \times (0.0008)^2 = \$1,750,000,000 \times 6.4 \times 10^{-7} = +\$1,120$$

$$\text{P\&L}_{\text{Carry}} = +\$1,200$$

$$\text{Total Predicted P\&L} = -\$280,000 + \$1,120 + \$1,200 = -\$277,680$$

---

### Problem 17: SABR Alpha from an ATM Quote

The ATM lognormal vol of a 2-year option on a $3\%$ forward is $20\%$; with $\beta = 0.5$, $\rho = -0.30$, $\nu = 0.50$ fixed, find $\alpha$.

**Solution:**

Step 1: First guess ignoring the $O(T)$ term: $\alpha_0 = \sigma_{\text{ATM}} F^{1-\beta} = 0.20 \times \sqrt{0.03} = 0.034641$.

Step 2: Solve $\frac{\alpha}{F^{1-\beta}}\left[1 + \Gamma(\alpha) T\right] = 0.20$ (the ATM cubic) by bisection or Newton: $\alpha = 0.033647$.

Step 3: Check: at that $\alpha$, $1 + \Gamma T = 1.029543$, and $0.033647 \times 1.029543 / \sqrt{0.03} = 20\%$; the $O(T)$ term lowered $\alpha$ by about $3\%$ relative to the first guess.

---

### Problem 18: HJM and LMM Drifts

1. In one-factor HJM with $\sigma(t, T) = 1\% \times e^{-0.05 (T - t)}$, what is the risk-neutral drift of the forward 5 years ahead?
2. Under the terminal measure, forward $L_k$ (vol $25\%$) is followed by one more forward $L_{k+1} = 5\%$ with $\tau = 0.5$, vol $20\%$ and correlation $0.9$; what is the drift of $dL_k/L_k$?

**Solution:**

Step 1: $\alpha = \frac{\sigma^2}{a} e^{-a(T-t)}(1 - e^{-a(T-t)}) = \frac{0.0001}{0.05} e^{-0.25}(1 - e^{-0.25}) = 3.4454 \times 10^{-4}$, about $3.4$ bp per year.

Step 2: $\mu_k = -\frac{\tau L_{k+1}}{1 + \tau L_{k+1}} \rho \sigma_k \sigma_{k+1} = -\frac{0.025}{1.025} \times 0.9 \times 0.25 \times 0.20 = -0.1098\%$ per year.

---

### Problem 19: Weighted Average Life at 200 PSA

A new 30-year pool has a $6.0\%$ WAC and $5.5\%$ pass-through coupon. Find the SMM at month 30 and the WAL at 200 PSA.

**Solution:**

Step 1: At 200 PSA the CPR from month 30 is $2 \times 6\% = 12\%$, so $\text{SMM} = 1 - 0.88^{1/12} = 1.0596\%$.

Step 2: Project month by month: level payment on the remaining term at the WAC, scheduled principal $=$ payment minus interest at the WAC, prepayment $=$ SMM times the balance after scheduled principal.

Step 3: $\text{WAL} = \sum_t t P_t / \sum_t P_t = 7.67$ years over principal only (the coupon sets investor interest and does not enter the WAL), against $11.36$ years at 100 PSA in [Mortgages and Securitized Products](22-Mortgages-and-Securitized-Products.md).

---

### Problem 20: Asset Swap of a Premium Bond

The swap curve is flat at a $3.50\%$ annual par rate. A 5-year $5.00\%$ annual bond yields $4.20\%$ on a coupon date. Find the par-par and market-value asset swap spreads.

**Solution:**

Step 1: Discount factors $d_i = 1.035^{-i}$, annuity $A = \sum d_i = 4.5151$.

Step 2: Market price at $4.20\%$: $103.5415$; the same cash flows on the swap curve: $\sum 5 d_i + 100 d_5 = 106.7726$.

Step 3: Par-par: $s = \frac{106.7726 - 103.5415}{100 \times 4.5151} = 71.56$ bp.

Step 4: Market value: $s_{\text{MV}} = 71.56 \times 100 / 103.5415 = 69.11$ bp, below par-par because the bond is above par (the opposite of the discount bond in [Fixed Income P&L and Relative Value](24-Fixed-Income-PnL-and-Relative-Value.md)).

---

### Problem 21: Carry and Roll-Down Breakeven

A 5-year note yields $4.00\%$ and is financed at $3.50\%$; its modified duration is $4.5$ and the curve around 5 years rises $10$ bp per year of maturity. How far can its yield rise over 3 months before the position loses money?

**Solution:**

Step 1: Carry in yield terms: $(4.00\% - 3.50\%) \times 0.25 / 4.5 = 2.78$ bp.

Step 2: Roll-down: the bond becomes a $4.75$-year bond on a curve $10$ bp per year steeper, so its yield falls $10 \times 0.25 = 2.50$ bp.

Step 3: Breakeven: $2.78 + 2.50 = 5.28$ bp of yield rise over the quarter (first order).

---

### Problem 22: Lognormal to Normal Volatility

Convert a $25\%$ ATM lognormal vol on a $2\%$ forward with 4 years to expiry into a normal vol.

**Solution:**

Step 1: Zeroth order: $\sigma_B F = 0.25 \times 200 = 50.00$ bp.

Step 2: Second order: $\sigma_N \approx \sigma_B F (1 - \sigma_B^2 T / 24) = 50 \times (1 - 0.0625 \times 4 / 24) = 49.48$ bp.

Step 3: Exact: equate the ATM Black value $F(2\Phi(\sigma_B \sqrt{T}/2) - 1)$ with the Bachelier value $\sigma_N \sqrt{T / 2\pi}$: $49.48$ bp, so the second-order formula is accurate to the quoted precision.

## Pitfalls

- **Ignoring Compounding Conventions:** Mixing semi-annual bond yields with continuously compounded forward rates creates significant pricing errors.
- **Neglecting Prepayment Optionality in MBS Duration:** Applying standard cash flow duration to MBS ignores negative convexity and drastically misstates risk during rate rallies.
- **Treating the Credit Triangle as an Exact Bootstrap:** $\lambda \approx S/(1 - R)$ ignores discounting and premium accrual and returns an average hazard rate to maturity, not a forward one.
For a single flat 150 bp quote the error is small ($2.49\%$ exact versus $2.50\%$, Problem 10).
On the upward-sloping 100/120/150 bp curve of [Credit and CDS](06-Credit-and-CDS.md), the bootstrapped $(3\text{y}, 5\text{y}]$ forward hazard is $3.37\%$, about $35\%$ above the shortcut.
- **Relying on the Gaussian Copula for Senior Tranches:** its zero tail dependence understates joint default clustering, which matters most for senior and super-senior layers.
- **Inconsistent Delivery Month Alignment in Futures Basis:** Comparing cash Treasury settlement against futures settlement without accounting for financing over the delivery window causes false arbitrage signals.
- **Ranking CTD by Gross Basis Alone:** the gross basis ignores carry to delivery; use net basis or implied repo (Problem 11).
- **Forgetting Which Way a Regression Hedge Leaves Risk:** regression-weighted butterflies are not parallel-neutral unless the betas sum to one.

## Interview questions

> [!question]- fi-ps-bond-accrued-interest-actual | How is accrued interest calculated on US Treasury notes, and why is actual/actual day count preferred over 30/360?
> The semi-annual coupon times actual days since the last coupon over actual days in the current coupon period (Problem 1: $2.25 \times 61/184 = 0.745924$).
> Actual/actual allocates each coupon in proportion to calendar time within its own period, so accrual matches the period the coupon pays for.

> [!question]- fi-ps-modified-vs-macaulay-duration | What is the mathematical and economic relationship between Macaulay duration and Modified duration?
> Macaulay duration is the present-value-weighted average time of the cash flows; modified duration is Macaulay divided by $(1 + y/m)$ for compounding frequency $m$.
> Modified duration is the relative price sensitivity to the bond's own yield, $-\frac{1}{P}\frac{\partial P}{\partial y}$: $2.8594 / 1.05 = 2.72325$ in Problem 2.

> [!question]- fi-ps-par-swap-rate-formula | State the formula for a par interest rate swap rate in terms of discount factors, and explain why the principal does not exchange.
> With one curve for projection and discounting, $S_n = \frac{1 - P(0, T_n)}{\sum_i \tau_i P(0, T_i)}$, because a floating leg plus a notional exchange at maturity is worth par.
> The notional is never paid because both legs reference the same notional, so hypothetical exchanges cancel; with separate projection and discounting curves the floating leg must be valued from projected forwards instead.

> [!question]- fi-ps-vasicek-mean-reversion-property | In the Vasicek short-rate model, what is the role of the parameter $a$, and what happens as $a \to 0$?
> $a$ is the speed of mean reversion toward $b$, with half-life $\ln 2 / a$; it makes long yields less volatile than short ones because $B(t, T) = (1 - e^{-a(T-t)})/a$ saturates at $1/a$.
> As $a \to 0$, $B(t, T) \to T - t$, the short rate becomes a Brownian motion with drift, every yield has the same volatility, and zero-bond price volatility $\sigma(T - t)$ grows linearly with maturity; with a time-dependent drift fitted to the curve this is Ho-Lee.

> [!question]- fi-ps-bachelier-vs-black-swaptions | Why has the fixed income market largely transitioned from Black-76 lognormal models to Bachelier normal models for swaptions?
> Black-76 needs positive forwards and strikes and its vol becomes unstable as rates approach zero, while Bachelier allows negative rates and quotes vol in bp, which is closer to how rate moves scale.
> The two are linked by price: $25\%$ lognormal on a $2\%$ forward for 4 years is $49.48$ bp normal (Problem 22).

> [!question]- fi-ps-ctd-implied-repo-rate | Define the Implied Repo Rate (IRR) for a deliverable Treasury bond and explain how it determines the Cheapest-to-Deliver (CTD).
> The return from buying the bond, selling the future and delivering: invoice amount plus coupons received, over the purchase price, annualized.
> The CTD is the bond with the highest implied repo rate, equivalently the lowest net basis; the gross basis of Problem 11 is only a first screen.

> [!question]- fi-ps-sofr-convexity-adjustment-sign | Why does a forward term rate paid at its fixing date (the classic in-arrears structure) require a positive convexity adjustment?
> The forward $F$ is a martingale only under the $T_2$-forward measure, where a fixing paid at $T_2$ is discounted by $P(T_1, T_2) = 1/(1 + \tau R)$, which is low exactly when the fixing $R$ is high.
> Paying at $T_1$ removes that discounting, so the expectation under the $T_1$-forward measure exceeds $F$: $0.63$ bp in Problem 12. (A compounded SOFR coupon paid at the end of its period needs no such adjustment.)

> [!question]- fi-ps-sabr-rho-parameter | In the SABR volatility model, what market feature is controlled by the correlation parameter $\rho$?
> The skew: $\rho$ is the correlation between forward and volatility shocks, and $\rho < 0$ makes vol rise as rates fall, lifting low strikes.
> $\rho = 0$ removes only this part of the skew; with $\beta < 1$ the backbone still makes lognormal vols higher at low strikes.

> [!question]- fi-ps-smm-vs-cpr-prepayment | What is the relationship between Single Monthly Mortality (SMM) and Constant Prepayment Rate (CPR)?
> $\text{CPR} = 1 - (1 - \text{SMM})^{12}$ and $\text{SMM} = 1 - (1 - \text{CPR})^{1/12}$.
> $\text{SMM} = 0.5\%$ is $5.84\%$ CPR; $12\%$ CPR is an SMM of $1.0596\%$.

> [!question]- fi-ps-pnl-attribution-gamma-term | In fixed income P&L attribution, what is the convexity (gamma) P&L term, and why is it always positive for long unhedged vanilla bond positions?
> The convexity P&L term is $\frac{1}{2} C_{\$} (\Delta y)^2 = \frac{1}{2} P \cdot C \cdot (\Delta y)^2$.
> Option-free bonds have positive convexity and $(\Delta y)^2 \ge 0$, so the term is non-negative for a long position whichever way yields move ($\$1,120$ for an 8 bp move in Problem 16).

> [!question]- fi-ps-tips-beir-derivation | Derive the exact Fisher relationship for the Breakeven Inflation Rate (BEIR) and compare it to the linear approximation.
> $(1 + y_{\text{nom}}) = (1 + y_{\text{real}})(1 + \text{BEIR})$ gives $\text{BEIR} = \frac{1 + y_{\text{nom}}}{1 + y_{\text{real}}} - 1$.
> The difference $y_{\text{nom}} - y_{\text{real}} - \text{BEIR}$ equals $y_{\text{real}} \times \text{BEIR}$, so the linear form overstates when the real yield is positive and understates when it is negative.

> [!question]- fi-ps-hull-white-analytical-bond-option | How does the Hull-White model achieve closed-form European bond option pricing without a tree?
> Under one-factor Hull-White the short rate is Gaussian, so a zero-coupon bond price is lognormal under the forward measure of the option expiry.
> The option is then a Black formula on the forward bond price with deterministic volatility $\sigma_P = \frac{\sigma}{a}(1 - e^{-a(T_2 - T_1)})\sqrt{\frac{1 - e^{-2a T_1}}{2a}}$ ($0.029610$ in Problem 7).

> [!question]- fi-ps-butterfly-5050-vs-regression | Why does a 50-50 DV01 butterfly trade suffer from curve twist leakage, and how does regression weighting eliminate it?
> A 50-50 fly is neutral to parallel moves only; under a linear twist about the body it has P&L $-\frac{1}{2}\text{DV01}_b k (T_1 + T_3 - 2T_2)$, which is non-zero unless the body is the midpoint of the wings (2s5s10s is not).
> Regression weighting sizes the wings at $\beta_1$ and $\beta_3$ times the body DV01 so the historical co-movement is hedged, at the cost of parallel exposure when $\beta_1 + \beta_3 \ne 1$.

> [!question]- fi-ps-par-par-vs-market-value-asw | Distinguish between a par-par asset swap spread and a market-value asset swap spread.
> Par-par: the investor pays 100 for bond plus swap (an upfront of $100 - P$) and the swap runs on 100; $s = (P_{\text{swap curve}} - P)/(100A)$.
> Market value: the swap runs on the dirty price, no upfront, notionals exchanged at maturity, and $s_{\text{MV}} = s_{\text{par-par}} \times 100/P$ (Problem 20: $71.56$ bp par-par, $69.11$ bp market value for a bond at $103.54$).

> [!question]- fi-ps-gaussian-copula-crisis-collapse | Explain why the one-factor Gaussian copula failed to predict joint defaults during the 2008 subprime crisis.
> It has zero tail dependence ($\lim_{u \to 0} P(U_1 < u \mid U_2 < u) = 0$), so beyond the pairwise correlation it adds no clustering of extreme defaults, and it was calibrated to benign data.
> The heaviest senior losses were on ABS CDOs backed by correlated subprime mortgage bonds, where inputs and collateral concentration mattered as much as the copula.

> [!question]- fi-ps-ytm-dirty-calc | A Treasury with a 4.5% coupon, 61 days into a 184-day coupon period and 10 coupons left, trades at 99.25 clean. What are the dirty price and yield?
> Dirty $= 99.25 + 2.25 \times 61/184 = 99.995924$.
> Discounting the 10 coupons from $123/184 = 0.668478$ periods out gives a yield of $4.674\%$ (semi-annual), above the coupon because the bond is below par.

> [!question]- fi-ps-bootstrap-zero-rate | Par yields are 3.0%, 3.5% and 4.0% for 1 to 3 years (annual). What is the 3-year continuously compounded zero rate?
> Bootstrapping gives $P(0, 1) = 0.970874$, $P(0, 2) = 0.933352$, $P(0, 3) = 0.888299$, so $z_3 = -\ln(0.888299)/3 = 3.948\%$.
> It is above $3.922\%$, the continuously compounded equivalent of the 4% par yield, because on an upward-sloping curve the zero rate reflects only the final, highest-rate cash flow while the par yield averages over all of them.

> [!question]- fi-ps-vasicek-bond-value | With Vasicek $a = 0.15$, $b = 5\%$, $\sigma = 1.5\%$, $r_0 = 3.5\%$, what is the 5-year zero-coupon bond price and yield?
> $B = 3.517556$, $\ln A = -0.071350$, so $P(0, 5) = 0.82328$ and the yield is $3.889\%$.
> The yield sits between $r_0$ and $b$ as mean reversion pulls the expected path up, minus a small convexity term from $\sigma^2$.

> [!question]- fi-ps-caplet-value | Price a caplet: forward 4.50%, strike 4.25%, Black vol 22%, fixing in 1 year, accrual 0.5, discount factor 0.935, notional 10 million.
> $d_1 = 0.3698$, $d_2 = 0.1498$, $F\Phi(d_1) - K\Phi(d_2) = 0.005210$, so the caplet is $10\text{m} \times 0.935 \times 0.5 \times 0.005210 = \$24,357.41$.

> [!question]- fi-ps-cds-upfront-calc | A 5-year CDS trades at 150 bp with recovery 40% and rates 4%. What upfront does a 100 bp coupon contract need?
> Solving the legs gives a flat hazard of $2.4875\%$ and RPV01 $4.2487$, so the upfront is $(150 - 100)\text{ bp} \times 4.2487 = 2.12\%$ of notional, paid by the protection buyer ($\$212,437$ on $\$10$ million).

> [!question]- fi-ps-sabr-alpha-atm | Given a 20% ATM vol, a 3% forward, 2 years, $\beta = 0.5$, $\rho = -0.3$, $\nu = 0.5$, what SABR $\alpha$ fits?
> $\alpha = 0.033647$, the root of the ATM cubic; the first guess $\sigma F^{1-\beta} = 0.034641$ is about $3\%$ too high because it ignores the $1 + \Gamma T = 1.029543$ factor.

> [!question]- fi-ps-pool-wal | What is the WAL of a new 30-year 6% WAC pool at 200 PSA, and what is the SMM once the ramp is complete?
> About $7.67$ years; from month 30 the CPR is $12\%$, an SMM of $1.0596\%$.
> At 100 PSA the same pool's WAL is $11.36$ years, so doubling the speed cuts the WAL by about a third.

> [!question]- fi-ps-asw-premium-bond | A 5-year 5% annual bond yields 4.20% on a flat 3.50% swap curve. What are its par-par and market-value asset swap spreads?
> Par-par: $(106.7726 - 103.5415)/(100 \times 4.5151) = 71.56$ bp; market value: $71.56 \times 100/103.5415 = 69.11$ bp.
> For a premium bond the market-value spread is the smaller of the two.

> [!question]- fi-ps-carry-breakeven | A 5-year note yields 4.00%, repo is 3.50%, duration 4.5, and the curve rises 10 bp per year near 5 years. How much yield rise over 3 months does carry plus roll-down absorb?
> About $5.28$ bp: carry $0.50\% \times 0.25 / 4.5 = 2.78$ bp of yield, roll-down $10 \times 0.25 = 2.50$ bp.

> [!question]- fi-ps-normal-vol-conversion | Convert 25% lognormal ATM vol on a 2% forward with 4 years to expiry into normal vol.
> $\sigma_B F = 50$ bp, times $(1 - \sigma_B^2 T/24) = 0.98958$, gives $49.48$ bp, which the exact ATM price inversion confirms to two decimals.

## Further reading

- Bruce Tuckman and Angel Serrat, *Fixed Income Securities: Tools for Today's Markets*, 3rd edition, Wiley, 2012.
- Damiano Brigo and Fabio Mercurio, *Interest Rate Models - Theory and Practice*, 2nd edition, Springer, 2006.
- John Hull, *Options, Futures, and Other Derivatives*, Pearson (chapters on interest rate derivatives and credit).
- David X. Li, *On Default Correlation: A Copula Function Approach*, Journal of Fixed Income, 2000.

## In this repo and SDE-Interview-Prep

- Problem set verification: [`code/fi_problem_set.py`](code/fi_problem_set.py) asserts every number in Problems 1 to 22 and the cards; the tranche expected losses quoted in Problem 16 are asserted in [`code/fi_credit_tranches.py`](code/fi_credit_tranches.py).
- Topic notes behind the problems: [Rates Volatility and SABR](18-Rates-Volatility-and-SABR.md), [Term Structure Models](19-Term-Structure-Models-HJM-LGM-LMM.md), [Credit Advanced](23-Credit-Advanced-CDS-Indices-and-Tranches.md), [Mortgages](22-Mortgages-and-Securitized-Products.md), [P&L and Relative Value](24-Fixed-Income-PnL-and-Relative-Value.md).
