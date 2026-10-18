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

On September 15, 2008, Lehman Brothers Holdings Inc. filed for Chapter 11 bankruptcy protection with $639 billion in assets and $619 billion in liabilities, marking the largest corporate bankruptcy in global history.
The bankruptcy triggered a catastrophic seizure across the global financial system: the overnight interbank lending market froze, the multi-trillion-dollar tri-party repo market experienced an unprecedented collateral run, and the Reserve Primary Money Market Fund "broke the buck" (falling to $0.97 per share).
The crisis was the culmination of a multi-year credit bubble engineered through the securitization of subprime residential mortgage loans into Residential Mortgage-Backed Securities (RMBS) and structured Collateralized Debt Obligations (CDOs).
Rating agencies (Moody's, S&P, Fitch) assigned AAA ratings to mezzanine CDO tranches under the flawed assumption of nationwide geographic housing diversification.
When US housing prices peaked in 2006 and mortgage default rates surged, investment banks holding leveraged proprietary inventory of CDOs and subprime paper suffered massive solvency and liquidity shortfalls.
The resulting panic required unprecedented sovereign bailouts: the federal takeover of Fannie Mae and Freddie Mac, an $85 billion emergency credit facility for American International Group (AIG), the $700 billion Troubled Asset Relief Program (TARP), and trillions in emergency liquidity facilities orchestrated by the Federal Reserve.

---

## Primary Sources and Chronology

- **February - April 2007**: Subprime mortgage lenders New Century Financial and Ownit Mortgage declare bankruptcy as early-vintage subprime loan delinquency rates spike.
- **June 20, 2007**: Bear Stearns pledges $3.2 billion to bail out two of its internal hedge funds (High-Grade Structured Credit Strategies Enhanced Leverage Fund) following margin calls from repo lenders.
- **August 9, 2007**: BNP Paribas freezes withdrawals across three investment funds with €2 billion in assets, stating that complete market illiquidity made it impossible to calculate a fair net asset value; European central banks and the Fed inject emergency liquidity.
- **March 16, 2008**: Bear Stearns suffers a fatal liquidity run on its overnight repo financing; the Federal Reserve engineers a shotgun sale to JPMorgan Chase at $2 per share (later revised to $10), backstopped by a $29 billion Fed loan facility (Maiden Lane I).
- **September 7, 2008**: The Federal Housing Finance Agency (FHFA) places government-sponsored enterprises Fannie Mae and Freddie Mac into federal conservatorship.
- **Sunday, September 14, 2008**: Emergency weekend negotiations at the Federal Reserve Bank of New York collapse when Barclays and Bank of America decline to acquire Lehman Brothers without federal government loss guarantees, which the Treasury refuses to provide.
- **Monday, September 15, 2008**:
  - 01:45 AM EST: Lehman Brothers Holdings Inc. files Chapter 11 bankruptcy.
  - Bank of America announces its acquisition of Merrill Lynch for $50 billion to preempt an imminent liquidity run.
  - The Dow Jones Industrial Average drops 504.48 points (-4.42%).
- **Tuesday, September 16, 2008**:
  - The Reserve Primary Fund (a $62 billion money-market mutual fund) writes off $785 million in Lehman commercial paper, dropping its net asset value to $0.97 per share ("breaking the buck") and sparking a $300 billion run on the money market fund industry.
  - The Federal Reserve authorizes an $85 billion loan to seize and rescue American International Group (AIG) to prevent the collapse of its Credit Default Swap (CDS) insurance obligations.
- **September 18, 2008**: Treasury Secretary Henry Paulson and Fed Chairman Ben Bernanke meet congressional leaders, warning that without immediate legislation, the US commercial financial system could freeze within days.
- **October 3, 2008**: Congress passes the Emergency Economic Stabilization Act of 2008, establishing the $700 billion Troubled Asset Relief Program (TARP).
- **March 6, 2009**: The S&P 500 touches its Great Financial Crisis intraday low of 666.79 (the "Devil's Low").
- **March 9, 2009**: The S&P 500 closes at its crisis closing low of 676.53, down 56.8% from its October 9, 2007 closing peak of 1,565.15.

---

## Market Backdrop and Structural Vulnerabilities

### 1. The Subprime Securitization Machine
Between 2001 and 2006, mortgage originators lowered underwriting standards, originating non-traditional mortgages:
- No-Doc / Low-Doc "Liar Loans"
- Subprime Adjustable Rate Mortgages (2/28 and 3/27 teaser rate ARMs)
- Negative amortization option ARMs
Wall Street investment banks purchased these loans, pooled them into Residential Mortgage-Backed Securities (RMBS), and sliced them into risk tranches:

```
+-----------------------------------------------------------------------+
|                 MORTGAGE SECURITIZATION TRANCHE WATERFALL             |
+-----------------------------------------------------------------------+
| Senior Tranche (AAA): Receives first cash flows; 80% of notional      |
| Mezzanine Tranche (BBB): Absorbs initial defaults; 15% of notional    |
| Equity / Residual (Unrated): First-loss piece; 5% of notional         |
+-----------------------------------------------------------------------+
```

To manufacture additional AAA assets, banks took the BBB-rated mezzanine tranches of multiple RMBS pools and repackaged them into **Collateralized Debt Obligations (CDOs)**.
Credit rating agencies evaluated these structures using Gaussian Copula correlation models (specifically David X. Li's 2000 model), assuming that default correlations between regional housing markets (e.g. Florida and Ohio) were low (0.2 to 0.3).
When nationwide home prices fell simultaneously, the correlation jumped to nearly 1.0, and AAA-rated CDO tranches suffered 80% to 100% principal write-downs.

### 2. Off-Balance-Sheet Vehicles (SIVs) and Tri-Party Repo
Investment banks operated with paper-thin equity capital cushions, running leverage ratios of 30-to-1 to 35-to-1:
- Lehman Brothers held $691 billion in assets against approximately $22 billion in equity (31.4x leverage).
- Much of this balance sheet was financed not through sticky retail customer deposits, but through overnight **tri-party repurchase agreements (repo)**.
Banks deposited collateral (MBS, CDOs, corporate bonds) with clearing banks (JPMorgan Chase, Bank of New York Mellon) and borrowed cash overnight from money market mutual funds.
When lenders grew concerned about the valuation of mortgage collateral, they demanded larger **haircuts** (expanding haircuts from 1% to 20% or 50%) or refused to roll repo loans entirely, creating an instantaneous liquidity run.

### 3. Credit Default Swaps (CDS) and AIG Financial Products
American International Group (AIG), an insurance company with a AAA credit rating, operated an unregulated derivatives unit in London (AIG Financial Products).
AIG sold hundreds of billions of dollars in unhedged Credit Default Swaps (CDS) insuring AAA-rated super-senior CDO tranches, collecting billions in premium income without posting collateral.
AIG's swap contracts contained covenants requiring AIG to post cash collateral if:
1. The underlying insured CDOs were downgraded by rating agencies.
2. AIG's own corporate credit rating was downgraded.
When both occurred simultaneously in September 2008, AIG faced an immediate $32 billion collateral cash shortfall that it could not fund, threatening the balance sheets of every major European and American dealer bank holding AIG protection.

---

## Microstructure Breakdown and Liquidity Evaporation

```
+-----------------------------------------------------------------------+
|               THE 2008 SHADOW BANKING REPO RUN CASCADE                |
+-----------------------------------------------------------------------+
| 1. Subprime Delinquencies Rise                                        |
|    Case-Shiller Home Price Index falls nationwide; CDO marks drop     |
|                                                                       |
| 2. Repo Haircut Shock                                                 |
|    Money funds raise repo haircuts on structured paper from 2% to 25% |
|                                                                       |
| 3. Severe Cash Depletion                                              |
|    Borrower must pledge $133.33 of assets for every $100 borrowed     |
|                                                                       |
| 4. Lehman Bankruptcy Announcement                                     |
|    Overnight repo lines pulled completely; interbank LIBOR-OIS spikes |
|                                                                       |
| 5. Money Market Run                                                   |
|    Reserve Primary Fund breaks the buck; institutional investors      |
|    withdraw $300B from prime money funds, freezing commercial paper   |
|                                                                       |
| 6. Global Credit Freeze                                               |
|    Corporations cannot roll 30-day payroll paper; Fed must step in    |
+-----------------------------------------------------------------------+
```

The TED spread (difference between 3-month USD LIBOR and 3-month Treasury bill yield), a direct measure of perceived credit risk in the interbank banking system, surged from a normal level of 25 basis points to an all-time peak of 464 basis points on October 10, 2008.
Banks hoarded cash reserves at the central bank and completely refused to lend to one another.

---

## Quantitative Autopsy

Consider an investment bank with balance sheet assets $A = \$600 \text{ billion}$, funded by liabilities (debt) $D = \$580 \text{ billion}$ and equity capital $E = \$20 \text{ billion}$:
$$\text{Leverage Ratio} = \frac{A}{E} = \frac{600}{20} = 30x$$
Assume the asset base contains 10% of subprime-linked securities and structured CDOs ($A_{\text{sub}} = \$60 \text{ billion}$):
If structured credit markets write down these assets by 35% ($0.35 \times 60 = \$21 \text{ billion}$), the bank's total asset value drops to:
$$A_{\text{new}} = 600 - 21 = \$579 \text{ billion}$$
The revised equity capital is:
$$E_{\text{new}} = A_{\text{new}} - D = 579 - 580 = -\$1 \text{ billion}$$
A minor 3.5% decline in total firm assets completely wipes out 100% of the institution's equity capital, rendering the bank legally insolvent.
In addition, under Repo 105 transactions, Lehman temporarily transferred up to $50 billion of liquid securities to offshore entities right before quarterly balance sheet reporting dates, misclassifying short-term financings as true sales to disguise its true leverage.

---

## Regulatory and Structural Legacy

The 2008 financial crisis generated the most extensive regulatory overhaul since the Great Depression:
1. **Dodd-Frank Wall Street Reform and Consumer Protection Act (2010)**:
   - **Volcker Rule**: Prohibited insured depository banks from engaging in proprietary trading or owning hedge funds and private equity funds.
   - **Comprehensive Capital Analysis and Review (CCAR)**: Annual supervisory stress testing mandating severe macroeconomic and financial market shock simulations.
   - **Orderly Liquidation Authority (Title II)**: Framework for the FDIC to wind down systemically important financial institutions without taxpayer bailouts.
2. **Mandatory Central Clearing for Over-the-Counter Derivatives**: Enforced through Title VII of Dodd-Frank and EMIR in Europe; standardized CDS and interest rate swaps must clear through registered Central Counterparties (CCPs).
3. **Basel III Capital and Liquidity Standards**:
   - Tripled Tier 1 Common Equity requirements.
   - Introduced the Liquidity Coverage Ratio (LCR) requiring banks to hold enough High-Quality Liquid Assets (HQLA) to survive a 30-day acute stress event.
   - Introduced the Net Stable Funding Ratio (NSFR) to penalize excessive reliance on short-term wholesale overnight repo funding.
4. **Money Market Fund Structural Reform**: The SEC mandated floating Net Asset Values (NAV) for institutional prime money market funds and established liquidity fees and redemption gates to prevent runs.

---

## Lessons for Traders and Risk Managers

- **Funding Risk Is Existential**: A portfolio of fundamentally sound assets can be liquidated at bankruptcy prices if financed with short-term borrowing that fails to roll.
- **Model Risk and Correlation Blindness**: Correlation models calibrated during tranquil bull regimes fail catastrophically when an underlying asset class experiences structural regime shifts.
- **Counterparty Credit Risk Is Real**: Never assume that clearing firms, prime brokers, or insurance underwriters are too big to fail; counterparty exposures must be collateralized daily with strict independent custody.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-017 | What was the balance sheet leverage ratio of Lehman Brothers immediately prior to its September 2008 bankruptcy?
> Approximately 31.4-to-1 ($691 billion in assets against roughly $22 billion in equity).

> [!question]- mkt-his-018 | What occurred when the Reserve Primary Fund 'broke the buck' on September 16, 2008?
> Its NAV fell to $0.97 per share due to losses on Lehman commercial paper, sparking a massive $300 billion run across institutional prime money market funds.

> [!question]- mkt-his-019 | What was the fundamental flaw in David X. Li's Gaussian Copula model for rating CDO tranches?
> It assumed low and stable default correlation across regional real estate markets, ignoring the systemic risk of nationwide home price deflation.

> [!question]- mkt-his-020 | What is the Liquidity Coverage Ratio (LCR) introduced under Basel III following the 2008 crisis?
> A requirement that banks hold sufficient unencumbered High-Quality Liquid Assets (HQLA) to withstand a 30-day severe liquidity stress scenario.
