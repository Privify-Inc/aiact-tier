# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Pre-flight check: runs the REAL train -> infer -> evaluate code paths on CPU with a tiny
random Qwen3 model and a toy tokenizer. Needs no downloads and no GPU, and takes about a minute.

It proves the plumbing works (data encoding, answer-only loss masking, LoRA, adapter loading,
generation, JSON parsing, metrics). It says NOTHING about model quality.

    python scripts/smoke_test_tiny.py
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tokenizers import Tokenizer, decoders, models, pre_tokenizers, trainers  # noqa: E402
from transformers import PreTrainedTokenizerFast, Qwen3Config, Qwen3ForCausalLM  # noqa: E402

from aiact_tier import evaluate as ev  # noqa: E402
from aiact_tier import train_lora  # noqa: E402
from aiact_tier.predict import Classifier  # noqa: E402
from aiact_tier.schema import SYSTEM_FULL, SYSTEM_SHORT  # noqa: E402
from aiact_tier.seeds import SEEDS  # noqa: E402

CHAT = ("{% for m in messages %}<|im_start|>{{ m.role }}\n{{ m.content }}<|im_end|>\n{% endfor %}"
        "{% if add_generation_prompt %}<|im_start|>assistant\n{% endif %}")


def main():
    tmp = Path(tempfile.mkdtemp(prefix="aiact-smoke-"))
    corpus = [t for ts in SEEDS.values() for t in ts] + [SYSTEM_SHORT, SYSTEM_FULL,
              '{"tier":"high_risk","provisions":["Annex III(4)(a)","Art. 50(1)"]}']
    tk = Tokenizer(models.BPE())
    tk.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tk.decoder = decoders.ByteLevel()
    tk.train_from_iterator(corpus, trainers.BpeTrainer(
        vocab_size=1500, special_tokens=["<|endoftext|>", "<|im_start|>", "<|im_end|>"],
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet()))
    tok = PreTrainedTokenizerFast(tokenizer_object=tk, eos_token="<|im_end|>", pad_token="<|endoftext|>")
    tok.chat_template = CHAT

    # Loss must cover ONLY the answer (plus end token); the prompt must be fully masked.
    enc = train_lora.encode_example(tok, {"text": "A spam filter.", "tier": "minimal", "provisions": []},
                                    512, "<|im_end|>")
    answer = tok.decode([t for t in enc["labels"] if t != -100])
    assert answer == '{"tier":"minimal","provisions":[]}<|im_end|>', f"bad label masking: {answer!r}"
    assert enc["labels"][0] == -100 and len(enc["labels"]) == len(enc["input_ids"])
    print("label masking OK:", answer)

    cfg = Qwen3Config(vocab_size=len(tok), hidden_size=64, intermediate_size=128, num_hidden_layers=2,
                      num_attention_heads=4, num_key_value_heads=2, head_dim=16,
                      max_position_embeddings=2048)
    base = tmp / "tiny-base"
    Qwen3ForCausalLM(cfg).save_pretrained(base)
    tok.save_pretrained(base)

    adapter = tmp / "adapter"
    train_lora.main(["--model", str(base), "--train", "data/train.jsonl", "--val", "data/val.jsonl",
                     "--out", str(adapter), "--max-steps", "4", "--batch-size", "2", "--grad-accum", "1",
                     "--max-len", "512", "--rank", "4", "--alpha", "8"])
    assert (adapter / "adapter_config.json").exists(), "adapter not saved"
    assert (adapter / "train_meta.json").exists()

    clf = Classifier(str(base), str(adapter), mode="short", max_new_tokens=12)
    outs = clf.raw_batch(["A spam filter.", "A social scoring platform for citizens."], batch_size=2)
    assert len(outs) == 2 and all(isinstance(o, str) for o in outs)
    print("sample raw outputs from the (untrained-quality) tiny model:", [o[:40] for o in outs])

    ev.main(["--backend", "hf", "--model", str(base), "--adapter", str(adapter), "--name", "smoke",
             "--out", str(tmp / "results"), "--limit", "4"])
    res = json.loads((tmp / "results" / "smoke.json").read_text())
    assert res["metrics"]["n"] == 4
    print("SMOKE TEST PASSED: train -> adapter -> generate -> parse -> metrics all ran.")


if __name__ == "__main__":
    main()
