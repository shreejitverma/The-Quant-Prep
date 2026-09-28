"use strict";
// Quant Prep dashboard. Vanilla JS, no build step. All data comes from the local qp API.

const $app = document.getElementById("app");
const TRACKS = { "quant-trader": "Quant Trader", "quant-research": "Quant Researcher", "quant-dev": "Quant Developer" };
const TRACK_ABBR = { "quant-trader": "T", "quant-research": "R", "quant-dev": "D" };
const MASTERY = ["unseen", "studied", "practiced", "solid", "interview-ready"];
let drillCleanup = null;

// ---------- helpers ----------
function h(tag, attrs, ...kids) {
  const el = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs || {})) {
    if (v === null || v === undefined || v === false) continue;
    if (k === "class") el.className = v;
    else if (k === "html") el.innerHTML = v;
    else if (k.startsWith("on")) el.addEventListener(k.slice(2), v);
    else if (k === "style" && typeof v === "object") Object.assign(el.style, v);
    else el.setAttribute(k, v === true ? "" : v);
  }
  for (const kid of kids.flat()) {
    if (kid === null || kid === undefined || kid === false) continue;
    el.append(kid instanceof Node ? kid : document.createTextNode(String(kid)));
  }
  return el;
}
const pct = (x) => `${Math.round((x || 0) * 100)}%`;
const fmtHours = (x) => `${Math.round(x)} h`;

async function api(path, body) {
  const opts = body === undefined ? {} : { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) };
  const res = await fetch(`/api/${path}`, opts);
  const data = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
  if (!res.ok) throw new Error(data.error || `HTTP ${res.status}`);
  return data;
}

function toast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => t.classList.remove("show"), 1800);
}

function bar(value, cls = "") {
  return h("div", { class: `bar ${cls}` }, h("span", { style: { width: pct(Math.min(1, Math.max(0, value))) } }));
}
function tierChip(t) { return h("span", { class: `chip ${t}` }, t); }
function statusChip(s) { return h("span", { class: `chip ${s}` }, s); }
function trackChips(tracks) { return h("span", { class: "chip", title: tracks.map((t) => TRACKS[t]).join(", ") }, tracks.map((t) => TRACK_ABBR[t]).join("")); }
function page(title, sub, ...actions) {
  return h("div", { class: "page-head" }, h("div", {}, h("h1", {}, title), sub ? h("p", {}, sub) : null), actions.length ? h("div", { class: "row" }, actions) : null);
}
function showError(err) {
  $app.replaceChildren(h("div", { class: "error" }, `Could not load: ${err.message}`), h("p", { class: "muted" }, "Is `./qp serve` still running?"));
}

function masteryControl(topic, onChange, large = false) {
  const wrap = h("span", { class: "row", style: { gap: "10px" } });
  const ctl = h("span", { class: `mastery ${large ? "large" : ""}`, role: "radiogroup", "aria-label": "Mastery" });
  const label = h("span", { class: "mastery-label" }, MASTERY[topic.mastery || 0]);
  const paint = (level) => {
    [...ctl.children].forEach((b, i) => { b.className = i < level ? `on m${level}` : ""; b.setAttribute("aria-checked", String(i + 1 === level)); });
    label.textContent = MASTERY[level];
  };
  for (let i = 1; i <= 4; i++) {
    ctl.append(h("button", {
      type: "button", role: "radio", title: `${i}: ${MASTERY[i]} (click again to clear)`,
      onclick: async (e) => {
        e.preventDefault(); e.stopPropagation();
        const level = topic.mastery === i ? i - 1 : i;
        try {
          const row = await api("mark", { id: topic.id, level });
          topic.mastery = row.mastery; paint(row.mastery);
          toast(`${topic.title}: ${MASTERY[row.mastery]}`);
          onChange && onChange(row);
        } catch (err) { toast(err.message); }
      },
    }));
  }
  paint(topic.mastery || 0);
  wrap.append(ctl);
  if (large) wrap.append(label);
  return wrap;
}

// ---------- markdown ----------
function renderTex(tex, display) {
  if (window.katex) {
    try { return katex.renderToString(tex, { displayMode: display, throwOnError: false, strict: "ignore" }); } catch (e) { /* fall through */ }
  }
  const esc = tex.replace(/&/g, "&amp;").replace(/</g, "&lt;");
  return display ? `<pre><code>${esc}</code></pre>` : `<code>${esc}</code>`;
}

function renderMarkdown(src) {
  const math = [];
  const stash = (tex, display) => { math.push([tex, display]); return `@@M${math.length - 1}@@`; };
  const protect = (text) => text
    .replace(/\$\$([\s\S]+?)\$\$/g, (_, t) => stash(t.trim(), true))
    .replace(/(^|[^\\$])\$(?!\s)([^\n$]+?)(?<!\s)\$(?!\d)/g, (_, pre, t) => pre + stash(t, false));
  // Protect maths outside code, and turn Obsidian callouts into HTML blocks.
  const out = [];
  const lines = src.split("\n");
  let fence = null;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const f = line.match(/^\s*(```|~~~)/);
    if (f) { fence = fence === f[1] ? null : fence || f[1]; out.push(line); continue; }
    if (fence) { out.push(line); continue; }
    const c = line.match(/^> \[!(\w+)\]([-+]?)\s*(.*)$/);
    if (c) {
      const [, type, fold, rawTitle] = c;
      const body = [];
      while (i + 1 < lines.length && lines[i + 1].startsWith(">")) { i++; body.push(lines[i].replace(/^> ?/, "")); }
      let title = rawTitle;
      let idAttr = "";
      if (type === "question") {
        const m = rawTitle.match(/^([a-z0-9-]+)\s*\|\s*(.*)$/);
        if (m) { idAttr = ` data-card="${m[1]}"`; title = m[2]; }
      }
      const titleHtml = window.marked ? marked.parseInline(protect(title)) : protect(title);
      const bodyMd = protect(body.join("\n"));
      if (fold) {
        out.push(`<details class="callout callout-${type}"${idAttr}${fold === "+" ? " open" : ""}><summary>${titleHtml}</summary>`, `<div class="callout-body">`, "", bodyMd, "", `</div></details>`, "");
      } else {
        out.push(`<div class="callout callout-${type}"><div class="callout-title">${titleHtml || type}</div>`, `<div class="callout-body">`, "", bodyMd, "", `</div></div>`, "");
      }
      continue;
    }
    // inline code spans keep their dollars
    out.push(line.split(/(`[^`]*`)/).map((seg, k) => (k % 2 ? seg : protect(seg))).join(""));
  }
  const md = out.join("\n");
  const escaped = `<pre>${src.replace(/&/g, "&amp;").replace(/</g, "&lt;")}</pre>`;
  // Without the markdown renderer and the sanitizer (offline), show the raw text rather than unsanitized HTML.
  if (!window.marked || !window.DOMPurify) return escaped;
  const html = marked.parse(md, { gfm: true }).replace(/@@M(\d+)@@/g, (_, n) => renderTex(math[+n][0], math[+n][1]));
  return DOMPurify.sanitize(html, { ADD_ATTR: ["open", "data-card"] });
}

function resolvePath(base, rel) {
  const parts = base.split("/").slice(0, -1);
  for (const seg of rel.split("/")) {
    if (seg === "..") parts.pop();
    else if (seg && seg !== ".") parts.push(seg);
  }
  return parts.join("/");
}

function mdView(body, notePath, paths) {
  const div = h("div", { class: "md", html: renderMarkdown(body) });
  div.querySelectorAll("a[href]").forEach((a) => {
    const href = a.getAttribute("href");
    if (/^[a-z]+:/i.test(href)) { a.target = "_blank"; a.rel = "noopener"; return; }
    if (href.startsWith("#")) return;
    const [file] = href.split("#");
    const target = resolvePath(notePath, decodeURIComponent(file));
    const id = paths[target] || paths[`${target.replace(/\/$/, "")}/README.md`];
    if (id) a.href = `#/note/${encodeURIComponent(id)}`;
    else { a.href = `/files/${target}`; a.target = "_blank"; }
  });
  div.querySelectorAll("img[src]").forEach((img) => {
    const src = img.getAttribute("src");
    if (!/^[a-z]+:/i.test(src)) img.src = `/files/${resolvePath(notePath, src)}`;
  });
  return div;
}

// ---------- views ----------
async function viewDashboard() {
  const s = await api("summary");
  const active = s.tracks.filter((t) => t.active);
  const written = s.sections.reduce((a, x) => a + x.written, 0);
  const topics = s.sections.reduce((a, x) => a + x.topics, 0);
  const kpis = h("div", { class: "grid g4" },
    kpi("Streak", `${s.streak} day${s.streak === 1 ? "" : "s"}`, "days with any study activity"),
    kpi("Review queue", String(s.queue), `${s.counts.cards_due} due, ${s.counts.cards_seen} of ${s.counts.cards} cards seen`),
    kpi("Mature cards", String(s.counts.cards_mature), "interval of 21 days or more"),
    kpi("Syllabus written", `${written}/${topics}`, "topics at solid or canonical"));
  const tracks = h("div", { class: "grid g3" }, s.tracks.map((t) =>
    h("div", { class: `panel track-card ${t.active ? "" : "inactive"}` },
      h("div", { class: "row" }, h("h3", {}, t.label), h("span", { class: "spacer" }), t.active ? null : h("span", { class: "chip" }, "not targeted")),
      h("div", { class: "pct" }, pct(t.readiness)),
      bar(t.readiness, t.readiness >= 0.75 ? "good" : ""),
      h("div", { class: "meta" }, h("span", {}, `${t.solid}/${t.topics} topics solid`), h("span", {}, `${fmtHours(t.hours_left)} left`)))));
  const next = h("div", { class: "panel" },
    h("div", { class: "panel-head" }, h("h2", {}, "Next up"), h("a", { href: "#/plan", class: "sub" }, "Full plan")),
    s.next.length ? h("div", { class: "list" }, s.next.map((n) =>
      h("div", { class: "list-item" },
        h("div", { class: "grow" },
          h("a", { class: "title", href: `#/note/${encodeURIComponent(n.id)}` }, n.title),
          h("div", { class: "sub" }, n.blocked_by.length ? `Blocked by ${n.blocked_by.join(", ")}` : `${n.hours} h, ${n.status === "seed" ? "not written yet" : n.status}`)),
        tierChip(n.tier),
        masteryControl(n, () => {})))) : h("p", { class: "muted" }, "Every targeted topic is at solid mastery."));
  const firms = h("div", { class: "panel" },
    h("div", { class: "panel-head" }, h("h2", {}, "Firm readiness"), h("a", { href: "#/firms", class: "sub" }, "All firms")),
    s.firms.slice(0, 8).map((f) => h("div", { class: "bar-row" },
      h("a", { class: "name", href: `#/firm/${f.id}` }, f.title), bar(f.readiness), h("span", { class: "v" }, pct(f.readiness)))));
  const heat = heatmap(s.activity, s.today);
  const drillLabels = { arith: "Arithmetic sprint", optiver: "80 in 8", mm: "Market-making P&L" };
  const drills = h("div", { class: "panel" },
    h("div", { class: "panel-head" }, h("h2", {}, "Drills"), h("a", { href: "#/drills", class: "sub" }, "Practice")),
    Object.entries(drillLabels).map(([k, label]) => h("div", { class: "bar-row", style: { gridTemplateColumns: "minmax(0,1fr) auto" } },
      h("span", { class: "name" }, label), h("span", { class: "v" }, s.best[k] !== undefined ? `best ${s.best[k]}` : "not tried"))));
  const sections = h("div", { class: "panel" },
    h("div", { class: "panel-head" }, h("h2", {}, "Sections"), h("span", { class: "sub" }, "readiness and topics written")),
    h("table", { class: "t" },
      h("thead", {}, h("tr", {}, h("th", {}, "Section"), h("th", { class: "hide-sm" }, "Written"), h("th", {}, "Readiness"), h("th", { class: "r" }, ""))),
      h("tbody", {}, s.sections.map((x) => h("tr", {},
        h("td", {}, h("a", { href: `#/syllabus?s=${x.folder}` }, x.title)),
        h("td", { class: "hide-sm muted num" }, `${x.written}/${x.topics}`),
        h("td", { style: { width: "40%" } }, bar(x.readiness, "thin")),
        h("td", { class: "r num muted" }, pct(x.readiness)))))));
  $app.replaceChildren(
    page("Dashboard", `Targeting ${active.map((t) => t.label).join(", ") || "no track"}. ${s.notes} notes, ${s.cards_total} review cards.`,
      h("a", { class: "btn primary", href: "#/review" }, s.queue ? `Review ${s.queue} cards` : "Review"),
      h("a", { class: "btn", href: "#/drills" }, "Drill")),
    h("div", { class: "stack" }, kpis, tracks, h("div", { class: "grid g2" }, next, firms),
      h("div", { class: "grid g2" }, h("div", { class: "panel" }, h("div", { class: "panel-head" }, h("h2", {}, "Activity"), h("span", { class: "sub" }, "last 26 weeks")), heat), drills),
      sections));
}

function kpi(label, value, hint) {
  return h("div", { class: "panel kpi" }, h("div", { class: "label" }, label), h("div", { class: "value" }, value), h("div", { class: "hint" }, hint));
}

function heatmap(activity, todayIso) {
  const today = new Date(`${todayIso}T00:00:00`);
  const start = new Date(today);
  start.setDate(start.getDate() - 7 * 26 + 1);
  start.setDate(start.getDate() - ((start.getDay() + 6) % 7)); // back to Monday so rows are weekdays
  const grid = h("div", { class: "heat", role: "img", "aria-label": "Study activity heatmap" });
  for (let d = new Date(start); d <= today; d.setDate(d.getDate() + 1)) {
    const iso = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
    const a = activity[iso] || {};
    const n = (a.reviews || 0) + 3 * (a.marks || 0) + 5 * (a.drills || 0);
    const lvl = n === 0 ? 0 : n < 10 ? 1 : n < 25 ? 2 : n < 50 ? 3 : 4;
    grid.append(h("i", { class: lvl ? `l${lvl}` : "", title: `${iso}: ${a.reviews || 0} reviews, ${a.marks || 0} topic updates, ${a.drills || 0} drills` }));
  }
  const legend = h("div", { class: "legend" }, "Less", ...[0, 1, 2, 3, 4].map((l) => h("i", { style: { background: `var(--m${l})` } })), "More");
  return h("div", {}, grid, legend);
}

async function viewSyllabus(params) {
  const cat = await api("catalog");
  const state = { q: "", tier: "", written: false, tracks: new Set(), open: params.get("s") };
  const body = h("div", {});
  const search = h("input", { class: "field", type: "search", placeholder: "Search topics", style: { width: "220px" }, oninput: (e) => { state.q = e.target.value.toLowerCase(); draw(); } });
  const tier = h("select", { class: "field", onchange: (e) => { state.tier = e.target.value; draw(); } },
    h("option", { value: "" }, "All tiers"), ["core", "advanced", "senior"].map((t) => h("option", { value: t }, t)));
  const trackToggles = Object.entries(TRACKS).map(([k, label]) => h("button", {
    class: "chip toggle", type: "button", onclick: (e) => { state.tracks.has(k) ? state.tracks.delete(k) : state.tracks.add(k); e.target.classList.toggle("on"); draw(); },
  }, label));
  const written = h("button", { class: "chip toggle", type: "button", onclick: (e) => { state.written = !state.written; e.target.classList.toggle("on"); draw(); } }, "Written only");
  function draw() {
    body.replaceChildren(...cat.sections.map((sec) => {
      if (sec.library) {
        if (state.q || state.tier || state.written || state.tracks.size) return null;
        return h("div", { class: "section-group" }, h("div", { class: "row" }, h("h2", {}, sec.title), h("span", { class: "chip" }, "library"),
          h("span", { class: "spacer" }), sec.readme ? h("a", { class: "btn small", href: `#/note/${encodeURIComponent(sec.readme)}` }, "Overview") : null),
          h("p", { class: "muted", style: { margin: "6px 0 0" } }, "Free-form research notes, best read in Obsidian. Not part of the tracked syllabus."));
      }
      const rows = sec.notes.filter((n) => (n.mastery !== null)
        && (!state.q || n.title.toLowerCase().includes(state.q) || n.id.includes(state.q))
        && (!state.tier || n.tier === state.tier)
        && (!state.written || n.status === "solid" || n.status === "canonical")
        && (!state.tracks.size || n.tracks.some((t) => state.tracks.has(t))));
      const extra = sec.notes.filter((n) => n.mastery === null && n.type !== "firm");
      if (!rows.length && (state.q || state.tier || state.written || state.tracks.size)) return null;
      const done = rows.filter((n) => n.mastery >= 3).length;
      const filtering = state.q || state.tier || state.written || state.tracks.size;
      return h("details", { class: "section-group", open: filtering || state.open === sec.folder || !state.open ? true : null, id: sec.folder },
        h("summary", {}, h("span", { class: "caret" }, "▸"), h("h2", {}, sec.title), sec.private ? h("span", { class: "chip", title: "Loaded from your private overlay; never committed" }, "private") : null,
          rows.length ? h("span", { class: "faint num" }, `${done}/${rows.length} solid`) : null,
          sec.readme ? h("a", { href: `#/note/${encodeURIComponent(sec.readme)}`, class: "btn small", onclick: (e) => e.stopPropagation() }, "Overview") : null),
        h("div", { class: "panel" }, rows.length ? h("table", { class: "t" },
          h("thead", {}, h("tr", {}, h("th", {}, "#"), h("th", {}, "Topic"), h("th", { class: "hide-sm" }, "Tracks"), h("th", {}, "Tier"),
            h("th", { class: "hide-sm" }, "Status"), h("th", { class: "r hide-sm" }, "Hours"), h("th", { class: "r hide-sm" }, "Cards"), h("th", {}, "Mastery"))),
          h("tbody", {}, rows.map((n) => h("tr", {},
            h("td", { class: "ord" }, n.path.split("/").pop().slice(0, 2)),
            h("td", {}, h("a", { href: `#/note/${encodeURIComponent(n.id)}`, class: n.status === "seed" ? "seed-title" : "" }, n.title)),
            h("td", { class: "hide-sm" }, trackChips(n.tracks)),
            h("td", {}, tierChip(n.tier)),
            h("td", { class: "hide-sm" }, statusChip(n.status)),
            h("td", { class: "r num hide-sm muted" }, n.hours),
            h("td", { class: "r num hide-sm muted" }, n.cards || ""),
            h("td", {}, masteryControl(n)))))) : null,
          extra.length ? h("div", { class: "row", style: { padding: "10px" } }, h("span", { class: "faint" }, "Also:"),
            extra.map((n) => h("a", { href: `#/note/${encodeURIComponent(n.id)}`, class: "chip" }, n.title))) : null));
    }));
    if (!body.children.length || [...body.children].every((c) => !c)) body.replaceChildren(h("div", { class: "empty" }, h("h2", {}, "No topics match"), "Clear a filter to see more."));
  }
  draw();
  $app.replaceChildren(page("Syllabus", "Every topic a senior quant is expected to know. Set mastery as you study: 1 studied, 2 practiced, 3 solid, 4 interview-ready."),
    h("div", { class: "row", style: { marginBottom: "18px" } }, search, tier, trackToggles, written), body);
  if (state.open) document.getElementById(state.open)?.scrollIntoView();
}

async function viewNote(id) {
  const n = await api(`note/${encodeURIComponent(id)}`);
  const section = n.path.split("/")[0];
  const side = h("div", { class: "note-side" });
  if (n.mastery !== null) {
    side.append(h("div", { class: "panel" }, h("h3", { style: { marginBottom: "10px" } }, "Your mastery"), masteryControl(n, null, true),
      h("div", { class: "faint", style: { fontSize: "12px", marginTop: "10px" } }, `Readiness ${pct(n.readiness)} combines mastery with card maturity.`)));
  }
  if (n.prereq_rows.length) {
    side.append(h("div", { class: "panel" }, h("h3", { style: { marginBottom: "8px" } }, "Prerequisites"),
      h("div", { class: "list" }, n.prereq_rows.map((p) => h("div", { class: "list-item" },
        h("a", { class: "grow title", href: `#/note/${encodeURIComponent(p.id)}` }, p.title),
        h("span", { class: `chip ${p.mastery >= 2 ? "solid" : ""}` }, MASTERY[p.mastery]))))));
  }
  if (n.unlocks.length) {
    side.append(h("div", { class: "panel" }, h("h3", { style: { marginBottom: "8px" } }, "Unlocks"),
      h("div", { class: "row" }, n.unlocks.map((u) => h("a", { class: "chip", href: `#/note/${encodeURIComponent(u.id)}` }, u.title)))));
  }
  if (n.cards) {
    const seen = n.card_rows.filter((c) => c.due).length;
    side.append(h("div", { class: "panel" }, h("h3", {}, "Review cards"),
      h("p", { class: "muted", style: { margin: "6px 0 10px" } }, `${n.cards} cards, ${seen} in your review rotation.`),
      h("a", { class: "btn small", href: "#/review" }, "Open review")));
  }
  side.append(h("div", { class: "faint", style: { fontSize: "12px" } }, h("span", { class: "mono" }, n.path)));
  const head = h("div", { class: "note-head" },
    h("div", { class: "crumbs" }, h("a", { href: `#/syllabus?s=${section}` }, section.replace(/^\d\d-/, "").replace(/-/g, " "))),
    h("h1", {}, n.title),
    h("div", { class: "row" }, n.tier ? tierChip(n.tier) : null, statusChip(n.status), n.tracks.length ? trackChips(n.tracks) : null,
      n.hours ? h("span", { class: "chip" }, `${n.hours} h`) : null, n.type !== "concept" ? h("span", { class: "chip" }, n.type) : null));
  $app.replaceChildren(head, h("div", { class: "note-layout" }, h("article", {}, mdView(n.body, n.path, n.paths)), side));
  window.scrollTo(0, 0);
}

async function viewReview() {
  let queue = await api("queue?limit=200");
  let i = 0, revealed = false, graded = 0;
  const labels = { again: "Again", hard: "Hard", good: "Good", easy: "Easy" };
  const hints = { again: "see it again today", hard: "shorter interval", good: "normal interval", easy: "longer interval" };
  function draw() {
    if (i >= queue.length) {
      $app.replaceChildren(page("Review", null), h("div", { class: "panel empty" },
        h("h2", {}, graded ? `Done: ${graded} card${graded === 1 ? "" : "s"} reviewed` : "Nothing due"),
        h("p", {}, graded ? "Come back tomorrow; intervals grow as you remember." : "Cards come from written topics. Study a topic, then its cards join the queue."),
        h("a", { class: "btn", href: "#/" }, "Back to dashboard")));
      updateBadge(0);
      return;
    }
    const c = queue[i];
    const answer = h("div", { class: "answer md", hidden: !revealed, html: renderMarkdown(c.answer) });
    const grades = h("div", { class: "grades", hidden: !revealed }, ["again", "hard", "good", "easy"].map((g, k) =>
      h("button", { class: `btn ${g}`, type: "button", onclick: () => grade(g) }, h("span", {}, `${labels[g]} `, h("span", { class: "kbd" }, String(k + 1))), h("small", {}, hints[g]))));
    const reveal = h("button", { class: "btn primary", type: "button", hidden: revealed, onclick: () => { revealed = true; draw(); } }, "Show answer ", h("span", { class: "kbd on-accent" }, "space"));
    $app.replaceChildren(page("Review", `${queue.length - i} left in this session${c.new ? ", new card" : ""}.`),
      h("div", { class: "panel review-card" },
        h("div", { class: "row" }, h("a", { class: "chip", href: `#/note/${encodeURIComponent(c.note_id)}` }, c.note_title), c.new ? h("span", { class: "chip core" }, "new") : null,
          h("span", { class: "spacer" }), h("span", { class: "faint num" }, `${i + 1} / ${queue.length}`)),
        h("div", { class: "prompt md", html: renderMarkdown(c.prompt) }), reveal, answer, grades));
  }
  let busy = false;
  async function grade(g) {
    if (busy || i >= queue.length) return; // one grade per card, even on double clicks or key repeat
    busy = true;
    const c = queue[i];
    try {
      await api("grade", { card: c.id, grade: g });
      graded++;
      if (g === "again") queue.push({ ...c, new: false });
      i++; revealed = false; draw();
      updateBadge(); // the nav badge counts what is still due, so it shrinks as the session progresses
    } catch (err) { toast(err.message); } finally { busy = false; }
  }
  const onKey = (e) => {
    if (e.repeat || location.hash !== "#/review" || e.target.tagName === "INPUT") return;
    if (e.code === "Space" && !revealed && i < queue.length) { e.preventDefault(); revealed = true; draw(); }
    else if (revealed && ["1", "2", "3", "4"].includes(e.key)) grade(["again", "hard", "good", "easy"][+e.key - 1]);
  };
  document.addEventListener("keydown", onKey);
  drillCleanup = () => document.removeEventListener("keydown", onKey);
  draw();
}

// ---------- drills ----------
function parseRational(raw) {
  const s = raw.trim().replace(/,/g, "").replace(/\s+/g, "");
  if ((s.match(/\//g) || []).length > 1) return null; // same rules as drills.parse_number
  const dec = (t) => {
    const m = t.match(/^(-?)(\d*)(?:\.(\d*))?$/);
    if (!m || (!m[2] && !m[3])) return null;
    const frac = m[3] || "";
    let num = BigInt((m[2] || "0") + frac);
    const den = 10n ** BigInt(frac.length);
    if (m[1]) num = -num;
    return [num, den];
  };
  if (s.includes("/")) {
    const [a, b] = s.split("/");
    const x = dec(a), y = dec(b);
    if (!x || !y || y[0] === 0n) return null;
    return [x[0] * y[1], x[1] * y[0]];
  }
  return dec(s);
}
function checkAnswer(p, raw) {
  const r = parseRational(raw);
  if (!r) return false;
  const [n, d] = r;
  if (p.tol === 0) return n * BigInt(p.den) === BigInt(p.num) * d;
  return Math.abs(Number(n) / Number(d) - p.num / p.den) <= p.tol + 1e-12;
}

async function viewDrills(params) {
  const mode = params.get("m") || "arith";
  const tabs = h("div", { class: "tabs" }, [["arith", "Arithmetic sprint"], ["optiver", "80 in 8"], ["mm", "Market-making game"]].map(([k, label]) =>
    h("button", { class: k === mode ? "on" : "", type: "button", onclick: () => { location.hash = `#/drills?m=${k}`; } }, label)));
  const stage = h("div", { class: "panel" });
  $app.replaceChildren(page("Drills", "Speed and judgement under time pressure. Every result is logged to your progress."), tabs, stage);
  if (mode === "mm") return mmGame(stage);
  timedDrill(stage, mode);
}

function timedDrill(stage, mode) {
  const cfg = mode === "arith"
    ? { seconds: 120, limit: Infinity, retry: true, intro: "Zetamac rules: addition and subtraction up to 100, multiplication tables 2-12 by 2-100, and the matching divisions. Correct answers submit themselves. 120 seconds." }
    : { seconds: 480, limit: 80, retry: false, intro: "80 mixed questions in 8 minutes: multiplication, decimals, percentages, fractions. Press Enter to submit; each question gets one attempt. Answer decimals or a/b." };
  const start = h("button", { class: "btn primary", type: "button", onclick: run }, "Start");
  stage.replaceChildren(h("div", { class: "drill-stage" }, h("p", { class: "muted", style: { maxWidth: "560px", margin: "0 auto 18px" } }, cfg.intro), start));
  async function run() {
    let problems;
    try { problems = await api(`problems?mode=${mode}&n=${cfg.limit === Infinity ? 400 : cfg.limit}`); } catch (err) { return toast(err.message); }
    let idx = 0, correct = 0, attempts = 0, done = false;
    const t0 = performance.now();
    const problemEl = h("div", { class: "drill-problem" });
    const input = h("input", { class: "drill-input", inputmode: "decimal", autocomplete: "off", "aria-label": "Answer" });
    const timeEl = h("b", {}), scoreEl = h("b", {}), progEl = h("b", {});
    const stats = h("div", { class: "drill-stats" }, h("span", {}, "Time ", timeEl), h("span", {}, "Score ", scoreEl), cfg.limit !== Infinity ? h("span", {}, "Question ", progEl) : null);
    const feedback = h("div", { class: "faint", style: { minHeight: "22px", marginTop: "12px" } });
    stage.replaceChildren(h("div", { class: "drill-stage" }, stats, problemEl, input, feedback));
    const paint = () => { problemEl.textContent = problems[idx].text; scoreEl.textContent = correct; progEl.textContent = `${Math.min(idx + 1, cfg.limit)}/${cfg.limit}`; };
    const advance = () => { idx++; input.value = ""; if (idx >= problems.length || idx >= cfg.limit) return finish(); paint(); };
    input.addEventListener("input", () => {
      input.classList.remove("wrong");
      if (cfg.retry && checkAnswer(problems[idx], input.value)) { attempts++; correct++; advance(); }
    });
    input.addEventListener("keydown", (e) => {
      if (e.key !== "Enter" || !input.value.trim()) return;
      if (cfg.retry) { input.classList.add("wrong"); return; }
      attempts++;
      if (checkAnswer(problems[idx], input.value)) { correct++; feedback.textContent = ""; }
      else feedback.textContent = `${problems[idx].text} = ${problems[idx].answer}`;
      advance();
    });
    const timer = setInterval(() => {
      const left = cfg.seconds - (performance.now() - t0) / 1000;
      timeEl.textContent = `${Math.floor(Math.max(0, left) / 60)}:${String(Math.floor(Math.max(0, left) % 60)).padStart(2, "0")}`;
      if (left <= 0) finish();
    }, 200);
    drillCleanup = () => clearInterval(timer);
    paint(); input.focus();
    async function finish() {
      if (done) return;
      done = true; clearInterval(timer);
      const seconds = Math.min(cfg.seconds, (performance.now() - t0) / 1000);
      let note = "";
      try { await api("drill", { mode, attempts, correct, seconds }); } catch (err) { note = ` (not saved: ${err.message})`; }
      stage.replaceChildren(h("div", { class: "drill-stage" },
        h("div", { class: "faint" }, "Score"), h("div", { class: "drill-problem" }, String(correct)),
        h("p", { class: "muted" }, `${correct} correct of ${attempts} answered in ${Math.round(seconds)} s${note}.`),
        h("button", { class: "btn primary", type: "button", onclick: run }, "Go again")));
    }
  }
}

async function mmGame(stage) {
  let game, st;
  try { ({ game, state: st } = await api("mm/new", {})); } catch (err) { return stage.replaceChildren(h("div", { class: "error" }, err.message)); }
  const log = [];
  const bid = h("input", { class: "field", type: "number", step: "1", "aria-label": "Bid" });
  const ask = h("input", { class: "field", type: "number", step: "1", "aria-label": "Ask" });
  const msg = h("div", { class: "faint", style: { minHeight: "22px", marginTop: "10px" } });
  let pending = false;
  const submit = async (e) => {
    e && e.preventDefault();
    if (pending) return; // a double Enter must not quote two rounds
    const b = parseInt(bid.value, 10), a = parseInt(ask.value, 10);
    if (Number.isNaN(b) || Number.isNaN(a)) { msg.textContent = "Enter an integer bid and ask."; return; }
    pending = true;
    try {
      const res = await api("mm/quote", { game, bid: b, ask: a });
      st = res.state; log.push(res.event); draw();
    } catch (err) { msg.textContent = err.message; } finally { pending = false; }
  };
  function draw() {
    const dice = h("div", { class: "dice" }, Array.from({ length: st.n_dice }, (_, k) =>
      k < st.revealed.length ? h("div", { class: "die" }, st.revealed[k]) : h("div", { class: "die hidden" }, "?")));
    const rows = log.map((e) => h("tr", {},
      h("td", { class: "num" }, e.round), h("td", { class: "num" }, `${e.bid} / ${e.ask}`),
      h("td", {}, e.trade ? `${e.trade.side === "sell" ? "Sold" : "Bought"} ${e.trade.qty} @ ${e.trade.price}` : "No trade"),
      h("td", { class: "hide-sm faint" }, e.trade ? e.trade.counterparty : ""),
      h("td", { class: "r num" }, e.fair_value), h("td", { class: "r num" }, e.revealed_die), h("td", { class: "r num" }, e.position)));
    const table = log.length ? h("table", { class: "t", style: { marginTop: "22px" } },
      h("thead", {}, h("tr", {}, h("th", {}, "Round"), h("th", {}, "Your market"), h("th", {}, "Result"), h("th", { class: "hide-sm" }, "Counterparty"),
        h("th", { class: "r" }, "Fair value"), h("th", { class: "r" }, "Die"), h("th", { class: "r" }, "Position"))), h("tbody", {}, rows)) : null;
    const intro = h("p", { class: "muted", style: { maxWidth: "620px", margin: "0 auto 14px" } },
      `Make a two-sided market on the sum of ${st.n_dice} hidden d${st.sides}. Width 1 to ${st.max_width}. Each trade is ${st.lot} lots. About half your counterparties know the total; the rest trade at random. One die is revealed after each round, then everything settles at the true sum.`);
    if (st.finished) {
      const s = st.summary;
      stage.replaceChildren(h("div", { class: "drill-stage" }, dice,
        h("div", { class: "faint" }, `Total ${s.total}. Final P&L`),
        h("div", { class: `drill-problem ${s.pnl >= 0 ? "pos" : "neg"}` }, `${s.pnl >= 0 ? "+" : ""}${s.pnl}`),
        h("p", { class: "muted" }, `Edge at fill ${s.edge_at_fill >= 0 ? "+" : ""}${s.edge_at_fill} versus fair value; adverse selection and inventory ${s.adverse_and_inventory >= 0 ? "+" : ""}${s.adverse_and_inventory}. ${s.trades} trade${s.trades === 1 ? "" : "s"}, ${s.informed_trades} with informed counterparties.`),
        h("button", { class: "btn primary", type: "button", onclick: () => mmGame(stage) }, "New game")), table || "");
      return;
    }
    const form = h("form", { class: "quote-row", onsubmit: submit },
      h("label", {}, "Bid", bid), h("label", {}, "Ask", ask), h("button", { class: "btn primary", type: "submit" }, "Quote"));
    stage.replaceChildren(h("div", { class: "drill-stage" }, intro, dice,
      h("div", { class: "drill-stats", style: { marginBottom: "16px" } }, h("span", {}, "Round ", h("b", {}, `${st.round}/${st.n_dice}`)), h("span", {}, "Position ", h("b", {}, st.position))),
      form, msg), table || "");
    bid.value = ""; ask.value = ""; msg.textContent = "";
    bid.focus();
  }
  draw();
}

async function viewPlan(params) {
  const tiers = params.get("tiers") || "all";
  const [s, plan] = await Promise.all([api("summary"), api(`plan?tiers=${tiers}`)]);
  const profile = s.profile;
  const hours = h("input", { class: "field", type: "number", min: "1", max: "100", step: "1", value: profile.hours_per_week, style: { width: "80px" } });
  const trackBtns = Object.entries(TRACKS).map(([k, label]) => h("button", {
    class: `chip toggle ${profile.tracks.includes(k) ? "on" : ""}`, type: "button",
    onclick: async () => {
      const next = profile.tracks.includes(k) ? profile.tracks.filter((t) => t !== k) : [...profile.tracks, k];
      if (!next.length) return toast("Keep at least one track");
      try { await api("profile", { tracks: next }); route(); } catch (err) { toast(err.message); }
    },
  }, label));
  const save = h("button", { class: "btn small", type: "button", onclick: async () => {
    try { await api("profile", { hours_per_week: Number(hours.value) }); route(); } catch (err) { toast(err.message); }
  } }, "Save");
  const tierSel = h("select", { class: "field", onchange: (e) => { location.hash = `#/plan?tiers=${e.target.value}`; } },
    [["all", "All tiers"], ["no-senior", "Core and advanced"], ["core", "Core only"]].map(([v, l]) => h("option", { value: v, selected: v === tiers ? true : null }, l)));
  const weeks = plan.weeks.length ? plan.weeks.map((w) => h("div", { class: "week" },
    h("div", { class: "when" }, h("b", {}, `Week ${w.week}`), h("span", {}, `${w.starts}, ${w.hours} h`)),
    h("div", { class: "topics" }, w.topics.map((t) => h("a", { href: `#/note/${encodeURIComponent(t.id)}`, title: `${t.tier}, ${t.hours} h` }, t.title)))))
    : [h("div", { class: "empty" }, h("h2", {}, "Nothing left to plan"), "Every topic in your tracks is at solid mastery.")];
  $app.replaceChildren(
    page("Study plan", `${plan.weeks.length} weeks, about ${Math.round(plan.total_hours)} hours at ${plan.hours_per_week} h per week, in prerequisite order. Mastered topics drop out automatically.`),
    h("div", { class: "panel", style: { marginBottom: "16px" } }, h("div", { class: "row" },
      h("span", { class: "muted" }, "Target tracks"), trackBtns, h("span", { class: "spacer" }),
      h("span", { class: "muted" }, "Hours per week"), hours, save, tierSel)),
    h("div", { class: "panel" }, weeks));
}

async function viewFirms() {
  const s = await api("summary");
  $app.replaceChildren(page("Firms", "Readiness per firm is your weighted readiness over the topics each firm emphasises."),
    h("div", { class: "grid g3" }, s.firms.map((f) => h("a", { class: "panel firm-card", href: `#/firm/${f.id}` },
      h("div", { class: "row" }, h("h3", {}, f.title), h("span", { class: "spacer" }), h("span", { class: "chip" }, (f.type || "").replace("-", " "))),
      h("div", { class: "pct" }, pct(f.readiness)), bar(f.readiness)))));
}

async function viewFirm(id) {
  const f = await api(`firm/${encodeURIComponent(id)}`);
  const focus = h("div", { class: "panel" }, h("div", { class: "panel-head" }, h("h2", {}, "Focus topics"), h("span", { class: "sub" }, "weakest first")),
    h("div", { class: "list" }, f.focus.map((t) => h("div", { class: "list-item" },
      h("div", { class: "grow" }, h("a", { class: "title", href: `#/note/${encodeURIComponent(t.id)}` }, t.title), h("div", { class: "sub" }, `${pct(t.readiness)} ready, ${t.hours} h`)),
      tierChip(t.tier), masteryControl(t)))));
  $app.replaceChildren(
    h("div", { class: "crumbs" }, h("a", { href: "#/firms" }, "Firms")),
    page(f.title, `${(f.type || "").replace("-", " ")}, guide ${f.status}. Readiness ${pct(f.readiness)}.`),
    h("div", { class: "note-layout wide-side" }, h("article", {}, mdView(f.body, f.path, f.paths)), h("div", { class: "note-side" }, focus)));
}

// ---------- router ----------
let badgeSeq = 0;
async function updateBadge(n) {
  const b = document.getElementById("due-badge");
  const seq = ++badgeSeq; // only the latest call may paint, so a slow earlier fetch cannot overwrite a newer count
  if (n === undefined) { try { n = (await api("summary")).queue; } catch { return; } }
  if (seq !== badgeSeq) return;
  b.hidden = !n; b.textContent = n;
}

async function route() {
  if (drillCleanup) { drillCleanup(); drillCleanup = null; }
  const hash = location.hash.slice(1) || "/";
  const [path, query] = hash.split("?");
  const params = new URLSearchParams(query || "");
  const parts = path.split("/").filter(Boolean);
  const name = parts[0] || "dashboard";
  document.querySelectorAll("#nav a").forEach((a) => a.classList.toggle("active", a.dataset.route === (name === "note" ? "syllabus" : name === "firm" ? "firms" : name)));
  try {
    if (name === "dashboard") await viewDashboard();
    else if (name === "syllabus") await viewSyllabus(params);
    else if (name === "note") await viewNote(decodeURIComponent(parts.slice(1).join("/")));
    else if (name === "review") await viewReview();
    else if (name === "drills") await viewDrills(params);
    else if (name === "plan") await viewPlan(params);
    else if (name === "firms") await viewFirms();
    else if (name === "firm") await viewFirm(decodeURIComponent(parts[1]));
    else $app.replaceChildren(h("div", { class: "empty" }, h("h2", {}, "Not found"), h("a", { href: "#/" }, "Dashboard")));
    document.title = `${document.querySelector("#app h1")?.textContent || "Quant Prep"} - Quant Prep`;
  } catch (err) { showError(err); }
  updateBadge();
}

window.addEventListener("hashchange", route);
window.addEventListener("DOMContentLoaded", () => {
  document.getElementById("side-foot").textContent = "Local only. Progress stays on this machine.";
  route();
});
