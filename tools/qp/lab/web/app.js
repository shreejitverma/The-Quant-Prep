/**
 * Markets Mastery OS - Trading Lab Web Runner
 * Forms, metric cards and Canvas charts for the 11 qp lab engines. Every number shown comes from the
 * Python engines through POST /api/lab/run; the page computes nothing itself, so without the qp server
 * (`./qp serve`) it refuses to run rather than show estimates that would disagree with the engines.
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
  },
  overfit_trap: {
    title: "Backtest Overfitting Trap & Deflated Sharpe",
    desc: "Calculates Deflated Sharpe Ratio (DSR), Harvey-Liu multiple testing haircuts, and CSCV PBO.",
    chartTitle: null,
    chartLegend: null,
    params: [
      { id: "p-observed-sharpe", label: "Observed Sharpe Ratio", type: "number", value: 1.5, step: 0.1, min: 0.1, max: 5.0 },
      { id: "p-num-trials", label: "Strategy Trials Tested (N)", type: "number", value: 100, step: 1, min: 1, max: 10000 },
      { id: "p-sample-length-days", label: "Sample Length (Trading Days)", type: "number", value: 1260, step: 1, min: 100, max: 10000 },
      { id: "p-skewness", label: "Return Skewness", type: "number", value: -0.5, step: 0.1, min: -5.0, max: 5.0 },
      { id: "p-kurtosis", label: "Return Kurtosis", type: "number", value: 4.5, step: 0.2, min: 1.5, max: 30.0 },
    ],
  },
  opt_desk: {
    title: "Options Volatility & Dynamic Delta Hedging Desk",
    desc: "Computes Black-Scholes Greeks, implied volatility smile, and dynamic delta-hedged tracking errors.",
    chartTitle: null,
    chartLegend: null,
    params: [
      { id: "p-scenario", label: "Desk Scenario", type: "select", value: "gamma_scalp", options: ["gamma_scalp", "earnings_crush", "skew_shift", "dispersion"] },
      { id: "p-spot", label: "Underlying Spot Price ($)", type: "number", value: 100.0, step: 1.0, min: 10.0, max: 5000.0 },
      { id: "p-strike", label: "Option Strike ($)", type: "number", value: 100.0, step: 1.0, min: 10.0, max: 5000.0 },
      { id: "p-implied-vol", label: "Implied Volatility (Fraction)", type: "number", value: 0.25, step: 0.01, min: 0.05, max: 2.0 },
      { id: "p-realized-vol", label: "Realized Volatility (Fraction)", type: "number", value: 0.32, step: 0.01, min: 0.05, max: 2.0 },
      { id: "p-days-to-expiry", label: "Days to Expiration", type: "number", value: 30, step: 1, min: 1, max: 365 },
      { id: "p-risk-free-rate", label: "Risk-Free Rate (Fraction)", type: "number", value: 0.04, step: 0.005, min: 0.0, max: 0.20 },
    ],
  },
  fut_desk: {
    title: "Futures Term Structure & Basis Arbitrage Desk",
    desc: "Evaluates cost-of-carry term structures, contango/backwardation geometry, roll yields, and basis convergence.",
    chartTitle: "Front Contract Basis Convergence",
    chartLegend: "Spot vs Front Future",
    params: [
      { id: "p-spot-price", label: "Spot Commodity/Index Price ($)", type: "number", value: 100.0, step: 5.0, min: 10.0, max: 10000.0 },
      { id: "p-risk-free-rate", label: "Financing Rate (Fraction)", type: "number", value: 0.045, step: 0.005, min: 0.0, max: 0.25 },
      { id: "p-dividend-yield", label: "Dividend / Yield (Fraction)", type: "number", value: 0.015, step: 0.005, min: 0.0, max: 0.20 },
      { id: "p-storage-cost", label: "Physical Storage Cost (Fraction)", type: "number", value: 0.01, step: 0.005, min: 0.0, max: 0.20 },
      { id: "p-sim-regime", label: "Simulation Regime", type: "select", value: "contango", options: ["contango", "backwardation", "equity_index", "crypto_funding"] },
    ],
  },
  port_alloc: {
    title: "Multi-Asset Portfolio Allocator & Risk Parity",
    desc: "Simulates Risk Parity vs 60/40 vs Equal Weight asset allocations, calculating Euler marginal risk contributions.",
    chartTitle: "Simulated Portfolio Equity Curve",
    chartLegend: "Monthly Equity ($)",
    params: [
      { id: "p-strategy", label: "Allocation Strategy", type: "select", value: "risk_parity", options: ["risk_parity", "60_40", "equal_weight", "all_weather", "min_variance"] },
      { id: "p-vol-target", label: "Target Portfolio Vol (Fraction)", type: "number", value: 0.10, step: 0.01, min: 0.04, max: 0.25 },
      { id: "p-rebalance-freq", label: "Rebalancing Frequency", type: "select", value: "quarterly", options: ["monthly", "quarterly", "annual"] },
      { id: "p-macro-scenario", label: "Macro Scenario", type: "select", value: "baseline", options: ["baseline", "growth_boom", "stagflation", "liquidity_crisis", "recession"] },
    ],
  },
  event_study: {
    title: "Historical Market Crises & Event Study Simulator",
    desc: "Replays abnormal returns, cumulative abnormal returns (CAR), Patell Z-tests, and pre-mortems across 10 market crises.",
    chartTitle: "Portfolio Equity through the Event Window",
    chartLegend: "Equity ($)",
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
  },
  lob_sim: {
    title: "Limit Order Book & Execution (TCA) Simulator",
    desc: "Models price-time priority, FIFO queue execution, TWAP/Almgren-Chriss execution, and implementation shortfall.",
    chartTitle: "Recent Trade Prices",
    chartLegend: "Last 50 Fills ($)",
    params: [
      { id: "p-initial-price", label: "Initial Mid Price ($)", type: "number", value: 100.0, step: 1.0, min: 10.0, max: 10000.0 },
      { id: "p-parent-size", label: "Parent Order Size (Shares)", type: "number", value: 5000, step: 100, min: 100, max: 100000 },
      { id: "p-parent-side", label: "Parent Order Side", type: "select", value: "buy", options: ["buy", "sell"] },
      { id: "p-strategy", label: "Execution Strategy", type: "select", value: "twap", options: ["twap", "aggressive", "almgren_chriss"] },
      { id: "p-n-steps", label: "Simulation Steps", type: "number", value: 100, step: 10, min: 10, max: 1000 },
    ],
  },
  mm_quote: {
    title: "Avellaneda-Stoikov Market Maker Quoting",
    desc: "Calculates optimal reservation prices, inventory skew adjustments, and spread capture.",
    chartTitle: "Mid Price Path over the Session",
    chartLegend: "Mid Price ($)",
    params: [
      { id: "p-initial-price", label: "Initial Mid Price ($)", type: "number", value: 100.0, step: 1.0, min: 10.0, max: 1000.0 },
      { id: "p-gamma", label: "Risk Aversion (Gamma, per 1% of Mid)", type: "number", value: 0.1, step: 0.001, min: 0.001, max: 2.0 },
      { id: "p-sigma", label: "Annualized Volatility (Sigma)", type: "number", value: 0.20, step: 0.01, min: 0.01, max: 2.0 },
      { id: "p-kappa", label: "Order Arrival Decay (Kappa, per 1% of Mid)", type: "number", value: 1.5, step: 0.1, min: 0.1, max: 10.0 },
      { id: "p-informed-fraction", label: "Toxic Flow Fraction", type: "number", value: 0.20, step: 0.05, min: 0.0, max: 0.90 },
      { id: "p-strategy", label: "Quoting Strategy", type: "select", value: "avellaneda_stoikov", options: ["avellaneda_stoikov", "naive_symmetric"] },
    ],
  },
  replay_chart: {
    title: "Interactive Blind Chart Replay & Calibration",
    desc: "Tests bar-by-bar market forecasting accuracy and computes the Murphy Brier calibration score.",
    chartTitle: "Blind Chart Segments",
    chartLegend: "Visible Bars of Trials 1 to 5",
    params: [
      { id: "p-level", label: "Difficulty Level (1-4)", type: "number", value: 1, step: 1, min: 1, max: 4 },
      { id: "p-bars-visible", label: "Visible Historical Bars", type: "number", value: 50, step: 5, min: 20, max: 200 },
      { id: "p-forecast-horizon", label: "Forecast Horizon (Bars)", type: "number", value: 5, step: 1, min: 1, max: 20 },
      { id: "p-num-trials", label: "Replay Trials", type: "number", value: 10, step: 1, min: 1, max: 50 },
      { id: "p-user-forecasts", label: "Your P(Up) per Trial (comma-separated, blank = simulated)", type: "text", value: "" },
    ],
  },
  journal_stats: {
    title: "Trade Journal Analytics & Expectancy",
    desc: "Analyzes R-multiple expectancy, rule adherence gaps, revenge trade tilt detection, and MAE/MFE efficiency.",
    chartTitle: "Win Rate by Setup",
    chartLegend: "Win Rate (%)",
    params: [
      { id: "p-sample-trades", label: "Sample Trades", type: "number", value: 100, step: 10, min: 20, max: 500 },
      { id: "p-win-rate", label: "Win Rate (Fraction)", type: "number", value: 0.45, step: 0.01, min: 0.20, max: 0.80 },
      { id: "p-risk-reward-ratio", label: "Risk/Reward Ratio", type: "number", value: 2.2, step: 0.1, min: 0.5, max: 5.0 },
      { id: "p-adherence-rate", label: "Plan Adherence (Fraction)", type: "number", value: 0.96, step: 0.01, min: 0.50, max: 1.0 },
    ],
  },
  games: {
    title: "Market Making Interview Games",
    desc: "Quotes dice and card sum games against informed and noise counterparties; the score is the share of the optimal edge captured.",
    chartTitle: null,
    chartLegend: null,
    params: [
      { id: "p-game-type", label: "Game Type", type: "select", value: "dice_sum", options: ["dice_sum", "card_sum"] },
      { id: "p-num-rounds", label: "Game Rounds", type: "number", value: 20, step: 5, min: 5, max: 100 },
      { id: "p-quoting-style", label: "Quoting Style", type: "select", value: "optimal", options: ["optimal", "wide_conservative", "naive_static"] },
    ],
  },
};

// Initialization
document.addEventListener("DOMContentLoaded", () => {
  setupSidebar();
  loadEngine("pos_sizing");
  document.getElementById("btn-run").addEventListener("click", runCurrentEngine);
});

const OFFLINE_MESSAGE =
  "[Offline] The Trading Lab runs only on the qp engines and none is reachable. " +
  "Start the server with ./qp serve and open the lab from it; the page shows no estimates of its own.";

function collectParams(config) {
  const params = {};
  config.params.forEach((p) => {
    const el = document.getElementById(p.id);
    if (el) {
      params[p.id.replace(/^p-/, "").replace(/-/g, "_")] = p.type === "number" ? parseFloat(el.value) : el.value;
    }
  });
  return params;
}

function showChart(visible) {
  const container = document.getElementById("chart-container");
  if (container) container.style.display = visible ? "" : "none";
  if (!visible) clearChart();
}

// Runs the selected engine on the backend and renders exactly what it returns.
async function runCurrentEngine() {
  const engine = currentEngine;
  const config = ENGINE_CONFIGS[engine];
  if (!config) return;
  const summary = document.getElementById("summary-text");

  let res;
  try {
    res = await fetch("/api/lab/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ engine, params: collectParams(config) }),
    });
  } catch (_e) {
    renderMetrics([]);
    showChart(false);
    summary.textContent = OFFLINE_MESSAGE;
    return;
  }

  const data = await res.json().catch(() => null);
  if (!res.ok || !data || !data.metrics) {
    renderMetrics([]);
    showChart(false);
    const errMsg = (data && data.error) || `Server returned ${res.status}: ${res.statusText}`;
    summary.textContent = `[Simulation Error] ${errMsg}`;
    return;
  }

  renderMetrics(
    Object.entries(data.metrics).map(([k, v]) => ({
      label: k.replace(/_/g, " ").toUpperCase(),
      value: formatMetric(k, v),
      sub: "Backend engine verification",
    })),
  );
  summary.textContent = data.summary ? `[Backend Engine] ${data.summary}` : "";
  showChart(renderBackendChart(engine, data));
  if (engine === "lob_sim") renderTimeAndSales((data.data && data.data.trades) || []);
}

// Draws the engine's own series; returns false when the engine has nothing to chart.
function renderBackendChart(engine, result) {
  const d = result.data || {};
  const m = result.metrics || {};
  const dollars = (v) => "$" + Math.round(v).toLocaleString();
  const thousands = (v) => "$" + Math.round(v / 1000) + "k";
  const price = (v) => "$" + v.toFixed(2);
  switch (engine) {
    case "pos_sizing":
      if (!d.sample_paths || !d.sample_paths.length) return false;
      drawMultiLineChart(d.sample_paths, d.sample_paths[0][0], "$", thousands);
      return true;
    case "port_alloc":
      if (!d.equity_curve) return false;
      drawMultiLineChart([d.equity_curve], d.equity_curve[0], "$", thousands);
      return true;
    case "event_study":
      if (!d.timeline) return false;
      drawMultiLineChart([[m.initial_capital, ...d.timeline.map((t) => t.portfolio_equity)]], m.initial_capital, "$", thousands);
      return true;
    case "fut_desk":
      if (!d.convergence_path) return false;
      drawMultiLineChart([d.convergence_path.map((x) => x.spot), d.convergence_path.map((x) => x.future)], m.spot_price, "$", price);
      return true;
    case "lob_sim":
      if (!d.trades || d.trades.length < 2) return false;
      drawMultiLineChart([d.trades.map((t) => t.price)], m.arrival_price, "$", price);
      return true;
    case "mm_quote":
      if (!d.price_history) return false;
      drawMultiLineChart([d.price_history], d.price_history[0], "$", price);
      return true;
    case "replay_chart":
      if (!d.trials || !d.trials.length) return false;
      drawMultiLineChart(d.trials.slice(0, 5).map((t) => t.visible_series), d.trials[0].visible_series[0], "$", price);
      return true;
    case "journal_stats": {
      const setups = Object.entries(d.setup_attribution || {});
      if (!setups.length) return false;
      drawBarChart(setups.map(([name, s]) => ({ label: name, val: s.win_rate })));
      return true;
    }
    default:
      return false;
  }
}

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
  document.getElementById("chart-title").textContent = config.chartTitle || "";
  document.getElementById("chart-legend").textContent = config.chartLegend || "";
  renderMetrics([]);
  showChart(false);
  renderTimeAndSales([]);
  document.getElementById("summary-text").textContent =
    'Click "Run Simulation" to run the qp engine with these parameters.';

  const tapeContainer = document.getElementById("lob-tape-container");
  if (tapeContainer) {
    tapeContainer.style.display = engId === "lob_sim" ? "block" : "none";
  }

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

function renderTimeAndSales(trades) {
  const tbody = document.getElementById("tape-body");
  if (!tbody) return;
  tbody.innerHTML = "";
  if (!trades || trades.length === 0) {
    const row = document.createElement("tr");
    row.innerHTML = `<td colspan="5" style="text-align: center; color: var(--text-muted); padding: 16px;">No recent trades recorded</td>`;
    tbody.appendChild(row);
    return;
  }
  const sorted = [...trades].sort((a, b) => b.time.localeCompare(a.time));
  sorted.forEach((t) => {
    const tr = document.createElement("tr");
    const isBuy = t.side === "buy";
    const sideClass = isBuy ? "side-buy" : "side-sell";
    const sideLabel = isBuy ? "BUY" : "SELL";
    const aggrClass = t.aggressor === "agent" ? "badge-agent" : "badge-market";
    const aggrLabel = t.aggressor === "agent" ? "ALGO" : "MARKET";
    const isBlock = t.size >= 300 ? "block-trade" : "";

    tr.className = isBlock;
    tr.innerHTML = `
      <td class="tape-time">${t.time || "09:30:00"}</td>
      <td class="tape-price ${sideClass}">$${Number(t.price).toFixed(2)}</td>
      <td class="tape-size">${Number(t.size).toLocaleString()}</td>
      <td class="tape-side"><span class="badge ${sideClass}">${sideLabel}</span></td>
      <td class="tape-aggr"><span class="badge ${aggrClass}">${aggrLabel}</span></td>
    `;
    tbody.appendChild(tr);
  });
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
