# SPDX-License-Identifier: Apache-2.0
# Author: Bhaskar Tallamraju, Privify Inc.
"""Hand-written seed descriptions used to build synthetic training data.

PROVENANCE: drafted with AI assistance (Anthropic's Claude) on 2026-10-07 from the
public text of the EU AI Act. All systems described are fictional. These seeds are
NOT yet reviewed by a legal expert; review before release (see docs/LABELING_GUIDE.md).

Each category has 3 seeds. They must never overlap with the gold test set
(tests/test_pipeline.py enforces a similarity limit).
"""

SEEDS = {
    # ---------------------------------------------------------------- prohibited
    "P_a": [
        "An app that embeds imperceptible audio and visual cues in video streams to push users into impulse purchases they would not otherwise make, tuned to bypass their conscious awareness.",
        "A chatbot for a gambling site that uses deceptive psychological tricks, adapted per user in real time, to keep problem gamblers betting beyond their limits.",
        "A shopping-cart plug-in that uses hidden dark-pattern persuasion engineered below conscious awareness to make shoppers pay far more than they intended, causing significant financial harm.",
    ],
    "P_b": [
        "A talking toy that encourages young children to attempt risky physical challenges by exploiting their immaturity and credulity.",
        "A promotion engine that targets people in financial distress with predatory loan offers, using their poverty and desperation to push harmful borrowing decisions.",
        "A companion app tuned to manipulate adults with cognitive disabilities into handing over money by exploiting their impaired judgment.",
    ],
    "P_c": [
        "A city-wide platform that assigns every resident a trust score from social media activity, friendships and shopping, and uses it to deny access to housing and public services in unrelated contexts.",
        "A system that rates citizens' general behavior across many data sources and lowers their access to public transport when their score drops.",
        "A company-wide score that evaluates employees' off-duty social conduct and personal relationships and applies detrimental treatment unrelated to the original data.",
    ],
    "P_d": [
        "A police tool that predicts which individuals will commit a crime in the future based only on their personality traits and demographic profile, with no objective facts linking them to criminal activity.",
        "A system that ranks teenagers by predicted likelihood of becoming offenders using only neighborhood, family background and psychological profiling.",
        "Software that flags people as future violent offenders purely from automated profiling of their characteristics, to guide stops and surveillance.",
    ],
    "P_e": [
        "A startup that crawls social media and public websites at scale to harvest faces and build a searchable facial recognition database.",
        "A tool that continuously pulls faces out of CCTV footage across a city, without targeting anyone, to expand a recognition database.",
        "A service that scrapes millions of profile photos from the internet indiscriminately to train and populate a face-matching index.",
    ],
    "P_f": [
        "A call-center tool that infers agents' emotions from voice and facial expression to rank and discipline them.",
        "A classroom camera system that infers students' emotional states from facial expressions to grade teachers and pupils.",
        "An office badge-and-camera system that infers employees' moods during the working day and flags unhappy staff to HR.",
    ],
    "P_g": [
        "A camera analytics product that infers people's sexual orientation from facial features.",
        "A system that deduces visitors' religion from their facial images to tailor security checks.",
        "A tool that infers a person's race and political leanings from voice and face data to segment audiences.",
    ],
    "P_h": [
        "A police system that scans the faces of passersby on a busy street in real time and matches them against a watchlist to make arrests on the spot.",
        "A live facial recognition network at a public stadium entrance, run by law enforcement, that identifies fans against a database as they walk in.",
        "Police body cameras that run live face matching on everyone in a public square to identify persons of interest immediately.",
    ],
    # ---------------------------------------------------------------- high risk: Annex III
    "H_1a": [
        "A post-event forensic tool that matches faces in recorded footage against a database to identify unknown people for a private security company.",
        "A system that identifies unknown individuals from voice recordings by searching a stored voiceprint database, not just confirming a claimed identity.",
        "A retail chain's system that identifies shoppers from camera feeds against a database of banned customers' faces.",
    ],
    "H_1b": [
        "A tool that categorizes people by inferred disability status from gait and facial video to route them to different services.",
        "A system that sorts people by inferred gender from voice and face for targeted advertising.",
        "An app that infers users' age group and gender from facial biometrics to segment them into categories.",
    ],
    "H_1c": [
        "A car-dealership kiosk that infers customers' emotions from facial expressions to adapt its sales pitch.",
        "A telehealth platform feature that infers patients' emotional state from voice and video to advise clinicians.",
        "A museum visitor-feedback system that detects visitors' emotions from facial expressions to rate exhibits.",
    ],
    "H_2": [
        "An AI controller acting as a safety component that balances load and trips protection on a regional electricity grid.",
        "A system that regulates chlorine dosing and pressure as a safety component of a municipal drinking-water network.",
        "An AI safety component managing traffic-signal timing and emergency stops on a motorway network.",
    ],
    "H_3a": [
        "A university tool that ranks applicants and decides who is admitted to its master's programs.",
        "A platform that assigns pupils to secondary schools based on automated scoring of their records.",
        "An AI that screens applications to a vocational training academy and rejects candidates below a threshold.",
    ],
    "H_3b": [
        "An AI grader that scores final exam essays and sets students' official marks.",
        "A system that evaluates pupils' learning outcomes and automatically adjusts their course progression.",
        "A tool that assesses coding assignments and determines whether students pass the module.",
    ],
    "H_3c": [
        "A system that decides which educational track a student may enter based on predicted aptitude.",
        "An AI that assesses new pupils and decides what education level they are placed in.",
        "A tool that determines which advanced courses a learner is allowed to access, based on an automated ability assessment.",
    ],
    "H_3d": [
        "An online exam proctoring system that analyzes webcam video to flag students suspected of cheating.",
        "A tool that monitors students' screens and eye movements during tests and detects prohibited behavior.",
        "An AI that listens to exam rooms and flags students who appear to be exchanging answers.",
    ],
    "H_4a": [
        "An applicant tracking system that automatically filters and ranks resumes and rejects low-scoring applicants.",
        "A tool that delivers targeted job advertisements to selected groups of people by predicted fit.",
        "A video-interview analysis AI that scores candidates' answers (language and content) and recommends who to shortlist.",
    ],
    "H_4b": [
        "A system that scores warehouse workers' productivity from sensor data and recommends promotions and dismissals.",
        "An AI that allocates tasks to gig drivers based on their individual behavior profiles and ratings.",
        "A tool that monitors employees' performance and conduct and feeds decisions about contract termination.",
    ],
    "H_5a": [
        "A government system that decides whether citizens qualify for unemployment benefits.",
        "An agency tool that evaluates eligibility for public healthcare services and reduces or revokes entitlements.",
        "An AI that determines whether housing-assistance recipients must repay benefits.",
    ],
    "H_5b": [
        "A bank's model that computes credit scores for loan applicants and accepts or rejects them.",
        "A buy-now-pay-later provider's system that evaluates consumers' creditworthiness at checkout.",
        "A mortgage scoring engine that rates private individuals' ability to repay.",
    ],
    "H_5c": [
        "A health-insurance system that assesses applicants' risk profiles and sets individual premiums.",
        "A life-insurance underwriting AI that prices policies from applicants' medical and lifestyle data.",
        "A tool that evaluates insurance risk for individual customers and decides coverage terms for life policies.",
    ],
    "H_5d": [
        "A system that classifies emergency calls and decides which ambulances to dispatch first.",
        "An AI that prioritizes dispatch of fire engines and police units based on analysis of incoming emergency calls.",
        "A hospital emergency-department triage tool that decides the urgency order of patients.",
    ],
    "H_6a": [
        "A police system that scores a person's risk of becoming a victim of stalking or domestic violence to prioritize protection.",
        "A law-enforcement tool that assesses the likelihood that individuals will become victims of crime in a region.",
        "A police AI that predicts which residents are most at risk of being victimized, to allocate protection resources.",
    ],
    "H_6b": [
        "A police interview tool that judges whether a suspect is lying from voice and physiological signals.",
        "A deception-detection system used by officers during questioning.",
        "A lie detector AI used by a police department.",
    ],
    "H_6c": [
        "An AI used by prosecutors that assesses how reliable digital evidence is in a criminal case.",
        "A police tool that scores the reliability of witness statements and exhibits during investigations.",
        "An AI system that evaluates the credibility of evidence for criminal prosecution.",
    ],
    "H_6d": [
        "A probation-service model that estimates re-offending risk using criminal records and objective case facts.",
        "A police tool that assesses a suspect's likelihood of re-offending using past convictions and conduct, with analysts reviewing the result.",
        "A system that assesses the past criminal behavior of groups to inform policing decisions.",
    ],
    "H_6e": [
        "A police analytics tool that profiles individuals linked to a fraud investigation by combining their records and communications.",
        "An AI that profiles suspects in a drug-trafficking investigation from phone and financial data.",
        "A prosecution support system that builds profiles of persons of interest from linked databases.",
    ],
    "H_7a": [
        "A border-control AI that assesses travelers' truthfulness from their responses and expressions during interviews.",
        "A lie detection tool used in asylum interviews.",
        "A border officer's tool that checks whether a visa applicant is lying.",
    ],
    "H_7b": [
        "A border system that scores travelers' risk of irregular migration before entry.",
        "A tool that assesses the security risk of visa applicants for a border agency.",
        "An AI that evaluates the health risk posed by arriving passengers for a migration authority.",
    ],
    "H_7c": [
        "An asylum-agency system that assesses the credibility of applicants' claims and recommends decisions.",
        "A visa-processing AI that evaluates applicants' eligibility and the reliability of their evidence.",
        "A tool that helps officers decide residence permit applications and appeals.",
    ],
    "H_7d": [
        "A border-crossing system that identifies unknown travelers by matching faces against a database.",
        "An AI that detects and recognizes people in camera footage along a border to identify them.",
        "A system at an asylum center that identifies individuals from biometrics to match against records.",
    ],
    "H_8a": [
        "A court tool that researches case law and suggests how the law applies to the facts of a pending case.",
        "An AI assistant for judges that interprets facts and applies legal provisions to draft decisions.",
        "An online arbitration platform's AI that applies legal rules to facts to propose rulings in disputes.",
    ],
    "H_8b": [
        "A campaign system that generates personalized messages designed to sway individual voters' choices in an upcoming election.",
        "An AI that targets undecided voters with tailored content to change how they vote in a referendum.",
        "A platform that micro-targets voters with persuasion content to influence turnout and choice.",
    ],
    "H_61": [
        "An AI-based safety component in a lift that decides when to brake, subject to third-party conformity assessment under EU lift and machinery rules.",
        "Software in a diagnostic imaging product that is itself a regulated medical device requiring notified-body assessment.",
        "An AI collision-avoidance safety function in an industrial machine covered by EU machinery law and requiring third-party assessment.",
    ],
    # ---------------------------------------------------------------- transparency (Art. 50)
    "L_1": [
        "A customer-support chatbot on a telecom website that answers billing questions in a chat window.",
        "A voice bot that answers a pharmacy's phone line and books appointments.",
        "An AI sales assistant that chats with website visitors about products.",
    ],
    "L_2": [
        "A text-to-image service that generates realistic images from prompts for general users.",
        "A voice-cloning and speech-synthesis API that produces realistic synthetic audio.",
        "A generative video platform that creates photorealistic clips from text descriptions.",
    ],
    "L_4a": [
        "A film studio uses AI face-swapping to put a real actor's likeness onto a stunt performer in a feature film.",
        "A brand deploys an AI tool to produce a realistic video of a real city landmark scene that never happened, for a public advertising campaign.",
        "A company publishes AI-synthesized audio of its CEO's voice reading a message the CEO never recorded.",
    ],
    "L_4b": [
        "A news website that publishes AI-written articles on local elections and public health without human editorial review.",
        "A publisher that auto-generates and posts AI-written reports about government policy to inform the public, with no editorial control.",
        "A portal that posts machine-generated summaries of parliamentary debates for citizens, without human review.",
    ],
    # ---------------------------------------------------------------- minimal
    "M": [
        "A tool that tags customer feedback comments as positive, neutral or negative for a marketing report.",
        "A demand-forecasting model for a supermarket's inventory planning.",
        "An OCR system that extracts fields from supplier invoices.",
        "An anomaly detector on server logs that alerts IT operations staff.",
        "A music recommendation engine for a streaming service.",
        "A predictive-maintenance model for office building HVAC units.",
        "A crop-yield prediction model that uses satellite imagery for farms.",
        "A fraud-detection model that flags suspicious card payment transactions.",
        "A visual inspection system that detects defects in plastic bottles on a factory line.",
        "A warehouse model that decides where to shelve products to shorten picking time.",
        "A model that forecasts energy use for data center cooling.",
        "A camera app feature that automatically sharpens night photos.",
        # near-miss negatives: topics adjacent to high-risk areas but outside them
        "A timetable generator that schedules classrooms and teachers for a school, without evaluating any student.",
        "A payroll tool that computes salaries and tax deductions from fixed rules and timesheets.",
        "A model that forecasts hospital bed occupancy at ward level for the next two weeks.",
        "A recommender that suggests library books to university students from their borrowing history.",
        "A model that predicts which website visitors are likely to click an ad banner, for an online publisher.",
        "A spell checker and grammar tool built into a word processor.",
        "A tool that clusters customer support tickets by topic for the support team's weekly report.",
        "A forecasting model for electricity prices used by an energy trading desk.",
        "A sales forecasting model that predicts a company's quarterly revenue.",
        "A weather-based irrigation scheduler for a commercial farm.",
        "An image classifier that sorts scanned documents by type, such as invoice, contract or letter.",
    ],
}

# Seeds with explicit multi-provision labels: (text, tier, provisions)
COMBOS = [
    ("A recruitment chatbot that talks with candidates in a chat window, collects their answers and ranks them for recruiters.",
     "high_risk", ["Annex III(4)(a)", "Art. 50(1)"]),
    ("A bank's customer-facing assistant that chats with applicants and computes their credit score to approve or decline loans.",
     "high_risk", ["Annex III(5)(b)", "Art. 50(1)"]),
    ("An AI tutor chatbot that talks to students and also grades their final exams to set official marks.",
     "high_risk", ["Annex III(3)(b)", "Art. 50(1)"]),
    ("A conversational triage assistant that chats with callers and ranks which emergencies get an ambulance first.",
     "high_risk", ["Annex III(5)(d)", "Art. 50(1)"]),
]
