# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""DRAFT gold test set. NOT VERIFIED.

These items were drafted with AI assistance and carry provisional labels. A legal expert
must review every row before any number is published (see docs/LABELING_GUIDE.md).
Rows are written with status "unverified"; evaluate.py prints a warning until every row
in data/gold.jsonl is "verified".

Run:  python -m aiact_tier.gold_draft --out data/gold_draft.jsonl --sheet eval/gold_review_sheet.csv
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from .taxonomy import BY_ID, label_for

# (category id, text, difficulty, note)
GOLD = [
    ("P_a", "A mobile game that flashes sub-threshold imagery and uses covert persuasion loops so players spend far more than planned, which has already led to serious debts.", "easy", ""),
    ("P_a", "Smart-TV firmware that inserts imperceptible audio tones to steer viewers toward ordering a sponsor's product without them realizing they were influenced.", "easy", ""),
    ("P_b", "A learning toy whose AI praises toddlers for climbing onto furniture and nudges them toward unsafe stunts because it knows they cannot judge danger.", "easy", ""),
    ("P_b", "A marketing model aimed at people living on welfare that detects money stress and pushes high-interest payday offers to induce decisions that harm them.", "easy", ""),
    ("P_c", "A municipal program that combines purchase history, online posts and associations of residents into one civic reliability rating, which then limits their access to kindergarten places and public libraries.", "easy", ""),
    ("P_c", "A platform scoring individuals' general social behavior to decide which services they may use, applied across unrelated areas of their life.", "medium", ""),
    ("P_d", "A predictive tool used by a regional police agency that labels residents as likely future offenders purely from their personality assessments and demographic features.", "easy", ""),
    ("P_e", "We built a crawler that downloads faces from public photo sites and security camera feeds en masse, with no specific target, to grow our recognition index.", "easy", ""),
    ("P_f", "A workplace analytics suite that reads facial expressions from laptop cameras to infer whether employees feel frustrated or bored and reports the results to managers.", "easy", ""),
    ("P_f", "Software installed in a school that infers pupils' emotions from their faces during lessons to produce engagement ratings for teachers.", "easy", ""),
    ("P_g", "A face-analysis API that claims to determine a person's religion and sexual orientation from a photo.", "easy", ""),
    ("P_h", "A national police pilot that runs live face recognition on CCTV in a public square to identify and detain wanted people as they walk past.", "medium", "Art. 5(1)(h) has narrow exceptions requiring prior authorization. Expert to confirm default label."),
    ("H_1a", "A forensic platform used by a private security firm to identify unknown individuals in stored CCTV clips by comparing faces to a large reference gallery.", "easy", ""),
    ("H_1a", "A system that identifies a speaker from a recorded call by searching a database of voiceprints, rather than checking a claimed identity.", "medium", ""),
    ("H_1b", "A system for a transit agency that infers whether passengers have a disability from video of how they move, to route them to separate queues.", "medium", "Annex III(1)(b) scope (what counts as sensitive or protected) is debated. Expert to confirm."),
    ("H_1b", "An analytics tool that assigns shoppers to categories by inferred sex and age from facial images.", "hard", "Is age or sex a sensitive or protected attribute under Annex III(1)(b)? Expert to confirm."),
    ("H_1c", "A customer-service kiosk in a bank lobby that reads facial expressions to infer customers' emotions and adjusts which offers it shows.", "medium", ""),
    ("H_1c", "An in-car system for a car-rental firm that infers renters' emotions from their voice to recommend upsells.", "medium", ""),
    ("H_2", "AI software acting as a safety component that controls pressure valves and shut-offs in a city gas distribution network.", "easy", ""),
    ("H_2", "A machine-learning module that manages traffic lights and incident response on a national highway system as a safety function.", "medium", ""),
    ("H_3a", "A scholarship and admissions AI that scores applications and decides which candidates a business school accepts.", "easy", ""),
    ("H_3a", "A system allocating children to public primary schools based on automated analysis of their files.", "easy", ""),
    ("H_3b", "An automated marker that grades students' written exams and records their final results.", "easy", ""),
    ("H_3b", "A platform that evaluates students' learning progress and steers which lessons they are given next.", "medium", ""),
    ("H_3c", "A tool that determines which education stream a teenager is permitted to enter based on a predicted ability score.", "medium", ""),
    ("H_3d", "Proctoring software that watches students through webcams during exams and raises alerts for suspected cheating.", "easy", ""),
    ("H_4a", "A tool that screens incoming CVs, discards weaker ones, and ranks the remaining applicants for the hiring manager.", "easy", ""),
    ("H_4a", "A service that decides which people see a job advertisement based on predicted suitability.", "medium", ""),
    ("H_4b", "An algorithm that tracks couriers' delivery speed and behavior and uses it to assign shifts, bonuses and contract renewals.", "easy", ""),
    ("H_4b", "Software that evaluates employees' work performance from activity logs and informs promotion and termination decisions.", "easy", ""),
    ("H_5a", "A social-security agency model that decides whether applicants are entitled to disability allowance and recalculates existing payments.", "easy", ""),
    ("H_5a", "A municipal system that determines whether residents keep their public healthcare coverage.", "medium", ""),
    ("H_5b", "A fintech model that determines individual consumers' credit scores and approves or declines personal loans.", "easy", ""),
    ("H_5b", "An underwriting engine that evaluates whether private persons can afford a car loan.", "medium", ""),
    ("H_5c", "An insurer's AI that estimates a customer's health risk and sets the premium for their private health policy.", "easy", ""),
    ("H_5c", "A life-insurance pricing model that uses applicants' age, habits and records to price cover.", "easy", ""),
    ("H_5d", "A control-room tool that triages incoming 112 calls and ranks which ones need an ambulance first.", "easy", ""),
    ("H_5d", "A hospital system that prioritizes arriving emergency patients for treatment.", "medium", ""),
    ("H_6a", "A law-enforcement application that estimates which individuals are most likely to be victims of violent crime so that police can prioritize outreach.", "medium", ""),
    ("H_6b", "A device used by investigators to detect lies in suspects' speech and body signals during police questioning.", "easy", ""),
    ("H_6c", "A tool used by a prosecution service to assess how trustworthy photographic and digital exhibits are in criminal investigations.", "medium", ""),
    ("H_6d", "A prison-service system that predicts a convict's chance of reoffending after release using their offence history and conduct records.", "medium", "Not solely profiling (uses objective records), so high_risk rather than prohibited. Expert to confirm."),
    ("H_6e", "Software that builds profiles of individuals connected to an organized-crime case by merging their communications and financial records.", "medium", ""),
    ("H_7a", "A border authority's tool that judges whether a traveler is being deceptive during an entry interview.", "easy", ""),
    ("H_7b", "A system that rates how likely arriving visa-exempt travelers are to overstay or pose a security threat, used by border police.", "easy", ""),
    ("H_7c", "An AI used by an immigration office to assess the credibility of asylum seekers' statements and recommend whether to grant protection.", "easy", ""),
    ("H_7d", "Cameras and software at a land border that identify individual travelers by matching their faces against watchlists.", "hard", "Could also be argued under Art. 5(1)(h) if real time and law enforcement. Expert to confirm."),
    ("H_8a", "A judicial research assistant that analyzes the facts of a dispute and suggests which legal provisions apply, used by judges.", "easy", ""),
    ("H_8b", "A voter-persuasion engine that tailors political ads to individual citizens to alter how they will vote.", "easy", ""),
    ("H_61", "A neural-network braking safety function embedded in a passenger lift, which must pass third-party conformity assessment under EU product legislation.", "medium", ""),
    ("H_61", "An AI diagnostic imaging module that is itself a medical device needing notified-body certification.", "medium", ""),
    ("L_1", "A virtual agent on a bank's website that chats with customers about opening accounts.", "easy", ""),
    ("L_1", "An AI phone agent that answers a restaurant's calls and takes reservations.", "easy", ""),
    ("L_2", "A platform that produces synthetic photographs from text prompts for anyone to download.", "easy", ""),
    ("L_2", "A text-to-speech provider that outputs lifelike synthetic voices through an API.", "easy", ""),
    ("L_4a", "A creative agency that uses AI to produce realistic footage of a real, existing street festival that never took place, for a public campaign.", "medium", ""),
    ("L_4a", "A broadcaster that uses AI to make a realistic clip of a real presenter saying words they never spoke.", "easy", ""),
    ("L_4b", "A website that auto-publishes AI-generated explainers about new tax laws for the general public with no editor checking them.", "medium", ""),
    ("M", "A spam filter that sorts incoming email on a company mail server.", "easy", ""),
    ("M", "A tool that predicts next month's demand for each product in a grocery chain.", "easy", ""),
    ("M", "A model that reads totals and dates from scanned supplier invoices.", "easy", ""),
    ("M", "A service that detects unusual patterns in server logs to alert IT staff.", "easy", ""),
    ("M", "A recommendation engine suggesting songs to listeners of a music app.", "easy", ""),
    ("M", "A model that spots card-payment fraud in real time for a payments processor.", "hard", "Fraud detection is expressly carved out of Annex III(5)(b). Expert to confirm minimal."),
    ("M", "A vision system detecting scratches on glass bottles on a production line.", "easy", ""),
    ("M", "A scheduler that optimizes delivery van routes to cut fuel use.", "easy", ""),
    ("M", "An algorithm that forecasts wind-farm output for the next day.", "easy", ""),
    ("M", "An app that groups holiday photos by place and date.", "easy", ""),
    # ---- low-keyword items: same legal substance, plain wording, to defeat keyword matching
    ("H_4a", "The platform ingests every inbound submission for an open vacancy and surfaces only the best-scoring tenth to the people who will make the offer.", "medium", "Low-keyword rewrite."),
    ("H_5b", "A model that estimates the probability that a private individual will miss repayments and sets the interest rate they are offered.", "medium", "Low-keyword rewrite."),
    ("H_3b", "An engine that reads pupils' written answers, assigns each a mark, and sends those marks straight to the official transcript.", "medium", "Low-keyword rewrite."),
    ("H_5a", "A tool that decides whether a household still meets the income test for monthly state assistance and cuts payments when it concludes it does not.", "medium", "Low-keyword rewrite."),
    ("H_6e", "Software that stitches together call records, bank movements and travel history of a named person to produce a behavioral profile for detectives.", "medium", "Low-keyword rewrite."),
    ("P_c", "A scheme that gives each inhabitant a standing derived from their online conduct, friendships and purchases, then sorts them into tiers that decide who can book appointments at any public office.", "medium", "Low-keyword rewrite."),
    ("P_f", "Cameras above call-center desks estimate how irritated or cheerful each agent looks and sounds, and the weekly ranking feeds into bonuses.", "medium", "Low-keyword rewrite."),
    ("L_1", "An automated agent greets visitors on an airline's site, answers questions about baggage, and rebooks flights through natural conversation.", "medium", "Low-keyword rewrite."),
    ("L_2", "A service that turns a short written prompt into a lifelike clip with moving people and a soundtrack, available to anyone with an account.", "medium", "Low-keyword rewrite."),
    ("M", "A model that decides the order in which pallets are loaded onto trucks to minimize unloading time.", "medium", "Near-miss negative."),
    ("M", "A system that reads gauge photos from a plant's meters and logs the values in a database.", "medium", "Near-miss negative."),
    ("M", "A recommender that suggests which recipe to cook based on what is in the fridge.", "easy", ""),
    ("H_2", "A learning-based controller that decides in real time when to open or isolate sections of a district heating network to prevent failures.", "medium", "Low-keyword rewrite."),
    ("H_7c", "A tool that reads the evidence submitted with residence permit requests and tells the case officer how likely the claim is to be genuine.", "medium", "Low-keyword rewrite."),
    ("H_8a", "A drafting aid for magistrates that retrieves relevant precedents and proposes how the statute fits the facts of the file.", "medium", "Low-keyword rewrite."),
    ("H_5d", "A system that listens to a caller's description and decides how fast a crew is sent and which unit it will be.", "medium", "Low-keyword rewrite."),
    ("H_1a", "A tool that sifts through hours of public-event footage and names the people in it by matching them to a gallery of known faces.", "medium", "Low-keyword rewrite."),
    ("P_g", "A pipeline that guesses from portrait photos which political party a person votes for.", "medium", "Low-keyword rewrite."),
]

# (id hint, text, tier, provisions, difficulty, note)
GOLD_EXPLICIT = [
    ("combo", "A hiring chatbot that interviews applicants through chat and ranks them for recruiters.", "high_risk", ["Annex III(4)(a)", "Art. 50(1)"], "medium", ""),
    ("combo", "A loan assistant that chats with customers on a website and calculates their credit score.", "high_risk", ["Annex III(5)(b)", "Art. 50(1)"], "medium", ""),
    ("combo", "A virtual teaching assistant that talks with pupils and also marks their final assessments.", "high_risk", ["Annex III(3)(b)", "Art. 50(1)"], "medium", ""),
    ("hard", "An automatic shift planner that assigns rota slots based only on staff availability declared in advance.", "minimal", [], "hard", "Is this task allocation 'based on individual behavior or personal traits' (Annex III(4)(b))? Availability is arguably neither. Expert to confirm."),
    ("hard", "A recruitment-interview tool that infers candidates' emotions from video to score them.", "prohibited", ["Art. 5(1)(f)"], "hard", "Depends on whether recruitment counts as 'workplace' for Art. 5(1)(f). Expert to confirm against Commission guidelines."),
    ("hard", "An exam proctoring tool that also infers students' emotions during tests.", "prohibited", ["Art. 5(1)(f)"], "medium", ""),
    ("hard", "A hospital tool that reads patients' voices to detect distress and alerts nurses.", "high_risk", ["Annex III(1)(c)", "Art. 50(3)"], "hard", "Patients are not workplace or education; check any medical-device overlap. Expert to confirm."),
]


def build_rows() -> list[dict]:
    rows = []
    n = 0
    for cid, text, diff, note in GOLD:
        n += 1
        lab = label_for(cid)
        rows.append({"id": f"G-{n:03d}", "text": text, **lab, "category": cid,
                     "difficulty": diff, "note": note, "status": "unverified"})
    for hint, text, tier, provs, diff, note in GOLD_EXPLICIT:
        n += 1
        rows.append({"id": f"G-{n:03d}", "text": text, "tier": tier, "provisions": provs,
                     "category": hint, "difficulty": diff, "note": note, "status": "unverified"})
    for r in rows:
        assert r["category"] in BY_ID or r["category"] in ("combo", "hard")
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="data/gold_draft.jsonl")
    ap.add_argument("--sheet", default="eval/gold_review_sheet.csv")
    a = ap.parse_args(argv)
    rows = build_rows()
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    with open(a.out, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    Path(a.sheet).parent.mkdir(parents=True, exist_ok=True)
    with open(a.sheet, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id", "system_description", "proposed_tier", "proposed_provisions", "difficulty",
                    "drafter_note", "reviewer1_tier", "reviewer1_provisions", "reviewer2_tier",
                    "reviewer2_provisions", "final_tier", "final_provisions", "comments"])
        for r in rows:
            w.writerow([r["id"], r["text"], r["tier"], "; ".join(r["provisions"]), r["difficulty"],
                        r["note"], "", "", "", "", "", "", ""])
    print(f"wrote {len(rows)} draft gold rows -> {a.out} and {a.sheet}")


if __name__ == "__main__":
    main()
