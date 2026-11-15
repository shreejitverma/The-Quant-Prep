---
type: guide
title: "Case File 05: 2008 Global Financial Crisis and Lehman Brothers Collapse"
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
tags: [market-history, gfc-2008, lehman-brothers, subprime-mortgage, cdo, repo-run, systemic-risk, case-study]
---

# Case File 05: 2008 Global Financial Crisis and Lehman Brothers Collapse

## Executive Summary

On September 15, 2008, Lehman Brothers Holdings Inc. filed for Chapter 11 bankruptcy, the largest bankruptcy filing in US history; its last quarterly report, for the quarter ended May 31, 2008, showed total assets of $639.4 billion.
At its fiscal year-end of November 30, 2007, Lehman reported total assets of $691.1 billion against stockholders' equity of $22.5 billion, a leverage ratio of 30.7 times.
The next day the Reserve Primary Fund, a money market fund holding $785 million of Lehman debt, wrote that debt down to zero and its net asset value fell to 97 cents a share ("breaking the buck"), which set off a run on prime money market funds.
The crisis grew out of the securitisation of subprime and other non-traditional mortgages into mortgage-backed securities and collateralised debt obligations (CDOs), funded with short-term wholesale borrowing such as repo.
The government response included the conservatorship of Fannie Mae and Freddie Mac, an $85 billion Federal Reserve credit facility for AIG, and the $700 billion Troubled Asset Relief Program (TARP).

---

## Primary Sources and Chronology

Sources used on this page: Financial Crisis Inquiry Commission, *The Financial Crisis Inquiry Report* (January 2011); Report of Anton R. Valukas, Examiner, *In re Lehman Brothers Holdings Inc.* (March 11, 2010), volume 3, section III.A.4 (Repo 105); Lehman Brothers Holdings Inc., Form 10-K for fiscal 2007 (Selected Financial Data) and Form 10-Q for the quarter ended May 31, 2008; SEC litigation release LR-21025 (Reserve Primary Fund); Federal Reserve Board press releases of March 2008 and September 16, 2008; Emergency Economic Stabilization Act of 2008; Gary Gorton and Andrew Metrick, "Securitized Banking and the Run on Repo", *Journal of Financial Economics* 104(3), 2012; David X. Li, "On Default Correlation: A Copula Function Approach", *Journal of Fixed Income* 9(4), 2000.

- **April 2007**: Subprime lender New Century Financial files for bankruptcy as delinquencies on recent subprime loans rise.
- **August 9, 2007**: BNP Paribas suspends the calculation of net asset value for three funds (Parvest Dynamic ABS, BNP Paribas ABS EURIBOR and BNP Paribas ABS EONIA), citing the impossibility of valuing their US asset-backed holdings (FCIC, citing the BNP Paribas press release).
- **March 16, 2008**: JPMorgan Chase agrees to acquire Bear Stearns, initially at $2 a share (raised to $10 a share on March 24), with Federal Reserve financing of a portfolio of Bear Stearns assets.
- **September 7, 2008**: The Federal Housing Finance Agency places Fannie Mae and Freddie Mac into conservatorship.
- **September 14, 2008**: Talks at the Federal Reserve Bank of New York fail to find a buyer for Lehman without government support (FCIC).
- **Monday, September 15, 2008**:
  - Lehman Brothers Holdings Inc. files for Chapter 11 bankruptcy.
  - Bank of America announces an agreement to acquire Merrill Lynch in an all-stock transaction valued at about $50 billion.
  - The Dow Jones Industrial Average falls 504.48 points, from 11,421.99 to 10,917.51, or 4.42%.
- **Tuesday, September 16, 2008**:
  - After the close, Reserve Management announces that the Primary Fund's $785 million of Lehman paper is valued at zero, and the fund breaks the buck at a net asset value of 97 cents (FCIC; SEC).
  - The Federal Reserve authorises the New York Fed to lend up to $85 billion to AIG, in exchange for a 79.9 percent equity interest.
- **October 3, 2008**: The Emergency Economic Stabilization Act of 2008 is signed into law, authorising the $700 billion TARP.
- **March 9, 2009**: The S&P 500 closes at 676.53, its crisis low, 56.78% below its October 9, 2007 record close of 1,565.15.

---

## Market Backdrop and Structural Vulnerabilities

### 1. The Securitisation Machine
Mortgage originators made large volumes of subprime, low-documentation and adjustable-rate loans in the mid-2000s, and these loans were pooled into residential mortgage-backed securities (RMBS) and cut into tranches by seniority (FCIC).
The tranche sizes below are a hypothetical illustration of the structure, not a specific deal:

```
+-----------------------------------------------------------------------+
|        MORTGAGE SECURITIZATION TRANCHE WATERFALL (HYPOTHETICAL)       |
+-----------------------------------------------------------------------+
| Senior Tranche (AAA): Paid first; 80% of notional                     |
| Mezzanine Tranche (BBB): Absorbs losses after equity; 15% of notional |
| Equity / Residual (Unrated): First-loss piece; 5% of notional         |
+-----------------------------------------------------------------------+
```

Lower-rated mezzanine tranches from many RMBS deals were themselves pooled into CDOs, whose senior tranches were often rated AAA (FCIC).
The value of such senior tranches depends heavily on the assumed correlation of defaults across the pool; one-factor Gaussian copula models in the spirit of Li (2000) became the standard market tool for this, and assumptions calibrated to regional housing downturns understated the risk of a national one.

### 2. Short-Term Wholesale Funding
Investment banks financed large balance sheets with short-term borrowing, much of it repo secured on securities.
Lehman's reported leverage ratio (total assets divided by stockholders' equity) was 30.7 times at November 30, 2007 (Form 10-K).
Gorton and Metrick (2012) document that haircuts on repo collateral rose sharply during the crisis, which is economically a run: a higher haircut forces the borrower to fund more of each asset itself or sell.

### 3. Repo 105
The Valukas examiner's report found that Lehman used "Repo 105" transactions to remove securities inventory temporarily from its balance sheet at quarter-ends: about $38.6 billion in the fourth quarter of 2007, $49.1 billion in the first quarter of 2008 and $50.38 billion in the second quarter of 2008.
The transactions were run through Lehman Brothers International (Europe) in London under a true-sale opinion from the law firm Linklaters under English law, and were not disclosed in Lehman's filings.

### 4. Credit Default Swaps and AIG
AIG Financial Products sold large amounts of credit default swap protection on super-senior CDO tranches (FCIC).
The contracts required AIG to post collateral when the referenced securities lost value or when AIG's own credit rating was cut, so falling CDO values and downgrades in 2008 produced collateral calls that AIG could not meet without government support.

---

## Microstructure Breakdown and Liquidity Evaporation

```
+-----------------------------------------------------------------------+
|               THE 2008 SHADOW BANKING REPO RUN CASCADE                |
+-----------------------------------------------------------------------+
| 1. Mortgage Delinquencies Rise                                        |
|    Home prices fall; marks on mortgage securities drop                |
|                                                                       |
| 2. Repo Haircut Shock                                                 |
|    Lenders raise haircuts on structured collateral                    |
|    (hypothetical: from 2% to 25%)                                     |
|                                                                       |
| 3. Funding Gap                                                        |
|    At a 25% haircut, $133.33 of collateral backs each $100 borrowed   |
|                                                                       |
| 4. Lehman Bankruptcy                                                  |
|    Counterparties pull funding from other dealers                     |
|                                                                       |
| 5. Money Market Run                                                   |
|    Reserve Primary Fund breaks the buck; investors pull money from    |
|    prime funds, which stop buying commercial paper                    |
|                                                                       |
| 6. Global Credit Freeze                                               |
|    Firms struggle to roll short-term funding; the Fed steps in        |
+-----------------------------------------------------------------------+
```

After the Primary Fund broke the buck, the run spread to money market funds with no direct Lehman exposure, as investors withdrew for fear that others would withdraw first (FCIC).

---

## Quantitative Autopsy

Consider a hypothetical investment bank with assets $A = \$600 \text{ billion}$, debt $D = \$580 \text{ billion}$ and equity $E = \$20 \text{ billion}$:
$$\text{Leverage Ratio} = \frac{A}{E} = \frac{600}{20} = 30x$$
Suppose 10% of its assets are subprime-linked securities ($A_{\text{sub}} = \$60 \text{ billion}$).
A 35% write-down of those securities ($0.35 \times 60 = \$21 \text{ billion}$) cuts total assets to:
$$A_{\text{new}} = 600 - 21 = \$579 \text{ billion}$$
and equity to:
$$E_{\text{new}} = A_{\text{new}} - D = 579 - 580 = -\$1 \text{ billion}$$
A 3.5% fall in total assets wipes out all of the equity, because at 30 times leverage a loss of $1/30 = 3.33\%$ of assets is enough.

The repo haircut arithmetic is $\$100 / (1 - 0.25) = \$133.33$ of collateral per $\$100$ of cash borrowed, against $\$100 / (1 - 0.02) = \$102.04$ at a 2% haircut.
Lehman's leverage is $691{,}063 / 22{,}490 = 30.73$ from the 10-K figures in millions of dollars, which the company reported as 30.7x, and the S&P 500 fall is $1 - 676.53/1{,}565.15 = 56.78\%$.

---

## Regulatory and Structural Legacy

1. **Dodd-Frank Wall Street Reform and Consumer Protection Act (July 2010)**:
   - **Volcker Rule (section 619)**: Restricts proprietary trading by banking entities and their investments in hedge funds and private equity funds.
   - **Stress testing (section 165)**: Requires supervisory and company-run stress tests for large banks; the Federal Reserve's annual Comprehensive Capital Analysis and Review (CCAR), begun in 2011, ties capital plans to these tests.
   - **Orderly Liquidation Authority (Title II)**: Lets the FDIC wind down a failing systemically important financial company.
2. **Central clearing of OTC derivatives**: Title VII of Dodd-Frank in the US and EMIR in the EU require standardised swaps to be cleared through central counterparties.
3. **Basel III**: Raised the minimum common equity requirement from 2% to 4.5% of risk-weighted assets plus a 2.5% capital conservation buffer, and added the Liquidity Coverage Ratio (enough high-quality liquid assets to survive a 30-day stress) and the Net Stable Funding Ratio.
4. **Money market fund reform**: The SEC's 2014 rules required a floating net asset value for institutional prime funds and allowed liquidity fees and redemption gates; the SEC's 2023 amendments removed the redemption gates.

---

## Lessons for Traders and Risk Managers

- **Funding Risk Is Existential**: Sound assets financed with short-term borrowing that cannot be rolled must be sold at distressed prices.
- **Model Risk and Correlation Blindness**: Correlation assumptions calibrated in calm, regional downturns fail in a national one.
- **Counterparty Credit Risk Is Real**: Collateralise exposures and monitor the counterparty, not just the trade.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-017 | What was the reported balance sheet leverage ratio of Lehman Brothers at its last fiscal year-end (November 30, 2007) before its September 2008 bankruptcy?
> 30.7 times: total assets of $691.1 billion against stockholders' equity of $22.5 billion (Lehman Form 10-K for fiscal 2007).

> [!question]- mkt-his-018 | What occurred when the Reserve Primary Fund 'broke the buck' on September 16, 2008?
> Its $785 million of Lehman debt was written down to zero and its net asset value fell to 97 cents a share, and the run spread to other prime money market funds, including ones with no Lehman exposure.

> [!question]- mkt-his-019 | What was the fundamental flaw in David X. Li's Gaussian Copula model for rating CDO tranches?
> Used with correlations calibrated to calm periods and regional downturns, the one-factor Gaussian copula understated the chance of defaults rising together in a national house price decline, which is the risk that senior tranches carry.

> [!question]- mkt-his-020 | What is the Liquidity Coverage Ratio (LCR) introduced under Basel III following the 2008 crisis?
> A requirement that banks hold enough unencumbered high-quality liquid assets to meet net cash outflows over a 30-day stress scenario.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_hist_05_gfc_2008.py`](../code/mkt_hist_05_gfc_2008.py) prints and asserts every number on this page: the balance-sheet example is evaluated line by line and checked against the leverage identity, the haircut arithmetic is checked by reconstructing the loan from the collateral, Lehman's leverage is recomputed from the 10-K figures, and the index changes are recomputed from the cited closes in exact decimal arithmetic.
- Related notes: [Case File 03: LTCM](03-1998-LTCM-Collapse-and-Relative-Value-Arbitrage.md), [Case File 10: 2022 UK LDI Crisis](10-2022-UK-LDI-Pension-Crisis-and-Gilt-Spiral.md).
