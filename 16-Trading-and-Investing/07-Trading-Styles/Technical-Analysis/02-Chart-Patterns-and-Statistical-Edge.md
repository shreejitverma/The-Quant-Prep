---
type: concept
title: "Classical Chart Patterns, Geometric Formations, and Statistical Reality"
track: [quant-trader, quant-research]
tier: core
status: solid
est_hours: 1.5
tags: [technical-analysis, chart-patterns, head-and-shoulders, breakouts, volatility-contraction, evidence-based]
prereqs: []
---

# Classical Chart Patterns, Geometric Formations, and Statistical Reality

Classical chart patterns form the visual cornerstone of discretionary technical analysis.
Popularized by Robert D. Edwards and John Magee in their 1948 classic *Technical Analysis of Stock Trends*, geometric formations such as Head and Shoulders, Double Bottoms, Triangles, and Flags are claimed to reflect recurring contests between buyers and sellers.
However, visual pattern recognition is notoriously susceptible to human cognitive biases, pareidolia (perceiving meaningful images in random visual noise), and hindsight selection.
This note separates chartist folklore from empirical reality, examines algorithmic pattern detection methodologies, evaluates peer-reviewed evidence, and analyzes the market microstructure mechanics behind false breakouts and liquidity sweeps.

---

## TL;DR

Classical geometric chart patterns describe consolidation zones bounded by trendlines, support, and resistance.
Reversal patterns (Head and Shoulders, Double Tops/Bottoms) signify exhaustion of directional momentum, while continuation patterns (Flags, Pennants, Triangles) represent pauses within an existing trend.
The evidence is mixed: Lo, Mamaysky, and Wang (2000) found that several algorithmically detected patterns shift the distribution of subsequent returns on US stocks (1962-1996), but they did not show profits after costs.
Large multi-rule studies that correct for data-snooping (Sullivan, Timmermann, and White 1999; Aronson 2006, whose 6,402 rules were indicator rules rather than visual patterns) found no rule that is significant out of sample or after the correction.
Practitioner setups such as the Volatility Contraction Pattern (VCP) have no peer-reviewed test cited here; treat them as hypotheses to backtest.

---

## Learning objectives

- Categorize classical geometric chart formations into reversal and continuation taxonomies.
- Evaluate the empirical evidence ledger for geometric patterns using academic literature and quantitative tests.
- Formulate algorithmic definitions of patterns using local extrema and kernel regression smoothing.
- Model the microstructure mechanics of false breakouts, liquidity engineering, and stop-loss hunting.
- Construct trade plans around Volatility Contraction Patterns (VCP) with objective invalidation levels.

---

## Core concepts

### 1. Taxonomy of Classical Geometric Formations

Edwards and Magee (1948) partitioned geometric patterns into two primary structural categories:

```
+---------------------------------------------------------------------------------+
|                       GEOMETRIC CHART PATTERN TAXONOMY                          |
+---------------------------------------------------------------------------------+
|  REVERSAL PATTERNS                              CONTINUATION PATTERNS           |
|  - Head and Shoulders (Top / Inverse)          - Bull / Bear Flags             |
|  - Double / Triple Tops and Bottoms            - Pennants                      |
|  - Rising / Falling Wedges                     - Symmetrical Triangles         |
|  - Broadening Formations                       - Ascending / Descending Triangles|
|  - Rounding Tops and Bottoms (Saucers)         - Rectangles / Consolidations   |
+---------------------------------------------------------------------------------+
```

1. **Head and Shoulders (Top and Bottom)**:
   - **Structure**: A Left Shoulder peak, followed by a higher Head peak, and a lower Right Shoulder peak.
   - The swing lows between the shoulders define the **Neckline** (horizontal or slanted).
   - **Economic Interpretation**: The rally to the Head represents the final primary push; the failure of the Right Shoulder to reach the Head signals exhaustion of buying demand.
   - The breakdown below the Neckline confirms the structural shift from higher highs to lower lows.
   - **Measured Move Target**:
     $$\text{Target} = P_{\text{neckline}} - (P_{\text{head}} - P_{\text{neckline}})$$

2. **Double Tops ("M" Formation) and Double Bottoms ("W" Formation)**:
   - Two distinct price peaks or troughs testing approximately the same price level separated by an intermediate valley.
   - Confirmation occurs strictly upon a close beyond the intervening peak/trough (the neckline).
   - Chartists advise against entering before the neckline breaks, because until then the shape is only a trading range that can resolve either way.

3. **Triangles (Ascending, Descending, Symmetrical)**:
   - **Ascending Triangle**: Flat horizontal resistance with rising swing lows (bullish accumulation bias).
   - **Descending Triangle**: Flat horizontal support with falling swing highs (bearish distribution bias).
   - **Symmetrical Triangle**: Converging trendlines indicating volatility compression and market indecision.
   - Chartists prefer breakouts well before the apex and distrust apex breakouts; this is a rule of thumb, not a tested result.

4. **Flags and Pennants**:
   - Short continuation patterns, a few weeks at most by chartist convention, that interrupt sharp, high-volume price advances ("the flagpole").
   - **Bull Flag**: A small downward-sloping rectangular channel against the prior advance on contracting volume.
   - **Pennant**: A tiny symmetrical triangle on drying volume.
   - Chartists read a breakout on expanding volume as trend resumption and project a measured move equal to the height of the initial flagpole.

### 2. Algorithmic Pattern Recognition: Kernel Smoothing

Human traders visually fit subjective patterns to charts, introducing severe confirmation bias.
To test pattern validity objectively, Lo, Mamaysky, and Wang (2000) formulated an algorithmic detection framework based on nonparametric kernel regression:

1. **Kernel Smoothing of Price Series**:
   Given a discrete price series $\{P_t\}_{t=1}^T$, compute a continuous smoothed path $\hat{m}(t)$ using Nadaraya-Watson kernel regression:
   $$\hat{m}(t) = \frac{\sum_{i=1}^T K_h(t - i) P_i}{\sum_{i=1}^T K_h(t - i)}$$
   where $K_h(u) = \frac{1}{h} \frac{1}{\sqrt{2\pi}} e^{-\frac{u^2}{2h^2}}$ is the Gaussian kernel and $h$ is the smoothing bandwidth.

2. **Identifying Local Extrema**:
   - Evaluate the first and second derivatives of $\hat{m}(t)$ to locate local extrema:
     - Local Maximum (Peak): $\hat{m}'(t^*) = 0$ and $\hat{m}''(t^*) < 0$.
     - Local Minimum (Trough): $\hat{m}'(t^*) = 0$ and $\hat{m}''(t^*) > 0$.
   - A sequence of five consecutive extrema $\{E_1, E_2, E_3, E_4, E_5\}$ is tested against geometric inequalities:
     - For Head and Shoulders: $E_1, E_3, E_5$ are peaks; $E_2, E_4$ are troughs.
     - Condition: $E_3 > E_1$, $E_3 > E_5$, $|E_1 - E_5| \le \epsilon |E_1|$, and $|E_2 - E_4| \le \epsilon |E_2|$.
   - Lo, Mamaysky, and Wang replace each kernel extremum by the highest (or lowest) actual price near it before applying the inequalities, so smoothing locates the turns but the test uses real prices.

### 3. Empirical Evidence Ledger

```
+---------------------------------------------------------------------------------+
|                           EVIDENCE LEDGER: CHART PATTERNS                       |
+---------------------------------------------------------------------------------+
|  Phenomenon: Classical Geometric Formations (H&S, Double Tops, Triangles)       |
|  Evidence Grade: MIXED to WEAK                                                  |
+---------------------------------------------------------------------------------+
|  Key Empirical Studies:                                                         |
|  1. Lo, Mamaysky, and Wang (2000, Journal of Finance):                          |
|     - 10 patterns detected by kernel regression in US stocks, 1962-1996.        |
|     - Goodness-of-fit and Kolmogorov-Smirnov tests: returns after several       |
|       patterns differ from the unconditional distribution.                      |
|     - Conclusion: some indicators give incremental information; no test of     |
|       profits net of costs.                                                     |
|  2. Curcio, Goodhart, Guillaume, and Payne (1997, Int. J. Finance & Econ.):     |
|     - Intraday FX filter rules built on support and resistance levels that      |
|       technical analysts reported to Reuters.                                   |
|     - Profitable in some trending periods but not on average; the result is    |
|       stronger once transaction costs are included.                             |
+---------------------------------------------------------------------------------+
|  Counter-Evidence & Failure Modes:                                              |
|  1. Aronson (2006, Evidence-Based Technical Analysis):                          |
|     - 6,402 indicator rules (trend, extreme and divergence rules) on the S&P    |
|       500, November 1980 to July 2005.                                          |
|     - None significant at the 0.05 level under White's Reality Check or a       |
|       Monte Carlo permutation test. Visual chart patterns were not tested.      |
|  2. Subjective Labeling and Look-Ahead Bias:                                    |
|     - Human chartists routinely identify patterns only after the subsequent move|
|       has unfolded, falsely inflating apparent predictive accuracy.             |
+---------------------------------------------------------------------------------+
```

### 4. False Breakouts, Liquidity Sweeps, and Microstructure

Why do some pattern breakouts fail quickly?
One documented mechanism comes from order flow; the intent-based stories on top of it are practitioner folklore:

1. **Stop-Loss Clustering**:
   - Chartist textbooks instruct retail traders to place buy-stop orders immediately above obvious horizontal resistance and sell-stop orders below support.
   - This creates dense pools of resting stop orders, which become market orders when triggered.
   - Osler (2003, Journal of Finance) documented this clustering in a bank's currency order book: stop-loss orders cluster just beyond round numbers and take-profit orders at them, and crossing a round number tends to accelerate the move.

2. **The Sweep Story ("Turtle Soup")**:
   - The practitioner account: a large buyer wants size without pushing price up, so price is pushed briefly below obvious support.
   - The triggered sell stops supply the liquidity the buyer absorbs, and price snaps back inside the range.
   - Discretionary traders call this a "bear trap" or "false breakdown."
   - The stop cascade is documented (Osler 2003); the claim that a given break was engineered on purpose is not testable from public data and should be treated as a story, not a fact.

### 5. Volatility Contraction Pattern (VCP)

Popularized by Mark Minervini (2013), building on Richard Wyckoff's ideas about supply absorption:
- An asset forms a sequence of consolidations whose pullbacks narrow (a hypothetical example: $20\%$, then $10\%$, then $5\%$).
- Volume contracts during the tighter pullbacks, which Minervini reads as floating supply being absorbed.
- Minervini's claim is that a breakout after supply dries up follows through; no peer-reviewed test of the VCP is cited here, so it is a hypothesis to backtest, not an established edge.

---

## Worked examples

### Example 1: Calculating Measured Move Target for Head and Shoulders

A discretionary equity analyst identifies a completed Head and Shoulders top pattern on a stock (hypothetical prices):
- Left Shoulder Peak: $\$150.00$.
- Intervening Left Trough: $\$135.00$.
- Head Peak: $\$165.00$.
- Intervening Right Trough: $\$135.00$.
- Right Shoulder Peak: $\$148.00$.
- Horizontal Neckline Level: $P_{\text{neckline}} = \$135.00$.

1. **Compute Height of the Pattern ($H$)**:
   $$H = P_{\text{head}} - P_{\text{neckline}} = \$165.00 - \$135.00 = \$30.00$$

2. **Evaluate Measured Move Downside Target**:
   $$\text{Target} = P_{\text{neckline}} - H = \$135.00 - \$30.00 = \$105.00$$

3. **Trade Plan and Invalidation**:
   - Trigger: Daily close below $\$135.00$ on expanding volume (e.g. entry at $\$134.00$).
   - Invalidation (Stop Loss): Price closes back above the Right Shoulder peak of $\$148.00$ (Risk $= \$14.00$).
   - Profit Target: $\$105.00$ (Reward $= \$29.00$).
   - Reward-to-Risk Ratio: $\frac{\$29.00}{\$14.00} = 2.07$, a $2.07R$ target.

4. **Pattern Test**:
   - The shoulders differ by $|150 - 148| / 150 = 1.33\%$ and the troughs are equal, so the five extrema pass the inequalities above at $\epsilon = 2\%$ but fail at $\epsilon = 1\%$.

### Example 2: Algorithmic Verification of a Double Bottom Pattern

A quantitative research engine analyzes local price extrema identified by Gaussian kernel regression:
- Extrema: $E_1 = \$100.00$ (first trough), $E_2 = \$115.00$ (intervening peak, the neckline), $E_3 = \$100.50$ (second trough).
- After $E_3$, a close at $\$116.00$ breaks the neckline and the next peak is $\$128.00$.
- Tolerance threshold: $\epsilon = 0.02$ ($2\%$).

1. **Test Trough Alignment**:
   $$\frac{|E_1 - E_3|}{E_1} = \frac{|\$100.00 - \$100.50|}{\$100.00} = \frac{0.50}{100.00} = 0.005 = 0.5\% \le \epsilon$$
   The two troughs match within the $2\%$ tolerance.

2. **Test Neckline Breakout**:
   $$P_{\text{close}} = \$116.00 > E_2 = \$115.00$$
   Price successfully breached the central neckline peak, confirming pattern completion.

3. **Evaluate Pattern Expectancy**:
   - Trough-to-neckline height: $H = \$115.00 - \$100.00 = \$15.00$.
   - Theoretical target: $\$115.00 + \$15.00 = \$130.00$.
   - Peak price reached: $\$128.00$, so $(128 - 115) / (130 - 115) = 86.7\%$ of the measured move was captured.

---

## Pitfalls

- **Trading Inside the Pattern Before Breakout Confirmation**:
  Anticipating pattern completion by entering before the neckline is violated means trading a range that has not resolved.
  Many shapes that look like forming tops instead resolve as continuations; only a systematic count over all candidates, not a gallery of successes, tells you how often.
- **Ignoring Volume Divergence on Continuation Patterns**:
  A valid bull flag or pennant requires volume to dry up during the consolidation channel.
  If volume expands heavily on down days within the flag, the formation represents aggressive distribution rather than healthy consolidation.
- **Failure to Account for Volatility Contraction**:
  Practitioners avoid breakouts from wide, loose consolidations because a stop placed below such a base is far away and false breaks are common.
  The claim that breakouts after range and ATR contraction work better is a testable hypothesis, not a result cited here.
- **Data Snooping in Pattern Backtesting**:
  Testing dozens of minor pattern parameter variations without adjusting significance thresholds leads to spurious overfitting.
  White's Reality Check or the Hansen Superior Predictive Ability test must be applied.

---

## Interview questions

> [!question]- mkt-ta-033 | What is a Head and Shoulders top pattern and what does it signify?
> A three-peak reversal formation where the central peak (Head) is highest, flanked by two lower peaks (Shoulders).
> It signals the transition from an uptrend (higher highs) to a downtrend (failure to make a higher high, followed by a neckline break).

> [!question]- mkt-ta-034 | What is the Neckline in a Head and Shoulders formation?
> The support trendline drawn through the two intervening reaction troughs between the left shoulder, head, and right shoulder.
> A decisive close below the neckline confirms the pattern.

> [!question]- mkt-ta-035 | How is the measured move price target calculated for a Head and Shoulders pattern?
> The vertical distance from the peak of the Head to the Neckline, subtracted from the Neckline breakout point: Target = Neckline - (Head - Neckline).
> It provides an objective minimum expectation for the subsequent move.

> [!question]- mkt-ta-036 | What is an Inverse Head and Shoulders pattern?
> A bullish reversal pattern featuring three troughs where the central trough is lowest, flanked by two higher troughs.
> It indicates exhaustion of selling pressure and signals an impending primary uptrend.

> [!question]- mkt-ta-037 | What did Lo, Mamaysky, and Wang (2000) discover regarding algorithmic pattern recognition?
> By smoothing prices with kernel regression and detecting extrema, they showed pattern-conditional return distributions were statistically distinct from unconditional distributions.
> On US stocks from 1962 to 1996 several patterns provided incremental information; the paper does not show profits after transaction costs.

> [!question]- mkt-ta-038 | What did David Aronson (2006) demonstrate in Evidence-Based Technical Analysis?
> None of 6,402 indicator rules tested on the S&P 500 from November 1980 to July 2005 was significant at the 0.05 level after White's Reality Check and a Monte Carlo permutation test.
> The best rules' back-tested returns were consistent with data-mining bias; the study tested indicator rules, not visual chart patterns.

> [!question]- mkt-ta-039 | What is a Double Top ("M" pattern) and when is it confirmed?
> A reversal formation featuring two price peaks testing the same general resistance level separated by a trough.
> It is confirmed only when price closes below the central intervening trough (neckline).

> [!question]- mkt-ta-040 | Why do unconfirmed double tops carry high failure rates?
> Until the neckline is broken, the price is simply oscillating in a trading range or healthy consolidation.
> Entering short before the neckline break results in frequent short squeeze losses when the range resolves upward.

> [!question]- mkt-ta-041 | What is an Ascending Triangle and what is its typical directional bias?
> A consolidation pattern formed by horizontal upper resistance and rising lower swing lows.
> Chartists read it as buyers absorbing supply at higher levels and expect an upward break; no peer-reviewed test of that bias is cited here.

> [!question]- mkt-ta-042 | What is a Descending Triangle and what is its typical directional bias?
> A consolidation pattern formed by horizontal lower support and falling upper swing highs.
> Chartists read it as persistent selling at lower prices and expect a downward break; no peer-reviewed test of that bias is cited here.

> [!question]- mkt-ta-043 | What is a Bull Flag and how should volume behave within it?
> A short-term continuation pattern where price consolidates in a compact downward-sloping channel following a sharp advance.
> By chartist convention volume dries up during the flag and expands on the breakout.

> [!question]- mkt-ta-044 | What is a Pennant pattern?
> A small symmetrical triangle continuation pattern, a few weeks at most by chartist convention, that forms after a vertical price advance.
> It reflects brief volatility compression before trend resumption.

> [!question]- mkt-ta-045 | What is a Volatility Contraction Pattern (VCP)?
> Minervini's term for a sequence of consolidation swings whose pullbacks and volume contract in turn (a hypothetical example: 20%, then 10%, then 5%).
> He reads it as floating supply being absorbed before a breakout; it has no peer-reviewed test cited here.

> [!question]- mkt-ta-046 | Why does trading breakouts from wide, loose patterns typically fail?
> The practitioner argument: wide swings mean supply has not been absorbed, and a stop below a loose base is far away, so a failed break costs more.
> It is an argument for testing, not a measured failure rate.

> [!question]- mkt-ta-047 | What is a liquidity sweep in modern market microstructure?
> A move through obvious support or resistance that triggers the stop-loss orders resting there, followed by a reversal.
> The stop cascade is documented (Osler 2003); the claim that a large trader engineered it to fill an order is a practitioner story that public data cannot confirm.

> [!question]- mkt-ta-048 | Explain the mechanics of a "bear trap" false breakdown.
> Price breaks below major support, triggering retail sell stops and drawing in breakout shorts.
> If buyers absorb the selling and price reverses back into the range, the breakout shorts are trapped and their covering adds to the rally.

> [!question]- mkt-ta-049 | What is a Cup and Handle pattern?
> A bullish continuation pattern popularized by William O'Neil consisting of a rounded U-shaped base (Cup) followed by a shallow downward drift (Handle).
> The handle represents a final shakeout of weak holders on low volume prior to breakout.

> [!question]- mkt-ta-050 | Why is the U-shaped cup preferred over a V-shaped recovery in Cup and Handle patterns?
> O'Neil's argument: a rounded U-shape means price spent time at the bottom, shaking out weak holders, while a V-shape has no base and meets overhead supply sooner.
> This is the practitioner rationale; no peer-reviewed test of U versus V cups is cited here.

> [!question]- mkt-ta-051 | What is a Rising Wedge pattern and what is its typical resolution?
> A formation where both support and resistance lines slope upward, but the support line is steeper (converging upward).
> Chartists read it as fading momentum within an uptrend and expect a downward break; this expectation is folklore unless tested.

> [!question]- mkt-ta-052 | What is a Falling Wedge pattern and what is its typical resolution?
> A formation where both trendlines slope downward, but the upper resistance line descends faster (converging downward).
> Chartists read it as selling exhaustion and expect an upward break; this expectation is folklore unless tested.

> [!question]- mkt-ta-053 | How does kernel bandwidth h influence algorithmic pattern detection?
> A small bandwidth h creates an under-smoothed line that captures high-frequency microstructure noise as false extrema.
> A large bandwidth h over-smooths the price, erasing legitimate intermediate chart patterns.

> [!question]- mkt-ta-054 | What is pareidolia in technical analysis?
> The psychological tendency of the human brain to perceive familiar geometric patterns or faces in completely random data.
> A pattern detector run on simulated random walks still labels some windows as head-and-shoulders, which is why a pattern must be compared with what noise alone produces.

> [!question]- mkt-ta-055 | What is an apex breakout in a symmetrical triangle and why is it undesirable?
> A breakout that occurs near the very point where the converging trendlines meet (the apex).
> Chartists distrust apex breakouts as lacking momentum; this is a rule of thumb, not a tested result.

> [!question]- mkt-ta-056 | What is a Rectangle (Trading Range) pattern?
> A consolidation formation where price bounces between parallel horizontal support and resistance boundaries.
> In auction terms it is a balance area where buyers and sellers transact two-way.

> [!question]- mkt-ta-057 | What is a breakout pullback rate and how should you measure it?
> The fraction of confirmed breakouts that return to test the breakout level before moving on.
> Measure it on every breakout your detector flags, point in time, not on a hand-picked set; practitioner books such as Bulkowski (2005) report such rates from the author's own pattern database, which is not peer-reviewed.

> [!question]- mkt-ta-058 | What is a shakeout in price action?
> A sharp, brief drop that triggers stop losses and then reverses into an advance.
> Practitioners describe it as shares moving from weak holders to strong ones; whether a drop was a shakeout is only known in hindsight.

> [!question]- mkt-ta-059 | What is the measured move projection for a Bull Flag?
> The vertical height of the initial flagpole added to the lowest point of the flag consolidation.
> Target = Flag_Low + (Flagpole_Top - Flagpole_Base).

> [!question]- mkt-ta-060 | Why is a volume breakout filter critical for trading geometric patterns?
> Practitioners treat a breakout on low volume as weakly supported and require above-average volume as confirmation.
> Any particular threshold (a multiple of average volume) is a parameter to choose and test, not a known constant.

> [!question]- mkt-ta-061 | What is a broadening formation (megaphone pattern)?
> A pattern featuring diverging trendlines with higher highs and lower lows.
> Chartists read it as rising volatility and indecision; the claim that it precedes reversals is folklore unless tested.

> [!question]- mkt-ta-062 | How can a trader quantify invalidation on a flag breakout?
> Invalidation occurs if price closes back below the low of the flag consolidation channel.
> If the asset breaks below the flag low, the thesis of immediate momentum continuation is disproven.

> [!question]- mkt-ta-063 | What is a multi-timeframe pattern confirmation?
> Requiring that an intraday pattern (e.g. 15-minute bull flag) align with a larger structural pattern on the daily chart (e.g. breakout from a daily cup-and-handle).
> The aim is to trade with the larger trend; whether the filter helps must be tested for the rule at hand.

> [!question]- mkt-ta-064 | What is White's Reality Check and why is it applied to technical trading rules?
> A bootstrap methodology developed by Halbert White (2000) that evaluates whether the best-performing trading rule in a search space is genuinely superior or merely the luckiest outcome among thousands tested.
> It controls for data-snooping bias in automated technical analysis.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_ta_02_chart_patterns.py`](../../code/mkt_ta_02_chart_patterns.py) prints and asserts every number on this page: the head-and-shoulders and double-bottom arithmetic in exact rational arithmetic, and the pattern labels by running a Lo-Mamaysky-Wang style kernel-regression detector on synthetic paths through the worked-example pivots (the head-and-shoulders passes at a 2% tolerance and fails at 1%); it also shows the detector labels head-and-shoulders windows in a seeded random walk.
- Related notes: [Dow Theory and Trend Evidence](01-Dow-Theory-and-Trend-Evidence.md), [Quantitative Rule Validation and Calibration](08-Quantitative-Rule-Validation-and-Calibration.md).

## Further reading

- Edwards, R. D., & Magee, J. (1948). *Technical Analysis of Stock Trends*. John Magee Inc.
- Curcio, R., Goodhart, C., Guillaume, D., & Payne, R. (1997). *Do technical trading rules generate profits? Conclusions from the intra-day foreign exchange market*. International Journal of Finance & Economics, 2(4), 267-280.
- Lo, A. W., Mamaysky, H., & Wang, J. (2000). *Foundations of technical analysis: Computational algorithms, statistical inference, and empirical implementation*. The Journal of Finance, 55(4), 1705-1765.
- White, H. (2000). *A reality check for data snooping*. Econometrica, 68(5), 1097-1126.
- Bulkowski, T. N. (2005). *Encyclopedia of Chart Patterns* (2nd ed.). John Wiley & Sons. Practitioner statistics from the author's database, not peer-reviewed.
- Osler, C. L. (2003). *Currency orders and exchange rate dynamics: An explanation for the predictive success of technical analysis*. The Journal of Finance, 58(5), 1791-1819.
- Sullivan, R., Timmermann, A., & White, H. (1999). *Data-snooping, technical trading rule performance, and the bootstrap*. The Journal of Finance, 54(5), 1647-1691.
- Aronson, D. R. (2006). *Evidence-Based Technical Analysis: Applying the Scientific Method and Statistical Inference to Trading Signals*. John Wiley & Sons.
- Minervini, M. (2013). *Trade Like a Stock Market Wizard: How to Achieve Super Performance in Stocks in Any Market*. McGraw-Hill Education.
