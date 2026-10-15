---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 6
title: "Aldercrest Endowment Manager Overlap"
los: [los-01-06-a, los-01-06-d]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Aldercrest Endowment Manager Overlap

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

The Aldercrest University Endowment allocates its public equity sleeve to 31 external managers.
Marcus Hale, the chief investment officer, suspects that managers hired for different styles are taking similar exposures, which would leave the endowment less diversified than its manager roster suggests.
He asks Sofia Lindqvist, a senior risk analyst, to use machine learning to test that suspicion.
The investment committee has said that it will consider consolidating the roster only if the analysis shows material overlap, so the results must be presented in a form the trustees can follow.
Every manager in the endowment's database carries a self-reported style label, but Lindqvist decides not to use the labels because they are the claims being tested.

Task 1: Lindqvist measures each manager's holdings on eight standardized risk features: value, size, momentum, quality, market beta, US dollar sensitivity, emerging-market revenue share, and liquidity.
Several of the features are highly correlated.
She extracts the eigenvalues of the covariance matrix of the eight features, shown in Exhibit 1, and the investment committee's policy is to retain the fewest components that explain at least 85% of total variance.

Exhibit 1: Eigenvalues of the feature covariance matrix

| Component | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Eigenvalue | 3.12 | 1.96 | 1.04 | 0.72 | 0.48 | 0.33 | 0.21 | 0.14 |

Task 2: As a pilot, Lindqvist runs k-means with k = 2 and Euclidean distance on six managers described by two standardized features, value tilt and size tilt.
The pilot is intended only to confirm that the software behaves as expected before the full roster is processed.
The initial centroids are C1 = (0.80, 0.80) and C2 = (-0.40, -0.40).

Exhibit 2: Pilot managers (standardized features)

| Manager | Value tilt | Size tilt |
|---|---|---|
| M1 | 0.90 | 0.40 |
| M2 | 0.60 | 1.10 |
| M3 | 0.10 | 0.20 |
| M4 | -0.70 | -0.30 |
| M5 | -0.20 | -0.90 |
| M6 | 0.30 | -0.40 |

Task 3: For the five emerging-market managers, labeled A to E, Lindqvist runs agglomerative hierarchical clustering with average linkage, using the pairwise distances in Exhibit 3.
Each distance is the Euclidean distance between two managers' standardized feature vectors.

Exhibit 3: Pairwise distances between emerging-market managers

| | A | B | C | D | E |
|---|---|---|---|---|---|
| A | 0 | 0.18 | 0.30 | 0.44 | 0.52 |
| B | 0.18 | 0 | 0.26 | 0.40 | 0.49 |
| C | 0.30 | 0.26 | 0 | 0.27 | 0.41 |
| D | 0.44 | 0.40 | 0.27 | 0 | 0.35 |
| E | 0.52 | 0.49 | 0.41 | 0.35 | 0 |

At a meeting on 14 April 2026, the two discuss the work.

Hale: "Once the principal components are computed, each component is effectively a group of managers, so we can report our exposure to each group directly from Task 1."

Lindqvist: "Before any clustering algorithm runs, the only choices I need to make are the distance measure and, for k-means only, the value of k."

Hale: "For the full roster of 31 managers, we have no idea how many genuinely distinct groups exist, and the committee wants to see the groupings at several levels of detail.
K-means is the faster algorithm, so run k-means on the full roster."

## Questions

1. Based on Exhibit 1 and the committee's policy, the number of principal components Lindqvist should retain, and the cumulative share of variance they explain, is: (LOS: los-01-06-d)
   - A. 3 components, explaining 76.5%.
   - B. 4 components, explaining 85.5%.
   - C. 6 components, explaining 95.6%.
2. Task 1 and Task 2 are best described, respectively, as: (LOS: los-01-06-a)
   - A. unsupervised dimension reduction and unsupervised clustering.
   - B. unsupervised dimension reduction and supervised classification.
   - C. unsupervised clustering and unsupervised clustering.
3. After the first assignment step of the Task 2 pilot, the updated centroid C2 is closest to: (LOS: los-01-06-d)
   - A. (-0.125, -0.350).
   - B. (-0.200, -0.533).
   - C. (-0.180, -0.360).
4. In Task 3, the second merge and the resulting three-cluster solution are: (LOS: los-01-06-d)
   - A. C joins {A, B} at a distance of 0.26, giving {A, B, C}, {D} and {E}.
   - B. C joins {A, B} at a distance of 0.28, giving {A, B, C}, {D} and {E}.
   - C. C and D merge at a distance of 0.27, giving {A, B}, {C, D} and {E}.
5. Lindqvist's statement about what must be specified before clustering is: (LOS: los-01-06-d)
   - A. correct.
   - B. incorrect, because the feature set that defines similarity must also be specified.
   - C. incorrect, because hierarchical clustering also requires a value of k.
6. The best response to Hale's final recommendation is that, for the full roster, Lindqvist should use: (LOS: los-01-06-d)
   - A. k-means, because its speed matters most when the number of groups is unknown.
   - B. hierarchical clustering, because it needs no number of clusters in advance and its dendrogram shows every level of grouping.
   - C. principal components analysis, because it is the unsupervised method that groups observations.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** With eight standardized features the eigenvalues sum to $8.00$, and each share is $\lambda_j / 8.00$.
>    Shares are 0.3900, 0.2450, 0.1300, 0.0900, 0.0600, 0.0413, 0.0263, 0.0175.
>    Cumulative shares are 39.0%, 63.5%, 76.5%, 85.5%, so four components are the fewest that reach 85%.
>    A is wrong because it keeps only the components with eigenvalues above 1 (the average eigenvalue), a rule of thumb that ignores the committee's 85% cumulative-share policy.
>    C is wrong because six components ($7.65 / 8.00 = 95.6\%$) apply the 95% top of the usual 85% to 95% range rather than the committee's stated 85%.
> 2. **A.** Neither task uses a target: Task 1 reduces eight correlated features to a few uncorrelated composites (dimension reduction), and Task 2 sorts unlabeled observations into groups (clustering).
>    B is wrong because the style labels were deliberately excluded, so no labeled target exists and the pilot is not classification.
>    C is wrong because PCA transforms features; it does not group observations.
> 3. **A.** Distances to C1 and C2: M1 0.4123 vs 1.5264, M2 0.3606 vs 1.8028, M3 0.9220 vs 0.7810, M4 1.8601 vs 0.3162, M5 1.9723 vs 0.5385, M6 1.3000 vs 0.7000.
>    M1 and M2 go to C1; M3, M4, M5 and M6 go to C2.
>    New C2 $= \left(\frac{0.10 - 0.70 - 0.20 + 0.30}{4}, \frac{0.20 - 0.30 - 0.90 - 0.40}{4}\right) = (-0.125, -0.350)$.
>    B is wrong because it assigns M3 to C1 on the basis that both of its features are positive, rather than by distance, and averages only M4, M5 and M6 to get $(-0.200, -0.533)$.
>    C is wrong because it includes the old centroid as a fifth member, $\left(\frac{-0.50 - 0.40}{5}, \frac{-1.40 - 0.40}{5}\right) = (-0.180, -0.360)$, although the centroid is the average of the members only.
> 4. **C.** The first merge is A with B at 0.18, the smallest distance.
>    Average linkage then gives $d(C, AB) = (0.30 + 0.26)/2 = 0.28$, $d(D, AB) = (0.44 + 0.40)/2 = 0.42$, $d(E, AB) = (0.52 + 0.49)/2 = 0.505$.
>    The smallest remaining distance is $d(C, D) = 0.27 < 0.28$, so C and D merge second, leaving {A, B}, {C, D} and {E}.
>    For completeness, the third merge is {A, B} with {C, D} at $(0.30 + 0.44 + 0.26 + 0.40)/4 = 0.35$, below $d(CD, E) = (0.41 + 0.35)/2 = 0.38$.
>    A is wrong because it uses the minimum pairwise distance (single linkage, $\min(0.30, 0.26) = 0.26$), which the vignette does not specify.
>    B is wrong because it computes the average linkage of 0.28 correctly but fails to compare it with the pairwise distance $d(C, D) = 0.27$.
> 5. **B.** Any clustering algorithm requires the analyst to specify the features that define similarity and the distance measure; k-means additionally requires k.
>    A is wrong because it omits the feature set.
>    C is wrong because hierarchical clustering does not require k; that is precisely its advantage over k-means.
> 6. **B.** When the number of groups is unknown, hierarchical clustering sorts observations without that prior input, and a horizontal cut of the dendrogram at different heights delivers groupings at any granularity, which is what the committee asked for.
>    A is wrong because k-means being faster is true but irrelevant; k-means still needs k before it runs, and speed does not solve the unknown-k problem.
>    C is wrong because PCA reduces features, it does not group managers, which is also the flaw in Hale's first statement.

## Distractor design

- Q1: A applies an eigenvalue-above-average cutoff instead of the stated cumulative-share rule; C uses the wrong retention target (95% instead of 85%).
- Q2: B treats unused style labels as a target; C confuses dimension reduction with clustering.
- Q3: B assigns an observation by quadrant rather than by distance; C averages the old centroid with the members.
- Q4: A uses the wrong linkage (single instead of average); B stops after computing the cluster distance without comparing it with all remaining pairs.
- Q5: A omits the feature set that defines similarity; C attributes the k-means input k to hierarchical clustering.
- Q6: A offers a true fact as a wrong reason; C confuses PCA with clustering.
