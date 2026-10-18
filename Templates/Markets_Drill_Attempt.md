---
type: drill-attempt
date: 2026-10-18
drill_id: "DRL-2026-001"
drill_category: "market-making"
engine_id: "games"
time_taken_seconds: 120
target_time_seconds: 120
accuracy_score: 0.85
target_accuracy: 0.80
passed: true
tags: [drill, deliberate-practice, calibration]
---

# Deliberate Practice Drill Attempt: {{drill_id}} ({{date}})

## 1. Drill Specification and Context
- **Drill Name**: Rapid Quoting and Inventory Skew Game
- **Category**: {{drill_category}}
- **Lab Engine**: {{engine_id}}
- **Target Competency**: Rapid two-sided market quoting under toxic flow arrival and inventory constraints.
- **Prerequisite Module**: [[16-Trading-and-Investing/30-Drills/Drill-02-Two-Sided-Quoting-and-Inventory-Skew|Two-Sided Quoting Drill]]

---

## 2. Performance Metrics and Benchmark Comparison
- **Time Elapsed**: {{time_taken_seconds}} seconds (Target: {{target_time_seconds}} seconds).
- **Accuracy Score**: {{accuracy_score}} (Benchmark: {{target_accuracy}}).
- **Gate Status**: Passed ({{passed}}).
- **Questions / Quotes Attempted**: Total number of rounds completed during the timed session.
- **Average Response Latency**: Milliseconds per decision or calculation.

---

## 3. Error Classification and Diagnostic Breakdown
| Problem # | Prompt / Card Scenario | Submitted Response | Correct Solution | Error Category (Math / Concept / Speed) |
|---|---|---|---|---|
| 01 | Bid/Ask with +4 units inventory | Bid $99.80 / Ask $100.20 | Bid $99.70 / Ask $100.10 | Concept (Under-skewed reservation price) |
| 02 | Implied vol calculation | 24.5% | 22.0% | Math (Arithmetic estimation error) |
| 03 | Bayes theorem update on toxic flow | P = 0.65 | P = 0.72 | Math (Denominator base rate omission) |

---

## 4. Speed-Accuracy Trade-off Analysis
- **Execution Pace**: Did the attempt rush through early calculations or bottleneck on specific questions?
- **Pacing Discipline**: Consistency of time allocation per decision across the drill duration.
- **Fatigue Factor**: Did error frequency increase toward the final third of the drill?

---

## 5. Calibration and Probabilistic Scoring
- **Brier Score**: Quadratic probability error on confidence-weighted assessments.
- **Overconfidence Gap**: Difference between stated confidence percentage and realized accuracy.
- **Directional Bias**: Tendency to systematically overestimate upside versus downside probability.

---

## 6. Cognitive Bottlenecks and Hesitation Points
- **Hesitation Triggers**: Which specific mathematical operation or market scenario triggered cognitive stall?
- **Working Memory Load**: Was mental scratchpad overloaded due to lack of chunking heuristics?
- **Emotional Reaction**: Frustration or loss of focus following an initial incorrect answer.

---

## 7. Deliberate Practice Remediation Plan
- **Targeted Micro-Drill**: Specific isolated drill or sub-routine to practice before the next full attempt.
- **Mental Model Heuristic**: Specific rule of thumb to compress calculation complexity under time pressure.
- **Next Scheduled Attempt**: Target date and required accuracy threshold to clear the next progression gate.
