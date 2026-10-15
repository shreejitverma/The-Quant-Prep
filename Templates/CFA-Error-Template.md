<%*
const lm = await tp.system.prompt("LM code (e.g. 06-03)");
const los = await tp.system.prompt("LOS ID (e.g. los-06-03-f)");
const question = await tp.system.prompt("Question source (note name and question number)");
const picked = await tp.system.prompt("What I picked");
const correct = await tp.system.prompt("Correct answer");
const cause = await tp.system.suggester(["concept: did not understand the idea","formula: wrong or forgotten formula","calculation: arithmetic or calculator slip","reading: misread the vignette or question","timing: rushed or ran out of time","trap: fell for the designed distractor","guess: had no idea"],["concept","formula","calculation","reading","timing","trap","guess"], false, "Root cause");
const rule = await tp.system.prompt("The one-line rule I will apply next time");
const date = tp.date.now("YYYY-MM-DD");
const slug = (question || "error").replace(/[^A-Za-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 40);
await tp.file.rename(`${date}-${slug}`);
const topicMap = {"01":"Quantitative Methods","02":"Economics","03":"Financial Statement Analysis","04":"Corporate Issuers","05":"Equity Valuation","06":"Fixed Income","07":"Derivatives","08":"Alternative Investments","09":"Portfolio Management","10":"Ethical and Professional Standards"};
const topic = topicMap[lm.slice(0,2)] ?? "";
-%>
---
type: cfa-error
date: <% date %>
topic: "<% topic %>"
lm: "<% lm %>"
los: "<% los %>"
question: "<% question %>"
picked: "<% picked %>"
correct: "<% correct %>"
cause: <% cause %>
rule: "<% rule %>"
resolved: false
tags: [cfa/l2, cfa/error]
---
# Error: <% question %>

**Rule:** <% rule %>

## Why the correct answer is right

- 

## Why my answer was tempting

- 

Mark `resolved: true` after answering a fresh question on the same LOS correctly.
