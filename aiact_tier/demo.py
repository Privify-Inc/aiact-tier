# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""One-command demo (Gradio web UI or plain CLI).

    pip install gradio
    python -m aiact_tier.demo --model outputs/aiact-tier-4b-merged

Without a GPU or model, try the offline keyword floor:
    python -m aiact_tier.demo --backend keyword --cli "A spam filter for email"
"""
from __future__ import annotations

import argparse
import json

from .baselines import keyword_predict
from .schema import parse_output

DISCLAIMER = ("Decision aid only, not legal advice. Outputs can be wrong. "
              "Have a qualified person review any compliance decision.")


def make_fn(args):
    if args.backend == "keyword":
        return lambda text: {"raw": (r := keyword_predict(text)), **parse_output(r)}
    from .predict import Classifier
    return Classifier(args.model, args.adapter).classify


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("text", nargs="?")
    ap.add_argument("--backend", choices=["hf", "keyword"], default="hf")
    ap.add_argument("--model", default=None)
    ap.add_argument("--adapter", default=None)
    ap.add_argument("--cli", action="store_true")
    a = ap.parse_args(argv)
    fn = make_fn(a)

    if a.cli or a.text:
        res = fn(a.text or input("Describe the AI system: "))
        print(json.dumps(res, indent=2))
        print(DISCLAIMER)
        return

    import gradio as gr

    def run(text):
        r = fn(text)
        return r["tier"] or "invalid output", ", ".join(r["provisions"]) or "none", r["raw"]

    gr.Interface(
        fn=run,
        inputs=gr.Textbox(lines=5, label="Describe the AI system"),
        outputs=[gr.Textbox(label="Risk tier"), gr.Textbox(label="Provisions"), gr.Textbox(label="Raw output")],
        title="Privify AI Act risk-tier classifier (v0.1)",
        description=DISCLAIMER,
    ).launch()


if __name__ == "__main__":
    main()
