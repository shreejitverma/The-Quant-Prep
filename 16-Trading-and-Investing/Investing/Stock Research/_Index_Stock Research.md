---
type: MOC
tags: [moc, investing, stocks, value-investing, godhood]
---
# Global Stock Research Map of Content

> "Price is what you pay. Value is what you get." - Warren Buffett

## Economic Intelligence
- **[[16-Trading-and-Investing/Investing/Macro & Micro Economics/Global Macro Report|Global Macro Report]]**: Interest Rates, Volatility, and Indices.
- **[[16-Trading-and-Investing/Investing/Macro & Micro Economics/Sector & Commodity Report|Sector & Commodity Report]]**: Oil, Gold, and Industrial Metals.

## Superinvestor Value Screener
```dataview
TABLE 
  value_metrics.returns.cagr_10y as "10y CAGR", 
  value_metrics.quality.roe as "ROE", 
  value_metrics.quality.debt_to_equity as "D/E",
  value_metrics.valuation.fcf_yield as "FCF Yield",
  value_metrics.valuation.peg_ratio as "PEG"
FROM "16-Trading-and-Investing/Investing/Stock Research"
WHERE value_metrics != null
SORT value_metrics.quality.roe DESC
```

## Sector & Geography Intelligence

### Communication Services
- **China**: [[../Investing/Stock Research/Communication Services/China/NetEase (NTES)|NetEase (NTES)]], [[../Investing/Stock Research/Communication Services/China/Tencent|Tencent]]
- **Japan**: [[../Investing/Stock Research/Communication Services/Japan/Nintendo|Nintendo]]
- **Other**: [[../Investing/Stock Research/Communication Services/Germany/CTS Eventim (EVD)|CTS Eventim (EVD)]], [[../Investing/Stock Research/Communication Services/_Sector_Analysis|_Sector_Analysis]]
- **US**: [[../Investing/Stock Research/Communication Services/US/Meta Platforms (META)|Meta Platforms (META)]], [[../Investing/Stock Research/Communication Services/US/Netflix (NFLX)|Netflix (NFLX)]]

### Consumer Discretionary
- **China**: [[../Investing/Stock Research/Consumer Discretionary/China/Alibaba|Alibaba]], [[../Investing/Stock Research/Consumer Discretionary/China/BYD Company|BYD Company]], [[../Investing/Stock Research/Consumer Discretionary/China/Kweichou Moutai (600519)|Kweichou Moutai (600519)]], [[../Investing/Stock Research/Consumer Discretionary/China/Meituan (3690.HK)|Meituan (3690.HK)]]
- **Europe**: [[../Investing/Stock Research/Consumer Discretionary/Europe/Ferrari (RACE.MI)|Ferrari (RACE.MI)]], [[../Investing/Stock Research/Consumer Discretionary/Europe/France/Hermès (RMS.PA)|Hermès (RMS.PA)]], [[../Investing/Stock Research/Consumer Discretionary/Europe/Hermès|Hermès]], [[../Investing/Stock Research/Consumer Discretionary/Europe/Inditex (ITX.MC)|Inditex (ITX.MC)]], [[../Investing/Stock Research/Consumer Discretionary/Europe/Italy/Ferrari (RACE.MI)|Ferrari (RACE.MI)]], [[../Investing/Stock Research/Consumer Discretionary/Europe/LVMH (MC.PA)|LVMH (MC.PA)]]
- **India**: [[../Investing/Stock Research/Consumer Discretionary/India/Titan Company|Titan Company]]
- **Japan**: [[../Investing/Stock Research/Consumer Discretionary/Japan/Fast Retailing (9983)|Fast Retailing (9983)]], [[../Investing/Stock Research/Consumer Discretionary/Japan/Toyota Motor|Toyota Motor]]
- **Other**: [[../Investing/Stock Research/Consumer Discretionary/Rest of World/MercadoLibre (MELI)|MercadoLibre (MELI)]], [[../Investing/Stock Research/Consumer Discretionary/_Sector_Analysis|_Sector_Analysis]]
- **US**: [[../Investing/Stock Research/Consumer Discretionary/US/Amazon (AMZN)|Amazon (AMZN)]], [[../Investing/Stock Research/Consumer Discretionary/US/Home Depot (HD)|Home Depot (HD)]], [[../Investing/Stock Research/Consumer Discretionary/US/Lowe’s (LOW)|Lowe’s (LOW)]], [[../Investing/Stock Research/Consumer Discretionary/US/McDonalds (MCD)|McDonalds (MCD)]], [[../Investing/Stock Research/Consumer Discretionary/US/Nike (NKE)|Nike (NKE)]], [[../Investing/Stock Research/Consumer Discretionary/US/Starbucks (SBUX)|Starbucks (SBUX)]]

### Consumer Staples
- **Europe**: [[../Investing/Stock Research/Consumer Staples/Europe/France/L’Oréal (OR.PA)|L’Oréal (OR.PA)]], [[../Investing/Stock Research/Consumer Staples/Europe/L’Oréal (OR.PA)|L’Oréal (OR.PA)]], [[../Investing/Stock Research/Consumer Staples/Europe/Nestlé|Nestlé]], [[../Investing/Stock Research/Consumer Staples/Europe/Unilever (ULVR.L)|Unilever (ULVR.L)]]
- **India**: [[../Investing/Stock Research/Consumer Staples/India/Asian Paints|Asian Paints]], [[../Investing/Stock Research/Consumer Staples/India/Hindustan Unilever (HINDUNILVR)|Hindustan Unilever (HINDUNILVR)]], [[../Investing/Stock Research/Consumer Staples/India/Marico (MARICO)|Marico (MARICO)]], [[../Investing/Stock Research/Consumer Staples/India/Nestle India (NESTLEIND)|Nestle India (NESTLEIND)]], [[../Investing/Stock Research/Consumer Staples/India/Pidilite Industries (PIDILITIND)|Pidilite Industries (PIDILITIND)]]
- **Other**: [[../Investing/Stock Research/Consumer Staples/_Sector_Analysis|_Sector_Analysis]]
- **Thailand**: [[../Investing/Stock Research/Consumer Staples/Thailand/CP All (CPALL)|CP All (CPALL)]]
- **US**: [[../Investing/Stock Research/Consumer Staples/US/Coca-Cola (KO)|Coca-Cola (KO)]], [[../Investing/Stock Research/Consumer Staples/US/Costco (COST)|Costco (COST)]], [[../Investing/Stock Research/Consumer Staples/US/PepsiCo (PEP)|PepsiCo (PEP)]], [[../Investing/Stock Research/Consumer Staples/US/Procter & Gamble (PG)|Procter & Gamble (PG)]], [[../Investing/Stock Research/Consumer Staples/US/Walmart (WMT)|Walmart (WMT)]]

### Energy
- **India**: [[../Investing/Stock Research/Energy/India/Reliance Industries|Reliance Industries]]
- **Middle East**: [[../Investing/Stock Research/Energy/Middle East/Saudi Aramco|Saudi Aramco]]
- **Other**: [[../Investing/Stock Research/Energy/_Sector_Analysis|_Sector_Analysis]]
- **US**: [[../Investing/Stock Research/Energy/US/Chevron (CVX)|Chevron (CVX)]], [[../Investing/Stock Research/Energy/US/Exxon Mobil (XOM)|Exxon Mobil (XOM)]]

### Financials
- **Brazil**: [[../Investing/Stock Research/Financials/Brazil/Itaú Unibanco (ITUB4)|Itaú Unibanco (ITUB4)]]
- **India**: [[../Investing/Stock Research/Financials/India/Bajaj Finance (BAJFINANCE)|Bajaj Finance (BAJFINANCE)]], [[../Investing/Stock Research/Financials/India/HDFC Bank|HDFC Bank]], [[../Investing/Stock Research/Financials/India/ICICI Bank (ICICIBANK)|ICICI Bank (ICICIBANK)]]
- **Indonesia**: [[../Investing/Stock Research/Financials/Indonesia/Bank Central Asia (BBCA)|Bank Central Asia (BBCA)]]
- **Malaysia**: [[../Investing/Stock Research/Financials/Malaysia/Public Bank (PBBANK)|Public Bank (PBBANK)]]
- **Middle East**: [[../Investing/Stock Research/Financials/Middle East/Emirates NBD|Emirates NBD]]
- **Other**: [[../Investing/Stock Research/Financials/Rest of World/Commonwealth Bank (CBA.AX)|Commonwealth Bank (CBA.AX)]], [[../Investing/Stock Research/Financials/_Sector_Analysis|_Sector_Analysis]]
- **Singapore**: [[../Investing/Stock Research/Financials/Singapore/DBS Bank (D05)|DBS Bank (D05)]]
- **Sweden**: [[../Investing/Stock Research/Financials/Sweden/Investor AB (INVE.B)|Investor AB (INVE.B)]]
- **US**: [[../Investing/Stock Research/Financials/US/Berkshire Hathaway (BRK.B)|Berkshire Hathaway (BRK.B)]], [[../Investing/Stock Research/Financials/US/Fair Isaac (FICO)|Fair Isaac (FICO)]], [[../Investing/Stock Research/Financials/US/Goldman Sachs (GS)|Goldman Sachs (GS)]], [[../Investing/Stock Research/Financials/US/JPMorgan Chase (JPM)|JPMorgan Chase (JPM)]], [[../Investing/Stock Research/Financials/US/Mastercard (MA)|Mastercard (MA)]], [[../Investing/Stock Research/Financials/US/Moody’s (MCO)|Moody’s (MCO)]], [[../Investing/Stock Research/Financials/US/S&P Global (SPGI)|S&P Global (SPGI)]], [[../Investing/Stock Research/Financials/US/Visa (V)|Visa (V)]]

### Healthcare
- **Brazil**: [[../Investing/Stock Research/Healthcare/Brazil/Raia Drogasil (RADL3)|Raia Drogasil (RADL3)]]
- **Europe**: [[../Investing/Stock Research/Healthcare/Europe/Novo Nordisk (NVO)|Novo Nordisk (NVO)]], [[../Investing/Stock Research/Healthcare/Europe/Roche|Roche]]
- **India**: [[../Investing/Stock Research/Healthcare/India/Sun Pharma (SUNPHARMA)|Sun Pharma (SUNPHARMA)]]
- **Japan**: [[../Investing/Stock Research/Healthcare/Japan/Hoya (7741)|Hoya (7741)]]
- **Other**: [[../Investing/Stock Research/Healthcare/Germany/Carl Zeiss Meditec (AFX)|Carl Zeiss Meditec (AFX)]], [[../Investing/Stock Research/Healthcare/Germany/Sartorius (SRT3)|Sartorius (SRT3)]], [[../Investing/Stock Research/Healthcare/Rest of World/CSL (CSL.AX)|CSL (CSL.AX)]], [[../Investing/Stock Research/Healthcare/_Sector_Analysis|_Sector_Analysis]]
- **US**: [[../Investing/Stock Research/Healthcare/US/Danaher (DHR)|Danaher (DHR)]], [[../Investing/Stock Research/Healthcare/US/Eli Lilly (LLY)|Eli Lilly (LLY)]], [[../Investing/Stock Research/Healthcare/US/IDEXX Laboratories (IDXX)|IDEXX Laboratories (IDXX)]], [[../Investing/Stock Research/Healthcare/US/Johnson & Johnson (JNJ)|Johnson & Johnson (JNJ)]], [[../Investing/Stock Research/Healthcare/US/Stryker (SYK)|Stryker (SYK)]], [[../Investing/Stock Research/Healthcare/US/Thermo Fisher Scientific (TMO)|Thermo Fisher Scientific (TMO)]], [[../Investing/Stock Research/Healthcare/US/UnitedHealth Group (UNH)|UnitedHealth Group (UNH)]]

### Industrials
- **Brazil**: [[../Investing/Stock Research/Industrials/Brazil/Localiza (RENT3)|Localiza (RENT3)]], [[../Investing/Stock Research/Industrials/Brazil/WEG SA (WEGE3)|WEG SA (WEGE3)]]
- **Europe**: [[../Investing/Stock Research/Industrials/Europe/Schneider Electric (SU.PA)|Schneider Electric (SU.PA)]], [[../Investing/Stock Research/Industrials/Europe/Siemens (SIE.DE)|Siemens (SIE.DE)]]
- **India**: [[../Investing/Stock Research/Industrials/India/Larsen & Toubro (LT)|Larsen & Toubro (LT)]]
- **Japan**: [[../Investing/Stock Research/Industrials/Japan/Fanuc (6954)|Fanuc (6954)]]
- **Other**: [[../Investing/Stock Research/Industrials/Germany/Rational AG (RAA)|Rational AG (RAA)]], [[../Investing/Stock Research/Industrials/Germany/Sixt SE (SIX2)|Sixt SE (SIX2)]], [[../Investing/Stock Research/Industrials/_Sector_Analysis|_Sector_Analysis]]
- **Sweden**: [[../Investing/Stock Research/Industrials/Sweden/Assa Abloy (ASSA.B)|Assa Abloy (ASSA.B)]], [[../Investing/Stock Research/Industrials/Sweden/Atlas Copco (ATCO.A)|Atlas Copco (ATCO.A)]]
- **US**: [[../Investing/Stock Research/Industrials/US/Caterpillar (CAT)|Caterpillar (CAT)]], [[../Investing/Stock Research/Industrials/US/Honeywell (HON)|Honeywell (HON)]], [[../Investing/Stock Research/Industrials/US/Lockheed Martin (LMT)|Lockheed Martin (LMT)]]

### Materials
- **Europe**: [[../Investing/Stock Research/Materials/Europe/Air Liquide (AI.PA)|Air Liquide (AI.PA)]]
- **Japan**: [[../Investing/Stock Research/Materials/Japan/Shin-Etsu Chemical (4063)|Shin-Etsu Chemical (4063)]]
- **Other**: [[../Investing/Stock Research/Materials/Germany/Fuchs SE (FPE3)|Fuchs SE (FPE3)]], [[../Investing/Stock Research/Materials/Germany/Symrise AG (SY1)|Symrise AG (SY1)]], [[../Investing/Stock Research/Materials/_Sector_Analysis|_Sector_Analysis]]
- **US**: [[../Investing/Stock Research/Materials/US/Sherwin-Williams (SHW)|Sherwin-Williams (SHW)]]

### Technology
- **Europe**: [[../Investing/Stock Research/Technology/Europe/ASML (ASML)|ASML (ASML)]], [[../Investing/Stock Research/Technology/Europe/SAP|SAP]]
- **India**: [[../Investing/Stock Research/Technology/India/Infosys (INFY)|Infosys (INFY)]], [[../Investing/Stock Research/Technology/India/TCS|TCS]]
- **Japan**: [[../Investing/Stock Research/Technology/Japan/Keyence|Keyence]], [[../Investing/Stock Research/Technology/Japan/Murata Manufacturing (6981)|Murata Manufacturing (6981)]], [[../Investing/Stock Research/Technology/Japan/Sony Group|Sony Group]]
- **Other**: [[../Investing/Stock Research/Technology/Germany/Nemetschek (NEM)|Nemetschek (NEM)]], [[../Investing/Stock Research/Technology/Rest of World/Shopify (SHOP)|Shopify (SHOP)]], [[../Investing/Stock Research/Technology/_Sector_Analysis|_Sector_Analysis]]
- **Singapore**: [[../Investing/Stock Research/Technology/Singapore/Sea Ltd (SE)|Sea Ltd (SE)]]
- **South Korea**: [[../Investing/Stock Research/Technology/South Korea/Samsung Electronics|Samsung Electronics]]
- **Sweden**: [[../Investing/Stock Research/Technology/Sweden/Hexagon AB (HEXA.B)|Hexagon AB (HEXA.B)]]
- **Taiwan**: [[../Investing/Stock Research/Technology/Taiwan/TSMC|TSMC]]
- **US**: [[../Investing/Stock Research/Technology/US/Adobe (ADBE)|Adobe (ADBE)]], [[../Investing/Stock Research/Technology/US/Alphabet (GOOGL)|Alphabet (GOOGL)]], [[../Investing/Stock Research/Technology/US/Apple (AAPL)|Apple (AAPL)]], [[../Investing/Stock Research/Technology/US/Intuit (INTU)|Intuit (INTU)]], [[../Investing/Stock Research/Technology/US/Microsoft (MSFT)|Microsoft (MSFT)]], [[../Investing/Stock Research/Technology/US/NVIDIA (NVDA)|NVIDIA (NVDA)]], [[../Investing/Stock Research/Technology/US/Oracle (ORCL)|Oracle (ORCL)]], [[../Investing/Stock Research/Technology/US/Salesforce (CRM)|Salesforce (CRM)]]

### Utilities
- **Brazil**: [[../Investing/Stock Research/Utilities/Brazil/Equatorial Energia (EQTL3)|Equatorial Energia (EQTL3)]]
- **Other**: [[../Investing/Stock Research/Utilities/_Sector_Analysis|_Sector_Analysis]]

### Historical Cautionary Tales
- [[../Investing/Stock Research/Historical/General Electric (The Fall from Godhood)|General Electric (The Fall from Godhood)]]
- [[../Investing/Stock Research/Historical/IBM (The Innovation Trap)|IBM (The Innovation Trap)]]
- [[../Investing/Stock Research/Historical/Kodak (The Digital Blindness)|Kodak (The Digital Blindness)]]
- [[../Investing/Stock Research/Historical/Nokia (The Platform Burning)|Nokia (The Platform Burning)]]
- [[../Investing/Stock Research/Historical/Xerox (Missing the Graphic Interface)|Xerox (Missing the Graphic Interface)]]

---
[[Dashboard|Back to Dashboard]]
