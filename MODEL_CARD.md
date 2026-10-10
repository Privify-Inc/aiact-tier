---
license: apache-2.0
base_model: Qwen/Qwen3-4B
library_name: transformers
pipeline_tag: text-generation
language:
- en
tags:
- eu-ai-act
- ai-governance
- compliance
- classification
- lora
---

# Privify AI Act Risk-Tier Classifier (v0.1)

**Author:** Bhaskar Tallamraju, Privify Inc. · **Fine-tuned from:**
[Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B) (Alibaba Cloud / Qwen Team, Apache 2.0) ·
**License:** Apache 2.0. The base model's capabilities come from the Qwen team's work; please cite the
[Qwen3 Technical Report](https://arxiv.org/abs/2505.09388) alongside this model.

> **Status:** v0.1, an early release. Results below come from a small test set (109 items) whose labels were cross-checked by AI models and adjudicated by the author, **not reviewed by a lawyer**. Treat the numbers as indicative, not definitive.

A 4B-parameter model, fine-tuned from Qwen3-4B with LoRA (Low-Rank Adaptation, a lightweight
fine-tuning method), that classifies a described AI system under the EU AI Act (Regulation (EU)
2024/1689). It returns a risk tier and the provisions that apply, as JSON.

```json
{"tier": "high_risk", "provisions": ["Annex III(4)(a)", "Art. 50(1)"]}
```

**Provided as is, with no warranty and no liability (Apache 2.0, sections 7 and 8). Not legal advice, not a compliance certification, not a substitute for a lawyer. Use is entirely at your own risk.**

**This is a decision aid, not legal advice.** It can be wrong. A qualified person must review any
compliance decision.

## Intended use

- First-pass triage of AI systems in an inventory, so reviewers look at the riskiest ones first.
- Research and benchmarking of AI Act classification.
- Education and tooling prototypes.

## Out of scope

- Automated compliance decisions without human review.
- Legal advice, certification, or any claim that a system complies with the Act.
- Classifying people (it classifies system descriptions only).
- General-purpose AI model obligations (Art. 51 onward), deadlines, fines, or conformity procedures.

## How to use

```python
from aiact_tier.predict import Classifier
clf = Classifier("Qwen/Qwen3-4B", adapter="privify/aiact-tier-4b-v0.1")  # LoRA adapter on the base model
print(clf.classify("A chatbot that screens job applicants and ranks them for recruiters."))
```

Quantized files (`Q8_0`, `Q4_K_M`) run in llama.cpp, Ollama and LM Studio. Use the prompt in
`aiact_tier/schema.py` (`SYSTEM_SHORT`). Greedy decoding is recommended.

## Labels

Four tiers (most to least severe): `prohibited` (Art. 5(1)(a) to (h)), `high_risk` (Annex III
categories and Art. 6(1)), `limited_transparency` (Art. 50), `minimal`. The tier is the most severe
that applies; provisions list every applicable one. The full list is in `aiact_tier/taxonomy.py`.

## Training data

- **Seed descriptions:** 137 hand-written fictional system descriptions (3 per category, 23 for
  `minimal`), plus 4 multi-provision examples. Drafted with AI assistance (Anthropic's Claude) from
  the public text of the Act, then not reviewed by a lawyer.
- **Framing variants:** each seed is repeated with label-neutral context (vendor, deployment, stage).
  This adds no new legal facts and gives little real diversity.
- **LLM paraphrases:** none in v0.1.
- **Not used:** customer data, personal data, scraped web text, or any confidential Privify data.
- **Split:** 2,704 train and 288 validation, split by seed so paraphrases never straddle the split.
- **Leakage control:** near-duplicates of gold items (token Jaccard 0.6 or more) are removed and a
  unit test blocks overlap.

## Training procedure

4-bit QLoRA (NF4 base weights, fp16 compute) on all linear layers, rank 16, alpha 32, dropout 0.05,
learning rate 2e-4 (cosine), 2 epochs, effective batch 16, max length 512, loss on the answer tokens only.
Hardware: one NVIDIA Tesla T4 (16 GB) on Kaggle, roughly 3 hours. Library versions: torch 2.11, transformers 5.16,
peft 0.20 (`eval/train_meta.json` has the exact settings and a hash of the training file).
Exact command, seed, data hash and library versions are saved in `train_meta.json`.

## Evaluation

Gold set: 109 hand-written system descriptions (93 standard cases plus 16 harder, vaguer ones). Labels were
drafted by Claude, then labeled blind by ChatGPT and Microsoft Copilot (tier agreement between the two:
Cohen's kappa 0.96), and disagreements were adjudicated by the author (`eval/REVIEW_PROVENANCE.md`).
**No lawyer reviewed them.** The base model and the baselines receive the long prompt that lists every allowed
provision; the fine-tuned model uses the short prompt.

| Model | Tier accuracy (95% CI) | Macro-F1 | Exact match | Hallucinated provisions | Critical errors |
|---|---|---|---|---|---|
| Majority class | 50.5% (42.2 to 59.6) | 16.8% | 0.0% | 0.0% | 0.0% |
| Keyword rules | 59.6% (49.5 to 68.8) | 59.6% | 44.0% | 0.0% | 24.8% |
| Qwen3-4B, zero-shot | 69.7% (61.5 to 78.9) | 54.4% | 41.3% | 4.9% | 2.8% |
| **This model (QLoRA 4-bit adapter)** | **80.7% (73.4 to 88.1)** | **74.8%** | **68.8%** | **2.1%** | **0.9%** |

Quantized GGUF versions and other base models were not evaluated in v0.1.

Critical error = a prohibited or high-risk system classified as limited or minimal.

**What the numbers show, and do not show**
- Fine-tuning beat the untuned base model by about 11 points of tier accuracy (paired bootstrap 95% CI: +3.7 to +18.3).
- **Banned practices are the weak spot.** Only 8 of 17 prohibited systems were labeled prohibited. The other 9 were
  labeled high-risk, mostly emotion recognition at work or school, social scoring and biometric inference of
  political views. The model errs toward the more cautious high-risk tier, but it does not reliably flag bans.
- **Harder cases are much worse.** On the 93 standard cases, tier accuracy is 87% (81 of 93). On the 16 harder, vaguer
  cases it is 44% (7 of 16). Expect lower accuracy on real vendor descriptions.
- The one critical error was a hospital emergency-triage system labeled minimal.
- The test set is small (the prohibited class has 17 items), the labels were not checked by a lawyer, and the training
  and test items were both drafted with AI help, so shared blind spots are possible.

## Limitations and known gaps

- **Law changes.** The Act was amended in 2026 by the Digital Omnibus on AI (deferred high-risk
  application dates, new prohibited practices). v0.1 does not cover the additions. Confirm current text
  on EUR-Lex.
- **No Art. 6(3) reasoning.** Some Annex III systems escape high-risk status when they pose no
  significant risk. The model does not weigh this and will tend to over-classify.
- **Coarse Annex I coverage.** Product-safety law is one category.
- **Ambiguous categories.** Annex III(1)(b), recruitment-stage emotion inference, and law-enforcement
  versus border-control biometrics are genuinely contestable. See `docs/LABELING_GUIDE.md`.
- **Short synthetic inputs.** Real vendor descriptions are longer and vaguer. Expect lower accuracy.
- **Open-ended minimal class.** Unusual harmless systems may be flagged.
- **Language.** English only.
- **Facts you must supply.** Classification depends on intended purpose and context. A vague
  description yields an unreliable answer.

## Risks and mitigations

See `docs/RISK_ASSESSMENT.md`. Main risks: over-reliance on the output, misuse as compliance
evidence, and under-classifying a risky system. Mitigations: the closed provision list, a reported
critical-error rate, a conservative bias toward the more severe tier, and the disclaimers above.

## Environmental impact

About 3 hours on one Tesla T4 (70 W maximum), so roughly 0.2 kWh. Region not recorded.

## Citation and contact

Author: Bhaskar Tallamraju, Privify Inc. Issues and label disputes: GitHub issues on the repository. If you use this model, please cite it via `CITATION.cff` and cite the Qwen3 Technical Report.

Built on Qwen3-4B (Apache 2.0, Alibaba Cloud / Qwen Team). See `NOTICE`.
