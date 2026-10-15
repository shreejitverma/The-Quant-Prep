---
type: cfa-lm
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
volume: 5
lm: 3
title: "Free Cash Flow Valuation"
pages: "125-219"
weight_band: "10-15%"
difficulty: 4
los_count: 12
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/equity-valuation]
---

# LM3: Free Cash Flow Valuation

Difficulty 4 of 5: the discounting is the same as the DDM, but the cash flow must first be built from financial statements, and the exam farms every mark from the FCFF and FCFE identities, the from-any-starting-point conversions, the WCInv exclusions, the after-tax interest add-back, and the target-debt-ratio forecast, all under item-set time pressure.

## LOS map

- **compare** the free cash flow to the firm (FCFF) and free cash flow to equity (FCFE) approaches to valuation (V5 p.125) ^los-05-03-a
    - Examiner asks: given a company description (negative FCFE and leverage, changing capital structure, stable capital structure), pick FCFF or FCFE and state the reason, or identify that FCFF discounts at WACC while FCFE discounts at r.
- **explain** the ownership perspective implicit in the FCFE approach (V5 p.125) ^los-05-03-b
    - Examiner asks: why a takeover or control investor uses free cash flow rather than dividends, because with control comes discretion over the uses of free cash flow.
- **explain** the appropriate adjustments to net income, earnings before interest and taxes (EBIT), earnings before interest, taxes, depreciation, and amortization (EBITDA), and cash flow from operations (CFO) to calculate FCFF and FCFE (V5 p.125) ^los-05-03-c
    - Examiner asks: which items are added or subtracted from each starting point, including the noncash-charge table (losses added, gains subtracted) and the IFRS interest classification caveat for CFO.
- **calculate** FCFF and FCFE (V5 p.125) ^los-05-03-d
    - Examiner asks: a full set of financial statements and a request for FCFF from NI, EBIT, EBITDA or CFO and FCFE from FCFF, NI or CFO, with WCInv excluding cash and notes payable and net borrowing including both notes payable and long-term debt.
- **describe** approaches for forecasting FCFF and FCFE (V5 p.125) ^los-05-03-e
    - Examiner asks: the sales-based method, incremental FCInv and WCInv as fixed fractions of the sales increase, and the target debt ratio shortcut FCFE = NI minus (1 minus DR) times the net investments.
- **explain** how dividends, share repurchases, share issues, and changes in leverage may affect future FCFF and FCFE (V5 p.125) ^los-05-03-f
    - Examiner asks: two statements, one saying dividends or buybacks change free cash flow (false, they are uses of it) and one saying leverage changes do not affect FCFE (false, new debt raises FCFE now and after-tax interest lowers it later).
- **compare** the FCFE model and dividend discount models (V5 p.125) ^los-05-03-g
    - Examiner asks: when the two give the same value (FCFE equals dividends, or all inputs consistent) and why FCFE is preferred for non-payers, payers whose dividends differ from capacity, and control situations.
- **evaluate** the use of net income and EBITDA as proxies for cash flow in valuation (V5 p.125) ^los-05-03-h
    - Examiner asks: what NI misses relative to FCFE (investments and net borrowing) and the four defects of EBITDA as an FCFF proxy (pre-tax, ignores the depreciation tax shield, ignores FCInv and WCInv, ignores capital structure).
- **explain** the use of sensitivity analysis in FCFF and FCFE valuations (V5 p.125) ^los-05-03-i
    - Examiner asks: recompute value with the low and high estimate of each input, one at a time, and rank the input ranges; the growth rate or the cost of equity usually wins.
- **explain** the single-stage (stable-growth), two-stage, and three-stage FCFF and FCFE models and justify the selection of the appropriate model given a company's characteristics (V5 p.125) ^los-05-03-j
    - Examiner asks: match a company profile (constant growth, abrupt drop, declining growth in stage 1, three phases) to the model, and recall that free cash flow "growth" may refer to sales, income or FCF itself.
- **estimate** a company's value using the appropriate free cash flow model(s) (V5 p.125) ^los-05-03-k
    - Examiner asks: the full build, forecast sales, margins, investments and debt financing, sum the PV of stage-1 FCFE or FCFF, add the PV of the terminal value, subtract debt (and preferred) for FCFF, divide by shares.
- **describe** approaches for calculating the terminal value in a multistage valuation model; and evaluate whether a stock is overvalued, fairly valued, or undervalued based on a free cash flow valuation model (V5 p.125) ^los-05-03-l
    - Examiner asks: Gordon terminal value from the first stable-growth cash flow versus a price or P/E multiple on terminal earnings, then compare model value with market price to call the stock over-, fairly or undervalued.

## Core intuition

Discounted cash flow valuation always prices the same thing, the present value of expected cash to the claimholder, so the only real question in this module is which cash and which claimholder (V5 p.126).
Dividends are the cash actually paid to shareholders; free cash flow is the cash available for distribution, and the two differ whenever the board pays out more or less than the company could sustainably distribute (V5 p.126, p.142).
FCFF is the cash flow available to all the company's suppliers of capital, debt, equity and sometimes preferred, after operating expenses including taxes have been paid and the necessary investments in working capital and fixed capital have been made (V5 p.127).
FCFE is what remains for common shareholders after the debtholders have also been served, that is after after-tax interest has been paid and principal transactions netted (V5 p.127, p.141).

> [!abstract] Idea 1: match the cash flow to the discount rate, and the model to the capital structure
> FCFF belongs to all capital providers, so it is discounted at WACC and gives firm value; equity value is firm value minus the market value of debt (V5 p.128, p.129).
> FCFE belongs to shareholders alone, so it is discounted at the required return on equity and gives equity value directly (V5 p.129).
> Use FCFE when the capital structure is stable, because it is more direct; use FCFF for a levered company with negative FCFE or a changing capital structure, because FCFF growth reflects fundamentals rather than fluctuating net borrowing, and WACC is less sensitive to leverage than the cost of equity (V5 p.128).

Analysts reach for free cash flow rather than dividends when the company pays no dividends, when dividends differ significantly from the capacity to pay them, when free cash flows align with profitability within a comfortable forecast horizon, or when the investor takes a control perspective, since a controlling owner can redirect the cash, for example to service acquisition debt (V5 p.126).
That control perspective is the ownership story implicit in FCFE: FCFE is the amount the company could pay as dividends, so it is the right measure for whoever gets to decide the payout (V5 p.142, p.156).
In practice free cash flow models dominate: 86.9% of analysts using DCF use discounted free cash flow, and FCFF models are used roughly twice as often as FCFE models (V5 p.126).

### Building the cash flow from the statements

Nothing labeled FCFF or FCFE appears in the financial statements, so the module's core skill is reconstruction (V5 p.126, p.127).
Starting from net income, three repairs are needed (V5 p.131).
First, add back net noncash charges, above all depreciation and amortization, because they reduced income without consuming cash; losses are added back and gains subtracted because the related cash sits in investing, not operations (V5 p.131, p.132, p.138).
Second, add back interest expense times (1 minus the tax rate), because after-tax interest was removed from net income but is cash flowing to a capital provider; the tax adjustment keeps FCFF consistent with the after-tax WACC that discounts it (V5 p.132).
Preferred dividends deducted in arriving at income available to common get the same add-back treatment, with no tax adjustment because they are not deductible (V5 p.132, p.159).
Third, subtract the investments in fixed capital and in working capital, because cash ploughed into receivables, inventory and equipment is not available for distribution (V5 p.132).
Working capital for valuation excludes cash and equivalents, because the change in cash is what the exercise is explaining, and excludes notes payable and the current portion of long-term debt, because interest-bearing liabilities are financing, not operations (V5 p.132, p.133).
Starting from CFO is shorter because depreciation and WCInv are already inside CFO; only the after-tax interest add-back and the capex subtraction remain, and under US GAAP interest paid is always in CFO so the add-back is always needed (V5 p.135).
Under IFRS interest paid may be classified as operating or financing; if it sits in financing, CFO was never reduced by it and no add-back is made (V5 p.135, p.137).
Deferred taxes deserve a look: add them back only if the company can keep deferring them indefinitely, and do not add back changes expected to reverse soon; share-based compensation expense is noncash now but has cash and share-count consequences later (V5 p.138, p.139).

> [!abstract] Idea 2: every starting point collapses to the same FCFF, and FCFE is always FCFF minus after-tax interest plus net borrowing
> From NI: add NCC and after-tax interest, subtract FCInv and WCInv; from CFO: add after-tax interest, subtract FCInv; from EBIT: multiply by (1 minus t), add depreciation, subtract FCInv and WCInv; from EBITDA: multiply by (1 minus t), add depreciation times t, subtract FCInv and WCInv (V5 p.131, p.135, p.147).
> The EBIT and EBITDA routes differ only in how depreciation is handled: EBIT already absorbed depreciation, so the full amount comes back; EBITDA never deducted it, so only the depreciation tax shield comes back (V5 p.147).
> For a single set of statements every route must produce the same number, which the exam exploits by asking for the same FCFF from two starting points, 155 for Pitts and 156 for LaForge from all four routes (V5 p.145, p.148, p.207).

The uses-of-free-cash-flow view is the consistency check: FCFF equals the increase in cash balances plus after-tax interest plus net debt repayment plus dividends plus net share repurchases, and FCFE equals the increase in cash balances plus dividends plus net repurchases (V5 p.149, p.150).
Reading the uses side reveals policy: Pitts borrowed 75 while paying 160 of dividends from FCFF of 155, so it was leveraging up partly to pay shareholders (V5 p.150, p.151).
This is also where the effect questions live: dividends, share repurchases and share issues are uses of free cash flow and change neither FCFF nor FCFE, whereas a leverage increase leaves FCFF unchanged but raises FCFE by the debt issued in the year of issue and lowers later FCFE by the after-tax interest (V5 p.156, p.157, p.161).

### Forecasting instead of measuring

Historical free cash flow can be grown at a constant rate, but the richer method drives everything off sales (V5 p.151).
Assume incremental fixed capital investment, capex minus depreciation, and incremental working capital investment are fixed fractions of the increase in sales; forecast sales growth and the EBIT margin, and FCFF is EBIT times (1 minus t) minus those two increments (V5 p.152).
Depreciation is treated as the cost of maintaining existing capacity, so only investment beyond depreciation is a claim on the growth in sales (V5 p.152).
For FCFE, assume a target debt ratio DR so that debt finances DR of the net new investment; net borrowing no longer needs a year-by-year forecast and FCFE equals net income minus (1 minus DR) times (FCInv minus Dep) minus (1 minus DR) times WCInv (V5 p.153).
The simplification assumes depreciation is the only noncash charge; when other noncash charges are significant, forecast the components individually or the estimate degrades, the trap behind Company A in the practice set (V5 p.153, p.155, p.205).

### Why not just use NI or EBITDA

Net income misses the investments in fixed and working capital and the net borrowing that FCFE captures, so NI equals FCFE only in the razor's edge case where new investment equals depreciation and WCInv and net borrowing are zero (V5 p.158).
EBITDA is before tax, ignores the depreciation tax shield, ignores FCInv and WCInv entirely, and from an equity view also ignores after-tax interest and debt flows, so it systematically overstates distributable cash for a growing company (V5 p.157, p.158).
Discounting EBITDA at a bond rate compounds the error by using a pre-tax, riskless rate on a risky, pre-tax, non-perpetual stream (V5 p.215).

### Models, terminal value and sensitivity

The model menu mirrors the DDM: single-stage constant growth, two-stage with either an abrupt drop or a decline in stage 1, and three-stage (V5 p.129, p.164, p.172).
An international variant runs the single-stage model in real terms, with a build-up real required return, country return plus industry, size and leverage adjustments, matched to a real growth rate, useful when inflation is high or volatile (V5 p.161, p.162).
In free cash flow models the stated "growth rate" may refer to sales, income or FCF itself, so read the vignette carefully (V5 p.165).
When sales growth steps down, FCFE can jump upward at the transition because investment needs and the debt financed against them collapse while profits keep growing, 169% growth for TechnoSchaft between years 3 and 4; negative FCFE in the high-investment years is normal and is simply discounted as a negative (V5 p.166, p.167, p.168).

> [!abstract] Idea 3: the terminal value carries most of the answer, and it is set at the last explicit-forecast date with the first stable-growth cash flow
> Terminal value at time n is FCFF or FCFE at n + 1 divided by (WACC minus g) or (r minus g), discounted n periods; alternatively apply a price or P/E multiple to terminal earnings, 18 times 2025 EPS for NYL (V5 p.165, p.201).
> The PV of the terminal value is routinely most of total value, 94% for TechnoSchaft and 95% for QuickChange, so the mature g and the discount rate drive everything (V5 p.167, p.219).
> Sensitivity analysis makes this concrete: move one input at a time between its low and high estimate and compare value ranges; for Petrobras the FCFE growth rate dominated beta, the risk-free rate and the ERP, and for Colanari the cost of equity dominated the growth rate and the cost of debt (V5 p.163, p.164, p.212).

The base-year cash flow deserves equal respect: value scales proportionally with FCFF0 or FCFE0, so a base year distorted by non-recurring items or unsustainable working capital changes must be normalized, the Duplico lesson that inventory cannot be squeezed below zero and a growing company's working capital needs grow (V5 p.139, p.141, p.163).
Finally, free cash flow values only the operating assets; excess cash, marketable securities, investment land and pension surpluses are added at market value to get total firm value, and ESG effects enter either as explicit cash flow adjustments (delayed mine opening, water capex) or as a risk premium added to the cost of equity when the effect is real but hard to quantify (V5 p.174, p.176, p.177).

## Formulas and derivations

**FCFF valuation model and equity value** (V5 p.128, p.129)
$$
\text{Firm value} = \sum_{t=1}^{\infty} \frac{FCFF_t}{(1+WACC)^t}, \qquad \text{Equity value} = \text{Firm value} - \text{MV(Debt)}
$$
^f-05-03-1

- $FCFF_t$: expected free cash flow to the firm at $t$; WACC: weighted average cost of capital; MV(Debt): market value of debt, not book.
- FCFF belongs to all capital providers, so discounting at the blended after-tax required return prices all the firm's capital; stripping out debt (and preferred, if any) leaves common equity (V5 p.129).
- Divide equity value by shares outstanding for value per share (V5 p.129).

**WACC** (V5 p.129)
$$
WACC = \frac{MV(Debt)}{MV(Debt)+MV(Equity)} r_d (1 - \text{Tax rate}) + \frac{MV(Equity)}{MV(Debt)+MV(Equity)} r
$$
^f-05-03-2

- Weights are market values or the known target capital structure; the tax rate is in principle the marginal rate; $r_d(1-t)$ is the after-tax cost of debt and $r$ the cost of equity (V5 p.129).
- Consistency rule: after-tax FCFF goes with after-tax WACC; a pre-tax convention would need both sides changed together (V5 p.132).
- With preferred stock a third term $w_p r_p$ is added with no tax adjustment, Welch: $0.4(8\%)(0.7) + 0.1(8\%) + 0.5(12\%) = 9.04\%$ (V5 p.160).

**FCFE valuation model** (V5 p.129)
$$
\text{Equity value} = \sum_{t=1}^{\infty} \frac{FCFE_t}{(1+r)^t}
$$
^f-05-03-3

- $r$: required return on equity, usually from the CAPM $r = R_F + \beta[E(R_M) - R_F]$ in this module's examples.
- FCFE is the residual claim after all other capital providers are paid, so the equity discount rate is the right risk adjustment (V5 p.129).

**Single-stage (constant-growth) FCFF model** (V5 p.129)
$$
\text{Firm value} = \frac{FCFF_1}{WACC - g} = \frac{FCFF_0 (1+g)}{WACC - g}
$$
^f-05-03-4

- Same geometric-series argument as the Gordon model with $FCFF_t = FCFF_{t-1}(1+g)$; requires $WACC > g$ (V5 p.129).
- Subtract the market value of debt to reach equity (V5 p.129).

> [!tip] Calculator
> Example 1: `700 × 1.05 =` gives 735; `0.102 - 0.05 =` gives 0.052; `735 ÷ 0.052 =` gives 14,134.6; `- 2200 = ÷ 200 =` gives 59.67.

**Single-stage (constant-growth) FCFE model** (V5 p.130)
$$
\text{Equity value} = \frac{FCFE_1}{r - g} = \frac{FCFE_0 (1+g)}{r - g}
$$
^f-05-03-5

- The growth rate of FCFE need not equal, and frequently does not equal, the growth rate of FCFF (V5 p.130).
- Welch grows FCFF at 4.0% and FCFE at 5.4% in the same problem (V5 p.159).

**FCFF from net income** (V5 p.131)
$$
FCFF = NI + NCC + Int(1 - \text{Tax rate}) - FCInv - WCInv
$$
^f-05-03-6

- NI: net income available to common, after preferred dividends; NCC: net noncash charges (depreciation, amortization, losses added; gains, restructuring reversals subtracted); Int: interest expense; FCInv: capex net of proceeds from fixed-asset sales; WCInv: increase in working capital excluding cash, equivalents, notes payable and the current portion of long-term debt (V5 p.131, p.132, p.133).
- Derivation: NI already deducted after-tax interest and noncash charges, so both are restored; then the cash reinvested in the business is removed because it is not distributable (V5 p.131, p.132).
- With preferred stock: add preferred dividends back as well, since they are cash to a capital provider (V5 p.159, p.160).

**FCFF from CFO** (V5 p.135)
$$
FCFF = CFO + Int(1 - \text{Tax rate}) - FCInv
$$
^f-05-03-7

- No depreciation or WCInv terms appear because CFO already contains them (V5 p.135).
- IFRS caveat: the add-back applies only if interest paid was classified inside operating cash flow, which US GAAP requires and most IFRS filers choose; if interest paid is classified as financing under IFRS, do not add it back (V5 p.135, p.137).
- IFRS also allows dividends paid in operating; if so, they must be added back to CFO since dividends are a use, not a determinant, of free cash flow (V5 p.137).

**FCFE from FCFF** (V5 p.141)
$$
FCFE = FCFF - Int(1 - \text{Tax rate}) + \text{Net borrowing}
$$
^f-05-03-8

- Net borrowing: debt issued minus debt repaid over the period, counting notes payable and long-term debt (and net new preferred issues when preferred exists) (V5 p.141, p.146, p.160).
- Reason: to pass from all-capital cash flow to equity cash flow, remove what debtholders received after tax and add what they contributed.
- Inverse: $FCFF = FCFE + Int(1-t) - \text{Net borrowing}$ (V5 p.142).

**FCFE from net income** (V5 p.142)
$$
FCFE = NI + NCC - FCInv - WCInv + \text{Net borrowing}
$$
^f-05-03-9

- Formula 6 combined with Formula 8: the $Int(1-t)$ add-back and subtraction cancel (V5 p.142).
- FCFE is the amount the company could afford to pay as dividends; boards smooth actual dividends, so FCFE and dividends usually differ (V5 p.142).

**FCFE from CFO** (V5 p.142)
$$
FCFE = CFO - FCInv + \text{Net borrowing}
$$
^f-05-03-10

- The shortest route on the exam when a cash flow statement is given; the same IFRS interest classification caveat applies (V5 p.135, p.137, p.142).

**FCFF from EBIT** (V5 p.147)
$$
FCFF = EBIT(1 - \text{Tax rate}) + Dep - FCInv - WCInv
$$
^f-05-03-11

- Derivation: with depreciation the only NCC, $NI = (EBIT - Int)(1-t) = EBIT(1-t) - Int(1-t)$; substitute into Formula 6 and the interest terms cancel (V5 p.147).
- No interest add-back is needed because EBIT sits above interest; noncash charges deducted below the EBIT line never need adjusting from this starting point (V5 p.147).

**FCFF from EBITDA** (V5 p.147)
$$
FCFF = EBITDA(1 - \text{Tax rate}) + Dep(\text{Tax rate}) - FCInv - WCInv
$$
^f-05-03-12

- Derivation: $NI = (EBITDA - Dep - Int)(1-t)$; substitute into Formula 6; depreciation survives only as its tax shield $Dep \times t$ because EBITDA never deducted it (V5 p.147).
- Contrast with Formula 11: from EBIT the full depreciation returns, from EBITDA only the tax shield; whether and how a noncash charge is adjusted depends on where it was deducted and whether it is tax deductible (V5 p.147, p.148).
- FCFE from EBIT or EBITDA: compute FCFF first, then apply Formula 8 (V5 p.148).

**Uses of FCFF and uses of FCFE** (V5 p.149, p.150)
$$
\begin{aligned}
FCFF &= \Delta \text{Cash} + Int(1-t) + \text{Net debt repayment} + \text{Dividends} + \text{Net share repurchases} \\
FCFE &= \Delta \text{Cash} + \text{Dividends} + \text{Net share repurchases}
\end{aligned}
$$
^f-05-03-13

- Uses must equal sources; net new borrowing enters as a negative repayment and net share issuance as a negative repurchase (V5 p.149, p.150).
- Pitts: $10 + 60 - 75 + 160 + 0 = 155 = FCFF$ and $10 + 160 + 0 = 170 = FCFE$ (V5 p.150, p.151).
- Reading the uses reveals capital structure policy: borrowing to pay dividends increases leverage (V5 p.149, p.151).

**Incremental investment ratios for sales-based forecasting** (V5 p.152)
$$
\frac{FCInv - Dep}{\Delta \text{Sales}} = \text{incremental FC rate}, \qquad \frac{WCInv}{\Delta \text{Sales}} = \text{incremental WC rate}
$$
^f-05-03-14

- Estimated from history, then applied to forecast sales increases; depreciation proxies the cost of maintaining existing capacity, so only the excess over depreciation is growth investment (V5 p.152).
- Pitts: $(400-300)/300 = 33.33\%$ and $45/300 = 15\%$ per dollar of sales increase (V5 p.153).
- Forecast FCFF as $EBIT(1-t)$ minus the two increments (V5 p.152).

**FCFE with a target debt ratio** (V5 p.153)
$$
FCFE = NI - (1 - DR)(FCInv - Dep) - (1 - DR)(WCInv)
$$
^f-05-03-15

- DR: target debt ratio, debt as a share of debt plus equity, assumed to finance DR of net new fixed capital and of WCInv; hence $\text{Net borrowing} = DR(FCInv - Dep) + DR(WCInv)$ and the borrowing forecast disappears (V5 p.153).
- FCFE equals NI minus the equity-financed share of net investment; assumes depreciation is the only noncash charge, so it misfires when other noncash charges are large (V5 p.153, p.155).

> [!tip] Calculator
> Example 10: `100 + 45 = × 0.5 =` gives 72.50 of net borrowing; `264 - 100 - 45 + 72.5 =` gives FCFE 191.50.

**FCFF and WACC with preferred stock** (V5 p.159, p.160)
$$
FCFF = NI + NCC + Int(1-t) + \text{Preferred dividends} - FCInv - WCInv
$$
^f-05-03-16

- NI is income available to common, so preferred dividends were already deducted and must be restored; no tax adjustment because they are not deductible (V5 p.159, p.160).
- WACC gains the term $w_p r_p$; equity value is firm value minus debt minus preferred; in FCFE, net borrowing includes net new preferred issuance (V5 p.159, p.160).

**Real-terms single-stage FCFE model** (V5 p.162)
$$
V_0 = \frac{FCFE_0 (1 + g_{real})}{r_{real} - g_{real}}
$$
^f-05-03-17

- $r_{real}$: build-up real required return, country return plus or minus industry, size and leverage adjustments; $g_{real}$: real growth benchmarked to the real country growth rate (V5 p.162).
- Useful for international stocks when inflation is high or volatile, because real rates and real growth are more reliably estimated than nominal ones (V5 p.161, p.162).
- Mukamba: $r_{real} = 7.30 + 0.80 - 0.33 - 0.12 = 7.65\%$, $g_{real} = 2.5\%$, $V_0 = 1{,}435/0.0515 = \text{CDF}27{,}864$ (V5 p.162, p.163).

**Two-stage FCFF model** (V5 p.165)
$$
\text{Firm value} = \sum_{t=1}^{n} \frac{FCFF_t}{(1+WACC)^t} + \frac{FCFF_{n+1}}{(WACC - g)} \cdot \frac{1}{(1+WACC)^n}
$$
^f-05-03-18

- The terminal value $FCFF_{n+1}/(WACC - g)$ sits at $t = n$ and is discounted $n$ periods; subtract debt for equity, divide by shares for per-share value (V5 p.165).
- Stage-2 growth is a long-run sustainable rate, slightly below GDP growth for a declining industry, slightly above for a secularly growing one (V5 p.164).

**Two-stage FCFE model and terminal value alternatives** (V5 p.165)
$$
\text{Equity value} = \sum_{t=1}^{n} \frac{FCFE_t}{(1+r)^t} + \frac{FCFE_{n+1}}{(r - g)} \cdot \frac{1}{(1+r)^n}
$$
^f-05-03-19

- $TV_n = FCFE_{n+1}/(r-g)$ by the constant-growth model, or alternatively a P/E multiple times forecast terminal EPS, 18 times 2025 EPS for NYL (V5 p.165, p.201).
- The PV of the terminal value is usually a substantial portion of total value, so terminal inputs dominate the answer (V5 p.165, p.167).
- Two stage-1 patterns: constant growth that drops abruptly, or growth that declines through stage 1 to the sustainable rate, the free cash flow analogue of the H-model pattern (V5 p.164, p.165).

> [!tip] Calculator
> Example 15: `CF` `2nd CLR WORK`, CF0 = 0, C01 = 0.90, C02 = 1.08, C03 = 55.846 (1.296 + 54.55), `NPV`, I = 12.4, `CPT` gives 40.98.

**Firm value with non-operating assets** (V5 p.177)
$$
\text{Firm value} = \text{Value of operating assets} + \text{Value of non-operating assets}
$$
^f-05-03-20

- Free cash flow values only the assets that generate operating cash flow; excess cash, excess marketable securities, investment land, noncurrent financial investments at market value, and pension surpluses are added separately (V5 p.177, p.219).
- Any asset excluded from the cash flow projection must have its value added back separately (V5 p.177).

### The from-any-starting-point table

| Starting point | To FCFF | To FCFE |
|---|---|---|
| NI | $+ NCC + Int(1-t) - FCInv - WCInv$ (V5 p.131) | $+ NCC - FCInv - WCInv + NB$ (V5 p.142) |
| CFO | $+ Int(1-t) - FCInv$ (V5 p.135) | $- FCInv + NB$ (V5 p.142) |
| EBIT | $\times (1-t) + Dep - FCInv - WCInv$ (V5 p.147) | FCFF route, then $- Int(1-t) + NB$ (V5 p.148) |
| EBITDA | $\times (1-t) + Dep(t) - FCInv - WCInv$ (V5 p.147) | FCFF route, then $- Int(1-t) + NB$ (V5 p.148) |
| FCFF | identity | $- Int(1-t) + NB$ (V5 p.141) |

NB is net borrowing.
Memorize the depreciation asymmetry (full add-back from EBIT, tax shield only from EBITDA) and the CFO shortcut (no NCC, no WCInv).

## Worked examples

### Example 1: using the constant-growth FCFF valuation model (V5 p.130)

Setup: Cagiati Enterprises, FCFF0 = CHF700 million, FCFE0 = CHF620 million, before-tax cost of debt 5.7%, required return on equity 11.8%, target structure 20% debt and 80% equity, tax rate 33.33%, FCFF growth 5.0% forever, debt CHF2.2 billion, 200 million shares.

Part 1: $WACC = 0.20(5.7\%)(1 - 0.3333) + 0.80(11.8\%) = 0.76\% + 9.44\% = 10.2\%$ (Formula 2).
Part 2: Firm value $= 700(1.05)/(0.102 - 0.05) = 735/0.052 = \text{CHF}14{,}134.6$ million; equity $= 14{,}134.6 - 2{,}200 = \text{CHF}11{,}934.6$ million (Formulas 4 and 1).
Part 3: value per share $= 11{,}934.6/200 = \text{CHF}59.67$.
Python check: `0.2*5.7*(2/3)+0.8*11.8 = 10.20`, `735/0.052 = 14134.615`, `11934.615/200 = 59.673`. ^ex-05-03-1

### Example 2: calculating FCFF from net income, Cane Distribution (V5 p.133, p.134)

Setup: Cane incorporated end-2017 with debt 224 and stock 336 (thousands); depreciable property 450 over 10 years; income statements and balance sheets for 2018 to 2020; tax 30%, interest 7%.

Apply Formula 6 each year, with WCInv from the working capital exhibit (working capital excluding cash and short-term debt rose 60 to 116 to 127.6 to 140.36).

| | 2018 | 2019 | 2020 |
|---|---|---|---|
| Net income | 97.52 | 107.28 | 118.00 |
| + Depreciation | 45.00 | 49.50 | 54.45 |
| + Int(1 - 0.30) | 10.98 | 12.08 | 13.28 |
| - FCInv | 0.00 | 50.00 | 55.00 |
| - WCInv | 56.00 | 11.60 | 12.76 |
| FCFF | 97.50 | 107.26 | 117.97 |

FCInv is the increase in gross fixed assets (500 to 550 to 605); 2018 has none.
Python check: `97.52+45+15.68*0.7-0-56 = 97.50`, `107.28+49.5+17.25*0.7-50-11.6 = 107.255` (curriculum rounds the after-tax interest to 12.08 and reports 107.26), `118+54.45+18.97*0.7-55-12.76 = 117.97`. ^ex-05-03-2

### Example 3: calculating FCFF from CFO, Cane Distribution (V5 p.136)

Setup: Cane's indirect-method cash flow statement; CFO of 86.52, 145.18, 159.69 for 2018 to 2020; interest paid 15.68, 17.25, 18.97; purchases of PP&E 0, 50, 55; tax 30%.

Apply Formula 7: FCFF = CFO + Int(1 - 0.30) - FCInv.
2018: $86.52 + 10.98 - 0 = 97.50$.
2019: $145.18 + 12.08 - 50 = 107.26$.
2020: $159.69 + 13.28 - 55 = 117.97$.
Identical to Example 2, as it must be, because CFO already nets depreciation and working capital.
Python check: `86.52+15.68*0.7 = 97.496`, `145.18+17.25*0.7-50 = 107.255`, `159.69+18.97*0.7-55 = 117.969`. ^ex-05-03-3

### Example 4: sustainability of working capital effects on free cash flow, Duplico (V5 p.139 to p.141)

Setup: Duplico's IFRS cash flow statement, 2020 to 2022; depreciation 235.4, 277.7, 309.2 against capex 997.8, 897.2, 317.6; analysts expect depreciation to grow substantially.

Part 1: in 2020 capex was over 4 times depreciation; by 2022 they were nearly equal (317.6 versus 309.2), so future depreciation growth depends on future capex.
Rising depreciation cuts net income by $Dep \times (1 - t)$ but raises CFO by $Dep \times t$, because the full depreciation is added back while income falls by only its after-tax amount; at worst, in a loss position, it is neutral for CFO (V5 p.140, p.141).
Part 2: the 2022 increases in inventories and trade receivables are uses of cash (negative adjustments), and the increases in payables, accrued expenses and other creditors are sources; each flows one for one into CFO and hence FCFE.
Declining asset balances or rising payables cannot fund growth forever, inventory cannot fall below zero, and a growing Duplico should expect working capital needs to grow (V5 p.141).
Python check: `997.8/235.4 = 4.24`, `317.6/309.2 = 1.03`. ^ex-05-03-4

### Example 5: adjusting NI or CFO to find FCFF and FCFE, Pitts Corporation (V5 p.143 to p.147)

Setup: Pitts 2020, NI 240, depreciation 300, interest 100, tax 40%, capex 400 (gross fixed assets 2,200 to 2,600), CFO 495, dividends 160; balance sheet changes: AR +40, inventory +30, AP +15, accrued +10, notes payable +50, long-term debt +25.

WCInv $= 40 + 30 - 15 - 10 = 45$, ignoring cash (+10) and notes payable, which are excluded by definition.
Net borrowing $= 50 + 25 = 75$.
Part 1, FCFF from NI: $240 + 300 + 100(0.60) - 400 - 45 = 240 + 300 + 60 - 400 - 45 = 155$ (Formula 6).
Part 2, FCFE from FCFF: $155 - 60 + 75 = 170$ (Formula 8).
Part 3, FCFE from NI: $240 + 300 - 400 - 45 + 75 = 170$ (Formula 9).
Part 4, FCFF from CFO: $495 + 60 - 400 = 155$ (Formula 7).
Part 5, FCFE from CFO: $495 - 400 + 75 = 170$ (Formula 10).
FCFE exceeds FCFF here only because external borrowing was large this year (V5 p.147).
Python check: `240+300+60-400-45 = 155`, `495-400+75 = 170`. ^ex-05-03-5

### Example 6: adjusting EBIT and EBITDA to find FCFF and FCFE, Pitts (V5 p.148, p.149)

Setup: Pitts EBIT 500, EBITDA 800, everything else as in Example 5.

From EBIT: $500(0.60) + 300 - 400 - 45 = 300 + 300 - 445 = 155$ (Formula 11).
From EBITDA: $800(0.60) + 300(0.40) - 400 - 45 = 480 + 120 - 445 = 155$ (Formula 12).
FCFE either way: $155 - 100(0.60) + 75 = 170$ (Formula 8).
Note the depreciation handling: full 300 from EBIT, only the 120 tax shield from EBITDA.
Python check: `500*0.6+300-445 = 155`, `800*0.6+300*0.4-445 = 155`. ^ex-05-03-6

### Example 7: constant growth in FCFF (V5 p.151)

Setup: Pitts FCFF of 155 in 2020, growing at the historical 15% a year.

$FCFF_{2021} = 155(1.15) = 178.25$; $FCFF_{2022} = 155(1.15)^2 = 204.99$; $FCFF_{2023} = 155(1.15)^3 = 235.74$.
Extrapolation at a constant rate is appropriate only if free cash flow has grown steadily and the historical relationships to fundamentals are expected to persist (V5 p.151).
Python check: `[155*1.15**k for k in (1,2,3)] = [178.25, 204.99, 235.74]`. ^ex-05-03-7

### Example 8: free cash flow tied to sales, Pitts 2021 forecast (V5 p.153, p.154)

Setup: sales 3,000 in 2020, up 300 from 2019, growing 10% a year; EBIT margin 16.67%; tax 40%; capex 400, depreciation 300.

Incremental FC rate $= (400 - 300)/300 = 33.33\%$; incremental WC rate $= 45/300 = 15\%$ (Formula 14).
Forecast: sales 3,300 (up 300), EBIT $= 0.1667 \times 3{,}300 = 550$, EBIT(1 - t) = 330.
FCFF $= 330 - 0.3333(300) - 0.15(300) = 330 - 100 - 45 = 185$.
Python check: `3300*(500/3000)*0.6 = 330`, `330-100-45 = 185`. ^ex-05-03-8

### Example 9: free cash flow growth tied to sales growth, five years (V5 p.154)

Setup: sales grow 10% a year for five years; EBIT margin declines 16.67%, 16.00%, 15.50%, 15.00%, 14.50%; tax 40%; incremental rates 33.33% and 15% throughout.

| Year | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Sales | 3,300.00 | 3,630.00 | 3,993.00 | 4,392.30 | 4,831.53 |
| EBIT | 550.00 | 580.80 | 618.92 | 658.85 | 700.57 |
| EBIT(1 - t) | 330.00 | 348.48 | 371.35 | 395.31 | 420.34 |
| Incremental FC | (100.00) | (110.00) | (121.00) | (133.10) | (146.41) |
| Incremental WC | (45.00) | (49.50) | (54.45) | (59.90) | (65.88) |
| FCFF | 185.00 | 188.98 | 195.90 | 202.31 | 208.05 |

FCFF grows slower than sales because the margin is eroding; the model can start from sales, NI, CFO or EBITDA (V5 p.154).
Python check: year 5 `4831.53*0.145*0.6-439.23*0.3333-439.23*0.15 = 208.06` (curriculum 208.05 by rounding). ^ex-05-03-9

### Example 10: finding FCFE from sales forecasts, Pitts 2021 (V5 p.155)

Setup: as Example 8, plus a net profit margin of 8% (240/3,000) and a 50% target debt ratio on incremental investments.

NI $= 0.08 \times 3{,}300 = 264$.
Net borrowing $= 0.50(100 + 45) = 72.50$.
FCFE $= 264 - 100 - 45 + 72.50 = 191.50$, or directly by Formula 15: $264 - 0.5(100) - 0.5(45) = 191.50$.
Python check: `264-0.5*145 = 191.5`. ^ex-05-03-10

### Example 11: the mistakes of using net income for FCFE and EBITDA for FCFF (V5 p.158)

Setup: a job applicant claims NI is the best FCFE measure and EBITDA the best FCFF measure.

Part 1: NI ignores the investments in fixed and working capital that reduce distributable cash and the net borrowing that increases it; NI equals FCFE only when new investment equals depreciation and WCInv and net borrowing are both zero (Formula 9; V5 p.158).
Part 2: EBITDA as FCFF ignores taxes, the depreciation tax shield, and the investments in fixed and working capital (Formula 12); from an equity perspective it additionally ignores after-tax interest and debt flows (V5 p.157, p.158).
Python check: with Pitts numbers EBITDA 800 versus FCFF 155, `800-155 = 645` of overstated "cash flow". ^ex-05-03-11

### Example 12: FCFF valuation with preferred stock, Welch Corporation (V5 p.159 to p.161)

Setup: bonds 400 at 8%, preferred 100 at 8%, common 500 at 12% (market values, millions); NI available to common 110, interest 32, preferred dividends 8, depreciation 40, FCInv 70, WCInv 20, net borrowing 25, tax 30%; FCFF grows 4.0%, FCFE 5.4%.

Part 1: $WACC = 0.4(8\%)(0.70) + 0.1(8\%) + 0.5(12\%) = 2.24 + 0.8 + 6.0 = 9.04\%$.
Part 2: $FCFF = 110 + 40 + 32(0.70) + 8 - 70 - 20 = 90.4$ (Formula 16).
Part 3: Firm value $= 90.4(1.04)/(0.0904 - 0.04) = 94.016/0.0504 = 1{,}865.4$; equity $= 1{,}865.4 - 400 - 100 = 1{,}365.4$.
Part 4: $FCFE = 110 + 40 - 70 - 20 + 25 = 85$ (preferred dividends stay out because NI already reflects them; net borrowing would include net new preferred issues).
Part 5: Equity value $= 85(1.054)/(0.12 - 0.054) = 89.59/0.066 = 1{,}357.42$.
The two approaches differ slightly (1,365.4 versus 1,357.4) because the growth and rate inputs are not forced to be mutually consistent.
Python check: `110+40+22.4+8-90 = 90.4`, `94.016/0.0504 = 1865.397`, `89.59/0.066 = 1357.424`. ^ex-05-03-12

### Example 13: real cash flows and discount rates for international stocks, Mukamba (V5 p.162, p.163)

Setup: normalized FCFE0 of CDF1,400 per share; real country return 7.30%, industry +0.80%, size -0.33%, leverage -0.12%; country real growth 3.0%, company 0.5% below.

$r_{real} = 7.30 + 0.80 - 0.33 - 0.12 = 7.65\%$; $g_{real} = 2.5\%$.
$V_0 = 1{,}400(1.025)/(0.0765 - 0.025) = 1{,}435/0.0515 = \text{CDF}27{,}864$ (Formula 17).
Python check: `1400*1.025/0.0515 = 27864.08`. ^ex-05-03-13

### Example 14: sensitivity analysis of an FCFE valuation, Petrobras (V5 p.163, p.164)

Setup: FCFE0 = BRL2.59, g = 7.0%, risk-free 8.9%, ERP 5.3%, beta 1.4.

Base case: $r = 8.9 + 1.4(5.3) = 16.32\%$; $V_0 = 2.59(1.07)/(0.1632 - 0.07) = 2.7713/0.0932 = \text{BRL}29.73$.

| Variable | Low | High | Value at low | Value at high |
|---|---|---|---|---|
| Beta | 1.2 | 1.6 | 33.55 | 26.70 |
| Risk-free rate | 7.9% | 9.9% | 33.31 | 26.85 |
| Equity risk premium | 4.3% | 6.3% | 34.99 | 25.85 |
| FCFE growth rate | 5.0% | 9.0% | 24.02 | 38.57 |

Value is inversely related to beta, the risk-free rate and the ERP, and positively related to growth; the growth-rate range (24.02 to 38.57) is the widest, so the valuation is most sensitive to g (V5 p.164).
Python check: `2.59*1.07/(0.089+1.4*0.053-0.07) = 29.73`, `2.59*1.09/(0.1632-0.09) = 38.57`, `2.59*1.05/(0.1632-0.05) = 24.02`. ^ex-05-03-14

### Example 15: two-stage FCFE with constant growth in each stage, TechnoSchaft (V5 p.166, p.167)

Setup: sales per share EUR25 at year 0; sales grow 20% for three years, 6% thereafter; net margin 10%; net FCInv 50% of the sales increase; WCInv 20% of the sales increase; debt finances 40% of net investment; beta 1.20, risk-free 7%, ERP 4.5%.

$r = 7\% + 1.2(4.5\%) = 12.4\%$.

| Year | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Sales | 30.000 | 36.000 | 43.200 | 45.792 | 48.540 | 51.452 |
| EPS | 3.000 | 3.600 | 4.320 | 4.579 | 4.854 | 5.145 |
| Net FCInv | 2.500 | 3.000 | 3.600 | 1.296 | 1.374 | 1.456 |
| WCInv | 1.000 | 1.200 | 1.440 | 0.518 | 0.550 | 0.582 |
| Debt financing | 1.400 | 1.680 | 2.016 | 0.726 | 0.769 | 0.815 |
| FCFE | 0.900 | 1.080 | 1.296 | 3.491 | 3.700 | 3.922 |

FCFE grows 20% in stage 1, then jumps 169% between years 3 and 4 because investment and its debt financing collapse when sales growth drops to 6%, then grows 6% (V5 p.167).
$TV_3 = 3.491/(0.124 - 0.06) = 54.55$.
$V_0 = 0.900/1.124 + 1.080/1.124^2 + 1.296/1.124^3 + 54.55/1.124^3 = 0.801 + 0.855 + 0.913 + 38.415 = \text{EUR}40.98$.
The PV of the terminal value is 38.415 of 40.98, almost 94% of value.
Python check: `3.4906/0.064 = 54.54`, `0.9/1.124+1.08/1.124**2+(1.296+54.5406)/1.124**3 = 40.976`. ^ex-05-03-15

### Example 16: two-stage FCFE with declining net income growth, Sindhuh Enterprises (V5 p.168, p.169)

Setup: EPS 2019 is $2.40; EPS growth 30%, 18%, 12%, 9%, 7% for 2020 to 2024, then 7%; net capex per share 3.00, 2.50, 2.00, 1.50, 1.00, then growing 7%; WCInv 50% of net capex; debt finances 30% of the total outlays; risk-free 6.0%, ERP 4.0%, beta 1.10.

$r = 6\% + 1.1(4\%) = 10.4\%$.

| Year | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---|---|---|---|---|
| EPS | 3.120 | 3.682 | 4.123 | 4.494 | 4.809 |
| Net FCInv | 3.000 | 2.500 | 2.000 | 1.500 | 1.000 |
| WCInv | 1.500 | 1.250 | 1.000 | 0.750 | 0.500 |
| Debt financing | 1.350 | 1.125 | 0.900 | 0.675 | 0.450 |
| FCFE | -0.030 | 1.057 | 2.023 | 2.919 | 3.759 |
| PV at 10.4% | -0.027 | 0.867 | 1.504 | 1.965 | |

FCFE is negative in 2020 because investment outruns earnings; the negative PV is simply included.
$V_{2023} = 3.759/(0.104 - 0.07) = 110.56$; PV $= 110.56/1.104^4 = 74.43$.
$V_{2019} = -0.027 + 0.867 + 1.504 + 1.965 + 74.43 = \$78.73$ per share.
Trailing P/E at the start of 2020: $78.73/2.40 = 32.8$; at the start of 2024: $110.56/4.494 = 24.6$; the multiple compresses as the high-growth phase ends (V5 p.169).
Python check: `3.759/0.034 = 110.56`, `-0.027+0.867+1.504+1.965+110.562/1.104**4 = 78.73`, `110.56/4.494 = 24.6`. ^ex-05-03-16

### Example 17: two-stage FCFE with declining sales growth, Medina Werks (V5 p.170, p.171)

Setup: current sales C$600 million; sales growth 20%, 16%, 12%, 10%, 8%, 7% and net margin 14%, 13%, 12%, 11%, 10.5%, 10% over years 1 to 6, then 7% and 10% forever; net capex 60% and WCInv 25% of the sales increase; debt finances 40%; beta 1.10, risk-free 6.0%, ERP 4.5%; 70 million shares.

$r = 6\% + 1.1(4.5\%) = 10.95\%$.

| Year | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Sales | 720.000 | 835.200 | 935.424 | 1,028.966 | 1,111.284 | 1,189.074 |
| Net profit | 100.800 | 108.576 | 112.251 | 113.186 | 116.685 | 118.907 |
| Net FCInv | 72.000 | 69.120 | 60.134 | 56.125 | 49.390 | 46.674 |
| WCInv | 30.000 | 28.800 | 25.056 | 23.386 | 20.579 | 19.447 |
| Debt financing | 40.800 | 39.168 | 34.076 | 31.804 | 27.988 | 26.449 |
| FCFE | 39.600 | 49.824 | 61.137 | 65.480 | 74.703 | 79.235 |
| PV at 10.95% | 35.692 | 40.475 | 44.763 | 43.211 | 44.433 | |

From year 6 everything is pegged to the 7% sales growth, so FCFE grows at 7%.
$TV_5 = 79.235/(0.1095 - 0.07) = \text{C\$}2{,}005.95$ million; PV $= 2{,}005.95/1.1095^5 = 1{,}193.12$.
Equity value $= 35.692 + 40.475 + 44.763 + 43.211 + 44.433 + 1{,}193.12 = \text{C\$}1{,}401.69$ million; per share $= 1{,}401.69/70 = \text{C\$}20.02$.
Python check: `79.235/0.0395 = 2005.95`, `2005.95/1.1095**5 = 1193.11`, `1401.69/70 = 20.02`. ^ex-05-03-17

### Example 18: three-stage FCFF with declining growth in stage 2, Reliant Home Furnishings (V5 p.172, p.173)

Setup: current FCFF $745 million; 309.39 million shares; beta 0.90, risk-free 5.04%, ERP 5.5%; cost of debt 7.1%; tax 34%; 20% debt, 80% equity; long-term debt $1.518 billion; FCFF growth 8.8% in years 1 to 4, then 7.4%, 6.0%, 4.6%, and 3.2% from year 8 on.

Part 1: $r = 5.04 + 0.9(5.5) = 9.99\%$; $WACC = 0.20(7.1)(0.66) + 0.80(9.99) = 8.93\%$.
Part 2: FCFF path 811, 882, 959, 1,044, 1,121, 1,188, 1,243, 1,283; PVs at 8.93% are 744, 743, 742, 741, 731, 711, 683, summing to $5,097 million.
$TV_7 = 1{,}283/(0.0893 - 0.032) = \$22{,}391$ million; PV $= 22{,}391/1.0893^7 = \$12{,}304$ million.
Firm value $= 5{,}097 + 12{,}304 = \$17{,}401$ million.
Part 3: equity $= 17{,}401 - 1{,}518 = \$15{,}883$ million.
Part 4: per share $= 15{,}883/309.39 = \$51.34$.
Python check: `745*1.088**4*1.074*1.06*1.046*1.032 = 1283.1`, `1283/0.0573 = 22391.8`, `(5097+12304-1518)/309.39 = 51.34`. ^ex-05-03-18

### Example 19: integrating ESG in a three-stage FCFF model, ACMC (V5 p.174 to p.179)

Setup: US copper miner at US$110 per share, buying a mine in a dry region; Dodd identifies government licensing delay (operations start in five years, not three), labor issues (compensation below peers, no safety link in executive pay), and underestimated water capex.
Stages: 2020 to 2024 pre-mine, 2025 to 2039 mine operating, 2040 on post-closure; revenue 1,000 in 2020 growing 2% to 2024; the mine adds 400 in 2025 growing 10% through 2031, then flat; total revenue grows 1% after 2039.
Financial assumptions: EBITDA 30% of revenue, tax 25%, FCInv 50% of EBITDA, depreciation 40% of capex, WCInv 10% of the revenue increase, pretax cost of debt 5%, risk-free 3%, beta 1.2, ERP 5%, debt ratio 50%; ESG add-ons are water capex of 10% of non-water capex and a 75 bp ESG equity risk premium.

Cost of debt $= 5\%(0.75) = 3.75\%$; cost of equity $= 3\% + 1.2(5\%) + 0.75\% = 9.75\%$; $WACC = 0.5(3.75\%) + 0.5(9.75\%) = 6.75\%$.
Each year FCFF $= EBITDA(1-t) + Dep(t) - FCInv - WCInv - \text{water FCInv}$, the EBITDA route of Formula 12; spot check 2020: $225.0 + 15.0 - 150.0 - 2.0 = 88.0$; 2025: $333.5 + 22.2 - 222.4 - 40.0 - 22.2 = 71.1$ (exhibit 71.2 by rounding).
PV of FCFF through 2035 is 1,178, PV of the perpetual FCFF from 2036 is 758, total 1,936; debt at the 50% ratio is 968; equity 968; per share $968/10 = \$97$.
Value 97 below price 110, so Dodd issues a sell; the ESG work lowered value through delay, extra capex and a higher discount rate (V5 p.177).
Python check: `0.5*0.05*0.75+0.5*(0.03+1.2*0.05+0.0075) = 0.0675`, `1000*0.3*0.75+0.4*150*0.25-150-2 = 88.0`. ^ex-05-03-19

## Item-set patterns

> [!warning] Trap 1: working capital investment that includes cash or notes payable
> The vignette's balance sheet shows changes in cash, receivables, inventory, payables, accruals, notes payable and long-term debt, and asks for FCFF.
> Correct: WCInv uses only operating items, receivables plus inventory minus payables minus accruals; cash is what is being explained and notes payable is interest-bearing financing (Pitts WCInv 45, LaForge 38, Holt 57).
> Distractors: including the change in cash, or treating the increase in notes payable as a working capital source instead of net borrowing (V5 p.132, p.133, p.145).

> [!warning] Trap 2: interest treatment by starting point
> The same question asks for FCFF from NI and from EBIT.
> Correct: add $Int(1-t)$ to NI or CFO; add nothing to EBIT or EBITDA, which sit above the interest line; forgetting the tax factor on the add-back is the classic wrong option.
> Distractors: adding full interest to NI (245 instead of 225 in the self-test), adding $Int(1-t)$ to EBIT as well, or forgetting the add-back entirely (V5 p.132, p.147).

> [!warning] Trap 3: the IFRS interest classification caveat
> The vignette says the statements are IFRS and interest paid is classified as a financing activity, then offers FCFF = CFO + Int(1 - t) - FCInv.
> Correct: when interest paid is not inside CFO, no add-back is made; FCFF = CFO - FCInv (and mind that IFRS dividends paid classified as operating must be added back to CFO).
> Distractors: mechanically adding after-tax interest, or assuming US GAAP treatment where interest paid is always operating (V5 p.135, p.137).

> [!warning] Trap 4: depreciation from EBIT versus from EBITDA
> Two starting points are offered with answer choices that mix $+ Dep$ and $+ Dep(t)$.
> Correct: from EBIT add the full depreciation; from EBITDA add only $Dep \times t$, the tax shield; both then subtract FCInv and WCInv.
> Distractors: adding full depreciation to EBITDA(1 - t) (overstates by $Dep(1-t)$, 337.5 versus 225 in the self-test), or adding the tax shield to the EBIT route (V5 p.147, p.148).

> [!warning] Trap 5: noncash charge direction
> A list of noncash transactions: a loss on an equipment sale, an intangibles impairment, a reversal of a restructuring charge.
> Correct: losses and impairments are added back; gains and reversals (income) are subtracted; deferred taxes are added back only if deferral is expected to continue indefinitely.
> Distractors: adding back the reversal, or subtracting the impairment; practice problem 8 tests exactly this triple (V5 p.138, p.139, p.203).

> [!warning] Trap 6: dividends, buybacks and leverage statements
> Two analyst statements: "share repurchases reduce FCFE" and "leverage changes do not affect FCFE".
> Correct: both are wrong; transactions with shareholders (dividends, repurchases, issues) are uses of free cash flow and do not change FCFF or FCFE, while a leverage increase leaves FCFF unchanged, raises FCFE by the new debt in the issue year, and lowers later FCFE through after-tax interest.
> Distractors: the symmetric-sounding versions of each statement; practice problem 35 answer is that neither statement is correct (V5 p.156, p.157, p.161, p.211).

> [!warning] Trap 7: net borrowing that misses one debt layer
> The balance sheet shows notes payable up 15 and long-term debt up 60.
> Correct: net borrowing is 75, both layers; with preferred stock, net new preferred issues also count; new borrowing enters FCFE positively even though it is a "liability".
> Distractors: using only long-term debt (60), or subtracting borrowing instead of adding (Holt FCFE 250 = 485 + 270 - 523 - 57 + 75) (V5 p.141, p.146, p.209).

> [!warning] Trap 8: the target debt ratio applied to the wrong side
> FCFE is forecast with a target DR of 30% and the option set contains NI minus DR times the net investment.
> Correct: FCFE = NI - (1 - DR)(FCInv - Dep) - (1 - DR)(WCInv); equity finances (1 - DR) of net new investment, and debt finances DR of it; also net capex means capex minus depreciation.
> Distractors: multiplying by DR instead of (1 - DR), or using gross capex without netting depreciation (V5 p.153, p.215).

> [!warning] Trap 9: terminal value timing and the stable-growth cash flow
> A two-stage build gives FCFE through year n and asks for value.
> Correct: $TV_n = FCFE_{n+1}/(r - g)$ with $FCFE_{n+1} = FCFE_n(1 + g_{stable})$, discounted n periods; if a P/E is given, $TV_n = P/E \times E_n$ with no further growth applied.
> Distractors: capitalizing $FCFE_n$ without one year of stable growth, discounting the terminal value n + 1 periods, or growing terminal earnings before applying the multiple (V5 p.165, p.167, p.201).

> [!warning] Trap 10: non-operating assets and preferred stock forgotten at the end
> The vignette mentions excess securities, investment land or a pension surplus, and a preferred class, then asks for equity value per share.
> Correct: firm value = value of operating assets + non-operating assets at market value; common equity = firm value - debt - preferred; only then divide by shares (Gothenburg 6.50, Bern scenario 2).
> Distractors: ignoring the non-operating assets, using book instead of market value for the investments, or forgetting to subtract preferred (V5 p.160, p.177, p.213, p.219).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM03-Free-Cash-Flow-Valuation-Practice-Problems]]

## Cross-links

- [[LM02-Discounted-Dividend-Valuation]]: supplies the DCF machinery this module reuses, the Gordon algebra behind every constant-growth stage, the terminal value logic, and the criteria (non-payer, dividends differ from capacity, control) that hand a valuation from dividends to free cash flow.
- [[LM04-Market-Based-Valuation-Price-and-Enterprise-Value-Multiples]]: the P/E-times-terminal-earnings alternative for terminal value comes from there, and this module's FCFF feeds the EV/EBITDA versus FCFF distinction and the justified multiples.
- [[LM05-Residual-Income-Valuation]]: the model of choice when expected free cash flows are negative within the forecast horizon, because it front-loads value recognition through book value; the three cash flow definitions compete for the same valuation job.
- [[LM06-Private-Company-Valuation]]: private-company income approaches discount normalized FCFF or FCFE built exactly as here, with the same WACC-versus-equity-rate matching and control considerations.
- [[LM06-Integration-of-Financial-Statement-Analysis-Techniques]]: the statement-level detective work, articulation problems, classification choices and quality-of-earnings flags, that decides whether reported CFO can be trusted as an FCFF starting point.
- [[LM02-Employee-Compensation-Post-Employment-and-Share-Based]]: the accounting behind the share-based compensation and pension items this module flags as noncash charges needing care, including the financing classification of option-exercise flows and the pension surplus treated as a non-operating asset.
- [[LM03-Cost-of-Capital-Advanced-Topics]]: builds the WACC and cost of equity that discount FCFF and FCFE here, including the build-up and country-adjustment logic mirrored in the real-terms international model.

## Self-test

Vignette A for Q1 to Q4: Kestrel Industrial reports under US GAAP.
For 2025: EBIT $500 million, interest expense $80 million, tax rate 25%, depreciation (the only noncash charge) $150 million, EBITDA $650 million.
Capital expenditures were $260 million; accounts receivable rose $45 million, inventory rose $30 million, accounts payable rose $25 million, accrued expenses rose $10 million, cash rose $12 million, notes payable rose $35 million, and long-term debt rose $55 million.

> [!question] Q1
> Kestrel's 2025 FCFF is closest to:
> A. $165 million.
> B. $225 million.
> C. $245 million.

> [!question] Q2
> Kestrel's 2025 FCFE is closest to:
> A. $165 million.
> B. $225 million.
> C. $255 million.

> [!question] Q3
> If Kestrel instead reported under IFRS and classified interest paid as a financing outflow, the correct FCFF calculation starting from the reported CFO would:
> A. still add interest times (1 minus the tax rate) to CFO.
> B. make no interest add-back to CFO.
> C. add the full interest paid to CFO.

> [!question] Q4
> Relative to the figures in Q1 and Q2, a further $100 million increase in accounts payable would:
> A. increase FCFF and FCFE by $100 million each.
> B. increase FCFF by $100 million and leave FCFE unchanged.
> C. leave both unchanged because payables are a financing item.

Vignette B for Q5 to Q7: Toivonen Oyj has current FCFF of EUR480 million and 400 million shares; the market value of debt is EUR2,400 million and the stock trades at EUR16.50.
The target capital structure is 30% debt and 70% equity, the pretax cost of debt is 6%, the tax rate is 20%, the cost of equity is 11%, and FCFF is expected to grow 4% forever.
For next year the analyst separately forecasts sales of EUR4,200 million, up EUR200 million, a net profit margin of 9%, incremental fixed capital investment of 40% of the sales increase, incremental working capital investment of 15% of the sales increase, and a 30% target debt ratio.

> [!question] Q5
> Toivonen's WACC is closest to:
> A. 7.60%.
> B. 9.14%.
> C. 9.50%.

> [!question] Q6
> The value per share from the single-stage FCFF model is closest to:
> A. 17.35.
> B. 18.28.
> C. 24.28.

> [!question] Q7
> The forecast FCFE for next year using the target-debt-ratio method is closest to:
> A. EUR268 million.
> B. EUR301 million.
> C. EUR345 million.

Vignette C for Q8 to Q10: Danae Marine has current FCFE of $2.00 per share, expected to grow 15% a year for three years and 5% a year thereafter; the required return on equity is 10%.
An associate proposes an alternative terminal value of 14 times year-3 EPS of $4.10.
A sensitivity table shows value ranges of $9.80 for the stable growth rate, $6.20 for the cost of equity, $3.10 for the stage-1 growth rate, and $2.40 for the base FCFE.

> [!question] Q8
> The value per share with a Gordon terminal value is closest to:
> A. 50.19.
> B. 52.27.
> C. 54.55.

> [!question] Q9
> The value per share using the earnings-multiple terminal value is closest to:
> A. 42.32.
> B. 49.69.
> C. 57.40.

> [!question] Q10
> Based on the sensitivity table, the valuation is most sensitive to the:
> A. stable growth rate.
> B. cost of equity.
> C. base-year FCFE.

> [!success]- Answer key
> Q1: B.
> WCInv $= 45 + 30 - 25 - 10 = 40$, excluding cash and notes payable; NI $= (500 - 80)(0.75) = 315$.
> $FCFF = 315 + 150 + 80(0.75) - 260 - 40 = 315 + 150 + 60 - 300 = 225$ (Python: `315+150+60-260-40 = 225`).
> Check from EBIT: $500(0.75) + 150 - 300 = 225$; from EBITDA: $650(0.75) + 150(0.25) - 300 = 225$.
> C adds full interest (245); A forgets the interest add-back (165) (V5 p.131, p.147).
>
> Q2: C.
> Net borrowing $= 35 + 55 = 90$; $FCFE = 225 - 60 + 90 = 255$ (Python: `225-60+90 = 255`).
> B is FCFF; A subtracts after-tax interest but forgets net borrowing (V5 p.141).
>
> Q3: B.
> When interest paid is classified as financing under IFRS, CFO was never reduced by interest, so no add-back is made; FCFF = CFO - FCInv.
> A is the US GAAP treatment; C double-counts by grossing up a CFO that already excludes interest (V5 p.135, p.137).
>
> Q4: A.
> A payables increase is a source of operating cash that reduces WCInv dollar for dollar, so both FCFF and FCFE rise by 100.
> C confuses trade payables with interest-bearing notes payable, which are excluded from working capital (V5 p.132, p.209).
>
> Q5: B.
> $WACC = 0.30(6\%)(0.80) + 0.70(11\%) = 1.44 + 7.70 = 9.14\%$ (Python: `0.3*6*0.8+0.7*11 = 9.14`).
> C skips the tax shield on debt (9.50%); A wrongly applies the tax factor to equity as well (7.60%) (V5 p.129).
>
> Q6: B.
> Firm value $= 480(1.04)/(0.0914 - 0.04) = 499.2/0.0514 = 9{,}712.1$; equity $= 9{,}712.1 - 2{,}400 = 7{,}312.1$; per share $= 7{,}312.1/400 = 18.28$ (Python: `(480*1.04/0.0514-2400)/400 = 18.28`).
> A forgets to grow FCFF (17.35); C forgets to subtract debt (24.28).
> At 16.50 the stock would look modestly undervalued (V5 p.129, p.130).
>
> Q7: B.
> NI $= 0.09(4{,}200) = 378$; incremental FCInv $= 0.40(200) = 80$; WCInv $= 0.15(200) = 30$.
> $FCFE = 378 - (1 - 0.30)(80 + 30) = 378 - 77 = 301$ (Python: `378-0.7*110 = 301`).
> A ignores debt financing (268); C multiplies by DR instead of (1 - DR) (345) (V5 p.153).
>
> Q8: C.
> $FCFE_1 = 2.30$, $FCFE_2 = 2.645$, $FCFE_3 = 3.0418$; $TV_3 = 3.0418(1.05)/(0.10 - 0.05) = 63.877$.
> $V_0 = 2.30/1.10 + 2.645/1.10^2 + (3.0418 + 63.877)/1.10^3 = 2.091 + 2.186 + 50.277 = 54.55$ (Python: `54.554`).
> B capitalizes $FCFE_3$ without the year of stable growth (52.27); A discounts the terminal value four periods (50.19) (V5 p.165).
>
> Q9: B.
> $TV_3 = 14 \times 4.10 = 57.40$; $V_0 = 2.091 + 2.186 + (3.0418 + 57.40)/1.331 = 49.69$ (Python: `2.0909+2.1859+60.4418/1.331 = 49.69`).
> C is the undiscounted terminal value; A applies the multiple to current rather than terminal EPS (V5 p.165, p.201).
>
> Q10: A.
> The widest value range, 9.80, belongs to the stable growth rate, consistent with Petrobras and McInish, where the growth input dominated.
> B is second; C has the narrowest range, though value scales one for one with the base FCFE (V5 p.163, p.164, p.217).

## Flashcards

#flashcards/cfa-l2/05-Equity-Valuation/lm03

FCFF in one line::Cash flow available to all suppliers of capital after operating expenses including taxes and after necessary investments in working and fixed capital (V5 p.127).
FCFE in one line::Cash flow available to common shareholders after operating expenses, interest, principal payments and necessary investments, equal to what the company could pay as dividends (V5 p.127, p.142).
Four conditions favoring free cash flow over dividends::No dividends; dividends differ significantly from capacity to pay; free cash flows align with profitability within the forecast horizon; investor takes a control perspective (V5 p.126).
Ownership perspective implicit in FCFE::Control; with control comes discretion over the uses of free cash flow, so FCFE measures what the owner could extract (V5 p.126, p.156).
Discount rate for FCFF and for FCFE::FCFF at WACC to get firm value; FCFE at the required return on equity to get equity value directly (V5 p.128, p.129).
When is FCFF preferred over FCFE?::Levered company with negative FCFE, or a changing capital structure where FCFF growth reflects fundamentals and WACC is less leverage-sensitive than the cost of equity (V5 p.128).
FCFF from net income::NI + NCC + Int(1 - Tax rate) - FCInv - WCInv (V5 p.131).
FCFF from CFO::CFO + Int(1 - Tax rate) - FCInv; no NCC or WCInv terms because CFO already includes them (V5 p.135).
FCFF from EBIT::EBIT(1 - Tax rate) + Dep - FCInv - WCInv (V5 p.147).
FCFF from EBITDA::EBITDA(1 - Tax rate) + Dep(Tax rate) - FCInv - WCInv; only the depreciation tax shield returns (V5 p.147).
FCFE from FCFF::FCFF - Int(1 - Tax rate) + Net borrowing (V5 p.141).
FCFE from net income::NI + NCC - FCInv - WCInv + Net borrowing (V5 p.142).
FCFE from CFO::CFO - FCInv + Net borrowing (V5 p.142).
Why is after-tax interest added back to NI for FCFF?::Interest net of its tax saving was deducted from income but is cash to debtholders, and after-tax FCFF must match the after-tax WACC (V5 p.132).
Working capital for free cash flow excludes which items?::Cash and equivalents (the change in cash is what is being explained) and notes payable plus the current portion of long-term debt (financing items) (V5 p.132, p.133).
Micro-problem: NI 100, Dep 30, Int 20, tax 30%, FCInv 40, WCInv 10; FCFF?::100 + 30 + 14 - 40 - 10 = 94; keystrokes 20 × 0.7 = + 100 + 30 - 40 - 10 = (V5 p.131).
Micro-problem: same firm, net borrowing 25; FCFE?::94 - 14 + 25 = 105, or 100 + 30 - 40 - 10 + 25 = 105 (V5 p.141, p.142).
IFRS interest classification caveat for FCFF from CFO::If interest paid is classified as financing rather than operating, CFO was never reduced by it, so no after-tax interest add-back is made (V5 p.135, p.137).
IFRS dividends paid classified as operating require what fix?::Add them back to CFO, because dividends are a use of free cash flow, not a determinant (V5 p.137).
Noncash items subtracted (not added) in the NCC adjustment::Gains on asset sales and non-operating activity, restructuring charge reversals, amortization of bond premium (V5 p.138).
Noncash items added back in the NCC adjustment::Depreciation, amortization and impairment of intangibles, restructuring charge expense, bond discount amortization, losses on sales (V5 p.138).
When should deferred taxes be added back to income for FCF purposes?::Only if the company is expected to keep deferring taxes indefinitely; not if the differences reverse in the near future (V5 p.138).
Treatment of preferred dividends when computing FCFF from NI available to common::Add them back with no tax adjustment; in FCFE net borrowing, include net new preferred issuance (V5 p.159, p.160).
Effect of a $100 increase in depreciation on FCFF at a 40% tax rate::+$40, the tax shield only; income falls 60 after tax and 100 is added back (V5 p.140, p.209).
Effect of a $100 increase in interest expense on FCFF and FCFE (40% tax)::FCFF unchanged (the add-back cancels it); FCFE falls by 60 (V5 p.209).
Effect of a $100 increase in notes payable on FCFF and FCFE::FCFF unchanged; FCFE rises 100 through net borrowing (V5 p.209).
Effect of dividends, share repurchases and share issues on FCFF and FCFE::None; they are uses of free cash flow, not determinants (V5 p.156, p.157, p.161).
How does a leverage increase affect FCFE?::Raises FCFE by the debt issued in that year, lowers future FCFE by the after-tax interest; FCFF is unaffected (V5 p.161).
Uses of FCFF identity::Increase in cash balances plus after-tax interest plus net debt repayment plus dividends plus net share repurchases; must equal sources (V5 p.149, p.150).
Uses of FCFE identity::Increase in cash balances plus dividends plus net share repurchases (V5 p.150).
Incremental fixed capital rate in sales-based forecasting::(Capital expenditures minus depreciation) divided by the increase in sales (V5 p.152).
FCFE with a target debt ratio::NI - (1 - DR)(FCInv - Dep) - (1 - DR)(WCInv); debt finances DR of net new investment, so borrowing needs no separate forecast (V5 p.153).
Key assumption behind the sales-based FCFE shortcut::Depreciation is the only noncash charge; large other noncash charges make it inaccurate (Company A trap) (V5 p.153, p.205).
Micro-problem: NI 200, FCInv - Dep 60, WCInv 20, DR 25%; FCFE?::200 - 0.75 × 80 = 140; keystrokes 60 + 20 = × 0.75 = then 200 - 60 = (V5 p.153).
When do NI and FCFE coincide?::New investment equals depreciation, and WCInv and net borrowing are both zero (V5 p.158).
Four defects of EBITDA as an FCFF proxy::Pre-tax measure; ignores the depreciation tax shield; ignores FCInv and WCInv; from the equity view also ignores capital structure and debt flows (V5 p.157, p.158).
Why do FCFE and dividends usually differ despite the same drivers?::Boards manage dividends, raising them gradually and avoiding cuts, so dividends are smoother than the residual FCFE (V5 p.142).
When do DDM and FCFE values agree?::When FCFE equals dividends each year, or when all inputs are known and mutually consistent (V5 p.157).
Real-terms single-stage FCFE model inputs::Build-up real required return (country return plus industry, size and leverage adjustments) and a real growth rate benchmarked to the country's real growth (V5 p.162).
Micro-problem: FCFE0 1,000, real r 8%, real g 3%; value?::1,000 × 1.03/0.05 = 20,600 (V5 p.162).
Sensitivity analysis procedure in FCF valuation::Recompute value with the low and the high estimate of one input at a time, holding others at base case, and compare the value ranges (V5 p.163).
Which inputs usually dominate FCF valuation sensitivity?::The FCFE or FCFF growth rate and the cost of equity; the base-year FCF scales value proportionally (V5 p.163, p.164, p.212).
Two patterns for stage 1 of a two-stage FCF model::Constant supernormal growth that drops abruptly, or growth declining through stage 1 to the sustainable rate (the H-model analogue) (V5 p.164, p.165).
In FCF models, "growth rate" can refer to what three things?::Sales, income (net or operating), or FCFF and FCFE themselves; the vignette must be read for which (V5 p.165).
Why can FCFE jump when sales growth slows?::Profits keep growing while investment needs and the debt financed against them collapse, TechnoSchaft's FCFE rose 169% between years 3 and 4 (V5 p.167).
Two-stage FCFF terminal value::TV_n = FCFF_{n+1}/(WACC - g), located at t = n and discounted n periods (V5 p.165).
Terminal value by multiple::TV_n = trailing P/E times forecast terminal earnings E_n, as with NYL's 18 times 2025 EPS (V5 p.165, p.201).
Typical share of total value contributed by the terminal value::A substantial majority, about 94% for TechnoSchaft and 78% for QuickChange (V5 p.167, p.219).
How are non-operating assets handled in FCF valuation?::Valued separately at market value (excess cash, securities, investment land, pension surplus) and added to the value of operating assets (V5 p.177, p.219).
Micro-problem: operating assets 900, excess securities 50, pension surplus 30, debt 400, 100 shares; per share?::(900 + 50 + 30 - 400)/100 = 5.80 (V5 p.177, p.219).
Two ways to integrate ESG in an FCF model::Quantify the cash flow effects directly (delayed opening, extra capex), and add a risk premium to the cost of equity for material but hard-to-quantify issues (V5 p.174, p.176).
Why is base-year FCF normalization critical?::Value scales proportionately with FCFF0 or FCFE0, so non-recurring items or unsustainable working capital swings distort the whole valuation (V5 p.139, p.163).
Trap answer on the statement "leverage changes do not affect FCFE"::False; new borrowing raises current FCFE and after-tax interest lowers future FCFE (V5 p.161, p.211).
Trap answer on the statement "buybacks affect free cash flow"::False; transactions with shareholders are uses of free cash flow (V5 p.157, p.211).
{{FCFF from EBITDA adds only Dep times the tax rate}}, while FCFF from EBIT adds the full depreciation (V5 p.147).
{{Net borrowing includes notes payable and long-term debt}} (and net new preferred), issued minus repaid (V5 p.141, p.146).
Micro-problem: EBITDA 400, Dep 100, tax 30%, FCInv 120, WCInv 30; FCFF?::400 × 0.7 + 100 × 0.3 - 120 - 30 = 160; keystrokes 400 × 0.7 = STO 1, 100 × 0.3 = + RCL 1 - 120 - 30 = (V5 p.147).
Micro-problem: FCFF0 90, WACC 9%, g 4%, debt 500, preferred 100, 50 shares; value per share?::90 × 1.04/0.05 = 1,872; (1,872 - 500 - 100)/50 = 25.44 (V5 p.129, p.160).

## Common mistakes

1. Including the change in cash or in notes payable inside WCInv; working capital for valuation excludes cash, equivalents, notes payable and the current portion of long-term debt (V5 p.132, p.133).
2. Forgetting the (1 - Tax rate) on the interest add-back, or adding interest back when starting from EBIT or EBITDA, which already sit above the interest line (V5 p.132, p.147).
3. Adding after-tax interest to CFO when the IFRS filer classified interest paid as financing; the add-back applies only when interest ran through operating cash flow (V5 p.135, p.137).
4. Adding full depreciation to the EBITDA route; from EBITDA only Dep times the tax rate returns, and mixing the EBIT and EBITDA templates is the most reliable distractor pair (V5 p.147, p.148).
5. Reversing the direction of gain and loss adjustments: gains and restructuring reversals are subtracted, losses and impairments added (V5 p.138, p.203).
6. Treating dividends or share repurchases as determinants of free cash flow, or denying that leverage changes affect FCFE (V5 p.156, p.157, p.161, p.211).
7. Missing a layer of net borrowing, notes payable plus long-term debt plus net new preferred, or subtracting borrowing instead of adding it in FCFE (V5 p.141, p.146, p.209).
8. Applying DR instead of (1 - DR) in the target-debt-ratio FCFE formula, or using gross capex instead of capex net of depreciation (V5 p.153, p.215).
9. Using the sales-based shortcut for a company with significant noncash charges other than depreciation, where it misestimates FCFE (V5 p.153, p.155, p.205).
10. Building the terminal value from the last explicit-year cash flow without one year of stable growth, or discounting the terminal value one period too many (V5 p.165, p.167).
11. Growing terminal earnings before applying a terminal P/E, or applying the multiple to FCFE instead of earnings (V5 p.201, p.219).
12. Forgetting to subtract preferred stock as well as debt from firm value, or to add non-operating assets (at market, not book, value) before subtracting claims (V5 p.160, p.177, p.219).
13. Using NI as an FCFE proxy or EBITDA as an FCFF proxy; each systematically misstates value, and EBITDA over a bond rate compounds four separate errors (V5 p.158, p.215).
14. Treating working capital squeezes (falling inventory, stretched payables) as sustainable free cash flow growth; they hit a floor and reverse for a growing company (V5 p.141, p.209).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "05-03" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
