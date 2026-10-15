---
type: cfa-lm
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
volume: 1
lm: 6
title: "Machine Learning"
pages: "197-274"
weight_band: "5-10%"
difficulty: 3
los_count: 4
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/quantitative-methods]
---

# LM6: Machine Learning

Difficulty 3 of 5: almost no arithmetic, but a very wide vocabulary (a dozen algorithms, each with its own hyperparameter, strength and failure mode) and the exam tests it by classification, so one blurred boundary (supervised vs unsupervised, regression vs classification, bias vs variance, k-means vs hierarchical) costs a whole item set.

## LOS map

- **describe** supervised machine learning, unsupervised machine learning, and deep learning (V1 p.199) ^los-01-06-a
    - Examiner asks: given a vignette describing the data (labeled or not) and the target (continuous, categorical, none), name the class of problem (regression, classification, dimension reduction, clustering) and whether it is supervised, unsupervised, or deep/reinforcement learning.
- **describe** overfitting and identify methods of addressing it (V1 p.203) ^los-01-06-b
    - Examiner asks: read "fits the training set well but predicts new data poorly" as overfitting and high variance error, then pick the remedy (a penalty that increases with complexity, or k-fold cross-validation) and reject the distractor that reverses the sign of the penalty or uses k-fold on time series.
- **describe** supervised machine learning algorithms - including penalized regression, support vector machine, k-nearest neighbor, classification and regression tree, ensemble learning, and random forest - and determine the problems for which they are best suited (V1 p.209) ^los-01-06-c
    - Examiner asks: "which technique is most appropriate" for a described problem (continuous vs categorical target, linear vs non-linear features, need for interpretability, many correlated features), plus a hyperparameter question (lambda, k, cost parameter, tree depth) and a LASSO with lambda = 0 trap.
- **describe** unsupervised machine learning algorithms - including principal components analysis, k-means clustering, and hierarchical clustering - and determine the problems for which they are best suited (V1 p.232) ^los-01-06-d
    - Examiner asks: distinguish dimension reduction (PCA, eigenvalues, scree plot) from clustering, choose k-means when the number of groups is known and hierarchical when it is not, and identify what must be specified (features, distance measure, k) before any clustering algorithm runs.

## Core intuition

> [!abstract] The whole module in one sentence
> Machine learning is "find the pattern, apply the pattern": an algorithm learns structure from data with fewer a priori assumptions than classical statistics, and the only score that matters is how well the learned pattern predicts data it has never seen (V1 p.199, p.204).

### Why the curriculum bothers with machine learning

Statistical models such as regression start from explicit structural assumptions, for example that observations are drawn from a specified distribution and that the relationship is linear (V1 p.199).
Those assumptions can fail, and when they do the model fails with them.
Machine learning drops most of the assumptions and lets the algorithm extract the structure directly from large amounts of data (V1 p.199).
That makes ML better than regression at problems with many variables (high dimensionality) or a high degree of non-linearity, and good at detecting change such as the preconditions of a regime switch (V1 p.199).
The curriculum's honest framing is that the investment practitioner does not need to master the mathematics but must be able to source appropriate inputs, interpret outputs, and translate them into actions, which requires the vocabulary this module teaches (V1 p.198).
The uses run the whole value chain: chatbots for client questions, alpha signals from non-linear forecasts or text analysis of 10-K and 10-Q changes, portfolio weights that maximise a Sharpe ratio under client restrictions, a covariance matrix estimated with fewer variables via PCA, and non-linear trading algorithms that cut implementation costs (V1 p.198).

### Three classes of learning, and the vocabulary shift

The module divides ML into supervised learning, unsupervised learning, and deep learning/reinforcement learning (V1 p.199).
Supervised learning infers a pattern between inputs (the Xs) and a known output (Y) from a labeled dataset, one where each observation pairs inputs with the associated output (V1 p.199).
Applying the algorithm to labeled data is called training; the learned pattern is then used to predict Y for new inputs (V1 p.199).
Multiple regression is itself supervised learning, and Exhibit 1 is a dictionary: the dependent variable is the target, the independent variables are the features, and the fit is judged by comparing predicted targets to actual targets on labeled test data (V1 p.200).
The credit card example fixes the picture: target is 1 for fraudulent, 0 otherwise, the features are transaction characteristics, and the program "learns from experience" if its hit rate rises as the database grows (V1 p.200).

> [!abstract] The first fork is always the target variable
> A continuous target makes the task regression, even if the technique is not "regression"; a categorical or ordinal target makes it classification and the model is called a classifier (V1 p.200).
> Ordinal targets such as credit ratings are ranked categories and sit between categorical and continuous on the measurement scale (V1 p.201).

Unsupervised learning has inputs but no target: the algorithm must discover structure in the data themselves, which makes it the tool for exploring datasets too big or complex to visualise (V1 p.201).
Its two problem types are dimension reduction, which cuts the number of features while retaining the variation across observations that carries the information, and clustering, which sorts observations into groups more similar within than between (V1 p.201).
Deep learning uses neural networks, highly flexible algorithms for supervised and unsupervised tasks with large datasets, non-linearities and interactions among features, to address complex tasks such as image classification and natural language processing (V1 p.201).
In reinforcement learning the computer learns from interacting with itself or with data generated by the same algorithm (V1 p.201).
Exhibit 2 organises every algorithm in the module by two axes, supervised vs unsupervised and continuous vs categorical variables; the exam tests that grid directly (V1 p.202).

| Target variable | Supervised (target present) | Unsupervised (no target) |
|---|---|---|
| Continuous | Regression: linear, penalized regression/LASSO, logistic, CART, random forest | Dimension reduction: PCA. Clustering: k-means, hierarchical |
| Categorical | Classification: logistic, SVM, KNN, CART | Dimension reduction: PCA. Clustering: k-means, hierarchical |
| Continuous or categorical | Neural networks, deep learning, reinforcement learning | Neural networks, deep learning, reinforcement learning |

### Overfitting: perfect hindsight, no foresight

Flexibility has a price.
An algorithm that fits the training data too well has absorbed noise and random fluctuations into the learned relationship, and that noise is absent from new data, so the model does not generalise (V1 p.203).
Generalisation means the model retains its explanatory power out of sample, and evaluation therefore focuses on prediction error on new data rather than on goodness of fit on the training data (V1 p.203, p.204).
The dataset is partitioned into three non-overlapping samples: a training sample to fit, a validation sample to tune and make structural choices, and a test sample to confirm predictive power; training and validation are "in-sample", the test sample is "out-of-sample" (V1 p.204, p.207).
The suit analogy is worth keeping: overfitting is a custom suit that fits one person, underfitting is a baggy suit that fits no one, robust fitting is a universal suit for people of similar dimensions (V1 p.204).
Complexity means the number of features, terms or branches and whether the model is linear or non-linear, and the two main contributors to overfitting are high noise and too much complexity (V1 p.204).

> [!abstract] Out-of-sample error has three parts and the exam asks which one you have
> Bias error is the degree to which the model fits the training data; erroneous assumptions give high bias, underfitting and high in-sample error.
> Variance error is how much results change on new data; unstable models pick up noise, giving overfitting and high out-of-sample error.
> Base error is randomness in the data and cannot be removed (V1 p.205).

Two pictures carry this.
The learning curve plots out-of-sample accuracy (1 minus error rate) against training sample size: a robust model's training and validation error rates converge toward the desired rate, a high-bias model converges below the desired accuracy and more data will not help, and a high-variance model's curves fail to converge (V1 p.205).
The fitting curve plots in-sample and out-of-sample error against model complexity: as complexity rises, in-sample error and bias fall while out-of-sample error and variance rise, so total error is U-shaped and the optimum sits where the bias and variance curves cross, just before total error starts to rise (V1 p.206).
Linear functions are more prone to bias and underfitting; non-linear functions are more prone to variance and overfitting (V1 p.206).
The trade-off is often expressed as cost (the gap between in- and out-of-sample error) against complexity (V1 p.207).

Two remedies exist and only two (V1 p.207).
The first is Occam's razor applied to models: limit the number of features and penalise complexity so that a parameter is kept only if it reduces out-of-sample error, which requires estimating an overfitting penalty.
The second is proper sampling through cross-validation, which estimates out-of-sample error directly from validation samples.
K-fold cross-validation shuffles the data (excluding the test sample and fresh data), splits it into k equal sub-samples, trains on k minus 1 of them and validates on the kth, and repeats k times so that each data point is used in training k minus 1 times and in validation once; k is typically 5 or 10 and the mean of the k validation errors estimates the out-of-sample error (V1 p.207).
The limitation the exam loves: k-fold cannot be used with time-series data, where only the most recent data can reasonably validate (V1 p.207).
The deep-learning case study shows the time-series alternative, walk-forward optimisation, where each period's test set becomes the next period's training set (V1 p.256).

### The supervised toolkit: what each algorithm does and when to reach for it

Penalized regression attacks overfitting at the source by adding to the sum of squared residuals a penalty that grows with the number of included features, so a feature stays only if it improves fit by more than the penalty it costs (V1 p.210).
LASSO uses the sum of absolute coefficients times lambda; because it drives unimportant coefficients to exactly zero it performs feature selection automatically, and with lambda equal to zero it collapses to OLS (V1 p.210).
Features are standardised to mean 0 and variance 1 so coefficient sizes are comparable, lambda is a hyperparameter tuned on the validation set, and the penalty is used only while fitting; once built the model is judged by squared residuals on the test set (V1 p.210).
Regularisation is the general name for shrinking estimates toward zero to reduce statistical variability in high-dimensional problems; it has cut default-forecasting feature sets to under 10 variables and stabilised covariance matrices for mean-variance optimisation (V1 p.210, p.211).

Support vector machine is a linear classifier: it finds the hyperplane that separates two labeled groups by the maximum margin, the widest strip between the classes (V1 p.211, p.212).
The margin is set by the closest observations, the support vectors, so adding data far from the boundary changes nothing, while adding data near it can move the boundary (V1 p.212).
When the data are not linearly separable, soft margin classification adds a penalty for misclassified training points and trades a wider margin against a lower error penalty; non-linear SVMs use curved boundaries and are more prone to overfitting (V1 p.212).
SVM suits small to medium but complex high-dimensional datasets such as financial statements or bankruptcy databases, is resilient to outliers and correlated features, and classifies text sentiment (V1 p.212).

K-nearest neighbor classifies a new observation by the majority label among its k closest existing observations; with k = 1 it copies its nearest neighbour, with k = 5 it takes a vote of five (V1 p.213).
It is non-parametric, handles multi-class problems directly, and its critical challenge is defining "similar": the distance metric, the feature selection (irrelevant or correlated features hurt, so it works best with few features), and k itself (V1 p.213, p.214).
An even k can produce ties; a k too small is noisy and sensitive to local outliers; a k too large dilutes the idea of nearest neighbours (V1 p.214).
Applications include bankruptcy prediction, implied bond ratings and custom index construction (V1 p.214).

Classification and regression tree splits the feature space one feature and one cutoff at a time, from a root node through decision nodes to terminal nodes; at each node it picks the feature and cutoff that produce the widest separation of the labels, and it stops when a further split adds little (V1 p.214, p.217).
A classification tree predicts the majority class at the terminal node; a regression tree predicts the mean of the labeled values there (V1 p.217).
The same feature can reappear lower down, and some features matter only after other conditions hold, which is how CART captures non-linear dependencies that multiple regression misses (V1 p.215, p.217).
Left unconstrained CART memorises the training data, so it is regularised by maximum depth, minimum node population, maximum number of decision nodes, or by pruning weak branches afterwards (V1 p.217).
Its selling point is the visual explanation of every prediction, which makes it an expert-system builder and a client-communication tool; typical uses are fraud detection in financial statements and consistent security selection (V1 p.218).

Ensemble learning combines the predictions of many models so the noise averages out; it is usually more accurate and more stable than the best single model (V1 p.218, p.219).
Heterogeneous ensembles combine different algorithms with a majority-vote classifier; homogeneous ensembles train the same algorithm on different bootstrap samples, bagging, and aggregate by vote for classification or average for regression (V1 p.219).
More models help up to a point, beyond which overfitting sets in; diversity of algorithms and hypotheses is what makes the law of large numbers work (V1 p.219).
A random forest is many CARTs trained by bagging, with extra diversity from considering only a random subset of m of the n features at each split; its hyperparameters are m, the number of trees, minimum node size and maximum depth (V1 p.219).
It reduces variance, protects against overfitting, and improves signal to noise, but it loses the interpretability of a single tree and is relatively black box (V1 p.220).

### The unsupervised toolkit

Principal components analysis transforms highly correlated features into a few uncorrelated composite variables by working on the covariance matrix (V1 p.232).
Eigenvectors define the new composite variables, each a linear combination of the original features and a direction in feature space; the eigenvalue attached to each gives the proportion of total variance it explains (V1 p.232, p.233).
PC1 is the line that minimises the sum of projection errors and maximises the spread of the data along it, PC2 is at right angles to PC1 and therefore uncorrelated with it, and so on (V1 p.233).
A scree plot shows variance explained per component and the analyst keeps the smallest number that reaches a desired share, often 85% to 95%; in the index illustration three components explained about 90% for the DLC 500 and 86% for the VLC 30 (V1 p.234, p.235).
The drawback is interpretability: composites cannot be labeled, so PCA is a black box, but lower-dimensional data train faster, overfit less by escaping the curse of dimensionality, and are easier to interpret downstream (V1 p.235).

Clustering seeks cohesion (observations within a cluster close together) and separation (clusters far apart) under a chosen distance measure, usually Euclidean straight-line distance or, for diversification work, correlation (V1 p.236).
The analyst must specify the features that define similarity and the distance measure before any algorithm runs (V1 p.236, p.243).
K-means partitions observations into a fixed number k of non-overlapping clusters by alternating two steps until nothing moves: assign each observation to its nearest centroid, then recompute each centroid as the average of its members (V1 p.237).
It is fast and scales to hundreds of millions of observations, but the result can depend on the initial centroids, so it is rerun from several starts, and k must be chosen in advance, in practice by face validity (V1 p.238).
Hierarchical clustering builds a hierarchy instead: agglomerative (bottom-up) starts with every observation as its own cluster and repeatedly merges the two closest, divisive (top-down) starts with one cluster and repeatedly splits (V1 p.239, p.240).
Agglomerative is faster, is used on large datasets and finds small clusters well because it works from local patterns; divisive sees the global structure and finds large clusters better (V1 p.240).
The dendrogram plots the merge history with arch height equal to the distance between merged clusters, so a horizontal cut at any height reads off a clustering of any granularity, which is the advantage over k-means: no k up front (V1 p.241).
Diversifying across clusters with maximum separation is a natural portfolio construction rule, and concentration inside one cluster flags concentrated risk (V1 p.241, p.242).

### Neural networks, deep nets, reinforcement learning

A neural network is regression with transformed features: an input layer with one node per feature, one or more hidden layers where learning happens, and an output layer (V1 p.249).
Each hidden node has a summation operator, which multiplies inputs by link weights and sums them into the total net input, and an activation function, a non-linear "dimmer switch" such as the sigmoid (output 0 to 1) or ReLU that scales the input into the node's output (V1 p.250).
Forward propagation passes outputs layer to layer; training compares predictions to labels by a loss such as mean squared error and adjusts weights backward through the layers (backward propagation) by the learning rate times the gradient of total error (V1 p.250, p.251).
The numbers of input, hidden and output nodes (4, 5, 1 in Exhibit 29), the activation function and the learning rate are hyperparameters; the trained weights are the parameters (V1 p.249, p.250, p.251).
More nodes and layers raise capacity and overfitting risk together; the trade-offs are black-box opacity and the data and compute needed (V1 p.251).
A deep neural network has many hidden layers, at least 2 and potentially more than 20, ends in a set of class probabilities and assigns the highest, and owes its success to large machine-readable datasets, better fitting methods and GPU hardware (V1 p.252).
Reinforcement learning has an agent taking actions in an environment to maximise reward over time, with neither labels nor instant feedback, learning through millions of trials; its success in markets is an open question (V1 p.253).

### The selection flowchart, as the exam tests it

Exhibit 37 is a decision tree and every "most appropriate technique" question is a walk through it (V1 p.264).

| Question in order | Answer | Technique |
|---|---|---|
| Complexity reduction needed (many highly correlated features)? | Yes | PCA |
| Numerical prediction (continuous target)? | Yes, linear data | Penalized regression, LASSO |
| Numerical prediction? | Yes, complex non-linear data | CART, random forest, neural nets |
| Classification with labeled data? | Linear data | KNN or SVM |
| Classification with labeled data? | Complex non-linear data | CART, random forest, neural nets |
| Classification with unlabeled data? | Non-linear data | Neural nets |
| Classification with unlabeled data, linear? | Number of categories known | K-means |
| Classification with unlabeled data, linear? | Number of categories unknown | Hierarchical clustering |

| Algorithm | Supervised? | Target | Hyperparameters named | Best suited to | Main weakness |
|---|---|---|---|---|---|
| Penalized regression / LASSO | Yes | Continuous | Lambda | Many correlated features, parsimony, feature selection (V1 p.209, p.210) | Linear only |
| SVM | Yes | Categorical (binary) | Cost parameter (margin penalty) | Small to medium, high-dimensional, outliers and correlated features (V1 p.212, p.226) | Linear boundary unless non-linear SVM, which overfits |
| KNN | Yes | Categorical, sometimes continuous | k, distance metric | Similarity problems, multi-class, few features (V1 p.213, p.214) | Sensitive to irrelevant features and to k |
| CART | Yes | Either | Max depth, min node population, max nodes, pruning | Non-linear interactions, interpretability (V1 p.217, p.218) | Overfits if unconstrained |
| Random forest | Yes | Either | m features per split, number of trees, node size, depth | Noisy data, generalisation, fraud with class imbalance (V1 p.219, p.220) | Black box |
| PCA | No | None | Number of components retained | Highly correlated features, visualisation, pre-processing (V1 p.232, p.235) | Components not interpretable |
| K-means | No | None | k, distance measure | Very large datasets, known number of groups (V1 p.237, p.238) | k in advance, initial centroids |
| Hierarchical | No | None | Distance and linkage measure | Unknown number of groups, multiple granularities (V1 p.239, p.241) | More compute than k-means |
| Neural networks / DNN | Either | Either | Layers, nodes, activation, learning rate | Non-linearities and interactions, large data (V1 p.249, p.252) | Black box, data and compute hungry |
| Reinforcement learning | Neither | Reward | Actions, environment | Sequential decisions, games, virtual trading (V1 p.253) | Unproven in markets |

## Formulas and derivations

**Decomposition of out-of-sample error** (V1 p.205)
$$ E_{out} = \text{Bias error} + \text{Variance error} + \text{Base error} $$
^f-01-06-1

- $E_{out}$: total out-of-sample error measured on the validation or test sample; $E_{in}$ is the same measure on the training sample (V1 p.205).
- Bias error: how well the model fits the training data; high bias means underfitting and high $E_{in}$.
- Variance error: how much results change on new data; high variance means overfitting and high $E_{out}$ with low $E_{in}$.
- Base error: randomness in the data, irreducible (V1 p.265).
- Reason it holds: the summary states out-of-sample error equals bias plus variance plus base error; low $E_{in}$ with high $E_{out}$ therefore isolates variance as the culprit (V1 p.205, p.265).

**Accuracy rate on a learning curve** (V1 p.205)
$$ \text{Accuracy rate} = 1 - \text{Error rate} $$
^f-01-06-2

- Plotted on the y-axis against the number of training samples; the desired accuracy rate is a horizontal target line (V1 p.206).
- Robust model: training and validation accuracy converge toward the desired rate as data grow; high bias: converge below it; high variance: fail to converge (V1 p.205).

**K-fold cross-validation estimate of out-of-sample error** (V1 p.207)
$$ \hat{E}_{out} = \bar{E}_{val} = \frac{1}{k} \sum_{j=1}^{k} E_{val, j} $$
^f-01-06-3

- $k$: number of equal sub-samples after random shuffling, typically 5 or 10; the test sample and fresh data are excluded first.
- Fold $j$ trains on $k - 1$ sub-samples and validates on the remaining one, so each point is in training $k - 1$ times and in validation once.
- Reason: averaging $k$ validation errors uses all in-sample data for both roles, mitigating the holdout problem of shrinking the training set, and reducing both bias and variance of the error estimate.
- Not valid for time series, where only the most recent data can validate; use walk-forward optimisation instead (V1 p.207, p.256).

**OLS objective** (V1 p.210)
$$ \min_{\hat{b}_0, \dots, \hat{b}_K} \sum_{i=1}^{n} \left(Y_i - \hat{Y}_i\right)^2 $$
^f-01-06-4

- $Y_i$: actual target; $\hat{Y}_i$: predicted target from $K$ standardised features (mean 0, variance 1) so coefficient magnitudes are comparable.
- This is the benchmark LASSO adds a penalty to; with no penalty every feature that reduces squared residuals at all is kept, which invites overfitting when $K$ is large (V1 p.209).

**LASSO penalty term** (V1 p.210)
$$ \text{Penalty term} = \lambda \sum_{k=1}^{K} \left|\hat{b}_k\right|, \quad \lambda > 0 $$
^f-01-06-5

- $\lambda$: hyperparameter set before learning, tuned on the validation set; larger $\lambda$ penalises the loss more heavily (V1 p.210, p.258).
- $\hat{b}_k$: standardised coefficient on feature $k$; only non-zero coefficients contribute, so the penalty increases with the number of included features.
- Sign convention: the penalty is added to the loss, so it always raises the objective; the exam distractor is a penalty that "decreases with the number of features" (V1 p.209).

**LASSO objective (penalized regression)** (V1 p.210)
$$ \min \left[ \sum_{i=1}^{n} \left(Y_i - \hat{Y}_i\right)^2 + \lambda \sum_{k=1}^{K} \left|\hat{b}_k\right| \right] $$
^f-01-06-6

- Derivation of the selection rule: adding feature $k$ lowers the first sum by some $\Delta SSR$ and raises the second by $\lambda |\hat{b}_k|$; the feature survives only if $\Delta SSR > \lambda |\hat{b}_k|$, so LASSO performs feature selection automatically (V1 p.210).
- Special case: $\lambda = 0$ reproduces OLS exactly, which is why "LASSO with lambda equal to 0" is the least appropriate regularised model (V1 p.210, p.273).
- The penalty applies only during fitting on training data; the finished model is scored by squared residuals on the test set (V1 p.210).
- The same L1 penalty shrinks the weights of a neural network in the deep-learning case study (V1 p.255).

**Classification metrics: accuracy, precision, recall, F1** (V1 p.221, p.226, p.227)
$$ \text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}, \quad \text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN} $$
^f-01-06-7

- Type I error is a false positive $FP$; Type II error is a false negative $FN$; $TP$ and $TN$ are correct classifications (V1 p.226).
- Precision: correctly predicted positives over all predicted positives; recall: correctly predicted positives over all actual positives (V1 p.221, p.227).
- F1 score is described in this module as the weighted average of precision and recall and is the better metric under class imbalance; LM07 gives its explicit form $F1 = 2 \times P \times R / (P + R)$ (V1 p.227).
- Benchmark: with three equally likely classes a useless model scores about 1/3; values near 1 are excellent (V1 p.227).

**CART class probability at a terminal node** (V1 p.230)
$$ P(\text{class } c) = \frac{n_c}{n_{\text{node}}} $$
^f-01-06-8

- $n_c$: training observations of class $c$ that reached the terminal node; $n_{\text{node}}$: all observations there, shown as "value = [winners, average, losers]" and "samples" in Exhibit 17 (V1 p.229).
- The predicted class is the majority class; for a regression tree the prediction is the mean of the labeled values at the node (V1 p.217).
- Example: node value [13, 4, 4] gives $13/21 = 0.619$ for winner and $4/21 = 0.190$ for each other class (V1 p.230).

**Proportion of variance explained by a principal component** (V1 p.232, p.233)
$$ \text{Share explained by PC}_j = \frac{\lambda_j}{\sum_{m=1}^{M} \lambda_m}, \quad \lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_M $$
^f-01-06-9

- $\lambda_j$: eigenvalue attached to eigenvector $j$ of the feature covariance matrix; it gives the proportion of total variance explained by that eigenvector (V1 p.232).
- Components are ordered from largest to smallest eigenvalue; the scree plot graphs these shares and the analyst retains the fewest components that reach a desired cumulative share, often 85% to 95% (V1 p.233, p.234).
- Reason: PC1 is the direction that minimises total projection error and maximises spread; PC2 is orthogonal to PC1, hence uncorrelated, and explains the most remaining variance (V1 p.233).

**Euclidean distance between two observations** (V1 p.236)
$$ d(\mathbf{x}, \mathbf{y}) = \sqrt{\sum_{j=1}^{p} \left(x_j - y_j\right)^2} $$
^f-01-06-10

- $x_j, y_j$: values of feature $j$ for the two observations, after standardisation when units differ.
- Smaller distance means more similar; the module also names correlation, the average Euclidean distance between standardised points, as the distance for diversification work (V1 p.236).
- The distance measure, like the feature set, must be chosen by the analyst before k-means, hierarchical clustering or KNN can run (V1 p.236, p.243).

**K-means centroid update** (V1 p.237)
$$ \mathbf{c}_g = \frac{1}{n_g} \sum_{i \in g} \mathbf{x}_i $$
^f-01-06-11

- $\mathbf{c}_g$: centroid of cluster $g$; $n_g$: observations currently assigned to it.
- Loop: assign each observation to its nearest centroid, recompute centroids as the average of members, repeat until no observation changes cluster; the result minimises intra-cluster distance (cohesion) and maximises inter-cluster distance (separation) for the fixed $k$ (V1 p.237).

**Average linkage distance between two clusters** (V1 p.240, p.246)
$$ d(A, B) = \frac{1}{n_A n_B} \sum_{i \in A} \sum_{j \in B} d(i, j) $$
^f-01-06-12

- Cluster distance may be defined as the minimum, maximum or average of the pairwise straight-line distances between members (V1 p.240).
- Case study: distance from UBS to the cluster GS_JPM is $(0.243 + 0.281)/2 = 0.262$; distance from the three banks to AAPL_GOOG is $(0.364 + 0.380 + 0.375 + 0.332 + 0.338 + 0.345)/6 = 0.356$ (V1 p.246).
- The arch height in the dendrogram equals this merge distance (V1 p.245).

**Rectified linear unit activation** (V1 p.249)
$$ f(x) = \max(0, x) $$
^f-01-06-13

- Outputs zero for a negative input and the input itself when positive; it is one of the non-linear activation choices, the other named one being the S-shaped sigmoid with range 0 to 1 (V1 p.249, p.250).

**Neural network as regression with transformed features** (V1 p.249)
$$ y = \beta_1 \max(0, x_1 + x_2 + x_3) + \beta_2 \max(0, x_2 + x_4) + \beta_3 \max(0, x_2 + x_3 + x_4) + \varepsilon = \beta_1 z_1 + \beta_2 z_2 + \beta_3 z_3 + \varepsilon $$
^f-01-06-14

- $z_1, z_2, z_3$: hidden-node outputs, each a ReLU of a sum of inputs; the output node combines them linearly.
- Compare with regression $y = \beta_1 x_1 + \beta_2 x_2 + \beta_3 x_3 + \beta_4 x_4 + \varepsilon$: the only structural difference is the non-linear transformation in the hidden layer (V1 p.249).
- Inputs are scaled first, for example each positive input divided by its maximum to lie in 0 to 1 (V1 p.249).

**Hidden node: summation operator and activation** (V1 p.250)
$$ \text{Total net input} = \sum_{j} w_j x_j, \qquad \text{Node output} = g\!\left(\sum_{j} w_j x_j\right) $$
^f-01-06-15

- $w_j$: weight on the link from input $j$, initially random, learned in training; $g$: activation function, chosen by the modeller (a hyperparameter), typically sigmoid or ReLU.
- A very negative net input through a sigmoid gives an output near 0 (node does not trigger); a positive one gives near 1 (node triggers); passing outputs forward is forward propagation (V1 p.250).

**Weight update in training** (V1 p.251)
$$ w_{\text{new}} = w_{\text{old}} - \eta \, \frac{\partial E}{\partial w_{\text{old}}} $$
^f-01-06-16

- $\eta$: learning rate, a hyperparameter setting the size of each adjustment; $\partial E / \partial w$: gradient of total error (for example MSE) with respect to the weight.
- The minus sign moves the weight against the gradient to reduce error; working backward through the layers is backward propagation; the final weights are the network's parameters (V1 p.251).

**Cross-sectional fundamental factor model** (V1 p.255)
$$ r_t = B f_t + \varepsilon_t $$
^f-01-06-17

- $r_t$: vector of $N$ stock returns at time $t$; $B$: $N \times K$ matrix of factor loadings (betas); $f_t$: factor returns estimated by cross-sectional regression; $\varepsilon_t$: model error.
- The DNN case replaces this linear map with a network that learns non-linear relations between loadings and returns, minimising out-of-sample MSE with a LASSO penalty on the weights (V1 p.255).

**Winner and loser labels in the fund case** (V1 p.225)
$$ \text{Label} = \begin{cases} +1 & \text{if } r \ge \bar{r} + \sigma_r \\ -1 & \text{if } r \le \bar{r} - \sigma_r \\ 0 & \text{otherwise} \end{cases} $$
^f-01-06-18

- $r$: one-month fund return; $\bar{r}, \sigma_r$: mean and standard deviation across all ETFs or all MFs respectively.
- Most funds land at 0, which is the class imbalance that makes F1 the preferred metric (V1 p.226, p.227).

**Information ratio used to back-test the DNN stock picks** (V1 p.259)
$$ IR = \frac{\alpha}{\text{Nonsystematic risk}} $$
^f-01-06-19

- Abnormal return per unit of risk for a well-diversified portfolio; 0.40 to 0.60 is considered quite good (V1 p.260).
- In-sample IRs of 0.697 to 0.623 versus out-of-sample 0.260 to 0.315 illustrate why only out-of-sample performance is a realistic assessment (V1 p.259, p.260).

## Worked examples

### Example 1: Machine learning overview (V1 p.202)

Four knowledge-check questions on definitions.

Q1: what best describes machine learning?
Answer B: a set of algorithmic approaches that generate structure or predictions from data without human intervention by finding a pattern and applying it (V1 p.199).
A is wrong because ML is not just for linear regression; C is wrong because ML is not limited to linear, labeled datasets.

Q2: discovering groupings with no target variable.
Answer A: unsupervised learning.
B and C both describe supervised learning, which requires labeled data and predicts a target (V1 p.201).

Q3: what distinguishes supervised learning?
Answer A: training on labeled data to infer a pattern-based prediction rule (V1 p.200).
B contradicts the labeled-data requirement; C describes unsupervised learning.

Q4: what is dimension reduction?
Answer C: reducing the number of features while retaining variation across observations to preserve the information in that variation (V1 p.201).
A describes classification; B describes clustering.
^ex-01-06-1

### Example 2: Evaluating ML algorithm performance (V1 p.208)

Setting: Shreya Anand classifies NIFTY 200 companies into dividend increase or no increase using 1,000 observations with 25 features and a labeled target; the model classifies the training sample well but not new data.

Q1: which statement defines good generalisation?
Statement 1, the model retains explanatory power out of sample, is correct (V1 p.203).
Statement 2 describes low in-sample power, a high-bias underfit; Statement 3 describes losing power out of sample, an overfit.

Q2: what impairs Anand's model?
Good in-sample, poor out-of-sample is the signature of overfitting, and overfitting is variance error (V1 p.205).
Answer B.
A pairs underfitting with bias, which would show poor in-sample fit; C pairs overfitting with bias, a contradiction.

Q3: which action addresses it?
Answer B: k-fold cross-validation to estimate out-of-sample error, then adjust the model (V1 p.207).
A is wrong because the penalty must increase, not decrease, with the number of features (V1 p.210).
C is wrong because her data are labeled and the task is classification; unsupervised models do not use labels.
Check on the data: with k = 5 each validation fold holds $1{,}000/5 = 200$ observations and each point is trained on 4 times.
^ex-01-06-2

### Example 3: Support vector machine and k-nearest neighbor (V1 p.221)

Setting: Rachel Lee must decide whether an unrated Biotron bond is low investment grade (Baa3/BBB-) or high non-investment grade (Ba1/BB+).

Q1: type of problem.
Supervised classification: the target is a rating category and the training data (rated bonds with features) are labeled (V1 p.221).

Q2: two algorithms and how each applies.
SVM: train on features and ratings of bonds in the two neighbouring buckets, find the maximum-margin hyperplane, and read which side Biotron falls on (V1 p.221, p.222).
KNN: pre-specify k, find the k rated bonds most similar to Biotron under the chosen distance measure, and assign the majority rating (V1 p.222).

Q3: why agreement between the two supports Watson's confidence.
If the two algorithms disagreed, the classification would be sensitive to the algorithm's approach; agreement shows the result is robust to the choice of method, so it is more likely correct (V1 p.222).
^ex-01-06-3

### Example 4: CART and ensemble learning (V1 p.222)

Setting: Laurie Kim wants to classify B/B2 to CCC/Caa2 high-yield bonds as default or no default using 19 fundamental and 5 technical factors, with strong non-linearities in the features.

Q1: problem type.
Classification (default vs no default), supervised because the history is labeled (V1 p.222).

Q2: dimensionality.
$19 + 5 = 24$ features, so the model has dimensionality 24 (V1 p.223).

Q3: is CART appropriate?
Yes: CART handles complex non-linear relationships and its tree gives a visual, interpretable explanation for the investment committee and clients (V1 p.223).

Q4: what CART does at each node.
It chooses the feature and the cutoff value that generate the widest separation of the labeled data, minimising classification error (V1 p.217, p.223).

Q5: avoiding overfitting.
Add regularisation parameters (maximum depth, minimum node population, maximum number of decision nodes) that stop the tree growing, or prune branches with little classifying power afterwards (V1 p.217, p.223).

Q6: how ensemble learning improves it.
Combine predictions from many models so noise averages out: heterogeneous learners (different algorithms with a voting classifier) or homogeneous learners (same algorithm on bagged training sets), including a random forest of CARTs trained by bagging (V1 p.219, p.223).
^ex-01-06-4

### Example 5: Classification of funds with a CART tree (V1 p.229)

Setting: a five-level CART on 1,067 ETFs using only valuation ratios; new ETF has P/S = 2.29, P/E = 7.20, P/B = 1.41, P/CF = 2.65; left branch is True.

Q1: trace the path.
Root: P/S <= 7.93? 2.29 <= 7.93, True, go left (node value [108, 864, 90], 1,062 samples).
Level 2: P/E <= 12.08? 7.20 <= 12.08, True, go left (value [42, 173, 30], 245 samples).
Level 3: P/S <= 1.32? 2.29 > 1.32, False, go right (value [20, 21, 6], 47 samples).
Level 4: P/B <= 1.275? 1.41 > 1.275, False, go right to the terminal node with value [13, 4, 4].
Majority class is winner (+1), so the prediction is winner (V1 p.230).
P/CF is never consulted on this path.

Q2: probability of the predicted class.
$P(\text{winner}) = 13/21 = 0.619$, about 62%; $P(\text{average}) = P(\text{loser}) = 4/21 = 0.190$, about 19% each (V1 p.230).
Consistency check on the exhibit: with three classes, $1 - (0.619^2 + 0.190^2 + 0.190^2) = 0.544$, which matches the "gini = 0.544" printed at that node, and the root gives $1 - ((108/1067)^2 + (864/1067)^2 + (95/1067)^2) = 0.326$, matching "gini = 0.326"; the Gini impurity formula is not a curriculum formula, it is my check that the exhibit numbers are internally consistent.

Q3: why be cautious.
Depth was capped at five levels for visualisation; only some of the important features from Exhibit 16 were used (adding asset class ratios, sector weights and especially net assets should raise F1); and only 21 of 1,067 funds reach this node, with 13 winners, too few for statistical confidence (V1 p.230).
A random forest, being an ensemble, would generalise out of sample better than any single tree (V1 p.230).
^ex-01-06-5

### Example 6: Investment uses of clustering algorithms (V1 p.242)

Setting: a Europe Diversified Equity Fund benchmarked to the STOXX Europe 600 may have hidden concentrations; three suggestions are on the table and analyst Kane makes two claims.

Q1: which suggestion is an ML task?
Answer B: finding inherent groupings among holdings from eight numerical measures is clustering (V1 p.243).
Suggestions 1 and 3 (exposure aggregation, and regressing fund returns on country and sector indexes) are traditional analysis and regression.

Q2: is Kane right that only the distance measure and k need specifying?
Answer C: not correct, because the feature set that defines similarity must also be specified whichever algorithm is used (V1 p.243).
B is wrong because no other hyperparameter is required by hierarchical clustering.

Q3: best justification for preferring hierarchical clustering.
Answer C: the number of distinct groups in the index is unknown, and k-means needs k in advance while hierarchical clustering sorts without that prior input (V1 p.243).
A is wrong because k-means is the faster algorithm, which would argue the other way (V1 p.238, p.239); B is wrong because dimensionality is not the deciding issue.
^ex-01-06-6

### Example 7: Hierarchical agglomerative clustering with six stocks (V1 p.247)

Setting: the eight-stock case (AAPL, F, FB, GM, GS, GOOG, JPM, UBS) is rerun without the auto stocks F and GM.

Q1: how the inputs change.
Same panel of closing prices and daily log returns but for six stocks, and a 6 by 6 distance matrix without the F and GM rows and columns (V1 p.247).

Q2: the three resulting clusters.
GS_JPM_UBS (banks), AAPL_GOOG (technology), and FB alone (V1 p.248).

Q3: why the result differs from the eight-stock case.
Replaying the merges from the distance matrix: JPM and GS merge first at 0.215; UBS joins at average distance $(0.243 + 0.281)/2 = 0.262$; AAPL and GOOG merge at 0.307 (V1 p.245, p.246).
In the eight-stock case the next merge was F with GM at 0.334 and then banks with AAPL_GOOG at 0.356, leaving three clusters of five stocks, two autos, and FB (V1 p.246).
With no autos there is no need to merge AAPL_GOOG into the bank cluster to reach three clusters, so the cut leaves the banks, the two tech names and FB separate; FB remains an outlier because its distances to everything else are the largest in the matrix (0.437 to 0.491) (V1 p.245, p.248).

Q4: new recommendation.
Buy FB, buy the cheaper of AAPL or GOOG, and buy the most attractive of GS, JPM or UBS, one name per cluster to keep return correlation low (V1 p.248).
^ex-01-06-7

### Example 8: Deep neural networks for style-drift detection (V1 p.253)

Setting: PEPF pays over A$400 million in fees to nearly 100 external managers and suspects style drift; Monroe proposes a DNN that compares real-time trading data with known styles.

Q1: define a DNN.
A neural network with many hidden layers, at least 2 but often more than 20, suited to complex non-linear tasks with interacting features, especially pattern recognition (V1 p.252, p.253).

Q2: is a DNN applicable?
Yes: detecting drift patterns in the daily trading of about 100 managers across many markets means processing huge amounts of complicated data, exactly the DNN use case (V1 p.254).

Q3: the three layer groups.
Input layer: one node per feature dimension.
Hidden layers: nodes with a summation operator and an activation function connected by links, where the model is learned.
Output layer: one node per style category producing probabilities that sum to one, for example (0.7, 0.2, 0.1) for three styles, with the observation assigned to the highest, Style I (V1 p.254).
Check: $0.7 + 0.2 + 0.1 = 1.0$.
^ex-01-06-8

### Example 9: Deep learning-based fundamental factor model, refined (V1 p.261)

Setting: Jane Hinton adds four fundamental factors and 11 sector dummies to the six-factor DNN and expands the universe from 218 to 420 stocks.

Q1: input changes.
Features become $6 + 4 + 11 = 21$, so the input layer has 21 neurons; the output layer is unchanged (V1 p.261).
Collinearity from dummies or high feature correlation, a problem for linear regression, is not an issue for a DNN (V1 p.261).

Q2: dataset sizes.
420 stocks for each of 101 periods, each with 21 loadings and a monthly return; under time-series cross-validation the current test set becomes the next training set (V1 p.261).
Per period the training set therefore holds 420 observations against 218 before.

Q3: architecture and hyperparameter changes.
Re-tune the LASSO regularisation hyperparameter by time-series cross-validation, or first increase the neurons per hidden layer and then cross-validate to find the bias-variance optimum (V1 p.261).

Q4: evaluating portfolio performance.
Forecast out-of-sample monthly returns from loadings not in the training set, rank and select the top predicted names, record the realised portfolio return, roll forward one month and repeat across all periods, then compute the information ratio from the mean and standard deviation of monthly portfolio excess returns (V1 p.261).
^ex-01-06-9

### Example 10: Summing up the major types of machine learning (V1 p.262)

Q1: classification problems involve all except continuous targets, answer B; binary and categorical targets define classification (V1 p.262).
Q2: penalized regression is a category of general linear models used when the number of features and overfitting are concerns, answer C; it is related to multiple regression and the penalty is added to the sum of squared residuals, not to the predicted target (V1 p.262).
Q3: CART is a supervised algorithm that accounts for non-linear relationships among features, answer C; it is not unsupervised and not a clustering algorithm (V1 p.262).
Q4: a neural network is based on layers of nodes connected by links when relationships are usually non-linear, answer B; it is not exactly modelled on the nervous system and is not a tree structure (V1 p.262).
Q5: hierarchical clustering is unsupervised grouping, answer A; a pre-specified k describes k-means and predetermined labels describe classification (V1 p.263).
Q6: dimension reduction reduces features while retaining as much variation as possible, answer C (V1 p.263).
^ex-01-06-10

### Case study A: Classification of winning and losing funds (V1 p.224)

Data: 1,594 ETFs and 6,085 MFs, $1{,}594 + 6{,}085 = 7{,}679$ rows by 22 columns (21 features plus the label) as of 15 February 2019 (V1 p.226).
Labels: +1 if the one-month return is at least one standard deviation above the mean of its fund type, -1 if at least one below, 0 otherwise, so most funds are 0 (V1 p.225, p.226).
Design: a typical split is 70% train, 15% validate, 15% test; here no tuning is done, so 70% trains and 30% tests, the same rows for every algorithm (V1 p.226).
For the ETF set that is about $0.7 \times 1{,}594 = 1{,}116$ training rows and 478 test rows; for MFs about 4,260 and 1,826.
Settings: CART max depth 5; SVM cost parameter 1.0 (a large cost forces a thin margin, a small one widens it); KNN k = 4; random forest 100 trees, depth 20 (V1 p.226).
Results, ETF: accuracy CART 0.770, SVM 0.774, KNN 0.724, RF 0.812; F1 CART 0.769, SVM 0.693, KNN 0.683, RF 0.770, so RF is most accurate but on F1 it ties with CART (V1 p.227).
Results, MF: accuracy CART 0.959, SVM 0.859, KNN 0.856, RF 0.969; F1 CART 0.959, SVM 0.847, KNN 0.855, RF 0.969, so RF dominates on both (V1 p.227).
The MF set is about four times larger, which explains the better scores; SVM and KNN are dominated by CART and RF, and RF is known to be more robust to noise (V1 p.227).
Feature importance by information gain: P/S about 0.08 to 0.09 and P/E about 0.06 to 0.07 in both; category size is by far the top MF feature (about 0.20) but minor for ETFs (about 0.04); net assets matters for ETFs (0.065) but is last for MFs (0.01) (V1 p.228, p.229).
^ex-01-06-11

### Case study B: Clustering stocks by co-movement similarity (V1 p.243)

Data: 501 daily adjusted closes for eight S&P 500 stocks, 30 May 2017 to 24 May 2019, giving 500 daily log returns per stock; the Investment Committee wants three buys with low mutual correlation (V1 p.243, p.244).
Steps: compute pairwise Euclidean distances between return vectors into an 8 by 8 matrix with zero diagonal; merge the closest pair; recompute distances to the new cluster by average linkage; repeat to one cluster; cut the dendrogram at three clusters (V1 p.244).
Merge sequence from Exhibit 25: JPM and GS at 0.215; UBS joins at $(0.243 + 0.281)/2 = 0.262$; AAPL and GOOG at 0.307; F and GM at 0.334; banks with AAPL_GOOG at $(0.364 + 0.380 + 0.375 + 0.332 + 0.338 + 0.345)/6 = 0.356$ (V1 p.245, p.246).
Recomputation: $2.134/6 = 0.3557$, rounds to 0.356 as printed.
Three clusters: the five-stock bank and tech cluster, F_GM, and FB alone; FB behaves unlike the other technology stocks, and AAPL and GOOG co-move more with banks than with autos (V1 p.246).
Comparison: k-means with k = 3 splits exactly by sector (banks, autos, tech including FB); agglomerative and divisive both isolate FB; all three agree that banks belong together; k-means results are not expected to match hierarchical ones (V1 p.247).
Recommendation: buy FB, the most attractive auto, and the most attractive bank (V1 p.247).
^ex-01-06-12

### Case study C: Deep neural network-based equity factor model (V1 p.254)

Data: 218 S&P 500 stocks after removing missing loadings, 101 monthly periods June 2010 to November 2018, six fundamental factors (enterprise value, EV/EBITDA, P/S, P/E, P/B, log market cap), target next-month return (V1 p.255, p.256).
Design: walk-forward optimisation, training on period t and testing on t + 1, then t + 1 trains and t + 2 tests, through training on period 100 and testing on 101 (V1 p.256).
Architecture: six input nodes, two hidden layers of 50 neurons each (deliberately over-specified so bias is low and variance high), one output; 50 nodes per layer stays below the 218 training observations; LASSO shrinks the weights (V1 p.257).
Results: out-of-sample MSE exceeds in-sample MSE but the gap narrows over the 101 months (V1 p.257).
First iteration: more L1 regularisation raises in-sample MSE (more bias) and lowers out-of-sample MSE (less variance); at the tested maximum of 0.10 the gap is $0.01025 - 0.0052 = 0.00505$, printed as roughly 0.0051, and the slopes say the optimum is above 0.10; the hyperparameter is typically between 0.001 and 1.0 and is not interpretable as a count of eliminated weights (V1 p.258).
Back-test: in-sample IRs of 0.6974, 0.6748, 0.6532, 0.6229 for 10, 15, 20, 25 stocks; out-of-sample 0.2600, 0.3108, 0.3078, 0.3149, before costs; good MSE does not guarantee a good selection strategy because the network predicts the mean return, not the distribution (V1 p.259, p.260).
^ex-01-06-13

## Item-set patterns

> [!warning] Trap 1: the target decides regression vs classification, not the algorithm name
> Vignette: "predict next quarter's return for each stock", then a distractor offers "classification" because the output is later used to rank into groups.
> Correct approach: a continuous target means regression; a categorical or ordinal target (acquired or not, rating bucket) means classification; no target at all means clustering (V1 p.200, p.273).
> Distractors: classification tempts when the vignette mentions "identify the 20 worst"; clustering tempts when it mentions groups; ordinal tempts for any binary label, but 0/1 has no ranking.

> [!warning] Trap 2: good in-sample, bad out-of-sample is variance, not bias
> Vignette: the model classifies training data well but fails on new data.
> Correct approach: overfitting equals high variance error; underfitting equals high bias error with poor in-sample fit too (V1 p.205, p.208).
> Distractors: "overfitting and bias error" mixes the two; "add more training data" is tempting but the learning curve for a high-bias model shows more data does not reach the desired accuracy (V1 p.205).

> [!warning] Trap 3: the sign of the penalty
> Vignette: a remedy "incorporates a penalty that decreases in size with the number of features".
> Correct approach: the penalty increases with included features so that a feature must earn its place; k-fold cross-validation is the other legitimate remedy (V1 p.207, p.209).
> Distractors: the reversed penalty reads plausibly at speed; "use an unsupervised model" tempts because it "avoids labels", but labeled classification needs supervision.

> [!warning] Trap 4: LASSO with lambda equal to zero is just OLS
> Vignette: "assuming regularisation is used, which model is least appropriate", listing LASSO with lambda 0, LASSO with lambda 0.5 to 1, and a pruned regression tree.
> Correct approach: lambda 0 removes the penalty entirely, so there is no regularisation (V1 p.210, p.273).
> Distractors: the pruned tree is regularised (pruning cuts weak branches); the large lambda is heavy regularisation, still regularisation; candidates pick the "extreme" lambda instead of the zero one.

> [!warning] Trap 5: k-fold on time series
> Vignette: monthly return data are shuffled into k folds.
> Correct approach: k-fold cannot be used with time-series data because only the most recent data can validate; use walk-forward (time-series) cross-validation (V1 p.207, p.256).
> Distractors: "k of 5 or 10 is standard" is true but irrelevant; "increase k" does not fix the ordering problem.

> [!warning] Trap 6: k-means vs hierarchical when the number of groups is unknown
> Vignette: an analyst wants to find natural groupings but does not know how many exist.
> Correct approach: hierarchical clustering produces every granularity and needs no k; k-means requires k in advance (V1 p.238, p.243).
> Distractors: "k-means is faster" is true and tempts as a reason to prefer it; "PCA" tempts because it is also unsupervised, but it reduces features, it does not group observations (V1 p.273).

> [!warning] Trap 7: what must be specified before clustering
> Vignette: "only the distance measure and k need to be specified".
> Correct approach: the feature set defining similarity must be specified for any clustering algorithm, plus the distance measure, plus k only for k-means (V1 p.236, p.243).
> Distractors: "other hyperparameters must be specified" sounds cautious but hierarchical clustering has no k; "correct" tempts because both named items are genuinely required.

> [!warning] Trap 8: CART advantages over KNN, all three not one
> Vignette: statements that CART needs no initial hyperparameter like k, needs no similarity measure, and gives a visual explanation.
> Correct approach: all three are true advantages (V1 p.217, p.218, p.273).
> Distractors: "Statement 3 only" tempts because CART does have regularisation hyperparameters such as max depth, but the statement is about an initial k-like hyperparameter that the algorithm cannot run without; KNN cannot run without k or a distance metric (V1 p.213, p.214).

> [!warning] Trap 9: ensemble beats swapping single models
> Vignette: a CART is in place; the next step is offered as "discard CART for SVM", "discard CART for KNN", or "combine CART with logistic, SVM and KNN".
> Correct approach: ensemble learning averages noise across models and typically beats the best single model (V1 p.219, p.274).
> Distractors: the fund case shows SVM and KNN dominated by CART and RF, so swapping to either is a downgrade (V1 p.227).

> [!warning] Trap 10: deep means at least two hidden layers, and dimmer switch vs summation
> Vignette: "NNs must have at least 10 hidden layers to be deep"; "the activation function sums weighted inputs".
> Correct approach: deep is at least 2, often more than 20; the summation operator forms total net input and the activation function then scales it like a dimmer (V1 p.250, p.252, p.274).
> Distractors: swapping the roles of the two node parts; quoting the "more than 20" figure as a minimum.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM06-Machine-Learning-Practice-Problems]]

## Cross-links

- [[LM01-Basics-of-Multiple-Regression-and-Underlying-Assumptions]]: multiple regression is the supervised-learning baseline here; Exhibit 1 translates dependent variable to target and independent variables to features, and the OLS sum of squared residuals is what LASSO penalises (V1 p.200, p.210).
- [[LM04-Extensions-of-Multiple-Regression]]: logistic regression appears in Exhibit 2 as the classifier the candidate already knows, and multicollinearity among features is the problem PCA and LASSO are built to handle (V1 p.202, p.232).
- [[LM05-Time-Series-Analysis]]: the prohibition on k-fold cross-validation for time series and the walk-forward alternative in the DNN case both rest on the ordering of time-series observations (V1 p.207, p.256).
- [[LM07-Big-Data-Projects]]: takes the concepts here into a full workflow, gives the explicit F1 formula and confusion-matrix metrics, and reuses the training, validation and test partition (V1 p.226, p.227).
- [[LM06-Backtesting-and-Simulation]]: the walk-forward information-ratio back-test of the DNN stock picks is the rolling-window approach that module formalises (V1 p.259, p.260).

## Self-test

Vignette A (Q1 to Q4): Meera Iyer, a quant at Sundaram Capital, builds a model to predict one-year default (yes or no) for 3,200 mid-market borrowers using 40 standardised financial ratios, many highly correlated.
Her first LASSO model with lambda = 0.8 keeps 9 features and gives training error 6% and validation error 7%.
Her second model, a CART grown without any depth limit, gives training error 0% and validation error 14%.
A colleague proposes shuffling the borrowers into 10 folds for cross-validation, and separately proposes PCA on the 40 ratios before fitting.
Iyer also runs a KNN with k = 4 and reports that several borrowers receive no clear classification.

> [!question] Q1
> The second model is most likely suffering from:
> A. high bias error, and adding more borrowers will fix it.
> B. high variance error, and regularising the tree (maximum depth or pruning) is an appropriate fix.
> C. high base error, which cross-validation removes.

> [!question] Q2
> The colleague's 10-fold proposal is:
> A. inappropriate because k must be 5.
> B. appropriate because the data are cross-sectional, so each borrower is used in training 9 times and in validation once.
> C. inappropriate because k-fold cross-validation can only be used with time-series data.

> [!question] Q3
> Iyer's first model is best described as performing:
> A. dimension reduction, because it reduced 40 features to 9 uncorrelated composites.
> B. feature selection, because the L1 penalty set 31 coefficients to exactly zero.
> C. clustering, because it grouped correlated ratios.

> [!question] Q4
> The KNN result with several unclassified borrowers is most likely because:
> A. k is even, allowing 2 to 2 ties among the nearest neighbours.
> B. KNN cannot be used for binary targets.
> C. the distance measure was Euclidean rather than correlation.

Vignette B (Q5 to Q7): Tomas Weil manages a European equity fund and wants to understand its hidden structure.
He has 600 holdings, each described by 12 operating and financial measures, and no view on how many natural groups exist.
After a first pass he decides he wants exactly 8 groups because the risk report has 8 slots.
He then wants a two-dimensional chart of all 600 holdings that preserves as much of the variation in the 12 measures as possible, and reads a scree plot showing eigenvalue shares of 38%, 27%, 12%, 8%, 5% and smaller.

> [!question] Q5
> For the first pass, the most appropriate algorithm is:
> A. k-means, because it is faster than hierarchical clustering on 600 observations.
> B. hierarchical clustering, because no number of clusters must be specified in advance and a dendrogram shows every granularity.
> C. PCA, because it is the unsupervised algorithm for grouping holdings.

> [!question] Q6
> For the 8-group requirement, Weil must specify, at a minimum:
> A. the feature set, the distance measure, and k = 8.
> B. the distance measure and k = 8 only.
> C. k = 8 only, because the features are already chosen by the risk report.

> [!question] Q7
> Using the scree plot, the first two principal components explain closest to:
> A. 38% of total variance, which is below the usual 85% to 95% retention target.
> B. 65% of total variance, which is below the usual 85% to 95% retention target.
> C. 85% of total variance, which meets the usual retention target.

Vignette C (Q8 to Q10): Lena Okafor trains a neural network to forecast next-month stock returns from six factor loadings on 218 stocks over 101 months.
The network has 6 input nodes, two hidden layers of 50 ReLU nodes, and 1 output node, and a LASSO penalty on the weights.
Raising the L1 hyperparameter from 0.02 to 0.10 moves in-sample MSE from 0.0044 to 0.0052 and out-of-sample MSE from 0.0128 to 0.01025.
A junior colleague proposes 10-fold cross-validation over the 101 months and calls the network "deep learning because it has more than 20 nodes per layer".

> [!question] Q8
> The effect of raising the L1 hyperparameter is best described as:
> A. more bias and less variance, which is the intended direction while out-of-sample MSE keeps falling.
> B. less bias and more variance, since in-sample error rose.
> C. no change in the bias-variance trade-off, since the hyperparameter is not interpretable.

> [!question] Q9
> The colleague's two claims are:
> A. both correct.
> B. both incorrect: k-fold cannot be used on time-ordered months, and "deep" refers to at least 2 hidden layers, not nodes per layer.
> C. the first incorrect and the second correct.

> [!question] Q10
> At a hidden node receiving inputs 0.5, -1.2 and 0.9 with weights 0.4, 0.5 and -0.3, the ReLU output is closest to:
> A. -0.67.
> B. 0.
> C. 0.67.

> [!success]- Answer key
> Q1: B. Zero training error with 14% validation error is the overfitting signature, which is variance error; an unconstrained CART memorises the training data and is regularised by max depth, min node population or pruning (V1 p.205, p.217). A is wrong because high bias shows poor in-sample fit and more data does not reach the desired accuracy. C is wrong because base error is irreducible randomness.
> Q2: B. Borrowers are cross-sectional, so random shuffling into k folds is valid; with k = 10 each observation trains 9 times and validates once (V1 p.207). A is wrong because k is typically 5 or 10, not fixed at 5. C reverses the rule: k-fold cannot be used with time series.
> Q3: B. LASSO's absolute-value penalty drives unimportant coefficients to zero and so performs feature selection automatically (V1 p.210). A is wrong because the 9 survivors are original ratios, not uncorrelated composites, which is what PCA produces. C is wrong because clustering groups observations, not features.
> Q4: A. An even k can produce ties with no clear classification; 4 neighbours can split 2 to 2 (V1 p.214). B is wrong because KNN is most often used for classification including binary. C is wrong because Euclidean distance is the standard choice and does not by itself cause ties.
> Q5: B. With the number of groups unknown, hierarchical clustering sorts without prior input and the dendrogram lets the analyst compare granularities (V1 p.239, p.241, p.243). A is a true fact used as a wrong reason; speed does not solve the unknown-k problem. C is wrong because PCA reduces features, it does not group observations.
> Q6: A. Any clustering run needs the feature set that defines similarity and a distance measure; k-means additionally needs k (V1 p.236, p.243). B omits the feature set, the exact error in Example 6. C omits both.
> Q7: B. $38\% + 27\% = 65\%$; the retention guideline is often 85% to 95%, so two components are not enough, and adding the third and fourth gives $65 + 12 + 8 = 85\%$ (V1 p.234). A counts only PC1. C requires four components, not two.
> Q8: A. More LASSO regularisation reduces non-zero weights, adds bias (in-sample MSE rises) and cuts variance (out-of-sample MSE falls); the case study says the optimum is above 0.10 because out-of-sample MSE is still falling (V1 p.258). B reverses the direction. C confuses interpretability of the hyperparameter's level with its effect.
> Q9: B. K-fold cross-validation cannot be used with time-series data; the case uses walk-forward optimisation instead (V1 p.207, p.256). Deep means at least 2 hidden layers, often more than 20 layers; node count per layer is irrelevant (V1 p.252). Note the network in the vignette is in fact deep because it has two hidden layers, but for the layer reason, not the node reason.
> Q10: B. Total net input $= 0.5(0.4) + (-1.2)(0.5) + 0.9(-0.3) = 0.20 - 0.60 - 0.27 = -0.67$; ReLU gives $\max(0, -0.67) = 0$, so the node does not trigger (V1 p.249, p.250). A is the raw net input without the activation. C drops the sign.

## Flashcards

#flashcards/cfa-l2/01-Quantitative-Methods/lm06

Elementary description of ML in four words::Find the pattern, apply the pattern (V1 p.199)

Supervised learning requires what kind of dataset?::A labeled dataset, matched sets of observed inputs (features) and the associated output (target) (V1 p.199)

ML term for the dependent variable and for the independent variables::Target and features (V1 p.200)

Continuous target means which class of supervised problem?::Regression, even if the technique used is not "regression" (V1 p.200)

Categorical or ordinal target means which class of supervised problem?::Classification, and the model is called a classifier (V1 p.200)

An ordinal variable sits where on the measurement scale?::Between categorical and continuous; it is a ranked category such as a credit rating (V1 p.201)

Two problem types suited to unsupervised learning::Dimension reduction and clustering (V1 p.201)

Definition of overfitting::The algorithm fits the training data too well, incorporating noise, so it does not generalise to new data (V1 p.203)

Three non-overlapping data samples and which are in-sample::Training and validation (in-sample) and test (out-of-sample) (V1 p.204)

Two main contributors to overfitting::High noise levels in the data and too much complexity in the model (V1 p.204)

{{Bias error}} causes underfitting and high in-sample error; {{variance error}} causes overfitting and high out-of-sample error; {{base error}} is randomness in the data (V1 p.205)

Out-of-sample error decomposition::$E_{out}$ = bias error + variance error + base error (V1 p.265)

A learning curve plots what against what?::Accuracy rate (1 minus error rate) in validation or test samples against the number of training samples (V1 p.205)

Learning-curve signature of high bias::Training and validation accuracy converge but below the desired accuracy rate; more data will not help (V1 p.205)

Learning-curve signature of high variance::Training and validation error rates fail to converge (V1 p.205)

A fitting curve plots what against what?::In-sample and out-of-sample error against model complexity; the optimum is where bias and variance curves cross (V1 p.206)

Which functions are more prone to bias and which to variance?::Linear functions to bias and underfitting; non-linear functions to variance and overfitting (V1 p.206)

Two common methods to reduce overfitting::An overfitting penalty that limits complexity (Occam's razor) and cross-validation for proper sampling (V1 p.207)

K-fold cross-validation, in one sentence
?
Shuffle the data (excluding test and fresh data), split into k equal sub-samples, train on k minus 1 and validate on the kth, repeat k times, and average the k validation errors as the estimate of out-of-sample error; k is typically 5 or 10 (V1 p.207)

Limitation of k-fold cross-validation::It cannot be used with time-series data, where only the most recent data can reasonably validate (V1 p.207)

LASSO penalty term::$\lambda \sum_{k=1}^{K} |\hat{b}_k|$ with $\lambda > 0$, added to the sum of squared residuals (V1 p.210)

LASSO with lambda equal to 0 is equivalent to::Ordinary least squares regression, no regularisation (V1 p.210)

When is the LASSO penalty applied?::Only during model building on training data; the finished model is evaluated by squared residuals on the test set (V1 p.210)

Definition of regularisation::Methods that reduce statistical variability in high-dimensional estimation by shrinking coefficient estimates toward zero, reducing complexity (V1 p.210)

Definition of a hyperparameter::A parameter whose value must be set by the researcher before learning begins, tuned on the validation set (V1 p.210)

What does SVM maximise?::The margin, the width of the strip separating the two classes around the discriminant boundary (V1 p.212)

Support vectors are::The observations closest to the boundary that determine the margin; data far from them do not affect the boundary (V1 p.212)

Soft margin classification::Adds a penalty for misclassified training observations so SVM trades a wider margin against a lower error penalty when data are not linearly separable (V1 p.212)

KNN decision rule::Assign the class held by the majority of the k nearest neighbours under the chosen distance measure (V1 p.213)

Why avoid an even k in KNN?::Ties may leave no clear classification (V1 p.214)

Effect of k too small and k too large in KNN::Too small gives a high error rate and sensitivity to local outliers; too large dilutes the concept of nearest neighbours (V1 p.214)

KNN works better with how many features?::A small number; irrelevant or correlated features hurt, so manual feature selection may be needed (V1 p.214)

CART prediction at a terminal node for classification and for regression::Majority category for classification; mean of the labeled values for regression (V1 p.217)

CART split rule at each node::Choose the feature and cutoff value that generate the widest separation of the labeled data, minimising classification error (V1 p.217)

Regularisation parameters for CART::Maximum tree depth, minimum population at a node, maximum number of decision nodes, or pruning afterwards (V1 p.217)

Main advantage of CART over black-box models::The tree gives a visual explanation for the prediction, useful for expert systems and client communication (V1 p.218)

Two categories of ensemble learning::Heterogeneous learners (different algorithms with a voting classifier) and homogeneous learners (same algorithm on bagged training sets) (V1 p.219)

Bagging in one sentence::Generate n new training sets by random sampling with replacement from the original, train n models, and aggregate by majority vote (classification) or average (regression) (V1 p.219)

Random forest definition::A collection of many decision trees trained by bagging, often with a random subset of m of n features considered at each split (V1 p.219)

Random forest hyperparameters::Number of features per split m, number of trees, minimum node size, maximum tree depth (V1 p.219)

Main drawback of random forest::Loses the interpretability of a single tree; relatively black box (V1 p.220)

Fraud case metrics: precision 89% means what and recall 82% means what?::89% of predicted frauds were frauds; 82% of actual frauds were caught (V1 p.221)

When is F1 preferred to accuracy?::When there is class imbalance, as when most funds are labeled 0 (V1 p.227)

PCA eigenvector and eigenvalue meanings::Eigenvector defines an uncorrelated composite variable (a direction); its eigenvalue gives the proportion of total variance that eigenvector explains (V1 p.232)

How PCA finds PC1::The line minimising the sum of projection errors and maximising the spread of the data; PC2 is at right angles, hence uncorrelated (V1 p.233)

Scree plot and the retention rule::Plots variance explained per component; keep the fewest components reaching the desired share, often 85% to 95% (V1 p.234)

Main drawback of PCA::Principal components are combinations of features and cannot be easily labeled or interpreted, a black box (V1 p.235)

Cohesion and separation in clustering::Cohesion is closeness within a cluster; separation is distance between clusters (V1 p.236)

Distance measure closely related to Euclidean and useful for diversification::Correlation, the average Euclidean distance between standardised points (V1 p.236)

K-means iteration in one line::Assign each observation to the nearest centroid, recompute centroids as member averages, repeat until no observation is reassigned (V1 p.237)

Two limitations of k-means::Result can depend on initial centroids (rerun with different starts) and k must be chosen before running (V1 p.238)

Agglomerative vs divisive hierarchical clustering::Agglomerative is bottom-up, each observation starts alone and the closest pair merges; divisive is top-down, one cluster is split repeatedly (V1 p.239, p.240)

Which hierarchical method suits large datasets and small clusters, and which suits large clusters?::Agglomerative for large datasets and small clusters (fast, local); divisive for large clusters (global structure) (V1 p.240)

Dendrogram arch height represents::The distance between the two clusters being merged; shorter dendrites mean greater similarity (V1 p.241)

30-second micro-problem: distance from UBS to cluster GS_JPM given d(UBS, JPM) = 0.243 and d(UBS, GS) = 0.281::(0.243 + 0.281)/2 = 0.262 by average linkage (V1 p.246)

30-second micro-problem: terminal node value [13, 4, 4], probability of the predicted class::13/21 = 0.619, about 62%, with 19% each for the other two classes (V1 p.230)

The two functional parts of a hidden node::A summation operator (weighted sum into total net input) and an activation function (non-linear dimmer switch) (V1 p.250)

ReLU function and sigmoid range::$f(x) = \max(0, x)$; sigmoid outputs between 0 and 1 (V1 p.249, p.250)

Weight update rule in training a neural network::New weight = old weight minus learning rate times the partial derivative of total error with respect to the old weight (V1 p.251)

Neural network hyperparameters named in the module::Number of input, hidden and output nodes (structure), the activation function, and the learning rate (V1 p.249, p.250, p.251)

Definition of a deep neural network::A neural network with many hidden layers, at least 2 but potentially more than 20 (V1 p.252)

Reinforcement learning framework::An agent performs actions in an environment to maximise reward over time, with no labeled data and no instantaneous feedback, learning by trial and error (V1 p.253)

Flowchart: many highly correlated features, first step::Dimension reduction with PCA (V1 p.264)

Flowchart: numerical prediction with linear data vs non-linear data::Penalized regression/LASSO for linear; CART, random forest or neural nets for non-linear (V1 p.264)

Flowchart: labeled classification with linear data vs non-linear data::KNN or SVM for linear; CART, random forest or neural nets for non-linear (V1 p.264)

Flowchart: unlabeled linear data, categories known vs unknown::K-means if the number of categories is known; hierarchical clustering if unknown (V1 p.264)

Which answer is the trap: "a penalty that decreases with the number of features" and why::It reverses the LASSO penalty, which must increase with included features so each must earn its place (V1 p.209, p.210)

## Common mistakes

1. Calling a problem classification because the predictions are later ranked or bucketed; the target's type at training time decides, and a continuous return is regression (V1 p.200, p.273).
2. Pairing overfitting with bias error; overfitting is variance error, underfitting is bias error (V1 p.205).
3. Believing more training data cures a high-bias model; the learning curve converges below the desired accuracy regardless of sample size (V1 p.205).
4. Writing the LASSO penalty as decreasing in the number of features, or forgetting that lambda equal to zero is plain OLS (V1 p.209, p.210).
5. Applying k-fold cross-validation to time-series data instead of walk-forward validation (V1 p.207, p.256).
6. Treating PCA as a clustering method; it reduces features to uncorrelated composites, it does not group observations (V1 p.232, p.273).
7. Choosing k-means when the number of groups is unknown, or citing k-means speed as the reason to prefer hierarchical clustering (V1 p.238, p.243).
8. Forgetting that the feature set defining similarity must be specified for every clustering algorithm, not just the distance measure and k (V1 p.243).
9. Claiming CART has no advantage over KNN beyond interpretability; CART also needs no initial k and no distance measure (V1 p.273).
10. Swapping the summation operator and the activation function, or setting the deep-learning threshold at 10 layers instead of at least 2 (V1 p.250, p.252, p.274).
11. Assuming random forest is as interpretable as a single tree; it is relatively black box, which is the price of lower variance (V1 p.220).
12. Judging a classifier on accuracy alone under class imbalance instead of F1, and forgetting that 1/3 is the useless-model baseline with three balanced classes (V1 p.227).
13. Reading a good out-of-sample MSE as proof of a profitable stock-selection strategy; the network predicts mean returns, not the distribution, and out-of-sample IRs were less than half the in-sample ones (V1 p.259, p.260).
14. Using an even k in KNN and then being surprised by ties (V1 p.214).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "01-06" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
