# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Prompts and output format shared by training, inference and evaluation."""
from __future__ import annotations

import json
import re

from .taxonomy import SEVERITY, TAXONOMY, TIERS, normalize_provision, sort_provisions

SYSTEM_SHORT = (
    "Classify the AI system described by the user under the EU AI Act. "
    'Reply with JSON only: {"tier": "prohibited|high_risk|limited_transparency|minimal", '
    '"provisions": [citations of the applicable provisions]}.'
)


def _build_full() -> str:
    lines = [
        "You classify AI systems under the EU AI Act (Regulation (EU) 2024/1689).",
        "Tiers, from most to least severe: prohibited, high_risk, limited_transparency, minimal.",
        "Choose the most severe tier that applies. List every applicable provision from the allowed list.",
        "Use an empty provisions list for minimal. Reply with JSON only, for example:",
        '{"tier": "high_risk", "provisions": ["Annex III(4)(a)", "Art. 50(1)"]}',
        "",
        "Allowed provisions:",
    ]
    seen = set()
    for c in TAXONOMY:
        if c["citation"] and c["citation"] not in seen and c["tier"] != "minimal":
            seen.add(c["citation"])
            lines.append(f'- {c["citation"]} ({c["tier"]}): {c["summary"]}')
    lines.append("- Art. 50(3) (transparency): deployers of emotion recognition or biometric categorization "
                 "systems must inform the people exposed to them.")
    return "\n".join(lines)


SYSTEM_FULL = _build_full()


def build_messages(text: str, mode: str = "short") -> list[dict]:
    system = SYSTEM_SHORT if mode == "short" else SYSTEM_FULL
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": f"AI system description:\n{text.strip()}"},
    ]


def format_target(tier: str, provisions: list[str]) -> str:
    return json.dumps({"tier": tier, "provisions": sort_provisions(provisions)}, separators=(",", ":"))


_THINK = re.compile(r"<think>.*?</think>", re.DOTALL)


def parse_output(raw: str) -> dict:
    """Parse model output. Never raises.

    Returns {"ok", "tier", "provisions" (valid, canonical), "invalid_provisions"}.
    ok is False when no JSON object with a valid tier could be read.
    """
    bad = {"ok": False, "tier": None, "provisions": [], "invalid_provisions": []}
    if not isinstance(raw, str):
        return bad
    text = _THINK.sub("", raw).strip()
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        return bad
    try:
        obj = json.loads(text[start : end + 1])
    except json.JSONDecodeError:
        return bad
    if not isinstance(obj, dict):
        return bad
    tier = obj.get("tier")
    if tier not in SEVERITY:
        return bad
    provs = obj.get("provisions", [])
    if not isinstance(provs, list):
        provs = []
    valid, invalid = [], []
    for p in provs:
        n = normalize_provision(p)
        if n:
            valid.append(n)
        else:
            invalid.append(str(p))
    return {"ok": True, "tier": tier, "provisions": sort_provisions(valid), "invalid_provisions": invalid}


__all__ = ["SYSTEM_SHORT", "SYSTEM_FULL", "build_messages", "format_target", "parse_output", "TIERS"]
