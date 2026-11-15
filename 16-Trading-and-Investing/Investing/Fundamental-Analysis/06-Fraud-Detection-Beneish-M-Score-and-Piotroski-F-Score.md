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

- The Beneish M-Score is an 8-variable probit model, estimated by Beneish (1999) on firms caught manipulating earnings, that screens for manipulation before it is publicly discovered; the paper reports that it identifies about half of the manipulators before discovery.
- An M-Score above -1.78 is the cost-weighted cut-off for the eight-variable model; the -2.22 cut-off seen on many screening sites is a looser screen that this note could not trace to the paper's tables.
- The Piotroski F-Score is a 9-point binary score of financial strength that separates stronger from weaker firms among high book-to-market (value) stocks.
- Piotroski (2000) reports that selecting financially strong firms within the highest book-to-market quintile raised the mean return by at least 7.5% a year over 1976-1996.
- Altman Z-Score predicts financial distress and insolvency risk, whereas Beneish M-Score detects active managerial fraud and Piotroski F-Score measures operational trajectory.

## Learning objectives

- Formulate, compute, and interpret all eight sub-indices of the Beneish M-Score.
- Benchmark M-Score against critical thresholds (-1.78 and -2.22) to classify earnings manipulation risk.
- Construct the 9-point Piotroski F-Score across profitability, leverage, and operating efficiency dimensions.
- Integrate the F-Score into quantitative value screening to eliminate value traps.
- Differentiate the diagnostic capabilities of Altman Z-Score, Beneish M-Score, and Piotroski F-Score.

## Core concepts

### 1. The Beneish M-Score: Architecture and Mathematical Specification

Messod Beneish (1999) estimated a probit model on a sample of known manipulators and Compustat control firms to identify firms inflating reported earnings.
The 8-variable model is:

$$\begin{aligned}
M = &-4.84 + 0.920 \times \text{DSRI} + 0.528 \times \text{GMI} + 0.404 \times \text{AQI} + 0.892 \times \text{SGI} \\
&+ 0.115 \times \text{DEPI} - 0.172 \times \text{SGAI} + 4.679 \times \text{TATA} - 0.327 \times \text{LVGI}
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
   $$\text{AQI} = \frac{1 - (\text{Current Assets}_t + \text{Net PP&E}_t) / \text{Total Assets}_t}{1 - (\text{Current Assets}_{t-1} + \text{Net PP&E}_{t-1}) / \text{Total Assets}_{t-1}}$$
   Some later implementations also exclude securities from the numerator's asset set; use one definition consistently.
   A ratio > 1.0 indicates a growing proportion of assets are capitalized deferred costs and intangibles rather than physical plant.

4. **Sales Growth Index (SGI)**:
   $$\text{SGI} = \frac{\text{Sales}_t}{\text{Sales}_{t-1}}$$
   Fast-growing firms face intense pressure to maintain high price-to-earnings multiples.

5. **Depreciation Index (DEPI)**:
   $$\text{Depreciation Rate} = \frac{\text{Depreciation}}{\text{Depreciation} + \text{Net PP&E}}$$
   $$\text{DEPI} = \frac{\text{Depreciation Rate}_{t-1}}{\text{Depreciation Rate}_t}$$
   A ratio > 1.0 indicates that depreciation rates have slowed, suggesting extended asset lives to lower expense.

6. **Sales, General, and Administrative Expenses Index (SGAI)**:
   $$\text{SGAI} = \frac{\text{SG&A}_t / \text{Sales}_t}{\text{SG&A}_{t-1} / \text{Sales}_{t-1}}$$
   A ratio > 1.0 reflects declining marketing and administrative efficiency.
   Beneish expected a positive relation with manipulation, but the estimated coefficient (-0.172) is negative.

7. **Leverage Index (LVGI)**:
   $$\text{Leverage} = \frac{\text{Current Liabilities} + \text{Long-Term Debt}}{\text{Total Assets}}$$
   $$\text{LVGI} = \frac{\text{Leverage}_t}{\text{Leverage}_{t-1}}$$
   A ratio > 1.0 indicates rising leverage, heightening risk of debt covenant violations.
   Beneish expected rising leverage to raise the incentive to manipulate, but in the estimated model LVGI carries a negative coefficient (-0.327), so rising leverage on its own lowers the M-Score.

8. **Total Accruals to Total Assets (TATA)**:
   Beneish (1999) measured total accruals from the balance sheet, as the change in working capital accounts other than cash less depreciation, scaled by total assets.
   Most screening tools now use the cash flow version, which this note's example uses:
   $$\text{TATA} = \frac{\text{Income from Continuing Operations}_t - \text{Operating Cash Flow}_t}{\text{Total Assets}_t}$$
   Higher accruals reflect lower earnings quality and cash conversion.

#### M-Score Decision Thresholds

The M-Score is a probit index, so $\Phi(M)$ (the standard normal distribution function) converts it to a model probability.
Because the model was fitted on a sample that over-represents manipulators, $\Phi(M)$ is a ranking device rather than a population probability.
Beneish chose cut-offs that minimize the expected cost of misclassification for different ratios of the cost of missing a manipulator to the cost of a false alarm.
Across those cut-offs, secondary summaries of the paper report that the model identifies 38% to 76% of manipulators while misclassifying 3.5% to 17.5% of non-manipulators.

- $M > -1.78$, that is $\Phi(M) > 3.75\%$: the cut-off used with the eight-variable model; flag for forensic review.
- $M > -2.22$, that is $\Phi(M) > 1.32\%$: a looser screen widely quoted online and often attached to five-variable versions of the model; it flags more firms, including many false positives.
- A flag starts an investigation of the footnotes; it is not evidence of fraud on its own.

### 2. The Piotroski F-Score: Fundamental Momentum Scoring

Joseph Piotroski (2000) built a 9-point score from binary signals of financial strength and applied it to firms in the highest book-to-market quintile.
Each signal scores 1 if its realization is good and 0 if bad; ROA, CFO and ACCRUAL are scaled by beginning-of-year total assets and asset turnover uses beginning-of-year assets.

$$\text{Piotroski F-Score} = \sum_{i=1}^9 F_i \quad \in [0, 9]$$

```
+-----------------------------------------------------------------------+
|                    PIOTROSKI 9-POINT SCORING RUBRIC                   |
+-----------------------------------------------------------------------+
| GROUP 1: PROFITABILITY SIGNALS (4 Points Max)                         |
|   F1 (ROA)      : NI before extraordinary items / assets > 0         |
|   F2 (CFO)      : Cash Flow from Operations / assets > 0              |
|   F3 (Delta ROA): ROA(t) > ROA(t-1)                                   |
|   F4 (ACCRUAL)  : CFO(t) > ROA(t) (Cash flow exceeds net income)      |
+-----------------------------------------------------------------------+
| GROUP 2: LEVERAGE, LIQUIDITY, AND DILUTION (3 Points Max)             |
|   F5 (Delta LEV): LT Debt / Avg Assets fell versus the prior year     |
|   F6 (Delta LIQ): Current Ratio(t) > Current Ratio(t-1)               |
|   F7 (EQ_OFFER) : No common equity issued in the prior year           |
+-----------------------------------------------------------------------+
| GROUP 3: OPERATING EFFICIENCY SIGNALS (2 Points Max)                  |
|   F8 (Delta MAR): Gross Margin(t) > Gross Margin(t-1)                 |
|   F9 (Delta TRN): Asset Turnover(t) > Asset Turnover(t-1)             |
+-----------------------------------------------------------------------+
```

#### Portfolio Implementation and Excess Returns

Piotroski notes that the average high book-to-market firm is financially distressed, and his results (1976-1996, 14,043 high book-to-market firm-years) show:
- **High F-Score (8 or 9)**: the "expected winners"; selecting them raised the mean return of a high book-to-market investor by at least 7.5% a year.
- **Low F-Score (0 or 1)**: the "expected losers".
- Buying expected winners and shorting expected losers generated a 23% annual return between 1976 and 1996.
- The benefits were concentrated in small and medium-sized firms, firms with low share turnover and firms with no analyst following.

### 3. Comparing Fraud, Distress, and Quality Frameworks

| Attribute | Beneish M-Score | Piotroski F-Score | Altman Z-Score |
|---|---|---|---|
| **Primary Objective** | Detect accounting manipulation & fraud | Measure operational momentum & value quality | Predict bankruptcy & insolvency probability |
| **Statistical Technique** | Probit regression (continuous score) | Binary scoring heuristic (integer 0-9) | Multiple discriminant analysis (MDA) |
| **Key Risk Flag** | Score > -1.78 | Score 0 or 1 (Piotroski's low group) | Score < 1.81 (Distress Zone) |
| **Primary Data Source** | 2 years of Income Statement & Balance Sheet | 2 years of 3 Financial Statements | Balance Sheet, Income Statement, Market Cap |
| **Market Role** | Short screening & forensic risk audit | Long value screening & fundamental quality filter | Credit risk, debt covenants, distress shorting |

```
Altman (1968) Z-Score (public manufacturing firms), ratios as decimals:
Z = 1.2*(Working Capital/Assets) + 1.4*(Retained Earnings/Assets) + 3.3*(EBIT/Assets) + 0.6*(Market Value of Equity/Book Value of Total Debt) + 0.999*(Sales/Assets)
Altman printed the first four weights as 0.012, 0.014, 0.033 and 0.006 with those ratios entered in percent.
In his sample every firm below 1.81 went bankrupt and every firm above 2.99 did not; 1.81 to 2.99 was his "zone of ignorance" (grey zone).
```

## Worked numerical example

Evaluate a hypothetical Apex Logistics across two fiscal years (income from continuing operations equals net income):

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
   $$\text{AQI} = \frac{0.12821}{0.13333} = 0.9615$$

4. **SGI**:
   $$\text{SGI} = \frac{1040}{800} = 1.3000$$

5. **DEPI**:
   $$\text{Dep} + \text{Net PP&E}_{t-1} = 30 + 300 = 330; \quad \text{Dep Rate}_{t-1} = \frac{30}{330} = 0.0909$$
   $$\text{Dep} + \text{Net PP&E}_t = 25 + 350 = 375; \quad \text{Dep Rate}_t = \frac{25}{375} = 0.0667$$
   $$\text{DEPI} = \frac{30/330}{25/375} = \frac{0.09091}{0.06667} = 1.3636$$

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
M = &-4.84 + 0.920(1.5385) + 0.528(1.0769) + 0.404(0.9615) + 0.892(1.3000) \\
&+ 0.115(1.3636) - 0.172(1.1333) + 4.679(0.0577) - 0.327(1.1692) \\
M = &-4.84 + 1.4154 + 0.5686 + 0.3885 + 1.1596 + 0.1568 - 0.1949 + 0.2699 - 0.3823 \\
M = &-1.458
\end{aligned}$$

M-Score Verdict:
Apex Logistics yields an M-Score of -1.458, above the -1.78 cut-off, so it is flagged for forensic review.
The model probability is $\Phi(-1.458) = 7.24\%$, about twice the $3.75\%$ at the cut-off; the largest contributions come from receivables growing far faster than sales (DSRI = 1.54) and sales growth itself (SGI = 1.30), with slowing depreciation (DEPI = 1.36) adding a little.

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
Apex Logistics scores 2 out of 9, one point above Piotroski's low group (0 or 1), with falling profitability, weaker liquidity, new shares issued (a 4% rise in the share count, used here as a proxy for an equity offering) and high accruals.
The example scales by year-end assets for simplicity; Piotroski scales ROA, CFO and accruals by beginning-of-year assets, which would need year-0 data here.

## Practice questions

> [!question]- mkt-fa-161 | What is the primary purpose of the Beneish M-Score?
> To screen for companies likely to be manipulating reported earnings, using eight financial-statement indices combined in a probit model; $\Phi(M)$ ranks firms but is not a population probability.

> [!question]- mkt-fa-162 | What is the critical threshold for the Beneish M-Score indicating manipulation?
> -1.78 for the eight-variable model, the cost-weighted cut-off ($\Phi(-1.78) = 3.75\%$); a score above it flags the firm for forensic review.
> The -2.22 figure quoted on many websites ($\Phi = 1.32\%$) is a looser screen, usually attached to five-variable versions.

> [!question]- mkt-fa-163 | What famous corporate collapse did the Beneish M-Score identify prior to public revelation?
> Enron is the story usually told: in spring 1998 a team of Cornell Johnson School MBA students recommended selling Enron and suggested it might be manipulating earnings (Cornell Daily Sun, 29 January 2007), and secondary accounts say the Beneish model was among their tools.
> No verified M-Score figure for Enron is quoted here.

> [!question]- mkt-fa-164 | What does a Days Sales in Receivables Index (DSRI) > 1.0 indicate in the M-Score?
> Receivables grew faster than sales, indicating accelerating credit terms, uncollected billings, or premature revenue recognition.

> [!question]- mkt-fa-165 | Why does a Gross Margin Index (GMI) > 1.0 increase the probability of manipulation?
> Deteriorating gross margins create severe pressure on corporate management to engage in aggressive accounting to meet earnings targets.

> [!question]- mkt-fa-166 | What does the Asset Quality Index (AQI) measure in the Beneish model?
> The proportion of total assets composed of non-current intangible assets and deferred costs relative to tangible property, plant, and equipment.

> [!question]- mkt-fa-167 | How does a Depreciation Index (DEPI) > 1.0 signal potential accounting abuse?
> It shows that the current effective depreciation rate has declined, suggesting management lengthened asset lives to reduce operating expenses.

> [!question]- mkt-fa-168 | What does the Total Accruals to Total Assets (TATA) variable capture in the M-Score?
> The degree to which reported accounting net income is supported by non-cash accruals rather than physical operating cash flow.

> [!question]- mkt-fa-169 | What is the 5-variable version of the Beneish M-Score?
> A reduced model built from five of the indices; versions circulating online differ in which five they keep and in their coefficients, so check the source before using one.
> Never apply the eight-variable model's -1.78 cut-off to a five-variable score.

> [!question]- mkt-fa-170 | What is the primary design goal of the Piotroski F-Score?
> To separate winning high-quality value stocks from value traps among companies trading at high book-to-market valuations.

> [!question]- mkt-fa-171 | How many total binary criteria comprise the Piotroski F-Score?
> Nine discrete binary tests, producing an aggregate score between 0 and 9.

> [!question]- mkt-fa-172 | What are the three core categories evaluated by the Piotroski F-Score?
> Profitability signals (4 points), Leverage/Liquidity/Dilution signals (3 points), and Operating Efficiency signals (2 points).

> [!question]- mkt-fa-173 | How does Piotroski score the accrual relationship in test F_ACCRUAL?
> 1 point if CFO scaled by beginning-of-year assets exceeds ROA (net income before extraordinary items over beginning-of-year assets), that is when accruals are negative; 0 otherwise.

> [!question]- mkt-fa-174 | How is equity dilution tested in the Piotroski F-Score?
> EQ_OFFER scores 1 if the firm did not issue common equity in the year before portfolio formation, 0 otherwise; a non-increasing share count is a common proxy.

> [!question]- mkt-fa-175 | What is considered a high (strong) Piotroski F-Score?
> An F-Score of 8 or 9, signifying exceptional financial health and operating momentum.

> [!question]- mkt-fa-176 | What is considered a low (distressed) Piotroski F-Score?
> Piotroski's low group is an F-Score of 0 or 1, the "expected losers" that formed the short side of his strategy.

> [!question]- mkt-fa-177 | What historical annualized excess return did Piotroski find by buying high F-Score value stocks and shorting low F-Score value stocks?
> A 23% annual return between 1976 and 1996 for buying high-score (8 or 9) and shorting low-score (0 or 1) firms within the highest book-to-market quintile (Piotroski 2000, abstract).

> [!question]- mkt-fa-178 | What is the primary difference between Altman Z-Score and Beneish M-Score?
> Altman Z-Score evaluates bankruptcy and default probability, while Beneish M-Score specifically evaluates fraud and accounting manipulation.

> [!question]- mkt-fa-179 | What is the distress threshold for the Altman Z-Score for public manufacturing firms?
> A Z-Score below 1.81 places the company in the bankruptcy Distress Zone.

> [!question]- mkt-fa-180 | What is the safe zone threshold for the Altman Z-Score?
> Above 2.99: in Altman's (1968) sample no firm above 2.99 went bankrupt; it is a low-risk zone, not a guarantee.

> [!question]- mkt-fa-181 | Why can a fraudulent company have an apparently safe Altman Z-Score?
> Because fabricated earnings and overstated assets artificially boost working capital, EBIT, and equity book values in the Z-Score equation.

> [!question]- mkt-fa-182 | Can a financially distressed company have a clean Beneish M-Score?
> Yes; a distressed firm with honest, deteriorating accounting will show an unmanipulated M-Score despite collapsing fundamentals.

> [!question]- mkt-fa-183 | What does the Leverage Index (LVGI) > 1.0 capture in the Beneish model?
> Rising leverage (current liabilities plus long-term debt over total assets), which Beneish expected to raise covenant pressure and the incentive to inflate earnings.
> In the estimated model its coefficient is negative (-0.327), so LVGI above 1 actually lowers M.

> [!question]- mkt-fa-184 | What does a negative coefficient on SGAI in the Beneish model signify?
> That the estimate went the opposite way from Beneish's hypothesis (he expected falling SG&A efficiency to raise manipulation risk); in the fitted model a rising SGAI slightly lowers M, so treat it as a weak variable rather than a signal in either direction.

> [!question]- mkt-fa-185 | How does the Piotroski F-Score define improvement in liquidity?
> Current Ratio in the current fiscal year exceeding the Current Ratio in the preceding fiscal year.

> [!question]- mkt-fa-186 | How does the Piotroski F-Score define improvement in asset efficiency?
> Asset Turnover (Revenue / Total Assets) in the current year exceeding Asset Turnover in the preceding year.

> [!question]- mkt-fa-187 | Why is the Piotroski F-Score particularly effective on small-cap equities?
> Piotroski found the benefits of the score concentrated in small and medium-sized firms, firms with low share turnover and firms with no analyst following, consistent with slower information flow in those firms.

> [!question]- mkt-fa-188 | How does the Beneish M-Score perform on financial institutions and banks?
> It does not apply: Beneish's sample excluded financial firms, and their sales, receivables and working-capital lines do not mean what the indices assume.

> [!question]- mkt-fa-189 | What is the false positive rate of the Beneish M-Score at the -1.78 threshold?
> Beneish reports rates by cut-off; across his cut-offs the model misclassifies 3.5% to 17.5% of non-manipulators while catching 38% to 76% of manipulators, and the paper's abstract summarizes it as identifying about half of manipulators before public discovery.
> No single verified false-positive figure for -1.78 is quoted here.

> [!question]- mkt-fa-190 | How does high Sales Growth Index (SGI) elevate manipulation risk?
> When growth decelerates, growth-oriented managers face intense valuation penalties, driving aggressive revenue recognition to preserve multiples.

> [!question]- mkt-fa-191 | What is the effect of combining low valuation (high BM) with a high F-Score?
> It filters out value traps that are cheap for structural solvency reasons, retaining only underpriced companies with operational tailwinds.

> [!question]- mkt-fa-192 | What is the optimal quantitative workflow combining Beneish, Piotroski, and Altman?
> One reasonable workflow (an analyst's design, not a published result): screen for value, drop firms in Altman's distress zone (Z < 1.81), send firms with M > -1.78 to forensic review, and favour high F-Scores (8 or 9) among the rest.

> [!question]- mkt-fa-261 | An M-Score is -1.458. What is the model probability, and how does it compare with the -1.78 cut-off?
> $\Phi(-1.458) = 7.24\%$, against $\Phi(-1.78) = 3.75\%$ at the cut-off, so the firm is flagged.
> Because the probit was fitted on a sample rich in manipulators, read the number as a ranking, not a population probability.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_fa_06_beneish_piotroski.py`](../../code/mkt_fa_06_beneish_piotroski.py) prints and asserts every number on this page: the eight Beneish indices in exact fractions, the M-Score as an exact sum and as the sum of the rounded terms shown, $\Phi(M)$ by the error function and by numerical integration of the normal density, and the nine Piotroski signals from the raw lines.
- Related notes: [Forensic Accounting, Sloan Accruals, and Earnings Quality](05-Forensic-Accounting-Sloan-Accruals-and-Earnings-Quality.md), [Financial Filings Forensics, 10-K Footnotes, and Governance Red Flags](08-Financial-Filings-Forensics-10K-Footnotes-and-Red-Flags.md).

## Further reading

- Altman, E. I. (1968). *Financial Ratios, Discriminant Analysis and the Prediction of Corporate Bankruptcy*. The Journal of Finance, 23(4), 589-609.
- Beneish, M. D. (1999). *The Detection of Earnings Manipulation*. Financial Analysts Journal, 55(5), 24-36.
- Dechow, P. M., Ge, W., Larson, C. R., & Sloan, R. G. (2011). *Predicting Material Accounting Misstatements*. Contemporary Accounting Research, 28(1), 17-82.
- Piotroski, J. D. (2000). *Value Investing: The Use of Historical Financial Statement Information to Separate Winners from Losers*. Journal of Accounting Research, 38, 1-41.
- The Cornell Daily Sun (29 January 2007). *Business School Students Caught Enron Early*.
