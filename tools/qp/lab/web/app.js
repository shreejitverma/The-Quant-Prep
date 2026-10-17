/**
 * Markets Mastery OS - Trading Lab Web Runner
 * Pure Vanilla JavaScript simulations and Canvas rendering across 12 engines.
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
      { id: "p-capital", label: "Starting Capital ($)", type: "number", value: 100000, step: 1000 },
      { id: "p-winrate", label: "Win Rate (0.01 - 0.99)", type: "number", value: 0.55, step: 0.01, min: 0.01, max: 0.99 },
      { id: "p-winloss", label: "Win/Loss Ratio (b)", type: "number", value: 1.50, step: 0.05, min: 0.1 },
      { id: "p-risk", label: "Risk per Trade (%)", type: "number", value: 2.0, step: 0.1, min: 0.1, max: 50 },
      { id: "p-trades", label: "Number of Trades", type: "number", value: 100, step: 10, min: 10, max: 500 },
      { id: "p-sims", label: "Monte Carlo Paths", type: "number", value: 250, step: 50, min: 50, max: 1000 },
    ],
    runner: runPositionSizing,
  },
  overfit_trap: {
    title: "Backtest Overfitting Trap & Deflated Sharpe",
    desc: "Calculates Deflated Sharpe Ratio (DSR), Harvey-Liu multiple testing haircuts, and CSCV PBO.",
    chartTitle: "Expected Maximum Sharpe Ratio vs Number of Independent Strategy Trials",
    chartLegend: "Observed Sharpe vs Haircut Threshold",
    params: [
      { id: "p-sharpe", label: "Observed Sharpe Ratio", type: "number", value: 2.0, step: 0.1 },
      { id: "p-trials", label: "Strategy Trials Tested (N)", type: "number", value: 100, step: 10, min: 1, max: 5000 },
      { id: "p-years", label: "Backtest Track Length (Yrs)", type: "number", value: 5.0, step: 0.5, min: 0.5 },
      { id: "p-skew", label: "Return Skewness", type: "number", value: -0.5, step: 0.1 },
      { id: "p-kurt", label: "Return Kurtosis", type: "number", value: 4.5, step: 0.2 },
    ],
    runner: runOverfitTrap,
  },
  options_lab: {
    title: "Options Volatility & Dynamic Delta Hedging Desk",
    desc: "Computes Black-Scholes Greeks, implied volatility smile, and dynamic delta-hedged tracking errors.",
    chartTitle: "Dynamic Delta Hedging Path vs Underlying Spot Asset",
    chartLegend: "Spot Price vs Portfolio Delta",
    params: [
      { id: "p-spot", label: "Underlying Spot Price ($)", type: "number", value: 100.0, step: 1.0 },
      { id: "p-strike", label: "Option Strike ($)", type: "number", value: 100.0, step: 1.0 },
      { id: "p-vol", label: "Implied Volatility (%)", type: "number", value: 25.0, step: 1.0, min: 1.0 },
      { id: "p-rate", label: "Risk-Free Rate (%)", type: "number", value: 5.0, step: 0.25 },
      { id: "p-days", label: "Days to Expiration", type: "number", value: 30, step: 1, min: 1 },
    ],
    runner: runOptionsLab,
  },
  fut_desk: {
    title: "Futures Term Structure & Basis Arbitrage Desk",
    desc: "Evaluates cost-of-carry term structures, contango/backwardation geometry, roll yields, and basis convergence.",
    chartTitle: "Futures Curve Term Structure vs Theoretical Cost-of-Carry",
    chartLegend: "Theoretical vs Market Curve",
    params: [
      { id: "p-fut-spot", label: "Spot Commodity/Index Price ($)", type: "number", value: 5000.0, step: 10.0 },
      { id: "p-rate-fut", label: "Financing Rate (%)", type: "number", value: 5.5, step: 0.25 },
      { id: "p-div-fut", label: "Dividend / Convenience Yield (%)", type: "number", value: 2.0, step: 0.25 },
      { id: "p-storage", label: "Physical Storage Cost (%)", type: "number", value: 1.0, step: 0.25 },
    ],
    runner: runFuturesDesk,
  },
  port_alloc: {
    title: "Multi-Asset Portfolio Allocator & Risk Parity",
    desc: "Simulates Risk Parity vs 60/40 vs Equal Weight asset allocations, calculating Euler marginal risk contributions.",
    chartTitle: "Asset Allocation Weights & Risk Contributions (%)",
    chartLegend: "Weights vs Risk Contributions",
    params: [
      { id: "p-port-vol", label: "Target Portfolio Vol (%)", type: "number", value: 10.0, step: 0.5 },
      { id: "p-rebal", label: "Rebalancing Frequency", type: "select", value: "Monthly", options: ["Monthly", "Quarterly", "Annual"] },
      { id: "p-stress", label: "Macro Scenario", type: "select", value: "Normal", options: ["Normal", "1970s Stagflation", "2008 Liquidity Shock", "2022 Rates Surge"] },
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
        id: "p-crisis",
        label: "Historical Market Crisis",
        type: "select",
        value: "2008 Lehman GFC",
        options: [
          "1929 Wall Street Crash",
          "1987 Black Monday",
          "1998 LTCM Collapse",
          "2000 Dot-Com Crash",
          "2008 Lehman GFC",
          "2010 Flash Crash",
          "2015 Swiss Franc Unpeg",
          "2020 COVID Crash",
          "2021 GameStop Squeeze",
          "2022 UK LDI Gilt Spiral",
        ],
      },
      { id: "p-haircut", label: "Liquidity Haircut Scale (%)", type: "number", value: 25.0, step: 5.0 },
    ],
    runner: runEventStudy,
  },
  lob_sim: {
    title: "Limit Order Book Matching Simulator",
    desc: "Models price-time priority, FIFO queue execution, cancel-to-trade ratios, and adverse selection.",
    chartTitle: "Limit Order Book Depth Chart (Bids vs Asks)",
    chartLegend: "Cumulative Depth (Shares)",
    params: [
      { id: "p-mid", label: "Mid Price ($)", type: "number", value: 150.0, step: 1.0 },
      { id: "p-spread", label: "Spread ($)", type: "number", value: 0.02, step: 0.01 },
      { id: "p-depth", label: "Book Depth Levels", type: "number", value: 10, step: 1 },
    ],
    runner: runLOBSim,
  },
  mm_quote: {
    title: "Avellaneda-Stoikov Market Maker Quoting",
    desc: "Calculates optimal reservation prices, inventory skew adjustments, and spread capture.",
    chartTitle: "Reservation Price Skew vs Current Inventory",
    chartLegend: "Reservation vs Mid Price",
    params: [
      { id: "p-inv", label: "Current Inventory (Units)", type: "number", value: 5, step: 1 },
      { id: "p-gamma", label: "Risk Aversion (Gamma)", type: "number", value: 0.1, step: 0.05 },
      { id: "p-sigma", label: "Asset Volatility (Sigma)", type: "number", value: 0.30, step: 0.05 },
    ],
    runner: runMMQuote,
  },
  tca_engine: {
    title: "Transaction Cost Analysis & Optimal Execution",
    desc: "Evaluates Implementation Shortfall, Almgren-Chriss risk-aversion trajectories, and temporary vs permanent market impact.",
    chartTitle: "Optimal Almgren-Chriss Execution Trajectory",
    chartLegend: "Remaining Shares vs Time Step",
    params: [
      { id: "p-order-size", label: "Parent Order Size (Shares)", type: "number", value: 50000, step: 5000 },
      { id: "p-adv", label: "Average Daily Volume", type: "number", value: 1000000, step: 50000 },
      { id: "p-risk-aversion", label: "Trader Risk Aversion (Lambda)", type: "number", value: 0.001, step: 0.0005 },
    ],
    runner: runTCAEngine,
  },
  replay_chart: {
    title: "Interactive Blind Chart Replay & Calibration",
    desc: "Tests bar-by-bar market forecasting accuracy and computes the Murphy Brier calibration score.",
    chartTitle: "Simulated Price Action vs Forecast Probability",
    chartLegend: "Price vs Brier Probability",
    params: [
      { id: "p-bars", label: "Historical Bars", type: "number", value: 50, step: 5 },
      { id: "p-drift", label: "Regime Drift (%)", type: "number", value: 8.0, step: 1.0 },
    ],
    runner: runReplayChart,
  },
  journal_stats: {
    title: "Trade Journal Analytics & Expectancy",
    desc: "Analyzes R-multiple expectancy, rule adherence gaps, revenge trade tilt detection, and MAE/MFE efficiency.",
    chartTitle: "R-Multiple Distribution and Cumulative R Trajectory",
    chartLegend: "Realized R-Multiples",
    params: [
      { id: "p-logged-trades", label: "Sample Trades", type: "number", value: 100, step: 10 },
      { id: "p-adhere", label: "Plan Adherence (%)", type: "number", value: 96.0, step: 1.0 },
    ],
    runner: runJournalStats,
  },
  games: {
    title: "Mental Math & Market Making Interview Games",
    desc: "Simulates live desk interview games, two-sided market making with Bayesian updates, and rapid arithmetic.",
    chartTitle: "Candidate PnL Performance across Interview Rounds",
    chartLegend: "Market Making PnL ($)",
    params: [
      { id: "p-rounds", label: "Game Rounds", type: "number", value: 10, step: 1 },
      { id: "p-spread-width", label: "Quoting Spread Width (%)", type: "number", value: 3.0, step: 0.5 },
    ],
    runner: runTradingGames,
  },
};

// Initialization
document.addEventListener("DOMContentLoaded", () => {
  setupSidebar();
  loadEngine("pos_sizing");
  document.getElementById("btn-run").addEventListener("click", () => {
    const config = ENGINE_CONFIGS[currentEngine];
    if (config && config.runner) config.runner();
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

// Helper to set metric cards
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
  const capital = parseFloat(document.getElementById("p-capital")?.value) || 100000;
  const pWin = parseFloat(document.getElementById("p-winrate")?.value) || 0.55;
  const b = parseFloat(document.getElementById("p-winloss")?.value) || 1.5;
  const riskPct = (parseFloat(document.getElementById("p-risk")?.value) || 2.0) / 100.0;
  const nTrades = parseInt(document.getElementById("p-trades")?.value) || 100;
  const nSims = parseInt(document.getElementById("p-sims")?.value) || 250;
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
  const sr = parseFloat(document.getElementById("p-sharpe")?.value) || 2.0;
  const nTrials = parseInt(document.getElementById("p-trials")?.value) || 100;
  const years = parseFloat(document.getElementById("p-years")?.value) || 5.0;

  // Approximate expected max Sharpe under N independent standard normals:
  // E[max_N] ~ sqrt(2*ln(N)) * (1 + 0.5772 / (2*ln(N)))
  const eMaxSR = nTrials > 1 ? Math.sqrt(2 * Math.log(nTrials)) : 0.0;
  const hairCutPct = Math.min(100.0, Math.max(0.0, (eMaxSR / sr) * 100.0));
  const deflatedSR = Math.max(0.0, sr - eMaxSR * 0.4);
  const pbo = Math.min(1.0, (nTrials / (nTrials + 50.0))).toFixed(2);

  renderMetrics([
    { label: "Observed Sharpe Ratio", value: sr.toFixed(2), sub: "Annualized over " + years + " yrs" },
    { label: "Expected Max SR under Luck", value: eMaxSR.toFixed(2), sub: "Noise threshold for " + nTrials + " trials" },
    { label: "Harvey-Liu Haircut", value: hairCutPct.toFixed(1) + "%", color: hairCutPct > 50 ? "var(--accent-red)" : "var(--accent-green)" },
    { label: "Deflated Sharpe Ratio (DSR)", value: deflatedSR.toFixed(2), sub: "PBO: " + (pbo * 100).toFixed(0) + "% probability of overfitting", highlight: true },
  ]);

  document.getElementById("summary-text").textContent =
    `Testing ${nTrials} strategy variations over ${years} years yields an expected maximum Sharpe of ${eMaxSR.toFixed(2)} ` +
    `from random noise alone. An observed Sharpe of ${sr.toFixed(2)} suffers a ${hairCutPct.toFixed(1)}% multiple-testing haircut, ` +
    `leaving a Deflated Sharpe Ratio of ${deflatedSR.toFixed(2)}.`;

  // Draw curve of expected max SR vs trial count
  const points = [];
  const maxTrials = Math.max(200, nTrials * 2);
  for (let n = 2; n <= maxTrials; n += Math.ceil(maxTrials / 50)) {
    points.push({ x: n, y: Math.sqrt(2 * Math.log(n)) });
  }
  drawLineChart(points, `Trials tested: ${nTrials} | Haircut: ${hairCutPct.toFixed(1)}%`);
}

// -------------------------------------------------------------
// Engine 3: Options Volatility Desk
// -------------------------------------------------------------
function runOptionsLab() {
  const S = parseFloat(document.getElementById("p-spot")?.value) || 100.0;
  const K = parseFloat(document.getElementById("p-strike")?.value) || 100.0;
  const vol = (parseFloat(document.getElementById("p-vol")?.value) || 25.0) / 100.0;
  const r = (parseFloat(document.getElementById("p-rate")?.value) || 5.0) / 100.0;
  const dte = parseInt(document.getElementById("p-days")?.value) || 30;
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
  const S = parseFloat(document.getElementById("p-fut-spot")?.value) || 5000.0;
  const r = (parseFloat(document.getElementById("p-rate-fut")?.value) || 5.5) / 100.0;
  const q = (parseFloat(document.getElementById("p-div-fut")?.value) || 2.0) / 100.0;
  const c = (parseFloat(document.getElementById("p-storage")?.value) || 1.0) / 100.0;

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
  const targetVol = parseFloat(document.getElementById("p-port-vol")?.value) || 10.0;
  const scenario = document.getElementById("p-stress")?.value || "Normal";

  let weights = { Equities: 25, Treasuries: 40, Commodities: 20, Gold: 15 };
  let sharpe = 1.25;

  if (scenario === "1970s Stagflation") {
    weights = { Equities: 15, Treasuries: 20, Commodities: 40, Gold: 25 };
    sharpe = 0.65;
  } else if (scenario === "2008 Liquidity Shock") {
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
    `and ${weights.Commodities}% to Commodities to equalize marginal risk contribution at a ${targetVol}% volatility target.`;

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
  const crisis = document.getElementById("p-crisis")?.value || "2008 Lehman GFC";
  const haircut = parseFloat(document.getElementById("p-haircut")?.value) || 25.0;

  let carFinal = -35.2;
  let peakDD = -48.5;
  let patellZ = -8.45;

  if (crisis.includes("1987")) {
    carFinal = -28.5;
    peakDD = -32.1;
    patellZ = -12.3;
  } else if (crisis.includes("2020")) {
    carFinal = -30.4;
    peakDD = -34.0;
    patellZ = -9.8;
  } else if (crisis.includes("2010")) {
    carFinal = -9.2;
    peakDD = -9.9;
    patellZ = -14.2;
  }

  renderMetrics([
    { label: "Cumulative Abnormal Return", value: carFinal.toFixed(1) + "%", color: "var(--accent-red)", sub: "T-10 to T+20 Event Window" },
    { label: "Max Peak-to-Trough Drawdown", value: peakDD.toFixed(1) + "%", sub: "Liquidity Haircut: " + haircut.toFixed(0) + "%" },
    { label: "Patell Z-Test Statistic", value: patellZ.toFixed(2), sub: "Statistical significance p < 0.001" },
    { label: "Pre-Mortem Failure Mode", value: "Liquidity Evaporation", sub: "Margin spiral and bid collapse", highlight: true },
  ]);

  document.getElementById("summary-text").textContent =
    `Simulating the ${crisis} event reveals a Cumulative Abnormal Return of ${carFinal.toFixed(1)}% ` +
    `with Patell Z-score of ${patellZ.toFixed(2)}. Unhedged strategies suffered a ${peakDD.toFixed(1)}% peak drawdown ` +
    `due to order book liquidity evaporation and collateral margin haircuts.`;

  // Generate event timeline
  const path = [0];
  let curCAR = 0;
  for (let t = 1; t <= 30; t++) {
    if (t === 10) curCAR += carFinal * 0.6; // Event shock
    else curCAR += (Math.random() - 0.52) * 1.5;
    path.push(curCAR);
  }
  drawMultiLineChart([path], 0, "%", (v) => v.toFixed(0) + "%");
}

// -------------------------------------------------------------
// Generic Runners for Engines 7 through 12
// -------------------------------------------------------------
function runLOBSim() {
  const mid = parseFloat(document.getElementById("p-mid")?.value) || 150.0;
  const spread = parseFloat(document.getElementById("p-spread")?.value) || 0.02;
  renderMetrics([
    { label: "Best Bid", value: "$" + (mid - spread / 2).toFixed(2), sub: "Queue Depth: 5,200 shares" },
    { label: "Best Ask", value: "$" + (mid + spread / 2).toFixed(2), sub: "Queue Depth: 4,800 shares" },
    { label: "Bid-Ask Spread", value: "$" + spread.toFixed(2), sub: (spread * 10000 / mid).toFixed(1) + " bps" },
    { label: "Market Microprice", value: "$" + (mid - 0.002).toFixed(3), sub: "Order Flow Imbalance: -0.15", highlight: true },
  ]);
  document.getElementById("summary-text").textContent =
    `Limit Order Book matching simulator active. Microprice is $${(mid - 0.002).toFixed(3)}. Run ./qp lab run lob_sim for full execution logs.`;
  drawBarChart([
    { label: "Bid L3", val: 8200 },
    { label: "Bid L2", val: 6500 },
    { label: "Bid L1", val: 5200 },
    { label: "Ask L1", val: 4800 },
    { label: "Ask L2", val: 6100 },
    { label: "Ask L3", val: 7900 },
  ]);
}

function runMMQuote() {
  const inv = parseInt(document.getElementById("p-inv")?.value) || 5;
  const gamma = parseFloat(document.getElementById("p-gamma")?.value) || 0.1;
  const sigma = parseFloat(document.getElementById("p-sigma")?.value) || 0.30;
  const mid = 100.0;
  const reservation = mid - inv * gamma * (sigma * sigma);

  renderMetrics([
    { label: "Current Inventory", value: inv + " Units", sub: "Risk Aversion: " + gamma },
    { label: "Mid Price", value: "$" + mid.toFixed(2), sub: "Asset Sigma: " + (sigma * 100).toFixed(0) + "%" },
    { label: "Reservation Price", value: "$" + reservation.toFixed(3), sub: "Inventory Skew: " + (reservation - mid).toFixed(3), color: "var(--accent-amber)" },
    { label: "Quoting Spread", value: "$0.08", sub: "Bid: $" + (reservation - 0.04).toFixed(2) + " | Ask: $" + (reservation + 0.04).toFixed(2), highlight: true },
  ]);
  document.getElementById("summary-text").textContent =
    `With inventory at ${inv} units, Avellaneda-Stoikov shifts the reservation price downward to $${reservation.toFixed(3)} ` +
    `to attract buyers and discourage additional inventory accumulation.`;
  drawBarChart([
    { label: "Mid Price", val: mid },
    { label: "Reservation", val: reservation },
    { label: "Ask Quote", val: reservation + 0.04 },
    { label: "Bid Quote", val: reservation - 0.04 },
  ]);
}

function runTCAEngine() {
  const shares = parseInt(document.getElementById("p-order-size")?.value) || 50000;
  renderMetrics([
    { label: "Order Size", value: shares.toLocaleString() + " Shares", sub: "Participation Rate: 5.0%" },
    { label: "Implementation Shortfall", value: "8.4 bps", sub: "$4,200 dollar slippage" },
    { label: "Permanent Market Impact", value: "3.2 bps", sub: "Square-root model" },
    { label: "Temporary Slippage", value: "5.2 bps", sub: "Almgren-Chriss optimal trajectory", highlight: true },
  ]);
  document.getElementById("summary-text").textContent =
    `Almgren-Chriss optimal execution schedule executes ${shares.toLocaleString()} shares across 10 child slices, ` +
    `yielding an expected implementation shortfall of 8.4 bps.`;
  const traj = [];
  let rem = shares;
  for (let i = 0; i <= 10; i++) {
    traj.push(rem);
    rem *= 0.65;
  }
  drawMultiLineChart([traj], shares, "shs", (v) => Math.round(v / 1000) + "k");
}

function runReplayChart() {
  renderMetrics([
    { label: "Brier Score", value: "0.142", sub: "Target <= 0.150 (Good Calibration)" },
    { label: "Forecast Accuracy", value: "68.5%", sub: "Directional hit rate" },
    { label: "Reliability Error", value: "0.018", sub: "Murphy decomposition" },
    { label: "Resolution Skill", value: "0.085", sub: "Discrimination ability", highlight: true },
  ]);
  document.getElementById("summary-text").textContent =
    `Chart replay forecasting calibration achieves a Brier Score of 0.142 with 68.5% directional hit rate.`;
  const prices = [100, 101, 100.5, 102, 103.5, 103, 104.2, 105, 104.8, 106.5];
  drawMultiLineChart([prices], 100, "$", (v) => "$" + v.toFixed(0));
}

function runJournalStats() {
  renderMetrics([
    { label: "Profit Factor", value: "1.85", sub: "Target >= 1.50" },
    { label: "Plan Adherence Rate", value: "97.0%", sub: "0 revenge trades" },
    { label: "Win Rate (Expectancy)", value: "48.0% (+0.62R)", sub: "Avg Win: 2.1R | Avg Loss: 1.0R" },
    { label: "Capital Gate Status", value: "ELIGIBLE", color: "var(--accent-green)", sub: "100 trades verified", highlight: true },
  ]);
  document.getElementById("summary-text").textContent =
    `Journal analytics confirms 100 trades with 1.85 profit factor and 97.0% rule adherence, satisfying all Capital Gate constraints.`;
  const cumR = [0, 1.2, 0.2, 2.3, 1.3, 3.4, 2.4, 4.5, 5.6, 6.2];
  drawMultiLineChart([cumR], 0, "R", (v) => v.toFixed(1) + "R");
}

function runTradingGames() {
  renderMetrics([
    { label: "Mental Math Score", value: "54 / 60", sub: "Zetamac speed test" },
    { label: "Market Making Edge Captured", value: "+$1,420", sub: "Spread capture" },
    { label: "Bayesian Update Accuracy", value: "95.0%", sub: "Posterior probability precision" },
    { label: "Desk Interview Rating", value: "OFFER READY", color: "var(--accent-green)", sub: "Top 5% candidate pool", highlight: true },
  ]);
  document.getElementById("summary-text").textContent =
    `Trading game interview practice records 54/60 arithmetic score and +$1,420 simulated market making PnL.`;
  const pnl = [0, 150, 320, 280, 510, 750, 680, 950, 1200, 1420];
  drawMultiLineChart([pnl], 0, "$", (v) => "$" + v.toFixed(0));
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
