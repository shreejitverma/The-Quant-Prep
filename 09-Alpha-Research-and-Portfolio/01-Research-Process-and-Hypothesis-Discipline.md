---
type: concept
track: [quant-research]
tier: core
status: solid
prereqs: []
est_hours: 3
sources: [Lopez de Prado - Advances in Financial Machine Learning (2018) ch 7 11 12, Isichenko - Quantitative Portfolio Management (2021) ch 2, Bailey and Lopez de Prado (2014) - The Deflated Sharpe Ratio - Journal of Portfolio Management 40(5), Harvey Liu and Zhu (2016) - and the Cross-Section of Expected Returns - Review of Financial Studies 29(1), Ioannidis (2005) - Why Most Published Research Findings Are False - PLoS Medicine 2(8), Harvey (2017) - The Scientific Outlook in Financial Economics - Journal of Finance 72(4)]
---

# Research Process and Hypothesis Discipline

## TL;DR

- A research idea is a falsifiable claim with an economic mechanism, a pre-registered test (universe, horizon, metric, threshold) and a kill criterion written down before the data is touched.
- Every variant you try is a draw from a noise distribution; with $N$ zero-skill variants the best in-sample Sharpe grows like $\sigma_{SR}\sqrt{2\ln N}$, so the research log (the count $N$) is part of the result.
- Low prior plus a loose threshold gives a mostly-false pipeline: with a 10% base rate, 80% power and $\alpha = 5\%$, 36% of "discoveries" are false; at $t > 3$ that falls to about 5%.
- Detecting Sharpe needs years: the $t$-stat of an annualised Sharpe $S$ over $Y$ years is roughly $S\sqrt{Y}$, so $S = 0.8$ needs about 6 years to reach $t = 2$ and 12 years for 80% power.
- Hold out a final test set you touch once, separate it in time, and never let its result feed back into the design.
- Kill ideas on pre-registered process rules (mechanism refuted, capacity, cost, data problems), not on one noisy live quarter.

## Learning objectives

- Frame research as falsifiable hypotheses with a pre-registered evaluation.
- Keep a research log of every variant tried to control selection bias.
- Decide when to kill an idea.

## Core concepts

### The research loop

A disciplined loop has five stages, and each stage has an artefact that someone else can audit.

1. **Hypothesis.** A one-paragraph statement of who is on the other side of the trade and why they accept a loss: risk premium, behavioural bias, structural constraint (index rebalancing, regulatory capital), or liquidity provision.
2. **Specification.** Universe, point-in-time data sources, signal definition, horizon, portfolio construction, cost model, the primary metric and the pass threshold, all written before looking at returns.
3. **Development sample.** Exploratory work, feature engineering and parameter choice, with every variant logged.
4. **Validation.** Walk-forward or purged cross-validation on data not used for selection ([Backtesting Methodology and Pitfalls](07-Backtesting-Methodology-and-Pitfalls.md)).
5. **Holdout and paper trading.** One look at a sealed period, then live paper trading or small capital, compared against a pre-stated tolerance band.

The mechanism matters because it tells you where the effect should and should not appear.
A behavioural under-reaction story predicts stronger effects in low-attention stocks and decay after publication; a risk-premium story predicts the effect loads on some bad-times state.
Those auxiliary predictions are cheap, independent tests: if the mechanism's side predictions fail, the headline result is probably noise.

### Falsifiability and pre-registration

A hypothesis is useful only if some outcome would refute it.
"Momentum works in some regime" is not falsifiable; "the 12-1 month cross-sectional momentum decile spread in US large caps has a positive mean excess return, $t > 3$, over 2005-2020 after 10 bp one-way costs" is.
Pre-registration fixes the researcher degrees of freedom (the choices that could otherwise be tuned to the data): lookback, skip period, universe filters, winsorisation, rebalance day, cost model and the metric.
Harvey (2017) calls tuning these after seeing the data "p-hacking"; the published $t$-stat is then conditional on a search it does not report.

### Selection bias from the search itself

Suppose you evaluate $N$ strategy variants, each with true Sharpe zero, on $Y$ years of data.
Each annualised Sharpe estimate is approximately $N(0, 1/Y)$, so the maximum of $N$ roughly independent estimates has mean

$$
E\Big[\max_n \widehat{SR}_n\Big] \approx \sqrt{\tfrac{1}{Y}}\Big[(1-\gamma)\Phi^{-1}\big(1-\tfrac1N\big) + \gamma\,\Phi^{-1}\big(1-\tfrac1{Ne}\big)\Big],
$$

with $\gamma \approx 0.5772$ the Euler-Mascheroni constant (Bailey and Lopez de Prado 2014).
The bracket grows like $\sqrt{2\ln N}$: 1.57 for $N=10$, 2.28 for $N=50$, 2.53 for $N=100$.
This is why the research log matters: the reported Sharpe is only interpretable next to the number of trials and the dispersion of their Sharpes, which are exactly the inputs of the deflated Sharpe ratio ([Overfitting and Deflated Sharpe](08-Overfitting-and-Deflated-Sharpe.md)).

What to log for every variant, including the ones that failed:

- A hash of the code and config, the data snapshot and the date run.
- The full return series (not just the Sharpe), so you can later compute correlations between trials and cluster them into effective independent trials.
- Why the variant was tried: a variant motivated by a previous result is not independent of it.

### Base rates: why most backtests are false

Treat each idea as a hypothesis test with prior probability $\pi$ of being real, significance level $\alpha$ and power $1-\beta$.
The fraction of "significant" results that are real (positive predictive value) is

$$
\text{PPV} = \frac{\pi(1-\beta)}{\pi(1-\beta) + (1-\pi)\alpha}.
$$

This is the argument of Ioannidis (2005), and Harvey, Liu and Zhu (2016) use the multiple-testing version of it to argue that new equity factors should clear $t > 3$ rather than $t > 2$.
Low priors are the norm in alpha research: most ideas are variations on crowded themes or pure data mining.
Two levers raise PPV: a stronger prior (a real mechanism, out-of-sample evidence in another market) and a stricter threshold.

### Statistical power and how long a test takes

For iid returns the $t$-statistic of mean excess return equals the annualised Sharpe times the square root of years: $t \approx S\sqrt{Y}$.
So the years needed to reach a critical value $c$ are $Y = (c/S)^2$, and for power $1-\beta$ at one-sided level $\alpha$ you need $Y = \big((z_{1-\alpha} + z_{1-\beta})/S\big)^2$.
Monthly-rebalanced equity factors with $S \approx 0.5$ need decades; this is why low-frequency researchers lean on cross-sectional breadth, multiple markets and economic priors, while high-frequency researchers can validate in weeks because their per-period Sharpe is high and $Y$ is effectively many independent days.

### Holdouts, and why they wear out

A holdout is valid only for its first use.
Once a holdout result changes a design decision, it has become part of the development sample and a new sealed period is needed.
Practical rules:

- Split in time, not randomly, and keep a gap (embargo) between development and holdout so overlapping labels do not leak.
- Prefer a holdout that is also out of domain (another region, another asset class) for mechanism tests.
- Track "holdout touches" in the log exactly like trials.

### When to kill an idea

Write kill criteria into the specification, in three families.

- **Evidence against the mechanism.** Side predictions fail, the effect lives entirely in microcaps or untradeable names, or it disappears once point-in-time data replaces restated data ([Point-in-Time Data and Survivorship](02-Point-in-Time-Data-and-Survivorship.md)).
- **Economics.** Net-of-cost Sharpe below the hurdle, capacity below the minimum the desk can run, or the signal is more than about 0.7 correlated with an existing book so its marginal contribution is small.
- **Live divergence.** A drawdown or tracking error band stated before launch, sized from the backtest distribution, not an ad hoc reaction to a bad month.

Because Sharpe estimates are so noisy over short windows (worked example 4), statistical evidence alone rarely justifies killing a strategy after a few months; process evidence (a data bug, a fill-model error, a crowding event) usually does.

## Worked examples

### 1. How many of your discoveries are real?

Setup: 10% of the ideas you test are real, your test has 80% power at $\alpha = 5\%$ two-sided.

- PPV at $t > 1.96$: $\frac{0.1 \times 0.8}{0.1\times0.8 + 0.9\times0.05} = \frac{0.080}{0.125} = 0.64$, so 36% of discoveries are false.
- Raise the bar to $t > 3$ ($\alpha = 0.0027$ two-sided).
  An effect with 80% power at 1.96 has non-centrality $\delta = 1.96 + 0.8416 = 2.80$, so power at 3 is $\Phi(2.80 - 3) = 0.421$.
- PPV at $t > 3$: $\frac{0.1\times0.421}{0.1\times0.421 + 0.9\times0.0027} = 0.945$.

Interview point: the stricter threshold roughly halves power but cuts the false discovery share from 36% to 5.5%; the cure for lost power is more data or better priors, not a looser threshold.

### 2. How long must a strategy run before you believe it?

Target: annualised Sharpe $S = 0.8$, iid returns.

- Years to reach $t = 2$: $Y = (2/0.8)^2 = 6.25$.
- Years for 80% power at one-sided 5%: $Y = \big((1.645 + 0.842)/0.8\big)^2 = 9.7$.
- Two-sided 5% with 80% power: $\big((1.960+0.842)/0.8\big)^2 = 12.3$ years.

For $S = 2$ the same power needs only about 1.5 to 2 years, which is why high-Sharpe, high-frequency strategies can be validated quickly and slow factors cannot.

### 3. The best of 50 random strategies

Setup: 50 variants, all with zero true Sharpe, evaluated on 5 years of daily data.

- Standard error of an annualised Sharpe estimate: $\sqrt{1/5} = 0.447$ (the $S^2/2$ term is zero at $S = 0$).
- Expected maximum of 50 standard normals: $(1-\gamma)\Phi^{-1}(0.98) + \gamma\Phi^{-1}(1 - 1/(50e)) = 2.276$ (simulation gives 2.25).
- Expected best Sharpe: $2.276 \times 0.447 = 1.02$.

A Sharpe of 1 after 50 unlogged tries on 5 years is exactly what pure noise produces.

```python
import numpy as np
rng = np.random.default_rng(0)
years, n_trials, n_sims = 5, 50, 20_000
sr_hat = rng.standard_normal((n_sims, n_trials)) / np.sqrt(years)  # annualised SR estimates, true SR = 0
print(sr_hat.max(axis=1).mean())  # about 1.01
```

### 4. Should we kill it after six bad months?

Setup: haircut backtest Sharpe 1.0, live for 6 months with realised annualised Sharpe $-0.5$.

- Standard error of a 6-month annualised Sharpe: $\sqrt{1/0.5} = 1.41$.
- $z = (-0.5 - 1.0)/1.41 = -1.06$, one-sided $p = 0.144$.
- Even if the strategy is exactly as good as claimed, a negative 6-month Sharpe has probability $\Phi(-1.0/1.41) = 0.24$.

The same shortfall after 2 years gives $z = -1.5/0.707 = -2.12$, $p = 0.017$, which is real evidence.
Conclusion: six months cannot statistically reject the backtest; the decision should come from pre-registered drawdown limits and a check of the process (fills, costs, data), not from the realised Sharpe alone.

## Pitfalls

- Reporting the best variant's Sharpe without the number of variants tried, or counting only the "serious" ones.
- Treating variants as independent when they are near-duplicates, or as near-duplicates when they are not; estimate the effective number of trials from the correlation of trial returns.
- Choosing the hypothesis after seeing the chart ("HARKing"), then writing the mechanism to fit.
- Reusing the holdout after a failed first look and calling the second pass out-of-sample.
- Killing a sound strategy on a noisy short window, or keeping a broken one because the kill rule was never written down.
- Ignoring the base rate: a clean $t = 2.2$ from a data-mined idea is weaker evidence than $t = 2.2$ from a mechanism with independent support.
- Letting the data vendor, universe or cost model drift between trials so results are not comparable.

## Interview questions

> [!question]- alpha-research-falsifiable-hypothesis | What makes an alpha hypothesis well formed?
> A mechanism, a precise testable claim and a kill condition fixed before looking at returns.
> It names who loses to you and why, states universe, horizon, signal, costs, metric and threshold, and makes side predictions (where the effect should be stronger or absent) that can refute it independently.

> [!question]- alpha-research-log-why | Why must a research log record every variant tried, including failures?
> Because the significance of the best result depends on how many trials produced it.
> With $N$ zero-skill trials the expected maximum Sharpe grows like $\sigma_{SR}\sqrt{2\ln N}$; the deflated Sharpe ratio needs $N$ and the cross-trial Sharpe variance, which only a complete log provides.

> [!question]- alpha-research-expected-max-sharpe | 50 strategies with zero true Sharpe are backtested on 5 years. What is the expected best annualised Sharpe?
> About 1.0.
> Each estimate is roughly $N(0, 1/5)$, standard error 0.447, and the expected maximum of 50 standard normals is about 2.28, giving $2.28 \times 0.447 \approx 1.02$.

> [!question]- alpha-research-ppv | 10% of your ideas are real, power is 80% and you test at 5%. What fraction of significant results are false?
> 36%.
> True positives $0.1 \times 0.8 = 0.08$, false positives $0.9 \times 0.05 = 0.045$, so PPV $= 0.08/0.125 = 0.64$.

> [!question]- alpha-research-t3-threshold | Why do Harvey, Liu and Zhu argue for $t > 3$ for new factors?
> Hundreds of factors have been tested on the same data, so a 5% per-test threshold produces many false discoveries.
> Adjusting for the number of tests (Bonferroni, Holm, BHY) pushes the required $t$ to roughly 3 or more; it trades some power for a much lower false discovery rate.

> [!question]- alpha-research-years-to-significance | How many years of iid data does a Sharpe 0.5 strategy need to reach $t = 2$?
> 16 years.
> The $t$-stat of the mean is roughly annualised Sharpe times $\sqrt{\text{years}}$, so $Y = (2/0.5)^2 = 16$.

> [!question]- alpha-research-holdout-reuse | Why is a holdout set valid only once?
> Once its result influences any design decision, the holdout becomes part of the selection process.
> Its performance is then conditioned on that selection and is biased upward like any in-sample number, so a fresh sealed period is needed.

> [!question]- alpha-research-kill-six-months | A Sharpe 1 strategy shows Sharpe $-0.5$ over its first 6 live months. Is that statistical evidence it is broken?
> No, $p \approx 0.14$.
> The 6-month annualised Sharpe has standard error $\sqrt{1/0.5} \approx 1.41$, so the shortfall is only about 1.06 standard errors; check process issues (fills, costs, data) and pre-registered drawdown limits instead.

> [!question]- alpha-research-mechanism-value | Why does an economic mechanism matter if the backtest is already significant?
> It raises the prior and generates independent side predictions.
> A higher prior raises the probability that a significant result is real, and side predictions (cross-sectional, cross-market, post-publication decay) test the idea on data the search did not touch.

> [!question]- alpha-research-kill-criteria | Name three families of pre-registered kill criteria.
> Mechanism refuted, economics fail and live divergence beyond a pre-set band.
> Mechanism: side predictions fail or the effect lives only in untradeable names; economics: net Sharpe, capacity or marginal contribution below hurdle; live: drawdown or tracking error outside a band sized from the backtest distribution.

> [!question]- alpha-research-researcher-degrees-freedom | Give four researcher degrees of freedom that inflate backtests if chosen after seeing results.
> Lookback window, universe filter, rebalance timing and cost model.
> Others include winsorisation level, skip period, sample start date and the metric itself; each silent choice is an unlogged trial.

> [!question]- alpha-research-effective-trials | Your log shows 200 variants but many are near-duplicates. What $N$ goes into a multiple-testing correction?
> The effective number of independent trials, estimated from the correlation of the trial return series.
> Cluster the trials (for example hierarchical clustering on return correlations) and count clusters; using 200 over-corrects, using 1 under-corrects.

## In this repo and SDE-Interview-Prep

- Related notes: [Overfitting and Deflated Sharpe](08-Overfitting-and-Deflated-Sharpe.md), [Backtesting Methodology and Pitfalls](07-Backtesting-Methodology-and-Pitfalls.md), [Hypothesis Testing and Multiple Comparisons](../02-Statistics-and-Econometrics/03-Hypothesis-Testing-and-Multiple-Comparisons.md), [Research Case Studies and Take-Homes](../13-Interview-Playbook/08-Research-Case-Studies-and-Take-Homes.md).

## Further reading

- Marcos Lopez de Prado, *Advances in Financial Machine Learning* (2018), chapters 7, 11 and 12.
- Michael Isichenko, *Quantitative Portfolio Management* (2021).
- Bailey and Lopez de Prado (2014), The Deflated Sharpe Ratio, Journal of Portfolio Management.
- Harvey, Liu and Zhu (2016), ... and the Cross-Section of Expected Returns, Review of Financial Studies.
- Harvey (2017), The Scientific Outlook in Financial Economics, Journal of Finance.
- Ioannidis (2005), Why Most Published Research Findings Are False, PLoS Medicine.
