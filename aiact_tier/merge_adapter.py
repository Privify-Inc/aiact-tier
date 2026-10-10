# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Merge a LoRA adapter into its base model and save a standalone model (safetensors).

    python -m aiact_tier.merge_adapter --base Qwen/Qwen3-4B \
        --adapter outputs/aiact-tier-lora --out outputs/aiact-tier-4b-merged
"""
import argparse


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)

    import torch
    from peft import PeftModel
    from transformers import AutoTokenizer

    from .hf_compat import load_causal_lm

    base = load_causal_lm(a.base, torch.bfloat16)
    merged = PeftModel.from_pretrained(base, a.adapter).merge_and_unload()
    merged.save_pretrained(a.out, safe_serialization=True)
    AutoTokenizer.from_pretrained(a.adapter).save_pretrained(a.out)
    print(f"merged model -> {a.out}")


if __name__ == "__main__":
    main()
