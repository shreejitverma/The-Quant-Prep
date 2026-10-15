---
type: cfa-lm
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
volume: 5
lm: 1
title: "Equity Valuation: Applications and Processes"
pages: "3-47"
weight_band: "10-15%"
difficulty: 2
los_count: 8
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/equity-valuation]
---

# LM1: Equity Valuation: Applications and Processes

Difficulty 2 of 5: almost no arithmetic, but eight definitional LOS whose distinctions (intrinsic versus estimated intrinsic value, going-concern versus liquidation, fair market versus investment value, absolute versus relative, top-down versus bottom-up) are exactly the kind of near-synonym pairs that item sets exploit, and it supplies the model-selection logic every later Equity module assumes.

## LOS map

- **define** valuation and intrinsic value and explain sources of perceived mispricing (V5 p.3) ^los-05-01-a
    - Examiner asks: given a director's statement about alpha, identify which term of $V_E - P = (V - P) + (V_E - V)$ is the true mispricing the manager hopes to capture and which is estimation error, or explain the Grossman-Stiglitz argument for why prices and intrinsic values can differ.
- **explain** the going concern assumption and contrast a going concern value to a liquidation value (V5 p.3) ^los-05-01-b
    - Examiner asks: which value concept a distressed-securities analyst uses that a core equity analyst ignores, or why a persistently unprofitable firm can be worth more dead than alive, or what an orderly liquidation value adds.
- **describe** definitions of value and justify which definition of value is most relevant to public company valuation (V5 p.3) ^los-05-01-c
    - Examiner asks: match fair market value, fair value, investment value, going-concern value and intrinsic value to a context (buy-sell agreement, impairment test, synergistic acquirer, public stock selection) and state which is the focus for listed equities.
- **describe** applications of equity valuation (V5 p.3) ^los-05-01-d
    - Examiner asks: which application is described by a statement about comparing market-implied expectations with the analyst's own (inferring market expectations), or by a merger opinion (fairness opinion), or by a restricted stock grant (share-based payment).
- **describe** questions that should be addressed in conducting an industry and competitive analysis (V5 p.3) ^los-05-01-e
    - Examiner asks: from a list of industry characteristics (entry barriers, rivalry, substitutes, supplier count, buyer count) pick the one that raises or lowers industry profitability under Porter's five forces, or name the three generic strategies, or identify the quality of earnings warning sign in a described accounting choice.
- **contrast** absolute and relative valuation models and describe examples of each type of model (V5 p.3) ^los-05-01-f
    - Examiner asks: classify a described model (ten-year FCF discounted plus terminal value, P/E versus peer median, asset-based) as absolute or relative, and explain why two relative valuations with different benchmarks can both be right.
- **describe** sum-of-the-parts valuation and conglomerate discounts (V5 p.3) ^los-05-01-g
    - Examiner asks: identify the company whose characteristics call for sum-of-the-parts (unrelated segments with different growth), or pick the explanation of the conglomerate discount from internal capital market inefficiency, endogenous factors and measurement error.
- **explain** broad criteria for choosing an appropriate approach for valuing a given company (V5 p.3) ^los-05-01-h
    - Examiner asks: for a company with negative earnings, no dividend and a plausible acquirer, choose free cash flow over DDM and P/E, and name the three criteria (company characteristics, data availability and quality, purpose and perspective of the valuation).

## Core intuition

Every valuation question reduces to one comparison: what is the asset worth, and what does the market charge for it?
Valuation is the estimation of an asset's value from variables related to future investment returns, from comparisons with similar assets, or, when relevant, from estimates of immediate liquidation proceeds (V5 p.4).
Those three sources map directly onto the three families the module introduces: present value models, relative valuation, and asset-based or liquidation valuation.
The intrinsic value of an asset is its value given a hypothetically complete understanding of its investment characteristics (V5 p.4).
Nobody has that understanding, so every analyst works with an estimate, and the entire logic of active management rests on the assumption that the market price can differ from intrinsic value (V5 p.4).

Why should price and value ever diverge?
The Grossman-Stiglitz paradox is the theoretical anchor (V5 p.5).
If prices perfectly reflected intrinsic value, no rational investor would pay to gather and analyse information, because the free price already contains everything.
But if nobody analyses, nothing pushes the price toward value in the first place.
The rational efficient markets formulation resolves this by saying investors gather information only when they expect higher gross returns than the free alternative of accepting the market price (V5 p.5).
Two further features widen the gap for common stock: intrinsic value is genuinely hard to determine, and trading costs exist, so price can wander further from value than it could for a Treasury bill (V5 p.5).
Analysts therefore treat prices with both respect and skepticism, and they recognise that neglected stocks and heavily followed stocks sit in different tiers of efficiency (V5 p.5).

> [!abstract] Idea 1: perceived mispricing has two sources, and only one of them earns alpha
> The manager sees $V_E - P$, the gap between the estimate and the price.
> By adding and subtracting the unobservable $V$, that gap is $(V - P) + (V_E - V)$.
> The first term is true mispricing, the thing that produces an abnormal return; the second term is the analyst's estimation error, which produces nothing but false confidence (V5 p.5).
> Good forecasts plus an appropriate model shrink the second term; a catalyst is what makes the first term pay out inside the investment horizon (V5 p.6).

The corollary the exam likes is that active selection requires expectations that differ from consensus and are, on average, correct (V5 p.6).
Being different is not enough, and being right about what everyone already knows is not enough either.
Even when both conditions hold, convergence of price to value may not happen within the investor's horizon, so many active investors also look for a catalyst, a market or corporate event that forces a re-evaluation (V5 p.6).
The Cornell study of Intel is the module's illustration: a press release about one quarter's revenue growth cut the stock from $61.50 to $43.31, roughly 30%, and a free cash flow model showed the pre-announcement price required 20% growth for ten years while the post-announcement price required well under 15% (V5 p.9).
Either the market overreacted, or the stock had been overvalued and the release was a catalyst; the way to adjudicate is to compare the implied 20% with the company's own history and industry forecasts, which is exactly the application called inferring market expectations (V5 p.9, p.10).

### Which value are we talking about?

The context of a valuation determines which definition of value applies, and the definition in turn shapes the approach (V5 p.4).
A going-concern assumption says the company keeps producing, uses its assets in a value-maximizing way and accesses its optimal financing for a relevant economic time frame; going-concern value is the value under that assumption and is the focus of the whole Equity topic (V5 p.6).
Liquidation value is what the company fetches if dissolved and its assets sold individually (V5 p.6).
Assets working together, plus human capital managing them, usually make going-concern value exceed liquidation value, but a persistently unprofitable business can be worth more dead than alive, which is why a distressed-securities analyst cares about liquidation value while a core equity analyst can ignore it (V5 p.6, p.47).
Liquidation value itself depends on the time available: nonperishable inventory dumped immediately fetches less than inventory sold over a longer period, hence the separate notion of orderly liquidation value (V5 p.6).

Fair market value is the price at which an asset would change hands between a willing buyer and a willing seller, neither under compulsion, both informed of all material facts; it dominates tax contexts and buy-sell agreements among private owners because the goal there is equitable treatment (V5 p.6).
Fair value is the related but not identical financial-reporting concept, defined by accounting standards for purposes such as impairment testing (V5 p.7).
Investment value is value to a specific buyer taking account of synergies and that buyer's requirements, and it is the number an acquirer with operating synergies actually pays attention to (V5 p.7).
For public equities, intrinsic value under a going-concern assumption is the relevant definition, and market prices should tend toward fair market value in the long run when the market trusts management to act for owners (V5 p.7).

> [!abstract] Idea 2: the definition of value is chosen by the purpose, not by the analyst's taste
> Public stock selection wants intrinsic going-concern value.
> A buy-sell agreement or an estate tax return wants fair market value.
> An impairment test wants the accounting standard's fair value.
> A synergistic acquirer wants investment value.
> A distressed fund wants liquidation value as a floor (V5 p.6, p.7).

### Who uses valuation, and for what

Stock selection is the primary use: is this security fairly priced, overpriced or underpriced relative to its estimated intrinsic value and relative to comparable securities (V5 p.7)?
Inferring market expectations reverses the model: hold every fundamental fixed except one, and solve for the value of that fundamental that sets model value equal to the market price (V5 p.7, p.8).
The implied expectation can be tested for reasonableness or used as a benchmark for another company (V5 p.7).
Corporate events (mergers, acquisitions, divestitures, spin-offs, going-private deals) change future cash flows and therefore equity value, and when an acquirer pays in its own stock, investors need to know whether that currency is fairly valued (V5 p.8).
Fairness opinions are third-party judgments on merger terms, usually from an investment bank, and are valuation exercises at their core (V5 p.8).
Evaluating business strategies, communicating with analysts and shareholders, appraising private businesses for transactions and tax, and valuing share-based compensation complete the list (V5 p.8).
The private business case matters because the absence of a market price changes the character of the valuation even though the models are shared, which is the bridge to [[LM06-Private-Company-Valuation]] and to IPO analysis (V5 p.8).

### The five-step process

The valuation process is understanding the business, forecasting performance, selecting the model, converting forecasts to a valuation, and applying the conclusions (V5 p.10).
Each step feeds the next: industry and competitive analysis plus financial statement analysis give the forecasts, the forecasts feed the model, the model output is adjusted by judgment, and the result becomes a recommendation, a transaction opinion or a strategic assessment (V5 p.10).
Understanding the business means understanding the economic and industry context, the company's strategy and its past performance (V5 p.10).
Frameworks such as Porter's five forces are not ends in themselves; their job is to make sure the analysis attends to the most important economic drivers and to flag which aspects deserve sensitivity analysis (V5 p.11).
The three questions to answer are: how attractive is the industry for sustained profitability, what is the company's competitive position and strategy, and how well has it executed and what are its prospects for future execution (V5 p.11, p.12).

Industry profitability rises when rivalry is low (few competitors, strong brand identification), entry costs are high, substitutes are few or switching costs are high, suppliers are many, and buyers are many (V5 p.11).
The practice set drills this in reverse: few barriers, high rivalry and low substitution costs all hurt men's clothing retail profitability, while a large number of wholesale suppliers helps it (V5 p.41, p.47).
Competitive position is read from the level and trend of market share, and Porter's generic strategies are cost leadership, differentiation and focus (cost focus or differentiation focus) (V5 p.11, p.12).
A business model describes how the company makes money: which customers, which products, how delivered and how financed; a low-cost carrier is the business model of an airline pursuing cost leadership (V5 p.12).
Execution is assessed from financial reports, but the module insists on two caveats: qualitative factors (ownership structure, intellectual and physical property, terms of licenses and franchises, contingent liabilities) matter, and past results must not simply be extrapolated because economic forces produce regression toward the mean (V5 p.12).
Successful companies draw competitors, poor performers get restructured, and long-horizon forecasts beyond about ten years should plausibly converge to the economy's average growth (V5 p.12).

### Information and the quality of what it reports

Sources include regulatory filings (10-K and 20-F annual, 10-Q and 6-K interim in the US), press releases, investor relations materials, conference calls and transcripts, and third parties such as industry bodies and commercial intelligence vendors (V5 p.15).
Regulation FD and the Code and Standards prohibit selective disclosure and use of material nonpublic information, which clarifies rather than obstructs the analyst's role (V5 p.15).
ESG information adds sustainability reports, regulator databases and not-for-profit standard setters (V5 p.16).

Quality of earnings analysis scrutinises all the statements to judge both the sustainability of performance and how accurately reported figures reflect economic reality (V5 p.17).
Nonrecurring items such as litigation settlements, temporary tax reductions and gains on nonoperating assets are lower quality than core earnings (V5 p.17).
The systematic tool is to split net income into a cash component (operating plus investing cash flow) and an accrual component; Sloan (1996) showed the cash component is more persistent, so high accruals predict lower future ROA and signal lower earnings quality (V5 p.17).
Exhibit 3 catalogues the warning signs by category: early revenue recognition and nonoperating gains classified as operating; over- or under-reserving, deferring expenses by capitalising them, and aggressive estimates such as long depreciable lives and high pension return assumptions; off-balance-sheet financing; and bank overdrafts characterised as operating cash flow (V5 p.18).
The three case examples make these concrete: Buffett on pension return assumptions, Tangoe's revenue from customers unlikely to pay, and Livent's capitalised preproduction costs (V5 p.19 to p.22).
The general signal is an asset account growing much faster than sales (V5 p.22).
Beyond aggressive accounting lies fraud, and the auditing standards' fraud risk indicators (pressure to hit targets, compensation tied to price, covenant pressure, related-party transactions, complex structures, turnover of management or auditors, prior violations) are a ready checklist (V5 p.22).

### Forecasting and choosing the model

Forecasting can be top-down (macro to industry to company, for example industry unit sales from GDP times market share) or bottom-up (micro to aggregate, for example sales per square metre of existing stores applied to new stores) (V5 p.23).
Qualitative judgments about management integrity and accounting transparency legitimately modify the numbers (V5 p.23).

> [!abstract] Idea 3: absolute models produce a number to compare with price; relative models produce a ranking against a benchmark that is itself assumed fairly priced
> Absolute models specify intrinsic value: present value models (dividend discount, free cash flow to equity, free cash flow to the firm, residual income) and asset-based valuation (V5 p.23 to p.25).
> Relative models say an asset is cheap or dear relative to another asset or group, using price or enterprise multiples; the method of comparables cannot deliver intrinsic value unless the comparison asset is fairly valued (V5 p.25, p.26).
> Two relative valuations with different benchmarks can both be right, and "undervalued" must be kept distinct from "relatively undervalued" (V5 p.25, p.26).

Present value models are harder for stock than for bonds because the cash flow stream must be defined and forecast rather than read from an indenture, extends forever, and is discounted at a subjective rate; control value and unused assets add further issues, which is why Graham and Dodd recommended a range of intrinsic values and why sensitivity analysis is essential (V5 p.24, p.25).
Asset-based valuation suits natural resource companies (proven reserves less extraction costs, board feet of timber), and mixed companies can be valued as the sum of divisions with the resource division valued on its reserves (V5 p.25).
Relative value investing is the aggressive form of relative valuation, with pairs trading (buy the relatively undervalued, short the relatively overvalued) as the classic example, and it profits whichever way the overall market moves so long as the spread closes (V5 p.25, p.26).

Sum-of-the-parts valuation values each business as an independent going concern and adds them, producing what is also called breakup value or private market value; it fits companies with segments in different industries with different valuation characteristics and is used to size the value unlocked by spin-offs, split-offs, tracking stock and carve-outs (V5 p.27).
The conglomerate discount is the market's tendency to price a multi-business company below narrower peers, explained by inefficient internal capital markets, endogenous factors (poor performers diversify by acquisition) or measurement error (the discount may not exist) (V5 p.29).
A breakup value above the unadjusted going-concern value can prompt divestiture or spin-off (V5 p.29).

The three model-selection criteria are consistency with the company's characteristics, appropriateness given data availability and quality, and consistency with the purpose and the analyst's perspective (V5 p.29).
A bank's largely marketable assets make asset-based relative valuation more relevant; a company with no dividend history pushes the analyst to a more complex present value model; volatile or negative earnings make P/E useless; an investor seeking control values free cash flow because it can redirect those flows (V5 p.29).
Practitioners use many models at once, about 17 valuation factors on average in the Merrill Lynch survey, combining rankings into composites (V5 p.29, p.30).

Converting forecasts to value adds sensitivity analysis and situational adjustments: a control premium for a stake that delivers control of the board and the options to redeploy assets or change capital structure, a lack of marketability discount for non-traded stock, an illiquidity discount for thinly traded stock, and a blockage factor when the block is large relative to volume without conferring control (V5 p.30).
Finally, analysts are sell-side, buy-side, corporate or independent, and they serve clients, capital markets and suppliers of capital by making better buy and sell decisions possible, moving prices toward value, and monitoring management (V5 p.31).
The research report must carry timely information, clear language, objectivity with key assumptions identified, a fact-opinion distinction, internally consistent analysis and recommendation, enough information to critique the valuation, key risks, and conflict disclosures (V5 p.33, p.34).
A target price needs its basis, a time frame and a statement of uncertainty, and a good company is not automatically a good investment because return depends on the price paid (V5 p.33, p.34).
Standards I(B), I(C), V(A), V(B) and V(C) govern the report, which is the link to [[LM02-Guidance-for-Standards-I-VII]] (V5 p.37).

## Formulas and derivations

**Perceived mispricing decomposition** (V5 p.5)
$$
V_E - P = (V - P) + (V_E - V)
$$
^f-05-01-1

- $V_E$: the analyst's estimated intrinsic value; $P$: observed market price; $V$: true but unobservable intrinsic value; all in currency per share.
- $(V - P)$ is true mispricing, the term that contributes to abnormal return (alpha); $(V_E - V)$ is estimation error and contributes nothing to return.
- Derivation: $V_E - P = V_E - P + V - V$, then regroup as $(V - P) + (V_E - V)$; the identity holds for any $V$, which is the point, because $V$ can be inserted even though it is never observed (V5 p.5).
- Illustration: $V_E = 50$, $P = 45$, true $V = 48$ gives a perceived gap of 5 of which only $48 - 45 = 3$ is real and $50 - 48 = 2$ is error (Python: `48-45 = 3`, `50-48 = 2`).

**Implied price appreciation to a target price** (V5 p.35)
$$
\text{Upside} = \frac{\text{Target price}}{P} - 1
$$
^f-05-01-2

- Target price is the estimated intrinsic value stated in the report; $P$ is the current market price.
- Passage B in Exhibit 5: $3.08 / 2.25 - 1 = 0.369$, the "36.8%" the report states (V5 p.34, p.35).
- A report should also give the basis for the target, a time frame and the uncertainty of reaching it (V5 p.33).

> [!tip] Calculator
> `3.08 ÷ 2.25 =` gives 1.3689; `- 1 =` gives 0.3689, so 36.9% upside.

**Sum-of-the-parts (breakup) value** (V5 p.27, p.28)
$$
V_{\text{SOTP}} = \sum_{i=1}^{n} V_i \;+\; \text{Corporate adjustments}, \qquad V_{\text{equity}} = V_{\text{SOTP}} - \text{Net debt}
$$
^f-05-01-3

- $V_i$: value of segment $i$ as an independent going concern, each from its own forecasts and possibly its own model or multiple; corporate adjustments cover unallocated overhead, taxes and assets or liabilities not attributable to any segment (V5 p.28).
- Also called breakup value or private market value (V5 p.27).
- Reason: segments in different industries have different growth, risk and appropriate multiples, so one blended multiple or one discount rate misprices the mix (V5 p.27).

**Conglomerate discount** (V5 p.29)
$$
\text{Conglomerate discount} = \frac{V_{\text{SOTP}} - \text{Market value}}{V_{\text{SOTP}}}
$$
^f-05-01-4

- The curriculum defines the concept verbally (the market applies a discount to a multi-business company relative to narrower peers); this ratio is the operational form in which a vignette will state it (V5 p.29).
- Three explanations: internal capital market inefficiency, endogenous factors (poor performers diversify), and measurement error (the discount may be an artefact) (V5 p.29).
- A positive discount means breakup value exceeds going-concern market value, which can prompt divestiture or spin-off (V5 p.29).

**Top-down revenue forecast** (V5 p.23)
$$
\text{Company units} = \text{Industry units} \times \text{Market share}, \qquad \text{Revenue} = \text{Company units} \times \text{Price}
$$
^f-05-01-5

- Industry units come from a macro forecast such as GDP; market share is the company's forecast share (V5 p.23).
- Practice Problem 11: a restaurant chain forecasting sales as market share times industry sales and a utility scaling with GDP are top-down (V5 p.44, p.48).

**Bottom-up revenue forecast** (V5 p.23)
$$
\text{Revenue} = \sum_{\text{stores}} \left(\text{Sales per square metre} \times \text{Square metres}\right)
$$
^f-05-01-6

- Micro-level productivity of existing units is applied to new units and aggregated; forecasts for individual companies can then be aggregated into industry forecasts (V5 p.23).
- Practice Problem 11: new stores assumed to match existing stores' sales per square metre is bottom-up (V5 p.44, p.48).

**Cash and accrual components of net income** (V5 p.17)
$$
\text{Accruals} = NI - \left(CFO + CFI\right)
$$
^f-05-01-7

- $NI$: net income; $CFO$: operating cash flow; $CFI$: investing cash flow; the cash component is their sum.
- Sloan (1996): the cash component is more persistent, so a higher accrual share predicts lower future ROA and indicates lower earnings quality (V5 p.17).
- Extreme case: a company with revenue and income but zero operating cash flow because it never collects receivables has net income entirely in accruals (V5 p.17).

**Receivables turnover and days receivable as an early warning** (V5 p.20)
$$
\text{AR turnover} = \frac{\text{Revenue}}{\text{Average receivables}}, \qquad \text{Days receivable} = \frac{365}{\text{AR turnover}}
$$
^f-05-01-8

- Recognising revenue from customers unlikely to pay and under-reserving for bad debts inflate receivables faster than revenue, so turnover falls and days rise (V5 p.20).
- Tangoe: $188{,}914 / 40{,}701 = 4.6$ falling to $212{,}476 / 50{,}110 = 4.2$; days $365 / 4.6 = 79$ rising to $365 / 4.2 = 87$ (V5 p.20).

> [!tip] Calculator
> `212476 ÷ 50110 =` gives 4.24; `365 ÷ 4.24 =` gives 86.1 days (the curriculum rounds turnover to 4.2 first and gets 87).

**Blended pension return assumption** (V5 p.19)
$$
r_{\text{plan}} = w_{\text{bonds}}\, r_{\text{bonds}} + (1 - w_{\text{bonds}})\, r_{\text{equity}} \;\Rightarrow\; r_{\text{equity}} = \frac{r_{\text{plan}} - w_{\text{bonds}}\, r_{\text{bonds}}}{1 - w_{\text{bonds}}}
$$
^f-05-01-9

- Buffett's illustration: 28% in cash and bonds at 5% and an 8% overall assumption implies $(0.08 - 0.28 \times 0.05) / 0.72 = 0.0917$, so equities must earn 9.2% after fees (V5 p.19).
- Expected return on plan assets is a deduction in pension expense, so an aggressive assumption understates expense and overstates net income (V5 p.19).

> [!tip] Calculator
> `0.28 × 0.05 =` gives 0.014; `0.08 - 0.014 =` gives 0.066; `÷ 0.72 =` gives 0.0917.

**Debt coverage with and without adding back capitalised-cost amortisation** (V5 p.21, p.22)
$$
\frac{\text{Debt}}{\text{EBITDA}_{\text{reported}}} \;\text{versus}\; \frac{\text{Debt}}{\text{EBITDA}_{\text{reported}} - \text{Amortisation of capitalised operating costs}}
$$
^f-05-01-10

- When operating outlays (Livent's preproduction costs) are capitalised, their amortisation is not a true non-cash item and should not be added back, because the cash left the company (V5 p.21).
- Livent 1996: reported debt/EBITDA 1.7 versus 5.5 without the add-back; 1997: 3.7 on EBITDA of $58.3 million versus a negative $52.6 million without the add-back, implying debt of about $215.7 million and an add-back of $110.9 million (Python: `3.7*58.3 = 215.71`, `58.3+52.6 = 110.9`) (V5 p.22).

| Criterion | Question to ask | Example from the module |
|---|---|---|
| Company characteristics | What assets create value, and how are cash flows distributed? | Bank with marketable assets favours asset-based relative valuation; controlling investor favours free cash flow (V5 p.29) |
| Data availability and quality | Are the model's inputs observable and reliable? | No dividend history weakens DDM; negative or volatile earnings weaken P/E (V5 p.29) |
| Purpose and perspective | Whose decision, and what bias might the writer carry? | Acquirer redirecting cash flows; reader of others' reports checks the author's perspective (V5 p.29) |

| Porter force | Industry is more profitable when | Men's clothing retail (Practice Problems) |
|---|---|---|
| Intra-industry rivalry | Rivalry is low, few competitors, strong brand identification | High rivalry: negative (V5 p.41) |
| Threat of new entrants | Entry costs and other barriers are high | Few barriers: negative (V5 p.41) |
| Threat of substitutes | Few substitutes, or high switching cost | Low substitution cost: negative (V5 p.41) |
| Bargaining power of suppliers | Many suppliers exist | Many wholesale suppliers: positive (V5 p.47) |
| Bargaining power of buyers | Many customers exist | Not stated in the vignette |

## Worked examples

### Example 1: Cornell's Intel study and inferring market expectations (V5 p.8, p.9, p.10)

Setup: on 21 September 2000 Intel warned that third-quarter revenue growth would fall 2 to 4 points short of its own guidance and 3 to 7 points short of analysts'; the stock fell from $61.50 to $43.31 in five days.
Cornell valued Intel as the present value of expected free cash flow with a conservatively low discount rate.

Step 1, size the move: $43.31 / 61.50 - 1 = -0.296$, a drop of $18.19 (Python: `43.31/61.50-1 = -0.2958`).
Step 2, reverse-engineer growth: the $61.50 price was consistent with 20% growth for ten years then 6% forever; $43.31 was consistent with a ten-year rate well under 15%; by 2009 the lower path implied revenue $50 billion below the higher path (V5 p.9).
Step 3, adjudicate: the release cited a cyclical slowdown in Europe, nothing about long-run fundamentals, so either the market overreacted or the stock was overvalued and the release was a catalyst (V5 p.9).
Knowledge check answer: compare the implied 20% with Intel's own recent growth, the industry's growth and economy forecasts; Cornell found 20% far above Intel's five-year average, achieved when the company was much smaller, and concluded the stock had been overvalued (V5 p.9, p.10).
This is the application "inferring market expectations": fix every input but growth, solve for the growth that equates model value to price, then judge it (V5 p.7, p.8).
The Apple (about 10% on lowered guidance) and Biogen (about 30% on a failed trial) moves in 2019 pose the same question (V5 p.8). ^ex-05-01-1

### Example 2: Oilfield services competitive analysis (V5 p.13, p.14)

Setup: six providers with fiscal 2018 revenue and net income (billions): Schlumberger 32.8 and 2.2, Halliburton 24.0 and 1.7, Baker Hughes 22.9 and 0.3, Saipem (2017) EUR 9.0 and -0.3, National Oilwell Varco 8.5 and -0.02, Weatherford 5.7 and -2.8.

Part 1, demand drivers: these companies sell to oil and gas producers, so exploration and production activity drives demand, and that activity is driven by crude oil and natural gas prices.
The framework is supply and demand for each commodity: gas inventories and gas-fired generation; OPEC capacity, production levels and new discoveries; household, commercial and power-generation oil use; economic growth on the demand side and depletion rates on the supply side (V5 p.14).
Revenue forecasting therefore runs top-down from commodity prices to activity to service demand.

Part 2, cost leadership: profit margin reflects cost structure, so a successfully executed cost leadership strategy shows up as a higher margin, and a cost leader should also show high revenue per employee (V5 p.14).
Computed margins: Schlumberger $2.2 / 32.8 = 6.7\%$, Halliburton $1.7 / 24.0 = 7.1\%$, Baker Hughes $0.3 / 22.9 = 1.3\%$, the rest negative (Python: `2.2/32.8 = 0.0671`, `1.7/24.0 = 0.0708`, `0.3/22.9 = 0.0131`).
The caveat is that margin also reflects pricing power, so a high margin could be differentiation rather than cost leadership; the level and trend must be read together with revenue per employee (V5 p.14).
For newer companies non-financial measures (clinical trial results, unique visitors) may be the critical revenue indicators (V5 p.14). ^ex-05-01-2

### Example 3: Buffett on pension return assumptions (V5 p.19)

Setup: the 363 S&P companies with pension plans assumed an average 8% return in 2006; cash and bonds averaged 28% of assets and Buffett assumes they earn 5%.

Implied equity return (Formula 9): $(0.08 - 0.28 \times 0.05) / 0.72 = (0.08 - 0.014) / 0.72 = 0.0917$, the 9.2% after fees that the curriculum states (Python: `(0.08-0.28*0.05)/0.72 = 0.09167`).
Buffett's reality check: for the Dow to deliver even the 20th century's 5.3% compound return through 2099 it would need to reach about 2,000,000 from under 13,000.

Part 1: the expected return on plan assets is a deduction in pension expense, so an aggressive assumption produces a larger-than-warranted deduction, understates pension expense and overstates net income, possibly turning pension expense into pension income (V5 p.19).
Part 2: the assumed return is disclosed in the footnotes to the financial statements (V5 p.19).
Exhibit 3 lists the same item under aggressive estimates together with high discount rates and low compensation growth for pension liabilities (V5 p.18). ^ex-05-01-3

### Example 4: Tangoe and Livent, extreme quality of earnings cases (V5 p.20, p.21, p.22)

Case A, Tangoe: the SEC charged it with recording revenue from customers unlikely to pay and understating the bad-debt allowance.

Part 1, statement impact: inflated revenue and earnings on the income statement, inflated receivables on the balance sheet, and net income exceeding operating cash flow when revenue outruns collections (V5 p.20).
Part 2, early warning (Formula 8): turnover $188{,}914 / 40{,}701 = 4.64$ in 2013 and $212{,}476 / 50{,}110 = 4.24$ in 2014; days $365 / 4.6 = 79$ and $365 / 4.2 = 87$ (Python: `188914/40701 = 4.6415`, `212476/50110 = 4.2402`, `365/4.6 = 79.35`, `365/4.2 = 86.90`).
Revenue grew $212{,}476 / 188{,}914 - 1 = 12.5\%$, which the curriculum rounds to 12%.
Discrepancy: the curriculum says average receivables grew 32%, but $50{,}110 / 40{,}701 - 1 = 23.1\%$ (Python: `50110/40701-1 = 0.2312`); the printed 32% appears to be a transposition of 23%, and the conclusion (receivables growing far faster than sales) is unchanged.
Other violations (a partner loan booked as revenue, contingency fees, prepayments recognised early) understate liabilities such as loans payable and unearned revenue (V5 p.20, p.21).

Case B, Livent: capitalised preproduction costs (advertising, sets, costumes, rehearsal salaries) and amortised them over each show's expected life.
Part 3: EPS was immediately higher because expenses were deferred (V5 p.21).
Part 4: the balance sheet carried an asset that should have been expensed given the uncertainty of theatrical revenue; expense deferral is the warning sign (V5 p.21).
Part 5 (Formula 10): mechanically adding back the amortisation inflates EBITDA and understates debt/EBITDA even though the cash was spent; in 1996 debt/EBITDA was 1.7 reported versus 5.5 without the add-back, and in 1997 reported EBITDA of $58.3 million became negative $52.6 million, implying debt of roughly $3.7 \times 58.3 = 215.7$ million and an add-back of $58.3 + 52.6 = 110.9$ million (Python: `3.7*58.3 = 215.71`, `58.3+52.6 = 110.9`).
Livent filed for bankruptcy in November 1998 (V5 p.22).
General lesson: an asset account growing much faster than sales signals aggressive accounting (V5 p.22). ^ex-05-01-4

### Example 5: Smithson Genomics, two relative valuations (V5 p.26)

Setup: one analyst says Smithson is at least 15% overvalued against the peer median P/E in healthcare information services; another says it is 10% undervalued against the Russell 3000 median P/E.

Both can be right because both are relative statements against different benchmarks.
If the whole healthcare information services industry is undervalued relative to the Russell 3000, Smithson can be dear against its peers and cheap against the market at the same time (V5 p.26).
Investment implications depend on whether the Russell 3000 itself trades near intrinsic value and whether liquidity supports the intended position, so the analyst should supplement relative valuation with an intrinsic value estimate (V5 p.26).
The method of comparables cannot specify intrinsic value without the extra assumption that the comparison asset is fairly valued; its advantages are simplicity, grounding in market prices and the principle that similar assets should sell at similar prices (V5 p.26). ^ex-05-01-5

### Example 6: Donaldson sum-of-the-parts (V5 p.27, p.28)

Setup (USD millions): Engine Products sales 1,849.0 (2018), 1,553.3 (2017), 1,391.3 (2016) with pre-tax earnings 261.3, 219.7, 163.5; Industrial Products sales 885.2, 818.6, 829.0 with pre-tax earnings 137.1, 129.1, 119.0; assets 1,110.3 versus 631.9 in 2018; capex 64.6 versus 31.4.

Margins 2018: Engine $261.3 / 1{,}849.0 = 14.1\%$; Industrial $137.1 / 885.2 = 15.5\%$, matching the curriculum (Python: `261.3/1849.0 = 0.1413`, `137.1/885.2 = 0.1549`).
Margins 2016: Engine $163.5 / 1{,}391.3 = 11.8\%$; Industrial $119.0 / 829.0 = 14.4\%$ (Python: `163.5/1391.3 = 0.1175`, `119.0/829.0 = 0.1435`).
Growth 2016 to 2018: Engine sales $(1{,}849.0 / 1{,}391.3)^{0.5} - 1 = 15.3\%$ a year versus Industrial $(885.2 / 829.0)^{0.5} - 1 = 3.3\%$ (Python: `(1849/1391.3)**0.5-1 = 0.1528`, `(885.2/829)**0.5-1 = 0.0333`).
Engine's share of sales rose from $1{,}391.3 / 2{,}220.3 = 62.7\%$ to $1{,}849.0 / 2{,}734.2 = 67.6\%$ (Python: `1391.3/2220.3 = 0.6266`, `1849/2734.2 = 0.6763`).
Corporate items: segment pre-tax earnings sum to $261.3 + 137.1 = 398.4$ against a company total of 363.6, so unallocated corporate costs are $-34.8$; segment assets sum to 1,742.2 against 1,976.6, leaving 234.4 of corporate assets (Python: `398.4-363.6 = 34.8`, `1976.6-1742.2 = 234.4`).

Part 1, why sum-of-the-parts: the segments differ in size, growth and margin; Engine is larger and growing far faster in sales, income, assets and capex, while Industrial has the higher margin, and management's 2013 target of 48% Industrial by 2021 is moving the wrong way, so whether the mix shifts is fundamental to the share price (V5 p.28).
Part 2, how: value each segment from its own sales and profitability forecasts, sum, and adjust for taxes, overhead and unattributed assets and liabilities (Formula 3) (V5 p.28).
The conglomerate discount discussion follows: if the market prices Donaldson below the sum, the explanations are internal capital misallocation, endogenous diversification or measurement error (V5 p.29). ^ex-05-01-6

### Example 7: Exhibit 5, two research report passages (V5 p.34, p.35)

Setup: Passage A values MXI by segments using "relative acquisition multiples and peer mean values", notes a 0.76 price-to-book and calls the shares "worth holding" with tempered enthusiasm; Passage B values TXI with a dividend discount model at EUR 3.08 against a price of EUR 2.25 and reiterates market outperform.

Passage B's upside (Formula 2): $3.08 / 2.25 - 1 = 0.369$, the "36.8%" stated (Python: `3.08/2.25-1 = 0.3689`).
Passage B gives the model, the inputs (dividend, growth rates, horizons, discount rate) and a clear conclusion, so the reader can critique it; its weakness is asserting the P/E is "low" without saying relative to what (V5 p.35).
Passage A is vague on method, quotes a price-to-book below 1 without a peer comparison, never quantifies the undervaluation, and ends with a feeble hedge that contradicts the top attractiveness rating elsewhere in the report (V5 p.35).
The lesson is the checklist on p.33 and p.34: sufficient information to critique, internal consistency, and a clear fact-opinion distinction. ^ex-05-01-7

## Item-set patterns

> [!warning] Trap 1: which difference is the alpha
> A director says active managers try to capture alpha and that mispricing is not directly observable.
> Correct: the source of abnormal return is $V - P$, true intrinsic value less market price (Practice Problem 1).
> Distractors: $V_E - P$ is what the manager perceives, but it includes estimation error; $V_E - V$ is pure error and is tempting because it is the only term that mentions the analyst's estimate (V5 p.5, p.47).

> [!warning] Trap 2: the value concept matched to the wrong fund
> A distressed fund and a core equity fund are described side by side.
> Correct: the distressed analyst considers liquidation value; the core analyst, focused on multi-year free cash flow, uses going-concern value (Practice Problems 2 and 3).
> Distractors: fair value and fair market value sound relevant to everyone and are chosen by candidates who forget that they are transaction and reporting concepts; investment value is chosen because it sounds like what an investor wants (V5 p.6, p.7, p.47).

> [!warning] Trap 3: naming the application
> A statement says analysts compare the expectations implied by the market price with their own.
> Correct: inferring or extracting market expectations (Practice Problem 4).
> Distractors: valuing private businesses and rendering fairness opinions are real applications and are tempting because the question stem says "use valuation concepts and models to"; only the implied-expectations wording matches the statement (V5 p.7, p.47).

> [!warning] Trap 4: Porter's forces with the sign reversed
> The vignette lists few entry barriers, high rivalry, low substitution costs and many suppliers, then asks which raises profitability.
> Correct: many suppliers, because supplier competition limits input price increases (Practice Problem 5).
> Distractors: entry costs and substitution costs are the right forces but the wrong direction, since low entry costs and low switching costs hurt profitability; candidates pick them because the force is named in the answer (V5 p.11, p.47).

> [!warning] Trap 5: nonrecurring items and the direction of bias
> A company's release includes a favourable settlement, a one-time tax credit and a gain on a nonoperating asset.
> Correct: reported earnings are biased upward relative to sustainable earnings (Practice Problem 6).
> Distractors: "unbiased" tempts candidates who reason that the items are disclosed; "downward" tempts those who think of conservative accounting; the only question is whether the items will recur (V5 p.17, p.47).

> [!warning] Trap 6: classifying the model
> An analyst discounts ten years of free cash flow plus a terminal value.
> Correct: absolute valuation, because the output is an intrinsic value (Practice Problem 7).
> Distractors: relative value is chosen because several retailers are compared; sum-of-the-parts is chosen because the firms are in the same industry; neither describes the model actually used (V5 p.23, p.47).

> [!warning] Trap 7: choosing the model for a no-earnings, no-dividend growth company
> VEGA is unprofitable for years, will not pay a dividend, and may attract acquirers.
> Correct: free cash flow, because it survives missing dividends and negative earnings and suits a control perspective (Practice Problem 8).
> Distractors: DDM fails on data availability; P/E fails on negative earnings; both are tempting because they are the simplest models (V5 p.29, p.47).

> [!warning] Trap 8: pairs trading arithmetic
> Three stocks are labelled 15% overvalued, 10% overvalued and 15% undervalued.
> Correct: buy the undervalued stock and short an overvalued one in the same industry (Practice Problem 12).
> Distractors: shorting both overvalued names is not a pair; buying an overvalued name is backwards; candidates also assume the most overvalued stock must be the short leg, but the stem's options only offer the 10% name (V5 p.25, p.26, p.48).

> [!warning] Trap 9: the situational adjustment for a 70% stake
> An acquirer buys 70% of a listed company in an all-stock deal.
> Correct: control premium, because more than 50% confers control (Practice Problem 15).
> Distractors: blockage factor applies to a large block that does not confer control; lack of marketability discount applies to non-traded shares, and the target is actively traded (V5 p.30, p.48).

> [!warning] Trap 10: top-down policy versus bottom-up diligence
> An analyst describes reading filings, joining calls and studying industry dynamics, and her firm's policy is top-down.
> Correct: she omitted general economic conditions, the macro layer that starts a top-down process (Practice Problem 16).
> Distractors: more micro inputs is bottom-up and moves away from policy; more probing questions on public calls is what the Bowman testimony says analysts avoid, and is unrelated to top-down (V5 p.23, p.32, p.48).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM01-Equity-Valuation-Applications-and-Processes-Practice-Problems]]

## Cross-links

- [[LM02-Discounted-Dividend-Valuation]]: the first absolute model; this module's definitions of intrinsic value, going-concern value and the data availability criterion (a company must have a dividend history or a forecastable policy) decide when a DDM is the right tool.
- [[LM03-Free-Cash-Flow-Valuation]]: the company-level cash flow definitions (FCFF, FCFE) introduced here as alternatives to dividends, and the control perspective that makes free cash flow the model for acquirers, are developed in full there.
- [[LM04-Market-Based-Valuation-Price-and-Enterprise-Value-Multiples]]: the method of comparables and the "relatively undervalued versus undervalued" distinction from this module become the P/E, P/B, EV/EBITDA and benchmark-selection mechanics there.
- [[LM05-Residual-Income-Valuation]]: residual income is the third company-level cash flow definition named here (accounting earnings above the cost of generating them) and depends on the quality of earnings judgments this module introduces.
- [[LM06-Private-Company-Valuation]]: fair market value, investment value, control premiums, lack of marketability discounts and the appraisal application of valuation are defined here and quantified there.
- [[LM05-Evaluating-Quality-of-Financial-Reports]]: Exhibit 3's earnings quality indicators, the accrual decomposition and the Tangoe and Livent cases are the same warning signs that module turns into the Beneish model and other formal tests.
- [[LM02-Guidance-for-Standards-I-VII]]: Exhibit 7 lists Standards I(B), I(C), V(A), V(B) and V(C) as the conduct rules for research reports; the ethics module supplies the detailed guidance and cases.

## Self-test

Vignette A for Q1 to Q3: Ines Karlsen, a buy-side analyst, estimates the intrinsic value of Norrland AB at SEK 180 against a market price of SEK 150.
Her director says: "Even if your model and forecasts are perfect, we may not earn the 20% you imply, because our fund reviews positions every 12 months."
A colleague using the same model but a higher discount rate estimates SEK 165.
Karlsen's report also states that Norrland, a loss-making shipyard, would fetch SEK 120 per share if its docks and land were sold individually and SEK 135 if sold over two years.

> [!question] Q1
> If the true intrinsic value of Norrland is SEK 170, the component of Karlsen's perceived mispricing that contributes to alpha is closest to:
> A. SEK 10.
> B. SEK 20.
> C. SEK 30.

> [!question] Q2
> The director's comment is best described as a concern about:
> A. estimation error in $V_E$.
> B. the absence of a catalyst within the investment horizon.
> C. the Grossman-Stiglitz paradox.

> [!question] Q3
> The SEK 120 and SEK 135 figures are, respectively, best described as:
> A. liquidation value and orderly liquidation value.
> B. going-concern value and liquidation value.
> C. fair market value and investment value.

Vignette B for Q4 to Q6: Prakash Mehta covers Halden Foods, whose 2025 net income is 240, operating cash flow 150 and investing cash flow -40 (all in millions).
Revenue rose 15% from 900 to 1,035 while average receivables rose 38% from 150 to 207.
Halden's pension footnote shows an 8.0% expected return on plan assets with 30% of assets in bonds yielding 4%.
Halden capitalises customer acquisition costs and amortises them over five years.

> [!question] Q4
> Halden's accrual component of net income and its days receivable in 2025 are closest to:
> A. 90 and 61 days.
> B. 130 and 61 days.
> C. 130 and 73 days.

> [!question] Q5
> The equity return implied by Halden's pension assumption is closest to:
> A. 8.0%.
> B. 9.0%.
> C. 9.7%.

> [!question] Q6
> Compared with expensing customer acquisition costs as incurred, Halden's policy most likely:
> A. raises current earnings and overstates debt/EBITDA if amortisation is added back.
> B. raises current earnings and understates debt/EBITDA if amortisation is added back.
> C. lowers current earnings and has no effect on EBITDA.

Vignette C for Q7 to Q8: Orsa Holdings has three segments valued independently at 1,200 (packaging, on an EV/EBITDA multiple), 800 (specialty chemicals, on a DCF) and 400 (a listed 40% stake in a logistics firm, at market).
Unallocated corporate costs have a capitalised value of -150, net debt is 600 and there are 100 million shares.
Orsa trades at 13.50 per share.
An activist argues the market applies a conglomerate discount that a spin-off would remove.

> [!question] Q7
> Orsa's sum-of-the-parts equity value per share and the implied conglomerate discount are closest to:
> A. 16.50 and 18%.
> B. 16.50 and 22%.
> C. 18.00 and 25%.

> [!question] Q8
> Which explanation of the conglomerate discount would, if true, imply that the activist's spin-off will not unlock value?
> A. Inefficient internal capital markets.
> B. Endogenous factors.
> C. Research measurement errors.

Vignette D for Q9 to Q10: Lena Voss must choose models for two companies.
Tessaro Bank holds mostly marketable securities and loans; Quillon Biotech has negative earnings, no dividend, one drug in phase III trials, and is the subject of takeover speculation.
Voss's firm publishes a target price of 42 on Quillon against a price of 30, states the DCF inputs, and includes the sentence "Quillon is an excellent company and therefore an excellent investment."

> [!question] Q9
> The most appropriate model choices are:
> A. asset-based relative valuation for Tessaro and free cash flow for Quillon.
> B. dividend discount for Tessaro and P/E relative valuation for Quillon.
> C. sum-of-the-parts for Tessaro and dividend discount for Quillon.

> [!question] Q10
> The research report on Quillon most clearly violates which characteristic of an effective report?
> A. It fails to present sufficient information to critique the valuation.
> B. It fails to distinguish a good company from a good investment.
> C. It fails to state the implied upside, which is 40%.

> [!success]- Answer key
> Q1: B.
> $V_E - P = 180 - 150 = 30$; true mispricing $V - P = 170 - 150 = 20$; estimation error $V_E - V = 180 - 170 = 10$ (Python: `170-150 = 20`, `180-170 = 10`).
> A is the error term; C is the whole perceived gap (V5 p.5).
>
> Q2: B.
> The director accepts the estimate and worries that convergence may not occur within the horizon, which is why active investors look for a catalyst.
> A is contradicted by "even if your model and forecasts are perfect"; C concerns why prices can differ from value at all, not the timing of convergence (V5 p.6).
>
> Q3: A.
> Value from selling assets individually is liquidation value; the higher figure from selling over a longer period is orderly liquidation value.
> B mislabels an asset-sale figure as going concern; C uses transaction concepts that are not about dissolution (V5 p.6).
>
> Q4: C.
> Cash component $= 150 + (-40) = 110$; accruals $= 240 - 110 = 130$; turnover $= 1{,}035 / 207 = 5.0$; days $= 365 / 5 = 73$ (Python: `240-(150-40) = 130`, `1035/207 = 5.0`, `365/5 = 73`).
> A uses CFO alone for the cash component (240 - 150 = 90) and the prior year's turnover of 6.0; B mixes the correct accrual with the prior-year days (V5 p.17, p.20).
>
> Q5: C.
> $(0.080 - 0.30 \times 0.04) / 0.70 = 0.068 / 0.70 = 0.0971$ (Python: `(0.08-0.3*0.04)/0.7 = 0.09714`).
> A is the blended rate; B is the answer if bonds were 25% of assets (V5 p.19).
>
> Q6: B.
> Deferring an operating outlay raises current earnings; adding back the amortisation to EBITDA hides a real cash cost, so debt/EBITDA is understated and financial strength overstated, exactly the Livent error.
> A has the direction of the ratio error reversed; C has the earnings effect reversed (V5 p.21, p.22).
>
> Q7: A.
> $V_{\text{SOTP}} = 1{,}200 + 800 + 400 - 150 = 2{,}250$; equity $= 2{,}250 - 600 = 1{,}650$; per share $1{,}650 / 100 = 16.50$; discount $= (16.50 - 13.50) / 16.50 = 18.2\%$ (Python: `1200+800+400-150-600 = 1650`, `(16.5-13.5)/16.5 = 0.1818`).
> B divides the gap by price instead of by sum-of-the-parts value ($3 / 13.5 = 22\%$); C forgets the corporate cost adjustment ($1{,}800 / 100 = 18.00$) (V5 p.27 to p.29).
>
> Q8: C.
> If the discount is an artefact of flawed measurement, there is no real gap to close.
> A implies a spin-off would improve capital allocation and unlock value; B says poor performers diversify, which explains the discount without denying that separation could help (V5 p.29).
>
> Q9: A.
> A bank's marketable assets make asset-based relative valuation more relevant; negative earnings and no dividend rule out P/E and DDM for Quillon, while free cash flow suits both the data and the takeover (control) perspective.
> B and C each assign a model that fails the data availability criterion for at least one company (V5 p.29).
>
> Q10: B.
> Returns depend on the price paid, so a good company is not automatically a good investment; the report conflates the two.
> A is wrong because the DCF inputs are stated; C is wrong because the upside is $42 / 30 - 1 = 40\%$ and stating it is not a listed requirement, although the basis, time frame and uncertainty of the target are (Python: `42/30-1 = 0.40`) (V5 p.33, p.34).

## Flashcards

#flashcards/cfa-l2/05-Equity-Valuation/lm01

Definition of valuation::Estimation of an asset's value based on variables related to future returns, comparisons with similar assets, or estimates of immediate liquidation proceeds (V5 p.4).
Definition of intrinsic value::The value of an asset given a hypothetically complete understanding of its investment characteristics (V5 p.4).
Grossman-Stiglitz paradox in one line::If prices perfectly reflected value nobody would pay to analyse, but without analysis prices could not reflect value; so investors analyse only when they expect to be rewarded (V5 p.5).
Perceived mispricing decomposition::$V_E - P = (V - P) + (V_E - V)$, true mispricing plus estimation error (V5 p.5).
Which term of the decomposition contributes to alpha?::$V - P$, the true but unobservable intrinsic value less the market price (V5 p.5).
Micro-problem: estimate 50, price 45, true value 48; true mispricing and error?::True mispricing 3, estimation error 2; keystrokes 48 - 45 = and 50 - 48 = (V5 p.5).
Two conditions for consistently successful active selection::Expectations must differ from consensus and be, on average, correct (V5 p.6).
Why do some active investors require a catalyst?::Convergence of price to intrinsic value may not happen within the investment horizon, so an event that forces re-evaluation is needed (V5 p.6).
Going-concern assumption::The company continues its business activities into the foreseeable future, using assets in a value-maximizing way and accessing optimal financing (V5 p.6).
Liquidation value::Value if the company is dissolved and its assets sold individually (V5 p.6).
Orderly liquidation value::Value when assets are sold over a longer period rather than immediately; higher than a forced liquidation (V5 p.6).
When can liquidation value exceed going-concern value?::For a persistently unprofitable business, worth more dead than alive (V5 p.6).
Fair market value::Price between a willing buyer and a willing seller, neither under compulsion, both informed of material facts; used in tax and buy-sell contexts (V5 p.6).
Fair value (financial reporting)::Amount for which an asset could be exchanged or a liability settled between knowledgeable willing parties in an arm's length transaction; related to but not identical with fair market value (V5 p.7).
Investment value::Value to a specific buyer taking account of synergies and that buyer's requirements and expectations (V5 p.7).
Which definition of value is relevant for public equities?::Intrinsic value estimated under a going-concern assumption (V5 p.7).
List the applications of equity valuation::Stock selection, inferring market expectations, evaluating corporate events, fairness opinions, evaluating strategies and business models, communicating with analysts and shareholders, appraising private businesses, share-based payment (V5 p.7, p.8).
How is a market expectation extracted?::Choose a model, estimate every fundamental except one, and solve for the value of that fundamental that makes model value equal to the market price (V5 p.7, p.8).
Cornell's Intel finding::The $61.50 pre-announcement price implied 20% growth for 10 years then 6%; the $43.31 price implied well under 15%; the 20% was far above Intel's history, so the stock had been overvalued (V5 p.9, p.10).
Five steps of the valuation process::Understand the business, forecast performance, select the model, convert forecasts to a valuation, apply the conclusions (V5 p.10).
Three questions of industry and competitive analysis::How attractive is the industry for sustained profitability; what is the company's competitive position and strategy; how well has it executed and what are its prospects (V5 p.11, p.12).
Porter's five forces::Intra-industry rivalry, threat of new entrants, threat of substitutes, bargaining power of suppliers, bargaining power of buyers (V5 p.11).
Feature of each force that raises industry profitability::Low rivalry with brand identification, high entry costs, few substitutes or high switching costs, many suppliers, many buyers (V5 p.11).
Porter's three generic strategies::Cost leadership, differentiation, focus (cost focus or differentiation focus) (V5 p.12).
Regression toward the mean in forecasting::Successful companies attract competition and poor performers get restructured, so long-horizon growth forecasts should converge to the economy's average (V5 p.12).
Qualitative factors to weigh in assessing execution::Ownership structure, intellectual and physical property, terms of licenses and franchise agreements, potential legal disputes and contingent liabilities (V5 p.12).
US annual and interim filings for domestic and foreign companies::10-K and 10-Q for US companies; 20-F and 6-K for non-US companies (V5 p.15).
What does Regulation FD do?::Prohibits companies from disclosing material nonpublic information to analysts without also disseminating it to the public (V5 p.15).
Quality of earnings analysis::Scrutiny of all financial statements to evaluate sustainability of performance and how accurately reported results reflect economic reality (V5 p.17).
Cash versus accrual components of earnings::Cash component is CFO plus CFI; accruals are net income minus the cash component; the cash component is more persistent (Sloan 1996) (V5 p.17).
What does a high accrual share predict?::Lower future ROA and lower earnings quality (V5 p.17).
Examples of aggressive estimates in Exhibit 3::Long depreciable lives, long amortisation periods, high pension discount rate, low compensation growth, high expected return on pension assets (V5 p.18).
Micro-problem: 8% plan return assumption, 28% bonds at 5%; implied equity return?::(0.08 - 0.014) / 0.72 = 9.2%; keystrokes 0.28 × 0.05 = then 0.08 - 0.014 = then ÷ 0.72 = (V5 p.19).
Effect of an aggressive expected return on plan assets::Larger deduction in pension expense, so expense is understated and net income overstated (V5 p.19).
Micro-problem: revenue 212,476 and average receivables 50,110; turnover and days?::Turnover 4.2, days 365 / 4.2 = 87; keystrokes 212476 ÷ 50110 = then 365 ÷ 4.2 = (V5 p.20).
General warning sign from the Tangoe and Livent cases::An asset account (receivables, deferred costs) growing much faster than sales (V5 p.22).
Why not add back amortisation of capitalised preproduction costs to EBITDA?::The cash was actually spent, so the add-back overstates debt-paying ability; Livent's 1996 debt/EBITDA was 1.7 with the add-back and 5.5 without (V5 p.21, p.22).
Three categories of fraud risk indicators::Incentives to commit fraud, opportunity to commit fraud, attitude toward committing fraud (V5 p.22).
Top-down versus bottom-up forecasting::Top-down moves from macro to industry to company; bottom-up aggregates micro-level forecasts into larger-scale forecasts (V5 p.23).
Absolute valuation model::A model that specifies an asset's intrinsic value; present value models and asset-based valuation (V5 p.23, p.25).
Company-level cash flow definitions used in present value models::Free cash flow (to equity or to the firm) and residual income (V5 p.24).
Why is present value harder for stock than for bonds?::Cash flows must be defined and forecast rather than read from a contract, extend indefinitely, and the discount rate is subjective (V5 p.24).
Relative valuation model::Estimates an asset's value relative to another asset using price or enterprise multiples; similar assets should sell at similar prices (V5 p.25).
Limitation of the method of comparables::It cannot specify intrinsic value without assuming the comparison asset is fairly valued (V5 p.26).
Pairs trading::Buy the relatively undervalued stock and short the relatively overvalued stock among closely related stocks; profits if the spread closes regardless of market direction (V5 p.25, p.26).
Sum-of-the-parts valuation::Sum of the estimated values of each business as an independent going concern; also called breakup value or private market value (V5 p.27).
When is sum-of-the-parts most useful?::Segments in different industries with different valuation characteristics, and when assessing spin-offs, split-offs, tracking stock and carve-outs (V5 p.27).
Three explanations of the conglomerate discount::Inefficient internal capital markets, endogenous factors (poor performers diversify by acquisition), research measurement errors (V5 p.29).
Three broad criteria for model selection::Consistent with company characteristics, appropriate given data availability and quality, consistent with the purpose and the analyst's perspective (V5 p.29).
Why would a controlling investor prefer free cash flow to dividends?::The acquirer can redirect free cash flows without affecting the acquisition's value (V5 p.29).
Situational adjustments to a valuation::Control premium, lack of marketability discount, illiquidity discount, blockage factor (V5 p.30).
Three groups analysts benefit::Clients (better buy and sell decisions), capital markets (prices closer to value), suppliers of capital (monitoring management) (V5 p.31).
What must a report state about a target price?::The basis for computing it, a time frame for reaching it, and the uncertainty of reaching it (V5 p.33).
Eight characteristics of an effective research report::Timely, clear language, objective with key assumptions identified, distinguishes fact from opinion, internally consistent, enough information to critique, states key risks, discloses conflicts (V5 p.33, p.34).
Micro-problem: target EUR 3.08, price EUR 2.25; implied upside?::3.08 / 2.25 - 1 = 36.9%; keystrokes 3.08 ÷ 2.25 = then - 1 = (V5 p.35).
Standards listed as governing research reports::I(B) independence and objectivity, I(C) misrepresentation, V(A) diligence and reasonable basis, V(B) communication with clients, V(C) record retention (V5 p.37).
Trap: "the analyst's estimation error contributes to alpha"::Wrong; only the difference between true intrinsic value and price contributes; estimation error is noise (V5 p.5).
Trap: "many suppliers hurt industry profitability"::Wrong; many suppliers compete and limit input price increases, which helps profitability (V5 p.11, p.47).
A good company is not necessarily a {{good investment}} because returns always depend on the {{price paid}} (V5 p.34).
The value derived from a sum-of-the-parts valuation is sometimes called the {{breakup value}} or {{private market value}} (V5 p.27).

## Common mistakes

1. Treating $V_E - P$ as the alpha opportunity; only $V - P$ earns abnormal return and $V_E - V$ is the analyst's own error (V5 p.5, p.47).
2. Assuming a correct estimate guarantees a return; convergence may not happen within the horizon, which is why catalysts matter (V5 p.6).
3. Confusing fair market value (willing buyer and seller, tax and buy-sell contexts) with fair value (accounting standard definition for reporting) and with intrinsic value (public equity focus) (V5 p.6, p.7).
4. Assigning investment value to a portfolio investor; it belongs to a specific buyer with synergies (V5 p.7).
5. Forgetting that liquidation value can exceed going-concern value for persistently unprofitable firms, and ignoring the time dimension captured by orderly liquidation value (V5 p.6).
6. Reversing the sign of a Porter force: low entry barriers, low switching costs and high rivalry reduce profitability; many suppliers and many buyers raise it (V5 p.11, p.47).
7. Extrapolating past growth without allowing for regression toward the mean from competition and restructuring (V5 p.12).
8. Calling favourable nonrecurring items unbiased because they are disclosed; they bias reported earnings upward relative to sustainable earnings (V5 p.17, p.47).
9. Adding back amortisation of capitalised operating costs to EBITDA, which hides real cash outflows and overstates debt-paying ability (V5 p.21, p.22).
10. Labelling a discounted free cash flow model as relative because several companies are compared; the model type depends on the output, not on how many firms are analysed (V5 p.23, p.47).
11. Reading "relatively undervalued" as "undervalued"; the comparables method assumes the benchmark is fairly priced, so two relative verdicts with different benchmarks can both be right (V5 p.25, p.26).
12. Choosing DDM or P/E for a company with no dividend or negative earnings instead of applying the data availability criterion and moving to free cash flow (V5 p.29, p.47).
13. Applying a lack of marketability discount or blockage factor to a controlling stake in a listed company when the relevant adjustment is a control premium (V5 p.30, p.48).
14. Treating diligence on filings and calls as top-down analysis; top-down starts with general economic conditions (V5 p.23, p.32, p.48).
15. Equating a good company with a good investment in a report; return depends on the price paid (V5 p.34).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "05-01" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
