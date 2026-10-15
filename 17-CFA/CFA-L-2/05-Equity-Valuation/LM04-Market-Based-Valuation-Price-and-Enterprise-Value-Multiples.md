---
type: cfa-lm
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
volume: 5
lm: 4
title: "Market-Based Valuation: Price and Enterprise Value Multiples"
pages: "221-335"
weight_band: "10-15%"
difficulty: 4
los_count: 18
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/equity-valuation]
---

# LM4: Market-Based Valuation: Price and Enterprise Value Multiples

Difficulty 4 of 5: eighteen LOS and seven multiples, each with a definition, a justified version derived from the Gordon growth model, a list of adjustments to the denominator and a comparables procedure, plus momentum indicators and harmonic means; the arithmetic is light but the item sets punish every definitional slip (trailing versus forward, basic versus diluted, EV versus market cap, SUE versus scaled surprise).

## LOS map

- **contrast** the method of comparables and the method based on forecasted fundamentals as approaches to using price multiples in valuation and explain economic rationales for each approach (V5 p.221) ^los-05-04-a
    - Examiner asks: which method rests on the law of one price and which on a DCF model, and which method can produce a relative but not an absolute misvaluation call.
- **calculate** and interpret a justified price multiple (V5 p.221) ^los-05-04-b
    - Examiner asks: given a DCF or residual income value and a forecast EPS or BVPS, compute the justified multiple and compare it with the actual multiple to call the stock over- or undervalued.
- **describe** rationales for and possible drawbacks to using alternative price multiples and dividend yield in valuation (V5 p.221) ^los-05-04-c
    - Examiner asks: which multiple survives negative EPS, which ignores cost structure, which mismatches an equity numerator with a pre-financing denominator, and which is a component of total return.
- **calculate** and interpret alternative price multiples and dividend yield (V5 p.221) ^los-05-04-d
    - Examiner asks: compute P/B after subtracting preferred equity, P/S from sales in billions and shares in billions, P/CF from EPS plus per-share depreciation, and a trailing dividend yield from four times the latest quarterly dividend.
- **calculate** and interpret underlying earnings, explain methods of normalizing earnings per share (EPS), and calculate normalized EPS (V5 p.221) ^los-05-04-e
    - Examiner asks: strip a nonrecurring gain and add back a nonrecurring charge while leaving a recurring depreciation increase alone, then normalize with either the historical average EPS or average ROE times current BVPS.
- **explain** and justify the use of earnings yield (E/P) (V5 p.221) ^los-05-04-f
    - Examiner asks: which metric gives a meaningful ranking when one company in the peer group has negative EPS, and why the negative-P/E stock ranks as the most expensive on E/P.
- **describe** fundamental factors that influence alternative price multiples and dividend yield (V5 p.221) ^los-05-04-g
    - Examiner asks: direction of change in P/E, P/B, P/S, P/CF, EV/EBITDA or D/P when r, g, ROE, profit margin, payout, WACC or ROIC moves.
- **calculate** and interpret a predicted P/E, given a cross-sectional regression on fundamentals, and explain limitations to the cross-sectional regression methodology (V5 p.221) ^los-05-04-h
    - Examiner asks: plug payout, beta and growth into a given regression, compare with the actual P/E, and name the three limitations (sample and period specific, unstable coefficients, multicollinearity).
- **calculate** and interpret the justified price-to-earnings ratio (P/E), price-to-book ratio (P/B), and price-to-sales ratio (P/S) for a stock, based on forecasted fundamentals (V5 p.221) ^los-05-04-i
    - Examiner asks: compute (1-b)/(r-g), (1-b)(1+g)/(r-g), (ROE-g)/(r-g) and (E/S)(1-b)/(r-g) from a vignette that supplies b, ROE, margin, r and g, sometimes with r hidden inside a CAPM.
- **calculate** and interpret the P/E-to-growth (PEG) ratio and explain its use in relative valuation (V5 p.221) ^los-05-04-j
    - Examiner asks: forward P/E divided by growth in percentage points, pick the lowest PEG as most attractive, and cite the three cautions (nonlinearity, no risk adjustment, no growth duration).
- **calculate** and explain the use of price multiples in determining terminal value in a multistage discounted cash flow (DCF) model (V5 p.221) ^los-05-04-k
    - Examiner asks: terminal value as benchmark trailing P/E times E_n or forward P/E times E_(n+1), contrasted with a Gordon growth terminal value built from payout, ROE and r.
- **evaluate** whether a stock is overvalued, fairly valued, or undervalued based on comparisons of multiples (V5 p.221) ^los-05-04-l
    - Examiner asks: compare the subject's multiple with a median, harmonic mean or adjusted benchmark and state the direction of misvaluation, remembering that a low multiple with lower growth and higher risk may be fairly valued.
- **evaluate** a stock by the method of comparables and explain the importance of fundamentals in using the method of comparables (V5 p.222) ^los-05-04-m
    - Examiner asks: explain a discount to the peer median by lower expected growth or higher beta, or explain why the conclusion may be wrong if the peers themselves are mispriced.
- **explain** alternative definitions of cash flow used in price and enterprise value (EV) multiples and describe limitations of each definition (V5 p.222) ^los-05-04-n
    - Examiner asks: which cash flow definition ignores working capital and noncash revenue (CF and EBITDA), which is most volatile and most often negative (FCFE), and which pre-interest flow is mismatched with a per-share price (EBITDA).
- **calculate** and interpret EV multiples and evaluate the use of EV/ EBITDA (V5 p.222) ^los-05-04-o
    - Examiner asks: build EV as market cap plus preferred plus minority interest plus debt less cash and short-term investments, divide by EBITDA equal to NI plus interest plus taxes plus D&A, and explain why EV/EBITDA beats P/EBITDA when leverage differs.
- **explain** sources of differences in cross-border valuation comparisons (V5 p.222) ^los-05-04-p
    - Examiner asks: which multiples are least affected by accounting differences (P/CFO, P/FCFE) and which are most affected (P/E, P/B, EBITDA-based), and how inflation and pass-through change justified P/E.
- **describe** momentum indicators and their use in valuation (V5 p.222) ^los-05-04-q
    - Examiner asks: distinguish scaled earnings surprise (divided by the dispersion of analyst forecasts) from SUE (divided by the standard deviation of historical surprises), and compute a relative-strength indicator scaled to 1.0.
- **explain** the use of the arithmetic mean, the harmonic mean, the weighted harmonic mean, and the median to describe the central tendency of a group of multiples (V5 p.222) ^los-05-04-r
    - Examiner asks: compute a harmonic mean of five P/Es, state that it dampens large outliers but not small ones, and recognize that the weighted harmonic mean reproduces the portfolio's aggregate P/E.

## Core intuition

A multiple is a price divided by one unit of something the buyer values: a unit of earnings, of book equity, of sales, of cash flow, or of dividends (V5 p.222).
A P/E of 20 says the market charges 20 units of currency for one unit of annual earnings, and an EV/EBITDA of 10 says an acquirer buying the whole enterprise, debt included, pays 10 years of pre-interest, pre-tax, pre-depreciation operating flow (V5 p.223, p.284).
Nothing in that number tells you whether 20 is cheap or dear; it only becomes information when set against a benchmark, and there are exactly two ways to build the benchmark (V5 p.223).

> [!abstract] Idea 1: two methods, two rationales, one algebra
> The method of comparables rests on the law of one price: similar assets should sell at similar multiples, so the benchmark is the multiple of a matched stock, a peer median, an industry or index multiple, or the stock's own history (V5 p.223, p.224).
> The method based on forecasted fundamentals rests on DCF: a multiple is the DCF value divided by a forecast fundamental, so the benchmark is the justified multiple implied by r, g, payout, ROE or margin (V5 p.225).
> The comparables method can only ever say "cheap relative to the comps"; the comps themselves may be mispriced, so a relative call is not an absolute call unless you also assume the comparison assets are fairly priced (V5 p.224, p.225).
> Fundamentals matter to the comparables user too, because no two companies are identical and the only defensible way to adjust a peer median is to point to a difference in growth, risk or profitability (V5 p.225, p.244).

The bridge between the two methods is the justified multiple.
Take any DCF value and divide it by the forecast fundamental: a DCF value of GBP 10.20 with forecast EPS of GBP 1.2 is a justified forward P/E of 8.5 (V5 p.225).
Take a peer median P/B of 2.2 and it is a justified P/B by comparables; multiply by BVPS of 23 and it becomes a fair value of 50.60 (V5 p.225, p.226).
The exam alternates between these two directions endlessly: multiply a benchmark by the fundamental to get a price, or divide the price by the fundamental to get a multiple to compare.
Both directions give the same verdict, so if the justified multiple exceeds the actual multiple the stock is undervalued, and if the benchmark times EPS exceeds the price the stock is undervalued (V5 p.225).

### Why P/E first, and why its denominator is the whole problem

Earning power is the chief driver of value and P/E is the most used multiple in surveys, but everything difficult about P/E lives in the denominator (V5 p.227).
EPS can be zero, negative or tiny; it mixes transient and recurring components; and it is shaped by accounting choices (V5 p.227).
The curriculum therefore spends pages on four adjustments before any P/E is computed: dilution, nonrecurring items, cyclicality and accounting comparability (V5 p.228).
Dilution is the easy one because companies report both basic and diluted EPS, and diluted EPS is preferred for comparisons, which raises the P/E (V5 p.228, p.229).
Nonrecurring items require judgment: the analyst hunts for asset sale gains, write-downs, impairments and provisions inside continuing operations, and does not accept the company's own "core" or non-GAAP figure at face value because it is a non-IFRS concept with no rules (V5 p.229, p.230, p.231).
Cyclicality is different in kind because business cycles repeat, so cyclical effects are transitory yet recurring; the fix is to normalize EPS to a mid-cycle level rather than to strip it out (V5 p.231).
The Molodovsky effect is the countercyclical behavior of P/E: high P/Es on depressed trough earnings and low P/Es on peak earnings, with no change in prospects (V5 p.231).

> [!abstract] Idea 2: normalize, then invert if the number is still useless
> Two normalization methods: average EPS over the last full cycle, or average ROE over the cycle times current BVPS; the second is usually preferred because it captures growth or shrinkage in the size of the business (V5 p.231, p.232).
> When EPS is negative, P/E is technically computable but meaningless, because the negative-P/E stock ranks below the cheapest positive-P/E stock while actually being the most expensive per unit of earnings (V5 p.233).
> The cure is the inverse price ratio E/P: price is never negative, so earnings yield ranks every stock correctly from cheapest (highest E/P) to most costly, and its distribution is less skewed by outliers than the P/E distribution (V5 p.234).
> The same logic gives B/P, S/P, CF/P and D/P; dividend yield is the standard form because P/D is undefined for non-payers while D/P is simply zero (V5 p.234, p.235, p.281).

Trailing P/E uses the last four quarters of EPS; forward (leading, prospective) P/E uses next year's expected EPS, where "next year" may mean the next four quarters, the next twelve months (NTM) or the next fiscal year (V5 p.227, p.228, p.235).
For rising earnings the forward P/E is systematically lower than the trailing P/E because the denominator is bigger, so mixing definitions across companies is not a random error but a biased one (V5 p.228).
Valuation is forward looking, so analysts prefer forward P/E when forecasts exist, and they must use forward P/E when an acquisition, divestiture or leverage change makes the past irrelevant; they fall back to trailing P/E when earnings are unpredictable (V5 p.228).
For volatile earners the forward P/E can swing from 8.1 to 13.6 to not meaningful depending only on which "next year" is chosen, which is the practical argument for normalizing (V5 p.237).

### Where the justified P/E comes from

Start with the Gordon growth model and divide both sides by earnings.
Dividing $P_0 = D_1/(r-g)$ by $E_1$ gives the forward P/E $(1-b)/(r-g)$; dividing by $E_0$ and writing $D_1 = D_0(1+g) = E_0(1-b)(1+g)$ gives the trailing P/E $(1-b)(1+g)/(r-g)$ (V5 p.238).
The justified P/E rises with expected growth and falls with required return, and that intuition survives in every more complex DCF model even when no closed form exists, in which case the justified P/E is simply the model value divided by forecast EPS (V5 p.239).
A second route to a fundamentals-based P/E is a cross-sectional regression of P/E on payout, growth and beta, which is quick but rarely a main tool because it is specific to its sample and period, its coefficients drift over years, and multicollinearity makes individual coefficients uninterpretable (V5 p.240, p.241).

### The comparables procedure and its benchmark ladder

Four steps: pick and compute the multiple; pick the comparison assets and compute their median or mean; apply the benchmark (possibly adjusted for fundamentals) to estimate value or compare it with the actual multiple; then ask whether the gap is explained by fundamentals (V5 p.242).
Benchmarks run from the closest match outward: a matched stock, the peer group median, the industry or sector, the equity index, and the stock's own past P/E (V5 p.242).
Averaging over a group reduces valuation error relative to a single comp, and the median beats the mean whenever outliers like a P/E of 70.67 or a not-meaningful negative P/E are in the sample (V5 p.242, p.245).
The two adjustments the exam expects are directional: higher expected growth than the peers justifies a higher P/E, and higher risk justifies a lower one (V5 p.244).
PEG packages the growth adjustment into one number, P/E per percentage point of growth, with lower being cheaper and below 1 sometimes read as attractive; but it assumes linearity between P/E and growth, ignores risk, and ignores the duration of growth (V5 p.246).
Broadening the comparison set to an industry or the whole market helps detect whether the peer group itself is mispriced, as would have been true for internet stocks in 1998 to 2000 (V5 p.248).
Own-history P/E rests on mean reversion, and the justified price is the historical benchmark P/E times the most recent (or normalized) EPS, but the method fails when the business mix, leverage or inflation environment has changed (V5 p.251, p.252, p.253).

Two market-level P/E models close the P/E section.
The Fed model sets the market's justified P/E at the reciprocal of the 10-year Treasury yield and calls the market overvalued when the earnings yield is below the bond yield; it ignores growth and the equity risk premium, mishandles inflation, and blows up at low rates, giving a justified P/E of 36.8 at a 2.72% yield (V5 p.250, p.251).
The Yardeni model adds growth: earnings yield equals the A-rated corporate bond yield minus a weight $b$ times consensus long-term growth, so justified P/E is $1/(CBY - b \times LTEG)$ (V5 p.251).
Inflation enters through cost pass-through: with a real required return $\rho$ and pass-through fraction $\lambda$, justified P/E is $1/[\rho + (1-\lambda)I]$, so higher inflation or lower pass-through lowers P/E, and full pass-through makes P/E immune to inflation (V5 p.254, p.255).
Finally, a benchmark P/E can price the terminal value of a multistage DDM: $V_n$ is a trailing terminal P/E times $E_n$ or a forward terminal P/E times $E_{n+1}$, grounded in market data but importing any mispricing in the benchmark (V5 p.255, p.256).

### P/B, P/S, P/CF and D/P follow the same template

P/B uses a stock variable from the balance sheet, so it is positive when EPS is not, more stable than EPS, natural for financial firms whose assets are near market value, and relevant for non-going concerns; its weaknesses are unrecorded human capital and internally generated intangibles, historical-cost assets distorted by inflation and technology, different business models with different asset intensity, and buybacks above book that shrink BVPS (V5 p.257, p.258, p.259).
Book value is common shareholders' equity, meaning total equity less preferred (and any preferred dividends in arrears), divided by common shares outstanding; tangible book removes goodwill and intangibles, and fair value footnotes can adjust financial assets and liabilities (V5 p.259, p.260, p.261, p.264).
The justified P/B is $(ROE - g)/(r - g)$, obtained by writing $E_1 = ROE \times B_0$ and $b = g/ROE$ in the Gordon model; what matters is ROE relative to r, and with no growth it collapses to ROE/r (V5 p.265).
The residual income form $1 + PV(\text{residual income})/B_0$ says P/B exceeds 1 exactly when the firm earns more than its cost of equity (V5 p.265, p.266).

P/S uses the top line, which is harder to manipulate than EPS or book, positive for going concerns, and stable; but sales growth without profit has no value, P/S ignores cost structure, and price is an equity claim while sales are pre-financing, which is why EV/S exists (V5 p.268, p.290).
The identity $P/S = (P/E) \times \text{net margin}$ links the two, and the justified P/S is margin times payout over $(r-g)$, so margin drives P/S directly and again through $g = b \times PM \times \text{turnover} \times \text{leverage}$ (V5 p.268, p.269, p.272).
Revenue recognition abuses (advertising barter, bill-and-hold, gross versus net booking) are the P/S analyst's specific hazard (V5 p.269, p.270, p.271).

Price to cash flow is less manipulable and more stable than P/E, but the label hides four denominators: CF (EPS plus per-share depreciation, amortization and depletion), CFO, FCFE and EBITDA (V5 p.275, p.277).
CF ignores working capital and noncash revenue, so front-loaded revenue slips past it; FCFE is the theoretically correct flow but is volatile and often negative; CFO can be dressed up by securitizing receivables or outsourcing payables, and IFRS lets interest and dividends move between sections; EBITDA is pre-interest and so belongs with EV, not price (V5 p.275, p.276, p.278).
Accelerated versus straight-line depreciation can manufacture 29% EPS growth out of identical cash flows, which is the clearest case for looking at cash flow (V5 p.276, p.277).

Dividend yield is a component of total return and the safer component, but it is only one component, dividends paid now displace future earnings, and the safety argument assumes biased pricing of return components (V5 p.280).
The trailing yield uses the dividend rate (four times the latest quarterly dividend, or the latest annual total for uneven semiannual payers); the justified yield is $(r-g)/(1+g)$, falling with growth and rising with r, which is why high-yield screens are value screens (V5 p.281, p.282).

> [!abstract] Idea 3: match the numerator to the claimant of the denominator
> Price is a claim of common shareholders, so it belongs over post-interest, post-preferred per-share flows: EPS, BVPS, FCFE, dividends.
> EBITDA, EBIT, FCFF and sales are flows to all capital providers, so they belong under enterprise value, which is market equity plus preferred plus minority interest plus debt less cash and short-term investments, the net price an acquirer pays for the whole business (V5 p.278, p.284, p.285).
> P/EBITDA and P/S are logical mismatches; EV/EBITDA and EV/S fix them and are the multiples to use when leverage differs across the comps (V5 p.278, p.290).
> Justified EV/EBITDA rises with FCFF growth and ROIC and falls with WACC, the firm-level analogues of g, ROE and r (V5 p.287).

EV/EBITDA is the workhorse for capital-intensive and highly levered businesses because EBITDA is pre-interest and pre-depreciation and is often positive when EPS is negative; its flaws are that it overstates operating cash flow when working capital grows and that it ignores capital expenditure, unlike FCFF (V5 p.284).
Total invested capital (TIC) is EV before deducting cash, and rankings by TIC/EBITDA and EV/EBITDA differ only when cash relative to EBITDA differs materially across the comps (V5 p.287, p.288).
Alternative denominators, EBITA and EBIT, drop information about capital spending as you move down the list but suit companies where only amortization, or neither charge, is material (V5 p.289, p.290).

### International, momentum and averaging

Cross-border comparisons fail on accounting standards, culture, macro context and the resulting risk and growth differences; IFRS versus US GAAP reconciliations showed goodwill, deferred taxes, FX, R&D, pensions and revaluations as the recurring gaps, and P/CFO and P/FCFE are least affected while P/E, P/B and EBITDA multiples are most affected (V5 p.291, p.293).
Momentum indicators compare price or earnings with their own history or expectation rather than with a fundamental: unexpected earnings is actual minus expected EPS, scaled earnings surprise divides that by the standard deviation of analysts' forecasts, SUE divides it by the standard deviation of past surprises, and relative strength divides a stock's price by an index level and rescales to 1.0 at the start (V5 p.293, p.294, p.296, p.297).
The exam's favorite distinction is the denominator of SUE (historical surprise dispersion) versus scaled surprise (analyst forecast dispersion) (V5 p.294, p.330).
Finally, when averaging multiples, the arithmetic mean is inflated by large outliers, the median is immune to them, the harmonic mean (reciprocal of the mean of reciprocals) dampens large outliers but can aggravate small ones near zero, and the weighted harmonic mean is exactly the portfolio's aggregate P/E, which is why index vendors use it (V5 p.299, p.300).
Two practical cautions close the module: look-ahead bias when back-testing trailing multiples with EPS that was not yet reported, and screens that omit profitability, risk and qualitative factors (V5 p.303, p.305).

## Formulas and derivations

**Trailing and forward P/E** (V5 p.227, p.228, p.235)
$$
\text{Trailing P/E} = \frac{P_0}{\text{EPS}_{\text{last 4 quarters}}}, \qquad \text{Forward P/E} = \frac{P_0}{E_1}, \qquad E_1 \in \{\text{next 4 quarters},\ \text{NTM},\ \text{next fiscal year}\}
$$
^f-05-04-1

- $P_0$: current price; trailing EPS is the sum of the most recent four quarters (TTM), computed as full prior year minus its first quarter plus the current first quarter when only one new quarter has been reported (V5 p.230).
- For rising earnings the forward P/E is below the trailing P/E because its denominator is larger, so the same definition must be applied to every stock in a comparison (V5 p.228).
- Use diluted EPS for comparisons; Siemens at EUR 95.94 has trailing P/E 13.47 on basic EPS 7.12 and 13.69 on diluted EPS 7.01 (V5 p.229).

**NTM EPS weighting** (V5 p.235)
$$
E_{\text{NTM}} = \frac{m}{12}\,E_{FY1} + \frac{12-m}{12}\,E_{FY2}
$$
^f-05-04-2

- $m$: months remaining in the current fiscal year FY1; $E_{FY1}$, $E_{FY2}$: annual EPS estimates for the current and following fiscal years.
- The weighting lets companies with different fiscal year ends be compared without quarterly estimates (V5 p.235).
- Microsoft in late August with 10 months left: $E_{\text{NTM}} = (10/12) E_{FY21} + (2/12) E_{FY22}$ (V5 p.235).

**Underlying (core) EPS** (V5 p.229, p.231, p.329)
$$
\text{Underlying EPS} = \text{Reported diluted EPS} - \text{Nonrecurring gains} + \text{Nonrecurring charges}
$$
^f-05-04-3

- Nonrecurring items include asset sale gains and losses, write-downs, goodwill impairment, provisions and changes in estimates, which often sit inside continuing operations (V5 p.231).
- A recurring item such as higher ongoing depreciation is not reversed, and company-reported core EPS is not accepted without examining the reconciliation (V5 p.230, p.329).
- Practice Problem 24: $0.81 - 0.04 + 0.03 = 0.80$ (V5 p.329).

**Normalized EPS, method of historical average EPS** (V5 p.231)
$$
\text{EPS}_{\text{norm}} = \frac{1}{n}\sum_{t=1}^{n} \text{EPS}_t \quad \text{over the most recent full cycle}
$$
^f-05-04-4

- Simple but ignores changes in the size of the business over the cycle (V5 p.231).
- Example 4: average of seven years of EPS is $0.79$, giving P/E $18.21/0.79 = 23.1$ (V5 p.232).

**Normalized EPS, method of average ROE** (V5 p.231, p.232)
$$
\text{EPS}_{\text{norm}} = \overline{ROE}_{\text{cycle}} \times \text{BVPS}_{\text{current}}
$$
^f-05-04-5

- Uses current book value per share, so it reflects growth or shrinkage in the equity base and is usually preferred; adjust BVPS if large write-downs distort it (V5 p.231, p.232).
- Variants multiply total assets by a long-run ROA or equity by a long-run ROE, useful when the latest year is a loss (V5 p.232).
- Example 4: $0.226 \times 4.82 = 1.09$, P/E $= 18.21/1.09 = 16.7$ (V5 p.233).

> [!tip] Calculator
> Average ROE method: enter the ROEs, e.g. `24.7 + 21.5 + 21.4 + 18.1 + 28.2 + 21.8 + 22.4 = ÷ 7 =` gives 22.6; then `× 4.82 =` gives 1.09; then `18.21 ÷ 1.09 =` gives 16.7.

**Earnings yield and the PVGO decomposition** (V5 p.234, p.250)
$$
\frac{E}{P} = \frac{1}{P/E}, \qquad P_0 = \frac{E_1}{r} + \text{PVGO} \;\Rightarrow\; r = \frac{E_1}{P_0}\ \text{when PVGO} = 0
$$
^f-05-04-6

- Price is never negative, so ranking by E/P from high to low ranks stocks from cheapest to most expensive even when some EPS are negative; report negative P/Es as NM (V5 p.234).
- Earnings yield is the expected return on a no-growth stock priced at value, which is why the Fed model's omission of growth is a flaw (V5 p.250).
- Tesla at 224.45 with EPS of $-7.72$ has E/P of $-2.51\%$, ranking last (V5 p.234).

**Justified forward P/E from the Gordon growth model** (V5 p.238)
$$
\frac{P_0}{E_1} = \frac{D_1/E_1}{r-g} = \frac{1-b}{r-g}
$$
^f-05-04-7

- $b$: retention rate, so $1-b$ is the payout ratio; $r$: required return on equity; $g$: sustainable dividend growth, often $b \times ROE$.
- Derivation: $P_0 = D_1/(r-g)$; divide both sides by $E_1$ and note $D_1 = (1-b)E_1$.
- Justified P/E rises with $g$ and payout and falls with $r$; Example 7 for BP: $(1-0.40)/(0.076-0.035) = 14.6$ (V5 p.239).

**Justified trailing P/E from the Gordon growth model** (V5 p.238)
$$
\frac{P_0}{E_0} = \frac{D_0(1+g)/E_0}{r-g} = \frac{(1-b)(1+g)}{r-g}
$$
^f-05-04-8

- Same variables; the extra $(1+g)$ converts the current-year payout into next year's dividend, so the trailing justified P/E always exceeds the forward one by the factor $(1+g)$.
- Practice Problem 30 for Sundanci: $(0.30 \times 1.13)/(0.14-0.13) = 33.9$ trailing versus $0.30/0.01 = 30$ forward (V5 p.330).

> [!tip] Calculator
> Forward: `1 - b = ÷ (r - g) =`; trailing: `(1 - b) × (1 + g) = ÷ (r - g) =`. For Sundanci: `0.30 × 1.13 = ÷ 0.01 =` gives 33.9.

**Justified multiple from any DCF or residual income value** (V5 p.225, p.239, p.278)
$$
\text{Justified multiple} = \frac{V_0^{\text{model}}}{\text{Forecast fundamental per share}}
$$
^f-05-04-9

- Used when no closed form exists: Toyota's FCFE value of JPY 6,980 over forecast EPS 720 gives a justified forward P/E of 9.7 against the market's 9.3 (V5 p.239, p.240).
- Same procedure yields justified P/CF, P/FCFE or P/B from the appropriate model value (V5 p.226, p.278).

**Predicted P/E from a cross-sectional regression** (V5 p.240)
$$
\widehat{P/E} = a_0 + a_1\,\text{DPR} + a_2\,\beta + a_3\,\text{EGR}
$$
^f-05-04-10

- DPR: dividend payout ratio; EGR: five-year earnings growth rate; coefficients are estimated on a sample of peers at one date.
- Example 9: $12.12 + 2.25(0.45) - 0.20(0.9) + 14.43(0.08) = 14.1$; an actual P/E of 18 above the prediction signals overvaluation (V5 p.240).
- Limitations: valid only for that sample and period, coefficients and explanatory power shift over time, multicollinearity blurs individual coefficients (V5 p.241).

**PEG ratio** (V5 p.246)
$$
\text{PEG} = \frac{P/E}{g\ (\text{in percentage points})}
$$
^f-05-04-11

- Use the forward P/E with the consensus five-year growth in percent, e.g. a P/E of 9.36 and growth of 1.83% gives $9.36/1.83 = 5.11$ (V5 p.246).
- Lower is cheaper, all else equal; PEG below 1 is sometimes called attractive, but the ratio assumes a linear P/E-growth link, ignores risk, and ignores growth duration (V5 p.246, p.247).

**Justified price from own historical P/E** (V5 p.252)
$$
\text{Justified price} = (\text{Benchmark own historical P/E}) \times (\text{Most recent EPS})
$$
^f-05-04-12

- Benchmarks include Value Line's rounded average of the four middle annual P/Es over 10 years or a five-year average trailing P/E; normalized EPS replaces recent EPS when it is negative (V5 p.252).
- Example 15 for Honda: $10.0 \times 381.93 = 3{,}819$ with the median, $9.7 \times 381.93 = 3{,}704$ with the mean (V5 p.252).

**Fed model** (V5 p.250)
$$
\text{Justified } \frac{P}{E}_{\text{market}} = \frac{1}{y_{10}}, \qquad \text{overvalued if } \frac{E_1}{P_0} < y_{10}
$$
^f-05-04-13

- $y_{10}$: yield on the 10-year Treasury; $E_1/P_0$: forward earnings yield on the index.
- At $y_{10} = 2.72\%$ the justified P/E is $1/0.0272 = 36.8$ against a trailing 18.9, illustrating the model's breakdown at low rates; it also ignores growth and the equity risk premium and mishandles inflation (V5 p.250, p.251).

**Yardeni model** (V5 p.251)
$$
\text{CEY} = \text{CBY} - b \times \text{LTEG} + \varepsilon \;\Rightarrow\; \frac{P}{E} = \frac{1}{\text{CBY} - b \times \text{LTEG}}
$$
^f-05-04-14

- CEY: current earnings yield on the index; CBY: Moody's A-rated corporate bond yield; LTEG: consensus five-year earnings growth; $b$: market's weight on growth, historically about 0.10, with 0.20 and 0.25 also reported (V5 p.251).
- Higher corporate yields lower the justified P/E and higher growth raises it; CBY carries a default premium but no equity risk premium, and five-year growth may not be sustainable (V5 p.251).

**Justified P/E with inflation and cost pass-through** (V5 p.253, p.254)
$$
\frac{P_0}{E_1} = \frac{1}{\rho + (1-\lambda)I}, \qquad \rho = r - I
$$
^f-05-04-15

- $I$: inflation; $\lambda$: fraction of cost inflation passed through to earnings; $\rho$: real required return.
- Derivation: with full payout and nominal growth $\lambda I$, $P_0 = E_1/(r - \lambda I)$ and $r - \lambda I = (r - I) + (1-\lambda)I = \rho + (1-\lambda)I$ (V5 p.254).
- $\lambda = 1$ gives $1/\rho$, immune to inflation; $\lambda = 0$ gives $1/r$; Example 16: $1/(0.03 + 0.25 \times 0.06) = 22.2$ (V5 p.254).

**Terminal value from a price multiple** (V5 p.255)
$$
V_n = (\text{Benchmark trailing P/E}) \times E_n \quad \text{or} \quad V_n = (\text{Benchmark forward P/E}) \times E_{n+1}
$$
^f-05-04-16

- $n$: the year the mature stage begins; the benchmark may be fundamentals-based (Gordon model divided by $E_n$ or $E_{n+1}$) or comparables-based (industry median or mean, own past average) (V5 p.255).
- Comparables are grounded in market data but import any benchmark mispricing; the Gordon model is very sensitive to $r$, payout and $g$ (V5 p.255, p.256).
- Example 17: $14.3 \times 3.00 = 42.90$ versus Gordon $1.35(1.0715)/(0.10-0.0715) = 50.76$ (V5 p.256).

**Book value per share** (V5 p.259, p.260)
$$
\text{BVPS} = \frac{\text{Total shareholders' equity} - \text{Preferred equity (and dividends in arrears)}}{\text{Common shares outstanding}}
$$
^f-05-04-17

- Tangible BVPS further subtracts goodwill and intangibles; fair value footnotes may adjust financial assets and liabilities; off-balance-sheet items and LIFO to FIFO restatements are other adjustments (V5 p.261, p.262, p.264).
- Example 19 for TD in 2018: $(80{,}040 - 5{,}000)/1{,}830.4 = 41.00$, so P/B $= 73.03/41.00 = 1.78$ (V5 p.261).

**Justified P/B from the Gordon growth model** (V5 p.265)
$$
\frac{P_0}{B_0} = \frac{ROE - g}{r - g}
$$
^f-05-04-18

- Derivation: $V_0 = E_1(1-b)/(r-g)$; set $E_1 = ROE \times B_0$ so $V_0/B_0 = ROE(1-b)/(r-g)$; substitute $b = g/ROE$ so $ROE(1-b) = ROE - g$ (V5 p.265).
- What matters is ROE relative to r; with $g = 0$ it is $ROE/r$; two stocks with the same P/B and different ROE make the higher-ROE one relatively undervalued (V5 p.265).
- Example: $(0.12-0.07)/(0.10-0.07) = 1.67$; Practice Problem 39: $(0.20-0.08)/(0.115-0.08) = 3.4$ (V5 p.265, p.332).

**Justified P/B from residual income** (V5 p.265, p.266)
$$
\frac{P_0}{B_0} = 1 + \frac{PV(\text{expected future residual earnings})}{B_0} = 1 + \frac{ROE - r}{r - g}
$$
^f-05-04-19

- The second form assumes a level residual income $(ROE - r)B_0$ growing at $g$: rewrite $ROE - g = (r-g) + (ROE - r)$ and divide by $r-g$ (V5 p.266).
- P/B is 1 when the firm just earns its cost of equity, above 1 when residual income is positive, below 1 when negative (V5 p.265).

**P/S and its link to P/E** (V5 p.268)
$$
\frac{P}{S} = \frac{P_0}{\text{Net sales per share}}, \qquad \frac{P}{S} = \frac{P}{E} \times \text{Net profit margin}
$$
^f-05-04-20

- Net sales are total sales less returns and discounts, usually the last fiscal year; because Sales $\times$ Margin $=$ Net income, two stocks with the same P/E differ in P/S by their margins (V5 p.268).
- Example 22: $10{,}486/788.6 = 13.30$ per share and $10.34/13.30 = 0.778$ (V5 p.269).

**Justified P/S from the Gordon growth model** (V5 p.269, p.272)
$$
\frac{P_0}{S_1} = \frac{(E_1/S_1)(1-b)}{r-g}, \qquad \frac{P_0}{S_0} = \frac{(E_0/S_0)(1-b)(1+g)}{r-g}
$$
^f-05-04-21

- $E/S$: net profit margin, forward or trailing; derivation: $P_0 = D_1/(r-g)$ with $D_1 = E_1(1-b)$, then divide both sides by $S_1$ (V5 p.269).
- Justified P/S rises with margin, payout and growth and falls with r; Example 26: $0.09 \times 0.35/(0.09-0.07) = 1.575$ (V5 p.273).

**Sustainable growth through DuPont** (V5 p.272)
$$
g = b \times PM_0 \times \frac{\text{Sales}}{\text{Total assets}} \times \frac{\text{Total assets}}{\text{Shareholders' equity}}
$$
^f-05-04-22

- Profit margin drives justified P/S directly and again through $g$, as long as sales do not fall proportionately when margin rises (V5 p.272).

**Cash flow per share, earnings-plus-noncash-charges definition** (V5 p.277)
$$
\text{CF} = \text{EPS} + \text{Per-share depreciation, amortization and depletion}, \qquad \frac{P}{CF} = \frac{P_0}{CF}
$$
^f-05-04-23

- "P/CF" is reserved for this definition; "price to cash flow" covers CFO, FCFE and EBITDA variants as well (V5 p.275).
- Ignores noncash revenue and working capital changes, so aggressive revenue recognition slips through (V5 p.275).
- Example 29 for Philips: $1.41 + 1.17 = 2.58$ and $36.31/2.58 = 14.1$ (V5 p.277).

**EBITDA and the alternative enterprise value denominators** (V5 p.278, p.287, p.289)
$$
\text{EBITDA} = NI + \text{Interest} + \text{Taxes} + D + A, \quad \text{EBITA} = NI + I + T + A, \quad \text{EBIT} = NI + I + T
$$
^f-05-04-24

- Start from net income from continuing operations excluding nonrecurring items; forecasts usually take EBIT and add D and A (V5 p.278, p.289).
- FCFF $= NI + \text{Interest}(1-t) + D + A - \text{WCInv} - \text{FCInv}$ is the theoretically preferred firm flow because it reflects capital expenditure (V5 p.289).
- Example 34: $2{,}400 + 143 + 906 + 511 = 3{,}960$ (V5 p.287).

**Justified price to cash flow from an FCFE model** (V5 p.278)
$$
V_0 = \frac{\text{FCFE}_0(1+g)}{r-g}, \qquad \text{Justified } \frac{P}{CF} = \frac{V_0}{CF_0}, \qquad \text{Justified } \frac{P}{FCFE} = \frac{V_0}{FCFE_0}
$$
^f-05-04-25

- Justified price to cash flow is inversely related to r and positively related to growth, however cash flow is defined (V5 p.278).
- Example 30 for Colgate: $V_0 = 1.032 \times 2.66/(0.074-0.032) = 65.36$, so P/CF $= 65.36/3.26 = 20.05$ and P/FCFE $= 65.36/2.66 = 24.57$ (V5 p.279).

**Trailing and leading dividend yield** (V5 p.281)
$$
\frac{D}{P}_{\text{trailing}} = \frac{\text{Dividend rate}}{P_0} = \frac{4 \times \text{Latest quarterly DPS}}{P_0}, \qquad \frac{D}{P}_{\text{leading}} = \frac{\text{Forecast DPS next 12 months}}{P_0}
$$
^f-05-04-26

- For uneven semiannual payers the dividend rate is the most recent annual total; for non-payers D/P is zero while P/D is undefined (V5 p.281).
- Example 32: BCE $0.58 \times 4 = 2.32$, $2.32/39.53 = 5.87\%$; BT ADR $0.976/15.20 = 6.42\%$ (V5 p.281, p.282).

**Justified dividend yield from the Gordon growth model** (V5 p.282)
$$
\frac{D_0}{P_0} = \frac{r-g}{1+g}
$$
^f-05-04-27

- Derivation: $P_0 = D_0(1+g)/(r-g)$, invert and multiply both sides by $D_0$.
- Yield falls with growth and rises with r, so high-yield selection is a value orientation; dividend safety is judged by payout, interest coverage and net debt to EBITDA (V5 p.282).

**Enterprise value and total invested capital** (V5 p.284, p.285, p.287)
$$
EV = MV_{\text{common}} + MV_{\text{preferred}} + \text{Minority interest} + MV_{\text{debt}} - \text{Cash and short-term investments}, \qquad TIC = EV + \text{Cash and investments}
$$
^f-05-04-28

- Cash is deducted because an acquirer gains access to it after buying out equity and debt holders; use market values of debt, or book or matrix prices when debt does not trade (V5 p.285).
- Example 34 for Colgate: $57{,}372 + 8{,}623 + 299 - 726 = 65{,}568$; Practice Problem 28: $1{,}733 + 6{,}766 + 275 - 581 - 495 = 7{,}698$ (V5 p.287, p.330).

> [!tip] Calculator
> Build EV left to right: `shares × price = + debt = + preferred = + minority interest = - cash = - short-term investments =`, then `÷ EBITDA =`. Gesticular: `1733 + 6766 + 275 - 581 - 495 = ÷ 560 =` gives 13.75.

**EV/EBITDA and EV/S** (V5 p.284, p.290)
$$
\frac{EV}{\text{EBITDA}} = \frac{EV}{NI + I + T + D + A}, \qquad \frac{EV}{S} = \frac{EV}{\text{Net sales}}
$$
^f-05-04-29

- Both numerator and denominator are firm-level totals, never per share; EV/EBITDA is preferred to P/EBITDA because EBITDA is a pre-interest flow to all capital providers (V5 p.278, p.333).
- Justified EV/EBITDA rises with FCFF growth and ROIC (after-tax operating profit over invested capital) and falls with WACC (V5 p.287).
- Example 36: $EV = 8{,}154 + 2{,}970 - 1{,}130 = 9{,}994$ and $EV/S = 9{,}994/10{,}486 = 0.953$ (V5 p.290).

**Unexpected earnings, percentage surprise and scaled earnings surprise** (V5 p.294)
$$
UE_t = EPS_t - E(EPS_t), \qquad \%\text{Surprise} = \frac{UE_t}{E(EPS_t)}, \qquad \text{Scaled surprise} = \frac{UE_t}{\sigma(\text{analysts' forecasts})}
$$
^f-05-04-30

- Scaling by the dispersion of analysts' forecasts says a given miss is more meaningful when analysts agreed (V5 p.294).
- Example 37 for BP: $(3.74 - 3.26)/0.29 = 1.66$ (V5 p.294).

**Standardized unexpected earnings (SUE)** (V5 p.294)
$$
SUE_t = \frac{EPS_t - E(EPS_t)}{\sigma\left[EPS_t - E(EPS_t)\right]_{\text{historical}}}
$$
^f-05-04-31

- The denominator is the standard deviation of past surprises over a prior window such as 20 quarters, not the dispersion of current analyst forecasts (V5 p.294, p.330).
- A $0.05$ surprise with past surprise dispersion $0.20$ gives SUE $0.25$; with dispersion $0.07$ it gives $0.71$ (V5 p.295).

**Relative strength indicator** (V5 p.296, p.297)
$$
RSTR_t = \frac{P^{\text{stock}}_t / P^{\text{index}}_t}{P^{\text{stock}}_0 / P^{\text{index}}_0}
$$
^f-05-04-32

- Scaled to 1.0 at the start; above 1 means the stock outperformed the index since then, and the one-period relative performance is the ratio of consecutive RSTR values (V5 p.296, p.298).
- The other type of relative strength is the stock's own compound return over six or twelve months, called price momentum (V5 p.296).
- Example 39: TLT $(144.04/2{,}923.65)/(121.90/2{,}640.87) = 1.067$, a 6.7% outperformance (V5 p.297, p.298).

**Harmonic mean and weighted harmonic mean of multiples** (V5 p.299)
$$
X_H = \frac{n}{\sum_{i=1}^{n} (1/X_i)}, \qquad X_{WH} = \frac{1}{\sum_{i=1}^{n} (w_i / X_i)}
$$
^f-05-04-33

- $w_i$: portfolio value weights summing to 1, $X_i > 0$; the weighted harmonic mean equals the aggregate portfolio multiple (total market cap over total earnings), which is why index vendors use it (V5 p.299, p.300).
- The harmonic mean is below the arithmetic mean unless all values are equal, dampens large outliers, but can aggravate small outliers near zero (V5 p.300).
- Practice Problem 21: $5/(1/5.9 + 1/8.3 + 1/3.0 + 1/15.0 + 1/4.6) = 5.5$ (V5 p.328).

> [!tip] Calculator
> Harmonic mean: `5.9 1/x + 8.3 1/x + 3 1/x + 15 1/x + 4.6 1/x = 1/x × 5 =` gives 5.51. The `1/x` key is the whole trick.

**CAPM required return for justified multiples** (V5 p.332)
$$
r = r_f + \beta \times \text{ERP}
$$
^f-05-04-34

- Practice Problem 38: $4.9\% + 1.2 \times 5.5\% = 11.5\%$, then fed into Formulas 8, 18 and 21 (V5 p.332).

## Worked examples

### Example 1: The method of comparables at its simplest (V5 p.224)

Setup: Company A has EPS of 1.50; its close competitor B trades at a P/E of 22 and the two have similar operating and financial profiles.

Part 1: at a price of 37.50, A's P/E is $37.50/1.50 = 25$, above B's 22, so A is overvalued relative to B if the companies are truly similar.
Part 2: if A should trade at B's multiple, its appropriate price is $1.50 \times 22 = 33$.
Both directions (compare multiples, or apply the benchmark to EPS) give the same verdict.
Python check: `37.5/1.5 = 25.0`, `1.5*22 = 33.0`. ^ex-05-04-1

### Example 2: Basic versus diluted EPS (V5 p.229)

Setup: Siemens reported basic EPS of EUR 7.12 and diluted EPS of EUR 7.01 for fiscal 2018; price EUR 95.94.

Trailing P/E on basic EPS: $95.94/7.12 = 13.47$; on diluted EPS: $95.94/7.01 = 13.69$.
Diluted EPS is smaller, so the P/E is higher; analysts prefer diluted EPS so companies with different amounts of dilutive securities are comparable.
Python check: `95.94/7.12 = 13.47`, `95.94/7.01 = 13.69`. ^ex-05-04-2

### Example 3: Trailing 12-month EPS and nonrecurring adjustments, Evergreen (V5 p.229, p.230)

Setup: price GBP 50.11 at 31 May 20X9; Q1 20X9 reported diluted EPS 0.81 including 0.34 restructuring and 0.26 acquisition amortization; company core EPS 1.41.
Full-year 20X8 reported 4.98 (Q1 20X8 1.27), core 6.41 (Q1 1.81), EPS excluding 20X8 legal provisions 5.07 (Q1 1.28).
TTM EPS = full year minus its Q1 plus current Q1.

Reported: $4.98 - 1.27 = 3.71$, plus $0.81$ gives $4.52$; P/E $= 50.11/4.52 = 11.1$.
Company core: $6.41 - 1.81 = 4.60$, plus $1.41$ gives $6.01$; P/E $= 50.11/6.01 = 8.3$.
Analyst's own adjustment (only the legal provision is nonrecurring, since restructuring recurs and amortization will continue): $5.07 - 1.28 = 3.79$, plus $0.81$ gives $4.60$; P/E $= 50.11/4.60 = 10.9$.
Lesson: core earnings are a non-IFRS concept with no rules, and the analyst's underlying EPS can sit well away from the company's (V5 p.230).
Python check: `50.11/4.52 = 11.09`, `50.11/6.01 = 8.34`, `50.11/4.60 = 10.89`. ^ex-05-04-3

### Example 4: Normalizing EPS for business-cycle effects, Zenlandia Chemical (V5 p.232, p.233)

Setup: ADR price 18.21 on 5 July 2021; 2014 to 2020 EPS 0.74, 0.63, 0.61, 0.54, 1.07, 0.88, 1.08; BVPS 3.00 rising to 4.82; ROE 24.7%, 21.5%, 21.4%, 18.1%, 28.2%, 21.8%, 22.4%.

Part 1, historical average EPS (Formula 4): sum $= 5.55$, divided by 7 gives $0.79$; P/E $= 18.21/0.79 = 23.1$.
Part 2, average ROE (Formula 5): sum of ROEs $= 158.1\%$, divided by 7 gives $22.6\%$; normalized EPS $= 0.226 \times 4.82 = 1.09$; P/E $= 18.21/1.09 = 16.7$.
Part 3: BVPS rose from 3.00 to 4.82, about 61%, and the average ROE method captures that larger equity base, so it gives a higher normalized EPS and a lower, more conservative-looking P/E.
Note the ROEs are computed on ending BVPS, so essentially trailing earnings are being normalized; consistency of the ROE definition across companies is required (V5 p.232).
Python check: `mean(eps) = 0.7929`, `18.21/0.79 = 23.05`, `mean(roe) = 22.59`, `0.226*4.82 = 1.089`, `18.21/1.09 = 16.71`. ^ex-05-04-4

### Example 5: Forward P/E on fiscal-year consensus, IBM (V5 p.236)

Setup: price 137.90 in late June 2019; consensus EPS 13.91 for FY1 (2019) and 14.17 for FY2 (2020).

FY1 forward P/E $= 137.90/13.91 = 9.9$; this FY1 figure blends one reported quarter with three forecast quarters.
FY2 forward P/E $= 137.90/14.17 = 9.7$.
Growth from FY1 to FY2 is under 2%, so the two definitions barely differ.
Python check: `137.90/13.91 = 9.91`, `137.90/14.17 = 9.73`, `14.17/13.91-1 = 0.0187`. ^ex-05-04-5

### Example 6: Forward P/E with volatile earnings, Selene Gaming (V5 p.236, p.237)

Setup: price 12.20 on 9 August 2020; quarterly EPS 2020: 0.10 (Mar), 0.00 (Jun), E(-0.10) (Sep), E(-0.50) (Dec); 2021 estimates 0.70, 0.80, 0.30, -0.30; annual estimates -0.50 for 2020 and 1.50 for 2021.

Part 1, next four quarters: $-0.10 - 0.50 + 0.70 + 0.80 = 0.90$; P/E $= 12.20/0.90 = 13.6$.
Part 2, NTM (Formula 2) with five months left in FY2020: $(5/12)(-0.50) + (7/12)(1.50) = -0.2083 + 0.875 = 0.667$; P/E $= 12.20/0.667 = 18.3$.
The curriculum rounds the NTM EPS to 0.67 and reports 18.2; the unrounded figure is 18.3, and either is acceptable given the rounding.
Part 3, current fiscal year: $0.10 + 0.00 - 0.10 - 0.50 = -0.50$; P/E $= 12.20/(-0.50) = -24.4$, not meaningful.
Part 4, next fiscal year: $0.70 + 0.80 + 0.30 - 0.30 = 1.50$; P/E $= 12.20/1.50 = 8.1$.
Four definitions give 13.6, 18.3, NM and 8.1, which is the argument for normalizing a procyclical earner.
Python check: `12.20/0.9 = 13.56`, `5/12*-0.5+7/12*1.5 = 0.6667`, `12.20/0.6667 = 18.30`, `12.20/0.67 = 18.21`, `12.20/1.5 = 8.13`. ^ex-05-04-6

### Example 7: Justified forward P/E from fundamentals, BP (V5 p.239)

Setup: retention $b = 40\%$, long-term growth 3.5%, required return 7.6% reflecting legal uncertainty.

Formula 7: $(1 - 0.40)/(0.076 - 0.035) = 0.60/0.041 = 14.6$.
Python check: `0.6/0.041 = 14.63`. ^ex-05-04-7

### Example 8: Justified P/E from an FCFE model, Toyota (V5 p.239, p.240)

Setup: price JPY 6,688; FCFE model value 6,980; forecast FY2020 EPS 720.

Part 1 (Formula 9): justified forward P/E $= 6{,}980/720 = 9.7$.
Part 2: market forward P/E $= 6{,}688/720 = 9.3$; the justified multiple is about 4% above the market multiple, the same 4% by which value exceeds price ($6{,}980/6{,}688 - 1 = 4.4\%$).
Python check: `6980/720 = 9.69`, `6688/720 = 9.29`, `6980/6688-1 = 0.0437`. ^ex-05-04-8

### Example 9: Predicted P/E from a cross-sectional regression (V5 p.240)

Setup: food company with beta 0.9, payout 0.45, earnings growth 0.08; regression $\widehat{P/E} = 12.12 + 2.25\,DPR - 0.20\,\beta + 14.43\,EGR$.

Part 1 (Formula 10): $12.12 + 2.25(0.45) - 0.20(0.9) + 14.43(0.08) = 12.12 + 1.0125 - 0.18 + 1.1544 = 14.1$.
Part 2: actual trailing P/E of 18 exceeds the predicted 14.1, so the stock sells at a higher multiple than fundamentals justify and appears overvalued.
Python check: `12.12+2.25*0.45-0.20*0.9+14.43*0.08 = 14.107`. ^ex-05-04-9

### Example 10: A simple peer-group comparison, Verizon (V5 p.244, p.245)

Setup: trailing P/Es: AT&T 13.20, Comcast 16.23, CenturyLink NMF (negative EPS), China Telecom 13.14, Charter 70.67, Verizon 15.03, Windstream 19.01; mean of the six meaningful values 24.55, median 15.03.

Part 1: CenturyLink and Charter are outliers, so the median 15.03 is the appropriate benchmark rather than the mean 24.55; with seven names the median is the middle ranked value (an even count would average the two middle values).
Part 2: Verizon's P/E equals the median, so with no fundamental differences it is fairly valued.
Part 3: AT&T, China Telecom and CenturyLink sit below the median and look undervalued; Charter, Comcast and Windstream look overvalued; follow-up analysis should look at cash flow, because telecoms carry large noncash charges that make earnings volatile and far below cash flow.
Python check: `mean([13.20,16.23,13.14,70.67,15.03,19.01]) = 24.55`, `sorted = [13.14, 13.2, 15.03, 16.23, 19.01, 70.67]`, so the seven-name median including CenturyLink's NMF at the bottom is 15.03. ^ex-05-04-10

### Example 11: Peer-group comparison modified by fundamentals (V5 p.246, p.247)

Setup: forward P/Es, five-year growth and betas: AT&T 9.36, 1.83%, 0.56; Comcast 12.92, 11.29%, 1.09; CenturyLink 8.89, 8.52%, 0.81; China Telecom 10.31, 6.90%, 0.81; Charter 30.32, 45.30%, 1.24; Verizon 11.99, 2.51%, 0.50; Windstream 16.29, 3.19%, 0.45; median forward P/E 11.99.

Part 1: PEG (Formula 11) $= $ forward P/E over growth in percent: AT&T $9.36/1.83 = 5.11$, Comcast $12.92/11.29 = 1.14$, CenturyLink $8.89/8.52 = 1.04$, China Telecom $10.31/6.90 = 1.49$, Charter $30.32/45.30 = 0.67$, Verizon $11.99/2.51 = 4.78$, Windstream $16.29/3.19 = 5.11$.
Among the three low-P/E names, CenturyLink has the highest growth and lowest PEG, so it is the most attractive; the high-growth names Comcast and Charter also carry the highest betas, consistent with growth stocks being riskier; PEG should be compared with industry and market PEGs rather than against an absolute 1.0.
Part 2: adjusting the median 11.99 up to 13.00 for AT&T's superior profitability and low risk, intrinsic value $= 3.63 \times 13.0 = 47.19$.
Part 3: 47.19 exceeds the market price 33.98, so AT&T appears undervalued on an absolute basis (the peer median is assumed fairly priced); a cleaner statement is that AT&T deserves a premium to 11.99 yet trades at 9.36 (V5 p.248).
Python check: `9.36/1.83 = 5.11`, `30.32/45.30 = 0.67`, `3.63*13 = 47.19`. ^ex-05-04-11

### Example 12: Valuation relative to the market (V5 p.248, p.249)

Setup: S&P 500 P/E 21.8; Stock A P/E 15.2 with a five-year average relative P/E of 80% of the index; Stock B 30.0 and 120%; Stock C 15.2 and 105%; equal growth and risk.

Part 1: historical relative P/Es imply A normally trades at $0.8 \times 21.8 = 17.4$, B at $1.2 \times 21.8 = 26.2$, C at $1.05 \times 21.8 = 22.9$.
A at 15.2 is a bit below its usual 17.4; C at 15.2 is far below its usual premium level, so C appears the most undervalued; B at 30.0 is above even its customary 26.2.
Part 2: the method assumes the historical relationship is stable, that is, the past is relevant to the future.
Python check: `0.8*21.8 = 17.44`, `1.2*21.8 = 26.16`, `1.05*21.8 = 22.89`. ^ex-05-04-12

### Example 13: The Fed model (V5 p.250)

Setup: 10-year Treasury yield 2.72% on 28 December 2018; trailing S&P 500 P/E 18.9.

Formula 13: justified P/E $= 1/0.0272 = 36.8$, roughly twice the actual 18.9, which by the model's logic makes stocks cheap.
The absurd size of the number at low rates is the point: the model ignores growth and the equity risk premium, and the yield-to-P/E link is nonlinear, so small rate changes swing the justified P/E enormously (V5 p.251).
Python check: `1/0.0272 = 36.76`. ^ex-05-04-13

### Example 14: The Yardeni model (V5 p.251)

Setup: $CEY = CBY - b \times LTEG + \text{residual}$ with $b$ historically about 0.10 and reported at 0.10, 0.20 and 0.25.

Inverting (Formula 14): $P/E = 1/(CBY - b \times LTEG)$.
Illustration with numbers of our own (not in the curriculum): CBY of 5% and LTEG of 8% with $b = 0.10$ give $1/(0.05 - 0.008) = 23.8$; raising CBY to 6% gives $1/0.052 = 19.2$, so higher corporate yields lower the justified P/E and higher growth raises it.
CBY includes a default premium but not an equity risk premium, and five-year growth may exceed the sustainable rate the Gordon model needs.
Python check: `1/(0.05-0.10*0.08) = 23.81`, `1/(0.06-0.008) = 19.23`. ^ex-05-04-14

### Example 15: Valuation relative to own historical P/Es, Honda (V5 p.252)

Setup: annual average P/Es 2014 to 2018: 9.7, 10.8, 10.9, 10.0, 6.9; mean 9.7, median 10.0; forecast FY2019 EPS JPY 381.93; recent price stated as JPY 2,837.

Part 1: benchmark 10.0 (median) or 9.7 (mean).
Part 2 (Formula 12): $10.0 \times 381.93 = 3{,}819$ and $9.7 \times 381.93 = 3{,}705$.
Part 3: the curriculum computes $2{,}817/3{,}819 - 1 = -26.2\%$ and $2{,}817/3{,}704 - 1 = -23.9\%$ using 2,817, which conflicts with the stated 2,837; with 2,837 the discounts are 25.7% and 23.4%.
Either way the stock trades roughly a quarter below its history-justified price and may be significantly undervalued, subject to the caveat that business mix, leverage and inflation may have changed (V5 p.253).
Python check: `mean([6.9,10,10.9,10.8,9.7]) = 9.66`, `10*381.93 = 3819.3`, `9.7*381.93 = 3704.7`, `2837/3819.3-1 = -0.257`, `2817/3819-1 = -0.262`. ^ex-05-04-15

### Example 16: P/Es and inflation pass-through (V5 p.253, p.254, p.255)

Setup: real required return $\rho = 3\%$ for both companies; Formula 15.

Part 1, both pass through 75%, inflation 6% for M and 2% for P: M $= 1/(0.03 + 0.25 \times 0.06) = 1/0.045 = 22.2$; P $= 1/(0.03 + 0.25 \times 0.02) = 1/0.035 = 28.6$.
With less than full pass-through, justified P/E falls as inflation rises.
Part 2, both face 6% inflation, M passes through 90% and P 70%: M $= 1/(0.03 + 0.10 \times 0.06) = 1/0.036 = 27.8$; P $= 1/(0.03 + 0.30 \times 0.06) = 1/0.048 = 20.8$.
At equal inflation the higher pass-through company earns the higher P/E, and the penalty for weak pass-through grows with inflation.
Python check: `1/0.045 = 22.22`, `1/0.035 = 28.57`, `1/0.036 = 27.78`, `1/0.048 = 20.83`. ^ex-05-04-16

### Example 17: Terminal value from P/E versus the Gordon growth model (V5 p.256)

Setup: $r = 0.10$; mature payout 0.45; industry ROE 0.13; $E_3 = 3.00$; industry P/E 14.3.

Part 1 (Formula 16): $V_3 = 14.3 \times 3.00 = 42.90$.
Part 2: $D_3 = 3.00 \times 0.45 = 1.35$; $g = b \times ROE = 0.55 \times 0.13 = 0.0715$; $V_3 = 1.35 \times 1.0715/(0.10 - 0.0715) = 1.4465/0.0285 = 50.76$.
The Gordon estimate is $50.76/42.90 - 1 = 18.3\%$ higher; the comparables figure is market-grounded but inherits any industry mispricing, while the Gordon figure is hypersensitive to r, payout and g.
Python check: `0.55*0.13 = 0.0715`, `1.35*1.0715/0.0285 = 50.76`, `50.76/42.9-1 = 0.1831`. ^ex-05-04-17

### Example 18: Business models reflected in P/Bs, US banks (V5 p.259)

Setup: P/Bs at end-2018: Citigroup 0.69, Wells Fargo 1.21, US Bancorp 1.63.

No arithmetic; the dispersion is explained by business model, not mispricing: Citigroup's one-stop-shop model and crisis losses, Wells Fargo's domestic loan and fee focus, US Bancorp's low-risk consumer and payments franchise plus acquisition-driven growth.
Lesson for LOS c: P/B misleads when asset intensity and business models differ across the comps (V5 p.258). ^ex-05-04-18

### Example 19: Computing book value per share, TD Bank (V5 p.260, p.261)

Setup (CAD millions): total equity 80,040 (2018), 75,190 (2017), 74,214 (2016); preferred shares 5,000, 4,750, 4,400; common shares outstanding 1,830.4, 1,842.5, 1,857.6 million; price 73.03 at 31 October 2018.

Part 1 (Formula 17): 2018 $(80{,}040 - 5{,}000)/1{,}830.4 = 75{,}040/1{,}830.4 = 41.00$; 2017 $(75{,}190 - 4{,}750)/1{,}842.5 = 38.23$; 2016 $(74{,}214 - 4{,}400)/1{,}857.6 = 37.58$.
The non-controlling interest is already inside total equity as presented and the curriculum deducts only preferred; the divisor is common shares outstanding, net of treasury shares.
Part 2: P/B $= 73.03/41.00 = 1.78$.
Python check: `75040/1830.4 = 41.00`, `70440/1842.5 = 38.23`, `69814/1857.6 = 37.58`, `73.03/41 = 1.78`. ^ex-05-04-19

### Example 20: Adjusting book value, Barclays (V5 p.262, p.263, p.264)

Setup (GBP millions): total shareholders' equity 62,957; goodwill and intangibles 7,915; financial assets carrying 643,174 versus fair value 625,841; financial liabilities carrying 823,658 versus fair value 823,259; 12,614 million diluted shares; price 2.4239.

Reported BVPS $= 62{,}957/12{,}614 = 4.9910$; P/B $= 2.4239/4.9910 = 0.49$.
Tangible BVPS $= (62{,}957 - 7{,}915)/12{,}614 = 4.3636$; P/B $= 0.56$.
Fair value gaps: assets are worth $643{,}174 - 625{,}841 = 17{,}333$ less than carrying value; liabilities are worth $823{,}658 - 823{,}259 = 399$ less, which raises equity.
Adjusted BVPS $= (62{,}957 - 7{,}915 - 17{,}333 + 399)/12{,}614 = 38{,}108/12{,}614 = 3.0211$; P/B $= 2.4239/3.0211 = 0.80$.
The spread from 0.49 to 0.80 is why the analyst questions management about model-based fair values and rate sensitivity.
Python check: `62957/12614 = 4.991`, `2.4239/4.991 = 0.486`, `55042/12614 = 4.3636`, `38108/12614 = 3.0211`, `2.4239/3.0211 = 0.802`. ^ex-05-04-20

### Example 21: P/B comparables, brokerage firms (V5 p.266, p.267)

Setup: P/B at 19 July 2013 and eight-year means: ETFC 0.65 (mean 1.14), SCHW 2.31 (mean 3.81), AMTD 2.53 (mean 3.45); forecast book value growth 1.5%, 10.5%, 9.0%; revenue growth -1.0%, 5.0%, 3.5%; betas 1.65, 1.20, 1.10.

ETFC's P/B is $0.65/2.31 = 28\%$ of SCHW's and $0.65/2.53 = 26\%$ of AMTD's, and $0.65/1.14 = 57\%$ of its own average.
The discount is explained by fundamentals: lower book value and revenue growth and a higher beta; whether it is undervalued depends on whether the analyst's growth forecast and its uncertainty differ from the consensus.
Python check: `0.65/2.31 = 0.281`, `0.65/2.53 = 0.257`, `0.65/1.14 = 0.570`. ^ex-05-04-21

### Example 22: Calculating P/S, Stora Enso (V5 p.269)

Setup: net sales EUR 10,486 million; shares 788.6 million (the problem statement says 788.4 but the solution uses 788.6); price 10.34.

Sales per share $= 10{,}486/788.6 = 13.30$; P/S $= 10.34/13.30 = 0.778$.
With 788.4 million shares the answer is 13.30 and 0.778 as well after rounding.
Python check: `10486/788.6 = 13.297`, `10.34/13.297 = 0.7776`. ^ex-05-04-22

### Example 23: Revenue recognition practices (1), advertising barter (V5 p.269, p.270)

Setup: during the 1998 to 2000 internet bubble two companies barter 1,000,000 of banner advertising with each other.

Each books 1,000,000 of revenue and 1,000,000 of expense: net income and cash flow are zero, but revenue growth and any P/S-based valuation are inflated, and the value placed on the advertising is questionable.
Regulators responded with SAB 101 and SIC 31; the analyst reviews footnotes for premature or aggressive revenue recognition before trusting P/S. ^ex-05-04-23

### Example 24: Revenue recognition practices (2), Diebold bill-and-hold (V5 p.270, p.271)

Setup: Diebold recognized bill-and-hold sales before delivery and restated; in 2010 it paid 25 million to settle SEC charges of manipulating earnings from 2002 to 2007, misstating pre-tax earnings by at least 127 million.

Bill-and-hold accelerates revenue into an earlier period; management compared actual earnings with analyst forecasts daily and kept "opportunity lists" of ways to close the gap.
Lesson: sales are harder to manipulate than earnings but not immune, so P/S needs a revenue-quality check. ^ex-05-04-24

### Example 25: Revenue recognition practices (3), Groupon (V5 p.271)

Setup: before its 2011 IPO Groupon restated revenue to net of merchant share, cutting sales by more than 50%, and dropped an invented non-GAAP metric that ignored marketing expense.

Gross versus net booking can double reported sales with no change in economics.
When the manipulated amount is unknown the analyst may avoid the stock or at least raise the risk premium, which lowers the justified P/S (V5 p.271). ^ex-05-04-25

### Example 26: Justified P/S based on forecasted fundamentals, Getinge (V5 p.272, p.273)

Setup: $r = 9\%$; long-term forecasts: profit margin 9.0%, payout 35%, growth 7%; forecast 2019 sales per share SEK 94.3; price 133.70.

Part 1 (Formula 21): $P/S = 0.09 \times 0.35/(0.09 - 0.07) = 0.0315/0.02 = 1.575$.
Part 2: intrinsic value $= 1.575 \times 94.3 = 148.52$.
Part 3: price 133.70 is below 148.52, so the stock appears undervalued by about 10%.
Python check: `0.09*0.35/0.02 = 1.575`, `1.575*94.3 = 148.52`, `133.70/148.52-1 = -0.0998`. ^ex-05-04-26

### Example 27: P/S comparables, Getinge versus CMD and NEO (V5 p.274)

Setup: P/S (TTM) GETI 1.54, CMD 3.96, NEO 8.79; margins -2.49%, 6.95%, 14.53%; revenue growth 9.50%, 5.20%, 1.50%; debt to equity 58.43, 35.58, 28.50; EV/Revenue 1.88, 4.14, 8.23.

Part 1: on P/S alone GETI is the lowest and looks relatively undervalued.
Part 2: GETI is closer to CMD than to NEO; NEO's much higher P/S reflects its high margin, while GETI's higher leverage and low EV/Revenue sit near CMD's; GETI's low P/S is consistent with its negative margin, so the discount is at least partly justified. ^ex-05-04-27

### Example 28: Accounting methods and cash flow (V5 p.276, p.277)

Setup: Companies A and B have identical cash revenues, cash expenses, share counts and total depreciation of 15.00 per share over 2018 to 2020; A uses straight-line (5.00 per year), B accelerated (7.50, 5.00, 2.50).

A's EPS is flat at 10.00 with cash flow 15.00 each year.
B's EPS is 7.50, 10.00, 12.50, a compound growth of $(12.50/7.50)^{1/2} - 1 = 29\%$ per year, with cash flow again 15.00 each year.
B appears to have earnings momentum that is pure depreciation policy; cash flow per share exposes the identity of the two firms.
Python check: `(12.5/7.5)**0.5-1 = 0.291`. ^ex-05-04-28

### Example 29: P/CF with cash flow as earnings plus noncash charges, Philips (V5 p.277)

Setup: 2018 net income from continuing operations EUR 1,310 million, EPS 1.41; depreciation and amortization 1,089 million, 1.17 per share; price 36.31.

Formula 23: CF $= 1.41 + 1.17 = 2.58$; P/CF $= 36.31/2.58 = 14.1$.
Python check: `36.31/2.58 = 14.07`. ^ex-05-04-29

### Example 30: Justified price to cash flow, Colgate-Palmolive (V5 p.278, p.279)

Setup: trailing FCFE 2.66 per share; trailing CF 3.26; $r = 7.4\%$; FCFE growth 3.2%.

Part 1 (Formula 25): $V_0 = 2.66 \times 1.032/(0.074 - 0.032) = 2.7451/0.042 = 65.36$.
Part 2: justified P/CF $= 65.36/3.26 = 20.05$.
Part 3: justified P/FCFE $= 65.36/2.66 = 24.57$.
Python check: `2.66*1.032/0.042 = 65.36`, `65.36/3.26 = 20.05`, `65.36/2.66 = 24.57`. ^ex-05-04-30

### Example 31: Price to cash flow and comparables (V5 p.279)

Setup: Company A price 17.98, CF 1.84, P/CF 9.8, FCFE 0.29, P/FCFE 62, five-year CF growth 13.4%, beta 1.50; Company B price 15.65, CF 1.37, P/CF 11.4, FCFE -0.99, P/FCFE NMF, growth 10.6%, beta 1.50.

A's P/CF is $9.8/11.4 - 1 = 14\%$ below B's, which would normally imply lower expected growth, yet A's growth forecast is 280 basis points higher at equal risk.
A therefore looks relatively undervalued; A's positive FCFE means operating cash flow plus new borrowing covers capital spending, while B's negative FCFE signals a need for external funding.
Python check: `9.8/11.4-1 = -0.140`, `13.4-10.6 = 2.8`. ^ex-05-04-31

### Example 32: Calculating dividend yield, BCE and BT (V5 p.281, p.282)

Setup: BCE quarterly dividends 0.56, 0.60, 0.58, 0.58 (latest), price 39.53; BT ADR semiannual dividends 0.675 and 0.301 in the latest year (total 0.976), price 15.20.

Part 1 (Formula 26): dividend rate $= 4 \times 0.58 = 2.32$; yield $= 2.32/39.53 = 5.87\%$.
Part 2: uneven semiannual payer, so the dividend rate is the latest annual total 0.976; yield $= 0.976/15.20 = 6.42\%$.
The curriculum prints "0.0642, or 6.52%"; the decimal 0.0642 is right and 6.52% is a typo for 6.42%.
Python check: `0.58*4 = 2.32`, `2.32/39.53 = 0.0587`, `0.976/15.20 = 0.0642`. ^ex-05-04-32

### Example 33: Dividend yield comparables, US electric utilities (V5 p.282, p.283)

Setup: growth, beta, yield, payout: Duke 7.20%, 0.18, 4.24%, 89%; NiSource 4.63%, 0.22, 2.70%, NMF (negative EPS); Portland General 5.20%, 0.24, 2.76%, 59%; PPL 0.60%, 0.55, 5.37%, 63%.

All betas are far below 1, so risk is similar; Duke's 89% payout makes its dividend the least secure; PPL's dividend is well covered but growth is 0.60%.
Portland General's expected total return is approximately yield plus growth, $2.76\% + 5.20\% = 7.96\%$, with no strong negatives, so the manager focuses there.
Python check: `2.76+5.20 = 7.96`. ^ex-05-04-33

### Example 34: Calculating EV/EBITDA, Colgate-Palmolive (V5 p.285, p.286, p.287)

Setup (USD millions): 863 million shares at 66.48; long-term debt 6,354; current portion 0; other non-current liabilities 2,269; noncontrolling interests 299; cash 726; net income 2,400; interest 143; taxes 906; D&A 511.

Market cap $= 863 \times 66.48 = 57{,}372$.
Debt-like items $= 6{,}354 + 0 + 2{,}269 = 8{,}623$ (book value is used because market value is not readily available).
EV (Formula 28) $= 57{,}372 + 8{,}623 + 299 - 726 = 65{,}568$.
EBITDA (Formula 24) $= 2{,}400 + 143 + 906 + 511 = 3{,}960$.
EV/EBITDA $= 65{,}568/3{,}960 = 16.6$.
The curriculum prints the EV total as 65,034, which does not equal the sum of its own components; 65,568 is correct and gives the curriculum's own 16.6, whereas 65,034 would give 16.4.
Python check: `863*66.48 = 57372.2`, `57372+8623+299-726 = 65568`, `65568/3960 = 16.56`, `65034/3960 = 16.42`. ^ex-05-04-34

### Example 35: Comparable enterprise value multiples, household products (V5 p.288, p.289)

Setup (USD billions): CL price 72.60, 860 million shares, debt 7.33, cash 0.93, EBITDA 4.07; KMB 140.25, 344, 8.46, 0.53, 3.81; CLX 156.96, 127, 2.69, 0.11, 1.28; CHD 79.15, 247, 2.38, 0.10, 0.97; margins 14.8%, 9.8%, 13.2%, 5.0%; revenue growth -0.5%, -0.2%, -3.8%, 13.8%.

CL: market cap $72.60 \times 0.860 = 62.44$; TIC $= 62.44 + 7.33 = 69.77$; EV $= 69.77 - 0.93 = 68.84$; TIC/EBITDA $= 69.77/4.07 = 17.1$; EV/EBITDA $= 68.84/4.07 = 16.9$.
KMB: 48.25, 56.71, 56.18, 14.9, 14.7; CLX: 19.93, 22.62, 22.51, 17.7, 17.6; CHD: 19.55, 21.93, 21.83, 22.6, 22.5.
Part 1: TIC and EV rankings differ only if cash relative to EBITDA differs materially across firms.
Part 2: EV multiples put firm value over a pre-interest flow, unlike price to cash flow, so they compare firms with different capital structures properly.
Part 3: CL looks undervalued versus CLX and CHD and overvalued versus KMB; CHD's premium fits its 13.8% growth, and CL's premium to KMB fits its higher margin.
Python check: `72.60*0.86 = 62.44`, `68.84/4.07 = 16.9`, `56.18/3.81 = 14.7`, `22.51/1.28 = 17.6`, `21.83/0.97 = 22.5`. ^ex-05-04-35

### Example 36: Calculating EV to sales, Stora Enso (V5 p.290)

Setup: market cap EUR 8,154 million (788.6 million shares at 10.34); non-current debt 2,970; cash 1,130; sales 10,486.

EV $= 8{,}154 + 2{,}970 - 1{,}130 = 9{,}994$; EV/S $= 9{,}994/10{,}486 = 0.953$.
The curriculum's solution line writes 8,145 but its total 9,994 uses 8,154; 8,145 would give 9,985 and 0.952.
Python check: `788.6*10.34 = 8154`, `8154+2970-1130 = 9994`, `9994/10486 = 0.953`. ^ex-05-04-36

### Example 37: Scaled earnings surprise using analysts' forecasts, BP (V5 p.294)

Setup: consensus 3.26; low 2.76; high 3.74; standard deviation of the 11 forecasts 0.29; actual equals the high forecast.

Formula 30: $(3.74 - 3.26)/0.29 = 0.48/0.29 = 1.66$.
The scaling denominator is the dispersion of analysts' forecasts, which distinguishes this from SUE.
Python check: `0.48/0.29 = 1.655`. ^ex-05-04-37

### Example 38: Unexpected earnings and SUE, Exxon and Volkswagen (V5 p.295, p.296)

Setup: Exxon Sep 2013 forecast 1.77, actual 1.79, standard deviation 0.1250; other Exxon quarters give SUE -3.51, 0.94, 4.32 and percentage surprises from -18.39% to 10.20%; VW SUEs -2.60, 1.97, 0.08, -3.57 and percentage surprises from -36.33% to 14.99%.

Part 1 (Formula 31): $UE = 1.79 - 1.77 = 0.02$; SUE $= 0.02/0.1250 = 0.16$.
Part 2: by percentage surprise VW's forecasts were less accurate (range -36.33% to 14.99% versus -18.39% to 10.20%); by SUE Exxon's were (range -3.51 to 4.32 versus -3.57 to 1.97), because Exxon's surprise standard deviation is much smaller, so the same-sized miss scores higher.
The curriculum quotes VW's upper SUE as 1.13 in the solution text; the exhibit shows 1.97, and the conclusion is unchanged.
Part 3: for March 2013 both percentage surprise (2.17% versus 3.59%) and SUE (0.08 versus 0.94) are lower for VW, so VW's consensus was more accurate that quarter.
Python check: `0.02/0.125 = 0.16`, `(1.55-1.90)/0.0997 = -3.51`, `(2.20-2.00)/0.0463 = 4.32`, `(3.54-5.56)/0.5658 = -3.57`, `(5.86-5.10)/0.3858 = 1.97`. ^ex-05-04-38

### Example 39: Relative strength versus an equity index, ETFs (V5 p.297, p.298)

Setup: S&P 500 2,640.87 (Mar 2018) to 2,923.65 (Aug 2019); TLT 121.90 to 144.04; FEU 34.64 to 32.47; EEM 48.28 to 39.70; Dec 2018 to Jan 2019 RSTR: FEU 0.909 to 0.885, EEM 0.852 to 0.872.

Construction (Formula 32): TLT/S&P in March 2018 $= 121.90/2{,}640.87 = 0.04616$, scaled to 1.000; April $119.10/2{,}648.05 = 0.04498$, RSTR $= 0.04498/0.04616 = 0.974$.
Part 1, August 2019: TLT $(144.04/2{,}923.65)/0.04616 = 1.067$, outperformance of 6.7%; FEU $(32.47/2{,}923.65)/(34.64/2{,}640.87) = 0.847$, underperformance of 15.3%; EEM $(39.70/2{,}923.65)/(48.28/2{,}640.87) = 0.743$, underperformance of 25.7%.
Part 2, December 2018: FEU fell from 0.909 to 0.885, $0.885/0.909 - 1 = -2.6\%$ (curriculum says 2.7%); EEM rose from 0.852 to 0.872, $+2.3\%$; EEM beat FEU that month even though FEU beat EEM over the full period.
Python check: `121.90/2640.87 = 0.04616`, `0.04498/0.04616 = 0.9744`, `(144.04/2923.65)/0.04616 = 1.067`, `0.885/0.909-1 = -0.0264`, `0.872/0.852-1 = 0.0235`. ^ex-05-04-39

### Example 40: Multiple indicators in stock valuation, analyst report excerpts (V5 p.301, p.302)

Setup: an Aussie Beverage report values the stock by DCF at A$0.82 (44% premium to price), cross-checks with a mid-cycle PER of 10.5 times FY08 EPS of 7.6 cents giving A$0.80, notes a forward PER of 9.1 at the A$0.75 target and a 5.7% yield; a Südliche Logistik report cites P/E 12.4 and EV/EBITDA 9 versus peers and raises the target to EUR 53 (24% upside).

Check: $10.5 \times 0.076 = 0.798 \approx 0.80$ and $0.75/0.082 = 9.1$ (a forward PER of 9.1 at the target implies forward EPS near 8.2 cents).
Lesson: practitioners combine a primary DCF with several multiples and a yield; the 2012 survey shows P/E, beta, EV/EBITDA, ROE, size and P/B used by more than half of institutions and an average of 9.3 factors per investor.
Python check: `10.5*0.076 = 0.798`, `0.75/9.1 = 0.0824`. ^ex-05-04-40

### Example 41: Using screens to find stocks, Larsen (V5 p.303, p.304, p.305)

Setup: successive screens on US stocks at 17 July 2019: P/E under 20 (2,096), P/B under 2.0 (1,384), PEG under 1.0 (89), dividend yield at least 3.0% (23), market cap over 10 billion (10); S&P 500 P/E 22.3, P/B 3.5, yield 1.9%.

Part 1: no momentum indicators (earnings surprise, relative strength) are included.
Part 2: Larsen is a large-cap value investor: every multiple criterion is a "less than" cutoff, her P/B cap sits below the index's 3.5, and she has no explicit growth or momentum criteria.
Part 3: limitations: no profitability or risk criteria (low P/E may reflect low profitability or high risk), no control over the vendor's input calculations, and no qualitative factors.
Look-ahead bias is the related back-testing hazard: using fourth-quarter EPS in early January before it was reported (V5 p.303).
Python check: `1384/2096 = 0.66` of the P/E survivors also pass the P/B screen. ^ex-05-04-41

## Item-set patterns

> [!warning] Trap 1: which P/E, trailing or forward, and which EPS
> The vignette mentions an acquisition, divestiture, leverage change or "unusual items" in last year's EPS, then supplies both trailing and next-year EPS and asks for "the most appropriate P/E".
> Correct: forward P/E when the past is not representative (Practice Problem 10: $65.50/3.50 = 18.71$); diluted EPS when a company has options or convertibles (Practice Problem 7: $30{,}000{,}000/33{,}333{,}333 = 0.90$, P/E 25).
> Distractors: the trailing P/E ($65.50/3.44 = 19.04$), a price to free cash flow ($65.50/2.68 = 24.44$) masquerading as a P/E, and the basic-EPS P/E of 22.5 that flatters the company with options (V5 p.228, p.326, p.327).

> [!warning] Trap 2: underlying EPS, which items to reverse
> A footnote lists a nonrecurring gain, a nonrecurring charge and a recurring cost increase, and offers both basic and diluted EPS.
> Correct: start from diluted EPS, subtract the gain, add back the charge, leave the recurring item: $0.81 - 0.04 + 0.03 = 0.80$, P/E $14.72/0.80 = 18.4$.
> Distractors: unadjusted diluted EPS (18.2), the same adjustments applied to basic EPS (17.7), and reversing the recurring depreciation too (V5 p.329).

> [!warning] Trap 3: normalized EPS by average ROE uses current BVPS and common book value
> The exhibit gives four or five years of EPS, BVPS and ROE, sometimes with an estimated current year, and a balance sheet with preferred stock.
> Correct: average the ROEs over the cycle the vignette defines, then multiply by the most recent (or estimated year-end) BVPS computed on common equity after deducting preferred: $0.131 \times 22.58 = 2.96$.
> Distractors: average ROE times BVPS on total equity ($0.131 \times 24.49 = 3.21$), the historical average EPS (5.07), and using an old year's BVPS (V5 p.328, p.329).

> [!warning] Trap 4: justified multiple, forward versus trailing and the hidden CAPM
> The stem gives payout (or DPS and EPS), ROE, growth, and either r directly or a risk-free rate, beta and ERP.
> Correct: build r first if needed ($4.9\% + 1.2 \times 5.5\% = 11.5\%$); forward P/E $(1-b)/(r-g)$, trailing P/E $(1-b)(1+g)/(r-g)$, P/B $(ROE-g)/(r-g)$, P/S margin $\times (1-b)/(r-g)$; use $D_1/E_1$ for forward when both are supplied ($(2.91/6.00)/0.09 = 5.4$).
> Distractors: trailing when forward is asked ($5.7$), the market's actual forward P/E ($8.3$), forgetting $(1+g)$ on trailing P/E (17.1 instead of 18.5), and using ROE in place of $(ROE - g)$ in the P/B numerator (V5 p.238, p.265, p.328, p.332).

> [!warning] Trap 5: EV components and the EV versus price mismatch
> A balance sheet or market data table lists common equity, preferred, debt (book and market), cash and short-term investments, and sometimes minority interest; a follow-up asks which of P/EBITDA and EV/EBITDA to trust.
> Correct: EV $=$ market common $+$ market preferred $+$ minority interest $+$ market debt $-$ cash $-$ short-term investments ($1{,}733 + 6{,}766 + 275 - 581 - 495 = 7{,}698$, EV/EBITDA 13.7); divide by total EBITDA, never per share; prefer EV/EBITDA when leverage differs because EBITDA is pre-interest.
> Distractors: forgetting short-term investments (14.6), forgetting preferred (EV/S 0.74 instead of 0.77), using book debt when market debt is given, and following P/EBITDA to the wrong pick (NCI at 10 versus RGI at 12 by P/EBITDA, but RGI 12.7 versus NCI 14.9 by EV/EBITDA) (V5 p.285, p.328, p.330, p.333).

> [!warning] Trap 6: negative EPS in the peer group
> One comp has negative trailing EPS and the question asks for the metric that gives a meaningful ranking.
> Correct: earnings yield E/P, because price is never negative; the lowest E/P (most negative) is the most expensive; alternatively normalized EPS or forward EPS if it is positive, and P/B or P/S as fallbacks.
> Distractors: computing and ranking negative P/Es, a "P/D" answer that is not a valuation ratio, and forward P/E when next year's EPS is also expected to be negative (V5 p.233, p.234, p.326, p.329).

> [!warning] Trap 7: SUE versus scaled earnings surprise, and relative strength definitions
> A statement says "SUE scales unexpected earnings by the standard deviation of analysts' forecasts".
> Correct: that is the scaled earnings surprise; SUE divides by the standard deviation of past unexpected earnings; relative strength compares a stock with its own past or with a group of stocks.
> Distractors: accepting the SUE statement, treating relative strength as a fundamental multiple, or forgetting that momentum is a growth-style tool inconsistent with a value mandate (V5 p.294, p.296, p.330, p.334).

> [!warning] Trap 8: averaging the peer multiples
> The peer table contains an outlier P/E (44.10 or 70.67) and the question asks which central tendency mitigates large outliers but not small ones, or asks for the harmonic mean benchmark.
> Correct: the harmonic mean, $n$ over the sum of reciprocals ($5/(1/5.9 + 1/8.3 + 1/3.0 + 1/15.0 + 1/4.6) = 5.5$); the median is immune to all outliers; the weighted harmonic mean reproduces the portfolio P/E.
> Distractors: the arithmetic mean (7.4 for the same five), the median (5.9), and concluding "undervalued" by comparing the subject's forward P/E of 8.3 with the arithmetic mean instead of the harmonic mean (V5 p.299, p.300, p.328).

> [!warning] Trap 9: P/S from mismatched units and the P/S versus P/E argument
> Sales are in billions and shares in millions or billions; a second question asks why P/E might be preferred to P/S.
> Correct: sales per share $= 67.44\text{ bn}/1.638821\text{ bn} = 41.15$, P/S $= 37.23/41.15 = 0.90$; P/E reflects financial leverage and cost structure while P/S does not, but sales are more stable and less manipulable than earnings, so "earnings are more stable" and "earnings are less manipulated" are wrong reasons.
> Distractors: price over total sales in billions (0.55), book value over sales per share (0.28), and the two false reasons (V5 p.268, p.327).

> [!warning] Trap 10: Fed and Yardeni model statements
> Statements describe when the Fed model calls the market under- or overvalued and what the Yardeni model adds.
> Correct: Fed model says overvalued when earnings yield is below the 10-year Treasury yield (so undervalued when above); Yardeni adds the consensus five-year earnings growth (LTEG) and uses the A-rated corporate bond yield.
> Distractors: reversing the inequality, claiming the Fed model includes growth or an equity risk premium, or claiming Yardeni uses the Treasury yield (V5 p.250, p.251, p.329).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM04-Market-Based-Valuation-Price-and-Enterprise-Value-Multiples-Practice-Problems]]

## Cross-links

- [[LM02-Discounted-Dividend-Valuation]]: every justified multiple here is the Gordon growth model divided by a fundamental, and $g = b \times ROE$ and the PVGO decomposition come straight from that module.
- [[LM03-Free-Cash-Flow-Valuation]]: FCFE and FCFF definitions feed P/FCFE, the justified P/CF from a constant-growth FCFE model, and the argument that FCFF beats EBITDA because it reflects capital expenditure.
- [[LM05-Residual-Income-Valuation]]: justified P/B equals $1 + PV(\text{residual income})/B_0$, so P/B above 1 means ROE above r; that module supplies the clean surplus machinery behind the identity.
- [[LM06-Private-Company-Valuation]]: the guideline public company and guideline transactions methods are this module's method of comparables applied with control premiums and marketability discounts.
- [[LM05-Evaluating-Quality-of-Financial-Reports]]: underlying earnings, normalized EPS, revenue recognition abuses (bill-and-hold, barter, gross booking) and cash flow enhancement tricks are the quality-of-earnings material behind the analyst adjustments here.
- [[LM03-Investments-in-Real-Estate-through-Publicly-Traded-Securities]]: P/FFO and P/AFFO for REITs are sector-specific price multiples built with the same comparables logic and the same EV-style adjustments for debt.

## Self-test

Vignette A for Q1 to Q4: Marlow Industrial trades at 48.00.
Trailing diluted EPS is 3.20, which includes a nonrecurring gain of 0.30 on an asset sale, a nonrecurring impairment charge of 0.50, and a 0.10 increase in lease expense that will continue.
Consensus forward EPS is 3.60 and next year's DPS is 1.44.
ROE is 12% and retention is 60%; BVPS is 30.00.
The risk-free rate is 3.0%, Marlow's beta is 1.2 and the equity risk premium is 5.0%.
Five peers trade at forward P/Es of 12.0, 14.0, 9.0, 40.0 and 16.0.

> [!question] Q1
> Marlow's trailing P/E on underlying EPS is closest to:
> A. 13.7.
> B. 14.1.
> C. 15.0.

> [!question] Q2
> Marlow's justified forward P/E based on the Gordon growth model is closest to:
> A. 13.3.
> B. 22.2.
> C. 23.8.

> [!question] Q3
> Marlow's justified P/B is closest to, and relative to its actual P/B the stock appears:
> A. 1.33, overvalued.
> B. 2.67, undervalued.
> C. 6.67, undervalued.

> [!question] Q4
> Using the harmonic mean of the peer forward P/Es as the benchmark, Marlow's shares are most likely:
> A. undervalued.
> B. fairly valued.
> C. overvalued.

Vignette B for Q5 to Q7: Kestrel Foods has 200 million shares at 25.00; preferred stock with market value 300 million; minority interest 150 million; debt with book value 1,800 million and market value 1,900 million; cash 400 million and short-term investments 250 million.
Net income is 320, interest 110, taxes 90, depreciation and amortization 280, sales 6,000 (all millions).
Rival Osprey Foods carries almost no debt and trades at EV/EBITDA of 10.0 and P/EBITDA of 9.5.

> [!question] Q5
> Kestrel's EV/EBITDA is closest to:
> A. 7.8.
> B. 8.4.
> C. 8.7.

> [!question] Q6
> Kestrel's P/S is closest to:
> A. 0.83.
> B. 1.12.
> C. 1.15.

> [!question] Q7
> In judging whether Kestrel is cheaper than Osprey, the analyst should rely on:
> A. EV/EBITDA, because EBITDA is a pre-interest flow to all capital providers and the two firms differ in leverage.
> B. P/EBITDA, because the equity investor pays the share price, not the enterprise value.
> C. P/E, because only P/E reflects the effect of financial leverage.

Vignette C for Q8 to Q10: Tanager Utilities trades at 28.00 and paid quarterly dividends of 0.40, 0.40, 0.42 and, most recently, 0.42; its required return is 8% and dividend growth 2%.
Last quarter the consensus EPS was 1.20 with a standard deviation of analyst forecasts of 0.06; actual EPS was 1.32; the standard deviation of Tanager's past earnings surprises over 20 quarters is 0.15.
Over the past year Tanager rose from 40 to 46 while its benchmark index rose from 2,000 to 2,200.

> [!question] Q8
> Tanager's trailing dividend yield is closest to:
> A. 5.86%.
> B. 5.88%.
> C. 6.00%.

> [!question] Q9
> Tanager's standardized unexpected earnings (SUE) for the quarter is closest to:
> A. 0.80.
> B. 2.00.
> C. 10.0%.

> [!question] Q10
> Tanager's relative-strength indicator versus the index, scaled to 1.0 a year ago, is closest to:
> A. 0.957.
> B. 1.045.
> C. 1.150.

> [!success]- Answer key
> Q1: B.
> Underlying EPS $= 3.20 - 0.30 + 0.50 = 3.40$ (the lease increase is recurring and stays); $48/3.40 = 14.1$.
> A reverses the recurring lease cost too ($48/3.50 = 13.7$); C uses reported EPS ($48/3.20 = 15.0$).
> Q2: B.
> $r = 3\% + 1.2 \times 5\% = 9\%$; $g = 0.6 \times 0.12 = 7.2\%$; payout 0.40; forward P/E $= 0.40/(0.09 - 0.072) = 0.40/0.018 = 22.2$ (also $D_1/E_1 = 1.44/3.60 = 0.40$).
> A is the actual forward P/E $48/3.60 = 13.3$; C is the justified trailing P/E $0.40 \times 1.072/0.018 = 23.8$.
> Q3: B.
> Justified P/B $= (0.12 - 0.072)/(0.09 - 0.072) = 0.048/0.018 = 2.67$; actual P/B $= 48/30 = 1.6$, below justified, so undervalued.
> A is $ROE/r = 1.33$, the zero-growth shortcut misapplied; C is $ROE/(r-g) = 6.67$, omitting $g$ from the numerator.
> Q4: A.
> Harmonic mean $= 5/(1/12 + 1/14 + 1/9 + 1/40 + 1/16) = 5/0.3534 = 14.15$; Marlow's forward P/E $48/3.60 = 13.3$ is below it, so relatively undervalued.
> The arithmetic mean 18.2 (dragged up by the 40.0 outlier) and the median 14.0 give the same direction; C would require a benchmark below 13.3.
> Q5: B.
> EV $= 5{,}000 + 300 + 150 + 1{,}900 - 400 - 250 = 6{,}700$; EBITDA $= 320 + 110 + 90 + 280 = 800$; $6{,}700/800 = 8.4$.
> A drops preferred and minority interest ($6{,}250/800 = 7.8$); C forgets to deduct short-term investments ($6{,}950/800 = 8.7$); using book debt would give 8.25.
> Q6: A.
> Sales per share $= 6{,}000/200 = 30$; P/S $= 25/30 = 0.83$.
> B is EV/S $6{,}700/6{,}000 = 1.12$; C is market cap plus debt over sales ($6{,}900/6{,}000 = 1.15$), neither of which is a price multiple.
> Q7: A.
> EBITDA belongs to debt and equity holders, so it must sit under a total-capital numerator; Kestrel's P/EBITDA of $5{,}000/800 = 6.25$ versus Osprey's 9.5 exaggerates Kestrel's cheapness because Kestrel's debt is ignored, while EV/EBITDA (8.4 versus 10.0) still shows Kestrel cheaper but by less.
> B mismatches an equity numerator with a pre-interest denominator; C is irrelevant to the EBITDA comparison and P/E's leverage sensitivity is a reason to prefer EV multiples when leverage differs.
> Q8: C.
> Dividend rate $= 4 \times 0.42 = 1.68$; yield $= 1.68/28 = 6.00\%$.
> A sums the last four dividends ($1.64/28 = 5.86\%$), a definition some vendors use but not the curriculum's; B is the justified yield $(0.08 - 0.02)/1.02 = 5.88\%$.
> Q9: A.
> $UE = 1.32 - 1.20 = 0.12$; SUE $= 0.12/0.15 = 0.80$ using the standard deviation of historical surprises.
> B is the scaled earnings surprise $0.12/0.06 = 2.00$ using analyst dispersion; C is the percentage surprise $0.12/1.20 = 10\%$.
> Q10: B.
> RSTR $= (46/2{,}200)/(40/2{,}000) = 0.020909/0.020 = 1.045$, a 4.5% outperformance.
> A is the reciprocal (index relative to stock); C is the stock's own 15% return, ignoring the index's 10%.

## Flashcards

#flashcards/cfa-l2/05-Equity-Valuation/lm04

Economic rationale for the method of comparables::The law of one price, two identical assets should sell at the same price (V5 p.224).
Economic rationale for the method based on forecasted fundamentals::A DCF model, since a multiple is the DCF value divided by a forecast fundamental (V5 p.225).
Justified price multiple definition::The estimated fair value of the multiple, justified either by comparables or by forecasted fundamentals (V5 p.225).
Trailing P/E denominator::EPS of the most recent four quarters (TTM) (V5 p.227).
Three interpretations of "next year" in forward P/E::Next four quarters, next twelve months (NTM), or next fiscal year (V5 p.235).
NTM EPS with m months left in FY1::(m/12) times FY1 EPS plus ((12-m)/12) times FY2 EPS (V5 p.235).
When must forward P/E be used instead of trailing?::After a major acquisition, divestiture or leverage change that makes past EPS unrepresentative (V5 p.228).
Which EPS for cross-company P/E comparisons, basic or diluted?::Diluted, so companies with different dilutive securities are comparable; it raises the P/E (V5 p.229).
Four analyst adjustments before computing trailing P/E::Dilution, nonrecurring items, business-cycle effects, and accounting method differences (V5 p.228).
Underlying earnings synonyms::Persistent, continuing, core earnings, excluding nonrecurring items (V5 p.229).
Molodovsky effect::P/E is countercyclical, high on depressed trough EPS and low on peak EPS (V5 p.231).
Two methods of normalizing EPS::Historical average EPS over the cycle, or average ROE over the cycle times current BVPS (V5 p.231).
Why the average ROE method is usually preferred::It uses current book value so it reflects growth or shrinkage in the size of the business (V5 p.231, p.232).
Micro-problem: ROEs 21.8, 16.3, 1.6, 8.9 percent; current BVPS 19.20; price 57.98; normalized P/E?::Average ROE 12.15 percent, EPS 2.33, P/E 24.9; keystrokes 21.8 + 16.3 + 1.6 + 8.9 = ÷ 4 = × 19.20 ÷ 100 = then 57.98 ÷ 2.33 = (V5 p.326).
Why negative P/Es are not meaningful::The negative-P/E stock ranks below the cheapest positive-P/E stock yet is the most expensive per unit of earnings (V5 p.233).
Cure for negative or tiny EPS in rankings::Use the inverse ratio E/P, since price is never negative; report negative P/Es as NM (V5 p.234).
Earnings yield as an expected return::E1/P0 is the expected return on a no-growth stock priced at value, from P0 = E1/r + PVGO with PVGO of zero (V5 p.250).
Justified forward P/E formula::(1 - b)/(r - g), the Gordon model divided by E1 (V5 p.238).
Justified trailing P/E formula::(1 - b)(1 + g)/(r - g), the Gordon model divided by E0 (V5 p.238).
Micro-problem: payout 0.30, r 14 percent, g 13 percent; trailing and forward justified P/E?::Trailing 0.30 × 1.13 ÷ 0.01 = 33.9; forward 0.30 ÷ 0.01 = 30 (V5 p.330).
Three limitations of cross-sectional P/E regressions::Valid only for the sample and period, coefficients unstable over time, multicollinearity blurs coefficients (V5 p.241).
Four steps of the method of comparables
?
Select and compute the multiple; select comparison assets and compute their median or mean; apply the benchmark (adjusted for fundamentals) or compare multiples; judge whether differences are explained by fundamentals (V5 p.242).

Why prefer the median to the mean for a peer benchmark?::The median is insensitive to outliers such as a P/E of 70 or a negative P/E (V5 p.245).
Directional adjustments in comparables::Higher expected growth justifies a higher P/E; higher operating or financial risk justifies a lower P/E (V5 p.244).
PEG ratio definition::P/E divided by expected earnings growth in percentage points; lower is more attractive (V5 p.246).
Three cautions on PEG::Assumes a linear P/E-growth link, ignores risk, ignores growth duration (V5 p.246).
Fed model rule::Market overvalued when the forward earnings yield is below the 10-year Treasury yield; justified P/E is 1 over the bond yield (V5 p.250).
Fed model criticisms::Ignores growth and the equity risk premium, mishandles inflation, nonlinear at low rates (V5 p.251).
Yardeni model justified P/E::1/(CBY - b × LTEG), with A-rated corporate bond yield and consensus five-year growth (V5 p.251).
Justified P/E with inflation I and pass-through lambda::1/(rho + (1 - lambda) I) where rho is the real required return (V5 p.254).
Effect of inflation on justified P/E::Lower P/E when pass-through is below 100 percent; no effect with full pass-through; the penalty grows with inflation (V5 p.255).
Terminal value from a multiple::Vn equals benchmark trailing P/E times En, or benchmark forward P/E times En+1 (V5 p.255).
Strength and weakness of comparables-based terminal value::Grounded in market data, but imports any mispricing embedded in the benchmark (V5 p.255, p.256).
Book value per share definition::(Total shareholders' equity minus preferred equity and dividends in arrears) divided by common shares outstanding (V5 p.259, p.260).
Tangible book value::Common equity minus reported goodwill and intangibles; exclusion of separable intangibles like patents may not be warranted (V5 p.261).
Justified P/B formula and derivation
?
(ROE - g)/(r - g); from V0 = E1(1 - b)/(r - g), put E1 = ROE × B0 and b = g/ROE so ROE(1 - b) = ROE - g (V5 p.265).

Justified P/B with zero growth::ROE/r; what drives P/B is ROE relative to r (V5 p.265).
Residual income form of justified P/B::1 plus PV of expected residual income over B0; P/B above 1 when ROE exceeds r (V5 p.265).
Micro-problem: ROE 20 percent, g 8 percent, r 11.5 percent; justified P/B?::(0.20 - 0.08)/(0.115 - 0.08) = 0.12/0.035 = 3.4 (V5 p.332).
Effect of share buybacks above book value on P/B::BVPS falls, so P/B rises and the stock looks more expensive against its own history (V5 p.259).
Relationship between P/S and P/E::P/S equals P/E times net profit margin (V5 p.268).
Justified forward P/S formula::(E1/S1)(1 - b)/(r - g), the Gordon model divided by S1 (V5 p.269).
Justified trailing P/S formula::(E0/S0)(1 - b)(1 + g)/(r - g) (V5 p.272).
Micro-problem: margin 9 percent, payout 35 percent, r 9 percent, g 7 percent; justified P/S?::0.09 × 0.35 ÷ 0.02 = 1.575 (V5 p.273).
Conceptual weakness of P/S::Price is an equity claim while sales are pre-financing, so use EV/S when capital structures differ; P/S also ignores cost structure (V5 p.268, p.290).
Three revenue recognition abuses that inflate P/S denominators::Advertising barter, bill-and-hold sales, booking gross instead of net revenue (V5 p.269, p.270, p.271).
Cash flow per share in the P/CF definition::EPS plus per-share depreciation, amortization and depletion (V5 p.277).
Limitation of the earnings-plus-noncash-charges cash flow::Ignores noncash revenue and working capital changes, so front-loaded revenue slips through (V5 p.275).
Limitation of FCFE in price multiples::Strongest theoretical link but more volatile and more often negative; capex timing distorts single-year P/FCFE (V5 p.275, p.278).
IFRS versus US GAAP cash flow classification issue::IFRS allows interest and dividends received in operating or investing and interest paid in operating or financing; US GAAP puts all three in operating (V5 p.276).
EBITDA from net income::Net income plus interest plus taxes plus depreciation plus amortization, starting from continuing operations excluding nonrecurring items (V5 p.278, p.287).
Why EV/EBITDA beats P/EBITDA::EBITDA is pre-interest, a flow to debt and equity, so it must sit under total firm value (V5 p.278).
Enterprise value formula
?
Market value of common equity plus market value of preferred plus minority interest plus market value of debt, minus cash, cash equivalents and short-term investments (V5 p.284, p.285).

Why cash is deducted from EV::An acquirer gains access to the cash after buying out equity and debt, lowering the net cost (V5 p.285).
Total invested capital versus EV::TIC does not deduct cash and investments; rankings differ only if cash relative to EBITDA differs materially (V5 p.287, p.288).
Two drawbacks of EV/EBITDA::Overstates operating cash flow when working capital grows; ignores capex, unlike FCFF (V5 p.284).
Fundamental drivers of justified EV/EBITDA::Positively FCFF growth and ROIC, negatively WACC (V5 p.287).
Micro-problem: debt 1,733, equity 6,766, preferred 275, cash 581, short-term investments 495, EBITDA 560; EV/EBITDA?::EV 7,698, multiple 13.7; keystrokes 1733 + 6766 + 275 - 581 - 495 = ÷ 560 = (V5 p.330).
Trailing dividend yield for a quarterly payer::Four times the most recent quarterly dividend divided by price (V5 p.281).
Justified dividend yield::(r - g)/(1 + g); falls with growth, rises with r, so high-yield screens are value screens (V5 p.282).
Dividend displacement of earnings::Holding ROE constant, dividends paid now displace earnings in all future periods (V5 p.280).
Multiples least and most affected by international accounting differences::Least P/CFO and P/FCFE; most P/E, P/B and EBITDA-based multiples (V5 p.293).
Unexpected earnings and percentage surprise::Actual EPS minus expected EPS; percentage surprise divides by expected EPS (V5 p.294).
Scaled earnings surprise denominator::Standard deviation of analysts' earnings forecasts (V5 p.294).
SUE denominator::Standard deviation of past unexpected earnings over a historical window such as 20 quarters (V5 p.294).
Which is the trap: "SUE scales by the dispersion of analyst forecasts"?::Wrong, that is the scaled earnings surprise; SUE uses historical surprise dispersion (V5 p.330).
Two types of relative strength::Stock versus its own past (compound return, price momentum) and stock versus a group or index, scaled to 1.0 at the start (V5 p.296).
Micro-problem: stock 40 to 46, index 2,000 to 2,200; RSTR?::(46/2200)/(40/2000) = 1.045, 4.5 percent outperformance (V5 p.297).
Harmonic mean formula::n divided by the sum of reciprocals; the reciprocal of the arithmetic mean of reciprocals (V5 p.299).
Weighted harmonic mean property::With value weights it equals the portfolio's aggregate multiple, so index vendors use it (V5 p.300).
Harmonic mean and outliers::Below the arithmetic mean unless all values equal; dampens large outliers but may aggravate small ones near zero (V5 p.300).
Micro-problem: peer P/Es 5.9, 8.3, 3.0, 15.0, 4.6; harmonic mean?::5.5; keystrokes 5.9 1/x + 8.3 1/x + 3 1/x + 15 1/x + 4.6 1/x = 1/x × 5 = (V5 p.328).
Look-ahead bias in back-tests::Using data such as fourth-quarter EPS before it was actually reported when computing trailing multiples (V5 p.303).
Limitations of commercial stock screens::No control over how inputs like EPS are computed, and no qualitative factors (V5 p.303, p.305).
The three momentum indicators in the curriculum::Earnings surprise, standardized unexpected earnings, relative strength (V5 p.293).
Situations where P/B is appropriate::{{Non-going concerns}}, {{companies of mainly liquid assets such as banks and insurers}}, and {{negative or highly variable EPS}} (V5 p.257, p.331).

## Common mistakes

1. Mixing trailing and forward P/Es across companies; for growing firms the forward multiple is systematically lower, so the error is biased, not random (V5 p.228).
2. Using basic EPS for a company with options or convertibles, which understates the P/E; compare on diluted EPS (V5 p.229, p.326).
3. Accepting company-reported core or adjusted EPS without reading the reconciliation; underlying earnings are the analyst's judgment, not the company's (V5 p.230).
4. Reversing a recurring cost increase when computing underlying EPS, or forgetting to subtract a nonrecurring gain (V5 p.329).
5. Normalizing with average ROE times an old year's BVPS, or times BVPS on total equity including preferred, instead of current common BVPS (V5 p.232, p.328).
6. Ranking stocks by P/E when one has negative EPS; use E/P, and label negative P/Es NM (V5 p.233, p.234).
7. Dropping the $(1+g)$ factor from the justified trailing P/E or P/S, or using $D_0/E_0$ in the forward P/E (V5 p.238, p.328).
8. Writing the justified P/B numerator as ROE instead of $ROE - g$, or reading a low P/B as cheap without checking ROE against r (V5 p.265).
9. Treating PEG below 1 as an absolute buy signal and ignoring that PEG omits risk and growth duration and assumes linearity (V5 p.246, p.247).
10. Building EV without preferred stock, minority interest or short-term investments, or dividing EV by per-share EBITDA (V5 p.285, p.330, p.333).
11. Choosing P/EBITDA over EV/EBITDA when leverage differs; EBITDA is pre-interest and belongs to all capital providers (V5 p.278, p.333).
12. Arguing that earnings are more stable or less manipulable than sales; the curriculum says the opposite, and the valid reason to prefer P/E is that it reflects leverage and cost structure (V5 p.268, p.327).
13. Confusing SUE (historical surprise dispersion) with scaled earnings surprise (analyst forecast dispersion) (V5 p.294, p.330).
14. Computing a trailing dividend yield from the last four dividends when the curriculum's dividend rate is four times the latest quarterly dividend, or forgetting that uneven semiannual payers use the latest annual total (V5 p.281).
15. Using the arithmetic mean of peer multiples when a large outlier is present; use the median, or the harmonic mean if only large outliers should be damped (V5 p.245, p.300).
16. Concluding a stock is undervalued in absolute terms from a relative comparison without asking whether the comparables or the index are themselves fairly priced (V5 p.224, p.331).
17. Applying own-historical P/E benchmarks after a change in business mix, leverage or inflation environment (V5 p.253).
18. Back-testing trailing multiples with earnings that had not yet been reported at the decision date (look-ahead bias) (V5 p.303).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "05-04" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
