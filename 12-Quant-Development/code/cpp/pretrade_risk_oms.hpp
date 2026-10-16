// Pre-trade risk gateway and order state machine, for
// 12-Quant-Development/13-Risk-Checks-and-Order-Management.md.
//
// What it models:
//   * FIX-style order lifecycle: OrdStatus (tag 39) driven by ExecType (tag 150) on execution
//     reports (35=8) and by order cancel rejects (35=9).
//   * Pre-trade checks in the spirit of SEC Rule 15c3-5(c)(1): kill switch, duplicate ClOrdID,
//     restricted list, max order quantity, price collar against a reference price, max notional,
//     repeated identical orders, message-rate throttle, worst-case position limit and a gross
//     credit limit that counts open orders, not only fills.
//   * Idempotent execution-report handling: duplicates are ignored by ExecID, every report is
//     reconciled against our own CumQty/LeavesQty, and any inconsistency trips the kill switch
//     (fail safe: when the books disagree, stop sending).
//   * The races of the FIX 4.4 order state change matrices (Volume 4, Appendix D, B.1.b to B.1.d):
//     while our cancel or replace is in flight, a report the venue sent before seeing it carries
//     the underlying OrdStatus (New or Partially filled), and one sent after carries Pending Cancel
//     or Pending Replace, which takes precedence even over Filled; both are accepted. An order that
//     fills completely while a cancel is pending stays pending until the venue's cancel reject.
//     A cancel may follow a replace that is still in flight (its OrigClOrdID is the last accepted
//     ClOrdID); the order is then Pending Cancel, either set of replace terms can still execute, and
//     the venue answers the two requests separately.
//
// Prices are integer cents and quantities integer shares, so every check is exact.
// Single-threaded by design: a real gateway pins this to one core and feeds it from a queue.

#pragma once

#include <algorithm>
#include <cstdint>
#include <deque>
#include <limits>
#include <map>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>

namespace oms {

enum class Side : char { Buy = '1', Sell = '2' };  // FIX tag 54 values

// FIX tag 39 values used here.
enum class OrdStatus : char {
    New = '0',
    PartiallyFilled = '1',
    Filled = '2',
    Canceled = '4',
    PendingCancel = '6',
    Rejected = '8',
    PendingNew = 'A',
    Expired = 'C',
    PendingReplace = 'E',
};

// FIX tag 150 values used here (FIX 4.4: Trade = 'F' replaced the old partial-fill/fill values).
enum class ExecType : char {
    New = '0',
    Canceled = '4',
    Replaced = '5',
    PendingCancel = '6',
    Rejected = '8',
    PendingNew = 'A',
    Expired = 'C',
    PendingReplace = 'E',
    Trade = 'F',
};

inline bool isTerminal(OrdStatus s) {
    return s == OrdStatus::Filled || s == OrdStatus::Canceled || s == OrdStatus::Rejected || s == OrdStatus::Expired;
}

// A cancel or replace we sent and the venue has not yet answered.
inline bool isPending(OrdStatus s) { return s == OrdStatus::PendingCancel || s == OrdStatus::PendingReplace; }

inline const char* toString(OrdStatus s) {
    switch (s) {
        case OrdStatus::New: return "New";
        case OrdStatus::PartiallyFilled: return "PartiallyFilled";
        case OrdStatus::Filled: return "Filled";
        case OrdStatus::Canceled: return "Canceled";
        case OrdStatus::PendingCancel: return "PendingCancel";
        case OrdStatus::Rejected: return "Rejected";
        case OrdStatus::PendingNew: return "PendingNew";
        case OrdStatus::Expired: return "Expired";
        case OrdStatus::PendingReplace: return "PendingReplace";
    }
    return "?";
}

enum class RejectReason {
    None,
    KillSwitch,
    DuplicateClOrdId,
    RestrictedSymbol,
    InvalidOrder,
    MaxQuantity,
    NoReferencePrice,
    PriceCollar,
    MaxNotional,
    RepeatedOrder,
    Throttle,
    PositionLimit,
    CreditLimit,
    UnknownOrder,
    NotModifiable,
};

inline const char* toString(RejectReason r) {
    switch (r) {
        case RejectReason::None: return "accepted";
        case RejectReason::KillSwitch: return "kill switch";
        case RejectReason::DuplicateClOrdId: return "duplicate ClOrdID";
        case RejectReason::RestrictedSymbol: return "restricted symbol";
        case RejectReason::InvalidOrder: return "invalid order";
        case RejectReason::MaxQuantity: return "max order quantity";
        case RejectReason::NoReferencePrice: return "no reference price";
        case RejectReason::PriceCollar: return "price collar";
        case RejectReason::MaxNotional: return "max notional";
        case RejectReason::RepeatedOrder: return "repeated identical order";
        case RejectReason::Throttle: return "message throttle";
        case RejectReason::PositionLimit: return "position limit";
        case RejectReason::CreditLimit: return "credit limit";
        case RejectReason::UnknownOrder: return "unknown order";
        case RejectReason::NotModifiable: return "order not modifiable";
    }
    return "?";
}

struct RiskLimits {
    std::int64_t maxOrderQty = 0;
    std::int64_t maxOrderNotionalCents = 0;
    std::int64_t priceCollarBps = 0;           // reject buys above ref*(1+c), sells below ref*(1-c)
    std::int64_t maxAbsPosition = 0;           // per symbol, worst case including open orders
    std::int64_t creditLimitCents = 0;         // gross: |positions| at reference + open order notional
    std::size_t maxMessagesPerWindow = 0;      // new and replace messages per rolling window
    std::uint64_t throttleWindowNs = 0;
    std::uint64_t repeatWindowNs = 0;          // identical symbol/side/qty/price inside this window
};

struct NewOrder {
    std::string clOrdId;  // tag 11
    std::string symbol;   // tag 55
    Side side;            // tag 54
    std::int64_t qty;     // tag 38
    std::int64_t priceCents;  // tag 44, limit orders only in this model
};

struct ExecReport {
    std::string execId;       // tag 17, unique per report
    std::string clOrdId;      // tag 11
    std::string origClOrdId;  // tag 41, on cancel and replace reports
    ExecType execType;        // tag 150
    OrdStatus ordStatus;      // tag 39 as the venue reports it
    std::int64_t lastQty = 0;     // tag 32
    std::int64_t lastPxCents = 0; // tag 31
    std::int64_t leavesQty = 0;   // tag 151
    std::int64_t cumQty = 0;      // tag 14
};

enum class ApplyResult { Applied, Duplicate, UnknownOrder, IllegalTransition, Inconsistent };

inline const char* toString(ApplyResult r) {
    switch (r) {
        case ApplyResult::Applied: return "applied";
        case ApplyResult::Duplicate: return "duplicate ignored";
        case ApplyResult::UnknownOrder: return "unknown order";
        case ApplyResult::IllegalTransition: return "illegal transition";
        case ApplyResult::Inconsistent: return "inconsistent quantities";
    }
    return "?";
}

struct Order {
    std::string key;  // ClOrdID of the original NewOrderSingle
    std::string currentClOrdId;
    std::string symbol;
    Side side;
    std::int64_t orderQty;
    std::int64_t priceCents;
    std::int64_t cumQty = 0;
    std::int64_t leavesQty;
    std::int64_t fillNotionalCents = 0;  // sum of lastQty * lastPx, for AvgPx (tag 6)
    OrdStatus status = OrdStatus::PendingNew;
    // Pending replace terms, applied when the venue confirms with ExecType=Replaced.
    std::string pendingReplaceClOrdId;
    std::int64_t pendingQty = 0;
    std::int64_t pendingPriceCents = 0;

    bool replacePending() const { return !pendingReplaceClOrdId.empty(); }
    void clearReplace() {
        pendingReplaceClOrdId.clear();
        pendingQty = 0;
        pendingPriceCents = 0;
    }

    double avgPx() const { return cumQty == 0 ? 0.0 : static_cast<double>(fillNotionalCents) / static_cast<double>(cumQty) / 100.0; }
    // Shares that could still execute: the larger of old and new leaves while a replace is in flight.
    std::int64_t worstCaseLeaves() const {
        if (replacePending()) return std::max(leavesQty, pendingQty - cumQty);
        return isTerminal(status) ? 0 : leavesQty;
    }
    std::int64_t worstCasePriceCents() const { return replacePending() ? std::max(priceCents, pendingPriceCents) : priceCents; }
};

// Prices above this are rejected as invalid; it also keeps price * 10000 inside int64.
inline constexpr std::int64_t kMaxPriceCents = std::int64_t{1} << 40;

class RiskGateway {
public:
    explicit RiskGateway(RiskLimits limits) : limits_(limits) {}

    // An invalid reference (not in (0, kMaxPriceCents]) is rejected and clears the symbol's last one,
    // so every check that needs it fails closed until a valid price arrives.
    bool setReferencePrice(const std::string& symbol, std::int64_t cents) {
        if (cents <= 0 || cents > kMaxPriceCents) {
            referencePx_.erase(symbol);
            return false;
        }
        referencePx_[symbol] = cents;
        return true;
    }
    void restrict(const std::string& symbol) { restricted_.insert(symbol); }

    // ---- outbound: new order ------------------------------------------------------------------
    RejectReason submit(const NewOrder& o, std::uint64_t nowNs) {
        const RejectReason r = checkNew(o, nowNs);
        seenClOrdIds_.insert(o.clOrdId);  // a rejected id is still burned: never reuse it
        if (r != RejectReason::None) return r;
        Order ord{o.clOrdId, o.clOrdId, o.symbol, o.side, o.qty, o.priceCents, 0, o.qty, 0, OrdStatus::PendingNew, {}, 0, 0};
        orders_.emplace(o.clOrdId, ord);
        alias_[o.clOrdId] = o.clOrdId;
        recordMessage(nowNs);
        recentOrders_.push_back({nowNs, o.symbol, o.side, o.qty, o.priceCents});
        return RejectReason::None;
    }

    // ---- outbound: cancel (never throttled, allowed under the kill switch: it reduces risk) -----
    // Also allowed while a replace is in flight, so the kill switch can cancel every live order.
    RejectReason requestCancel(const std::string& key, const std::string& cancelClOrdId) {
        Order* o = find(key);
        if (o == nullptr) return RejectReason::UnknownOrder;
        if (isTerminal(o->status) || o->status == OrdStatus::PendingCancel) return RejectReason::NotModifiable;
        if (!seenClOrdIds_.insert(cancelClOrdId).second) return RejectReason::DuplicateClOrdId;
        alias_[cancelClOrdId] = o->key;
        if (o->status != OrdStatus::PendingReplace) statusBeforePending_[o->key] = o->status;
        o->status = OrdStatus::PendingCancel;
        return RejectReason::None;
    }

    // ---- outbound: cancel/replace, risk-checked on the worst case of old and new terms ---------
    RejectReason requestReplace(const std::string& key, const std::string& newClOrdId, std::int64_t newQty,
                                std::int64_t newPriceCents, std::uint64_t nowNs) {
        if (killed_) return RejectReason::KillSwitch;
        Order* o = find(key);
        if (o == nullptr) return RejectReason::UnknownOrder;
        if (isTerminal(o->status) || o->status == OrdStatus::PendingCancel || o->status == OrdStatus::PendingReplace)
            return RejectReason::NotModifiable;
        if (seenClOrdIds_.count(newClOrdId) != 0) return RejectReason::DuplicateClOrdId;
        if (newQty <= o->cumQty) return RejectReason::InvalidOrder;  // cannot replace below what already filled
        const NewOrder probe{newClOrdId, o->symbol, o->side, newQty, newPriceCents};
        RejectReason r = staticChecks(probe);
        if (r == RejectReason::None && !throttleAllows(nowNs)) r = RejectReason::Throttle;
        if (r == RejectReason::None) {
            // While the replace is in flight either the old or the new terms can execute, so the
            // order's exposure becomes max(old leaves, new leaves) at max(old price, new price).
            const std::int64_t newLeaves = newQty - o->cumQty;
            const std::int64_t extraQty = std::max<std::int64_t>(0, newLeaves - o->leavesQty);
            const std::int64_t worstNotional = std::max(o->leavesQty, newLeaves) * std::max(o->priceCents, newPriceCents);
            r = exposureChecks(o->symbol, o->side, extraQty, worstNotional - o->leavesQty * o->priceCents);
        }
        seenClOrdIds_.insert(newClOrdId);
        if (r != RejectReason::None) return r;
        alias_[newClOrdId] = o->key;
        statusBeforePending_[o->key] = o->status;
        o->status = OrdStatus::PendingReplace;
        o->pendingReplaceClOrdId = newClOrdId;
        o->pendingQty = newQty;
        o->pendingPriceCents = newPriceCents;
        recordMessage(nowNs);
        return RejectReason::None;
    }

    // ---- inbound: execution report (35=8) --------------------------------------------------------
    ApplyResult onExecutionReport(const ExecReport& er) {
        if (!seenExecIds_.insert(er.execId).second) return ApplyResult::Duplicate;  // idempotent
        Order* o = find(er.clOrdId);
        if (o == nullptr && !er.origClOrdId.empty()) o = find(er.origClOrdId);
        if (o == nullptr) {
            engageKillSwitch("execution report for an unknown order");
            return ApplyResult::UnknownOrder;
        }
        const ApplyResult r = apply(*o, er);
        if (r == ApplyResult::IllegalTransition || r == ApplyResult::Inconsistent) {
            engageKillSwitch("execution report does not reconcile with the order book");
        }
        return r;
    }

    // ---- inbound: order cancel reject (35=9) restores the pre-pending state ----------------------
    // With a cancel on top of a pending replace, only the rejected request is undone.
    ApplyResult onCancelReject(const std::string& requestClOrdId) {
        Order* o = find(requestClOrdId);
        if (o == nullptr) return ApplyResult::UnknownOrder;
        if (!isPending(o->status)) return ApplyResult::IllegalTransition;
        if (o->status == OrdStatus::PendingCancel && o->replacePending()) {
            if (requestClOrdId == o->pendingReplaceClOrdId) {
                o->clearReplace();
            } else {
                o->status = OrdStatus::PendingReplace;
            }
            return ApplyResult::Applied;
        }
        o->status = restoredStatus(*o);
        o->clearReplace();
        return ApplyResult::Applied;
    }

    // ---- kill switch: block new risk, return the cancels to send for every live order -----------
    std::vector<std::string> engageKillSwitch(const std::string& reason) {
        if (!killed_) {
            killed_ = true;
            killReason_ = reason;
        }
        std::vector<std::string> toCancel;
        for (const auto& [key, ord] : orders_) {
            if (!isTerminal(ord.status) && ord.status != OrdStatus::PendingCancel) toCancel.push_back(key);
        }
        return toCancel;
    }
    // Re-arming is a deliberate human action, never automatic.
    void resetKillSwitch() {
        killed_ = false;
        killReason_.clear();
    }

    bool killed() const { return killed_; }
    const std::string& killReason() const { return killReason_; }
    const Order* order(const std::string& anyClOrdId) const {
        const auto a = alias_.find(anyClOrdId);
        if (a == alias_.end()) return nullptr;
        const auto it = orders_.find(a->second);
        return it == orders_.end() ? nullptr : &it->second;
    }
    std::int64_t position(const std::string& symbol) const {
        const auto it = position_.find(symbol);
        return it == position_.end() ? 0 : it->second;
    }
    std::int64_t openQty(const std::string& symbol, Side side) const {
        std::int64_t q = 0;
        for (const auto& [key, ord] : orders_)
            if (ord.symbol == symbol && ord.side == side) q += ord.worstCaseLeaves();
        return q;
    }
    // Gross exposure the credit limit is measured against. A held symbol without a valid reference
    // cannot be valued, so the exposure is reported as unbounded (fail closed).
    std::int64_t grossExposureCents() const {
        std::int64_t e = 0;
        for (const auto& [sym, pos] : position_) {
            if (pos == 0) continue;
            const auto ref = referencePx_.find(sym);
            if (ref == referencePx_.end()) return kUnvaluedExposure;
            e += (pos < 0 ? -pos : pos) * ref->second;
        }
        for (const auto& [key, ord] : orders_) e += ord.worstCaseLeaves() * ord.worstCasePriceCents();
        return e;
    }
    static constexpr std::int64_t kUnvaluedExposure = std::numeric_limits<std::int64_t>::max();

private:
    struct Recent {
        std::uint64_t t;
        std::string symbol;
        Side side;
        std::int64_t qty;
        std::int64_t px;
    };

    Order* find(const std::string& anyClOrdId) {
        const auto a = alias_.find(anyClOrdId);
        if (a == alias_.end()) return nullptr;
        const auto it = orders_.find(a->second);
        return it == orders_.end() ? nullptr : &it->second;
    }

    OrdStatus restoredStatus(const Order& o) const {
        const auto it = statusBeforePending_.find(o.key);
        OrdStatus s = it == statusBeforePending_.end() ? OrdStatus::New : it->second;
        if (o.cumQty > 0 && (s == OrdStatus::New || s == OrdStatus::PendingNew)) s = OrdStatus::PartiallyFilled;
        return s;
    }

    // Order-by-order checks that need no portfolio state.
    RejectReason staticChecks(const NewOrder& o) const {
        if (restricted_.count(o.symbol) != 0) return RejectReason::RestrictedSymbol;
        if (o.qty <= 0 || o.priceCents <= 0 || o.priceCents > kMaxPriceCents) return RejectReason::InvalidOrder;
        if (o.qty > limits_.maxOrderQty) return RejectReason::MaxQuantity;
        const auto ref = referencePx_.find(o.symbol);
        if (ref == referencePx_.end()) return RejectReason::NoReferencePrice;  // fail closed
        // Integer collar: price * 10000 vs ref * (10000 +- bps); kMaxPriceCents keeps both products in range.
        if (o.side == Side::Buy && o.priceCents * 10000 > ref->second * (10000 + limits_.priceCollarBps)) return RejectReason::PriceCollar;
        if (o.side == Side::Sell && o.priceCents * 10000 < ref->second * (10000 - limits_.priceCollarBps)) return RejectReason::PriceCollar;
        if (o.priceCents > std::numeric_limits<std::int64_t>::max() / o.qty) return RejectReason::MaxNotional;
        if (o.qty * o.priceCents > limits_.maxOrderNotionalCents) return RejectReason::MaxNotional;
        return RejectReason::None;
    }

    // Portfolio checks: worst-case position and gross credit, both counting open orders.
    RejectReason exposureChecks(const std::string& symbol, Side side, std::int64_t addQty, std::int64_t addNotionalCents) const {
        const std::int64_t pos = position(symbol);
        if (side == Side::Buy && pos + openQty(symbol, Side::Buy) + addQty > limits_.maxAbsPosition) return RejectReason::PositionLimit;
        if (side == Side::Sell && pos - openQty(symbol, Side::Sell) - addQty < -limits_.maxAbsPosition) return RejectReason::PositionLimit;
        const std::int64_t gross = grossExposureCents();
        if (gross > limits_.creditLimitCents || addNotionalCents > limits_.creditLimitCents - gross) return RejectReason::CreditLimit;
        return RejectReason::None;
    }

    bool throttleAllows(std::uint64_t nowNs) {
        // Expire only entries that are really older than the window: a clock that steps backwards
        // must not wrap the unsigned difference and empty the window (that would fail open).
        while (!sent_.empty() && nowNs >= sent_.front() && nowNs - sent_.front() >= limits_.throttleWindowNs) sent_.pop_front();
        return sent_.size() < limits_.maxMessagesPerWindow;
    }
    void recordMessage(std::uint64_t nowNs) { sent_.push_back(nowNs); }

    bool isRepeat(const NewOrder& o, std::uint64_t nowNs) {
        while (!recentOrders_.empty() && nowNs >= recentOrders_.front().t && nowNs - recentOrders_.front().t >= limits_.repeatWindowNs)
            recentOrders_.pop_front();
        for (const Recent& r : recentOrders_)
            if (r.symbol == o.symbol && r.side == o.side && r.qty == o.qty && r.px == o.priceCents) return true;
        return false;
    }

    RejectReason checkNew(const NewOrder& o, std::uint64_t nowNs) {
        if (killed_) return RejectReason::KillSwitch;
        if (seenClOrdIds_.count(o.clOrdId) != 0) return RejectReason::DuplicateClOrdId;
        if (const RejectReason r = staticChecks(o); r != RejectReason::None) return r;
        if (isRepeat(o, nowNs)) return RejectReason::RepeatedOrder;
        if (const RejectReason r = exposureChecks(o.symbol, o.side, o.qty, o.qty * o.priceCents); r != RejectReason::None) return r;
        // Throttle last: only orders that would otherwise go out are counted against the rate.
        if (!throttleAllows(nowNs)) return RejectReason::Throttle;
        return RejectReason::None;
    }

    // The status the venue reports while it has not yet seen our pending cancel or replace.
    OrdStatus underlying(const Order& o) const { return isPending(o.status) ? restoredStatus(o) : o.status; }
    void setUnderlying(Order& o, OrdStatus s) {
        if (isPending(o.status)) {
            statusBeforePending_[o.key] = s;  // pending states take precedence in OrdStatus
        } else {
            o.status = s;
        }
    }

    ApplyResult apply(Order& o, const ExecReport& er) {
        switch (er.execType) {
            case ExecType::PendingNew:
                if (underlying(o) != OrdStatus::PendingNew) return ApplyResult::IllegalTransition;
                return reconcile(o, er);
            case ExecType::New:
                // The ack may arrive after we already sent a cancel or replace (Appendix D, B.1.d).
                if (underlying(o) != OrdStatus::PendingNew) return ApplyResult::IllegalTransition;
                setUnderlying(o, OrdStatus::New);
                return reconcile(o, er);
            case ExecType::Rejected:
                if (underlying(o) != OrdStatus::PendingNew) return ApplyResult::IllegalTransition;
                o.status = OrdStatus::Rejected;
                o.leavesQty = 0;
                o.clearReplace();
                return reconcile(o, er);
            case ExecType::Trade: {
                // A fill may arrive while a cancel or replace is pending, or before the New ack.
                if (isTerminal(o.status)) return ApplyResult::IllegalTransition;
                if (er.lastQty <= 0 || er.lastQty > o.leavesQty) return ApplyResult::Inconsistent;  // overfill
                if (er.lastPxCents <= 0 || er.lastPxCents > kMaxPriceCents) return ApplyResult::Inconsistent;
                o.cumQty += er.lastQty;
                o.leavesQty -= er.lastQty;
                o.fillNotionalCents += er.lastQty * er.lastPxCents;
                position_[o.symbol] += o.side == Side::Buy ? er.lastQty : -er.lastQty;
                // While a cancel is pending, even a completing fill leaves OrdStatus at Pending Cancel
                // (Appendix D, B.1.c); the venue's cancel reject then reports Filled.
                setUnderlying(o, o.leavesQty == 0 ? OrdStatus::Filled : OrdStatus::PartiallyFilled);
                return reconcile(o, er);
            }
            case ExecType::PendingCancel:
                if (o.status != OrdStatus::PendingCancel) return ApplyResult::IllegalTransition;
                return reconcile(o, er);
            case ExecType::PendingReplace:
                if (!o.replacePending()) return ApplyResult::IllegalTransition;
                return reconcile(o, er);
            case ExecType::Canceled:
            case ExecType::Expired:
                // Solicited (after our cancel) or unsolicited (IOC remainder, end of day) cancel.
                if (isTerminal(o.status) || o.status == OrdStatus::PendingNew) return ApplyResult::IllegalTransition;
                o.status = er.execType == ExecType::Canceled ? OrdStatus::Canceled : OrdStatus::Expired;
                o.leavesQty = 0;
                o.clearReplace();
                return reconcile(o, er);
            case ExecType::Replaced: {
                if (!o.replacePending()) return ApplyResult::IllegalTransition;
                // Fills that crossed the replace may have used up the new quantity: the venue then
                // amends the order quantity to CumQty and reports Filled (Appendix D, C.3.b and C.3.c).
                o.orderQty = std::max(o.pendingQty, o.cumQty);
                o.priceCents = o.pendingPriceCents;
                o.leavesQty = o.orderQty - o.cumQty;
                o.currentClOrdId = er.clOrdId;
                o.clearReplace();
                const OrdStatus s = o.leavesQty == 0 ? OrdStatus::Filled : o.cumQty > 0 ? OrdStatus::PartiallyFilled : OrdStatus::New;
                // A cancel sent after the replace is still pending against the replaced order.
                if (o.status == OrdStatus::PendingCancel) {
                    statusBeforePending_[o.key] = s;
                } else {
                    o.status = s;
                }
                return reconcile(o, er);
            }
        }
        return ApplyResult::IllegalTransition;
    }

    // Our book must agree with the venue's CumQty, LeavesQty and OrdStatus on every report.
    // While a cancel or replace is pending the venue may report either the pending status (it has
    // seen the request) or the underlying one (the report crossed our request on the wire).
    ApplyResult reconcile(const Order& o, const ExecReport& er) const {
        if (er.cumQty != o.cumQty || er.leavesQty != o.leavesQty) return ApplyResult::Inconsistent;
        if (!isTerminal(o.status) && o.cumQty + o.leavesQty != o.orderQty) return ApplyResult::Inconsistent;
        const bool statusOk = er.ordStatus == o.status || (isPending(o.status) && er.ordStatus == underlying(o)) ||
                              (o.replacePending() && er.ordStatus == OrdStatus::PendingReplace);
        if (!statusOk) return ApplyResult::Inconsistent;
        return ApplyResult::Applied;
    }

    RiskLimits limits_;
    bool killed_ = false;
    std::string killReason_;
    std::unordered_map<std::string, std::int64_t> referencePx_;
    std::unordered_set<std::string> restricted_;
    std::unordered_set<std::string> seenClOrdIds_;
    std::unordered_set<std::string> seenExecIds_;
    std::map<std::string, Order> orders_;  // ordered so kill-switch cancel lists are deterministic
    std::unordered_map<std::string, std::string> alias_;  // any ClOrdID in the chain -> original key
    std::unordered_map<std::string, OrdStatus> statusBeforePending_;
    std::map<std::string, std::int64_t> position_;
    std::deque<std::uint64_t> sent_;
    std::deque<Recent> recentOrders_;
};

}  // namespace oms
