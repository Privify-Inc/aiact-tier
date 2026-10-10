# Privify AI Act Risk-Tier Classifier (v0.1)

**Author: Bhaskar Tallamraju, Privify Inc.** · Fine-tuned from Qwen3-4B · Apache 2.0 · free for anyone to use, modify and ship.

An open model that reads a plain-English description of an AI system and returns its EU AI Act
risk tier plus the provisions that apply.

```json
{"tier": "high_risk", "provisions": ["Annex III(4)(a)", "Art. 50(1)"]}
```

Tiers: `prohibited`, `high_risk`, `limited_transparency`, `minimal`. The tier is the most severe one
that applies. The allowed provisions are a closed list (`aiact_tier/taxonomy.py`), so the model cannot
cite an article that does not exist, and any output outside the list is counted as a hallucination.

> **AS IS, NO WARRANTY, NO SUPPORT.** Provided under Apache 2.0 (see `LICENSE`, sections 7 and 8:
> no warranty, no liability). The author and Privify Inc. accept no responsibility for any use of this
> software or its outputs. Not affiliated with or endorsed by the European Union, Alibaba Cloud or the Qwen team.
>
> **Decision aid only, not legal advice.** Outputs can be wrong. A qualified person must review any
> compliance decision.

## Status (honest version)

| Item | State |
|---|---|
| Taxonomy (39 categories, 38 provisions), prompts, parser, metrics | Built, 16 unit tests pass |
| Training data builder (2,704 train / 288 val template-framed examples) | Built, deterministic |
| Gold test set | 109 items (93 + 16 harder), **AI cross-checked** (ChatGPT, Copilot, author-adjudicated), **not lawyer-reviewed**. See `eval/REVIEW_PROVENANCE.md` |
| Training, inference, evaluation code | Smoke-tested end to end on CPU with a tiny random Qwen3 (transformers 5.19, peft 0.21) |
| Training on real Qwen3-4B | **Done** (4-bit QLoRA, 2 epochs, one Tesla T4, about 3 hours). Settings in `eval/train_meta.json` |
| LLM paraphrase expansion (`llm_expand.py`) | Written, **not run** (needs your API key) |
| GGUF export, Gradio demo launch | Written, **not run** |
| Benchmark numbers for the fine-tuned model | **80.7% tier accuracy** (95% CI 73.4 to 88.1) on the 109-item test set; see the model card for weak spots |

## Results (109-item test set, AI cross-checked, not lawyer-reviewed)

| Model | Tier accuracy | Critical errors |
|---|---|---|
| Always guess the most common tier | 50.5% | 0.0% |
| Keyword rules | 59.6% | 24.8% |
| Qwen3-4B, zero-shot | 69.7% | 2.8% |
| **This model** | **80.7%** | **0.9%** |

Weak spots: only 8 of 17 prohibited systems are labeled prohibited (the rest are called high-risk), and
accuracy on the 16 harder, vaguer cases is 44%. Details and caveats are in `MODEL_CARD.md`.

## Quick start

```bash
pip install -r requirements.txt pytest
make test           # 16 tests, no GPU
make baselines      # offline floors on the draft gold set
make smoke          # about 1 minute, proves train -> infer -> evaluate runs on this machine
```

## Reproduce on a GPU (24 GB or more)

```bash
make data                         # data/train.jsonl, data/val.jsonl
make train                        # LoRA on Qwen/Qwen3-4B -> outputs/aiact-tier-lora
make eval-zeroshot                # un-tuned base model, long prompt (fair baseline)
make eval-ours                    # fine-tuned model, short prompt
make merge && make gguf           # merged weights and Q8_0 / Q4_K_M quantized files
make demo                         # web demo
```

Full day-by-day plan: `docs/RUNBOOK.md`.

## Layout

```
aiact_tier/taxonomy.py       label space, single source of truth
aiact_tier/schema.py         prompts, output format, tolerant parser
aiact_tier/seeds.py          training seeds (AI-assisted drafts, need legal review)
aiact_tier/make_data.py      builds train/val, grouped split, near-duplicate guard vs gold
aiact_tier/llm_expand.py     optional LLM paraphrase expansion for real diversity
aiact_tier/gold_draft.py     DRAFT gold set + reviewer sheet generator
aiact_tier/finalize_gold.py  reviewer sheet -> verified gold, with Cohen's kappa
aiact_tier/train_lora.py     LoRA training, answer-only loss
aiact_tier/evaluate.py       one benchmark, any backend (hf, OpenAI-compatible, offline)
aiact_tier/metrics.py        accuracy, macro-F1, hallucination, critical-error rate, CIs
scripts/                     GGUF export, CPU smoke test
docs/                        runbook, counsel memo, reviewer guide, risk assessment, launch kit
MODEL_CARD.md                Hugging Face model card (results and limits)
```

## What the metrics mean

- **Critical error rate**: a prohibited or high-risk system called limited or minimal. This is the
  failure that hurts users most, so it is reported on its own.
- **Hallucinated provision rate**: cited a provision that is not in the closed list.
- **Exact match**: tier and the full provision set both correct.

## Known gaps in v0.1

- Prohibited practices added by the 2026 Digital Omnibus on AI are not covered.
- The Art. 6(3) "not high-risk" exception for some Annex III systems is not modeled.
- Annex I product-safety coverage is one coarse category.
- General-purpose AI model obligations and all deadlines are out of scope.
- The minimal class is open-ended and thinly seeded. Expect false alarms on unusual harmless systems.
- Training data is synthetic and short-form; real vendor descriptions are messier.

## Contributing

Sign off commits (`git commit -s`) to certify the Developer Certificate of Origin. Open an issue
with a system description and the label you think is right, citing the provision. Label disputes
are welcome and useful.

## License

Apache License 2.0 (see `LICENSE`). Weights are derived from Qwen3-4B, also Apache 2.0; see `NOTICE`.

## Credits

- **Author:** Bhaskar Tallamraju, Privify Inc.
- **Open-sourced by:** Privify Inc., as a free contribution to the community. No paid tier, no
  commercial restrictions.
- **Base model:** [Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B) by Alibaba Cloud / Qwen Team
  (Apache 2.0). This work is a LoRA fine-tune of their model, and the credit for the base model is
  theirs. Please cite the [Qwen3 Technical Report](https://arxiv.org/abs/2505.09388) too.
