---
type: cfa-lm
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
volume: 1
lm: 1
title: "Basics of Multiple Regression and Underlying Assumptions"
pages: "3-24"
weight_band: "5-10%"
difficulty: 2
los_count: 3
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/quantitative-methods]
---

# LM1: Basics of Multiple Regression and Underlying Assumptions

Difficulty 2 of 5: almost no arithmetic, but the exam punishes sloppy language about "holding other variables constant", which chart tests which assumption, and the difference between pairwise and partial relationships.

## LOS map

- **describe** the types of investment problems addressed by multiple linear regression and the regression process (V1 p.5) ^los-01-01-a
    - Examiner asks: given a vignette describing a dependent variable and a diagnostic result, pick the next step in the Exhibit 2 flowchart (logistic vs linear, adjust and re-estimate, or use the model).
- **formulate** a multiple linear regression model, describe the relation between the dependent variable and several independent variables, and interpret estimated regression coefficients (V1 p.8) ^los-01-01-b
    - Examiner asks: interpret an intercept or a partial slope in words with the "holding all other independent variables constant" clause, or plug given X values into the estimated equation to get a predicted Y.
- **explain** the assumptions underlying a multiple linear regression model and interpret residual plots indicating potential violations of these assumptions (V1 p.10) ^los-01-01-c
    - Examiner asks: match a named chart (pairs plot, residuals vs predicted, residuals vs X, normal Q-Q) to the assumption it diagnoses, or read a described pattern and name the violated assumption.

## Core intuition

> [!abstract] The whole module in one sentence
> Multiple regression explains the variation of one dependent variable with the variation of several independent variables, and every slope is a partial effect: the change in Y for a one-unit change in that X while the other Xs are frozen (V1 p.8).

### Why more than one X

Financial outcomes rarely have a single driver.
A stock's excess return responds to the market, to size, to value, to profitability and to investment aggressiveness at the same time, which is exactly what the Fama-French five-factor model tries to capture (V1 p.5).
A one-factor regression would push all of the omitted drivers into the error term and would attribute to the single included factor whatever it happens to share with the excluded ones.
Multiple regression lets the analyst untangle those shared movements and ask a sharper question: what does this factor do on its own, once the others are accounted for?
The curriculum gives three canonical uses: understanding return drivers (a factor model), predicting a binary event such as financial distress from leverage, profitability, growth and market share, and measuring the effect of country-risk dimensions on equity returns (V1 p.5).
The introduction warns just as clearly about the downside: used incorrectly, multiple regression yields spurious relationships, poor predictions and a misleading picture of the drivers (V1 p.3).
The software does the estimation; the analyst's job is specification and interpretation (V1 p.3).

### The regression process as a decision tree

Exhibit 2 is a flowchart and the exam tests it as a flowchart (V1 p.6).
The first fork is the nature of the dependent variable.
If Y is continuous, such as a return, ordinary multiple linear regression is the starting point.
If Y is discrete, such as a 0/1 flag for takeover target or not, the model is a logistic regression instead (V1 p.5).
After estimation the analyst looks at the residuals and asks whether the assumptions hold.
If they do not, the answer is never "report anyway"; it is "adjust the model and re-estimate" (V1 p.7).
Only after the assumptions pass does the analyst look at goodness of fit, ask whether the overall fit is significant, and ask whether this is the best of the candidate models.
A model that fails any of those tests loops back to adjustment.
A model that passes every gate is used for analysis and prediction (V1 p.6).
Notice the ordering: assumptions are checked before fit, because fit statistics are meaningless if the assumptions that give them their distributions are broken.
The independent variables in the specification may be continuous, such as financial ratios, or discrete dummy variables indicating membership in a class such as an industry (V1 p.5).

### What the equation says

The model is $Y_i = b_0 + b_1 X_{1i} + \dots + b_k X_{ki} + \varepsilon_i$ over $n$ observations, and $n$ must exceed $k$ (V1 p.8).
The terms in the $X$s are the deterministic part; the error $\varepsilon_i$ is the stochastic part (V1 p.8).
The target is the same as in simple regression: explain the variation of $Y$, meaning the sum of squared deviations of $Y$ from its mean, which is the sum of squares total (V1 p.8).
The intercept $b_0$ is the expected value of $Y$ when every independent variable is zero (V1 p.4).
That reading is mechanical and sometimes economically silly, for example a positive alpha when all factor returns are zero, but it is the reading the exam wants.

> [!abstract] Partial means "holding the others constant"
> A slope $b_j$ in multiple regression is a partial regression coefficient: the change in $Y$ for a one-unit change in $X_j$ with all other independent variables held constant (V1 p.8).
> Every coefficient interpretation on the exam must carry that clause, and a slope from a multiple regression is not the same number you would get from regressing $Y$ on $X_j$ alone.

The bond example makes the partial idea concrete (V1 p.8).
Regressing monthly bond index excess returns on the change in government yields and the change in credit spreads gives $RET = 0.0023 - 5.0585\,BY - 2.1901\,CS$.
The slope on yields, $-5.0585$, is an empirical duration: a one-unit rise in yields lowers the index return by 5.0585 units with spreads unchanged (V1 p.8).
The spread slope is the same idea for credit: a one-unit widening costs 2.1901 units of return with yields unchanged.
Because both drivers are in the model, neither coefficient is contaminated by the fact that yields and spreads tend to move together.

### Why pairwise pictures can lie

The ABC stock example contains the most examinable subtlety in the module (V1 p.12).
In the scatterplot matrix, ABC's excess return shows no visible relation to the size factor SMB, yet in the regression SMB has a t-statistic of $-2.19$ and is significant (V1 p.12).
The scatterplot compares two variables in isolation; the regression coefficient is a partial effect after controlling for the market and value factors.
A factor can be irrelevant in isolation and important once the others are held fixed, or the reverse.
That is why pairwise plots are used for spotting non-linearity and outliers, not for deciding which variables belong in the model (V1 p.4).
The pairs plot also shows the correlation among the independent variables; SMB and HML have a nearly flat fitted line, which is the desirable case, because near-linear dependence among the $X$s makes coefficients hard to interpret (V1 p.12).

### The five assumptions and why each exists

Ordinary least squares gives valid inference only if five assumptions hold (V1 p.10).
Linearity: the relationship between $Y$ and the $X$s is linear, otherwise a straight-line model systematically misses, and the residuals curve against the fitted values.
Homoskedasticity: the residual variance is the same for every observation, otherwise the standard errors that feed every t-test and F-test are wrong.
Independence of errors: observations are independent, so residuals are uncorrelated across observations; with time-series data this is the assumption most often broken.
Normality: residuals are normally distributed, which is what justifies using t and F distributions in small samples.
Independence of independent variables, in two parts: the $X$s are not random, and there is no exact linear relation among the $X$s or combinations of them (V1 p.10).
The last assumption is the one that decides whether the model can be estimated at all.
An exact linear relation makes estimation impossible; an approximate one, signalled by significant pairwise correlations among the $X$s, lets the model be estimated but makes the coefficients hard to interpret (V1 p.10).
The tools to test and fix violations are deferred to later modules; here the task is to recognise them in pictures (V1 p.10).

> [!abstract] Each diagnostic plot answers one question
> Pairs plot: are the relationships linear and are there outliers?
> Residuals vs predicted: is the spread constant, and where are the outliers?
> Residuals vs one $X$: does that variable still explain the leftovers, which would mean misspecification, and are there extreme $X$ values?
> Normal Q-Q: are the residuals normal, or fat-tailed? (V1 pp.13-18)

### Reading the residual plots

The residuals-versus-predicted plot for ABC shows a cloud centred on zero with no direction and no fanning, which supports constant variance and uncorrelated errors (V1 p.13).
Three points, months 7, 25 and 95, sit far from the cloud and are flagged as potential outliers; the analyst's response is to look for shocks in those months from factors the model omits (V1 p.14).
The residuals-versus-factor plots in Exhibit 6 show the same three outliers and no directional pattern against any factor, which supports the linearity assumption for each $X$ (V1 p.14).
The normal Q-Q plot compares the standardized residuals to a standard normal; if the residuals are normal they lie on the diagonal, and the 5th percentile residual should sit near $-1.65$ standard deviations (V1 p.16).
For ABC, observations 25 and 95 fall well below the line beyond $-2$ and observation 7 sits above it near $+2.5$, but the bulk of the points track the diagonal, so the error term is judged close to normal (V1 p.17).
The CRYPTO knowledge check shows the opposite picture: departures from the diagonal past $\pm 2$ standard deviations mean fat tails, a routine feature of financial time series (V1 p.19).

## Formulas and derivations

**Variation of Y (sum of squares total)** (V1 p.8)
$$ \text{Variation of } Y = \sum_{i=1}^{n} \left(Y_i - \bar{Y}\right)^2 $$
^f-01-01-1

- $Y_i$: observed dependent variable, in the units of $Y$ (percent, dollars, and so on).
- $\bar{Y}$: sample mean of $Y$; $n$: number of observations.
- This is what the regression is trying to explain; it splits into an explained part and a residual part, which LM02 uses for $R^2$ and the F-test.
- Squaring makes deviations above and below the mean count equally, so the total is never negative and is zero only if every $Y_i$ equals the mean.

**Simple linear regression model** (V1 p.8)
$$ Y_i = b_0 + b_1 X_i + \varepsilon_i, \quad i = 1, 2, \dots, n $$
^f-01-01-2

- $b_0$: intercept; $b_1$: slope; $\varepsilon_i$: error term for observation $i$.
- One independent variable explains $Y$; the multiple model generalises this by adding regressors.

**Multiple linear regression model, Equation (1)** (V1 p.8)
$$ Y_i = b_0 + b_1 X_{1i} + b_2 X_{2i} + b_3 X_{3i} + \dots + b_k X_{ki} + \varepsilon_i, \quad i = 1, 2, \dots, n $$
^f-01-01-3

- $X_{ji}$: value of independent variable $j$ for observation $i$, $j = 1, \dots, k$.
- $b_0$: intercept, the expected $Y$ when all $X_j = 0$ (V1 p.4).
- $b_j$: partial slope coefficient on $X_j$ (V1 p.8).
- $\varepsilon_i$: stochastic error; the $X$ terms are the deterministic part.
- Constraint: $n > k$, otherwise there are not enough observations to pin down the $k+1$ coefficients (V1 p.8).

**Estimated (fitted) regression equation** (V1 p.8)
$$ \hat{Y}_i = \hat{b}_0 + \hat{b}_1 X_{1i} + \hat{b}_2 X_{2i} + \dots + \hat{b}_k X_{ki} $$
^f-01-01-4

- Hats mark estimates obtained by OLS from the sample; there is no error term because $\hat{Y}_i$ is the fitted value, not the observation.
- The residual is the gap between the observation and the fit, defined next.

**Residual** (V1 p.13)
$$ e_i = Y_i - \hat{Y}_i $$
^f-01-01-5

- $e_i$: sample residual, the estimate of the unobservable $\varepsilon_i$.
- The curriculum plots $e_i$ against $\hat{Y}_i$ and against each $X_j$; the definition is implicit in those plots (V1 p.13).
- Residuals, not errors, are what you can actually inspect, so every diagnostic in this module is a picture of $e_i$.

**Partial slope interpretation** (V1 p.8)
$$ b_j = \frac{\Delta Y}{\Delta X_j}\bigg|_{\text{all other } X \text{ held constant}} $$
^f-01-01-6

- $b_j$ has units of ($Y$ units) per ($X_j$ unit).
- Reason: differencing Equation (1) with only $X_j$ changing by one unit leaves $\Delta Y = b_j$, because every other term is unchanged and the error is zero in expectation.
- Sign convention: negative $b_j$ means $Y$ falls when $X_j$ rises, other things equal.

**Prediction from the estimated equation** (V1 p.8)
$$ \hat{Y} = \hat{b}_0 + \sum_{j=1}^{k} \hat{b}_j X_j^{*} $$
^f-01-01-7

- $X_j^{*}$: the given scenario values of each independent variable, in the same units the model was estimated in.
- Bond example: $0.0023 - 5.0585(0.005) - 2.1901(0.001) = -0.0252$ (V1 p.8).

> [!tip] Calculator
> BA II Plus, chain arithmetic: `0.0023 - 5.0585 x 0.005 = ` then `- 2.1901 x 0.001 =`.
> Because the BA II Plus in chain mode evaluates left to right, key each product first: `5.0585 x 0.005 = STO 1`, `2.1901 x 0.001 = STO 2`, then `0.0023 - RCL 1 - RCL 2 =` gives $-0.0252$.

**Empirical duration from a yield-change slope** (V1 p.8)
$$ \hat{b}_{BY} = -D_{\text{emp}} \quad \Rightarrow \quad D_{\text{emp}} = 5.0585 $$
^f-01-01-8

- $BY$: change in government bond yield; $RET$: bond index excess return.
- Duration is the proportional price change per unit yield change with the opposite sign, so a return-on-yield-change slope of $-5.0585$ is an empirical duration of 5.0585 (V1 p.8).

**Homoskedasticity assumption** (V1 p.10)
$$ \operatorname{Var}(\varepsilon_i) = \sigma^2_{\varepsilon} \quad \text{for all } i $$
^f-01-01-9

- $\sigma^2_{\varepsilon}$: a single constant error variance, in squared $Y$ units.
- Violation, heteroskedasticity, shows as fanning or clustering in the residuals-versus-predicted plot (V1 p.18).

**Independence of errors assumption** (V1 p.10)
$$ \operatorname{Cov}(\varepsilon_i, \varepsilon_j) = 0 \quad \text{for } i \neq j $$
^f-01-01-10

- Observations are independent, so residuals are uncorrelated across observations.
- With time series this is the serial-correlation question that LM03 tests formally.

**Normality assumption** (V1 p.10)
$$ \varepsilon_i \sim N\!\left(0, \sigma^2_{\varepsilon}\right) $$
^f-01-01-11

- Combined with the two assumptions above, the errors are independent and identically normal.
- Checked with the normal Q-Q plot; under normality 5% of standardized residuals fall below $-1.65$ (V1 p.16).

**No exact linear relation among independent variables** (V1 p.10)
$$ \text{No constants } c_0, c_1, \dots, c_k \text{ (not all zero) with } c_0 + c_1 X_{1i} + \dots + c_k X_{ki} = 0 \ \forall i $$
^f-01-01-12

- Assumption 5b; an exact relation makes the coefficients unidentifiable, so the model cannot be estimated (V1 p.10).
- An approximate relation, flagged by significant pairwise correlations among the $X$s, allows estimation but muddies interpretation (V1 p.10).

**Standardized residual for the Q-Q plot** (V1 p.16)
$$ z_i = \frac{e_i}{s_e} $$
^f-01-01-13

- $s_e$: standard error of the estimate, the sample standard deviation of the residuals (0.0628 for ABC, V1 p.12).
- The Q-Q plot puts $z_i$ on the vertical axis against the theoretical standard normal quantile on the horizontal axis; normal residuals line up on the diagonal (V1 p.16).

**Reading the software output: coefficient t-statistic** (V1 p.12)
$$ t_{\hat{b}_j} = \frac{\hat{b}_j - 0}{s_{\hat{b}_j}} $$
^f-01-01-14

- $s_{\hat{b}_j}$: standard error of the coefficient; degrees of freedom $n - k - 1 = 116$ for ABC.
- Exhibit 4: MKTRF $1.2889 / 0.1538 = 8.38$; SMB $-0.5841 / 0.2664 = -2.19$; HML $-0.6810 / 0.2231 = -3.05$ (V1 p.12).
- Formal testing belongs to LM02; here you only need to read the column and recognise which factors are significant.

**Reading the software output: coefficient of determination and adjusted version** (V1 p.12)
$$ R^2 = \frac{SS_{\text{regression}}}{SS_{\text{total}}}, \qquad \bar{R}^2 = 1 - (1 - R^2)\frac{n-1}{n-k-1} $$
^f-01-01-15

- Exhibit 4: $0.2914 / 0.7489 = 0.3891$; adjusted $1 - 0.6109 \times 119/116 = 0.3733$ (V1 p.12).
- Multiple R is $\sqrt{R^2} = 0.6238$.

**Reading the software output: standard error of the estimate and F-statistic** (V1 p.12)
$$ s_e = \sqrt{\frac{SS_{\text{residual}}}{n-k-1}}, \qquad F = \frac{SS_{\text{regression}}/k}{SS_{\text{residual}}/(n-k-1)} $$
^f-01-01-16

- Exhibit 4: $s_e = \sqrt{0.4575/116} = 0.0628$; $F = 0.0971 / 0.0039 = 24.63$ with $(3, 116)$ degrees of freedom (V1 p.12).
- These are shown here so the ABC output is fully readable; derivations and hypothesis tests are in LM02.

## Worked examples

### Example 1: Regression process knowledge check (V1 p.7)

Setting: a junior analyst must pick the action for four situations, using the Exhibit 2 flowchart.

| Issue | Where in the flowchart | Action |
|---|---|---|
| Dependent variable is 1 if merger target, 0 otherwise | First fork: Y is not continuous | Use logistic regression |
| Five independent variables, none significant | "Is the overall fit significant?" answered NO | Adjust the model and re-estimate |
| Residuals not homoskedastic | "Are the assumptions satisfied?" answered NO | Adjust the model and re-estimate |
| Assumptions hold, fit significant, best of the candidates | All gates passed | Use the model for analysis and prediction |

Reasoning: every NO in Exhibit 2 routes back to "adjust the model", and only the discrete-Y fork routes to a different estimator (V1 p.6).
^ex-01-01-1

### Example 2: Bond index regression interpretation (V1 p.8)

Given: $RET = 0.0023 - 5.0585\,BY - 2.1901\,CS$, 60 monthly observations, where $BY$ is the change in government bond yields and $CS$ the change in investment-grade credit spreads.

Step 1, intercept.
If $BY = CS = 0$ the index earns 0.0023% per month on average.
Annualised by simple multiplication: $0.0023 \times 12 = 0.0276\%$, which the curriculum rounds to approximately 0.028% (V1 p.8).

Step 2, yield slope.
A one-unit change in $BY$ changes $RET$ by $-5.0585$ with $CS$ constant, so the empirical duration is 5.0585 (V1 p.8).

Step 3, spread slope.
A one-unit widening in $CS$ changes $RET$ by $-2.1901$ with $BY$ constant (V1 p.8).

Step 4, prediction for $BY = 0.005$, $CS = 0.001$.
$5.0585 \times 0.005 = 0.0252925$.
$2.1901 \times 0.001 = 0.0021901$.
$RET = 0.0023 - 0.0252925 - 0.0021901 = -0.0251826$.
Rounded: $-0.0252$, or $-2.52\%$, matching the curriculum (V1 p.8).
^ex-01-01-2

### Example 3: Fama-French three-factor knowledge check (V1 p.9)

Given: $RETRF = 1.5324 + 0.5892\,MKTRF - 0.8719\,SMB - 0.0560\,HML$, returns in whole percentages.

Part 1, intercept.
With $MKTRF = SMB = HML = 0$ the expected portfolio excess return is 1.5324% (V1 p.9).

Part 2, slopes, each with the others held constant.
MKTRF up 1% raises the portfolio return by 0.5892%.
SMB up 1% lowers it by 0.8719%.
HML up 1% lowers it by 0.0560% (V1 p.9).

Part 3, prediction for $MKTRF = 1$, $SMB = 4$, $HML = -2$.
$0.5892 \times 1 = 0.5892$.
$0.8719 \times 4 = 3.4876$.
$-0.0560 \times (-2) = +0.1120$.
$\hat{R} = 1.5324 + 0.5892 - 3.4876 + 0.1120 = -1.2540$.

Discrepancy note: the curriculum solution writes $R = 1.534 + 0.5892 - 0.8719(4) - 0.0560(-2) = -1.2524$ (V1 p.9).
That line uses 1.534 for the intercept, which is a typo for the stated 1.5324; with the correct intercept the answer is $-1.2540\%$.
The method is identical and the difference (0.0016) is immaterial, but if an exam option shows $-1.25$, it is consistent with either version.
^ex-01-01-3

### Example 4: Reading the ABC scatterplot matrix (V1 pp.11-12)

Setting: 120 monthly excess returns of ABC stock regressed on MKTRF, SMB and HML; the pairs plot shows every pairwise scatter, fitted line with 95% band, and a histogram of each variable on the diagonal (V1 p.11).

Observation 1: ABC_RETRF vs MKTRF slopes upward, a positive relation (V1 p.12).

Observation 2: ABC_RETRF vs SMB looks flat.
Yet SMB is significant in the regression (t = $-2.19$, p = 0.0304).
Reconciliation: the scatterplot is a pairwise, unconditional picture; the regression coefficient is partial, after controlling for MKTRF and HML (V1 p.12).

Observation 3: ABC_RETRF vs HML slopes downward, a negative relation, consistent with the estimated HML coefficient of $-0.6810$ (V1 p.12).

Observation 4: SMB vs HML is nearly flat, so the two explanatory variables are close to uncorrelated, which is desirable for assumption 5b (V1 p.12).

Observation 5: because every point is plotted, the matrix also flags extreme values and outliers (V1 p.12).
^ex-01-01-4

### Example 5: Reconstructing Exhibit 4, the ABC regression output (V1 p.12)

Given: $n = 120$, $k = 3$, $SS_{\text{regression}} = 0.2914$, $SS_{\text{residual}} = 0.4575$, $SS_{\text{total}} = 0.7489$.

Degrees of freedom: regression $k = 3$; residual $n - k - 1 = 116$; total $n - 1 = 119$; check $0.2914 + 0.4575 = 0.7489$.

$R^2 = 0.2914 / 0.7489 = 0.3891$; multiple R $= \sqrt{0.3891} = 0.6238$.

Adjusted $R^2 = 1 - (1 - 0.3891)(119/116) = 1 - 0.6109 \times 1.02586 = 0.3733$.

$MS_{\text{regression}} = 0.2914 / 3 = 0.0971$; $MS_{\text{residual}} = 0.4575 / 116 = 0.00394$, displayed as 0.0039.

$F = 0.0971 / 0.00394 = 24.63$, matching the reported 24.6278.

Standard error $= \sqrt{0.00394} = 0.0628$.

t-statistics from the coefficient columns: intercept $0.0052 / 0.0061 = 0.85$; MKTRF $1.2889 / 0.1538 = 8.38$; SMB $-0.5841 / 0.2664 = -2.19$; HML $-0.6810 / 0.2231 = -3.05$.
Small differences in the third decimal versus the exhibit (0.8435, 8.3791, $-2.1922$, $-3.0523$) come from the exhibit rounding the standard errors to four places.

95% intervals with $t_{0.025,116} = 1.981$: MKTRF $1.2889 \pm 1.981 \times 0.1538 = (0.984, 1.594)$, matching the exhibit's $(0.9842, 1.5935)$.

Conclusion: MKTRF, SMB and HML are all significant at 5% (p-values 0.0000, 0.0304, 0.0028); the intercept is not (p = 0.4007) (V1 p.12).
^ex-01-01-5

### Example 6: Residual diagnostics for ABC, Exhibits 5 to 7 (V1 pp.13-17)

Step 1, residuals vs predicted (Exhibit 5).
The cloud is centred on zero with no direction and no fanning, which supports constant variance and uncorrelated errors (V1 p.13).
Three square markers, months 7, 25 and 95, sit far from the cloud and are potential outliers; check those dates for shocks omitted from the model (V1 p.14).

Step 2, residuals vs each factor (Exhibit 6, panels A to C).
No directional pattern against MKTRF, SMB or HML, so no sign of misspecification or non-linearity in any factor; the same three outliers reappear (V1 p.14).

Step 3, normal Q-Q (Exhibit 7).
Under normality the 5th percentile standardized residual should sit near $-1.65$ (V1 p.16).
Observations 25 and 95 lie well below the diagonal beyond $-2$ and observation 7 lies above it near $+2.5$; setting those three aside, the points track the diagonal, so the error term is close to normal (V1 p.17).

Verdict: the ABC model passes the visual checks for linearity, homoskedasticity, independence and normality, with three observations flagged for follow-up.
^ex-01-01-6

### Example 7: CRYPTO knowledge check (V1 pp.17-19)

Setting: monthly price changes of a cryptocurrency regressed on price changes of gold (GOLD) and a technology index (TECH), five years of data.

Part 1: a significant pairwise correlation between GOLD and TECH suggests an approximate linear relation between the independent variables, a potential violation of assumption 5 (independence of independent variables), to be explored further (V1 p.17).

Part 2: residuals vs predicted CRYPTO is used to spot clustering or patterns that suggest heteroskedasticity, and to spot outliers (V1 p.18).

Part 3: residuals vs GOLD is used to spot extreme values of the independent variable that may influence the estimates, and any relation between the residuals and GOLD, which would signal misspecification (V1 p.18).

Part 4: the normal Q-Q plot checks whether the residuals are normally distributed (V1 p.18).

Part 5: a pairwise scatterplot detects a linear relationship between dependent and independent variables; answer A (V1 p.18).
B is wrong because heteroskedasticity is a residual property, and C is wrong because normality of residuals is the Q-Q plot's job.

Part 6: the CRYPTO vs TECH scatter shows a positive, possibly significant relationship, plus several potential outliers (V1 p.18).

Part 7: a normal Q-Q plot detects whether residuals are normally distributed; answer C (V1 p.19).

Part 8: the Q-Q plot departs from the diagonal past $\pm 2$ standard deviations, so the residuals are not normal; the distribution is fat-tailed, which is common in financial time series (V1 p.19).
^ex-01-01-7

## Item-set patterns

> [!warning] Trap 1: the slope without the ceteris paribus clause
> Presentation: three options interpret a coefficient; one omits "holding all other independent variables constant", one swaps the direction (a 0.037% change in X for a 1% change in Y), one adds the intercept to the slope.
> Approach: the correct reading is a one-unit change in $X_j$ produces a $b_j$ change in $Y$ with every other $X$ fixed (V1 p.8).
> Distractors: the swapped-direction option tempts because both numbers appear in the equation; the intercept-plus-slope option ($-0.999 + 0.037 = -0.962$ in the practice set) tempts because it looks like a "total effect" (V1 p.22).

> [!warning] Trap 2: pairwise plot says nothing, regression says significant
> Presentation: the vignette shows a flat scatterplot of Y against $X_2$ and a significant t-statistic on $X_2$, then asks which statement is consistent.
> Approach: the scatterplot is unconditional; the coefficient is partial after controlling for the other $X$s, so both can be true at once (V1 p.12).
> Distractors: "the regression must be misspecified" and "the t-statistic must be wrong" both tempt because they resolve the apparent contradiction, but there is no contradiction.

> [!warning] Trap 3: which chart tests which assumption
> Presentation: four charts are labelled and the question asks which assesses homoskedasticity, or independence of the $X$s, or normality.
> Approach: residuals vs predicted for homoskedasticity and outliers; a scatter of one $X$ against another for independence of the $X$s; Q-Q for normality; Y vs one $X$ for linearity (V1 pp.13-18, p.23).
> Distractors: the Y-vs-X scatter tempts for homoskedasticity because it shows spread, but spread of Y is not spread of residuals; the residual plot tempts for independence of the $X$s because it is "the diagnostic chart".

> [!warning] Trap 4: binary dependent variable
> Presentation: the analyst wants to model whether a firm is a takeover target, defaults, or is upgraded.
> Approach: a 0/1 dependent variable routes to logistic regression at the first fork of the process (V1 p.5).
> Distractors: "multiple linear regression with a dummy independent variable" tempts because dummies are legitimate on the right-hand side; the trap is a dummy on the left-hand side.

> [!warning] Trap 5: assumption violated, what next
> Presentation: residuals fan out, or five variables are all insignificant, and the question asks for the analyst's next step.
> Approach: adjust the model and re-estimate; never proceed to goodness of fit or prediction until the assumptions and significance gates pass (V1 p.7).
> Distractors: "report the model with a caveat" and "drop to simple regression" tempt as pragmatic shortcuts that the flowchart does not allow.

> [!warning] Trap 6: correlated regressors
> Presentation: the vignette reports a high correlation between two independent variables and asks which assumption is at risk and what the consequence is.
> Approach: assumption 5b, no exact linear relation among the $X$s; an approximate relation still allows estimation but makes interpretation problematic, while an exact relation prevents estimation (V1 p.10).
> Distractors: "independence of errors" tempts because the word independence appears; "the model cannot be estimated" tempts but applies only to an exact relation.

> [!warning] Trap 7: Q-Q plot reading
> Presentation: a Q-Q plot where points bend away from the diagonal beyond $\pm 2$ standard deviations.
> Approach: the residuals are fat-tailed and not normal; the pattern is typical of financial time series (V1 p.19).
> Distractors: "heteroskedastic" tempts because the tails look like spread; "linearity violated" tempts because the plotted points are not on a line, but the Q-Q line is not a regression line.

> [!warning] Trap 8: units and the intercept
> Presentation: returns in whole percentages in one regression and decimals in another; the question asks for a prediction or annualises the intercept.
> Approach: plug values in the units the model was estimated in and keep the output in those units; the bond intercept 0.0023% per month is about 0.028% per year by simple multiplication by 12 (V1 p.8).
> Distractors: options that multiply a decimal coefficient by a whole-percent input, or compound the intercept, tempt because the arithmetic is easy and wrong.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM01-Basics-of-Multiple-Regression-and-Underlying-Assumptions-Practice-Problems]]

## Cross-links

- [[LM02-Evaluating-Regression-Model-Fit-and-Interpreting-Model-Results]]: takes the Exhibit 4 output shown here (R-squared, adjusted R-squared, F, t-statistics, p-values, confidence intervals) and turns it into formal hypothesis tests and model comparison; this module supplies the model and the assumptions those tests rely on.
- [[LM03-Model-Misspecification]]: the five assumptions listed here are tested formally there (Breusch-Pagan for heteroskedasticity, Durbin-Watson and Breusch-Godfrey for serial correlation, VIF for multicollinearity) and fixed with robust standard errors; the residual plots here are the visual first pass.
- [[LM04-Extensions-of-Multiple-Regression]]: dummy independent variables mentioned here as discrete regressors, the logistic regression that the process flowchart routes to for a 0/1 dependent variable, and influence analysis for the outliers flagged in the residual plots are all developed there.
- [[LM05-Time-Series-Analysis]]: the independence-of-errors assumption is the one most often broken with monthly return data; time-series models are the response when residuals are serially correlated.
- [[LM06-Machine-Learning]]: supervised learning generalises the regression process here, and penalised regression is the machine-learning answer to too many correlated regressors.
- [[LM07-Big-Data-Projects]]: the model-building loop (specify, estimate, diagnose, adjust) reappears as the data-science project workflow.
- [[LM04-Using-Multifactor-Models]]: the Fama-French factor regressions used as examples here are the estimation engine for multifactor return attribution in Portfolio Management.
- [[LM06-Backtesting-and-Simulation]]: factor-model coefficients estimated by regression feed backtests, and the fat-tailed residuals seen in the CRYPTO Q-Q plot are why backtests use non-normal or bootstrapped distributions.

## Self-test

Vignette A (Q1 to Q4): Priya Nair regresses monthly excess returns of a small-cap fund (RET, in whole percent) on MKTRF, SMB and HML using 84 months of data.
Output: $\widehat{RET} = 0.21 + 0.94\,MKTRF + 0.62\,SMB - 0.18\,HML$; $SS_{\text{regression}} = 1{,}250$, $SS_{\text{residual}} = 750$; the SMB coefficient has standard error 0.31.
Her colleague notes that a scatterplot of RET against HML is nearly flat, that a scatterplot of SMB against HML slopes strongly upward, and that the Q-Q plot of residuals bends below the diagonal beyond $-2$.

> [!question] Q1
> The best interpretation of the SMB coefficient is that a one-percentage-point increase in SMB:
> A. raises RET by 0.62 percentage points, other factors held constant.
> B. raises RET by 0.83 percentage points, since the intercept must be added.
> C. raises RET by 0.62 percentage points only when MKTRF and HML are zero.

> [!question] Q2
> Using the estimated equation, the predicted RET for a month in which MKTRF = 2, SMB = -1 and HML = 3 is closest to:
> A. 0.93.
> B. 1.47.
> C. 3.25.

> [!question] Q3
> The colleague's observation about the SMB-versus-HML scatterplot most directly raises concern about:
> A. independence of errors.
> B. an approximate linear relation among the independent variables.
> C. linearity between RET and SMB.

> [!question] Q4
> The flat RET-versus-HML scatterplot together with a significant HML t-statistic is best explained by:
> A. a coding error, because a flat scatterplot cannot coexist with a significant coefficient.
> B. the scatterplot showing the unconditional relation while the coefficient is partial.
> C. heteroskedastic residuals inflating the t-statistic.

Vignette B (Q5 to Q7): Tomas Weil is modelling whether a bond issuer is downgraded within a year (1 if downgraded, 0 otherwise) using leverage, interest coverage and an industry dummy.
His first attempt uses OLS multiple regression; the residuals-versus-predicted plot shows two parallel bands, and the residual variance rises with the predicted value.

> [!question] Q5
> According to the regression process, Weil's first decision should have been to:
> A. use logistic regression because the dependent variable is discrete.
> B. drop the industry dummy because discrete variables violate the linearity assumption.
> C. examine goodness of fit before checking the assumptions.

> [!question] Q6
> The rising residual variance in Weil's plot is most directly a violation of:
> A. normality.
> B. homoskedasticity.
> C. independence of independent variables.

> [!question] Q7
> Suppose Weil re-specifies with a continuous dependent variable and all assumptions pass, but the overall fit is not significant. His next step per the process is to:
> A. use the model for prediction because the assumptions hold.
> B. adjust the model and re-estimate.
> C. test the individual coefficients instead.

Vignette C (Q8 to Q10): Lena Osei estimates the bond index regression $RET = 0.0023 - 5.0585\,BY - 2.1901\,CS$ from the curriculum, with RET in decimal monthly excess return, using 60 observations.

> [!question] Q8
> For a month in which yields fall by 0.002 and spreads widen by 0.003, the predicted excess return is closest to:
> A. $-0.0144$.
> B. $0.0058$.
> C. $0.0190$.

> [!question] Q9
> The most accurate statement about the model's empirical duration is that it:
> A. equals 5.0585 and is the return sensitivity to yield changes with spread changes held constant.
> B. equals 2.1901 because credit spreads dominate bond index returns.
> C. cannot be inferred because duration is a price concept, not a return concept.

> [!question] Q10
> Osei plots the residuals against BY and observes a clear U-shape. The most appropriate conclusion is that:
> A. the residuals are fat-tailed.
> B. the relationship between RET and BY may be non-linear, so the model is misspecified.
> C. the independent variables are exactly collinear.

> [!success]- Answer key
> Q1: A.
> The partial slope is the change in Y for a one-unit change in SMB with the other regressors held constant (V1 p.8).
> B adds the intercept, which is the Q2-of-the-practice-set trap.
> C confuses "held constant" with "equal to zero"; the other factors can sit at any fixed level.
>
> Q2: A.
> $0.21 + 0.94(2) + 0.62(-1) - 0.18(3)$: $0.94 \times 2 = 1.88$; $0.21 + 1.88 = 2.09$; $2.09 - 0.62 = 1.47$; $1.47 - 0.54 = 0.93$.
> B (1.47) is the running total after forgetting the HML term.
> C (3.25) flips the sign of both negative terms.
>
> Q3: B.
> A strongly sloped scatter between two independent variables signals an approximate linear relation among the regressors, assumption 5b; estimation is still possible but interpretation is problematic (V1 p.10).
> A concerns correlation of residuals across observations.
> C concerns the Y-vs-X relation, not X-vs-X.
>
> Q4: B.
> The ABC example shows exactly this: no visible SMB relation in the pairs plot yet a significant SMB coefficient, because the regression measures the partial relation (V1 p.12).
> A is wrong because the two facts are compatible.
> C is wrong because heteroskedasticity affects the reliability of standard errors but is not the explanation the curriculum gives for this pattern.
>
> Q5: A.
> The first fork in Exhibit 2 asks whether the dependent variable is continuous; a 0/1 outcome routes to logistic regression (V1 pp.5-6).
> B is wrong because dummy independent variables are explicitly allowed (V1 p.5).
> C reverses the order; assumptions are checked before fit (V1 p.6).
>
> Q6: B.
> Homoskedasticity requires the residual variance to be the same for all observations; variance rising with the predicted value is heteroskedasticity (V1 p.10, p.18).
> A would be diagnosed by a Q-Q plot.
> C would be diagnosed by an X-vs-X scatter or pairwise correlations.
>
> Q7: B.
> A NO at "Is the overall fit significant?" loops back to "adjust the model" (V1 p.6, p.7).
> A skips a gate.
> C is not a step in the process; individual coefficient tests come after the overall fit passes (LM02).
>
> Q8: B.
> $-5.0585 \times (-0.002) = +0.010117$; $-2.1901 \times 0.003 = -0.0065703$; $0.0023 + 0.010117 - 0.0065703 = 0.0058467$, or about 0.0058.
> A ($-0.0144$) treats the yield fall as a rise; C ($0.0190$) flips the sign of both slopes.
>
> Q9: A.
> The yield slope is $-5.0585$, so the index behaves like a bond with duration 5.0585, measured with CS held constant (V1 p.8).
> B picks the wrong coefficient.
> C is wrong because the curriculum explicitly calls this an empirical duration.
>
> Q10: B.
> A pattern between residuals and an independent variable suggests the model is misspecified, here by a missing non-linear term in BY (V1 p.18).
> A would be read from a Q-Q plot.
> C would prevent estimation altogether, and there is no evidence about it in a residual-vs-X plot.

## Flashcards

#flashcards/cfa-l2/01-Quantitative-Methods/lm01

Multiple regression equation, general form::$Y_i = b_0 + b_1 X_{1i} + \dots + b_k X_{ki} + \varepsilon_i$, $i = 1, \dots, n$, with $n > k$ (V1 p.8)

Deterministic vs stochastic part of the regression model::The terms in the $X$s are deterministic; the error $\varepsilon_i$ is stochastic (V1 p.8)

Meaning of the intercept $b_0$::Expected value of $Y$ when all independent variables equal zero (V1 p.4)

Meaning of a partial regression coefficient $b_j$::Change in $Y$ for a one-unit change in $X_j$ holding all other independent variables constant (V1 p.8)

Variation of Y is also called::Sum of squares total, $\sum (Y_i - \bar{Y})^2$ (V1 p.8)

Three uses of multiple regression named in the module::Identify relationships between variables, test existing theories, forecast (V1 p.5)

Dependent variable is 0/1; which model?::Logistic regression, not multiple linear regression (V1 p.5)

What can a discrete independent variable represent?::Membership in a class, such as an industry sector, via a dummy variable (V1 p.5)

First question in the regression process flowchart::Is the dependent variable continuous? (V1 p.6)

Assumptions fail in the process flowchart; what next?::Adjust the model and re-estimate (V1 p.7)

Overall fit not significant; what next?::Adjust the model and re-estimate (V1 p.7)

List the five assumptions of multiple linear regression
?
Linearity, homoskedasticity, independence of errors, normality, independence of independent variables (V1 p.10)

Two parts of the independence-of-independent-variables assumption
?
5a: independent variables are not random. 5b: no exact linear relation between two or more independent variables or combinations of them (V1 p.10)

Exact linear relation among the Xs; consequence::The model cannot be estimated (V1 p.10)

Approximate linear relation among the Xs; consequence::The model can be estimated but interpretation is problematic (V1 p.10)

Signal of an approximate linear relation among the Xs::Significant pairwise correlations between independent variables (V1 p.10)

Homoskedasticity definition::Variance of the regression residuals is the same for all observations (V1 p.10)

Independence of errors definition::Observations are independent, so residuals are uncorrelated across observations (V1 p.10)

Normality assumption::Regression residuals are normally distributed (V1 p.10)

Another name for the scatterplot matrix::Pairs plot (V1 p.10)

What sits on the diagonal of a pairs plot?::Histogram of each variable (V1 p.11)

What does a pairwise scatterplot detect?::Whether there is a linear relationship between dependent and independent variables, plus outliers (V1 p.18)

Which chart assesses homoskedasticity?::Residuals vs predicted values (V1 p.23)

Which chart assesses independence of independent variables?::Scatter of one independent variable against another (V1 p.23)

Which chart assesses normality of residuals?::Normal Q-Q plot (V1 p.19)

Purpose of residuals vs one independent variable
?
Detect extreme values of that X that may influence the estimates, and any relation between residuals and X, which suggests misspecification (V1 p.18)

Q-Q plot: residuals normal means the points lie where?::Along the diagonal (V1 p.16)

Under normality the 5th percentile standardized residual appears at::About $-1.65$ standard deviations (V1 p.16)

Q-Q points bend away from the diagonal past $\pm 2$ SD; interpretation::Fat-tailed residuals, not normal; common in financial time series (V1 p.19)

Flat Y-vs-X scatter but significant coefficient; why?::The scatter shows the unconditional relation; the coefficient is partial after controlling for other Xs (V1 p.12)

Bond regression $RET = 0.0023 - 5.0585\,BY - 2.1901\,CS$; empirical duration::5.0585, from the negative of the yield-change slope (V1 p.8)

Bond regression prediction for BY = 0.005, CS = 0.001
?
$0.0023 - 5.0585(0.005) - 2.1901(0.001) = -0.0252$, or $-2.52\%$. Keys: 5.0585 x .005 = STO 1, 2.1901 x .001 = STO 2, .0023 - RCL 1 - RCL 2 = (V1 p.8)

Bond intercept 0.0023% per month annualised::About 0.028% per year, $0.0023 \times 12 = 0.0276$ (V1 p.8)

FF3 knowledge check: predicted return for MKTRF = 1, SMB = 4, HML = -2
?
$1.5324 + 0.5892 - 3.4876 + 0.1120 = -1.2540$; the curriculum prints $-1.2524$ using a mistyped intercept of 1.534 (V1 p.9)

Trap: coefficient interpretation option that adds the intercept to the slope::Wrong; $-0.999 + 0.037 = -0.962$ is not a marginal effect (V1 p.22)

Trap: "a 0.037% increase in X gives a 1% increase in Y"::Wrong; it reverses the roles of X and Y (V1 p.22)

ABC regression: $R^2$ from SS regression 0.2914 and SS total 0.7489::$0.2914 / 0.7489 = 0.3891$ (V1 p.12)

ABC regression: residual degrees of freedom with n = 120, k = 3::$120 - 3 - 1 = 116$ (V1 p.12)

ABC regression: t-stat for MKTRF from 1.2889 and SE 0.1538::$1.2889 / 0.1538 = 8.38$; keys: 1.2889 / .1538 = (V1 p.12)

ABC regression: standard error of estimate from SS residual 0.4575 and df 116::$\sqrt{0.4575 / 116} = 0.0628$; keys: .4575 / 116 = then the square-root key (V1 p.12)

ABC residual plots flagged which months as outliers?::Months 7, 25 and 95 (V1 p.14)

What should an analyst do about flagged outlier months?::Check for shocks from factors not in the model at those dates (V1 p.14)

In the residuals-vs-predicted plot, no directional relationship suggests::Constant variance and uncorrelated errors (V1 p.13)

CRYPTO example: significant GOLD-TECH correlation threatens which assumption?::Independence of independent variables (V1 p.17)

The {{residuals vs predicted}} plot is the primary tool for spotting heteroskedasticity and outliers (V1 p.18)

A dependent variable that is {{discrete}} (for example a 0/1 indicator) is modelled with {{logistic regression}} (V1 p.5)

A slope in multiple regression is called a {{partial regression coefficient}} or partial slope coefficient (V1 p.8)

The model is estimated over $n$ observations where $n$ must be {{larger than k}} (V1 p.8)

Multiple R in the ABC output, 0.6238, equals::$\sqrt{R^2} = \sqrt{0.3891}$ (V1 p.12)

Order of gates in the regression process after estimation::Analyze residuals and assumptions, then goodness of fit, then overall significance, then best-model check, then use (V1 p.6)

What does the pairs plot reveal about SMB vs HML for ABC?::Little or no correlation, a desirable property between explanatory variables (V1 p.12)

Why check assumptions before fit statistics?::Fit and test statistics rely on the assumptions for their distributions, so they are meaningless if assumptions fail (V1 p.6, p.10)

Name three software commands for regression from Exhibit 1::Excel Data Analysis > Regression, R lm, Python statsmodels or sklearn LinearRegression (V1 p.4)

## Common mistakes

1. Interpreting a slope without the clause "holding all other independent variables constant", or reading it as the change in $X$ for a change in $Y$ (V1 p.8, p.22).
2. Adding the intercept to the slope and calling the sum the effect of a one-unit change in $X$ (V1 p.22).
3. Reading "holding others constant" as "others equal to zero"; the intercept, not the slope, is the all-zero case (V1 p.4, p.8).
4. Treating a flat pairwise scatterplot as proof that a variable does not belong in the model; the regression coefficient is partial and can be significant anyway (V1 p.12).
5. Using multiple linear regression when the dependent variable is a 0/1 indicator instead of routing to logistic regression (V1 p.5).
6. Assigning the wrong chart to an assumption: Y-vs-X for linearity, residuals-vs-predicted for homoskedasticity and outliers, X-vs-X for independence of regressors, Q-Q for normality (V1 pp.13-19, p.23).
7. Proceeding to goodness of fit or prediction after a failed assumption check or an insignificant overall fit, instead of adjusting and re-estimating (V1 p.6, p.7).
8. Confusing "independence of errors" with "independence of independent variables" because both contain the word independence (V1 p.10).
9. Claiming a model cannot be estimated when regressors are merely highly correlated; only an exact linear relation prevents estimation (V1 p.10).
10. Reading a Q-Q plot whose tails bend away from the diagonal as heteroskedasticity rather than fat tails (V1 p.19).
11. Mixing units when predicting: whole-percent factor inputs into a decimal-return model, or forgetting that 0.0023 in the bond example is already a percentage per month (V1 p.8, p.9).
12. Forgetting the outliers: the residual plots are also the tool for identifying extreme observations to investigate, not only for assumption checks (V1 p.14).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "01-01" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
