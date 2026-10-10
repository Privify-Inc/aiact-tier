# Branding guide: free for the community, signed by Privify

Positioning line: **"A free contribution from Privify Inc. to the AI governance community."**
Open source with a visible author is normal and builds trust. The brand earns attention by being
useful and honest, not by being forced on users.

## Where the Privify name appears (checklist)

- [x] Author line and SPDX line at the top of every source file
- [x] `NOTICE`, `CITATION.cff` (so academic and industry citations name Privify Inc.)
- [x] README banner and "About Privify" section
- [x] Model card: "Developed and open-sourced by Privify Inc."
- [x] Authorship credit (Bhaskar Tallamraju) in file headers, NOTICE, CITATION.cff and README
- [x] Qwen3-4B credited in NOTICE, README, model card, CITATION.cff and the training script
- [x] Decision: no "powered by" or promotional lines inside code, the demo UI, or model outputs
- [ ] Model name and repo name: `privify/aiact-tier-4b-v0.1` (confirm with counsel, Q3)
- [ ] GitHub organization and Hugging Face organization pages with logo, link to privify.io
- [ ] Logo in README header and model card (add the Privify logo files under `assets/`)
- [ ] Social preview image for GitHub, launch graphic for X and LinkedIn
- [ ] Release notes, blog post, launch posts (drafted in `docs/LAUNCH_POSTS.md`)
- [ ] Commits and releases made from a Privify organization account

## What Apache 2.0 does and does not give you

- **Does:** anyone who redistributes the code or weights must keep the copyright notices and the
  `NOTICE` file, so "Privify Inc." travels with every copy and fork.
- **Does not:** force anyone to advertise Privify, or to say "powered by Privify".
- **Trademark:** the license does not grant the Privify name or logo. Forks can reuse the code but
  cannot call their product "Privify". Counsel should confirm this given the pending PRIVIFY filing.

## Do

- Say "developed and open-sourced by Privify Inc." and "fine-tuned from Qwen3-4B". Credit the base
  model plainly. Apache 2.0 requires it, and it protects our credibility.
- Add a polite citation request (in `CITATION.cff` and the README).
- Keep one clear link to privify.io, in the README and model card, not on every line.

## Do not

- Put brand text, ads, or hidden watermarks into the model's outputs. It annoys users, breaks
  downstream parsing, and reads as deceptive.
- Add a license clause that forces "powered by" credit in advertising. That makes it no longer open
  source, clashes with other licenses, and invites community backlash. If you want a firm
  restriction, call it "open weights" and ask counsel to draft it, knowing adoption will drop.
- Say "compliant", "certified" or quote accuracy before the verified benchmark exists.
- Claim to have built the base model.
