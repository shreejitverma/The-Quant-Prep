// Worked examples for 07-Order-Book-and-Matching-Engine.md, printed and checked:
//   1. an aggressive limit order walking the book;
//   2. cancel/replace and queue priority;
//   3. IOC, FOK and post-only;
//   4. self-trade prevention;
//   5. an opening call auction;
//   6. building a book from ITCH 5.0 messages.
// The engine is lob_engine.hpp, the ITCH book builder lob_itch_book.hpp; edge cases are in
// tests/test_lob_engine.cpp. Prices are integer ticks (here: cents).
// Build: clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror order_matching_engine.cpp

#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>

#include "lob_engine.hpp"
#include "lob_itch_book.hpp"

using namespace lob;

namespace {

int g_failures = 0;

void check(bool ok, const char* what) {
    if (!ok) {
        ++g_failures;
        std::printf("CHECK FAILED: %s\n", what);
    }
}

const char* name(EventType t) {
    switch (t) {
        case EventType::Accepted: return "ACCEPT";
        case EventType::Rejected: return "REJECT";
        case EventType::Fill: return "FILL";
        case EventType::Cancelled: return "CANCEL";
        case EventType::Replaced: return "REPLACE";
    }
    return "?";
}

void print(const std::vector<Event>& ev) {
    for (const auto& e : ev)
        std::printf("    %-7s id %llu counter %llu px %lld qty %lld reason %d\n", name(e.type), static_cast<unsigned long long>(e.id),
                    static_cast<unsigned long long>(e.counter_id), static_cast<long long>(e.price), static_cast<long long>(e.qty),
                    static_cast<int>(e.reason));
}

NewOrder limit(OrderId id, Side s, Price px, Qty q, TraderId trader = 1) { return NewOrder{id, trader, s, OrdType::Limit, Tif::Day, px, q}; }

}  // namespace

int main() {
    std::vector<Event> ev;

    std::printf("1. walking the book\n");
    OrderBook book(1024);
    book.submit(limit(1, Side::Sell, 10100, 300), ev);
    book.submit(limit(2, Side::Sell, 10100, 200), ev);
    book.submit(limit(3, Side::Sell, 10200, 500), ev);
    book.submit(limit(4, Side::Buy, 9900, 400), ev);
    ev.clear();
    book.submit(limit(5, Side::Buy, 10200, 600, 2), ev);
    print(ev);
    check(ev.size() == 4, "accept + three fills");
    check(ev.size() > 1 && ev[1] == Event{EventType::Fill, 5, 1, 10100, 300, Reason::None}, "fill 300 @ 101.00 against order 1 (time priority)");
    check(ev.size() > 2 && ev[2] == Event{EventType::Fill, 5, 2, 10100, 200, Reason::None}, "fill 200 @ 101.00 against order 2");
    check(ev.size() > 3 && ev[3] == Event{EventType::Fill, 5, 3, 10200, 100, Reason::None}, "fill 100 @ 102.00 against order 3");
    // Notional and average price from the engine's fill events, not from the expected fills.
    Qty filled = 0;
    Qty notional = 0;  // cents x shares
    for (const auto& e : ev)
        if (e.type == EventType::Fill) {
            filled += e.qty;
            notional += e.qty * e.price;
        }
    const double avg = static_cast<double>(notional) / static_cast<double>(filled) / 100.0;
    std::printf("    filled %lld, notional %.2f, average price %.4f\n", static_cast<long long>(filled), static_cast<double>(notional) / 100.0, avg);
    check(filled == 600, "qd-lobimpl-walk-book: 600 filled");
    check(notional == 6'070'000, "qd-lobimpl-walk-book: notional 60,700.00");
    check(std::lround(avg * 1e4) == 1'011'667, "qd-lobimpl-walk-book: average price 101.1667");
    check(book.best_ask() == 10200 && book.depth_at(Side::Sell, 10200) == 400, "qd-lobimpl-walk-book: 400 remain offered at 102.00");

    std::printf("2. cancel/replace and priority\n");
    OrderBook pq(1024);
    pq.submit(limit(10, Side::Buy, 10000, 100), ev);
    pq.submit(limit(11, Side::Buy, 10000, 100), ev);
    pq.submit(limit(12, Side::Buy, 10000, 100), ev);
    ev.clear();
    pq.replace(10, 10, 10000, 60, ev);  // size down at the same price: keeps its place
    const auto q1 = pq.queue_at(Side::Buy, 10000);
    std::printf("    after reducing 10 to 60: queue %llu %llu %llu\n", static_cast<unsigned long long>(q1[0]),
                static_cast<unsigned long long>(q1[1]), static_cast<unsigned long long>(q1[2]));
    check(q1 == std::vector<OrderId>{10, 11, 12}, "size-down keeps priority");
    pq.replace(11, 11, 10000, 150, ev);  // size up: goes to the back
    const auto q2 = pq.queue_at(Side::Buy, 10000);
    std::printf("    after increasing 11 to 150: queue %llu %llu %llu\n", static_cast<unsigned long long>(q2[0]),
                static_cast<unsigned long long>(q2[1]), static_cast<unsigned long long>(q2[2]));
    check(q2 == std::vector<OrderId>{10, 12, 11}, "size-up loses priority");
    check(pq.depth_at(Side::Buy, 10000) == 310, "level total 60 + 100 + 150");

    std::printf("3. IOC, FOK, post-only (asks: 400 @ 102.00 left from example 1)\n");
    ev.clear();
    book.submit(NewOrder{20, 2, Side::Buy, OrdType::Limit, Tif::Fok, 10200, 500}, ev);
    print(ev);
    check(ev.back().type == EventType::Cancelled && ev.back().reason == Reason::FokNotFillable, "FOK 500 vs 400 available: killed");
    check(book.depth_at(Side::Sell, 10200) == 400, "FOK touched nothing");
    ev.clear();
    book.submit(NewOrder{21, 2, Side::Buy, OrdType::Limit, Tif::Ioc, 10200, 500}, ev);
    print(ev);
    check(ev.size() > 1 && ev[1].type == EventType::Fill && ev[1].qty == 400, "IOC fills 400");
    check(ev.size() > 2 && ev[2].type == EventType::Cancelled && ev[2].qty == 100 && ev[2].reason == Reason::IocRemainder,
          "IOC remainder 100 cancelled");
    book.submit(limit(22, Side::Sell, 10300, 100), ev);
    ev.clear();
    book.submit(NewOrder{23, 2, Side::Buy, OrdType::Limit, Tif::Day, 10300, 100, true}, ev);
    print(ev);
    check(ev.size() == 1 && ev[0].reason == Reason::PostOnlyWouldCross, "post-only at the offer is rejected");

    std::printf("4. self-trade prevention\n");
    OrderBook stp(1024);
    stp.submit(limit(30, Side::Sell, 10000, 100, 7), ev);
    stp.submit(limit(31, Side::Sell, 10000, 100, 8), ev);
    ev.clear();
    stp.submit(NewOrder{32, 7, Side::Buy, OrdType::Limit, Tif::Day, 10000, 150, false, Stp::CancelResting}, ev);
    print(ev);
    check(ev.size() > 1 && ev[1] == Event{EventType::Cancelled, 30, 32, 10000, 100, Reason::SelfTrade}, "own resting order cancelled");
    check(ev.size() > 2 && ev[2] == Event{EventType::Fill, 32, 31, 10000, 100, Reason::None}, "then trades with the other firm");
    check(stp.best_bid() == 10000 && stp.depth_at(Side::Buy, 10000) == 50, "remaining 50 rests");

    std::printf("5. opening auction\n");
    OrderBook auction(1024, Phase::PreOpen);
    auction.submit(limit(40, Side::Buy, 10200, 10), ev);
    auction.submit(limit(41, Side::Buy, 10100, 20), ev);
    auction.submit(limit(42, Side::Buy, 10000, 30), ev);
    auction.submit(limit(43, Side::Sell, 9900, 15), ev);
    auction.submit(limit(44, Side::Sell, 10000, 25), ev);
    auction.submit(limit(45, Side::Sell, 10200, 20), ev);
    // Independent recomputation of the note's table (and card qd-lobimpl-auction-numeric) from the
    // order list; the engine's clearing price is checked against it below.
    const Qty want_buy[] = {60, 60, 30, 10};
    const Qty want_sell[] = {15, 40, 40, 60};
    const Qty want_exec[] = {15, 40, 30, 10};
    int k = 0;
    for (Price p : {9900, 10000, 10100, 10200}) {
        Qty buy = 0, sell = 0;
        for (auto [bp, bq] : {std::pair{10200, 10}, std::pair{10100, 20}, std::pair{10000, 30}})
            if (bp >= p) buy += bq;
        for (auto [sp, sq] : {std::pair{9900, 15}, std::pair{10000, 25}, std::pair{10200, 20}})
            if (sp <= p) sell += sq;
        std::printf("    price %lld: buy %lld sell %lld executable %lld\n", static_cast<long long>(p), static_cast<long long>(buy),
                    static_cast<long long>(sell), static_cast<long long>(std::min(buy, sell)));
        check(buy == want_buy[k] && sell == want_sell[k] && std::min(buy, sell) == want_exec[k], "qd-lobimpl-auction-numeric: volume table");
        ++k;
    }
    ev.clear();
    const auto res = auction.uncross(10050, ev);
    check(res.has_value(), "the auction uncrosses");
    const AuctionResult cleared = res.value_or(AuctionResult{});
    std::printf("    clearing price %lld volume %lld imbalance %lld, %zu fills\n", static_cast<long long>(cleared.price),
                static_cast<long long>(cleared.volume), static_cast<long long>(cleared.imbalance), ev.size());
    check(cleared.price == 10000 && cleared.volume == 40 && cleared.imbalance == 20,
          "qd-lobimpl-auction-numeric: clears 40 @ 100.00, buy imbalance 20");
    Qty traded = 0;
    for (const auto& e : ev) traded += e.qty;
    check(traded == 40 && ev.size() == 4, "four fills totalling 40");
    check(auction.best_bid() == 10000 && auction.depth_at(Side::Buy, 10000) == 20 && auction.best_ask() == 10200, "post-auction book");
    OrderBook tie(16, Phase::PreOpen);
    tie.submit(limit(50, Side::Buy, 10100, 10), ev);
    tie.submit(limit(51, Side::Sell, 9900, 10), ev);
    const Price t_hi = tie.indicative_auction(10100).value_or(AuctionResult{}).price;
    const Price t_lo = tie.indicative_auction(9800).value_or(AuctionResult{}).price;
    std::printf("    tie: reference 101.00 -> %lld, reference 98.00 -> %lld\n", static_cast<long long>(t_hi), static_cast<long long>(t_lo));
    check(t_hi == 10100 && t_lo == 9900, "reference price breaks the tie");

    std::printf("6. ITCH 5.0 book building\n");
    namespace it = lob::itch;
    constexpr std::uint16_t kLocate = 7;
    const char stock[9] = "ZVZZT   ";
    std::vector<std::uint8_t> stream;
    it::frame(stream, it::encode_add(kLocate, 1000, 1, 'B', 300, stock, 1'000'100));  // 300 @ 100.0100
    it::frame(stream, it::encode_add(kLocate, 1001, 2, 'B', 200, stock, 1'000'100));
    it::frame(stream, it::encode_add(kLocate, 1002, 3, 'S', 500, stock, 1'000'300));
    it::frame(stream, it::encode_executed(kLocate, 1003, 1, 100, 77));  // 100 of order 1 traded
    it::frame(stream, it::encode_cancel(kLocate, 1004, 2, 50));          // 50 of order 2 cancelled
    it::frame(stream, it::encode_replace(kLocate, 1005, 3, 4, 400, 1'000'200));  // ask improves to 100.0200
    it::frame(stream, it::encode_add(kLocate + 1, 1006, 5, 'S', 999, stock, 1));  // other stock: skipped
    it::frame(stream, it::encode_delete(kLocate, 1007, 1));
    it::BookBuilder bb(kLocate);
    const auto st = bb.apply_stream(stream.data(), stream.size());
    std::printf("    %zu bytes, applied %llu, skipped %llu, errors %llu\n", stream.size(), static_cast<unsigned long long>(bb.applied),
                static_cast<unsigned long long>(bb.skipped), static_cast<unsigned long long>(bb.errors));
    std::printf("    best bid %u x %llu, best ask %u x %llu, live orders %zu\n", bb.best_bid(),
                static_cast<unsigned long long>(bb.bid_shares(bb.best_bid())), bb.best_ask(),
                static_cast<unsigned long long>(bb.ask_shares(bb.best_ask())), bb.live_orders());
    check(st == it::Status::Ok && bb.applied == 7 && bb.skipped == 1 && bb.errors == 0, "stream counts");
    check(stream.size() == 3 * (2 + 36) + (2 + 31) + (2 + 23) + (2 + 35) + (2 + 36) + (2 + 19), "framed size");
    check(stream.size() == 268, "framed size is 268 bytes");
    std::printf("    ITCH lengths: A %zu F %zu E %zu C %zu X %zu D %zu U %zu\n", it::message_length('A'), it::message_length('F'),
                it::message_length('E'), it::message_length('C'), it::message_length('X'), it::message_length('D'), it::message_length('U'));
    check(it::message_length('A') == 36 && it::message_length('F') == 40 && it::message_length('E') == 31 && it::message_length('C') == 36 &&
              it::message_length('X') == 23 && it::message_length('D') == 19 && it::message_length('U') == 35,
          "qd-lobimpl-itch-lengths: ITCH 5.0 sections 4.3 and 4.4");
    check(bb.best_bid() == 1'000'100 && bb.bid_shares(1'000'100) == 150, "bid 150 = order 2's 200 - 50");
    check(bb.best_ask() == 1'000'200 && bb.ask_shares(1'000'200) == 400, "replaced ask 400 @ 100.0200");
    check(bb.live_orders() == 2, "orders 2 and 4 remain");

    std::printf("%s\n", g_failures == 0 ? "all checks passed" : "CHECKS FAILED");
    return g_failures == 0 ? EXIT_SUCCESS : EXIT_FAILURE;
}
