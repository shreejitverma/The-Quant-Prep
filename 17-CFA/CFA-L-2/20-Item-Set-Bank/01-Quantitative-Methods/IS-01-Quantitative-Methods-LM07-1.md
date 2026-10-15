---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 7
title: "Halvorsen Mutual Policy Lapse Model"
los: [los-01-07-a, los-01-07-b, los-01-07-d, los-01-07-c]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Halvorsen Mutual Policy Lapse Model

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Ingrid Solberg is a data analyst at Halvorsen Mutual, a Norwegian property and casualty insurer that writes commercial policies for small and mid-sized firms.
Her manager, Marcus Oyelaran, has asked her to build a supervised machine learning model that predicts whether a commercial policyholder will lapse, that is, fail to renew, within the next 12 months.
The retention team will use the model output, a binary lapse flag, to decide which brokers to contact before renewal dates.

On 3 March, Solberg met Halvorsen's database administrator to clarify the schema of the policy administration system, downloaded five years of policy records, and read the Readme files that accompanied a broker extract purchased from an outside vendor.
She then pulled a raw sample to check data quality, shown in Exhibit 1.

**Exhibit 1: Raw policy sample (premium in NOK thousands)**

| ID | Inception date | Annual premium | Employees | Claims since inception | Prior insurer | Years with prior insurer |
|---|---|---|---|---|---|---|
| 101 | 04/02/2019 | 212 | 38 | 1 | Fjord Forsikring | 4 |
| 102 | 17 Jan 2021 | 96 | -14 | 0 | Nordvest | 2 |
| 103 | 30/11/2018 | 344 | 120 | 2 | None | 6 |
| 104 | 09/09/2020 | 158 | 55 | not recorded | Nordvest | 3 |
| 105 | 22/06/2017 | | 21 | 0 | Fjord Forsikring | 1 |
| 106 | 04/02/2019 | 212 | 38 | 1 | Fjord Forsikring | 4 |

Every claim filed by a Halvorsen policyholder is processed through Halvorsen's own claims system.

After cleansing, Solberg examined the annual premium variable across 2,400 policies.
Summary statistics are shown in Exhibit 2.

**Exhibit 2: Annual premium after cleansing (NOK thousands, n = 2,400)**

| Statistic | Value |
|---|---|
| Minimum | 18 |
| First quartile | 142 |
| Median | 215 |
| Third quartile | 318 |
| Maximum | 1,460 |
| Mean | 247 |
| Standard deviation | 131 |
| Skewness | 2.8 |

Because the premium distribution is strongly right-skewed, Solberg decides to flag outliers using the interquartile range method with the conventional multiple.
She will winsorize any flagged value by replacing it with the bound it breached, and then rescale premium to the range 0 to 1 using the full winsorized sample.

For data exploration, Solberg creates an indicator variable, large_employer, equal to 1 when a policyholder has more than 250 employees.
She also converts the seven-level industry code into seven binary columns.

Solberg trains three logistic regression specifications and reports classification error rates in Exhibit 3.

**Exhibit 3: Classification error rates**

| Specification | Features | Training error | Cross-validation error |
|---|---|---|---|
| Model 1 | All 64 raw features | 4.1% | 17.8% |
| Model 2 | 12 features chosen by chi-square ranking | 22.6% | 23.9% |
| Model 3 | Model 2 plus large_employer and industry columns | 9.8% | 11.2% |

Oyelaran reviews the results on 21 March and comments, "Model 2 is attractive because its training and cross-validation errors are nearly identical, so it generalises well."

## Questions

1. Solberg's activities on 3 March are best classified in the structured data project step of: (LOS: los-01-07-a)
   - A. conceptualization.
   - B. data collection.
   - C. data preparation and wrangling.
2. The data errors in the rows for ID 103 and ID 104 of Exhibit 1, respectively, are best described as: (LOS: los-01-07-b)
   - A. inconsistency and inaccuracy.
   - B. inconsistency and incompleteness.
   - C. non-uniformity and invalidity.
3. Based on Exhibit 2 and Solberg's chosen outlier method, the premium value above which a policy is flagged as an outlier is closest to: (LOS: los-01-07-b)
   - A. NOK 582 thousand.
   - B. NOK 640 thousand.
   - C. NOK 846 thousand.
4. After Solberg's planned outlier treatment, the rescaled premium for a policy with an annual premium of NOK 265 thousand is closest to: (LOS: los-01-07-b)
   - A. 0.137.
   - B. 0.171.
   - C. 0.438.
5. Solberg's creation of large_employer and the seven industry columns is best described as: (LOS: los-01-07-d)
   - A. feature selection, part of data exploration.
   - B. feature engineering, part of data exploration.
   - C. data extraction, part of data preparation and wrangling.
6. Based on Exhibit 3, is Oyelaran's comment on Model 2 correct? (LOS: los-01-07-c)
   - A. Yes.
   - B. No, because Model 2 is overfit and has high variance error.
   - C. No, because Model 2 is underfit and has high bias error.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Clarifying the database schema with an administrator, downloading the records, and reading the Readme files that accompany vendor data are the practical tasks of data collection, the second structured step (V1 p.278, p.281).
> A is wrong because conceptualization was Oyelaran's definition of the output (a binary lapse flag), its users (the retention team), and how it embeds in the business; that preceded 3 March.
> C is wrong because preparation and wrangling begins after collection, with cleansing and preprocessing of the downloaded data.
> 2. **A.** ID 103 lists "None" as prior insurer yet records 6 years with a prior insurer, a conflict between two fields, so inconsistency (V1 p.283).
> ID 104 shows claims since inception as "not recorded", but every claim filed since inception passed through Halvorsen's own system, so the true value is knowable and the entry is not a measure of it, so inaccuracy (V1 p.283, p.287).
> B is wrong because it treats the knowable "not recorded" as a missing value; the blank premium for ID 105 is the incompleteness case.
> C is wrong because both of its errors sit in the row for ID 102: non-uniformity is its "17 Jan 2021" date format and invalidity is its negative employee count.
> 3. **A.** $\text{IQR} = 318 - 142 = 176$.
> Upper bound $= Q_3 + 1.5 \times \text{IQR} = 318 + 264 = 582$ (V1 p.285).
> The lower bound $142 - 264 = -122$ is below the minimum of 18, so no low outliers exist.
> B is wrong because $247 + 3 \times 131 = 640$ is the three standard deviation rule, which applies only to normal data and Exhibit 2 shows skewness of 2.8.
> C is wrong because $318 + 3.0 \times 176 = 846$ uses the multiple that flags extreme values, not the conventional 1.5.
> 4. **C.** Winsorization replaces each value above the upper bound with 582, so the new maximum is 582; no value breaches the lower bound of -122, so the minimum stays 18.
> Normalized value $= (265 - 18) / (582 - 18) = 247 / 564 = 0.4379$ (V1 p.285, p.286).
> A is wrong because $(265 - 247) / 131 = 0.1374$ is the standardized value, but Solberg rescales to the range 0 to 1.
> B is wrong because $(265 - 18) / (1{,}460 - 18) = 247 / 1{,}442 = 0.1713$ uses the pre-winsorization maximum, which is exactly the outlier sensitivity that winsorizing first is meant to remove.
> 5. **B.** An indicator built from domain knowledge (the income_above_100k analogue) and one hot encoding of a categorical variable into binary columns are the curriculum's examples of feature engineering, one of the three data exploration tasks (V1 p.300).
> A is wrong because feature selection keeps or drops existing features without creating new ones.
> C is wrong because extraction in preprocessing is the creation of a basic derived variable such as age from a date; one hot encoding and domain indicators are named as feature engineering.
> 6. **C.** Model 2 has close errors, but both are large (22.6% and 23.9%) relative to Model 3 (9.8% and 11.2%), so it is underfit with high bias; high training error signals bias (V1 p.316).
> Too few features cause underfitting, and Model 3 shows that feature engineering cured it (V1 p.310).
> A is wrong because a small gap alone is not a good fit; the errors must also be small.
> B is wrong because the overfit specification is Model 1, with CV error far above training error (17.8% against 4.1%).

## Distractor design

1. A: confuses the planning step with collection; C: places any data handling after conceptualization into wrangling.
2. B: treats a knowable but unrecorded value as missing (inaccuracy vs incompleteness); C: misreads the exhibit, taking errors from other rows.
3. B: wrong formula variant (three standard deviation rule on skewed data); C: wrong multiple (3.0 extreme-value bound).
4. A: standardization instead of normalization; B: uses the raw maximum, ignoring the winsorization step.
5. A: confuses feature selection with feature engineering; C: confuses preprocessing extraction with exploration-stage engineering.
6. A: reads a small gap as a good fit; B: reverses the bias and variance diagnosis.
