---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 7
title: "Marlowe and Finch Trade Surveillance Classifier"
los: [los-01-07-f, los-01-07-c]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Marlowe and Finch Trade Surveillance Classifier

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Marlowe and Finch Securities is a US broker-dealer whose surveillance system generates alerts on trades that precede material announcements.
Chief compliance officer Evelyn Castellanos has asked data scientist Oluwaseun Adebayo to replace manual triage with a supervised classifier that labels each alert 1 (likely violation, escalate) or 0 (no violation, close).

Adebayo assembles 48,000 historical alerts, of which 2,400 were confirmed as violations after investigation.
A further 6,500 recent alerts are still under review and have no outcome.
The average manual review takes 42 minutes per alert.
He splits the labelled alerts 60:20:20 into training, cross-validation, and test sets by stratified random sampling, so each set keeps the 5% violation rate.
He fits a LASSO-penalized logistic regression, which outputs a probability that an alert is a violation.

Castellanos explains her priorities on 2 June: "A missed violation exposes us to regulatory fines and sanctions far larger than the cost of an unnecessary investigation.
I want the model to catch as many true violations as possible, even at the price of more false alerts."

Exhibit 1 shows the cross-validation confusion matrices at three probability thresholds.

**Exhibit 1: Cross-validation confusion matrices (9,600 alerts)**

| Threshold p | TP | FN | FP | TN |
|---|---|---|---|---|
| 0.30 | 408 | 72 | 690 | 8,430 |
| 0.50 | 312 | 168 | 240 | 8,880 |
| 0.70 | 216 | 264 | 60 | 9,060 |

A junior analyst, Priya Nandakumar, notes that the 0.70 threshold produces the highest accuracy of the three and recommends it.
Adebayo replies that a model that never escalates any alert would still be right on 95% of the cross-validation set.

Adebayo is concerned that the 5% violation rate limits what the model can learn about violations.
He considers rebalancing the training set before retraining.

Before choosing a threshold, Adebayo runs a grid search over the LASSO penalty, lambda, holding the threshold at 0.50.
Results are shown in Exhibit 2.

**Exhibit 2: Grid search over lambda (log-loss)**

| Lambda | Training error | Cross-validation error | Features with non-zero coefficients |
|---|---|---|---|
| 0.001 | 0.061 | 0.148 | 211 |
| 0.05 | 0.092 | 0.097 | 38 |
| 2.0 | 0.171 | 0.176 | 4 |

On 9 June, Nandakumar makes two statements in the project log:

- Statement 1: "Lambda and the probability threshold are hyperparameters that we set, whereas the logistic regression coefficients are parameters learned from the training data."
- Statement 2: "Bias error and variance error are the measures used in the performance evaluation task to judge goodness of fit, alongside the confusion matrix and ROC curve."

Adebayo will present the ROC curve for the chosen specification to the compliance committee, with one point marked for each threshold in Exhibit 1.

## Questions

1. Based on Exhibit 1, the F1 score at the 0.50 threshold is closest to: (LOS: los-01-07-f)
   - A. 0.565.
   - B. 0.605.
   - C. 0.958.
2. Given Castellanos's 2 June priorities, which threshold in Exhibit 1 is most appropriate? (LOS: los-01-07-f)
   - A. 0.30
   - B. 0.50
   - C. 0.70
3. The point on the ROC curve that corresponds to the 0.30 threshold, expressed as (x-axis, y-axis), is closest to: (LOS: los-01-07-f)
   - A. (0.628, 0.850).
   - B. (0.850, 0.076).
   - C. (0.076, 0.850).
4. If Adebayo randomly undersamples the majority class in the training set until the two classes are of equal size, the rebalanced training set will contain: (LOS: los-01-07-f)
   - A. 2,880 alerts.
   - B. 4,800 alerts.
   - C. 54,720 alerts.
5. Based on Exhibit 2, the models with lambda of 0.001 and lambda of 2.0, respectively, are best described as: (LOS: los-01-07-c)
   - A. overfit with high variance, and underfit with high bias.
   - B. underfit with high bias, and overfit with high variance.
   - C. overfit with high variance, and a good fit because its two errors are close.
6. Which of Nandakumar's 9 June statements is correct? (LOS: los-01-07-f)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Precision $= 312 / (312 + 240) = 312 / 552 = 0.5652$.
> Recall $= 312 / (312 + 168) = 312 / 480 = 0.6500$.
> $F_1 = 2 \times 0.5652 \times 0.6500 / (0.5652 + 0.6500) = 0.7348 / 1.2152 = 0.6047$ (V1 p.313).
> A is wrong because 0.565 is the precision alone.
> C is wrong because $(312 + 8{,}880) / 9{,}600 = 0.9575$ is the accuracy, which is inflated by the 95% majority class.
> 2. **A.** A missed violation is a false negative, a Type II error, so the relevant metric is recall (V1 p.313).
> Recall is $408/480 = 0.8500$ at 0.30, $312/480 = 0.6500$ at 0.50, and $216/480 = 0.4500$ at 0.70, so 0.30 is best; the lower threshold escalates more alerts, trading more false positives for fewer false negatives (V1 p.341, p.342).
> B is wrong because 0.50 has the highest F1 (0.6047 against 0.5171 at 0.30 and 0.5714 at 0.70), but F1 weights FP and FN equally and Castellanos does not.
> C is wrong because 0.70 has the highest accuracy, $(216 + 9{,}060)/9{,}600 = 0.9663$, and the highest precision, $216/276 = 0.7826$, both of which reward avoiding false positives, the opposite of her concern; Adebayo's 95% naive benchmark shows why accuracy misleads under class imbalance (V1 p.311, p.314).
> 3. **C.** The ROC curve plots the false positive rate on the x-axis against the true positive rate on the y-axis (V1 p.314, p.315).
> $FPR = FP / (TN + FP) = 690 / (8{,}430 + 690) = 690 / 9{,}120 = 0.0757$.
> $TPR = TP / (TP + FN) = 408 / 480 = 0.8500$.
> A is wrong because $690 / (408 + 690) = 690 / 1{,}098 = 0.6284$ divides FP by predicted positives, which is one minus precision, not the false positive rate.
> B is wrong because it swaps the axes.
> 4. **A.** Training set $= 0.60 \times 48{,}000 = 28{,}800$ alerts; stratification keeps $0.05 \times 28{,}800 = 1{,}440$ violations and 27,360 non-violations.
> Undersampling the majority to match the minority leaves $1{,}440 + 1{,}440 = 2{,}880$ alerts (V1 p.311).
> B is wrong because $2 \times 2{,}400 = 4{,}800$ uses violations from the whole labelled dataset, which would leak cross-validation and test observations into training.
> C is wrong because $2 \times 27{,}360 = 54{,}720$ is the size after oversampling the minority to match the majority, not undersampling.
> 5. **A.** At lambda 0.001, training error is small (0.061) and CV error much larger (0.148): slight regularization, high variance, overfitting (V1 p.316, p.317).
> At lambda 2.0, both errors are large (0.171 and 0.176): large regularization, high bias, underfitting; the optimum is lambda 0.05, where the errors are close and small (V1 p.317).
> B is wrong because it reverses the diagnosis.
> C is wrong because close errors indicate a good fit only when they are also small; the 2.0 model's errors are almost double those at 0.05.
> 6. **A.** Statement 1 is correct: parameters such as regression coefficients are learned from the data, while hyperparameters such as lambda and the p-threshold are set manually and are not data-dependent (V1 p.316).
> Statement 2 is wrong: performance evaluation uses error analysis, ROC and AUC, and RMSE; bias and variance are the diagnostic language of the tuning task (V1 p.312, p.316).
> B and C are wrong because each accepts Statement 2.

## Distractor design

1. A: reports precision instead of F1; C: reports accuracy, the class-imbalance trap.
2. B: picks the best F1 when the cost is asymmetric; C: picks the best accuracy and precision, which guard against Type I rather than Type II cost.
3. A: wrong FPR denominator (predicted positives instead of actual negatives); B: swaps the ROC axes.
4. B: uses the full dataset's minority count instead of the training set's; C: confuses undersampling the majority with oversampling the minority.
5. B: reverses bias and variance; C: reads a small gap as a good fit without checking the error level.
6. B and C: place bias and variance under performance evaluation instead of tuning.
