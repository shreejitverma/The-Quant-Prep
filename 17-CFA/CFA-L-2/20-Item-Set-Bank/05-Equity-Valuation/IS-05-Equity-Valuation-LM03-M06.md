---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 3
title: "Castellan Specialty Glass: Building FCFF from Sales"
los: [los-05-03-e, los-05-03-i, los-05-03-k, los-05-03-l]
difficulty: 4
minutes: 12
source: mock-06
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Castellan Specialty Glass: Building FCFF from Sales

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tomas Reyes, CFA, is a senior analyst at Northgate Pension Trust, which holds listed industrial equities for the long term.
He is valuing Castellan Specialty Glass Inc., a US maker of coated architectural glass and display substrates, whose shares trade at USD 56.00.
Castellan has 100 million shares outstanding, and all company figures are in USD millions.

Reyes values Castellan with a two-stage FCFF model driven by sales.
He estimates the incremental fixed capital investment rate (capital expenditures minus depreciation, per dollar of sales increase) and the incremental working capital investment rate from the 2025 relationship between investment and the increase in sales.
He applies both rates to the increase in sales in every forecast year, including the stable-growth years.

Exhibit 1: Castellan operating data (USD millions)

| Item | 2024 | 2025 |
|---|---|---|
| Sales | 2,400 | 2,700 |
| EBITDA | | 645 |
| Depreciation | | 240 |
| EBIT | | 405 |
| Capital expenditures | | 390 |

Exhibit 2: Castellan balance sheet changes, 2025 (USD millions)

| Item | Change |
|---|---|
| Cash and equivalents | +30 |
| Accounts receivable | +48 |
| Inventories | +36 |
| Accounts payable | +21 |
| Notes payable | +25 |
| Long-term debt | +40 |

Reyes forecasts sales growth of 12% a year for 2026, 2027 and 2028 as new float lines for solar and display glass ramp up.
From 2029 onward sales grow at 4% a year indefinitely.
The EBIT margin stays at its 2025 level of 15% throughout, and the tax rate is 25%.

Exhibit 3: Castellan capital and non-operating data

| Item | Value |
|---|---|
| Risk-free rate | 3.5% |
| Equity beta | 1.25 |
| Equity risk premium | 5.0% |
| Pretax cost of debt | 6.0% |
| Target weights: debt, equity | 30%, 70% |
| Debt, market value | USD 1,150 million |
| Debt, book value | USD 1,300 million |
| 20% stake in Ardent Float Glass, a listed company: carrying amount | USD 70 million |
| 20% stake in Ardent Float Glass: market value | USD 180 million |

Castellan's operating forecast excludes its stake in Ardent, which contributes nothing to Castellan's operating cash flow.
Reyes values Castellan's operating assets at the end of 2025, discounts at WACC with the cost of equity from the CAPM, and places the terminal value at the end of 2028.
Northgate's policy is to hold a stock whose estimated value exceeds its market price and to reduce the position otherwise.

Northgate's risk committee then asks Reyes for a sensitivity test.
Castellan's furnaces are gas-fired, and the committee believes carbon transition risk is material but too uncertain to model in the cash flows.
The committee asks Reyes to add a 0.90 percentage point ESG risk premium to the cost of equity, holding the cash flow forecast, the capital structure weights, the growth rates and every other input at their base-case values.

## Questions

1. Castellan's forecast FCFF for 2029 is closest to: (LOS: los-05-03-e)
   - A. USD 320.91 million.
   - B. USD 336.09 million.
   - C. USD 348.73 million.
2. The value of Castellan's operating assets at the end of 2025 is closest to: (LOS: los-05-03-k)
   - A. USD 3,035.73 million.
   - B. USD 6,195.22 million.
   - C. USD 6,675.81 million.
3. Reyes's base-case value per share and the action consistent with Northgate's policy are closest to: (LOS: los-05-03-l)
   - A. USD 57.06; hold the stock.
   - B. USD 55.26; reduce the position.
   - C. USD 55.56; reduce the position.
4. After the risk committee's ESG adjustment, Castellan's value per share is closest to: (LOS: los-05-03-i)
   - A. USD 44.44.
   - B. USD 47.73.
   - C. USD 55.92.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Incremental fixed capital rate $= (390 - 240)/(2{,}700 - 2{,}400) = 150/300 = 50\%$.
> Incremental working capital rate uses operating items only, excluding cash and notes payable: $(48 + 36 - 21)/300 = 63/300 = 21\%$.
> Sales: 2026 3,024.0000; 2027 3,386.8800; 2028 3,793.3056; 2029 $3{,}793.3056(1.04) = 3{,}945.0378$, an increase of 151.7322.
> 2029: $EBIT(1-t) = 0.15(3{,}945.0378)(0.75) = 443.8168$; net FCInv $= 0.50(151.7322) = 75.8661$; WCInv $= 0.21(151.7322) = 31.8638$.
> $FCFF_{2029} = 443.8168 - 75.8661 - 31.8638 = 336.0869$.
> Investment falls sharply in 2029 because sales grow by 151.73 instead of 406.43, while operating profit keeps rising.
> A is wrong because it includes the increase in cash in working capital: rate $= (48 + 36 + 30 - 21)/300 = 31\%$ and $443.8168 - 0.81(151.7322) = 320.9137$.
> C is wrong because it nets the increase in notes payable against working capital as if it were an operating liability: rate $= (48 + 36 - 21 - 25)/300 = 12.6667\%$ and $443.8168 - 0.626667(151.7322) = 348.7312$.
> 2. **C.** Cost of equity $= 3.5\% + 1.25(5.0\%) = 9.75\%$; $WACC = 0.30(6.0\%)(0.75) + 0.70(9.75\%) = 1.35\% + 6.825\% = 8.175\%$.
> FCFF: 2026 $340.2000 - 0.71(324.0000) = 110.1600$; 2027 $381.0240 - 0.71(362.8800) = 123.3792$; 2028 $426.7469 - 0.71(406.4256) = 138.1847$.
> PV of 2026 to 2028 $= 101.8350 + 105.4358 + 109.1640 = 316.4348$.
> From 2030 both EBIT and the sales increase grow at 4%, so FCFF grows at 4% from 2029 and $TV_{2028} = FCFF_{2029}/(WACC - g) = 336.0869/(0.08175 - 0.04) = 8{,}049.9851$.
> PV of the terminal value $= 8{,}049.9851/1.08175^3 = 6{,}359.3739$, about 95% of the total.
> Operating assets $= 316.4348 + 6{,}359.3739 = 6{,}675.8087$.
> A is wrong because it builds the terminal value from 2028 FCFF grown at 4% ($138.1847 \times 1.04 = 143.7121$), ignoring the fall in investment when growth slows: $316.4348 + (143.7121/0.04175)/1.08175^3 = 3{,}035.7285$.
> B is wrong because it discounts the terminal value four periods instead of three: $316.4348 + 8{,}049.9851/1.08175^4 = 6{,}195.2181$.
> 3. **A.** Firm value adds the non-operating stake at market value: $6{,}675.8087 + 180 = 6{,}855.8087$.
> Equity $= 6{,}855.8087 - 1{,}150 = 5{,}705.8087$, using the market value of debt; per share $= 57.06$.
> Value exceeds the USD 56.00 price, so the policy says hold.
> B is wrong because it omits the Ardent stake: $(6{,}675.8087 - 1{,}150)/100 = 55.26$, which reverses the action.
> C is wrong because it deducts debt at book value: $(6{,}855.8087 - 1{,}300)/100 = 55.56$, which also reverses the action.
> 4. **B.** Revised cost of equity $= 9.75\% + 0.90\% = 10.65\%$; $WACC = 1.35\% + 0.70(10.65\%) = 8.805\%$, up only 63 bp because equity carries a 70% weight.
> PV of 2026 to 2028 $= 101.2453 + 104.2184 + 107.2787 = 312.7424$.
> $TV_{2028} = 336.0869/(0.08805 - 0.04) = 6{,}994.5240$; PV $= 6{,}994.5240/1.08805^3 = 5{,}430.1472$.
> Operating assets $= 5{,}742.8896$; per share $= (5{,}742.8896 + 180 - 1{,}150)/100 = 47.73$, a fall of 9.33 that takes value well below the price.
> Almost all of the change comes through the terminal value, whose denominator falls from 4.175% to 4.805%.
> A is wrong because it adds the full 0.90 percentage points to WACC instead of to the cost of equity: $WACC = 9.075\%$, operating assets $= 5{,}414.3495$, and per share $= 44.44$.
> C is wrong because it applies the new WACC to the discount factors but leaves the base terminal value of 8,049.9851 unchanged: operating assets $= 312.7424 + 8{,}049.9851/1.08805^3 = 6{,}562.2890$, and per share $= 55.92$.

## Distractor design

1. A: increase in cash included in working capital investment (misread exhibit); C: notes payable treated as an operating liability instead of financing (wrong formula variant).
2. A: terminal cash flow set to $FCFF_n(1 + g)$ instead of the forecast $FCFF_{n+1}$, ignoring the investment drop (period error); B: terminal value discounted $n + 1$ periods (period error).
3. B: non-operating asset omitted (misread exhibit), which flips the action; C: book instead of market value of debt deducted (book vs market).
4. A: equity premium added to WACC without the equity weight (wrong formula variant); C: discount rate changed in the discount factors but not in the terminal value denominator (partial recomputation).
