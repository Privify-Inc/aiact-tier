# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Build synthetic training data from the seed descriptions.

Template framing only adds label-neutral context (vendor, deployment, stage). It adds NO new
legal facts. For real diversity, run llm_expand.py and pass its output with --extra.

    python -m aiact_tier.make_data --out data
"""
from __future__ import annotations

import argparse
import json
import random
import re
from collections import Counter
from pathlib import Path

from .seeds import COMBOS, SEEDS
from .taxonomy import BY_ID, label_for, sort_provisions

PRE = ["", "Product description: ", "Vendor pitch: ", "Internal project brief: ",
       "AI system under review: ", "Description: "]
POST = ["", " It is sold as a cloud service.", " It runs on-premises at the customer's site.",
        " The vendor is a European startup.", " The vendor is based outside the EU but sells into the EU.",
        " It is currently in the pilot stage.", " It was first released this year.",
        " It is used in several countries."]


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def jaccard(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    return len(ta & tb) / len(ta | tb) if ta and tb else 0.0


def variants(text: str, rng: random.Random, n: int) -> list[str]:
    combos = sorted({(a, b) for a in PRE for b in POST})
    rng.shuffle(combos)
    out = [text]
    for a, b in combos:
        if len(out) >= n:
            break
        v = f"{a}{text}{b}"
        if v not in out:
            out.append(v)
    return out


def seed_items():
    """Yield (group, text, tier, provisions, category)."""
    for cid, texts in SEEDS.items():
        lab = label_for(cid)
        for i, t in enumerate(texts):
            yield f"{cid}:{i}", t, lab["tier"], lab["provisions"], cid
    for i, (t, tier, provs) in enumerate(COMBOS):
        yield f"COMBO:{i}", t, tier, sort_provisions(provs), "combo"


def load_jsonl(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def build(per_seed: int, val_frac: float, seed: int, extra: str | None, gold_path: str | None):
    rng = random.Random(seed)
    items = list(seed_items())
    gold = load_jsonl(gold_path) if gold_path and Path(gold_path).exists() else []

    rows = []
    for group, text, tier, provs, cat in items:
        # Minimal is the open-ended "everything else" class: give it more variants per seed.
        n_var = min(per_seed * 3, len(PRE) * len(POST)) if tier == "minimal" else per_seed
        for j, v in enumerate(variants(text, rng, n_var)):
            rows.append({"id": f"{group}:{j}", "group": group, "text": v, "tier": tier,
                         "provisions": provs, "category": cat, "source": "template"})

    if extra and Path(extra).exists():
        for k, r in enumerate(load_jsonl(extra)):
            cid = r["category"]
            lab = label_for(cid) if cid in BY_ID else {"tier": r["tier"], "provisions": r["provisions"]}
            rows.append({"id": f"LLM:{cid}:{k}", "group": f"LLM:{cid}:{r.get('seed_index', k)}",
                         "text": r["text"], "tier": lab["tier"], "provisions": lab["provisions"],
                         "category": cid, "source": "llm"})

    # drop anything too close to a gold item
    kept, dropped = [], 0
    for r in rows:
        if any(jaccard(r["text"], g["text"]) >= 0.6 for g in gold):
            dropped += 1
            continue
        kept.append(r)

    groups = sorted({r["group"] for r in kept})
    rng.shuffle(groups)
    val_groups = set(groups[: max(1, int(len(groups) * val_frac))])
    train = [r for r in kept if r["group"] not in val_groups]
    val = [r for r in kept if r["group"] in val_groups]
    return train, val, dropped


def write_jsonl(path: Path, rows: list[dict]):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data")
    ap.add_argument("--per-seed", type=int, default=16)
    ap.add_argument("--val-frac", type=float, default=0.1)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--extra", default="data/expanded.jsonl", help="LLM-expanded examples (optional)")
    ap.add_argument("--gold", default="data/gold_ai_checked.jsonl", help="used only to drop near-duplicates")
    a = ap.parse_args(argv)

    train, val, dropped = build(a.per_seed, a.val_frac, a.seed, a.extra, a.gold)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    write_jsonl(out / "train.jsonl", train)
    write_jsonl(out / "val.jsonl", val)
    print(f"train={len(train)} val={len(val)} dropped_near_gold={dropped}")
    print("train tiers:", dict(Counter(r["tier"] for r in train)))
    print("sources:", dict(Counter(r["source"] for r in train)))


if __name__ == "__main__":
    main()
