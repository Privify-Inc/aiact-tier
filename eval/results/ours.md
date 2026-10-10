### ours  (n=109, gold set: AI CROSS-CHECKED, NOT LAWYER-REVIEWED)

| Metric | Value |
|---|---|
| Tier accuracy | 80.7% (95% CI 73.4% to 88.1%) |
| Tier macro-F1 | 74.8% |
| Exact match (tier + provisions) | 68.8% |
| Provision micro-F1 | 68.4% |
| Hallucinated provisions | 2.1% |
| Invalid outputs | 0.0% |
| Critical errors (prohibited/high-risk called limited/minimal) | 0.9% |
| Under-classification (less severe than gold) | 10.1% |

| Gold \ Predicted | prohibited | high_risk | limited_transparency | minimal | invalid |
|---|---|---|---|---|---|
| prohibited | 8 | 9 | 0 | 0 | 0 |
| high_risk | 0 | 53 | 1 | 1 | 0 |
| limited_transparency | 2 | 2 | 9 | 0 | 0 |
| minimal | 0 | 3 | 3 | 18 | 0 |
