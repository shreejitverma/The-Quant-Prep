// A miniature pricing library in the QuantLib style, for 12-Quant-Development/10-Pricing-Library-Design.md.
//
// The separation the note teaches:
//   market data   SimpleQuote (observable numbers), FlatYieldCurve, FlatVolSurface
//   model         BlackScholesProcess (spot + curves + vol, no payoff knowledge)
//   engines       AnalyticEuropeanEngine, BinomialCrrEngine, MonteCarloEuropeanEngine
//   instrument    EuropeanOption (contract terms only, no maths), a LazyObject that caches its results
//
// Changing a quote notifies curve -> process -> engine -> instrument; the instrument only marks
// itself dirty and reprices on the next NPV() call (lazy evaluation). Greeks come three ways:
// closed form, bump-and-reprice through the observer graph, and a reverse-mode AAD tape.
//
// Header-only, standard library only. Not thread-safe by design (see the note): observers and
// caches are shared mutable state, exactly the hazard real libraries must manage.

#pragma once

#include <algorithm>
#include <array>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <limits>
#include <memory>
#include <numbers>
#include <random>
#include <stdexcept>
#include <utility>
#include <vector>

namespace pricing {

// ---------------------------------------------------------------------------------------------
// Observer / Observable. Both sides keep a list so either can be destroyed first safely.
// ---------------------------------------------------------------------------------------------

class Observable;

class Observer {
public:
    Observer() = default;
    Observer(const Observer&) = delete;
    Observer& operator=(const Observer&) = delete;
    virtual ~Observer();
    virtual void update() = 0;
    void registerWith(Observable& observable);
    void unregisterWith(Observable& observable);

private:
    friend class Observable;
    std::vector<Observable*> observables_;
};

class Observable {
public:
    Observable() = default;
    Observable(const Observable&) = delete;
    Observable& operator=(const Observable&) = delete;
    virtual ~Observable() {
        for (Observer* o : observers_) std::erase(o->observables_, this);
    }
    // Iterate over a snapshot: an observer may (un)register while being notified.
    void notifyObservers() {
        const std::vector<Observer*> snapshot = observers_;
        for (Observer* o : snapshot) o->update();
    }
    std::size_t observerCount() const { return observers_.size(); }

private:
    friend class Observer;
    std::vector<Observer*> observers_;
};

inline Observer::~Observer() {
    for (Observable* o : observables_) std::erase(o->observers_, this);
}

inline void Observer::registerWith(Observable& observable) {
    if (std::find(observables_.begin(), observables_.end(), &observable) == observables_.end()) {
        observables_.push_back(&observable);
        observable.observers_.push_back(this);
    }
}

inline void Observer::unregisterWith(Observable& observable) {
    std::erase(observables_, &observable);
    std::erase(observable.observers_, this);
}

// ---------------------------------------------------------------------------------------------
// Market data
// ---------------------------------------------------------------------------------------------

// A number that can change: spot, a rate, a vol. Notifies only on an actual change.
class SimpleQuote final : public Observable {
public:
    explicit SimpleQuote(double value) : value_(value) {}
    double value() const { return value_; }
    void setValue(double value) {
        if (value != value_) {
            value_ = value;
            notifyObservers();
        }
    }

private:
    double value_;
};

// Continuously compounded flat zero curve: P(0, t) = exp(-r t).
class FlatYieldCurve final : public Observable, public Observer {
public:
    explicit FlatYieldCurve(SimpleQuote& rate) : rate_(rate) { registerWith(rate); }
    double zeroRate() const { return rate_.value(); }
    double discount(double t) const { return std::exp(-rate_.value() * t); }
    void update() override { notifyObservers(); }

private:
    const SimpleQuote& rate_;
};

// Flat Black volatility surface: sigma(t, K) = sigma for every expiry and strike.
class FlatVolSurface final : public Observable, public Observer {
public:
    explicit FlatVolSurface(SimpleQuote& vol) : vol_(vol) { registerWith(vol); }
    double blackVol(double /*t*/, double /*strike*/) const { return vol_.value(); }
    double blackVariance(double t, double strike) const {
        const double s = blackVol(t, strike);
        return s * s * t;
    }
    void update() override { notifyObservers(); }

private:
    const SimpleQuote& vol_;
};

// ---------------------------------------------------------------------------------------------
// Model: dS/S = (r - q) dt + sigma dW under the risk-neutral measure.
// ---------------------------------------------------------------------------------------------

class BlackScholesProcess final : public Observable, public Observer {
public:
    BlackScholesProcess(SimpleQuote& spot, FlatYieldCurve& riskFree, FlatYieldCurve& dividend, FlatVolSurface& vol)
        : spot_(spot), riskFree_(riskFree), dividend_(dividend), vol_(vol) {
        registerWith(spot);
        registerWith(riskFree);
        registerWith(dividend);
        registerWith(vol);
    }
    double spot() const { return spot_.value(); }
    double rate() const { return riskFree_.zeroRate(); }
    double dividendYield() const { return dividend_.zeroRate(); }
    double vol(double t, double strike) const { return vol_.blackVol(t, strike); }
    double discount(double t) const { return riskFree_.discount(t); }
    double forward(double t) const { return spot() * dividend_.discount(t) / riskFree_.discount(t); }
    void update() override { notifyObservers(); }

private:
    const SimpleQuote& spot_;
    const FlatYieldCurve& riskFree_;
    const FlatYieldCurve& dividend_;
    const FlatVolSurface& vol_;
};

// ---------------------------------------------------------------------------------------------
// Normal distribution helpers (double versions; AD versions are below)
// ---------------------------------------------------------------------------------------------

inline double normPdf(double x) { return std::exp(-0.5 * x * x) / std::sqrt(2.0 * std::numbers::pi); }
inline double normCdf(double x) { return 0.5 * std::erfc(-x / std::numbers::sqrt2); }

// ---------------------------------------------------------------------------------------------
// Instrument terms and engine interface
// ---------------------------------------------------------------------------------------------

enum class OptionType { Call, Put };

struct OptionArguments {
    OptionType type;
    double strike;
    double expiry;  // year fraction; a real library stores dates and asks a day counter
};

struct OptionResults {
    static constexpr double kNaN = std::numeric_limits<double>::quiet_NaN();
    double value = kNaN;
    double delta = kNaN;
    double gamma = kNaN;
    double vega = kNaN;
    double rho = kNaN;
    double errorEstimate = kNaN;  // Monte Carlo standard error; NaN for deterministic engines
};

// Engines hold the process by reference to keep the example short, so the market objects must
// outlive every engine; QuantLib holds processes and term structures through shared_ptr and Handle.
// Engines are functional here (const calculate returning results). QuantLib engines instead
// hold mutable arguments_ and results_ members filled by the instrument; that is one reason a
// QuantLib engine instance must not be shared across threads.
class PricingEngine : public Observable, public Observer {
public:
    virtual OptionResults calculate(const OptionArguments& args) const = 0;
    void update() override { notifyObservers(); }
};

// Closed-form Black-Scholes-Merton price and Greeks.
class AnalyticEuropeanEngine final : public PricingEngine {
public:
    explicit AnalyticEuropeanEngine(BlackScholesProcess& process) : process_(process) { registerWith(process); }

    OptionResults calculate(const OptionArguments& a) const override {
        const double s = process_.spot();
        const double r = process_.rate();
        const double q = process_.dividendYield();
        const double t = a.expiry;
        const double k = a.strike;
        const double sigma = process_.vol(t, k);
        if (t <= 0.0 || sigma <= 0.0 || s <= 0.0 || k <= 0.0) throw std::domain_error("analytic engine needs t, sigma, S, K > 0");
        const double sqrtT = std::sqrt(t);
        const double d1 = (std::log(s / k) + (r - q + 0.5 * sigma * sigma) * t) / (sigma * sqrtT);
        const double d2 = d1 - sigma * sqrtT;
        const double dfR = std::exp(-r * t);
        const double dfQ = std::exp(-q * t);
        OptionResults out;
        out.gamma = dfQ * normPdf(d1) / (s * sigma * sqrtT);
        out.vega = s * dfQ * normPdf(d1) * sqrtT;
        if (a.type == OptionType::Call) {
            out.value = s * dfQ * normCdf(d1) - k * dfR * normCdf(d2);
            out.delta = dfQ * normCdf(d1);
            out.rho = k * t * dfR * normCdf(d2);
        } else {
            out.value = k * dfR * normCdf(-d2) - s * dfQ * normCdf(-d1);
            out.delta = -dfQ * normCdf(-d1);
            out.rho = -k * t * dfR * normCdf(-d2);
        }
        return out;
    }

private:
    const BlackScholesProcess& process_;
};

// Cox-Ross-Rubinstein binomial tree (European exercise). Converges at O(1/N) with oscillation.
class BinomialCrrEngine final : public PricingEngine {
public:
    BinomialCrrEngine(BlackScholesProcess& process, int steps) : process_(process), steps_(steps) {
        if (steps < 1) throw std::invalid_argument("steps must be >= 1");
        registerWith(process);
    }

    OptionResults calculate(const OptionArguments& a) const override {
        const double s = process_.spot();
        const double t = a.expiry;
        const double sigma = process_.vol(t, a.strike);
        const double dt = t / steps_;
        const double u = std::exp(sigma * std::sqrt(dt));
        const double d = 1.0 / u;
        const double growth = std::exp((process_.rate() - process_.dividendYield()) * dt);
        const double p = (growth - d) / (u - d);
        if (p <= 0.0 || p >= 1.0) throw std::domain_error("CRR probability outside (0, 1); use more steps");
        const double disc = std::exp(-process_.rate() * dt);
        const auto n = static_cast<std::size_t>(steps_);
        std::vector<double> v(n + 1);
        for (std::size_t j = 0; j <= n; ++j) {
            // node j has j up moves and n - j down moves
            const double st = s * std::pow(u, static_cast<double>(j)) * std::pow(d, static_cast<double>(n - j));
            v[j] = payoff(a, st);
        }
        double vUp = 0.0;
        double vDown = 0.0;
        for (std::size_t step = n; step > 0; --step) {
            for (std::size_t j = 0; j < step; ++j) v[j] = disc * (p * v[j + 1] + (1.0 - p) * v[j]);
            if (step == 2) {  // after this sweep v[0], v[1] are the two nodes at time dt
                vDown = v[0];
                vUp = v[1];
            }
        }
        OptionResults out;
        out.value = v[0];
        if (n >= 2) out.delta = (vUp - vDown) / (s * u - s * d);
        return out;
    }

private:
    static double payoff(const OptionArguments& a, double st) {
        return a.type == OptionType::Call ? std::max(st - a.strike, 0.0) : std::max(a.strike - st, 0.0);
    }
    const BlackScholesProcess& process_;
    int steps_;
};

// Uniform in (0, 1) from the raw 64-bit output of std::mt19937_64. The engine's output sequence
// is fixed by the standard, unlike std::normal_distribution whose algorithm is implementation
// defined, so this is reproducible across libstdc++ and libc++.
inline double uniformOpen01(std::mt19937_64& rng) {
    return (static_cast<double>(rng() >> 11) + 0.5) * 0x1.0p-53;
}

// Monte Carlo on the exact GBM terminal distribution with antithetic pairs, fixed seed.
class MonteCarloEuropeanEngine final : public PricingEngine {
public:
    MonteCarloEuropeanEngine(BlackScholesProcess& process, std::size_t pairs, std::uint64_t seed)
        : process_(process), pairs_(pairs), seed_(seed) {
        if (pairs < 2) throw std::invalid_argument("need at least 2 antithetic pairs");
        registerWith(process);
    }

    OptionResults calculate(const OptionArguments& a) const override {
        const double s = process_.spot();
        const double t = a.expiry;
        const double sigma = process_.vol(t, a.strike);
        const double drift = (process_.rate() - process_.dividendYield() - 0.5 * sigma * sigma) * t;
        const double diffusion = sigma * std::sqrt(t);
        const double df = process_.discount(t);
        std::mt19937_64 rng(seed_);
        double sum = 0.0;
        double sumSq = 0.0;
        for (std::size_t i = 0; i < pairs_; ++i) {
            const double z = boxMuller(rng);
            const double upPayoff = payoff(a, s * std::exp(drift + diffusion * z));
            const double downPayoff = payoff(a, s * std::exp(drift - diffusion * z));
            const double y = 0.5 * (upPayoff + downPayoff);  // one antithetic pair is one sample
            sum += y;
            sumSq += y * y;
        }
        const double m = static_cast<double>(pairs_);
        const double mean = sum / m;
        const double var = (sumSq - m * mean * mean) / (m - 1.0);
        OptionResults out;
        out.value = df * mean;
        out.errorEstimate = df * std::sqrt(var / m);
        return out;
    }

private:
    static double payoff(const OptionArguments& a, double st) {
        return a.type == OptionType::Call ? std::max(st - a.strike, 0.0) : std::max(a.strike - st, 0.0);
    }
    static double boxMuller(std::mt19937_64& rng) {
        const double u1 = uniformOpen01(rng);
        const double u2 = uniformOpen01(rng);
        return std::sqrt(-2.0 * std::log(u1)) * std::cos(2.0 * std::numbers::pi * u2);
    }
    const BlackScholesProcess& process_;
    std::size_t pairs_;
    std::uint64_t seed_;
};

// ---------------------------------------------------------------------------------------------
// Lazy instrument
// ---------------------------------------------------------------------------------------------

// Caches its results; a notification only marks it dirty and forwards the notification.
class LazyObject : public Observable, public Observer {
public:
    void update() override {
        if (calculated_) {
            calculated_ = false;
            notifyObservers();
        }
    }
    bool isCalculated() const { return calculated_; }

protected:
    void calculate() const {
        if (!calculated_) {
            calculated_ = true;  // set first so re-entrant calls do not recurse
            try {
                performCalculations();
            } catch (...) {
                calculated_ = false;
                throw;
            }
        }
    }
    void invalidate() {
        calculated_ = false;
        notifyObservers();
    }
    virtual void performCalculations() const = 0;

private:
    mutable bool calculated_ = false;
};

// Contract terms only. It does not know how it is priced; the engine does.
// The engine is held by shared_ptr (as QuantLib does): a raw pointer would dangle if the engine
// were destroyed while the instrument still referred to it.
class EuropeanOption final : public LazyObject {
public:
    EuropeanOption(OptionType type, double strike, double expiry) : args_{type, strike, expiry} {
        if (strike <= 0.0 || expiry <= 0.0) throw std::invalid_argument("strike and expiry must be positive");
    }

    void setPricingEngine(std::shared_ptr<PricingEngine> engine) {
        if (!engine) throw std::invalid_argument("null pricing engine");
        if (engine_) unregisterWith(*engine_);
        engine_ = std::move(engine);
        registerWith(*engine_);
        invalidate();
    }

    double NPV() const { return results().value; }
    const OptionResults& results() const {
        calculate();
        return results_;
    }
    const OptionArguments& arguments() const { return args_; }
    int recalculations() const { return recalculations_; }

private:
    void performCalculations() const override {
        if (!engine_) throw std::logic_error("no pricing engine set");
        results_ = engine_->calculate(args_);
        ++recalculations_;
    }

    OptionArguments args_;
    std::shared_ptr<PricingEngine> engine_;
    mutable OptionResults results_{};
    mutable int recalculations_ = 0;
};

// ---------------------------------------------------------------------------------------------
// Bump-and-reprice Greeks through the observer graph
// ---------------------------------------------------------------------------------------------

enum class Difference { Forward, Central };

// Bumps the quote, reprices (the instrument is invalidated by notification), restores the quote.
// Mutating shared market data is why bump-and-reprice must not run concurrently on one graph.
inline double bumpGreek(const EuropeanOption& option, SimpleQuote& quote, double h, Difference scheme) {
    const double original = quote.value();
    const double base = option.NPV();
    quote.setValue(original + h);
    const double up = option.NPV();
    double result = 0.0;
    if (scheme == Difference::Forward) {
        result = (up - base) / h;
    } else {
        quote.setValue(original - h);
        const double down = option.NPV();
        result = (up - down) / (2.0 * h);
    }
    quote.setValue(original);
    return result;
}

// Newton solve on the vol quote so the instrument reprices to a market price (a one-parameter
// calibration). Every iteration flows through quote -> surface -> process -> engine -> option.
struct CalibrationResult {
    double vol;
    int iterations;
};

inline CalibrationResult calibrateVolatility(const EuropeanOption& option, SimpleQuote& volQuote, double targetPrice,
                                             double tolerance = 1e-12, int maxIterations = 50) {
    for (int i = 1; i <= maxIterations; ++i) {
        const OptionResults& r = option.results();
        const double diff = r.value - targetPrice;
        if (std::fabs(diff) < tolerance) return {volQuote.value(), i - 1};
        if (!(r.vega > 1e-12)) throw std::runtime_error("calibration needs an engine with positive vega");
        volQuote.setValue(std::max(volQuote.value() - diff / r.vega, 1e-6));
    }
    throw std::runtime_error("calibration did not converge");
}

// ---------------------------------------------------------------------------------------------
// Reverse-mode AAD: a tape of nodes, each storing up to two parents and the local partials.
// ---------------------------------------------------------------------------------------------

class Tape {
public:
    std::size_t leaf() { return push(0, {0, 0}, {0.0, 0.0}); }
    std::size_t unary(std::size_t a, double da) { return push(1, {a, 0}, {da, 0.0}); }
    std::size_t binary(std::size_t a, double da, std::size_t b, double db) { return push(2, {a, b}, {da, db}); }
    std::size_t size() const { return nodes_.size(); }
    void clear() { nodes_.clear(); }

    // One backward sweep: adjoint[i] = d output / d node i for every node on the tape.
    std::vector<double> adjoints(std::size_t output) const {
        std::vector<double> adj(nodes_.size(), 0.0);
        adj.at(output) = 1.0;
        for (std::size_t i = output + 1; i-- > 0;) {
            const Node& n = nodes_[i];
            for (std::size_t k = 0; k < n.arity; ++k) adj[n.parent[k]] += n.partial[k] * adj[i];
        }
        return adj;
    }

private:
    struct Node {
        std::size_t arity;
        std::array<std::size_t, 2> parent;
        std::array<double, 2> partial;
    };
    std::size_t push(std::size_t arity, std::array<std::size_t, 2> parent, std::array<double, 2> partial) {
        nodes_.push_back(Node{arity, parent, partial});
        return nodes_.size() - 1;
    }
    std::vector<Node> nodes_;
};

class AD {
public:
    AD(Tape& tape, double value) : value_(value), index_(tape.leaf()), tape_(&tape) {}  // independent variable
    AD(Tape* tape, double value, std::size_t index) : value_(value), index_(index), tape_(tape) {}
    double value() const { return value_; }
    std::size_t index() const { return index_; }
    Tape* tape() const { return tape_; }

private:
    double value_;
    std::size_t index_;
    Tape* tape_;
};

inline AD operator+(const AD& a, const AD& b) { return {a.tape(), a.value() + b.value(), a.tape()->binary(a.index(), 1.0, b.index(), 1.0)}; }
inline AD operator-(const AD& a, const AD& b) { return {a.tape(), a.value() - b.value(), a.tape()->binary(a.index(), 1.0, b.index(), -1.0)}; }
inline AD operator*(const AD& a, const AD& b) {
    return {a.tape(), a.value() * b.value(), a.tape()->binary(a.index(), b.value(), b.index(), a.value())};
}
inline AD operator/(const AD& a, const AD& b) {
    const double inv = 1.0 / b.value();
    return {a.tape(), a.value() * inv, a.tape()->binary(a.index(), inv, b.index(), -a.value() * inv * inv)};
}
inline AD operator+(const AD& a, double c) { return {a.tape(), a.value() + c, a.tape()->unary(a.index(), 1.0)}; }
inline AD operator+(double c, const AD& a) { return a + c; }
inline AD operator-(const AD& a, double c) { return {a.tape(), a.value() - c, a.tape()->unary(a.index(), 1.0)}; }
inline AD operator-(double c, const AD& a) { return {a.tape(), c - a.value(), a.tape()->unary(a.index(), -1.0)}; }
inline AD operator*(const AD& a, double c) { return {a.tape(), a.value() * c, a.tape()->unary(a.index(), c)}; }
inline AD operator*(double c, const AD& a) { return a * c; }
inline AD operator/(const AD& a, double c) { return {a.tape(), a.value() / c, a.tape()->unary(a.index(), 1.0 / c)}; }
inline AD operator-(const AD& a) { return {a.tape(), -a.value(), a.tape()->unary(a.index(), -1.0)}; }
inline AD exp(const AD& a) {
    const double e = std::exp(a.value());
    return {a.tape(), e, a.tape()->unary(a.index(), e)};
}
inline AD log(const AD& a) { return {a.tape(), std::log(a.value()), a.tape()->unary(a.index(), 1.0 / a.value())}; }
inline AD sqrt(const AD& a) {
    const double s = std::sqrt(a.value());
    return {a.tape(), s, a.tape()->unary(a.index(), 0.5 / s)};
}
inline AD normCdf(const AD& a) { return {a.tape(), normCdf(a.value()), a.tape()->unary(a.index(), normPdf(a.value()))}; }

inline double value(double x) { return x; }
inline double value(const AD& x) { return x.value(); }

// Black-Scholes-Merton price written once, generic in the number type: double gives the price,
// AD records the computation on a tape for one reverse sweep.
template <class T>
T blackScholesPrice(OptionType type, const T& spot, double strike, const T& rate, const T& dividend, const T& vol, double expiry) {
    using std::exp;
    using std::log;
    const double sqrtT = std::sqrt(expiry);
    const T sigmaSqrtT = vol * sqrtT;
    const T d1 = (log(spot / strike) + (rate - dividend + 0.5 * vol * vol) * expiry) / sigmaSqrtT;
    const T d2 = d1 - sigmaSqrtT;
    const T dfR = exp(-rate * expiry);
    const T dfQ = exp(-dividend * expiry);
    if (type == OptionType::Call) return spot * dfQ * normCdf(d1) - strike * dfR * normCdf(d2);
    return strike * dfR * normCdf(-d2) - spot * dfQ * normCdf(-d1);
}

struct AadGreeks {
    double value;
    double delta;
    double rho;
    double dividendRho;
    double vega;
    std::size_t tapeNodes;
};

// One forward pass records the tape; one backward sweep yields every first-order sensitivity.
inline AadGreeks aadGreeks(OptionType type, double spot, double strike, double rate, double dividend, double vol, double expiry) {
    Tape tape;
    const AD s(tape, spot);
    const AD r(tape, rate);
    const AD q(tape, dividend);
    const AD v(tape, vol);
    const AD price = blackScholesPrice(type, s, strike, r, q, v, expiry);
    const std::vector<double> adj = tape.adjoints(price.index());
    return {price.value(), adj[s.index()], adj[r.index()], adj[q.index()], adj[v.index()], tape.size()};
}

}  // namespace pricing
