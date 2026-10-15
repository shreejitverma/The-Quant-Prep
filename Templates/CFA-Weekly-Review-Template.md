<%*
const date = tp.date.now("YYYY-MM-DD");
await tp.file.rename(`${date}-weekly-review`);
-%>
---
type: cfa-weekly-review
date: <% date %>
tags: [cfa/l2, cfa/review]
---
# Weekly review: week ending <% date %>

## Attempts this week

```dataview
TABLE source, score, max, minutes_used, confidence
FROM "17-CFA/CFA-L-2/22-Attempts"
WHERE type = "cfa-attempt" AND date >= date(this.date) - dur(7 days)
SORT date DESC
```

## New errors by cause

```dataview
TABLE WITHOUT ID cause AS "Cause", length(rows) AS "Count", rows.file.link AS "Errors"
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND date >= date(this.date) - dur(7 days)
GROUP BY cause
```

## Modules whose mastery is below 70

```dataview
TABLE mastery, status, next_review
FROM "17-CFA/CFA-L-2"
WHERE type = "cfa-lm" AND mastery < 70 AND status != "not-started"
SORT mastery ASC
```

## Plan delta for next week

- Behind or ahead of [[17-CFA/CFA-L-2/00-Strategy/Study-Plan|the plan]]: 
- Modules to re-open: 
- Item-set count target next week: 
