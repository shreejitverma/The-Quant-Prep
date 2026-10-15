---
type: cfa-lm
topic: "Corporate Issuers"
topic_code: "04"
topic_slug: "04-Corporate-Issuers"
volume: 4
lm: 2
title: "Environmental, Social, and Governance (ESG) Considerations in Investment Analysis"
pages: "67-98"
weight_band: "5-10%"
difficulty: 2
los_count: 4
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/corporate-issuers]
---

# LM2: Environmental, Social, and Governance (ESG) Considerations in Investment Analysis

Difficulty 2 of 5: almost no computation, but the item sets punish imprecise vocabulary, so the work is memorizing the ownership-structure conflict matrix, the three ESG identification approaches with their specific weaknesses, and the exact direction of every valuation adjustment for equities versus bonds.

## LOS map

- **describe** global variations in ownership structures and the possible effects of these variations on corporate governance policies and practices (V4 p.67) ^los-04-02-a
    - Examiner asks: given an ownership percentage and a voting-rights description, name the structure (dispersed vs concentrated ownership crossed with dispersed vs concentrated voting power) and the resulting conflict (principal-agent vs principal-principal), or identify which influential shareholder type creates which specific governance risk.
- **evaluate** the effectiveness of a company's corporate governance policies and practices (V4 p.67) ^los-04-02-b
    - Examiner asks: given a vignette describing a board (size, independence count, CEO duality, tenure, diversity, committees, say-on-pay, dual-class shares), pick the single feature that most increases or decreases governance risk and reject the features that only look bad.
- **describe** how ESG-related risk exposures and investment opportunities may be identified and evaluated (V4 p.67) ^los-04-02-c
    - Examiner asks: match an identification approach (proprietary research, ESG data vendors, not-for-profit reporting frameworks such as SASB or GRI) to its characteristic weakness (inconsistent voluntary disclosure, subjective scores, standard-setting rather than company data), or test materiality and investment-horizon interactions.
- **evaluate** ESG risk exposures and investment opportunities related to a company (V4 p.67) ^los-04-02-d
    - Examiner asks: given a company profile, state the direction of the adjustment: which forecast line items move, whether the equity discount rate rises or falls, whether the DCF value rises or falls, and whether the credit spread widens or tightens, and distinguish the equity focus (opportunities plus downside) from the fixed-income focus (downside only).

## Core intuition

This module answers two questions.
First, who actually controls a company, and what conflict does that control structure bake in?
Second, once environmental, social, and governance risks are identified, where exactly do they enter a valuation model?

### Ownership determines the conflict, not the quality of the people

Corporate ownership structures are classified as dispersed, concentrated, or a hybrid of the two (V4 p.68).
Dispersed ownership means many shareholders, none able to exercise control individually.
Concentrated ownership means an individual shareholder or a group (controlling shareholders) can exercise control, and the group is typically a family, another company, or a sovereign entity (V4 p.68).
Globally, concentration is the norm: the OECD found 38 of 47 jurisdictions predominantly concentrated, with only Australia, Ireland, the United Kingdom, and the United States classified as dispersed and Canada, Germany, Japan, the Netherlands, and Switzerland classified as hybrid (V4 p.68, p.69).

The subtlety the exam tests is that ownership percentage and control can be disconnected (V4 p.69).
Controlling shareholders may be majority owners (more than 50%) or minority owners (less than 50%) who control through mechanisms.
Horizontal ownership is cross-holding share arrangements among companies with mutual business interests, which cements alliances but entrenches insiders.
Vertical (pyramid) ownership is a company or group holding controlling interests in holding companies that in turn control operating companies, so control cascades down with little capital at each layer (V4 p.69).
Dual-class shares give one class superior or sole voting rights and the other class inferior or no voting rights; combined with a pyramid, the top of the pyramid keeps control with relatively few total shares owned (V4 p.69, p.70).

> [!abstract] Idea 1: cross ownership concentration with voting-power concentration and the conflict names itself
> Dispersed ownership plus dispersed voting power produces weak shareholders facing strong managers: the principal-agent problem, where managers use company resources for themselves (V4 p.70).
> Concentrated ownership plus concentrated voting power produces strong shareholders and weak managers: the principal-principal problem, controlling shareholders diverting resources at the expense of minority shareholders (V4 p.70).
> Dispersed ownership plus concentrated voting power (dual-class, pyramids) is still principal-principal, except the controllers do not even own a majority of the cash flow rights (V4 p.70).
> Concentrated ownership plus dispersed voting power arises from voting caps, legal restrictions on the voting rights of large positions, often imposed to deter foreign control of strategic companies (V4 p.70).

The full matrix, which is the single most tested table in the module (V4 p.70):

| Ownership | Voting power | Shareholder vs manager strength | Conflict |
|---|---|---|---|
| Dispersed | Dispersed | Weak shareholders, strong managers | Principal-agent |
| Concentrated | Concentrated | Strong shareholders, weak managers | Principal-principal (controlling vs minority) |
| Dispersed | Concentrated | Strong controllers without majority economics | Principal-principal via dual-class or pyramids |
| Concentrated | Dispersed | Large owners with capped votes | Voting caps limit control |

The economic logic: monitoring is a public good.
A shareholder with 0.1% of a company bears all the cost of monitoring management but captures 0.1% of the benefit, so nobody monitors and managers run free.
A controlling shareholder internalizes enough of the benefit to monitor effectively, which solves the agent problem but creates a new one: the controller can tunnel value out through related-party transactions, so the victim changes from all shareholders to minority shareholders.

### Influential shareholder types each carry a signature risk

Identifying who sits on the register tells the analyst which governance risk to price (V4 p.71, p.72).

| Shareholder type | Benefit | Signature risk |
|---|---|---|
| Banks (Europe, Asia) | Informed, long-term capital | Lender-shareholder conflict: push the company into large loans on unfavorable terms (V4 p.71) |
| Families (Latin America, Asia, Europe) | Low principal-agent risk, concentrated ownership and management | Poor transparency, weak minority rights, difficulty attracting quality management, interlocking directorates (V4 p.71) |
| State-owned enterprises (mixed-ownership model) | Implicit or explicit state guarantee against bankruptcy | Lower market scrutiny of management; social or public policy goals over shareholder value (V4 p.71, p.72) |
| Institutional investors | Resources and expertise; hold boards accountable | Rarely a controlling stake in dispersed markets (V4 p.72) |
| Group companies (horizontal or vertical) | Strategic alliances, stable relationships | Related-party transactions at minority shareholders' expense; blocks outside acquirers (V4 p.72) |
| Private equity (VC, LBO) | Corporate codes, performance-based manager pay | Concentrated control during holding period (V4 p.72) |
| Foreign investors | Demand higher transparency; cross-listing benefits local minorities | Influence depends on stake size (V4 p.72) |
| Managers and directors (insiders) | Alignment as ownership rises | Entrenchment: large positions protect their own interests (V4 p.72) |

### Ownership structure shapes the governance machinery

Independent directors, defined by no material employment, ownership, or remuneration relationship with the company, originated in dispersed ownership jurisdictions to strengthen board monitoring of managers (V4 p.73).
Dispersed markets rely on them heavily: the United States requires audit, nomination, and compensation committees to be composed entirely of independent directors.
Concentrated markets need them less, because the controller already monitors management, so the principal-agent problem is smaller there; almost all OECD countries still impose or recommend a minimum number (one to three) or a minimum ratio (20% to 50% or greater) of independent directors (V4 p.73).
Boards come in one tier (a single board mixing executive and non-executive directors, the most common form) or two tiers (a supervisory board overseeing a management board, mandated in Argentina, Germany, and Russia, optional in Brazil and France); German supervisory boards seat key stakeholders such as banks and labor (V4 p.73).
Special voting arrangements protect minorities in Brazil, India, Portugal, Turkey, Italy, Israel, and the United Kingdom; a UK premium listing with a controlling shareholder requires independent directors to be approved separately by the whole shareholder base and by non-controlling shareholders (V4 p.73, p.74).
Governance codes usually run on comply-or-explain; Japan goes further by making companies without outside directors justify their absence, Chile uses company law, and India uses listing requirements (V4 p.74).
Stewardship codes push investors to engage; the UK Stewardship Code requires UK asset managers investing in UK shares to publish a comply-or-explain statement of commitment (V4 p.74).

### Evaluating a specific board

Effective governance is associated with higher profitability, better credit access, sustainable dividends, and a lower cost of capital; ineffective governance with reputational damage, share weakness, and a higher cost of capital (V4 p.74).
In practice analysts adjust the risk premium (cost of capital) or the credit spread to reflect governance quality (V4 p.75).
The checklist the exam draws vignettes from (V4 p.75, p.76):
CEO duality (CEO also chairs the board) compromises oversight; a lead independent director partially cures it.
Absence or minority of independent directors invites self-serving management and raises perceived risk.
Committees (audit, governance, remuneration, nomination, risk and compliance) should be sufficiently independent; non-independent members taint compensation, selection, and reporting integrity.
Skills should match core operations, with environmental or social expertise on boards in exposed sectors.
Tenure beyond 10 years is long: deep knowledge, but alignment with management and resistance to change.
Composition covers number and diversity of directors including professional, cultural, geographic, gender, age, and tenure dimensions; oversized or homogeneous boards govern less effectively.
Board evaluation can be self-evaluation or external review, covering duties, leadership, structure, and board-management interaction (V4 p.76).
Executive remuneration analysis covers transparency, incentive-plan performance criteria, linkage to strategy, and the CEO-to-average-worker pay ratio; say-on-pay lets shareholders vote or give feedback on pay, and clawback policies recover paid remuneration after restatements, misconduct, breach of law, or risk failures (V4 p.77).
Straight voting is one vote per share; dual-class structures give founders and management superior votes and are a standing minority-shareholder conflict (V4 p.77).

### Identifying ESG factors: three approaches, three weaknesses

> [!abstract] Idea 2: the identification approach determines the failure mode
> Proprietary research uses company disclosures (annual reports, sustainability reports, proxies, 10-K filings), and fails on inconsistent reporting and voluntary, variable disclosure, which kills comparability (V4 p.78, p.79).
> ESG data vendors (MSCI, Sustainalytics) convert disclosures into scores and rankings, and fail on the subjectivity of those assessments (V4 p.80).
> Not-for-profit initiatives and reporting frameworks (IIRC, GRI, SASB, 2DII) standardize disclosure, with SASB promoting uniform accounting standards and publishing materiality maps of sector-specific factors; they set standards rather than provide company-level answers (V4 p.80).

Materiality in an ESG context means issues expected to affect a company's operations, its financial performance, and the valuation of its securities (V4 p.78).
Companies may stretch the word to showcase positive but immaterial news and bury negative material news (V4 p.78, p.79).
The investment horizon interacts with materiality: some issues bite short term, others long term, and the horizon can shift suddenly with regulation or a controversy such as an oil spill; credit analysts care especially because bonds have different maturities (V4 p.79).
A short-horizon investor can rationally ignore a long-dated environmental risk that a long-horizon investor must model as plant upgrades and fines (V4 p.79).
Relevance is industry-specific: energy and steel are environmental stories, banks are social stories (data security, privacy, customer satisfaction), and every industry is a governance story; governance factors are reasonably consistent across companies while environmental and social best practice varies (V4 p.79).

### Integration: where the adjustment lands

> [!abstract] Idea 3: equities get upside and downside, bonds get downside only
> In equity analysis, ESG integration both identifies opportunities and mitigates downside risk: adjust forecast financials (revenues, operating and non-operating costs, margins, earnings, capex), adjust the discount rate or a price or terminal-value multiple, or run sensitivity and scenario analysis (V4 p.81, p.83).
> In fixed income, the bond redeems at par at maturity, so upside is capped and integration focuses on mitigating downside risk: internal credit assessments, forecast ratios, relative credit ranking, and adjustments to the credit spread or CDS (V4 p.81, p.82, p.83).
> Balance-sheet adjustments usually reflect estimated impaired assets, the stranded-assets channel (V4 p.83).

Stranded assets are assets that become obsolete or not economically viable, often from regulatory or policy change or demand shifts; a coal company's 10-year notes suffer far more than its 1-year notes because the risk is long-dated (V4 p.82).
The spread effect of the same ESG risk therefore differs by maturity (V4 p.82).
Green bonds designate proceeds for projects with environmental or climate benefits; the first was the European Investment Bank's Climate Awareness Bond in 2007 (V4 p.82).
Issuers label the bonds under the voluntary Green Bond Principles (2014, maintained by the International Capital Market Association), bear extra monitoring and reporting costs, and may gain a diversified investor base and a new-issue premium (V4 p.82).
Analytically a green bond is the issuer's conventional bond with earmarked proceeds: same ratings, same recourse, sometimes a demand-driven premium (tighter spread) (V4 p.82, p.83).
Greenwashing is the risk that proceeds are not actually used for the environmental project, so the investor overpaid for the green label or violates a mandate; liquidity risk matters too because buy-and-hold investors dominate (V4 p.83).
The ESG Integration Framework organizes all of this into research, security, and portfolio levels spanning qualitative and quantitative research, valuation for equities and fixed income, portfolio construction, asset allocation, scenario analysis, and risk management (V4 p.84).

## Formulas and derivations

The module is qualitative; these blocks formalize the metrics it uses and the one valuation mechanism every answer reduces to.

**Formula 1: Water intensity ratio** (V4 p.85)
$$ \text{Water intensity} = \frac{\text{total liters of water used}}{\text{liters of beverage produced}} $$
^f-04-02-1

Variables: numerator and denominator in liters, so the ratio is dimensionless liters per liter.
Lower is better; to compare companies of different sizes the module normalizes it per USD 1 million of revenue (V4 p.85).
It is the canonical example of a quantitative environmental metric feeding a cost forecast.

**Formula 2: Gross margin after an ESG cost adjustment** (V4 p.86)
$$ \text{GM} = 1 - \frac{\text{COGS}}{\text{Revenue}}, \qquad \text{GM}_{\text{ESG}} = 1 - \left(\frac{\text{COGS}}{\text{Revenue}} - \Delta\right) $$
^f-04-02-2

Variables: COGS/Revenue is cost of goods sold as a fraction of revenue; delta is the forecast reduction in that ratio from the ESG factor (positive delta = cost improvement).
Gross margin is sales minus cost of goods sold, as a percentage of sales (V4 p.86).
An environmental efficiency gain enters the model as a lower COGS ratio, which raises gross margin one for one.

**Formula 3: ESG-adjusted single-stage DCF value** (V4 p.83, p.97)
$$ V_0 = \frac{CF_1}{r - g} = \frac{CF_0(1+g)}{r - g} $$
^f-04-02-3

Variables: CF1 is next-period cash flow, r is the required return (cost of equity), g is long-run growth, all per period.
The module's qualitative rule quantified: negative ESG exposure raises r and lowers g, and both changes shrink the denominator's spread and the numerator, so value falls; positive exposure does the reverse (V4 p.83, p.97).
This is the anchor for every "after integrating ESG, value will..." question.

> [!tip] Calculator
> Single-stage value with CF0 = 100, g down from 3% to 2%, r up from 9% to 10%.
> Before: 100 [x] 1.03 [=] [/] 0.06 [=] gives 1,716.67.
> After: 100 [x] 1.02 [=] [/] 0.08 [=] gives 1,275.00.
> Change: 1275 [/] 1716.67 [-] 1 [=] gives -25.7%.

**Formula 4: Non-performing loan ratio as a governance proxy** (V4 p.91)
$$ \text{NPL ratio} = \frac{\text{non-performing loans}}{\text{total loans outstanding}} $$
^f-04-02-4

Variables: NPLs are loans not current on contractual interest or principal; both sides in currency, ratio usually quoted in percent or basis points.
The module uses credit risk as a proxy for a bank's governance quality: a weakly governed bank underwrites badly, so its NPL ratio runs above peers (Sumiyoshi runs 50 bps higher) (V4 p.91).

**Formula 5: Spread-widening price effect for ESG credit risk** (V4 p.82, p.83)
$$ \frac{\Delta P}{P} \approx -D_s \times \Delta s $$
^f-04-02-5

Variables: Ds is spread duration in years, delta s the change in credit spread in decimal, price change in percent of par.
This is the standard mechanism behind the module's statement that the spread effect of ESG risk differs by maturity: longer bonds have larger spread duration, so the same long-dated stranded-asset risk hits a 10-year note much harder than a 1-year note (V4 p.82).

## Worked examples

### Example 1: Conflicts between shareholders and managers (V4 p.70, p.71) 

Setup: Company A is a widely held conglomerate.
Managers collectively own about 30% of the shares; no other holder owns more than 1%; every share carries one vote.
Task: describe the potential conflict.

Step 1: classify ownership.
No single holder or bloc controls the company: the managers' 30% is collective, not a controlling group in the curriculum's reading, and the rest is atomized below 1%, so ownership is dispersed.
Step 2: classify voting power.
One share one vote with dispersed holdings means dispersed voting power.
Step 3: read the matrix.
Dispersed ownership plus dispersed voting power gives weak shareholders and strong managers.
Conclusion: the risk is that managers use company resources to pursue their own interests rather than maximize shareholder value, which is the principal-agent problem (V4 p.71).
The 30% insider stake is the tempting distractor toward principal-principal, but no controlling shareholder exists to oppress minorities; the curriculum solution names principal-agent.
^ex-04-02-1

### Example 2: Evaluating the board of directors (V4 p.76, p.77)

Setup: Style, a public Italian clothing retailer founded by the Donato family.
Board of 11: a chairperson who is not the CEO, 2 independent directors, and among the 6 non-independent directors 4 are Donato family members, each with at least 20 years of tenure.
5 of 11 directors are women, including chair Leila Donato; ages span 35 to 75.
Task: evaluate board effectiveness.

Positives.
Step 1: no CEO duality, since the chair is not the CEO, a sign of effective governance (V4 p.77).
Step 2: diversity in gender (5 of 11 women) and age (35 to 75) is a positive attribute.
Negatives.
Step 3: independence is substandard: 2 of 11 is 18.2% (2/11 = 0.1818, computed), below the typical 20% to 50% OECD minimum ratio range for independent directors (V4 p.73).
Step 4: four family members sit on the board including the chair, so the family monitors itself.
Step 5: family directors' tenure of at least 20 years far exceeds the 10-year threshold that governance codes deem long, threatening independence and adaptability (V4 p.76).
Conclusion: separated CEO and chair roles and diversity are positives; low independence and very long family tenure are the governance risks.
^ex-04-02-2

### Example 3: ESG integration, environmental factors, Frizzle Drinks (V4 p.85, p.86, p.87)

Setup: Frizzle is a fictitious US non-alcoholic beverage giant operating in developed and emerging markets including water-scarce countries.
Water is the key ingredient, so water intensity (Formula 1) is the key ESG metric.
From 2009 to 2021 Frizzle cut water intensity by 27%, and it targets another 13% cut by 2025F (V4 p.85).
Analyst Sam Smith normalizes water intensity per USD 1 million of revenue for peer comparison and finds Frizzle improving faster than peers (V4 p.85, p.86).
The curriculum prints no solution; the numbers below rework its stated assumptions, recomputed in Python.

Step 1: cumulative intensity reduction if the target is met.
Reductions compound multiplicatively: 1 - (1 - 0.27)(1 - 0.13) = 1 - 0.73 x 0.87 = 1 - 0.6351 = 0.3649, a 36.5% total cut from the 2009 level.
Step 2: cost adjustment.
For 2022, pre-adjustment COGS/revenue is forecast at 40% for Frizzle versus a 42% peer average; Smith assumes the water-intensity gain cuts Frizzle's ratio by 1 percentage point while peers stay flat (V4 p.86).
Adjusted Frizzle COGS/revenue = 40% - 1% = 39%.
Step 3: margin consequence via Formula 2.
Gross margin before = 100% - 40% = 60%; after = 100% - 39% = 61%; peers = 100% - 42% = 58%.
The ESG adjustment widens Frizzle's gross-margin lead over peers from 2 points to 3 points.
Step 4: valuation direction.
Lower COGS raises forecast earnings, so all else equal the fair value of Frizzle stock rises; operating cash flow also improves, so for the bonds and CDS Smith checks whether current spreads already price the lower ESG risk and adjusts accordingly (V4 p.87).
This is the rare direction on the exam: an ESG factor as an opportunity, not a risk.
^ex-04-02-3

### Example 4: ESG integration, social factors, Well Pharma (V4 p.87, p.88, p.89, p.90)

Setup: Well is a fictitious European pharmaceutical maker with the weakest peer-group record on product recalls and regulatory warning letters, including four major drug quality and safety scandals that brought lost sales, lawsuits, and fines.
Product quality is the material social factor; its components are quality controversies, warning letters, recalls, fines, and the percentage of plants with quality certifications such as ISO 9001 (V4 p.88).
Each maps to a financial impact: brand damage cuts sales, compliance and recalls raise costs, fines force provisions, low certification foreshadows recalls (V4 p.88, p.89).
The curriculum states the adjustments without a worked solution; the arithmetic below applies them to an illustrative base, recomputed in Python.

Smith's stated adjustments (V4 p.89): revenues fall 2% next year; COGS/revenue rises 1.3 percentage points; non-operating expenses (restructuring and other non-recurring costs) add 4.5% of operating income.
Step 1: illustrative base of revenue 1,000, COGS ratio 13% (in line with peers per Exhibit 12), other operating costs 700.
Step 2: adjusted revenue = 1,000 x 0.98 = 980.0.
Step 3: adjusted COGS ratio = 13% + 1.3% = 14.3%, so COGS = 980 x 0.143 = 140.14, pushing the ratio well above the peer average that stays near 13% (V4 p.89).
Step 4: operating income = 980 - 140.14 - 700 = 139.86.
Step 5: added non-operating expense = 0.045 x 139.86 = 6.29.
Every adjustment is negative: lower revenue, thinner margin, extra charges below the operating line.
Step 6: valuation direction.
Earnings and cash flow fall, hurting both shareholders and bondholders, with a further hit if investors judge the brand impaired; the nature of the adjustments depends on whether the quality problems are recurring or one-off (V4 p.89, p.90).
^ex-04-02-4

### Example 5: ESG integration, governance factors, Sumiyoshi Banking Group (V4 p.90, p.91)

Setup: Sumiyoshi is a fictitious Japanese bank holding company (80% of revenue from Japan) in commercial banking, leasing, securities, and consumer finance.
Smith benchmarks its board against the domestic peer group (V4 p.90, p.91).
No curriculum solution is printed; the evaluation below reads Exhibit 14 line by line.

Step 1: where Sumiyoshi matches peers.
Two-tier board like peers; audit, nomination, remuneration, and risk committees in place; straight voting; no dual-class shares; no single large shareholder; neither discloses incentive-plan metrics; both have CEO duality.
Step 2: where Sumiyoshi lags.
No independent chairperson (peers yes) on top of CEO duality; board independence 36% versus 47%; gender diversity 7% female versus 17%; directors with tenure over 10 years 14% versus 0%; 4 board committees versus 5 with no governance committee; non-executive directors with industry executive experience 20% versus 67%; no say-on-pay provision (peers yes) (V4 p.91).
Step 3: quantify with the governance proxy, Formula 4.
Smith estimates Sumiyoshi's NPL/total loans ratio runs 50 bps above the peer average, so if peers ran 1.10% Sumiyoshi runs 1.60% (illustrative levels; the 50 bp gap is the curriculum's number) (V4 p.91).
Step 4: valuation direction.
For the stock, raise the risk premium in the discount rate; for the bonds, widen the credit spread relative to peers (V4 p.91).
Using Formula 3 with the calculator-tip numbers: raising r from 9% to 10% and cutting g from 3% to 2% moves value from 100(1.03)/0.06 = 1,716.67 to 100(1.02)/0.08 = 1,275.00, a 25.7% haircut, which is the mechanism behind "increase the risk premium" stated in one line.
^ex-04-02-5

## Item-set patterns

> [!warning] Trap 1: insider ownership percentage read as concentration
> The vignette shows managers collectively owning 25% to 35% with no other holder above 1% and equal voting rights, and asks for the conflict.
> Correct approach: no controlling shareholder exists, so this is dispersed ownership, dispersed voting power, weak shareholders, strong managers, principal-agent (V4 p.70, p.71).
> Distractors: principal-principal tempts because 30% looks controlling; voting caps tempt because a number is mentioned, but caps are legal restrictions, not holdings.

> [!warning] Trap 2: family majority with equal votes called principal-agent
> A family owns 55% with one vote per share.
> Correct approach: concentrated ownership plus concentrated voting power, strong shareholders, weak managers, so the conflict is controlling versus minority shareholders, principal-principal (V4 p.70, p.97).
> Distractors: principal-agent tempts because managers appear; but family control lowers principal-agent risk since the family monitors management (V4 p.71, p.98).

> [!warning] Trap 3: the board feature that only looks bad
> The vignette loads a board description with one genuine defect (say 1 independent director out of 15) and two features that sound bad but are fine or good (family control, separate CEO and chair).
> Correct approach: test each feature against the checklist; independence below the 20% to 50% OECD range is the defect (V4 p.73, p.97, p.98).
> Distractors: CEO duality when the roles are actually separate; family control, which reduces principal-agent risk even as it brings transparency drawbacks.

> [!warning] Trap 4: identification approach and weakness mismatched
> Yorkton-style vignette: the analyst uses proprietary methods on company filings, and the question asks the potential problem.
> Correct approach: proprietary use of company disclosures suffers from inconsistent reporting and voluntary, variable disclosure (V4 p.79, p.96).
> Distractors: subjective scores and rankings belong to the vendor approach (MSCI, Sustainalytics); uniform accounting standards belong to SASB and the framework approach (V4 p.80, p.96).

> [!warning] Trap 5: time horizon dismissed as irrelevant to materiality
> A statement claims the horizon has little effect on which ESG factors are material.
> Correct approach: horizon is central, especially in credit analysis because bonds have different maturities, and impacts migrate between short and long term with regulation or controversies (V4 p.79, p.96).
> Distractor: the statement sounds efficient-markets plausible; the curriculum flatly contradicts it.

> [!warning] Trap 6: ESG integration direction flipped for a negative exposure
> A steel or coal company faces long-run emissions regulation and falling end-market demand.
> Correct approach: revenues fall, operating costs rise, the discount rate rises, growth falls, DCF value falls; the balance-sheet channel is stranded assets (V4 p.82, p.97).
> Distractors: "reducing operating costs" and "increasing revenues" reverse the signs; "remain unchanged" tempts if you assume the market has priced it.

> [!warning] Trap 7: equity-analysis tools attributed to fixed income
> A bond analyst integrates ESG and the question asks the focus or the tool.
> Correct approach: fixed income focuses on mitigating downside risk and adjusts the credit spread or CDS; equity focuses on opportunities plus downside and adjusts the discount rate or multiples (V4 p.81, p.98).
> Distractors: adjusting the discount rate and identifying opportunities are the equity answers planted on bond questions.

> [!warning] Trap 8: green bond treated as a different credit
> A green bond question implies special recourse or rating.
> Correct approach: analysis and valuation are essentially the same as the issuer's conventional bonds, same ratings and recourse; the differences are earmarked proceeds, a possible demand-driven premium, greenwashing risk, and liquidity risk from buy-and-hold ownership (V4 p.82, p.83).
> Distractors: assuming the green label changes seniority or credit quality, or that a green premium is guaranteed.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM02-Environmental-Social-and-Governance-ESG-Considerations-in-Investment-Analysis-Practice-Problems]]

## Cross-links

- [[LM01-Analysis-of-Dividends-and-Share-Repurchases]]: governance quality drives payout discipline; agency conflicts between managers and shareholders motivate dividends as a bonding device, and the same ownership-structure vocabulary carries over.
- [[LM03-Cost-of-Capital-Advanced-Topics]]: this module says "raise the discount rate for ESG risk"; LM03 supplies the machinery (risk premium build-ups, country and company-specific premia) that the adjustment lands in.
- [[LM04-Corporate-Restructuring]]: stranded assets and ESG-driven impairments are triggers for the divestitures and restructurings LM04 evaluates, and board effectiveness determines whether restructuring serves shareholders.
- [[LM02-Guidance-for-Standards-I-VII]]: using material nonpublic ESG information, greenwashing claims in client communications, and diligence over third-party ESG scores all engage Standards II, I(C), and V(A).
- [[LM01-Equity-Valuation-Applications-and-Processes]]: ESG integration is a worked instance of the valuation process: forecast adjustments, discount-rate changes, and scenario analysis inside a DCF or multiples framework.

## Self-test

Vignette A (questions 1 to 5): Lena Ortiz analyzes Karuna Foods, a packaged-food company listed in a developing market.
The founding Karuna family owns 38% of shares through a holding company that also controls two other listed operating companies.
Karuna Foods has two share classes: class A (family, 10 votes per share) and class B (public, 1 vote per share); the family controls 74% of votes.
The 12-member board includes the CEO, who also chairs it, 3 independent directors, and 2 directors who have served 14 years.
The country's governance code recommends at least one third independent directors on a comply-or-explain basis.
Karuna sources palm oil from suppliers criticized for deforestation, and a new packaging-waste levy is under parliamentary debate.
Ortiz's fund holds Karuna's 8-year bonds; a colleague holds the equity.

1. Karuna's ownership structure is best described as:
A. concentrated ownership and dispersed voting power.
B. dispersed ownership and concentrated voting power.
C. concentrated ownership within a vertical arrangement with concentrated voting power.

2. The primary conflict embedded in Karuna's structure is between:
A. shareholders and managers.
B. controlling and minority shareholders.
C. creditors and shareholders.

3. The board feature most likely to increase governance risk is:
A. CEO duality.
B. the 14-year director tenures.
C. independent directors at 25% of the board.

4. Relative to the code's recommendation, Karuna's board independence is:
A. compliant, so no disclosure is required.
B. non-compliant, requiring an explanation under comply-or-explain.
C. non-compliant, requiring delisting.

5. For the 8-year bonds, the packaging levy and palm-oil exposure most likely lead Ortiz to:
A. widen her spread assumption.
B. lower her discount rate.
C. raise her terminal growth assumption.

Vignette B (questions 6 to 10): Marc Duval covers two issuers.
Nordwind Utility issues a bond labeled green to fund wind farms; the bond ranks pari passu with Nordwind's conventional notes and carries the same rating.
Duval learns that a third of proceeds quietly funded a gas-plant retrofit.
Helios Apparel, a fast-fashion retailer, faces a documentary alleging supplier sweatshops; Duval expects a consumer boycott lasting two quarters and new supply-chain audit costs equal to 0.8% of revenue annually.
Helios currently trades at 14x forward earnings versus peers at 15x.
Duval values Helios equity with a single-stage model: forecast cash flow 200, r 8%, g 2.5%.
After ESG integration he uses r 8.6% and g 2.1%.

6. The Nordwind finding is best described as:
A. greenwashing.
B. stranded assets.
C. a voting cap violation.

7. Compared with Nordwind's conventional notes, the green bond's credit analysis should:
A. use a separate recovery assumption.
B. be essentially the same, since ratings and recourse match.
C. assume a permanently tighter spread.

8. The supply-chain audit costs enter Duval's Helios model most directly through:
A. higher operating costs in forecast financials.
B. a lower tax rate.
C. a higher terminal multiple.

9. Helios's ESG-adjusted equity value per Duval's inputs (cash flow forecast of 200 is next-period CF1 in both cases) changes by approximately:
A. -15%.
B. -18%.
C. -21%.

10. If Duval's fund had held Helios bonds instead, his ESG focus would shift toward:
A. capturing the boycott's upside.
B. mitigating downside risk via spread adjustment.
C. raising the target multiple.

> [!success]- Answer key
> 1. C.
> The family holds 38% (minority) but sits atop a holding company controlling multiple listed companies, a vertical (pyramid) arrangement, and dual-class shares give it 74% of votes: concentrated control with concentrated voting power (V4 p.69, p.70).
> A is wrong because voting power is concentrated, not dispersed (no voting caps exist).
> B describes the generic dual-class case but misses that ownership here is also concentrated through the pyramid, so C is more complete.
> 2. B.
> Strong controlling shareholders and weak managers create the principal-principal conflict: the family can tunnel value from minorities via the group structure and related-party transactions (V4 p.70, p.72).
> A is the dispersed-ownership conflict; C is a real conflict in finance but not the one this ownership structure creates.
> 3. A.
> The CEO chairing the board compromises the board's monitoring role, the classic CEO duality concern, made worse here because the controller already dominates votes (V4 p.75).
> B matters (tenure over 10 years is long) but affects 2 directors; C, at 25%, sits within the typical 20% to 50% recommended range, so it is the least of the three problems (V4 p.73, p.76).
> 4. B.
> 3 of 12 is 25%, below the code's one-third recommendation; under comply-or-explain the company must disclose why it does not comply, not delist (V4 p.74).
> A is wrong on the arithmetic (25% < 33.3%); C overstates the sanction.
> 5. A.
> Bond analysis integrates ESG by adjusting the credit spread for downside risk; a new levy and deforestation exposure raise cost and reputational risk, widening the spread (V4 p.82, p.83).
> B and C are equity-model moves, and both go the wrong direction for a risk increase.
> 6. A.
> Proceeds not used for the beneficial environmental purpose is the definition of greenwashing (V4 p.83).
> B concerns assets stranded by regulation or demand shifts; C is an ownership-structure term, irrelevant here.
> 7. B.
> Green bonds normally carry the same credit ratings and bondholder recourse as the issuer's conventional bonds, so analysis and valuation are essentially the same; only proceeds use, a possible demand premium, greenwashing, and liquidity differ (V4 p.82, p.83).
> A invents a recovery difference that pari passu ranking contradicts; C turns a possible demand-driven premium into a certainty.
> 8. A.
> Recurring audit costs of 0.8% of revenue are an operating-cost adjustment to forecast financials, the standard first channel of ESG integration (V4 p.83).
> B has no basis; C would raise value, the wrong direction, and multiples are a separate channel.
> 9. A.
> Before: 200/(0.08 - 0.025) = 200/0.055 = 3,636.36.
> After: 200/(0.086 - 0.021) = 200/0.065 = 3,076.92.
> Change: 3,076.92/3,636.36 - 1 = -15.4% (with CF1 fixed, the value ratio is just old spread over new spread, 0.055/0.065 = 0.8462).
> B (-18%) comes from misreading the 1.0-point total denominator move as roughly 18% of the 5.5% spread applied twice; C (-21%) comes from also shrinking CF1 by g, double-counting the growth cut.
> 10. B.
> Fixed-income ESG integration focuses on mitigating downside risk, implemented through spread or CDS adjustments (V4 p.81, p.98).
> A and C describe the equity side (opportunity capture, multiple adjustments).

## Flashcards

#flashcards/cfa-l2/04-Corporate-Issuers/lm02

Dispersed ownership::Many shareholders, none of which can individually exercise control over the corporation (V4 p.68)
Concentrated ownership::An individual shareholder or group (controlling shareholders) able to exercise control, typically a family, another company, or a sovereign entity (V4 p.68)
How common is concentrated ownership globally?::OECD found 38 of 47 jurisdictions predominantly concentrated; only Australia, Ireland, the UK, and the US are dispersed; Canada, Germany, Japan, Netherlands, Switzerland are hybrid (V4 p.68, p.69)
Horizontal ownership::Cross-holding share arrangements among companies with mutual business interests, such as key customers or suppliers (V4 p.69)
Vertical (pyramid) ownership::A company or group with controlling interests in two or more holding companies that in turn control operating companies (V4 p.69)
Dual-class shares::One share class holds superior or sole voting rights while the other holds inferior or no voting rights, disconnecting ownership from control (V4 p.69)
Dispersed ownership + dispersed voting power creates which conflict?::Principal-agent, weak shareholders vs strong managers who may pursue their own interests (V4 p.70)
Concentrated ownership + concentrated voting power creates which conflict?::Principal-principal, strong controlling shareholders extracting value from minority shareholders (V4 p.70)
Dispersed ownership + concentrated voting power arises through which mechanisms?::Dual-class share structures and pyramid structures; conflict is still principal-principal (V4 p.70)
Voting caps::Legal restrictions on the voting rights of large share positions, producing concentrated ownership with dispersed voting power, often to deter foreign control (V4 p.70)
Signature risk when a bank is both lender and shareholder::It may push the company into large loans on unfavorable terms to the detriment of other shareholders (V4 p.71)
Benefit and drawbacks of family ownership
?
Benefit is lower principal-agent risk from combined ownership and management.
Drawbacks are poor transparency, lack of accountability, weak minority rights, and difficulty attracting quality management talent (V4 p.71).

Interlocking directorates::The same individuals serve on boards of multiple corporations, common in Latin America, letting one family control several companies (V4 p.71)
Mixed-ownership model::Listed state-owned enterprises partially owned by the sovereign with publicly traded shares; lower market scrutiny and implicit or explicit state guarantees (V4 p.71, p.72)
Governance risk of group companies::Related-party transactions at the expense of minority shareholders; cross-holdings also block outside purchases of significant stakes (V4 p.72)
Insiders in a governance context::Managers and board directors who are also shareholders; alignment improves as stakes rise, but large stakes enable entrenchment (V4 p.72)
Independent board director::A director with no material relationship with the company regarding employment, ownership, or remuneration (V4 p.73)
Where did independent directors originate and why?::In dispersed ownership jurisdictions, to strengthen the board's monitoring role over managers (V4 p.73)
Typical OECD minimum for independent directors::A minimum number (one to three) or a minimum ratio, typically 20% to 50% or greater (V4 p.73)
One-tier vs two-tier board
?
One tier is a single board mixing executive (internal) and non-executive (external) directors, the most common form.
Two tier is a supervisory board overseeing a management board, mandatory in Argentina, Germany, and Russia (V4 p.73).

Who sits on German supervisory boards besides shareholders?::Representatives of key stakeholders such as banks and labor groups (V4 p.73)
UK premium listing rule with a controlling shareholder::Independent directors must be separately approved by the entire shareholder base and by non-controlling shareholders (V4 p.73, p.74)
Comply-or-explain::Companies disclose adoption of recommended governance practices or explain why not; Japan additionally makes firms without outside directors justify the absence (V4 p.74)
Stewardship codes::Voluntary codes encouraging investors to exercise rights and engage; the UK version requires asset managers to publish a comply-or-explain commitment statement (V4 p.74)
CEO duality::The CEO also serves as board chairperson, raising concern that monitoring is compromised; a lead independent director is the partial remedy (V4 p.75)
When is board tenure considered long?::Beyond 10 years per many governance codes; positives are experience, negatives are lost independence and resistance to change (V4 p.76)
Say-on-pay::A provision letting shareholders vote on or give feedback about executive remuneration (V4 p.77)
Clawback policy::Allows the company to recover previously paid remuneration after restatements, misconduct, breach of law, or risk management deficiencies (V4 p.77)
Straight voting::One vote for each share owned (V4 p.77)
The three approaches to identifying ESG factors
?
Proprietary methods using company disclosures and own research.
ESG data vendors such as MSCI and Sustainalytics providing scores and rankings.
Not-for-profit initiatives and reporting frameworks such as IIRC, GRI, SASB, and 2DII (V4 p.79, p.80).

Weakness of proprietary company-data approach::Inconsistent reporting of ESG information and metrics among firms plus voluntary, variable disclosure, creating comparability problems (V4 p.79, p.96)
Weakness of the ESG data-vendor approach::Subjective assessments embedded in scores and rankings (V4 p.80, p.96)
What does SASB do?::Seeks to promote uniform accounting standards for sustainability reporting and publishes materiality maps of sector-specific material ESG factors (V4 p.80)
ESG materiality::ESG issues expected to affect a company's operations, financial performance, and the valuation of its securities (V4 p.78)
Why does investment horizon matter for ESG materiality?::Issues differ in when they bite, horizons can shift with regulation or controversies, and credit analysts face different bond maturities (V4 p.79)
Which industries map to which ESG factor emphasis?::Energy and steel are mainly environmental; banks are mainly social (data security, privacy, customer satisfaction); governance applies to all (V4 p.79)
Equity vs fixed-income ESG integration focus::Equity uses ESG to identify opportunities and mitigate downside; fixed income focuses on mitigating downside because bonds redeem at par (V4 p.81)
Equity valuation channels for ESG adjustments::Forecast financials (revenues, costs, margins, capex), the discount rate, price or terminal-value multiples, and sensitivity or scenario analysis (V4 p.81, p.83)
Fixed-income valuation channels for ESG adjustments::Internal credit assessments, forecast ratios, relative credit ranking, and adjusting the credit spread or CDS (V4 p.81, p.82, p.83)
Stranded assets::Assets that become obsolete or not economically viable, often from regulatory or policy changes or demand shifts (V4 p.82)
Why does ESG risk hit long bonds harder than short bonds?::The risk is long-dated and spread duration rises with maturity, so a 10-year note's valuation suffers far more than a 1-year note's (V4 p.82)
Green bond::A bond whose proceeds are designated to fund projects with environmental or climate benefits; first was the EIB Climate Awareness Bond in 2007 (V4 p.82)
Green Bond Principles::Voluntary 2014 standards guiding issuers on labeling bonds green, maintained by the International Capital Market Association (V4 p.82)
How do green bonds compare with the issuer's conventional bonds?::Normally same credit ratings and recourse, same analysis and valuation; possible demand-driven premium (tighter spread), extra monitoring costs for the issuer (V4 p.82, p.83)
Greenwashing::The risk that green bond proceeds are not actually used for the beneficial environmental project, causing overpayment or mandate violations (V4 p.83)
{{Liquidity}} risk matters for green bonds because they are often held by {{buy-and-hold}} investors (V4 p.83)
Water intensity ratio::Total liters of water used per liter of beverage produced; normalized per USD 1 million of revenue for peer comparison (V4 p.85)
Frizzle micro-drill: COGS/rev 40%, ESG adjustment cuts it 1 point, peers at 42%; gross margins?::Frizzle after 61% vs 60% before vs peers 58%; keystrokes 1 - 0.39 and 1 - 0.42 (V4 p.86)
Well Pharma's three stated ESG adjustments::Revenues down 2%, COGS/revenue up 1.3 points, non-operating expenses up 4.5% of operating income (V4 p.89)
Material social factor for pharmaceutical companies::Product quality, decomposed into controversies, warning letters, recalls, fines, and certification percentage (V4 p.88)
Sumiyoshi governance red flags vs peers::No independent chair with CEO duality, 36% vs 47% independence, 7% vs 17% female, 14% long-tenure directors vs 0%, 20% vs 67% industry-experienced non-executives, no say-on-pay (V4 p.91)
NPL ratio as governance proxy::Non-performing loans over total loans; Sumiyoshi runs about 50 bps above peers, signaling weaker credit and governance quality (V4 p.91)
Gordon micro-drill: CF0 100, r 9% to 10%, g 3% to 2%; value change?::From 100(1.03)/0.06 = 1,716.67 to 100(1.02)/0.08 = 1,275.00, a 25.7% decline; keystrokes 103 / 0.06 then 102 / 0.08 (V4 p.97)
Which conflict does a 55% family stake with equal votes create?::Principal-principal, controlling vs minority shareholders; strong shareholders and weak managers (V4 p.97)
Does family control raise or lower principal-agent risk?::Lowers it, because ownership and management responsibility are concentrated in the same hands (V4 p.71, p.98)
After bad ESG news, the trio of adjustments for equity DCF::Cut revenue or growth forecasts, raise operating cost forecasts, raise the discount rate; value falls (V4 p.97)
ESG effect on a risky issuer's credit spread::The spread widens to compensate for higher ESG risk, lowering bond value by roughly spread duration times the widening (V4 p.82, p.98)

## Common mistakes

1. Calling a 30% collective insider stake "concentrated ownership" and answering principal-principal when no controlling shareholder exists; with dispersed holdings and equal votes the conflict is principal-agent (V4 p.70, p.71).
2. Treating family control as a governance risk amplifier; it lowers principal-agent risk, and its costs are transparency, minority rights, and talent, not agent conflict (V4 p.71, p.98).
3. Assigning the vendor approach's weakness (subjective scores) to proprietary company-data research, whose weakness is inconsistent, voluntary disclosure (V4 p.79, p.80, p.96).
4. Claiming time horizon barely affects materiality; it is central, migrates with regulation and controversies, and matters most in credit work because maturities differ (V4 p.79, p.96).
5. Flipping the sign of ESG adjustments: for a negative exposure, revenues and growth fall, operating costs rise, the discount rate rises, and DCF value falls, all four together (V4 p.97).
6. Using equity tools on bond questions: fixed income adjusts the credit spread or CDS and focuses on downside; the discount rate and opportunity identification belong to equity (V4 p.81, p.98).
7. Believing CEO duality exists whenever the company has both a CEO and a chairperson; duality means the same person holds both roles (V4 p.75).
8. Assuming a green bond is a different credit; ratings, recourse, and valuation match the issuer's conventional bonds, with only proceeds use, possible premium, greenwashing, and liquidity differing (V4 p.82, p.83).
9. Forgetting that a controlling shareholder can hold under 50%: pyramids and dual-class shares deliver control without majority ownership (V4 p.69, p.70).
10. Reading long board tenure as pure experience; beyond 10 years, codes treat tenure as a threat to independence and adaptability (V4 p.76).
11. Judging board independence by counting independent directors without computing the ratio against the 20% to 50% OECD range (1 of 15 is 6.7%, a fail) (V4 p.73, p.97).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "04-02" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
