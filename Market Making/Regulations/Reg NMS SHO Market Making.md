Regulation NMS & SHO: Comprehensive Guide for Quantitative Developers in Market Making
Target Role: Quantitative Developer – Market Making Firm
Focus Areas: Low-latency execution, microstructure arbitrage, liquidity provision, regulatory compliance
Document Purpose: Interview preparation + production system design context
 
Executive Summary
As a quantitative developer in market making, you operate at the intersection of regulatory constraints (NMS/SHO), microstructure mechanics (NBBO/protected quotes/order types), and low-latency system design. This document provides end-to-end mastery of:
1.	Regulation NMS: How order protection, access rules, sub-penny rules, and market data rules shape routing logic, quote competition, and execution quality
2.	Regulation SHO: How short sale marking, locate, close-out, and circuit breakers affect market maker inventory management and settlement risk
3.	Market maker exemptions: Bona fide market making exceptions under SHO and how to operationalize continuous quoting requirements
4.	Practical systems integration: How these regulations translate into C++/Python code for smart order routers, risk checks, and compliance monitoring
Interview Readiness Targets:
•	Explain trade-through protection and ISO mechanics on a whiteboard
•	Design a compliant market making quote engine with SHO locate/close-out logic
•	Analyze maker-taker fee structures and their impact on liquidity provision strategies
•	Debug routing failures involving protected quotes and locked/crossed markets
 
Part I: Regulation NMS – The Foundation of Order Routing and Quote Competition
1.1 What Problem Does Reg NMS Solve?
Before Reg NMS (pre-2005), U.S. equity markets were fragmented with inconsistent trade-through protection. Manual floor markets (NYSE specialists) coexisted with electronic venues, creating execution quality disparities and information asymmetries[1][2].
Core Objective: Create a unified national market system where investors receive best available prices regardless of venue, while preserving competition among trading centers[1][7].
Key Insight for Market Makers: Reg NMS defines the "playing field" for quote competition. Your quotes compete not just on your venue but across all lit exchanges. Understanding protected quotes and routing obligations is non-negotiable for building compliant liquidity provision systems[20][25].
 
1.2 Rule 611: Order Protection Rule (Trade-Through Protection)
1.2.1 Core Requirement
Rule 611 prohibits trading centers from executing trades at prices inferior to protected quotations displayed on other trading centers, except under enumerated exceptions[4][20].
Protected Quotation Definition[20][25]:
•	Must be automated (immediately executable without human intervention)
•	Must be displayed publicly at the National Best Bid or Offer (NBBO)
•	Must be disseminated via consolidated market data feeds (SIP)
•	Must be a quotation (not just an indication of interest)
What This Means for Market Makers: If you're providing liquidity on Venue A at $100.01 (protected bid), and Venue B tries to execute a sell at $100.00, Venue B violates Rule 611 unless an exception applies. Your quote has "priority" across the national market system[20].
1.2.2 Critical Exceptions: Intermarket Sweep Orders (ISOs)
ISO Definition: A limit order that, when routed to execute against protected quotations at better prices, simultaneously routes to all better-priced venues to satisfy their displayed size before executing at the destination venue[25][27].
Example ISO Workflow:
Current NBBO: $100.00 × $100.02 (bid × ask)
Protected quotes:
•	Venue A: 500 shares @ $100.01
•	Venue B: 300 shares @ $100.01
•	Venue C: 200 shares @ $100.01
Aggressive buy order: 2000 shares, limit $100.02
Smart router action:
1.	Send ISOs to Venues A, B, C to clear all $100.01 offers (1000 shares total)
2.	Simultaneously send remaining 1000 shares @ $100.02 to preferred venue
3.	All orders marked as ISO to claim Rule 611 exception
Why ISOs Matter for Market Makers[25]:
•	They allow aggressive participants to "sweep" your quotes without waiting for sequential routing
•	Your market making engine must handle sudden liquidity removal from ISO sweeps
•	ISO logic is central to smart order router (SOR) design in low-latency systems
Interview Question: "How would you detect if a venue is systematically ignoring protected quotes?"
Answer Framework: Monitor execution prices vs. NBBO timestamp-synchronized across venues; flag trades executing worse than protected quotes without ISO marking; calculate slippage distribution and test for statistical significance of trade-throughs.
1.2.3 Other Rule 611 Exceptions (Know These)
Beyond ISOs, Rule 611 provides eight other exceptions[25]:
1.	Benchmark/VWAP orders: Trades priced using algorithmic benchmarks
2.	Stopped orders: Where a trading center guarantees a price
3.	Flickering quotes: Protected quotes that were displayed <1 second ago
4.	Orders for which protection not required: Manual quotes, non-NMS securities
5.	Self-help exception: When a venue becomes inaccessible/non-operational
Market Maker Relevance: The "flickering quote" exception is critical. If your quote updates faster than SIP latency (~1-5ms typical), aggressive participants may trade through your stale SIP price legally. This drives direct feed adoption in market making[22].
 
1.3 Rule 610: Access Rule (Fair Access and Fee Caps)
1.3.1 Access Fee Caps
Rule 610 limits fees that trading centers can charge for accessing protected quotations to $0.003 per share (30 mils) for stocks ≥$1.00[1][2].
Why This Matters: Fee caps prevent venues from "hiding" execution costs in access charges. For market makers, this creates a level playing field where maker-taker rebates are constrained, affecting profitability calculations[28][38].
1.3.2 Fair and Non-Discriminatory Access
Trading centers must provide fair access to their quotes without unreasonable discrimination. No preferential treatment based on participant identity[1].
Market Maker Implication: You cannot be "locked out" of quoting on a venue if you meet objective membership criteria. But co-location fees, data feed fees, and port costs create effective barriers outside Rule 610's scope.
1.3.3 Locked and Crossed Markets
Rule 610 requires markets to establish rules preventing participants from displaying quotes that lock (bid = ask) or cross (bid > ask) protected quotations on other venues[30].
Example:
Protected NBBO: $100.00 × $100.01
Your market making system posts:
•	Bid: $100.01 → LOCKS the market (bid = best offer)
•	Offer: $99.99 → CROSSES the market (offer < best bid)
Both are prohibited under Rule 610
Low-Latency Challenge: Your quote engine must maintain sub-millisecond awareness of NBBO to avoid inadvertent locks/crosses, especially during fast market conditions. This requires direct feed consumption and lock/cross detection logic in pre-trade risk checks[30].
 
1.4 Rule 612: Sub-Penny Rule
1.4.1 Prohibition on Sub-Penny Quoting
For stocks priced ≥$1.00, trading centers cannot accept or rank orders in increments smaller than $0.01[1][2].
Allowed: $100.00, $100.01, $100.02
Prohibited: $100.001, $100.0099
For stocks <$1.00: Sub-penny increments are permitted (e.g., $0.9999, $0.9998).
1.4.2 Why This Rule Exists
Problem: Sub-penny "pennying" allowed high-frequency traders to jump queue by improving price by $0.0001, effectively front-running resting orders without meaningful price improvement[1].
Market Maker Perspective: Sub-penny protection preserves queue priority. If you post a $100.01 bid, competitors cannot undercut you with $100.0101. Your priority is protected for the full penny increment.
Edge Case: Sub-penny executions are allowed (e.g., midpoint matching at $100.005), but you cannot display sub-penny quotes. Your order management system must handle this distinction.
 
1.5 Market Data Rules (Rules 601-603)
Reg NMS updated rules governing consolidation and dissemination of quotes and trades[1][2]:
•	Rule 601: Dissemination of transaction reports and quotation information
•	Rule 602: Dissemination of quotations in NMS securities
•	Rule 603: Distribution and display of information with respect to quotations
Critical for Market Makers: These rules define the Securities Information Processor (SIP) feeds that distribute consolidated NBBO. The SIP is the "official" source for protected quotes under Rule 611, even though direct feeds are faster[20][22].
Latency Arbitrage: SIP latency (typically 300μs - 5ms slower than direct feeds) creates opportunities and risks:
•	Opportunity: Trading against stale SIP NBBO using direct feed data
•	Risk: Regulatory reliance on SIP for trade-through calculations means your direct feed advantage is legally constrained
System Design: Production market making systems maintain both direct feeds (for speed) and SIP feeds (for compliance validation).
 
1.6 NMS Impact on Market Making Strategy
1.6.1 Quote Competition Dynamics
Reg NMS transformed market making from venue-specific to cross-venue competition[23][26]:
Pre-NMS: NYSE specialists had informational/temporal advantages; could see order flow before executing
Post-NMS: All protected quotes compete equally; speed and price are primary differentiators
For Quant Devs: Your quote engine competes with every other market maker across all lit venues simultaneously. Latency to update quotes in response to NBBO changes is critical.
1.6.2 Maker-Taker Economics
Exchanges use maker-taker pricing to incentivize liquidity provision[28][38][41]:
Typical Structure:
•	Maker rebate: $0.0020/share (20 mils) – paid to you for posting resting orders
•	Taker fee: $0.0030/share (30 mils) – charged for removing liquidity
•	Exchange profit: $0.0010/share spread
Market Making P&L Formula:
P&L = (Spread Capture) + (Maker Rebates) - (Adverse Selection) - (Inventory Risk)
Example:
•	Post bid @ $100.00, ask @ $100.02 (2-cent spread)
•	Fill 10,000 shares on each side (neutral inventory)
•	Gross spread: 10,000 × $0.02 = $200
•	Maker rebates: 20,000 × $0.0020 = $40
•	Gross revenue: $240
Assume adverse selection costs $0.005/share:
•	Adverse selection: 20,000 × $0.005 = $100
•	Net P&L: $240 - $100 = $140
Strategy Insight: At tight spreads (1-2 cents), maker rebates can represent 20-30% of gross revenue. Venue selection and rebate optimization are first-order effects[28][41].
1.6.3 Dark Pool Considerations
Rule 611 does not require routing to dark pools (their quotes aren't protected). But your market making system must decide when to post liquidity in dark venues vs. lit exchanges[25].
Trade-off:
•	Lit venues: Maker rebates, but exposed to adverse selection from informed flow seeing your quotes
•	Dark pools: No rebates, but reduced information leakage and potential price improvement
 
Part II: Regulation SHO – Short Selling, Settlement, and Market Maker Exceptions
2.1 Why Short Selling Needs Regulation
Core Problem: "Naked" short selling (selling without arranging to borrow) can create failures to deliver (FTDs), where the seller cannot deliver shares by T+2 settlement. Persistent FTDs distort price discovery and settlement integrity[2][6].
Reg SHO Objective: Establish clear rules for short sale marking, locate, close-out, and a circuit breaker to prevent abusive short selling while preserving legitimate market making and hedging[2][6].
 
2.2 Rule 200: Marking Requirements
2.2.1 Order Marking Obligations
Every equity order must be marked as[2][6]:
•	Long: Seller owns the security and will deliver from existing holdings
•	Short: Seller does not own the security or will deliver from borrowed shares
•	Short Exempt: Short sale exempt from Rule 201 circuit breaker (discussed below)
Market Maker Compliance: Your order management system (OMS) must tag every sell order with the correct marking. This requires real-time inventory tracking to determine long/short status[2].
2.2.2 Common Marking Errors (Interview Red Flags)
1.	Failure to aggregate accounts: Marking long on Account A when short on Account B (same beneficial owner)
2.	Mislabeling hedges: Marking a short sale as "long" because it hedges an options position (still short unless you own underlying)
3.	Delayed inventory updates: Using stale position data resulting in incorrect marks
System Design Requirement: Atomic position updates synchronized with order marking logic. Race conditions between fills and position updates create regulatory risk.
 
2.3 Rule 203(b): Locate Requirement
2.3.1 Basic Locate Obligation
Before executing a short sale, a broker-dealer must:
1.	Borrow or arrange to borrow the security, OR
2.	Have reasonable grounds to believe the security can be borrowed and delivered by settlement[2][6]
The locate must be obtained and documented before the short sale[2].
2.3.2 What Constitutes "Reasonable Grounds"
Acceptable locate sources[2]:
•	Easy-to-borrow list: Securities generally available from lending desk
•	Specific borrow arrangement: Confirmation from securities lending desk
•	Reasonable grounds belief: Based on recent locate history for that security
Not Acceptable[2]:
•	Relying solely on prior-day locate for a new trading day
•	Assuming a large-cap stock is always available without verification
2.3.3 Bona Fide Market Maker Exception to Locate (CRITICAL)
Exemption: Market makers engaged in bona fide market making activities are exempt from the locate requirement[3][24][31][37][40].
Rationale: Market makers must provide continuous two-sided liquidity, often in fast-moving markets where obtaining a locate for every short sale would introduce unacceptable delays[1][31].
SEC Definition of Bona Fide Market Making[24][37][40][43]:
1.	Regularly and continuously quote on both bid and ask sides
2.	Quotes must be at or near the market (competitive pricing)
3.	Quotes must be widely available to investors and broker-dealers (not hidden/anonymous)
4.	Market making activity must be legitimate liquidity provision, not speculation
What Is NOT Bona Fide Market Making[24][37][43]:
•	Posting quotes only briefly or only on one side
•	"Speculative selling strategies" disguised as market making
•	Routinely executing shorts away from the market maker's quotes
•	Arrangements to use the exemption to facilitate another party's locate avoidance
2.3.4 FINRA Supervisory Expectations (Production System Requirements)
FINRA's examination reports emphasize firms must demonstrate compliance with bona fide market making requirements through[24][37][40]:
Monitoring and Controls:
•	Where quotes are placed: Lit exchanges vs. dark pools; visible vs. hidden orders
•	Frequency and timing of quoting: Continuous presence vs. sporadic quoting
•	Proprietary vs. customer flow: Ratio of prop trades to customer order facilitation
•	Quote competitiveness: Spread width, distance from NBBO, time at NBBO
Red Flags for Supervisory Systems[43]:
•	Quotes posted only briefly (e.g., milliseconds)
•	Quotes posted anonymously or non-competitively (far from market)
•	Quotes only on one side of the market
•	High ratio of proprietary directional trades vs. market making fills
Interview Question: "Design a real-time compliance system to validate bona fide market making status."
Answer Framework:
class BonafideMarketMakerMonitor:
def init(self, symbol: str):
self.symbol = symbol
self.bid_quote_time = 0.0
self.ask_quote_time = 0.0
self.total_bid_time = 0.0
self.total_ask_time = 0.0
self.prop_short_volume = 0
self.customer_facilitation_volume = 0
self.quote_updates = []
def on_quote_update(self, side: str, price: float, size: int, nbbo_bid: float, nbbo_ask: float, timestamp: float):
    """Track quoting continuity and competitiveness"""
    # Check quote competitiveness (within N cents of NBBO)
    if side == 'bid':
        competitive = (nbbo_bid - price) <= 0.03  # Within 3 cents
        if competitive:
            self.total_bid_time += (timestamp - self.bid_quote_time)
        self.bid_quote_time = timestamp
    elif side == 'ask':
        competitive = (price - nbbo_ask) <= 0.03
        if competitive:
            self.total_ask_time += (timestamp - self.ask_quote_time)
        self.ask_quote_time = timestamp
            
    self.quote_updates.append({
        'side': side, 'price': price, 'nbbo_bid': nbbo_bid, 
        'nbbo_ask': nbbo_ask, 'timestamp': timestamp
    })

def on_short_sale(self, is_customer_facilitation: bool, volume: int):
    """Track short sale activity classification"""
    if is_customer_facilitation:
        self.customer_facilitation_volume += volume
    else:
        self.prop_short_volume += volume

def validate_bonafide_status(self, current_time: float, trading_hours: float) -> tuple[bool, str]:
    """Validate continuous two-sided quoting and activity mix"""
    bid_uptime_pct = self.total_bid_time / trading_hours
    ask_uptime_pct = self.total_ask_time / trading_hours
    
    # Requirement: >80% uptime on both sides (example threshold)
    if bid_uptime_pct < 0.80:
        return False, f"Insufficient bid quoting: {bid_uptime_pct:.1%}"
    if ask_uptime_pct < 0.80:
        return False, f"Insufficient ask quoting: {ask_uptime_pct:.1%}"
    
    # Check proprietary vs customer ratio
    total_volume = self.prop_short_volume + self.customer_facilitation_volume
    if total_volume > 0:
        prop_ratio = self.prop_short_volume / total_volume
        if prop_ratio > 0.70:  # Example: >70% prop trades is suspicious
            return False, f"Excessive proprietary short volume: {prop_ratio:.1%}"
    
    return True, "Compliant bona fide market making"

Key Metrics to Track:
•	Bid/ask quote uptime percentage per symbol per day
•	Average spread vs. NBBO spread
•	Time-weighted presence at NBBO
•	Short volume classification (customer facilitation vs. proprietary speculation)
 
2.4 Rule 204: Close-Out Requirement
2.4.1 Settlement Timeline and FTD Triggers
Standard Settlement: T+2 (trade date + 2 business days)
Example:
Monday (T): Trade executed, short sale of 10,000 shares
Wednesday (T+2): Settlement date – must deliver shares to buyer
Thursday (T+3): If shares not delivered, FTD is recorded at NSCC
2.4.2 Close-Out Deadlines
If a fail-to-deliver occurs, Rule 204 requires[2][6]:
For clearing participants: Must close out the FTD by purchasing or borrowing securities no later than the beginning of regular trading hours on T+3 (settlement day + 1 business day)[2].
If close-out fails: The broker-dealer and any broker-dealer for which it clears cannot effect further short sales in that security without pre-borrowing (arranging borrow before order entry) until the FTD is closed out and the purchase/borrow settles[2][6].
2.4.3 Pre-Borrow Restriction (Penalty for Failed Close-Out)
Trigger: Failed to close out FTD by T+3 deadline
Penalty: Cannot execute any short sales in that security without pre-borrow until[2]:
1.	The fail is closed out (via purchase or borrow), AND
2.	The close-out transaction settles
Market Maker Exception Does NOT Apply: Even bona fide market makers are subject to pre-borrow restrictions if they fail to close out[2][24].
System Design Implication: Your risk system must maintain per-symbol FTD status and block short sales (or require pre-borrow flag) when close-out failures occur.
// C++ Pre-Borrow Check in Order Entry
struct SymbolSettlementState {
std::string symbol;
int64_t outstanding_ftd_shares;
bool pre_borrow_required;
std::chrono::system_clock::time_point close_out_deadline;
};
class Rule204Compliance {
private:
std::unordered_map<std::string, SymbolSettlementState> settlement_states_;
public:
bool validate_short_sale(const std::string& symbol, int64_t quantity, bool has_pre_borrow) {
auto it = settlement_states_.find(symbol);
if (it == settlement_states_.end()) {
return true; // No outstanding FTD
}
    if (it->second.pre_borrow_required && !has_pre_borrow) {
        // Block short sale - pre-borrow restriction active
        return false;
    }
    
    return true;
}

void on_ftd_reported(const std::string& symbol, int64_t ftd_shares, 
                     std::chrono::system_clock::time_point settlement_date) {
    auto& state = settlement_states_[symbol];
    state.symbol = symbol;
    state.outstanding_ftd_shares += ftd_shares;
    // T+3 close-out deadline
    state.close_out_deadline = settlement_date + std::chrono::hours(24);
}

void check_close_out_deadlines(std::chrono::system_clock::time_point current_time) {
    for (auto& [symbol, state] : settlement_states_) {
        if (state.outstanding_ftd_shares > 0 && current_time > state.close_out_deadline) {
            // Missed close-out deadline - activate pre-borrow requirement
            state.pre_borrow_required = true;
        }
    }
}

};
 
2.5 Rule 201: Alternative Uptick Rule (Short Sale Circuit Breaker)
2.5.1 Trigger Condition
Rule 201 activates when a stock experiences an intraday price decline of 10% or more from the previous day's closing price[2][6].
Example:
Previous Close: $100.00
Trigger Price: $90.00 (10% decline)
If stock trades at or below $90.00 during the day:
→ Rule 201 circuit breaker activates
2.5.2 Price Test Restriction
Once triggered, short sales can only be executed at a price above the current National Best Bid (NBB)[2][6].
Duration: Remainder of the day the decline occurred + the entire next trading day[2].
Example:
Circuit breaker triggered Tuesday at 10:30 AM
Current NBB: $89.50
Allowed short sale prices: ≥$89.51
Prohibited: $89.50 or lower
Restriction lasts:
•	Tuesday 10:30 AM - 4:00 PM
•	Wednesday 9:30 AM - 4:00 PM
2.5.3 Exceptions to Rule 201
Certain orders are marked "short exempt" and not subject to the price test[2]:
1.	Market maker quotes: Bona fide market making activity (subject to ongoing SEC/FINRA scrutiny)
2.	Certain arbitrage activities: Basket/index arbitrage, merger arbitrage, hedging related instruments
3.	Over-the-counter transactions: Trades not on an exchange
Market Maker Implication: Your quotes can provide liquidity on both sides even during circuit breaker, but you must mark properly as "short exempt" and maintain bona fide activity standards[24].
2.5.4 System Implementation
class Rule201CircuitBreaker:
def init(self, symbol: str, prior_close: float):
self.symbol = symbol
self.prior_close = prior_close
self.trigger_price = prior_close * 0.90
self.is_triggered = False
self.trigger_date = None
self.restriction_end_date = None
def on_trade(self, price: float, timestamp: datetime):
    """Check if circuit breaker should activate"""
    if not self.is_triggered and price <= self.trigger_price:
        self.is_triggered = True
        self.trigger_date = timestamp.date()
        # Restriction lasts through next trading day
        self.restriction_end_date = self.get_next_trading_day(self.trigger_date)
        
def validate_short_sale(self, price: float, current_nbb: float, 
                       current_date: date, is_short_exempt: bool) -> bool:
    """Validate short sale against price test"""
    if not self.is_triggered:
        return True  # No restriction active
        
    if current_date > self.restriction_end_date:
        return True  # Restriction expired
        
    if is_short_exempt:
        return True  # Market maker or other exemption
        
    # Price test: must be above NBB
    return price > current_nbb

@staticmethod
def get_next_trading_day(current_date: date) -> date:
    """Get next trading day (simplified - needs holiday calendar)"""
    next_day = current_date + timedelta(days=1)
    while next_day.weekday() >= 5:  # Skip weekends
        next_day += timedelta(days=1)
    return next_day

 
2.6 Threshold Securities
2.6.1 Definition and Identification
A security becomes a threshold security when aggregate FTDs meet both criteria[2][6]:
1.	≥10,000 shares, AND
2.	≥0.5% of total shares outstanding
These levels must persist for 5 consecutive settlement days[2].
2.6.2 Additional Close-Out Requirements
For threshold securities, if FTDs persist for 13 consecutive settlement days, Rule 203(b)(3) imposes an immediate close-out obligation (stricter than Rule 204's T+3)[2].
Market Maker Impact: Even with bona fide market making exemption, you face accelerated close-out deadlines for threshold securities. Your settlement monitoring must flag these automatically.
2.6.3 Public Disclosure
Threshold securities lists are published by exchanges (e.g., Nasdaq, NYSE) and updated regularly. Your risk system should ingest these lists daily.
Data Source: https://www.nasdaqtrader.com/trader.aspx?id=regshothreshold
 
Part III: Production System Design – Integrating NMS and SHO
3.1 Smart Order Router (SOR) Requirements
3.1.1 Core Routing Logic
Your SOR must satisfy Reg NMS Rule 611 (order protection) while optimizing for execution quality, fees, and latency.
High-Level SOR Algorithm:
1.	Receive order (buy/sell, quantity, limit price)
2.	Snapshot current NBBO and all protected quotes across venues
3.	For aggressive order (marketable):
a. If single venue has full size at NBBO → route there
b. If multiple venues at NBBO:
o	Optimize for: maker-taker fees, fill probability, latency
o	Consider historical fill rates, queue position estimates
c. If NBBO insufficient for full size:
o	Decide: ISO sweep vs. sequential routing vs. post-and-wait
4.	For passive order (non-marketable):
a. Select venue based on: rebates, queue position likelihood, adverse selection risk
b. Avoid locking/crossing protected quotes (Rule 610)
5.	Tag orders appropriately: ISO, short/long/short exempt, etc.
6.	Monitor fills and route remaining quantity if partial fill
3.1.2 ISO Sweep Logic (Detailed)
struct ProtectedQuote {
std::string venue;
double price;
int64_t size;
uint64_t timestamp_ns;
};
class ISORouter {
private:
std::vector<ProtectedQuote> get_protected_quotes_better_than(double limit_price, bool is_buy) {
std::vector<ProtectedQuote> better_quotes;
// Query all venues for protected quotes
for (auto& venue : venues_) {
auto quotes = venue.get_protected_quotes();
for (auto& quote : quotes) {
if (is_buy && quote.price <= limit_price) {
better_quotes.push_back(quote);
} else if (!is_buy && quote.price >= limit_price) {
better_quotes.push_back(quote);
}
}
}
// Sort by price priority (best first)
std::sort(better_quotes.begin(), better_quotes.end(),
[is_buy](const auto& a, const auto& b) {
return is_buy ? (a.price < b.price) : (a.price > b.price);
});
return better_quotes;
}
public:
void route_with_iso(Order& order) {
auto better_quotes = get_protected_quotes_better_than(order.limit_price, order.is_buy);
    std::vector<ChildOrder> child_orders;
    int64_t remaining_qty = order.quantity;
    
    // Sweep all better-priced protected quotes
    for (auto& quote : better_quotes) {
        if (remaining_qty <= 0) break;
        
        int64_t sweep_qty = std::min(remaining_qty, quote.size);
        ChildOrder iso_sweep;
        iso_sweep.venue = quote.venue;
        iso_sweep.price = quote.price;
        iso_sweep.quantity = sweep_qty;
        iso_sweep.is_iso = true;  // Mark as ISO
        iso_sweep.time_in_force = TimeInForce::IOC;
        
        child_orders.push_back(iso_sweep);
        remaining_qty -= sweep_qty;
    }
    
    // Send primary order to destination venue simultaneously
    ChildOrder primary_order;
    primary_order.venue = select_destination_venue(order);
    primary_order.price = order.limit_price;
    primary_order.quantity = remaining_qty;
    primary_order.is_iso = true;
    child_orders.push_back(primary_order);
    
    // Send all child orders simultaneously (critical for compliance)
    send_simultaneous_orders(child_orders);
}

};
Latency Constraint: ISOs must be sent simultaneously to comply with Rule 611. In practice, "simultaneous" means within microseconds. Use non-blocking I/O and parallel socket sends[25].
 
3.2 Market Making Quote Engine with SHO Compliance
3.2.1 High-Level Architecture
┌─────────────────────────────────────────────────────────┐
│ Market Data Feed Handler │
│ (Direct feeds + SIP, NBBO tracking, order book) │
└────────────────────┬────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│ Signal Generation Engine │
│ (Spread models, inventory targets, adverse selection) │
└────────────────────┬────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│ Quote Pricing Logic │
│ (Bid/ask calculation, size determination) │
└────────────────────┬────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│ Pre-Trade Risk & Compliance Checks │
│ • Rule 610: Lock/cross detection │
│ • Rule 200: Short sale marking (inventory check) │
│ • Rule 203(b): Bona fide market making validation │
│ • Rule 204: Pre-borrow check for FTD symbols │
│ • Rule 201: Circuit breaker price test │
│ • Position limits, capital checks │
└────────────────────┬────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│ Order Management System (OMS) │
│ (Order creation, venue routing, state tracking) │
└────────────────────┬────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────┐
│ FIX Gateway / Venue Connections │
│ (Exchange protocols, co-location, drop copy) │
└─────────────────────────────────────────────────────────┘
3.2.2 Continuous Two-Sided Quoting (Bona Fide Requirement)
class MarketMakingEngine {
private:
struct QuoteState {
double bid_price;
double ask_price;
int64_t bid_size;
int64_t ask_size;
uint64_t last_update_time_ns;
};
std::unordered_map<std::string, QuoteState> active_quotes_;
std::unordered_map<std::string, int64_t> inventory_;
Rule204Compliance rule204_checker_;
Rule201CircuitBreaker* circuit_breakers_;

// Parameters for bona fide market making
static constexpr double MAX_SPREAD_WIDTH = 0.05;  // 5 cents max
static constexpr int64_t MIN_QUOTE_SIZE = 100;
static constexpr uint64_t MAX_QUOTE_AGE_NS = 1'000'000'000;  // 1 second

public:
void update_quotes(const std::string& symbol, double nbbo_bid, double nbbo_ask) {
// Determine quote prices based on signal + inventory
auto [target_bid, target_ask] = calculate_quote_prices(symbol, nbbo_bid, nbbo_ask);
    // Pre-trade compliance checks
    if (!validate_quotes_compliance(symbol, target_bid, target_ask, nbbo_bid, nbbo_ask)) {
        // Log compliance violation and skip this update
        return;
    }
    
    // Determine sizes (skew based on inventory)
    auto [bid_size, ask_size] = calculate_quote_sizes(symbol, inventory_[symbol]);
    
    // Check short sale marking for ask side
    bool ask_is_short = (inventory_[symbol] < ask_size);
    
    if (ask_is_short) {
        // Check Rule 204 pre-borrow requirement
        if (!rule204_checker_.validate_short_sale(symbol, ask_size, false)) {
            // Cannot quote on ask side - pre-borrow restriction active
            ask_size = 0;
        }
        
        // Check Rule 201 circuit breaker
        auto* cb = get_circuit_breaker(symbol);
        if (cb && !cb->validate_short_sale(target_ask, nbbo_bid, 
                                           get_current_date(), true)) {
            // Adjust ask price above NBB if circuit breaker active
            target_ask = std::max(target_ask, nbbo_bid + 0.01);
        }
    }
    
    // Send quote updates to exchange
    send_quote_update(symbol, target_bid, target_ask, bid_size, ask_size);
    
    // Update state for bona fide tracking
    active_quotes_[symbol] = {target_bid, target_ask, bid_size, ask_size, 
                               current_time_ns()};
}

bool validate_quotes_compliance(const std::string& symbol, double bid, double ask,
                                 double nbbo_bid, double nbbo_ask) {
    // Rule 610: Prevent locking/crossing
    if (bid >= nbbo_ask) {
        // Would lock/cross the market
        return false;
    }
    if (ask <= nbbo_bid) {
        // Would cross on ask side
        return false;
    }
    
    // Bona fide requirement: quotes must be "at or near" the market
    double bid_distance = nbbo_bid - bid;
    double ask_distance = ask - nbbo_ask;
    
    if (bid_distance > MAX_SPREAD_WIDTH || ask_distance > MAX_SPREAD_WIDTH) {
        // Quotes too wide - may not qualify as bona fide
        return false;
    }
    
    // Size requirements
    if (bid_size < MIN_QUOTE_SIZE || ask_size < MIN_QUOTE_SIZE) {
        // Insufficient size
        return false;
    }
    
    return true;
}

std::pair<double, double> calculate_quote_prices(const std::string& symbol,
                                                  double nbbo_bid, double nbbo_ask) {
    // Simple example: quote at NBBO with inventory skew
    int64_t inv = inventory_[symbol];
    int64_t target_inv = 0;
    
    double bid_adjustment = 0.0;
    double ask_adjustment = 0.0;
    
    // Skew quotes to mean-revert inventory
    if (inv > target_inv + 1000) {
        // Long inventory - want to sell, make ask more aggressive
        ask_adjustment = -0.01;
        bid_adjustment = +0.01;
    } else if (inv < target_inv - 1000) {
        // Short inventory - want to buy
        bid_adjustment = -0.01;
        ask_adjustment = +0.01;
    }
    
    return {nbbo_bid + bid_adjustment, nbbo_ask + ask_adjustment};
}

};
 
3.3 Compliance Monitoring and Reporting
3.3.1 Daily Compliance Metrics
Your production system must generate end-of-day reports demonstrating regulatory compliance:
Reg NMS Metrics:
•	Trade-through incidents (executions worse than protected quotes without valid exception)
•	ISO usage percentage and sweep completion rate
•	Locked/crossed quote incidents and duration
•	NBBO participation rate (time spent at NBBO vs. away)
Reg SHO Metrics:
•	Short sale marking accuracy audit (sample fills vs. inventory)
•	Locate documentation completeness
•	FTD incidents, close-out timing, pre-borrow restriction activations
•	Bona fide market making uptime (two-sided quote presence %)
•	Rule 201 circuit breaker compliance (short sales during restriction)
3.3.2 Example Compliance Dashboard SQL Queries
-- Trade-through detection query
SELECT
trade_time,
symbol,
execution_price,
nbbo_bid,
nbbo_ask,
side,
CASE
WHEN side = 'BUY' AND execution_price > nbbo_ask THEN 'POTENTIAL_TRADE_THROUGH'
WHEN side = 'SELL' AND execution_price < nbbo_bid THEN 'POTENTIAL_TRADE_THROUGH'
ELSE 'OK'
END AS compliance_status
FROM executions e
JOIN nbbo_snapshots n ON e.symbol = n.symbol
AND n.snapshot_time = (SELECT MAX(snapshot_time)
FROM nbbo_snapshots
WHERE symbol = e.symbol AND snapshot_time <= e.trade_time)
WHERE execution_date = CURRENT_DATE
AND is_iso = FALSE
HAVING compliance_status = 'POTENTIAL_TRADE_THROUGH';
-- Bona fide market making validation query
SELECT
symbol,
SUM(CASE WHEN bid_size > 0 THEN 1 ELSE 0 END) / COUNT(
) AS bid_uptime_pct,SUM(CASE WHEN ask_size > 0 THEN 1 ELSE 0 END) / COUNT() AS ask_uptime_pct,
AVG(bid_price - nbbo_bid) AS avg_bid_distance,
AVG(ask_price - nbbo_ask) AS avg_ask_distance
FROM quote_snapshots
WHERE snapshot_date = CURRENT_DATE
GROUP BY symbol
HAVING bid_uptime_pct < 0.80 OR ask_uptime_pct < 0.80;
-- Rule 204 close-out monitoring
SELECT
symbol,
settlement_date,
ftd_shares,
close_out_deadline,
close_out_time,
CASE
WHEN close_out_time IS NULL AND CURRENT_TIMESTAMP > close_out_deadline
THEN 'MISSED_DEADLINE'
WHEN close_out_time > close_out_deadline THEN 'LATE_CLOSEOUT'
ELSE 'COMPLIANT'
END AS status
FROM fails_to_deliver
WHERE settlement_date >= CURRENT_DATE - INTERVAL '10 days';
 
Part IV: Interview Preparation – Key Questions and Frameworks
4.1 Whiteboard Question: Design a Compliant Market Making System
Question: "Walk me through the architecture of a low-latency market making system that complies with Reg NMS and Reg SHO. Focus on the critical compliance checkpoints."
Answer Framework:
1.	Market Data Layer:
o	Consume direct feeds (ITCH, PITCH) + SIP for compliance validation
o	Maintain order book depth and NBBO tracker
o	Latency: <10μs for direct feed processing
2.	Signal Generation:
o	Spread modeling (bid/ask targets)
o	Inventory risk management (position limits, skew)
o	Adverse selection detection
3.	Pre-Trade Risk Checks (CRITICAL):
For each quote update:
a. Lock/cross check against NBBO (Rule 610)
b. Short sale marking based on inventory (Rule 200)
c. Bona fide validation: competitive pricing, two-sided presence (Rule 203(b))
d. Pre-borrow check if FTD closeout failed (Rule 204)
e. Circuit breaker price test if Rule 201 triggered
f. Position limits, capital utilization
4.	Order Management:
o	FIX/binary protocol engines for exchange connectivity
o	Order state machines (new, partial fill, filled, canceled)
o	Fill handling and inventory updates
5.	Post-Trade Compliance:
o	Settlement monitoring (T+2 tracking)
o	FTD detection and close-out logic
o	Daily compliance reporting
6.	Monitoring/Surveillance:
o	Real-time alerting for compliance violations
o	Quote uptime metrics per symbol
o	Trade-through incident tracking
Bonus Points: Discuss specific latency optimizations (kernel bypass, FPGA parsing, lock-free data structures) while maintaining compliance correctness.
 
4.2 Case Study: Handling a Rule 201 Circuit Breaker Event
Scenario: You're market making in TSLA. At 11:30 AM, TSLA drops from $250.00 (prior close) to $224.50, triggering the Rule 201 circuit breaker. Current NBB is $224.50.
Questions:
1.	What happens to your existing quotes?
2.	What price can you quote on the ask side for the rest of the day?
3.	Does the restriction apply to your firm's customer order facilitation?
4.	When does the restriction expire?
Answers:
1.	Existing quotes: Your ask quote at $224.60 is now non-compliant (must be >$224.50, so ≥$224.51). Exchange will likely reject or cancel your quote. You must update immediately[2][6].
2.	Ask side pricing: You can only quote ≥$224.51 (above current NBB). As NBB moves, your minimum ask price updates dynamically[2].
3.	Customer facilitation: If you're facilitating a customer short sale order, the customer's order is subject to Rule 201 unless marked "short exempt" for a valid reason. Your firm's market making quotes can be marked "short exempt" if bona fide, but this doesn't automatically extend to customer orders[2][24].
4.	Expiration: End of day Wednesday + all of Thursday trading hours (assuming circuit breaker triggered Tuesday)[2].
System Response:
Detect circuit breaker activation
if price <= trigger_price:
circuit_breaker.activate()
Update quote logic
if circuit_breaker.is_active():
min_ask_price = current_nbb + 0.01 # Above NBB
ask_price = max(calculated_ask_price, min_ask_price)
Mark quotes as short exempt (if bona fide market maker)
if ask_requires_short_sell:
order_params['short_sale_type'] = 'SHORT_EXEMPT'
 
4.3 Scenario: Optimizing Routing with Maker-Taker Fees
Scenario: You need to fill a 5,000 share buy order in AAPL. Current NBBO is $180.00 × $180.01.
Protected quotes:
•	Nasdaq: 2,000 @ $180.01 (maker rebate: $0.0030/share, taker fee: $0.0030/share)
•	NYSE: 2,000 @ $180.01 (maker rebate: $0.0020/share, taker fee: $0.0030/share)
•	BATS: 1,500 @ $180.01 (maker rebate: $0.0025/share, taker fee: $0.0025/share)
Question: How do you route this order to minimize total cost?
Analysis:
Aggressive (take liquidity) costs:
•	Nasdaq: 2,000 × $0.0030 = $6.00
•	NYSE: 2,000 × $0.0030 = $6.00
•	BATS: 1,500 × $0.0025 = $3.75
•	Total taker fees: $15.75
But you could instead:
1.	Post passive order at $180.00 (join bid)
2.	Wait for fills (become the maker)
3.	Earn rebates instead of paying fees
If filled as maker at $180.00:
•	Save $0.01/share on price = $50.00
•	Earn $0.0025/share rebate (average) = $12.50
•	Total savings: $62.50
Trade-off: Execution certainty (immediate fill vs. risk of adverse selection if price moves to $180.02+)
Optimal Strategy (market making context):
•	Post at $180.00 for 3,000 shares (partial size)
•	If not filled within 100ms (parameterized), sweep at $180.01 with ISO
•	Balances rebate capture with execution certainty
This optimization is why maker-taker is central to market making P&L.
 
4.4 Debugging Question: Why Did My Locate Fail?
Scenario: Your market making system attempts a 10,000 share short sale in XYZ at 9:35 AM. The pre-trade check fails with error: "LOCATE_REQUIRED". But XYZ is on your easy-to-borrow list with 500,000 shares available.
What could cause this?
Debugging Checklist:
1.	Stale ETB list: Your easy-to-borrow list was generated at 8:00 AM. By 9:35 AM, availability changed. Check timestamp of last ETB refresh[2].
2.	Aggregate position check: You already have 490,000 shares short across multiple accounts. The locate system must check firm-wide short exposure, not just this order[2].
3.	Hard-to-borrow flag: XYZ was recently removed from ETB due to high borrow costs or limited supply. Your static list hasn't updated[2].
4.	Threshold security status: XYZ became a threshold security overnight. Your compliance system flagged it for enhanced scrutiny, requiring explicit locate for each short sale[2].
5.	Pre-borrow restriction: Previous FTD in XYZ with missed close-out deadline triggered Rule 204 pre-borrow requirement. Cannot short without explicit pre-borrow[2][6].
System Fix:
def validate_locate(symbol: str, quantity: int) -> tuple[bool, str]:
# Check 1: Pre-borrow restriction (Rule 204)
if is_pre_borrow_required(symbol):
if not has_explicit_borrow_arrangement(symbol, quantity):
return False, "PRE_BORROW_REQUIRED"
# Check 2: Bona fide market maker exemption
if is_bonafide_market_maker(symbol):
    return True, "BONAFIDE_EXEMPTION"

# Check 3: Threshold security - require explicit locate
if is_threshold_security(symbol):
    return validate_explicit_locate(symbol, quantity)

# Check 4: Easy-to-borrow with freshness check
etb_entry = get_etb_entry(symbol)
if etb_entry and etb_entry.available_shares >= quantity:
    if (current_time() - etb_entry.last_update_time) < 15*60:  # 15 min freshness
        return True, "ETB_LOCATE"

# Check 5: Firm-wide short exposure
total_short = get_firm_wide_short_position(symbol)
if total_short + quantity > get_locate_capacity(symbol):
    return False, "INSUFFICIENT_FIRM_CAPACITY"

# Fallback: require explicit locate
return validate_explicit_locate(symbol, quantity)

 
Part V: Advanced Topics and Current Developments
5.1 Rule 611 Reform Discussions (2024-2026)
Recent SEC roundtables have examined whether Rule 611 should be modified or repealed[22][30]:
Criticisms of Current Rule 611[22][23]:
•	Incentivizes "quote fading" (posting/canceling quotes rapidly to avoid fills)
•	Fragmentation increased (40+ execution venues vs. ~10 pre-NMS)
•	Displayed liquidity declined (more dark/hidden orders)
•	Complexity for retail investors to understand execution quality
Proposed Changes Under Discussion[22]:
•	Relaxing trade-through protection: Allow executions at midpoint or with price improvement without sweeping all protected quotes
•	Increasing tick sizes: Force wider spreads to encourage displayed liquidity
•	Modifying ISO requirements: Require actual routing vs. just marking orders as ISO
Impact on Market Making: Any Rule 611 changes would fundamentally alter competitive dynamics. Monitor SEC rulemaking closely.
 
5.2 Short Selling Disclosure Requirements
Recent proposals (2024-2025) suggest enhanced short position disclosure:
Potential Requirements:
•	Daily reporting of short positions above certain thresholds
•	Public disclosure of large short positions (similar to 13F for longs)
•	Real-time FTD data availability
Market Maker Implications: Increased transparency could reveal proprietary inventory management strategies. May require more sophisticated hedging to mask directional exposure.
 
5.3 Decimalization and Sub-Penny Pilot Programs
SEC has run pilot programs testing different tick sizes:
Tick Size Pilot (2016-2018): Tested $0.05 increments for small-cap stocks
Result: Wider spreads, reduced liquidity, mixed impact on price discovery[1]
Sub-Penny Access Fee Pilot (proposed): Test allowing sub-penny pricing in dark pools to compete with lit markets
Market Making Strategy: Different tick regimes require different spread models. Build parameterized systems that adapt to tick size changes.
 
Part VI: Study Plan and Resources
6.1 Core Reading (Must Complete)
1.	SEC Release 34-51808 – Regulation NMS Final Rule (2005): https://www.sec.gov/rules-regulations/2005/06/regulation-nms
2.	SEC Release 34-50103 – Regulation SHO Final Rule (2004): https://www.sec.gov/rules/final/34-50103.htm
3.	FINRA Regulatory Notices:
o	Notice 09-11: Bona Fide Market Making
o	Notice 20-15: Regulation SHO Compliance
4.	SEC Risk Alert: Regulation SHO and Compliance Issues (2013)
6.2 Practical Exercises
Exercise 1: Build a rule 611 validator
•	Input: Order (price, size, side), NBBO snapshot, protected quotes
•	Output: Compliant routing plan or ISO sweep orders
Exercise 2: Implement Rule 204 FTD tracking
•	Input: Daily trade/settlement data
•	Output: Close-out deadlines, pre-borrow restriction triggers
Exercise 3: Design bona fide market making monitor
•	Input: Quote update stream
•	Output: Uptime metrics, competitiveness scores, compliance alerts
Exercise 4: Optimize routing with maker-taker fees
•	Input: Order, venue quotes with fee structures
•	Output: Optimal routing decision with cost breakdown
6.3 Mock Interview Questions (Practice These)
1.	"Explain the difference between ISOs and directed orders. When would you use each?"
2.	"Design the pre-trade risk check module for a market making system. What validations are mandatory vs. optional?"
3.	"A stock drops 10% in 5 minutes. Walk through every regulatory impact on your system."
4.	"You receive a locate reject for a stock on your easy-to-borrow list. Debug this issue."
5.	"Your firm gets flagged for excessive trade-throughs. How do you investigate and remediate?"
6.	"Compare maker-taker vs. taker-maker pricing models. How do they affect market making strategy?"
7.	"Explain how NBBO calculation works with odd lot orders (< 100 shares). How does Reg NMS handle these?"
8.	"Design a settlement monitoring system that alerts on potential Rule 204 violations before they occur."
6.4 Systems Design Follow-Up Topics
After mastering NMS/SHO, expand to:
1.	FIX Protocol: Deep dive into FIX 4.2/4.4, order types (35=D/F/G), execution reports (35=8)
2.	Market Data Protocols: ITCH (Nasdaq), PITCH (BATS), FAST (CME), Pillar (NYSE)
3.	Co-location and Latency: Network topology, switch latency, kernel bypass (DPDK), FPGA parsing
4.	Order Book Modeling: Price-time priority, hidden orders, iceberg orders, pro-rata vs. FIFO
5.	Adverse Selection Models: PIN model, VPIN, order flow toxicity, informed trader detection
6.	Inventory Risk Management: Skew functions, hedging with ETFs/futures, overnight risk
 
Appendix A: Regulatory Citation Index
RuleCitationTopicReg NMS Rule 61117 CFR § 242.611Order Protection Rule (Trade-Through)Reg NMS Rule 61017 CFR § 242.610Access Rule (Fees, Locked/Crossed Markets)Reg NMS Rule 61217 CFR § 242.612Sub-Penny RuleReg NMS Rules 601-60317 CFR § 242.601-603Market Data RulesReg SHO Rule 20017 CFR § 242.200Marking Requirements (Long/Short/Short Exempt)Reg SHO Rule 20117 CFR § 242.201Circuit Breaker (Alternative Uptick Rule)Reg SHO Rule 203(b)17 CFR § 242.203(b)Locate Requirement + Bona Fide Market Maker ExceptionReg SHO Rule 20417 CFR § 242.204Close-Out Requirement (T+3, Pre-Borrow Restriction)
 
Appendix B: Glossary of Terms
NBBO: National Best Bid and Offer – highest bid and lowest ask across all protected quotes
Protected Quotation: Automated, displayed, immediately executable quote disseminated via SIP
ISO: Intermarket Sweep Order – order type that sweeps protected quotes at better prices
FTD: Fail to Deliver – when seller cannot deliver shares by T+2 settlement
Threshold Security: Stock with persistent FTDs (≥10,000 shares and ≥0.5% of float for 5 days)
Bona Fide Market Making: Continuous, competitive, two-sided quoting for legitimate liquidity provision
Maker-Taker: Fee structure where makers receive rebates and takers pay fees
SIP: Securities Information Processor – consolidates quotes/trades across exchanges
Locate: Confirmation that shares can be borrowed for short sale (required under Rule 203(b))
Pre-Borrow: Requirement to arrange borrow before order entry (penalty for failed close-out)
 
Summary: Key Takeaways for Market Making Quant Developers
1.	Reg NMS shapes routing: Rule 611 (order protection), Rule 610 (access/fees), Rule 612 (sub-penny), market data rules define the competitive landscape for cross-venue liquidity provision.
2.	ISOs are central: Understanding intermarket sweep orders is mandatory for smart order router design and compliance with protected quote obligations.
3.	Reg SHO governs settlement: Marking (Rule 200), locate (Rule 203), close-out (Rule 204), circuit breaker (Rule 201) create operational requirements for short selling and inventory management.
4.	Bona fide market making exemption is powerful but scrutinized: Continuous two-sided competitive quoting is required to claim locate exemption. FINRA actively monitors for abuse.
5.	Compliance is not optional: Pre-trade risk checks must validate Rule 610 (lock/cross), Rule 200 (marking), Rule 203 (locate/bona fide), Rule 204 (pre-borrow), Rule 201 (circuit breaker) on every order.
6.	Maker-taker economics matter: Rebates can represent 20-30% of gross revenue at tight spreads. Venue selection and fee optimization are first-order strategy considerations.
7.	Latency + compliance must coexist: Low-latency systems (μs-level) must maintain regulatory correctness. Design with compliance checks in the critical path, optimized for speed.
8.	Monitor regulatory changes: Rule 611 reform, short selling disclosure, tick size pilots are active areas of rulemaking that could reshape market structure.
You are now prepared to discuss Reg NMS and Reg SHO fluently in market making quantitative developer interviews, design compliant production systems, and understand the regulatory constraints that shape modern equity market microstructure.
 
References
[1] U.S. Securities and Exchange Commission. (2005). Regulation NMS. https://www.sec.gov/rules-regulations/2005/06/regulation-nms
[2] U.S. Securities and Exchange Commission. (2005). Key Points About Regulation SHO. https://www.sec.gov/investor/pubs/regsho.htm
[3] FINRA. (2023). Regulation SHO – Bona Fide Market Making Exemptions and Reuse. https://www.finra.org/rules-guidance/guidance/reports/2023-finras-examination-and-risk-monitoring-program/regulation-sho
[4] Cornell Law School. (2024). 17 CFR § 242.611 - Order protection rule. https://www.law.cornell.edu/cfr/text/17/242.611
[6] Investopedia. (2022). Regulation SHO Explained: Short Sale Rules and Key Requirements. https://www.investopedia.com/terms/r/regsho.asp
[7] U.S. Securities and Exchange Commission. (2005). Regulation NMS Final Rule Release 34-51808.
[20] SIFMA. (2025). Rethinking Trade-Through Prohibitions: Beware of the Market Structure Octopus. https://www.sifma.org/news/blog/rethinking-trade-through-prohibitions-beware-of-the-market-structure-octopus
[22] U.S. Securities and Exchange Commission. (2025). Statement at the Roundtable on Rule 611 of Regulation NMS. https://www.sec.gov/newsroom/speeches-statements/uyeda-roundtable-rule-611-regulation-nms-121625
[23] ACSU Buffalo. (2024). Regulation NMS and Market Quality. https://www.acsu.buffalo.edu/~keechung/MGF743/Lecture Notes/Regulation NMS and Market Quality PowerPoint.pptx
[24] FINRA. (2024). Regulation SHO – Bona Fide Market Making Exemptions. https://www.finra.org/rules-guidance/guidance/reports/2024-finra-annual-regulatory-oversight-report/regulation-sho
[25] U.S. Securities and Exchange Commission. (2015). Rule 611 of Regulation NMS - memo to SEC Market Structure Advisory Committee. https://www.sec.gov/spotlight/emsac/memo-rule-611-regulation-nms.pdf
[28] CFA Institute. (2017). Regulation NMS - Review and Recommendations. https://rpc.cfainstitute.org/sites/default/files/-/media/documents/article/position-paper/regulation-nms-review-recommendations.ashx
[30] FlexTrade. (2025). The Order Protection Rule: Is an Equity Market Structure Shake-Up Ahead? https://flextrade.com/resources/the-order-protection-rule-is-an-equity-market-structure-shake-up-ahead/
[31] Mercatus Center. (2012). The Options Market Maker Exception to SEC Regulation SHO. https://www.mercatus.org/research/working-papers/options-market-maker-exception-sec-regulation-sho
[37] Bracewell LLP. (2024). FINRA Facts and Trends: January 2024. https://www.bracewell.com/resources/finra-facts-and-trends-january-2024/
[38] Investopedia. (2023). Understanding Maker-Taker Fees: Impact on Traders and Market. https://www.investopedia.com/articles/active-trading/042414/what-makertaker-fees-mean-you.asp
[40] FINRA. (2025). Regulation SHO – Bona Fide Market Making and Close-Out Requirements. https://www.finra.org/rules-guidance/guidance/reports/2025-finra-annual-regulatory-oversight-report/regulation-sho
[41] QuestDB. (2023). Maker-Taker Model. https://questdb.com/glossary/maker-taker-model/
[43] CSG Law. (2024). Regulation SHO | NSCP Currents On Demand. https://www.csglaw.com/wp-content/uploads/2024/05/Regulation-SHO-NSCP-Currents-On-Demand-2024-Kelly.pdf
