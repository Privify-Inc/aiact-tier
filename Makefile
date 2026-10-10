BASE ?= Qwen/Qwen3-4B
ADAPTER ?= outputs/aiact-tier-lora
MERGED ?= outputs/aiact-tier-4b-merged

.PHONY: test smoke gold data baselines train train-4bit eval-ours eval-zeroshot merge gguf demo finalize-gold

test:
	python -m pytest -q

smoke:           # run this on the GPU box first: proves the whole pipeline works, about 1 minute
	python scripts/smoke_test_tiny.py

gold:            # regenerate the DRAFT gold set and the reviewer sheet
	python -m aiact_tier.gold_draft

finalize-gold:   # after reviewers finish the sheet
	python -m aiact_tier.finalize_gold

data:            # template-framed training data (add --extra data/expanded.jsonl after llm_expand)
	python -m aiact_tier.make_data --out data

baselines:
	python -m aiact_tier.evaluate --backend majority --name majority-baseline
	python -m aiact_tier.evaluate --backend keyword  --name keyword-baseline

train:
	python -m aiact_tier.train_lora --model $(BASE) --out $(ADAPTER)

train-4bit:      # 16 GB GPU (free Colab / Kaggle T4): QLoRA
	python -m aiact_tier.train_lora --model $(BASE) --out $(ADAPTER) --load-4bit --batch-size 2 --grad-accum 8

eval-zeroshot:   # the un-tuned base model, long prompt
	python -m aiact_tier.evaluate --backend hf --model $(BASE) --name base-zero-shot

eval-ours:
	python -m aiact_tier.evaluate --backend hf --model $(BASE) --adapter $(ADAPTER) --name ours

merge:
	python -m aiact_tier.merge_adapter --base $(BASE) --adapter $(ADAPTER) --out $(MERGED)

gguf:
	bash scripts/export_gguf.sh $(MERGED) outputs/gguf

demo:
	python -m aiact_tier.demo --model $(MERGED)
