// Unit, property and fuzz tests for itch50_feed_handler.hpp (note 08) used
// as the worked testing example in note 14.
//
//   * Message lengths and field offsets against the ITCH 5.0 spec (03/06/2015).
//   * Round trips, truncation, unknown types.
//   * MoldUDP64 framing: heartbeat, end of session, malformed blocks deliver
//     nothing.
//   * Arbitration property: for random streams, random losses on A and B and
//     random interleaving, the merged stream is exactly 1..N in order after
//     retransmission, and the book equals the loss-free book.
//   * Seeded fuzz loops over decode, the packet parser, the arbitrator and
//     the book builder; run under ASan/UBSan they prove no out-of-bounds read.
//
// Framework-free: exits non-zero on any failure. Randomness is a hand-written
// splitmix64 so the cases are identical on libstdc++ and libc++ (the
// standard fixes std::mt19937's output but not std::uniform_int_distribution's).

#include "itch50_feed_handler.hpp"

#include <algorithm>
#include <cstdint>
#include <iostream>
#include <limits>
#include <random>
#include <utility>
#include <vector>

using namespace itch50;

namespace {

int g_failures = 0;
int g_total = 0;

#define EXPECT(cond)                                                                       \
    do {                                                                                   \
        ++g_total;                                                                         \
        if (!(cond)) {                                                                     \
            ++g_failures;                                                                  \
            std::cerr << "  FAIL: " << __FILE__ << ":" << __LINE__ << " -> " #cond << "\n"; \
        }                                                                                  \
    } while (0)

#define RUN_TEST(fn)                                       \
    do {                                                   \
        std::cout << "[RUN ] " #fn << std::endl;           \
        const int before = g_failures;                     \
        fn();                                              \
        std::cout << (g_failures == before ? "[ OK ] " : "[FAIL] ") << #fn << std::endl; \
    } while (0)

struct SplitMix64 {
    std::uint64_t s;
    std::uint64_t next() {
        std::uint64_t z = (s += 0x9E3779B97F4A7C15ull);
        z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ull;
        z = (z ^ (z >> 27)) * 0x94D049BB133111EBull;
        return z ^ (z >> 31);
    }
    std::uint64_t below(std::uint64_t n) { return next() % n; }  // tiny modulo bias is irrelevant here
};

const Session kSession = {'T', 'E', 'S', 'T', 'S', 'E', 'S', 'S', '0', '1'};

// ---------------------------------------------------------------------------
// Spec conformance
// ---------------------------------------------------------------------------

void test_message_lengths_match_spec() {
    EXPECT(message_length('S') == 12);
    EXPECT(message_length('R') == 39);
    EXPECT(message_length('H') == 25);
    EXPECT(message_length('A') == 36);
    EXPECT(message_length('F') == 40);
    EXPECT(message_length('E') == 31);
    EXPECT(message_length('C') == 36);
    EXPECT(message_length('X') == 23);
    EXPECT(message_length('D') == 19);
    EXPECT(message_length('U') == 35);
    EXPECT(message_length('P') == 44);
    EXPECT(message_length('Q') == 40);
    EXPECT(message_length('B') == 19);
    EXPECT(message_length('Z') == 0);
    EXPECT(kMaxPrice4 == 0x77359400u);
}

void test_add_order_offsets_are_big_endian() {
    DecodedMessage m;
    m.type = 'A';
    m.stock_locate = 0x0102;
    m.tracking_number = 0x0304;
    m.timestamp_ns = 0x0A0B0C0D0E0Full;  // 6 bytes
    m.order_ref = 0x1112131415161718ull;
    m.side = 'S';
    m.shares = 0x21222324u;
    m.stock = {'A', 'B', 'C', ' ', ' ', ' ', ' ', ' '};
    m.price = 0x31323334u;
    const auto w = encode(m);
    EXPECT(w.size() == 36);
    EXPECT(w[0] == 'A');
    EXPECT(w[1] == 0x01 && w[2] == 0x02);                  // Stock Locate offset 1 length 2
    EXPECT(w[3] == 0x03 && w[4] == 0x04);                  // Tracking Number offset 3 length 2
    EXPECT(w[5] == 0x0A && w[10] == 0x0F);                 // Timestamp offset 5 length 6
    EXPECT(w[11] == 0x11 && w[18] == 0x18);                // Order Reference offset 11 length 8
    EXPECT(w[19] == 'S');                                  // Buy/Sell offset 19
    EXPECT(w[20] == 0x21 && w[23] == 0x24);                // Shares offset 20 length 4
    EXPECT(w[24] == 'A' && w[31] == ' ');                  // Stock offset 24 length 8
    EXPECT(w[32] == 0x31 && w[35] == 0x34);                // Price offset 32 length 4
}

void test_replace_and_executed_with_price_offsets() {
    DecodedMessage u;
    u.type = 'U';
    u.order_ref = 1;
    u.new_order_ref = 2;
    u.shares = 3;
    u.price = 4;
    const auto wu = encode(u);
    EXPECT(wu.size() == 35);
    EXPECT(wu[18] == 1 && wu[26] == 2 && wu[30] == 3 && wu[34] == 4);  // offsets 11, 19, 27, 31

    DecodedMessage c;
    c.type = 'C';
    c.order_ref = 9;
    c.shares = 8;
    c.match_number = 7;
    c.printable = 'N';
    c.price = 6;
    const auto wc = encode(c);
    EXPECT(wc.size() == 36);
    EXPECT(wc[18] == 9 && wc[22] == 8 && wc[30] == 7 && wc[31] == 'N' && wc[35] == 6);
}

void test_lengths_equal_sum_of_spec_field_widths() {
    // Each spec length re-derived from the field widths listed in the spec's
    // message formats: the 11-byte common header (type 1, locate 2, tracking 2,
    // timestamp 6) plus the type's own fields. Independent of message_length().
    struct Layout {
        char type;
        std::vector<std::size_t> fields;
    };
    const std::vector<Layout> layouts = {
        {'S', {1}},                                         // Event Code
        {'R', {8, 1, 1, 4, 1, 1, 2, 1, 1, 1, 1, 1, 4, 1}},  // Stock .. Inverse Indicator
        {'H', {8, 1, 1, 4}},                                // Stock, Trading State, Reserved, Reason
        {'A', {8, 1, 4, 8, 4}},                             // Ref, Buy/Sell, Shares, Stock, Price
        {'F', {8, 1, 4, 8, 4, 4}},                          // as A plus Attribution
        {'E', {8, 4, 8}},                                   // Ref, Executed Shares, Match
        {'C', {8, 4, 8, 1, 4}},                             // as E plus Printable, Execution Price
        {'X', {8, 4}},                                      // Ref, Canceled Shares
        {'D', {8}},                                         // Ref
        {'U', {8, 8, 4, 4}},                                // Original Ref, New Ref, Shares, Price
        {'P', {8, 1, 4, 8, 4, 8}},                          // Ref, Buy/Sell, Shares, Stock, Price, Match
        {'Q', {8, 8, 4, 8, 1}},                             // Shares, Stock, Cross Price, Match, Cross Type
        {'B', {8}},                                         // Match
    };
    const std::size_t header = 1 + 2 + 2 + 6;
    EXPECT(header == 11);
    for (const auto& l : layouts) {
        std::size_t len = header;
        for (std::size_t w : l.fields) len += w;
        EXPECT(len == message_length(l.type));
    }
}

void test_last_field_ends_at_spec_length() {
    // encode() sizes its buffer from message_length(), so w.size() alone is
    // circular; check that the last field is written into the last bytes.
    DecodedMessage m;
    m.type = 'S';
    m.event_code = 'C';
    EXPECT(encode(m)[11] == 'C' && encode(m).size() == 12);
    m = DecodedMessage{};
    m.type = 'E';
    m.match_number = 0x0102030405060708ull;
    auto w = encode(m);
    EXPECT(w.size() == 31 && w[23] == 0x01 && w[30] == 0x08);  // Match Number offset 23 length 8
    m = DecodedMessage{};
    m.type = 'X';
    m.shares = 0x0A0B0C0Du;
    w = encode(m);
    EXPECT(w.size() == 23 && w[19] == 0x0A && w[22] == 0x0D);  // Canceled Shares offset 19 length 4
    m = DecodedMessage{};
    m.type = 'D';
    m.order_ref = 0x1112131415161718ull;
    w = encode(m);
    EXPECT(w.size() == 19 && w[11] == 0x11 && w[18] == 0x18);  // Order Reference offset 11 length 8
    m = DecodedMessage{};
    m.type = 'F';
    m.attribution = {'Q', 'P', 'M', 'M'};
    w = encode(m);
    EXPECT(w.size() == 40 && w[36] == 'Q' && w[39] == 'M');  // Attribution offset 36 length 4
    m = DecodedMessage{};
    m.type = 'P';
    m.match_number = 0x2122232425262728ull;
    w = encode(m);
    EXPECT(w.size() == 44 && w[36] == 0x21 && w[43] == 0x28);  // Match Number offset 36 length 8
}

void test_round_trip_every_decoded_type() {
    const char types[] = {'S', 'A', 'F', 'E', 'C', 'X', 'D', 'U', 'P'};
    SplitMix64 rng{7};
    for (char t : types) {
        DecodedMessage m;
        m.type = t;
        m.stock_locate = static_cast<std::uint16_t>(rng.next());
        m.tracking_number = static_cast<std::uint16_t>(rng.next());
        m.timestamp_ns = rng.next() & ((1ull << 48) - 1);
        if (t == 'S') m.event_code = 'Q';
        if (t != 'S') m.order_ref = rng.next();
        if (t == 'U') m.new_order_ref = rng.next();
        if (t == 'E' || t == 'C' || t == 'P') m.match_number = rng.next();
        if (t != 'S' && t != 'D') m.shares = static_cast<std::uint32_t>(rng.next());
        if (t == 'A' || t == 'F' || t == 'U' || t == 'P' || t == 'C') m.price = static_cast<std::uint32_t>(rng.next());
        if (t == 'A' || t == 'F' || t == 'P') {
            m.side = 'B';
            m.stock = {'X', 'Y', 'Z', ' ', ' ', ' ', ' ', ' '};
        }
        if (t == 'F') m.attribution = {'M', 'P', 'I', 'D'};
        if (t == 'C') m.printable = 'Y';
        const auto w = encode(m);
        DecodedMessage back;
        EXPECT(decode(w.data(), w.size(), back) == DecodeStatus::Ok);
        EXPECT(encode(back) == w);
        EXPECT(back.order_ref == m.order_ref && back.shares == m.shares && back.price == m.price);
        EXPECT(back.timestamp_ns == m.timestamp_ns && back.stock_locate == m.stock_locate);
    }
}

void test_truncated_unknown_and_empty() {
    const char types[] = {'S', 'R', 'H', 'A', 'F', 'E', 'C', 'X', 'D', 'U', 'P', 'Q', 'B'};
    for (char t : types) {
        std::vector<std::uint8_t> buf(message_length(t), 0);
        buf[0] = static_cast<std::uint8_t>(t);
        DecodedMessage out;
        out.order_ref = 42;
        EXPECT(decode(buf.data(), buf.size() - 1, out) == DecodeStatus::Truncated);
        EXPECT(out.order_ref == 42);  // untouched on error
        EXPECT(decode(buf.data(), buf.size(), out) == DecodeStatus::Ok);
    }
    const std::uint8_t z[1] = {'Z'};
    DecodedMessage out;
    EXPECT(decode(z, 1, out) == DecodeStatus::UnknownType);
    EXPECT(decode(z, 0, out) == DecodeStatus::Empty);
    EXPECT(decode(nullptr, 5, out) == DecodeStatus::Empty);
}

// ---------------------------------------------------------------------------
// MoldUDP64 framing
// ---------------------------------------------------------------------------

void test_mold_heartbeat_and_end_of_session() {
    const auto hb = build_mold_packet(kSession, 77, {}, kMoldHeartbeat);
    const auto eos = build_mold_packet(kSession, 77, {}, kMoldEndOfSession);
    EXPECT(hb.size() == 20 && eos.size() == 20);
    int calls = 0;
    MoldHeader h;
    EXPECT(parse_mold_packet(hb.data(), hb.size(), h, [&](std::uint64_t, const std::uint8_t*, std::size_t) { ++calls; }) ==
           MoldStatus::Ok);
    EXPECT(h.count == 0 && h.sequence == 77);
    EXPECT(parse_mold_packet(eos.data(), eos.size(), h, [&](std::uint64_t, const std::uint8_t*, std::size_t) { ++calls; }) ==
           MoldStatus::Ok);
    EXPECT(h.count == 0xFFFF && calls == 0);
}

void test_mold_malformed_delivers_nothing() {
    DecodedMessage d;
    d.type = 'D';
    d.order_ref = 5;
    const auto pkt = build_mold_packet(kSession, 1, {encode(d), encode(d)});
    EXPECT(pkt.size() == 20 + 2 * (2 + 19));
    int calls = 0;
    auto count = [&](std::uint64_t, const std::uint8_t*, std::size_t) { ++calls; };
    MoldHeader h;
    EXPECT(parse_mold_packet(pkt.data(), pkt.size(), h, count) == MoldStatus::Ok);
    EXPECT(calls == 2);
    calls = 0;
    // Cut the second block short: the first block must not be delivered either.
    EXPECT(parse_mold_packet(pkt.data(), pkt.size() - 1, h, count) == MoldStatus::BadBlock);
    EXPECT(calls == 0);
    // Extra byte after the declared blocks.
    std::vector<std::uint8_t> longer = pkt;
    longer.push_back(0);
    EXPECT(parse_mold_packet(longer.data(), longer.size(), h, count) == MoldStatus::TrailingBytes);
    EXPECT(parse_mold_packet(pkt.data(), 19, h, count) == MoldStatus::TooShort);
    EXPECT(calls == 0);
}

void test_mold_packet_and_request_offsets() {
    // MoldUDP64 V1.00 downstream packet: Session 0..9, Sequence Number 10..17,
    // Message Count 18..19, then per block a 2-byte length and the message.
    DecodedMessage d;
    d.type = 'D';
    d.order_ref = 0x55;
    const auto pkt = build_mold_packet(kSession, 0x0102030405060708ull, {encode(d), encode(d)});
    EXPECT(pkt.size() == 20 + 2 * (2 + 19));
    EXPECT(std::equal(kSession.begin(), kSession.end(), pkt.begin()));
    EXPECT(pkt[10] == 0x01 && pkt[17] == 0x08);           // Sequence Number offset 10 length 8
    EXPECT(pkt[18] == 0x00 && pkt[19] == 0x02);           // Message Count offset 18 length 2
    EXPECT(pkt[20] == 0x00 && pkt[21] == 19);             // first Message Length offset 20
    EXPECT(pkt[22] == 'D' && pkt[22 + 19 - 1] == 0x55);   // first Message Data offset 22
    EXPECT(pkt[41] == 0x00 && pkt[42] == 19 && pkt[43] == 'D');  // second block follows directly
    // Request Packet: Session 10, Sequence Number 8, Requested Message Count 2.
    const auto req = build_mold_request(kSession, 11, 3);
    EXPECT(req.size() == 20);
    EXPECT(std::equal(kSession.begin(), kSession.end(), req.begin()));
    EXPECT(read_be(req.data() + 10, 8) == 11 && read_be(req.data() + 18, 2) == 3);
}

void test_heartbeat_reveals_tail_gap() {
    // Losing the last packet before a quiet period is only visible through
    // the next heartbeat, which carries the next expected sequence number.
    DecodedMessage d;
    d.type = 'D';
    std::vector<std::uint64_t> got;
    LineArbitrator arb([&](std::uint64_t s, const std::uint8_t*, std::size_t) { got.push_back(s); });
    const auto p1 = build_mold_packet(kSession, 1, {encode(d), encode(d)});
    arb.on_packet(p1.data(), p1.size());
    EXPECT(!arb.missing().has_value());
    const auto hb = build_mold_packet(kSession, 6, {}, kMoldHeartbeat);  // 3..5 were lost
    EXPECT(arb.on_packet(hb.data(), hb.size()) == PacketAction::Heartbeat);
    const auto gap = arb.missing();
    EXPECT(gap.has_value() && gap->first == 3 && gap->last == 5 && gap->size() == 3);
    EXPECT(arb.stats().gaps_detected == 1);
}

void test_wrong_session_rejected() {
    DecodedMessage d;
    d.type = 'D';
    LineArbitrator arb([](std::uint64_t, const std::uint8_t*, std::size_t) {});
    const auto p1 = build_mold_packet(kSession, 1, {encode(d)});
    Session other = kSession;
    other[9] = '2';
    const auto p2 = build_mold_packet(other, 2, {encode(d)});
    EXPECT(arb.on_packet(p1.data(), p1.size()) == PacketAction::Delivered);
    EXPECT(arb.on_packet(p2.data(), p2.size()) == PacketAction::WrongSession);
    EXPECT(arb.next_expected() == 2);
}

void test_overlapping_packet_delivers_only_new_messages() {
    DecodedMessage d;
    d.type = 'D';
    std::vector<std::uint64_t> got;
    LineArbitrator arb([&](std::uint64_t s, const std::uint8_t*, std::size_t) { got.push_back(s); });
    const auto a = build_mold_packet(kSession, 1, {encode(d), encode(d)});            // 1..2
    const auto b = build_mold_packet(kSession, 2, {encode(d), encode(d), encode(d)});  // 2..4
    arb.on_packet(a.data(), a.size());
    arb.on_packet(b.data(), b.size());
    EXPECT((got == std::vector<std::uint64_t>{1, 2, 3, 4}));
}

void test_card_overlap_8_to_12_while_expecting_10() {
    // Card qd-feed-overlap: a packet carrying 8..12 arrives while 10 is next.
    DecodedMessage d;
    d.type = 'D';
    std::vector<std::uint64_t> got;
    LineArbitrator arb([&](std::uint64_t s, const std::uint8_t*, std::size_t) { got.push_back(s); });
    const auto p1_9 = build_mold_packet(kSession, 1, std::vector<std::vector<std::uint8_t>>(9, encode(d)));
    const auto p8_12 = build_mold_packet(kSession, 8, std::vector<std::vector<std::uint8_t>>(5, encode(d)));
    EXPECT(arb.on_packet(p1_9.data(), p1_9.size()) == PacketAction::Delivered);
    EXPECT(arb.next_expected() == 10);
    got.clear();
    EXPECT(arb.on_packet(p8_12.data(), p8_12.size()) == PacketAction::Delivered);
    EXPECT((got == std::vector<std::uint64_t>{10, 11, 12}));
    EXPECT(arb.next_expected() == 13);
}

void test_longer_copy_of_buffered_packet_is_kept() {
    // Line A buffers 3..4 behind a gap; a differently packetised copy 3..6
    // (for example a resend) must not be discarded as a duplicate.
    DecodedMessage d;
    d.type = 'D';
    std::vector<std::uint64_t> got;
    LineArbitrator arb([&](std::uint64_t s, const std::uint8_t*, std::size_t) { got.push_back(s); });
    const auto p1 = build_mold_packet(kSession, 1, {encode(d)});                                   // 1
    const auto p34 = build_mold_packet(kSession, 3, {encode(d), encode(d)});                       // 3..4
    const auto p36 = build_mold_packet(kSession, 3, {encode(d), encode(d), encode(d), encode(d)});  // 3..6
    const auto p2 = build_mold_packet(kSession, 2, {encode(d)});                                   // 2
    EXPECT(arb.on_packet(p1.data(), p1.size()) == PacketAction::Delivered);
    EXPECT(arb.on_packet(p34.data(), p34.size()) == PacketAction::Buffered);
    EXPECT(arb.on_packet(p36.data(), p36.size()) == PacketAction::Buffered);   // longer copy replaces
    EXPECT(arb.on_packet(p34.data(), p34.size()) == PacketAction::Duplicate);  // shorter copy dropped
    EXPECT(arb.buffered() == 1);
    EXPECT(arb.on_packet(p2.data(), p2.size()) == PacketAction::Delivered);
    EXPECT((got == std::vector<std::uint64_t>{1, 2, 3, 4, 5, 6}));
    EXPECT(arb.next_expected() == 7 && !arb.missing().has_value());
}

void test_full_reorder_buffer_is_reported() {
    DecodedMessage d;
    d.type = 'D';
    LineArbitrator arb([](std::uint64_t, const std::uint8_t*, std::size_t) {}, 1, 2);
    const auto p3 = build_mold_packet(kSession, 3, {encode(d)});
    const auto p5 = build_mold_packet(kSession, 5, {encode(d)});
    const auto p7 = build_mold_packet(kSession, 7, {encode(d)});
    EXPECT(arb.on_packet(p3.data(), p3.size()) == PacketAction::Buffered);
    EXPECT(arb.on_packet(p5.data(), p5.size()) == PacketAction::Buffered);
    EXPECT(arb.on_packet(p7.data(), p7.size()) == PacketAction::BufferFull);
    EXPECT(arb.buffered() == 2 && arb.next_expected() == 1);
}

// ---------------------------------------------------------------------------
// Book building
// ---------------------------------------------------------------------------

void test_zero_share_add_never_rests() {
    BookBuilder b;
    DecodedMessage a;
    a.type = 'A';
    a.stock_locate = 4;
    a.order_ref = 1;
    a.side = 'B';
    a.shares = 0;
    a.price = 100'000;
    EXPECT(b.apply(a) == ApplyStatus::Ok);
    EXPECT(b.live_orders() == 0 && b.levels(4, 'B') == 0 && !b.top(4).has_bid);
}

void test_book_rejects_inconsistent_updates() {
    BookBuilder b;
    DecodedMessage a;
    a.type = 'A';
    a.stock_locate = 3;
    a.order_ref = 10;
    a.side = 'B';
    a.shares = 100;
    a.price = 500'000;
    EXPECT(b.apply(a) == ApplyStatus::Ok);
    EXPECT(b.apply(a) == ApplyStatus::DuplicateOrder);
    DecodedMessage x;
    x.type = 'X';
    x.order_ref = 10;
    x.shares = 101;
    EXPECT(b.apply(x) == ApplyStatus::Overfill);
    x.order_ref = 11;
    x.shares = 1;
    EXPECT(b.apply(x) == ApplyStatus::UnknownOrder);
    a.order_ref = 12;
    a.side = '?';
    EXPECT(b.apply(a) == ApplyStatus::BadSide);
    EXPECT(b.level(3, 'B', 500'000) == 100);
    DecodedMessage e;
    e.type = 'E';
    e.order_ref = 10;
    e.shares = 100;
    EXPECT(b.apply(e) == ApplyStatus::Ok);
    EXPECT(b.live_orders() == 0 && b.levels(3, 'B') == 0 && !b.top(3).has_bid);
}

void test_card_cumulative_deltas_300_e100_x150() {
    // Card qd-feed-itch-deltas: Add 300, Executed 100, Cancel 150 leaves 50
    // displayed; the order dies when display shares reach zero.
    BookBuilder b;
    DecodedMessage a;
    a.type = 'A';
    a.stock_locate = 2;
    a.order_ref = 7;
    a.side = 'B';
    a.shares = 300;
    a.price = 1'000'000;
    EXPECT(b.apply(a) == ApplyStatus::Ok);
    DecodedMessage e;
    e.type = 'E';
    e.order_ref = 7;
    e.shares = 100;
    EXPECT(b.apply(e) == ApplyStatus::Ok);
    DecodedMessage x;
    x.type = 'X';
    x.order_ref = 7;
    x.shares = 150;
    EXPECT(b.apply(x) == ApplyStatus::Ok);
    EXPECT(b.level(2, 'B', 1'000'000) == 50 && b.live_orders() == 1);
    x.shares = 50;
    EXPECT(b.apply(x) == ApplyStatus::Ok);
    EXPECT(b.live_orders() == 0 && b.levels(2, 'B') == 0);
}

void test_replace_keeps_side_and_locate() {
    BookBuilder b;
    DecodedMessage a;
    a.type = 'A';
    a.stock_locate = 9;
    a.order_ref = 1;
    a.side = 'S';
    a.shares = 300;
    a.price = 1'010'000;
    EXPECT(b.apply(a) == ApplyStatus::Ok);
    DecodedMessage u;
    u.type = 'U';
    u.stock_locate = 9;
    u.order_ref = 1;
    u.new_order_ref = 2;
    u.shares = 120;
    u.price = 1'005'000;
    EXPECT(b.apply(u) == ApplyStatus::Ok);
    const TopOfBook t = b.top(9);
    EXPECT(t.has_ask && t.ask_price == 1'005'000 && t.ask_shares == 120 && !t.has_bid);
    EXPECT(b.level(9, 'S', 1'010'000) == 0);
    EXPECT(b.apply(u) == ApplyStatus::UnknownOrder);  // the old reference is dead
    // The spec gives the replacement a new day-unique reference: reusing the old one is rejected
    // and leaves the order as it was.
    DecodedMessage same = u;
    same.order_ref = 2;
    same.new_order_ref = 2;
    same.shares = 50;
    EXPECT(b.apply(same) == ApplyStatus::DuplicateOrder);
    EXPECT(b.top(9).ask_shares == 120 && b.level(9, 'S', 1'005'000) == 120);
}

// A sequence number so large that the packet's last message would wrap past 2^64 cannot come from
// a real session: it is malformed, not a duplicate of messages already delivered.
void test_sequence_overflow_is_malformed() {
    DecodedMessage d;
    d.type = 'D';
    d.order_ref = 5;
    int delivered = 0;
    LineArbitrator arb([&](std::uint64_t, const std::uint8_t*, std::size_t) { ++delivered; }, 1, 64);
    const auto wrap = build_mold_packet(kSession, std::numeric_limits<std::uint64_t>::max(), {encode(d), encode(d)});
    EXPECT(arb.on_packet(wrap.data(), wrap.size()) == PacketAction::Malformed);
    const auto last = build_mold_packet(kSession, std::numeric_limits<std::uint64_t>::max() - 1, {encode(d)});
    EXPECT(arb.on_packet(last.data(), last.size()) == PacketAction::Buffered);  // ends exactly at 2^64 - 1: still valid
    EXPECT(delivered == 0 && arb.stats().duplicate_packets == 0);
}

// ---------------------------------------------------------------------------
// Property: random stream, random losses, random interleaving
// ---------------------------------------------------------------------------

std::vector<DecodedMessage> random_stream(SplitMix64& rng, std::size_t n) {
    std::vector<DecodedMessage> out;
    std::vector<std::pair<std::uint64_t, std::uint32_t>> live;  // ref, shares
    std::uint64_t next_ref = 1;
    std::uint64_t match = 1;
    for (std::size_t i = 0; i < n; ++i) {
        DecodedMessage m;
        m.stock_locate = static_cast<std::uint16_t>(1 + rng.below(3));
        m.timestamp_ns = 34'200'000'000'000ull + i;
        const std::uint64_t r = rng.below(10);
        if (live.empty() || r < 4) {
            m.type = 'A';
            m.order_ref = next_ref++;
            m.side = rng.below(2) ? 'B' : 'S';
            m.shares = static_cast<std::uint32_t>(100 * (1 + rng.below(5)));
            m.price = static_cast<std::uint32_t>(990'000 + 100 * rng.below(21));
            live.emplace_back(m.order_ref, m.shares);
        } else {
            const std::size_t k = static_cast<std::size_t>(rng.below(live.size()));
            auto& [ref, sh] = live[k];
            m.order_ref = ref;
            if (r < 6) {
                m.type = r == 4 ? 'E' : 'X';
                m.shares = static_cast<std::uint32_t>(1 + rng.below(sh));
                if (m.type == 'E') m.match_number = match++;
                sh -= m.shares;
            } else if (r < 8) {
                m.type = 'D';
                sh = 0;
            } else {
                m.type = 'U';
                m.new_order_ref = next_ref++;
                m.shares = static_cast<std::uint32_t>(100 * (1 + rng.below(5)));
                m.price = static_cast<std::uint32_t>(990'000 + 100 * rng.below(21));
                ref = m.new_order_ref;
                sh = m.shares;
            }
            if (sh == 0) live.erase(live.begin() + static_cast<long>(k));
        }
        out.push_back(m);
    }
    return out;
}

void test_property_arbitration_rebuilds_reference_book() {
    SplitMix64 rng{2026};
    int cases = 0;
    for (int trial = 0; trial < 200; ++trial) {
        const std::size_t n = 20 + static_cast<std::size_t>(rng.below(200));
        const auto stream = random_stream(rng, n);
        BookBuilder ref;
        bool ref_ok = true;
        for (const auto& m : stream) ref_ok = ref_ok && ref.apply(m) == ApplyStatus::Ok;
        EXPECT(ref_ok);

        // Packetise into 1..5 messages per packet.
        std::vector<std::vector<std::uint8_t>> pkts;
        std::vector<std::pair<std::uint64_t, std::size_t>> ranges;  // first seq, count
        for (std::size_t i = 0; i < n;) {
            const std::size_t k = std::min<std::size_t>(n - i, 1 + rng.below(5));
            std::vector<std::vector<std::uint8_t>> body;
            for (std::size_t j = 0; j < k; ++j) body.push_back(encode(stream[i + j]));
            pkts.push_back(build_mold_packet(kSession, i + 1, body));
            ranges.emplace_back(i + 1, k);
            i += k;
        }
        // Each line independently loses about 20% of packets; arrivals interleave.
        std::vector<std::pair<int, std::size_t>> arrivals;  // line, packet
        for (std::size_t p = 0; p < pkts.size(); ++p) {
            for (int line = 0; line < 2; ++line) {
                if (rng.below(5) != 0) arrivals.emplace_back(line, p);
            }
        }
        for (std::size_t i = 1; i < arrivals.size(); ++i) {  // local reordering only
            if (rng.below(3) == 0) std::swap(arrivals[i - 1], arrivals[i]);
        }

        BookBuilder live;
        std::vector<std::uint64_t> seqs;
        bool apply_ok = true;
        LineArbitrator arb([&](std::uint64_t s, const std::uint8_t* d, std::size_t len) {
            DecodedMessage m;
            apply_ok = apply_ok && decode(d, len, m) == DecodeStatus::Ok && live.apply(m) == ApplyStatus::Ok;
            seqs.push_back(s);
        });
        for (const auto& [line, p] : arrivals) arb.on_packet(pkts[p].data(), pkts[p].size());
        const auto hb = build_mold_packet(kSession, n + 1, {}, kMoldHeartbeat);
        arb.on_packet(hb.data(), hb.size());
        // Retransmit until whole: the server answers with exactly the requested messages.
        int requests = 0;
        while (auto gap = arb.missing()) {
            ++requests;
            std::vector<std::vector<std::uint8_t>> body;
            for (std::uint64_t s = gap->first; s <= gap->last; ++s) body.push_back(encode(stream[s - 1]));
            const auto rt = build_mold_packet(kSession, gap->first, body);
            arb.on_packet(rt.data(), rt.size());
            if (requests > 1000) break;
        }
        bool exact = seqs.size() == n;
        for (std::size_t i = 0; exact && i < n; ++i) exact = seqs[i] == i + 1;
        EXPECT(exact);
        EXPECT(apply_ok);
        bool same = true;
        for (std::uint16_t loc = 1; loc <= 3; ++loc) {
            same = same && live.depth(loc, 'B') == ref.depth(loc, 'B') && live.depth(loc, 'S') == ref.depth(loc, 'S');
        }
        EXPECT(same);
        EXPECT(live.live_orders() == ref.live_orders());
        ++cases;
    }
    std::cout << "  arbitration property held on " << cases << " random sessions\n";
    EXPECT(cases == 200);
}

// ---------------------------------------------------------------------------
// Fuzzing: arbitrary bytes must never crash or read out of bounds
// ---------------------------------------------------------------------------

void test_fuzz_decode_random_bytes() {
    SplitMix64 rng{1};
    const char known[] = {'S', 'R', 'H', 'A', 'F', 'E', 'C', 'X', 'D', 'U', 'P', 'Q', 'B'};
    int ok = 0;
    int round_trips = 0;
    bool status_as_specified = true;
    for (int i = 0; i < 20000; ++i) {
        const std::size_t n = static_cast<std::size_t>(rng.below(48));
        std::vector<std::uint8_t> buf(n);
        for (auto& b : buf) b = static_cast<std::uint8_t>(rng.next());
        if (n > 0 && rng.below(2) == 0) buf[0] = static_cast<std::uint8_t>(known[rng.below(sizeof(known))]);
        DecodedMessage m;
        // Decode from an exact-size heap buffer so ASan catches any overread.
        const DecodeStatus st = decode(n ? buf.data() : nullptr, n, m);
        // Expected status from the spec lengths (pinned to the spec in test_message_lengths_match_spec): a buffer
        // decodes exactly when its type is known and it holds at least that many bytes.
        const std::size_t spec_len = n == 0 ? 0 : message_length(static_cast<char>(buf[0]));
        const DecodeStatus expected = n == 0           ? DecodeStatus::Empty
                                      : spec_len == 0  ? DecodeStatus::UnknownType
                                      : n < spec_len   ? DecodeStatus::Truncated
                                                       : DecodeStatus::Ok;
        status_as_specified = status_as_specified && st == expected;
        if (st == DecodeStatus::Ok) {
            ++ok;
            const std::size_t len = message_length(m.type);
            EXPECT(len <= n);
            const bool full = m.type != 'R' && m.type != 'H' && m.type != 'Q' && m.type != 'B';
            if (full) {
                const auto w = encode(m);
                EXPECT(std::equal(w.begin(), w.end(), buf.begin()));
                ++round_trips;
            }
        }
    }
    std::cout << "  20000 random buffers: " << ok << " decoded, " << round_trips << " re-encoded byte for byte\n";
    EXPECT(status_as_specified);
    EXPECT(ok > 1000 && round_trips > 1000);  // the property was exercised, not vacuously true
}

void test_fuzz_packets_into_arbitrator_and_book() {
    SplitMix64 rng{99};
    DecodedMessage a;
    a.type = 'A';
    a.order_ref = 1;
    a.side = 'B';
    a.shares = 100;
    a.price = 1'000'000;
    const auto valid = build_mold_packet(kSession, 1, {encode(a), encode(a)});
    BookBuilder book;
    std::uint64_t last_seq = 0;
    bool monotone = true;
    LineArbitrator arb(
        [&](std::uint64_t s, const std::uint8_t* d, std::size_t len) {
            monotone = monotone && s > last_seq;
            last_seq = s;
            DecodedMessage m;
            if (decode(d, len, m) == DecodeStatus::Ok) book.apply(m);  // any status is fine, no UB allowed
        },
        1, 64);
    for (int i = 0; i < 5000; ++i) {
        std::vector<std::uint8_t> pkt = valid;
        const std::uint64_t mode = rng.below(4);
        if (mode == 0) {  // flip random bytes
            for (int k = 0; k < 3; ++k) pkt[static_cast<std::size_t>(rng.below(pkt.size()))] ^= static_cast<std::uint8_t>(rng.next());
        } else if (mode == 1) {  // truncate
            pkt.resize(static_cast<std::size_t>(rng.below(pkt.size())));
        } else if (mode == 2) {  // pure noise
            pkt.resize(static_cast<std::size_t>(rng.below(80)));
            for (auto& b : pkt) b = static_cast<std::uint8_t>(rng.next());
        } else {  // valid framing, random sequence number
            write_be(pkt.data() + 10, 1 + rng.below(200), 8);
        }
        // Copy to an exact-size heap block so overreads are caught.
        std::vector<std::uint8_t> exact(pkt.begin(), pkt.end());
        arb.on_packet(exact.empty() ? nullptr : exact.data(), exact.size());
    }
    std::cout << "  " << arb.stats().packets << " mutated packets fed to the arbitrator, delivery stayed monotone\n";
    EXPECT(monotone);
    EXPECT(arb.stats().packets == 5000);
}

void test_mt19937_is_portable_but_distributions_are_not_required_to_be() {
    // [rand.predef]: the 10000th output of a default-constructed mt19937 is
    // 4123659995 on every conforming implementation.
    std::mt19937 g;
    std::uint32_t v = 0;
    for (int i = 0; i < 10000; ++i) v = static_cast<std::uint32_t>(g());
    std::cout << "  mt19937 10000th output " << v << "\n";
    EXPECT(v == 4123659995u);
}

}  // namespace

int main() {
    RUN_TEST(test_message_lengths_match_spec);
    RUN_TEST(test_add_order_offsets_are_big_endian);
    RUN_TEST(test_replace_and_executed_with_price_offsets);
    RUN_TEST(test_lengths_equal_sum_of_spec_field_widths);
    RUN_TEST(test_last_field_ends_at_spec_length);
    RUN_TEST(test_round_trip_every_decoded_type);
    RUN_TEST(test_truncated_unknown_and_empty);
    RUN_TEST(test_mold_heartbeat_and_end_of_session);
    RUN_TEST(test_mold_malformed_delivers_nothing);
    RUN_TEST(test_mold_packet_and_request_offsets);
    RUN_TEST(test_heartbeat_reveals_tail_gap);
    RUN_TEST(test_wrong_session_rejected);
    RUN_TEST(test_overlapping_packet_delivers_only_new_messages);
    RUN_TEST(test_card_overlap_8_to_12_while_expecting_10);
    RUN_TEST(test_longer_copy_of_buffered_packet_is_kept);
    RUN_TEST(test_full_reorder_buffer_is_reported);
    RUN_TEST(test_book_rejects_inconsistent_updates);
    RUN_TEST(test_zero_share_add_never_rests);
    RUN_TEST(test_card_cumulative_deltas_300_e100_x150);
    RUN_TEST(test_replace_keeps_side_and_locate);
    RUN_TEST(test_sequence_overflow_is_malformed);
    RUN_TEST(test_property_arbitration_rebuilds_reference_book);
    RUN_TEST(test_fuzz_decode_random_bytes);
    RUN_TEST(test_fuzz_packets_into_arbitrator_and_book);
    RUN_TEST(test_mt19937_is_portable_but_distributions_are_not_required_to_be);

    std::cout << "\n" << (g_total - g_failures) << "/" << g_total << " assertions passed" << std::endl;
    return g_failures == 0 ? 0 : 1;
}
