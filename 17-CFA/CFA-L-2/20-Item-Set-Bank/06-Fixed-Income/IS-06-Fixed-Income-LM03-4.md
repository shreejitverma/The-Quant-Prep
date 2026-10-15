---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 3
title: "Lindqvist Family Office Convertible Mandate"
los: [los-06-03-m, los-06-03-n, los-06-03-o, los-06-03-p, los-06-03-q]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Lindqvist Family Office Convertible Mandate

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Amara Deschamps, CFA, is the investment and compliance officer at the Lindqvist Family Office.
The family's investment policy statement (IPS) divides assets into a fixed-income sleeve and an equity sleeve.
The IPS permits the fixed-income sleeve to hold a convertible bond only while its price behaves primarily like a straight bond.
Convertibles whose price primarily follows the underlying share must be reclassified to the equity sleeve, and convertibles that trade as hybrids require investment committee sign-off.

The fixed-income sleeve holds a 2.25% annual-coupon convertible bond issued by Pellucid Semiconductor, par USD 1,000.
The bond is callable by Pellucid at par from 2027 and putable by the holder at par in 2028; the put is a soft put, so Pellucid may settle it in cash, shares, or a combination.
Exhibit 1 summarises the data Deschamps collected on 12 September.

**Exhibit 1: Pellucid convertible bond data**

| Item | Value |
|---|---|
| Conversion price at issuance | USD 40.00 |
| Share price at issuance | USD 32.00 |
| Current convertible bond price | USD 1,345 |
| Current share price | USD 52.00 |
| Straight value (non-convertible, same terms) | USD 960 |
| Threshold dividend per share | USD 0.40 |
| Current annual dividend per share | USD 0.25 |

A dealer's arbitrage-free model supplies the component values in Exhibit 2, each per bond.

**Exhibit 2: Dealer component values (USD per bond)**

| Component | Value |
|---|---|
| Straight bond | 960 |
| Call option on Pellucid shares | 412 |
| Pellucid's call option on the bond | 58 |
| Holder's put option on the bond | 31 |

Pellucid's board has announced a 5-for-4 stock split effective next month; the conversion terms in Exhibit 1 are those in force today.

The fixed-income sleeve also holds a three-year floating-rate note issued by Aldermoor Development Bank, a AAA supranational that Deschamps values with no credit spread.
The note pays the one-year reference rate set in arrears, with a floor of 3.25%.
Exhibit 3 shows the benchmark tree, calibrated at 12% volatility to par rates of 2.600%, 3.100% and 3.450%.

**Exhibit 3: One-year forward rates at 12% volatility**

| Node | Year 0 | Year 1 | Year 2 |
|---|---|---|---|
| Upper | 2.6000% | 4.0522% | 5.2624% |
| Middle | | | 4.1396% |
| Lower | | 3.1876% | 3.2563% |

Jonas Lindqvist, a family member who sits on the investment committee, makes two statements at the September meeting.

Statement 1: "The floor on the Aldermoor note only matters if rates fall in the future, so the note should be worth par today."

Statement 2: "The Pellucid bond is still a bond. Its value can never fall below USD 960, so it clearly belongs in the fixed-income sleeve."

Deschamps undertakes to calculate the bond's conversion metrics, check its price against the dealer model, and give the committee a recommendation on its classification under the IPS.

## Questions

1. Immediately after the stock split takes effect, the conversion price and conversion ratio of the Pellucid bond will be closest to: (LOS: los-06-03-n)
   - A. USD 32.00 and 31.25 shares.
   - B. USD 32.00 and 25.00 shares.
   - C. USD 50.00 and 20.00 shares.
2. Using the terms in force today, the market conversion premium ratio of the Pellucid bond is closest to: (LOS: los-06-03-o)
   - A. 3.35%
   - B. 3.46%
   - C. 40.10%
3. Suppose that the next day the Pellucid bond trades at USD 1,270 while the share price remains at USD 52.00. The minimum value of the bond and the appropriate response are: (LOS: los-06-03-o)
   - A. USD 960; there is no arbitrage because the price exceeds the straight value.
   - B. USD 1,300; buy the bond, convert it, and sell the shares for a gain of about USD 30 per bond.
   - C. USD 1,300; sell the bond short and buy the shares for a gain of about USD 30 per bond.
4. Using Exhibit 2, the arbitrage-free value of the Pellucid bond is closest to: (LOS: los-06-03-p)
   - A. USD 1,283
   - B. USD 1,345
   - C. USD 1,461
5. Regarding Statement 2, the most appropriate classification of the Pellucid bond under the IPS is: (LOS: los-06-03-q)
   - A. fixed-income sleeve, because the straight value of USD 960 limits the downside.
   - B. hybrid, requiring committee sign-off, because the share price is close to the conversion price.
   - C. equity sleeve, because the share price is well above the conversion price and the bond's price tracks the share.
6. The value of the Aldermoor floored floating-rate note is closest to: (LOS: los-06-03-m)
   - A. 99.337
   - B. 100.030
   - C. 100.663

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** A 5-for-4 split gives five shares for every four held, so the conversion price is multiplied by $4/5$ and the conversion ratio by $5/4$, preserving par (V6 p.167).
> Conversion ratio today $= 1{,}000/40.00 = 25$; after the split, conversion price $= 40.00 \times 0.8 = 32.00$ and ratio $= 25 \times 1.25 = 31.25$, and $32.00 \times 31.25 = 1{,}000$.
> B is wrong because it adjusts only the price and leaves the ratio, so conversion into 25 shares at USD 32.00 no longer covers par.
> C is wrong because it moves both terms in the wrong direction, penalising holders for the split.
> The dividend of USD 0.25 is below the USD 0.40 threshold dividend, so no dividend adjustment applies.
> 2. **B.** Market conversion price $= 1{,}345/25 = 53.80$; market conversion premium per share $= 53.80 - 52.00 = 1.80$; premium ratio $= 1.80/52.00 = 3.4615\%$, about 3.46% (V6 p.169, p.170).
> A is wrong because it divides the premium by the market conversion price: $1.80/53.80 = 3.3457\%$.
> C is wrong because it is the premium over straight value, $1{,}345/960 - 1 = 40.1042\%$, a different measure.
> 3. **B.** Conversion value $= 52.00 \times 25 = 1{,}300$; minimum value $= \max(1{,}300,\ 960) = 1{,}300$ (V6 p.168, p.169).
> At USD 1,270 the bond trades below its conversion value, so buying the bond, converting into 25 shares, and selling them locks in $1{,}300 - 1{,}270 = 30$ per bond.
> A is wrong because the floor is the greater of conversion value and straight value, not the straight value alone.
> C is wrong because it shorts the cheap asset and buys the expensive one, losing USD 30 per bond.
> 4. **B.** A callable putable convertible equals straight value plus the investor's call on the stock, minus the issuer's call on the bond, plus the investor's put: $960 + 412 - 58 + 31 = 1{,}345$ (V6 p.172).
> The model value equals the market price, so the bond is fairly priced on the dealer model.
> A is wrong because it subtracts the holder's put: $960 + 412 - 58 - 31 = 1{,}283$.
> C is wrong because it adds Pellucid's call: $960 + 412 + 58 + 31 = 1{,}461$.
> 5. **C.** The share price (USD 52.00) is 30% above the conversion price (USD 40.00), the conversion value (USD 1,300) far exceeds the straight value (USD 960), and the premium per share is only USD 1.80, so the bond behaves like the stock (V6 p.172, p.173).
> Under the IPS, such a convertible must be reclassified to the equity sleeve.
> A is wrong because the USD 960 floor is USD 385 below the price and is a moving floor; the price would have to fall a long way before the bond behaved like debt.
> B is wrong because hybrid behaviour requires the share to trade near the conversion price, not well above it.
> 6. **C.** Coupons are set in arrears at $\max(r_{\text{node}}, 3.25\%)$, so the floor binds wherever the node rate is below 3.25%.
> Year 2 nodes: 5.2624%, 4.1396% and 3.2563% all exceed 3.25%, so each node is worth 100.
> Year 1 upper: 4.0522% exceeds the floor, so the node is worth 100.
> Year 1 lower: 3.1876% is below the floor, so the Year 2 coupon is 3.25: $(3.25 + 100)/1.031876 = 100.0605$.
> Year 0: 2.6000% is below the floor, so the Year 1 coupon is 3.25: $(3.25 + 0.5 \times (100 + 100.0605))/1.026 = 100.6630$.
> The floor is worth $100.663 - 100 = 0.663$, added because the floor is an investor option (V6 p.162, p.163).
> A is wrong because it subtracts the floor as if it were an issuer option: $100 - 0.663 = 99.337$.
> B is wrong because it ignores that the floor already binds at Year 0: $(2.60 + 0.5 \times (100 + 100.0605))/1.026 = 100.030$.
> Statement 1 is therefore incorrect.

## Distractor design

- Q1: B adjusts only one term of the conversion terms (par not preserved); C applies the split adjustment in the wrong direction (sign).
- Q2: A divides the premium by the market conversion price instead of the share price (wrong denominator); C substitutes the premium over straight value (wrong formula variant).
- Q3: A takes the straight value as the whole floor (wrong formula variant); C reverses the arbitrage trade (sign).
- Q4: A subtracts the investor's put and C adds the issuer's call (holder-sign errors in the decomposition).
- Q5: A treats the straight-value floor as binding (bond-like misread); B places the share near the conversion price (misread exhibit).
- Q6: A treats the floor as an issuer option (sign); B skips the Year 0 reset (set-in-arrears timing error).
