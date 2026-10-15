---
type: cfa-lm
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
volume: 9
lm: 1
title: "Economics and Investment Markets"
pages: "3-89"
weight_band: "10-15%"
difficulty: 3
los_count: 11
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/portfolio-management]
---

# LM1: Economics and Investment Markets

Difficulty 3 of 5: the arithmetic is light (a handful of implied-premium subtractions and one present-value table), but eleven "explain" LOS build a dense web of premium symbols and countercyclical relationships, and every item set swaps a sign or a direction somewhere to catch a candidate who memorized labels instead of the covariance logic underneath them.

## LOS map

- **explain** the notion that to affect market values, economic factors must affect one or more of the following: 1) default-free interest rates across maturities, 2) the timing and/or magnitude of expected cash flows, and 3) risk premiums (V9 p.3) ^los-09-01-a
    - Examiner asks: given a shock (real rate rise, inflation surprise, cash flow revision), identify which channel of the pricing equation moves the price and in which direction, as in Practice Problem 1.
- **explain** the role of expectations and changes in expectations in market valuation (V9 p.3) ^los-09-01-b
    - Examiner asks: why a price can fall on "good" news, and the answer is that only the surprise relative to what was already anticipated moves prices, since anticipated information is already in the price.
- **explain** the relationship between the long-term growth rate of the economy, the volatility of the growth rate, and the average level of real short-term interest rates (V9 p.3) ^los-09-01-c
    - Examiner asks: rank countries by real short-term rate from a table of nominal GDP growth, inflation, and growth volatility, forcing you to subtract inflation first and then weigh both growth and volatility.
- **explain** how the phase of the business cycle affects policy and short-term interest rates, the slope of the term structure of interest rates, and the relative performance of bonds of differing maturities (V9 p.3) ^los-09-01-d
    - Examiner asks: what the yield curve does in a recession (steepens, because the policy rate is cut hard at the short end while long yields anticipate recovery) and to compute a Taylor rule policy rate from l, inflation, target inflation, and the output gap.
- **describe** the factors that affect yield spreads between non-inflation-adjusted and inflation-indexed bonds (V9 p.3) ^los-09-01-e
    - Examiner asks: decompose the break-even inflation rate into expected inflation plus an inflation-uncertainty premium, and conclude "indeterminate" when the two components move in opposite directions.
- **explain** how the phase of the business cycle affects credit spreads and the performance of credit-sensitive fixed-income instruments (V9 p.3) ^los-09-01-f
    - Examiner asks: which bond outperforms when a recession hits (high quality beats low quality as spreads widen) and which outperforms when spreads narrow (low rated beats high rated).
- **explain** how the characteristics of the markets for a company's products affect the company's credit quality (V9 p.3) ^los-09-01-g
    - Examiner asks: whose spread widens most in a downturn, and the answer stacks cyclicality of the product on top of a low rating, with airlines as the curriculum's standing example.
- **explain** the relationship between the consumption hedging properties of equity and the equity risk premium (V9 p.3) ^los-09-01-h
    - Examiner asks: what a large equity risk premium implies about the correlation between equity payoffs and consumption (positive, so equities are a poor hedge) and which asset is the good hedge (short-dated default-free bonds).
- **explain** how the phase of the business cycle affects short-term and long-term earnings growth expectations (V9 p.3) ^los-09-01-i
    - Examiner asks: whether cyclical or non-cyclical companies show the sharper earnings swing at each phase, especially the sharp cyclical earnings rebound coming out of a recession.
- **describe** cyclical effects on valuation multiples (V9 p.3) ^los-09-01-j
    - Examiner asks: which change in the pricing equation justifies a higher equilibrium P/E (higher expected real earnings growth, lower l, lower expected inflation, lower inflation uncertainty, lower equity premium) and which change lowers it.
- **describe** the economic factors affecting investment in commercial real estate (V9 p.3) ^los-09-01-k
    - Examiner asks: why the commercial real estate discount rate stacks a credit-like premium, an equity-like premium, and a liquidity premium on the nominal rate, and to run the rent-plus-resale present value at that stacked rate.

## Core intuition

The whole module is one equation applied five times.
Every financial asset is a claim on the real economy, so its price is the sum of its expected cash flows discounted at a rate built from a real default-free rate, expected inflation, and one or more risk premiums (V9 p.4, p.5).
Each asset class differs from the next only in which premiums appear in the denominator and how uncertain the numerator is, so the module walks the spectrum from real default-free bonds (no premiums) to commercial real estate (every premium at once) (V9 p.5, p.71).
The economy can move a price only through three channels: the default-free rates, the timing or magnitude of expected cash flows, or the risk premiums (V9 p.3, p.5).

> [!abstract] Idea 1: one pricing equation, premiums stacked as certainty erodes
> Real default-free bond: discount at $l_{t,s}$ alone, so only real-rate changes move the price (V9 p.26).
> Nominal default-free bond: add expected inflation $\theta_{t,s}$ and the inflation-uncertainty premium $\pi_{t,s}$ (V9 p.27).
> Credit-risky bond: add the credit premium $\gamma^i_{t,s}$ (V9 p.49).
> Equity: add the extra equity premium $\kappa^i_{t,s}$, with $\lambda^i_{t,s} = \gamma^i_{t,s} + \kappa^i_{t,s}$ the equity risk premium versus default-free debt (V9 p.60).
> Commercial real estate: add the liquidity premium $\phi^i_{t,s}$ on top of all of the above (V9 p.71).

Expectations do the pricing, not history.
Asset values depend on expected future cash flows conditional on today's information, so information that was fully anticipated is already in the price and only news, the surprise relative to expectations, forces prices to adjust (V9 p.6, p.7).
That is why markets can fall on "good" data: if the expectation was for better, the release is bad news relative to the price (V9 p.7).
Investor sentiment can also move values, but it works through the discount rate, by raising or lowering risk premiums, rather than through the economy's direct effect on cash flows (V9 p.7).

The real default-free rate is not zero even without default or inflation risk, because investing means not consuming today.
The marginal utility of one more unit of consumption in the future relative to one more unit today is the inter-temporal rate of substitution $\tilde m_{t,s}$, and the price of a one-period real default-free bond is exactly the expectation of that ratio (V9 p.8, p.9).
In good times current consumption is high, marginal utility of consuming today is low, $\tilde m$ is low, bond prices are low, and real rates are high; in bad times the reverse (V9 p.8).
Every investor trades until Equation 3 holds, so the equilibrium bond price aggregates every participant's willingness to defer consumption (V9 p.10, p.11).
Because marginal utility diminishes with wealth, wealthier investors hold the safe asset only at a lower price, demand smaller premiums for risk, and shift toward risky assets (decreasing absolute risk aversion) (V9 p.12).

> [!abstract] Idea 2: the covariance with bad times is the risk premium
> A risky asset's premium is driven by the covariance between its future payoff and the inter-temporal rate of substitution (V9 p.15, p.17).
> Most risky assets pay off in good times, exactly when the marginal value of consumption is low, so the covariance is negative, today's price is lower, and the required return carries a positive premium (V9 p.15).
> An asset that pays off in bad times is a consumption hedge: its covariance is positive, its premium negative, its price high, and its required return can sit below the risk-free rate (V9 p.17, p.20).
> Even a default-free two-period bond bears a small premium, because its price one period ahead is uncertain and covaries negatively with $\tilde m$ (V9 p.14, p.16).

Growth and volatility set the level of real rates.
Higher expected real GDP growth means more goods and services tomorrow, so investors save less and borrow more, and the real rate must rise to clear the market; higher volatility of growth means more income risk, more precautionary saving, and again higher required real rates on offer for risk-averse savers (V9 p.13, p.17, p.18).
So real rates should be higher in fast-growing, volatile developing economies than in slow, stable developed ones, and the UK "great moderation" evidence links falling GDP volatility to the 1990-2007 decline in index-linked gilt real yields (V9 p.18, p.23).
After 2008, real yields fell despite higher volatility because expected future growth fell further, and safe-haven demand for scarce index-linked bonds pushed some real yields negative (V9 p.24, p.25).

Short-term nominal rates add expected inflation and track the central bank's policy rate.
A T-bill's horizon is so short that the inflation-uncertainty premium is negligible, so its yield is approximately $l_{t,s} + \theta_{t,s}$, and T-bill yields hug both measured inflation and the policy rate (V9 p.27, p.28, p.29).
The Taylor rule benchmarks that policy rate: the neutral rate (real rate plus target inflation) plus half the inflation gap plus half the output gap, with the effective weight on inflation 1.5 because inflation enters twice (V9 p.30).
Positive output gaps come with high or rising inflation, negative gaps with high unemployment, and a central bank that holds rates "too low for too long" can inflate a credit bubble, as the rule suggests the Fed did in 2002-2005 (V9 p.30, p.31, p.32).

The gap between nominal and real default-free yields of the same maturity is the break-even inflation rate, and it is not a pure forecast.
BEI equals expected inflation $\theta_{t,s}$ plus the inflation-uncertainty premium $\pi_{t,s}$, so a 2.0% BEI implies expected inflation below 2.0% whenever the premium is positive (V9 p.33).
The premium grows with maturity because investors trust their inflation view over three months far more than over twenty years (V9 p.33).
In the 2008-2009 downturn BEI rates fell across developed markets as weaker demand meant weaker expected inflation, with Italian 10-year BEI dropping from 2.3% to 0.8% (V9 p.33, p.34).

The slope of the curve is the business-cycle dial.
In a recession the central bank cuts the policy rate hard, but long yields fall less because short rates are expected back to normal as the recession recedes, so the curve steepens; late expansion brings peak inflation and high short rates, so the curve flattens or inverts, and inversion is read as a recession predictor (V9 p.40, p.42).
Level, slope, and curvature explain nearly all curve movement (level alone 92.7% in the United States and 95.2% in the United Kingdom) (V9 p.39).
On top of expectations sits a bond risk premium that rises with maturity: long bonds hedge bad times less well than short bonds, average term spreads are positive (0.50% US and 0.40% UK post-1945), and returns on government bonds correlate negatively with GDP, which is why the "normal" curve slopes up (V9 p.43, p.44).
An upward slope is therefore ambiguous about the path of rates, because it can reflect expected hikes, or flat expectations plus premiums, or even expected cuts more than offset by premiums; supply, demand, and regulation (the UK pension rules that inverted the long gilt end) can distort it further (V9 p.46, p.47).

Credit stacks a default premium on the same machinery.
The credit spread compensates for expected loss, which is default probability times one minus the recovery rate, plus a true risk premium, because defaults cluster in downturns and cannot be fully diversified away (V9 p.50, p.51).
Spreads widen going into recessions and narrow in recoveries; recovery rates themselves are procyclical, so loss rates are countercyclical (V9 p.50, p.53).
When spreads narrow, investors stop discriminating and low-rated bonds outperform; when the cycle turns down, high-rated bonds outperform as the quality spread widens (V9 p.54, p.59).
Sector matters through the product: consumer cyclical and airline spreads blow out in recessions while non-cyclical spreads move modestly, and company-level ratios (interest coverage 17.6x for Aaa versus 0.9x for B) anchor the rating (V9 p.55, p.56).
Sovereigns are not exempt: emerging market spreads and eurozone CDS premiums repriced dramatically in 2008-2011 as ability to pay deteriorated (V9 p.57, p.58).

Equities strip away even the cash flow schedule.
Dividends are discretionary, can fall or vanish, and equity holders stand behind debt holders in bankruptcy, so equity demands $\kappa^i_{t,s}$ on top of the credit premium (V9 p.60).
Equities pay off in good times and crash in recessions, so they are a poor consumption hedge and the ex post equity premium is large: 2.2% (Switzerland) to 5.1% (Australia) per year over 1900-2017, 4.5% for the United States, roughly 3% to 5% ex ante (V9 p.61, p.66, p.67).
Earnings are procyclical and cyclical sectors amplify the swing; sharp profit rebounds off a lowered cost base can lead the economy out of recession, which makes profits a leading indicator (V9 p.62, p.63).
P/Es rise in expansions and fall in recessions, and a higher equilibrium P/E can be justified by higher expected real earnings growth, lower real rates, lower expected inflation, lower inflation uncertainty, or a lower equity premium; Shiller's CAPE smooths earnings over ten years, and extreme CAPE peaks (1929, 1999) preceded negative 10-year real returns (V9 p.68, p.69).

Commercial real estate is part bond, part equity, and illiquid.
Rents are contractual, sometimes upward-only or indexed, so the income stream is bond-like and its quality depends on tenant credit; the uncertain end-of-lease property value adds the equity-like piece; and exit takes months or years, so a liquidity premium $\phi^i_{t,s}$ is demanded because an illiquid asset is useless as a hedge exactly when you need cash (V9 p.70, p.71, p.72).
UK rental income grew a stable 6.5% nominal per year over 30 years, but capital values are strongly procyclical (down 26% in the UK 1990s recession, down 55.5% in Ireland 2008-2009), so the required premium sits nearer the equity premium than the bond premium (V9 p.73, p.74, p.75).

## Formulas and derivations

**Fundamental pricing equation (Equation 1)** (V9 p.5)
$$
P_t^i = \sum_{s=1}^{N} \frac{E_t\!\left[\widetilde{CF}^{\,i}_{t+s}\right]}{\left(1 + l_{t,s} + \theta_{t,s} + \rho^i_{t,s}\right)^s}
$$
^f-09-01-1

- $P_t^i$: value of asset $i$ today; $N$: number of cash flows; $\widetilde{CF}^{\,i}_{t+s}$: uncertain nominal cash flow $s$ periods ahead; $E_t[\cdot]$: expectation conditional on today's information.
- $l_{t,s}$: yield today on a real default-free investment paying one unit at $t+s$; $\theta_{t,s}$: expected inflation between $t$ and $t+s$; $\rho^i_{t,s}$: asset-specific risk premium.
- General enough for every instrument: a zero has one cash flow, an equity has $N \to \infty$; the economy acts only through the numerator (expected cash flows) or the denominator (discount rates) (V9 p.5).

**Discount rate build-up (Equation 2)** (V9 p.6)
$$
1 + l_{t,s} + \theta_{t,s} + \rho^i_{t,s}, \qquad s = 1, \ldots, N
$$
^f-09-01-2

- The additive form approximates the exact multiplicative compounding of the three components (V9 p.6).
- $\rho^i_{t,s}$ varies by asset class and over time, rising in recessions when investors are less willing to bear default risk, and can include liquidity risk as well as cash flow risk (V9 p.6).

**Price of a one-period real default-free bond (Equation 3)** (V9 p.9)
$$
P_{t,s} = E_t\!\left(1 \cdot \tilde m_{t,s}\right) = E_t\!\left(\tilde m_{t,s}\right)
$$
^f-09-01-3

- $\tilde m_{t,s}$: inter-temporal rate of substitution, the ratio of marginal utility of consumption at $t+s$ to marginal utility today, a random variable because future income is uncertain (V9 p.8, p.9).
- Technically $\tilde m_{t,s} = \delta \, MU(C_{t+s})/MU(C_t)$ with $\delta$ a pure time-preference discount factor; the same object is the stochastic discount factor or pricing kernel (V9 p.9).
- Holds in equilibrium because any investor whose expected $\tilde m$ exceeds the price buys, pushing own consumption down and marginal utility up until expectation and price converge for everyone (V9 p.10).

**One-period real risk-free rate (Equation 4)** (V9 p.11)
$$
l_{t,1} = \frac{1 - P_{t,1}}{P_{t,1}} = \frac{1}{E_t\!\left(\tilde m_{t,1}\right)} - 1
$$
^f-09-01-4

- The return is payoff minus price over price, so the real rate is inversely related to the expected inter-temporal rate of substitution (V9 p.11).
- High real rates mean current consumption is dear relative to future consumption; this is the hinge connecting GDP growth (which lowers $E_t(\tilde m)$) to rates (V9 p.11, p.17).

> [!tip] Calculator
> $E_t(\tilde m) = 0.954498$: `1 / 0.954498 = - 1 =` gives 0.047671, or 4.7671%.

**Multi-period default-free bond pricing (Equation 5)** (V9 p.13)
$$
P_{t,s} = E_t\!\left(\tilde P_{t+1,s-1}\, \tilde m_{t,1}\right)
$$
^f-09-01-5

- $\tilde P_{t+1,s-1}$: next period's uncertain market price of the bond, whose maturity has shrunk by one period; add any coupon promised at $t+1$ to the right-hand side (V9 p.13).
- The one-period bond's certain payoff is replaced by a random resale price, and that price risk is what creates a term premium on default-free bonds (V9 p.13, p.14).

**Covariance decomposition of price (Equation 6)** (V9 p.15)
$$
P_{t,s} = \frac{E_t\!\left(\tilde P_{t+1,s-1}\right)}{1 + l_{t,1}} + \mathrm{cov}_t\!\left(\tilde P_{t+1,s-1},\, \tilde m_{t,1}\right)
$$
^f-09-01-6

- First term: risk-neutral present value, the expected future price discounted at the risk-free rate; second term: the discount (or premium) for risk (V9 p.15).
- Derivation: $E_t(\tilde x \tilde y) = E_t(\tilde x)E_t(\tilde y) + \mathrm{cov}(\tilde x, \tilde y)$ applied to Equation 5, then substitute $E_t(\tilde m_{t,1}) = 1/(1 + l_{t,1})$ from Equation 4 (V9 p.14, p.15).
- For a one-period default-free bond the future payoff is the constant 1, the covariance is zero, and Equation 6 collapses to Equation 3; for risky assets the covariance is typically negative, so price is lower and required return higher (V9 p.15).

**Expected holding-period return and the risk premium (Equations 7 and 8)** (V9 p.16)
$$
r_{t,s} = \frac{E_t\!\left(\tilde P_{t+1,s-1}\right) - P_{t,s}}{P_{t,s}}, \qquad r_{t,s} - l_{t,1} = -\frac{\left(1 + l_{t,1}\right)}{P_{t,s}}\,\mathrm{cov}_t\!\left(\tilde m_{t,1},\, \tilde P_{t+1,s-1}\right) = \rho^i_{t,s}
$$
^f-09-01-7

- The premium over the risk-free rate is proportional to minus the covariance: the more negative the covariance with $\tilde m$, the larger the premium and the lower today's price (V9 p.15, p.16).
- An asset with positive covariance (pays off in bad times) hedges consumption, carries a negative premium, and can require less than the risk-free rate (V9 p.17).

**Real default-free bond pricing (Equation 9)** (V9 p.26)
$$
P_t^i = \sum_{s=1}^{N} \frac{CF^i_{t+s}}{\left(1 + l_{t,s}\right)^s}
$$
^f-09-01-8

- Cash flows are certain in real terms, so only changes in $l_{t,s}$ move the price, and $l_{t,s}$ is set by expected growth and growth volatility through aggregated saving decisions (V9 p.26).
- Proxy in practice: yields on short-dated inflation-linked government bonds (TIPS, index-linked gilts) (V9 p.21).

**Nominal default-free bond pricing (Equation 10)** (V9 p.27)
$$
P_t^i = \sum_{s=1}^{N} \frac{CF^i_{t+s}}{\left(1 + l_{t,s} + \theta_{t,s} + \pi_{t,s}\right)^s}
$$
^f-09-01-9

- $\theta_{t,s}$: expected inflation; $\pi_{t,s}$: risk premium for inflation uncertainty, not asset specific, growing with horizon because inflation is harder to forecast over 20 years than over 3 months (V9 p.27, p.33).
- The payoff is certain in nominal terms; it is the real value of that payoff that is risky, hence $\pi_{t,s}$ (V9 p.27).

> [!tip] Calculator
> Implied $\pi_{t,1}$ from a one-year zero at 95.92, $l = 1.25\%$, $\theta = 2.5\%$: `100 / 95.92 = - 1.0375 =` gives 0.00504, or 0.504%.

**T-bill pricing (Equation 11)** (V9 p.27)
$$
P_t^i = \frac{CF^i_{t+s}}{\left(1 + l_{t,s} + \theta_{t,s}\right)^s}
$$
^f-09-01-10

- One payment, horizon so short that $\pi_{t,s} \approx 0$: the near-certain real payoff makes a T-bill a good hedge, so no premium is demanded (V9 p.27, p.33).
- T-bill yields therefore track short-term real rates, near-term inflation expectations, and the policy rate (V9 p.28, p.29).

**Taylor rule (Equation 12)** (V9 p.30)
$$
pr_t = l_t + \iota_t + 0.5\left(\iota_t - \iota_t^*\right) + 0.5\left(Y_t - Y_t^*\right) = l_t + 1.5\,\iota_t - 0.5\,\iota_t^* + 0.5\left(Y_t - Y_t^*\right)
$$
^f-09-01-11

- $pr_t$: policy rate; $l_t$: equilibrium real short rate; $\iota_t$: inflation; $\iota_t^*$: target inflation; $Y_t - Y_t^*$: output gap in percent (log actual minus log potential GDP).
- The effective inflation weight is 1.5 because inflation appears twice; with inflation on target and a zero gap, $pr_t = l_t + \iota_t^*$, the neutral rate (V9 p.30).
- Text check: $l = 2.0\%$, $\iota = 3.0\%$, $\iota^* = 2.0\%$, gap $= 2.0\%$ gives $2.0 + 3.0 + 0.5(1.0) + 0.5(2.0) = 6.5\%$ (Python confirms 6.5) (V9 p.30).

> [!tip] Calculator
> `2 + 3 + 0.5 x 1 + 0.5 x 2 =` on the second form: `2 + 1.5 x 3 = - 0.5 x 2 = + 0.5 x 2 =` also 6.5.

**Break-even inflation rate** (V9 p.33)
$$
BEI_{t,s} = y^{nominal}_{t,s} - y^{real}_{t,s} = \theta_{t,s} + \pi_{t,s}
$$
^f-09-01-12

- Nominal minus real default-free yield at the same maturity; embeds expected inflation plus the inflation-uncertainty premium, so it is not a pure market inflation forecast (V9 p.33, p.35).
- With $\pi_{t,s} > 0$, expected inflation is below the observed BEI; if $\theta$ rises while $\pi$ falls, the direction of BEI is indeterminate (V9 p.33, p.87 solution 13).

**Credit-risky bond pricing (Equation 13)** (V9 p.49)
$$
P_t^i = \sum_{s=1}^{N} \frac{E_t\!\left[\widetilde{CF}^{\,i}_{t+s}\right]}{\left(1 + l_{t,s} + \theta_{t,s} + \pi_{t,s} + \gamma^i_{t,s}\right)^s}
$$
^f-09-01-13

- $\gamma^i_{t,s}$: credit premium, distinct from $\pi_{t,s}$; the cash flow schedule is known but payment is uncertain, and recovery in default is unknown (V9 p.49).
- The measured credit spread (corporate minus same-currency, same-maturity government yield) is conceptually akin but not equal to $\gamma^i_{t,s}$ (V9 p.50, p.77).

> [!tip] Calculator
> Implied $\gamma$ from a one-year corporate at 94.21, $l = 1.25\%$, $\theta = 2.5\%$, $\pi = 0.50\%$: `100 / 94.21 = - 1.0425 =` gives 0.0190, or 1.90%.

**Expected loss (Equation 14)** (V9 p.51)
$$
\text{Expected loss} = \text{Probability of default} \times \left(1 - \text{Recovery rate}\right)
$$
^f-09-01-14

- A risk-neutral investor would demand only this; risk-averse investors demand more because defaults cluster in downturns and the residual risk cannot be diversified away (V9 p.51).
- Recovery rates rank senior secured above senior unsecured above subordinated, and all are procyclical, so loss rates are countercyclical (V9 p.53).

**Equity pricing relative to credit-risky debt (Equation 15)** (V9 p.60)
$$
P_t^i = \sum_{s=1}^{\infty} \frac{E_t\!\left[\widetilde{CF}^{\,i}_{t+s}\right]}{\left(1 + l_{t,s} + \theta_{t,s} + \pi_{t,s} + \gamma^i_{t,s} + \kappa^i_{t,s}\right)^s}
$$
^f-09-01-15

- No maturity: dividends run to perpetuity; $\kappa^i_{t,s}$ is the extra premium over the same issuer's debt because equity gets the residual cash flow and loses everything in bankruptcy while bondholders recover something (V9 p.60).

**Equity risk premium form (Equation 16)** (V9 p.60)
$$
P_t^i = \sum_{s=1}^{\infty} \frac{E_t\!\left[\widetilde{CF}^{\,i}_{t+s}\right]}{\left(1 + l_{t,s} + \theta_{t,s} + \pi_{t,s} + \lambda^i_{t,s}\right)^s}, \qquad \lambda^i_{t,s} = \gamma^i_{t,s} + \kappa^i_{t,s}
$$
^f-09-01-16

- $\lambda^i_{t,s}$: the equity risk premium as usually quoted, the required addition over a long-dated plain-vanilla default-free bond of the same currency (V9 p.60).
- Ex post 1900-2017: 2.2% (Switzerland) to 5.1% (Australia), US 4.5%, world 3.2%; a 3% to 5% ex ante range is the curriculum's takeaway (V9 p.66, p.67).

**Commercial real estate pricing (Equation 17)** (V9 p.71)
$$
P_t^i = \sum_{s=1}^{N} \frac{E_t\!\left(\widetilde{CF}^{\,i}_{t+s}\right)}{\left(1 + l_{t,s} + \theta_{t,s} + \pi_{t,s} + \gamma^i_{t,s} + \kappa^i_{t,s} + \phi^i_{t,s}\right)^s}
$$
^f-09-01-17

- $\gamma^i_{t,s}$: tenant credit risk on the rent; $\kappa^i_{t,s}$: equity-like uncertainty about the property's end-of-lease value; $\phi^i_{t,s}$: liquidity premium, because a sale can take months or years and illiquidity destroys hedging value in bad times (V9 p.71, p.72).
- Relative sizes depend on lease length, tenant quality, and location (V9 p.72).

> [!tip] Calculator
> Example 17's value: `N=10, I/Y=7.25, PMT=500000, FV=10000000, CPT PV` gives $-8{,}437{,}796$.

Discount-rate decomposition by asset class (V9 p.5, p.27, p.49, p.60, p.71, p.72):

| Asset class | Discount rate components | Cash flow certainty |
| --- | --- | --- |
| Real default-free bond (index-linked government) | $l_{t,s}$ | Certain in real terms |
| Nominal default-free bond | $l_{t,s} + \theta_{t,s} + \pi_{t,s}$ | Certain in nominal terms only |
| T-bill (very short nominal) | $l_{t,s} + \theta_{t,s}$ ($\pi \approx 0$) | Certain, near-certain real value |
| Corporate (credit-risky) bond | $l_{t,s} + \theta_{t,s} + \pi_{t,s} + \gamma^i_{t,s}$ | Schedule known, payment uncertain |
| Equity | $l_{t,s} + \theta_{t,s} + \pi_{t,s} + \gamma^i_{t,s} + \kappa^i_{t,s}$ (i.e. $+ \lambda^i_{t,s}$) | Size and timing uncertain, perpetual |
| Commercial real estate, government tenant, indexed rent | $l_{t,s} + \kappa^i_{t,s} + \phi^i_{t,s}$ | Rent real and default-free, resale uncertain |
| Commercial real estate, government tenant, fixed rent | $l_{t,s} + \theta_{t,s} + \pi_{t,s} + \kappa^i_{t,s} + \phi^i_{t,s}$ | Rent nominal and default-free |
| Commercial real estate, corporate tenant, fixed rent | $l_{t,s} + \theta_{t,s} + \pi_{t,s} + \gamma^i_{t,s} + \kappa^i_{t,s} + \phi^i_{t,s}$ | Rent nominal with tenant credit risk |

## Worked examples

**Example 1: the inter-temporal rate of substitution (1 of 3)** (V9 p.9, p.10)
The investor's willingness to trade present for future consumption is $\tilde m_{t,1} = e^{a + b\tilde z}$, with $\tilde z$ a zero-mean economic shock taking a negative value (bad state, probability 0.4) or a positive value (good state, probability 0.6); $a$ and $b$ are negative under standard risk-aversion assumptions.
The state prices consistent with the 1999-2014 US yield curve are 0.954676 (bad state) and 0.954379 (good state).
$E_t(\tilde m_{t,1}) = 0.4 \times 0.954676 + 0.6 \times 0.954379 = 0.954498$ (Python confirms 0.954498).
The bond promising $1 in one year is worth $0.954498 today; note the $1 is worth more in the bad state, where consumption is scarce and marginal utility high. ^ex-09-01-1

**Example 2: the inter-temporal rate of substitution (2 of 3)** (V9 p.11)
The market price of the bond is $9,540 per $10,000 of face, but the investor's expected inter-temporal rate of substitution is $0.954498 per $1, i.e. $9,544.98.
She values the guaranteed $10,000 more than the market does, so she buys; buying raises her future income, lowers its marginal utility, and lowers her willingness to invest.
Only if many investors share the $9,544.98 valuation does the demand pressure lift the market price until every participant's marginal willingness equals the price, which is the equilibrium of Equation 3. ^ex-09-01-2

**Example 3: the inter-temporal rate of substitution (3 of 3)** (V9 p.11)
With $P_{t,1} = 0.954498$, the one-period real risk-free rate is $l_{t,1} = (1 - 0.954498)/0.954498 = 0.047671$, or 4.7671% (Python confirms 0.047671).
Equivalently $1/0.954498 - 1 = 4.7671\%$: the real rate is the reciprocal of the expected inter-temporal rate of substitution minus one. ^ex-09-01-3

**Example 4: the case of increasing wealth** (V9 p.12)
Add 0.1 to $\tilde z$ in both states, making the investor wealthier; the state prices fall to 0.954528 (bad) and 0.954231 (good).
$E_t(\tilde m_{t,1}) = 0.4 \times 0.954528 + 0.6 \times 0.954231 = 0.954350$ (Python confirms 0.954350).
The expected inter-temporal rate of substitution is lower by $0.954498 - 0.954350 = 0.000148$ (Python confirms), so the wealthier investor buys the safe bond only at a lower price and substitutes toward risky assets.
This is decreasing absolute risk aversion: with fundamental needs met, the wealthy demand a smaller premium per unit of risk than the poor. ^ex-09-01-4

**Example 5: pricing a two-period default-free bond** (V9 p.13, p.14)
The Time 1 price of the two-year bond is $\tilde P_{t+1,2-1} = e^{a' + b'\tilde z}$: 0.839181 in the bad state (probability 0.4) and 0.954840 in the good state (probability 0.6).
Expected Time 1 price: $0.4 \times 0.839181 + 0.6 \times 0.954840 = 0.908576$ (Python confirms).
Risk-neutral value: $0.908576 / 1.047671 = 0.867234$ (Python confirms), discounting at Example 3's 4.7671%.
Actual price from Equation 5: $0.4 \times 0.839181 \times 0.954676 + 0.6 \times 0.954840 \times 0.954379 = 0.867226$ (Python confirms).
The market price is below the risk-neutral value by $0.867234 - 0.867226 = 0.000008$ per 1 of principal (Python: 0.0000082, matching the printed 0.000008 after rounding), because $E_t(\tilde P)E_t(\tilde m) = 0.908576 \times 0.954498 = 0.867234 > E_t(\tilde P \tilde m)$.
Price uncertainty at Time 1 creates a risk premium even though the bond is default free. ^ex-09-01-5

**Example 6: an alternative method to evaluate the price discount for risk** (V9 p.15, p.16)
Covariance directly: $\mathrm{cov}_t(\tilde m_{t,1}, \tilde P_{t+1,2-1}) = 0.4(0.954676 - 0.954498)(0.839181 - 0.908576) + 0.6(0.954379 - 0.954498)(0.954840 - 0.908576) = -0.000008$ (Python: $-0.0000082$).
In the bad state the willingness to invest is above average while the bond price is below average, and vice versa, so the covariance is negative and the bond is an inferior hedge, priced 0.000008 below its risk-neutral value.
Holding-period return (Equation 7): $(0.908576 - 0.867226)/0.867226 = 0.047681$, or 4.7681% (Python confirms), so the risk premium is $\rho^i_{t,s} = 0.047681 - 0.047671 = 0.00001$ (Python confirms).
Equation 8 cross-check: $-(1.047671/0.867226) \times (-0.000008) = 0.00001$ (Python: 0.0000099, confirming the printed 0.00001). ^ex-09-01-6

**Example 7: the effect of volatility on prices** (V9 p.17, p.18)
Double the standard deviation of $\tilde z$; the one-period state prices spread to 0.954855 (bad) and 0.954260 (good) but the mean is unchanged: $0.4 \times 0.954855 + 0.6 \times 0.954260 = 0.954498$ (Python confirms).
The two-period Time 1 prices spread to 0.776625 and 1.005451, so $E_t(\tilde P_{t+1,2-1}) = 0.4 \times 0.776625 + 0.6 \times 1.005451 = 0.913921$ (Python confirms; the good-state price above 1 implies a slightly unrealistic negative yield).
Price: $0.4 \times 0.776625 \times 0.954855 + 0.6 \times 1.005451 \times 0.954260 = 0.872303$ (Python confirms).
Risk-neutral value: $0.913921 / 1.047671 = 0.872336$ (Python: 0.872335, a last-digit rounding difference), so $\mathrm{cov} = 0.872303 - 0.872336 = -0.000033$ (Python confirms).
The one-year holding-period return rises to $(0.913921 - 0.872303)/0.872303 = 4.771\%$ versus 4.768% in Example 6 (Python confirms 4.771%): more volatility, bigger negative covariance, bigger required premium.
Practical implications: real rates are higher where trend growth is higher, and higher where growth is more volatile (V9 p.18). ^ex-09-01-7

**Example 8: the present value model and macroeconomic factors (knowledge check)** (V9 p.18, p.19, p.20)
Q1: an asset's risk premium is high when there is a negative relationship between its future payoff and investors' marginal utility from future consumption; answer C.
Zero covariance means risk free, positive covariance means the asset is a hedge and returns less than the risk-free rate (V9 p.19).
Q2: the real risk-free rate is positively related to real GDP growth (C): higher future income reduces the need to save, so a higher rate is needed to induce saving (V9 p.19).
Q3: the real risk-free rate is positively related to the volatility of real GDP growth (C): more income risk makes risk-averse investors demand more compensation (V9 p.19).
Q4: an asset paying high returns in downturns can require less than the nominal risk-free rate (A, yes): its covariance term is positive, so its premium is negative (V9 p.19, p.20).
Q5: above-trend real GDP growth has an ambiguous effect on overall equity values: expected earnings (numerator) rise, but the real rate (denominator) rises too, and the given information cannot say which dominates (V9 p.20). ^ex-09-01-8

**Example 9: the evolution of real yields** (V9 p.22, p.23, p.24)
UK index-linked gilt real yields (the oldest index-linked market, first issue 1981) trended down from 1985 to 2007 while average real growth barely moved (2.8% for 1985-1999 versus 2.7% for 2000-2007), so growth expectations cannot explain the fall.
UK and OECD GDP-growth volatility fell sharply from the mid-1990s (the "great moderation"), and that volatility decline is the plausible driver of the falling real default-free rate.
The mechanism is Idea 2 in reverse: less income uncertainty means less precautionary demand for compensation, so the equilibrium real yield falls; the same force plausibly lowered conventional bond yields elsewhere (V9 p.24). ^ex-09-01-9

**Example 10: post-global financial crisis, 2008-2011 real default-free yields** (V9 p.24, p.25)
By December 2011 short-dated real yields had fallen below pre-crisis levels everywhere, and UK and US short real yields were negative, with most TIPS and all index-linked gilts negative across the curve.
Volatility had risen, which alone should have raised real yields; the resolution is that expected future growth fell further, dragging the equilibrium real yield down.
Two amplifiers: fear of future inflation (post quantitative easing) raised demand for inflation protection, and index-linked bonds are special and scarce, so safe-haven demand in a crisis can push their yields down and even negative (V9 p.25, p.26). ^ex-09-01-10

**Example 11: the risk premium for inflation uncertainty** (V9 p.27)
A one-year default-free bond with face 100 trades at 95.92; the real risk-free rate is 1.25% and expected inflation 2.5%.
Implied premium: $\pi_{t,s} = 100/95.92 - (1 + 0.0125 + 0.025) = 1.042535 - 1.0375 = 0.504\%$ (Python: 0.5035%, matching the printed 0.504%).
The bond's total yield of 4.2535% decomposes as real rate 1.25% plus expected inflation 2.50% plus inflation-uncertainty premium 0.50%. ^ex-09-01-11

**Example 12: level, slope, and curvature of the yield curve** (V9 p.38, p.39, p.40)
Principal components analysis of the US and UK curves (3 months to 10 years, January 1999 to January 2014) attributes 92.7% (US) and 95.2% (UK) of curve movement to level, 6.9% and 4.5% to slope, and 0.3% each to curvature.
Level is driven by economic activity and inflation views; slope reflects the bond risk premium plus the policy cycle, since short rates are cut in recessions while long rates anticipate normalization, so the slope increases during recession.
If investors expect policy and short risk-free rates to normalize as recession recedes, the curve steepens at the short end and flattens at the long end, so curvature can rise too; the three factors are information for central banks and investors alike (V9 p.40). ^ex-09-01-12

**Example 13: interest rates, the yield curve, and the business cycle (knowledge check)** (V9 p.42, p.43)
Q1: the instrument for studying real rates and the cycle is the default-free inflation-indexed bond (C), whose payments adjust with prices (V9 p.42).
Q2: an unanticipated rise in real GDP growth and volatility raises the real rate, so the coupon payments of an inflation-indexed bond (a function of the indexed principal and real coupon terms) would rise (A) (V9 p.42).
Q3: the spread between non-inflation-adjusted and inflation-indexed bonds reflects both inflation expectations and an inflation-uncertainty premium (C), the BEI decomposition (V9 p.42).
Q4: inverted curves predict recessions because late-cycle expansions carry peak inflation and high short rates while long yields embed expected disinflation and slackening credit demand, flattening or inverting the curve (V9 p.43). ^ex-09-01-13

**Example 14: the Japanese yield curve and business cycle, 1990-2018** (V9 p.47, p.48)
Real Japanese GDP growth averaged above 4.60% in the 1980s and about 1.5% in the 1990s and 2000s after the property and stock collapse; real short policy rates fell from 4%-5% in 1990 to negative by 1997.
As the Bank of Japan cut its policy rate from just over 8.0% (end-1990) to 0.45% (end-1995), the term spread steepened from $-1.63\%$ to $+2.59\%$ (Python: the change is $2.59 - (-1.63) = 4.22$ points of steepening), the market signaling belief that stimulus would restore growth and inflation.
Since the mid-1990s, despite zero rates and quantitative easing, the spread has fallen steadily to virtually 0.00% by end-2018: persistent weak growth and inflation flatten the curve, the LOS d mechanism running in slow motion for three decades (V9 p.48). ^ex-09-01-14

**Example 15: the credit risk premium** (V9 p.49, p.50)
A one-year corporate bond with face 100 trades at 94.21; the real risk-free rate is 1.25%, expected inflation 2.5%, and the inflation-uncertainty premium 0.50%.
Implied credit premium: $\gamma^i_{t,s} = 100/94.21 - (1 + 0.0125 + 0.025 + 0.005) = 1.061458 - 1.0425 = 1.90\%$ (Python: 1.8958%, matching the printed 1.90%).
The full yield build-up is real rate plus expected inflation plus inflation-uncertainty premium plus credit premium, the Equation 13 denominator in action. ^ex-09-01-15

**Example 16: the credit premium for the Royal Bank of Scotland** (V9 p.58, p.59)
The five-year CDS premium on RBS senior unsecured debt (a close proxy for its credit spread) surged in the crisis as perceived default risk rose, in step with the index spreads of Exhibits 15 and 17 and the sovereign repricing of Exhibit 19.
For scale, insuring EUR 10 million of German, Italian, Irish, and Spanish sovereign debt cost EUR 1,800, 8,800, 2,500, and 2,800 per year in January 2006 (1.8, 8.8, 2.5, 2.8 bps) and EUR 59,830, 306,860, 825,390, and 300,610 by August 2011 (Python: 59.83, 306.86, 825.39, 300.61 bps).
The RBS premium eventually declined because the UK government nationalized the bank, transferring the credit risk to the sovereign balance sheet (V9 p.58). ^ex-09-01-16

**Example 17: a real estate investment decision** (V9 p.72, p.73)
Inputs: real risk-free rate 1.25%, expected inflation 2.5%, inflation-uncertainty premium 0.50%; the tenant's (Supermarket plc) 10-year senior unsecured bond yields 5.75%, implying a 1.50% credit spread.
The investor requires a 0.50% property risk premium (end-value and rental uncertainty, the $\kappa$ piece) plus a 1.0% liquidity premium ($\phi$), so the required return is $5.75\% + 0.5\% + 1.0\% = 7.25\%$.
Cash flows: rent of $500,000 in arrears for years 1-10 plus estimated resale of $10 million at year 10.
Present values at 7.25% (Python confirms every row): 466,200; 434,686; 405,301; 377,903; 352,357; 328,538; 306,330; 285,622; 266,314; then year 10 is $10{,}500{,}000/1.0725^{10} = 5{,}214{,}543$.
Implied property value: $8,437,796 (Python: 8,437,796).
The asking price is $8.2 million, below the implied value, so the purchase clears the 7.25% hurdle and the analyst should recommend it. ^ex-09-01-17

**Example 18: valuation and the business cycle** (V9 p.76)
How does real estate valuation differ from public equity valuation?
Real estate does not trade in public markets (REITs are the exception), so its valuation must reflect a discount for the relative lack of liquidity, the $\phi^i_{t,s}$ term that public equities do not carry. ^ex-09-01-18

## Item-set patterns

> [!warning] Trap 1: good news that makes prices fall
> The vignette reports a strong data release and a falling market, then asks for the explanation.
> Correct: prices embed anticipated information, so only the surprise matters; if expectations were for even better data, the release is bad news relative to the price (V9 p.7).
> Distractors blame irrationality or claim the pricing model fails; both ignore that expectations, not levels, drive valuation (V9 p.6, p.7).

> [!warning] Trap 2: the sign of the hedge
> An asset is described as paying off well during downturns, and the question asks about its required return or premium.
> Correct: payoff high when marginal utility is high means positive covariance with $\tilde m$, a negative risk premium, and a required return that can sit below the risk-free rate (V9 p.17, p.20).
> Distractors assert every risky asset must earn more than the risk-free rate, or flip the covariance sign; remember risk premium sign follows minus the covariance (V9 p.16).

> [!warning] Trap 3: ranking real rates from nominal data
> A table gives nominal GDP growth, inflation, and growth volatility for several countries and asks where real short rates are highest.
> Correct: subtract inflation to get real growth first, then rank on real growth and volatility together, both positively related to the real rate (V9 p.17, p.18; Practice Problem 4).
> Distractors reward ranking on raw nominal growth (Country 1 style) or ignoring volatility entirely (V9 p.86).

> [!warning] Trap 4: which premiums to subtract from the implied yield
> A one-year zero's price is given with a menu of rates, and the implied premium is requested.
> Correct: compute $100/P - 1$ and subtract exactly the components below the premium you want: $l + \theta$ for $\pi$ (government bond), $l + \theta + \pi$ for $\gamma$ (corporate) (V9 p.27, p.50).
> Distractors are the values you get by omitting one component or by reporting the whole yield; on Practice Problem 18, 10% (yield) and 10% less $l + \theta$ both appear as wrong options (V9 p.88).

> [!warning] Trap 5: break-even inflation as a forecast
> The vignette gives a BEI spread and asks what inflation the market "expects", or moves $\theta$ and $\pi$ in opposite directions.
> Correct: $BEI = \theta + \pi$, so expected inflation is below BEI whenever $\pi > 0$, and opposite-direction moves make the BEI change indeterminate (V9 p.33; Practice Problems 5 and 13).
> Distractors equate BEI with expected inflation or claim the components always move together (V9 p.86, p.87).

> [!warning] Trap 6: what the curve does in a recession
> A recession is forecast and the question asks for the yield curve response.
> Correct: the policy rate is cut hard, long yields fall less because normalization is expected, so the curve steepens (upward slope from flat); inversion belongs to the late expansion that precedes recession, not to the recession itself (V9 p.40, p.42).
> Distractors offer "inverts" (confusing the predictor with the response) or "flattens" (the late-cycle move) (V9 p.87).

> [!warning] Trap 7: slope says nothing definitive about rate expectations
> An upward-sloping default-free curve is observed and a statement about expected future rates is requested.
> Correct: the slope mixes expectations with maturity-increasing bond risk premiums, so expectations are indeterminate; the curve can slope up even with expected cuts if premiums more than offset them (V9 p.46).
> Distractors state rates "must" be expected to rise, or premiums "must" rise; a downward slope is the one shape that mostly pins expectations (declining rates) (V9 p.46, p.88).

> [!warning] Trap 8: quality rotation over the credit cycle
> Spreads are described as narrowing (or a recession as arriving) and the outperformer among rating buckets is requested.
> Correct: narrowing spreads favor lower-rated bonds (investors stop discriminating and weak credits improve fastest); a downturn favors higher-rated bonds as the quality spread widens; cyclical sector plus low rating widens most (V9 p.54, p.59; Practice Problems 8, 20, 22).
> Distractors reverse the rotation or claim government bonds outperform while spreads narrow (V9 p.88, p.89).

> [!warning] Trap 9: commercial real estate's stable income
> A statement notes that commercial property rental income barely moves over the cycle and invites a low, bond-like discount rate.
> Correct: income is stable (UK rental growth averaged 6.5% nominal over 30 years) but capital values are strongly procyclical, so the asset hedges badly and the premium sits near the equity premium plus a liquidity premium (V9 p.73, p.74, p.75).
> Distractors call real estate a good consumption hedge or make liquidity the only difference from bonds rather than from equities (Practice Problem 28 keys the equity-versus-real-estate difference to liquidity) (V9 p.89).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM01-Economics-and-Investment-Markets-Practice-Problems]]

## Cross-links

- [[LM01-The-Term-Structure-and-Interest-Rate-Dynamics]]: the Fixed Income treatment of the same curve, where this module's expectations-plus-premium story of the slope becomes spot, forward, and swap machinery and the term premium reappears in the liquidity preference and preferred habitat theories.
- [[LM02-Economic-Growth]]: supplies the growth-accounting and convergence logic behind LOS c, since trend GDP growth and its volatility are exactly what set the average real short rate here.
- [[LM02-Discounted-Dividend-Valuation]]: applies this module's Equation 15 and 16 machinery to actual equity valuation, with the required return built from the same risk-free rate plus equity risk premium and the P/E drivers reappearing in justified multiples.
- [[LM02-Analysis-of-Active-Portfolio-Management]]: consumes the premiums built here as the passive baseline; active value added is measured against benchmarks whose expected returns are exactly these premium stacks.
- [[LM04-Using-Multifactor-Models]]: generalizes the single stochastic discount factor into multiple priced risk factors, so this module's covariance-with-bad-times premium becomes factor sensitivities times factor risk premiums.
- [[LM05-Measuring-and-Managing-Market-Risk]]: the risk decomposition here (rates, inflation, credit, equity, liquidity) is the same map a risk manager stresses; spread widening in downturns and illiquidity in crises drive the scenario design.

## Self-test

Vignette A for Q1 to Q4: Mara Voss models a representative investor whose inter-temporal rate of substitution takes the value 0.9560 in a bad state (probability 0.35) and 0.9500 in a good state (probability 0.65).
She also observes a one-year default-free nominal government zero (face 100) priced at 97.15, estimates the one-year real risk-free rate at 1.00% and expected inflation at 1.60%, and observes a one-year corporate zero (face 100) priced at 92.80 in a market where the real rate is 1.50%, expected inflation 2.00%, and the inflation-uncertainty premium 0.40%.

> [!question] Q1
> The one-period real risk-free rate implied by Voss's model is closest to:
> A. 4.60%.
> B. 5.03%.
> C. 5.26%.

> [!question] Q2
> The implied premium for inflation uncertainty in the government zero is closest to:
> A. 0.33%.
> B. 1.93%.
> C. 2.93%.

> [!question] Q3
> The implied credit premium in the corporate zero is closest to:
> A. 3.86%.
> B. 4.26%.
> C. 7.76%.

> [!question] Q4
> Voss finds an asset whose payoff is highest in the bad state. Relative to the risk-free rate, its required return is most likely:
> A. higher, because all risky assets must offer a positive premium.
> B. lower, because its payoff covaries positively with the inter-temporal rate of substitution.
> C. equal, because expected payoffs are unchanged across states.

Vignette B for Q5 to Q7: an economist applies the Taylor rule to an economy with an equilibrium real short rate of 1.5%, inflation of 4.0%, an inflation target of 2.0%, and an output gap of $-1.0\%$; the current policy rate is 4.5% and the yield curve is flat.
She expects the economy to enter a recession within two quarters.
The 10-year break-even inflation rate is 2.4%; she expects 10-year inflation expectations to rise by 0.3% and the inflation-uncertainty premium to fall by 0.5%.

> [!question] Q5
> The Taylor rule policy rate is closest to:
> A. 3.5%.
> B. 6.0%.
> C. 7.0%.

> [!question] Q6
> If the recession arrives and the central bank responds conventionally, the yield curve will most likely:
> A. invert, signaling the recession.
> B. steepen, as the short end falls more than the long end.
> C. flatten, as long yields fall to meet the policy rate.

> [!question] Q7
> Based on her expectations, the 10-year break-even inflation rate should:
> A. rise by 0.3%.
> B. fall by 0.2%.
> C. stay at 2.4%, since expectations and premiums offset by construction.

Vignette C for Q8 to Q10: a portfolio manager expects a recession and reviews three positions: an Aaa non-cyclical corporate bond, a B3 airline bond, and a commercial property let to a corporate tenant.
The property carries a 5-year lease paying 300,000 rent annually in arrears, with an estimated resale value of 5,000,000 at the end of year 5.
The tenant's bond yields 6.4%; the manager requires a 0.5% property risk premium and a 1.0% liquidity premium.
An equity strategist on the desk argues the market's equilibrium P/E has fallen.

> [!question] Q8
> Into the recession, the relative performance ranking most consistent with the credit cycle is:
> A. the B3 airline bond outperforms the Aaa non-cyclical bond.
> B. the Aaa non-cyclical bond outperforms the B3 airline bond.
> C. both perform equally, since spreads move in parallel across ratings.

> [!question] Q9
> The value of the property at the manager's required return is closest to:
> A. 4,619,691.
> B. 4,814,996.
> C. 4,916,662.

> [!question] Q10
> The change most consistent with the strategist's claim of a lower equilibrium P/E is:
> A. a decrease in the equity risk premium.
> B. a decline in uncertainty about future inflation.
> C. an increase in expected inflation.

> [!success]- Answer key
> Q1: B.
> $E(\tilde m) = 0.35 \times 0.9560 + 0.65 \times 0.9500 = 0.9521$ and $l = 1/0.9521 - 1 = 5.031\%$ (Python: 5.031%); A is the bad-state rate alone ($1/0.956 - 1 = 4.60\%$) and C the good-state rate alone ($1/0.95 - 1 = 5.26\%$), each ignoring the expectation in Equation 3 (V9 p.9, p.11).
> Q2: A.
> $\pi = 100/97.15 - (1 + 0.010 + 0.016) = 0.334\%$ (Python: 0.3336%); B forgets to subtract expected inflation (1.93%), and C is the whole yield (2.93%), the Trap 4 pattern (V9 p.27).
> Q3: A.
> $\gamma = 100/92.80 - (1 + 0.015 + 0.020 + 0.004) = 3.86\%$ (Python: 3.8586%); B omits the 0.40% inflation-uncertainty premium (4.26%), and C is the raw yield (7.76%) (V9 p.50).
> Q4: B.
> Paying off when marginal utility is high makes the covariance with $\tilde m$ positive, the risk premium negative, and the required return below the risk-free rate; A states the false universal, and C confuses expected payoff with covariance (V9 p.17, p.20).
> Q5: B.
> $pr = 1.5 + 4.0 + 0.5(4.0 - 2.0) + 0.5(-1.0) = 6.0\%$ (Python: 6.0); A is the neutral rate ($1.5 + 2.0$), C flips the sign of the output gap (7.0%) (V9 p.30).
> Q6: B.
> Policy cuts drop the short end while long yields embed normalization, so the flat curve steepens; A is the pre-recession signal, C the late-expansion move (V9 p.40, p.42).
> Q7: B.
> $\Delta BEI = \Delta\theta + \Delta\pi = +0.3\% - 0.5\% = -0.2\%$ (Python: $-0.2$); A counts only the expectations leg, and C invents an offset the decomposition does not impose (V9 p.33).
> Q8: B.
> Recession widens spreads and widens the quality spread, and the airline bond stacks cyclical sector on low rating, so the Aaa non-cyclical outperforms; A is the narrowing-regime pattern and C contradicts the sector and rating evidence (V9 p.54, p.55, p.59).
> Q9: A.
> Required return $= 6.4\% + 0.5\% + 1.0\% = 7.9\%$; $PV = \sum_{t=1}^{4} 300{,}000/1.079^t + 5{,}300{,}000/1.079^5 = 4{,}619{,}691$ (Python: 4,619,691); B omits the liquidity premium (discounting at 6.9% gives 4,814,996), C omits both property premiums (6.4% gives 4,916,662) (V9 p.71, p.72, p.73).
> Q10: C.
> Higher expected inflation raises the discount rate and lowers the equilibrium P/E; A and B both lower the discount rate and raise it, the reverse of the claim (V9 p.69).

## Flashcards

#flashcards/cfa-l2/09-Portfolio-Management/lm01

Three channels through which economic factors affect market values::Default-free interest rates across maturities, the timing or magnitude of expected cash flows, and risk premiums (V9 p.3, p.5).
General discount rate on asset i's cash flows::One plus the real default-free rate plus expected inflation plus the asset-specific risk premium (V9 p.6).
Why can prices fall on good economic news?::Prices embed anticipated information; only the surprise relative to expectations moves prices, and the news was worse than expected (V9 p.7).
How does investor sentiment affect asset values?::Directly through discount rates via higher or lower risk premiums, and possibly indirectly through future cash flows (V9 p.7).
Inter-temporal rate of substitution::Ratio of the marginal utility of consumption s periods ahead to the marginal utility of consumption today; random, also called the stochastic discount factor or pricing kernel (V9 p.8, p.9).
Price of a one-period real default-free bond::The expectation of the inter-temporal rate of substitution, P equals E(m) (V9 p.9).
One-period real risk-free rate from the bond price::{{(1 − P)/P, equivalently 1/E(m) − 1}} (V9 p.11).
In good times, is the marginal utility of current consumption high or low?::Low, because current consumption is already high; so m is low and real rates are high (V9 p.8).
Decreasing absolute risk aversion implies what about wealthy investors?::They invest larger amounts in risky assets and demand lower risk premiums, because their marginal utility loss per unit of risk is smaller (V9 p.12).
Multi-period default-free bond price (Equation 5)::P equals the expectation of the product of next period's bond price and the one-period rate of substitution (V9 p.13).
Covariance pricing decomposition (Equation 6)::Price equals expected future price discounted at the risk-free rate plus the covariance of the future price with m (V9 p.15).
Risk-neutral present value::The expected future price discounted at the risk-free rate, the asset's value if investors demanded no compensation for risk (V9 p.15).
Sign of the covariance term for most risky assets::Negative, because payoffs are high when the marginal value of consumption is low; hence lower prices and positive risk premiums (V9 p.15).
An asset that pays off in bad times has what kind of premium?::A negative risk premium, a high price, and a required return that can sit below the risk-free rate; it hedges consumption (V9 p.17).
Why does even a default-free two-period bond carry a risk premium?::Its price one period ahead is uncertain and covaries negatively with the rate of substitution (V9 p.14, p.16).
Real rate versus trend GDP growth::Positively related; more future goods reduce saving and increase borrowing, so the market-clearing real rate rises (V9 p.17).
Real rate versus GDP growth volatility::Positively related; more income risk makes risk-averse savers demand a higher real return (V9 p.17, p.18).
Why are real rates higher in developing economies?::They grow below steady state to catch up, so the marginal product of capital and trend growth are higher (V9 p.18).
Why did real yields fall after 2008 despite higher volatility?::Expected future growth fell further, and safe-haven demand for scarce index-linked bonds pushed yields down, some negative (V9 p.24, p.25).
Which single variable moves the price of a real default-free bond?::The real default-free rate; the cash flows are certain in real terms (V9 p.26).
Why is the inflation-uncertainty premium negligible for T-bills?::The three-month horizon makes the real payoff nearly certain, so the T-bill hedges bad outcomes and no premium is demanded (V9 p.27, p.33).
Taylor rule::{{pr = l + iota + 0.5(iota − iota*) + 0.5(Y − Y*)}}, equivalently l + 1.5 iota − 0.5 iota* + 0.5 gap (V9 p.30).
Neutral policy rate::The equilibrium real rate plus the targeted inflation rate; the rate that neither spurs nor impedes activity (V9 p.30).
Why is the effective Taylor weight on inflation 1.5?::Inflation appears twice, once as compensation and once in the inflation gap, and stabilizing inflation requires the larger weight (V9 p.30).
Positive output gap is associated with what?::Production beyond sustainable capacity and high or rising inflation; negative gaps come with high unemployment (V9 p.30).
Break-even inflation rate::Nominal minus real default-free yield at the same maturity, equal to expected inflation plus the inflation-uncertainty premium (V9 p.33).
Is BEI the market's inflation forecast?::No; it overstates expected inflation by the (normally positive) inflation-uncertainty premium (V9 p.33, p.35).
What happens to BEI when expected inflation rises but inflation uncertainty falls?::Indeterminate; the two components move the spread in opposite directions (V9 p.87).
Yield curve movement shares for level, slope, curvature (US)::92.7%, 6.9%, 0.3%; UK 95.2%, 4.5%, 0.3% (V9 p.39).
What does the yield curve do during a recession, and why?
?
It steepens: the central bank cuts the policy rate hard at the short end, while long yields fall less because short rates are expected back to normal as the recession recedes (V9 p.40).

Why does an inverted curve predict recession?
?
Late expansions carry peak inflation and high short rates, while long yields embed expected disinflation and slack credit demand; the inversion prices the coming downturn (V9 p.42).

Average US and UK term-spread slopes post-1945::0.50% and 0.40%, evidence of a positive bond risk premium that rises with maturity (V9 p.43).
Why does the bond risk premium rise with maturity?::Long-dated bonds are less negatively correlated with bad times, so they hedge consumption less well than short-dated bonds (V9 p.43, p.44).
What does an upward-sloping curve say about future rate expectations?::Nothing definitive; it can reflect expected hikes, flat expectations plus premiums, or expected cuts more than offset by premiums (V9 p.46).
Non-cycle forces that can distort government yield curves::Supply and demand shifts (Treasury scare 2000, Asian central bank buying) and regulation (UK pension rules inverting the long gilt end) (V9 p.46, p.47).
Credit spread::Corporate yield minus a same-currency, same-maturity government yield; compensation akin but not equal to the credit premium gamma (V9 p.50, p.77).
Expected loss formula::{{Probability of default times (1 − Recovery rate)}} (V9 p.51).
Why do credit premiums exceed expected loss?::Defaults cluster in downturns, so even a diversified portfolio keeps market risk and risk-averse investors demand extra return (V9 p.51).
Recovery rate ranking and cyclicality::Senior secured above senior unsecured above subordinated, and all recover more in expansions than contractions (V9 p.53).
Who outperforms when credit spreads narrow?::Lower-rated corporates beat higher-rated, and corporates beat governments; investors discriminate less between weak and strong credit (V9 p.54, p.89).
Who outperforms when the cycle turns down?::Higher-rated bonds, as the spread between low and high quality widens (V9 p.59).
Which spreads widen most in a downturn?::Bonds from cyclical sectors with low credit ratings; both dimensions amplify the response (V9 p.55, p.89).
Aaa versus B pre-tax interest coverage::17.6 times versus 0.9 times; coverage, cash flow to debt, and debt to capital anchor ratings (V9 p.56).
Why do sovereigns carry a credit premium despite printing power?::Governments have both printed and defaulted (Russia 1998, Argentina, Brazil, Mexico), so the premium is positive and varies with creditworthiness (V9 p.56, p.89).
What is kappa in the equity pricing equation?::The premium equity requires over the same issuer's credit-risky debt, for residual claims and total loss in bankruptcy (V9 p.60).
Equity risk premium lambda decomposition::{{lambda = gamma + kappa}}, the required addition over a long-dated default-free bond of the same currency (V9 p.60).
Ex post equity premium range 1900-2017::2.2% (Switzerland) to 5.1% (Australia); US 4.5%, world 3.2%; ex ante roughly 3% to 5% (V9 p.66, p.67).
Why is the equity premium large?::Equity payoffs are positively correlated with consumption (poor hedge), so the covariance of prices with m is strongly negative (V9 p.61, p.89).
Which earnings rebound fastest coming out of recession?::Cyclical companies, off a reduced cost base; profits can lead the economy out of recession (V9 p.62, p.89).
Five factors that can justify a higher equilibrium P/E
?
Higher expected real earnings growth, lower real rates, lower expected inflation, lower inflation uncertainty, or a lower equity risk premium (V9 p.69).

Shiller CAPE::Real price over a 10-year moving average of real earnings; peaks in 1929, 1965, 1999 preceded negative average 10-year real returns (V9 p.69).
Commercial real estate cash flow character::Part bond (contractual, sometimes indexed or upward-only rents from tenants of given credit quality) and part equity (uncertain end-of-lease property value) (V9 p.70, p.71).
Why does commercial real estate carry a liquidity premium?::Exit can take months or years with high transaction costs, so the asset cannot fund consumption in bad times (V9 p.71, p.72).
Full commercial real estate discount rate (corporate tenant, fixed rent)::l + theta + pi + gamma + kappa + phi (V9 p.72).
UK commercial property income versus capital values::Income grew a stable 6.5% nominal per year over 30 years; capital values are procyclical, down 26% in the 1990s recession (V9 p.73, p.74).
Micro-problem: one-year zero at 95.92, l 1.25%, theta 2.5%; find pi::100 / 95.92 = 1.042535, minus 1.0375 gives 0.504%; keystrokes 100 / 95.92 = - 1.0375 = (V9 p.27).
Micro-problem: corporate zero at 94.21, l 1.25%, theta 2.5%, pi 0.5%; find gamma::100 / 94.21 = 1.061458, minus 1.0425 gives 1.90%; keystrokes 100 / 94.21 = - 1.0425 = (V9 p.50).
Micro-problem: Taylor rate for l 2%, inflation 3%, target 2%, gap 2%::2 + 3 + 0.5(1) + 0.5(2) = 6.5%; keystrokes 2 + 3 + 0.5 + 1 = (V9 p.30).
Micro-problem: rent 500,000 for 10 years plus 10,000,000 resale, rate 7.25%; value?::8,437,796; keystrokes N=10, I/Y=7.25, PMT=500000, FV=10000000, CPT PV (V9 p.73).
The trap answer equal to the bond's full yield signals what error?::Reporting the yield instead of subtracting the default-free components to isolate the requested premium (V9 p.88).

## Common mistakes

1. Ranking real short rates on nominal GDP growth without subtracting inflation, and forgetting that growth volatility is a co-equal driver (V9 p.18, p.86).
2. Treating the break-even inflation rate as the market's pure inflation forecast instead of expected inflation plus a positive uncertainty premium (V9 p.33, p.86).
3. Calling the BEI direction when expected inflation and the uncertainty premium move oppositely; the correct answer is indeterminate (V9 p.87).
4. Predicting inversion during a recession; the curve steepens in recessions and the inversion happens late in the preceding expansion (V9 p.40, p.42, p.87).
5. Reading rate expectations off an upward slope; premiums make expectations indeterminate, and only a downward slope points clearly to expected declines (V9 p.46, p.88).
6. Subtracting the wrong components from an implied yield: leaving the inflation-uncertainty premium inside a "credit premium", or reporting the whole yield as the premium (V9 p.50, p.88).
7. Flipping the credit rotation: low-rated bonds outperform when spreads narrow, high-rated bonds outperform when the cycle turns down (V9 p.54, p.59, p.88).
8. Assigning the higher equity risk premium to non-cyclical companies; cyclicals hedge worse and deserve the larger premium, and their earnings are the more volatile (V9 p.64, p.89).
9. Claiming any risky asset must yield more than the risk-free rate; a bad-times payoff means positive covariance with m, a negative premium, and a lower required return (V9 p.17, p.20, p.87).
10. Saying wealth raises the marginal utility of consumption or the rate of substitution; both fall as wealth rises, which is why the wealthy demand smaller premiums (V9 p.12, p.86).
11. Calling commercial real estate a good consumption hedge because rents are stable; capital values are procyclical and the asset is illiquid exactly when cash is needed (V9 p.74, p.75, p.89).
12. Forgetting the liquidity premium when building the commercial real estate discount rate, which overstates the property's value (V9 p.72, p.73).
13. Confusing the inflation-uncertainty premium pi (applies to all nominal assets, grows with horizon) with the asset-specific credit premium gamma (V9 p.27, p.49).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "09-01" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
