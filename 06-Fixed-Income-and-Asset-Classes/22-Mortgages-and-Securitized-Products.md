---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: solid
prereqs: [callable-and-bermudan-products]
est_hours: 5
sources: [SIFMA Uniform Practices for the Clearance and Settlement of Mortgage-Backed Securities, Frank Fabozzi - The Handbook of Mortgage-Backed Securities, Bruce Tuckman and Angel Serrat - Fixed Income Securities chapter 20]
---

# Mortgages and Securitized Products

## TL;DR

Agency Mortgage-Backed Securities (MBS) pool thousands of conforming residential mortgages into liquid pass-through certificates backed by government or agency guarantees (Ginnie Mae, Fannie Mae, Freddie Mac).
Because residential borrowers hold a continuous, uncompensated option to prepay their mortgage at par, MBS exhibit pronounced negative convexity.
When interest rates fall, prepayments accelerate, shortening duration and capping price upside (contraction risk); when rates rise, prepayments dry up, lengthening duration and amplifying losses (extension risk).
Prepayment speeds are parameterized by Single Monthly Mortality (SMM), Constant Prepayment Rate (CPR), and the Public Securities Association (PSA) benchmark.
The forward To-Be-Announced (TBA) market allows liquid forward trading and dollar roll financing without specific pool selection prior to delivery.

## Learning objectives

- Differentiate Agency MBS from Non-Agency securitizations across credit, liquidity, and guarantee structures.
- Calculate prepayment metrics: Single Monthly Mortality (SMM), Constant Prepayment Rate (CPR), and PSA benchmark schedules.
- Formulate the core economic drivers of prepayment: refinancing incentive, turnover, curtailment, and pool burnout.
- Analyze the negative convexity profile of mortgage pass-throughs and evaluate contraction and extension risk.
- Explain the trading mechanics of the TBA forward market, cheapest-to-deliver allocation, and dollar roll financing.
- Value structured tranches: Sequential pay, Planned Amortization Class (PAC), and Interest-Only (IO) / Principal-Only (PO) strips.

## Core concepts

### 1. Agency MBS vs Non-Agency Securitization

Securitization transforms illiquid pools of individual residential and commercial loans into tradeable, rated fixed income securities.
The US mortgage market divides into two distinct segments:
1. **Agency MBS:** Securities issued or guaranteed by Government-Sponsored Enterprises (GSEs):
   - **Ginnie Mae (GNMA):** Backed by the full faith and credit of the US Federal Government.
   Covers loans insured by the Federal Housing Administration (FHA) and Department of Veterans Affairs (VA).
   - **Fannie Mae (FNMA) and Freddie Mac (FHLMC):** Quasi-governmental GSEs operating under federal conservatorship.
   Cover conforming conventional mortgages meeting strict size, loan-to-value (LTV), and credit score criteria.
   Agency MBS carry near-zero credit default risk; their dominant risk factor is **prepayment risk**.
2. **Non-Agency (Private-Label) MBS:** Issued by commercial and investment banks without government backing.
   Cover non-conforming loans (jumbo loans exceeding conforming limits, Alt-A, subprime).
   These securities utilize internal credit enhancement (senior-subordinated tranching, excess spread, overcollateralization) and carry substantial credit, default, and loss-severity risk.

### 2. Mortgage Pass-Through Mechanics

In a standard residential mortgage pass-through certificate, homeowner monthly payments are collected by a mortgage servicer, stripped of servicing and guarantee fees (typically $25\text{ to }50\text{ bps}$ per annum), and passed through pro rata to investors.

Each monthly payment $PMT$ made by a homeowner consists of two components:
$$PMT = \text{Interest}_t + \text{Scheduled Principal}_t + \text{Prepayment}_t$$
1. **Interest Component:** Calculated on the remaining balance:
$$\text{Interest}_t = \text{Balance}_{t-1} \times \frac{r_{\text{mortgage}}}{12}$$
2. **Scheduled Principal:** Fixed amortization that grows over the loan's 30-year lifetime.
3. **Prepayment:** Unscheduled early principal payoff.
When a borrower refinances, sells a home, or pays down extra principal, that cash is returned immediately to pass-through certificate holders at par ($100$).

### 3. Prepayment Metrics: SMM, CPR, and PSA

Prepayment risk is quantified using three standard mathematical metrics.

#### Single Monthly Mortality (SMM)
SMM is the percentage of outstanding principal at the start of the month that is prepaid during that month, net of scheduled principal amortization:
$$\text{SMM}_t = \frac{\text{Prepayments}_t}{\text{Beginning Balance}_t - \text{Scheduled Principal}_t}$$

#### Constant Prepayment Rate (CPR)
CPR is the annualized equivalent of SMM, assuming constant compounding over 12 months:
$$1 - \text{CPR} = (1 - \text{SMM})^{12}$$
$$\text{CPR} = 1 - (1 - \text{SMM})^{12}$$
Inverting this expression yields monthly SMM from annual CPR:
$$\text{SMM} = 1 - (1 - \text{CPR})^{1/12}$$

#### The Public Securities Association (PSA) Benchmark
The PSA model is an empirical baseline schedule of prepayment speeds for 30-year residential mortgages:
- In month 1, CPR is $0.2\%$.
- CPR increases linearly by $0.2\%$ per month for the first 30 months, reaching $6.0\%$ CPR at month 30.
- From month 30 through month 360, CPR remains constant at $6.0\%$.

Mathematically, for benchmark $100\%$ PSA speed:
$$\text{CPR}(m) = \begin{cases} 0.06 \times \left(\frac{m}{30}\right) = 0.002 \times m, & 1 \le m \le 30 \\ 0.06 = 6.0\%, & m > 30 \end{cases}$$
Prepayment expectations are quoted as a multiple of this benchmark:
- $150\%$ PSA: CPR ramp reaches $6.0\% \times 1.5 = 9.0\%$ at month 30.
- $50\%$ PSA: CPR ramp reaches $6.0\% \times 0.5 = 3.0\%$ at month 30.

### 4. Economic Drivers of Prepayment

Prepayment forecasting models (such as those developed by Andrew Davidson, BlackRock, or banks) model prepayments as a sum of four distinct behavioral components:
1. **Refinancing Incentive:** The primary driver.
When prevailing mortgage rates drop significantly below the loan's note rate ($r_{\text{note}} - r_{\text{market}} \ge 50\text{ to }100\text{ bps}$), borrowers refinance into lower-rate loans, paying off the existing mortgage at par.
2. **Housing Turnover:** Home sales driven by employment relocations, family changes, or lifestyle upgrades require existing mortgages to be settled at closing.
Turnover occurs even when prevailing rates are higher than the existing note rate.
3. **Curtailments:** Partial principal prepayments made by borrowers seeking to accelerate debt retirement.
4. **Pool Burnout:** As interest rates fall and stay low, financially sophisticated borrowers refinance early.
The borrowers remaining in the pool are un-refinanceable (due to poor credit, high LTV, low documentation) or financially inert.
Consequently, during subsequent rate drops, the prepayment speed of an older "burned-out" pool fails to accelerate, exhibiting lower prepayment sensitivity.

### 5. Negative Convexity and Extension/Contraction Risk

Because homeowners possess an uncompensated call option on their mortgage debt at par, an Agency MBS behaves like a long position in a straight bond combined with a short American call option on the bond:
$$\text{Price}(\text{MBS}) = \text{Price}(\text{Bond}) - \text{Price}(\text{Prepayment Option})$$

#### Negative Convexity Dynamics
- **Yields Fall (Contraction Risk):** When interest rates drop, homeowners refinance.
Prepayments surge, returning cash to MBS holders at par.
The price of the MBS cannot rise much above $100$ (or par plus premium).
The investor must reinvest the returned capital at prevailing low market yields.
Modified duration contracts rapidly (e.g., from 6 years down to 1.5 years).
- **Yields Rise (Extension Risk):** When interest rates rise, refinancing activity ceases.
Homeowners hold onto their low-rate mortgages.
Expected mortgage lifetimes extend from 5-7 years out to 15-25 years.
Duration extends rapidly (e.g., from 4 years up to 9 years) precisely when interest rates are surging, amplifying capital losses.

The resulting price-yield curve curves downward ($\partial^2 P / \partial y^2 < 0$), exhibiting negative convexity across the refinancing corridor.

### 6. The TBA Forward Market and Dollar Rolls

Agency MBS trade predominantly in the forward **To-Be-Announced (TBA)** market.
In a TBA trade, buyers and sellers agree on five basic parameters:
1. Issuer (Fannie Mae, Freddie Mac, Ginnie Mae).
2. Maturity (30-year, 15-year).
3. Coupon (e.g. 5.5%, 6.0%).
4. Settlement date (monthly SIFMA calendar settlement).
5. Price and notional.

Specific mortgage pool numbers are not identified at the trade date.
Under the SIFMA **48-Hour Rule**, the seller must notify the buyer of the exact pool IDs to be delivered by 3:00 p.m. ET two business days before settlement.
Because the seller chooses which pools to deliver, the seller delivers the **Cheapest-to-Deliver (CTD)** pools (typically pools with the worst geographic concentration, highest prepayment risk, or fast-paying characteristics).

#### The Dollar Roll
A **Dollar Roll** is a financing transaction in the TBA market.
An investor who owns current-month TBA contracts sells them for current-month settlement and simultaneously buys future-month TBAs of the same agency, coupon, and maturity.
- The investor gives up current-month principal, interest, and prepayments.
- In return, the investor receives cash today (which is invested at overnight or repo rates) and buys the forward TBA at a discount called the **Drop**:
$$\text{Drop} = \text{Front-Month Price} - \text{Back-Month Price}$$
The **implied financing rate** of the dollar roll measures the effective borrowing rate locked in by the trade.
When implied financing rates trade below general collateral (GC) repo rates, the dollar roll is said to trade "on special", providing an attractive funding source for mortgage desks.

### 7. Collateralized Mortgage Obligations (CMOs)

Pass-through securities pool all cash flows pro rata.
**Collateralized Mortgage Obligations (CMOs)** re-tranche pass-through cash flows to redirect prepayment risk into tailored risk-return profiles:
1. **Sequential Pay Tranches (A, B, C, Z):** Tranche A receives all principal payments (scheduled and prepayments) until fully retired; Tranche B then receives all principal, followed by C.
Tranche A has short duration and low extension risk; Tranche C has long duration.
The **Z-Tranche (Accrual Tranche)** receives no interest until earlier tranches are retired, accreting unpaid interest into principal.
2. **Planned Amortization Class (PAC) Tranches:** Protected by a surrounding **Companion / Support Tranche**.
As long as prepayment speeds stay within a specified PAC collar (e.g. 100% to 250% PSA), the PAC tranche receives a guaranteed, deterministic amortization schedule.
The companion tranche absorbs all prepayment variability, experiencing extreme contraction and extension risk.
3. **Stripped MBS: Interest-Only (IO) and Principal-Only (PO):**
   - **PO Strips:** Receive all principal cash flows.
   Sold at a deep discount to par.
   When rates drop and prepayments surge, cash flows arrive faster, generating massive capital gains.
   PO bonds have high positive duration.
   - **IO Strips:** Receive all interest cash flows.
   When rates drop, principal prepays rapidly, extinguishing future interest payments.
   IO prices plummet when rates fall!
   Consequently, IO strips have **negative duration** and act as natural hedges against rising interest rates.

## Worked examples

### Example 1: SMM to CPR Conversion
A mortgage servicer reports that a pool of 30-year fixed-rate mortgages experienced a Single Monthly Mortality of $\text{SMM} = 0.50\%$ ($0.0050$) in June.
Calculate the annualized Constant Prepayment Rate (CPR).

Use the compound annualization formula:
$$\text{CPR} = 1 - (1 - \text{SMM})^{12}$$
Substitute $\text{SMM} = 0.005$:
$$1 - \text{SMM} = 1 - 0.005 = 0.995$$
$$(0.995)^{12} = 0.941623$$
$$\text{CPR} = 1 - 0.941623 = 0.058377 = 5.8377\% \quad (5.84\%)$$
Our reference implementation [`fi_mortgages.py`](code/fi_mortgages.py) confirms:
`smm_to_cpr(0.005) == 0.058377` ($5.84\%$).

### Example 2: PSA Benchmark Prepayment Schedule
Evaluate the projected CPR for:
1. A 10-month-old mortgage pool at $100\%$ PSA.
2. A 30-month-old mortgage pool at $150\%$ PSA.

1. **Month 10 at 100% PSA:**
Since $m = 10 \le 30$:
$$\text{CPR} = 6.0\% \times \left(\frac{10}{30}\right) \times \frac{100}{100} = 6.0\% \times \frac{1}{3} = 2.00\%$$
2. **Month 30 at 150% PSA:**
Since $m = 30$:
$$\text{CPR} = 6.0\% \times \left(\frac{30}{30}\right) \times \frac{150}{100} = 6.0\% \times 1.5 = 9.00\%$$
Our reference implementation [`fi_mortgages.py`](code/fi_mortgages.py) yields:
`psa_cpr(10, 100.0) == 0.02` ($2.0\%$) and `psa_cpr(30, 150.0) == 0.09` ($9.0\%$).

### Example 3: Implied Financing Rate in a Dollar Roll
A mortgage trader holds a 30-year Fannie Mae 6.0% TBA with a current-month settlement price of $P_1 = 101.50$ (settling in 30 days).
The forward-month TBA trades at $P_2 = 101.125$ (settling in 60 days).
The drop is $P_1 - P_2 = 101.50 - 101.125 = 0.375$ ($12/32$, i.e. $12\text{ ticks}$).
Over the 30-day roll period, the expected coupon plus interest earned on reinvested principal is estimated at $\$0.48$ per $\$100$ par.
Calculate the implied financing rate locked in by rolling the position.

Rolling means selling the pool for front-month settlement at $P_1$ and buying it back for forward settlement at $P_2$, giving up the $0.48$ of cash flows in between.
The cost of that financing is the cash flow given up net of the drop:
$$\text{Net Cost} = \text{Expected Cash Flow Given Up} - \text{Drop} = 0.480 - 0.375 = 0.105$$
The trader effectively borrows $P_1$ for 30 days and repays $P_2$ plus the forgone cash flows, so:
$$\text{Implied Rate} = \frac{P_2 + 0.480 - P_1}{P_1} \times \frac{360}{30} = \frac{0.105}{101.50} \times 12 = 1.2414\% \quad (1.24\%)$$
With the Treasury repo rate at $4.50\%$, the roll is trading $4.50\% - 1.24\% = 3.26\%$ ($326\text{ bps}$) "on special".
The trader saves 326 bps by financing MBS in the dollar roll rather than in the general collateral repo market.

### Example 4: Sequential CMO Cash Flow Waterfall
Consider a two-tranche sequential CMO backed by a mortgage pool with initial outstanding balances:
Tranche A balance is $\$60,000,000$ and Tranche B balance is $\$40,000,000$.
In month 1, total principal cash flow (scheduled amortization plus unscheduled prepayments) returned from the collateral is $\$1,500,000$.
Under sequential pay rules, all principal flows to Tranche A until Tranche A is fully retired.
Tranche A receives the full $\$1,500,000$, reducing its ending balance to $\$60,000,000 - \$1,500,000 = \$58,500,000$.
Tranche B receives $\$0$ of principal, maintaining its ending balance at $\$40,000,000$.
Our reference implementation [`fi_mortgages.py`](code/fi_mortgages.py) confirms:
`sequential_cmo_month_waterfall([60_000_000.0, 40_000_000.0], 1_500_000.0)` produces `[1_500_000.0, 0.0]` received and `[58_500_000.0, 40_000_000.0]` ending balances.

## Pitfalls

- **Assuming fixed duration for MBS portfolios:** Quoting a static duration for an Agency MBS ignores the reality that duration shifts from 2 years to 8 years across the refinancing cycle; risk systems must compute dynamic OAS effective duration.
- **Neglecting pool burnout in aging collateral:** Applying uniform prepayment curves to seasoned pools overestimates prepayment speeds; seasoned borrowers who have failed to refinance through multiple rate troughs will not refinance in the next rally.
- **Confusing Agency and Non-Agency credit exposure:** Agency MBS have zero credit default risk but severe prepayment risk; Non-Agency MBS combine prepayment risk with catastrophic credit subordination and loss severity risk.
- **Ignoring the adverse selection of the 48-hour TBA rule:** Sellers in the TBA market deliver the lowest-quality conforming pools; pricing a TBA as an average pool results in systematic overvaluation.
- **Mishandling Interest-Only (IO) duration:** Hedging an IO strip with standard long Treasury bonds compounds risk, because IO bonds possess negative duration (prices rise when interest rates rise).

## Interview questions

> [!question]- fi-mbs-securitized-negative-convexity | Why do Agency MBS exhibit negative convexity?
> Homeowners hold an uncompensated option to prepay their mortgage at par.
> When rates drop, prepayments accelerate, capping bond price appreciation near par and shortening duration.
> When rates rise, prepayments collapse, extending duration and magnifying price declines.

> [!question]- fi-mbs-securitized-smm-to-cpr | How do you convert Single Monthly Mortality (SMM) to Constant Prepayment Rate (CPR)?
> $\text{CPR} = 1 - (1 - \text{SMM})^{12}$.
> SMM is the monthly prepayment percentage; compounding it over 12 months yields the annualized CPR.

> [!question]- fi-mbs-securitized-psa-benchmark | Describe the 100% PSA prepayment benchmark.
> The PSA benchmark starts at $0.2\%$ CPR in month 1, increases by $0.2\%$ each month up to $6.0\%$ CPR at month 30, and remains flat at $6.0\%$ CPR for the remaining life of the mortgage.

> [!question]- fi-mbs-securitized-tba-48hr-rule | What is the TBA market and the 48-hour rule?
> TBA is a liquid forward market where Agency MBS trade on general specifications without specifying pool IDs.
> Under the 48-hour rule, the seller must notify the buyer of the exact pools to be delivered by 3:00 p.m. ET two business days prior to settlement.

> [!question]- fi-mbs-securitized-dollar-roll | What is a dollar roll and why is it used?
> A dollar roll is a transaction where an investor sells a front-month TBA and buys a back-month TBA of the same collateral.
> It serves as a short-term financing vehicle, allowing the investor to borrow funds at the implied financing rate while postponing physical delivery.

> [!question]- fi-mbs-securitized-burnout | What is pool burnout in mortgage prepayment?
> Burnout occurs when a mortgage pool has been exposed to low interest rates over multiple periods.
> Borrowers who were able and willing to refinance have already done so; the remaining borrowers are insensitive or uncreditworthy, dampening future prepayment spikes.

> [!question]- fi-mbs-securitized-pac-vs-companion | How does a PAC tranche differ from a Companion tranche in a CMO?
> A PAC tranche has a protected, predictable principal amortization schedule as long as prepayments remain within a designated PSA collar.
> The companion (support) tranche absorbs all prepayment variability, expanding when prepayments accelerate and contracting when they slow.

> [!question]- fi-mbs-securitized-io-duration | Why do Interest-Only (IO) mortgage strips have negative duration?
> When interest rates rise, homeowners refinance less, extending the remaining principal balance.
> Because IO strips receive interest calculated on that larger balance over a longer period, total cash flows increase, driving the price of the IO strip up when interest rates rise.

> [!question]- fi-mbs-securitized-agency-vs-nonagency | Contrast Agency MBS with Non-Agency MBS regarding credit risk.
> Agency MBS carry explicit or implicit government guarantees against default (Ginnie Mae is full faith and credit; Fannie/Freddie are GSEs), carrying near-zero default risk.
> Non-Agency MBS lack government backing, relying on credit tranching, and expose investors to direct default loss.

> [!question]- fi-mbs-securitized-contraction-extension | Distinguish between contraction risk and extension risk.
> Contraction risk occurs when rates fall: prepayments surge, cash is returned early at par, and duration shrinks.
> Extension risk occurs when rates rise: prepayments collapse, cash flows are deferred into the distant future, and duration lengthens.

## Further reading

- SIFMA, *Uniform Practices for the Clearance and Settlement of Mortgage-Backed Securities and Other Related Securities*, SIFMA Guidelines.
- Frank Fabozzi, *The Handbook of Mortgage-Backed Securities*, 7th Edition, McGraw-Hill, 2016.
- Bruce Tuckman and Angel Serrat, *Fixed Income Securities: Tools for Today's Markets*, Chapter 20: "Mortgages and Mortgage-Backed Securities".
- Andrew Davidson and Alexander Levin, *Mortgage Valuation Models: Embedded Options, Risk, and Uncertainty*, Oxford University Press, 2014.

## In this repo and SDE-Interview-Prep

- Code: [`code/fi_mortgages.py`](code/fi_mortgages.py) (SMM to CPR conversion, PSA benchmark schedules, dollar roll implied financing rates, and sequential CMO cash flow waterfalls).
- Prereq: [Callable and Bermudan Products](20-Callable-and-Bermudan-Products.md).
- Next: [Credit Advanced: CDS Indices and Tranches](23-Credit-Advanced-CDS-Indices-and-Tranches.md).
