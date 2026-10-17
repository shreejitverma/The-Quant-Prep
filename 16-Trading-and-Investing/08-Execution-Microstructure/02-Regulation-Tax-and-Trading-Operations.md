---
type: concept
track: [quant-trader, quant-risk]
tier: core
status: solid
prereqs: []
est_hours: 4
sources: [FINRA Rule 4210 - Margin Requirements, Internal Revenue Code - Section 1091 (Wash Sales) and Section 1256, SEC Regulation SHO - Regulation of Short Sales (17 CFR 242.200-204), Income Tax Act of India (1961) - Section 43(5) and Section 44AB]
---

# Regulation, Tax, and Trading Operations

## TL;DR

- Regulatory frameworks and tax structures govern the real-world operational feasibility, margin leverage limits, and net post-friction profitability of market participants.
- The Pattern Day Trader (PDT) rule under FINRA Rule 4210 requires US margin accounts executing four or more day trades within five business days to maintain a minimum equity balance of $25,000.
- The IRS Wash-Sale Rule (IRC Section 1091) disallows the deduction of a capital loss if a substantially identical security is acquired within 30 days before or after the sale date, adding the disallowed loss to the cost basis of the new position.
- IRC Section 1256 grants advantageous 60/40 tax treatment to regulated futures and broad-based index options, taxing 60% of gains at long-term capital gains rates and 40% at short-term rates regardless of holding period.
- SEC Regulation SHO enforces locate requirements (Rule 203) before executing short sales and mandates strict buy-in closeout schedules (Rule 204) to eliminate abusive naked short selling and persistent fails to deliver.

## Learning objectives

- Formulate and apply the FINRA Pattern Day Trader (PDT) margin rules and intraday buying power calculations.
- Deconstruct the 61-day window of the IRS Wash-Sale Rule and calculate adjusted cost basis across complex trading sequences.
- Compare the tax implications of trading equity shares versus Section 1256 futures and broad-based index options.
- Evaluate the requirements and benefits of the IRS Section 475(f) Mark-to-Market election for active traders.
- Navigate SEC Regulation SHO locate rules (Rule 203) and mandatory clearinghouse closeout thresholds (Rule 204).
- Analyze Indian securities taxation, including Securities Transaction Tax (STT), turnover definitions, and business income treatment under Section 43(5).

## Core concepts

### 1. The Pattern Day Trader (PDT) Rule (FINRA Rule 4210)

Under Financial Industry Regulatory Authority (FINRA) Rule 4210 and Federal Reserve Regulation T, an individual trading through a US margin brokerage account is classified as a **Pattern Day Trader (PDT)** if:
- They execute four or more **day trades** (opening and closing the same security position within the same regular trading day) within any rolling five-business-day window.
- The number of day trades represents more than 6% of the customer's total trades during that period.

```
+-----------------------------------------------------------------------+
|                    FINRA PATTERN DAY TRADER CONSTRAINTS               |
+-----------------------------------------------------------------------+
| Account Equity >= $25,000        | Account Equity < $25,000           |
|----------------------------------+------------------------------------|
| Day Trading Buying Power = 4x    | Maximum 3 day trades per rolling   |
| Maintenance Margin Excess        | 5 business days.                   |
|                                  | If 4th trade executed:             |
| Unrestricted day trading allowed | Account flagged; day trading locked|
| Overnight Buying Power = 2x Reg T| for 90 days or until $25k deposited|
+-----------------------------------------------------------------------+
```

Day Trading Buying Power (DTBP) is calculated at the beginning of each trading day:
$$\text{DTBP} = 4 \times (\text{Account Equity} - \text{Maintenance Margin Requirement})$$
If a trader exceeds their DTBP during the day, the broker issues a **Day Trading Margin Call**, giving the trader five business days to deposit funds while restricting execution leverage to 2x.

### 2. The IRS Wash-Sale Rule (IRC Section 1091)

Under Section 1091 of the Internal Revenue Code, a taxpayer cannot claim a tax deduction for a loss on the sale of stock or securities if the taxpayer acquires a **substantially identical** security within a 61-day window:
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
1. The loss is disallowed for the current tax year.
2. The disallowed dollar loss is added directly to the cost basis of the newly acquired replacement shares:
$$\text{New Cost Basis} = \text{Purchase Price of New Shares} + \text{Disallowed Loss}$$
3. The holding period of the original shares is added to the holding period of the new shares.
Active retail traders who trade the same security back and forth throughout December without closing all positions prior to January frequently discover that their tax deductible losses are disallowed, leaving them with massive tax liabilities on gross profits.

### 3. Section 1256 Contracts and the 60/40 Rule

To eliminate wash-sale tracking complexity on standardized derivatives, the US Congress enacted Internal Revenue Code Section 1256.
A **Section 1256 Contract** includes:
- Regulated futures contracts (e.g. CME S&P 500 E-mini, Nasdaq 100 E-mini, Crude Oil, Gold, Treasuries).
- Foreign currency futures and eligible forward contracts.
- Non-equity broad-based index options (e.g. SPX, NDX, RUT cash-settled options, and VIX options).

Section 1256 contracts receive two major tax advantages:
1. **The 60/40 Capital Gains Split**: Regardless of how briefly the contract was held (even if held for only two seconds), all net capital gains are taxed as:
   - 60% Long-Term Capital Gains rate (maximum federal rate 20%).
   - 40% Short-Term Capital Gains rate (ordinary income rate, maximum 37%).
   - Maximum blended federal tax rate of approximately 26.8% (versus 37.0% for short-term single-stock trading).
2. **Mark-to-Market Accounting at Year-End**: All open Section 1256 contracts are deemed sold at their fair market settlement value on the final business day of the tax year; open paper profits or losses are realized, and the Wash-Sale Rule does not apply.

### 4. Section 475(f) Mark-to-Market Election for Professional Traders

Professional day traders who qualify under the IRS definition of **Trader in Securities Status (TSS)** can make an election under IRC Section 475(f).
Under Section 475(f):
- All open trading positions are marked to market on December 31.
- All gains and losses are treated as **Ordinary Income and Ordinary Losses** rather than capital gains.
- The standard $3,000 annual net capital loss limitation is eliminated; active traders can deduct unlimited net trading losses against other income sources (such as spousal wages or interest).
- The Wash-Sale Rule is completely eliminated for trading accounts.

### 5. SEC Regulation SHO: Short Sale Governance

Adopted in 2004 and updated in 2008, SEC Regulation SHO governs short selling in US equity markets:
1. **Rule 203(b)(1) - The Locate Requirement**: A broker-dealer cannot accept or execute a short sale order unless the broker has:
   - Borrowed the security, or
   - Entered into a bona-fide arrangement to borrow the security, or
   - Reasonable grounds to believe that the security can be borrowed so that it can be delivered on the settlement date (an official "Locate").
2. **Rule 204 - Close-Out Requirements for Fails to Deliver (FTD)**:
   - If a participant has a fail-to-deliver position in an equity security at a registered clearing agency (NSCC) following settlement, the participant must close out the fail by borrowing or purchasing shares of like kind.
   - For standard sales, the closeout must occur before trading open on the morning of $T+3$ (under $T+1$ settlement, $T+2$).
   - For threshold securities (stocks with persistent aggregate fails exceeding 10,000 shares and 0.5% of outstanding float), mandatory buy-in rules are triggered.

### 6. Indian Markets: Taxation and Turnover Framework (SEBI / Income Tax Act)

In India, trading taxation is defined under the Income Tax Act of 1961:
1. **Tax Treatment of F&O Derivatives**: Under Section 43(5), transactions in exchange-traded futures and options are officially classified as **Non-Speculative Business Income** (unlike equity intraday trading, which is classified as Speculative Business Income).
   - Losses on F&O can be offset against any other business income and carried forward for up to 8 assessment years.
2. **Securities Transaction Tax (STT)**:
   - Levied directly on turnover at execution.
   - Equity intraday: 0.025% on the sell side.
   - Futures: 0.02% on the sell side (increased by Finance Act 2024).
   - Options: 0.10% on the option premium on the sell side, and 0.125% on intrinsic value for exercised options.
3. **Turnover Definition under Section 44AB for Tax Audits**:
   - For Futures: Total absolute turnover = Sum of positive and negative PnL across all closed trades.
   - For Options: Total absolute turnover = Sum of absolute PnL across all trades plus total option sale premium received.
   - If total turnover exceeds ₹10 Crore (where digital transactions exceed 95%), a mandatory independent Chartered Accountant tax audit is required.

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

---

## Pitfalls

- **Holding Wash-Sale Losses Across Year-End**: Incurring massive wash sales in November and December while holding the replacement shares into the new year, which locks the loss deduction into the subsequent tax year while tax on earlier gains is due immediately.
- **Triggering Pattern Day Trader Lockout Under $25,000**: Executing a 4th day trade in an account with $24,500 in equity, causing the broker to freeze the account to closing transactions only for 90 days.
- **Failing to Make Section 475(f) Election in Timely Manner**: Attempting to claim ordinary loss deductions without filing the Section 475(f) election with the IRS by the due date of the prior year's tax return (April 15).
- **Ignoring Locate Borrow Fees on Hard-to-Borrow (HTB) Shorts**: Shorting heavily shorted stocks without monitoring negative rebate rates (which can exceed 50% to 100% annualized daily borrow cost).
- **Miscalculating F&O Turnover in Indian Markets**: Calculating turnover as gross trade value rather than absolute sum of profits and losses, erroneously triggering costly mandatory tax audits.

---

## Interview questions

> [!question]- mkt-reg-001 | What defines a Pattern Day Trader (PDT) under FINRA Rule 4210?
> A margin account customer who executes four or more day trades within five business days, provided day trades exceed 6% of total trades.

> [!question]- mkt-reg-002 | What is the minimum equity requirement for a Pattern Day Trader under FINRA rules?
> A minimum of $25,000 in account equity prior to engaging in day trading.

> [!question]- mkt-reg-003 | What happens if a PDT account falls below $25,000 in equity?
> The account is restricted from executing further day trades until equity is brought back to $25,000, or limited to closing orders only.

> [!question]- mkt-reg-004 | What is Day Trading Buying Power (DTBP) under FINRA rules?
> Up to four times the account's maintenance margin excess calculated at the beginning of the trading day.

> [!question]- mkt-reg-005 | What is the 61-day window under the IRS Wash-Sale Rule (IRC Section 1091)?
> The 30 calendar days before the sale date, the day of the sale, and the 30 calendar days after the sale date.

> [!question]- mkt-reg-006 | What happens to a disallowed loss under the IRS Wash-Sale Rule?
> The disallowed loss is added to the cost basis of the newly acquired replacement security.

> [!question]- mkt-reg-007 | Does the Wash-Sale Rule apply across multiple accounts owned by the same individual (including IRAs)?
> Yes, the IRS explicitly aggregates transactions across all accounts, including taxable brokerage accounts and tax-advantaged IRAs.

> [!question]- mkt-reg-008 | What is the tax penalty if a wash sale occurs between a taxable account and an IRA?
> The loss is permanently disallowed; it cannot be added to the IRA cost basis and is completely lost for tax purposes.

> [!question]- mkt-reg-009 | What is a Section 1256 Contract under the US Internal Revenue Code?
> A regulated futures contract, foreign currency contract, or broad-based non-equity index option.

> [!question]- mkt-reg-010 | What is the 60/40 tax rule for Section 1256 contracts?
> Net capital gains are automatically taxed as 60% long-term capital gains and 40% short-term capital gains, regardless of holding time.

> [!question]- mkt-reg-011 | Does the Wash-Sale Rule apply to Section 1256 futures contracts?
> No, Section 1256 contracts are marked to market on December 31 and are legally exempt from the Wash-Sale Rule.

> [!question]- mkt-reg-012 | What is the primary tax benefit of an IRC Section 475(f) Mark-to-Market election for active traders?
> Net trading losses are treated as ordinary losses (exempt from the $3,000 annual net capital loss limit) and wash sales are eliminated.

> [!question]- mkt-reg-013 | When must an existing taxpayer file an IRC Section 475(f) election with the IRS?
> By the due date (without extensions) of the tax return for the tax year prior to the year the election takes effect (typically April 15).

> [!question]- mkt-reg-014 | What is the Locate Requirement under SEC Regulation SHO Rule 203(b)?
> Brokers must locate and document available borrowable shares before executing any customer short sale order.

> [!question]- mkt-reg-015 | What is a Hard-to-Borrow (HTB) stock?
> A security where available lending supply is scarce, requiring short sellers to pay a negative borrow fee (rebate) to share lenders.

> [!question]- mkt-reg-016 | What is an SEC Regulation SHO Rule 204 mandatory close-out?
> A requirement that clearing firms buy in or borrow shares to resolve a fail-to-deliver (FTD) within specified settlement deadlines.

> [!question]- mkt-reg-017 | What is a threshold security under SEC Regulation SHO?
> An equity security with aggregate fails to deliver for five consecutive settlement days of 10,000 shares or more, representing at least 0.5% of float.

> [!question]- mkt-reg-018 | What is the Customer Protection Rule (SEC Rule 15c3-3)?
> A rule requiring broker-dealers to maintain customer fully paid and excess margin securities in a segregated, protected reserve account.

> [!question]- mkt-reg-019 | What is the maximum insurance protection provided by the Securities Investor Protection Corporation (SIPC)?
> Up to $500,000 per customer, including a maximum limit of $250,000 for uninvested cash claims.

> [!question]- mkt-reg-020 | Does SIPC insurance protect investors against market losses on open positions?
> No, SIPC protects exclusively against the theft or insolvency of the registered broker-dealer custodian.

> [!question]- mkt-reg-021 | What is Securities Transaction Tax (STT) in Indian equity markets?
> A regulatory turnover tax levied directly on the value of taxable securities transactions executed on recognized Indian stock exchanges.

> [!question]- mkt-reg-022 | Under Section 43(5) of the Indian Income Tax Act, how are equity F&O derivatives classified?
> As Non-Speculative Business Income.

> [!question]- mkt-reg-023 | How is intraday equity cash trading classified for tax purposes in India?
> As Speculative Business Income (cannot be offset against non-speculative business income).

> [!question]- mkt-reg-024 | How is absolute turnover calculated for futures trading under Indian Section 44AB?
> The sum of all positive and negative profit and loss amounts across all executed trades.

> [!question]- mkt-reg-025 | What is the purpose of the mandatory Chartered Accountant tax audit under Indian Section 44AB?
> To independently audit business books of accounts when trading turnover exceeds specified statutory limits (e.g. ₹10 Crore with digital transactions).

> [!question]- mkt-reg-026 | Can Indian traders carry forward non-speculative business losses from F&O trading?
> Yes, non-speculative business losses can be carried forward for up to 8 consecutive assessment years to offset future business income.

> [!question]- mkt-reg-027 | What is Federal Reserve Regulation T initial margin on US equity cash shares?
> 50% initial margin, allowing a maximum of 2-to-1 overnight leverage for long equity purchases.

> [!question]- mkt-reg-028 | What is portfolio margin compared to traditional Regulation T margin?
> A risk-based margin framework (using TIMS) calculating margin requirements based on net portfolio risk across modeled stress scenarios.

> [!question]- mkt-reg-029 | What is the minimum account equity typically required by US brokers to qualify for Portfolio Margin?
> A minimum of $100,000 to $125,000 in unencumbered account equity.

> [!question]- mkt-reg-030 | What is CFTC Rule 1.20 regarding futures customer funds?
> Mandating that futures commission merchants (FCMs) strictly segregate customer commodity funds from firm proprietary capital.

> [!question]- mkt-reg-031 | What is a short squeeze forced buy-in under clearinghouse operations?
> When a clearing broker involuntarily purchases shares in the open market to cover a client's short position because borrowed shares were recalled.

> [!question]- mkt-reg-032 | What is the primary golden rule of trading operations and compliance?
> Never let operational friction, regulatory penalties, or unhedged tax liabilities erode trading edge.

---

## Further reading

- Financial Industry Regulatory Authority. (2021). *FINRA Rule 4210: Margin Requirements*. FINRA Manual.
- Internal Revenue Service. (2023). *Publication 550: Investment Income and Expenses (Including Capital Gains and Losses)*. US Department of the Treasury.
- Securities and Exchange Commission. (2004). *Regulation SHO: Regulation of Short Sales*. 17 CFR Part 242.
- Taxmann. (2024). *Direct Taxes Law & Practice: Taxation of Derivatives and Speculative Transactions*. Taxmann Publications.
