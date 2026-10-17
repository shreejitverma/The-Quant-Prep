/**
 * Markets Mastery OS - Trading Lab Web Runner
 * Pure Vanilla JavaScript simulation and Canvas rendering.
 */

function runMonteCarloSimulation() {
  const capital = parseFloat(document.getElementById("p-capital").value) || 100000;
  const pWin = parseFloat(document.getElementById("p-winrate").value) || 0.55;
  const b = parseFloat(document.getElementById("p-winloss").value) || 1.5;
  const riskPct = (parseFloat(document.getElementById("p-risk").value) || 2.0) / 100.0;
  const nTrades = parseInt(document.getElementById("p-trades").value) || 100;
  const nSims = parseInt(document.getElementById("p-sims").value) || 250;
  const ruinThresh = 0.50;

  // Kelly calculation: f* = p - (1 - p) / b
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

    if (s < 5) {
      samplePaths.push(path);
    }
  }

  finalEquities.sort((a, b) => a - b);
  maxDrawdowns.sort((a, b) => a - b);

  const medianEquity = finalEquities[Math.floor(finalEquities.length / 2)];
  const meanEquity = finalEquities.reduce((a, b) => a + b, 0) / finalEquities.length;
  const meanDD = maxDrawdowns.reduce((a, b) => a + b, 0) / maxDrawdowns.length;
  const p95DD = maxDrawdowns[Math.floor(maxDrawdowns.length * 0.95)];
  const ruinProb = ruinCount / nSims;

  // Update DOM metrics
  document.getElementById("m-kelly").textContent = (fKelly * 100).toFixed(1) + "%";
  document.getElementById("m-half-kelly").textContent = "Half-Kelly: " + (fHalfKelly * 100).toFixed(1) + "%";
  document.getElementById("m-median").textContent = "$" + Math.round(medianEquity).toLocaleString();
  document.getElementById("m-mean").textContent = "Mean: $" + Math.round(meanEquity).toLocaleString();
  document.getElementById("m-drawdown").textContent = (meanDD * 100).toFixed(1) + "%";
  document.getElementById("m-p95-dd").textContent = "95th Percentile: " + (p95DD * 100).toFixed(1) + "%";
  document.getElementById("m-ruin").textContent = (ruinProb * 100).toFixed(1) + "%";

  const ruinElem = document.getElementById("m-ruin");
  if (ruinProb > 0.05) {
    ruinElem.style.color = "var(--accent-red)";
  } else {
    ruinElem.style.color = "var(--accent-green)";
  }

  document.getElementById("summary-text").textContent =
    `Kelly fraction is ${(fKelly * 100).toFixed(1)}%. At ${(riskPct * 100).toFixed(1)}% risk per trade across ` +
    `${nTrades} trades, median terminal equity is $${Math.round(medianEquity).toLocaleString()} ` +
    `with a ${(ruinProb * 100).toFixed(1)}% probability of an account drawdown >= 50%.`;

  renderCanvasChart(samplePaths, capital);
}

function renderCanvasChart(samplePaths, capital) {
  const canvas = document.getElementById("equity-canvas");
  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;

  ctx.clearRect(0, 0, width, height);

  // Background
  ctx.fillStyle = "#182230";
  ctx.fillRect(0, 0, width, height);

  // Find max value across sample paths
  let maxVal = capital * 1.5;
  samplePaths.forEach((path) => {
    path.forEach((val) => {
      if (val > maxVal) maxVal = val;
    });
  });

  const padLeft = 60;
  const padRight = 20;
  const padTop = 30;
  const padBottom = 40;
  const chartW = width - padLeft - padRight;
  const chartH = height - padTop - padBottom;

  // Draw grid lines
  ctx.strokeStyle = "#243044";
  ctx.lineWidth = 1;
  const gridSteps = 4;
  for (let i = 0; i <= gridSteps; i++) {
    const y = padTop + (chartH / gridSteps) * i;
    const val = maxVal - (maxVal / gridSteps) * i;
    ctx.beginPath();
    ctx.moveTo(padLeft, y);
    ctx.lineTo(width - padRight, y);
    ctx.stroke();

    ctx.fillStyle = "#64748b";
    ctx.font = "10px sans-serif";
    ctx.textAlign = "right";
    ctx.fillText("$" + Math.round(val / 1000) + "k", padLeft - 8, y + 3);
  }

  // Draw baseline capital line
  const baseY = padTop + chartH - (capital / maxVal) * chartH;
  ctx.strokeStyle = "rgba(255, 255, 255, 0.2)";
  ctx.setLineDash([4, 4]);
  ctx.beginPath();
  ctx.moveTo(padLeft, baseY);
  ctx.lineTo(width - padRight, baseY);
  ctx.stroke();
  ctx.setLineDash([]);

  // Colors for paths
  const colors = ["#3b82f6", "#10b981", "#f59e0b", "#ec4899", "#8b5cf6"];

  samplePaths.forEach((path, pathIdx) => {
    ctx.strokeStyle = colors[pathIdx % colors.length];
    ctx.lineWidth = 2;
    ctx.beginPath();

    const nPoints = path.length;
    path.forEach((val, ptIdx) => {
      const x = padLeft + (ptIdx / (nPoints - 1)) * chartW;
      const y = padTop + chartH - (val / maxVal) * chartH;
      if (ptIdx === 0) {
        ctx.moveTo(x, y);
      } else {
        ctx.lineTo(x, y);
      }
    });

    ctx.stroke();
  });
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("btn-run").addEventListener("click", runMonteCarloSimulation);
  // Initial run on page load
  runMonteCarloSimulation();
});
