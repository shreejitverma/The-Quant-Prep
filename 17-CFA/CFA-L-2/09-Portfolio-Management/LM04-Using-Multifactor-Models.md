---
type: cfa-lm
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
volume: 9
lm: 4
title: "Using Multifactor Models"
pages: "203-249"
weight_band: "10-15%"
difficulty: 3
los_count: 7
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/portfolio-management]
---

# LM4: Using Multifactor Models

Difficulty 3 of 5: the arithmetic is light (weighted averages, one subtraction per surprise, one square root), but the exam lives in the definitional seams, which model type puts what where, what the intercept means in each, which step is estimated first, and the arbitrage and active-risk questions punish anyone who cannot set up the trade or the variance decomposition from scratch.

## LOS map

- **describe** arbitrage pricing theory (APT), including its underlying assumptions and its relation to multifactor models (V9 p.203) ^los-09-04-a
    - Examiner asks: pick the statement that is NOT one of the three APT assumptions (the classic distractor asserts that arbitrage opportunities DO exist among well-diversified portfolios), or contrast APT with the CAPM on the strength of assumptions and the number and identity of factors.
- **define** arbitrage opportunity and determine whether an arbitrage opportunity exists (V9 p.203) ^los-09-04-b
    - Examiner asks: given expected returns and factor sensitivities for three or four well-diversified portfolios, build the combination that matches one portfolio's sensitivity, compare expected returns, and select the strategy (buy the cheap side, short the matched combination) that earns a riskless profit with zero net investment.
- **calculate** the expected return on an asset given an asset’s factor sensitivities and the factor risk premiums (V9 p.203) ^los-09-04-c
    - Examiner asks: solve two APT equations in two unknowns for the risk-free rate and the factor premium, then price a third portfolio; or plug surprises into a macro model, remembering the intercept is the expected return.
- **describe** and compare macroeconomic factor models, fundamental factor models, and statistical factor models (V9 p.203) ^los-09-04-d
    - Examiner asks: which model uses surprises versus returns versus extracted portfolios as factors, in which model sensitivities are specified first versus estimated last, and the half-true statement about statistical models (minimal assumptions, yes; easy interpretation, no).
- **describe** uses of multifactor models and interpret the output of analyses based on multifactor models (V9 p.203) ^los-09-04-e
    - Examiner asks: read an active return decomposition table (factor tilts versus security selection) or an active risk squared table and characterize the manager, or identify which model type suits style analysis, index replication, or rules-based factor investing.
- **describe** the potential benefits for investors in considering multiple risk dimensions when modeling asset returns (V9 p.203) ^los-09-04-f
    - Examiner asks: explain why an investor with a given income profile should tilt toward or away from a factor (comparative advantage in bearing business cycle or inflation risk), and why the multifactor view improves on the CAPM two-fund prescription.
- **explain** sources of active risk and interpret tracking risk and the information ratio (V9 p.203) ^los-09-04-g
    - Examiner asks: compute IR as mean active return over tracking error, decompose active risk squared into active factor risk and active specific risk, take the square root to recover tracking error, and state the IR of a well-run index fund (zero).

## Core intuition

The whole module rests on one idea from the CAPM era that survives every generalization: only risk that cannot be diversified away should be compensated with higher expected return (V9 p.204).
The CAPM compresses all systematic risk into one number, beta against the market portfolio, and explains differences in mean returns with that single factor (V9 p.204).
Decades of evidence say that compression loses information: small-cap, value, and momentum stocks earn returns the market factor alone cannot explain (V9 p.204, p.209).
A factor is simply a variable or characteristic with which individual asset returns are correlated, and multifactor models let several such systematic influences carry their own premium and their own sensitivity (V9 p.203).

Ross's arbitrage pricing theory supplies the equilibrium discipline (V9 p.205).
The APT makes only three assumptions: a factor model describes asset returns, investors can form well-diversified portfolios that eliminate asset-specific risk, and no arbitrage opportunities exist among well-diversified portfolios (V9 p.206).
Notice what the APT does not assume: it never specifies the identity or even the number of the factors, and it needs far weaker assumptions than the CAPM's full mean-variance apparatus (V9 p.205, p.206).
An arbitrage opportunity is an opportunity to earn an expected positive net profit without risk and with no net investment of money (V9 p.206).
If such an opportunity appears, the trade that exploits it is mechanical: buy the portfolio whose expected return is too high for its factor sensitivity, and fund the purchase by shorting a combination of other portfolios engineered to have exactly the same factor sensitivity (V9 p.208).
The combined position has zero factor risk, zero net cost, and positive expected profit, so prices must move until the profit vanishes; that price pressure is what enforces the APT equation (V9 p.209).

> [!abstract] Idea 1: matching sensitivities converts a mispricing into free money
> Any well-diversified portfolio's expected return must lie on the line (or hyperplane) defined by the risk-free rate and the factor premiums (V9 p.206).
> A portfolio off that line can be paired against a same-sensitivity combination of on-line portfolios; the sensitivity difference is zero, so the position carries no factor risk, and diversification has already killed the asset-specific risk (V9 p.208, p.209).
> Every APT arbitrage question is the same three steps: find the replicating weights, compare expected returns, buy cheap and short dear.

The APT's factor premium λ has a concrete meaning: it is the expected reward for holding a pure factor portfolio, a portfolio with sensitivity 1 to that factor and 0 to every other factor (V9 p.206).
The Carhart four-factor model is the curriculum's flagship example: the market excess return (RMRF) plus size (SMB, small minus big), value (HML, high book-to-market minus low), and momentum (WML, winners minus losers) (V9 p.209, p.210).
What the CAPM calls anomalies, the Carhart model reinterprets as systematic risk factors whose exposure the market compensates (V9 p.210).

The taxonomy of multifactor models is the most heavily tested description in the module, because the three types differ in what the factor IS, not just in what it is called (V9 p.211).
In a macroeconomic factor model, the factors are surprises in macro variables, actual value minus predicted value, such as unexpected inflation or unexpected GDP growth (V9 p.211, p.217).
Only surprises can move prices, because the predicted component is already embedded in the price and hence in the expected return; that is exactly why the intercept of a macro model is the asset's expected return (V9 p.218).
In a fundamental factor model, the factors are returns associated with attributes of stocks or companies, such as book-to-price, market cap, P/E, or financial leverage, that explain cross-sectional differences in stock prices (V9 p.211).
In a statistical factor model, statistical methods extract the factors from historical returns themselves; the factors are portfolios of the securities under study, defined by portfolio weights (V9 p.211).
Factor analysis models pick the portfolios that best reproduce historical return covariances; principal components models pick the portfolios that best reproduce historical return variances (V9 p.211).
Statistical models make minimal assumptions, which is their advantage, but the extracted factors usually have no economic name, which is why interpretation is their weakness (V9 p.211).

> [!abstract] Idea 2: the same regression equation means three different things
> The equation R_i = a_i + b_i1 F_1 + ... + b_iK F_K + e_i serves every model type, but each term changes meaning with the type (V9 p.212, p.217).
> Macro model: F is a surprise with expected value zero, b is a regression slope estimated AFTER the surprise series is built, and the intercept a is the asset's expected return (V9 p.217, p.218).
> Fundamental model: F is a factor return estimated by regression AFTER the sensitivities are specified, b is a standardized attribute of the security ((value minus mean)/standard deviation), the factors do not have zero means, and the intercept is not interpreted beyond being a regression intercept (V9 p.212).
> The order-of-estimation contrast (macro: factors first, betas second; fundamental: betas first, factor returns second) is a recurring exam question (V9 p.212).

The standardized beta deserves a moment because it is the one formula unique to fundamental models (V9 p.212).
A stock whose dividend yield sits one standard deviation above the cross-sectional average has a dividend yield sensitivity of exactly +1, whatever the units of the raw attribute, so sensitivities to earnings yield, leverage, and momentum all live on one comparable scale (V9 p.212).
Binary attributes such as industry membership escape the standardization and enter as 0/1 dummy variables (V9 p.212).
Fundamental factors sort into company fundamental factors (earnings growth, leverage), company share-related factors (price multiples, market cap, momentum, trading activity), and macroeconomic factors (industry membership, CAPM beta, yield curve sensitivity); global models often use the country, industry, and style classification (V9 p.213).
The same machinery ports to fixed income, with macro surprise models applying almost mechanically and fundamental models rebuilt on duration, credit, currency, and geography exposures, as in the Dopfel sector framework that splits the Bloomberg Barclays Aggregate into government maturity buckets, investment-grade credit, high yield, and MBS (V9 p.213, p.214).
Style factors such as value, momentum, carry, and volatility apply across asset classes, with value defined as real yield and carry as term spread for bonds (V9 p.215).

Everything after the taxonomy is application, and all of it runs through one pair of decompositions (V9 p.223).
Active return, the portfolio return minus the benchmark return, splits into the return from factor tilts (differences in factor sensitivities times factor returns) plus security selection (V9 p.224).
The decomposition is a lie detector: a self-described stock picker whose entire active return came from a value tilt, with negative security selection, was paid for a factor bet, not for picking stocks (V9 p.225, p.226).
Active risk, the standard deviation of active returns, also called tracking error or tracking risk, gets the same treatment in variance space, because variances of uncorrelated components add (V9 p.226, p.228).
Active risk squared equals active factor risk plus active specific risk, where active factor risk comes from different-from-benchmark factor exposures and active specific risk comes from different-from-benchmark holdings within factors (V9 p.228).
The information ratio, mean active return over tracking error, then measures how much the manager was paid per unit of the active risk taken (V9 p.227).

> [!abstract] Idea 3: return and risk walk through the same two doors
> A manager can differ from the benchmark in only two ways: factor exposures and individual holdings (V9 p.224, p.228).
> Return attribution prices the two doors (factor tilts versus security selection); risk attribution sizes them (active factor risk versus active specific risk) (V9 p.224, p.228).
> Interpreting the pair together answers the exam's favorite question: was the manager's realized return earned in the way the manager claims to invest?

Benchmarks for scale: a passive US equity strategy can hold tracking error near 0.10% a year, enhanced index strategies target about 2%, diversified active large-cap runs 2% to 6%, and aggressive active managers run 6% to 10% or more (V9 p.226, p.227).
Investors write these quantities into manager guidelines, for example requiring IR of at least 0.30 and tracking risk below 3% versus the S&P 500 (V9 p.227).

In construction, multifactor models serve passive management (replicating an index's factor exposures with a sampled portfolio), active management (establishing desired risk profiles around alpha forecasts), and rules-based active management, the alternative index strategies that tilt mechanically toward size, value, quality, or momentum at low cost (V9 p.231).
The building block is again the pure factor portfolio: sensitivity 1 to one factor, 0 to the rest, which a manager buys to speculate on the factor or shorts to hedge an existing exposure (V9 p.231, p.232).
The Wolfe Research case combines eight pure factor portfolios (earnings yield, book-to-market, expected EPS growth, price momentum, EPS revision, ROE, low leverage, earnings quality), formed by buying the top quintile and shorting the bottom quintile on each attribute, into equally weighted (benchmark) and risk parity multifactor portfolios; risk parity weights each factor for equal risk contribution, and its Sharpe ratio in the backtest was nearly double the equal-weight version in the United States because volatility fell more than return (V9 p.233, p.234, p.235, p.236).

Finally, factor thinking reframes strategic decisions (V9 p.236).
Each investor should ask which priced risks they have a comparative advantage in bearing: a long-horizon endowment can harvest business cycle and liquidity premiums, while an investor living on salary income should demand a large premium for procyclical assets, and a wealthy investor with no labor income can tilt toward them (V9 p.236, p.237).
That is a richer prescription than the CAPM's two-fund answer of market portfolio plus risk-free asset, and it is the economic content of LOS f (V9 p.236, p.237).

## Formulas and derivations

**Multifactor return-generating process** (V9 p.205)
$$
R_i = a_i + b_{i1} I_1 + b_{i2} I_2 + \cdots + b_{iK} I_K + \varepsilon_i
$$
^f-09-04-1

- $R_i$: return to asset $i$; $a_i$: intercept, the expected return of asset $i$ when all factors are zero; $I_k$: return to factor $k$; $b_{ik}$: sensitivity of asset $i$ to factor $k$; $\varepsilon_i$: zero-mean error, the portion of return the factors do not explain.
- This is a time-series model of realized returns; in any period the error can be non-zero, but it averages to zero (V9 p.205).
- A common variant subtracts $R_F$ from both sides so the dependent variable and the market factor are excess returns, as in the Carhart model (V9 p.205).

**APT expected return equation** (V9 p.206)
$$
E(R_p) = R_F + \lambda_1 \beta_{p,1} + \cdots + \lambda_K \beta_{p,K}
$$
^f-09-04-2

- $\lambda_j$: factor risk premium (factor price), the expected reward for bearing the risk of factor $j$; $\beta_{p,j}$: sensitivity of portfolio $p$ to factor $j$; $K$: number of factors, far fewer than the number of assets.
- Holds for well-diversified portfolios under the three APT assumptions; if no risk-free asset exists, replace $R_F$ with $\lambda_0$, the expected return on a risky portfolio with zero sensitivity to all factors (V9 p.206).
- Derivation logic: any deviation from this linear relation lets an investor construct a zero-cost, zero-factor-risk position with positive expected profit, and assumption 3 forbids that (V9 p.208, p.209).

**Factor risk premium from a pure factor portfolio** (V9 p.206, p.207)
$$
\lambda_j = E(R_j) - R_F
$$
^f-09-04-3

- $E(R_j)$: expected return on the pure factor portfolio for factor $j$, the portfolio with sensitivity 1 to factor $j$ and 0 to all others.
- Follows from formula 2 with $\beta_j = 1$ and all other betas zero: $E_1 = R_F + \lambda_1 \times 1$, so with $E_1 = 0.12$ and $R_F = 0.04$, $\lambda_1 = 0.08$ (V9 p.207).
- The interpretation of the premium depends on the model; in the Carhart model the market premium is the market return in excess of the risk-free rate, and SMB, HML, WML premiums are mean long-side returns minus mean short-side returns (V9 p.206).

**Carhart four-factor model (return-generating form)** (V9 p.209)
$$
R_p - R_F = a_p + b_{p1}\,RMRF + b_{p2}\,SMB + b_{p3}\,HML + b_{p4}\,WML + \varepsilon_p
$$
^f-09-04-4

- $RMRF$: value-weighted equity index return in excess of the one-month T-bill rate; $SMB$: average return on three small-cap portfolios minus three large-cap portfolios; $HML$: average return on two high book-to-market portfolios minus two low book-to-market portfolios; $WML$: past-year winners minus losers; $a_p$: alpha, return beyond that expected for the portfolio's systematic risk (V9 p.209, p.210).
- The model extends Fama-French three-factor with momentum; the CAPM's size, value, and momentum anomalies become priced systematic factors (V9 p.209, p.210).

**Carhart equilibrium expected return** (V9 p.210)
$$
E(R_p) = R_F + \beta_{p,1}\,RMRF + \beta_{p,2}\,SMB + \beta_{p,3}\,HML + \beta_{p,4}\,WML
$$
^f-09-04-5

- The expected value of alpha is zero in equilibrium, so dropping $a_p$ and $\varepsilon_p$ from formula 4 gives the expected-return form, the Carhart instance of the APT equation (V9 p.210).

**Standardized beta (fundamental factor sensitivity)** (V9 p.212)
$$
b_{ik} = \frac{\text{Value of attribute } k \text{ for asset } i - \text{Average value of attribute } k}{\sigma(\text{Values of attribute } k)}
$$
^f-09-04-6

- Cross-sectional standardization: a stock at the average attribute value has sensitivity 0; one standard deviation above gives +1, one below gives -1.
- Example: dividend yield 3.5%, average 2.5%, standard deviation 2% gives $b = (3.5 - 2.5)/2 = 0.50$ (V9 p.212).
- The scaling makes sensitivities comparable across attributes with different units; binary variables such as industry membership stay as 0/1 dummies (V9 p.212).

**Macroeconomic factor model with surprise factors** (V9 p.217, p.218)
$$
R_i = a_i + b_{i1} F_1 + \cdots + b_{iK} F_K + \varepsilon_i, \qquad F_k = \text{Actual}_k - \text{Predicted}_k
$$
^f-09-04-7

- $F_k$: the surprise in factor $k$, with expected value zero; $a_i$: the expected return to asset $i$; $b_{ik}$: response of return to a one-unit surprise in factor $k$, holding other factors constant; $\varepsilon_i$: asset-specific return, e.g. from a company-specific event (V9 p.217, p.218, p.219).
- Predicted values are excluded because they are already in prices and hence in $a_i$; the model splits return into expected return, factor-surprise return, and asset-specific return (V9 p.218).
- Sign conventions to memorize: the GDP growth premium is typically positive, and the inflation premium is typically negative, because positive inflation sensitivity is an inflation hedge that investors accept lower return to hold (V9 p.219).
- Portfolio parameters are market-value-weighted averages of asset parameters (V9 p.219).

**Fixed-income fundamental (style) factor model** (V9 p.215)
$$
R_i = a_i + b_{i1} F_{Gvt\_Sh} + b_{i2} F_{Gvt\_Int} + b_{i3} F_{Gvt\_Lg} + b_{i4} F_{Invest} + b_{i5} F_{HiYld} + b_{i6} F_{MBS} + \varepsilon_i
$$
^f-09-04-8

- Factors are sector returns from the Dopfel decomposition of the Bloomberg Barclays Aggregate (government short, intermediate, long, investment-grade credit, high yield, MBS) (V9 p.214, p.215).
- The style weights $b_{ik}$ come from a constrained regression with the weights summing to 100%, which is what makes the output read as a sector allocation (V9 p.215).
- Extends to ESG scores and forward-looking construction via a quantitative objective function (V9 p.215).

**Active return** (V9 p.224)
$$
\text{Active return} = R_p - R_B
$$
^f-09-04-9

- $R_p$: portfolio return; $R_B$: benchmark return; positive active return is the entire objective of holding different-from-benchmark weights (V9 p.224).

**Active return decomposition** (V9 p.224)
$$
\text{Active return} = \sum_{k=1}^{K} \left[(\text{Portfolio sensitivity})_k - (\text{Benchmark sensitivity})_k\right] \times (\text{Factor return})_k + \text{Security selection}
$$
^f-09-04-10

- The first term is the return from factor tilts; the second is security selection, the part of active return from overweighting outperformers and underweighting underperformers (V9 p.224).
- Sensitivities are measured as of the beginning of the evaluation period (V9 p.224).
- Security selection is found as the residual: active return minus the summed tilt contributions.

**Tracking error (active risk) and annualization** (V9 p.226)
$$
TE = s(R_p - R_B), \qquad TE_{ann} = TE_{daily}\sqrt{250} = TE_{monthly}\sqrt{12}
$$
^f-09-04-11

- $s(\cdot)$: sample standard deviation of the time series of active returns; tracking risk is the curriculum's synonym (V9 p.226).
- The square-root annualization assumes serially uncorrelated returns and 250 trading days (V9 p.226).
- Scale anchors: passive about 0.10%, enhanced index about 2%, diversified active large-cap 2% to 6%, aggressive active 6% to 10% or more (V9 p.226, p.227).

**Information ratio** (V9 p.227)
$$
IR = \frac{\bar{R}_p - \bar{R}_B}{s(R_p - R_B)}
$$
^f-09-04-12

- Numerator: sample mean active return; denominator: tracking error; both must be on the same time basis (V9 p.227).
- Measures mean active return per unit of active risk, the active-management analog of the Sharpe ratio; it assumes the portfolio has the same systematic risk as its benchmark (V9 p.227).
- Example: mean portfolio return 9%, benchmark 7.5%, TE 6% gives $IR = 1.5/6 = 0.25$ (V9 p.227).

> [!tip] Calculator
> IR: `9 - 7.5 = / 6 =` gives 0.25.
> Annualize a 1.2% monthly TE: `12 sqrt(x) x 1.2 =` gives 4.16.

**Active risk squared** (V9 p.228)
$$
\text{Active risk squared} = s^2(R_p - R_B)
$$
^f-09-04-13

- The variance of active return; variances are used because variances of uncorrelated components are additive, which standard deviations are not (V9 p.228).

**Decomposition of active risk squared** (V9 p.228)
$$
\text{Active risk squared} = \text{Active factor risk} + \text{Active specific risk}
$$
^f-09-04-14

- Active factor risk: the contribution from different-from-benchmark exposures to the model's factors; found indirectly as active risk squared minus active specific risk (V9 p.228).
- Active specific risk (security selection risk): the residual, non-factor active risk, the compensation-bearing risk of security selection (V9 p.228).
- Both components are variances (units of % squared); take the square root of the total to recover tracking error (V9 p.228, p.230).

**Active specific risk** (V9 p.228)
$$
\text{Active specific risk} = \sum_{i=1}^{n} (w_i^a)^2 \, \sigma_{\varepsilon_i}^2
$$
^f-09-04-15

- $w_i^a$: active weight of asset $i$, portfolio weight minus benchmark weight; $\sigma_{\varepsilon_i}^2$: residual variance of asset $i$, the return variance the factors leave unexplained (V9 p.228).
- Squared active weights mean many small active positions produce far less specific risk than a few concentrated ones, which is why high specific risk signals a less diversified portfolio (V9 p.228, p.230).

**Active factor risk (direct form)** (V9 p.229)
$$
b_j^a = \sum_{i=1}^{n} w_i^a b_{ji}, \qquad \text{Active factor risk} = \sum_{i=1}^{K}\sum_{j=1}^{K} b_i^a b_j^a \operatorname{cov}(F_i, F_j)
$$
^f-09-04-16

- $b_j^a$: the portfolio's active exposure to factor $j$, each asset's sensitivity weighted by its active weight and summed (V9 p.229).
- The double sum is a quadratic form in the factor covariance matrix; the cross terms drop out when factor covariances are negligible, as assumed in the Example 9 exhibit (V9 p.229).

## Worked examples

**Example 1: Determining the Parameters in a One-Factor APT Model** (V9 p.207, p.208)
Three well-diversified portfolios load on one factor: A has expected return 0.075 and sensitivity 0.5, B has 0.150 and 2.0, C has 0.070 and 0.4.
Two unknowns ($R_F$ and $\lambda_1$) need two equations: $0.075 = R_F + 0.5\lambda_1$ and $0.150 = R_F + 2\lambda_1$.
Subtracting, $0.075 = 1.5\lambda_1$, so $\lambda_1 = 0.075/1.5 = 0.05$ (Python: 0.05).
Then $R_F = 0.075 - 0.5 \times 0.05 = 0.05$ (Python: 0.05), so the APT equation is $E(R_p) = 0.05 + 0.05\beta_{p,1}$.
Check with C: $E(R_C) = 0.05 + 0.05 \times 0.4 = 0.07$ (Python: 0.07), matching the exhibit, so all three portfolios sit on one pricing line and no arbitrage exists among them. ^ex-09-04-1

**Example 2: Checking Whether Portfolio Returns Are Consistent with No Arbitrage** (V9 p.208, p.209)
Portfolio D is added: expected return 0.08, sensitivity 0.45, against the model $E(R_p) = 0.05 + 0.05\beta_{p,1}$ from Example 1.
Step 1, replicate D's sensitivity: an equally weighted portfolio of A and C has sensitivity $0.5 \times 0.5 + 0.5 \times 0.4 = 0.45$ and expected return $0.5 \times 0.075 + 0.5 \times 0.07 = 0.0725$ (Python: 0.45 and 0.0725).
Step 2, price D with the APT: $E(R_D) = 0.05 + 0.05 \times 0.45 = 0.0725$ (Python: 0.0725), but D offers 0.08, so D is undervalued for its factor risk.
Step 3, construct the arbitrage: buy $10,000 of D, funded by shorting $10,000 of the 50/50 A+C portfolio, so the initial net cash flow is $0 and the net factor sensitivity is $0.45 - 0.45 = 0$.
In one year the long leg is expected to pay $10{,}000 \times 1.08 = \$10{,}800$ and the short leg costs $10{,}000 \times 1.0725 = \$10{,}725$ to close, leaving an expected profit of $10{,}800 - 10{,}725 = \$75$ with no net investment and no factor risk (Python: 10800, 10725, 75).
Asset-specific risk is negligible because the portfolios are well diversified; buying pressure on D then raises its price and lowers its expected return until the opportunity vanishes, which is how arbitrage restores equilibrium. ^ex-09-04-2

**Example 3: Calculating Factor-Based Expected Returns at the Portfolio Level** (V9 p.216)
A fixed-income portfolio has estimated exposures of 35% intermediate government, 40% investment-grade credit, 5% securitized, and 20% high yield, with expected component returns of 1.50%, 4.25%, 1.75%, and 5.75% respectively.
The portfolio expected return is the exposure-weighted average: $E(R) = 0.35 \times 1.50\% + 0.40 \times 4.25\% + 0.05 \times 1.75\% + 0.20 \times 5.75\%$.
That is $0.5250\% + 1.7000\% + 0.0875\% + 1.1500\% = 3.4625\%$ (Python: 3.4625%), which the curriculum rounds to 3.46%.
The short and long government sectors carry zero exposure, so their 0.25% and 3.00% component returns never enter the sum. ^ex-09-04-3

**Example 4: Reconciling Bond Portfolio Characteristics Using Style Factors** (V9 p.216, p.217)
A strategy marketed as intermediate-duration (5 to 7 years) investment grade shows style weights of 2% government short, 4% government intermediate, 14% government long, 56% investment-grade credit, 6% MBS/securitized, and 18% high yield.
The exposures are inconsistent with the mandate for two reasons.
First, the 18% high-yield loading is significant below-investment-grade exposure; a true investment-grade portfolio would have none.
Second, the tilt toward longer-duration sectors (14% government long against only 4% intermediate) implies a longer-than-intermediate portfolio duration.
This is the fixed-income style model doing for bonds what returns-based style analysis does for equities: catching a mandate violation from the factor loadings alone. ^ex-09-04-4

**Example 5: Estimating Returns for a Two-Stock Portfolio Given Factor Sensitivities** (V9 p.220)
Given $R_{MANM} = 0.09 - 1F_{INFL} + 1F_{GDP} + \varepsilon_{MANM}$ and $R_{NXT} = 0.12 + 2F_{INFL} + 4F_{GDP} + \varepsilon_{NXT}$, with one-third in MANM and two-thirds in NXT.
Part 1, the portfolio equation is the weighted average term by term.
Intercept: $(1/3) \times 0.09 + (2/3) \times 0.12 = 0.11$ (Python: 0.11).
Inflation sensitivity: $(1/3)(-1) + (2/3)(2) = 1$; GDP sensitivity: $(1/3)(1) + (2/3)(4) = 3$ (Python: 1.0 and 3.0).
So $R_P = 0.11 + 1F_{INFL} + 3F_{GDP} + (1/3)\varepsilon_{MANM} + (2/3)\varepsilon_{NXT}$.
Part 2, the expected return is the intercept, 11%, because surprises and errors have zero expected value.
Part 3, with $F_{INFL} = 0.01$, $F_{GDP} = 0$, and both errors at 0.005: $R_P = 0.11 + 1 \times 0.01 + 3 \times 0 + (1/3) \times 0.005 + (2/3) \times 0.005 = 0.125$, or 12.5% (Python: 0.125). ^ex-09-04-5

**Example 6: Comparing Types of Factor Models** (V9 p.221, p.222, p.223)
Connor (1995) ran a five-factor macroeconomic model and the BARRA US-E2 fundamental model on the same 779 large-cap US stocks, January 1985 to December 1993.
The macro model explained about 11% of return variance, with default premium (2.4% alone, 8.1% marginal) and term structure (1.1% alone, 7.7% marginal) the strongest factors and inflation adding nothing at the margin (V9 p.221).
The fundamental model explained about 43%, with industries (55 dummy variables) the most important factor at 16.3% alone and 18.0% marginal (V9 p.222).
Three cautions stop the naive conclusion that fundamental models are simply better.
The industries factor must sum to the market while the macro model contains no market portfolio, so part of the gap is built into the comparison; no significance tests were reported; and a macro factor's claim to represent undiversifiable systematic risk is individually backed by statistical evidence, which is not true of every fundamental factor, since a manager can simply exclude an industry (V9 p.222).
The trade-off to carry into the exam: macro models are parsimonious and map directly to economic views, while fundamental models are large (67 variables here) and give a detailed, security-characteristic picture of risk; Connor also found the macro model added no marginal explanatory power once the fundamental model was in place (V9 p.222, p.223). ^ex-09-04-6

**Example 7: Four-Factor Model Active Return Decomposition** (V9 p.224, p.225, p.226)
A self-described stock picker is benchmarked to a large-cap index; the Carhart decomposition gives portfolio sensitivities (0.95, -1.05, 0.40, 0.05), benchmark sensitivities (1.00, -1.00, 0.00, 0.03), and factor returns (5.52%, -3.35%, 5.10%, 9.63%) for RMRF, SMB, HML, WML.
Tilt contributions are difference times factor return.
RMRF: $(0.95 - 1.00) \times 5.52\% = -0.2760\%$; SMB: $(-1.05 + 1.00) \times (-3.35\%) = +0.1675\%$; HML: $0.40 \times 5.10\% = 2.0400\%$; WML: $0.02 \times 9.63\% = 0.1926\%$ (Python confirms all four).
Return from factor tilts A $= 2.1241\%$; security selection B $= -0.0500\%$; active return $= 2.0741\%$ (Python: 2.1241, 2.0741).
Proportions of active return: -13.3%, +8.1%, +98.4%, +9.3%, so tilts are 102.4% and selection -2.4% (Python confirms each proportion).
Question 1, mandate and style: the benchmark's sensitivities (RMRF 1, SMB -1, HML 0, WML 0.03) describe a large-cap mandate with no value or momentum bias; the portfolio's positive HML exposure of 0.40 with near-zero WML marks the manager as large-cap value, not momentum and probably not contrarian value.
Question 2, sources: essentially all the active return (about 98%) came from the HML tilt in a period when value paid 5.10%; the RMRF tilt lost money, the SMB and WML tilts made small profits.
Question 3, concerns: the stock picker's security selection was negative, so the discussion should demand evidence the manager can time HML returns and probe the stock selection discipline, because a growth-led market would have exposed this portfolio. ^ex-09-04-7

**Example 8: Creating Active Manager Guidelines** (V9 p.227)
A US public employee retirement system solicits a low-active-risk US large-cap equity fund with constraints: S&P 500 constituents only; at least 200 issues with the maximum per issuer the greater of 5% of portfolio value or 150% of the issuer's index weight; a minimum information ratio of 0.30 since inception or over the last seven years; and tracking risk below 3% versus the S&P 500 over the same window.
The benchmark works as a continuously observable reference standard, so quantitative risk and return objectives can be written directly into manager guidelines, and the sponsor sets individual mandates so the sum across managers equals the desired total risk exposure.
The pairing is deliberate: the IR floor demands active reward per unit of risk, while the tracking-risk cap and diversification rules keep the active risk itself small and mostly specific. ^ex-09-04-8

**Example 9: A Comparison of Active Risk** (V9 p.229, p.230)
Four managers share a benchmark and are decomposed with the BARRA US-E4 model (12 style factors, about 60 industry factors), with the industry-style covariance assumed negligible.
Active risk squared (% squared): A has industry 12.25, style 17.15, specific 19.60; B has 1.25, 13.75, 10.00; C has 1.25, 17.50, 6.25; D has 0.03, 0.47, 0.50.
Totals: A $= 12.25 + 17.15 + 19.60 = 49$; B $= 25$; C $= 25$; D $= 1$ (Python confirms each total factor risk plus specific equals the stated active risk squared).
Restating as proportions of active risk squared and taking square roots: A is 25% industry, 35% style, 60% total factor, 40% specific, TE $= \sqrt{49} = 7\%$; B is 5%, 55%, 60%, 40%, TE 5%; C is 5%, 70%, 75%, 25%, TE 5%; D is 3%, 47%, 50%, 50%, TE 1% (Python confirms every percentage and root).
Question 1, A versus B: A runs more active risk (7% versus 5%); the factor/specific split is identical at 60/40, but A takes substantial active industry risk while B is approximately industry neutral with bigger style bets.
Question 2, B versus C: same total active risk and both industry neutral, but C bets more on style factors while B carries more specific risk, implying B is somewhat less diversified than C.
Question 3, D: negligible active risk marks D as effectively passive; its active factor risk of 0.50 in variance terms is $\sqrt{0.50} = 0.707\%$ as a standard deviation (Python: 0.7071), exposures nearly matching the benchmark. ^ex-09-04-9

**Example 10: Factor Portfolios** (V9 p.232, p.233)
Six portfolios A through F carry sensitivities to five Burmeister, Roll, and Ross macro factors: confidence risk (corporate-government yield spread), time horizon risk (20-year government minus 30-day T-bill spread), inflation risk (unanticipated inflation change), business cycle risk (unexpected change in real business activity), and market timing risk (the equity index return unexplained by the first four).
Portfolio B has sensitivity 1.00 to business cycle risk and 0 to everything else; Portfolio D has sensitivity 1.00 to time horizon risk and 0 to everything else.
Question 1 and 2: to bet that real business activity will increase, use Portfolio B, the pure factor portfolio for business cycle risk, and go LONG, because a pure bet needs unit exposure to the target factor and nothing else.
Question 3 and 4: to hedge an existing positive exposure to time horizon risk, use Portfolio D, the pure factor portfolio for that risk, and go SHORT, which offsets the positive exposure.
Portfolios A, C, E, F all mix non-zero sensitivities across factors (for example F loads 0.80 confidence, 1.00 time horizon, -1.05 inflation, 0.30 business cycle, 0.75 market timing), so any position in them drags along unwanted factor bets. ^ex-09-04-10

## Item-set patterns

> [!warning] Trap 1: the assumption that is not an assumption
> The vignette lists APT properties and asks which is NOT a key assumption.
> Correct: the three assumptions are a factor model describes returns, diversification can eliminate asset-specific risk, and NO arbitrage opportunities exist among well-diversified portfolios (V9 p.206).
> The favorite distractor states that arbitrage opportunities DO exist, a one-word inversion; others smuggle in CAPM baggage (mean-variance investors, a market portfolio, normally distributed returns) that the APT never requires (V9 p.206, p.240).

> [!warning] Trap 2: the arbitrage strategy that runs backwards
> Expected returns and sensitivities for three funds are given and three buy/short strategies offered.
> Correct: build the combination whose sensitivity matches the target fund, compare expected returns, then buy the higher-expected-return side and short the matched lower one (V9 p.208, p.246).
> Distractors buy the overpriced side (right weights, wrong direction) or use weights that do not match sensitivities (50/50 when 60/40 is needed); check the weighted sensitivity before anything else (V9 p.246, p.247).

> [!warning] Trap 3: surprise means actual minus predicted
> A table gives forecast and actual values for macro factors.
> Correct: the factor value is actual minus forecast, so 1.0% actual GDP growth against a 1.5% forecast is a NEGATIVE 0.5% surprise, multiplied by the sensitivity for the return effect (V9 p.218, p.247).
> Distractors use the actual value or the forecast as the factor, drop the negative sign, or add the full factor value to the intercept that already contains the predicted component (V9 p.218).

> [!warning] Trap 4: the intercept is the expected return (macro models only)
> Given a macro model's intercept and last year's realized return, the question asks for the expected return.
> Correct: in a macroeconomic factor model the intercept IS the expected return, because factors are zero-mean surprises; realized return differs by factor effects and the error term (V9 p.218, p.248).
> Distractors offer the realized return, the risk-free rate, or benchmark-plus-something; note the contrast with fundamental models, where the standardized-beta intercept has no such interpretation (V9 p.212).

> [!warning] Trap 5: which model estimates what first
> Paired statements describe the estimation order and factor definitions of macro versus fundamental models.
> Correct: macro models build the factor (surprise) series first and regress for sensitivities; fundamental models specify sensitivities (standardized attributes) first and regress for factor returns; fundamental factors are returns, not surprises, and need not have zero means (V9 p.212, p.248).
> The distractor swaps the estimation order or claims fundamental sensitivities are regression slopes (V9 p.248, p.249).

> [!warning] Trap 6: the half-true statistical-model statement
> A statement praises statistical factor models for minimal assumptions AND easy interpretation.
> Correct: minimal assumptions is true, but interpretation is generally HARDER because extracted factors rarely map to economic meaning; also keep factor analysis (reproduces covariances) distinct from principal components (reproduces variances) (V9 p.211, p.249).
> Compound statements fail on their weakest clause; answer the interpretation half, not the assumptions half.

> [!warning] Trap 7: variance versus standard deviation in active risk
> An exhibit reports active factor risk, active specific risk, and active risk squared in % squared and asks for tracking error or proportions.
> Correct: the components are variances that sum to active risk squared; proportions are each component over the total, and TE is the square root of the total (49 gives 7%, 25 gives 5%) (V9 p.228, p.229, p.230).
> Distractors divide by TE instead of TE squared, forget the square root, or claim only factors with non-zero portfolio sensitivity contribute to active risk, when any different-from-benchmark sensitivity, including a zero against a non-zero benchmark, contributes (V9 p.248).

> [!warning] Trap 8: information ratio edge cases
> The vignette asks for an IR from a table, the IR of an index fund, or the two risks a manager takes to raise IR.
> Correct: IR is mean active return over tracking error on the same time basis, a well-run index fund has an IR of zero because its active return is zero, and the two active risks are active factor risk and active specific risk (V9 p.227, p.228, p.249).
> Distractors divide by active risk squared, use total return in the numerator, or offer the passive fund a positive IR for low tracking error (V9 p.248, p.249).

> [!warning] Trap 9: long or short the factor portfolio
> A manager wants to bet on or hedge a factor using pure factor portfolios.
> Correct: a pure factor portfolio has sensitivity 1 to one factor and 0 to all others; go long to speculate on a positive surprise, short to hedge an existing positive exposure (V9 p.231, p.232, p.233).
> Distractors pick a portfolio with mixed sensitivities because its target-factor loading is 1, or reverse the direction of the hedge (V9 p.232, p.233).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM04-Using-Multifactor-Models-Practice-Problems]]

## Cross-links

- [[LM02-Analysis-of-Active-Portfolio-Management]]: takes this module's information ratio and active risk and builds the full active-management theory around them (the fundamental law, transfer coefficient, optimal aggressiveness); learn TE and IR here first, then their determinants there.
- [[LM05-Measuring-and-Managing-Market-Risk]]: the factor covariance machinery behind active factor risk reappears in VaR and risk budgeting; sensitivity-based risk measures there generalize the factor exposures interpreted here.
- [[LM06-Backtesting-and-Simulation]]: the rolling-window backtest used to build the benchmark and risk parity multifactor portfolios in this module is the exact procedure LM6 formalizes, including the look-ahead bias the second rolling window avoids.
- [[LM04-Extensions-of-Multiple-Regression]]: supplies the regression toolkit this module consumes; macro models regress returns on surprise series and fundamental models regress returns cross-sectionally on standardized attributes, with dummy variables for industries.
- [[LM04-Hedge-Fund-Strategies]]: applies conditional factor models (factor exposures that switch between normal and crisis periods) to hedge fund return series, extending the unconditional multifactor models built here.

## Self-test

Vignette A for Q1 to Q4: An analyst observes three well-diversified portfolios priced by a one-factor APT model: X with expected return 9.5% and sensitivity 0.75, Y with 13.1% and 1.35, Z with 10.4% and 0.90.
A new well-diversified portfolio W is offered with expected return 11.5% and factor sensitivity 1.05.
All investors agree on these expected returns over a one-year horizon.

> [!question] Q1
> The risk-free rate implied by Portfolios X and Y is closest to:
> A. 3.6%.
> B. 5.0%.
> C. 6.0%.

> [!question] Q2
> The factor risk premium is closest to:
> A. 4.5%.
> B. 6.0%.
> C. 9.5%.

> [!question] Q3
> Is Portfolio Z priced consistently with the APT model implied by X and Y?
> A. Yes.
> B. No, Z is undervalued.
> C. No, Z is overvalued.

> [!question] Q4
> The arbitrage exploiting Portfolio W's pricing, per $10,000 position, is closest to:
> A. Buy W, short a 50/50 mix of X and Y, expected profit $20.
> B. Short W, buy a 50/50 mix of X and Y, expected profit $20.
> C. Buy W, short a 50/50 mix of X and Z, expected profit $35.

Vignette B for Q5 to Q7: A macro two-factor model for a fund reads $R = 7.2\% - 0.8F_{INFL} + 1.4F_{GDP} + \varepsilon$.
Inflation was forecast at 2.5% and came in at 3.1%; GDP growth was forecast at 2.0% and came in at 1.4%; the fund's asset-specific return was +0.3%.
Separately, the analyst runs a fundamental model in which a stock has a dividend yield of 1.2% while the cross-sectional average is 2.8% with a standard deviation of 1.6%.

> [!question] Q5
> The fund's return for the period is closest to:
> A. 6.18%.
> B. 7.50%.
> C. 8.22%.

> [!question] Q6
> Which factor surprise had the larger effect on the fund's return, and what sign?
> A. Inflation, positive.
> B. GDP growth, negative.
> C. Inflation, negative.

> [!question] Q7
> The stock's standardized sensitivity to the dividend yield factor is closest to:
> A. -1.6.
> B. -1.0.
> C. +0.75.

Vignette C for Q8 to Q10: A consultant reviews an active equity manager whose active risk squared is 36 (% squared), of which active factor risk is 27.
The manager's mean active return was 1.8% per year.
A second manager reports a monthly tracking error of 1.2%.
A third manager holds an existing positive exposure to an inflation factor and wants to neutralize it using one of several pure factor portfolios.

> [!question] Q8
> The first manager's active specific risk and tracking error are closest to:
> A. 9 (% squared) and 6%.
> B. 9 (% squared) and 36%.
> C. 27 (% squared) and 6%.

> [!question] Q9
> The first manager's information ratio and the second manager's annualized tracking error are closest to:
> A. 0.05 and 4.16%.
> B. 0.30 and 4.16%.
> C. 0.30 and 14.40%.

> [!question] Q10
> The third manager should:
> A. short the inflation factor portfolio, which has sensitivity 1 to inflation and 0 to all other factors.
> B. buy the inflation factor portfolio, which has sensitivity 1 to inflation and 0 to all other factors.
> C. short a portfolio with sensitivity 1 to inflation and 0.5 to the business cycle factor.

> [!success]- Answer key
> Q1: B.
> Two equations: $0.095 = R_F + 0.75\lambda$ and $0.131 = R_F + 1.35\lambda$; subtracting gives $\lambda = 0.036/0.60 = 0.06$ and $R_F = 0.095 - 0.75 \times 0.06 = 0.05$ (Python: 0.06 and 0.05); A solves for lambda but reports 3.6% (the return spread), C misreads the intercept.
> Q2: B.
> From Q1, $\lambda = 6\%$; A divides the spread by the wrong sensitivity gap, C is X's expected return recycled.
> Q3: A.
> Implied $E(R_Z) = 0.05 + 0.90 \times 0.06 = 0.104$ (Python: 0.104), exactly the offered 10.4%, so Z sits on the pricing line and no arbitrage involves it.
> Q4: A.
> Replicate W's 1.05 sensitivity with weights $w$ on X: $0.75w + 1.35(1-w) = 1.05$ gives $w = 0.5$; the 50/50 X+Y mix has expected return $0.5 \times 9.5\% + 0.5 \times 13.1\% = 11.3\%$ (Python: 1.05 and 0.113), below W's 11.5%, so W is undervalued: buy W, short the mix, and expect $10{,}000 \times (0.115 - 0.113) = \$20$ (Python: 20.0); B trades the right pair backwards, C's X+Z mix at 50/50 has sensitivity $0.825 \ne 1.05$, leaving factor risk.
> Q5: A.
> Surprises: inflation $3.1 - 2.5 = +0.6\%$, GDP $1.4 - 2.0 = -0.6\%$; $R = 7.2 - 0.8 \times 0.6 + 1.4 \times (-0.6) + 0.3 = 7.2 - 0.48 - 0.84 + 0.3 = 6.18\%$ (Python: 6.18); B forgets the error term and one factor, C flips the GDP surprise sign.
> Q6: B.
> GDP's effect is $1.4 \times (-0.6\%) = -0.84\%$ against inflation's $-0.8 \times 0.6\% = -0.48\%$, so GDP growth, negative, dominates; C has the right runner-up, A has the wrong sign entirely.
> Q7: B.
> Standardized beta $= (1.2 - 2.8)/1.6 = -1.0$ (Python: -1.0), one standard deviation below average; A forgets to divide by the standard deviation correctly (uses the raw gap), C is a sign-and-scale error.
> Q8: A.
> Active specific risk $= 36 - 27 = 9$ (% squared), and TE $= \sqrt{36} = 6\%$ (Python: 9 and 6.0); B forgets the square root, C returns the factor component instead of the specific component.
> Q9: B.
> $IR = 1.8\%/6\% = 0.30$ and annualized TE $= 1.2\% \times \sqrt{12} = 4.16\%$ (Python: 0.30 and 4.157); A divides the mean active return by active risk squared, C multiplies the monthly TE by 12 instead of the square root of 12.
> Q10: A.
> Hedging an existing positive exposure requires a SHORT position in the pure factor portfolio for that factor (sensitivity 1 to inflation, 0 elsewhere) (V9 p.232, p.233); B is the speculative direction, C drags in an unwanted business cycle bet.

## Flashcards

#flashcards/cfa-l2/09-Portfolio-Management/lm04

Factor (investments definition)::A variable or characteristic with which individual asset returns are correlated (V9 p.203).
Arbitrage opportunity::An opportunity to earn an expected positive net profit without risk and with no net investment of money (V9 p.206).
The three APT assumptions::A factor model describes asset returns; investors can form well-diversified portfolios that eliminate asset-specific risk; no arbitrage opportunities exist among well-diversified portfolios (V9 p.206).
Which APT "assumption" is the classic exam distractor?::That arbitrage opportunities DO exist among well-diversified portfolios; the real assumption is that they do not (V9 p.206).
How does the APT differ from the CAPM on assumptions?::The APT makes fewer and weaker assumptions and does not specify the number or identity of factors or require mean-variance preferences (V9 p.205, p.206).
APT equation::{{E(Rp) = RF + lambda1 x beta_p1 + ... + lambdaK x beta_pK}} (V9 p.206).
Factor risk premium lambda_j::The expected reward for bearing the risk of a portfolio with sensitivity 1 to factor j and 0 to all other factors (V9 p.206).
Pure factor portfolio::A portfolio with sensitivity of 1 to one factor and 0 to all other factors; used to speculate on or hedge that factor (V9 p.206, p.231).
What replaces RF in the APT equation when no risk-free asset exists?::lambda0, the expected return on a risky portfolio with zero sensitivity to all factors (V9 p.206).
Micro-problem: pure factor portfolio earns 12%, RF is 4%; lambda?::lambda = 12% - 4% = 8%; keystrokes 12 - 4 = (V9 p.207).
The three steps of an APT arbitrage check::Build a combination matching the target's factor sensitivity, compare expected returns, buy the higher-return side and short the matched lower one (V9 p.208).
Why is the APT arbitrage position riskless?::The matched sensitivities cancel factor risk and diversification has eliminated asset-specific risk, so zero net cost earns a positive expected profit (V9 p.208, p.209).
Carhart four factors::RMRF (market excess return), SMB (small minus big), HML (high minus low book-to-market), WML (winners minus losers) (V9 p.209).
What does the Carhart model do to CAPM anomalies?::It reinterprets size, value, and momentum anomalies as priced systematic risk factors (V9 p.210).
Macroeconomic factor model factors::Surprises in macroeconomic variables, actual minus predicted, with expected value zero (V9 p.211, p.217).
Fundamental factor model factors::Returns associated with attributes of stocks or companies that explain cross-sectional price differences, such as book-to-price, market cap, P/E, leverage (V9 p.211).
Statistical factor model factors::Portfolios of the securities under study, defined by portfolio weights, extracted by statistical methods from historical returns (V9 p.211).
Factor analysis models vs principal components models::Factor analysis factors best explain historical return covariances; principal components factors best explain historical return variances (V9 p.211).
Advantage and drawback of statistical factor models::Minimal assumptions, but the factors are generally hard to interpret economically (V9 p.211).
Surprise in a macro factor::Actual value minus predicted value; only the surprise moves returns because predictions are already in prices (V9 p.217, p.218).
Intercept of a macroeconomic factor model::The expected return of the asset, the return when all surprises and the error are zero (V9 p.218).
Intercept of a fundamental factor model with standardized betas::Not interpreted beyond being a regression intercept included so expected asset-specific risk is zero (V9 p.212).
Standardized beta formula::Attribute value for the asset minus the cross-sectional average, divided by the standard deviation of the attribute's values (V9 p.212).
Micro-problem: dividend yield 3.5%, average 2.5%, sd 2%; sensitivity?::(3.5 - 2.5)/2 = 0.50, half a standard deviation above average (V9 p.212).
How do industry factors enter fundamental models?::As 0/1 dummy variables, exempt from standardization (V9 p.212).
Estimation order in macro vs fundamental models::Macro builds the surprise series first and regresses for sensitivities; fundamental specifies sensitivities (attributes) first and regresses for factor returns (V9 p.212).
Three groups of fundamental factors for equities::Company fundamental factors, company share-related factors, and macroeconomic factors such as industry membership (V9 p.213).
Global factor model classification::Country, industry, and style factors, with country and industry as dummies (V9 p.213).
Fixed-income fundamental factor categories::Duration, credit, currency, and geography (V9 p.214).
Typical signs of macro factor premiums::GDP growth premium positive; inflation premium negative, because positive inflation sensitivity is a hedge investors pay for (V9 p.219).
How are portfolio-level macro model parameters found?::As market-value-weighted averages of the individual assets' parameters (V9 p.219).
Active return definition::Portfolio return minus benchmark return (V9 p.224).
Active return decomposition::Return from factor tilts (sensitivity differences times factor returns) plus security selection (V9 p.224).
Return from factor tilts::The sum over factors of (portfolio sensitivity minus benchmark sensitivity) times the factor return, using beginning-of-period sensitivities (V9 p.224).
Security selection in return attribution::The residual active return from overweighting outperformers and underweighting underperformers (V9 p.224).
Tracking error (tracking risk, active risk)::The sample standard deviation of the time series of active returns (V9 p.226).
Annualizing tracking error::Multiply daily TE by the square root of 250 or monthly TE by the square root of 12, assuming serially uncorrelated returns (V9 p.226).
Typical TE ranges (passive, enhanced, diversified active, aggressive)::About 0.10% passive, about 2% enhanced index, 2% to 6% diversified active large-cap, 6% to 10% or more aggressive (V9 p.226, p.227).
Information ratio::Mean active return divided by tracking error, on the same time basis; active reward per unit of active risk (V9 p.227).
Micro-problem: portfolio mean 9%, benchmark mean 7.5%, TE 6%; IR?::(9 - 7.5)/6 = 0.25; keystrokes 9 - 7.5 = / 6 = (V9 p.227).
IR of an index fund meeting its objective::Zero, because active return is zero (V9 p.249).
Active risk squared::The variance of active return, s squared of (Rp minus RB) (V9 p.228).
Decomposition of active risk squared::Active factor risk plus active specific risk, both stated as variances (V9 p.228).
Active factor risk::The contribution to active risk squared from different-from-benchmark factor exposures; found indirectly as the total minus active specific risk (V9 p.228).
Active specific risk formula::Sum over assets of squared active weight times the asset's residual variance (V9 p.228).
What does high active specific risk suggest about a portfolio?::More concentrated, less diversified security selection bets (V9 p.228, p.230).
Micro-problem: active risk squared 49, active factor risk 29.40; specific and TE?::Specific = 49 - 29.40 = 19.60 (% squared); TE = sqrt(49) = 7% (V9 p.229, p.230).
Do zero portfolio sensitivities against non-zero benchmark sensitivities create active risk?::Yes; any different-from-benchmark sensitivity is an active exposure that contributes to active risk (V9 p.248).
Three portfolio construction uses of multifactor models::Passive index replication by matching factor exposures, active alpha and risk-profile construction, and rules-based (alternative index) factor tilts (V9 p.231).
Rules-based active management::Transparent, mechanical, low-cost strategies tilting toward factors such as size, value, quality, momentum, capturing systematic exposure once attributed to alpha (V9 p.231).
Position to hedge an existing positive factor exposure::Short the pure factor portfolio for that factor (V9 p.233).
Risk parity multifactor portfolio weighting::Each pure factor portfolio is weighted so it contributes equally to overall portfolio risk, using the factor covariance matrix (V9 p.234).
US backtest result, risk parity vs equal-weight multifactor portfolio::Risk parity earned a lower cumulative return with much lower volatility, nearly doubling the Sharpe ratio (V9 p.235, p.236).
Comparative advantage framing of strategic decisions::Tilt toward priced risks you can bear better than average (long-horizon endowment and business cycle or liquidity risk) and away from risks you bear worse (V9 p.236, p.237).
Why is the multifactor view richer than the CAPM prescription?::The CAPM sends everyone to the market portfolio plus a risk-free asset; factor models let investors tilt exposures to match their own risk-bearing advantages (V9 p.236, p.237).

## Common mistakes

1. Reading "arbitrage opportunities exist among well-diversified portfolios" as an APT assumption; the assumption is that none exist, and the inverted statement is a standing distractor (V9 p.206, p.246).
2. Shorting the underpriced side of an APT arbitrage; always buy the side whose expected return is too high for its sensitivity and short the matched replication (V9 p.208, p.247).
3. Building the replicating combination without checking that its weighted sensitivity actually matches the target (50/50 when 60/40 matches), which leaves factor risk in a supposedly riskless trade (V9 p.246, p.247).
4. Using actual factor values instead of surprises (actual minus predicted) in a macro model, or dropping the sign of a negative surprise (V9 p.218, p.247).
5. Answering a macro model's expected return with the realized return; the intercept is the expected return because surprises and errors have zero means (V9 p.218, p.248).
6. Carrying the macro-model intercept interpretation into fundamental models, where standardized betas strip the intercept of that meaning (V9 p.212).
7. Swapping the estimation order: macro models estimate sensitivities last (surprise series first), fundamental models specify sensitivities first (factor returns estimated last) (V9 p.212, p.248).
8. Accepting the half-true claim that statistical models' minimal assumptions make them easy to interpret; interpretation is their weakness (V9 p.211, p.249).
9. Stopping at the largest single-factor effect when the question asks for the largest combined effect of several surprises, or vice versa (V9 p.247, p.248).
10. Treating active factor risk and active specific risk as standard deviations; they are variances, proportions are taken against active risk squared, and tracking error is the square root of the total (V9 p.228, p.230).
11. Claiming only factors with non-zero portfolio sensitivity drive active risk; a zero sensitivity against a non-zero benchmark sensitivity is an active bet (V9 p.248).
12. Giving an index fund a positive information ratio for having low tracking error; zero active return means zero IR (V9 p.227, p.249).
13. Annualizing a monthly tracking error by multiplying by 12 instead of the square root of 12 (V9 p.226).
14. Going long the pure factor portfolio when the task is to hedge an existing positive exposure; hedging requires the short position (V9 p.233).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "09-04" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
