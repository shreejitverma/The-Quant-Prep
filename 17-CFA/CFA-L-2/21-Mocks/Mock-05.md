---
type: cfa-mock
mock: 5
sessions: 2
minutes_per_session: 132
tags: [cfa/l2, cfa/mock]
---
# Mock 5

Two sessions of 2 hours 12 minutes, 11 item sets each, no notes, calculator reset before each session.
Log the attempt with QuickAdd (CFA: log attempt) with source Mock-05 and confidence recorded before opening any answer key.
Fresh item sets written for this mock (source mock-05); each also lives in the bank under its own note.

## Session 1

## Item set 1 (09-04): Pell River Retirement System: Enhanced Index Risk Budget

Source: [[IS-09-Portfolio-Management-LM04-M05]], difficulty 3.

### Vignette

The Pell River Municipal Employees' Retirement System allocates part of its US large-cap equity portfolio to an enhanced index mandate managed by Corvina Asset Management.
The mandate's guidelines require Corvina to keep annual tracking risk at or below 2.00% and to deliver an information ratio of at least 0.35, both measured over the trailing three years.
Nadia Ferreira, CFA, a senior investment officer at the system, is preparing Corvina's mandate review.
Oliver Stroud, a consultant retained by the board, assists her.

Ferreira uses the system's fundamental factor model, which has four standardized style factors and industry factors.
Corvina's industry weights match the benchmark's, so its industry exposures are omitted.
The model vendor states that covariances among the style factor returns are negligible, and it reports Corvina's active specific risk as 1.17 (% squared).
Sensitivities are measured at the start of the review period.

**Exhibit 1: Style factor sensitivities and factor return volatility**

| Factor | Corvina sensitivity | Benchmark sensitivity | Annual standard deviation of factor return |
|---|---|---|---|
| Value (book-to-price) | 0.30 | 0.10 | 3.0% |
| Size (log market capitalization) | 0.45 | 0.60 | 4.0% |
| Momentum (12-month price change) | 0.12 | 0.00 | 5.0% |
| Quality (return on equity) | 0.20 | 0.20 | 2.5% |

**Exhibit 2: Trailing three-year performance, annualized**

| Statistic | Corvina | Benchmark |
|---|---|---|
| Mean return | 11.40% | 10.80% |
| Standard deviation of return | 15.8% | 15.2% |

Ferreira computes Corvina's active factor risk directly from the active exposures and the factor variances, adds the vendor's active specific risk to obtain active risk squared, and then evaluates the manager against both guideline limits.

Stroud reviews Ferreira's draft and makes two comments.

Stroud (2 June): "Corvina's quality sensitivity of 0.20 is its second-largest exposure in Exhibit 1, so the quality factor must be one of the more important sources of its active risk. By contrast, its momentum sensitivity is the smallest of its tilts, so momentum can contribute very little."

Stroud (2 June, continued): "I ran a five-factor macroeconomic model and our fundamental model, which includes about 60 industry dummy variables, on the same large-cap universe last year. The fundamental model explained 41% of the variance of monthly stock returns against 13% for the macroeconomic model. The fundamental model is therefore superior in every respect, and the system has no use for a macroeconomic model."

Ferreira intends to present a breakdown of Corvina's active risk that shows how much comes from security selection and how much comes from each style tilt, because the board has asked whether an enhanced index manager should be taking style bets at all.
She also plans to respond to Stroud's model comparison before the board meets, because the system's liability-driven overlay program already uses a macroeconomic model to measure its exposure to inflation and interest rate surprises.

### Questions

1. Corvina's active factor risk is closest to: (LOS: los-09-04-g)
   - A. 0.28 (% squared).
   - B. 1.08 (% squared).
   - C. 4.66 (% squared).
2. Corvina's tracking risk and information ratio, and its compliance with the mandate guidelines, are best described as: (LOS: los-09-04-g)
   - A. 1.50% and 0.40; both guidelines are met.
   - B. 2.25% and 0.27; neither guideline is met.
   - C. 0.60% and 1.00; both guidelines are met.
3. Based on Ferreira's decomposition, which statement about the sources of Corvina's active risk is most accurate? (LOS: los-09-04-e)
   - A. Momentum contributes the least active factor risk, because Corvina's momentum active exposure is the smallest of its three style tilts.
   - B. The quality factor contributes to active risk, because Corvina's quality sensitivity of 0.20 is not zero.
   - C. Active specific risk is 52% of active risk squared, and the value, size, and momentum tilts each account for 16%.
4. The most appropriate response to Stroud's model comparison is that: (LOS: los-09-04-d)
   - A. part of the fundamental model's explanatory advantage is built into the comparison, because its industry factors together replicate the market, while the macroeconomic model is more parsimonious and maps directly to economic views such as inflation surprises.
   - B. Stroud is correct, because the proportion of return variance explained is the single criterion for choosing a factor model.
   - C. Stroud's figures are probably reversed, because macroeconomic models, whose factors are zero-mean surprises, typically explain more return variance than fundamental models.

## Item set 2 (09-05): Oakhurst Capital Advisors: Relative Risk and Sensitivity Scenarios

Source: [[IS-09-Portfolio-Management-LM05-M05]], difficulty 3.

### Vignette

Mireille Fontaine, CFA, is head of investment risk at Oakhurst Capital Advisors, a long-only asset manager.
She reports to Rafael Okonkwo, the firm's chief investment officer.
Fontaine is preparing risk reports for two client accounts.

The first account is a USD 800 million global equity mandate for a university endowment, managed against a global equity index.
The endowment's investment committee wants a forward-looking estimate of how far the mandate could lag its benchmark over the next year.
Fontaine runs Oakhurst's risk model on the current holdings and obtains the annual estimates in Exhibit 1.
She assumes the expected active return is zero and that active returns are normally distributed.

Exhibit 1: Global equity mandate, forward-looking annual estimates

| Item | Value |
|---|---|
| Standard deviation of portfolio returns | 17.4% |
| Standard deviation of benchmark returns | 15.2% |
| Correlation between portfolio and benchmark returns | 0.95 |
| Realized tracking error, last three years | 2.10% |
| Expected return of the benchmark | 7.5% |

The committee chair asks for the mandate's 5% annual relative VaR in US dollars, together with a plain-language interpretation.

The second account is a USD 400 million balanced account for a family office.
It holds USD 240 million in an equity sleeve and USD 160 million in an option-free, investment-grade bond sleeve.
Fontaine applies the sensitivities in Exhibit 2 to a scenario the family office has asked about: the broad equity index falls 15% and bond yields rise by 80 basis points.

Exhibit 2: Balanced account sensitivities

| Sleeve | Market value (USD millions) | Sensitivity |
|---|---|---|
| Equity | 240 | Beta of 1.09 relative to the broad equity index |
| Bonds | 160 | Duration 6.8, convexity 58, yield 4.5% |

Oakhurst also manages two bond mandates that the family office is considering, a high-yield corporate mandate and an investment-grade corporate mandate.
The firm's report shows sensitivities for both, grouped into maturity buckets.
Fontaine and Okonkwo discuss what these sensitivity reports can and cannot show.

Fontaine: "Our reports place all bonds maturing between 7 and 15 years into one bucket and show a single duration for it; doing so implicitly assumes that yield changes are perfectly correlated within the bucket, so the report can hide exposure to changes in the shape of the curve inside that range."

Okonkwo: "The high-yield and investment-grade mandates both have a spread duration of 4.2, so the family office can treat them as carrying the same credit spread risk."

Okonkwo also notes that the family office's advisers are used to bank risk reports expressed in currency units at 99% confidence, and he asks Fontaine to explain Oakhurst's convention of reporting risk as a percentage of assets and relative to benchmarks.

### Questions

1. Based on Exhibit 1, the global equity mandate's annualized ex ante tracking error is closest to: (LOS: los-09-05-e)
   - A. 2.10%.
   - B. 2.20%.
   - C. 5.59%.
2. Using the sensitivities in Exhibit 2, the estimated change in the value of the balanced account under the family office's scenario is closest to: (LOS: los-09-05-g)
   - A. a loss of USD 44.1 million.
   - B. a loss of USD 47.3 million.
   - C. a loss of USD 47.6 million.
3. Regarding the statements on sensitivity reports, which is correct? (LOS: los-09-05-i)
   - A. Fontaine's statement only.
   - B. Okonkwo's statement only.
   - C. Both statements.
4. The response to the committee chair's request that Fontaine should give is closest to: (LOS: los-09-05-a)
   - A. USD 44.7 million; the mandate should be expected to underperform its benchmark by at least this amount in about one year in 20.
   - B. USD 73.8 million; this is the maximum amount by which the mandate should be expected to underperform its benchmark in 19 years out of 20.
   - C. USD 73.8 million; the mandate should be expected to underperform its benchmark by at least this amount in about one year in 20.

## Item set 3 (07-02): Tasman Hardwood Imports: Currency Options on a Euro Invoice

Source: [[IS-07-Derivatives-LM02-M05]], difficulty 3.

### Vignette

Liam Kovac, CFA, is a treasury analyst at Tasman Hardwood Imports, an Australian company that reports in Australian dollars (AUD).
Tasman has ordered kiln-drying equipment from a German manufacturer and must pay EUR 3,000,000 in six months.
The chief financial officer, Ruth Delaney, wants to cap the AUD cost of the invoice while keeping the benefit if the euro weakens.
Kovac has obtained quotes from Jonah Whitford, a derivatives salesperson at Coral Sea Bank, for six-month European call options on the euro covering the full invoice.
All interest rates in Exhibit 1 are annualized and continuously compounded.

**Exhibit 1: EUR option inputs**

| Item | Value |
|---|---|
| Spot exchange rate | AUD 1.6500 per EUR |
| Exercise price | AUD 1.6800 per EUR |
| Time to expiration | 0.50 years |
| AUD risk-free rate | 4.10% |
| EUR risk-free rate | 2.30% |
| Six-month forward exchange rate | AUD 1.6649 per EUR |
| Implied volatility used in the model | 9.0% |
| Historical volatility, past 12 months | 11.0% |
| $N(d_1)$ at 9.0% volatility | 0.4562 |
| $N(d_2)$ at 9.0% volatility | 0.4311 |

Kovac values the options with the Black-Scholes-Merton (BSM) model adjusted for the carry benefit of the underlying currency.
Delaney asks him to express the option position as an equivalent combination of euro holdings and AUD money-market borrowing or lending, because Tasman's board approves only hedges it can describe in cash terms.
She adds that any euros in such a portfolio would be held on deposit at the EUR risk-free rate until the invoice date.

In a memo dated 11 August, Kovac makes three statements about the model.

- Statement 1: "BSM assumes that the AUD/EUR exchange rate follows geometric Brownian motion, so its continuously compounded returns are normally distributed and the rate does not jump."
- Statement 2: "BSM treats the interest earned on euro holdings as a yield paid continuously at a constant rate, which is why the EUR rate enters the model as the carry benefit."
- Statement 3: "Because BSM allows volatility to change over the option's life, we can use today's 9.0% implied volatility even though historical volatility has been 11.0%."

Delaney questions whether the forward rate in Exhibit 1 should replace the spot rate in the model.
Kovac answers that the spot rate and the two interest rates already imply that forward rate, so the carry-adjusted BSM model uses the spot rate directly.

On 12 August, Whitford tells Kovac that Coral Sea Bank also writes the matching European put on the euro, with the same exercise price and expiry.
He notes that the bank's risk team hedges its written options in delta terms, and he asks Kovac to confirm the delta of one matching put from Exhibit 1.
Whitford also says that a rise in the EUR interest rate would, other things equal, lower the value of Tasman's calls.

### Questions

1. The BSM value of calls on EUR 3,000,000 is closest to: (LOS: los-07-02-h)
   - A. AUD 64,468.
   - B. AUD 103,713.
   - C. AUD 129,534.
2. The portfolio that replicates Tasman's call position is closest to: (LOS: los-07-02-g)
   - A. buy EUR 1,352,951 and borrow AUD 2,128,656.
   - B. buy EUR 1,352,951 and borrow AUD 2,147,901.
   - C. buy EUR 1,368,600 and borrow AUD 2,128,656.
3. Which of Kovac's statements is inconsistent with the assumptions of the BSM model? (LOS: los-07-02-f)
   - A. Statement 1.
   - B. Statement 2.
   - C. Statement 3.
4. The delta of one matching European put on the euro is closest to: (LOS: los-07-02-k)
   - A. -0.5376.
   - B. -0.5438.
   - C. -0.5490.

## Item set 4 (01-03): Halvorsen Bulk Carriers Freight Exposure Model

Source: [[IS-01-Quantitative-Methods-LM03-M05]], difficulty 4.

### Vignette

Skerry Point Capital is a hedge fund that trades listed shipping equities.
On 2 February 2026, portfolio manager Anders Viklund asks analyst Mei-Lin Castellanos, CFA, to estimate the sensitivity of Halvorsen Bulk Carriers (HBC), an Oslo-listed dry-bulk shipowner, to dry-bulk freight rates.
Viklund plans to hedge the fund's HBC position with freight futures in proportion to that sensitivity, so he wants an estimate whose significance he can trust.
The fund's risk committee approves a hedge ratio only if it rests on a coefficient that is significant at the 5% level in a two-tailed test.
The committee also requires standard errors that are robust to every violation diagnosed in the model, and it prefers the simplest specification consistent with economic reasoning.

Castellanos uses monthly data from January 2017 through December 2025.
Model 1 regresses HBC's monthly excess return (%) on the market excess return (MKT, %), the monthly percentage change in the Baltic Dry Index (BDI), and the monthly percentage change in the bunker fuel price (FUEL).
No lagged value of HBC's return is used as a regressor.

**Exhibit 1: Model 1 estimates**

| Variable | Coefficient | OLS standard error | White standard error | Newey-West standard error |
|---|---|---|---|---|
| Intercept | 0.2100 | 0.7310 | 0.7420 | 0.7960 |
| MKT | 1.1800 | 0.1420 | 0.1760 | 0.2010 |
| BDI | 0.2150 | 0.0420 | 0.0512 | 0.0588 |
| FUEL | -0.1640 | 0.0710 | 0.0830 | 0.0940 |

| ANOVA | df | Sum of squares |
|---|---|---|
| Regression | 3 | 5,168.9 |
| Residual | 104 | 5,832.4 |
| Total | 107 | 11,001.3 |

A plot of the Model 1 residuals against BDI shows the spread of the residuals widening in months with large freight rate moves.
Castellanos squares the Model 1 residuals and regresses them on MKT, BDI, and FUEL.

**Exhibit 2: ANOVA of the regression of squared Model 1 residuals on MKT, BDI, and FUEL**

| Source | df | Sum of squares |
|---|---|---|
| Regression | 3 | 9,406.0 |
| Residual | 104 | 106,437.0 |
| Total | 107 | 115,843.0 |

She also computes the sum of squared differences between successive Model 1 residuals, $\sum_{t=2}^{n}(\hat{u}_t - \hat{u}_{t-1})^2 = 11{,}256.5$.
Because dry-bulk freight follows seasonal patterns tied to the Chinese New Year and the South American grain harvest, she also runs a Breusch-Godfrey test with 12 lags on the Model 1 residuals, which gives an F-statistic of 2.31.

Viklund suggests adding the monthly percentage change in the Baltic Capesize Index (CAPE), noting that Capesize vessels make up most of HBC's fleet.
Castellanos points out that the Capesize rate is one of the components from which the BDI is calculated.
She nevertheless estimates Model 2, which adds CAPE to the three Model 1 regressors, and summarizes both models in Exhibit 3.
The pairwise correlation between BDI and CAPE over the sample is 0.95.

**Exhibit 3: Model comparison**

| Statistic | Model 1 | Model 2 |
|---|---|---|
| $R^2$ | 0.4698 | 0.4712 |
| Adjusted $R^2$ | 0.4546 | 0.4507 |
| BDI coefficient | 0.2150 | 0.1320 |
| BDI OLS standard error | 0.0420 | 0.1383 |
| BDI Newey-West standard error | 0.0588 | 0.1936 |
| $R^2$ of BDI regressed on the other regressors | 0.300 | 0.935 |

**Exhibit 4: Selected critical values**

| Distribution | Value |
|---|---|
| Chi-square, 3 df, upper 5% | 7.815 |
| Chi-square, 4 df, upper 5% | 9.488 |
| Chi-square, 3 df, upper 1% | 11.345 |
| F(12, 92), upper 5% | 1.859 |
| F(3, 92), upper 5% | 2.704 |
| t, 103 or 104 df, two-tailed 5% | 1.983 |

At a meeting on 9 February 2026, Viklund states: "Model 2 is the one to hedge with. Capesize exposure drives HBC's earnings, and once CAPE is in the model the BDI coefficient is no longer significant, so the broad index is not the exposure we should hedge."

### Questions

1. The Breusch-Pagan test statistic for Model 1 and the conclusion at the 5% significance level are closest to: (LOS: los-01-03-b)
   - A. 3.06; there is no evidence of conditional heteroskedasticity.
   - B. 8.77; there is evidence of conditional heteroskedasticity.
   - C. 8.77; there is no evidence of conditional heteroskedasticity.
2. The Durbin-Watson statistic for Model 1 and the most appropriate conclusion about serial correlation are: (LOS: los-01-03-c)
   - A. 1.93; the residuals show no serial correlation, so the OLS standard errors of Model 1 are reliable.
   - B. 1.93; serial correlation up to lag 12 is present even though first-order autocorrelation is negligible, so Newey-West standard errors should be used and the coefficient estimates remain consistent.
   - C. 1.02; strong positive first-order serial correlation makes the Model 1 coefficient estimates inconsistent.
3. The variance inflation factor of BDI in Model 2 and, holding the MSE and the sample variance of BDI constant, the factor by which the OLS standard error of the BDI coefficient rises from Model 1 to Model 2 are closest to: (LOS: los-01-03-d)
   - A. 10.26 and 2.68.
   - B. 15.38 and 3.28.
   - C. 15.38 and 10.77.
4. To decide whether HBC has a significant BDI exposure to hedge, the specification, standard errors, and conclusion most consistent with avoiding model misspecification are: (LOS: los-01-03-a)
   - A. Model 2 with Newey-West standard errors; $t = 0.68$, so HBC has no significant BDI exposure.
   - B. Model 1 with Newey-West standard errors; $t = 3.66$, so the BDI exposure is significant.
   - C. Model 1 with White standard errors; $t = 4.20$, so the BDI exposure is significant.

## Item set 5 (06-02): Okonkwo Family Office: Step-Up Note Paths

Source: [[IS-06-Fixed-Income-LM02-M05]], difficulty 3.

### Vignette

Hana Sato, CFA, is an investment analyst at the Okonkwo Family Office, which manages the fixed-income wealth of a multigenerational family.
The office is considering a three-year, option-free step-up note issued by a supranational development bank whose debt trades on the government benchmark curve.
The note pays annual coupons of 2.00% in Year 1, 3.00% in Year 2, and 4.50% in Year 3, and repays 100 of par at maturity.

Sato receives a lognormal binomial interest rate tree from a pricing vendor.
The vendor states that the tree is calibrated to the annual-pay benchmark par curve of 1.80% (1 year), 2.30% (2 years), and 2.65% (3 years), but the file omits the volatility assumption.

Exhibit 1: Vendor tree of one-year forward rates

| Time 0 | Time 1 | Time 2 |
|---|---|---|
| 1.8000% | 3.2072% | 4.3986% |
| | 2.4239% | 3.3244% |
| | | 2.5125% |

Sato labels each path by the sequence of up (H) and down (L) moves after Time 0.
For example, path HL takes the higher rate at Time 1 and then moves down to the middle rate at Time 2, while path LH takes the lower rate at Time 1 and then moves up to the middle rate at Time 2.

Exhibit 2: Rates along each path

| Path | Time 0 | Time 1 | Time 2 |
|---|---|---|---|
| HH | 1.8000% | 3.2072% | 4.3986% |
| HL | 1.8000% | 3.2072% | 3.3244% |
| LH | 1.8000% | 2.4239% | 3.3244% |
| LL | 1.8000% | 2.4239% | 2.5125% |

Sato's first task is to recover the volatility assumption embedded in the vendor tree, because the family office's policy requires it to be documented.
Her second task is to value the step-up note pathwise and to confirm the result against backward induction.

Pieter de Wit, the family office's external fixed-income adviser, reviews the vendor's calibration method with Sato and makes two statements.

Statement 1: "To calibrate Time 2, the vendor holds the Time 1 rates fixed at their calibrated values, sets the other Time 2 rates as multiples of the lowest rate using the lognormal spacing, and adjusts the lowest rate until the three-year benchmark par bond is valued at exactly 100."

Statement 2: "If the vendor recalibrated the tree with a higher volatility assumption, the lower rate at Time 1 would rise, because both Time 1 rates must move up to offset the wider spread."

The family office also holds a small position in agency collateralized mortgage obligations.
For those securities the vendor uses a Monte Carlo forward-rate simulation, and de Wit makes two further statements.

Statement 3: "Modelers often impose mean reversion on simulated rates by setting upper and lower bounds on the rate process."

Statement 4: "To make the simulation arbitrage free, the vendor adjusts the rates on each path separately so that every individual path prices the benchmark bonds at their market values."

Sato records her conclusions in the family office's investment committee memo.

### Questions

1. The volatility assumption embedded in the vendor tree is closest to: (LOS: los-06-02-c)
   - A. 28.0%.
   - B. 16.2%.
   - C. 14.0%.
2. The present value of the step-up note's cash flows along path HL is closest to: (LOS: los-06-02-g)
   - A. 99.5155.
   - B. 101.0822.
   - C. 101.8402.
3. Which of de Wit's statements about calibration is correct? (LOS: los-06-02-d)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.
4. Which of de Wit's statements about Monte Carlo simulation is correct? (LOS: los-06-02-h)
   - A. Statement 4 only.
   - B. Statement 3 only.
   - C. Both Statement 3 and Statement 4.

## Item set 6 (10-01): Kestrel Ridge Advisors: Auditing a Prospect Pitch Book

Source: [[IS-10-Ethics-LM01-M05]], difficulty 4.

### Vignette

Grace Mbeki, CFA, is chief compliance officer of Kestrel Ridge Advisors, a Toronto investment adviser that manages discretionary Canadian equity accounts for professionals and small foundations.
Kestrel's founding partner, Omar Haddad, CFA, asked Leah Fournier, a CFA Level III candidate and associate portfolio manager who reports to him, to draft a pitch book for prospective clients.
Before the pitch book is printed, Mbeki reviews it against the CFA Institute Code of Ethics and Standards of Professional Conduct.

**Exhibit 1: Canadian equity accounts managed by Kestrel, calendar year 20X5**

| Account | Beginning market value (CAD millions) | Return, 20X5 | Status |
|---|---|---|---|
| A | 42.0 | 13.5% | Open |
| B | 28.0 | 15.2% | Open |
| C | 18.0 | 11.8% | Open |
| D | 7.0 | -6.4% | Terminated by the client on 31 December 20X5 |
| E | 5.0 | -9.0% | Terminated by the client on 31 December 20X5 |
| Model portfolio | 0.0 | 19.0% | Hypothetical; no client assets |
| Benchmark, broad Canadian equity index | n/a | 10.4% | Benchmark |

All five client accounts followed the same strategy and were under Kestrel's management for the whole of 20X5.
The pitch book states: "Kestrel's Canadian equity strategy returned 13.7% in 20X5, beating the benchmark by 3.3 percentage points."
Fournier's working file shows that she weighted each account by its beginning market value and left out Accounts D and E "because they are no longer clients".

**Exhibit 2: Other pitch book content**

| Item | Content |
|---|---|
| 1 | "Every Kestrel partner holds the CFA charter, a credential that ensures our clients earn superior returns." |
| 2 | A two-page description of the "Kestrel Quality Screen" as a model developed in-house; the screen and most of its wording were copied, without attribution, from a report published by an unrelated brokerage firm |
| 3 | A welcome page for prospective clients introduced by Northway Tax Partners, an accounting firm; the pitch book does not mention that Kestrel pays Northway CAD 1,500 for each client it introduces |
| 4 | A "Code of Ethics" page quoting two principles of the CFA Institute Code of Ethics, shown below as Quotations X and Y |

Northway introduced 11 new clients to Kestrel in 20X5.

Quotation X: "Place the integrity of the investment profession and the interests of clients above their own personal interests."

Quotation Y: "Use reasonable care and exercise independent professional judgment when conducting investment analysis and making investment recommendations."

Kestrel's outside counsel has confirmed that provincial securities rules do not require an adviser to disclose payments to parties that introduce clients.
Haddad and Mbeki discuss Exhibit 2 on 9 February.

Haddad (9 February): "Items 1 and 2 most directly engage the same sub-standard, Standard I(C) Misrepresentation, because both overstate what Kestrel offers."

Mbeki (9 February): "Even though provincial rules are silent, the Northway payments in Item 3 must be disclosed to prospective clients, because where the Standards are stricter than the law, members and candidates follow the Standards."

Haddad ends the meeting by saying that because Fournier drafted the pitch book, any disciplinary exposure is hers alone.
He adds that, as a candidate rather than a charterholder, she could face at most a public censure.
Mbeki replies that the Code and Standards bind both of them individually, and she asks Fournier to recompute the performance figure before the pitch book goes to print.

### Questions

1. Using Exhibit 1, the 20X5 return that would make the pitch book's performance figure fair, accurate, and complete is closest to: (LOS: los-10-01-a)
   - A. 5.02%.
   - B. 11.15%.
   - C. 11.59%.
2. Regarding the 9 February statements, which is most likely correct? (LOS: los-10-01-a)
   - A. Haddad's statement only.
   - B. Mbeki's statement only.
   - C. Both statements.
3. Regarding Quotations X and Y on the pitch book's Code of Ethics page, which statement is most accurate? (LOS: los-10-01-a)
   - A. Both quotations are complete statements of Code of Ethics principles.
   - B. Quotation X is complete; Quotation Y omits "taking investment actions, and engaging in other professional activities".
   - C. Quotation X is incomplete because it omits the interests of employers; Quotation Y is complete.
4. Assume Haddad and Fournier each reject charges proposed by Professional Conduct staff and a Disciplinary Review Committee panel finds that each violated the Code and Standards. The sanctions available to the panel are best described as: (LOS: los-10-01-b)
   - A. Haddad: public censure, suspension of membership and use of the CFA designation, or revocation of the charter; Fournier: suspension or prohibition from further participation in the CFA Program.
   - B. Haddad: public censure, suspension of membership and use of the CFA designation, or revocation of the charter; Fournier: public censure at most, as Haddad states.
   - C. Haddad: none, because only the member who drafted the pitch book can be sanctioned; Fournier: revocation of the CFA charter once she earns it.

## Item set 7 (09-02): Tidemark Reinsurance: Rebuilding the Active Equity Line-Up

Source: [[IS-09-Portfolio-Management-LM02-M05]], difficulty 4.

### Vignette

Oluwaseun Adeyemi, CFA, is a senior analyst in the investment office of Tidemark Reinsurance.
Tidemark's surplus portfolio holds a global developed-market equity allocation, currently a single index fund that replicates the benchmark.
Beatriz Montalvo, the chief investment officer, has asked Adeyemi to choose one external active manager for the allocation and to evaluate an in-house systematic sleeve.
Tidemark may hold the index fund long or short through futures.

The benchmark's expected return is 8.46%, its volatility is 15.5%, and the risk-free rate is 3.50%, giving a benchmark Sharpe ratio of 0.32.
Adeyemi assumes that every manager's active returns are uncorrelated with benchmark returns and that every portfolio has a benchmark beta of 1.

Exhibit 1: Candidate managers

| | Cobalt Ridge | Larchmont Sector | Pinecrest Quant |
|---|---|---|---|
| Strategy | Long-short country pairs | Industry rotation | Stock selection |
| Number of positions | 12 pairs | 20 industries | 500 stocks |
| Average pairwise correlation of active returns | -0.06 | 0.20 | 0.00 |
| Forecast and rebalancing cycle | Annual | Quarterly | Monthly |
| Information coefficient | 0.06 | 0.08 | 0.015 |
| Transfer coefficient | 0.85 | 0.75 | 0.65 |
| Delivered active risk | 5.0% | 6.5% | 3.5% |
| Realized 3-year information ratio | 0.21 | 0.38 | 0.12 |

Adeyemi's due diligence adds three facts.
Larchmont's quarterly forecasts come from a fresh industry survey each quarter, and successive quarterly forecasts are uncorrelated.
Pinecrest's pitch book reports breadth of $500 \times 12 = 6{,}000$, but its composite valuation score changes very little from month to month, and Adeyemi estimates that each stock's score has a month-to-month correlation above 0.95.
Cobalt Ridge's pairs are built so that the active returns of different pairs are mildly negatively correlated.

Montalvo notes on 2 June 2026 that, to keep the mandate simple, Tidemark may initially hold the chosen manager on its own, at its delivered active risk, with no position in the index fund.

Montalvo adds that Tidemark's board is considering new country position caps for any external mandate.
Cobalt Ridge estimates that, under those caps, its transfer coefficient would fall from 0.85 to 0.55, with no change to its information coefficient or breadth.

The in-house sleeve is an unconstrained long-short strategy, so Adeyemi treats its transfer coefficient as 1.00.
It selects among 225 stocks with uncorrelated active returns and annual independent forecasts.
Its expected information coefficient is 0.04, and the standard deviation of its realized annual information coefficient over the past 15 years is 0.10.
Tidemark's risk model predicts an active risk of 2.0% for the sleeve.
The sleeve's realized information coefficient last year was 0.07.

Adeyemi plans to report the sleeve using the strategy-risk refinement of Qian and Hua, because the naive fundamental law ignores uncertainty about the information coefficient.
Montalvo remarks that the committee has seen naive fundamental-law estimates overstate realized information ratios before, and she wants a figure that allows for that.

### Questions

1. Based on Exhibit 1 and the due diligence findings, the manager with the highest expected information ratio is: (LOS: los-09-02-e)
   - A. Cobalt Ridge.
   - B. Larchmont Sector.
   - C. Pinecrest Quant.
2. If Tidemark holds the manager selected in Question 1 on its own, at its delivered active risk, the expected Sharpe ratio of the equity allocation is closest to: (LOS: los-09-02-d)
   - A. 0.316.
   - B. 0.398.
   - C. 0.441.
3. If the board adopts the position caps, the maximum Sharpe ratio Tidemark can achieve by optimally combining Cobalt Ridge with the index fund is closest to: (LOS: los-09-02-c)
   - A. 0.361.
   - B. 0.375.
   - C. 0.415.
4. After allowing for strategy risk, the in-house sleeve's expected active risk and expected information ratio are closest to: (LOS: los-09-02-f)
   - A. 2.0% and 0.60.
   - B. 3.0% and 0.60.
   - C. 3.0% and 0.40.

## Item set 8 (02-01): Lindenhof Macro Rand Carry Post-Mortem

Source: [[IS-02-Economics-LM01-M05]], difficulty 3.

### Vignette

Lindenhof Macro is a Frankfurt-based hedge fund that reports in euros (EUR).
One year ago, portfolio manager Johanna Richter opened a carry trade that borrowed EUR for one year and invested the proceeds in one-year South African rand (ZAR) deposits.
The position was unwound today, and Richter has asked analyst Thabo Nkosi to prepare a post-mortem for the investment committee.
The fund's systems carry no direct ZAR/EUR history, so Nkosi must work from the dealer rates in Exhibit 1.

**Exhibit 1: Spot Rates (mid-market)**

| Currency pair | At initiation | Today (unwind) |
|---|---|---|
| ZAR/USD | 17.85 | 19.62 |
| USD/EUR | 1.0820 | 1.1040 |
| JPY/USD | 149.30 | 142.10 |

**Exhibit 2: One-Year Deposit Rates at Initiation**

| Currency | Rate |
|---|---|
| ZAR | 8.25% |
| USD | 5.05% |
| EUR | 3.40% |
| JPY | 0.20% |

For nine months the trade performed as expected, and the rand strengthened modestly against the euro.
In the final quarter, a spike in global volatility triggered a rush of leveraged investors out of high-yield currencies, and the rand fell sharply before the position could be closed.

Nkosi also assembles the South African balance of payments data in Exhibit 3.

**Exhibit 3: South Africa, Selected External Accounts (% of GDP)**

| Item | Prior year | Holding year |
|---|---|---|
| Current account balance | -1.6% | -3.9% |
| Net foreign portfolio inflows | +2.1% | +5.4% |
| External debt | 41% | 44% |

Most of the portfolio inflows went into rand-denominated government bonds.
In a draft of the post-mortem, Nkosi writes: "The rand strengthened during the first nine months even though the current account deficit more than doubled, which shows that the current account has no bearing on the value of the rand."
Richter asks him to replace that sentence with an explanation that is consistent with the curriculum's view of how balance of payments flows affect exchange rates.

Richter also wants a long-run fair value estimate before she decides whether to re-enter the trade.
A 2014 study commissioned by the fund concluded that the rand was at its purchasing power parity value against the euro in 2014, at ZAR/EUR 14.40.
Since then, the South African consumer price index has risen from 100.0 to 162.8, and the euro area index has risen from 100.0 to 128.6.
Nkosi is asked to express the rand's misvaluation today as the percentage by which its market value in EUR differs from its PPP value in EUR.

Finally, two policy announcements were made this morning.
The European Central Bank cut its policy rate by 50 basis points, while euro area finance ministers committed to a joint programme of fiscal consolidation.
The South African Reserve Bank raised its repo rate by 75 basis points, while the South African Treasury announced a multi-year infrastructure programme financed by government bond issuance.
Nkosi notes that both economies have floating exchange rates and allow capital to move freely.
Richter asks for the most likely short-run effect of the two sets of announcements on the ZAR/EUR rate.
She adds that she will consider the long-run implications of South Africa's rising debt separately.

### Questions

1. The realized all-in return on the EUR-funded rand carry trade, net of the funding cost, is closest to: (LOS: los-02-01-i)
   - A. -3.48%.
   - B. -4.92%.
   - C. -6.88%.
2. Based on relative purchasing power parity, the rand today is best described as: (LOS: los-02-01-h)
   - A. undervalued by about 15.8%.
   - B. undervalued by about 10.8%.
   - C. overvalued by about 18.8%.
3. The explanation that Nkosi should most appropriately substitute for the sentence in his draft is that: (LOS: los-02-01-j)
   - A. a current account deficit raises the demand for the deficit country's currency, so the rand's strength was the expected result of the wider deficit.
   - B. investment and financing flows dominate exchange rate movements in the short run because asset prices and portfolio allocations adjust quickly, while trade flows adjust with long lags, so a persistent deficit weighs on the currency mainly over the long run.
   - C. rising external debt raises the market's estimate of a deficit country's long-run equilibrium exchange rate, which supported the rand during the first nine months.
4. Under the Mundell-Fleming model, the most likely short-run effect of this morning's announcements on the ZAR/EUR rate is that it will: (LOS: los-02-01-k)
   - A. rise.
   - B. fall.
   - C. move in an indeterminate direction.

## Item set 9 (01-07): Larkspur Equity Restaurant Sales Beat Model

Source: [[IS-01-Quantitative-Methods-LM07-M05]], difficulty 3.

### Vignette

Larkspur Equity Partners runs a long-only consumer fund with a large allocation to listed North American restaurant chains.
Portfolio manager Adaeze Nwankwo has asked analyst Tomasz Wierzbicki to build a supervised model that predicts whether a chain's quarterly same-store sales will beat (1) or miss (0) the consensus estimate.
The model combines structured location data with the sentiment of online customer reviews.

Wierzbicki licenses weekly foot traffic counts for 3,900 restaurant locations from a mobile geolocation vendor at a cost of USD 85,000 a year, and he merges them with location-level sales reported by the chains.
While preparing the structured data, he performs four actions:

- Action 1: for each location, he adds dine-in sales, third-party delivery sales, and catering sales into a single total sales variable.
- Action 2: he deletes the rows for 62 locations that closed permanently before the start of the sample period.
- Action 3: he translates the sales of Canadian locations from Canadian dollars into US dollars at each quarter's average exchange rate.
- Action 4: he deletes the street address column because each location already has a unique location ID.

A histogram of weekly foot traffic is close to bell-shaped, and Wierzbicki confirms that no location lies more than three standard deviations from the mean.
He therefore decides to rescale foot traffic to a mean of 0 and a standard deviation of 1 before training.
Summary statistics for the cleansed variable are in Exhibit 1.

**Exhibit 1: Weekly foot traffic per location (visits, n = 3,838)**

| Statistic | Value |
|---|---|
| Mean | 4,820 |
| Median | 4,550 |
| Standard deviation | 1,150 |
| Minimum | 1,610 |
| Maximum | 8,190 |
| Skewness | 0.12 |

One location of the chain Copperkettle Grill records weekly foot traffic of 7,005 visits.

For the text component, Wierzbicki scrapes 186,000 customer reviews from a public review website.
Each review carries a star rating, which he uses to label it positive or negative.
After cleansing, tokenization, lowercasing, and stemming, he ranks candidate tokens for a review sentiment classifier.
For each token he computes the collection-level term frequency and the mutual information between token occurrence and the positive and negative review classes.
Selected results are in Exhibit 2.

**Exhibit 2: Selected stemmed tokens from customer reviews**

| Token | Collection-level term frequency | Mutual information |
|---|---|---|
| order | 0.0184 | 0.0035 |
| food | 0.0096 | 0.0006 |
| friendli | 0.0017 | 0.0412 |
| cold | 0.0021 | 0.0694 |

The classifier's output, a sentiment score for each chain, becomes one feature in the sales beat model.

Wierzbicki trains a logistic regression on the combined features and evaluates it on a holdout test set of 400 chain-quarters.
The results are in Exhibit 3.

**Exhibit 3: Test set confusion matrix (400 chain-quarters)**

| | Actual beat (1) | Actual miss (0) |
|---|---|---|
| Predicted beat (1) | 116 | 44 |
| Predicted miss (0) | 28 | 212 |

On 18 August, Nwankwo describes how the fund will use the model: "We will add to a position only when the model predicts a beat.
The mistake that hurts us is buying a chain ahead of a quarter that turns out to be a miss, because those stocks gap down on the release.
Failing to predict a beat just means we sit out a quarter, and that costs us very little."

### Questions

1. The data transformations in Actions 1, 2, and 3, respectively, are best described as: (LOS: los-01-07-b)
   - A. aggregation, selection, and conversion.
   - B. extraction, filtration, and conversion.
   - C. aggregation, filtration, and conversion.
2. After Wierzbicki's planned rescaling, the foot traffic value for the Copperkettle Grill location is closest to: (LOS: los-01-07-b)
   - A. 0.820.
   - B. 1.900.
   - C. 2.135.
3. Based on Exhibit 2, the token with the greatest power to discriminate between positive and negative reviews is: (LOS: los-01-07-e)
   - A. "food".
   - B. "order".
   - C. "cold".
4. Given Nwankwo's 18 August comments, the performance measure that best reflects the fund's concern, and its value from Exhibit 3, are closest to: (LOS: los-01-07-f)
   - A. precision, 0.725.
   - B. recall, 0.806.
   - C. accuracy, 0.820.

## Item set 10 (04-01): Oriel Packaging: Returning Surplus Cash

Source: [[IS-04-Corporate-Issuers-LM01-M05]], difficulty 3.

### Vignette

Samuel Okafor, CFA, is a portfolio manager at Ferndale Private Wealth in London.
His client Rhian Castell holds 100,000 shares of Oriel Packaging plc, a UK maker of corrugated packaging that reports in British pounds (GBP).
Castell bought the shares several years ago at GBP 12.00 per share.

After several years of strong trading, Oriel has accumulated GBP 90 million of surplus cash that earns close to zero.
The board intends to return the full amount to shareholders early in 2026, after the regular dividend for 2026 has been paid.
It is choosing between a one-time special cash dividend and a repurchase of shares at the current market price.
Exhibit 1 presents data Okafor has gathered.

Exhibit 1: Oriel Packaging, selected data (end of 2025)

| Item | Value |
|---|---|
| Common shares outstanding | 50 million |
| Current share price | GBP 18.00 |
| Trailing price-to-earnings ratio | 12.5 |
| Price-to-book ratio | 0.80 |
| Regular dividend per share | GBP 0.72 |
| Surplus cash to be distributed | GBP 90 million |
| Pretax rate quoted by lenders on a new term loan | 7.2% |
| Corporate tax rate | 25% |

Exhibit 2: Oriel Packaging, forecast for 2026 before any special distribution (GBP millions)

| Item | Value |
|---|---|
| Net income | 72 |
| Cash flow from operations | 121 |
| Fixed capital investment | 58 |
| Net borrowing (repayment) | (17) |
| Regular cash dividends | 36 |

Castell pays tax at 30% on dividends and at 20% on realized capital gains.
Ferndale also manages a charitable foundation that owns Oriel shares and pays no tax.
To compare the two routes for Castell, Okafor assumes that the share price falls by the amount of any special dividend on the ex-dividend date, and that a repurchase at the market price leaves the share price unchanged.
He also assumes Castell tenders her shares pro rata, selling the same fraction of her holding as the fraction of Oriel's shares the company buys back.
He measures her wealth as after-tax cash plus the market value of the shares she keeps, ignoring any tax on gains she has not realized.

Oriel's chief financial officer, Harriet Lindqvist, tells analysts, "Because our shares trade below book value, the repurchase will raise book value per share, and because the cash earns nothing, it will also raise earnings per share."

One director, Paolo Mancuso, asks whether Oriel should go further and repurchase an additional block of shares at the current market price with a new term loan.
He wants to know the highest pretax interest rate on the loan at which such a repurchase, evaluated on its own at the current share price and trailing price-to-earnings ratio, would not reduce earnings per share, assuming net income is otherwise unchanged.

Okafor's colleague Ines Barros is responsible for Ferndale's dividend-safety screens.
She plans to recompute Oriel's 2026 FCFE coverage ratio if the board chooses the repurchase, using the forecasts in Exhibit 2.

### Questions

1. Relative to the special dividend, the repurchase increases Castell's after-tax wealth by an amount closest to: (LOS: los-04-01-l)
   - A. GBP 0.
   - B. GBP 18,000.
   - C. GBP 42,000.
2. If Oriel repurchases shares with the GBP 90 million at the current market price, its book value per share after the repurchase is closest to: (LOS: los-04-01-k)
   - A. GBP 14.00.
   - B. GBP 20.70.
   - C. GBP 23.00.
3. The answer to Mancuso's question is closest to: (LOS: los-04-01-j)
   - A. 6.00%.
   - B. 8.00%.
   - C. 10.67%.
4. If the board chooses the repurchase, Barros's 2026 FCFE coverage ratio for Oriel is closest to: (LOS: los-04-01-m)
   - A. 0.37.
   - B. 0.63.
   - C. 1.28.

## Item set 11 (03-03): Northmark Agri-Equipment Nordic and Arvenia Units

Source: [[IS-03-Financial-Statement-Analysis-LM03-M05]], difficulty 3.

### Vignette

Northmark Agri-Equipment Ltd. is a Canadian manufacturer of tractors and harvesting equipment.
It reports under US GAAP with the Canadian dollar (CAD) as its presentation currency, and its fiscal year ends on 31 December.
Samuel Okonjo, CFA, a buy-side analyst at Birchfield Asset Management, is reviewing two of Northmark's foreign subsidiaries.

Northmark Nordic AB, based in Gothenburg, keeps its accounting records in Swedish kronor (SEK).
It imports finished machines from Northmark's Canadian plants under invoices denominated in CAD and resells them to Scandinavian dealers.
Its selling prices are set from Northmark's CAD price list, converted at the monthly rate, and Nordic has no production of its own.
Nordic remits its cash to the parent every week and is financed entirely by intercompany advances from the parent.

Northmark Arvenia S.A. assembles and sells equipment in the Republic of Arvenia under its own management, using the Arvenian lira (ARL).
It sets prices in ARL against local competitors, pays its staff and suppliers in ARL, and borrows from Arvenian banks.
Arvenia's cumulative inflation over 2023 to 2025 exceeded 100%, and Northmark's auditors have confirmed that the economy is highly inflationary.

At a Birchfield research meeting on 16 February 2026, Okonjo's colleague Ingrid Solheim comments on the two units.

Solheim: "Nordic is a Swedish company that keeps its books in kronor, so it must be translated with the current rate method. Arvenia is autonomous, so its local currency is its functional currency, but because it is hyperinflationary Northmark first restates its statements for inflation and then translates them at the current rate."

**Exhibit 1: Northmark Nordic sales and exchange rates**

| Item | 2024 | 2025 |
|---|---|---|
| Sales (SEK millions) | 480 | 516 |
| Average rate (CAD per SEK) | 0.1290 | 0.1245 |
| Year-end rate (CAD per SEK) | 0.1270 | 0.1230 |

**Exhibit 2: Northmark Arvenia balance sheet, 31 December 2025 (ARL millions)**

| Assets | | Liabilities and equity | |
|---|---|---|---|
| Cash | 12 | Accounts payable | 10 |
| Accounts receivable | 18 | Bank loan | 55 |
| Inventory | 25 | Common stock | 50 |
| Equipment, net | 72 | Retained earnings | 12 |
| Total | 127 | Total | 127 |

Arvenia's cash, receivables, payables and bank loan were at the same levels on 1 January 2025 and changed little during the year.
The equipment was bought on 1 January 2024 for ARL90 million and is depreciated straight-line over ten years with no residual value.

**Exhibit 3: Arvenia general price index and exchange rates**

| Date or period | General price index | CAD per ARL |
|---|---|---|
| 1 January 2024 | 100 | 0.0800 |
| 31 December 2024 | 150 | 0.0500 |
| Average 2025 | 180 | 0.0400 |
| 31 December 2025 | 240 | 0.0320 |

Okonjo is also building a comparison with an IFRS peer whose hyperinflationary subsidiary holds similar equipment.
He wants to know how much of Nordic's growth came from Scandinavian demand and how much from the currency, and how the Arvenian equipment would be carried and expensed under each set of standards.

### Questions

1. Under Northmark's reporting framework, the methods Northmark should apply to Northmark Nordic and Northmark Arvenia, respectively, are: (LOS: los-03-03-a)
   - A. the current rate method for Nordic and the temporal method for Arvenia.
   - B. the temporal method for Nordic, and inflation restatement followed by the current rate method for Arvenia.
   - C. the temporal method for both subsidiaries.
2. Northmark Nordic's 2025 sales growth as reported in CAD, and the foreign exchange component of that growth, are closest to: (LOS: los-03-03-c)
   - A. 3.75%, of which -3.75 percentage points is foreign exchange.
   - B. 3.75%, of which -3.49 percentage points is foreign exchange.
   - C. 7.50%, of which 0.00 percentage points is foreign exchange.
3. The 2025 result on Northmark Arvenia's net monetary position included in Northmark's consolidated statements is closest to: (LOS: los-03-03-g)
   - A. a gain of CAD180,000 in net income.
   - B. a gain of CAD630,000 in net income.
   - C. a gain of CAD630,000 in other comprehensive income.
4. The 2025 depreciation expense on the Arvenian equipment in Northmark's consolidated statements, and the amount the IFRS peer would report for identical equipment in an identical subsidiary, are closest to: (LOS: los-03-03-g)
   - A. CAD288,000 and CAD691,200.
   - B. CAD720,000 and CAD384,000.
   - C. CAD720,000 and CAD691,200.

## Session 2

## Item set 12 (04-04): Vantorra Industrie Spin Off of Quellis Sensing

Source: [[IS-04-Corporate-Issuers-LM04-M05]], difficulty 3.

### Vignette

Ingrid Halvorsen, CFA, is a portfolio manager at Skerry Capital, which holds shares of Vantorra Industrie SE, a German maker of industrial valves and pumps with a fast-growing sensor business.
On 20 May 2026, Vantorra announced that it will spin off its Sensing segment as Quellis Sensing AG, a separately listed company.
Vantorra shareholders will receive one Quellis share for every three Vantorra shares they hold.
Before the distribution, Quellis will borrow EUR800 million and pay the full amount to Vantorra as a special dividend, and Vantorra will use it to repay part of its 5.0% debt.
Quellis will start with no cash, and all of Vantorra's current cash will stay with Vantorra.
Management expects the separation to be completed in the first quarter of 2027.
Vantorra shares rose 9% on the announcement day and closed at EUR14.00.

**Exhibit 1: Vantorra segment data, next twelve months (EUR millions)**

| Segment | Revenue | EBITDA | D&A | Revenue growth |
|---|---|---|---|---|
| Flow Control | 3,100 | 520 | 120 | 2% |
| Sensing | 900 | 180 | 50 | 14% |

Unallocated corporate costs are EUR60 million a year.
Vantorra has 240 million shares outstanding, total debt of EUR3,000 million at 5.0%, and cash of EUR200 million earning 2.0%; its tax rate is 25%.
After the separation, Quellis will need its own corporate functions, costing EUR18 million a year.
Only EUR8 million of Vantorra's corporate costs will disappear, so Vantorra will keep EUR52 million.

**Exhibit 2: Listed sensing companies**

| Company | EV/EBITDA | Revenue growth |
|---|---|---|
| Sensor peer 1 | 10.5x | 4% |
| Sensor peer 2 | 12.0x | 7% |
| Sensor peer 3 | 14.5x | 10% |
| Sensor peer 4 | 17.0x | 13% |
| Sensor peer 5 | 19.5x | 16% |

**Exhibit 3: Other valuation data**

| Item | Value |
|---|---|
| Median EV/EBITDA, listed flow control companies | 9.0x |
| Median EV/EBITDA, completed acquisitions of sensing businesses, 2022-2025 | 18.2x |

Halvorsen values each company after the separation on its next-twelve-month EBITDA net of its own corporate costs.
She applies the median EV/EBITDA multiple of the listed companies in its industry.
She works on a full-year basis, as if the special dividend, the debt repayment, and the distribution had already occurred.

Halvorsen reviews the announcement with a junior analyst, Tomas Brandt, who drafts three conclusions for her investment committee memo.
The first is that the 9% share price gain on the announcement day shows the spin off will create long-term value for Vantorra shareholders.
The second is that Vantorra's current share price should already reflect the expected impact of the spin off, adjusted for the risk that it is not completed.
The third is that the spin off is less likely than a sale of Sensing to a competitor to close on schedule, because spin offs attract greater antitrust scrutiny.

### Questions

1. Halvorsen's estimate of Quellis's enterprise value is closest to: (LOS: los-04-04-c)
   - A. EUR2,349 million.
   - B. EUR2,610 million.
   - C. EUR2,948 million.
2. Halvorsen's estimate of the combined value, per Vantorra share held today, of one Vantorra share after the separation plus the Quellis shares distributed on it is closest to: (LOS: los-04-04-f)
   - A. EUR12.34.
   - B. EUR15.67.
   - C. EUR19.00.
3. Vantorra's pro forma EPS for the first full year after the separation is closest to: (LOS: los-04-04-d)
   - A. EUR0.63.
   - B. EUR0.76.
   - C. EUR1.13.
4. Which of Brandt's conclusions about the initial evaluation of the spin off is most accurate? (LOS: los-04-04-b)
   - A. The first conclusion.
   - B. The second conclusion.
   - C. The third conclusion.

## Item set 13 (06-04): Fenwick Mutual: Migration Drag Across the Maturity Spectrum

Source: [[IS-06-Fixed-Income-LM04-M05]], difficulty 3.

### Vignette

Ruth Okonkwo, CFA, is a fixed-income analyst at Fenwick Mutual Insurance, a property and casualty insurer with a large portfolio of investment-grade corporate bonds.
The chief investment officer, Paolo Grieco, is deciding where on the maturity curve to place a new allocation to Tarrant Chemicals, an issuer currently rated BBB.
Tarrant has two senior unsecured bonds outstanding, and Okonkwo compares them over a one-year horizon.

Exhibit 1: Tarrant Chemicals bonds

| Bond | Maturity | Yield to maturity | Expected modified duration at the one-year horizon | Coupon |
|---|---|---|---|---|
| S | 5 years | 4.60% | 3.70 | 4.25% |
| L | 10 years | 5.05% | 7.30 | 4.75% |

Okonkwo uses the one-year transition probabilities for BBB issuers in Exhibit 2 and the credit spreads by rating and maturity bucket in Exhibit 3.
She assumes that the Exhibit 3 spreads apply at the one-year horizon and that each bond's current spread equals the BBB spread for its maturity bucket.
Fenwick's policy ignores the probability of default in migration calculations for investment-grade bonds.

Exhibit 2: One-year transition probabilities from BBB (%)

| AAA | AA | A | BBB | BB | B | CCC, CC, C | D |
|---|---|---|---|---|---|---|---|
| 0.02 | 0.35 | 5.20 | 86.10 | 5.80 | 1.40 | 0.83 | 0.30 |

Exhibit 3: Credit spreads by rating and maturity bucket

| Rating | AAA | AA | A | BBB | BB | B | CCC, CC, C |
|---|---|---|---|---|---|---|---|
| Five-year bucket | 0.45% | 0.65% | 0.90% | 1.35% | 2.90% | 5.20% | 8.60% |
| Ten-year bucket | 0.60% | 0.85% | 1.15% | 1.70% | 3.50% | 6.30% | 9.90% |

Grieco comments, "Bond L pays 45 bps more than Bond S, so on a one-year view the long bond is the better use of the allocation."

Okonkwo also reviews a default model that Fenwick's risk department applies to Wexford Components, a smaller holding.
The model treats Wexford's equity as a call option on the company's assets, with a strike price equal to the face value of its zero-coupon debt, and it estimates the probability of default as the portion of the asset value distribution at debt maturity that lies below that face value.
Wexford recently entered a volatile new business line, and the risk department expects the volatility of its assets to rise sharply while the asset value and the face value of debt stay unchanged.

Finally, Grieco asks Okonkwo to compare two instruments backed by the same type of collateral, both offered by Sundby Hypotek Bank.
The first is a residential mortgage-backed security (RMBS) issued by a special purpose entity (SPE) that bought a static pool of mortgages from Sundby in a true sale.
The second is a Sundby covered bond backed by a cover pool of residential mortgages, with a conditional pass-through redemption structure.
Sundby services the mortgages in both structures.

### Questions

1. Ignoring the probability of default, the expected one-year return on Bond L, adjusted for credit migration, is closest to: (LOS: los-06-04-c)
   - A. 3.55%.
   - B. 3.75%.
   - C. 6.55%.
2. Regarding Grieco's comment, after adjusting for credit migration: (LOS: los-06-04-c)
   - A. Bond L offers the higher expected return, by about 45 bps.
   - B. Bond S offers the higher expected return, by about 19 bps.
   - C. Bond S offers the higher expected return, by about 39 bps.
3. Under the risk department's model for Wexford, the expected rise in asset volatility will most likely: (LOS: los-06-04-d)
   - A. increase the value of equity, decrease the value of debt, and increase the probability of default.
   - B. decrease the value of equity, decrease the value of debt, and increase the probability of default.
   - C. increase the value of equity, leave the value of debt unchanged because its face value is fixed, and increase the probability of default.
4. Which statement comparing the two Sundby instruments is most accurate? (LOS: los-06-04-h)
   - A. The RMBS investors have recourse to both Sundby and the mortgage pool, because Sundby continues to service the loans.
   - B. The covered bond investors have recourse to both Sundby and the cover pool, and Sundby must replace nonperforming mortgages in the cover pool, whereas the RMBS investors rely on the SPE's static pool.
   - C. If Sundby misses the covered bond's scheduled final payment, the bond defaults and payments are accelerated immediately.

## Item set 14 (03-01): Kaskade Versicherung: Bond Portfolio and an Impaired Hotel Associate

Source: [[IS-03-Financial-Statement-Analysis-LM01-M05]], difficulty 4.

### Vignette

Yuki Tanabe, CFA, covers European insurers for a Zurich asset manager.
She is reviewing the 2027 accounts of Kaskade Versicherung AG, a Swiss property insurer that reports under IFRS.
All amounts are in CHF millions, Kaskade has a December year end, and taxes are ignored.

On 1 January 2026 Kaskade bought three securities for its general account.
Bond D is a four-year bond with par of 200 and a 3% annual coupon, held to collect contractual cash flows that are solely payments of principal and interest.
The market yield on Bond D was 5.0% on the purchase date, and Kaskade paid 185.82.
Bond E is a bond with par of 120 and a 4% annual coupon, bought at par and held in a business model whose objective is achieved both by collecting cash flows and by selling.
Security F is a block of listed shares that Kaskade does not hold for trading and irrevocably elected to measure at fair value through other comprehensive income.

Exhibit 1: General account securities

| Security | Cost 1 Jan 2026 | Fair value 31 Dec 2026 | Fair value 31 Dec 2027 | 2027 event |
|---|---|---|---|---|
| Bond D | 185.82 | 187.40 | 195.10 | Coupon 6.0 received |
| Bond E | 120.00 | 126.00 | n/a | Coupon 4.8 received, then sold on 31 Dec 2027 for 123.60 |
| Security F | 40.00 | 44.00 | n/a | Dividend 1.5 received, then sold on 31 Dec 2027 for 49.00 |

Kaskade also owns 30% of Seeblick Hotels AG, which it accounts for using the equity method.
The carrying amount of the investment was 284 at 31 December 2026.
Amortization of the excess purchase price, which relates to Seeblick's buildings, is 3 per year.
Seeblick reported 2027 net income of 20 and, to support its share price, paid dividends of 30.

After a collapse in Alpine tourism bookings, Kaskade tested the Seeblick investment for impairment at 31 December 2027.

Exhibit 2: Seeblick impairment data at 31 December 2027

| Item | Amount |
|---|---|
| Quoted fair value of Kaskade's 30% stake | 236 |
| Costs to sell the stake | 4 |
| Value in use of the stake | 251 |
| Seeblick total revenue, 2027 | 410 |

Tanabe's colleague, Marc Aebischer, covers Helvetic Re Corp., a US GAAP peer with an identical 30% stake in a hotel group, identical carrying amounts, and identical 2027 impairment data.
Helvetic Re's management has concluded that the decline in value is other than temporary.

Tanabe is also comparing Kaskade with a competitor that designates its bonds at fair value through profit or loss to avoid an accounting mismatch with its insurance liabilities.
To isolate the effect of that choice, she asks how Kaskade's results would have differed had it designated Bond D at fair value through profit or loss on 1 January 2026.

### Questions

1. The carrying amount of Bond D on Kaskade's balance sheet at 31 December 2027 is closest to: (LOS: los-03-01-a)
   - A. CHF 189.11 million.
   - B. CHF 192.57 million.
   - C. CHF 192.91 million.
2. The 2027 profit or loss Kaskade recognizes from Bond E and Security F combined is closest to: (LOS: los-03-01-a)
   - A. CHF 6.3 million.
   - B. CHF 9.9 million.
   - C. CHF 18.9 million.
3. The 2027 impairment loss on the Seeblick investment recognized by Kaskade, and the impairment loss Helvetic Re recognizes on the same facts, are closest to: (LOS: los-03-01-b)
   - A. CHF 27 million and CHF 42 million.
   - B. CHF 46 million and CHF 42 million.
   - C. CHF 36 million and CHF 51 million.
4. Had Kaskade designated Bond D at fair value through profit or loss, its combined 2026 and 2027 pre-tax profit would have been: (LOS: los-03-01-c)
   - A. higher by CHF 2.53 million.
   - B. higher by CHF 4.24 million.
   - C. higher by CHF 9.28 million.

## Item set 15 (05-03): Ostrander Precision Castings: Paying Down the Acquisition Debt

Source: [[IS-05-Equity-Valuation-LM03-M05]], difficulty 3.

### Vignette

Naomi Achebe, CFA, is a portfolio manager at Ridgeview Asset Management, which runs a US mid-cap value fund.
She is reviewing Ostrander Precision Castings Inc., a US producer of investment-cast turbine and pump components that reports under US GAAP.
Ostrander has 90 million shares outstanding, and the shares trade at USD 30.00.
All figures are in USD millions, and the tax rate is 25%.

In 2024 Ostrander bought a competitor with a large bridge loan, which lifted its debt to 55% of total capital at market values.
Management has since announced a plan to reduce debt to 35% of total capital over the next three years and to hold it there, and 2025 was the first year of the plan.

Exhibit 1: Ostrander statement of cash flows, 2025 (USD millions)

| Item | 2025 |
|---|---|
| Net income | 210 |
| Depreciation and amortization | 185 |
| Increase in accounts receivable | (40) |
| Increase in inventories | (25) |
| Increase in accounts payable | 18 |
| Cash flow from operating activities | 348 |
| Capital expenditures | (260) |
| Proceeds from sale of equipment | 20 |
| Cash flow from investing activities | (240) |
| Repayment of long-term debt | (400) |
| Increase in notes payable | 50 |
| Issuance of common shares under employee plans | 30 |
| Dividends paid | (60) |
| Cash flow from financing activities | (380) |
| Net change in cash | (272) |

Interest paid of USD 120 million is included in cash flow from operating activities.
The equipment was sold at its carrying amount, so no gain or loss was recognized.
Achebe considers 2025 operating results and investment representative of the company's normal level.

Exhibit 2: Ostrander capital and market data

| Item | Value |
|---|---|
| Debt, book value | USD 1,550 million |
| Debt, market value | USD 1,480 million |
| Pretax cost of debt | 6.4% |
| Risk-free rate | 4.0% |
| Equity beta | 1.20 |
| Equity risk premium | 5.5% |
| Current weights: debt, equity | 55%, 45% |
| Target weights after the plan: debt, equity | 35%, 65% |

Achebe first reconstructs 2025 FCFF and FCFE from the cash flow statement.
She then discusses the choice of model with Rhys Holloway, a colleague on the fund's research team.

Holloway says: "FCFE was negative in 2025 only because Ostrander used cash to repay debt, which is a financing choice. Discounting FCFF at WACC avoids having to forecast the repayment schedule year by year, and WACC is less sensitive to the leverage change than the cost of equity is."

Achebe decides to use a single-stage FCFF model.
She expects FCFF to grow at 4.0% a year indefinitely from its 2025 level.
Because the model is a perpetuity, she weights the costs of capital at the capital structure Ostrander will hold for the long run, and she estimates the cost of equity with the CAPM.
The fund buys only shares whose estimated value exceeds the market price.

### Questions

1. Ostrander's 2025 FCFF is closest to: (LOS: los-05-03-c)
   - A. USD 151 million.
   - B. USD 198 million.
   - C. USD 228 million.
2. Ostrander's 2025 FCFE is closest to: (LOS: los-05-03-d)
   - A. USD -292 million.
   - B. USD -212 million.
   - C. USD -242 million.
3. Holloway's statement is best described as: (LOS: los-05-03-a)
   - A. correct.
   - B. incorrect, because FCFF for a levered company must be discounted at the required return on equity.
   - C. incorrect, because a company with negative FCFE should be valued with a dividend discount model rather than a free cash flow model.
4. Achebe's estimate of Ostrander's value per share and her conclusion are closest to: (LOS: los-05-03-l)
   - A. USD 28.16; the shares are overvalued.
   - B. USD 33.62; the shares are undervalued.
   - C. USD 50.65; the shares are undervalued.

## Item set 16 (08-04): Quillfeather Multi-Strategy Fund Desk Review

Source: [[IS-08-Alternative-Investments-LM04-M05]], difficulty 3.

### Vignette

Mariko Tanabe, CFA, is an investment officer at Harrowgate Mutual Insurance, which is conducting annual due diligence on its USD 300 million allocation to the Quillfeather Multi-Strategy Fund.
Quillfeather runs four desks under one roof, and Tanabe reviews one current position from each desk with Quillfeather's chief risk officer, Declan Moyo.

The equity desk runs a stub trade in Brannock Industries, a listed holding company that owns 70% of Brannock Logistics and 45% of Selwyn Chemicals, both separately listed.
The desk regards Brannock Industries as overvalued relative to the market value of its two listed stakes.
It has shorted 120,000 Brannock Industries shares and weights the subsidiary legs by the parent's ownership percentages.
Exhibit 1 shows the desk's data.

**Exhibit 1: Brannock stub trade data**

| Company | Share price (USD) | Market beta | Parent's ownership |
|---|---|---|---|
| Brannock Industries (parent) | 58.20 | 1.05 | n/a |
| Brannock Logistics | 31.40 | 0.90 | 70% |
| Selwyn Chemicals | 24.75 | 1.20 | 45% |

The event desk runs a merger arbitrage book.
Its two largest positions are in stock-for-stock deals, in each of which the desk is long the target and short the acquirer in the offer ratio.
Exhibit 2 summarizes them.

**Exhibit 2: Largest merger arbitrage positions**

| Deal | Structure | Current spread |
|---|---|---|
| Veldhoven Pharma (Netherlands) for Ashby Biologics (United States) | Cross-border, friendly; needs approval from both countries' regulators | 6.1% |
| Corrin Foods for Pell Bakeries (both United States) | Domestic, friendly, horizontal | 2.4% |

Moyo makes two statements about the merger book.

Statement 1: "The Veldhoven-Ashby spread is wider mainly because a cross-border deal needs two governmental approvals, which raises the risk that it fails."

Statement 2: "To protect the Veldhoven-Ashby position if the deal fails, we buy out-of-the-money puts on Veldhoven and out-of-the-money calls on Ashby."

The rates desk put on a trade during a recent period of market stress, when hedged inflation-linked bonds traded far cheaper than their usual premium over nominal bonds.
The desk bought USD 40 million of 5-year inflation-linked government bonds at a real yield of 2.45% and shorted USD 40 million of 5-year nominal government bonds of the same government at a yield of 4.05%.
It also entered a zero-cost 5-year inflation swap on a notional of USD 40 million, receiving a fixed rate of 2.30% and paying realized inflation.
Trailing 12-month inflation is 3.10%.
Assume the inflation accrual on the inflation-linked bonds equals the inflation paid on the swap, and ignore financing and transaction costs.

The volatility desk hedges the fund's equity tail risk.
One year ago it bought a one-year volatility swap on a broad equity index with a vega notional of USD 150,000 per volatility point.
The strike was set at the swap's fair volatility of 16.0 at inception.
Over the year, the index's realized volatility was 21.4, and on the expiry date the index's one-month implied volatility was 19.0.

Tanabe tells Moyo that she will summarize each desk's position for Harrowgate's investment committee meeting on 18 March.

### Questions

1. To complete the Brannock stub trade, the equity desk's position in Selwyn Chemicals should be: (LOS: los-08-04-b)
   - A. long 54,000 shares.
   - B. long 66,000 shares.
   - C. short 54,000 shares.
2. Which of Moyo's statements about the merger arbitrage book is correct? (LOS: los-08-04-c)
   - A. Statement 1 only
   - B. Statement 2 only
   - C. Both Statement 1 and Statement 2
3. The rates desk's expected annual net cash flow from its combined position is closest to: (LOS: los-08-04-d)
   - A. negative USD 640,000
   - B. USD 280,000
   - C. USD 600,000
4. The payoff to the volatility desk on the volatility swap at expiry is closest to: (LOS: los-08-04-f)
   - A. USD 450,000
   - B. USD 810,000
   - C. negative USD 810,000

## Item set 17 (07-01): Valtoria AG: Franc-Euro Swap Funding for a Eurozone Acquisition

Source: [[IS-07-Derivatives-LM01-M05]], difficulty 4.

### Vignette

Valtoria AG is a Swiss specialty pharmaceutical company that reports in Swiss francs (CHF).
To fund the purchase of a German contract manufacturer, Valtoria's treasury enters a two-year fixed-for-fixed currency swap with a dealer.
Marc Keller, CFA, the group treasurer, and his analyst, Ines Baumann, manage the hedge program.

At initiation Valtoria delivers CHF 150,000,000 to the dealer and receives the equivalent euro (EUR) notional at the spot rate of CHF 0.9380 per EUR 1.
Every 180 days Valtoria pays a fixed euro rate on the euro notional and receives a fixed franc rate on the franc notional, and the notionals are re-exchanged at maturity.
Both fixed rates are set at their no-arbitrage levels, and all rates are add-on rates on an actual/360 basis.

Exhibit 1: Spot rates at swap initiation

| Days | 180 | 360 | 540 | 720 |
|---|---|---|---|---|
| EUR | 2.60% | 2.70% | 2.78% | 2.85% |
| CHF | 0.85% | 0.92% | 0.98% | 1.04% |

Valtoria also has an existing CHF 80,000,000 interest rate swap, entered one year ago, in which it pays a fixed rate of 1.60% and receives MRR, with semiannual resets on the same 180-day schedule.
The swap had three years to run at inception, so four semiannual settlements remain, and today is a reset date that coincides with the currency swap's initiation.

One hundred twenty days after the currency swap's initiation, Baumann prepares a quarter-end valuation.
The first semiannual exchange of fixed payments will occur 60 days later.

Exhibit 2: Spot rates 120 days after initiation

| Days | 60 | 240 | 420 | 600 |
|---|---|---|---|---|
| EUR | 2.88% | 2.96% | 3.03% | 3.09% |
| CHF | 0.70% | 0.76% | 0.81% | 0.86% |

On the valuation date the spot exchange rate is CHF 0.9610 per EUR 1, and the one-year forward rate is CHF 0.9400 per EUR 1.

Baumann drafts two statements for the audit committee.

Statement 1: "Had the exchange rate been quoted in euros per franc, the euro would become currency a, and the value of the currency swap to Valtoria would then be the negative of the value we report."

Statement 2: "Of the three market moves since initiation (higher euro rates, lower franc rates, and a stronger euro), only the stronger euro has reduced the value of the currency swap to Valtoria."

Keller asks Baumann to confirm the payment schedule and both valuations before the committee meets.

### Questions

1. Based on Exhibit 1, Valtoria's semiannual fixed euro payment is closest to: (LOS: los-07-01-f)
   - A. EUR 1,962,135.
   - B. EUR 2,230,094.
   - C. EUR 4,460,188.
2. Based on Exhibit 2, the value of the currency swap to Valtoria 120 days after initiation is closest to: (LOS: los-07-01-f)
   - A. -CHF 3,542,756.
   - B. CHF 154,808.
   - C. CHF 3,542,756.
3. Based on Exhibit 1, the value today of Valtoria's existing CHF interest rate swap is closest to: (LOS: los-07-01-e)
   - A. -CHF 1,798,101.
   - B. -CHF 899,051.
   - C. CHF 899,051.
4. Which of Baumann's statements is correct? (LOS: los-07-01-f)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both Statement 1 and Statement 2.

## Item set 18 (05-02): Vellmar Brewing: What the Share Price Already Assumes

Source: [[IS-05-Equity-Valuation-LM02-M05]], difficulty 4.

### Vignette

Dmitri Albescu, CFA, manages the European dividend strategy at Corvina Income Partners, a Luxembourg asset manager whose funds hold minority stakes in listed consumer staples companies.
On 11 September 2026 he is reviewing Vellmar Brewing Group SE, a mature brewer with operations in Germany, Poland and the Baltic states.
Vellmar's shares trade at EUR 62.40, and the annual dividend of EUR 2.40 per share was paid last week.
Management has published a three-year dividend plan that raises the payout ratio gradually while a brewery consolidation program is completed.
Albescu treats the dividends in the plan as known and assumes that dividends grow at a constant rate forever after year 3.
Rather than impose his own terminal growth rate, he first wants to know what growth rate the market price already assumes.

Exhibit 1: Vellmar per-share data and forecasts (EUR)

| | Year 0 (actual) | Year 1 | Year 2 | Year 3 |
|---|---|---|---|---|
| Earnings per share | 3.95 | 4.20 | 4.40 | 4.60 |
| Dividend per share | 2.40 | 2.52 | 2.70 | 2.85 |

Exhibit 2: Market and benchmark data

| Input | Value |
|---|---|
| Risk-free rate | 2.5% |
| Vellmar beta | 0.90 |
| Equity risk premium | 5.0% |
| Vellmar ROE, fiscal 2025 | 12.0% |
| Vellmar equity multiplier, fiscal 2025 | 2.8 |
| Industry median ROE, mature European brewers | 7.5% |
| Management's long-run target payout ratio | 55% |
| Peer median trailing P/E | 16.0 |
| Peer median leading P/E | 15.0 |

Albescu estimates Vellmar's required return with the CAPM.
Because Vellmar's recent ROE was achieved with leverage well above the sector's, Corvina's policy is to set mature ROE equal to the industry median when analyzing growth after an explicit forecast period.
Albescu also wants to report how much of the current price reflects growth opportunities rather than the value of Vellmar's existing assets, using the market price as the estimate of value.

His colleague Sigrid Hollis, who covers the same sector, reviews his working papers on 12 September 2026.
She prefers to anchor terminal values in peer multiples and makes three statements.

Statement 1: "Because the Gordon terminal value at the end of year 3 is calculated from the year-4 dividend, it should be discounted four periods to today."

Statement 2: "Applying the peer median trailing P/E to Vellmar's year-3 EPS gives a terminal value that implies a higher perpetual dividend growth rate than the rate embedded in today's share price."

Statement 3: "Setting the terminal value with a peer multiple rather than the Gordon model removes the need to make any assumption about Vellmar's growth after year 3."

Albescu notes that whatever terminal value is used will account for most of the estimated value of a mature company such as Vellmar.

### Questions

1. The perpetual dividend growth rate after year 3 that is implied by Vellmar's current share price is closest to: (LOS: los-05-02-f)
   - A. 2.96%.
   - B. 2.68%.
   - C. 2.80%.
2. Under Corvina's policy for mature ROE, the long-run payout ratio consistent with the market-implied growth rate, and the conclusion Albescu should draw given management's target payout, are closest to: (LOS: los-05-02-p)
   - A. 35.8%; undervalued.
   - B. 64.2%; overvalued.
   - C. 64.2%; undervalued.
3. Vellmar's present value of growth opportunities per share and the component of its leading P/E attributable to growth opportunities are closest to: (LOS: los-05-02-g)
   - A. EUR 2.40 and 0.57.
   - B. EUR 5.97 and 1.42.
   - C. EUR 2.40 and 14.29.
4. Which of Hollis's statements is most accurate? (LOS: los-05-02-m)
   - A. Statement 1.
   - B. Statement 2.
   - C. Statement 3.

## Item set 19 (06-01): Larchmont Treasury Fund: Riding the Curve and Re-Measuring Its Risk

Source: [[IS-06-Fixed-Income-LM01-M05]], difficulty 4.

### Vignette

Solenne Dufour, CFA, manages the Larchmont Treasury Fund, a CAD 400 million fund that holds only Canadian government zero-coupon bonds.
A large share of the fund is earmarked for a known distribution in exactly two years.
Dufour is considering replacing part of her two-year zero-coupon holding with a longer bond that she would sell at the two-year horizon.

Exhibit 1: Canadian government spot rates (annual compounding)

| Maturity (years) | 1 | 2 | 3 | 4 | 5 | 6 | 10 |
|---|---|---|---|---|---|---|---|
| Spot rate | 1.90% | 2.40% | 2.85% | 3.20% | 3.45% | 3.65% | 4.10% |

The three-month Treasury bill yields 1.72%, and the fund's management fee is 0.15% a year; Dufour ignores both in her analysis.

Dufour's candidate is the six-year government zero-coupon bond.
Her base case is that the spot curve in Exhibit 1 will be unchanged two years from today.
She compares the six-year zero, sold after two years, with the maturity-matched two-year zero held to maturity.

Her colleague, Rhys Albright, is unconvinced.
"Your base case is only one outcome," he says.
"Tell me how high the four-year spot rate can be two years from today before your trade does worse than simply holding the two-year zero."
Dufour agrees to compute that breakeven four-year rate from Exhibit 1.

Dufour decides to proceed and switches CAD 100 million of market value from the two-year zero into the six-year zero.

Exhibit 2: Fund holdings at market value (CAD millions)

| Holding | Before the switch | After the switch |
|---|---|---|
| Two-year zero | 220 | to be computed |
| Six-year zero | 100 | to be computed |
| Ten-year zero | 80 | 80 |
| Total | 400 | 400 |

The fund's risk analyst, Kwame Asante, measures curve risk with key rate durations at the 2-, 6- and 10-year points.
For each key rate, he uses the market value weight of the zero at that maturity multiplied by its maturity, the approximation the fund's risk system applies to zero-coupon bonds.
Asante's stress scenario for the risk committee is a bear steepening in which, after the switch, the 2-year key rate rises 10 bps, the 6-year key rate rises 30 bps, and the 10-year key rate rises 45 bps.

The fund's economist, Beatrix Holm, adds two statements to the committee pack.

Statement 1: "Research on government yields finds that monetary policy explains most of the variation in short- and intermediate-term yields, whereas inflation expectations explain most of the variation in long-term yields."

Statement 2: "The finance ministry plans to shorten the average maturity of its new bond issuance. By adding duration supply to the market, this should raise the bond risk premium and push long-term yields higher."

Dufour wants each statement checked before the pack is circulated.

### Questions

1. Under Dufour's base case, the annualized two-year horizon return on the six-year zero-coupon bond is closest to: (LOS: los-06-01-d)
   - A. 2.40%.
   - B. 3.65%.
   - C. 4.56%.
2. The breakeven four-year spot rate two years from today that answers Albright's question is closest to: (LOS: los-06-01-c)
   - A. 4.01%.
   - B. 4.28%.
   - C. 4.56%.
3. Under Asante's stress scenario, the change in the fund's value is closest to: (LOS: los-06-01-i)
   - A. -CAD 5.84 million.
   - B. -CAD 6.35 million.
   - C. -CAD 7.44 million.
4. Which of Holm's statements is correct? (LOS: los-06-01-k)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both statements.

## Item set 20 (05-04): Pasir Ridge Life: Market-Level Multiples for an Equity Sleeve

Source: [[IS-05-Equity-Valuation-LM04-M05]], difficulty 3.

### Vignette

Teo Kah Wei, CFA, heads equities at Pasir Ridge Life Assurance, a Singapore insurer that runs a global equity sleeve for its participating fund.
On 30 June 2026 he prepares a note for the investment committee on three questions: whether the US equity market is attractively priced, how two emerging-market holdings should be valued in an inflationary setting, and whether one industrial holding is still cheap.

Exhibit 1: US market data, 30 June 2026

| Item | Value |
|---|---|
| Broad US equity index level | 5,600 |
| Index EPS, next 12 months (consensus) | 280 |
| Index EPS, trailing 12 months | 256 |
| Yield on 10-year US Treasury note | 4.30% |
| Yield on A-rated US corporate bonds | 5.50% |
| Consensus five-year index EPS growth | 9.50% |

Teo applies the Yardeni model with a weight on long-term growth of 0.10, the historical estimate, and compares the result with the index's forward multiple.

For the emerging-market holdings, Teo uses a justified P/E that allows for incomplete pass-through of cost inflation to earnings.
Both holdings pay out essentially all their earnings, and he assigns each a real required return of 4.5%.

Exhibit 2: Inflation inputs

| Holding | Country | Expected inflation | Pass-through rate |
|---|---|---|---|
| Orchid Consumer Holdings | Singapore | 2.0% | 70% |
| Verano Energia SA | Brazil | 6.0% | 70% |

Verano's nominal required return, 10.5%, appears in the risk team's model, which adds expected inflation to the real rate.

Teo also reports the aggregate valuation of the sleeve's five largest positions, which make up the whole of a concentrated sub-portfolio.
The investment committee wants a single forward P/E that equals the sub-portfolio's total market value divided by its total forecast earnings.

Exhibit 3: Concentrated sub-portfolio, 30 June 2026

| Holding | Portfolio weight (by market value) | Forward P/E |
|---|---|---|
| Holding 1 | 30% | 14.0 |
| Holding 2 | 25% | 18.0 |
| Holding 3 | 20% | 25.0 |
| Holding 4 | 15% | 9.0 |
| Holding 5 | 10% | 40.0 |

Finally, Teo reviews Brightwater Industrial Corp., a US machinery maker whose fiscal year ends on 30 September.
Brightwater's shares trade at USD 85.10.
Consensus EPS is USD 4.00 for fiscal 2026 and USD 4.80 for fiscal 2027.
Over the past five years Brightwater's forward P/E has averaged 95% of the index's forward P/E, and Teo sees no change in its business mix, leverage or growth outlook relative to the index.
To make Brightwater's multiple comparable with the index's next-12-month multiple, he calendarizes its EPS by weighting the two fiscal-year estimates by the months of each that fall within the next 12 months.

His colleague Farah Iskandar, who manages the fund's fixed income book, reads the draft on 2 July 2026.
She notes that the Yardeni model uses a corporate bond yield, which contains a default premium but no equity risk premium, and that its five-year growth input may not be sustainable forever.
She asks Teo to keep the model as one input among several, not as a standalone signal.
Teo agrees to present each answer with the benchmark it rests on, so that the committee can see where a relative conclusion depends on the benchmark being fairly priced.

### Questions

1. The Yardeni model's justified forward P/E for the index, and the valuation it indicates for the US market, are closest to: (LOS: los-05-04-l)
   - A. 22.0; undervalued.
   - B. 23.3; undervalued.
   - C. 22.0; overvalued.
2. Verano's justified P/E is closest to: (LOS: los-05-04-p)
   - A. 8.1.
   - B. 11.5.
   - C. 15.9.
3. The forward P/E the investment committee requests for the sub-portfolio in Exhibit 3 is closest to: (LOS: los-05-04-r)
   - A. 16.0.
   - B. 16.5.
   - C. 19.1.
4. Based on its own historical relationship with the index, Brightwater's forward P/E and valuation are best described as: (LOS: los-05-04-m)
   - A. 18.5; undervalued.
   - B. 21.3; overvalued.
   - C. 20.3; overvalued.

## Item set 21 (03-05): Brenmoor Networks: Accruals, Capitalized Line Costs, and Market Risk

Source: [[IS-03-Financial-Statement-Analysis-LM05-M05]], difficulty 3.

### Vignette

Ingrid Solberg, CFA, is a credit analyst at Halvard Fixed Income Partners, a bond fund that holds senior unsecured notes issued by Brenmoor Networks SE.
Brenmoor is an established telecommunications carrier that leases line capacity from other carriers to complete its network.
Brenmoor and its closest peer, Ostley Telecom plc, report under IFRS with a December year end, and all amounts are in € millions.
Solberg is updating her credit assessment of Brenmoor's FY2025 results.

Exhibit 1: Selected FY2025 data (€ millions)

| Item | Brenmoor | Ostley |
|---|---|---|
| Operating income | 780.0 | 395.0 |
| Pre-tax income | 548.0 | 347.0 |
| Net income | 411.0 | 260.0 |
| Cash flow from operating activities | 1,150.0 | 520.0 |
| Capital expenditures | 1,020.0 | 455.0 |
| Dividends paid | 180.0 | 95.0 |
| Total assets, 31 December 2024 | 9,600.0 | 5,900.0 |
| Total assets, 31 December 2025 | 10,400.0 | 6,100.0 |

Solberg's screen measures aggregate accruals as net income minus operating cash flow, scaled by average total assets.

Exhibit 2: Brenmoor, common-size data at 31 December (€ millions)

| Item | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Gross property, plant, and equipment | 3,420.0 | 3,627.0 | 4,224.0 | 5,096.0 |
| Total assets | 9,000.0 | 9,300.0 | 9,600.0 | 10,400.0 |
| Gross PP&E as a percentage of total assets | 38.0% | 39.0% | 44.0% | 49.0% |

Brenmoor's annual reports describe no change in network strategy since 2021, and its subscriber numbers have grown by about 2% a year.

In January 2026, before any announcement by the company, Solberg's colleague Marek Novak wrote in an internal note: "Brenmoor's operating cash flow is nearly three times its net income and its accruals are strongly negative, so its earnings are of high quality and we can rely on its cash generation."

In March 2026 Brenmoor announced that its audit committee had found that €240.0 million of FY2025 payments to other carriers for leased line capacity, an operating cost, had been capitalized within PP&E additions.
Depreciation of €12.0 million had been recorded on these amounts in FY2025.
Brenmoor's tax rate is 25%, and taxes paid in FY2025 are unaffected by the correction.

Solberg also reviews the market risk section of Brenmoor's FY2025 financial statement notes, summarized in Exhibit 3.
The notes state that the sensitivities are symmetric, so an equal move in the opposite direction has the opposite effect.

Exhibit 3: Brenmoor, market risk sensitivities disclosed in the FY2025 notes (€ millions)

| Change in market variable | Effect on pre-tax income |
|---|---|
| 100 basis point parallel rise in euro interest rates | $-26.0$ |
| 10% appreciation of the British pound against the euro | $+18.0$ |
| 10% appreciation of the Polish zloty against the euro | $-9.0$ |

Solberg's stress scenario for FY2026 assumes a 100 basis point parallel rise in euro interest rates together with a 10% depreciation of the British pound against the euro, with the zloty unchanged.

### Questions

1. Brenmoor's FY2025 aggregate accruals ratio, and its earnings quality relative to Ostley on this measure alone, are closest to: (LOS: los-03-05-e)
   - A. $-7.4\%$; higher earnings quality than Ostley.
   - B. $-7.4\%$; lower earnings quality than Ostley.
   - C. $-3.7\%$; lower earnings quality than Ostley.
2. After correcting for the capitalized line costs, Brenmoor's FY2025 operating cash flow and free cash flow (operating cash flow less capital expenditures) are closest to: (LOS: los-03-05-i)
   - A. €910.0 million and €130.0 million.
   - B. €910.0 million and $-€110.0$ million.
   - C. €970.0 million and €190.0 million.
3. The most appropriate response to Novak's January 2026 note is that: (LOS: los-03-05-h)
   - A. Novak is correct, because operating cash flow well above net income is the clearest indicator of high earnings quality.
   - B. Novak is incorrect, because the rise in gross PP&E as a share of total assets with no change in strategy is consistent with operating costs being capitalized, which moves outflows to investing activities and inflates operating cash flow.
   - C. Novak is incorrect, because strongly negative accruals indicate that Brenmoor is recognizing revenue before it is earned.
4. Based on Exhibit 3, the effect of Solberg's stress scenario as a percentage of Brenmoor's FY2025 pre-tax income is closest to: (LOS: los-03-05-m)
   - A. $-1.5\%$.
   - B. $-8.0\%$.
   - C. $-10.7\%$.

## Item set 22 (10-02): Pembrook and Vale Advisers: Conduct Beyond the Portfolio

Source: [[IS-10-Ethics-LM02-M05]], difficulty 3.

### Vignette

Pembrook and Vale Advisers is a regional wealth management firm with offices in three cities.
Its general counsel, Hollis Grange, is reviewing several matters raised at the firm's quarterly compliance meeting in September 2026.

Rafael Quint is an associate portfolio analyst who sat the Level III examination of the CFA Program in August 2026.
Results are scheduled for release in October 2026.
On 5 September, Quint posted on a public online forum for candidates: "Level III was long but fair, and I expect a low pass rate."
In the same post he added: "Anyone who skipped private wealth taxation made a mistake, because there were several questions on it and almost nothing on swaps."
On 7 September, he updated his professional networking profile to read: "Completed the CFA Program in August 2026; eligible for the charter upon meeting the work experience requirement."

Grange is also reviewing three personal matters reported by employees.
Teodor Blix, CFA, was arrested on a Saturday for blocking a public road during a peaceful climate protest and was charged with a minor public-order offence.
Wren Castell, CFA, filed for personal bankruptcy after large uninsured medical bills; her filing was complete and accurate.
Idris Fenn, CFA, is the volunteer treasurer of a youth sports club.
When he bought equipment for the club, he submitted to the club a supplier invoice he had altered to show a price 20% higher than the price paid, and kept the difference.
None of the three matters involved client assets.

Marguerite Oduya, CFA, is a senior adviser at the firm.
In July 2026 she met Beatrix Sallow, a prospective client, who explained during the meeting that she intended to sell her family business within a year and would need advice on investing the proceeds.
Sallow later hired another adviser.
In August, Oduya mentioned Sallow's plan to sell the business to a friend who works as a business broker, explaining that "Sallow never became our client, and my friend could help her."
Separately, Oduya provided copies of an existing client's account records to the CFA Institute Professional Conduct Program, which was investigating a complaint the client had filed about a former Pembrook and Vale employee.
Local law permits such disclosure.

Finally, Ferrow Logistics, a listed company whose shares are held in about 40 Pembrook and Vale client accounts, has invited Oduya to join its board of directors.
The board pays an annual cash retainer and grants stock options to directors.
Oduya has told Grange that she would like to accept and wants to know how to proceed.
Pembrook and Vale's code of ethics requires employees to report outside activities to compliance but says nothing more specific about directorships.

Grange plans to summarize each matter for the firm's management committee.
For each, the committee wants to know which Standard, if any, is engaged, and which firm procedure or member action would be consistent with the Code and Standards.

### Questions

1. Which of Quint's communications most likely violate the Standards? (LOS: los-10-02-a)
   - A. The forum post only, because he criticized the length of the examination and predicted the pass rate.
   - B. The profile only, because a candidate may not claim to have completed the Program or to be eligible for the charter before results are released.
   - C. Both the forum post, for disclosing which topics were and were not tested, and the profile.
2. Which employee most likely violated the Standard relating to misconduct? (LOS: los-10-02-a)
   - A. Blix.
   - B. Castell.
   - C. Fenn.
3. Which of Oduya's disclosures is most likely inconsistent with the Standard relating to preservation of confidentiality? (LOS: los-10-02-a)
   - A. Neither, because Sallow never became a client and the Professional Conduct Program disclosure was permitted.
   - B. Only the disclosure of Sallow's plans to the business broker.
   - C. Both, because client information may be disclosed only with the client's permission.
4. With respect to the Ferrow board seat, the course of action most consistent with the Standards is for Oduya to: (LOS: los-10-02-b)
   - A. accept only after obtaining written consent from Pembrook and Vale, disclose the directorship prominently to clients, and have the firm separate her from investment decisions on Ferrow.
   - B. accept, and disclose the directorship to clients in the firm's next annual letter once she has attended her first board meeting.
   - C. accept but decline the stock options, so that no disclosure or consent is required.

## Answer keys

> [!success]- Item set 1 (09-04)
> 1. **B.** Active exposures are Corvina's sensitivities minus the benchmark's: value $0.30 - 0.10 = 0.20$, size $0.45 - 0.60 = -0.15$, momentum $0.12 - 0.00 = 0.12$, quality $0.20 - 0.20 = 0.00$.
> With negligible factor covariances, active factor risk $= \sum (b_k^a)^2 \sigma^2(F_k)$.
> Value $0.20^2 \times 3.0^2 = 0.3600$; size $(-0.15)^2 \times 4.0^2 = 0.3600$; momentum $0.12^2 \times 5.0^2 = 0.3600$; quality $0.00^2 \times 2.5^2 = 0.0000$.
> Active factor risk $= 1.0800$ (% squared).
> A is wrong because it multiplies squared active exposures by factor standard deviations instead of variances: $0.04 \times 3.0 + 0.0225 \times 4.0 + 0.0144 \times 5.0 = 0.2820$.
> C is wrong because it uses Corvina's own sensitivities instead of active exposures: $0.09 \times 9 + 0.2025 \times 16 + 0.0144 \times 25 + 0.04 \times 6.25 = 4.6600$.
> 2. **A.** Active risk squared $= 1.0800 + 1.1700 = 2.2500$, so tracking risk $= \sqrt{2.2500} = 1.5000\%$.
> Mean active return $= 11.40 - 10.80 = 0.6000\%$, so $IR = 0.60/1.50 = 0.4000$.
> Tracking risk of 1.50% is within the 2.00% limit and the IR of 0.40 exceeds the 0.35 floor, so both guidelines are met.
> B is wrong because it reports active risk squared as tracking risk and divides by it: $0.60/2.25 = 0.2667$.
> C is wrong because it takes the difference in total return volatilities, $15.8 - 15.2 = 0.60\%$, as tracking risk; tracking risk is the standard deviation of the active return series, not the difference in standard deviations, which gives the spurious $IR = 0.60/0.60 = 1.0000$.
> 3. **C.** Active specific risk is $1.17/2.25 = 52.00\%$ of active risk squared, and active factor risk is $1.08/2.25 = 48.00\%$.
> Each of the three style tilts contributes $0.36/2.25 = 16.00\%$, so the manager's active risk is split about evenly between security selection and style bets, with no single tilt dominating.
> A is wrong because contribution depends on the squared active exposure times the factor variance; momentum's small exposure is offset by the highest factor volatility, so it contributes the same 0.36 as value and size.
> B is wrong because active risk comes from active exposures; Corvina's quality sensitivity equals the benchmark's, so its active quality exposure and contribution are zero.
> 4. **A.** Fundamental models, with many industry and style variables, often explain more return variance than macroeconomic models, but the gap overstates their superiority.
> The industry dummy variables together sum to the market, while the macroeconomic model contains no market factor, so part of the advantage is built into the comparison.
> Macroeconomic models are parsimonious and let the user express and measure exposures to economic views directly, which is what the system's overlay program needs, while fundamental models give a detailed, security-characteristic picture of risk; the model types serve different uses.
> B is wrong because variance explained ignores parsimony, interpretability, and the purpose of the analysis.
> C is wrong because it reverses the typical empirical finding; zero-mean surprise factors say nothing about how much variance a model explains.
>
> **Distractor design**
>
> 1. A: factor standard deviations used instead of factor variances; C: portfolio sensitivities used instead of active (portfolio minus benchmark) exposures.
> 2. B: active risk squared reported as tracking risk (square root omitted); C: difference in total volatilities used as tracking risk (misread exhibit decoy).
> 3. A: small active exposure assumed to mean small risk contribution, ignoring factor variance; B: zero portfolio-minus-benchmark exposure confused with a non-zero portfolio sensitivity.
> 4. B: variance explained treated as the only model criterion; C: empirical ranking reversed and zero-mean surprise property misapplied.

> [!success]- Item set 2 (09-05)
> 1. **C.** Ex ante tracking error is VaR machinery run on the portfolio minus the benchmark, so it is the standard deviation of the return difference, quoted as one standard deviation annualized.
> Terms: $0.174^2 = 0.030276$; $0.152^2 = 0.023104$; $2(0.95)(0.174)(0.152) = 0.050251$.
> Variance of active return $= 0.030276 + 0.023104 - 0.050251 = 0.003129$, so tracking error $= \sqrt{0.003129} = 0.055936$, about 5.59%.
> A is wrong because 2.10% is the realized (ex post) tracking error of the past holdings, which is backward-looking and does not reflect the current holdings the committee asked about.
> B is wrong because it subtracts the two volatilities, $17.4\% - 15.2\% = 2.20\%$, which would be correct only if the correlation were exactly 1.
> 2. **B.** Equity sleeve: $240 \times 1.09 \times (-0.15) = -39.2400$ million.
> Bond sleeve: duration term $-6.8 \times 0.0080/1.045 = -0.052057$; convexity term $\tfrac{1}{2}(58)(0.0080)^2/1.045^2 = 0.001700$; return $= -0.050358$, so the change is $160 \times (-0.050358) = -8.0573$ million.
> Total $= -39.2400 - 8.0573 = -47.2973$ million, a loss of about USD 47.3 million, or 11.82% of the account.
> A is wrong because it ignores beta and applies the index move directly to the equity sleeve: $240 \times (-0.15) - 8.0573 = -44.0573$ million.
> C is wrong because it omits the convexity term: $160 \times (-0.052057) = -8.3292$ million, total $-47.5692$ million; for a large yield change the positive convexity term should be included.
> 3. **A.** Fontaine is correct: aggregating sensitivities into a bucket assumes perfect correlation of the rate changes inside it, so broad buckets can conceal curve risk, which is the granularity trade-off of sensitivity reporting.
> Okonkwo is incorrect: sensitivity measures say nothing about how volatile the underlying factor is, and high-yield spreads are far more volatile than investment-grade spreads, so equal spread durations do not mean equal spread risk.
> B and C are wrong because each accepts Okonkwo's statement.
> 4. **C.** With zero expected active return, the 5% relative VaR is $1.65 \times 0.055936 = 0.092294$ of assets, and $0.092294 \times 800{,}000{,}000 = \text{USD } 73{,}835{,}094$, about USD 73.8 million.
> Like any VaR, it is a minimum shortfall at the stated frequency: underperformance of at least USD 73.8 million should occur in about 5% of years, or one year in 20, and the shortfall in those years can be larger.
> A is wrong because it reports the one standard deviation tracking error in dollars, $0.055936 \times 800\text{m} = \text{USD } 44.7$ million, which corresponds to a 16% relative VaR (about one year in six), not a 5% one.
> B is wrong because it reads VaR as a maximum; VaR places no upper bound on the shortfall.
> Expressing the result as 9.23% of assets and relative to the benchmark is the long-only convention Okonkwo asked about, because an unleveraged manager's key risk is underperformance rather than insolvency.
>
> **Distractor design**
>
> 1. A: misread exhibit (ex post realized tracking error used for the ex ante measure); B: wrong formula variant (volatility difference, which assumes a correlation of 1).
> 2. A: beta ignored (index move applied to the equity sleeve); C: convexity term omitted for a large yield change.
> 3. B: sensitivity treated as a risk measure that captures factor volatility; C: both statements accepted without checking the spread-volatility limitation.
> 4. A: wrong threshold (one-sigma, 16% figure reported as the 5% relative VaR); B: VaR misread as a maximum shortfall.

> [!success]- Item set 3 (07-02)
> 1. **B.** For a currency option the underlying is the spot rate quoted in domestic currency per unit of foreign currency (AUD per EUR), the domestic AUD rate is the risk-free rate, and the foreign EUR rate is the carry benefit $\gamma = r^f$.
> $c = Se^{-r^f T}N(d_1) - Xe^{-rT}N(d_2)$ with $e^{-0.023 \times 0.5} = 0.988566$ and $e^{-0.041 \times 0.5} = 0.979709$.
> Currency leg: $1.6500(0.988566)(0.4562) = 0.744123$; bond leg: $1.6800(0.979709)(0.4311) = 0.709552$.
> $c = 0.744123 - 0.709552 = 0.034571$ per EUR, or $0.034571 \times 3{,}000{,}000 = $ AUD 103,713 (full-precision BSM gives 0.034621 per EUR; the difference is rounding in the $N(\cdot)$ values).
> A is wrong because it swaps the domestic and foreign rates, $1.65e^{-0.0205}(0.4562) - 1.68e^{-0.0115}(0.4311) = 0.737461 - 0.715972 = 0.021489$, AUD 64,468.
> C is wrong because it omits the carry benefit on the currency leg, $1.65(0.4562) - 0.709552 = 0.043178$, AUD 129,534.
> 2. **A.** A BSM call is a leveraged position in the underlying: hold $e^{-r^f T}N(d_1)$ units of the foreign currency per option, financed by borrowing $e^{-rT}XN(d_2)$ in domestic currency.
> Euros: $0.988566 \times 0.4562 \times 3{,}000{,}000 = $ EUR 1,352,951, which grow on deposit at the EUR rate, just as dividend-paying shares require fewer shares in the replication.
> Borrowing: $0.709552 \times 3{,}000{,}000 = $ AUD 2,128,656.
> Net cost: $1{,}352{,}951 \times 1.65 - 2{,}128{,}656 = 2{,}232{,}370 - 2{,}128{,}656 = $ AUD 103,713, the call value from Question 1.
> B is wrong because it discounts the strike at the EUR rate rather than the AUD rate, $1.68 \times 0.988566 \times 0.4311 \times 3{,}000{,}000 = $ AUD 2,147,901.
> C is wrong because it holds $N(d_1) \times 3{,}000{,}000 = $ EUR 1,368,600, ignoring that the euro deposit earns the foreign rate.
> 3. **C.** BSM assumes the volatility of the underlying's return is known and constant over the option's life; using implied volatility is a practical input choice, not a feature of the model.
> A is wrong because geometric Brownian motion, with normally distributed continuously compounded returns and no jumps, is a BSM assumption.
> B is wrong because BSM assumes any yield on the underlying is paid continuously at a constant rate, which is exactly how the foreign interest rate enters a currency option.
> 4. **A.** Put delta is $-e^{-r^f T}N(-d_1)$, with $N(-d_1) = 1 - 0.4562 = 0.5438$.
> $\text{Delta}_p = -0.988566 \times 0.5438 = -0.5376$.
> Carry-adjusted parity gives the same result: $\text{Delta}_c - e^{-r^f T} = 0.988566(0.4562) - 0.988566 = 0.4510 - 0.9886 = -0.5376$.
> B is wrong because it drops the carry factor, $-N(-d_1) = -0.5438$.
> C is wrong because it uses the no-carry parity relation, $\text{Delta}_c - 1 = 0.4510 - 1 = -0.5490$.
> Whitford's remark about the EUR rate is also consistent with the model: a higher carry benefit lowers call values and raises put values.
>
> **Distractor design**
>
> 1. A: domestic and foreign rates swapped (misread exhibit); C: carry benefit omitted from the currency leg (wrong formula variant).
> 2. B: strike discounted at the foreign rate instead of the domestic rate (rate mix-up); C: currency holding sized at $N(d_1)$ without the carry adjustment (wrong formula variant).
> 3. A: geometric Brownian motion misread as an inconsistent assumption (assumption misread); B: continuous constant carry yield misread as inconsistent (assumption misread).
> 4. B: carry factor omitted from put delta (wrong formula variant); C: no-carry delta parity applied to a currency option (wrong formula variant).

> [!success]- Item set 4 (01-03)
> 1. **B.** The total degrees of freedom in Exhibit 2 are 107, so $n = 107 + 1 = 108$. The unadjusted $R^2$ of the auxiliary regression is $9{,}406.0 / 115{,}843.0 = 0.081196$, or 0.0812 rounded. $\chi^2_{BP} = nR^2 = 108 \times 0.081196 = 8.7692$. The degrees of freedom equal the $k = 3$ regressors, so the 5% critical value is 7.815, and $8.7692 > 7.815$ (p-value 0.0325) rejects the null of no conditional heteroskedasticity at 5%, though not at 1% (11.345). A is wrong because it reports the F-statistic of the auxiliary regression, $(9{,}406.0/3)/(106{,}437.0/104) = 3{,}135.3333/1{,}023.4327 = 3.0635$, instead of $nR^2$, and compares it with the chi-square critical value. C is wrong because it counts the intercept as a regressor and uses 4 degrees of freedom, whose 5% critical value 9.488 exceeds 8.7692.
> 2. **B.** $DW = 11{,}256.5 / 5{,}832.4 = 1.9300$, where the denominator is the residual sum of squares of Model 1, so $r \approx 1 - 1.9300/2 = 0.0350$ and first-order serial correlation is negligible. The Breusch-Godfrey statistic is distributed $F(p, n - p - k - 1) = F(12, 108 - 12 - 3 - 1) = F(12, 92)$, and $2.31 > 1.859$ (p-value 0.0126), so serial correlation up to lag 12 is present; the Durbin-Watson test misses it because it detects only first-order serial correlation. Because no regressor is a lagged dependent variable, the coefficients remain consistent and only the standard errors are understated, so Newey-West (HAC) standard errors are required, and they also handle the conditional heteroskedasticity found in question 1. A is wrong because it relies on the Durbin-Watson statistic alone and ignores the Breusch-Godfrey rejection. C is wrong because it divides by the total sum of squares, $11{,}256.5 / 11{,}001.3 = 1.0232$ (implied $r \approx 0.4884$), and because serial correlation makes coefficients inconsistent only when a lagged dependent variable is a regressor.
> 3. **B.** $VIF_{BDI} = 1/(1 - 0.935) = 15.3846$ in Model 2, against $1/(1 - 0.300) = 1.4286$ in Model 1. The sampling variance of a coefficient is proportional to its VIF, so with the MSE and the variance of BDI unchanged the standard error rises by $\sqrt{15.3846 / 1.4286} = \sqrt{10.7692} = 3.2817$. The Exhibit 3 ratio $0.1383 / 0.0420 = 3.2929$ is slightly larger because the MSE rises from $5{,}832.4/104 = 56.0808$ to about 56.4805 when a degree of freedom is lost. A is wrong because it uses the squared pairwise correlation as $R_j^2$: $1/(1 - 0.95^2) = 10.2564$ and $\sqrt{10.2564/1.4286} = 2.6795$; with more than two regressors the auxiliary $R^2$, not the pairwise correlation, determines the VIF. C is wrong because it reports the variance ratio, 10.7692, as the standard error ratio instead of taking its square root.
> 4. **B.** The CAPE series is a component of the BDI, so adding it violates parsimony and economic reasoning: it raises $R^2$ only from 0.4698 to 0.4712, lowers adjusted $R^2$ from 0.4546 to 0.4507, and creates serious multicollinearity (VIF 15.38 > 10). The correct specification is Model 1, whose BDI VIF of 1.43 raises no concern, with Newey-West standard errors because questions 1 and 2 found conditional heteroskedasticity and serial correlation: $t = 0.2150 / 0.0588 = 3.6565 > 1.983$, so the BDI exposure is significant at 5%. A is wrong because $t = 0.1320 / 0.1936 = 0.6818$ is small only because multicollinearity inflates the standard error; concluding there is no exposure is a Type II error, and the correction is to drop the redundant regressor, not to reinterpret the model. C is wrong because White standard errors correct only for heteroskedasticity; $t = 0.2150 / 0.0512 = 4.1992$ still overstates significance because it ignores the serial correlation found in question 2.
>
> **Distractor design**
>
> 1. A uses the auxiliary regression's F-statistic in place of $nR^2$; C counts the intercept in the chi-square degrees of freedom.
> 2. A trusts the first-order Durbin-Watson test over the Breusch-Godfrey test; C divides by the total instead of the residual sum of squares and applies the lagged-dependent-variable consequence to a model without one.
> 3. A uses the squared pairwise correlation instead of the auxiliary $R^2$; C reports the variance inflation ratio as the standard error ratio.
> 4. A reads a multicollinearity-inflated standard error as absence of exposure; C uses heteroskedasticity-only standard errors when serial correlation is also present.

> [!success]- Item set 5 (06-02)
> 1. **C.** Adjacent rates at the same date satisfy $i_H = i_L e^{2\sigma}$, so $\sigma = \ln(i_H / i_L)/2$.
> $i_H / i_L = 3.2072\% / 2.4239\% = 1.3232$, $\ln(1.3232) = 0.2800$, and $\sigma = 0.2800 / 2 = 0.1400$, or 14.0%.
> The Time 2 rates confirm it: $3.3244\% / 2.5125\% = 4.3986\% / 3.3244\% = 1.3231 = e^{0.28}$.
> A is wrong because it forgets to halve the log ratio, treating adjacent nodes as one standard deviation apart ($\ln 1.3232 = 28.0\%$).
> B is wrong because it uses a linear spacing, $(1.3232 - 1)/2 = 16.2\%$, instead of the lognormal relation.
> 2. **B.** Discount each cash flow by the cumulative product of the rates along path HL.
> Discount factors: $1/1.018 = 0.982318$; $1/(1.018 \times 1.032072) = 0.951792$; $1/(1.018 \times 1.032072 \times 1.033244) = 0.921169$.
> Present value: $2.00 \times 0.982318 + 3.00 \times 0.951792 + 104.50 \times 0.921169 = 1.9646 + 2.8554 + 96.2622 = 101.0822$.
> The four path values are 100.0917 (HH), 101.0822 (HL), 101.8402 (LH), and 102.6084 (LL); their average, 101.4056, equals the backward induction value and the spot-rate value on spots of 1.8000%, 2.3058% and 2.6639%.
> A is wrong because it discounts each cash flow at the single rate for its period raised to its time, $2/1.018 + 3/1.032072^2 + 104.50/1.033244^3 = 99.5155$, instead of compounding across the path.
> C is wrong because it misreads the path convention and values path LH (lower rate at Time 1, then the middle rate), which gives 101.8402.
> 3. **A.** Statement 1 describes calibration correctly: each date is solved after the earlier dates are fixed, the Time 2 rates are tied together by $e^{2\sigma}$ spacing, and the lowest rate is iterated until the benchmark par bond for that maturity prices at 100.
> Statement 2 is incorrect because a higher volatility spreads the calibrated rates farther apart around the implied forward rate: the upper rate rises and the lower rate falls.
> Recalibrating Exhibit 1 at 20% volatility moves the Time 1 rates to 3.3731% and 2.2611%, so the lower rate falls from 2.4239%.
> B and C are wrong because they accept Statement 2, which reverses the effect of volatility on the lower node.
> 4. **B.** Statement 3 is correct: modelers commonly impose mean reversion on the simulated rates through upper and lower bounds on the rate process.
> Statement 4 is incorrect because the drift adjustment is one constant added to all rates on all paths until the average present value across paths of each benchmark equals its market price; individual paths are not forced to reprice the benchmarks.
> A and C are wrong because they accept Statement 4, which replaces the single drift adjustment with path-by-path fitting.
>
> **Distractor design**
>
> 1. A: log ratio not halved (nodes treated as one standard deviation apart); B: linear rather than lognormal spacing.
> 2. A: per-period rates applied independently instead of cumulative path discounting; C: path convention misread (LH valued instead of HL).
> 3. B and C: effect of higher volatility on the lower node reversed.
> 4. A and C: drift adjustment misdescribed as path-by-path fitting rather than one constant on all paths that reprices benchmarks on average.

> [!success]- Item set 6 (10-01)
> 1. **B.** Standard III(D) requires reasonable efforts to ensure that performance information is fair, accurate, and complete (V10 p.15).
> Accounts D and E were managed under the strategy for the full year, so dropping them because they later left produces a survivor-only figure that is not complete.
> Asset-weighted return of all five accounts, using beginning market values as weights: $42.0(0.135) + 28.0(0.152) + 18.0(0.118) + 7.0(-0.064) + 5.0(-0.090) = 5.6700 + 4.2560 + 2.1240 - 0.4480 - 0.4500 = 11.1520$.
> Total beginning value $= 100.0$, so the return is $11.1520/100.0 = 0.1115$, or $11.15\%$, which beats the benchmark by $11.15 - 10.40 = 0.75$ percentage points, not 3.3.
> Fournier's figure is $12.0500/88.0 = 0.1369$, or $13.69\%$, because it omits D and E.
> A is wrong because it equal-weights the five accounts: $(13.5 + 15.2 + 11.8 - 6.4 - 9.0)/5 = 25.1/5 = 5.02\%$, ignoring the beginning-value weighting that Kestrel's own method uses.
> C is wrong because it weights by ending market values ($47.6700, 32.2560, 20.1240, 6.5520, 4.5500$, total $111.1520$), giving $0.1159$, or $11.59\%$; ending weights already contain each account's return and overweight the winners.
> The model portfolio (19.0%) is a decoy: it holds no client assets, so it has zero weight in an asset-weighted return, and blending it in would itself misstate actual performance.
> 2. **B.** Mbeki is correct: VI(C) requires disclosure to clients and prospective clients, as appropriate, of any compensation paid to others for recommending the member's services (V10 p.17), and I(A) requires members to follow the more strict rule when the Code and Standards conflict with applicable law (V10 p.14).
> Silence in provincial rules therefore does not remove the VI(C) obligation.
> Haddad is wrong because the two items engage different sub-standards.
> Item 1 exaggerates what holding the CFA charter implies, which is VII(B) Reference to CFA Institute, the CFA Designation, and the CFA Program (V10 p.17).
> Item 2 presents another firm's work as Kestrel's own, which is a misrepresentation relating to investment analysis under I(C) (V10 p.14).
> A is wrong because it sends the designation claim to I(C) on the general idea of overstatement, when the sub-standard that names the specific behaviour is VII(B).
> C is wrong because it accepts Haddad's single-sub-standard mapping as well.
> 3. **B.** The second Code component reads in full "Place the integrity of the investment profession and the interests of clients above their own personal interests", so Quotation X is complete (V10 p.13).
> The third component reads "Use reasonable care and exercise independent professional judgment when conducting investment analysis, making investment recommendations, taking investment actions, and engaging in other professional activities", so Quotation Y drops two of the four activities (V10 p.13).
> A is wrong because Quotation Y is truncated and reads as complete only if the four activities are not remembered.
> C is wrong because it imports the "before the employer's" wording of Standard III(A) into the Code, and the second Code component does not mention employers (V10 p.15).
> 4. **A.** For members, the sanctions include public censure, suspension of membership and use of the CFA designation, and revocation of the CFA charter; candidates who violate the Code and Standards or testing policies are subject to suspension or prohibition from further participation in the CFA Program (V10 p.8).
> The Code and Standards apply to every member and candidate individually, regardless of job function (V10 p.13), and Haddad in addition has a duty under IV(C) to make reasonable efforts to ensure that Fournier, who is under his supervision, complies (V10 p.16).
> B is wrong because it adopts Haddad's claim that public censure is the ceiling for a candidate; suspension or prohibition from the program is the candidate sanction.
> C is wrong because it clears the supervising member, whose own conduct and IV(C) duty are at issue, and it applies a charterholder sanction to a candidate who holds no charter.
>
> **Distractor design**
>
> 1. A: equal weights in place of beginning-value weights (wrong weighting scheme); C: ending market values used as weights (weights contaminated by the period's returns).
> 2. A: designation exaggeration mislabelled as I(C) because both overstate (VII(B) versus I(C)); C: the same mislabelling plus acceptance of the correct I(A) point.
> 3. A: truncated third component accepted as complete; C: III(A) "before employer" wording grafted onto the second Code component.
> 4. B: candidate sanction capped at public censure (Haddad's error); C: supervisor wrongly cleared and a member sanction applied to a candidate.

> [!success]- Item set 7 (09-02)
> 1. **A.** Apply $IR = TC \times IC \times \sqrt{BR}$, with breadth adjusted for correlation, $BR = N/[1 + (N-1)\rho]$, and for truly independent decisions over time.
> Cobalt Ridge: $BR = 12/[1 + 11(-0.06)] = 12/0.34 = 35.2941$, so $IR = 0.85 \times 0.06 \times 5.9409 = 0.3030$.
> Larchmont: per quarter $BR = 20/[1 + 19(0.20)] = 20/4.80 = 4.1667$; four independent quarters give $BR = 16.6667$, so $IR = 0.75 \times 0.08 \times 4.0825 = 0.2449$.
> Pinecrest: the persistent score means monthly rebalancing does not add independent decisions, so $BR = 500$ and $IR = 0.65 \times 0.015 \times 22.3607 = 0.2180$.
> B is wrong because it ignores the correlation adjustments: Larchmont at $BR = 80$ gives $0.75 \times 0.08 \times 8.9443 = 0.5367$, while Cobalt at $BR = 12$ falls to $0.1767$.
> C is wrong because it accepts the pitch-book breadth of 6,000: $0.65 \times 0.015 \times 77.4597 = 0.7552$.
> The realized 3-year IRs are ex post and do not measure expected skill; ranking by them would also point to Larchmont.
> 2. **B.** Expected active return $= IR \times \sigma_A = 0.3030 \times 5.0 = 1.5149\%$, and expected benchmark excess return $= 0.32 \times 15.5 = 4.9600\%$.
> Expected excess return of the allocation $= 4.9600 + 1.5149 = 6.4749\%$.
> Total risk $= \sqrt{15.5^2 + 5.0^2} = 16.2865\%$, because benchmark and active returns are uncorrelated.
> Sharpe ratio $= 6.4749/16.2865 = 0.3976$.
> This is below the maximum because 5.0% is far below the optimal active risk of $(0.3030/0.32) \times 15.5 = 14.68\%$.
> A is wrong because it adds benchmark risk and active risk in levels: $6.4749/(15.5 + 5.0) = 0.3159$.
> C is wrong because it assumes the delivered active risk is optimal and reports $\sqrt{0.32^2 + 0.3030^2} = 0.4407$.
> 3. **B.** The unconstrained IR is $IR^{*} = IC\sqrt{BR} = 0.06 \times 5.9409 = 0.3565$.
> Under the caps, $IR = 0.55 \times 0.3565 = 0.1960$, and $SR_P = \sqrt{SR_B^2 + TC^2 (IR^{*})^2} = \sqrt{0.32^2 + 0.1960^2} = 0.3753$.
> A is wrong because it applies the new TC to the already constrained IR: $0.55 \times 0.3030 = 0.1666$, and $\sqrt{0.32^2 + 0.1666^2} = 0.3608$.
> C is wrong because it does not square TC: $\sqrt{0.32^2 + 0.55 \times 0.3565^2} = 0.4151$.
> 4. **C.** Strategy risk: $\sigma_A = \sigma_{IC}\sqrt{N}\,\sigma_{RM} = 0.10 \times \sqrt{225} \times 2.0 = 0.10 \times 15 \times 2.0 = 3.0\%$.
> Expected active return $= (IC/\sigma_{IC})\,\sigma_A = (0.04/0.10) \times 3.0 = 1.20\%$, so the IR is $1.20/3.0 = 0.40$.
> The naive law gives $IR = 0.04\sqrt{225} = 0.60$, so the adjusted IR is $0.40/0.60 = 66.67\%$ of the naive figure, inside the 45% to 91% range the curriculum cites.
> The expected active return is the same 1.20% as the naive law at 2.0%; strategy risk raises the risk, not the return.
> A is wrong because it ignores strategy risk and uses the risk-model active risk with the naive IR.
> B is wrong because it raises active risk to 3.0% but applies the naive law at that risk, $0.60 \times 3.0 = 1.80\%$, which scales the return up with the risk.
> Last year's realized IC of 0.07 is a single observation, not the expected IC.
>
> **Distractor design**
>
> 1. B: correlation adjustment to breadth ignored; C: naive time-series breadth accepted for a persistent signal.
> 2. A: benchmark and active risk added in levels instead of variances; C: delivered active risk assumed optimal, maximum Sharpe ratio reported.
> 3. A: new transfer coefficient applied to the already constrained IR (TC counted twice); C: transfer coefficient not squared in the constrained Sharpe relation.
> 4. A: strategy risk ignored (risk-model active risk and naive IR); B: naive IR applied at the strategy-risk active risk.

> [!success]- Item set 8 (02-01)
> 1. **C.** Build ZAR/EUR $= (\text{ZAR/USD}) \times (\text{USD/EUR})$ so that the USD cancels: initiation $17.85 \times 1.0820 = 19.3137$; today $19.62 \times 1.1040 = 21.6605$ (Python: 21.66048) (V2 p.40).
> The rand's price in EUR is $1/19.3137$ at initiation and $1/21.6605$ today, so the gross return in EUR $= \dfrac{1/21.6605}{1/19.3137} \times 1.0825 - 1 = 19.3137 \times 1.0825/21.6605 - 1 = -3.4782\%$.
> Net of the 3.40% EUR funding cost: $-3.4782\% - 3.40\% = -6.8782\% \approx -6.88\%$.
> Check on EUR 1,000,000: buy ZAR 19,313,700, grow it to ZAR 20,907,080.25, convert back to EUR 965,217.77, and repay EUR 1,034,000, a loss of EUR 68,782.23.
> The rand fell $19.3137/21.6605 - 1 = -10.83\%$ against the euro, more than the 4.85% yield spread, which is the crash risk that gives carry returns their negative skew (V2 p.38, p.39).
> A is wrong because it is the gross return and forgets to subtract the EUR funding cost.
> B is wrong because it runs the trade through the ZAR/USD rate alone, $17.85 \times 1.0825/19.62 - 1 = -1.5157\%$, less 3.40% gives $-4.9157\%$, ignoring the euro's move against the dollar from 1.0820 to 1.1040.
> 2. **A.** Relative PPP moves the 2014 fair value by the ratio of the price level changes: PPP ZAR/EUR today $= 14.40 \times 162.8/128.6 = 14.40 \times 1.265941 = 18.2295$ (V2 p.30).
> Today's market rate is 21.6605, so one euro buys more rand in the market than PPP warrants and the rand is cheap.
> Market value of the rand in EUR relative to its PPP value $= (1/21.6605)/(1/18.2295) - 1 = 18.2295/21.6605 - 1 = -15.84\%$, an undervaluation of about 15.8%.
> Such deviations are a long-run anchor rather than a short-run signal, since PPP has little explanatory power at a one-year horizon but strong power at five years and beyond (V2 p.31, p.32).
> B is wrong because it adds the cumulative inflation differential instead of taking the ratio of the price indexes: $14.40 \times (1 + 0.628 - 0.286) = 19.3248$, giving $19.3248/21.6605 - 1 = -10.78\%$; the additive approximation drops the cross-product term, which becomes large over a multi-year horizon with high cumulative inflation.
> C is wrong because it computes $21.6605/18.2295 - 1 = +18.82\%$, which is the euro's overvaluation measured on the wrong base, and then reads the higher ZAR/EUR rate as a stronger rand.
> 3. **B.** Persistent current account deficits tend to weaken a currency over the long run, but in the short run the capital account dominates because financial asset prices and portfolio positions adjust almost instantly while goods prices, production, and trade demand respond with long lags (V2 p.40, p.41).
> Net portfolio inflows rising from 2.1% to 5.4% of GDP more than financed the wider 3.9% deficit, which explains the rand's early strength without implying that the current account is irrelevant.
> A is wrong because a current account deficit increases the supply of the deficit country's currency under the flow supply and demand channel, which puts downward, not upward, pressure on the rand.
> C is wrong because under the debt sustainability channel a rising external debt ratio leads markets to revise the deficit country's long-run equilibrium value downward, not upward.
> 4. **B.** Both economies have high capital mobility, so each policy mix works through real interest rates and capital flows (V2 p.49).
> The euro area pairs expansionary monetary policy with restrictive fiscal policy, which lowers real rates and depreciates the EUR.
> South Africa pairs restrictive monetary policy with expansionary fiscal policy, which raises real rates and appreciates the ZAR.
> Both effects push the ZAR/EUR rate, the price of one euro in rand, down, so it falls.
> A is wrong because it reads a stronger rand as a higher ZAR/EUR rate, reversing the quote direction.
> C is wrong because it applies the low capital mobility table, in which mixed monetary and fiscal combinations are indeterminate (V2 p.50); the portfolio balance concern about rising South African debt is a long-run effect that Richter has set aside.
>
> **Distractor design**
>
> 1. A: forgets the funding cost (gross versus net); B: runs the trade through the ZAR/USD leg only, so the USD does not cancel (wrong cross rate).
> 2. B: adds the cumulative inflation differential instead of using the price index ratio (wrong formula variant); C: measures the misvaluation on the wrong base and misreads the quote direction (base and sign).
> 3. A: reverses the flow supply and demand effect of a deficit (sign); C: reverses the debt sustainability effect (sign).
> 4. A: misreads the direction of the ZAR/EUR quote (quote direction); C: applies the low capital mobility table to open economies (misread exhibit assumption).

> [!success]- Item set 9 (01-07)
> 1. **C.** Adding dine-in, delivery, and catering sales into one total sales variable combines two or more variables into one, which is aggregation, the curriculum's salary plus other income example (V1 p.284).
> Deleting rows that are not needed, here the locations closed before the sample period, is filtration (V1 p.284).
> Translating CAD into USD is conversion, which covers currency, units, and data types (V1 p.285).
> Action 4, deleting an unneeded column, is the selection case and is a decoy.
> A is wrong because selection removes columns, not rows; Action 2 removes rows.
> B is wrong because extraction creates a new variable from a single existing one, such as age from a date of birth, whereas Action 1 sums several variables into one.
> 2. **B.** Rescaling to mean 0 and standard deviation 1 is standardization, which suits this variable because its distribution is close to normal and the three standard deviation check found no outliers (V1 p.285, p.286).
> $X^{\text{std}} = (7{,}005 - 4{,}820) / 1{,}150 = 2{,}185 / 1{,}150 = 1.9000$.
> A is wrong because $(7{,}005 - 1{,}610) / (8{,}190 - 1{,}610) = 5{,}395 / 6{,}580 = 0.8199$ is the normalized value on a scale of 0 to 1, which is not the rescaling Wierzbicki chose.
> C is wrong because $(7{,}005 - 4{,}550) / 1{,}150 = 2{,}455 / 1{,}150 = 2.1348$ centres on the median instead of the mean.
> 3. **C.** Mutual information is 0 when a token is distributed the same way across classes and approaches 1 as the token concentrates in one class, so the highest value, 0.0694 for "cold", marks the most discriminating token (V1 p.302, p.303).
> A is wrong because "food" has the lowest mutual information, 0.0006, so it appears in positive and negative reviews almost equally; choosing it reads the measure backwards.
> B is wrong because "order" has the highest collection-level term frequency, 0.0184, but frequency measures how common a token is, not whether it separates the classes; the most frequent tokens behave like stop words and cause underfitting (V1 p.302).
> 4. **A.** Buying ahead of a quarter that turns out to be a miss means the model predicted 1 when the actual was 0, a false positive or Type I error, so precision is the relevant measure (V1 p.312, p.313).
> $P = TP / (TP + FP) = 116 / (116 + 44) = 116 / 160 = 0.7250$.
> B is wrong because recall, $116 / (116 + 28) = 116 / 144 = 0.8056$, guards against false negatives, the missed beats that Nwankwo says cost little.
> C is wrong because accuracy, $(116 + 212) / 400 = 328 / 400 = 0.8200$, weights both error types equally and is inflated by the majority miss class (256 of 400 actual outcomes, so a model that always predicts a miss scores 0.64); for reference, $F_1 = 2 \times 0.7250 \times 0.8056 / (0.7250 + 0.8056) = 1.1681 / 1.5306 = 0.7632$ (V1 p.313, p.314).
>
> **Distractor design**
>
> 1. A: treats row removal (filtration) as column removal (selection); B: labels a sum of several variables as extraction instead of aggregation.
> 2. A: wrong formula variant (normalization instead of standardization); C: misread exhibit, centring on the median instead of the mean.
> 3. A: reads mutual information backwards (lowest instead of highest); B: confuses high term frequency with discriminatory power.
> 4. B: reverses Type I and Type II cost (recall instead of precision); C: picks the headline accuracy measure, which ignores the stated asymmetric cost.

> [!success]- Item set 10 (04-01)
> 1. **C.** Special dividend per share $= 90 / 50 = 1.80$ and the ex-dividend price is $18.00 - 1.80 = 16.20$.
> Dividend route: cash $100{,}000 \times 1.80 = 180{,}000$, tax $0.30 \times 180{,}000 = 54{,}000$, so after-tax cash is 126,000; shares are worth $100{,}000 \times 16.20 = 1{,}620{,}000$; wealth $= 1{,}746{,}000$.
> Repurchase route: Oriel buys $90 / 18.00 = 5$ million shares, 10% of the total, so Castell sells $10{,}000$ shares for $180{,}000$.
> Her realized gain is $10{,}000 \times (18.00 - 12.00) = 60{,}000$, taxed at 20%, so tax is 12,000 and after-tax cash is 168,000; her remaining 90,000 shares are worth $90{,}000 \times 18.00 = 1{,}620{,}000$; wealth $= 1{,}788{,}000$.
> Advantage of the repurchase $= 1{,}788{,}000 - 1{,}746{,}000 = 42{,}000$.
> Only the gain above her cost basis is taxed, and at a lower rate, which is the tax advantage that leads companies and investors to prefer repurchases when capital gains are taxed more lightly than dividends (V4 p.40).
> A is wrong because the equivalence of dividends and repurchases at the market price holds only when taxes and information content are the same; here they are not (V4 p.38).
> B is wrong because it taxes the entire 180,000 of sale proceeds at 20% instead of only the 60,000 gain: tax of 36,000 leaves wealth of 1,764,000, an advantage of only 18,000, the same figure obtained by applying the 10-point rate difference to the full distribution.
> 2. **C.** BVPS before the repurchase $= 18.00 / 0.80 = 22.50$, so book equity $= 22.50 \times 50 = 1{,}125$ million.
> After spending 90 million to buy 5 million shares: $BVPS = (1{,}125 - 90) / (50 - 5) = 1{,}035 / 45 = 23.0000$.
> BVPS rises because the repurchase price of 18.00 is below the pre-repurchase BVPS of 22.50, so Lindqvist is right on this point (V4 p.37).
> A is wrong because it inverts the price-to-book ratio, $BVPS = 18.00 \times 0.80 = 14.40$, giving equity of 720 million and $(720 - 90) / 45 = 14.0000$.
> B is wrong because it divides the reduced equity by the original share count: $1{,}035 / 50 = 20.7000$.
> 3. **C.** A debt-financed repurchase leaves EPS unchanged when the after-tax cost of debt equals the earnings yield (V4 p.36).
> Earnings yield $= 1 / 12.5 = 8.00\%$, so the breakeven after-tax rate is 8.00% and the breakeven pretax rate is $0.08 / (1 - 0.25) = 10.6667\%$.
> The lenders' quoted 7.2% pretax is $7.2\% \times 0.75 = 5.40\%$ after tax, below the earnings yield, so the proposed loan would be accretive.
> A is wrong because it multiplies the earnings yield by $(1 - t)$ instead of dividing: $0.08 \times 0.75 = 6.00\%$.
> B is wrong because it compares the earnings yield directly with the pretax borrowing rate, ignoring the tax deductibility of interest.
> 4. **A.** $FCFE = CFO - FCInv + \text{Net borrowing} = 121 - 58 - 17 = 46$ million (V4 p.50).
> Distributions $= 36$ regular dividends $+ 90$ repurchase $= 126$ million.
> FCFE coverage $= 46 / 126 = 0.3651$ (V4 p.49).
> A ratio well below 1 means distributions exceed the cash generated in the year; here the 80 million shortfall is met from the accumulated 90 million of surplus cash, a one-time drawdown rather than borrowing, so the ratio should not be read as a recurring policy.
> B is wrong because it adds the debt repayment instead of subtracting it: $(121 - 58 + 17) / 126 = 80 / 126 = 0.6349$.
> C is wrong because it leaves the repurchase out of the denominator: $46 / 36 = 1.2778$.
>
> **Distractor design**
>
> 1. A: dividend-repurchase equivalence applied despite different tax rates (condition ignored); B: capital gains tax applied to full proceeds rather than to the gain over cost basis (wrong tax base).
> 2. A: price-to-book ratio inverted when deriving BVPS (misread exhibit); B: post-repurchase equity divided by pre-repurchase share count (mismatched numerator and denominator).
> 3. A: earnings yield multiplied rather than divided by $(1 - t)$ (wrong formula variant); B: pretax borrowing rate compared directly with the earnings yield (before-tax vs after-tax).
> 4. B: debt repayment added to FCFE (sign error on net borrowing); C: repurchases omitted from the coverage denominator (wrong formula variant).

> [!success]- Item set 11 (03-03)
> 1. **C.** Nordic prices from the CAD price list, buys in CAD, remits cash weekly and is financed by the parent, so it is an extension of the parent and its functional currency is the CAD; the location and bookkeeping currency define only the local currency (V3 p.135, p.136).
> A parent-currency functional currency calls for the temporal method (V3 p.138).
> Arvenia's functional currency would be the ARL, but US GAAP overrides that for a highly inflationary economy and requires the temporal method as if the parent's currency were functional, with no inflation restatement (V3 p.141, p.157).
> A is wrong because it treats the local currency as the functional currency for Nordic, the error in Solheim's first statement.
> B is wrong because inflation restatement followed by translation at the current rate is the IFRS (IAS 29) approach, which a US GAAP reporter may not use, the error in Solheim's second statement.
> 2. **A.** Sales are translated at the average rate under both methods (V3 p.140).
> Translated sales: 2024 $480 \times 0.1290 = 61.9200$; 2025 $516 \times 0.1245 = 64.2420$ (CAD millions); reported growth $64.2420 / 61.9200 - 1 = 3.75\%$.
> Constant-currency sales at the 2024 average rate: $516 \times 0.1290 = 66.5640$, growth $7.50\%$, equal to SEK growth $516 / 480 - 1$.
> Foreign exchange component $= 3.75\% - 7.50\% = -3.75$ percentage points (V3 p.172, p.173).
> B is wrong because it uses the percentage change in the rate, $0.1245 / 0.1290 - 1 = -3.49\%$, as the growth component; the rate change also applies to the SEK36 million of new sales, so the component is the gap between reported and constant-currency growth.
> C is wrong because it reports local currency growth as if translation left growth unchanged.
> 3. **B.** Under the temporal method only monetary items are exposed: $12 + 18 - 10 - 55 = -35$ ARL million, a net monetary liability (V3 p.139).
> With balances essentially constant through the year, the ARL's fall from 0.0500 to 0.0320 shrinks that liability in CAD by $35{,}000{,}000 \times (0.0500 - 0.0320) = 630{,}000$, a remeasurement gain (V3 p.134, p.158).
> Under the temporal method the gain goes to net income (V3 p.138).
> A is wrong because it counts inventory as a monetary asset: $(12 + 18 + 25 - 10 - 55) \times 0.0180 = -10 \times 0.0180$, a gain of $180{,}000$.
> C is wrong because it places the result in other comprehensive income as a translation adjustment, the current rate method treatment.
> 4. **C.** Annual depreciation is $90 / 10 = 9$ ARL million.
> US GAAP (temporal): depreciation at the historical rate of the equipment, $9{,}000{,}000 \times 0.0800 = 720{,}000$, so the charge does not shrink as the ARL collapses (V3 p.138, p.141).
> IFRS (IAS 29, then current rate): restate from the acquisition-date index, $9{,}000{,}000 \times 240 / 100 = 21{,}600{,}000$ ARL, then translate at the closing rate, $21{,}600{,}000 \times 0.0320 = 691{,}200$ (V3 p.142, p.143, p.158).
> The two differ because the ARL fell $1 - 0.0320 / 0.0800 = 60\%$ in CAD while prices rose $140\%$; only if the rate had fallen exactly in line with the index, to $0.0800 / 2.4 = 0.0333$, would the two frameworks agree (V3 p.159, p.161).
> A is wrong because it translates unrestated historical cost at the closing rate for the US GAAP figure, $9{,}000{,}000 \times 0.0320 = 288{,}000$, the disappearing-plant result neither standard allows.
> B is wrong because it restates depreciation from the 2025 average index as if it were an expense incurred evenly during the year: $9{,}000{,}000 \times 240 / 180 \times 0.0320 = 384{,}000$; depreciation is restated from the date the asset was acquired.
>
> **Distractor design**
>
> - Q1: A treats location and bookkeeping currency as the functional currency; B applies the IFRS hyperinflation approach to a US GAAP reporter.
> - Q2: B uses the pure rate change instead of the reported minus constant-currency gap (wrong formula variant); C assumes translation preserves growth; the year-end rates are decoys, since sales use average rates.
> - Q3: A classifies inventory as monetary (misread exhibit); C puts a temporal-method result in OCI (current rate placement); the average rate 0.0400 is a decoy.
> - Q4: A is the disappearing-plant error (closing rate on unrestated cost under US GAAP); B restates a cost-based expense from the average index instead of the acquisition index.

> [!success]- Item set 12 (04-04)
> 1. **A.** A spun-off company trades without a control premium, so comparable company analysis with listed peers is the appropriate method.
> Peer multiples sorted are 10.5, 12.0, 14.5, 17.0, 19.5, so the median is 14.5x.
> Quellis EBITDA net of its own corporate costs $= 180 - 18 = 162$.
> $EV = 14.5 \times 162 = 2{,}349$.
> B is wrong because it ignores the standalone corporate costs Quellis will bear: $14.5 \times 180 = 2{,}610$.
> C is wrong because it applies the acquisition multiple, which embeds a takeover premium that a spun-off company's shares will not carry: $18.2 \times 162 = 2{,}948.4$.
> 2. **B.** Vantorra after the separation: EBITDA $= 520 - 52 = 468$; $EV = 9.0 \times 468 = 4{,}212$.
> Net debt $= (3{,}000 - 800) - 200 = 2{,}000$; equity $= 4{,}212 - 2{,}000 = 2{,}212$; per share $= 2{,}212/240 = 9.2167$.
> Quellis equity $= 2{,}349 - 800 = 1{,}549$; Quellis shares $= 240/3 = 80$ million, worth $1{,}549/80 = 19.3625$ each, or $19.3625/3 = 6.4542$ per Vantorra share held today.
> Combined value $= 9.2167 + 6.4542 = 15.6708$, which is $15.6708/14.00 - 1 = 11.93\%$ above the current price.
> Equivalently, the sum of the two enterprise values, $4{,}212 + 2{,}349 = 6{,}561$, exceeds Vantorra's trading EV of $240 \times 14.00 + 2{,}800 = 6{,}160$ by 401, even after the EUR10 million a year of dis-synergies ($52 + 18 - 60$).
> A is wrong because it deducts Vantorra's pre-separation net debt of 2,800, ignoring the repayment funded by the special dividend: $(4{,}212 - 2{,}800)/240 + 6.4542 = 5.8833 + 6.4542 = 12.3375$.
> C is wrong because it ignores the EUR800 million Quellis borrows, counting the special dividend twice: $9.2167 + 2{,}349/240 = 9.2167 + 9.7875 = 19.0042$.
> 3. **B.** Before the separation: EBITDA $= 520 + 180 - 60 = 640$; EBIT $= 640 - 170 = 470$; EBT $= 470 - 0.05 \times 3{,}000 + 0.02 \times 200 = 470 - 150 + 4 = 324$; net income $= 243$; EPS $= 243/240 = 1.0125$.
> After the separation: EBIT $= 468 - 120 = 348$; interest expense $= 0.05 \times 2{,}200 = 110$; interest income $= 4$.
> EBT $= 348 - 110 + 4 = 242$; tax $= 60.5$; net income $= 181.5$.
> A spin off is a stock dividend of Quellis shares, so Vantorra's share count stays at 240 million: EPS $= 181.5/240 = 0.7563$.
> A is wrong because it keeps the pre-separation interest expense, ignoring the EUR800 million debt repayment: $(348 - 150 + 4) \times 0.75 = 151.5$, and $151.5/240 = 0.6313$.
> C is wrong because it treats the distribution like a share repurchase and cuts Vantorra's share count by one-third: $181.5/160 = 1.1344$.
> 4. **B.** Once a restructuring is announced, the market prices in its expected impact immediately, including the risk that it is not completed, so the current share price already reflects it.
> A is wrong because research finds no correlation between announcement-day returns and excess returns two or more years later; the price reaction is not a verdict on long-run value creation.
> C is wrong because a spin off creates two independent companies without concentrating market power, so it avoids the antitrust scrutiny that a sale to a competitor can attract.
> Its execution risk comes from the several quarters needed to separate the businesses and from leaving the valuation to the market.
>
> **Distractor design**
>
> 1. B skips the standalone corporate costs of the spun-off company; C applies a transaction multiple, with its embedded control premium, to a spin off.
> 2. A omits the debt repayment funded by the special dividend; C ignores the debt the spun-off company takes on and double counts the dividend.
> 3. A ignores the interest saved on the repaid debt; C reduces the parent's share count as if the spin off were a buyback.
> 4. A trusts the announcement-day return; C reverses the regulatory advantage of a spin off over a sale to a competitor.

> [!success]- Item set 13 (06-04)
> 1. **A.** Use the BBB row and the ten-year bucket, where Bond L's current spread is 1.70%.
> Price change for each migration $= -7.30 \times (s_i - 1.70\%)$: AAA $+8.0300\%$; AA $+6.2050\%$; A $+4.0150\%$; BBB $0$; BB $-13.1400\%$; B $-33.5800\%$; CCC, CC, C $-59.8600\%$.
> Weighted: $(0.0002)(8.0300) + (0.0035)(6.2050) + (0.0520)(4.0150) + (0.8610)(0) + (0.0580)(-13.1400) + (0.0140)(-33.5800) + (0.0083)(-59.8600)$.
> $= 0.0016 + 0.0217 + 0.2088 + 0 - 0.7621 - 0.4701 - 0.4968 = -1.4970\%$ (full precision; the rounded terms sum to $-1.4969\%$).
> Expected return $= 5.05\% - 1.4970\% = 3.5530\%$, about 3.55%.
> The 0.30% default probability is excluded under Fenwick's policy, so the transition probabilities used sum to 99.70%.
> B is wrong because it uses the five-year spread bucket for the ten-year bond (current spread 1.35%, drag $-1.2990\%$, return $3.7510\%$).
> C is wrong because it adds the migration drag to the yield instead of subtracting it ($5.05\% + 1.4970\% = 6.5470\%$).
> 2. **C.** Bond S uses the five-year bucket, current spread 1.35%, and price change $-3.70 \times (s_i - 1.35\%)$: AAA $+3.3300\%$; AA $+2.5900\%$; A $+1.6650\%$; BBB $0$; BB $-5.7350\%$; B $-14.2450\%$; CCC, CC, C $-26.8250\%$.
> Weighted: $0.0007 + 0.0091 + 0.0866 + 0 - 0.3326 - 0.1994 - 0.2226 = -0.6584\%$ (full precision; the rounded terms sum to $-0.6582\%$).
> Expected return on Bond S $= 4.60\% - 0.6584\% = 3.9416\%$.
> Difference: $3.9416\% - 3.5530\% = 0.3886\%$, so Bond S is ahead by about 39 bps.
> The longer duration of Bond L magnifies the downgrade-skewed spread changes, and its larger migration drag (1.50% versus 0.66%) more than offsets its 45 bp yield advantage, so Grieco's comment is wrong.
> A is wrong because it compares the yields to maturity only, which is Grieco's reasoning and ignores migration.
> B is wrong because it values both bonds with the five-year spread bucket, so Bond L's return is $3.7510\%$ and the gap is $3.9416\% - 3.7510\% = 0.1906\%$.
> 3. **A.** In the structural model, equity is a long call on the assets struck at the face value of debt, and debt equals a default-free bond minus a put on the assets struck at the same face value.
> Higher asset volatility raises the value of both options, so equity (the call) gains, debt (which is short the put) loses, and the probability mass of the asset distribution below the default barrier grows, so the probability of default rises.
> B is wrong because it treats equity as losing value with higher risk; limited liability caps the shareholders' downside, so the option value of equity rises with volatility.
> C is wrong because a fixed face value does not make the debt's value fixed; the debtholders have written the put to shareholders, and the value of that put rises with volatility.
> 4. **B.** A covered bond is a senior obligation of the bank with dual recourse to Sundby and the cover pool, and the cover pool is dynamic: nonperforming assets must be replaced.
> The mortgages stay on Sundby's balance sheet, whereas in the RMBS the true sale to a bankruptcy-remote SPE leaves the investors dependent on the pool and the deal structure, with the servicer creating operational and counterparty risk but no claim on Sundby.
> A is wrong because servicing the loans does not give investors recourse to the originator; the true sale is designed to separate the pool from Sundby's credit.
> C is wrong because it describes a hard bullet; under a conditional pass-through structure, a missed scheduled payment converts the covered bond into a pass-through security after the original maturity date, and payments are passed through as the cover pool generates cash.
>
> **Distractor design**
>
> 1. B: wrong spread bucket used (five-year spreads for a ten-year bond, misread exhibit); C: migration drag added to YTM instead of subtracted (sign).
> 2. A: yield comparison without the migration adjustment; B: five-year bucket applied to both bonds (misread exhibit carried from Question 1).
> 3. B: equity treated as a risky claim that loses value with volatility instead of a call option; C: debt treated as a fixed claim, ignoring the written put.
> 4. A: servicer role confused with recourse to the originator; C: hard bullet confused with conditional pass-through.

> [!success]- Item set 14 (03-01)
> 1. **B.** Bond D is at amortized cost, with interest income at the 5.0% effective rate on the opening carrying amount; the discount accretes by interest income less the coupon of $0.03 \times 200 = 6.0$.
> 2026: interest income $= 0.05 \times 185.82 = 9.2910$; carrying amount $= 185.82 + 9.2910 - 6.0 = 189.1110$.
> 2027: interest income $= 0.05 \times 189.1110 = 9.4556$; carrying amount $= 189.1110 + 9.4556 - 6.0 = 192.5665$.
> A is wrong because it stops after one period of accretion (189.11).
> C is wrong because it accretes the discount straight line, $(200 - 185.82) / 4 = 3.545$ per year, giving $185.82 + 2 \times 3.545 = 192.91$, instead of using the effective interest method.
> 2. **B.** Bond E is an FVOCI debt instrument: interest of 4.8 goes to profit or loss, and on sale the cumulative fair value gain held in OCI is reclassified to profit or loss, so the total gain in profit or loss is sale price less amortized cost (par), $123.60 - 120.00 = 3.60$.
> Security F is an FVOCI equity instrument: only the dividend of 1.5 reaches profit or loss, and the gain of $49.00 - 40.00 = 9.00$ stays in equity and is never recycled.
> Total $= 4.8 + 3.6 + 1.5 = 9.9$.
> A is wrong because it applies the equity no-recycling rule to Bond E as well, $4.8 + 1.5 = 6.3$.
> C is wrong because it recycles Security F's gain as though it were debt, $9.9 + 9.0 = 18.9$.
> 3. **A.** Carrying amount before impairment $= 284 + 0.30 \times 20 - 3 - 0.30 \times 30 = 284 + 6 - 3 - 9 = 278$.
> IFRS compares the carrying amount with the recoverable amount, the higher of value in use and fair value less costs to sell: $\max(251,\ 236 - 4) = \max(251,\ 232) = 251$, so the loss $= 278 - 251 = 27$.
> US GAAP writes an equity method investment down to fair value when the decline is other than temporary: loss $= 278 - 236 = 42$.
> B is wrong because it uses the lower of the two IFRS measures as the recoverable amount, $278 - 232 = 46$.
> C is wrong because it leaves the dividends out of the roll-forward, giving a carrying amount of $284 + 6 - 3 = 287$ and losses of $287 - 251 = 36$ and $287 - 236 = 51$.
> 4. **A.** Under FVPL, income is the coupon plus the change in fair value; under amortized cost it is effective interest.
> 2026: FVPL $= 6.0 + (187.40 - 185.82) = 7.58$ against 9.2910, a difference of $-1.7110$.
> 2027: FVPL $= 6.0 + (195.10 - 187.40) = 13.70$ against 9.4556, a difference of $+4.2444$.
> Combined difference $= -1.7110 + 4.2444 = +2.5335$, which equals fair value less amortized cost at the end of 2027, $195.10 - 192.5665 = 2.5335$.
> B is wrong because it compares 2027 only and ignores the 2026 shortfall of FVPL income (4.24).
> C is wrong because it adds the whole fair value change since purchase on top of the reported effective interest, $195.10 - 185.82 = 9.28$, double counting the discount accretion that is already inside the fair value change.
>
> **Distractor design**
>
> 1. A: one period instead of two (period error); C: straight-line discount accretion instead of the effective interest method (wrong formula variant).
> 2. A: FVOCI debt treated as FVOCI equity, no recycling on sale; C: FVOCI equity gain recycled as if it were debt (category swap).
> 3. B: recoverable amount taken as the lower rather than the higher of value in use and fair value less costs to sell; C: dividends omitted from the equity method roll-forward (chained carrying amount error).
> 4. B: single period compared instead of the cumulative two years (period error); C: fair value change added on top of effective interest, double counting the accretion.

> [!success]- Item set 15 (05-03)
> 1. **B.** From CFO only two adjustments remain, because depreciation and working capital investment are already inside CFO.
> Under US GAAP interest paid is in CFO, so after-tax interest is added back: $120(1 - 0.25) = 90$.
> FCInv is capital expenditures net of disposal proceeds: $260 - 20 = 240$.
> $FCFF = CFO + Int(1-t) - FCInv = 348 + 90 - 240 = 198$.
> A is wrong because it deducts working capital investment a second time: $WCInv = 40 + 25 - 18 = 47$ and $198 - 47 = 151$.
> C is wrong because it adds back the full interest instead of the after-tax amount: $348 + 120 - 240 = 228$.
> 2. **C.** Net borrowing $= 50 - 400 = -350$, counting both notes payable and long-term debt.
> $FCFE = CFO - FCInv + \text{Net borrowing} = 348 - 240 - 350 = -242$.
> Check from FCFF: $198 - 90 - 350 = -242$.
> Check from uses: $FCFE = \Delta \text{Cash} + \text{Dividends} + \text{Net share repurchases} = -272 + 60 - 30 = -242$, where the share issuance is a negative repurchase.
> A is wrong because it omits the increase in notes payable from net borrowing: $348 - 240 - 400 = -292$.
> B is wrong because it treats the share issuance as a source of FCFE: $-242 + 30 = -212$; share issues are transactions with shareholders and do not change free cash flow.
> 3. **A.** FCFF is preferred for a levered company with negative FCFE or a changing capital structure.
> FCFF is before all debt flows, so its growth reflects operating fundamentals rather than a repayment schedule, and WACC is less sensitive to changes in leverage than the cost of equity.
> B is wrong because FCFF belongs to all capital providers and is discounted at WACC; only FCFE is discounted at the required return on equity.
> C is wrong because negative FCFE points to the FCFF approach, not to a dividend model, and dividends that are not linked to capacity would be a poor basis for value.
> 4. **B.** Cost of equity $= 4.0\% + 1.20(5.5\%) = 10.6\%$.
> At the target weights, $WACC = 0.35(6.4\%)(0.75) + 0.65(10.6\%) = 1.68\% + 6.89\% = 8.57\%$.
> Firm value $= 198(1.04)/(0.0857 - 0.04) = 205.92/0.0457 = 4{,}505.9081$.
> Equity $= 4{,}505.9081 - 1{,}480 = 3{,}025.9081$, using the market value of debt; per share $= 3{,}025.9081/90 = 33.62$.
> The estimate exceeds the USD 30.00 price, so the shares are undervalued and qualify for purchase.
> A is wrong because it omits the tax shield on debt: $WACC = 0.35(6.4\%) + 6.89\% = 9.13\%$, firm value $= 205.92/0.0513 = 4{,}014.0351$, and $(4{,}014.0351 - 1{,}480)/90 = 28.16$, which reverses the conclusion.
> C is wrong because it uses the current 55/45 weights instead of the long-run target: $WACC = 0.55(4.8\%) + 0.45(10.6\%) = 7.41\%$, firm value $= 205.92/0.0341 = 6{,}038.7097$, and $(6{,}038.7097 - 1{,}480)/90 = 50.65$.
>
> **Distractor design**
>
> 1. A: WCInv subtracted from CFO although CFO already contains it (double count); C: full interest added back (before-tax vs after-tax).
> 2. A: notes payable omitted from net borrowing (missed debt layer); B: share issuance treated as a determinant of FCFE (use vs determinant).
> 3. B: FCFF matched with the cost of equity (cash flow and discount rate mismatched); C: negative FCFE taken as a reason to abandon free cash flow models (wrong model criterion).
> 4. A: debt tax shield omitted from WACC (before-tax vs after-tax), which flips the conclusion; C: current rather than target weights used in a perpetuity (misread exhibit).

> [!success]- Item set 16 (08-04)
> 1. **A.** In a stub trade, the subsidiary legs are weighted by the parent's ownership percentages, so each parent share shorted is offset by buying subsidiary shares equal to the ownership percentage.
> Because the desk is short the overvalued parent, it must be long the subsidiaries: Selwyn Chemicals shares bought $= 120{,}000 \times 0.45 = 54{,}000$ (and Brannock Logistics shares bought $= 120{,}000 \times 0.70 = 84{,}000$).
> This replicates the parent's look-through exposure to its listed stakes, so only the relative mispricing of the parent against its holdings remains.
> The share prices and betas in Exhibit 1 are not needed for the ownership-weighted hedge.
> B is wrong because it uses the 55% of Selwyn held by outside shareholders: $120{,}000 \times (1 - 0.45) = 66{,}000$.
> C is wrong because it reverses the direction of the subsidiary leg; shorting both the parent and the subsidiary would double the exposure rather than hedge it.
> 2. **A.** Statement 1 is correct: cross-border deals need two governmental approvals and so carry a higher risk of failure, which the market prices as a wider spread than a domestic friendly deal.
> Statement 2 is incorrect because it reverses both legs of the hedge.
> The desk is long Ashby (the target) and short Veldhoven (the acquirer); if the deal fails, Ashby falls back and Veldhoven rebounds toward their pre-announcement prices.
> The protection is therefore out-of-the-money calls on Veldhoven, which cover the short as the acquirer rallies, and out-of-the-money puts on Ashby, which floor the long as the target falls.
> B is wrong because the puts on the acquirer and calls on the target pay off when the position is already winning, not when the deal fails.
> C is wrong because it accepts the reversed hedge in Statement 2.
> 3. **B.** The inflation accrual received on the inflation-linked bonds cancels the realized inflation paid on the swap, and the equal long and short positions require no net outlay.
> Net rate $= 2.45\% + 2.30\% - 4.05\% = 0.70\%$, or 70 bps, well above the usual premium, which is why the trade appears only in stressed markets.
> Annual net cash flow $= 0.0070 \times 40{,}000{,}000 = 280{,}000$.
> A is wrong because it ignores the inflation swap and compares the real yield directly with the nominal yield: $(2.45\% - 4.05\%) \times 40{,}000{,}000 = -640{,}000$.
> C is wrong because it adds the trailing inflation rate instead of the swap's fixed rate, counting the inflation accrual on the bonds while forgetting that the swap pays that inflation away: $(2.45\% + 3.10\% - 4.05\%) \times 40{,}000{,}000 = 1.50\% \times 40{,}000{,}000 = 600{,}000$.
> 4. **B.** A volatility swap is a forward contract on realized volatility; the buyer receives the vega notional times realized volatility minus the strike.
> Payoff $= 150{,}000 \times (21.4 - 16.0) = 150{,}000 \times 5.4 = 810{,}000$.
> The implied volatility on the expiry date is a decoy; the swap settles on realized volatility, which is why it gives pure volatility exposure without delta hedging.
> A is wrong because it uses the implied volatility at expiry instead of realized volatility: $150{,}000 \times (19.0 - 16.0) = 450{,}000$.
> C is wrong because it gives the seller's payoff; the desk bought the swap and receives realized volatility.
>
> **Distractor design**
>
> - Q1: B uses the outside shareholders' percentage instead of the parent's ownership percentage; C reverses the direction of the subsidiary leg.
> - Q2: B and C accept the reversed failure hedge (puts on the acquirer, calls on the target).
> - Q3: A omits the inflation swap's fixed leg; C substitutes trailing inflation for the swap's fixed rate (misread exhibit).
> - Q4: A uses implied volatility at expiry instead of realized volatility; C is a sign error (seller's payoff reported for the buyer).

> [!success]- Item set 17 (07-01)
> 1. **B.** The quote is CHF per EUR, so $NA_{EUR} = 150{,}000{,}000/0.9380 = \text{EUR }159{,}914{,}712$.
> EUR PV factors: $1/[1 + 0.0260(0.5)] = 0.987167$, $1/[1 + 0.0270(1.0)] = 0.973710$, $1/[1 + 0.0278(1.5)] = 0.959969$, $1/[1 + 0.0285(2.0)] = 0.946074$, sum 3.866920.
> $r_{EUR} = (1 - 0.946074)/3.866920 \times (360/180) = 1.3946\% \times 2 = 2.7891\%$.
> Payment $= 159{,}914{,}712 \times (180/360) \times 0.027891 = \text{EUR }2{,}230{,}094$.
> A is wrong because it multiplies by the spot rate to get the euro notional, $150{,}000{,}000 \times 0.9380 = 140{,}700{,}000$, giving 1,962,135.
> C is wrong because it applies the annual rate to a half-year period, doubling the payment.
> 2. **A.** The quote is CHF per EUR, so currency a is the franc, and Valtoria, which receives francs, is the party whose value is $V_{CS}$.
> CHF PV factors at initiation are 0.995768, 0.990884, 0.985513, 0.979624 (sum 3.951789), so $r_{CHF} = (1 - 0.979624)/3.951789 \times 2 = 1.0312\%$, a periodic coupon of 0.5156%.
> Exhibit 2 CHF factors are 0.998835, 0.994959, 0.990638, 0.985869 (sum 3.970301), so the CHF bond is worth $0.005156 \times 3.970301 + 0.985869 = 1.006341$ per 1, or CHF 150,951,126.
> Exhibit 2 EUR factors are 0.995223, 0.980649, 0.965857, 0.951022 (sum 3.892751), so the EUR bond is worth $0.013946 \times 3.892751 + 0.951022 = 1.005309$ per 1, or EUR 160,763,665.
> $V_{CS} = 150{,}951{,}126 - 0.9610 \times 160{,}763{,}665 = 150{,}951{,}126 - 154{,}493{,}882 = -\text{CHF }3{,}542{,}756$.
> B is wrong because it translates the euro bond at the initial spot rate of 0.9380, giving $+154{,}808$.
> C is wrong because it negates the value on the belief that Valtoria pays currency a; that figure is the dealer's value.
> The one-year forward rate is a decoy; the formula uses the current spot rate.
> 3. **B.** Today is a reset date, so the floating leg is worth par and the swap is valued from the new fixed rate on a swap with the same four remaining dates.
> That rate comes from the Exhibit 1 CHF curve and equals the currency swap's CHF rate: $FS_t = 0.5 \times 1.0312\% = 0.5156\%$ against $FS_0 = 0.5 \times 1.60\% = 0.80\%$.
> Receive-fixed value $= 80{,}000{,}000 \times (0.0080 - 0.005156) \times 3.951789 = 899{,}051$.
> Valtoria pays fixed and rates have fallen, so its value is $-899{,}051$.
> A is wrong because it uses the annual rate difference instead of the periodic difference, doubling the loss to $-1{,}798{,}101$.
> C is wrong because it reports the receive-fixed counterparty's value.
> 4. **B.** Statement 1 is incorrect: relabeling currency a changes only which party the formula values directly; Valtoria's economic value is unchanged and would be obtained by negating the new $V_{CS}$ and converting it at the current spot rate.
> Statement 2 is correct: higher euro rates lower the value of the euro bond Valtoria is short, lower franc rates raise the value of the franc bond it is long, and only the rise in the euro from CHF 0.9380 to CHF 0.9610 hurts a party that owes euros.
> Translating at the initial spot rate gives $+154{,}808$, so the currency move alone swings the value by about CHF 3.7 million.
> A and C accept Statement 1, which confuses the formula's reference party with the economics of the position.
>
> **Distractor design**
>
> 1. A: notional solved in the wrong direction ($NA_b = S_0 NA_a$ instead of $NA_a/S_0$); C: annual rate not scaled by the accrual period.
> 2. B: translation at $S_0$ instead of $S_t$; C: currency a misidentified, value reported for the wrong party (sign).
> 3. A: annual instead of periodic rate difference; C: value reported for the wrong party (sign).
> 4. A and C: currency a labeling mistaken for a change in the position's economics.

> [!success]- Item set 18 (05-02)
> 1. **B.** CAPM: $r = 2.5\% + 0.90 \times 5.0\% = 7.0\%$.
> PV of the planned dividends: $2.52/1.07 + 2.70/1.07^2 + 2.85/1.07^3 = 2.3551 + 2.3583 + 2.3264 = 7.0399$.
> The terminal value must supply the rest of the price: $62.40 - 7.0399 = 55.3601$ today, or $55.3601 \times 1.07^3 = 55.3601 \times 1.225043 = 67.8185$ at $t = 3$.
> Solve $V_3 = D_3(1 + g)/(r - g)$ for $g$ with $D_3$ in the role of $D_0$: $g = (V_3 r - D_3)/(V_3 + D_3) = (67.8185 \times 0.07 - 2.85)/(67.8185 + 2.85) = 1.8973/70.6685 = 0.02685$, or 2.68%.
> Check: $7.0399 + 2.85 \times 1.02685/[(0.07 - 0.02685) \times 1.225043] = 62.40$.
> A is wrong because it compounds the residual forward four periods, $55.3601 \times 1.310796 = 72.5658$, which gives $g = 2.96\%$; the terminal value sits at $t = 3$.
> C is wrong because it treats $D_3$ as the next dividend, $g = r - D_3/V_3 = 0.07 - 2.85/67.8185 = 0.07 - 0.042024 = 2.80\%$; the Gordon numerator at $t = 3$ is $D_4 = D_3(1 + g)$.
> 2. **C.** With mature ROE set to the industry median of 7.5%, $g = b \times ROE$ gives retention $= 0.026848/0.075 = 0.3580$ and payout $= 1 - 0.3580 = 64.20\%$.
> The price is consistent with Vellmar paying out 64.2% of earnings in maturity, while management targets 55%.
> At the target, sustainable growth is $0.45 \times 7.5\% = 3.375\%$, above the 2.68% the market prices; because mature ROE (7.5%) exceeds $r$ (7.0%), the extra retention creates value.
> Albescu's value at 3.375% terminal growth is $7.0399 + 2.85 \times 1.03375/[(0.07 - 0.03375) \times 1.225043] = 73.38$, above the 62.40 price, so the shares are undervalued.
> A is wrong because 35.8% is the retention ratio, not the payout ratio.
> B is wrong because it reverses the direction: implied growth below sustainable growth means the market is paying for less growth than Vellmar should deliver, so the shares are undervalued, not overvalued.
> Using Vellmar's leverage-inflated 12.0% ROE instead of the median would give a payout of $1 - 0.026848/0.12 = 77.6\%$, contrary to Corvina's policy.
> 3. **A.** No-growth value $= E_1/r = 4.20/0.07 = 60.00$; PVGO $= P_0 - E_1/r = 62.40 - 60.00 = 2.40$.
> Leading P/E decomposition: $P_0/E_1 = 62.40/4.20 = 14.8571 = 1/r + \text{PVGO}/E_1 = 14.2857 + 0.5714$, so the growth component is 0.57.
> Only $2.40/62.40 = 3.8\%$ of the price reflects growth opportunities, consistent with new investment earning a mature ROE only slightly above the required return.
> B is wrong because it computes the no-growth value with trailing EPS, $62.40 - 3.95/0.07 = 62.40 - 56.4286 = 5.9714$ and $5.9714/4.20 = 1.4218$; the perpetuity of constant earnings starts with $E_1$.
> C is wrong because 14.29 is the no-growth component $1/r$, not the growth component.
> 4. **B.** A trailing multiple is applied to earnings at the terminal date: $V_3 = 16.0 \times 4.60 = 73.60$, above the market-implied $V_3$ of 67.8185 from Question 1.
> The perpetual growth consistent with 73.60 is $(73.60 \times 0.07 - 2.85)/(73.60 + 2.85) = 2.3020/76.45 = 3.01\%$, above the 2.68% implied by the price, so Statement 2 is correct.
> Even the leading multiple misapplied to $E_3$ ($15.0 \times 4.60 = 69.00$, implied $g = 2.76\%$) would exceed 2.68%, so the conclusion does not hinge on that choice.
> A is wrong because $V_3$ is the value at $t = 3$ of all dividends from year 4 onward; it is built from $D_4$ precisely because it sits at $t = 3$, so it is discounted three periods, not four.
> C is wrong because a multiple-based terminal value embeds growth and required return assumptions implicitly, since any P/E is itself a function of $r$, $g$ and payout, and it also imports any mispricing in the peer group.
>
> **Distractor design**
>
> 1. A: terminal value located at $t = 4$ instead of $t = 3$ when backing it out of price (period error); C: $D_3$ treated as the next dividend in the implied-growth identity ($D_0$ versus $D_1$).
> 2. A: retention ratio reported as the payout ratio; B: direction of the implied versus sustainable growth comparison reversed.
> 3. B: trailing EPS used in the no-growth value $E/r$; C: no-growth P/E component $1/r$ reported instead of $\text{PVGO}/E_1$.
> 4. A: terminal value discounted $n + 1$ periods because it is built from $D_{n+1}$; C: multiple-based terminal value wrongly treated as assumption-free.

> [!success]- Item set 19 (06-01)
> 1. **C.** Buy the six-year zero at $100/(1.0365)^6 = 100/1.239983 = 80.6462$.
> With the curve unchanged, in two years it is a four-year zero priced at the four-year spot rate: $100/(1.032)^4 = 100/1.134276 = 88.1620$.
> Annualized return $= (88.1620/80.6462)^{1/2} - 1 = (1.093194)^{1/2} - 1 = 4.5559\%$, about 4.56%.
> The result equals the forward rate that rolls out of the pricing, $f_{4,2} = [(1.0365)^6/(1.032)^4]^{1/2} - 1 = 4.56\%$, and it beats the 2.40% maturity-matched return because a static upward-sloping curve lets the bond roll down to a lower yield.
> A is wrong because it is the return on the maturity-matched two-year zero, which is also the return every bond earns over two years if spot rates evolve as the forward curve implies, not if the curve stays static.
> B is wrong because it assumes the bond is sold at its original 3.65% yield, which equates the horizon return with the six-year yield and ignores the rolldown gain.
> 2. **B.** The six-year zero underperforms the two-year zero when its two-year growth factor falls below $(1.024)^2 = 1.048576$.
> Breakeven: $\frac{100/(1+z_4^*)^4}{100/(1.0365)^6} = (1.024)^2$, so $(1+z_4^*)^4 = (1.0365)^6/(1.024)^2 = 1.239983/1.048576 = 1.182540$.
> $z_4^* = 1.182540^{1/4} - 1 = 4.2807\%$, about 4.28%, which is the implied forward rate $f_{2,4}$ for a four-year loan beginning in two years.
> Check: at 4.28% the sale price is $100/1.182540 = 84.5637$ and $(84.5637/80.6462)^{1/2} - 1 = 2.40\%$.
> The trade therefore beats maturity matching as long as the four-year spot rate in two years stays below today's forward rate, a rise of up to about 108 bps from today's 3.20%: rolling down the curve is a bet that future spot rates will be lower than the forward curve implies.
> A is wrong because it uses the wrong end date, $f_{2,2} = [(1.032)^4/(1.024)^2]^{1/2} - 1 = (1.081730)^{1/2} - 1 = 4.01\%$, the forward for a loan ending in year 4 rather than year 6.
> C is wrong because it swaps the subscripts and computes $f_{4,2} = 4.56\%$, the rate for a two-year loan beginning in four years, which is the Question 1 static-curve return rather than a breakeven.
> 3. **C.** After the switch the holdings are $220 - 100 = 120$, $100 + 100 = 200$ and $80$, with weights 0.30, 0.50 and 0.20.
> Key rate durations: $KeyDur_2 = 0.30 \times 2 = 0.60$, $KeyDur_6 = 0.50 \times 6 = 3.00$, $KeyDur_{10} = 0.20 \times 10 = 2.00$; they sum to an effective duration of 5.60.
> $\%\Delta P = -[0.60(0.0010) + 3.00(0.0030) + 2.00(0.0045)] = -[0.0006 + 0.0090 + 0.0090] = -0.0186$, or $-1.86\%$.
> Value change $= -0.0186 \times 400 = -\text{CAD } 7.44$ million.
> A is wrong because it uses the pre-switch holdings (weights 0.55, 0.25, 0.20; KRDs 1.10, 1.50, 2.00): $-[0.0011 + 0.0045 + 0.0090] = -1.46\%$, or $-5.84$ million, which misses the extra 6-year exposure the switch created.
> B is wrong because it applies the 5.60 effective duration to the average shift of $(10 + 30 + 45)/3 = 28.33$ bps: $-5.60 \times 0.002833 \times 400 = -6.35$ million, which ignores shaping risk in a non-parallel scenario.
> 4. **A.** Statement 1 is correct: monetary policy explains about two-thirds of the variation in short- and intermediate-term government yields, and inflation explains about two-thirds of the variation in long-term yields.
> Statement 2 is incorrect: shortening the maturity structure of government debt reduces, not adds, the duration supplied to investors, which tends to lower the bond risk premium and long-term yields; a lengthening maturity structure (like larger deficits) raises them.
> B is wrong because it accepts a statement with the supply effect reversed and rejects a correct statement on the drivers of yields.
> C is wrong because Statement 2 misstates the direction in which the maturity structure of government debt moves the bond risk premium.
>
> **Distractor design**
>
> 1. A: maturity-matched or forward-consistent return used instead of the static-curve return (wrong scenario); B: sale at the original yield, horizon return equated with YTM (rolldown gain ignored).
> 2. A: forward with the wrong end date, $f_{2,2}$ from $z_4$ and $z_2$ (period); C: subscripts swapped, $f_{4,2}$ instead of $f_{2,4}$ (spot vs forward notation).
> 3. A: pre-switch holdings used to weight the key rate durations (misread exhibit); B: effective duration times the average shift (shaping risk ignored).
> 4. B: supply effect of the debt maturity structure reversed (sign); C: accepts the reversed supply effect alongside the correct statement.

> [!success]- Item set 20 (05-04)
> 1. **A.** The Yardeni model sets the earnings yield equal to the A-rated corporate bond yield less the growth weight times consensus long-term growth: $0.0550 - 0.10 \times 0.0950 = 0.0455$.
> Justified P/E $= 1/0.0455 = 21.9780$, or 22.0.
> The index's forward P/E is $5{,}600/280 = 20.0000$ (earnings yield 5.00%, above the justified 4.55%), so the market is undervalued by this model.
> B is wrong because it is the Fed model, $1/0.0430 = 23.2558$, which uses the Treasury yield and ignores growth.
> C is wrong because it reverses the direction: a justified P/E above the actual P/E indicates undervaluation.
> The trailing index P/E of $5{,}600/256 = 21.8750$ is also below 22.0, so the decoy trailing figure does not change the verdict.
> 2. **C.** Justified P/E $= 1/[\rho + (1-\lambda)I] = 1/(0.045 + 0.30 \times 0.060) = 1/0.0630 = 15.8730$, or 15.9.
> A is wrong because it uses the nominal required return in place of the real rate ($1/(0.105 + 0.018) = 1/0.1230 = 8.1301$), counting inflation twice.
> B is wrong because it multiplies inflation by the pass-through rate instead of by the fraction not passed through ($1/(0.045 + 0.70 \times 0.060) = 1/0.0870 = 11.4943$).
> For comparison, Orchid's justified P/E is $1/(0.045 + 0.30 \times 0.020) = 1/0.0510 = 19.6078$: with equal pass-through, the higher-inflation company earns the lower multiple.
> 3. **A.** The aggregate portfolio multiple is the weighted harmonic mean of the holdings' multiples, using market value weights.
> $\sum w_i/X_i = 0.30/14 + 0.25/18 + 0.20/25 + 0.15/9 + 0.10/40 = 0.0214 + 0.0139 + 0.0080 + 0.0167 + 0.0025 = 0.0625$ (unrounded 0.062484).
> Weighted harmonic mean $= 1/0.062484 = 16.0041$, or 16.0.
> B is wrong because it is the unweighted harmonic mean ($5/0.303095 = 16.4965$), which ignores the portfolio weights.
> C is wrong because it is the weighted arithmetic mean ($0.30 \times 14 + 0.25 \times 18 + 0.20 \times 25 + 0.15 \times 9 + 0.10 \times 40 = 19.05$), which is pulled up by the 40.0 multiple and does not equal total value over total earnings.
> 4. **A.** On 30 June, 3 months of fiscal 2026 remain, so NTM EPS $= (3/12) \times 4.00 + (9/12) \times 4.80 = 1.0000 + 3.6000 = 4.6000$.
> Forward P/E $= 85.10/4.6000 = 18.5000$.
> The historical benchmark is $0.95 \times 20.0 = 19.00$, so Brightwater trades about 2.6% below its customary relative multiple and appears undervalued; the justified price is $19.00 \times 4.60 = 87.40$.
> The conclusion relies on the historical relative relationship being stable, which Teo has checked, and on the index itself being fairly priced.
> B is wrong because it uses fiscal 2026 EPS alone ($85.10/4.00 = 21.2750$), a year that is three-quarters complete and mostly in the past.
> C is wrong because it reverses the weights ($(9/12) \times 4.00 + (3/12) \times 4.80 = 4.2000$, $85.10/4.2000 = 20.2619$).
>
> **Distractor design**
>
> 1. B: Fed model (Treasury yield, no growth) substituted for Yardeni; C: direction of misvaluation reversed.
> 2. A: nominal required return used where the real return belongs; B: pass-through rate used in place of one minus the pass-through rate.
> 3. B: unweighted harmonic mean that ignores portfolio weights; C: weighted arithmetic mean, which does not reproduce the aggregate multiple.
> 4. B: current fiscal-year EPS used instead of NTM EPS (period mismatch with the index's forward multiple); C: NTM month weights reversed.

> [!success]- Item set 21 (03-05)
> 1. **A.** Average total assets $= (9{,}600.0 + 10{,}400.0)/2 = 10{,}000.0$.
> Brenmoor: $(411.0 - 1{,}150.0)/10{,}000.0 = -739.0/10{,}000.0 = -7.39\%$.
> Ostley: $(260.0 - 520.0)/[(5{,}900.0 + 6{,}100.0)/2] = -260.0/6{,}000.0 = -4.33\%$.
> A smaller (more negative) accruals ratio means a larger cash component, which is more persistent, so on this measure alone Brenmoor's earnings look higher in quality than Ostley's.
> B is wrong because it reverses the reading: lower accruals, not higher, are the favorable signal.
> C is wrong because it uses operating income instead of net income ($(780.0 - 1{,}150.0)/10{,}000.0 = -3.70\%$), which is then above Ostley's $-4.33\%$ and reads as lower quality.
> 2. **A.** Capitalization moved the 240.0 cash payment from operating to investing activities, so corrected operating cash flow $= 1{,}150.0 - 240.0 = 910.0$ and corrected capital expenditures $= 1{,}020.0 - 240.0 = 780.0$.
> Free cash flow $= 910.0 - 780.0 = 130.0$, unchanged from the reported $1{,}150.0 - 1{,}020.0 = 130.0$: a classification shift moves cash between sections but does not change total cash flow.
> The correction also cuts net income by $(240.0 - 12.0) \times (1 - 0.25) = 171.0$ to 240.0, but net income does not enter either measure.
> B is wrong because it reduces operating cash flow but leaves the 240.0 in capital expenditures ($910.0 - 1{,}020.0 = -110.0$), counting the same payment twice.
> C is wrong because it deducts the after-tax amount from operating cash flow ($1{,}150.0 - 240.0 \times 0.75 = 970.0$; $970.0 - 780.0 = 190.0$), although taxes paid are unaffected, so the full pre-tax cash payment moves.
> 3. **B.** Gross PP&E rose from 38.0% and 39.0% of total assets to 44.0% and 49.0% with no change in strategy and only modest subscriber growth, the balance sheet build-up that must offset an under-reported expense.
> Capitalized operating costs are reported as investing outflows, so operating cash flow above net income and negative accruals give a false sense of security; the investing section and the common-size balance sheet should be checked before OCF is trusted.
> A is wrong because OCF above net income is not proof of quality when the cash outflows have been classified as investing.
> C is wrong because premature revenue recognition raises receivables and accruals; strongly negative accruals point the other way, and the problem here is expense capitalization, not revenue.
> 4. **B.** The rate rise reduces pre-tax income by 26.0; with symmetric sensitivities, a 10% depreciation of the pound reduces it by 18.0.
> Combined effect $= -26.0 - 18.0 = -44.0$; as a percentage of pre-tax income $= -44.0/548.0 = -8.03\%$.
> The zloty sensitivity is not part of the scenario.
> A is wrong because it applies the pound sensitivity with the wrong sign, as if the pound appreciated ($(-26.0 + 18.0)/548.0 = -1.46\%$).
> C is wrong because it divides a pre-tax effect by net income ($-44.0/411.0 = -10.71\%$).
>
> **Distractor design**
>
> 1. B: lower accruals read as lower quality (direction error); C: operating income used instead of net income (misread exhibit, decoy number).
> 2. B: payment removed from OCF but left in capex (double count); C: after-tax amount moved although taxes paid are unaffected (before-tax vs after-tax error).
> 3. A: OCF above net income treated as proof of quality (false sense of security); C: negative accruals linked to premature revenue (sign error).
> 4. A: currency move applied with the wrong sign (sign error); C: pre-tax sensitivity scaled by net income (before-tax vs after-tax error).

> [!success]- Item set 22 (10-02)
> 1. **C.** Opinions about the examination's difficulty or pass rate are permitted, but naming topics tested or not tested reveals confidential program information and violates Standard VII(A).
> Quint remains a candidate until results are released; claiming to have completed the Program and to be eligible for the charter misrepresents his candidacy and violates Standard VII(B).
> A is wrong because it punishes the permitted opinion and misses the profile.
> B is wrong because it treats the forum post as pure opinion and misses the disclosure of topic coverage.
> 2. **C.** Altering an invoice to take money from the club is dishonesty and fraud that reflects adversely on Fenn's integrity, violating Standard I(D) even though it occurred outside his job.
> A is wrong because civil disobedience in support of personal beliefs, although illegal, generally does not reflect on professional reputation, integrity, or competence.
> B is wrong because personal bankruptcy does not violate I(D) unless it involved fraudulent or deceitful conduct, and Castell's filing was accurate.
> 3. **B.** Standard III(E) covers information about current, former, and prospective clients; Sallow's plans were learned in a confidential prospective-client meeting, and none of the three exceptions (illegal activity, disclosure required by law, client permission) applies.
> Good intentions toward Sallow do not excuse the disclosure.
> Providing information to the Professional Conduct Program is not a violation, because the program is treated as an extension of the member when disclosure is permitted by law.
> A is wrong because the duty extends to prospective clients.
> C is wrong because the Professional Conduct Program disclosure is permitted.
> 4. **A.** Paid board service is compensation that could compete with the employer's interest, so Standard IV(B) requires written consent from the employer before acceptance.
> The directorship creates conflicts between duties to clients and to Ferrow's shareholders, equity-based compensation, and access to material nonpublic information, so Standard VI(A) requires prominent, plain-language disclosure, and the recommended practice is to isolate the director from investment decisions on the company with a firewall.
> B is wrong because disclosure must be made before the conflict affects clients, not after the fact in a routine letter, and it omits employer consent.
> C is wrong because the cash retainer alone requires consent, and the directorship itself is a conflict to disclose whether or not options are received.
>
> **Distractor design**
>
> 1. A: permitted exam-difficulty opinion treated as the violation, candidacy misstatement missed; B: disclosure of tested topics mistaken for opinion.
> 2. A: illegal but nonprofessional civil disobedience treated as misconduct; B: honest bankruptcy treated as misconduct.
> 3. A: confidentiality duty wrongly limited to current clients; C: Professional Conduct Program disclosure wrongly treated as a breach.
> 4. B: late, after-the-fact disclosure with no employer consent; C: declining one form of compensation treated as removing the conflict.
