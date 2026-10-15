---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 7
title: "Larkspur Equity Restaurant Sales Beat Model"
los: [los-01-07-b, los-01-07-e, los-01-07-f]
difficulty: 3
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Larkspur Equity Restaurant Sales Beat Model

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Larkspur Equity Partners runs a long-only consumer fund with a large allocation to listed North American restaurant chains.
Portfolio manager Adaeze Nwankwo has asked analyst Tomasz Wierzbicki to build a supervised model that predicts whether a chain's quarterly same-store sales will beat (1) or miss (0) the consensus estimate.
The model combines structured location data with the sentiment of online customer reviews.

Wierzbicki licenses weekly foot traffic counts for 3,900 restaurant locations from a mobile geolocation vendor at a cost of USD 85,000 a year, and he merges them with location-level sales reported by the chains.
While preparing the structured data, he performs four actions:

- Action 1: for each location, he adds dine-in sales, third-party delivery sales, and catering sales into a single total sales variable.
- Action 2: he deletes the rows for 62 locations that closed permanently before the start of the sample period.
- Action 3: he translates the sales of Canadian locations from Canadian dollars into US dollars at each quarter's average exchange rate.
- Action 4: he deletes the street address column because each location already has a unique location ID.

A histogram of weekly foot traffic is close to bell-shaped, and Wierzbicki confirms that no location lies more than three standard deviations from the mean.
He therefore decides to rescale foot traffic to a mean of 0 and a standard deviation of 1 before training.
Summary statistics for the cleansed variable are in Exhibit 1.

**Exhibit 1: Weekly foot traffic per location (visits, n = 3,838)**

| Statistic | Value |
|---|---|
| Mean | 4,820 |
| Median | 4,550 |
| Standard deviation | 1,150 |
| Minimum | 1,610 |
| Maximum | 8,190 |
| Skewness | 0.12 |

One location of the chain Copperkettle Grill records weekly foot traffic of 7,005 visits.

For the text component, Wierzbicki scrapes 186,000 customer reviews from a public review website.
Each review carries a star rating, which he uses to label it positive or negative.
After cleansing, tokenization, lowercasing, and stemming, he ranks candidate tokens for a review sentiment classifier.
For each token he computes the collection-level term frequency and the mutual information between token occurrence and the positive and negative review classes.
Selected results are in Exhibit 2.

**Exhibit 2: Selected stemmed tokens from customer reviews**

| Token | Collection-level term frequency | Mutual information |
|---|---|---|
| order | 0.0184 | 0.0035 |
| food | 0.0096 | 0.0006 |
| friendli | 0.0017 | 0.0412 |
| cold | 0.0021 | 0.0694 |

The classifier's output, a sentiment score for each chain, becomes one feature in the sales beat model.

Wierzbicki trains a logistic regression on the combined features and evaluates it on a holdout test set of 400 chain-quarters.
The results are in Exhibit 3.

**Exhibit 3: Test set confusion matrix (400 chain-quarters)**

| | Actual beat (1) | Actual miss (0) |
|---|---|---|
| Predicted beat (1) | 116 | 44 |
| Predicted miss (0) | 28 | 212 |

On 18 August, Nwankwo describes how the fund will use the model: "We will add to a position only when the model predicts a beat.
The mistake that hurts us is buying a chain ahead of a quarter that turns out to be a miss, because those stocks gap down on the release.
Failing to predict a beat just means we sit out a quarter, and that costs us very little."

## Questions

1. The data transformations in Actions 1, 2, and 3, respectively, are best described as: (LOS: los-01-07-b)
   - A. aggregation, selection, and conversion.
   - B. extraction, filtration, and conversion.
   - C. aggregation, filtration, and conversion.
2. After Wierzbicki's planned rescaling, the foot traffic value for the Copperkettle Grill location is closest to: (LOS: los-01-07-b)
   - A. 0.820.
   - B. 1.900.
   - C. 2.135.
3. Based on Exhibit 2, the token with the greatest power to discriminate between positive and negative reviews is: (LOS: los-01-07-e)
   - A. "food".
   - B. "order".
   - C. "cold".
4. Given Nwankwo's 18 August comments, the performance measure that best reflects the fund's concern, and its value from Exhibit 3, are closest to: (LOS: los-01-07-f)
   - A. precision, 0.725.
   - B. recall, 0.806.
   - C. accuracy, 0.820.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Adding dine-in, delivery, and catering sales into one total sales variable combines two or more variables into one, which is aggregation, the curriculum's salary plus other income example (V1 p.284).
> Deleting rows that are not needed, here the locations closed before the sample period, is filtration (V1 p.284).
> Translating CAD into USD is conversion, which covers currency, units, and data types (V1 p.285).
> Action 4, deleting an unneeded column, is the selection case and is a decoy.
> A is wrong because selection removes columns, not rows; Action 2 removes rows.
> B is wrong because extraction creates a new variable from a single existing one, such as age from a date of birth, whereas Action 1 sums several variables into one.
> 2. **B.** Rescaling to mean 0 and standard deviation 1 is standardization, which suits this variable because its distribution is close to normal and the three standard deviation check found no outliers (V1 p.285, p.286).
> $X^{\text{std}} = (7{,}005 - 4{,}820) / 1{,}150 = 2{,}185 / 1{,}150 = 1.9000$.
> A is wrong because $(7{,}005 - 1{,}610) / (8{,}190 - 1{,}610) = 5{,}395 / 6{,}580 = 0.8199$ is the normalized value on a scale of 0 to 1, which is not the rescaling Wierzbicki chose.
> C is wrong because $(7{,}005 - 4{,}550) / 1{,}150 = 2{,}455 / 1{,}150 = 2.1348$ centres on the median instead of the mean.
> 3. **C.** Mutual information is 0 when a token is distributed the same way across classes and approaches 1 as the token concentrates in one class, so the highest value, 0.0694 for "cold", marks the most discriminating token (V1 p.302, p.303).
> A is wrong because "food" has the lowest mutual information, 0.0006, so it appears in positive and negative reviews almost equally; choosing it reads the measure backwards.
> B is wrong because "order" has the highest collection-level term frequency, 0.0184, but frequency measures how common a token is, not whether it separates the classes; the most frequent tokens behave like stop words and cause underfitting (V1 p.302).
> 4. **A.** Buying ahead of a quarter that turns out to be a miss means the model predicted 1 when the actual was 0, a false positive or Type I error, so precision is the relevant measure (V1 p.312, p.313).
> $P = TP / (TP + FP) = 116 / (116 + 44) = 116 / 160 = 0.7250$.
> B is wrong because recall, $116 / (116 + 28) = 116 / 144 = 0.8056$, guards against false negatives, the missed beats that Nwankwo says cost little.
> C is wrong because accuracy, $(116 + 212) / 400 = 328 / 400 = 0.8200$, weights both error types equally and is inflated by the majority miss class (256 of 400 actual outcomes, so a model that always predicts a miss scores 0.64); for reference, $F_1 = 2 \times 0.7250 \times 0.8056 / (0.7250 + 0.8056) = 1.1681 / 1.5306 = 0.7632$ (V1 p.313, p.314).

## Distractor design

1. A: treats row removal (filtration) as column removal (selection); B: labels a sum of several variables as extraction instead of aggregation.
2. A: wrong formula variant (normalization instead of standardization); C: misread exhibit, centring on the median instead of the mean.
3. A: reads mutual information backwards (lowest instead of highest); B: confuses high term frequency with discriminatory power.
4. B: reverses Type I and Type II cost (recall instead of precision); C: picks the headline accuracy measure, which ignores the stated asymmetric cost.
