// Demo for 12-Quant-Development/10-Pricing-Library-Design.md: every number the note quotes is
// printed and asserted here.
//
// Build: clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror -pthread -o pricing_library pricing_library.cpp
// Run:   ./pricing_library

#include "pricing_library.hpp"

#include <cmath>
#include <cstdio>
#include <cstdlib>
#include <limits>
#include <memory>

namespace {

int g_failures = 0;

void check(bool ok, const char* what) {
    if (!ok) {
        ++g_failures;
        std::fprintf(stderr, "ASSERTION FAILED: %s\n", what);
    }
}

bool near(double a, double b, double tol) { return std::fabs(a - b) <= tol; }

}  // namespace

int main() {
    using namespace pricing;

    // Market data, model, engine, instrument: four separate layers.
    SimpleQuote spot(100.0);
    SimpleQuote rate(0.05);
    SimpleQuote dividend(0.0);
    SimpleQuote vol(0.20);
    FlatYieldCurve riskFree(rate);
    FlatYieldCurve dividendCurve(dividend);
    FlatVolSurface surface(vol);
    BlackScholesProcess process(spot, riskFree, dividendCurve, surface);
    auto analytic = std::make_shared<AnalyticEuropeanEngine>(process);

    EuropeanOption call(OptionType::Call, 100.0, 1.0);
    EuropeanOption put(OptionType::Put, 100.0, 1.0);
    call.setPricingEngine(analytic);
    put.setPricingEngine(analytic);

    // 1. Known-answer price, parity and analytic Greeks.
    const OptionResults c = call.results();  // copy: results() refers to a cache that later reprices overwrite
    const double callPrice = c.value;
    const double putPrice = put.NPV();
    const double parityRhs = 100.0 - 100.0 * std::exp(-0.05);
    std::printf("[1] analytic call %.4f put %.4f\n", callPrice, putPrice);
    std::printf("    parity C - P = %.4f, S - K exp(-rT) = %.4f\n", callPrice - putPrice, parityRhs);
    std::printf("    delta %.4f gamma %.5f vega %.3f rho %.3f\n", c.delta, c.gamma, c.vega, c.rho);
    check(near(callPrice, 10.4506, 5e-5), "call price 10.4506");
    check(near(putPrice, 5.5735, 5e-5), "put price 5.5735");
    check(near(callPrice - putPrice, parityRhs, 1e-12), "put-call parity");
    check(near(parityRhs, 4.8771, 5e-5), "parity rhs 4.8771");
    check(near(c.delta, 0.6368, 5e-5), "delta 0.6368");
    check(near(c.gamma, 0.01876, 5e-6), "gamma 0.01876");
    check(near(c.vega, 37.524, 5e-4), "vega 37.524");
    check(near(c.rho, 53.232, 5e-4), "rho 53.232");

    // 2. Lazy evaluation and caching: repeated NPV calls reuse the cache; a quote change
    //    invalidates through the observer chain; setting the same value again does nothing.
    const int r0 = call.recalculations();
    (void)call.NPV();
    (void)call.NPV();
    const int r1 = call.recalculations();
    spot.setValue(101.0);
    const bool dirtyAfterBump = !call.isCalculated();
    const double bumped = call.NPV();
    const int r2 = call.recalculations();
    spot.setValue(101.0);
    (void)call.NPV();
    const int r3 = call.recalculations();
    spot.setValue(100.0);
    (void)call.NPV();
    std::printf("[2] recalcs: after first price %d, after 2 more NPV calls %d, after spot 101 %d (dirty %d), same value again %d\n",
                r0, r1, r2, dirtyAfterBump ? 1 : 0, r3);
    std::printf("    call at spot 101 = %.4f\n", bumped);
    check(r0 == 1 && r1 == 1, "cached NPV does not recalculate");
    check(dirtyAfterBump && r2 == 2, "spot change invalidates and reprices once");
    check(r3 == 2, "unchanged quote does not notify");
    check(near(bumped, 11.0967, 5e-5), "call at spot 101 = 11.0967");
    std::printf("    observers: spot %zu, process %zu, analytic engine %zu\n", spot.observerCount(), process.observerCount(),
                analytic->observerCount());
    check(spot.observerCount() == 1 && process.observerCount() == 1 && analytic->observerCount() == 2, "observer graph wiring");

    // 3. Engine swap: same instrument, numerical engines.
    std::printf("[3] CRR binomial call price and error vs analytic\n");
    const int stepsList[] = {50, 51, 100, 101, 500, 1000};
    double crrErr[6] = {};
    double crrPx[6] = {};
    int idx = 0;
    for (int n : stepsList) {
        call.setPricingEngine(std::make_shared<BinomialCrrEngine>(process, n));  // the old engine is released
        const double v = call.NPV();
        crrPx[idx] = v;
        crrErr[idx] = v - callPrice;
        std::printf("    N=%4d  %.4f  error %+.4f\n", n, v, crrErr[idx]);
        ++idx;
    }
    // CRR at-the-money errors oscillate between even and odd N and shrink like 1/N.
    check(near(crrErr[0], -0.0399, 5e-5), "CRR N=50 error -0.0399");
    check(near(crrErr[1], 0.0344, 5e-5), "CRR N=51 error +0.0344");
    check(near(crrErr[2], -0.0200, 5e-5), "CRR N=100 error -0.0200");
    check(near(crrErr[3], 0.0174, 5e-5), "CRR N=101 error +0.0174");
    check(near(crrErr[4], -0.0040, 5e-5), "CRR N=500 error -0.0040");
    check(near(crrErr[5], -0.0020, 5e-5), "CRR N=1000 error -0.0020");
    const double crrTable[6] = {10.4107, 10.4850, 10.4306, 10.4680, 10.4466, 10.4486};
    for (int i = 0; i < 6; ++i) check(near(crrPx[i], crrTable[i], 5e-5), "CRR price table entry");
    std::printf("    N x error for even N: %.3f %.3f %.3f %.3f\n", 50 * crrErr[0], 100 * crrErr[2], 500 * crrErr[4], 1000 * crrErr[5]);
    check(near(50 * crrErr[0], -1.995, 5e-4) && near(100 * crrErr[2], -1.997, 5e-4) && near(500 * crrErr[4], -1.999, 5e-4) &&
              near(1000 * crrErr[5], -1.999, 5e-4),
          "even-N CRR N x error = -1.995 -1.997 -1.999 -1.999 (about -2 / N)");

    call.setPricingEngine(std::make_shared<MonteCarloEuropeanEngine>(process, 100000, 42));
    const OptionResults m = call.results();
    const double z = (m.value - callPrice) / m.errorEstimate;
    std::printf("    MC 100000 antithetic pairs seed 42: %.4f +- %.4f (z = %.2f)\n", m.value, m.errorEstimate, z);
    check(std::fabs(z) < 3.0, "MC within 3 standard errors");
    check(m.errorEstimate > 0.01 && m.errorEstimate < 0.04, "MC standard error about 0.02");
    // Seed-stable values (the engine's random stream is fully specified by the standard).
    check(near(m.value, 10.4372, 5e-5) && near(m.errorEstimate, 0.0231, 5e-5) && near(z, -0.58, 5e-3), "MC seed 42 values");
    call.setPricingEngine(analytic);

    // 4. Bump-and-reprice delta: truncation versus round-off.
    std::printf("[4] finite-difference delta error vs bump h (analytic delta %.10f)\n", c.delta);
    std::printf("    %8s  %12s  %12s  %12s\n", "h", "forward err", "central err", "gamma*h/2");
    const double hs[] = {1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-8, 1e-10};
    double fwdErr[9] = {};
    double cenErr[9] = {};
    idx = 0;
    for (double h : hs) {
        fwdErr[idx] = bumpGreek(call, spot, h, Difference::Forward) - c.delta;
        cenErr[idx] = bumpGreek(call, spot, h, Difference::Central) - c.delta;
        std::printf("    %8.0e  %+12.3e  %+12.3e  %12.3e\n", h, fwdErr[idx], cenErr[idx], 0.5 * c.gamma * h);
        ++idx;
    }
    check(near(spot.value(), 100.0, 0.0), "bump restores the quote");
    // Forward difference: error = gamma h / 2 to leading order for h in the truncation regime.
    check(near(fwdErr[1], 0.5 * c.gamma * 1e-1, 0.05 * 0.5 * c.gamma * 1e-1), "forward error ~ gamma h/2 at h=0.1");
    check(near(fwdErr[2], 0.5 * c.gamma * 1e-2, 0.02 * 0.5 * c.gamma * 1e-2), "forward error ~ gamma h/2 at h=0.01");
    // Central difference: O(h^2); dividing h by 10 divides the error by about 100.
    check(std::fabs(cenErr[0] / cenErr[1]) > 90.0 && std::fabs(cenErr[0] / cenErr[1]) < 110.0, "central error is O(h^2)");
    check(std::fabs(cenErr[2]) < 1e-7, "central error at h=0.01 below 1e-7");
    // Round-off floor: at h = 1e-10 the error is far above the best achievable error.
    check(std::fabs(fwdErr[8]) > 1e-8 && std::fabs(cenErr[8]) > 1e-8, "round-off dominates at h=1e-10");
    // Balancing truncation against round-off: forward h* ~ sqrt(eps) x scale, central h* ~ cbrt(eps) x scale.
    const double eps = std::numeric_limits<double>::epsilon();
    std::printf("    eps %.3e, sqrt(eps) %.2e, cbrt(eps) %.2e\n", eps, std::sqrt(eps), std::cbrt(eps));
    check(eps == 0x1p-52 && near(eps, 2.220e-16, 5e-20), "eps = 2^-52 = 2.220e-16");
    check(near(std::sqrt(eps), 1.49e-8, 5e-11) && near(std::cbrt(eps), 6.06e-6, 5e-9), "optimal-step constants");
    check(std::fabs(cenErr[4]) < 1e-9, "central at h=1e-4 is accurate to 1e-9");
    // The table the note quotes, each entry asserted at the rounding the note prints. Two entries are
    // quoted to 3 figures because one ulp of price round-off is already 1.8e-11 at h = 1e-4 (forward)
    // and about 1e-13 at h = 0.01 (central), close to the 4th figure. Round-off-dominated entries
    // (forward from h = 1e-5, central from h = 1e-3) depend on the platform libm and are asserted by size only.
    const double fwdTable[5] = {9.294e-3, 9.372e-4, 9.380e-5, 9.381e-6, 9.38e-7};
    const double fwdTol[5] = {5e-7, 5e-8, 5e-9, 5e-10, 5e-10};
    const double cenTable[3] = {-8.596e-5, -8.599e-7, -8.60e-9};
    const double cenTol[3] = {5e-9, 5e-11, 5e-12};
    for (int i = 0; i < 5; ++i) check(near(fwdErr[i], fwdTable[i], fwdTol[i]), "forward error table entry at quoted rounding");
    // The gamma h / 2 column is 9.381e-3 x h in every row, asserted at the 4 figures printed.
    for (double h : hs) check(near(0.5 * c.gamma * h, 9.381e-3 * h, 5e-7 * h), "gamma h / 2 column = 9.381e-3 x h");
    check(std::fabs(fwdErr[5] / 9.341e-8 - 1.0) < 3e-2, "forward error at h=1e-5, platform-dependent: size only");
    for (int i = 0; i < 3; ++i) check(near(cenErr[i], cenTable[i], cenTol[i]), "central error table entry at quoted rounding");
    for (int i = 3; i < 7; ++i) check(std::fabs(cenErr[i]) < 1e-8, "central error below 1e-8 for h in [1e-6, 1e-3]");
    check(std::fabs(fwdErr[6]) > 1e-9 && std::fabs(fwdErr[6]) < 1e-7, "forward error at h=1e-6 is about 1e-8");
    check(std::fabs(fwdErr[7]) > 1e-8 && std::fabs(fwdErr[7]) < 1e-5 && std::fabs(cenErr[7]) > 1e-8 && std::fabs(cenErr[7]) < 1e-5,
          "round-off band at h=1e-8");
    check(std::fabs(fwdErr[8]) > 1e-7 && std::fabs(fwdErr[8]) < 1e-3 && std::fabs(cenErr[8]) > 1e-7 && std::fabs(cenErr[8]) < 1e-3,
          "round-off band at h=1e-10");

    // Central vega with a 1 vol point bump (0.01), and rho with 1 bp.
    const double vegaFd = bumpGreek(call, vol, 0.01, Difference::Central);
    const double rhoFd = bumpGreek(call, rate, 0.0001, Difference::Central);
    std::printf("    central vega (h = 0.01) %.4f vs %.4f; central rho (h = 1bp) %.4f vs %.4f\n", vegaFd, c.vega, rhoFd, c.rho);
    check(near(vegaFd, c.vega, 0.01), "FD vega within 0.01");
    check(near(vegaFd, 37.5210, 5e-5) && near(c.vega, 37.5240, 5e-5) && near(rhoFd, 53.2325, 5e-5), "printed FD vega and rho");
    check(near(rhoFd, c.rho, 1e-4), "FD rho within 1e-4");

    // 5. AAD: one forward pass plus one backward sweep gives every first-order Greek.
    const AadGreeks g = aadGreeks(OptionType::Call, 100.0, 100.0, 0.05, 0.0, 0.20, 1.0);
    std::printf("[5] AAD: value %.4f delta %.10f vega %.6f rho %.6f dividend-rho %.6f tape nodes %zu\n", g.value, g.delta, g.vega,
                g.rho, g.dividendRho, g.tapeNodes);
    std::printf("    |AAD - analytic|: delta %.1e vega %.1e rho %.1e\n", std::fabs(g.delta - c.delta), std::fabs(g.vega - c.vega),
                std::fabs(g.rho - c.rho));
    check(near(g.value, callPrice, 1e-12), "AAD value");
    check(near(g.delta, c.delta, 1e-13), "AAD delta = analytic");
    check(near(g.vega, c.vega, 1e-13), "AAD vega = analytic");
    check(near(g.rho, c.rho, 1e-13), "AAD rho = analytic");
    // dV/dq for a call is -S T exp(-qT) N(d1) = -100 * delta here.
    check(near(g.dividendRho, -100.0 * c.delta, 1e-10), "AAD dividend rho = -S T delta");
    check(g.tapeNodes == 28, "tape has 28 nodes");
    check(near(g.delta, 0.6368306512, 5e-11) && near(g.vega, 37.524035, 5e-7) && near(g.rho, 53.232482, 5e-7) &&
              near(g.dividendRho, -63.683065, 5e-7),
          "printed AAD Greeks 0.6368306512 37.524035 53.232482 -63.683065");

    // 6. Calibration: solve the vol quote so the option reprices to a market price of 12.
    const int before = call.recalculations();
    const CalibrationResult cal = calibrateVolatility(call, vol, 12.0);
    const int reprices = call.recalculations() - before;
    std::printf("[6] implied vol for call price 12.0000: %.6f after %d Newton steps (%d reprices)\n", cal.vol, cal.iterations, reprices);
    check(near(cal.vol, 0.241117, 5e-7), "implied vol 0.241117");
    check(cal.iterations == 3 && reprices == 4, "3 Newton steps, 4 reprices");
    check(near(call.NPV(), 12.0, 1e-10), "calibrated price");
    check(cal.iterations <= 5, "Newton converges in a few steps");
    vol.setValue(0.20);

    if (g_failures != 0) {
        std::fprintf(stderr, "%d assertion(s) failed\n", g_failures);
        return EXIT_FAILURE;
    }
    std::printf("all assertions passed\n");
    return EXIT_SUCCESS;
}
