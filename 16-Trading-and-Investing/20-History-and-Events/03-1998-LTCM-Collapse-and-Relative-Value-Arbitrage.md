---
type: guide
title: "Case File 03: 1998 LTCM Collapse and Relative Value Arbitrage"
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: solid
tags: [market-history, ltcm, relative-value, fixed-income-arbitrage, leverage, correlation-breakdown, var-failure, case-study]
---

# Case File 03: 1998 LTCM Collapse and Relative Value Arbitrage

## Executive Summary

Long-Term Capital Management (LTCM), founded in February 1994 by former Salomon Brothers Vice Chairman John Meriwether with a team that included two Nobel laureates, nearly failed in September 1998.
The fund ran convergence trades (relative value arbitrage) on a balance sheet of over $125 billion at August 31, 1998, against equity of $4.8 billion at the start of the year, a balance-sheet leverage ratio of more than 25-to-1, plus gross notional derivatives of over $1.4 trillion (President's Working Group, April 1999).
After Russia devalued the ruble and declared a debt moratorium on August 17, 1998, a flight to quality widened risk spreads and liquidity premiums in markets around the world at the same time, and LTCM lost 44 percent of its value in August alone.
On September 23, 1998, at the Federal Reserve Bank of New York, fourteen banks and brokerage firms agreed to invest $3.625 billion in exchange for 90 percent of the fund; no public money was used, and the last of the consortium's investment was returned by the end of 1999.

---

## Primary Sources and Chronology

Sources used on this page: President's Working Group on Financial Markets, *Hedge Funds, Leverage, and the Lessons of Long-Term Capital Management* (April 1999), pages 10 to 14 and Appendix C; Michael Fleming and Weiling Liu, "Near Failure of Long-Term Capital Management", Federal Reserve History (2013), which draws on William McDonough's testimony of October 1, 1998 and on the US General Accounting Office (2000); Basel Committee on Banking Supervision, *Banks' Interactions with Highly Leveraged Institutions* (January 1999).

- **February 1994**: LTCM is founded; its fund, Long-Term Capital Portfolio, L.P., is a Cayman Islands partnership (PWG).
- **1994 to 1997**: LTCM generates returns of 20 percent in 1994, 43 percent in 1995, 41 percent in 1996 and 17 percent in 1997 (Federal Reserve History, citing the *Wall Street Journal*); the PWG gives net-of-fee returns of approximately 40 percent in 1995 and 1996 and slightly less than 20 percent in 1997.
- **End of 1997**: LTCM returns approximately $2.7 billion of capital to investors, cutting the capital base by about 36 percent to $4.8 billion without reducing its positions (PWG).
- **July 31, 1998**: The fund holds $4.1 billion of capital, down about fifteen percent from the start of the year (PWG).
- **August 17, 1998**: Russia devalues the ruble and declares a debt moratorium (PWG).
- **August 21, 1998**: LTCM suffers huge losses and begins seeking additional capital (Federal Reserve History).
- **End of August 1998**: August losses of $1.8 billion leave capital at $2.3 billion, a loss of over fifty percent for the year (PWG).
- **September 2, 1998**: LTCM discloses its August losses in a letter to investors (Federal Reserve History).
- **September 21, 1998**: Bear Stearns, LTCM's prime broker, has required collateral for potential settlement exposures, and counterparties are seeking as much collateral as possible; a default could come as soon as September 23 (PWG).
- **September 23, 1998**:
  - An investor group led by Warren Buffett offers to buy out the partners for $250 million and then inject $3.75 billion, but the offer is not accepted by the 12:30 p.m. deadline (Federal Reserve History).
  - At about 6:00 p.m., fourteen firms agree to invest $3.625 billion for 90 percent of the fund; two firms in the talks decline to participate (Federal Reserve History; PWG).
- **End of 1999**: The fund returns the last of the consortium's investment (Federal Reserve History, citing GAO 2000).

---

## Market Backdrop and Structural Vulnerabilities

### 1. Relative-Value Fixed Income Arbitrage
The PWG defines convergence trading as taking offsetting positions in two related securities in the hope that the price gap between them will move in a favourable direction.
About 80 percent of the fund's balance-sheet positions were in G-7 government bonds, and it also traded mortgage-backed, corporate and emerging-market bonds, equities, futures on about a dozen exchanges, and swaps and options with several dozen counterparties (PWG).
Typical convergence trades of this kind include:
- **On-the-run vs off-the-run Treasuries**: A newly issued (on-the-run) bond usually yields slightly less than an older bond of similar maturity because it is more liquid; the trade is long the off-the-run bond and short the on-the-run bond.
- **Swap spreads**: Positions that profit if the spread between swap rates and government bond yields moves back to its usual range.
- **Equity relative value**: Pairs such as Royal Dutch and Shell Transport, whose cash flows were split 60:40 between the two listed companies yet whose prices deviated from that ratio for long periods (Kenneth Froot and Emil Dabora, "How Are Stock Prices Affected by the Location of Trade?", *Journal of Financial Economics* 53(2), 1999).
Each trade earns a small spread, so a meaningful return on equity requires large positions relative to capital.

### 2. Leverage and Position Size
At the end of August 1998 the gross notional amounts of the fund's contracts exceeded $500 billion on futures exchanges, $750 billion in swaps and $150 billion in options and other OTC derivatives (PWG).
A number of its futures positions were more than five percent of open interest, and in a few cases well above ten percent (PWG).
Positions that large cannot be cut quickly without moving prices against the seller.

### 3. Risk Models Estimated in Calm Periods
The PWG found that losses in individual markets greatly exceeded what conventional risk models, estimated during more stable periods, suggested were probable.
The simultaneous shocks to many markets confounded expectations of relatively low correlations, and the flight to quality reduced liquidity, contrary to the assumptions implicit in the models.

---

## Microstructure Breakdown and Liquidity Evaporation

```
+-----------------------------------------------------------------------+
|                    LTCM COLLATERAL MARGIN SPIRAL                      |
+-----------------------------------------------------------------------+
| 1. Russian Default (Aug 17, 1998)                                     |
|    Flight to quality; risk spreads and liquidity premiums widen       |
|                                                                       |
| 2. Mark-to-Market Losses and Collateral Calls                         |
|    Counterparties mark positions daily and call for collateral        |
|                                                                       |
| 3. Positions Too Large to Cut                                         |
|    Selling into thin markets would move prices further                |
|                                                                       |
| 4. Capital Falls ($4.8B at Jan 1 -> $2.3B at Aug 31)                  |
|    Leverage on remaining capital rises sharply                        |
|                                                                       |
| 5. Prime Broker and Counterparties Tighten Terms                      |
|    Collateral demands drain liquidity                                 |
|                                                                       |
| 6. Systemic Threat                                                    |
|    Default would force counterparties to close out at once            |
|    -> NY Fed hosts the private consortium recapitalisation            |
+-----------------------------------------------------------------------+
```

As its condition worsened, previously flexible credit arrangements became more rigid and daily mark-to-market valuations for collateral calls became more contentious, with some counterparties applying possible liquidation values (PWG).

---

## Quantitative Autopsy

This is a hypothetical illustration of a convergence trade, not LTCM's actual book.
Let the yield spread between a 30-year off-the-run Treasury ($Y_{\text{off}}$) and the on-the-run Treasury ($Y_{\text{on}}$) be:
$$S(t) = Y_{\text{off}}(t) - Y_{\text{on}}(t)$$
Assume a calm-period model with daily spread volatility $\sigma = 0.8 \text{ bps}$ and a position of notional $N = \$20 \text{ billion}$ long off-the-run and short on-the-run:
$$\Delta \text{PnL} = -N \times D \times \Delta S$$
where $D = 14.61$ is the modified duration of a 30-year par bond yielding 5.5% with semiannual coupons.
A 3-standard-deviation daily move is $3 \times 0.8 = 2.4 \text{ bps}$, giving a loss of:
$$\Delta \text{PnL} = -\$20{,}000{,}000{,}000 \times 14.61 \times 0.00024 = -\$70.1 \text{ million}$$
If the spread instead widens by 18 bps, that move is 22.5 standard deviations under the calm-period model, and the loss is:
$$\Delta \text{PnL} = -\$20{,}000{,}000{,}000 \times 14.61 \times 0.0018 = -\$526.0 \text{ million}$$
The point is the ratio: a model calibrated in calm periods assigns essentially zero probability to a move it later has to absorb, and when many such trades widen together the losses add up instead of offsetting.

The fund's own figures are consistent with each other: $125/4.8 = 26.04$ times leverage, a fall from $4.8 billion to $4.1 billion is 14.58% (the PWG's "about fifteen percent"), an August loss of $1.8 billion on $4.1 billion is 43.90% (Federal Reserve History's "44 percent"), and $2.3 billion at the end of August is 52.08% below $4.8 billion (the PWG's "over fifty percent").

---

## Regulatory and Structural Legacy

1. **Counterparty risk management**: The PWG recommended that banks and dealers improve their credit risk management with highly leveraged counterparties, including stress testing of credit and market risk and more meaningful disclosure.
2. **Basel Committee guidance**: In January 1999 the Basel Committee published *Banks' Interactions with Highly Leveraged Institutions* and accompanying sound practices for banks' dealings with highly leveraged institutions.
3. **Collateral haircuts**: The PWG notes that competition had led banks to reduce or eliminate haircuts, sometimes providing 100% financing, and that examiners evaluate the risks of smaller haircuts.
4. **Private-sector resolution**: The New York Fed provided facilities and encouraged the firms to seek the least disruptive solution, but the recapitalisation was funded by the counterparties themselves (PWG).

---

## Lessons for Traders and Risk Managers

- **Liquidity Trumps Theoretical Fair Value**: A trade that will converge in two years is worthless if margin calls force you out next week.
- **Correlations Rise in a Crisis**: Diversification across markets fails when many participants must sell whatever is liquid at the same time.
- **Size Is a Risk Factor**: Positions that are a large share of open interest cannot be cut quickly without moving the price.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-009 | What was the core investment strategy of Long-Term Capital Management?
> Convergence trading (relative value arbitrage): offsetting positions in related securities expected to move back together, run at high leverage because each spread was small.

> [!question]- mkt-his-010 | What external geopolitical catalyst triggered the LTCM liquidity death spiral in August 1998?
> Russia's devaluation of the ruble and declaration of a debt moratorium on August 17, 1998, which set off a global flight to quality.

> [!question]- mkt-his-011 | Why did LTCM's Value at Risk (VaR) models catastrophically underestimate its true portfolio risk?
> The models were estimated during stable periods; in the crisis, losses greatly exceeded what they suggested, shocks hit many markets at once despite assumed low correlations, and liquidity dried up (PWG, 1999).

> [!question]- mkt-his-012 | Why did the Federal Reserve Bank of New York intervene to coordinate a private bank consortium bailout of LTCM?
> A default on a balance sheet of over $125 billion with large derivatives positions would have forced counterparties to close out at once in fragile markets; the NY Fed hosted the talks, and fourteen firms invested $3.625 billion for 90 percent of the fund.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_hist_03_ltcm.py`](../code/mkt_hist_03_ltcm.py) prints and asserts every number on this page: the modified duration comes from the closed-form par-bond annuity formula and is checked against a central finite difference of the explicit 60-coupon price sum, the losses and the sigma multiple are computed from the stated inputs, and the PWG and Federal Reserve History capital figures are cross-checked against each other.
- Related notes: [Case File 05: 2008 Global Financial Crisis](05-2008-Global-Financial-Crisis-and-Lehman-Collapse.md), [Case File 10: 2022 UK LDI Crisis](10-2022-UK-LDI-Pension-Crisis-and-Gilt-Spiral.md).
