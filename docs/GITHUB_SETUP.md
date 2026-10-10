# GitHub repo setup (15 minutes, free)

1. Create a GitHub **organization** (e.g. `privify`), then a **public** repo `aiact-tier`. Free plan is enough.
2. Push this folder as the first commit. `git init && git add . && git commit -s -m "Initial release" && git push`.
3. Settings: enable Issues, Discussions and "Private vulnerability reporting"; disable Wiki.
4. Branch protection on `main`: require PR and passing `ci`. Add a `v0.1.0` tag and a GitHub Release.
5. Pin the About line: "EU AI Act risk-tier classifier. As is, no warranty." Topics: eu-ai-act, ai-governance, lora, qwen3.
6. Do NOT commit weights, `data/gold.jsonl` raw reviewer sheets with names, API keys, or Privify internal files.
7. Weights go to a Hugging Face model repo (same org), using MODEL_CARD.md as its README. Link both ways.
8. Fill TBDs first: CITATION.cff repo URL, SECURITY.md contact (use a shared inbox, not personal email).
