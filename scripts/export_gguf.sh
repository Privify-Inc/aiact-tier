#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
# Convert the merged model to GGUF and quantize it so it runs in Ollama, llama.cpp and LM Studio.
# Usage: scripts/export_gguf.sh outputs/aiact-tier-4b-merged outputs/gguf
# Requires: git, cmake, a C++ toolchain, python with the repo requirements installed.
set -euo pipefail

MERGED="${1:?path to merged HF model}"
OUT="${2:-outputs/gguf}"
mkdir -p "$OUT"

if [ ! -d llama.cpp ]; then
  git clone --depth 1 https://github.com/ggml-org/llama.cpp
fi
pip install -q -r llama.cpp/requirements/requirements-convert_hf_to_gguf.txt
cmake -S llama.cpp -B llama.cpp/build -DCMAKE_BUILD_TYPE=Release >/dev/null
cmake --build llama.cpp/build --target llama-quantize -j >/dev/null

python llama.cpp/convert_hf_to_gguf.py "$MERGED" --outfile "$OUT/aiact-tier-f16.gguf" --outtype f16
for Q in Q8_0 Q4_K_M; do
  llama.cpp/build/bin/llama-quantize "$OUT/aiact-tier-f16.gguf" "$OUT/aiact-tier-$Q.gguf" "$Q"
done
ls -lh "$OUT"
echo "Re-run the benchmark on the quantized files (evaluate.py --backend openai against llama-server)"
echo "and publish the quantized scores next to the full-precision ones."
