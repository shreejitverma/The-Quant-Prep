---
type: cfa-lm
topic: "Financial Statement Analysis"
topic_code: "03"
topic_slug: "03-Financial-Statement-Analysis"
volume: 3
lm: 6
title: "Integration of Financial Statement Analysis Techniques"
pages: "369-410"
weight_band: "10-15%"
difficulty: 3
los_count: 5
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/financial-statement-analysis]
---

# LM6: Integration of Financial Statement Analysis Techniques

Difficulty 3 of 5: no new accounting standard is introduced, but the exam expects you to run a full DuPont, strip out an equity-method investee, compute both accruals ratios and reconcile operating cash flow to EBIT from a vignette in under 18 minutes, and every one of those steps has a sign or denominator trap.

## LOS map

- **demonstrate** the use of a framework for the analysis of financial statements, given a particular problem, question, or purpose (e.g., valuing equity based on comparables, critiquing a credit rating, obtaining a comprehensive picture of financial leverage, evaluating the perspectives given in management's discussion of financial results) (V3 p.370) ^los-03-06-a
    - Examiner asks: given a purpose stated by a portfolio manager or credit officer, identify which phase of the six-phase framework a described activity belongs to, or pick the analysis (DuPont, accruals, cash flow coverage, segment capital allocation) that answers the stated question.
- **identify** financial reporting choices and biases that affect the quality and comparability of companies' financial statements and explain how such biases may affect financial decisions (V3 p.372) ^los-03-06-b
    - Examiner asks: spot that income from associates is an after-tax number with no matching revenue, that a one-off disposal gain or revaluation is inflating net margin and ROE, or that a change in standard (IFRS 11, IAS 19) breaks comparability across years or against a peer.
- **evaluate** the quality of a company's financial data and recommend appropriate adjustments to improve quality and comparability with similar companies, including adjustments for differences in accounting standards, methods, and assumptions (V3 p.378) ^los-03-06-c
    - Examiner asks: compute a company-only net profit margin, asset turnover and ROE after removing the equity-method investee from profit and from total assets, and state why leverage is left unadjusted.
- **evaluate** how a given change in accounting standards, methods, or assumptions affects financial statements and ratios (V3 p.381) ^los-03-06-d
    - Examiner asks: explain the direction of the change in total assets, liabilities, segment sales or a ratio when proportional consolidation is replaced by the equity method, or when a revised pension standard is applied retrospectively.
- **analyze** and interpret how balance sheet modifications, earnings normalization, and cash flow statement related modifications affect a company's financial statements, financial ratios, and overall financial condition (V3 p.381) ^los-03-06-e
    - Examiner asks: compute the balance-sheet-based and cash-flow-based accruals ratios, adjust operating cash flow for taxes and interest so it is comparable with EBIT, normalize profit for impairments and provisions, and read the trend for earnings quality.

## Core intuition

This module contains no new accounting rule.
It is a rehearsal of how an analyst turns a manager's question into a chain of calculations, and the exam tests whether you can execute that chain on unfamiliar numbers.
The curriculum's own warning is the right starting point: financial analysis is a means to an end, and the analyst should choose the technique that fits the question rather than apply every tool to every situation (V3 p.370).

> [!abstract] Idea 1: the six-phase framework is a loop from purpose to follow-up, and phases 3 and 4 are where the work lives
> Define the purpose and context, collect input data, process the data into analytically useful form, analyze and interpret, develop and communicate conclusions, then follow up by repeating the steps as new information arrives (V3 p.370, p.371).
> The case study spends nearly all its pages on phases 3 and 4, and the analyst treats them jointly because processing the data (adjusting statements, building common-size tables, computing ratios) and interpreting it happen at the same desk (V3 p.373).

The purpose in the case is concrete.
A pension fund portfolio manager wants Nestlé as a long-term core holding and asks three things: what drives earnings growth and is it sustainable, how do earnings relate to cash flow, and does the balance sheet reflect the company's full rights and obligations so that the capital structure can support future plans (V3 p.371).
Phase 1 restates that as identifying the drivers of financial success, assessing their sustainability, and identifying the risks to that sustainability (V3 p.372).
Phase 2 is simply gathering several years of annual reports (V3 p.372).
Everything after that is a sequence of disaggregations, each one prompted by a question the previous step raised.

> [!abstract] Idea 2: seek granularity, because aggregates conceal
> The premise underlying all of the case work is to constantly look beneath the level of information presented, because reducing a figure into smaller components reveals the earnings drivers and exposes weak operations hidden inside stronger aggregates (V3 p.373).

DuPont analysis is the first application of that premise.
ROE is the return the common shareholder actually earns, and it can be split as return on assets times leverage, as net profit margin times asset turnover times leverage, or five ways as EBIT margin times tax burden times interest burden times asset turnover times leverage (V3 p.373).
Each factor points to a different owner of the result: operating managers own the EBIT margin and turnover, the tax department owns the tax burden, the treasurer owns the interest burden and leverage.
The exam expects you to compute all five from an income statement and balance sheet and then to say which factor drove the change.

The case then confronts the first quality problem.
Nestlé's income from associates and joint ventures was CHF8,003 million in 2014, which is 53.7% of profit for the year (V3 p.374).
That number is a pure after-tax net income figure with no matching revenue on the income statement, and most of it came from L'Oréal, of which Nestlé owned 23.4% (V3 p.374).
In 2014 it also contained one-off items: a CHF4,569 million gain on selling L'Oréal shares back to L'Oréal and a CHF2,817 million revaluation gain when Nestlé's original 50% of Galderma was remeasured to fair value on acquiring the other half (V3 p.374).
Two things go wrong if you leave that inside DuPont.
First, the net profit margin combines Nestlé's own sales with someone else's profits, so the margin says 16.27% when the core business earned 7.53% on each franc of sales (V3 p.380).
Second, asset turnover is depressed because the investment in associates sits in total assets but generates no sales, so turnover reads 0.722 instead of 0.787 (V3 p.379).
The returns of associates are not under Nestlé management's control, so mixing them in produces conclusions about the Nestlé-only business that are based on commingled information (V3 p.374).

The fix is mechanical and you must be able to do it from a vignette.
Subtract income from associates from profit for the year to get profit excluding associates, and subtract the investment in associates from total assets to get the assets Nestlé itself employs (V3 p.379).
Recompute margin on the reduced profit and turnover on the average of the reduced asset base.
Do not adjust leverage.
The analyst assumes the same blend of debt and equity finances the investment in associates as finances the Nestlé-only assets, so the leverage ratio stays at the consolidated value (V3 p.382).
Nestlé-only ROE is then margin excluding associates times turnover excluding associates times unadjusted leverage, and the difference from reported ROE is the associates' contribution to ROE (V3 p.382, p.383).
The result reverses the story: reported ROE rose from 17.67% to 21.97% over 2012 to 2014, but Nestlé-only ROE fell from 17.15% to 11.08%, and 10.89 percentage points of the 2014 figure came from associates (V3 p.383).

The next disaggregation is earnings normalization.
Nestlé-only margin fell every year, so the analyst looks for a reason and finds recurring provisions and impairments, including a CHF1,908 million goodwill impairment in 2014 on US ice cream and pizza acquisitions (V3 p.381).
Adding those unusual charges back gives an adjusted margin that is more stable, 10.62% versus 7.53% in 2014, and an adjusted Nestlé-only ROE of 15.63% (V3 p.382, p.383).
But note the analyst's judgment: he computes the adjusted figures to understand the trend and then refuses to exclude the charges from the rest of the analysis, because they involve management decisions, they recur regularly, and they affect returns to shareholders (V3 p.382, p.383).
The exam likes this distinction between an adjustment made for insight and an adjustment made to the base case.

> [!abstract] Idea 3: accrual earnings are a claim, cash flow is the evidence, and capital allocation should be judged on the cash basis management uses
> Every later step in the case asks whether an accrual number is backed by cash: EBIT by cash generated from operations, net income by CFO plus CFI, segment EBIT margins by cash return on segment assets, and reported ROE by the ROE of the assets management actually controls (V3 p.392, p.397, p.399).

Asset composition and capital structure are common-size questions.
Goodwill plus intangibles rose from 32.9% of total assets in 2011 to 40.7% in 2014, which tells you Nestlé grows by acquisition, and the investing section of the cash flow statement confirms that 69.0% of three-year investing outflows went to acquisitions, with Wyeth alone at 74.8% of 2012 investing cash (V3 p.384, p.385).
Leverage of 1.87 to 1.98 looked stable in DuPont, but the long-term capital mix shows equity falling from 74.2% to 71.5% and long-term financial debt rising from 7.8% to 12.3% of long-term capital, so the financing became riskier in a way the single leverage ratio could not show (V3 p.385, p.386).
Working capital then reveals where the liquidity cushion sits: DSO and inventory days fell, payable days rose to 126.5, and the cash conversion cycle went negative at minus 8 days, so Nestlé collects cash from customers eight days before it pays suppliers (V3 p.386).

Segment analysis turns the question to capital allocation.
Nestlé reports segments by management responsibility, not pure geography, and the 2013 change to IFRS 11 was not pushed back before 2012, so only three comparable years exist (V3 p.387, p.388).
The analyst's tool is the ratio of a segment's share of capital expenditure to its share of total assets: above 1 the segment receives a growth allocation, below 1 it is being starved (V3 p.390).
On an EBIT margin view this looks irrational, because the most profitable segment, Nestlé Nutrition at 20.77%, has the lowest ratio at 0.39 while Waters at 9.66% margin gets 1.34 (V3 p.390).
The picture flips on a cash basis: segment cash generation (EBIT plus depreciation and amortisation) over average segment assets shows Nutrition earning only 9.9% while the Americas and Asia, Oceania and Africa earn 27.5% and 26.8%, and those are exactly the segments getting growth allocations (V3 p.392, p.393).
The lesson stated by the curriculum is that if management makes capital budgeting decisions on a cash flow basis, they should be evaluated on a cash flow basis (V3 p.393).
The product group view adds the warning sign: Nutrition and Health Science has the highest asset share at 32.4% and the lowest EBIT return on assets at 8.4% versus 14.1% for the company, and that is where the acquisitions and the goodwill impairment sit (V3 p.395).

Accruals are the module's most testable computation.
Net operating assets are operating assets (total assets less cash and short-term investments) minus operating liabilities (total liabilities less long-term debt and debt in current liabilities) (V3 p.396).
The balance-sheet-based accruals ratio is the change in NOA over average NOA, and the cash-flow-based accruals ratio is net income minus the sum of CFO and CFI, over average NOA (V3 p.397).
Both fell from 2012 to 2014 and neither is large or trending higher, which is what a low-concern reading looks like (V3 p.397).
Then the cash flow relationships: cash generated from operations exceeded operating profit in every year, 1.38 to 1.58 times, which is the direct evidence that operating earnings are backed by cash (V3 p.399).
The practice problems convert this into the exam version: operating cash flow must be put before interest and taxes to be comparable with EBIT, and under IFRS a company that classifies interest paid in financing needs only the tax add-back (V3 p.409).
Coverage ratios close the loop: cash flow to reinvestment 3.89, cash flow to total debt 78.3%, cash flow interest coverage 33.2, and total debt payable in roughly two years from cash flow after reinvestment, all of which say the balance sheet can support more borrowing if an opportunity arises (V3 p.400, p.401).

The final decomposition is valuation.
L'Oréal is traded separately, so the analyst removes its market value from Nestlé's market capitalisation and its CHF934 million earnings contribution from Nestlé's earnings to get an implied Nestlé-only P/E of 15.5 against 16.0 for the whole and 19.9 for the S&P 500, a discount of 22% (V3 p.402, p.403).
That is the sum-of-the-parts logic you meet again in [[LM04-Market-Based-Valuation-Price-and-Enterprise-Value-Multiples]].
The phase 5 report lists support (liquidity, cash flow above earnings, an apparently undervalued core) and concerns (declining core profitability, declining cash return on assets, acquisitions in a low-return group, goodwill write-downs while acquiring), and recommends waiting (V3 p.403, p.404).
Phase 6 shows follow-up in practice: the portfolio manager buys a smaller-than-core position and asks for updates each reporting period focused on the accruals tests, cash flow support of earnings and return on assets (V3 p.404).

## Formulas and derivations

**ROE two-way decomposition** (V3 p.373)
$$
ROE = ROA \times \text{Leverage} = \frac{NI}{\text{Avg total assets}} \times \frac{\text{Avg total assets}}{\text{Avg total equity}}
$$
^f-03-06-1

- $NI$: profit for the year including non-controlling interests when equity includes NCI, as Nestlé's traditional ROE does (V3 p.380).
- Average balances are the mean of beginning and ending year values.
- Reason: total assets cancel, leaving $NI/\text{Avg equity}$.

**ROE three-way (traditional DuPont)** (V3 p.373)
$$
ROE = \underbrace{\frac{NI}{\text{Sales}}}_{\text{Net profit margin}} \times \underbrace{\frac{\text{Sales}}{\text{Avg total assets}}}_{\text{Asset turnover}} \times \underbrace{\frac{\text{Avg total assets}}{\text{Avg total equity}}}_{\text{Leverage}}
$$
^f-03-06-2

- Sales and total assets cancel in sequence, so the product is $NI/\text{Avg equity}$.
- Bickchip practice data gives turnover and assets/equity directly, so only the margin must be computed (V3 p.406).

**ROE five-way decomposition** (V3 p.373)
$$
ROE = \underbrace{\frac{EBIT}{\text{Sales}}}_{\text{EBIT margin}} \times \underbrace{\frac{NI}{EBT}}_{\text{Tax burden}} \times \underbrace{\frac{EBT}{EBIT}}_{\text{Interest burden}} \times \frac{\text{Sales}}{\text{Avg total assets}} \times \frac{\text{Avg total assets}}{\text{Avg total equity}}
$$
^f-03-06-3

- Tax burden is the share of pre-tax profit kept after tax, so a higher value means a lower effective tax rate (V3 p.379).
- Interest burden is the share of EBIT that survives net financial expense, so a value near 1 means little interest cost (V3 p.380).
- The first three factors multiply to the net profit margin; the last two are unchanged from Formula 2.

**Net profit margin excluding associates** (V3 p.379)
$$
NPM_{excl} = \frac{NI - \text{Income from associates and JVs}}{\text{Sales}}
$$
^f-03-06-4

- Income from associates is after tax with no revenue attached, so it is removed from the numerator only (V3 p.374).
- 2014: $(14{,}904 - 8{,}003)/91{,}612 = 6{,}901/91{,}612 = 7.53\%$ (V3 p.379).

**Tax burden and interest burden excluding associates** (V3 p.380)
$$
\text{Tax burden}_{excl} = \frac{NI - \text{Income from associates}}{EBT}, \qquad \text{Interest burden} = \frac{EBT}{EBIT}
$$
^f-03-06-5

- $EBT$ is profit before taxes, associates and joint ventures, so it already excludes associates; only the numerator of the tax burden needs adjusting (V3 p.380).
- Check: $\text{Tax burden}_{excl} \times \text{Interest burden} \times \text{EBIT margin} = NPM_{excl}$, that is $0.6721 \times 0.9416 \times 0.1190 = 0.0753$ (V3 p.380).

**Asset turnover excluding associates** (V3 p.379)
$$
TAT_{excl} = \frac{\text{Sales}}{\left[(TA_{t} - INV_{t}) + (TA_{t-1} - INV_{t-1})\right]/2}
$$
^f-03-06-6

- $INV$: investments in associates and joint ventures on the balance sheet; $TA$: total assets.
- 2014: $91{,}612/[(108{,}127 + 124{,}801)/2] = 91{,}612/116{,}464 = 0.787$ versus $0.722$ unadjusted (V3 p.379).
- Effect of associates on turnover $= TAT - TAT_{excl} = 0.722 - 0.787 = -0.065$ (V3 p.379).

**Associates' effect on net profit margin** (V3 p.380)
$$
\text{Associates' effect} = \frac{NPM}{NPM_{excl}}, \qquad NPM = NPM_{excl} \times \text{Associates' effect}
$$
^f-03-06-7

- A multiplicative factor, so 216.07% means reported margin is 2.16 times the core margin, or 116.07% higher (V3 p.380).
- It is the bridge row in Exhibit 6 that lets the five-way product still reproduce reported ROE.

**Company-only ROE and associates' contribution** (V3 p.382, p.383)
$$
ROE_{only} = NPM_{excl} \times TAT_{excl} \times \text{Leverage}, \qquad \text{Associates' contribution} = ROE - ROE_{only}
$$
^f-03-06-8

- Leverage is left at the consolidated value because the same debt and equity mix is assumed to finance both asset pools (V3 p.382).
- 2014: $0.0753 \times 0.787 \times 1.87 = 11.08\%$; contribution $= 21.97\% - 11.08\% = 10.89\%$ (V3 p.382, p.383).

**Profit adjusted for unusual charges and margin consumed** (V3 p.381, p.382)
$$
\text{Adjusted profit} = (NI - \text{Assoc.}) + \text{Goodwill impairment} + \text{Provisions}, \qquad \text{Margin consumed} = \frac{\text{Adjusted profit}}{\text{Sales}} - NPM_{excl}
$$
^f-03-06-9

- The provisions are added back without tax effect on the assumption they are non-deductible in the year recognised (V3 p.382).
- 2014: $6{,}901 + 1{,}908 + 920 = 9{,}729$; margin $10.62\%$; consumed $10.62\% - 7.53\% = 3.09\%$ (V3 p.382).

**Acquisitions as a share of investing cash flow** (V3 p.385)
$$
\text{Acquisition share} = \frac{\text{Acquisition of businesses}}{\text{Cash flow from investing activities}}
$$
^f-03-06-10

- Both are outflows, so take absolute values; 2012: $10{,}916/14{,}491 = 75.3\%$; Wyeth alone $10{,}846/14{,}491 = 74.8\%$ (V3 p.385).

**Long-term capital structure shares** (V3 p.386)
$$
\text{Share}_i = \frac{\text{Component}_i}{\text{LT financial liabilities} + \text{Other LT liabilities} + \text{Total equity}}
$$
^f-03-06-11

- Current liabilities are excluded; the denominator is long-term capital only.
- 2014: $12{,}396/(28{,}671 + 71{,}884) = 12.3\%$ for long-term financial debt (V3 p.386).

**Defensive interval ratio** (V3 p.386)
$$
DIR = \frac{\text{Cash} + \text{ST investments} + \text{Receivables}}{\text{Daily cash expenditure}}, \quad \text{Daily cash exp.} = \frac{\text{Cash operating expenses} - \text{Non-cash items}}{365}
$$
^f-03-06-12

- Non-cash items removed: depreciation, amortisation, impairments of PP&E, intangibles and goodwill (V3 p.386).
- 2014: $22{,}340/209.5 = 106.6$ days (V3 p.386).

**Cash conversion cycle** (V3 p.386)
$$
CCC = DSO + DOH - \text{Days payables}, \qquad DSO = \frac{\text{Avg receivables}}{\text{Sales}} \times 365, \quad DOH = \frac{\text{Avg inventory}}{COGS} \times 365, \quad \text{Days payables} = \frac{\text{Avg payables}}{\text{Purchases}} \times 365
$$
^f-03-06-13

- Purchases $= COGS + \text{Ending inventory} - \text{Beginning inventory}$; using COGS instead gives 128.6 days rather than the curriculum's 126.5 (V3 p.386).
- 2014: $51.1 + 67.4 - 126.5 = -8.0$ days, negative because suppliers finance the cycle (V3 p.386).

**Capital expenditure share to asset share ratio** (V3 p.390)
$$
\text{Growth allocation ratio}_i = \frac{\text{Capex}_i / \text{Total capex}}{\text{Assets}_i / \text{Total assets}}
$$
^f-03-06-14

- Above 1: the segment receives a growth allocation; below 1: it is receiving less than its asset share and will shrink in relative terms over time (V3 p.390).
- Nutrition 2014: $9.7\%/24.6\% = 0.39$; Europe: $20.0\%/11.4\% = 1.75$ (V3 p.390).

**Segment cash generation and cash return on average assets** (V3 p.391, p.392)
$$
\text{Segment cash generation} = EBIT_{seg} + D\&A_{seg}, \qquad \text{Cash return} = \frac{EBIT_{seg} + D\&A_{seg}}{\text{Avg segment assets}}
$$
^f-03-06-15

- An approximation used because segment cash flow statements are not published (V3 p.391).
- Europe 2014: $(2{,}327 + 473)/11{,}544 = 24.3\%$; Nutrition: $(1{,}997 + 330)/23{,}483 = 9.9\%$ (V3 p.392).

**EBIT return on assets by product group** (V3 p.394)
$$
\text{EBIT ROA} = \frac{EBIT_{group}}{\text{Avg assets}_{group}}
$$
^f-03-06-16

- Product-group assets are reported on an average basis already, unlike segment assets, which are year-end (V3 p.394).
- Nutrition and Health Science 2014: $2{,}723/32{,}245 = 8.4\%$ against the company's $14{,}019/99{,}583 = 14.1\%$ (V3 p.395).

**Net operating assets** (V3 p.396)
$$
NOA = \underbrace{(\text{Total assets} - \text{Cash and ST investments})}_{\text{Operating assets}} - \underbrace{(\text{Total liabilities} - \text{LT debt} - \text{Debt in current liabilities})}_{\text{Operating liabilities}}
$$
^f-03-06-17

- 2014: $(133{,}450 - 8{,}881) - (61{,}566 - 12{,}396 - 8{,}810) = 124{,}569 - 40{,}360 = 84{,}209$ (V3 p.396).

**Balance-sheet-based accruals ratio** (V3 p.397)
$$
\text{BS accruals ratio}_t = \frac{NOA_t - NOA_{t-1}}{(NOA_t + NOA_{t-1})/2}
$$
^f-03-06-18

- Numerator is the balance-sheet-based aggregate accrual; a large or rising value signals earnings built on accruals rather than cash (V3 p.397).
- 2014: $5{,}380/81{,}519 = 6.6\%$ (V3 p.397).

**Cash-flow-based accruals ratio** (V3 p.397)
$$
\text{CF accruals ratio}_t = \frac{NI_t - (CFO_t + CFI_t)}{(NOA_t + NOA_{t-1})/2}
$$
^f-03-06-19

- $CFO$ and $CFI$ carry their statement signs; an investing outflow is negative, so subtracting a negative CFI raises the accrual (V3 p.397).
- 2014: $[14{,}904 - (14{,}700 - 3{,}072)]/81{,}519 = 3{,}276/81{,}519 = 4.0\%$ (V3 p.397).
- Bickchip 2020: $[4{,}038 - (9{,}822 - 10{,}068)]/43{,}192 = 4{,}284/43{,}192 = 9.9\%$ (V3 p.409).

> [!tip] Calculator
> Key the bracket first: `9822 - 10068 =` gives $-246$, then `4038 - 246 +/- =` gives 4,284, then `÷ 43192 =` gives 0.0992.
> Write the bracket sum down before subtracting; the most common slip is subtracting 246 instead of $-246$.
> The distractor 13.4% is $|4{,}038 - 9{,}822|/43{,}192$, which forgets CFI entirely.

**Cash generated from operations to operating profit** (V3 p.399)
$$
\frac{\text{Cash generated from operations}}{\text{Operating profit (EBIT)}}
$$
^f-03-06-20

- Nestlé's cash generated from operations is stated before taxes paid and net treasury flows, so it is already on a pre-interest, pre-tax basis comparable with EBIT (V3 p.398).
- 2014: $17{,}199/10{,}905 = 1.58$; consistently below 1 would make operating profit suspect (V3 p.399).

**Operating cash flow before interest and taxes to operating income** (V3 p.409)
$$
\frac{CFO + \text{Taxes paid} + \text{Interest paid (only if classified in CFO)}}{EBIT}
$$
^f-03-06-21

- Under IFRS a company may classify interest paid in financing; then only the tax add-back is needed (V3 p.409).
- Bickchip 2020: $(9{,}822 + 1{,}930)/6{,}270 = 11{,}752/6{,}270 = 1.87$, closest to 1.9 (V3 p.409).

**Cash return on total assets** (V3 p.400)
$$
\text{Cash return on total assets} = \frac{\text{Cash generated from operations}}{\text{Avg total assets}}
$$
^f-03-06-22

- Total assets reflect the sum of management's past allocations, so this is the cash yield on all investments (V3 p.399).
- 2014: $17{,}199/126{,}946 = 13.5\%$, down from 15.5% in 2012 (V3 p.400).

**Cash flow to reinvestment** (V3 p.400)
$$
\frac{\text{Cash generated from operations}}{\text{Capex} + \text{Expenditure on intangibles}}
$$
^f-03-06-23

- 2014: $17{,}199/(3{,}914 + 509) = 17{,}199/4{,}423 = 3.89$ (V3 p.400).

**Cash flow to total debt and years to pay off debt** (V3 p.400)
$$
\frac{\text{Cash generated from operations}}{\text{Current debt} + \text{Current derivative liabilities} + \text{LT debt}}, \qquad \text{Years} = \frac{\text{Total debt}}{\text{Cash generated from operations} - \text{Reinvestment}}
$$
^f-03-06-24

- The denominator of the years measure is the module's proxy for free cash flow, cash from operations after the capital spending needed to maintain the reinvestment policy (V3 p.400).
- The full FCFE definition (CFO less fixed capital investment plus net borrowing) and its comparison with net income live in [[LM03-Free-Cash-Flow-Valuation]].
- 2014: $17{,}199/21{,}963 = 78.3\%$; years $= 21{,}963/(17{,}199 - 4{,}423) = 1.72$, about two years (V3 p.400).

**Cash flow interest coverage** (V3 p.401)
$$
\text{Cash flow interest coverage} = \frac{\text{Cash generated from operations}}{\text{Cash interest paid}}
$$
^f-03-06-25

- 2014: $17{,}199/518 = 33.2$ times (V3 p.401).

**Implied company-only market value and earnings** (V3 p.401, p.402)
$$
V_{only} = \text{Market cap} - \text{Market value of listed associate}, \qquad E_{only} = NI - \text{Associate's earnings} - NCI
$$
^f-03-06-26

- Market value of the associate $=$ shares held $\times$ price $\times$ FX rate: $129.881 \times 139.30 \times 1.202 = \text{CHF}21{,}747$ million (V3 p.401).
- $V_{only} = 231{,}135 - 21{,}747 = 209{,}388$; $E_{only} = 14{,}904 - 934 - 448 = 13{,}522$ (V3 p.402).

**Decomposed price-to-earnings ratios** (V3 p.403)
$$
P/E_{only} = \frac{V_{only}}{E_{only}}, \qquad \text{Discount to market} = 1 - \frac{P/E_{only}}{P/E_{market}}
$$
^f-03-06-27

- $209{,}388/13{,}522 = 15.5$; $1 - 15.5/19.9 = 22\%$; whole company $231{,}135/14{,}456 = 16.0$, a 20% discount (V3 p.402, p.403).

## Worked examples

### Example 1: Revising the 2011 balance sheet for IAS 19 and IFRS 11 (V3 p.377, p.378)

Setup: the 2012 comparatives were restated for IAS 19 revised and IFRS 11, but the 2011 year-end had not been, so the analyst imposes the 1 January 2012 adjustments on the 31 December 2011 balances (V3 p.377).
IFRS 11 removed proportional consolidation of Cereal Partners Worldwide and Galderma and replaced it with the equity method, so every line of the joint ventures' assets and liabilities comes out and a single investment line goes in (V3 p.378).
Total assets: $114{,}091 - 5 - 646 = 113{,}440$ (Python: `113440`).
Investments in associates rise by 1,688 to 10,317 while total assets fall by 646, because the JV assets removed (786 current plus 511 PP&E, 395 goodwill, 571 intangibles and others) exceed the equity-method investment recognised (V3 p.377).
Total liabilities: $55{,}817 - 73 - 646 = 55{,}098$; the IFRS 11 effect on liabilities equals the effect on assets, as it must for a net-to-one-line reclassification.
IAS 19 lowers employee benefit liabilities by 91, raises deferred tax liabilities by 18 and lowers deferred tax assets by 5, netting to equity up 68: $58{,}274 + 68 = 58{,}342$ (Python: `58342`).
Why it matters: without this revision the 2012 average-asset and average-equity denominators would mix a proportionally consolidated year with an equity-method year and the 2012 DuPont would be non-comparable (V3 p.377). ^ex-03-06-1

### Example 2: Data needed for DuPont, Exhibit 5 (V3 p.379)

Profit excluding associates, 2014: $14{,}904 - 8{,}003 = 6{,}901$; 2013: $10{,}445 - 1{,}264 = 9{,}181$; 2012: $10{,}677 - 1{,}253 = 9{,}424$ (Python: `6901, 9181, 9424`).
Total assets excluding associates, 2014: $133{,}450 - 8{,}649 = 124{,}801$; 2013: $120{,}442 - 12{,}315 = 108{,}127$; 2012: $125{,}877 - 11{,}586 = 114{,}291$; 2011: $113{,}440 - 10{,}317 = 103{,}123$.
Total equity excluding associates, 2014: $71{,}884 - 8{,}649 = 63{,}235$, though this line is not used because leverage is left unadjusted (V3 p.382).
Share of net income from associates, 2014: $8{,}003/14{,}904 = 53.7\%$ (Python: `0.5370`) (V3 p.374). ^ex-03-06-2

### Example 3: Expanded DuPont, 2014 column of Exhibit 6 (V3 p.379, p.380)

Tax burden excluding associates: $6{,}901/10{,}268 = 67.21\%$ (Python: `0.6721`).
Interest burden: $10{,}268/10{,}905 = 94.16\%$ (Python: `0.9416`).
EBIT margin: $10{,}905/91{,}612 = 11.90\%$ (Python: `0.1190`).
Net profit margin excluding associates: $0.6721 \times 0.9416 \times 0.1190 = 7.53\%$, and directly $6{,}901/91{,}612 = 7.53\%$.
Reported net profit margin: $14{,}904/91{,}612 = 16.27\%$; associates' effect $= 16.27\%/7.53\% = 216.07\%$ (Python: `2.1597`).
Asset turnover excluding associates: $91{,}612/[(108{,}127 + 124{,}801)/2] = 91{,}612/116{,}464 = 0.787$ (Python: `0.7866`).
Reported asset turnover: $91{,}612/[(120{,}442 + 133{,}450)/2] = 91{,}612/126{,}946 = 0.722$ (Python: `0.7217`); effect of associates $= -0.065$.
ROA: $16.27\% \times 0.722 = 11.75\%$ (Python: `0.1174`).
Leverage: $126{,}946/[(64{,}139 + 71{,}884)/2] = 126{,}946/68{,}012 = 1.87$ (Python: `1.867`).
ROE: $11.75\% \times 1.87 = 21.97\%$; traditional check $14{,}904/68{,}012 = 21.91\%$, the gap being rounding of the factors (Python: exact product `0.2191`, rounded-factor product `0.2197`) (V3 p.380).
Same method for 2013 gives tax burden 73.82%, interest burden 95.17%, EBIT margin 14.18%, margin excluding associates 9.96%, turnover excluding associates 0.829, reported turnover 0.748, ROA 8.47%, leverage 1.94, ROE 16.44% (Python: `0.7382, 0.9517, 0.1418, 0.0996, 0.8287, 0.7483, 0.0848, 1.943, 0.1647`).
For 2012: 74.30%, 94.73%, 14.92%, 10.50%, 0.825, 0.750, 8.93%, 1.98, 17.67% (Python: `0.7430, 0.9473, 0.1492, 0.1050, 0.8253, 0.7498, 0.0892, 1.978, 0.1765`).
Reading: reported ROE rose across the three years, but the core margin fell from 10.50% to 7.53% and the core turnover slipped from 0.825 to 0.787, so the rise is entirely from associates (V3 p.380, p.381). ^ex-03-06-3

### Example 4: Profitability adjusted for unusual charges, Exhibit 7 (V3 p.381, p.382)

2014: $6{,}901 + 1{,}908 + 920 = 9{,}729$; margin $9{,}729/91{,}612 = 10.62\%$; consumed $10.62\% - 7.53\% = 3.09\%$ (Python: `9729, 0.1062, 0.0309`).
2013: $9{,}181 + 114 + 862 = 10{,}157$; margin $11.02\%$; consumed $1.06\%$ (Python: `10157, 0.1102, 0.0106`).
2012: $9{,}424 + 14 + 618 = 10{,}056$; margin $11.21\%$; consumed $0.71\%$ (Python: `10056, 0.1121, 0.0070`).
Reading: adjusted margins are more stable but still decline each year, so the unusual charges explain the size of the 2014 drop, not the direction of the trend.
The analyst keeps the charges in the base analysis because they recur, reflect management decisions and reduce shareholder returns (V3 p.382). ^ex-03-06-4

### Example 5: ROE with and without associates, Exhibit 8 (V3 p.382, p.383)

Nestlé-only ROE 2014: $7.53\% \times 0.787 \times 1.87 = 11.08\%$ (Python: `0.1108`); contribution of associates $= 21.97\% - 11.08\% = 10.89\%$.
2013: $9.96\% \times 0.829 \times 1.94 = 16.02\%$; contribution $16.44\% - 16.02\% = 0.42\%$ (Python: `0.1602, 0.0042`).
2012: $10.50\% \times 0.825 \times 1.98 = 17.15\%$; contribution $17.67\% - 17.15\% = 0.52\%$ (Python: `0.1715, 0.0052`).
Reading: the associates' contribution jumped from about half a point to 10.89 points in 2014 because of the L'Oréal share exchange and the Galderma revaluation, while the core ROE fell in each of the last two years (V3 p.383). ^ex-03-06-5

### Example 6: Nestlé-only ROE with unusual charges removed, Exhibit 9 (V3 p.383)

2014: $10.62\% \times 0.787 \times 1.87 = 15.63\%$ (Python: `0.1563`).
2013: $11.02\% \times 0.829 \times 1.94 = 17.72\%$; the curriculum shows 17.73%, a rounding difference in the unrounded factors (Python with unrounded inputs: `0.1774`).
2012: $11.21\% \times 0.825 \times 1.98 = 18.31\%$ (Python: `0.1831`).
Reading: the level improves by 4 to 5 points but the slope is still negative, which the analyst calls a genuine concern because the biggest part of the entity should be the main driver of returns (V3 p.383). ^ex-03-06-6

### Example 7: Net profit margin spread, Exhibit 10 (V3 p.383)

2014: $16.27\% - 7.53\% = 8.74\%$; 2013: $11.33\% - 9.96\% = 1.37\%$; 2012: $11.90\% - 10.50\% = 1.40\%$ (Python: `0.0874, 0.0137, 0.0140`).
The widening spread is the with-and-without comparison that shows how much of consolidated profitability depends on associates rather than on Nestlé's own operations (V3 p.383). ^ex-03-06-7

### Example 8: Asset composition, Exhibit 11 (V3 p.384)

2014 shares of total assets 133,450: cash 7,448 gives 5.6%; short-term investments 1,433 gives 1.1%; inventories 9,172 gives 6.9%; receivables 13,459 gives 10.1%; total current 33,961 gives 25.5%; PP&E 28,421 gives 21.3%; goodwill 34,557 gives 25.9%; intangibles 19,800 gives 14.8% (Python: `0.0558, 0.0107, 0.0687, 0.1009, 0.2545, 0.2130, 0.2590, 0.1484`).
Goodwill plus intangibles: 2014 $(34{,}557 + 19{,}800)/133{,}450 = 40.7\%$; 2011 $(28{,}613 + 8{,}785)/113{,}440 = 32.9\%$ (Python: `0.4073, 0.3297`).
Reading: for a food manufacturer the analyst expected inventory and plant to dominate; 40.7% in acquisition intangibles says the strategy is growth by acquisition and shifts the analysis toward the investing cash flows and goodwill impairment risk (V3 p.384). ^ex-03-06-8

### Example 9: Investing activities and acquisition intensity, Exhibit 12 (V3 p.384, p.385)

Acquisition share of investing outflow: 2014 $1{,}986/3{,}072 = 64.6\%$; 2013 $321/1{,}606 = 20.0\%$; 2012 $10{,}916/14{,}491 = 75.3\%$; three-year $13{,}223/19{,}169 = 69.0\%$ (Python: `0.6465, 0.1999, 0.7533, 0.6898`).
Wyeth nutrition acquisition in 2012: $10{,}846/14{,}491 = 74.8\%$ of that year's investing cash (Python: `0.7485`).
Note the 2014 investing outflow is small only because the L'Oréal share sale brought in 3,958 of net divestment proceeds from associates; capex alone was 3,914 (V3 p.385). ^ex-03-06-9

### Example 10: Long-term capital structure, Exhibit 13 (V3 p.385, p.386)

Long-term capital 2014 $= 28{,}671 + 71{,}884 = 100{,}555$.
Long-term financial liabilities $12{,}396/100{,}555 = 12.3\%$; other long-term liabilities $(28{,}671 - 12{,}396)/100{,}555 = 16.2\%$; equity $71{,}884/100{,}555 = 71.5\%$ (Python: `0.1233, 0.1619, 0.7149`).
2011: long-term capital $20{,}243 + 58{,}342 = 78{,}585$; financial debt $6{,}165/78{,}585 = 7.8\%$; other $17.9\%$; equity $74.2\%$ (Python: `0.0785, 0.1791, 0.7424`).
Reading: DuPont leverage moved only between 1.87 and 1.98, yet bond-type debt rose from 7.8% to 12.3% of long-term capital, which is riskier than the employee benefit obligations it partly replaced (V3 p.385, p.386). ^ex-03-06-10

### Example 11: Working capital ratios, Exhibit 14 (V3 p.386)

Current ratio 2014: $33{,}961/32{,}895 = 1.03$ (Python: `1.0324`).
Quick ratio: $(7{,}448 + 1{,}433 + 13{,}459)/32{,}895 = 22{,}340/32{,}895 = 0.68$ (Python: `0.6791`).
Daily cash expenditure: $[47{,}553 + 8{,}217 + 19{,}651 + 1{,}628 - 3{,}058 + 797 - 159 + (3{,}114 - 1{,}908) + 637]/365 = 76{,}472/365 = 209.5$; defensive interval $22{,}340/209.5 = 106.6$ days (Python: `209.51, 106.63`).
The 797 is net other trading expenses $907 - 110$, the 159 is impairment of PP&E and intangibles $136 + 23$, the 3,114 is net other operating expenses $3{,}268 - 154$, and the 637 is net financial expense $772 - 135$ (V3 p.374, p.375).
DSO: $[(13{,}459 + 12{,}206)/2]/91{,}612 \times 365 = 51.1$ days (Python: `51.13`).
DOH: $[(9{,}172 + 8{,}382)/2]/47{,}553 \times 365 = 67.4$ days (Python: `67.37`).
Purchases $= 47{,}553 + 9{,}172 - 8{,}382 = 48{,}343$; days payables $[(17{,}437 + 16{,}072)/2]/48{,}343 \times 365 = 126.5$ days (Python: `126.50`; on COGS it would be 128.6, so the curriculum uses purchases).
Cash conversion cycle $= 51.1 + 67.4 - 126.5 = -8.0$ days (Python: `-8.00`); 2013 check gives $50.0 + 65.7 - 117.8 = -2.1$ (Python: `-2.10`).
Reading: the liquidity cushion is not in the current ratio but in faster cash generation; the negative cycle comes mostly from steadily later payment of vendors (V3 p.386). ^ex-03-06-11

### Example 12: Segment EBIT margins and shares, Exhibits 15 to 17 (V3 p.388 to p.390)

EBIT margins 2014: Nutrition $1{,}997/9{,}614 = 20.77\%$; Other businesses $2{,}654/13{,}884 = 19.12\%$; Americas $5{,}117/27{,}277 = 18.76\%$; Asia, Oceania and Africa $3{,}408/18{,}272 = 18.65\%$; Europe $2{,}327/15{,}175 = 15.33\%$; Waters $714/7{,}390 = 9.66\%$ (Python: `0.2077, 0.1912, 0.1876, 0.1865, 0.1533, 0.0966`).
Asset shares of 99,313: Nutrition $24{,}448/99{,}313 = 24.6\%$; Other $21.5\%$; Americas $21.1\%$; AOA $15.2\%$; Europe $11.4\%$; Waters $6.2\%$ (Python: `0.246, 0.215, 0.211, 0.152, 0.114, 0.062`).
Capex shares of 3,727: Nutrition $363/3{,}727 = 9.7\%$; Other $15.4\%$; Americas $27.9\%$; AOA $18.7\%$; Europe $20.0\%$; Waters $8.3\%$ (Python: `0.097, 0.154, 0.279, 0.187, 0.200, 0.083`).
Concentration: the three geographic segments were $66.3\%$ of 2014 sales versus $70.1\%$ in 2012, and $77.4\%$ of operating profit versus $83.9\%$ (Python: `0.6628, 0.7008, 0.7741, 0.8384`) (V3 p.388).
Nutrition went from 8.8% of sales and 11.2% of operating profit in 2012 to 10.5% and 14.2% in 2014, the Wyeth effect (Python: `0.0876, 0.1121, 0.1049, 0.1424`) (V3 p.387). ^ex-03-06-12

### Example 13: Growth allocation ratios, Exhibit 18 (V3 p.390)

Capex share over asset share, 2014: Nutrition $9.7/24.6 = 0.39$; Other $15.4/21.5 = 0.72$; Americas $27.9/21.1 = 1.32$; AOA $18.7/15.2 = 1.23$; Europe $20.0/11.4 = 1.75$; Waters $8.3/6.2 = 1.34$ (Python from unrounded shares: `0.40, 0.72, 1.32, 1.23, 1.76, 1.32`; the curriculum's 0.39, 1.75 and 1.34 use the rounded percentages).
Reading on an EBIT margin basis: the most profitable segment gets the smallest allocation and the least profitable (Waters) gets a growth allocation, which puzzles the analyst; the absolute capex to Waters is nonetheless the lowest of all segments (V3 p.390, p.391). ^ex-03-06-13

### Example 14: Segment cash return on average assets, Exhibits 19 and 20 (V3 p.391, p.392)

Cash generation $=$ EBIT $+$ D&A, 2014: Europe $2{,}327 + 473 = 2{,}800$; Americas $5{,}117 + 681 = 5{,}798$; AOA $3{,}408 + 510 = 3{,}918$; Waters $714 + 403 = 1{,}117$; Nutrition $1{,}997 + 330 = 2{,}327$; Other $2{,}654 + 525 = 3{,}179$ (Python matches all six).
Average assets 2014, Europe: $(11{,}308 + 11{,}779)/2 = 11{,}544$; Nutrition: $(24{,}448 + 22{,}517)/2 = 23{,}483$; Other: $(21{,}345 + 9{,}564)/2 = 15{,}455$.
Cash return: Europe $2{,}800/11{,}544 = 24.3\%$; Americas $5{,}798/21{,}079 = 27.5\%$; AOA $3{,}918/14{,}630 = 26.8\%$; Waters $1{,}117/6{,}124 = 18.2\%$; Nutrition $2{,}327/23{,}483 = 9.9\%$; Other $3{,}179/15{,}455 = 20.6\%$ (Python: `0.2426, 0.2751, 0.2678, 0.1824, 0.0991, 0.2057`).
Reading: Nutrition has the highest EBIT margin and the lowest cash return on assets because its asset base is inflated by acquisition intangibles; the Americas and AOA have the highest cash returns and receive growth allocations, so on the cash basis management's allocation is rational (V3 p.393). ^ex-03-06-14

### Example 15: Product group EBIT margins and EBIT return on assets, Exhibits 21 and 22 (V3 p.393 to p.395)

EBIT margins 2014: Powdered and Liquid Beverages $4{,}685/20{,}302 = 23.1\%$; Water $710/6{,}875 = 10.3\%$; Milk and Ice Cream $2{,}701/16{,}743 = 16.1\%$; Nutrition and Health Science $2{,}723/13{,}046 = 20.9\%$; Prepared Dishes $1{,}808/13{,}538 = 13.4\%$; Confectionery $1{,}344/9{,}769 = 13.8\%$; Pet Care $2{,}246/11{,}339 = 19.8\%$ (Python: `0.2308, 0.1033, 0.1613, 0.2087, 0.1336, 0.1376, 0.1981`).
EBIT return on average assets 2014: PLB $4{,}685/11{,}599 = 40.4\%$; Water $710/5{,}928 = 12.0\%$; NHS $2{,}723/32{,}245 = 8.4\%$; company $14{,}019/99{,}583 = 14.1\%$ (Python: `0.4039, 0.1198, 0.0844, 0.1408`).
Asset share: NHS $32{,}245/99{,}583 = 32.4\%$, PLB $11.6\%$ (Python: `0.3238, 0.1165`).
Reading: NHS is where the acquisitions went, it is the biggest asset pool, its return on assets is below even Water's and it drags down the company return each year; PLB has the best margin and the best return on the smallest asset base, which raises the question whether capital is going where returns are best (V3 p.395). ^ex-03-06-15

### Example 16: Net operating assets and accruals ratios, Exhibits 23 and 24 (V3 p.396, p.397)

NOA 2014: operating assets $133{,}450 - 8{,}881 = 124{,}569$; operating liabilities $61{,}566 - 12{,}396 - 8{,}810 = 40{,}360$; NOA $= 84{,}209$.
NOA 2013: $120{,}442 - 7{,}053 = 113{,}389$; $56{,}303 - 10{,}363 - 11{,}380 = 34{,}560$; NOA $78{,}829$.
NOA 2012: $116{,}581 - 35{,}797 = 80{,}784$; NOA 2011: $105{,}658 - 32{,}988 = 72{,}670$ (Python: `84209, 78829, 80784, 72670`).
Balance-sheet accruals 2014: $84{,}209 - 78{,}829 = 5{,}380$; average NOA $(84{,}209 + 78{,}829)/2 = 81{,}519$; ratio $5{,}380/81{,}519 = 6.6\%$ (Python: `0.0660`).
2013: $-1{,}955/79{,}807 = -2.4\%$; 2012: $8{,}114/76{,}727 = 10.6\%$ (Python: `-0.0245, 0.1058`).
Cash-flow accruals 2014: $14{,}904 - (14{,}700 + (-3{,}072)) = 14{,}904 - 11{,}628 = 3{,}276$; ratio $3{,}276/81{,}519 = 4.0\%$ (Python: `0.0402`).
2013: $10{,}445 - (14{,}992 - 1{,}606) = -2{,}941$; ratio $-3.7\%$; 2012: $10{,}677 - (15{,}668 - 14{,}491) = 9{,}500$; ratio $12.4\%$ (Python: `-0.0369, 0.1238`).
Reading: levels are small relative to operating assets and neither ratio trends higher; 2012 is elevated because the Wyeth acquisition sat in investing outflows, which is why the cash-flow ratio includes CFI at all (V3 p.397). ^ex-03-06-16

### Example 17: Operating cash flow versus operating profit and total assets, Exhibits 26 and 27 (V3 p.399, p.400)

Cash generated from operations to EBIT: 2014 $17{,}199/10{,}905 = 1.58$; 2013 $18{,}206/13{,}068 = 1.39$; 2012 $18{,}525/13{,}388 = 1.38$ (Python: `1.577, 1.393, 1.384`).
Cash return on average total assets: 2014 $17{,}199/126{,}946 = 13.5\%$; 2013 $18{,}206/123{,}160 = 14.8\%$; 2012 $18{,}525/119{,}659 = 15.5\%$ (Python: `0.1355, 0.1478, 0.1548`).
Reading: earnings are backed by cash in every year, but the cash yield on the asset base is falling, which points back at the goodwill impairment and the low-return NHS acquisitions (V3 p.399, p.400). ^ex-03-06-17

### Example 18: Cash flow coverage of reinvestment, debt and interest, Exhibit 28 (V3 p.400, p.401)

Reinvestment 2014: $3{,}914 + 509 = 4{,}423$; coverage $17{,}199/4{,}423 = 3.89$; 2013 $18{,}206/5{,}330 = 3.42$; 2012 $18{,}525/5{,}598 = 3.31$ (Python: `3.889, 3.416, 3.309`).
Total debt 2014: $8{,}810 + 757 + 12{,}396 = 21{,}963$; cash flow to debt $17{,}199/21{,}963 = 78.3\%$; 2013 $18{,}206/22{,}124 = 82.3\%$; 2012 $18{,}525/27{,}839 = 66.5\%$ (Python: `0.7831, 0.8229, 0.6654`).
Years to repay debt from cash flow after reinvestment: $21{,}963/(17{,}199 - 4{,}423) = 21{,}963/12{,}776 = 1.72$, about two years (Python: `1.719`).
Cash flow interest coverage: $17{,}199/518 = 33.2$; 2013 $18{,}206/505 = 36.1$; 2012 $18{,}525/559 = 33.1$ (Python: `33.20, 36.05, 33.14`).
Reading: reinvestment is covered three to four times and improving, debt could be repaid in two years while maintaining reinvestment, and interest is covered 33 times, so financial capacity exists for more debt if an opportunity appears (V3 p.400, p.401). ^ex-03-06-18

### Example 19: Removing L'Oréal from value and earnings, Exhibits 29 to 31 (V3 p.401 to p.403)

L'Oréal holding in euros: $129.881 \times 139.30 = 18{,}092$ million; in CHF at 1.202: $21{,}747$ million (Python: `18092.4, 21747.1`).
Nestlé market capitalisation: $3{,}168.400 \times 72.95 = 231{,}135$ million; implied Nestlé-only value $231{,}135 - 21{,}747 = 209{,}388$ (Python: `231134.8, 209387.7`).
Pro rata: L'Oréal $21{,}747/231{,}135 = 9.4\%$; Nestlé $90.6\%$ (Python: `0.0941, 0.9059`).
Standalone earnings: $14{,}904 - 934 = 13{,}970$; less NCI 448 gives $13{,}522$ to shareholders (Python: `13970, 13522`).
P/E ratios: whole company $231{,}135/14{,}456 = 16.0$; Nestlé-only $209{,}388/13{,}522 = 15.5$; L'Oréal $21{,}747/934 = 23.3$ (Python: `15.99, 15.48, 23.28`).
Discounts to the S&P 500 multiple of 19.9: $1 - 16.0/19.9 = 20\%$; $1 - 15.5/19.9 = 22\%$ (Python: `0.197, 0.222`).
Earnings split: L'Oréal $934/14{,}456 = 6.5\%$ of earnings but 9.4% of value, so the market pays a higher multiple for L'Oréal than for the core (Python: `0.0646`).
Reading: the analyst reads the deeper discount on the core as the market becoming skeptical about slipping core profitability, and lists it as both an opportunity and a warning in the phase 5 report (V3 p.402, p.404). ^ex-03-06-19

## Item-set patterns

> [!warning] Trap 1: ROE trend read from the reported line while the drivers say the opposite
> The vignette gives three years of net income, sales, turnover and leverage and asks whether ROE is rising and why.
> Correct: compute margin times turnover times leverage for each year, then attribute the change factor by factor; in Bickchip, margin and turnover rose while leverage fell, so ROE rose despite deleveraging (V3 p.409).
> Distractors: "stable" because the changes are small, "leverage drove it" because assets/equity is the biggest number, or reading a rising margin as a rising ROE without checking the other two factors.

> [!warning] Trap 2: equity-method income left inside the margin
> The income statement shows a large "income from associates" line below tax, and the question asks for the company's own net profit margin or ROE.
> Correct: subtract associates' income from profit, subtract the investment in associates from total assets for turnover, leave leverage alone (V3 p.379, p.382).
> Distractors: adjusting the numerator but not the asset base (overstated turnover), adjusting leverage as well (double counting the asset removal), or removing associates from sales, which contain nothing from associates.

> [!warning] Trap 3: sign of CFI in the cash-flow accruals ratio
> Exhibit shows CFO 9,822 and CFI (10,068) in parentheses.
> Correct: $NI - (CFO + CFI) = 4{,}038 - (9{,}822 - 10{,}068) = 4{,}284$; ratio 9.9% (V3 p.409).
> Distractors: 13.4% drops CFI, 23.3% is CFI alone over NOA, and a negative answer comes from adding the investing outflow to CFO with the wrong sign.

> [!warning] Trap 4: comparing raw CFO with EBIT
> The question asks for operating cash flow before interest and taxes to operating income.
> Correct: add back taxes paid always; add back interest paid only if the company classified it in operating (V3 p.409).
> Distractors: raw $9{,}822/6{,}270 = 1.6$ ignores both add-backs; $(9{,}822 + 1{,}930 + 1{,}169)/6{,}270 = 2.1$ adds back interest that was in financing and never reduced CFO.

> [!warning] Trap 5: unusual charges excluded from the base case
> The vignette shows impairments and provisions and asks what the analyst should conclude about profitability.
> Correct: normalize to understand the trend, but treat recurring provisions and impairments as real costs of management decisions and keep them in the assessment (V3 p.382, p.383).
> Distractors: "exclude all non-recurring items" (they recur here), "adjusted margin is stable so profitability is stable" (it still declines), or "impairments are non-cash so they do not matter" (they signal overpayment for acquisitions).

> [!warning] Trap 6: capital allocation judged on EBIT margin alone
> Segment table gives EBIT margins, capex shares and asset shares.
> Correct: compute capex share over asset share to identify growth allocations, then judge against cash return on segment assets (EBIT plus D&A over average assets), not against margin (V3 p.390, p.392).
> Distractors: "the highest-margin segment is starved of capital so allocation is irrational" (its cash return on assets is the lowest), or picking the segment with the largest absolute capex as the growth allocation.

> [!warning] Trap 7: divestiture candidate under a return-on-capital-employed criterion
> Bickchip: segment EBIT margins 11%, 5% and 8% and capital employed and capex by segment.
> Correct: the segment with the lowest margin that also absorbs a large and rising share of capital and capex, Power and Industrial at 5% margin, 31% of capital, capex share rising from 32% to 36% (V3 p.409).
> Distractors: Medical Equipment because it uses the most capital (its margin is higher), or Automation because it is the smallest (it has the best margin).

> [!warning] Trap 8: accounting standard change mistaken for an operating change
> A balance sheet shows total assets falling and investments in associates rising between two years, with a note about IFRS 11.
> Correct: moving from proportional consolidation to the equity method removes the JV's assets, liabilities, sales and expenses and replaces them with one investment line and one income line; segment history before the change is not comparable (V3 p.378, p.388).
> Distractors: "the company sold assets", "leverage improved operationally", or extending a segment trend across the restatement date.

> [!warning] Trap 9: leverage read from the DuPont factor only
> DuPont leverage moves within 1.87 to 1.98 and an option says the capital structure is unchanged.
> Correct: common-size the long-term capital; long-term financial debt rose from 7.8% to 12.3% of long-term capital, so financing risk rose even though the asset-to-equity multiple barely moved (V3 p.385, p.386).
> Distractors: treating employee benefit obligations as equivalent in risk to bonds, or citing a rising current ratio as evidence the balance sheet got safer.

> [!warning] Trap 10: sum-of-the-parts P/E
> The vignette gives the market value and earnings of a listed associate and asks for the implied multiple on the core business.
> Correct: subtract the associate's market value from market cap and its earnings contribution (and NCI) from earnings before dividing (V3 p.402, p.403).
> Distractors: subtracting the book value of the investment instead of its market value, or forgetting to remove the associate's earnings so the core P/E looks even lower.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM06-Integration-of-Financial-Statement-Analysis-Techniques-Practice-Problems]]

## Cross-links

- [[LM01-Intercorporate-Investments]]: the equity method is why income from associates appears as a single after-tax line with no revenue and why the investment sits in non-current assets; the Galderma step acquisition and remeasurement gain are the business-combination mechanics behind the 2014 spike.
- [[LM02-Employee-Compensation-Post-Employment-and-Share-Based]]: the IAS 19 revision that changed benefit obligations is the reason the 2011 balance sheet had to be revised before averaging, and employee benefit liabilities are the "other long-term liabilities" the analyst treats as less onerous than bonds.
- [[LM03-Multinational-Operations]]: translating the L'Oréal holding from EUR to CHF and the translation reserve inside equity come from this module; the CHF/EUR rate of 1.202 is the only FX input in the case.
- [[LM05-Evaluating-Quality-of-Financial-Reports]]: defines the balance-sheet and cash-flow accruals ratios, the CFO-to-operating-income comparison and the warning signs (goodwill impairment, provisions, gains on disposal) that this case applies to Nestlé.
- [[LM03-Free-Cash-Flow-Valuation]]: FCFE and FCFF are the formal versions of the cash flow after reinvestment used here to compute years to repay debt, and the net income to FCFE bridge is the valuation analogue of the accruals test.
- [[LM04-Market-Based-Valuation-Price-and-Enterprise-Value-Multiples]]: the implied Nestlé-only P/E after removing L'Oréal is a sum-of-the-parts application of price multiples and the discount to the S&P 500 multiple is a relative valuation judgment.

## Self-test

> [!question] ST1
> Halden AG reports 2025 profit for the year of 6,200 including income from associates of 1,400, sales of 48,000, EBIT 5,900 and EBT 5,500.
> Total assets were 62,000 at end-2025 and 58,000 at end-2024; investments in associates were 7,000 and 6,000; average total equity was 30,000.
> Halden's company-only ROE (excluding associates, leverage unadjusted) is closest to:
> A. 17.9%.
> B. 20.7%.
> C. 16.0%.

> [!question] ST2
> Using the Halden data in ST1, the associates' effect on net profit margin, expressed as the curriculum's multiplicative factor, is closest to:
> A. 129%.
> B. 77%.
> C. 23%.

> [!question] ST3
> An analyst removes an equity-method investee from a company's DuPont analysis.
> Which statement about the adjustment is most accurate?
> A. Leverage should be recomputed on assets and equity net of the investment.
> B. Sales should be reduced by the investee's revenue share.
> C. Net profit margin and asset turnover are adjusted; leverage is not.

> [!question] ST4
> A company has total assets 90,000, cash and short-term investments 6,000, total liabilities 50,000, long-term debt 15,000 and short-term debt 5,000 at year-end, and NOA of 56,000 at the prior year-end.
> The balance-sheet-based accruals ratio is closest to:
> A. $-3.6\%$.
> B. $-3.7\%$.
> C. $3.6\%$.

> [!question] ST5
> Net income 8,000; CFO 9,500; CFI (12,000); CFF 1,800; average NOA 60,000.
> The cash-flow-based accruals ratio is closest to:
> A. $-2.5\%$.
> B. 17.5%.
> C. 14.5%.

> [!question] ST6
> A US GAAP filer reports CFO 4,200 after paying interest of 300 and taxes of 900; EBIT is 3,000.
> Operating cash flow before interest and taxes to operating income is closest to:
> A. 1.40.
> B. 1.70.
> C. 1.80.

> [!question] ST7
> Segment data: Segment X has 30% of total assets, 45% of capex and an EBIT margin of 12%; Segment Y has 25% of total assets, 10% of capex and an EBIT margin of 20%; Segment Y's cash return on average assets is 8% versus 24% for X.
> The most appropriate conclusion is that management's capital allocation is:
> A. irrational, because the highest-margin segment receives the lowest growth allocation.
> B. rational, because growth allocations follow cash return on assets rather than EBIT margin.
> C. indeterminate until segment cash flow statements are disclosed.

> [!question] ST8
> A company's core net profit margin fell from 10.5% to 7.5% over three years while a normalized margin adding back goodwill impairments and provisions fell from 11.2% to 10.6%.
> The analyst should most likely conclude that:
> A. profitability is stable once non-recurring charges are removed.
> B. the charges explain the size of the decline but not its direction, and they should stay in the assessment if they recur.
> C. the charges are non-cash and therefore irrelevant to earnings quality.

> [!question] ST9
> A company adopts a standard that replaces proportional consolidation of a 50% joint venture with the equity method.
> Relative to the prior treatment, which is most likely?
> A. Total assets fall, consolidated sales fall, net income is unchanged.
> B. Total assets rise, consolidated sales fall, net income falls.
> C. Total assets fall, consolidated sales are unchanged, net income falls.

> [!question] ST10
> Parent market capitalisation is 120,000 with earnings to shareholders of 8,000, including 600 from a 20% listed associate whose holding has a market value of 15,000.
> Non-controlling interests take 200 of earnings (already excluded from the 8,000).
> The implied parent-only P/E is closest to:
> A. 15.0.
> B. 14.2.
> C. 13.1.

> [!success]- Answer key
> ST1: A. Profit excluding associates $6{,}200 - 1{,}400 = 4{,}800$; margin $4{,}800/48{,}000 = 10.0\%$; assets excluding associates $62{,}000 - 7{,}000 = 55{,}000$ and $58{,}000 - 6{,}000 = 52{,}000$, average $53{,}500$; turnover $48{,}000/53{,}500 = 0.897$; leverage on unadjusted averages $60{,}000/30{,}000 = 2.0$; ROE $= 0.10 \times 0.897 \times 2.0 = 17.9\%$ (Python: `0.1794`).
> B is reported ROE $6{,}200/30{,}000 = 20.7\%$ with associates left in (Python: `0.2067`).
> C combines the adjusted margin with the reported turnover $48{,}000/60{,}000 = 0.80$, giving $0.10 \times 0.80 \times 2.0 = 16.0\%$, the numerator-only adjustment (V3 p.379, p.382).
> ST2: A. Reported margin $6{,}200/48{,}000 = 12.92\%$; core margin $10.0\%$; factor $12.92/10.0 = 129\%$ (Python: `1.2917`). B is the inverse $10/12.92 = 77\%$; C is the associates' share of profit $1{,}400/6{,}200 = 23\%$, a different measure (V3 p.380).
> ST3: C. The curriculum adjusts margin and turnover and assumes the same capital mix finances both asset pools, so leverage is unchanged (V3 p.382). A double counts; B is wrong because equity-method investees contribute no sales.
> ST4: A. Operating assets $90{,}000 - 6{,}000 = 84{,}000$; operating liabilities $50{,}000 - 15{,}000 - 5{,}000 = 30{,}000$; NOA $= 54{,}000$; change $54{,}000 - 56{,}000 = -2{,}000$; average $(54{,}000 + 56{,}000)/2 = 55{,}000$; ratio $-2{,}000/55{,}000 = -3.6\%$ (Python: `-0.0364`).
> B divides by ending NOA, $-2{,}000/54{,}000 = -3.7\%$ (Python: `-0.0370`).
> C drops the sign; a negative ratio means NOA shrank, which is the low-accrual direction (V3 p.397).
> ST5: B. $[8{,}000 - (9{,}500 - 12{,}000)]/60{,}000 = [8{,}000 + 2{,}500]/60{,}000 = 10{,}500/60{,}000 = 17.5\%$ (Python: `0.175`).
> A is $(8{,}000 - 9{,}500)/60{,}000 = -2.5\%$, dropping CFI entirely.
> C is $[8{,}000 - (9{,}500 - 12{,}000 + 1{,}800)]/60{,}000 = 8{,}700/60{,}000 = 14.5\%$, which wrongly nets financing cash flow into the accrual (Python: `0.145`) (V3 p.397).
> ST6: C. US GAAP puts interest paid in operating, so both are added back: $(4{,}200 + 300 + 900)/3{,}000 = 5{,}400/3{,}000 = 1.80$ (Python: `1.8`). A is raw CFO over EBIT; B adds back taxes only, which is the IFRS-with-interest-in-financing case (V3 p.409).
> ST7: B. Growth allocation ratios: X $45/30 = 1.5$, Y $10/25 = 0.4$ (Python: `1.5, 0.4`); X earns 24% cash on assets versus 8% for Y, so capital follows cash returns, exactly the Nestlé pattern where Nutrition had the highest margin and lowest cash return (V3 p.393). A judges on margin alone; C ignores that the EBIT plus D&A proxy is the curriculum's accepted substitute.
> ST8: B. Normalized margin still falls (11.2% to 10.6%), so the trend is intact; the curriculum keeps recurring provisions and impairments in the base analysis because they are management decisions affecting shareholder returns (V3 p.382, p.383). A misreads a smaller decline as stability; C ignores that impairments signal overpaid acquisitions.
> ST9: A. Equity method removes the JV's assets, liabilities, sales and expenses line by line and records one investment and one share-of-profit line, so assets and sales fall while net income is unchanged (Nestlé 2011: total assets down 646, associates up 1,688) (V3 p.378). B and C get the sales or income effect wrong.
> ST10: B. Parent-only value $120{,}000 - 15{,}000 = 105{,}000$; parent-only earnings $8{,}000 - 600 = 7{,}400$; P/E $105{,}000/7{,}400 = 14.19$ (Python: `14.19`). A is $120{,}000/8{,}000$ with nothing removed; C is $105{,}000/8{,}000 = 13.1$, removing value but not earnings, the trap in Exhibit 31 (V3 p.402, p.403).

## Flashcards

#flashcards/cfa-l2/03-Financial-Statement-Analysis/lm06

Six phases of the financial statement analysis framework::Define purpose and context; collect input data; process data into analytically useful form; analyze and interpret; develop and communicate conclusions; follow up (V3 p.370, p.371).
Which phases of the framework does the Nestlé case treat jointly and why?::Phases 3 and 4, because processing the data and interpreting it are best done together (V3 p.373).
Primary reason for performing financial analysis::To help make an economic decision (V3 p.370).
The premise of "seeking granularity"::Constantly look beneath the presented level of information; disaggregation reveals earnings drivers and weak operations hidden in aggregates (V3 p.373).
ROE two-way decomposition::ROA times leverage (V3 p.373).
ROE three-way decomposition::Net profit margin times asset turnover times leverage (V3 p.373).
ROE five-way decomposition::EBIT margin times tax burden times interest burden times asset turnover times leverage (V3 p.373).
Tax burden::Net income divided by EBT; the share of pre-tax profit kept after tax (V3 p.380).
Interest burden::EBT divided by EBIT; the share of operating profit left after net financial expense (V3 p.380).
Why remove income from associates before DuPont?::It is an after-tax figure with no matching revenue and not under management's control, so it commingles core margins and turnover with outside returns (V3 p.374).
Company-only net profit margin::(Net income minus income from associates) divided by sales (V3 p.379).
Company-only asset turnover::Sales divided by average of (total assets minus investment in associates) (V3 p.379).
Which DuPont factor is not adjusted for associates and why?::Leverage, because the same debt and equity mix is assumed to finance the associates' assets and the core assets (V3 p.382).
Company-only ROE formula::Margin excluding associates times turnover excluding associates times unadjusted leverage (V3 p.382).
Associates' contribution to ROE::Reported ROE minus company-only ROE (V3 p.383).
Micro-problem: profit 14,904, associates 8,003, sales 91,612; core margin?::6,901 / 91,612 = 7.53% (V3 p.379).
Micro-problem: reported margin 16.27%, core margin 7.53%; associates' effect factor?::16.27 / 7.53 = 216.07%, meaning reported margin is 116.07% higher than core (V3 p.380).
Micro-problem: core margin 7.53%, core turnover 0.787, leverage 1.87; core ROE?::0.0753 x 0.787 x 1.87 = 11.08%; keystrokes .0753 × .787 × 1.87 = (V3 p.382).
Micro-problem: reported ROE 21.97%, core ROE 11.08%; associates' contribution?::10.89 percentage points (V3 p.383).
What made 2014 income from associates unusual for Nestlé?::A 4,569 gain on selling L'Oréal shares back to L'Oréal and a 2,817 revaluation gain on the 50% of Galderma already owned (V3 p.374).
Adjusted profit for unusual charges::Profit excluding associates plus goodwill impairment plus provisions, provisions not tax-affected (V3 p.381, p.382).
Why did the analyst keep unusual charges in the base DuPont analysis?::They involve management decisions, recur regularly and affect shareholder returns (V3 p.382).
Micro-problem: core profit 6,901, goodwill impairment 1,908, provisions 920, sales 91,612; adjusted margin and margin consumed?::9,729 / 91,612 = 10.62%; consumed 10.62% minus 7.53% = 3.09% (V3 p.382).
What did goodwill plus intangibles at 40.7% of assets tell the analyst?::Nestlé follows a growth-by-acquisition strategy, so acquisitions and impairment risk need study (V3 p.384).
Shortcoming of the DuPont leverage ratio for capital structure analysis::It says nothing about the nature or riskiness of the financing instruments; bond debt is more onerous than employee benefit obligations (V3 p.385).
Long-term capital structure denominator::Long-term financial liabilities plus other long-term liabilities plus total equity (V3 p.386).
Defensive interval ratio::(Cash plus short-term investments plus receivables) divided by daily cash expenditure, where daily cash expenditure excludes depreciation, amortisation and impairments (V3 p.386).
Cash conversion cycle::DSO plus days of inventory on hand minus days payables (V3 p.386).
Denominator for days payables in the Nestlé case::Purchases, which equal COGS plus ending inventory minus beginning inventory (V3 p.386).
Meaning of a negative cash conversion cycle::Cash is collected from customers before suppliers are paid; Nestlé's minus 8 days came mainly from paying vendors later (V3 p.386).
Growth allocation ratio::Segment share of capex divided by segment share of total assets; above 1 is a growth allocation, below 1 the segment shrinks in relative terms (V3 p.390).
Micro-problem: segment capex share 9.7%, asset share 24.6%; ratio and reading?::0.39, the segment is being allocated far less than its asset share (V3 p.390).
Segment cash generation proxy::Segment EBIT plus segment depreciation and amortisation, because segment cash flow statements are not published (V3 p.391).
Segment cash return on assets::(EBIT plus D&A) divided by average segment assets (V3 p.392).
Why did the low capex allocation to Nestlé Nutrition make sense on a cash basis?::Nutrition had the highest EBIT margin but the lowest cash return on assets, 9.9%, because its asset base is inflated by acquisition intangibles (V3 p.393).
Principle for evaluating capital allocation stated in the case::If management makes capital budgeting decisions on a cash flow basis, evaluate them on a cash flow basis (V3 p.393).
Why are product-group assets not comparable with segment assets in the Nestlé report?::Product-group assets are reported on an average basis and segment assets at year-end, and segments carry unallocated assets (V3 p.394).
Net operating assets::(Total assets minus cash and short-term investments) minus (total liabilities minus long-term debt minus debt in current liabilities) (V3 p.396).
Balance-sheet-based accruals ratio::(NOA end minus NOA beginning) divided by average NOA (V3 p.397).
Cash-flow-based accruals ratio::[Net income minus (CFO plus CFI)] divided by average NOA (V3 p.397).
Micro-problem: NI 4,038, CFO 9,822, CFI (10,068), average NOA 43,192; cash-flow accruals ratio?::[4,038 minus (9,822 minus 10,068)] / 43,192 = 4,284 / 43,192 = 9.9% (V3 p.409).
Trap: cash-flow accruals ratio of 13.4% in the Bickchip problem::Comes from (NI minus CFO) / NOA, which drops the investing cash flow (V3 p.409).
What accruals pattern would have worried the analyst most?::High absolute accruals ratios that are consistently trending higher (V3 p.397).
Cash generated from operations to operating profit, purpose::Tests whether accrual operating profit is backed by cash; consistently below 1 makes operating profit suspect (V3 p.399).
Operating cash flow before interest and taxes::CFO plus taxes paid plus interest paid, the latter only if interest was classified in operating (V3 p.409).
Micro-problem: CFO 9,822, taxes paid 1,930, interest paid 1,169 in financing, EBIT 6,270; OCF before interest and taxes to EBIT?::(9,822 + 1,930) / 6,270 = 1.87; do not add back interest (V3 p.409).
Cash flow to reinvestment::Cash generated from operations divided by (capex plus expenditure on intangibles) (V3 p.400).
Total debt in the Nestlé cash flow to debt ratio::Current financial debt plus current derivative liabilities plus long-term financial debt (V3 p.400).
Micro-problem: total debt 21,963, cash from operations 17,199, reinvestment 4,423; years to repay?::21,963 / (17,199 minus 4,423) = 1.72, about two years (V3 p.400).
Implied company-only market value::Market capitalisation minus market value of the listed associate holding (V3 p.402).
Company-only earnings to shareholders::Consolidated earnings minus the associate's earnings contribution minus non-controlling interests (V3 p.402).
Micro-problem: implied value 209,388, standalone earnings 13,522, market P/E 19.9; company-only P/E and discount?::15.5 and 1 minus 15.5 / 19.9 = 22% (V3 p.403).
Effect of replacing proportional consolidation with the equity method (IFRS 11)::JV assets, liabilities, sales and expenses removed line by line and replaced by one investment line and one share-of-profit line; net income unchanged (V3 p.378).
Why was 2011 segment data non-comparable with 2012 onward?::The IFRS 11 change was not carried back into segment information before 2012 (V3 p.388).
Phase 6 follow-up instruction in the Nestlé case::Update the report each reporting period, emphasizing the accruals tests and cash flow support of earnings, with particular regard to return on assets (V3 p.404).
Trap: reading a stable DuPont leverage ratio as an unchanged capital structure::Common-size the long-term capital; Nestlé's long-term financial debt rose from 7.8% to 12.3% of long-term capital while leverage stayed near 1.9 (V3 p.386).
The 2014 rise in Nestlé's reported ROE came from {{gains on the L'Oréal share exchange and the Galderma revaluation inside income from associates}}, not from core operations (V3 p.383).
The cash-flow-based accruals ratio subtracts {{CFO plus CFI}} from net income before dividing by average NOA (V3 p.397).
Segments with a growth allocation ratio above 1 are receiving {{a larger share of capex than their share of assets}} (V3 p.390).

## Common mistakes

1. Removing income from associates from profit but leaving the investment in associates in total assets, which overstates the core asset base and understates core turnover (V3 p.379).
2. Adjusting leverage for associates as well as margin and turnover; the curriculum assumes the same capital mix finances both asset pools and leaves leverage unadjusted (V3 p.382).
3. Reading a rising reported ROE as improving performance without decomposing it; Nestlé's core ROE fell in every year while reported ROE rose (V3 p.383).
4. Dropping the investing cash flow from the cash-flow-based accruals ratio, or adding a negative CFI with the wrong sign; the ratio is net income minus (CFO plus CFI) over average NOA (V3 p.397, p.409).
5. Dividing accruals by ending NOA instead of average NOA (V3 p.397).
6. Comparing raw CFO with EBIT; add back taxes paid, and add back interest paid only when the company classifies it in operating activities (V3 p.409).
7. Excluding recurring provisions and impairments from the base analysis as if they were non-recurring; the analyst normalizes for insight but keeps them because they recur and reflect management decisions (V3 p.382).
8. Judging capital allocation on EBIT margin alone; the curriculum evaluates it on cash return on segment assets, which reversed the conclusion about Nestlé Nutrition (V3 p.393).
9. Computing days payables on COGS instead of purchases, which gives 128.6 days rather than 126.5 (V3 p.386).
10. Treating DuPont leverage of 1.87 to 1.98 as an unchanged capital structure while long-term financial debt rose from 7.8% to 12.3% of long-term capital (V3 p.386).
11. Extending a segment trend across the IFRS 11 restatement date, when pre-2012 segment data included proportionally consolidated JV amounts (V3 p.388).
12. Removing the associate's market value from market capitalisation but not its earnings (or the NCI share) when computing a company-only P/E (V3 p.402, p.403).
13. Averaging a restated year with an unrestated prior year in DuPont denominators; the analyst revised the 2011 balance sheet first (V3 p.377).
14. Assuming a rising current ratio is the liquidity cushion when the real cushion is faster cash generation and a negative cash conversion cycle (V3 p.386).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "03-06" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
