# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Benchmark runner. Same gold set, same metrics, any model.

Backends:
  majority / keyword   offline floors (no GPU)
  hf                   a local or Hugging Face model, optionally with a LoRA adapter
  openai               any OpenAI-compatible server (llama.cpp, vLLM, Ollama, or a hosted API)

Baselines get the long prompt (--mode full) that lists every allowed provision, so the
comparison is fair. The fine-tuned model uses the short prompt it was trained on.

    python -m aiact_tier.evaluate --backend keyword --name keyword
    python -m aiact_tier.evaluate --backend hf --model Qwen/Qwen3-4B --adapter outputs/aiact-tier-lora --name ours
    python -m aiact_tier.evaluate --backend hf --model Qwen/Qwen3-4B --name qwen3-4b-zero-shot
    python -m aiact_tier.evaluate --backend openai --base-url http://localhost:8080/v1 --model x --name served
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from collections import Counter
from pathlib import Path

from .baselines import keyword_predict, majority_predict
from .make_data import load_jsonl
from .metrics import evaluate, to_markdown
from .schema import build_messages, parse_output


def pick_gold(path: str | None) -> tuple[list[dict], str]:
    if path is None:
        path = next((c for c in ("data/gold.jsonl", "data/gold_ai_checked.jsonl") if Path(c).exists()), "data/gold_draft.jsonl")
    rows = load_jsonl(path)
    statuses = {r.get("status") for r in rows}
    verified = statuses <= {"verified", "ai_cross_checked"}
    status = ("VERIFIED" if statuses == {"verified"} else
              "AI CROSS-CHECKED, NOT LAWYER-REVIEWED" if verified else "DRAFT, NOT EXPERT-VERIFIED")
    if not verified:
        print(f"WARNING: {path} is not expert-verified. Do not publish these numbers.", file=sys.stderr)
    return rows, status


def call_openai(base_url: str, key: str, model: str, text: str, mode: str) -> str:
    req = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps({"model": model, "temperature": 0, "max_tokens": 128,
                         "messages": build_messages(text, mode)}).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {key}"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["choices"][0]["message"]["content"]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--gold", default=None)
    ap.add_argument("--backend", choices=["majority", "keyword", "hf", "openai"], required=True)
    ap.add_argument("--model", default=None)
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--api-key-env", default="OPENAI_API_KEY")
    ap.add_argument("--mode", choices=["short", "full"], default=None)
    ap.add_argument("--name", required=True)
    ap.add_argument("--out", default="eval/results")
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args(argv)

    gold, status = pick_gold(a.gold)
    if a.limit:
        gold = gold[: a.limit]
    texts = [g["text"] for g in gold]
    mode = a.mode or ("short" if a.adapter else "full")

    if a.backend == "keyword":
        raws = [keyword_predict(t) for t in texts]
    elif a.backend == "majority":
        train = load_jsonl("data/train.jsonl")
        top = Counter(r["tier"] for r in train).most_common(1)[0][0]
        raws = [majority_predict(t, top) for t in texts]
    elif a.backend == "hf":
        from .predict import Classifier
        raws = Classifier(a.model, a.adapter, mode).raw_batch(texts)
    else:
        key = os.environ.get(a.api_key_env, "none")
        raws = [call_openai(a.base_url, key, a.model, t, mode) for t in texts]

    preds = [parse_output(r) for r in raws]
    m = evaluate(gold, preds)
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    result = {"name": a.name, "backend": a.backend, "model": a.model, "adapter": a.adapter,
              "mode": mode, "gold_status": status, "metrics": m,
              "predictions": [{"id": g["id"], "raw": r} for g, r in zip(gold, raws)]}
    (out / f"{a.name}.json").write_text(json.dumps(result, indent=2, ensure_ascii=False))
    md = to_markdown(a.name, m, status)
    (out / f"{a.name}.md").write_text(md)
    print(md)


if __name__ == "__main__":
    main()
