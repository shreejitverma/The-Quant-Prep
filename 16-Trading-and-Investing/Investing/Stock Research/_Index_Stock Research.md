---
type: MOC
tags: [moc, investing, stocks, global-research, godhood]
---
# Global Stock Research Map of Content

> "Price is what you pay. Value is what you get." - Warren Buffett

## Quant Suite Intelligence
- **[[16-Trading-and-Investing/Investing/Risk Management/Correlation Matrix|Portfolio Correlation Matrix]]**: Identifying hidden risks and diversification offsets.
- **[[16-Trading-and-Investing/Investing/Macro & Micro Economics/Global Macro Report|Global Macro Report]]**: Live interest rate and volatility tracking.

## Sector Benchmarking Reports
- **[[16-Trading-and-Investing/Investing/Stock Research/Technology/_Sector_Analysis|Technology Benchmark]]** | **[[16-Trading-and-Investing/Investing/Stock Research/Financials/_Sector_Analysis|Financials Benchmark]]**
- **[[16-Trading-and-Investing/Investing/Stock Research/Healthcare/_Sector_Analysis|Healthcare Benchmark]]** | **[[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/_Sector_Analysis|Staples Benchmark]]**
- **[[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/_Sector_Analysis|Discretionary Benchmark]]** | **[[16-Trading-and-Investing/Investing/Stock Research/Industrials/_Sector_Analysis|Industrials Benchmark]]**

## Superinvestor Value Screener
```dataview
TABLE 
  value_metrics.quality.roe as "ROE", 
  value_metrics.implied_growth_rate as "Implied Growth",
  value_metrics.returns.cagr_10y as "10y CAGR",
  value_metrics.valuation.fcf_yield as "FCF Yield",
  value_metrics.valuation.peg_ratio as "PEG"
FROM "16-Trading-and-Investing/Investing/Stock Research"
WHERE value_metrics != null
SORT value_metrics.quality.roe DESC
```

## Sector & Geography Intelligence

### Communication Services
- **China**: [[16-Trading-and-Investing/Investing/Stock Research/Communication Services/China/NetEase (NTES)|NetEase (NTES)]], [[16-Trading-and-Investing/Investing/Stock Research/Communication Services/China/Tencent|Tencent]]
- **Japan**: [[16-Trading-and-Investing/Investing/Stock Research/Communication Services/Japan/Nintendo|Nintendo]]
- **Other**: [[16-Trading-and-Investing/Investing/Stock Research/Communication Services/Germany/CTS Eventim (EVD)|CTS Eventim (EVD)]]
- **US**: [[16-Trading-and-Investing/Investing/Stock Research/Communication Services/US/Meta Platforms (META)|Meta Platforms (META)]], [[16-Trading-and-Investing/Investing/Stock Research/Communication Services/US/Netflix (NFLX)|Netflix (NFLX)]]

### Consumer Discretionary
- **China**: [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/China/Alibaba|Alibaba]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/China/BYD Company|BYD Company]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/China/Kweichou Moutai (600519)|Kweichou Moutai (600519)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/China/Meituan (3690.HK)|Meituan (3690.HK)]]
- **Europe**: [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/Europe/Ferrari (RACE.MI)|Ferrari (RACE.MI)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/Europe/France/Hermès (RMS.PA)|Hermès (RMS.PA)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/Europe/Hermès|Hermès]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/Europe/Inditex (ITX.MC)|Inditex (ITX.MC)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/Europe/Italy/Ferrari (RACE.MI)|Ferrari (RACE.MI)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/Europe/LVMH (MC.PA)|LVMH (MC.PA)]]
- **India**: [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/India/Titan Company|Titan Company]]
- **Japan**: [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/Japan/Fast Retailing (9983)|Fast Retailing (9983)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/Japan/Toyota Motor|Toyota Motor]]
- **Other**: [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/Rest of World/MercadoLibre (MELI)|MercadoLibre (MELI)]]
- **US**: [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/US/Amazon (AMZN)|Amazon (AMZN)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/US/Home Depot (HD)|Home Depot (HD)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/US/Lowe’s (LOW)|Lowe’s (LOW)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/US/McDonalds (MCD)|McDonalds (MCD)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/US/Nike (NKE)|Nike (NKE)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Discretionary/US/Starbucks (SBUX)|Starbucks (SBUX)]]

### Consumer Staples
- **Europe**: [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/Europe/France/L’Oréal (OR.PA)|L’Oréal (OR.PA)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/Europe/L’Oréal (OR.PA)|L’Oréal (OR.PA)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/Europe/Nestlé|Nestlé]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/Europe/Unilever (ULVR.L)|Unilever (ULVR.L)]]
- **India**: [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/India/Asian Paints|Asian Paints]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/India/Hindustan Unilever (HINDUNILVR)|Hindustan Unilever (HINDUNILVR)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/India/Marico (MARICO)|Marico (MARICO)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/India/Nestle India (NESTLEIND)|Nestle India (NESTLEIND)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/India/Pidilite Industries (PIDILITIND)|Pidilite Industries (PIDILITIND)]]
- **Thailand**: [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/Thailand/CP All (CPALL)|CP All (CPALL)]]
- **US**: [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/US/Coca-Cola (KO)|Coca-Cola (KO)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/US/Costco (COST)|Costco (COST)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/US/PepsiCo (PEP)|PepsiCo (PEP)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/US/Procter & Gamble (PG)|Procter & Gamble (PG)]], [[16-Trading-and-Investing/Investing/Stock Research/Consumer Staples/US/Walmart (WMT)|Walmart (WMT)]]

### Energy
- **India**: [[16-Trading-and-Investing/Investing/Stock Research/Energy/India/Reliance Industries|Reliance Industries]]
- **Middle East**: [[16-Trading-and-Investing/Investing/Stock Research/Energy/Middle East/Saudi Aramco|Saudi Aramco]]
- **US**: [[16-Trading-and-Investing/Investing/Stock Research/Energy/US/Chevron (CVX)|Chevron (CVX)]], [[16-Trading-and-Investing/Investing/Stock Research/Energy/US/Exxon Mobil (XOM)|Exxon Mobil (XOM)]]

### Financials
- **Brazil**: [[16-Trading-and-Investing/Investing/Stock Research/Financials/Brazil/Itaú Unibanco (ITUB4)|Itaú Unibanco (ITUB4)]]
- **India**: [[16-Trading-and-Investing/Investing/Stock Research/Financials/India/Bajaj Finance (BAJFINANCE)|Bajaj Finance (BAJFINANCE)]], [[16-Trading-and-Investing/Investing/Stock Research/Financials/India/HDFC Bank|HDFC Bank]], [[16-Trading-and-Investing/Investing/Stock Research/Financials/India/ICICI Bank (ICICIBANK)|ICICI Bank (ICICIBANK)]]
- **Indonesia**: [[16-Trading-and-Investing/Investing/Stock Research/Financials/Indonesia/Bank Central Asia (BBCA)|Bank Central Asia (BBCA)]]
- **Malaysia**: [[16-Trading-and-Investing/Investing/Stock Research/Financials/Malaysia/Public Bank (PBBANK)|Public Bank (PBBANK)]]
- **Middle East**: [[16-Trading-and-Investing/Investing/Stock Research/Financials/Middle East/Emirates NBD|Emirates NBD]]
- **Other**: [[16-Trading-and-Investing/Investing/Stock Research/Financials/Rest of World/Commonwealth Bank (CBA.AX)|Commonwealth Bank (CBA.AX)]]
- **Singapore**: [[16-Trading-and-Investing/Investing/Stock Research/Financials/Singapore/DBS Bank (D05)|DBS Bank (D05)]]
- **Sweden**: [[16-Trading-and-Investing/Investing/Stock Research/Financials/Sweden/Investor AB (INVE.B)|Investor AB (INVE.B)]]
- **US**: [[16-Trading-and-Investing/Investing/Stock Research/Financials/US/Berkshire Hathaway (BRK.B)|Berkshire Hathaway (BRK.B)]], [[16-Trading-and-Investing/Investing/Stock Research/Financials/US/Fair Isaac (FICO)|Fair Isaac (FICO)]], [[16-Trading-and-Investing/Investing/Stock Research/Financials/US/Goldman Sachs (GS)|Goldman Sachs (GS)]], [[16-Trading-and-Investing/Investing/Stock Research/Financials/US/JPMorgan Chase (JPM)|JPMorgan Chase (JPM)]], [[16-Trading-and-Investing/Investing/Stock Research/Financials/US/Mastercard (MA)|Mastercard (MA)]], [[16-Trading-and-Investing/Investing/Stock Research/Financials/US/Moody’s (MCO)|Moody’s (MCO)]], [[16-Trading-and-Investing/Investing/Stock Research/Financials/US/S&P Global (SPGI)|S&P Global (SPGI)]], [[16-Trading-and-Investing/Investing/Stock Research/Financials/US/Visa (V)|Visa (V)]]

### Healthcare
- **Brazil**: [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/Brazil/Raia Drogasil (RADL3)|Raia Drogasil (RADL3)]]
- **Europe**: [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/Europe/Novo Nordisk (NVO)|Novo Nordisk (NVO)]], [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/Europe/Roche|Roche]]
- **India**: [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/India/Sun Pharma (SUNPHARMA)|Sun Pharma (SUNPHARMA)]]
- **Japan**: [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/Japan/Hoya (7741)|Hoya (7741)]]
- **Other**: [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/Germany/Carl Zeiss Meditec (AFX)|Carl Zeiss Meditec (AFX)]], [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/Germany/Sartorius (SRT3)|Sartorius (SRT3)]], [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/Rest of World/CSL (CSL.AX)|CSL (CSL.AX)]]
- **US**: [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/US/Danaher (DHR)|Danaher (DHR)]], [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/US/Eli Lilly (LLY)|Eli Lilly (LLY)]], [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/US/IDEXX Laboratories (IDXX)|IDEXX Laboratories (IDXX)]], [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/US/Johnson & Johnson (JNJ)|Johnson & Johnson (JNJ)]], [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/US/Stryker (SYK)|Stryker (SYK)]], [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/US/Thermo Fisher Scientific (TMO)|Thermo Fisher Scientific (TMO)]], [[16-Trading-and-Investing/Investing/Stock Research/Healthcare/US/UnitedHealth Group (UNH)|UnitedHealth Group (UNH)]]

### Industrials
- **Brazil**: [[16-Trading-and-Investing/Investing/Stock Research/Industrials/Brazil/Localiza (RENT3)|Localiza (RENT3)]], [[16-Trading-and-Investing/Investing/Stock Research/Industrials/Brazil/WEG SA (WEGE3)|WEG SA (WEGE3)]]
- **Europe**: [[16-Trading-and-Investing/Investing/Stock Research/Industrials/Europe/Schneider Electric (SU.PA)|Schneider Electric (SU.PA)]], [[16-Trading-and-Investing/Investing/Stock Research/Industrials/Europe/Siemens (SIE.DE)|Siemens (SIE.DE)]]
- **India**: [[16-Trading-and-Investing/Investing/Stock Research/Industrials/India/Larsen & Toubro (LT)|Larsen & Toubro (LT)]]
- **Japan**: [[16-Trading-and-Investing/Investing/Stock Research/Industrials/Japan/Fanuc (6954)|Fanuc (6954)]]
- **Other**: [[16-Trading-and-Investing/Investing/Stock Research/Industrials/Germany/Rational AG (RAA)|Rational AG (RAA)]], [[16-Trading-and-Investing/Investing/Stock Research/Industrials/Germany/Sixt SE (SIX2)|Sixt SE (SIX2)]]
- **Sweden**: [[16-Trading-and-Investing/Investing/Stock Research/Industrials/Sweden/Assa Abloy (ASSA.B)|Assa Abloy (ASSA.B)]], [[16-Trading-and-Investing/Investing/Stock Research/Industrials/Sweden/Atlas Copco (ATCO.A)|Atlas Copco (ATCO.A)]]
- **US**: [[16-Trading-and-Investing/Investing/Stock Research/Industrials/US/Caterpillar (CAT)|Caterpillar (CAT)]], [[16-Trading-and-Investing/Investing/Stock Research/Industrials/US/Honeywell (HON)|Honeywell (HON)]], [[16-Trading-and-Investing/Investing/Stock Research/Industrials/US/Lockheed Martin (LMT)|Lockheed Martin (LMT)]]

### Materials
- **Europe**: [[16-Trading-and-Investing/Investing/Stock Research/Materials/Europe/Air Liquide (AI.PA)|Air Liquide (AI.PA)]]
- **Japan**: [[16-Trading-and-Investing/Investing/Stock Research/Materials/Japan/Shin-Etsu Chemical (4063)|Shin-Etsu Chemical (4063)]]
- **Other**: [[16-Trading-and-Investing/Investing/Stock Research/Materials/Germany/Fuchs SE (FPE3)|Fuchs SE (FPE3)]], [[16-Trading-and-Investing/Investing/Stock Research/Materials/Germany/Symrise AG (SY1)|Symrise AG (SY1)]]
- **US**: [[16-Trading-and-Investing/Investing/Stock Research/Materials/US/Sherwin-Williams (SHW)|Sherwin-Williams (SHW)]]

### Technology
- **Europe**: [[16-Trading-and-Investing/Investing/Stock Research/Technology/Europe/ASML (ASML)|ASML (ASML)]], [[16-Trading-and-Investing/Investing/Stock Research/Technology/Europe/SAP|SAP]]
- **India**: [[16-Trading-and-Investing/Investing/Stock Research/Technology/India/Infosys (INFY)|Infosys (INFY)]], [[16-Trading-and-Investing/Investing/Stock Research/Technology/India/TCS|TCS]]
- **Japan**: [[16-Trading-and-Investing/Investing/Stock Research/Technology/Japan/Keyence|Keyence]], [[16-Trading-and-Investing/Investing/Stock Research/Technology/Japan/Murata Manufacturing (6981)|Murata Manufacturing (6981)]], [[16-Trading-and-Investing/Investing/Stock Research/Technology/Japan/Sony Group|Sony Group]]
- **Other**: [[16-Trading-and-Investing/Investing/Stock Research/Technology/Germany/Nemetschek (NEM)|Nemetschek (NEM)]], [[16-Trading-and-Investing/Investing/Stock Research/Technology/Rest of World/Shopify (SHOP)|Shopify (SHOP)]]
- **Singapore**: [[16-Trading-and-Investing/Investing/Stock Research/Technology/Singapore/Sea Ltd (SE)|Sea Ltd (SE)]]
- **South Korea**: [[16-Trading-and-Investing/Investing/Stock Research/Technology/South Korea/Samsung Electronics|Samsung Electronics]]
- **Sweden**: [[16-Trading-and-Investing/Investing/Stock Research/Technology/Sweden/Hexagon AB (HEXA.B)|Hexagon AB (HEXA.B)]]
- **Taiwan**: [[16-Trading-and-Investing/Investing/Stock Research/Technology/Taiwan/TSMC|TSMC]]
- **US**: [[16-Trading-and-Investing/Investing/Stock Research/Technology/US/Adobe (ADBE)|Adobe (ADBE)]], [[16-Trading-and-Investing/Investing/Stock Research/Technology/US/Alphabet (GOOGL)|Alphabet (GOOGL)]], [[16-Trading-and-Investing/Investing/Stock Research/Technology/US/Apple (AAPL)|Apple (AAPL)]], [[16-Trading-and-Investing/Investing/Stock Research/Technology/US/Intuit (INTU)|Intuit (INTU)]], [[16-Trading-and-Investing/Investing/Stock Research/Technology/US/Microsoft (MSFT)|Microsoft (MSFT)]], [[16-Trading-and-Investing/Investing/Stock Research/Technology/US/NVIDIA (NVDA)|NVIDIA (NVDA)]], [[16-Trading-and-Investing/Investing/Stock Research/Technology/US/Oracle (ORCL)|Oracle (ORCL)]], [[16-Trading-and-Investing/Investing/Stock Research/Technology/US/Salesforce (CRM)|Salesforce (CRM)]]

### Utilities
- **Brazil**: [[16-Trading-and-Investing/Investing/Stock Research/Utilities/Brazil/Equatorial Energia (EQTL3)|Equatorial Energia (EQTL3)]]

### Historical Cautionary Tales
- [[16-Trading-and-Investing/Investing/Stock Research/Historical/General Electric (The Fall from Godhood)|General Electric (The Fall from Godhood)]]
- [[16-Trading-and-Investing/Investing/Stock Research/Historical/IBM (The Innovation Trap)|IBM (The Innovation Trap)]]
- [[16-Trading-and-Investing/Investing/Stock Research/Historical/Kodak (The Digital Blindness)|Kodak (The Digital Blindness)]]
- [[16-Trading-and-Investing/Investing/Stock Research/Historical/Nokia (The Platform Burning)|Nokia (The Platform Burning)]]
- [[16-Trading-and-Investing/Investing/Stock Research/Historical/Xerox (Missing the Graphic Interface)|Xerox (Missing the Graphic Interface)]]

---
[[16-Trading-and-Investing/Investing/_Index_Investing|Back to Investing]]
