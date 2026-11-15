---
type: guide
title: "Case File 09: 2021 GameStop Meme Squeeze and DTCC Margin Halt"
track: [quant-trader, quant-risk, quant-dev]
tier: advanced
status: solid
tags: [market-history, gamestop-2021, meme-stocks, short-squeeze, gamma-squeeze, dtcc-margin, clearing-risk, case-study]
---

# Case File 09: 2021 GameStop Meme Squeeze and DTCC Margin Halt

## Executive Summary

In January 2021 the share price of GameStop Corp. (NYSE: GME) rose from a close of $19.95 on January 12 to a record close of $347.51 on January 27 and an intraday high of $483.00 on January 28, amid heavy individual-investor buying and intense social media attention (SEC staff report, October 14, 2021).
GME short interest reached 122.97% of float in January 2021, possible because the same shares can be lent and sold short more than once.
The SEC staff found that short covering contributed to price rises in some periods but was a small fraction of overall buying, that "it was the positive sentiment, not the buying-to-cover, that sustained the weeks-long price appreciation", and that it did not find evidence of a gamma squeeze.
On January 27 the National Securities Clearing Corporation (NSCC) made intraday margin calls of $6.9 billion on 36 clearing members, and on January 28 several retail brokers, including Robinhood and Interactive Brokers, restricted customers to closing positions in GME and other stocks.
The episode fed into the SEC's adoption of T+1 settlement, which took effect on May 28, 2024.

---

## Primary Sources and Chronology

Sources used on this page: SEC staff, *Staff Report on Equity and Options Market Structure Conditions in Early 2021* (October 14, 2021), sections 3.1 to 3.6 and 4; House Committee on Financial Services hearing of February 18, 2021 (testimony cited in the SEC report); SEC Release 34-96930 (February 15, 2023) adopting T+1; SEC Release 34-98738 (October 13, 2023) adopting Rule 13f-2 and Form SHO.

- **April 2020**: A GME short interest ratio of 84% is reportedly noted on Reddit (SEC report).
- **December 31, 2020**: GME short interest reaches 109.26% (SEC report).
- **January 11, 2021**: GameStop announces that Ryan Cohen, of Chewy, will join its board; GME reaches an intraday high of $20.65, about 17% above the prior close.
- **January 13, 2021**: GME closes at $31.40, up from $19.95 the day before, on about 144 million shares against about 7 million the day before.
- **January 22, 2021**: GME rises from $43 to $72 in about three hours; 197.2 million shares trade, the highest volume of the month.
- **January 27, 2021**: GME closes at $347.51, more than 1,600% above its January 11 close (SEC report) of $19.94 (contemporary press reports); NSCC makes intraday margin calls of $6.9 billion on 36 members, bringing total required margin to $25.5 billion, and both NSCC and OCC clear record volumes.
- **January 28, 2021**: GME reaches an intraday high of $483.00; NSCC waives the excess capital premium charge for all members; one broker-dealer described in the SEC report puts new customer purchases in eight securities (AMC, BlackBerry, Bed Bath & Beyond, Express, GME, Koss, Naked Brand and Nokia) on position-closing-only status, and Robinhood and Interactive Brokers state that in some cases customers can only sell certain securities.
- **February 2, 2021**: NSCC removes the excess capital premium waiver.
- **February 5, 2021**: That broker-dealer removes its remaining limits (SEC report).
- **February 18, 2021**: The House Committee on Financial Services holds its hearing "Game Stopped? Who Wins and Loses When Short Sellers, Social Media, and Retail Investors Collide", with testimony from Robinhood CEO Vladimir Tenev, Citadel founder Kenneth Griffin, Melvin Capital founder Gabriel Plotkin and others.
- **October 14, 2021**: The SEC staff publishes its report.

---

## Market Backdrop and Structural Vulnerabilities

### 1. Short Interest Above 100% of Float
GME short interest as a percent of float reached 122.97% in January 2021, far above other meme stocks such as Bed Bath & Beyond (66.02%) and AMC (11.4%) (SEC report).
Short interest can exceed 100% when the same shares are lent multiple times by successive purchasers (SEC report, footnote 75):
- Lender A lends 1 share to short seller X, who sells it to buyer B.
- Buyer B lends the same share to short seller Y, who sells it to buyer C.
- One share has now been sold short twice, so on a 100-share float the short interest is 2%, although 99 of the 100 shares have never been sold short.
If every share in the float is lent and sold short, and every buyer lends again once, the short interest is 200%, and the short sellers together owe 200 shares against a float of 100.

### 2. The Gamma Squeeze Hypothesis
A gamma squeeze occurs when market makers buy a stock to hedge the risk of calls they have written, putting further upward pressure on the price (SEC report).
For GME in January 2021 the SEC staff did not find evidence of one: individual customers' GME options volume rose from $58.5 million on January 21 to $563.4 million on January 22 and peaked at $2.4 billion on January 27, but the increase was mostly in put buying rather than call buying, and the data show that market makers were buying, rather than writing, calls.
The mechanism is still worth understanding, because it can matter for other stocks (see the Quantitative Autopsy).

### 3. Payment for Order Flow and Retail Brokers
Many retail brokers route customer orders to wholesale market makers that pay for the order flow, and the SEC staff report recommends considering whether digital engagement practices and payment for order flow lead investors to trade more than they otherwise would.

---

## Microstructure Breakdown and Liquidity Evaporation

The stress appeared in clearing and settlement:
1. **The settlement lag**: In January 2021 US equities settled two business days after the trade (T+2), and NSCC, as the central counterparty, bears the risk of a member failing before settlement.
2. **Clearing margin**: NSCC collects margin from members to cover that risk, and in highly volatile trading it may require more (SEC report).
   On January 27, 2021, its intraday calls of $6.9 billion comprised $2.1 billion of mark-to-market calls and $4.8 billion of a special charge imposed on 18 members, all of whom paid.
3. **The excess capital premium**: Several members were also subject to an excess capital premium (ECP) charge based on the ratio of their excess risk to their capital, and NSCC waived it for all members on January 28.
   Absent the waiver, one retail broker-dealer would have faced an ECP charge of more than double its margin requirement of $1.4 billion on January 28 (SEC report).
4. **Broker restrictions**: NSCC's rules do not let it stop members trading particular symbols; the restrictions were decisions by the broker-dealers, which said they were a reaction to NSCC margin calls and capital charges (SEC report).
   Witnesses at the February 18, 2021 hearing testified that the restrictions did not result from pressure by hedge funds.

---

## Quantitative Autopsy

The dealer-hedging mechanism behind a gamma squeeze, with hypothetical numbers.
A dealer short $N_{\text{contracts}}$ calls (100 shares each) has delta:
$$\Delta_{\text{dealer}} = -N_{\text{contracts}} \times 100 \times N(d_1)$$
and to hedge must hold $Q_{\text{hedge}}$ shares:
$$Q_{\text{hedge}} = N_{\text{contracts}} \times 100 \times N(d_1)$$
The extra shares needed per dollar rise in the stock are set by gamma:
$$\frac{\partial Q_{\text{hedge}}}{\partial S} = N_{\text{contracts}} \times 100 \times \Gamma = N_{\text{contracts}} \times 100 \times \frac{N'(d_1)}{S \sigma \sqrt{\tau}}$$
Take a dealer short 10,000 at-the-money calls with $S = K = 40$ and volatility $\sigma = 200\%$.
With 5 trading days to expiry ($\tau = 5/252$) the dealer must buy about 35,053 shares per $1 rise; with 1 trading day left it must buy about 79,006 shares, 2.25 times as many.
Near the money, gamma grows roughly like $1/\sqrt{\tau}$ as expiry approaches (the ratio here is close to $\sqrt{5} = 2.236$), so short-dated calls concentrated near the price can force large hedge purchases.
If market makers are instead long calls, as the SEC staff found for GME, their hedging works the other way and dampens moves.

The headline changes follow from the SEC report's prices: from $19.95 to the $347.51 close is a rise of 1,641.90%, and to the $483.00 intraday high is 2,321.05%.
From the January 11 close of $19.94 the rise to $347.51 is 1,642.78%, the SEC report's "more than 1,600%".

---

## Regulatory and Structural Legacy

1. **T+1 settlement**: SEC Release 34-96930 (February 15, 2023) amended Rule 15c6-1 to shorten the standard settlement cycle for most broker-dealer transactions from T+2 to T+1, with a compliance date of May 28, 2024; the SEC staff report had noted that shortening the settlement cycle is one way to reduce the risk that thinly capitalised broker-dealers pose to the clearing house.
2. **Short position reporting (Rule 13f-2)**: Adopted on October 13, 2023, it requires institutional investment managers above set thresholds to report short positions monthly on Form SHO, with aggregated data published by the SEC; as of November 2026 the compliance date has been extended by SEC exemptive relief, so check the SEC's Form SHO page for the current date.
3. **Payment for order flow and engagement**: The SEC staff report recommended further consideration of digital engagement practices and payment for order flow.

---

## Lessons for Traders and Risk Managers

- **Treat Very High Short Interest as a Risk Factor**: When short interest exceeds the float, covering can move the price regardless of fundamentals; size short positions in such names with that tail in mind.
- **Understand Counterparty and Clearing Risk**: A broker's clearing margin and capital can limit what its customers may trade, whatever their own account balances.
- **Test the Story Against the Data**: The popular gamma-squeeze narrative did not match the options data; check who was actually buying and writing.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-033 | What was the reported short interest of GameStop Corp. as a percentage of float prior to the January 2021 squeeze?
> GME short interest reached 122.97% of float in January 2021 and was 109.26% on December 31, 2020 (SEC staff report).

> [!question]- mkt-his-034 | What is a gamma squeeze in options market microstructure?
> Market makers who have written calls buy the underlying stock to hedge as its price rises, adding upward pressure; for GME in January 2021 the SEC staff found no evidence of one, since market makers were buying rather than writing calls.

> [!question]- mkt-his-035 | Why did retail brokerages like Robinhood restrict customer purchasing of GameStop on January 28, 2021?
> They said the restrictions were a reaction to NSCC margin calls and capital charges driven by extreme volatility; NSCC had made $6.9 billion of intraday margin calls on January 27, and one retail broker-dealer would have faced an excess capital premium charge of more than double its $1.4 billion margin requirement without NSCC's waiver.

> [!question]- mkt-his-036 | What major settlement reform did the SEC implement in May 2024 as a direct response to the GameStop clearinghouse crisis?
> T+1 settlement: the SEC adopted it on February 15, 2023 (Release 34-96930) and it took effect on May 28, 2024, shortening the window in which the clearing house bears member default risk.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_hist_09_gamestop.py`](../code/mkt_hist_09_gamestop.py) prints and asserts every number on this page: the price changes are recomputed from the SEC report's prices and checked against its "more than 1,600%" statement, the NSCC call is checked against its two components, the re-lending examples run on a share ledger of loan records that counts the short interest and the shares never sold short, and the hedge figures use the closed-form gamma checked against a finite difference of the delta.
- Related notes: [Case File 06: 2010 Flash Crash](06-2010-Flash-Crash-and-LOB-Evaporation.md), [Case File 02: 1987 Black Monday](02-1987-Black-Monday-and-Portfolio-Insurance.md).
