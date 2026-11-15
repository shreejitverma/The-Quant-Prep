---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [Damodaran (2012) - Investment Valuation: Tools and Techniques for Determining the Value of Any Asset, Fernandez (2002) - Valuation Methods and Shareholder Value Creation, Koller Goedhart and Wessels (2020) - Valuation: Measuring and Managing the Value of Companies (McKinsey)]
---

# Relative Valuation and Multiples Done Right

## TL;DR

- Multiples are not an alternative to discounted cash flow models; every valuation multiple is an algebraic simplification of a DCF model reflecting specific growth, risk, and reinvestment drivers.
- The Cardinal Sin of relative valuation is mismatched numerators and denominators: Enterprise Value must strictly pair with pre-interest operating metrics (EBIT, EBITDA, Sales), while Equity Value must strictly pair with after-interest equity metrics (Net Income, Book Value).
- Enterprise multiples (EV/EBIT, EV/NOPAT) are structurally superior to equity multiples (P/E) because they are independent of capital structure and leverage distortions.
- Warren Buffett has criticized EBITDA in Berkshire Hathaway's shareholder letters (for example 2000 and 2002) because depreciation reflects real capital spending required to replace aging assets.
- A high Price-to-Book (P/B) ratio is economically justified if and only if Return on Equity (ROE) substantially exceeds the Cost of Equity ($K_e$); low P/B paired with sub-hurdle ROE is the classic recipe for a value trap.

## Learning objectives

- Differentiate enterprise-level multiples from equity-level multiples and eliminate numerator-denominator mismatches.
- Calculate Enterprise Value with rigorous treatment of operating leases, cash equivalents, non-controlling interests, and affiliate investments.
- Derive the intrinsic mathematical determinants of P/E, EV/EBITDA, and P/B from first principles.
- Critique EBITDA as a cash flow proxy and evaluate the impact of maintenance capex on multiple integrity.
- Formulate the Price/Earnings-to-Growth (PEG) ratio and identify its mathematical failure modes.
- Execute peer group selection based on fundamental operating risk, margin profile, and capital intensity rather than superficial industry classifications.

## Core concepts

### 1. Multiples as Condensed DCF Models

Practitioners often view relative valuation as a market-driven alternative to DCF.
In reality, multiples are mathematically bound to DCF value drivers.
Consider the constant growth Gordon Growth model for Equity Value:

$$P_0 = \frac{\text{Dividends}_1}{K_e - g} = \frac{\text{Net Income}_1 \times (1 - b)}{K_e - g}$$

Where $b$ is the retention rate (Reinvestment Rate) and $(1 - b)$ is the payout ratio.
Dividing both sides by next year's earnings ($\text{EPS}_1$) yields the **Intrinsic Forward P/E**:

$$\frac{P_0}{\text{EPS}_1} = \frac{1 - b}{K_e - g} = \frac{\text{Payout Ratio}}{K_e - g}$$

For a hypothetical firm with ROE 15%, $K_e$ 9% and $g$ 4%, the sustainable payout is $1 - g / \text{ROE} = 73.33\%$, so the justified forward P/E is $0.7333 / 0.05 = 14.67\times$.
This simple equation reveals that a company's P/E multiple is not an arbitrary market mood; in this steady state it is governed by three variables:
1. **Growth ($g$)**: Higher expected growth drives higher multiples, provided reinvestment earns above the cost of capital.
2. **Cost of Equity ($K_e$)**: Higher risk and higher interest rates depress multiples.
3. **Reinvestment Needs ($b$)**: Higher capital intensity (lower payout ratio) depresses multiples for any given growth rate.

```
+-----------------------------------------------------------------------+
|                    THE THREE DRIVERS OF VALUATION MULTIPLES           |
+-----------------------------------------------------------------------+
| Multiple Expansion Drivers             Multiple Contraction Drivers   |
| - Accelerating organic growth (g)      - Decelerating growth          |
| - High Return on Capital (ROIC / ROE)  - Low Return on Capital        |
| - Low operating and financial leverage - High debt and cyclicality    |
| - Lower risk-free rates and WACC       - Rising cost of capital       |
+-----------------------------------------------------------------------+
```

### 2. The Golden Rule of Consistent Multiples

The single most common error in equity research is pairing an enterprise-level value with an equity-level cash flow metric, or vice versa:

```
+-----------------------------------------------------------------------+
|                    THE CONSISTENCY TAXONOMY                           |
+-----------------------------------------------------------------------+
| METRIC CLASS   | NUMERATOR              | ALLOWABLE DENOMINATORS      |
+----------------+------------------------+-----------------------------+
| Enterprise     | Enterprise Value (EV)  | - Revenue (EV/Sales)        |
| Level          | Claims of debt, equity,| - EBITDA (EV/EBITDA)        |
|                | and preferred holders  | - EBIT (EV/EBIT)            |
|                |                        | - NOPAT (EV/NOPAT)          |
|                |                        | - Invested Capital (EV/IC)  |
+----------------+------------------------+-----------------------------+
| Equity         | Market Capitalization  | - Net Income (P/E)          |
| Level          | (Share Price x Shares) | - Book Value (P/B)          |
|                | Claims of common       | - Free Cash Flow to Equity  |
|                | shareholders only      | - Dividends (Yield)         |
+----------------+------------------------+-----------------------------+
```

The Mismatch Sins:
- **Never compute EV / Net Income**: Net income is after interest expense; debt holders have already been paid, but EV includes debt claims.
- **Never compute Market Cap / EBITDA**: EBITDA belongs to both debt and equity holders; comparing it to equity market cap ignores leverage.

### 3. Calculating Enterprise Value (EV) with Precision

$$\text{EV} = \text{Market Cap} + \text{Total Debt} + \text{Lease Liabilities} + \text{Preferred Stock} + \text{Non-Controlling Interests} - \text{Cash \& Cash Equivalents} - \text{Investments in Associates}$$

```
+-----------------------------------------------------------------------+
|                      ENTERPRISE VALUE BRIDGE                          |
+-----------------------------------------------------------------------+
| [+] Market Capitalization (Diluted Shares x Stock Price)              |
| [+] Short-Term Debt & Current Portion of Long-Term Debt               |
| [+] Long-Term Interest-Bearing Debt (Market Value)                    |
| [+] Operating Lease Liabilities (ASC 842 / IFRS 16)                   |
| [+] Fair Value of Preferred Stock                                     |
| [+] Non-Controlling (Minority) Interests (Fair Value)                 |
| [-] Cash, Cash Equivalents, and Marketable Securities (Excess Cash)   |
| [-] Equity Affiliates / Non-Consolidated Associates                   |
| [=] ENTERPRISE VALUE (EV)                                             |
+-----------------------------------------------------------------------+
```

Why subtract Equity Affiliates?
If a company owns 30% of an unconsolidated affiliate, its income statement recognizes only its share of affiliate net income (below EBIT under equity method accounting).
EBITDA does not include the affiliate's operating profits; therefore, the affiliate asset value must be removed from EV to maintain metric consistency.

### 4. EBITDA: The Good, The Bad, and The Dangerous

EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization) is widely used in leveraged lending as a rough measure of operating cash available to service debt.

```
+-----------------------------------------------------------------------+
|                        THE DANGERS OF EBITDA                          |
+-----------------------------------------------------------------------+
| "References to EBITDA make us shudder - does management think the    |
| tooth fairy pays for capital expenditures?"                           |
|     - Warren Buffett, Berkshire Hathaway 2000 shareholder letter      |
+-----------------------------------------------------------------------+
```

#### Why EV/EBITDA is Dangerous:
1. **Ignores Maintenance Capex**: Equipment, data centers, and physical assets wear out. Depreciation reflects the economic consumption of capital; ignoring it treats asset replacement as non-existent.
2. **Favors Capital-Intensive Over Capital-Light Firms**:
   - Company A (Software): $100M EBITDA, $5M Capex -> True Cash Flow = $95M.
   - Company B (Trucking): $100M EBITDA, $60M Capex -> True Cash Flow = $40M.
   - Both trade at $10\times$ EV/EBITDA ($1,000M EV). Company A is far cheaper on cash flow after capex: EV/(EBITDA - Capex) is $10.5\times$ vs $25.0\times$.
3. **Susceptible to Working Capital Distortions**: EBITDA completely ignores cash consumed by swelling accounts receivable or inventory.

**The Solution**: Use **EV/EBIT** or **EV/EBITA** (EBITA adds back acquired intangible amortization but preserves physical plant depreciation).

### 5. Price-to-Book (P/B) and the Fundamental ROE Link

Price-to-Book ratio is mathematically driven by the spread between Return on Equity (ROE) and Cost of Equity ($K_e$):

$$\frac{P_0}{B_0} = \frac{\text{ROE} - g}{K_e - g} = 1 + \frac{\text{ROE} - K_e}{K_e - g}$$

```
+-----------------------------------------------------------------------+
|                  THE P/B - ROE VALUATION MATRIX                       |
+-----------------------------------------------------------------------+
| Condition          | Economic Status       | Multiple Implication    |
+--------------------+-----------------------+-------------------------+
| ROE > Ke           | Value Creator         | Justified P/B > 1.0     |
| ROE = Ke           | Value Neutral         | Justified P/B = 1.0     |
| ROE < Ke           | Value Destroyer       | Justified P/B < 1.0     |
+--------------------+-----------------------+-------------------------+
```

The Value Trap Warning:
A stock trading at $0.6\times$ Book Value is not necessarily cheap.
If the company earns an ROE of 4% while its cost of equity is 10%, its justified multiple is $0.04 / 0.10 = 0.40\times$ at zero growth, and $0.25\times$ at 2% growth, because growth destroys value when ROE is below $K_e$.
Buying low P/B without verifying that ROE exceeds $K_e$ is the fastest way to purchase decaying assets.

### 6. The PEG Ratio: Heuristic vs Reality

Popularized by Peter Lynch in *One Up on Wall Street* (1989), the PEG ratio compares P/E to annual growth:

$$\text{PEG} = \frac{\text{P/E Ratio}}{\text{Annual Earnings Growth Rate } (g \times 100)}$$

Rules of thumb claim $\text{PEG} < 1.0$ indicates undervaluation.
However, the PEG heuristic makes flawed implicit assumptions:
- It assumes growth is linear and risk-free.
- It ignores the reinvestment required to achieve growth (ROIC).
- It breaks down completely at very low growth (P/E of 10 with 2% growth = PEG of 5.0) and very high growth (P/E of 80 with 100% growth = PEG of 0.8, hiding extreme terminal risk).

## Worked numerical case study

Compare two competitors in the industrial equipment sector (hypothetical companies; every figure below is hypothetical):

| Financial Metric | Precision Corp (A) | Heavy Gear Inc (B) |
|---|---|---|
| Share Price | $80.00 | $35.00 |
| Diluted Shares Outstanding | 50.0M | 100.0M |
| Market Capitalization | $4,000M | $3,500M |
| Total Debt (including leases) | $600M | $2,500M |
| Cash and Equivalents | $200M | $100M |
| Enterprise Value (EV) | $4,400M | $5,900M |
| Revenue | $2,000M | $3,000M |
| EBITDA | $440M (Margin: 22.0%) | $590M (Margin: 19.7%) |
| Depreciation & Amortization | $90M | $290M |
| Operating Income (EBIT) | $350M (Margin: 17.5%) | $300M (Margin: 10.0%) |
| Interest Expense | $30M | $150M |
| Pre-tax Income (EBT) | $320M | $150M |
| Net Income (Taxes 25%) | $240M | $112.5M |
| Book Value of Equity | $2,000M | $1,500M |

### Step 1: Compare Multiples Across Both Entities

```
+-----------------------------------------------------------------------+
|                        COMPARATIVE MULTIPLES TABLE                    |
+------------------------+-----------------------+----------------------+
| Valuation Multiple     | Precision Corp (A)    | Heavy Gear Inc (B)   |
+------------------------+-----------------------+----------------------+
| EV / Sales             | 2.20x                 | 1.97x                |
| EV / EBITDA            | 10.00x                | 10.00x               |
| EV / EBIT              | 12.57x                | 19.67x               |
| P / E (Market Cap/NI)  | 16.67x                | 31.11x               |
| P / B (Market Cap/BV)  | 2.00x                 | 2.33x                |
| ROE (Net Income / BV)  | 12.00%                | 7.50%                |
| Financial Leverage     | 0.91x Net Debt/EBITDA | 4.07x Net Debt/EBITDA|
+------------------------+-----------------------+----------------------+
```

### Forensic Analysis:
1. **The EV/EBITDA Mirage**:
   On an EV/EBITDA basis, both companies appear identical, trading at exactly $10.00\times$.
   A superficial analyst would conclude that Company B is equally attractive or even cheaper because its EV/Sales is lower ($1.97\times$ vs $2.20\times$).
2. **The EV/EBIT Reality**:
   Company B requires heavy capital reinvestment, consuming $290M in depreciation (9.7% of revenue) compared to Company A's $90M (4.5% of revenue).
   On EV/EBIT, Company A trades at **12.57x**, while Company B trades at a staggering **19.67x** (56% more expensive!).
3. **The Debt & P/E Distortion**:
   Company B carries $2,400M in net debt ($4.07\times$ EBITDA), consuming half of its operating profit in interest ($150M).
   This collapses Net Income to $112.5M, driving its P/E multiple to **31.11x**, while Company A trades at **16.67x**.
4. **ROE & P/B Audit**:
   Company A earns an ROE of 12.0% with minimal debt; Company B earns an ROE of only 7.5% despite extreme financial leverage.
   Verdict: Precision Corp (A) is cheaper on EV/EBIT, P/E and P/B, level on EV/EBITDA and dearer only on EV/Sales, and earns a higher ROE with far less leverage.

## Practice questions

> [!question]- mkt-val-097 | What is the fundamental relationship between valuation multiples and DCF models?
> Every valuation multiple is an algebraic simplification of a discounted cash flow model reflecting specific growth, payout, and cost of capital drivers.

> [!question]- mkt-val-098 | What is the Cardinal Sin of relative valuation?
> Mismatching enterprise-level metrics with equity-level metrics (e.g. EV / Net Income or Market Cap / EBITDA).

> [!question]- mkt-val-099 | Why are enterprise multiples (EV/EBIT) structurally superior to equity multiples (P/E)?
> They evaluate the operating business independent of capital structure, preventing leverage and interest rate differences from distorting comparisons.

> [!question]- mkt-val-100 | What is the formula for Enterprise Value (EV)?
> EV = Market Cap + Total Debt + Leases + Preferred Stock + Minority Interest - Cash and Marketable Securities - Non-Consolidated Affiliates.

> [!question]- mkt-val-101 | Why must investments in non-consolidated associates be subtracted from Enterprise Value?
> Because the operating earnings (EBIT/EBITDA) of associates are not included in consolidated operating profit, requiring their asset value to be removed for consistency.

> [!question]- mkt-val-102 | Why is EBITDA an imperfect proxy for operating cash flow?
> Because it ignores the physical cash required to replace aging fixed assets (capex) as well as investments in operating working capital and cash taxes.

> [!question]- mkt-val-103 | What is the difference between EV/EBITDA and EV/EBIT?
> EV/EBIT accounts for depreciation, reflecting the ongoing capital consumption required to maintain the enterprise's asset base.

> [!question]- mkt-val-104 | What is the mathematical relationship between the Price-to-Book (P/B) ratio and Return on Equity (ROE)?
> P/B = (ROE - g) / (Ke - g); justified P/B exceeds 1.0 if and only if ROE exceeds the cost of equity.

> [!question]- mkt-val-105 | What is a 'value trap' in the context of Price-to-Book multiples?
> A stock trading at a low P/B multiple that appears cheap, but earns an ROE well below its cost of capital, perpetually destroying economic value.

> [!question]- mkt-val-106 | What is the forward P/E ratio formula derived from the Gordon Growth model?
> Forward P/E = Payout Ratio / (Ke - g) = (1 - Reinvestment Rate) / (Ke - g).

> [!question]- mkt-val-107 | How does an increase in interest rates affect P/E multiples across the market?
> Higher interest rates increase the Cost of Equity (Ke), widening the denominator (Ke - g) and compressing P/E multiples.

> [!question]- mkt-val-108 | What is the PEG ratio and how is it calculated?
> PEG = (P/E Ratio) / (Annual EPS Growth Rate * 100), used as a rule-of-thumb metric for growth-adjusted valuation.

> [!question]- mkt-val-109 | What is a major mathematical flaw of the PEG ratio?
> It assumes linear risk and ignores return on invested capital; two companies growing at 20% can have identical PEG ratios even if one requires 5x more capital.

> [!question]- mkt-val-110 | Why do cyclical companies trade at deceptively low P/E multiples at the top of an economic cycle?
> Because peak earnings are unsustainably elevated; the market anticipates earnings mean reversion and prices the stock for future profit contraction.

> [!question]- mkt-val-111 | Why do cyclical companies trade at deceptively high P/E multiples at the trough of an economic cycle?
> Because trough earnings are depressed; the market anticipates future economic recovery and prices in the upcoming rebound in operating cash flows.

> [!question]- mkt-val-112 | What is the Shiller CAPE ratio?
> The Cyclically Adjusted Price-to-Earnings ratio (Campbell and Shiller 1998), which divides the real (inflation-adjusted) price by the 10-year average of real earnings to smooth the business cycle.

> [!question]- mkt-val-113 | How does financial leverage artificially inflate Return on Equity (ROE)?
> By funding assets with low-cost debt, shrinking the equity denominator; however, it elevates financial risk and the required cost of equity (Ke).

> [!question]- mkt-val-114 | What is the EV/Sales multiple and when is it appropriately utilized?
> Comparing enterprise value to revenue; used primarily for early-stage companies or unprofitable software firms where margins are negative.

> [!question]- mkt-val-115 | What is the danger of using EV/Sales without adjusting for gross margins?
> A company with a 20% gross margin trading at 2x sales is far more expensive than a company with an 80% gross margin trading at 2x sales.

> [!question]- mkt-val-116 | What is EV/Invested Capital and what does it measure?
> It compares the market enterprise value to the capital invested in operating assets; it is a rough analogue of Tobin's q, which divides by replacement cost rather than book capital.

> [!question]- mkt-val-117 | How does a company's ROIC dictate its justified EV/Invested Capital multiple?
> EV/IC = (ROIC - g) / (WACC - g); when ROIC exceeds WACC, justified EV/IC is greater than 1.0.

> [!question]- mkt-val-118 | What is the EV/EBITA multiple and why do private equity analysts prefer it?
> It adds back non-cash amortization of acquired intangibles from past M&A, but retains real physical depreciation, avoiding distortions from purchase accounting.

> [!question]- mkt-val-119 | What are non-controlling (minority) interests on the balance sheet?
> The portion of consolidated equity in a subsidiary owned by external third parties, included in Enterprise Value because 100% of the subsidiary's cash flow is in EBITDA.

> [!question]- mkt-val-120 | Why must operating lease liabilities be added to debt in Enterprise Value under ASC 842?
> Because lease obligations are debt-like contractual financing commitments; ASC 842 still books operating-lease cost as a single straight-line operating expense inside EBITDA (only IFRS 16 and finance leases split it into interest and depreciation), so adding the lease liability to EV requires adding rent back to the denominator (EV/EBITDAR) to keep the multiple consistent.

> [!question]- mkt-val-121 | What is a 'pure play' comparable company?
> A peer company operating exclusively in the same industry segment, without distortion from unrelated business units or conglomerate divisions.

> [!question]- mkt-val-122 | How do share buybacks impact historical P/E comparisons?
> Buybacks reduce share count and artificially boost EPS growth, making EPS outpace net income growth and distorting multi-year multiple trends.

> [!question]- mkt-val-123 | What is multiple expansion vs multiple contraction?
> Multiple expansion occurs when market valuation multiples increase (e.g. P/E from 15x to 22x); contraction occurs when multiples shrink, reducing returns.

> [!question]- mkt-val-124 | What proportion of long-term equity returns is driven by multiple expansion versus fundamental earnings growth?
> Annual return is roughly dividend yield plus earnings growth plus the annualized change in the multiple, and the multiple term shrinks with the horizon.
> A re-rating from 15x to 22x adds 46.67% in one year but only 3.90% a year over 10 years and 1.93% a year over 20, so over long horizons earnings growth and dividends dominate unless multiples trend.

> [!question]- mkt-val-125 | How does working capital intensity affect the justified EV/EBIT multiple?
> High working capital intensity requires more cash reinvestment per dollar of EBIT, depressing free cash flow conversion and reducing justified multiples.

> [!question]- mkt-val-126 | Why should non-operating or excess cash be deducted when calculating Enterprise Value?
> Because excess cash is not required to generate operating earnings (EBIT/EBITDA); netting it isolates the net cost to acquire the operating core.

> [!question]- mkt-val-127 | What is the difference between trailing P/E and forward P/E?
> Trailing P/E uses historical EPS over the past 12 months; forward P/E uses consensus forecast EPS over the next 12 months.

> [!question]- mkt-val-128 | What is the ultimate rule for conducting peer multiple benchmarking?
> Benchmark only against peers with comparable return on capital, margin structure, capital intensity, and structural competitive advantages.

> [!question]- mkt-val-262 | A stock re-rates from 15x to 22x earnings. How much does that add to annual return over 1, 10 and 20 years?
> (22 / 15)^(1/T) - 1: 46.67% over one year, 3.90% a year over 10 years, and 1.93% a year over 20 years.
> A one-off re-rating matters a lot for short holding periods and little for long ones.

---

## In this repo and The-Distinguished-Engineer

- Code: [`../../code/mkt_val_04_multiples.py`](../../code/mkt_val_04_multiples.py) prints and asserts every number on this page: the comparative multiples table in exact fractions, justified P/B and forward P/E against a year-by-year clean-surplus dividend simulation, the PEG and EBITDA examples, and the re-rating contribution by bisection against its closed form.
- Related notes: [Cost of Capital, WACC, and Terminal Value Traps](02-Cost-of-Capital-WACC-and-Terminal-Value-Traps.md), [Specialized Valuation](07-Specialized-Valuation-Financials-Cyclicals-and-Loss-Makers.md).

## Further reading

- Berkshire Hathaway. Shareholder letters, 2000 and 2002. berkshirehathaway.com/letters.
- Campbell, J. Y., & Shiller, R. J. (1998). Valuation ratios and the long-run stock market outlook. *Journal of Portfolio Management*, 24(2), 11-26.
- Damodaran, A. (2012). *Investment Valuation: Tools and Techniques for Determining the Value of Any Asset* (3rd ed.). John Wiley & Sons. Ch. 17 (relative valuation), Ch. 18 (earnings multiples), Ch. 19 (book value multiples).
- Fernandez, P. (2002). *Valuation Methods and Shareholder Value Creation*. Academic Press.
- Koller, T., Goedhart, M., & Wessels, D. (2020). *Valuation: Measuring and Managing the Value of Companies* (7th ed.). John Wiley & Sons. Ch. 18 (using multiples).
- Lynch, P. (1989). *One Up on Wall Street*. Simon & Schuster.
- Shiller, R. J. (2000). *Irrational Exuberance*. Princeton University Press.
