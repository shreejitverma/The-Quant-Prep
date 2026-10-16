// Demo for 12-Quant-Development note 08 (Market Data Feed Handlers and
// Protocols): a scripted ITCH 5.0 session over MoldUDP64, published on two
// redundant lines A and B with different packet losses, merged by the
// LineArbitrator, one gap that neither line fills recovered with a
// MoldUDP64 retransmission request, and the book rebuilt by BookBuilder.
// Every printed number is asserted; the final book is also checked against
// a book built from the loss-free stream.
//
// Build: clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror -pthread
//        -o itch50_feed_handler itch50_feed_handler.cpp

#include "itch50_feed_handler.hpp"

#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>

using namespace itch50;

namespace {

int g_failures = 0;

void check(bool ok, const char* what) {
    if (!ok) {
        ++g_failures;
        std::fprintf(stderr, "ASSERTION FAILED: %s\n", what);
    }
}

constexpr std::uint16_t kLocate = 1;
constexpr std::uint64_t kMsAfterOpen = 34'200'000'000'000ull;  // 09:30:00 in ns since midnight

DecodedMessage base(char type, std::uint64_t t_ns) {
    DecodedMessage m;
    m.type = type;
    m.stock_locate = type == 'S' ? 0 : kLocate;  // spec: locate is always 0 on S
    m.timestamp_ns = t_ns;
    return m;
}

DecodedMessage add(std::uint64_t t, std::uint64_t ref, char side, std::uint32_t shares, std::uint32_t price) {
    DecodedMessage m = base('A', t);
    m.order_ref = ref;
    m.side = side;
    m.shares = shares;
    m.price = price;
    m.stock = {'Q', 'P', 'D', 'E', 'M', 'O', ' ', ' '};
    return m;
}

double px(std::uint32_t price4) { return static_cast<double>(price4) / 10000.0; }

}  // namespace

int main() {
    // ---- 1. The scripted session: 16 messages, sequence numbers 1..16 ----
    std::vector<DecodedMessage> script;
    std::uint64_t t = kMsAfterOpen;
    {
        DecodedMessage s = base('S', t);
        s.event_code = 'O';  // Start of Messages
        script.push_back(s);
    }
    script.push_back(add(t += 1000, 1, 'B', 300, 1'000'000));  // 100.0000
    script.push_back(add(t += 1000, 2, 'B', 200, 999'900));    //  99.9900
    script.push_back(add(t += 1000, 3, 'S', 400, 1'000'200));  // 100.0200
    {
        DecodedMessage f = add(t += 1000, 4, 'S', 100, 1'000'100);  // 100.0100, attributed
        f.type = 'F';
        f.attribution = {'Q', 'P', 'M', 'M'};
        script.push_back(f);
    }
    script.push_back(add(t += 1000, 5, 'B', 500, 1'000'000));
    {
        DecodedMessage e = base('E', t += 1000);  // order 4 fully executed
        e.order_ref = 4;
        e.shares = 100;
        e.match_number = 1;
        script.push_back(e);
    }
    {
        DecodedMessage x = base('X', t += 1000);  // order 3 partially canceled
        x.order_ref = 3;
        x.shares = 150;
        script.push_back(x);
    }
    {
        DecodedMessage u = base('U', t += 1000);  // order 2 replaced by 6
        u.order_ref = 2;
        u.new_order_ref = 6;
        u.shares = 250;
        u.price = 1'000'100;
        script.push_back(u);
    }
    {
        DecodedMessage c = base('C', t += 1000);  // order 1 executed at another price
        c.order_ref = 1;
        c.shares = 100;
        c.match_number = 2;
        c.printable = 'Y';
        c.price = 1'000'050;
        script.push_back(c);
    }
    {
        DecodedMessage p = base('P', t += 1000);  // non-displayed match: no book effect
        p.side = 'B';
        p.shares = 200;
        p.stock = {'Q', 'P', 'D', 'E', 'M', 'O', ' ', ' '};
        p.price = 1'000'150;
        p.match_number = 3;
        script.push_back(p);
    }
    {
        DecodedMessage d = base('D', t += 1000);
        d.order_ref = 5;
        script.push_back(d);
    }
    script.push_back(add(t += 1000, 7, 'S', 300, 1'000'200));
    {
        DecodedMessage e = base('E', t += 1000);
        e.order_ref = 6;
        e.shares = 50;
        e.match_number = 4;
        script.push_back(e);
    }
    script.push_back(add(t += 1000, 8, 'B', 100, 999'900));
    {
        DecodedMessage x = base('X', t += 1000);
        x.order_ref = 7;
        x.shares = 100;
        script.push_back(x);
    }
    const std::uint64_t n_msgs = script.size();

    // Encode once; message i has sequence number i + 1.
    std::vector<std::vector<std::uint8_t>> wire;
    std::uint64_t wire_bytes = 0;
    for (const auto& m : script) {
        wire.push_back(encode(m));
        wire_bytes += wire.back().size();
    }

    // ---- 2. Packetise: packets of at most 3 messages ----
    const Session session = {'Q', 'P', 'D', 'E', 'M', 'O', '0', '0', '0', '1'};
    const std::vector<std::pair<std::uint64_t, std::uint64_t>> packet_ranges = {
        {1, 3}, {4, 5}, {6, 8}, {9, 10}, {11, 13}, {14, 16}};  // inclusive sequence ranges
    std::vector<std::vector<std::uint8_t>> packets;
    for (const auto& [first, last] : packet_ranges) {
        std::vector<std::vector<std::uint8_t>> body(wire.begin() + static_cast<long>(first - 1),
                                                    wire.begin() + static_cast<long>(last));
        packets.push_back(build_mold_packet(session, first, body));
    }
    const auto heartbeat = build_mold_packet(session, n_msgs + 1, {}, kMoldHeartbeat);
    const auto end_of_session = build_mold_packet(session, n_msgs + 1, {}, kMoldEndOfSession);

    // ---- 3. Reference book from the loss-free stream ----
    BookBuilder reference;
    for (const auto& m : script) {
        const ApplyStatus st = reference.apply(m);
        check(st == ApplyStatus::Ok || st == ApplyStatus::Ignored, "reference apply");
    }

    // ---- 4. Live: A loses packet 2, B loses packet 3, both lose packet 5 ----
    BookBuilder book;
    std::vector<std::uint64_t> delivered_seqs;
    std::uint64_t decode_errors = 0;
    LineArbitrator arb([&](std::uint64_t seq, const std::uint8_t* data, std::size_t len) {
        DecodedMessage m;
        if (decode(data, len, m) != DecodeStatus::Ok) {
            ++decode_errors;
            return;
        }
        delivered_seqs.push_back(seq);
        const ApplyStatus st = book.apply(m);
        if (st != ApplyStatus::Ok && st != ApplyStatus::Ignored) ++decode_errors;
    });

    // Arrival order on the NIC: (line, packet index). B trails A.
    struct Arrival {
        char line;
        int packet;  // index into packets, -1 heartbeat, -2 end of session
    };
    const std::vector<Arrival> arrivals = {
        {'A', 0}, {'B', 0}, {'A', 2}, {'B', 1}, {'A', 3}, {'B', 3},
        {'A', 5}, {'B', 5}, {'A', -1}, {'B', -1}, {'A', -2}, {'B', -2}};
    std::uint64_t from_a = 0;
    std::uint64_t from_b = 0;
    const char* action_names[] = {"delivered", "duplicate", "buffered", "heartbeat", "end of session", "malformed",
                                  "wrong session"};
    std::vector<PacketAction> actions;
    std::vector<std::uint64_t> delivered_per_arrival;
    std::vector<std::uint64_t> next_after;
    std::printf("arrival  packet      action          delivered  next expected\n");
    for (const auto& a : arrivals) {
        const auto& pkt = a.packet == -1 ? heartbeat : a.packet == -2 ? end_of_session : packets[static_cast<std::size_t>(a.packet)];
        const std::uint64_t before = arb.stats().delivered_messages;
        const PacketAction act = arb.on_packet(pkt.data(), pkt.size());
        const std::uint64_t got = arb.stats().delivered_messages - before;
        (a.line == 'A' ? from_a : from_b) += got;
        actions.push_back(act);
        delivered_per_arrival.push_back(got);
        next_after.push_back(arb.next_expected());
        char label[32];
        if (a.packet >= 0) {
            const auto& r = packet_ranges[static_cast<std::size_t>(a.packet)];
            std::snprintf(label, sizeof(label), "%llu..%llu", static_cast<unsigned long long>(r.first),
                          static_cast<unsigned long long>(r.second));
        } else {
            std::snprintf(label, sizeof(label), "%s", a.packet == -1 ? "HB 17" : "EOS 17");
        }
        std::printf("   %c     %-10s  %-14s  %9llu  %13llu\n", a.line, label, action_names[static_cast<int>(act)],
                    static_cast<unsigned long long>(got), static_cast<unsigned long long>(arb.next_expected()));
    }
    using PA = PacketAction;
    check(actions == std::vector<PacketAction>{PA::Delivered, PA::Duplicate, PA::Buffered, PA::Delivered,
                                               PA::Delivered, PA::Duplicate, PA::Buffered, PA::Duplicate,
                                               PA::Heartbeat, PA::Heartbeat, PA::EndOfSession, PA::EndOfSession},
          "arrival actions");
    check(delivered_per_arrival == std::vector<std::uint64_t>{3, 0, 0, 5, 2, 0, 0, 0, 0, 0, 0, 0},
          "messages delivered per arrival");
    check(next_after == std::vector<std::uint64_t>{4, 4, 4, 9, 11, 11, 11, 11, 11, 11, 11, 11},
          "next expected sequence after each arrival");

    // ---- 5. Neither line had 11..13: request a retransmission ----
    const auto gap = arb.missing();
    check(gap.has_value(), "a gap remains after both lines");
    const std::uint64_t gap_first = gap ? gap->first : 0;
    const std::uint64_t gap_size = gap ? gap->size() : 0;
    const auto request = build_mold_request(session, gap_first, static_cast<std::uint16_t>(gap_size));
    // The re-request server answers with a normal downstream packet built
    // from its message store, unicast to the requesting socket.
    MoldHeader req_hdr;
    const bool req_ok = parse_mold_request(request.data(), request.size(), req_hdr);
    check(req_ok && req_hdr.session == session, "server parses the 20-byte request");
    std::vector<std::vector<std::uint8_t>> resend(wire.begin() + static_cast<long>(req_hdr.sequence - 1),
                                                  wire.begin() + static_cast<long>(req_hdr.sequence - 1 + req_hdr.count));
    const auto retrans = build_mold_packet(session, req_hdr.sequence, resend);
    const std::uint64_t before_rt = arb.stats().delivered_messages;
    arb.on_packet(retrans.data(), retrans.size());
    const std::uint64_t from_retrans = arb.stats().delivered_messages - before_rt;

    // ---- 6. Report and assert ----
    const ArbStats& s = arb.stats();
    const TopOfBook top = book.top(kLocate);
    const TopOfBook ref_top = reference.top(kLocate);

    std::printf("ITCH 5.0 over MoldUDP64, scripted session\n");
    std::printf("messages in session          %llu\n", static_cast<unsigned long long>(n_msgs));
    std::printf("ITCH payload bytes           %llu\n", static_cast<unsigned long long>(wire_bytes));
    std::printf("packets on each line         %zu (+ heartbeat + end of session)\n", packets.size());
    std::printf("gaps detected                %llu\n", static_cast<unsigned long long>(s.gaps_detected));
    std::printf("packets buffered ahead of gap %llu\n", static_cast<unsigned long long>(s.buffered_packets));
    std::printf("duplicate packets dropped    %llu\n", static_cast<unsigned long long>(s.duplicate_packets));
    std::printf("messages first seen on A     %llu\n", static_cast<unsigned long long>(from_a));
    std::printf("messages first seen on B     %llu\n", static_cast<unsigned long long>(from_b));
    std::printf("retransmission request       seq %llu count %llu\n", static_cast<unsigned long long>(gap_first),
                static_cast<unsigned long long>(gap_size));
    std::printf("messages from retransmission %llu\n", static_cast<unsigned long long>(from_retrans));
    std::printf("messages delivered in order  %llu\n", static_cast<unsigned long long>(s.delivered_messages));
    std::printf("best bid  %.4f x %llu\n", px(top.bid_price), static_cast<unsigned long long>(top.bid_shares));
    std::printf("best ask  %.4f x %llu\n", px(top.ask_price), static_cast<unsigned long long>(top.ask_shares));
    std::printf("bid levels %zu, ask levels %zu, live orders %zu\n", book.levels(kLocate, 'B'),
                book.levels(kLocate, 'S'), book.live_orders());

    for (const auto& [p, q] : book.depth(kLocate, 'B')) std::printf("  bid level %.4f x %llu\n", px(p), static_cast<unsigned long long>(q));
    for (const auto& [p, q] : book.depth(kLocate, 'S')) std::printf("  ask level %.4f x %llu\n", px(p), static_cast<unsigned long long>(q));
    using Levels = std::vector<std::pair<std::uint32_t, std::uint64_t>>;
    check(book.depth(kLocate, 'B') == Levels{{1'000'100, 200}, {1'000'000, 200}, {999'900, 100}}, "bid depth");
    check(book.depth(kLocate, 'S') == Levels{{1'000'200, 450}}, "ask depth");
    check(n_msgs == 16, "16 messages");
    check(wire_bytes == 12 + 36 * 6 + 40 + 31 * 2 + 23 * 2 + 35 + 36 + 44 + 19, "payload bytes from spec lengths");
    check(wire_bytes == 510, "510 payload bytes");
    check(packets.size() == 6, "6 packets");
    check(s.gaps_detected == 2, "two gaps: 4..5 (filled by B) and 11..13 (retransmitted)");
    check(s.buffered_packets == 2, "packets 3 and 6 were buffered");
    check(s.duplicate_packets == 3, "B copies of packets 1, 4 and 6 dropped");
    check(from_a == 5, "A delivered 1..3 and 9..10");
    check(from_b == 5, "B delivered 4..5 then drained 6..8");
    check(gap_first == 11 && gap_size == 3, "request 11 for 3");
    check(from_retrans == 6, "retransmission delivers 11..13 and drains 14..16");
    check(s.delivered_messages == 16, "every message delivered once");
    check(decode_errors == 0, "no decode or apply errors");
    bool in_order = delivered_seqs.size() == n_msgs;
    for (std::size_t i = 0; in_order && i < delivered_seqs.size(); ++i) in_order = delivered_seqs[i] == i + 1;
    check(in_order, "sequence numbers delivered exactly 1..16 in order");
    check(!arb.missing().has_value(), "no gap left");
    check(top.has_bid && top.bid_price == 1'000'100 && top.bid_shares == 200, "best bid 100.0100 x 200");
    check(top.has_ask && top.ask_price == 1'000'200 && top.ask_shares == 450, "best ask 100.0200 x 450");
    check(book.levels(kLocate, 'B') == 3 && book.levels(kLocate, 'S') == 1, "3 bid levels, 1 ask level");
    check(book.live_orders() == 5, "orders 1 3 6 7 8 live");
    check(book.depth(kLocate, 'B') == reference.depth(kLocate, 'B'), "bids equal loss-free reference");
    check(book.depth(kLocate, 'S') == reference.depth(kLocate, 'S'), "asks equal loss-free reference");
    check(ref_top.bid_price == top.bid_price && ref_top.ask_shares == top.ask_shares, "top equals reference");

    // ---- 7. One Add Order on the wire, byte by byte ----
    char hex[2 * 36 + 1] = {};
    for (std::size_t i = 0; i < wire[1].size(); ++i) {
        std::snprintf(hex + 2 * i, 3, "%02X", wire[1][i]);
    }
    std::printf("Add Order seq 2 (36 bytes): %s\n", hex);
    check(std::string(hex) ==
              "41"                  // 'A'
              "0001"                // Stock Locate 1
              "0000"                // Tracking Number 0
              "1F1ACED9F3E8"        // Timestamp 34,200,000,001,000 ns (09:30:00.000001)
              "0000000000000001"    // Order Reference Number 1
              "42"                  // 'B'
              "0000012C"            // Shares 300
              "515044454D4F2020"    // Stock "QPDEMO  "
              "000F4240",           // Price(4) 1,000,000 = 100.0000
          "Add Order bytes");
    DecodedMessage back;
    check(decode(wire[1].data(), wire[1].size(), back) == DecodeStatus::Ok, "decodes");
    std::printf("decoded: locate %u, timestamp %llu ns, ref %llu, side %c, shares %u, price %.4f\n", back.stock_locate,
                static_cast<unsigned long long>(back.timestamp_ns), static_cast<unsigned long long>(back.order_ref),
                back.side, back.shares, px(back.price));
    check(back.stock_locate == 1 && back.timestamp_ns == 34'200'000'001'000ull && back.order_ref == 1 &&
              back.side == 'B' && back.shares == 300 && back.price == 1'000'000,
          "decoded fields");

    // ---- 8. Format arithmetic quoted in the note ----
    const std::uint64_t ns_per_day = 86'400ull * 1'000'000'000ull;
    const std::uint64_t max48 = (1ull << 48) - 1;
    int bits_needed = 0;
    while ((1ull << bits_needed) <= ns_per_day) ++bits_needed;
    std::printf("ns per day %llu needs %d bits; 48-bit max %llu ns = %.1f hours\n",
                static_cast<unsigned long long>(ns_per_day), bits_needed, static_cast<unsigned long long>(max48),
                static_cast<double>(max48) / 3.6e12);
    check(bits_needed == 47, "a day of nanoseconds needs 47 bits");
    check(max48 > ns_per_day, "48 bits cover a day");
    check(std::abs(static_cast<double>(max48) / 3.6e12 - 78.2) < 0.05, "48 bits cover 78.2 hours");
    std::printf("Price(4) maximum 0x%08X = %.4f\n", kMaxPrice4, px(kMaxPrice4));
    check(kMaxPrice4 == 0x77359400u, "spec maximum price in hex");

    // MoldUDP64 payload efficiency for k Add Orders (36 bytes) per packet:
    // 36k / (20 + 38k). Wire: + UDP 8 + IPv4 20 + Ethernet 14 header + 4 FCS
    // + 8 preamble + 12 inter-frame gap = 66 bytes per frame.
    const double eff1 = 36.0 / (20.0 + 38.0);
    const double eff10 = 360.0 / (20.0 + 380.0);
    const double frame1 = 20.0 + 38.0 + 66.0;
    const double pps_10g = 10e9 / (frame1 * 8.0);
    std::printf("Mold efficiency, 1 add/packet %.4f, 10 adds/packet %.4f\n", eff1, eff10);
    std::printf("one add per frame: %.0f bytes on the wire, %.2f million packets/s at 10 Gb/s\n", frame1,
                pps_10g / 1e6);
    check(std::abs(eff1 - 0.6207) < 5e-5, "eff1");
    check(std::abs(eff10 - 0.9) < 1e-12, "eff10");
    check(frame1 == 124.0, "124 bytes per frame");
    check(std::abs(pps_10g / 1e6 - 10.08) < 5e-3, "10.08 Mpps");

    if (g_failures != 0) {
        std::fprintf(stderr, "%d assertion(s) failed\n", g_failures);
        return 1;
    }
    std::printf("all assertions passed\n");
    return 0;
}
