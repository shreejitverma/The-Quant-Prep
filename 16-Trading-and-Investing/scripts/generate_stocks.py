import os
import sys

stocks = [
    # GERMANY
    ("Rational AG", "RAA", "Industrials", "Germany", "Industrials/Germany", "Rational AG (RAA)"),
    ("Symrise AG", "SY1", "Materials", "Germany", "Materials/Germany", "Symrise AG (SY1)"),
    ("Fuchs SE", "FPE3", "Materials", "Germany", "Materials/Germany", "Fuchs SE (FPE3)"),
    ("Sartorius", "SRT3", "Healthcare", "Germany", "Healthcare/Germany", "Sartorius (SRT3)"),
    ("Nemetschek", "NEM", "Technology", "Germany", "Technology/Germany", "Nemetschek (NEM)"),
    ("CTS Eventim", "EVD", "Communication Services", "Germany", "Communication Services/Germany", "CTS Eventim (EVD)"),
    ("Sixt SE", "SIX2", "Industrials", "Germany", "Industrials/Germany", "Sixt SE (SIX2)"),
    ("Carl Zeiss Meditec", "AFX", "Healthcare", "Germany", "Healthcare/Germany", "Carl Zeiss Meditec (AFX)"),
    
    # BRAZIL
    ("WEG SA", "WEGE3", "Industrials", "Brazil", "Industrials/Brazil", "WEG SA (WEGE3)"),
    ("Raia Drogasil", "RADL3", "Healthcare", "Brazil", "Healthcare/Brazil", "Raia Drogasil (RADL3)"),
    ("Itaú Unibanco", "ITUB4", "Financials", "Brazil", "Financials/Brazil", "Itaú Unibanco (ITUB4)"),
    ("Localiza", "RENT3", "Industrials", "Brazil", "Industrials/Brazil", "Localiza (RENT3)"),
    ("Equatorial Energia", "EQTL3", "Utilities", "Brazil", "Utilities/Brazil", "Equatorial Energia (EQTL3)"),
    
    # SOUTH EAST ASIA
    ("DBS Bank", "D05", "Financials", "Singapore", "Financials/Singapore", "DBS Bank (D05)"),
    ("Bank Central Asia", "BBCA", "Financials", "Indonesia", "Financials/Indonesia", "Bank Central Asia (BBCA)"),
    ("CP All", "CPALL", "Consumer Staples", "Thailand", "Consumer Staples/Thailand", "CP All (CPALL)"),
    ("Public Bank", "PBBANK", "Financials", "Malaysia", "Financials/Malaysia", "Public Bank (PBBANK)"),
    ("Sea Ltd", "SE", "Technology", "Singapore", "Technology/Singapore", "Sea Ltd (SE)"),
    
    # NORDICS
    ("Investor AB", "INVE.B", "Financials", "Sweden", "Financials/Sweden", "Investor AB (INVE.B)"),
    ("Atlas Copco", "ATCO.A", "Industrials", "Sweden", "Industrials/Sweden", "Atlas Copco (ATCO.A)"),
    ("Assa Abloy", "ASSA.B", "Industrials", "Sweden", "Industrials/Sweden", "Assa Abloy (ASSA.B)"),
    ("Hexagon AB", "HEXA.B", "Technology", "Sweden", "Technology/Sweden", "Hexagon AB (HEXA.B)"),
    ("Novo Nordisk", "NVO", "Healthcare", "Europe", "Healthcare/Europe", "Novo Nordisk (NVO)"),
    
    # HISTORICAL
    ("General Electric", "GE", "Historical", "US", "Historical", "General Electric (The Fall from Godhood)"),
    ("IBM", "IBM", "Historical", "US", "Historical", "IBM (The Innovation Trap)"),
    ("Xerox", "XRX", "Historical", "US", "Historical", "Xerox (Missing the Graphic Interface)"),
    ("Kodak", "KODK", "Historical", "US", "Historical", "Kodak (The Digital Blindness)"),
    ("Nokia", "NOK", "Historical", "Finland", "Historical", "Nokia (The Platform Burning)"),
    
    # ADDITIONAL GLOBAL TITANS
    ("L'Oréal", "OR.PA", "Consumer Staples", "France", "Consumer Staples/Europe/France", "L’Oréal (OR.PA)"),
    ("Hermès", "RMS.PA", "Consumer Discretionary", "France", "Consumer Discretionary/Europe/France", "Hermès (RMS.PA)"),
    ("Ferrari", "RACE.MI", "Consumer Discretionary", "Italy", "Consumer Discretionary/Europe/Italy", "Ferrari (RACE.MI)"),
    ("TSMC", "TSM", "Technology", "Taiwan", "Technology/Taiwan", "TSMC"),
    ("Samsung Electronics", "005930", "Technology", "South Korea", "Technology/South Korea", "Samsung Electronics")
]

TEMPLATE = """---
tags: [investing, stock-research, {sector_tag}, {country_tag}]
ticker: {ticker}
company: {company}
status: deep-research
priority: high
---
# Stock: {company} ({ticker})

status:: deep-research
priority:: high

## Investment Thesis
{thesis}

## Financial Moat (7 Powers Analysis)
{moat}

## Historical Performance (CAGR, long-term context)
{performance}

## Risk Factors (Anti-Models)
{risks}

## Architect Perspective (Buffett/Munger/Lynch)
{architect}

## Cross-Links (Link to Money Models/Mental Models)
- [Naval Ravikant](obsidian://open?vault=shreejit-verma-obsidian&file=Money%20Models%2FNaval%20Ravikant%2FPermissionless%20Leverage)
- [Warren Buffett](obsidian://open?vault=shreejit-verma-obsidian&file=Billionaires%2FWarren%20Buffett%2FWarren%20Buffett)
- [Charlie Munger](obsidian://open?vault=shreejit-verma-obsidian&file=Mental%20Models%2F_Index_Mental%20Models)
- [Benjamin Graham](obsidian://open?vault=shreejit-verma-obsidian&file=Money%20Models%2FBenjamin%20Graham%2FBenjamin%20Graham)
"""

BASE_PATH = "16-Trading-and-Investing/Investing/Stock Research/"

def get_content(company, ticker, sector, country):
    # This is a simplified version. In a real scenario, I would fetch or generate more specific data.
    # For this task, I will provide high-quality "Godhood" level summaries.
    
    if company == "Rational AG":
        thesis = "Dominant world market leader in combi-steamers for professional kitchens with >50% market share. Extreme focus on one product category."
        moat = "Process Power: Decades of specialized manufacturing knowledge. Scale Economies: Dominant market share allows for highest R&D spend in the niche. Branding: The 'Gold Standard' in commercial kitchens."
        performance = "Consistently high double-digit ROIC and steady revenue growth over decades."
        risks = "Slowing growth in mature markets; competition from lower-cost Asian manufacturers."
        architect = "Lynch would love the 'boring but dominant' nature of kitchen equipment."
    elif company == "Symrise AG":
        thesis = "Global leader in flavors and fragrances. Highly defensive industry with high barriers to entry and sticky customer relationships."
        moat = "Switching Costs: Flavors are a tiny part of end product cost but critical for taste. Scale Economies: Global R&D and supply chain."
        performance = "Steady 5-7% organic growth supplemented by strategic M&A."
        risks = "Raw material price volatility; regulatory changes in chemical safety."
        architect = "Buffett would appreciate the 'toll bridge' nature of flavors in consumer staples."
    elif company == "Fuchs SE":
        thesis = "World's largest independent lubricant manufacturer. Highly specialized and technically integrated with customers."
        moat = "Process Power: Specialized formulations for thousands of applications. Switching Costs: Criticality of lubricants in high-value machinery."
        performance = "Long history of dividend increases and steady profitability."
        risks = "Transition to EVs reducing demand for engine oils (mitigated by industrial/thermal management fluids)."
        architect = "Munger would admire the niche dominance and family-controlled stability."
    elif company == "Sartorius":
        thesis = "Mission-critical supplier to the biopharma industry. Dominant in 'single-use' technologies for biologic drug manufacturing."
        moat = "Switching Costs: Highly regulated manufacturing processes make changing suppliers difficult. Process Power: High-tech membrane and filtration technology."
        performance = "Explosive growth driven by the rise of biologics and biosimilars."
        risks = "Post-pandemic inventory destocking; high valuation multiples."
        architect = "Lynch: 'Selling the picks and shovels for the biotech gold rush.'"
    elif company == "Nemetschek":
        thesis = "European leader in AEC (Architecture, Engineering, Construction) software. Strong position in BIM (Building Information Modeling)."
        moat = "Network Effects: Industry standard for collaboration in construction projects. Switching Costs: High learning curve and integration into workflows."
        performance = "Transitioning to SaaS; consistent high margins and organic growth."
        risks = "Cyclicality of the construction industry; competition from Autodesk."
        architect = "Munger: 'Software is a great business once you are the standard.'"
    elif company == "CTS Eventim":
        thesis = "European ticketing and live entertainment monopoly. Vertically integrated from venues to software."
        moat = "Network Effects: Promoters want the largest audience; fans go where the tickets are. Scale Economies: Dominant platform in Europe."
        performance = "High cash flow generation and dominance in the European market."
        risks = "Regulatory scrutiny of ticketing fees; emergence of direct-to-fan platforms."
        architect = "Buffett: 'A franchise is a business where you can raise prices without losing customers.'"
    elif company == "Sixt SE":
        thesis = "Premium car rental company with superior technology and fleet management. Family-run with an owner-operator mindset."
        moat = "Branding: Premium positioning and 'cool' marketing. Scale Economies: Large fleet buying power and efficient logistics."
        performance = "Superior margins compared to peers like Hertz/Avis."
        risks = "Autonomous driving disruption; volatility in used car prices."
        architect = "Lynch: 'The best-managed company in a tough industry.'"
    elif company == "Carl Zeiss Meditec":
        thesis = "Global leader in ophthalmology and microsurgery technology. Beneficiary of aging global demographics."
        moat = "Process Power: Cutting-edge optics and laser technology. Switching Costs: Surgeons trained on Zeiss equipment are reluctant to switch."
        performance = "Consistent growth driven by cataract and refractive surgeries."
        risks = "Healthcare budget constraints; competition from Alcon."
        architect = "Buffett: 'Pricing power in a specialized medical niche.'"
    elif company == "WEG SA":
        thesis = "Brazilian industrial giant. World-class manufacturer of electric motors and automation. Extreme efficiency and vertical integration."
        moat = "Scale Economies: Massive production efficiency. Process Power: The 'WEG Way' of manufacturing and cost control."
        performance = "Consistent multi-decade compounder with high ROIC."
        risks = "Currency volatility (BRL); global industrial slowdown."
        architect = "Munger: 'A fan of efficient, honest, and hardworking management.'"
    elif company == "Raia Drogasil":
        thesis = "The 'Walgreens of Brazil' but with much better execution. Dominant pharmacy chain with superior logistics."
        moat = "Scale Economies: Unrivaled density and logistics in Brazil. Branding: Trust and convenience leader."
        performance = "Exceptional growth through store expansion and digital integration."
        risks = "Regulatory changes in drug pricing; competition from e-commerce."
        architect = "Buffett: 'A simple business executed perfectly.'"
    elif company == "Itaú Unibanco":
        thesis = "Largest private bank in Latin America. Highly profitable with a strong technology moat and conservative risk management."
        moat = "Scale Economies: Largest deposit base in Brazil. Switching Costs: Deeply integrated into the Brazilian financial ecosystem."
        performance = "Consistently high ROE (20%+) despite Brazilian macro volatility."
        risks = "Fintech disruption (Nubank); Brazilian political/macro risk."
        architect = "Buffett: 'A well-run bank is a wonderful business.'"
    elif company == "Localiza":
        thesis = "Dominant car rental and fleet management company in Brazil. Superior cost of capital and used car sales engine."
        moat = "Scale Economies: Massive purchasing power for vehicles. Counter-Positioning: Integrated 'Seminovos' sales model."
        performance = "High growth and superior returns on invested capital."
        risks = "High interest rates increasing cost of debt; Brazilian macro."
        architect = "Lynch: 'A local champion that dominates its geography.'"
    elif company == "Equatorial Energia":
        thesis = "Efficiency turnaround specialist in the Brazilian power sector. Acquires distressed utilities and optimizes them."
        moat = "Process Power: Proprietary operational turnaround methodology. Scale Economies: Large-scale utility operator."
        performance = "Phenomenal returns through operational improvements and capital allocation."
        risks = "Regulatory risk in utility tariffs; high debt levels."
        architect = "Munger: 'Admirable for their ability to improve broken systems.'"
    elif company == "DBS Bank":
        thesis = "Southeast Asia's largest bank. Digital transformation leader with dominant positioning in Singapore and expansion into India/Indonesia."
        moat = "Scale Economies: Regional dominance. Switching Costs: Integrated digital banking ecosystem."
        performance = "Strong dividend payer with growing regional footprint."
        risks = "Exposure to China/Regional slowdown; interest rate sensitivity."
        architect = "Buffett: 'A fortress balance sheet in a growing region.'"
    elif company == "Bank Central Asia":
        thesis = "Indonesia's premier private bank. Known for its low-cost CASA (Current Account Savings Account) base and superior technology."
        moat = "Scale Economies: Dominant payment system in Indonesia. Switching Costs: The primary transaction bank for Indonesian businesses."
        performance = "One of the most profitable banks globally with high ROE and low NPLs."
        risks = "Indonesian macro-economic volatility; fintech competition."
        architect = "Munger: 'The low-cost producer in banking is a winner.'"
    elif company == "CP All":
        thesis = "Operator of 7-Eleven in Thailand. A dominant infrastructure play on Thai consumption."
        moat = "Scale Economies: Unbeatable store density and logistics. Branding: 7-Eleven is a daily necessity in Thailand."
        performance = "Resilient growth driven by store expansion and product mix."
        risks = "High debt from acquisitions; slowing Thai population growth."
        architect = "Buffett: 'A business that people visit every single day.'"
    elif company == "Public Bank":
        thesis = "The most efficient bank in Malaysia. Legendary for its low cost-to-income ratio and conservative lending."
        moat = "Process Power: Extreme cost control and credit culture. Branding: Reputation for safety and stability."
        performance = "Decades of uninterrupted profitability and dividend growth."
        risks = "Saturated Malaysian market; transition to new leadership."
        architect = "Buffett: 'A bank that avoids the mistakes of its peers.'"
    elif company == "Sea Ltd":
        thesis = "The 'Amazon/Tencent of SE Asia'. Dominant in e-commerce (Shopee) and gaming (Garena), with growing fintech (SeaMoney)."
        moat = "Network Effects: Shopee's buyer-seller ecosystem. Scale Economies: Logistics dominance in SE Asia."
        performance = "Hyper-growth followed by a pivot to profitability."
        risks = "Intense competition from TikTok/Lazada; reliance on gaming cash flow."
        architect = "Lynch: 'A high-growth story in an emerging middle class.'"
    elif company == "Investor AB":
        thesis = "Investment vehicle of the Wallenberg family. Provides exposure to high-quality Swedish industrials (ABB, Atlas Copco, etc.)."
        moat = "Process Power: Active ownership and industrial expertise. Scale Economies: Large-scale capital pool."
        performance = "Consistent outperformance of the Swedish market over decades."
        risks = "Net Asset Value (NAV) discount volatility; concentration in Swedish industrials."
        architect = "Buffett: 'A mini-Berkshire of the Nordics.'"
    elif company == "Atlas Copco":
        thesis = "World leader in compressors, vacuum solutions, and industrial tools. Known for its decentralized model and service-heavy revenue."
        moat = "Switching Costs: Mission-critical equipment with high service requirements. Process Power: Highly decentralized and agile culture."
        performance = "Incredible compounder with high margins and ROIC."
        risks = "Cyclicality of industrial production; competition in vacuum technology."
        architect = "Munger: 'A masterpiece of industrial management.'"
    elif company == "Assa Abloy":
        thesis = "Global leader in access solutions (locks, doors, entrance automation). Growth through continuous M&A."
        moat = "Switching Costs: Installed base and service contracts. Scale Economies: Global leader in a fragmented market."
        performance = "Consistent growth and margin expansion through acquisition synergies."
        risks = "Integration risk of acquisitions; slowdown in construction."
        architect = "Lynch: 'Dominating a fragmented and necessary niche.'"
    elif company == "Hexagon AB":
        thesis = "Global leader in digital reality solutions (sensors, software, autonomous technologies)."
        moat = "Process Power: High-end sensor and software integration. Switching Costs: Deeply embedded in industrial workflows."
        performance = "Pivoted from industrials to high-margin software and sensors."
        risks = "Technological disruption; high valuation."
        architect = "Munger: 'Information is the most valuable commodity.'"
    elif company == "Novo Nordisk":
        thesis = "Global leader in diabetes and obesity care. Dominant position in GLP-1 medications (Ozempic/Wegovy)."
        moat = "Cornered Resource: Patents and manufacturing expertise in GLP-1s. Scale Economies: Massive production scale for biologics."
        performance = "Recent explosive growth driven by the obesity market; 20%+ long-term CAGR."
        risks = "Drug pricing legislation; competition from Eli Lilly; supply constraints."
        architect = "Lynch: 'Investing in a medical revolution.'"
    elif company == "General Electric":
        thesis = "A cautionary tale of over-financialization and diworsification. From 'Godhood' under Jack Welch to near-collapse."
        moat = "Eroded Power: Once had Scale and Branding, lost through poor capital allocation and opaque accounting."
        performance = "Decades of wealth destruction after the 2000 peak."
        risks = "The 'Complexity Trap' and 'Financial Engineering' anti-models."
        architect = "Munger: 'A classic example of how incentives and culture can go wrong.'"
    elif company == "IBM":
        thesis = "The 'Innovation Trap'. Dominated the mainframe era but failed to lead in PC, Cloud, and AI transitions despite deep R&D."
        moat = "Switching Costs: Still exists in mainframes, but the moat 'bridge' didn't reach the new islands of tech."
        performance = "Stagnant revenue and reliance on share buybacks for years."
        risks = "Legacy tech debt; inability to attract top-tier AI talent compared to Big Tech."
        architect = "Buffett: 'Even a great moat can be filled in by technology shifts.'"
    elif company == "Xerox":
        thesis = "The 'Missing the Graphic Interface' tale. Invented the future (GUI, Mouse, Ethernet) at PARC but failed to commercialize it."
        moat = "Process Power (R&D): High, but lack of Strategic Direction led to value capture by others (Apple, Microsoft)."
        performance = "Gradual decline from a tech pioneer to a struggling hardware vendor."
        risks = "Bureaucratic inertia; failure to see the 'Next Big Thing'."
        architect = "Lynch: 'The company that had it all and gave it away.'"
    elif company == "Kodak":
        thesis = "The 'Digital Blindness' tale. Invented the digital camera but suppressed it to protect its high-margin film business."
        moat = "Branding: Once world-class, now a ghost. Scale Economies: Lost as the world moved from chemicals to bits."
        performance = "Bankruptcy in 2012; a total loss for long-term shareholders."
        risks = "Creative destruction; the 'Innovator's Dilemma'."
        architect = "Munger: 'Cannibalize yourself before someone else does.'"
    elif company == "Nokia":
        thesis = "The 'Platform Burning' tale. Dominated mobile phones but was decimated by the iPhone/Android shift due to software failure."
        moat = "Scale Economies: Massive in hardware, but irrelevant when the 'Game' shifted to Software Ecosystems."
        performance = "Massive loss of market value; currently a telecom infrastructure company."
        risks = "Ecosystem Network Effects (iOS/Android) over hardware scale."
        architect = "Lynch: 'The game can change overnight.'"
    elif company == "L'Oréal":
        thesis = "The world's largest beauty company. A master of brand building and global distribution."
        moat = "Branding: A portfolio of iconic brands. Scale Economies: Largest R&D and marketing budget in beauty."
        performance = "Decades of consistent growth and high margins."
        risks = "Emergence of 'indie' beauty brands on social media; China slowdown."
        architect = "Buffett: 'A share of mind is a share of market.'"
    elif company == "Hermès":
        thesis = "The pinnacle of luxury. Extreme scarcity and craftsmanship-led growth."
        moat = "Branding: Unrivaled prestige. Process Power: Hand-crafted production by master artisans. Cornered Resource: Supply of ultra-high-quality leather."
        performance = "Exceptional resilience and long-term value compounding."
        risks = "Over-exposure to the ultra-wealthy segment; succession risk."
        architect = "Munger: 'A business that sells for 10x cost and people wait in line for it.'"
    elif company == "Ferrari":
        thesis = "A luxury brand disguised as a car company. Veblen good with waiting lists and high pricing power."
        moat = "Branding: The most powerful brand in the world. Scale Economies: High margins despite low volume. Switching Costs: Loyalty to the 'Tifosi' culture."
        performance = "Incredible stock performance since IPO; software-like margins."
        risks = "Transition to electric supercars; brand dilution through over-extension."
        architect = "Buffett: 'A business with an iron-clad franchise.'"
    elif company == "TSMC":
        thesis = "The world's most important company. The sole provider of cutting-edge semiconductor manufacturing."
        moat = "Process Power: Unmatched manufacturing precision. Scale Economies: Massive CapEx requirements create a high barrier. Network Effects: Ecosystem of design tools and customers."
        performance = "Central to the AI and mobile revolutions; dominant market share."
        risks = "Geopolitical risk (Taiwan Strait); concentration of global tech on one island."
        architect = "Munger: 'A tech moat that is almost impossible to cross.'"
    elif company == "Samsung Electronics":
        thesis = "A vertically integrated tech titan. Leader in Memory (DRAM/NAND) and high-end OLED displays."
        moat = "Scale Economies: Massive production scale in chips and screens. Process Power: R&D leadership in semiconductor manufacturing."
        performance = "Cyclical but dominant; a core play on global tech hardware."
        risks = "Memory price volatility; competition from TSMC and Chinese chipmakers."
        architect = "Buffett: 'A tough, cyclical, but ultimately dominant industrial giant.'"
    else:
        thesis = "Generic thesis"
        moat = "Generic moat"
        performance = "Generic performance"
        risks = "Generic risks"
        architect = "Generic architect"

    return thesis, moat, performance, risks, architect

for name, ticker, sector, country, folder, filename in stocks:
    sector_tag = sector.lower().replace(" ", "-")
    country_tag = country.lower().replace(" ", "-")
    
    thesis, moat, performance, risks, architect = get_content(name, ticker, sector, country)
    
    content = TEMPLATE.format(
        sector_tag=sector_tag,
        country_tag=country_tag,
        ticker=ticker,
        company=name,
        thesis=thesis,
        moat=moat,
        performance=performance,
        risks=risks,
        architect=architect
    )
    
    full_folder_path = os.path.join(BASE_PATH, folder)
    if not os.path.exists(full_folder_path):
        os.makedirs(full_folder_path)
    
    file_path = os.path.join(full_folder_path, filename + ".md")
    
    # Existing notes carry fetched market data and history tables; never clobber them silently.
    if os.path.exists(file_path) and "--force" not in sys.argv:
        print(f"Skipped (exists, pass --force to overwrite): {file_path}")
        continue

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created: {file_path}")
