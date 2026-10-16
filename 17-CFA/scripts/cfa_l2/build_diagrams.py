"""Generate Excalidraw diagrams (uncompressed JSON) for the mechanisms Level II rewards drawing from memory."""

from __future__ import annotations

import json
import random
import sys

from cfa_common import L2

random.seed(7)
OUT = L2 / "51-Diagrams"


def base(kind, x, y, w, h, **kw):
    e = {
        "id": kw.pop("id", f"{kind}{random.randint(10**8, 10**9)}"),
        "type": kind,
        "x": x,
        "y": y,
        "width": w,
        "height": h,
        "angle": 0,
        "strokeColor": kw.pop("stroke", "#1e1e1e"),
        "backgroundColor": kw.pop("bg", "transparent"),
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": kw.pop("style", "solid"),
        "roughness": 0,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": random.randint(1, 10**9),
        "version": 1,
        "versionNonce": random.randint(1, 10**9),
        "isDeleted": False,
        "boundElements": None,
        "updated": 1,
        "link": None,
        "locked": False,
    }
    e.update(kw)
    return e


def text(x, y, s, size=16, **kw):
    w = max(40, int(len(s) * size * 0.55))
    return base(
        "text",
        x,
        y,
        w,
        size * 1.3,
        text=s,
        originalText=s,
        fontSize=size,
        fontFamily=1,
        textAlign=kw.pop("align", "left"),
        verticalAlign="top",
        baseline=size,
        containerId=None,
        lineHeight=1.25,
        **kw,
    )


def rect(x, y, w, h, **kw):
    return base("rectangle", x, y, w, h, **kw)


def line(x1, y1, x2, y2, arrow=True, **kw):
    e = base(
        "arrow" if arrow else "line",
        x1,
        y1,
        x2 - x1,
        y2 - y1,
        points=[[0, 0], [x2 - x1, y2 - y1]],
        lastCommittedPoint=None,
        startBinding=None,
        endBinding=None,
        startArrowhead=None,
        endArrowhead="arrow" if arrow else None,
        **kw,
    )
    return e


def ellipse(x, y, w, h, **kw):
    return base("ellipse", x, y, w, h, **kw)


def write(name: str, title: str, elements: list, notes: str) -> None:
    OUT.mkdir(exist_ok=True)
    texts = "\n".join(f"{e['text']} ^{e['id']}" for e in elements if e["type"] == "text")
    doc = {
        "type": "excalidraw",
        "version": 2,
        "source": "cfa_l2/build_diagrams.py",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }
    md = f"""---
excalidraw-plugin: parsed
tags: [excalidraw, cfa/l2, cfa/diagram]
generated: true
---
Open in Excalidraw view (More options menu) to see the drawing.

# {title}

{notes}

# Excalidraw Data

## Text Elements
{texts}

%%
## Drawing
```json
{json.dumps(doc)}
```
%%
"""
    (OUT / f"{name}.excalidraw.md").write_text(md)


def binomial_tree():
    els = [text(40, 20, "Binomial interest rate tree: backward induction (Fixed Income LM2, LM3)", 20)]
    nodes = {(0, 0): (80, 260), (1, 0): (330, 140), (1, 1): (330, 380), (2, 0): (580, 40), (2, 1): (580, 260), (2, 2): (580, 480)}
    labels = {(0, 0): "i0", (1, 0): "i1,H", (1, 1): "i1,L", (2, 0): "i2,HH", (2, 1): "i2,HL", (2, 2): "i2,LL"}
    for k, (x, y) in nodes.items():
        els.append(rect(x, y, 130, 70, bg="#e7f5ff"))
        els.append(text(x + 10, y + 8, labels[k], 16))
        els.append(text(x + 10, y + 36, "V = (0.5 Vu + 0.5 Vd + C) / (1 + i)", 10))
    for a, b in [((0, 0), (1, 0)), ((0, 0), (1, 1)), ((1, 0), (2, 0)), ((1, 0), (2, 1)), ((1, 1), (2, 1)), ((1, 1), (2, 2))]:
        x1, y1 = nodes[a]
        x2, y2 = nodes[b]
        els.append(line(x1 + 130, y1 + 35, x2, y2 + 35))
    els.append(rect(780, 40, 200, 510, bg="#fff3bf"))
    els.append(text(790, 50, "Maturity: V = 100 + C", 13))
    els.append(text(790, 80, "Adjacent rates: iH = iL e^(2 sigma)", 13))
    els.append(text(790, 110, "Callable: V = min(V, call price)", 13))
    els.append(text(790, 140, "Putable: V = max(V, put price)", 13))
    els.append(text(790, 170, "Work right to left", 13))
    els.append(text(790, 200, "Higher sigma: call worth more,", 13))
    els.append(text(790, 220, "callable bond worth less", 13))
    els.append(line(80, 580, 760, 580, arrow=True))
    els.append(text(300, 590, "time (years)", 13))
    write(
        "Binomial-Interest-Rate-Tree",
        "Binomial interest rate tree with backward induction",
        els,
        (
            "Value each node from the right: discount the average of the two next-period values plus the "
            "coupon at the node rate; apply the call or put rule at each node before discounting further."
        ),
    )


def price_yield():
    els = [text(40, 20, "Price vs yield: straight, callable, putable (Fixed Income LM3)", 20)]
    ox, oy = 100, 520
    els.append(line(ox, oy, ox + 700, oy))
    els.append(line(ox, oy, ox, oy - 440))
    els.append(text(ox + 660, oy + 10, "yield", 14))
    els.append(text(ox - 60, oy - 450, "price", 14))
    # straight bond: convex curve approximated by a polyline
    pts = [[0, 0], [100, -60], [200, -110], [300, -150], [400, -185], [500, -215], [600, -240]]
    straight = base("line", ox + 60, oy - 40 - 200, 600, 240, points=[[p[0], -p[1] - 240] for p in pts], stroke="#1e1e1e")
    els.append(straight)
    els.append(text(ox + 620, oy - 300, "straight", 13))
    callable_pts = [[0, 0], [100, -20], [200, -50], [300, -95], [400, -150], [500, -200], [600, -235]]
    els.append(base("line", ox + 60, oy - 40 - 200, 600, 240, points=[[p[0], -p[1] - 240 + 20] for p in callable_pts], stroke="#c92a2a"))
    els.append(text(ox + 100, oy - 60, "callable: capped near the call price (negative convexity at low yields)", 12, stroke="#c92a2a"))
    putable_pts = [[0, 0], [100, -60], [200, -110], [300, -150], [400, -175], [500, -190], [600, -198]]
    els.append(base("line", ox + 60, oy - 40 - 200, 600, 240, points=[[p[0], -p[1] - 240 - 25] for p in putable_pts], stroke="#2b8a3e"))
    els.append(text(ox + 380, oy - 260, "putable: floored near the put price", 12, stroke="#2b8a3e"))
    els.append(line(ox + 60, oy - 262, ox + 660, oy - 262, arrow=False, style="dashed"))
    els.append(text(ox + 62, oy - 280, "call price", 12))
    els.append(rect(ox + 20, oy + 40, 660, 90, bg="#fff3bf"))
    els.append(text(ox + 30, oy + 48, "Vcallable = Vstraight - Vcall     Vputable = Vstraight + Vput", 14))
    els.append(text(ox + 30, oy + 78, "Effective duration: callable < straight at low yields; putable < straight at high yields", 12))
    write(
        "Callable-Putable-Price-Yield",
        "Price-yield curves for straight, callable and putable bonds",
        els,
        (
            "The callable bond's price is capped by the call price as yields fall (negative convexity); "
            "the putable bond's price is floored by the put price as yields rise."
        ),
    )


def option_payoffs():
    els = [text(40, 20, "Option payoff and profit at expiration (Derivatives LM2)", 20)]
    panels = [
        ("Long call", [[0, 0], [200, 0], [400, -200]], [[0, 40], [200, 40], [400, -160]]),
        ("Long put", [[0, -200], [200, 0], [400, 0]], [[0, -160], [200, 40], [400, 40]]),
        ("Short call", [[0, 0], [200, 0], [400, 200]], [[0, -40], [200, -40], [400, 160]]),
        ("Short put", [[0, 200], [200, 0], [400, 0]], [[0, 160], [200, -40], [400, -40]]),
    ]
    for i, (name, pay, prof) in enumerate(panels):
        px, py = 60 + (i % 2) * 560, 80 + (i // 2) * 360
        els.append(text(px, py, name, 16))
        els.append(line(px, py + 200, px + 420, py + 200, arrow=True))
        els.append(line(px, py + 320, px, py + 60, arrow=True))
        els.append(text(px + 200, py + 205, "X", 12))
        els.append(text(px + 400, py + 205, "S_T", 12))
        els.append(base("line", px + 10, py + 200, 400, 200, points=[[p[0], p[1]] for p in pay], stroke="#1971c2"))
        els.append(base("line", px + 10, py + 200, 400, 200, points=[[p[0], p[1]] for p in prof], stroke="#e8590c", style="dashed"))
    els.append(rect(60, 800, 980, 70, bg="#fff3bf"))
    els.append(
        text(
            70,
            808,
            "solid: payoff = max(0, S - X) or max(0, X - S); dashed: profit = payoff - premium (long) or premium - payoff (short)",
            13,
        )
    )
    els.append(text(70, 836, "Put-call parity: c + X e^(-rT) = p + S0   (or with PV(X) discrete)", 13))
    write(
        "Option-Payoff-Diagrams",
        "Option payoff and profit diagrams",
        els,
        "Four panels: long call, long put, short call, short put; solid is payoff, dashed is profit after premium.",
    )


def swap_timeline():
    els = [text(40, 20, "Plain vanilla interest rate swap: cash flow timeline (Derivatives LM1)", 20)]
    els.append(line(80, 300, 980, 300, arrow=True))
    for k in range(5):
        x = 120 + k * 200
        els.append(line(x, 290, x, 310, arrow=False))
        els.append(text(x - 10, 320, f"t={k}", 13))
        if k > 0:
            els.append(line(x, 300, x, 180, arrow=True, stroke="#2b8a3e"))
            els.append(text(x - 60, 150, "fixed: r_fix x NP x (days/360)", 11, stroke="#2b8a3e"))
            els.append(line(x, 300, x, 420, arrow=True, stroke="#c92a2a"))
            els.append(text(x - 60, 430, "floating: MRR(t-1) x NP", 11, stroke="#c92a2a"))
    els.append(rect(80, 500, 900, 120, bg="#fff3bf"))
    els.append(text(90, 508, "Swap fixed rate: r_fix = (1 - DF_n) / sum(DF_i)  from the spot curve's discount factors", 14))
    els.append(
        text(90, 540, "Value to fixed receiver after inception: NP x (r_fix,new - r_fix,old) x sum of remaining DFs (per period basis)", 13)
    )
    els.append(
        text(
            90,
            570,
            "Floating leg resets to par at every reset date; the floating rate is set at the start of the period and paid at the end",
            13,
        )
    )
    write(
        "Swap-Cash-Flow-Timeline",
        "Interest rate swap cash flow timeline",
        els,
        (
            "Fixed payments up, floating payments down; the floating rate for a period is the market reference "
            "rate observed at the start of that period."
        ),
    )


def consolidation_flows():
    els = [text(40, 20, "Intercorporate investments: which method, and what flows where (FSA LM1)", 20)]
    boxes = [
        ("< 20%: financial asset", "FVTPL, FVOCI, amortized cost", "dividends in income; fair value changes to P/L or OCI", "#e7f5ff"),
        ("20-50%: significant influence", "equity method", "one-line: share of NI in income, dividends reduce carrying value", "#fff3bf"),
        (
            "> 50%: control",
            "consolidation (acquisition method)",
            "100% of sub's assets, liabilities, revenue, expenses; NCI shown",
            "#ffe8cc",
        ),
        ("Shared control", "joint venture: equity method (IFRS 11)", "proportionate consolidation not permitted under IFRS", "#e6fcf5"),
    ]
    for i, (a, b, c, bg) in enumerate(boxes):
        y = 80 + i * 130
        els.append(rect(60, y, 280, 100, bg=bg))
        els.append(text(70, y + 8, a, 14))
        els.append(rect(380, y, 260, 100, bg=bg))
        els.append(text(390, y + 8, b, 14))
        els.append(rect(680, y, 420, 100, bg=bg))
        els.append(text(690, y + 8, c, 11))
        els.append(line(340, y + 50, 380, y + 50))
        els.append(line(640, y + 50, 680, y + 50))
    els.append(rect(60, 620, 1040, 110, bg="#f8f9fa"))
    els.append(
        text(
            70,
            628,
            (
                "Goodwill: full = FV of sub - FV of net identifiable assets (US GAAP); partial = purchase price "
                "- % share of FV net assets (IFRS option)"
            ),
            12,
        )
    )
    els.append(
        text(
            70,
            656,
            (
                "Equity method vs consolidation: same net income and equity; consolidation shows higher revenue, "
                "assets, liabilities, so lower margins and leverage ratios differ"
            ),
            12,
        )
    )
    els.append(
        text(
            70,
            684,
            (
                "Impairment: equity method tests the whole investment; consolidated goodwill tested at the "
                "reporting unit (US GAAP) or CGU (IFRS)"
            ),
            12,
        )
    )
    write(
        "Intercorporate-Investment-Methods",
        "Intercorporate investment accounting methods",
        els,
        "Ownership level drives the method; the method drives which lines of the investor's statements move.",
    )


def translation_flows():
    els = [text(40, 20, "Multinational operations: temporal (remeasurement) vs current rate (translation) (FSA LM3)", 20)]
    els.append(rect(60, 80, 480, 260, bg="#ffe8cc"))
    els.append(text(70, 88, "Temporal method (functional currency = parent's)", 15))
    els.append(text(70, 120, "Monetary items at current rate; nonmonetary at historical", 12))
    els.append(text(70, 145, "Revenue and expenses at average; COGS and depreciation at historical", 12))
    els.append(text(70, 170, "Remeasurement gain or loss goes to the INCOME STATEMENT", 12, stroke="#c92a2a"))
    els.append(text(70, 195, "Exposure = net monetary assets (or liabilities)", 12))
    els.append(text(70, 220, "Local currency depreciates and net monetary liabilities: GAIN", 12))
    els.append(rect(600, 80, 480, 260, bg="#e7f5ff"))
    els.append(text(610, 88, "Current rate method (functional currency = local)", 15))
    els.append(text(610, 120, "All assets and liabilities at current rate", 12))
    els.append(text(610, 145, "Revenue and expenses at average rate; equity at historical", 12))
    els.append(text(610, 170, "Translation adjustment goes to OCI (CTA in equity)", 12, stroke="#1971c2"))
    els.append(text(610, 195, "Exposure = net assets (equity)", 12))
    els.append(text(610, 220, "Pure balance sheet ratios unchanged; mixed ratios change", 12))
    els.append(rect(60, 380, 1020, 140, bg="#fff3bf"))
    els.append(
        text(
            70,
            388,
            (
                "Hyperinflation (IFRS): restate for inflation first, then translate at the current rate; US "
                "GAAP: use the temporal method with the parent's currency as functional"
            ),
            12,
        )
    )
    els.append(
        text(
            70,
            416,
            (
                "Decision: is the subsidiary self-contained (local functional currency, current rate) or an "
                "extension of the parent (parent functional currency, temporal)?"
            ),
            12,
        )
    )
    els.append(
        text(
            70,
            444,
            (
                "Translation of a foreign subsidiary: both methods; a foreign-currency transaction on the parent's "
                "own books: always income statement"
            ),
            12,
        )
    )
    write(
        "Translation-vs-Remeasurement",
        "Translation vs remeasurement decision and effects",
        els,
        "Which method applies follows from the functional currency; where the FX gain or loss lands follows from the method.",
    )


def term_structure():
    els = [text(40, 20, "Term structure shapes and the theories that explain them (Fixed Income LM1)", 20)]
    ox, oy = 100, 420
    els.append(line(ox, oy, ox + 800, oy))
    els.append(line(ox, oy, ox, oy - 320))
    els.append(text(ox + 760, oy + 10, "maturity", 13))
    els.append(text(ox - 60, oy - 335, "yield", 13))
    curves = [
        (
            "normal (upward): expectations of rising rates or positive term premium",
            [[0, -100], [200, -150], [400, -185], [600, -205], [780, -215]],
            "#2b8a3e",
        ),
        ("flat: transition, or equal expected short rates with no premium", [[0, -160], [780, -160]], "#1971c2"),
        ("inverted: expected rate cuts, recession signal", [[0, -230], [200, -190], [400, -165], [600, -150], [780, -142]], "#c92a2a"),
        (
            "humped: mixed expectations at intermediate maturities",
            [[0, -120], [200, -200], [400, -210], [600, -180], [780, -160]],
            "#e8590c",
        ),
    ]
    for i, (label, pts, col) in enumerate(curves):
        els.append(base("line", ox + 10, oy, 780, 250, points=pts, stroke=col))
        els.append(text(ox + 10, oy + 40 + i * 24, label, 12, stroke=col))
    els.append(rect(ox - 20, oy + 150, 900, 120, bg="#fff3bf"))
    els.append(
        text(
            ox - 10,
            oy + 158,
            (
                "Pure expectations: forward = expected future spot. Local expectations: only over short horizons. "
                "Liquidity preference: forwards exceed expected spots by a premium."
            ),
            12,
        )
    )
    els.append(
        text(
            ox - 10,
            oy + 186,
            (
                "Segmented markets: each maturity's supply and demand sets its rate. Preferred habitat: investors "
                "leave their habitat only for a premium."
            ),
            12,
        )
    )
    els.append(
        text(
            ox - 10,
            oy + 214,
            (
                "Forward rate model: (1 + z_B)^B = (1 + z_A)^A (1 + f_A,B-A)^(B-A); riding the curve pays when "
                "the curve is upward sloping and stays put."
            ),
            12,
        )
    )
    write(
        "Term-Structure-Shapes",
        "Term structure shapes and theories",
        els,
        "Four shapes and the five theories; the forward rate model ties spots to forwards.",
    )


def pension_components():
    els = [text(40, 20, "Defined benefit pension cost: components and where they go (FSA LM2)", 20)]
    rows = [
        ("Current service cost", "P/L", "P/L", "#e7f5ff"),
        ("Past service cost", "P/L (immediately)", "OCI, then amortized to P/L", "#e7f5ff"),
        (
            "Net interest (IFRS) / interest cost and expected return (US GAAP)",
            "P/L: net interest = discount rate x net pension liability",
            "P/L: interest cost on PBO minus expected return on plan assets",
            "#fff3bf",
        ),
        (
            "Actuarial gains and losses (remeasurement)",
            "OCI, never recycled",
            "OCI, amortized to P/L via the corridor (10% of the greater of PBO or plan assets)",
            "#ffe8cc",
        ),
        ("Difference between actual and expected return", "part of remeasurement in OCI", "OCI, amortized", "#ffe8cc"),
    ]
    els.append(text(60, 70, "Component", 14))
    els.append(text(420, 70, "IFRS", 14))
    els.append(text(760, 70, "US GAAP", 14))
    for i, (a, b, c, bg) in enumerate(rows):
        y = 100 + i * 90
        els.append(rect(60, y, 340, 75, bg=bg))
        els.append(text(68, y + 8, a, 12))
        els.append(rect(420, y, 320, 75, bg=bg))
        els.append(text(428, y + 8, b, 11))
        els.append(rect(760, y, 360, 75, bg=bg))
        els.append(text(768, y + 8, c, 11))
    els.append(rect(60, 570, 1060, 110, bg="#f8f9fa"))
    els.append(
        text(70, 578, "Balance sheet: net pension liability (asset) = PBO - fair value of plan assets; asset ceiling under IFRS", 12)
    )
    els.append(
        text(
            70,
            606,
            (
                "Total periodic pension cost = contributions - change in funded status = service cost + interest "
                "cost - actual return on assets + past service cost + actuarial losses"
            ),
            12,
        )
    )
    els.append(
        text(
            70,
            634,
            (
                "Analyst adjustments: reclassify interest cost to financing, actual return to investing; contributions "
                "above total cost are like debt repayment"
            ),
            12,
        )
    )
    write(
        "Pension-Cost-Components",
        "Defined benefit pension cost components under IFRS and US GAAP",
        els,
        "The same economic cost is split differently between profit or loss and OCI under the two frameworks.",
    )


def main() -> int:
    for fn in (
        binomial_tree,
        price_yield,
        option_payoffs,
        swap_timeline,
        consolidation_flows,
        translation_flows,
        term_structure,
        pension_components,
    ):
        fn()
    print(f"diagrams: {len(list(OUT.glob('*.excalidraw.md')))} written to {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
