# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
import json
import random
from pathlib import Path

import pytest

from aiact_tier import gold_draft, make_data, metrics
from aiact_tier.baselines import keyword_predict
from aiact_tier.llm_expand import keep, parse_list
from aiact_tier.schema import SYSTEM_FULL, format_target, parse_output
from aiact_tier.seeds import COMBOS, SEEDS
from aiact_tier.taxonomy import (BY_ID, SEVERITY, TAXONOMY, VALID_PROVISIONS, label_for,
                                 normalize_provision)


def test_taxonomy_ids_unique_and_tiers_valid():
    ids = [c["id"] for c in TAXONOMY]
    assert len(ids) == len(set(ids))
    assert all(c["tier"] in SEVERITY for c in TAXONOMY)


def test_every_seed_category_exists_and_has_three_or_more():
    for cid, texts in SEEDS.items():
        assert cid in BY_ID, cid
        assert len(texts) >= 3
    # every non-meta category has seeds
    assert set(BY_ID) == set(SEEDS)


def test_combos_use_valid_provisions():
    for _, tier, provs in COMBOS:
        assert tier in SEVERITY
        assert all(p in VALID_PROVISIONS for p in provs)


def test_provision_normalization():
    assert normalize_provision("annex iii(4)(a)") == "Annex III(4)(a)"
    assert normalize_provision("Art 5(1)(c)") == "Art. 5(1)(c)"
    assert normalize_provision("Article 99") is None


def test_parse_output_variants():
    ok = parse_output('{"tier":"high_risk","provisions":["Annex III(4)(a)","Art. 50(1)"]}')
    assert ok["ok"] and ok["tier"] == "high_risk" and len(ok["provisions"]) == 2
    think = parse_output('<think>hmm</think>\n{"tier":"minimal","provisions":[]}')
    assert think["ok"] and think["tier"] == "minimal"
    halluc = parse_output('{"tier":"high_risk","provisions":["Annex III(9)(z)"]}')
    assert halluc["ok"] and halluc["invalid_provisions"] == ["Annex III(9)(z)"]
    assert not parse_output("no json here")["ok"]
    assert not parse_output('{"tier":"scary"}')["ok"]


def test_format_target_roundtrip():
    s = format_target("high_risk", ["Art. 50(1)", "Annex III(4)(a)"])
    p = parse_output(s)
    assert p["provisions"] == ["Annex III(4)(a)", "Art. 50(1)"]


def test_full_prompt_lists_every_citation():
    for p in VALID_PROVISIONS:
        assert p in SYSTEM_FULL


def test_metrics_known_values():
    gold = [
        {"tier": "prohibited", "provisions": ["Art. 5(1)(c)"], "category": "P_c"},
        {"tier": "high_risk", "provisions": ["Annex III(4)(a)"], "category": "H_4a"},
        {"tier": "minimal", "provisions": [], "category": "M"},
        {"tier": "high_risk", "provisions": ["Annex III(5)(b)"], "category": "H_5b"},
    ]
    preds = [
        parse_output('{"tier":"prohibited","provisions":["Art. 5(1)(c)"]}'),   # exact
        parse_output('{"tier":"high_risk","provisions":["Annex III(9)(z)"]}'),  # tier ok, hallucinated
        parse_output('{"tier":"minimal","provisions":[]}'),                     # exact
        parse_output('{"tier":"minimal","provisions":[]}'),                     # critical error
    ]
    m = metrics.evaluate(gold, preds)
    assert m["tier_accuracy"] == pytest.approx(0.75)
    assert m["exact_match"] == pytest.approx(0.5)
    assert m["critical_error_rate"] == pytest.approx(0.25)
    assert m["under_classification_rate"] == pytest.approx(0.25)
    # predicted provisions: 1 valid (ex1) + 1 invalid (ex2) -> 50 percent hallucinated
    assert m["hallucinated_provision_rate"] == pytest.approx(0.5)
    assert m["confusion"]["high_risk"]["minimal"] == 1


def test_gold_draft_is_consistent_and_flagged_unverified():
    rows = gold_draft.build_rows()
    assert len(rows) >= 70
    assert all(r["status"] == "unverified" for r in rows)
    assert len({r["id"] for r in rows}) == len(rows)
    for r in rows:
        assert r["tier"] in SEVERITY
        assert all(p in VALID_PROVISIONS for p in r["provisions"])
    cats = {r["category"] for r in rows}
    assert {c for c in BY_ID} <= cats, "gold draft should cover every category"


def test_no_seed_leaks_into_gold():
    gold = gold_draft.build_rows()
    seeds = [t for ts in SEEDS.values() for t in ts] + [c[0] for c in COMBOS]
    worst = max(make_data.jaccard(s, g["text"]) for s in seeds for g in gold)
    assert worst < 0.6, f"seed/gold overlap too high: {worst:.2f}"


def test_build_is_deterministic_and_grouped_split():
    a = make_data.build(8, 0.1, 13, None, None)
    b = make_data.build(8, 0.1, 13, None, None)
    assert a[0] == b[0] and a[1] == b[1]
    train, val, _ = a
    assert {r["group"] for r in train}.isdisjoint({r["group"] for r in val})
    assert all(r["tier"] in SEVERITY for r in train + val)


def test_llm_expand_helpers():
    assert parse_list('Sure! ["one two three four five six seven eight nine", "b"]')[0].startswith("one")
    assert parse_list("nothing") == []
    gold = [{"text": "a spam filter that sorts email"}]
    assert not keep("short text", gold, set())
    assert not keep("This high-risk system under the AI Act screens job applicants every single day", gold, set())
    assert keep("A tool that screens job applicants and ranks them for the hiring manager each week", gold, set())


def test_keyword_baseline_returns_parseable_output():
    for t in ["A spam filter", "A social scoring platform for citizens", "A chatbot for banking"]:
        assert parse_output(keyword_predict(t))["ok"]
