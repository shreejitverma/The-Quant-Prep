<%*
const source = await tp.system.prompt("Source (item set or mock note name, e.g. IS-06-Fixed-Income-LM03-1 or Mock-01)");
const topic = await tp.system.suggester(["mixed","Quantitative Methods","Economics","Financial Statement Analysis","Corporate Issuers","Equity Valuation","Fixed Income","Derivatives","Alternative Investments","Portfolio Management","Ethical and Professional Standards"],["mixed","Quantitative Methods","Economics","Financial Statement Analysis","Corporate Issuers","Equity Valuation","Fixed Income","Derivatives","Alternative Investments","Portfolio Management","Ethical and Professional Standards"], false, "Topic");
const confidence = await tp.system.suggester(["1 guessing","2 unsure","3 fair","4 confident","5 certain"],[1,2,3,4,5], false, "Confidence BEFORE checking answers");
const score = await tp.system.prompt("Score (correct answers)");
const max = await tp.system.prompt("Max (questions)");
const minutes = await tp.system.prompt("Minutes used");
const lm = await tp.system.prompt("LM code (e.g. 06-03) or blank for mixed", "");
const losMissed = await tp.system.prompt("LOS IDs missed, comma separated (e.g. los-06-03-f, los-06-03-i)", "");
const date = tp.date.now("YYYY-MM-DD");
await tp.file.rename(`${date}-${source}`);
-%>
---
type: cfa-attempt
date: <% date %>
source: "[[<% source %>]]"
topic: "<% topic %>"
lm: "<% lm %>"
score: <% score %>
max: <% max %>
minutes_used: <% minutes %>
confidence: <% confidence %>
los_missed: [<% losMissed %>]
tags: [cfa/l2, cfa/attempt]
---
# Attempt: <% source %> on <% date %>

Score <% score %>/<% max %> in <% minutes %> minutes, confidence <% confidence %>/5 before checking.

## What went wrong

- 

## Errors to log

Use QuickAdd "CFA: log error" once per miss, then link them here.

- 
