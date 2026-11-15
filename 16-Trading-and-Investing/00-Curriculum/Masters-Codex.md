---
type: reference
title: "Markets Mastery OS - Masters Codex"
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: solid
tags: [curriculum, masters-codex, lineage, principles, execution-rules]
---

# Markets Mastery OS - Masters Codex

The Masters Codex distils the philosophy, principles, rules and failure modes of ten investors and traders into ideas that can be tested, simulated and practised.
Every statement of what a master said, wrote or did cites the primary text it comes from: a shareholder letter with its year, a book, an interview or a dated speech.
Direct quotations appear only where the wording was checked against that text (as of November 2026).
Lines labelled "Codex practice" and every "Master's Shoes" anti-pattern are this curriculum's own synthesis, not claims about the master.

---

## 1. Benjamin Graham (1894 - 1976)
- **Lineage**: Classical Value Investing and Security Analysis.
- **Core Principles**:
  - **Margin of Safety**: Buy only when the price sits well below a conservative estimate of value; Graham's 1976 interview restates this as being able to justify every purchase by objective reasoning that shows a margin of safety in value terms.
  - **Mr. Market Metaphor**: The market as an emotional business partner offering daily quotes that the investor may use or ignore (*The Intelligent Investor*, chapter 8).
  - **Net-Current-Asset Value (NCAV / Net-Net)**: Graham's working-capital value gives no weight to plant and other fixed assets and deducts all liabilities in full from current assets:
    $$\text{NCAV} = \text{Current Assets} - \text{Total Liabilities} - \text{Preferred Stock}$$
- **Concrete Execution Rules**:
  - Buy bargain issues at no more than two-thirds of net current asset value, the practice Graham describes in *The Intelligent Investor* (chapter 15).
  - Rely on group results rather than single issues: in the 1976 interview Graham says an individual investor should be able to find 30 issues or more that offer attractive buying opportunities, and judges the net-current-asset method by the expectable group outcome.
  - Set a selling policy at purchase: a profit objective of 50 to 100 percent and a maximum holding period of two to three years, selling at market any holding that has not reached the objective by then (1976 interview).
- **Primary Sources**: Graham and Dodd (*Security Analysis*, 1934); Graham (*The Intelligent Investor*, 1949; 4th revised edition 1973); Hartman L. Butler Jr., "A Conversation with Benjamin Graham", *Financial Analysts Journal* (1976), interview of March 6 1976.
- **Master's Shoes (Anti-Pattern)**: The "cigar butt" trap; buying structurally dying businesses whose working capital erodes before any value is realised.

---

## 2. Warren Buffett (born 1930)
- **Lineage**: Modern Quality Value Investing and Capital Allocation.
- **Core Principles**:
  - **Economic Moats**: The 2007 Berkshire letter describes a truly great business as one with an enduring moat that protects excellent returns on invested capital.
  - **Owner Earnings**: Defined in the 1986 letter as (a) reported earnings plus (b) depreciation, depletion, amortization and certain other non-cash charges, less (c) the average annual capitalized expenditure the business requires to fully maintain its long-term competitive position and unit volume, with any additional working capital needed for that purpose included in (c):
    $$\text{Owner Earnings} = \text{Net Income} + \text{D\&A and other non-cash charges} - \text{Maintenance Capex (including required working capital)}$$
    Owner earnings can be above or below reported net income, depending on whether maintenance spending exceeds the non-cash charges.
  - **Circle of Competence**: The 1996 letter asks investors to evaluate only businesses within their circle of competence, noting that the size of the circle matters less than knowing its boundaries.
- **Concrete Execution Rules**:
  - "It's far better to buy a wonderful company at a fair price than a fair company at a wonderful price." (1989 letter, "Mistakes of the First Twenty-five Years").
  - Codex practice: judge management on its long-run capital allocation record, for example the spread of return on invested capital over the cost of capital and the prices paid for buybacks.
- **Primary Sources**: Berkshire Hathaway shareholder letters (berkshirehathaway.com/letters, 1977 onward); Cunningham (*The Essays of Warren Buffett: Lessons for Corporate America*, first published 1997, several later editions).
- **Master's Shoes (Anti-Pattern)**: Overpaying for perceived quality; holding an asset through a valuation bubble because of reluctance to realise capital gains.

---

## 3. Charlie Munger (1924 - 2023)
- **Lineage**: Multidisciplinary Mental Models and Behavioral Rationality.
- **Core Principles**:
  - **Inversion**: In his 1986 Harvard School commencement speech Munger credits the mathematician Carl Jacobi with the maxim "Invert, always invert" and applies it by asking what would guarantee failure, then avoiding it.
  - **Latticework of Mental Models**: Munger's 1994 USC Business School talk, "A Lesson on Elementary, Worldly Wisdom", argues for carrying the big models from many disciplines rather than one.
  - **Lollapalooza Effect**: In "The Psychology of Human Misjudgment" (1995) Munger describes several psychological tendencies acting together in the same direction to produce extreme outcomes.
- **Concrete Execution Rules**:
  - Codex practice: write a checklist of failure modes before committing capital.
  - Codex practice: reject mediocre opportunities and concentrate capital in the rare ideas that clear a high bar.
  - Codex practice: avoid needless turnover, which interrupts compounding and adds costs and taxes.
- **Primary Sources**: Munger (*Poor Charlie's Almanack*, 2005, edited by Peter D. Kaufman), which reprints the 1986, 1994 and 1995 talks.
- **Master's Shoes (Anti-Pattern)**: Intellectual overconfidence; underestimating technological disruption because it sits outside historical business patterns.

---

## 4. Edward O. Thorp (born 1932)
- **Lineage**: Quantitative Arbitrage and Mathematical Position Sizing.
- **Core Principles**:
  - **The Kelly Criterion**: Size each bet to maximise the expected logarithmic growth rate of capital (Kelly 1956), which Thorp applied first to blackjack and then to markets.
  - **Hedged Warrant Positions**: Thorp and Kassouf (1967) set out a system of hedging overpriced warrants against the common stock so that the position profits largely independently of the stock's direction.
- **Concrete Execution Rules**:
  - Bet a fraction of full Kelly when the edge is estimated with error; Thorp (2006) discusses fractional Kelly as a way to cut volatility and the damage from overestimating the edge.
  - Codex practice: rebalance delta-hedged warrant and convertible positions as the underlying stock moves.
- **Primary Sources**: Thorp and Kassouf (*Beat the Market: A Scientific Stock Market System*, 1967); Thorp (*A Man for All Markets*, 2017); Thorp (2006), "The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market", in *Handbook of Asset and Liability Management*, Volume 1, edited by Zenios and Ziemba; Kelly (*A New Interpretation of Information Rate*, 1956).
- **Master's Shoes (Anti-Pattern)**: Model risk from inputs; full-Kelly sizing on an overestimated edge produces deep drawdowns.

---

## 5. Jim Simons (1938 - 2024)
- **Lineage**: Quantitative Statistical Arbitrage and Systematic Signal Extraction.
- **Core Principles**:
  - **Scientific Method in Finance**: Zuckerman (2019) describes Renaissance Technologies building trading models from patterns found in large, carefully cleaned historical datasets.
  - **Hiring Scientists**: Zuckerman (2019) documents Simons recruiting mathematicians, physicists, statisticians and computer scientists rather than traditional Wall Street traders.
  - **Many Small Edges**: Zuckerman (2019) quotes Robert Mercer saying the firm was right on only about 50.75 percent of its trades, with profits coming from applying that small edge across a very large number of trades.
- **Concrete Execution Rules**:
  - Codex practice: require statistical significance after multiple-testing penalties before trading a pattern, whether or not it has a narrative explanation.
  - Codex practice: clean historical data for corporate actions, venue quirks and timestamp errors before testing anything on it.
- **Primary Sources**: Zuckerman (*The Man Who Solved the Market: How Jim Simons Launched the Quant Revolution*, 2019); Simons, "Mathematics, Common Sense, and Good Luck: My Life and Careers", MIT School of Science Dean's Colloquium (2010).
- **Master's Shoes (Anti-Pattern)**: Crowding in statistical arbitrage factors leading to sudden factor unwinds, as in the August 2007 quant crisis studied by Khandani and Lo (2011), "What Happened to the Quants in August 2007? Evidence from Factors and Transactions Data", *Journal of Financial Markets*.

---

## 6. Paul Tudor Jones (born 1954)
- **Lineage**: Discretionary Global Macro and Technical Inflection Trading.
- **Core Principles**:
  - **Asymmetric Risk/Reward**: In his interview in Robbins (2014) Jones describes looking for trades that offer about five dollars of reward for each dollar of risk.
    At 5:1 the breakeven win rate is $1/(1+5) = 16.67\%$, and a 30% win rate gives an expectancy of $0.3 \times 5 - 0.7 \times 1 = 0.80$R per trade.
  - **The 200-Day Moving Average**: In the same interview Jones names the 200-day moving average of closing prices as his metric for whether to stay in or get out of a market.
  - **Defense First**: In Schwager (1989) Jones stresses that he is more concerned with controlling losses than with making money.
- **Concrete Execution Rules**:
  - Codex practice: cut a position as soon as the trade thesis is violated rather than hoping for recovery.
  - Codex practice: look for inflection points where consensus positioning is crowded.
- **Primary Sources**: Schwager (*Market Wizards*, 1989, Paul Tudor Jones chapter, which also covers his trading around the October 1987 crash); Robbins (*Money: Master the Game*, 2014, Paul Tudor Jones interview).
- **Master's Shoes (Anti-Pattern)**: Picking bottoms in sustained downtrends before price action confirms exhaustion.

---

## 7. Stanley Druckenmiller (born 1953)
- **Lineage**: Concentrated Macro and Liquidity Analysis.
- **Core Principles**:
  - **Liquidity Over Earnings**: In his January 18, 2015 speech at the Lost Tree Club, Druckenmiller says he learned early that earnings do not move the overall market; the Federal Reserve and the movement of liquidity do.
  - **Concentrated Conviction**: In the Druckenmiller chapter of Schwager (1992) he credits George Soros with the lesson that "It's not whether you're right or wrong that's important, but how much money you make when you're right and how much you lose when you're wrong."
- **Concrete Execution Rules**:
  - Codex practice: add to a working position only while the macro thesis keeps strengthening, and cut a losing trade when price action contradicts the thesis.
  - Codex practice: watch currency crosses and sovereign yield curve spreads as context for equity positioning.
- **Primary Sources**: Schwager (*The New Market Wizards*, 1992, Stanley Druckenmiller chapter); Druckenmiller, speech at the Lost Tree Club, North Palm Beach, January 18, 2015.
- **Master's Shoes (Anti-Pattern)**: Over-leveraging in choppy, range-bound regimes where false breakouts produce repeated whipsaw losses.

---

## 8. Richard Dennis (born 1949) and William Eckhardt
- **Lineage**: The Turtle Trading System and Systematic Trend Following.
- **Core Principles**:
  - **Trading Can Be Taught**: Dennis bet Eckhardt that trading could be taught, and trained two groups of novices recruited in December 1983 and December 1984 (Faith 2007; Covel 2007).
  - **Volatility-Normalized Sizing ($N$)**: $N$ is the 20-day exponential moving average of the true range, and one unit risks 1% of account equity per $N$ of price movement:
    $$\text{Unit Size} = \frac{1\% \times \text{Account Equity}}{N \times \text{Dollars per Point}}$$
- **Concrete Execution Rules** (Faith 2003, *The Original Turtle Trading Rules*):
  - System 1 entry: breakout above the 20-day high (long) or below the 20-day low (short).
  - System 2 entry: breakout above the 55-day high (long) or below the 55-day low (short).
  - Pyramiding: add one unit for every $\frac{1}{2} N$ of favourable movement, up to 4 units in a single market.
  - Stop loss: $2N$ from the most recent entry, with earlier units' stops raised by $\frac{1}{2} N$ as units are added.
- **Primary Sources**: Faith (*The Original Turtle Trading Rules*, 2003); Faith (*Way of the Turtle*, 2007); Covel (*The Complete TurtleTrader*, 2007).
- **Master's Shoes (Anti-Pattern)**: Long sideways markets in which repeated breakout whipsaws build large cumulative drawdowns.

---

## 9. Peter Lynch (born 1944)
- **Lineage**: Growth at a Reasonable Price (GARP) and Qualitative Scuttlebutt.
- **Core Principles**:
  - **Price/Earnings to Growth (PEG Ratio)**: Lynch writes that the P/E of a fairly priced company equals its growth rate, so a ratio of P/E to growth below 1 is attractive:
    $$\text{PEG} = \frac{\text{P/E Ratio}}{\text{Earnings Growth Rate (\%)}}$$
  - **Invest in What You Know**: Use everyday observation of products and stores as an early lead, then do the research before buying.
  - **Categorization of Equities**: Slow Growers, Stalwarts, Fast Growers, Cyclicals, Turnarounds and Asset Plays.
- **Concrete Execution Rules**:
  - Avoid "whisper stocks", the long-shot stories with no earnings that Lynch warns against.
  - Do not sell a winner only because its price has risen if the story behind it is intact.
  - In cyclicals, a low P/E can signal peak earnings and a high P/E depressed trough earnings.
- **Primary Sources**: Lynch with John Rothchild (*One Up On Wall Street*, 1989); Lynch with John Rothchild (*Beating the Street*, 1993).
- **Master's Shoes (Anti-Pattern)**: Confusing a familiar consumer product with a durable moat; holding declining retail franchises disrupted by scale competitors.

---

## 10. Howard Marks (born 1946)
- **Lineage**: Credit Cycles, Second-Level Thinking, and Risk Asymmetry.
- **Core Principles**:
  - **Second-Level Thinking**: First-level thinking judges a good company a buy; second-level thinking asks what the consensus already believes and what is priced in, so a good company priced as a great one can be a sell (*The Most Important Thing*, 2011).
  - **The Pendulum of Investor Psychology**: Sentiment swings between euphoria and depression, and risk is highest when investors believe there is none (*The Most Important Thing*; *Mastering the Market Cycle*, 2018).
  - **Risk Control**: Marks defines the risk that matters as the probability of permanent loss rather than volatility.
- **Concrete Execution Rules**:
  - Codex practice: become more defensive when credit spreads are tight and lending terms loosen.
  - Codex practice: deploy capital when prices are depressed by forced selling.
- **Primary Sources**: Marks (*The Most Important Thing: Uncommon Sense for the Thoughtful Investor*, 2011); Marks (*Mastering the Market Cycle*, 2018); Oaktree Capital memos (1990 onward, oaktreecapital.com).
- **Master's Shoes (Anti-Pattern)**: Being early; sitting in defensive cash through a long expansion, which for a time looks no different from being wrong.

---

## In this repo and The-Distinguished-Engineer

- Backing script: [mkt_hist_00_curriculum.py](../code/mkt_hist_00_curriculum.py) asserts the 5:1 breakeven win rate (16.67%) and expectancy (0.80R) in exact rational arithmetic and checks the expectancy against a seeded simulation of 2,000,000 Bernoulli trades within five standard errors.
- Turtle sizing and Kelly sizing can be practised in the `pos_sizing` Trading Lab engine.

---

## Navigation

- **Master Hub**: [[16-Trading-and-Investing/MARKETS_HUB|Markets Mastery OS Master Hub]]
- **Foundational Canon**: [[16-Trading-and-Investing/00-Curriculum/Canon|Foundational Canon]]
- **Learning Path**: [[16-Trading-and-Investing/00-Curriculum/Learning-Path|Learning Path and Stages]]
