---
type: cfa-lm
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
volume: 9
lm: 5
title: "Measuring and Managing Market Risk"
pages: "251-319"
weight_band: "10-15%"
difficulty: 2
los_count: 12
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/portfolio-management]
---

# LM5: Measuring and Managing Market Risk

Difficulty 2 of 5: the arithmetic is limited to one parametric VaR calculation and a handful of sensitivity plugs, but the item sets punish loose language, VaR is a minimum loss, not a maximum or an expected one, and the exam swaps conventions (5% vs 16%), scaling rules, and constraint labels relentlessly.

## LOS map

- **explain** the use of value at risk (VaR) in measuring portfolio risk (V9 p.251) ^los-09-05-a
    - Examiner asks: given a VaR statement such as "5% one-day VaR of $2.2 million", pick the only correct interpretation (minimum loss expected 5% of the time) and reject "maximum loss", "expected loss", and "95% of the time we lose less than" phrasings.
- **compare** the parametric (variance-covariance), historical simulation, and Monte Carlo simulation methods for estimating VaR (V9 p.251) ^los-09-05-b
    - Examiner asks: match a described estimation process (normality assumption, repricing on actual past returns, user-specified distribution with random draws) to its method, or pick the method best suited to a portfolio with options, limited data history, or expected non-normal volatility.
- **estimate** and interpret VaR under the parametric, historical simulation, and Monte Carlo simulation methods (V9 p.251) ^los-09-05-c
    - Examiner asks: compute a parametric VaR from annual inputs, which forces the divide-by-250 and divide-by-root-250 scaling before applying $E(R_p) - z\sigma_p$, or identify the historical VaR as the fifth percentile of sorted portfolio returns.
- **describe** advantages and limitations of VaR (V9 p.251) ^los-09-05-d
    - Examiner asks: which listed statement is not an advantage (there is no consensus calculation method) or not a limitation (a well-built VaR does adjust for duration), with liquidity, correlation risk, trending, and left-tail understatement as the recurring limitation set.
- **describe** extensions of VaR (V9 p.251) ^los-09-05-e
    - Examiner asks: match a definition to CVaR (average loss beyond the cutoff), incremental VaR (before-and-after VaR for a position change), marginal VaR (effect of a very small change, sums to total VaR), or ex ante tracking error (VaR run on portfolio minus benchmark).
- **describe** sensitivity risk measures and scenario risk measures and compare these measures to VaR (V9 p.251) ^los-09-05-f
    - Examiner asks: which measure carries probability information (VaR) versus pure responsiveness (duration, beta, delta), and which measures are based on a particular historical period (historical scenarios and VaR, not hypothetical scenarios or sensitivities).
- **demonstrate** how equity, fixed-income, and options exposure measures may be used in measuring and managing market risk and volatility risk (V9 p.251) ^los-09-05-g
    - Examiner asks: compute a bond return from duration and convexity for a given yield shock, rank bonds across rate scenarios, estimate a new option price with delta, gamma, and vega, or choose the option overlay that moves a portfolio delta to a target.
- **describe** the use of sensitivity risk measures and scenario risk measures (V9 p.251) ^los-09-05-h
    - Examiner asks: distinguish historical from hypothetical scenarios, identify reverse stress testing (stressing the portfolio's top exposures), and insist on full revaluation rather than delta-gamma or duration-convexity shortcuts for options in scenarios.
- **describe** advantages and limitations of sensitivity risk measures and scenario risk measures (V9 p.251) ^los-09-05-i
    - Examiner asks: which statement is not a limitation of scenario measures (they do not assume normality) or of sensitivities (they say nothing about the likelihood of the move), and why plausibility pressure makes hypothetical scenarios too small.
- **explain** constraints used in managing market risks, including risk budgeting, position limits, scenario limits, and stop-loss limits (V9 p.251) ^los-09-05-j
    - Examiner asks: classify a described rule as a risk budget (VaR or tracking error allocation), position limit (market value cap), scenario limit (loss tolerance per scenario), or stop-loss limit (liquidate after a realized loss), and recall that marginal VaR budgets sum exactly to total VaR.
- **explain** how risk measures may be used in capital allocation decisions (V9 p.251) ^los-09-05-k
    - Examiner asks: compare two activities' expected returns per unit of economic capital against a hurdle rate, or identify economic capital as the equity needed to survive severe tail losses at very high confidence.
- **describe** risk measures used by banks, asset managers, pension funds, and insurers (V9 p.251) ^los-09-05-l
    - Examiner asks: match surplus at risk to pension funds, ex ante tracking error and percentage-of-assets reporting to long-only managers, maximum drawdown and gross exposure to hedge funds, and economic capital plus liquidity gap to banks and insurers.

## Core intuition

Market risk is the risk arising from movements in stock prices, interest rates, exchange rates, and commodity prices, as distinct from credit risk (counterparty failure to pay) and operational risk (V9 p.252).
Everything in this module is a way of answering one question with models: how much could this portfolio lose, how often, and from which exposures (V9 p.252).
The module's architecture is three layers, a probability-based summary number (VaR and its extensions), responsiveness numbers with no probabilities attached (sensitivities), and what-if numbers for extreme worlds (scenarios and stress tests), followed by the constraints and capital decisions built on top of them (V9 p.252).

> [!abstract] Idea 1: VaR is a point on the profit-and-loss distribution, read as a minimum loss at a stated frequency over a stated horizon
> Value at risk is the minimum loss that would be expected a certain percentage of the time over a certain period of time, given assumed market conditions (V9 p.253).
> Every VaR statement has three explicit elements, the size of the loss (in currency or percent of portfolio), the probability (5%, 1%, or 16%), and the time horizon (a day, a month, a year) (V9 p.253).
> "The 5% VaR is EUR2.2 million over one day" means a loss of at least EUR2.2 million should occur on about 5% of trading days, roughly once a month, and it says nothing about how much worse the loss could be (V9 p.253).
> VaR is emphatically not "how much one can lose"; the answer to that question is the entire portfolio (V9 p.253).

The percentage conventions are pure normal-distribution geometry (V9 p.254).
A 5% VaR sits 1.65 standard deviations below the mean, a 1% VaR sits 2.33 standard deviations below, and a one standard deviation move corresponds to a 16% VaR (V9 p.254).
The 16% figure comes from adding the 50% of outcomes above the mean to the 34% lying within one standard deviation below it, leaving 16% of outcomes further out (V9 p.254, p.255).
There is no rule fixing the cutoff or the horizon; a higher confidence level produces a higher VaR, and choosing threshold, horizon, and method is judgment, which is the first hint that VaR is less objective than it looks (V9 p.254, p.255).

Estimation always follows the same first two steps regardless of method (V9 p.256).
First, risk decomposition converts holdings into exposures to risk factors, trivially for a stock that is its own factor, laboriously for a foreign convertible bond that carries currency, equity, and curve exposures at once (V9 p.256).
Second, a data history is gathered for each factor over a lookback period, with the crucial caveat that the parametric and Monte Carlo methods only need parameter estimates, which the user can and should override with judgment when the lookback is unrepresentative, exactly as the text overrides its own sample by resetting SPY to a 10.5% return and 20% volatility and SPLB to 6% and 8.5% (V9 p.256, p.257).
The third step is where the methods split (V9 p.256).

> [!abstract] Idea 2: three routes to the same percentile, differing in what they assume and what they can handle
> The parametric (variance-covariance) method assumes a distribution, normally the normal, computes the portfolio mean and standard deviation from weights, volatilities, and correlations, and reads the VaR directly off the z-scale; it is simple, but it is hostage to its parameter estimates (especially covariances) and handles options badly because truncated option payoffs are not normal (V9 p.258, p.261).
> The historical simulation method reprices the current portfolio on every day of the lookback, sorts the outcomes, and takes the relevant percentile; nothing in it is impossible, since it all actually happened, and it accommodates options, but it is only as good as the assumption that the future resembles that particular past (V9 p.262, p.264).
> The Monte Carlo method generates thousands of random factor returns from any distribution the user specifies (respecting the correlations), reprices, sorts, and reads the percentile; it is unconstrained by normality or by history, and with a normal specification and enough draws it converges to the parametric answer (V9 p.265, p.266, p.267).
> On the same $150 million, 80/20 SPY/SPLB portfolio the three methods return 5% VaRs of $2,445,150 (parametric), $1,622,272 (historical), and $2,517,702 (Monte Carlo), and the spread is the lesson, the historical number is smaller mainly because the lookback's equity volatility was abnormally low relative to the long-run inputs the other two methods were given (V9 p.260, p.263, p.267).

The scaling discipline matters more than the formula (V9 p.259).
Annual inputs become daily by dividing the expected return by 250 and the standard deviation by the square root of 250, because variance scales with time while standard deviation scales with its square root (V9 p.259).
The reverse trip annualizes the return by multiplying by 250 and the volatility by root 250; what is forbidden is annualizing the daily VaR itself, since that treats the mean and the volatility as if they scaled the same way (V9 p.259).

VaR's advantages are practical, it is a simple, easily communicated single number, it makes risk comparable across asset classes and trading units, it feeds capital allocation and risk-adjusted performance evaluation, it can be backtested against realized breach frequency, and regulators accept it (V9 p.269).
Its limitations are the exam's favorite list, subjectivity in every choice, understatement of left-tail frequency under normality, blindness to liquidity, vulnerability to correlations rising in stress, vulnerability to trending (losing just under the limit every day) and to low-volatility regimes, misreading as a worst case, oversimplification, and disregard of the right tail (V9 p.270, p.271).
The extensions answer questions VaR cannot, CVaR gives the expected loss once the cutoff is breached, incremental VaR gives the change in VaR from a contemplated position change, marginal VaR gives the effect of a very small change and decomposes total VaR into position contributions, and ex ante tracking error (relative VaR) runs the whole machinery on the portfolio minus its benchmark to estimate potential underperformance (V9 p.271, p.272).

> [!abstract] Idea 3: sensitivities say how much you move, scenarios say what a hostile world does, VaR says how often; only together do they work
> Duration, convexity, beta, delta, gamma, and vega measure the response of a position to a single small change in one risk factor and carry no probability content at all; duration says what a 1 bp move does but nothing about whether 1 bp moves are likely (V9 p.284).
> Scenario measures shock many factors at once, by large amounts, either replaying a historical window (uncontroversial, since it happened, but it will not repeat exactly) or positing a hypothetical event (free of history, able to stress correlations, but hard to calibrate and biased small by the need to appear plausible) (V9 p.279, p.281, p.286).
> VaR is probabilistic but history-bound; scenarios are history-free but probability-free; sensitivities are precise but silent on likelihood, so risk managers use all three, and constraints built on multiple measures are the mark of good practice (V9 p.284, p.287).

Two operational warnings recur.
Scenarios applied to options or option-embedded securities must fully reprice the instruments, because delta-gamma (and duration-convexity) approximations are built for small moves and fail at scenario-sized shocks (V9 p.280, p.283).
And sensitivities aggregated into buckets assume perfect correlation inside the bucket, so granularity is a real design choice, broad buckets hide curve risk, narrow buckets overwhelm the reader (V9 p.285).

Constraints turn measures into management (V9 p.288).
It is the limit placed on a measure, not the confidence level of the measure, that makes a framework restrictive; a loose limit on a 99% VaR can bind less than a tight limit on an 84% VaR (V9 p.288).
Risk budgeting allocates the total risk appetite (VaR, economic capital, or tracking error) down the hierarchy, and if standalone desk VaRs are summed the firm under-uses its appetite because diversification is thrown away, which is cured either by over-allocation with a pro rata clawback or by budgeting in marginal VaR, whose parts sum exactly to the total (V9 p.289).
Position limits cap market value or notional per issuer, country, currency, category, or liquidity tier, and they are the best defense against the concentration and single-name event risk VaR handles poorly (V9 p.290).
Scenario limits set a loss tolerance per scenario, higher for the more extreme scenarios, and trigger corrective action when crossed (V9 p.290, p.291).
Stop-loss limits force size reduction or liquidation after a realized loss over a specified period, which is the direct answer to the trending limitation of VaR; the dynamic version, hedging more as losses grow, is drawdown control or portfolio insurance (V9 p.291).

Capital allocation applies the same logic to shareholders' equity (V9 p.291).
Economic capital is the capital the firm needs to survive severe losses at very high confidence (99% to 99.99%, usually one year), actual capital must exceed it, and the appetite is subdivided across activities like a risk budget (V9 p.291, p.295).
Because capital is scarce and expensive, each activity's expected return per unit of allocated capital is compared with a hurdle rate; a portfolio earning EUR50,000 on EUR325,000 of capital (15.4%) beats a 15% hurdle while one earning EUR100,000 on EUR1,000,000 (10%) fails it despite the larger absolute income (V9 p.292).

Finally, who uses what follows from three drivers, leverage, risk-factor mix, and accounting or regulatory regime (V9 p.293).
Leveraged players (banks, hedge funds) care about high-confidence, short-horizon tail measures because insolvency is possible; unleveraged long-only managers care about underperformance, so they use lower confidence levels, longer horizons, percentage-of-assets units, and benchmark-relative measures (V9 p.293, p.296).
Banks run liquidity gap, VaR on the trading book, leverage ratios, duration and Greeks by desk, economic capital on the full balance sheet, and stress tests (V9 p.294, p.295).
Asset managers live on position limits, sensitivities, liquidity and redemption metrics, and ex ante tracking error, with VaR mainly for absolute-return mandates; the ex post versus ex ante tracking error distinction (realized history versus current holdings pushed through past markets) is a tested fine point (V9 p.296, p.297).
Hedge funds add gross exposure, leverage, and maximum drawdown, because non-normal strategies make standard deviation misleading (V9 p.298).
Pension funds discount liability cash flows, hold them as short positions, and watch surplus at risk, the VaR of assets minus liabilities, the engine of liability-driven investing (V9 p.299, p.300).
Insurers split by line, property and casualty lines (weakly market-correlated) monitor exposures against target allocations plus economic capital and VaR for catastrophe losses, while life lines (long liabilities, discount-rate sensitive) emphasize asset-liability matching and scenarios stressing market and non-market factors together (V9 p.300, p.301).

## Formulas and derivations

**Standard normal (z) transformation** (V9 p.258)
$$
z = \frac{R - \mu}{\sigma}
$$
^f-09-05-1

- $R$: observed return; $\mu$: expected value; $\sigma$: standard deviation; $z$: distance from the mean in standard deviation units.
- Any normal distribution converts to the standard normal (mean 0, deviation 1), so one table of cutoffs serves every portfolio (V9 p.258).
- The exam cutoffs: 5% VaR at $z = 1.65$, 1% VaR at $z = 2.33$, 16% VaR at $z = 1.00$ below the mean (V9 p.258).

**Portfolio expected return (two assets)** (V9 p.258)
$$
E(R_p) = w_1 E(R_1) + w_2 E(R_2)
$$
^f-09-05-2

- $w_i$: portfolio weights summing to 1; $E(R_i)$: expected return per asset or risk factor, annual unless stated.
- Expectation is linear, so the portfolio mean is just the weighted average; no correlation enters the mean (V9 p.258).

**Portfolio volatility (two assets)** (V9 p.258)
$$
\sigma_p = \sqrt{w_1^2 \sigma_1^2 + w_2^2 \sigma_2^2 + 2 w_1 w_2 \rho_{12} \sigma_1 \sigma_2}
$$
^f-09-05-3

- $\sigma_i$: asset volatilities; $\rho_{12}$: correlation; $\rho_{12}\sigma_1\sigma_2$: the covariance (V9 p.258).
- Variance of a sum picks up twice the covariance of the pair; a negative correlation (the text uses $-0.06$) trims portfolio volatility below the weighted average of the parts (V9 p.258, p.259).
- Parametric VaR is "very sensitive to the parameter estimates, especially the covariances", which is why this term is the danger spot (V9 p.261).

> [!tip] Calculator
> For the 80/20 SPY/SPLB inputs: `0.8 x 0.2 = x^2` gives 0.0256 (store), `0.2 x 0.085 = x^2` gives 0.000289 (add), `2 x 0.8 x 0.2 x 0.06 +/- x 0.2 x 0.085 =` gives -0.0003264 (add), total 0.0255626, then `sqrt(x)` gives 0.159883.

**Annual-to-daily scaling** (V9 p.259)
$$
E(R_p)_{daily} = \frac{E(R_p)_{annual}}{250}, \qquad \sigma_{p,daily} = \frac{\sigma_{p,annual}}{\sqrt{250}}
$$
^f-09-05-4

- 250: assumed trading days per year; reverse the trip with $\times 250$ and $\times \sqrt{250}$ to annualize (V9 p.259).
- Variance scales linearly with time, so standard deviation scales with the square root of time; the mean scales linearly (V9 p.259).
- Never annualize a daily VaR directly; multiplying the daily VaR by 250 or by $\sqrt{250}$ mixes the two scaling laws and is a standing distractor (V9 p.259, p.261).

**Parametric VaR** (V9 p.260)
$$
\text{VaR} = \left\{ \left[ E(R_p) - z\,\sigma_p \right] \times (-1) \right\} \times V_p
$$
^f-09-05-5

- $z$: 1.65 for 5%, 2.33 for 1%, 1.00 for 16%; $V_p$: portfolio value in currency; $E(R_p)$ and $\sigma_p$ must match the VaR horizon (daily for a daily VaR).
- Four steps: multiply $\sigma_p$ by $z$, subtract from $E(R_p)$, flip the sign (VaR is quoted as a positive number), multiply by portfolio value; asset managers often stop before the last step and quote percent of assets (V9 p.260).
- Holds because the chosen percentile of a normal distribution lies exactly $z$ standard deviations below the mean (V9 p.258).

> [!tip] Calculator
> Daily 5% VaR on $150m: `1.65 x 0.010112 = +/- + 0.000384 = +/-` gives 0.016301, then `x 150000000 =` gives 2,445,150.

**Conditional VaR (expected shortfall)** (V9 p.271, p.272)
$$
\text{CVaR} = E\left[ \text{Loss} \mid \text{Loss} \geq \text{VaR} \right]
$$
^f-09-05-6

- The average of the losses beyond the VaR cutoff; also called expected tail loss or expected shortfall (V9 p.271, p.272).
- Best obtained under historical simulation or Monte Carlo by averaging the observations in the tail (5% of 1,006 historical returns is 50 observations; 5% of 10,000 simulations is 500); the parametric route needs calculus beyond scope (V9 p.272).
- VaR answers "minimum loss at the confidence level"; CVaR answers "expected loss once the cutoff is breached" (V9 p.271, p.272).

**Incremental VaR (IVaR)** (V9 p.272)
$$
\text{IVaR} = \text{VaR}_{after\ change} - \text{VaR}_{before\ change}
$$
^f-09-05-7

- Recompute the full portfolio VaR under the contemplated position change (add, delete, or resize) and difference it against the current VaR (V9 p.272).
- Captures diversification, so IVaR can be negative when the new position hedges; it evaluates a trade before it is done (V9 p.272).

**Marginal VaR (MVaR) and VaR decomposition** (V9 p.272)
$$
\text{MVaR}_i \approx \frac{\partial\, \text{VaR}}{\partial\, w_i}, \qquad \sum_i \text{MVaR}_i\ \text{(position-weighted)} = \text{VaR}_p
$$
^f-09-05-8

- Calculus-based effect of a very small change in position $i$; loosely (not strictly) read as the VaR change per $1 or per 1% of position (V9 p.272).
- In a diversified portfolio the position-weighted marginal VaRs sum to the total VaR, so MVaR decomposes VaR into asset contributions, and budgets set in MVaR sum exactly to the top-of-house budget (V9 p.272, p.289).

**Ex ante tracking error (relative VaR)** (V9 p.272, p.273)
$$
\text{Ex ante TE} = \text{VaR}\left( \text{portfolio holdings} - \text{benchmark holdings} \right)
$$
^f-09-05-9

- Run any standard VaR model on the portfolio with the benchmark entered as short positions scaled to the portfolio's value; typically quoted as a one standard deviation annualized figure (V9 p.272, p.273).
- A portfolio identical to its benchmark has ex ante tracking error near zero; the measure grows with active deviation (V9 p.273).
- Against a cash benchmark, relative VaR and VaR coincide because cash has zero volatility (V9 p.296).

**CAPM and beta** (V9 p.274)
$$
E(R_i) = R_F + \beta_i \left[ E(R_M) - R_F \right], \qquad \beta_i = \frac{\text{Cov}(R_i, R_M)}{\text{Var}(R_M)}
$$
^f-09-05-10

- $E(R_M) - R_F$: the equity risk premium; beta measures the sensitivity of the security's expected return to it (V9 p.274).
- The broad market beta averages to 1.0; beta above (below) 1 marks the asset as more (less) volatile than the market (V9 p.274).
- Beta is the primary equity exposure measure; multifactor extensions refine it (V9 p.274).

**Duration approximation of a bond return** (V9 p.275)
$$
\frac{\Delta B}{B} \approx -D \, \frac{\Delta y}{1 + y}
$$
^f-09-05-11

- $D$: duration (weighted-average time to maturity, treating the bond as partially maturing at each coupon); $y$: the bond's yield; $\Delta y$: a single change applied to all rates (V9 p.275).
- First-order only: derived for an infinitesimal yield change at an instant, so it degrades for large moves and long horizons (V9 p.275).
- The minus sign encodes the inverse price-yield relation; in a falling-rate scenario the highest-duration bond gains most (V9 p.275, p.319).

> [!tip] Calculator
> Bond with $D = 10.2$, $\Delta y = -20$ bp, ignoring the yield divisor as the curriculum's scenario ranking does: `10.2 x 0.002 = +/- +/-` gives +2.04%.

**Duration plus convexity approximation** (V9 p.275)
$$
\frac{\Delta B}{B} \approx -D \, \frac{\Delta y}{1 + y} + \frac{1}{2}\, C \, \frac{(\Delta y)^2}{(1+y)^2}
$$
^f-09-05-12

- $C$: convexity, the sensitivity of duration to rate changes; the second-order term is always positive for option-free bonds because $(\Delta y)^2 > 0$ (V9 p.275).
- Convexity matters for large yield changes and long holding periods, exactly where duration alone fails (V9 p.275).
- Even so, duration-convexity is inadequate for scenario-sized shocks on option-embedded bonds; full revaluation is required there (V9 p.280).

**Option delta and the delta price approximation** (V9 p.276)
$$
\Delta \approx \frac{\text{Change in value of option}}{\text{Change in value of underlying}}, \qquad c + \Delta c \approx c + \Delta_c \, \Delta S
$$
^f-09-05-13

- Call deltas run 0 to 1, put deltas 0 to $-1$; deep out-of-the-money options sit near 0, deep in-the-money calls (puts) near 1 ($-1$), and the same limits apply as expiration approaches (V9 p.276).
- Delta is the options analogue of duration, a first-order effect valid for small moves over short periods (V9 p.276).
- Forwards, futures, and swaps have linear payoffs and can use their underlying's exposure measures; options cannot (V9 p.275).

**Gamma and the delta-gamma price approximation** (V9 p.276, p.277)
$$
\Gamma \approx \frac{\text{Change in delta}}{\text{Change in value of underlying}}, \qquad c + \Delta c \approx c + \Delta_c \, \Delta S + \frac{1}{2}\, \Gamma_c \, (\Delta S)^2
$$
^f-09-05-14

- Gamma is the second-order effect, the change in the change, the options analogue of convexity (V9 p.276).
- Gamma is largest for at-the-money options near expiration, where a small move in the underlying decides whether the option finishes in or out of the money (V9 p.276, p.277).
- Micro-check: delta 0.6, gamma 0.02, underlying up 0.10, new delta $0.6 + 0.02 \times 0.10 = 0.602$ (V9 p.276).

**Vega and the delta-gamma-vega approximation** (V9 p.277)
$$
\text{Vega} \approx \frac{\text{Change in value of option}}{\text{Change in volatility of underlying}}, \qquad c + \Delta c \approx c + \Delta_c \, \Delta S + \frac{1}{2}\, \Gamma_c \, (\Delta S)^2 + \text{vega}\,(\Delta \sigma)
$$
^f-09-05-15

- Vega is a first-order effect in volatility; option values respond to volatility even when the underlying does not move (V9 p.277).
- The composite expression is the full sensitivity kit for an option position, and portfolio deltas, gammas, and vegas are the money-weighted sums across positions (an ETF has delta 1 and zero gamma and vega) (V9 p.277).

> [!tip] Calculator
> Call at 4.00, delta 0.55, gamma 0.04, vega 0.11, underlying +2.00, volatility +1 point: `0.55 x 2 = STO 1` (1.10), `0.04 x 4 = / 2 = STO 2` (0.08), `RCL 1 + RCL 2 + 0.11 + 4 =` gives 5.29.

**Funding ratio and surplus** (V9 p.299)
$$
\text{Funding ratio} = \frac{\text{Assets}}{\text{PV(Liabilities)}}, \qquad \text{Surplus} = \text{Assets} - \text{PV(Liabilities)}
$$
^f-09-05-16

- Overfunded above 100%, underfunded below; jurisdictions dictate the discount curve (corporates in the US, inflation-linked gilts in the UK, government bonds in the Netherlands) (V9 p.299).
- Surplus at risk is VaR applied to assets long and liabilities short, estimating how much assets might underperform liabilities, usually over one year; breaching the limit triggers reallocation toward liability-matching assets, which is liability-driven investing (V9 p.299, p.300).

**Gross exposure** (V9 p.298)
$$
\text{Gross exposure} = \left| \text{Long} \right| + \left| \text{Short} \right|
$$
^f-09-05-17

- Long-short, market neutral, and arbitrage hedge funds track long, short, and gross exposure separately; gross size flags how much correlation risk the book carries (V9 p.298).

## Worked examples

**Example 1: definition of VaR** (V9 p.255)
Q1: given a VaR of $12.5 million at 5% for one month, the correct statement is C, the minimum loss that would be expected to occur over one month 5% of the time is $12.5 million.
A fails because VaR never gives the likelihood of losing an exact amount, and B fails because VaR is a minimum loss, not an expected loss (V9 p.255).
Q2: the statement that is not correct is A, "a 1% VaR implies a downward move of 1%"; a 1% VaR is the point 2.33 standard deviations below the expected value, and the 1% is a probability, not a move size.
B and C are correct restatements: one standard deviation down is the 16% VaR, and 1.65 standard deviations below the mean is the 5% VaR (V9 p.255). ^ex-09-05-1

**Text demonstration: the parametric VaR of the $150 million SPY/SPLB portfolio, digit by digit** (V9 p.257, p.258, p.259, p.260)
Inputs after judgment overrides: 80% SPY with $E(R) = 10.5\%$, $\sigma = 20\%$; 20% SPLB with $E(R) = 6\%$, $\sigma = 8.5\%$; correlation $-0.06$ (V9 p.257).
Mean: $E(R_p) = 0.8(0.105) + 0.2(0.06) = 0.084 + 0.012 = 0.096000$ (Python: 0.096000).
Variance, term by term: $(0.8)^2(0.2)^2 = 0.64 \times 0.04 = 0.025600$; $(0.2)^2(0.085)^2 = 0.04 \times 0.007225 = 0.000289$; $2(0.8)(0.2)(-0.06)(0.2)(0.085) = -0.000326$; sum $= 0.025563$ (Python: 0.0255626).
Volatility: $\sqrt{0.0255626} = 0.159883$ (Python: 0.1598831), the curriculum's 15.99% (V9 p.259).
Daily scaling: $E(R_p) = 0.096/250 = 0.000384$ and $\sigma_p = 0.159883/\sqrt{250} = 0.159883/15.811388 = 0.010112$ (Python confirms both) (V9 p.259).
5% VaR, four steps: Step 1, $1.65 \times 0.010112 = 0.016685$; Step 2, $0.000384 - 0.016685 = -0.016301$; Step 3, flip the sign to 0.016301; Step 4, $0.016301 \times \$150{,}000{,}000 = \$2{,}445{,}150$ (Python with the curriculum's rounded steps: $2,445,150; fully unrounded: $2,445,094, an immaterial rounding difference) (V9 p.260).
Interpretation: on 5% of trading days the portfolio would be expected to lose at least $2,445,150 (V9 p.260). ^ex-09-05-2

**Example 2: parametric VaR** (V9 p.260, p.261)
Q1: the parameters of the normal distribution needed for parametric VaR are A, expected value and standard deviation; skewness and kurtosis describe non-normal distributions (V9 p.260).
Q2: 1% VaR on the same portfolio: Step 1, $2.33 \times 0.010112 = 0.023561$; Step 2, $0.000384 - 0.023561 = -0.023177$; Step 3, flip sign; Step 4, $0.023177 \times \$150\text{m} = \$3{,}476{,}550$, so A ($3.5 million) is correct (Python: 3,476,550 with curriculum rounding).
B ($2.4 million) is the 5% VaR and C ($1.4 million) is the one standard deviation (16%) VaR, $0.009728 \times 150\text{m} = \$1{,}459{,}200$ (Python: 1,459,200) (V9 p.261).
Q3: annual 5% VaR: annualize the daily inputs, $0.000384 \times 250 = 0.096000$ and $0.010112 \times \sqrt{250} = 0.159885$ (note the round-trip artifact, the direct figure is 0.159883).
Step 1, $0.159885 \times 1.65 = 0.263810$; Step 2, $0.096000 - 0.263810 = -0.167810$; Step 4, $0.167810 \times \$150\text{m} = \$25{,}171{,}500$, so B ($25 million) is correct (Python: 25,171,478 unrounded).
A ($38 million) multiplies the daily VaR by $\sqrt{250}$ (Python: $2{,}445{,}150 \times 15.8114 = \$38{,}661{,}216$) and C ($600 million) multiplies it by 250 (Python: $611 million); both mis-scale (V9 p.261). ^ex-09-05-3

**Text demonstration: historical simulation on the same portfolio** (V9 p.262, p.263)
Daily portfolio returns are rebuilt at fixed 80/20 weights: Day 1 is $0.8(0.0080) + 0.2(-0.0053) = 0.0064 - 0.00106 = 0.0053$, or 0.53% (Python: 0.534%) (V9 p.262).
Python check of the other rows: Day 2 $= 0.02\%$, Day 3 $= 0.07\%$, Day 5 $= -1.39\%$, all matching Exhibit 4; Day 4 computes to $-0.448\%$ from the printed SPY $-0.63\%$ and SPLB $+0.28\%$, while the exhibit shows $+0.56\% = 0.8(+0.0063) + 0.2(0.0028)$, so the printed SPY sign is a typo and the intended SPY return is $+0.63\%$.
All lookback returns are sorted worst to best and the percentile is read off (Excel's percentile function): 1% VaR $2,643,196; 5% VaR $1,622,272; 16% VaR $880,221 (V9 p.263).
These are data-determined (the underlying 1,006-day series is not printed), so they cannot be recomputed here; the comparison is the point, every historical VaR is far below its parametric counterpart because the lookback's SPY volatility (13.64%) was well under the 20% long-run input fed to the parametric model, and no normality was imposed (V9 p.263, p.264). ^ex-09-05-4

**Example 3: historical simulation VaR** (V9 p.265)
Q1: C is correct, a 5% historical simulation VaR is the fifth percentile, the point beyond which 5% of outcomes are larger losses.
A wrongly anchors on the expected value, and B imports the parametric 1.65 standard deviation machinery into a method that never computes a standard deviation (V9 p.265).
Q2: the limitation is A, the past may not repeat itself.
B is wrong because the method relies on no distribution at all, and C is wrong because the method never formally estimates a mean or variance to bias (V9 p.265). ^ex-09-05-5

**Text demonstration: Monte Carlo simulation on the same portfolio** (V9 p.266, p.267)
Using the parametric inputs, 10,000 correlated draws ($\rho = -0.06$) are generated, weighted 80/20, sorted, and read at the 1st, 5th, and 16th percentiles: 1% VaR $3,541,035; 5% VaR $2,517,702; 16% VaR $1,524,735 (V9 p.267).
These depend on the random seed and cannot be reproduced exactly; a Python rerun with the same parameters and 10,000 correlated draws gives $3,539,236, $2,475,253, and $1,460,517, matching the curriculum's figures to within sampling error and confirming the text's explanation that the small gap to the parametric VaR ($3,476,550, $2,445,150, $1,459,200) is sampling noise, not method (V9 p.267).
The distribution was specified normal only for comparability; the method's attraction is that virtually any distribution could have been used (V9 p.267). ^ex-09-05-6

**Example 4: Monte Carlo simulation VaR** (V9 p.268)
Q1: C is correct, Monte Carlo converges to the parametric answer when it uses the same distribution and parameters and a sufficiently large sample.
A is wrong because the parametric method cannot handle the non-normal case, and B is wrong because neither method works from historical outcomes directly (V9 p.268).
Q2: the advantage is B, flexibility to accommodate many distributions; there is no simple formula (A is wrong) and no parameter-determined number of required simulations (C is wrong, there is no industry standard) (V9 p.268). ^ex-09-05-7

**Example 5: advantages and limitations of VaR** (V9 p.271)
Q1: the non-advantage is B, "there is widespread agreement on how to calculate it"; there is none, and that subjectivity is a limitation.
A (simple to communicate) and C (comparable across portfolios and trading units) are genuine advantages (V9 p.271).
Q2: the limitation is C, VaR focuses exclusively on potential losses and ignores potential gains (the right tail).
A is wrong because only the parametric method typically needs normality, and B is wrong because regulators encourage or require VaR but never prescribe a maximum (V9 p.271). ^ex-09-05-8

**Text demonstration: CVaR and incremental VaR on the sample portfolio** (V9 p.272)
Historical CVaR: 5% of the 1,006 lookback returns is 50 observations (Python: $0.05 \times 1{,}006 = 50.3$, truncated to 50); the average of those 50 worst outcomes is $2,668,389, so once the $1,622,272 VaR is breached the expected loss is about $2.7 million (V9 p.272).
(The paragraph's opening reference to "our sample of 500 historical returns" is inconsistent with the 1,006-return sample used everywhere else; 1,006 is the operative count.)
Monte Carlo CVaR: 5% of 10,000 draws is 500 observations, whose average is $4,397,756; the text quotes the underlying 5% VaR as $2,517,705 here versus $2,517,702 earlier, a last-digit inconsistency in the curriculum (V9 p.272).
Incremental VaR: raising SPY to 90% lifts the parametric inputs to $E(R_p) = 0.9(0.105) + 0.1(0.06) = 0.1005$ and $\sigma_p = 0.179690$ (Python), daily $0.000402$ and $0.011365$; the new 5% VaR is $[1.65 \times 0.011365 - 0.000402] \times 150\text{m} \approx \$2{,}752{,}500$ and the IVaR is $2{,}752{,}500 - 2{,}445{,}150 = \$307{,}350$ (Python unrounded: new VaR $2,752,444, IVaR $307,294, matching to rounding) (V9 p.272). ^ex-09-05-9

**Example 6: extensions of VaR** (V9 p.273)
Q1: conditional VaR measures C, the average loss given that VaR is exceeded; it ignores losses inside the cutoff (not A) and makes no normal-versus-stressed market distinction (not B) (V9 p.273).
Q2: incremental VaR is A, the change in VaR from increasing a position in an asset; it reflects intentional exposure changes, not market volatility spikes (not B), and it is not a ranking gap between the two riskiest assets (not C) (V9 p.273).
Q3: marginal VaR is C, the change in VaR for a small change in a given holding; it is related to but not the same as incremental VaR (not A) and has nothing to do with margin calls (not B) (V9 p.273). ^ex-09-05-10

**Example 7: sensitivity risk measures** (V9 p.277, p.278)
Q1: B, duration and convexity are the first- and second-order effects of yield changes on bond prices; A and C describe duration alone, not convexity (V9 p.277).
Q2: the incorrect statement is B, delta does not precisely capture the change in call value; the relationship is approximate, while the 0-to-1 range (A) and the moneyness limits (C) are correct (V9 p.278).
Q3: A, gamma is a second-order effect and vega a first-order effect.
Gamma has nothing to do with volatility (B confuses it with vega), and C invents a sensitivity of volatility to the underlying price; the micro-arithmetic from the text confirms the mechanics, delta 0.6 with gamma 0.02 and a 0.10 rise in the underlying gives a new delta of $0.6 + 0.02 \times 0.10 = 0.602$ (Python: 0.002 increment) (V9 p.276, p.278). ^ex-09-05-11

**Example 8: scenario analysis** (V9 p.283)
Q1: the reverse stress test is A, identify the top 10 exposures and construct a hypothetical stress that hurts them all simultaneously; reverse stress testing targets the portfolio's own trouble spots.
B is an ordinary historical worst-day search, and C (reversing the signs of 2008) simulates a strong bull market (V9 p.283).
Q2: the participant least likely to run pass/fail stress tests is B, the long-only asset manager; without leverage, insolvency is remote, so pass/fail solvency screens matter less than underperformance, while banks (A) and levered hedge funds (C) must test capital survival (V9 p.283).
Q3: C, fully reprice the options under the scenario's market returns; delta (A) and delta plus gamma (B) are small-move approximations that misestimate scenario-sized shocks (V9 p.283). ^ex-09-05-12

**Example 9: limitations of risk measures** (V9 p.287, p.288)
Q1: the non-limitation is A; a well-executed VaR does adjust for bonds of different durations.
Reliance on recent historical correlations and volatilities (B) and inaccuracy when positions are large relative to market liquidity (C) are genuine VaR limitations (V9 p.287).
Q2: C is true, duration effectively assumes the correlation between the fixed-income exposure and the driving rate is 1 (all rates move by the same amount), while beta embeds the historical correlation between the equity and its index.
A is wrong because the 1 bp shock is applied to current rates, not a historical period, and B is wrong because sensitivities are too small-move to reveal extreme option behavior (V9 p.287).
Q3: the non-limitation is B, scenario measures assume no distribution at all; difficulty ascribing probabilities (A) and the impossibility of enumerating every future scenario (C) are real limitations (V9 p.288).
Q4: B, historical scenario analysis and VaR are both based on market returns from a particular historical period; hypothetical scenarios and sensitivity measures (A) are not, and delta and vega (C) are sensitivities, not history-based measures (V9 p.288). ^ex-09-05-13

**Text demonstration: desk-level budgets and the capital hurdle** (V9 p.289, p.292)
A bank with a EUR10 million total VaR appetite that hands five desks EUR2 million standalone limits each will never use its full appetite whenever desk correlations are below 1, because diversification benefits die at the desk level; the cures are over-allocation with pro rata clawbacks, or marginal VaR budgets that sum exactly to EUR10 million and let desks reinvest the diversification benefit (V9 p.289).
Capital hurdle: Portfolio A needs EUR325,000 of capital and expects EUR50,000 per year, a return on capital of $50{,}000/325{,}000 = 15.4\%$ (Python: 15.38%); Portfolio B expects EUR100,000 on EUR1,000,000, or 10.0%.
Against a 15% hurdle rate, A clears and B fails despite B's larger absolute income, so capital goes to A (V9 p.292). ^ex-09-05-14

**Example 10: creating constraints with risk measures** (V9 p.292, p.293)
Q1: the non-example of risk budgeting is C, cutting positions after a 5% monthly loss, which is a stop-loss limit; a desk VaR limit (A) and an ex ante tracking error allowance (B) are risk budgets (V9 p.292).
Q2: B, when marginal VaR is used the total risk budget equals the sum of the individual sub-portfolio budgets, by construction of the decomposition.
A denies exactly that property, and C describes the underutilization that arises when standalone (not marginal) VaRs are summed (V9 p.293). ^ex-09-05-15

**Example 11: uses of risk measures by market participants** (V9 p.301, p.302)
Q1: C, long-only asset managers most consistently express risk as a percentage of assets and relative to a benchmark; banks (A) and corporations (B) report mostly in currency units and absolute terms (V9 p.301).
Q2: C, ex ante tracking error pushes current holdings through the variability of historical markets, while ex post tracking error measures the realized deviation of historical holdings in historical markets.
A is wrong because ex post tracking error did capture the options actually held (and parametric ex ante versions may misstate options), and B is wrong because ex post tracking error forecasts nothing, it only records the past (V9 p.302). ^ex-09-05-16

## Item-set patterns

> [!warning] Trap 1: misreading the VaR statement
> The vignette quotes "a 5% one-day VaR of $X" and offers interpretations.
> Correct: X is the minimum loss expected on 5% of days; equivalently, losses of at least X occur about once a month of trading days (V9 p.253).
> Distractors say "expected maximum loss" (VaR bounds nothing above), "5% chance of losing exactly X" (VaR is a threshold, not a point probability), or "95% of the time we lose less than X" (most days are gains, not smaller losses) (V9 p.253, p.316).

> [!warning] Trap 2: the z-score and convention swap
> A question quietly switches between 5%, 1%, and 16% VaR or between confidence (95%) and tail (5%) language.
> Correct: 5% pairs with 1.65, 1% with 2.33, 16% with 1.00 standard deviation, and a higher confidence level always produces a larger VaR (V9 p.254, p.258).
> Distractors price the wrong percentile (the $2.4m option next to the $3.5m answer is the 5% number offered on a 1% question) or claim a 1% VaR means a 1% downward move (V9 p.255, p.261).

> [!warning] Trap 3: annualizing the VaR instead of the inputs
> Annual VaR is requested from daily figures, or vice versa.
> Correct: scale the mean by 250 and the standard deviation by $\sqrt{250}$, then rerun the VaR formula (V9 p.259).
> Distractors multiply the finished daily VaR by 250 or by $\sqrt{250}$; both appear as printed options ($600m and $38m against the correct $25m) and both mix the scaling laws of mean and volatility (V9 p.261).

> [!warning] Trap 4: method identification by fingerprint
> A paragraph describes an estimation process and asks which method it is.
> Correct: normality plus expected returns, volatilities, and correlations is parametric; repricing today's portfolio on actual past factor returns and sorting is historical simulation; user-specified distributions with random draws is Monte Carlo (V9 p.258, p.262, p.265).
> Distractors hinge on shared features, all three sort a distribution, both parametric and Monte Carlo can use normal inputs, and both simulation methods take percentiles, so anchor on the distinguishing assumption, not the shared mechanics (V9 p.268, p.318).

> [!warning] Trap 5: extension name matching
> CVaR, IVaR, MVaR, and relative VaR definitions are shuffled.
> Correct: CVaR averages the losses beyond the cutoff; IVaR differences the VaR before and after a discrete position change; MVaR is the calculus version for a very small change and its weighted parts sum to total VaR; ex ante tracking error is VaR on portfolio-minus-benchmark (V9 p.271, p.272).
> Distractors call MVaR the margin-call VaR, make IVaR a volatility-spike effect, or offer relative VaR when a tail average (CVaR) is described (V9 p.273, p.317).

> [!warning] Trap 6: sensitivities used where probabilities or big moves are needed
> A vignette asks what duration or delta says about likelihood, or applies delta-gamma to a crash scenario.
> Correct: sensitivities carry zero probability content and are built for small moves; scenario analysis on options or option-embedded bonds requires full revaluation (V9 p.280, p.284).
> Distractors let gamma or convexity "fix" the large-move problem (they are inadequate at scenario scale) or claim a same-sensitivity high-yield and investment-grade portfolio carry equal risk (spread volatilities differ) (V9 p.283, p.285).

> [!warning] Trap 7: constraint classification
> A described rule must be labeled risk budget, position limit, scenario limit, or stop-loss limit.
> Correct: allocation of VaR or tracking error appetite is a risk budget; a cap on market value or notional per name, country, or category is a position limit; a loss tolerance per stress event is a scenario limit; forced reduction after a realized loss over a period is a stop-loss limit (V9 p.289, p.290, p.291).
> Distractors relabel a stop-loss as a risk budget (Example 10's exact trick) or a 1.75%-per-security cap as a risk budget or stop-loss (it is a position limit) (V9 p.292, p.311).

> [!warning] Trap 8: participant-measure mismatches
> Four institutions are described and a measure must be assigned.
> Correct: banks use liquidity gap, trading-book VaR, leverage ratios, and economic capital; long-only managers use position limits, sensitivities, and ex ante tracking error in percent of assets; hedge funds add gross exposure, leverage, and maximum drawdown; pensions use surplus at risk; insurers split property-casualty (exposures, economic capital, VaR for catastrophe) from life (asset-liability matching, combined market and non-market scenarios) (V9 p.294 to p.301).
> Distractors give the pension's surplus at risk to a bank, or hand a leveraged hedge fund the low-confidence long-horizon preferences of an unleveraged manager (V9 p.293, p.298).

> [!warning] Trap 9: ex post versus ex ante tracking error
> A fund "monitors the historical deviation between portfolio returns and benchmark returns" and the question asks which measure that is.
> Correct: historical deviation of realized returns is ex post tracking error; ex ante tracking error pushes today's holdings through past market variability to estimate potential future deviation, and it reacts immediately to a strategy change while ex post lags until new data dominate (V9 p.297).
> Distractors offer active share (a holdings-overlap percentage, not a return deviation) or beta sensitivity (V9 p.297, p.319).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM05-Measuring-and-Managing-Market-Risk-Practice-Problems]]

## Cross-links

- [[LM04-Using-Multifactor-Models]]: supplies the factor machinery behind risk decomposition; the module's first step (converting holdings into factor exposures) and the equity manager's practice of regressing portfolios on growth, value, momentum, and size factors are LM4's models put to risk work.
- [[LM06-Backtesting-and-Simulation]]: takes over where this module stops, backtesting is how VaR's "reliability can be verified" advantage is executed, and LM6 deepens the historical and Monte Carlo simulation mechanics (rolling windows, sensitivity to assumptions) that generate the VaR distributions here.
- [[LM02-Valuation-of-Contingent-Claims]]: derives the delta, gamma, and vega this module uses as given; knowing the BSM sources of the Greeks explains why delta drifts to 1 or 0 with moneyness and why gamma peaks at the money near expiry.
- [[LM03-Valuation-and-Analysis-of-Bonds-with-Embedded-Options]]: provides the effective duration and convexity toolkit and the full-revaluation lattice that scenario analysis demands for option-embedded bonds, the exact instruments this module says delta-gamma and duration-convexity shortcuts misprice.
- [[LM04-Analysis-of-Financial-Institutions]]: the FSA view of the same banks and insurers profiled here; capital adequacy, liquidity, and reserve analysis there mirror the economic capital, liquidity gap, and reserve-driven measures in the participants section.

## Self-test

Vignette A for Q1 to Q4: A risk analyst runs a $200 million portfolio, 70% in an equity ETF (expected return 9%, standard deviation 18%) and 30% in a bond ETF (expected return 4%, standard deviation 6%), correlation 0.10, 250 trading days.
She computes parametric VaR at several thresholds and considers shifting the allocation to 80/20.

> [!question] Q1
> The portfolio's annual standard deviation is closest to:
> A. 12.73%.
> B. 12.90%.
> C. 14.40%.

> [!question] Q2
> The daily 5% parametric VaR in dollars is closest to:
> A. $1.57 million.
> B. $2.63 million.
> C. $2.69 million.

> [!question] Q3
> The annual 1% parametric VaR is closest to:
> A. $41.6 million.
> B. $45.1 million.
> C. $60.1 million.

> [!question] Q4
> If the allocation moves to 80/20 equity/bond, the incremental VaR (daily, 5%) is closest to:
> A. -$343,000.
> B. +$343,000.
> C. +$2,977,000.

Vignette B for Q5 to Q7: The same analyst holds a call option priced at 4.00 with delta 0.55, gamma 0.04, and vega 0.11, and a bond with duration 6.5, convexity 60, and yield 3%.
She is also drafting the fund's stress testing program and wants to identify the firm's most dangerous concentrations.

> [!question] Q5
> If the underlying rises by 2.00 and implied volatility rises by 1 percentage point, the estimated new call price using delta, gamma, and vega is closest to:
> A. 5.10.
> B. 5.18.
> C. 5.29.

> [!question] Q6
> If the bond's yield rises 50 bps, the estimated return using duration and convexity is closest to:
> A. -3.16%.
> B. -3.08%.
> C. +3.08%.

> [!question] Q7
> The exercise of identifying the portfolio's top 10 exposures and designing the market movements that would hurt them most is best described as:
> A. backtesting.
> B. reverse stress testing.
> C. historical scenario analysis.

Vignette C for Q8 to Q10: A consultant reviews risk frameworks at four institutions.
A pension fund measures how much assets could underperform liabilities at 95% confidence over a year; a hedge fund running merger arbitrage reports its worst peak-to-trough return; a bank allocates a 99.97% one-year loss estimate across desks; an asset manager liquidates any portfolio losing more than 6% in a month.
The consultant also examines a Monte Carlo output of 100 sorted portfolio outcomes whose five worst losses are $3.2, $2.8, $2.6, $2.5, and $2.4 million.

> [!question] Q8
> From the simulation output, the 5% VaR and CVaR are closest to:
> A. VaR $2.4 million; CVaR $2.7 million.
> B. VaR $2.7 million; CVaR $2.4 million.
> C. VaR $2.4 million; CVaR $3.2 million.

> [!question] Q9
> The asset manager's liquidation rule is best classified as a:
> A. stop-loss limit.
> B. scenario limit.
> C. risk budget.

> [!question] Q10
> The measures used by the pension fund, the hedge fund, and the bank are, respectively:
> A. surplus at risk; maximum drawdown; economic capital.
> B. relative VaR; gross exposure; leverage ratio.
> C. surplus at risk; conditional VaR; liquidity gap.

> [!success]- Answer key
> Q1: B.
> $\sigma_p = \sqrt{(0.7 \times 0.18)^2 + (0.3 \times 0.06)^2 + 2(0.7)(0.3)(0.10)(0.18)(0.06)} = \sqrt{0.015876 + 0.000324 + 0.000454} = 0.129049$ (Python: 12.9049%); A drops the correlation term (12.73%), C is the weighted average of the volatilities (14.40%), which ignores diversification entirely.
> Q2: B.
> Daily inputs: $0.075/250 = 0.000300$ and $0.129049/\sqrt{250} = 0.008162$; VaR $= (1.65 \times 0.008162 - 0.000300) \times 200\text{m} = \$2{,}633{,}382$ (Python: 2,633,382); A is the 16% one-sigma VaR ($1,572,353), C omits the expected-return offset ($1.65 \sigma$ alone gives $2,693,460).
> Q3: B.
> Annual: $(2.33 \times 0.129049 - 0.075) \times 200\text{m} = \$45{,}136{,}754$ (Python: 45.14m); A multiplies the daily 5% VaR by $\sqrt{250}$ ($41.6m, wrong on two counts, scaling and z), C omits the mean ($2.33 \times 0.129049 \times 200\text{m} = 60.1\text{m}$).
> Q4: B.
> At 80/20: $E(R_p) = 0.080$, $\sigma_p = 0.145690$, daily VaR $= \$2{,}976{,}702$ (Python), so IVaR $= 2{,}976{,}702 - 2{,}633{,}382 = +\$343{,}320$; A flips the sign (risk rises when the riskier asset's weight rises against a low correlation), C is the new VaR itself, not the increment.
> Q5: C.
> $\Delta c = 0.55 \times 2.00 + \tfrac{1}{2}(0.04)(2.00)^2 + 0.11 \times 1 = 1.10 + 0.08 + 0.11 = 1.29$, new price $4.00 + 1.29 = 5.29$ (Python: 5.29); A is delta only (5.10), B is delta plus gamma but no vega (5.18), each dropping a requested term.
> Q6: B.
> $\Delta B/B = -6.5 \times 0.005/1.03 + \tfrac{1}{2}(60)(0.005)^2/1.03^2 = -0.031553 + 0.000707 = -0.030846$, about $-3.08\%$ (Python: -3.0846%); A is duration only ($-3.16\%$), C flips the sign, forgetting that prices fall when yields rise, and convexity always adds back, never subtracts, for an option-free bond.
> Q7: B.
> Targeting the portfolio's own most significant exposures and asking what would make them risky is reverse stress testing (V9 p.281); A verifies a VaR model's breach frequency against history, C replays an actual past period rather than starting from the portfolio's concentrations.
> Q8: A.
> With 100 outcomes, the 5% VaR is the fifth-worst outcome, $2.4 million (the minimum loss in the worst 5%), and CVaR is the average of the five worst, $(3.2 + 2.8 + 2.6 + 2.5 + 2.4)/5 = \$2.7$ million (Python: 2.7); B swaps the two, C uses the single worst loss for CVaR instead of the tail average.
> Q9: A.
> Forced liquidation after a realized loss of a given size in a specified period is the definition of a stop-loss limit (V9 p.291); a scenario limit caps modeled losses under a hypothetical event, not realized losses, and a risk budget allocates VaR or tracking error appetite before the fact.
> Q10: A.
> Assets-minus-liabilities VaR is surplus at risk (pension), worst peak-to-trough return is maximum drawdown, standard for event-driven and non-normal hedge fund strategies, and a 99.97% one-year loss estimate allocated across businesses is economic capital (bank) (V9 p.298, p.299, p.295); B and C reassign each institution a measure it uses at most secondarily, and the hedge fund item in C (CVaR) was never described.

## Flashcards

#flashcards/cfa-l2/09-Portfolio-Management/lm05

Value at risk (VaR) definition::The minimum loss expected a certain percentage of the time over a certain period of time, given assumed market conditions (V9 p.253).
Three explicit elements of a VaR statement::Size of the loss (currency or percent), probability (frequency), and time horizon (V9 p.253).
Is VaR a minimum or a maximum loss?::A minimum loss; the most one can lose is the entire portfolio (V9 p.253).
The 5% VaR corresponds to how many standard deviations below the mean?::1.65 under a normal distribution (V9 p.254).
The 1% VaR corresponds to how many standard deviations below the mean?::2.33 under a normal distribution (V9 p.254).
A one standard deviation downward move equals which VaR?::The 16% VaR, an 84% confidence level (V9 p.254).
Risk decomposition::The first step of every VaR method, converting portfolio holdings into exposures to risk factors (V9 p.256).
Which VaR methods formally require a data history?::Only historical simulation; parametric and Monte Carlo need parameter estimates, often seeded from history but adjustable by judgment (V9 p.256).
Fingerprint of the parametric VaR method::Assumes a distribution (normally the normal) and computes VaR from expected returns, volatilities, and correlations (V9 p.258).
Fingerprint of the historical simulation method::Reprices the current portfolio on each day of the lookback, sorts outcomes, and reads the percentile; no distribution assumed (V9 p.262).
Fingerprint of the Monte Carlo method::User-specified distribution, thousands of correlated random draws, reprice, sort, read the percentile (V9 p.265).
Convert an annual expected return and volatility to daily::Divide the return by 250 and the volatility by the square root of 250 (V9 p.259).
Four steps of parametric VaR::Multiply sigma by z, subtract from the expected return, flip the sign, multiply by portfolio value (V9 p.260).
Micro-problem, daily 5% VaR with mean 0.0384% and sigma 1.0112% on $150m::1.65 x 0.010112 = 0.016685; 0.000384 - 0.016685 = -0.016301; flip; x 150m = $2,445,150 (V9 p.260).
Micro-problem, same portfolio 1% VaR::2.33 x 0.010112 = 0.023561; 0.000384 - 0.023561 = -0.023177; x 150m = $3,476,550 (V9 p.261).
Biggest weakness of parametric VaR with options::Truncated option payoffs make returns non-normal, which the normal-based method handles badly (V9 p.261).
Primary advantage and weakness of historical simulation::It uses only outcomes that actually happened (nothing impossible), but the past may not repeat (V9 p.264).
Which methods can accommodate options well?::Historical simulation and Monte Carlo; both capture actual or fully repriced option behavior (V9 p.264, p.267).
When does Monte Carlo VaR converge to parametric VaR?::Same distribution, same parameters, and a sufficiently large number of simulations (V9 p.268).
Name four limitations of VaR::{{Subjectivity, underestimating extreme (left-tail) events, ignoring liquidity, correlation risk in stress, trending and volatility regimes, misread as worst case, oversimplification, disregard of the right tail}} (V9 p.270, p.271).
Trending limitation of VaR::A portfolio can lose just under its VaR limit day after day, accumulating large losses without a breach (V9 p.270).
Conditional VaR (CVaR)::The average loss conditional on exceeding the VaR cutoff; also called expected shortfall or expected tail loss (V9 p.271, p.272).
Best methods for computing CVaR::Historical simulation and Monte Carlo, by averaging observed tail losses; parametric needs out-of-scope mathematics (V9 p.272).
Incremental VaR (IVaR)::The change in portfolio VaR from adding, deleting, or resizing a position; new VaR minus old VaR (V9 p.272).
Marginal VaR (MVaR)::Calculus-based effect on VaR of a very small position change; weighted MVaRs sum to total VaR (V9 p.272).
Ex ante tracking error (relative VaR)::VaR applied to the portfolio holdings minus benchmark holdings (benchmark as short positions), usually one sigma annualized (V9 p.272, p.273).
Ex post vs ex ante tracking error::Ex post measures realized historical deviation from the benchmark; ex ante pushes current holdings through past market variability (V9 p.297).
Which reacts first to a strategy change, ex ante or ex post tracking error?::Ex ante, immediately; ex post lags until new data dominate the history (V9 p.297).
Active share (as a risk constraint)::The percentage of the portfolio that differs from the benchmark, monitored to help limit tracking error (V9 p.297).
Beta as a risk measure::Covariance of asset and market returns divided by market variance; sensitivity to the equity risk premium; market average is 1.0 (V9 p.274).
Duration in one sentence::Weighted-average time to maturity acting as the first-order sensitivity of bond price to a single change in all rates (V9 p.275).
Convexity in one sentence::The sensitivity of duration to rate changes, a second-order correction needed for large yield moves and long horizons (V9 p.275).
Delta ranges for calls and puts::Calls 0 to 1, puts 0 to -1; deep in-the-money approaches the bound, deep out-of-the-money approaches 0 (V9 p.276).
When is gamma largest?::Near the money and close to expiration, when a small underlying move decides the option's fate (V9 p.276, p.277).
Micro-problem, delta 0.6 and gamma 0.02, underlying up 0.10; new delta?::0.6 + 0.02 x 0.10 = 0.602 (V9 p.276).
What do sensitivity measures not tell you?::The probability of the underlying change, and which portfolio has greater loss potential (no volatility distinction) (V9 p.284, p.285).
Two features distinguishing scenario measures from sensitivities::Multiple factors moved at once, and much larger movements (V9 p.278).
Historical scenario::Portfolio return from replaying a specific past period (1987 crash, 2008 crisis) with full repricing of current holdings (V9 p.279).
Hypothetical scenario::Extreme movements and co-movements that have not occurred; hard to assign probability but the only way to test unseen events (V9 p.281).
Reverse stress testing::Identify the portfolio's most significant exposures, then design the scenarios that would damage them most (V9 p.281).
Why must options be fully repriced in scenarios?::Delta-gamma (and duration-convexity) are small-move approximations, inadequate for scenario-sized shocks (V9 p.280, p.283).
Who runs single-factor pass/fail stress tests?::Leveraged parties, banks and hedge funds, testing whether a shock would impair capital (V9 p.282).
What makes a risk framework restrictive?::The limit placed on the measure, not the confidence level of the measure (V9 p.288).
Risk budgeting::Agreeing the total risk appetite at the top and allocating it to sub-activities, typically in VaR or ex ante tracking error terms (V9 p.289).
Why do standalone desk VaR limits underuse the firm's appetite?::Summing standalone VaRs ignores diversification across desks; cure with over-allocation or marginal VaR budgets (V9 p.289).
Position limits::Caps on market value or notional per issuer, currency, country, category, gross long-short size, or liquidity tier; the control for the event and single-name risk VaR handles poorly (V9 p.290).
Scenario limit::A tolerance on estimated loss for a given scenario, set higher for the more extreme scenarios, triggering corrective action if crossed (V9 p.290, p.291).
Stop-loss limit::Required size reduction or liquidation after a realized loss of a given size in a specified period; the answer to VaR's trending problem (V9 p.291).
Economic capital::The capital a firm needs to survive severe losses from its risks, measured at very high confidence (99% to 99.99%) usually over one year (V9 p.291, p.295).
Capital allocation hurdle logic::Compare each activity's expected return per unit of allocated capital with the hurdle rate; 50k on 325k (15.4%) beats a 15% hurdle, 100k on 1m (10%) fails it (V9 p.292).
Three drivers of which risk measures a participant uses::Degree of leverage, mix of risk factors, and accounting or regulatory regime (V9 p.293).
Bank risk measure set::Liquidity gap, trading-book VaR, leverage ratio, sensitivities including Greeks by tenor, economic capital, scenario analysis and stress tests on the full balance sheet (V9 p.294, p.295).
How do long-only managers express VaR and duration?::As percentages of net assets, and usually relative to a benchmark (V9 p.296).
Hedge fund specific measures::Gross exposure (long plus short absolute values), leverage, high-confidence short-horizon VaR, strategy-tuned scenarios, maximum drawdown (V9 p.298).
Maximum drawdown (as a risk measure)::Worst-returning month or quarter, or worst peak-to-trough decline; supplements sigma and beta for non-normal strategies (V9 p.298).
Surplus at risk::VaR with assets long and pension liabilities as short fixed-income positions; how much assets might underperform liabilities, usually over one year (V9 p.299).
Property and casualty insurer risk measures::Sensitivities against target asset allocation ranges, economic capital and VaR for catastrophic loss, scenarios stressing market and insurance risks together (V9 p.300, p.301).
Life insurer risk emphasis::Long discount-rate-sensitive liabilities, closer asset-liability matching, scenarios stressing market and non-market (longevity) factors together (V9 p.301).
The trap answer when a question asks for annual VaR from a daily VaR::Any option formed by multiplying the daily VaR by 250 or by root 250; rescale the inputs instead (V9 p.261).

## Common mistakes

1. Reading VaR as an expected loss or a maximum loss; it is a minimum loss at the stated frequency, and losses can and will exceed it (V9 p.253, p.270).
2. Saying "95% of the time we will lose less than X", which implies losing on 95% of days; the correct complement is that returns are at least $-X$ 95% of the time, gains included (V9 p.253, p.316).
3. Mismatching the z-score and the threshold: 1.65 belongs to 5%, 2.33 to 1%, 1.00 to 16%; adjacent answer options price the other conventions (V9 p.254, p.261).
4. Annualizing a daily VaR by multiplying by 250 or $\sqrt{250}$ instead of annualizing the mean (times 250) and the volatility (times $\sqrt{250}$) and recomputing (V9 p.259, p.261).
5. Forgetting to subtract the expected return before applying the z multiple, which overstates VaR; the omission is a printed distractor in the annual VaR problems (V9 p.260, p.320).
6. Attributing a normality assumption to historical simulation, or historical outcomes to the parametric and Monte Carlo methods; each method's fingerprint is its distribution treatment (V9 p.262, p.265, p.318).
7. Confusing the extensions: CVaR is the tail average, IVaR the before-and-after difference for a discrete change, MVaR the small-change derivative whose parts sum to total VaR, relative VaR the portfolio-minus-benchmark VaR (V9 p.271, p.272).
8. Treating sensitivities as if they carried probability or volatility information; equal spread durations do not mean equal risk when spread volatilities differ (V9 p.284, p.285).
9. Applying delta-gamma or duration-convexity approximations inside scenario analysis for options or option-embedded bonds instead of full revaluation (V9 p.280, p.283, p.317).
10. Using an instrument's own price history (or historical durations) in a historical scenario; historical yields and spreads drive correct repricing because the instrument's characteristics have changed with time (V9 p.279, p.317).
11. Classifying a stop-loss rule as risk budgeting or a position cap as a risk budget; budgets allocate appetite ex ante, position limits cap market value, stop-losses trigger on realized losses (V9 p.289, p.290, p.291, p.292).
12. Claiming summed standalone desk VaRs equal the firm's VaR; only marginal VaR budgets sum to the total, and standalone summing strands diversification benefits (V9 p.289, p.293).
13. Assigning the wrong measure to the wrong participant, for example surplus at risk to a bank or high-confidence two-week VaR to an unleveraged long-only manager (V9 p.293, p.299).
14. Confusing ex post with ex ante tracking error, or either with active share; realized-deviation language signals ex post (V9 p.297, p.319).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "09-05" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
