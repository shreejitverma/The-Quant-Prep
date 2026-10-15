---
type: cfa-lm
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
volume: 1
lm: 4
title: "Extensions of Multiple Regression"
pages: "75-108"
weight_band: "5-10%"
difficulty: 3
los_count: 3
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/quantitative-methods]
---

# LM4: Extensions of Multiple Regression

Difficulty 3 of 5: the concepts are few (leverage, studentized residuals, dummies, logit) but the exam lives in the arithmetic of converting log odds to probabilities and in reading dummy coefficients relative to the base group, where sign and reference-category traps are dense.

## LOS map

- **describe** influence analysis and methods of detecting influential data points (V1 p.76) ^los-01-04-a
    - Examiner asks: given a table of leverage values and studentized residuals with n and k, compute the leverage cutoff $3(k+1)/n$ and the t critical value with $n-k-2$ degrees of freedom, then flag the observations that breach each rule.
- **formulate** and interpret a multiple regression model that includes qualitative independent variables (V1 p.83) ^los-01-04-b
    - Examiner asks: identify the base category and the number of dummies for a set of categories, then compute a fitted value or a difference between groups from an intercept dummy, a slope dummy, or both.
- **formulate** and interpret a logistic regression model (V1 p.91) ^los-01-04-c
    - Examiner asks: interpret an intercept or slope coefficient as log odds, convert it to odds and to a probability, compute a marginal effect at the means, and run a likelihood ratio test against the intercept-only model.

## Core intuition

This module answers three questions that arise the moment a regression leaves the textbook and meets real data.
First, can a handful of observations be silently steering the whole fit?
Second, how do we put categories (industry, fund style, regulated or not, month of the year) into a model that only understands numbers?
Third, what do we do when the thing we want to predict is itself a category, such as bankrupt or not, repurchaser or not, winning fund or not?

> [!abstract] Idea 1: influence has two sources, extreme X and extreme Y, and each has its own detector
> A high-leverage point is unusual in the independent variables, an outlier is unusual in the dependent variable, and an observation is influential only if removing it materially changes the estimated regression (V1 p.76, p.81).

Start with the geometry.
Ordinary least squares minimises the sum of squared vertical distances, so any observation far from the others in the X direction acts like a long lever arm: a small vertical pull at the end of a long arm rotates the fitted line a great deal (V1 p.77).
That is why the curriculum calls the measure leverage, $h_{ii}$.
Leverage lies between 0 and 1 and grows with the distance of the observation's X values from the mean of X across the sample (V1 p.78).
The leverages of all observations add up to $k+1$, the number of estimated coefficients including the intercept, so the average leverage is $(k+1)/n$ (V1 p.78).
The rule of thumb flags any observation whose leverage is more than three times the average, that is $h_{ii} > 3(k+1)/n$ (V1 p.78).
Nothing about the Y value enters leverage; a point can have huge leverage and sit exactly on the fitted line, in which case it is unusual but harmless (V1 p.77).

An outlier is the other case: its Y value is far from what the model predicts for its X values, so its residual is large (V1 p.77).
The naive check, look at the raw residual, has a flaw.
An influential outlier drags the fitted line toward itself, which shrinks its own residual and hides the very problem we are looking for.
The cure is the deleted residual: refit the model without observation $i$, predict $Y_i$ from that refit, and measure how far the actual $Y_i$ is from that prediction (V1 p.80).
Divide by the standard error of the residuals from the deleted fit and you have the studentized deleted residual $t_i^*$, which follows a t distribution with $n-k-2$ degrees of freedom (V1 p.80, p.81).
The degrees of freedom are one fewer than the usual $n-k-1$ because one observation has been deleted.
The right-hand form of Equation 1 shows the trick that makes this practical: you never have to refit $n$ times, because $t_i^*$ can be computed from the full-sample residual $e_i$, the leverage $h_{ii}$, and $MSE_{(i)}$ (V1 p.80).
Two rules of thumb apply: $|t_i^*| > 3$ flags an outlier, and $|t_i^*|$ above the t critical value at the chosen significance level flags the outlier as potentially influential (V1 p.81).

Detection is only half the job.
The curriculum is explicit that outliers and high-leverage points are unusual but not necessarily a problem, and that an observation is influential only if its exclusion causes substantial changes in the estimated regression function (V1 p.77, p.81).
So the workflow is: flag with leverage and studentized residuals, look at the influence plot, refit without the flagged points, and compare (V1 p.82).
Then ask why the point exists.
If it is a data entry error, correct or discard it, or winsorize the sample (V1 p.82).
If it is valid, the point is telling you something: an omitted variable or a violated assumption, which links straight back to the misspecification checklist in LM03 (V1 p.82).

> [!abstract] Idea 2: a dummy variable is a switch that moves the intercept, the slope, or both, always measured against a base group
> With $n$ categories you use $n-1$ dummies; the omitted category is the base, and every dummy coefficient is a difference from that base, not an absolute level (V1 p.84).

Why $n-1$ and not $n$?
If you include a dummy for every category, the dummies sum to 1 for every observation, which is exactly the constant column that estimates the intercept.
That is perfect collinearity, and the regression fails (V1 p.84).
Dropping one category fixes it and makes that category the reference point.
In the mutual fund example the base is value funds, so the BLEND coefficient of 0.661 means blend funds earn 0.661 percentage points more per year than value funds, holding expense ratio, cash, age, and size constant, and the GROWTH coefficient of 2.498 is the corresponding premium of growth over value (V1 p.88).
The intercept, $-2.909$, is the return that is unexplained by the independent variables for the base group (V1 p.88).

An intercept dummy shifts the line vertically by $d_0$; the two groups have parallel lines (V1 p.85).
A slope dummy is an interaction $D \times X$, and its coefficient $d_1$ is the change in the slope for the group with $D=1$, so that group's slope is $b_1 + d_1$ (V1 p.87).
When both are present, the difference between the groups is $d_0 + d_1 X$, so it depends on the level of X (V1 p.87).
That last sentence is the source of most exam traps: the gap between a regulated and an unregulated firm in the REG example is $-0.5 - 0.2 \times MKTSH$, which widens as market share grows (V1 p.91).
Testing whether a dummy matters is an ordinary t test on its coefficient (V1 p.87).
Testing whether a whole set of dummies matters, such as eleven month dummies for seasonality, is the F test and the adjusted $R^2$ from LM02 (V1 p.106).

> [!abstract] Idea 3: when Y is binary, model the log odds, not the probability, and estimate by maximum likelihood
> The logit transformation $\ln[P/(1-P)]$ maps a probability on $(0,1)$ to the whole real line, so a linear model on the log odds can never predict an impossible probability (V1 p.92, p.93).

A linear probability model regresses a 0/1 outcome directly on the X variables (V1 p.92).
It can predict probabilities above 1 or below 0, and it forces the effect of each X on the probability to be the same everywhere, which is unrealistic for something like bankruptcy and leverage (V1 p.92).
The odds, $P/(1-P)$, are the probability the event happens divided by the probability it does not; a probability of 0.75 is odds of 3 to 1 (V1 p.92).
The natural log of the odds is the logit, and logistic regression makes the logit a linear function of the X variables (V1 p.92, p.93).
Inverting gives the S-shaped probability curve $P = 1/(1+e^{-z})$, which is approximately linear in the middle and flat near 0 and 1 (V1 p.92, p.93).

Because the model is non-linear in the probability, the coefficients are not marginal effects on the probability.
A slope coefficient $b_j$ is the change in the log odds per unit change in $X_j$, holding the other variables constant (V1 p.93, p.106).
Exponentiating it gives the multiplicative change in the odds.
The effect on the probability depends on where you are on the curve: at $P = 0.5$ the slope of the curve is at its maximum, and in the tails a one-unit change in X does almost nothing (V1 p.93, p.94).
The curriculum's standard way to state a marginal effect is therefore to compute the probability at the sample means of all X variables, bump one variable up by one unit, recompute, and take the difference (V1 p.94).

Estimation is by maximum likelihood, not least squares, because the outcome is binomial (V1 p.93).
That has three consequences.
Coefficient tests look like OLS tests, reported as z statistics with p-values (V1 p.93).
There is no $R^2$; the pseudo-$R^2$ in the output is only meaningful for comparing specifications on the same dataset (V1 p.93, p.95).
Overall fit is judged by the log-likelihood, which is always negative, so closer to zero is better, and by the likelihood ratio test $LR = -2(LL_{restricted} - LL_{unrestricted})$, distributed chi-square with degrees of freedom equal to the number of restrictions (V1 p.94, p.95).
The LR test plays exactly the role the joint F test plays in OLS: the null is that the smaller model is adequate, and rejection favours the larger model (V1 p.95).
The error term is assumed to follow a logistic distribution, which looks like the normal but has fatter tails (V1 p.93).
Finally, logistic regression is the workhorse of binary classification in machine learning, for example classifying the sentiment of a press release from its tokens, which is the bridge to LM06 (V1 p.98).

## Formulas and derivations

**Leverage rule of thumb** (V1 p.78)
$$
h_{ii} > 3\left(\frac{k+1}{n}\right) \Rightarrow \text{observation } i \text{ is potentially influential}
$$
^f-01-04-1

- $h_{ii}$: leverage of observation $i$, between 0 and 1, larger when the X values of observation $i$ are far from their means (V1 p.78).
- $k$: number of independent variables; $n$: number of observations.
- Reason: the leverages sum to $k+1$ (Formula 2), so the average leverage is $(k+1)/n$; the rule flags anything above three times the average.

**Sum of leverages** (V1 p.78)
$$
\sum_{i=1}^{n} h_{ii} = k + 1
$$
^f-01-04-2

- The $+1$ is the intercept; the sum equals the number of estimated coefficients.
- Consequence: adding regressors raises average leverage, so the cutoff in Formula 1 rises with $k$ and falls with $n$.

**Deleted residual** (V1 p.80)
$$
e_i^* = Y_i - \hat{Y}_i^*
$$
^f-01-04-3

- $\hat{Y}_i^*$: the prediction for observation $i$ from a model estimated on the other $n-1$ observations (observation $i$ deleted).
- Why: an influential point pulls the full-sample line toward itself and shrinks its own ordinary residual; deleting it before predicting removes that self-masking.

**Studentized deleted residual** (V1 p.80)
$$
t_i^* = \frac{e_i^*}{s_{e}^*} = \frac{e_i}{\sqrt{MSE_{(i)}\,(1-h_{ii})}}
$$
^f-01-04-4

- $s_e^*$: standard deviation of the residuals from the deleted regression; $e_i$: ordinary residual from the full-sample fit; $MSE_{(i)}$: mean squared error of the model with observation $i$ deleted; $h_{ii}$: leverage (V1 p.80).
- The right-hand form uses only full-sample quantities plus $MSE_{(i)}$, which is why software can compute all $n$ values without $n$ separate refits.
- High leverage inflates $t_i^*$ through the $(1-h_{ii})$ term: the same raw residual is more suspicious at a high-leverage point.

**Studentized residual decision rules** (V1 p.81)
$$
|t_i^*| > 3 \Rightarrow \text{outlier}; \qquad |t_i^*| > t_{\alpha/2,\; n-k-2} \Rightarrow \text{potentially influential}
$$
^f-01-04-5

- Degrees of freedom are $n-k-2$: the usual $n-k-1$ less one for the deleted observation (V1 p.80).
- Example: $n=15$, $k=2$ gives 11 df and a 5% two-tailed critical value of 2.2010; $n=26$, $k=3$ gives 21 df and 2.080 (V1 p.81, p.83).

> [!tip] Calculator
> The BA II Plus has no t table; the exam supplies the critical value or a table.
> Your only computation is $df = n - k - 2$ and the cutoff $3 \times (k+1) \div n$.
> Keystrokes for $n=96$, $k=2$: `3 × 3 ÷ 96 =` gives 0.09375.

**Number of dummies for n categories** (V1 p.84)
$$
\text{dummies required} = n_{cat} - 1
$$
^f-01-04-6

- The omitted category is the base (control) group; each dummy coefficient is measured relative to it (V1 p.84).
- Reason: with all $n_{cat}$ dummies included, $\sum D_j = 1$ for every observation, which duplicates the intercept column and violates the no-exact-linear-relationship assumption (V1 p.84).

**Intercept dummy model** (V1 p.84)
$$
Y_i = b_0 + d_0 D_i + b_1 X_i + \varepsilon_i
$$
^f-01-04-7

- $D_i = 0$: $Y = b_0 + b_1 X$ (base).
$D_i = 1$: $Y = (b_0 + d_0) + b_1 X$ (V1 p.85).
- $d_0$ is the vertical distance between two parallel lines; it may be positive or negative (V1 p.85).

**Slope dummy (interaction) model** (V1 p.86)
$$
Y_i = b_0 + b_1 X_i + d_1 D_i X_i + \varepsilon_i
$$
^f-01-04-8

- $D_i X_i$ equals $X_i$ when $D_i = 1$ and zero otherwise (V1 p.89).
- $D_i = 1$: $Y = b_0 + (b_1 + d_1) X$, so $d_1$ is the change in slope, not the slope itself (V1 p.87).

**Intercept and slope dummy model** (V1 p.87)
$$
Y_i = b_0 + d_0 D_i + b_1 X_i + d_1 D_i X_i + \varepsilon_i
$$
^f-01-04-9

- $D_i = 1$: $Y = (b_0 + d_0) + (b_1 + d_1) X$ (V1 p.87).
- The gap between the groups is $d_0 + d_1 X$, which varies with $X$; this is the quantity the exam asks you to sign and size (V1 p.87, p.91).

**Linear probability model (what not to use)** (V1 p.92)
$$
Y_i = b_0 + b_1 X_{1i} + b_2 X_{2i} + b_3 X_{3i} + \varepsilon_i, \qquad Y_i \in \{0, 1\}
$$
^f-01-04-10

- Fitted values can fall outside $[0,1]$ and the effect of each $X$ on the probability is forced to be constant (V1 p.92).

**Odds** (V1 p.92)
$$
\text{Odds} = \frac{P}{1-P}
$$
^f-01-04-11

- $P$: probability the event occurs; $1-P$: probability it does not.
- $P = 0.75$ gives odds of $0.75/0.25 = 3$, read as 3 to 1 (V1 p.92).
- Inverse: $P = \text{Odds}/(1+\text{Odds})$, which is how the curriculum converts $e^{b_0}$ back to a probability (V1 p.96).

**Logistic transformation (logit, log odds)** (V1 p.92)
$$
\text{logit}(P) = \ln\left(\frac{P}{1-P}\right)
$$
^f-01-04-12

- Maps $P \in (0,1)$ onto $(-\infty, +\infty)$, which is what lets a linear right-hand side be valid everywhere.
- $P = 0.5$ gives log odds of 0; $P > 0.5$ gives positive log odds; $P < 0.5$ gives negative log odds.

**Logistic regression model** (V1 p.93)
$$
\ln\left(\frac{P}{1-P}\right) = b_0 + b_1 X_1 + b_2 X_2 + b_3 X_3 + \varepsilon
$$
^f-01-04-13

- $b_j$: change in the log odds of the event per one-unit change in $X_j$, other variables held constant (V1 p.93, p.106).
- $b_0$: the log odds of the event when every $X_j = 0$ (V1 p.96, p.106).
- Estimated by maximum likelihood using the binomial distribution; coefficients are tested with z statistics (V1 p.93).

**Event probability from the logit** (V1 p.93)
$$
P = \frac{1}{1 + \exp\left[-(b_0 + b_1 X_1 + b_2 X_2 + b_3 X_3)\right]}
$$
^f-01-04-14

- Derivation: let $z = b_0 + \sum b_j X_j$.
Then $P/(1-P) = e^{z}$, so $P = e^{z}(1-P)$, $P(1+e^{z}) = e^{z}$, $P = e^{z}/(1+e^{z}) = 1/(1+e^{-z})$.
- Sigmoid: near-linear around $P = 0.5$, flat near 0 and 1 (V1 p.92).

> [!tip] Calculator
> Compute $e^{-z}$, add 1, take the reciprocal.
> For $z = -0.8923$: `0.8923 2nd [e^x]` gives $e^{0.8923} = 2.4408$; `+ 1 = 1/x` gives $P = 0.2906$.
> For a positive $z$ such as 0.5777, key `0.5777 +/- 2nd [e^x] + 1 = 1/x` to get 0.6405; a sign slip here is the source of the 82.2% distractor in Practice Problem 12.

**Odds multiplier from a logit coefficient (derived)** (V1 p.93)
$$
\frac{\text{Odds}(X_j + 1)}{\text{Odds}(X_j)} = e^{b_j}
$$
^f-01-04-15

- Follows from Formula 13: raising $X_j$ by one adds $b_j$ to the log odds, so the odds are multiplied by $e^{b_j}$.
- The curriculum states the interpretation in log-odds terms (V1 p.93); the exponentiated form is the algebraic consequence and a common distractor when an option says "change in the odds" for the raw coefficient (V1 p.106).

**Marginal effect at the means** (V1 p.94)
$$
\Delta P_j = P\left(\bar{X}_1, \ldots, \bar{X}_j + 1, \ldots, \bar{X}_k\right) - P\left(\bar{X}_1, \ldots, \bar{X}_j, \ldots, \bar{X}_k\right)
$$
^f-01-04-16

- Compute the probability at the sample means, then again with only $X_j$ increased by one unit (or by the increment stated in the question), and subtract (V1 p.94, p.96).
- The effect is largest where $P$ is near 0.5 and shrinks in the tails because the slope of the probability curve is $P(1-P) b_j$ (V1 p.93, p.94).

**Likelihood ratio test** (V1 p.94)
$$
LR = -2\left(LL_{restricted} - LL_{unrestricted}\right) \sim \chi^2_{q}
$$
^f-01-04-17

- $LL$: log-likelihood, always negative, higher (closer to zero) is better fit (V1 p.95).
- $q$: number of restrictions, equal to the number of coefficients set to zero (V1 p.94).
- $H_0$: the restricted (smaller) model is adequate; reject if $LR$ exceeds the chi-square critical value (V1 p.95).
- Restricted model with intercept only is reported as LL-Null; the software's LLR p-value is the p-value of this test (V1 p.95).

> [!tip] Calculator
> $LL_{null} = -312.68$, $LL = -304.20$: `312.68 +/- - 304.20 +/- = × 2 +/- =` gives 16.96.
> Critical $\chi^2$ with 3 df at 5% is 7.8150 (V1 p.97).

**Pseudo-R2 (McFadden form, not stated in the curriculum)** (V1 p.95)
$$
\text{Pseudo-}R^2 = 1 - \frac{LL_{unrestricted}}{LL_{null}}
$$
^f-01-04-18

- The curriculum only says pseudo-$R^2$ is produced by software and is valid only for comparing specifications of the same model on the same dataset (V1 p.93, p.95).
- This form reproduces Exhibit 13: $1 - 304.20/312.68 = 0.0271$, and Practice Problem Model 1: $1 - 451.66/478.86 = 0.057$ (V1 p.95, p.102).
Do not expect to be asked to compute it.

## Worked examples

### Example 1: Nutritional supplement retailers, leverage (V1 p.78 to p.80)

Setup: OPM regressed on PROD and ONLINE, $n = 15$, $k = 2$.
Panel A full sample: PROD coefficient 0.77, t = 2.70, p = 0.02; ONLINE coefficient $-0.29$, t = $-1.02$, p = 0.33; intercept 7.03, p = 0.61.
Panel B shows Observation 7 with leverage 0.80.
Panel C after removing one observation: intercept 9.81, PROD 0.74 (p = 0.05), ONLINE $-0.36$ (p = 0.57).

Part 1: which slopes differ from zero at 5%?
Only PROD, because its p-value of 0.02 is below 0.05; ONLINE has p = 0.33 (V1 p.79).

Part 2: which observations are potentially influential by leverage?
Cutoff $= 3(k+1)/n = 3 \times 3 / 15 = 9/15 = 0.60$.
Observation 7 has leverage 0.80, which exceeds 0.60, so it is potentially influential; no other observation crosses the line (V1 p.79, p.80).

Part 3: how do results change after removal?
Removing Observation 7 raises the intercept from 7.03 to 9.81, lowers the PROD coefficient slightly from 0.77 to 0.74, and raises its p-value from 0.02 to 0.05.
The standard errors roughly double (intercept 13.60 to 24.80, ONLINE 0.28 to 0.61) because a high-leverage point carries a lot of the X variation that pins down the slopes.
The conclusion that PROD matters at the 5% level still holds, so the point is influential on magnitudes but not on the qualitative conclusion (V1 p.80).
Python check: `3*3/15 = 0.60`. ^ex-01-04-1

### Example 2: Nutritional supplement retailers, studentized residuals (V1 p.81)

Same regression, $n = 15$, $k = 2$.
Degrees of freedom $= n - k - 2 = 15 - 2 - 2 = 11$.
The 5% two-tailed critical t with 11 df is 2.2010 (Python: `t.ppf(0.975, 11) = 2.2010`).
Exhibit 5 shows Observations 2 and 3 with $|t_i^*| > 2.2010$, so both are flagged as potentially influential outliers and should be examined further (V1 p.81).
Note the contrast with Example 1: Observation 7 is the high-leverage point (extreme X) while 2 and 3 are outliers (extreme Y); leverage and studentized residuals identify different observations because they detect different kinds of unusualness (V1 p.81). ^ex-01-04-2

### Example 3: ROA regression, outlier question set (V1 p.82 to p.83)

Setup: 26 observations, three independent variables, studentized residuals plotted for each observation.
Observation 3 shows 2.915, Observation 5 shows $-4.033$, Observation 4 shows 1.932; every other value is below 1 in absolute terms.

Part 1: which observations are outliers at 5%?
$df = n - k - 2 = 26 - 3 - 2 = 21$.
Critical t at 5% two-tailed with 21 df is $\pm 2.080$ (Python: `t.ppf(0.975, 21) = 2.0796`).
$|2.915| > 2.080$ and $|-4.033| > 2.080$, so Observations 3 and 5 are outliers; Observation 4 at 1.932 is not (V1 p.83).
Observation 5 also breaches the absolute rule $|t^*| > 3$.

Part 2: recommended action.
Investigate Observations 3 and 5 for data entry or data quality problems before deciding whether to correct, discard, or winsorize; if the data are valid, consider whether a variable is omitted or an assumption is violated (V1 p.82, p.83). ^ex-01-04-3

### Example 4: Mutual fund returns with intercept dummies (V1 p.87 to p.88)

Setup: five-year average annual return regressed on EXP, CASH, AGE, SIZE, BLEND, GROWTH; value funds are the base.
$n = 23{,}025$, $R^2 = 0.1230$, adjusted $R^2 = 0.1228$, F = 538 with significance 0.

Number of dummies: three styles need $3 - 1 = 2$ dummies (BLEND, GROWTH); VALUE is the base with no dummy (V1 p.87).

Interpretation of coefficients (all p-values 0.00, so all significant):
- Intercept $-2.909$: the return not explained by the independent variables for the base (value) group (V1 p.88).
- BLEND 0.661: blend funds earn 0.661 percentage points per year more than value funds, other variables constant (V1 p.88).
- GROWTH 2.498: growth funds earn 2.498 percentage points more than value funds (V1 p.88).
- AGE 0.074: each additional year of age adds 0.074 percentage points for every style, because there is no slope dummy yet (V1 p.88).

Fit: $R^2$ of 12.30% against adjusted $R^2$ of 12.28% differ by only 0.02 percentage points, which with six regressors and 23,025 observations signals that the regressors are collectively statistically meaningful rather than padding (V1 p.88).
Implied difference between blend and growth: $2.498 - 0.661 = 1.837$ percentage points in favour of growth (Python: `2.498-0.661 = 1.837`). ^ex-01-04-4

### Example 5: Mutual fund returns with intercept and slope dummies (V1 p.89 to p.90)

Setup: add AGE_BLEND $= AGE \times BLEND$ and AGE_GROWTH $= AGE \times GROWTH$.
New coefficients: intercept $-2.810$, AGE 0.065, BLEND 0.603, GROWTH 2.262, AGE_BLEND 0.005 (p = 0.53), AGE_GROWTH 0.020 (p = 0.01).

Base group slope: value funds gain 0.065 percentage points per year of age (BLEND = 0 and GROWTH = 0) (V1 p.89).

Growth fund slope on AGE: $0.065 + 0.020 = 0.085$ percentage points per year, because AGE_GROWTH is significant at p = 0.01 (V1 p.89).
Python: `0.065+0.020 = 0.085`.

Blend fund slope on AGE: AGE_BLEND has p = 0.53, so it is not distinguishable from zero and blend funds share the base slope of 0.065 statistically; the point estimate would be $0.065 + 0.005 = 0.070$.

Growth versus value in total: the curriculum combines the intercept shift 2.262 with the slope 0.085 and quotes 2.347 (V1 p.90).
Python: `2.262+0.085 = 2.347`.
Read this carefully: the exact gap between a growth and a value fund of age $A$ is $2.262 + 0.020 A$, so 2.347 is the curriculum's shorthand for "intercept premium plus the growth fund's full age slope"; the precise per-year difference in slope is only 0.020, not 0.085. ^ex-01-04-5

### Example 6: Global macro interview, choosing dummy structures (V1 p.90 to p.91)

Part 1: categorise countries as emerging (1) or developed (0) with a change in intercept.
Answer B, an intercept dummy, because the requirement is a level shift by market development status; A misdescribes what a slope dummy does and C misdescribes an interaction term as an intercept shift (V1 p.90).

Part 2: model the interaction of GDP growth and market status.
Answer C: $\text{Return} = b_0 + b_1 GDPG + d_1 EM + d_2 (EM \times GDPG) + \varepsilon$.
A and B include both EM and DM dummies, which with an intercept is the dummy variable trap (perfect collinearity, since EM + DM = 1 for every country); B also omits the interaction (V1 p.90).

Part 3: $RET = 0.50 - 0.5\,REG + 0.4\,MKTSH - 0.2\,REG\_MKTSH$.
Write the two fitted lines.
Unregulated (REG = 0): $RET = 0.50 + 0.4\,MKTSH$.
Regulated (REG = 1): $RET = (0.50 - 0.5) + (0.4 - 0.2)\,MKTSH = 0.00 + 0.2\,MKTSH$.
Difference, regulated minus unregulated: $-0.5 - 0.2\,MKTSH$.
- Statement A is correct: at any market share the regulated firm is at least 0.5 lower, and the gap only grows as MKTSH rises (V1 p.91).
- Statement C is correct: for each one-unit rise in market share the regulated firm gains 0.2 while the unregulated firm gains 0.4, so the regulated firm falls a further 0.2 behind (V1 p.91).
Python: `0.2-0.4 = -0.2`.
- Statement B is wrong: the MKTSH coefficient is positive for both groups and REG is negative, so non-regulated firms with larger shares have higher, not lower, ROA (V1 p.91).
The curriculum's solution phrases the sum of dummy coefficients as $-0.3$; the cleaner statement is the pair of lines above. ^ex-01-04-6

### Example 7: Odds from a probability (V1 p.92)

If the probability of bankruptcy is 0.75, the odds are $0.75/(1 - 0.75) = 0.75/0.25 = 3$, that is 3 to 1: bankruptcy is three times as probable as survival (V1 p.92).
Log odds $= \ln 3 = 1.0986$ (Python: `log(3) = 1.0986`).
Reverse check: $P = 3/(1+3) = 0.75$. ^ex-01-04-7

### Example 8: Share repurchase logit (V1 p.95 to p.98)

Setup: $n = 500$, Repurchase on CASH, DE, NPM.
Coefficients: intercept $-0.4738$ (p = 0.016), CASH $-0.9118$ (p = 0.430), DE $-0.3186$ (p = 0.017), NPM 0.9407 (p = 0.024).
Log-likelihood $-304.20$, LL-Null $-312.68$, LLR p-value 0.0007, pseudo-$R^2$ 0.0271.
Means: CASH 0.083, DE 0.9182, NPM $-0.0535$.

Part 1: interpret the intercept.
$-0.4738$ is the log odds of repurchasing when CASH, DE, and NPM are all zero.
Odds $= e^{-0.4738} = 0.6226$; probability $= 0.6226/(1 + 0.6226) = 0.3837$, or 38.37% (V1 p.96).
Python: `exp(-0.4738) = 0.62263`, `0.62263/1.62263 = 0.38372`.

Part 2: marginal effects at the means.
$z_0 = -0.4738 + (-0.9118)(0.083) + (-0.3186)(0.9182) + (0.9407)(-0.0535)$
$= -0.4738 - 0.07568 - 0.29254 - 0.05033 = -0.89235$.
$P_0 = 1/(1 + e^{0.89235}) = 1/(1 + 2.4408) = 0.2906$, so 29.06% (V1 p.96).
Python: `0.29063`.
- CASH from 0.083 to 0.093: $z = -0.89235 - 0.009118 = -0.90147$, $P = 0.2887$; change $= 28.87\% - 29.06\% = -0.19\%$ (V1 p.97).
Python: `0.28875`, delta `-0.00188`.
- NPM from $-0.0535$ to $-0.0435$: $z = -0.89235 + 0.009407 = -0.88294$, $P = 0.2926$; change $= +0.20\%$ (V1 p.97).
Python: `0.29257`, delta `+0.00194`.
- DE from 0.9182 to 0.9282: $z = -0.89235 - 0.003186 = -0.89554$, $P = 0.2900$; change $= -0.07\%$ (V1 p.97).
Python: `0.28997`, delta `-0.00066`.
Sanity check with the slope of the curve: $P(1-P) b_j \Delta X = 0.2906 \times 0.7094 \times (-0.9118)(0.01) = -0.00188$ for CASH, matching the exact recomputation.
Note the increment is 0.01 (1 percentage point of the ratio), not one whole unit; the question sets the increment (V1 p.96).

Part 3: LR test against intercept-only.
$H_0: b_1 = b_2 = b_3 = 0$; $H_a$: at least one non-zero.
$LR = -2(-312.68 - (-304.20)) = -2(-8.48) = 16.96$ (V1 p.98).
Python: `16.96`.
Critical $\chi^2$ with 3 df at 5% is 7.8150 (Python: `chi2.ppf(0.95, 3) = 7.8147`).
$16.96 > 7.815$, reject $H_0$: the three variables are jointly significant and the unrestricted model fits better; the reported LLR p-value of 0.0007 agrees (Python: `1 - chi2.cdf(16.96, 3) = 0.00072`) (V1 p.98).
Individually, DE and NPM are significant at 5% (p = 0.017, 0.024) while CASH is not (p = 0.430) (V1 p.98). ^ex-01-04-8

## Item-set patterns

> [!warning] Trap 1: leverage cutoff uses k + 1, not k
> The vignette gives $n$ and $k$ and a column of $h_{ii}$.
> Correct: cutoff $= 3(k+1)/n$.
> Distractors: $3k/n$ (forgets the intercept, gives a lower cutoff and flags too many points), the single highest leverage only (tempting because it is visually obvious), or a round number such as 0.10 that happens to sit near the cutoff (V1 p.78, p.106).

> [!warning] Trap 2: studentized residual sign and degrees of freedom
> The table mixes positive and negative studentized residuals.
> Correct: compare the absolute value to the t critical value with $n-k-2$ df.
> Distractors: flagging only the positive values above the critical value (ignores $-2.906$), using $n-k-1$ df (gives a slightly wrong critical value when you must look it up), or applying the $|t^*| > 3$ outlier rule when the question asks about influence at a stated significance level (V1 p.81, p.106).

> [!warning] Trap 3: unusual is not the same as influential
> The vignette shows a high-leverage point sitting on the fitted line, or asks what removing a point does.
> Correct: influence is judged by refitting without the point and comparing coefficients; a point can be high leverage or an outlier without changing conclusions.
> Distractors: "must be deleted" (automatic deletion is warned against), "has no effect because it is on the line" stated without a refit, "is a data error" (may be a valid signal of an omitted variable) (V1 p.77, p.81, p.82).

> [!warning] Trap 4: the base category and the intercept
> Twelve months, eleven dummies.
> Correct: the omitted month (December) is the base and its expected return is the intercept; each dummy is the difference from December.
> Distractors: "November is the base" because it is the last one listed, "the average of the eleven coefficients is the base return", or reading a month's coefficient as that month's return rather than as the difference from December (V1 p.84, p.106).

> [!warning] Trap 5: slope dummy coefficient is a change in slope, not the slope
> Output shows AGE 0.065 and AGE_GROWTH 0.020.
> Correct: growth fund slope $= 0.065 + 0.020 = 0.085$; value fund slope $= 0.065$.
> Distractors: quoting 0.020 as the growth fund slope, or adding the intercept dummy 2.262 to a slope (mixing units, since one is a level shift and the other is per unit of AGE) (V1 p.89).

> [!warning] Trap 6: the gap between groups depends on X when both dummies are present
> $RET = 0.50 - 0.5\,REG + 0.4\,MKTSH - 0.2\,REG\_MKTSH$.
> Correct: gap $= -0.5 - 0.2\,MKTSH$, so it widens with market share.
> Distractors: "regulated firms are exactly 0.5 lower" (true only at MKTSH = 0), "larger market share hurts unregulated firms" (sign confusion; 0.4 is positive), "sum of coefficients is $-0.3$" as a stand-alone interpretation (V1 p.91).

> [!warning] Trap 7: log odds versus odds versus probability
> An option says the slope coefficient is "the change in the odds" or "the change in probability".
> Correct: it is the change in the log odds per unit change in $X_j$, other variables constant; $e^{b_j}$ is the odds multiplier; the probability change depends on the level of every variable.
> Distractor wording also includes "while all other variables increase by one unit" instead of "holding constant" (V1 p.93, p.106).

> [!warning] Trap 8: intercept of a logit
> Options: "probability if all X are one", "log odds of the event if all X are zero", "log odds of the non-event if all X are zero".
> Correct: log odds of the event when all X are zero; convert with $e^{b_0}/(1+e^{b_0})$ if a probability is requested.
> The non-event log odds is $-b_0$ (V1 p.96, p.106).

> [!warning] Trap 9: using every coefficient when the question says significant ones only
> Practice Problem 12 asks for a probability "using only the statistically significant variable estimates".
> Correct: $z = -1.9589 + 0.3453 \times 4.0 = -0.5777$, $P = 35.95\%$.
> Distractor A (27.4%) is exactly what you get by plugging in all eight coefficients; distractor C (82.2%) comes from a sign slip in the exponent.
> Then compare to the stated threshold (65%) to classify (V1 p.105, p.108).

> [!warning] Trap 10: log-likelihood and LR test direction
> Two models: LL $-451.66$ and $-450.40$.
> Correct: higher (closer to zero) is better, so $-450.40$ wins; LR $= -2(LL_R - LL_U)$ is positive and compared with $\chi^2_q$.
> Distractors: "lower log-likelihood is better" (thinking of it as a loss), negative LR from reversing the subtraction, using $n-k-1$ instead of $q$ for the df, or comparing pseudo-$R^2$ across different datasets (V1 p.94, p.95, p.107).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM04-Extensions-of-Multiple-Regression-Practice-Problems]]

## Cross-links

- [[LM01-Basics-of-Multiple-Regression-and-Underlying-Assumptions]]: supplies the OLS model, the assumption of no exact linear relationship among regressors (the reason for $n-1$ dummies), and the residual definitions that leverage and studentized residuals build on.
- [[LM02-Evaluating-Regression-Model-Fit-and-Interpreting-Model-Results]]: the joint F test and adjusted $R^2$ are the tools used to test a block of dummies (the seasonality problem), and the LR test is the logit analogue of the nested F test.
- [[LM03-Model-Misspecification]]: influential points that are valid data point to omitted variables or violated assumptions; the remedies overlap with the misspecification fixes.
- [[LM05-Time-Series-Analysis]]: seasonal dummies here foreshadow seasonality handling in autoregressive models, and month or quarter dummies are the regression alternative to seasonal lags.
- [[LM06-Machine-Learning]]: logistic regression is the baseline binary classifier; the sentiment classification example and the winner or average ETF label are supervised classification problems.
- [[LM04-Using-Multifactor-Models]]: factor and style membership (value, growth, blend) is encoded with dummies exactly as in the mutual fund example.

## Self-test

> [!question] ST1
> An analyst regresses quarterly EBITDA margin on four independent variables using 60 firms.
> Leverage values for the five largest firms are 0.31, 0.27, 0.24, 0.19, and 0.12.
> Using the curriculum rule of thumb, how many of these five are potentially influential high-leverage points?
> A. Two.
> B. Three.
> C. Five.

> [!question] ST2
> With 30 observations and 4 regressors, an analyst computes a studentized deleted residual of 2.20 for one observation.
> At the 5% level (two-tailed), the observation is:
> A. flagged as potentially influential because 2.20 exceeds the critical value with 25 df.
> B. flagged as potentially influential because 2.20 exceeds the critical value with 24 df.
> C. not flagged because 2.20 is below 3.

> [!question] ST3
> A scatterplot shows one observation with an extreme X value lying almost exactly on the regression line fitted without it.
> Which statement is most accurate?
> A. The observation is a high-leverage point but is unlikely to be influential.
> B. The observation is an outlier and should be deleted.
> C. The observation must have a large studentized residual.

> [!question] ST4
> An analyst wants quarter-of-year effects in a regression of fund flows with an intercept.
> She includes dummies Q1, Q2, Q3, and Q4.
> The most likely consequence is:
> A. the model estimates but the Q4 coefficient is insignificant.
> B. the regression fails because the dummies sum to the intercept column.
> C. the model is fine because each quarter has its own coefficient.

> [!question] ST5
> Estimated model: $Y = 2.0 + 1.5D + 0.8X - 0.3(D \times X)$, where $D = 1$ for foreign firms.
> For a foreign firm with $X = 10$ and a domestic firm with $X = 10$, the difference (foreign minus domestic) in predicted Y is closest to:
> A. $+1.5$.
> B. $-1.5$.
> C. $-3.0$.

> [!question] ST6
> In the model of ST5, the slope of Y with respect to X for foreign firms is:
> A. $-0.3$.
> B. $0.5$.
> C. $0.8$.

> [!question] ST7
> A logit for loan default has a coefficient of 0.6931 on a leverage ratio.
> A one-unit increase in the ratio, other variables constant:
> A. doubles the probability of default.
> B. doubles the odds of default.
> C. raises the log odds of default by $e^{0.6931}$.

> [!question] ST8
> A logit has intercept $-1.2$, coefficient 0.5 on $X$ (continuous) and $-0.8$ on $D$ (dummy).
> For an observation with $X = 2$, $D = 1$, the probability of the event is closest to:
> A. 26.9%.
> B. 36.8%.
> C. 73.1%.

> [!question] ST9
> Unrestricted logit with five regressors has log-likelihood $-191.2$; LL-Null is $-200.5$.
> Using the LR test at 5%, the analyst should:
> A. reject the intercept-only model because $18.6 > 11.07$.
> B. fail to reject because $9.3 < 11.07$.
> C. reject because $18.6 > 9.49$.

> [!question] ST10
> For a fitted logit, three observations have linear index $z$ of $-0.5$, $1.5$, and $2.5$.
> For which observation will a one-unit increase in $z$ produce the largest change in predicted probability?
> A. $z = -0.5$.
> B. $z = 1.5$.
> C. $z = 2.5$.

> [!success]- Answer key
> ST1: A. Cutoff $= 3(k+1)/n = 3 \times 5/60 = 0.25$ (Python: `0.25`).
> Values above 0.25: 0.31 and 0.27, so exactly two are flagged; 0.24 is below the line.
> B tempts by rounding 0.24 up or by using $3k/n = 0.20$, which would flag 0.24 as a third point under the wrong formula.
> C would flag every listed value, which no version of the rule supports since 0.19 and 0.12 are below even 0.20 (V1 p.78).
> ST2: B. $df = n - k - 2 = 30 - 4 - 2 = 24$; critical t at 5% two-tailed is 2.064 (Python: `t.ppf(0.975, 24) = 2.0639`), and $2.20 > 2.064$.
> A uses $n - k - 1 = 25$ df (wrong df; the conclusion happens to be the same but the reasoning is not).
> C applies the outlier rule of thumb instead of the significance test the question asked for (V1 p.80, p.81).
> ST3: A. Extreme X means high leverage; lying on the line fitted without it means removing it barely changes the fit, so it is not influential, and its deleted residual is small, so C is wrong.
> B confuses leverage with outlier status and recommends automatic deletion, which the curriculum warns against (V1 p.77, p.81).
> ST4: B. Four categories need three dummies; including all four with an intercept makes $Q1 + Q2 + Q3 + Q4 = 1$ for every observation, which is perfectly collinear with the intercept, so the regression fails.
> A and C describe outcomes that cannot occur (V1 p.84).
> ST5: B. Foreign: $2.0 + 1.5 + 0.8(10) - 0.3(10) = 8.5$.
> Domestic: $2.0 + 0.8(10) = 10.0$.
> Difference $= 8.5 - 10.0 = -1.5$ (Python: `8.5`, `10.0`).
> A reads only the intercept dummy and ignores the interaction.
> C applies the slope dummy alone ($-0.3 \times 10$) and ignores the intercept shift (V1 p.87).
> ST6: B. Foreign slope $= b_1 + d_1 = 0.8 + (-0.3) = 0.5$.
> A quotes the change in slope.
> C quotes the base group slope (V1 p.87).
> ST7: B. $e^{0.6931} = 2.00$ (Python: `1.9999`), so the odds double.
> A is wrong because probability changes depend on the level of all variables and cannot double in general.
> C misstates the log-odds change, which is 0.6931 itself, not its exponential (V1 p.93).
> ST8: A. $z = -1.2 + 0.5(2) - 0.8(1) = -1.0$; $P = 1/(1 + e^{1}) = 1/3.7183 = 0.2689$ (Python: `0.26894`).
> B is the odds $e^{-1} = 0.368$ mistaken for the probability.
> C is $1 - P$, the sign error in the exponent (V1 p.93).
> ST9: A. $LR = -2(-200.5 - (-191.2)) = -2(-9.3) = 18.6$ (Python: `18.6`); df $= q = 5$ restrictions, critical $\chi^2_5 = 11.07$ (Python: `11.0705`); $18.6 > 11.07$, reject.
> B forgets the factor of 2.
> C uses the 4 df critical value 9.49; the conclusion happens to match but the df are wrong (V1 p.94, p.95).
> ST10: A. Probability changes: from $-0.5$ to $0.5$: $0.6225 - 0.3775 = 0.2449$; from $1.5$ to $2.5$: $0.9241 - 0.8176 = 0.1066$; from $2.5$ to $3.5$: $0.9707 - 0.9241 = 0.0465$ (Python).
> The curve is steepest near $P = 0.5$, that is near $z = 0$, so the observation at $-0.5$ moves most.
> B and C sit in the flattening upper tail (V1 p.93, p.94).

## Flashcards

#flashcards/cfa-l2/01-Quantitative-Methods/lm04

High-leverage point::An observation with an extreme value of an independent variable (V1 p.76).
Outlier (in regression influence analysis)::An observation with an extreme value of the dependent variable relative to its predicted value, giving a large residual (V1 p.77).
Influential observation::One whose exclusion from the sample causes substantial changes in the estimated regression function (V1 p.81).
Leverage rule of thumb::Flag observation i if $h_{ii} > 3(k+1)/n$ (V1 p.78).
Sum of all leverages in a regression::$k + 1$ (V1 p.78).
Range of the leverage measure::Between 0 and 1 (V1 p.78).
Degrees of freedom for the studentized deleted residual test::$n - k - 2$ (V1 p.80).
Absolute rule of thumb for flagging an outlier with studentized residuals::$|t_i^*| > 3$ (V1 p.81).
Studentized deleted residual, full-sample form::$t_i^* = e_i / \sqrt{MSE_{(i)}(1 - h_{ii})}$ (V1 p.80).
Micro-problem: n = 40, k = 3, leverage cutoff?::$3 \times 4 / 40 = 0.30$; keystrokes 3 × 4 ÷ 40 = (V1 p.78).
Micro-problem: n = 96, k = 2, leverage cutoff?::$9/96 = 0.09375$ (V1 p.106).
Micro-problem: n = 26, k = 3, df for studentized residual test?::$26 - 3 - 2 = 21$, critical t at 5% is 2.080 (V1 p.83).
Three remedies for an influential point that is a data error::Correct the data, discard it, or winsorize the dataset, then re-estimate (V1 p.82).
What a valid influential point may signal::An omitted explanatory variable or a violated regression assumption (V1 p.82).
Number of dummies needed for n categories::$n - 1$; the omitted category is the base or control group (V1 p.84).
Why not include a dummy for every category?::The dummies would sum to the intercept column, creating an exact linear relationship among regressors (V1 p.84).
Intercept dummy model::$Y = b_0 + d_0 D + b_1 X + \varepsilon$; D = 1 shifts the line up or down by $d_0$, parallel to the base line (V1 p.84, p.85).
Slope dummy model::$Y = b_0 + b_1 X + d_1 D X + \varepsilon$; D = 1 changes the slope to $b_1 + d_1$ (V1 p.86, p.87).
Difference between groups when both intercept and slope dummies are present::$d_0 + d_1 X$, which depends on the level of X (V1 p.87).
Which coefficient represents the base month in a regression with 11 month dummies?::The intercept; December is the base (V1 p.106).
Micro-problem: value fund AGE slope 0.065, AGE_GROWTH 0.020; growth fund slope on AGE?::$0.065 + 0.020 = 0.085$ (V1 p.89).
Micro-problem: RET = 0.50 - 0.5REG + 0.4MKTSH - 0.2REG_MKTSH; regulated firm's slope on MKTSH?::$0.4 - 0.2 = 0.2$ (V1 p.91).
How to test whether one dummy variable matters::A t test on its coefficient (V1 p.87).
How to test whether a whole set of dummies matters::The joint F test on the block, plus adjusted $R^2$ (V1 p.106).
Linear probability model problem 1::Predicted probabilities can be greater than 1 or less than 0 (V1 p.92).
Linear probability model problem 2::It forces a linear relation between probability and each X over the whole range (V1 p.92).
Odds of an event::$P / (1 - P)$ (V1 p.92).
Logit or log odds::$\ln[P / (1 - P)]$ (V1 p.92).
Logistic regression model::$\ln[P/(1-P)] = b_0 + b_1 X_1 + b_2 X_2 + b_3 X_3 + \varepsilon$ (V1 p.93).
Probability from the logit index z::$P = 1 / (1 + e^{-z})$ (V1 p.93).
Interpretation of a logit slope coefficient::Change in the log odds of the event per unit change in $X_j$, holding other variables constant (V1 p.93).
Interpretation of a logit intercept::Log odds of the event when all independent variables equal zero (V1 p.96).
Odds multiplier for a one-unit increase in $X_j$::$e^{b_j}$ (derived from V1 p.93).
Micro-problem: logit intercept -0.4738; implied probability when all X = 0?::$e^{-0.4738} = 0.6226$; $P = 0.6226 / 1.6226 = 0.3837$ (V1 p.96).
Micro-problem: probability 0.75; odds and log odds?::Odds 3 to 1; log odds $\ln 3 = 1.0986$ (V1 p.92).
Micro-problem: log odds of -1.3863; probability?::$e^{-1.3863} = 0.25$; $P = 0.25/1.25 = 0.20$ (V1 p.93).
Micro-problem: coefficient 0.6931; effect on odds?::Odds multiplied by $e^{0.6931} = 2.0$ (V1 p.93).
Estimation method for logistic regression::Maximum likelihood estimation using the binomial distribution (V1 p.93).
Assumed error distribution in a logit::Logistic distribution, similar to the normal but with fatter tails (V1 p.93).
Where is the marginal effect of X on P largest in a logit?::Near $P = 0.5$, the inflection point of the sigmoid; smallest in the tails (V1 p.93, p.94).
Marginal effect at the means, procedure::Compute P at the means of all X, raise one X by one unit, recompute P, take the difference (V1 p.94).
Likelihood ratio test statistic::$LR = -2(LL_{restricted} - LL_{unrestricted})$, chi-square with q restrictions df (V1 p.94).
Null hypothesis of the LR test::The smaller, restricted model is the better model (V1 p.95).
Sign and reading of the log-likelihood::Always negative; values closer to zero indicate a better fit (V1 p.95).
Micro-problem: LL-Null -312.68, LL -304.20; LR statistic?::$-2(-312.68 + 304.20) = 16.96$; reject at 3 df since 16.96 > 7.815 (V1 p.98).
Micro-problem: LL-Null -200.5, LL -191.2, five regressors; LR and decision at 5%?::$LR = 18.6$ versus $\chi^2_5 = 11.07$; reject the intercept-only model.
When may pseudo-R2 be used?::Only to compare different specifications of the same model on the same dataset (V1 p.93, p.95).
OLS analogue of the LR test::The joint F test comparing restricted and unrestricted nested models (V1 p.94).
Trap: option says a logit slope is "the change in the odds"::Wrong; the raw coefficient is the change in log odds, the odds change by the factor $e^{b_j}$ (V1 p.106).
Trap: option says the logit intercept is "the probability when all X are one"::Wrong on both counts; it is the log odds when all X are zero (V1 p.106).
Trap: "Model 2 fits better because its log-likelihood is lower"::Wrong reasoning; higher (less negative) log-likelihood is better (V1 p.107).
Trap: using all coefficients when told to use only significant ones::Gives 27.4% instead of 36.0% in Practice Problem 12; follow the instruction (V1 p.108).
Trap: flagging only positive studentized residuals::Compare the absolute value with the critical t; negative residuals count too (V1 p.106).
Trap: cutoff $3k/n$ for leverage::Wrong; the numerator is $k + 1$ because the intercept counts (V1 p.78).
In a logit, the effect of a one-unit change in $X_1$ on P depends on {{the level of all the other independent variables}} (V1 p.93).
Studentized residuals detect {{outliers in Y}}; leverage detects {{extreme X values}} (V1 p.82).
Growth funds' AGE slope is the {{sum of the AGE and AGE_GROWTH coefficients}} (V1 p.89).
Logistic regression is widely used for {{binary classification}} problems in machine learning, such as sentiment classification of financial text (V1 p.98).

## Common mistakes

1. Using $3k/n$ instead of $3(k+1)/n$ as the leverage cutoff, which forgets that the intercept is one of the $k+1$ estimated coefficients (V1 p.78).
2. Using $n-k-1$ degrees of freedom for the studentized deleted residual test instead of $n-k-2$; one observation is deleted when the residual is computed (V1 p.80).
3. Comparing signed studentized residuals with the critical value and missing large negative residuals; the rule is on the absolute value (V1 p.81, p.106).
4. Treating every high-leverage point or outlier as influential, or deleting it automatically; influence requires a refit and comparison, and valid unusual points may signal an omitted variable (V1 p.77, p.81, p.82).
5. Including a dummy for every category alongside the intercept, which creates exact collinearity and makes the regression fail (V1 p.84).
6. Reading a dummy coefficient as the level for that group instead of the difference from the base group, and misidentifying the base (the omitted category, whose level is the intercept) (V1 p.84, p.106).
7. Quoting the interaction coefficient as the group's slope rather than the change in slope; the group slope is $b_1 + d_1$ (V1 p.87, p.89).
8. Saying two groups differ by the intercept dummy alone when a slope dummy is also present; the gap is $d_0 + d_1 X$ and changes with $X$ (V1 p.87, p.91).
9. Interpreting a logit coefficient as a change in probability or in odds; it is a change in log odds, the odds multiplier is $e^{b_j}$, and the probability effect depends on all variable levels (V1 p.93, p.106).
10. Reporting the intercept's exponential as a probability without dividing by $1 + e^{b_0}$ (V1 p.96).
11. Sign errors in $P = 1/(1 + e^{-z})$, which flip $P$ into $1 - P$ (for example 82.2% instead of 36.0%) (V1 p.108).
12. Ranking models by "lower" log-likelihood, or subtracting in the wrong order in the LR statistic; higher log-likelihood is better and $LR = -2(LL_R - LL_U)$ is positive (V1 p.95, p.107).
13. Comparing pseudo-$R^2$ across models built on different datasets (V1 p.95).
14. Applying an LR test to two non-nested models such as Regressions 1 and 2 in the practice set; the LR test requires restrictions on a common model (V1 p.95).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "01-04" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
