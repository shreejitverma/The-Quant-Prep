---
type: MOC
tags: [moc, finance]
---
# Trading Map of Content

## Automated Directory
```dataview
TABLE summary as "Summary", file.mday as "Last Modified"
FROM "16-Trading-and-Investing/Finance/Trading"
WHERE file.name != this.file.name
SORT file.name ASC
```

---
[[Dashboard|Back to Dashboard]]
