---
type: problem-set
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
prereqs: [kelly-criterion-and-position-sizing, var-and-expected-shortfall, xva, liquidity-and-model-risk]
est_hours: 8
sources: [Jorion - Value at Risk 3rd edition (McGraw-Hill 2006), Gregory - The xVA Challenge 4th edition (Wiley 2020), Almgren and Chriss - Optimal Execution of Portfolio Transactions - Journal of Risk 3(2) 5-39 (2000), Magdon-Ismail Atiya Pratap and Abu-Mostafa - On the Maximum Drawdown of a Brownian Motion - Journal of Applied Probability 41(1) 147-161 (2004), Hull and White - Incorporating Volatility Updating into the Historical Simulation Method for Value-at-Risk - Journal of Risk 1(1) 5-19 (1998), Broadie Glasserman and Kou - A Continuity Correction for Discrete Barrier Options - Mathematical Finance 7(4) 325-349 (1997), Basel Framework CRE52 CRE53 MAR21 MGN20 (version effective 1 January 2023), SR 26-2 Revised Guidance on Model Risk Management (17 April 2026)]
---

# Risk and Trading Problem Set

## TL;DR

- Twenty-four problems across the section, each solved the way you would at a whiteboard and each answer recomputed and asserted by code against an independent route (closed form against simulation, shortcut against full formula, Euler sum against brute force).
- Problems 1 to 8 revisit sizing, VaR and ES, scenarios, drawdowns and Greek P&L; problems 9 to 24 cover sensitivities, risk decomposition, counterparty exposure, XVA, liquidity and model risk.
- Recurring lessons: shortcuts are fine when you know their error (the midpoint MVA shortcut is 0.15% off, the drawdown asymptote 12% off at two years), conventions decide the answer (Effective EPE is 100,000 by the Basel sum and 70,000 by trapezoid), and dependence can dominate (a two-state wrong-way book has 5.26 times the independent CVA).

## Learning objectives

- Calculate optimal position sizing under the Kelly criterion and the drawdown probabilities of fractional Kelly.
- Compute parametric VaR and ES, filtered historical scenarios, the most plausible reverse-stress scenario and expected maximum drawdown.
- Attribute option P&L with vanna and volga and derive the daily break-even move.
- Choose bumps, count pricing calls and judge Taylor proxies against full revaluation.
- Execute Euler risk decomposition and equal-risk-contribution weights.
- Compute exposure profiles, Effective EPE, collateralised exposure, NGR, CVA and DVA, and funding, margin and capital adjustments.
- Solve discrete Almgren-Chriss schedules, liquidity-adjusted VaR, and quantify model risk with alternative models and continuity corrections.

## Core concepts

Formulas used, each derived in the linked note:

| Topic | Formula | Note |
| :--- | :--- | :--- |
| Kelly | $f^* = (\mu - r)/\sigma^2$, growth $f\mu - \tfrac12 f^2\sigma^2$, $P(\text{reach } x \text{ of start}) = x^{2/c - 1}$ at fraction $c$ | [Kelly](01-Kelly-Criterion-and-Position-Sizing.md) |
| Normal VaR and ES | $z_\alpha\sigma$, $\varphi(z_\alpha)\sigma/(1 - \alpha)$ | [VaR and ES](03-VaR-and-Expected-Shortfall.md) |
| Reverse stress, linear | $x^* = -L\,\Sigma\delta/(\delta^\top\Sigma\delta)$, distance $L/\sqrt{\delta^\top\Sigma\delta}$ | [Stress Testing](04-Stress-Testing-and-Scenarios.md) |
| Drawdown asymptote | $E[\text{MDD}] \approx \tfrac{\sigma}{2S}(\ln(S^2T/2) + 1.9635)$ | [Drawdowns](05-Drawdowns-and-Risk-Limits.md) |
| Break-even move | $\sigma S\sqrt{\Delta t}$, about $\sigma S/16$ per trading day | [P&L Attribution](06-PnL-Attribution-and-Greek-Risk.md) |
| Bumps | forward error $\tfrac h2 V''$, central $\tfrac{h^2}{6}V'''$; Hessian $2N^2 + 1$ pricings | [Sensitivities](12-Sensitivities-and-Revaluation.md) |
| Euler | $\rho = \sum_i x_i\,\partial\rho/\partial x_i$; normal: $x_i z(\Sigma x)_i/\sigma_P$ | [Risk Decomposition](13-Risk-Decomposition-and-Attribution.md) |
| Exposure | forward $\text{EE} = Ne^{rt}(2\Phi(\tfrac12\sigma\sqrt t) - 1)$; Effective EPE $= \sum \text{EEE}_{t_k}\Delta t_k$ over year one | [CCR Analytics](14-Counterparty-Credit-Risk-Analytics.md) |
| XVA | $\text{CVA} = \text{LGD}\int\text{DEE}\,dPD$; $\text{FCA} = \int s\,\text{DEE}\,dt$; $\text{KVA} = \int h\,E[DK]\,dt$ | [XVA](15-XVA.md) |
| Liquidity | $\text{COL} = \tfrac12 V(\bar s + a\sigma_s)$; horizon factor $(L+1)(2L+1)/(6L)$; $\cosh\kappa\tau = 1 + \tfrac12\tilde\kappa^2\tau^2$ | [Liquidity and Model Risk](16-Liquidity-and-Model-Risk.md) |

## Worked examples

All numbers are printed and asserted by `python 11-Risk-and-Trading/code/risk_problem_set.py`, which reuses functions from the section's other scripts.

### Problem 1: Kelly sizing and drawdown odds

Excess return 12%, volatility 16%.

1. Full Kelly $f^* = 0.12/0.0256 = 4.6875$ (Sharpe 0.75); growth $S^2/2 = 0.28125$.
2. Half Kelly: leverage 2.34375, volatility 0.375, growth 0.2109375, so 75% of the growth for a quarter of the variance.
3. Log wealth is Brownian with drift $cS^2 - \tfrac12 c^2S^2$ and variance $c^2S^2$ at fraction $c$ of Kelly, so the probability of ever falling to a fraction $x$ of the starting capital is $x^{2/c - 1}$: 0.5 at full Kelly and 0.125 at half Kelly for $x = \tfrac12$.
4. Halving before doubling: $1/(2^{2/c - 1} + 1)$, i.e. $1/3$ and $1/9$; a 20,000-path simulation at full Kelly gives about 0.33.
5. A 50% drawdown from a running peak happens with probability one eventually; these numbers are about the starting capital.

### Problem 2: VaR and ES of a 50m book

Daily volatility 1.2%, normal, zero mean: $\sigma = 600{,}000$.

1. $z_{0.99} = 2.326348$, VaR $= 1{,}395{,}809$.
2. ES multiplier $\varphi(z)/0.01 = 2.665214$, ES $= 1{,}599{,}128$; averaging the quantile function over the tail gives about 2.665, the definition of ES.
3. The 97.5% ES multiplier is 2.337803, almost the 99% VaR multiplier, which is why FRTB's switch kept normal-tail capital roughly level.

### Problem 3: filtered historical scenarios

Today's EWMA vol 2.2%; day A fell 3% at vol 1%, day B fell 4.5% at vol 3%.

1. Day A: $-0.03 \times 0.022/0.01 = -6.6\%$ (a 3-sigma day replayed at today's vol).
2. Day B: $-0.045 \times 0.022/0.03 = -3.3\%$.
3. Unfiltered HS ranks B as worse; after filtering, A is twice as severe.

### Problem 4: the most plausible 2.5m loss

P&L $= 20\text{m}\,x_1 - 50{,}000\,x_2$ (equity return, yield change in bp), sds 1% and 8bp, correlation 0.2.

1. $x^* = -L\,\Sigma\delta/(\delta^\top\Sigma\delta)$: equity $-1.7857\%$ and yields $+42.857$bp, which loses exactly 2.5m.
2. Mahalanobis distance $L/\sqrt{\delta^\top\Sigma\delta} = 6.0994$; a search over 3,600 directions finds the same minimum.
3. The scenario mixes a modest equity fall with a large yield rise: the book is short duration risk in a way the equity limit does not see.
4. A one-dimensional tail at that distance has probability $5.32 \times 10^{-10}$; in two factors the probability of some scenario at least that far out is higher, which is why plausibility is judged by distance, not by one quantile.

### Problem 5: expected maximum drawdown

Sharpe 1.2, volatility 12%, log-equity drift $\mu = S\sigma$.

| Horizon | exact $E[\text{MDD}]$ | Magdon-Ismail asymptote |
| ---: | ---: | ---: |
| 2 years | 0.1319 | 0.1164 |
| 10 years | 0.2022 | 0.1969 |

1. The asymptote $(\sigma/2S)(\ln(S^2T/2) + 1.9635)$ is the large-$T$ limit (the constant is $4 \times 0.49088$) and undershoots at short horizons by 12% here.
2. With zero drift, $E[\text{MDD}] = \sqrt{\pi/2}\,\sigma\sqrt T = 0.2127$ at two years: drift turns $\sqrt T$ growth into logarithmic growth.

### Problem 6: Greek P&L with cross terms

1,000 reference calls ($S = K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$); over one day spot rises 2 and vol falls 2.5 points.

| Term | P&L |
| :--- | ---: |
| Delta | 1,273.66 |
| Gamma | 37.52 |
| Vega | $-938.10$ |
| Vanna | 14.07 |
| Volga | 3.08 |
| Theta (one day) | $-25.47$ |
| Full revaluation | 373.83 |

1. Without vanna and volga the unexplained P&L is 26.21; with them it is 9.06 (the rest is third order and time cross terms).
2. A desk whose explain ignores spot-vol cross terms sees unexplained P&L on exactly the days spot and vol move together.

### Problem 7: break-even move

Delta-hedged long gamma 800 at $S = 500$, implied vol 18%.

1. Daily theta $\tfrac12\sigma^2S^2\Gamma/252 = 12{,}857.14$.
2. Break-even $|\Delta S|$ solves $\tfrac12\Gamma\Delta S^2 = 12{,}857.14$: 5.6695, equal to $\sigma S/\sqrt{252}$.
3. Rule of 16: $\sigma S/16 = 5.625$, since $\sqrt{252} = 15.875$.

### Problem 8: a PCA level shock

Eigenvalues 0.000180, 0.000018, 0.000002 (three tenors), level eigenvector $(1, 1, 1)/\sqrt 3$.

1. Variance shares 0.90, 0.09 and 0.01.
2. A $+1.5$ sd level shock is $1.5\sqrt{0.00018} \times 0.57735 = 116.19$bp at every tenor.
3. Its Mahalanobis distance under the covariance it came from is exactly 1.5: factor shocks are plausibility-calibrated by construction.

### Problem 9: forward against central bumps

Reference call, 1% spot bump.

1. Forward: 0.646125, an error of 0.9907 times $\Gamma h/2$.
2. Central: 0.636745, an error of 0.9996 times $V'''h^2/6$.
3. Central costs two pricings instead of one and is about 100 times more accurate here.

### Problem 10: counting pricing calls

A 50-factor book.
Running central differences on a pricer that counts its calls: 100 calls for the gradient and 5,001 for the full Hessian, matching $2N^2 + 1$.
With AAD the gradient costs a few pricings' worth of work instead of 100.

### Problem 11: a short put in a crash

Short the 1-year at-the-money put (worth 5.5735), spot falls 25 with vol unchanged.

1. Full revaluation: $-15.5166$.
2. Delta-gamma: $-14.9424$, understating the loss by 0.5743.
3. The sign comes from the third derivative ($V''' = -0.000516$, the same for put and call); a short option's proxy error can go either way, so test it.

### Problem 12: Euler decomposition

80m at 15% vol and 20m at 25% vol, correlation 0.4, 95% one-year VaR.

1. Portfolio volatility 14.73%, VaR 24,230,207.
2. Marginal VaR per dollar 0.234486 and 0.273567; components 18,758,870 and 5,471,337, summing to the VaR.
3. Brute-force central differences agree with the Euler gradient to $10^{-9}$.
4. The smaller position has the larger marginal VaR: cutting it reduces VaR faster per dollar.

### Problem 13: two-asset risk parity

Vols 15% and 25%.
The equal-risk-contribution weight of the 15% asset is 0.625 at correlation $-0.5$, 0 and 0.8: with two assets ERC is inverse volatility whatever the correlation.

### Problem 14: forward exposure in closed form

Par forward, $N = 10\text{m}$, vol 30%, $r = 0$, one year.

1. $\text{EE} = N(2\Phi(0.15) - 1) = 1{,}192{,}354$; rule of thumb $0.4N\sigma\sqrt t = 1{,}200{,}000$.
2. $\text{PFE}_{95} = N(e^{-0.045 + 0.3 z_{0.95}} - 1) = 5{,}658{,}927$.
3. A million-path simulation gives about 1,192,500 and about 5,651,000.

### Problem 15: Effective EPE by the Basel sum

EE at 0, 0.5, 1, 2, 3, 4, 5 years: 0, 80k, 120k, 160k, 130k, 80k, 0.

1. Effective EE: 0, 80k, 120k, 160k, then 160k to maturity.
2. Effective EPE $= \sum_{t_k \le 1}\text{EEE}_{t_k}\Delta t_k = 0.5 \times 80\text{k} + 0.5 \times 120\text{k} = 100{,}000$ (CRE53.13); a trapezoid would give 70,000.
3. EAD $= 1.4 \times 100{,}000 = 140{,}000$; EPE over the life (trapezoid) is 100,000.

### Problem 16: what the MPOR costs

Same forward, daily variation margin.

1. Collateralised EE $= N(2\Phi(\tfrac12\sigma\sqrt\delta) - 1)$: 239,329 for 10 business days, 338,412 for 20 (ratio 1.4140).
2. Against 1,192,354 uncollateralised at one year, daily margin removes 0.7993 of the EE.

### Problem 17: net-to-gross

Trades worth $+20$, $-15$, $+5$, $-2$ (millions).
Gross 25, net 8, NGR 0.32, so standardised initial margin is scaled by $0.4 + 0.6 \times 0.32 = 0.592$ (MGN20.17).

### Problem 18: CVA and DVA with flat exposure

One year, average EE 500k, ENE 300k, hazards 3% (counterparty) and 1.5% (bank), LGD 60%, rate 4%.

1. PDs 0.029554 and 0.014888.
2. CVA $\approx 0.6 \times e^{-0.02} \times 500\text{k} \times 0.029554 = 8{,}691$; the exact integral with flat exposure gives 8,692.
3. DVA $= 2{,}627$; net $\text{DVA} - \text{CVA} = -6{,}064$.
4. Credit-triangle shortcut $1.8\% \times 500\text{k} \times (1 - e^{-0.04})/0.04 = 8{,}823$.

### Problem 19: midpoint shortcuts for FVA, MVA, KVA

1. FCA $0.0075 \times 400\text{k} \times 0.945 \times 3 = 8{,}505$; MVA $0.012 \times 2\text{m} \times 0.910 \times 5 = 109{,}200$; KVA $0.10 \times 500\text{k} \times 0.910 \times 5 = 227{,}500$.
2. With the flat rate implied by $P(0, 2.5) = 0.910$ (3.7724%), $\int_0^5 e^{-rt}dt = 4.5567$ against the midpoint 4.55, so the MVA integral is 109,362: the shortcut is 0.15% low.
3. The bigger error in practice is the flat profile itself: IM and capital decay over the life (see the simulated profiles in [XVA](15-XVA.md)).

### Problem 20: wrong-way risk in two states

Exposure 10m with probability 10% (stress) and 1m otherwise; PD 1%, LGD 60%.

1. Independent: $0.6 \times 0.01 \times 1.9\text{m} = 11{,}400$.
2. All defaults in the stress state: $0.6 \times 0.1 \times 0.1 \times 10\text{m} = 60{,}000$, 5.26 times as much, with the same PD and the same exposure distribution; simulation gives about 59,800.

### Problem 21: Almgren-Chriss in discrete time

Sell 500,000 shares over 3 daily intervals, $\sigma = 2$, $\eta = 2 \times 10^{-6}$, $\lambda = 2 \times 10^{-6}$, no permanent impact.

1. $\tilde\kappa^2 = 4$, so $\cosh\kappa = 3$ and $\kappa = 1.762747$ per day.
2. Sales: 414,286, 71,429 and 14,286; the first-order linear system gives the same holdings.
3. Using the continuous $\kappa = 2$ would sell 432,355 on day 1: the continuous formula is wrong for daily trading.

### Problem 22: liquidity-adjusted VaR

30m bond, 1-day VaR 1.5m, spread 1.2% (sd 0.6%), 3 days to sell.

1. Cost of liquidation $\tfrac12 \times 30\text{m} \times (0.012 + 2.326 \times 0.006) = 389{,}371$.
2. Equal daily sales: multiplier $\sqrt{4 \times 7/18} = 1.2472$.
3. L-VaR $= 1.5\text{m} \times 1.2472 + 389{,}371 = 2{,}260{,}200$.

### Problem 23: negative prices

Futures at 5, Bachelier vol 15.96 a year, one month.
$P(F_T < 0) = 0.1389$ and the zero-strike put is worth 0.3255; Black prices both at zero.

### Problem 24: a barrier continuity correction

Daily-monitored barrier at 90, vol 20%.
The equivalent continuous barrier is $90e^{-0.5826 \times 0.2\sqrt{1/252}} = 89.3418$, a shift of 0.007340 in log terms; pricing with 90 instead overstates knock-out probability.

## Pitfalls

- Reading "probability of a 50% drawdown" as relative to the start when it is relative to the peak, or vice versa.
- Quoting VaR from $z$ rounded to four digits on large books: the difference is visible in the dollars.
- Applying the drawdown asymptote to short track records.
- Taylor proxies of short-option books in crashes, and diagonal-only Greeks in spot-vol moves.
- Trapezoid instead of the CRE53.13 sum for Effective EPE; undiscounted EE in CVA.
- Midpoint shortcuts with flat profiles for IM and capital, which decay.
- Continuous-time Almgren-Chriss on daily schedules.
- Liquidation multipliers without a stated convention.
- Pricing near-zero underlyings with lognormal models.

## Interview questions

> [!question]- risk-full-vs-half-kelly-drawdown | Why do professional quants recommend trading at half-Kelly rather than full Kelly?
> Half Kelly keeps 75% of the growth rate (0.2109 against 0.28125 at Sharpe 0.75) with a quarter of the variance.
> The chance of ever falling to half the starting capital is $x^{2/c - 1}$: 0.5 at full Kelly and 0.125 at half; of halving before doubling, 1/3 against 1/9.
> And Kelly is computed from estimated edges: overestimating the edge by a factor of two puts you at twice Kelly, where growth is zero.

> [!question]- risk-var-vs-es-coherence | Why is Expected Shortfall (ES) a coherent risk measure while Value at Risk (VaR) is not?
> VaR can fail subadditivity: for discrete or skewed losses, combining positions can raise VaR above the sum, penalising diversification; ES is monotone, translation invariant, positively homogeneous and subadditive for all distributions (Artzner, Delbaen, Eber and Heath 1999).
> For normal tails the two are close: 99% VaR is $2.326\sigma$, 99% ES $2.665\sigma$ and 97.5% ES $2.338\sigma$.
> ES is harder to backtest because it is not elicitable.

> [!question]- risk-euler-allocation-homogeneity | State the condition for Euler risk allocation to hold, and which risk measures qualify.
> The measure must be homogeneous of degree one in position sizes, $\rho(cx) = c\rho(x)$; then $\rho = \sum x_i\,\partial\rho/\partial x_i$.
> Volatility, normal VaR, and VaR and ES of any loss distribution qualify; variance (degree two) does not without halving.
> In Problem 12 the components 18,758,870 and 5,471,337 sum to the VaR 24,230,207.

> [!question]- risk-almgren-chriss-urgency-parameter | In the Almgren-Chriss framework, what does the urgency parameter $\kappa$ dictate?
> Holdings decay like $\sinh(\kappa(T - t))/\sinh(\kappa T)$, so $1/\kappa$ is the time scale over which the order is worked off; $\kappa$ grows with risk aversion and volatility and falls with temporary impact.
> In discrete time $\cosh(\kappa\tau) = 1 + \tfrac12\tilde\kappa^2\tau^2$ with $\tilde\kappa^2 = \lambda\sigma^2/\tilde\eta$: $\kappa = 1.762747$ in Problem 21, not the continuous 2, and $\lambda = 0$ gives TWAP.

> [!question]- risk-swap-vs-forward-exposure-geometry | Contrast the Expected Exposure profile of an interest rate swap with that of an FX forward.
> A forward's EE rises with time to maturity, like $0.4N\sigma\sqrt t$ for small $\sigma\sqrt t$, because all value settles at the end.
> A swap's EE is humped: rate dispersion grows like $\sqrt t$ while the remaining annuity shrinks, so it peaks early (1.75 years for the 5-year example in [CCR Analytics](14-Counterparty-Credit-Risk-Analytics.md)) and ends at zero.

> [!question]- risk-effective-epe-definition | What is Effective EPE under the Basel framework, and why was it introduced?
> The time-weighted average over the first year of Effective EE, the running maximum of EE starting from current exposure (CRE53.12 to CRE53.13); IMM EAD is $1.4\times$ it.
> The running maximum stops maturing short-dated trades from lowering exposure when in practice they are rolled over.
> In Problem 15 it is 100,000 and EAD 140,000.

> [!question]- risk-dva-paradox-accounting | Explain the DVA paradox and why it creates controversial accounting profits.
> DVA values the bank's option to default on its liabilities, so it grows as the bank's own credit worsens and the bank books gains while weakening: in the XVA example DVA rises from 2,925 to 9,074 if its hazard goes from 1.5% to 5%.
> CET1 derecognises it (CAP30.15), and it cannot be hedged directly.

> [!question]- risk-fva-mechanics-dealer | Why does an uncollateralised client swap hedged with a collateralised interdealer swap generate FVA?
> When the client trade is in the money the hedge is out of the money, so the dealer posts variation margin on the hedge while receiving nothing from the client; it funds that cash at its unsecured spread and earns only the collateral rate.
> The cost is $\int s\,\text{DEE}\,dt$: 5,062 at 80bp on the 10m 5-year swap in [XVA](15-XVA.md), with a symmetric benefit of 2,683 on the other side.

> [!question]- risk-mva-regulatory-driver | What regulatory development made Margin Valuation Adjustment (MVA) a pricing component?
> The BCBS-IOSCO margin requirements: covered entities exchange initial margin equal to a 99% 10-day potential future exposure (MGN20.9), gross and segregated, with rehypothecation only under strict conditions (MGN20.40 to MGN20.41), so IM must be funded for the trade's life.
> Problem 19: average IM of 2m funded at 1.2% for five years costs 109,362 with the exact discount integral.

> [!question]- risk-sr-11-7-three-lines-of-defense | What are the responsibilities of the second line of defence in model risk management?
> Independent model risk management and validation: effective challenge of design, implementation and use, independent testing and benchmarking, the model inventory, and findings that can restrict use or require reserves.
> SR 26-2 (17 April 2026) superseded SR 11-7: it requires effective challenge by objective experts with standing to effect change, but says validation quality depends on rigour rather than organisational structure, and has internal audit evaluate rather than duplicate validation.

> [!question]- risk-fhs-volatility-updating | How does Filtered Historical Simulation adapt historical return scenarios to the current regime?
> Divide each historical return by the volatility of its own day and multiply by today's: $r\,\sigma_{\text{now}}/\sigma_\tau$ (Hull and White 1998).
> With today's vol at 2.2%, a 3% fall on a 1% vol day becomes $-6.6\%$, while a 4.5% fall on a 3% vol day becomes $-3.3\%$: the ranking of historical days reverses.

> [!question]- risk-reverse-stress-testing-mahalanobis | How does reverse stress testing identify the most plausible scenario triggering a given loss?
> Minimise the Mahalanobis distance $\sqrt{x^\top\Sigma^{-1}x}$ subject to the loss; for a linear book the answer is $x^* = -L\,\Sigma\delta/(\delta^\top\Sigma\delta)$ at distance $L/\sqrt{\delta^\top\Sigma\delta}$.
> In Problem 4 a 2.5m loss is reached most plausibly by equity $-1.79\%$ and yields $+42.86$bp, at distance 6.0994; nonlinear books need numerical search and several starting points.

> [!question]- risk-expected-maximum-drawdown-analytics | How does expected maximum drawdown scale with Sharpe ratio, volatility and horizon?
> With positive drift it grows only logarithmically: the Magdon-Ismail asymptote is $(\sigma/2S)(\ln(S^2T/2) + 1.9635)$; with zero drift it grows like $\sqrt{\pi/2}\,\sigma\sqrt T$.
> At Sharpe 1.2 and 12% vol, the exact expectation is 0.1319 at two years against an asymptote of 0.1164, and 0.2022 against 0.1969 at ten; with zero drift it is 0.2127 at two years.
> Use the exact series for short records; the asymptote undershoots.

> [!question]- risk-vanna-volga-pnl-attribution | Why are Vanna and Volga needed in options P&L attribution?
> On days when spot and implied vol move together, the cross term $\text{vanna}\,\Delta S\,\Delta\sigma$ and the vol convexity $\tfrac12\text{volga}\,\Delta\sigma^2$ are first-order visible.
> In Problem 6 (spot +2, vol $-2.5$ points on 1,000 calls) they add 14.07 and 3.08 and cut the unexplained P&L from 26.21 to 9.06.

> [!question]- risk-black-scholes-daily-breakeven-rule-of-16 | Derive the daily break-even move for a delta-hedged option and explain the Rule of 16.
> From $\Theta + \tfrac12\sigma^2S^2\Gamma = 0$, one day's theta is $\tfrac12\sigma^2S^2\Gamma\Delta t$; equating to $\tfrac12\Gamma\Delta S^2$ gives $|\Delta S| = \sigma S\sqrt{\Delta t}$.
> With 252 trading days $\sqrt{252} = 15.875 \approx 16$: for $S = 500$ and 18% vol, 5.6695 exactly and 5.625 by the rule.

> [!question]- risk-lvar-spread-cost-and-scaling | How does Liquidity-Adjusted VaR account for spread costs and a multi-day liquidation horizon?
> Add half the stressed relative spread times the position, $\tfrac12 V(\bar s + a\sigma_s)$, and scale the 1-day VaR for the days the position is still held.
> With equal daily sales the variance factor is $(L+1)(2L+1)/(6L)$ (1.2472 in sd for $L = 3$); the often-quoted $\sqrt{1 + (L-1)/3}$ assumes one full day and then continuous selling; in Problem 22 the total is 2,260,200 on a 1.5m VaR.

> [!question]- risk-pca-yield-curve-factor-shocks | How are principal components interpreted for a yield curve, and how are factor shocks built?
> The first components are usually level, slope and curvature (see [Risk Factor Modelling](10-Risk-Factor-Modelling.md)); a shock of $k$ sds along component $i$ is $k\sqrt{\lambda_i}\,v_i$.
> In Problem 8, $1.5\sqrt{0.00018} \times 0.57735 = 116.19$bp per tenor, and its Mahalanobis distance is exactly 1.5.

> [!question]- risk-kva-capital-valuation-adjustment | What is Capital Valuation Adjustment (KVA), and how is it priced into OTC derivatives?
> The cost of the return required on regulatory capital held over the trade's life, $\int h\,E[D(t)K_t]\,dt$, with $K_t$ simulated (SA-CCR, CVA capital, market risk on hedges) and $h$ a management-set hurdle.
> A midpoint shortcut with flat capital of 500k at 10% over five years gives 227,500; with a simulated, decaying capital profile the 10m 5-year swap in [XVA](15-XVA.md) carries about 18,130.

> [!question]- risk-short-gamma-proxy-crash | A risk system uses delta-gamma for a book short at-the-money puts. In a 25% crash, is the proxy loss too high or too low?
> Too low here: full revaluation loses 15.5166 per put, the proxy 14.9424.
> The error is third order, so its sign depends on $V'''$; for a long call the proxy overstated large-move losses in the stress run of [Sensitivities](12-Sensitivities-and-Revaluation.md).
> Never assume the direction; revalue stress scenarios in full.

> [!question]- risk-eepe-discrete-weights | EE at 0.5 and 1 year is 80k and 120k with zero today. What is Effective EPE, and what do people get wrong?
> 100,000: CRE53.13 sums Effective EE at each grid date times $\Delta t_k$ over the first year, $0.5 \times 80\text{k} + 0.5 \times 120\text{k}$.
> A trapezoid gives 70,000, 30% lower; use the regulatory weights for regulatory numbers.

> [!question]- risk-wwr-two-state | Exposure is 10m with probability 10% and 1m otherwise, PD 1%, LGD 60%. What is CVA if every default happens in the bad state?
> 60,000, against 11,400 if default is independent of the state: 5.26 times as much with identical PD and exposure distribution.
> Wrong-way risk is about the joint distribution, which marginal inputs cannot reveal.

> [!question]- risk-ac-discrete-kappa | Why does the discrete Almgren-Chriss schedule use $\cosh(\kappa\tau) = 1 + \tfrac12\tilde\kappa^2\tau^2$ rather than $\kappa = \tilde\kappa$?
> The first-order conditions are a second-order difference equation whose solutions are $e^{\pm\kappa t_k}$ with that $\kappa$; $\kappa \to \tilde\kappa$ only as $\tau \to 0$.
> With $\tilde\kappa = 2$ and daily steps $\kappa = 1.762747$: day-1 sales of 414,286, against 432,355 from the continuous formula.

> [!question]- risk-xva-midpoint-shortcut | Is $\text{MVA} \approx s \cdot E[\text{IM}] \cdot P(0, T/2) \cdot T$ a good approximation?
> For the discounting, yes: with $P(0, 2.5) = 0.910$ the integral $\int_0^5 e^{-rt}dt = 4.5567$ against 4.55, so 109,362 against 109,200.
> The real error is assuming flat IM: initial margin and capital decay as the trade ages, which is why engines simulate the profiles.

> [!question]- risk-forward-pfe-closed-form | Give the 95% PFE at one year of a par forward with vol 30% and notional 10m (zero rates).
> $N(e^{-\sigma^2/2 + \sigma z_{0.95}} - 1) = 5{,}658{,}927$, against an EE of 1,192,354.
> The PFE is the quantile of $\max(V, 0)$, valid as a closed form because more than 5% of outcomes are positive.

> [!question]- risk-ngr-four-trades | Trades worth +20, -15, +5 and -2 with one counterparty: what are NGR and the standardised IM scaling?
> Gross 25, net 8, NGR 0.32; the standardised schedule scales gross IM by $0.4 + 0.6 \times 0.32 = 0.592$ (MGN20.17).

> [!question]- risk-cva-flat-exposure | One-year trade, flat EE 500k, hazard 3%, LGD 60%, rate 4%. Estimate CVA two ways.
> Midpoint: $0.6 \times e^{-0.02} \times 500\text{k} \times (1 - e^{-0.03}) = 8{,}691$; exact integral $0.6 \times 500\text{k} \times 0.03(1 - e^{-0.07})/0.07 = 8{,}692$.
> The credit-triangle shortcut with spread 1.8% gives 8,823, too high because it ignores survival.

> [!question]- risk-bgk-barrier-shift | How do you price a daily-monitored barrier with a continuous-monitoring formula?
> Shift the barrier away from spot by $e^{\mp 0.5826\sigma\sqrt{\Delta t}}$ (Broadie, Glasserman and Kou 1997): 90 becomes 89.3418 for 20% vol and daily monitoring.
> In [Liquidity and Model Risk](16-Liquidity-and-Model-Risk.md) the shifted formula gives 8.9139 for a down-and-out call against 8.6655 unshifted, matching a daily Monte Carlo.

> [!question]- risk-erc-two-asset-any-correlation | Two assets have vols 15% and 25%. What equal-risk-contribution weights do correlations of -0.5, 0 and 0.8 give?
> 0.625 and 0.375 in every case: with two assets equal contributions force $w_1\sigma_1 = w_2\sigma_2$, so correlation drops out.

## In this repo and SDE-Interview-Prep

- [risk_problem_set.py](code/risk_problem_set.py): every problem above, reusing [drawdowns.py](code/drawdowns.py), [risk_sensitivities.py](code/risk_sensitivities.py), [risk_decomposition.py](code/risk_decomposition.py), [risk_ccr_analytics.py](code/risk_ccr_analytics.py) and [risk_liquidity_model.py](code/risk_liquidity_model.py).
- Numbers quoted from other notes in the cards (the swap peak, DVA and FVA of the XVA example, KVA of the simulated swap, the barrier prices) are asserted by [risk_ccr_analytics.py](code/risk_ccr_analytics.py), [risk_xva_pricing.py](code/risk_xva_pricing.py), [risk_sensitivities.py](code/risk_sensitivities.py) and [risk_liquidity_model.py](code/risk_liquidity_model.py).
- Notes: [Kelly](01-Kelly-Criterion-and-Position-Sizing.md), [VaR and ES](03-VaR-and-Expected-Shortfall.md), [Stress Testing](04-Stress-Testing-and-Scenarios.md), [Drawdowns](05-Drawdowns-and-Risk-Limits.md), [P&L Attribution](06-PnL-Attribution-and-Greek-Risk.md), [Sensitivities](12-Sensitivities-and-Revaluation.md), [Risk Decomposition](13-Risk-Decomposition-and-Attribution.md), [CCR Analytics](14-Counterparty-Credit-Risk-Analytics.md), [XVA](15-XVA.md), [Liquidity and Model Risk](16-Liquidity-and-Model-Risk.md).

## Further reading

- P. Jorion, *Value at Risk*, 3rd edition, McGraw-Hill 2006.
- J. Gregory, *The xVA Challenge*, 4th edition, Wiley 2020.
- R. Almgren and N. Chriss, "Optimal execution of portfolio transactions", *Journal of Risk* 3(2), 5-39, 2000.
- M. Magdon-Ismail, A. Atiya, A. Pratap and Y. Abu-Mostafa, "On the maximum drawdown of a Brownian motion", *Journal of Applied Probability* 41(1), 147-161, 2004.
- J. Hull and A. White, "Incorporating volatility updating into the historical simulation method for value-at-risk", *Journal of Risk* 1(1), 5-19, 1998.
- M. Broadie, P. Glasserman and S. Kou, "A continuity correction for discrete barrier options", *Mathematical Finance* 7(4), 325-349, 1997.
- Basel Committee on Banking Supervision, Basel Framework CRE52, CRE53 and MGN20.
