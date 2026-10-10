# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Evaluation metrics. Pure Python so they run anywhere and are easy to audit."""
from __future__ import annotations

import random
from collections import Counter, defaultdict

from .taxonomy import SEVERITY, TIERS

COLS = TIERS + ["invalid"]


def _prf(tp: int, fp: int, fn: int) -> dict:
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    f = 2 * p * r / (p + r) if p + r else 0.0
    return {"precision": p, "recall": r, "f1": f}


def bootstrap_ci(flags: list[int], n_boot: int = 1000, seed: int = 0) -> tuple[float, float]:
    if not flags:
        return (0.0, 0.0)
    rng = random.Random(seed)
    n = len(flags)
    means = sorted(sum(flags[rng.randrange(n)] for _ in range(n)) / n for _ in range(n_boot))
    return (means[int(0.025 * n_boot)], means[int(0.975 * n_boot) - 1])


def evaluate(gold: list[dict], preds: list[dict]) -> dict:
    """gold rows need tier, provisions, category. preds are parse_output() dicts."""
    assert len(gold) == len(preds), "gold and predictions differ in length"
    n = len(gold)
    conf = {g: {c: 0 for c in COLS} for g in TIERS}
    correct_tier, exact, per_cat = [], [], defaultdict(list)
    tp = fp = fn = 0
    n_valid_p = n_invalid_p = ex_halluc = 0
    critical = under = over = invalid = 0

    for g, p in zip(gold, preds):
        gt = g["tier"]
        gp = set(g["provisions"])
        if not p["ok"]:
            invalid += 1
            conf[gt]["invalid"] += 1
            pt, pp = None, set()
        else:
            pt, pp = p["tier"], set(p["provisions"])
            conf[gt][pt] += 1
        tier_ok = int(pt == gt)
        ex_ok = int(tier_ok and pp == gp)
        correct_tier.append(tier_ok)
        exact.append(ex_ok)
        per_cat[g.get("category", "?")].append(ex_ok)
        tp += len(gp & pp)
        fp += len(pp - gp)
        fn += len(gp - pp)
        if p["ok"]:
            n_valid_p += len(p["provisions"])
            n_invalid_p += len(p["invalid_provisions"])
            ex_halluc += int(bool(p["invalid_provisions"]))
            d = SEVERITY[pt] - SEVERITY[gt]
            under += int(d > 0)
            over += int(d < 0)
            critical += int(d >= 2)

    per_tier = {}
    for t in TIERS:
        t_tp = conf[t][t]
        t_fn = sum(conf[t].values()) - t_tp
        t_fp = sum(conf[g][t] for g in TIERS if g != t)
        per_tier[t] = {**_prf(t_tp, t_fp, t_fn), "support": sum(conf[t].values())}
    present = [t for t in TIERS if per_tier[t]["support"] > 0]
    macro_f1 = sum(per_tier[t]["f1"] for t in present) / len(present) if present else 0.0
    total_p = n_valid_p + n_invalid_p
    acc_ci = bootstrap_ci(correct_tier)
    ex_ci = bootstrap_ci(exact)

    return {
        "n": n,
        "tier_accuracy": sum(correct_tier) / n if n else 0.0,
        "tier_accuracy_ci95": list(acc_ci),
        "tier_macro_f1": macro_f1,
        "exact_match": sum(exact) / n if n else 0.0,
        "exact_match_ci95": list(ex_ci),
        "provision_micro": _prf(tp, fp, fn),
        "invalid_output_rate": invalid / n if n else 0.0,
        "hallucinated_provision_rate": n_invalid_p / total_p if total_p else 0.0,
        "examples_with_hallucinated_provision": ex_halluc / n if n else 0.0,
        "critical_error_rate": critical / n if n else 0.0,
        "under_classification_rate": under / n if n else 0.0,
        "over_classification_rate": over / n if n else 0.0,
        "per_tier": per_tier,
        "confusion": conf,
        "per_category_exact": {k: sum(v) / len(v) for k, v in sorted(per_cat.items())},
    }


def to_markdown(name: str, m: dict, gold_status: str) -> str:
    pct = lambda x: f"{100 * x:.1f}%"
    lo, hi = m["tier_accuracy_ci95"]
    out = [
        f"### {name}  (n={m['n']}, gold set: {gold_status})",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Tier accuracy | {pct(m['tier_accuracy'])} (95% CI {pct(lo)} to {pct(hi)}) |",
        f"| Tier macro-F1 | {pct(m['tier_macro_f1'])} |",
        f"| Exact match (tier + provisions) | {pct(m['exact_match'])} |",
        f"| Provision micro-F1 | {pct(m['provision_micro']['f1'])} |",
        f"| Hallucinated provisions | {pct(m['hallucinated_provision_rate'])} |",
        f"| Invalid outputs | {pct(m['invalid_output_rate'])} |",
        f"| Critical errors (prohibited/high-risk called limited/minimal) | {pct(m['critical_error_rate'])} |",
        f"| Under-classification (less severe than gold) | {pct(m['under_classification_rate'])} |",
        "",
        "| Gold \\ Predicted | " + " | ".join(COLS) + " |",
        "|---|" + "---|" * len(COLS),
    ]
    for g in TIERS:
        out.append(f"| {g} | " + " | ".join(str(m["confusion"][g][c]) for c in COLS) + " |")
    return "\n".join(out) + "\n"
