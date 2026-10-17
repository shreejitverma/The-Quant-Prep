// Tests for lob_engine.hpp and lob_itch_book.hpp (07-Order-Book-and-Matching-Engine.md).
// Edge cases, plus a randomized differential test against a deliberately naive reference
// matcher (linear scans, obviously correct) over 20,000 seeded adds, cancels, cancel/replaces,
// IOC, FOK and market orders. Framework-free.

#include "lob_engine.hpp"
#include "lob_itch_book.hpp"

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

namespace {

int g_failures = 0;
int g_total = 0;

#define EXPECT(cond)                                                                            \
    do {                                                                                        \
        ++g_total;                                                                              \
        if (!(cond)) {                                                                          \
            ++g_failures;                                                                       \
            std::cerr << "  FAIL: " << __FILE__ << ":" << __LINE__ << " -> " #cond << std::endl; \
        }                                                                                       \
    } while (0)

using namespace lob;

NewOrder limit(OrderId id, Side s, Price px, Qty q, TraderId t = 1) { return NewOrder{id, t, s, OrdType::Limit, Tif::Day, px, q}; }

void test_validation() {
    OrderBook b(4);
    std::vector<Event> ev;
    b.submit(limit(1, Side::Buy, 100, 0), ev);
    EXPECT(ev.back().reason == Reason::BadQuantity);
    b.submit(limit(1, Side::Buy, 0, 10), ev);
    EXPECT(ev.back().reason == Reason::BadPrice);
    b.submit(limit(1, Side::Buy, 100, 10), ev);
    b.submit(limit(1, Side::Buy, 101, 10), ev);
    EXPECT(ev.back().reason == Reason::DuplicateId);
    b.cancel(99, ev);
    EXPECT(ev.back().type == EventType::Rejected && ev.back().reason == Reason::UnknownOrder);
    for (OrderId id = 2; id <= 4; ++id) b.submit(limit(id, Side::Buy, 100, 1), ev);
    b.submit(limit(5, Side::Buy, 100, 1), ev);
    EXPECT(ev.back().reason == Reason::BookFull);  // pool of 4 exhausted: rejected, not reallocated
    b.cancel(2, ev);
    b.submit(limit(5, Side::Buy, 100, 1), ev);
    EXPECT(ev.back().type == EventType::Accepted);  // slot recycled
}

// Quantities above one billion are rejected on entry and on replace, so level totals cannot overflow.
void test_quantity_upper_bound() {
    OrderBook b(4);
    std::vector<Event> ev;
    constexpr Qty kHuge = INT64_MAX;
    b.submit(limit(1, Side::Buy, 100, kHuge), ev);
    EXPECT(ev.back().type == EventType::Rejected && ev.back().reason == Reason::BadQuantity);
    b.submit(limit(2, Side::Buy, 100, 1'000'000'001), ev);
    EXPECT(ev.back().type == EventType::Rejected && ev.back().reason == Reason::BadQuantity);
    b.submit(limit(3, Side::Buy, 100, 1'000'000'000), ev);
    b.submit(limit(4, Side::Buy, 100, 1'000'000'000), ev);
    EXPECT(ev.back().type == EventType::Accepted);
    EXPECT(b.depth_at(Side::Buy, 100) == 2'000'000'000);
    b.replace(3, 5, 101, kHuge, ev);
    EXPECT(ev.back().type == EventType::Rejected && ev.back().reason == Reason::BadQuantity);
    EXPECT(b.open_qty(3) == 1'000'000'000 && b.depth_at(Side::Buy, 100) == 2'000'000'000);
}

void test_market_order_and_empty_book() {
    OrderBook b(16);
    std::vector<Event> ev;
    b.submit(NewOrder{1, 1, Side::Buy, OrdType::Market, Tif::Day, 0, 10}, ev);
    EXPECT(ev.size() == 2 && ev[1].reason == Reason::IocRemainder && ev[1].qty == 10);  // nothing to hit: never rests
    EXPECT(b.order_count() == 0);
    b.submit(limit(2, Side::Buy, 99, 5), ev);
    b.submit(limit(3, Side::Buy, 98, 5), ev);
    ev.clear();
    b.submit(NewOrder{4, 2, Side::Sell, OrdType::Market, Tif::Day, 0, 8}, ev);
    EXPECT(ev[1] == (Event{EventType::Fill, 4, 2, 99, 5, Reason::None}));  // best bid first
    EXPECT(ev[2] == (Event{EventType::Fill, 4, 3, 98, 3, Reason::None}));
    EXPECT(b.best_bid() == 98 && b.depth_at(Side::Buy, 98) == 2);
}

void test_cancel_middle_of_queue_and_level_cleanup() {
    OrderBook b(16);
    std::vector<Event> ev;
    for (OrderId id = 1; id <= 3; ++id) b.submit(limit(id, Side::Sell, 105, 10), ev);
    b.cancel(2, ev);
    EXPECT((b.queue_at(Side::Sell, 105) == std::vector<OrderId>{1, 3}));
    EXPECT(b.depth_at(Side::Sell, 105) == 20);
    b.cancel(1, ev);
    b.cancel(3, ev);
    EXPECT(b.level_count(Side::Sell) == 0 && !b.best_ask().has_value());
    b.submit(limit(4, Side::Sell, 105, 10), ev);  // the level is rebuilt cleanly
    EXPECT((b.queue_at(Side::Sell, 105) == std::vector<OrderId>{4}));
}

void test_replace_variants() {
    OrderBook b(16);
    std::vector<Event> ev;
    b.submit(limit(1, Side::Buy, 100, 10), ev);
    b.submit(limit(2, Side::Buy, 100, 10), ev);
    b.submit(limit(3, Side::Sell, 102, 10), ev);
    ev.clear();
    b.replace(1, 11, 100, 4, ev);  // new id, smaller: keeps front of queue under the new id
    EXPECT((b.queue_at(Side::Buy, 100) == std::vector<OrderId>{11, 2}));
    EXPECT(!b.open_qty(1).has_value() && b.open_qty(11) == 4);
    ev.clear();
    b.replace(2, 12, 102, 6, ev);  // reprice through the offer: trades immediately
    EXPECT(ev[0].type == EventType::Replaced && ev[1].type == EventType::Accepted);
    EXPECT(ev[2] == (Event{EventType::Fill, 12, 3, 102, 6, Reason::None}));
    EXPECT(b.depth_at(Side::Sell, 102) == 4 && b.depth_at(Side::Buy, 100) == 4);
    b.replace(11, 3, 100, 1, ev);  // new id clashes with a live order
    EXPECT(ev.back().reason == Reason::DuplicateId);
    b.replace(77, 78, 100, 1, ev);
    EXPECT(ev.back().reason == Reason::UnknownOrder);
}

void test_post_only_replace() {
    OrderBook b(16);
    std::vector<Event> ev;
    b.submit(limit(1, Side::Sell, 101, 10), ev);
    NewOrder po = limit(2, Side::Buy, 100, 10);
    po.post_only = true;
    b.submit(po, ev);
    ev.clear();
    b.replace(2, 3, 102, 10, ev);  // repricing through the offer must not turn the maker into a taker
    EXPECT(ev.size() == 1 && ev[0] == (Event{EventType::Rejected, 3, 0, 0, 0, Reason::PostOnlyWouldCross}));
    EXPECT(b.open_qty(2) == 10 && !b.open_qty(3) && b.depth_at(Side::Sell, 101) == 10);
    ev.clear();
    b.replace(2, 4, 99, 10, ev);  // a non-crossing reprice keeps the order post-only
    EXPECT(ev.size() == 2 && ev[0].type == EventType::Replaced && ev[1].type == EventType::Accepted);
    ev.clear();
    b.replace(4, 5, 101, 10, ev);
    EXPECT(ev.size() == 1 && ev[0].reason == Reason::PostOnlyWouldCross && b.open_qty(4) == 10);
}

void test_stp_modes() {
    for (Stp mode : {Stp::CancelResting, Stp::CancelAggressor, Stp::CancelBoth}) {
        OrderBook b(16);
        std::vector<Event> ev;
        b.submit(limit(1, Side::Sell, 100, 10, 9), ev);  // same trader as the aggressor
        b.submit(limit(2, Side::Sell, 100, 10, 5), ev);
        ev.clear();
        b.submit(NewOrder{3, 9, Side::Buy, OrdType::Limit, Tif::Day, 100, 15, false, mode}, ev);
        Qty filled = 0;
        for (const auto& e : ev)
            if (e.type == EventType::Fill) filled += e.qty;
        if (mode == Stp::CancelResting) {
            EXPECT(filled == 10 && !b.open_qty(1) && b.open_qty(3) == 5);
        } else if (mode == Stp::CancelAggressor) {
            EXPECT(filled == 0 && b.open_qty(1) == 10 && !b.open_qty(3));
        } else {
            EXPECT(filled == 0 && !b.open_qty(1) && !b.open_qty(3) && b.open_qty(2) == 10);
        }
    }
    // FOK precheck honours STP: the only liquidity ahead belongs to the same trader.
    OrderBook b(16);
    std::vector<Event> ev;
    b.submit(limit(1, Side::Sell, 100, 10, 9), ev);
    b.submit(limit(2, Side::Sell, 101, 10, 5), ev);
    ev.clear();
    b.submit(NewOrder{3, 9, Side::Buy, OrdType::Limit, Tif::Fok, 101, 10, false, Stp::CancelAggressor}, ev);
    EXPECT(ev.back().reason == Reason::FokNotFillable && b.open_qty(1) == 10 && b.open_qty(2) == 10);
    ev.clear();
    b.submit(NewOrder{4, 9, Side::Buy, OrdType::Limit, Tif::Fok, 101, 10, false, Stp::CancelResting}, ev);
    EXPECT(ev.back().type == EventType::Fill && ev.back().counter_id == 2 && !b.open_qty(1));
}

void test_auction_phase_rules() {
    OrderBook b(16, Phase::PreOpen);
    std::vector<Event> ev;
    b.submit(NewOrder{1, 1, Side::Buy, OrdType::Market, Tif::Day, 0, 5}, ev);
    EXPECT(ev.back().reason == Reason::NotAllowedInPhase);
    b.submit(limit(2, Side::Buy, 105, 5), ev);
    b.submit(limit(3, Side::Sell, 95, 5), ev);
    EXPECT(b.best_bid() == 105 && b.best_ask() == 95);  // crossed book is legal before the uncross
    ev.clear();
    const auto r = b.uncross(100, ev);
    // Candidates are the limit prices in the book (95, 105); volume, imbalance and distance to the
    // reference all tie, so the last rule picks the lower price.
    EXPECT(r && r->volume == 5 && r->price == 95);
    EXPECT(b.phase() == Phase::Continuous && b.order_count() == 0);
    OrderBook empty(4, Phase::PreOpen);
    EXPECT(!empty.uncross(100, ev).has_value() && empty.phase() == Phase::Continuous);
}

// ------------------------------------------------------------------ differential test
struct RefOrder {
    OrderId id;
    Side side;
    Price price;
    Qty qty;
    std::uint64_t seq;
};

class ReferenceBook {  // O(n) everything; correct by inspection
    std::vector<RefOrder> book_;
    std::uint64_t seq_ = 0;

public:
    static bool crosses(const NewOrder& o, const RefOrder& r) {
        return r.side != o.side && (o.type == OrdType::Market || (o.side == Side::Buy ? r.price <= o.price : r.price >= o.price));
    }
    std::vector<Event> submit(const NewOrder& o) {
        std::vector<Event> ev{{EventType::Accepted, o.id, 0, o.price, o.qty, Reason::None}};
        if (o.tif == Tif::Fok) {  // all crossing liquidity, no STP in this test
            Qty avail = 0;
            for (const auto& r : book_)
                if (crosses(o, r)) avail += r.qty;
            if (avail < o.qty) {
                ev.push_back({EventType::Cancelled, o.id, 0, o.price, o.qty, Reason::FokNotFillable});
                return ev;
            }
        }
        Qty rem = o.qty;
        while (rem > 0) {
            auto best = book_.end();
            for (auto it = book_.begin(); it != book_.end(); ++it) {
                if (!crosses(o, *it)) continue;
                if (best == book_.end()) {
                    best = it;
                    continue;
                }
                const bool better_px = o.side == Side::Buy ? it->price < best->price : it->price > best->price;
                if (better_px || (it->price == best->price && it->seq < best->seq)) best = it;
            }
            if (best == book_.end()) break;
            const Qty q = std::min(rem, best->qty);
            ev.push_back({EventType::Fill, o.id, best->id, best->price, q, Reason::None});
            rem -= q;
            best->qty -= q;
            if (best->qty == 0) book_.erase(best);
        }
        if (rem > 0) {
            if (o.type == OrdType::Limit && o.tif == Tif::Day)
                book_.push_back({o.id, o.side, o.price, rem, seq_++});
            else
                ev.push_back({EventType::Cancelled, o.id, 0, o.price, rem, Reason::IocRemainder});
        }
        return ev;
    }
    std::vector<Event> cancel(OrderId id) {
        for (auto it = book_.begin(); it != book_.end(); ++it)
            if (it->id == id) {
                std::vector<Event> ev{{EventType::Cancelled, id, 0, it->price, it->qty, Reason::UserCancel}};
                book_.erase(it);
                return ev;
            }
        return {{EventType::Rejected, id, 0, 0, 0, Reason::UnknownOrder}};
    }
    // Same price and no larger: amend in place, keep the arrival sequence. Otherwise cancel and
    // re-enter as a new Day limit with a fresh sequence number (back of the queue).
    std::vector<Event> replace(OrderId old_id, OrderId new_id, Price px, Qty q) {
        for (auto it = book_.begin(); it != book_.end(); ++it) {
            if (it->id != old_id) continue;
            std::vector<Event> ev{{EventType::Replaced, new_id, old_id, px, q, Reason::None}};
            if (px == it->price && q <= it->qty) {
                it->id = new_id;
                it->qty = q;
                return ev;
            }
            const Side s = it->side;
            book_.erase(it);
            const auto more = submit(NewOrder{new_id, 1, s, OrdType::Limit, Tif::Day, px, q});
            ev.insert(ev.end(), more.begin(), more.end());
            return ev;
        }
        return {{EventType::Rejected, new_id, 0, 0, 0, Reason::UnknownOrder}};
    }
    Qty depth(Side s, Price p) const {
        Qty d = 0;
        for (const auto& o : book_)
            if (o.side == s && o.price == p) d += o.qty;
        return d;
    }
};

void test_differential_against_reference() {
    OrderBook fast(4096);
    ReferenceBook ref;
    std::mt19937_64 rng(2026);
    std::vector<Event> ev;
    OrderId next_id = 1;
    int mismatches = 0;
    int replaces = 0, fok_kills = 0, fills = 0;
    int steps = 0;
    for (; steps < 20'000 && mismatches == 0; ++steps) {
        const int r = static_cast<int>(rng() % 100);
        std::vector<Event> want;
        ev.clear();
        if (r < 20 && next_id > 1) {
            const OrderId id = 1 + rng() % (next_id - 1);
            fast.cancel(id, ev);
            want = ref.cancel(id);
        } else if (r < 35 && next_id > 1) {  // cancel/replace: size down, size up or reprice
            const OrderId span = std::min<OrderId>(next_id - 1, 40);  // recent ids: mostly still live
            const OrderId old_id = next_id - 1 - rng() % span;
            const OrderId new_id = next_id++;
            const auto px = static_cast<Price>(95 + rng() % 11);
            const auto q = static_cast<Qty>(1 + rng() % 20);
            fast.replace(old_id, new_id, px, q, ev);
            want = ref.replace(old_id, new_id, px, q);
        } else {
            NewOrder o{next_id++, 1, (rng() & 1) ? Side::Buy : Side::Sell, OrdType::Limit, Tif::Day,
                       static_cast<Price>(95 + rng() % 11), static_cast<Qty>(1 + rng() % 20)};
            if (r >= 85) o.tif = Tif::Ioc;
            if (r >= 91) o.tif = Tif::Fok;
            if (r >= 97) o.type = OrdType::Market;
            fast.submit(o, ev);
            want = ref.submit(o);
        }
        if (ev != want) ++mismatches;
        for (const auto& e : ev) {
            replaces += e.type == EventType::Replaced;
            fok_kills += e.reason == Reason::FokNotFillable;
            fills += e.type == EventType::Fill;
        }
        for (Price p = 95; p <= 105; ++p)
            if (fast.depth_at(Side::Buy, p) != ref.depth(Side::Buy, p) || fast.depth_at(Side::Sell, p) != ref.depth(Side::Sell, p))
                ++mismatches;
        const auto bb = fast.best_bid();
        const auto ba = fast.best_ask();
        if (bb && ba && *bb >= *ba) ++mismatches;  // continuous book is never crossed after matching
    }
    std::cout << "differential: " << steps << " operations, " << replaces << " replaces, " << fok_kills << " FOK kills, " << fills
              << " fills, " << mismatches << " mismatches" << std::endl;
    EXPECT(mismatches == 0);
    EXPECT(steps == 20'000);  // the note quotes 20,000 operations (card qd-lobimpl-differential)
    EXPECT(replaces > 0 && fok_kills > 0 && fills > 0);  // every path was actually exercised
}

// ------------------------------------------------------------------ ITCH builder errors
void test_itch_errors() {
    namespace it = lob::itch;
    const char stock[9] = "TEST    ";
    it::BookBuilder bb(1);
    auto add = it::encode_add(1, 0, 10, 'B', 100, stock, 500);
    EXPECT(add.size() == 36);
    EXPECT(it::encode_executed(1, 0, 10, 1, 1).size() == 31 && it::encode_cancel(1, 0, 10, 1).size() == 23);
    EXPECT(it::encode_delete(1, 0, 10).size() == 19 && it::encode_replace(1, 0, 10, 11, 1, 1).size() == 35);
    EXPECT(bb.apply(add.data(), add.size()) == it::Status::Ok);
    EXPECT(bb.apply(add.data(), add.size()) == it::Status::DuplicateOrder);
    EXPECT(bb.apply(add.data(), 35) == it::Status::Truncated);
    auto bad_side = it::encode_add(1, 0, 11, 'Q', 1, stock, 500);
    EXPECT(bb.apply(bad_side.data(), bad_side.size()) == it::Status::BadSide);
    auto over = it::encode_cancel(1, 0, 10, 101);
    EXPECT(bb.apply(over.data(), over.size()) == it::Status::Overfill);
    EXPECT(bb.bid_shares(500) == 100);  // a rejected modify leaves the book untouched
    auto ghost = it::encode_delete(1, 0, 999);
    EXPECT(bb.apply(ghost.data(), ghost.size()) == it::Status::UnknownOrder);
    const std::uint8_t sys[] = {'S', 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 'O'};
    EXPECT(bb.apply(sys, sizeof sys) == it::Status::Skipped);
    std::vector<std::uint8_t> stream;
    it::frame(stream, it::encode_executed(1, 0, 10, 100, 5));
    stream.pop_back();  // cut the last byte of the block
    EXPECT(bb.apply_stream(stream.data(), stream.size()) == it::Status::Truncated);
    EXPECT(bb.bid_shares(500) == 100);
    std::vector<std::uint8_t> ok;
    it::frame(ok, it::encode_executed(1, 0, 10, 100, 5));
    EXPECT(bb.apply_stream(ok.data(), ok.size()) == it::Status::Ok);
    EXPECT(bb.bid_shares(500) == 0 && bb.live_orders() == 0);  // fully executed order leaves the book
}

// A rejected message or buffer must leave the book exactly as it was (note 07: reported, not applied).
void test_itch_rejects_do_not_mutate() {
    namespace it = lob::itch;
    const char stock[9] = "TEST    ";
    it::BookBuilder bb(1);
    auto a1 = it::encode_add(1, 0, 1, 'B', 100, stock, 500);
    auto a2 = it::encode_add(1, 0, 2, 'S', 70, stock, 600);
    EXPECT(bb.apply(a1.data(), a1.size()) == it::Status::Ok && bb.apply(a2.data(), a2.size()) == it::Status::Ok);
    auto clash = it::encode_replace(1, 0, 1, 2, 30, 510);  // new reference 2 is already live
    EXPECT(bb.apply(clash.data(), clash.size()) == it::Status::DuplicateOrder);
    EXPECT(bb.bid_shares(500) == 100 && bb.bid_shares(510) == 0 && bb.ask_shares(600) == 70 && bb.live_orders() == 2);

    std::vector<std::uint8_t> stream;  // 70 sell: cancel 20, then a cut-off execution of 10
    it::frame(stream, it::encode_cancel(1, 0, 2, 20));
    it::frame(stream, it::encode_executed(1, 0, 2, 10, 7));
    std::vector<std::uint8_t> cut(stream.begin(), stream.end() - 1);
    EXPECT(bb.apply_stream(cut.data(), cut.size()) == it::Status::Truncated);
    EXPECT(bb.ask_shares(600) == 70 && bb.applied == 2);
    EXPECT(bb.apply_stream(stream.data(), stream.size()) == it::Status::Ok);
    EXPECT(bb.ask_shares(600) == 40 && bb.errors == 1);  // 70 - 20 - 10; the one error is the clash above

    it::BookBuilder fresh(1);
    auto zero = it::encode_add(1, 0, 3, 'B', 0, stock, 505);  // zero display shares: dead on arrival
    EXPECT(fresh.apply(zero.data(), zero.size()) == it::Status::Ok);
    EXPECT(fresh.live_orders() == 0 && fresh.bid_shares(505) == 0);
}

}  // namespace

int main() {
    test_validation();
    test_quantity_upper_bound();
    test_market_order_and_empty_book();
    test_cancel_middle_of_queue_and_level_cleanup();
    test_replace_variants();
    test_post_only_replace();
    test_stp_modes();
    test_auction_phase_rules();
    test_differential_against_reference();
    test_itch_errors();
    test_itch_rejects_do_not_mutate();
    std::cout << (g_total - g_failures) << "/" << g_total << " assertions passed" << std::endl;
    return g_failures == 0 ? 0 : 1;
}
