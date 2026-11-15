---
type: guide
title: "Case File 10: 2022 UK LDI Pension Crisis and Gilt Spiral"
track: [quant-trader, quant-risk, quant-research]
tier: advanced
status: solid
tags: [market-history, ldi-crisis-2022, uk-gilts, pension-funds, interest-rate-swaps, leverage, bank-of-england, case-study]
---

# Case File 10: 2022 UK LDI Pension Crisis and Gilt Spiral

## Executive Summary

After the UK Government's Growth Plan of Friday, September 23, 2022, a package of unfunded tax cuts announced without an Office for Budget Responsibility forecast, long-dated gilt yields rose at a speed and scale the Bank of England called unprecedented: the 30-year gilt yield rose by 160 basis points in just a few days, with two daily increases of more than 35 basis points against a previous record daily rise of 29 basis points since 2000.
Defined benefit (DB) pension funds hedge their liabilities through liability-driven investment (LDI), with over £1 trillion invested in LDI strategies in the UK, much of it using repo and derivatives leverage to hold more long gilts than the cash invested.
As yields rose, the net asset value of leveraged LDI funds fell and margin and collateral calls rose, and pooled LDI funds could not raise cash from their many small pension fund investors fast enough, leaving them facing forced sales of long gilts into an illiquid market.
On Wednesday, September 28, the Bank of England announced temporary purchases of long-dated gilts to restore market functioning, indemnified by HM Treasury; the 30-year yield fell by more than 100 basis points that day, and the Bank bought £19.3 billion of gilts in total before the operation ended on October 14.

---

## Primary Sources and Chronology

Sources used on this page: Letter from Sir Jon Cunliffe, Deputy Governor for Financial Stability, to Mel Stride MP, Chair of the Treasury Committee (October 5, 2022); Bank of England market notice and announcement of September 28, 2022; Bank of England statement on the end of the gilt market operation (October 17, 2022); Bank of England *Quarterly Bulletin* 2023, "Financial stability buy/sell tools: a gilt market case study"; Bank of England *Financial Stability Report*, December 2022; Financial Policy Committee, *Financial Policy Summary and Record*, March 2023.

- **Thursday, September 22, 2022**: The Monetary Policy Committee announces its September decision; long-term gilt yields rise by around 20 basis points (Cunliffe letter).
- **Friday, September 23, 2022**: The Chancellor announces the Growth Plan; sterling falls by around 4% against the US dollar and long-term gilt yields rise by 30 basis points, and LDI fund managers raise their first concerns with the Bank.
- **Monday, September 26, 2022**: The 30-year gilt yield rises by around 50 basis points, leaving it more than 80 basis points above its level at the start of September 23; LDI managers report that continued moves would force them to sell large quantities of long gilts, at least £50 billion in a short time on the market intelligence received, against average daily trading of £12 billion in these maturities.
- **Tuesday, September 27, 2022**: The 30-year yield falls 20 basis points in the morning and then rises 67 basis points by the evening, about 47 basis points above the previous evening; several LDI managers tell the Bank that multiple funds are likely to fall into negative net asset value and begin winding up the next morning.
- **Wednesday, September 28, 2022**: Late in the morning the Bank announces purchases of long-dated conventional gilts at "whatever scale is needed to restore market functioning", with auctions each weekday until October 14 and an initial limit of £5 billion per auction; the 30-year yield falls by more than 100 basis points that day, and its intraday range of 127 basis points exceeds the annual range in all but 4 of the previous 27 years.
- **October 11 to 14, 2022**: The Bank adds index-linked gilts to its purchases.
- **October 14, 2022**: The operation ends; in total the Bank bought £19.3 billion of gilts, £12.1 billion conventional and £7.2 billion index-linked (Quarterly Bulletin).
- **October 2022**: Chancellor Kwasi Kwarteng is dismissed on October 14, his successor Jeremy Hunt reverses almost all of the Growth Plan's tax measures on October 17, and Prime Minister Liz Truss announces her resignation on October 20 and leaves office on October 25, after 49 days.
- **March 29, 2023**: The Financial Policy Committee judges that LDI funds should be resilient to a yield shock of, at a minimum, around 250 basis points, and asks The Pensions Regulator to set minimum resilience levels.

---

## Market Backdrop and Structural Vulnerabilities

### 1. The Defined Benefit Liability
A DB scheme promises pensions far into the future, and the present value of those liabilities is computed by discounting the promised cash flows at long-term yields:
$$L = \sum_{t=1}^T \frac{CF_t}{(1 + y_t)^t}$$
Because the cash flows are long-dated, the liability is very sensitive to long-term yields: a liability with duration $D_L$ changes by about $-D_L \times \Delta y$ of its value for a yield change $\Delta y$.
More than 20% of UK DB schemes were in deficit in August 2022, and more than 40% a year earlier (Cunliffe letter).

### 2. The Liability-Driven Investment (LDI) Solution
LDI aims to make the value of a scheme's assets move in line with its liabilities, and the closest match is long-term gilts, particularly index-linked gilts (Cunliffe letter).
LDI strategies use leverage, through repo borrowing and derivatives, so that a scheme can hold more long-gilt exposure than its cash allocation while also holding growth assets such as equities.
Large schemes run LDI themselves or in segregated accounts; smaller schemes invest together in pooled LDI funds run by asset managers, each with many pension fund investors.
Each LDI fund keeps a cushion between its assets and its borrowing to absorb losses on gilts, and when losses eat into it, investors are asked to add capital (rebalancing), which is harder for pooled funds with many small investors.

### 3. Solvent but Illiquid
In the Bank's stylised example, a fund holds gilts at 2 times leverage (half of the gilts funded by repo), so its cushion is half the gilt holdings, and a fall of around 30% in gilt prices severely erodes it.
The pension scheme as a whole might be better off when yields rise, because its liabilities fall by more than its other assets, but the LDI fund still has to meet margin calls in cash now (Cunliffe letter).
Previous stress tests had generally assumed a maximum move of about 100 basis points in a short period, including the FPC's own 2018 assessment of pension schemes' ability to meet variation margin calls (Cunliffe letter).

---

## Microstructure Breakdown and Liquidity Evaporation

```
+-----------------------------------------------------------------------+
|                    THE 2022 UK LDI MARGIN DEATH SPIRAL                |
+-----------------------------------------------------------------------+
| 1. Fiscal Shock                                                       |
|    Long gilt yields jump; LDI fund asset values fall                  |
|                                                                       |
| 2. Margin and Collateral Calls                                        |
|    Leverage rises as the cushion shrinks                              |
|                                                                       |
| 3. Rebalancing Too Slow                                               |
|    Pooled funds cannot collect capital from many small investors      |
|    within the time available                                          |
|                                                                       |
| 4. Forced Gilt Sales                                                  |
|    Funds must sell long gilts into an illiquid market                 |
|                                                                       |
| 5. Prices Fall Further                                                |
|    Sales push yields higher, eroding other funds' cushions            |
|                                                                       |
| 6. Self-Reinforcing Spiral                                            |
|    Defaults would put repo collateral up for sale -> BoE backstop     |
+-----------------------------------------------------------------------+
```

Had the Bank not intervened, the Cunliffe letter says, a large number of pooled LDI funds would have been left with negative net asset value, the gilts their bank lenders held as collateral might have been sold on the market, and the resulting price falls would have forced other institutions to sell assets too.

---

## Quantitative Autopsy

This is a hypothetical position.
A scheme deposits £200 million in an LDI fund that uses 5x leverage to hold interest-rate exposure equivalent to a notional of $N = £1.0 \text{ billion}$ with duration $D = 22$ years.
To first order the position changes in value by:
$$\Delta \text{Value} \approx -N \times D \times \Delta y$$
For a rise of $\Delta y = +1.50\%$ (150 basis points):
$$\Delta \text{Value} \approx -£1{,}000{,}000{,}000 \times 22 \times 0.0150 = -£330{,}000{,}000$$
The £330 million loss exceeds the £200 million of collateral, leaving:
$$\text{Collateral Balance} = £200{,}000{,}000 - £330{,}000{,}000 = -£130{,}000{,}000$$
Convexity reduces the loss for a move this large: repricing a zero-coupon position of the same duration exactly gives a loss of £281.1 million, which still leaves the collateral at -£81.1 million.
If the scheme has only £30 million of liquid assets to send, it is £100 million short on the first-order figure, and the LDI fund must sell gilts or close hedges, which pushes yields up for every other fund.
In the Bank's stylised 2x fund, a 30% fall in gilt prices removes 60% of the cushion, because the borrowing does not shrink when the gilts fall.

---

## Regulatory and Structural Legacy

1. **Minimum LDI resilience**: In March 2023 the Financial Policy Committee judged that LDI funds should be able to withstand a yield shock of, at a minimum, around 250 basis points, in addition to the resilience needed for other risks and day-to-day moves, and asked The Pensions Regulator to set minimum levels of resilience for LDI funds and mandates.
2. **Financial stability tools**: The episode was the first time the Bank intervened in the gilt market in pursuit of its statutory financial stability objective (Cunliffe letter), and the Bank has since described the operation as a case study for financial stability buy and sell tools (Quarterly Bulletin 2023).
3. **Non-bank leverage**: The Bank's December 2022 *Financial Stability Report* reviewed the LDI episode and the vulnerabilities from leverage in non-bank finance.

---

## Lessons for Traders and Risk Managers

- **Solvency Is Not Liquidity**: A scheme can be better off economically while its leveraged hedge faces cash calls it cannot meet in time.
- **Concentrated Positioning Breaks Prices**: When many funds hold the same leveraged position, forced sales by some raise the losses of the rest.
- **Stress Beyond History**: Stress tests built on a 100-basis-point maximum failed against a 160-basis-point move in a few days.

---

## Case Study Drills and Review Questions

> [!question]- mkt-his-037 | What policy announcement triggered the catastrophic UK Gilt market sell-off in September 2022?
> The Government's Growth Plan of September 23, 2022, a package of unfunded tax cuts announced without an OBR forecast, after which long gilt yields rose by an unprecedented amount (Cunliffe letter).

> [!question]- mkt-his-038 | What was the primary purpose of Liability-Driven Investment (LDI) strategies for UK defined benefit pension schemes?
> To make the value of the scheme's assets move in line with its liabilities, mainly through leveraged exposure to long-term gilts using repo and derivatives, while keeping capital for growth assets.

> [!question]- mkt-his-039 | Why did rising Gilt yields trigger a liquidity crisis for pension schemes whose long-term solvency had actually improved?
> Rising yields cut the value of the leveraged gilt and derivative positions in LDI funds immediately and produced margin and collateral calls in cash, while the fall in liabilities was a paper gain that could not be used to pay them.

> [!question]- mkt-his-040 | What emergency action did the Bank of England take on September 28, 2022, to halt the LDI death spiral?
> It announced temporary purchases of long-dated gilts at whatever scale was needed to restore market functioning, with daily auctions until October 14 and an initial limit of £5 billion per auction; it bought £19.3 billion in total.

---

## In this repo and The-Distinguished-Engineer

- Code: [`code/mkt_hist_10_ldi_gilts.py`](../code/mkt_hist_10_ldi_gilts.py) prints and asserts every number on this page: the first-order loss uses a sensitivity checked by finite difference against an exactly repriced zero-coupon position (whose exact loss is also asserted), the Bank's stylised fund is evaluated on an explicit balance sheet, the purchase total is checked against its two components, the auction days are counted from the calendar, and the days in office are counted from the dates.
- Related notes: [Case File 03: LTCM](03-1998-LTCM-Collapse-and-Relative-Value-Arbitrage.md), [Case File 05: 2008 Global Financial Crisis](05-2008-Global-Financial-Crisis-and-Lehman-Collapse.md).
