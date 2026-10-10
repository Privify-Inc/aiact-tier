# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Expand seed descriptions into diverse paraphrases with an LLM you control.

Why: template framing (make_data.py) is low-diversity. LLM paraphrases give real variety.

Providers (set the key as an environment variable, never in code):
  --provider openai     any OpenAI-compatible endpoint (OPENAI_API_KEY, optional OPENAI_BASE_URL)
                        works with vLLM, llama.cpp server, Ollama, or a hosted API
  --provider anthropic  Anthropic Messages API (ANTHROPIC_API_KEY)

LEGAL CHECK FIRST: some model providers restrict using their outputs to train other models.
Read the terms of whichever model you use and have counsel confirm (see docs/COUNSEL_MEMO.md).
Record the provider and model in the model card's data provenance section.

Output: data/expanded.jsonl rows {category, seed_index, text, source}. Labels are inherited
from the seed's category, so a human must spot-check at least 5 percent before training.

    python -m aiact_tier.llm_expand --provider openai --model <name> --n 12
"""
from __future__ import annotations

import argparse
import json
import os
import re
import urllib.request
from pathlib import Path

from .make_data import jaccard, load_jsonl
from .seeds import SEEDS

PROMPT = """You are helping build a test-free training set for an EU AI Act risk classifier.
Rewrite the AI system description below in {n} different ways.

Rules:
- Keep the legal characterization identical. Do not add or remove facts that would change which
  EU AI Act category applies (who uses it, what it decides, whom it affects, the setting).
- Vary the domain details, wording, sentence structure, and length (1 to 3 sentences each).
- Describe fictional systems only. Use no real company names or real people.
- Do NOT mention the EU AI Act, articles, annexes, or words like prohibited, high-risk, or risk tier.
- Return ONLY a JSON array of {n} strings.

Description:
{text}
"""

LEAK = re.compile(r"\b(prohibited|high[- ]risk|annex|article \d|ai act|risk tier|limited risk|minimal risk)\b", re.I)


def build_prompt(text: str, n: int) -> str:
    return PROMPT.format(n=n, text=text)


def parse_list(raw: str) -> list[str]:
    start, end = raw.find("["), raw.rfind("]")
    if start < 0 or end <= start:
        return []
    try:
        arr = json.loads(raw[start : end + 1])
    except json.JSONDecodeError:
        return []
    return [s.strip() for s in arr if isinstance(s, str) and s.strip()]


def call_openai(model: str, prompt: str) -> str:
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=json.dumps({"model": model, "temperature": 0.9,
                         "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["choices"][0]["message"]["content"]


def call_anthropic(model: str, prompt: str) -> str:
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps({"model": model, "max_tokens": 2000,
                         "messages": [{"role": "user", "content": prompt}]}).encode(),
        headers={"Content-Type": "application/json", "anthropic-version": "2023-06-01",
                 "x-api-key": os.environ["ANTHROPIC_API_KEY"]},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return "".join(b.get("text", "") for b in json.load(r)["content"])


def keep(text: str, gold: list[dict], seen: set[str]) -> bool:
    words = len(text.split())
    if words < 8 or words > 90 or LEAK.search(text) or text.lower() in seen:
        return False
    return not any(jaccard(text, g["text"]) >= 0.6 for g in gold)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=["openai", "anthropic"], required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--n", type=int, default=12, help="paraphrases per seed")
    ap.add_argument("--out", default="data/expanded.jsonl")
    ap.add_argument("--gold", default="data/gold_draft.jsonl")
    a = ap.parse_args(argv)

    call = call_openai if a.provider == "openai" else call_anthropic
    gold = load_jsonl(a.gold) if Path(a.gold).exists() else []
    seen: set[str] = set()
    rows = []
    for cid, texts in SEEDS.items():
        for i, t in enumerate(texts):
            try:
                got = parse_list(call(a.model, build_prompt(t, a.n)))
            except Exception as e:  # network or API error: skip this seed, keep going
                print(f"[skip] {cid}:{i} -> {e}")
                continue
            for g in got:
                if keep(g, gold, seen):
                    seen.add(g.lower())
                    rows.append({"category": cid, "seed_index": i, "text": g,
                                 "source": f"llm:{a.provider}:{a.model}"})
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"wrote {len(rows)} paraphrases -> {a.out}. Spot-check at least 5% before training.")


if __name__ == "__main__":
    main()
