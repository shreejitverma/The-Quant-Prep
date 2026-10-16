// Unit tests for the miniature pricing library (12-Quant-Development/code/cpp/pricing_library.hpp),
// used by 12-Quant-Development/10-Pricing-Library-Design.md.
//
// Covers: known-answer prices, put-call parity, analytic vs finite-difference vs AAD Greeks,
// lazy caching and invalidation through the observer graph, engine swaps, observer lifetime,
// and calibration. Framework-free; exits non-zero on failure.

#include "pricing_library.hpp"

#include <cmath>
#include <iostream>
#include <memory>
#include <stdexcept>

namespace {

int g_failures = 0;
int g_total = 0;

#define EXPECT(cond)                                                                 \
    do {                                                                             \
        ++g_total;                                                                   \
        if (!(cond)) {                                                               \
            ++g_failures;                                                            \
            std::cerr << "  FAIL: " << __FILE__ << ":" << __LINE__ << " -> " #cond << std::endl; \
        }                                                                            \
    } while (0)

#define RUN_TEST(fn)                                                   \
    do {                                                               \
        std::cout << "[RUN ] " #fn << std::endl;                       \
        const int before = g_failures;                                 \
        fn();                                                          \
        std::cout << (g_failures == before ? "[ OK ] " : "[FAIL] ") << #fn << std::endl; \
    } while (0)

bool near(double a, double b, double tol) { return std::fabs(a - b) <= tol; }

using namespace pricing;

// A complete market: S = 100, r = 5%, q = 2%, sigma = 25% unless a test changes it.
struct Market {
    SimpleQuote spot{100.0};
    SimpleQuote rate{0.05};
    SimpleQuote dividend{0.02};
    SimpleQuote vol{0.25};
    FlatYieldCurve riskFree{rate};
    FlatYieldCurve dividendCurve{dividend};
    FlatVolSurface surface{vol};
    BlackScholesProcess process{spot, riskFree, dividendCurve, surface};
    std::shared_ptr<AnalyticEuropeanEngine> analytic = std::make_shared<AnalyticEuropeanEngine>(process);
};

void test_known_answer_textbook_call() {
    // Hull's classic: S = 42, K = 40, r = 10%, sigma = 20%, T = 0.5 gives call 4.76 and put 0.81.
    SimpleQuote spot(42.0), rate(0.10), dividend(0.0), vol(0.20);
    FlatYieldCurve rf(rate), dc(dividend);
    FlatVolSurface surface(vol);
    BlackScholesProcess process(spot, rf, dc, surface);
    auto engine = std::make_shared<AnalyticEuropeanEngine>(process);
    EuropeanOption call(OptionType::Call, 40.0, 0.5);
    EuropeanOption put(OptionType::Put, 40.0, 0.5);
    call.setPricingEngine(engine);
    put.setPricingEngine(engine);
    EXPECT(near(call.NPV(), 4.76, 0.005));
    EXPECT(near(put.NPV(), 0.81, 0.005));
}

void test_put_call_parity_with_dividends() {
    Market m;
    EuropeanOption call(OptionType::Call, 95.0, 1.5);
    EuropeanOption put(OptionType::Put, 95.0, 1.5);
    call.setPricingEngine(m.analytic);
    put.setPricingEngine(m.analytic);
    const double rhs = 100.0 * std::exp(-0.02 * 1.5) - 95.0 * std::exp(-0.05 * 1.5);
    EXPECT(near(call.NPV() - put.NPV(), rhs, 1e-12));
    EXPECT(near(m.process.forward(1.5), 100.0 * std::exp(0.03 * 1.5), 1e-12));
}

void test_aad_matches_analytic_greeks() {
    Market m;
    EuropeanOption put(OptionType::Put, 110.0, 0.75);
    put.setPricingEngine(m.analytic);
    const OptionResults r = put.results();
    const AadGreeks g = aadGreeks(OptionType::Put, 100.0, 110.0, 0.05, 0.02, 0.25, 0.75);
    EXPECT(near(g.value, r.value, 1e-12));
    EXPECT(near(g.delta, r.delta, 1e-12));
    EXPECT(near(g.vega, r.vega, 1e-10));
    EXPECT(near(g.rho, r.rho, 1e-10));
}

void test_central_fd_matches_analytic_and_restores_quotes() {
    Market m;
    EuropeanOption call(OptionType::Call, 105.0, 2.0);
    call.setPricingEngine(m.analytic);
    const OptionResults r = call.results();
    EXPECT(near(bumpGreek(call, m.spot, 1e-3, Difference::Central), r.delta, 1e-8));
    EXPECT(near(bumpGreek(call, m.vol, 1e-4, Difference::Central), r.vega, 1e-5));
    EXPECT(near(bumpGreek(call, m.rate, 1e-5, Difference::Central), r.rho, 1e-5));
    // Forward difference is biased by about gamma * h / 2.
    const double fwd = bumpGreek(call, m.spot, 0.5, Difference::Forward);
    EXPECT(near(fwd - r.delta, 0.5 * r.gamma * 0.5, 0.05 * 0.5 * r.gamma * 0.5));
    EXPECT(m.spot.value() == 100.0 && m.vol.value() == 0.25 && m.rate.value() == 0.05);
    EXPECT(near(call.NPV(), r.value, 0.0));
}

void test_lazy_cache_and_invalidation() {
    Market m;
    EuropeanOption call(OptionType::Call, 100.0, 1.0);
    EXPECT(call.recalculations() == 0);
    call.setPricingEngine(m.analytic);
    EXPECT(!call.isCalculated());  // setting an engine does not price
    (void)call.NPV();
    (void)call.NPV();
    EXPECT(call.recalculations() == 1);
    m.vol.setValue(0.30);  // quote -> surface -> process -> engine -> option
    EXPECT(!call.isCalculated());
    (void)call.NPV();
    EXPECT(call.recalculations() == 2);
    m.vol.setValue(0.30);  // unchanged value: no notification
    EXPECT(call.isCalculated());
    m.dividend.setValue(0.0);  // any upstream node invalidates
    EXPECT(!call.isCalculated());
}

void test_engine_swap_reprices_and_converges() {
    Market m;
    EuropeanOption put(OptionType::Put, 100.0, 1.0);
    put.setPricingEngine(m.analytic);
    const double exact = put.NPV();
    const double exactDelta = put.results().delta;
    auto crr = std::make_shared<BinomialCrrEngine>(m.process, 2000);
    put.setPricingEngine(crr);
    EXPECT(!put.isCalculated());
    EXPECT(near(put.NPV(), exact, 2e-3));
    EXPECT(near(put.results().delta, exactDelta, 2e-3));
    auto mc = std::make_shared<MonteCarloEuropeanEngine>(m.process, 20000, 7);
    put.setPricingEngine(mc);
    const OptionResults r = put.results();
    EXPECT(std::fabs(r.value - exact) < 4.0 * r.errorEstimate);
    // Same seed, same number: the Monte Carlo engine is reproducible.
    MonteCarloEuropeanEngine mc2(m.process, 20000, 7);
    EXPECT(mc2.calculate(put.arguments()).value == r.value);
}

void test_old_engine_no_longer_invalidates() {
    Market m;
    SimpleQuote otherSpot(50.0);
    FlatYieldCurve rf(m.rate), dc(m.dividend);
    FlatVolSurface surface(m.vol);
    BlackScholesProcess otherProcess(otherSpot, rf, dc, surface);
    auto other = std::make_shared<AnalyticEuropeanEngine>(otherProcess);
    EuropeanOption call(OptionType::Call, 100.0, 1.0);
    call.setPricingEngine(other);
    call.setPricingEngine(m.analytic);
    (void)call.NPV();
    otherSpot.setValue(60.0);  // the detached engine must not reach the option
    EXPECT(call.isCalculated());
    EXPECT(other->observerCount() == 0);
}

void test_observer_lifetime_either_order() {
    auto quote = std::make_unique<SimpleQuote>(0.01);
    {
        FlatYieldCurve curve(*quote);
        EXPECT(quote->observerCount() == 1);
    }
    EXPECT(quote->observerCount() == 0);  // observer destroyed first: unregistered
    auto shortLived = std::make_unique<SimpleQuote>(1.0);
    struct Counter final : Observer {
        int n = 0;
        void update() override { ++n; }
    } counter;
    counter.registerWith(*shortLived);
    shortLived->setValue(2.0);
    EXPECT(counter.n == 1);
    shortLived.reset();  // observable destroyed first: the observer must not dangle
    counter.registerWith(*quote);
    quote->setValue(0.02);
    EXPECT(counter.n == 2);
}

void test_missing_engine_throws_and_stays_dirty() {
    EuropeanOption call(OptionType::Call, 100.0, 1.0);
    bool threw = false;
    try {
        (void)call.NPV();
    } catch (const std::logic_error&) {
        threw = true;
    }
    EXPECT(threw);
    EXPECT(!call.isCalculated());  // a failed calculation must not leave a stale "calculated" flag
}

// A zero vol quote makes u = d = 1; with r == q the CRR probability is 0/0 = NaN, which must not
// slip through as a price.
void test_crr_rejects_degenerate_tree() {
    Market m;
    m.vol.setValue(0.0);
    m.dividend.setValue(0.05);  // r == q
    EuropeanOption call(OptionType::Call, 100.0, 1.0);
    call.setPricingEngine(std::make_shared<BinomialCrrEngine>(m.process, 100));
    bool threw = false;
    try {
        (void)call.NPV();
    } catch (const std::domain_error&) {
        threw = true;
    }
    EXPECT(threw);
    EXPECT(!call.isCalculated());
}

void test_calibration_recovers_vol() {
    Market m;
    EuropeanOption call(OptionType::Call, 120.0, 0.5);
    call.setPricingEngine(m.analytic);
    m.vol.setValue(0.33);
    const double target = call.NPV();
    m.vol.setValue(0.20);
    const CalibrationResult c = calibrateVolatility(call, m.vol, target);
    EXPECT(near(c.vol, 0.33, 1e-10));
    EXPECT(c.iterations < 10);
}

}  // namespace

int main() {
    RUN_TEST(test_known_answer_textbook_call);
    RUN_TEST(test_put_call_parity_with_dividends);
    RUN_TEST(test_aad_matches_analytic_greeks);
    RUN_TEST(test_central_fd_matches_analytic_and_restores_quotes);
    RUN_TEST(test_lazy_cache_and_invalidation);
    RUN_TEST(test_engine_swap_reprices_and_converges);
    RUN_TEST(test_old_engine_no_longer_invalidates);
    RUN_TEST(test_observer_lifetime_either_order);
    RUN_TEST(test_missing_engine_throws_and_stays_dirty);
    RUN_TEST(test_crr_rejects_degenerate_tree);
    RUN_TEST(test_calibration_recovers_vol);
    std::cout << "\n" << (g_total - g_failures) << "/" << g_total << " assertions passed" << std::endl;
    return g_failures == 0 ? 0 : 1;
}
