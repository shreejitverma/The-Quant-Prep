// Price-time priority limit order book and matching engine for 07-Order-Book-and-Matching-Engine.md.
//
// Data structures
//   - Orders live in a preallocated pool (std::vector<OrderNode>) addressed by 32-bit index, with a
//     free list: the pool itself never allocates after construction.
//   - Each price level is a FIFO, an intrusive doubly linked list threaded through the pool by index
//     (prev/next), so cancel of any order is O(1) once it is found.
//   - Levels are kept in one std::map<Price, Level, PriceOrder> per side, ordered so that begin() is
//     the best price on both sides (descending bids, ascending asks). O(log L) to create a level,
//     amortised O(1) to erase one through a stored iterator, O(1) to reach the best one.
//     (Do not key bids ascending and read std::prev(end()): libc++ caches only the leftmost node, so
//     that is O(log L) there; libstdc++ also caches the rightmost. Production engines often replace
//     the map by an array indexed by tick; lob_bench.cpp measures both.)
//   - OrderId -> pool index in a std::unordered_map reserved for the pool capacity. reserve() only
//     presizes the bucket array: every insert still allocates a node, and each new price level
//     allocates a map node. Production engines remove both (open-addressing id table or a dense id
//     array, preallocated level arrays).
//
// Exception policy: the only operations that can throw are those allocations and the caller's event
// vector growing. A half-applied command leaves no consistent book to recover, so the commands are
// noexcept and std::bad_alloc terminates the process rather than corrupting state.
//
// Supported: limit and market orders; Day (rest), IOC and FOK time in force; post-only;
// self-trade prevention (cancel resting, cancel aggressor, cancel both); cancel; cancel/replace
// (a quantity decrease at the same price keeps priority, anything else loses it; the quantity is
// the new open quantity, not FIX OrderQty, which counts the already-executed part); and a
// single-price call auction (pre-open phase, then uncross).
//
// Events are appended to a caller-owned vector so the engine itself does no I/O.

#pragma once

#include <algorithm>
#include <cstddef>
#include <cstdint>
#include <map>
#include <optional>
#include <stdexcept>
#include <unordered_map>
#include <vector>

namespace lob {

using Price = std::int64_t;  // integer ticks
using Qty = std::int64_t;
using OrderId = std::uint64_t;
using TraderId = std::uint32_t;

enum class Side : std::uint8_t { Buy, Sell };
enum class OrdType : std::uint8_t { Limit, Market };
enum class Tif : std::uint8_t { Day, Ioc, Fok };
enum class Stp : std::uint8_t { None, CancelResting, CancelAggressor, CancelBoth };
enum class Phase : std::uint8_t { PreOpen, Continuous };

struct NewOrder {
    OrderId id = 0;
    TraderId trader = 0;
    Side side = Side::Buy;
    OrdType type = OrdType::Limit;
    Tif tif = Tif::Day;
    Price price = 0;  // ignored for market orders
    Qty qty = 0;
    bool post_only = false;
    Stp stp = Stp::None;
};

enum class EventType : std::uint8_t { Accepted, Rejected, Fill, Cancelled, Replaced };
enum class Reason : std::uint8_t {
    None,
    DuplicateId,
    BadQuantity,
    BadPrice,
    UnknownOrder,
    PostOnlyWouldCross,
    FokNotFillable,
    IocRemainder,
    SelfTrade,
    UserCancel,
    BookFull,
    NotAllowedInPhase,
};

struct Event {
    EventType type;
    OrderId id;          // the order this event is about (the aggressor for a fill)
    OrderId counter_id;  // fill: resting order; replace: the old id
    Price price;
    Qty qty;
    Reason reason;
    friend bool operator==(const Event&, const Event&) = default;
};

struct AuctionResult {
    Price price = 0;
    Qty volume = 0;
    Qty imbalance = 0;  // buy volume minus sell volume at the clearing price
};

class OrderBook {
    static constexpr std::uint32_t kNil = 0xFFFF'FFFFu;

    struct Level {
        std::uint32_t head = kNil;
        std::uint32_t tail = kNil;
        Qty total = 0;
        std::uint32_t count = 0;
    };
    // One comparator type for both sides keeps a single LevelMap (and iterator) type while making
    // begin() the best level on each side.
    struct PriceOrder {
        bool descending = false;
        bool operator()(Price a, Price b) const noexcept { return descending ? b < a : a < b; }
    };
    using LevelMap = std::map<Price, Level, PriceOrder>;

    struct OrderNode {
        OrderId id = 0;
        TraderId trader = 0;
        Price price = 0;
        Qty qty = 0;
        Side side = Side::Buy;
        Stp stp = Stp::None;
        bool post_only = false;
        std::uint32_t prev = kNil;
        std::uint32_t next = kNil;
        LevelMap::iterator level{};
    };

    std::vector<OrderNode> nodes_;
    std::vector<std::uint32_t> free_;
    std::unordered_map<OrderId, std::uint32_t> index_;
    LevelMap bids_{PriceOrder{true}};  // best (highest) bid first
    LevelMap asks_{PriceOrder{false}};  // best (lowest) ask first
    Phase phase_ = Phase::Continuous;

public:
    explicit OrderBook(std::size_t max_orders, Phase phase = Phase::Continuous) : phase_(phase) {
        if (max_orders >= kNil) throw std::length_error("OrderBook: pool indices are 32-bit");
        nodes_.resize(max_orders);
        free_.reserve(max_orders);
        for (std::size_t i = max_orders; i-- > 0;) free_.push_back(static_cast<std::uint32_t>(i));
        index_.reserve(max_orders);
    }

    // ------------------------------------------------------------------ queries
    [[nodiscard]] std::optional<Price> best_bid() const {
        if (bids_.empty()) return std::nullopt;
        return bids_.begin()->first;
    }
    [[nodiscard]] std::optional<Price> best_ask() const {
        if (asks_.empty()) return std::nullopt;
        return asks_.begin()->first;
    }
    [[nodiscard]] Qty depth_at(Side s, Price p) const {
        const LevelMap& m = s == Side::Buy ? bids_ : asks_;
        const auto it = m.find(p);
        return it == m.end() ? 0 : it->second.total;
    }
    [[nodiscard]] std::size_t level_count(Side s) const { return s == Side::Buy ? bids_.size() : asks_.size(); }
    [[nodiscard]] std::size_t order_count() const { return index_.size(); }
    [[nodiscard]] Phase phase() const { return phase_; }
    // FIFO order of the resting order ids at one level (for tests and debugging).
    [[nodiscard]] std::vector<OrderId> queue_at(Side s, Price p) const {
        std::vector<OrderId> out;
        const LevelMap& m = s == Side::Buy ? bids_ : asks_;
        const auto it = m.find(p);
        if (it == m.end()) return out;
        for (std::uint32_t i = it->second.head; i != kNil; i = nodes_[i].next) out.push_back(nodes_[i].id);
        return out;
    }
    [[nodiscard]] std::optional<Qty> open_qty(OrderId id) const {
        const auto it = index_.find(id);
        if (it == index_.end()) return std::nullopt;
        return nodes_[it->second].qty;
    }

    // ------------------------------------------------------------------ commands (HOT PATH)
    void submit(const NewOrder& o, std::vector<Event>& out) noexcept {
        if (o.qty <= 0) return reject(o.id, Reason::BadQuantity, out);
        if (o.type == OrdType::Limit && o.price <= 0) return reject(o.id, Reason::BadPrice, out);
        if (o.type == OrdType::Market && o.post_only) return reject(o.id, Reason::BadPrice, out);
        if (index_.contains(o.id)) return reject(o.id, Reason::DuplicateId, out);
        if (phase_ == Phase::PreOpen) {
            if (o.type != OrdType::Limit || o.tif != Tif::Day || o.post_only) return reject(o.id, Reason::NotAllowedInPhase, out);
            if (free_.empty()) return reject(o.id, Reason::BookFull, out);
            out.push_back({EventType::Accepted, o.id, 0, o.price, o.qty, Reason::None});
            rest(o, o.qty);  // no matching before the uncross
            return;
        }
        if (o.post_only && would_cross(o)) return reject(o.id, Reason::PostOnlyWouldCross, out);
        const bool will_rest = o.type == OrdType::Limit && o.tif == Tif::Day;
        if (will_rest && free_.empty()) return reject(o.id, Reason::BookFull, out);
        out.push_back({EventType::Accepted, o.id, 0, o.price, o.qty, Reason::None});
        if (o.tif == Tif::Fok && fillable_qty(o) < o.qty) {
            out.push_back({EventType::Cancelled, o.id, 0, o.price, o.qty, Reason::FokNotFillable});
            return;
        }
        Qty remaining = o.qty;
        const bool aggressor_alive = match(o, remaining, out);
        if (!aggressor_alive || remaining == 0) return;
        if (will_rest) {
            rest(o, remaining);
        } else {
            out.push_back({EventType::Cancelled, o.id, 0, o.price, remaining, Reason::IocRemainder});
        }
    }

    void cancel(OrderId id, std::vector<Event>& out) noexcept {
        const auto it = index_.find(id);
        if (it == index_.end()) return reject(id, Reason::UnknownOrder, out);
        const std::uint32_t i = it->second;
        out.push_back({EventType::Cancelled, id, 0, nodes_[i].price, nodes_[i].qty, Reason::UserCancel});
        remove_resting(i);
    }

    // Cancel/replace. Same price and a quantity no larger than the open quantity: amend in place and
    // keep queue position. Otherwise: cancel and re-enter as a new Day limit order (loses priority,
    // and may trade immediately if the new price crosses). A post-only order stays post-only: a
    // replace that would cross is rejected and the original order is left untouched.
    void replace(OrderId old_id, OrderId new_id, Price new_price, Qty new_qty, std::vector<Event>& out) noexcept {
        const auto it = index_.find(old_id);
        if (it == index_.end()) return reject(new_id, Reason::UnknownOrder, out);
        if (new_qty <= 0) return reject(new_id, Reason::BadQuantity, out);
        if (new_price <= 0) return reject(new_id, Reason::BadPrice, out);
        if (new_id != old_id && index_.contains(new_id)) return reject(new_id, Reason::DuplicateId, out);
        const std::uint32_t i = it->second;
        OrderNode& n = nodes_[i];
        if (new_price == n.price && new_qty <= n.qty) {
            n.level->second.total -= n.qty - new_qty;
            n.qty = new_qty;
            if (new_id != old_id) {
                index_.erase(it);
                index_.emplace(new_id, i);
                n.id = new_id;
            }
            out.push_back({EventType::Replaced, new_id, old_id, new_price, new_qty, Reason::None});
            return;
        }
        const NewOrder fresh{new_id, n.trader, n.side, OrdType::Limit, Tif::Day, new_price, new_qty, n.post_only, n.stp};
        if (fresh.post_only && would_cross(fresh)) return reject(new_id, Reason::PostOnlyWouldCross, out);
        remove_resting(i);
        out.push_back({EventType::Replaced, new_id, old_id, new_price, new_qty, Reason::None});
        submit(fresh, out);
    }

    // ------------------------------------------------------------------ call auction
    // Clearing price: maximise executable volume; then minimise |imbalance|; then closest to the
    // reference price; then the lower price. (A common rule set; each venue publishes its own.)
    [[nodiscard]] std::optional<AuctionResult> indicative_auction(Price reference) const {
        std::vector<Price> candidates;
        for (const auto& [p, l] : bids_) candidates.push_back(p);
        for (const auto& [p, l] : asks_) candidates.push_back(p);
        std::sort(candidates.begin(), candidates.end());
        candidates.erase(std::unique(candidates.begin(), candidates.end()), candidates.end());
        std::optional<AuctionResult> best;
        for (Price p : candidates) {
            Qty buy = 0;
            Qty sell = 0;
            for (auto it = bids_.begin(); it != bids_.end() && it->first >= p; ++it) buy += it->second.total;
            for (auto it = asks_.begin(); it != asks_.end() && it->first <= p; ++it) sell += it->second.total;
            const AuctionResult r{p, std::min(buy, sell), buy - sell};
            if (r.volume == 0) continue;
            if (!best || better_auction(r, *best, reference)) best = r;
        }
        return best;
    }

    // Executes the auction at a single price, then switches to continuous trading.
    std::optional<AuctionResult> uncross(Price reference, std::vector<Event>& out) noexcept {
        const auto result = indicative_auction(reference);
        phase_ = Phase::Continuous;
        if (!result) return result;
        const Price p = result->price;
        while (!bids_.empty() && !asks_.empty()) {
            auto bit = bids_.begin();
            auto ait = asks_.begin();
            if (bit->first < p || ait->first > p) break;
            const std::uint32_t b = bit->second.head;
            const std::uint32_t a = ait->second.head;
            const Qty q = std::min(nodes_[b].qty, nodes_[a].qty);
            // In an auction neither side is the aggressor; report the buy order as id and the sell as counter.
            out.push_back({EventType::Fill, nodes_[b].id, nodes_[a].id, p, q, Reason::None});
            reduce(b, q);
            reduce(a, q);
        }
        return result;
    }

private:
    static bool better_auction(const AuctionResult& a, const AuctionResult& b, Price ref) {
        if (a.volume != b.volume) return a.volume > b.volume;
        const Qty ia = a.imbalance < 0 ? -a.imbalance : a.imbalance;
        const Qty ib = b.imbalance < 0 ? -b.imbalance : b.imbalance;
        if (ia != ib) return ia < ib;
        const Price da = a.price > ref ? a.price - ref : ref - a.price;
        const Price db = b.price > ref ? b.price - ref : ref - b.price;
        if (da != db) return da < db;
        return a.price < b.price;
    }

    static void reject(OrderId id, Reason r, std::vector<Event>& out) { out.push_back({EventType::Rejected, id, 0, 0, 0, r}); }

    bool crosses(const NewOrder& o, Price level_px) const {
        if (o.type == OrdType::Market) return true;
        return o.side == Side::Buy ? level_px <= o.price : level_px >= o.price;
    }

    bool would_cross(const NewOrder& o) const {
        const LevelMap& opp = o.side == Side::Buy ? asks_ : bids_;
        if (opp.empty()) return false;
        return crosses(o, opp.begin()->first);
    }

    // Exactly the quantity match() would fill, walking in priority order and applying STP.
    Qty fillable_qty(const NewOrder& o) const {
        const LevelMap& opp = o.side == Side::Buy ? asks_ : bids_;
        Qty avail = 0;
        auto visit_level = [&](const Level& l) {
            for (std::uint32_t i = l.head; i != kNil; i = nodes_[i].next) {
                const OrderNode& n = nodes_[i];
                if (o.stp != Stp::None && n.trader == o.trader) {
                    if (o.stp == Stp::CancelResting) continue;
                    return false;  // aggressor would be cancelled here
                }
                avail += n.qty;
                if (avail >= o.qty) return false;
            }
            return true;
        };
        for (auto it = opp.begin(); it != opp.end() && crosses(o, it->first); ++it)
            if (!visit_level(it->second)) break;
        return avail;
    }

    // Walks the opposite side in price-time priority. Returns false if STP cancelled the aggressor.
    bool match(const NewOrder& o, Qty& remaining, std::vector<Event>& out) {
        LevelMap& opp = o.side == Side::Buy ? asks_ : bids_;
        while (remaining > 0 && !opp.empty()) {
            const auto lit = opp.begin();
            if (!crosses(o, lit->first)) break;
            const Price px = lit->first;
            std::uint32_t cur = lit->second.head;
            bool aggressor_alive = true;
            while (cur != kNil && remaining > 0) {
                OrderNode& maker = nodes_[cur];
                const std::uint32_t next = maker.next;
                if (o.stp != Stp::None && maker.trader == o.trader) {
                    if (o.stp == Stp::CancelResting || o.stp == Stp::CancelBoth) {
                        out.push_back({EventType::Cancelled, maker.id, o.id, px, maker.qty, Reason::SelfTrade});
                        unlink_and_free(cur);
                    }
                    if (o.stp == Stp::CancelAggressor || o.stp == Stp::CancelBoth) {
                        out.push_back({EventType::Cancelled, o.id, 0, o.price, remaining, Reason::SelfTrade});
                        remaining = 0;
                        aggressor_alive = false;
                        break;
                    }
                    cur = next;
                    continue;
                }
                const Qty q = std::min(remaining, maker.qty);
                out.push_back({EventType::Fill, o.id, maker.id, px, q, Reason::None});
                remaining -= q;
                maker.qty -= q;
                lit->second.total -= q;
                if (maker.qty == 0) unlink_and_free(cur);
                cur = next;
            }
            if (lit->second.count == 0) opp.erase(lit);
            if (!aggressor_alive) return false;
        }
        return true;
    }

    void rest(const NewOrder& o, Qty qty) {
        const std::uint32_t i = free_.back();
        free_.pop_back();
        LevelMap& side = o.side == Side::Buy ? bids_ : asks_;
        const auto lit = side.try_emplace(o.price).first;
        Level& l = lit->second;
        nodes_[i] = OrderNode{o.id, o.trader, o.price, qty, o.side, o.stp, o.post_only, l.tail, kNil, lit};
        if (l.tail != kNil)
            nodes_[l.tail].next = i;
        else
            l.head = i;
        l.tail = i;
        l.total += qty;
        ++l.count;
        index_.emplace(o.id, i);
    }

    // Removes node i from its level FIFO and returns it to the pool; the caller erases an empty level.
    void unlink_and_free(std::uint32_t i) {
        OrderNode& n = nodes_[i];
        Level& l = n.level->second;
        if (n.prev != kNil)
            nodes_[n.prev].next = n.next;
        else
            l.head = n.next;
        if (n.next != kNil)
            nodes_[n.next].prev = n.prev;
        else
            l.tail = n.prev;
        l.total -= n.qty;
        --l.count;
        index_.erase(n.id);
        free_.push_back(i);
    }

    void remove_resting(std::uint32_t i) {
        const auto lit = nodes_[i].level;
        LevelMap& side = nodes_[i].side == Side::Buy ? bids_ : asks_;
        unlink_and_free(i);
        if (lit->second.count == 0) side.erase(lit);
    }

    void reduce(std::uint32_t i, Qty q) {
        nodes_[i].qty -= q;
        nodes_[i].level->second.total -= q;
        if (nodes_[i].qty == 0) remove_resting(i);
    }
};

}  // namespace lob
