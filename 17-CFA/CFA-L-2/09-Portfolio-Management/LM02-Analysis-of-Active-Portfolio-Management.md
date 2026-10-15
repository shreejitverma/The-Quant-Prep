---
type: cfa-lm
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
volume: 9
lm: 2
title: "Analysis of Active Portfolio Management"
pages: "91-153"
weight_band: "10-15%"
difficulty: 3
los_count: 6
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/portfolio-management]
---

# LM2: Analysis of Active Portfolio Management

Difficulty 3 of 5: the whole module is one multiplicative identity applied over and over, but the exam mixes four look-alike ratios (SR, IR, IC, TC), tests square-root-of-breadth arithmetic under time pressure, and loves the Sharpe-vs-information-ratio property table where every cell is a plausible distractor.

## LOS map

- **describe** how value added by active management is measured (V9 p.91) ^los-09-02-a
    - Examiner asks: compute value added from a table of portfolio weights, benchmark weights, and returns, then decompose it into an asset allocation piece (active weights times benchmark returns) and a security selection piece (portfolio weights times sub-portfolio value added).
- **calculate** and interpret the information ratio (ex post and ex ante) and contrast it to the Sharpe ratio (V9 p.91) ^los-09-02-b
    - Examiner asks: divide active return by active risk, then decide which of two statements about cash and aggressiveness is correct; the Sharpe ratio survives cash and leverage while the unconstrained information ratio survives scaling of active weights, and mixing the two properties up is the standing trap.
- **describe** and interpret the fundamental law of active portfolio management, including its component terms, transfer coefficient, information coefficient, breadth, and active risk (aggressiveness) (V9 p.91) ^los-09-02-c
    - Examiner asks: match each component to its definition (IC is forecasts vs realized returns, TC is forecasts vs weights taken, BR is independent decisions per year, sigma_A is aggressiveness), then multiply TC times IC times the square root of BR times sigma_A to get expected active return.
- **explain** how the information ratio may be useful in investment manager selection and choosing the level of active portfolio risk (V9 p.91) ^los-09-02-d
    - Examiner asks: pick the manager with the highest expected IR regardless of active risk level, compute the combined Sharpe ratio as the square root of SR_B squared plus IR squared, and size the optimal active risk as (IR/SR_B) times sigma_B including the benchmark weight needed to get there.
- **compare** active management strategies, including market timing and security selection, and evaluate strategy changes in terms of the fundamental law of active management (V9 p.91) ^los-09-02-e
    - Examiner asks: convert a market timer's accuracy into IC = 2(% correct) - 1, contrast a high-IC low-BR sector rotator with a low-IC high-BR stock picker, and predict what a change (more securities, more frequent rebalancing, new constraints) does to BR, TC, and hence the IR.
- **describe** the practical strengths and limitations of the fundamental law of active management (V9 p.91) ^los-09-02-f
    - Examiner asks: explain why a naive BR = securities times periods overstates breadth (cross-sectional and time-series dependence), why ex ante IC is uncertain and biased upward, and which stated limitation is the weakest answer (constraints, because TC already handles them).

## Core intuition

Active management exists because someone believes markets are not perfectly efficient and that their own forecasts beat the consensus (V9 p.92).
Once asset management is delegated and cheap index funds exist, the only defensible scorecard is performance relative to a benchmark, not absolute performance (V9 p.92).
So the module builds everything on relative quantities: active weights (portfolio weight minus benchmark weight), active returns (asset return minus benchmark return), and active risk (the volatility of the portfolio-minus-benchmark return difference) (V9 p.94, p.101).
A benchmark qualifies for this role only if it is representative of the manager's opportunity set, replicable at low cost, and verifiable ex ante with timely returns ex post (V9 p.93).
When the benchmark is a float-adjusted capitalization-weighted total market index, active management is a zero-sum game before costs, because the market portfolio is the average of all investors; for narrower benchmarks the game is not zero sum since managers can go outside the index (V9 p.93).

> [!abstract] Idea 1: value added is a covariance between what you did and what happened
> Value added is $R_A = \sum \Delta w_i R_{Ai}$: you make money if and only if the assets you overweighted beat the benchmark and the assets you underweighted lagged it (V9 p.94).
> Algebraically this sum is $N$ times the covariance between active weights and realized active returns, which is why every parameter in this module is some correlation (V9 p.109).
> Hold every asset at its benchmark weight and value added is identically zero, whatever returns do (V9 p.97).

The first practical payoff is performance attribution.
A composite portfolio's total value added splits into an asset allocation term, active class weights times benchmark class returns, plus a security selection term, portfolio class weights times the value added inside each class (V9 p.96).
The split is slightly arbitrary (the interaction effect is assigned to selection), but it answers the question the exam always asks: how much of the 2018 loss came from tilting toward equities versus picking bad stocks (V9 p.96).
In the curriculum's own illustration, a 68/32 Fidelity/PIMCO investor against a 60/40 policy lost 0.8% to security selection and 0.4% to the allocation tilt, for a total of -1.2%, which reconciles exactly with portfolio return minus policy return (V9 p.96, p.97).

The second building block is the pair of reward-to-risk ratios.
The Sharpe ratio divides excess return over the risk-free rate by total volatility; it is an absolute measure (V9 p.97).
The information ratio divides active return by active risk; it is a relative measure, and it can be read as the consistency of value added, since investors prefer steady outperformance to lumpy outperformance (V9 p.100).
Both come in ex ante (expected) and ex post (realized) flavors, and both are conventionally annualized, multiplying mean monthly returns by 12 and monthly volatility by the square root of 12 (V9 p.97, p.98).
Two term-of-art portfolios anchor the distinction: a closet index fund has a Sharpe ratio close to the benchmark's, tiny active risk, and an IR near zero or negative after fees, while a market-neutral long-short fund benchmarked to the risk-free rate has identical SR and IR because excess return equals active return and total risk equals active risk (V9 p.101).

> [!abstract] Idea 2: cash moves the Sharpe ratio's inputs proportionally, aggressiveness moves the information ratio's inputs proportionally
> Blend an active fund with cash and both the excess return and the volatility scale by the fund weight, so the Sharpe ratio is untouched; leverage is the same statement with a weight above one (V9 p.99).
> Multiply every active weight by a constant $c$ and both active return and active risk scale by $c$, so the unconstrained IR is untouched; the same trick works from outside by mixing the fund with the benchmark portfolio (V9 p.102).
> But cross the wires and both statements fail: adding cash shrinks the IR, and aggressiveness does change a constrained portfolio's IR because binding constraints drag the transfer coefficient down (V9 p.102, p.125).

Why care about the IR at all?
Because of one clean optimality result: properly combined with the benchmark, the best achievable squared Sharpe ratio is the benchmark's squared Sharpe ratio plus the squared information ratio, $SR_P^2 = SR_B^2 + IR^2$ (V9 p.103).
The active portfolio with the highest IR therefore delivers the highest Sharpe ratio to the end investor, which makes the expected IR the single best criterion for choosing among active managers sharing a benchmark, and the ex post IR the best criterion for grading them afterwards (V9 p.103, p.107).
The same mean-variance condition pins down how aggressive to be: the optimal active risk is $\sigma_A = (IR/SR_B)\sigma_B$ (V9 p.103).
A skilled manager (high IR) deserves more tracking risk; as IR falls toward zero the optimal active risk collapses to zero and you should simply index (V9 p.106).
If the fund arrives with the wrong amount of active risk, you do not need to re-engineer its holdings; a long or short position in the benchmark rescales active risk and active return together, preserving the IR (V9 p.102, p.104).

> [!abstract] Idea 3: the fundamental law factorizes skill into four multiplicative parts
> Expected active return is $E(R_A) = TC \times IC \times \sqrt{BR} \times \sigma_A$: how faithfully you implement (TC), how well you forecast (IC), how many independent bets you make per year (BR), and how hard you press (sigma_A) (V9 p.115).
> The correlation triangle makes the first two concrete: IC is the correlation between forecasts and realized active returns (signal quality), TC is the correlation between forecasts and the active weights actually taken (portfolio construction), and value added sits on the base of the triangle between weights and realizations (V9 p.108, p.109).
> Breadth enters under a square root, so skill scales linearly but diversification of bets only with the root: doubling your IC doubles expected alpha, doubling your independent decisions multiplies it by 1.41 (V9 p.112).

The machinery behind the law is worth two minutes because the exam tests its joints.
Forecasts are standardized through the Grinold rule, $\mu_i = IC \cdot \sigma_i \cdot S_i$, alpha equals skill times volatility times score, which sizes expected active returns to be modest when the assumed IC is modest (V9 p.110).
Mean-variance optimization then yields active weights proportional to $\mu_i / \sigma_i^2$, scaled up by the desired portfolio active risk: bigger forecasts get bigger weights, riskier names get smaller weights, and more aggressiveness scales everybody up (V9 p.110).
Substituting optimal weights back into the expected value added gives the basic law $E(R_A)^* = IC\sqrt{BR}\,\sigma_A$, and dividing by sigma_A gives the unconstrained information ratio $IR^* = IC\sqrt{BR}$ (V9 p.112).
Real portfolios cannot hold the optimal weights: long-only rules, turnover limits, ESG screens, and position caps push actual weights away from optimal ones, and the transfer coefficient, typically 0.20 to 0.90 in practice, multiplies straight through the law (V9 p.114, p.131).
TC also degrades the optimal aggressiveness, $\sigma_A = TC (IR^*/SR_B)\sigma_B$, and caps the achievable Sharpe improvement at $SR_B^2 + TC^2 (IR^*)^2$; at TC = 0 you should hold the benchmark (V9 p.116, p.117).

Ex post, the same law grades what actually happened.
Replace the expected IC with the realized information coefficient $IC_R$ and you get the value added the portfolio should have delivered given that period's forecasting success; the residual is constraint-induced noise (V9 p.117).
The variance split is stark: only $TC^2$ of the variation in realized performance is attributable to forecasting skill, and $1 - TC^2$ is noise from constraints, so a TC = 0.6 manager has 64% of period-to-period performance driven by luck-like noise, and good quarters prove little (V9 p.117).

Applications turn the crank on the same four dials (V9 p.119).
The global equity example shows an essentially unconstrained 120/20 long-short fund achieving TC of 0.995 and IR of 0.49, then watches the long-only and 10% position-cap versions grind TC down to 0.694 and then 0.567 as active risk is pushed from 2% to 3%, an IR decay from 0.49 to 0.34 to 0.28 (V9 p.120, p.124).
That is the key concept in one exhibit: an unconstrained IR is invariant to aggressiveness, but a constrained IR falls as aggressiveness rises because the constraints bind harder (V9 p.125).
The fixed-income credit-timing example shows the other extreme: a single quarterly binary bet (IG versus HY) has breadth of only 4, so even 55% accuracy, IC = 0.10, earns an IR of just 0.20; the timer needs either implausibly high accuracy or genuinely independent higher-frequency decisions to compete with a 100-stock picker (V9 p.126, p.127).
Breadth itself needs care: correlated bets shrink it below the security count via $BR = N/[1 + (N-1)\rho]$, negatively correlated near-arbitrage positions can inflate it far above N, and rebalancing more often adds breadth only when successive forecasts are truly independent (V9 p.127, p.133).

The limitations close the loop (V9 p.132).
The law ignores transaction costs and taxes, inherits every weakness of mean-variance optimization, and leans on two fragile inputs: the ex ante IC, which managers overestimate and which varies over time, and independence assumptions that make naive breadth counts like 500 stocks times 12 months into fantasy (V9 p.132, p.133, p.134).
Qian and Hua's strategy-risk refinement makes the first limitation quantitative: uncertainty about the IC adds risk of its own, $\sigma_A = \sigma_{IC}\sqrt{N}\sigma_{RM}$, and realized information ratios come in at roughly 45% to 91% of naive fundamental-law estimates (V9 p.132).

## Formulas and derivations

**Benchmark and portfolio returns** (V9 p.93)
$$
R_B = \sum_{i=1}^{N} w_{B,i} R_i, \qquad R_P = \sum_{i=1}^{N} w_{P,i} R_i
$$
^f-09-02-1

- $w_{B,i}$, $w_{P,i}$: benchmark and portfolio weights of security $i$ (decimals summing to 1); $R_i$: total return on security $i$.
- Securities outside either portfolio simply carry weight zero in that summation, so the same $N$ serves both (V9 p.93).
- These are definitions, not results; every later formula differences them.

**Value added (active return)** (V9 p.93, p.94)
$$
R_A = R_P - R_B = \sum_{i=1}^{N} \Delta w_i R_i = \sum_{i=1}^{N} \Delta w_i R_{Ai}
$$
^f-09-02-2

- $\Delta w_i = w_{P,i} - w_{B,i}$: active weight (sums to zero across $i$); $R_{Ai} = R_i - R_B$: active security return.
- Subtract the two summations in formula 1 and the common returns factor out against the weight differences.
- The last equality holds because $\sum \Delta w_i R_B = R_B \sum \Delta w_i = 0$; value added is positive exactly when overweights beat the benchmark and underweights lag it (V9 p.94).
- Equivalently $R_A = N \times \mathrm{COV}(\Delta w_i, R_{Ai})$ since both series have zero cross-sectional means (V9 p.109).

**Alpha versus active return** (V9 p.94)
$$
\alpha_P = R_P - \beta_P R_B \qquad \text{vs.} \qquad R_A = R_P - R_B
$$
^f-09-02-3

- $\beta_P$: beta of the managed portfolio against the benchmark.
- Alpha is the beta-adjusted (risk-adjusted) value added; calling plain active return "alpha" implicitly assumes $\beta_P = 1$ (V9 p.94).
- The module's IR likewise assumes beta 1; Grinold and Kahn's beta-adjusted counterpart of active risk is "residual risk" (V9 p.100).

**Decomposition of value added** (V9 p.96)
$$
R_A = \sum_{j=1}^{M} \Delta w_j R_{B,j} + \sum_{j=1}^{M} w_{P,j} R_{A,j}
$$
^f-09-02-4

- $j = 1 \dots M$: asset classes; $\Delta w_j$: active class weight against the policy portfolio; $R_{B,j}$: benchmark return of class $j$; $R_{A,j} = R_{P,j} - R_{B,j}$: value added inside class $j$.
- Start from $R_A = \sum w_{P,j} R_{P,j} - \sum w_{B,j} R_{B,j}$, add and subtract $\sum w_{P,j} R_{B,j}$, and regroup.
- First term is the asset allocation decision, second is security selection; the interaction effect is assigned (arbitrarily) to selection (V9 p.96).

**Sharpe ratio** (V9 p.97)
$$
SR_P = \frac{R_P - R_F}{\sigma_P}
$$
^f-09-02-5

- $R_F$: risk-free rate; $\sigma_P$: total volatility of the portfolio return; both numerator and denominator annualized (monthly mean times 12, monthly volatility times $\sqrt{12}$) (V9 p.98).
- Ex ante, use $E(R_P)$ and forecast volatility; ex post, use sample averages and the sample standard deviation over the same window for every fund compared (V9 p.97, p.98).
- Long-run equity benchmark Sharpe ratios historically run about 0.20 to 0.60 (V9 p.98).

**Sharpe ratio is unaffected by cash or leverage** (V9 p.99)
$$
SR_C = \frac{R_C - R_F}{\sigma_C} = \frac{w_P (R_P - R_F)}{w_P \sigma_P} = SR_P
$$
^f-09-02-6

- $w_P$: weight in the risky portfolio, $1 - w_P$ in cash; $R_C = w_P R_P + (1-w_P) R_F$ and $\sigma_C = w_P \sigma_P$ because cash is riskless.
- The fund weight cancels top and bottom; with $w_P > 1$ the cash weight is negative (leverage) and the identity still holds (V9 p.99).
- This is the engine of two-fund separation: pick the highest-Sharpe risky portfolio, then set total risk with cash or leverage to taste (V9 p.99).

> [!tip] Calculator
> Combined-portfolio checks are chained arithmetic: for 64% Growth Fund of America (11.1%, 15.7%) and 36% cash at 2.3%: `.64 x 11.1 + .36 x 2.3 = ` 7.93, `- 2.3 = / (.64 x 15.7) =` about 0.56, matching the fund's own Sharpe ratio (V9 p.99).

**Information ratio** (V9 p.101)
$$
IR = \frac{R_P - R_B}{\sigma(R_P - R_B)} = \frac{R_A}{\sigma_A}
$$
^f-09-02-7

- $\sigma_A$: active risk (benchmark tracking risk), the standard deviation of the return difference, annualized like the Sharpe ratio.
- Ex ante, the numerator is $E(R_P) - E(R_B)$ over expected active risk; ex post, realized average active return over the sample standard deviation of active returns (V9 p.101).
- Interpreted as the consistency of active return; under the zero-sum property the average realized IR across funds sharing a benchmark is about zero, and realized 25-year IRs cluster within roughly -0.30 to +0.30 (V9 p.101).

**Information ratio is unaffected by aggressiveness (unconstrained)** (V9 p.102)
$$
R_C = \sum_{i=1}^{N} c\,\Delta w_i R_{Ai} = c R_A, \qquad IR_C = \frac{c R_A}{c \sigma_A} = IR
$$
^f-09-02-8

- $c$: any positive constant multiplying every active weight.
- Both active return and active risk scale linearly in $c$, so the ratio is invariant; an outside investor achieves the same rescaling by mixing the fund with the benchmark, e.g. an 80/20 fund/benchmark mix cuts a 5.0% active risk to 4.0% (V9 p.102).
- Contrast with cash: adding cash changes active return and active risk non-proportionally against a risky benchmark, so the IR generally shrinks (V9 p.102).

**Combined squared Sharpe ratio** (V9 p.103)
$$
SR_P^2 = SR_B^2 + IR^2
$$
^f-09-02-9

- Holds when the active portfolio is combined with the benchmark at the optimal level of active risk; active return is uncorrelated with the benchmark return, so the two reward-to-risk contributions add in squares like orthogonal legs.
- Implication: the highest-IR fund produces the highest achievable Sharpe ratio, making expected IR the single best manager-selection criterion for a given benchmark (V9 p.103).
- Caution: squaring destroys the sign, so the formula is not usable for ranking negative-IR funds (V9 p.103).

> [!tip] Calculator
> BA II Plus: `.44 x^2 + .35 x^2 = ` then `sqrt(x)` gives 0.56 for $SR_B = 0.44$, $IR = 0.35$.

**Optimal amount of active risk (unconstrained)** (V9 p.103)
$$
\sigma_A^{*} = \frac{IR}{SR_B}\,\sigma_B
$$
^f-09-02-10

- $\sigma_B$: total risk of the benchmark; multiply the right side by the portfolio's benchmark beta if it differs from 1 (V9 p.103).
- Derivation: mean-variance optimality equates marginal reward per unit variance across the two return sources, $E(R_A)/\sigma_A^2 = E(R_B - R_F)/\sigma_B^2$; substitute $E(R_A) = IR\,\sigma_A$ and $E(R_B - R_F) = SR_B\,\sigma_B$ and solve for $\sigma_A$ (V9 p.103).
- If the fund's delivered active risk differs, hold it at weight $\sigma_A^{*}/\sigma_A^{fund}$ with the balance (possibly negative) in the benchmark (V9 p.104, p.107).

**Total risk of the active portfolio** (V9 p.104)
$$
\sigma_P^2 = \sigma_B^2 + \sigma_A^2
$$
^f-09-02-11

- Benchmark return variance and active return variance add because active return is uncorrelated with the benchmark under the beta-1 assumption.
- Used to verify the combined Sharpe ratio: at $IR = 0.30$, $SR_B = 0.40$, $\sigma_B = 16\%$, optimal $\sigma_A = 12\%$, total excess return is $6.4 + 3.6 = 10.0\%$, total risk $\sqrt{16^2 + 12^2} = 20\%$, and $SR = 0.50 = \sqrt{0.40^2 + 0.30^2}$ (V9 p.103, p.104).

**Mean-variance optimal active weights** (V9 p.110)
$$
\Delta w_i^{*} = \frac{\mu_i}{\sigma_i^2}\cdot\frac{\sigma_A}{\sqrt{\sum_{i=1}^{N} \mu_i^2/\sigma_i^2}}
$$
^f-09-02-12

- $\mu_i$: forecasted (subjective expected) active return of security $i$; $\sigma_i$: forecasted volatility of security $i$'s active return; assumes uncorrelated active returns.
- Weights rise with the forecast, fall with security-level risk, and scale with the portfolio active risk budget $\sigma_A$ (V9 p.110).
- This is the maximum expected active return portfolio subject to the active risk limit; it is the solution the transfer coefficient later measures shortfall against.

**Grinold rule for scaling forecasts** (V9 p.110)
$$
\mu_i = IC\,\sigma_i S_i
$$
^f-09-02-13

- $S_i$: standardized scores with cross-sectional variance 1 (e.g. +2, +1, 0, -1, -2 scheme); alpha equals skill times volatility times score.
- A low assumed IC compresses forecasted active returns toward zero, keeping expected alphas honest relative to claimed skill (V9 p.110).
- Ambitious score patterns (betting positively-correlated assets move oppositely) raise the effective IC used in fundamental-law accounting; timid patterns lower it, as in the 0.20 assumed vs 0.12 effective IC of the Treasury ladder example (V9 p.122, p.129).

**Optimal active weights under the Grinold rule** (V9 p.110)
$$
\Delta w_i^{*} = \frac{\mu_i}{\sigma_i^2}\cdot\frac{\sigma_A}{IC\sqrt{BR}}
$$
^f-09-02-14

- Substitute formula 13 into formula 12; with $BR = N$ the messy square-root term collapses into $IC\sqrt{BR}$.
- $BR$: breadth, the number of independent decisions per year, replacing the raw count $N$ (V9 p.110).

**Information coefficient (risk-weighted)** (V9 p.110)
$$
IC = \rho\!\left(\frac{R_{Ai}}{\sigma_i},\; \frac{\mu_i}{\sigma_i}\right)
$$
^f-09-02-15

- Cross-sectional correlation between risk-deflated realized active returns and risk-deflated forecasts; range -1 to +1, with values below 0.20 the practical norm (V9 p.110).
- Ex ante IC must be positive or the investor should index; realized (ex post) $IC_R$ can be negative and drives realized value added (V9 p.110).
- If all securities share one residual volatility, the risk weighting drops out and IC is the plain correlation of forecasts with outcomes (V9 p.115).

**Basic fundamental law** (V9 p.112)
$$
E(R_A)^{*} = IC\sqrt{BR}\,\sigma_A, \qquad IR^{*} = IC\sqrt{BR}
$$
^f-09-02-16

- Plug the optimal weights (formula 14) and the Grinold forecasts (formula 13) into $E(R_A) = \sum \Delta w_i \mu_i$; the algebra assumes $BR = N$ uncorrelated bets.
- Skill enters linearly, breadth only under a square root: quadrupling independent decisions merely doubles the IR (V9 p.112).
- The * marks the unconstrained optimal construction; it is the ceiling the transfer coefficient discounts.

**Transfer coefficient** (V9 p.114)
$$
TC = \rho\!\left(\frac{\mu_i}{\sigma_i},\; \Delta w_i \sigma_i\right) = \rho\!\left(\Delta w_i^{*}\sigma_i,\; \Delta w_i \sigma_i\right)
$$
^f-09-02-17

- Risk-weighted cross-sectional correlation between forecasted active returns and the active weights actually taken; equivalently between optimal and actual active weights, since optimal weights are proportional to $\mu_i/\sigma_i^2$ (V9 p.114).
- Note the risk adjustment goes opposite ways: forecasts are divided by $\sigma_i$, weights are multiplied by $\sigma_i$.
- Range -1 to +1; unconstrained portfolios sit near 1.00, practice runs about 0.20 to 0.90, and TC can even go negative when a portfolio badly needs rebalancing (V9 p.114, p.115, p.131).

**Full (expanded) fundamental law** (V9 p.115)
$$
E(R_A) = TC \times IC \times \sqrt{BR}\,\sigma_A, \qquad IR = TC \times IC \times \sqrt{BR}
$$
^f-09-02-18

- Constraints scale the whole expected value added by TC: a TC of 0.60 delivers 60% of the unconstrained alpha and IR (V9 p.115, p.131).
- All four parameters multiply, so halving any one halves expected active return; only breadth hides under the root.
- Assumes a single-index risk model with uncorrelated residual active returns; richer risk models keep the same form with more complex parameter measurements (V9 p.115).

> [!tip] Calculator
> The law is four keystrokes: for TC 0.80, IC 0.05, BR 100, sigma_A 4%: `100 sqrt(x) x .80 x .05 x 4 =` 1.6% expected active return (V9 p.118).

**Optimal aggressiveness and Sharpe ratio with constraints** (V9 p.116)
$$
\sigma_A = TC\,\frac{IR^{*}}{SR_B}\,\sigma_B, \qquad SR_P^2 = SR_B^2 + TC^2 (IR^{*})^2
$$
^f-09-02-19

- $IR^{*}$: the information ratio of the otherwise unconstrained strategy (formula 16).
- Replace $IR$ with $TC \times IR^{*}$ in formulas 9 and 10; constraints shrink both the optimal tracking risk and the achievable Sharpe improvement by the factor TC (squared, for the Sharpe term).
- At TC = 0 the optimal active risk is zero: just buy the benchmark (V9 p.117).

**Ex post attribution: conditional value added, noise, and the variance split** (V9 p.117)
$$
E(R_A \mid IC_R) = TC \times IC_R \times \sqrt{BR}\,\sigma_A, \qquad R_A = E(R_A \mid IC_R) + \text{Noise}
$$
^f-09-02-20

- $IC_R$: realized information coefficient for the period; the conditional term is the value added the period's actual forecasting success should have produced.
- The noise term is constraint-induced: variance decomposes with proportion $TC^2$ from variation in realized IC (forecasting success) and $1 - TC^2$ from noise (V9 p.117).
- A TC = 0.60 manager gets only 36% of performance variation from skill realization, so low-TC investors regularly see good forecasting with bad performance and vice versa (V9 p.117).

**Market timing information coefficient** (V9 p.127)
$$
IC = 2 \times (\%\ \text{correct}) - 1
$$
^f-09-02-21

- For dichotomous (+1/-1) calls: with unit-variance zero-mean score series, the time-series correlation equals the fraction correct minus the fraction incorrect (V9 p.127).
- A 55% accurate timer has IC = 0.10; a coin flipper has IC = 0; perfect foresight has IC = 1.
- With quarterly calls, BR = 4 and $IR = 0.10\sqrt{4} = 0.20$; the timer needs genuinely independent monthly ($IR = 0.35$) or daily ($IR = 1.58$) calls at the same accuracy to compete (V9 p.127, p.128).

**Breadth with correlated decisions (rule of thumb)** (V9 p.133)
$$
BR = \frac{N}{1 + (N-1)\rho}
$$
^f-09-02-22

- $\rho$: common correlation across the active returns in the risk model.
- $\rho = 0$ gives $BR = N$; positive correlation shrinks breadth (industry bets are one decision, not thirty); negative correlation expands it, e.g. $N = 2$, $\rho = -0.8$ gives $BR = 2/0.2 = 10$, the near-arbitrage case (V9 p.133).
- Breadth need not be an integer, and time-wise it multiplies by rebalancing frequency only when successive forecasts are independent (V9 p.111, p.133).

**Strategy risk (Qian and Hua)** (V9 p.132)
$$
\sigma_A = \sigma_{IC}\sqrt{N}\,\sigma_{RM}, \qquad E(R_A) = \frac{IC}{\sigma_{IC}}\,\sigma_A
$$
^f-09-02-23

- $\sigma_{RM}$: tracking risk predicted by the risk model; $\sigma_{IC}$: volatility of the realized information coefficient over time (skill uncertainty); derived under TC = 1 and BR = N.
- Uncertainty about skill adds active risk beyond the risk model's estimate, so realized IRs land at roughly 45% to 91% of naive fundamental-law estimates (V9 p.132).
- The higher the uncertainty about forecasting ability, the smaller the likely value added (V9 p.133).

## Worked examples

**Text demonstration: 60/40 stock-bond tilt** (V9 p.94)
Benchmark 60/40 stocks/bonds; the manager holds 70/30; stocks return 14.0%, bonds 2.0%.
Portfolio return $0.70(14.0) + 0.30(2.0) = 10.4\%$; benchmark return $0.60(14.0) + 0.40(2.0) = 9.2\%$ (Python confirms 10.4 and 9.2).
Value added directly: $10.4 - 9.2 = 1.2\%$.
Via formula 2 with active returns: $0.10(14.0 - 9.2) - 0.10(2.0 - 9.2) = 0.48 + 0.72 = 1.2\%$, showing 0.5% from the stock overweight and 0.7% from the bond underweight (Python: 0.48 and 0.72).
Flip the stock return to -14.0%: portfolio -9.2%, benchmark -7.6%, and value added $0.10(-14.0) - 0.10(2.0) = -1.6\%$ (Python confirms).

**Example 1: value added and country equity markets** (V9 p.95)
MSCI EAFE benchmark, country allocator, 2018 returns: UK 17%/16% (-7.6%), Japan 25%/14% (-9.0%), France 11%/8% (-3.5%), Germany 9%/24% (-15.8%), Other 38%/38% (-0.1%).
Largest overweight: Germany, $24 - 9 = +15\%$; largest underweight: Japan, $14 - 25 = -11\%$.
Value added with active weights and total returns: $-0.01(-7.6) - 0.11(-9.0) - 0.03(-3.5) + 0.15(-15.8) = -1.2\%$ (Python: -1.199%, rounding to -1.2%).
"Other Countries" contributes nothing because its active weight is zero, and the relative-return version of formula 2 gives the same result (Python cross-check: $R_P = -6.586\%$, $R_B = -5.387\%$, difference -1.199%). ^ex-09-02-1

**Text demonstration: Fidelity/PIMCO attribution** (V9 p.96, p.97)
2018: Fidelity Magellan -5.6% vs S&P 500 -4.5%; PIMCO Total Return -0.3% vs Aggregate 0.0%; investor holds 68/32 against a 60/40 policy.
Security selection: fund value added is -1.1% and -0.3%; weighted, $0.68(-1.1) + 0.32(-0.3) = -0.8\%$ (Python: -0.844, the curriculum rounds to -0.8).
Asset allocation: active weights +8%/-8%, so $0.08(-4.5) - 0.08(0.0) = -0.4\%$ (Python: -0.36, rounded to -0.4).
Total $-0.8 - 0.4 = -1.2\%$, confirmed by portfolio return $0.68(-5.6) + 0.32(-0.3) = -3.9\%$ minus policy return $0.60(-4.5) + 0.40(0.0) = -2.7\%$ (Python: -3.904 and -2.700, difference -1.204, i.e. -1.2%).

**Text demonstration: two-fund separation with the Growth Fund of America** (V9 p.99)
Target 10% volatility from a fund with expected return 11.1%, volatility 15.7%, risk-free 2.3%.
Hold $10.0/15.7 = 64\%$ in the fund, 36% in cash: expected return $0.64(11.1) + 0.36(2.3) = 7.9\%$, volatility $0.64(15.7) = 10.0\%$, and Sharpe $(7.9 - 2.3)/10.0 = 0.56$, unchanged from the fund's 0.56 (Python: return 7.932, vol 10.048, SR 0.5605, matching the fund's unrounded $(11.1-2.3)/15.7 = 0.5605$).

**Example 2: adjusting risk and return using the Sharpe ratio** (V9 p.99, p.100)
Large cap: 8.2% return, 14.6% volatility, SR 0.40; small cap: 10.3%, 19.2%, SR 0.42; risk-free 2.3%.
Cash weight to bring small cap to large-cap risk: fund weight $14.6/19.2 = 76\%$, so 24% cash; combined volatility $0.76(19.2) = 14.6\%$ (Python: 0.7604 and 14.6).
The combined Sharpe ratio is unaffected by cash: still 0.42.
Combined expected return $0.76(10.3) + 0.24(2.3) = 8.4\%$, 20 bps above the large-cap 8.2% at identical risk; recheck $(8.4 - 2.3)/14.6 = 0.42$ (Python: 8.38, SR 0.4164, i.e. 0.42). ^ex-09-02-2

**Text demonstration: optimal aggressiveness at IR 0.30** (V9 p.103, p.104)
Fund: IR 0.30, active risk 8.0%; benchmark: excess return 6.4%, risk 16.0%, SR 0.40.
Optimal active risk (formula 10): $(0.30/0.40) \times 16.0 = 12.0\%$ (Python confirms).
At that aggressiveness the Sharpe ratio is $\sqrt{0.40^2 + 0.30^2} = 0.50$ (Python: 0.500).
Verification: active return $0.30 \times 12.0 = 3.6\%$, total excess $6.4 + 3.6 = 10.0\%$, total risk $\sqrt{16^2 + 12^2} = 20.0\%$, Sharpe $10/20 = 0.50$ (Python confirms all).
Getting there requires $12.0/8.0 = 1.5$ times the fund, funded by shorting the benchmark 0.5 times (V9 p.104).

**Example 3: expected value added based on the information ratio** (V9 p.106, p.107)
Fund I (Magellan-like): SR 0.38, active risk 5.1%, IR -0.27; Fund II (GFoA-like): SR 0.56, active risk 6.2%, IR 0.20; S&P 500: return 9.9%, risk 14.4%, SR 0.53, risk-free 2.3%.
1. Fund II is the better complement to the benchmark because it has the higher expected IR (0.20 vs -0.27), and expected IR is the criterion.
2. Sharpe improvement from Fund II: $\sqrt{0.53^2 + 0.20^2} = 0.57$ (Python: 0.5665, rounded 0.57), up from 0.53.
3. To raise Fund I's active risk from 5.1% to 5.4%: manage more aggressively, short the benchmark, or simply hold less benchmark (or less of another active fund) than otherwise.
4. Optimal active risk for Fund II: $(0.20/0.53) \times 14.4 = 5.4\%$ (Python: 5.434); benchmark weight $1 - 5.4/6.2 = 13\%$ (Python: 0.129).
Check: active return $0.20(5.4) = 1.1\%$, total excess $7.6 + 1.1 = 8.7\%$, total risk $\sqrt{14.4^2 + 5.4^2} = 15.4\%$ (Python: 15.379), Sharpe $8.7/15.4 = 0.57$ (Python: 0.565), matching part 2. ^ex-09-02-3

**Example 4: scaling active return forecasts and sizing active weights** (V9 p.111, p.112)
Four uncorrelated securities, volatilities 25/50/25/50%, scores +1/+1/-1/-1, IC = 0.20.
1. Grinold rule (formula 13): $\mu_1 = 0.20(25.0)(1.0) = 5.0\%$; similarly +10.0%, -5.0%, -10.0% (Python confirms 5.0).
2. Uncorrelated bets with year-to-year independence mean four separate decisions: $BR = 4$.
3. Active weights (formula 14) at $\sigma_A = 9\%$: $\Delta w_1^{*} = \frac{0.05}{0.25^2}\cdot\frac{0.09}{0.20\sqrt{4}} = 18\%$ (Python: 0.180); the four weights are +18%, +9%, -18%, -9% (Python: security 2 gives $0.10 \times 0.09/(0.50^2 \times 0.4) = 9\%$). ^ex-09-02-4

**Example 5: the basic fundamental law** (V9 p.113, p.114)
Same four securities; equally weighted benchmark ($w_{B,i} = 25\%$) with expected benchmark return 10.0%.
1. Portfolio weights are benchmark plus active: 43%, 34%, 7%, 16% (sums to 100%); total return forecasts are 10% plus active: 15%, 20%, 5%, 0%.
2. Forecasted portfolio return $0.43(15) + 0.34(20) + 0.07(5) + 0.16(0) = 13.6\%$ (Python: 13.6); expected active return $13.6 - 10.0 = 3.6\%$, or directly $0.18(5) + 0.09(10) - 0.18(-5) - 0.09(-10) = 3.6\%$ (Python: 3.6).
3. Active risk $[0.18^2(25^2) + 0.09^2(50^2) + 0.18^2(25^2) + 0.09^2(50^2)]^{1/2} = 9.0\%$ (Python: 9.0).
4. Law check: $IC\sqrt{BR}\sigma_A = 0.20 \times 2 \times 9.0 = 3.6\%$, and $IR^{*} = 0.20\sqrt{4} = 0.40 = 3.6/9.0$ (Python confirms both). ^ex-09-02-5

**Example 6: the expanded fundamental law** (V9 p.115, p.116)
Same forecasts; a constrained optimizer at $\sigma_A = 9\%$ delivers actual active weights +6%, +4%, +7%, -17% against optimal +18%, +9%, -18%, -9%.
1. TC is the correlation of $\Delta w_i \sigma_i$ with $\mu_i/\sigma_i$: risk-weighted weights (1.5, 2.0, 1.75, -8.5) vs risk-weighted forecasts (0.20, 0.20, -0.20, -0.20); correlation = 0.58 (Python: 0.5769, curriculum rounds to 0.58); for the optimal weights TC = 1.0 by construction (Python: 1.000).
2. Actual forecasted active return $0.06(5) + 0.04(10) + 0.07(-5) + (-0.17)(-10) = 2.1\%$ (Python: 2.05); actual active risk $[0.06^2(25^2) + 0.04^2(50^2) + 0.07^2(25^2) + 0.17^2(50^2)]^{1/2} = 9.0\%$ (Python: 9.031).
3. Law check: $TC \times IC \times \sqrt{BR}\,\sigma_A = 0.58 \times 0.20 \times 2 \times 9.0 = 2.1\%$ (Python: 2.088), matching the direct calculation.
Note the constraint cost: 3.6% expected alpha shrank to 2.1%, a 42% haircut at the same tracking risk. ^ex-09-02-6

**Text demonstration: constrained optimal aggressiveness** (V9 p.117)
TC 0.50, unconstrained IR 0.30, benchmark SR 0.40 and risk 16.0%.
Optimal active risk (formula 19): $0.50(0.30/0.40)(16.0) = 6.0\%$ (Python: 6.0).
Maximum Sharpe: $\sqrt{0.40^2 + 0.50^2 \times 0.30^2} = 0.43$ (Python: 0.4272).
If the fund runs 8.0% active risk, mix $1 - 6.0/8.0 = 25\%$ benchmark with 75% fund to reach the optimum (Python: 0.25).

**Example 7: ex post performance** (V9 p.118)
Strategy: BR = 100, IC = 0.05, TC = 0.80, $\sigma_A = 4.0\%$; expected value added $0.80 \times 0.05 \times 10 \times 4.0 = 1.6\%$ (Python: 1.6).
1. Realized $IC_R = -0.10$: conditional value added $0.80 \times (-0.10) \times 10 \times 4.0 = -3.2\%$ (Python: -3.2); with negative realized skill, expect negative active return.
2. Actual active return -2.6%: noise $= -2.6 - (-3.2) = +0.6\%$ (Python: 0.6); constraints happened to help this period, and -2.6% is well inside the 4.0% tracking-risk band.
3. Variance split: $TC^2 = 0.64$, so 64% of performance variation comes from realized forecasting success and 36% from constraint-induced noise (Python: 0.64). ^ex-09-02-7

**Text demonstration: global equity strategy, unconstrained and constrained** (V9 p.119 to p.125)
24 MSCI country assets vs ACWI, scores in {-2,...,+2} scaled by IC = 0.10 through the Grinold rule; e.g. UK forecast $0.10 \times 6.4 \times 2.0 = 1.3\%$ (Python: 1.28).
Long-short optimizer at $\sigma_A = 2.00\%$: TC 0.995, effective IC 0.099, BR 24.5 (above 24 because of non-zero active correlations); law gives $E(R_A) = 0.995 \times 0.099 \times \sqrt{24.5} \times 2.00 = 0.98\%$ and $IR = 0.49$ (Python: 0.9751 and 0.4876), matching the direct sum of weights times forecasts.
Swapping two pairs of scores (a more ambitious forecast against positively correlated markets) lifts effective IC to 0.105 and IR to $0.997 \times 0.105 \times \sqrt{24.5} = 0.53$ vs the actual 0.52 (Python: 0.5182).
Long-only plus 10% position caps: TC falls to 0.694 and $E(R_A) = 0.694 \times 0.099 \times \sqrt{24.5} \times 2.00 = 0.68\%$, IR 0.34 (Python: 0.6802 and 0.3401), roughly a one-third loss to constraints.
Raising active risk to about 2.74% tightens the caps further: TC 0.567 and IR $0.567 \times 0.099 \times \sqrt{24.5} = 0.28$ (Python: 0.2778); constrained IRs fall as aggressiveness rises.

**Text demonstration: fixed-income credit timing** (V9 p.126 to p.128)
Benchmark 70% IG / 30% HY; quarterly binary credit call; quarterly volatilities 2.84% and 4.64%, correlation 0.575.
Quarterly active risk of the switch: $[2.84^2 - 2(2.84)(4.64)(0.575) + 4.64^2]^{1/2} = 3.80\%$ (Python: 3.8001), annualized $3.80 \times \sqrt{4} = 7.60\%$.
55% accuracy gives $IC = 0.55 - 0.45 = 0.10$; Grinold rule per quarter: $0.10(3.80)(1.0) = 38$ bps, identical to the probability-weighted average $0.55(3.80) + 0.45(-3.80)$ (Python: 0.38 both ways).
Capping annual active risk at 2.00% sets the active weight at $2.00/7.60 = 26.3\%$ (Python: 0.2632), i.e. 43.7/56.3 splits when bullish on credit and 96.3/3.7 when bearish.
Law: $E(R_A) = 0.10\sqrt{4} \times 2.00 = 40$ bps a year (10 bps a quarter, also $0.263 \times 38$), and $IR = 0.10\sqrt{4} = 0.20$ (Python confirms).
Truly independent monthly calls would give $IR = 0.10\sqrt{12} = 0.35$; daily, $0.10\sqrt{250} = 1.58$ (Python: 0.3464 and 1.5811); repeating the same quarterly signal three times a month adds nothing.
With continuous signals and a long-only constraint at 4.0% active risk, signals of -0.57 and +1.32 imply active weights of -30.0% and +69.5% (Python: -0.30 and 0.6947), hitting the 0%/100% bounds; the normal-distribution transfer coefficient is $\Phi(1.32) - \Phi(-0.57) = 0.62$ (Python: 0.6222), so $IR = 0.62 \times 0.10\sqrt{250} = 0.98$, not 1.58, and $E(R_A) = 0.98 \times 4.00 = 3.92\%$, not 6.32% (Python: 0.9803 and 3.92).

**Text demonstration: Treasury maturity-bucket selection** (V9 p.128 to p.130)
Five Treasury maturity buckets, equally weighted benchmark; active correlations range +0.49 to -0.49, giving BR = 9.4 despite only 5 assets.
First (rates-will-rise) score set: effective IC 0.12 despite the 0.20 scaling IC, because one macro view drives all five scores; $E(R_A) = 0.12\sqrt{9.4} \times 1.00 = 37$ bps (Python: 0.3679).
Sample forecast: 10-20yr active return $0.20 \times 4.57 \times (-1.76) = -1.61\%$ (Python: -1.6086).
Second (curve-shape) score set is more ambitious: effective IC 0.18, $E(R_A) = 0.18\sqrt{9.4} \times 1.00 = 55$ bps and $IR = 0.55$ (Python: 0.5519).
Doubling active risk to 2.00% would push the 2.8% total weight in long bonds negative, so without shorting the TC would drop below 1.00 (V9 p.130).

**Example 8: compare and contrast active management strategies** (V9 p.125, p.126)
Stock selection: 100 uncorrelated securities, IC = 0.05; sector rotation: 9 sectors, IC = 0.15; annual independent forecasts.
1. Breadth: BR = 100 and BR = 9.
2. Unconstrained IRs: $0.05\sqrt{100} = 0.50$ vs $0.15\sqrt{9} = 0.45$; the lower-skill stock picker wins on breadth (Python: 0.50 and 0.45).
3. At $\sigma_A = 3.0\%$: expected active returns $0.50(3.0) = 1.50\%$ vs $0.45(3.0) = 1.35\%$.
4. Long-only and turnover limits with TC = 0.60: $IR = 0.60 \times 0.05 \times 10 = 0.30$ and $E(R_A) = 0.30(3.0) = 0.90\%$ (Python confirms).
5. Raising active risk to 4.0% makes constraints bind harder, so TC likely falls (say to 0.50), giving $IR = 0.25$ and $E(R_A) = 0.25(4.0) = 1.0\%$, not the proportional 1.2%: aggressiveness buys less than it should. ^ex-09-02-8

**Example 9: breadth and rebalancing in active management** (V9 p.130, p.131)
Four assets; active returns of #1 and #2 correlated 0.25, likewise #3 and #4; other correlations zero; BR = 3.2.
1. Breadth is below $N = 4$ because paired assets move together, so bets on them partly repeat one decision.
2. Forecasting #1 and #2 both to outperform (with #3, #4 underperforming) is a less ambitious forecast than splitting each pair, so fundamental-law accounting adjusts the IC downward by more in the first case.
3. Monthly rebalancing could scale breadth up to $12 \times 3.2 = 38.4$ (Python: 38.4), but only if monthly decisions are truly independent over time, the IC survives the higher frequency, and constraints (e.g. turnover limits) do not cut the TC. ^ex-09-02-9

**Example 10: limitations of the fundamental law** (V9 p.134)
A stock picker claims IC = 0.05 with BR = 12 x 500 = 6,000, so $IR = 0.05\sqrt{6000} = 3.87$ and, at 3.0% active risk, $E(R_A) = 11.6\%$ (Python: 3.873 and 11.62).
Reasons the number is fantasy: cross-sectional dependence (sector-driven forecasts make far fewer than 500 independent bets), time-series dependence (slow-moving signals like earnings yield repeat for months, so 12 monthly decisions are not 12 bets), and IC uncertainty (strategy risk shrinks realized IRs and the IC itself drifts).
A constraints/TC answer is the weakest, because the transfer coefficient is already a standard refinement of the law rather than a limitation of it. ^ex-09-02-10

## Item-set patterns

> [!warning] Trap 1: alpha versus active return
> The vignette calls the simple return difference "alpha" or asserts the two are equal.
> Correct: $R_A = R_P - R_B$ while $\alpha_P = R_P - \beta_P R_B$; they coincide only when $\beta_P = 1$ (V9 p.94).
> Distractor statements that define active weights correctly but sneak "equal to alpha" into the active return sentence make "both correct" tempting; check each clause separately (V9 p.138).

> [!warning] Trap 2: which decomposition term is which
> A table gives sub-portfolio returns, benchmark returns, actual weights, and policy weights, and asks for value added from selection or allocation.
> Correct: selection is actual portfolio weights times sub-portfolio value added, $\sum w_{P,j} R_{A,j}$; allocation is active class weights times benchmark class returns, $\sum \Delta w_j R_{B,j}$ (V9 p.96).
> The distractors are the other component and the total; the question's answer options are usually exactly (allocation, selection, total), so compute both pieces and match (V9 p.142).

> [!warning] Trap 3: cash versus aggressiveness on the two ratios
> Paired statements claim adding cash changes (or does not change) the IR, and scaling active weights changes (or does not change) it.
> Correct: the Sharpe ratio is unaffected by cash or leverage; the IR of an unconstrained portfolio is unaffected by proportional scaling of active weights but is generally shrunk by adding cash (V9 p.99, p.102).
> Every permutation of these properties appears as a distractor; anchor on which ratio's numerator and denominator scale together under the change described (V9 p.142, p.143).

> [!warning] Trap 4: highest Sharpe ratio does not mean best complement to the benchmark
> Candidate funds are listed with Sharpe ratios, IRs, total risks, and active risks, and the question asks which to combine with the benchmark.
> Correct: rank by expected information ratio, because $SR_P^2 = SR_B^2 + IR^2$; total-risk Sharpe ranking is irrelevant to the combination decision (V9 p.103).
> A fund with the highest Sharpe ratio or lowest active risk is planted to catch candidates who forget the squared-IR result; likewise ranking by active risk is not ranking by total risk (V9 p.101, p.144).

> [!warning] Trap 5: optimal active risk and the benchmark weight sign
> Given IR, SR_B, sigma_B, and the fund's delivered active risk, size the optimal combination.
> Correct: $\sigma_A^{*} = (IR/SR_B)\sigma_B$; fund weight $= \sigma_A^{*}/\sigma_A^{fund}$ and benchmark weight is the remainder, which is negative (a short) when the fund is not aggressive enough (V9 p.103, p.151).
> Distractors swap the ratio (using $SR_B/IR$), use the fund's own risk in place of the benchmark's, or offer the round-number leverage (1.5x) from a different example; verify with $SR_P = \sqrt{SR_B^2 + IR^2}$ (V9 p.151).

> [!warning] Trap 6: IC versus TC identification
> Verbal definitions are attributed to analysts: "realized returns versus anticipated returns" and "realized returns versus active weights."
> Correct: IC correlates forecasts with realized active returns; TC correlates forecasts (equivalently optimal weights) with the actual active weights taken; neither is defined against realized returns and weights (V9 p.109, p.114).
> The trap statement pairs "realized" with either correlation; both analysts can be wrong, and C ("neither") is a real answer, as in Practice Problem 23 (V9 p.145).

> [!warning] Trap 7: breadth inflation
> A strategy multiplies securities by rebalancing periods to claim huge breadth and a spectacular IR.
> Correct: breadth counts independent decisions; industry clustering and persistent signals (low P/E tilts, slow-moving views) make both the cross-sectional and time-series counts smaller, and $BR = N/[1 + (N-1)\rho]$ quantifies the cross-sectional shrinkage (V9 p.133, p.134).
> Distractors accept the naive product or claim rebalancing frequency alone adds breadth; frequency helps only with truly independent successive forecasts and an intact IC and TC (V9 p.131).

> [!warning] Trap 8: what changes when constraints are added or relaxed
> A manager adds position caps, or clients drop short-selling bans and turnover limits.
> Correct: constraints work through TC; adding them lowers TC, expected active return, the optimal aggressiveness $TC(IR^{*}/SR_B)\sigma_B$, and makes the IR decline with active risk; relaxing them raises expected active return (V9 p.116, p.125).
> Distractors claim constraints make the IR invariant to active risk (backwards: that is the unconstrained property) or increase the transfer of forecasts into weights; watch compound questions where one change raises and another lowers alpha, and net them (V9 p.147).

> [!warning] Trap 9: market timing accuracy to IC
> A timer is right 55% of the time and the vignette asks for the IC or the IR.
> Correct: $IC = 2(0.55) - 1 = 0.10$, then $IR = IC\sqrt{BR}$ with BR equal to the number of independent calls per year, not the number of assets (V9 p.127).
> Distractors use 0.55 itself as the IC, use 0.10 without the breadth root, or count four quarterly repeats of one view as four decisions (V9 p.127).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM02-Analysis-of-Active-Portfolio-Management-Practice-Problems]]

## Cross-links

- [[LM01-Economics-and-Investment-Markets]]: supplies the equilibrium view of expected returns and risk premiums that active management deliberately bets against; this module's mu_i forecasts are subjective deviations from exactly the discount-rate machinery LM1 builds.
- [[LM04-Using-Multifactor-Models]]: provides the multi-factor risk models that define active security returns as residuals ($R_{Ai} = R_i - \sum \beta_{j,i} R_j$), decompose active risk, and make IC and TC measurable in practice; the fundamental law assumes such a risk model exists and works.
- [[LM06-Backtesting-and-Simulation]]: the toolkit for estimating the ex post inputs this module consumes (realized IC, active risk, IR) and for stress-testing them; the strategy-risk limitation (IC uncertainty) is precisely what backtests with rolling windows expose.
- [[LM01-Basics-of-Multiple-Regression-and-Underlying-Assumptions]]: the correlation and covariance mechanics behind IC and TC (cross-sectional correlations of risk-weighted variables) and the independence assumptions behind breadth are quantitative-methods material; a regression of realized on forecasted active returns is an IC estimate.
- The curriculum ships a separate technical appendix PDF for this module (technical-append-to-analysis-of-active-portfolio-mgmt.pdf) with formal derivations of the fundamental law; this note works entirely from the module text, so consult the appendix only for proof-level detail.

## Self-test

Vignette A for Q1 to Q4: Meera Iyer allocates to the Kestrel Fund, an active equity fund benchmarked to an index with total risk 15.0% and Sharpe ratio 0.45.
Kestrel's expected information ratio is 0.36 and it currently runs 7.2% active risk.
Iyer can hold Kestrel, the benchmark index fund, and cash in any proportions, including short positions in the index.

> [!question] Q1
> The optimal amount of active risk for Iyer's combined portfolio is closest to:
> A. 7.2%.
> B. 12.0%.
> C. 18.8%.

> [!question] Q2
> At the optimal active risk, the combined portfolio's Sharpe ratio is closest to:
> A. 0.45.
> B. 0.58.
> C. 0.81.

> [!question] Q3
> The weights on Kestrel and the benchmark that achieve the optimal active risk are closest to:
> A. 0.60 on Kestrel and 0.40 on the benchmark.
> B. 1.00 on Kestrel and 0.00 on the benchmark.
> C. 1.67 on Kestrel and -0.67 on the benchmark.

> [!question] Q4
> If new client guidelines impose position caps that cut Kestrel's transfer coefficient from 1.00 to 0.60 while the unconstrained IR stays 0.36, the new optimal active risk is closest to:
> A. 4.3%.
> B. 7.2%.
> C. 12.0%.

Vignette B for Q5 to Q7: Tomas Silva compares three strategies for the same equity benchmark.
Strategy 1 selects among 120 stocks whose active returns are uncorrelated, with annual independent forecasts, IC 0.06, and a long-only implementation with TC 0.65.
Strategy 2 is a quarterly market timer who is correct 57% of the time, with each quarterly call truly independent and no implementation constraints.
Strategy 3 rotates across 20 industry groups whose active returns share a common pairwise correlation of 0.25, with annual forecasts, IC 0.10, and TC 1.00.

> [!question] Q5
> Strategy 1's expected information ratio is closest to:
> A. 0.43.
> B. 0.55.
> C. 0.66.

> [!question] Q6
> Strategy 2's information coefficient and information ratio are closest to:
> A. IC 0.14, IR 0.28.
> B. IC 0.57, IR 1.14.
> C. IC 0.14, IR 0.48.

> [!question] Q7
> Strategy 3's breadth, after the correlation adjustment, is closest to:
> A. 3.5.
> B. 5.75.
> C. 20.0.

Vignette C for Q8 to Q10: The Halcyon Fund runs TC = 0.70, assumed IC = 0.05, BR = 64, and active risk 3.0%.
In 2025 its realized information coefficient was -0.08 and its realized active return was -0.9%.
An analyst reviewing the year states: "Because the realized active return of -0.9% was better than skill alone implied, the constraints hurt the fund this year."

> [!question] Q8
> The value added expected conditional on the realized information coefficient was closest to:
> A. -1.92%.
> B. -1.34%.
> C. -0.90%.

> [!question] Q9
> The constraint-induced noise component of 2025 active return was closest to:
> A. -0.44%.
> B. +0.44%.
> C. +1.34%.

> [!question] Q10
> The share of Halcyon's performance variance over time attributable to constraint-induced noise is closest to:
> A. 30%.
> B. 49%.
> C. 51%.

> [!success]- Answer key
> Q1: B.
> $\sigma_A^{*} = (IR/SR_B)\sigma_B = (0.36/0.45)(15.0) = 12.0\%$ (Python: 12.0).
> A is the fund's delivered active risk (nothing says delivered = optimal); C misuses $\sqrt{15^2 + 12^2} = 19.2$, the total risk, as active risk.
> Q2: B.
> $SR_P = \sqrt{0.45^2 + 0.36^2} = 0.576$, closest to 0.58 (Python: 0.5763).
> A ignores the active contribution; C adds levels ($0.45 + 0.36 = 0.81$) instead of squares.
> Verification: expected excess $= 0.45(15) + 0.36(12) = 6.75 + 4.32 = 11.07$; total risk $\sqrt{15^2 + 12^2} = 19.21$; $11.07/19.21 = 0.576$ (Python confirms).
> Q3: C.
> Kestrel weight $= 12.0/7.2 = 1.67$, benchmark weight $= 1 - 1.67 = -0.67$: lever the fund by shorting the benchmark (Python: 1.6667 and -0.6667).
> A rescales in the wrong direction (that mix would cut active risk to 4.3%); B leaves active risk at the suboptimal 7.2%.
> Q4: B.
> $\sigma_A = TC(IR^{*}/SR_B)\sigma_B = 0.60(0.36/0.45)(15.0) = 7.2\%$; constraints scale the optimal aggressiveness by TC.
> A applies TC twice ($0.6^2 \times 12$); C forgets TC entirely.
> Q5: A.
> $IR = TC \times IC \times \sqrt{BR} = 0.65 \times 0.06 \times \sqrt{120} = 0.43$ (Python: 0.4272).
> C ($0.06\sqrt{120} = 0.66$) forgets the TC; B is a half-way blend with no meaning.
> Q6: A.
> $IC = 2(0.57) - 1 = 0.14$ and $IR = 0.14\sqrt{4} = 0.28$ (Python: 0.14 and 0.28).
> B uses accuracy itself as IC; C uses monthly breadth ($0.14\sqrt{12} = 0.48$) that the quarterly facts do not support.
> Q7: A.
> $BR = N/[1 + (N-1)\rho] = 20/[1 + 19(0.25)] = 20/5.75 = 3.5$ (Python: 3.478).
> B stops at the denominator; C ignores the correlation adjustment; note Strategy 3's IR is then only $0.10\sqrt{3.478} = 0.19$ despite the higher IC, so on these numbers the wide, low-skill Strategy 1 still wins.
> Q8: B.
> $E(R_A \mid IC_R) = TC \times IC_R \times \sqrt{BR}\,\sigma_A = 0.70(-0.08)(8)(3.0) = -1.34\%$ (Python: -1.344).
> A drops the TC ($-0.08 \times 8 \times 3 = -1.92$); C is the actual return, not the conditional expectation.
> Q9: B.
> Noise $= R_A - E(R_A \mid IC_R) = -0.9 - (-1.34) = +0.44\%$ (Python: 0.444): constraints helped, so the analyst's quoted conclusion is backwards.
> A flips the sign; C subtracts in the wrong order and drops the actual return.
> Q10: C.
> Noise share $= 1 - TC^2 = 1 - 0.49 = 51\%$ (Python: 0.51).
> B is the skill share $TC^2$; A is a rounding decoy; with TC = 0.70, slightly more than half of period performance variation is constraint noise, which is why single-year results say little about skill.

## Flashcards

#flashcards/cfa-l2/09-Portfolio-Management/lm02

Value added (active return) definition::The managed portfolio return minus the benchmark portfolio return, RA = RP - RB (V9 p.93).
Active weight definition::The portfolio weight of an asset minus its benchmark weight; active weights always sum to zero (V9 p.94).
Value added as a sum product::RA equals the sum over assets of active weight times active security return, where RAi = Ri - RB (V9 p.94).
When is value added positive?::When overweighted assets beat the benchmark and underweighted assets trail it, i.e. active weights correlate positively with realized active returns (V9 p.94, p.109).
Alpha vs active return::Alpha is beta-adjusted, RP minus beta times RB; active return assumes beta equals 1 (V9 p.94).
Three qualities of a good benchmark::Representative of the selection universe, replicable at low cost, verifiable ex ante with timely returns ex post (V9 p.93).
Why is active management a zero-sum game against a total market index?::The float-adjusted cap-weighted market portfolio is the average of all investors, so before costs active gains must net to zero (V9 p.93).
Decomposition of value added (two terms)::Asset allocation, the sum of active class weights times benchmark class returns, plus security selection, the sum of portfolio class weights times within-class value added (V9 p.96).
Where does the interaction effect go in the curriculum's attribution?::It is arbitrarily assigned to the security selection term (V9 p.96).
Sharpe ratio formula::Portfolio return minus the risk-free rate, divided by total portfolio volatility (V9 p.97).
Annualization convention for monthly data::Multiply mean monthly return by 12 and monthly volatility by the square root of 12 (V9 p.98).
Effect of cash or leverage on the Sharpe ratio::None; excess return and volatility scale by the same weight, so the ratio is unchanged (V9 p.99).
Two-fund separation::Every investor should combine the highest-Sharpe risky portfolio with cash or leverage to set total risk (V9 p.99).
Information ratio formula::Active return divided by active risk, the annualized standard deviation of portfolio-minus-benchmark returns (V9 p.101).
What does the IR measure intuitively?::The consistency of active return, reward per unit of benchmark tracking risk (V9 p.100).
Closet index fund signature::Sharpe ratio close to the benchmark's, very low active risk, IR near zero or negative after fees (V9 p.101).
Active share::Half the sum of absolute active weights; measures how different a portfolio is from its benchmark (V9 p.101).
Market-neutral fund vs riskless benchmark::Its Sharpe ratio and information ratio are identical because excess return equals active return and total risk equals active risk (V9 p.101).
Effect of scaling all active weights by c on an unconstrained portfolio::Active return and active risk both scale by c, so the IR is unchanged (V9 p.102).
Effect of adding cash on the IR::It generally shrinks the information ratio (V9 p.102).
How does an outside investor change a fund's active risk without touching holdings?::Blend with the benchmark to cut it, or short the benchmark (or hold less of it) to raise it; the IR is preserved (V9 p.102).
Combined squared Sharpe ratio relation::{{SR_P^2 = SR_B^2 + IR^2}} at the optimal level of active risk (V9 p.103).
Why is expected IR the best manager-selection criterion?::The highest-IR fund produces the highest combined Sharpe ratio for any investor sharing that benchmark (V9 p.103).
Optimal amount of active risk (unconstrained)::{{sigma_A = (IR / SR_B) x sigma_B}} (V9 p.103).
Total risk of an active portfolio::sigma_P squared equals benchmark variance plus active return variance (V9 p.104).
30-second micro: IR 0.25, SR_B 0.50, sigma_B 20%; optimal active risk?
?
(0.25/0.50) x 20 = 10%.
Keystrokes: `.25 / .5 x 20 =` 10.
Combined Sharpe: `.5 x^2 + .25 x^2 = sqrt` 0.559 (V9 p.103).

What happens to optimal active risk as IR approaches zero?::It goes to zero; the optimal portfolio becomes the passive benchmark (V9 p.106).
Grinold rule::{{mu_i = IC x sigma_i x S_i}}, alpha equals skill times volatility times score, with scores standardized to cross-sectional variance 1 (V9 p.110).
Mean-variance optimal active weight intuition::Proportional to forecast over variance, scaled up by the portfolio active risk budget (V9 p.110).
Information coefficient definition::The risk-weighted cross-sectional correlation between forecasted active returns and realized active returns; signal quality (V9 p.109, p.110).
Typical IC magnitude in practice::Small positive values, usually below 0.20 (V9 p.110).
Transfer coefficient definition::The risk-weighted cross-sectional correlation between forecasted active returns (or optimal weights) and the active weights actually taken; portfolio construction fidelity (V9 p.109, p.114).
Typical TC range in practice::About 0.20 to 0.90; near 1.00 only when essentially unconstrained (V9 p.114, p.131).
When can TC be negative?::When the portfolio badly needs rebalancing, so current weights anticorrelate with current forecasts (V9 p.115).
Breadth definition::The number of independent investment decisions made per year (V9 p.110).
Basic fundamental law::{{E(R_A) = IC x sqrt(BR) x sigma_A}} for the unconstrained optimal portfolio (V9 p.112).
Full fundamental law::{{E(R_A) = TC x IC x sqrt(BR) x sigma_A}}, and IR = TC x IC x sqrt(BR) (V9 p.115).
The four inputs of the fundamental law in words::Skill (IC), construction fidelity (TC), independent decisions per year (BR), and aggressiveness (active risk) (V9 p.115, p.136).
Which fundamental-law inputs may be outside the manager's control?::TC, BR, and sigma_A can be set by policy or regulation; skill is the manager's own (V9 p.136).
Optimal active risk with constraints::{{sigma_A = TC x (IR* / SR_B) x sigma_B}}; at TC = 0 hold the benchmark (V9 p.116, p.117).
Constrained combined Sharpe relation::SR_P squared equals SR_B squared plus TC squared times IR* squared (V9 p.116).
Conditional expected value added ex post::{{E(R_A given IC_R) = TC x IC_R x sqrt(BR) x sigma_A}}, realized IC replacing expected IC (V9 p.117).
Ex post variance decomposition::TC squared of performance variance comes from realized IC variation; 1 minus TC squared is constraint-induced noise (V9 p.117).
30-second micro: TC 0.9, IC 0.1, BR 36, sigma_A 4%; expected active return?
?
0.9 x 0.1 x 6 x 4 = 2.16%.
Keystrokes: `36 sqrt x .9 x .1 x 4 =` 2.16 (V9 p.115).

Market timer IC from accuracy::IC = 2 x (proportion correct) - 1; 55% right gives 0.10 (V9 p.127).
Why do market timing strategies need high accuracy?::Breadth is tiny (e.g. 4 quarterly calls), so IR = IC x sqrt(BR) stays modest unless IC is large (V9 p.127).
Does repeating the same signal monthly raise breadth?::No; breadth rises with frequency only when successive decisions are truly independent (V9 p.127, p.133).
Breadth rule of thumb with correlation::{{BR = N / (1 + (N - 1) x rho)}} (V9 p.133).
30-second micro: N = 2, rho = -0.5; breadth?
?
BR = 2/(1 - 0.5) = 4, double the asset count; negative correlation inflates breadth (V9 p.133).

Why can arbitrage-like strategies have huge breadth?::Strongly negatively correlated active returns make each pair of positions worth many independent bets, e.g. N = 2 at rho = -0.8 gives BR = 10 (V9 p.133).
Why is fixed income hard for the fundamental law?::Bonds share duration, credit, and optionality exposures, so active returns are correlated in subtle ways, and default/option payoffs break the normality assumption (V9 p.133).
Qian-Hua strategy risk::Uncertainty in the IC adds active risk, sigma_A = sigma_IC x sqrt(N) x sigma_RM, so realized IRs run about 45% to 91% of naive law estimates (V9 p.132).
Two limitation categories the module emphasizes::Ex ante uncertainty about the IC (skill), and non-independence of decisions across assets and over time (breadth) (V9 p.132, p.133).
Which limitation answer is weakest for an overstated-IR question?::Constraints/transfer coefficient, because TC is a standard refinement of the law, not an ignored limitation (V9 p.134).
Which decisions did the 120/20 global equity example show constraints damaging?::Long-only plus 10% caps cut TC from 0.995 to 0.694 (IR 0.49 to 0.34), and raising active risk to 3% cut TC further to 0.567 (IR 0.28) (V9 p.124, p.125).
Trap: fund with highest Sharpe ratio vs highest IR as benchmark complement::Choose the highest IR; the combined Sharpe ratio is sqrt(SR_B^2 + IR^2), so stand-alone Sharpe ranking misleads (V9 p.103, p.144).
Trap: does low active risk alone prove closet indexing?::Low active risk and near-benchmark Sharpe suggest it; a small IR does not, since the IR is indeterminate at tiny active risk and often negative after fees (V9 p.151).
Why is Equation SR_P^2 = SR_B^2 + IR^2 useless for negative-IR funds?::Squaring loses the sign, so a bad fund can look as attractive as a good one (V9 p.103).
30-second micro: fund active risk 5%, want 4%; benchmark weight?
?
Hold 80% fund, 20% benchmark: 0.8 x 5 = 4% active risk, IR unchanged (V9 p.102).

## Common mistakes

1. Equating active return with alpha; alpha is beta-adjusted ($\alpha_P = R_P - \beta_P R_B$) and the two match only at beta 1 (V9 p.94, p.148).
2. Crossing the invariance properties: cash/leverage leaves the Sharpe ratio unchanged, proportional aggressiveness leaves the unconstrained IR unchanged; assigning either property to the other ratio is the module's most-tested error (V9 p.99, p.102, p.143).
3. Using portfolio weights with portfolio returns (or benchmark weights with benchmark returns) in the attribution terms; allocation is active weights times benchmark returns, selection is portfolio weights times sub-portfolio value added (V9 p.96, p.150).
4. Ranking benchmark complements by Sharpe ratio or raw active return instead of the IR; $SR_P^2 = SR_B^2 + IR^2$ makes the IR the only ranking that matters (V9 p.103, p.152).
5. Adding SR and IR in levels instead of squares when computing the combined Sharpe ratio, or forgetting to take the final square root (V9 p.103, p.149).
6. Inverting the optimal-risk ratio, using $SR_B/IR$ instead of $IR/SR_B$, or multiplying by the fund's active risk instead of the benchmark's total risk in $\sigma_A^{*} = (IR/SR_B)\sigma_B$ (V9 p.103, p.151).
7. Solving $IR = IC\sqrt{BR}$ for breadth and forgetting to square the quotient, e.g. reporting 4 instead of 17 securities (V9 p.145, p.152).
8. Misdefining IC or TC against "realized" quantities: IC pairs forecasts with realized returns, TC pairs forecasts with weights taken; TC never touches realized returns (V9 p.114, p.152).
9. Forgetting the risk weighting in IC and TC calculations, or applying it the same way to both arguments; forecasts are divided by sigma_i while weights are multiplied by it (V9 p.110, p.114).
10. Counting breadth as securities times rebalancing periods despite correlated industry bets and persistent signals; apply $BR = N/[1+(N-1)\rho]$ cross-sectionally and demand time-series independence before multiplying by frequency (V9 p.133, p.134, p.147).
11. Treating a market timer's accuracy as the IC instead of $2 \times \text{accuracy} - 1$ (V9 p.127).
12. Assuming a constrained portfolio keeps its IR when aggressiveness rises; binding constraints cut TC as active risk grows, so the constrained IR falls (V9 p.125, p.126).
13. Concluding skill from a good year at low TC; with TC = 0.6 only 36% of performance variance reflects forecasting success, the rest is constraint noise (V9 p.117).
14. Forgetting that the ex ante IC must be positive to justify active management at all, while realized IC can be negative (V9 p.110).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "09-02" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
