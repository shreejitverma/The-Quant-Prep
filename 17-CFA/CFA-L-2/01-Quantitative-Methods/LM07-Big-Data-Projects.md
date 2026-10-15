---
type: cfa-lm
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
volume: 1
lm: 7
title: "Big Data Projects"
pages: "275-372"
weight_band: "5-10%"
difficulty: 3
los_count: 7
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/quantitative-methods]
---

# LM7: Big Data Projects

Difficulty 3 of 5: the arithmetic is four ratios from a 2 by 2 table, but the module is a long ordered checklist (five steps, six error types, five transformations, four cleansing operations, four normalization operations, three exploration tasks, three training tasks, three evaluation techniques) and the exam tests it by asking which step, which error, which metric, or which fix, so one swapped label costs the question.

## LOS map

- **identify** and explain steps in a data analysis project (V1 p.277) ^los-01-07-a
    - Examiner asks: given a description of an activity (scraping web pages, resolving missing values, drawing a word cloud, choosing a p-threshold), name the step it belongs to in the structured pipeline (conceptualization, collection, preparation and wrangling, exploration, training) or the text pipeline (problem formulation, curation, preparation and wrangling, exploration, training), and order the steps correctly.
- **describe** objectives, steps, and examples of preparing and wrangling data (V1 p.281) ^los-01-07-b
    - Examiner asks: read a raw data table and classify each defect as incompleteness, invalidity, inaccuracy, inconsistency, non-uniformity, or duplication, then classify a transformation as extraction, aggregation, filtration, selection, or conversion, and compute a normalized or standardized value.
- **evaluate** the fit of a machine learning algorithm (V1 p.281) ^los-01-07-c
    - Examiner asks: from training and cross-validation error or AUC figures, decide whether the model underfits (high bias, both errors large) or overfits (high variance, CV error much larger than training error) and pick the fix (regularization, fewer features, more data, or feature engineering).
- **describe** objectives, methods, and examples of data exploration (V1 p.295) ^los-01-07-d
    - Examiner asks: distinguish exploratory data analysis, feature selection, and feature engineering; match a visualization (histogram, box plot, scatterplot, word cloud) to its data type; identify chi-square, mutual information, and frequency measures as feature selection tools.
- **describe** methods for extracting, selecting and engineering features from textual data (V1 p.301) ^los-01-07-e
    - Examiner asks: identify which tokens to drop (very high and very low term frequency), compute TF at the collection and sentence level, DF, IDF and TF-IDF, and recognise number tokens, n-grams, name entity recognition and parts of speech as text feature engineering.
- **describe** objectives, steps, and techniques in model training (V1 p.308) ^los-01-07-f
    - Examiner asks: name the three training tasks (method selection, performance evaluation, tuning), compute precision, recall, accuracy and F1 from a confusion matrix, read ROC and AUC, state the 60:20:20 split, fix class imbalance by undersampling the majority or oversampling the minority, and place bias and variance under tuning rather than performance evaluation.
- **describe** preparing, wrangling, and exploring text-based data for financial forecasting (V1 p.318) ^los-01-07-g
    - Examiner asks: follow the Financial Phrase Bank sentiment case, reproduce a term frequency measures table entry, explain why stop words were kept at normalization and removed later by custom frequency cut-offs, and interpret the before and after regularization AUCs and the threshold p-value selection.

## Core intuition

> [!abstract] The whole module in one sentence
> A big data project is a pipeline that turns raw, often unstructured, data into a clean structured matrix, learns a pattern from part of it, and proves the pattern generalises by scoring it on data it never saw; every step exists to remove a specific way that pipeline can lie to you (V1 p.278, p.309).

### Why big data needs its own module

Big data, also called alternative data, is data from markets, businesses, governments, individuals, sensors and the Internet of Things, and the explosion of the last decade has been mostly unstructured: posts, tweets, emails, web traffic, news, images (V1 p.275).
Investment managers want the information edge embedded in it, for example a fund manager using 10-K text to forecast stock sentiment as an input to a broader model that includes corporate financials (V1 p.276).
Structured data are numbers and values that drop straight into a data table; unstructured data need specific preparation before a machine can read them, so the practitioner must understand how unstructured data become structured inputs to machine learning (V1 p.276).
The curriculum characterises big data by the 3Vs: volume (quantity, now petabytes and exabytes, with a megabyte a tablespoon of sand, a petabyte a 1.6 kilometre beach and an exabyte a 1,600 kilometre beach), variety (structured, semi-structured and unstructured sources, with legal and ethical privacy issues), and velocity (speed of creation, over a billion tweets every three days, five billion searches a day, "data-in-motion" versus "data-at-rest") (V1 p.276, p.277).
For inference and prediction there is a fourth V, veracity, the credibility and reliability of the source; social media is plagued with spam, by some estimates 10% to 15% of it completely fake, and web spam is over 20% of all web content (V1 p.277).
The module focuses on variety and veracity as they show up in text (V1 p.278).
Textual big data supplies topics (what people talk about) and sentiment (how they feel about it); one US study found positive Twitter sentiment predicted the Dow Jones trend up to three days ahead with nearly 87% accuracy (V1 p.277).

### The two pipelines, and why the first four steps differ

> [!abstract] Two five-step pipelines that share only the last step
> Structured: conceptualization, data collection, data preparation and wrangling, data exploration, model training (V1 p.278).
> Text: text problem formulation, data (text) curation, text preparation and wrangling, text exploration, model training (V1 p.278, p.279).
> Both are iterative, and the insights from one pass may send you back to reconceptualization (V1 p.278).

Conceptualization decides what the output is (will the stock rise one week ahead), who uses it, and how it embeds in business processes; it is a blueprint on a drawing board, a modifiable plan that also fixes whether the model is supervised or unsupervised and where the data will come from (V1 p.278, p.281).
Data collection for structured projects usually pulls numeric data already in tabular form, columns of features and rows of instances; the practical advice is to clarify the database schema with an administrator before downloading, read the Readme files that accompany raw files, and weigh internal data against vendor data delivered by API or csv (V1 p.278, p.281).
Vendor data save preparation time but cost money, may be unsuited to projects about your own users, and their cleansing may have masked or destroyed the underlying trends where alpha lives, so buying a dataset can mean buying away your edge (V1 p.281, p.282).
Data preparation and wrangling is cleansing (resolving missing and out-of-range values) plus preprocessing (extracting, aggregating, filtering, selecting columns); it is the foundation, consumes most of the project time, and needs domain specialists (V1 p.278, p.281).
Data exploration is exploratory data analysis, feature selection and feature engineering (V1 p.278).
Model training is method selection, performance evaluation and tuning (V1 p.278, p.308).

The text pipeline differs because text is unstructured and the goal is to produce structured output, typically a class or a score, from unstructured input (V1 p.278).
Text problem formulation fixes the exact inputs and outputs, for example a sentiment score from text, and how the classification will be used (V1 p.278).
Text curation gathers external text through web services or web spidering (scraping, crawling) programs that extract raw content from web pages, and may require experts to annotate reliable target labels such as bullish or bearish for supervised learning (V1 p.278).
Text preparation and wrangling is the cleansing and preprocessing that converts a character stream into a matrix that traditional models can consume (V1 p.279).
Text exploration is text visualization such as word clouds plus text feature selection and engineering (V1 p.279).
The classifier's structured output can then be combined with other structured variables or used directly for forecasting (V1 p.279).

### Structured data cleansing: six errors, each with its own tell

Data cleansing examines, identifies and mitigates errors in raw data; manual entry gives incomplete, duplicated, erroneous or inaccurate values and automated systems give similar problems from server failures and bugs (V1 p.282).
The six error types are the most exam-tested list in the module, and Exhibit 3, a US bank's customer table, gives one example of each (V1 p.283).

| Error | Definition | Exhibit 3 example | Fix |
|---|---|---|---|
| Incompleteness | Data not present, missing values | Missing gender, salary, other income, salutation, state in rows for IDs 3 to 6 | Alternate sources; omit or mark NA, impute mean, median, mode or zero at exploration (V1 p.283) |
| Invalidity | Outside a meaningful range | Date of birth 1/1/1900, beyond a human lifespan | Verify other administrative records (V1 p.283) |
| Inaccuracy | Not a measure of the true value | Credit card "Don't Know"; everyone has one or does not | Business records and administrators (V1 p.283) |
| Inconsistency | Conflicts with corresponding data points or reality | Name "Ms. XYZ" with gender M | Clarify with another source (V1 p.283) |
| Non-uniformity | Not in an identical format | Dates as 12/5/1970 and 15 Jan, 1975; ambiguous dollar symbol | Convert to a standard format (V1 p.283) |
| Duplication | Same observation twice | Row 6 repeats row 3's name and date of birth | Remove the duplicate (V1 p.283) |

The distinction that trips candidates: invalidity is out of range (a negative income), inaccuracy is a plausible value that is not the truth (an "unknown" loan amount the lender must know), inconsistency is a contradiction between two fields (interest expense with zero debt), non-uniformity is a formatting mismatch (V1 p.283, p.287, p.354).
Cleansing is expensive because it combines automated rule-based tools with manual row by row, column by column inspection, and metadata from software such as SPSS is the starting point (V1 p.284).
The business value of the project sets the required data quality; if errors cannot be resolved, dropping about 100 rows from a dataset of more than 10,000 may not matter, but in a dataset under 1,000 rows every row may count (V1 p.284).

### Structured data preprocessing: five transformations, outliers, and scaling

Preprocessing transforms and scales the cleansed data (V1 p.284).

| Transformation | Meaning | Exhibit 4 example |
|---|---|---|
| Extraction | New variable from an existing one | Age from date of birth; a ratio of two columns (V1 p.284, p.288) |
| Aggregation | Two or more variables into one | Salary plus other income into total income (V1 p.284) |
| Filtration | Remove rows not needed | Drop the British Columbia customer from a US bank dataset (V1 p.284) |
| Selection | Remove columns not needed | Drop name and date of birth once ID and age exist (V1 p.284, p.285) |
| Conversion | Set correct types, strip prefixes and suffixes, convert currency, time zones | Nominal name, continuous salary, categorical gender and credit card; CAD to USD (V1 p.285) |

Selection of columns during preprocessing must not be confused with feature selection during exploration; preprocessing needs only basic intuition and a word with the data administrator, feature selection needs statistics and a full EDA (V1 p.284, p.299).
Outliers must be identified with domain knowledge, then removed or replaced by imputed values (V1 p.285).
In normal data, a value more than 3 standard deviations from the mean may be an outlier; for any distribution the interquartile range, IQR equal to the 75th minus the 25th percentile, flags values above the third quartile plus 1.5 IQR or below the first quartile minus 1.5 IQR, and a multiple of 3.0 marks extreme values (V1 p.285).
Removing outliers is trimming or truncation (a 5% trimmed dataset drops the top 5% and bottom 5%); replacing them with the largest and smallest non-outlier values is winsorization (V1 p.285).
Note the Exhibit 5 subtlety: a salary of zero was an outlier, but after aggregation into total income of 55,000 it no longer is, so the order of operations changes what counts as an outlier (V1 p.285).

Scaling shifts and rescales a feature so that features with very different ranges, such as age and income, form a homogeneous training set; SVMs and neural networks need it, and outliers must be removed first (V1 p.285, p.286).
Normalization maps a variable into [0, 1] using its minimum and maximum, is sensitive to outliers, and can be used when the distribution is unknown (V1 p.286).
Standardization centres by the mean and divides by the standard deviation to give mean 0 and standard deviation 1, is less sensitive to outliers, but assumes the data are normally distributed (V1 p.286).

### Text cleansing and text wrangling

Unstructured data are about 80% of all data and come as text, images, video and audio; text processing is the cleansing and transformation of text into a structured format (V1 p.288).
Raw web text carries html tags, punctuation and white space that human readers never see, as the Robots Are Us example shows (V1 p.288, p.289).
Regular expressions (regex) search for character patterns, for example `<.*?>` finds every html tag, and GREP applies them; html parsers exist in R and Python (V1 p.289).

The four cleansing operations, in order (V1 p.289, p.290):
1. Remove html tags, though some generic tags may be kept for formatting meaning.
2. Remove punctuation, but substitute annotations such as /percentSign/, /dollarSign/ and /questionMark/ for punctuation that carries meaning, replace sentence-ending periods with /endSentence/, drop periods after abbreviations, and keep hyphens and underscores that bind words such as e-mail.
3. Remove numbers or replace them with /number/, because the value of a number rarely helps classification and each distinct number would otherwise become its own word; the exception is information extraction, where the numbers themselves are the output.
4. Remove extra white space, tabs and leading and trailing spaces, which the earlier operations often create.

Sequence matters: after punctuation removal "1.2 million" becomes "12 million", harmless only because a later step replaces all numbers with /number/ (V1 p.290).

Text wrangling starts with tokenization, the splitting of text into tokens, where a token is equivalent to a word; tokenization can be at character level but is most commonly at word level (V1 p.291).
Normalization then has four operations (V1 p.291):
1. Lowercasing, so "The" and "the" are one word.
2. Stop word removal: "the", "is", "a" carry no semantic meaning for ML training, though advanced applications may need them for context, and custom stop words such as "exhibit" in filings can be added.
3. Stemming, a rule-based conversion of inflected forms to a stem that need not be a real word, "analyzed" and "analyzing" to "analyz", "analysing" to "analys", by Porter's algorithm; simpler and more common in English.
4. Lemmatization, an algorithmic conversion to the morphological root or lemma, "analyze", which is more expensive and needs knowledge of the language.

Stemming and lemmatization both reduce data sparseness, the many unique low-frequency tokens, by folding sparse forms into less sparse stems, which helps train less complex models (V1 p.292).
The normalized tokens form the bag-of-words (BOW), the distinct set of tokens across all texts; it ignores word position and sequence, which makes it memory efficient but blind to context (V1 p.292).
The last preprocessing step builds the document term matrix (DTM): one row per document, one column per BOW token, cells holding counts (or later, TF values); this is the moment unstructured text becomes structured data (V1 p.292).
Exhibit 10 and 11 show four sentences shrinking from a 19-word BOW to 8 stems and then to a 4 by 8 DTM (V1 p.292, p.293).

> [!abstract] The n-gram fix for the "no market" problem
> BOW dropped the stop word "no" and lost the negative meaning of "no market"; n-grams, sequences of n words (unigram, bigram, trigram), keep adjacent words as one token such as "no_market" or "not_good", and are built into the BOW and DTM exactly like unigrams (V1 p.293, p.329).
> Stop words attached inside an n-gram, such as "to_the", survive stop word removal, so normalization interacts with the n-gram choice (V1 p.294).

### Data exploration: EDA, feature selection, feature engineering

Exploration investigates distributions and relationships, and its quality strongly affects training; without domain knowledge it produces spurious relationships (V1 p.295).
EDA uses graphs (histograms, bar charts, box plots, density plots, heat maps, word clouds) and descriptive statistics, and it doubles as the communication medium among business users, domain experts and analysts (V1 p.296).
Its objectives: understand data properties, find patterns and relationships, inspect basic hypotheses, document distributions, plan the modelling strategy (V1 p.296).
For structured data, one-dimensional EDA computes mean, median, quartiles, ranges, standard deviation, skewness and kurtosis and draws histograms (equal bins and frequencies), bar charts (frequencies of categorical variables), box plots (median, quartiles, outliers) and density plots (smoothed histograms) (V1 p.296, p.297).
Multi-dimensional EDA uses correlation matrices, scatterplots, line graphs, stacked bars, and multiple box plots per feature against the target; high-dimensional data can be reduced first with PCA (V1 p.296, p.297).
A visual relationship must be confirmed by a statistical test: parametric ANOVA, t-test and Pearson correlation, or non-parametric chi-square and Spearman rank-order correlation (V1 p.298).

Feature selection keeps only pertinent features; fewer features mean lower complexity and shorter training, and the goal is a parsimonious model with maximum out-of-sample predictive power (V1 p.296, p.299).
Diagnostics should check redundancy, heteroskedasticity and multicollinearity, and univariate scoring methods (chi-square, correlation coefficients, information gain such as R-squared) rank each feature, with automatic forward and backward passes (V1 p.299, p.300).
Dimensionality reduction is a different tool: it creates new uncorrelated combinations of features, whereas feature selection includes or excludes existing features without altering them (V1 p.300).
Feature engineering creates new features by transforming or decomposing existing ones: the log of a product of features, an income_above_100k indicator built from tax-bracket domain knowledge, one hot encoding of a five-level education variable into five 0/1 columns, or second-of-hour and day-of-date fields from a timestamp for trading algorithms (V1 p.300).
Different feature engineering can produce dramatically different results from the same algorithm (V1 p.301).

### Text exploration: which tokens carry the signal

Text applications are text classification (supervised), topic modeling (unsupervised), fraud detection, and sentiment analysis (both) (V1 p.301).
The corpus is the collection of texts, and the basic statistic is term frequency (TF), the number of times a token appears across all texts divided by the total number of tokens (V1 p.301).
In topic modeling the highest-TF words are removed as stop words or common vocabulary; in sentiment analysis and classification the chi-square measure of word association finds words that differ between positive and negative sentences (V1 p.301).
Word clouds show the most informative words by scaling font size to frequency, with colour adding dimensions such as word length (V1 p.301, p.302).

> [!abstract] Noise sits at both ends of the frequency scale
> The most frequent tokens appear in every text, so they strain the model to find any decision boundary: underfitting.
> The rarest tokens appear in a handful of texts, so the model learns to assign those texts to a class on the strength of a name: overfitting.
> Feature selection for text removes both ends and keeps the middle (V1 p.302, p.327, p.331).

Three selection methods are named (V1 p.302, p.303):
1. Frequency measures: prune the vocabulary by dropping tokens with very high and very low TF; document frequency (DF), the share of documents containing the token, discards tokens present in all texts and is the simplest method, working well with many thousands of tokens.
2. Chi-square test: tests independence between token occurrence and class occurrence; tokens with the highest statistic occur more in one class and have higher discriminatory power.
3. Mutual information (MI): 0 if the token is distributed the same across classes, approaching 1 as the token concentrates in one class; Exhibit 18 shows "soccer" at 0.0781 for sports and "election" at 0.0612 for politics.

Text feature engineering techniques (V1 p.303, p.304):
1. Numbers: differentiate /number4/ for years from /number10/ for identification numbers.
2. N-grams: keep discriminative multi-word patterns such as stock_market intact.
3. Name entity recognition (NER): tag tokens with object classes such as ORGANIZATION, DATE, LOCATION, MONEY, TIME, PERCENT, and protect them from lowercasing and stemming.
4. Parts of speech (POS): tag nouns, verbs, adjectives and proper nouns, so "market" the verb (marketing) and "market" the noun (stock trading) are separated and compound nouns such as "CFA Institute" become one token.

### Model training: three tasks and two kinds of failure

Training is systematic, iterative and recursive, with the iteration count set by the problem and the required performance; ML engineers and domain experts must work together (V1 p.308).
Its three tasks are method selection, performance evaluation, and tuning (V1 p.308).
For structured and unstructured data the training process is the same, because by this stage the text has become a data matrix (V1 p.309).
Fitting is the degree to which the model generalises to new data: Exhibit 21's underfit boundary misses four training points, the S-shaped overfit boundary misses none but will fail out of sample, the good fit misses one (V1 p.309).
Fitting errors come mainly from dataset size (small data underfits) and feature count (few features underfit, many features overfit through low degrees of freedom); so feature selection minimises overfitting and feature engineering prevents underfitting (V1 p.310).

Method selection is governed by three factors (V1 p.310, p.311):
1. Supervised or unsupervised: supervised data contain ground truth, the known target; typical supervised methods are regression, ensemble trees, SVM and neural networks (default prediction); unsupervised are dimensionality reduction, clustering and anomaly detection (grouping financial institutions).
2. Type of data: CART for numerical, GLMs and SVMs for text, neural networks and deep learning for images, deep learning for speech.
3. Size of data: SVMs suit "wider" data with 10,000 to 100,000 features and few instances; neural networks suit "longer" data with far more instances than features.

Methods can be stacked: logistic regression classifies sentiment from text, and that classification becomes a feature in a CART that also uses structured financials (V1 p.311).
Before supervised training the master dataset is split into training (about 60%), cross-validation or validation (about 20%) and test (the rest), by random sampling such as the k-fold method; unsupervised learning needs no split because there are no labels (V1 p.311).
Class imbalance, where one class dominates, lets a naive "no one defaults" model score high accuracy while missing every default; the cure is to randomly undersample the majority "0" class or oversample the minority "1" class, with or without replacement, or to synthesise minority observations (V1 p.311).

Performance evaluation for binary classifiers uses three techniques (V1 p.312 to p.315):
1. Error analysis with the confusion matrix: TP, FP (Type I error), FN (Type II error), TN, and from them precision, recall, accuracy and F1.
2. ROC curve, false positive rate on the x-axis against true positive rate on the y-axis across cutoff points, with AUC near 1.0 near-perfect and 0.5 random guessing; more convex is better.
3. RMSE for continuous prediction, mostly regression.

> [!abstract] Precision guards against Type I cost, recall guards against Type II cost, F1 balances them
> Precision is right when a false positive is expensive (scrapping a good product; buying a stock whose sentiment is really negative).
> Recall is right when a false negative is expensive (shipping a defective product; shorting a stock whose sentiment is really positive).
> Accuracy is fine for balanced classes; F1, the harmonic mean, is the overall measure when classes are unequal because it sits close to the smaller of precision and recall (V1 p.313, p.314, p.342).

Tuning reads the errors: high training error means underfitting and bias; CV error far above training error means overfitting and variance; total error is bias plus variance and the trade-off is minimised, not eliminated (V1 p.316).
Parameters are learned from the training data (regression coefficients, network weights, support vectors); hyperparameters are set by hand and are not data-dependent (lambda, activation function, hidden layers, number of trees and depth, k in KNN and k-means, the p-threshold in logistic regression) (V1 p.316).
There is no formula for hyperparameters, so grid search trains the model over combinations of values, cross-validates each, and picks the combination whose training and CV errors are close and small (V1 p.316).
The fitting curve plots training and CV error against a hyperparameter such as lambda: slight regularization gives small training error and large CV error (variance, overfitting), large regularization gives large error on both (bias, underfitting), optimum regularization gives similar and minimal errors (V1 p.317).
If bias or variance persists after tuning, add training instances, or cut features for variance and add features for bias, then retrain; in a model built from sub-models, ceiling analysis finds which sub-model's improvement would lift overall accuracy most (V1 p.318).

### The sentiment case study, step by step

Robo-readers analyse text for sentiment polarity toward a target, and the project asks how well sentiment in English news sentences about NASDAQ OMX Helsinki companies can be classified (V1 p.318).
Curation: the Financial Phrase Bank on Researchgate, six files of which four hold data, 14,780 sentences labelled positive, neutral or negative from an investor's view; the project keeps 2,180 positive or negative sentences from the AllAgree and 75Agree files, 1,457 positive and 723 negative, and the data are cross-sectional, not time series (V1 p.318, p.319).
Cleansing: split each line on the "@" separator into sentence and sentiment columns, no html to remove, substitute percentage and dollar signs with word annotations before stripping other punctuation, remove numbers but first expand "m", "mln", "mn" to "million", remove white space (V1 p.319, p.320).
Normalization: lowercase, do not remove stop words yet because "not", "more", "very", "few" carry sentiment, stem, and collapse EUR and USD into "currencysign"; the result is 2,673 unique tokens in the preliminary unigram BOW (V1 p.321, p.322).
EDA: the most frequent tokens ("the", "million", "currencysign") are the same in both classes so cannot discriminate; sentence lengths run 26 to 273 characters with a mean near 120 and no outliers; the split word cloud shows "decreas" and "down" in the negative half, "increas" and "rose" in the positive half (V1 p.323 to p.325).
Feature selection: 44,151 non-unique tokens across 2,180 sentences; TF at collection level (collection frequency) runs from 2.265e-05 to 5.429e-02; the 14 words above the 99.5th percentile become custom stop words and the 714 words below the 30th percentile are dropped, with single characters removed as well (V1 p.326, p.327, p.329).
The DTM cells use TF rather than TF-IDF because the documents are single sentences, and TF-IDF varies with the number of documents so performance can shift on a corpus with few documents (V1 p.329).
Feature engineering: unigrams and bigrams together, so negations such as not_good and no_longer survive, giving tokens like loss_prior, oper_rose, sale_increas (V1 p.329, p.330).
Training: labels 1 positive and 0 negative, a 60:20:20 split by stratified random sampling within class, DTMs of 1,309 by 9,188 (training), 435 by 9,188 (CV) and 436 by 9,188 (test) with the columns fixed by the training BOW while the master corpus had 11,501 tokens (V1 p.332, p.333).
Method: SVM, decision trees and logistic regression were candidates; SVM and logistic regression beat trees, and logistic regression is retained because it handles sparse DTMs by shrinking coefficients of rare tokens toward zero and outputs a probability p that needs a threshold (V1 p.333).
Evaluation: AUC 96.5% on training against 86.2% on CV means overfitting; LASSO regularization brings them to 95.7% and 94.8%, a good fit; an unregularized model with all tokens gave 99.1% against 89.4%, overfitting again, and nothing underfits since all AUCs are far above 50% (V1 p.334, p.335).
Threshold tuning: at p = 0.50 the CV confusion matrix gives accuracy 0.90 and F1 0.93; sweeping p from 0.01 to 0.99 and tabulating 0.45 to 0.75 shows 0.60 to 0.63 maximise both, so 0.60 is chosen and accuracy, F1 and precision rise to 0.91, 0.94 and 0.90 (V1 p.335 to p.338).
Test: 436 new sentences, processed identically, give precision 0.89, recall 0.98, F1 0.93, accuracy 0.90, similar to training and CV, so the model is robust and not overfitting; a 30-sentence sample had 3 misclassifications, 27/30 = 90% (V1 p.338 to p.340).

## Formulas and derivations

**Normalization to [0, 1]** (V1 p.286)
$$ X_{i}^{\text{norm}} = \frac{X_i - X_{\min}}{X_{\max} - X_{\min}} $$
^f-01-07-1

- $X_i$: observation; $X_{\min}$, $X_{\max}$: minimum and maximum of the feature over the full sample, so the result lies in [0, 1] (V1 p.286).
- Derivation: subtracting the minimum shifts the smallest value to 0; dividing by the range scales the largest to 1; every other value keeps its relative position.
- Sensitive to outliers because a single extreme value stretches the range and compresses everything else, so treat outliers first; usable when the distribution is unknown (V1 p.286).

> [!tip] Calculator
> Practice Q6: 1.2 - 0.2 = 1.0; 12.2 - 0.2 = 12.0; 1.0 / 12.0 = 0.0833 (V1 p.354).

**Standardization to mean 0 and standard deviation 1** (V1 p.286)
$$ X_{i}^{\text{std}} = \frac{X_i - \mu}{\sigma} $$
^f-01-07-2

- $\mu$: mean of the feature; $\sigma$: its standard deviation (V1 p.286).
- Centering subtracts the mean so the new mean is 0; scaling divides by the standard deviation so the new standard deviation is 1.
- Less sensitive to outliers than normalization, but the data must be normally distributed (V1 p.286).

**Standard deviation outlier rule for normal data** (V1 p.285)
$$ \lvert X_i - \mu \rvert > 3\sigma \;\Rightarrow\; X_i \text{ may be an outlier} $$
^f-01-07-3

- Applies to normally distributed data only (V1 p.285).
- Reason: under normality about 0.3% of values fall beyond 3 standard deviations, so such a value is more likely an error or an extreme case than a typical observation.

**Interquartile range outlier bounds for any distribution** (V1 p.285)
$$ \text{IQR} = Q_3 - Q_1, \qquad \text{outlier if } X_i > Q_3 + 1.5\,\text{IQR} \text{ or } X_i < Q_1 - 1.5\,\text{IQR} $$
^f-01-07-4

- $Q_3$, $Q_1$: 75th and 25th percentiles; a multiple of 3.0 instead of 1.5 flags extreme values (V1 p.285).
- Reason it holds: the IQR measures the central spread without using the mean or standard deviation, so it works whatever the shape of the distribution.
- Trimming removes flagged values; winsorization replaces them with the largest or smallest non-outlier value (V1 p.285).

**Precision** (V1 p.313)
$$ P = \frac{TP}{TP + FP} $$
^f-01-07-5

- $TP$: actual 1 predicted 1; $FP$: actual 0 predicted 1, the Type I error (V1 p.312, p.313).
- Denominator is everything the model called positive, so precision answers "when it says 1, how often is it right".
- Use when the cost of a false positive is high: scrapping a good product, buying a stock whose sentiment is really negative (V1 p.313, p.342).

**Recall, also sensitivity and true positive rate** (V1 p.313, p.315)
$$ R = \frac{TP}{TP + FN} = TPR $$
^f-01-07-6

- $FN$: actual 1 predicted 0, the Type II error (V1 p.312, p.313).
- Denominator is everything that is actually positive, so recall answers "of the real 1s, how many did it catch".
- Use when the cost of a false negative is high: shipping a defective product, shorting a stock whose sentiment is really positive (V1 p.313, p.342).
- The true positive rate on the ROC y-axis is the same ratio (V1 p.314, p.315).

**Accuracy** (V1 p.313)
$$ \text{Accuracy} = \frac{TP + TN}{TP + FP + TN + FN} $$
^f-01-07-7

- Numerator is all correct predictions, denominator is all predictions (V1 p.313).
- Appropriate when the classes are balanced; with class imbalance a naive majority-class model scores high accuracy while missing every minority case (V1 p.311, p.314).

**F1 score, harmonic mean of precision and recall** (V1 p.313)
$$ F_1 = \frac{2PR}{P + R} = \frac{2}{\frac{1}{P} + \frac{1}{R}} $$
^f-01-07-8

- Derivation: the harmonic mean of two numbers is $2/(1/P + 1/R)$; multiply numerator and denominator by $PR$ to get $2PR/(P+R)$.
- The harmonic mean sits closer to the smaller of P and R than the arithmetic mean does, so a model cannot hide a weak recall behind a strong precision (V1 p.314).
- Preferred overall measure under unequal class distribution; equal weight to FP and FN (V1 p.313, p.336).

> [!tip] Calculator
> Exhibit 24: P = 3 / 4 = 0.75; R = 3 / 5 = 0.60; 2 x 0.75 x 0.60 = 0.90; 0.75 + 0.60 = 1.35; 0.90 / 1.35 = 0.6667 (V1 p.314).
> Practice Q13 to Q15: P = 182 / 234 = 0.7778; R = 182 / 213 = 0.8545; F1 = 2 x 0.7778 x 0.8545 / (0.7778 + 0.8545) = 1.3292 / 1.6323 = 0.8143; accuracy = 278 / 361 = 0.7701 (V1 p.355, p.356).

**False positive rate, ROC x-axis** (V1 p.314)
$$ FPR = \frac{FP}{TN + FP} $$
^f-01-07-9

- Denominator is all actual negatives, so FPR is the share of real 0s wrongly called 1 (V1 p.314).
- The ROC curve plots FPR against TPR as the logistic cutoff p moves from 0 to 1; a more convex curve and higher AUC are better, AUC near 1.0 is near-perfect and 0.5 is random guessing (V1 p.314, p.315).

**True positive rate, ROC y-axis** (V1 p.315)
$$ TPR = \frac{TP}{TP + FN} $$
^f-01-07-10

- Identical to recall; a point on the ROC curve is one confusion matrix at one threshold (V1 p.314, p.315).
- Lowering the threshold classifies more observations as 1, raising both TPR and FPR, which traces the curve from the origin to (1, 1).

**Root mean squared error** (V1 p.315)
$$ \text{RMSE} = \sqrt{\sum_{i=1}^{n} \frac{(\text{Predicted}_i - \text{Actual}_i)^2}{n}} $$
^f-01-07-11

- $n$: number of predictions; the errors are squared, averaged, then rooted so the result is in the units of the target (V1 p.315).
- For continuous prediction, mostly regression; smaller is better (V1 p.315).

**Term frequency at the collection level, also collection frequency** (V1 p.328)
$$ TF_{\text{coll}} = \frac{\text{TotalWordCount}}{\text{Total number of words in collection}} $$
^f-01-07-12

- TotalWordCount: occurrences of the token in the whole corpus; the denominator in the project is 44,151 (V1 p.326, p.328).
- Example: "the" occurs 2,397 times, so $2{,}397 / 44{,}151 = 0.05429$ (V1 p.328).
- Used to find outlier tokens: the highest are stop words, the lowest are proper nouns and sparse terms, the middle carries the signal (V1 p.327, p.331).

**Term frequency at the sentence level** (V1 p.328)
$$ TF_{\text{sent}} = \frac{\text{WordCountInSentence}}{\text{TotalWordsInSentence}} $$
^f-01-07-13

- Example: "the" appears 6 times in the 39-word sentence 701, so $6/39 = 0.15385$; 5 times in the 37-word sentence 223, so $5/37 = 0.13514$ (V1 p.328).
- This is the TF that fills the DTM cells in the project and the TF that multiplies IDF (V1 p.328, p.329).

**Document frequency** (V1 p.328)
$$ DF = \frac{\text{SentenceCountWithWord}}{\text{Total number of sentences}} $$
^f-01-07-14

- Total sentences in the project is 2,180; "the" appears in 1,453, so $DF = 0.66651$, 66.7% of sentences (V1 p.328).
- A high DF means the token is everywhere and differentiates nothing (V1 p.328).

**Inverse document frequency** (V1 p.328)
$$ IDF = \ln\!\left(\frac{1}{DF}\right) $$
^f-01-07-15

- The curriculum writes log; the worked numbers use the natural log, since $\ln(1/0.66651) = 0.40569$ matches Exhibit 39 (V1 p.327, p.328).
- Derivation: $1/DF$ is large for rare tokens and 1 for a token in every document; the log compresses the scale so IDF is 0 for a universal token and grows slowly with rarity.
- IDF measures how unique a term is across the corpus and is not directly related to corpus size (V1 p.328).

**TF-IDF** (V1 p.328)
$$ TF\text{-}IDF = TF_{\text{sent}} \times IDF $$
^f-01-07-16

- It is sentence-level TF, not collection-level TF, that is multiplied (V1 p.328, p.359).
- Example: "of" in sentence 128, $0.16667 \times 0.79545 = 0.13258$ (V1 p.329).
- High TF-IDF means a term frequent within few documents, a unique and important term; low means a term present in many documents (V1 p.328).
- Values vary with the number of documents, so a model built on TF-IDF can behave differently on a corpus with few documents (V1 p.329).

**Logistic regression probability of positive sentiment** (V1 p.333)
$$ P(y = 1) = \frac{1}{1 + \exp\!\left[-(\beta_0 + \beta_1 x_1 + \beta_2 x_2 + \cdots + \beta_n x_n)\right]} $$
^f-01-07-17

- $x_j$: TF value of token $j$ in the sentence's DTM row; $\beta_j$: penalized logistic coefficient learned by maximum likelihood (V1 p.333, p.338).
- The output is a probability between 0 and 1; a sentence is classified 1 when $p$ exceeds the threshold, which is a tuned hyperparameter rather than the theoretical 0.50 (V1 p.316, p.333).

**Total fitting error and the tuning diagnosis** (V1 p.316)
$$ \text{Total error} = \text{Bias error} + \text{Variance error}, \qquad \text{Error}_{CV} \gg \text{Error}_{train} \Rightarrow \text{overfitting} $$
^f-01-07-18

- High training error signals underfitting and bias; CV error significantly above training error signals overfitting and variance (V1 p.316).
- Neither can be eliminated, so tuning minimises the sum; the fitting curve against lambda shows the minimum where the two error curves meet and are both small (V1 p.316, p.317).

## Worked examples

### Example 1: Steps in ML model building (V1 p.279, p.280, p.281)

Setting: LendALot, a B2C lender, wants in-house ML credit scoring, starting with structured data and later adding free-response text from loan applications; Paul Wang leads the team.

Q1: one decision per structured step.
A, conceptualization: specify the output (a binary creditworthiness class), who uses it, and how it embeds in LendALot's processes (V1 p.280).
B, data collection: internal, external, or both (V1 p.280).
C, preparation and wrangling: cleansing needs (missing and extreme values) and preprocessing needs (extract, aggregate, filter, select columns) (V1 p.280).
D, exploration: which EDA methods, which features to use, which to engineer (V1 p.280).
E, training: which algorithm, supervised given labels, how fit is measured, how the model is validated and tuned (V1 p.280).

Q2: Wang's instruction to enhance the model with text from free-response fields.
This is text problem formulation, the first text step, because it defines the text input and the intended output (V1 p.280).

Q3: two text curation needs.
The data are internal, so the team must ensure the comment fields were correctly implemented and enabled, and that response rates are high enough to analyse if the fields are optional (V1 p.280).

Q4: two text preparation and wrangling needs.
Text cleansing and text preprocessing, the two tasks that turn an unstructured stream into structured values (V1 p.281).
^ex-01-07-1

### Example 2: Preparing and wrangling structured data (V1 p.286, p.287, p.288)

Setting: Lynn Lee's seven-row loan sample: Ms. Beta has income of -63,050; Mr. Gamma has no loan type; Ms. Delta's loan amount is "unknown" though the loan was repaid; Mr. Zeta appears in rows 7 and 8 identically.
Wang's Statement 1: keep ID, drop Name; Statement 2: create loan amount as a percent of income.

Q1: Ms. Beta, answer A, invalidity, because income cannot be negative, so the value is outside a meaningful range (V1 p.287).
Q2: Mr. Gamma, answer C, incompleteness, the loan type is missing (V1 p.287).
Q3: Ms. Delta, answer B, inaccuracy, the lender must know how much it lent to a borrower who repaid, so "unknown" is not the true value; it is not out of range, so not invalidity (V1 p.287).
Q4: Mr. Zeta, answer C, duplication, row 8 repeats row 7 (V1 p.287).
Q5: Statement 1 is data selection, removing a column not needed because ID already identifies the observation (V1 p.287).
Q6: Statement 2 is data extraction, a new variable formed as the ratio of two existing ones; "data engineering" is not the curriculum's preprocessing term (V1 p.288).
Check on Q6: for Mr. Alpha the ratio would be $10{,}000 / 34{,}000 = 0.294$, a legitimate extracted feature.
^ex-01-07-2

### Example 3: Unstructured data preparation and wrangling (V1 p.294, p.295)

Q1: the output of preparing and wrangling text is C, a document term matrix, the structured table computers can read; a confusion matrix belongs to evaluation (V1 p.294).
Q2: annotations are added when removing C, punctuation, because percent signs, currency symbols and question marks carry meaning; html tags and white space are removed without annotation (V1 p.294).
Q3: a DTM column is A, a token from the BOW; rows are instances (V1 p.294).
Q4: a DTM cell is B, a count of the tokens of that column's kind in that document (V1 p.295).
Q5: normalization includes C, lowercasing; removing numbers and white space are cleansing (V1 p.295).
Q6: for infrequent words that risk complex models, A, stemming, which aggregates sparse inflected forms into a stem; scaling is for numeric features, cleansing is a prior step (V1 p.295).
Q7: C, tokenization splits text into tokens; it is part of wrangling, not cleansing, and is most commonly at word level, not character level (V1 p.295).
^ex-01-07-3

### Example 4: Data exploration (V1 p.305, p.306)

Setting: Eric Kim examines six loan rows with structured fields (ID, loan outcome, income, loan amount, credit score, loan type) and free-response text explaining the credit score.

Q1: histograms and box plots show how income, loan amount and credit score are distributed, overall and within defaulted versus non-defaulted loans; scatterplots of income against loan amount, income against credit score and loan amount against credit score, overall and by outcome, reveal relationships between continuous variables (V1 p.305, p.306).
Q2: a word cloud for the free responses gives a quick view of term frequency; besides obvious words ("credit", "score"), words such as "worked", "hard", "probably", "embarrassed", "regret", "good", "decent", "great" might predict creditworthiness (V1 p.306).
Q3: with a discrete target (loan outcome), chi-square and information gain are suitable univariate ranking methods; they also apply to word-count features such as TF and DF built from frequent words like "worked" and "hard" (V1 p.306).
Q4: bigrams that could discriminate outcomes: "credit_score" and "worked_hard" (V1 p.306).
^ex-01-07-4

### Example 5: Textual feature representations (V1 p.306, p.307, p.308)

Q1: three representations to consider are bag-of-words, n-grams, and parts of speech; name entity recognition is less applicable because the borrower text has no explicit people, places, dates or organizations (V1 p.307).
Q2: rationale for each.
BOW applies wherever token boundaries are explicit (English) or inferable (Spanish) and is the best starting point (V1 p.307).
N-grams add context: "worked" appears three times (rows 5 to 7), twice in no-default text and once in defaulted text; the trigram "have_worked_hard" appears in both no-default texts while "had_worked_harder" appears in the defaulted text, so the trigram separates accomplishment from regret where the unigram cannot (V1 p.307, p.308).
POS tags show composition, whether borrowers use many action words (verbs) or descriptors (adjectives), and whether that differs between default and no-default (V1 p.308).
^ex-01-07-5

### Example 6: Calculating and interpreting term frequency measures (V1 p.330, p.331, p.332)

Setting: Jack and Jill's corpus has 44,151 tokens and 2,180 sentences; Table 1 lists "a" in sentence 1,826 (TotalWordCount 873, 6 of 34 words, in 687 sentences) and Table 2 lists "great" in sentence 1,368 (TotalWordCount 4, 1 of 9 words, in 4 sentences).

Q1: TF at collection and sentence level.
Collection level for "a": $873 / 44{,}151 = 0.019773$, 1.977%.
Collection level for "great": $4 / 44{,}151 = 0.0000906$, 0.009%.
Sentence level for "a": $6 / 34 = 0.176471$, 17.647%.
Sentence level for "great": $1 / 9 = 0.111111$, 11.111%.
Collection-level TF identifies outliers: the highest values are stop words like "a", the lowest are proper nouns and sparse terms, and intermediate values carry sentiment information; sentence-level TF measures a token's importance within one instance (V1 p.331).

Q2: TF-IDF.
DF for "a": $687 / 2{,}180 = 0.315138$; for "great": $4 / 2{,}180 = 0.001835$.
IDF for "a": $\ln(1 / 0.315138) = 1.154746$; for "great": $\ln(1 / 0.001835) = 6.300786$.
TF-IDF for "a": $0.176471 \times 1.154746 = 0.203779$; for "great": $0.111111 \times 6.300786 = 0.700087$.
Python check reproduces 0.2037787 and 0.7000873 to seven places, matching Exhibits 39 and 40.
High TF-IDF flags "great" as frequent within few documents, an important unique term; low TF-IDF flags "a" as present in most sentences and non-discriminative (V1 p.332).
Extra rows from Exhibit 39 and 40 verified: "the" in sentence 701 gives $6/39 \times 0.405694 = 0.062415$; "argument" in sentence 1,952 gives $1/6 \times 7.687080 = 1.281180$ (V1 p.327, p.329).
^ex-01-07-6

### Example 7: Comparing performance metrics for confusion matrices with different threshold p values (V1 p.340, p.341, p.342)

Setting: the CV confusion matrix at p = 0.60 (Exhibit 50) has TP 284, FP 30, FN 7, TN 114; Matrix A at p = 0.75 has TP 281, FP 28, FN 17, TN 110; Matrix B at p = 0.45 has TP 281, FP 41, FN 4, TN 110.

Recomputed metrics:

| Matrix | Threshold | Precision | Recall | F1 | Accuracy |
|---|---|---|---|---|---|
| Exhibit 50 | 0.60 | $284/314 = 0.9045$ | $284/291 = 0.9759$ | 0.9388 | $398/435 = 0.9149$ |
| A | 0.75 | $281/309 = 0.9094$ | $281/298 = 0.9430$ | 0.9259 | $391/436 = 0.8968$ |
| B | 0.45 | $281/322 = 0.8727$ | $281/285 = 0.9860$ | 0.9259 | $391/436 = 0.8968$ |

Q1: A versus 0.60.
A has fewer TPs (281 vs 284) and fewer TNs (110 vs 114), so lower accuracy (0.90 vs 0.91) and lower F1 (0.93 vs 0.94); its precision is slightly better (0.91 vs 0.90) from fewer FPs, but its recall is much worse (0.94 vs 0.98) from 17 FNs against 7; the 0.60 model is superior (V1 p.341).
Q2: B versus 0.60.
B has the same TPs and TNs as A, so the same lower accuracy 0.90 and F1 0.93; its recall is slightly better (0.99 vs 0.98) from fewer FNs but its precision is lower (0.87 vs 0.90) from 41 FPs against 30; again 0.60 wins (V1 p.341).
Q3: A versus B.
A has higher precision (0.91 vs 0.87), B higher recall (0.99 vs 0.94), the FP versus FN trade-off; raising the threshold cuts FPs and raises FNs, lowering it does the reverse; in sentiment terms an FP buys a stock whose sentiment is actually negative and an FN avoids or shorts a stock whose sentiment is actually positive; the 0.60 model balances the two (V1 p.341, p.342).
Note: the book labels these CV matrices N = 436 while the CV split has 435 sentences; the arithmetic above uses the matrix totals as printed.
^ex-01-07-7

### Exhibit 24: Performance metrics from a ten-observation sample (V1 p.314)

Ten observations with actual and predicted labels give TP 3 (obs 1, 3, 5), TN 4 (obs 2, 7, 8, 9), FN 2 (obs 4, 6), FP 1 (obs 10).
$P = 3 / (3 + 1) = 0.75$.
$R = 3 / (3 + 2) = 0.60$.
$F_1 = 2 \times 0.75 \times 0.60 / (0.75 + 0.60) = 0.90 / 1.35 = 0.6667$.
Accuracy $= (3 + 4) / 10 = 0.70$.
Precision above recall means the model is better at avoiding FPs than FNs; F1 at 0.67 sits closer to the smaller value 0.60 than the arithmetic mean 0.675 would; with 5 actual 1s and 5 actual 0s the classes are balanced so accuracy is also appropriate (V1 p.314).
^ex-01-07-8

### Exhibits 47 and 50: Tuning the threshold on the CV set (V1 p.335 to p.338)

At p = 0.50: TP 284, FP 38, FN 7, TN 106.
$P = 284 / 322 = 0.8820$, $R = 284 / 291 = 0.9759$, $F_1 = 0.9266$ (the book's 0.93 from rounded inputs is 0.9273), accuracy $= 390 / 435 = 0.8966$, matching the 0.8965517 row in Exhibit 49 (V1 p.335, p.337).
Sweeping p from 0.45 to 0.75: recall stays at 0.9759 from 0.48 to 0.62 while precision climbs as FPs fall, so F1 and accuracy peak at 0.60 to 0.62 with precision 0.9045, F1 0.9388, accuracy 0.9149; from 0.63 recall starts to drop (V1 p.336, p.337).
At p = 0.60: TP 284, FP 30, FN 7, TN 114.
$P = 284 / 314 = 0.9045$, $R = 0.9759$, $F_1 = 0.9388$, accuracy $= 398 / 435 = 0.9149$.
Relative to 0.50: eight FPs became TNs, precision up two points to 0.90, accuracy and F1 up one point to 0.91 and 0.94 (V1 p.338).
Note: Exhibit 49's row for 0.58 prints recall as 9.9759, a typo for 0.9759.
^ex-01-07-9

### Exhibits 51 and 52: Test set results (V1 p.338, p.339, p.340)

The 30-sentence sample misclassifies sentence 10 (p = 0.46, actual 1), sentence 26 (p = 0.77, actual 0) and sentence 30 (p = 0.71, actual 0), so sample accuracy is $27 / 30 = 0.90$ (V1 p.338).
Full test set: TP 284, FP 35, FN 7, TN 110, N 436.
$P = 284 / 319 = 0.8903$, $R = 284 / 291 = 0.9759$, $F_1 = 0.9311$, accuracy $= 394 / 436 = 0.9037$.
Training AUC 95.7%, CV metrics 0.91 and 0.94, test metrics 0.90 and 0.93: performance is similar across all three splits, so the model is robust, not overfitting, and should generalise to new sentences that receive identical tokenization, cleansing and preprocessing (V1 p.339, p.340).
^ex-01-07-10

## Item-set patterns

> [!warning] Trap: "the second step in the text pipeline is preparation and wrangling"
> The vignette lists steps out of order or swaps a text step for a structured one.
> Correct approach: recite both lists; text curation is the second text step, data collection is the second structured step, preparation and wrangling is third in both, exploration fourth in both, training fifth in both (V1 p.278, p.354).
> Distractor: the statement that describes cleansing and converting to a structured format and calls it "curation" is tempting because curation sounds like tidying; curation is gathering the raw text by web services or spidering (V1 p.278, p.356).

> [!warning] Trap: which V is the concern
> A character worries that 10% to 15% of social media content is fake, or that data arrive every second, or that sources are of many kinds.
> Correct approach: fake or unreliable content is veracity; speed of creation is velocity; array of source types is variety; sheer quantity is volume (V1 p.276, p.277).
> Distractor: velocity is tempting for Twitter because tweets stream fast, but the concern quoted is about reliability, so veracity (V1 p.354).

> [!warning] Trap: six data errors that sound alike
> A raw table has one negative income, one "unknown" loan amount, one interest expense with zero debt, dates in three formats, a repeated row, and blank cells.
> Correct approach: negative is invalidity (out of range); unknown but knowable is inaccuracy; interest with no debt is inconsistency (two fields contradict); mixed formats is non-uniformity; repeated row is duplication; blank is incompleteness (V1 p.283, p.287, p.354).
> Distractors: invalidity for the "unknown" amount tempts because it is not a number, but it is not outside a range; non-uniformity for the interest/debt row tempts because something looks off, but format is identical (V1 p.354).

> [!warning] Trap: extraction versus selection versus feature engineering
> An analyst creates an age variable from IPO date, builds a coverage ratio, and deletes the date column.
> Correct approach: creating a new variable from an existing one during preprocessing is extraction; deleting a column is selection; both are preprocessing, not feature engineering, which happens later in exploration (V1 p.284, p.354).
> Distractors: conversion tempts because a date became a number, but conversion is about data types and units; aggregation tempts for the ratio, but aggregation sums similar variables into one (V1 p.284, p.285).

> [!warning] Trap: cleansing operation or normalization operation
> A statement lists html tags, punctuation, numbers and white space as things to remove "before normalizing", or claims tokenization is part of cleansing.
> Correct approach: the four cleansing operations are html tags, punctuation (with annotations for meaningful marks), numbers (or /number/), white space; the normalization operations are lowercasing, stop words, stemming, lemmatization; tokenization precedes normalization within wrangling (V1 p.289 to p.291, p.295).
> Distractor: the statement is wrong only in its treatment of punctuation, because meaningful punctuation must be substituted with annotations rather than removed outright; the white-space option is a decoy (V1 p.354, p.355).

> [!warning] Trap: which tokens to remove after a frequency analysis
> An exhibit shows the five highest-TF words ("the", "and", "to") and the five lowest ("naval", "stereotype").
> Correct approach: remove both groups; high TF words are stop words that cause underfitting, low TF words are sparse proper nouns that cause overfitting; informative tokens have intermediate TF (V1 p.302, p.327, p.357, p.358).
> Distractors: "only Group 1" tempts because stop words are the familiar noise; "only Group 2" tempts because rare words look like errors; the exam wants both (V1 p.357).

> [!warning] Trap: TF-IDF statement sets
> Three statements: IDF equals the inverse of DF; collection-level TF times IDF gives TF-IDF; TF-IDF varies with the number of documents.
> Correct approach: IDF is the log of the inverse of DF; sentence-level TF multiplies IDF; the third statement is correct (V1 p.328, p.329, p.359).
> Distractors: dropping the log is the classic omission; the collection-level TF is the number that appears first in the table, so it tempts.

> [!warning] Trap: which metric answers the client's cost concern
> A manager says "we are most concerned with the cost of Type I errors" and three confusion matrices show different precision, recall, F1 and accuracy.
> Correct approach: Type I is FP, so precision, and pick the matrix with the highest precision even if another has higher accuracy or F1 (V1 p.313, p.360).
> Distractors: highest accuracy tempts because it is the headline number; highest F1 tempts because the dataset is imbalanced, but F1 balances FP and FN and the manager does not want balance (V1 p.360).

> [!warning] Trap: bias and variance are tuning, not performance evaluation
> A remark says fitting errors such as bias and variance are used in the performance evaluation stage to measure goodness of fit.
> Correct approach: performance evaluation uses error analysis, ROC/AUC and RMSE; bias and variance are the language of tuning (V1 p.312, p.316, p.362).
> Distractor: the remark sounds right because bias and variance are errors and evaluation measures errors, but the curriculum places the diagnosis under tuning.

> [!warning] Trap: reading AUC pairs
> A table gives training and CV AUC for several thresholds: 56.7/57.3, 91.3/89.7, 98.4/87.1.
> Correct approach: near 50% is random guessing; a large gap with training far higher is overfitting; close and high is a good fit, so the middle row wins, and the fix for the overfit row is LASSO regularization, not lowering AUC or reducing ROC convexity (V1 p.315, p.334, p.358).
> Distractor: the highest training AUC tempts as "best"; the exam wants the smallest generalisation gap at a high level.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM07-Big-Data-Projects-Practice-Problems]]

## Cross-links

- [[LM06-Machine-Learning]]: supplies the vocabulary this module applies: supervised versus unsupervised, overfitting as variance error, the training/validation/test partition, LASSO as the regularization used on the sentiment logistic model, and SVM, CART and neural networks as the candidate methods (V1 p.311, p.316, p.334).
- [[LM04-Extensions-of-Multiple-Regression]]: logistic regression is the classifier of the case study; its output is a probability from the logistic function and the p-threshold is the hyperparameter tuned here (V1 p.333).
- [[LM01-Basics-of-Multiple-Regression-and-Underlying-Assumptions]]: the feature selection diagnostics named here, heteroskedasticity and multicollinearity, and the information-gain measure via R-squared are the regression tools of that module (V1 p.299, p.300).
- [[LM05-Time-Series-Analysis]]: the Financial Phrase Bank is explicitly cross-sectional, which is why random k-fold style splitting is allowed; time series would forbid it (V1 p.311, p.319).
- [[LM06-Backtesting-and-Simulation]]: the discipline of scoring a model only on data it never saw, and the trade-off between in-sample and out-of-sample performance, is the same one that module formalises for investment strategies (V1 p.309, p.340).

## Self-test

Vignette A (Q1 to Q4): Priya Nair at Kaveri Capital builds a model to flag which small-cap issuers will restate earnings within a year, using structured ratios and MD&A text scraped from filings.
Her raw ratio table has one issuer with a current ratio of -2.1, one with "n/a" for total assets although the issuer files audited accounts, one with two rows identical in every field, and revenue reported in USD millions for some issuers and INR crores for others.
She plans to (i) create "log of market cap times revenue" as a new feature, (ii) delete the ticker column, (iii) rescale interest coverage to [0, 1], and (iv) cap the top and bottom 2% of leverage ratios at the 98th and 2nd percentile values.
For the text she removes html, replaces "%" with /percentSign/, replaces every number with /number/, lowercases, keeps "not" and "no", and stems with Porter's algorithm.
Her frequency table shows "the" with TF 0.052 and "kaveri" with TF 2.3e-05.
The restatement class is 4% of issuers.

> [!question] Q1
> The four data errors, in the order listed, are best classified as:
> A. invalidity, inaccuracy, duplication, non-uniformity.
> B. invalidity, incompleteness, duplication, inconsistency.
> C. inconsistency, incompleteness, invalidity, non-uniformity.

> [!question] Q2
> Which of Nair's four planned operations is a data preprocessing transformation rather than a feature engineering, scaling, or outlier treatment?
> A. (i) only.
> B. (ii) only.
> C. (iii) and (iv).

> [!question] Q3
> Operation (iv) is best described as:
> A. trimming, appropriate because normalization is sensitive to outliers.
> B. winsorization, appropriate because it should precede normalization.
> C. standardization, appropriate only if leverage is normally distributed.

> [!question] Q4
> Regarding "the" and "kaveri", and the 4% restatement class, Nair should most likely:
> A. remove both tokens and oversample the restatement class.
> B. remove "the" only and undersample the restatement class.
> C. keep both tokens because "not" and "no" were kept, and use accuracy as the overall metric.

Vignette B (Q5 to Q7): Tomas Reyes trains a logistic regression on 5,000 labelled analyst-call sentences (3,800 positive, 1,200 negative), split 60:20:20.
Unregularized, the model shows AUC 0.99 on training and 0.84 on CV; with LASSO it shows 0.94 and 0.93.
At p = 0.50 the CV confusion matrix is TP 700, FP 90, FN 60, TN 150; at p = 0.70 it is TP 640, FP 40, FN 120, TN 200.
Reyes's client will short any stock whose call is classified negative and says a wrongly shorted stock is far costlier than a missed short.

> [!question] Q5
> The change from AUC 0.99/0.84 to 0.94/0.93 is best described as:
> A. a move from underfitting toward the optimum, since training AUC fell.
> B. a reduction in variance error, since the CV gap closed while CV AUC rose.
> C. an increase in bias error that should be reversed by reducing lambda.

> [!question] Q6
> At p = 0.50 versus p = 0.70, precision and F1 are closest to:
> A. 0.886 and 0.903 versus 0.941 and 0.889.
> B. 0.921 and 0.903 versus 0.842 and 0.889.
> C. 0.886 and 0.850 versus 0.941 and 0.840.

> [!question] Q7
> Given the client's cost statement, and treating "negative" as the positive class of interest for the short trade, the metric to maximise and the threshold direction are:
> A. precision of the negative class, raising the bar for calling a sentence negative.
> B. recall of the negative class, lowering the bar for calling a sentence negative.
> C. accuracy, since the client cares about both error types.

Vignette C (Q8 to Q10): Lena Fischer computes term frequency measures for a corpus of 3,000 sentences and 60,000 tokens.
The token "surg" occurs 90 times in the corpus, appears once in sentence 412 (12 words), and is present in 75 sentences.
The token "compani" occurs 2,400 times, twice in sentence 412, and is present in 1,800 sentences.
Fischer says: Statement 1, "surg" has the higher IDF because it is present in fewer sentences; Statement 2, if the corpus doubles to 6,000 sentences with the same proportions, IDF is unchanged; Statement 3, the DTM should use TF-IDF because the documents are single sentences.

> [!question] Q8
> TF-IDF for "surg" in sentence 412 is closest to:
> A. 0.307.
> B. 0.083.
> C. 0.006.

> [!question] Q9
> TF-IDF for "compani" in sentence 412 is closest to:
> A. 0.085.
> B. 0.167.
> C. 0.511.

> [!question] Q10
> Which of Fischer's statements is correct?
> A. Statements 1 and 2 only.
> B. Statements 1 and 3 only.
> C. Statement 2 only.

> [!success]- Answer key
> Q1: A.
> A negative current ratio is outside a meaningful range, invalidity (V1 p.283); "n/a" for an audited filer is a value that is not the truth though knowable, inaccuracy, the same logic as Ms. Delta's unknown loan amount (V1 p.287); identical rows are duplication; mixed currencies and units are non-uniformity, the ambiguous-dollar-symbol case (V1 p.283).
> B mislabels "n/a" as incompleteness, which would fit only if no source could supply it, and mislabels units as inconsistency, which needs a contradiction between fields; C mislabels the negative ratio as inconsistency.
> Q2: B.
> Deleting a column is selection, one of the five preprocessing transformations (V1 p.284).
> (i) creates a feature from a transformation of two features, the "log of the product" example of feature engineering in exploration (V1 p.300); (iii) is normalization, scaling; (iv) is winsorization, outlier treatment (V1 p.285, p.286).
> A and C therefore pick the wrong operations.
> Q3: B.
> Replacing extreme values with the boundary non-outlier values is winsorization, and outliers must be handled before scaling because normalization is sensitive to them (V1 p.285, p.286).
> A is wrong because trimming removes rather than caps; C is wrong because standardization is a scaling method, not an outlier treatment.
> Q4: A.
> "the" is a high-TF stop word (underfitting) and "kaveri" is a low-TF proper noun (overfitting), so both are noise; a 4% minority class is class imbalance, cured by oversampling the minority or undersampling the majority (V1 p.302, p.311).
> B undersamples the minority, deepening the imbalance; C confuses the decision to keep sentiment-bearing stop words such as "not" with keeping all stop words, and accuracy is inappropriate with a 96/4 split (V1 p.314, p.321).
> Q5: B.
> A large training-minus-CV AUC gap is overfitting, variance error; LASSO closed the gap and raised CV AUC, exactly the case study's 96.5/86.2 to 95.7/94.8 (V1 p.334, p.335).
> A is wrong because a 0.99 training AUC is not underfitting; C is wrong because bias would show as low AUC on both sets, and lowering lambda would reintroduce the variance.
> Q6: A.
> At 0.50: $P = 700/790 = 0.886$, $R = 700/760 = 0.921$, $F_1 = 2 \times 0.886 \times 0.921 / 1.807 = 0.903$.
> At 0.70: $P = 640/680 = 0.941$, $R = 640/760 = 0.842$, $F_1 = 2 \times 0.941 \times 0.842 / 1.783 = 0.889$ (V1 p.313).
> B swaps precision with recall; C pairs precision with accuracy ($850/1{,}000 = 0.850$ and $840/1{,}000 = 0.840$) in place of F1.
> Q7: A.
> A wrongly shorted stock is a false positive for the negative class, a Type I cost, so maximise precision; raising the threshold for calling a sentence negative reduces FPs at the cost of FNs, the Matrix A direction in Example 7 (V1 p.313, p.341, p.342).
> B optimises for Type II cost, the opposite of the client's statement; C ignores the explicit asymmetry and the class imbalance.
> Q8: A.
> $TF_{sent} = 1/12 = 0.08333$; $DF = 75/3{,}000 = 0.025$; $IDF = \ln(1/0.025) = 3.6889$; $TF\text{-}IDF = 0.08333 \times 3.6889 = 0.3074$ (V1 p.328).
> B is the sentence-level TF alone; C is the collection-level TF $90/60{,}000 = 0.0015$ times IDF, $0.0055$, which is not the definition.
> Q9: A.
> $TF_{sent} = 2/12 = 0.16667$; $DF = 1{,}800/3{,}000 = 0.6$; $IDF = \ln(1/0.6) = 0.5108$; $TF\text{-}IDF = 0.16667 \times 0.5108 = 0.0851$ (V1 p.328).
> B is TF alone; C is IDF alone.
> Q10: A.
> Statement 1 is correct: IDF is $\ln(1/DF)$ and DF is lower for "surg" (V1 p.328).
> Statement 2 is correct: with the same proportions DF is unchanged, and IDF depends only on DF, "its meaning is not directly related to the size of the corpus" (V1 p.328).
> Statement 3 is wrong: the case study uses TF, not TF-IDF, precisely because the documents are sentences, and TF-IDF varies with document count (V1 p.329).
> B and C therefore misjudge Statement 3 or Statement 1.

## Flashcards

#flashcards/cfa-l2/01-Quantitative-Methods/lm07

Big data's 3Vs plus the fourth V for inference::Volume, variety, velocity; veracity (credibility and reliability) (V1 p.276, p.277)

Estimated share of social media content that is completely fake::10% to 15%; web spam is over 20% of web content (V1 p.277)

Five structured ML model building steps in order::Conceptualization, data collection, data preparation and wrangling, data exploration, model training (V1 p.278)

Five text ML model building steps in order::Text problem formulation, data (text) curation, text preparation and wrangling, text exploration, model training (V1 p.278, p.279)

What does text curation involve?::Gathering external text via web services or web spidering (scraping, crawling) programs, plus expert annotation of target labels for supervised learning (V1 p.278)

Two tasks of data preparation and wrangling::Cleansing (identify and mitigate errors in raw data) and preprocessing (transform and scale the cleansed data) (V1 p.282)

Six structured data error types::Incompleteness, invalidity, inaccuracy, inconsistency, non-uniformity, duplication (V1 p.283)

{{Invalidity}} is a value outside a meaningful range; {{inaccuracy}} is a value that is not the true value; {{inconsistency}} is a conflict with corresponding data points or reality (V1 p.283)

Dates in mixed formats and an ambiguous dollar symbol are which error?::Non-uniformity (V1 p.283)

Five preprocessing transformations::Extraction, aggregation, filtration, selection, conversion (V1 p.284, p.285)

Creating an age variable from a date of birth or a ratio from two columns is::Extraction (V1 p.284, p.288)

Removing rows not needed versus removing columns not needed::Filtration removes rows; selection removes columns (V1 p.284)

Outlier rule for normal data::More than 3 standard deviations from the mean (V1 p.285)

IQR outlier bounds::Above Q3 + 1.5 IQR or below Q1 - 1.5 IQR; 3.0 IQR marks extreme values (V1 p.285)

Trimming versus winsorization::Trimming removes outliers (5% trimmed drops top and bottom 5%); winsorization replaces them with the largest and smallest non-outlier values (V1 p.285)

Normalization formula and range::(X - Xmin) / (Xmax - Xmin), range [0, 1], sensitive to outliers, usable when distribution unknown (V1 p.286)

Standardization formula and assumption::(X - mean) / standard deviation, mean 0 and sd 1, less outlier-sensitive, requires normal distribution (V1 p.286)

Four text cleansing operations::Remove html tags, remove punctuation (with annotations for meaningful marks), remove numbers (or /number/), remove white space (V1 p.289, p.290)

Punctuation that should be annotated rather than deleted::Percent signs, currency symbols, question marks (/percentSign/, /dollarSign/, /questionMark/); sentence periods become /endSentence/ (V1 p.289)

Four text normalization operations::Lowercasing, stop word removal, stemming, lemmatization (V1 p.291)

Stemming versus lemmatization::Stemming is rule-based and gives a stem that may not be a word ("analyz"); lemmatization is algorithmic and gives the morphological root ("analyze"), more expensive (V1 p.291)

What is data sparseness and what reduces it?::Many unique low-frequency tokens; stemming and lemmatization aggregate them into stems or lemmas (V1 p.292)

Bag-of-words definition and limitation::Distinct set of tokens from all texts; ignores word position and sequence (V1 p.292)

Document term matrix rows, columns, cells::Rows are documents, columns are BOW tokens, cells hold counts or TF values (V1 p.292)

Why are n-grams needed?::BOW drops "no" and loses "no market"; bigrams like no_market and not_good keep negation intact (V1 p.293, p.329)

Three tasks of data exploration::Exploratory data analysis, feature selection, feature engineering (V1 p.296)

Feature selection versus dimensionality reduction::Selection includes or excludes existing features unchanged; reduction creates new uncorrelated combinations (V1 p.300)

One hot encoding::Converting a categorical variable into binary 0/1 columns, one per level (V1 p.300)

Where does noise sit in a token frequency distribution?::Both ends: highest-TF stop words cause underfitting, lowest-TF sparse terms cause overfitting (V1 p.302)

Three feature selection methods for text::Frequency measures (TF, DF), chi-square test of token and class independence, mutual information (0 if same across classes, toward 1 if concentrated in one) (V1 p.302, p.303)

Four text feature engineering techniques::Number tokens by length (/number4/), n-grams, name entity recognition, parts of speech tagging (V1 p.303, p.304)

Three tasks of model training::Method selection, performance evaluation, tuning (V1 p.308)

Three factors governing method selection::Supervised or unsupervised, type of data, size of data (V1 p.310, p.311)

SVM suits which dataset shape, neural networks which?::SVM suits wider data (10,000 to 100,000 features, few instances); NNs suit longer data (instances far exceed features) (V1 p.311)

Recommended split of the master dataset::Training 60%, cross-validation 20%, test 20%; no split for unsupervised learning (V1 p.311)

Two fixes for class imbalance::Randomly undersample the majority class or oversample the minority class (V1 p.311)

Three performance evaluation techniques::Error analysis (confusion matrix), ROC curve with AUC, RMSE (V1 p.312 to p.315)

FP and FN as Type I and Type II::FP is Type I error, FN is Type II error (V1 p.312)

Precision formula and when to use it::TP / (TP + FP); when the cost of a false positive is high (V1 p.313)

Recall formula and when to use it::TP / (TP + FN), also sensitivity and TPR; when the cost of a false negative is high (V1 p.313)

Accuracy formula and when appropriate::(TP + TN) / (TP + FP + TN + FN); balanced classes (V1 p.313, p.314)

F1 formula and when preferred::2PR / (P + R), harmonic mean; unequal class distribution, equal weight to FP and FN (V1 p.313)

30-second drill: TP 3, FP 1, FN 2, TN 4::P 0.75, R 0.60, F1 0.6667, accuracy 0.70; keystrokes 2 x 0.75 x 0.6 = 0.9, divided by 1.35 (V1 p.314)

ROC axes and AUC benchmarks::x-axis FPR = FP / (TN + FP), y-axis TPR = TP / (TP + FN); AUC near 1.0 near-perfect, 0.5 random guessing, more convex is better (V1 p.314, p.315)

Parameters versus hyperparameters::Parameters are learned from training data (coefficients, weights, support vectors); hyperparameters are set manually and not data-dependent (lambda, layers, trees, k, p-threshold) (V1 p.316)

Diagnosis from training and CV error::High training error means underfitting and bias; CV error much higher than training error means overfitting and variance (V1 p.316)

What is grid search?::Training over combinations of hyperparameter values, cross-validating each, and picking the combination with close and small training and CV errors (V1 p.316)

Slight versus large regularization on the fitting curve::Slight: small training error, large CV error, high variance, overfitting; large: both errors large, high bias, underfitting (V1 p.317)

Financial Phrase Bank counts used in the case::2,180 sentences from 14,780; 1,457 positive, 723 negative; cross-sectional data (V1 p.319)

Why were stop words kept at normalization in the case?::"not", "more", "very", "few" carry sentiment; custom stop words were found later by frequency analysis (V1 p.321, p.327)

Custom stop word cut-offs in the case::14 words above the 99.5th TF percentile removed, 714 words below the 30th percentile removed, plus single characters (V1 p.327, p.329)

IDF formula and worked value for DF 0.6665::ln(1 / DF) = ln(1 / 0.6665) = 0.4057 (V1 p.328)

TF-IDF uses which TF?::Sentence-level TF times IDF; high value means frequent in few documents (V1 p.328)

Why TF rather than TF-IDF in the case DTM?::Documents are single sentences, and TF-IDF varies with the number of documents (V1 p.329)

AUCs before and after LASSO in the case::96.5% training and 86.2% CV before (overfit); 95.7% and 94.8% after (good fit) (V1 p.334, p.335)

Final threshold and CV metrics in the case::p = 0.60; precision 0.90, recall 0.98, F1 0.94, accuracy 0.91 (V1 p.338)

Test set metrics in the case::Precision 0.89, recall 0.98, F1 0.93, accuracy 0.90, similar to CV so not overfitting (V1 p.340)

Sentiment meaning of FP and FN::FP buys a stock whose sentiment is actually negative; FN avoids or shorts a stock whose sentiment is actually positive (V1 p.342)

Which answer is the trap when asked for precision from TP 182, FP 52, FN 31, TN 96?::81% (the F1) and 85% (the recall) are traps; precision is 182 / 234 = 78% (V1 p.355)

Bias and variance belong to which training task?::Tuning, not performance evaluation (V1 p.316, p.362)

## Common mistakes

1. Placing text preparation and wrangling second in the text pipeline; curation is second, preparation third, exploration fourth in both pipelines (V1 p.278, p.354).
2. Calling the cleansing and conversion of text to a structured format "curation"; curation is gathering the raw text (V1 p.278, p.356).
3. Answering velocity for a concern about fake accounts; reliability of the source is veracity (V1 p.277, p.354).
4. Confusing inaccuracy (a knowable value recorded wrongly or as unknown) with invalidity (a value outside any meaningful range) and inconsistency (two fields that contradict each other) (V1 p.283, p.287, p.354).
5. Labelling the creation of an age or ratio variable as conversion or aggregation; it is extraction, and deleting a column is selection, not feature selection (V1 p.284, p.354).
6. Standardizing when the vignette says normalize, or forgetting to subtract the minimum: $(1.2 - 0.2)/(12.2 - 0.2) = 0.083$, not $1.2/12.2$ (V1 p.286, p.354).
7. Removing all punctuation and numbers blindly; percent and currency signs need annotations, and numbers must be kept for information extraction (V1 p.289, p.290, p.355).
8. Treating tokenization as cleansing or as character-level; it is the first wrangling step and is usually at word level (V1 p.291, p.295).
9. Removing only high-frequency tokens after a frequency analysis; the rare tail causes overfitting and must go too (V1 p.302, p.357).
10. Writing IDF as 1/DF without the log, or multiplying collection-level TF instead of sentence-level TF (V1 p.328, p.359).
11. Reporting precision, recall, F1 or accuracy for the wrong ratio; all four are answer choices in the same question and the denominators differ (V1 p.313, p.355).
12. Using accuracy as the overall measure on an imbalanced dataset, or choosing F1 when the client has stated an asymmetric FP or FN cost (V1 p.314, p.359, p.360).
13. Reading the highest training AUC as the best model; the best fit has high and close training and CV AUCs, and a gap means overfitting fixed by regularization (V1 p.334, p.358).
14. Splitting an unlabelled dataset 60:20:20; unsupervised learning needs no split (V1 p.311, p.359).
15. Assigning bias and variance to performance evaluation; the evaluation techniques are error analysis, ROC and RMSE, and bias and variance are the tuning diagnosis (V1 p.312, p.316, p.362).
16. Oversampling the majority class to fix imbalance; undersample the majority or oversample the minority (V1 p.311, p.357).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "01-07" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
