---
type: cfa-hub
tags: [cfa/l2, hub]
exam_date: 2026-11-24
plan_start: 2026-08-26
weekday_hours: 3.5
weekend_hours: 7
cssclasses: [cfa-hub]
---
# CFA Level II Hub

Exam: 24 November 2026.
Front door for the whole platform.
Everything below is computed from note properties; nothing here is edited by hand.

## Today

```dataviewjs
const hub = dv.current();
const today = dv.date("today");
const exam = dv.date(hub.exam_date);
const start = dv.date(hub.plan_start);
const daysLeft = Math.ceil(exam.diff(today, "days").days);
const dayN = Math.floor(today.diff(start, "days").days) + 1;
const week = Math.floor((dayN - 1) / 7) + 1;
const pass = week <= 7 ? "Pass 1 (learn)" : week <= 10 ? "Pass 2 (item sets)" : "Pass 3 (mocks)";
dv.paragraph(`**${daysLeft} days to the exam.** Day ${dayN}, week ${week}, ${pass}.`);

const lms = dv.pages('"17-CFA/CFA-L-2"').where(p => p.type === "cfa-lm");
const due = lms.where(p => p.next_review && dv.date(p.next_review) <= today).sort(p => p.next_review);
dv.header(4, `LM reviews due (${due.length})`);
dv.list(due.map(p => `${p.file.link} (mastery ${p.mastery ?? 0})`));

const errors = dv.pages('"17-CFA/CFA-L-2/23-Error-Log"').where(p => p.type === "cfa-error" && p.resolved !== true);
const stale = errors.where(p => p.date && today.diff(dv.date(p.date), "days").days >= 7);
dv.header(4, `Unresolved errors: ${errors.length} (stale 7+ days: ${stale.length})`);
dv.list(stale.limit(10).map(p => `${p.file.link}: ${p.rule ?? ""}`));

const decks = lms.where(p => p.status && p.status !== "not-started").map(p => `#flashcards/cfa-l2/${p.topic_slug}/lm${String(p.lm).padStart(2,"0")}`);
dv.header(4, "SRS decks in rotation");
dv.paragraph(decks.length ? decks.join(", ") : "None yet: start a module to add its deck.");
```

```tasks
not done
tags include #cfa/plan
due before tomorrow
sort by due
short mode
```

## Mastery heatmap

```dataviewjs
const lms = dv.pages('"17-CFA/CFA-L-2"').where(p => p.type === "cfa-lm").sort(p => `${p.topic_code}-${String(p.lm).padStart(2,"0")}`);
const color = m => m >= 85 ? "#1b7f3b" : m >= 70 ? "#5aa02c" : m >= 50 ? "#d9a300" : m > 0 ? "#d9541e" : "#777";
const byTopic = {};
for (const p of lms) (byTopic[p.topic] ??= []).push(p);
let html = "";
for (const [topic, arr] of Object.entries(byTopic)) {
  html += `<div style="margin:4px 0"><span style="display:inline-block;width:230px">${topic}</span>`;
  for (const p of arr) {
    const m = p.mastery ?? 0;
    html += `<a href="${p.file.path}" class="internal-link" title="LM${p.lm} ${p.title}: ${m}" style="display:inline-block;width:34px;height:22px;margin:1px;background:${color(m)};color:#fff;font-size:11px;text-align:center;line-height:22px;border-radius:3px;text-decoration:none">${p.lm}</a>`;
  }
  html += "</div>";
}
dv.el("div", html || "No LM notes yet.");
```

## Weight vs mastery

```dataviewjs
const weights = {"01":"5-10%","02":"5-10%","03":"10-15%","04":"5-10%","05":"10-15%","06":"10-15%","07":"5-10%","08":"5-10%","09":"10-15%","10":"10-15%"};
const lms = dv.pages('"17-CFA/CFA-L-2"').where(p => p.type === "cfa-lm");
const rows = [];
for (const code of Object.keys(weights)) {
  const arr = lms.where(p => String(p.topic_code) === code || String(p.topic_code).padStart(2,"0") === code);
  const n = arr.length;
  const avg = n ? Math.round(arr.array().reduce((s,p) => s + (p.mastery ?? 0), 0) / n) : 0;
  const mastered = arr.where(p => p.status === "mastered").length;
  rows.push([code, arr.length ? arr.array()[0].topic : "", weights[code], n, avg, `${mastered}/${n}`]);
}
dv.table(["Code","Topic","Weight","LMs","Avg mastery","Mastered"], rows);
```

## Attempts, calibration, mock trend

```dataviewjs
const at = dv.pages('"17-CFA/CFA-L-2/22-Attempts"').where(p => p.type === "cfa-attempt").sort(p => p.date);
if (!at.length) { dv.paragraph("No attempts logged yet. Use QuickAdd: CFA log attempt."); }
else {
  const mocks = at.where(p => String(p.source ?? "").toLowerCase().includes("mock"));
  dv.header(4, "Mock scores");
  dv.table(["Date","Source","Score","Percent","Minutes"], mocks.map(p => [p.date, p.source, `${p.score}/${p.max}`, Math.round(100*p.score/p.max) + "%", p.minutes_used]));
  const byTopic = {};
  for (const p of at) {
    const t = p.topic ?? "mixed";
    const b = (byTopic[t] ??= {n:0, acc:0, conf:0});
    b.n++; b.acc += p.score / p.max; b.conf += (p.confidence ?? 3) / 5;
  }
  dv.header(4, "Calibration by topic (confidence minus accuracy; positive means over-confident)");
  dv.table(["Topic","Attempts","Accuracy","Confidence","Gap"], Object.entries(byTopic).map(([t,b]) => [t, b.n, Math.round(100*b.acc/b.n)+"%", Math.round(100*b.conf/b.n)+"%", Math.round(100*(b.conf-b.acc)/b.n)+" pts"]));
}
```

## Errors by cause

```dataview
TABLE WITHOUT ID cause AS "Cause", length(rows) AS "Count"
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error"
GROUP BY cause
SORT length(rows) DESC
```

## Study board

![[17-CFA/CFA-L-2/00-Strategy/Study-Board]]

## Navigation

- [[17-CFA/CFA-L-2/00-Strategy/Study-Plan|Study Plan]] and [[17-CFA/CFA-L-2/00-Strategy/Distinction-Strategy|Distinction Strategy]]
- [[17-CFA/CFA-L-2/00-Strategy/Calculator-Playbook|Calculator Playbook]] and [[17-CFA/CFA-L-2/00-Strategy/Exam-Day-Playbook|Exam Day Playbook]]
- [[17-CFA/CFA-L-2/40-Formula-Sheets/Master-Formula-Sheet|Master Formula Sheet]]
- Topics: [[17-CFA/CFA-L-2/01-Quantitative-Methods/_Index|Quant]], [[17-CFA/CFA-L-2/02-Economics/_Index|Economics]], [[17-CFA/CFA-L-2/03-Financial-Statement-Analysis/_Index|FSA]], [[17-CFA/CFA-L-2/04-Corporate-Issuers/_Index|Corporate Issuers]], [[17-CFA/CFA-L-2/05-Equity-Valuation/_Index|Equity]], [[17-CFA/CFA-L-2/06-Fixed-Income/_Index|Fixed Income]], [[17-CFA/CFA-L-2/07-Derivatives/_Index|Derivatives]], [[17-CFA/CFA-L-2/08-Alternative-Investments/_Index|Alternatives]], [[17-CFA/CFA-L-2/09-Portfolio-Management/_Index|Portfolio Management]], [[17-CFA/CFA-L-2/10-Ethics/_Index|Ethics]]
- Bases: [[17-CFA/CFA-L-2/60-Bases/LM-Status.base|LM Status]], [[17-CFA/CFA-L-2/60-Bases/Attempts.base|Attempts]], [[17-CFA/CFA-L-2/60-Bases/Errors.base|Errors]]
- [[17-CFA/CFA-L-2/00-Strategy/Build-Checklist|Build Checklist]]

Desktop-only blocks: the three `dataviewjs` blocks above.
On mobile, use the Bases and the `tasks` query, which render everywhere.
