---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 3
title: "Harrowgate Components: Rebuilding Free Cash Flow from the Filings"
los: [los-05-03-a, los-05-03-c, los-05-03-d, los-05-03-f, los-05-03-h]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Harrowgate Components: Rebuilding Free Cash Flow from the Filings

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Owen Maddox, CFA, is an equity analyst at Brightwater Securities covering industrial suppliers.
He is preparing an initiation report on Harrowgate Components Inc., a US manufacturer of hydraulic valves and actuators that reports under US GAAP.
Harrowgate's tax rate is 25%, and all figures are in USD millions.

During 2025 Harrowgate sold surplus machining equipment with a carrying amount of 16 for cash proceeds of 40.
The resulting gain is reported in other income, below operating income.
Depreciation is the company's only other noncash charge.

Exhibit 1: Harrowgate income statement data, 2025 (USD millions)

| Item | 2025 |
|---|---|
| Revenue | 4,800 |
| EBITDA | 910 |
| Depreciation | 260 |
| EBIT | 650 |
| Gain on sale of equipment | 24 |
| Interest expense | 90 |
| Income before tax | 584 |
| Income tax expense (25%) | 146 |
| Net income | 438 |

Exhibit 2: Harrowgate balance sheet changes and other cash items, 2025 (USD millions)

| Item | Amount |
|---|---|
| Increase in cash and equivalents | 18 |
| Increase in accounts receivable | 55 |
| Increase in inventories | 40 |
| Increase in accounts payable | 22 |
| Increase in accrued liabilities | 8 |
| Increase in notes payable | 30 |
| Increase in long-term debt | 50 |
| Capital expenditures | 400 |
| Proceeds from sale of equipment | 40 |
| Dividends paid | 150 |
| Share repurchases | 161 |

Maddox also reviews Voss AG, a German competitor that reports under IFRS.
Voss's 2025 cash flow from operations is EUR 612 million.
Voss classifies interest paid of EUR 90 million as a financing cash outflow and dividends paid of EUR 70 million as an operating cash outflow, so its reported operating cash flow is after dividends and before interest.
Voss's capital expenditures were EUR 380 million, and its tax rate is also 25%.

Maddox discusses his draft with Dana Whitcombe, a senior associate on the team.
Whitcombe makes the following statement:

"Management told us that next year's capital expenditures will be almost exactly equal to depreciation. In that case Harrowgate's net income will be a good proxy for its FCFE, and you can simplify the model."

Maddox then reads the minutes of Harrowgate's most recent investor day.
The chief financial officer announced a three-year plan to raise the company's debt-to-capital ratio from 25% to 45%.
The first step is a USD 300 million issue of long-term notes on the last business day of 2026, with the entire proceeds used on the same day to repurchase common shares.
Further debt-funded repurchases are expected in 2027 and 2028, and the timing will depend on market conditions.

Maddox must decide whether to value Harrowgate by discounting FCFF or FCFE.
He notes that Harrowgate has never had negative FCFE and that its operating margins have been stable for five years.

## Questions

1. Harrowgate's 2025 FCFF is closest to: (LOS: los-05-03-d)
   - A. USD 316.5 million.
   - B. USD 339.0 million.
   - C. USD 364.5 million.
2. Harrowgate's 2025 FCFE is closest to: (LOS: los-05-03-d)
   - A. USD 299.0 million.
   - B. USD 329.0 million.
   - C. USD 396.5 million.
3. Based on its reported cash flow from operations, Voss's 2025 FCFF is closest to: (LOS: los-05-03-c)
   - A. EUR 232.0 million.
   - B. EUR 302.0 million.
   - C. EUR 369.5 million.
4. Holding operating results constant, the effect of the planned 2026 note issue and repurchase on Harrowgate's 2026 free cash flow is most likely that: (LOS: los-05-03-f)
   - A. FCFF and FCFE are both unchanged.
   - B. FCFF is unchanged, and FCFE is higher by USD 300 million.
   - C. FCFF and FCFE are each higher by USD 300 million.
5. Whitcombe's statement is best described as: (LOS: los-05-03-h)
   - A. correct.
   - B. incorrect, because net income also omits the investment in working capital and net borrowing.
   - C. incorrect, because net income omits the after-tax interest that is added back to reach FCFE.
6. Given the investor day announcement, the approach Maddox should most likely use to value Harrowgate's equity is: (LOS: los-05-03-a)
   - A. FCFE discounted at the required return on equity, because it is the more direct approach.
   - B. FCFF discounted at WACC, because the capital structure is expected to change.
   - C. FCFE discounted at WACC, because WACC is less sensitive than the cost of equity to changes in leverage.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** $FCFF = NI + NCC + Int(1-t) - FCInv - WCInv$.
> Net noncash charges are depreciation less the gain: $260 - 24 = 236$; the gain raised net income, but the cash came in through investing.
> After-tax interest $= 90(1 - 0.25) = 67.5$.
> FCInv is capital expenditures net of proceeds: $400 - 40 = 360$.
> WCInv uses operating items only, excluding cash and notes payable: $55 + 40 - 22 - 8 = 65$.
> $FCFF = 438 + 260 - 24 + 67.5 - 360 - 65 = 316.5$.
> B is wrong because it adds back the full interest of 90 instead of $90(0.75)$: $438 + 236 + 90 - 425 = 339.0$.
> C is wrong because it adds the gain back instead of subtracting it: $438 + 260 + 24 + 67.5 - 425 = 364.5$.
> 2. **B.** Net borrowing counts both debt layers: $30 + 50 = 80$.
> $FCFE = FCFF - Int(1-t) + \text{Net borrowing} = 316.5 - 67.5 + 80 = 329.0$.
> Check from net income: $438 + 260 - 24 - 360 - 65 + 80 = 329.0$.
> Check from uses: $\Delta \text{Cash} + \text{Dividends} + \text{Repurchases} = 18 + 150 + 161 = 329.0$.
> A is wrong because it counts only the long-term debt increase as borrowing: $316.5 - 67.5 + 50 = 299.0$.
> C is wrong because it adds net borrowing to FCFF without removing after-tax interest: $316.5 + 80 = 396.5$.
> 3. **B.** Under IFRS the starting CFO must be adjusted to reflect the company's classification choices.
> Interest paid is in financing, so CFO was never reduced by it and no after-tax interest add-back is made.
> Dividends paid were deducted inside CFO, and dividends are a use of free cash flow rather than a determinant, so they are added back.
> $FCFF = CFO + \text{Dividends in CFO} - FCInv = 612 + 70 - 380 = 302.0$.
> A is wrong because it ignores the dividend classification: $612 - 380 = 232.0$.
> C is wrong because it also adds after-tax interest as if interest were in CFO under US GAAP: $612 + 70 + 90(0.75) - 380 = 369.5$.
> 4. **B.** New borrowing leaves FCFF unchanged, because FCFF is before all financing flows.
> Net borrowing of 300 raises 2026 FCFE by 300; because the notes are issued on the last business day, no 2026 interest reduces FCFE, although after-tax interest will reduce FCFE from 2027.
> The repurchase is a use of FCFE, not a determinant of it, so it does not offset the borrowing.
> A is wrong because it treats the repurchase as reducing FCFE.
> C is wrong because it treats net borrowing as a component of FCFF.
> 5. **B.** $FCFE = NI + NCC - FCInv - WCInv + \text{Net borrowing}$.
> Capital expenditures equal to depreciation makes only the fixed-capital terms cancel; net income equals FCFE only if WCInv and net borrowing are also zero.
> Harrowgate's 2025 WCInv was 65 and net borrowing was 80, and the company plans large debt issues, so neither term is likely to be zero.
> A is wrong for that reason.
> C is wrong because after-tax interest is added back to reach FCFF, not FCFE; FCFE is already after interest.
> 6. **B.** FCFF is preferred when the capital structure is changing, because FCFF growth reflects fundamentals while FCFE growth is distorted by fluctuating net borrowing, and WACC is less sensitive to leverage than the cost of equity.
> A is wrong because the direct FCFE approach is preferred only when the capital structure is stable.
> C is wrong because it mismatches the cash flow and the discount rate; FCFE belongs to equity and must be discounted at the required return on equity.

## Distractor design

1. B: full interest added instead of $Int(1-t)$ (before-tax vs after-tax); C: gain added back instead of subtracted (sign of noncash item).
2. A: notes payable omitted from net borrowing (missed debt layer); C: FCFF-to-FCFE conversion without subtracting after-tax interest (wrong formula variant).
3. A: IFRS dividends-in-operating classification ignored (IFRS vs US GAAP); C: interest add-back applied as if US GAAP (IFRS vs US GAAP).
4. A: repurchase treated as reducing FCFE (use vs determinant); C: borrowing put into FCFF (firm vs equity perspective).
5. A: fixed-capital cancellation mistaken for full equivalence (wrong formula variant); C: FCFF adjustment applied to FCFE (firm vs equity perspective).
6. A: stable-structure rule applied to a changing structure (misread exhibit); C: cash flow and discount rate mismatched (wrong formula variant).
