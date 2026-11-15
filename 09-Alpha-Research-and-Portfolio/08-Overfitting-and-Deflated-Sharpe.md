---
type: concept
track: [quant-research]
tier: core
status: solid
prereqs: [backtesting-methodology-and-pitfalls, hypothesis-testing-and-multiple-comparisons]
est_hours: 4
sources: [Bailey and Lopez de Prado (2014) - The Deflated Sharpe Ratio - Journal of Portfolio Management 40(5) 94-107, Bailey and Lopez de Prado (2012) - The Sharpe Ratio Efficient Frontier - Journal of Risk 15(2) 3-44, Bailey Borwein Lopez de Prado and Zhu (2017) - The Probability of Backtest Overfitting - Journal of Computational Finance 20(4), Bailey Borwein Lopez de Prado and Zhu (2014) - Pseudo-Mathematics and Financial Charlatanism - Notices of the AMS 61(5) 458-471, Harvey and Liu (2015) - Backtesting - Journal of Portfolio Management 42(1) 13-28, Harvey Liu and Zhu (2016) - and the Cross-Section of Expected Returns - Review of Financial Studies 29(1) 5-68, Lopez de Prado - Advances in Financial Machine Learning (2018) ch 11 12 14, Lo (2002) - The Statistics of Sharpe Ratios - Financial Analysts Journal 58(4) 36-52, Mertens (2002) - Variance of the IID Estimator in Lo (2002) - working paper University of Basel]
---

# Overfitting, Deflated Sharpe and Multiple Testing

## TL;DR

- Selecting the best of $N$ backtests inflates its Sharpe: under the null the expected maximum is $\sqrt{V}\,[(1-\gamma)\Phi^{-1}(1-1/N) + \gamma\Phi^{-1}(1-1/(Ne))]$, with $V$ the cross-trial variance of Sharpe estimates.
- The probabilistic Sharpe ratio $\text{PSR}(SR^*) = \Phi\big[(\widehat{SR}-SR^*)\sqrt{T-1}/\sqrt{1-\hat\gamma_3\widehat{SR}+\tfrac{\hat\gamma_4-1}{4}\widehat{SR}^2}\big]$ corrects for sample length, skewness and kurtosis; the deflated Sharpe ratio is PSR with $SR^*$ set to that expected maximum.
- The probability of backtest overfitting (PBO) from CSCV is the fraction of train/test splits in which the in-sample winner ranks at or below the out-of-sample median; about 0.5 means selection is worthless.
- Combinatorial purged cross-validation with $N$ groups and $k$ test groups gives $\binom{N}{k}$ splits and $\binom{N-1}{k-1}$ full backtest paths, so you get a distribution of Sharpes, not one.
- Harvey-Liu haircut: convert Sharpe to a $p$-value, adjust for $M$ tests (Bonferroni, Holm, BHY), convert back; haircuts are large for marginal Sharpes and small for strong ones, not a flat 50%.
- Minimum backtest length: with 5 years of data, about 45 independent trials already make an annualised Sharpe of 1 the expected best result under pure noise.

## Learning objectives

- Compute the deflated Sharpe ratio and the probability of backtest overfitting.
- Use combinatorially purged cross-validation.
- Apply multiple-testing haircuts to reported Sharpe ratios.

## Core concepts

### Why the best backtest is biased

Let $\widehat{SR}_1,\dots,\widehat{SR}_N$ be Sharpe estimates from $N$ independent trials whose true Sharpe is zero, each approximately $N(0, V)$.
For iid standard normals $Z_n$, extreme value theory gives

$$
E\Big[\max_n Z_n\Big] \approx (1-\gamma)\,\Phi^{-1}\Big(1-\frac1N\Big) + \gamma\,\Phi^{-1}\Big(1-\frac{1}{N}e^{-1}\Big),
$$

with $\gamma \approx 0.5772$ the Euler-Mascheroni constant.
So the expected best Sharpe under the null is $\sqrt V$ times that bracket, which grows like $\sqrt{2\ln N}$ (bracket values: 1.57 at $N = 10$, 2.53 at $N = 100$, 3.26 at $N = 1000$).
In-sample Sharpe is therefore uninformative unless reported with $N$ and $V$, which is why the research log is mandatory ([Research Process and Hypothesis Discipline](01-Research-Process-and-Hypothesis-Discipline.md)).

### Probabilistic Sharpe ratio

For $T$ iid (not necessarily normal) returns with per-period Sharpe $SR$, skewness $\gamma_3$ and kurtosis $\gamma_4$ (normal $=3$), the estimator is asymptotically normal with variance

$$
\text{Var}(\widehat{SR}) \approx \frac{1 - \gamma_3 SR + \frac{\gamma_4 - 1}{4}SR^2}{T-1},
$$

the non-normal extension of Lo (2002) due to Mertens (2002), as quoted in Bailey and Lopez de Prado (2012, equation 8); for normal returns the numerator is $1 + SR^2/2$.
A simulation of 1,260 returns from a two-normal mixture with skewness $-1$ and kurtosis 6 at a daily Sharpe of 0.126 reproduces $(T-1)\text{Var}(\widehat{SR}) = 1.146$ and rejects the normal-returns value 1.008.
Bailey and Lopez de Prado (2012, equation 11) define the probability that the true Sharpe exceeds a benchmark $SR^*$:

$$
\widehat{\text{PSR}}(SR^*) = \Phi\left[\frac{(\widehat{SR} - SR^*)\sqrt{T-1}}{\sqrt{1 - \hat\gamma_3\widehat{SR} + \frac{\hat\gamma_4 - 1}{4}\widehat{SR}^2}}\right].
$$

Everything is in per-period units: $\widehat{SR}$ is the daily Sharpe if $T$ counts days.
Negative skew and fat tails widen the denominator and lower PSR, which is exactly the profile of short-volatility and carry strategies.

### Deflated Sharpe ratio

Bailey and Lopez de Prado (2014, equation 2) set the benchmark to the Sharpe you expect from the best of $N$ skill-less trials:

$$
SR_0 = \sqrt{V\big[\{\widehat{SR}_n\}\big]}\left[(1-\gamma)\Phi^{-1}\Big(1-\frac1N\Big) + \gamma\,\Phi^{-1}\Big(1-\frac1N e^{-1}\Big)\right], \qquad \text{DSR} = \widehat{\text{PSR}}(SR_0).
$$

Inputs, and how each is abused:

- $N$: the number of effectively independent trials; estimate it by clustering the trial return series, not by counting files.
- $V$: the variance of the Sharpe estimates across trials, in the same per-period units as $\widehat{SR}$.
- $T$, $\hat\gamma_3$, $\hat\gamma_4$: sample length and higher moments of the selected strategy.

DSR is a probability; a common bar is 0.95, read as "95% confidence the true Sharpe exceeds what selection alone would produce".

### Probability of backtest overfitting (CSCV)

Bailey, Borwein, Lopez de Prado and Zhu (2017) measure whether the selection procedure itself has out-of-sample value.
Combinatorially symmetric cross-validation (CSCV):

1. Form the $T \times N$ matrix of returns of all $N$ configurations tried.
2. Split the rows into $S$ contiguous blocks ($S$ even).
3. For each of the $\binom{S}{S/2}$ ways to choose half the blocks as the training set $J$ (complement $\bar J$ is the test set): find the in-sample winner $n^* = \arg\max_n SR_n(J)$, compute its relative rank $\bar\omega \in (0,1)$ among all $N$ configurations on $\bar J$, and the logit $\lambda = \ln\big(\bar\omega/(1-\bar\omega)\big)$.
4. $\text{PBO} = \Pr(\lambda \le 0)$, the fraction of splits in which the in-sample winner is at or below the out-of-sample median.

The paper writes the relative rank as $\bar\omega = \bar r/(N+1)$ with $\bar r$ the winner's out-of-sample rank, and PBO as $\int_{-\infty}^{0} f(\lambda)\,d\lambda$.

PBO near 0 means in-sample ranking carries over; near 0.5 means selection is noise; above 0.5 means the procedure systematically picks configurations that do worse than a random one out of sample.
The same machinery gives the regression of OOS on IS performance (performance degradation), the probability that the winner loses money out of sample, and a stochastic-dominance test.

### Combinatorial purged cross-validation (CPCV)

Walk-forward produces one historical path and one Sharpe.
CPCV (Lopez de Prado, *Advances in Financial Machine Learning*, chapter 12) splits the data into $N$ contiguous groups, uses every choice of $k$ groups as the test set with purging and embargo on the training side, giving $\binom{N}{k}$ splits.
Each group appears in $\binom{N-1}{k-1}$ test sets, so the test predictions can be stitched into

$$
\varphi[N, k] = \frac{k}{N}\binom{N}{k} = \binom{N-1}{k-1}
$$

complete out-of-sample backtest paths.
The output is a distribution of path Sharpes whose dispersion shows how much of the headline Sharpe is path luck.

### Multiple-testing haircuts (Harvey and Liu)

Harvey and Liu (2015) note that practitioners commonly discount backtested Sharpes by 50% as a rule of thumb, and replace that with a haircut derived from multiple testing: turn a Sharpe into a $t$-stat, adjust its $p$-value for the number of tests $M$, and convert back:

1. $t = \widehat{SR}_{\text{ann}}\sqrt{Y}$ for $Y$ years of iid returns (adjust for autocorrelation if needed); two-sided $p = 2(1-\Phi(t))$.
2. Adjusted $p$: Bonferroni $p^{M} = \min(Mp, 1)$; Holm is a step-down version that is uniformly more powerful; BHY (Benjamini-Hochberg-Yekutieli) controls the false discovery rate under arbitrary dependence, rejecting the $k$-th smallest of $M$ $p$-values when $p_{(k)} \le \frac{k}{M c(M)}\alpha$ with $c(M) = \sum_{j=1}^M 1/j$.
3. Haircut $t^{M} = \Phi^{-1}(1 - p^{M}/2)$, haircut Sharpe $= t^{M}/\sqrt Y$, haircut $= 1 - \widehat{SR}^{M}/\widehat{SR}$.

Harvey, Liu and Zhu (2016) apply this logic to the 316 factors they catalogue and conclude that a new factor needs a $t$-statistic greater than 3.0 rather than 2.0.
The general hypothesis-testing background is in [Hypothesis Testing and Multiple Comparisons](../02-Statistics-and-Econometrics/03-Hypothesis-Testing-and-Multiple-Comparisons.md).

### Minimum backtest length

If each annualised Sharpe estimate over $Y$ years is $N(0, 1/Y)$ under the null, the expected best of $N$ is $\text{bracket}(N)/\sqrt Y$.
Setting it equal to a target Sharpe $E[\max_N]$ and solving gives the minimum backtest length of Bailey, Borwein, Lopez de Prado and Zhu (2014, theorem 2):

$$
\text{MinBTL} \approx \frac{\big[(1-\gamma)\Phi^{-1}(1-\frac1N) + \gamma\Phi^{-1}(1-\frac1{Ne})\big]^2}{E[\max_N]^2} < \frac{2\ln N}{E[\max_N]^2}\ \text{years}.
$$

Below that length, a Sharpe of $E[\max_N]$ is what $N$ trials produce with no skill.

## Worked examples

### 1. Deflating a Sharpe of 2

A researcher ran $N = 100$ effectively independent trials; the annualised Sharpes across trials have standard deviation 0.5.
The winner has annualised Sharpe 2.0 over 5 years of daily data ($T = 1260$), skewness $-1$, kurtosis 6.

- Per-period units: $\widehat{SR} = 2/\sqrt{252} = 0.1260$ daily; $V = 0.25/252$, $\sqrt V = 0.0315$.
- Expected maximum bracket for $N = 100$: 2.531, so $SR_0 = 0.0315 \times 2.531 = 0.0797$ daily (1.27 annualised).
- Denominator: $\sqrt{1 + 1\times0.126 + \tfrac{5}{4}\times0.126^2} = 1.0704$.
- $z = (0.1260 - 0.0797)\sqrt{1259}/1.0704 = 1.534$, so $\text{DSR} = \Phi(1.534) = 0.938$.

Compare $\text{PSR}(0) = \Phi(4.18) \approx 1.0000$: the undeflated test calls it a certainty, the deflated one falls just short of 0.95.
With $N = 1000$, $SR_0$ rises to 1.63 annualised and DSR drops to 0.78; a winner with Sharpe 1.5 and $N = 100$ gets DSR 0.69.
The `bracket` and `psr` functions in the script compute all of these with the standard library's `NormalDist` (DSR 0.9375 at four decimals).
The bracket is itself an approximation: the exact expected maximum of 100 standard normals is 2.508, not 2.531, so $SR_0$ is about 1% conservative.

### 2. Harvey-Liu haircut

A strategy has annualised Sharpe 1.0 over 10 years.

- $t = 1.0\sqrt{10} = 3.16$, two-sided $p = 0.00157$.
- $M = 10$ tests, Bonferroni: $p^M = 0.0157$, $t^M = 2.42$, haircut Sharpe $= 2.42/\sqrt{10} = 0.76$, haircut 24%.
- $M = 100$: $p^M = 0.157$, $t^M = 1.42$, haircut Sharpe 0.45, haircut 55%.
- A Sharpe 2.0 strategy with $M = 100$: $t = 6.32$, $p = 2.5\times10^{-10}$, $p^M = 2.5\times10^{-8}$, $t^M = 5.57$, haircut Sharpe 1.76, haircut only 12%.
- A Sharpe 0.5 strategy: $t = 1.58$, $p = 0.114$, and with $M = 100$ the adjusted $p$ caps at 1: haircut 100%.

The haircut is nonlinear: marginal results are wiped out, strong ones barely touched.
Holm's adjusted $p$-value is never larger than Bonferroni's, so its haircut is never larger; BHY controls the false discovery rate instead, and its haircut depends on the whole set of $p$-values tested.

### 3. Minimum backtest length

Target: do not let noise produce an annualised Sharpe of 1.

- $N = 45$: bracket $= 2.236$, MinBTL $= 2.236^2/1 = 5.0$ years (bound $2\ln45 = 7.6$).
- $N = 100$: 6.4 years; $N = 1000$: 10.6 years.

So with 5 years of data, trying more than about 45 independent configurations makes a Sharpe of 1 the expected best result from pure noise; this is the paper's own example ("if only five years of data are available, no more than forty-five independent model configurations should be tried").

### 4. CPCV bookkeeping

$N = 6$ groups, $k = 2$ test groups: $\binom62 = 15$ train/test splits and $\varphi = \tfrac26\times15 = \binom51 = 5$ full backtest paths.
With $N = 10$, $k = 2$: 45 splits and 9 paths.
CSCV with $S = 16$ blocks evaluates $\binom{16}{8} = 12{,}870$ splits (the PBO paper prints 12,780, a typo); $S = 10$ gives 252.

### 5. PBO by simulation

```python
import numpy as np
from itertools import combinations

def pbo(M: np.ndarray, S: int = 10) -> float:
    """CSCV probability of backtest overfitting; M is a T x N matrix of returns of N configurations."""
    blocks = np.array_split(np.arange(M.shape[0]), S)
    sharpe = lambda x: x.mean(0) / x.std(0)
    logits = []
    for train in combinations(range(S), S // 2):
        test = [b for b in range(S) if b not in train]
        is_sr = sharpe(M[np.concatenate([blocks[b] for b in train])])
        oos_sr = sharpe(M[np.concatenate([blocks[b] for b in test])])
        n_star = np.argmax(is_sr)                    # in-sample winner
        rank = (oos_sr <= oos_sr[n_star]).sum()      # its OOS rank, 1 = worst
        w = rank / (M.shape[1] + 1)
        logits.append(np.log(w / (1 - w)))
    return float(np.mean(np.array(logits) <= 0))
```

With 50 pure-noise configurations over 1000 days and $S = 10$, PBO averaged 0.48 across 100 simulated datasets (the null expectation is 0.5), but individual datasets ranged from 0.10 to 0.96.
Adding a daily mean of 0.15 standard deviations (annualised Sharpe about 2.4) to one configuration dropped the average PBO to 0.08.
The script reproduces this with a seeded, block-statistics implementation of CSCV and checks that the snippet above returns identical values on the same data.
Lesson: PBO is itself a noisy statistic on one dataset; read it together with DSR and the OOS-versus-IS degradation plot.

## Pitfalls

- Computing DSR with annualised $\widehat{SR}$ but $T$ in days (or the reverse); every input must use the same period.
- Plugging excess kurtosis where the formula wants kurtosis ($\gamma_4 = 3$ for normal).
- Counting only "serious" trials in $N$, or counting near-duplicates as independent; both distort $SR_0$.
- Treating PSR against zero as a significance test for a selected strategy: it ignores the selection.
- Applying a flat 50% haircut to every Sharpe, which over-penalises strong results and under-penalises marginal ones.
- Using CSCV with blocks so short that autocorrelated returns leak across block boundaries.
- Believing PBO from a single dataset to two decimal places.
- Forgetting that the iid assumption behind all these formulas fails for autocorrelated returns; adjust $T$ or the Sharpe (Lo 2002) first.

## Interview questions

> [!question]- alpha-dsr-definition | What is the deflated Sharpe ratio?
> The probabilistic Sharpe ratio evaluated against the Sharpe expected from the best of $N$ skill-less trials.
> $\text{DSR} = \Phi\big[(\widehat{SR}-SR_0)\sqrt{T-1}/\sqrt{1-\hat\gamma_3\widehat{SR}+\tfrac{\hat\gamma_4-1}{4}\widehat{SR}^2}\big]$ with $SR_0 = \sqrt V\,[(1-\gamma)\Phi^{-1}(1-1/N)+\gamma\Phi^{-1}(1-1/(Ne))]$.

> [!question]- alpha-dsr-sr0-inputs | Which inputs set the DSR benchmark $SR_0$, and in what units?
> The number of effectively independent trials $N$ and the variance $V$ of Sharpe estimates across trials.
> Both are in the same per-period units as $\widehat{SR}$ and $T$; mixing annualised Sharpe with daily $T$ is the most common error.

> [!question]- alpha-dsr-psr-formula | Write the probabilistic Sharpe ratio and say what the skew and kurtosis terms do.
> $\text{PSR}(SR^*) = \Phi\big[(\widehat{SR}-SR^*)\sqrt{T-1}/\sqrt{1-\hat\gamma_3\widehat{SR}+\tfrac{\hat\gamma_4-1}{4}\widehat{SR}^2}\big]$.
> Negative skew and kurtosis above 3 inflate the standard error of $\widehat{SR}$, so the same Sharpe earns lower confidence for crash-prone strategies.

> [!question]- alpha-dsr-euler-mascheroni | What is the approximate expected maximum of $N$ iid standard normals used in the DSR?
> $(1-\gamma)\Phi^{-1}(1-1/N)+\gamma\Phi^{-1}(1-1/(Ne))$ with $\gamma \approx 0.5772$.
> It is about 1.57 for $N=10$, 2.53 for $N=100$ and 3.26 for $N=1000$, growing like $\sqrt{2\ln N}$.

> [!question]- alpha-dsr-example-100-trials | Best of 100 trials: annualised Sharpe 2.0, 5 years daily, cross-trial Sharpe sd 0.5, skew $-1$, kurtosis 6. DSR?
> About 0.94.
> $SR_0 = 0.0315\times2.531 = 0.0797$ daily (1.27 annualised), $z = (0.1260-0.0797)\sqrt{1259}/1.0704 = 1.53$, $\Phi(1.53) = 0.94$.

> [!question]- alpha-pbo-definition | Define the probability of backtest overfitting from CSCV.
> The fraction of combinatorial train/test splits in which the in-sample best configuration ranks at or below the median out of sample.
> Each split's winner gets relative OOS rank $\bar\omega$ and logit $\lambda = \ln(\bar\omega/(1-\bar\omega))$; $\text{PBO} = \Pr(\lambda\le0)$.

> [!question]- alpha-pbo-interpret | PBO comes out at 0.5. What does that mean?
> In-sample selection has no out-of-sample value: the winner is as likely to be below the OOS median as above it.
> A skilful procedure gives PBO near 0; above 0.5 the procedure systematically selects configurations worse than random.

> [!question]- alpha-cpcv-paths | CPCV with 6 groups and 2 test groups: how many splits and how many backtest paths?
> 15 splits and 5 paths.
> Splits $= \binom62 = 15$; paths $= \tfrac{k}{N}\binom Nk = \binom{N-1}{k-1} = 5$.

> [!question]- alpha-haircut-procedure | Describe the Harvey-Liu Sharpe haircut procedure.
> Sharpe to $t$-stat to $p$-value, adjust the $p$-value for $M$ tests, then back to $t$ and Sharpe.
> $t = SR\sqrt{Y}$, Bonferroni $p^M = \min(Mp,1)$ (or Holm, BHY), $t^M = \Phi^{-1}(1-p^M/2)$, haircut Sharpe $= t^M/\sqrt Y$.

> [!question]- alpha-haircut-example | Sharpe 1.0 over 10 years, 100 tests, Bonferroni. Haircut Sharpe?
> About 0.45, a 55% haircut.
> $t = 3.16$, $p = 0.00157$, $p^M = 0.157$, $t^M = 1.42$, $1.42/\sqrt{10} = 0.45$.

> [!question]- alpha-haircut-nonlinear | Why is a flat 50% Sharpe haircut wrong?
> Multiple-testing haircuts are nonlinear in the Sharpe.
> With $M = 100$ over 10 years, Sharpe 2.0 is haircut only 12% while Sharpe 1.0 is haircut 55% and Sharpe 0.5 is wiped out; Harvey and Liu (2015) call the 50% haircut only a rule of thumb for this reason.

> [!question]- alpha-hlz-t3 | What $t$-stat hurdle do Harvey, Liu and Zhu propose for new equity factors, and why?
> About 3.0.
> Harvey, Liu and Zhu (2016) catalogue 316 factors tested on largely the same data, and adjusting for that many tests (Bonferroni, Holm, BHY) pushes the significance threshold well above the single-test 2.0.

> [!question]- alpha-minbtl | With 5 years of data, how many independent trials make a Sharpe of 1 the expected best from pure noise?
> About 45.
> Bailey et al.'s approximation to the expected max of 45 standard normals, $(1-\gamma)\Phi^{-1}(1-1/N) + \gamma\Phi^{-1}(1-1/(Ne))$, is 2.236 (simulation gives 2.21), and $2.236/\sqrt5 = 1.0$; this is their minimum backtest length argument.

> [!question]- alpha-dsr-vs-psr0 | Why is PSR against zero the wrong test for a strategy chosen from many?
> It treats the winner as if it were the only strategy tested.
> Under selection even zero-skill strategies produce a maximum Sharpe well above zero; DSR replaces the zero benchmark with that expected maximum.

> [!question]- alpha-dsr-more-trials | The DSR example (annualised Sharpe 2.0, 5 years daily, cross-trial sd 0.5, skew $-1$, kurtosis 6) used $N = 100$. What happens with $N = 1000$?
> DSR falls from 0.94 to about 0.78.
> The bracket grows from 2.531 to 3.255, so $SR_0$ rises from 1.27 to 1.63 annualised and the gap to the observed 2.0 shrinks.

> [!question]- alpha-haircut-holm-vs-bonferroni | For the same set of tests, can Holm's haircut ever exceed Bonferroni's?
> No.
> Holm multiplies the $k$-th smallest $p$-value by $M - k + 1 \le M$ (then enforces monotonicity), so its adjusted $p$-value is never above Bonferroni's $Mp$ and its haircut is never larger.

## In this repo and The-Distinguished-Engineer

- Code: [`code/alpha_08_deflated_sharpe.py`](code/alpha_08_deflated_sharpe.py) prints and asserts every number on this page: the Euler-Mascheroni bracket against quadrature and simulation, the non-normal Sharpe variance by simulating a skewed fat-tailed mixture, DSR and PSR with the standard library, Harvey-Liu haircuts with $p$-values from `math.erfc` and $t$-stats by bisection, MinBTL by direct search over $N$, CPCV paths by enumerating and stitching every split, and PBO by a block-statistics CSCV that must equal the snippet above.
- Related notes: [Research Process and Hypothesis Discipline](01-Research-Process-and-Hypothesis-Discipline.md), [Backtesting Methodology and Pitfalls](07-Backtesting-Methodology-and-Pitfalls.md), [Performance Metrics and the Fundamental Law](09-Performance-Metrics-and-Fundamental-Law.md), [Order Statistics and Extremes](../01-Probability/08-Order-Statistics-and-Extremes.md).

## Further reading

- David H. Bailey and Marcos Lopez de Prado, "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality", *Journal of Portfolio Management* 40(5) (2014), 94-107.
- David H. Bailey and Marcos Lopez de Prado, "The Sharpe Ratio Efficient Frontier", *Journal of Risk* 15(2) (2012), 3-44 (PSR, the Mertens variance and minimum track record length).
- David H. Bailey, Jonathan Borwein, Marcos Lopez de Prado and Qiji Jim Zhu, "The Probability of Backtest Overfitting", *Journal of Computational Finance* 20(4) (2017).
- David H. Bailey, Jonathan Borwein, Marcos Lopez de Prado and Qiji Jim Zhu, "Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance", *Notices of the AMS* 61(5) (2014), 458-471.
- Campbell R. Harvey and Yan Liu, "Backtesting", *Journal of Portfolio Management* 42(1) (2015), 13-28.
- Campbell R. Harvey, Yan Liu and Heqing Zhu, "... and the Cross-Section of Expected Returns", *Review of Financial Studies* 29(1) (2016), 5-68.
- Andrew W. Lo, "The Statistics of Sharpe Ratios", *Financial Analysts Journal* 58(4) (2002), 36-52.
- Marcos Lopez de Prado, *Advances in Financial Machine Learning* (2018), chapters 11, 12 and 14.
