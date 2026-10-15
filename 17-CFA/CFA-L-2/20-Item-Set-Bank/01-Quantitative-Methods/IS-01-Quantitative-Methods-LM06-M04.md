---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 6
title: "Oberwald Private Wealth Client Analytics"
los: [los-01-06-a, los-01-06-b, los-01-06-c, los-01-06-d]
difficulty: 3
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Oberwald Private Wealth Client Analytics

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Oberwald Private Wealth is a Zurich-based wealth manager with about 48,000 client relationships.
Liesel Brandvold, head of client analytics, has asked data scientist Anselm Quiroga to build machine learning tools for the executive committee.
Every client record carries 20 standardized features, including assets under management, tenure, number of products held, portfolio drawdown over the past year, and frequency of contact with the relationship manager.

Workstream 1 predicts whether a client will close all accounts within the next 12 months.
The historical data mark each of 31,500 current and former clients as having left (1) or stayed (0).
Quiroga partitions these records at random into training, validation and test samples.
He first tunes the maximum depth of a single classification tree on the validation sample.
For each depth, his software decomposes the estimated out-of-sample error rate as shown in Exhibit 1.
The base error rate is estimated at 3.0% at every depth.

Exhibit 1: Error decomposition for the single classification tree

| Maximum depth | Terminal nodes | Bias error | Variance error |
|---|---|---|---|
| 2 | 4 | 12.1% | 0.9% |
| 4 | 15 | 8.4% | 2.0% |
| 6 | 38 | 5.6% | 3.6% |
| 8 | 87 | 3.7% | 6.1% |
| 10 | 164 | 2.2% | 9.4% |

Quiroga then fits a random forest of classification trees trained by bagging, in which each tree considers a random subset of 4 of the 20 features at every split.
For the committee he presents an illustrative forest of nine trees.
Exhibit 2 shows, for client 7741, the proportion of training clients who left among those at the terminal node that each tree assigns to the client.
Client 7741 has assets under management of CHF 3.8 million and a tenure of 11 years.

Exhibit 2: Proportion of "left" at client 7741's terminal node, by tree

| Tree | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| Proportion left | 0.91 | 0.46 | 0.84 | 0.43 | 0.88 | 0.47 | 0.41 | 0.93 | 0.44 |

Workstream 2 forecasts each client's net new assets, in Swiss francs, over the next 12 months, using the same 20 features and the recorded net new assets of past years.
Relationship managers will afterward place each client into a "growing", "stable" or "shrinking" band for their call plans.

Workstream 3 uses the text of 310,000 archived call-center transcripts, each already tagged by staff with one of 12 complaint categories, to assign every new transcript to a category.
Quiroga proposes a neural network with six hidden layers for this task.

Separately, the executive committee has decided to reorganize the service model around exactly five client service tiers.
It wants the tiers built from the 20 client features rather than from assets alone, and many of those features are highly correlated.
On 5 November 2026, Brandvold and Quiroga discuss the tiering project.

Brandvold: "We could run principal components analysis on the 20 features and keep five components.
Each component would then be one service tier."

Quiroga: "I ran k-means with k = 5 twice, from different initial centroids, and the two runs placed about 6% of clients in different tiers.
That tells me k-means is unreliable here, so I would switch to agglomerative hierarchical clustering."

## Questions

1. Workstream 2 and Workstream 3 are best described, respectively, as: (LOS: los-01-06-a)
   - A. supervised classification, and supervised classification using deep learning.
   - B. supervised regression, and supervised classification using deep learning.
   - C. supervised regression, and unsupervised clustering, because the 12 complaint categories are groups of similar transcripts.
2. Based on Exhibit 1, the maximum depth Quiroga should select and its estimated out-of-sample error rate are closest to: (LOS: los-01-06-b)
   - A. depth 6, with an error rate of 9.2%.
   - B. depth 10, with an error rate of 5.2%.
   - C. depth 6, with an error rate of 12.2%.
3. Based on Exhibit 2, the illustrative random forest classifies client 7741 as: (LOS: los-01-06-c)
   - A. stayed, because 5 of the 9 trees, or 56%, vote stayed.
   - B. left, because the average proportion left across the 9 trees is 64%.
   - C. left, because Tree 1 assigns a proportion left of 91%.
4. The most appropriate approach to the tiering project is: (LOS: los-01-06-d)
   - A. principal components analysis retaining five components, each of which defines one service tier.
   - B. k-means with k = 5 on the chosen features and distance measure, rerun from several different sets of initial centroids and the resulting solutions compared.
   - C. agglomerative hierarchical clustering, because the dependence of k-means results on the initial centroids makes k-means unsuitable.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The type of the target variable decides the problem class (V1 p.200).
>    Workstream 2 is trained on recorded net new assets, a continuous amount in Swiss francs, so it is supervised regression; mapping forecasts into three bands after training does not change a continuous target into a categorical one.
>    Workstream 3 is trained on transcripts that already carry one of 12 category labels, so it is supervised classification (V1 p.199, p.200).
>    A network with six hidden layers meets the deep-learning definition of at least 2 hidden layers, and natural language processing is a standard deep-learning task (V1 p.201, p.252).
>    A is wrong because it classifies Workstream 2 by the bands relationship managers use afterward rather than by the continuous target the model learns.
>    C is wrong because the 12 categories are known labels used in training; clustering applies only when no target exists and the algorithm discovers the groups itself (V1 p.201).
> 2. **C.** Out-of-sample error is the sum of bias error, variance error and base error (V1 p.205).
>    Totals by depth: 2: $12.1 + 0.9 + 3.0 = 16.0\%$; 4: $8.4 + 2.0 + 3.0 = 13.4\%$; 6: $5.6 + 3.6 + 3.0 = 12.2\%$; 8: $3.7 + 6.1 + 3.0 = 12.8\%$; 10: $2.2 + 9.4 + 3.0 = 14.6\%$.
>    Total error is U-shaped in complexity and is lowest at depth 6, just before rising variance error outweighs falling bias error (V1 p.206).
>    The terminal-node column is a decoy; complexity is already captured by depth.
>    A is wrong because it omits the base error: $5.6 + 3.6 = 9.2\%$ picks the right depth, since base error is the same at every depth, but understates the error rate by 3.0 points.
>    B is wrong because it omits the variance error, so the error falls with every extra level ($2.2 + 3.0 = 5.2\%$ at depth 10); that is judging the tree by its fit to the training data, which selects the most overfitted tree.
> 3. **A.** Each tree predicts the majority class at its terminal node, so a tree votes "left" when the proportion left exceeds 0.50.
>    Trees 1, 3, 5 and 8 vote left (0.91, 0.84, 0.88, 0.93); Trees 2, 4, 6, 7 and 9 vote stayed (0.46, 0.43, 0.47, 0.41, 0.44).
>    A random forest used for classification aggregates the trees by majority vote (V1 p.219): stayed wins 5 to 4, a share of $5 / 9 = 0.5556$, or 56%.
>    B is wrong because it averages the tree outputs, $5.77 / 9 = 0.6411$, which is the aggregation rule for regression, not classification; averaging lets four very confident trees outweigh the five-tree majority.
>    C is wrong because it reports one tree; the forest's value comes from combining many trees so their noise averages out, which is why it generalizes better than any single tree (V1 p.218, p.220).
> 4. **B.** The number of tiers is fixed in advance at five, which is the condition under which k-means is the appropriate clustering algorithm (V1 p.237, p.264).
>    The analyst must still specify the features that define similarity and the distance measure, as for any clustering algorithm (V1 p.236, p.243).
>    K-means results can depend on the initial centroids, so the standard remedy is to rerun it from several different starting points and compare the solutions on cohesion and separation, not to abandon it (V1 p.237, p.238).
>    PCA may be used first to reduce the highly correlated features to a few uncorrelated composites, but the grouping itself is still done by the clustering step (V1 p.232, p.235).
>    A is wrong because principal components are composite features, not groups of clients; PCA is dimension reduction, not clustering, which is the flaw in Brandvold's statement.
>    C is wrong because sensitivity to initial centroids is a known and manageable limitation; hierarchical clustering is preferred when the number of groups is unknown, which is not the case here, and it would not use the committee's prior choice of five tiers as an input (V1 p.243).

## Distractor design

- Q1: A labels a continuous target as categorical because its forecasts are bucketed after training; C treats known training labels as clusters.
- Q2: A omits the base error from the out-of-sample error decomposition; B omits the variance error and so selects on in-sample fit.
- Q3: B applies the regression aggregation rule (averaging) to a classification forest; C reports a single tree instead of the ensemble.
- Q4: A confuses dimension reduction with clustering; C treats the initial-centroid limitation as disqualifying and ignores that the number of groups is known.
