---
type: guide
title: "Case File 04: 2000 Dot-Com Bubble and Telecom Crash"
track: [quant-trader, quant-research, quant-risk]
tier: core
status: solid
tags: [market-history, dot-com-bubble, tech-crash, telecom-debt, lockup-expiration, valuation-bubble, case-study]
---

# Case File 04: 2000 Dot-Com Bubble and Telecom Crash

## Executive Summary

The Nasdaq Composite closed at a record 5,048.62 on March 10, 2000, after an intraday high of 5,132.52, and fell to a closing low of 1,114.11 on October 9, 2002, a decline of 77.93%.
It did not close above its March 2000 record until April 23, 2015.
The bubble rested on expectations for internet companies, many of which had no profits, and on a market for initial public offerings that rewarded growth narratives over cash flow.
Between June 1999 and May 2000 the Federal Reserve raised the federal funds target six times, from 4.75% to 6.50%, and as funding markets closed, companies that burned cash had to raise capital or fail.
The aftermath produced the Sarbanes-Oxley Act of 2002 after the Enron and WorldCom frauds, and the 2003 Global Research Analyst Settlement separating research from investment banking.

---

## Primary Sources and Chronology

Sources used on this page: Nasdaq Composite closes as reported at the time (for example *Fortune*, April 23, 2015, on the first close above 5,048.62); Federal Reserve FOMC statements of 1999 and 2000; Alan Greenspan, "The Challenge of Central Banking in a Democratic Society", speech at the American Enterprise Institute, December 5, 1996; *United States v. Microsoft*, Conclusions of Law, April 3, 2000; SEC Release 33-7881 (August 2000) adopting Regulation FD and Rule 10b5-1; SEC press release 2003-54 (April 28, 2003); Sarbanes-Oxley Act of 2002.

- **August 9, 1995**: Netscape Communications goes public; shares offered at $28 open at $71 after a delay of nearly two hours and close at $58.25, a market value of more than $2 billion (contemporary press reports).
- **December 5, 1996**: Alan Greenspan asks in his American Enterprise Institute speech how we would know when "irrational exuberance has unduly escalated asset values".
- **June 30, 1999**: The FOMC raises the federal funds target by 25 basis points to 5.00%, the first of six increases.
- **January 10, 2000**: America Online announces an all-stock agreement to combine with Time Warner.
- **March 10, 2000**: The Nasdaq Composite reaches an intraday high of 5,132.52 and a record close of 5,048.62.
- **March 20, 2000**: *Barron's* publishes "Burning Up" by Jack Willoughby, reporting a Pegasus Research International study of 207 internet companies that found at least 51 would run out of cash within twelve months.
- **April 3, 2000**: Judge Thomas Penfield Jackson rules in *United States v. Microsoft* that Microsoft violated sections 1 and 2 of the Sherman Act.
- **May 16, 2000**: The FOMC raises the federal funds target by 50 basis points to 6.50%, the sixth increase since June 1999.
- **November 2000 to July 2001**: Pets.com announces its liquidation (November 2000), eToys files for bankruptcy (March 2001) and Webvan files for bankruptcy (July 2001).
- **October 9, 2002**: The Nasdaq Composite closes at 1,114.11, its bear-market low.

---

## Market Backdrop and Structural Vulnerabilities

### 1. Valuation Without Earnings
Many internet companies went public with little revenue and no profits, and analysts and investors leaned on traffic and user-growth measures instead of earnings or free cash flow.
A company valued on a distant cash flow is a long-duration asset, so its price is very sensitive to the discount rate and to the growth assumed (see the Quantitative Autopsy).

### 2. Small Floats and Lockups
Many IPOs sold only a small share of the company to the public, while insiders and venture investors agreed to lockups (commonly 180 days) before they could sell.
A small float limits the supply of shares at first and can produce large first-day gains; when lockups expire, the supply of tradable shares rises.

### 3. Cash Burn and Closing Funding Markets
The Barron's study of March 20, 2000 is a direct measure of the vulnerability: at least 51 of 207 internet companies, about a quarter, were on course to exhaust their cash within twelve months.
Companies with negative operating cash flow depend on new equity or debt, so when IPO and follow-on markets closed, many could not survive.

### 4. Telecom Overbuild and Accounting Fraud
Telecom carriers borrowed heavily to build fibre networks ahead of demand, and several later failed.
WorldCom, the largest of the failures, overstated its earnings by classifying operating costs as capital expenditure, which the SEC charged in its civil complaint of June 26, 2002.

---

## Microstructure Breakdown and Liquidity Evaporation

```
+-----------------------------------------------------------------------+
|                    THE DOT-COM CASH BURN DEATH SPIRAL                 |
+-----------------------------------------------------------------------+
| 1. Fed Tightening (4.75% -> 6.50%, June 1999 to May 2000)             |
|    Higher discount rates hit long-duration growth stocks hardest      |
|                                                                       |
| 2. Capital Market Window Closes                                       |
|    IPOs and follow-on offerings dry up                                |
|                                                                       |
| 3. Cash Burn                                                          |
|    Companies with negative operating cash flow run down their cash    |
|                                                                       |
| 4. Lockup Expirations                                                 |
|    Insider shares become saleable into falling prices                 |
|                                                                       |
| 5. Corporate Failure                                                  |
|    Liquidation or bankruptcy; equity goes to zero                     |
+-----------------------------------------------------------------------+
```

A company whose every sale loses cash does not suffer a recession-style earnings dip when funding stops; it runs out of cash and fails.

---

## Quantitative Autopsy

The Gordon growth formula values a cash flow stream growing at $g$ forever and discounted at $r > g$:
$$P_0 = \frac{\text{FCF}_1}{r - g}$$
The inputs below are hypothetical, chosen to show the sensitivity, not estimates of 1999 market expectations.
With $r = 16\%$ and $g = 15\%$ the spread is $1.0\%$:
$$P_0 = \frac{\text{FCF}_1}{0.01} = 100 \times \text{FCF}_1$$
If the required return rises to $r = 20\%$ and expected growth falls to $g = 8\%$, the spread becomes:
$$(r - g) = 0.20 - 0.08 = 12.0\%$$
and the multiple collapses:
$$\frac{P_{\text{new}}}{P_{\text{old}}} = \frac{1 / 0.12}{1 / 0.01} = \frac{8.33}{100.0} = 0.0833 \quad (-91.67\%)$$
No change in the current cash flow is needed for a fall of this size; a narrow $(r - g)$ spread is what makes long-duration equity fragile.

The headline numbers follow from the cited data: $1 - 1{,}114.11/5{,}048.62 = 77.93\%$; the six FOMC moves (25, 25, 25, 25, 25 and 50 basis points) total 175 basis points, from 4.75% to 6.50%; and Netscape's first-day close of $58.25 was 108.04% above the $28 offer price.

---

## Regulatory and Structural Legacy

1. **Sarbanes-Oxley Act of 2002**: Enacted after the Enron and WorldCom frauds; section 302 requires CEO and CFO certification of periodic reports and section 404 requires management's assessment of internal control over financial reporting.
2. **Global Research Analyst Settlement (2003)**: On April 28, 2003, the SEC, NASD, NYSE and state regulators announced settlements with ten investment firms totalling about $1.4 billion, with reforms separating research from investment banking (SEC press release 2003-54).
3. **Regulation FD (2000)**: Adopted by the SEC in August 2000 to stop issuers disclosing material non-public information selectively to analysts and investors before the public.
4. **Rule 10b5-1 (2000)**: Adopted in the same release, it provides an affirmative defence for insiders trading under a plan set up before they had material non-public information.

---

## Lessons for Traders and Risk Managers

- **Narrative Is Not Cash Flow**: A real technological change does not guarantee returns to the first companies that build it.
- **Float Scarcity Creates False Signals**: Low-float IPOs can trade far above long-run value until supply arrives.
- **Discount Rate Sensitivity of Long-Duration Assets**: When value depends on cash flows far in the future, small changes in $r$ or $g$ move the price a great deal.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-013 | What was the total percentage decline in the NASDAQ Composite Index from its March 2000 peak to its October 2002 trough?
> 77.93%, from the record close of 5,048.62 on March 10, 2000 to the close of 1,114.11 on October 9, 2002.

> [!question]- mkt-his-014 | What role did 180-day IPO lockup expirations play in the dot-com crash?
> Lockups kept insider and venture shares off the market after IPOs; as they expired, the supply of tradable shares rose into a falling market for companies whose small floats had supported high prices.

> [!question]- mkt-his-015 | What was vendor financing in the late-1990s telecommunications equipment sector?
> Equipment makers lending to, or extending credit to, carriers so that the carriers could buy the makers' equipment, which booked sales whose collection depended on the customers' own fragile funding.

> [!question]- mkt-his-016 | How did the 2003 Global Research Analyst Settlement alter Wall Street operations?
> It required ten firms to pay about $1.4 billion and to separate research from investment banking, so that analysts' pay and coverage were insulated from banking business (SEC press release 2003-54).

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_hist_04_dot_com.py`](../code/mkt_hist_04_dot_com.py) prints and asserts every number on this page: the Nasdaq decline and the Netscape gain are recomputed from the cited prices in exact decimal arithmetic, the FOMC moves are summed from the individual decisions, and the Gordon multiples are checked against an explicit sum of the discounted growing cash flows.
- Related notes: [Case File 05: 2008 Global Financial Crisis](05-2008-Global-Financial-Crisis-and-Lehman-Collapse.md).
