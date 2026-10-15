---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 7
title: "Coastal Teachers Office Vacancy Nowcast"
los: [los-01-07-a, los-01-07-d, los-01-07-f]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Coastal Teachers Office Vacancy Nowcast

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Coastal Teachers' Retirement System is a public pension plan with a large direct office real estate portfolio.
Its research head, Samuel Achterberg, must report to the investment committee each quarter on the expected office vacancy rate in the plan's metropolitan markets.
He has assigned analyst Mei-Lin Harrow to build a machine learning nowcast that combines structured market data with local business news.

The project has three components.
First, a regression model predicts next-quarter office vacancy (in percent) for each market from 40 structured features, including sublease space, employment growth, and construction completions.
Second, a text classifier labels local business news articles as signalling tenant expansion or tenant contraction; its output will become an additional feature in the regression.
Third, an exploratory topic model groups 22,000 unlabelled news articles into themes for the committee report.

For the classifier, Harrow wrote a web spider that scraped articles from 60 regional business news sites, and two of the plan's leasing specialists labelled 1,150 articles as expansion or contraction.
After cleansing and normalization, the classifier's document term matrix has 1,150 rows and 38,000 token columns.

On 8 July, Harrow summarizes the text work in two statements:

- Statement 1: "Scraping the news sites with a web spider and having our leasing specialists label the articles is text curation, the second step of the text project."
- Statement 2: "Building word clouds and ranking tokens by chi-square belongs to text preparation and wrangling, the third step of the text project."

For the structured features, Harrow plans the exploration stage.
She writes: "I will draw scatterplots of vacancy against each continuous feature, confirm any visible relationship with a Pearson or Spearman correlation test, and then run principal components analysis on the 40 features.
PCA is our feature selection step, because it reduces the number of features while leaving each original feature unchanged."

Achterberg asks which algorithm suits the classifier and how the unlabelled topic model dataset should be partitioned.
He notes that the committee cares about the size of vacancy forecast errors in percentage points, and that a single large miss in a major market is more damaging to the plan's leasing strategy than several small ones.

Harrow then compares two candidate regression specifications on five holdout markets.
The committee's operating budget for the project is USD 180,000.

**Exhibit 1: Holdout predictions of next-quarter office vacancy (%)**

| Market | Actual | Model X | Model Y |
|---|---|---|---|
| 1 | 14.2 | 15.0 | 14.0 |
| 2 | 18.6 | 17.1 | 19.9 |
| 3 | 11.9 | 12.5 | 11.5 |
| 4 | 21.4 | 19.8 | 23.9 |
| 5 | 16.0 | 16.9 | 15.6 |

Achterberg wants the specification with the better fit under the performance measure the curriculum recommends for continuous predictions.

## Questions

1. Which of Harrow's 8 July statements is correct? (LOS: los-01-07-a)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.
2. Harrow's exploration plan for the structured features is most likely incorrect with respect to: (LOS: los-01-07-d)
   - A. the use of scatterplots, because a histogram is required for continuous features.
   - B. the confirmation test, because a visual relationship does not need statistical confirmation.
   - C. her description of PCA, because it creates new combinations of features rather than selecting among the original features.
3. For the classifier, the method best suited to the size of the data, and the share of the 22,000-article topic model dataset that should be allocated to a training subset, are: (LOS: los-01-07-f)
   - A. a neural network; 60%.
   - B. a support vector machine; 60%.
   - C. a support vector machine; 0%.
4. Based on Exhibit 1, the preferred specification and its performance measure are closest to: (LOS: los-01-07-f)
   - A. Model X, 1.15.
   - B. Model X, 1.32.
   - C. Model Y, 0.96.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Text curation, the second text step, gathers external text through web services or web spidering and may use experts to annotate target labels for supervised learning (V1 p.278).
> Statement 2 is wrong because word clouds and chi-square feature selection belong to text exploration, the fourth step; text preparation and wrangling, the third step, is cleansing and preprocessing (V1 p.279, p.301, p.302).
> B and C are wrong because each accepts Statement 2.
> 2. **C.** PCA is dimensionality reduction, which creates new uncorrelated combinations of the features; feature selection includes or excludes existing features without altering them (V1 p.297, p.300).
> A is wrong because scatterplots are the standard multi-dimensional EDA tool for the relationship between two continuous variables; histograms show one variable's distribution (V1 p.296, p.297).
> B is wrong because the curriculum requires a visual relationship to be confirmed statistically, using parametric tests such as Pearson correlation or non-parametric tests such as Spearman rank correlation (V1 p.298).
> 3. **C.** With 38,000 features and only 1,150 instances the data are "wide", which suits a support vector machine, and SVMs also suit text (V1 p.310, p.311).
> The topic model is unsupervised because the 22,000 articles have no labels, so no training, validation, or test split is needed and 0% is allocated to a training subset (V1 p.311).
> A is wrong because neural networks suit "long" data with far more instances than features, and 60% is the supervised training share.
> B is wrong because it applies the supervised 60:20:20 split to an unlabelled dataset.
> 4. **A.** RMSE is the performance measure for continuous prediction (V1 p.315).
> Model X errors: $0.8, -1.5, 0.6, -1.6, 0.9$; squared: $0.64, 2.25, 0.36, 2.56, 0.81$; sum $6.62$; mean $1.3240$; $\text{RMSE}_X = \sqrt{1.3240} = 1.1507$.
> Model Y errors: $-0.2, 1.3, -0.4, 2.5, -0.4$; squared: $0.04, 1.69, 0.16, 6.25, 0.16$; sum $8.30$; mean $1.6600$; $\text{RMSE}_Y = \sqrt{1.6600} = 1.2884$.
> Model X has the lower RMSE, so it is preferred.
> B is wrong because 1.32 is Model X's mean squared error; the square root was omitted.
> C is wrong because 0.96 is Model Y's mean absolute error, $(0.2 + 1.3 + 0.4 + 2.5 + 0.4)/5 = 0.96$, which is lower than Model X's 1.08; RMSE squares errors and so penalises Model Y's 2.5 point miss in market 4 more heavily.

## Distractor design

1. B and C: place text exploration tasks (word clouds, chi-square) in the preparation and wrangling step.
2. A: mismatches visualization to data type; B: skips the statistical confirmation step; the correct answer separates dimensionality reduction from feature selection.
3. A: wrong data-shape rule (neural networks for wide data) plus a supervised split; B: supervised split applied to unlabelled data.
4. B: omits the square root (MSE instead of RMSE); C: wrong formula variant (mean absolute error), which reverses the ranking.
