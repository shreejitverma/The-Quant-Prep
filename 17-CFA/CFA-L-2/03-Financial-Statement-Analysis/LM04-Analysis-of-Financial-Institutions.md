---
type: cfa-lm
topic: "Financial Statement Analysis"
topic_code: "03"
topic_slug: "03-Financial-Statement-Analysis"
volume: 3
lm: 4
title: "Analysis of Financial Institutions"
pages: "201-283"
weight_band: "10-15%"
difficulty: 3
los_count: 6
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/financial-statement-analysis]
---

# LM4: Analysis of Financial Institutions

Difficulty 3 of 5: the arithmetic is simple division, but the module carries a very large vocabulary (three capital tiers, two Basel liquidity ratios, three loan-loss ratios, five insurance ratios) and the exam scores you on picking the right numerator, the right denominator, and the right direction of "better", so definitional precision under time pressure is the whole game.

## LOS map

- **describe** how financial institutions differ from other companies (V3 p.201) ^los-03-04-a
    - Examiner asks: two statements about banks, one about systemic importance and one claiming bank assets are mostly deposits, and you must spot that deposits are liabilities while assets are loans and securities.
- **describe** key aspects of financial regulations of financial institutions (V3 p.201) ^los-03-04-b
    - Examiner asks: a quoted description of a Basel III requirement (capital, 30-day liquidity, or one-year stable funding) and you must name which of the three it is, or rank industries by global systemic risk.
- **explain** the CAMELS (capital adequacy, asset quality, management, earnings, liquidity, and sensitivity) approach to analyzing a bank, including key ratios and its limitations (V3 p.208) ^los-03-04-c
    - Examiner asks: which attribute CAMELS fails to address (competitive environment, government support, culture, off-balance-sheet items), or which component a given ratio belongs to.
- **analyze** a bank based on financial statements and other factors (V3 p.208) ^los-03-04-d
    - Examiner asks: an exhibit of capital by tier and RWA, or of loan-loss data, from which you compute three years of ratios and conclude "improving", "declining", or "mixed".
- **describe** other factors to consider in analyzing a bank (V3 p.226) ^los-03-04-e
    - Examiner asks: which supplementary fact (falling benefit obligation, high equity compensation, fierce competition) is favourable or unfavourable, and why freestanding credit derivatives raise earnings volatility.
- **describe** key ratios and other factors to consider in analyzing an insurance company (V3 p.252) ^los-03-04-f
    - Examiner asks: compute or rank combined ratios, interpret a fall in the loss and loss adjustment expense ratio, and contrast P&C against L&H on claim predictability, policy duration, capital requirements, and interest rate sensitivity.

## Core intuition

A bank is not a factory with a different product; it is a balance sheet whose assets are other people's promises and whose liabilities are other people's deposits.
That single fact drives everything in this module: why banks are regulated so heavily, why an analyst starts with capital rather than with earnings, and why the ratios that matter are ratios of one kind of promise to another.

> [!abstract] Idea 1: systemic importance plus financial assets explain both the regulation and the analytical toolkit
> Banks are intermediaries whose inter-linkages spread one failure to households, corporates, other banks, and governments, and their assets are loans and securities measured close to fair value, so regulators police capital, liquidity, and asset riskiness, and the analyst borrows the regulators' framework (V3 p.202, p.203).

Start with why a bank failure is different from a retailer failure.
A bank accepts deposits and lends them out, so it sits at the centre of a network that links every type of entity in the economy (V3 p.202).
If one bank cannot honour deposits, the shock travels along those links; the curriculum calls this financial contagion, and the possibility that the whole system fails because a major institution fails is systemic risk (V3 p.202).
Even the expectation that a bank might not pay can trigger a bank run, which is why deposits are insured up to a limit by governments (V3 p.202, p.203).
Because of this, regulators constrain the amount of capital a bank must hold, its minimum liquidity, and the riskiness of its assets (V3 p.202).

The second difference is the nature of the assets.
A manufacturer owns plant and inventory; a bank owns loans and securities, and those financial assets carry credit risk, liquidity risk, market risk, and interest rate risk directly, and they are often carried at fair value (V3 p.203).
Practice Problem 1 tests exactly this: the tempting wrong statement says bank assets are mostly deposits, but deposits are over 80% of liabilities, not assets (V3 p.202, p.278).

Insurance companies are the other institution in scope.
Their systemic footprint is smaller because a smaller share of their business crosses borders and because foreign branches must hold assets locally against local policy liabilities; the exception is reinsurance, which is largely international and links insurers around the world (V3 p.205).
That is the logic behind Practice Problem 8: global commercial banks have the most cross-border business and the highest global systemic risk, credit unions (member-owned, non-profit, local) the least (V3 p.204, p.279).

Regulation is layered.
Global bodies harmonise standards and reduce regulatory arbitrage, but only national regulators have legal authority over a given institution (V3 p.205, p.208).
The Basel Committee on Banking Supervision, hosted by the Bank for International Settlements since 1974, wrote Basel III, whose three highlights you must be able to recognise from a one-sentence description (V3 p.205, p.207).
First, minimum capital: a bank must fund a minimum percentage of its risk-weighted assets with equity capital so that leverage cannot rise to the point where loan losses wipe it out (V3 p.207).
Second, minimum liquidity: enough high-quality liquid assets to survive a 30-day liquidity stress scenario (V3 p.207).
Third, stable funding: a minimum amount of stable funding relative to liquidity needs over a one-year horizon, where stability rises with deposit tenor and with retail rather than interbank sources (V3 p.207).
Other bodies to recognise by mission: the Financial Stability Board (identify and coordinate action on systemic risk), the International Association of Deposit Insurers, the International Association of Insurance Supervisors, and IOSCO for securities markets; the last two form the Joint Forum with the Basel Committee (V3 p.207, p.208).

> [!abstract] Idea 2: CAMELS is a regulator's rating grid, and every component pairs a discretionary number with a less discretionary one
> Each of Capital adequacy, Asset quality, Management, Earnings, Liquidity, and Sensitivity is rated 1 (best) to 5 (worst), the composite is examiner-weighted rather than a plain average, and the analytical trick throughout is to compare a management estimate (allowance, provision, fair value) to something harder to manipulate (charge-offs, non-accrual loans, RWA) (V3 p.209, p.238).

Capital adequacy asks how much of the bank's risk-adjusted assets is funded with loss-absorbing capital.
Assets are weighted by risk: cash 0%, corporate loans 100%, high-volatility commercial real estate and loans over 90 days past due above 100%, and off-balance-sheet exposures are weighted and included too (V3 p.209).
Capital is tiered: Common Equity Tier 1 (common stock, share premium, retained earnings, accumulated OCI, less intangibles and deferred tax assets) is the most loss-absorbing because it is permanent; Additional Tier 1 is subordinated, perpetual, fully discretionary-coupon instruments such as qualifying preferred stock; Tier 2 is subordinated to depositors and general creditors with at least five years' original maturity, plus limited portions of the loan-loss allowance (V3 p.210, p.232, p.233).
The Basel III floors are 4.5% CET1, 6.0% Tier 1, and 8.0% total capital, all as a percentage of RWA (V3 p.210).
The exam lesson from HSBC is that a ratio can rise because the numerator rises or because RWA falls; HSBC's ratios strengthened in 2016 even though CET1 capital fell, because RWA fell more (V3 p.211, p.212).
The lesson from Practice Problem 9 is that the three ratios can move in different directions: CET1 and Tier 1 improving while total capital declines means the bank is running down Tier 2, which is a mixed signal (V3 p.279, p.280).

Asset quality is about existing and potential credit risk and the strength of the processes that generate the assets (V3 p.212).
Loans are carried at amortised cost net of an allowance; securities are carried at amortised cost, FVOCI, or FVTPL under IFRS, and under US GAAP the three debt categories are held to maturity, trading, and available for sale, with all equity investments at fair value through net income (V3 p.212).
Composition matters first: what share of assets is highly liquid, what share is investments, and what share is loans, where loans include loans to banks, loans to customers, and reverse repos, which are collateralised loans (V3 p.212, p.213).
Credit quality matters second: the split of financial instruments by grade, and whether impairment allowances move in step with impaired assets (V3 p.215, p.216).
The allowance is discretionary, so the curriculum triangulates it against two harder facts: non-performing (non-accrual) loans, and net charge-offs, which are charge-offs less recoveries (V3 p.238).
Three ratios follow: allowance to non-performing loans, allowance to net charge-offs, and provision to net charge-offs (V3 p.238).
A rising allowance-to-non-accrual ratio means reserves are being built ahead of trouble; a provision-to-charge-off ratio below one means the bank is expensing less than it is actually losing, so the allowance is being drained and a catch-up may be coming (V3 p.239, p.240).
For securities, the tell is the age of unrealised losses: losses older than twelve months rarely reverse and hint at unrecognised other-than-temporary impairment, especially in held-to-maturity holdings whose fair value is hidden by amortised-cost accounting (V3 p.236, p.237).

Management capability can only be observed circumstantially from outside: board independence, separate CEO and chair, a risk committee that actually meets, an unqualified opinion on internal controls, and, ultimately, the bank's performance (V3 p.216, p.217, p.240, p.241).

Earnings should be high quality, meaning unbiased estimates and sustainable sources (V3 p.217).
The two big estimates are loan impairment allowances and Level 3 fair values, where inputs are unobservable model assumptions; Level 1 is quoted prices for identical instruments, Level 2 is observable inputs such as similar-instrument prices or yield curves (V3 p.217, p.218).
Composition is the other half: net interest income and fee income are sustainable, trading income is volatile, and a rising trading share is a quality warning (V3 p.218, p.242).
Net interest income itself comes from maturity transformation, borrowing short and lending long, which earns the curve's slope in normal times and loses when the curve inverts or short funding markets seize (V3 p.242, p.243).
The Citigroup case adds a subtle earnings-quality test: over five years the decline in credit-loss provisions explained 84% of the growth in pretax income, meaning very little profit growth came from the business itself (V3 p.241, p.242).

> [!abstract] Idea 3: LCR is a 30-day survival ratio, NSFR is a one-year funding-structure ratio, and both must exceed 100%
> LCR divides high-quality liquid assets by stressed 30-day net cash outflows; NSFR divides available stable funding (capital and liabilities weighted by stability factors) by required stable funding (assets weighted by how long they need funding); the LCR is about surviving a run, the NSFR is about not funding mortgages with overnight money (V3 p.220, p.221, p.247, p.248).

Liquidity matters more for a bank than for any other company because its current liabilities are deposits (V3 p.220).
The Basel III liquidity standards were a direct response to 2008, when banks with adequate capital still failed for lack of cash (V3 p.220).
The LCR numerator is unencumbered HQLA, cash or assets convertible to cash at little loss; the denominator is expected net outflows over a 30-day stress, computed by applying outflow factors to liabilities, netting inflows from assets maturing within 30 days, and adding a maturity-mismatch add-on (V3 p.220, p.222, p.247).
An LCR of 121% means the bank could withstand outflows 21% above the stress assumption, or equivalently survive 36.3 days of stress-level outflows (V3 p.247).
The NSFR weights funding sources by ASF factor: 100% for regulatory capital and liabilities of a year or more, 95% for stable retail and small-business deposits under a year, 90% for less stable retail deposits, 50% for non-financial corporate, operational, sovereign, and six-to-twelve-month wholesale funding, and 0% for everything else including short interbank funding and trade-date payables (V3 p.221).
Required stable funding is driven by asset composition and maturity: long-dated loans need stable funding, HQLA do not, and highly liquid assets do not enter the calculation at all (V3 p.221, p.248).
Two monitoring metrics round out liquidity: concentration of funding (dependence on one source) and contractual maturity mismatch, which is the same maturity transformation that generates net interest income (V3 p.221).
Practice Problem 20 is the classic link: a 30-day reverse repo is a highly liquid asset, so it moves the LCR, not the NSFR (V3 p.283).

Sensitivity to market risk covers interest rates, exchange rates, equity, and commodity prices, on and off balance sheet (V3 p.224).
Even a bank with perfectly matched asset and liability terms gains net interest income when rates rise, simply because it has more assets than liabilities; in practice the sign depends on repricing frequency, and a bank whose assets reprice faster is helped by rising rates (V3 p.224, p.225).
A sensitivity table is static: it assumes today's balance sheet structure persists and ignores management response, which is why central-bank rate cuts after 2008 did not hurt banks the way a static table would predict (V3 p.225).
VaR is the other disclosure: a one-day, 99% confidence loss estimate that is good for tracking a single bank's risk appetite over time but poor for comparing banks because assumptions differ (V3 p.225, p.249).

CAMELS is neither comprehensive nor integrated, and the order of the letters does not rank importance; capital and liquidity carry equal weight in Basel III (V3 p.226).
Bank-specific gaps are government support (size, health of the national system, SIFI status, government ownership), the bank's mission (community bank exposed to one industry versus diversified global bank), and corporate culture, judged from narrow-focus losses, restatements, above-average equity compensation that incentivises risk-taking, and slow loss provisioning followed by big write-downs (V3 p.226, p.227, p.228).
Generic gaps are competitive environment, off-balance-sheet items (unconsolidated VIEs, benefit plans, assets under management), segment information, currency exposure, risk factor disclosures, and Basel III Pillar 3 disclosures (V3 p.228, p.229, p.230).
Derivative accounting is the sleeper here: a derivative that qualifies as a cash-flow or net-investment hedge runs through OCI, but a freestanding derivative or fair-value hedge is marked through earnings every period, which creates volatility and can force extra collateral (V3 p.246, p.247).

Insurers earn premiums and invest the float, the premium collected but not yet paid out (V3 p.252, p.253).
P&C policies are short, claims are lumpy and unpredictable (accidents, weather), so P&C insurers hold high capital and invest conservatively in liquid fixed income (V3 p.252, p.258).
L&H policies are long, claims track stable mortality tables, so L&H insurers can hold less capital and reach for higher-return assets, but their risk-based capital must incorporate interest rate risk because long-duration products create material rate exposure (V3 p.252, p.266, p.268).
The P&C business is cyclical: a low industry combined ratio signals a hard market that attracts entrants who cut prices, premiums earned fall, the combined ratio rises into a soft market, and competitors exit (V3 p.254).
The combined ratio is the sum of the loss and loss adjustment expense ratio (over premiums earned, measuring underwriting judgment) and the underwriting expense ratio (over premiums written, measuring acquisition efficiency); below 100% is an underwriting profit (V3 p.254, p.255, p.257).
Loss reserves are the critical estimate: too optimistic and pricing is inadequate, and the longer the tail (asbestos), the harder the estimate (V3 p.255).
Downward revisions of prior-year reserves flow straight to pretax income, so they can signal either conservative initial reserving or earnings management (V3 p.256, p.257).
For both insurer types the analysis covers business profile, earnings, investment returns (income over invested assets, with and without unrealised gains), liquidity (fair value hierarchy as a liquidity proxy, no current ratio for L&H), and capitalisation (no global standard yet, Solvency II in the EU, NAIC risk-based capital in the US) (V3 p.253, p.259, p.261, p.268).

## Formulas and derivations

**Risk-weighted assets** (V3 p.209)
$$
RWA = \sum_{i} \text{Exposure}_i \times w_i
$$
^f-03-04-1

- $w_i$: regulator-set risk weight; cash 0%, corporate loans 100%, high-volatility commercial real estate and loans over 90 days past due above 100%, for example 150% (V3 p.209).
- Off-balance-sheet exposures are weighted and included (V3 p.209).
- Curriculum example: $10 \times 0\% + 1{,}000 \times 100\% + 10 \times 150\% = 1{,}015$ (V3 p.209).

**Common Equity Tier 1 ratio** (V3 p.210, p.279)
$$
\text{CET1 ratio} = \frac{\text{Common Equity Tier 1 Capital}}{RWA}
$$
^f-03-04-2

- CET1 capital: common stock, issuance surplus, retained earnings, accumulated OCI, less intangibles and deferred tax assets and other regulatory deductions (V3 p.210, p.231).
- Basel III minimum 4.5% (V3 p.210).
- Most loss-absorbing tier because it is permanent and puts shareholders' funds first in line (V3 p.210).

**Tier 1 capital ratio** (V3 p.210, p.279)
$$
\text{Tier 1 ratio} = \frac{\text{CET1 Capital} + \text{Additional Tier 1 Capital}}{RWA}
$$
^f-03-04-3

- Additional Tier 1: subordinated to deposits and debt, no fixed maturity, coupons fully at the bank's discretion; qualifying perpetual preferred stock is the typical instrument (V3 p.210, p.232).
- Basel III minimum 6.0% (V3 p.210).

**Total capital ratio** (V3 p.210, p.279)
$$
\text{Total capital ratio} = \frac{\text{Tier 1 Capital} + \text{Tier 2 Capital}}{RWA}
$$
^f-03-04-4

- Tier 2: subordinated to depositors and general creditors, original maturity at least five years, plus limited portions of the loan-loss allowance and excess eligible credit reserves over expected losses (V3 p.210, p.233).
- Basel III minimum 8.0% (V3 p.210).
- Derived check: Tier 2 capital equals total regulatory capital less CET1 less Additional Tier 1, which is how you back out Tier 2 from a disclosure that omits it.

**Basel III minimum capital requirements** (V3 p.210)
$$
\text{CET1} \geq 4.5\%\,RWA, \qquad \text{Tier 1} \geq 6.0\%\,RWA, \qquad \text{Total} \geq 8.0\%\,RWA
$$
^f-03-04-5

- Global floors; national regulators set the binding requirements for their own institutions and may add buffers (V3 p.210).
- Basel III also adds a capital conservation buffer and counter-cyclical buffers on top (V3 p.210).

**Pillar 1 capital charge** (V3 p.211)
$$
\text{Capital required} = 8\% \times RWA
$$
^f-03-04-6

- HSBC: $857.2\text{bn} \times 8\% = 68.6\text{bn}$ (V3 p.211).
- Follows directly from the 8% total capital floor in Formula 5.

**Liquidity Coverage Ratio** (V3 p.220, p.247)
$$
LCR = \frac{\text{High-quality liquid assets}}{\text{Expected net cash outflows over 30-day stress}} \geq 100\%
$$
^f-03-04-7

- Numerator: unencumbered assets convertible to cash at little or no loss (V3 p.222).
- Denominator: prescribed outflow factors applied to liabilities, less inflows from assets maturing within 30 days, plus a maturity-mismatch add-on (V3 p.247).
- Below 100% signals an inability to meet stressed liquidity needs (V3 p.247).

> [!tip] Calculator
> Citigroup 2016: `403.7 ÷ 332.5 =` gives 1.214, so 121%.
> Excess HQLA: `403.7 - 332.5 =` gives 71.2.

**Stress survival days implied by LCR** (V3 p.247)
$$
\text{Days covered} = LCR \times 30
$$
^f-03-04-8

- Citigroup: $1.21 \times 30 = 36.3$ days of stress-level outflows (V3 p.247).
- Equivalent statement: the bank can withstand outflows $LCR - 100\%$ above the stress assumption.

**Net Stable Funding Ratio** (V3 p.220, p.248)
$$
NSFR = \frac{\text{Available stable funding}}{\text{Required stable funding}} > 100\%
$$
^f-03-04-9

- Available stable funding: capital and liabilities weighted by ASF factor (Formula 10) (V3 p.220).
- Required stable funding: assets weighted by how much stable funding they need; long-dated loans high, HQLA nil (V3 p.221, p.248).
- Described as an inverted LCR: it measures one-year funding structure, not 30-day survival (V3 p.248).

**Available stable funding** (V3 p.220, p.221)
$$
ASF = \sum_{k} \text{Amount}_k \times \text{ASF factor}_k
$$
^f-03-04-10

- Factors: 100% regulatory capital (excluding Tier 2 under one year) and liabilities of one year or more; 95% stable retail and small-business deposits under one year; 90% less stable retail deposits; 50% non-financial corporate, operational, sovereign, and other six-to-twelve-month funding; 0% other liabilities, net derivative liabilities, trade-date payables (V3 p.221).
- Reason: retail deposits stay through stress, interbank money leaves overnight, so the weights encode empirical stickiness (V3 p.207, p.221).

**Net charge-offs** (V3 p.238, p.239)
$$
\text{Net charge-offs} = \text{Charge-offs} - \text{Recoveries}
$$
^f-03-04-11

- Less discretionary than the allowance because a charge-off is a confirmed loss, but it is a lagging indicator and recoveries can be timed to smooth earnings (V3 p.238).
- Citigroup consumer 2016: $7{,}644 - 1{,}594 = 6{,}050$ (V3 p.239).

**Allowance roll-forward** (V3 p.238)
$$
\text{Allowance}_{end} = \text{Allowance}_{begin} + \text{Provision} - \text{Net charge-offs}
$$
^f-03-04-12

- The allowance is a contra-asset to loans; the provision is the income-statement expense that builds it; net charge-offs draw it down (V3 p.238).
- Consequence: provision below net charge-offs means the allowance is shrinking, which is the mechanism behind Formula 15.
- Underestimating the allowance overstates both assets and net income (V3 p.238).

**Allowance to non-performing loans** (V3 p.238)
$$
\frac{\text{Allowance for loan losses}}{\text{Non-performing (non-accrual) loans}}
$$
^f-03-04-13

- Non-accrual loans are not paying contractual amounts, an objective measure (V3 p.238).
- Rising ratio means reserves are being built ahead of loans going bad, a positive sign; falling toward one means a thin cushion (V3 p.239).

**Allowance to net charge-offs** (V3 p.238)
$$
\frac{\text{Allowance for loan losses}}{\text{Net loan charge-offs}}
$$
^f-03-04-14

- Years of current charge-off experience the allowance could absorb (V3 p.239).
- Citigroup corporate fell from 11.44 to 5.29, still ample but the lowest in five years (V3 p.239, p.240).

**Provision to net charge-offs** (V3 p.238)
$$
\frac{\text{Provision for loan losses}}{\text{Net loan charge-offs}}
$$
^f-03-04-15

- Provision should correlate with net charge-offs; a ratio persistently below 1.0 means provisioning trails actual losses and a catch-up adjustment may follow (V3 p.240).
- Rising ratio is read as more conservative provisioning (V3 p.240, p.282).

**Impairment allowance coverage of impaired assets** (V3 p.216)
$$
\text{Coverage} = \frac{\text{Impairment allowances}}{\text{Impaired assets}}
$$
^f-03-04-16

- HSBC: $11{,}027/28{,}058 = 39.3\%$ in 2015 and $8{,}100/20{,}510 = 39.5\%$ in 2016, so a 26.5% fall in allowances matched a 26.9% fall in impaired assets (V3 p.216).
- The test is whether allowances move in proportion to the objective measure they are meant to cover.

**Liquid assets to total assets** (V3 p.214)
$$
\text{Balance-sheet liquidity} = \frac{\text{Cash and most liquid items}}{\text{Total assets}}
$$
^f-03-04-17

- HSBC's most liquid items: cash and central bank balances, items in course of collection, Hong Kong government certificates of indebtedness (V3 p.213).
- Companion common-size ratios: investments to total assets and loans (to banks, to customers, plus reverse repos) to total assets (V3 p.214).

**Net interest revenue** (V3 p.242)
$$
\text{Net interest revenue} = \text{Interest earned on interest-bearing assets} - \text{Interest paid on interest-bearing liabilities}
$$
^f-03-04-18

- Created by maturity transformation: borrow short, lend long (V3 p.242).
- Citigroup 2016: $58{,}077 - 12{,}511 = 45{,}566$ (V3 p.243, p.245).

**Net interest margin** (V3 p.245)
$$
NIM = \frac{\text{Net interest revenue}}{\text{Average interest-earning assets}}
$$
^f-03-04-19

- Citigroup 2016: $45{,}566/1{,}594{,}086 = 2.86\%$, down from 2.93% (V3 p.245).
- Average-balance analysis explains the past; end-of-period balances and rates are a better base for projecting (V3 p.246).
- An unexpected inversion of the yield curve raises short funding costs and compresses NIM (V3 p.243, p.283).

**Composite CAMELS rating** (V3 p.251, p.252)
$$
\text{Composite} = \frac{\sum_{c} w_c \times \text{Rating}_c}{\sum_{c} w_c}
$$
^f-03-04-20

- Ratings run 1 (best) to 5 (worst); unweighted, the sum runs 6 to 30 and dividing by 6 gives the arithmetic mean (V3 p.209, p.251).
- Weights are analyst-chosen: an equity analyst doubling asset quality and earnings turned Citigroup's 1.75 into 2.00 (V3 p.252).
- If every component has the same rating the weights are irrelevant (V3 p.251).

> [!tip] Calculator
> Unweighted: `1 + 2.5 + 2 + 3 + 1 + 1 = ÷ 6 =` gives 1.75.
> Weighted: `1 + 5 + 2 + 6 + 1 + 1 = ÷ 8 =` gives 2.00.

**VaR relative to earnings and capital** (V3 p.250)
$$
\frac{\text{Total trading and credit portfolio VaR}}{\text{Net income from continuing operations}}, \qquad \frac{\text{VaR}}{\text{Common equity}}
$$
^f-03-04-21

- Citigroup: $105/15{,}033 = 0.7\%$ of net income and $105/205{,}867 = 0.1\%$ of equity at year-end 2016 (V3 p.250).
- VaR is a one-day, 99% measure; useful for intra-company trends, not for cross-company comparison (V3 p.249).

**Trading revenue per unit of risk** (V3 p.283)
$$
\text{Reward to risk} = \frac{\text{Annual trading revenue}}{\text{Average daily trading VaR}}
$$
^f-03-04-22

- Practice Problem 17: N-bank improved from $134\times$ to $160\times$, T-bank flat at $80\times$ (V3 p.276, p.283).
- Higher is better; it is a trend measure within one bank for the same reason VaR itself is.

**Statutory underwriting losses** (V3 p.254)
$$
\text{Losses} = \text{Claims paid} + \left(\text{Ending loss reserves} - \text{Beginning loss reserves}\right)
$$
^f-03-04-23

- The reserve change converts cash claims into accrual losses; a reserve release (downward revision) lowers losses and lifts pretax income (V3 p.254, p.256).

**Loss and loss adjustment expense ratio** (V3 p.257)
$$
\text{Loss and LAE ratio} = \frac{\text{Loss expense} + \text{Loss adjustment expense}}{\text{Net premiums earned}}
$$
^f-03-04-24

- Measures the success of underwriting in estimating the risks insured; lower is better (V3 p.257).
- Denominator is premiums earned, the portion of written premiums recognised over the coverage period (V3 p.257).

**Underwriting expense ratio** (V3 p.257)
$$
\text{Underwriting expense ratio} = \frac{\text{Underwriting expense}}{\text{Net premiums written}}
$$
^f-03-04-25

- Measures the efficiency of money spent obtaining new premiums (commissions, sales staff); lower is better (V3 p.255, p.257).
- Denominator is premiums written, not earned, under statutory practice; Travelers reports a modified version over earned premiums (V3 p.255).

**Combined ratio** (V3 p.257)
$$
\text{Combined ratio} = \text{Loss and LAE ratio} + \text{Underwriting expense ratio}
$$
^f-03-04-26

- Below 100% is an underwriting profit and an efficient operation; above 100% is an underwriting loss (V3 p.254, p.257).
- Because the two components have different denominators, the combined ratio is a sum of ratios, not a single fraction (V3 p.257).

> [!tip] Calculator
> Hartford: `11351 ÷ 13811 =` gives 0.822; `5156 ÷ 10568 =` gives 0.488; `0.822 + 0.488 =` gives 1.310, an underwriting loss.

**Dividends to policyholders (shareholders) ratio** (V3 p.257)
$$
\text{Dividend ratio} = \frac{\text{Dividends to policyholders (shareholders)}}{\text{Net premiums earned}}
$$
^f-03-04-27

- A liquidity measure: cash out as dividends relative to premiums earned in the same period (V3 p.257).

**Combined ratio after dividends** (V3 p.257)
$$
\text{Combined ratio after dividends} = \text{Combined ratio} + \text{Dividend ratio}
$$
^f-03-04-28

- Stricter efficiency test that counts discretionary cash paid to policyholders or shareholders (V3 p.257).
- CNA: $116.0\% + 11.7\% = 127.7\%$ (V3 p.258).

**Reinsurance ceded share of reserves** (V3 p.256)
$$
\text{Ceded share} = \frac{\text{Reinsurance recoverables on unpaid losses}}{\text{Gross claims and claim adjustment expense reserves}}
$$
^f-03-04-29

- Travelers ceded 16.7% to 17.6% of gross loss reserves across 2014 to 2016 (V3 p.256).
- Ceding transfers risk to a reinsurer for a premium; the ceding company expects to recover losses from the reinsurer (V3 p.256).

**Investment return on invested assets** (V3 p.259, p.266, p.267)
$$
\text{Investment return} = \frac{\text{Investment income (with or without unrealised gains)}}{\text{Average invested assets (cash and investments)}}
$$
^f-03-04-30

- Computed two ways, with and without unrealised capital gains, to show how much of the return is unrealised (V3 p.259, p.266).
- AIA fixed income: $(5{,}290 + 127)/116{,}265.5 = 4.7\%$ using average loans, deposits, and debt securities (V3 p.267).
- L&H interest rate risk is judged separately by comparing asset and liability duration (V3 p.266).

## Worked examples

### Example 1: HSBC capital position (V3 p.210 to p.212)

Setup: CET1 116,552 (2016) and 130,863 (2015); Additional Tier 1 21,470 and 22,440; Tier 2 34,336 and 36,530; total regulatory capital 172,358 and 189,833; RWA 857,181 and 1,102,995, all in $m.

Part 1: did the ratios strengthen or weaken?
2016 CET1 $= 116{,}552/857{,}181 = 13.6\%$ versus $130{,}863/1{,}102{,}995 = 11.9\%$.
2016 Tier 1 $= (116{,}552 + 21{,}470)/857{,}181 = 138{,}022/857{,}181 = 16.1\%$ versus $153{,}303/1{,}102{,}995 = 13.9\%$.
2016 total $= 172{,}358/857{,}181 = 20.1\%$ versus $189{,}833/1{,}102{,}995 = 17.2\%$.
All three strengthened (V3 p.211).
Python: `0.13597, 0.16102, 0.20108; 0.11864, 0.13899, 0.17211`.

Part 2: primary reason?
CET1 capital actually fell 10.9% ($116{,}552/130{,}863 - 1$), so the numerator cannot explain the improvement.
RWA fell 22.3% ($857{,}181/1{,}102{,}995 - 1$), and that denominator shrinkage is the primary reason (V3 p.212).
Cross-check on the RWA table: credit 655.7 + counterparty 62.0 + market 41.5 + operational 98.0 = 857.2bn, and the Pillar 1 charge is $857.2 \times 8\% = 68.6$bn (V3 p.211).
Python: `-0.1094, -0.2229, 68.58`. ^ex-03-04-1

### Example 2: HSBC asset composition (V3 p.213 to p.214)

Setup: total assets 2,374,986 (2016) and 2,409,656 (2015), $m.

Part 1: most liquid assets (cash and central bank balances, items in course of collection, Hong Kong certificates of indebtedness).
2015: $(98{,}934 + 5{,}768 + 28{,}410)/2{,}409{,}656 = 133{,}112/2{,}409{,}656 = 5.5\%$.
2016: $(128{,}009 + 5{,}003 + 31{,}228)/2{,}374{,}986 = 164{,}240/2{,}374{,}986 = 6.9\%$.
Balance-sheet liquidity increased (V3 p.214).
Python: `0.05524, 0.06915`.

Part 2: investments (trading assets, financial assets designated at fair value, financial investments).
2015: $(224{,}837 + 23{,}852 + 428{,}955)/2{,}409{,}656 = 677{,}644/2{,}409{,}656 = 28.1\%$.
2016: $(235{,}125 + 24{,}756 + 436{,}797)/2{,}374{,}986 = 696{,}678/2{,}374{,}986 = 29.3\%$.
The investment share rose (V3 p.214).
Python: `0.28122, 0.29334`.

Part 3: loans (to banks, to customers, plus non-trading reverse repos).
2015: $(90{,}401 + 924{,}454 + 146{,}255)/2{,}409{,}656 = 1{,}161{,}110/2{,}409{,}656 = 48.2\%$.
2016: $(88{,}126 + 861{,}504 + 160{,}974)/2{,}374{,}986 = 1{,}110{,}604/2{,}374{,}986 = 46.8\%$.
The loan share fell (V3 p.214).
Python: `0.48186, 0.46763`.
Note the classification logic: reverse repos are collateralised loans the bank has made, so they count as loans; assets held for sale are disposal-group long-term assets and are not the same as available-for-sale securities (V3 p.212, p.213). ^ex-03-04-2

### Example 3: HSBC credit quality (V3 p.215 to p.216)

Setup: gross financial instruments 2,212,851 (2016) and 2,245,436 (2015); strong quality 1,579,517 and 1,553,830; impaired 20,510 and 28,058; impairment allowances 8,100 and 11,027, $m.

Part 1: did credit quality improve?
Strong share 2015 $= 1{,}553{,}830/2{,}245{,}436 = 69.2\%$; 2016 $= 1{,}579{,}517/2{,}212{,}851 = 71.4\%$.
The strong-quality share rose 2.2 points while the gross total fell 1.5%, so quality improved (V3 p.216).
Python: `0.69200, 0.71379, -0.01451`.

Part 2: do allowances track impaired assets?
Allowances fell $8{,}100/11{,}027 - 1 = -26.5\%$; impaired assets fell $20{,}510/28{,}058 - 1 = -26.9\%$.
Coverage $= 11{,}027/28{,}058 = 39.3\%$ in 2015 and $8{,}100/20{,}510 = 39.5\%$ in 2016, essentially constant, so yes, the allowance change reflects the change in impaired assets (V3 p.216).
Python: `-0.26544, -0.26901, 0.39301, 0.39493`.
Other lines for the common-size habit: good quality 14.2% (2016) from 14.7%, satisfactory 11.9% from 13.1%, past due not impaired 0.4% from 0.6% (a 30.7% dollar fall), impaired 0.9% from 1.2% (V3 p.216). ^ex-03-04-3

### Example 4: HSBC composition of earnings (V3 p.218 to p.220)

Setup: 2016 total operating income 59,836; net interest income 29,813; net fee income 12,777; net trading income 9,452, $m.

Part 1: primary source and share.
Net interest income $= 29{,}813/59{,}836 = 49.8\%$, the largest source (V3 p.219).
Python: `0.49824`.

Part 2: trading share.
$9{,}452/59{,}836 = 15.8\%$ (V3 p.219).
Python: `0.15797`.

Part 3: trend.
Total operating income fell every year from 82,545 (2012) to 59,836 (2016).
From 2012 to 2015 the mix was stable at roughly 46% net interest and 21% fees; in 2016 the net interest share jumped to 49.8% and trading rose to 15.8% from 12.3%, while income from instruments designated at fair value swung to $-4.5\%$ (V3 p.219).
Python: 2015 NII share `32531/71092 = 0.4576`, 2012 NII share `37672/82545 = 0.4564`, 2016 fee share `0.2135`.
Quality reading: the rising trading share and the volatile fair-value line reduce sustainability even though the largest source remains net interest income (V3 p.218). ^ex-03-04-4

### Example 5: HSBC liquidity disclosures (V3 p.222 to p.224)

Setup: group EC LCR 136% at end 2016 (116% in 2015); entity LCRs and NSFRs for 2016 include UK 123/116, Hong Kong branch 185/157, Singapore 154/112, USA 130/120, France 122/120, Hang Seng 218/162, Canada 142/139, China 253/49.

Part 1: highest liquid assets relative to stressed needs?
HSBC Bank China, LCR 253%, the highest in the table (V3 p.223).

Part 2: most stable funding relative to required stable funding?
Hang Seng Bank, NSFR 162%, the highest (V3 p.223).

Part 3: furthest from the Basel III NSFR target of more than 100%?
HSBC Bank China at 49%, the only entity below 100%; the curriculum suggests RMB capital controls or jurisdictional issues but says the example cannot confirm the cause (V3 p.223, p.224).
Note the two ratios can diverge sharply for one entity: China has the best short-term liquidity and the worst long-term funding structure, which is exactly why Basel III has two standards (V3 p.220). ^ex-03-04-5

### Example 6: HSBC market risk sensitivity (V3 p.224 to p.225)

Setup: four quarterly parallel shocks of 25 bp; +25 bp raises 2016 NII by 1,709; $-25$ bp lowers it by 2,406, $m.

Part 1: decrease under the downward shift?
$2{,}406$ million (V3 p.225).
The asymmetry ($+1{,}709$ versus $-2{,}406$) is itself informative: HSBC expects its assets to reprice faster and further than its liabilities, so it is asset-sensitive, and falling rates hurt more than rising rates help (V3 p.225).

Part 2: why did central banks cut rates if cuts hurt banks?
The sensitivity table is static and assumes the balance sheet structure does not change; after the crisis, banks' borrowing costs fell to near zero while loan rates stayed far higher, and the cuts were aimed at economy-wide liquidity and stimulus, not bank earnings (V3 p.225).
Related: VaR is the other tool, computed at 99% confidence over one day using two years of price history (V3 p.225). ^ex-03-04-6

### Example 7: Aegon versus MetLife revenue diversification (V3 p.262 to p.264)

Setup: Aegon 2016 (EUR m) premiums 23,453, investment income 7,788, fees 2,414, total 33,655; MetLife 2016 ($m) premiums 39,153, investment income 13,358, policy fees and other 10,965, total 63,476.

Part 1: compare 2016 diversification.
Aegon premium share $= 23{,}453/33{,}655 = 69.7\%$; MetLife $= 39{,}153/63{,}476 = 61.7\%$.
MetLife appears more diversified (about 62% from premiums versus nearly 70%), with the caveat that premiums are the more stable source, so diversification is bought with potentially more variable revenue (V3 p.264).
Python: `0.69687, 0.61682`; Aegon investment share `0.2314`, MetLife `0.2104`.

Part 2: trends.
Both companies' premium shares are higher in 2016 than in any of the prior four years (Aegon 65.0% in 2012, MetLife 55.7% in 2012).
Aegon: premium income grew 15.4% in 2015 ($22{,}925/19{,}864 - 1$) and investment income fell 8.6% in 2016 ($7{,}788/8{,}525 - 1$).
MetLife: investment income fell 10.6% in 2015 ($19{,}916/22{,}273 - 1$) and 32.9% in 2016 ($13{,}358/19{,}916 - 1$), which mechanically raised the premium share (V3 p.264).
Python: `0.15410, -0.08645, -0.10582, -0.32928`. ^ex-03-04-7

### Example 8: AIA investment portfolio (V3 p.266 to p.267)

Setup: loans and deposits 7,062 (2016) and 7,211 (2015); debt securities 113,618 and 104,640; equities 30,211 and 27,159; total 154,908 and 142,742, US$m; 2016 interest income 5,290, dividends 654, rental 140, gains 1,471 of which 127 on debt.

Part 1: allocation and change.
Debt securities are 73.3% in both years; loans and deposits slipped from 5.1% to 4.6% and equities rose from 19.0% to 19.5%, a very small shift from loans and deposits toward equities (V3 p.267).
Python: `0.7335, 0.0456, 0.0505, 0.1950, 0.1903`.

Part 2: return on average fixed-income assets.
Fixed-income income $= 5{,}290 + 127 = 5{,}417$.
Average fixed-income assets $= [(7{,}062 + 113{,}618) + (7{,}211 + 104{,}640)]/2 = 232{,}531/2 = 116{,}265.5$.
Return $= 5{,}417/116{,}265.5 = 4.7\%$ (V3 p.267).
Python: `5417, 116265.5, 0.04659`.
Trap: the curriculum includes only the gains attributable to debt securities (127), not the full 1,471, and uses the average rather than the ending balance. ^ex-03-04-8

### Example 9: Citigroup capital ratios (V3 p.231 to p.233)

Setup: CET1 capital 167,378 (2016) and 173,862 (2015); Additional Tier 1 11,009 and 2,558; Tier 2 23,759 and 22,326; RWA 1,166,764 and 1,190,853, $m.

CET1 ratio $= 167{,}378/1{,}166{,}764 = 14.35\%$ (2015: $173{,}862/1{,}190{,}853 = 14.60\%$), a slight decline driven mostly by more deferred tax assets being disallowed (V3 p.231, p.232).
Tier 1 $= (167{,}378 + 11{,}009)/1{,}166{,}764 = 178{,}387/1{,}166{,}764 = 15.29\%$ (2015: 14.81%), improved because of additional qualifying perpetual preferred stock and fewer DTAs disallowed at the Tier 1 level (V3 p.232).
Total $= (178{,}387 + 23{,}759)/1{,}166{,}764 = 202{,}146/1{,}166{,}764 = 17.33\%$ (2015: 16.69%), improved through the Tier 1 rise and more qualifying subordinated debt (V3 p.233).
Python: `0.14346, 0.14600, 0.15289, 0.14815, 0.17325, 0.16689`.
All three far exceed the 4.5%, 6.0%, and 8.0% minimums, so a rating of 1 is justified (V3 p.233).
Reconciliation check on Additional Tier 1 for 2016: $19{,}069 + 1{,}371 + 17 + 24 - 343 - 8{,}535 - 533 - 61 = 11{,}009$ (V3 p.232); note that the "less" line of $(24)$ adds back because it is a negative deduction.
Python: `11009`. ^ex-03-04-9

### Example 10: Citigroup investment securities quality (V3 p.234 to p.237)

Setup: total assets 1,792,077; liquid assets 670,119; investments 353,304; loans net of unearned income 624,369; AFS amortised cost 300,269 and fair value 299,424; gross unrealised losses 2,566 of which 1,394 under twelve months and 1,172 twelve months or older; state and municipal losses 757 on cost 10,797, of which 702 are older than twelve months; HTM unrealised losses 457 of which 373 older than twelve months, $m.

Composition: liquid assets $670{,}119/1{,}792{,}077 = 37.4\%$ (largest group, up from 35.9%), investments 19.7% (unchanged), loans 34.9% (V3 p.234, p.235).
Python: `0.37393, 0.19715, 0.34841`.
AFS: fair value is below cost by $300{,}269 - 299{,}424 = 845$; the largest contributor is state and municipal at $757/10{,}797 = 7.0\%$ of cost, the only class with losses above 2% (V3 p.236).
Aging: $1{,}394/2{,}566 = 54\%$ of losses are under twelve months; of the 1,172 older losses, $702/1{,}172 = 60\%$ are municipals, raising concern that these will be realised (V3 p.236).
HTM: 457 of losses is 1.3% of cost and $373/457 = 82\%$ is older than twelve months, and because HTM is at amortised cost the classification hides fair value, so there may be unrecognised impairment (V3 p.237).
Python: `845, 0.07011, 0.5433, 0.5990, 0.8162`.
Reading: investment policy is fairly conservative, but the age of the losses suggests possible denial of impairment (V3 p.240). ^ex-03-04-10

### Example 11: Citigroup loan loss ratios (V3 p.238 to p.240)

Setup 2016: consumer allowance 9,358, provision 6,323, charge-offs 7,644, recoveries 1,594, non-accrual 3,158; corporate allowance 2,702, provision 426, charge-offs 578, recoveries 67, non-accrual 2,421, $m.

Net charge-offs: consumer $7{,}644 - 1{,}594 = 6{,}050$; corporate $578 - 67 = 511$ (V3 p.239).
Consumer: allowance to non-accrual $9{,}358/3{,}158 = 2.96$ (highest in five years, rising, allowance built ahead of trouble); allowance to net charge-offs $9{,}358/6{,}050 = 1.55$ (cushion stable around 1.4 to 1.65); provision to net charge-offs $6{,}323/6{,}050 = 1.05$, the first year above 1.0 in five, so provisioning has turned more conservative (V3 p.239, p.240).
Corporate: allowance to non-accrual $2{,}702/2{,}421 = 1.12$ (lowest in five years, declining three years running, a thin layer); allowance to net charge-offs $2{,}702/511 = 5.29$ (ample but down from 11.44); provision to net charge-offs $426/511 = 0.83$, below 1.0 in four of five years, so provisioning trails actual losses and 2015's 3.61 looks like a catch-up (V3 p.239, p.240).
Python: `6050, 511, 2.963, 1.547, 1.045, 1.116, 5.288, 0.834`.
Verdict: consumer loans well reserved, corporate less so, mixed asset quality, rating 2.5 (V3 p.240). ^ex-03-04-11

### Example 12: Citigroup earnings quality (V3 p.241 to p.242)

Setup: pretax income 21,477 (2016) versus 15,096 (2011); total provisions for credit losses 6,982 versus 12,359; 2013 pretax rose 11,637 while provisions fell 2,815; 2016 revenues 69,875 with net interest 45,104 and trading 7,585, $m.

Five-year change in pretax income $= 21{,}477 - 15{,}096 = 6{,}381$; five-year change in provisions $= 6{,}982 - 12{,}359 = -5{,}377$.
The provision decline explains $5{,}377/6{,}381 = 84\%$ of the pretax improvement, so almost no profit growth came from elsewhere (V3 p.241, p.242).
In 2013 the provision drop supplied $2{,}815/11{,}637 = 24\%$ of the increase (V3 p.241).
Python: `6381, -5377, 0.8427, 0.2419`.
Composition: trading is $7{,}585/69{,}875 = 10.9\%$ of revenue, up from 7.2% in 2012 and trending upward, the wrong direction for sustainability; net interest is 64.5%, improved from 61.1% but below 2012's 67.1% (V3 p.242).
Python: `0.10855, 0.07162, 0.64550`.
Verdict: earnings quality not exceedingly high, rating 3 (V3 p.246). ^ex-03-04-12

### Example 13: Citigroup net interest margin (V3 p.243 to p.246)

Setup 2016: interest revenue 58,077 on average interest-earning assets 1,594,086 (3.64%); interest expense 12,511 on average interest-bearing liabilities 1,212,602 (1.03%); US net interest revenue 27,929 on 859,311; non-US 17,637 on 734,775, $m.

Net interest revenue $= 58{,}077 - 12{,}511 = 45{,}566$.
NIM $= 45{,}566/1{,}594{,}086 = 2.86\%$, down from 2.93% in 2015 and 2.90% in 2014 (V3 p.245).
US NIM $= 27{,}929/859{,}311 = 3.25\%$ (up from 3.09%); non-US $= 17{,}637/734{,}775 = 2.40\%$ (down from 2.73%), declining since 2014 as the dollar strengthened and translation effects bit (V3 p.245, p.246).
Python: `45566, 0.02858, 0.03250, 0.02400, 0.02729`.
Drivers: the average rate earned slipped from 3.68% to 3.64% (OneMain disposal cut US loan yields from 7.08% to 6.72%) while funding cost rose in every liability category (V3 p.244, p.245).
Caveat the exam likes: average-balance analysis explains what happened but end-of-period balances are the better base for projection (V3 p.246). ^ex-03-04-13

### Example 14: Citigroup LCR and NSFR (V3 p.247 to p.248)

Setup: HQLA 403.7 and net outflows 332.5 at end 2016 (389.2 and 344.4 at end 2015); available stable funding 1,341.5 (deposits 929.4, long-term debt 206.2, common equity 205.9) against required stable funding 1,122.0, $bn.

LCR $= 403.7/332.5 = 121\%$ (2015: $389.2/344.4 = 113\%$), excess HQLA $403.7 - 332.5 = 71.2$.
Interpretation: outflows could run 21% above the stress case, or the bank survives $1.21 \times 30 = 36.3$ days at stress-level outflows (V3 p.247).
Python: `1.2141, 1.1301, 71.2, 36.3`.
NSFR (rough, unweighted) $= 1{,}341.5/1{,}122.0 = 120\%$ (2015: $1{,}314.3/1{,}109.5 = 118\%$), stable and comfortably above 100% (V3 p.248).
Python: `1.1956, 1.1846`.
Verdict: liquidity very good, rating 1 (V3 p.248).
Note the required-funding side lists investments, net loans, goodwill, intangibles, MSRs, and other assets but no liquid assets, because HQLA do not enter the NSFR (V3 p.248). ^ex-03-04-14

### Example 15: Citigroup VaR and capital sensitivity (V3 p.249 to p.251)

Setup: total trading and credit portfolio VaR 105 at end 2016 (average 92) versus 98 (average 117) in 2015; net income from continuing operations 15,033 (2016) and 17,386 (2015); common equity 205,867; capital ratio sensitivities 0.90 bp per $100m of capital and 1.20 bp per $1bn of RWA for CET1, $m.

Average trading VaR fell to 70 from 92 and average trading-plus-credit VaR to 92 from 117, mainly from interest rate hedging changes (V3 p.250).
Year-end VaR rose to 105 from 98, but $105/15{,}033 = 0.7\%$ of net income and $105/205{,}867 = 0.05\%$, rounded to 0.1%, of equity (V3 p.250).
Python: `0.00698, 0.00051`.
Covariance check: $83 + 32 + 13 + 27 - 70 = 85$ total trading VaR at year-end, so the diversification adjustment is large relative to the components (V3 p.249).
Capital sensitivity: $100/1{,}166{,}764 = 0.86$ bp per $100m of CET1 and $167{,}378/1{,}165{,}764 - 167{,}378/1{,}166{,}764 = 1.23$ bp per $1bn of RWA, consistent with the disclosed 0.90 and 1.20, and negligible against a 14.35% ratio (V3 p.251).
Python: `0.857 bp, 1.231 bp`.
Caveats: VaR is one-day and ignores lingering dislocations; sensitivities are static and change one factor at a time (V3 p.250, p.251).
Verdict: sensitivity controlled, rating 1 (V3 p.251). ^ex-03-04-15

### Example 16: Citigroup composite CAMELS score (V3 p.251 to p.252)

Setup: ratings C 1.0, A 2.5, M 2.0, E 3.0, L 1.0, S 1.0; an equity analyst weights asset quality and earnings at 2 and the others at 1.

Unweighted: $(1.0 + 2.5 + 2.0 + 3.0 + 1.0 + 1.0)/6 = 10.5/6 = 1.75$.
Weighted: $(1.0 \times 1 + 2.5 \times 2 + 2.0 \times 1 + 3.0 \times 2 + 1.0 \times 1 + 1.0 \times 1)/8 = 16.0/8 = 2.00$ (V3 p.252).
Python: `1.75, 2.00`.
The weighted score is worse because the analyst emphasises the two weakest components; a different analyst (a bondholder weighting capital and liquidity) would land below 1.75 (V3 p.230, p.252). ^ex-03-04-16

### Example 17: P&C underwriting ratios for five insurers (V3 p.257 to p.258)

Setup ($m): Travelers losses and LAE 15,070, premiums earned 24,534, underwriting expense 8,139, premiums written 24,958, dividends 757; Hartford 11,351, 13,811, 5,156, 10,568, 334; W. R. Berkley 3,846, 6,293, 2,396, 6,424, 184; CNA 5,270, 6,924, 2,787, 6,988, 813; Markel 2,051, 3,866, 1,437, 4,001, 0.

| Insurer | Loss and LAE | Underwriting expense | Combined | Dividend | After dividends |
|---|---|---|---|---|---|
| Travelers | $15{,}070/24{,}534 = 61.4\%$ | $8{,}139/24{,}958 = 32.6\%$ | 94.0% | $757/24{,}534 = 3.1\%$ | 97.1% |
| Hartford | $11{,}351/13{,}811 = 82.2\%$ | $5{,}156/10{,}568 = 48.8\%$ | 131.0% | 2.4% | 133.4% |
| W. R. Berkley | 61.1% | 37.3% | 98.4% | 2.9% | 101.3% |
| CNA | 76.1% | 39.9% | 116.0% | 11.7% | 127.7% |
| Markel | 53.1% | 35.9% | 89.0% | 0.0% | 89.0% |

Python: Travelers `0.6142, 0.3261, 0.9404, 0.0309, 0.9712`; Hartford `0.8219, 0.4879, 1.3098, 0.0242, 1.3340`; Berkley `0.6112, 0.3730, 0.9841, 0.0292, 1.0134`; CNA `0.7611, 0.3988, 1.1599, 0.1174, 1.2774`; Markel `0.5305, 0.3592, 0.8897, 0, 0.8897`.
Markel is best (89%), Hartford worst (131%) with both components elevated; Travelers is the median on loss ratio and below median on expense and combined ratios, so it sits in the better half, and stays there after dividends (V3 p.257).
Minor point: Markel's loss ratio is 53.05%, printed as 53.1% in one row and 53.0% in the combined-ratio row; the combined ratio of 89.0% uses 53.0% (V3 p.258).
Berkley is the instructive case: an underwriting profit before dividends (98.4%) becomes a loss after dividends (101.3%) (V3 p.258). ^ex-03-04-17

### Example 18: Travelers loss reserve roll-forward (V3 p.255 to p.257)

Setup 2016 ($m): net reserves at start 39,823; current-year estimated claims 15,675; prior-year decrease 680; total increases 14,995; payments 14,796 (6,220 current year, 8,576 prior years); FX $-74$; net reserves at end 39,948; reinsurance recoverables 7,981 on gross reserves 47,929; pretax income 4,053; total claims and expenses 23,572.

Roll-forward: $39{,}823 + 14{,}995 - 14{,}796 - 74 = 39{,}948$, which ties.
Python: `39948`.
Short tail: current-year payments are $6{,}220/15{,}675 = 39.7\%$ of current-year estimated claims, so a major part of the exposure settles within the year (V3 p.256).
Reinsurance: $7{,}981/47{,}929 = 16.7\%$ of gross reserves ceded (17.5% in 2015, 17.6% in 2014) (V3 p.256).
Reserve increases are $14{,}995/23{,}572 = 63.6\%$ of total claims and expenses, the single largest expense driver (V3 p.256).
Downward revisions of prior-year estimates: $680/4{,}053 = 16.8\%$ of pretax income (17.2% in 2015, 17.4% in 2014), small against total increases but large against profit, so they could reflect conservative initial reserving or a tool for managing earnings (V3 p.256, p.257).
Python: `0.3968, 0.1665, 0.6361, 0.1678, 0.1724, 0.1739`. ^ex-03-04-18

### Example 19: Travelers portfolio and fair value hierarchy (V3 p.258 to p.260)

Setup: investments 70,488 of which fixed maturities 60,515, equities 732, short-term 4,865; Level 1 fixed maturities 2,038 and Level 1 equities 654, $m.

Composition: fixed maturities $60{,}515/70{,}488 = 85.9\%$, short-term 6.9% (a cash proxy), equities 1.0%, consistent with a P&C insurer favouring steady, liquid, low-risk assets; investments are 70% of total assets (V3 p.258, p.259).
Python: `0.8585, 0.0690, 0.0104`.
Level 1 share $= (2{,}038 + 654)/(60{,}515 + 732) = 2{,}692/61{,}247 = 4.4\%$; the rest is almost all Level 2, which implies less liquidity than Level 1 but not illiquidity, and the pricing-service disclosure (reported trades, dealer quotes, two-sided markets) supports the fairness of the values (V3 p.260).
Python: `0.04395`.
Revenue mix for context: premiums $24{,}534/27{,}625 = 88.8\%$ and net investment income 8.3% of 2016 revenues (V3 p.253).
Python: `0.8881, 0.0833`. ^ex-03-04-19

## Item-set patterns

> [!warning] Trap 1: deposits are liabilities, not assets
> The vignette has an analyst say "bank assets consist mostly of deposits, which face different risks than tangible assets".
> Correct: bank assets are predominantly financial assets (loans and securities); deposits are over 80% of liabilities.
> Distractors: "both statements correct" tempts because the risk half of the sentence is true; "only the deposit statement" tempts if you misread systemic importance as applying only to the largest banks (V3 p.202, p.203, p.278).

> [!warning] Trap 2: which Basel III pillar is being described
> A quoted sentence describes a requirement without naming it.
> Correct: "minimum percentage of RWA funded with equity so leverage cannot exhaust capital" is the capital requirement; "enough HQLA for a 30-day stress" is the LCR; "stable funding over a one-year horizon based on deposit tenor and depositor type" is the NSFR.
> Distractors: liquidity and stable funding are swapped because both mention deposits; the tell is 30 days versus one year (V3 p.207, p.278).

> [!warning] Trap 3: reading three capital ratios that move in different directions
> Exhibit gives CET1, Additional Tier 1, Tier 2, total capital, and RWA for three years.
> Correct: compute all three ratios; CET1 and Tier 1 rising while total falls means Tier 2 is being run down, and the honest verdict is "mixed", not "improving".
> Distractors: "improving" if you compute only CET1; "declining" if you compute only total capital; also watch a ratio that improves purely because RWA fell (V3 p.212, p.279, p.280).

> [!warning] Trap 4: which loan-loss ratio answers which question
> Exhibit gives allowance, provision, charge-offs, recoveries, and net charge-offs for consumer and commercial loans over three years.
> Correct: "cushion" means allowance to net charge-offs; "conservatism of provisioning" means provision to net charge-offs; "provision trailing losses" means provision to net charge-offs below 1.0.
> Distractors: a statement that provisioning "trailed" charge-offs when the ratio is above 1.0 every year; a statement about consumer conservatism "declining" when provision to net charge-offs rose from 0.45 to 1.22 (V3 p.238, p.240, p.281, p.282).

> [!warning] Trap 5: what drives the impairment allowance
> Credit-quality exhibit shows strong-quality assets rising, impaired assets falling, past-due-not-impaired rising, and allowances rising.
> Correct: match the percentage change in allowances to the category with the same percentage change; 12.5% and 22.2% growth in allowances track 12.4% and 22.0% growth in past-due-not-impaired assets.
> Distractors: "impaired assets" is the textbook driver (and the HSBC example uses it), but here impaired assets fell while allowances rose, so it cannot be the explanation; "strong quality" moves the wrong way for a rising allowance (V3 p.216, p.280, p.281).

> [!warning] Trap 6: liquidity from asset composition versus liquidity ratios
> One exhibit shows liquid assets as a falling share of total assets while another shows LCR and NSFR rising.
> Correct: answer the question asked; "based only on asset composition" means liquid assets to total assets, and a falling share is declining liquidity even if absolute liquid assets grew.
> Distractors: "increasing risk from loans to total assets" when the loan share actually fell slightly (50.4% to 49.6%); "decreasing risk from investments" when the investment share rose (V3 p.280).

> [!warning] Trap 7: combined ratio denominators and the 100% line
> Loss and LAE ratio uses net premiums earned; underwriting expense ratio uses net premiums written; the combined ratio is their sum.
> Correct: an insurer with the lowest combined ratio has the most efficient underwriting operation, and below 100% is an underwriting profit.
> Distractors: picking the lowest loss ratio alone (Insurer C wins on both here, but a vignette can split them); using premiums earned for both; treating a combined ratio above 100% as merely "less efficient" rather than a loss (V3 p.254, p.257, p.278).

> [!warning] Trap 8: what a falling loss ratio means
> Loss and LAE ratio falls from 61.3% to 59.1% while the expense ratio ticks up.
> Correct: the loss ratio measures success in estimating insured risks, so the fall means improved risk estimation; "efficiency in obtaining new premiums" is the expense ratio, which worsened.
> Distractors: "overall efficiency decreased" when the combined ratio fell from 97.1% to 95.4%; "more efficient at obtaining premiums" when the expense ratio rose (V3 p.257, p.282).

> [!warning] Trap 9: P&C versus L&H attributes
> A list of "differences" contains one reversed statement.
> Correct: L&H claims are more predictable, P&C policies are shorter, and it is L&H (not P&C) that has lower capital requirements and can seek higher-return investments; L&H risk-based capital also incorporates interest rate risk.
> Distractors: assigning the lower capital requirement to P&C because P&C policies are short; assigning interest rate sensitivity to P&C (V3 p.252, p.266, p.268, p.278, p.282).

> [!warning] Trap 10: earnings quality from trading share and freestanding derivatives
> Exhibit shows trading revenue share by bank across years, or a bank's notional freestanding credit derivatives collapsing from 305bn to 13bn.
> Correct: the bank with the lowest trading share has the highest earnings quality; a fall in freestanding derivatives reduces earnings volatility because freestanding positions are marked through the income statement.
> Distractors: "quality highest in the year trading peaked"; "increased posted collateral" (a shrinking book needs less collateral); "consistent correlations" (freestanding status usually means the hedge correlation could not be substantiated) (V3 p.218, p.242, p.246, p.247, p.283).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM04-Analysis-of-Financial-Institutions-Practice-Problems]]

## Cross-links

- [[LM01-Intercorporate-Investments]]: supplies the IFRS 9 categories (amortised cost, FVOCI, FVTPL), the US GAAP debt categories (HTM, trading, AFS), and the VIE consolidation logic that the asset-quality and off-balance-sheet sections here assume.
- [[LM02-Employee-Compensation-Post-Employment-and-Share-Based]]: benefit plans are the "off-balance-sheet" item whose funding shortfalls can drain bank cash, and equity-based compensation is a corporate-culture flag; Practice Problem 13 draws on both.
- [[LM03-Multinational-Operations]]: currency translation adjustments reduce a global bank's capital when the home currency strengthens, and Citigroup's falling non-US NIM is attributed to exactly that translation effect.
- [[LM05-Evaluating-Quality-of-Financial-Reports]]: the discretionary-versus-objective test (allowance versus charge-offs, reserve releases versus pretax income, Level 3 fair values) is the bank and insurer application of the earnings-quality framework.
- [[LM06-Integration-of-Financial-Statement-Analysis-Techniques]]: common-size analysis of assets and revenues, and the habit of decomposing a ratio change into numerator and denominator effects, are applied here to RWA, capital, and operating income.
- [[LM04-Credit-Analysis-Models]]: expected loss, probability of default, and loss given default are the modelling side of the loan impairment allowance whose adequacy this module tests with ratios.
- [[LM05-Measuring-and-Managing-Market-Risk]]: VaR mechanics, confidence level, holding period, and the limits of VaR as a single-day measure underpin the sensitivity component and the trading-revenue-to-VaR ratio.

## Self-test

> [!question] ST1
> A bank reports CET1 capital of 52,000, Additional Tier 1 of 6,000, Tier 2 of 9,000, and RWA of 610,000.
> Its Tier 1 capital ratio is closest to:
> A. 8.5%.
> B. 9.5%.
> C. 11.0%.

> [!question] ST2
> A bank holds 200 of cash (0% weight), 1,000 of residential mortgages (50%), 3,000 of corporate loans (100%), and 100 of loans over 90 days past due (150%).
> Its risk-weighted assets and Pillar 1 capital charge at 8% are closest to:
> A. 3,500 and 280.
> B. 3,650 and 292.
> C. 4,300 and 344.

> [!question] ST3
> A bank discloses HQLA of 250 and expected net cash outflows over a 30-day stress of 200.
> Which statement is most accurate?
> A. The LCR is 80%, below the Basel III minimum.
> B. The LCR is 125%, and the bank could survive about 37.5 days of stress-level outflows.
> C. The LCR is 125%, so the bank's one-year funding structure is adequate.

> [!question] ST4
> A bank's funding is: regulatory capital 100, stable retail deposits under one year 400, less stable retail deposits under one year 200, non-financial corporate funding under one year 150, other liabilities with no stated maturity 50.
> Required stable funding is 650.
> Using the Basel III ASF factors, the NSFR is closest to:
> A. 98%.
> B. 113%.
> C. 138%.

> [!question] ST5
> A bank begins the year with a loan-loss allowance of 4,800, records a provision of 1,500, and has net charge-offs of 2,000; non-accrual loans at year end are 3,200.
> Which conclusion is most accurate?
> A. The allowance rose to 5,300 because the provision was added.
> B. The allowance fell to 4,300 and provisioning trailed actual losses, with a provision-to-net-charge-off ratio of 0.75.
> C. The allowance-to-non-accrual ratio of 1.50 shows reserves are being built ahead of problem loans.

> [!question] ST6
> Over five years, a bank's pretax income rose by 4,000 while its total credit-loss provisions fell by 2,800, and its trading revenue share rose from 6% to 14%.
> An analyst should most likely conclude that earnings quality:
> A. improved, because pretax income grew.
> B. is weak, because 70% of the pretax improvement came from lower provisions and the trading share rose.
> C. is strong, because a lower provision means better credit quality.

> [!question] ST7
> A bank's disclosure shows that four quarterly +25 bp shocks raise projected NII by 800 while four $-25$ bp shocks lower it by 1,100.
> The most accurate inference is that the bank:
> A. has liabilities that reprice faster than its assets.
> B. expects its assets to reprice more quickly and to a greater extent than its liabilities, with falling rates hurting more than rising rates help.
> C. should expect this exact outcome because the disclosure incorporates management responses.

> [!question] ST8
> A P&C insurer reports loss and LAE of 1,420, net premiums earned of 2,000, underwriting expense of 590, and net premiums written of 2,050.
> Using the curriculum's statutory definitions, the combined ratio is closest to:
> A. 71.0%, an underwriting profit.
> B. 99.8%, an underwriting profit.
> C. 100.5%, an underwriting loss.

> [!question] ST9
> A P&C insurer released 300 of prior-year loss reserves in a year when pretax income was 1,500.
> The most appropriate analyst reaction is that the release:
> A. proves the initial reserves were set conservatively.
> B. is immaterial because it is small relative to total reserve increases.
> C. contributed 20% of pretax income and could reflect either conservative initial reserving or earnings management, so it warrants scrutiny.

> [!question] ST10
> An L&H insurer reports interest income of 2,400 and gains on debt securities of 60; loans, deposits, and debt securities totalled 50,000 at the start of the year and 54,000 at the end.
> Following the curriculum's method, the return on average fixed-income assets is closest to:
> A. 4.56%.
> B. 4.62%.
> C. 4.73%.

> [!success]- Answer key
> ST1: B.
> Tier 1 $= (52{,}000 + 6{,}000)/610{,}000 = 9.51\%$ (Python: `0.09508`).
> A is the CET1 ratio $52{,}000/610{,}000 = 8.52\%$; C is the total capital ratio $67{,}000/610{,}000 = 10.98\%$ (V3 p.210).
>
> ST2: B.
> $RWA = 200 \times 0 + 1{,}000 \times 0.5 + 3{,}000 \times 1.0 + 100 \times 1.5 = 0 + 500 + 3{,}000 + 150 = 3{,}650$; charge $= 0.08 \times 3{,}650 = 292$ (Python: `3650, 292`).
> A forgets the 150% weight on past-due loans; C is the unweighted total 4,300 (V3 p.209, p.211).
>
> ST3: B.
> $LCR = 250/200 = 125\%$ and $1.25 \times 30 = 37.5$ days (Python: `1.25, 37.5`).
> A inverts the ratio.
> C describes the NSFR; the LCR says nothing about one-year funding structure (V3 p.220, p.247, p.248).
>
> ST4: B.
> $ASF = 100 \times 1.00 + 400 \times 0.95 + 200 \times 0.90 + 150 \times 0.50 + 50 \times 0 = 100 + 380 + 180 + 75 + 0 = 735$; $NSFR = 735/650 = 113\%$ (Python: `735, 1.1308`).
> A omits capital ($635/650 = 97.7\%$); C uses unweighted funding ($900/650 = 138\%$) (V3 p.220, p.221).
>
> ST5: B.
> Ending allowance $= 4{,}800 + 1{,}500 - 2{,}000 = 4{,}300$; provision to net charge-offs $= 1{,}500/2{,}000 = 0.75$, below 1.0, so provisioning trailed losses (Python: `4300, 0.75`).
> A ignores charge-offs.
> C uses the beginning allowance ($4{,}800/3{,}200 = 1.50$); on the ending balance it is $4{,}300/3{,}200 = 1.34$, and a single-year level cannot show "building ahead" without a trend (V3 p.238, p.239, p.240).
>
> ST6: B.
> $2{,}800/4{,}000 = 70\%$ of the pretax gain came from a discretionary estimate falling, and trading income is the most volatile source, so quality is weak (Python: `0.70`).
> A confuses level with quality; C ignores that provisions are discretionary and can be under-recorded (V3 p.218, p.241, p.242).
>
> ST7: B.
> NII rising with rates means assets reprice faster and further than liabilities; the larger downside ($-1{,}100$ versus $+800$) mirrors HSBC's asymmetric disclosure.
> A has the direction backwards.
> C is wrong because such tables are static and assume no management action (V3 p.224, p.225).
>
> ST8: B.
> Loss and LAE ratio $= 1{,}420/2{,}000 = 71.0\%$; underwriting expense ratio $= 590/2{,}050 = 28.8\%$; combined $= 99.8\%$, below 100% (Python: `0.710, 0.2878, 0.9978`).
> A stops at the loss ratio.
> C uses premiums earned in the expense ratio ($590/2{,}000 = 29.5\%$, combined 100.5%), which is the modified GAAP-style presentation, not the statutory definition (V3 p.255, p.257).
>
> ST9: C.
> $300/1{,}500 = 20\%$ of pretax income (Python: `0.20`), the same order as Travelers' 16.8% to 17.4%.
> The curriculum says downward revisions indicate conservative initial reserving but may also be a tool for manipulating earnings, so A over-claims and B misjudges materiality by the wrong benchmark (V3 p.256, p.257).
>
> ST10: C.
> Income $= 2{,}400 + 60 = 2{,}460$; average assets $= (50{,}000 + 54{,}000)/2 = 52{,}000$; return $= 2{,}460/52{,}000 = 4.73\%$ (Python: `0.04731`).
> A divides by the ending balance ($2{,}460/54{,}000 = 4.56\%$); B omits the debt gains ($2{,}400/52{,}000 = 4.62\%$) (V3 p.267).

## Flashcards

#flashcards/cfa-l2/03-Financial-Statement-Analysis/lm04

Two distinctive features of financial institutions::Systemic importance (intermediation creates linkages, contagion) and assets that are predominantly financial assets carried near fair value (V3 p.202, p.203).
Definition of systemic risk::Risk of disruption to financial services caused by impairment of part of the financial system with serious negative consequences for the whole economy (V3 p.202).
Three highlights of Basel III::Minimum capital as a percentage of RWA, minimum liquidity for a 30-day stress (LCR), and minimum stable funding over one year (NSFR) (V3 p.207).
Basel III CET1 minimum::4.5% of risk-weighted assets (V3 p.210).
Basel III Tier 1 minimum::6.0% of risk-weighted assets (V3 p.210).
Basel III total capital minimum::8.0% of risk-weighted assets (V3 p.210).
What is in CET1 capital::Common stock, issuance surplus, retained earnings, accumulated OCI, less intangibles, deferred tax assets, and other regulatory deductions (V3 p.210).
Criteria for Additional Tier 1 instruments::Subordinate to deposits and debt, no fixed maturity, payments entirely at the bank's discretion; qualifying perpetual preferred stock (V3 p.210, p.232).
Criteria for Tier 2 instruments::Subordinate to depositors and general creditors, original maturity of at least five years, plus limited portions of the loan-loss allowance (V3 p.210, p.233).
Risk weight on cash, corporate loans, loans over 90 days past due::0%, 100%, above 100% (150% in the example) (V3 p.209).
Which body wrote Basel III and who hosts it::The Basel Committee on Banking Supervision, hosted by the Bank for International Settlements (V3 p.205, p.207).
Financial Stability Board goal::Identify systemic risk in the financial sector and coordinate jurisdictional action to address it (V3 p.207).
CAMELS letters::Capital adequacy, Asset quality, Management capabilities, Earnings sufficiency, Liquidity position, Sensitivity to market risk (V3 p.209).
CAMELS rating scale::1 is best, 5 is worst; composite is examiner-weighted, not a simple mean (V3 p.209).
Three ratios for judging the loan-loss allowance::Allowance to non-performing loans; allowance to net charge-offs; provision to net charge-offs (V3 p.238).
Why compare the allowance to charge-offs::The allowance and provision are discretionary; net charge-offs and non-accrual loans are more objective (V3 p.238).
Provision to net charge-offs persistently below 1.0 means::Provisioning trails actual losses; the allowance is being drained and a catch-up may follow (V3 p.240).
Net charge-offs formula::Charge-offs minus recoveries (V3 p.239).
Allowance roll-forward::Ending allowance equals beginning allowance plus provision minus net charge-offs (V3 p.238).
LCR definition::High-quality liquid assets divided by expected net cash outflows over a 30-day stress scenario; minimum 100% (V3 p.220, p.247).
NSFR definition::Available stable funding divided by required stable funding; target above 100% (V3 p.220, p.221).
ASF factor for stable retail deposits under one year::95% (V3 p.221).
ASF factor for less stable retail deposits under one year::90% (V3 p.221).
ASF factor for non-financial corporate funding under one year::50% (V3 p.221).
ASF factor for regulatory capital and liabilities of one year or more::100% (V3 p.221).
Do HQLA enter the NSFR::No; highly liquid assets do not enter the NSFR calculation (V3 p.248).
Two Basel III liquidity monitoring metrics discussed::Concentration of funding and contractual maturity mismatch (V3 p.221).
Fair value Level 1, 2, 3 inputs::Level 1 quoted prices for identical instruments in active markets; Level 2 observable but not identical quotes (similar instruments, yield curves, spreads); Level 3 unobservable model inputs (V3 p.217, p.218).
Most volatile bank income source::Trading income; net interest and fee income are more sustainable (V3 p.218).
Net interest margin formula::Net interest revenue divided by average interest-earning assets (V3 p.245).
Effect of an unexpected yield curve inversion on NIM::Decreases, because short-term funding costs rise above long-term loan yields (V3 p.243, p.283).
Freestanding derivative accounting::Fair value changes go through the income statement each period, raising earnings volatility and possibly collateral needs (V3 p.247).
Cash flow hedge or net investment hedge accounting::Fair value changes go to OCI and are recognised in net income over the life of the hedged transaction (V3 p.246).
VaR usefulness across banks::Good for intra-company trends, poor for comparing companies because assumptions differ (V3 p.249).
Bank-specific factors CAMELS does not address::Government support, mission of the banking entity, corporate culture (V3 p.226, p.227, p.228).
Generic factors CAMELS does not address::Competitive environment, off-balance-sheet items, segment information, currency exposure, risk factors, Basel III disclosures (V3 p.228, p.229, p.230).
Corporate culture red flags::Losses from narrow concentrated bets, restatements from control failures, above-average equity compensation, slow provisioning followed by large write-downs (V3 p.228).
Insurance float::Premiums collected but not yet paid out as benefits, invested for income (V3 p.252).
P&C versus L&H claims and policy length::P&C short policies and lumpy unpredictable claims; L&H long policies and predictable actuarial claims (V3 p.252).
Which insurer type has lower capital requirements::L&H, because claims are more predictable; L&H risk-based capital also incorporates interest rate risk (V3 p.268).
Loss and LAE ratio::(Loss expense plus loss adjustment expense) divided by net premiums earned; measures success in estimating insured risks (V3 p.257).
Underwriting expense ratio::Underwriting expense divided by net premiums written; measures efficiency in obtaining new premiums (V3 p.257).
Combined ratio::Loss and LAE ratio plus underwriting expense ratio; below 100% is an underwriting profit (V3 p.257).
Combined ratio after dividends::Combined ratio plus dividends to policyholders (shareholders) over net premiums earned; a stricter efficiency test (V3 p.257).
Hard versus soft P&C market::Low combined ratio signals a hard market that attracts entrants who cut prices, pushing the combined ratio up into a soft market (V3 p.254).
Downward revision of prior-year reserves signals::Conservative initial reserving or possibly earnings manipulation; flows straight to pretax income (V3 p.256, p.257).
Investment return metric for insurers::Investment income divided by invested assets, computed with and without unrealised gains (V3 p.259, p.266).
L&H interest rate risk metric::Compare duration of assets with duration of liabilities (V3 p.266).
Reverse repurchase agreement from the bank's view::A collateralised loan the bank has made; counts as a loan and, if 30-day, as a liquid asset for the LCR (V3 p.212, p.283).
Micro: CET1 116,552 and RWA 857,181, CET1 ratio?::13.6%; keystrokes 116552 ÷ 857181 = 0.136 (V3 p.211).
Micro: HQLA 403.7 and net outflows 332.5, LCR and stress days?::121% and 36.3 days; keystrokes 403.7 ÷ 332.5 = 1.214, × 30 = 36.4 (curriculum rounds LCR to 121% first) (V3 p.247).
Micro: losses 11,351 on premiums earned 13,811, expenses 5,156 on premiums written 10,568, combined ratio?::131.0%; keystrokes 11351 ÷ 13811 = 0.822, 5156 ÷ 10568 = 0.488, sum 1.310 (V3 p.258).
Micro: allowance 1,540 and net charge-offs 1,060, cushion ratio?::1.45; keystrokes 1540 ÷ 1060 = 1.453 (V3 p.281).
Micro: ratings 1, 2.5, 2, 3, 1, 1 with weights 1, 2, 1, 2, 1, 1, composite?::2.00; keystrokes 1 + 5 + 2 + 6 + 1 + 1 = 16, ÷ 8 = 2.00 (V3 p.252).
The trap in "bank assets consist mostly of deposits"::Deposits are liabilities (over 80% of them); assets are loans and securities (V3 p.202, p.278).
The trap in "P&C insurers have lower capital requirements"::Reversed; L&H insurers have lower capital requirements because claims are predictable (V3 p.268, p.278).
Which ratio does a 30-day reverse repo affect::The LCR, because it is a highly liquid asset; not the NSFR (V3 p.283).
{{Two examiners can assign the same six CAMELS component ratings and still reach different composite ratings}} because each weights the components by judgment (V3 p.209).
{{Net interest income rises when rates rise even for a perfectly matched bank}} simply because the bank has more assets than liabilities (V3 p.224).
{{Level 2}} securities dominate Travelers' fixed maturities at 96.3%, implying less liquidity than Level 1 but not illiquidity (V3 p.260).

## Common mistakes

1. Calling deposits assets; deposits are the bulk of bank liabilities, and bank assets are loans and securities (V3 p.202, p.203).
2. Confusing the LCR (30-day stress, HQLA) with the NSFR (one-year funding structure, ASF over RSF) when a vignette describes one in words (V3 p.207, p.220).
3. Judging capital adequacy from one ratio; compute CET1, Tier 1, and total, and call divergent trends "mixed" (V3 p.279, p.280).
4. Attributing an improved capital ratio to more capital when RWA fell; decompose numerator and denominator (V3 p.212).
5. Using the wrong loan-loss ratio for the question: cushion is allowance over net charge-offs, conservatism is provision over net charge-offs, and "trailing" means that ratio is below 1.0 (V3 p.238, p.240).
6. Assuming allowances must track impaired assets; test which category's percentage change actually matches the allowance change (V3 p.216, p.280).
7. Putting net premiums earned in the underwriting expense ratio denominator; the statutory definition uses net premiums written, while the loss ratio uses premiums earned (V3 p.255, p.257).
8. Treating the combined ratio as a single fraction; it is the sum of two ratios with different denominators (V3 p.257).
9. Reversing P&C and L&H attributes on capital requirements and interest rate sensitivity; L&H has lower capital needs and its risk-based capital incorporates interest rate risk (V3 p.268).
10. Comparing VaR across banks; the curriculum limits VaR to intra-company trends because assumptions differ (V3 p.249).
11. Treating a rate sensitivity table as a forecast; it is static, ignores management response, and changes one factor at a time (V3 p.225, p.251).
12. Reading a rising trading share or a provision-driven profit increase as good earnings; both lower earnings quality (V3 p.242, p.246).
13. Including all investment gains when the question asks for fixed-income return; use only the gains on debt securities and the average balance (V3 p.267).
14. Assuming CAMELS letters are ordered by importance; capital and liquidity are equally weighted in Basel III (V3 p.226).
15. Reading a reserve release as automatically conservative; it can also be earnings management, and it is material relative to pretax income (V3 p.256, p.257).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "03-04" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
