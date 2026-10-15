---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 6
title: "Kestrel Point Neural Factor Model"
los: [los-01-06-a, los-01-06-b]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Kestrel Point Neural Factor Model

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Kestrel Point Capital is a quantitative equity hedge fund that ranks stocks by forecast return.
Mei Tanaka, head of research, is replacing the fund's linear fundamental factor model with a neural network.
The dataset covers 350 stocks over 96 monthly periods, from January 2018 to December 2025.
For each stock and month, the features are 9 factor loadings, and the target is the stock's return in the following month.
The fund rebalances monthly into the 25 stocks with the highest forecast returns.
The investment committee will approve the new model only if its forecasts improve on the linear model out of sample, after trading costs, so Tanaka must document every tuning decision.
Before training, each input is scaled to lie between 0 and 1.

The production network has 9 input nodes, three hidden layers of 40 nodes each using the rectified linear unit (ReLU) activation function, and 1 output node.
A LASSO (L1) penalty is applied to the network weights during training, and the learning rate is 0.05.

To explain the mechanics to the portfolio managers, Tanaka presents a stripped-down version with three scaled inputs, two hidden ReLU nodes, one linear output node, and no bias terms.

Exhibit 1: Illustrative network for one stock

| Item | Input 1 | Input 2 | Input 3 | Weight to output |
|---|---|---|---|---|
| Scaled input value | 0.60 | 0.25 | 0.80 | |
| Weights into hidden node H1 | 0.50 | -1.10 | 0.30 | 0.080 |
| Weights into hidden node H2 | -0.40 | 0.90 | -0.70 | 0.050 |

She also shows one training step for a single link weight, using the production learning rate.
The weight currently equals 0.40, and the partial derivative of total error with respect to that weight is 1.8.

Tanaka then tests four values of the L1 hyperparameter, holding the architecture fixed, with the results in Exhibit 2.

Exhibit 2: Mean squared error by L1 hyperparameter

| L1 hyperparameter | In-sample MSE | Out-of-sample MSE |
|---|---|---|
| 0.01 | 0.0038 | 0.0141 |
| 0.03 | 0.0043 | 0.0112 |
| 0.06 | 0.0049 | 0.0097 |
| 0.10 | 0.0058 | 0.0101 |

On 9 June 2026, Oluwaseun Adeyemi, a portfolio manager, reviews the work.

Adeyemi: "To tune the L1 hyperparameter properly, we should shuffle the 96 months at random into 8 folds, train on 7 folds, validate on the eighth, and average the 8 validation errors."

Tanaka: "Our current procedure trains on each month and tests on the following month, then rolls forward one month at a time, and I would keep it."

Adeyemi also proposes a second project.
He wants an algorithm that decides how to slice large orders during the trading day.
It would receive no labeled examples of good execution; instead, it would try different slicing actions in a simulated market, observe the resulting implementation shortfall, and learn over millions of trials to maximize a reward equal to the negative of that shortfall.

## Questions

1. Tanaka's production return model is best described as: (LOS: los-01-06-a)
   - A. supervised learning with a deep neural network.
   - B. unsupervised learning, because the hidden layers learn their own transformed features.
   - C. supervised learning with a neural network that is not deep, because a deep network requires more than 20 hidden layers.
2. Based on Exhibit 1, the illustrative network's predicted return is closest to: (LOS: los-01-06-a)
   - A. 2.12%.
   - B. -0.76%.
   - C. 1.33%.
3. After the training step Tanaka shows, the new value of the link weight is closest to: (LOS: los-01-06-a)
   - A. 0.31.
   - B. 0.49.
   - C. -1.40.
4. Based on Exhibit 2, the L1 hyperparameter Tanaka should select is: (LOS: los-01-06-b)
   - A. 0.01.
   - B. 0.06.
   - C. 0.10.
5. Regarding the tuning procedure, the better approach is: (LOS: los-01-06-b)
   - A. Adeyemi's, because averaging 8 validation errors uses every month for both training and validation.
   - B. Adeyemi's, provided the number of folds is increased to 10.
   - C. Tanaka's, because k-fold cross-validation cannot be used with time-series data.
6. Adeyemi's order-slicing project is best described as: (LOS: los-01-06-a)
   - A. supervised learning, because the implementation shortfall of each trial serves as a label.
   - B. reinforcement learning.
   - C. unsupervised clustering of order-slicing actions.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The target, next-month return, is observed for every stock and month, so the data are labeled and the task is supervised (regression, because the target is continuous).
>    A deep neural network has many hidden layers, at least 2 and potentially more than 20; the production network has three, so it qualifies.
>    B is wrong because learning transformed features in hidden layers does not remove the labeled target; the weights are fitted by comparing predictions to actual returns.
>    C is wrong because it quotes the "more than 20" figure as a minimum, when the threshold is at least 2 hidden layers.
> 2. **A.** Total net input to H1 $= 0.60(0.50) + 0.25(-1.10) + 0.80(0.30) = 0.3000 - 0.2750 + 0.2400 = 0.2650$, and ReLU gives $z_1 = \max(0, 0.2650) = 0.2650$.
>    Total net input to H2 $= 0.60(-0.40) + 0.25(0.90) + 0.80(-0.70) = -0.2400 + 0.2250 - 0.5600 = -0.5750$, and ReLU gives $z_2 = \max(0, -0.5750) = 0$.
>    Output $= 0.080(0.2650) + 0.050(0) = 0.0212$, or 2.12%.
>    B is wrong because it passes H2's negative net input through without the activation function: $0.0212 + 0.050(-0.5750) = 0.0212 - 0.02875 = -0.00755$, or -0.76%.
>    C is wrong because it attaches the output weights to the wrong hidden nodes: $0.050(0.2650) + 0.080(0) = 0.01325$, or 1.33%.
> 3. **A.** $w_{new} = w_{old} - \eta \, \partial E / \partial w = 0.40 - 0.05(1.8) = 0.40 - 0.09 = 0.31$.
>    B is wrong because it adds the adjustment ($0.40 + 0.09 = 0.49$), moving the weight up the error gradient instead of down it.
>    C is wrong because it omits the learning rate ($0.40 - 1.8 = -1.40$).
> 4. **B.** The goal is the lowest out-of-sample error, and out-of-sample MSE falls from 0.0141 to 0.0112 to 0.0097 and then rises to 0.0101, so 0.06 is optimal.
>    Moving from 0.01 to 0.06 raises in-sample MSE (more bias) and lowers out-of-sample MSE (less variance) until total out-of-sample error turns up.
>    The in-sample to out-of-sample gaps are 0.0103, 0.0069, 0.0048 and 0.0043.
>    A is wrong because it selects the lowest in-sample MSE, 0.0038, which rewards the least regularized and most overfitted model.
>    C is wrong because it minimizes the gap (0.0043) rather than out-of-sample error; the smaller gap at 0.10 comes from a worse in-sample fit, while out-of-sample MSE has already risen to 0.0101.
> 5. **C.** K-fold cross-validation shuffles observations at random, which is invalid for time-series data because only the most recent data can reasonably validate a model.
>    Tanaka's procedure is walk-forward validation, where each month's test set becomes the next month's training set.
>    A is wrong because using every month for both roles is the benefit of k-fold for cross-sectional data, but shuffling months lets the model train on the future and validate on the past.
>    B is wrong because changing k does not fix the ordering problem.
> 6. **B.** An agent takes actions in an environment to maximize a reward over time, with no labeled data and no instantaneous feedback, and learns through millions of trials; that is reinforcement learning.
>    A is wrong because the shortfall is a reward observed after the agent chooses its action, not a labeled example of the correct action for given inputs.
>    C is wrong because nothing is being grouped; the algorithm is choosing sequential actions to maximize reward.

## Distractor design

- Q1: B treats hidden-layer feature learning as the absence of a target; C quotes "more than 20" hidden layers as the deep-learning minimum.
- Q2: B skips the activation function on a negative net input; C misreads the exhibit by swapping the output weights.
- Q3: B reverses the sign of the gradient step; C omits the learning rate.
- Q4: A selects on in-sample fit; C minimizes the in-sample to out-of-sample gap instead of out-of-sample error.
- Q5: A applies the cross-sectional benefit of k-fold to time-series data; B changes k, which does not address the ordering problem.
- Q6: A treats a reward as a label; C treats sequential decision-making as clustering.
