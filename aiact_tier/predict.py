# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Inference helper and CLI.

    python -m aiact_tier.predict --model outputs/aiact-tier-4b-merged "A chatbot that ..."
    python -m aiact_tier.predict --model Qwen/Qwen3-4B --adapter outputs/aiact-tier-lora "..."

Output is a decision aid, not legal advice.
"""
from __future__ import annotations

import argparse
import json

from .schema import build_messages, parse_output


class Classifier:
    def __init__(self, model: str, adapter: str | None = None, mode: str | None = None,
                 max_new_tokens: int = 64):
        import torch
        from transformers import AutoTokenizer

        from .hf_compat import load_causal_lm

        self.torch = torch
        self.mode = mode or ("short" if adapter or "aiact" in model.lower() else "full")
        self.max_new_tokens = max_new_tokens
        self.tok = AutoTokenizer.from_pretrained(model)  # adapters share the base tokenizer
        self.tok.padding_side = "left"
        if self.tok.pad_token is None:
            self.tok.pad_token = self.tok.eos_token
        if torch.cuda.is_available():
            dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16  # T4 has no bf16
        else:
            dtype = torch.float32
        self.model = load_causal_lm(model, dtype)
        if adapter:
            from peft import PeftModel
            self.model = PeftModel.from_pretrained(self.model, adapter)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device).eval()

    def raw_batch(self, texts: list[str], batch_size: int = 2) -> list[str]:
        out = []
        for i in range(0, len(texts), batch_size):
            prompts = [
                self.tok.apply_chat_template(build_messages(t, self.mode), tokenize=False,
                                             add_generation_prompt=True, enable_thinking=False)
                for t in texts[i : i + batch_size]
            ]
            enc = self.tok(prompts, return_tensors="pt", padding=True, add_special_tokens=False).to(self.device)
            with self.torch.no_grad():
                gen = self.model.generate(**enc, max_new_tokens=self.max_new_tokens, do_sample=False,
                                          pad_token_id=self.tok.pad_token_id)
            for row in gen:
                out.append(self.tok.decode(row[enc["input_ids"].shape[1]:], skip_special_tokens=True))
        return out

    def classify(self, text: str) -> dict:
        raw = self.raw_batch([text], batch_size=1)[0]
        return {"raw": raw, **parse_output(raw)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("text")
    ap.add_argument("--model", required=True)
    ap.add_argument("--adapter", default=None)
    a = ap.parse_args(argv)
    print(json.dumps(Classifier(a.model, a.adapter).classify(a.text), indent=2))


if __name__ == "__main__":
    main()
