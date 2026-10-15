---
type: cfa-lm
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
volume: 9
lm: 3
title: "Exchange-Traded Funds: Mechanics and Applications"
pages: "155-201"
weight_band: "10-15%"
difficulty: 2
los_count: 8
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/portfolio-management]
---

# LM3: Exchange-Traded Funds: Mechanics and Applications

Difficulty 2 of 5: the module is almost entirely descriptive with only two calculation types (holding-period cost and leveraged-ETF daily resets), but the exam extracts precision from the tracking-error source list, the bid-ask spread sign conventions, and the cost and risk taxonomies, all of which are easy to half-know.

## LOS map

- **explain** the creation/redemption process of ETFs and the function of authorized participants (V9 p.155) ^los-09-03-a
    - Examiner asks: given an ETF trading at a premium or discount to iNAV, state which direction the AP trades (buy the basket and sell or create ETF shares at a premium; buy ETF shares and redeem them for the basket at a discount), and who ultimately bears the transaction costs.
- **describe** how ETFs are traded in secondary markets (V9 p.155) ^los-09-03-b
    - Examiner asks: distinguish the primary market (in-kind, OTC, APs and the issuer only) from the secondary market (exchange trading open to anyone), and recall T+2 settlement with up to six days for market makers.
- **describe** sources of tracking error for ETFs (V9 p.155) ^los-09-03-c
    - Examiner asks: rank three ETFs by expected tracking error given replication approach, ADRs versus local shares, and securities lending, or identify the smallest contributor (infrequent index changes) and the negative cost (lending income).
- **describe** factors affecting ETF bid–ask spreads (V9 p.155) ^los-09-03-d
    - Examiner asks: spot the sign error in a set of statements (order flow and market-maker competition are negatively related to spreads, liquidity-provider costs and risks positively), and name which spread components drop out for very liquid ETFs.
- **describe** sources of ETF premiums and discounts to NAV (V9 p.155) ^los-09-03-e
    - Examiner asks: rank ETFs by expected premium or discount given percentage of foreign holdings and trading frequency, or compute a premium from ETF price and NAV or iNAV.
- **describe** costs of owning an ETF (V9 p.155) ^los-09-03-f
    - Examiner asks: compute the total holding-period cost as the prorated management fee plus round-trip commissions plus one full bid-offer spread, and state how the cost mix shifts as the holding period lengthens.
- **describe** types of ETF risk (V9 p.155) ^los-09-03-g
    - Examiner asks: match a scenario to the right risk label (ETN counterparty, settlement, security lending, fund closure, expectation related) or compute a leveraged or inverse ETF's multi-day NAV and contrast it with the naive multiple.
- **identify** and describe portfolio uses of ETFs (V9 p.155) ^los-09-03-h
    - Examiner asks: classify a described application (cash equitization, rebalancing, completion, transition management, factor tilt) and pick the right selection criterion, trading cost for tactical uses versus management fee for buy-and-hold.

## Core intuition

Everything in this module hangs off one structural fact: an ETF lives in two markets at once (V9 p.156).
The secondary market is the exchange, where any investor buys or sells ETF shares from another investor exactly as they would a stock, and where the issuer is not involved at all and receives no cash flow (V9 p.157).
The primary market is an over-the-counter channel between the issuer and a small club of institutional broker/dealers called authorized participants, and it is the only place ETF shares are ever created or destroyed (V9 p.156, p.157).
The trade in that primary market is in kind: the AP delivers a pre-specified basket of securities (the creation basket, published every morning) and receives a block of ETF shares (a creation unit, usually 50,000 shares), or hands back ETF shares and receives the redemption basket (V9 p.157, p.158).
Because the swap is shares for shares of equal value, the prices at which either side happened to trade during the day are irrelevant to the exchange itself (V9 p.157).

> [!abstract] Idea 1: the AP arbitrage is the price anchor
> When the ETF price drifts above the value of its basket (a premium), APs buy the basket, swap it for new ETF shares, and sell those shares into the market; when the price drifts below (a discount), APs buy ETF shares and redeem them for the basket, selling the securities (V9 p.158, p.159).
> Each round of this trade pushes the ETF price back toward fair value, so arbitrage keeps the ETF trading inside a band whose width equals the cost of doing the arbitrage plus a risk premium for volatility and liquidity risk (V9 p.158).
> The band can be one tick wide for liquid US equity ETFs or more than 1% wide for high-yield bond ETFs whose baskets are hard to trade (V9 p.158).

The economics of who pays is the second load-bearing idea, and it is the exam's favorite contrast with mutual funds (V9 p.160).
The AP absorbs all costs of transacting the basket securities, pays a creation/redemption fee to the issuer, and passes those costs to transacting investors through the ETF's bid-ask spread (V9 p.159, p.160).
Non-transacting shareholders are therefore shielded from other investors' entry and exit, whereas in a mutual fund the manager trades securities to meet flows and every shareholder shares those costs (V9 p.160).
The curriculum calls this "tax fair" as well: secondary-market selling never forces the fund to sell holdings, and an in-kind redemption is not a taxable event, so one investor's exit does not distribute capital gains to everyone else (V9 p.169).
On top of fairness sits tax efficiency: because the manager chooses which tax lots to deliver into a redemption basket, it can push out the lowest-cost-basis shares, continuously raising the fund's average cost basis and minimizing unrealized gains that could ever be distributed (V9 p.160, p.169).
The issuer also controls the dials that keep the mechanism working: basket size (10,000 to 600,000 shares), custom or cash baskets for illiquid holdings, and creation fees from $50 (VTIP) to $28,000 (VSS) (V9 p.160).
Fixed-income, leveraged, inverse, and commodity ETFs often use cash creation/redemption because their underlying bonds or swap positions are impractical to move in kind, which buys AP participation at the price of trading costs and tax impact inside the fund (V9 p.160).

Delivery on the index promise is measured in two related but different ways (V9 p.163, p.164).
Tracking error is the standard deviation of daily return differences between fund and index, typically annualized over 12 months; it measures variability only and says nothing about direction or about whether errors were concentrated in a few days (V9 p.164).
Tracking difference is the return gap over a holding period, best examined as a series of rolling 12-month numbers, which reveals the cumulative effect of management and expenses and compares directly with the expense ratio (V9 p.164, p.165).
All else equal an index fund should lag its benchmark by its expense ratio, so when EEM's median rolling shortfall of 0.79% exceeds its 0.69% fee, the extra 0.10% is the footprint of everything else on the source list (V9 p.165).
That list is mechanical to memorize and heavily tested: fees and expenses, representative sampling/optimization, depositary receipts and other ETFs held in place of local shares, index changes, fund accounting practices, regulatory and tax differences, and asset manager operations such as securities lending, which is a negative cost that offsets expenses (V9 p.165, p.166, p.168, p.169).
Sampling deserves respect because it both shifts the median unpredictably across market regimes and widens the range of outcomes, as GMF's tracking range of 1.95% versus EEM's 0.57% shows (V9 p.166, p.167).

> [!abstract] Idea 2: spreads, premiums, and discounts are information about the underlying, not noise
> A market maker's quoted spread is a price for immediacy that is bounded above by creation/redemption fees and direct costs, plus the underlying securities' own spreads, plus hedging or carry risk compensation, plus a profit margin, minus a discount for the chance an offsetting order arrives quickly (V9 p.170, p.171).
> For very liquid ETFs, trades match in seconds and never touch creation/redemption, so the first three components barely matter and the ETF can trade tighter than its own underlying basket (V9 p.171).
> Premiums and discounts to NAV largely reflect stale or lagged NAVs, foreign underlying markets that closed hours earlier, bond marks from dealer quotes rather than trades, or an ETF that simply has not traded recently; a liquid ETF quoting away from a stale NAV is doing price discovery, not mispricing (V9 p.172, p.173).

Costs must be assembled into a total-cost-of-ownership view, because the visible expense ratio can be the smallest piece (V9 p.175).
Trading costs (commissions, half the bid-ask spread on the way in and half on the way out, premiums or discounts paid) are one-time and dominate short holding periods; management fees, portfolio turnover, and taxable distributions accrue with time and dominate long holding periods; securities lending income and discounts received are negative costs (V9 p.175, p.176).
The crossover arithmetic is simple and examinable: a 0.25% round trip with a 0.15% annual fee costs 0.29% over 3 months (trading is 87% of the total) but 0.70% over 3 years (fees are 64% of the total) (V9 p.176, p.177).
That is why tactical traders choose ETFs on liquidity and spread even at a higher fee, while buy-and-hold investors weight the management fee (V9 p.177).

The risk section is a matching exercise plus one calculation (V9 p.177).
ETNs are unsecured debt, so their counterparty risk is theoretically 100% on issuer default, monitorable through the issuer's CDS spread, with a one-year CDS above 5% a significant warning (V9 p.177, p.178).
Swap-based ETFs carry settlement risk on unrealized gains between settlement dates; securities lending is overcollateralized to 102% domestic and 105% international and has never cost an ETF shareholder money; fund closure risk stems from regulation, competition, and corporate actions, with soft closures (creation halts, strategy changes) able to break the arbitrage and leave an ETN at a 5%+ premium, as with MORL (V9 p.179, p.180).
Expectation-related risk is investors misunderstanding complex products, and leveraged and inverse funds are the canonical case: they reset exposure daily to deliver a multiple of the one-day return, so compounding makes multi-day returns diverge from the naive multiple, and long-horizon holders must rebalance periodically (V9 p.180, p.181, p.182).

Finally, uses: the module's application taxonomy has three buckets (V9 p.182, p.183).
Portfolio efficiency covers cash equitization to kill cash drag, rebalancing in a single trade, completion of exposure gaps, and transition management between external managers (V9 p.183, p.184).
Asset class exposure management covers strategic core positions and tactical tilts, where the highest-volume ETFs are preferred and trading cost beats fee as the selection criterion (V9 p.184, p.185).
Active and factor investing covers smart beta ETFs (rules-based factor exposure, typically longer-term buy-and-hold), risk management uses (low volatility, currency hedged, duration hedged), leveraged and inverse tactical tools, discretionary active ETFs (largest in fixed income), and dynamic multi-asset strategies (V9 p.186, p.187, p.188).

## Formulas and derivations

**End-of-day ETF premium or discount** (V9 p.172)
$$
\text{Premium or discount (\%)} = \frac{\text{ETF price} - \text{NAV per share}}{\text{NAV per share}}
$$
^f-09-03-1

- ETF price: exchange closing price; NAV per share: end-of-day net asset value from closing prices of the holdings.
- Positive means premium, negative means discount.
- It holds by definition: NAV is the fair-value yardstick, so any gap is quoted relative to it; the gap persists only inside the arbitrage band because APs trade it away beyond that (V9 p.158, p.172).

**Intraday ETF premium or discount** (V9 p.172)
$$
\text{Premium or discount (\%)} = \frac{\text{ETF price} - \text{iNAV per share}}{\text{iNAV per share}}
$$
^f-09-03-2

- iNAV: "indicated" NAV, an intraday fair-value estimate computed from the day's creation basket and disseminated by exchanges (V9 p.172).
- Same sign convention as the end-of-day version; use iNAV whenever the question says intraday.
- A stale iNAV (foreign underlying markets closed, bonds marked from dealer bids) makes an apparent premium or discount informational rather than a true mispricing (V9 p.172, p.173).

**Round-trip trading cost** (V9 p.176)
$$
\text{Round-trip trading cost (\%)} = (\text{One-way commission \%} \times 2) + \left(\tfrac{1}{2}\,\text{Bid-ask spread \%} \times 2\right)
$$
^f-09-03-3

- One-way commission: commission on a single purchase or sale; bid-ask spread: full quoted spread, of which each transaction pays half.
- Buying costs half the spread and selling costs the other half, so a full round trip pays commissions twice and the whole spread once.
- With a $10 commission on a $20,000 trade (0.05% each way) and a 0.15% spread: $(0.05\% \times 2) + (0.5 \times 0.15\% \times 2) = 0.10\% + 0.15\% = 0.25\%$ (V9 p.176).

**Total holding-period cost** (V9 p.176)
$$
\text{Holding-period cost (\%)} = \text{Round-trip trade cost (\%)} + \frac{\text{Months held}}{12} \times \text{Annual management fee (\%)}
$$
^f-09-03-4

- Trading costs are incurred once regardless of holding period; the management fee accrues pro rata with time (V9 p.175, p.176).
- Exam wording lists "round-trip commissions" and "bid-offer spread on purchase and sale" separately; add each once and prorate only the fee.
- As the holding period lengthens, the fee share of total cost rises and the trading share falls, which drives the tactical-versus-buy-and-hold selection logic (V9 p.177).

> [!tip] Calculator
> Nine-month hold, 0.32% fee, 0.20% round-trip commissions, 0.10% spread: `0.32 x 9 / 12 = 0.24`, then `+ 0.20 + 0.10 = 0.54`.
> Never multiply the commissions or the spread by the holding period.

**Tracking error** (V9 p.164)
$$
TE = \text{annualized } \sigma\!\left(R_{ETF,d} - R_{Index,d}\right)
$$
^f-09-03-5

- $R_{ETF,d}$: fund daily return measured at NAV; $R_{Index,d}$: index daily return; reported over a 12-month window.
- It is a dispersion statistic only: it reveals neither the direction of performance nor whether errors were concentrated, so pair it with a mean or median (V9 p.164).
- EEM's daily-difference standard deviation over the sample year was 0.012% (V9 p.164).

**Rolling tracking difference** (V9 p.164, p.165)
$$
TD_{12m} = R_{ETF,12m} - R_{Index,12m}
$$
^f-09-03-6

- Computed over rolling 12-month windows and summarized by median and range.
- It shows the cumulative effect of management and expenses and is directly comparable to the expense ratio; expect $TD \approx -\text{expense ratio}$ for a clean index fund, with the residual explained by the tracking-error source list (V9 p.165).

**Leveraged ETF daily NAV and exposure reset** (V9 p.180, p.181)
$$
NAV_t = NAV_{t-1}\left(1 + L \times r_t\right), \qquad \text{Required notional}_t = L \times NAV_t
$$
^f-09-03-7

- $L$: daily return multiple (3 for a 3x fund, $-2$ for an inverse 2x fund); $r_t$: one-day index return.
- The fund must reset notional swap exposure to $L \times NAV$ at each close; after a gain the exposure has grown less than $L$ times the new NAV requires, so exposure is added, and vice versa (V9 p.180, p.181).
- Compounding of daily resets means the holding-period return is $\prod_t (1 + L r_t) - 1$, not $L$ times the index's period return, so multi-day results diverge from the naive multiple (V9 p.181, p.182).

## Worked examples

**Example 1: AP arbitrage when the ETF trades at a premium** (V9 p.158, p.159)
The ETF trades at $25.10 while the fair value of its basket is $25.00.
Step 1: the AP buys the creation basket in the market at the $25.00 per-ETF-share fair value.
Step 2: the AP simultaneously sells ETF shares in the market at $25.10, locking in $25.10 - 25.00 = 0.10$ per share (Python: 0.10) before trading costs and creation fees.
Step 3: the AP delivers the basket to the issuer in exchange for a creation unit of new ETF shares, covering the shares it sold.
The selling pressure on the ETF and buying pressure on the basket close the gap, and APs repeat until no profitable gap remains (V9 p.159).
^ex-09-03-1

**Example 2: AP arbitrage when the ETF trades at a discount** (V9 p.159)
The ETF trades at $24.90 while basket fair value is $25.00.
Step 1: the AP buys ETF shares in the market at $24.90.
Step 2: the AP simultaneously sells the underlying securities at fair value, capturing $25.00 - 24.90 = 0.10$ per share (Python: 0.10).
Step 3: the AP presents the ETF shares to the issuer for redemption and receives the redemption basket, covering its security sales.
Note the direction trap: at a discount the AP buys the ETF and redeems; the reverse description (buying the basket and creating) belongs to the premium case (V9 p.159).
^ex-09-03-2

**Example 3: EEM daily tracking and rolling tracking difference** (V9 p.164, p.165)
EEM tracks the MSCI Emerging Markets Index, holding about 900 of 1,150 constituents.
Its standard deviation of daily return differences over the year was 0.012%, tiny in itself, which is why daily tracking error alone understates cost.
The 12-month rolling tracking difference had a median of $-0.79\%$ against an expense ratio of $0.69\%$, so the fund lagged by an extra $0.79\% - 0.69\% = 0.10\%$ (Python: 0.10) beyond fees.
The rolling shortfall ranged from $-0.38\%$ to $-0.95\%$, a range of $-0.38 - (-0.95) = 0.57\%$ (Python: 0.57), showing variability that a single annual number would hide.
Lesson: compare the median rolling tracking difference to the expense ratio, and attribute the residual to sampling, withholding taxes, and the other list items (V9 p.165).
^ex-09-03-3

**Example 4: GMF and the cost of representative sampling** (V9 p.166, p.167)
GMF held only 763 of the 2,342 securities in the S&P Asia Pacific Emerging BMI, with a median constituent market cap of $2.8 billion versus $0.695 billion for the index, so the sample omits many mid- and small caps.
Consequence 1: regime dependence; GMF underperforms when EM mid- and small caps beat large caps, and outperforms in the reverse regime, so the median tracking difference is unstable across regimes.
Consequence 2: dispersion; GMF's trailing-12-month tracking difference ran from $+1.14\%$ to $-0.81\%$, a range of $1.14 - (-0.81) = 1.95\%$ (Python: 1.95), versus EEM's 0.57%.
The ratio is $1.95/0.57 = 3.42$ (Python: 3.42), which the curriculum rounds up to "nearly 4 times" (V9 p.167).
Sampling can therefore enhance or detract from returns, but it always widens the distribution of tracking outcomes (V9 p.167).
^ex-09-03-4

**Example 5 (curriculum Example 1): comparison of US ETF trading costs** (V9 p.173, p.174, p.175)
Exhibit 9 compares SPY, IVV, VOO (all S&P 500), EUSA (MSCI USA Equal Weighted), and IWM (Russell 2000).
SPY trades a median $20.23 billion a day with a $0.01 average spread and 0.00% median premium/discount; IVV and VOO are smaller ($1.08 billion and $739.69 million median) but nearly as tight because the underlying is liquid and easy to hedge.
EUSA trades only $0.94 million median with an average spread of 0.12% and maximum premium 0.96%, because its benchmark has no futures or related index products for market-maker hedging and holds close to 600 stocks.
IWM holds far more and smaller stocks with wide underlying spreads, yet trades at a 0.01% spread and 0.01% median premium/discount because volume is high ($3.81 billion median) and Russell 2000 futures make hedging quick, proving that ETF liquidity is driven by ETF-level order flow and hedgeability, not just the holdings.
Exhibit 10's bond ETFs (TLT, JNK, HYG) all show tight spreads (0.01% to 0.03%) but persistent positive median premiums (TLT 0.03%, JNK 0.10%, HYG 0.20%) and larger maximum premiums and discounts than the equity ETFs, because underlying bonds trade in a dealer market without continuous pricing; the positive median premiums say buyers were in net demand and paid above fair value for high-yield access, and in stress the exchange-traded ETF price is the better reflection of true supply and demand (V9 p.174, p.175).
^ex-09-03-5

**Example 6: round-trip trading cost** (V9 p.176)
An investor pays a $10 commission on a $20,000 trade, i.e. 0.05% each way, and the ETF's bid-ask spread is 0.15%.
Round trip cost $= (0.05\% \times 2) + (\tfrac{1}{2} \times 0.15\% \times 2) = 0.10\% + 0.15\% = 0.25\%$ (Python: 0.25).
For a position held under a year, 0.25% can exceed the entire annual expense ratio of many ETFs (V9 p.176).
^ex-09-03-6

**Example 7: holding-period cost at 3 months, 12 months, and 3 years** (V9 p.176, p.177)
ETF terms: 0.15% annual fee, 0.05% one-way commissions, 0.15% spread, so the round trip costs 0.25% from Example 6.
3-month cost $= 0.25\% + \tfrac{3}{12} \times 0.15\% = 0.2875\% \approx 0.29\%$ (Python: 0.2875).
12-month cost $= 0.25\% + \tfrac{12}{12} \times 0.15\% = 0.40\%$ (Python: 0.40).
3-year cost $= 0.25\% + \tfrac{36}{12} \times 0.15\% = 0.70\%$ (Python: 0.70).
Cost mix (Python): trading is $0.25/0.2875 = 87.0\%$ of the 3-month total, $62.5\%$ of the 12-month total, and $35.7\%$ of the 3-year total; the fee share is $13.0\%$, $37.5\%$, and $64.3\%$.
Exhibit 12 prints these shares as 0.86/0.14, 0.625/0.375, and 0.36/0.64; my recomputation gives 0.8696/0.1304 and 0.3571/0.6429, so the curriculum's 0.86 and 0.36 are truncations of the same figures, not different answers.
The conclusion is the tested part: trading costs dominate short holds, management fees dominate long holds (V9 p.177).
^ex-09-03-7

**Example 8: levered 3x ETF exposure reset** (V9 p.180, p.181)
A 3x FTSE 100 fund has NAV 100 (in GBP) and notional swap exposure of $3 \times 100 = 300$.
The index rises 5% in a day.
Exposure grows to $300 \times 1.05 = 315$; NAV grows to $100 \times (1 + 3 \times 5\%) = 115$ (Python: 315, 115).
To deliver 3x the next day, the fund needs $3 \times 115 = 345$ of exposure, so it must add $345 - 315 = 30$ of notional swap exposure (Python: 345, 30).
Resets follow gains with added exposure and losses with reduced exposure, which is exactly what makes multi-day compounding path dependent (V9 p.181).
^ex-09-03-8

**Example 9: levered inverse -2x ETF over three days** (V9 p.181, p.182)
A -2x S&P 500 fund starts at NAV 100 with the index at 100.
Day 2: the index rises to 110, a one-day return of 10%; the ETF returns $-2 \times 10\% = -20\%$ and NAV falls to $100 \times (1 - 0.20) = 80$ (Python: -20%, 80).
Day 3: the index falls to 99, a one-day return of $(99-110)/110 = -10\%$; the ETF returns $-2 \times (-10\%) = +20\%$ and NAV rises to $80 \times 1.20 = 96$ (Python: +20%, 96).
Over the period the index returned $(99-100)/100 = -1\%$, so a naive holder expects $-2 \times (-1\%) = +2\%$; the fund actually returned $(96-100)/100 = -4\%$ (Python: -1%, +2%, -4%).
The fund delivered its promise every single day; compounding of daily resets is what breaks the naive multi-day multiple, which is why these funds are not buy-and-hold products beyond about a month without periodic rebalancing (V9 p.182).
^ex-09-03-9

## Item-set patterns

> [!warning] Trap: which way does the AP trade at a premium or discount
> The vignette states an ETF trades at a premium (or discount) to iNAV exceeding arbitrage costs and asks for the most likely transaction.
> Correct approach: premium means buy the basket, deliver it for new ETF shares, sell ETF shares; discount means buy ETF shares, redeem for the basket, sell the securities.
> Distractors flip the direction (redemption baskets received at a premium), credit the wrong actor (the sponsor "creates shares" on its own initiative, or retail investors exchange baskets), or describe the premium mechanics under a discount label; each is tempting because both legs always involve baskets and ETF shares, and only the direction and actor change (V9 p.159, p.198).

> [!warning] Trap: prorating the wrong cost in the holding-period calculation
> The vignette lists an annual fee, round-trip commissions, and a bid-offer spread "on purchase and sale," with a holding period other than 12 months.
> Correct approach: cost = (months/12) x fee + commissions + spread, prorating only the fee and adding the quoted spread once.
> Distractor 1 charges the full-year fee (0.62% instead of 0.54% in Q10); distractor 2 double-counts the spread by adding it for purchase and again for sale (0.64%); both look plausible because the stem's phrase "on purchase and sale" invites doubling and the fee is quoted annually (V9 p.176, p.193).

> [!warning] Trap: tracking error versus tracking difference
> The vignette asks what reported tracking error measures or how best to assess cumulative performance.
> Correct approach: tracking error is the annualized standard deviation of daily return differences (magnitude of deviation only); a rolling 12-month tracking difference shows cumulative under- or outperformance and compares with the expense ratio.
> Distractors offer "difference in annual return" as tracking error, claim tracking error reveals direction or the distribution of errors, or offer the expense ratio as the best performance measure; each borrows a true property of the other statistic (V9 p.164, p.165, p.195).

> [!warning] Trap: ranking tracking error from portfolio characteristics
> The vignette gives a table of replication approach, ADRs versus local shares, and securities lending, and asks which ETF tracks best.
> Correct approach: full replication beats sampling; local shares beat ADRs (trading-hour mismatches create discrepancies); securities lending income offsets fees and lowers tracking error while income is smaller than expenses.
> The tempting error is treating lending as a pure risk that raises tracking error, or ignoring the ADR effect because "economic exposure is equivalent"; both statements are half-true and the question hinges on the half that matters (V9 p.166, p.168, p.169, p.198).

> [!warning] Trap: the sign of each bid-ask spread driver
> The vignette has an analyst assert relationships between spreads and order flow, liquidity-provider costs, and market-maker competition.
> Correct approach: more order flow means lower spreads (negative), more costs and risks mean higher spreads (positive), more competition means lower spreads (negative); the only subtracted component in the spread build-up is the likelihood of a quick offsetting order.
> Distractors state competition as positively related (the classic error) or claim creation/redemption fees drive spreads of very liquid ETFs, whose trades match without ever touching creation/redemption (V9 p.170, p.171, p.198).

> [!warning] Trap: premiums and discounts as staleness, not mispricing
> The vignette compares ETFs by percentage of foreign holdings and trading frequency, or shows a bond ETF at a discount in a stressed market.
> Correct approach: the largest premiums and discounts belong to ETFs with stale reference prices, i.e. high foreign holdings (underlying markets closed during ETF trading) and low trading frequency (last trade far from the NAV timestamp); in stress, the liquid ETF price is the price-discovery vehicle and the NAV is the stale number.
> Distractors pick the ETF with high trading frequency, or treat a stressed-market discount as an arbitrage failure rather than stale NAV inputs (V9 p.172, p.173, p.198, p.199).

> [!warning] Trap: leveraged and inverse funds over multiple days
> The vignette gives an index path over two or three days and asks for the leveraged or inverse ETF's return or NAV.
> Correct approach: apply $L$ to each day's return separately and compound: $NAV_T = NAV_0 \prod (1 + L r_t)$; never apply $L$ to the period return.
> The naive-multiple answer is always among the options (the +2% in the -2x example whose true answer is -4%), and a second distractor typically applies $L$ to the sum of daily returns without compounding (V9 p.181, p.182).

> [!warning] Trap: matching risk labels to scenarios
> The vignette describes a scenario and asks which risk it illustrates.
> Correct approach: ETN issuer default exposure is counterparty risk (monitor CDS spreads, worry above 5% one-year); mark-to-market exposure on OTC swaps between settlements is settlement risk; regulation, competition, and corporate actions drive fund-closure risk; creation halts and strategy changes are soft closures; an investor who does not understand an inverse or leveraged product bears expectation-related risk.
> Distractors cross-assign the labels, and "counterparty risk" tempts on any derivative-sounding scenario even when the described problem is comprehension, not credit (V9 p.177, p.179, p.180, p.200).

> [!warning] Trap: factor ETFs and tactical-use criteria
> The vignette asks how smart beta ETFs are used or which ETF suits a tactical trade.
> Correct approach: factor ETFs are rules-based, longer-term buy-and-hold tools for outperformance or risk modification, not tactical trading instruments; tactical trades favor the highest-volume ETFs in the asset class, selected on trading cost and liquidity rather than management fee.
> Distractors claim factor ETFs are primarily tactical, or pick the lowest-fee ETF for a short-horizon trade where spread and liquidity dominate (V9 p.177, p.186, p.201).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM03-Exchange-Traded-Funds-Mechanics-and-Applications-Practice-Problems]]

## Cross-links

- [[LM04-Using-Multifactor-Models]]: factor and smart beta ETFs are the cheapest implementation vehicle for the factor exposures LM04 models; the factor definitions (value, momentum, quality, size) and the return-attribution machinery there explain what a smart beta ETF actually delivers and how to judge one against its factor benchmark.
- [[LM05-Measuring-and-Managing-Market-Risk]]: the risk measures in LM05 drive the ETF applications here; beta, duration, and currency exposures measured there are adjusted in practice with index, duration-hedged, currency-hedged, and inverse ETFs, and cash equitization and rebalancing are the standing risk-control uses.
- [[LM04-Market-Based-Valuation-Price-and-Enterprise-Value-Multiples]] (05-Equity-Valuation): the screening rules inside value, dividend, and quality factor ETFs are built from the price and enterprise value multiples defined in that module, so understanding those multiples tells you what a value-factor ETF holds and why its tracking behavior differs from a cap-weighted fund.

## Self-test

Vignette: Mira Chen is an adviser at Meridian Wealth who implements client portfolios with ETFs.
Chen observes that ETF A, which holds US large-cap equities, trades at $41.16 while its iNAV is $42.00, and she estimates arbitrage costs at well under the gap.
She is comparing three international equity ETFs: ETF X (full replication, local shares, securities lending), ETF Y (representative sampling, ADRs, securities lending), and ETF Z (full replication, ADRs, no securities lending).
For a six-month tactical position she considers ETF B, which charges a 0.24% annual management fee, 0.12% round-trip commissions, and a 0.08% bid-offer spread on purchase and sale.
A client separately holds a 2x leveraged ETF bought at a NAV of $100 just before the index returned +4% on day 1 and -5% on day 2.
Chen also reviews an ETN whose issuing bank's one-year CDS trades at 6%, and she is parking a terminated bond manager's proceeds until a replacement manager is funded.

**Q1.** Given ETF A's pricing, the most likely AP transaction is to:
A. buy the creation basket and exchange it for new ETF shares.
B. buy ETF A shares and exchange them for the redemption basket.
C. sell ETF A shares short and wait for the sponsor to reduce shares outstanding.

**Q2.** The premium or discount on ETF A is closest to:
A. -2.00%.
B. -2.04%.
C. +2.04%.

**Q3.** Which international ETF should have the lowest tracking error?
A. ETF X
B. ETF Y
C. ETF Z

**Q4.** The expected total holding-period cost for the six-month position in ETF B is closest to:
A. 0.32%.
B. 0.40%.
C. 0.44%.

**Q5.** The client's 2x leveraged ETF NAV after day 2 is closest to:
A. $97.20.
B. $97.60.
C. $98.00.

**Q6.** Relative to a naive expectation of 2 times the index's two-day return, the leveraged ETF's two-day return is:
A. lower, because daily resetting compounds losses in volatile markets.
B. identical, because the fund delivered 2x on each day.
C. higher, because added exposure after day 1 cushioned the day 2 decline.

**Q7.** The 6% one-year CDS on the ETN issuer most directly signals elevated:
A. counterparty risk.
B. settlement risk.
C. fund-closure risk.

**Q8.** Parking the terminated manager's proceeds in an ETF benchmarked to the mandate's index until the new manager is funded is best described as:
A. cash equitization.
B. completion.
C. transition management.

**Q9.** Chen tells a colleague that a reported 12-month tracking error of 0.15% for ETF X proves the fund lagged its index by only 0.15% for the year.
Her statement is:
A. correct.
B. incorrect, because tracking error measures dispersion, not the cumulative return gap.
C. incorrect, because tracking error must be compared with the fund's beta first.

**Q10.** A client sells a large block of ETF X on the exchange at a gain; the most accurate tax statement is that the sale:
A. forces the fund to sell holdings, distributing gains to remaining shareholders.
B. triggers a taxable event for the selling client but not for the fund or its remaining shareholders.
C. is tax free because ETF redemptions occur in kind.

> [!success]- Answer key
> Q1: B.
> ETF A trades at a discount ($41.16 < 42.00$), so APs buy the cheap ETF shares, redeem them with the sponsor for the redemption basket, and sell the securities at fair value (V9 p.159).
> A describes the premium trade; C is not a mechanism at all, since only AP redemption reduces shares outstanding.
> Q2: A.
> $(41.16 - 42.00)/42.00 = -0.84/42.00 = -2.00\%$ (Python: -2.00%).
> B divides by the ETF price instead of iNAV ($-0.84/41.16 = -2.04\%$), and C drops the sign; the denominator is always (i)NAV (V9 p.172).
> Q3: A.
> ETF X has full replication, local shares, and lending income offsetting expenses, all three tracking-error reducers (V9 p.166, p.168, p.169).
> B samples and holds ADRs (two error sources); C holds ADRs and forgoes the lending offset.
> Q4: A.
> $(6/12) \times 0.24\% + 0.12\% + 0.08\% = 0.12\% + 0.20\% = 0.32\%$ (Python: 0.32).
> B (0.40%) double-counts the spread for purchase and sale; C (0.44%) charges the full-year fee without prorating (V9 p.176).
> Q5: A.
> Day 1: $100 \times (1 + 2 \times 4\%) = 108$; day 2: $108 \times (1 + 2 \times (-5\%)) = 108 \times 0.90 = 97.20$ (Python: 108, 97.20).
> B ($97.60$) applies 2x to the index's period return of $1.04 \times 0.95 - 1 = -1.2\%$ (naive multiple); C ($98.00$) applies 2x to the sum of daily returns ($-1\%$) without compounding (V9 p.181, p.182).
> Q6: A.
> Naive expectation: $2 \times (-1.2\%) = -2.4\%$; actual: $97.20/100 - 1 = -2.8\%$ (Python: -2.4%, -2.8%).
> The day 1 reset added exposure at the higher NAV, so the day 2 decline hit a larger notional; daily resetting compounds against the holder when the index reverses (V9 p.181, p.182).
> B ignores compounding across days; C has the direction of the reset effect backwards for a gain-then-loss path.
> Q7: A.
> An ETN is unsecured issuer debt, and a one-year CDS above 5% signals significant default risk, i.e. counterparty risk (V9 p.177, p.178).
> B concerns unrealized swap gains between settlement dates; C concerns the fund shutting down for business reasons, not issuer default.
> Q8: C.
> Holding a benchmark ETF while managers are hired, fired, or funded is transition management; the ETF may even be handed to the new manager as funding (V9 p.184).
> A is investing excess cash to avoid cash drag; B fills a lasting exposure gap left by existing managers, not an interim manager change.
> Q9: B.
> Tracking error is the annualized standard deviation of daily return differences; it has no sign and says nothing about the cumulative gap, which is the rolling tracking difference's job (V9 p.164, p.165).
> A confuses dispersion with performance; C invents a beta precondition that plays no role in the definition.
> Q10: B.
> A secondary-market sale transfers shares between investors; the fund does not trade, so the seller realizes a personal taxable gain while remaining shareholders are unaffected, the "tax fair" property (V9 p.169).
> A describes the traditional mutual fund mechanics; C confuses the client's own exchange sale (taxable to the client) with an AP's in-kind redemption (not a taxable event for the fund).

## Flashcards

#flashcards/cfa-l2/09-Portfolio-Management/lm03

Primary market for ETFs::OTC creation/redemption between authorized participants and the ETF issuer, the only way ETF shares are created or destroyed (V9 p.156).
Secondary market for ETFs::Exchange trading of ETF shares between any market participants, the only access for ordinary investors (V9 p.156).
Authorized participant::A large broker/dealer, often a market maker, authorized by the issuer to create and redeem ETF shares in kind (V9 p.157).
Creation basket::The list of securities the ETF wants to own, published each business day, which also drives the iNAV calculation (V9 p.157).
Creation unit::The large block of ETF shares (usually but not always 50,000) exchanged with the AP in a creation or redemption (V9 p.157).
Redemption basket::The securities the AP receives when redeeming ETF shares; it can differ from the creation basket for tax, compliance, or investment reasons (V9 p.158).
Why is basket pricing irrelevant in a creation?::The swap is in kind and of equal value, so only the securities and share quantities matter, not the day's prices (V9 p.157).
AP trade when the ETF is at a premium::Buy the creation basket, exchange it for new ETF shares, sell the ETF shares at the higher price (V9 p.158, p.159).
AP trade when the ETF is at a discount::Buy ETF shares, redeem them for the redemption basket, sell the securities at the higher fair value (V9 p.159).
What sets the width of the arbitrage band?::The cost of the arbitrage plus a risk premium for volatility and liquidity risk of the ETF and its basket (V9 p.158).
Arbitrage gap for hard-to-trade underlyings::Can exceed 1% (high-yield bonds) versus one tick for liquid US equity ETFs (V9 p.158).
Who bears AP transaction costs?::Transacting ETF investors, through the bid-ask spread; non-transacting shareholders are shielded (V9 p.159, p.160).
Why are ETFs called tax fair?::Secondary-market selling never forces portfolio sales, and in-kind AP redemptions are not taxable events, so one investor's exit creates no gains for others (V9 p.169).
ETF tax-efficiency lever::Managers deliver the lowest-cost-basis tax lots into redemption baskets, raising average cost basis and minimizing unrealized gains (V9 p.160, p.169).
Which ETFs often use cash instead of in-kind creation?::Fixed-income ETFs with illiquid bonds, plus many leveraged, inverse, and commodity ETFs managing swap positions (V9 p.160).
Creation basket size range::From 10,000 to 600,000 ETF shares, chosen by the issuer (V9 p.160).
US ETF settlement cycle::T+2 through NSCC continuous net settlement, with market makers allowed up to six days (V9 p.161).
Role of the DTC::Holds the book of accounts of security ownership at the member-firm level and nets cleared trades for settlement (V9 p.161).
European ETF market structure::Mostly institutional, fragmented across exchanges and 29 CSDs, heavy negotiated OTC trading and multiple listings, producing wider spreads (V9 p.161, p.162).
Tracking error definition::Annualized standard deviation of daily return differences between the fund and its index, usually over 12 months (V9 p.164).
Tracking difference definition::The fund-minus-index return gap over a holding period, best studied as rolling 12-month values with median and range (V9 p.164, p.165).
What does tracking error fail to reveal?::Direction of performance and the distribution or concentration of the daily errors (V9 p.164).
Expected annual shortfall of a clean index fund::Approximately its expense ratio; residual gaps come from the other tracking-error sources (V9 p.165).
Seven sources of ETF tracking error::Fees and expenses, representative sampling, depositary receipts and other ETFs, index changes, fund accounting practices, regulatory and tax requirements, asset manager operations (V9 p.165, p.166).
Effect of representative sampling on tracking::Makes the median tracking difference regime dependent and dramatically widens the range of outcomes (V9 p.166, p.167).
Why do ADRs cause tracking error?::Same economic exposure but different trading hours and prices than local shares, creating portfolio-versus-index discrepancies (V9 p.167, p.168).
Smallest typical tracking-error source::Index changes, because they are infrequent and managers can trade them at market-on-close prices with AP help (V9 p.168).
Securities lending as a negative cost::Lending fees and collateral interest offset fund expenses, lowering tracking error until income exceeds expenses (V9 p.166, p.169).
Which spread factors are negatively related to ETF spreads?::Ongoing order flow and market-maker competition; liquidity-provider costs and risks are positively related (V9 p.170, p.198).
Five components bounding an ETF bid-ask spread::Creation/redemption and direct fees, underlying securities' spreads, hedging or carry risk compensation, market-maker profit spread, minus the offsetting-order likelihood discount (V9 p.170).
Which spread components fade for very liquid ETFs?::Creation/redemption fees, underlying spreads, and hedging-risk compensation, because trades match quickly without creation/redemption (V9 p.171).
Why are fixed-income ETF spreads wider than equity?::Underlying bonds trade in an opaque dealer market, are hard to hedge, and often trade actively only near issuance (V9 p.171, p.172).
End-of-day premium or discount formula::(ETF price minus NAV per share) divided by NAV per share (V9 p.172).
iNAV::Intraday indicated NAV, the fair-value estimate of an ETF share based on that day's creation basket (V9 p.172).
Two drivers of premiums and discounts::Timing differences (foreign closes, bond quote conventions) and stale pricing of infrequently traded ETFs (V9 p.172, p.173).
When is an ETF a price-discovery vehicle?::When its underlying markets are closed or bond marks are stale, so the live ETF price is the best current value estimate (V9 p.173).
Round-trip trading cost formula::One-way commission times two, plus half the bid-ask spread times two (V9 p.176).
Holding-period cost formula::Round-trip trade cost plus the management fee prorated by months over twelve (V9 p.176).
Micro-problem: 9-month hold, 0.32% fee, 0.20% round-trip commissions, 0.10% spread::(9/12) x 0.32 + 0.20 + 0.10 = 0.54%; keystrokes 0.32 x 9 / 12 = + 0.20 + 0.10 = (V9 p.193, p.199).
Micro-problem: 9-month hold, 0.40% fee, 0.55% commissions, 0.20% spread::(9/12) x 0.40 + 0.55 + 0.20 = 1.05%; the 1.15% distractor skips prorating the fee (V9 p.200).
How does cost mix shift with holding period?::Trading costs dominate short holds (87% of a 3-month total in the text example) and management fees dominate long holds (64% at 3 years) (V9 p.177).
Selection criterion for tactical ETF trades::Liquidity and trading costs, not management fees; highest-volume ETFs in the category are preferred (V9 p.177, p.185).
Costs that are negative for ETF holders::Securities lending income, discounts received at purchase, and taxable losses harvested (V9 p.175).
ETN counterparty risk::ETNs are unsecured, unsubordinated issuer debt, so counterparty risk is theoretically 100% on instantaneous issuer default (V9 p.177, p.178).
How to monitor ETN default risk::The issuing bank's CDS spread; a one-year CDS above 5% signals significant default risk (V9 p.178).
Settlement risk in ETFs::Mark-to-market gains on OTC swaps are exposed to counterparty default between (usually daily or weekly) settlements (V9 p.179).
Securities lending collateral standard::Overcollateralized at 102% domestic and 105% international, with cash collateral in very short-term instruments (V9 p.179).
Three drivers of fund-closure risk::Regulation, competition, and corporate actions such as issuer mergers (V9 p.179, p.180).
Soft closure::A creation halt or investment-strategy change without an actual fund closing; halted creations can leave an ETN at a large premium, as with MORL at over 5% (V9 p.180).
Expectation-related risk::Investors not understanding how complex ETFs such as leveraged and inverse funds perform (V9 p.180).
Leveraged ETF daily reset::Exposure must return to L times NAV each close; the fund adds notional after index gains and cuts it after losses (V9 p.180, p.181).
Micro-problem: 3x fund, NAV 100, index +5%::NAV becomes 115, exposure grows 300 to 315, required exposure 345, so add 30 notional (V9 p.181).
Micro-problem: -2x fund, index 100 to 110 to 99::NAV 100 to 80 to 96; period return -4% versus the naive +2% expectation (V9 p.181, p.182).
Holding-period guidance for leveraged ETFs::Not buy-and-hold beyond roughly a month; long-horizon holders must rebalance periodically to maintain target exposure (V9 p.182).
Three buckets of ETF portfolio applications::Portfolio efficiency, asset class exposure management, and active and factor investing (V9 p.182, p.183).
Cash equitization::Investing excess cash in liquid benchmark ETFs to stay fully invested and minimize cash drag (V9 p.183).
Cash drag::Fund mis-tracking relative to its index caused by holding uninvested cash (V9 p.183).
Completion strategy::Using ETFs to fill a temporary gap in exposure to an asset class, sector, theme, or factor left by other managers (V9 p.183).
Transition management with ETFs::Holding a benchmark ETF to keep market exposure while managers are replaced, sometimes funding the new manager with ETF positions (V9 p.184).
Three drawbacks of ETFs for very large asset owners::Negotiable cheaper SMAs or commingled trusts, SMA customization, and public disclosure requirements on large ETF holdings (V9 p.184).
Factor (smart beta) ETF::Rules-based index ETF screening or weighting on return drivers such as value, dividend yield, growth, quality, volatility, momentum; typically longer-term buy-and-hold (V9 p.186).
Multi-factor versus single-factor ETFs::Multi-factor spreads risk and lowers return volatility but caps the upside from timing any single factor (V9 p.187).
Where are the largest active ETFs?::Fixed income, where passive management is less dominant; active ETFs are still only 2%-3% of global ETF assets (V9 p.186, p.187).
Thematic ETFs::Passive holdings expressing an active niche view (cybersecurity, robotics); evaluate them like stocks given comparable volatility (V9 p.185).
Smart beta share of ETF assets::Roughly 20% of global ETF assets, versus 2%-3% for discretionary active ETFs (V9 p.186).

## Common mistakes

1. Reversing the AP arbitrage direction: at a premium the AP buys the basket and sells or creates ETF shares; at a discount the AP buys ETF shares and redeems; the practice set tests this in both directions (V9 p.159, p.197, p.198).
2. Letting anyone other than an AP transact with the sponsor: retail investors never exchange baskets for creation units, and the sponsor never initiates share creation on its own (V9 p.157, p.197).
3. Charging the full annual management fee for a partial-year holding period, or double-counting the bid-offer spread for purchase and sale; prorate only the fee and add the quoted spread once (V9 p.176, p.199, p.200).
4. Calling the daily-disclosed security list a creation unit; the list is the creation basket, the unit is the ETF share block (V9 p.157, p.197).
5. Treating tracking error as a performance measure: it is an annualized dispersion statistic that reveals neither direction nor error concentration; the rolling tracking difference measures cumulative performance (V9 p.164, p.165, p.199).
6. Assuming securities lending raises tracking error: lending income is a negative cost that reduces tracking error while income stays below fund expenses (V9 p.166, p.169, p.198).
7. Marking market-maker competition as positively related to spreads; competition and order flow narrow spreads, only liquidity-provider costs and risks widen them (V9 p.170, p.198).
8. Expecting the ETF with high trading frequency or low foreign holdings to show the biggest premiums and discounts; staleness (low frequency, high foreign share) drives the biggest gaps (V9 p.172, p.173, p.198).
9. Applying the leverage multiple to a multi-day index return instead of compounding daily: the -2x fund on a -1% index path returned -4%, not +2% (V9 p.181, p.182).
10. Labeling every derivative-flavored scenario counterparty risk: comprehension failures are expectation-related risk, swap mark-to-market exposure is settlement risk, and regulation, competition, and corporate actions are fund-closure risk (V9 p.179, p.180, p.200).
11. Believing mutual funds may simply retain realized capital gains or that ETF secondary-market selling pushes tax liabilities onto remaining ETF holders; both reverse the tax-fairness comparison (V9 p.169, p.199).
12. Using factor (smart beta) ETFs as tactical trading tools or picking tactical ETFs by expense ratio; factor ETFs are buy-and-hold vehicles and tactical trades are chosen on volume, liquidity, and trading cost (V9 p.177, p.186, p.200, p.201).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "09-03" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
