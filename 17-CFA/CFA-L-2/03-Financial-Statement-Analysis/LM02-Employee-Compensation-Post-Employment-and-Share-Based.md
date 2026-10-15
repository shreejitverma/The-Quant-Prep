---
type: cfa-lm
topic: "Financial Statement Analysis"
topic_code: "03"
topic_slug: "03-Financial-Statement-Analysis"
volume: 3
lm: 2
title: "Employee Compensation: Post-Employment and Share-Based"
pages: "63-113"
weight_band: "10-15%"
difficulty: 4
los_count: 5
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/financial-statement-analysis]
---

# LM2: Employee Compensation: Post-Employment and Share-Based

Difficulty 4 of 5: the arithmetic is light (straight-line vesting, treasury stock method, beginning balance times a rate) but two accounting regimes run in parallel, every assumption has a direction effect on three different statements, and the vignettes are built from note disclosures where the trap is which line goes where (P&L, OCI, cash flow, equity).

## LOS map

- **contrast** types of employee compensation (V3 p.65) ^los-03-02-a
    - Examiner asks: given a compensation arrangement, classify it (short-term, long-term, termination, share-based, post-employment, DC versus DB) and state the measurement basis and the balance sheet account that takes the offsetting entry.
- **explain** how share-based compensation affects the financial statements (V3 p.69) ^los-03-02-b
    - Examiner asks: from an RSU or option grant table compute the annual expense from grant-date fair value over the vesting period, then trace the equity, cash flow, tax windfall, and diluted share effects, and say what changes (nothing) when the share price moves after the grant.
- **explain** how to forecast share-based compensation expense and shares outstanding in a financial statement model and their use in valuation (V3 p.84) ^los-03-02-c
    - Examiner asks: forecast SBC as a percentage of revenue, convert the expense to shares issued by dividing by grant-date fair value, roll basic shares forward, and decide whether to deduct SBC from free cash flow or inflate the share count.
- **explain** how post-employment benefits affect the financial statements (V3 p.89) ^los-03-02-d
    - Examiner asks: from a pension note compute funded status, the IFRS P&L amount (service cost plus net interest) and OCI remeasurement, or the US GAAP five-component expense, and identify the cash flow (contributions) and balance sheet (net pension asset or liability) amounts.
- **explain** financial modeling and valuation considerations for post-employment benefits (V3 p.100) ^los-03-02-e
    - Examiner asks: which DB items belong in a DCF (service cost expensed, net interest excluded, net pension liability deducted from EV as debt, surplus ignored) and how a change in discount rate, salary growth, or expected return moves the obligation, the expense, and cash flow.

## Core intuition

Every form of pay in this module obeys one rule: recognise the fair value of compensation as an expense in the period the employee provides the service, and put the offsetting entry somewhere on the balance sheet until the employer settles (V3 p.66).
Salaries settle within two weeks, so expense, liability, and cash all sit in the same period and nobody argues.
Share-based compensation and defined benefit pensions settle years or decades later at an uncertain amount, so the expense has to be estimated, the offsetting entry lingers, and the gap between expense and cash is where the analysis lives (V3 p.63, p.68).

![[Pension-Cost-Components.excalidraw]]

> [!abstract] Idea 1: the offsetting entry tells you the economics
> Short-term benefits credit a liability that cash later extinguishes; share-based awards credit equity because shares, not cash, settle them; DB pensions credit or debit a net pension liability or asset equal to the funded status (V3 p.67, p.70, p.91).
> Follow the credit and you know what the cash flow statement will show: operating outflow for salaries and plan contributions, nothing for equity-settled awards, and a financing inflow only when options are exercised (V3 p.67, p.72, p.74, p.94).

Start with the five categories in Exhibit 1: short-term benefits (paid within 12 months), long-term benefits, termination benefits, share-based compensation, and post-employment benefits, distinguished by the delay between service and payment and by the form of payment (V3 p.65, p.66).
Short-term benefits are the bulk of cost and are measured undiscounted; when the employee makes inventory the cost is capitalised into inventories and only reaches the income statement as cost of sales when the goods are sold (V3 p.67).
Termination benefits are the one type that often appears as a discrete line such as restructuring charges; everything else is folded into the functional expense line of the employee's role (V3 p.68).

Share-based compensation changes three things relative to salaries.
The credit goes to equity (a share-based compensation reserve), vesting runs over years rather than weeks, and the amount is fair value measured once, at the grant date (V3 p.70).
That last point is the source of half the exam questions.
Once granted, an award's expense is locked: a 25% rise in the share price after the grant leaves the expense for that grant unchanged, and only future grants feel the higher price (V3 p.70, p.73).
An RSU's grant-date fair value is simply the share price, adjusted down for dividends the holder will not receive (V3 p.71).
An option's grant-date fair value must be modelled, typically with Black-Scholes or a binomial model, and the inputs matter: higher volatility, longer expected life, higher risk-free rate, and lower dividend yield all raise the value and therefore the expense (V3 p.73, p.74).
Volatility is the most subjective input and the one management can lean on (V3 p.74).
Because options are usually granted at the money their intrinsic value is zero, which is exactly why pre-2005 intrinsic value accounting produced zero expense and why fair value expensing was so contested (V3 p.75, p.76).

Settlement differs too.
RSUs convert to shares automatically at vesting; the only entry is a transfer inside equity from the reserve to common stock and paid-in capital (V3 p.74).
Options settle only if the employee chooses to exercise, which happens when the share price is above the strike; the company then records a financing cash inflow of options exercised times strike, and again a transfer within equity (V3 p.74, p.75).
The share price at exercise never touches the accounts; it only decides how many options get exercised (V3 p.75).

> [!abstract] Idea 2: grant-date fair value is fixed for the books, but the tax deduction and the share count float with the market
> The tax return deducts the settlement-date value (share price for RSUs, intrinsic value for options), so a rising share price creates a tax windfall and a falling one a shortfall; IFRS books these in equity, US GAAP runs them through income tax expense (V3 p.77, p.78).
> Diluted shares use the treasury stock method, where assumed proceeds (fixed at grant-date values) are divided by a floating average share price, so a falling price makes RSUs less dilutive and a rising price more dilutive (V3 p.79 to p.81).

The tax point has a practical consequence for US GAAP reporters: the effective tax rate becomes a function of the share price.
Meta's effective rate was 16.7% in 2021 with 2.2 points of windfall, then jumped toward the 21% statutory rate as the share price fell 72% in 2022 (V3 p.79).
An analyst should therefore never extrapolate an effective tax rate that contains a windfall, and should expect IFRS reporters to show more stable effective rates because their windfalls bypass earnings (V3 p.79).

On share count, basic shares rise only when awards settle (V3 p.79).
Unsettled awards enter diluted shares through the treasury stock method: add the awards, then subtract the shares that could be repurchased at the average price with the assumed proceeds, where assumed proceeds are cash from exercise (strike times options, zero for RSUs) plus the average unrecognised share-based compensation expense (V3 p.79, p.80).
The unrecognised expense is counted as proceeds because settling the awards today would avoid that future expense (V3 p.80).
The mechanics produce four rules: in-the-money options are dilutive, out-of-the-money or at-the-money options are anti-dilutive, RSUs are dilutive unless the average price has fallen far below the grant price, and a rapid rise in the share price raises dilution because fewer shares can be repurchased (V3 p.81).
A loss-making company reports identical basic and diluted shares whatever it has outstanding, because diluted EPS may not exceed basic EPS, so the analyst should add the disclosed anti-dilutive securities back for valuation (V3 p.81, p.82).

For modelling, share-based compensation is normally forecast as a percentage of revenue, separately from the cash operating expenses because it must be added back on the cash flow statement and may have a different driver, particularly for early-stage companies where it falls as a share of revenue with maturity (V3 p.85, p.86).
The offsetting entry in the model is to equity; forget it and the balance sheet is out by exactly the expense (V3 p.85, p.113).
Shares issued from vesting are the expense divided by the grant-date fair value per share, and basic shares roll forward as beginning plus vesting and exercises plus issuances less repurchases (V3 p.87, p.113).
In valuation the curriculum is blunt: ignoring share-based compensation because it is non-cash is wrong, because it transfers value from shareholders to employees and many companies buy back shares to offset it, which makes it behave like cash (V3 p.87, p.88).
The pragmatic fix is to deduct it from free cash flow; the alternative is to inflate the share count for expected dilution, and the two should give the same answer (V3 p.87, p.88, p.113).
Free cash flow multiples flatter heavy users of share-based compensation, as the Company A versus Company B illustration shows, and GAAP and non-GAAP multiples must never be mixed in a peer comparison (V3 p.88).

Now pensions.
A defined contribution plan is a salary-like promise: the employer pays an agreed contribution, expenses it, and is done; the employee bears the investment and actuarial risk (V3 p.89, p.90).
A defined benefit plan promises an amount at retirement, usually a formula of final salary and years of service, so the employer bears the investment risk that plan assets underperform and the actuarial risk that employees live longer, retire earlier, or earn more than assumed (V3 p.89, p.90).
Anything not explicitly DC is accounted for as DB, including other post-employment benefits such as retiree medical care, which are usually unfunded pay-as-you-go plans (V3 p.90, p.91).
Closed plans admit no new members; frozen plans stop accruing benefits for existing members (V3 p.90).

> [!abstract] Idea 3: the balance sheet carries the funded status, and the expense is the accrual change in that funded status split into cost buckets
> Funded status = fair value of plan assets minus pension obligation; negative is a net pension liability, positive a net pension asset, and plans are never netted against each other (V3 p.91, p.92).
> Under IFRS the change in funded status not caused by contributions is the periodic cost: service cost and net interest in profit or loss, remeasurements in OCI (V3 p.93, p.94).
> Contributions are the only cash item, in operating activities; benefit payments reduce assets and obligation equally and never appear on the sponsor's statements (V3 p.94).

Why not just expense the contribution?
Because the contribution is a funding decision, not a cost: an employer can skip contributions for years while employees keep earning benefits and the discount keeps unwinding, both of which raise the obligation (V3 p.93).
So the expense is built from what actually moved the obligation and the assets.
Service cost is the increase in the obligation from another year of service under the benefit formula (current) plus any plan amendment affecting past service (past), computed by an actuary with the projected unit credit method; under IFRS both are operating expenses (V3 p.93).
Net interest is the beginning net pension liability or asset times the discount rate, shown below operating income with financing costs; it nets the interest cost on the obligation against interest income on assets at the same rate (V3 p.94, p.111).
Remeasurement is everything else: the actual return on assets minus the interest income already assumed on them, plus actuarial gains and losses from changed assumptions; IFRS books it in OCI and never recycles it (V3 p.94, p.97).
The discount rate is the yield on investment-grade corporate bonds in the benefit currency, so a decade of low rates is what ballooned GE's deficit from a USD 4 billion surplus to over USD 35 billion and 41% of market capitalisation (V3 p.92, p.93).

US GAAP keeps the same balance sheet and cash flow statement but breaks the income statement differently into five parts: current service cost, gross interest cost on the obligation, expected return on plan assets as an offset, amortisation of past service cost (which first goes to OCI), and amortisation of actuarial gains and losses and asset return differences, most commonly through the corridor (V3 p.96).
Two levers matter for analysis.
The expected return is a management assumption, so a higher assumed return lowers reported expense with no economic change (V3 p.96, p.99).
The corridor defers gains and losses: only the cumulative unrecognised amount above 10% of the larger of the obligation and plan assets is amortised, over the average remaining working life (V3 p.96).
IFRS has no corridor and no expected return; its net interest uses the discount rate on both sides (V3 p.94, p.97).

Assumptions drive everything.
A higher discount rate, lower salary growth, lower inflation, lower life expectancy, and for OPEB a lower healthcare cost trend all shrink the obligation and the expense, so those are the aggressive directions; under US GAAP a higher expected return is a further aggressive lever (V3 p.99).
Shell's sensitivity table gives the scale: a 1% fall in the discount rate raises its obligation by USD 18,954 million, versus a fall of USD 14,599 million for a 1% rise, the asymmetry that convexity produces (V3 p.99).
The discount rate has a subtle second effect: a lower rate raises the obligation and therefore raises the interest cost even though the rate fell, because the larger obligation usually more than offsets the smaller rate except for short-duration plans (V3 p.113).
And the analyst should check internal consistency: salary growth normally rises with inflation, so a lower salary growth assumption alongside higher inflation is a red flag (V3 p.113).

For valuation the treatment is asymmetric.
An underfunded plan is debt: deduct the net pension liability in the bridge from enterprise value to equity value.
An overfunded plan is ignored because plan assets belong to the plan and cannot be paid out to shareholders (V3 p.100).
In the free cash flow itself, leave service cost expensed (it is compensation in lieu of salary even though it is non-cash), but strip out net interest because it is the unwinding of a present value that the EV bridge already deducts in full (V3 p.100, p.101, p.113).
Small, well-funded, frozen plans (net liability under 5% of market capitalisation) can be left unmodelled (V3 p.100).

## Formulas and derivations

**Short-term benefit expense per pay period** (V3 p.67)
$$
\text{Expense per period} = \frac{\text{Annual salary}}{\text{Pay periods per year}} = \frac{82{,}200}{52/2} = 3{,}162
$$
^f-03-02-1

- Measured undiscounted; recognised as the employee provides service with a credit to accrued compensation, settled by cash in operating activities (V3 p.67).
- If the employee manufactures goods the same amount is capitalised into inventories and expensed as cost of sales on sale (V3 p.67).

**Grant-date fair value of an RSU award** (V3 p.71)
$$
FV_{RSU} = N_{RSU} \times P_{grant} \;(\text{less PV of dividends foregone if the RSU does not participate})
$$
^f-03-02-2

- $P_{grant}$: share price on the grant date; the value is fixed and never remeasured for later share price moves (V3 p.70, p.71).
- Reason: an RSU is a claim to one share with no exercise price, so its value is the share less any dividends the holder misses during vesting (V3 p.71).

**Annual share-based compensation expense (straight-line vesting)** (V3 p.72)
$$
\text{Expense}_t = \sum_{\text{grants } g} \frac{N_g \times FV_g}{T_g} \quad \text{for each year } t \text{ inside grant } g\text{'s vesting period}
$$
^f-03-02-3

- $N_g$: awards granted net of expected forfeitures; $FV_g$: grant-date fair value per award; $T_g$: vesting period in years (V3 p.69, p.72).
- Credit is to the share-based compensation reserve in equity; no cash flow, added back under the indirect method (V3 p.70, p.72).
- Reason: the service is rendered evenly over the vesting period, so the fixed grant-date value is spread evenly; overlapping grants stack (V3 p.72).

**Aggregate fair value of an option grant** (V3 p.74)
$$
FV_{options} = N_{options} \times FV_{per\ option} = 25 \text{ million} \times 1{,}288 = 32{,}200 \text{ million JPY}
$$
^f-03-02-4

- $FV_{per\ option}$ comes from an option pricing model at the grant date; intrinsic value is zero for an at-the-money grant so the whole value is time value (V3 p.73, p.74).
- Expensed over the vesting period exactly as in Formula 3 (V3 p.74).

**Option exercise entries** (V3 p.75)
$$
\text{CFF inflow} = N_{exercised} \times K; \qquad \Delta\text{Paid-in capital} = N_{exercised}\,K + \frac{N_{exercised}}{N_{granted}} FV_{options}
$$
^f-03-02-5

- $K$: strike price; the share price at exercise is irrelevant to the amounts booked (V3 p.75).
- The second term is the transfer of the reserve balance attributable to the exercised options from the reserve to paid-in capital (V3 p.75).

**Tax windfall or shortfall on settlement** (V3 p.78, p.112)
$$
\text{Excess tax benefit} = t \times \left(\text{Tax deduction at settlement} - \text{Cumulative SBC expense}\right)
$$
^f-03-02-6

- Tax deduction: settlement-date share price for RSUs, intrinsic value at exercise for options; cumulative expense is at grant-date fair value (V3 p.77).
- Positive is a windfall (settlement price above grant price); negative is a shortfall (V3 p.78).
- IFRS: recognised directly in equity; US GAAP: reduces (windfall) or increases (shortfall) income tax expense on the income statement (V3 p.78).

**Diluted shares outstanding, treasury stock method** (V3 p.79, p.80)
$$
\text{Diluted shares} = \text{Basic shares} + N_{awards} - \frac{\text{Assumed proceeds}}{\bar{P}}
$$
^f-03-02-7

- $N_{awards}$: unvested RSUs or unexercised options judged likely to vest (performance-conditioned awards not yet met are excluded); $\bar{P}$: average share price for the period (V3 p.80).
- If the subtraction is negative for an instrument (assumed repurchases exceed the awards) the instrument is anti-dilutive and excluded (V3 p.81).
- Diluted EPS cannot exceed basic EPS, so a loss-making company reports diluted shares equal to basic shares (V3 p.81).

**Assumed proceeds** (V3 p.80)
$$
\text{Assumed proceeds} = N_{options} \times K + \overline{\text{Unrecognised SBC expense}}
$$
^f-03-02-8

- Cash proceeds are zero for RSUs (V3 p.80).
- The average unrecognised expense is counted because settling today avoids that future expense; it is a proxy for value the company would otherwise still have to deliver (V3 p.80).

**Unrecognised share-based compensation expense** (V3 p.80)
$$
U_t = N_{unvested,t} \times FV_{grant}; \qquad \overline{U} = \frac{U_{t-1} + U_t}{2}
$$
^f-03-02-9

- Based on grant-date fair values, so it is fixed while the average price floats; that is why RSUs become anti-dilutive after a large price fall (V3 p.80, p.81).
- For a single grant vesting straight-line, $U_t$ equals the aggregate fair value less cumulative expense recognised.

> [!tip] Calculator
> Workflow RSUs: unvested 3,028,000, average unrecognised 6,601 million, average price 4,200.
> `6601 ÷ 4200 = × 1000000 =` gives 1,571,667 assumed repurchases; `3028000 - 1571667 =` gives 1,456,333 dilutive shares (V3 p.81).
> Always check the sign: if the repurchase figure exceeds the award count, the answer is zero, not negative.

**Share-based compensation forecast** (V3 p.85)
$$
\text{SBC}_{t+1} = \text{Revenue}_{t+1} \times \frac{\text{SBC}}{\text{Revenue}}\bigg|_{\text{assumed}}
$$
^f-03-02-10

- The ratio can be a historical average, management guidance, or a reversion toward a sector average (V3 p.85).
- Model it as a discrete line so it can be added back in the cash flow statement and credited to equity; cash operating expenses are modelled excluding it (V3 p.85, p.86).

**Basic shares roll-forward** (V3 p.87)
$$
S_{end} = S_{beg} + \text{RSUs vested} + \text{Options exercised} + \text{Other issuances} - \text{Repurchases}
$$
^f-03-02-11

- Grants net of forfeitures and settlements are forecast first, consistent with the expense forecast (V3 p.87).
- Diluted shares are then forecast by adding an assumed dilutive percentage of outstanding awards (V3 p.87).

**Shares issued from vesting of RSUs** (V3 p.113)
$$
\Delta S_{basic} = \frac{\text{SBC expense recognised at vesting}}{FV_{grant\ per\ share}} = \frac{50.6}{46.36} = 1.09 \text{ million}
$$
^f-03-02-12

- Reason: for RSUs vesting and settlement coincide, and the expense on each vesting share is its grant-date fair value, so expense divided by grant-date value is the share count (V3 p.113).
- Trap: dividing by the current market price understates the shares issued when the price has risen (V3 p.107, p.113).

**Free cash flow and share-based compensation** (V3 p.88)
$$
FCF = CFO - \text{Capex}; \qquad FCF_{adj} = CFO - \text{Capex} - \text{SBC}
$$
^f-03-02-13

- Reported FCF excludes SBC because it is non-cash, which flatters FCF margin and P/FCF for heavy users; Company B's P/FCF is 37 versus 83 for identical Company A (V3 p.88).
- In a DCF the pragmatic treatment is to deduct SBC from FCF, or equivalently to increase the share count for expected dilution (V3 p.87, p.88).

**DC plan expense** (V3 p.91)
$$
\text{DC expense} = \text{Contribution rate} \times \text{Salary} = 5\% \times \frac{82{,}200}{26} = 158
$$
^f-03-02-14

- Expense and accrued liability as service vests; cash contribution in operating activities; no plan assets or obligations on the sponsor's balance sheet (V3 p.91).

**Funded status (curriculum Equation 1)** (V3 p.91)
$$
\text{Funded status} = \text{Fair value of plan assets} - \text{Pension obligation}
$$
^f-03-02-15

- Negative: net pension liability (underfunded); positive: net pension asset (overfunded); reported net, but separate plans are not netted with each other (V3 p.92).
- Pension obligation: present value of expected future payments from service to date, discounted at investment-grade corporate bond yields in the benefit currency, gross of assets (V3 p.92).
- Plan assets are the plan's property, legally isolated from the sponsor and unavailable to shareholders (V3 p.92, p.100).

**Pension obligation roll-forward** (V3 p.102)
$$
PBO_{end} = PBO_{beg} + \text{Service cost} + \text{Interest cost} - \text{Benefits paid} \pm \text{Actuarial loss (gain)} + \text{Past service cost}
$$
^f-03-02-16

- Interest cost $= r \times PBO_{beg}$ with $r$ the discount rate (V3 p.96).
- Kensington: $28{,}416 + 228 + 1{,}557 - 1{,}322 + 0 = 28{,}879$ (V3 p.102).

**Plan assets roll-forward** (V3 p.102)
$$
A_{end} = A_{beg} + \text{Actual return} + \text{Contributions} - \text{Benefits paid}
$$
^f-03-02-17

- Benefits paid appear in both roll-forwards with the same sign, so they are neutral to funded status (V3 p.94).
- Actual rate of return $= \text{Actual return} / A_{beg}$, for example $1{,}302 / 23{,}432 = 5.56\%$ (V3 p.111).

**IFRS periodic pension cost** (V3 p.93, p.94)
$$
\text{P\&L} = \text{Service cost}_{current + past} + \text{Net interest expense (income)}; \qquad \text{OCI} = \text{Remeasurements}
$$
^f-03-02-18

- Service cost sits in operating expense by function; net interest sits below operating income with financing costs; remeasurements never reach earnings (V3 p.93, p.94, p.111).
- Total periodic pension cost $=$ P\&L $+$ OCI, for example $228 + 273 - 18 = 483$ (V3 p.102).

**IFRS net interest** (V3 p.94)
$$
\text{Net interest} = r \times \left(PBO_{beg} - A_{beg}\right) = r \times PBO_{beg} - r \times A_{beg}
$$
^f-03-02-19

- Expense when the plan is underfunded, income when overfunded; the same discount rate is applied to both sides (V3 p.94, p.111).
- Kensington: $5.48\% \times 4{,}984 = 273$; the difference from the gross interest cost of 1,557 is the interest income on plan assets, 1,284 (V3 p.102, p.111).

> [!tip] Calculator
> `4984 × .0548 =` gives 273.1; `28416 × .0548 =` gives 1,557.2; `23432 × .0548 =` gives 1,284.1.
> Sign check: negative funded status times the rate is an expense.

**IFRS remeasurement** (V3 p.97)
$$
\text{Remeasurement} = \left[\text{Actual return} - r \times A_{beg}\right] + \text{Actuarial gains} - \text{Actuarial losses}
$$
^f-03-02-20

- The first bracket is the net return on plan assets in excess of the interest income assumed in net interest (V3 p.97).
- Actuarial gains and losses are changes in the obligation from changed assumptions (salary growth, discount rate, mortality); an increase in the obligation is a loss (V3 p.94).
- Workflow 20X8: $50.5 - 20.2 = 30.3$ gain to OCI (V3 p.95).

**US GAAP periodic pension cost in P&L** (V3 p.96)
$$
\text{Pension expense} = SC + r \times PBO_{beg} - \hat{R} \times A_{beg} + \text{Amort. of past service cost} + \text{Amort. of net (gains) losses}
$$
^f-03-02-21

- $SC$: current service cost only; past service cost goes to OCI first and is amortised over the average service life of affected employees (V3 p.96).
- $\hat{R}$: expected long-term rate of return on plan assets, a management assumption (V3 p.96).
- Interest cost is gross and presented with interest expense below operating income (V3 p.96).
- XYZ under US GAAP with no amortisation: $200 + 2{,}940 - 3{,}120 = 20$ (V3 p.111).

**US GAAP difference between actual and expected return** (V3 p.97)
$$
\text{Asset gain (loss)} = \text{Actual return} - \hat{R} \times A_{beg}
$$
^f-03-02-22

- Goes to OCI with actuarial gains and losses, then is amortised through the corridor or faster; immediate recognition in P\&L is permitted but rare (V3 p.96, p.97).

**Corridor amortisation** (V3 p.96)
$$
\text{Amortisation}_t = \frac{\max\left(0,\; |G_{beg}| - 10\% \times \max(PBO_{beg}, A_{beg})\right)}{\text{Average remaining working life}}
$$
^f-03-02-23

- $G_{beg}$: net cumulative unrecognised gains and losses at the beginning of the period (V3 p.96).
- Only the excess over the 10% corridor is amortised; inside the corridor nothing reaches earnings, which is the smoothing purpose (V3 p.96).

**Total periodic pension cost from the funded status change (derived)** (V3 p.94)
$$
\text{Total periodic pension cost} = \text{Contributions} - \Delta\text{Funded status}
$$
^f-03-02-24

- Derivation: $\Delta FS = \Delta A - \Delta PBO = (\text{Actual return} + C - B) - (SC + IC - B \pm \text{Actuarial}) = C - (SC + IC - \text{Actual return} \pm \text{Actuarial})$; the bracket is the economic cost, so cost $= C - \Delta FS$.
- The curriculum states the principle (the expense is a non-cash accrual based on the change in the net pension liability or asset, not the contribution) and Kensington confirms it: $693 - (-4{,}774 + 4{,}984) = 693 - 210 = 483$ (V3 p.94, p.102).
- Under IFRS the total splits into P\&L (service cost plus net interest) and OCI (remeasurements); under US GAAP the same total splits into P\&L and OCI differently.

**Obligation sensitivity to the discount rate** (V3 p.99)
$$
\Delta PBO \approx -D_{PBO} \times PBO \times \Delta r, \qquad \text{with } |\Delta PBO| \text{ larger for a rate fall than a rise}
$$
^f-03-02-25

- The obligation behaves like a long-duration bond; Shell shows $+18{,}954$ for $-1\%$ and $-14{,}599$ for $+1\%$ (V3 p.99).
- Not a curriculum formula; the module gives the direction and the disclosure, the duration form is the reason.

**DB plans in the enterprise value bridge** (V3 p.100)
$$
\text{Equity value} = EV - \text{Debt} + \text{Cash} - \max(0,\; -\text{Funded status})
$$
^f-03-02-26

- Only an underfunded plan (net liability) is deducted; a surplus is ignored because plan assets cannot be distributed (V3 p.100).
- Deduct the end-of-period net liability, not the gross obligation and not the prior-year figure (V3 p.111).

**DB items in free cash flow** (V3 p.100, p.101)
$$
FCF_{DCF}: \text{ service cost expensed (not added back)}; \quad \text{net interest excluded}
$$
^f-03-02-27

- Service cost is future compensation in lieu of salary, so it stays in the cost base even though non-cash (V3 p.100).
- Net interest is the unwinding of a present value that the EV bridge already captures by deducting the net liability, so including it double counts (V3 p.101, p.113).

**Direction table: assumption changes** (V3 p.73, p.74, p.99, p.113)

| Assumption raised | Pension obligation | IFRS or US GAAP pension expense | Cash flow |
|---|---|---|---|
| Discount rate | Falls | Falls (service cost falls; interest cost usually falls because the smaller obligation outweighs the higher rate, except short-duration plans) | No effect |
| Salary growth rate | Rises | Rises (service cost and interest cost rise) | No effect |
| Inflation rate | Rises (indexed benefits) | Rises | No effect |
| Life expectancy | Rises | Rises | No effect |
| Healthcare cost trend (OPEB) | Rises | Rises | No effect |
| Expected return on plan assets (US GAAP only) | No effect | Falls | No effect |

| Option input raised | Option fair value | SBC expense | Net income |
|---|---|---|---|
| Expected volatility | Rises | Rises | Falls |
| Expected life | Rises | Rises | Falls |
| Risk-free rate | Rises | Rises | Falls |
| Dividend yield | Falls | Falls | Rises |
| Share price after grant | No effect on existing grants | No effect | No effect (tax and dilution effects only) |

## Worked examples

### Example 1: Short-term benefits, legal and manufacturing employees (V3 p.67)

Legal employee, annual salary SGD 82,200 paid every two weeks.
Pay periods per year $= 52 / 2 = 26$.
Expense per period $= 82{,}200 / 26 = 3{,}161.5$, rounded to 3,162 (Python: `82200/26 = 3161.54`).
Grant (1 January): no impact.
Vesting (1 to 14 January): G&A expense $+3{,}162$, accrued compensation $+3{,}162$, no cash flow.
Settlement (14 January): accrued compensation $-3{,}162$, CFO $-3{,}162$, no income statement impact.

Manufacturing employee, SGD 102,200: $102{,}200 / 26 = 3{,}930.8$, rounded to 3,931 (Python: `3930.77`).
Vesting: inventories $+3{,}931$ and accrued compensation $+3{,}931$; no expense yet.
Settlement 14 January: accrued compensation and cash both $-3{,}931$.
Sale on 3 April: cost of sales $+3{,}931$, inventories $-3{,}931$.
The lesson is that the cash flow and the expense can sit in different quarters even for the simplest compensation, because the cost is capitalised until the service is consumed (V3 p.67). ^ex-03-02-1

### Example 2: Share-based compensation accounting, 25,000 shares (V3 p.69, p.70)

Grant 1 January 20X1, three-year service vesting, grant-date fair value BRL 273,000.
Annual expense $= 273{,}000 / 3 = 91{,}000$ (Python: `91000.0`).
Each of 20X1, 20X2, 20X3: R&D expense 91,000; share-based compensation reserve (equity) $+91{,}000$; no cash flow, with 91,000 added back under the indirect method.
At settlement in 20X3 the cumulative 273,000 transfers from the reserve to common stock and paid-in capital.
Three differences from Example 1: the credit is to equity not a liability, vesting spans three years, and the measurement basis is grant-date fair value rather than the undiscounted payment (V3 p.70).
Fair value is measured once; any later change in share price has no effect on this grant (V3 p.70). ^ex-03-02-2

### Example 3: Knowledge check, Workflow RSU awards (V3 p.71 to p.73)

Three grants, each vesting one third per year, no dividends, forfeitures as they occur, three quarters to R&D and one quarter to executives.

Part 1: aggregate fair values and annual expense (Python, JPY millions).
- 1 January 20X1: $4{,}542{,}000 \times 4{,}360 = 19{,}803$; per year $6{,}601$.
- 1 January 20X2: $3{,}521{,}000 \times 3{,}270 = 11{,}514$; per year $3{,}838$.
- 1 January 20X3: $5{,}198{,}000 \times 3{,}333 = 17{,}325$; per year $5{,}775$.
Total expense: 20X1 $6{,}601$; 20X2 $6{,}601 + 3{,}838 = 10{,}439$; 20X3 $6{,}601 + 3{,}838 + 5{,}775 = 16{,}214$ (Python: `6601.04, 10438.93, 16213.91`).
Split: 20X1 R&D $4{,}951$ and G&A $1{,}650$; 20X2 R&D $7{,}829$ and G&A $2{,}610$; 20X3 R&D $12{,}161$ and G&A $4{,}054$ (Python: `0.75 × 16213.9 = 12160.4`).
Balance sheet: reserve rises by the year's expense; in 20X3 the 20X1 grant vests and 19,803 transfers from the reserve to paid-in capital.
Cash flow: none; add back under the indirect method (V3 p.72).

Part 2: share prices on 1 January 20X2 and 20X3 25% higher.
New prices $3{,}270 \times 1.25 = 4{,}088$ and $3{,}333 \times 1.25 = 4{,}166$ (Python: `4087.5, 4166.25`).
New aggregate values $14{,}394$ and $21{,}655$; per year $4{,}798$ and $7{,}218$ (Python: `14392.1, 21656.2; 4797.4, 7218.7`).
Expense: 20X1 $6{,}601$ (unchanged); 20X2 $6{,}601 + 4{,}798 = 11{,}399$; 20X3 $11{,}399 + 7{,}218 = 18{,}617$.
Percentage change: 0%, $11{,}399 / 10{,}439 - 1 = 9.2\%$, $18{,}617 / 16{,}214 - 1 = 14.8\%$ (Python: `0.0919, 0.1482`), which the curriculum rounds to 9% and 15%.
A 25% price rise moves the expense by far less because the 20X1 grant is locked at its grant-date value and each new grant phases in over three years (V3 p.73). ^ex-03-02-3

### Example 4: Knowledge check, Workflow option awards (V3 p.74, p.75)

25 million at-the-money options granted 1 January 20X1, vesting 31 December 20X3, share price and strike JPY 4,360, fair value per option JPY 1,288, seven-year life.

Part 1: aggregate fair value $= 25 \times 1{,}288 = 32{,}200$ million; annual expense $= 32{,}200 / 3 = 10{,}733$ million (Python: `10733.33`).
Each year: G&A expense 10,733; reserve $+10{,}733$; no cash flow, add back under the indirect method.

Part 2: 20X4 with the share price below 4,360.
The options are out of the money, nobody exercises, no financial statement impact (V3 p.75).

Part 3: 20X5, share price 5,400, 6 million exercised.
Cash inflow from financing $= 6 \times 4{,}360 = 26{,}160$ million (Python: `26160`).
Reserve transferred $= (6 / 25) \times 32{,}200 = 7{,}728$ million; paid-in capital $+26{,}160 + 7{,}728 = 33{,}888$ million (Python: `7728, 33888`).
No income statement effect; the 5,400 price only explains why exercise happened (V3 p.75). ^ex-03-02-4

### Example 5: Meta Platforms, tax effects under US GAAP (V3 p.78, p.79)

Reconciliation 2021: $21\% + 1.0\% - 2.2\% - 1.3\% - 3.5\% + 0.9\% + 0.8\% = 16.7\%$ (Python: `16.7`).
2020: $21\% + 0.8\% - 1.6\% - 1.3\% - 1.9\% - 2.4\% - 3.0\% + 0.6\% = 12.2\%$ (Python: `12.2`).
The excess tax benefit line ($-2.2\%$ in 2021, $-1.6\%$ in 2020) exists because the share price rose 23% and 30% in those years, so RSUs settled above their grant-date values and the tax deduction exceeded the book expense (V3 p.78).
When the share price fell 72% in 2022 the windfall evaporated and the effective rate rose to the 21% statutory rate, up 8 points in the third quarter year on year (V3 p.79).
Under IFRS the same windfall would have gone to equity and the effective rate would have stayed near statutory (V3 p.78, p.79). ^ex-03-02-5

### Example 6: Workflow diluted shares with unvested RSUs and options (V3 p.80, p.81)

Basic shares 176,401,000, positive net income, average price JPY 4,200, unrecognised expense 21,467 million (options) and 13,202 million (RSUs) at 31 December 20X1.
Check the unrecognised figures: options $32{,}200 - 10{,}733 = 21{,}467$; RSUs $19{,}803 - 6{,}601 = 13{,}202$ (Python).

Options: cash proceeds $= 25{,}000{,}000 \times 4{,}360 = 109{,}000$ million; average unrecognised $= (0 + 21{,}467)/2 = 10{,}734$ million (rounded); assumed repurchases $= (109{,}000 + 10{,}734) / 4{,}200 = 28.508$ million shares, that is 28,508,095 (Python with 10,734: `28508095`; with 10,733.5: `28507976`).
Repurchases exceed the 25 million options, so the options are anti-dilutive and contribute zero; the curriculum's "million" after 28,508,095 is a typo for shares (V3 p.81).

RSUs: unvested $= 4{,}542{,}000 \times 2/3 = 3{,}028{,}000$ (two thirds of the 20X1 grant remain after one year of vesting); cash proceeds zero; average unrecognised $= (0 + 13{,}202)/2 = 6{,}601$ million; assumed repurchases $= 6{,}601 \text{ million} / 4{,}200 = 1{,}571{,}667$; dilutive shares $= 3{,}028{,}000 - 1{,}571{,}667 = 1{,}456{,}333$ (Python: `1571666.7, 1456333.3`).
Diluted shares $= 176{,}401{,}000 + 1{,}456{,}333 = 177{,}857{,}333$ (Python: `177857333`).
25 million anti-dilutive options are disclosed but excluded (V3 p.80). ^ex-03-02-6

### Example 7: ServiceNow, anti-dilutive awards with a net loss (V3 p.82)

2018: net loss USD 26,704 thousand; basic and diluted shares both 177,846,023; net loss per share $-0.15$.
Excluded anti-dilutive securities: options 1,810,580, RSUs 10,201,660, ESPP 317,940, convertible debt 5,806,933, warrants 13,589,879, total 31,727,069.
Including them: $31{,}727{,}069 / 177{,}846{,}023 = 17.8\%$, rounding to 18%, for a share count of about 209.6 million, the curriculum's 210 million (Python: `0.1784, 209573092`).
Because diluted EPS cannot exceed basic EPS, a loss-maker reports the same share count regardless of what is outstanding; ServiceNow's diluted count did rise by 25 million to 203 million once it became profitable (V3 p.82).
Analyst action: add disclosed anti-dilutive securities to the diluted count for valuation (V3 p.82). ^ex-03-02-7

### Example 8: Meta Platforms, selecting the right share count (V3 p.83)

Three months to 30 September (millions): 2022 basic 2,682, dilutive RSUs 5, diluted 2,687, anti-dilutive RSUs 119; 2021 basic 2,814, dilutive RSUs 45, diluted 2,859, anti-dilutive 0.
A 72% price fall raised assumed repurchases (fixed grant-date proceeds divided by a much lower average price), so dilutive RSUs fell from 45 to 5 and 119 million became anti-dilutive (V3 p.83).
This flatters EPS through a lower share count in the same period that the vanished tax windfall hurts it through a higher tax rate; neither latest-quarter value should be assumed to persist (V3 p.83). ^ex-03-02-8

### Example 9: Meta Platforms, share-based compensation disclosures (V3 p.83, p.84)

Unvested RSU roll-forward (thousands): $96{,}733 + 59{,}127 - 44{,}574 - 12{,}438 = 98{,}848$ (Python: `98848`).
Weighted-average grant-date fair values: unvested opening USD 181.88, granted 305.40, vested 198.95, forfeited 211.58, closing 244.58.
Unrecognised expense USD 22.77 billion over a weighted-average three years, so the run-rate expense embedded in existing grants is about USD 7.6 billion a year.
Fair value of shares vesting in 2021 was USD 14.42 billion against a grant-date basis of roughly $44{,}574 \times 198.95 = 8.87$ billion, which is the windfall that produced the tax benefit of USD 3.08 billion in Example 5 (V3 p.84).
The disclosure gives the analyst every input to Formulas 7 to 9: unvested awards, grant-date values, and unrecognised expense (V3 p.83, p.84). ^ex-03-02-9

### Example 10: Free cash flow measures and share-based compensation (V3 p.88)

Company A: CFO 420, capex 300, FCF $= 120$, FCF margin $120 / 1{,}000 = 12\%$, P/E $= 10{,}000 / 120 = 83$, P/FCF $= 83$.
Company B: SBC 150 instead of cash pay, CFO 570, FCF $= 270$, margin 27%, P/E 83, P/FCF $= 10{,}000 / 270 = 37$ (Python: `83.3, 37.0`).
The two companies are economically identical; B's lower P/FCF is an artefact of paying in shares, which still transfers value and dilutes owners (V3 p.88).
Deducting SBC restores B's FCF to 120 and its multiple to 83. ^ex-03-02-10

### Example 11: Forecasting Workflow's share-based compensation (V3 p.85, p.86)

Step 1: subtract SBC from each cost line (JPY millions).
20X3: cost of revenues $4{,}279 - 44 = 4{,}235$; R&D $11{,}172 - 3{,}161 = 8{,}011$; S&M $15{,}559 - 1{,}630 = 13{,}929$; G&A $6{,}529 - 915 = 5{,}614$ (Python).
The curriculum table shows 4,234, 8,010, 13,930 and 5,613, differences of 1 from rounding of underlying figures; 20X1 G&A shows 1,848 where $2{,}576 - 768 = 1{,}808$, and the 20X1 SBC lines sum to 2,702 not the stated 2,661, so treat the 20X1 column as internally inconsistent and rely on the method.
Step 2: percentages of revenue for 20X3: cost of revenues 10%, R&D 19%, S&M 33%, G&A 13%, SBC 14% (Python: `10.2, 19.2, 33.5, 13.5, 13.8`).
Step 3: forecast 20X4E percentages 8%, 19%, 31%, 13%, 12% on revenue $62{,}440$ (a 50% increase on 41,628).
Step 4: cost of revenues $0.08 \times 62{,}440 = 4{,}995$; gross profit excl. SBC $57{,}445$; R&D $11{,}864$; S&M $19{,}356$; G&A $8{,}117$; SBC $7{,}493$; total operating expenses $11{,}864 + 19{,}356 + 8{,}117 + 7{,}493 = 46{,}830$; operating income $62{,}440 - 4{,}995 - 46{,}830 = 10{,}615$ (Python: `4995.2, 11863.6, 19356.4, 8117.2, 7492.8, 46830, 10614.8`).
The discrete SBC line then feeds the cash flow add-back and the equity credit (V3 p.86). ^ex-03-02-11

### Example 12: Employer accounting for a DC plan (V3 p.91)

Contribution 5% of salary, salary SGD 82,200, paid every two weeks.
Per period $= 0.05 \times 82{,}200 / 26 = 158.1$, rounded to 158 (Python: `158.08`).
Vesting: G&A expense $+158$, accrued compensation $+158$.
Settlement 14 January: accrued compensation $-158$, CFO $-158$.
Plan assets and withdrawals never appear on the employer's statements; the plan is a separate entity (V3 p.91). ^ex-03-02-12

### Example 13: Workflow DB pension over two periods (V3 p.94, p.95)

Part 1, 20X1: contribution 710 at the start of the year, service cost 5, discount rate 2%, no benefits, actual return $-3\%$, no other contributions, no assumption changes.
Beginning obligation and beginning assets (before the opening contribution) are both zero, so net interest is zero (V3 p.95).
Actual return $= -0.03 \times 710 = -21.3$; remeasurement $= -21.3 - 0 = -21.3$ to OCI (Python: `-21.3`).
Ending assets $= 710 - 21.3 = 688.7$; ending obligation $= 5$; net pension asset $= 683.7$ (Python: `683.7`).
Income statement: operating expense 5.
Balance sheet: cash $-710$, net pension asset 683.7.
Cash flow: CFO $-710$ (V3 p.95).

Part 2, 20X8: service cost 9, benefits paid 5, discount rate 2%, beginning obligation 97, beginning assets 1,010, actual return 5%, no contributions.
Beginning funded status $= 1{,}010 - 97 = 913$ (net asset).
Net interest income $= 0.02 \times 913 = 18.26$, reported as 18.3 (Python: `18.26`).
Actual return $= 0.05 \times 1{,}010 = 50.5$; interest income assumed on assets $= 0.02 \times 1{,}010 = 20.2$; remeasurement $= 50.5 - 20.2 = 30.3$ to OCI (Python: `30.3`).
Note the curriculum's wording "difference between actual return and net interest income" is loose; $50.5 - 18.3 = 32.2$ does not reconcile, while $50.5 - 20.2 = 30.3$ does, and Exhibit 8 defines the net return on plan assets as actual return less plan assets times the interest rate (V3 p.97).
Roll-forwards: obligation $97 + 9 + 1.94 - 5 = 102.94$; assets $1{,}010 + 50.5 - 5 = 1{,}055.5$; net pension asset $= 952.56$, reported as 952.6 (Python: `952.56`).
Check with Formula 24: change in funded status $= 952.56 - 913 = 39.56$; total cost $= 0 - 39.56 = -39.56$ (a net gain); P&L $= 9 - 18.26 = -9.26$; OCI $= -39.56 + 9.26 = -30.3$, a gain of 30.3 (Python: `30.3`).
Cash flow: no impact because no contributions were made; benefits paid of 5 are neutral to funded status (V3 p.95). ^ex-03-02-13

### Example 14: Shell plc DB disclosures and sensitivities (V3 p.97 to p.99)

31 December 2021 (USD millions): obligations $-107{,}336$, plan assets $104{,}495$, asset ceiling $-13$, deficit $-2{,}854$; recognised as non-current assets 8,471, pension liabilities $-6{,}458$, OPEB liabilities $-4{,}867$, total $-2{,}854$ (Python: `8471 - 6458 - 4867 = -2854`).
The gross-up is the no-netting rule: overfunded plans (Netherlands surplus 1,756, UK 3,807, US funded 182) sit in assets while unfunded plans (US unfunded 1,129, OPEB 4,067) sit in liabilities (V3 p.98, p.99).
Asset allocation: 32% equities, 57% debt, 7% real estate, 3% funds, 1% cash; expected contributions USD 900 million in 2022 (V3 p.99).
Sensitivities: discount rate $-1\%$ raises the obligation by 18,954 and $+1\%$ lowers it by 14,599; pension increase rate $\pm 1\%$ gives $-9{,}908$ to $+12{,}171$; inflation $\pm 1\%$ gives $-10{,}691$ to $+13{,}325$; one year of life expectancy for men is about $\pm 1{,}940$ (V3 p.99).
Analyst reading: the discount rate is the dominant assumption, its effect is asymmetric, and management's aggressive direction is a high discount rate with low salary growth, inflation, and longevity (V3 p.99). ^ex-03-02-14

## Item-set patterns

> [!warning] Trap 1: the share price moved after the grant
> The vignette reports a higher or lower share price at year end or at vesting and asks for the effect on expense.
> Correct: no effect on the expense of existing grants, because grant-date fair value is measured once; only new grants, the tax windfall, and the treasury stock method respond to price (V3 p.70, p.73).
> Distractors: expense scaled up by the price change (tempting because the award is "worth more"), a gain or loss recognised in P&L (confusing equity-settled awards with cash-settled ones), or a remeasurement of the reserve.

> [!warning] Trap 2: RSU versus option valuation inputs
> A question changes the volatility assumption and asks about RSU expense, or changes the dividend yield and asks about option expense.
> Correct: RSU fair value is the share price (less foregone dividends), so volatility is irrelevant; option value rises with volatility, life, and the risk-free rate and falls with dividend yield (V3 p.71, p.73, p.74, p.112).
> Distractors: applying option logic to RSUs (Practice Problem 12), or reversing the dividend yield direction (Practice Problem 25).

> [!warning] Trap 3: where the tax windfall goes
> The settlement price exceeds the grant price and the vignette asks for the effect on income tax expense.
> Correct: US GAAP reduces income tax expense by $t \times (\text{deduction} - \text{expense})$; IFRS books the same amount directly in equity and leaves the effective tax rate alone (V3 p.78, p.112).
> Distractors: $t \times$ full deduction (Practice Problem 15 option C), the wrong sign (treating a windfall as an increase), or applying the US GAAP treatment to an IFRS reporter.

> [!warning] Trap 4: treasury stock method proceeds
> A share count question gives unrecognised expense at two dates, an average price, and unvested awards.
> Correct: proceeds are cash from exercise plus the average of the two unrecognised balances; divide by the average price; subtract from the award count; a negative result means anti-dilutive, contribute zero (V3 p.80, p.81, p.112).
> Distractors: adding the gross award count (Practice Problem 17 option C), using the ending unrecognised balance only, dividing by the grant price, or counting anti-dilutive options as negative dilution.

> [!warning] Trap 5: net loss and diluted shares
> The company reports a net loss and large unvested awards.
> Correct: basic and diluted shares are equal; every unvested award is anti-dilutive regardless of moneyness, and the analyst adds them back for valuation (V3 p.81, p.82, p.113).
> Distractors: computing a treasury stock dilution anyway, or adding only the in-the-money awards.

> [!warning] Trap 6: IFRS pension P&L versus total cost
> A pension note shows service cost, net interest, remeasurements, and a total, then asks for the operating expense, the income statement amount, or the balance sheet change.
> Correct: operating expense is service cost only; P&L is service cost plus net interest; remeasurements are OCI; the balance sheet change equals contributions minus total cost (V3 p.93, p.94, p.111).
> Distractors: the total periodic cost (483) as the operating expense, the change in funded status (210) as the expense, or the contribution (693) as the expense (Practice Problems 3, 4, 5).

> [!warning] Trap 7: US GAAP five components
> An IFRS reporter's data is given and the question asks what US GAAP P&L would show.
> Correct: current service cost plus gross interest cost ($r \times PBO_{beg}$) minus expected return ($\hat{R} \times A_{beg}$) plus any amortisation; past service cost and the actuarial loss go to OCI unless the question says otherwise (V3 p.96, p.111).
> Distractors: including past service cost in P&L (IFRS treatment), using the actual return instead of the expected return, or applying the discount rate to assets.

> [!warning] Trap 8: the discount rate and the interest cost
> The vignette lowers the discount rate and asks what happens to interest cost or net income.
> Correct: a lower rate raises the obligation; the interest cost usually rises because the larger obligation outweighs the smaller rate (except short-duration plans); net income falls; cash flow is unchanged (V3 p.113).
> Distractors: "lower rate, lower interest cost" (rate-only reasoning), or a cash flow effect (contributions are a funding decision, not an accounting one).

> [!warning] Trap 9: expected return and the obligation
> The question changes the expected return on plan assets and asks about the obligation or an IFRS expense.
> Correct: the expected return never enters the obligation, and under IFRS it does not exist; it only lowers US GAAP expense (V3 p.94, p.96, p.113).
> Distractors: "the obligation would be lower" (Practice Problem 20), or an IFRS net interest that uses the expected return.

> [!warning] Trap 10: DCF treatment of pensions and SBC
> A colleague's model expenses service cost and net interest, deducts the net pension liability, or adds back SBC.
> Correct: keep service cost expensed, remove net interest (already captured by deducting the net liability at present value), deduct only underfunded status, ignore a surplus, and either deduct SBC from FCF or inflate the share count (V3 p.87, p.100, p.101, p.113).
> Distractors: removing service cost because it is non-cash, deducting the gross obligation, adding a surplus to equity value, or treating SBC as a source of cash.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM02-Employee-Compensation-Post-Employment-and-Share-Based-Practice-Problems]]

## Cross-links

- [[LM01-Intercorporate-Investments]]: the same fair value and net-presentation logic (funded status is one of the few permitted net presentations) sits beside the equity method and consolidation choices that also move reported liabilities and ratios.
- [[LM05-Evaluating-Quality-of-Financial-Reports]]: pension assumptions (discount rate, salary growth, expected return, volatility) are discretionary levers on earnings quality; Terra Mercado's internal inconsistency check is the quality-of-earnings toolkit applied to compensation.
- [[LM06-Integration-of-Financial-Statement-Analysis-Techniques]]: the analyst adjustments here (SBC out of FCF, net pension liability into debt, anti-dilutive shares back into the count, windfall out of the tax rate) are the inputs the integration module feeds into ratios and forecasts.
- [[LM03-Free-Cash-Flow-Valuation]]: this module decides what FCFF and FCFE contain: service cost expensed, net interest excluded, SBC deducted or dilution modelled, and the net pension deficit treated as debt in the EV bridge.
- [[LM01-Analysis-of-Dividends-and-Share-Repurchases]]: buybacks that offset SBC dilution are why the curriculum treats SBC as economically cash-like, and the treasury stock method's average price link is the mirror of repurchase timing effects on EPS.

## Self-test

> [!question] ST1
> An IFRS reporter's DB plan has a beginning obligation of 5,000, beginning plan assets of 4,200, and a discount rate of 4%.
> The net interest amount recognised in profit or loss for the year is closest to:
> A. 32 expense.
> B. 168 income.
> C. 200 expense.

> [!question] ST2
> A sponsor contributed 150 during the year. Funded status moved from $-600$ at the start to $-540$ at the end.
> Total periodic pension cost (P&L plus OCI) for the year is closest to:
> A. 90.
> B. 150.
> C. 210.

> [!question] ST3
> Under US GAAP: current service cost 100, beginning obligation 3,000, discount rate 5%, beginning plan assets 2,500, expected return 7%, amortisation of past service cost 10, cumulative unrecognised actuarial loss 400 at the beginning of the year, average remaining working life 10 years.
> Pension expense in P&L is closest to:
> A. 85.
> B. 95.
> C. 125.

> [!question] ST4
> An IFRS plan has beginning plan assets of 2,000, a 3% discount rate, an actual return of 120, and an actuarial loss of 50 from a mortality update.
> The remeasurement recognised in OCI is closest to:
> A. a gain of 10.
> B. a gain of 70.
> C. a loss of 50.

> [!question] ST5
> Basic shares 100 million, net income positive, 6 million unvested RSUs, unrecognised SBC expense 90 million at the start and 120 million at the end of the year, average share price 30.
> Diluted shares are closest to:
> A. 102.0 million.
> B. 102.5 million.
> C. 106.0 million.

> [!question] ST6
> 4 million options with strike 20, average share price 25, average unrecognised SBC expense 8 million, profitable company.
> Incremental dilutive shares from the options are closest to:
> A. 0.
> B. 0.48 million.
> C. 0.80 million.

> [!question] ST7
> 1 million RSUs granted at a fair value of 40 settle when the share price is 55; the tax rate is 25%.
> Under US GAAP the effect on income tax expense is closest to:
> A. a reduction of 3.75 million.
> B. a reduction of 13.75 million.
> C. no effect; the benefit is recognised in equity.

> [!question] ST8
> Which set of assumption changes would all reduce a sponsor's reported pension obligation?
> A. Higher discount rate, lower salary growth, lower life expectancy.
> B. Higher discount rate, higher expected return on plan assets, lower inflation.
> C. Lower discount rate, lower salary growth, lower healthcare cost trend.

> [!question] ST9
> EV 10,000, debt 2,000, cash 500, a pension plan with a surplus of 300, and an unfunded OPEB plan with a deficit of 700.
> Equity value under the curriculum's treatment is closest to:
> A. 7,800.
> B. 8,100.
> C. 8,500.

> [!question] ST10
> Next-year revenue 800 million, SBC forecast at 12% of revenue, weighted-average grant-date fair value of vesting RSUs 32, share price 128, repurchases 1.0 million shares, beginning basic shares 200 million, no other issuance.
> Ending basic shares are closest to:
> A. 199.75 million.
> B. 202.0 million.
> C. 203.0 million.

> [!success]- Answer key
> ST1: A. Net interest $= 4\% \times (5{,}000 - 4{,}200) = 4\% \times 800 = 32$, an expense because the plan is underfunded (Python: `32.0`).
> B is the interest income on assets alone ($4\% \times 4{,}200$); C is the gross interest cost ($4\% \times 5{,}000$), the US GAAP component, not the IFRS net figure (V3 p.94).
> ST2: A. Change in funded status $= -540 - (-600) = +60$; total cost $= 150 - 60 = 90$ (Python: `90`).
> C adds instead of subtracting; B assumes contributions equal cost, which is the DC logic the curriculum says violates accrual accounting for DB plans (V3 p.94).
> ST3: B. Corridor $= 10\% \times \max(3{,}000, 2{,}500) = 300$; excess $= 400 - 300 = 100$; amortisation $= 100 / 10 = 10$.
> Expense $= 100 + 150 - 175 + 10 + 10 = 95$ (Python: `95.0`).
> A omits the corridor amortisation; C amortises the whole 400 ($40$) instead of the excess (V3 p.96).
> ST4: A. Net return on assets $= 120 - 3\% \times 2{,}000 = 60$ gain; less the actuarial loss of 50 gives a net gain of 10 in OCI (Python: `10.0`).
> B forgets to strip out the interest income already in net interest; C ignores the asset component (V3 p.97).
> ST5: B. Average unrecognised $= (90 + 120)/2 = 105$; assumed repurchases $= 105 / 30 = 3.5$ million; diluted $= 100 + 6 - 3.5 = 102.5$ million (Python: `102.5`).
> A uses the ending balance only ($120/30 = 4$); C adds the gross RSUs (V3 p.80).
> ST6: B. Proceeds $= 4 \times 20 + 8 = 88$; repurchases $= 88 / 25 = 3.52$ million; dilutive $= 4 - 3.52 = 0.48$ million (Python: `0.48`).
> C ignores the unrecognised expense ($80/25 = 3.2$, net $0.8$); A wrongly treats an in-the-money option as anti-dilutive (V3 p.80, p.81).
> ST7: A. Windfall $= 25\% \times (55 - 40) \times 1 = 3.75$ million, a reduction in income tax expense under US GAAP (Python: `3.75`).
> B taxes the full deduction; C is the IFRS treatment (V3 p.78).
> ST8: A. Each of a higher discount rate, lower salary growth, and lower longevity shrinks the obligation.
> B includes the expected return, which never touches the obligation; C includes a lower discount rate, which raises it (V3 p.99, p.113).
> ST9: A. Equity $= 10{,}000 - 2{,}000 + 500 - 700 = 7{,}800$; the surplus is ignored because plan assets cannot be distributed (Python: `7800`).
> B adds the 300 surplus; C ignores the OPEB deficit, which is a liability the company must pay (V3 p.100).
> ST10: B. SBC $= 0.12 \times 800 = 96$ million; shares vesting $= 96 / 32 = 3.0$ million; ending basic $= 200 + 3.0 - 1.0 = 202.0$ million (Python: `202.0`).
> C forgets the repurchases; A divides by the market price of 128 ($0.75$ million) instead of grant-date fair value (V3 p.87, p.113).

## Flashcards

#flashcards/cfa-l2/03-Financial-Statement-Analysis/lm02

Underlying principle of IAS 19 for all compensation::Recognise the fair value of compensation as an expense in the period the employee provides the service, usually the vesting period (V3 p.66).
Five categories of employee compensation::Short-term benefits, long-term benefits, termination benefits, share-based compensation, post-employment benefits (V3 p.66).
Three differences between SBC accounting and salary accounting::Credit to equity not a liability; vesting over years; measured at grant-date fair value not undiscounted payment (V3 p.70).
Grant-date fair value of an RSU::The share price at grant, reduced for dividends expected during vesting if the RSU does not participate (V3 p.71).
Grant-date fair value of an employee stock option::Estimated with an option pricing model (Black-Scholes or binomial); intrinsic value is zero at the money so it is all time value (V3 p.73).
Four option inputs that raise option fair value::Higher volatility, longer expected life, higher risk-free rate, lower dividend yield (V3 p.73, p.74).
Effect of a share price rise after the grant on the expense of that grant::None; fair value is measured once at grant (V3 p.70).
Micro-problem: 4,542,000 RSUs at JPY 4,360, 3-year vesting; annual expense?::4,542,000 times 4,360 equals 19,803 million; divided by 3 equals 6,601 million (V3 p.72).
Micro-problem: 25 million options at FV 1,288, 3-year vesting; annual expense?::25 times 1,288 equals 32,200 million; divided by 3 equals 10,733 million (V3 p.74).
Cash flow effect of an option exercise::Financing inflow equal to options exercised times strike price (V3 p.74).
Tax deduction basis for RSUs and options::Share price at settlement for RSUs; intrinsic value at exercise for options; timing is at settlement (V3 p.77).
Tax windfall formula::Tax rate times (tax deduction at settlement minus cumulative SBC expense) (V3 p.112).
Where IFRS books a tax windfall::Directly in equity as a gain (V3 p.78).
Where US GAAP books a tax windfall::As a decrease in income tax expense on the income statement (V3 p.78).
Which regime has more volatile effective tax rates from SBC?::US GAAP, because windfalls and shortfalls run through income tax expense (V3 p.79).
Micro-problem: 3,332,063 RSUs settle at 71.50, grant FV 19.25, tax 17%; windfall?::0.17 times 52.25 times 3,332,063 equals 29.6 million reduction in US GAAP tax expense (V3 p.112).
Treasury stock method for diluted shares::Basic shares plus awards minus (assumed proceeds divided by average share price) (V3 p.79, p.80).
Assumed proceeds in the treasury stock method::Cash from exercise (strike times options, zero for RSUs) plus average unrecognised SBC expense (V3 p.80).
Average unrecognised SBC expense::The average of the last two period-end unrecognised balances, each equal to unvested awards times grant-date fair value (V3 p.80).
Micro-problem: 5 million RSUs, unrecognised 60 and 80 million, average price 35; dilutive shares?::Average 70 million divided by 35 equals 2 million repurchased; 5 minus 2 equals 3 million dilutive (V3 p.80).
When are options anti-dilutive under the treasury stock method?::When out of the money or at the money (average price at or below strike) (V3 p.81).
When can RSUs be anti-dilutive?::When the average share price is materially below the grant-date price, because unrecognised expense is at grant prices (V3 p.81).
Diluted shares for a company with a net loss::Equal to basic shares; all potentially dilutive securities are anti-dilutive (V3 p.81, p.82).
Common forecast basis for SBC expense::Percentage of revenues, modelled discretely from cash operating expenses (V3 p.85).
Balance sheet entry that balances the SBC forecast::Credit to equity (share-based compensation reserve) equal to the expense (V3 p.85, p.113).
Shares issued from RSU vesting in a forecast::SBC expense recognised at vesting divided by grant-date fair value per share (V3 p.113).
Basic shares roll-forward::Beginning plus RSUs vested and options exercised plus other issuances minus repurchases (V3 p.87).
Two DCF fixes for SBC dilution::Deduct SBC from free cash flow, or increase the share count for expected dilution; both should give the same result (V3 p.87, p.88).
Why FCF multiples flatter heavy SBC users::SBC is excluded from FCF although it transfers value and dilutes owners; Company B shows P/FCF 37 versus 83 for identical Company A (V3 p.88).
DC plan: who bears investment and actuarial risk?::The employee; the employer's obligation ends with the contribution (V3 p.89, p.90).
DB plan: who bears investment and actuarial risk?::The employer sponsor (V3 p.90).
What is OPEB and how is it usually funded?::Non-monetary post-employment benefits such as retiree medical care, usually unfunded pay-as-you-go, accounted for as DB (V3 p.90, p.91).
Funded status::Fair value of plan assets minus pension obligation; negative is a net pension liability, positive a net pension asset (V3 p.91, p.92).
Discount rate for the pension obligation::Yield on investment-grade corporate bonds (or government bonds if no liquid market) in the benefit currency (V3 p.92).
IFRS periodic pension cost components::Service cost (current and past) in P&L, net interest in P&L below operating income, remeasurements in OCI (V3 p.93, p.94).
IFRS net interest::Discount rate times beginning net pension liability or asset (V3 p.94).
IFRS remeasurement components::Actual return minus (plan assets times discount rate), plus actuarial gains and losses from assumption changes (V3 p.94, p.97).
Micro-problem: IFRS, service cost 80, obligation 4,000, assets 3,600, rate 5%; P&L?::80 plus 0.05 times 400 equals 100 (V3 p.94).
Micro-problem: US GAAP, service cost 80, obligation 4,000 at 5%, assets 3,600 at 7% expected, no amortisation; P&L?::80 plus 200 minus 252 equals 28 (V3 p.96).
US GAAP five components of pension expense::Current service cost, interest cost, expected return on plan assets, amortisation of past service cost, amortisation of net actuarial gains and losses (V3 p.96).
US GAAP treatment of past service cost::To OCI when incurred, then amortised to P&L over the average service life of affected employees (V3 p.96).
Corridor rule::Amortise only the cumulative unrecognised gains and losses exceeding 10% of the greater of beginning obligation and beginning plan assets, over the average remaining working life (V3 p.96).
Micro-problem: unrecognised loss 900, obligation 8,000, assets 7,000, 8-year remaining life; amortisation?::Corridor 800; excess 100; 100 divided by 8 equals 12.5 (V3 p.96).
Total periodic pension cost from cash and balance sheet data::Contributions minus change in funded status (V3 p.94, p.102).
Micro-problem: contributions 693, funded status from minus 4,984 to minus 4,774; total cost?::693 minus 210 equals 483 (V3 p.102).
Effect of benefits paid on funded status::None; assets and obligation fall equally (V3 p.94).
Aggressive pension assumptions::High discount rate, low salary growth, low inflation, low life expectancy, low healthcare trend, and under US GAAP a high expected return (V3 p.99).
Does the expected return affect the obligation?::No; it affects only US GAAP expense (V3 p.113).
Effect of a lower discount rate on interest cost::Usually higher, because the larger obligation outweighs the lower rate, except for short-duration plans (V3 p.113).
Internally inconsistent assumption pair::Higher inflation with lower salary growth, since salaries move with inflation (V3 p.113).
DB plans in the EV to equity bridge::Deduct an underfunded status as debt; ignore a surplus because plan assets cannot be distributed (V3 p.100).
Service cost in a DCF::Leave it expensed in free cash flow; it is compensation in lieu of salary (V3 p.100).
Net interest in a DCF::Exclude it; the deficit is already deducted at present value (V3 p.101).
Trap: "expense the actual return under US GAAP"::Wrong; US GAAP P&L uses the expected return, and the difference goes to OCI (V3 p.96, p.97).
Trap: "RSU expense falls when volatility falls"::Wrong; RSU value is the share price and volatility is irrelevant (V3 p.112).
Trap: "net pension liability change equals the pension expense"::Wrong; the change equals contributions minus total cost (V3 p.94).
Under IFRS remeasurements are recognised in {{OCI}} and are {{never recycled}} to earnings (V3 p.94).
Under US GAAP interest cost is {{gross}}, computed as {{discount rate times beginning obligation}}, while IFRS net interest is {{discount rate times beginning funded status}} (V3 p.94, p.96).
Under the treasury stock method assumed proceeds are {{fixed at grant-date values}} while the divisor, the {{average share price}}, floats (V3 p.80, p.83).
A frozen plan has {{no future service cost}}, so only its {{funded status}} matters in valuation (V3 p.100).

## Common mistakes

1. Remeasuring an existing grant when the share price moves; grant-date fair value is fixed and later price changes only affect new grants, tax windfalls, and dilution (V3 p.70, p.73).
2. Applying option pricing inputs (volatility, expected life) to RSUs, whose fair value is just the share price adjusted for dividends (V3 p.71, p.112).
3. Reversing the dividend yield effect on option value: a higher yield lowers the option value and the expense (V3 p.73, p.113).
4. Booking the tax windfall in the wrong place: IFRS to equity, US GAAP to income tax expense; and taxing the whole deduction instead of the excess over the book expense (V3 p.78, p.112).
5. Using the ending unrecognised SBC expense rather than the average of the two period ends in the treasury stock method, or forgetting the unrecognised expense altogether (V3 p.80).
6. Adding gross unvested awards to the share count instead of the net treasury stock figure, or subtracting anti-dilutive amounts as negative dilution (V3 p.80, p.81, p.112).
7. Computing dilution for a loss-making company; basic and diluted shares are equal, and the analyst adds anti-dilutive awards back only for valuation (V3 p.81, p.82).
8. Forgetting the equity credit when modelling SBC, which leaves the balance sheet out by exactly the expense (V3 p.85, p.113).
9. Dividing forecast SBC by the market price to get shares issued; the divisor is grant-date fair value per share (V3 p.113).
10. Treating the pension contribution as the expense; the expense is the accrual change in funded status split into cost components (V3 p.93, p.94).
11. Reporting total periodic cost or the change in funded status as the operating expense; only service cost is operating, net interest is financing, remeasurements are OCI (V3 p.93, p.111).
12. Putting past service cost through P&L under US GAAP; it goes to OCI first and is amortised (V3 p.96).
13. Using actual return in US GAAP P&L instead of expected return, or applying the expected return to the obligation (V3 p.96, p.113).
14. Amortising the whole unrecognised gain or loss rather than only the excess over the 10% corridor (V3 p.96).
15. Reasoning "lower discount rate, lower interest cost"; the larger obligation usually dominates and interest cost rises (V3 p.113).
16. Deducting the gross obligation, the opening deficit, or a surplus in the EV bridge; deduct only the closing net liability (V3 p.100, p.111).
17. Stripping service cost out of FCF as non-cash, or leaving net interest in FCF after deducting the net pension liability, which double counts (V3 p.100, p.101, p.113).
18. Extrapolating an effective tax rate that contains an SBC windfall, which overstates FCFF and EV (V3 p.79, p.113).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "03-02" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
