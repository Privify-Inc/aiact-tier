# Prompt for ChatGPT / Copilot (blind review)

Upload `eval/gold_blind_for_ai.csv` (descriptions only, no draft labels), paste everything below the line.
Use a fresh chat per model. Save each reply as a CSV: `review_chatgpt.csv`, `review_copilot.csv`.

---

You are an independent expert reviewer in EU AI Act (Regulation (EU) 2024/1689) classification. Label each AI-system description in the attached CSV. Work blind: you have not seen anyone else's answers, and you must not guess what a "drafter" intended.

TASK
For every row, fill in the columns `tier`, `provisions`, `confidence_1_to_5`, `comments`. Keep `id` and `system_description` unchanged. Return the full completed CSV (all rows) in one code block, nothing else before it. If you hit a length limit, continue from the next id when I say "continue".

TIER (pick exactly one; the MOST SEVERE that applies)
prohibited > high_risk > limited_transparency > minimal
- prohibited: Art. 5(1)(a) to (h)
- high_risk: Annex III categories, or Art. 6(1) (Annex I product-safety systems)
- limited_transparency: Art. 50 duties only
- minimal: none of the above

PROVISIONS
List every provision that applies, separated by semicolons, using ONLY these exact strings:
Annex III(1)(a), Annex III(1)(b), Annex III(1)(c), Annex III(2), Annex III(3)(a), Annex III(3)(b), Annex III(3)(c), Annex III(3)(d), Annex III(4)(a), Annex III(4)(b), Annex III(5)(a), Annex III(5)(b), Annex III(5)(c), Annex III(5)(d), Annex III(6)(a), Annex III(6)(b), Annex III(6)(c), Annex III(6)(d), Annex III(6)(e), Annex III(7)(a), Annex III(7)(b), Annex III(7)(c), Annex III(7)(d), Annex III(8)(a), Annex III(8)(b), Art. 5(1)(a), Art. 5(1)(b), Art. 5(1)(c), Art. 5(1)(d), Art. 5(1)(e), Art. 5(1)(f), Art. 5(1)(g), Art. 5(1)(h), Art. 50(1), Art. 50(2), Art. 50(3), Art. 50(4), Art. 6(1)
Leave empty for minimal. Do not invent others.

RULES
1. Check Art. 5 first, then Annex III and Art. 6(1), then Art. 50, else minimal.
2. A system can have several provisions. Example: a hiring chatbot is high_risk with "Annex III(4)(a); Art. 50(1)". Emotion recognition outside work and school is high_risk with "Annex III(1)(c); Art. 50(3)".
3. Assume the description is complete and accurate. Do not infer facts it does not state.
4. IGNORE the Art. 6(3) "not high-risk" exception. Label as if it does not apply; mention in comments if you think it would.
5. Ignore deadlines and the 2026 Digital Omnibus additions, but flag in comments if an item touches them.
6. If the text is too vague to label, write UNCLEAR in comments and say what is missing.
7. confidence_1_to_5: 5 = certain, 1 = guess. Be honest; low scores on contested items are useful.
8. comments: one short sentence naming the key reason, REQUIRED when confidence is 3 or lower.

CONTESTED AREAS (state which way you ruled in comments)
- Annex III(1)(b): which attributes count as sensitive or protected?
- Art. 5(1)(f): does emotion inference during recruitment count as "workplace"?
- Art. 5(1)(h) vs Annex III(7)(d): live face matching at borders
- Annex III(5)(b): fraud detection carve-out from credit scoring
- Annex III(4)(b): shift scheduling from declared availability
- Annex III(6)(d): when a risk score becomes "solely profiling"

OUTPUT FORMAT
CSV with header: id,system_description,tier,provisions,confidence_1_to_5,comments
Quote fields that contain commas. Provisions separated by semicolons. No extra commentary.
