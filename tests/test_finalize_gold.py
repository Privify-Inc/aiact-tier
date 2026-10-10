# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
import pytest

from aiact_tier.finalize_gold import cohen_kappa, finalize


def row(i, t1="", p1="", t2="", p2="", ft="", fp=""):
    return {"id": i, "system_description": f"system {i}", "reviewer1_tier": t1,
            "reviewer1_provisions": p1, "reviewer2_tier": t2, "reviewer2_provisions": p2,
            "final_tier": ft, "final_provisions": fp, "comments": ""}


def test_agreement_adjudication_and_stats():
    rows = [
        row("G-001", "prohibited", "Art. 5(1)(c)", "prohibited", "art 5(1)(c)"),
        row("G-002", "high_risk", "Annex III(4)(a)", "minimal", "", "high_risk", "Annex III(4)(a)"),
    ]
    gold, stats = finalize(rows, {})
    assert [g["tier"] for g in gold] == ["prohibited", "high_risk"]
    assert all(g["status"] == "verified" for g in gold)
    assert stats["agreed_without_adjudication"] == 1


def test_unresolved_and_invalid_rows_block_finalization():
    with pytest.raises(ValueError) as e:
        finalize([row("G-003", "high_risk", "Annex III(4)(a)", "minimal", "")], {})
    assert "disagree" in str(e.value)
    with pytest.raises(ValueError) as e:
        finalize([row("G-004", "high_risk", "Annex III(99)", "high_risk", "Annex III(99)")], {})
    assert "unknown provision" in str(e.value)
    with pytest.raises(ValueError):
        finalize([row("G-005", "minimal", "Art. 50(1)", "minimal", "Art. 50(1)")], {})


def test_kappa_perfect_and_chance():
    assert cohen_kappa(["minimal", "high_risk"], ["minimal", "high_risk"]) == pytest.approx(1.0)
    assert cohen_kappa(["minimal", "high_risk"], ["high_risk", "minimal"]) < 0
