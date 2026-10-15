---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 6
title: "Norrland Mutual Claims Fraud Screen"
los: [los-01-06-b, los-01-06-c]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Norrland Mutual Claims Fraud Screen

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Norrland Mutual is a property and casualty insurer that must demonstrate to its regulator that its claims fraud controls are effective.
Henrik Dahl, a data scientist in the special investigations unit, is building a screen that flags motor claims for referral to investigators.
He has 12,000 historical claims, each labeled as fraudulent or legitimate after investigation, and 11 features per claim.
The features include the claim amount relative to the policy limit, the age of the policy, the claimant's prior claim history, and whether the repair shop belongs to Norrland's approved network.
Fewer than 7% of the historical claims were confirmed as fraudulent, so the classes are heavily imbalanced.
Investigators can review only about 150 referrals per week, so the unit cannot simply refer every unusual claim.
Dahl splits the claims at random into a training sample (70%), a validation sample (20%) and a test sample (10%).

Dahl first grows a classification and regression tree (CART) on the training sample.
Exhibit 1 shows the tree, where "value" lists the number of training claims at each node as [fraudulent, legitimate].

Exhibit 1: CART fitted on the training sample

| Node | Split rule | If true | If false | Value [fraudulent, legitimate] | Samples |
|---|---|---|---|---|---|
| 1 | Claim-to-policy-limit ratio <= 0.62 | Node 2 | Node 3 | [560, 7,840] | 8,400 |
| 2 | Days since policy inception <= 45 | Node 4 | Node 5 | [310, 5,120] | 5,430 |
| 3 | Terminal | | | [250, 2,720] | 2,970 |
| 4 | Prior claims in last 24 months <= 1 | Node 8 | Node 9 | [52, 118] | 170 |
| 5 | Terminal | | | [258, 5,002] | 5,260 |
| 8 | Terminal | | | [14, 92] | 106 |
| 9 | Terminal | | | [38, 26] | 64 |

A new claim arrives with a claim-to-policy-limit ratio of 0.48, a policy that is 30 days old, three prior claims in the last 24 months, and a repair shop outside Norrland's approved network.

Dahl next fits a random forest and evaluates it once on the test sample.
He treats a claim as referred whenever the forest's majority vote is fraudulent.
Exhibit 2 reports the results.

Exhibit 2: Random forest results on the test sample

| | Predicted fraudulent | Predicted legitimate |
|---|---|---|
| Actually fraudulent | 84 | 16 |
| Actually legitimate | 21 | 1,079 |

On 22 May 2026, Amara Nwosu, the chief compliance officer, sets out the regulator's expectations.

Nwosu: "The regulator wants us to report the share of actually fraudulent claims that our screen catches, because a missed fraud is the costly error.
In addition, every claim we refer to investigators must come with a documented reason that can be shown to the policyholder."

Dahl responds the same day.

Dahl: "Replacing the single tree with a random forest of 300 trees, each considering 4 of the 11 features at every split, will reduce overfitting and still give us a tree diagram explaining each referral.
Before that, I will choose the maximum depth of the single tree so that we have a fair benchmark."

Nwosu asks Dahl to confirm which sample he will use for that depth choice before any results are reported.

## Questions

1. Using Exhibit 1, the new claim's predicted class and the probability of that class are closest to: (LOS: los-01-06-c)
   - A. fraudulent, 0.59.
   - B. legitimate, 0.87.
   - C. legitimate, 0.59.
2. The metric Nwosu should report to the regulator, and its value from Exhibit 2, is closest to: (LOS: los-01-06-c)
   - A. recall of 0.80.
   - B. recall of 0.84.
   - C. accuracy of 0.97.
3. Dahl's statement about the random forest is: (LOS: los-01-06-c)
   - A. correct.
   - B. incorrect, because a random forest reduces overfitting but is relatively black box and gives no single tree diagram to explain a referral.
   - C. incorrect, because averaging many trees increases variance error relative to a single tree.
4. To choose the maximum depth of the single tree, Dahl should use: (LOS: los-01-06-b)
   - A. the validation sample of 2,400 claims.
   - B. the test sample of 1,200 claims.
   - C. the training sample of 8,400 claims.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** At node 1, $0.48 \le 0.62$ is true, so go to node 2.
>    At node 2, $30 \le 45$ is true, so go to node 4.
>    At node 4, $3 \le 1$ is false, so go to terminal node 9 with value [38, 26].
>    The predicted class is the majority class, fraudulent, with $P(\text{fraudulent}) = 38 / 64 = 0.5938$.
>    The repair shop feature never enters the tree and is a decoy.
>    B is wrong because it follows the true branch at node 4 and lands in node 8, giving legitimate with $92 / 106 = 0.8679$.
>    C is wrong because it reads the value array as [legitimate, fraudulent], so the majority of 38 is mislabeled as legitimate.
> 2. **B.** The share of actual frauds that the screen catches is recall, $TP / (TP + FN) = 84 / (84 + 16) = 84 / 100 = 0.84$.
>    A is wrong because $84 / (84 + 21) = 84 / 105 = 0.80$ is precision, the share of flagged claims that are actually fraudulent, not the share of actual frauds caught.
>    C is wrong because accuracy, $(84 + 1{,}079) / 1{,}200 = 1{,}163 / 1{,}200 = 0.9692$, is inflated by the large majority of legitimate claims and does not measure missed frauds (Type II errors).
> 3. **B.** A random forest trains many trees on bagged samples, with a random subset of features at each split, so it reduces variance and protects against overfitting.
>    The price is that it loses the interpretability of a single tree, so it cannot supply the documented reason Nwosu requires.
>    A is wrong because the second half of Dahl's statement is false.
>    C is wrong because averaging the predictions of many diverse trees reduces variance; it does not increase it.
> 4. **A.** Hyperparameters such as maximum depth are tuned on the validation sample, which holds $0.20 \times 12{,}000 = 2{,}400$ claims.
>    The training sample is $0.70 \times 12{,}000 = 8{,}400$ claims and the test sample is $0.10 \times 12{,}000 = 1{,}200$ claims, consistent with the 1,200 claims in Exhibit 2.
>    B is wrong because the test sample must be kept out of every modeling choice so that it gives an honest out-of-sample estimate; tuning on it contaminates the reported results.
>    C is wrong because tuning on the training sample always favours the deepest tree, which has the lowest in-sample error and the worst overfitting.

## Distractor design

- Q1: B takes the wrong branch on a false split test; C misreads the order of the value array.
- Q2: A swaps precision for recall (uses FP instead of FN in the denominator); C uses accuracy under class imbalance.
- Q3: A accepts the interpretability claim; C reverses the variance effect of ensembling.
- Q4: B tunes on the out-of-sample test set; C tunes on in-sample training fit.
