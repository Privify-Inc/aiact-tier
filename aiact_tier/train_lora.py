# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""LoRA fine-tuning for the AI Act risk-tier classifier.

Fine-tunes Qwen3-4B (Alibaba Cloud / Qwen Team, Apache 2.0). Credit for the base model belongs to them.

Loss is computed on the answer only (prompt tokens are masked).

    python -m aiact_tier.train_lora --model Qwen/Qwen3-4B \
        --train data/train.jsonl --val data/val.jsonl --out outputs/aiact-tier-lora

Needs a GPU with about 24 GB for a 4B model in bf16 (A10, L4, A100, RTX 4090). On a 16 GB GPU
(free Colab/Kaggle T4) add --load-4bit (QLoRA; needs bitsandbytes). For a smaller/faster first run
use --model Qwen/Qwen3-1.7B.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
from pathlib import Path

from .schema import build_messages, format_target


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def end_token_for(tok, override: str | None) -> str:
    if override:
        return override
    return "<|im_end|>" if "<|im_end|>" in tok.get_vocab() else tok.eos_token


def encode_example(tok, row: dict, max_len: int, end_token: str):
    """Returns a dict of input_ids / labels / attention_mask, or None if it does not fit."""
    msgs = build_messages(row["text"], mode="short")
    prompt = tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True,
                                     enable_thinking=False)
    completion = format_target(row["tier"], row["provisions"]) + end_token
    p_ids = tok(prompt, add_special_tokens=False)["input_ids"]
    c_ids = tok(completion, add_special_tokens=False)["input_ids"]
    if len(p_ids) + len(c_ids) > max_len:
        return None
    ids = p_ids + c_ids
    return {"input_ids": ids, "labels": [-100] * len(p_ids) + c_ids, "attention_mask": [1] * len(ids)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3-4B")
    ap.add_argument("--train", default="data/train.jsonl")
    ap.add_argument("--val", default="data/val.jsonl")
    ap.add_argument("--out", default="outputs/aiact-tier-lora")
    ap.add_argument("--epochs", type=float, default=3.0)
    ap.add_argument("--lr", type=float, default=2e-4)
    ap.add_argument("--batch-size", type=int, default=4)
    ap.add_argument("--grad-accum", type=int, default=4)
    ap.add_argument("--max-len", type=int, default=512)
    ap.add_argument("--rank", type=int, default=16)
    ap.add_argument("--alpha", type=int, default=32)
    ap.add_argument("--dropout", type=float, default=0.05)
    ap.add_argument("--seed", type=int, default=13)
    ap.add_argument("--max-steps", type=int, default=-1, help="for smoke tests")
    ap.add_argument("--end-token", default=None)
    ap.add_argument("--no-grad-ckpt", action="store_true")
    ap.add_argument("--load-4bit", action="store_true",
                    help="QLoRA: 4-bit base model, fits a 16 GB GPU (T4). Requires bitsandbytes and CUDA.")
    a = ap.parse_args(argv)

    import torch
    from peft import LoraConfig, get_peft_model
    from torch.utils.data import Dataset
    from transformers import AutoTokenizer, Trainer, TrainingArguments

    from .hf_compat import load_causal_lm, load_causal_lm_4bit, warmup_kwargs

    random.seed(a.seed)
    torch.manual_seed(a.seed)

    tok = AutoTokenizer.from_pretrained(a.model)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token
    end = end_token_for(tok, a.end_token)

    def prep(path):
        rows, skipped = [], 0
        for r in load_jsonl(path):
            e = encode_example(tok, r, a.max_len, end)
            if e is None:
                skipped += 1
            else:
                rows.append(e)
        return rows, skipped

    train_rows, sk1 = prep(a.train)
    val_rows, sk2 = prep(a.val) if a.val and Path(a.val).exists() else ([], 0)
    print(f"train={len(train_rows)} val={len(val_rows)} skipped_too_long={sk1 + sk2}")

    class Rows(Dataset):
        def __init__(self, rows):
            self.rows = rows

        def __len__(self):
            return len(self.rows)

        def __getitem__(self, i):
            return self.rows[i]

    pad_id = tok.pad_token_id

    def collate(batch):
        m = max(len(b["input_ids"]) for b in batch)
        pad = lambda seq, v: seq + [v] * (m - len(seq))
        return {
            "input_ids": torch.tensor([pad(b["input_ids"], pad_id) for b in batch]),
            "attention_mask": torch.tensor([pad(b["attention_mask"], 0) for b in batch]),
            "labels": torch.tensor([pad(b["labels"], -100) for b in batch]),
        }

    use_cuda = torch.cuda.is_available()
    bf16 = use_cuda and torch.cuda.is_bf16_supported()
    dtype = torch.bfloat16 if bf16 else torch.float32
    if use_cuda and not bf16 and not a.load_4bit:
        print("WARNING: bf16 not supported on this GPU; training in float32 (slower, more memory).")

    fp16 = False
    if a.load_4bit:
        if not use_cuda:
            raise SystemExit("--load-4bit needs a CUDA GPU")
        compute = torch.bfloat16 if bf16 else torch.float16
        fp16 = not bf16
        model = load_causal_lm_4bit(a.model, compute)
        from peft import prepare_model_for_kbit_training
        model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=not a.no_grad_ckpt)
        model.config.use_cache = False
    else:
        model = load_causal_lm(a.model, dtype)
        model.config.use_cache = False
        if not a.no_grad_ckpt:
            model.gradient_checkpointing_enable()
            model.enable_input_require_grads()
    model = get_peft_model(model, LoraConfig(
        r=a.rank, lora_alpha=a.alpha, lora_dropout=a.dropout,
        target_modules="all-linear", task_type="CAUSAL_LM"))
    model.print_trainable_parameters()

    args = TrainingArguments(
        output_dir=a.out,
        num_train_epochs=a.epochs,
        max_steps=a.max_steps,
        per_device_train_batch_size=a.batch_size,
        per_device_eval_batch_size=a.batch_size,
        gradient_accumulation_steps=a.grad_accum,
        learning_rate=a.lr,
        lr_scheduler_type="cosine",
        **warmup_kwargs(0.03),
        logging_steps=10,
        eval_strategy="epoch" if val_rows else "no",
        save_strategy="epoch",
        save_total_limit=2,
        bf16=bf16,
        fp16=fp16,
        report_to="none",
        seed=a.seed,
        remove_unused_columns=False,
        gradient_checkpointing=not a.no_grad_ckpt,
    )
    trainer = Trainer(model=model, args=args, train_dataset=Rows(train_rows),
                      eval_dataset=Rows(val_rows) if val_rows else None, data_collator=collate)
    trainer.train()
    trainer.save_model(a.out)
    tok.save_pretrained(a.out)

    import peft, transformers
    meta = {
        "base_model": a.model, "args": vars(a),
        "train_sha256": hashlib.sha256(Path(a.train).read_bytes()).hexdigest(),
        "versions": {"torch": torch.__version__, "transformers": transformers.__version__,
                     "peft": peft.__version__},
    }
    (Path(a.out) / "train_meta.json").write_text(json.dumps(meta, indent=2))
    print(f"saved adapter -> {a.out}")


if __name__ == "__main__":
    main()
