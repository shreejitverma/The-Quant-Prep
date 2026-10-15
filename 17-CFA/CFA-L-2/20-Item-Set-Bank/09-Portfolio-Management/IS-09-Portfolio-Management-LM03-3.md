---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 3
title: "Corbel Securities: A Supervisory Review of Leveraged Products"
los: [los-09-03-b, los-09-03-g, los-09-03-h]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Corbel Securities: A Supervisory Review of Leveraged Products

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Hannah Weiss, CFA, is a compliance officer at Corbel Securities, a retail broker-dealer.
After a cluster of client complaints, she is reviewing accounts serviced by registered representative Luis Cardenas that hold leveraged and inverse exchange-traded products.
The two funds involved are TRPL, which seeks 3 times the daily return of a broad equity index, and DWNX, which seeks -2 times the daily return of the same index.
Both funds obtain exposure through total return swaps and reset exposure at each close.

Exhibit 1: Index closing levels over the review window

| Date | Index close |
|---|---|
| Day 0 (Monday) | 1,500.00 |
| Day 1 (Tuesday) | 1,560.00 |
| Day 2 (Wednesday) | 1,482.00 |
| Day 3 (Thursday) | 1,526.46 |

TRPL's NAV was USD 50.00 per share at the Day 0 close.
TRPL had net assets of USD 200 million at the Day 0 close, with swap notional exposure set at 3 times net assets.
Its expense ratio is 0.95%, which Weiss ignores over the three days.

Client 1 bought DWNX at the Day 0 close to hedge an equity portfolio for the three days.
He complained on Friday, writing: "The index rose less than 2% over three days, so I expected DWNX to lose about twice that much.
It lost far more.
The fund must have failed to deliver its stated objective."

Client 2 wanted to leave TRPL after the Day 3 close.
She holds 60,000 TRPL shares and asked Cardenas whether she could avoid the exchange spread by redeeming her shares directly with the fund sponsor at NAV, as she does with her mutual funds.

Client 3 holds an exchange-traded note, ETN-1, which also delivers leveraged index exposure.
ETN-1 is a senior unsecured obligation of its issuing bank.
The bank's one-year credit default swap spread widened from 1.4% to 5.8% during the review window.
A second note from a different issuer, ETN-2, stopped issuing new notes last month and now trades at a 6.4% premium to its indicative value; no Corbel clients hold it.

Cardenas explains his general approach to the products in a memo to Weiss with three proposed uses.

Use 1: "For a client who expects a sharp market move around a central bank announcement, I buy TRPL or DWNX for one or two days and close the position afterward."

Use 2: "For retired clients seeking higher long-run returns, I place 15% of the equity allocation in TRPL as a permanent core holding with no rebalancing."

Use 3: "For clients with idle cash in their accounts, I buy TRPL so the cash earns index-like returns until it is invested."

Weiss must decide which complaints have merit, what she should tell Client 2, and which of Cardenas's uses to approve.

## Questions

1. TRPL's NAV per share at the Day 3 close is closest to: (LOS: los-09-03-g)
   - A. USD 51.88.
   - B. USD 52.65.
   - C. USD 53.00.
2. To restore 3 times leverage after the Day 1 close, TRPL must change its swap notional exposure by closest to: (LOS: los-09-03-g)
   - A. +USD 24 million.
   - B. +USD 48 million.
   - C. +USD 72 million.
3. DWNX's return over the three days, and the risk that best describes Client 1's complaint, are: (LOS: los-09-03-g)
   - A. -3.53%, and expectation-related risk.
   - B. -4.87%, and expectation-related risk.
   - C. -4.87%, and counterparty risk.
4. The development affecting Client 3's ETN-1 most directly signals elevated: (LOS: los-09-03-g)
   - A. counterparty risk, with a potential loss of up to the full value of the note if the issuer defaults.
   - B. settlement risk, with a potential loss limited to unrealized gains since the last reset.
   - C. fund-closure risk, of the kind that has left ETN-2 trading at a premium.
5. Weiss's most accurate response to Client 2 is that she: (LOS: los-09-03-b)
   - A. can redeem directly with the sponsor at NAV because her position exceeds the usual creation unit size.
   - B. can redeem through Corbel at the day's NAV, as she does with her mutual funds, because TRPL is an open-end fund.
   - C. must sell her shares on the exchange, because only authorized participants transact with the sponsor.
6. Which of Cardenas's proposed uses is most consistent with the appropriate use of leveraged and inverse ETFs? (LOS: los-09-03-h)
   - A. Use 1
   - B. Use 2
   - C. Use 3

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Daily index returns: Day 1 $1560/1500 - 1 = +4.00\%$, Day 2 $1482/1560 - 1 = -5.00\%$, Day 3 $1526.46/1482 - 1 = +3.00\%$.
> Daily resets: $50.00 \times (1 + 3 \times 0.04) \times (1 + 3 \times (-0.05)) \times (1 + 3 \times 0.03) = 50.00 \times 1.12 \times 0.85 \times 1.09 = 51.8840$.
> B is wrong because it applies 3 times to the three-day index return of $1526.46/1500 - 1 = 1.7640\%$: $50.00 \times (1 + 0.052920) = 52.6460$.
> C is wrong because it applies 3 times to the sum of daily returns ($4 - 5 + 3 = 2\%$) without compounding: $50.00 \times 1.06 = 53.00$.
> 2. **B.** Before the reset, exposure has grown with the index: $600 \times 1.04 = 624$ million.
> Net assets have grown by 3 times the index return: $200 \times (1 + 3 \times 0.04) = 224$ million, so the required exposure is $3 \times 224 = 672$ million.
> The fund must add $672 - 624 = 48$ million of notional exposure.
> A is wrong because $624 - 600 = 24$ million is the passive growth in exposure already embedded in the swaps, not the adjustment.
> C is wrong because $672 - 600 = 72$ million ignores that the existing swap notional has already grown to 624 million.
> 3. **B.** DWNX: $(1 - 2 \times 0.04)(1 - 2 \times (-0.05))(1 - 2 \times 0.03) - 1 = 0.92 \times 1.10 \times 0.94 - 1 = -0.048720$, or $-4.87\%$.
> The naive expectation was $-2 \times 1.764\% = -3.528\%$.
> DWNX delivered $-2$ times the index return on each day; the gap comes from compounding of daily resets on a volatile path.
> The client's belief that the fund failed its objective is a misunderstanding of how the product works, which is expectation-related risk.
> A is wrong because $-3.53\%$ is the naive multiple of the period return, exactly the misunderstanding in the complaint.
> C is wrong because no counterparty defaulted or failed to pay; the loss arose as designed.
> 4. **A.** An ETN is unsecured debt of its issuer, so counterparty risk is theoretically 100% of the note's value on an instantaneous default.
> The issuer's CDS spread is the monitoring tool, and a one-year CDS spread above 5%, here 5.8%, signals significant default risk.
> B is wrong because settlement risk describes a fund's exposure to unrealized swap gains between resets; an ETN holder is exposed to the whole note.
> C is wrong because ETN-2's premium reflects a soft closure (an issuance halt that breaks the arbitrage), a different issuer and a different risk; the decoy does not describe ETN-1's development.
> 5. **C.** Individual investors trade ETF shares only in the secondary market, on the exchange; creation and redemption is a primary-market transaction between the sponsor and authorized participants.
> A is wrong because access to redemption depends on being an AP, not on position size; 60,000 shares exceeding a typical 50,000-share creation unit is a decoy.
> B is wrong because it applies mutual fund mechanics; ETF shareholders who are not APs cannot redeem with the fund at NAV.
> 6. **A.** Leveraged and inverse ETFs are tactical tools for short-horizon views or hedges, because daily resets make returns over longer periods path dependent; positions held beyond short periods need periodic rebalancing.
> B is wrong because a permanent, unrebalanced core holding exposes clients to compounding decay and drift from the intended exposure.
> C is wrong because cash equitization calls for a liquid, unlevered ETF on the relevant benchmark; a 3 times fund would turn idle cash into leveraged exposure.

## Distractor design

1. B: leverage multiple applied to the period return (naive multiple); C: leverage multiple applied to the sum of daily returns (no compounding).
2. A: passive exposure growth read as the required trade; C: required exposure compared with the stale starting notional.
3. A: naive period multiple used; C: comprehension risk mislabeled as a credit risk because the product uses swaps.
4. B: fund swap-settlement label applied to a note holder; C: decoy soft-closure scenario substituted for issuer credit risk.
5. A: position size confused with AP status; B: mutual fund redemption mechanics applied to an ETF.
6. B: leveraged product treated as buy-and-hold; C: cash equitization confused with leveraged exposure.
