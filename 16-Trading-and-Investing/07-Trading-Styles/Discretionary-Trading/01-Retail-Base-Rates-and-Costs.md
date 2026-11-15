---
type: concept
title: "Retail Base Rates, Transaction Friction, and Expectancy"
track: [quant-trader, quant-research]
tier: core
status: solid
est_hours: 1.5
tags: [retail-trading, base-rates, transaction-costs, expectancy, barber-odean, sebi-study]
prereqs: []
---

# Retail Base Rates, Transaction Friction, and Expectancy

Every serious market participant must begin by confronting the empirical base rates of trading outcomes.
Brokerage marketing and trading-course promotion present discretionary trading as accessible, low-friction wealth generation.
Studies of complete account-level datasets in the US, Taiwan, Brazil and India find the opposite: most active individual traders lose money once transaction costs are counted.
Understanding these base rates and the arithmetic of all-in trading frictions is the prerequisite for designing a system with positive net expectancy.

---

## TL;DR

- Account-level studies find that most active individual traders lose money: 89% of individual equity F&O traders in India lost money in FY 2022 and 93% over FY 2022 to FY 2024 (SEBI 2023 and 2024), and 97% of Brazilian mini-index futures day traders who persisted at least 300 days lost money (Chague, De-Losso and Giovannetti).
- In Taiwan, individual investors' trading losses equalled 2.2% of GDP a year (Barber, Lee, Liu and Odean 2009); in the US, the most active fifth of households earned 11.4% a year against a market return of 17.9% (Barber and Odean 2000).
- Trading performance is governed by the expectancy equation $E = (P_{\text{win}} \times \bar{W}) - (P_{\text{loss}} \times \bar{L}) - C_{\text{friction}}$.
- All-in friction includes explicit commissions, exchange and regulatory fees, bid-ask spread crossing, market impact, borrow fees, margin financing and taxation.
- A strategy with positive gross edge easily turns into negative net expectancy once high turnover multiplies all-in friction.

---

## Learning objectives

- Analyze primary empirical base-rate studies on retail trader performance (Barber-Odean 2000, Barber et al. 2009, Chague et al. 2019, SEBI 2023 and 2024).
- Decompose all-in trading frictions across explicit commissions, spread crossing, market impact, borrow fees, financing, and tax drag.
- Formulate mathematical trade expectancy in dollar terms and normalized R-multiples.
- Calculate the break-even win rate required to survive under specific risk-to-reward ratios and turnover friction.
- Evaluate the compounding destructive impact of turnover and over-trading on capital growth.

---

## Core concepts

### 1. The Empirical Base Rates of Retail Trading

Studies of complete broker or exchange datasets reach the same conclusion across markets:

1. **Barber and Odean (2000) - "Trading Is Hazardous to Your Wealth" (US equities)**:
   - Studied 66,465 households with accounts at a large US discount broker from 1991 to 1996.
   - The average household turned over 75% of its portfolio annually and earned 16.4% a year net, against 17.9% for the market, a shortfall of $17.9 - 16.4 = 1.5$ percentage points.
   - The households that traded most earned 11.4% a year net, a shortfall of $17.9 - 11.4 = 6.5$ percentage points.
   - Conclusion (the paper's): trading is hazardous to your wealth, and the most active traders paid the most for it.

2. **Barber, Lee, Liu, and Odean (2009) - "Just How Much Do Individual Investors Lose by Trading?" (Taiwan Stock Exchange)**:
   - Used the complete trade record of the Taiwan Stock Exchange from 1995 to 1999.
   - Individual investors' trading losses were equivalent to 2.2% of Taiwan's GDP, or 2.8% of total personal income.
   - Virtually all individual trading losses trace to their aggressive (marketable) orders.
   - Institutions gained about 1.5 percentage points a year from trading, and foreign institutions captured nearly half of institutional profits.

3. **Chague, De-Losso, and Giovannetti (2019) - "Day Trading for a Living?" (Brazilian equity futures)**:
   - Followed every individual who began day trading the Brazilian equity index futures market between 2013 and 2015 and persisted for at least 300 days.
   - **97%** of them lost money.
   - Only **0.4%** earned more than a bank teller's starting pay (US\$54 per day).
   - The top individual earned only US\$310 per day, with a standard deviation of US\$2,560 per day.
   - The authors found no evidence of learning by day trading and concluded it is virtually impossible to day trade for a living.

4. **SEBI Study (January 2023) - Indian equity futures and options**:
   - The Securities and Exchange Board of India (SEBI) studied 45.2 lakh (about 4.5 million) unique individual equity F&O traders in FY 2022, using all individual clients of the top 10 brokers.
   - **89%** of individual traders incurred net losses; the average loss among loss-makers was about ₹1.1 lakh (₹110,000).
   - For active traders excluding outliers, loss-makers spent an additional 28% of their net trading losses on transaction costs, and profit-makers spent between 15% and 50% of their profits on transaction costs.
   - The remaining $100\% - 89\% = 11\%$ of individual traders were net profitable, with an average profit of about ₹1.5 lakh.
   - A follow-up study (SEBI press release 37/2024, 23 September 2024) found that 93% of more than 1 crore (10 million) individual F&O traders made losses over FY 2022 to FY 2024, averaging about ₹2 lakh per loss-maker including transaction costs.

### 2. The All-In Transaction Friction Waterfall

Retail traders frequently count only the broker's advertised commission (for example "zero commission" or "₹20 per order").
In institutional practice, all-in friction $C_{\text{friction}}$ is a multi-tiered waterfall:

$$C_{\text{friction}} = C_{\text{comm}} + C_{\text{spread}} + C_{\text{impact}} + C_{\text{exchange}} + C_{\text{tax}} + C_{\text{funding}}$$

- **Explicit Commission ($C_{\text{comm}}$)**: Direct broker execution fee per share, contract, or flat order.
- **Half-Spread Crossing ($C_{\text{spread}}$)**: Crossing the bid-ask spread on market orders ($P_a - S$ on buy, $S - P_b$ on sell).
- **Market Slippage and Impact ($C_{\text{impact}}$)**: Moving the order book depth during execution, scaling with size relative to liquidity.
- **Regulatory and Exchange Fees ($C_{\text{exchange}}$)**: Exchange access and clearing fees, SEC Section 31 fees and the FINRA Trading Activity Fee on US equity sales, clearing house levies.
- **Statutory Taxes ($C_{\text{tax}}$)**: Stamp duty, capital gains taxes, and India's Securities Transaction Tax (STT); as of November 2026 STT is 0.1% on each side of a delivery equity trade, 0.05% of the sale value of futures and 0.15% of the option premium on sale, the derivative rates having been raised from 1 April 2026 by the Union Budget 2026-27 (Finance Act 2026), after earlier increases in 2023 and from 1 October 2024.
- **Financing and Borrow Drag ($C_{\text{funding}}$)**: Margin interest on leveraged longs, hard-to-borrow annualized fees on short stock.

### 3. Mathematical Expectancy in Trading

Mathematical expectancy $E$ represents the expected average dollar gain or loss per trade over a statistically significant sample:

$$E = (P_{\text{win}} \times \bar{W}) - (P_{\text{loss}} \times \bar{L}) - C_{\text{friction}}$$

Where:
- $P_{\text{win}}$ is the probability of a winning trade (win rate).
- $P_{\text{loss}} = 1 - P_{\text{win}}$ is the probability of a losing trade.
- $\bar{W}$ is the average gross dollar gain on winning trades.
- $\bar{L}$ is the average gross dollar loss on losing trades.
- $C_{\text{friction}}$ is the round-trip all-in transaction cost per trade.

#### The R-Multiple Expectancy Framework
To normalize performance across varying position sizes and asset prices, discretionary traders commonly define risk in units of $1R$ (the initial dollar amount risked to the stop-loss):

$$R = |P_{\text{entry}} - P_{\text{stop}}| \times Q$$

Every trade outcome is recorded as an $R$-multiple (e.g. $+2.5R$, $-1.0R$, $+0.5R$).
The expectancy in $R$-multiples ($E_R$) is:

$$E_R = (P_{\text{win}} \times \bar{W}_R) - ((1 - P_{\text{win}}) \times 1.0) - c_R$$

Where $\bar{W}_R = \bar{W} / R$ is the average reward-to-risk ratio, and $c_R = C_{\text{friction}} / R$ is the friction drag expressed as a fraction of initial risk.
For a system to be viable over time, its expectancy must be strictly positive:

$$E_R > 0 \iff P_{\text{win}} > \frac{1.0 + c_R}{1.0 + \bar{W}_R}$$

---

## Worked examples

### Example 1: The High-Frequency Friction Drag on a "Zero-Commission" Trader

All inputs in this example are hypothetical.
A retail day trader with a $\$25,000$ account trades 5 round-trips per day for 252 trading days ($5 \times 252 = 1,260$ round-trips annually) in a liquid stock trading at $\$100.00$.
Position size is 500 shares ($\$50,000$ gross market value, $2\times$ leverage).
The broker charges $\$0.00$ commission.
The all-in frictions per trade are:
- Quoted spread: $\$0.02$ ($2\text{ cents}$).
  The trader crosses half the spread on each side (market buy at the ask and market sell at the bid):
  $$C_{\text{spread}} = 2 \times \frac{\$0.02}{2} \times 500 = \$0.02 \times 500 = \$10.00$$
- Slippage / delayed queue fill: $\$0.01$ total per round-trip:
  $$C_{\text{slippage}} = \$0.01 \times 500 = \$5.00$$
- Exchange and regulatory fees: $\$1.50$ round-trip:
  $$C_{\text{exchange}} = \$1.50$$
- Total round-trip friction per trade:
  $$C_{\text{friction}} = \$10.00 + \$5.00 + \$1.50 = \$16.50\text{ per trade}$$

**Annualized Drag**:
$$\text{Total Annual Friction} = 1,260 \times \$16.50 = \$20,790$$

**Capital Impact**:
The annual friction represents:
$$\frac{\$20,790}{\$25,000} = 83.16\%\text{ of starting account equity}$$
Even with zero gross skill (gross profits equal gross losses), the trader loses $83.16\%$ of starting equity in one year purely to execution friction.
To break even, the trader must make gross trading profits equal to $83.16\%$ of starting equity.

### Example 2: Expectancy and Break-Even Win Rate Calculation

A trader develops a breakout strategy targeting $\bar{W}_R = 2.0R$ with a hard stop at $-1.0R$.
The trader risks $R = \$500$ per trade.
Round-trip execution friction is $\$35$ ($c_R = \frac{\$35}{\$500} = 0.07R$).

1. **Calculate the Theoretical Break-Even Win Rate (Zero Friction)**:
   $$P_{\text{break-even}} = \frac{1.0}{1.0 + 2.0} = \frac{1}{3} = 33.33\%$$

2. **Calculate the Realized Break-Even Win Rate (With Friction)**:
   $$P_{\text{break-even, real}} = \frac{1.0 + 0.07}{1.0 + 2.0} = \frac{1.07}{3.0} = 35.67\%$$

3. **Evaluate Realized Performance at 40% Win Rate**:
   Suppose the trader achieves a $40\%$ win rate across 200 trades:
   $$E_R = (0.40 \times 2.0) - (0.60 \times 1.0) - 0.07 = 0.80 - 0.60 - 0.07 = +0.13R\text{ per trade}$$
   Total Expected Profit:
   $$\text{Total PnL} = 200 \times (+0.13R) = +26R = 26 \times \$500 = +\$13,000$$

4. **Evaluate Performance if Win Rate Slips to 35%**:
   $$E_R = (0.35 \times 2.0) - (0.65 \times 1.0) - 0.07 = 0.70 - 0.65 - 0.07 = -0.02R\text{ per trade}$$
   Total Expected Loss:
   $$\text{Total PnL} = 200 \times (-0.02R) = -4R = -\$2,000$$
   A 5-percentage-point drop in win rate turns a profitable system into a losing one, because friction has already raised the break-even win rate to $35.67\%$.

---

## Pitfalls

- **The "Free Commission" Delusion**:
  A zero-commission broker is paid in other ways, for example through payment for order flow (PFOF) from wholesale market makers, which creates a conflict of interest over where orders are routed.
  The spread, impact and fees in Example 1 remain whatever the commission.
- **Ignoring Sampling Error in Small Samples**:
  A trader with 20 winning trades out of 30 ($66.7\%$ win rate) believes they have mastered the market.
  At $N = 30$ the standard error of the observed win rate is $\sqrt{p(1-p)/N} = 8.6\%$, so a normal-approximation 95% interval runs from $49.8\%$ to $83.5\%$ and cannot rule out a coin-flip win rate.
- **Neglecting Tax Asymmetry**:
  In the US, as of November 2026, short-term gains are taxed as ordinary income (top federal rate 37%, plus the 3.8% net investment income tax above the income thresholds), while net capital losses offset ordinary income only up to USD 3,000 a year (USD 1,500 if married filing separately) under IRC section 1211(b), with the excess carried forward.
- **Compounding Turnover Decay**:
  Costs are paid on every trade whether it wins or loses, so with zero gross edge equity can only decline, and the decline grows linearly with turnover.

---

## Interview questions

> [!question]- mkt-trd-001 | What was the central finding of Barber and Odean's 2000 empirical study on individual investors?
> Trading reduced returns, and the heaviest traders lost the most.
> The average household (75% annual turnover) earned 16.4% a year against the market's 17.9%; the households that traded most earned 11.4%, a 6.5-point annual shortfall net of costs.

> [!question]- mkt-trd-002 | What did the Chague et al. study discover regarding individuals day-trading Brazilian equity futures?
> 97% of the individuals who day-traded for at least 300 days lost money.
> Only 0.4% earned more than a bank teller's starting pay (USD 54 per day), the best individual earned USD 310 per day with a daily standard deviation of USD 2,560, and there was no evidence of learning.

> [!question]- mkt-trd-003 | What percentage of retail traders lost money in Indian equity F&O according to the 2023 SEBI study?
> 89% of individual traders incurred net losses during FY 2022.
> For active traders excluding outliers, loss-makers paid transaction costs equal to an additional 28% of their net trading losses, and profit-makers paid 15% to 50% of their profits.
> A September 2024 SEBI follow-up found 93% of individual F&O traders lost money over FY 2022 to FY 2024.

> [!question]- mkt-trd-004 | State the mathematical expectancy equation for a trading strategy.
> Expectancy = (P_win * Average_Win) - (P_loss * Average_Loss) - Cost_friction.
> Expectancy quantifies the expected average net dollar gain or loss per trade across a large sample.

> [!question]- mkt-trd-005 | What is an R-multiple in professional trade management?
> An R-multiple expresses a trade's realized profit or loss as a ratio of the initial dollar risk defined by the stop-loss: R = Dollar_PnL / Dollar_Risk.
> A 2R gain represents a profit equal to twice the initial amount risked.

> [!question]- mkt-trd-006 | What is the break-even win rate formula for a strategy targeting an average reward-to-risk ratio W_R?
> P_breakeven = (1.0 + c_R) / (1.0 + W_R), where c_R is the round-trip transaction friction expressed as a fraction of initial risk R.
> With zero friction and a 2:1 reward-to-risk ratio, the break-even win rate is exactly 1/3 (33.33%).

> [!question]- mkt-trd-007 | Why does high turnover convert a statistically neutral strategy into a catastrophic loser?
> Every transaction subtracts spread, market impact, clearing fees, and taxes from account equity.
> With high turnover, accumulated friction scales linearly with volume, eroding account equity even if gross trading returns are zero.

> [!question]- mkt-trd-008 | What are the six components of the all-in trading friction waterfall?
> 1. Broker commissions.
> 2. Quoted bid-ask spread crossing.
> 3. Market impact and execution slippage.
> 4. Exchange access, clearing, and regulatory fees.
> 5. Statutory stamp duty, STT, and transaction taxes.
> 6. Margin financing and short borrow costs.

> [!question]- mkt-trd-009 | How does Payment for Order Flow (PFOF) create a hidden cost for retail traders?
> The broker is paid by the wholesaler that executes its customers' orders, so its routing decision is conflicted.
> Wholesalers usually fill at or inside the quoted spread, but the size of that price improvement varies across brokers and is the hidden cost or benefit; SEC Rule 606 requires brokers to disclose their routing and PFOF and Rule 605 requires market centers to publish execution-quality statistics.

> [!question]- mkt-trd-010 | What is the disposition effect documented by Terrance Odean (1998)?
> The tendency of investors to sell winning positions too soon and hold losing positions too long; Odean found it in 10,000 discount-brokerage accounts (1987 to 1993).
> It was not justified by subsequent performance and, for taxable accounts, lowered after-tax returns.

> [!question]- mkt-trd-011 | Why is a high win rate (e.g. 80%) not a guarantee of profitability?
> An 80% win rate strategy that wins $100 on 8 trades (+ $800) but loses $500 on 2 trades (- $1,000) has negative net expectancy (- $200).
> Expectancy depends equally on the magnitude of wins versus losses (the payoff ratio).

> [!question]- mkt-trd-012 | What is the Pattern Day Trader (PDT) rule under US FINRA regulations, and is it still in force?
> As of November 2026 it has been replaced: FINRA Regulatory Notice 26-10 (SEC approval in Exchange Act Release No. 105226, 14 April 2026) replaced the FINRA Rule 4210 day-trading margin requirements, including the pattern-day-trader designation and its $25,000 minimum equity, with intraday margin standards effective 4 June 2026; firms may phase in until 20 October 2027.
> Under the old rule a margin account with four or more day trades in five business days was a pattern day trader and needed $25,000 of equity to keep day trading, so some brokers may still apply it during the phase-in.

> [!question]- mkt-trd-013 | What is Securities Transaction Tax (STT) and how does it distort high-frequency equity trading in India?
> STT is a statutory tax levied by the Government of India on the value of equity and derivatives transactions (on the premium for options).
> As of November 2026 delivery trades pay 0.1% on each side, a 20-basis-point round-trip hurdle that penalizes short-term delivery trading.

> [!question]- mkt-trd-014 | What is the wash-sale rule under US IRS Section 1091?
> If an investor sells a security at a loss and repurchases the same or substantially identical security within 30 days before or after the sale, the loss cannot be deducted.
> The disallowed loss is added to the cost basis of the newly purchased security, delaying tax loss harvesting.

> [!question]- mkt-trd-015 | How does sample size N impact confidence in an observed win rate?
> The standard error of an observed proportion p across N trades is sqrt(p * (1 - p) / N).
> For N = 50 and p = 50%, the normal-approximation 95% confidence interval spans 36% to 64%, rendering short-term performance indistinguishable from random luck.

> [!question]- mkt-trd-016 | What is the difference between geometric mean return and arithmetic mean return?
> Arithmetic mean is the simple average of periodic returns; geometric mean is the true compounding rate of capital growth: (1 + R_geo)^T = Product(1 + R_t).
> Geometric return is never above arithmetic return and is strictly lower whenever returns vary (AM-GM inequality), with R_geo ~ R_arith - 0.5 * sigma^2 for small returns.

> [!question]- mkt-trd-017 | What is variance drag and how does volatility destroy compounding capital?
> Volatility reduces compound geometric growth relative to simple average returns.
> A 50% loss requires a 100% subsequent gain to break even, illustrating the asymmetric mathematical penalty of downward volatility.

> [!question]- mkt-trd-018 | What is the overconfidence bias among retail traders as documented by Barber and Odean (2001)?
> In "Boys Will Be Boys" (Quarterly Journal of Economics, 2001) men traded 45% more than women, consistent with greater overconfidence.
> Trading reduced men's net returns by 2.65 percentage points a year against 1.72 percentage points for women.

> [!question]- mkt-trd-019 | What does a market order pay compared with a passive limit order, and which one bears adverse selection?
> A market order pays for immediacy: it crosses the spread and pays the half-spread plus any impact on the resting depth.
> A resting limit order earns the half-spread (and a rebate on some maker-taker venues) but bears adverse selection: it tends to fill when price is moving through it, and it may not fill at all.

> [!question]- mkt-trd-020 | What is survivorship bias in retail trading education and marketing?
> Showcasing the rare profitable traders while ignoring the majority who lost and quit (89% to 97% losers in the SEBI and Chague et al. studies).
> It creates the false perception that retail day trading is a repeatable, low-risk career path.

> [!question]- mkt-trd-021 | How does hard-to-borrow (HTB) fee rate erode the edge of short-selling momentum breakdowns?
> Borrow fees accrue daily on the short position's value, and for hard-to-borrow names they can be very high; a hypothetical 50% annual fee costs 50% / 365 = 0.137% of the position per day.
> A directionally correct short can still lose money if the decline takes longer than the fee allows.

> [!question]- mkt-trd-022 | What is implementation shortfall in discretionary trade execution?
> The difference between the paper return of a position valued at the decision price and the return actually achieved (Perold 1988, Journal of Portfolio Management).
> It aggregates decision delay, market movement during entry, spread, impact, commissions, and the opportunity cost of shares never filled.

> [!question]- mkt-trd-023 | What is a profit factor and how is it calculated?
> Profit Factor = Gross Total Profits / Gross Total Losses.
> A profit factor above 1.00 means positive expectancy over the sample; there is no universal "good" threshold, so judge it after costs and with its sampling error.

> [!question]- mkt-trd-024 | Why is a Profit Factor of 1.10 dangerously fragile in live market execution?
> A profit factor of 1.10 leaves little room for extra costs: a system winning 40% of trades at 1.65R against 1.0R losses has PF = 0.66 / 0.60 = 1.10 and expectancy of only 0.06R per trade.
> An extra 0.06R of slippage or fees per trade takes it to break-even.

> [!question]- mkt-trd-025 | How does leverage amplify trading friction relative to equity capital?
> If an investor uses 4x leverage to trade $100,000 GMV on $25,000 equity, a 10-basis-point round-trip cost ($100) represents 0.40% of their actual equity.
> Cost as a fraction of equity scales linearly with both leverage and turnover.

> [!question]- mkt-trd-026 | What is the gambler's fallacy in discretionary trading?
> The irrational belief that after a series of consecutive losing trades, the probability of the next trade being a winner is increased.
> In independent market trials, the probability distribution of each setup remains unchanged regardless of past streaks.

> [!question]- mkt-trd-027 | How does mental accounting distort retail risk management?
> Traders treat "house money" (accumulated profits) more recklessly than their initial principal, the house-money effect of Thaler and Johnson (1990, Management Science).
> They widen stops and increase position sizes on winning streaks, so a reversal can give back the accumulated profits.

> [!question]- mkt-trd-028 | What is the impact of asymmetric capital gains tax treatment on net Sharpe ratio?
> If losses were fully deductible at the same rate as gains are taxed, tax would scale returns and roughly preserve the Sharpe ratio.
> When losses are only partly or slowly deductible, tax cuts the right tail more than the left, lowering the after-tax mean more than the volatility and so lowering the after-tax Sharpe.

> [!question]- mkt-trd-029 | What is the risk-free rate hurdle in evaluating trading performance?
> Capital allocated to trading must beat the risk-free yield net of all costs and taxes.
> With a hypothetical 4% Treasury bill yield, a trader earning 6% gross who pays 3% in fees and taxes earns 3% net, below riskless cash.

> [!question]- mkt-trd-030 | Why does retail order flow clustering around round numbers (e.g. $100, $50) create adverse execution?
> Osler (2003, Journal of Finance) found, in a large dealing bank's FX order book, that take-profit orders cluster at round numbers and stop-loss orders cluster just beyond them.
> Triggered stops are market orders, so price tends to accelerate after crossing a round number, and a stop placed in the cluster fills into that move with extra slippage.

> [!question]- mkt-trd-031 | What is revenge trading and what physiological mechanism triggers it?
> Impulsive, unplanned trades executed immediately after a painful loss to recover capital rapidly.
> No single established physiological trigger is documented; the behavior matches the break-even effect of Thaler and Johnson (1990), in which people who are behind seek risk to get back to even, so treat it as a rule to prevent (daily loss limits) rather than a mechanism to diagnose.

> [!question]- mkt-trd-032 | Why must every trade plan specify the exact invalidation price before order placement?
> Pre-defining the invalidation price establishes the objective boundary where the market thesis is proven wrong.
> It removes in-the-moment hesitation during adverse price movement and bounds planned risk to 1R, although gaps and slippage can still make the realized loss larger.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_trd_01_base_rates_costs.py`](../../code/mkt_trd_01_base_rates_costs.py) prints and asserts every number on this page: Example 1 by an explicit fill-by-fill cash ledger checked against the cost formula, break-even win rates by bisection on the expectancy against exact rational arithmetic, win-rate standard errors from the exact binomial variance, and the card arithmetic from enumerated trade lists; the study figures are cited constants.
- Related notes: [Position Sizing and Ruin](02-Position-Sizing-and-Ruin.md), [Probability and Decision Making](06-Probability-and-Decision-Making.md).

## Further reading

- Barber, B. M., & Odean, T. (2000). *Trading is hazardous to your wealth: The common stock investment performance of individual investors*. The Journal of Finance, 55(2), 773-806.
- Barber, B. M., & Odean, T. (2001). *Boys will be boys: Gender, overconfidence, and common stock investment*. The Quarterly Journal of Economics, 116(1), 261-292.
- Barber, B. M., Lee, Y. T., Liu, Y. J., & Odean, T. (2009). *Just how much do individual investors lose by trading?*. The Review of Financial Studies, 22(2), 609-632.
- Chague, F., De-Losso, R., & Giovannetti, B. (2019). *Day trading for a living?*. Working Paper 2019_47, Department of Economics, University of Sao Paulo (FEA-USP); revised as FGV EESP Textos para Discussao 525 (2020).
- FINRA (2026). *Regulatory Notice 26-10: FINRA Adopts New Intraday Margin Standards to Replace the Day Trading Margin Requirements*. https://www.finra.org/rules-guidance/notices/26-10
- Odean, T. (1998). *Are investors reluctant to realize their losses?*. The Journal of Finance, 53(5), 1775-1798.
- Osler, C. L. (2003). *Currency orders and exchange rate dynamics: An explanation for the predictive success of technical analysis*. The Journal of Finance, 58(5), 1791-1819.
- Perold, A. F. (1988). *The implementation shortfall: Paper versus reality*. The Journal of Portfolio Management, 14(3), 4-9.
- Securities and Exchange Board of India (SEBI). (2023). *Analysis of Profit and Loss of Individual Traders dealing in Equity F&O Segment* (published 25 January 2023). SEBI Research Study.
- Securities and Exchange Board of India (SEBI). (2024). *Updated SEBI Study Reveals 93% of Individual Traders Incurred Losses in Equity F&O between FY22 and FY24*. Press Release No. 37/2024, 23 September 2024.
- Thaler, R. H., & Johnson, E. J. (1990). *Gambling with the house money and trying to break even: The effects of prior outcomes on risky choice*. Management Science, 36(6), 643-660.
