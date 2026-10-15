---
type: cfa-lm
topic: "Financial Statement Analysis"
topic_code: "03"
topic_slug: "03-Financial-Statement-Analysis"
volume: 3
lm: 3
title: "Multinational Operations"
pages: "115-199"
weight_band: "10-15%"
difficulty: 4
los_count: 10
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/financial-statement-analysis]
---

# LM3: Multinational Operations

Difficulty 4 of 5: the rules are few (two translation methods, one exposure concept, one hyperinflation split) but the exam tests them as direction tables crossed with ratio arithmetic, and one wrong rate on one line item breaks a whole translation worksheet.

## LOS map

- **compare** and contrast presentation in (reporting) currency, functional currency, and local currency (V3 p.115) ^los-03-03-a
    - Examiner asks: given a subsidiary that keeps its books in one currency, prices its goods in another and reports to a parent in a third, name the functional currency from the Exhibit 3 indicators and state which translation method follows.
- **describe** foreign currency transaction exposure, including accounting for and disclosures about foreign currency transaction gains and losses (V3 p.115) ^los-03-03-b
    - Examiner asks: for a receivable or payable that straddles a balance sheet date, compute the gain or loss in each period, state that it goes to net income even though unrealized, and identify which of three transactions actually creates exposure.
- **analyze** how changes in exchange rates affect the translated sales of the subsidiary and parent company (V3 p.115) ^los-03-03-c
    - Examiner asks: sales are translated at the average rate under both methods, so a strengthening foreign currency raises translated sales and a weakening one lowers them; compute the constant-currency sales or the share of a segment with the currency effect removed.
- **compare** the current rate method and the temporal method, evaluate how each affects the parent company's balance sheet and income statement, and determine which method is appropriate in various scenarios (V3 p.115) ^los-03-03-d
    - Examiner asks: which rate (current, historical, average) applies to inventory, fixed assets, debt, receivables, COGS and depreciation under each method, and whether the adjustment lands in net income or in equity.
- **calculate** the translation effects and evaluate the translation of a subsidiary's balance sheet and income statement into the parent company's presentation currency (V3 p.115) ^los-03-03-e
    - Examiner asks: translate a short balance sheet, then back out retained earnings (temporal) or the cumulative translation adjustment (current rate) as the balancing figure, and sign the translation gain or loss.
- **analyze** how the current rate method and the temporal method affect financial statements and ratios (V3 p.115) ^los-03-03-f
    - Examiner asks: which ratios are preserved from local currency under the current rate method (pure balance sheet or pure income statement ratios), which are distorted (mixed ratios), and which ratio is identical under both methods (receivables turnover).
- **analyze** how alternative translation methods for subsidiaries operating in hyperinflationary economies affect financial statements and ratios (V3 p.115) ^los-03-03-g
    - Examiner asks: restate a nonmonetary asset by the price index ratio and translate at the current rate (IFRS), or hold it at the historical rate (US GAAP), and compute the cumulative translation gain or loss over two years.
- **describe** how multinational operations affect a company's effective tax rate (V3 p.115) ^los-03-03-h
    - Examiner asks: read an effective tax rate reconciliation, identify the "effect of tax rates in foreign jurisdictions" line, and attribute a change in the effective rate to a shift in the profit mix across jurisdictions.
- **explain** how changes in the components of sales affect the sustainability of sales growth (V3 p.115) ^los-03-03-i
    - Examiner asks: decompose reported sales growth into volume, price and mix, foreign exchange, and acquisitions, and rank countries or segments by organic growth rather than by reported growth.
- **analyze** how currency fluctuations potentially affect financial results, given a company's countries of operation (V3 p.115) ^los-03-03-j
    - Examiner asks: from a company's disclosed exposures and sensitivity analysis, state which currency movement hurts earnings and use a cash-flow-at-risk table to calibrate a downside forecast.

## Core intuition

A multinational has two kinds of foreign currency problems, and they are accounted for in two different places (V3 p.116, p.117).
The first is a transaction denominated in a currency other than the entity's functional currency: an export receivable, an import payable, a foreign loan.
The second is a whole subsidiary that keeps its books in another currency and has to be folded into the parent's consolidated statements.
The transaction problem is settled in cash within months, so its gains and losses go straight to net income.
The subsidiary problem is a permanent investment, so the standards ask whether the subsidiary is really operating in the parent's currency or in its own before deciding whether the revaluation belongs in income or in equity (V3 p.137, p.138).

### Three currencies and one decision

The local currency is the currency of the country where the entity sits.
The functional currency is the currency of the primary economic environment in which it operates, normally the currency in which it generates and spends cash.
The presentation (reporting) currency is the currency in which the statements are published (V3 p.117).
For most companies all three coincide, but for a foreign subsidiary the functional currency must be chosen, and that one choice determines everything that follows (V3 p.135).
IFRS lists the indicators: the currency that mainly influences sales prices, the currency of the country whose competitive forces and regulations set those prices, the currency that influences labour and material costs, the currency of financing, and the currency in which operating receipts are retained; then whether the operation is an extension of the parent or autonomous, how large intra-group transactions are, whether cash flows are remitted to the parent, and whether the operation can service its own debt (V3 p.135, p.136).
When the indicators are mixed, the first two (sales prices and the market that sets them) take priority (V3 p.135).
An autonomous, self-contained subsidiary that prices and finances locally has the local currency as its functional currency; a sales outlet or an extension of the parent that prices in the parent's currency and remits cash has the parent's currency (V3 p.136, p.198).

![[Translation-vs-Remeasurement.excalidraw]]

> [!abstract] Idea 1: the functional currency picks the method, the method picks the exposure, and the exposure picks where the gain or loss goes
> Functional currency is the local (foreign) currency: current rate method, exposure is net assets, the adjustment accumulates in equity as the cumulative translation adjustment (CTA) until the subsidiary is sold.
> Functional currency is the parent's currency: temporal method (US GAAP calls it remeasurement), exposure is net monetary assets, the gain or loss goes through net income now (V3 p.137, p.138, p.139).
> The economic logic: a subsidiary that lives in the parent's currency has foreign-currency monetary items that will be settled soon, so the gain is near-realized and belongs in income; a subsidiary that lives in its own currency is a single investment whose translation swings are unrealized until disposal.

### Transactions: the sign rule

Every foreign currency transaction is recorded at the spot rate on the transaction date; the inventory or sale is fixed at that amount forever (V3 p.118, p.119).
Only the receivable or payable is remeasured at each balance sheet date and at settlement, and each remeasurement is a gain or loss in net income, realized or not (V3 p.119, p.120).
If a balance sheet date intervenes, the gain to that date is recognized in year one and the remainder in year two; the two periods sum to the actual realized gain (V3 p.120, p.121).
The sign follows from the nature of the position: a receivable is an asset exposure, so a strengthening foreign currency is a gain and a weakening one a loss; a payable is a liability exposure, so a strengthening foreign currency is a loss and a weakening one a gain (V3 p.121).

| Transaction | Exposure | Foreign currency strengthens | Foreign currency weakens |
|---|---|---|---|
| Export sale (receivable) | Asset | Gain | Loss |
| Import purchase (payable) | Liability | Loss | Gain |

Neither IFRS nor US GAAP says where on the income statement these gains and losses go: some companies put them in other operating income or expense, others below operating profit in net financing cost (V3 p.121).
Gross margin and net margin are unaffected either way, but operating margin differs, and the operating choice injects exchange-rate volatility into operating profit, which distorts peer comparisons (V3 p.123).
Both standards require disclosure of the aggregate exchange difference in net income, but neither requires disclosure of the line item that holds it (V3 p.124).
Transaction gains and losses are often immaterial because the amounts are small, the rates stable, receivables and payables in the same currency naturally offset, or the company hedges with forwards and options (V3 p.129).

### Translation: why a plug is unavoidable

Translate every line of a subsidiary's balance sheet at the same rate and it stays in balance (V3 p.131).
Translate common stock at its historical rate, so that the parent's original investment stays at its historical cost, and the moment the rate moves the translated balance sheet no longer balances (V3 p.131).
The plug that restores balance is the translation adjustment, and its size is the net exposure times the rate change (V3 p.132, p.133).
Under the current rate approach every asset and liability is exposed, so the plug equals net assets times the rate change; under the monetary approach only cash, receivables and payables are exposed, so the plug equals net monetary assets times the rate change (V3 p.132, p.133, p.134).
The Spanco illustration makes the point with one balance sheet: with all items at current rate a weakening dollar produces a 2,000 euro loss on net assets of 10,000, whereas with only monetary items exposed the same move produces a 400 euro gain because monetary liabilities (5,000) exceed monetary assets (3,000) (V3 p.132, p.133).

> [!abstract] Idea 2: the translation adjustment is exposure times rate change, and the sign table for transactions applies unchanged
> Net asset exposure plus a strengthening foreign currency gives a positive adjustment; net liability exposure plus a strengthening foreign currency gives a negative one; reverse the currency move and the signs flip (V3 p.134).
> Under the current rate method exposure is almost always a net asset (equity is positive), so the CTA moves with the foreign currency.
> Under the temporal method most liabilities are monetary and most assets are not, so exposure is usually a net monetary liability, and a strengthening foreign currency produces a remeasurement loss in net income (V3 p.137, p.139).

| Balance sheet exposure | Foreign currency strengthens | Foreign currency weakens |
|---|---|---|
| Net asset | Positive translation adjustment | Negative translation adjustment |
| Net liability | Negative translation adjustment | Positive translation adjustment |

The cumulative translation adjustment is the running sum of each period's adjustment; a negative 2,000 in one quarter followed by a positive 500 leaves a cumulative negative 1,500 (V3 p.134).
When the subsidiary is sold the CTA is recycled into net income as a realized gain or loss (V3 p.137).

### The two methods line by line

Current rate method: all assets and liabilities at the current (balance sheet date) rate, equity accounts other than retained earnings at historical rates, revenues and expenses at the rate on the transaction date, in practice the average rate, dividends at the rate on the declaration date (V3 p.137, p.140).
The income statement is translated first, retained earnings roll forward from translated net income less translated dividends, and the CTA is the balance sheet plug (V3 p.145).
Temporal method: monetary assets and liabilities (and nonmonetary items carried at current value) at the current rate, nonmonetary items at historical cost at their historical rates, equity at historical rates, most revenues and expenses at the average rate, but cost of goods sold, depreciation and amortization at the historical rates of the assets they come from (V3 p.138, p.140).
The balance sheet is translated first, retained earnings is the plug, and the remeasurement gain or loss is whatever makes the income statement reconcile to that retained earnings figure (V3 p.145).
Deferred revenue is a nonmonetary liability, so it sits at the historical rate under the temporal method; deferred taxes, payables, accrued expenses and debt are monetary (V3 p.131, p.140).
The temporal method forces the company to track the rate at which every piece of inventory and plant was bought, and the inventory cost flow assumption decides which rate applies: FIFO ending inventory carries recent rates and FIFO COGS older rates, LIFO the reverse, and weighted average cost uses the weighted average rate for both (V3 p.138).

| Item | Current rate method | Temporal method |
|---|---|---|
| Cash, receivables | Current | Current |
| Inventory at cost, PP&E, intangibles | Current | Historical |
| Nonmonetary assets at current value (marketable securities, inventory written to market) | Current | Current (rate when the value was set) |
| Payables, accrued expenses, debt, deferred taxes | Current | Current |
| Deferred revenue | Current | Historical |
| Common stock, paid-in capital | Historical | Historical |
| Retained earnings | Roll-forward | Plug (balancing figure) |
| Revenues, most expenses | Average | Average |
| COGS, depreciation, amortization | Average | Historical (rate of the related asset) |
| Dividends | Historical (declaration date) | Historical (declaration date) |
| Translation adjustment | Separate component of equity (CTA) | Gain or loss in net income |
| Exposure | Net assets | Net monetary assets (adjusted for nonmonetary items at current value) |

### What each method does to the numbers

In the Canadaco illustration the Canadian dollar strengthens from 0.70 to 0.80 euro over the year (V3 p.145).
Under the current rate method net assets are exposed and the currency strengthened, so the plug is a positive 202,000 euro adjustment in equity and net income is 885,000 (V3 p.146, p.147).
Under the temporal method exposed liabilities (payables plus notes payable) exceed exposed assets (cash plus receivables), so the same strengthening produces a 245,000 euro translation loss in net income, and net income falls to 745,000 even though income before the translation loss (990,000) is higher than under the current rate method because COGS and depreciation were translated at the older, lower rates (V3 p.146, p.147).
Total assets are higher under the current rate method (4,624,000 versus 4,282,000) because inventory and plant are translated at the higher current rate rather than at historical rates; that ordering reverses if the foreign currency weakens (V3 p.147, p.153).

> [!abstract] Idea 3: strengthening foreign currency raises revenues, assets and liabilities under both methods; only net income and equity depend on the method and the exposure
> Current rate method: strengthening raises everything, including net income and equity (positive CTA).
> Temporal method with net monetary liabilities: strengthening raises revenues, assets and liabilities but lowers net income and equity through the translation loss.
> Temporal method with net monetary assets: strengthening raises everything, including net income, through a translation gain.
> Weakening reverses every arrow (V3 p.153, p.156, p.157).

| Foreign currency move | Temporal, net monetary liability exposure | Temporal, net monetary asset exposure | Current rate method |
|---|---|---|---|
| Strengthens | Revenues up, assets up, liabilities up, net income down, equity down (translation loss) | Revenues up, assets up, liabilities up, net income up, equity up (translation gain) | Revenues up, assets up, liabilities up, net income up, equity up (positive CTA) |
| Weakens | Revenues down, assets down, liabilities down, net income up, equity up (translation gain) | Revenues down, assets down, liabilities down, net income down, equity down (translation loss) | Revenues down, assets down, liabilities down, net income down, equity down (negative CTA) |

Companies can manage temporal exposure by matching monetary assets to monetary liabilities; eliminating current rate exposure would require total assets to equal total liabilities, that is zero equity, which is impractical (V3 p.152).
Financing a fixed asset with equity rather than a local-currency loan removes a 300,000 euro temporal loss in the Canadaco case (V3 p.151, p.152).

### Ratios: pure versus mixed

Under the current rate method every balance sheet item is translated at the same rate and every income statement item at the same rate, so a ratio built entirely from the balance sheet (current ratio, debt to assets, debt to equity) or entirely from the income statement (gross, operating and net margins, interest coverage) is identical in local currency and in translated currency (V3 p.149).
Mixed ratios (turnovers, ROA, ROE) are distorted because the numerator uses the average rate and the denominator the current rate; with a strengthening currency the current rate exceeds the average, so translated turnover and return ratios are lower than in local currency (V3 p.149).
Under the temporal method almost every ratio is distorted, in a direction that cannot be generalized, because COGS, depreciation, inventory and fixed assets each carry their own historical rate (V3 p.149).
Two exceptions: receivables turnover is the same under both methods because sales are at the average and receivables at the current rate under both, and inventory turnover under the temporal method equals the local currency figure because COGS and inventory share the same historical rate (V3 p.149).
The cash ratio uses only monetary items, so it is unaffected by the choice of method (V3 p.198).

### Hyperinflation: two philosophies

When the local economy is highly inflationary the functional currency is irrelevant (V3 p.141).
IFRS restates the local-currency statements for inflation under IAS 29 and then translates everything at the current rate; US GAAP forbids restatement and requires the temporal method, as if the parent's currency were the functional currency (V3 p.141, p.157).
US GAAP defines highly inflationary as cumulative three-year inflation above 100%, roughly 26% per year, applied with judgment; IAS 29 treats a cumulative rate approaching or exceeding 100% as an indicator (V3 p.141).
The FASB chose the temporal method to avoid the "disappearing plant" problem: translating historical cost at ever weaker rates makes land and buildings shrink toward nothing on the parent's balance sheet (V3 p.141, p.142).
Under IAS 29, monetary items are not restated because they are already in current money, nonmonetary items and all equity are restated by the change in the general price index since acquisition, income statement items are restated from the dates recorded, and the purchasing power gain or loss on the net monetary position goes to net income (V3 p.158).
Holding cash during inflation is a purchasing power loss; owing money is a purchasing power gain, exactly analogous to the temporal method's translation gain on net monetary liabilities when the currency weakens (V3 p.158, p.159).
If the exchange rate falls by exactly the same proportion as the price index rises (purchasing power parity holds precisely), the two approaches give identical results; in practice they rarely do (V3 p.159, p.161).

### Reading the disclosures

Both standards require disclosure of the exchange differences recognized in net income and of the CTA in equity with a reconciliation of its opening and closing balances; US GAAP adds the amount recycled from equity on disposal of a foreign entity (V3 p.163).
The exchange difference in net income mixes transaction gains and losses with temporal-method translation gains and losses, and companies are not required to split them (V3 p.163).
A multinational may apply both methods at once, one per subsidiary, so its statements can carry a translation loss in income and a CTA in equity simultaneously (V3 p.162).
Two peers can choose differently (Exxon Mobil largely local currency, Chevron the US dollar), so net income is not comparable until the analyst adds the CTA movement to net income on a clean-surplus basis (V3 p.162, p.167, p.168).

Multinational operations reach the effective tax rate through the mix of profits across jurisdictions and through transfer pricing; the reconciliation between the statutory rate and the effective rate discloses the "effect of tax rates in foreign jurisdictions" line, and a change in that line means either a change in rates abroad or a shift in where profit is earned (V3 p.169, p.171).
Sales growth decomposes into volume, price and mix, foreign exchange, and acquisitions; growth from volume and price is more sustainable and more under management's control than growth from exchange rates, which is why companies report organic or constant-currency growth (V3 p.171, p.172, p.173).
Sensitivity disclosures such as BMW's cash-flow-at-risk by currency pair let the analyst calibrate downside scenarios for profit and cash flow (V3 p.174, p.175, p.176).

## Formulas and derivations

**Foreign currency transaction gain or loss in a period** (V3 p.119, p.120, p.121)
$$
\text{Gain}_{t} = FC \times (S_t - S_{t-1}) \times \begin{cases} +1 & \text{asset (receivable)} \\ -1 & \text{liability (payable)} \end{cases}
$$
^f-03-03-1

- $FC$: foreign currency amount of the receivable or payable; $S_t$: spot rate in functional currency per unit of foreign currency at date $t$ (balance sheet date or settlement date).
- The inventory or revenue is fixed at $FC \times S_0$ and never remeasured; only the monetary balance moves.
- Example 2: $10{,}000 \times (1.480 - 1.460) = 200$ gain in 20X1, $10{,}000 \times (1.475 - 1.480) = -50$ in 20X2 (V3 p.120, p.121).

**Realized gain equals the sum of period gains** (V3 p.120, p.121)
$$
\sum_{t} \text{Gain}_t = FC \times (S_{settle} - S_0) \times (\pm 1)
$$
^f-03-03-2

- Telescoping sum: intermediate balance sheet dates only change timing, never the total.
- Example 2: $200 - 50 = 150 = 10{,}000 \times (1.475 - 1.460)$ (V3 p.121).
- The French importer's Canadian dollar payable: $-2{,}860 + 540 - 2{,}360 = -4{,}680 = -100{,}000 \times (0.7753 - 0.7285)$ (V3 p.124).

**Operating profit margin under the two placement alternatives** (V3 p.122, p.123)
$$
\text{OPM}_{\text{operating placement}} = \frac{\text{Operating profit}_{ex} + G}{\text{Sales}}, \qquad \text{OPM}_{\text{non-operating placement}} = \frac{\text{Operating profit}_{ex}}{\text{Sales}}
$$
^f-03-03-3

- $G$: transaction gain (negative for a loss); $\text{Operating profit}_{ex}$: operating profit excluding the gain.
- Gross margin and net margin are identical under both placements; only the operating line moves (V3 p.123).

**Current rate method translation** (V3 p.137, p.140, p.145)
$$
A^{PC} = A^{FC} \times C, \quad L^{PC} = L^{FC} \times C, \quad CS^{PC} = CS^{FC} \times H, \quad NI^{PC} = NI^{FC} \times A, \quad Div^{PC} = Div^{FC} \times H_{div}
$$
^f-03-03-4

- $C$: current rate at the balance sheet date; $H$: historical rate at the equity contribution; $A$: average rate; $H_{div}$: rate on the dividend declaration date; all in parent currency per unit of foreign currency.
- Translate the income statement first, then retained earnings, then the balance sheet; the CTA is the plug in Formula 6.

**Translated retained earnings roll-forward** (V3 p.139, p.140)
$$
RE^{PC}_{end} = RE^{PC}_{begin} + NI^{PC} - Div^{FC} \times H_{div}
$$
^f-03-03-5

- Same under both methods; the difference is that $NI^{PC}$ comes from the translated income statement under the current rate method and is derived from the balance sheet plug under the temporal method.
- Canadaco, current rate: $0 + 885{,}000 - 350{,}000 \times 0.78 = 612{,}000$ (V3 p.146).

**Cumulative translation adjustment as a plug and as exposure times rate change** (V3 p.132, p.134, p.145)
$$
\begin{aligned}
CTA_{end} &= (A^{FC} - L^{FC}) \times C - CS^{FC} \times H - RE^{PC}_{end} \\
\Delta CTA &= NA^{FC}_{begin} \times (C - C_{begin}) + NI^{FC} \times (C - A) - Div^{FC} \times (C - H_{div})
\end{aligned}
$$
^f-03-03-6

- $NA^{FC}_{begin}$: beginning net assets in foreign currency; the second form says the adjustment is the exposure held during the period times the change in rate since each component was recorded.
- Canadaco: $1{,}500{,}000 \times (0.80 - 0.70) + 1{,}180{,}000 \times (0.80 - 0.75) - 350{,}000 \times (0.80 - 0.78) = 150{,}000 + 59{,}000 - 7{,}000 = 202{,}000$, which matches the plug (V3 p.147).

> [!tip] Calculator
> Plug form for Canadaco: `5780000 × 0.80 =` gives 4,624,000; `3450000 × 0.80 =` gives 2,760,000; `4624000 - 2760000 - 1050000 - 612000 =` gives 202,000.

**Temporal method translation and the remeasurement gain or loss** (V3 p.138, p.140, p.145)
$$
\begin{aligned}
RE^{PC}_{end} &= \underbrace{MA^{FC} \times C + NMA^{FC} \times H_{asset}}_{\text{translated assets}} - ML^{FC} \times C - NML^{FC} \times H - CS^{FC} \times H \\
\text{Translation gain (loss)} &= RE^{PC}_{end} - RE^{PC}_{begin} + Div^{FC} \times H_{div} - \text{Income before translation}^{PC}
\end{aligned}
$$
^f-03-03-7

- $MA$, $ML$: monetary assets and liabilities; $NMA$, $NML$: nonmonetary items at their own historical rates; income before translation uses $A$ for most lines but $H_{inv}$ for COGS and $H_{PPE}$ for depreciation.
- Translate the balance sheet first; retained earnings is the plug; the gain or loss is whatever reconciles the income statement to that plug.
- Canadaco: assets $4{,}282{,}000$, liabilities $2{,}760{,}000$, stock $1{,}050{,}000$, so $RE = 472{,}000$; income before translation $990{,}000$, dividends $273{,}000$, so the loss is $472{,}000 + 273{,}000 - 990{,}000 = -245{,}000$ (V3 p.146, p.147).

> [!tip] Calculator
> Canadaco temporal assets: `980000 + 900000 = × 0.80 =` gives 1,504,000; `1200000 × 0.74 =` gives 888,000; `2700000 × 0.70 =` gives 1,890,000; sum 4,282,000. Then `4282000 - 2760000 - 1050000 =` gives 472,000; `472000 + 273000 - 990000 =` gives -245,000.

**Balance sheet exposure by method** (V3 p.137, p.139)
$$
\text{Exposure}_{\text{current rate}} = TA^{FC} - TL^{FC} = \text{Net assets}, \qquad \text{Exposure}_{\text{temporal}} = MA^{FC} - ML^{FC} \;(\text{plus nonmonetary items at current value})
$$
^f-03-03-8

- Positive exposure with a strengthening foreign currency gives a positive adjustment; the four-cell sign table in Idea 2 follows.
- Consol-Can: net assets $400 - 77 - 175 = 148$ under the current rate method versus net monetary $135 + 98 - 77 - 175 = -19$ under the temporal method (V3 p.198).

**Temporal-method loss avoided by financing with equity** (V3 p.151, p.152)
$$
\Delta \text{Translation gain} = \text{Monetary liability}^{FC} \times (C - C_{begin})
$$
^f-03-03-9

- Example 5: $3{,}000{,}000 \times (0.80 - 0.70) = 300{,}000$, the difference between a 245,000 loss (net monetary liabilities) and a 55,000 gain (net monetary assets) (V3 p.151, p.152).

**IAS 29 inflation restatement of a nonmonetary item** (V3 p.142, p.143, p.158, p.160)
$$
\text{Restated}^{FC} = \text{Historical cost}^{FC} \times \frac{GPI_{end}}{GPI_{acq}}, \qquad \text{Translated}^{PC} = \text{Restated}^{FC} \times C
$$
^f-03-03-10

- $GPI$: general price index; equivalently multiply by $(1 + \pi_1)(1 + \pi_2)\dots$ for successive annual inflation rates.
- Turkey land: $542{,}700{,}000 \times 1.38 \times 1.69 \times 1.45 = 1{,}835{,}243{,}163$ TL, divided by 1,669,000 TL per dollar gives 1,100 dollars (V3 p.143).
- Income statement items are restated from the average index: Example 7 revenue $1{,}000 \times 200/125 = 1{,}600$ (V3 p.160).

> [!tip] Calculator
> Ambleu patent: `85.17 × 1.406 × 1.623 =` gives 194.35; `÷ 14.4810 =` gives 13.42; `15 - 13.42 =` gives the 1.58 cumulative loss (V3 p.194).

**Purchasing power gain or loss on the net monetary position** (V3 p.158, p.160, p.161)
$$
\text{PP gain} = \sum_{\text{monetary liabilities}} L \times \frac{GPI_{end} - GPI_{date}}{GPI_{date}} - \sum_{\text{monetary assets}} A \times \frac{GPI_{end} - GPI_{date}}{GPI_{date}}
$$
^f-03-03-11

- Each monetary balance is indexed from the date it arose (beginning balance from the opening index, additions during the year from the average index).
- Example 7: $5{,}000 \times 1.00 - 1{,}000 \times 1.00 - 750 \times 0.60 = 3{,}550$ FC (V3 p.161).

**Highly inflationary threshold** (V3 p.141)
$$
(1 + \pi)^3 > 2 \;\Rightarrow\; \pi > 2^{1/3} - 1 \approx 26\% \text{ per year}
$$
^f-03-03-12

- US GAAP: cumulative three-year inflation above 100%; IAS 29: approaching or exceeding 100% is an indicator, applied with judgment about trend.
- Crenland: GPI 100 to 228.2 over two years is 128.2% cumulative, already above the threshold (V3 p.194).

**Clean-surplus adjusted net income** (V3 p.162, p.167, p.168)
$$
NI_{adj} = NI_{reported} + \Delta CTA
$$
^f-03-03-13

- Adds the period's translation adjustment from the statement of stockholders' equity back into income so that a current-rate company and a temporal-method company are on the same footing.
- Exxon Mobil 2011: $42{,}206 - 867 = 41{,}339$; Chevron 2011: $27{,}008 + 17 = 27{,}025$ (V3 p.168).
- Yahoo 2011: adjusted change is $(1{,}062{,}699 + 209{,}887) / (1{,}244{,}628 + 131{,}205) - 1 = -7.5\%$ instead of $-14.6\%$ (V3 p.166).

**Effective tax rate and its reconciliation** (V3 p.169, p.170, p.171)
$$
ETR = \frac{\text{Tax expense}}{\text{Pretax profit}} = \text{Statutory rate} + \text{Foreign jurisdiction effect} + \text{Other reconciling items}
$$
^f-03-03-14

- The foreign jurisdiction line is positive when profits are earned where rates exceed the home rate and negative otherwise; its change across years signals a shift in profit mix or in foreign rates.
- Heineken 2011: $25.0\% + 3.5\% + \dots = 26.1\%$; Ambleu 2017: $96 / 294 = 32.65\%$ against $94 / 269 = 34.94\%$ in 2016 (V3 p.170, p.194).

**Sales growth decomposition** (V3 p.172, p.173, p.174)
$$
g_{\text{reported}} = g_{\text{volume}} + g_{\text{price and mix}} + g_{FX} + g_{\text{acquisitions}}, \qquad g_{\text{organic}} = g_{\text{reported}} - g_{FX} - g_{\text{acquisitions}}
$$
^f-03-03-15

- Constant-currency growth removes only the FX term; organic growth removes FX and acquisitions or divestitures.
- P&G, October 2008 to September 2009 average: reported $-7\%$, FX effect $-8\%$, acquisitions $0\%$, so organic growth is $-7\% - (-8\%) - 0\% = 1\%$ (V3 p.174).
- General Mills Latin America: reported $-5\%$, FX $-16\%$, constant currency $+11\%$ (V3 p.172).

**Ratio preservation under the current rate method** (V3 p.148, p.149)
$$
\frac{X^{FC} \times C}{Y^{FC} \times C} = \frac{X^{FC}}{Y^{FC}}, \qquad \frac{X^{FC} \times A}{Y^{FC} \times A} = \frac{X^{FC}}{Y^{FC}}, \qquad \frac{X^{FC} \times A}{Y^{FC} \times C} \ne \frac{X^{FC}}{Y^{FC}} \text{ when } A \ne C
$$
^f-03-03-16

- Pure balance sheet and pure income statement ratios are preserved; mixed ratios are scaled by $A / C$, so a strengthening currency ($C > A$) lowers translated turnover and return ratios.
- Canadaco: receivables turnover $13.33$ in C$ becomes $12.50 = 13.33 \times 0.75 / 0.80$ in euro under both methods (V3 p.148).

| Ratio | Local currency versus current rate method | Current rate versus temporal (Canadaco, C$ strengthening) |
|---|---|---|
| Current ratio | Same | Temporal lower (inventory at historical 0.74 versus 0.80) |
| Debt to assets, debt to equity | Same | Temporal higher (assets and equity lower) |
| Interest coverage | Same | Temporal higher (COGS and depreciation at lower historical rates) |
| Gross, operating margin | Same | Temporal higher |
| Net profit margin | Same | Temporal lower (translation loss in income) |
| Receivables turnover | Lower under current rate | Identical under both methods |
| Inventory turnover | Lower under current rate | Temporal equals local currency figure |
| Fixed asset turnover | Lower under current rate | Temporal higher |
| ROA, ROE | Lower under current rate | Direction case-specific (ROA lower, ROE higher for Canadaco) |

## Worked examples

### Example 1: FinnCo, peso payable settled before year end (V3 p.119)

Setup: FinnCo (functional currency euro) buys goods for MXN100,000 on 1 November 20X1 at MXN1 = EUR0.0684 and pays on 15 December 20X1 at MXN1 = EUR0.0703.

Step 1, record the purchase: inventory and payable at $100{,}000 \times 0.0684 = 6{,}840$ euro.
Step 2, settle: cash paid $100{,}000 \times 0.0703 = 7{,}030$ euro.
Step 3, Formula 1 for a liability: $-100{,}000 \times (0.0703 - 0.0684) = -190$, a realized loss in 20X1 net income.
Inventory stays at 6,840; cash falls by 7,030; retained earnings fall by 190.
The peso strengthened and FinnCo owed pesos, so the liability exposure produced a loss.
Python check: `100000*0.0703-100000*0.0684 = 190`. ^ex-03-03-1

### Example 2: FinnCo, pound receivable across a balance sheet date (V3 p.120, p.121)

Setup: sale of £10,000 on 15 November 20X1, collected 15 January 20X2; rates 1.460, 1.480 (31 December) and 1.475 euro per pound.

Receivable in euro at each date: $14{,}600$, $14{,}800$, $14{,}750$.
20X1 gain: $10{,}000 \times (1.480 - 1.460) = 200$, unrealized but in net income.
20X2 loss: $10{,}000 \times (1.475 - 1.480) = -50$.
Formula 2 check: $200 - 50 = 150 = 10{,}000 \times (1.475 - 1.460)$, the realized gain over the whole life.
Had this been a £10,000 payable, the signs flip: a 200 loss then a 50 gain (V3 p.121).
Python check: `10000*(1.48-1.46) = 200`, `10000*(1.475-1.48) = -50`. ^ex-03-03-2

### Example 3: placement of the gain and the operating margin (V3 p.122, p.123)

Setup: revenues 20,000, COGS 12,000, other operating expenses 5,000, non-operating expenses 1,200 in both years; a 200 gain in 20X1 and a 50 loss in 20X2.

20X1, Alternative 1 (operating): other operating expenses $5{,}000 - 200 = 4{,}800$, operating profit $8{,}000 - 4{,}800 = 3{,}200$, margin $16.0\%$; net profit $3{,}200 - 1{,}200 = 2{,}000$, margin $10.0\%$.
20X1, Alternative 2 (non-operating): operating profit $3{,}000$, margin $15.0\%$; non-operating $1{,}200 - 200 = 1{,}000$; net profit $2{,}000$, margin $10.0\%$.
20X2, Alternative 1: other operating $5{,}050$, operating profit $2{,}950$, margin $14.75\%$; net profit $1{,}750$, margin $8.75\%$.
20X2, Alternative 2: operating profit $3{,}000$, margin $15.0\%$; non-operating $1{,}250$; net profit $1{,}750$, margin $8.75\%$.
Gross margin is $40\%$ throughout.
Alternative 1 makes operating margin swing from 16.0% to 14.75% while Alternative 2 holds it at 15.0%; the placement choice, not economics, creates the volatility.
Python check: `3200/20000 = 0.16`, `2950/20000 = 0.1475`, `1750/20000 = 0.0875`. ^ex-03-03-3

### Illustration: French importer with a C$100,000 payable over three reporting dates (V3 p.123, p.124)

Rates euro per C$: 0.7285 (1 December X1), 0.7571 (31 December X1), 0.7517 (31 March X2), 0.7753 (15 May X2).
Euro value of the payable: 72,850; 75,710; 75,170; 77,530.
Period results for a liability: $-(75{,}710 - 72{,}850) = -2{,}860$ (Q4 X1 loss), $-(75{,}170 - 75{,}710) = +540$ (Q1 X2 gain), $-(77{,}530 - 75{,}170) = -2{,}360$ (Q2 X2 loss).
Total $-4{,}680 = -(77{,}530 - 72{,}850)$, the realized loss; the interim unrealized loss of 2,860 was a poor predictor of the final 4,680.
Python check: `100000*(0.7753-0.7285) = 4680`. ^ex-03-03-4

### Illustration: Spanco and Amerco, why the plug arises and which items are exposed (V3 p.131, p.132, p.133)

Setup: Amerco starts on 31 December 20X1 with cash 3,000, inventory 12,000, notes payable 5,000 and common stock 10,000 (US$), rate €1 = US$1; by 31 March 20X2 the rate is €0.80 per US$1 with no transactions.

All items at current rate: assets $15{,}000 \times 0.80 = 12{,}000$; notes payable $4{,}000$; common stock at historical $10{,}000$; plug $12{,}000 - 4{,}000 - 10{,}000 = -2{,}000$.
Decomposition: loss 600 on cash, loss 2,400 on inventory, gain 1,000 on notes payable, net $-2{,}000$; equivalently net assets $10{,}000 \times (0.80 - 1.00)$.
Monetary items only at current rate: cash $2{,}400$, inventory stays $12{,}000$, notes payable $4{,}000$, plug $14{,}400 - 4{,}000 - 10{,}000 = +400$.
Decomposition: loss 600 on cash, gain 1,000 on notes payable; equivalently net monetary liability $2{,}000 \times (1.00 - 0.80) = 400$ gain.
Same rate move, opposite sign, because the exposure flipped from net assets of 10,000 to net monetary liabilities of 2,000.
Python check: `15000*0.8-5000*0.8-10000 = -2000`, `3000*0.8+12000-5000*0.8-10000 = 400`. ^ex-03-03-5

### Example 4: Turkish land under three approaches (V3 p.141, p.142, p.143)

Setup: land bought 1 January 2000 for TL542,700,000 (US$1,000 at TL542,700 per dollar); year-end rates 670,800; 1,474,525; 1,669,000; inflation 38%, 69%, 45%.

Approach 1, current rate on historical cost (not allowed by either standard): $542{,}700{,}000 / 670{,}800 = 809$; $/ 1{,}474{,}525 = 368$; $/ 1{,}669{,}000 = 325$.
Annual losses $-191$, $-441$, $-43$; cumulative $-675$; land has "disappeared" to 325 dollars.
Approach 2, temporal (US GAAP): historical rate every year, land stays at $1{,}000$, no translation gain or loss.
Approach 3, restate then translate (IFRS), Formula 10:
- 2000: $542{,}700{,}000 \times 1.38 = 748{,}926{,}000$; $/ 670{,}800 = 1{,}116$; gain $116$.
- 2001: $748{,}926{,}000 \times 1.69 = 1{,}265{,}684{,}940$; $/ 1{,}474{,}525 = 858$; loss $-258$; cumulative $-142$.
- 2002: $1{,}265{,}684{,}940 \times 1.45 = 1{,}835{,}243{,}163$; $/ 1{,}669{,}000 = 1{,}100$; gain $242$; cumulative $+100$.
The IFRS figure of 1,100 reflects both the likely rise in the lira value of the land and the actual fall in the lira.
Python check: `542700000*1.38*1.69*1.45/1669000 = 1099.6`. ^ex-03-03-6

### Illustration: Canadaco under both methods, with ratios (V3 p.143 to p.149)

Setup: Canadaco starts 1 January 20X1 with cash C$1,500,000 and PP&E C$3,000,000, financed by a C$3,000,000 note and C$1,500,000 stock.
20X1: sales 12,000,000; COGS 9,000,000; selling 750,000; depreciation 300,000; interest 270,000; tax 500,000; net income 1,180,000; dividends 350,000 on 1 December.
Year-end balance sheet: cash 980,000; receivables 900,000; inventory 1,200,000 (FIFO); PP&E 3,000,000 less 300,000; payables 450,000; note 3,000,000; stock 1,500,000; retained earnings 830,000.
Rates euro per C$: 0.70 (1 January), 0.75 (average), 0.74 (inventory), 0.78 (dividend), 0.80 (31 December).

Current rate method (Formulas 4 to 6):
- Net income $1{,}180{,}000 \times 0.75 = 885{,}000$; dividends $350{,}000 \times 0.78 = 273{,}000$; retained earnings $612{,}000$.
- Assets $5{,}780{,}000 \times 0.80 = 4{,}624{,}000$; liabilities $3{,}450{,}000 \times 0.80 = 2{,}760{,}000$; stock $1{,}500{,}000 \times 0.70 = 1{,}050{,}000$.
- CTA $= 4{,}624{,}000 - 2{,}760{,}000 - 1{,}050{,}000 - 612{,}000 = 202{,}000$, positive because net assets were exposed and the C$ strengthened.
- Total equity $1{,}050{,}000 + 612{,}000 + 202{,}000 = 1{,}864{,}000$.

Temporal method (Formula 7):
- Assets: cash and receivables $1{,}880{,}000 \times 0.80 = 1{,}504{,}000$; inventory $1{,}200{,}000 \times 0.74 = 888{,}000$; net PP&E $2{,}700{,}000 \times 0.70 = 1{,}890{,}000$; total $4{,}282{,}000$.
- Liabilities $2{,}760{,}000$; stock $1{,}050{,}000$; retained earnings plug $472{,}000$.
- Income before translation: $9{,}000{,}000 - 9{,}000{,}000 \times 0.74 - 562{,}500 - 300{,}000 \times 0.70 - 202{,}500 - 375{,}000 = 9{,}000{,}000 - 6{,}660{,}000 - 562{,}500 - 210{,}000 - 202{,}500 - 375{,}000 = 990{,}000$.
- Net income needed $= 472{,}000 + 273{,}000 = 745{,}000$; translation loss $= 745{,}000 - 990{,}000 = -245{,}000$.
- Exposed liabilities (450,000 + 3,000,000) exceed exposed assets (980,000 + 900,000), and the C$ strengthened, so a loss is expected.

Differences: net income $+18.8\%$ higher under current rate ($885 / 745 - 1$), income before translation $-10.6\%$ lower, total assets $+8.0\%$, total equity $+22.5\%$ (V3 p.147).

Ratios (C$, current rate, temporal):
- Current ratio $6.84$, $6.84$, $6.64$; debt to assets $0.52$, $0.52$, $0.56$; debt to equity $1.29$, $1.29$, $1.58$; interest coverage $7.22$, $7.22$, $7.74$.
- Gross margin $0.25$, $0.25$, $0.26$; operating margin $0.16$, $0.16$, $0.17$; net margin $0.10$, $0.10$, $0.08$.
- Receivables turnover $13.33$, $12.50$, $12.50$; inventory turnover $7.50$, $7.03$, $7.50$; fixed asset turnover $4.44$, $4.17$, $4.76$.
- ROA $0.20$, $0.19$, $0.17$; ROE $0.51$, $0.47$, $0.49$.
Only receivables turnover is the same under both methods; pure ratios match the C$ figures under the current rate method; every mixed ratio is lower under the current rate method because $0.75 / 0.80 < 1$.
Python check: `4624000-2760000-1050000-612000 = 202000`; `4282000-2760000-1050000 = 472000`; `472000+273000-990000 = -245000`; `9000000/720000 = 12.5`; `6660000/888000 = 7.5`. ^ex-03-03-7

### Example 5: temporal method with net monetary liabilities versus net monetary assets (V3 p.150, p.151, p.152)

Setup: Case A as in the Canadaco illustration (note payable 3,000,000, stock 1,500,000); Case B finances PP&E with stock 4,500,000 and no debt, keeping the same 270,000 interest expense for comparability.

Case A: retained earnings plug $472{,}000$, translation loss $-245{,}000$, net income $745{,}000$.
Case B: assets unchanged at $4{,}282{,}000$; liabilities $450{,}000 \times 0.80 = 360{,}000$; stock $4{,}500{,}000 \times 0.70 = 3{,}150{,}000$; retained earnings $4{,}282{,}000 - 360{,}000 - 3{,}150{,}000 = 772{,}000$.
Net income $772{,}000 + 273{,}000 = 1{,}045{,}000$; translation gain $1{,}045{,}000 - 990{,}000 = +55{,}000$.
Difference $772{,}000 - 472{,}000 = 300{,}000 = 3{,}000{,}000 \times (0.80 - 0.70)$, the loss on holding the C$ note while the C$ strengthened (Formula 9).
Monetary assets exceed monetary liabilities in Case B, so the strengthening C$ produces a gain.
Python check: `4282000-360000-3150000 = 772000`; `772000+273000-990000 = 55000`; `3000000*0.10 = 300000`. ^ex-03-03-8

### Example 6: stable, strengthening and weakening C$ under both methods (V3 p.153 to p.156)

Rates (stable, strengthens, weakens): average 0.70, 0.75, 0.65; inventory 0.70, 0.74, 0.66; dividend 0.70, 0.78, 0.62; year end 0.70, 0.80, 0.60; opening 0.70 in all.

Current rate method:
- Stable: net income $1{,}180{,}000 \times 0.70 = 826{,}000$; retained earnings $826{,}000 - 245{,}000 = 581{,}000$; assets $4{,}046{,}000$; liabilities $2{,}415{,}000$; CTA $4{,}046{,}000 - 2{,}415{,}000 - 1{,}050{,}000 - 581{,}000 = 0$; equity $1{,}631{,}000$.
- Strengthens: net income $885{,}000$; sales $9{,}000{,}000$; assets $4{,}624{,}000$; liabilities $2{,}760{,}000$; CTA $+202{,}000$; equity $1{,}864{,}000$.
- Weakens: net income $767{,}000$; sales $7{,}800{,}000$; retained earnings $767{,}000 - 217{,}000 = 550{,}000$; assets $3{,}468{,}000$; liabilities $2{,}070{,}000$; CTA $3{,}468{,}000 - 2{,}070{,}000 - 1{,}050{,}000 - 550{,}000 = -202{,}000$; equity $1{,}398{,}000$.
Everything moves with the C$: sales, net income, assets, liabilities, equity all higher when it strengthens and lower when it weakens.

Temporal method:
- Stable: assets $4{,}046{,}000$; retained earnings $581{,}000$; income before translation $826{,}000$; translation gain zero; net income $826{,}000$; equity $1{,}631{,}000$.
- Strengthens: assets $4{,}282{,}000$; retained earnings $472{,}000$; income before translation $990{,}000$; loss $-245{,}000$; net income $745{,}000$; equity $1{,}522{,}000$.
- Weakens: assets $1{,}880{,}000 \times 0.60 + 1{,}200{,}000 \times 0.66 + 2{,}700{,}000 \times 0.70 = 1{,}128{,}000 + 792{,}000 + 1{,}890{,}000 = 3{,}810{,}000$; liabilities $2{,}070{,}000$; retained earnings $3{,}810{,}000 - 2{,}070{,}000 - 1{,}050{,}000 = 690{,}000$; income before translation $7{,}800{,}000 - 5{,}940{,}000 - 487{,}500 - 210{,}000 - 175{,}500 - 325{,}000 = 662{,}000$; net income $690{,}000 + 217{,}000 = 907{,}000$; translation gain $+245{,}000$; equity $1{,}740{,}000$.
With net monetary liabilities, a stronger C$ raises sales but lowers net income and equity; a weaker C$ lowers sales but raises net income and equity, the Exhibit 5 pattern.
Python check: `1880000*0.60+1200000*0.66+2700000*0.70 = 3810000`; `3810000-2070000-1050000 = 690000`; `690000+217000-662000 = 245000`. ^ex-03-03-9

### Example 7: ABC's subsidiary in a country with 100% inflation, IFRS versus US GAAP (V3 p.159, p.160, p.161)

Setup: land FC9,000 bought 1 January 20X1; cash 1,000 at start, 1,750 at year end; note payable 5,000 at 5%; stock 5,000; rent revenue 1,000; interest 250; net income 750.
GPI 100, 125 (average), 200; rates US$ per FC 1.00, 0.80 (average), 0.50.

IFRS restate then translate (Formulas 10 and 11):
- Cash $1{,}750$ (monetary, not restated); land $9{,}000 \times 200/100 = 18{,}000$; total $19{,}750$.
- Note payable $5{,}000$; stock $5{,}000 \times 200/100 = 10{,}000$; retained earnings plug $19{,}750 - 5{,}000 - 10{,}000 = 4{,}750$.
- Revenue $1{,}000 \times 200/125 = 1{,}600$; interest $250 \times 200/125 = 400$; subtotal $1{,}200$; purchasing power gain $4{,}750 - 1{,}200 = 3{,}550$.
- Check of the gain: note payable $5{,}000 \times 1.00 = 5{,}000$ gain; opening cash $1{,}000 \times 1.00 = 1{,}000$ loss; cash added during the year $750 \times (200 - 125)/125 = 450$ loss; net $3{,}550$.
- Translate everything at 0.50: assets $9{,}875$; land $9{,}000$; net income $4{,}750 \times 0.50 = 2{,}375$; no translation adjustment.
US GAAP temporal: cash $1{,}750 \times 0.50 = 875$; land $9{,}000 \times 1.00 = 9{,}000$; note $2{,}500$; stock $5{,}000$; retained earnings plug $9{,}875 - 2{,}500 - 5{,}000 = 2{,}375$; revenue $800$; interest $200$; translation gain $2{,}375 - 600 = 1{,}775$.
Identical results because the GPI doubled and the FC halved in dollar value, exactly purchasing power parity.
If the year-end rate were 0.60 instead: IFRS net income $4{,}750 \times 0.60 = 2{,}850$; US GAAP retained earnings $1{,}750 \times 0.60 + 9{,}000 - 5{,}000 \times 0.60 - 5{,}000 = 2{,}050$, so the methods diverge (V3 p.161).
Python check: `5000-1000-750*75/125 = 3550`; `4750*0.5 = 2375`; `1750*0.6+9000-3000-5000 = 2050`. ^ex-03-03-10

### Example 8: Yahoo's translation disclosures (V3 p.164, p.165, p.166)

1. Accumulated OCI rose from 504,254 to 697,869 thousand, a change of $193{,}615$; visible in the balance sheet equity section and in the statement of stockholders' equity.
2. The foreign currency translation adjustment in 2011 OCI was $209{,}887$ thousand, arising from the current rate method applied to subsidiaries with foreign functional currencies; with positive net assets, a positive adjustment means foreign currencies strengthened against the dollar.
3. Adjusted net income (Formula 13): 2010 $1{,}244{,}628 + 131{,}205 = 1{,}375{,}833$; 2011 $1{,}062{,}699 + 209{,}887 = 1{,}272{,}586$; change $-7.5\%$ instead of the reported $-14.6\%$.
4. Yahoo describes risk from the dollar's perspective because the dollar is its reporting currency: a stronger dollar lowers translated revenues, expenses and income.
5. Asia Pacific share: $830{,}482 / 4{,}380{,}828 = 19.0\%$; at 2010 rates revenue would have been $59{,}000$ lower in Asia Pacific, $16{,}000$ lower in EMEA and $6{,}000$ lower in the Americas, so the share would have been $771{,}482 / 4{,}299{,}828 = 17.9\%$.
Python check: `(1062699+209887)/(1244628+131205)-1 = -0.075`; `771482/4299828 = 0.1794`. ^ex-03-03-11

### Example 9: Exxon Mobil versus Chevron on a clean-surplus basis (V3 p.167, p.168)

Adjusted net income (Formula 13), millions of dollars:
- Exxon Mobil: 2011 $42{,}206 - 867 = 41{,}339$; 2010 $31{,}398 + 1{,}034 = 32{,}432$; 2009 $19{,}658 + 3{,}629 = 23{,}287$.
- Chevron: 2011 $27{,}008 + 17 = 27{,}025$; 2010 $19{,}136 + 6 = 19{,}142$; 2009 $10{,}563 + 60 = 10{,}623$.
Ratios of Exxon to Chevron, reported: $1.6$, $1.6$, $1.9$; adjusted: $1.5$, $1.7$, $2.2$.
Exxon's adjustments are far larger because it designates the local currency as functional for most operations (current rate, CTA in equity) while Chevron uses the dollar (temporal, gains in income).
Adjusting brings the two closer to comparable but not fully, because the methods also translate the underlying lines differently.
Python check: `19658+3629 = 23287`; `23287/10623 = 2.19`. ^ex-03-03-12

### Example 10: Heineken and Colgate-Palmolive effective tax rate reconciliations (V3 p.169, p.170, p.171)

1. Heineken's domestic rate is 25.0% (2011), lower than Colgate's US statutory 35.0%.
2. Multinational operations raised Heineken's effective rate by 3.5 points ("effect of tax rates in foreign jurisdictions", 62 million on a base of 1,785) and lowered Colgate's by 1.7 points ("earnings taxed at other than United States statutory rate").
3. Heineken's foreign effect rose from 1.9 points in 2010 to 3.5 in 2011, suggesting its profit mix shifted toward higher-tax countries, or that rates rose where it earns profit.
Heineken's reported effective rate: $465 / 1{,}785 = 26.1\%$ on profit before tax excluding associates.
Python check: `62/1785 = 0.0347`; `465/1785 = 0.2605`. ^ex-03-03-13

### Example 11: Procter and Gamble organic sales growth (V3 p.173, p.174)

1. P&G presents organic sales growth (reported growth excluding acquisitions, divestitures and foreign exchange) because it shows underlying trends on a consistent basis and because it is a management compensation metric.
2. October 2008 to September 2009 averages: reported $-7\%$, FX effect $-8\%$, acquisitions $0\%$, organic $+1\%$; Formula 15 gives $-7\% - (-8\%) - 0\% = 1\%$.
Without the currency headwind reported and organic growth would both have been 1%.
General Mills, fiscal 2011: Latin America reported $-5\%$ with a $-16\%$ currency impact is $+11\%$ constant currency; Canada $8\%$ reported with $+5\%$ currency is only $3\%$ constant currency (V3 p.172).
Python check: `-7-(-8)-0 = 1`; `-5-(-16) = 11`. ^ex-03-03-14

## Item-set patterns

> [!warning] Trap 1: which transaction creates exposure
> The vignette lists three transactions: a sale paid on the purchase date, a loan a subsidiary takes in its own functional currency, and an import purchase on 45-day terms in a foreign currency.
> Correct: only the deferred payment in a currency other than the entity's functional currency creates transaction exposure; a same-day settlement has no interval and a loan in the borrower's functional currency is not a foreign currency transaction for the borrower (V3 p.118, p.193).
> Distractors: the sale in dollars (tempting because it is a foreign currency) and the loan from a bank whose presentation currency differs (tempting because two currencies appear); the test is the borrower's functional currency, not the lender's.

> [!warning] Trap 2: the sign of a transaction gain when the rate is quoted the other way round
> Exhibit gives ₣B per NVK (foreign currency units per unit of functional currency) rising from 4.1779 to 4.1790 on a ₣B payable.
> Correct: a rising quote means the foreign currency weakened, so a payable produces a gain: $27{,}000 / 4.1779 - 27{,}000 / 4.1790 = 1.70$ per ton (V3 p.193).
> Distractors: multiplying instead of dividing, or reading a rising number as a strengthening foreign currency and calling it a loss; a third distractor uses the year-end rate 4.2374 for a transaction settled on 15 July.

> [!warning] Trap 3: which rate for which line under the temporal method
> The vignette provides five rates (opening, average, inventory weighted average, dividend, closing) and asks for inventory, fixed assets, debt or receivables.
> Correct: monetary items at closing, inventory at its acquisition rate (FIFO recent, weighted average uses the weighted average rate), fixed assets at the rate when purchased, COGS and depreciation at the rates of their assets, sales at average (V3 p.138, p.140, p.197).
> Distractors: the average rate for inventory when the vignette says FIFO and gives a specific inventory rate, the closing rate for fixed assets (that is the current rate method), or the debt issuance rate for long-term debt (never used; debt is monetary).

> [!warning] Trap 4: retained earnings and CTA are plugs, not translations
> The vignette gives a balance sheet in local currency and asks for translated retained earnings (temporal) or the translation adjustment (current rate).
> Correct: translate every other line, then subtract to find the balancing figure; Consol-Can gives $369 - 325 = 44$ million (V3 p.197).
> Distractors: retained earnings times the closing rate (46) or times the historical rate (41); both are offered as options.

> [!warning] Trap 5: exposure under the two methods
> The board asks what the balance sheet exposure would be if the functional currency changed.
> Correct: current rate exposure is net assets (total assets less total liabilities), $400 - 77 - 175 = 148$; temporal exposure is net monetary assets, $135 + 98 - 77 - 175 = -19$ (V3 p.198).
> Distractors: total assets (400), or the net monetary figure when the question asks about the current rate method; also "reduce exposure by issuing debt to buy fixed assets", which increases a net monetary liability rather than reducing it (V3 p.198, p.199).

> [!warning] Trap 6: direction of net income under the temporal method when the currency strengthens
> The vignette says the foreign currency strengthened and the subsidiary uses the temporal method, then asks whether net income or equity is higher or lower than under a stable currency.
> Correct: check the monetary position first; with net monetary liabilities a strengthening currency produces a translation loss, so net income and equity fall even though revenues, assets and liabilities rise (V3 p.156, p.157).
> Distractors: assuming strengthening raises everything (true only under the current rate method or with net monetary assets), or forgetting that translated income before the translation loss can still be higher because COGS is at an older, lower rate.

> [!warning] Trap 7: which ratios change when the functional currency changes
> The question asks which ratio is most likely affected by switching from temporal to current rate.
> Correct: a ratio mixing a nonmonetary balance sheet item with an income statement item (fixed asset turnover) changes; the cash ratio (monetary only) and receivables turnover (sales at average, receivables at current under both) do not (V3 p.149, p.198).
> Distractors: receivables turnover (feels like it should change because it is a mixed ratio) and the cash ratio (a balance sheet ratio, but built only from monetary items).

> [!warning] Trap 8: gross margin and the inventory method plus translation method combination
> Which combination of inventory cost flow and translation method gives the highest translated gross margin when the foreign currency is depreciating and local inflation is positive?
> Correct: FIFO gives lower COGS in local currency under inflation, so FIFO beats weighted average in both cases; the translation method then depends on the currency's direction. For Eurexim with a depreciating hryvnia the curriculum answer is FIFO plus the current rate method (V3 p.196); for Acceletron with an appreciating Singapore dollar it is FIFO plus the temporal method, because COGS translated at older, lower rates is smaller than COGS at the average rate (V3 p.199).
> Distractors: weighted average cost (raises COGS under inflation) and the wrong method for the direction of the currency; always reason from "which rate makes COGS smallest relative to sales at the average rate".

> [!warning] Trap 9: hyperinflation under IFRS versus US GAAP
> The vignette states cumulative inflation over 100% and asks for the translated value of a nonmonetary asset or of revenue.
> Correct under IFRS: restate by the price index ratio from acquisition (or from the average for income items), then translate at the closing rate; under US GAAP: historical rate with no restatement (V3 p.141, p.157, p.194, p.196).
> Distractors: translating historical cost at the closing rate with no restatement (the "disappearing plant" number, 31,452 for the Abuelio warehouse), keeping historical cost at the historical rate under IFRS (50,000), or restating from the base index rather than from the acquisition or average index.

> [!warning] Trap 10: organic growth versus reported growth
> A table shows volume, price, foreign exchange and net sales growth by country and asks which has the most sustainable growth.
> Correct: rank by volume plus price (organic), because FX is outside management's control; Abuelio's 13% beats Borliand's 13% reported growth that includes a 4-point currency tailwind (V3 p.172, p.196).
> Distractors: the highest reported growth, or the domestic country because it has no FX line.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM03-Multinational-Operations-Practice-Problems]]

## Cross-links

- [[LM01-Intercorporate-Investments]]: translation is applied to a subsidiary that has already been consolidated with the acquisition method, so 100% of the subsidiary's lines, goodwill and any non-controlling interest are what get translated; the CTA sits alongside the other equity components created at acquisition.
- [[LM05-Evaluating-Quality-of-Financial-Reports]]: the functional currency designation, the placement of transaction gains in operating income, and the choice between a translation loss in income and a CTA in equity are earnings quality levers; clean-surplus adjusted income is the analyst's defence.
- [[LM06-Integration-of-Financial-Statement-Analysis-Techniques]]: the integration case decomposes reported growth into organic and currency components and adjusts turnover and return ratios for translation distortions before comparing multinationals.
- [[LM01-Currency-Exchange-Rates-Understanding-Equilibrium-Value]]: the direction of the currency move is the input to every table here; purchasing power parity is the reason the IFRS restate-then-translate and US GAAP temporal results coincide only when the exchange rate change equals the inflation differential.
- [[LM01-Pricing-and-Valuation-of-Forward-Commitments]]: forward contracts and options are the instruments companies use to hedge the transaction exposures described here, and their fair value changes join the transaction gains in the exchange difference recognized in net income.

## Self-test

Vignette A for Q1 to Q4: Kestrel, a subsidiary of a US parent, was formed on 1 January 2025 with LC1,200 of stock and an LC1,500 bank loan, and immediately bought PP&E for LC2,300.
At 31 December 2025 Kestrel reports (LC): cash 400, receivables 600, inventory 900, PP&E net 2,100, payables 500, debt 1,500, stock 1,200, retained earnings 800.
2025 income statement (LC): sales 6,000, COGS 4,000, depreciation 200, SG&A 700, interest 100, tax 200, net income 800; no dividends.
Rates USD per LC: 0.50 (1 January and PP&E), 0.56 (inventory acquired), 0.55 (average), 0.60 (31 December).

> [!question] Q1
> If the LC is Kestrel's functional currency, the translation adjustment for 2025 is closest to:
> A. 120.
> B. 160.
> C. 200.

> [!question] Q2
> If the US dollar is Kestrel's functional currency, translated total assets at 31 December 2025 are closest to:
> A. 2,000.
> B. 2,154.
> C. 2,400.

> [!question] Q3
> If the US dollar is Kestrel's functional currency, the 2025 remeasurement result included in net income is closest to:
> A. a loss of 56.
> B. a loss of 100.
> C. a gain of 56.

> [!question] Q4
> If the US dollar is Kestrel's functional currency, the translated 2025 gross profit margin is closest to:
> A. 32.1%.
> B. 33.3%.
> C. 39.4%.

Vignette B for Q5 to Q7: Halcyon Inc. (functional and presentation currency US dollar, US GAAP) buys equipment from a UK supplier for £250,000 on 10 November 2025, payable on 20 January 2026; rates USD per GBP are 1.30 (10 November), 1.34 (31 December) and 1.31 (20 January).
Halcyon's subsidiary in Orlandia bought land for FC500,000 on 1 January 2025 when the rate was USD0.020 per FC; Orlandia's general price index rose from 100 to 250 during 2025 and the year-end rate is USD0.009 per FC; Orlandia has been highly inflationary for three years.
Halcyon's 2025 tax reconciliation on pretax income of 1,000: statutory rate 30%, effect of foreign jurisdictions -40, non-deductible expenses +15, other items zero.

> [!question] Q5
> The foreign currency transaction result Halcyon reports in 2025 net income on the equipment purchase is closest to:
> A. a loss of 10,000.
> B. a gain of 10,000.
> C. a loss of 2,500.

> [!question] Q6
> The Orlandia land in Halcyon's 31 December 2025 consolidated balance sheet under US GAAP, and the amount it would show under IFRS, are closest to:
> A. 10,000 and 11,250.
> B. 4,500 and 11,250.
> C. 10,000 and 10,000.

> [!question] Q7
> Halcyon's 2025 effective tax rate is closest to:
> A. 26.0%.
> B. 27.5%.
> C. 31.5%.

Vignette C for Q8 to Q10: Meridian AG reports in euro and has two subsidiaries.
Sub P has the euro as functional currency and holds net monetary liabilities in its local currency; Sub Q has its local currency as functional currency and has positive net assets.
Sub Q's 2025 sales were LCQ8,000 (average rate EUR0.55 per LCQ) and its year-end receivables LCQ800 (closing rate EUR0.60).
Meridian's reported 2025 sales growth was 9%, of which 4 points came from foreign exchange and 2 points from an acquisition.
An analyst expects both local currencies to weaken 10% against the euro in 2026.

> [!question] Q8
> Sub Q's receivables turnover in Meridian's euro statements is closest to:
> A. 9.17.
> B. 10.00.
> C. 10.91.

> [!question] Q9
> If the analyst's currency forecast is right, Meridian's 2026 statements will most likely show:
> A. a remeasurement gain in net income from Sub P and a negative translation adjustment in equity from Sub Q.
> B. a remeasurement loss in net income from Sub P and a negative translation adjustment in equity from Sub Q.
> C. remeasurement gains in net income from both subsidiaries.

> [!question] Q10
> Meridian's 2025 organic sales growth is closest to:
> A. 3%.
> B. 5%.
> C. 7%.

> [!success]- Answer key
> Q1: B. Current rate method; the adjustment equals exposure times rate change: opening net assets $1{,}200 \times (0.60 - 0.50) = 120$ plus net income $800 \times (0.60 - 0.55) = 40$, total $160$; plug check: net assets $2{,}000 \times 0.60 = 1{,}200$ less stock $600$ less retained earnings $800 \times 0.55 = 440$ gives $160$. A stops at the opening exposure; C applies the full-year change to ending net assets, ignoring that income accrued at the average rate (V3 p.134, p.145).
> Q2: B. Temporal: $(400 + 600) \times 0.60 + 900 \times 0.56 + 2{,}100 \times 0.50 = 600 + 504 + 1{,}050 = 2{,}154$. A translates everything at the historical rate; C is the current rate method ($4{,}000 \times 0.60$) (V3 p.138, p.140).
> Q3: A. Retained earnings plug $2{,}154 - 2{,}000 \times 0.60 - 600 = 354$; income before remeasurement $6{,}000 \times 0.55 - 4{,}000 \times 0.56 - 200 \times 0.50 - (700 + 100 + 200) \times 0.55 = 3{,}300 - 2{,}240 - 100 - 550 = 410$; remeasurement $354 - 410 = -56$, a loss, consistent with net monetary liabilities and a strengthening LC. B multiplies ending net monetary liabilities ($-1{,}000$) by the rate change, which ignores when the balances arose; C has the wrong sign (V3 p.139, p.145).
> Q4: A. Sales $3{,}300$, COGS $4{,}000 \times 0.56 = 2{,}240$, margin $1{,}060 / 3{,}300 = 32.1\%$ versus $33.3\%$ in LC and under the current rate method (B); C translates COGS at the PP&E rate of 0.50, which applies to depreciation, not to inventory (V3 p.138, p.149).
> Q5: A. Payable of £250,000; the pound strengthened from 1.30 to 1.34 by the balance sheet date, so the liability grew by $250{,}000 \times 0.04 = 10{,}000$, an unrealized loss recognized in 2025 net income. B has the sign of a receivable; C is the total realized loss over both years ($250{,}000 \times 0.01$), of which $7{,}500$ is a 2026 gain (V3 p.120, p.121).
> Q6: A. US GAAP temporal: historical cost at the historical rate $500{,}000 \times 0.020 = 10{,}000$. IFRS: restate $500{,}000 \times 250 / 100 = 1{,}250{,}000$, translate at $0.009$ gives $11{,}250$. B's 4,500 is historical cost at the closing rate, allowed by neither standard; C would hold only if the rate had fallen to exactly $0.020 / 2.5 = 0.008$, the purchasing power parity case (V3 p.141, p.142, p.143, p.161).
> Q7: B. $(300 - 40 + 15) / 1{,}000 = 27.5\%$; the negative foreign effect means profits are earned where rates are below 30%. A omits the non-deductible add-back; C omits the foreign jurisdiction effect: $(300 + 15) / 1{,}000 = 31.5\%$ (V3 p.169, p.170).
> Q8: A. Sales at the average rate and receivables at the closing rate under both methods: $8{,}000 \times 0.55 / (800 \times 0.60) = 4{,}400 / 480 = 9.17$. B is the LC figure, which is not preserved because the ratio mixes statements; C swaps the rates, putting sales at the closing rate and receivables at the average rate: $4{,}800 / 440 = 10.91$ (V3 p.148, p.149).
> Q9: A. Sub P uses the temporal method with net monetary liabilities; a weakening local currency shrinks those liabilities in euro, a remeasurement gain in net income. Sub Q uses the current rate method with net assets; a weakening local currency produces a negative CTA in equity. B has Sub P's sign wrong; C puts Sub Q's adjustment in the wrong statement (V3 p.134, p.157).
> Q10: A. Organic growth $= 9\% - 4\% - 2\% = 3\%$. B is constant-currency growth (removing FX only); C removes only the acquisition (V3 p.173, p.174).

## Flashcards

#flashcards/cfa-l2/03-Financial-Statement-Analysis/lm03

Three currencies in multinational accounting::Local (country of location), functional (primary economic environment, where cash is generated and spent), presentation or reporting (currency of the published statements) (V3 p.117).
Definition of a foreign currency transaction::A transaction denominated in a currency other than the entity's functional currency, such as an import, export, or borrowing in another currency (V3 p.118).
When does transaction exposure arise?::Only when the transaction date and the settlement date differ and the amount is fixed in a foreign currency (V3 p.118).
Receivable in a foreign currency that strengthens::Transaction gain (asset exposure) (V3 p.121).
Payable in a foreign currency that strengthens::Transaction loss (liability exposure) (V3 p.121).
Where do unrealized transaction gains at a balance sheet date go?::Net income, under both IFRS and US GAAP, one of the few cases where an unrealized gain is recognized in income (V3 p.120).
Do the standards specify where on the income statement transaction gains sit?::No; companies choose operating (other operating income or expense) or non-operating (net financing cost), and only the aggregate amount in net income must be disclosed (V3 p.121, p.124).
Which margin is affected by the placement choice for transaction gains?::Operating profit margin; gross and net margins are unchanged (V3 p.123).
Micro-problem: £10,000 receivable, rates 1.460 at sale, 1.480 at year end, 1.475 at settlement; gains by year?::Year 1 gain 200, year 2 loss 50, realized total 150; keystrokes 10000 × 0.02 = then 10000 × 0.005 = (V3 p.120, p.121).
Four reasons transaction gains are often immaterial::Few or small transactions, stable rates, natural offsets between receivables and payables in the same currency, hedging with forwards and options (V3 p.129).
Two conceptual questions in translating a subsidiary::Which exchange rate for each item, and where the translation adjustment goes (income or equity) (V3 p.130).
Why does a translation adjustment arise at all?::Equity is held at historical rates while other items move to the current rate, so the translated balance sheet no longer balances (V3 p.131, p.132).
Balance sheet exposure under the current rate method::Net assets (total assets less total liabilities), almost always a net asset exposure (V3 p.137).
Balance sheet exposure under the temporal method::Net monetary assets (monetary assets less monetary liabilities, adjusted for nonmonetary items carried at current value), usually a net liability (V3 p.139).
Net asset exposure plus strengthening foreign currency::Positive translation adjustment (V3 p.134).
Net liability exposure plus strengthening foreign currency::Negative translation adjustment or translation loss (V3 p.134).
Priority among the IFRS functional currency indicators::The currency that influences sales prices and the currency of the country whose competition and regulation set those prices come first (V3 p.135).
Which method when the subsidiary's functional currency is the local currency?::Current rate method; adjustment to the CTA in equity (V3 p.137).
Which method when the subsidiary's functional currency is the parent's currency?::Temporal method (remeasurement under US GAAP); gain or loss in net income (V3 p.137, p.138).
Three-step functional currency approach::Identify the functional currency, translate foreign balances into it (temporal logic), then translate functional currency statements into the presentation currency at the current rate (V3 p.136).
Current rate method rates for assets, liabilities, equity, income::Assets and liabilities at current, equity at historical, revenues and expenses at average (transaction-date) rates, dividends at the declaration-date rate (V3 p.137, p.140).
Temporal method rates for COGS and depreciation::The historical rates of the inventory and fixed assets they relate to (V3 p.138, p.140).
Temporal method rate for deferred revenue::Historical, because deferred revenue is a nonmonetary liability (V3 p.140).
Which rate for long-term debt under either method?::Current (closing) rate; debt is monetary; the issuance rate is never used (V3 p.140, p.199).
FIFO versus LIFO under the temporal method::FIFO ending inventory at recent rates and COGS at older rates; LIFO the reverse; weighted average cost uses the weighted average rate for both (V3 p.138).
Order of translation under the current rate method::Income statement first, then retained earnings, then the balance sheet with the CTA as the plug (V3 p.145).
Order of translation under the temporal method::Balance sheet first with retained earnings as the plug, then the income statement with the translation gain or loss as the reconciling figure (V3 p.145).
Formula for translated retained earnings::Beginning translated retained earnings plus translated net income less dividends at the declaration-date rate (V3 p.139).
Micro-problem: Canadaco current rate CTA::Assets 5,780,000 × 0.80 less liabilities 3,450,000 × 0.80 less stock 1,050,000 less retained earnings 612,000 gives 202,000; keystrokes 4624000 - 2760000 - 1050000 - 612000 = (V3 p.147).
Micro-problem: Canadaco temporal translation loss::Retained earnings plug 472,000 plus dividends 273,000 less income before translation 990,000 gives a 245,000 loss (V3 p.146, p.147).
How can a company eliminate temporal exposure?::Match monetary assets to monetary liabilities; current rate exposure can be eliminated only with zero equity (V3 p.152).
Effect of a strengthening foreign currency under the current rate method::Revenues, assets, liabilities, net income and equity all higher (V3 p.157).
Effect of a strengthening foreign currency under the temporal method with net monetary liabilities::Revenues, assets and liabilities higher; net income and equity lower through a translation loss (V3 p.157).
Effect of a weakening foreign currency under the temporal method with net monetary liabilities::Revenues, assets and liabilities lower; net income and equity higher through a translation gain (V3 p.157).
Which ratios are preserved under the current rate method?::Pure balance sheet ratios (current, debt to assets, debt to equity) and pure income statement ratios (margins, interest coverage) (V3 p.149).
Which ratios are distorted under the current rate method and in which direction when the currency strengthens?::Mixed ratios (turnovers, ROA, ROE) are lower because the numerator uses the average rate and the denominator the higher current rate (V3 p.149).
Only ratio identical under both translation methods::Receivables turnover (sales at average, receivables at current under both) (V3 p.149).
Ratio unchanged by the temporal method relative to local currency::Inventory turnover, because COGS and inventory share the same historical rate (V3 p.149).
Ratio unaffected by a change of functional currency because it uses only monetary items::Cash ratio (V3 p.198).
US GAAP definition of highly inflationary::Cumulative three-year inflation above 100%, about 26% per year, applied with judgment (V3 p.141).
IFRS treatment of a subsidiary in a hyperinflationary economy::Restate for inflation under IAS 29, then translate at the current rate; no translation adjustment arises (V3 p.141, p.161).
US GAAP treatment of a subsidiary in a hyperinflationary economy::Temporal method as if the parent's currency were functional; no inflation restatement (V3 p.141).
What is the disappearing plant problem?::Translating historical cost at ever weaker rates shrinks nonmonetary assets toward zero, which is why US GAAP mandates the temporal method under hyperinflation (V3 p.141).
IAS 29 treatment of monetary items::Not restated; the purchasing power gain or loss on the net monetary position goes to net income (V3 p.158).
Holding cash during inflation is a purchasing power {{loss}}; owing money is a purchasing power {{gain}} (V3 p.158, p.159).
When do IFRS and US GAAP give identical hyperinflation results?::When the exchange rate changes by exactly the same proportion as the price index, that is when purchasing power parity holds precisely (V3 p.159, p.161).
Micro-problem: land FC9,000, GPI 100 to 200, rate 1.00 to 0.50; IFRS and US GAAP values?::IFRS 9,000 × 2 × 0.50 = 9,000; US GAAP 9,000 × 1.00 = 9,000; identical because PPP held (V3 p.160, p.161).
Required translation disclosures under both standards::Exchange differences recognized in net income, and the CTA in equity with a reconciliation of opening and closing balances; US GAAP adds the amount recycled on disposal (V3 p.163).
What happens to the CTA when the subsidiary is sold?::It is transferred out of equity into net income as a realized gain or loss (V3 p.137).
Clean-surplus adjusted net income::Reported net income plus the period's translation adjustment from the statement of equity; used to compare current-rate and temporal-method companies (V3 p.162, p.167).
Micro-problem: Yahoo net income 1,244,628 to 1,062,699, CTA 131,205 and 209,887; adjusted change?::1,375,833 to 1,272,586, a 7.5% decline instead of 14.6% (V3 p.166).
Which line in a tax reconciliation captures multinational operations?::Effect of tax rates in foreign jurisdictions (or earnings taxed at other than the statutory rate); its change reflects profit mix or foreign rate changes (V3 p.169, p.171).
Definition of organic sales growth::Reported growth excluding foreign exchange and acquisitions or divestitures; constant-currency growth removes only FX (V3 p.172, p.173).
Why is volume and price growth more sustainable than FX growth?::Management controls volume and price; exchange rates are outside its control and can reverse (V3 p.172).
Micro-problem: reported growth -7%, FX effect -8%, acquisitions 0%; organic growth?::-7 - (-8) - 0 = 1% (V3 p.174).
Trap: which transaction creates exposure, same-day dollar sale, subsidiary loan in its own currency, or 45-day import payable in a foreign currency?::Only the 45-day payable; the same-day sale has no interval and the loan is in the borrower's functional currency (V3 p.193).
Trap: retained earnings under the temporal method::Never translated at a rate; it is the balancing figure after every other line is translated (V3 p.197).
Trap: reducing a net monetary liability exposure::Sell nonmonetary assets for cash; issuing any debt increases the net monetary liability (V3 p.198, p.199).
Highest translated gross margin when the foreign currency has been strengthening::FIFO plus the temporal method, because COGS is translated at older, lower rates while sales use the average rate (V3 p.199).
Under the current rate method total assets are {{higher}} than under the temporal method when the foreign currency has strengthened, and {{lower}} when it has weakened (V3 p.153).

## Common mistakes

1. Treating a transaction settled on the purchase date, or a subsidiary's loan in its own functional currency, as a foreign currency transaction exposure (V3 p.118, p.193).
2. Getting the sign wrong when rates are quoted as foreign currency units per unit of functional currency; a rising quote means the foreign currency weakened (V3 p.121, p.193).
3. Remeasuring the inventory or revenue along with the payable or receivable; only the monetary balance is remeasured (V3 p.119).
4. Assuming transaction gains always sit below operating profit; placement is a choice and only the aggregate must be disclosed (V3 p.121, p.124).
5. Confusing the exposure definitions: net assets under the current rate method, net monetary assets under the temporal method (V3 p.137, p.139).
6. Translating inventory or fixed assets at the closing rate under the temporal method, or at historical rates under the current rate method (V3 p.140, p.197).
7. Using the debt issuance rate for long-term debt; monetary items always use the closing rate (V3 p.199).
8. Translating retained earnings directly at some rate instead of deriving it as the plug (temporal) or rolling it forward (current rate) (V3 p.139, p.197).
9. Concluding that a strengthening foreign currency raises net income under the temporal method without checking whether the subsidiary has net monetary liabilities (V3 p.156, p.157).
10. Forgetting that income before the translation loss can be higher under the temporal method even when net income is lower, because COGS and depreciation are at older rates (V3 p.147).
11. Claiming that mixed ratios are preserved under the current rate method, or that receivables turnover differs between methods (V3 p.149).
12. Applying the current rate method to a hyperinflationary subsidiary's unrestated historical cost, the disappearing plant error (V3 p.141, p.142, p.194).
13. Restating a hyperinflationary income statement item from the base index instead of from the average index at which it was recorded (V3 p.158, p.194).
14. Applying IAS 29 restatement under US GAAP, or the temporal method under IFRS, for a hyperinflationary subsidiary (V3 p.141, p.157).
15. Ranking countries by reported sales growth rather than by volume plus price when asked about sustainable growth (V3 p.172, p.196).
16. Attributing a change in the effective tax rate to exchange rates rather than to the profit mix across jurisdictions or foreign rate changes (V3 p.169, p.194).
17. Comparing net income across a current-rate company and a temporal-method company without adding the CTA movement back on a clean-surplus basis (V3 p.162, p.167).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "03-03" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
