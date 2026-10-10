# Launch kit (drafts)

Numbers are filled from `eval/results/*.md` (109-item test set, AI cross-checked, not lawyer-reviewed).
Say so in every post. Do not claim compliance, certification, expert or lawyer review, or that it runs
on a laptop until the quantized files are tested. Name placeholder: **Privify AI Act Tier** (`privify/aiact-tier-4b-v0.1`).

## Hacker News

**Title:** Show HN: Open-source model that classifies AI systems under the EU AI Act (4B, Apache 2.0)

**First comment (post immediately):**
> We built this because teams keep asking which of their AI systems the EU AI Act actually touches,
> and the answer is usually a spreadsheet and a lawyer's afternoon.
>
> It's a LoRA adapter on Qwen3-4B that takes a plain-English system description and returns a tier
> plus the provisions, from a closed list so it can't invent an article.
>
> Numbers on our 109-item test set: 80.7% tier accuracy vs 69.7% for the untuned base model, 59.6% for a
> keyword matcher and 50.5% for always guessing the most common class. Only 0.9% of high-risk or
> prohibited systems were called limited or minimal (one item).
>
> Honest weak spots: it only flags 8 of 17 banned practices as prohibited (it calls the rest high-risk,
> mostly workplace/school emotion recognition and social scoring), and on our 16 harder, vaguer cases it
> is at 44%. The test labels were cross-checked by ChatGPT and Copilot and adjudicated by me. No lawyer
> has reviewed them. Test set, labeling guide and eval harness are in the repo so you can check us.
>
> It's not legal advice, and it doesn't do the Art. 6(3) exemption or the 2026 Omnibus additions.
> It's v0.1. We want label disputes more than stars. Open an issue with a system and the provision
> you think applies.

## X thread

1. We just open-sourced a small model that tells you where an AI system lands under the EU AI Act:
   prohibited, high-risk, transparency-only, or minimal. LoRA on Qwen3-4B, Apache 2.0. [link]
2. Why small? Triage should be cheap and runnable in your own environment, so system descriptions
   don't have to leave it.
3. It cites provisions only from a closed list. Results on our 109-item test set: 80.7% tier accuracy vs
   69.7% for the untuned base model and 59.6% for keyword rules.
4. Where it's weak, we say so: it flags only 8 of 17 banned practices as prohibited, and it scores 44% on our
   16 hardest cases. Labels were cross-checked by AI models and adjudicated by me, not by a lawyer.
5. It's a decision aid, not legal advice. Known gaps are in the model card. Break it and tell us: [GitHub link]

## LinkedIn (Bhaskar, CTO voice)

> After 26 years in cybersecurity, I've learned that a control nobody can check is a liability. So when
> we decided to release an open model, we picked a problem we hear a lot: "Which of our AI systems does
> the EU AI Act actually cover?"
>
> Today Privify is open-sourcing a small classifier (a LoRA adapter on Qwen3-4B) that maps a plain-English
> description of an AI system to its risk tier and the provisions that apply. Apache 2.0.
>
> On our 109-item test set it reaches 80.7% tier accuracy, against 69.7% for the untuned base model.
> It also has clear weak spots, and I'd rather you hear them from me: it flags only about half of the
> banned practices as prohibited, and it does much worse on vague, messy descriptions. The test labels
> were cross-checked by AI models and adjudicated by me, not reviewed by a lawyer.
>
> It is a decision aid, not legal advice, and v0.1 has gaps we list openly. If you work on AI governance,
> send me your hardest edge cases.
>
> Model, data, benchmark and code: [link]. #EUAIAct #AIGovernance #OpenSource

## Blog post outline (800 to 1,000 words)

1. **The problem:** inventories of AI systems, and the first question everyone asks.
2. **What we built:** input, output, closed provision list, one example.
3. **How we tested it:** gold set, two reviewers, kappa, baselines, critical-error rate.
4. **Results:** table from the model card; one paragraph on where it fails.
5. **What it doesn't do:** the known gaps, stated plainly.
6. **How to run it:** three commands; quantized sizes.
7. **How to help:** label disputes, harder test cases, other languages.
8. **Where this fits at Privify:** one paragraph, one link to privify.io. No feature claims beyond what ships.

## Email to 3 to 5 early reviewers

> Subject: Could you try to break a small open model before we release it?
>
> Hi [Name], we're releasing a 4B model on [date] that classifies AI systems under the EU AI Act. You
> know this area better than most. Could you spend 20 minutes throwing hard or ambiguous system
> descriptions at it and tell us where it's wrong? Model and quick start: [private link]. Anything you
> send is credited if you wish. It's a decision aid, not legal advice, and we'd rather hear the bad news
> now. Thanks, Bhaskar
