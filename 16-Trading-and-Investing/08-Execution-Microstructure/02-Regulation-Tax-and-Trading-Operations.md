---
type: concept
track: [quant-trader, quant-risk]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [FINRA Regulatory Notice 26-10 - Intraday Margin Standards, FINRA Rule 4210 - Margin Requirements, Internal Revenue Code - Sections 1091 1256 475 and 461(l), Revenue Ruling 2008-5, SEC Regulation SHO (17 CFR 242.200-204), Income-tax Act 1961 and Income-tax Act 2025, Finance Bill 2026 - STT rates, ICAI Guidance Note on Tax Audit 2026]
---

# Regulation, Tax, and Trading Operations

## TL;DR

- Regulatory frameworks and tax structures govern the real-world operational feasibility, margin leverage limits, and net post-friction profitability of market participants.
- FINRA's Pattern Day Trader (PDT) rule, with its $25,000 minimum for margin accounts making four or more day trades in five business days, was replaced by intraday margin standards effective June 4, 2026 (Regulatory Notice 26-10), with brokers allowed to phase in until October 20, 2027.
- The IRS Wash-Sale Rule (IRC Section 1091) disallows the deduction of a capital loss if a substantially identical security is acquired within 30 days before or after the sale date, adding the disallowed loss to the cost basis of the new position.
- IRC Section 1256 gives regulated futures and nonequity (for example broad-based index) options 60/40 treatment, taxing 60% of gains as long-term and 40% as short-term regardless of holding period, and marks open contracts to market at year-end.
- SEC Regulation SHO requires a locate before a short sale (Rule 203(b)(1)) and sets close-out deadlines for fails to deliver (Rule 204), aimed at abusive naked short selling and persistent fails.

## Learning objectives

- Explain the former FINRA Pattern Day Trader (PDT) rule and the intraday margin standards that replaced it in 2026.
- Deconstruct the 61-day window of the IRS Wash-Sale Rule and calculate adjusted cost basis across complex trading sequences.
- Compare the tax implications of trading equity shares versus Section 1256 futures and broad-based index options.
- Evaluate the requirements and benefits of the IRS Section 475(f) Mark-to-Market election for active traders.
- Navigate SEC Regulation SHO locate rules (Rule 203) and close-out deadlines for fails to deliver (Rule 204).
- Analyze Indian securities taxation, including Securities Transaction Tax (STT), turnover for the tax audit, and business income treatment of F&O.

## Core concepts

### 1. US Day-Trading Margin: From the PDT Rule to Intraday Margin (FINRA Rule 4210)

The US day-trading rules changed in 2026, so a trader must know both the old rule (still applied by some brokers during the transition) and the new one.

**The pattern day trader (PDT) rule, in force from 2001 until June 4, 2026.**
Under the former FINRA Rule 4210(f)(8)(B), approved by the SEC in 2001 (Release 34-44009), a margin customer was a **pattern day trader** if:
- They executed four or more **day trades** (opening and closing the same position within one day) within any five business days.
- Those day trades were more than 6% of the customer's total trades in that window.

```
+-----------------------------------------------------------------------+
|           FORMER FINRA PATTERN DAY TRADER RULE (UNTIL JUNE 4, 2026)   |
+-----------------------------------------------------------------------+
| Equity >= $25,000                 | Equity < $25,000                  |
|-----------------------------------+-----------------------------------|
| Day-trading buying power =        | No day trading until equity is    |
| 4 x maintenance margin excess     | restored to $25,000               |
| (prior day's close)               |                                   |
| Day-trading margin call: 5        | Unmet call: account restricted to |
| business days to meet             | a cash-available basis for 90     |
|                                   | days or until the call is met     |
+-----------------------------------------------------------------------+
```

Day Trading Buying Power (DTBP) was set from the prior day's close:
$$\text{DTBP} = 4 \times (\text{Account Equity} - \text{Maintenance Margin Requirement})$$
Exceeding it produced a day-trading margin call with five business days to meet it; an unmet call restricted the account to trading on a cash-available basis for 90 days or until the call was met.

**The intraday margin standards, effective June 4, 2026.**
The SEC approved FINRA's proposal SR-FINRA-2025-017 on April 14, 2026 (Release 34-105226), and FINRA Regulatory Notice 26-10 (April 20, 2026) sets the effective date at June 4, 2026, with members allowed to phase in implementation until October 20, 2027.
The amendments delete the pattern day trader designation and the $25,000 minimum equity requirement.
In their place, new Rule 4210(d)(2) requires a member to compute an **intraday margin deficit** for margin accounts (good-faith and portfolio margin accounts excluded) on days with a transaction that reduces intraday margin excess:
- The deficit is the largest margin deficiency following such a transaction, and the member must require it to be met as promptly as possible.
- A deficit stays outstanding until it is met or until the close of business on the 15th business day after it arose.
- A customer with a practice of not meeting deficits who fails to meet one by the fifth business day is restricted for 90 calendar days (or until it is met); deficits no larger than the lesser of 5% of account equity or $1,000 do not count.
As of November 2026, a broker that has not yet migrated may still apply the old day-trading requirements, so check your broker's disclosure.

### 2. The IRS Wash-Sale Rule (IRC Section 1091)

Under Section 1091 of the Internal Revenue Code, a taxpayer cannot deduct a loss on the sale of stock or securities if the taxpayer acquires a **substantially identical** security within a 61-day window:
- 30 calendar days before the sale date.
- The day of the sale.
- 30 calendar days after the sale date.

```
+-----------------------------------------------------------------------+
|                         THE 61-DAY WASH-SALE WINDOW                   |
+-----------------------------------------------------------------------+
| [-30 Days Prior] -------- [Day 0: Sale at Loss] -------- [+30 Days Post]|
| <--------------------------- 61 Days --------------------------------->|
| Any purchase of substantially identical security triggers DISALLOWANCE |
+-----------------------------------------------------------------------+
```

When a wash sale occurs:
1. The loss is disallowed when realised.
2. The disallowed loss is added to the cost basis of the replacement shares (IRC 1091(d)):
$$\text{New Cost Basis} = \text{Purchase Price of New Shares} + \text{Disallowed Loss}$$
3. The holding period of the original shares is added to the holding period of the new shares (IRC 1223(3)).
A trader who repeatedly sells at a loss and buys back within the window, and still holds the replacement shares at year-end, carries the disallowed losses into the basis of those shares instead of deducting them that year.

### 3. Section 1256 Contracts and the 60/40 Rule

IRC Section 1256 gives standardised exchange-traded derivatives a simple mark-to-market regime.
Under Section 1256(b), a **Section 1256 contract** is a regulated futures contract, a foreign currency contract, a nonequity option, a dealer equity option or a dealer securities futures contract.
- Regulated futures include CME E-mini S&P 500 and Nasdaq-100, crude oil, gold and Treasury futures.
- Nonequity options include cash-settled broad-based index options such as SPX, NDX, RUT and VIX options.

Section 1256 contracts receive two tax features:
1. **The 60/40 Capital Gains Split** (Section 1256(a)(3)): however briefly the contract was held, gains and losses are treated as:
   - 60% long-term capital gain or loss (top federal rate 20% in 2026).
   - 40% short-term capital gain or loss (taxed at ordinary rates, top rate 37% in 2026).
   - At the top brackets the blended federal rate is $0.6 \times 20\% + 0.4 \times 37\% = 26.8\%$ (or $30.6\%$ with the 3.8% net investment income tax), versus $37.0\%$ on short-term single-stock gains.
2. **Mark-to-Market at Year-End** (Section 1256(a)(1)): open contracts are treated as sold at fair market value on the last business day of the tax year, and Section 1256(f)(5) switches off the wash-sale rule for losses recognised by that year-end mark.

### 4. Section 475(f) Mark-to-Market Election for Professional Traders

A taxpayer whose activity qualifies as a trade or business of trading securities (**trader tax status**) can elect mark-to-market accounting under IRC Section 475(f).
Under Section 475(f):
- All securities held in the trading business are marked to market at year-end.
- Gains and losses are **ordinary income and ordinary losses** rather than capital gains, reported on Form 4797.
- The $3,000 annual net capital loss limitation of Section 1211(b) therefore does not apply to those losses.
- The wash-sale rule does not apply to securities that are marked to market.
- Large ordinary losses can still be limited by the excess business loss rule of Section 461(l) (a 2026 threshold of $256,000 single and $512,000 joint, per Rev. Proc. 2025-32), with the excess carried forward.
- For an existing taxpayer the election must be filed by the original due date (without extensions) of the return for the year before the election year, for example by the due date of the 2025 return for an election effective in 2026.

### 5. SEC Regulation SHO: Short Sale Governance

The SEC adopted Regulation SHO in 2004 (Release 34-50103) and added the close-out rule, Rule 204, as a temporary rule in 2008 and in final form in 2009 (Release 34-60388):
1. **Rule 203(b)(1) - The Locate Requirement**: A broker-dealer cannot accept or effect a short sale order unless it has:
   - Borrowed the security, or
   - Entered into a bona-fide arrangement to borrow the security, or
   - Reasonable grounds to believe that the security can be borrowed so that it can be delivered when due, and has documented that determination.
2. **Rule 204 - Close-Out Requirements for Fails to Deliver (FTD)**:
   - A participant of a registered clearing agency with a fail to deliver must close it out by borrowing or buying securities of like kind and quantity.
   - For a fail from a short sale the deadline is the beginning of regular trading hours on the settlement day after the settlement date; with T+1 settlement (since May 28, 2024) that is the morning of T+2.
   - For a fail from a long sale or from bona fide market making the deadline is the beginning of regular trading hours on the third consecutive settlement day after the settlement date, the morning of T+4 under T+1 settlement.
   - A **threshold security** (Rule 203(c)(6)) has aggregate fails of 10,000 shares or more for five consecutive settlement days, equal to at least 0.5% of total shares outstanding, and appears on an SRO threshold list; fails in it that persist for 13 consecutive settlement days must be closed out under Rule 203(b)(3).

### 6. Indian Markets: Taxation and Turnover Framework

The rules below are stated as of November 2026.
The Income-tax Act, 2025 replaced the Income-tax Act, 1961 from April 1, 2026 (tax year 2026-27 onward) and renumbers its sections; the 1961 section numbers are used here because most published guidance and past returns still cite them, so map them to the new Act before filing.
1. **Tax Treatment of F&O Derivatives**: Under section 43(5) of the 1961 Act, exchange-traded derivatives on a recognised stock exchange are excluded from "speculative transactions", so F&O profits are **non-speculative business income**, while intraday equity trades settled without delivery are **speculative business income**.
   - Non-speculative business losses can be set off against other business income (not salary) and carried forward for up to 8 assessment years; speculative losses can be set off only against speculative gains and carried forward for up to 4 years.
2. **Securities Transaction Tax (STT)**, levied on the value of the transaction under the Finance (No. 2) Act, 2004, at these rates from April 1, 2026 (Finance Bill 2026, clause 143):
   - Equity delivery: 0.1% on both buy and sell.
   - Equity intraday: 0.025% on the sell side.
   - Futures: 0.05% on the sell side (0.02% from October 1, 2024 to March 31, 2026, and 0.0125% before that).
   - Options: 0.15% of the premium on the sell side (previously 0.1%), and 0.15% of the intrinsic value for options exercised (previously 0.125%).
3. **Turnover for the Tax Audit (section 44AB of the 1961 Act)**:
   - ICAI's Guidance Note on Tax Audit (revised 2025 and 2026 editions, paragraph 5.11(b)) computes derivatives turnover as the total of favourable and unfavourable differences on each trade, i.e. the sum of absolute trade-level P&L.
   - For options, premium received on sale is also included, unless it is already part of the reported net profit (no double counting).
   - A tax audit is required when business turnover exceeds Rs 1 crore, or Rs 10 crore when cash receipts and cash payments are each no more than 5% of the totals.

---

## Worked examples

### Example 1: Wash-Sale Cost Basis Adjustment
A trader engages in the following sequential transactions in stock ABC:
- **March 1**: Buys 100 shares of ABC at $50.00 ($5,000 investment).
- **April 10**: Sells 100 shares of ABC at $42.00, realizing an $800 capital loss.
- **April 25 (15 days later, inside 30-day window)**: Re-enters the stock by purchasing 100 shares of ABC at $45.00 ($4,500 investment).
Because replacement shares were acquired within 30 days of the loss sale, the $800 loss is a **Wash Sale** and cannot be deducted on the trader's tax return for April.
The disallowed loss of $800 is added to the cost basis of the April 25 purchase:
$$\text{Adjusted Cost Basis} = \$4,500 + \$800 = \$5,300 \quad (\$53.00 \text{ per share})$$
If the trader subsequently sells the 100 shares on June 1 at $55.00 ($5,500 proceeds), the taxable gain is:
$$\text{Taxable Gain} = \$5,500 - \$5,300 = +\$200$$
The trader eventually realizes the tax benefit of the original $800 loss by reducing the taxable gain on the final sale from $1,000 ($5,500 - $4,500) down to $200.
Over both lots the trader recognises $0 + $200 = $200, exactly the economic result of losing $800 on the first lot and gaining $1,000 on the second, so the rule defers the loss rather than destroying it.

### Example 2: F&O Turnover for the Indian Tax Audit
A trader closes five hypothetical futures trades with P&L of Rs 12,000, -Rs 8,500, Rs 3,000, -Rs 15,000 and Rs 6,500.
Turnover is the sum of the absolute differences, Rs 45,000, even though the net result is a loss of Rs 2,000; the gross contract value of the trades does not enter it.

---

## Pitfalls

- **Holding Wash-Sale Losses Across Year-End**: Realising losses in November and December and buying back within 30 days while holding the replacement shares into the new year defers those losses into the basis of the new shares, while tax on the year's gains is still due.
- **Assuming Your Broker Has Already Dropped the PDT Rule**: FINRA's intraday margin standards took effect on June 4, 2026, but brokers may phase them in until October 20, 2027, so a broker can still enforce the old four-trades and $25,000 rule in November 2026.
- **Failing to Make Section 475(f) Election in Timely Manner**: Attempting to claim ordinary loss deductions without filing the Section 475(f) election with the IRS by the due date of the prior year's tax return (April 15).
- **Ignoring Locate Borrow Fees on Hard-to-Borrow (HTB) Shorts**: Shorting heavily shorted stocks without monitoring the borrow fee, which is reset daily and can become a large annualised cost.
- **Miscalculating F&O Turnover in Indian Markets**: Calculating turnover as gross trade value rather than the sum of absolute trade-level differences (plus option-sale premium per ICAI), wrongly concluding that a tax audit is required.

---

## Interview questions

> [!question]- mkt-reg-001 | What defines a Pattern Day Trader (PDT) under FINRA Rule 4210?
> Under the rule in force until June 4, 2026: a margin customer who executes four or more day trades within five business days, provided those day trades are more than 6% of total trades.
> FINRA's intraday margin standards (Regulatory Notice 26-10) deleted the designation from June 4, 2026, with brokers allowed to phase in until October 20, 2027.

> [!question]- mkt-reg-002 | What is the minimum equity requirement for a Pattern Day Trader under FINRA rules?
> $25,000 under the former rule; the 2026 amendments delete the minimum, though a broker still in its phase-in period (until October 20, 2027) may apply it.

> [!question]- mkt-reg-003 | What happens if a PDT account falls below $25,000 in equity?
> Under the former rule it could not day trade until equity was restored to $25,000; under the 2026 standards there is no equity floor, and the restriction instead follows unmet intraday margin deficits (90 calendar days for a customer with a practice of not meeting them).

> [!question]- mkt-reg-004 | What is Day Trading Buying Power (DTBP) under FINRA rules?
> Under the former rule, four times the maintenance margin excess as of the prior day's close; the 2026 amendments replace buying-power limits with the intraday margin deficit test of new Rule 4210(d)(2).

> [!question]- mkt-reg-005 | What is the 61-day window under the IRS Wash-Sale Rule (IRC Section 1091)?
> The 30 calendar days before the sale date, the day of the sale, and the 30 calendar days after the sale date.

> [!question]- mkt-reg-006 | What happens to a disallowed loss under the IRS Wash-Sale Rule?
> The disallowed loss is added to the cost basis of the newly acquired replacement security.

> [!question]- mkt-reg-007 | Does the Wash-Sale Rule apply across multiple accounts owned by the same individual (including IRAs)?
> Yes: the rule looks at purchases by the taxpayer in any account, and Rev. Rul. 2008-5 applies it to a repurchase inside the taxpayer's IRA or Roth IRA.

> [!question]- mkt-reg-008 | What is the tax penalty if a wash sale occurs between a taxable account and an IRA?
> Under Rev. Rul. 2008-5 the loss is disallowed and the IRA's basis is not increased, so the loss is effectively lost for tax purposes.

> [!question]- mkt-reg-009 | What is a Section 1256 Contract under the US Internal Revenue Code?
> Under IRC 1256(b): a regulated futures contract, foreign currency contract, nonequity option (for example a broad-based index option), dealer equity option or dealer securities futures contract.

> [!question]- mkt-reg-010 | What is the 60/40 tax rule for Section 1256 contracts?
> Net capital gains are automatically taxed as 60% long-term capital gains and 40% short-term capital gains, regardless of holding time.

> [!question]- mkt-reg-011 | Does the Wash-Sale Rule apply to Section 1256 futures contracts?
> Section 1256(f)(5) provides that the wash-sale rule does not apply to losses recognised by the year-end mark to market, and because open contracts are marked at year-end there is no deferred loss to disallow.

> [!question]- mkt-reg-012 | What is the primary tax benefit of an IRC Section 475(f) Mark-to-Market election for active traders?
> Net trading losses are ordinary, so the $3,000 capital-loss limit does not apply and wash sales do not apply to marked securities; large losses can still be capped by the excess business loss limit of IRC 461(l).

> [!question]- mkt-reg-013 | When must an existing taxpayer file an IRC Section 475(f) election with the IRS?
> By the due date (without extensions) of the tax return for the tax year prior to the year the election takes effect (typically April 15).

> [!question]- mkt-reg-014 | What is the Locate Requirement under SEC Regulation SHO Rule 203(b)?
> A broker-dealer may not accept or effect a short sale unless it has borrowed the security, arranged to borrow it, or has reasonable grounds to believe it can be borrowed for delivery when due, and has documented this.

> [!question]- mkt-reg-015 | What is a Hard-to-Borrow (HTB) stock?
> A security where available lending supply is scarce, requiring short sellers to pay a negative borrow fee (rebate) to share lenders.

> [!question]- mkt-reg-016 | What is an SEC Regulation SHO Rule 204 mandatory close-out?
> A participant of a registered clearing agency with a fail to deliver must close it out by borrowing or buying shares: by the start of trading on the settlement day after settlement date for short sales (T+2 under T+1 settlement), and by the third settlement day after settlement date for long sales and bona fide market making.

> [!question]- mkt-reg-017 | What is a threshold security under SEC Regulation SHO?
> An equity security with aggregate fails to deliver for five consecutive settlement days of 10,000 shares or more, equal to at least 0.5% of total shares outstanding, and included on an SRO threshold list (Rule 203(c)(6)).

> [!question]- mkt-reg-018 | What is the Customer Protection Rule (SEC Rule 15c3-3)?
> It requires a broker-dealer to keep possession or control of customers' fully paid and excess margin securities, and to hold cash in a special reserve bank account for the exclusive benefit of customers, sized by the reserve formula.

> [!question]- mkt-reg-019 | What is the maximum insurance protection provided by the Securities Investor Protection Corporation (SIPC)?
> Up to $500,000 per customer, including a $250,000 limit for cash (SIPC, as of November 2026).

> [!question]- mkt-reg-020 | Does SIPC insurance protect investors against market losses on open positions?
> No: SIPC restores customer securities and cash missing when a member broker-dealer fails; it does not cover market losses.

> [!question]- mkt-reg-021 | What is Securities Transaction Tax (STT) in Indian equity markets?
> A regulatory turnover tax levied directly on the value of taxable securities transactions executed on recognized Indian stock exchanges.

> [!question]- mkt-reg-022 | Under Section 43(5) of the Indian Income Tax Act, how are equity F&O derivatives classified?
> As non-speculative business income: section 43(5) of the 1961 Act excludes eligible exchange-traded derivatives from speculative transactions (the Income-tax Act, 2025 renumbers the provision from April 1, 2026).

> [!question]- mkt-reg-023 | How is intraday equity cash trading classified for tax purposes in India?
> As Speculative Business Income (cannot be offset against non-speculative business income).

> [!question]- mkt-reg-024 | How is absolute turnover calculated for futures trading under Indian Section 44AB?
> The sum of the absolute favourable and unfavourable differences on each trade, i.e. sum |P&L|, per ICAI's Guidance Note on Tax Audit; Example 2 gives Rs 45,000 for five trades netting to a Rs 2,000 loss.

> [!question]- mkt-reg-025 | What is the purpose of the mandatory Chartered Accountant tax audit under Indian Section 44AB?
> To audit business accounts when turnover exceeds the statutory limit: Rs 1 crore, or Rs 10 crore when cash receipts and cash payments are each no more than 5% of the totals.

> [!question]- mkt-reg-026 | Can Indian traders carry forward non-speculative business losses from F&O trading?
> Yes, non-speculative business losses can be carried forward for up to 8 consecutive assessment years to offset future business income.

> [!question]- mkt-reg-027 | What is Federal Reserve Regulation T initial margin on US equity cash shares?
> 50% initial margin for margin equity securities (12 CFR 220.12), so a long purchase can be at most 2-to-1 leveraged at inception.

> [!question]- mkt-reg-028 | What is portfolio margin compared to traditional Regulation T margin?
> A risk-based framework under FINRA Rule 4210(g) that sets margin from the largest loss across a range of price moves, using theoretical prices from an SEC-approved model (in practice values supplied by the OCC).

> [!question]- mkt-reg-029 | What is the minimum account equity typically required by US brokers to qualify for Portfolio Margin?
> There is no single regulatory figure to quote: brokers may set higher house minimums for portfolio margin, so check the broker's disclosure.
> As of November 2026, FINRA Rule 4210(g)(4)(C) bars positions in unlisted derivatives unless the account establishes and maintains equity of at least $5 million.
> As of November 2026, FINRA Rule 4210(g)(1)(K) requires each portfolio margin account with less than $5 million in equity to maintain margin for intraday risk.

> [!question]- mkt-reg-030 | What is CFTC Rule 1.20 regarding futures customer funds?
> It requires futures commission merchants (FCMs) to separately account for and segregate futures customer funds, holding enough at all times to cover their total obligations to customers, at permitted depositories with written acknowledgments.

> [!question]- mkt-reg-031 | What is a short squeeze forced buy-in under clearinghouse operations?
> When a clearing broker involuntarily purchases shares in the open market to cover a client's short position because borrowed shares were recalled.

> [!question]- mkt-reg-032 | What is the primary golden rule of trading operations and compliance?
> Never let operational friction, regulatory penalties, or unhedged tax liabilities erode trading edge.

## In this repo and The-Distinguished-Engineer

- Code: [mkt_exec_02_regulation_tax.py](../code/mkt_exec_02_regulation_tax.py) prints and asserts every computed number in this note; the wash-sale window is counted with calendar dates, the basis example is checked against the economics of both lots, and the 60/40 rate by taxing a stated gain; rules and rates are cited constants with their sources and dates; run it with `uv run --no-project --with numpy python 16-Trading-and-Investing/code/mkt_exec_02_regulation_tax.py`.
- Syllabus: [Fragmentation, Reg NMS and Routing](../../07-Market-Microstructure/09-Fragmentation-Reg-NMS-and-Routing.md).

---

## Further reading

- Financial Industry Regulatory Authority. (2026). *Regulatory Notice 26-10: Intraday Margin Standards*. April 20, 2026; SEC approval Release 34-105226 (April 14, 2026).
- Financial Industry Regulatory Authority. *FINRA Rule 4210: Margin Requirements*. FINRA Manual (as of November 2026).
- Internal Revenue Service. (2008). *Revenue Ruling 2008-5*. Internal Revenue Bulletin 2008-3.
- Internal Revenue Service. (2025). *Rev. Proc. 2025-32* (2026 inflation adjustments) and *Publication 550: Investment Income and Expenses*.
- Securities and Exchange Commission. (2004). *Short Sales (Regulation SHO)*. Release 34-50103; Rule 204 adopted in Release 34-60388 (2009). 17 CFR 242.200-204.
- Government of India. (2026). *Finance Bill 2026, Memorandum Explaining the Provisions* (STT, clause 143).
- Institute of Chartered Accountants of India. (2026). *Guidance Note on Tax Audit under Section 44AB of the Income-tax Act, 1961* (revised 2026 edition).
