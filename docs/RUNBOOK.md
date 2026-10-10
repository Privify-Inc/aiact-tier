# One-week runbook (target launch: Tuesday, October 13, 2026)

Dates are in IST. Items marked **TODAY** are the slowest dependencies.

## TODAY (Wed Oct 7)

- [ ] Send `docs/COUNSEL_MEMO.md` to counsel. Ask for sign-off by Mon Oct 12.
- [ ] Get a GPU. Our existing Azure VMs are CPU-only, so request GPU quota now (new quotas can take
      days) or use a rented GPU for a few days. Needs 24 GB or more of GPU memory.
      Options: Azure `Standard_NC24ads_A100_v4` (A100 80 GB) or `Standard_NV36ads_A10_v5` (A10 24 GB);
      or a rented A100 or L4 from any GPU cloud. Also check whether NVIDIA Inception offers cloud credits.
      A T4 is too small and lacks bf16.
- [ ] Find two legal reviewers for the gold set (see `docs/LABELING_GUIDE.md`) and send them the sheet.
- [ ] Pick an API model for paraphrase expansion only after counsel answers Q4(b). Or skip it for v0.1.

## Thu Oct 8: GPU box and data

```bash
git clone <repo> && cd privify-aiact-tier
pip install -r requirements.txt pytest
make test && make smoke          # both must pass before spending GPU hours
make data
# optional, after counsel OK on provider terms:
# export ANTHROPIC_API_KEY=...   (or OPENAI_API_KEY / OPENAI_BASE_URL)
# python -m aiact_tier.llm_expand --provider anthropic --model <model> --n 12
# spot-check 5% of data/expanded.jsonl by hand, then:
# python -m aiact_tier.make_data --out data --extra data/expanded.jsonl
```

## Fri Oct 9: first training run

```bash
make train                       # minutes to under an hour on an A100 class GPU (estimate)
make eval-zeroshot && make eval-ours     # on the DRAFT gold set: for debugging only
```

Look at `eval/results/ours.json` predictions, not just the table. Fix label or seed problems, not the test set.

## Sat Oct 10: iterate and freeze

- Reviewers return the sheet. `make finalize-gold` produces `data/gold.jsonl`.
- Retrain if needed (change seeds or hyperparameters, never train on gold).
- Add a second baseline served with llama.cpp or Ollama: `evaluate.py --backend openai --base-url http://localhost:8080/v1 --model <name>`.
- Freeze the model. Run the final numbers once on the verified gold set.

## Sun Oct 11: package

```bash
make merge && make gguf
# serve each quantized file with llama-server and re-run evaluate.py --backend openai
```

- Fill every `TBD` in `MODEL_CARD.md` from `eval/results/*.md`.
- Add `SECURITY.md` with a disclosure email. Tag the repo `v0.1.0`.

## Mon Oct 12: gates (all must be yes, otherwise slip the launch)

- [ ] Counsel signed off on license, NOTICE, disclaimers, launch posts.
- [ ] Gold set verified, kappa published, no draft numbers anywhere.
- [ ] Security scan of the repo and weights folder for secrets and customer data (e.g. gitleaks).
- [ ] Model card has no `TBD`.
- [ ] Quantized scores reported next to full-precision scores.
- [ ] Brief 2 or 3 trusted practitioners for day-one comments.

## Tue Oct 13: launch

```bash
hf auth login                                   # token from an env var, never in code
hf upload <org>/aiact-tier-4b-v0.1 outputs/aiact-tier-4b-merged .
hf upload <org>/aiact-tier-4b-v0.1-gguf outputs/gguf .
```

Publish the GitHub repo, post from `docs/LAUNCH_POSTS.md`, submit to Hacker News, and stay online all day.
