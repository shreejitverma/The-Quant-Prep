---
type: cfa-lm
topic: "Financial Statement Analysis"
topic_code: "03"
topic_slug: "03-Financial-Statement-Analysis"
volume: 3
lm: 5
title: "Evaluating Quality of Financial Reports"
pages: "285-367"
weight_band: "10-15%"
difficulty: 3
los_count: 13
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/financial-statement-analysis]
---

# LM5: Evaluating Quality of Financial Reports

Difficulty 3 of 5: the arithmetic is light (Beneish products, a Z-score, DSO, an after-tax adjustment) but the module is long, case-heavy, and tested through direction-of-effect questions where the distractor is the opposite sign of a warning sign, the wrong quality attribute (completeness versus unbiased measurement), or a ratio that moves the "good" way for a bad reason.

## LOS map

- **demonstrate** the use of a conceptual framework for assessing the quality of a company's financial reports (V3 p.287) ^los-03-05-a
    - Examiner asks: given a set of analyst conclusions about a company, place its reports on the quality spectrum (GAAP and decision-useful, GAAP but biased, GAAP with earnings management, non-compliant, fictitious) and state which of the two framework questions fails.
- **explain** potential problems that affect the quality of financial reports (V3 p.289) ^los-03-05-b
    - Examiner asks: for a given choice (premature revenue, understated bad debt, capitalized operating cost, reclassified receivable, understated intangibles in an acquisition) state the direction of the effect on income, assets, liabilities, equity, and the affected ratios.
- **describe** how to evaluate the quality of a company's financial reports (V3 p.302) ^los-03-05-c
    - Examiner asks: identify which of the seven general steps a described action belongs to, or which warning sign in Exhibit 4 a research note matches.
- **evaluate** the quality of a company's financial reports (V3 p.303) ^los-03-05-d
    - Examiner asks: compute or compare Beneish M-scores against the $-1.78$ cutoff, interpret an index above one, and state the two limitations of quantitative models (association not causation, declining predictive power).
- **describe** indicators of earnings quality (V3 p.307) ^los-03-05-e
    - Examiner asks: pick the indicator (recurring earnings, persistence and accruals, beating benchmarks, enforcement actions and restatements) and explain why exactly meeting consensus or a high accruals share is a quality flag.
- **describe** the concept of sustainable (persistent) earnings (V3 p.311) ^los-03-05-f
    - Examiner asks: read $\beta_1$ in $E_{t+1} = \alpha + \beta_1 E_t + \varepsilon$ as persistence, and compare $\beta_1$ on cash flow with $\beta_2$ on accruals.
- **explain** mean reversion in earnings and how the accruals component of earnings affects the speed of mean reversion (V3 p.315) ^los-03-05-g
    - Examiner asks: two firms with the same high ROE, one with a larger accruals component; which reverts faster and why an analyst must not extrapolate extreme earnings.
- **evaluate** the earnings quality of a company (V3 p.317) ^los-03-05-h
    - Examiner asks: from a receivables and revenue table compute DSO, receivables to revenue, and growth rates, then say whether receivables growth outpacing revenue growth signals channel stuffing or bill-and-hold; or detect capitalization from a common-size PP&E buildup.
- **evaluate** the cash flow quality of a company (V3 p.330) ^los-03-05-i
    - Examiner asks: from research notes on OCF sign, sustainability, adequacy to cover capex, dividends, and debt repayment, and volatility, pick the high-quality company; or unwind a classification shift and restate OCF growth.
- **describe** indicators of balance sheet quality (V3 p.340) ^los-03-05-j
    - Examiner asks: match a fact (off-balance-sheet purchase obligations, obsolete inventory not written down, aggregated line items) to completeness, unbiased measurement, or clear presentation.
- **evaluate** the balance sheet quality of a company (V3 p.340) ^los-03-05-k
    - Examiner asks: compare goodwill with market capitalization to infer a likely write-off, or recompute return on sales after grossing up an equity-method investee's sales.
- **describe** indicators of cash flow quality (V3 p.330) ^los-03-05-l
    - Examiner asks: list the four characteristics of high-quality OCF for an established company and identify the working-capital pattern (payables up, receivables and inventory down) that flags managed OCF.
- **describe** sources of information about risk (V3 p.343) ^los-03-05-m
    - Examiner asks: which source is least timely (the audit opinion), which is a warning sign (auditor change, NT filing, CFO resignation), and what the five IFRS management commentary elements and the MD&A items cover.

## Core intuition

This module teaches you to be the analyst who is short Enron in November 2000 rather than the one reading about it in December 2001 (V3 p.286).
Every technique in it follows from one accounting identity and two questions.
The identity is $A - L = E$: any choice that inflates income inflates equity and therefore must inflate an asset or deflate a liability somewhere on the balance sheet (V3 p.290).
The two questions are: are the reports GAAP-compliant and decision-useful, and are the results (earnings, cash flow, balance sheet) of high quality, meaning adequate and sustainable (V3 p.288)?

> [!abstract] Idea 1: reporting quality and results quality are different attributes, and the first is a precondition for judging the second
> Reporting quality is about the information: is it relevant and does it faithfully represent economic reality?
> Results (earnings) quality is about the economics: do the earnings cover the cost of capital and will they recur?
> Low reporting quality makes results quality unassessable; high reporting quality is necessary but not sufficient for high results quality (V3 p.286, p.287).

The curriculum insists on keeping the two apart because they fail in different ways.
A company whose only profit is a one-off lawsuit settlement can have perfect reporting quality and terrible earnings quality (V3 p.287).
The converse is the dangerous case: poor economics motivate management to misreport, so low results quality is itself a reason to scrutinise reporting quality (V3 p.287).
The quality spectrum in Exhibit 2 stacks the combinations from best to worst: GAAP, decision-useful, sustainable, and adequate returns at the top; GAAP and decision-useful but low earnings quality; within GAAP but biased choices; within GAAP but earnings management (real or accounting); non-compliant accounting; and fictitious transactions at the bottom (V3 p.288, p.289).
Decision-useful means relevant and faithfully representative, where faithful representation is complete, neutral, and free from error, exactly the IASB Conceptual Framework characteristics (V3 p.288).

Bias has a direction.
Aggressive choices raise current-period reported performance and position and tend to lower later periods; conservative choices do the reverse (V3 p.289).
Earnings management is a third flavour: smoothing, which understates earnings in good periods and overstates them in bad ones so that reported volatility is lower than economic volatility (V3 p.289).
Bias also lives in presentation: a company can disclose transparently or in a way that buries the unfavourable and highlights the favourable (V3 p.289).
Below the GAAP line the reports simply cannot be relied on (V3 p.289).

> [!abstract] Idea 2: every quality problem is a choice about amount, timing, or classification, and the accounting equation tells you where it must show up
> Amount and timing choices touch several statements at once because income flows into equity and equity must balance against net assets (V3 p.290).
> Classification choices usually touch one statement, but they can flatter the ratios analysts watch most: receivables measures, the current ratio, operating margin, and operating cash flow (V3 p.292, p.294).

Work through the effects like a bookkeeper.
Premature or fictitious revenue overstates income, equity, and receivables (V3 p.290).
Delayed expense recognition overstates income and equity and either overstates an asset (understated bad debt inflates receivables, understated depreciation inflates PP&E) or understates a liability (understated interest or tax accruals) (V3 p.290).
Understated contingent liabilities and overstated fair values of financial assets both leak into equity through income or OCI (V3 p.290).
Operating cash flow can be pumped by delaying payables, accelerating collections, deferring inventory purchases, and postponing maintenance or research (V3 p.290).
Classification shifts move inventory to other assets (Merck, which cut days of inventory and the current ratio), receivables to long-term receivables, non-operating gains into operating income, ordinary expenses into "non-recurring" special items, gains through net income and losses through OCI, and asset sales or capitalized operating costs into the investing section so that OCF looks stronger (V3 p.292, p.293, p.294).

Motivation matters as much as mechanism.
The Level I fraud triangle (pressure, opportunity, rationalization) is not restated in this module, but every piece of it appears with a page.
Pressure: compensation largely tied to financial results (V3 p.296), the wish to inflate a share price before a stock-financed acquisition or to secure a better price as a target (V3 p.297), and the market reward for meeting or narrowly beating consensus (V3 p.316).
Opportunity: fair value measurement without quoted prices, goodwill that is never amortized, reserves and allowances that can be raised or released, multiple-element contracts, and an auditor that does not verify (V3 p.291, p.298, p.301, p.322, p.326).
Rationalization: describing a goodwill impairment as "non-recurring and non-cash" so investors overlook a bad acquisition (V3 p.298).
Acquisitions deserve a paragraph of their own: they add the target's OCF to the acquirer's with no "with and without" disclosure, they tempt the acquirer to understate amortizable intangibles so more of the price sits in non-amortized goodwill, and misreporting firms are more likely to acquire because consolidation muddies comparability (V3 p.297, p.298).

Even GAAP-compliant statements can diverge from economic reality.
A special purpose entity can be kept off the balance sheet on a voting-control argument when the economics say consolidate; the variable interest entity concept exists because of Digilog and Enron (V3 p.298, p.299).
A single-period impairment or restructuring charge is conservative in the current period but usually means earlier periods were overstated, so the analyst spreads recurring-type charges across past periods and excludes truly one-off items (V3 p.300, p.301).
R&D is expensed even though it creates assets, order backlog is an unrecognized asset, and items such as available-for-sale gains, revaluation surpluses, translation adjustments, pension remeasurements, and cash flow hedge results sit in OCI where the analyst must decide whether to treat them as income (V3 p.301).

> [!abstract] Idea 3: earnings equal cash flow plus accruals, the cash part persists more, so the size and abnormality of accruals is the master indicator of earnings quality and of how fast mean reversion will bite
> Persistence is $\beta_1$ in $E_{t+1} = \alpha + \beta_1 E_t + \varepsilon$; decomposed, the coefficient on cash flow exceeds the coefficient on accruals (Sloan 1996) (V3 p.311).
> Extreme earnings revert to the mean through competition and management change; a large or abnormal accruals component accelerates the reversion (V3 p.315, p.316).

The evaluation procedure has seven steps: understand the business and industry, learn about management incentives and insider sales, identify the judgment-heavy accounting areas, compare with prior year and with peers (policies and ratios), check warning signs, look for segment shifting in multi-segment firms, and apply quantitative tools (V3 p.302, p.303).
The quantitative tool is the Beneish model, a probit whose eight indices each capture a plausible motive or mechanism: receivables outrunning sales (DSR), margin deterioration (GMI), a rising share of soft assets (AQI), sales growth pressure (SGI), a falling depreciation rate (DEPI), SG&A inefficiency (SGAI), high accruals, and rising leverage (LEVI) (V3 p.304, p.305).
The M-score is standard normal, so its probability is $N(M)$; $-1.78$ maps to 3.8% and is the cutoff Beneish considered relevant for investors, and $-1.49$ maps to 6.8% (V3 p.305).
The cutoff trades off Type I errors (calling a manipulator clean) against Type II errors (calling a clean firm a manipulator) (V3 p.305).
Two limitations are examinable: accounting-based models find associations, not cause and effect, and the model's predictive power has declined because managers test their tactics against it (V3 p.307).

Earnings quality indicators are recurring earnings, persistence and accruals, beating benchmarks, and external confirmations (V3 p.307).
Recurring earnings exclude discontinued operations and one-off gains; Enron's smooth 24% and 26% increases in pre-interest income were manufactured from non-merchant asset gains, a gain on a subsidiary's stock issuance, equity-affiliate earnings, and other income, which were 52% of the 1999 total (V3 p.308, p.309).
Classification shifting does not change net income but inflates "core" earnings by pushing normal expenses into special items, and non-GAAP measures need a reconciliation and a sceptical read (Groupon's SEC-rejected metric excluded online marketing costs) (V3 p.309, p.310).
Accruals can be screened by modelling normal accruals on economic drivers (credit sales growth, depreciable assets) and treating the regression residual as abnormal or discretionary accruals, or simply by scaling total accruals by average assets (V3 p.311, p.312).
Positive net income with negative operating cash flow is the loudest signal (Allou, Enron quarterly) (V3 p.312, p.314), but the WorldCom exhibit shows the converse trap: OCF exceeding net income is not proof of quality when the fraud is capitalization, because capitalized costs are investing outflows (V3 p.314, p.315).
Exactly meeting or narrowly beating consensus clusters suspiciously in the data; enforcement actions and restatements are confirmations that arrive too late to be useful (V3 p.316, p.317).

The three cases are the module's exam bank.
Sunbeam: one-time product-line disposals in revenue, a grill sale with full return rights, channel stuffing, and bill-and-hold sales; the trail was receivables up 38.5% against revenue up 18.7%, receivables to revenue rising from 21.7% to 25.3%, DSO rising from 79.1 to 92.4 days, a $59 million receivables sale hiding a pro forma DSO of 110.8 days, DSO roughly 40 days worse than the industry median, and a revenue note admitting bill-and-hold sales of 3% of revenue that translated into about 5.9% of earnings (V3 p.318 to p.321).
MicroStrategy: multiple-element contracts with services mischaracterised as immediately recognised licence revenue; the trail was a support-revenue share that climbed for three quarters and then dropped sharply in exactly the quarters where the misallocation happened (V3 p.322, p.323).
WorldCom: line costs capitalised into PP&E; the trail was gross PP&E rising from 30% to 31% to 37% to 45% to 47% of total assets in a common-size balance sheet with no change in strategy (V3 p.326, p.327).

Bankruptcy risk is the extreme of poor results quality.
Altman's Z-score combines liquidity, cumulative profitability, current profitability, market leverage, and asset turnover with weights 1.2, 1.4, 3.3, 0.6, 1.0; below 1.81 is high bankruptcy probability, above 3.00 is low, between is unclear (V3 p.329, p.330).
Its weaknesses are that it is static (Shumway's hazard model fixes that) and accounting-based under a going-concern assumption (Merton-style market models and CDS data fix that); the best models mix both (V3 p.330).

Cash flow quality is judged on OCF.
For an established company high-quality OCF is positive, from sustainable sources, adequate to cover capex, dividends, and debt repayments, and low in volatility relative to peers; a start-up is expected to have negative OCF and CFI funded by financing (V3 p.331).
OCF is harder to manipulate than earnings, but timing tricks (selling receivables, stretching payables, visible as falling DSO and rising days of payables) and classification tricks (interest and dividends under IFRS, trading versus non-trading securities, Nautica moving a $21.1 million short-term investment sale from investing to operating) exist (V3 p.331, p.332, p.337, p.339).
Satyam is the case where an accruals screen failed because reported cash kept pace with profits; the tells were a $53 million derivative "gain" added back in the OCF reconciliation that management could not explain (37% of pre-tax profit), rising DSO, and $500 million parked in non-interest-bearing current accounts, more than 90% of which did not exist (V3 p.332 to p.335).

Balance sheet reporting quality has three attributes: completeness, unbiased measurement, and clear presentation (V3 p.340).
Completeness fails with off-balance-sheet purchase obligations (constructively capitalise them) and with unconsolidated joint ventures near 50% ownership, which also overstate return on sales because the parent books its share of the investee's profit but none of its sales (V3 p.340).
Unbiased measurement fails with unrecognised impairments (goodwill above market capitalisation at Sealed Air, followed by a $1,892.3 million impairment), understated deferred tax valuation allowances, level 3 style non-observable inputs, and pension discount rates (V3 p.341, p.343).
Clear presentation is about disaggregation and the notes; a LIFO inventory note, for example, tells you inventory is unlikely to be overstated (V3 p.343).

Finally, where does risk information come from?
The audit opinion is the least timely source: Kodak's going-concern paragraph was dated five weeks after the bankruptcy filing, and Groupon's material weakness never appeared in an audit opinion (V3 p.344 to p.347).
Auditor changes (three auditors in three years at a Madoff feeder fund), an auditor too small for the client, and independence questions are warning signs (V3 p.347).
The notes carry contingent obligations, pension, and financial instrument sensitivities (Shell's 1% rate move and 10% currency moves); the management commentary (five IFRS elements, MD&A Items 7 and 7A) gives management's view of principal risks, ideally non-boilerplate; 8-K and NT filings, CESR-style ad hoc disclosures, and the financial press (Weil's article that triggered Chanos) round out the list, always confirmed against regulatory filings (V3 p.348 to p.355).

## Formulas and derivations

**Accounting equation and net assets** (V3 p.290)
$$
A - L = E = \text{Net assets}
$$
^f-03-05-1

- $A$, $L$, $E$: total assets, total liabilities, and equity at the balance sheet date.
- Reason it matters: an income statement choice changes $E$ through retained earnings, so an asset or a liability must move by the same amount; overstated revenue therefore means overstated receivables or cash, and understated expense means an overstated asset or an understated liability (V3 p.290).

**Beneish M-score** (V3 p.304)
$$
M = -4.84 + 0.920\,DSR + 0.528\,GMI + 0.404\,AQI + 0.892\,SGI + 0.115\,DEPI - 0.172\,SGAI + 4.679\,\text{Accruals} - 0.327\,LEVI
$$
^f-03-05-2

- Estimated with a probit model; higher (less negative) $M$ means a higher probability of manipulation (V3 p.304, p.305).
- Positive coefficients on DSR, GMI, AQI, SGI, DEPI, and Accruals; negative on SGAI and LEVI, which is counterintuitive for leverage and a favourite distractor.
- Statistically significant variables in Beneish (1999) were DSR, GMI, AQI, SGI, and Accruals (V3 p.304 footnote).

> [!tip] Calculator
> Eight products and an intercept: key each product with `×` and `=`, accumulate with `STO` or write the running total.
> For XYZ: `1.3 × .92 =` 1.196, `1.1 × .528 =` 0.5808, `.8 × .404 =` 0.3232, `1.1 × .892 =` 0.9812, `1.1 × .115 =` 0.1265, `.6 × .172 +/- =` $-0.1032$, `.15 × 4.679 =` 0.7018, `.6 × .327 +/- =` $-0.1962$; sum 3.6103, less 4.84 gives $-1.23$ (V3 p.305).

**Days sales receivable index** (V3 p.304)
$$
DSR = \frac{\text{Receivables}_t / \text{Sales}_t}{\text{Receivables}_{t-1} / \text{Sales}_{t-1}}
$$
^f-03-05-3

- Above 1: receivables grew faster than sales, consistent with premature or fictitious revenue or with customers' deteriorating ability to pay (V3 p.304, p.306).

**Gross margin index** (V3 p.304)
$$
GMI = \frac{\text{Gross margin}_{t-1}}{\text{Gross margin}_t}
$$
^f-03-05-4

- Prior year in the numerator, so above 1 means margins deteriorated, a predisposition to manipulate (V3 p.304, p.306).

**Asset quality index** (V3 p.304)
$$
AQI = \frac{1 - (PPE_t + CA_t)/TA_t}{1 - (PPE_{t-1} + CA_{t-1})/TA_{t-1}}
$$
^f-03-05-5

- $PPE$: property, plant, and equipment; $CA$: current assets; $TA$: total assets.
- The numerator is the share of assets that are neither current nor PP&E (soft assets); a rise signals excessive capitalization of expenditures (V3 p.304).

**Sales growth index** (V3 p.304)
$$
SGI = \frac{\text{Sales}_t}{\text{Sales}_{t-1}}
$$
^f-03-05-6

- Growth itself is not manipulation, but managing the perception of continued growth and the capital needs it creates predisposes firms to manipulate (V3 p.304, p.306).

**Depreciation index** (V3 p.304)
$$
DEPI = \frac{\text{Depreciation rate}_{t-1}}{\text{Depreciation rate}_t}, \qquad \text{Depreciation rate} = \frac{\text{Depreciation}}{\text{Depreciation} + PPE}
$$
^f-03-05-7

- Prior year over current year again, so above 1 means the depreciation rate fell, which can mean lengthened lives and understated expense (V3 p.304, p.306).

**SG&A expense index** (V3 p.304)
$$
SGAI = \frac{SGA_t / \text{Sales}_t}{SGA_{t-1} / \text{Sales}_{t-1}}
$$
^f-03-05-8

- Above 1 means falling administrative and marketing efficiency; the model's coefficient is negative (V3 p.304).

**Beneish accruals** (V3 p.304)
$$
\text{Accruals} = \frac{\text{Income before extraordinary items} - \text{Cash from operations}}{\text{Total assets}}
$$
^f-03-05-9

- The largest coefficient (4.679); higher accruals indicate more of income is non-cash and more easily managed (V3 p.304).

**Leverage index** (V3 p.305)
$$
LEVI = \frac{\text{Leverage}_t}{\text{Leverage}_{t-1}}, \qquad \text{Leverage} = \frac{\text{Debt}}{\text{Assets}}
$$
^f-03-05-10

- Rising leverage could predispose firms to manipulate to avoid covenant breaches, yet the estimated coefficient is negative (V3 p.305).

**Probability of manipulation from the M-score** (V3 p.305)
$$
P(\text{manipulation}) = N(M), \qquad N(-1.78) = 3.8\%, \quad N(-1.49) = 6.8\%
$$
^f-03-05-11

- $M$ is a standard normal variable (mean 0, standard deviation 1); the probability is the left-tail area, NORMSDIST in Excel (V3 p.305).
- Beneish et al. (2013) use $M > -1.78$ as the flag; the cutoff balances the cost of Type I errors (manipulator classified as clean) against Type II errors (clean firm classified as manipulator) (V3 p.305).

> [!tip] Calculator
> The BA II Plus has no normal CDF.
> The exam gives you the probability or asks only for the comparison with $-1.78$; a less negative score is a higher probability.

**Altman Z-score, ratio form** (V3 p.329)
$$
Z = 1.2\,\frac{NWC}{TA} + 1.4\,\frac{RE}{TA} + 3.3\,\frac{EBIT}{TA} + 0.6\,\frac{MVE}{BVL} + 1.0\,\frac{\text{Sales}}{TA}
$$
^f-03-05-12

- $NWC$: net working capital (liquidity); $RE$: retained earnings (cumulative profitability and age); $EBIT/TA$: current profitability, a variant of ROA; $MVE/BVL$: market value of equity over book value of liabilities (solvency, higher is safer); Sales/TA: activity (V3 p.329, p.330).
- All ratios enter as decimals in this form; higher $Z$ is better.
- Interpretation: $Z < 1.81$ high probability of bankruptcy, $Z > 3.00$ low probability, between 1.81 and 3.00 unclear (V3 p.330).
- Derived by discriminant analysis on manufacturers, which is why it combines ratios rather than reading each independently (V3 p.329).

**Altman Z-score, original 1968 form** (V3 p.330)
$$
Z = 0.012\,X_1 + 0.014\,X_2 + 0.033\,X_3 + 0.006\,X_4 + 0.999\,X_5
$$
^f-03-05-13

- $X_1$ to $X_4$ are entered as percentages (10% is 10.0) and $X_5$ as a decimal (200% is 2.0); multiplying the first four coefficients by 100 recovers Formula 12 (V3 p.330).

> [!tip] Calculator
> Ratio form for $NWC/TA = 0.10$, $RE/TA = 0.20$, $EBIT/TA = 0.08$, $MVE/BVL = 0.9$, Sales/TA $= 1.4$: `1.2 × .1 + 1.4 × .2 + 3.3 × .08 + .6 × .9 + 1.4 =` gives 2.604, in the grey zone.

**Earnings persistence** (V3 p.311)
$$
\text{Earnings}_{t+1} = \alpha + \beta_1\,\text{Earnings}_t + \varepsilon
$$
^f-03-05-14

- $\beta_1$ is the persistence coefficient; a higher $\beta_1$ means more persistent earnings and a more useful valuation input (V3 p.311).

**Cash and accruals persistence** (V3 p.311)
$$
\text{Earnings}_{t+1} = \alpha + \beta_1\,\text{Cash flow}_t + \beta_2\,\text{Accruals}_t + \varepsilon
$$
^f-03-05-15

- Sloan (1996): $\beta_1 > \beta_2$, the cash component persists more than the accrual component, so a larger accruals share means lower quality and faster mean reversion (V3 p.311, p.316).

**Aggregate accruals, simple form** (V3 p.312, p.314)
$$
\text{Accruals} \approx \text{Net income} - \text{Operating cash flow}, \qquad \text{scaled by average assets or average net operating income}
$$
^f-03-05-16

- Non-discretionary accruals arise from normal transactions; discretionary (abnormal) accruals are the residual after regressing total accruals on drivers such as credit sales growth and depreciable assets (Jones, modified Jones, the SEC's Accounting Quality Model) (V3 p.311, p.312).
- Positive net income with negative OCF is the extreme signal, but Enron and WorldCom show OCF above net income during fraud, so the measure is not mechanical (V3 p.312, p.314, p.315).

**Balance-sheet-based accruals ratio (from LM06)** (V3 p.397)
$$
\text{BS accruals ratio}_t = \frac{NOA_t - NOA_{t-1}}{(NOA_t + NOA_{t-1})/2}
$$
^f-03-05-17

- $NOA$: net operating assets, operating assets (total assets less cash and short-term investments) minus operating liabilities (total liabilities less long-term debt and debt in current liabilities) (V3 p.396).
- The change in NOA is the balance-sheet-based aggregate accrual; a high or rising ratio is the warning, and subcomponents (change in net receivables over average NOA) isolate the source (V3 p.397).
- Nestle 2014: $5{,}380 / 81{,}519 = 6.6\%$ (V3 p.397).

**Cash-flow-based accruals ratio (from LM06)** (V3 p.397)
$$
\text{CF accruals ratio}_t = \frac{NI_t - (CFO_t + CFI_t)}{(NOA_t + NOA_{t-1})/2}
$$
^f-03-05-18

- $NI$: net income; $CFO$: operating cash flow; $CFI$: investing cash flow, both with their signs (V3 p.397).
- Reason it holds: earnings not backed by operating or investing cash must sit in NOA as accruals; both ratios should tell the same story (Nestle 2014: $3{,}276 / 81{,}519 = 4.0\%$) (V3 p.397).
- LM06 practice: $[4{,}038 - (9{,}822 - 10{,}068)] / 43{,}192 = 9.9\%$ (V3 p.409).

**Days sales outstanding** (V3 p.319)
$$
DSO = \frac{\text{Accounts receivable}}{\text{Revenue}/365}
$$
^f-03-05-19

- Rising DSO means slower collection or revenue that was never genuine; compare over time and with peers (V3 p.319, p.321).

> [!tip] Calculator
> Sunbeam 1997: `1168.2 ÷ 365 = STO 1`, then `295.6 ÷ RCL 1 =` gives 92.4 days; turnover `365 ÷ 92.4 =` 3.95 (V3 p.319).

**Accounts receivable turnover** (V3 p.319)
$$
\text{AR turnover} = \frac{365}{DSO} = \frac{\text{Revenue}}{\text{Accounts receivable}}
$$
^f-03-05-20

- Falling turnover is the same story as rising DSO; a reclassification of receivables to long-term or a receivables sale raises reported turnover for the wrong reason (V3 p.319, p.320, p.368).

**Receivables to revenue** (V3 p.319)
$$
\frac{\text{Receivables}}{\text{Revenue}} \quad \text{and its year-on-year change}
$$
^f-03-05-21

- A rising percentage means a smaller share of sales has been collected; a shipment of unwanted goods or a fictitious sale raises receivables and revenue by the same amount, which raises the ratio (V3 p.319).

**Bill-and-hold earnings contribution** (V3 p.321)
$$
\text{After-tax contribution} = \text{Revenue} \times \text{B\&H share} \times \text{Gross margin} \times (1 - t)
$$
^f-03-05-22

- Sunbeam: $1{,}168.18 \times 3\% = 35.05$; $\times 28.3\% = 9.92$; $\times (1 - 0.35) = 6.45$; $6.45 / 109.42 = 5.9\%$ of earnings from continuing operations (V3 p.321).

**Operating cash flow restated for a classification shift** (V3 p.339)
$$
OCF_{\text{comparable}} = OCF_{\text{reported}} - \text{Inflow reclassified from investing or financing}
$$
^f-03-05-23

- Nautica fiscal 2001: $78{,}018 - 28{,}445 = 49{,}573$; growth becomes $49{,}573 / 62{,}685 - 1 = -21\%$ instead of the reported $78{,}018 / 83{,}801 - 1 = -7\%$ (V3 p.339).
- Total cash flow is unchanged by a shift; only the split between sections moves (V3 p.337).

**Return on sales adjusted for an equity-method investee** (V3 p.340, p.367)
$$
\text{Adjusted return on sales} = \frac{\text{Net income}}{\text{Sales} + \text{Share of investee sales}}
$$
^f-03-05-24

- The parent's income already includes its share of investee profit but its revenue excludes the investee's sales, so the reported margin is overstated; grossing up sales lowers it (V3 p.340, p.367).

**Implied value of non-goodwill assets** (V3 p.343)
$$
\text{Implied value of other assets} = \text{Market capitalization} - \text{Goodwill}
$$
^f-03-05-25

- Market capitalization equals shares outstanding times price.
- If the difference is negative the market attributes less than zero to every other asset, so goodwill is overvalued and a write-off is likely (Sealed Air: $2{,}689 - 4{,}209.6 < 0$, then a $1{,}892.3$ million impairment) (V3 p.343).

**Constructive capitalization of purchase obligations** (V3 p.340)
$$
\text{Adjusted assets} = \text{Reported assets} + PV(\text{purchase obligations}); \qquad \text{Adjusted liabilities} = \text{Reported liabilities} + PV(\text{purchase obligations})
$$
^f-03-05-26

- Applied to material take-or-pay contracts so that leverage reflects the commitment; a completeness adjustment (V3 p.340).

**Recurring (core) pre-tax earnings** (V3 p.366)
$$
\text{Core pre-tax earnings} = \text{Reported pre-tax income} + \text{Non-recurring expenses} - \text{Non-recurring gains}
$$
^f-03-05-27

- Miland: $5.4 + 1.2 + 0.5 = 7.1$ billion; the 1.1 billion of other non-operating expenses is recurring and stays out of the adjustment (V3 p.366).

**After-tax effect of correcting misstatements** (V3 p.366)
$$
\Delta NI = -(\Delta \text{Revenue overstated} + \Delta \text{Costs capitalized}) \times (1 - t)
$$
^f-03-05-28

- Globales: $(50 + 100) \times (1 - 0.25) = 112.5$ million reduction; forgetting the tax shield gives 150, applying the tax rate instead of one minus the tax rate gives 37.5 (V3 p.366).

## Worked examples

### Example 1: Satyam, fictitious reports (V3 p.290 to p.292)

Setup: the CEO created fictitious bank statements to inflate cash and interest income, fake salary accounts he then emptied, and the head of internal audit created fictitious customer accounts and invoices; the World Bank found kickbacks and billing for services not provided; auditors ignored bank confirmations that disagreed with the books.

Part 1: position on the quality spectrum.
The bottom rung, reports based on fictitious transactions; neither framework question can be answered because the information is fabricated (V3 p.291).

Part 2: each act through $A - L = E$.
- World Bank billing for services not provided: receivables and service revenue up; kickbacks, if booked, raise commissions expense and a payable or cut cash; net effect is overstated income, net assets, and equity (V3 p.291).
- Fictitious interest income: income, cash or interest receivable, and equity all overstated, hidden by falsified revenue and cash balances (V3 p.291).
- Fake employees: wages expense up and cash down, so income and equity understated; a real but fraudulent cash outflow, hidden by falsifying revenue and cash (V3 p.292).
- Fictitious revenue: revenue, income, cash or receivables, and equity overstated (V3 p.292).

Part 3: documents falsified.
Invoices to the World Bank, bank statements, employee records, and customer accounts and invoices, all aimed at the external auditors (V3 p.292).

What a reader could have seen: revenue growth compared with growth in short-term and long-term trade receivables and unbilled revenue, plus a separate "investments in bank deposits" line next to cash (V3 p.292). ^ex-03-05-1

### Example 2: Merck, balance sheet reclassification (V3 p.293 to p.294)

Setup: 2002 inventory was reported at $3,411.8 million in the 2002 report; the 2003 report restated 2002 as $2,964.3 million of inventory and $447.5 million inside other assets, the portion held for product launches not expected to sell within a year.
Check: $2{,}964.3 + 447.5 = 3{,}411.8$ (Python: `3411.8`).

Part 1: days of inventory on hand.
A, decreasing: the reported inventory numerator falls relative to cost of goods sold (V3 p.293).

Part 2: current ratio.
A, decrease: current assets fall by the reclassified amount, current liabilities are unchanged (V3 p.294).

Analytical problem: the logic is defensible (operating cycle of one year), but inventory turnover cannot be computed on a consistent basis for 2002 and earlier because the "other assets" portion for those years is not disclosed, so the time series is broken (V3 p.294). ^ex-03-05-2

### Example 3: Digilog, variable interest entity (V3 p.298 to p.299)

Setup: Digilog funded DBS with $10 million of convertible debt convertible into nearly 100% of the equity; DBS's manager owned all of the few thousand dollars of common stock; Digilog did not consolidate for two loss-making years, booked interest income on the debt, then converted and consolidated once DBS turned profitable.

Question: the argument Digilog would most likely make.
C is correct: that the manager has operational and financial control.
It fails because a few thousand dollars against $10 million is not economic control; lacking voting control (A) is not sufficient to avoid consolidation; and B is false, since Digilog is exposed to variable returns through possible losses and the conversion option (V3 p.299).
The SEC held that consolidation would have been the most meaningful presentation even though no specific GAAP then addressed it, and the VIE concept later codified this (V3 p.299). ^ex-03-05-3

### Example 4: Asset impairments and restructuring charges (V3 p.299 to p.300)

Setup: Fuji Electric recorded a 6.5 billion yen impairment on its solar business entirely in fiscal 2012; Elan recorded $42.4 million of restructuring costs in 2012 for closing a San Francisco facility.

Question: recognising the whole charge in one period most likely overstates which periods' income?
A, prior periods: the deterioration happened over a longer time, so earlier years carried assets that were already impaired; the current year is understated unless the charge recurs, and future years would be overstated only if reversals occur, which is unlikely (V3 p.300).
Charging everything now is conservative accounting (V3 p.300).
Analyst response: if such charges recur, spread them across past and current periods to normalise; if truly one-off (a natural disaster) exclude them (V3 p.300).
Related items that suggest prior overstatement: revisions to remaining lives, sudden increases in allowances and reserves, and large loss accruals for environmental or litigation liabilities (V3 p.301). ^ex-03-05-4

### Example 5: XYZ Corporation, Beneish model (V3 p.305 to p.306)

Setup: DSR 1.300, GMI 1.100, AQI 0.800, SGI 1.100, DEPI 1.100, SGAI 0.600, Accruals 0.150, LEVI 0.600.

Products (Python, four decimals): DSR $0.920 \times 1.3 = 1.1960$; GMI $0.528 \times 1.1 = 0.5808$; AQI $0.404 \times 0.8 = 0.3232$; SGI $0.892 \times 1.1 = 0.9812$; DEPI $0.115 \times 1.1 = 0.1265$; SGAI $-0.172 \times 0.6 = -0.1032$; Accruals $4.679 \times 0.15 = 0.7018$; LEVI $-0.327 \times 0.6 = -0.1962$.
Sum of products $= 3.6103$; $M = 3.6103 - 4.84 = -1.2297$.
Probability $N(-1.2297) = 10.94\%$ (Python: `NormalDist().cdf(-1.2297) = 0.1094`).
The curriculum prints $M = -1.231$ and 10.93%; the 0.001 gap is rounding of the intermediate products, and the conclusion is identical (V3 p.305).

Part 1: flag at a $-1.78$ cutoff?
Yes: $-1.23 > -1.78$, and 10.9% is far above the 3.8% probability the cutoff implies (V3 p.306).

Part 2: what DSR, GMI, SGI, DEPI above one mean.
DSR: receivables as a share of sales rose, possible premature revenue or weaker customer credit.
GMI: last year's margin was higher, so margins deteriorated.
SGI: sales grew, which creates growth-perception and capital-raising pressure.
DEPI: the depreciation rate was higher last year, so it fell, possibly understated depreciation (V3 p.306).
Note the AQI of 0.8 and SGAI of 0.6 both point the other way, which the model weighs but does not override. ^ex-03-05-5

### Example 6: Enron, non-recurring items (V3 p.308 to p.309)

Setup (millions): operating income 1,378 (1998), 802 (1999), 1,953 (2000); income before interest, minority interests, and taxes 1,582, 1,995, 2,482; other income in 1999 included equity affiliates 309, gains on non-merchant assets 541, other income 181.

Part 1: trends.
Operating income fell 41.8% in 1999 ($802/1{,}378 - 1$) and rose 143.5% in 2000 ($1{,}953/802 - 1$); the income line below other items rose smoothly, $1{,}995/1{,}582 - 1 = 26.1\%$ and $2{,}482/1{,}995 - 1 = 24.4\%$ (Python: `0.261`, `0.244`) (V3 p.308).

Part 2: non-recurring items and their size.
Gains on non-merchant asset sales and the TNPC stock issuance gain are non-recurring; equity in affiliates and other income are highly variable.
In 1999 the three variable items were $(309 + 541 + 181)/1{,}995 = 1{,}031/1{,}995 = 51.7\%$, which the curriculum rounds to 52% (Python: `0.5168`) (V3 p.309).

Part 3: Chanos's statement.
Market participants were feeding reported income into earnings-based valuation without stripping non-recurring items (V3 p.309). ^ex-03-05-6

### Example 7: Allou Health & Beauty, income versus operating cash flow (V3 p.312 to p.314)

Setup (fiscal years to 31 March): revenues 421,046,773 (2000), 548,146,953 (2001), 564,151,260 (2002); gross profit 53,083,098, 65,556,597, 63,260,672; operating income 22,256,558, 28,490,063, 27,276,779; income from continuing operations 7,043,548, 2,458,367, 6,589,658; net cash used in operations $(27{,}137{,}652)$, $(34{,}195{,}838)$, $(17{,}397{,}230)$; receivables increased 25.7, 9.7, 24.1 million and inventories 40.8, 12.6, 9.1 million.

Part 1: income statement view.
Revenue grew 30.2% then 2.9% (Python: `548.1/421.0 - 1 = 0.302`, `564.2/548.1 - 1 = 0.029`).
Gross margin 12.6%, 12.0%, 11.2% (Python: `0.1261`, `0.1196`, `0.1121`); operating margin 5.3%, 5.2%, 4.8% (Python: `0.0529`, `0.0520`, `0.0484`).
2001 income was depressed by a 5,642,678 impairment; every year is profitable and looks stable (V3 p.313).

Part 2: income versus OCF.
Positive income and negative OCF in all three years; persistent negative OCF is not sustainable for a going concern (V3 p.313).
Accruals proxy, income minus OCF: 34.2, 36.7, 24.0 million (Python: `7043548 + 27137652 = 34181200`, `2458367 + 34195838 = 36654205`, `6589658 + 17397230 = 23986888`), each several times reported income.

Part 3: the reconciling items.
Rising receivables and inventories explain most of the gap; the company was accumulating inventory and not collecting; under the indirect method an increase in a current asset is subtracted from income (V3 p.314).
Afterwards the warehouses burned, management was blamed, and sales and inventories were shown to have been fraudulently inflated; the company also changed auditor in each of 2000, 2001, and 2002 (V3 p.312, p.344). ^ex-03-05-7

### Illustration: Enron and WorldCom, when OCF exceeds net income (V3 p.314 to p.315)

Enron quarterly (31 March): net income 338 (2000) and 425 (2001) with operating cash used of $(457)$ and $(464)$, the Allou pattern (V3 p.314).
Enron annual: OCF to net income $1{,}640/703 = 2.33$ (1998), $1{,}228/893 = 1.38$ (1999), $4{,}779/979 = 4.88$ (2000) (Python: `2.333`, `1.375`, `4.882`); the question is why OCF was more than double, almost 50% above, and almost five times net income, and the answer was transactions designed to generate OCF (V3 p.314).
WorldCom: OCF 11,005, 7,666, 7,994 against net income 4,013, 4,153, 1,501 for 1999 to 2001; OCF above earnings looked like quality, but the fraud was capitalising line costs, which moved the outflow to investing (V3 p.315).
Lesson: accrual measures are indicators, not mechanical tests; check investing activity before trusting OCF (V3 p.315). ^ex-03-05-8

### Illustration: Sunbeam receivables and bill-and-hold (V3 p.318 to p.321)

Setup ($ millions): revenue 1,016.9, 984.2, 1,168.2 for 1995 to 1997; gross receivables 216.2, 213.4, 295.6; $59 million of receivables sold in December 1997; bill-and-hold sales 3% of 1997 revenue; gross margin 28.3%; tax 35%; earnings from continuing operations 109.42.

Growth: revenue $984.2/1{,}016.9 - 1 = -3.2\%$, $1{,}168.2/984.2 - 1 = 18.7\%$; receivables $-1.3\%$ then $295.6/213.4 - 1 = 38.5\%$ (Python: `-0.032`, `0.187`, `-0.013`, `0.385`) (V3 p.319).
Receivables to revenue: 21.3%, 21.7%, 25.3% (Python: `0.2126`, `0.2168`, `0.2530`).
DSO: $216.2/(1{,}016.9/365) = 77.6$; $213.4/(984.2/365) = 79.1$; $295.6/(1{,}168.2/365) = 92.4$ (Python: `77.6`, `79.1`, `92.4`); turnover $365/DSO = 4.7, 4.6, 4.0$ (V3 p.319).
Exhibit 12 prints 77.7, 79.2, 92.3 from unrounded inputs; the differences are immaterial (V3 p.320).
Pro forma 1997 with the sold receivables added back: $295.6 + 59 = 354.6$; growth $354.6/213.4 - 1 = 66.1\%$; to revenue $354.6/1{,}168.2 = 30.4\%$; DSO $354.6/(1{,}168.2/365) = 110.8$; turnover 3.3 (Python: `0.6617`, `0.3035`, `110.8`, `3.29`) (V3 p.320).
Industry median DSO 44.6, 46.7, 50.4, so Sunbeam was 33.0, 32.5, and 41.9 days worse (V3 p.321).
Bill-and-hold: $1{,}168.18 \times 0.03 = 35.05$; $\times 0.283 = 9.92$; $\times 0.65 = 6.45$; $6.45/109.42 = 5.9\%$ (Python: `35.05`, `9.92`, `6.45`, `0.0589`) (V3 p.321).
Reading: receivables growth outrunning revenue growth, a rising receivables share, rising DSO, a receivables sale that flattered every ratio, and a note admitting a questionable practice that was 6% of earnings (V3 p.319 to p.322). ^ex-03-05-9

### Illustration: MicroStrategy revenue mix (V3 p.322 to p.324)

Setup ($ thousands): licences 15,873, 36,601, 72,721 and support 6,730, 16,956, 33,709 for 1996 to 1998; a $4.5 million Q4 1998 contract and a $14.1 million Q4 1999 contract were booked as licence revenue although they were largely services.

Annual mix: licences $15{,}873/22{,}603 = 70.2\%$, $36{,}601/53{,}557 = 68.3\%$, $72{,}721/106{,}430 = 68.3\%$ (Python: `0.702`, `0.683`, `0.683`) (V3 p.323).
Had the $4.5 million not been recognised at all, revenue would have been $106{,}430 - 4{,}500 = 101{,}930$ and support $33{,}709/101{,}930 = 33.1\%$ (Python: `101930`, `0.331`) (V3 p.323).
Quarterly support share: 28.2%, 31.7%, 37.3%, then 29.3% in 4Q98; 35.4%, 31.9%, 29.9%, 26.8% in 1999, with the sharp drops in exactly the two quarters of misallocation (V3 p.323, p.324).
Reading: there is no business reason for the licence and support proportions to swing quarter to quarter; a stated multiple-deliverable policy plus an erratic mix is the cue to question allocation (V3 p.324). ^ex-03-05-10

### Illustration: WorldCom common-size balance sheet (V3 p.326 to p.327)

Gross PP&E as a share of total assets: 30%, 31%, 37%, 45%, 47% for 1997 to 2001; the fraud (capitalising line costs paid to other carriers) began in 1999 and no strategy change explained the jump (V3 p.326, p.327).
Reading: an under-reported expense needs an offsetting balance sheet build-up; scan non-current assets quarter to quarter, relate margins to balance sheet growth, watch asset turnover, depreciation relative to the asset base, and capex relative to gross PP&E (V3 p.327, p.328). ^ex-03-05-11

### Illustration: Satyam cash flow statement and receivables (V3 p.332 to p.335)

An accruals screen missed Satyam because reported cash kept pace with profit (V3 p.332).
Quarter to 30 June 2008: a $53.0 million "gain/(loss) on foreign exchange forward and option contracts" was added back in reconciling profit before tax of 143.1 to cash from operations; a gain should not be added back, and it was $53/143.1 = 37\%$ of pre-tax profit (Python: `0.370`); management could not explain it on the call (V3 p.333).
Receivables (millions): revenue 793.6, 1,096.3, 1,461.4, 2,138.1 for 2005 to 2008; gross receivables 178.3, 238.1, 386.9, 539.1.
DSO $= 82.0, 79.3, 96.6, 92.0$ (Python: `82.0`, `79.3`, `96.6`, `92.0`); the 2006 to 2007 jump of 17 days was the concern, and the 20-F blamed an "increase in collection period" (V3 p.333, p.334).
Receivables grew 62.5% in 2007 against revenue growth of 33.3% (Python: `0.625`, `0.333`) (V3 p.334).
Cash: $500 million in non-interest-bearing current accounts with no explanation; the CEO later confessed that over 90% of reported cash did not exist (V3 p.334, p.335). ^ex-03-05-12

### Example 8: Sunbeam statement of cash flows (V3 p.335 to p.336)

Setup ($ thousands): 1996 restructuring, impairment, and other costs 154,869 and other non-cash special charges 128,800; 1997 restructuring accrual $(43{,}378)$; 1997 receivables $(84{,}576)$ and inventories $(100{,}810)$; OCF 81,516, 14,163, $(8{,}249)$ for 1995 to 1997 against net earnings 50,511, $(228{,}262)$, 109,415.

Part 1: inflated and reversed restructuring charges.
The indirect reconciliation shows non-cash 1996 charges of $154{,}869 + 128{,}800 = 283{,}669$, about $284 million (Python: `283669`), and a 1997 reversal of about $43 million through the restructuring accrual line; big-bath then release manufactures an apparent turnaround after the new CEO arrived (V3 p.336).

Part 2: improper revenue recognition.
Net income, receivables, and inventories: income and receivables overstated, with the receivables increase shown as a large negative adjustment; the 1997 inventory build reflects goods that were "sold" and later returned (V3 p.336).
Cross-check: 1997 earnings of 109,415 with OCF of $(8{,}249)$ is the Allou pattern again. ^ex-03-05-13

### Example 9: Nautica, classification of cash flows (V3 p.337 to p.339)

Setup ($ thousands): the fiscal 2000 report showed OCF 62,685 and an investing inflow of 21,116 from short-term investment sales; the fiscal 2001 report restated fiscal 2000 OCF as 83,801 and reported fiscal 2001 OCF of 78,018 including 28,445 of short-term investment sales.

Part 1: fiscal 2000 OCF as first reported and as restated.
62,685 and 83,801 (V3 p.339).

Part 2: where the 21,116 went.
$83{,}801 - 62{,}685 = 21{,}116$ (Python: `21116`); it moved from investing into "changes in operating assets and liabilities" (V3 p.339).

Part 3: growth as reported and on the original basis.
Reported: $78{,}018/83{,}801 - 1 = -6.9\%$, about $-7\%$ (Python: `-0.069`).
Original basis: $78{,}018 - 28{,}445 = 49{,}573$; $49{,}573/62{,}685 - 1 = -20.9\%$, about $-21\%$ (Python: `49573`, `-0.209`) (V3 p.339).
Detection: compare the same year across two successive annual reports; restatements, recasts, dropped voluntary disclosures, and new risk disclosures all deserve an explanation (V3 p.340). ^ex-03-05-14

### Example 10: Sealed Air, goodwill (V3 p.341 to p.343)

Setup: 192,062,185 shares; price about $18 in December 2011 and $14 in August 2012; goodwill 4,209.6 million and intangibles 2,035.7 million on total assets of 11,432.0 million at end 2011; 2012 impairment of goodwill and other intangibles 1,892.3 million.

Part 1: market value.
$192{,}062{,}185 \times 18 = 3{,}457$ million; $\times 14 = 2{,}689$ million (Python: `3457.1`, `2688.9`) (V3 p.343).

Part 2: goodwill versus market value.
Goodwill of 4,209.6 exceeded both; goodwill plus intangibles were $(4{,}209.6 + 2{,}035.7)/11{,}432.0 = 54.6\%$ of assets, about 55% (Python: `0.546`) (V3 p.343).

Part 3: why a clue to write-offs.
If market cap equalled goodwill the implied value of all other assets would be zero; here it is negative, $2{,}689 - 4{,}209.6 = -1{,}521$ million (Python: `-1520.7`), so goodwill is overvalued (V3 p.343).

Part 4: was the article right?
Yes: the 1,892.3 million impairment followed in 2012, and goodwill fell to 3,191.4 million (V3 p.343). ^ex-03-05-15

### Example 11: Shell, use of risk disclosures (V3 p.349 to p.351)

Setup: most debt raised centrally and swapped to floating dollar rates; subsidiaries discouraged from further rate management; a 1% rate rise cuts pre-tax income by $27 million (2011: $146 million); a 10% appreciation of the Australian dollar raises pre-tax income by $246 million; 2012 pre-tax income $50,289 million.

Part 1: centralised or decentralised?
Centralised: debt is raised centrally, swaps convert most of it to floating dollar rates, and subsidiary-level rate management is discouraged (V3 p.351).

Part 2: significance of a 1% rate rise.
$27/50{,}289 = 0.054\%$ of pre-tax income, under 0.1%, insignificant (Python: `0.00054`) (V3 p.351).

Part 3: 10% Australian dollar appreciation.
$+246$ million, $246/50{,}289 = 0.49\%$, about 0.5% of pre-tax income (Python: `0.0049`) (V3 p.351).
Note the sign differences across currencies (sterling $-185$, Canadian dollar $+131$) and that net asset effects come from translation of non-dollar-functional entities, not from income (V3 p.351). ^ex-03-05-16

## Item-set patterns

> [!warning] Trap 1: the warning sign stated backwards
> The vignette lists research notes such as "discounts and returns have decreased", "receivables turnover is increasing", "depreciable lives were shortened", or "operating income is much lower than OCF".
> Correct: only the direction in Exhibit 4 is a warning sign: increases in discounts and returns, decreasing receivables turnover (rising DSO), lengthened lives, OCF much lower than operating income, receivables growing faster than revenue, margins rising, revenue growing faster than peers (V3 p.296, p.303).
> Distractors reverse the sign; shortening lives is conservative, and OCF above operating income is not the Exhibit 4 flag (V3 p.366, p.367).

> [!warning] Trap 2: OCF above net income read as proof of quality
> A firm shows OCF comfortably above earnings every year.
> Correct: check the investing section and the common-size balance sheet; capitalised operating costs (WorldCom) and transactions engineered to produce OCF (Enron) both inflate OCF (V3 p.314, p.315, p.327).
> Distractor: "earnings are high quality because cash exceeds income", which is the false sense of security the curriculum names explicitly (V3 p.315).

> [!warning] Trap 3: Beneish signs and the direction of the cutoff
> M-scores of $-1.54$, $-2.60$, $-1.86$ are given, with year-on-year changes.
> Correct: the highest (least negative) score is the most likely manipulator; compare each with $-1.78$; the change column is a distractor (V3 p.305, p.367).
> Also tested: SGAI and LEVI carry negative coefficients, an index above 1 for GMI or DEPI means deterioration because the prior year is in the numerator, and the model gives associations, not causes, with declining power over time (V3 p.304, p.307).

> [!warning] Trap 4: persistence coefficients
> $E_{t+1} = \alpha + \beta_1 CF_t + \beta_2 \text{Accruals}_t$, and the question asks when persistence is highest.
> Correct: $\beta_1 > \beta_2$, the cash component persists more (V3 p.311, p.366).
> Distractors: $\beta_2 > \beta_1$ (reversed) and $\beta_1 < 0$ (nonsense: a negative coefficient on cash would mean cash predicts lower earnings).

> [!warning] Trap 5: mean reversion speed with two similar ROEs
> Two firms with the same above-average ROE; one has a larger cash component.
> Correct: both revert, the one with more accruals reverts faster, so the cash-heavy firm's ROE declines more slowly (V3 p.316, p.366).
> Distractors: "same rate" (ignores composition) and "more rapidly" (reverses the accruals effect).

> [!warning] Trap 6: reclassified receivables and the ratios that "improve"
> Receivables drop sharply and long-term trade receivables rise, or receivables are sold.
> Correct: DSO falls, turnover rises, and the current ratio falls, all mechanically; the improvement is fake (V3 p.292, p.320, p.368).
> Distractors: "turnover will decrease" and "current ratio will increase", which get the mechanics wrong.

> [!warning] Trap 7: which balance sheet attribute is missing
> Obsolete inventory not written down, off-balance-sheet purchase obligations, or a single aggregated "other assets" line.
> Correct: unbiased measurement for the impairment, completeness for the off-balance-sheet item, clear presentation for the aggregation (V3 p.340, p.341, p.343, p.367).
> Distractor: choosing completeness for the inventory case because the note "is informative", when the note being informative is exactly why presentation is not the problem.

> [!warning] Trap 8: equity-method investee and return on sales
> A 49% unconsolidated profitable investee; peers consolidate.
> Correct: reported return on sales is overstated because income includes the share of profit but sales exclude the investee's revenue; grossing up sales lowers the margin (V3 p.340, p.367).
> Distractors: "remain the same" and "increase".

> [!warning] Trap 9: revenue recognition flags in inventory
> A company let customers take excess product with free return rights and later restated.
> Correct: overstated revenue overstates net income and receivables and understates inventory, because goods still effectively owned were removed from inventory (V3 p.336, p.367).
> Distractors: "understated net income" and "understated receivables" reverse the effect.

> [!warning] Trap 10: adjusting income for misstatements and non-recurring items
> Improper revenue of 50, improper capitalisation of 100, tax 25%; or pre-tax income 5.4 with 1.2 of acquisition costs, 0.5 restructuring, and 1.1 of other non-operating expense.
> Correct: $\Delta NI = 150 \times 0.75 = 112.5$; core pre-tax $= 5.4 + 1.2 + 0.5 = 7.1$ (V3 p.366).
> Distractors: 150 (no tax), 37.5 (tax rate instead of one minus the rate), 4.3 or 4.8 (subtracting the non-recurring items or adding the recurring one).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM05-Evaluating-Quality-of-Financial-Reports-Practice-Problems]]

## Cross-links

- [[LM01-Intercorporate-Investments]]: supplies the equity method (why an unconsolidated 49% investee overstates return on sales), consolidation and VIE rules behind the Digilog case, and goodwill measurement and impairment behind the acquisition incentive to understate amortizable intangibles.
- [[LM02-Employee-Compensation-Post-Employment-and-Share-Based]]: pension discount rate and other actuarial estimates are the unbiased-measurement items this module tells you to examine, and the pension remeasurement in OCI is one of the OCI items the analyst must decide whether to treat as income.
- [[LM03-Multinational-Operations]]: translation adjustments in OCI, functional currency choices, and the segment-shifting warning (Step 6) for multinationals; Shell's FX sensitivity disclosure is read with LM03's translation mechanics.
- [[LM06-Integration-of-Financial-Statement-Analysis-Techniques]]: takes the balance-sheet-based and cash-flow-based accruals ratios (Formulas 17 and 18), the OCF versus net income comparison, and the DuPont decomposition into a full company analysis (Nestle), so this module's indicators become that module's phases 3 and 4.
- [[LM04-Market-Based-Valuation-Price-and-Enterprise-Value-Multiples]]: normalized earnings and the treatment of non-recurring items feed the E in P/E; Enron's non-recurring gains and classification shifting are exactly the adjustments a multiples analyst must make.
- [[LM01-Analysis-of-Dividends-and-Share-Repurchases]]: the cash flow quality test that OCF covers capex, dividends, and debt repayment is the sustainability test for payout policy; FCFE coverage of dividends and repurchases is the same question from the corporate side.

## Self-test

> [!question] ST1
> An analyst computes the following Beneish variables for Corvid Ltd: DSR 1.25, GMI 1.05, AQI 1.10, SGI 1.30, DEPI 1.02, SGAI 0.95, Accruals 0.08, LEVI 1.05.
> Using the $-1.78$ cutoff, Corvid's M-score and classification are closest to:
> A. $-1.55$, flagged as a likely manipulator.
> B. $-1.55$, not flagged.
> C. $-0.53$, flagged as a likely manipulator.

> [!question] ST2
> Two manufacturers report the following ratios.
> Firm X: NWC/TA 0.10, RE/TA 0.20, EBIT/TA 0.08, MVE/BVL 0.90, Sales/TA 1.40.
> Firm Y: NWC/TA $-0.05$, RE/TA 0.05, EBIT/TA 0.02, MVE/BVL 0.40, Sales/TA 0.90.
> Using Altman's Z-score, the analyst should conclude that:
> A. X is in the grey zone and Y has a high probability of bankruptcy.
> B. both firms have a low probability of bankruptcy because Z exceeds 1.81 for each.
> C. X has a low probability of bankruptcy and Y is in the grey zone.

> [!question] ST3
> Revenue rises from 1,200 to 1,380 and gross receivables from 180 to 240 over one year.
> Which statement is most accurate?
> A. DSO rises from about 55 to about 63 days, and receivables growth of 33% outpacing revenue growth of 15% is a warning sign of premature revenue recognition.
> B. Receivables turnover rises, which indicates improved collection.
> C. The receivables-to-revenue ratio falls, which is consistent with high revenue quality.

> [!question] ST4
> Net operating assets rise from 500 to 560; net income is 60, CFO 40, CFI $-30$.
> The balance-sheet-based and cash-flow-based accruals ratios are closest to:
> A. 11.3% and 9.4%.
> B. 12.0% and 3.8%.
> C. 11.3% and 13.2%.

> [!question] ST5
> An analyst concludes that Halden overstated revenue by 80 and improperly capitalised 40 of operating costs; the tax rate is 30%.
> The decline in net income after correcting both items is closest to:
> A. 36.
> B. 84.
> C. 120.

> [!question] ST6
> Pell Corp reports net income 120 on sales 1,000, a 12.0% return on sales; income includes its share of a profitable 40%-owned equity-method investee whose sales attributable to Pell's share are 400.
> Peers consolidate similar holdings.
> The comparable return on sales is closest to:
> A. 8.6%.
> B. 12.0%.
> C. 16.8%.

> [!question] ST7
> Ostrava has 150 million shares at $12 and reports goodwill of $2,100 million.
> The value the market implicitly assigns to all non-goodwill assets, and the implication, are:
> A. $-300$ million; goodwill appears overvalued and a write-off is likely.
> B. $+300$ million; goodwill appears fairly stated.
> C. $1,800$ million; no inference can be drawn without total assets.

> [!question] ST8
> An IFRS reporter that had classified interest paid as operating reclassifies it as financing this year with no other change in activity.
> Compared with last year, its reported:
> A. total cash flow rises and OCF rises.
> B. total cash flow is unchanged and OCF rises.
> C. total cash flow is unchanged and OCF falls.

> [!question] ST9
> A shipping company has material take-or-pay purchase contracts that are disclosed but not recognised.
> The balance sheet reporting-quality attribute most affected, and the analyst's adjustment, are:
> A. completeness; add the present value of the obligations to both assets and liabilities.
> B. unbiased measurement; discount the obligations at the risk-free rate and deduct them from equity.
> C. clear presentation; disaggregate the obligations in the notes.

> [!question] ST10
> Which of the following is the least timely source of information about a company's reporting risk?
> A. An NT filing announcing inability to file on time.
> B. The resignation of the chief financial officer announced on Form 8-K.
> C. The external auditor's opinion on the annual financial statements.

> [!success]- Answer key
> ST1: A. Products: $0.920 \times 1.25 = 1.1500$; $0.528 \times 1.05 = 0.5544$; $0.404 \times 1.10 = 0.4444$; $0.892 \times 1.30 = 1.1596$; $0.115 \times 1.02 = 0.1173$; $-0.172 \times 0.95 = -0.1634$; $4.679 \times 0.08 = 0.3743$; $-0.327 \times 1.05 = -0.3434$; sum 3.2932; $M = 3.2932 - 4.84 = -1.547$ (Python: `-1.5467`), probability $N(-1.547) = 6.1\%$.
> $-1.55$ is less negative than $-1.78$, so the score exceeds the cutoff and the firm is flagged.
> B is the trap of reading $-1.55$ as "below $-1.78$" because it looks like a smaller number; the cutoff is on the number line, and $-1.55 > -1.78$.
> C adds the SGAI and LEVI terms instead of subtracting them ($-1.5467 + 2 \times 0.1634 + 2 \times 0.3434 = -0.53$) (V3 p.304, p.305).
> ST2: A. $Z_X = 1.2(0.10) + 1.4(0.20) + 3.3(0.08) + 0.6(0.90) + 1.0(1.40) = 0.12 + 0.28 + 0.264 + 0.54 + 1.40 = 2.604$ (Python: `2.604`), between 1.81 and 3.00, unclear.
> $Z_Y = 1.2(-0.05) + 1.4(0.05) + 3.3(0.02) + 0.6(0.40) + 1.0(0.90) = -0.06 + 0.07 + 0.066 + 0.24 + 0.90 = 1.216$ (Python: `1.216`), below 1.81, high probability.
> B misreads 1.216 as above 1.81 or treats 1.81 as the only threshold; C shifts both firms one zone up (V3 p.329, p.330).
> ST3: A. $DSO_0 = 180/(1{,}200/365) = 54.75$; $DSO_1 = 240/(1{,}380/365) = 63.48$ (Python: `54.75`, `63.48`); receivables grew $240/180 - 1 = 33.3\%$ against revenue $1{,}380/1{,}200 - 1 = 15.0\%$.
> B: turnover falls from 6.67 to 5.75. C: receivables to revenue rises from 15.0% to 17.4% (V3 p.319).
> ST4: A. Average NOA $= (500 + 560)/2 = 530$; balance-sheet ratio $= 60/530 = 11.3\%$; cash-flow ratio $= [60 - (40 - 30)]/530 = 50/530 = 9.4\%$ (Python: `0.1132`, `0.0943`).
> B divides the change by opening NOA (12.0%) and computes $(60 - 40)/530$ without CFI; C adds CFI with the wrong sign, $[60 - (40 + 30)]/530 = -1.9\%$ in magnitude, or $(60 + 10)/530 = 13.2\%$ (V3 p.397).
> ST5: B. Pre-tax reduction $80 + 40 = 120$; after tax $120 \times 0.70 = 84$ (Python: `84.0`).
> A applies 30% instead of 70%; C ignores tax (V3 p.366).
> ST6: A. $120/(1{,}000 + 400) = 8.57\%$ (Python: `0.0857`); the reported 12.0% (B) includes investee profit without investee sales; C multiplies instead of dividing by the gross-up factor (V3 p.340, p.367).
> ST7: A. Market cap $= 150 \times 12 = 1{,}800$; $1{,}800 - 2{,}100 = -300$ (Python: `1800`, `-300`); a negative implied value for every other asset means goodwill is overvalued.
> B has the sign wrong; C stops at market cap and ignores that the comparison with goodwill alone is what the curriculum uses (V3 p.343).
> ST8: B. A classification shift never changes total cash flow; moving an outflow from operating to financing raises OCF by the interest paid, with no economic change (V3 p.337).
> A changes the total; C reverses the direction.
> ST9: A. Off-balance-sheet obligations are a completeness failure; constructive capitalisation adds the present value of the payments to assets and liabilities.
> B confuses the attribute and the mechanics; C addresses presentation, which is not the problem when the item is off the balance sheet entirely (V3 p.340).
> ST10: C. The audit opinion covers historical statements and typically arrives after other signals (Kodak's going-concern paragraph postdated the bankruptcy filing); NT filings and senior financial officer resignations are timely warning signs (V3 p.344, p.345, p.354, p.355).

## Flashcards

#flashcards/cfa-l2/03-Financial-Statement-Analysis/lm05

Financial reporting quality::Whether the information disclosed is relevant and faithfully represents economic reality, that is, decision-useful (V3 p.286).
Results or earnings quality::Whether the earnings and cash generated provide an adequate return (at or above the cost of capital) and are sustainable (V3 p.286, p.288).
Relationship between reporting quality and earnings quality::High reporting quality is necessary to assess earnings quality but not sufficient for high earnings quality (V3 p.287).
Two questions of the conceptual framework::Are the reports GAAP-compliant and decision-useful? Are the results of high quality, adequate and sustainable? (V3 p.288).
Quality spectrum, top to bottom::GAAP decision-useful sustainable adequate; GAAP decision-useful but low earnings quality; within GAAP but biased choices; within GAAP but earnings management (real and accounting); non-compliant accounting; fictitious transactions (V3 p.288).
Aggressive accounting choice::Increases current-period reported performance and position and may decrease later periods (V3 p.289).
Conservative accounting choice::Decreases current-period reported performance and position and may increase later periods (V3 p.289).
Earnings smoothing::Understating earnings in good periods and overstating in bad periods to reduce reported volatility (V3 p.289).
Effect of premature revenue recognition on the statements::Overstated income, equity, and assets (usually receivables) (V3 p.290).
Four ways to inflate OCF operationally::Defer payables, accelerate customer payments, defer inventory purchases, defer maintenance and research spending (V3 p.290).
Why acquisitions tempt understatement of amortizable intangibles::The residual goes to goodwill, which is not amortized, so future expense is lower until impairment (V3 p.298).
Single-period impairment or restructuring charge most likely overstates::Prior periods' net income (V3 p.300).
Seven steps to evaluate financial report quality::Understand company and industry; learn about management; identify significant judgment areas; compare with prior year and peers; check warning signs; check segment shifting; apply quantitative tools (V3 p.302, p.303).
Beneish M-score intercept and coefficient signs::Intercept $-4.84$; positive on DSR, GMI, AQI, SGI, DEPI, Accruals; negative on SGAI and LEVI (V3 p.304).
DSR formula::(Receivables/Sales) this year divided by (Receivables/Sales) last year (V3 p.304).
GMI formula and reading::Gross margin last year over gross margin this year; above 1 means margins deteriorated (V3 p.304).
AQI formula::$[1 - (PPE + CA)/TA]_t$ over the same ratio at $t-1$; rising soft assets suggest capitalization (V3 p.304).
DEPI formula and reading::Depreciation rate last year over this year, with rate = Depreciation/(Depreciation + PPE); above 1 means the rate fell (V3 p.304).
Beneish accruals definition::(Income before extraordinary items minus cash from operations) over total assets, coefficient 4.679 (V3 p.304).
LEVI definition::Debt-to-assets this year over last year, coefficient $-0.327$ (V3 p.305).
Beneish probability cutoff::M-score above $-1.78$, a 3.8% probability of manipulation; $-1.49$ corresponds to 6.8% (V3 p.305).
Micro-problem: M-score products sum to 3.6103; M-score?::$3.6103 - 4.84 = -1.23$, above $-1.78$, flagged; keystrokes 3.6103 - 4.84 = (V3 p.305).
Micro-problem: M-scores $-1.54$, $-2.60$, $-1.86$; most likely manipulator?::$-1.54$, the least negative and the only one above $-1.78$ (V3 p.367).
Two limitations of quantitative misreporting models::They establish associations, not cause and effect; predictive power declines because managers test their tactics against the model (V3 p.307).
Four indicators of earnings quality::Recurring earnings; persistence and accruals; beating benchmarks; external confirmations such as enforcement actions and restatements (V3 p.307).
Classification shifting::Moving normal expenses into special items or discontinued operations so core earnings look higher with net income unchanged (V3 p.309).
Persistence regression::$E_{t+1} = \alpha + \beta_1 E_t + \varepsilon$; higher $\beta_1$ means more persistent earnings (V3 p.311).
Cash versus accruals persistence::In $E_{t+1} = \alpha + \beta_1 CF_t + \beta_2 \text{Accruals}_t + \varepsilon$, $\beta_1 > \beta_2$ (V3 p.311).
Discretionary versus non-discretionary accruals::Non-discretionary arise from normal transactions; discretionary come from unusual transactions or choices, possibly to distort earnings, and are the outliers to watch (V3 p.311).
Loudest accrual signal::Positive net income with negative operating cash flow, as at Allou and Enron's quarters (V3 p.312, p.314).
Why OCF above net income is not proof of quality::WorldCom capitalised line costs, which moved the outflow to investing and inflated OCF (V3 p.315).
Mean reversion in earnings::Extreme high or low earnings revert to normal through competition and management change; a large accruals component speeds the reversion (V3 p.315, p.316).
Beating benchmarks as a quality flag::Exactly meeting or narrowly beating consensus clusters suspiciously and raises earnings quality questions, though the interpretation is debated (V3 p.316).
Sunbeam revenue devices::One-time product-line disposals in revenue, a grill sale with full return rights, channel stuffing, bill-and-hold sales (V3 p.318).
DSO formula::Accounts receivable divided by (Revenue/365); turnover is 365/DSO (V3 p.319).
Micro-problem: receivables 295.6, revenue 1,168.2; DSO?::$295.6/(1{,}168.2/365) = 92.4$ days; keystrokes 1168.2 ÷ 365 = STO 1, 295.6 ÷ RCL 1 = (V3 p.319).
Micro-problem: Sunbeam 1997 receivables up 38.5%, revenue up 18.7%; reading?::Receivables outrunning revenue suggests pulled-forward sales via discounts or return rights (V3 p.320).
Micro-problem: bill-and-hold 3% of revenue 1,168.18, gross margin 28.3%, tax 35%; share of earnings 109.42?::$1{,}168.18 \times 0.03 \times 0.283 \times 0.65 = 6.45$; $6.45/109.42 = 5.9\%$ (V3 p.321).
WorldCom tell::Gross PP&E rose from 30% and 31% of total assets to 37%, 45%, 47% with no strategy change (V3 p.327).
Altman Z-score weights::1.2 NWC/TA, 1.4 RE/TA, 3.3 EBIT/TA, 0.6 MVE/BVL, 1.0 Sales/TA (V3 p.329).
Altman Z-score zones::Below 1.81 high bankruptcy probability; above 3.00 low; between unclear (V3 p.330).
Micro-problem: NWC/TA 0.10, RE/TA 0.20, EBIT/TA 0.08, MVE/BVL 0.9, Sales/TA 1.4; Z?::$0.12 + 0.28 + 0.264 + 0.54 + 1.4 = 2.60$, grey zone (V3 p.329, p.330).
Two shortcomings of the Altman model::Static single-period measures (hazard models fix); accounting data under a going-concern assumption (market-based Merton models fix) (V3 p.330).
Four characteristics of high-quality OCF for an established company::Positive; from sustainable sources; adequate to cover capex, dividends, and debt repayment; low volatility relative to peers (V3 p.331).
IFRS versus US GAAP classification of interest and dividends::IFRS allows interest paid as operating or financing and interest and dividends received as operating or investing; US GAAP requires all as operating (V3 p.337).
Three attributes of balance sheet reporting quality::Completeness, unbiased measurement, clear presentation (V3 p.340).
Constructive capitalization::Add the present value of purchase obligations to reported assets and liabilities (V3 p.340).
Why an unconsolidated investee overstates return on sales::The parent includes its share of investee profit but none of the investee's sales (V3 p.340).
Goodwill above market capitalization implies::A negative implied value for all other assets, so goodwill is overvalued and a write-off is likely (V3 p.343).
Why the audit opinion is a weak risk source::It is historical and rarely timely; Kodak's going-concern paragraph was dated after the bankruptcy filing (V3 p.344, p.345).
Five elements of the IFRS management commentary::Nature of the business; objectives and strategies; resources, risks, and relationships; results and prospects; performance measures and indicators (V3 p.352).
NT filing::Notification of inability to file on time; highly likely to signal reporting quality problems (V3 p.354).
Trap: "OCF exceeds operating income, so it is a warning sign"::Wrong direction; the Exhibit 4 sign is OCF much lower than operating income (V3 p.296, p.367).
Trap: "obsolete inventory not written down is a completeness problem"::Wrong; it is unbiased measurement (V3 p.341, p.367).
Trap: "the firm with the bigger drop in M-score is the most likely manipulator"::Wrong; the level relative to $-1.78$ matters, not the change (V3 p.367).
Balance-sheet-based accruals ratio (earnings quality screen)::$(NOA_t - NOA_{t-1})$ over average NOA, from LM06 (V3 p.397).
Cash-flow-based accruals ratio (earnings quality screen)::$[NI - (CFO + CFI)]$ over average NOA, from LM06 (V3 p.397).
In the Beneish model the two variables with negative coefficients are {{SGAI and LEVI}} (V3 p.304).
High-quality earnings provide a return {{equal to or above the cost of capital}} and are {{sustainable}} (V3 p.288).
Earnings with a larger accruals component are {{less persistent}} and revert to the mean {{faster}} (V3 p.316).

## Common mistakes

1. Reading a warning sign in the wrong direction: the flags are increases in discounts and returns, falling receivables turnover, lengthened lives, and OCF much lower than operating income; the opposites are not flags (V3 p.296, p.366, p.367).
2. Treating OCF above net income as proof of earnings quality without checking investing outflows for capitalised operating costs (V3 p.315, p.327).
3. Ranking Beneish M-scores by the change rather than the level, or reading $-1.55$ as "below the cutoff" because it is a smaller number in absolute value; less negative means more likely to manipulate (V3 p.305, p.367).
4. Forgetting that GMI and DEPI put the prior year in the numerator, so an index above one means deterioration, and forgetting the negative coefficients on SGAI and LEVI (V3 p.304, p.305).
5. Claiming a quantitative model proves cause and effect; it establishes associations only, and its power declines as managers learn it (V3 p.307).
6. Reversing the persistence result: the coefficient on cash flow exceeds the coefficient on accruals, so a bigger accruals share means faster mean reversion, not slower (V3 p.311, p.316, p.366).
7. Adjusting core earnings by subtracting non-recurring expenses or adding recurring ones; add back only the non-recurring expenses (V3 p.366).
8. Forgetting the tax effect, or applying the tax rate instead of one minus the tax rate, when converting a pre-tax misstatement to net income (V3 p.366).
9. Saying reclassifying receivables to long-term or selling receivables lowers turnover or raises the current ratio; DSO falls, turnover rises, the current ratio falls (V3 p.292, p.320, p.368).
10. Assigning an unrecognised inventory impairment to completeness or clear presentation; it is unbiased measurement, and completeness is for off-balance-sheet items (V3 p.340, p.341, p.367).
11. Saying return on sales is unaffected by an unconsolidated equity-method investee; income includes the profit share but sales exclude the investee's revenue, so the reported margin is overstated (V3 p.340, p.367).
12. Believing overstated revenue overstates inventory; it overstates receivables and net income and understates inventory when goods will be returned (V3 p.336, p.367).
13. Treating a classification shift as changing total cash flow; it only moves cash between sections, and comparing successive annual reports exposes it (V3 p.337, p.339).
14. Relying on the audit opinion for timely risk information; auditor changes, NT filings, and CFO resignations are the timely signals (V3 p.344, p.347, p.354, p.355).
15. Copying the curriculum's rounded Beneish total ($-1.231$) as if it were exact; recompute the products, since the exam gives the coefficients and expects your own arithmetic (V3 p.305).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "03-05" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
