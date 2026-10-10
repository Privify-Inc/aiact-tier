# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Trivial offline baselines. They give the benchmark a floor and need no GPU or network."""
from __future__ import annotations

import re

from .schema import format_target

_RULES = [
    # (pattern, tier, provisions)
    (r"social (score|scoring)|trust score|reliability rating|civic", "prohibited", ["Art. 5(1)(c)"]),
    (r"subliminal|imperceptible|sub-threshold|covert persuasion", "prohibited", ["Art. 5(1)(a)"]),
    (r"scrap\w*|crawl\w*|harvest\w*", "prohibited", ["Art. 5(1)(e)"]),
    (r"sexual orientation|religion|political leaning", "prohibited", ["Art. 5(1)(g)"]),
    (r"emotion|mood", "high_risk", ["Annex III(1)(c)", "Art. 50(3)"]),
    (r"credit|loan|creditworth", "high_risk", ["Annex III(5)(b)"]),
    (r"insurance|premium", "high_risk", ["Annex III(5)(c)"]),
    (r"recruit|candidate|r[eé]sum[eé]|\bcvs?\b|applicant|hiring", "high_risk", ["Annex III(4)(a)"]),
    (r"employee|worker|courier|promotion|dismiss", "high_risk", ["Annex III(4)(b)"]),
    (r"exam|student|pupil|school|admission|grade|grader", "high_risk", ["Annex III(3)(a)"]),
    (r"asylum|visa|border|migra", "high_risk", ["Annex III(7)(b)"]),
    (r"police|law enforcement|prosecut|suspect|offen[cd]", "high_risk", ["Annex III(6)(e)"]),
    (r"court|judge|judicial|arbitrat", "high_risk", ["Annex III(8)(a)"]),
    (r"voter|election|referendum", "high_risk", ["Annex III(8)(b)"]),
    (r"benefit|entitle", "high_risk", ["Annex III(5)(a)"]),
    (r"emergency|ambulance|triage|dispatch", "high_risk", ["Annex III(5)(d)"]),
    (r"deepfake|face-swap|never (said|spoke)|never took place", "limited_transparency", ["Art. 50(4)"]),
    (r"chatbot|virtual agent|assistant|chat window|voice bot|phone agent", "limited_transparency", ["Art. 50(1)"]),
    (r"generates?|text-to-|synthetic", "limited_transparency", ["Art. 50(2)"]),
]


def keyword_predict(text: str) -> str:
    t = text.lower()
    for pat, tier, provs in _RULES:
        if re.search(pat, t):
            return format_target(tier, provs)
    return format_target("minimal", [])


def majority_predict(_text: str, tier: str = "high_risk") -> str:
    return format_target(tier, [])
