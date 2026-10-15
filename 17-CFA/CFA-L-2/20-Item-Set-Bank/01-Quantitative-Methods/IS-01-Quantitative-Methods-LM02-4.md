---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 2
title: "Aldermoor Energy peak-load hedging models"
los: [los-01-02-a, los-01-02-b, los-01-02-c]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Aldermoor Energy peak-load hedging models

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Aldermoor Energy is a regional electric utility that buys forward power contracts each month to cover its expected peak demand.
Treasurer Marcus Feld sets the hedge volume from a regression forecast of next month's peak load, measured in megawatts (MW).
Ingrid Solberg, a treasury analyst, received three nested models from an external weather-analytics vendor, each estimated on n = 60 months.
The independent variables are cooling degree days (CDD), heating degree days (HDD), industrial production growth (IP, percent), the average wholesale power price (PRICE, USD per MWh) and regional employment growth (EMP, percent).

Model 1 uses CDD and HDD.
Model 2 adds IP.
Model 3 adds PRICE and EMP to Model 2.
The vendor report shows coefficients and R-squared only; standard errors and t-statistics were not delivered.
The total sum of squares of peak load is 4,860,000 MW squared for all three models.

Exhibit 1. Vendor report

| Item | Model 1 | Model 2 | Model 3 |
|---|---|---|---|
| Intercept | 1,812 | 1,850 | 1,905 |
| CDD | 4.31 | 4.20 | 4.12 |
| HDD | 1.42 | 1.35 | 1.31 |
| IP | | 22.0 | 19.5 |
| PRICE | | | -1.10 |
| EMP | | | 11.8 |
| R-squared | 0.7120 | 0.7275 | 0.7330 |
| Mean peak load (MW) | 2,640 | 2,640 | 2,640 |

Exhibit 2. Assumptions for July 2026

| CDD | HDD | IP | PRICE | EMP |
|---|---|---|---|---|
| 310 | 8 | -1.5 | 58 | 0.4 |

The CDD and HDD figures are a meteorological forecast, and IP is the treasury's own economic forecast.
For Model 2 and these assumptions the vendor's software gives a standard error of the forecast of 172 MW.

Selected values: $\ln(60) = 4.0943$; $t_{0.025}(56) = 2.003$; $F_{0.05}(2, 54) = 3.168$; $F_{0.05}(3, 54) = 2.776$.

On 20 June 2026, Feld and Solberg discussed the choice of model.

Feld: "Model 3 has the highest R-squared, so it is the most reliable. The vendor also offered a twelve-variable model with an R-squared of 0.7600, which is even better. Whichever model we use, the 95% range for July is simply the forecast plus or minus about two standard errors of estimate."

Solberg: "R-squared cannot tell us when to stop adding variables. I will rank the models on adjusted R-squared and the information criteria, check whether IP and whether PRICE and EMP earn their places, and build the July range from the standard error of the forecast, because our weather and production inputs are themselves forecasts."

Feld will hedge a volume equal to the lower bound of the 95% prediction interval for July.

## Questions

1. The model with the highest adjusted R-squared, and that adjusted R-squared, are: (LOS: los-01-02-a)
   - A. Model 2, 0.713
   - B. Model 3, 0.733
   - C. Model 3, 0.756
2. The absolute value of the t-statistic of IP in Model 2, and its significance at the 5% level, are closest to: (LOS: los-01-02-b)
   - A. 1.74; not significant
   - B. 1.78; not significant
   - C. 3.19; significant
3. The F-statistic for the joint test that the PRICE and EMP coefficients are both zero, and the conclusion at the 5% level, are: (LOS: los-01-02-b)
   - A. 0.56; fail to reject
   - B. 1.11; fail to reject
   - C. 1.42; fail to reject
4. $AIC_2 - AIC_1$, $BIC_2 - BIC_1$, and the model Solberg should use for the July hedge forecast are closest to: (LOS: los-01-02-a)
   - A. -1.32, +0.78, Model 1
   - B. -1.32, +0.78, Model 2
   - C. +0.56, +2.65, Model 1
5. Using Model 2, the predicted July peak load is closest to: (LOS: los-01-02-c)
   - A. 3,104 MW
   - B. 3,130 MW
   - C. 3,196 MW
6. Regarding Feld's twelve-variable model, which evaluation is most accurate? (LOS: los-01-02-a)
   - A. Its R-squared of 0.760 exceeds that of every vendor model, so it fits best.
   - B. Its adjusted R-squared is about 0.809, above Model 2's, so it should replace Model 2.
   - C. Its adjusted R-squared is about 0.699, below Model 2's, so the extra variables do not justify their degrees of freedom.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** $\bar{R}^2 = 1 - \left(\frac{n-1}{n-k-1}\right)(1 - R^2)$.
>    Model 1: $1 - (59 / 57)(0.2880) = 0.70189$; Model 2: $1 - (59 / 56)(0.2725) = 0.71290$; Model 3: $1 - (59 / 54)(0.2670) = 0.70828$.
>    Model 2 is highest; adding PRICE and EMP raised R-squared by 0.0055 but lowered adjusted R-squared.
>    B is wrong because 0.733 is Model 3's unadjusted R-squared, which is always highest for the largest model.
>    C is wrong because it inverts the degrees-of-freedom factor, $1 - (54 / 59)(0.2670) = 0.75563$, which rewards rather than penalises extra variables.
> 2. **B.** Adding one variable is a nested test with $q = 1$, and its F equals the square of the added variable's t-statistic.
>    Because $SSE = SST(1 - R^2)$ and SST is common, $F = \frac{(0.2880 - 0.2725) / 1}{0.2725 / 56} = \frac{0.0155}{0.0048661} = 3.1853$, so $|t| = \sqrt{3.1853} = 1.7847$.
>    1.78 is below $t_{0.025}(56) = 2.003$, so IP is not significant at 5%, although $|t| > 1$ explains why adjusted R-squared rose from Model 1 to Model 2.
>    A is wrong because it puts the restricted model's residual share in the denominator in place of the unrestricted one, $0.0155 / (0.2880 / 56) = 3.0139$, and $\sqrt{3.0139} = 1.7361$.
>    C is wrong because 3.19 is the F-statistic, not its square root.
> 3. **A.** $H_0: b_{PRICE} = b_{EMP} = 0$; restricted Model 2, unrestricted Model 3, $q = 2$, $n - k - 1 = 54$.
>    In SSE terms: $SSE_2 = 4{,}860{,}000 \times 0.2725 = 1{,}324{,}350$ and $SSE_3 = 4{,}860{,}000 \times 0.2670 = 1{,}297{,}620$.
>    $F = \frac{(1{,}324{,}350 - 1{,}297{,}620) / 2}{1{,}297{,}620 / 54} = \frac{13{,}365}{24{,}030} = 0.5562$, the same as $\frac{0.0055 / 2}{0.2670 / 54}$.
>    0.56 is below 3.168, so fail to reject; PRICE and EMP do not jointly explain peak load.
>    B is wrong because it does not divide the rise in SSE by $q$, $0.0055 / 0.0049444 = 1.1124$.
>    C is wrong because it uses Model 1 as the restricted model with $q = 3$, $(0.0210 / 3) / 0.0049444 = 1.4157$, which tests IP, PRICE and EMP together rather than the pair named.
> 4. **B.** The first term of both criteria is $n \ln(SSE / n)$; the change from Model 1 to Model 2 is $60 \ln(0.2725 / 0.2880) = -3.3193$.
>    $AIC_2 - AIC_1 = -3.3193 + 2(1) = -1.3193$; $BIC_2 - BIC_1 = -3.3193 + 4.0943(1) = +0.7750$.
>    Full values: $AIC_1 = 609.4446$, $AIC_2 = 608.1253$, $AIC_3 = 610.9019$; $BIC_1 = 615.7276$, $BIC_2 = 616.5026$, $BIC_3 = 623.4679$.
>    AIC, the prediction criterion, is lowest for Model 2, so the hedge forecast should use Model 2; BIC would pick Model 1 as the best-fitting model.
>    A is wrong because it applies BIC, the goodness-of-fit criterion, to a prediction task.
>    C is wrong because it uses the common logarithm, $60 \log_{10}(0.2725 / 0.2880) = -1.4416$, giving $-1.4416 + 2 = +0.5584$ and $-1.4416 + 4.0943 = +2.6528$.
> 5. **B.** $\hat{Y} = 1{,}850 + 4.20(310) + 1.35(8) + 22.0(-1.5) = 1{,}850 + 1{,}302.0 + 10.8 - 33.0 = 3{,}129.8$ MW.
>    PRICE and EMP are not in Model 2, so their assumptions are not used.
>    A is wrong because it uses Model 3, the highest R-squared model: $1{,}905 + 1{,}277.2 + 10.48 - 29.25 - 63.8 + 4.72 = 3{,}104.35$ MW.
>    C is wrong because it adds the IP term instead of subtracting it, $3{,}129.8 + 66.0 = 3{,}195.8$ MW.
>    For reference, the 95% interval is $3{,}129.8 \pm 2.003 \times 172 = 3{,}129.8 \pm 344.5$, or 2,785 MW to 3,474 MW, so Feld hedges about 2,785 MW; using SEE $= \sqrt{1{,}324{,}350 / 56} = 153.78$ would give a narrower 2,822 MW to 3,438 MW and overstate the hedge.
> 6. **C.** With $k = 12$, $n - k - 1 = 47$ and $\bar{R}^2 = 1 - (59 / 47)(1 - 0.7600) = 1 - 0.30128 = 0.69872$.
>    That is below Model 2's 0.71290: nine extra variables raised R-squared by 0.0325 but consumed more degrees of freedom than they repaid, the curriculum's picture of overfitting.
>    A is wrong because R-squared never falls when variables are added, so it cannot judge parsimony.
>    B is wrong because it inverts the degrees-of-freedom factor, $1 - (47 / 59)(0.2400) = 0.80881$.

## Distractor design

1. B: unadjusted R-squared used to rank models; C: degrees-of-freedom factor inverted.
2. A: restricted model's residual sum of squares used in the denominator; C: F-statistic reported without taking the square root.
3. B: rise in SSE not divided by $q$; C: wrong restricted model ($q = 3$, Model 1).
4. A: BIC applied to a prediction purpose; C: common logarithm used instead of natural logarithm.
5. A: forecast taken from the highest R-squared model rather than the model selected for prediction; C: sign error on a negative assumed value.
6. A: model judged on R-squared; B: degrees-of-freedom factor inverted.
