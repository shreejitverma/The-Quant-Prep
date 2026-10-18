// Header-only feed handler building blocks for Nasdaq TotalView-ITCH 5.0
// carried over MoldUDP64, used by 12-Quant-Development note 08
// (Market Data Feed Handlers and Protocols).
//
// Sources (layouts copied field by field, offsets and lengths in bytes):
//   * Nasdaq TotalView-ITCH 5.0 Interface Specification, version 5.0,
//     03/06/2015 (12-Quant-Development/protocol-specs/NASDAQ-TotalView-ITCH-5.pdf).
//     All integers are big-endian and unsigned; prices are Price(4), an
//     integer with 4 implied decimals; timestamps are 6-byte nanoseconds
//     since midnight.
//   * Nasdaq MoldUDP64 Protocol Specification V1.00: a 20-byte downstream
//     header (Session 10, Sequence Number 8, Message Count 2), then Message
//     Blocks of a 2-byte Message Length followed by the message data.
//     Message Count 0 is a heartbeat and 0xFFFF is end of session; both
//     carry the next expected sequence number.
//
// Components:
//   decode()/encode()       one ITCH message <-> DecodedMessage
//   parse_mold_packet()     validate a whole MoldUDP64 packet, then deliver
//   LineArbitrator          merge lines A and B by sequence number, buffer
//                           packets that arrive ahead of a gap, report gaps
//   BookBuilder             order-reference keyed book with per-price levels
//
// Teaching code: correct and bounds-checked, not tuned. A production
// handler replaces std::map / std::vector copies with preallocated arrays
// indexed by stock locate and price, and an open-addressing order table.

#ifndef QUANT_PREP_ITCH50_FEED_HANDLER_HPP
#define QUANT_PREP_ITCH50_FEED_HANDLER_HPP

#include <array>
#include <cstddef>
#include <cstdint>
#include <functional>
#include <limits>
#include <map>
#include <optional>
#include <unordered_map>
#include <utility>
#include <vector>

namespace itch50 {

// ---------------------------------------------------------------------------
// Big-endian primitives. Byte-wise shifts: no alignment or aliasing UB and
// no dependence on host endianness.
// ---------------------------------------------------------------------------

inline std::uint64_t read_be(const std::uint8_t* p, std::size_t width) {
    std::uint64_t v = 0;
    for (std::size_t i = 0; i < width; ++i) {
        v = (v << 8) | p[i];
    }
    return v;
}

inline void write_be(std::uint8_t* p, std::uint64_t v, std::size_t width) {
    for (std::size_t i = 0; i < width; ++i) {
        p[width - 1 - i] = static_cast<std::uint8_t>(v & 0xFFu);
        v >>= 8;
    }
}

// Price(4): 200,000.0000 is the documented maximum (0x77359400).
inline constexpr std::uint32_t kMaxPrice4 = 2'000'000'000u;

// Spec lengths for every ITCH 5.0 message type this file knows about.
// Returns 0 for an unknown type.
inline constexpr std::size_t message_length(char type) {
    switch (type) {
        case 'S': return 12;  // System Event
        case 'R': return 39;  // Stock Directory
        case 'H': return 25;  // Stock Trading Action
        case 'A': return 36;  // Add Order, no MPID attribution
        case 'F': return 40;  // Add Order with MPID attribution
        case 'E': return 31;  // Order Executed
        case 'C': return 36;  // Order Executed With Price
        case 'X': return 23;  // Order Cancel
        case 'D': return 19;  // Order Delete
        case 'U': return 35;  // Order Replace
        case 'P': return 44;  // Trade (non-cross)
        case 'Q': return 40;  // Cross Trade
        case 'B': return 19;  // Broken Trade
        default: return 0;
    }
}

inline constexpr std::size_t kMaxMessageLength = 44;  // 'P', the longest message above
static_assert(message_length('P') == kMaxMessageLength);

// Flat decoded form; fields not used by a type stay zero.
struct DecodedMessage {
    char type = 0;
    std::uint16_t stock_locate = 0;      // offset 1, length 2
    std::uint16_t tracking_number = 0;   // offset 3, length 2
    std::uint64_t timestamp_ns = 0;      // offset 5, length 6
    std::uint64_t order_ref = 0;         // A F E C X D P, original ref for U
    std::uint64_t new_order_ref = 0;     // U only
    std::uint64_t match_number = 0;      // E C P
    std::uint32_t shares = 0;            // A F E C X U P (executed or canceled for E C X)
    std::uint32_t price = 0;             // A F U P, execution price for C
    char side = 0;                       // 'B' or 'S' for A F P
    char printable = 0;                  // C only
    char event_code = 0;                 // S only
    std::array<char, 8> stock{};         // A F P
    std::array<char, 4> attribution{};   // F only
};

enum class DecodeStatus { Ok, Empty, UnknownType, Truncated };

// Decode one ITCH message of n bytes. n may exceed the spec length (trailing
// bytes are ignored, which tolerates appended fields); n below it is
// Truncated. `out` is written only on Ok. Types R, H, Q and B decode the
// common header only.
inline DecodeStatus decode(const std::uint8_t* p, std::size_t n, DecodedMessage& out) {
    if (p == nullptr || n == 0) return DecodeStatus::Empty;
    const char type = static_cast<char>(p[0]);
    const std::size_t need = message_length(type);
    if (need == 0) return DecodeStatus::UnknownType;
    if (n < need) return DecodeStatus::Truncated;

    DecodedMessage m;
    m.type = type;
    m.stock_locate = static_cast<std::uint16_t>(read_be(p + 1, 2));
    m.tracking_number = static_cast<std::uint16_t>(read_be(p + 3, 2));
    m.timestamp_ns = read_be(p + 5, 6);
    auto copy8 = [&](std::size_t off) {
        for (std::size_t i = 0; i < 8; ++i) m.stock[i] = static_cast<char>(p[off + i]);
    };
    switch (type) {
        case 'S':
            m.event_code = static_cast<char>(p[11]);
            break;
        case 'A':
        case 'F':
            m.order_ref = read_be(p + 11, 8);
            m.side = static_cast<char>(p[19]);
            m.shares = static_cast<std::uint32_t>(read_be(p + 20, 4));
            copy8(24);
            m.price = static_cast<std::uint32_t>(read_be(p + 32, 4));
            if (type == 'F') {
                for (std::size_t i = 0; i < 4; ++i) m.attribution[i] = static_cast<char>(p[36 + i]);
            }
            break;
        case 'E':
            m.order_ref = read_be(p + 11, 8);
            m.shares = static_cast<std::uint32_t>(read_be(p + 19, 4));
            m.match_number = read_be(p + 23, 8);
            break;
        case 'C':
            m.order_ref = read_be(p + 11, 8);
            m.shares = static_cast<std::uint32_t>(read_be(p + 19, 4));
            m.match_number = read_be(p + 23, 8);
            m.printable = static_cast<char>(p[31]);
            m.price = static_cast<std::uint32_t>(read_be(p + 32, 4));
            break;
        case 'X':
            m.order_ref = read_be(p + 11, 8);
            m.shares = static_cast<std::uint32_t>(read_be(p + 19, 4));
            break;
        case 'D':
            m.order_ref = read_be(p + 11, 8);
            break;
        case 'U':
            m.order_ref = read_be(p + 11, 8);
            m.new_order_ref = read_be(p + 19, 8);
            m.shares = static_cast<std::uint32_t>(read_be(p + 27, 4));
            m.price = static_cast<std::uint32_t>(read_be(p + 31, 4));
            break;
        case 'P':
            m.order_ref = read_be(p + 11, 8);
            m.side = static_cast<char>(p[19]);
            m.shares = static_cast<std::uint32_t>(read_be(p + 20, 4));
            copy8(24);
            m.price = static_cast<std::uint32_t>(read_be(p + 32, 4));
            m.match_number = read_be(p + 36, 8);
            break;
        default:
            break;  // R H Q B: header only
    }
    out = m;
    return DecodeStatus::Ok;
}

// Encode m into out (capacity cap). Returns bytes written, or 0 if the type
// is unknown or cap is too small. Unused bytes of R/H/Q/B are zero.
inline std::size_t encode(const DecodedMessage& m, std::uint8_t* out, std::size_t cap) {
    const std::size_t len = message_length(m.type);
    if (len == 0 || out == nullptr || cap < len) return 0;
    for (std::size_t i = 0; i < len; ++i) out[i] = 0;
    out[0] = static_cast<std::uint8_t>(m.type);
    write_be(out + 1, m.stock_locate, 2);
    write_be(out + 3, m.tracking_number, 2);
    write_be(out + 5, m.timestamp_ns, 6);
    auto put8 = [&](std::size_t off) {
        for (std::size_t i = 0; i < 8; ++i) out[off + i] = static_cast<std::uint8_t>(m.stock[i]);
    };
    switch (m.type) {
        case 'S':
            out[11] = static_cast<std::uint8_t>(m.event_code);
            break;
        case 'A':
        case 'F':
            write_be(out + 11, m.order_ref, 8);
            out[19] = static_cast<std::uint8_t>(m.side);
            write_be(out + 20, m.shares, 4);
            put8(24);
            write_be(out + 32, m.price, 4);
            if (m.type == 'F') {
                for (std::size_t i = 0; i < 4; ++i) out[36 + i] = static_cast<std::uint8_t>(m.attribution[i]);
            }
            break;
        case 'E':
            write_be(out + 11, m.order_ref, 8);
            write_be(out + 19, m.shares, 4);
            write_be(out + 23, m.match_number, 8);
            break;
        case 'C':
            write_be(out + 11, m.order_ref, 8);
            write_be(out + 19, m.shares, 4);
            write_be(out + 23, m.match_number, 8);
            out[31] = static_cast<std::uint8_t>(m.printable);
            write_be(out + 32, m.price, 4);
            break;
        case 'X':
            write_be(out + 11, m.order_ref, 8);
            write_be(out + 19, m.shares, 4);
            break;
        case 'D':
            write_be(out + 11, m.order_ref, 8);
            break;
        case 'U':
            write_be(out + 11, m.order_ref, 8);
            write_be(out + 19, m.new_order_ref, 8);
            write_be(out + 27, m.shares, 4);
            write_be(out + 31, m.price, 4);
            break;
        case 'P':
            write_be(out + 11, m.order_ref, 8);
            out[19] = static_cast<std::uint8_t>(m.side);
            write_be(out + 20, m.shares, 4);
            put8(24);
            write_be(out + 32, m.price, 4);
            write_be(out + 36, m.match_number, 8);
            break;
        default:
            break;
    }
    return len;
}

inline std::vector<std::uint8_t> encode(const DecodedMessage& m) {
    std::array<std::uint8_t, kMaxMessageLength> buf{};
    const std::size_t len = encode(m, buf.data(), buf.size());
    return std::vector<std::uint8_t>(buf.begin(), buf.begin() + static_cast<std::ptrdiff_t>(len));
}

// ---------------------------------------------------------------------------
// MoldUDP64
// ---------------------------------------------------------------------------

inline constexpr std::size_t kMoldHeaderSize = 20;
inline constexpr std::uint16_t kMoldHeartbeat = 0;
inline constexpr std::uint16_t kMoldEndOfSession = 0xFFFF;

using Session = std::array<char, 10>;

struct MoldHeader {
    Session session{};
    std::uint64_t sequence = 0;  // sequence number of the first message
    std::uint16_t count = 0;     // message count, 0 heartbeat, 0xFFFF end
};

enum class MoldStatus { Ok, TooShort, BadBlock, TrailingBytes };

// Validate the whole packet first, then call deliver(seq, data, len) for
// each message block in order. A malformed packet delivers nothing, so a
// consumer never sees half a packet.
template <class Deliver>
MoldStatus parse_mold_packet(const std::uint8_t* p, std::size_t n, MoldHeader& hdr, Deliver&& deliver) {
    if (p == nullptr || n < kMoldHeaderSize) return MoldStatus::TooShort;
    MoldHeader h;
    for (std::size_t i = 0; i < 10; ++i) h.session[i] = static_cast<char>(p[i]);
    h.sequence = read_be(p + 10, 8);
    h.count = static_cast<std::uint16_t>(read_be(p + 18, 2));
    const std::size_t blocks = (h.count == kMoldEndOfSession) ? 0 : h.count;
    // Pass 1: every block must fit exactly.
    std::size_t off = kMoldHeaderSize;
    for (std::size_t b = 0; b < blocks; ++b) {
        if (n - off < 2) return MoldStatus::BadBlock;
        const std::size_t len = static_cast<std::size_t>(read_be(p + off, 2));
        if (n - off - 2 < len) return MoldStatus::BadBlock;
        off += 2 + len;
    }
    if (off != n) return MoldStatus::TrailingBytes;
    hdr = h;
    // Pass 2: deliver.
    off = kMoldHeaderSize;
    for (std::size_t b = 0; b < blocks; ++b) {
        const std::size_t len = static_cast<std::size_t>(read_be(p + off, 2));
        deliver(h.sequence + b, p + off + 2, len);
        off += 2 + len;
    }
    return MoldStatus::Ok;
}

inline std::vector<std::uint8_t> build_mold_packet(const Session& session, std::uint64_t first_seq,
                                                   const std::vector<std::vector<std::uint8_t>>& msgs,
                                                   std::uint16_t count_override = 1) {
    // count_override is only consulted for an empty msgs list: pass
    // kMoldHeartbeat or kMoldEndOfSession.
    std::size_t size = kMoldHeaderSize;
    for (const auto& m : msgs) size += 2 + m.size();
    std::vector<std::uint8_t> out(size);
    for (std::size_t i = 0; i < 10; ++i) out[i] = static_cast<std::uint8_t>(session[i]);
    write_be(out.data() + 10, first_seq, 8);
    const std::uint16_t count = msgs.empty() ? count_override : static_cast<std::uint16_t>(msgs.size());
    write_be(out.data() + 18, count, 2);
    std::size_t off = kMoldHeaderSize;
    for (const auto& m : msgs) {
        write_be(out.data() + off, m.size(), 2);
        for (std::size_t i = 0; i < m.size(); ++i) out[off + 2 + i] = m[i];
        off += 2 + m.size();
    }
    return out;
}

// MoldUDP64 Request Packet: Session 10, Sequence Number 8, Requested
// Message Count 2, sent unicast to a re-request server.
inline std::array<std::uint8_t, 20> build_mold_request(const Session& session, std::uint64_t first_seq,
                                                       std::uint16_t count) {
    std::array<std::uint8_t, 20> out{};
    for (std::size_t i = 0; i < 10; ++i) out[i] = static_cast<std::uint8_t>(session[i]);
    write_be(out.data() + 10, first_seq, 8);
    write_be(out.data() + 18, count, 2);
    return out;
}

// Server side of a re-request: exactly 20 bytes, no message blocks.
inline bool parse_mold_request(const std::uint8_t* p, std::size_t n, MoldHeader& out) {
    if (p == nullptr || n != kMoldHeaderSize) return false;
    for (std::size_t i = 0; i < 10; ++i) out.session[i] = static_cast<char>(p[i]);
    out.sequence = read_be(p + 10, 8);
    out.count = static_cast<std::uint16_t>(read_be(p + 18, 2));
    return true;
}

// ---------------------------------------------------------------------------
// A/B line arbitration and gap detection
// ---------------------------------------------------------------------------

struct SeqRange {
    std::uint64_t first = 0;  // inclusive
    std::uint64_t last = 0;   // inclusive
    std::uint64_t size() const { return last - first + 1; }
};

enum class PacketAction {
    Delivered,       // at least one new message delivered in order
    Duplicate,       // every message already delivered (the other line won)
    Buffered,        // ahead of a gap: held until the gap fills
    Heartbeat,       // no data; may reveal a gap at the tail
    EndOfSession,
    Malformed,
    WrongSession,
    BufferFull,      // reorder buffer at capacity: caller must escalate to snapshot recovery
};

struct ArbStats {
    std::uint64_t packets = 0;
    std::uint64_t delivered_messages = 0;
    std::uint64_t duplicate_packets = 0;
    std::uint64_t buffered_packets = 0;
    std::uint64_t gaps_detected = 0;  // transitions from "in sequence" to "gap open"
};

// Merges any number of redundant lines carrying the same MoldUDP64 stream.
// First copy of each sequence number wins; later copies are dropped.
// Packets beyond the next expected sequence number are copied into a
// bounded reorder buffer. The caller decides when an open gap has waited
// long enough and then requests a retransmission (or a snapshot).
class LineArbitrator {
public:
    using Sink = std::function<void(std::uint64_t seq, const std::uint8_t* data, std::size_t len)>;

    explicit LineArbitrator(Sink sink, std::uint64_t first_expected = 1, std::size_t max_buffered = 1024)
        : sink_(std::move(sink)), next_(first_expected), max_buffered_(max_buffered) {}

    PacketAction on_packet(const std::uint8_t* p, std::size_t n) {
        ++stats_.packets;
        MoldHeader h;
        std::vector<std::pair<const std::uint8_t*, std::size_t>> msgs;
        const MoldStatus st = parse_mold_packet(p, n, h, [&](std::uint64_t, const std::uint8_t* d, std::size_t len) {
            msgs.emplace_back(d, len);
        });
        if (st != MoldStatus::Ok || h.sequence > std::numeric_limits<std::uint64_t>::max() - msgs.size()) return PacketAction::Malformed;
        if (!session_) {
            session_ = h.session;
        } else if (*session_ != h.session) {
            return PacketAction::WrongSession;
        }
        if (h.count == kMoldHeartbeat || h.count == kMoldEndOfSession) {
            // Both carry the next expected sequence number.
            if (h.sequence > tail_hint_) tail_hint_ = h.sequence;
            note_gap_state();
            return h.count == kMoldHeartbeat ? PacketAction::Heartbeat : PacketAction::EndOfSession;
        }
        const std::uint64_t end = h.sequence + msgs.size();  // one past the last
        if (end > tail_hint_) tail_hint_ = end;
        if (end <= next_) {
            ++stats_.duplicate_packets;
            return PacketAction::Duplicate;
        }
        if (h.sequence > next_) {
            auto existing = buffer_.find(h.sequence);
            if (existing != buffer_.end()) {
                // Same first sequence already buffered (normally the other
                // line's identical copy). Keep whichever packet reaches
                // further: a resend may be packetised differently, and
                // dropping a longer copy would lose its extra messages.
                if (end <= packet_end(existing->second)) {
                    ++stats_.duplicate_packets;
                    return PacketAction::Duplicate;
                }
                existing->second.assign(p, p + n);
                return PacketAction::Buffered;
            }
            if (buffer_.size() >= max_buffered_) return PacketAction::BufferFull;
            buffer_.emplace(h.sequence, std::vector<std::uint8_t>(p, p + n));
            ++stats_.buffered_packets;
            note_gap_state();
            return PacketAction::Buffered;
        }
        deliver_from(h.sequence, msgs);
        drain();
        note_gap_state();
        return PacketAction::Delivered;
    }

    // First missing range, if any: either before the earliest buffered
    // packet or, with nothing buffered, before the latest heartbeat hint.
    std::optional<SeqRange> missing() const {
        if (!buffer_.empty()) {
            const std::uint64_t first_buffered = buffer_.begin()->first;
            if (first_buffered > next_) return SeqRange{next_, first_buffered - 1};
        }
        if (tail_hint_ > next_) return SeqRange{next_, tail_hint_ - 1};
        return std::nullopt;
    }

    std::uint64_t next_expected() const { return next_; }
    std::size_t buffered() const { return buffer_.size(); }
    const ArbStats& stats() const { return stats_; }
    std::optional<Session> session() const { return session_; }

private:
    void deliver_from(std::uint64_t first_seq, const std::vector<std::pair<const std::uint8_t*, std::size_t>>& msgs) {
        for (std::size_t i = 0; i < msgs.size(); ++i) {
            const std::uint64_t seq = first_seq + i;
            if (seq < next_) continue;  // overlap with what we already have
            sink_(seq, msgs[i].first, msgs[i].second);
            ++stats_.delivered_messages;
            next_ = seq + 1;
        }
    }

    void drain() {
        while (!buffer_.empty() && buffer_.begin()->first <= next_) {
            const std::vector<std::uint8_t> pkt = std::move(buffer_.begin()->second);
            buffer_.erase(buffer_.begin());
            MoldHeader h;
            std::vector<std::pair<const std::uint8_t*, std::size_t>> msgs;
            parse_mold_packet(pkt.data(), pkt.size(), h, [&](std::uint64_t, const std::uint8_t* d, std::size_t len) {
                msgs.emplace_back(d, len);
            });
            deliver_from(h.sequence, msgs);
        }
    }

    // One past the last sequence number of a buffered (already validated) packet.
    static std::uint64_t packet_end(const std::vector<std::uint8_t>& pkt) {
        return read_be(pkt.data() + 10, 8) + read_be(pkt.data() + 18, 2);
    }

    void note_gap_state() {
        const bool open = missing().has_value();
        if (open && !gap_open_) ++stats_.gaps_detected;
        gap_open_ = open;
    }

    Sink sink_;
    std::uint64_t next_;
    std::size_t max_buffered_;
    std::uint64_t tail_hint_ = 0;  // one past the highest sequence seen anywhere
    bool gap_open_ = false;
    std::optional<Session> session_;
    std::map<std::uint64_t, std::vector<std::uint8_t>> buffer_;
    ArbStats stats_;
};

// ---------------------------------------------------------------------------
// Book building
// ---------------------------------------------------------------------------

enum class ApplyStatus { Ok, Ignored, UnknownOrder, DuplicateOrder, Overfill, BadSide };

struct TopOfBook {
    bool has_bid = false;
    std::uint32_t bid_price = 0;
    std::uint64_t bid_shares = 0;
    bool has_ask = false;
    std::uint32_t ask_price = 0;
    std::uint64_t ask_shares = 0;
};

// Rebuilds the displayed book from ITCH order messages. Order reference
// numbers are day-unique across all stocks, so one table serves every
// locate. Modify messages are deltas: E, C and X subtract shares, D and U
// remove the order, U re-adds it under the new reference with the same
// side and locate (the spec omits them from U).
class BookBuilder {
public:
    ApplyStatus apply(const DecodedMessage& m) {
        switch (m.type) {
            case 'A':
            case 'F':
                return add(m.order_ref, m.stock_locate, m.side, m.price, m.shares);
            case 'E':
            case 'C':
            case 'X':
                return reduce(m.order_ref, m.shares);
            case 'D': {
                auto it = orders_.find(m.order_ref);
                if (it == orders_.end()) return ApplyStatus::UnknownOrder;
                return reduce(m.order_ref, it->second.shares);
            }
            case 'U': {
                auto it = orders_.find(m.order_ref);
                if (it == orders_.end()) return ApplyStatus::UnknownOrder;
                if (orders_.count(m.new_order_ref) != 0) return ApplyStatus::DuplicateOrder;
                const Order old = it->second;
                const ApplyStatus st = reduce(m.order_ref, old.shares);
                if (st != ApplyStatus::Ok) return st;
                return add(m.new_order_ref, old.locate, old.side, m.price, m.shares);
            }
            default:
                return ApplyStatus::Ignored;  // S, P, Q, B, R, H do not change the displayed book
        }
    }

    TopOfBook top(std::uint16_t locate) const {
        TopOfBook t;
        auto it = books_.find(locate);
        if (it == books_.end()) return t;
        const Book& b = it->second;
        if (!b.bids.empty()) {
            t.has_bid = true;
            t.bid_price = b.bids.begin()->first;
            t.bid_shares = b.bids.begin()->second;
        }
        if (!b.asks.empty()) {
            t.has_ask = true;
            t.ask_price = b.asks.begin()->first;
            t.ask_shares = b.asks.begin()->second;
        }
        return t;
    }

    // Aggregated displayed shares at one price on one side (0 if empty).
    std::uint64_t level(std::uint16_t locate, char side, std::uint32_t price) const {
        auto it = books_.find(locate);
        if (it == books_.end()) return 0;
        if (side == 'B') {
            auto l = it->second.bids.find(price);
            return l == it->second.bids.end() ? 0 : l->second;
        }
        auto l = it->second.asks.find(price);
        return l == it->second.asks.end() ? 0 : l->second;
    }

    std::size_t live_orders() const { return orders_.size(); }

    std::size_t levels(std::uint16_t locate, char side) const {
        auto it = books_.find(locate);
        if (it == books_.end()) return 0;
        return side == 'B' ? it->second.bids.size() : it->second.asks.size();
    }

    // Snapshot of every level for equality checks in tests.
    std::vector<std::pair<std::uint32_t, std::uint64_t>> depth(std::uint16_t locate, char side) const {
        std::vector<std::pair<std::uint32_t, std::uint64_t>> out;
        auto it = books_.find(locate);
        if (it == books_.end()) return out;
        if (side == 'B') {
            for (const auto& kv : it->second.bids) out.emplace_back(kv.first, kv.second);
        } else {
            for (const auto& kv : it->second.asks) out.emplace_back(kv.first, kv.second);
        }
        return out;
    }

private:
    struct Order {
        std::uint16_t locate;
        char side;
        std::uint32_t price;
        std::uint32_t shares;
    };
    struct Book {
        std::map<std::uint32_t, std::uint64_t, std::greater<>> bids;  // best (highest) first
        std::map<std::uint32_t, std::uint64_t> asks;                  // best (lowest) first
    };

    ApplyStatus add(std::uint64_t ref, std::uint16_t locate, char side, std::uint32_t price, std::uint32_t shares) {
        if (side != 'B' && side != 'S') return ApplyStatus::BadSide;
        if (orders_.count(ref) != 0) return ApplyStatus::DuplicateOrder;
        if (shares == 0) return ApplyStatus::Ok;  // zero display shares: dead on arrival, never rests
        orders_.emplace(ref, Order{locate, side, price, shares});
        Book& b = books_[locate];
        if (side == 'B') {
            b.bids[price] += shares;
        } else {
            b.asks[price] += shares;
        }
        return ApplyStatus::Ok;
    }

    ApplyStatus reduce(std::uint64_t ref, std::uint32_t shares) {
        auto it = orders_.find(ref);
        if (it == orders_.end()) return ApplyStatus::UnknownOrder;
        Order& o = it->second;
        if (shares > o.shares) return ApplyStatus::Overfill;
        Book& b = books_[o.locate];
        if (o.side == 'B') {
            take(b.bids, o.price, shares);
        } else {
            take(b.asks, o.price, shares);
        }
        o.shares -= shares;
        if (o.shares == 0) orders_.erase(it);  // spec: zero display shares means the order is dead
        return ApplyStatus::Ok;
    }

    template <class Levels>
    static void take(Levels& levels, std::uint32_t price, std::uint64_t shares) {
        auto l = levels.find(price);
        if (l == levels.end()) return;
        l->second -= shares;
        if (l->second == 0) levels.erase(l);
    }

    std::unordered_map<std::uint64_t, Order> orders_;
    std::unordered_map<std::uint16_t, Book> books_;
};

}  // namespace itch50

#endif  // QUANT_PREP_ITCH50_FEED_HANDLER_HPP
