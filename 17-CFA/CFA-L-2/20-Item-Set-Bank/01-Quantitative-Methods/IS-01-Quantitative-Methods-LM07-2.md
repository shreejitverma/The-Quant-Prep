---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 7
title: "Kestrel Ridge Earnings Call Sentiment"
los: [los-01-07-g, los-01-07-e]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Kestrel Ridge Earnings Call Sentiment

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Kestrel Ridge Capital is an event-driven hedge fund that trades European industrial equities around earnings releases.
Portfolio manager Rhys Whitcombe wants a sentiment score for each earnings call to feed the fund's valuation model alongside consensus revisions.
Quantitative analyst Daniela Okafor is building the text classifier.

Okafor scraped 3,600 management sentences from transcript web pages, and two sector analysts labelled each sentence positive or negative.
A typical raw sentence reads: "Order intake rose 12.5% to EUR 1.2 mln in the third quarter."
Her cleansing procedure, applied in order, is:

- Step 1: strip all html tags.
- Step 2: delete every punctuation character.
- Step 3: expand "m", "mln" and "mn" to "million", then replace every number with the token /number/.
- Step 4: remove extra white space.

She then tokenizes at the word level, lowercases, replaces "EUR" and "USD" with "currencysign", and applies Porter's stemmer.
She deliberately does not remove a standard stop word list at this stage.
After normalization the corpus contains 71,280 tokens, and she builds unigrams and bigrams.

On 14 May, Whitcombe states, "Keeping stop words is a mistake.
They are the most frequent tokens, so you should have removed a standard stop word list during normalization, before any frequency analysis."

Exhibit 1 reports term frequency inputs for four tokens, all drawn from sentence 2,214, which contains 32 tokens after normalization.
Zeltwig AG is a small supplier mentioned by name in the sentence.

**Exhibit 1: Term frequency inputs (corpus of 3,600 sentences, 71,280 tokens)**

| Token | Occurrences in corpus | Occurrences in sentence 2,214 | Sentences containing token |
|---|---|---|---|
| the | 3,920 | 4 | 2,590 |
| guidanc | 410 | 2 | 372 |
| margin_expans | 61 | 1 | 58 |
| zeltwig | 2 | 1 | 2 |

Okafor fills the document term matrix with sentence-level term frequency values.
To prune noise, she will remove every token whose collection-level term frequency lies above the 99.5th percentile or below the 30th percentile of the distribution in Exhibit 2.

**Exhibit 2: Percentiles of collection-level term frequency**

| Percentile | Term frequency |
|---|---|
| 99.5th | 0.0095 |
| 50th | 0.00031 |
| 30th | 0.000042 |

On 16 May, Okafor makes two statements to Whitcombe:

- Statement 1: "Because each document is a single sentence, the document term matrix should hold term frequency values rather than TF-IDF values, which vary with the number of documents."
- Statement 2: "If we double the corpus to 7,200 sentences and 'guidanc' appears in 744 of them, its inverse document frequency will rise because the corpus is larger."

Finally, Okafor notices that "guide" is used both as a verb ("we guide to growth") and as a noun, and that the compound noun "order intake" is split into two unrelated unigram tokens.
She plans one further text feature engineering technique to address both problems.

## Questions

1. Okafor's cleansing procedure is most likely deficient because: (LOS: los-01-07-g)
   - A. deleting the percent sign in Step 2 discards meaning that should be kept as an annotation.
   - B. Step 2 turns "1.2" into "12" before Step 3, corrupting the numeric information.
   - C. Step 3 removes numbers that a sentiment classifier needs as inputs.
2. Is Whitcombe's 14 May statement correct? (LOS: los-01-07-g)
   - A. Yes, because stop words are high-frequency tokens that cause overfitting.
   - B. No, because words such as "not" and "few" carry sentiment, and uninformative high-frequency tokens are removed later by frequency cut-offs.
   - C. Yes, because Porter's stemmer cannot be applied until stop words have been removed.
3. The TF-IDF of "margin_expans" in sentence 2,214 is closest to: (LOS: los-01-07-e)
   - A. 0.004.
   - B. 0.129.
   - C. 1.940.
4. Which of Okafor's 16 May statements is correct? (LOS: los-01-07-g)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.
5. The text feature engineering technique that best addresses Okafor's final concern is: (LOS: los-01-07-e)
   - A. n-grams.
   - B. parts of speech tagging.
   - C. name entity recognition.
6. Applying Okafor's cut-offs to Exhibit 1, which tokens will be removed? (LOS: los-01-07-e)
   - A. "the" only.
   - B. "zeltwig" only.
   - C. Both "the" and "zeltwig".

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Most punctuation is removed, but percent signs, currency symbols and question marks carry meaning and should be replaced with annotations such as /percentSign/ before other punctuation is stripped, exactly as the case study did (V1 p.289, p.319, p.320).
> B is wrong because the "1.2" to "12" change is harmless here: Step 3 replaces every number with /number/, so the value never reaches the model (V1 p.290).
> C is wrong because numbers are kept only for information extraction; for classification their values rarely help and each distinct number would become its own sparse token (V1 p.290).
> 2. **B.** In the sentiment case, stop words were deliberately kept at normalization because words such as "not", "more", "very" and "few" carry sentiment; high-frequency noise was removed later through custom stop words set by collection frequency cut-offs (V1 p.321, p.327).
> A is wrong on two counts: the statement is incorrect, and the highest-frequency tokens cause underfitting, not overfitting, because they appear in every class (V1 p.302).
> C is wrong because stemming does not depend on stop word removal; the case study stemmed with stop words still present (V1 p.321).
> 3. **B.** Sentence-level $TF = 1/32 = 0.03125$.
> $DF = 58 / 3{,}600 = 0.016111$.
> $IDF = \ln(1 / 0.016111) = 4.1282$.
> $TF\text{-}IDF = 0.03125 \times 4.1282 = 0.1290$ (V1 p.328).
> A is wrong because it multiplies collection-level TF, $61 / 71{,}280 = 0.000856$, by IDF to get $0.0035$; TF-IDF uses sentence-level TF (V1 p.328, p.359).
> C is wrong because it omits the log, $0.03125 \times 62.069 = 1.9397$; IDF is the log of the inverse of DF (V1 p.328).
> 4. **A.** Statement 1 matches the case study, which used TF rather than TF-IDF in the DTM because the documents are single sentences and TF-IDF values vary with the number of documents (V1 p.329).
> Statement 2 is wrong: $DF = 744 / 7{,}200 = 0.1033$, identical to $372 / 3{,}600 = 0.1033$, so $IDF = \ln(1/0.1033) = 2.2698$ in both cases; IDF depends on the proportion of documents containing the token, not on corpus size (V1 p.328).
> B and C are wrong because each accepts Statement 2.
> 5. **B.** Parts of speech tagging labels tokens as nouns, verbs, adjectives and so on, which separates "guide" the verb from "guide" the noun, and it identifies compound nouns so that "order intake" becomes one token, as with "CFA Institute" (V1 p.304).
> A is wrong because Okafor already builds bigrams, and an n-gram can keep "order_intake" together but cannot tell the verb from the noun.
> C is wrong because name entity recognition tags object classes such as ORGANIZATION, MONEY and DATE; neither a verb nor a generic business term is a named entity (V1 p.303, p.304).
> 6. **C.** Collection-level TF equals corpus occurrences divided by 71,280.
> "the": $3{,}920 / 71{,}280 = 0.054994$, above the 99.5th percentile of 0.0095, so removed.
> "guidanc": $410 / 71{,}280 = 0.005752$, between the cut-offs, so kept.
> "margin_expans": $61 / 71{,}280 = 0.000856$, kept.
> "zeltwig": $2 / 71{,}280 = 0.0000281$, below the 30th percentile of 0.000042, so removed.
> High-TF tokens cause underfitting and sparse proper nouns cause overfitting, so both tails go (V1 p.302, p.327).
> A is wrong because it removes only the high tail.
> B is wrong because it removes only the low tail; note that "zeltwig" has the highest TF-IDF in the exhibit, $0.03125 \times \ln(3{,}600/2) = 0.03125 \times 7.4955 = 0.2342$, which is the trap: a rare name looks unique but lets the model classify on a name.

## Distractor design

1. B: sequence error that the later number step neutralises; C: confuses sentiment classification with information extraction.
2. A: right that the tokens are frequent but wrong fit error (overfitting instead of underfitting); C: invented dependency between normalization operations.
3. A: collection-level TF instead of sentence-level TF; C: IDF without the log.
4. B and C: assume IDF depends on corpus size rather than on the document proportion.
5. A: n-grams fix sequence but not word class; C: confuses POS tags with NER object classes.
6. A: removes only the stop-word tail; B: removes only the sparse tail, or is misled by the high TF-IDF of a rare name.
