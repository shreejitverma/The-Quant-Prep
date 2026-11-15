---
type: guide
title: "Case File 01: 1929 Wall Street Crash and the Great Depression"
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
tags: [market-history, 1929-crash, great-depression, margin-calls, leverage, ticker-lag, case-study]
---

# Case File 01: 1929 Wall Street Crash and the Great Depression

## Executive Summary

The Dow Jones Industrial Average closed at a peak of 381.17 on September 3, 1929, and by its November 13 close of 198.69 it had lost 47.87% of its value.
The decline continued until July 8, 1932, when the Dow closed at 41.22, a peak-to-trough fall of 89.19%; it did not regain its 1929 high until November 23, 1954.
Stock purchases on margin, where buyers typically put down 10 percent and borrowed the rest, turned the price fall into forced selling and losses for the lenders.
The crash was followed by waves of bank failures (about 9,000 bank suspensions in 1930 to 1933 by the FDIC's count) and a fall in the money supply of nearly 30 percent from the fall of 1930 to the winter of 1933.
The policy response built the modern US framework: the Banking Act of 1933 (Glass-Steagall, which created the FDIC), the Securities Act of 1933, and the Securities Exchange Act of 1934, which created the SEC and gave the Federal Reserve authority over margin requirements.

---

## Primary Sources and Chronology

Sources used on this page: Gary Richardson, Alejandro Komai, Michael Gou and Daniel Park, "Stock Market Crash of 1929", Federal Reserve History (written as of November 22, 2013); Gary Richardson, "The Great Depression" and "Banking Panics of 1930-31", Federal Reserve History (2013); FDIC, *A Brief History of Deposit Insurance in the United States* (1998), chapter 3; the Brady Report (Report of the Presidential Task Force on Market Mechanisms, January 1988), chapter 1; NBER US business cycle chronology; Federal Reserve Regulation T, 12 CFR 220.12; J. K. Galbraith, *The Great Crash, 1929* (1955); Dow closes of October 26 to 29, 1929 and July 8, 1932, and NYSE volume, as reported at the time (contemporary press reports).

- **August 1929**: The NBER dates the business-cycle peak of the Great Depression contraction to August 1929; the trough is March 1933.
- **September 3, 1929**: The Dow closes at its peak of 381.17, a six-fold rise from 63 in August 1921 (Federal Reserve History).
- **September 5, 1929**: The forecaster Roger Babson predicts a crash at the Annual National Business Conference (Federal Reserve History, endnote).
- **October 24, 1929 (Black Thursday)**: Heavy selling; a coalition of bankers attempts to restore confidence by publicly buying blocks of shares (Federal Reserve History).
- **October 28, 1929 (Black Monday)**: The Dow falls 38.33 points from the Saturday October 26 close of 298.97 to 260.64, a decline of 12.82% (closes from contemporary press reports; the Brady Report rounds the fall to 12.8 percent).
- **October 29, 1929 (Black Tuesday)**: The Dow falls another 30.57 points to 230.07, a decline of 11.73% (Brady Report: 11.7 percent), on New York Stock Exchange volume of about 16.4 million shares, a record at the time (contemporary press reports).
- **November 13, 1929**: The Dow closes at 198.69, "almost half" below its peak (Federal Reserve History).
- **July 8, 1932**: The Dow closes at 41.22, its lowest value of the twentieth century (contemporary press reports).
- **March 1933**: The commercial banking system collapses and the President declares a bank holiday on March 6 (FDIC).

---

## Market Backdrop and Structural Vulnerabilities

### 1. Margin Lending
Investors bought stock on margin: "Purchasers put down a fraction of the price, typically 10 percent, and borrowed the rest" (Federal Reserve History).
The borrowing was funded through loans to brokers and call loans, so a fall in stock prices threatened both the investor's equity and the lender's collateral.
At 10% down a buyer holds ten times leverage, so a 10% price fall wipes out the buyer's entire stake (see the Quantitative Autopsy).

### 2. Ticker Tape Lag and Information Delay
Prices reached brokerage offices by telegraphic ticker, and on the heaviest days the ticker ran far behind trading on the floor (Galbraith 1955).
Investors away from the floor therefore traded on stale prices, which made it hard to know whether a margin account was still solvent.

### 3. Leveraged Investment Trusts
Closed-end investment trusts, including the Goldman Sachs Trading Corporation and its offshoots Shenandoah and Blue Ridge, issued debt and preferred stock and bought shares of other trusts, layering leverage on leverage (Galbraith 1955, chapter "In Goldman, Sachs We Trust").
Layered leverage multiplies a fall in the underlying portfolio into a much larger fall in the common stock of the top trust.

---

## Microstructure Breakdown and Liquidity Evaporation

```
+-----------------------------------------------------------------------+
|                 1929 LIQUIDATION CASCADE FEEDBACK LOOP                |
+-----------------------------------------------------------------------+
| 1. Price Drop                                                         |
|    Margin accounts at 10% down lose equity ten times as fast          |
|                                                                       |
| 2. Margin Calls                                                       |
|    Borrowers who cannot post cash are sold out by their brokers       |
|                                                                       |
| 3. Forced Market Sell Orders                                          |
|    Liquidation orders arrive regardless of price                      |
|                                                                       |
| 4. Information Delay                                                  |
|    The ticker runs behind the floor; investors trade on stale prices  |
|                                                                       |
| 5. Further Price Falls                                                |
|    Losses spread to the lenders that financed the margin loans        |
+-----------------------------------------------------------------------+
```

Forced sellers do not choose their price, so each round of margin calls adds sell orders exactly when buyers are scarce.

---

## Quantitative Autopsy

The numbers below are a hypothetical illustration of 10% margin.
Let the initial stock price be $S_0 = 100$, bought with $10$ of equity and $90$ of borrowed money:
$$\text{Account Equity} = E(S) = S - \text{Debt} = S - 90$$
$$\text{Margin Percentage} = M(S) = \frac{S - 90}{S}$$
When the stock drops by 10% to $S_1 = 90$, equity drops to:
$$E(90) = 90 - 90 = 0$$
The investor loses 100% of the initial capital on a 10% price fall.
If the broker cannot sell immediately and the position is closed at $S_2 = 82$, the account finishes in deficit:
$$E(82) = 82 - 90 = -8$$
The lender now has an unsecured loss of $8$ per share, which is how margin losses pass from investors to brokers and their banks.

The headline index moves are computed from the cited Dow closes:
- Peak to November 13, 1929: $1 - 198.69/381.17 = 47.87\%$.
- Peak to July 8, 1932: $1 - 41.22/381.17 = 89.19\%$.
- October 28: $38.33/298.97 = 12.82\%$; October 29: $30.57/260.64 = 11.73\%$.
- Bank suspensions by year (FDIC, 1998): 1,350 (1930), 2,293 (1931), 1,453 (1932) and about 4,000 (1933), a total of 9,096 for 1930 to 1933.

---

## Regulatory and Structural Legacy

1. **Margin regulation**: Section 7 of the Securities Exchange Act of 1934 gave the Federal Reserve Board authority to set margin requirements, which it exercises through Regulation T; as of November 2026 the initial margin for a margin equity security is 50 percent of current market value (12 CFR 220.12).
2. **Banking Act of 1933 (Glass-Steagall)**: Separated commercial banking from investment banking and created the FDIC.
3. **Securities Act of 1933 and Securities Exchange Act of 1934**: Required registration and periodic disclosure for public securities and created the Securities and Exchange Commission.
4. **Pecora investigation**: The Senate Banking Committee inquiry of 1932 to 1934 into stock exchange practices exposed pools and abuses that shaped this legislation.

---

## Lessons for Traders and Risk Managers

- **Leverage converts drawdowns into ruin**: At $L$ times leverage a price fall of $1/L$ wipes out the equity; size positions so that the worst plausible gap does not reach that threshold.
- **Data lags in a crisis**: Feeds and order systems slow down exactly when volume peaks, so plan for trading on stale information.
- **Credit losses travel**: Losses on collateralised lending pass from borrowers to lenders, so equity stress becomes funding stress.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-001 | What was the typical down payment for buying stock on margin in the US leading up to the 1929 crash?
> Typically 10 percent, with the rest borrowed (Federal Reserve History), which is ten times leverage.

> [!question]- mkt-his-002 | How did ticker tape lag amplify the panic during Black Thursday and Black Tuesday?
> On the heaviest days the ticker ran far behind floor trading, so investors away from the floor did not know current prices or whether their margin accounts were still solvent, and sold on stale information.

> [!question]- mkt-his-003 | What authority over margin did the Federal Reserve receive after the 1929 crash?
> Section 7 of the Securities Exchange Act of 1934 gave the Federal Reserve Board authority to set margin requirements, exercised through Regulation T.

> [!question]- mkt-his-004 | What happened to the Dow Jones Industrial Average between its September 1929 peak and July 1932 trough?
> It fell from 381.17 (September 3, 1929) to 41.22 (July 8, 1932), a decline of 89.19%.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_hist_01_1929_crash.py`](../code/mkt_hist_01_1929_crash.py) prints and asserts every number on this page: each percentage decline is recomputed from the cited closes in exact decimal arithmetic and checked against the cited point changes and the Brady Report's and Federal Reserve History's rounded figures, the FDIC suspension total is summed from the yearly counts, and the margin example is evaluated on an explicit balance sheet.
- Related notes: [Case File 02: 1987 Black Monday](02-1987-Black-Monday-and-Portfolio-Insurance.md), [Case File 05: 2008 Global Financial Crisis](05-2008-Global-Financial-Crisis-and-Lehman-Collapse.md).
