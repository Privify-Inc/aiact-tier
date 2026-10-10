# Labeling guide for the gold test set

The benchmark is only as trustworthy as these labels. Two reviewers label independently; a lead
reviewer settles disagreements. Aim for 150 to 200 items (we start from 93 AI-assisted drafts).

## What you are labeling

For each described AI system, fill in:

- **Tier** (the most severe that applies): `prohibited`, `high_risk`, `limited_transparency`, `minimal`.
- **Provisions** (all that apply), from the closed list in `aiact_tier/taxonomy.py`, written like
  `Annex III(4)(a)`, `Art. 5(1)(f)`, `Art. 50(1)`. Leave empty for `minimal`.

Assume the description is complete and accurate as written. Do not infer facts it does not state.

## Rules of thumb

1. Check Art. 5 (prohibited) first, then Annex III and Art. 6(1) (high-risk), then Art. 50, else minimal.
2. A system can have several provisions. A hiring chatbot is `high_risk` with `Annex III(4)(a)` and
   `Art. 50(1)`. Emotion recognition outside work and school is `high_risk` with `Annex III(1)(c)` and
   `Art. 50(3)`.
3. **A `prohibited` item lists only its Art. 5 provision(s).** A banned practice is not also high-risk, and
   Art. 50 duties are moot for it. (Both AI reviewers added Annex III and Art. 50(3); we ruled against it.)
   Art. 5(1)(a) and (b) also need significant harm (or reasonable likelihood of it) to be stated in the text.
4. Ignore the Art. 6(3) "not high-risk" exception in v0.1. Label as if it does not apply, and note in
   comments when you think it would.
5. Ignore deadlines and the Digital Omnibus additions, except to flag items that touch them.
6. If the text is too vague to label, write `UNCLEAR` in comments and propose a rewrite.

## Known contested categories (please discuss before labeling)

| Topic | Question |
|---|---|
| Annex III(1)(b) | Which attributes count as "sensitive or protected"? Age? Sex? Disability? |
| Art. 5(1)(f) | Does emotion inference during recruitment count as "workplace"? |
| Art. 5(1)(h) vs Annex III(7)(d) | Live face matching at borders: law enforcement or migration control? |
| Annex III(5)(b) | Fraud detection is carved out of credit scoring. Where is the edge? |
| Annex III(4)(b) | Is shift scheduling from declared availability "task allocation based on behavior or traits"? |
| Annex III(6)(d) | When does a risk score cross from objective facts into "solely profiling"? |

Record your resolution for each in comments so we can publish it with the benchmark.

## Process

1. Open `eval/gold_review_sheet.csv`. Columns `reviewer1_*` and `reviewer2_*` are for the two
   reviewers. Do not look at each other's answers.
2. Where the reviewers disagree, the lead fills `final_tier` and `final_provisions` and explains in `comments`.
3. Reviewers may append new rows (id starting `N-`) for systems the draft misses, especially harder,
   vaguer or longer descriptions.
4. Run `python -m aiact_tier.finalize_gold`. It refuses to write unless every row is agreed or
   adjudicated, validates every provision against the closed list, and writes `data/gold.jsonl` with
   status `verified`. It prints percent agreement and Cohen's kappa (a chance-corrected agreement score).
5. Publish the kappa and the contested-category rulings with the benchmark.

## Do not

- Look at model outputs before labeling.
- Copy text from the Act into descriptions.
- Add real company names or real people.
