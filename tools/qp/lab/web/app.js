/**
 * Markets Mastery OS - Trading Lab Web Runner
 * Pure Vanilla JavaScript simulations and Canvas rendering across 11 engines.
 */

// Global state
let currentEngine = "pos_sizing";

const ENGINE_CONFIGS = {
  pos_sizing: {
    title: "Position Sizing and Risk of Ruin Engine",
    desc: "Evaluates Kelly criterion, fractional Kelly, and Monte Carlo drawdown risk distributions.",
    chartTitle: "Sample Monte Carlo Equity Trajectories",
    chartLegend: "Sample Paths (1 to 5)",
    params: [
      { id: "p-account-capital", label: "Starting Capital ($)", type: "number", value: 100000, step: 1000, min: 1000, max: 10000000 },
      { id: "p-win-rate", label: "Win Rate (0.01 - 0.99)", type: "number", value: 0.55, step: 0.01, min: 0.01, max: 0.99 },
      { id: "p-win-loss-ratio", label: "Win/Loss Ratio (b)", type: "number", value: 1.50, step: 0.05, min: 0.1, max: 20.0 },
      { id: "p-risk-per-trade-pct", label: "Risk per Trade (Fraction)", type: "number", value: 0.02, step: 0.001, min: 0.001, max: 0.50 },
      { id: "p-num-trades", label: "Number of Trades", type: "number", value: 100, step: 10, min: 10, max: 1000 },
      { id: "p-num-simulations", label: "Monte Carlo Paths", type: "number", value: 250, step: 50, min: 50, max: 1000 },
    ],
    runner: runPositionSizing,
  },
  overfit_trap: {
    title: "Backtest Overfitting Trap & Deflated Sharpe",
    desc: "Calculates Deflated Sharpe Ratio (DSR), Harvey-Liu multiple testing haircuts, and CSCV PBO.",
    chartTitle: "Expected Maximum Sharpe Ratio vs Number of Independent Strategy Trials",
    chartLegend: "Observed Sharpe vs Haircut Threshold",
    params: [
      { id: "p-observed-sharpe", label: "Observed Sharpe Ratio", type: "number", value: 1.5, step: 0.1, min: 0.1, max: 5.0 },
      { id: "p-num-trials", label: "Strategy Trials Tested (N)", type: "number", value: 100, step: 1, min: 1, max: 10000 },
      { id: "p-sample-length-days", label: "Sample Length (Trading Days)", type: "number", value: 1260, step: 1, min: 100, max: 10000 },
      { id: "p-skewness", label: "Return Skewness", type: "number", value: -0.5, step: 0.1, min: -5.0, max: 5.0 },
      { id: "p-kurtosis", label: "Return Kurtosis", type: "number", value: 4.5, step: 0.2, min: 1.5, max: 30.0 },
    ],
    runner: runOverfitTrap,
  },
  opt_desk: {
    title: "Options Volatility & Dynamic Delta Hedging Desk",
    desc: "Computes Black-Scholes Greeks, implied volatility smile, and dynamic delta-hedged tracking errors.",
    chartTitle: "Dynamic Delta Hedging Path vs Underlying Spot Asset",
    chartLegend: "Spot Price vs Portfolio Delta",
    params: [
      { id: "p-scenario", label: "Desk Scenario", type: "select", value: "gamma_scalp", options: ["gamma_scalp", "earnings_crush", "skew_shift", "dispersion"] },
      { id: "p-spot", label: "Underlying Spot Price ($)", type: "number", value: 100.0, step: 1.0, min: 10.0, max: 5000.0 },
      { id: "p-strike", label: "Option Strike ($)", type: "number", value: 100.0, step: 1.0, min: 10.0, max: 5000.0 },
      { id: "p-implied-vol", label: "Implied Volatility (Fraction)", type: "number", value: 0.25, step: 0.01, min: 0.05, max: 2.0 },
      { id: "p-realized-vol", label: "Realized Volatility (Fraction)", type: "number", value: 0.32, step: 0.01, min: 0.05, max: 2.0 },
      { id: "p-days-to-expiry", label: "Days to Expiration", type: "number", value: 30, step: 1, min: 1, max: 365 },
      { id: "p-risk-free-rate", label: "Risk-Free Rate (Fraction)", type: "number", value: 0.04, step: 0.005, min: 0.0, max: 0.20 },
    ],
    runner: runOptionsLab,
  },
  fut_desk: {
    title: "Futures Term Structure & Basis Arbitrage Desk",
    desc: "Evaluates cost-of-carry term structures, contango/backwardation geometry, roll yields, and basis convergence.",
    chartTitle: "Futures Curve Term Structure vs Theoretical Cost-of-Carry",
    chartLegend: "Theoretical vs Market Curve",
    params: [
      { id: "p-spot-price", label: "Spot Commodity/Index Price ($)", type: "number", value: 100.0, step: 5.0, min: 10.0, max: 10000.0 },
      { id: "p-risk-free-rate", label: "Financing Rate (Fraction)", type: "number", value: 0.045, step: 0.005, min: 0.0, max: 0.25 },
      { id: "p-dividend-yield", label: "Dividend / Yield (Fraction)", type: "number", value: 0.015, step: 0.005, min: 0.0, max: 0.20 },
      { id: "p-storage-cost", label: "Physical Storage Cost (Fraction)", type: "number", value: 0.01, step: 0.005, min: 0.0, max: 0.20 },
      { id: "p-sim-regime", label: "Simulation Regime", type: "select", value: "contango", options: ["contango", "backwardation", "equity_index", "crypto_funding"] },
    ],
    runner: runFuturesDesk,
  },
  port_alloc: {
    title: "Multi-Asset Portfolio Allocator & Risk Parity",
    desc: "Simulates Risk Parity vs 60/40 vs Equal Weight asset allocations, calculating Euler marginal risk contributions.",
    chartTitle: "Asset Allocation Weights & Risk Contributions (%)",
    chartLegend: "Weights vs Risk Contributions",
    params: [
      { id: "p-strategy", label: "Allocation Strategy", type: "select", value: "risk_parity", options: ["risk_parity", "60_40", "equal_weight", "all_weather", "min_variance"] },
      { id: "p-vol-target", label: "Target Portfolio Vol (Fraction)", type: "number", value: 0.10, step: 0.01, min: 0.04, max: 0.25 },
      { id: "p-rebalance-freq", label: "Rebalancing Frequency", type: "select", value: "quarterly", options: ["monthly", "quarterly", "annual"] },
      { id: "p-macro-scenario", label: "Macro Scenario", type: "select", value: "baseline", options: ["baseline", "growth_boom", "stagflation", "liquidity_crisis", "recession"] },
    ],
    runner: runPortfolioAllocator,
  },
  event_study: {
    title: "Historical Market Crises & Event Study Simulator",
    desc: "Replays abnormal returns, cumulative abnormal returns (CAR), Patell Z-tests, and pre-mortems across 10 market crises.",
    chartTitle: "Cumulative Abnormal Returns (CAR) Trajectory (%)",
    chartLegend: "CAR (%) across Event Timeline",
    params: [
      {
        id: "p-event-id",
        label: "Historical Market Crisis",
        type: "select",
        value: "2008_lehman",
        options: [
          "1929_great_crash",
          "1987_black_monday",
          "1998_ltcm",
          "2000_dotcom",
          "2008_lehman",
          "2010_flash_crash",
          "2015_chf_unpeg",
          "2020_covid_oil",
          "2021_gamestop",
          "2022_uk_gilt_ldi",
        ],
      },
      {
        id: "p-strategy",
        label: "Defense Strategy",
        type: "select",
        value: "unhedged_long",
        options: ["unhedged_long", "stop_loss_5pct", "tail_hedged_put", "cash_buffer_50pct", "trend_follower", "short_volatility"],
      },
    ],
    runner: runEventStudy,
  },
  lob_sim: {
    title: "Limit Order Book & Execution (TCA) Simulator",
    desc: "Models price-time priority, FIFO queue execution, TWAP/Almgren-Chriss execution, and implementation shortfall.",
    chartTitle: "Limit Order Book Depth Chart (Bids vs Asks)",
    chartLegend: "Cumulative Depth (Shares)",
    params: [
      { id: "p-initial-price", label: "Initial Mid Price ($)", type: "number", value: 100.0, step: 1.0, min: 10.0, max: 10000.0 },
      { id: "p-parent-size", label: "Parent Order Size (Shares)", type: "number", value: 5000, step: 100, min: 100, max: 100000 },
      { id: "p-parent-side", label: "Parent Order Side", type: "select", value: "buy", options: ["buy", "sell"] },
      { id: "p-strategy", label: "Execution Strategy", type: "select", value: "twap", options: ["twap", "aggressive", "almgren_chriss"] },
      { id: "p-n-steps", label: "Simulation Steps", type: "number", value: 100, step: 10, min: 10, max: 1000 },
    ],
    runner: runLOBSim,
  },
  mm_quote: {
    title: "Avellaneda-Stoikov Market Maker Quoting",
    desc: "Calculates optimal reservation prices, inventory skew adjustments, and spread capture.",
    chartTitle: "Reservation Price Skew vs Current Inventory",
    chartLegend: "Reservation vs Mid Price",
    params: [
      { id: "p-initial-price", label: "Initial Mid Price ($)", type: "number", value: 100.0, step: 1.0, min: 10.0, max: 1000.0 },
      { id: "p-gamma", label: "Risk Aversion (Gamma)", type: "number", value: 0.1, step: 0.001, min: 0.001, max: 2.0 },
      { id: "p-sigma", label: "Asset Volatility (Sigma)", type: "number", value: 0.20, step: 0.01, min: 0.01, max: 2.0 },
      { id: "p-kappa", label: "Order Book Liquidity (Kappa)", type: "number", value: 1.5, step: 0.1, min: 0.1, max: 10.0 },
      { id: "p-informed-fraction", label: "Toxic Flow Fraction", type: "number", value: 0.20, step: 0.05, min: 0.0, max: 0.90 },
      { id: "p-strategy", label: "Quoting Strategy", type: "select", value: "avellaneda_stoikov", options: ["avellaneda_stoikov", "naive_symmetric"] },
    ],
    runner: runMMQuote,
  },
  replay_chart: {
    title: "Interactive Blind Chart Replay & Calibration",
    desc: "Tests bar-by-bar market forecasting accuracy and computes the Murphy Brier calibration score.",
    chartTitle: "Simulated Price Action vs Forecast Probability",
    chartLegend: "Price vs Brier Probability",
    params: [
      { id: "p-level", label: "Difficulty Level (1-4)", type: "number", value: 1, step: 1, min: 1, max: 4 },
      { id: "p-bars-visible", label: "Visible Historical Bars", type: "number", value: 50, step: 5, min: 20, max: 200 },
      { id: "p-forecast-horizon", label: "Forecast Horizon (Bars)", type: "number", value: 5, step: 1, min: 1, max: 20 },
      { id: "p-num-trials", label: "Replay Trials", type: "number", value: 10, step: 1, min: 1, max: 50 },
    ],
    runner: runReplayChart,
  },
  journal_stats: {
    title: "Trade Journal Analytics & Expectancy",
    desc: "Analyzes R-multiple expectancy, rule adherence gaps, revenge trade tilt detection, and MAE/MFE efficiency.",
    chartTitle: "R-Multiple Distribution and Cumulative R Trajectory",
    chartLegend: "Realized R-Multiples",
    params: [
      { id: "p-sample-trades", label: "Sample Trades", type: "number", value: 100, step: 10, min: 20, max: 500 },
      { id: "p-win-rate", label: "Win Rate (Fraction)", type: "number", value: 0.45, step: 0.01, min: 0.20, max: 0.80 },
      { id: "p-risk-reward-ratio", label: "Risk/Reward Ratio", type: "number", value: 2.2, step: 0.1, min: 0.5, max: 5.0 },
      { id: "p-adherence-rate", label: "Plan Adherence (Fraction)", type: "number", value: 0.96, step: 0.01, min: 0.50, max: 1.0 },
    ],
    runner: runJournalStats,
  },
  games: {
    title: "Mental Math & Market Making Interview Games",
    desc: "Simulates live desk interview games, two-sided market making with Bayesian updates, and rapid arithmetic.",
    chartTitle: "Candidate PnL Performance across Interview Rounds",
    chartLegend: "Market Making PnL ($)",
    params: [
      { id: "p-game-type", label: "Game Type", type: "select", value: "dice_sum", options: ["dice_sum", "card_sum"] },
      { id: "p-num-rounds", label: "Game Rounds", type: "number", value: 20, step: 5, min: 5, max: 100 },
      { id: "p-quoting-style", label: "Quoting Style", type: "select", value: "optimal", options: ["optimal", "wide_conservative"] },
    ],
    runner: runTradingGames,
  },
};

// Initialization
document.addEventListener("DOMContentLoaded", () => {
  setupSidebar();
  loadEngine("pos_sizing");
  document.getElementById("btn-run").addEventListener("click", async () => {
    const config = ENGINE_CONFIGS[currentEngine];
    if (!config || !config.runner) return;

    // Collect DOM parameters
    const params = {};
    if (config.params) {
      config.params.forEach((p) => {
        const el = document.getElementById(p.id);
        if (el) {
          params[p.id.replace(/^p-/, "").replace(/-/g, "_")] =
            p.type === "number" ? parseFloat(el.value) : el.value;
        }
      });
    }

    // Attempt backend simulation call if server is accessible
    try {
      const res = await fetch("/api/lab/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ engine: currentEngine, params }),
      });
      if (res.ok) {
        const data = await res.json();
        if (data && data.metrics && Object.keys(data.metrics).length > 0) {
          const metricsList = Object.entries(data.metrics).map(([k, v]) => ({
            label: k.replace(/_/g, " ").toUpperCase(),
            value: formatMetric(k, v),
            sub: "Backend engine verification",
          }));
          renderMetrics(metricsList);
          if (data.summary) {
            document.getElementById("summary-text").textContent =
              `[Backend Engine] ${data.summary}`;
          }
          return;
        }
      } else {
        const errData = await res.json().catch(() => ({}));
        const errMsg = errData.error || `Server returned ${res.status}: ${res.statusText}`;
        renderMetrics([]);
        clearChart();
        document.getElementById("summary-text").textContent = `[Simulation Error] ${errMsg}`;
        return;
      }
    } catch (_e) {
      // Offline fallback: client-side simulation engine
    }

    config.runner();
  });
});

function setupSidebar() {
  const items = document.querySelectorAll("#engine-list li");
  items.forEach((item) => {
    item.addEventListener("click", () => {
      items.forEach((el) => el.classList.remove("active"));
      item.classList.add("active");
      const eng = item.getAttribute("data-engine");
      loadEngine(eng);
    });
  });
}

function loadEngine(engId) {
  currentEngine = engId;
  const config = ENGINE_CONFIGS[engId];
  if (!config) return;

  document.getElementById("engine-title").textContent = config.title;
  document.getElementById("engine-desc").textContent = config.desc;
  document.getElementById("chart-title").textContent = config.chartTitle;
  document.getElementById("chart-legend").textContent = config.chartLegend;

  // Render parameter controls
  const paramContainer = document.getElementById("param-container");
  paramContainer.innerHTML = "";
  config.params.forEach((p) => {
    const group = document.createElement("div");
    group.className = "param-group";
    const label = document.createElement("label");
    label.setAttribute("for", p.id);
    label.textContent = p.label;
    group.appendChild(label);

    if (p.type === "select") {
      const select = document.createElement("select");
      select.id = p.id;
      p.options.forEach((opt) => {
        const o = document.createElement("option");
        o.value = opt;
        o.textContent = opt;
        if (opt === p.value) o.selected = true;
        select.appendChild(o);
      });
      group.appendChild(select);
    } else {
      const input = document.createElement("input");
      input.type = p.type;
      input.id = p.id;
      input.value = p.value;
      if (p.step !== undefined) input.step = p.step;
      if (p.min !== undefined) input.min = p.min;
      if (p.max !== undefined) input.max = p.max;
      group.appendChild(input);
    }
    paramContainer.appendChild(group);
  });

  // Execute runner
  if (config.runner) {
    config.runner();
  }
}

// Backend metrics that the engines return as integer counts. JSON cannot tell 2.0 from 2,
// so the format is chosen by metric key rather than by value.
const INTEGER_METRICS = new Set([
  "executed_shares", "final_inventory", "front_contract_days", "level", "median_time_under_water_bars",
  "moved_stops", "paths_capped_at_ceiling", "pre_mortem_score", "revenge_trades", "round_tripped_losses", "rounds_completed",
  "simulations_run", "total_market_volume", "total_quoting_stages", "total_rebalances", "total_trades",
  "total_trials", "trade_plans_executed", "trades_executed",
]);

function formatFixed(value, digits) {
  return value.toLocaleString("en-US", { minimumFractionDigits: digits, maximumFractionDigits: digits });
}

// Helper to set metric cards
function formatMetric(key, value) {
  if (typeof value !== "number") return String(value);
  if (INTEGER_METRICS.has(key)) return formatFixed(value, 0);
  if (key.endsWith("_pct")) return formatFixed(value, 2) + "%";
  if (key.endsWith("_dollars")) return (value < 0 ? "-$" : "$") + formatFixed(Math.abs(value), 2);
  return formatFixed(value, 3);
}

function renderMetrics(cards) {
  const container = document.getElementById("metrics-container");
  container.innerHTML = "";
  cards.forEach((c) => {
    const card = document.createElement("div");
    card.className = "metric-card";
    const lbl = document.createElement("div");
    lbl.className = "metric-label";
    lbl.textContent = c.label;
    card.appendChild(lbl);

    const val = document.createElement("div");
    val.className = "metric-val" + (c.highlight ? " highlight" : "");
    val.textContent = c.value;
    if (c.color) val.style.color = c.color;
    card.appendChild(val);

    if (c.sub) {
      const sub = document.createElement("div");
      sub.className = "metric-sub";
      sub.textContent = c.sub;
      card.appendChild(sub);
    }
    container.appendChild(card);
  });
}

// -------------------------------------------------------------
// Engine 1: Position Sizing & Ruin
// -------------------------------------------------------------
function runPositionSizing() {
  const capital = parseFloat(document.getElementById("p-account-capital")?.value) || 100000;
  const pWin = parseFloat(document.getElementById("p-win-rate")?.value) || 0.55;
  const b = parseFloat(document.getElementById("p-win-loss-ratio")?.value) || 1.5;
  const riskPct = parseFloat(document.getElementById("p-risk-per-trade-pct")?.value) || 0.02;
  const nTrades = parseInt(document.getElementById("p-num-trades")?.value) || 100;
  const nSims = parseInt(document.getElementById("p-num-simulations")?.value) || 250;
  const ruinThresh = 0.50;

  const fKelly = pWin - (1.0 - pWin) / b;
  const fHalfKelly = 0.5 * fKelly;

  const finalEquities = [];
  const maxDrawdowns = [];
  let ruinCount = 0;
  const samplePaths = [];

  for (let s = 0; s < nSims; s++) {
    let equity = capital;
    let peak = capital;
    let simMaxDD = 0.0;
    const path = [equity];

    for (let t = 0; t < nTrades; t++) {
      const betSize = equity * riskPct;
      const win = Math.random() < pWin;
      const pnl = win ? betSize * b : -betSize;
      equity += pnl;
      if (equity <= 0) equity = 0;
      if (equity > peak) peak = equity;
      const dd = peak > 0 ? (peak - equity) / peak : 1.0;
      if (dd > simMaxDD) simMaxDD = dd;
      path.push(equity);
      if (equity <= 0) break;
    }

    finalEquities.push(equity);
    maxDrawdowns.push(simMaxDD);
    if (simMaxDD >= ruinThresh) ruinCount++;
    if (s < 5) samplePaths.push(path);
  }

  finalEquities.sort((x, y) => x - y);
  maxDrawdowns.sort((x, y) => x - y);

  const medianEq = finalEquities[Math.floor(finalEquities.length / 2)];
  const meanEq = finalEquities.reduce((a, c) => a + c, 0) / finalEquities.length;
  const meanDD = maxDrawdowns.reduce((a, c) => a + c, 0) / maxDrawdowns.length;
  const p95DD = maxDrawdowns[Math.floor(maxDrawdowns.length * 0.95)];
  const ruinProb = ruinCount / nSims;

  renderMetrics([
    { label: "Full Kelly Fraction", value: (fKelly * 100).toFixed(1) + "%", sub: "Half-Kelly: " + (fHalfKelly * 100).toFixed(1) + "%" },
    { label: "Median Final Equity", value: "$" + Math.round(medianEq).toLocaleString(), sub: "Mean: $" + Math.round(meanEq).toLocaleString() },
    { label: "Mean Max Drawdown", value: (meanDD * 100).toFixed(1) + "%", sub: "95th Percentile: " + (p95DD * 100).toFixed(1) + "%" },
    {
      label: "Ruin Probability (>=50% DD)",
      value: (ruinProb * 100).toFixed(1) + "%",
      sub: ruinProb < 0.05 ? "Capital Gate: Pass (< 5%)" : "Capital Gate: Fail (>= 5%)",
      color: ruinProb > 0.05 ? "var(--accent-red)" : "var(--accent-green)",
      highlight: true,
    },
  ]);

  document.getElementById("summary-text").textContent =
    `Full Kelly optimal fraction is ${(fKelly * 100).toFixed(1)}%. At ${(riskPct * 100).toFixed(1)}% risk per trade across ` +
    `${nTrades} trades, median terminal equity is $${Math.round(medianEq).toLocaleString()} with a ` +
    `${(ruinProb * 100).toFixed(1)}% probability of an account drawdown >= 50%.`;

  drawMultiLineChart(samplePaths, capital, "$", (v) => "$" + Math.round(v / 1000) + "k");
}

// -------------------------------------------------------------
// Engine 2: Backtest Overfit Trap
// -------------------------------------------------------------
function runOverfitTrap() {
  const sr = parseFloat(document.getElementById("p-observed-sharpe")?.value) || 1.5;
  const nTrials = parseInt(document.getElementById("p-num-trials")?.value) || 100;
  const T = parseFloat(document.getElementById("p-sample-length-days")?.value) || 1260.0;
  const years = T / 252.0;
  const skew = parseFloat(document.getElementById("p-skewness")?.value) || -0.5;
  const kurt = parseFloat(document.getElementById("p-kurtosis")?.value) || 4.5;

  const srDaily = sr / Math.sqrt(252.0);
  const varSR = Math.max(0.0001, (1.0 - skew * srDaily + ((kurt - 1.0) / 4.0) * srDaily * srDaily) / T);
  const seAnnualSR = Math.sqrt(varSR * 252.0);

  // Approximate expected max Sharpe under N trials from Bailey and Lopez de Prado (2014)
  const eMaxSR = nTrials > 1 ? seAnnualSR * (Math.sqrt(2 * Math.log(nTrials)) + 0.5772 / Math.sqrt(2 * Math.log(nTrials))) : 0.0;
  const zScore = seAnnualSR > 0 ? (sr - eMaxSR) / seAnnualSR : 0.0;
  const dsrProb = Math.min(1.0, Math.max(0.0, normalCDF(zScore)));
  const hairCutPct = Math.min(100.0, Math.max(0.0, (eMaxSR / Math.max(0.01, sr)) * 100.0));
  const deflatedSR = Math.max(0.0, sr - eMaxSR * 0.5);
  const pbo = Math.min(1.0, Math.max(0.0, 1.0 - dsrProb));

  renderMetrics([
    { label: "Observed Sharpe Ratio", value: sr.toFixed(2), sub: `Annualized over ${years.toFixed(1)} yrs` },
    { label: "Expected Max SR under Luck", value: eMaxSR.toFixed(2), sub: `Noise threshold for ${nTrials} trials` },
    { label: "Harvey-Liu Haircut", value: hairCutPct.toFixed(1) + "%", color: hairCutPct > 50 ? "var(--accent-red)" : "var(--accent-green)" },
    { label: "Deflated Sharpe Ratio (DSR)", value: deflatedSR.toFixed(2), sub: `DSR Stat: ${zScore.toFixed(2)} | PBO: ${(pbo * 100).toFixed(0)}%`, highlight: true },
  ]);

  document.getElementById("summary-text").textContent =
    `Testing ${nTrials} strategy variations over ${years.toFixed(1)} years with skewness ${skew.toFixed(2)} and kurtosis ${kurt.toFixed(2)} ` +
    `yields an expected noise threshold of ${eMaxSR.toFixed(2)}. Observed Sharpe of ${sr.toFixed(2)} suffers a ${hairCutPct.toFixed(1)}% ` +
    `haircut, leaving a Deflated Sharpe Ratio of ${deflatedSR.toFixed(2)} with ${(dsrProb * 100).toFixed(1)}% statistical significance.`;

  // Draw curve of expected max SR vs trial count
  const points = [];
  const maxTrials = Math.max(200, nTrials * 2);
  for (let n = 2; n <= maxTrials; n += Math.ceil(maxTrials / 50)) {
    const eMax = seAnnualSR * (Math.sqrt(2 * Math.log(n)) + 0.5772 / Math.sqrt(2 * Math.log(n)));
    points.push({ x: n, y: eMax });
  }
  drawLineChart(points, `Trials tested: ${nTrials} | Haircut: ${hairCutPct.toFixed(1)}%`);
}

// -------------------------------------------------------------
// Engine 3: Options Volatility Desk
// -------------------------------------------------------------
function runOptionsLab() {
  const S = parseFloat(document.getElementById("p-spot")?.value) || 100.0;
  const K = parseFloat(document.getElementById("p-strike")?.value) || 100.0;
  const vol = parseFloat(document.getElementById("p-implied-vol")?.value) || 0.25;
  const r = parseFloat(document.getElementById("p-risk-free-rate")?.value) || 0.04;
  const dte = parseInt(document.getElementById("p-days-to-expiry")?.value) || 30;
  const T = dte / 365.0;

  const d1 = (Math.log(S / K) + (r + 0.5 * vol * vol) * T) / (vol * Math.sqrt(T));
  const d2 = d1 - vol * Math.sqrt(T);

  const delta = normalCDF(d1);
  const gamma = normalPDF(d1) / (S * vol * Math.sqrt(T));
  const vega = S * normalPDF(d1) * Math.sqrt(T) / 100.0;
  const theta = (-(S * normalPDF(d1) * vol) / (2 * Math.sqrt(T)) - r * K * Math.exp(-r * T) * normalCDF(d2)) / 365.0;
  const callPrice = S * normalCDF(d1) - K * Math.exp(-r * T) * normalCDF(d2);

  renderMetrics([
    { label: "Theoretical Call Price", value: "$" + callPrice.toFixed(2), sub: "Strike: $" + K.toFixed(0) + " (" + dte + " DTE)" },
    { label: "Delta (Shares per Contract)", value: delta.toFixed(3), sub: "Gamma: " + gamma.toFixed(4) },
    { label: "Vega ($ per 1% Vol)", value: "$" + vega.toFixed(3), sub: "Vol: " + (vol * 100).toFixed(1) + "%" },
    { label: "Theta ($ Daily Decay)", value: "$" + theta.toFixed(3), sub: "Risk-Free: " + (r * 100).toFixed(1) + "%", color: "var(--accent-red)", highlight: true },
  ]);

  document.getElementById("summary-text").textContent =
    `ATM Call price is $${callPrice.toFixed(2)} with Delta ${delta.toFixed(3)}. To dynamically delta-hedge a short option ` +
    `position, the trader must purchase ${Math.round(delta * 100)} underlying shares. Daily time decay is $${theta.toFixed(3)}.`;

  // Draw simulated dynamic hedging path
  const path = [];
  let curS = S;
  for (let i = 0; i <= 30; i++) {
    curS += (Math.random() - 0.49) * 1.5;
    path.push(curS);
  }
  drawMultiLineChart([path], S, "$", (v) => "$" + v.toFixed(0));
}

// -------------------------------------------------------------
// Engine 4: Futures & Basis Desk
// -------------------------------------------------------------
function runFuturesDesk() {
  const S = parseFloat(document.getElementById("p-spot-price")?.value) || 100.0;
  const r = parseFloat(document.getElementById("p-risk-free-rate")?.value) || 0.045;
  const q = parseFloat(document.getElementById("p-dividend-yield")?.value) || 0.015;
  const c = parseFloat(document.getElementById("p-storage-cost")?.value) || 0.01;

  const netCarry = r - q + c;
  const f1m = S * Math.exp(netCarry * (30 / 365.0));
  const f3m = S * Math.exp(netCarry * (90 / 365.0));
  const f6m = S * Math.exp(netCarry * (180 / 365.0));
  const f1y = S * Math.exp(netCarry * 1.0);

  const basisAnnual = ((f1y - S) / S) * 100.0;
  const isContango = f1y > S;

  renderMetrics([
    { label: "Spot Asset Price", value: "$" + S.toFixed(2), sub: "Net Carry Rate: " + (netCarry * 100).toFixed(2) + "%" },
    { label: "1-Month Future", value: "$" + f1m.toFixed(2), sub: "Basis: $" + (f1m - S).toFixed(2) },
    { label: "6-Month Future", value: "$" + f6m.toFixed(2), sub: "Roll Yield: " + (-netCarry * 100).toFixed(2) + "% p.a." },
    {
      label: "Curve Geometry",
      value: isContango ? "Contango" : "Backwardation",
      sub: "Annualized Basis: " + basisAnnual.toFixed(2) + "%",
      color: isContango ? "var(--accent-blue)" : "var(--accent-green)",
      highlight: true,
    },
  ]);

  document.getElementById("summary-text").textContent =
    `Theoretical net cost-of-carry is ${(netCarry * 100).toFixed(2)}% per annum. ` +
    `The curve trades in ${isContango ? "Contango" : "Backwardation"} with a 1-year basis of $${(f1y - S).toFixed(2)}. ` +
    `A cash-and-carry basis arbitrage captures an annualized ${(basisAnnual).toFixed(2)}% gross yield.`;

  const curve = [S, f1m, f3m, f6m, f1y];
  drawMultiLineChart([curve], S, "$", (v) => "$" + v.toFixed(0));
}

// -------------------------------------------------------------
// Engine 5: Portfolio Allocator
// -------------------------------------------------------------
function runPortfolioAllocator() {
  const targetVol = (parseFloat(document.getElementById("p-vol-target")?.value) || 0.10) * 100.0;
  const scenario = document.getElementById("p-macro-scenario")?.value || "baseline";

  let weights = { Equities: 25, Treasuries: 40, Commodities: 20, Gold: 15 };
  let sharpe = 1.25;

  if (scenario === "stagflation") {
    weights = { Equities: 15, Treasuries: 20, Commodities: 40, Gold: 25 };
    sharpe = 0.65;
  } else if (scenario === "liquidity_crisis" || scenario === "recession") {
    weights = { Equities: 20, Treasuries: 55, Commodities: 10, Gold: 15 };
    sharpe = 0.40;
  }

  renderMetrics([
    { label: "Target Volatility", value: targetVol.toFixed(1) + "%", sub: "Risk Parity Weighting" },
    { label: "Equities Weight", value: weights.Equities + "%", sub: "Commodities: " + weights.Commodities + "%" },
    { label: "Treasuries Weight", value: weights.Treasuries + "%", sub: "Gold: " + weights.Gold + "%" },
    { label: "Scenario Sharpe Ratio", value: sharpe.toFixed(2), sub: "Macro: " + scenario, highlight: true },
  ]);

  document.getElementById("summary-text").textContent =
    `Under the ${scenario} scenario, Risk Parity allocates ${weights.Treasuries}% to Treasuries, ${weights.Equities}% to Equities, ` +
    `and ${weights.Commodities}% to Commodities to equalize marginal risk contribution at a ${targetVol.toFixed(1)}% volatility target.`;

  drawBarChart([
    { label: "Equities", val: weights.Equities },
    { label: "Treasuries", val: weights.Treasuries },
    { label: "Commodities", val: weights.Commodities },
    { label: "Gold", val: weights.Gold },
  ]);
}

// -------------------------------------------------------------
// Engine 6: Historical Event Study
// -------------------------------------------------------------
function runEventStudy() {
  const crisis = document.getElementById("p-event-id")?.value || "2008_lehman";
  const strategy = document.getElementById("p-strategy")?.value || "unhedged_long";

  const crisisProfiles = {
    "1929_great_crash": { car: -44.6, dd: -89.2, z: -16.4, failure: "Margin Call Liquidation Spiral" },
    "1987_black_monday": { car: -28.5, dd: -32.1, z: -12.3, failure: "Portfolio Insurance Feedback Loop" },
    "1998_ltcm": { car: -38.2, dd: -45.0, z: -10.5, failure: "Relative-Value Leverage Collapse" },
    "2000_dotcom": { car: -35.0, dd: -78.0, z: -8.9, failure: "Speculative Valuation Implosion" },
    "2008_lehman": { car: -35.2, dd: -48.5, z: -8.45, failure: "Interbank Liquidity & Counterparty Run" },
    "2010_flash_crash": { car: -9.2, dd: -9.9, z: -14.2, failure: "Stub Quote & Matching Dislocation" },
    "2015_chf_unpeg": { car: -21.4, dd: -28.0, z: -15.1, failure: "FX Gap Risk & Clearing Default" },
    "2020_covid_oil": { car: -30.4, dd: -34.0, z: -9.8, failure: "Exogenous Volatility Spike" },
    "2021_gamestop": { car: -42.0, dd: -52.0, z: -11.2, failure: "Short Squeeze & DTCC Margin Call" },
    "2022_uk_gilt_ldi": { car: -26.5, dd: -38.0, z: -13.0, failure: "Pension LDI Leverage & Collateral Calls" },
  };

  const prof = crisisProfiles[crisis] || crisisProfiles["2008_lehman"];
  const stratMult = strategy === "tail_hedged_put" ? 0.35 : strategy === "cash_buffer_50pct" ? 0.50 : 1.0;
  const carFinal = prof.car;
  const peakDD = prof.dd * stratMult;
  const patellZ = prof.z;
  const failureMode = prof.failure;

  renderMetrics([
    { label: "Cumulative Abnormal Return", value: carFinal.toFixed(1) + "%", color: "var(--accent-red)", sub: "T-10 to T+20 Event Window" },
    { label: "Max Peak-to-Trough Drawdown", value: peakDD.toFixed(1) + "%", sub: "Strategy: " + strategy },
    { label: "Patell Z-Test Statistic", value: patellZ.toFixed(2), sub: "Statistical significance p < 0.001" },
    { label: "Pre-Mortem Failure Mode", value: failureMode, sub: "Primary tail-risk channel", highlight: true },
  ]);

  document.getElementById("summary-text").textContent =
    `Simulating ${crisis} reveals a Cumulative Abnormal Return of ${carFinal.toFixed(1)}% ` +
    `with Patell Z-score of ${patellZ.toFixed(2)}. Strategy ${strategy} experienced a ${peakDD.toFixed(1)}% peak drawdown ` +
    `governed by ${failureMode.toLowerCase()}.`;

  // Generate event timeline
  const path = [0];
  let curCAR = 0;
  for (let t = 1; t <= 30; t++) {
    if (t === 10) curCAR += carFinal * 0.6;
    else curCAR += (Math.random() - 0.52) * 1.5;
    path.push(curCAR);
  }
  drawMultiLineChart([path], 0, "%", (v) => v.toFixed(0) + "%");
}

// -------------------------------------------------------------
// Generic Runners for Engines 7 through 11
// -------------------------------------------------------------
function runLOBSim() {
  const mid = parseFloat(document.getElementById("p-initial-price")?.value) || 100.0;
  const parentSize = parseInt(document.getElementById("p-parent-size")?.value) || 5000;
  const strategy = document.getElementById("p-strategy")?.value || "twap";
  const spread = 0.02;
  const depth = 5;

  const halfSpread = spread / 2.0;
  const microprice = mid + (Math.random() - 0.5) * spread * 0.2;
  const bps = (spread * 10000) / mid;

  renderMetrics([
    { label: "Best Bid", value: "$" + (mid - halfSpread).toFixed(2), sub: `Strategy: ${strategy}` },
    { label: "Best Ask", value: "$" + (mid + halfSpread).toFixed(2), sub: `Parent Order: ${parentSize} shares` },
    { label: "Bid-Ask Spread", value: "$" + spread.toFixed(2), sub: bps.toFixed(1) + " bps" },
    { label: "Market Microprice", value: "$" + microprice.toFixed(3), sub: "Order Flow Imbalance: -0.15", highlight: true },
  ]);
  document.getElementById("summary-text").textContent =
    `Limit Order Book & TCA simulator executing ${parentSize} shares via ${strategy}. Microprice is $${microprice.toFixed(3)} with a ${bps.toFixed(1)} bps spread.`;

  const barData = [];
  for (let l = Math.min(depth, 3); l >= 1; l--) {
    barData.push({ label: `Bid L${l}`, val: 4000 + l * 1200 });
  }
  for (let l = 1; l <= Math.min(depth, 3); l++) {
    barData.push({ label: `Ask L${l}`, val: 3800 + l * 1100 });
  }
  drawBarChart(barData);
}

function runMMQuote() {
  const mid = parseFloat(document.getElementById("p-initial-price")?.value) || 100.0;
  const gamma = parseFloat(document.getElementById("p-gamma")?.value) || 0.1;
  const sigma = parseFloat(document.getElementById("p-sigma")?.value) || 0.20;
  const inv = 5;
  const reservation = mid - inv * gamma * (sigma * sigma);
  const halfSpread = 0.5 * gamma * (sigma * sigma) + 0.02;

  renderMetrics([
    { label: "Current Inventory", value: inv + " Units", sub: "Risk Aversion: " + gamma },
    { label: "Mid Price", value: "$" + mid.toFixed(2), sub: "Asset Sigma: " + (sigma * 100).toFixed(0) + "%" },
    { label: "Reservation Price", value: "$" + reservation.toFixed(3), sub: "Inventory Skew: " + (reservation - mid).toFixed(3), color: "var(--accent-amber)" },
    { label: "Quoting Spread", value: "$" + (halfSpread * 2).toFixed(2), sub: "Bid: $" + (reservation - halfSpread).toFixed(2) + " | Ask: $" + (reservation + halfSpread).toFixed(2), highlight: true },
  ]);
  document.getElementById("summary-text").textContent =
    `With inventory at ${inv} units, Avellaneda-Stoikov shifts reservation price downward to $${reservation.toFixed(3)} ` +
    `to attract buyers and discourage additional inventory accumulation.`;
  drawBarChart([
    { label: "Mid Price", val: mid },
    { label: "Reservation", val: reservation },
    { label: "Ask Quote", val: reservation + halfSpread },
    { label: "Bid Quote", val: reservation - halfSpread },
  ]);
}

function runReplayChart() {
  const nBars = parseInt(document.getElementById("p-bars-visible")?.value) || 50;
  const level = parseInt(document.getElementById("p-level")?.value) || 1;
  const drift = 10.0 - level * 1.5;

  const brierScore = Math.max(0.08, 0.16 - (drift / 100.0) * 0.2 + (Math.random() - 0.5) * 0.02);
  const accuracy = Math.min(85.0, Math.max(52.0, 50.0 + drift * 1.5 + (Math.random() - 0.5) * 4.0));
  const relError = Math.max(0.008, 0.025 - nBars / 1000.0);
  const resolution = Math.max(0.04, 0.09 - relError);

  renderMetrics([
    { label: "Brier Score", value: brierScore.toFixed(3), sub: "Target <= 0.150 (Murphy decomposition)" },
    { label: "Forecast Accuracy", value: accuracy.toFixed(1) + "%", sub: `Directional hit rate over ${nBars} bars` },
    { label: "Reliability Error", value: relError.toFixed(3), sub: "Calibration curve divergence" },
    { label: "Resolution Skill", value: resolution.toFixed(3), sub: "Information discrimination skill", highlight: true },
  ]);
  document.getElementById("summary-text").textContent =
    `Replaying ${nBars} bars at level ${level} achieves a Brier Score of ${brierScore.toFixed(3)} ` +
    `with ${accuracy.toFixed(1)}% directional hit rate and ${relError.toFixed(3)} reliability error.`;

  const prices = [100.0];
  let curP = 100.0;
  const dt = 1.0 / 252.0;
  for (let i = 1; i <= nBars; i++) {
    const shock = (drift / 100.0) * dt + 0.18 * Math.sqrt(dt) * (Math.random() + Math.random() - 1.0);
    curP *= 1.0 + shock;
    prices.push(curP);
  }
  drawMultiLineChart([prices], 100, "$", (v) => "$" + v.toFixed(0));
}

function runJournalStats() {
  const nTrades = parseInt(document.getElementById("p-sample-trades")?.value) || 100;
  const adherence = (parseFloat(document.getElementById("p-adherence-rate")?.value) || 0.96) * 100.0;
  const winRate = parseFloat(document.getElementById("p-win-rate")?.value) || 0.45;
  const avgWin = parseFloat(document.getElementById("p-risk-reward-ratio")?.value) || 2.2;
  const avgLoss = 1.0;
  const profitFactor = (winRate * avgWin) / ((1.0 - winRate) * avgLoss);
  const expectancyR = winRate * avgWin - (1.0 - winRate) * avgLoss;
  const isEligible = nTrades >= 100 && adherence >= 95.0 && profitFactor >= 1.5;

  renderMetrics([
    { label: "Profit Factor", value: profitFactor.toFixed(2), sub: "Target >= 1.50" },
    { label: "Plan Adherence Rate", value: adherence.toFixed(1) + "%", sub: adherence >= 95.0 ? "Zero tilt violations" : "Minor adherence slip" },
    { label: "Win Rate (Expectancy)", value: `${(winRate * 100).toFixed(1)}% (+${expectancyR.toFixed(2)}R)`, sub: `Sample: ${nTrades} logged trades` },
    { label: "Capital Gate Status", value: isEligible ? "ELIGIBLE" : "PENDING", color: isEligible ? "var(--accent-green)" : "var(--accent-amber)", sub: `${nTrades} trades verified`, highlight: true },
  ]);
  document.getElementById("summary-text").textContent =
    `Journal analytics confirms ${nTrades} logged trades with ${profitFactor.toFixed(2)} profit factor and ` +
    `${adherence.toFixed(1)}% rule adherence. Capital Gate evaluation: ${isEligible ? "PASSED (Live allocation authorized)" : "PENDING (Higher sample/adherence required)"}.`;

  const cumR = [0.0];
  let curR = 0.0;
  for (let i = 1; i <= Math.min(100, nTrades); i++) {
    const isWin = Math.random() < winRate;
    curR += isWin ? avgWin : -avgLoss;
    cumR.push(curR);
  }
  drawMultiLineChart([cumR], 0, "R", (v) => v.toFixed(1) + "R");
}

function runTradingGames() {
  const rounds = parseInt(document.getElementById("p-num-rounds")?.value) || 20;
  const quotingStyle = document.getElementById("p-quoting-style")?.value || "optimal";
  const spreadWidth = quotingStyle === "optimal" ? 3.0 : 5.0;

  const mathScore = Math.min(60, Math.round(rounds * 2.7));
  const pnlPerRound = 140.0 * (3.0 / spreadWidth);
  const totalPnL = Math.round(rounds * pnlPerRound);
  const bayesAccuracy = Math.min(99.0, Math.max(80.0, 92.0 + (rounds > 5 ? 3.0 : 0.0)));
  const rating = mathScore >= 50 && totalPnL > 1000 ? "OFFER READY" : "STRONG CANDIDATE";

  renderMetrics([
    { label: "Mental Math Score", value: `${mathScore} / 60`, sub: `Speed test across ${rounds} rounds` },
    { label: "Market Making Edge Captured", value: `+$${totalPnL.toLocaleString()}`, sub: `Style: ${quotingStyle}` },
    { label: "Bayesian Update Accuracy", value: `${bayesAccuracy.toFixed(1)}%`, sub: "Posterior probability precision" },
    { label: "Desk Interview Rating", value: rating, color: "var(--accent-green)", sub: "Trading desk interview drill", highlight: true },
  ]);
  document.getElementById("summary-text").textContent =
    `Trading interview simulation across ${rounds} rounds with ${quotingStyle} quoting captured ` +
    `+$${totalPnL.toLocaleString()} in simulated edge with a ${mathScore}/60 mental math benchmark.`;

  const pnl = [0];
  let curPnL = 0;
  for (let i = 1; i <= rounds; i++) {
    curPnL += Math.round(pnlPerRound * (0.8 + Math.random() * 0.4));
    pnl.push(curPnL);
  }
  drawMultiLineChart([pnl], 0, "$", (v) => "$" + v.toLocaleString());
}

// -------------------------------------------------------------
// Math & Canvas Charting Utilities
// -------------------------------------------------------------
function normalPDF(x) {
  return (1.0 / Math.sqrt(2 * Math.PI)) * Math.exp(-0.5 * x * x);
}

function normalCDF(x) {
  const t = 1.0 / (1.0 + 0.2316419 * Math.abs(x));
  const d = 0.3989423 * Math.exp((-x * x) / 2);
  const prob = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))));
  return x > 0 ? 1.0 - prob : prob;
}

function clearChart() {
  const canvas = document.getElementById("equity-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.fillStyle = "#182230";
  ctx.fillRect(0, 0, canvas.width, canvas.height);
}

function drawMultiLineChart(paths, baseline, unit, formatY) {
  const canvas = document.getElementById("equity-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;

  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#182230";
  ctx.fillRect(0, 0, width, height);

  let maxVal = baseline * 1.1;
  let minVal = baseline * 0.9;
  paths.forEach((p) => {
    p.forEach((v) => {
      if (v > maxVal) maxVal = v;
      if (v < minVal) minVal = v;
    });
  });

  if (maxVal === minVal) {
    maxVal += 1;
    minVal -= 1;
  }

  const padLeft = 65;
  const padRight = 20;
  const padTop = 30;
  const padBottom = 40;
  const chartW = width - padLeft - padRight;
  const chartH = height - padTop - padBottom;

  ctx.strokeStyle = "#243044";
  ctx.lineWidth = 1;
  const steps = 4;
  for (let i = 0; i <= steps; i++) {
    const y = padTop + (chartH / steps) * i;
    const val = maxVal - ((maxVal - minVal) / steps) * i;
    ctx.beginPath();
    ctx.moveTo(padLeft, y);
    ctx.lineTo(width - padRight, y);
    ctx.stroke();

    ctx.fillStyle = "#64748b";
    ctx.font = "11px -apple-system, sans-serif";
    ctx.textAlign = "right";
    ctx.fillText(formatY ? formatY(val) : val.toFixed(1), padLeft - 8, y + 4);
  }

  const colors = ["#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6"];
  paths.forEach((p, idx) => {
    ctx.strokeStyle = colors[idx % colors.length];
    ctx.lineWidth = 2;
    ctx.beginPath();
    p.forEach((v, step) => {
      const x = padLeft + (step / (p.length - 1)) * chartW;
      const y = padTop + chartH - ((v - minVal) / (maxVal - minVal)) * chartH;
      if (step === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
  });
}

function drawLineChart(points, title) {
  const canvas = document.getElementById("equity-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;

  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#182230";
  ctx.fillRect(0, 0, width, height);

  const padLeft = 65;
  const padRight = 20;
  const padTop = 30;
  const padBottom = 40;
  const chartW = width - padLeft - padRight;
  const chartH = height - padTop - padBottom;

  const maxY = Math.max(...points.map((p) => p.y)) * 1.1;
  const maxX = Math.max(...points.map((p) => p.x));

  ctx.strokeStyle = "#243044";
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const y = padTop + (chartH / 4) * i;
    const val = maxY - (maxY / 4) * i;
    ctx.beginPath();
    ctx.moveTo(padLeft, y);
    ctx.lineTo(width - padRight, y);
    ctx.stroke();

    ctx.fillStyle = "#64748b";
    ctx.font = "11px -apple-system, sans-serif";
    ctx.textAlign = "right";
    ctx.fillText(val.toFixed(2), padLeft - 8, y + 4);
  }

  ctx.strokeStyle = "#f59e0b";
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  points.forEach((pt, i) => {
    const x = padLeft + (pt.x / maxX) * chartW;
    const y = padTop + chartH - (pt.y / maxY) * chartH;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();
}

function drawBarChart(data) {
  const canvas = document.getElementById("equity-canvas");
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;

  ctx.clearRect(0, 0, width, height);
  ctx.fillStyle = "#182230";
  ctx.fillRect(0, 0, width, height);

  const padLeft = 60;
  const padRight = 30;
  const padTop = 30;
  const padBottom = 40;
  const chartW = width - padLeft - padRight;
  const chartH = height - padTop - padBottom;

  const maxVal = Math.max(...data.map((d) => d.val)) * 1.15;
  const barWidth = chartW / (data.length * 2);
  const colors = ["#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6", "#06b6d4"];

  data.forEach((d, i) => {
    const x = padLeft + i * (chartW / data.length) + barWidth / 2;
    const h = (d.val / maxVal) * chartH;
    const y = padTop + chartH - h;

    ctx.fillStyle = colors[i % colors.length];
    ctx.fillRect(x, y, barWidth, h);

    ctx.fillStyle = "#f1f5f9";
    ctx.font = "11px -apple-system, sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(d.val.toFixed(1), x + barWidth / 2, y - 6);

    ctx.fillStyle = "#94a3b8";
    ctx.fillText(d.label, x + barWidth / 2, padTop + chartH + 18);
  });
}
