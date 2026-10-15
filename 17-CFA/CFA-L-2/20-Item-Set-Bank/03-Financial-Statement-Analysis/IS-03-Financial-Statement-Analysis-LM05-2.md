---
type: cfa-itemset
topic: "Financial Statement Analysis"
topic_code: "03"
topic_slug: "03-Financial-Statement-Analysis"
lm: 5
title: "Maplewood Home Appliances: Receivables, Bill-and-Hold, and Persistence"
los: [los-03-05-b, los-03-05-e, los-03-05-f, los-03-05-g, los-03-05-h]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/financial-statement-analysis]
---

# Maplewood Home Appliances: Receivables, Bill-and-Hold, and Persistence

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Tomas Reyes, CFA, is an equity analyst at Larchmont Securities.
He is updating his earnings forecast and valuation of Maplewood Home Appliances Inc., a US distributor of small kitchen appliances to regional retail chains.
Maplewood reports under US GAAP with a December year end, and all amounts are in $ millions.

Maplewood's 2025 revenue growth of 18.1% was well above the 6% reported by its closest peers.
Reyes gathers the receivables data in Exhibit 1.

Exhibit 1: Maplewood revenue and receivables ($ millions)

| Item | 2023 | 2024 | 2025 |
|---|---|---|---|
| Revenue | 1,420.0 | 1,512.0 | 1,786.0 |
| Gross accounts receivable | 248.5 | 262.1 | 318.4 |

A liquidity note discloses that in December 2025 Maplewood sold $72.0 million of trade receivables to a factor without recourse and derecognized them.
No receivables were sold in earlier years.

The revenue recognition note states that 4% of 2025 revenue came from bill-and-hold arrangements under which customers were invoiced but Maplewood retained the goods in its warehouses.
Maplewood's 2025 gross margin was 26.5% and its effective tax rate was 24%.

A separate disclosure explains that in the fourth quarter of 2025 Maplewood shipped a promotional volume of countertop ovens to three distributors, granting them an unconditional right to return unsold units through April 2026, and recognized the full amount as revenue on shipment.

Exhibit 2 summarizes the 2025 income statement items below gross profit that Reyes considers relevant.

Exhibit 2: Selected 2025 income statement items ($ millions)

| Item | Amount | Note |
|---|---|---|
| Pre-tax income from continuing operations | 127.4 | As reported |
| Restructuring charge (included above) | 18.6 | First restructuring charge in ten years |
| Gain on sale of warehouse (included above) | 22.3 | One-time disposal |
| Other non-operating expense (included above) | 9.7 | Currency and bank fees; incurred every year |
| Earnings from continuing operations | 96.8 | After tax |

To forecast 2026 earnings, Reyes uses a persistence regression estimated by his firm's quantitative team on a panel of appliance distributors:

$$
\text{Earnings}_{t+1} = 4.0 + 0.84\,\text{Cash flow}_t + 0.38\,\text{Accruals}_t
$$

He decomposes Maplewood's 2025 earnings from continuing operations of $96.8 million into a cash flow component of $41.3 million and an accruals component of $55.5 million.

Reyes also compares Maplewood with Ridgefield Housewares, a peer.
Both companies reported 2025 ROE well above the industry average of 12%: Maplewood 24% and Ridgefield 23%.
Ridgefield's earnings consist mostly of cash flow, with accruals equal to about 10% of earnings.

## Questions

1. After adjusting for the receivables sale, Maplewood's 2025 days sales outstanding (DSO) compared with its 2024 DSO is closest to: (LOS: los-03-05-h)
   - A. 12.9 days lower.
   - B. 1.8 days higher.
   - C. 16.5 days higher.
2. The after-tax contribution of bill-and-hold sales, as a percentage of 2025 earnings from continuing operations, is closest to: (LOS: los-03-05-h)
   - A. 4.7%.
   - B. 14.9%.
   - C. 19.6%.
3. Relative to appropriate revenue recognition, the promotional oven shipment most likely caused Maplewood's 2025 statements to show: (LOS: los-03-05-b)
   - A. overstated net income and overstated inventory.
   - B. overstated net income and understated inventory.
   - C. understated net income and understated receivables.
4. Maplewood's 2025 recurring (core) pre-tax earnings are closest to: (LOS: los-03-05-e)
   - A. $123.7 million.
   - B. $133.4 million.
   - C. $146.0 million.
5. Using the persistence regression, Reyes's forecast of Maplewood's 2026 earnings is closest to: (LOS: los-03-05-f)
   - A. $59.8 million.
   - B. $66.3 million.
   - C. $85.3 million.
6. Relative to Ridgefield's ROE, Maplewood's ROE is most likely to decline toward the industry average: (LOS: los-03-05-g)
   - A. more slowly.
   - B. at the same rate.
   - C. more rapidly.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** 2024: $DSO = 262.1/(1{,}512.0/365) = 262.1/4.1425 = 63.27$ days.
> 2025 as reported: $318.4/(1{,}786.0/365) = 318.4/4.8932 = 65.07$ days.
> 2025 pro forma, adding back the sold receivables: $(318.4 + 72.0)/4.8932 = 390.4/4.8932 = 79.79$ days.
> Change: $79.79 - 63.27 = 16.51$ days higher; pro forma receivables grew $390.4/262.1 - 1 = 48.9\%$ against revenue growth of $1{,}786.0/1{,}512.0 - 1 = 18.1\%$.
> A is wrong because it subtracts the sold receivables instead of adding them back ($(318.4 - 72.0)/4.8932 - 63.27 = 50.36 - 63.27 = -12.92$).
> B is wrong because it uses reported receivables, which the sale flattered ($65.07 - 63.27 = 1.80$).
> 2. **B.** Bill-and-hold revenue $= 1{,}786.0 \times 0.04 = 71.44$; gross profit $= 71.44 \times 0.265 = 18.9316$; after tax $= 18.9316 \times (1 - 0.24) = 14.3880$.
> Share of earnings $= 14.3880/96.8 = 14.86\%$.
> A is wrong because it multiplies by the tax rate instead of one minus the tax rate ($18.9316 \times 0.24 = 4.5436$; $4.5436/96.8 = 4.69\%$).
> C is wrong because it ignores taxes ($18.9316/96.8 = 19.56\%$).
> 3. **B.** Recognizing revenue on goods the customer may return overstates revenue, net income, and receivables, and understates inventory, because goods that are still effectively Maplewood's were removed from inventory at shipment.
> A is wrong because inventory is understated, not overstated; the cost of the shipped units left inventory when revenue was recognized.
> C is wrong because it reverses the direction of both effects.
> 4. **A.** Core pre-tax earnings add back non-recurring expenses and remove non-recurring gains: $127.4 + 18.6 - 22.3 = 123.7$.
> The other non-operating expense of 9.7 recurs every year and stays in core earnings.
> B is wrong because it also adds back the recurring 9.7 ($127.4 + 18.6 + 9.7 - 22.3 = 133.4$).
> C is wrong because it adds back the restructuring charge but leaves the one-time warehouse gain in core earnings ($127.4 + 18.6 = 146.0$).
> 5. **A.** $E_{2026} = 4.0 + 0.84 \times 41.3 + 0.38 \times 55.5 = 4.0 + 34.692 + 21.090 = 59.782$.
> The cash coefficient exceeds the accruals coefficient, so a company whose earnings are 57.3% accruals ($55.5/96.8 = 0.5733$) is forecast to see a large decline.
> B is wrong because it swaps the coefficients, applying the higher persistence to accruals ($4.0 + 0.38 \times 41.3 + 0.84 \times 55.5 = 66.314$).
> C is wrong because it applies the cash flow coefficient to total earnings and ignores the accruals decomposition ($4.0 + 0.84 \times 96.8 = 85.312$).
> 6. **C.** Both ROEs are well above average and should revert toward the mean; the larger accruals component in Maplewood's earnings makes them less persistent, so Maplewood's ROE should revert faster.
> A is wrong because it reverses the accruals effect; the cash-heavy company, Ridgefield, is the one whose ROE declines more slowly.
> B is wrong because it ignores the composition of earnings, which is what drives the speed of mean reversion.

## Distractor design

1. A: sold receivables subtracted instead of added back (sign error); B: reported receivables used, ignoring the factoring sale (misread exhibit).
2. A: tax rate applied instead of one minus the tax rate (before-tax vs after-tax error); C: no tax adjustment (before-tax vs after-tax error).
3. A: inventory effect reversed (direction error); C: both effects reversed (sign error).
4. B: recurring expense treated as non-recurring (misclassified item); C: non-recurring gain left in core earnings (incomplete adjustment).
5. B: cash and accruals coefficients swapped (wrong formula variant); C: cash coefficient applied to total earnings (decomposition ignored).
6. A: accruals effect on reversion speed reversed (direction error); B: composition of earnings ignored.
