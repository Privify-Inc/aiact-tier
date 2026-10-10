# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Turn the completed reviewer sheet into the verified gold set (data/gold.jsonl).

Workflow (see docs/LABELING_GUIDE.md):
  1. Two reviewers fill reviewer1_* and reviewer2_* independently in eval/gold_review_sheet.csv.
  2. Where they disagree, a lead reviewer fills final_tier / final_provisions.
  3. Run:  python -m aiact_tier.finalize_gold --sheet eval/gold_review_sheet.csv

Rows are accepted when both reviewers agree, or when final_* is filled. Anything else is
listed and the script exits without writing. Reviewers may append new rows (id starting "N-").
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

from .taxonomy import SEVERITY, TIERS, normalize_provision, sort_provisions


def parse_provs(s: str) -> list[str]:
    return [p.strip() for p in re.split(r"[;,]\s*", s or "") if p.strip()]


def canon(provs: list[str], problems: list[str], rid: str) -> list[str]:
    out = []
    for p in provs:
        n = normalize_provision(p)
        if n is None:
            problems.append(f"{rid}: unknown provision '{p}'")
        else:
            out.append(n)
    return sort_provisions(out)


def cohen_kappa(a: list[str], b: list[str]) -> float:
    n = len(a)
    if n == 0:
        return 0.0
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum((ca[t] / n) * (cb[t] / n) for t in TIERS)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def finalize(rows: list[dict], draft_by_id: dict[str, dict], status: str = "verified"):
    gold, problems = [], []
    r1, r2 = [], []
    agreed = changed = 0
    for row in rows:
        rid = row["id"].strip()
        text = row["system_description"].strip()
        if not rid or not text:
            continue
        t1, t2 = row.get("reviewer1_tier", "").strip(), row.get("reviewer2_tier", "").strip()
        p1 = canon(parse_provs(row.get("reviewer1_provisions", "")), problems, rid)
        p2 = canon(parse_provs(row.get("reviewer2_provisions", "")), problems, rid)
        ft = row.get("final_tier", "").strip()
        fp = canon(parse_provs(row.get("final_provisions", "")), problems, rid)
        if t1 and t2:
            r1.append(t1)
            r2.append(t2)
        if ft:
            tier, provs = ft, fp
        elif t1 and t1 == t2 and p1 == p2:
            tier, provs = t1, p1
            agreed += 1
        else:
            problems.append(f"{rid}: reviewers disagree or are missing; fill final_tier/final_provisions")
            continue
        if tier not in SEVERITY:
            problems.append(f"{rid}: invalid tier '{tier}'")
            continue
        if tier == "minimal" and provs:
            problems.append(f"{rid}: minimal must have no provisions")
            continue
        d = draft_by_id.get(rid, {})
        if d and (d["tier"], d["provisions"]) != (tier, provs):
            changed += 1
        gold.append({"id": rid, "text": text, "tier": tier, "provisions": provs,
                     "category": d.get("category", "expert"), "difficulty": d.get("difficulty", "expert"),
                     "note": row.get("comments", "").strip(), "status": status})
    if problems:
        raise ValueError("\n".join(problems))
    stats = {"n": len(gold), "agreed_without_adjudication": agreed,
             "changed_from_draft": changed,
             "tier_kappa_reviewer1_vs_reviewer2": round(cohen_kappa(r1, r2), 3) if r1 else None}
    return gold, stats


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", default="eval/gold_review_sheet.csv")
    ap.add_argument("--draft", default="data/gold_draft.jsonl")
    ap.add_argument("--out", default="data/gold.jsonl")
    ap.add_argument("--status", default="verified", choices=["verified", "ai_cross_checked"],
                    help="use ai_cross_checked when the reviewers were AI models, not human experts")
    a = ap.parse_args(argv)
    with open(a.sheet, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    draft = {}
    if Path(a.draft).exists():
        draft = {json.loads(l)["id"]: json.loads(l) for l in open(a.draft, encoding="utf-8") if l.strip()}
    try:
        gold, stats = finalize(rows, draft, a.status)
    except ValueError as e:
        print("Cannot finalize:\n" + str(e))
        raise SystemExit(1)
    with open(a.out, "w", encoding="utf-8") as f:
        for g in gold:
            f.write(json.dumps(g, ensure_ascii=False) + "\n")
    print(f"wrote {len(gold)} rows with status {a.status} -> {a.out}")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
