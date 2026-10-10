### base-zero-shot  (n=109, gold set: AI CROSS-CHECKED, NOT LAWYER-REVIEWED)

| Metric | Value |
|---|---|
| Tier accuracy | 69.7% (95% CI 61.5% to 78.9%) |
| Tier macro-F1 | 54.4% |
| Exact match (tier + provisions) | 41.3% |
| Provision micro-F1 | 41.7% |
| Hallucinated provisions | 4.9% |
| Invalid outputs | 1.8% |
| Critical errors (prohibited/high-risk called limited/minimal) | 2.8% |
| Under-classification (less severe than gold) | 20.2% |

| Gold \ Predicted | prohibited | high_risk | limited_transparency | minimal | invalid |
|---|---|---|---|---|---|
| prohibited | 4 | 10 | 1 | 0 | 2 |
| high_risk | 0 | 52 | 1 | 2 | 0 |
| limited_transparency | 2 | 0 | 3 | 8 | 0 |
| minimal | 0 | 6 | 1 | 17 | 0 |
