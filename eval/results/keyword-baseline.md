### keyword-baseline  (n=109, gold set: AI CROSS-CHECKED, NOT LAWYER-REVIEWED)

| Metric | Value |
|---|---|
| Tier accuracy | 59.6% (95% CI 49.5% to 68.8%) |
| Tier macro-F1 | 59.6% |
| Exact match (tier + provisions) | 44.0% |
| Provision micro-F1 | 42.5% |
| Hallucinated provisions | 0.0% |
| Invalid outputs | 0.0% |
| Critical errors (prohibited/high-risk called limited/minimal) | 24.8% |
| Under-classification (less severe than gold) | 33.9% |

| Gold \ Predicted | prohibited | high_risk | limited_transparency | minimal | invalid |
|---|---|---|---|---|---|
| prohibited | 5 | 7 | 0 | 5 | 0 |
| high_risk | 0 | 33 | 0 | 22 | 0 |
| limited_transparency | 0 | 2 | 8 | 3 | 0 |
| minimal | 0 | 5 | 0 | 19 | 0 |
