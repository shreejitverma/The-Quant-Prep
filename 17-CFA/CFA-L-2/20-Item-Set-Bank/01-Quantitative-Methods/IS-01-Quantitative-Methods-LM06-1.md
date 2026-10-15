---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 6
title: "Harbourline Bank SME Credit Models"
los: [los-01-06-a, los-01-06-b, los-01-06-c]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Harbourline Bank SME Credit Models

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Harbourline Bank is a regional lender with a growing book of small and medium-sized enterprise (SME) loans.
Priya Raman, head of credit analytics, is rebuilding two of the bank's credit models.
The first model predicts whether a borrower will default within 12 months of origination.
Its dataset contains 2,400 historical borrowers, each described by 30 features standardized to mean 0 and variance 1, and each carrying a recorded outcome of 1 (defaulted) or 0 (did not default).
The bank also assigns every borrower an internal risk grade from 1 (strongest) to 7 (weakest), but Raman does not use the grade in either model.
The second model predicts loss given default (LGD), measured as the percentage of exposure lost, for borrowers that have defaulted.
The credit policy team later maps each predicted LGD into one of four recovery bands for pricing.

Before fitting any model, Raman sets aside 15% of the 2,400 borrowers as a test sample.
She intends to report test-sample results to the credit committee only after every modeling choice is final.
Her first two default models produce the results in Exhibit 1.

Exhibit 1: Default model results

| Model | Features used | Training error rate | Validation error rate |
|---|---|---|---|
| Logistic regression | 30 | 11.8% | 12.4% |
| CART, no depth limit and no pruning | 30 | 0.6% | 17.9% |

On 3 March 2026, Daniel Okoro, the bank's chief risk officer, reviews Exhibit 1 and asks for 8-fold cross-validation on the borrowers that remain after the test sample is removed.
Raman runs it on a revised default model and records the validation error of each fold in Exhibit 2.

Exhibit 2: 8-fold cross-validation error rates for the revised default model

| Fold | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Validation error (%) | 10.4 | 11.2 | 9.8 | 10.9 | 11.6 | 10.1 | 10.7 | 11.3 |

For the LGD model, Raman fits LASSO with a penalty hyperparameter of $\lambda = 0.8$ on the training data.
Two candidate fits are summarized in Exhibit 3.

Exhibit 3: Candidate LASSO fits for the LGD model (training data, standardized features)

| Candidate | Non-zero coefficients | Sum of squared residuals | Sum of absolute coefficients |
|---|---|---|---|
| P | 12 | 318.40 | 6.90 |
| Q | 7 | 320.10 | 3.20 |

On 10 March 2026, Okoro asks for a quick check of a new applicant, Tidewater Joinery, using k-nearest neighbor with Euclidean distance on two standardized features, interest coverage and leverage.
Tidewater's feature values are 0.20 and -0.40, respectively.
Raman selects the six labeled borrowers in Exhibit 4 as the reference set and notes that she would prefer k = 4 to Okoro's k = 3 "so that more neighbours vote."

Exhibit 4: Reference borrowers (standardized features)

| Borrower | Interest coverage | Leverage | Outcome |
|---|---|---|---|
| B1 | 0.50 | -0.10 | Default |
| B2 | -0.30 | -0.60 | No default |
| B3 | 0.10 | 0.30 | No default |
| B4 | 0.60 | -0.80 | Default |
| B5 | -0.10 | -0.90 | No default |
| B6 | 1.10 | 0.20 | Default |

Okoro closes the review with a requirement: "The credit committee must see the specific reason each applicant is declined, and our features clearly interact in non-linear ways, so the final default model must satisfy both conditions."

## Questions

1. The default model and the LGD model are best described, respectively, as: (LOS: los-01-06-a)
   - A. regression and regression.
   - B. classification and regression.
   - C. classification and classification.
2. The CART model in Exhibit 1 is most likely: (LOS: los-01-06-b)
   - A. underfitted, with high bias error, which adding more borrowers to the training sample would correct.
   - B. overfitted, with high variance error, which limiting tree depth or pruning would address.
   - C. overfitted, with high bias error, which a penalty that decreases with the number of features would address.
3. Based on Exhibit 2, the estimate of out-of-sample error and the number of borrowers in each validation fold are closest to: (LOS: los-01-06-b)
   - A. 10.75% and 255 borrowers.
   - B. 10.75% and 300 borrowers.
   - C. 12.29% and 255 borrowers.
4. Based on Exhibit 3, which candidate does LASSO prefer, and what is the value of its objective function? (LOS: los-01-06-c)
   - A. Candidate P, 318.40.
   - B. Candidate P, 312.88.
   - C. Candidate Q, 322.66.
5. Using Exhibit 4, Tidewater Joinery's classification under Okoro's k = 3 and under Raman's k = 4 is, respectively: (LOS: los-01-06-c)
   - A. default under k = 3; no clear classification under k = 4.
   - B. no default under k = 3; no clear classification under k = 4.
   - C. default under k = 3; default under k = 4.
6. Given Okoro's closing requirement, the most appropriate final default model is: (LOS: los-01-06-c)
   - A. a random forest of several hundred bagged trees.
   - B. a CART regularized by maximum depth and minimum node population.
   - C. a soft-margin support vector machine.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The type of the target variable decides the problem class.
>    The default target is 1 or 0, a categorical variable, so the default model is a classifier.
>    LGD is a continuous percentage, so the LGD model is regression even though its output is later mapped into recovery bands.
>    A is wrong because it labels the default model by its probability output rather than by its categorical target.
>    C is wrong because bucketing predictions after training does not change a continuous target into a categorical one.
> 2. **B.** A training error of 0.6% against a validation error of 17.9% is the signature of overfitting, which is high variance error.
>    An unconstrained CART memorizes the training data and is regularized by maximum depth, minimum node population, maximum number of decision nodes, or pruning.
>    A is wrong because underfitting shows poor in-sample fit as well, and on the learning curve more data does not lift a high-bias model to the desired accuracy.
>    C is wrong on two counts: overfitting is variance error, not bias error, and the penalty must increase with the number of features.
> 3. **A.** In-sample borrowers $= 2{,}400 \times (1 - 0.15) = 2{,}040$, so each fold holds $2{,}040 / 8 = 255$ borrowers, and each borrower is used in training 7 times and in validation once.
>    The estimate of out-of-sample error is the mean validation error, $\hat{E}_{out} = (10.4 + 11.2 + 9.8 + 10.9 + 11.6 + 10.1 + 10.7 + 11.3) / 8 = 86.0 / 8 = 10.75\%$.
>    B is wrong because $2{,}400 / 8 = 300$ folds the test sample into the cross-validation, but the test sample must be excluded first.
>    C is wrong because $86.0 / 7 = 12.29\%$ divides by $k - 1$ instead of $k$.
> 4. **C.** The LASSO objective is $SSR + \lambda \sum |\hat{b}_k|$.
>    Candidate P: $318.40 + 0.8 \times 6.90 = 318.40 + 5.52 = 323.92$.
>    Candidate Q: $320.10 + 0.8 \times 3.20 = 320.10 + 2.56 = 322.66$.
>    Q has the lower objective, so the 5 extra features in P do not reduce squared residuals by enough ($1.70$) to cover their penalty cost ($5.52 - 2.56 = 2.96$).
>    A is wrong because it compares raw sums of squared residuals, which is OLS ($\lambda = 0$) and ignores the penalty.
>    B is wrong because it subtracts the penalty ($318.40 - 5.52 = 312.88$ against $320.10 - 2.56 = 317.54$), reversing the sign of the penalty term.
> 5. **A.** Euclidean distances from (0.20, -0.40): B1 $= \sqrt{0.30^2 + 0.30^2} = 0.4243$, B2 $= \sqrt{0.50^2 + 0.20^2} = 0.5385$, B4 $= \sqrt{0.40^2 + 0.40^2} = 0.5657$, B5 $= \sqrt{0.30^2 + 0.50^2} = 0.5831$, B3 $= \sqrt{0.10^2 + 0.70^2} = 0.7071$, B6 $= \sqrt{0.90^2 + 0.60^2} = 1.0817$.
>    With k = 3 the neighbours are B1 (default), B2 (no default) and B4 (default), so the majority vote is default.
>    With k = 4, B5 (no default) joins, giving a 2 to 2 tie and no clear classification, which is why an even k is avoided.
>    B is wrong because it ranks neighbours on interest coverage alone (nearest B3, then B1 and B5 at 0.30), dropping the leverage feature and producing a no-default majority.
>    C is wrong because it breaks the 2 to 2 tie in favour of the single closest neighbour, which is k = 1 in disguise, not the k = 4 majority rule.
> 6. **B.** Only CART handles non-linear interactions among features and also gives a visual explanation of every prediction through the feature and cutoff at each node.
>    Regularizing it by maximum depth and minimum node population also addresses the overfitting seen in Exhibit 1.
>    A is wrong because a random forest reduces variance but is relatively black box, so it fails the committee's explanation requirement.
>    C is wrong because an SVM is a linear classifier that offers no node-by-node explanation, and a non-linear SVM would add overfitting risk.

## Distractor design

- Q1: A judges the problem by the model's output (a probability) rather than the target; C treats post-training bucketing of a continuous target as a categorical target.
- Q2: A confuses overfitting with underfitting (bias vs variance); C pairs overfitting with bias and reverses the sign of the complexity penalty.
- Q3: B forgets to exclude the test sample before forming folds; C divides the sum of fold errors by $k - 1$.
- Q4: A drops the penalty (OLS, $\lambda = 0$); B subtracts the penalty instead of adding it.
- Q5: B misreads the exhibit by using one feature instead of both in the distance; C resolves an even-k tie by the nearest neighbour.
- Q6: A ignores the interpretability constraint; C ignores the non-linearity constraint and the explanation requirement.
