# Cheapest ways to run the training (about 2,700 short examples, 3 epochs)

| Option | Cost | GPU | Notes |
|---|---|---|---|
| **Kaggle notebook** | Free (weekly GPU quota, about 30 h) | T4 16 GB (x2) | Needs a free account, phone verification and Internet switched on. Sessions up to about 9 h. Best free choice. |
| **Google Colab free** | Free | T4 16 GB | May disconnect after a few hours; run the sanity cell first. |
| **RunPod / Vast.ai, RTX 4090 or A5000 (24 GB)** | Roughly $0.3 to $0.6 per hour, so about $1 to $3 for the whole run | 24 GB | Fastest and simplest: bf16, no 4-bit needed (`make train`). Check current prices. |
| Azure (your existing account) | Quota request needed | NC/ND series | Slow to get GPU quota. Not recommended for this week. |

Free options use 4-bit QLoRA (`make train-4bit`), which gives slightly lower quality than bf16 LoRA.
If you use a free T4, report "QLoRA 4-bit" in the model card. Use the notebook
`scripts/train_on_free_gpu.ipynb`: upload the repo zip, run the cells top to bottom.

Expected time on a T4: sanity run 5 minutes, full run roughly 1.5 to 3 hours, evaluation 20 to 30 minutes.
Not yet run on a real GPU by the author, so budget one retry for version problems.
