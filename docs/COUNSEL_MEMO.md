# Memo to counsel: open-source release of an AI Act classifier model

**To:** [Counsel]  **From:** Bhaskar Tallamraju, CTO, Privify Inc.  **Date:** October 7, 2026
**Sign-off needed by:** Monday, October 12, 2026 (launch target Tuesday, October 13)

## 1. What we plan to release

- A fine-tuned version of **Qwen3-4B** (a 4-billion-parameter language model) that classifies a
  described AI system under the EU AI Act into a risk tier and lists the applicable provisions.
- Weights (merged and a LoRA adapter, where LoRA is a lightweight fine-tuning method), quantized
  files, training and evaluation code, synthetic training data, a benchmark test set, and a model card.
- Publisher: Privify Inc. (California corporation). Channels: GitHub and Hugging Face.
- **Not released:** the Forge product, customer data, or any proprietary or confidential data.
- Proposed license: **Apache License 2.0**, plus a `NOTICE` file crediting Qwen3-4B.

## 2. Facts we checked (October 7, 2026)

| Item | What we saw | Source |
|---|---|---|
| Qwen3-4B license | Model page shows `apache-2.0`; 4.0B parameters | huggingface.co/Qwen/Qwen3-4B |
| Alternative base, Gemma 4 E4B | Page shows `apache-2.0` and links to Google's own license page. We did **not** read that page | huggingface.co/google/gemma-4-E4B-it |
| EU Digital Omnibus on AI | Provisional agreement May 7, 2026: Annex III high-risk obligations deferred to Dec 2, 2027, product-embedded to Aug 2, 2028 | Sidley (datamatters.sidley.com), Gibson Dunn |
| Omnibus status and new bans | Entered into force Jul 27, 2026. Adds two prohibitions (realistic intimate imagery and child abuse material generation) applying from Dec 2, 2026. Most Art. 50 transparency duties unchanged | mondaq.com K&L Gates article (page read Oct 7) |

We read law-firm summaries (pages opened and checked), not the Official Journal text.

## 3. Questions for counsel

1. **License and attribution.** Is Apache 2.0 right for our code, weights and data? Our understanding is
   we must include the license text, keep upstream notices, and mark that we changed the model. Any
   concern about the patent grant? Any reason to prefer a restricted license?
2. **Base-model terms.** Please confirm the license file in the Qwen3-4B repository itself, not just the
   Hugging Face label, and that no separate acceptable-use terms apply.
3. **Names and trademarks.** We plan to avoid "Qwen" or "Alibaba" in the model name beyond factual
   attribution. Is using "Privify" in the name fine given our pending USPTO application for PRIVIFY? Our branding plan: Privify Inc. copyright and SPDX headers in every file, NOTICE and CITATION files, a visible "developed and open-sourced by Privify Inc." line, no brand text in model outputs, and no "powered by" advertising clause in the license. Please confirm the Apache 2.0 notice requirements keep Privify's name on forks, and that the Privify name and logo stay unlicensed trademarks.
4. **Training data.**
   - (a) Our seeds are fictional system descriptions paraphrasing the Act. Any issue reusing and
     paraphrasing EU legal text?
   - (b) The seeds were drafted with AI assistance (Anthropic's Claude). We may also use a third-party
     LLM to paraphrase them. Do those providers' terms restrict using outputs to train or release a
     model? Which provider is acceptable? We will record provenance either way.
   - (c) Any concern releasing AI-assisted text under Apache 2.0, given uncertain copyright in
     AI-generated material?
5. **Disclaimers and liability.** Please draft or approve the "decision aid, not legal advice" wording.
   Any risk of claims over reliance on a wrong classification, or of unauthorized practice of law in any
   jurisdiction? Anything beyond Apache 2.0's warranty disclaimer?
6. **Our own AI Act position.** Our reading: Art. 2(12) exempts free and open-source AI systems except
   prohibited, high-risk, and Art. 50 systems. Our classifier classifies systems, not people, so it is
   not an Annex III use case, and it does not generate public-facing content. Our fine-tuning compute is
   small, so we do not believe we become a general-purpose AI model provider under the Commission's
   guidance. Please confirm each point, including whether publishing to EU users puts us in scope.
7. **Export controls and sanctions.** Please confirm there is no US export-control or sanctions issue in
   publishing these weights worldwide, including with contributors based in India.
8. **Ownership.** Confirm Privify Inc. owns all code, data and weights being released, with signed IP
   assignments from every contributor, including contractors and any affiliated entities. Should external
   contributions use a DCO (Developer Certificate of Origin, a sign-off per commit) or a CLA
   (Contributor License Agreement)? We lean DCO for simplicity.
9. **Privacy.** All training text is fictional and synthetic. Please confirm nothing further is needed
   under GDPR or similar laws.
10. **Responsible release.** Please review `docs/RISK_ASSESSMENT.md` and approve the release gate. We will
    add a `SECURITY.md` with a disclosure contact.
11. **Public claims.** Please review `docs/LAUNCH_POSTS.md`. We will not say "compliant", "certified" or
    quote accuracy without verified evidence.

## 4. What we have not verified

- Official Journal text of the Act and the Omnibus; Commission guidance on prohibited practices and
  general-purpose AI models.
- The full Qwen3-4B repository license file and any other files in that repository.
- Our labels. The test set and training seeds are AI-assisted drafts awaiting expert review.

## 5. Attachments

`LICENSE`, `NOTICE`, `MODEL_CARD.md`, `docs/RISK_ASSESSMENT.md`, `docs/LAUNCH_POSTS.md`.

## 6. Plain-English summary

- We want to publish a small AI model that sorts AI systems into EU AI Act risk levels.
- It is built on someone else's open model (Qwen3-4B), which allows this, but we must credit it.
- Lawyer checks needed: license choice, who owns what, whether AI-generated training text is safe to
  release, the "not legal advice" disclaimer, and export rules.
- We believe the release itself is not regulated as high-risk, but a lawyer must confirm.
- If the lawyer has not signed off by Monday, we move the launch date rather than skip the check.
