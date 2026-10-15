---
type: cfa-lm
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
volume: 1
lm: 3
title: "Model Misspecification"
pages: "49-74"
weight_band: "5-10%"
difficulty: 3
los_count: 4
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/quantitative-methods]
---
# LM3: Model Misspecification

Difficulty 3 of 5: the arithmetic is trivial (one product, one reciprocal, one table lookup) but the exam lives in the fine distinctions between which violation breaks which output, which test detects it, and which fix applies, so the marks are lost to confusion rather than computation.

## LOS map

- **describe** how model misspecification affects the results of a regression analysis and how to avoid common forms of misspecification (V1 p.50) ^los-01-03-a
    - Examiner asks: a residual scatterplot or a description of a model is given and you must name the failure (omitted variable, wrong functional form, wrong scaling, wrong pooling), state whether coefficients or only standard errors are damaged, and pick the correction.
- **explain** the types of heteroskedasticity and how it affects statistical inference (V1 p.55) ^los-01-03-b
    - Examiner asks: compute the Breusch-Pagan statistic $nR^2$ from an auxiliary regression, compare it with a chi-square critical value with $k$ degrees of freedom, and state that conditional (not unconditional) heteroskedasticity deflates standard errors, inflates t-statistics and raises Type I errors, fixed by robust (White) standard errors.
- **explain** serial correlation and how it affects statistical inference (V1 p.61) ^los-01-03-c
    - Examiner asks: read a Breusch-Godfrey F-statistic against an $F(p, n-p-k-1)$ critical value, then decide whether coefficients are invalid (only when a lagged dependent variable is a regressor) or only the standard errors are deflated, fixed by Newey-West or robust standard errors.
- **explain** multicollinearity and how it affects regression analysis (V1 p.66) ^los-01-03-d
    - Examiner asks: spot the classic symptom (high $R^2$, significant F, insignificant t-statistics), compute $VIF_j = 1/(1-R_j^2)$, apply the 5 and 10 thresholds, and list the three corrections (drop a variable, change a proxy, increase the sample).

## Core intuition

Everything in this module follows from one question: what does OLS assume, and what breaks when the assumption fails.
[[LM01-Basics-of-Multiple-Regression-and-Underlying-Assumptions]] gave the assumptions: linear in the parameters, errors with zero mean and constant variance, errors uncorrelated across observations, no exact linear relation among regressors, and errors normally distributed.
[[LM02-Evaluating-Regression-Model-Fit-and-Interpreting-Model-Results]] built the inference machinery on top of those assumptions: standard errors, t-statistics, the F-test, confidence intervals.
This module asks what happens to that machinery when the model is wrong.

> [!abstract] Idea 1: misspecification is the root, assumption violations are the symptoms
> Exhibit 2 (V1 p.51) is a causal chain, not a list.
> Omit a variable, use the wrong functional form, fail to scale, or pool data that should not be pooled, and the leftover structure shows up in the residuals as heteroskedasticity, serial correlation or multicollinearity.
> The curriculum's first correction is therefore always "revise the model" and only then "use robust standard errors" (Exhibit 14, V1 p.70).

Start with specification itself.
Exhibit 1 (V1 p.51) lists five principles: the model should be grounded in economic reasoning, parsimonious, good out of sample, of appropriate functional form, and free of assumption violations.
The economic reasoning principle matters because a regressor that fits the sample without a story is likely to be an overfit artifact that fails out of sample.
Parsimony matters because every extra regressor costs a degree of freedom and invites multicollinearity.
The functional form principle matters because a nonlinear relationship forced into a straight line leaves systematic residuals, which is heteroskedasticity by construction.

Now the four failures of functional form (V1 p.51-52).
Omitted variables are the most important because they are the only failure that can bias the coefficients themselves.
If the true model is $Y = b_0 + b_1 X_1 + b_2 X_2 + \varepsilon$ and you estimate $Y = b_0 + b_1 X_1 + \varepsilon$, the residual of your model is $b_2 X_2 + \varepsilon$ (V1 p.52).
Two cases follow.
If $X_2$ is uncorrelated with $X_1$, the residual no longer has zero mean and is no longer identically distributed, so the intercept is biased, but the slope on $X_1$ is still estimated correctly.
If $X_2$ is correlated with $X_1$, the error term is now correlated with a regressor, and the slope on $X_1$, the intercept, the residuals and the standard errors are all biased and inconsistent (V1 p.52).
The economic reason is simple: OLS attributes to $X_1$ whatever part of $X_2$ moves with it, so the coefficient on $X_1$ absorbs the omitted effect.
The knowledge check on gold and VIX (V1 p.52-55) shows the fingerprint: the residuals from a two-factor model line up on a straight line against the market excess return, with $R^2 = 0.6474$, which means the market belongs in the model.

Inappropriate form of variables means specifying a linear relation when theory or a plot says the relation is nonlinear (V1 p.52).
The standard fix is a log transformation when the relation becomes linear in proportional changes.
Inappropriate scaling means regressing raw values across companies of different sizes when common-size ratios are the comparable quantity (V1 p.52).
Inappropriate pooling means running one regression across a structural break, a regulatory change or a shift from a low-volatility to a high-volatility regime (V1 p.52).
The scatterplot signature of bad pooling is distinct, widely separated clusters with little correlation within each, and the remedy is to estimate on the subsample most representative of the forecast period.

> [!abstract] Idea 2: all three violations attack the standard errors, but only some attack the coefficients
> Heteroskedasticity and serial correlation without a lagged dependent variable leave the coefficients consistent and lie only about their precision, usually by understating standard errors so t-statistics are too large (V1 p.57, p.62).
> Serial correlation with a lagged dependent variable and omitted correlated variables make the coefficients themselves inconsistent (V1 p.52, p.61).
> Multicollinearity leaves coefficients consistent but inflates standard errors so t-statistics are too small (V1 p.66).
> The direction of the standard error error is the single most tested fact in the module.

Heteroskedasticity means the error variance is not constant across observations (V1 p.55).
The curriculum splits it into two types.
Unconditional heteroskedasticity is error variance that changes but is not correlated with the regressors, and it creates no major problem for inference (V1 p.56).
Conditional heteroskedasticity is error variance that is correlated with, that is conditional on, the values of the regressors, and it is the problematic type (V1 p.56).
Why is it a problem?
The OLS formula for the standard error of a coefficient assumes one error variance, estimated by the MSE.
When the variance is larger exactly where the regressor takes extreme values, the true uncertainty about the slope is larger than the MSE-based formula reports, so standard errors are understated, t-statistics are inflated, and the analyst commits more Type I errors, rejecting true nulls (V1 p.57).
The F-test is also unreliable because the MSE is a biased estimator of the population error variance (V1 p.56-57).

The Breusch-Pagan test converts this intuition into a procedure (Exhibit 4, V1 p.57).
Run the original regression, square the residuals, and regress the squared residuals on the same regressors.
If the regressors explain the squared residuals, then the error variance depends on the regressors, which is the definition of conditional heteroskedasticity.
The test statistic is $nR^2$ from the auxiliary regression, chi-square with $k$ degrees of freedom, and the test is one-tailed to the right (V1 p.57).
In the Fama-French example (Exhibit 5, V1 p.58) the statistic is 13.40 against 3 factors and the null is rejected at the 1% level.
The correction is not to re-estimate the coefficients, which are fine, but to replace the standard errors with robust standard errors, also called heteroskedasticity-consistent or White-corrected standard errors (V1 p.59).
Exhibit 6 (V1 p.59) shows the result: the coefficients are identical to Exhibit 5, the MKTRF standard error rises from 0.060 to 0.091, and the t-statistic falls from 20.6 to 13.6.

Serial correlation means errors are correlated across observations, and it lives mainly in time-series and panel regressions (V1 p.61).
Positive first-order serial correlation means a positive residual today makes a positive residual tomorrow more likely, so the sign of the residual persists (V1 p.61-62).
The consequences depend on one fact (Exhibit 7, V1 p.61).
If no regressor is a lagged value of the dependent variable, the coefficients are consistent and only the standard errors are wrong.
If a regressor is a lagged dependent variable, every coefficient is inconsistent.
The economic reason is that a lagged dependent variable contains last period's error, and if that error is correlated with this period's error, the regressor is correlated with the error term, which is the same disease as an omitted correlated variable.
With positive serial correlation the MSE understates the population error variance, so the F-statistic is inflated, the standard errors are understated and the t-statistics are inflated, again producing Type I errors (V1 p.62).

Two tests appear.
The Durbin-Watson test compares the squared differences of successive residuals with the sum of squared residuals, but it detects only first-order serial correlation (V1 p.62).
The Breusch-Godfrey test is more robust because it detects correlation up to a chosen order $p$: regress the residuals on the original regressors plus $p$ lagged residuals and test whether the lagged-residual coefficients are jointly zero (Exhibit 8, V1 p.62).
The statistic is F-distributed with $p$ and $n - p - k - 1$ degrees of freedom (V1 p.62).
The GDP on consumption example (Exhibit 9, V1 p.63) shows a slope with a t-statistic of 32 and a BG test that rejects, so the analyst cannot trust that t-statistic until the standard errors are corrected.
The correction is again robust standard errors, now called serial-correlation consistent, Newey-West, or heteroskedasticity- and autocorrelation-consistent (HAC) standard errors, and these correct for both problems at once (V1 p.64).
Exhibit 10 (V1 p.64) shows the CONS standard error rising from 0.027 to 0.036 and the t-statistic falling from 32.0 to 24.3, while the coefficient 0.8696 does not move.
The curriculum stresses that the serial correlation is not eliminated; the standard errors simply account for it.

> [!abstract] Idea 3: market efficiency says these patterns should not exist, so if you find them, exploit them as well as correct them
> Heteroskedasticity in the form of volatility clustering and serial correlation in returns are both forms of predictability (V1 p.59, p.62, p.65).
> Under even weak-form efficiency they should be arbitraged away.
> The curriculum therefore tells the analyst to correct the standard errors and to understand and capitalize on the underlying process.

Multicollinearity is the violation of the assumption that no exact linear relation exists among the regressors (V1 p.66).
An exact relation makes estimation impossible; an approximate one makes it possible but uninformative.
The consequence is the opposite direction from the other two violations: coefficients stay consistent, but their standard errors are inflated and t-statistics diminished, so t-tests have little power (V1 p.66).
The economic reason is that when two regressors move together, the data cannot say which one is driving the dependent variable, so the estimate of each slope is imprecise even though the pair together explains the dependent variable well.
That gives the classic symptom: high $R^2$ and a significant F-statistic with individually insignificant t-statistics (V1 p.66).
Pairwise correlations are inadequate as a detector beyond two regressors because a linear combination of several variables can be highly collinear with another regressor while every pairwise correlation is modest (V1 p.66).
The variance inflation factor fixes this: regress $X_j$ on the other $k-1$ regressors, take the $R_j^2$, and compute $VIF_j = 1/(1-R_j^2)$ (V1 p.66).
A VIF of 1 means no correlation with the other regressors, above 5 warrants investigation, above 10 requires correction (V1 p.67).
The FSPTX example (Exhibit 11-13, V1 p.67-69) is the cleanest demonstration in the curriculum: adding the S&P 500 to a regression that already contains its growth and value components leaves $R^2$ at 0.782, pushes the standard error of SGX from 0.196 to 6.166, and pushes VIFs into the thousands.
Corrections are to drop a variable, use a different proxy, or increase the sample size (V1 p.69), and if the only goal is prediction rather than interpretation, multicollinearity may not matter at all.

Exhibit 14 (V1 p.70) is the module in one table and should be memorized as a three-row decision matrix.

| Violation | Damage | Detection | Correction |
|---|---|---|---|
| Heteroskedastic errors (V1 p.70) | Biased standard errors (understated) | Residual plots; Breusch-Pagan test | Revise model; robust standard errors |
| Serial correlation (V1 p.70) | Inconsistent coefficients if lagged dependent variable; biased standard errors | Breusch-Godfrey test (Durbin-Watson for first order only) | Revise model; serial-correlation consistent standard errors |
| Multicollinearity (V1 p.70) | Inflated standard errors, low power | Variance inflation factor | Revise model; increase sample size |

## Formulas and derivations

**Omitted-variable residual** (V1 p.51-52)
$$
Y_i = b_0 + b_1 X_{1i} + b_2 X_{2i} + \varepsilon_i \quad \text{(true)}, \qquad Y_i = b_0 + b_1 X_{1i} + \varepsilon_i \quad \text{(estimated)}, \qquad \text{residual} = b_2 X_{2i} + \varepsilon_i
$$
^f-01-03-1

- $X_2$ is the omitted regressor, $b_2$ its true coefficient, $\varepsilon_i$ the true error with zero mean.
- If $\mathrm{Corr}(X_1, X_2) = 0$: residual has non-zero mean and is not identically distributed, so the intercept is biased but $\hat{b}_1$ is still correct (V1 p.52).
- If $\mathrm{Corr}(X_1, X_2) \neq 0$: the error is correlated with $X_1$, so $\hat{b}_0$, $\hat{b}_1$, the residuals and the standard errors are all biased and inconsistent (V1 p.52).
- Reason it holds: the estimated residual is whatever the estimated model leaves unexplained, and that includes the entire omitted term $b_2 X_{2i}$.

**Breusch-Pagan auxiliary regression** (V1 p.57)
$$
\hat{u}_t^2 = a_0 + a_1 X_{1t} + a_2 X_{2t} + \cdots + a_k X_{kt} + \epsilon_t, \qquad H_0: a_1 = a_2 = \cdots = a_k = 0
$$
^f-01-03-2

- $\hat{u}_t$ are the residuals from the original regression $Y_t = b_0 + b_1 X_{1t} + \cdots + b_k X_{kt} + u_t$, squared to proxy the error variance.
- The regressors are exactly the $k$ regressors of the original model.
- $H_a$: at least one $a_j \neq 0$, meaning the error variance depends on a regressor, which is conditional heteroskedasticity (V1 p.57).
- Reason it holds: each observation's squared residual is correlated with the regressors if the regressors affect the variance of the errors.

**Breusch-Pagan test statistic** (V1 p.57)
$$
\chi^2_{BP,k} = n R^2 \sim \chi^2_k
$$
^f-01-03-3

- $n$ is the number of observations, $R^2$ is from the auxiliary regression in formula 2, $k$ is the number of independent variables in the original regression.
- One-tailed, right-side test: reject $H_0$ of no conditional heteroskedasticity when $nR^2$ exceeds the chi-square critical value with $k$ degrees of freedom (V1 p.57).
- Reason it holds: under $H_0$ the auxiliary $R^2$ is near zero, and $nR^2$ is the Lagrange-multiplier form of the joint test that all $a_j = 0$.
- Common critical values at 5%: $k=1$: 3.841, $k=2$: 5.991, $k=3$: 7.815, $k=4$: 9.488, $k=5$: 11.070 (matches the 11.07 given in the practice problems at V1 p.71).

> [!tip] Calculator
> BA II Plus: enter $n$, press `×`, enter $R^2$ (as a decimal, not a percentage), press `=`.
> For 96 observations and $R^2 = 0.06511$: `96 × 0.06511 =` gives 6.2506.
> Use the $R^2$ of the auxiliary regression, never the adjusted $R^2$ and never the $R^2$ of the original regression.

**Breusch-Godfrey auxiliary regression** (V1 p.62)
$$
\hat{u}_t = a_0 + a_1 X_{1t} + a_2 X_{2t} + \cdots + a_k X_{kt} + \rho_1 \hat{u}_{t-1} + \cdots + \rho_p \hat{u}_{t-p} + e_t, \qquad H_0: \rho_1 = \cdots = \rho_p = 0
$$
^f-01-03-4

- $\hat{u}_t$ are the residuals (not squared) from the original regression, $p$ is the chosen order of serial correlation to test, $\rho_j$ is the coefficient on the $j$-th lagged residual.
- Exhibit 8 (V1 p.62) illustrates with $p = 1$, so a single lagged residual $\rho_1 \hat{u}_{t-1}$ and $H_0: \rho_1 = 0$ against $H_a: \rho_1 \neq 0$.
- Reason it holds: if errors are correlated with their own lags up to order $p$, the lagged residuals will have explanatory power for the current residual even after controlling for the original regressors.

**Breusch-Godfrey test distribution** (V1 p.62)
$$
F_{BG} \sim F\left(p,\; n - p - k - 1\right)
$$
^f-01-03-5

- $p$ lags in the numerator degrees of freedom; $n - p - k - 1$ in the denominator, where $k$ is the number of original regressors and $p$ observations are lost to lagging.
- Reject $H_0$ of no serial correlation up to lag $p$ when $F_{BG}$ exceeds the critical value, or when the reported p-value is below the significance level (V1 p.62).
- Software may also report a chi-square version; the exam gives you the statistic and the degrees of freedom and expects a table comparison.
- Reason it holds: the BG statistic is the joint F-test on the $p$ lagged-residual coefficients in formula 4, so its numerator degrees of freedom is the number of restrictions $p$.

**Durbin-Watson statistic** (V1 p.62)
$$
DW = \frac{\sum_{t=2}^{n} (\hat{u}_t - \hat{u}_{t-1})^2}{\sum_{t=1}^{n} \hat{u}_t^2} \approx 2(1 - r)
$$
^f-01-03-6

- $r$ is the sample first-order autocorrelation of the residuals; the curriculum describes DW verbally as the squared differences of successive residuals compared with the sum of squared residuals (V1 p.62).
- $DW = 2$ means no first-order serial correlation, $DW \to 0$ means strong positive serial correlation, $DW \to 4$ means strong negative serial correlation.
- Limitation stated in the module: DW tests only first-order serial correlation, which is why the curriculum prefers Breusch-Godfrey (V1 p.62).
- Reason the approximation holds: expanding the numerator gives $\sum \hat{u}_t^2 + \sum \hat{u}_{t-1}^2 - 2\sum \hat{u}_t \hat{u}_{t-1} \approx 2\sum \hat{u}_t^2 (1 - r)$ for large $n$.

**Variance inflation factor** (V1 p.66)
$$
VIF_j = \frac{1}{1 - R_j^2}
$$
^f-01-03-7

- $R_j^2$ is the coefficient of determination from regressing $X_j$ on the other $k - 1$ independent variables; it has nothing to do with the dependent variable $Y$.
- $VIF_j = 1$ when $R_j^2 = 0$ (no correlation with the other regressors), which is the minimum (V1 p.66).
- Rules of thumb: $VIF_j > 5$ warrants investigation, $VIF_j > 10$ indicates serious multicollinearity requiring correction (V1 p.67), equivalent to $R_j^2 > 0.80$ and $R_j^2 > 0.90$.
- Reason it holds: the sampling variance of $\hat{b}_j$ is proportional to $1/(1 - R_j^2)$, so the VIF is the factor by which the variance of the coefficient is inflated relative to a regressor uncorrelated with the others.

> [!tip] Calculator
> BA II Plus: enter $R_j^2$, press `+/-`, `+ 1 =`, then `1/x`.
> For $R_j^2 = 0.942$: `0.942 +/- + 1 = 1/x` gives 17.24.
> Reverse direction if a VIF is given and you need $R_j^2$: `VIF 1/x +/- + 1 =`.

**Inverting the VIF and the two-regressor case** (V1 p.66, p.69)
$$
R_j^2 = 1 - \frac{1}{VIF_j}, \qquad \text{with exactly two regressors: } R_j^2 = r_{12}^2 \;\Rightarrow\; VIF_1 = VIF_2 = \frac{1}{1 - r_{12}^2}
$$
^f-01-03-8

- $r_{12}$ is the pairwise correlation between the two regressors; with two regressors the auxiliary $R^2$ is exactly the squared pairwise correlation, so both VIFs are equal (Exhibit 13, V1 p.69: SGX and SVX both 3.97).
- With more than two regressors, low pairwise correlations do not rule out multicollinearity (V1 p.66), so only the VIF is a reliable detector.
- Reason it holds: for a simple regression of $X_1$ on $X_2$ the $R^2$ equals the squared correlation, and the relation is symmetric.

**t-statistic with robust standard errors** (V1 p.59, p.64)
$$
t_{robust} = \frac{\hat{b}_j}{SE_{robust}(\hat{b}_j)}, \qquad \hat{b}_j \text{ unchanged}, \quad SE_{robust} > SE_{OLS} \text{ typically}
$$
^f-01-03-9

- $SE_{robust}$ is the White (heteroskedasticity-consistent) standard error or the Newey-West / HAC (heteroskedasticity- and autocorrelation-consistent) standard error.
- The correction changes the standard errors only; the coefficient estimates from Exhibit 5 to 6 and from Exhibit 9 to 10 are identical (V1 p.59, p.64).
- Larger standard errors mean smaller t-statistics, larger p-values, wider confidence intervals, fewer rejections of $H_0$ (V1 p.61, p.64).
- Reason it holds: the robust estimator replaces the single-variance assumption in the variance-covariance matrix with an estimator that uses the observed residual pattern.

## Worked examples

**Example 1: Gold returns, VIX, and the two-factor precious metals model (knowledge check, V1 p.52-55)**

Setup: 32 months of gold returns (GOLD) regressed on changes in the VIX.
Two scatterplots are shown: GOLD versus VIX change, and residuals versus GOLD.

Part 1: violations indicated by the scatterplots.
- The residual plot shows a strong positive linear relationship between residuals and GOLD, not random noise.
- Residuals that track the dependent variable are not zero-mean, not independent, not identically distributed, and heteroskedastic (V1 p.53).
- The scatter of GOLD on VIX shows no clear linear relation, so VIX alone does not explain gold returns.

Part 2: correction.
- Add explanatory variables: market returns, expected inflation, and an indicator for high versus low geopolitical risk periods (V1 p.54).

Part 3: the factor model $PORTA_i = b_0 + b_1 X_{1i} + b_2 X_{2i} + \varepsilon_i$.
Results (V1 p.54):

| Variable | Coefficient | SE | t-stat | p-value |
|---|---|---|---|---|
| Intercept | 0.013 | 0.005 | 2.671 | 0.009 |
| X1 | 1.896 | 0.208 | 9.111 | 0.000 |
| X2 | 0.170 | 0.186 | 0.916 | 0.361 |

Check of the t-statistics: $1.896 / 0.208 = 9.115$ and $0.170 / 0.186 = 0.914$, matching the table to rounding; the intercept $0.013 / 0.005 = 2.600$ versus the printed 2.671, the gap being rounding of the coefficient and standard error to three decimals.
Adjusted $R^2$ is 43% and the F-test rejects the joint null.
The residuals plotted against MKTRF fit the line $y = 1.0225x - 0.0118$ with $R^2 = 0.6474$ (V1 p.54).
- Misspecification type: omitted variable bias, because the residuals of the two-factor model are strongly explained by a variable not in the model (V1 p.54).

Part 4: effect on the estimated model.
- The coefficients on X1 and X2 are biased and inconsistent, and so are their standard errors, so no statistical inference can be drawn from the model (V1 p.54).
- This is the correlated-omitted-variable case of formula 1: MKTRF is almost certainly correlated with the two factors.

Part 5: correction.
- Include MKTRF and re-estimate the model (V1 p.55).
^ex-01-03-1

**Example 2: Breusch-Pagan test on the Fama-French three-factor model for stock XYZ (Exhibits 5 and 6, V1 p.57-59)**

Setup: 120 monthly observations, regressors MKTRF, SMB, HML, so $k = 3$.
Panel A (V1 p.58): $R^2 = 0.8788$, adjusted $R^2 = 0.8757$, $F = 280.4951$, residual df 116.

| Variable | Coefficient | SE (OLS) | t (OLS) | SE (robust) | t (robust) |
|---|---|---|---|---|---|
| Intercept | -0.0026 | 0.0024 | -1.0735 | 0.0021 | -1.2347 |
| MKTRF | 1.2414 | 0.0601 | 20.6419 | 0.0910 | 13.6483 |
| SMB | 1.0953 | 0.1042 | 10.5147 | 0.1111 | 9.8605 |
| HML | -0.1065 | 0.0872 | -1.2205 | 0.1015 | -1.0488 |

Step 1: verify the OLS t-statistics.
- MKTRF: $1.2414 / 0.0601 = 20.656$, printed 20.6419, rounding of SE.
- SMB: $1.0953 / 0.1042 = 10.512$, printed 10.5147.
- HML: $-0.1065 / 0.0872 = -1.221$, printed -1.2205.

Step 2: BP test (Panel B, V1 p.58).
- BP statistic 13.40264, chi-square with $k = 3$ degrees of freedom.
- Critical values: 7.815 at 5%, 11.345 at 1%.
- $13.40 > 11.345$, so reject $H_0$ of no conditional heteroskedasticity at the 1% level, as the curriculum states (V1 p.58).
- Recomputed p-value for 13.40264 on 3 df is 0.0038, not the 0.00038 printed in Panel B; the conclusion (rejection at 1%) is unchanged, but the printed p-value is inconsistent with 3 degrees of freedom and should not be memorized.

Step 3: robust standard errors (Exhibit 6, V1 p.59).
- MKTRF SE rises from 0.0601 to 0.0910, a factor of $0.0910 / 0.0601 = 1.514$; robust t $= 1.2414 / 0.0910 = 13.64$.
- SMB SE rises from 0.1042 to 0.1111, factor 1.066; robust t $= 1.0953 / 0.1111 = 9.86$.
- HML SE rises from 0.0872 to 0.1015; robust t $= -0.1065 / 0.1015 = -1.05$, still insignificant.
- The intercept SE falls slightly (0.0024 to 0.0021), a reminder that robust SEs are usually but not always larger.
- Coefficients are unchanged; MKTRF and SMB remain significant, so the substantive conclusion survives the correction.
^ex-01-03-2

**Example 3: Three ESG models, residual plots and BP tests (knowledge check, V1 p.59-61)**

Part 1: residual scatterplots against X1, X2, X3.
- Model A: the spread of residuals narrows dramatically as X1 increases, so heteroskedasticity is an issue (V1 p.60).
- Model B: no discernible pattern, just noise, so no heteroskedasticity issue.
- Model C: the spread widens dramatically in a nonlinear pattern as X3 increases, so both heteroskedasticity and nonlinearity (inappropriate functional form) are present.

Part 2: BP tests at 5% (V1 p.60).

| Model | BP statistic | p-value | Conclusion |
|---|---|---|---|
| A | 7.183 | 0.0072 | Heteroskedastic (p < 0.05) |
| B | 0.035 | 0.8523 | Homoskedastic |
| C | 29.586 | 0.0001 | Heteroskedastic |

Check: each model has one regressor, so $k = 1$ and the 5% critical value is 3.841.
- A: $7.183 > 3.841$, reject; recomputed p-value on 1 df is 0.0074, consistent with the printed 0.0072.
- B: $0.035 < 3.841$, fail to reject; recomputed p-value 0.8516, consistent with 0.8523.
- C: $29.586 > 3.841$, reject; p-value is below 0.0001.

Part 3: effect of White's correction given heteroskedastic residuals (V1 p.61).
- Standard errors increase, t-statistics decrease, p-values increase for the independent variables.
- Coefficients do not change.
^ex-01-03-3

**Example 4: GDP on consumption, Breusch-Godfrey test and Newey-West correction (Exhibits 9 and 10, V1 p.63-64)**

Setup: 30 years of quarterly data, $n = 121$, one regressor (CONS), so $k = 1$.
Panel A (V1 p.63): $R^2 = 0.896$, adjusted 0.895, $F = 1023.0$.
Multiple R check: $\sqrt{0.896} = 0.947$, printed 0.946.

| Variable | Coefficient | SE (OLS) | t (OLS) | p | SE (robust) | t (robust) | p |
|---|---|---|---|---|---|---|---|
| Intercept | 0.0991 | 0.050 | 1.974 | 0.051 | 0.058 | 1.701 | 0.091 |
| CONS | 0.8696 | 0.027 | 31.990 | 0.000 | 0.036 | 24.310 | 0.000 |

Step 1: OLS inference.
- CONS: $0.8696 / 0.027 = 32.2$, printed 31.990 (SE rounded to 3 decimals), significant at 1%.

Step 2: BG test (Panel B, V1 p.63).
- F-statistic 23.6113 with printed p-value 0.0230.
- With $p$ lags the degrees of freedom are $F(p, 121 - p - 1 - 1)$; for $p = 1$ that is $F(1, 118)$ with a 5% critical value of 3.92.
- $23.61$ far exceeds any plausible critical value, so reject $H_0$ of no serial correlation; the printed p-value of 0.0230 is much larger than what an F of 23.6 implies on these degrees of freedom, but the rejection conclusion stands.

Step 3: robust (Newey-West / HAC) standard errors (Exhibit 10, V1 p.64).
- CONS SE rises from 0.027 to 0.036; robust t $= 0.8696 / 0.036 = 24.16$, printed 24.310.
- Intercept SE rises from 0.050 to 0.058; robust t $= 0.0991 / 0.058 = 1.709$, printed 1.701, and the intercept p-value rises from 0.051 to 0.091, so the intercept is no longer close to significant at 5%.
- The 95% interval for CONS widens from [0.816, 0.923] to [0.799, 0.940].
- The reported F-statistic falls from 1023.0 to 591.0 because the robust covariance matrix also feeds the joint test.
- Coefficients are unchanged; serial correlation is not removed, only accounted for (V1 p.64).
^ex-01-03-4

**Example 5: Critical F-values for four BG tests and robust standard errors (knowledge check, V1 p.65)**

Part 1: critical values at 5% and conclusions.

| Model | BG F-statistic | df (num, den) | Critical F (5%) | Serial correlation? |
|---|---|---|---|---|
| A | 5.1634 | 4, 13 | 3.1791 | Yes, $5.16 > 3.18$ |
| B | 22.0560 | 6, 15 | 2.7905 | Yes, $22.06 > 2.79$ |
| C | 2.3400 | 4, 15 | 3.0556 | No, $2.34 < 3.06$ |
| D | 1.9800 | 3, 35 | 2.8742 | No, $1.98 < 2.87$ |

Recomputed with scipy: $F_{0.95}(4,13) = 3.1791$, $F_{0.95}(6,15) = 2.7905$, $F_{0.95}(4,15) = 3.0556$, $F_{0.95}(3,35) = 2.8742$, all matching the curriculum table exactly.
Reading the degrees of freedom: the numerator df is the number of lags $p$ tested, so Model A tests 4 lags and Model B tests 6 lags.

Part 2: robust standard errors (V1 p.65).
- Coefficient standard errors corrected for possible bias from autocorrelation and heteroskedasticity.
- They are larger than OLS standard errors and allow the regression results to be used for statistical inference.
^ex-01-03-5

**Example 6: FSPTX on growth and value indexes, then adding the S&P 500 (V1 p.67-69)**

Setup: 60 monthly returns, $FSPTX_t = b_0 + b_1 SGX_t + b_2 SVX_t + \varepsilon_t$.

Model without SPX (Exhibit 11, V1 p.67):
- $R^2 = 0.1486 / 0.1900 = 0.782$; adjusted $R^2 = 1 - (1 - 0.782)(59/57) = 0.774$, matching.
- $F = 0.0743 / 0.0007 = 106$ by the rounded MS values, or $ (0.1486/2)/(0.0414/57) = 102.3$ using the sums of squares, matching the printed 102.2425.
- SGX: $1.7765 / 0.196 = 9.064$, significant at 1%; SVX: $-0.4488 / 0.196 = -2.290$, printed -2.292, significant at 5%.
- 95% interval for SGX: $1.7765 \pm 2.0025 \times 0.196 = [1.384, 2.169]$, matching.

Model with SPX (Exhibit 12 Panel A, V1 p.68):
- $R^2$ still 0.782, adjusted $R^2 = 1 - (1 - 0.782)(59/56) = 0.770$, matching; $F = (0.1486/3)/(0.0414/56) = 67.0$, printed 66.9683.
- SGX: coefficient 1.5302, SE 6.166, $t = 0.248$, p 0.805.
- SVX: coefficient -0.6686, SE 5.503, $t = -0.121$, p 0.904.
- SPX: coefficient 0.4658, SE 11.657, $t = 0.040$, p 0.968.
- Standard error inflation: SGX $6.166 / 0.196 = 31.5$ times, SVX $5.503 / 0.196 = 28.1$ times.

Correlation matrix (Exhibit 12 Panel B, V1 p.68-69): SPX with SVX 0.96, SPX with SGX 0.97, SVX with SGX 0.87.

VIFs (Exhibit 13, V1 p.69):

| Regressor | VIF with SPX | VIF without SPX |
|---|---|---|
| SGX | 3,863.85 | 3.97 |
| SVX | 3,083.22 | 3.97 |
| SPX | 12,904.81 | - |

Checks:
- Without SPX there are two regressors, so $VIF = 1/(1 - r^2)$ with $r = 0.87$: $1/(1 - 0.7569) = 4.11$; the printed 3.97 implies $r = 0.865$, consistent with 0.87 after rounding.
- With SPX, $VIF = 3{,}863.85$ implies $R_j^2 = 1 - 1/3863.85 = 0.9997$, and $12{,}904.81$ implies 0.9999; SPX is almost an exact linear combination of its own growth and value components.
- Diagnosis: same $R^2$, F still significant, every t-statistic collapsed to insignificance, VIFs far above 10: classic multicollinearity from over-specifying the model (V1 p.68).
- Fix: drop SPX, which returns to the Exhibit 11 model with VIFs below 5.
^ex-01-03-6

**Example 7: CAPEX, ADV, R&D model of ROA and its VIFs (knowledge check, V1 p.69-70)**

Setup: adjusted $R^2 = 86.50\%$, overall $F = 54.4039$.

| Variable | Coefficient | SE | t-stat | p-value | VIF |
|---|---|---|---|---|---|
| Intercept | 4.7022 | 1.2349 | 3.8078 | 0.0010 | - |
| CAPEX | 1.2302 | 0.1056 | 11.6490 | 0.0000 | 1.164 |
| ADV | -0.0371 | 0.1062 | -0.3490 | 0.7304 | 1.068 |
| R&D | 0.1029 | 0.2837 | 0.3628 | 0.7203 | 1.095 |

Checks: $1.2302 / 0.1056 = 11.650$, $-0.0371 / 0.1062 = -0.349$, $0.1029 / 0.2837 = 0.363$, $4.7022 / 1.2349 = 3.808$, all matching.

Part 1: regression results alone (V1 p.70).
- The F-statistic is significant, so at least one slope is non-zero, and CAPEX has a highly significant t-statistic.
- This is not the multicollinearity symptom (significant F with no significant t), so multicollinearity is not a concern.

Part 2: VIF results (V1 p.70).
- All VIFs are well below 5 and close to 1; implied $R_j^2$ values are $1 - 1/1.164 = 0.141$, $1 - 1/1.068 = 0.064$, $1 - 1/1.095 = 0.087$.
- Variances are not inflated, t-statistics are reliable, multicollinearity is not an issue; ADV and R&D are insignificant because they do not explain ROA, not because of collinearity.
^ex-01-03-7

## Item-set patterns

> [!warning] Trap 1: the wrong $R^2$ in the BP statistic
> The vignette gives an Exhibit with both the original regression output and the BP auxiliary regression output, or gives the auxiliary output with Multiple R, $R^2$ and adjusted $R^2$ on adjacent rows.
> Correct approach: $nR^2$ using the plain $R^2$ of the auxiliary regression of squared residuals on the regressors (V1 p.57).
> Distractor built from adjusted $R^2$ (practice problem 1 option A: $96 \times 0.01317 = 1.264$) is tempting because adjusted $R^2$ is what LM02 taught you to prefer.
> Distractor built from the original regression's $R^2$ is tempting because it is the bigger, more familiar number.

> [!warning] Trap 2: unconditional versus conditional heteroskedasticity
> The vignette states that residual variance differs across observations and asks about the consequence.
> Correct approach: ask whether the variance is correlated with the regressors; only conditional heteroskedasticity damages inference (V1 p.56).
> Distractor "standard errors are biased" for unconditional heteroskedasticity is tempting because it is still an assumption violation; the curriculum says it creates no major problems.
> Distractor "coefficients are biased" is tempting because the word bias is everywhere in the module; heteroskedasticity biases standard errors, not coefficients.

> [!warning] Trap 3: direction of the standard error error
> The vignette asks what happens to standard errors, t-statistics and Type I or Type II errors under each violation.
> Correct approach: conditional heteroskedasticity and positive serial correlation understate SE, inflate t, and raise Type I errors (V1 p.57, p.62); multicollinearity overstates SE, deflates t, and raises Type II errors (low power) (V1 p.66).
> Distractor "inflated standard errors" for serial correlation (practice problem 2 option C) is tempting because the multicollinearity row of the summary says inflated.
> Distractor "more Type II errors" for heteroskedasticity is tempting because candidates confuse fewer rejections with too many rejections.

> [!warning] Trap 4: lagged dependent variable decides whether coefficients survive serial correlation
> Exhibit 2 in the practice set gives a column "Independent variable is lagged value of dependent variable: Yes/No" next to the test results.
> Correct approach: with serial correlation, coefficients are invalid only if that column says Yes; otherwise only standard errors are invalid (Exhibit 7, V1 p.61).
> Distractor "valid coefficient estimates" when the column says Yes is tempting because the general rule for serial correlation is that coefficients remain consistent.
> Distractor that ignores the column entirely and treats BG and DW the same is tempting because both test the same thing.

> [!warning] Trap 5: which test, which distribution, which degrees of freedom
> The vignette gives statistics and asks for the critical value or the conclusion.
> Correct approach: BP is chi-square with $k$ regressors as df, one-tailed right (V1 p.57); BG is $F(p, n - p - k - 1)$ where $p$ is the number of lags (V1 p.62); DW is compared with its own table and tests only first-order correlation (V1 p.62); VIF has no distribution, only the 5 and 10 thresholds (V1 p.67).
> Distractor using $k$ as the BG numerator df is tempting because $k$ is the BP df.
> Distractor using a two-tailed chi-square for BP is tempting because the BG alternative is written $\rho_1 \neq 0$.

> [!warning] Trap 6: what robust standard errors do and do not change
> The vignette shows a before-and-after table and asks what changed.
> Correct approach: coefficients are identical, standard errors typically rise, t-statistics fall, p-values rise, the underlying heteroskedasticity or serial correlation is not removed (V1 p.59, p.64).
> Distractor "the coefficients are re-estimated" is tempting because the exhibit is labelled a new regression.
> Distractor "serial correlation is eliminated" is tempting because the correction is called a fix; the curriculum explicitly says it is not eliminated.

> [!warning] Trap 7: pairwise correlation as the multicollinearity detector
> The vignette gives a correlation matrix with modest pairwise correlations plus a VIF table.
> Correct approach: beyond two regressors, low pairwise correlations are not sufficient to rule out multicollinearity; use the VIF (V1 p.66).
> Distractor "no multicollinearity because no pairwise correlation exceeds 0.7" is tempting because it is how Level I taught correlation.
> Distractor that uses the correlation of the regressor with the dependent variable is tempting because that matrix row is also shown.

> [!warning] Trap 8: reading VIF thresholds as a single cutoff
> The vignette gives VIFs such as 3.97, 6.2, 13.4 and asks which variables have multicollinearity issues.
> Correct approach: above 5 means investigate, above 10 means serious and requires correction (V1 p.67); the question wording ("serious", "requires correction", "warrants investigation") selects the threshold.
> Distractor grouping a VIF of 4 with a VIF of 13 (practice problem 3 option B style) is tempting if the candidate uses "above 1" as the cutoff.
> Distractor that treats VIF of exactly 5 as serious is tempting because candidates collapse the two thresholds into one.

> [!warning] Trap 9: the multicollinearity symptom versus the omitted-variable symptom
> Two models are described: one with high $R^2$, significant F and insignificant t-statistics, and one whose residuals are correlated with a variable not in the model.
> Correct approach: the first is multicollinearity (V1 p.66), the second is omitted variable bias (V1 p.52), and their corrections differ (drop or re-proxy a variable versus add the omitted one).
> Distractor recommending "add more variables" for the multicollinearity case is tempting because more variables feels like a richer model; it makes collinearity worse (Exhibit 12, V1 p.68).
> Distractor recommending "drop a variable" for the omitted-variable case is tempting because it is the multicollinearity fix.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM03-Model-Misspecification-Practice-Problems]]

## Cross-links

- [[LM01-Basics-of-Multiple-Regression-and-Underlying-Assumptions]]: supplies the six assumptions whose violations this module diagnoses, and the residual-plot reading skills (residuals versus fitted values and versus each regressor) that Exhibit 3 and the knowledge checks rely on.
- [[LM02-Evaluating-Regression-Model-Fit-and-Interpreting-Model-Results]]: supplies the t-test, F-test, $R^2$ and adjusted $R^2$ machinery; this module explains when those statistics lie (deflated SE under heteroskedasticity and serial correlation, inflated SE under multicollinearity) and why the BP statistic uses unadjusted $R^2$.
- [[LM04-Extensions-of-Multiple-Regression]]: extends the misspecification agenda to influential observations, dummy variables and logistic regression; the outlier and leverage diagnostics there are the other half of the residual analysis started here.
- [[LM05-Time-Series-Analysis]]: serial correlation becomes the central object; autoregressive models, the autocorrelation of residuals test, and ARCH are the time-series versions of the BG test and conditional heteroskedasticity introduced here.
- [[LM06-Backtesting-and-Simulation]]: the out-of-sample principle from Exhibit 1 and the data-pooling warning (structural breaks, regime changes) reappear as backtesting pitfalls and rolling-window design.

## Self-test

**Q1.** An analyst regresses 60 monthly hedge fund returns on four factors, then regresses the squared residuals on the same four factors and obtains $R^2 = 0.14$ and adjusted $R^2 = 0.077$.
At a 5% level, the Breusch-Pagan conclusion is most likely:
A. Reject the null; conditional heteroskedasticity is present because $8.4 > 7.815$.
B. Fail to reject the null; the statistic 8.4 is below the critical value 9.488.
C. Fail to reject the null; the statistic 4.62 is below the critical value 9.488.

**Q2.** A regression of quarterly sales growth on advertising growth includes last quarter's sales growth as a regressor.
A Breusch-Godfrey test with two lags rejects the null at 1%.
The most accurate description of the estimated model is:
A. Coefficients are consistent but standard errors are understated.
B. Coefficients are inconsistent and standard errors are understated.
C. Coefficients are consistent and standard errors are overstated.

**Q3.** An analyst reports that the error variance in her cross-sectional model rises for firms with higher leverage, one of the regressors.
She also notes that the error variance in a second model varies across observations but is unrelated to any regressor.
Which statement is most accurate?
A. Both models require robust standard errors because both violate the constant-variance assumption.
B. Only the first model produces unreliable t-tests; the second exhibits unconditional heteroskedasticity, which creates no major inference problem.
C. Only the second model produces unreliable t-tests because the pattern cannot be modeled.

**Q4.** A four-regressor model has pairwise regressor correlations no larger than 0.45, $R^2 = 0.88$, a significant F-statistic, and no individually significant slope.
The VIF of X3 is 12.6.
The best interpretation is:
A. Multicollinearity is ruled out by the low pairwise correlations, so the insignificant t-statistics reflect irrelevant variables.
B. X3 is approximately a linear combination of the other regressors ($R_3^2 \approx 0.92$), and multicollinearity explains the pattern.
C. The model suffers from omitted variable bias because residuals must be correlated with an excluded regressor.

**Q5.** After applying Newey-West standard errors to a time-series regression, an analyst observes that the slope coefficient is unchanged at 0.42 while its standard error rises from 0.19 to 0.31 with 96 residual degrees of freedom.
At 5%, the slope:
A. Remains significant because the coefficient did not change.
B. Is no longer significant because $t$ falls from 2.21 to 1.35.
C. Cannot be assessed because Newey-West removes the serial correlation and the regression must be re-run.

**Q6.** A Durbin-Watson statistic of 0.90 is reported for a regression with 80 observations and three regressors, none of which is a lagged dependent variable.
The most appropriate conclusion is:
A. Positive first-order serial correlation ($r \approx 0.55$); coefficients remain consistent; standard errors are understated.
B. Negative first-order serial correlation; coefficients are inconsistent.
C. No serial correlation because the statistic is below 2.

**Q7.** In a BG test with $p = 2$ lags on a model with $n = 80$ and $k = 3$ regressors, the F-statistic is 2.85.
The critical value at 5% is closest to $F(2, 74) = 3.12$.
The analyst should conclude:
A. Serial correlation up to order 2 is present because 2.85 exceeds the $F(3, 74)$ critical value.
B. There is insufficient evidence of serial correlation up to order 2 because $2.85 < 3.12$.
C. The BP test should be used instead because the errors are heteroskedastic.

**Q8.** A regression of a technology fund's returns on the S&P 500 growth index and value index gives VIFs of 3.97 for each regressor.
Adding the S&P 500 index itself gives VIFs above 3,000 and leaves $R^2$ unchanged.
The most appropriate correction is:
A. Increase the sample size until the VIFs fall below 5.
B. Drop the S&P 500 index, which is a near-exact linear combination of its growth and value components.
C. Apply White-corrected standard errors so the t-statistics become reliable.

**Q9.** Residuals from a one-factor model of a gold fund show a strong upward linear relationship when plotted against the excess market return, with $R^2 = 0.65$ in that plot.
The scatter of the fund's returns on the model's regressor shows no clear relation.
The misspecification and its effect are best described as:
A. Inappropriate scaling; only the intercept is biased.
B. Omitted variable correlated with the regressor; all coefficients and standard errors are biased and inconsistent.
C. Conditional heteroskedasticity; standard errors are understated but coefficients are consistent.

**Q10.** An analyst wishes only to forecast next month's portfolio return from a five-factor model with two VIFs above 10.
Which statement best reflects the curriculum?
A. Multicollinearity may not be a major issue because the goal is prediction rather than interpreting individual coefficients.
B. The model cannot be used until the VIFs are reduced below 5.
C. Robust standard errors should be applied because multicollinearity biases the standard errors downward.

> [!success]- Answer key
> **Q1: B.** $nR^2 = 60 \times 0.14 = 8.4$ with $k = 4$ df; the 5% critical value is 9.488, so fail to reject. A uses the $k = 3$ critical value of 7.815. C uses adjusted $R^2$ ($60 \times 0.077 = 4.62$), which is not the BP statistic.
> **Q2: B.** A lagged dependent variable plus serial correlation makes all coefficients inconsistent (Exhibit 7, V1 p.61), and serial correlation understates standard errors (V1 p.62). A is the no-lagged-dependent-variable case. C describes multicollinearity.
> **Q3: B.** Variance correlated with a regressor is conditional heteroskedasticity, which biases standard errors; variance unrelated to regressors is unconditional and creates no major problem (V1 p.56). A over-treats; C reverses the two.
> **Q4: B.** $R_3^2 = 1 - 1/12.6 = 0.921$; high $R^2$, significant F, insignificant t-statistics is the classic symptom (V1 p.66), and pairwise correlations are not a sufficient screen beyond two regressors. A is the pairwise trap. C has no evidence in the stem.
> **Q5: B.** $0.42/0.19 = 2.21 > 1.985$ (5% two-tailed, 96 df) but $0.42/0.31 = 1.35 < 1.985$. A ignores that significance depends on the standard error. C is wrong because robust standard errors do not remove serial correlation and no re-estimation of coefficients occurs (V1 p.64).
> **Q6: A.** $DW \approx 2(1 - r)$ gives $r \approx 1 - 0.90/2 = 0.55$, positive serial correlation; without a lagged dependent variable coefficients are consistent and standard errors understated (V1 p.61-62). B has the wrong sign and wrong coefficient conclusion. C misreads DW, for which 2 means no correlation.
> **Q7: B.** BG is $F(p, n - p - k - 1) = F(2, 74)$; $2.85 < 3.12$ so fail to reject. A uses $k$ as the numerator df, which is the BP degrees of freedom. C confuses the tests.
> **Q8: B.** Dropping the redundant regressor is the direct cure (V1 p.68-69). A is a listed remedy but cannot fix a near-exact linear dependence. C addresses heteroskedasticity, not multicollinearity; robust SEs do not shrink inflated variances.
> **Q9: B.** Residuals explained by an excluded variable signal omitted variable bias; a correlated omission biases every coefficient and the standard errors (V1 p.52, p.54). A misidentifies the failure and the effect. C describes a different violation; heteroskedasticity is a variance pattern, not a linear residual relationship with an excluded variable.
> **Q10: A.** The curriculum states that if the goal is only to predict the dependent variable, multicollinearity may not be a major issue (V1 p.69). B invents a rule. C is wrong because multicollinearity inflates rather than deflates standard errors and robust SEs are not the remedy.

## Flashcards

#flashcards/cfa-l2/01-Quantitative-Methods/lm03

Breusch-Pagan test statistic::$nR^2$ where $R^2$ is from regressing squared residuals on the original regressors; chi-square with $k$ df; one-tailed right (V1 p.57)
Breusch-Godfrey test distribution::$F(p, n - p - k - 1)$ where $p$ is the number of residual lags and $k$ the number of regressors (V1 p.62)
Variance inflation factor formula::$VIF_j = 1/(1 - R_j^2)$, with $R_j^2$ from regressing $X_j$ on the other regressors (V1 p.66)
VIF rules of thumb::Above 5 warrants investigation; above 10 indicates serious multicollinearity requiring correction (V1 p.67)
Minimum possible VIF::1, when $R_j^2 = 0$ and $X_j$ is uncorrelated with the other regressors (V1 p.66)
Five principles of proper model specification::Economic reasoning, parsimony, good out-of-sample performance, appropriate functional form, no violations of regression assumptions (V1 p.51)
Four failures in regression functional form::Omitted variables, inappropriate form of variables, inappropriate variable scaling, inappropriate data pooling (V1 p.51)
Omitted variable uncorrelated with the included regressor::Intercept biased, slope on the included regressor still correct, residual has non-zero mean (V1 p.52)
Omitted variable correlated with the included regressor::All coefficients, residuals and standard errors biased and inconsistent (V1 p.52)
Unconditional heteroskedasticity::Error variance not correlated with the regressors; violates an assumption but creates no major inference problems (V1 p.56)
Conditional heteroskedasticity::Error variance correlated with the values of the regressors; standard errors understated, t-statistics inflated, more Type I errors (V1 p.56-57)
Effect of conditional heteroskedasticity on the F-test::Unreliable because MSE becomes a biased estimator of the population error variance (V1 p.56-57)
Robust standard errors, other names::Heteroskedasticity-consistent or White-corrected standard errors (V1 p.59)
Serial-correlation corrections, other names::Serial-correlation consistent, Newey-West, HAC (heteroskedasticity- and autocorrelation-consistent) standard errors (V1 p.64)
Do robust standard errors change the coefficients?::No; coefficients are identical, only the standard errors, t-statistics and p-values change (V1 p.59, p.64)
Does a Newey-West correction eliminate serial correlation?::No; the serial correlation remains, the standard errors now account for it (V1 p.64)
Serial correlation with no lagged dependent variable regressor::Coefficients consistent, standard errors invalid (Exhibit 7, V1 p.61)
Serial correlation with a lagged dependent variable regressor::All coefficients inconsistent and standard errors invalid (Exhibit 7, V1 p.61)
Positive serial correlation, definition::A positive residual raises the chance of a positive residual in the next observation; residual signs persist (V1 p.61-62)
Effect of positive serial correlation on the F-statistic::Inflated, because MSE underestimates the population error variance (V1 p.62)
Durbin-Watson test limitation::Tests only first-order serial correlation; BG detects correlation up to order $p$ (V1 p.62)
Durbin-Watson value with no first-order serial correlation::Approximately 2; below 2 indicates positive, above 2 negative serial correlation (V1 p.62, formula 6)
Multicollinearity, effect on coefficients and standard errors::Coefficients consistent but imprecise; standard errors inflated; t-statistics diminished; low power (V1 p.66)
Classic multicollinearity symptom::High $R^2$ and significant F-statistic with individually insignificant t-statistics (V1 p.66)
Why pairwise correlations are inadequate for detecting multicollinearity::With more than two regressors, a linear combination of several regressors can be highly collinear while pairwise correlations are low (V1 p.66)
Three corrections for multicollinearity::Exclude one or more variables, use a different proxy for a variable, increase the sample size (V1 p.69)
When multicollinearity may not matter::When the goal is only to predict the dependent variable, not to interpret individual regressors (V1 p.69)
Type of error raised by heteroskedasticity and serial correlation::Type I (rejecting a true null) because t-statistics are inflated (V1 p.57, p.62)
Type of error raised by multicollinearity::Type II (failing to reject a false null) because t-tests have little power (V1 p.66)
Exhibit 14 correction for heteroskedasticity::Revise the model; use robust standard errors (V1 p.70)
Exhibit 14 correction for serial correlation::Revise the model; use serial-correlation consistent standard errors (V1 p.70)
Exhibit 14 correction for multicollinearity::Revise the model; increase sample size (V1 p.70)
Market efficiency and residual patterns::Under weak-form efficiency, heteroskedasticity and serial correlation should not appear in financial data; if found, they are exploitable predictability (V1 p.59, p.62, p.65)
Scatterplot signature of inappropriate data pooling::Discrete, widely separated clusters with little correlation within each (V1 p.52)
Fix for a nonlinear relation that is linear in proportional changes::Take the natural logarithm of the variable (V1 p.52)
Fix for comparing companies of different sizes::Scale variables, for example common-size financial statements (V1 p.52)
The BP test is {{one-tailed, right-side}} with {{$k$}} degrees of freedom where $k$ is the number of {{independent variables in the original regression}}.
The dependent variable in the BP auxiliary regression is the {{squared residual}}; in the BG auxiliary regression it is the {{residual}} itself.
With exactly two regressors correlated at $r$, both VIFs equal {{$1/(1-r^2)$}}.
Micro-problem: $n = 96$, auxiliary $R^2 = 0.06511$, 5 regressors, 5% critical 11.07; conclusion?
?
$96 \times 0.06511 = 6.251 < 11.07$; fail to reject; no evidence of conditional heteroskedasticity (V1 p.73). Keystrokes: `96 × 0.06511 =`

Micro-problem: $R_j^2 = 0.942$; VIF and verdict?
?
$1/(1 - 0.942) = 17.24 > 10$; serious multicollinearity, requires correction (V1 p.67). Keystrokes: `0.942 +/- + 1 = 1/x`

Micro-problem: VIF = 6.25; implied $R_j^2$ and verdict?
?
$R_j^2 = 1 - 1/6.25 = 0.84$; above 5 but below 10, warrants investigation (V1 p.67). Keystrokes: `6.25 1/x +/- + 1 =`

Micro-problem: BG F = 5.16 with df (4, 13), 5% critical 3.18; conclusion?
?
$5.16 > 3.18$; reject; serial correlation up to lag 4 is present (V1 p.65)

Micro-problem: coefficient 1.2414, OLS SE 0.0601, robust SE 0.0910; robust t?
?
$1.2414 / 0.0910 = 13.64$, down from $20.66$; still significant (V1 p.59)

Micro-problem: DW = 3.088; sign and approximate size of first-order autocorrelation?
?
$r \approx 1 - 3.088/2 = -0.54$; negative serial correlation (V1 p.71, formula 6)

Which answer is the trap: BP statistic computed with adjusted $R^2$?
?
It is the trap; BP uses the unadjusted $R^2$ of the auxiliary regression. In practice problem 1, $96 \times 0.01317 = 1.264$ is the distractor and $96 \times 0.06511 = 6.251$ is correct (V1 p.73)

Which answer is the trap: "serial correlation inflates standard errors"?
?
Trap; serial correlation deflates (understates) standard errors and inflates t-statistics. Inflated standard errors belong to multicollinearity (V1 p.62, p.66)

Which answer is the trap: "add another index to the regression to improve fit" when the index is a combination of existing regressors?
?
Trap; it introduces severe multicollinearity, leaves $R^2$ unchanged and destroys the t-statistics (Exhibit 12, V1 p.68)

Which test applies: residual variance appears to grow with a regressor?
?
Breusch-Pagan; $nR^2$ versus chi-square with $k$ df; fix with White standard errors (V1 p.57, p.59)

Which test applies: residuals from a quarterly time-series model show persistent signs?
?
Breusch-Godfrey (or Durbin-Watson for first order only); F with $(p, n - p - k - 1)$ df; fix with Newey-West standard errors (V1 p.62, p.64)

Which test applies: high $R^2$, significant F, no significant t-statistics?
?
Variance inflation factor; no hypothesis test, compare with 5 and 10; fix by dropping a variable, re-proxying, or enlarging the sample (V1 p.66-69)

## Common mistakes

1. Using adjusted $R^2$, or the original regression's $R^2$, in the BP statistic instead of the unadjusted $R^2$ of the squared-residual auxiliary regression (V1 p.57, p.73).
2. Treating the BP test as two-tailed; it is a one-tailed, right-side chi-square test with $k$ degrees of freedom (V1 p.57).
3. Using $k$ (number of regressors) as the numerator degrees of freedom of the BG F-test; the numerator df is $p$, the number of lags, and the denominator is $n - p - k - 1$ (V1 p.62).
4. Saying heteroskedasticity or serial correlation biases the coefficients; they bias the standard errors, and coefficients become inconsistent only when a lagged dependent variable is a regressor under serial correlation, or when a correlated variable is omitted (V1 p.52, p.57, p.61).
5. Getting the direction backwards: heteroskedasticity and serial correlation understate standard errors and inflate t-statistics (Type I errors); multicollinearity inflates standard errors and deflates t-statistics (low power) (V1 p.57, p.62, p.66).
6. Treating unconditional heteroskedasticity as an inference problem; only conditional heteroskedasticity, where variance is correlated with the regressors, damages tests (V1 p.56).
7. Believing robust or Newey-West standard errors change the coefficient estimates or eliminate the serial correlation; only the standard errors, t-statistics and p-values change, and the correlation remains (V1 p.59, p.64).
8. Screening for multicollinearity with pairwise correlations when there are more than two regressors; low pairwise correlations do not rule it out, the VIF does (V1 p.66).
9. Collapsing the VIF thresholds into one cutoff; above 5 is investigate, above 10 is serious and requires correction (V1 p.67).
10. Recommending "add more variables" as a cure for multicollinearity; adding a variable that is a combination of existing regressors makes it worse (Exhibit 12, V1 p.68), and the listed cures are drop a variable, change a proxy, or increase the sample (V1 p.69).
11. Confusing the omitted-variable signature (residuals linearly related to an excluded variable) with the heteroskedasticity signature (residual spread changing with a regressor) or the pooling signature (separated clusters) (V1 p.52-54, p.60).
12. Forgetting the Durbin-Watson limitation: it detects only first-order serial correlation, which is why the curriculum prefers Breusch-Godfrey (V1 p.62).
13. Forgetting that the module's first correction for every violation is to revise the model; robust standard errors are the second line, not a substitute for a well-specified model (Exhibit 14, V1 p.70).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "01-03" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
