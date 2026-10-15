---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 2
title: "Skagerrak Re: Quarter-End Option Book"
los: [los-07-02-f, los-07-02-g, los-07-02-h, los-07-02-i, los-07-02-j]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Skagerrak Re: Quarter-End Option Book

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Skagerrak Re is a Norwegian reinsurer that reports in Norwegian kroner (NOK).
Its treasury holds a small book of European options and must report fair values at each quarter-end.
Henrik Dahl, CFA, the head of treasury valuation, is reviewing the quarter-end marks prepared by junior analyst Ingvild Berg.
All rates in the exhibits are annualized, and every rate used for discounting is continuously compounded.

Berg's valuation memo opens with three statements about the Black-Scholes-Merton (BSM) model.

- Assumption 1: "The Fjordline share price follows geometric Brownian motion, so its continuously compounded returns are normally distributed."
- Assumption 2: "Because the model allows early exercise, it can value American-style Fjordline calls directly."
- Assumption 3: "Brokerage costs and taxes are small, so the model captures them through the risk-free rate."

Exhibit 1: Equity and currency positions

| Item | Fjordline Shipping call | USD put |
|---|---|---|
| Underlying price | NOK 240.00 per share | NOK 10.50 per USD |
| Exercise price | NOK 250.00 | NOK 10.50 |
| Time to expiration | 0.50 years | 0.50 years |
| Volatility | 30% | 10% |
| NOK risk-free rate | 4.00% | 4.00% |
| USD risk-free rate | not applicable | 5.00% |
| Model outputs | $d_1 = 0.0079$, $d_2 = -0.2042$, $N(d_1) = 0.5032$, $N(d_2) = 0.4191$ | Matching USD call value NOK 0.2646 |

Fjordline pays no dividends.
Skagerrak owns the USD put because a large share of its reinsurance premiums is received in US dollars.
Dahl asks Berg to derive the put value from the treasury system's value for the matching call.

Exhibit 2: Index futures, caplet, and swaption inputs

| Item | Value |
|---|---|
| OBX index level | 1,400.00 |
| OBX dividend yield | 2.00% |
| Three-month OBX futures price | 1,407.02 |
| OBX futures put: exercise 1,400, $T = 0.25$ | $N(d_1) = 0.5401$, $N(d_2) = 0.5042$, $N(-d_1) = 0.4599$, $N(-d_2) = 0.4958$ |
| Current three-month NIBOR | 4.30% |
| FRA rate, 6 x 9 months | 4.60% |
| Caplet: exercise rate 4.50%, expiry 0.50 years, 90/360 accrual | $N(d_1) = 0.5894$, $N(d_2) = 0.5338$ |
| Current five-year NOK swap rate (annual payments) | 4.20% |
| One-year forward, five-year NOK swap rate | 4.40% |
| Swaption: exercise rate 4.50%, expiry 1.00 year, PVA 4.2508 | $N(d_1) = 0.5031$, $N(d_2) = 0.4160$, $N(-d_1) = 0.4969$, $N(-d_2) = 0.5840$ |
| Continuously compounded risk-free rate for discounting | 4.00% (futures option), 4.20% (caplet) |

Skagerrak holds one OBX futures put, valued per index point, as a partial hedge of its equity portfolio.
It also holds a caplet on NOK 200,000,000 of the floating-rate loan that finances its Oslo headquarters.
The caplet expires in six months and is based on three-month NIBOR for the following three months; its payoff is set at expiry and paid three months later.

On 30 September, Dahl asks Berg about a new transaction.
Skagerrak plans to issue NOK 500,000,000 of five-year fixed-rate subordinated notes in one year and wants protection against a rise in swap rates before then.
Berg proposes a one-year European swaption on a five-year annual-pay swap with an exercise rate of 4.50%, and she prices it with the Black model using the inputs in Exhibit 2.

Dahl notes that the insurer also holds callable fixed-rate corporate bonds but says those will be discussed at the next review.

## Questions

1. Which of Berg's assumptions is consistent with the BSM model? (LOS: los-07-02-f)
   - A. Assumption 1.
   - B. Assumption 2.
   - C. Assumption 3.
2. Based on Exhibit 1, the BSM replicating portfolio for one long Fjordline call is closest to: (LOS: los-07-02-g)
   - A. long 0.4191 shares and borrowing NOK 123.31.
   - B. long 0.5032 shares and borrowing NOK 102.70.
   - C. long 0.5032 shares and borrowing NOK 104.78.
3. The value of the USD put derived from the matching call is closest to: (LOS: los-07-02-h)
   - A. NOK 0.0567.
   - B. NOK 0.2133.
   - C. NOK 0.3159.
4. The Black model value of the OBX futures put is closest to: (LOS: los-07-02-i)
   - A. 46.56.
   - B. 49.76.
   - C. 53.51.
5. The value of the caplet on the headquarters loan is closest to: (LOS: los-07-02-j)
   - A. NOK 64,108.
   - B. NOK 149,777.
   - C. NOK 151,358.
6. The swaption Berg should recommend for the planned note issue, and its value, are closest to: (LOS: los-07-02-j)
   - A. a payer swaption worth NOK 5,122,639.
   - B. a payer swaption worth NOK 7,261,217.
   - C. a receiver swaption worth NOK 9,386,617.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** BSM assumes the underlying follows geometric Brownian motion, so continuously compounded returns are normally distributed and prices are lognormal.
> B is wrong because BSM values European options only; American options need a lattice with an exercise test at every node.
> C is wrong because BSM assumes no frictions at all (no transaction costs or taxes), and the risk-free rate is a known constant, not a container for costs.
> 2. **B.** The call is replicated by buying $n_S = N(d_1) = 0.5032$ shares and shorting $N(d_2) = 0.4191$ zero-coupon bonds, each priced at $B = 250e^{-0.04 \times 0.5} = 250(0.980199) = 245.0497$.
> The borrowing is $0.4191(245.0497) = 102.7003$ and the share purchase costs $0.5032(240) = 120.7680$.
> Net cost $120.7680 - 102.7003 = 18.0677$, which matches the BSM call value of 18.06 to rounding in the $N(\cdot)$ values: a call is a leveraged position in the stock.
> A is wrong because it swaps the two probabilities, buying $N(d_2)$ shares and borrowing $N(d_1)B = 0.5032(245.0497) = 123.3090$.
> C is wrong because it borrows against the undiscounted exercise price, $0.4191(250) = 104.7750$, instead of the zero-coupon bond price $e^{-rT}X$.
> 3. **C.** For a currency option the underlying is the spot rate in domestic currency per unit of foreign currency (NOK per USD), the domestic NOK rate is the risk-free rate, and the foreign USD rate is the carry benefit $\gamma = r^f$.
> Carry-adjusted parity: $p = c - Se^{-r^f T} + Xe^{-rT} = 0.2646 - 10.50e^{-0.025} + 10.50e^{-0.020}$.
> With $10.50e^{-0.025} = 10.2408$ and $10.50e^{-0.020} = 10.2921$, $p = 0.2646 - 10.2408 + 10.2921 = 0.3159$ (full BSM put: 0.3159).
> The put exceeds the call because the USD carry rate is above the NOK rate, which lowers the expected NOK value of a dollar.
> A is wrong because it ignores the carry benefit, $0.2646 - 10.50 + 10.2921 = 0.0567$.
> B is wrong because it swaps the domestic and foreign rates, $0.2646 - 10.2921 + 10.2408 = 0.2133$.
> 4. **A.** The Black model uses the futures price, not the spot index, and discounts the whole bracket at the risk-free rate: $p = e^{-rT}[XN(-d_2) - F_0(T)N(-d_1)]$.
> Bracket: $1{,}400(0.4958) - 1{,}407.02(0.4599) = 694.1200 - 647.0885 = 47.0315$.
> Discount: $e^{-0.04 \times 0.25} = 0.990050$, so $p = 0.990050(47.0315) = 46.5635$, about 46.56; the dividend yield never enters because the futures price already embeds the carry.
> B is wrong because it substitutes the spot level 1,400.00 for the futures price, $0.990050[1{,}400(0.4958 - 0.4599)] = 0.990050(50.2600) = 49.7599$.
> C is wrong because it is the call, $0.990050[1{,}407.02(0.5401) - 1{,}400(0.5042)] = 0.990050(54.0515) = 53.5137$; Black futures parity confirms the put, $53.5137 - 0.990050(7.02) = 46.5635$.
> 5. **B.** The underlying is the 6 x 9 FRA rate of 4.60%, and because the rate is set at expiry and paid three months later, discounting runs to $t_{j-1} + t_m = 0.50 + 0.25 = 0.75$ years.
> Bracket: $0.0460(0.5894) - 0.0450(0.5338) = 0.0271124 - 0.0240210 = 0.0030914$.
> Value: $200{,}000{,}000 \times 0.25 \times e^{-0.042 \times 0.75} \times 0.0030914 = 50{,}000{,}000 \times 0.968991 \times 0.0030914 = $ NOK 149,777.
> A is wrong because it uses spot NIBOR 4.30% as the underlying, bracket $0.0430(0.5894) - 0.0240210 = 0.0013232$, value NOK 64,108.
> C is wrong because it discounts only to the option expiry, $e^{-0.042 \times 0.50} = 0.979219$, giving NOK 151,358.
> 6. **B.** A future fixed-rate issuer hurt by rising rates wants the right to pay fixed: a payer swaption, whose underlying is the one-year forward, five-year swap rate of 4.40%.
> $PAYSWN = (AP)(PVA)[R_{FIX}N(d_1) - R_X N(d_2)] = 1 \times 4.2508 \times [0.0440(0.5031) - 0.0450(0.4160)]$.
> Bracket: $0.0221364 - 0.0187200 = 0.0034164$, so value $= 500{,}000{,}000 \times 4.2508 \times 0.0034164 = $ NOK 7,261,217.
> A is wrong because it uses the current five-year swap rate 4.20% instead of the forward swap rate, bracket $0.0211302 - 0.0187200 = 0.0024102$, NOK 5,122,639.
> C is wrong because a receiver swaption pays off when rates fall, the opposite of the hedge; its value $500{,}000{,}000 \times 4.2508 \times [0.0450(0.5840) - 0.0440(0.4969)] = $ NOK 9,386,617 is higher only because the 4.50% strike is above the 4.40% forward rate.
> Payer minus receiver equals $500{,}000{,}000 \times 4.2508 \times (0.0440 - 0.0450) = -2{,}125{,}400$, which confirms both values.

## Distractor design

1. B: European-only model credited with early exercise (model scope); C: frictionless-market assumption misread as costs absorbed in the rate (assumption misread).
2. A: $N(d_1)$ and $N(d_2)$ swapped between stock and bond legs (wrong formula variant); C: bond leg priced at the undiscounted strike (spot vs present value).
3. A: carry benefit omitted from parity (wrong formula variant); B: domestic and foreign rates swapped (misread exhibit).
4. B: spot index used in place of the futures price (spot vs forward); C: call value reported instead of the put (call vs put formula).
5. A: spot NIBOR used in place of the FRA rate (spot vs forward); C: discounting stops at option expiry instead of the settlement date (period error).
6. A: current swap rate used in place of the forward swap rate (spot vs forward); C: receiver swaption chosen for a rising-rate hedge (direction error).
