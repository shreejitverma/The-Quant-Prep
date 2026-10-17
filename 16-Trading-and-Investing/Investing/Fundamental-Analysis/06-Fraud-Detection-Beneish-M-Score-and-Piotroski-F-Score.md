---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Altman (1968) - Financial Ratios Discriminant Analysis and the Prediction of Corporate Bankruptcy, Beneish (1999) - The Detection of Earnings Manipulation, Piotroski (2000) - Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers]
---

# Fraud Detection, Beneish M-Score, and Piotroski F-Score

## TL;DR

- The Beneish M-Score is an empirical 8-variable probabilistic model designed to detect corporate earnings manipulation before public restatements occur.
- A Beneish M-Score greater than -1.78 signals a high probability of accounting manipulation; the model successfully flagged Enron (-0.24) years before its bankruptcy.
- The Piotroski F-Score is a 9-point binary fundamental momentum framework that separates resilient value companies from bankrupt value traps.
- Applying the Piotroski F-Score to the highest Book-to-Market (value) decile historically boosted annual investment returns by 7.5% by systematically eliminating deteriorating businesses.
- Altman Z-Score predicts financial distress and insolvency risk, whereas Beneish M-Score detects active managerial fraud and Piotroski F-Score measures operational trajectory.

## Learning objectives

- Formulate, compute, and interpret all eight sub-indices of the Beneish M-Score.
- Benchmark M-Score against critical thresholds (-1.78 and -2.22) to classify earnings manipulation risk.
- Construct the 9-point Piotroski F-Score across profitability, leverage, and operating efficiency dimensions.
- Integrate the F-Score into quantitative value screening to eliminate value traps.
- Differentiate the diagnostic capabilities of Altman Z-Score, Beneish M-Score, and Piotroski F-Score.

## Core concepts

### 1. The Beneish M-Score: Architecture and Mathematical Specification

Messod Beneish (1999) developed a probit regression model to identify firms systematically inflating reported earnings.
The complete 8-variable model is specified as:

$$\begin{aligned}
M = &-4.84 + 0.920 \times \text{DSRI} + 0.528 \times \text{GMI} + 0.404 \times \text{AQI} + 0.892 \times \text{SGI} \\
&+ 0.115 \times \text{DEPI} - 0.172 \times \text{SGAI} + 4.037 \times \text{TATA} + 0.0327 \times \text{LVGI}
\end{aligned}$$

```
+-----------------------------------------------------------------------+
|                    BENEISH M-SCORE VARIABLE TAXONOMY                  |
+-----------------------------------------------------------------------+
| Index | Full Name                      | Economic Meaning             |
+-------+--------------------------------+------------------------------+
| DSRI  | Days Sales in Receivables      | Disproportionate growth in   |
|       | Index                          | uncollected revenue vs sales |
| GMI   | Gross Margin Index             | Deteriorating gross margins  |
|       |                                | tempting manipulation        |
| AQI   | Asset Quality Index            | Shifting expenses into       |
|       |                                | capitalized intangible assets|
| SGI   | Sales Growth Index             | Pressure on growth companies |
|       |                                | to maintain momentum         |
| DEPI  | Depreciation Index             | Slowing depreciation rates to|
|       |                                | boost operating profit       |
| SGAI  | SG&A Expenses Index            | Declining sales efficiency   |
|       |                                | or aggressive cost control   |
| LVGI  | Leverage Index                 | Rising debt covenant pressure|
|       |                                | incentivizing fabrication    |
| TATA  | Total Accruals to Total Assets | Non-cash accounting share of |
|       |                                | total net operating income   |
+-----------------------------------------------------------------------+
```

#### Detailed Formulas for the 8 Variables

1. **Days Sales in Receivables Index (DSRI)**:
   $$\text{DSRI} = \frac{\text{Receivables}_t / \text{Sales}_t}{\text{Receivables}_{t-1} / \text{Sales}_{t-1}}$$
   A ratio > 1.0 indicates receivables outpaced sales, signaling accelerated revenue recognition or channel stuffing.

2. **Gross Margin Index (GMI)**:
   $$\text{GMI} = \frac{\text{Gross Margin}_{t-1}}{\text{Gross Margin}_t} = \frac{(\text{Sales}_{t-1} - \text{COGS}_{t-1}) / \text{Sales}_{t-1}}{(\text{Sales}_t - \text{COGS}_t) / \text{Sales}_t}$$
   A ratio > 1.0 indicates deteriorating gross margins, increasing executive pressure to engage in earnings management.

3. **Asset Quality Index (AQI)**:
   $$\text{Non-Current Assets ex PP&E} = 1 - \left( \frac{\text{Current Assets}_t + \text{Net PP&E}_t}{\text{Total Assets}_t} \right)$$
   $$\text{AQI} = \frac{1 - (\text{Current Assets}_t + \text{Net PP&E}_t + \text{Securities}_t) / \text{Total Assets}_t}{1 - (\text{Current Assets}_{t-1} + \text{Net PP&E}_{t-1} + \text{Securities}_{t-1}) / \text{Total Assets}_{t-1}}$$
   A ratio > 1.0 indicates a growing proportion of assets are capitalized deferred costs and intangibles rather than physical plant.

4. **Sales Growth Index (SGI)**:
   $$\text{SGI} = \frac{\text{Sales}_t}{\text{Sales}_{t-1}}$$
   Fast-growing firms face intense pressure to maintain high price-to-earnings multiples.

5. **Depreciation Index (DEPI)**:
   $$\text{Depreciation Rate} = \frac{\text{Depreciation}}{\text{Gross PP&E} + \text{Depreciation}}$$
   $$\text{DEPI} = \frac{\text{Depreciation Rate}_{t-1}}{\text{Depreciation Rate}_t}$$
   A ratio > 1.0 indicates that depreciation rates have slowed, suggesting extended asset lives to lower expense.

6. **Sales, General, and Administrative Expenses Index (SGAI)**:
   $$\text{SGAI} = \frac{\text{SG&A}_t / \text{Sales}_t}{\text{SG&A}_{t-1} / \text{Sales}_{t-1}}$$
   A ratio > 1.0 reflects declining marketing and administrative efficiency.

7. **Leverage Index (LVGI)**:
   $$\text{Leverage} = \frac{\text{Current Liabilities} + \text{Long-Term Debt}}{\text{Total Assets}}$$
   $$\text{LVGI} = \frac{\text{Leverage}_t}{\text{Leverage}_{t-1}}$$
   A ratio > 1.0 indicates rising leverage, heightening risk of debt covenant violations.

8. **Total Accruals to Total Assets (TATA)**:
   $$\text{TATA} = \frac{\text{Net Income}_t - \text{Operating Cash Flow}_t}{\text{Total Assets}_t}$$
   Higher accruals reflect lower earnings quality and cash conversion.

#### M-Score Decision Thresholds

```
M-Score Value:
 < -2.22 : Normal accounting; extremely low probability of manipulation.
 -2.22 to -1.78 : Moderate risk zone; warrants forensic footnote review.
 > -1.78 : HIGH PROBABILITY OF MANIPULATION (Statistically Significant Flag).
```

### 2. The Piotroski F-Score: Fundamental Momentum Scoring

Joseph Piotroski (2000) created a discrete 9-point fundamental score designed specifically to evaluate high book-to-market (low valuation) equities.
Each metric is scored as a binary value: 1 point if positive/improving, 0 points if negative/deteriorating.

$$\text{Piotroski F-Score} = \sum_{i=1}^9 F_i \quad \in [0, 9]$$

```
+-----------------------------------------------------------------------+
|                    PIOTROSKI 9-POINT SCORING RUBRIC                   |
+-----------------------------------------------------------------------+
| GROUP 1: PROFITABILITY SIGNALS (4 Points Max)                         |
|   F1 (ROA)      : Return on Assets > 0                                |
|   F2 (CFO)      : Cash Flow from Operations > 0                       |
|   F3 (Delta ROA): ROA(t) > ROA(t-1)                                   |
|   F4 (ACCRUAL)  : CFO(t) > ROA(t) (Cash flow exceeds net income)      |
+-----------------------------------------------------------------------+
| GROUP 2: LEVERAGE, LIQUIDITY, AND DILUTION (3 Points Max)             |
|   F5 (Delta LEV): Long-Term Debt / Assets(t) < Debt / Assets(t-1)     |
|   F6 (Delta LIQ): Current Ratio(t) > Current Ratio(t-1)               |
|   F7 (EQ DILUT) : Common Shares Outstanding(t) <= Shares(t-1)         |
+-----------------------------------------------------------------------+
| GROUP 3: OPERATING EFFICIENCY SIGNALS (2 Points Max)                  |
|   F8 (Delta MAR): Gross Margin(t) > Gross Margin(t-1)                 |
|   F9 (Delta TRN): Asset Turnover(t) > Asset Turnover(t-1)             |
+-----------------------------------------------------------------------+
```

#### Portfolio Implementation and Excess Returns

Piotroski demonstrated that value stocks are heavily populated by financially distressed companies (value traps).
A quantitative screen combining value with F-Score generates powerful risk-adjusted alpha:
- **F-Score 8 to 9 (Strong Fundamentals)**: High historical outperformance, robust balance sheets, accelerating cash flows.
- **F-Score 0 to 2 (Weak Fundamentals)**: High probability of bankruptcy, dilutive share issuances, deteriorating margins.
- A long/short strategy (Long Top Quintile BM with F-Score 8-9, Short Top Quintile BM with F-Score 0-2) generated 23% annualized returns between 1972 and 1996.

### 3. Comparing Fraud, Distress, and Quality Frameworks

| Attribute | Beneish M-Score | Piotroski F-Score | Altman Z-Score |
|---|---|---|---|
| **Primary Objective** | Detect accounting manipulation & fraud | Measure operational momentum & value quality | Predict bankruptcy & insolvency probability |
| **Statistical Technique** | Probit regression (continuous score) | Binary scoring heuristic (integer 0-9) | Multiple discriminant analysis (MDA) |
| **Key Risk Flag** | Score > -1.78 | Score $\le$ 3 | Score < 1.81 (Distress Zone) |
| **Primary Data Source** | 2 years of Income Statement & Balance Sheet | 2 years of 3 Financial Statements | Balance Sheet, Income Statement, Market Cap |
| **Market Role** | Short screening & forensic risk audit | Long value screening & fundamental quality filter | Credit risk, debt covenants, distress shorting |

```
Altman Z-Score Formula (Manufacturing):
Z = 1.2*(Working Capital/Assets) + 1.4*(Retained Earnings/Assets) + 3.3*(EBIT/Assets) + 0.6*(Market Cap/Total Debt) + 0.999*(Sales/Assets)
Thresholds: Z < 1.81 (Distress Zone), 1.81 <= Z <= 2.99 (Grey Zone), Z > 2.99 (Safe Zone)
```

## Worked numerical example

Evaluate Apex Logistics across two fiscal years:

| Account ($ Millions) | Year 1 ($t-1$) | Year 2 ($t$) |
|---|---|---|
| Sales (Revenue) | 800.0 | 1,040.0 (+30.0%) |
| Cost of Goods Sold (COGS) | 520.0 | 702.0 |
| Gross Profit | 280.0 (35.0%) | 338.0 (32.5%) |
| SG&A Expenses | 120.0 (15.0%) | 176.8 (17.0%) |
| Operating Income (EBIT) | 160.0 | 161.2 |
| Net Income | 90.0 | 85.0 |
| Operating Cash Flow (CFO) | 110.0 | 40.0 |
| Accounts Receivable | 80.0 | 160.0 (+100.0%) |
| Current Assets | 220.0 | 330.0 |
| Net PP&E | 300.0 | 350.0 |
| Total Assets | 600.0 | 780.0 |
| Current Liabilities | 100.0 | 160.0 |
| Long-Term Debt | 150.0 | 220.0 |
| Common Shares Outstanding (M) | 50.0 | 52.0 (+4.0%) |
| Depreciation Expense | 30.0 | 25.0 |

### Part 1: Compute Beneish M-Score

1. **DSRI**:
   $$\text{Rec/Sales}_t = \frac{160}{1040} = 0.1538; \quad \text{Rec/Sales}_{t-1} = \frac{80}{800} = 0.1000$$
   $$\text{DSRI} = \frac{0.1538}{0.1000} = 1.5385$$

2. **GMI**:
   $$\text{GM}_{t-1} = \frac{280}{800} = 0.3500; \quad \text{GM}_t = \frac{338}{1040} = 0.3250$$
   $$\text{GMI} = \frac{0.3500}{0.3250} = 1.0769$$

3. **AQI**:
   $$\text{Asset Non-PP&E/CA}_t = 1 - \frac{330 + 350}{780} = 1 - \frac{680}{780} = 1 - 0.8718 = 0.1282$$
   $$\text{Asset Non-PP&E/CA}_{t-1} = 1 - \frac{220 + 300}{600} = 1 - \frac{520}{600} = 1 - 0.8667 = 0.1333$$
   $$\text{AQI} = \frac{0.1282}{0.1333} = 0.9617$$

4. **SGI**:
   $$\text{SGI} = \frac{1040}{800} = 1.3000$$

5. **DEPI**:
   $$\text{Gross PP&E approx} = 300 + 30 = 330; \quad \text{Dep Rate}_{t-1} = \frac{30}{330} = 0.0909$$
   $$\text{Gross PP&E approx}_t = 350 + 25 = 375; \quad \text{Dep Rate}_t = \frac{25}{375} = 0.0667$$
   $$\text{DEPI} = \frac{0.0909}{0.0667} = 1.3628$$

6. **SGAI**:
   $$\text{SGA/Sales}_t = \frac{176.8}{1040} = 0.1700; \quad \text{SGA/Sales}_{t-1} = \frac{120}{800} = 0.1500$$
   $$\text{SGAI} = \frac{0.1700}{0.1500} = 1.1333$$

7. **LVGI**:
   $$\text{Lev}_t = \frac{160 + 220}{780} = \frac{380}{780} = 0.4872; \quad \text{Lev}_{t-1} = \frac{100 + 150}{600} = \frac{250}{600} = 0.4167$$
   $$\text{LVGI} = \frac{0.4872}{0.4167} = 1.1692$$

8. **TATA**:
   $$\text{TATA} = \frac{\text{Net Income}_t - \text{CFO}_t}{\text{Total Assets}_t} = \frac{85.0 - 40.0}{780.0} = \frac{45.0}{780.0} = 0.0577$$

#### Compute M-Score:
$$\begin{aligned}
M = &-4.84 + 0.920(1.5385) + 0.528(1.0769) + 0.404(0.9617) + 0.892(1.3000) \\
&+ 0.115(1.3628) - 0.172(1.1333) + 4.037(0.0577) + 0.0327(1.1692) \\
M = &-4.84 + 1.4154 + 0.5686 + 0.3885 + 1.1596 + 0.1567 - 0.1949 + 0.2329 + 0.0382 \\
M = &-1.075
\end{aligned}$$

M-Score Verdict:
Apex Logistics yields an M-Score of -1.075, substantially higher than the critical threshold of -1.78.
This signals a high statistical probability of accounting manipulation, driven by extreme receivables expansion (DSRI = 1.54) and slowing depreciation (DEPI = 1.36).

### Part 2: Compute Piotroski F-Score

1. **F_ROA**: Net Income ($85M) > 0 -> **1 Point**.
2. **F_CFO**: CFO ($40M) > 0 -> **1 Point**.
3. **F_DROA**: $\text{ROA}_t = 85/780 = 10.9\%$; $\text{ROA}_{t-1} = 90/600 = 15.0\%$. $\Delta \text{ROA} < 0$ -> **0 Points**.
4. **F_ACCRUAL**: $\text{CFO / Assets}_t = 40/780 = 5.1\% < \text{ROA}_t (10.9\%)$ -> **0 Points**.
5. **F_DLEVER**: Long-Term Debt / Assets: $220/780 = 28.2\%$ vs $150/600 = 25.0\%$ (Leverage increased) -> **0 Points**.
6. **F_DLIQUID**: Current Ratio: $330/160 = 2.06$ vs $220/100 = 2.20$ (Liquidity worsened) -> **0 Points**.
7. **F_EQ**: Shares increased from 50M to 52M (Dilution occurred) -> **0 Points**.
8. **F_DMARGIN**: Gross margin fell from 35.0% to 32.5% -> **0 Points**.
9. **F_DTURN**: Asset Turnover: $1040/780 = 1.333$ vs $800/600 = 1.333$ (Flat / no improvement) -> **0 Points**.

F-Score Total = 2 / 9 Points.
Piotroski Verdict:
Apex Logistics scores a dismal 2 out of 9, placing it squarely in the distress / short candidate category with deteriorating profitability, declining liquidity, shareholder dilution, and high accruals.

## Practice questions

> [!question] mkt-fa-161 | What is the primary purpose of the Beneish M-Score?
> To calculate the empirical statistical probability that a company is manipulating its reported accounting earnings.

> [!question] mkt-fa-162 | What is the critical threshold for the Beneish M-Score indicating manipulation?
> An M-Score greater than -1.78 indicates a statistically significant probability of earnings manipulation.

> [!question] mkt-fa-163 | What famous corporate collapse did the Beneish M-Score identify prior to public revelation?
> Enron Corporation, which had a glaringly flagged M-Score of -0.24 in 1999 and 2000.

> [!question] mkt-fa-164 | What does a Days Sales in Receivables Index (DSRI) > 1.0 indicate in the M-Score?
> Receivables grew faster than sales, indicating accelerating credit terms, uncollected billings, or premature revenue recognition.

> [!question] mkt-fa-165 | Why does a Gross Margin Index (GMI) > 1.0 increase the probability of manipulation?
> Deteriorating gross margins create severe pressure on corporate management to engage in aggressive accounting to meet earnings targets.

> [!question] mkt-fa-166 | What does the Asset Quality Index (AQI) measure in the Beneish model?
> The proportion of total assets composed of non-current intangible assets and deferred costs relative to tangible property, plant, and equipment.

> [!question] mkt-fa-167 | How does a Depreciation Index (DEPI) > 1.0 signal potential accounting abuse?
> It shows that the current effective depreciation rate has declined, suggesting management lengthened asset lives to reduce operating expenses.

> [!question] mkt-fa-168 | What does the Total Accruals to Total Assets (TATA) variable capture in the M-Score?
> The degree to which reported accounting net income is supported by non-cash accruals rather than physical operating cash flow.

> [!question] mkt-fa-169 | What is the 5-variable version of the Beneish M-Score?
> A truncated specification omitting SGI, DEPI, and SGAI, used when detailed footnote data or multi-year historical series are unavailable.

> [!question] mkt-fa-170 | What is the primary design goal of the Piotroski F-Score?
> To separate winning high-quality value stocks from value traps among companies trading at high book-to-market valuations.

> [!question] mkt-fa-171 | How many total binary criteria comprise the Piotroski F-Score?
> Nine discrete binary tests, producing an aggregate score between 0 and 9.

> [!question] mkt-fa-172 | What are the three core categories evaluated by the Piotroski F-Score?
> Profitability signals (4 points), Leverage/Liquidity/Dilution signals (3 points), and Operating Efficiency signals (2 points).

> [!question] mkt-fa-173 | How does Piotroski score the accrual relationship in test F_ACCRUAL?
> 1 point if Operating Cash Flow exceeds Return on Assets (CFO > ROA); 0 points if net income exceeds cash flow.

> [!question] mkt-fa-174 | How is equity dilution tested in the Piotroski F-Score?
> 1 point if common shares outstanding in the current year are less than or equal to the prior year (no dilutive equity issued).

> [!question] mkt-fa-175 | What is considered a high (strong) Piotroski F-Score?
> An F-Score of 8 or 9, signifying exceptional financial health and operating momentum.

> [!question] mkt-fa-176 | What is considered a low (distressed) Piotroski F-Score?
> An F-Score of 0, 1, or 2, identifying financially deteriorating companies and prime short candidates.

> [!question] mkt-fa-177 | What historical annualized excess return did Piotroski find by buying high F-Score value stocks and shorting low F-Score value stocks?
> Approximately 23% annualized spread between 1972 and 1996.

> [!question] mkt-fa-178 | What is the primary difference between Altman Z-Score and Beneish M-Score?
> Altman Z-Score evaluates bankruptcy and default probability, while Beneish M-Score specifically evaluates fraud and accounting manipulation.

> [!question] mkt-fa-179 | What is the distress threshold for the Altman Z-Score for public manufacturing firms?
> A Z-Score below 1.81 places the company in the bankruptcy Distress Zone.

> [!question] mkt-fa-180 | What is the safe zone threshold for the Altman Z-Score?
> A Z-Score above 2.99 indicates negligible insolvency probability.

> [!question] mkt-fa-181 | Why can a fraudulent company have an apparently safe Altman Z-Score?
> Because fabricated earnings and overstated assets artificially boost working capital, EBIT, and equity book values in the Z-Score equation.

> [!question] mkt-fa-182 | Can a financially distressed company have a clean Beneish M-Score?
> Yes; a distressed firm with honest, deteriorating accounting will show an unmanipulated M-Score despite collapsing fundamentals.

> [!question] mkt-fa-183 | What does the Leverage Index (LVGI) > 1.0 capture in the Beneish model?
> Increasing total financial debt relative to assets, which escalates default risk and creates incentives to inflate earnings.

> [!question] mkt-fa-184 | What does a negative coefficient on SGAI in the Beneish model signify?
> Abnormally aggressive cuts to SG&A relative to sales can signal desperation to manufacture operating margins.

> [!question] mkt-fa-185 | How does the Piotroski F-Score define improvement in liquidity?
> Current Ratio in the current fiscal year exceeding the Current Ratio in the preceding fiscal year.

> [!question] mkt-fa-186 | How does the Piotroski F-Score define improvement in asset efficiency?
> Asset Turnover (Revenue / Total Assets) in the current year exceeding Asset Turnover in the preceding year.

> [!question] mkt-fa-187 | Why is the Piotroski F-Score particularly effective on small-cap equities?
> Small caps receive less analyst coverage and institutional scrutiny, allowing fundamental mispricings to persist longer.

> [!question] mkt-fa-188 | How does the Beneish M-Score perform on financial institutions and banks?
> Poorly; bank balance sheets do not distinguish operating from financing working capital, requiring specialized credit models.

> [!question] mkt-fa-189 | What is the false positive rate of the Beneish M-Score at the -1.78 threshold?
> Approximately 8.8% in Beneish's original sample, while correctly identifying 76% of known accounting manipulators.

> [!question] mkt-fa-190 | How does high Sales Growth Index (SGI) elevate manipulation risk?
> When growth decelerates, growth-oriented managers face intense valuation penalties, driving aggressive revenue recognition to preserve multiples.

> [!question] mkt-fa-191 | What is the effect of combining low valuation (high BM) with a high F-Score?
> It filters out value traps that are cheap for structural solvency reasons, retaining only underpriced companies with operational tailwinds.

> [!question] mkt-fa-192 | What is the optimal quantitative workflow combining Beneish, Piotroski, and Altman?
> Screen for value or growth, filter out bankruptcy risk (Z < 1.81), eliminate manipulation risk (M > -1.78), and rank longs by fundamental momentum (F >= 8).

---

## Further reading

- Altman, E. I. (1968). *Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy*. The Journal of Finance, 23(4), 589-609.
- Beneish, M. D. (1999). *The Detection of Earnings Manipulation*. Financial Analysts Journal, 55(5), 24-36.
- Dechow, P. M., Ge, W., Larson, C. R., & Sloan, R. G. (2011). *Predicting Material Accounting Misstatements*. Contemporary Accounting Research, 28(1), 17-82.
- Piotroski, J. D. (2000). *Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers*. Journal of Accounting Research, 38, 1-41.
