"""Text signals for finance in numpy: dictionary tone, tf-idf, document similarity, embeddings and timestamp leakage.

Backs 10-Machine-Learning-for-Finance/09-NLP-and-LLMs-for-Finance.md.

1. Dictionary tone on a toy sentence with a finance word list and a general-purpose list that also flags
   "liability" and "tax" (the misclassification Loughran and McDonald 2011 document).
2. Tf-idf by hand on a three-document corpus and cosine similarity (checked against a hand-derived closed form, plus
   a log-base invariance check); year-over-year filing similarity with raw and sublinear (1 + ln tf) term weights.
3. Near-duplicate headlines by Jaccard similarity of word sets.
4. Random high-dimensional embeddings are nearly orthogonal: sd of cosine about 1/sqrt(d).
5. Exponentially decayed aggregation of news sentiment.
6. Timestamp leakage: the same news signal backtested with date-level alignment (trades before the news) and with
   publication-time alignment (trades after it). Only the alignment differs between the two runs; simulated IC and
   Sharpe are compared with their closed forms.

Run: uv run --no-project --with numpy python 10-Machine-Learning-for-Finance/code/text_signals.py
"""

from __future__ import annotations

import math
from collections import Counter

import numpy as np


def check(label: str, value: float, expected: float, tol: float, fmt: str = ".4f") -> float:
    """Print a result and assert it matches the literal the note quotes, to tolerance and to printed rounding."""
    printed = f"{value:{fmt}}"
    print(f"{label} = {printed}")
    quoted = f"{expected:{fmt}}"
    assert abs(value - expected) <= tol + 1e-12, f"{label}: got {value}, expected {expected} +/- {tol}"
    assert printed.lstrip("-") == quoted.lstrip("-") or printed == quoted, f"{label}: prints {printed}, note quotes {quoted}"
    return value


def tokens(text: str) -> list[str]:
    return [w.strip(".,;:").lower() for w in text.split()]


# ---------------------------------------------------------------------------
# 1. Dictionary tone
# ---------------------------------------------------------------------------

# Toy word lists for illustration only (not the published dictionaries).
FIN_POS = {"exceeded", "improved", "strong", "growth"}
FIN_NEG = {"impairment", "litigation", "decline", "loss"}
GENERAL_NEG = FIN_NEG | {"liability", "tax"}  # a general-purpose list that also flags ordinary accounting words


def tone(words: list[str], pos: set[str], neg: set[str]) -> tuple[float, float]:
    """Tone (P - N)/(P + N), positive = bullish, defined as 0 when no listed word appears; and the negative share."""
    p = sum(w in pos for w in words)
    n = sum(w in neg for w in words)
    return ((p - n) / (p + n) if p + n else 0.0), n / len(words)


def section_dictionary() -> None:
    # Backs: Worked example 1; cards ml-nlp-lm-dictionary, ml-nlp-tone-calc.
    print("\n== 1. Dictionary tone ==")
    sentence = "Revenue growth exceeded guidance and margins improved, while the tax liability rose and one impairment was recorded."
    words = tokens(sentence)
    check("words in the sentence", len(words), 17, 0, ".0f")
    t_fin, neg_fin = tone(words, FIN_POS, FIN_NEG)
    t_gen, neg_gen = tone(words, FIN_POS, GENERAL_NEG)
    check("tone (pos - neg)/(pos + neg), finance list", t_fin, 0.50, 1e-12, ".2f")
    check("tone, general-purpose list", t_gen, 0.00, 5e-3, ".2f")
    check("negative-word share, finance list", neg_fin, 0.059, 5e-4, ".3f")
    check("negative-word share, general-purpose list", neg_gen, 0.176, 5e-4, ".3f")


# ---------------------------------------------------------------------------
# 2. Tf-idf and cosine similarity
# ---------------------------------------------------------------------------


def tfidf(docs: list[list[str]], log=np.log) -> tuple[list[str], np.ndarray, np.ndarray]:
    """Raw term count times log(N / df); returns the vocabulary, the idf vector (counted from the corpus) and weights."""
    vocab = sorted({w for d in docs for w in d})
    n = len(docs)
    df = np.array([sum(w in d for d in docs) for w in vocab])
    idf = log(n / df)
    tf = np.array([[Counter(d)[w] for w in vocab] for d in docs], dtype=float)
    return vocab, idf, tf * idf


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(a @ b / math.sqrt(float(a @ a) * float(b @ b)))


def section_tfidf() -> None:
    # Backs: Worked examples 2 and 3; cards ml-nlp-tfidf, ml-nlp-cosine-topic, ml-nlp-idf-base.
    print("\n== 2. Tf-idf and similarity ==")
    docs = [
        tokens("guidance raised on strong demand"),
        tokens("guidance cut on weak demand"),
        tokens("dividend raised on strong cash flow"),
    ]
    vocab, idf, w = tfidf(docs)
    col = {v: i for i, v in enumerate(vocab)}
    # idf values are counted from the corpus by tfidf(); the literals are ln(3/3), ln(3/2) and ln(3/1).
    check("idf of 'on' (in all 3 docs)", idf[col["on"]], 0.000, 1e-12, ".3f")
    check("idf of 'guidance' (2 of 3 docs)", idf[col["guidance"]], 0.405, 5e-4, ".3f")
    check("idf of 'cut' (1 of 3 docs)", idf[col["cut"]], 1.099, 5e-4, ".3f")
    check("tf-idf weight of 'cut' in doc 2", w[1, col["cut"]], 1.099, 5e-4, ".3f")
    check("cosine(doc 1, doc 2), tf-idf", cosine(w[0], w[1]), 0.245, 5e-4, ".3f")
    check("cosine(doc 1, doc 3), tf-idf", cosine(w[0], w[2]), 0.204, 5e-4, ".3f")
    # Closed form for cos(1, 2): doc 1 has four terms of weight ln 1.5; doc 2 shares two of them and adds two of weight ln 3.
    a, b = math.log(1.5), math.log(3.0)
    check(
        "cosine(doc 1, doc 2), closed form 2a^2 / sqrt(4a^2 (2a^2 + 2b^2))",
        2 * a * a / math.sqrt(4 * a * a * (2 * a * a + 2 * b * b)),
        0.245,
        5e-4,
        ".3f",
    )
    # Changing the log base multiplies every idf by the same constant, so tf-idf cosines do not change (card ml-nlp-idf-base).
    _, _, w10 = tfidf(docs, log=np.log10)
    check("cosine(doc 1, doc 2), tf-idf with log base 10", cosine(w10[0], w10[1]), 0.245, 5e-4, ".3f")
    check(
        "max |cosine change| from switching ln to log10 over all pairs",
        max(abs(cosine(w[i], w[j]) - cosine(w10[i], w10[j])) for i in range(3) for j in range(i + 1, 3)),
        0.0,
        1e-12,
        ".1f",
    )
    counts = np.array([[Counter(d)[v] for v in vocab] for d in docs], dtype=float)
    check("cosine(doc 1, doc 2), raw counts", cosine(counts[0], counts[1]), 0.600, 5e-4, ".3f")

    # Year-over-year filing similarity on term counts (toy risk-factor sections).
    last_year = tokens("we face competition and regulation and currency risk")
    this_year = tokens("we face competition and regulation and currency risk and litigation risk and supply risk")
    vocab2 = sorted(set(last_year) | set(this_year))
    a = np.array([Counter(last_year)[v] for v in vocab2], dtype=float)
    b = np.array([Counter(this_year)[v] for v in vocab2], dtype=float)
    check("filing similarity: dot product of term counts", float(a @ b), 16.0, 1e-12, ".0f")
    check("filing similarity: squared norm, last year", float(a @ a), 10.0, 1e-12, ".0f")
    check("filing similarity: squared norm, this year", float(b @ b), 32.0, 1e-12, ".0f")
    check("year-over-year cosine similarity of the risk section", cosine(a, b), 0.894, 5e-4, ".3f")
    # Sublinear tf (1 + ln count for count > 0) rescales terms unequally ("and" 2 -> 4, "risk" 1 -> 3), so the cosine moves
    # (card ml-nlp-idf-base); in the three headlines every count is 1, so there it would change nothing.
    a_sub = np.where(a > 0, 1 + np.log(np.where(a > 0, a, 1.0)), 0.0)
    b_sub = np.where(b > 0, 1 + np.log(np.where(b > 0, b, 1.0)), 0.0)
    check("year-over-year cosine with sublinear tf weights 1 + ln tf", cosine(a_sub, b_sub), 0.905, 5e-4, ".3f")
    check("max term count in the three headlines (so 1 + ln tf equals raw tf there)", float(counts.max()), 1.0, 0, ".0f")


# ---------------------------------------------------------------------------
# 3. Near duplicates
# ---------------------------------------------------------------------------


def jaccard(a: list[str], b: list[str]) -> float:
    sa, sb = set(a), set(b)
    return len(sa & sb) / len(sa | sb)


def section_near_duplicates() -> None:
    # Backs: Worked example 4; card ml-nlp-novelty.
    print("\n== 3. Near-duplicate headlines ==")
    h1 = tokens("Acme beats estimates and raises full-year guidance")
    h2 = tokens("Acme raises full-year guidance and beats estimates")
    h3 = tokens("Acme beats estimates but cuts full-year guidance")
    check("Jaccard(h1, h2): same story, reordered", jaccard(h1, h2), 1.00, 1e-12, ".2f")
    check("Jaccard(h1, h3): different news", jaccard(h1, h3), 0.56, 5e-3, ".2f")


# ---------------------------------------------------------------------------
# 4. Random embeddings
# ---------------------------------------------------------------------------


def section_embeddings() -> None:
    # Backs: Worked example 5; card ml-nlp-embedding-null.
    print("\n== 4. Random embeddings are nearly orthogonal ==")
    d = 768
    check("1/sqrt(768)", 1 / math.sqrt(d), 0.0361, 5e-5)
    rng = np.random.default_rng(10)
    a = rng.standard_normal((20_000, d))
    b = rng.standard_normal((20_000, d))
    cos = (a * b).sum(axis=1) / np.sqrt((a * a).sum(axis=1) * (b * b).sum(axis=1))
    check("sd of cosine between random 768-d vectors", float(cos.std()), 0.0360, 5e-5)
    check("99th percentile of |cosine|, random 768-d vectors", float(np.quantile(np.abs(cos), 0.99)), 0.093, 5e-4, ".3f")


# ---------------------------------------------------------------------------
# 5. Decayed aggregation
# ---------------------------------------------------------------------------


def section_decay() -> None:
    # Backs: Worked example 6; card ml-nlp-decay.
    print("\n== 5. Decayed news aggregation ==")
    half_life = 2.0  # days
    lam = math.log(2) / half_life
    items = [(0.0, 0.8), (3.0, -0.5)]  # (day, sentiment)
    at_day = 4.0
    score = sum(s * math.exp(-lam * (at_day - t)) for t, s in items)
    check("decayed sentiment on day 4, half-life 2 days", score, -0.154, 5e-4, ".3f")
    # Components by counting half-lives, 2^(-age / half-life), a different route from exp(-lambda age).
    old_item = items[0][1] * 0.5 ** ((at_day - items[0][0]) / half_life)
    new_item = items[1][1] * 0.5 ** ((at_day - items[1][0]) / half_life)
    check("day-0 item after 4 days (two half-lives): 0.8 * 0.5^2", old_item, 0.2, 1e-12, ".1f")
    check("day-3 item after 1 day (half a half-life): -0.5 * 0.5^0.5", new_item, -0.354, 5e-4, ".3f")
    assert abs(old_item + new_item - score) < 1e-12, "half-life counting and exp(-lambda t) decay disagree"


# ---------------------------------------------------------------------------
# 6. Timestamp leakage
# ---------------------------------------------------------------------------


def section_timestamp_leak() -> None:
    # Backs: Worked example 7 and TL;DR; cards ml-nlp-timestamp-leak, ml-nlp-ic-formula.
    print("\n== 6. Timestamp leakage ==")
    rng = np.random.default_rng(11)
    n = 20_000  # news items, each on its own stock-day
    s = rng.standard_normal(n)  # sentiment, known exactly at publication
    jump = 0.01 * s  # immediate price reaction at publication (1% per unit sentiment)
    drift = 0.001 * s  # slow post-news drift over the next trading day
    noise_same = 0.02 * rng.standard_normal(n)  # rest of the publication day's return
    noise_next = 0.02 * rng.standard_normal(n)  # rest of the next day's return
    ret_pub_day = jump + noise_same  # close before publication -> close of the publication day
    ret_next_day = drift + noise_next  # close of the publication day -> next close

    def stats(pos: np.ndarray, ret: np.ndarray) -> tuple[float, float]:
        pnl = pos * ret
        return float(np.corrcoef(pos, ret)[0, 1]), float(pnl.mean() / pnl.std() * math.sqrt(252))

    ic_naive, sr_naive = stats(s, ret_pub_day)  # date-level join: position taken at the prior close
    ic_pit, sr_pit = stats(s, ret_next_day)  # point in time: position taken after publication
    check("IC, date-level alignment (enters before the news)", ic_naive, 0.457, 5e-4, ".3f")
    check("IC, publication-time alignment", ic_pit, 0.046, 5e-4, ".3f")
    check("Sharpe of sentiment-weighted P&L per item times sqrt(252), date-level alignment", sr_naive, 6.6, 0.05, ".1f")
    check("annualised Sharpe, publication-time alignment", sr_pit, 0.7, 0.05, ".1f")
    check("theoretical IC, date-level: 0.01 / sqrt(0.01^2 + 0.02^2)", 0.01 / math.sqrt(0.01**2 + 0.02**2), 0.447, 5e-4, ".3f")
    check("theoretical IC, publication-time: 0.001 / sqrt(0.001^2 + 0.02^2)", 0.001 / math.sqrt(0.001**2 + 0.02**2), 0.050, 5e-4, ".3f")
    # P&L per item is s (a s + sigma e) with s, e ~ N(0, 1): mean a, variance a^2 Var(s^2) + sigma^2 = 2 a^2 + sigma^2.
    check(
        "theoretical Sharpe, date-level: 0.01 / sqrt(2 * 0.01^2 + 0.02^2) * sqrt(252)",
        0.01 / math.sqrt(2 * 0.01**2 + 0.02**2) * math.sqrt(252),
        6.5,
        0.05,
        ".1f",
    )
    check(
        "theoretical Sharpe, publication-time: 0.001 / sqrt(2 * 0.001^2 + 0.02^2) * sqrt(252)",
        0.001 / math.sqrt(2 * 0.001**2 + 0.02**2) * math.sqrt(252),
        0.8,
        0.05,
        ".1f",
    )
    # Sampling error of the per-item Sharpe estimate, scaled by sqrt(252): about sqrt(252 / n).
    # So simulated 6.6 vs 6.5 and 0.7 vs 0.8 are within one standard error.
    check("standard error of the annualised Sharpe estimate, sqrt(252 / 20000)", math.sqrt(252 / n), 0.11, 5e-3, ".2f")
    assert abs(sr_naive - 0.01 / math.sqrt(2 * 0.01**2 + 0.02**2) * math.sqrt(252)) < 2 * math.sqrt(252 / n)
    assert abs(sr_pit - 0.001 / math.sqrt(2 * 0.001**2 + 0.02**2) * math.sqrt(252)) < 2 * math.sqrt(252 / n)
    # Large-sample standard error of a correlation estimate: (1 - rho^2) / sqrt(n).
    ic_true_naive = 0.01 / math.sqrt(0.01**2 + 0.02**2)
    ic_true_pit = 0.001 / math.sqrt(0.001**2 + 0.02**2)
    se_naive = check("standard error of the IC estimate, date-level", (1 - ic_true_naive**2) / math.sqrt(n), 0.006, 5e-4, ".3f")
    se_pit = check("standard error of the IC estimate, publication-time", (1 - ic_true_pit**2) / math.sqrt(n), 0.007, 5e-4, ".3f")
    assert abs(ic_naive - ic_true_naive) < 2 * se_naive and abs(ic_pit - ic_true_pit) < 2 * se_pit


if __name__ == "__main__":
    section_dictionary()
    section_tfidf()
    section_near_duplicates()
    section_embeddings()
    section_decay()
    section_timestamp_leak()
    print("\nall checks passed")
