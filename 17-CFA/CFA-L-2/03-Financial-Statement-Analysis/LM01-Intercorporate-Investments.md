---
type: cfa-lm
topic: "Financial Statement Analysis"
topic_code: "03"
topic_slug: "03-Financial-Statement-Analysis"
volume: 3
lm: 1
title: "Intercorporate Investments"
pages: "3-61"
weight_band: "10-15%"
difficulty: 4
los_count: 3
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/financial-statement-analysis]
---

# LM1: Intercorporate Investments

Difficulty 4 of 5: only three LOS, but they cover four accounting regimes (financial assets, equity method, consolidation, SPEs), every one of them carries a carrying-value or goodwill computation, and the item sets test the ratio consequences of switching between methods rather than a single number.

## LOS map

- **describe** the classification, measurement, and disclosure under International Financial Reporting Standards (IFRS) for 1) investments in financial assets, 2) investments in associates, 3) joint ventures, 4) business combinations, and 5) special purpose and variable interest entities (V3 p.3) ^los-03-01-a
    - Examiner asks: given a portfolio table with FVPL, FVOCI and amortized cost securities, compute the balance sheet carrying value and the income statement effect of each, or roll an equity method investment forward with excess purchase price amortization, or compute full and partial goodwill and the non-controlling interest at acquisition.
- **compare** and contrast IFRS and US GAAP in their classification, measurement, and disclosure of investments in financial assets, investments in associates, joint ventures, business combinations, and special purpose and variable interest entities (V3 p.3) ^los-03-01-b
    - Examiner asks: which standard permits partial goodwill, which requires the two-step goodwill impairment test, which allows impairment reversal on an equity method investment, which restricts the fair value option, and how contingent liabilities and potential voting rights are treated differently.
- **analyze** how different methods used to account for intercorporate investments affect financial statements and ratios (V3 p.3) ^los-03-01-c
    - Examiner asks: for the same investee, rank net profit margin, leverage, ROE, ROA, current ratio and asset turnover across the equity method, proportionate consolidation and full consolidation, and explain why net income to the parent is identical under all of them.

## Core intuition

Every company that owns a piece of another company has to answer one question before it can close its books: how much of the other company's assets, liabilities, revenues and profits belong on my statements?
The accounting answer is driven by influence, not by the cheque size (V3 p.4).
No significant influence means the investor is a passive holder and reports a financial asset.
Significant influence means the investor can shape the investee's policies, so it reports its share of the investee's earnings as they are earned, through the equity method.
Control means the investee is economically part of the investor, so every line of the investee is added to the investor's statements and a non-controlling interest is carved out for the shares the investor does not own.
Shared control is a joint venture, which is reported with the equity method (V3 p.4, p.11).
The percentage thresholds of 20% and 50% are presumptions, not rules; the exam repeatedly tests a 15% or 19% holder with board seats who must use the equity method, and a sub-50% holder who nevertheless controls (V3 p.4, p.10, p.14).

![[Intercorporate-Investment-Methods.excalidraw]]

> [!abstract] Idea 1: the level of influence picks the method, and the method picks which lines move
> Financial asset: one asset line, income from dividends, interest and fair value changes.
> Equity method: one asset line and one income line that captures the investor's share of the investee's net income (one-line consolidation).
> Consolidation: every asset, liability, revenue and expense line of the subsidiary at 100%, with goodwill and a non-controlling interest to reconcile the parent's purchase price to the shares it actually owns (V3 p.11, p.30, p.31).

### Financial assets: three measurement buckets

IFRS 9 replaced the old portfolio labels (held-to-maturity, available-for-sale, trading) with a two-question test on debt instruments (V3 p.6).
Question one is about the business model: are the assets held to collect contractual cash flows?
Question two is about the cash flows themselves: are they solely payments of principal and interest?
Pass both and the debt instrument sits at amortized cost, with interest income computed at the effective rate at purchase and the coupon-minus-income difference amortizing any premium or discount (V3 p.6, p.7, p.58).
If the business model is hold-to-collect-and-sell, the debt instrument goes to fair value through other comprehensive income (FVOCI), where interest still hits profit or loss but fair value swings park in OCI (V3 p.7).
Everything else, including anything designated to avoid an accounting mismatch, is fair value through profit or loss (FVPL) (V3 p.7).
Equity instruments cannot be at amortized cost, because their cash flows are not solely principal and interest.
Held-for-trading equity must be FVPL; other equity may be irrevocably elected into FVOCI, in which case only the dividend touches profit or loss and the fair value changes never recycle (V3 p.7).
Derivatives are FVPL unless they are hedging instruments (V3 p.8).
Reclassification of equity instruments is prohibited, and reclassification of debt is allowed only when the business model changes, without restating prior periods (V3 p.9).
The other IFRS 9 change is the move from an incurred loss model to an expected credit loss model, which recognizes 12-month expected losses on performing assets and lifetime expected losses on non-performing ones (V3 p.6, p.9).
US GAAP arrived at a similar but not identical place through ASC 825 and ASC 326 (V3 p.6).
The analyst's move is to strip investing items (interest, dividends, gains and losses) out of operating performance and to use the disclosed fair values for every class of investment when comparing companies (V3 p.9, p.10).

### Equity method: the investment account is a running share of the investee's equity

The economic reason for the equity method is that a significant-influence investor can affect the timing of dividends, so counting dividends as income would let the investor manage its own earnings (V3 p.14).
Instead the investor recognizes its share of the investee's net income when the investee earns it, and treats dividends as a return of capital that shrinks the investment account (V3 p.11, p.12, p.23).
The investment therefore behaves like a bank balance: it starts at cost, grows by the investor's share of profits, shrinks by dividends received, and shrinks again by the amortization of any excess purchase price (V3 p.12, p.18).
If losses drive the balance to zero, the investor stops recognizing losses and resumes only after later profits have absorbed the unrecognized losses (V3 p.12).

> [!abstract] Idea 2: cost minus book value splits into identifiable step-ups and goodwill, and only the step-ups on depreciable assets are amortized
> Excess purchase price equals cost less the investor's share of the investee's book value of net assets.
> First allocate the investor's share of each fair value step-up to the specific asset; the residual is goodwill.
> Step-ups on inventory, plant and finite-lived intangibles are amortized against equity income over the asset's life; step-ups on land and goodwill are not (V3 p.15, p.16, p.17).

Why is cost usually above book value?
Because the investee's balance sheet carries historical cost, while the buyer pays for fair values and for synergies (V3 p.15).
The allocation is never booked formally; the balance sheet shows a single line at cost, and the investor privately tracks the schedule so that each year's equity income is reduced by the amortization of the step-ups (V3 p.15, p.17).
Over time the investment balance drifts toward the ownership share of the investee's book value, and the clean identity that the exam loves is: investment balance equals the investor's share of the investee's book net assets plus the unamortized excess purchase price (V3 p.18).
If the investor's share of fair value exceeds cost, the excess is not a negative goodwill asset but income in the acquisition period (V3 p.15).

Goodwill inside an equity method investment is not separately tested; the whole investment is tested by comparing its recoverable amount (higher of value in use and fair value less costs to sell) with its carrying amount under IFRS, or its fair value with its carrying amount under US GAAP (V3 p.13, p.19).
IFRS allows reversal of an equity method impairment up to the recoverable amount; US GAAP does not (V3 p.19).
Both regimes allow a fair value option for equity method investments, but IFRS restricts it to venture capital organizations, mutual funds, unit trusts and similar entities, while US GAAP opens it to everyone; the election is irrevocable, no amortization is booked and no goodwill arises (V3 p.18, p.19).

Transactions between the investor and its associate cannot generate realized profit until the goods are used or sold to a third party, because the investor can set the terms and timing (V3 p.20).
Whether the sale is upstream (associate to investor) or downstream (investor to associate), the investor eliminates its ownership share of the profit still sitting in inventory, and adds it back when the goods leave the group (V3 p.20, p.22).
The mechanical rule is the same in both directions: unrealized profit equals total profit on the transaction times the fraction unsold, and the elimination equals the investor's percentage times that amount (V3 p.22).

Analysts should ask three questions about equity method reporting (V3 p.23).
Is the method itself appropriate, or is a 19% holder dodging associate losses, or a 25% holder capturing income without cash access?
Are large associate liabilities hidden off the investor's balance sheet, flattering debt ratios and net margin?
Are the equity earnings backed by dividend cash flow, given that the method recognizes income regardless of distributions?

### Joint ventures: equity method, with proportionate consolidation as the rare exception

A joint venture is a contractual arrangement establishing joint control (V3 p.11).
Both IFRS and US GAAP require the equity method; proportionate consolidation, where the venturer adds its share of each line of the venture, is allowed only in rare circumstances (V3 p.11).
Net income and total net assets are identical under the two methods, because the equity method's single line is the net of the same revenues, expenses, assets and liabilities.
The difference is entirely in the gross lines: proportionate consolidation raises sales, expenses, assets and liabilities, so margins fall and turnover and leverage measures change (V3 p.11).

### Business combinations: the acquisition method

Control triggers consolidation and the acquisition method, under both IFRS and US GAAP; pooling of interests is gone (V3 p.24, p.25).
IFRS does not distinguish legal forms, while US GAAP labels a combination as a merger (A + B = A), an acquisition (A + B = A and B, parent and subsidiary) or a consolidation (A + B = C), but the accounting is the same (V3 p.24, p.25).
The fair value of the consideration given, including the acquisition-date fair value of any contingent consideration, measures the acquisition; direct costs such as legal and valuation fees are expensed as incurred (V3 p.26).
The acquirer measures the acquiree's identifiable tangible and intangible assets and liabilities at fair value, including internally developed intangibles the acquiree never recognized, and recognizes contingent liabilities that are present obligations that can be measured reliably (V3 p.26).
Expected restructuring costs are not liabilities at the acquisition date; they are expensed later as incurred (V3 p.26, p.44).
IFRS records contingent liabilities whenever fair value can be reliably measured; US GAAP records contractual contingencies at fair value and non-contractual ones only if it is more likely than not that they meet the definition of a liability (V3 p.26, p.43).

> [!abstract] Idea 3: goodwill is a residual, and the only difference between full and partial goodwill is whether the non-controlling interest is measured at fair value or at its share of identifiable net assets
> Full goodwill equals the fair value of the whole entity less the fair value of identifiable net assets; the non-controlling interest is its share of the entity's fair value.
> Partial goodwill equals the consideration paid less the acquirer's share of the fair value of identifiable net assets; the non-controlling interest is its share of identifiable net assets.
> US GAAP requires full goodwill; IFRS allows either, transaction by transaction.
> Net income to the parent is identical under both, because 100% of the fair value step-ups are depreciated either way; only total assets and total equity differ, so ROA and ROE differ slightly (V3 p.27, p.31, p.33, p.34).

When the price is below the fair value of net identifiable assets, the acquisition is a bargain purchase and the difference is an immediate gain in profit or loss, never negative goodwill on the balance sheet (V3 p.27).
Goodwill has an indefinite life, is never amortized, and is tested for impairment at least annually (V3 p.27, p.34).
The post-combination balance sheet adds the parent's book values to 100% of the subsidiary's fair values, adds goodwill, adds the fair value of shares issued to capital stock and additional paid-in capital, and carries only the parent's retained earnings (V3 p.29, p.30).
In later periods, cost of goods sold and depreciation are higher than the sum of the separate companies because the subsidiary's inventory and PP&E were stepped up (V3 p.30).

The impairment tests differ in shape.
IFRS is one step: compare the recoverable amount of the cash-generating unit with its carrying amount including goodwill; any shortfall is the loss, first absorbed by goodwill and then allocated pro rata to the other non-cash assets of the unit (V3 p.34, p.35).
US GAAP is two steps: first compare the fair value of the reporting unit with its carrying amount to detect impairment, then measure the loss as carrying goodwill less implied goodwill, where implied goodwill is the fair value of the unit less the fair value of its identifiable net assets; the loss is capped at carrying goodwill and nothing else is automatically written down (V3 p.34, p.35, p.36).
Once written down, goodwill is never restored under either regime (V3 p.34).

### SPEs and VIEs: consolidation follows economic control, not voting shares

A special purpose entity is created by a sponsor for a narrow purpose, is often thinly capitalized, and used to be kept off the sponsor's balance sheet because the sponsor lacked a majority of the votes while guaranteeing the SPE's debt (V3 p.39, p.40).
The result was higher asset turnover, lower leverage and higher reported profitability, with Enron as the cautionary tale (V3 p.40).
IFRS 10 broadened control to power over the entity plus exposure or rights to variable returns, so a sponsor that benefits consolidates (V3 p.25, p.40).
US GAAP calls the broader class a variable interest entity, flags an entity as a VIE when equity at risk is insufficient or when equity holders lack decision-making ability, the obligation to absorb losses or the right to returns, and requires the primary beneficiary (the party that absorbs the majority of expected losses or receives the majority of residual returns) to consolidate regardless of voting interest (V3 p.25, p.40, p.41).
When a sponsor sells receivables to an SPE that borrows to pay for them, and then consolidates, the receivables come back, the SPE's debt becomes group debt, and any gain on the sale is reversed; the consolidated balance sheet is indistinguishable from direct borrowing (V3 p.41, p.42).

### Why the ratio effects are the heart of the exam

Take a parent that owns 50% of an investee and compare the equity method with consolidation.
Net income to the parent's shareholders is the same, because the single equity income line equals the parent's share of the same revenues and expenses (V3 p.11, p.59, p.61).
Consolidation shows all of the investee's revenue, so net profit margin and operating margin move toward the investee's own margins (V3 p.58, p.61).
Consolidation shows all of the investee's assets and liabilities plus goodwill, so total assets, total liabilities, leverage and the current ratio change; the equity method hides those liabilities (V3 p.23, p.61, p.62).
Consolidation adds the non-controlling interest to total equity, so return on equity computed on total equity is lower (V3 p.61).
These are the comparisons the practice sets for Cinnamon, Zimt, BetterCare and NinMount drill, and the comparison table in the formulas section is the summary to memorize.

## Formulas and derivations

**Amortized cost roll-forward and effective interest income** (V3 p.7, p.58)
$$
\text{Interest income}_t = r_{mkt,0} \times CV_{t-1}, \qquad CV_t = CV_{t-1} + \text{Interest income}_t - \text{Coupon}_t
$$
^f-03-01-1

- $r_{mkt,0}$: market yield at the purchase date; $CV$: carrying value (initial fair value, usually price paid); coupon $=$ stated rate $\times$ par.
- A premium (price above par, stated rate above market rate) makes the coupon exceed interest income, so the carrying value amortizes down toward par; a discount amortizes up (V3 p.58).
- Practice Problem 22: $0.04 \times 11{,}000{,}000 = 440{,}000$ income against a $500{,}000$ coupon, so the carrying value falls by $60{,}000$ to $10{,}940{,}000$ (V3 p.59).

> [!tip] Calculator
> Premium amortization for one period: `11000000 × 0.04 =` gives 440,000; `500000 - 440000 =` gives 60,000; `11000000 - 60000 =` gives 10,940,000.

**Income statement effect by financial asset category** (V3 p.7)
$$
\text{P/L}_{\text{FVPL}} = \text{Interest or dividends} + \Delta FV, \quad \text{P/L}_{\text{FVOCI}} = \text{Interest or dividends}, \quad \text{P/L}_{\text{AC}} = \text{Effective interest}
$$
^f-03-01-2

- $\Delta FV$: change in fair value during the period; for FVOCI it goes to other comprehensive income instead.
- Balance sheet carrying value is fair value for FVPL and FVOCI and amortized cost for AC (V3 p.7, p.58).
- Practice Problems 1 to 4 turn on exactly this split: reclassifying Dumas from amortized cost to FVPL would raise the carrying value by the unrealized gain and raise pre-tax earnings by the year's fair value change (V3 p.58).

**Equity method carrying value** (V3 p.12, p.18, p.21)
$$
I_t = I_{t-1} + p \times NI_t - p \times Div_t - A_t - p \times UP_t + p \times RP_t
$$
^f-03-01-3

- $I$: investment account; $p$: ownership share; $NI$, $Div$: investee net income and dividends; $A_t$: amortization of the excess purchase price; $UP_t$: profit on intra-group sales still unrealized at year end; $RP_t$: previously deferred profit realized this period.
- $I_0$ is cost, including directly related transaction costs (V3 p.13).
- Dividends are a return of capital, not income, which is why they reduce the balance and never appear in profit or loss (V3 p.11, p.23).
- The balance cannot go below zero; losses beyond that are unrecognized until later profits absorb them (V3 p.12).

**Equity income line** (V3 p.20, p.22)
$$
\text{Equity income}_t = p \times NI_t - A_t - p \times UP_t + p \times RP_t
$$
^f-03-01-4

- Same terms as Formula 3 without the dividend, because the income line is the change in the balance excluding distributions.
- Example 4: $0.25 \times 20{,}000 - 500 - 0.25 \times 8{,}000 = 2{,}500$ (V3 p.20).

**Excess purchase price** (V3 p.16)
$$
\text{Excess} = \text{Cost} - p \times BV_{\text{net assets}}
$$
^f-03-01-5

- $BV_{\text{net assets}}$: book value of the investee's net identifiable assets at acquisition.
- Example 2: $100{,}000 - 0.30 \times 220{,}000 = 34{,}000$ (V3 p.16).

**Allocation of excess to identifiable assets** (V3 p.16)
$$
\text{Step-up}_j = p \times \left(FV_j - BV_j\right)
$$
^f-03-01-6

- Computed asset by asset (or liability by liability) using acquisition-date fair values; liabilities with fair value below book value add to the step-up total.
- Example 2: plant $0.30 \times 30{,}000 = 9{,}000$, land $0.30 \times 20{,}000 = 6{,}000$ (V3 p.16).

**Goodwill in an equity method investment** (V3 p.15, p.16, p.17)
$$
GW = \text{Cost} - p \times FV_{\text{net identifiable assets}} = \text{Excess} - \sum_j \text{Step-up}_j
$$
^f-03-01-7

- The two forms are identical because $p \times FV = p \times BV + \sum_j p(FV_j - BV_j)$.
- Goodwill stays inside the single investment line, is not amortized, and is not separately impairment-tested (V3 p.15, p.19).
- If $p \times FV$ exceeds cost, the difference is income in the acquisition period, not negative goodwill (V3 p.15).

> [!tip] Calculator
> Example 3 in one pass: `1200000 × 0.3 =` gives 360,000; `500000 - 360000 =` gives 140,000; `300000 × 0.3 =` gives 90,000; `140000 - 90000 =` gives 50,000 goodwill.

**Annual amortization of a step-up** (V3 p.17)
$$
A_t = \sum_j \frac{\text{Step-up}_j}{\text{Useful life}_j}
$$
^f-03-01-8

- Straight-line unless told otherwise; land and goodwill have indefinite lives and contribute zero; an inventory step-up is expensed when the inventory is sold (V3 p.16, p.17).
- Example 2: $9{,}000 / 10 = 900$ per year against equity income and the investment balance (V3 p.17).

**Composition identity of the investment balance** (V3 p.18)
$$
I_t = p \times BV_{\text{net assets},t} + \left(\text{Excess} - \sum_{s \le t} A_s\right)
$$
^f-03-01-9

- $BV_{\text{net assets},t}$: the investee's book net assets at time $t$, after its own income, dividends and any unrealized profit adjustment.
- Reason: the excess is a cost borne by the investor, not the investee, so it sits on top of the investor's share of the investee's own equity (V3 p.18).
- Example 3: $0.30 \times 1{,}250{,}000 + (140{,}000 - 9{,}000) = 375{,}000 + 131{,}000 = 506{,}000$, matching the roll-forward (V3 p.18).

**Unrealized profit elimination on intra-group inventory** (V3 p.22)
$$
UP = (\text{Sale price} - \text{Cost}) \times \text{Fraction unsold}, \qquad \text{Elimination} = p \times UP
$$
^f-03-01-10

- Applies to both upstream and downstream sales; the fraction unsold can be computed from units or from sales value (V3 p.20, p.22).
- Alternative route: margin $\times$ ending intra-group inventory gives $UP$ directly, as in Example 5 ($0.40 \times 40{,}000 = 16{,}000$) (V3 p.22).
- The elimination reverses (adds back) in the period the goods are sold to third parties (V3 p.20, p.22).

**Full goodwill** (V3 p.27)
$$
GW_{\text{full}} = FV_{\text{entity}} - FV_{\text{identifiable net assets}}
$$
^f-03-01-11

- $FV_{\text{entity}}$: fair value of the acquiree as a whole (100%), often inferred as purchase price divided by the share acquired when no separate estimate is given (V3 p.61).
- Required under US GAAP; optional under IFRS (V3 p.27, p.31).
- Example 6: $1{,}000{,}000 - 900{,}000 = 100{,}000$ (V3 p.27).

**Partial goodwill** (V3 p.27)
$$
GW_{\text{partial}} = \text{Consideration} - p \times FV_{\text{identifiable net assets}}
$$
^f-03-01-12

- IFRS only, transaction by transaction (V3 p.27).
- Example 6: $800{,}000 - 0.80 \times 900{,}000 = 80{,}000$ (V3 p.27).
- Relationship: $GW_{\text{full}} - GW_{\text{partial}} = (1-p)(FV_{\text{entity}} - FV_{\text{identifiable net assets}})$ when consideration equals $p \times FV_{\text{entity}}$, which is the non-controlling interest's slice of goodwill.

**Non-controlling interest at acquisition** (V3 p.31, p.32)
$$
NCI_{\text{full}} = (1-p) \times FV_{\text{entity}}, \qquad NCI_{\text{partial}} = (1-p) \times FV_{\text{identifiable net assets}}
$$
^f-03-01-13

- Presented within equity on the consolidated balance sheet under both regimes (V3 p.31).
- Example 8: $0.10 \times 200{,}000 = 20{,}000$ (full) versus $0.10 \times 160{,}000 = 16{,}000$ (partial); the 4,000 gap equals the goodwill gap (V3 p.32, p.33).
- The balance sheet balances either way: extra goodwill on the asset side is matched by extra NCI on the equity side.

> [!tip] Calculator
> Practice Problem 28: `1500 × 0.2 =` gives 300 (partial); the full goodwill distractor is `2000 × 0.2 =` giving 400.

**Bargain purchase gain** (V3 p.27)
$$
\text{Gain} = FV_{\text{identifiable net assets}} - \text{Purchase price} \quad (>0)
$$
^f-03-01-14

- Recognized immediately in profit or loss under both IFRS and US GAAP (V3 p.27).
- Contingent consideration is measured at fair value at the combination date and later changes go through profit or loss (V3 p.28, p.43).

**Post-combination consolidated balance sheet** (V3 p.29, p.30)
$$
\text{Assets}_{\text{cons}} = BV_{\text{parent}} - I_{\text{parent}} + FV_{\text{sub identifiable assets}} + GW, \qquad \text{Equity}_{\text{cons}} = \text{Equity}_{\text{parent}} + NCI
$$
^f-03-01-15

- $I_{\text{parent}}$: the investment account on the parent's separate books, which is eliminated on consolidation (V3 p.62).
- Liabilities are the parent's book values plus the subsidiary's fair values (V3 p.29).
- Only the parent's retained earnings survive; shares issued as consideration add par to capital stock and the rest to additional paid-in capital (V3 p.30).
- Practice Problem 34: $2{,}140 - 320 + 1{,}070 + 60 = 2{,}950$ (V3 p.62).

**Consolidated income statement with NCI** (V3 p.33)
$$
NI_{\text{parent shareholders}} = NI_{\text{consolidated}} - (1-p) \times NI_{\text{sub, adjusted}}
$$
^f-03-01-16

- $NI_{\text{sub, adjusted}}$: the subsidiary's income after the extra depreciation on fair value step-ups, which the non-controlling interest shares (V3 p.33, p.34).
- Example 8 income table: $63{,}500 - 0.10 \times 63{,}500 = 57{,}150$ under both goodwill methods (V3 p.33).
- Why identical: the step-up depreciation is the same under both methods, so the only difference is in balance sheet totals (V3 p.34).

**IFRS goodwill impairment, one step** (V3 p.34, p.35)
$$
\text{Loss}_{\text{IFRS}} = \max\left(0,\; CV_{\text{CGU}} - \text{Recoverable amount}_{\text{CGU}}\right)
$$
^f-03-01-17

- Recoverable amount is the higher of value in use (present value of expected cash flows) and fair value less costs to sell (V3 p.19, p.34).
- The loss first reduces the goodwill allocated to the cash-generating unit; any remainder is allocated pro rata to the other non-cash assets (V3 p.34, p.35).
- Example 9: $1{,}400{,}000 - 1{,}300{,}000 = 100{,}000$; with a recoverable amount of 800,000 the loss is 600,000, of which 300,000 wipes goodwill and 300,000 hits other assets (V3 p.35).

**US GAAP goodwill impairment, two steps** (V3 p.34, p.35, p.36)
$$
\text{Step 1: } FV_{\text{RU}} < CV_{\text{RU}} \Rightarrow \text{impaired}; \qquad \text{Step 2: } \text{Loss} = \min\left(GW_{\text{carrying}},\; GW_{\text{carrying}} - \left(FV_{\text{RU}} - FV_{\text{identifiable net assets}}\right)\right)
$$
^f-03-01-18

- Implied goodwill $= FV_{\text{RU}} - FV_{\text{identifiable net assets}}$, computed exactly as in a business combination (V3 p.35).
- The loss cannot exceed carrying goodwill; no other assets are automatically written down (V3 p.35, p.36).
- Example 10: implied goodwill $1{,}300{,}000 - 1{,}200{,}000 = 100{,}000$, loss $300{,}000 - 100{,}000 = 200{,}000$ (V3 p.36).

> [!tip] Calculator
> Practice Problem 27 under IFRS: `15200 - 14900 =` gives 300.
> The US GAAP distractor is `14800 - 14400 =` giving implied goodwill 400, then `520 - 400 =` giving 120.

**Proportionate consolidation line items** (V3 p.11, p.59)
$$
\text{Line}_{\text{venturer}} = \text{Line}_{\text{own}} + p \times \text{Line}_{\text{JV}}
$$
^f-03-01-19

- Applies to every revenue, expense, asset and liability line; equity and net income are unchanged relative to the equity method (V3 p.11).
- Practice Problem 14: $686 + 0.5 \times 577 = 974.5$ total liabilities (V3 p.59).

**Implied fair value of the target from the price paid** (V3 p.61)
$$
FV_{\text{entity}} = \frac{\text{Purchase price}}{p}
$$
^f-03-01-20

- Used when the vignette gives a price for a fraction and the fair value of the whole is needed, as in Practice Problem 31: $320 / 0.5 = 640$ (V3 p.61).
- Assumes the price per share paid for the block is the fair value per share of the whole, which is the standard exam simplification.

**Ratio comparison across methods** (V3 p.11, p.23, p.34, p.61, p.62)
$$
NI_{\text{parent}}^{\text{equity}} = NI_{\text{parent}}^{\text{prop}} = NI_{\text{parent}}^{\text{cons}}, \qquad \text{Sales}^{\text{equity}} < \text{Sales}^{\text{prop}} < \text{Sales}^{\text{cons}}, \qquad \text{Assets}^{\text{equity}} < \text{Assets}^{\text{prop}} < \text{Assets}^{\text{cons}}
$$
^f-03-01-21

| Item | Equity method | Proportionate consolidation | Full consolidation (partial GW) | Full consolidation (full GW) |
|---|---|---|---|---|
| Revenue and expenses | Parent only | Parent plus share of JV | Parent plus 100% of subsidiary | Same as partial |
| Net income to parent | Same | Same | Same | Same |
| Total assets | Parent, one investment line | Parent plus share of JV assets | Parent plus 100% of subsidiary at fair value plus partial goodwill | Higher by NCI share of goodwill |
| Total liabilities | Parent only | Parent plus share of JV liabilities | Parent plus 100% of subsidiary | Same as partial |
| Total equity | Parent only | Parent only | Parent plus NCI (share of identifiable net assets) | Parent plus NCI (share of fair value) |
| Net profit margin | Highest | Middle | Lowest | Same as partial |
| Debt to equity | Lowest | Middle | Highest | Slightly lower than partial |
| ROE on total equity | Highest | Same as equity | Lower | Lowest |
| ROA | Highest | Middle | Lower | Lowest |
| Asset turnover | Depends on investee turnover versus parent | Moves toward JV | Moves toward subsidiary | Same direction as partial |

- The net income equality holds because equity income equals the parent's share of exactly the revenues and expenses that consolidation shows in gross (V3 p.11, p.59).
- Asset turnover under consolidation can be higher or lower than under the equity method; in the NinMount set it is higher because Boswell turns assets faster than the investment line does (V3 p.62).
- Example 8: ROA 8.28% versus 8.33% and ROE 13.45% versus 13.57% for full versus partial goodwill on identical net income (V3 p.34).

**Recoverable amount** (V3 p.19, p.34)
$$
\text{Recoverable amount} = \max\left(\text{Value in use},\; FV - \text{Costs to sell}\right)
$$
^f-03-01-22

- Value in use is the present value of the future cash flows expected from continuing use and disposal (V3 p.19, p.34).
- Used for both the equity method investment test and the IFRS cash-generating unit test (V3 p.19, p.34).

**Gain or loss on losing significant influence** (V3 p.13, p.14)
$$
\text{Gain} = \left(FV_{\text{retained interest}} + \text{Proceeds}\right) - I_{\text{carrying}}
$$
^f-03-01-23

- From the Deutsche Bank policy note; the retained stake is remeasured to fair value on the date the equity method stops (V3 p.13, p.14).
- The mirror case: a previously held financial asset that becomes an associate is remeasured to fair value through profit or loss, with any OCI balance reclassified (V3 p.13).

## Worked examples

### Example 1: Branch and Williams, balance in the investment account (V3 p.12)

Setup: Branch buys 20% of Williams for €200,000 on 1 January 2016; Williams earns €200,000, €300,000 and €400,000 and pays dividends of €50,000, €100,000 and €200,000 over 2016 to 2018.
Purchase price equals 20% of book value, so there is no excess to amortize.

Year by year with Formula 3:
- 2016: $200{,}000 + 0.20 \times 200{,}000 - 0.20 \times 50{,}000 = 200{,}000 + 40{,}000 - 10{,}000 = 230{,}000$.
- 2017: $230{,}000 + 60{,}000 - 20{,}000 = 270{,}000$.
- 2018: $270{,}000 + 80{,}000 - 40{,}000 = 310{,}000$.

Shortcut: $200{,}000 + 0.20 \times (900{,}000 - 350{,}000) = 200{,}000 + 110{,}000 = 310{,}000$ (V3 p.12).
Equity income reported each year is €40,000, €60,000 and €80,000; the dividends never touch the income statement.
Python check: `200000+0.2*(900000-350000) = 310000`. ^ex-03-01-1

### Example 2: Blake and Brown, excess purchase price and goodwill (V3 p.16, p.17)

Setup: Blake pays €100,000 for 30% of Brown; Brown's net assets are €220,000 at book and €270,000 at fair value, the €50,000 gap being plant (€30,000) and land (€20,000).

Step 1, excess (Formula 5): $100{,}000 - 0.30 \times 220{,}000 = 100{,}000 - 66{,}000 = 34{,}000$.
Step 2, allocation (Formula 6): plant $0.30 \times 30{,}000 = 9{,}000$; land $0.30 \times 20{,}000 = 6{,}000$.
Step 3, goodwill (Formula 7): $34{,}000 - 9{,}000 - 6{,}000 = 19{,}000$.
Check via the other form: $100{,}000 - 0.30 \times 270{,}000 = 100{,}000 - 81{,}000 = 19{,}000$.

Amortization (Formula 8) with a 10-year life for plant: $9{,}000 / 10 = 900$ per year; land and goodwill contribute nothing (V3 p.17).
Each year equity income and the investment balance are €900 lower than the naive share of Brown's income.
The balance sheet shows a single line, Investment in Brown €100,000, on the acquisition date (V3 p.16).
Python check: `100000-0.3*220000 = 34000`, `34000-9000-6000 = 19000`, `9000/10 = 900`. ^ex-03-01-2

### Example 3: Parker and Prince, goodwill and year-end balance (V3 p.17, p.18)

Setup: Parker pays €500,000 for 30% of Prince on 1 January 2018; Prince's net assets are €1,200,000 at book and €1,500,000 at fair value, the €300,000 difference being plant with 10 years of life.
Prince earns €100,000 and pays €50,000 in 2018.

Part 1, goodwill.
Excess $= 500{,}000 - 0.30 \times 1{,}200{,}000 = 500{,}000 - 360{,}000 = 140{,}000$.
Plant step-up $= 0.30 \times 300{,}000 = 90{,}000$.
Goodwill $= 140{,}000 - 90{,}000 = 50{,}000$ (V3 p.18).

Part 2, investment balance at 31 December 2018 (Formula 3).
$500{,}000 + 0.30 \times 100{,}000 - 0.30 \times 50{,}000 - 90{,}000 / 10 = 500{,}000 + 30{,}000 - 15{,}000 - 9{,}000 = 506{,}000$ (V3 p.18).
Equity income for the year is $30{,}000 - 9{,}000 = 21{,}000$.

Composition check (Formula 9).
Prince's ending net assets $= 1{,}200{,}000 + 100{,}000 - 50{,}000 = 1{,}250{,}000$; Parker's share $= 0.30 \times 1{,}250{,}000 = 375{,}000$.
Unamortized excess $= 140{,}000 - 9{,}000 = 131{,}000$.
Sum $= 375{,}000 + 131{,}000 = 506{,}000$, matching the roll-forward (V3 p.18).
Python check: `500000+30000-15000-9000 = 506000`, `0.3*1250000+131000 = 506000`. ^ex-03-01-3

### Example 4: Wicker and Foxworth, upstream inventory sale (V3 p.20, p.21)

Setup: Wicker pays €1,000,000 for 25% of Foxworth on 1 January 2018; Foxworth's book net assets are €3,800,000; a building is undervalued by €40,000 with 20 years of life; Foxworth earns €20,000, pays €3,200 in dividends, and its income includes €8,000 of profit on inventory sold to Wicker that Wicker still holds.

Excess and allocation first.
Excess $= 1{,}000{,}000 - 0.25 \times 3{,}800{,}000 = 1{,}000{,}000 - 950{,}000 = 50{,}000$.
Building step-up $= 0.25 \times 40{,}000 = 10{,}000$; amortization $= 10{,}000 / 20 = 500$ per year.
Goodwill $= 50{,}000 - 10{,}000 = 40{,}000$ (V3 p.21).

Part 1, equity income (Formula 4).
Share of reported income $= 0.25 \times 20{,}000 = 5{,}000$.
Less amortization $500$.
Less unrealized profit $0.25 \times 8{,}000 = 2{,}000$.
Equity income $= 5{,}000 - 500 - 2{,}000 = 2{,}500$ (V3 p.20).
The elimination is the investor's share only, because the profit sits in Foxworth's income and Wicker recognized 25% of it through the equity pickup.

Part 2, investment balance.
$1{,}000{,}000 + 2{,}500 - 0.25 \times 3{,}200 = 1{,}000{,}000 + 2{,}500 - 800 = 1{,}001{,}700$ (V3 p.21).

Composition check (Formula 9).
Foxworth's adjusted net assets $= 3{,}800{,}000 + (20{,}000 - 8{,}000) - 3{,}200 = 3{,}808{,}800$; Wicker's share $= 0.25 \times 3{,}808{,}800 = 952{,}200$.
Unamortized excess $= 50{,}000 - 500 = 49{,}500$.
Sum $= 952{,}200 + 49{,}500 = 1{,}001{,}700$ (V3 p.21).
Python check: `5000-500-2000 = 2500`, `1000000+2500-800 = 1001700`, `0.25*3808800+49500 = 1001700`. ^ex-03-01-4

### Example 5: Jones and Jason, downstream inventory sale (V3 p.21, p.22)

Setup: Jones owns 25% of Jason; amortization of excess purchase price is €8,000 per year; in 2017 Jones sold inventory costing €96,000 to Jason for €160,000; Jason resold €120,000 of it in 2017 and the rest in 2018; Jason earns €800,000 in 2017 and €820,000 in 2018.

Unrealized profit (Formula 10).
Total profit $= 160{,}000 - 96{,}000 = 64{,}000$.
Fraction unsold $= 1 - 120{,}000 / 160{,}000 = 0.25$.
Unrealized profit $= 64{,}000 \times 0.25 = 16{,}000$; Jones's share $= 0.25 \times 16{,}000 = 4{,}000$.
Alternative route: margin $64{,}000 / 160{,}000 = 40\%$ on €40,000 of unsold goods gives $16{,}000$, then $\times 0.25 = 4{,}000$ (V3 p.22).

Part 1, 2017 equity income.
$0.25 \times 800{,}000 - 8{,}000 - 4{,}000 = 200{,}000 - 8{,}000 - 4{,}000 = 188{,}000$ (V3 p.22).

Part 2, 2018 equity income.
The remaining goods are sold, so the deferred €4,000 is realized and added back.
$0.25 \times 820{,}000 - 8{,}000 + 4{,}000 = 205{,}000 - 8{,}000 + 4{,}000 = 201{,}000$ (V3 p.22).
Note the direction of the sale does not change the arithmetic; downstream profit sits in Jones's own income, but the elimination is still the ownership share run through equity income (V3 p.20).
Python check: `0.25*800000-8000-4000 = 188000`, `0.25*820000-8000+4000 = 201000`. ^ex-03-01-5

### Example 6: Full versus partial goodwill (V3 p.27)

Setup: Acquirer pays $800,000 for 80% of Acquiree; identifiable net assets have a fair value of $900,000; the whole entity is worth $1,000,000.

Partial goodwill (Formula 12, IFRS only): $800{,}000 - 0.80 \times 900{,}000 = 800{,}000 - 720{,}000 = 80{,}000$.
Full goodwill (Formula 11, US GAAP and IFRS option): $1{,}000{,}000 - 900{,}000 = 100{,}000$.
The $20,000 difference is the non-controlling interest's 20% share of total goodwill, and it shows up as a $20,000 higher NCI under full goodwill: $0.20 \times 1{,}000{,}000 = 200{,}000$ versus $0.20 \times 900{,}000 = 180{,}000$.
Python check: `800000-0.8*900000 = 80000`, `1000000-900000 = 100000`. ^ex-03-01-6

### Example 7: Franklin and Jefferson, post-combination balance sheet (V3 p.28 to p.30)

Setup: Franklin issues 1,000,000 shares of €1 par stock worth €15 each for 100% of Jefferson.
Jefferson's net assets are €1,900,000 at book and €5,400,000 at fair value (inventory up €1,300,000, PP&E up €2,000,000, long-term debt down €200,000).

Purchase price allocation (thousands).
Consideration $= 1{,}000{,}000 \times 15 = 15{,}000$.
Excess over book $= 15{,}000 - 1{,}900 = 13{,}100$.
Goodwill $= 15{,}000 - 5{,}400 = 9{,}600$.
Allocation of the excess: inventory 1,300, PP&E 2,000, debt 200, goodwill 9,600, total 13,100 (V3 p.29).

Consolidated balance sheet (thousands), parent book plus subsidiary fair value plus goodwill.
- Cash and receivables $10{,}000 + 300 = 10{,}300$.
- Inventory $12{,}000 + 3{,}000 = 15{,}000$.
- PP&E $27{,}000 + 4{,}500 = 31{,}500$.
- Goodwill $9{,}600$.
- Total assets $66{,}400$.
- Current payables $8{,}000 + 600 = 8{,}600$; long-term debt $16{,}000 + 1{,}800 = 17{,}800$; total liabilities $26{,}400$.
- Capital stock $5{,}000 + 1{,}000 = 6{,}000$; APIC $6{,}000 + 14{,}000 = 20{,}000$; retained earnings $14{,}000$ (Franklin's only); total equity $40{,}000$.
- Check: $26{,}400 + 40{,}000 = 66{,}400$ (V3 p.29).

Post-acquisition effect: cost of goods sold will be €1,300,000 higher as the stepped-up inventory sells, and depreciation €2,000,000 higher over the PP&E life, than if the two companies had reported separately (V3 p.30).
Python check: `15e6-5.4e6 = 9.6e6`, `10300+15000+31500+9600 = 66400`, `26400+40000 = 66400`. ^ex-03-01-7

### Example 8: Parent and Subsidiary, non-controlling interest under full and partial goodwill (V3 p.31 to p.34)

Setup: Parent issues shares worth €180,000 for 90% of Subsidiary; Subsidiary's shares are worth €200,000 in total; identifiable net assets are €100,000 at book and €160,000 at fair value (PP&E up €60,000).

Part 1, consolidated PP&E.
$235{,}000 + 155{,}000 = 390{,}000$ under both regimes, because 100% of the subsidiary's assets are consolidated at fair value regardless of the percentage owned (V3 p.32).

Part 2, full goodwill.
Goodwill $= 200{,}000 - 160{,}000 = 40{,}000$; NCI $= 0.10 \times 200{,}000 = 20{,}000$ (V3 p.32).

Part 3, partial goodwill.
Goodwill $= 180{,}000 - 0.90 \times 160{,}000 = 180{,}000 - 144{,}000 = 36{,}000$; NCI $= 0.10 \times 160{,}000 = 16{,}000$ (V3 p.32).

Balance sheets (V3 p.33).
Total assets: $55{,}000 + 205{,}000 + 390{,}000 + 40{,}000 = 690{,}000$ (full) versus $686{,}000$ (partial).
Total liabilities $75{,}000 + 190{,}000 = 265{,}000$ either way.
Equity: $20{,}000 + 267{,}000 + 138{,}000 = 425{,}000$ (full) versus $16{,}000 + 267{,}000 + 138{,}000 = 421{,}000$ (partial).
Capital stock is $87{,}000 + 180{,}000 = 267{,}000$ and retained earnings are the parent's €138,000.

Income statement (V3 p.33).
Income from continuing operations $= 250{,}000 - 137{,}500 - 10{,}000 - 39{,}000 = 63{,}500$; NCI share $0.10 \times 63{,}500 = 6{,}350$; income to parent $57{,}150$ under both methods.

Ratios (V3 p.34).
ROA: $57{,}150 / 690{,}000 = 8.28\%$ (full) versus $57{,}150 / 686{,}000 = 8.33\%$ (partial).
ROE: $57{,}150 / 425{,}000 = 13.45\%$ versus $57{,}150 / 421{,}000 = 13.57\%$.
Partial goodwill gives the higher returns because the denominators are smaller while the numerator is identical.
Python check: `57150/690000 = 0.08283`, `57150/686000 = 0.08331`, `57150/425000 = 0.13447`, `57150/421000 = 0.13575`. ^ex-03-01-8

### Example 9: Goodwill impairment under IFRS (V3 p.35)

Setup: a cash-generating unit has a carrying value of €1,400,000 including €300,000 of goodwill; recoverable amount €1,300,000; fair value of identifiable net assets €1,200,000.

One step (Formula 17): loss $= 1{,}400{,}000 - 1{,}300{,}000 = 100{,}000$, charged to goodwill, which falls to €200,000 (V3 p.35).
The €1,200,000 fair value of identifiable net assets is irrelevant under IFRS; it is there to tempt you into the US GAAP computation.

Variant: recoverable amount €800,000.
Loss $= 1{,}400{,}000 - 800{,}000 = 600{,}000$; goodwill absorbs €300,000 and the remaining €300,000 is allocated pro rata to the other non-cash assets of the unit (V3 p.35).
Python check: `1400000-1300000 = 100000`, `1400000-800000 = 600000`. ^ex-03-01-9

### Example 10: Goodwill impairment under US GAAP (V3 p.35, p.36)

Setup: a reporting unit has fair value $1,300,000, carrying value $1,400,000 including $300,000 of goodwill, and identifiable net assets with fair value $1,200,000.

Step 1: $1{,}300{,}000 < 1{,}400{,}000$, so impairment exists.
Step 2 (Formula 18): implied goodwill $= 1{,}300{,}000 - 1{,}200{,}000 = 100{,}000$; loss $= 300{,}000 - 100{,}000 = 200{,}000$; goodwill falls to $100,000 (V3 p.36).
Compare with Example 9: same inputs, IFRS loss 100,000 versus US GAAP loss 200,000, because US GAAP measures the shortfall in goodwill specifically rather than in the unit as a whole.

Variant: fair value of the unit $800,000.
Implied goodwill $= 800{,}000 - 1{,}200{,}000 = -400{,}000$, so the loss is capped at the $300,000 carrying goodwill and no other asset is written down automatically (V3 p.36).
Python check: `1300000-1200000 = 100000`, `300000-100000 = 200000`. ^ex-03-01-10

### Example 11: Odena receivables securitization through an SPE (V3 p.41, p.42)

Setup: Odena has cash €30M, receivables €60M, other assets €40M, liabilities €47M, equity €83M, and wants €55M.
Alternative 1: borrow €55M directly.
Alternative 2: put €5M into an SPE, have the SPE borrow €55M and buy the €60M of receivables.

Alternative 1: cash $30 + 55 = 85$; non-current liabilities $20 + 55 = 75$; total assets $185$; total liabilities $102$; equity unchanged at $83$.

Alternative 2, SPE alone: receivables 60, debt 55, equity 5.
Odena alone: receivables fall by 60, cash rises by $60 - 5 = 55$ to 85, and if the SPE paid more than carrying value (say €65M) Odena would book a gain (V3 p.42).
Consolidated (control exists): receivables 60, cash 85, other assets 40, total assets 185; non-current liabilities 75, total liabilities 102; equity 83.
The consolidated statements are identical to direct borrowing, and any gain on the sale is reversed in consolidation (V3 p.42).
The only economic advantage left is that a bankruptcy-remote SPE may borrow more cheaply (V3 p.42).
Python check: `30+55 = 85`, `85+60+40 = 185`, `27+75 = 102`, `102+83 = 185`. ^ex-03-01-11

## Item-set patterns

> [!warning] Trap 1: carrying value of a mixed portfolio
> The exhibit lists cost, prior-year market value and current-year market value for FVPL, FVOCI and amortized cost securities.
> Correct: FVPL and FVOCI at current market value, amortized cost at cost adjusted for premium or discount amortization (at cost if bought at par).
> Distractors: summing all three at market value (118,000 in Practice Problem 1), summing all three at cost (115,000 only coincidentally close), or using the prior-year market values (V3 p.46, p.58).

> [!warning] Trap 2: which line moves when a security is reclassified
> The question asks what happens to interest income, to pre-tax earnings, or to the carrying value if an amortized cost bond bought at par were FVPL.
> Correct: interest income is unchanged (coupon either way when bought at par), pre-tax earnings change by the year's unrealized gain or loss, carrying value changes by the cumulative unrealized gain.
> Distractors: saying interest income changes, or using the cumulative gain (5,000) when the question asks about the year's earnings effect (1,000) (V3 p.58).

> [!warning] Trap 3: premium versus discount and the direction of interest income
> The vignette says cost equals par except for one security whose par differs.
> Correct: par below cost means the bond was bought at a premium (stated rate above effective rate), so interest income is below the coupon; par above cost is a discount, so income exceeds the coupon.
> Distractor: picking the security whose par is above cost (Dumas at 55,000) as the one that lowers income (V3 p.58).

> [!warning] Trap 4: percentage versus influence
> A 15% or 19% holder has board representation and policy participation, or a 25% holder cannot access the investee's cash.
> Correct: significant influence is a judgment; board seats, policy participation, material transactions, personnel interchange and technological dependency establish it below 20%.
> Distractors: "financial asset because below 20%", or "controlling because it sits on the board" (V3 p.10, p.60).

> [!warning] Trap 5: goodwill in an equity method purchase
> Purchase price, ownership share, book and fair value tables are given.
> Correct: goodwill $=$ cost $-$ share $\times$ fair value of net identifiable assets, or excess less step-ups.
> Distractors: the whole excess over book value (99 in Practice Problem 24), the step-up only (39), or share $\times$ (fair value $-$ book value) of total assets rather than net assets (V3 p.60).

> [!warning] Trap 6: forgetting the amortization or the dividend in the roll-forward
> Investee income, dividends and a plant step-up with a remaining life are all given.
> Correct: cost plus share of income less share of dividends less step-up amortization.
> Distractors: skipping amortization (321 in Practice Problem 26), skipping the income pickup (282), or subtracting the full step-up in one year (V3 p.61).

> [!warning] Trap 7: full versus partial goodwill and the NCI
> The fair value of the entity and the fair value of identifiable net assets are both given, with a stated method.
> Correct: partial NCI $=$ minority share $\times$ identifiable net assets; full NCI $=$ minority share $\times$ entity fair value.
> Distractors: using entity fair value under partial (400 in Practice Problem 28), or the goodwill amount itself (500 equals 2,000 less 1,500) (V3 p.61).

> [!warning] Trap 8: which impairment test the question wants
> The exhibit supplies carrying value, recoverable amount, fair value of the unit and fair value of identifiable net assets, all at once.
> Correct: under IFRS use carrying less recoverable amount (300); under US GAAP use carrying goodwill less implied goodwill (520 less 400 equals 120).
> Distractor: the other regime's number, or fair value of the unit less identifiable net assets (400) reported as the loss (V3 p.61).

> [!warning] Trap 9: ratio ranking across methods
> Forecast statements for parent and investee are given and the question asks which method gives the highest margin, leverage, ROE or turnover.
> Correct: net income to the parent is identical; equity method has the smallest sales, assets, liabilities and equity, so highest margin, lowest debt to equity, highest ROE; consolidation adds NCI to equity and all investee liabilities.
> Distractors: "net income highest under consolidation", "equity unchanged under consolidation" (it rises by NCI), or claiming full and partial goodwill change net income (V3 p.58, p.59, p.61, p.62).

> [!warning] Trap 10: SPE consolidation
> A sponsor sells receivables to an SPE in which it holds no votes but absorbs the losses.
> Correct: it is the primary beneficiary and consolidates; revenue, receivables and cash are as if it borrowed directly and any gain on sale is reversed.
> Distractors: "off balance sheet because no voting interest", "consolidate only if a qualifying SPE" (that category no longer exists), or "revenue is higher because of the sale" (V3 p.41, p.42, p.58, p.59).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM01-Intercorporate-Investments-Practice-Problems]]

## Cross-links

- [[LM02-Employee-Compensation-Post-Employment-and-Share-Based]]: the same OCI-versus-profit-or-loss discipline used for FVOCI assets governs pension remeasurements, and both modules feed the analyst's comprehensive income adjustments.
- [[LM03-Multinational-Operations]]: consolidation of foreign subsidiaries applies the acquisition method mechanics here (100% of subsidiary lines, NCI, goodwill) and then translates them; goodwill translation and impairment interact.
- [[LM04-Analysis-of-Financial-Institutions]]: banks hold most of their balance sheet in IFRS 9 categories, so the amortized cost, FVOCI and FVPL rules and the expected credit loss model from this module are the foundation for analysing bank asset quality.
- [[LM05-Evaluating-Quality-of-Financial-Reports]]: choice of equity method versus consolidation, SPE structuring and goodwill impairment timing are core earnings and balance sheet quality warning signs.
- [[LM06-Integration-of-Financial-Statement-Analysis-Techniques]]: the ratio comparison table here is applied in the integration case, where the analyst removes equity method income and investments to compute operating ROA and adjusts leverage for unconsolidated affiliates.
- [[LM05-Residual-Income-Valuation]]: residual income models start from book value of equity, which depends on whether goodwill, NCI and equity method investments are recognized and on the clean surplus violations created by FVOCI and impairment reversals.
- [[LM04-Corporate-Restructuring]]: acquisitions are analysed in corporate issuers for value creation; this module supplies the accounting consequences of the same transactions, including goodwill, bargain purchases and contingent consideration.

## Self-test

Vignette A for Q1 to Q3: On 1 January 2024 Halden AG (IFRS) pays 600 for 40% of Vire SA, whose book net assets are 1,000.
Fair values exceed book values by 200 for plant (8 years remaining) and 150 for a patent (5 years remaining); all other fair values equal book values.
Halden has two board seats.
Vire reports 2024 net income of 300 and pays dividends of 100.
During 2024 Vire sold goods costing 100 to Halden for 150; 40% of the goods remain in Halden's inventory at year end (all figures in millions).

> [!question] Q1
> The goodwill embedded in Halden's investment in Vire is closest to:
> A. 60.
> B. 140.
> C. 200.

> [!question] Q2
> Ignoring the intra-group sale, Halden's investment in Vire at 31 December 2024 is closest to:
> A. 658.
> B. 680.
> C. 698.

> [!question] Q3
> Including the intra-group sale, Halden's 2024 equity income from Vire is closest to:
> A. 90.
> B. 98.
> C. 100.

Vignette B for Q4 to Q6: On 1 January 2025 Corvid Inc. acquires 75% of Petrel Ltd for cash of 1,200.
The fair value of Petrel's identifiable net assets is 1,300 and the fair value of Petrel as a whole is 1,600.
Separately, Corvid's cash-generating unit (also its reporting unit) has a carrying amount of 5,000 including goodwill of 800, a recoverable amount of 4,500, a fair value of 4,400 and identifiable net assets with fair value 4,000.

> [!question] Q4
> Under IFRS partial goodwill, the non-controlling interest recognized at acquisition is closest to:
> A. 300.
> B. 325.
> C. 400.

> [!question] Q5
> The difference between total equity under the full goodwill method and under the partial goodwill method at the acquisition date is closest to:
> A. 0.
> B. 75.
> C. 300.

> [!question] Q6
> The goodwill impairment loss on Corvid's unit under IFRS and under US GAAP, respectively, is closest to:
> A. 500 and 400.
> B. 400 and 500.
> C. 500 and 800.

Vignette C for Q7 to Q8: Brume plc (IFRS) buys a bond with par 10 million and an 8% annual coupon for 11.5 million when the market rate is 6%, and classifies it at amortized cost under a hold-to-collect model.
At the first year end its fair value is 11.6 million.
Brume also acquires a target for 4,200 whose identifiable net assets have a fair value of 4,600 and whose total fair value is 5,000.

> [!question] Q7
> The carrying value of the bond at the first year end is closest to:
> A. 11.39 million.
> B. 11.50 million.
> C. 11.60 million.

> [!question] Q8
> The acquisition of the target results in:
> A. goodwill of 400 on the balance sheet.
> B. a gain of 400 in profit or loss.
> C. a gain of 800 in profit or loss.

Vignette D for Q9 to Q10: Larkin Co. has sales 2,000, net income 150 (which includes equity income of 30 from its 60% subsidiary Sorrel), total assets 3,000 (including the investment in Sorrel at 360), liabilities 1,500 and equity 1,500.
Sorrel has sales 800, net income 50, assets 900, liabilities 400 and net assets 500 with fair values equal to book values.
Larkin paid 360 for its 60% stake, and Sorrel's total fair value is 600.
A separate 50% joint venture, Tarn, has revenue 600, assets 1,000, liabilities 400 and net income 40; Larkin carries it at 300 under the equity method.

> [!question] Q9
> If Larkin consolidates Sorrel under the partial goodwill method, its debt to equity ratio is closest to:
> A. 1.00.
> B. 1.09.
> C. 1.12.

> [!question] Q10
> If Larkin switched Tarn from the equity method to proportionate consolidation, which statement is most accurate?
> A. Total liabilities rise by 200 and equity is unchanged.
> B. Net income rises by 20 and total assets rise by 500.
> C. Revenue rises by 600 and net profit margin is unchanged.

> [!success]- Answer key
> Q1: A.
> Excess $= 600 - 0.40 \times 1{,}000 = 200$; step-ups $0.40 \times 200 = 80$ (plant) and $0.40 \times 150 = 60$ (patent); goodwill $= 200 - 80 - 60 = 60$ (Python: `200-80-60 = 60`).
> B deducts only the patent step-up; C is the whole excess over book value (V3 p.16).
>
> Q2: A.
> Amortization $= 80/8 + 60/5 = 10 + 12 = 22$.
> Balance $= 600 + 0.40 \times 300 - 0.40 \times 100 - 22 = 600 + 120 - 40 - 22 = 658$ (Python: `600+120-40-22 = 658`).
> B omits amortization; C omits the dividend (V3 p.18).
>
> Q3: A.
> Unrealized profit $= (150 - 100) \times 0.40 = 20$; Halden's share $= 0.40 \times 20 = 8$.
> Equity income $= 0.40 \times 300 - 22 - 8 = 120 - 22 - 8 = 90$ (Python: `120-22-8 = 90`).
> B is the pre-elimination figure $120 - 22 = 98$; C deducts the whole unrealized profit of 20 but forgets the 22 of amortization, and the upstream direction does not change the share-based elimination (V3 p.20, p.22).
>
> Q4: B.
> Partial NCI $= 0.25 \times 1{,}300 = 325$; A is 0.25 of 1,200 (the price, not the net assets); C is the full goodwill NCI $0.25 \times 1{,}600 = 400$ (V3 p.32).
>
> Q5: B.
> Full goodwill $= 1{,}600 - 1{,}300 = 300$; partial goodwill $= 1{,}200 - 0.75 \times 1{,}300 = 225$; the 75 difference equals $NCI_{\text{full}} - NCI_{\text{partial}} = 400 - 325 = 75$ and is the only difference in total equity (Python: `300-225 = 75`).
> A assumes no difference; C confuses the difference with full goodwill itself (V3 p.33).
>
> Q6: A.
> IFRS: $5{,}000 - 4{,}500 = 500$, first against goodwill.
> US GAAP: step 1, $4{,}400 < 5{,}000$; step 2, implied goodwill $4{,}400 - 4{,}000 = 400$, loss $800 - 400 = 400$ (Python: `5000-4500 = 500`, `800-400 = 400`).
> B swaps the regimes; C writes off all goodwill under US GAAP, which happens only when implied goodwill is at or below zero (V3 p.34 to p.36).
>
> Q7: A.
> Coupon $0.08 \times 10 = 0.80$ million; interest income $0.06 \times 11.5 = 0.69$ million; premium amortization $0.11$ million; carrying value $11.5 - 0.11 = 11.39$ million (Python: `11.5e6-110000 = 11390000`).
> B ignores amortization; C is fair value, which applies only to FVPL or FVOCI (V3 p.7, p.59).
>
> Q8: B.
> Price 4,200 is below the fair value of identifiable net assets 4,600, so this is a bargain purchase and the 400 difference is an immediate gain in profit or loss.
> A books negative goodwill, which neither regime allows; C uses the entity fair value, which is irrelevant to the gain (V3 p.27).
>
> Q9: C.
> Partial goodwill $= 360 - 0.60 \times 500 = 60$; NCI $= 0.40 \times 500 = 200$.
> Consolidated assets $= 3{,}000 - 360 + 900 + 60 = 3{,}600$; liabilities $= 1{,}500 + 400 = 1{,}900$; equity $= 1{,}500 + 200 = 1{,}700$; debt to equity $= 1{,}900 / 1{,}700 = 1.12$ (Python: `1900/1700 = 1.118`).
> A is the equity method ratio; B is the full goodwill ratio $1{,}900 / 1{,}740 = 1.09$, where NCI is $0.40 \times 600 = 240$ and goodwill is 100 (V3 p.33, p.61).
>
> Q10: A.
> Proportionate consolidation adds 50% of each line: liabilities rise by $0.5 \times 400 = 200$, assets rise by $0.5 \times 1{,}000 - 300 = 200$ net of the eliminated investment line, equity and net income are unchanged.
> B is wrong on both counts because net income does not change and the asset increase is 500 gross but 200 net; C is wrong because revenue rises by 300, not 600, and margin falls when revenue rises on unchanged income (V3 p.11, p.59).

## Flashcards

#flashcards/cfa-l2/03-Financial-Statement-Analysis/lm01

Presumed influence thresholds for intercorporate investments::Below 20% no significant influence, 20% to 50% significant influence, above 50% control; all are presumptions, not rules (V3 p.4).
Two IFRS 9 criteria for amortized cost::Business model is to hold to collect contractual cash flows, and cash flows are solely payments of principal and interest (V3 p.6, p.7).
Business model that leads to FVOCI for a debt instrument::Hold to collect and sell (V3 p.7).
Can an equity instrument be measured at amortized cost under IFRS 9?::No, equity is FVPL or, by irrevocable election for non-trading equity, FVOCI (V3 p.7).
What reaches profit or loss for an FVOCI equity investment?::Only dividend income; fair value changes stay in OCI and never recycle (V3 p.7).
Reclassification rule for financial assets under IFRS 9::Equity classifications are irrevocable; debt may be reclassified only when the business model changes, with no restatement of prior periods (V3 p.9).
IFRS 9 impairment model for loans::Expected credit loss model replacing incurred loss; 12-month expected losses for performing assets, lifetime for non-performing (V3 p.6, p.9).
Interest income on an amortized cost bond::Market rate at purchase times beginning carrying value; the coupon minus that income is the premium or discount amortization (V3 p.58).
Micro-problem: pay 11 million for par 10 million, 5% coupon, 4% market rate; year-end carrying value?::Income 440,000, coupon 500,000, amortization 60,000, carrying value 10.94 million; keystrokes 11000000 × 0.04 = then 500000 - 440000 = then 11000000 - 60000 = (V3 p.59).
Evidence of significant influence below 20%::Board representation, participation in policy making, material transactions, interchange of managerial personnel, technological dependency (V3 p.10).
IFRS versus US GAAP on potential voting rights when assessing significant influence::IFRS considers currently exercisable warrants, options and convertibles; US GAAP looks only at voting shares outstanding (V3 p.10).
Required method for joint ventures under IFRS and US GAAP::Equity method; proportionate consolidation only in rare circumstances (V3 p.11).
Why the equity method is called one-line consolidation::The investor's share of the investee's net assets is one balance sheet line and its share of net income is one income statement line (V3 p.11).
Treatment of dividends received under the equity method::Return of capital that reduces the investment account; not income (V3 p.11, p.23).
Equity method when losses reduce the investment to zero::Stop recognizing losses; resume only after later profits absorb the unrecognized losses (V3 p.12).
Equity method carrying value formula::Cost plus share of net income less share of dividends less amortization of excess purchase price less share of unrealized intra-group profit (V3 p.12, p.18, p.21).
Micro-problem: 20% bought for 200,000; cumulative income 900,000 and dividends 350,000; balance?::200,000 + 0.2 × 550,000 = 310,000 (V3 p.12).
Excess purchase price definition::Cost less the investor's share of the book value of the investee's net identifiable assets (V3 p.16).
Goodwill in an equity method investment::Cost less share of fair value of net identifiable assets; equals excess purchase price less allocated step-ups (V3 p.16, p.17).
Which step-ups are amortized against equity income?::Those on assets that are expensed or depreciated (inventory, plant, finite intangibles); land and goodwill are not (V3 p.17).
Micro-problem: 30% for 500,000; book net assets 1,200,000; plant undervalued 300,000 with 10-year life; goodwill and annual amortization?::Excess 140,000, step-up 90,000, goodwill 50,000, amortization 9,000 per year (V3 p.17, p.18).
Composition identity for the equity method balance::Share of investee's book net assets plus unamortized excess purchase price (V3 p.18).
Treatment when share of fair value exceeds cost in an equity method purchase::Excluded from the carrying amount and recognized as income in the acquisition period (V3 p.15).
Fair value option for equity method investments: who may use it?::US GAAP any entity; IFRS only venture capital organizations, mutual funds, unit trusts and similar entities; irrevocable at initial recognition (V3 p.18).
What happens to amortization and goodwill under the fair value option?::No amortization of excess cost and no goodwill; fair value changes, interest and dividends go to profit or loss (V3 p.19).
Equity method impairment test under IFRS::Compare the recoverable amount of the whole investment with its carrying amount; goodwill is not tested separately; reversal permitted (V3 p.13, p.19).
Equity method impairment under US GAAP::Recognize when fair value falls below carrying value and the decline is other than temporary; write down to fair value; no reversal (V3 p.19).
Recoverable amount::Higher of value in use and fair value less costs to sell (V3 p.19, p.34).
Upstream versus downstream sale::Upstream is associate to investor, downstream is investor to associate; in both, the investor eliminates its share of the unrealized profit (V3 p.20).
Unrealized profit elimination formula::Investor share times total profit on the sale times the fraction still unsold at period end (V3 p.22).
Micro-problem: 25% owner sells goods costing 96,000 for 160,000; 25% unsold; elimination?::64,000 × 0.25 = 16,000 unrealized; 0.25 × 16,000 = 4,000 deducted from equity income and added back when sold (V3 p.22).
Three analyst concerns about the equity method::Whether the method is appropriate given actual influence, investee liabilities hidden from debt ratios and net margin, and whether equity earnings are backed by dividend cash flow (V3 p.23).
US GAAP legal forms of business combinations::Merger (A + B = A), acquisition (A + B = A and B as parent and subsidiary), consolidation (A + B = C) (V3 p.24, p.25).
Measurement of the acquisition under the acquisition method::Fair value of consideration given including acquisition-date fair value of contingent consideration; direct costs expensed (V3 p.26).
Contingent liabilities in a business combination, IFRS versus US GAAP::IFRS recognizes if fair value can be measured reliably; US GAAP recognizes contractual ones at fair value and non-contractual ones only if more likely than not (V3 p.26, p.43).
Treatment of expected restructuring costs at acquisition::Not a liability at the acquisition date; expensed when incurred (V3 p.26, p.44).
Full goodwill formula::Fair value of the entity less fair value of identifiable net assets; required under US GAAP, optional under IFRS (V3 p.27).
Partial goodwill formula::Consideration paid less acquirer's share of fair value of identifiable net assets; IFRS only (V3 p.27).
Micro-problem: 800,000 for 80%; identifiable net assets 900,000; entity 1,000,000; partial and full goodwill?::Partial 800,000 - 720,000 = 80,000; full 1,000,000 - 900,000 = 100,000 (V3 p.27).
NCI measurement under full and partial goodwill::Full is NCI share of entity fair value; partial is NCI share of fair value of identifiable net assets (V3 p.31, p.32).
Bargain purchase treatment::Excess of fair value of net assets over price is an immediate gain in profit or loss (V3 p.27).
Which retained earnings survive a business combination?::Only the acquirer's; the target's earnings enter consolidated retained earnings only after the acquisition (V3 p.30).
Why net income to the parent is identical under full and partial goodwill::Step-up depreciation is the same under both methods and is shared with the NCI; only total assets and equity differ (V3 p.33, p.34).
IFRS goodwill impairment test::One step at the cash-generating unit; loss equals carrying amount less recoverable amount, first against goodwill then pro rata to other non-cash assets (V3 p.34, p.35).
US GAAP goodwill impairment test::Two steps at the reporting unit; if fair value is below carrying amount, loss equals carrying goodwill less implied goodwill, capped at carrying goodwill (V3 p.34 to p.36).
Implied goodwill::Fair value of the reporting unit less fair value of its identifiable net assets (V3 p.35).
Micro-problem: unit carrying 1,400,000 with goodwill 300,000, recoverable 1,300,000, fair value 1,300,000, identifiable net assets 1,200,000; loss under IFRS and US GAAP?::IFRS 100,000; US GAAP implied goodwill 100,000 so loss 200,000 (V3 p.35, p.36).
Can goodwill impairment be reversed?::No, under either IFRS or US GAAP (V3 p.34).
IFRS 10 definition of control::Power over the investee's financial and operating policy plus exposure or rights to variable returns (V3 p.25).
US GAAP VIE indicators::Equity at risk insufficient to finance activities without support, or equity holders lack decision-making ability, the obligation to absorb losses, or the right to returns (V3 p.40).
Who consolidates a VIE under US GAAP?::The primary beneficiary, the party absorbing the majority of expected losses or receiving the majority of residual returns, regardless of voting interest (V3 p.25, p.41).
Effect of consolidating a receivables securitization SPE::Receivables return, SPE debt becomes group debt, gain on sale is reversed, and the balance sheet matches direct borrowing (V3 p.42).
Which method gives the highest net profit margin for the same investee?::Equity method, because net income to the parent is identical but revenue is lowest (V3 p.58, p.61).
Which method gives the lowest debt to equity?::Equity method; consolidation adds investee liabilities and, under partial goodwill, a smaller NCI than under full goodwill (V3 p.58, p.61).
Trap: "net income is highest under consolidation"::Wrong; net income to parent shareholders is the same under equity method, proportionate consolidation and full consolidation (V3 p.59).
Trap: using the fair value of the unit less identifiable net assets as the IFRS impairment loss::Wrong; that is US GAAP implied goodwill; IFRS loss is carrying amount less recoverable amount (V3 p.61).
Trap: "SPE is off balance sheet because the sponsor holds no votes"::Wrong; control by exposure to losses or returns forces consolidation under both regimes (V3 p.41, p.58).
Micro-problem: 50% stake bought for 320 when net assets are 580 at fair value except unrecorded licenses; license value and annual amortization over 6 years?::Implied fair value 640, licenses 60, amortization 10 per year (V3 p.61).
Under the equity method the investment is classified as a {{non-current}} asset and the investor's share of profit and the carrying amount must be {{separately disclosed}} (V3 p.11).
Under IFRS 9, financial assets that are {{derivatives}} are measured at FVPL unless they are hedging instruments (V3 p.8).

## Common mistakes

1. Marking an amortized cost security to market when computing the portfolio carrying value; only FVPL and FVOCI sit at fair value (V3 p.58).
2. Confusing the direction of premium and discount amortization: par below cost is a premium and pushes interest income below the coupon (V3 p.58).
3. Deciding the accounting method by percentage alone and ignoring board seats, policy participation or contractual joint control (V3 p.4, p.10, p.60).
4. Counting dividends from an associate as income; under the equity method they reduce the investment and never reach profit or loss (V3 p.11, p.23).
5. Reporting the whole excess purchase price as goodwill instead of allocating the investor's share of each fair value step-up first (V3 p.16, p.60).
6. Amortizing goodwill or land step-ups, or forgetting to amortize plant and intangible step-ups in the year-end roll-forward (V3 p.17, p.61).
7. Eliminating 100% of the unrealized intra-group profit rather than the investor's ownership share, or forgetting to add it back when the goods are sold (V3 p.20, p.22).
8. Using entity fair value for the NCI under partial goodwill, or identifiable net assets under full goodwill (V3 p.32, p.61).
9. Booking negative goodwill on a bargain purchase instead of an immediate gain (V3 p.27).
10. Applying the US GAAP implied goodwill computation when the question says IFRS, or vice versa, when the exhibit supplies data for both (V3 p.35, p.36, p.61).
11. Assuming net income to the parent differs across the equity method, proportionate consolidation and full consolidation; only the gross lines, totals and NCI differ (V3 p.11, p.59, p.61).
12. Forgetting that consolidation adds the NCI to total equity, which lowers ROE on total equity and lowers debt to equity relative to a consolidation without NCI (V3 p.58, p.61).
13. Leaving the parent's investment account in consolidated total assets instead of eliminating it and replacing it with the subsidiary's fair-valued assets and goodwill (V3 p.62).
14. Treating an SPE as off balance sheet because the sponsor holds no voting shares, or believing IFRS has a qualifying SPE exemption (V3 p.41, p.58).
15. Capitalizing acquisition-related legal and valuation fees or expected restructuring costs into the purchase price; both are expensed (V3 p.26, p.44).
16. Reversing a goodwill impairment, or a US GAAP equity method impairment, when values recover; only IFRS equity method impairments may be reversed (V3 p.19, p.34).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "03-01" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
