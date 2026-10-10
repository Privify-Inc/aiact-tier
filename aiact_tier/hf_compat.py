# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Small shims so the code runs on transformers 4.51+ and 5.x."""
from __future__ import annotations

import inspect


def load_causal_lm(path: str, dtype):
    """transformers 5 renamed torch_dtype -> dtype; try the new name, fall back to the old."""
    from transformers import AutoModelForCausalLM

    try:
        return AutoModelForCausalLM.from_pretrained(path, dtype=dtype)
    except TypeError:
        return AutoModelForCausalLM.from_pretrained(path, torch_dtype=dtype)


def warmup_kwargs(ratio: float) -> dict:
    """transformers 5 removed warmup_ratio (warmup_steps accepts a float ratio instead)."""
    from transformers import TrainingArguments

    params = inspect.signature(TrainingArguments.__init__).parameters
    return {"warmup_ratio": ratio} if "warmup_ratio" in params else {"warmup_steps": ratio}


def load_causal_lm_4bit(path: str, compute_dtype):
    """QLoRA: load the frozen base model in 4-bit (needs a CUDA GPU and bitsandbytes)."""
    import torch
    from transformers import AutoModelForCausalLM, BitsAndBytesConfig

    cfg = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_use_double_quant=True, bnb_4bit_compute_dtype=compute_dtype)
    return AutoModelForCausalLM.from_pretrained(path, quantization_config=cfg,
                                                device_map={"": torch.cuda.current_device()})
