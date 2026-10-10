# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Label space for the Privify AI Act risk-tier classifier (v0.1).

Single source of truth: every provision string the model may emit is defined here.
Summaries are our own paraphrases of Regulation (EU) 2024/1689 (the EU AI Act).
They are NOT legal advice. Verify against the Official Journal text.

Tier = the most severe tier that applies. A system can carry several provisions
(for example a hiring chatbot is high_risk under Annex III(4)(a) and also
subject to Art. 50(1) because it talks to people).

Known gaps in v0.1 (listed in MODEL_CARD.md as well):
  - Prohibited practices added by the 2026 Digital Omnibus on AI are not covered yet.
  - The Art. 6(3) "not high-risk" derogation for Annex III systems is not modeled.
  - Annex I (product-safety) coverage is a single coarse category.
  - General-purpose AI model obligations (Art. 51 onward) are out of scope.
  - Application dates and deadlines are out of scope.
"""
from __future__ import annotations

import re

TIERS = ["prohibited", "high_risk", "limited_transparency", "minimal"]
SEVERITY = {t: i for i, t in enumerate(TIERS)}  # 0 = most severe


def _cat(cid, tier, citation, title, summary, also=()):
    return {
        "id": cid,
        "tier": tier,
        "citation": citation,
        "title": title,
        "summary": summary,
        "also": list(also),
    }


TAXONOMY = [
    # ------------------------------------------------------------------ Art. 5(1): prohibited
    _cat("P_a", "prohibited", "Art. 5(1)(a)", "Manipulative or deceptive techniques",
         "Subliminal, purposefully manipulative or deceptive techniques that materially distort "
         "behavior and are likely to cause significant harm."),
    _cat("P_b", "prohibited", "Art. 5(1)(b)", "Exploiting vulnerabilities",
         "Exploiting vulnerabilities due to age, disability or a specific social or economic "
         "situation to materially distort behavior in a harmful way."),
    _cat("P_c", "prohibited", "Art. 5(1)(c)", "Social scoring",
         "Evaluating or classifying people over time by social behavior or personal traits, "
         "leading to detrimental treatment in unrelated contexts or unjustified, disproportionate treatment."),
    _cat("P_d", "prohibited", "Art. 5(1)(d)", "Crime prediction by profiling alone",
         "Predicting that a person will commit a criminal offence based solely on profiling or "
         "personality traits, not on objective facts directly linked to criminal activity."),
    _cat("P_e", "prohibited", "Art. 5(1)(e)", "Untargeted facial image scraping",
         "Building or expanding facial recognition databases through untargeted scraping of facial "
         "images from the internet or CCTV."),
    _cat("P_f", "prohibited", "Art. 5(1)(f)", "Emotion inference at work or school",
         "Inferring emotions of people in the workplace or in education institutions, except for "
         "medical or safety reasons."),
    _cat("P_g", "prohibited", "Art. 5(1)(g)", "Sensitive biometric categorization",
         "Biometric categorization that infers race, political opinions, trade union membership, "
         "religious or philosophical beliefs, sex life or sexual orientation."),
    _cat("P_h", "prohibited", "Art. 5(1)(h)", "Real-time remote biometric ID for law enforcement",
         "Real-time remote biometric identification in publicly accessible spaces for law "
         "enforcement, outside the narrow listed exceptions."),
    # ------------------------------------------------------------------ Annex III: high-risk
    _cat("H_1a", "high_risk", "Annex III(1)(a)", "Remote biometric identification",
         "Remote biometric identification systems (not mere verification of a claimed identity)."),
    _cat("H_1b", "high_risk", "Annex III(1)(b)", "Biometric categorization by sensitive or protected attributes",
         "Biometric categorization by sensitive or protected attributes that is not already prohibited.",
         also=["Art. 50(3)"]),
    _cat("H_1c", "high_risk", "Annex III(1)(c)", "Emotion recognition",
         "Emotion recognition systems (outside the workplace and education settings that are prohibited).",
         also=["Art. 50(3)"]),
    _cat("H_2", "high_risk", "Annex III(2)", "Critical infrastructure safety components",
         "Safety components in the management and operation of critical digital infrastructure, road "
         "traffic, or the supply of water, gas, heating or electricity."),
    _cat("H_3a", "high_risk", "Annex III(3)(a)", "Education admission",
         "Determining access or admission, or assigning people to education and training institutions."),
    _cat("H_3b", "high_risk", "Annex III(3)(b)", "Evaluating learning outcomes",
         "Evaluating learning outcomes, including when used to steer the learning process."),
    _cat("H_3c", "high_risk", "Annex III(3)(c)", "Education level assessment",
         "Assessing the appropriate level of education a person will receive or can access."),
    _cat("H_3d", "high_risk", "Annex III(3)(d)", "Exam proctoring",
         "Monitoring and detecting prohibited behavior of students during tests."),
    _cat("H_4a", "high_risk", "Annex III(4)(a)", "Recruitment and selection",
         "Recruitment or selection: targeted job ads, filtering applications, evaluating candidates."),
    _cat("H_4b", "high_risk", "Annex III(4)(b)", "Employment decisions and monitoring",
         "Decisions on work terms, promotion, termination, task allocation based on behavior or traits, "
         "and monitoring or evaluating workers."),
    _cat("H_5a", "high_risk", "Annex III(5)(a)", "Public benefits eligibility",
         "Evaluating eligibility for essential public benefits and services, and granting, reducing, "
         "revoking or reclaiming them."),
    _cat("H_5b", "high_risk", "Annex III(5)(b)", "Credit scoring",
         "Evaluating creditworthiness or establishing credit scores of individuals (fraud detection excepted)."),
    _cat("H_5c", "high_risk", "Annex III(5)(c)", "Life and health insurance",
         "Risk assessment and pricing for individuals in life and health insurance."),
    _cat("H_5d", "high_risk", "Annex III(5)(d)", "Emergency call triage and dispatch",
         "Classifying emergency calls, prioritizing dispatch of emergency services, and emergency patient triage."),
    _cat("H_6a", "high_risk", "Annex III(6)(a)", "Victim risk assessment (law enforcement)",
         "Law enforcement assessing a person's risk of becoming a victim of criminal offences."),
    _cat("H_6b", "high_risk", "Annex III(6)(b)", "Polygraphs (law enforcement)",
         "Polygraphs and similar tools used by law enforcement."),
    _cat("H_6c", "high_risk", "Annex III(6)(c)", "Evidence reliability",
         "Evaluating the reliability of evidence in criminal investigation or prosecution."),
    _cat("H_6d", "high_risk", "Annex III(6)(d)", "Offending and re-offending risk",
         "Assessing a person's risk of offending or re-offending (not solely by profiling), or assessing "
         "personality traits or past criminal behavior."),
    _cat("H_6e", "high_risk", "Annex III(6)(e)", "Profiling in criminal investigations",
         "Profiling of individuals in the detection, investigation or prosecution of criminal offences."),
    _cat("H_7a", "high_risk", "Annex III(7)(a)", "Polygraphs (migration and border)",
         "Polygraphs and similar tools used by public authorities in migration, asylum and border control."),
    _cat("H_7b", "high_risk", "Annex III(7)(b)", "Migration risk assessment",
         "Assessing security, irregular-migration or health risks posed by a person entering or seeking to enter."),
    _cat("H_7c", "high_risk", "Annex III(7)(c)", "Asylum, visa and residence applications",
         "Assisting examination of asylum, visa and residence-permit applications, including evidence reliability."),
    _cat("H_7d", "high_risk", "Annex III(7)(d)", "Identifying people in migration and border control",
         "Detecting, recognizing or identifying people in migration, asylum and border control (not travel-document checks)."),
    _cat("H_8a", "high_risk", "Annex III(8)(a)", "Judicial decision support",
         "Assisting a judicial authority in researching and interpreting facts and law and applying the law to facts."),
    _cat("H_8b", "high_risk", "Annex III(8)(b)", "Influencing elections and voting",
         "Influencing the outcome of an election or referendum or the voting behavior of people."),
    _cat("H_61", "high_risk", "Art. 6(1)", "Product safety component under Annex I legislation",
         "A safety component of, or itself, a product covered by Annex I EU harmonization legislation that "
         "requires third-party conformity assessment."),
    # ------------------------------------------------------------------ Art. 50: transparency
    _cat("L_1", "limited_transparency", "Art. 50(1)", "AI interacting directly with people",
         "AI systems intended to interact directly with people (chatbots, voice agents): people must be told "
         "they are dealing with AI unless obvious."),
    _cat("L_2", "limited_transparency", "Art. 50(2)", "Synthetic content generation",
         "Providers of AI systems that generate synthetic audio, image, video or text must mark outputs in a "
         "machine-readable way."),
    _cat("L_4a", "limited_transparency", "Art. 50(4)", "Deepfakes",
         "Deployers of AI that generates or manipulates image, audio or video forming a deepfake must disclose it."),
    _cat("L_4b", "limited_transparency", "Art. 50(4)", "AI-generated public-interest text",
         "Deployers of AI that generates text published to inform the public on matters of public interest "
         "must disclose it, unless there is human editorial review."),
    # ------------------------------------------------------------------ minimal
    _cat("M", "minimal", None, "Minimal risk",
         "Anything outside Art. 5, Art. 6 with Annex I or III, and Art. 50 (spam filters, forecasting, "
         "log anomaly detection, fraud detection, etc.)."),
]

BY_ID = {c["id"]: c for c in TAXONOMY}


def provisions_for(cid: str) -> list[str]:
    c = BY_ID[cid]
    return ([c["citation"]] if c["citation"] else []) + list(c["also"])


# Canonical provision strings, in a stable order.
VALID_PROVISIONS: list[str] = []
for _c in TAXONOMY:
    for _p in provisions_for(_c["id"]):
        if _p not in VALID_PROVISIONS:
            VALID_PROVISIONS.append(_p)

_ORDER = {p: i for i, p in enumerate(VALID_PROVISIONS)}


def _squash(s: str) -> str:
    return re.sub(r"[\s.]+", "", s).lower()


_CANON = {_squash(p): p for p in VALID_PROVISIONS}


def normalize_provision(s: str) -> str | None:
    """Return the canonical provision string, or None if it is not in the taxonomy."""
    if not isinstance(s, str):
        return None
    return _CANON.get(_squash(s))


def sort_provisions(provs: list[str]) -> list[str]:
    return sorted(set(provs), key=lambda p: _ORDER.get(p, 10_000))


def label_for(cid: str) -> dict:
    c = BY_ID[cid]
    return {"tier": c["tier"], "provisions": sort_provisions(provisions_for(cid))}
