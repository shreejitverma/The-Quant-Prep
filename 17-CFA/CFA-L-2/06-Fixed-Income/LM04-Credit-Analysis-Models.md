---
type: cfa-lm
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
volume: 6
lm: 4
title: "Credit Analysis Models"
pages: "199-273"
weight_band: "10-15%"
difficulty: 4
los_count: 8
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/fixed-income]
---

# LM4: Credit Analysis Models

Difficulty 4 of 5: the CVA table is a seven-column machine the exam expects you to build from scratch, the arbitrage-free tree from LM2 returns with a credit layer on top, floaters add in-arrears coupons and a discount margin search, and the conceptual LOS (structural versus reduced-form, spread term structure, securitized debt) hide precise classification traps behind easy-sounding prose.

## LOS map

- **explain** expected exposure, the loss given default, the probability of default, and the credit valuation adjustment (V6 p.199) ^los-06-04-a
    - Examiner asks: complete or interpret a year-by-year CVA table (exposure, recovery, LGD, conditional POD from a hazard rate, POS, expected loss, discounted expected loss), sum the last column to the CVA, and subtract it from the VND to get fair value.
- **explain** credit scores and credit ratings (V6 p.199) ^los-06-04-b
    - Examiner asks: which FICO factor explains a score change (payment history 35%, debt burden 30%, length 15%, types of credit 10%, recent inquiries 10%), or a ratings question on notching, outlooks and watch status, and why agencies rate both issuers and issues.
- **calculate** the expected return on a bond given transition in its credit rating (V6 p.199) ^los-06-04-c
    - Examiner asks: from one row of a transition matrix plus credit spreads and a modified duration, compute each migration's percentage price change as minus duration times the spread change, probability-weight them, and add the sum to the YTM.
- **explain** structural and reduced-form models of corporate credit risk, including assumptions, strengths, and weaknesses (V6 p.199) ^los-06-04-d
    - Examiner asks: classify a described estimation approach (option pricing on the balance sheet versus regression on observable variables) as structural or reduced-form, and pick the correct strength or weakness (default barrier data problem versus no economic explanation of default).
- **calculate** the value of a bond and its credit spread, given assumptions about the credit risk parameters (V6 p.199) ^los-06-04-e
    - Examiner asks: value a fixed-rate bond or floater on a binomial tree assuming no default, build the CVA table with tree-based expected exposures, report fair value as VND minus CVA, and convert to a credit spread or discount margin.
- **interpret** changes in a credit spread (V6 p.199) ^los-06-04-f
    - Examiner asks: which change (doubling the default probability versus halving the recovery rate) widens the spread more, or decompose an observed spread move into POD, LGD, liquidity and tax components of the XVA family.
- **explain** the determinants of the term structure of credit spreads and interpret a term structure of credit spreads (V6 p.199) ^los-06-04-g
    - Examiner asks: match a curve shape (flat, upward, steep, inverted) to credit quality, financial conditions, supply and demand, or company-value drivers, and recognize that a distressed bond trades at its recovery value so the inverted curve is an optical effect.
- **compare** the credit analysis required for securitized debt to the credit analysis of corporate debt (V6 p.199) ^los-06-04-h
    - Examiner asks: given the granularity and homogeneity of an asset pool, pick book, portfolio or loan-by-loan analysis, and identify covered bond features (dual recourse, dynamic cover pool, hard bullet versus soft bullet versus conditional pass-through).

## Core intuition

The credit spread between a corporate bond and a maturity-matched government bond is the market's rent for two distinct things: how likely the issuer is to default and how much the investor loses if it does (V6 p.200).
Default risk is the narrow concept, the probability of the event; credit risk is the broad one, probability times severity, which is why a well-collateralized loan can have high default risk and low credit risk at the same time (V6 p.200).
The module's machinery makes this rent explicit.
Take the bond's promised cash flows, ask what the position is worth at each future date if default happens then (the expected exposure), take away what the creditor claws back (the recovery), and what remains is the loss given default (V6 p.200, p.201, p.203).
Weight each date's LGD by the probability that default happens exactly then, discount at risk-free rates, and add it up.
That sum is the credit valuation adjustment, the price of the credit risk in present value terms (V6 p.202, p.203).

> [!abstract] Idea 1: fair value of a risky bond is VND minus CVA
> Value the bond as if it could never default (VND), using benchmark discount factors or the benchmark binomial tree.
> Then subtract the CVA, the sum over dates of LGD times POD times the risk-free discount factor.
> The same compensation can be quoted two ways: as the CVA in present value per 100 par at Date 0, or as the credit spread in annual yield terms over the benchmark (V6 p.203, p.221, p.222).

The probabilities in the table are risk-neutral, not historical.
A one-year bond priced at par with a historical default rate of 1% would be worth more than its market price if you discounted the actual expected payoff at the risk-free rate; the market price of 100 implies a larger default probability, 1.60% in the text's example (V6 p.201, p.202).
Risk-neutral PODs exceed actual PODs for two reasons: investors demand a premium for uncertainty over the timing of default losses, and observed spreads bundle in liquidity and tax differences that the model attributes to credit (V6 p.202, p.235).
The year-by-year PODs are conditional probabilities, hazard rates: each year's POD is the constant annual default probability applied to the survivors, so POD on Date t equals the hazard rate times the probability of survival through Date t-1, and the POS after t years of a constant hazard is (1 minus the hazard) to the power t (V6 p.203).
The hazard rate does not need to be constant; the floater example raises it from 0.50% to 0.75% in later years, and the term structure section raises it in steps to generate an upward-sloping spread curve (V6 p.227, p.242).
The whole engine can run in reverse: given the observed price and a recovery assumption, trial-and-error search finds the implied annual POD, and for a fixed price the assumed POD and recovery rate are positively correlated, since a higher recovery (smaller LGD) must be offset by a higher default probability (V6 p.205).

Where do the PODs come from?
Two families of models (V6 p.213).
Structural models start from the balance sheet: the company defaults when the asset value falls below a default barrier set by its liabilities, so equity is a call option on the assets struck at the face value of debt, and debt is the assets minus that call, equivalently a default-free bond minus a put on the assets (V6 p.213, p.215, p.216).
The default probability is endogenous, the slice of the future asset value distribution below the barrier, and it rises with asset volatility, time and leverage (V6 p.215).
The weakness is data: company assets do not trade, and the default barrier is hard to measure, especially when companies hide debt, which is exactly when you need the model most (V6 p.213, p.214).
Reduced-form models give up on explaining why default happens and model when, as a Poisson process whose intensity (the hazard rate) is estimated by regression on observable company and macro variables (V6 p.214).
Their strength is observable inputs that can track the business cycle; their weakness is that default arrives as a statistical surprise, whereas real defaults are usually preceded by a string of downgrades, as RadioShack's slide from AAA in 1983 to D in 2015 shows (V6 p.211, p.214).
The practical division of labor: structural models suit insiders (management, banks' internal risk systems, rating agencies), reduced-form models suit pricing debt and credit derivatives from market data (V6 p.216, p.217).

> [!abstract] Idea 2: interest rate volatility enters credit valuation only through the expected exposure
> On a binomial tree calibrated to the benchmark par curve, the VND of an option-free bond is identical at 10% and 20% volatility; volatility never changes default-free value.
> But the expected exposure at each date is the probability-weighted bond value across nodes plus the coupon, and the lognormal tree spreads rates asymmetrically around the forward, so higher volatility slightly lowers expected exposures and the CVA (3.5390 versus 3.5394 in the text).
> Credit risk makes an option-free bond volatility-sensitive, which is otherwise true only of bonds with embedded options (V6 p.221, p.224, p.225).

Credit scores and ratings are third-party summaries of this risk for markets that cannot run the model: scores (FICO 300 to 850) in retail lending, ratings in wholesale bond markets (V6 p.208, p.210).
Ratings order issuers by probability of default and fold in loss given default through notching of specific issues off the senior unsecured issuer rating, which is why they are credit ratings and not just default ratings (V6 p.211).
Ratings move, and the transition matrix prices that movement: because downgrade probabilities exceed upgrade probabilities and downgrade spread jumps are larger than upgrade spread compressions, expected migration shaves the expected one-year return below the promised YTM even with no default (V6 p.212).
The mechanical bridge is duration: each migration's price effect is minus modified duration times the spread change, and the probability-weighted sum adjusts the YTM (V6 p.212).

Spread changes decompose along the same lines as the CVA.
The benchmark yield carries the macro factors (expected inflation, expected real rate); the spread carries the micro factors: expected default loss first, then liquidity and taxation, the trio the derivatives world generalizes into the XVA family (CVA, FVA, LVA, TVA) (V6 p.232, p.233).
Within the credit component, a POD change moves the spread more than an equal-sized proportional recovery change, because the POD multiplies the entire loss while the recovery only rescales it: doubling the POD on the three-year bond widened the spread from 90 bps to 182 bps, while halving the recovery moved it to 121 bps (V6 p.236, p.237).

> [!abstract] Idea 3: the term structure of credit spreads is the market's forecast of hazard rates, until distress turns it into arithmetic on the recovery rate
> Stable hazard rates give a flat spread curve; hazard rates that rise with maturity give an upward slope (62 bps at 3 years, 86 at 5, 132 at 10 in the text's stepped-hazard example).
> High-grade issuers sit near the zero lower bound of spreads, so migration can only widen them and their curves are flat to slightly upward sloping.
> A bond expected to default trades at its recovery value at every maturity, so the shorter bond shows the huge annualized spread and the curve inverts steeply, an optical effect, not a maturity preference (V6 p.239, p.242, p.243, p.244).

Securitized debt swaps the single-issuer balance sheet for a pool of assets in an SPE, so the analysis pivots on three questions (V6 p.244, p.245).
First, the collateral: granularity (how many obligations) and homogeneity (how alike they are) select the technique, a statistics-based book approach for short-term granular homogeneous pools, a portfolio approach for medium-term dynamic granular pools, and loan-by-loan work for non-granular heterogeneous pools such as CMBS and leveraged loan CLOs (V6 p.245, p.246).
Second, the servicer: origination standards, documentation and collection capability are ongoing operational and counterparty risks, gauged from seasoned deals of the same servicer (V6 p.246, p.247).
Third, the structure: bankruptcy remoteness through a true sale to the SPE, and enhancements such as overcollateralization, tranching, performance triggers and excess spread (V6 p.247).
Covered bonds are the hybrid: senior bank debt with dual recourse to the issuer and a dynamic, replenished cover pool, redemption regimes from hard bullet to soft bullet to conditional pass-through, and ratings typically several notches above the issuing bank (V6 p.247, p.248).

## Formulas and derivations

**Loss given default and loss severity** (V6 p.201, p.203)
$$
LGD_t = EE_t \times (1 - RR), \qquad \text{Loss severity} = 1 - RR
$$
^f-06-04-1

- $EE_t$: expected exposure at date $t$ per 100 of par, the amount at risk before recovery; $RR$: recovery rate as a fraction of the exposure (interest as well as principal).
- Recovery is assumed instantaneous and proportional to the whole exposure, so LGD is just the unrecovered fraction of what the position is worth at the default date.
- The one-year 4% bond at par has exposure 104 and, at 40% recovery, LGD $= 104 \times 0.60 = 62.4$ (V6 p.201).

**Risk-neutral default probability from a one-period price** (V6 p.202)
$$
\text{Price} = \frac{\big[FV_{nd} \times (1 - P^*)\big] + \big(FV_{def} \times P^*\big)}{1 + r_f}
$$
^f-06-04-2

- $FV_{nd}$: payoff with no default (coupon plus principal); $FV_{def}$: payoff in default (recovery); $r_f$: risk-free rate; $P^*$: risk-neutral POD.
- Discounting at the risk-free rate, not the bond's YTM, is the defining move of risk-neutral valuation; solving $100 = [104(1-P^*) + 41.6P^*]/1.03$ gives $P^* = 1.60\%$ against an actual default rate of 1% (V6 p.201, p.202).
- $P^*$ exceeds the actual probability because of the default timing risk premium and the liquidity and tax content of observed spreads (V6 p.202).

**Hazard rate, conditional POD and probability of survival** (V6 p.203)
$$
POD_t = h \times POS_{t-1}, \qquad POS_t = POS_{t-1} - POD_t = (1 - h)^t
$$
^f-06-04-3

- $h$: annual (hazard) default probability, conditional on no prior default; $POS_0 = 100\%$.
- Each year's POD is the hazard applied to the survivors, so PODs shrink over time even with constant $h$; the cumulative POD is the sum of the annual PODs and equals $1 - (1-h)^T$.
- With $h = 1.25\%$: POD sequence 1.2500%, 1.2344%, 1.2189%, 1.2037%, 1.1887%, cumulative 6.0957%, and $POS_5 = 0.9875^5 = 93.9043\%$ (V6 p.202, p.203).
- The hazard can change over the bond's life; then $POS_t = POS_{t-1} - h_t \times POS_{t-1}$ date by date (V6 p.227, p.242).

**Expected exposure with no interest rate volatility** (V6 p.202, p.206, p.207)
$$
EE_t^{zero} = \frac{100}{(1 + r_f)^{T-t}}, \qquad EE_t^{coupon} = c + \sum_{k=t+1}^{T} \frac{CF_k}{(1 + r_f)^{k-t}}
$$
^f-06-04-4

- With a flat curve and no volatility, exposure is the bond's value at date $t$ discounted at the risk-free rate, plus the coupon then due.
- Five-year zero at 3%: Date 1 exposure $100/1.03^4 = 88.8487$; Example 2's 5% coupon bond at 2.5%: Date 1 exposure $5 + 5/1.025 + 105/1.025^2 = 109.8186$ (V6 p.202, p.206, p.207).

**Credit valuation adjustment** (V6 p.202, p.203)
$$
CVA = \sum_{t=1}^{T} LGD_t \times POD_t \times DF_t
$$
^f-06-04-5

- $DF_t$: default-risk-free discount factor for date $t$ (from the flat curve or the bootstrapped benchmark curve); $LGD_t \times POD_t$ is the expected loss for date $t$.
- The CVA is the present value of all expected default losses, the market price of the bond's credit risk as of Date 0 (V6 p.202, p.203).

> [!tip] Calculator
> One CVA row on the BA II Plus: exposure `100 ÷ 1.03 y^x 4 =` (88.8487), LGD `× 0.6 =` (53.3092), expected loss `× 0.0125 =` (0.6664), PV `÷ 1.03 =` (0.6470).
> Keep POS running in memory: `1 - 0.0125 = STO 1`, next POD `0.0125 × RCL 1 =`.

**Fair value of a risky bond** (V6 p.203, p.221)
$$
\text{Fair value} = VND - CVA
$$
^f-06-04-6

- $VND$: value assuming no default, from benchmark discount factors or backward induction through the benchmark tree.
- Five-year zero: $VND = 100 \times 0.862609 = 86.2609$, $CVA = 3.1549$, fair value $83.1060$ (V6 p.203).
- If the market price differs from fair value, the analyst has a buy or sell signal under the assumed credit parameters (V6 p.222).

**Credit spread and its approximation** (V6 p.203)
$$
\text{Spread} = YTM_{risky} - YTM_{benchmark} \approx h \times (1 - RR)
$$
^f-06-04-7

- The exact spread solves the price-yield equation at the fair value; the approximation is the annual default probability times loss severity.
- Five-year zero: YTM from $100/(1+y)^5 = 83.1060$ is 3.77%, spread $= 3.77\% - 3.00\% = 77$ bps; approximation $1.25\% \times 0.60 = 0.75\%$ (V6 p.203).
- For a given price and spread, assumed POD and recovery are positively correlated: at 30% recovery the implied hazard drops to 1.0675% (V6 p.205).

**Expected return under credit migration** (V6 p.212)
$$
\Delta \%P_{i} = -\,MD \times (\text{spread}_{i} - \text{spread}_{current}), \qquad E[R] \approx YTM + \sum_i p_i \, \Delta \%P_i
$$
^f-06-04-8

- $MD$: expected modified duration at the horizon; $p_i$: transition probability from the matrix row of the current rating; the no-change cell contributes zero.
- Migration usually subtracts from return because the probabilities are skewed toward downgrades and downgrade spread changes are larger than upgrade ones (V6 p.212).
- A rated 10-year bond, $MD = 7.2$: expected percentage change $= -0.6342\%$, so expected return is YTM minus 63.42 bps assuming no default (V6 p.212).

> [!tip] Calculator
> Per row: `7.2 +/- × ( 0.015 - 0.011 ) = ` gives -2.88%; accumulate each product `× 0.084 =` into memory with `STO + 2`, then recall the sum.

**Structural model: option interpretation of debt and equity** (V6 p.215, p.216)
$$
D(T) + E(T) = A(T), \quad E(T) = \max[A(T) - K, 0], \quad D(T) = A(T) - \max[A(T) - K, 0] = K - \max[K - A(T), 0]
$$
^f-06-04-9

- $A(T)$: random asset value at debt maturity $T$; $K$: face value of the zero-coupon debt, the default barrier.
- Equity is a long call on the assets struck at $K$ (limited liability, never negative); debtholders own the assets and have written that call, or equivalently own a default-free bond worth $K$ and have written a put on the assets struck at $K$.
- The two readings give identical payoffs in both states ($A(T) > K$ and $A(T) < K$), which is Example 5's point; the put is the value of shareholders' limited liability (V6 p.216).
- POD is endogenous: the probability mass of $A(T)$ below $K$, increasing in asset variance, time and leverage (V6 p.215).

**Bootstrapped discount factors from the benchmark par curve** (V6 p.217, p.218)
$$
100 = \Big(c_N \times \sum_{t=1}^{N-1} DF_t\Big) + (100 + c_N) \times DF_N \;\Rightarrow\; DF_N = \frac{100 - c_N \sum_{t=1}^{N-1} DF_t}{100 + c_N}
$$
^f-06-04-10

- $c_N$: coupon per 100 of the $N$-year par bond; solve sequentially from $N = 1$.
- Par curve -0.25%, 0.75%, 1.50%, 2.25%, 2.75% gives $DF$ = 1.002506, 0.985093, 0.955848, 0.913225, 0.870016 (V6 p.217, p.218).
- A negative one-year yield just means $DF_1 > 1$; the actual instrument is a zero priced above par at 100.2506 (V6 p.217).

**Spot and forward rates from discount factors** (V6 p.218)
$$
z_N = \Big(\frac{1}{DF_N}\Big)^{1/N} - 1, \qquad f_{N-1,1} = \frac{DF_{N-1}}{DF_N} - 1
$$
^f-06-04-11

- $z_2 = (1/0.985093)^{1/2} - 1 = 0.7538\%$; one-year forward two years ahead $= 0.985093/0.955848 - 1 = 3.0596\%$ (V6 p.218).
- The binomial tree spreads its node rates around these forwards for the assumed volatility (V6 p.218, p.219).

**Backward induction with credit-free rates** (V6 p.220)
$$
V_{node} = \frac{0.5 \times (V_{up} + V_{down}) + c}{1 + r_{node}}
$$
^f-06-04-12

- $V_{up}, V_{down}$: next-date values at the two successor nodes; $c$: the coupon due at the next date; $r_{node}$: the one-year rate at the node.
- Pricing the 2.75% benchmark bond back to exactly 100.0000 confirms the tree is calibrated arbitrage free (V6 p.219, p.220).

**VND from benchmark discount factors** (V6 p.221)
$$
VND = \sum_{t=1}^{T} CF_t \times DF_t
$$
^f-06-04-13

- Same answer as backward induction: the 3.50% five-year corporate has $VND = 103.5450$ either way; the tree's advantage is that it also delivers the expected exposures (V6 p.221).
- VND is volatility-invariant for option-free bonds: at 20% volatility the tree still returns 103.5450 (V6 p.224, p.225).

**Expected exposure on the tree, fixed-coupon bond** (V6 p.221, p.222)
$$
EE_t = \sum_{nodes} p_{node} \times V_{node,t} + c
$$
^f-06-04-14

- $p_{node}$: probability of reaching the node (binomial weights 0.0625, 0.25, 0.375, 0.25, 0.0625 at Date 4); $V_{node,t}$: ex-coupon bond value at the node; the certain coupon is added.
- Date 4 for the 3.50% bond: $(0.0625)(96.4659) + (0.25)(97.6692) + (0.375)(98.6769) + (0.25)(99.5175) + (0.0625)(100.2165) + 3.50 = 102.0931$ (V6 p.221, p.222).
- At maturity $EE_T = 100 + c$.

**Floating-rate note: in-arrears coupon and expected exposure** (V6 p.225, p.226, p.227)
$$
c_{t} = (r_{t-1} + QM) \times 100, \qquad EE_t = \sum p_{node,t} V_{node,t} + \sum p_{node,t-1} \, c(r_{t-1})
$$
^f-06-04-15

- $QM$: quoted margin over the one-year benchmark rate; the rate is set at the start of the period and paid at the end, so the coupon arriving at date $t$ uses date $t-1$ node probabilities while the bond value uses date $t$ probabilities.
- Final payment at a Date $T-1$ node with rate $r$: $(r + QM) \times 100 + 100$ (V6 p.226).
- Date 4 exposure of the 0.50% margin floater combines the five Date 4 values with the four Date 3 coupons: 105.6535 (V6 p.227).

**Discount margin of a floater** (V6 p.228, p.229)
$$
V_0(DM) = \text{fair value}, \quad \text{discounting each node at } 1 + r_{node} + DM
$$
^f-06-04-16

- The DM is to a floater what the credit spread is to a fixed-rate bond: the constant addition to every benchmark rate in the tree that reprices the note to its (fair or market) value, found by trial-and-error search.
- Fair value 99.9047 below par means DM (0.52046%) must exceed the quoted margin (0.50%) (V6 p.228, p.229).

**Distressed debt: CVA collapses to VND minus recovery value** (V6 p.244)
$$
CVA_{distressed} = VND - \text{Recovery price}, \qquad \text{Fair value} = \text{Recovery price}
$$
^f-06-04-17

- When default is essentially certain and cross-default clauses hit all maturities, every bond trades at the recovery rate regardless of maturity.
- Five-year zero: fair value 40, yield 20.1124%, spread 17.1124%; ten-year: fair value 40, yield 9.5958%, spread 6.5958%; the steeply inverted spread curve is an optical artifact of annualizing the same dollar loss over different horizons (V6 p.244).

## Worked examples

### Example 1: The five-year zero-coupon CVA table, Exhibits 2 and 3 (V6 p.202 to p.204)

Setup: five-year, zero-coupon corporate bond; flat government curve at 3.00%; hazard rate 1.25% per year; recovery 40% of the exposure; default only at year ends.

Column by column (Formulas 3, 4, 5):

| Date | Exposure | Recovery | LGD | POD | POS | Expected loss | DF | PV of loss |
|---|---|---|---|---|---|---|---|---|
| 1 | 88.8487 | 35.5395 | 53.3092 | 1.2500% | 98.7500% | 0.6664 | 0.970874 | 0.6470 |
| 2 | 91.5142 | 36.6057 | 54.9085 | 1.2344% | 97.5156% | 0.6778 | 0.942596 | 0.6389 |
| 3 | 94.2596 | 37.7038 | 56.5558 | 1.2189% | 96.2967% | 0.6894 | 0.915142 | 0.6309 |
| 4 | 97.0874 | 38.8350 | 58.2524 | 1.2037% | 95.0930% | 0.7012 | 0.888487 | 0.6230 |
| 5 | 100.0000 | 40.0000 | 60.0000 | 1.1887% | 93.9043% | 0.7132 | 0.862609 | 0.6152 |

Walk one row in full, Date 3: exposure $100/1.03^2 = 94.2596$; recovery $94.2596 \times 0.40 = 37.7038$; LGD $= 56.5558$; POD $= 1.25\% \times 97.5156\% = 1.2189\%$; expected loss $= 56.5558 \times 0.012189 = 0.6894$; PV $= 0.6894 \times 0.915142 = 0.6309$ (V6 p.203).
Cumulative POD $= 6.0957\%$ and $POS_5 = 0.9875^5 = 93.9043\%$; they sum to 100%.
CVA $=$ sum of the last column $= 3.1549$.
$VND = 100 \times 0.862609 = 86.2609$; fair value $= 86.2609 - 3.1549 = 83.1060$.
YTM solves $100/(1+y)^5 = 83.1060$, so $y = 3.77\%$ and the spread is 77 bps; the approximation $1.25\% \times 0.60 = 0.75\%$ is close (V6 p.203).
Exhibit 3's default-timing IRRs from a purchase at 83.1060 with recovery of that date's Column 3 amount: -57.24% (Date 1), -33.63%, -23.16%, -17.32%, -13.61% (Date 5), and +3.77% with no default.
The dispersion of outcomes by default timing is the source of the default risk premium inside risk-neutral PODs (V6 p.204, p.205).
Python check: `CVA = 3.1549`, `fair = 83.1060`, `ytm = 3.7704%`, IRRs match to 4 dp (full-precision YTM is 3.7704%, printed as 3.77%). ^ex-06-04-1

### Example 2: Ranking credit risk, curriculum Example 1 (V6 p.205, p.206)

Setup: three bonds, exposures 104, 98, 92; PODs 0.75%, 0.90%, 0.80%; recoveries 40, 35, 30 per 100.

Expected loss $=$ (exposure $-$ recovery) $\times$ POD:
- A: $(104 - 40) \times 0.0075 = 64 \times 0.0075 = 0.480$.
- B: $(98 - 35) \times 0.0090 = 63 \times 0.0090 = 0.567$.
- C: $(92 - 30) \times 0.0080 = 62 \times 0.0080 = 0.496$.

Ranking from highest credit risk: B, C, A.
No trading recommendation is possible because prices are not given.
Python check: `0.480, 0.567, 0.496`. ^ex-06-04-2

### Example 3: Overvalued or undervalued, curriculum Example 2 (V6 p.206, p.207)

Setup: three-year, 5% annual payment corporate at 104; hazard 1.50%; recovery 40%; flat government curve at 2.50%.

Exposures include the coupon (Formula 4): Date 1 $= 5 + 5/1.025 + 105/1.025^2 = 109.8186$; Date 2 $= 5 + 105/1.025 = 107.4390$; Date 3 $= 105$.

| Date | Exposure | Recovery | LGD | POD | POS | Expected loss | DF | PV of loss |
|---|---|---|---|---|---|---|---|---|
| 1 | 109.8186 | 43.9274 | 65.8911 | 1.5000% | 98.5000% | 0.9884 | 0.975610 | 0.9643 |
| 2 | 107.4390 | 42.9756 | 64.4634 | 1.4775% | 97.0225% | 0.9524 | 0.951814 | 0.9066 |
| 3 | 105.0000 | 42.0000 | 63.0000 | 1.4553% | 95.5672% | 0.9169 | 0.928599 | 0.8514 |

CVA $= 2.7222$; $VND = 5/1.025 + 5/1.025^2 + 105/1.025^3 = 107.1401$; fair value $= 104.4178$.
At a market price of 104 the bond is undervalued by about 0.42 per 100.
Buying at 104, the IRRs are -57.76% (default Date 1, receive 43.9274), -33.27% (Date 2), -22.23% (Date 3), and +3.57% with no default, the YTM at 104.
The text twice calls this a five-year bond in the solution narrative; it is the three-year bond, a typo, and the numbers are for three years.
Python check: `CVA = 2.7222`, `VND = 107.1401`, `fair = 104.4178`, IRRs `-0.5776, -0.3327, -0.2223, 0.0357`. ^ex-06-04-3

### Example 4: Credit scoring, curriculum Example 3 (V6 p.209)

Setup: Tess Waresmith's FICO score rose from 760 to 775; which factors explain it?

- A (older, no late payments): helps; age itself is not scored, but average account age and oldest account age are, so time passing improves the score.
- B (limit raised from $1,000 to $2,500, same balance): helps; the debt-to-limit ratio falls, improving the 30% debt burden component.
- C (new car loan): helps; a new type of credit with no late payments benefits the 10% types-of-credit component.
- D (refraining from self-checking): no effect; self-checks are soft inquiries and never enter the score.

So A, B and C explain the improvement; D is a distractor built on confusing soft and hard inquiries (V6 p.208, p.209).
No arithmetic to check. ^ex-06-04-4

### Example 5: Migration drag for an A rated bond, Exhibit 7 (V6 p.212)

Setup: A rated 10-year corporate, expected modified duration 7.2 at horizon; transition row: AAA 0.05%, AA 2.50%, A 87.50%, BBB 8.40%, BB 0.75%, B 0.60%, CCC/CC/C 0.12%, D 0.08%; spreads 0.60%, 0.90%, 1.10%, 1.50%, 3.40%, 6.50%, 9.50%.

Price changes (Formula 8): to AAA $-7.2 \times (0.60\% - 1.10\%) = +3.60\%$; to AA $+1.44\%$; to BBB $-2.88\%$; to BB $-16.56\%$; to B $-38.88\%$; to CCC/CC/C $-60.48\%$.
Probability-weighted sum:
$(0.0005)(3.60\%) + (0.0250)(1.44\%) + (0.8750)(0) + (0.0840)(-2.88\%) + (0.0075)(-16.56\%) + (0.0060)(-38.88\%) + (0.0012)(-60.48\%) = -0.6342\%$.
Expected one-year return $=$ YTM $- 0.6342\%$, assuming no default; for investment grade the 0.08% to D is ignored, but for high yield the default state must be added (V6 p.212).
Python check: `-0.6342%`. ^ex-06-04-5

### Example 6: Migration drag for a AAA bond, curriculum Example 4 (V6 p.213)

Setup: AAA rated 10-year corporate, modified duration 7.3 at horizon; AAA row of Exhibit 7.

Price changes: to AA $-7.3 \times (0.90\% - 0.60\%) = -2.19\%$; to A $-3.65\%$; to BBB $-6.57\%$; to BB $-20.44\%$; to B $-43.07\%$; to CCC/CC/C $-64.97\%$.
Weighted sum:
$(0.9000)(0) + (0.0900)(-2.19\%) + (0.0060)(-3.65\%) + (0.0015)(-6.57\%) + (0.0010)(-20.44\%) + (0.0010)(-43.07\%) + (0.0005)(-64.97\%) = -0.3249\%$.
Expected return is YTM less about 32.5 bps even though AAA cannot be upgraded, the pure one-sidedness of migration at the top of the scale.
Python check: full precision gives $-0.3248\%$; the curriculum's $-0.3249\%$ uses the rounded per-transition price changes, an immaterial rounding difference. ^ex-06-04-6

### Example 7: Put-based reading of the structural model, curriculum Example 5 (V6 p.216)

Setup: show that Feely's decomposition, equity $= A(T) - K$ plus a long put struck at $K$, debt $= K$ minus that put, matches the call-based model.

$E(T) = A(T) - K + \max[K - A(T), 0]$ and $D(T) = K - \max[K - A(T), 0]$.
If $A(T) > K$: put expires worthless, $E(T) = A(T) - K$, $D(T) = K$, same as the call version in the money.
If $A(T) < K$: put pays $K - A(T)$, so $E(T) = 0$ and $D(T) = A(T)$, same as the call version out of the money.
The put's value is the price of shareholders' limited liability, purchased from the debtholders; risky debt $=$ default-free debt $-$ put on assets.
Both readings restate $D(T) + E(T) = A(T)$, so they must agree state by state. ^ex-06-04-7

### Example 8: VND and CVA on the tree, Exhibits 9 to 13 (V6 p.217 to p.222)

Setup: benchmark par curve -0.25%, 0.75%, 1.50%, 2.25%, 2.75%; 10% volatility tree (Exhibit 10); five-year 3.50% annual payment corporate; hazard 1.25%; recovery 40%.

Step 1, bootstrap (Formula 10): $DF_1 = 100/99.75 = 1.002506$; then 0.985093, 0.955848, 0.913225, 0.870016; spots -0.2500%, 0.7538%, 1.5166%, 2.2953%, 2.8240%; forwards 1.7677%, 3.0596%, 4.6674%, 4.9664% (V6 p.217, p.218).
Step 2, check calibration: the 2.75% government bond prices to 100.0000 through the tree, for example Date 4 top node $102.75/1.072918 = 95.7669$ and Date 3 top node $[(0.5)(95.7669) + (0.5)(96.9614) + 2.75]/1.062197 = 93.3105$ (V6 p.219, p.220).
Step 3, VND: backward induction gives 103.5450, identical to $3.50 \times (1.002506 + 0.985093 + 0.955848 + 0.913225) + 103.50 \times 0.870016 = 103.5450$ (V6 p.221).
Step 4, expected exposures (Formula 14), for example Date 4: $(0.0625)(96.4659) + (0.25)(97.6692) + (0.375)(98.6769) + (0.25)(99.5175) + (0.0625)(100.2165) + 3.50 = 102.0931$.

| Date | Expected exposure | LGD | POD | DF | CVA per year |
|---|---|---|---|---|---|
| 1 | 103.2862 | 61.9717 | 1.2500% | 1.002506 | 0.7766 |
| 2 | 101.5481 | 60.9289 | 1.2344% | 0.985093 | 0.7409 |
| 3 | 101.0433 | 60.6260 | 1.2189% | 0.955848 | 0.7064 |
| 4 | 102.0931 | 61.2559 | 1.2037% | 0.913225 | 0.6734 |
| 5 | 103.5000 | 62.1000 | 1.1887% | 0.870016 | 0.6422 |

CVA $= 3.5394$; fair value $= 103.5450 - 3.5394 = 100.0056$.
YTM at that price is 3.4988%, so the spread over the 2.75% five-year par yield is 0.7488%, about 75 bps; the same credit risk as a Date 0 amount (3.5394) or an annual rate (74.88 bps) (V6 p.222).
Python check: bootstrap, tree values, `CVA = 3.5394`, `fair = 100.0056`, `ytm = 3.4988%`. ^ex-06-04-8

### Example 9: Buy or pass on a high-yield bond, curriculum Example 6 (V6 p.223, p.224)

Setup: three-year, 4.00% annual payment bond priced at 104; Boller's parameters: hazard 2.25%, recovery 40%, 10% volatility, same benchmark curve and tree.

VND by backward induction: Date 2 values $104/1.037026 = 100.2868$, $104/1.030315 = 100.9400$, $104/1.024820 = 101.4812$; Date 1 values $[(0.5)(100.2868) + (0.5)(100.9400) + 4]/1.019442 = 102.6183$ and $[(0.5)(100.9400) + (0.5)(101.4812) + 4]/1.015918 = 103.5621$; Date 0 $[(0.5)(102.6183) + (0.5)(103.5621) + 4]/0.997500 = 107.3586$.
Expected exposures: Date 1 $(0.5)(102.6183) + (0.5)(103.5621) + 4 = 107.0902$; Date 2 $(0.25)(100.2868) + (0.5)(100.9400) + (0.25)(101.4812) + 4 = 104.9120$; Date 3 $= 104$.
PODs: 2.25%, $2.25\% \times 97.75\% = 2.1994\%$, $2.25\% \times 97.75\%^2 = 2.1499\%$.

| Date | Expected exposure | LGD | POD | DF | CVA per year |
|---|---|---|---|---|---|
| 1 | 107.0902 | 64.2541 | 2.2500% | 1.002506 | 1.4493 |
| 2 | 104.9120 | 62.9472 | 2.1994% | 0.985093 | 1.3638 |
| 3 | 104.0000 | 62.4000 | 2.1499% | 0.955848 | 1.2823 |

CVA $= 4.0954$; fair value $= 107.3586 - 4.0954 = 103.2632 < 104$, so the bond is overvalued at the market price and Boller declines to buy.
Python check: `VND = 107.3586`, `CVA = 4.0954`, `fair = 103.2632`. ^ex-06-04-9

### Example 10: Volatility touches CVA, not VND, Exhibits 15 and 16 (V6 p.224, p.225)

Setup: same 3.50% five-year corporate, same credit parameters, but a 20% volatility tree.

The Date 4 rate range widens from 3.2764% to 7.2918% (10% vol) to 2.0948% to 10.3757% (20% vol), yet backward induction still returns $VND = 103.5450$: volatility cannot change a default-free option-free value on a calibrated tree.
Expected exposures dip slightly for Dates 2 to 4 (101.5423, 101.0233, 102.0636 versus 101.5481, 101.0433, 102.0931) because the lognormal tree is asymmetric around the forwards: the top rates move up more than the bottom rates move down, and the lower bond values at the top nodes dominate.
CVA $= 3.5390$ versus 3.5394, fair value $100.0060$ versus $100.0056$: a small volatility effect that exists only because of credit risk (V6 p.225).
Python check: `VND(20%) = 103.5450`, `CVA = 3.5390`, `fair = 100.0060`. ^ex-06-04-10

### Example 11: The risky floater and its discount margin, Exhibits 17 to 19 (V6 p.225 to p.229)

Setup: five-year floater paying the one-year benchmark rate plus a 0.50% quoted margin, in arrears; 10% volatility tree; hazard 0.50% and recovery 20% for Dates 1 to 3, then 0.75% and 10% for Dates 4 and 5.

VND: coupons sit one date after the rate that sets them, for example the Date 1 payment is $(-0.25\% + 0.50\%) \times 100 = 0.25$ and the Date 5 payoff after a 4.8878% Date 4 rate is 105.3878.
Backward induction gives node values barely above 100 everywhere (that is the point of a floater; at a zero quoted margin they would all be exactly 100) and $VND = 102.3633$ (V6 p.226).
Expected exposure mixes probability dates (Formula 15), for example Date 4:
$[(0.0625)(100.4660) + (0.25)(100.4718) + (0.375)(100.4767) + (0.25)(100.4808) + (0.0625)(100.4841)] + [(0.125)(6.7197) + (0.375)(5.5922) + (0.375)(4.6692) + (0.125)(3.9134)] = 105.6535$.

| Date | Expected exposure | LGD | POD | DF | CVA per year |
|---|---|---|---|---|---|
| 1 | 102.1074 | 81.6859 | 0.5000% | 1.002506 | 0.4095 |
| 2 | 103.6583 | 82.9266 | 0.4975% | 0.985093 | 0.4064 |
| 3 | 104.4947 | 83.5957 | 0.4950% | 0.955848 | 0.3955 |
| 4 | 105.6535 | 95.0881 | 0.7388% | 0.913225 | 0.6416 |
| 5 | 105.4864 | 94.9377 | 0.7333% | 0.870016 | 0.6057 |

The POD jump at Date 4 is $0.75\% \times POS_3 = 0.75\% \times 98.5075\% = 0.7388\%$, the worsening hazard applied to the survivors; cumulative POD 2.9646%.
CVA $= 2.4586$; fair value $= 102.3633 - 2.4586 = 99.9047$, below par, so the discount margin must exceed the quoted margin.
Adding a trial DM to every node rate and searching reprices the floater to 99.9047 at $DM = 0.52046\%$ (V6 p.228, p.229).
Python check: `VND = 102.3633`, `CVA = 2.4586`, `fair = 99.9047`, `DM = 0.52046%`. ^ex-06-04-11

### Example 12: Distressed floater, curriculum Example 7 (V6 p.229 to p.232)

Setup: three-year floater at the one-year rate plus 2.50%, rated CCC, priced at 84; hazard 30% for Year 1, then 10% per year; recovery 50% to 60%; 10% volatility.

VND: Date 2 values 102.4107, 102.4264, 102.4395; Date 1 values 104.8248 and 104.8557; $VND = [(0.5)(104.8248) + (0.5)(104.8557) + 2.25]/0.9975 = 107.3586$.
Expected exposures: 107.0902, 106.6938, 105.5619.
PODs: 30%, $10\% \times 70\% = 7\%$, $10\% \times 63\% = 6.3\%$; cumulative 43.3%.
At 50% recovery: LGDs 53.5451, 53.3469, 52.7810; CVA $= 16.1038 + 3.6786 + 3.1784 = 22.9608$; fair value $= 107.3586 - 22.9608 = 84.3978$.
At 60% recovery: LGDs 42.8361, 42.6775, 42.2248; CVA $= 18.3686$; fair value $= 88.9900$.
At the 84 market price the floater is fairly priced under 50% recovery and clearly cheap under 60%, so Yassin recommends buying.
The DM at the market price of 84 is 8.9148%, far above the 2.50% quoted margin, the deep-discount signature (V6 p.231, p.232).
Python check: `VND = 107.3586`, CVAs `22.9608` and `18.3686`, fairs `84.3978` and `88.9900`, `DM = 8.9148%`. ^ex-06-04-12

### Example 13: From spreads to implied PODs and back, Exhibits 23 to 25 (V6 p.233 to p.235)

Setup: the 3.50% five-year corporate ($VND = 103.5450$); find hazard rates consistent with rating-level spreads at 40% recovery, then change the recovery.

For a 0.60% AAA spread, trial-and-error gives hazard 1.01%: PODs 1.0100%, 0.9998%, 0.9897%, 0.9797%, 0.9698% (cumulative 4.9490%), CVA $= 2.8731$, fair value $100.6719$, YTM 3.35%, spread $= 3.35\% - 2.75\% = 0.60\%$.
Repeating per rating (V6 p.234):

| Rating | Spread | Annual POD | Cumulative POD |
|---|---|---|---|
| AAA | 0.60% | 1.01% | 4.95% |
| AA | 0.90% | 1.49% | 7.23% |
| A | 1.10% | 1.83% | 8.82% |
| BBB | 1.50% | 2.48% | 11.80% |
| BB | 3.40% | 5.64% | 25.19% |
| B | 6.50% | 10.97% | 44.07% |
| CCC, CC, C | 9.50% | 16.50% | 59.41% |

These risk-neutral PODs dwarf historical AAA default rates because they carry the timing risk premium plus liquidity and tax effects (V6 p.234, p.235).
Recovery next: keep hazard 1.83% but cut recovery from 40% to 30%; LGDs rise (72.3003, 71.0837, 70.7303, 71.4652, 72.4500), CVA rises to 5.9781, fair value falls to 97.5670, YTM 4.05%, spread 1.30%.
That 20 bp widening for subordination is exactly how notching translates a lower recovery into a lower issue rating (V6 p.235).
Python check: hazard search reproduces the table to within 0.01% (rounding in the curriculum's trial-and-error), `CVA(1.01%) = 2.8731`, `fair = 100.6719`; `CVA(1.83%, 30%) = 5.9781`, `fair = 97.5670`. ^ex-06-04-13

### Example 14: POD versus recovery sensitivity, curriculum Example 8 (V6 p.235 to p.237)

Setup: three-year, 3% annual payment corporate on the 20% volatility tree; base case hazard 1.50%, recovery 40%.

Base: Date 2 node values 98.6591, 100.0492, 101.0032; Date 1 values 100.2313, 102.0770; $VND = 104.4152$.
Expected exposures 104.1541, 102.9402, 103.0000; CVA $= 2.6984$; fair value $101.7168$; YTM 2.40%; spread $= 2.40\% - 1.50\% = 0.90\%$.
Double the POD to 3.00% (recovery 40%): PODs 3.0000%, 2.9100%, 2.8227%; CVA $= 5.3174$; fair value $99.0978$; YTM 3.32%; spread 1.82%.
Halve the recovery to 20% (hazard 1.50%): LGDs jump to 83.3233, 82.3522, 82.4000; CVA $= 3.5978$; fair value $100.8173$; YTM 2.71%; spread 1.21%.
Kapili's intuition is right: doubling POD widens the spread by 92 bps, halving recovery by only 31 bps, because POD scales the whole expected loss while recovery only rescales LGD.
Python check: `VND = 104.4152`, CVAs `2.6984, 5.3174, 3.5978`, fairs `101.7168, 99.0978, 100.8173`, YTMs `2.40%, 3.32%, 2.71%`. ^ex-06-04-14

### Example 15: Hazard rates and the shape of the spread curve, Exhibits 31 and 32 and the distressed case (V6 p.241 to p.244)

Setup: zero-coupon bonds, flat 3.00% benchmark, 40% recovery.

Raise the flat hazard from 1.25% to 1.50% on the five-year zero: expected losses rise to 0.7996 through 0.8472, CVA $= 3.7670$, fair value $= 86.2609 - 3.7670 = 82.4939$, YTM 3.9240%, spread 92.40 bps versus 77 bps before: a parallel hazard rise widens the whole curve (V6 p.242).
Now step the hazard by horizon: 1.00% in Years 1 to 3, 2.00% in Years 4 and 5, 3.00% in Years 6 to 10.
- 3-year: CVA $= 1.6308$, fair $= 91.5142 - 1.6308 = 89.8833$, YTM 3.6192%, spread 61.92 bps.
- 5-year: CVA $= 3.5259$ (PODs jump to 1.9406% and 1.9018% in Years 4 and 5), fair $= 82.7350$, YTM 3.8633%, spread 86.33 bps.
- 10-year: cumulative POD 19.9767%, CVA $= 8.9187$, fair $= 74.4094 - 8.9187 = 65.4907$, YTM 4.3235%, spread 132.35 bps.

Rising expected hazards produce the upward-sloping spread curve typical of investment grade (V6 p.242, p.243).
Distress flips it: if default is imminent and both the 5-year and 10-year bonds trade at the 40 recovery value, then CVA $= VND - 40$ (46.2609 and 34.4094), and the yields are $(100/40)^{1/5} - 1 = 20.1124\%$ and $(100/40)^{1/10} - 1 = 9.5958\%$, spreads 17.1124% and 6.5958%.
The steep inversion is an optical effect of annualizing the same dollar outcome over different horizons, not a maturity view (V6 p.244).
Python check: all CVAs, fair values, YTMs and spreads reproduce to 4 dp. ^ex-06-04-15

## Item-set patterns

> [!warning] Trap 1: expected exposure versus LGD versus expected loss
> The vignette gives exposure, recovery rate and POD for several bonds and asks which has the most credit risk, or what the exposure is.
> Correct: exposure is before recovery (coupon plus principal, 100 + 5 = 105 for a one-year 5% bond); LGD is exposure times (1 - recovery); credit risk ranks on expected loss = LGD x POD.
> Distractors: ranking on POD alone (default risk, not credit risk), subtracting recovery from the exposure when the question asks for exposure, or ranking on LGD and ignoring POD (V6 p.200, p.201, p.206, p.252).

> [!warning] Trap 2: the conditional POD chain
> A table asks for the Date 3 POD given a 1.25% annual default probability.
> Correct: POD_3 = 1.25% x POS_2 = 1.25% x (0.9875)^2 = 1.2189%; POS declines by each POD; cumulative POD is the sum of the column.
> Distractors: using 1.25% flat for every date, computing POS as 1 - t x 1.25%, or treating cumulative POD as 1.25% x t (V6 p.203).

> [!warning] Trap 3: risk-neutral versus actual default probabilities
> A statement claims actual probabilities include the timing risk premium, or that the spread is pure credit risk.
> Correct: the risk-neutral POD is larger; it embeds the premium for uncertainty over default timing, and observed spreads also carry liquidity and tax effects.
> Distractors: Observation-1-style claims attaching the premium to actual probabilities, and any answer discounting risk-neutral payoffs at the bond's own YTM instead of the risk-free rate (V6 p.202, p.235, p.252).

> [!warning] Trap 4: migration math sign and base
> Given a transition row, spreads and modified duration, compute the expected return.
> Correct: each transition's price change is minus duration times (new spread - old spread); weight by probabilities including zero for staying put; expected return is YTM plus the (usually negative) sum.
> Distractors: using the destination spread instead of the spread change (-8.00% in PP Q6), applying duration to yields not spreads, forgetting the minus sign, or weighting by the wrong matrix row (V6 p.212, p.253).

> [!warning] Trap 5: structural versus reduced-form fingerprints
> A model description must be classified.
> Correct: option pricing on assets, default barrier, equity volatility from the stock price = structural (endogenous default, why); regression of default intensity on leverage, ROA, macro variables = reduced-form (exogenous default, when).
> Distractors: "reduced-form is newer so better" (age is immaterial), "structural is too complex to compute" (the real weakness is unobservable inputs), calling a rating-prediction regression a structural model (V6 p.213, p.214, p.256).

> [!warning] Trap 6: tree exposures need the coupon and the right probabilities
> A CVA table on a binomial tree must be completed.
> Correct: expected exposure at date t is the node-probability-weighted bond value plus the coupon; for a floater, the coupon term uses date t-1 probabilities because rates set in arrears.
> Distractors: omitting the coupon, using 0.5/0.5 weights at every date instead of binomial weights (0.25, 0.50, 0.25 at Date 2), or discounting the expected losses at the corporate yield instead of benchmark factors (V6 p.221, p.227).

> [!warning] Trap 7: which spread the question wants
> After computing fair value, the item asks for "the credit spread over a theoretical comparable government bond with the same coupon".
> Correct: compute the corporate YTM at fair value and subtract the YTM of a government bond with identical cash flows priced at VND (1.08% in PP Q17).
> Distractors: spread over the par yield from the exhibit (1.01%), or reporting the government YTM itself (2.25% or 2.18%) as the spread (V6 p.256, p.267).

> [!warning] Trap 8: POD versus recovery sensitivity
> The vignette doubles the default probability and separately halves the recovery rate and asks which widens the spread more.
> Correct: the POD change dominates (90 to 182 bps versus 90 to 121 bps); VND never changes when credit parameters change.
> Distractors: claiming VND falls, expecting symmetric effects, or reasoning that recovery "matters more because LGD is bigger" (V6 p.236, p.237).

> [!warning] Trap 9: the inverted distressed curve
> A high-likelihood-of-default issuer shows short-maturity spreads far above long ones and the item asks for the interpretation.
> Correct: all its bonds trade near the recovery price because of cross-default provisions; the inversion is an optical effect of annualizing the same loss over different horizons, not a market view that long bonds are safer.
> Distractors: "long-term bonds have less credit risk", "the market expects rapid recovery" (that is the cyclical-industry inversion, a different case), or treating the spread curve as informative about risk-reward across maturities (V6 p.243, p.244).

> [!warning] Trap 10: securitized debt approach matching
> An ABS pool is described (size, number, similarity, static or dynamic) and an approach must be chosen.
> Correct: granular + homogeneous + short-term static book = statistics-based book approach; granular + homogeneous + medium-term dynamic = portfolio approach; non-granular or heterogeneous = loan by loan.
> Distractors: loan-by-loan for thousands of similar auto loans (inefficient), statistics on a changing pool (needs the portfolio approach), or corporate-style issuer analysis that ignores servicer and structure (V6 p.245, p.246, p.260).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM04-Credit-Analysis-Models-Practice-Problems]]

## Cross-links

- [[LM01-The-Term-Structure-and-Interest-Rate-Dynamics]]: supplies the spot, forward and bootstrapping machinery reused here to build benchmark discount factors from the par curve and to discount expected losses.
- [[LM02-The-Arbitrage-Free-Valuation-Framework]]: the calibrated binomial tree and backward induction from that module are the engine for VND and for the expected exposures in the CVA table; the calibration check (benchmark bond prices back to par) is identical.
- [[LM03-Valuation-and-Analysis-of-Bonds-with-Embedded-Options]]: volatility changes option-free bond values only through credit (this module's point); contrast with callables and putables where volatility works through the embedded option, and with OAS as the spread measure there.
- [[LM05-Credit-Default-Swaps]]: hazard rates, POD, LGD and the expected-loss logic built here price CDS protection legs; the distressed-curve trade (sell short protection, buy long protection) is executed in the CDS market.
- [[LM04-Analysis-of-Financial-Institutions]]: the credit analysis of banks in FSA complements the covered bond and securitization discussion, since dual recourse quality depends on the issuing institution's balance sheet.

## Self-test

Vignette A for Q1 to Q6: Ana Rojas values a three-year, 4% annual payment corporate bond.
The government yield curve is flat at 2.00%, the annual (hazard) probability of default is 2.00% with default only at year ends, and the recovery rate is 40% of the exposure.
There is no interest rate volatility.
She computes exposures of 107.8831, 105.9608 and 104.0000 for Dates 1 to 3.

> [!question] Q1
> The Date 2 probability of default in Rojas's CVA table is closest to:
> A. 1.9208%.
> B. 1.9600%.
> C. 2.0000%.

> [!question] Q2
> The credit valuation adjustment for the bond is closest to:
> A. 3.5964.
> B. 3.7393.
> C. 5.8808.

> [!question] Q3
> The fair value of the bond is closest to:
> A. 102.17.
> B. 104.00.
> C. 105.77.

> [!question] Q4
> The bond's credit spread is closest to its:
> A. hazard rate times the recovery rate.
> B. hazard rate times one minus the recovery rate.
> C. cumulative probability of default divided by three.

> [!question] Q5
> If Rojas raises the recovery assumption to 50% and leaves the hazard rate unchanged, the fair value:
> A. rises to about 102.77.
> B. falls to about 101.57.
> C. is unchanged, because recovery affects only the loss severity, not the price.

> [!question] Q6
> An investor buys the bond at Rojas's fair value and the issuer defaults on Date 2, paying the assumed recovery on that date.
> The annualized return is closest to:
> A. -21.4%.
> B. -33.6%.
> C. -59.1%.

Vignette B for Q7 to Q10: Mikel Sanz reviews three positions.
Position 1 is a BB rated bond, YTM 6.20%, expected modified duration 4.8 at the one-year horizon; the BB transition row (excluding default) is AAA 0.01%, AA 0.06%, A 0.30%, BBB 7.75%, BB 79.50%, B 8.75%, CCC/CC/C 2.38%, with 10-year spreads 0.60%, 0.90%, 1.10%, 1.50%, 3.40%, 6.50%, 9.50%.
Position 2 is an issuer whose default probability a consultant estimates as the portion of the future asset value distribution lying below a barrier set by the firm's liabilities, with volatility inferred from the traded equity.
Position 3 is a distressed issuer with 4-year and 8-year zero-coupon bonds, cross-default provisions, and both bonds priced at 45 per 100 of par; the benchmark curve is flat at 3%.
Sanz also holds an ABS backed by a static, short-term book of thousands of similar trade receivables.

> [!question] Q7
> Ignoring the probability of default, the expected one-year return on the BB bond is closest to:
> A. 4.95%.
> B. 6.20%.
> C. 7.45%.

> [!question] Q8
> The consultant's model for Position 2 is best described as:
> A. reduced-form, because equity prices are observable market data.
> B. structural, because default is endogenous to the balance sheet and has the features of an option.
> C. structural, because the default intensity is estimated with regression analysis.

> [!question] Q9
> The credit spreads implied by Position 3's prices (about 19.1% at 4 years and 7.5% at 8 years) are best interpreted as:
> A. evidence that the market considers the 8-year bond much safer.
> B. an optical effect: both bonds trade at the expected recovery value, and the same dollar loss annualizes to a larger spread over the shorter horizon.
> C. a mispricing, because cross-default provisions require equal spreads across maturities.

> [!question] Q10
> For the trade receivables ABS, the most appropriate credit analysis approach is:
> A. loan by loan.
> B. portfolio based.
> C. statistics based on the existing book.

> [!success]- Answer key
> Q1: B.
> POD_2 $=$ hazard times Date 1 survival $= 2.00\% \times 98.00\% = 1.9600\%$ (Python: `0.02*0.98 = 0.0196`).
> A is POD_3 $= 2.00\% \times 96.04\%$; C forgets the conditioning (V6 p.203).
>
> Q2: A.
> LGDs $= 0.60 \times$ exposure: 64.7299, 63.5765, 62.4000; PODs 2.0000%, 1.9600%, 1.9208%; expected losses 1.2946, 1.2461, 1.1986; discounted at 2% (0.980392, 0.961169, 0.942322): 1.2692 + 1.1977 + 1.1294 $= 3.5964$ (Python: `CVA = 3.5964`).
> B is the undiscounted expected-loss sum; C is the cumulative POD from the curriculum's Bond III, a units trap (V6 p.202, p.203).
>
> Q3: A.
> $VND = 4/1.02 + 4/1.02^2 + 104/1.02^3 = 105.7678$; fair value $= 105.7678 - 3.5964 = 102.1714$ (Python: `fair = 102.1714`).
> B is par; C is the VND with no credit adjustment (V6 p.203, p.221).
>
> Q4: B.
> YTM at 102.1714 is 3.229%, spread $= 1.229\%$; the approximation $h(1 - RR) = 2.00\% \times 0.60 = 1.20\%$ is closest (Python: `spread = 1.229%`).
> A gives 0.80% and C gives $5.8808\%/3 = 1.96\%$, both off (V6 p.203).
>
> Q5: A.
> CVA falls to $2.9970$ (LGD scales by $0.50/0.60$), fair value $= 105.7678 - 2.9970 = 102.7708$ (Python: `102.7708`).
> B moves the wrong way; C confuses "recovery does not change VND" with "does not change fair value" (V6 p.205, p.235).
>
> Q6: B.
> Cash flows: 4 at Date 1, recovery $105.9608 \times 0.40 = 42.3843$ at Date 2; solve $102.1714 = 4/(1+r) + 42.3843/(1+r)^2$: $r = -33.61\%$ (Python: `irr = -0.3361`).
> A assumes recovery of the full exposure at Date 3; C uses the LGD as the recovery (V6 p.204, p.207).
>
> Q7: A.
> Price changes from BB: $-4.8 \times (s - 3.40\%)$: +13.44%, +12.00%, +11.04%, +9.12%, 0%, -14.88%, -29.28%.
> Weighted sum $= (0.0001)(13.44) + (0.0006)(12.00) + (0.0030)(11.04) + (0.0775)(9.12) + (0.7950)(0) + (0.0875)(-14.88) + (0.0238)(-29.28) = -1.25\%$ (Python: `-1.2504%`).
> Expected return $= 6.20\% - 1.25\% = 4.95\%$; B ignores migration; C adds the drag (V6 p.212).
>
> Q8: B.
> Default barrier, below-barrier probability mass and equity-implied volatility are the structural (company-value) model; default is endogenous.
> A mislabels because using equity data does not make a model reduced-form; C attaches the reduced-form estimation method to the wrong family (V6 p.213 to p.215).
>
> Q9: B.
> Near-certain default with cross-default provisions makes every maturity trade at the recovery price; $CVA = VND - 45$ for each, and the yields $(100/45)^{1/4} - 1 = 22.09\%$ and $(100/45)^{1/8} - 1 = 10.50\%$ annualize the same loss over different horizons (Python: spreads `19.09%` and `7.50%`).
> A reads the optical inversion as a risk ranking; C invents a no-arbitrage condition on spreads that does not exist (V6 p.244).
>
> Q10: C.
> Short-term, static, granular, homogeneous receivables are evaluated with a statistics-based approach on the existing book.
> B fits a dynamic pool; A fits heterogeneous, non-granular pools (V6 p.245, p.246).

## Flashcards

#flashcards/cfa-l2/06-Fixed-Income/lm04

Default risk versus credit risk::Default risk is the probability of the default event; credit risk adds severity, the expected loss if default occurs, so collateral can make default risk high while credit risk is low (V6 p.200).
Expected exposure::The projected amount the investor could lose at each date if default occurs, before recovery; for a one-year 4% bond at par it is 104 (V6 p.200, p.201).
Loss given default formula::Exposure times one minus the recovery rate; loss severity is one minus the recovery rate (V6 p.201).
Recovery rate drivers::Industry, seniority in the capital structure, total leverage, and whether the issue is secured or collateralized (V6 p.201).
Why risk-neutral PODs exceed actual PODs::They embed the default timing risk premium, and observed spreads also include liquidity and tax effects that the model attributes to credit (V6 p.202, p.235).
In risk-neutral valuation, expected payoffs are discounted at the {{risk-free rate}}, not the bond's yield to maturity (V6 p.202).
Hazard rate::The annual probability of default conditional on no prior default; each date's POD is the hazard times the prior date's probability of survival (V6 p.203).
Probability of survival after t years at constant hazard h::One minus h, raised to the power t; cumulative POD is one minus that (V6 p.203).
Micro-problem: h is 1.25%; POD for Date 3?::1.25% times 0.9875 squared, which is 1.2189%; keystrokes 0.9875 x^2 = times 0.0125 = (V6 p.203).
CVA definition::The sum over dates of LGD times POD times the risk-free discount factor; the present value of expected default losses and the price of the bond's credit risk (V6 p.202, p.203).
Fair value of a risky bond::Value assuming no default minus the credit valuation adjustment (V6 p.203, p.221).
Two equivalent quotes of credit compensation::The CVA as a Date 0 present value per 100 par, or the credit spread as an annual rate over the benchmark for the bond's life (V6 p.203).
Credit spread approximation::Annual default probability times one minus the recovery rate; 1.25% times 0.60 gives about 0.75% versus the exact 0.77% (V6 p.203).
For a given price and spread, assumed POD and recovery rate are {{positively}} correlated (V6 p.205).
Micro-problem: exposure 98, recovery 35 per 100, POD 0.90%; expected loss?::LGD 63 times 0.009 equals 0.567 (V6 p.206).
Where credit scores and credit ratings are used::Scores in retail lending to individuals and small businesses; ratings in wholesale markets for corporates, sovereigns and ABS (V6 p.208).
FICO factor weights::Payment history 35%, debt burden 30%, length of credit history 15%, types of credit 10%, recent hard inquiries 10% (V6 p.208).
Does self-checking a FICO score hurt it?::No, self-checks are soft inquiries and are excluded; only hard inquiries from new credit applications count (V6 p.208, p.209).
Notching::Adjusting an issue rating off the senior unsecured issuer rating for priority of claim and subordination; it folds LGD into ratings, which is why they are credit ratings, not default ratings (V6 p.211).
Transition matrix expected return adjustment::Each migration's price change is minus modified duration times the spread change; probability-weight the changes and add the sum to the YTM (V6 p.212).
Why migration usually reduces expected return::Probabilities are skewed toward downgrades, and downgrade spread widenings are larger than upgrade tightenings (V6 p.212).
Micro-problem: MD 7.2, spread goes 1.10% to 1.50%; price change?::Minus 7.2 times 0.40% equals minus 2.88%; keystrokes 7.2 +/- times 0.004 = (V6 p.212).
Structural model default condition::Default occurs when the asset value falls below the default barrier set by the liabilities; POD is the probability mass below the barrier and rises with asset variance, time and leverage (V6 p.214, p.215).
Equity in the structural model::A long call on the company's assets with strike equal to the face value of debt; limited liability means it is never negative (V6 p.215).
Debt in the structural model, two readings::Assets minus the call written to shareholders, or a default-free bond worth K minus a put on the assets struck at K (V6 p.215, p.216).
The value of shareholders' limited liability equals the value of the {{put option}} they hold against the debtholders (V6 p.216).
Structural model strengths and weaknesses::Explains why default happens and links credit to option pricing, but needs unobservable inputs (asset value, volatility, default barrier) that hidden debt can corrupt (V6 p.213, p.214).
Reduced-form model estimation::Default intensity from regression on observable company variables (leverage, net income to assets, cash to assets) and macro variables (unemployment, GDP growth, equity volatility) (V6 p.214).
Reduced-form model weaknesses::No economic explanation of default, and default arrives as a surprise even though real defaults usually follow repeated downgrades (V6 p.214).
Who should use which credit model?::Structural for insiders (management, banks' internal risk, rating agencies); reduced-form for valuing risky debt and credit derivatives from market data (V6 p.216, p.217).
Which inputs does a reduced-form model need from the balance sheet?::None beyond published data; that is the point, it uses only observable market and accounting variables (V6 p.214, p.217).
VND::The bond's value assuming no default, from benchmark discount factors or backward induction on the calibrated benchmark tree; unchanged by credit parameters and by volatility for option-free bonds (V6 p.221, p.224).
Expected exposure on a binomial tree, fixed-coupon bond::Probability-weighted node values plus the coupon for the date; at maturity, par plus coupon (V6 p.221, p.222).
Floater expected exposure quirk::Bond values use date-t node probabilities but the in-arrears coupon uses date t-1 probabilities, because the rate was set one period earlier (V6 p.227).
Discount margin::The constant addition to every benchmark rate in the tree that reprices the floater to its value; the floater analog of the credit spread, above the quoted margin when price is below par (V6 p.228, p.229).
Micro-problem: floater pays one-year rate plus 0.50%; Date 0 rate is minus 0.25%; Date 1 coupon?::0.25 per 100, since minus 0.25% plus 0.50% is 0.25%; the payment is in arrears (V6 p.225, p.226).
Effect of higher interest rate volatility on a risky option-free bond::VND is unchanged; expected exposures and CVA fall slightly because the lognormal tree spreads rates asymmetrically above the forwards, so fair value rises marginally (V6 p.224, p.225).
Components of a corporate bond yield::Benchmark part carries expected inflation and expected real rate; the spread carries expected default loss plus liquidity and taxation (V6 p.232, p.233).
XVA family::Valuation adjustments to a benchmark (OIS-discounted) value: CVA for credit, FVA funding, LVA liquidity, TVA taxation; CVA is the most developed (V6 p.233).
POD versus recovery sensitivity of the spread::Doubling the POD widens the spread far more than halving the recovery; on the three-year 3% bond, 90 to 182 bps versus 90 to 121 bps (V6 p.236, p.237).
Which trade expresses disagreement with a high near-term implied POD that declines over time?::Sell short-term CDS protection and buy longer-term protection (V6 p.244).
Term structure of credit spreads, four drivers::Credit quality, financial conditions (countercyclical spreads), market supply and demand including liquidity of traded issues, and company-value model outputs such as equity volatility (V6 p.239, p.240).
Typical spread curve for the highest ratings::Flat or slightly upward sloping, because spreads sit near zero and migration can only widen them (V6 p.239).
Why an LBO or a cyclical trough can invert a high-yield spread curve::Investors expect deleveraging or industry recovery to improve credit over time, so near-term spreads exceed long-term spreads (V6 p.243).
Distressed bond pricing rule::Price converges to the recovery value regardless of maturity; CVA equals VND minus the recovery price and the inverted spread curve is an optical effect (V6 p.244).
Which benchmark is often substituted for government bonds in spread term structure work?::The interbank swap curve, because off-the-run government maturities are illiquid and interpolation distorts spreads (V6 p.241).
Bonds to include when building an issuer's credit curve::Senior unsecured general obligations only; exclude embedded options, liens and unique provisions, and remember cross-default clauses link all maturities (V6 p.241).
Granularity and homogeneity::Granularity is the number of obligations in the pool; homogeneity is how alike they are; together they select the credit analysis approach (V6 p.245, p.246).
Approach for short-term granular homogeneous pools (credit cards, trade receivables)::Statistics-based analysis of the existing book (V6 p.245, p.246).
Approach for medium-term granular homogeneous dynamic pools (auto ABS)::Portfolio-based approach, because the pool changes over time (V6 p.245, p.246, p.260).
Approach for non-granular heterogeneous pools (CMBS, CRE, leveraged loan CLOs, project finance)::Loan-by-loan analysis of each obligation (V6 p.245, p.246).
Three pillars of securitized debt credit analysis::The collateral pool (granularity, homogeneity, tenor), the originator and servicer (operational and counterparty risk, seasoned-deal track record), and the structure (true sale to the SPE, overcollateralization, tranching, triggers, excess spread) (V6 p.245 to p.247).
Excess spread::Return built into an ABS above the expected loss of the pool; the first cushion against asset quality deterioration (V6 p.247).
Covered bond::A senior debt obligation of a financial institution with dual recourse to the issuer and a dynamic, replenished cover pool of mortgages or public sector debt (V6 p.247, p.248).
Covered bond redemption regimes::Hard bullet (default and acceleration on missed schedule), soft bullet (default delayed to a new final maturity, usually up to a year), conditional pass-through (converts to pass-through after the original maturity) (V6 p.248).
Why covered bonds rate above the issuing bank::Dual recourse, mandatory cover pool maintenance, public supervision and BRRD protection push default probability down and recovery up, often worth several notches (V6 p.248).

## Common mistakes

1. Netting recovery out of the exposure and then applying the recovery rate again in the LGD column; exposure is before recovery, LGD is exposure times one minus recovery (V6 p.200, p.201).
2. Using the flat hazard rate as every year's POD instead of conditioning on survival; PODs must decline along the column when the hazard is constant (V6 p.203).
3. Discounting risk-neutral expected payoffs at the bond's YTM instead of the risk-free rate, which double-counts the credit risk (V6 p.202).
4. Summing undiscounted expected losses (3.5395) or the cumulative POD (5.8808%) and calling it the CVA (3.3367); only the discounted column is the CVA (V6 p.251, p.261).
5. Multiplying duration by the destination spread level instead of the spread change in migration problems, or dropping the minus sign (V6 p.212, p.262).
6. Labeling any model that uses stock market data as reduced-form; equity-implied asset volatility with a default barrier is structural (V6 p.214, p.256, p.264).
7. Forgetting the coupon in tree-based expected exposures, or using 0.5/0.5 weights at dates beyond Date 1 instead of binomial node probabilities (V6 p.221, p.222).
8. Using date-t probabilities for a floater's coupon when the in-arrears coupon was set at date t-1 rates (V6 p.227).
9. Recomputing VND when only credit parameters change; POD and recovery shocks move the CVA only (V6 p.236, p.270).
10. Expecting recovery changes to move the spread as much as POD changes; the POD scales the whole expected loss and dominates (V6 p.236, p.237).
11. Reading a distressed issuer's inverted spread curve as a view that long bonds are safer, when all its bonds simply trade at the recovery price (V6 p.244).
12. Recommending loan-by-loan analysis for granular homogeneous pools, or a static book approach for a dynamic pool (V6 p.246, p.274).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "06-04" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
