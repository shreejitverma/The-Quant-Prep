---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Kahneman and Tversky (1979) - Prospect Theory: An Analysis of Decision under Risk, Tversky and Kahneman (1992) - Advances in Prospect Theory: Cumulative Representation of Uncertainty, Shefrin and Statman (1985) - The Disposition to Sell Winners Too Early and Ride Losers Too Long, Odean (1998) - Are Investors Reluctant to Realize Their Losses?, Barber and Odean (2000) - Trading Is Hazardous to Your Wealth, Cremers and Petajisto (2009) - How Active Is Your Fund Manager?, Thaler (1985) - Mental Accounting and Consumer Choice, Statman (2019) - Behavioral Finance: The Second Generation]
---

# Behavioral Portfolio Management and Decision Rules

## TL;DR

- Classical portfolio theory assumes investors maximize expected utility of wealth; Prospect Theory (Kahneman and Tversky 1979) describes investors who judge gains and losses relative to a reference point, weigh losses more than gains, and keep separate mental accounts.
- Tversky and Kahneman (1992) estimated a median loss-aversion coefficient of $\lambda = 2.25$, which helps explain the disposition effect (Shefrin and Statman 1985): selling winners too early and holding losers too long.
- Odean (1998) found that 10,000 discount-brokerage accounts realized 14.8% of their gains but only 9.8% of their losses over 1987-1993, and Barber and Odean (2000) found that the most active traders earned 11.4% a year against 17.9% for the market.
- Institutional fund management is distorted by agency friction and career risk; as Keynes wrote in chapter 12 of *The General Theory*, "Worldly wisdom teaches that it is better for reputation to fail conventionally than to succeed unconventionally."
- Outcome bias (Baron and Hershey 1988; "resulting" in Duke 2018) judges a decision by its result, leading investors to double down on lucky gambles and abandon sound processes during normal drawdowns.
- Debiasing architectures help: written decision checklists, pre-mortems (Klein 2007), systematic rebalancing rules, and explicit red-team challenges.

## Learning objectives

- Formulate Kahneman and Tversky's Prospect Theory value function $v(x)$ and subjective probability weighting function $w(p)$.
- Analyze the micro-mechanics of the disposition effect and its empirical impact on portfolio momentum and tax efficiency.
- Dissect institutional agency problems: career risk, closet indexing, and peer benchmark tracking.
- Distinguish between decision quality and outcome quality using Annie Duke's "resulting" framework.
- Design and implement an institutional investment governance framework with automated decision rules and debiasing gates.

## Core concepts

### 1. Prospect Theory: Mathematical Structure

Kahneman and Tversky (1979, Econometrica) proposed Prospect Theory as a descriptive alternative to Expected Utility Theory, documenting choices that violate it and showing that people evaluate outcomes as gains and losses relative to a reference point $r_0$ rather than as levels of final wealth:

```
+-----------------------------------------------------------------------+
|                    THE PROSPECT THEORY VALUE FUNCTION v(x)            |
+-----------------------------------------------------------------------+
| Value v(x)                                                            |
|                           ^                                           |
|                           |             * * * [Concave: Risk Averse]  |
|                           |       * *                                 |
|                           |   *                                       |
|                           | *                                         |
| --------------------------+---------------------------------------> x |
|                   Losses  |  Reference Point (r_0)            Gains   |
|                      *    |                                           |
|                   *       |                                           |
|               *           |                                           |
|             *             |                                           |
|      * * *                |                                           |
| [Convex: Risk Seeking]    |                                           |
+-----------------------------------------------------------------------+
```

The empirical value function is modeled as a two-part power function:

$$v(x) = \begin{cases} x^\alpha & \text{if } x \ge 0 \\ -\lambda (-x)^\beta & \text{if } x < 0 \end{cases}$$

Tversky and Kahneman (1992, Journal of Risk and Uncertainty) estimated the median parameters:
- $\alpha = \beta = 0.88$ (diminishing sensitivity to gains and losses)
- $\lambda = 2.25$ (the loss aversion coefficient)
- a probability weighting function $w(p) = p^\gamma / (p^\gamma + (1-p)^\gamma)^{1/\gamma}$ with $\gamma = 0.61$ for gains, which gives $w(0.5) = 0.421$ and $w(0.01) = 0.055$.

The function possesses three defining characteristics:
1. **Reference Dependence**: Gains and losses are measured relative to a psychological reference point (often the purchase price or previous high-water mark).
2. **Loss Aversion ($\lambda = 2.25$)**: Ignoring curvature, a $10,000 loss carries the same weight as a $22,500 gain; with $\alpha = \beta = 0.88$ the offsetting gain is $2.25^{1/0.88} \times 10{,}000 = \$25{,}131$.
3. **Diminishing Sensitivity and Reflection**:
   The function is concave in the gain domain ($v''(x) < 0$ for $x > 0$), producing risk aversion for gains: a 50% chance at $10,000 is worth only 0.920 of a sure $5,000 ($0.5 \times 2^{0.88}$), before probability weighting.
   The function is convex in the loss domain ($v''(x) > 0$ for $x < 0$), producing risk seeking for losses: by the same ratio, a 50% chance of losing $10,000 hurts only 0.920 as much as a sure $5,000 loss.

### 2. The Disposition Effect and Execution Traps

Shefrin and Statman (1985) named the disposition effect: the tendency of investors to sell winning investments too soon and hold losing investments too long:

```
+-----------------------------------------------------------------------+
|                    THE DISPOSITION EFFECT MECHANISM                   |
+-----------------------------------------------------------------------+
| Position in GAIN (+30%)               Position in LOSS (-30%)         |
| Concave Value Domain                  Convex Value Domain             |
| Sensation: Fear of losing gains       Sensation: Hope of breaking even|
| Psychological Goal: Pride realization Psychological Goal: Regret avoid|
| Action: SELL PREMATURELY              Action: HOLD / DOUBLE DOWN      |
| Financial Cost: Cut winners short     Financial Cost: Ride losers down|
+-----------------------------------------------------------------------+
```

Odean (1998, Journal of Finance) analyzed trading records for 10,000 accounts at a large discount brokerage from 1987 through 1993 and compared the Proportion of Gains Realized (PGR) with the Proportion of Losses Realized (PLR):

$$\text{PGR} = \frac{\text{Realized Gains}}{\text{Realized Gains} + \text{Paper Gains}}$$

$$\text{PLR} = \frac{\text{Realized Losses}}{\text{Realized Losses} + \text{Paper Losses}}$$

Over the whole year PGR was 0.148 and PLR 0.098, a difference with a t-statistic above 35.
In December the pattern reversed (PLR 0.128 against PGR 0.108), consistent with tax-motivated selling of losers, while January to November showed PGR 0.152 against PLR 0.094.
Selling winners was not justified by later returns: over the next 252 trading days the winners investors sold beat the CRSP value-weighted index by 3.41 percentage points more than the paper losers they kept.
The disposition effect directly opposes rational tax-loss harvesting: investors realize taxable gains immediately while deferring deductible capital losses.

Barber and Odean (2000, Journal of Finance) studied 66,465 households at a large discount broker over 1991-1996.
The households that traded most earned 11.4% a year while the market returned 17.9%, a gap of 6.5 percentage points; the average household earned 16.4% and turned over 75% of its portfolio a year.
They attribute the high trading to overconfidence.

### 3. Institutional Agency and Career Risk

In professional fund management, decisions are rarely made by pure fiduciaries maximizing long-term client capital; they are made by portfolio managers managing personal career risk.
John Maynard Keynes described this in Chapter 12 of *The General Theory* (1936):

> "Worldly wisdom teaches that it is better for reputation to fail conventionally than to succeed unconventionally."

```
+-----------------------------------------------------------------------+
|                    THE INSTITUTIONAL CAREER RISK MATRIX               |
+-----------------------------------------------------------------------+
| Investment Strategy | Market Outcome: SUCCESS | Market Outcome: FAILURE |
|---------------------+-------------------------+-------------------------|
| CONVENTIONAL BET    | Moderate Praise         | Little Blame            |
| (Benchmark Hugging) | "Market did well"       | "Everyone lost money"   |
|                     | Bonus: High             | Job: Safe               |
|---------------------+-------------------------+-------------------------|
| UNCONVENTIONAL BET  | High Praise             | Severe Blame            |
| (True Active Alpha) | "Genius manager"        | "Irresponsible rogue"   |
|                     | Bonus: High             | Job: At risk            |
+-----------------------------------------------------------------------+
```

Because being unconventionally wrong is punished more than being conventionally wrong, institutional managers face asymmetric career payoffs.
This asymmetry produces predictable institutional behaviors:
1. **Closet Indexing**: Holding portfolios that differ little from the benchmark while charging active fees; Cremers and Petajisto (2009) define Active Share as the share of holdings that differ from the benchmark and use 20% to 60% Active Share as their range for closet indexers.
2. **Window Dressing**: Buying recent winners and selling recent losers just before reporting dates so that disclosed holdings look better (Lakonishok, Shleifer, Thaler and Vishny 1991).
3. **Herding and Performance Chasing**: Buying the same consensus macro trades as peer managers, ensuring that if the trade blows up, the entire peer group suffers equally.

### 4. Decision Quality Versus Outcome Quality: Resulting

Baron and Hershey (1988) documented outcome bias: people rate the same decision as better when it happened to turn out well.
Annie Duke (*Thinking in Bets*, 2018) calls the habit of judging decisions by their outcomes "resulting":

```
+-----------------------------------------------------------------------+
|                    THE RESULTING / DECISION MATRIX                    |
+-----------------------------------------------------------------------+
|                     | GOOD OUTCOME             | BAD OUTCOME          |
|---------------------+--------------------------+----------------------|
| GOOD DECISION       | DESERVED SUCCESS         | BAD BREAK            |
| (Positive EV,       | Sound process rewarded   | Sound process,       |
| Disciplined Sizing) | by favorable variance    | unfavored probability|
|---------------------+--------------------------+----------------------|
| BAD DECISION        | DUMB LUCK                | POETIC JUSTICE       |
| (Negative EV,       | Reckless gamble rewarded | Reckless gamble      |
| Reckless Sizing)    | by positive tail shock   | punished by variance |
+-----------------------------------------------------------------------+
```

In financial markets, high-quality decisions with positive mathematical expectancy occasionally suffer severe losses due to irreducible stochastic noise.
Conversely, reckless decisions (such as all-in unhedged short options) can produce massive short-term profits.
Amateur investors evaluate their performance by looking solely at their bank account ("I made money, therefore my thesis was right").
Professional quantitative portfolio managers evaluate trades by examining the decision process: edge verification, sample size, risk constraints, and execution efficiency.

### 5. Institutional Debiasing Architectures

To counter predictable cognitive biases, investment firms can build decision architectures:

```
                 SYSTEMATIC DEBIASING ARCHITECTURE
                 
[Investment Idea / Signal Generated]
                 |
                 v
+-------------------------------------------------+
| 1. Explicit Checklists: Negative Screening      |
|    - Verify leverage, liquidity, governance     |
+-------------------------------------------------+
                 |
                 v
+-------------------------------------------------+
| 2. Gary Klein Pre-Mortem Protocol               |
|    - "Assume it is a year later and the trade   |
|       failed badly. How did it happen?"         |
+-------------------------------------------------+
                 |
                 v
+-------------------------------------------------+
| 3. Red Team / Devil's Advocate Review           |
|    - Designated counter-analyst argues short    |
+-------------------------------------------------+
                 |
                 v
+-------------------------------------------------+
| 4. Automated Position Sizing & Pre-Commitment   |
|    - Hard risk limits, fixed Kelly fractions    |
|    - Automated stop-loss execution              |
+-------------------------------------------------+
```

1. **The Pre-Mortem Protocol (Klein 2007, Harvard Business Review)**:
   Before committing, the team imagines that the project has already failed badly in the future, and each member independently writes down every reason why.
   This makes dissent legitimate and surfaces risks that a confident team would otherwise not voice.

2. **Automated Rebalancing and Execution Rules**:
   Removing emotional human discretion from the selling process.
   Stop-losses and target trim bands are programmed into automated order management systems (OMS) upon trade entry.

3. **Blinded Research Reviews**:
   Presenting financial data and business metrics to investment committees without company names or ticker symbols, eliminating brand bias, celebrity CEO halo effects, and political prejudice.

---

## Flashcard drill bank

> [!question]- mkt-pf-225 | Who developed Prospect Theory, and in what year was it published?
> Daniel Kahneman and Amos Tversky, published in 1979 in Econometrica.

> [!question]- mkt-pf-226 | What is the primary difference between Expected Utility Theory and Prospect Theory?
> Expected utility evaluates absolute wealth; Prospect theory evaluates gains and losses relative to an arbitrary reference point.

> [!question]- mkt-pf-227 | What is the empirical value of the loss aversion coefficient lambda?
> About 2.25, the median estimate in Tversky and Kahneman (1992), meaning a loss weighs about 2.25 times as much as an equal gain (ignoring curvature).

> [!question]- mkt-pf-228 | Why is the Prospect Theory value function S-shaped?
> It is concave in the gain domain (risk-averse for gains) and convex in the loss domain (risk-seeking for losses).

> [!question]- mkt-pf-229 | What is the 'Disposition Effect'?
> The behavioral tendency of investors to sell winning positions too early and hold losing positions too long.

> [!question]- mkt-pf-230 | Who coined the term 'Disposition Effect'?
> Hersh Shefrin and Meir Statman in their 1985 paper.

> [!question]- mkt-pf-231 | How does Terrance Odean's research quantify the disposition effect?
> By showing that the Proportion of Realized Gains (PGR) exceeds the Proportion of Realized Losses (PLR): 0.148 against 0.098 for 10,000 accounts over 1987-1993, reversing only in December.

> [!question]- mkt-pf-232 | Why does the disposition effect harm tax efficiency?
> Investors realize taxable capital gains immediately while delaying realization of deductible capital losses.

> [!question]- mkt-pf-233 | What is Mental Accounting as defined by Richard Thaler?
> The cognitive tendency to treat money differently based on its source, intended purpose, or account category, violating fungibility.

> [!question]- mkt-pf-234 | How does the 'House Money Effect' alter risk behavior?
> After prior gains people take more risk, treating the gains as "house money" rather than their own capital (Thaler and Johnson 1990).

> [!question]- mkt-pf-235 | What is 'resulting' or outcome bias in investing?
> Judging the quality of an investment decision solely by its outcome rather than the probabilistic rigor of the process.

> [!question]- mkt-pf-236 | What did John Maynard Keynes write about conventional versus unconventional failure?
> 'Worldly wisdom teaches that it is better for reputation to fail conventionally than to succeed unconventionally.'

> [!question]- mkt-pf-237 | What is 'career risk' for an institutional portfolio manager?
> The personal financial danger of being terminated for underperforming a benchmark or peer group over short-term evaluation horizons.

> [!question]- mkt-pf-238 | What is 'closet indexing'?
> An active fund holding a portfolio close to its benchmark while charging active fees; Cremers and Petajisto (2009) treat funds with Active Share of 20% to 60% as closet indexers.

> [!question]- mkt-pf-239 | What is 'window dressing' by institutional asset managers?
> Selling embarrassingly losing stocks and purchasing popular recent winning stocks right before reporting dates to display attractive holdings to clients.

> [!question]- mkt-pf-240 | What is overconfidence bias in quantitative trading?
> Overestimating the precision of one's forecasts, the accuracy of private information, and one's personal ability to control market outcomes.

> [!question]- mkt-pf-241 | What is the 'illusion of control'?
> The false belief that an investor can influence or predict the outcome of an inherently stochastic or uncontrollable market process.

> [!question]- mkt-pf-242 | What is hindsight bias?
> The inclination after an event has occurred to view it as having been predictable ('I knew it all along').

> [!question]- mkt-pf-243 | What is recency bias?
> The tendency to overweight recent market performance and extrapolate current trends indefinitely into the future.

> [!question]- mkt-pf-244 | What is the Gary Klein 'Pre-Mortem' protocol?
> A project review exercise where the team assumes an investment has completely failed in the future and works backward to identify the causes.

> [!question]- mkt-pf-245 | What is a 'Red Team' in an investment committee?
> A designated group of analysts whose explicit assignment is to construct the strongest possible bear case and disprove the proposed thesis.

> [!question]- mkt-pf-246 | Why does blinded evaluation improve stock research quality?
> Removing company names and ticker symbols strips away brand loyalty, media narratives, and executive charisma from fundamental valuation.

> [!question]- mkt-pf-247 | What is an Investment Policy Statement (IPS) pre-commitment rule?
> A binding governance rule established in advance that dictates exact rebalancing thresholds and risk limits, bypassing emotional discretion.

> [!question]- mkt-pf-248 | What is the 'endowment effect' in portfolio management?
> Valuing an asset higher simply because one owns it (Kahneman, Knetsch and Thaler 1990), leading to reluctance to sell underperforming positions.

> [!question]- mkt-pf-249 | What is the 'sunk cost fallacy' in losing trades?
> Continuing to allocate capital or attention to a losing investment based on cumulative past expenditures rather than forward-looking prospective return.

> [!question]- mkt-pf-250 | How does probability weighting in Cumulative Prospect Theory explain lottery-ticket trading?
> People overweight small probabilities (w(p) > p for small p; with gamma = 0.61, w(0.01) = 0.055), which makes long-shot payoffs such as deep out-of-the-money options and lottery-like stocks attractive.

> [!question]- mkt-pf-251 | What is 'confirmation bias' during an investment holding period?
> Actively seeking information that supports an existing thesis while ignoring or rationalizing contradictory data.

> [!question]- mkt-pf-252 | What is the role of an investment journal in systematic trading?
> Documenting the thesis, expected catalysts, planned exit rules, and emotional state at trade inception to enable objective post-hoc review.

> [!question]- mkt-pf-253 | Why are automated rebalancing algorithms superior to discretionary human rebalancing?
> Algorithms execute contrarian trades (selling winners and buying losers) unemotionally according to predetermined mathematical thresholds.

> [!question]- mkt-pf-254 | What is the 'narrative fallacy' coined by Nassim Nicholas Taleb?
> The human compulsion to weave disjointed facts into simple causal stories, which makes us overestimate how well we understand past market moves (Taleb, *The Black Swan*, 2007, chapter 6).

> [!question]- mkt-pf-255 | How does peer comparison lead to institutional herd behavior?
> Managers are benchmarked against peers; deviating from consensus carries asymmetric career penalty with limited personal upside.

> [!question]- mkt-pf-256 | What is the primary golden rule of behavioral portfolio management?
> Design systematic rules and governance structures that protect the investment process from human cognitive and emotional vulnerabilities.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_pm_08_behavioral.py`](../../code/mkt_pm_08_behavioral.py) prints and asserts every computed number on this page: the loss-offsetting gain by bisection on the value function against the closed form, the gamble ratios by direct evaluation against $0.5 \times 2^{0.88}$, the decision weights from the Tversky-Kahneman weighting function, Odean's PGR and PLR recomputed from his published counts in exact fractions with the two-proportion t-statistic, and the Barber-Odean return gaps.
- Related notes: [Portfolio Rebalancing, Tax Drag, and Execution Friction](03-Portfolio-Rebalancing-Tax-Drag-and-Execution-Friction.md) (tax-loss harvesting, the opposite of the disposition effect), [Kelly Criterion and Capital Growth Theory](05-Kelly-Criterion-and-Capital-Growth-Theory.md) (pre-committed sizing rules).

## Further reading

- Barber, B. M., & Odean, T. (2000). *Trading Is Hazardous to Your Wealth: The Common Stock Investment Performance of Individual Investors*. Journal of Finance, 55(2), 773-806.
- Baron, J., & Hershey, J. C. (1988). *Outcome Bias in Decision Evaluation*. Journal of Personality and Social Psychology, 54(4), 569-579.
- Cremers, K. J. M., & Petajisto, A. (2009). *How Active Is Your Fund Manager? A New Measure That Predicts Performance*. Review of Financial Studies, 22(9), 3329-3365.
- Duke, A. (2018). *Thinking in Bets*. Portfolio.
- Kahneman, D., Knetsch, J. L., & Thaler, R. H. (1990). *Experimental Tests of the Endowment Effect and the Coase Theorem*. Journal of Political Economy, 98(6), 1325-1348.
- Kahneman, D., & Tversky, A. (1979). *Prospect Theory: An Analysis of Decision under Risk*. Econometrica, 47(2), 263-291.
- Keynes, J. M. (1936). *The General Theory of Employment, Interest and Money*, chapter 12. Macmillan.
- Klein, G. (2007). *Performing a Project Premortem*. Harvard Business Review, 85(9).
- Lakonishok, J., Shleifer, A., Thaler, R., & Vishny, R. (1991). *Window Dressing by Pension Fund Managers*. American Economic Review, 81(2), 227-231.
- Odean, T. (1998). *Are Investors Reluctant to Realize Their Losses?* Journal of Finance, 53(5), 1775-1798.
- Shefrin, H., & Statman, M. (1985). *The Disposition to Sell Winners Too Early and Ride Losers Too Long: Theory and Evidence*. Journal of Finance, 40(3), 777-790.
- Statman, M. (2019). *Behavioral Finance: The Second Generation*. CFA Institute Research Foundation.
- Thaler, R. (1985). *Mental Accounting and Consumer Choice*. Marketing Science, 4(3), 199-214.
- Thaler, R. H., & Johnson, E. J. (1990). *Gambling with the House Money and Trying to Break Even: The Effects of Prior Outcomes on Risky Choice*. Management Science, 36(6), 643-660.
- Tversky, A., & Kahneman, D. (1992). *Advances in Prospect Theory: Cumulative Representation of Uncertainty*. Journal of Risk and Uncertainty, 5(4), 297-323.
