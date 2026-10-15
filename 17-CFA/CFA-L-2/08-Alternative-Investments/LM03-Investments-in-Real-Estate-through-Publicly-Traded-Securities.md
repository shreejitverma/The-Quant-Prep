---
type: cfa-lm
topic: "Alternative Investments"
topic_code: "08"
topic_slug: "08-Alternative-Investments"
volume: 8
lm: 3
title: "Investments in Real Estate through Publicly Traded Securities"
pages: "121-163"
weight_band: "5-10%"
difficulty: 2
los_count: 5
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/alternative-investments]
---

# LM3: Investments in Real Estate through Publicly Traded Securities

Difficulty 2 of 5: the arithmetic (NAVPS builds, FFO and AFFO walks, multiples, a two-step DDM) is short-division easy, but the exam punishes any confusion about which items get added versus subtracted in each walk and which valuation lens fits which situation, so the module is a memory-precision test more than a computation test.

## LOS map

- **discuss** types of publicly traded real estate securities (V8 p.121) ^los-08-03-a
    - Examiner asks: classify a described company as an equity REIT, mortgage REIT, REOC, or MBS from clues about what it owns, whether it is tax advantaged, and whether it develops for-sale property, or identify why a business is organized as a REOC rather than a REIT.
- **justify** the use of net asset value per share (NAVPS) in valuation of publicly traded real estate securities and estimate NAVPS based on forecasted cash net operating income (V8 p.121) ^los-08-03-b
    - Examiner asks: build NAVPS from a table of NOI, non-cash rent, growth, a cap rate, other assets and liabilities, or state what a cap rate increase or a deferred tax liability does to the estimate.
- **describe** the use of funds from operations (FFO) and adjusted funds from operations (AFFO) in REIT valuation (V8 p.121) ^los-08-03-c
    - Examiner asks: walk from net income to FFO (add depreciation and losses, subtract gains) and from FFO to AFFO (subtract non-cash rent and recurring capex), or say which measure best captures current economic return and which is more widely compiled by data providers.
- **calculate** and interpret the value of a REIT share using the net asset value, relative value (price-to-FFO and price-to-AFFO), and discounted cash flow approaches (V8 p.121) ^los-08-03-d
    - Examiner asks: value one REIT three ways from one exhibit, including a two-step dividend discount model with a Gordon terminal value, and reconcile or rank the answers.
- **explain** advantages and disadvantages of investing in real estate through publicly traded securities compared to private vehicles (V8 p.121) ^los-08-03-e
    - Examiner asks: match an investor objective (liquidity, growth, control, tax efficiency) to the right vehicle among direct ownership, REIT, REOC, and MBS, and identify the trade-off each choice sacrifices.

## Core intuition

Start with what a REIT actually is: a legal bargain with the tax authority (V8 p.123).
The company gives up retained earnings by promising to distribute 90 to 100 percent of taxable income, to hold at least 75 percent of assets in real estate, and to earn at least 75 percent of income from rents or mortgage interest; in exchange, dividends paid are deductible, which effectively exempts the REIT from corporate income tax (V8 p.123, p.124).
Shareholders are taxed once instead of twice, and that single layer of taxation is the economic engine that makes the structure worth its restrictions (V8 p.125).
The restrictions bind, though: a REIT cannot retain much cash flow, so every acquisition or development program pushes it back to the capital markets, and the faster it grows the more often it must issue equity or debt (V8 p.126).
Countries add qualification plumbing such as the US 5/50 rule (at least 100 shareholders, no five owning more than half ) precisely to stop a small group from wrapping one building in a tax shelter (V8 p.124).

A real estate operating company (REOC) is the counterfactual: an ordinary taxable company that owns real estate (V8 p.123).
Businesses choose the REOC form when no REIT regime exists in their country, when they develop for-sale property to a large extent, or when they earn non-qualifying income such as brokerage and third-party management (V8 p.123).
The REOC pays tax but keeps full operating and financial flexibility and can reinvest all its income, so growth potential is higher while current income is lower (V8 p.147, p.148).
Mortgage-backed securities are the debt route: securitized claims on pools of residential (RMBS) or commercial (CMBS) mortgage loans, and by market value real estate debt securities dwarf the listed equity side (V8 p.123).
Equity REITs own buildings; mortgage REITs own loans (V8 p.123).

> [!abstract] Idea 1: a REIT trades retained earnings for tax exemption
> The payout, asset, and income tests are the price of deducting dividends from taxable income (V8 p.123, p.124).
> Every downstream fact follows: high dividend yields, dependence on external capital for growth, taxable REIT subsidiaries for non-qualifying business, and the premium investors place on managements that can raise and deploy capital well (V8 p.126, p.127).
> The payout requirement is based on taxable income, which is computed after depreciation, so a REIT can pay out far more cash than the rule requires while still complying easily (V8 p.142).

The valuation half of the module is best read as a series of repairs to historical cost accounting.
US GAAP carries buildings at cost less accumulated depreciation, which understates long-held appreciating assets and overstates depreciation, so book value per share is nearly useless for a REIT (V8 p.127, p.128).
IFRS at least permits a fair value model for investment property, in which case reported values may be usable directly (V8 p.127).
Each valuation tool repairs a different statement.
NAVPS repairs the balance sheet: restate assets and liabilities at market value, divide by shares (V8 p.128).
FFO repairs the income statement: add back real estate depreciation and amortization because investors believe buildings hold or gain value, and strip gains and losses on property sales because they are not sustainable operating income (V8 p.132, p.134).
AFFO repairs FFO: remove the non-cash portion of straight-lined rent and charge the recurring capital expenditures and leasing costs needed to keep the buildings competitive, leaving the best available proxy for sustainable, distributable cash earnings (V8 p.132, p.134).

> [!abstract] Idea 2: NAV looks through the balance sheet, FFO and AFFO look through the income statement
> To build NAVPS, capitalize forward cash NOI at a market cap rate, add other tangible assets, subtract hard liabilities, and drop soft items (goodwill, deferred financing costs, deferred tax assets and liabilities) because they are accounting provisions, not economic claims (V8 p.128, p.129).
> To build AFFO, start from net income and make exactly four moves: add depreciation and amortization, net out gains and losses on sales, subtract non-cash straight-line rent, subtract recurring maintenance capex and leasing commissions (V8 p.132, p.134).
> The exam's favorite distractors reverse a sign or swap depreciation for non-cash rent somewhere in these walks.

The cap rate is where all the economics of the property market compress into one number: it is NOI divided by value, the required current-income return for risk of that type (V8 p.129, p.130).
Value moves inversely with it, so a 100 bp cap rate rise marks down the estimated real estate value, and NAV with it, immediately (V8 p.148, p.151).
Cap rates and values per square foot look like shortcuts, but they are distilled from full discounted cash flow underwriting by private buyers, so an NAV is a private-market DCF wearing a simple ratio (V8 p.130).
NAV has soft spots the exam probes: it treats the company as a static pool of assets rather than a going concern, it says nothing about management's ability to add or destroy value, and it turns subjective when transactions dry up or the portfolio is huge or holds odd assets such as raw land, single-use properties, and joint ventures (V8 p.131).
That is why shares oscillate between premiums and discounts to NAV of 25 percent or more, why a strong management team can justify paying a premium, and why analysts often use NAV relatively, buying the smallest premium or selling the smallest discount, or backing an implied cap rate out of the share price to compare two portfolios (V8 p.131, p.132).

Multiples are the income-lens cousin of P/E.
P/FFO is the sector's P/E; P/AFFO approximates a cash flow multiple; both are computed on current price over year-ahead estimates (V8 p.132, p.133).
Three drivers separate REIT multiples: expected FFO and AFFO growth (business model, supply-constrained geography, management, lease structure), the riskiness of the underlying cash flows (apartments beat hotels; young, well-maintained portfolios beat deferred-maintenance ones), and leverage, since FFO and AFFO are levered income and higher debt raises required returns and compresses multiples (V8 p.133).
EV/EBITDA sidesteps leverage entirely, and its inverse EBITDA/EV approximates the cap rate formula NOI/value (V8 p.133).
Because REITs must pay out most income, dividend discount and DCF models port over directly: two- or three-step models with near, intermediate, and long-run growth, a CAPM discount rate, and a Gordon terminal value (V8 p.122, p.123, p.142).

Property subtype economics drive the cash flow risk input.
Necessity-anchored shopping centers (grocery, drug) are defensive, and strict zoning that blocks new supply protects rents (V8 p.141).
Health care REITs shrug off recessions but live and die on demographics and government funding of health care (V8 p.162).
Storage has trivially low barriers to entry, so overbuilding is the standing risk (V8 p.162).
Hotels have no leases at all, so their cash flows swing with the cycle, while apartments re-lease annually and offices and centers carry long leases that smooth income (V8 p.125, p.133).
Long leases mean stability today but slower mark-to-market of rents; short leases mean volatility but faster inflation capture.

> [!abstract] Idea 3: one building, two prices, and an arbitrage channel between them
> Public pricing is liquid, forward looking, and contaminated by equity market beta; private pricing is appraisal based and lags market conditions (V8 p.127, p.131, p.145).
> Persistent gaps get closed by corporate action: companies trading far below NAV go private or sell assets, and when values are rich, private funds exit through IPOs and public companies sell buildings to realize gains (V8 p.144).
> This is also why public real estate hedges less in the short run (high equity correlation) yet tracks real estate fundamentals over the long term (V8 p.145).

Choosing public versus private is an objectives question, not a ranking (V8 p.144).
Public buys liquidity, professional management, diversification, low minimums, limited liability, regulation, transparency, and (for REITs) single taxation; it costs volatility, short-run equity correlation, activity restrictions, taxation of dividends at income rates, and the risk of trading away from underlying value (V8 p.145).
Private buys control, strategy freedom (merchant development), the illiquidity premium, and depreciation tax shelter; it costs illiquidity, high fees and minimums, stale appraisals, low transparency, and leverage-driven returns (V8 p.145).
Institutions commonly hold both and use the listed side to express short-term views quickly (V8 p.144).

## Formulas and derivations

**Net asset value per share** (V8 p.128)
$$
\text{NAVPS} = \frac{\text{Market value of assets} - \text{Market value of liabilities}}{\text{Shares outstanding}}
$$
^f-08-03-1

- Assets and liabilities at current market value, not book; exclude soft items (goodwill, deferred financing costs, deferred tax assets and liabilities) and mark debt to market when rates have moved (V8 p.128).
- It holds because a claim on net assets is worth what the assets would fetch less what must be repaid; book values fail only because historical cost accounting misstates the numerator (V8 p.127, p.128).
- Computed pre-tax on liquidation gains, because an acquirer's tax position is unknowable (V8 p.128).

**Net operating income** (V8 p.128)
$$
\text{NOI} = \text{Gross rental revenue} - \text{Vacancy and collection loss} - \text{Operating expenses}
$$
^f-08-03-2

- Operating expenses include insurance, property taxes, utilities, G&A, repairs and maintenance; NOI is before interest, income taxes, depreciation, and amortization (V8 p.128).
- NOI is the property-level analogue of EBIT: the income the building itself throws off regardless of who owns or finances it (V8 p.128).

**Value of operating real estate by direct capitalization** (V8 p.129, p.130)
$$
V_{\text{operating RE}} = \frac{\text{Expected next-12-month cash NOI}}{\text{Cap rate}}, \qquad \text{Cap rate} = \frac{\text{NOI}}{\text{Total value}}
$$
^f-08-03-3

- Cash NOI = reported NOI minus non-cash straight-line rent plus full-year effect of mid-year acquisitions, then grown one year (V8 p.129).
- The cap rate comes from recent comparable transactions; it is the market's required current return for that risk, so dividing by it is a perpetuity valuation of the rental stream (V8 p.129, p.130).
- Value falls when the cap rate rises and rises with expected NOI growth (V8 p.148, p.149).

> [!tip] Calculator
> Exhibit 2 build: `270432 - 7667 + 4534 =` (267,299) `x 1.015 =` (271,308) `/ 0.07 =` (3,875,829); add `+ 65554 + 34566 + 45667 + 23456 =` (4,045,072); `- 1010988 - 119886 =` (2,914,198); `/ 55689 =` 52.33.

**Funds from operations** (V8 p.132, p.134)
$$
\text{FFO} = \text{Net income} + \text{D\&A (real estate)} + \text{Losses on sales} - \text{Gains on sales} + \text{Impairments}
$$
^f-08-03-4

- The compact curriculum form is FFO = (Net income + Depreciation + Amortization) - (Net gains on sale of real property); the fuller Nareit form adds losses, subtracts gains, and adds back real estate impairments and write-downs (V8 p.132, p.134).
- Depreciation is added back because real estate tends to hold or gain value, so IFRS and US GAAP depreciation is not economic; gains and losses are stripped because they are not sustainable operating income (V8 p.134).
- FFO is an SEC-accepted non-GAAP measure that must be reconciled to GAAP net income; it is not a cash flow measure and excludes the spending needed to sustain the assets (V8 p.134).

**Adjusted funds from operations** (V8 p.132, p.134)
$$
\text{AFFO} = \text{FFO} - \text{Non-cash (straight-line) rent} - \text{Recurring maintenance capex and leasing costs}
$$
^f-08-03-5

- Straight-line rent books the average contractual rent over a lease with step-ups, so early-year revenue exceeds cash received; the difference is the non-cash rent removed here (V8 p.134).
- Recurring capex and leasing costs (commissions, tenant improvements, allowances) are real costs of keeping space rented, so AFFO, also called FAD or cash available for distribution, best approximates sustainable dividend-paying capacity (V8 p.134).
- AFFO is superior in concept but noisier in practice; estimates vary so much that data providers compile FFO, not AFFO (V8 p.134, p.135).

**Relative valuation by sector multiple** (V8 p.143, p.155)
$$
V_0 = \left(\frac{P}{\text{FFO}}\right)_{\text{sector}} \times \text{FFO}_1 \text{ per share}, \qquad V_0 = \left(\frac{P}{\text{AFFO}}\right)_{\text{sector}} \times \text{AFFO}_1 \text{ per share}
$$
^f-08-03-6

- Multiples use current price over year-ahead estimates and are compared with the company's own history and with peers owning similar property (V8 p.133).
- P/FFO is the REIT P/E; P/AFFO approximates a cash earnings multiple; both are levered, so leverage differences must be adjusted for separately, unlike EV/EBITDA (V8 p.133).

**Two-step dividend discount model** (V8 p.122, p.156, p.158)
$$
V_0 = \sum_{t=1}^{n} \frac{D_t}{(1+r)^t} + \frac{1}{(1+r)^n}\cdot\frac{D_{n+1}}{r-g}
$$
^f-08-03-7

- $D_t$: forecast dividends per share; $r$: required return on equity; $g$: long-run growth from year $n+1$; the Gordon terminal value sits at the end of year $n$ and is discounted $n$ periods (V8 p.161, p.163).
- Applicable to REITs precisely because the payout requirement makes dividends large and forecastable; investors typically use two- or three-step versions with near, intermediate, and long-term growth (V8 p.122, p.123).

> [!tip] Calculator
> Baldwin: terminal `1.06 x 1.05 = / 0.035 =` (31.71); Year 2 cash flow `+ 1.06 =` (32.77); `/ 1.085 / 1.085 =` (27.84); `+` PV of D1 `1 / 1.085 =` (0.9217); total 28.76.

**CAPM required return for the discount rate** (V8 p.142, p.158)
$$
r = r_f + \beta \times \text{Market risk premium}
$$
^f-08-03-8

- CSC: $4.0\% + 0.80 \times 5.0\% = 8.0\%$; Baldwin: $4.0\% + 0.90 \times 5.0\% = 8.5\%$ (V8 p.142, p.158).
- REIT betas below 1 reflect lease-contract income stability relative to the broad equity market (V8 p.142).

**Implied cap rate from the share price** (V8 p.132)
$$
\text{Implied cap rate} = \frac{\text{Expected cash NOI}}{\text{Equity market cap} + \text{MV of debt and other liabilities} - \text{Non-RE assets}}
$$
^f-08-03-9

- Run the NAV model backward: put the current share price in as NAVPS and solve for the cap rate the market is paying (V8 p.132).
- Comparing implied cap rates across two similar portfolios shows whether the market prices them differently, a relative-value use of an absolute tool (V8 p.132).

**Payout, coverage, and leverage metrics** (V8 p.139, p.140)
$$
\text{Payout} = \frac{\text{DPS}}{\text{FFO or AFFO per share}}, \quad \text{Coverage} = \frac{\text{EBITDA}}{\text{Interest}}, \quad \text{Leverage} = \frac{\text{Net debt}}{\text{EBITDA}}
$$
^f-08-03-10

- Net debt = total debt minus cash and equivalents; debt is also compared with equity market capitalization and with gross (undepreciated) real estate cost (V8 p.140).
- Lower leverage and higher coverage than peers support a premium multiple because FFO and AFFO are levered income (V8 p.133, p.140).

## Worked examples

**Exhibit walk 1: analyst adjustments to obtain NAVPS** (V8 p.128, p.129)
Build NAVPS for a REIT with last-12-month NOI of $270,432 thousand, non-cash rent $7,667, a mid-year acquisition needing a $4,534 full-impact adjustment, 1.5% growth, a 7.0% cap rate, cash $65,554, land held for development $34,566, accounts receivable $45,667, prepaid/other $23,456, debt $1,010,988, other liabilities $119,886, and 55,689 shares.
Line 1, cash NOI: $270{,}432 - 7{,}667 + 4{,}534 = 267{,}299$ (Python confirms); non-cash straight-line rent comes out, and half a year of acquisition NOI is added so a full year is in the base.
Line 2, forward NOI: $267{,}299 \times 1.015 = 271{,}308$ (Python: growth of 4,009).
Line 3, operating real estate: $271{,}308 / 0.07 = 3{,}875{,}829$ (Python: 3,875,828.6).
Line 4, gross assets: $3{,}875{,}829 + 65{,}554 + 34{,}566 + 45{,}667 + 23{,}456 = 4{,}045{,}072$; land and other tangibles enter at book, intangibles are excluded.
Line 5, NAV: $4{,}045{,}072 - 1{,}010{,}988 - 119{,}886 = 2{,}914{,}198$; deferred taxes would not be deducted because they are an accounting provision, not an economic liability (V8 p.129).
Line 6, NAVPS: $2{,}914{,}198 / 55{,}689 = 52.33$ (Python: 52.3299). ^ex-08-03-1

**Exhibit walk 2: FFO and AFFO for Office Equity REIT Inc.** (V8 p.135)
Net income SGD160,638 thousand, D&A 76,100, losses from sale of depreciable real estate 25,000, non-cash rent 21,103, recurring capex and leasing commissions 55,765, shares 55,689.
FFO walk: $160{,}638 + 76{,}100 + 25{,}000 = 261{,}738$ (Python confirms); the 25,000 is a loss, so it is added back; a gain would be subtracted.
FFO per share: $261{,}738 / 55{,}689 = 4.70$ (Python: 4.6999).
AFFO walk: $261{,}738 - 21{,}103 - 55{,}765 = 184{,}870$ (Python confirms).
AFFO per share: $184{,}870 / 55{,}689 = 3.32$ (Python: 3.3197).
AFFO is 71% of FFO here; the gap is the recurring cost of staying in business that FFO ignores. ^ex-08-03-2

**Examples 1 and 2: what moves REIT multiples** (V8 p.133)
Example 1: owning apartments has less cash flow variability than owning hotels (annual leases versus nightly room rates), so apartment REITs trade at relatively high multiples compared with hotel REITs.
Example 2: companies with young, well-maintained portfolios trade at higher multiples than companies with older, deferred-maintenance properties that will need heavy capex to sustain rent growth.
Both are instances of driver 2 (risk of the underlying real estate); the other drivers are expected FFO/AFFO growth and leverage, where higher leverage lowers the multiple (V8 p.133). ^ex-08-03-3

**Mini case walk 1: CSC's FFO, AFFO, and payout ratios** (V8 p.136, p.139)
From Capitol Shopping Center REIT's Year 2 statements: net income 124,454, D&A 115,110, non-cash rents 5,112, recurring capex 20,006, weighted shares 60,600, dividends 2.80 per share.
FFO: $124{,}454 + 115{,}110 = 239{,}564$; per share $239{,}564/60{,}600 = 3.95$ (Python: 3.9532).
AFFO: $239{,}564 - 5{,}112 - 20{,}006 = 214{,}446$; per share $214{,}446/60{,}600 = 3.54$ (Python: 3.5387).
Payouts: $2.80/3.95 = 70.9\%$ of FFO and $2.80/3.54 = 79.1\%$ of AFFO (Python: 70.83% and 79.12%; the exhibit's 70.9%/79.1% uses unrounded per-share figures).
Year 1 checks: FFO $= 225{,}987$ (3.76), AFFO $= 202{,}041$ (3.36), payouts 73.1% and 81.8% (Python confirms all).
Note the non-cash rent deduction equals the cash flow statement's change in deferred rents, 5,112, which is where analysts find it (V8 p.139). ^ex-08-03-4

**Mini case walk 2: CSC's balance sheet analysis** (V8 p.140)
Ending debt: mortgages 701,884 + notes 1,090,745 = 1,792,629.
Equity market cap: $61{,}100 \times 72.36 = 4{,}421{,}196$; debt/market cap $= 1{,}792{,}629/4{,}421{,}196 = 40.5\%$ versus peers at 47.1% (Python: 40.55%).
Interest coverage: $340{,}387/100{,}823 = 3.38\times$ versus peers at 2.35x (Python: 3.3761).
Net debt: $1{,}792{,}629 - 85{,}736 = 1{,}706{,}893$; net debt/EBITDA $= 1{,}706{,}893/340{,}387 = 5.01\times$ versus peers at 7.10x (Python confirms).
Net debt/gross real estate: $1{,}706{,}893/3{,}761{,}361 = 45.4\%$ versus peers at 52.8% (Python: 45.38%).
Every metric shows CSC less levered and better covered than peers, which supports a premium multiple (V8 p.140, p.141). ^ex-08-03-5

**Mini case walk 3: CSC's comparative multiples at $69.85** (V8 p.142, p.143)
Consensus estimates: FFO/share $4.23 (Yr3E) and $4.59 (Yr4E); AFFO/share $3.76 and $4.09.
P/FFO: $69.85/4.23 = 16.5\times$ and $69.85/4.59 = 15.2\times$ (Python: 16.51, 15.22).
P/AFFO: $69.85/3.76 = 18.6\times$ and $69.85/4.09 = 17.1\times$ (Python: 18.58, 17.08).
Premium to shopping center REITs (14.5x, 13.3x, 16.1x, 14.5x): $16.5/14.5 - 1 = 13.8\%$, then 14.3%, 15.5%, 17.9% (Python confirms all four).
Premium to all REITs: 16.2%, 18.8%, 12.7%, 17.1% (Python confirms).
The premium is defensible: defensive necessity-retail tenants, supply-constrained DC market, lower leverage (40.5% versus 47.1%), better coverage, steadier growth; the counterargument is less upside if peers recover faster (V8 p.141, p.142).
Context: CSC's own historical P/FFO range is 9x to 19x, and its CAPM required return is $4.0\% + 0.80 \times 5.0\% = 8.0\%$ (V8 p.142). ^ex-08-03-6

**Knowledge check Q1: expertise required** (V8 p.146)
Which asset needs the most investor real estate expertise: an REOC share, an equity REIT share, or a direct single-property investment?
C, the direct investment: public vehicles supply professional management and board oversight, so shareholders need far less property expertise. ^ex-08-03-7

**Knowledge check Q2: operating and financial flexibility** (V8 p.146)
A, the REOC: it can invest in any real estate activity, retain all income, and use any capital structure; REITs face income, asset, and payout restrictions; a direct single property is illiquid and indivisible, limiting flexibility. ^ex-08-03-8

**Knowledge check Q3: broadest diversification** (V8 p.146, p.147)
C, the mixed office-and-retail company across urban and suburban markets: two property types and two market types.
A (Hong Kong SAR apartments) is one asset type in one market; B (big-city offices) is one asset type whose markets co-move through global trade and finance exposure.
Alternative: several pure-play companies in non-overlapping regions and types can also diversify. ^ex-08-03-9

**Knowledge check Q4: REIT advantage over direct ownership** (V8 p.147)
A, diversification of property holdings.
B fails because REITs face activity restrictions, and C fails because public trading imports stock market co-movement, reducing overall-portfolio diversification versus private real estate. ^ex-08-03-10

**Knowledge checks Q5 and Q6: matching investors to vehicles** (V8 p.147)
Investor A (liquidity objective): REOC and REIT shares, because they trade on exchanges; direct property does not.
Investor B (maximum growth): REOC or direct investment, because both reinvest freely and can develop; REIT payout rules cap retained earnings and thus growth.
Caveats: thinly floated listed shares may not deliver the promised liquidity, and management quality matters as much as the wrapper. ^ex-08-03-11

**Knowledge check Q7: best measure of current economic return** (V8 p.148)
B, AFFO: it deducts non-cash rent, maintenance capex, and leasing costs from FFO.
FFO ignores those costs; net income also carries non-economic depreciation. ^ex-08-03-12

**Knowledge check Q8: NAVPS from NOI and a cap rate** (V8 p.148)
NOI $115 million, book value of properties $1,005 million, market value of debt $505 million, cap rate 7%, 100 million shares.
Real estate value: $115/0.07 = \$1{,}642.857$ million (Python: 1,642.857).
NAV: $1{,}642.857 - 505 = 1{,}137.857$; NAVPS $= 1{,}137.857/100 = \$11.38$ (B).
A ($10.05) is book assets per share, $1{,}005/100$, ignoring market values and debt; C ($16.42) is the capitalized real estate per share, $1{,}642.857/100$, forgetting the liabilities. ^ex-08-03-13

**Knowledge check Q9: what lowers estimated NAVPS** (V8 p.148, p.149)
A, a higher capitalization rate: value = NOI/cap rate, so NAV falls as the cap rate rises.
B raises NOI and therefore NAV; C, deferred tax liabilities, are soft items excluded from the NAV calculation entirely. ^ex-08-03-14

**Knowledge check Q10: cap rate increase** (V8 p.149)
C, estimated NAV falls: the cap rate maps NOI to market value, and NAV inherits the markdown.
A is unrelated (cost of debt is set by credit markets), and B confuses the cap rate with the income forecast: NOI comes from income growth, not from the cap rate. ^ex-08-03-15

**Knowledge check Q11: from AFFO back to FFO per share** (V8 p.149)
Non-cash rent 207,430; depreciation 611,900; recurring capex and leasing commissions 550,750; AFFO 3,320,000; AFFO/share 3.32.
Shares: $3{,}320{,}000/3.32 = 1{,}000{,}000$.
FFO reverses the AFFO deductions: $3{,}320{,}000 + 207{,}430 + 550{,}750 = 4{,}078{,}180$ (Python confirms); per share $\approx 4.08$ (B).
A ($3.93) adds depreciation instead: $3{,}320{,}000 + 611{,}900 = 3{,}931{,}900$.
C ($4.48) adds depreciation and capex, $3{,}320{,}000 + 611{,}900 + 550{,}750 = 4{,}482{,}650$ (Python: 4.4827 per share); the curriculum's wording for C says depreciation plus both add-backs, which would give 4.69, so the printed option is best reproduced as depreciation plus capex; either way the error is letting depreciation into an AFFO-to-FFO bridge where it does not belong. ^ex-08-03-16

**Knowledge check Q12: what data compilers do not gather** (V8 p.150)
B, AFFO: no universally accepted computation method and inconsistent corporate reporting stop Bloomberg and Refinitiv from compiling it; FFO is standard in the United States and NAV in Europe and Asia. ^ex-08-03-17

**Knowledge check Q13: a downturn and CSC's valuation** (V8 p.150)
C is the least likely outcome: NAV gets less useful in a weak, illiquid market because few observable transactions make cap rates subjective.
A and B are likely: multiples would compress marketwide, but investors would pay a relative premium for CSC's stability, so its multiples would sit above peers. ^ex-08-03-18

**Knowledge check Q14: land and relative multiples** (V8 p.150)
C: land held for development contributes no FFO or AFFO but has value and future growth potential, so CSC deserves a higher multiple than no-land peers, not a lower one or no adjustment. ^ex-08-03-19

**Knowledge check Q15: rates rise 200 bps, buyers demand higher cap rates** (V8 p.150, p.151)
B: NAV falls, because estimated real estate value falls when the analyst raises the cap rate 100 to 200 bps.
A has the sign backward; C is wrong because the NAV effect flows through asset values regardless of CSC's near-term debt maturities. ^ex-08-03-20

**Knowledge check Q16: land bought 15 years ago at one-third of today's value** (V8 p.151)
B: mark the land to today's value and raise NAV; NAV is a market-value construct, not book (C wrong).
A is wrong because the cap rate prices the income-producing portfolio only and has nothing to do with non-income-producing land. ^ex-08-03-21

**Knowledge check Q17: zoning allows new supply, long-term growth falls 0.5%** (V8 p.151)
A: a lower growth rate shrinks every projected dividend and the terminal value, so the DDM present value decreases. ^ex-08-03-22

**Knowledge check Q18: same P/NAV, different cap rates, who has higher P/FFO** (V8 p.151, p.152)
REIT A (P/NAV 100%, 6% cap) versus REIT B (P/NAV 99%, 8% cap), similar portfolio values, interest, and overhead.
A: if each portfolio is worth 100, REIT A generates 6 of NOI and REIT B generates 8; with similar interest and overhead, A's FFO is lower on the same price, so its P/FFO is higher.
C ignores that a lower cap rate means less income per unit of value; the near-identical P/NAV is exactly what makes the FFO difference decisive. ^ex-08-03-23

**Synthesis: CSC's acquisition arithmetic** (V8 p.141)
CSC bought three centers for $111.2 million at a 6.75% first-year return versus market cap rates of 6.00 to 6.25%: expected NOI $= 111.2 \times 0.0675 = \$7.51$ million (Python: 7.506), funded with a $54.6 million 6% mortgage, 1 million new shares, and cash.
Buying below-market (higher cap rate) plus lease-up potential is how a REIT creates value despite the payout constraint; the NAVPS build in walk 1 shows why mid-year deals need the half-year adjustment: only half the 7.5 million sits in last-12-month NOI. ^ex-08-03-24

## Item-set patterns

> [!warning] Trap 1: the FFO walk with a gain instead of a loss
> The vignette gives net income, D&A, and a gain on sale (sometimes hidden inside "other income").
> Correct: FFO = net income + D&A - gains + losses + impairments; Baldwin's $2,162 gain is subtracted, not added (V8 p.132, p.161).
> Distractors add the gain (inflating FFO) or skip it entirely; both appear as priced options in Practice Problem 15.

> [!warning] Trap 2: depreciation sneaking into the AFFO bridge
> Given AFFO and asked for FFO (or vice versa), the exhibit plants a depreciation line it does not need.
> Correct: FFO = AFFO + non-cash rent + recurring capex; depreciation belongs only in the net-income-to-FFO leg (V8 p.132, p.149).
> Distractors add depreciation to AFFO (knowledge check Q11 option A) or subtract adjustments that should be added (Practice Problem 4 options A and C).

> [!warning] Trap 3: shares outstanding hidden in per-share data
> No share count is given, only a total and its per-share figure.
> Correct: shares = AFFO / AFFO per share (for example 4,000,000/5.00 = 800,000), then convert the answer to per share before applying price (V8 p.160).
> The distractor divides by the wrong total or applies the multiple to the aggregate figure.

> [!warning] Trap 4: cap rate direction and the soft-liability decoy
> A rate shock or a deferred tax liability is dropped into an NAV question.
> Correct: NAV moves inversely with the cap rate and is unaffected by deferred taxes, goodwill, and deferred financing costs, which are excluded as non-economic (V8 p.128, p.148, p.149).
> Distractors treat DTLs as deductible debt or claim higher cap rates raise value through "higher income".

> [!warning] Trap 5: NAVPS distractors are always the partial builds
> Every NAVPS item set prices the wrong intermediate lines as options.
> Correct: capitalize forward cash NOI, add other tangible assets, subtract debt and hard liabilities, divide by shares (V8 p.129).
> Distractors: book assets per share (no marking to market, no debt), capitalized real estate per share (no debt), or NAV without the cash and receivables add (knowledge check Q8, Practice Problem 6).

> [!warning] Trap 6: terminal value timing in the two-step DDM
> The model gives explicit dividends through year $n$ and long-run growth after.
> Correct: terminal value $= D_{n+1}/(r-g)$ sits at the end of year $n$; add it to $D_n$ and discount both $n$ periods (Baldwin: $(1.06 + 31.71)/1.085^2$) (V8 p.163).
> Distractors discount the terminal value an extra year, build $D_{n+1}$ with the wrong growth rate, or use $D_n$ in the Gordon numerator.

> [!warning] Trap 7: which multiple with which cash flow
> The exhibit supplies both FFO and AFFO plus both sector multiples.
> Correct: pair P/FFO with FFO per share and P/AFFO with AFFO per share; AFFO = FFO - non-cash rent - recurring capex first if only FFO is given (V8 p.155, p.161, p.162).
> Distractors cross-multiply (AFFO times the P/FFO multiple gives Practice Problem 7's option A) or skip the AFFO conversion (option C of Practice Problem 9).

> [!warning] Trap 8: "best measure" wording
> One question asks for the best measure of current economic return, another for the most compiled estimate, another for the primary European metric.
> Correct: AFFO for economic return, FFO for availability of estimates, NAV (price-to-NAV) for Europe and Asia (V8 p.126, p.134, p.135, p.150).
> The distractor is always the right answer to a different one of these three questions.

> [!warning] Trap 9: matching property subtype to its economic driver
> A REIT's subtype is disclosed and the question asks for the biggest risk or the resilience claim.
> Correct: storage fears easy entry and overbuilding; health care is recession-resistant but exposed to demographics and government funding; necessity retail is defensive with zoning-limited supply; hotels are cyclical with no leases; apartments carry less cash flow variability than hotels (V8 p.125, p.133, p.141, p.162).
> Distractors assign retail metrics (tenant sales per square foot) or obsolescence to a storage REIT, or claim recessions hurt health care REITs most.

> [!warning] Trap 10: public versus private advantage swaps
> A statement list mixes advantages of each vehicle.
> Correct: liquidity, low minimums, transparency, single taxation, professional management belong to public REITs; control, strategy freedom, illiquidity premium, depreciation tax deferral belong to private; REITs still trade with high short-run equity correlation and can sit below NAV (V8 p.145).
> Distractors credit REITs with control or private funds with liquidity, or claim REIT diversification extends to the overall portfolio level (it is diluted by stock market co-movement) (V8 p.126).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM03-Investments-in-Real-Estate-through-Publicly-Traded-Securities-Practice-Problems]]

## Cross-links

- [[LM02-Overview-of-Types-of-Real-Estate-Investment]]: supplies the raw material this module securitizes, property subtypes and their economic value drivers, lease structures, appraisal methods, and the cap rate mechanics that NAV borrows wholesale.
- [[LM04-Market-Based-Valuation-Price-and-Enterprise-Value-Multiples]]: P/FFO and P/AFFO are sector-specific price multiples; the peer-comparison logic, the justified-premium reasoning, and the EV/EBITDA leverage neutrality all come from the equity multiples toolkit.
- [[LM03-Free-Cash-Flow-Valuation]]: the two-step DDM with a Gordon terminal value and the CAPM discount rate are the equity DCF machinery applied to REIT dividends; AFFO plays the role sustainable free cash flow plays there.

## Self-test

Vignette for Q1 to Q6: Meridian Logistics REIT owns warehouse properties.
Last-12-month NOI is $180.0 million, which includes $6.0 million of non-cash straight-line rent; a mid-year acquisition requires a $3.0 million adjustment for its full-year impact; cash NOI is expected to grow 2.0% over the next 12 months.
Comparable transactions support a 6.5% cap rate.
Other balance sheet items (millions): cash $40; land held for development $25; accounts receivable $15; goodwill $30; total debt $900; deferred tax liabilities $45; other hard liabilities $60; shares outstanding 50 million.
Year results (millions): net income $95; depreciation and amortization $70; gain on sale of properties $10; real estate impairment $5; non-cash rent $6; recurring maintenance capex and leasing costs $22.
Sector multiples: P/FFO 13.0x, P/AFFO 15.5x; Meridian trades at $36.00; risk-free rate 4.0%, beta 0.90, market risk premium 5.0%; expected DPS $1.80 next year, growing 5.0% in years 2 and 3 and 3.5% thereafter.

> [!question] Q1
> Meridian's NAVPS is closest to:
> A. $35.94.
> B. $37.65.
> C. $37.95.

> [!question] Q2
> Meridian's FFO per share is closest to:
> A. $3.00.
> B. $3.20.
> C. $3.60.

> [!question] Q3
> Meridian's AFFO per share is closest to:
> A. $2.64.
> B. $2.76.
> C. $2.88.

> [!question] Q4
> Using the sector P/AFFO multiple, Meridian's value per share is closest to:
> A. $34.32.
> B. $40.92.
> C. $49.60.

> [!question] Q5
> Using a two-step dividend discount model, Meridian's intrinsic value per share is closest to:
> A. $34.46.
> B. $35.89.
> C. $36.98.

> [!question] Q6
> At the $36.00 price, Meridian's implied cap rate is closest to:
> A. 6.54%.
> B. 6.74%.
> C. 10.03%.

> [!question] Q7
> A European property company earns 55% of its income from third-party property management and brokerage and develops condominiums for sale.
> The company is most likely organized as:
> A. an equity REIT, provided it distributes 90% of taxable income.
> B. a REOC, because its activities would not satisfy REIT qualification tests.
> C. a mortgage REIT, because development is a lending activity.

> [!question] Q8
> A REIT discloses that rental revenue includes $12 million of straight-line rent in excess of cash rent collected, reflecting contractual step-ups in long leases.
> Relative to a REIT with identical FFO and no step-up leases, this REIT's AFFO is most likely:
> A. lower, because the non-cash rent is deducted from FFO.
> B. higher, because future contractual rents are locked in.
> C. the same, because straight-lining affects only the balance sheet.

> [!question] Q9
> An analyst notes that every REIT in a sector trades at a discount to NAV, and a client concludes the whole sector must be bought.
> The best counterargument is that:
> A. NAV discounts mean managements are adding value, so discounts persist.
> B. NAV is then better used relatively, selling the smallest discounts and buying the largest, since sector-wide gaps can persist until corporate actions close them.
> C. NAV estimates are always more reliable than market prices.

> [!question] Q10
> An income-focused taxable investor wants liquid exposure and minimal entity-level taxation; a family office wants merchant development profits and maximum reinvestment.
> The best pairing is:
> A. investor: public REIT; family office: private vehicle or REOC.
> B. investor: REOC; family office: public REIT.
> C. investor: CMBS; family office: public REIT.

> [!success]- Answer key
> Q1: C.
> Cash NOI $= 180.0 - 6.0 + 3.0 = 177.0$; forward NOI $= 177.0 \times 1.02 = 180.54$; real estate $= 180.54/0.065 = 2{,}777.5$; gross assets $= 2{,}777.5 + 40 + 25 + 15 = 2{,}857.5$ (goodwill excluded); NAV $= 2{,}857.5 - 900 - 60 = 1{,}897.5$ (DTL excluded); NAVPS $= 1{,}897.5/50 = \$37.95$ (Python: 37.9508).
> B (37.65) wrongly includes goodwill as an asset and the DTL as a liability; A (35.94) forgets both the growth year and the acquisition adjustment (Python: 35.94).
> Q2: B.
> FFO $= 95 + 70 - 10 + 5 = 160$; per share $160/50 = \$3.20$ (Python confirms).
> C (3.60) adds the gain instead of subtracting; A (3.00) subtracts the impairment instead of adding it back.
> Q3: A.
> AFFO $= 160 - 6 - 22 = 132$; per share $132/50 = \$2.64$ (Python confirms).
> B (2.76) forgets the non-cash rent; C (2.88) adds the non-cash rent instead of subtracting.
> Q4: B.
> $2.64 \times 15.5 = \$40.92$ (Python confirms); against the $36.00 price, Meridian trades below its sector-implied value.
> A (34.32) uses the P/FFO multiple 13.0x on AFFO; C (49.60) uses 15.5x on FFO per share ($3.20 \times 15.5$), both cross-pairings.
> Q5: C.
> $r = 4.0\% + 0.90 \times 5.0\% = 8.5\%$; $D_1 = 1.80$, $D_2 = 1.89$, $D_3 = 1.9845$, $D_4 = 1.9845 \times 1.035 = 2.0540$; terminal at end of Year 3 $= 2.0540/(0.085 - 0.035) = 41.08$; $V_0 = 1.80/1.085 + 1.89/1.085^2 + (1.9845 + 41.08)/1.085^3 = \$36.98$ (Python: 36.9793).
> A (34.46) discounts the terminal value four periods (Python: 34.4598); B (35.89) uses $D_3$ instead of $D_4$ in the Gordon numerator (Python: 35.8918).
> Q6: B.
> Implied real estate value $= 36.00 \times 50 + 900 + 60 - 40 - 25 - 15 = 2{,}680$; implied cap rate $= 180.54/2{,}680 = 6.74\%$ (Python: 6.7366%).
> A (6.54%) forgets to strip the non-real-estate assets (Python: 6.5413%); C (10.03%) divides NOI by equity market cap alone, ignoring debt (Python: 10.03%).
> Q7: B.
> Non-qualifying service income (management, brokerage) and for-sale development are exactly the activities that push a business into REOC form; A fails because payout alone cannot cure failed income and activity tests; C misreads development as lending.
> Q8: A.
> AFFO subtracts non-cash straight-line rent from FFO, so booking rent ahead of cash lowers AFFO; B confuses contract quality with the accounting adjustment; C is wrong because straight-lining inflates current revenue and FFO, which AFFO corrects.
> Q9: B.
> Sector-wide premiums and discounts can persist until the gap widens enough for market forces (going private, asset sales, IPO exits) to close it, so NAV works better as a relative screen; A inverts the premium logic (value-adding management justifies premiums, not discounts); C overstates NAV, which turns subjective in illiquid markets.
> Q10: A.
> The taxable income seeker wants the REIT's liquidity, high payout, and single taxation; the family office wants merchant development and full reinvestment, which REIT rules restrict and private vehicles or REOCs allow; B reverses the tax logic; C hands the equity investor a debt instrument.

## Flashcards

#flashcards/cfa-l2/08-Alternative-Investments/lm03

Principal types of publicly traded real estate securities::REITs, REOCs, and mortgage-backed securities (RMBS and CMBS) (V8 p.123).
Equity REIT vs mortgage REIT::Equity REITs own real estate; mortgage REITs make or invest in loans secured by real estate (V8 p.123).
Three typical REIT qualification tests::Distribute 90 to 100 percent of taxable earnings, hold at least 75 percent of assets in real estate, earn at least 75 percent of income from rents or mortgage interest (V8 p.123, p.124).
Source of the REIT tax advantage::Dividends paid are deductible from income, effectively exempting the REIT from corporate income tax, so shareholders face single taxation (V8 p.123, p.125).
US 5/50 rule::A REIT needs at least 100 shareholders, and no five or fewer shareholders may own more than 50 percent of shares (V8 p.124).
When is a business organized as a REOC instead of a REIT?::No REIT regime in its country, large-scale for-sale development, or non-qualifying services such as brokerage and third-party management (V8 p.123).
Internally vs externally managed REITs::Self-managed REITs have employee executives under a shareholder-elected board and fewer conflicts; external managers charge asset-based fees and may push affiliate services (V8 p.124).
Taxable REIT subsidiary (TRS)::A subsidiary that pays income tax on earnings from non-REIT-qualifying activities such as merchant development or third-party management (V8 p.126).
Four disadvantages of REITs vs private real estate::Lack of retained earnings, regulatory costs, diluted portfolio diversification from stock market co-movement, and limits on asset types owned (V8 p.126).
Where are REIT structures most dominant?::North America (98 percent of listed real estate by value) versus 41 percent in Europe and 49 percent in Asia Pacific (V8 p.125).
NAVPS formula::(Market value of assets minus market value of liabilities) divided by shares outstanding (V8 p.128).
NOI formula (REIT analysis)::Gross rental revenue minus estimated vacancy and collection loss minus operating expenses, before interest, income taxes, and D&A (V8 p.128).
Why is BVPS a poor REIT value measure?::Historical cost accounting understates long-held appreciating assets and overstates depreciation (V8 p.127, p.128).
IFRS investment property options::Cost model or fair value model; fair value changes hit net income, the choice applies to all investment property, and disclosure of fair value is required even under cost (V8 p.127).
Items excluded from NAV as soft or non-economic::Goodwill, deferred financing expenses, deferred tax assets and liabilities (V8 p.128, p.129).
Cash NOI adjustments before capitalizing::Remove non-cash straight-line rent and add the full-year impact of mid-year acquisitions, then apply expected growth (V8 p.129).
Value of operating real estate::{{Expected next-12-month cash NOI divided by the cap rate}} (V8 p.129).
Cap rate definition::NOI divided by total property value; the required current-income return from recent comparable transactions (V8 p.129, p.130).
Three methods used to calculate NAV::Cap rate approach on NOI, value per square foot on the portfolio, and appraised values from financial statements (V8 p.130).
Effect of a cap rate increase on NAV::Estimated real estate value and NAV both fall; NOI itself is unchanged (V8 p.148, p.149).
Implied cap rate::Solve the NAV model backward from the current share price to find the cap rate the market is paying (V8 p.132).
Why can shares trade at persistent premiums or discounts to NAV?::Stock investors are forward looking while appraisals lag, management can add or subtract value, and gaps persist until corporate actions close them (V8 p.127, p.131).
Two reasons well-run REITs should trade above NAVPS::Daily liquidity warrants a lower required return than private ownership, and public markets attract above-average management (V8 p.131).
When does NAV become subjective?::Illiquid markets with few transactions, portfolios of hundreds of properties, and odd assets such as raw land, single-use buildings, service businesses, joint ventures (V8 p.131).
NAV used relatively::Buy the smallest premium (or sell the smallest discount) when the whole sector trades on one side of NAV (V8 p.131, p.132).
FFO formula (REIT analysis)::Net income plus depreciation and amortization plus losses minus gains on sales of real property, plus real estate impairments (V8 p.132, p.134).
Why add depreciation back in FFO?::Real estate tends to hold or gain value, so accounting depreciation does not reflect economic reality (V8 p.134).
Why strip gains and losses on sales from FFO?::They are not sustainable, normal operating income (V8 p.134).
AFFO formula::{{FFO minus non-cash (straight-line) rent minus recurring maintenance-type capex and leasing costs}} (V8 p.132, p.134).
Other names for AFFO::Funds available for distribution (FAD) or cash available for distribution (V8 p.134).
Straight-line rent adjustment::The difference between average contractual rent booked as revenue and the cash rent actually received in the period (V8 p.134).
AFFO vs FFO trade-off::AFFO is the better economic income and dividend-capacity measure but is noisier; FFO is standardized (Nareit) and widely compiled (V8 p.134, p.135).
Which REIT estimate do data compilers not gather, and why?::AFFO, because there is no universally accepted methodology and corporate reporting is inconsistent (V8 p.135, p.150).
Three drivers of P/FFO and P/AFFO multiples::Expected FFO/AFFO growth, risk of the underlying real estate, and leverage and access to capital (V8 p.133).
Effect of leverage on P/FFO::Higher leverage raises required return and lowers the multiple; FFO is levered income (V8 p.133).
Why use EV/EBITDA for REITs?::It is leverage neutral, and EBITDA/EV approximates the cap rate formula NOI over value (V8 p.133).
Apartment vs hotel REIT multiples::Apartments have less cash flow variability, so they trade at higher multiples than hotel REITs (V8 p.133).
Best measure of a REIT's current economic return::AFFO, because it deducts non-cash rent, maintenance capex, and leasing costs (V8 p.148).
Preferred REIT metric by region::P/FFO in the United States, price-to-NAV in Europe and Asia (V8 p.126, p.132).
Which valuation measure suits REITs because active private markets exist for the assets?::Net asset value (V8 p.122).
Why do DDM models fit REITs?::Payout requirements make dividends large and forecastable; two- or three-step models with a Gordon terminal value are standard (V8 p.122, p.123).
Two-step DDM terminal value timing::Terminal value equals next year's dividend over (r minus g), dated at the end of the last forecast year and discounted that many periods (V8 p.163).
30-second drill: NOI 115, cap rate 7 percent, debt 505, 100 million shares; NAVPS?::115/0.07 = 1,642.9; minus 505 = 1,137.9; divided by 100 = 11.38 (V8 p.148).
30-second drill: AFFO 4.0m, AFFO/share 5.00, non-cash rent 0.215m, recurring capex 0.7m, price 80; P/FFO?::Shares 800k; FFO = 4.915m; FFO/share 6.14; 80/6.14 = 13.0x (V8 p.160).
30-second drill: NI 142,187, D&A 90,409, gains 2,162, shares 121,944, P/FFO 11.5x; price?::FFO 230,434; per share 1.89; times 11.5 = 21.73 (V8 p.162).
Trap: given AFFO, find FFO::Add back both non-cash rent and recurring capex; never add depreciation, which belongs only in the net-income-to-FFO leg (V8 p.149).
Storage REIT signature risk::Low barriers to entry invite overbuilding by new competitive facilities (V8 p.162).
Health care REIT exposures::Resistant to recessions; exposed to demographics and government funding of health care (V8 p.162).
Shopping center defensiveness::Necessity tenants (grocery, drug) plus strict zoning that limits new supply (V8 p.141).
REIT payout requirement base::Taxable income after depreciation, so cash dividends can far exceed the required minimum while still complying (V8 p.142).
Advantages unique to public real estate::Liquidity, low minimums, limited liability, transparency, regulation, professional management, tax-efficient REIT structure (V8 p.145).
Advantages unique to private real estate::Control, strategy freedom including merchant development, illiquidity premium, accelerated depreciation tax benefits, low short-run equity correlation (V8 p.145).
How do public-private valuation gaps close?::Companies below NAV go private or sell to private funds; at high values, public companies sell assets and private funds exit via IPO (V8 p.144).

## Common mistakes

1. Adding gains on property sales to net income in the FFO walk instead of subtracting them (Baldwin's $2,162 gain hides in other income) (V8 p.132, p.162).
2. Letting depreciation into the AFFO-to-FFO bridge; only non-cash rent and recurring capex reverse, and depreciation belongs to the net income leg (V8 p.149).
3. Subtracting the straight-line rent and capex adjustments when reconstructing FFO from AFFO (or adding them when going the other way), producing the 14.3x and 20.7x distractors of Practice Problem 4 (V8 p.160).
4. Deducting deferred tax liabilities, goodwill, or deferred financing costs in an NAV build; soft items are excluded (V8 p.128, p.149).
5. Forgetting to subtract debt (or to add cash and receivables) after capitalizing NOI, the classic wrong options in knowledge check Q8 and Practice Problem 6 (V8 p.148, p.161).
6. Capitalizing raw last-12-month NOI without removing non-cash rent, adding the acquisition full-year impact, and applying next-year growth (V8 p.129).
7. Using the cost of equity as the cap rate (Practice Problem 6's $51.26 distractor); the cap rate comes from property transactions, not CAPM (V8 p.130, p.161).
8. Mis-timing the DDM terminal value: it dates to the end of the last explicit forecast year, uses the following year's dividend, and is discounted that many periods, not one more (V8 p.161, p.163).
9. Crossing multiples and measures: P/FFO with AFFO per share or P/AFFO with FFO per share (V8 p.161, p.162).
10. Claiming a discount to NAVPS signals overvaluation, or that below-NAV trading helps a REIT raise capital; it signals potential undervaluation and impedes non-dilutive issuance (V8 p.127).
11. Ranking FFO above AFFO as an economic return measure; AFFO wins on concept, FFO on standardization and availability (V8 p.134, p.135).
12. Assigning the wrong subtype risk: overbuilding belongs to storage, demographics and government funding to health care, tenant sales to retail (V8 p.162).
13. Crediting REITs with overall-portfolio diversification or operating flexibility; stock market co-movement dilutes the former, and qualification rules deny the latter (V8 p.126, p.147).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "08-03" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
