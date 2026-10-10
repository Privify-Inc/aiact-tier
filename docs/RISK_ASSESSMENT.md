# Release risk assessment (v0.1)

We sell AI governance, so we hold our own release to that standard. Ratings are qualitative
judgments by the author; owners and dates are to be filled in.

| # | Risk | Impact | Likelihood | Mitigation | Owner |
|---|---|---|---|---|---|
| 1 | Under-classification: a prohibited or high-risk system called minimal | High | Medium | Critical-error rate reported separately; conservative tier bias; disclaimers; human review wording in README and model card | TBD |
| 2 | Over-reliance: used as compliance evidence | High | Medium | "Decision aid, not legal advice" in README, model card, demo, and every CLI output | TBD |
| 3 | Wrong labels in training or test data | High | Medium | Two-reviewer gold set with published kappa; seeds reviewed by an expert; leakage test | TBD |
| 4 | Stale law: Omnibus changes and new prohibited practices | Medium | High | Known gaps listed; version and date stamped; update plan at 3 months | TBD |
| 5 | Hallucinated citations | Medium | Medium | Closed provision list; hallucination rate reported; invalid output counted as wrong | TBD |
| 6 | License or provenance defect (base model, AI-generated data, trademarks) | High | Low | Counsel memo; NOTICE; provenance recorded in the model card | TBD |
| 7 | Leak of confidential or personal data | High | Low | Only fictional synthetic text used; secret scan before upload; safetensors only (no pickle files) | TBD |
| 8 | Misleading marketing claims | Medium | Medium | Counsel reviews posts; no "compliant" or "certified"; numbers only from verified gold | TBD |
| 9 | Adversarial inputs: descriptions worded to dodge a tier | Medium | Medium | Documented as a limitation; not a security control | TBD |
| 10 | Abandoned repository | Medium | Medium | Weekly issue triage for 3 months; v0.2 plan; named maintainer | TBD |
| 11 | Bias across sectors or phrasing | Low | Medium | Per-category accuracy reported; gold set to include varied sectors and styles | TBD |

## Release gate

Do not publish unless all are true: counsel signed off; gold set verified and kappa recorded;
no draft numbers anywhere; model card has no `TBD`; secret scan clean; quantized results reported;
security disclosure contact live.
