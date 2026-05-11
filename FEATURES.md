# Fe+ Iron Balance Tool — Feature & Launch Tracker

Last updated: 10 May 2026

> **Note for Claude Code:** Read this file at the start of each session for project context. Update task status (change `[ ]` to `[x]`) when tasks are completed during a session.

---

## Phase 0 — Dev Now

- [x] Fix Stripe URLs and test full purchase flow
- [x] Fix tooltip event listeners — all 7 working
- [x] Add 3.6 µg/L/month tooltip on Tips tab
- [x] Add constants panel for ÷8, 0.5 mg/ml, 30 mg basal, 4% absorption
- [x] Add disclaimers — anchor, urgent symptoms, uncertainty near chart
- [x] Add Terms and Conditions page
- [x] Add Privacy page
- [x] Review paywall security — success page bypass blocked, promo code system added, client-side limitations documented in SECURITY.md
- [x] Promo code system added — PROMO_HASHES array, hashed input, modal UI
- [ ] Move DEV_MODE to top of first script tag
- [x] Fix maintenance rate bug (`tieredRate` → `maintAbsRate` in calcStrategy)
- [x] GitHub repo public with .gitignore protecting credentials
- [x] Site live on GitHub Pages
- [x] v1.0.0-beta released — 8 May 2026

---

## Strategy Tab — Tooltip and Language Fixes (May 2026)

- [x] Start ferritin tooltip — removed BSH/NICE attribution, updated "Optimal for menstruating women" to sufficiency threshold framing
- [x] Balance Model infusion note — rnd(mg2f(1000)) replaced with "60–125 µg/L in non-anaemic patients" range with anaemia caveat
- [x] GP letter 30 µg/L label — added "(BSH 2021)" citation
- [x] Recovery target badge — "Optimal" changed to "Well-repleted"
- [x] Strategy chart commentary — removed "immediately" from infusion spike timing language
- [x] ctip-post-iv and ctip-ia-peak tooltips — updated from simple ÷8 formula to tiered model description with population-average caveat
- [x] Stored iron conversion note added to ctip-start-ferr and ctip-recovery-target tooltips

## Strategy Tab — Alt-Day and Formulation (May 2026)

- [x] Alt-day option card and ALTERNATE-DAY DOSING NOTE hidden when maintDailyMg < fm2.elemPerTab (already below one tablet/day)
- [x] Phase 2 formulation comparison table added — sulfate, fumarate, bisglycinate, Spatone with dynamic dose calculations
- [x] Phase 2 diet commentary added — conditional framing (close gap / contribute / insufficient) with specific practical examples and absorption notes

## Infusion Planner — Enhancements (May 2026)

- [x] Fix expected decline rate formula (was incorrectly scaling flowMl by bleed days)
- [x] Add bleed days validation warnings (>10 on pill = amber, >15 any = red)
- [x] Add actual vs expected decline rate consistency check (30% threshold)
- [x] Add symptomatic zone band (15–30 µg/L) on infusion analysis chart
- [x] Add projected "back to critical" (30 µg/L) date from last actual
- [x] Add smooth orange trend curve through actuals (spanGaps, tension 0.4)
- [x] Fix pre-infusion dot hidden behind symptomatic band (moved to beforeDatasetsDraw)
- [x] Estimated ferritin today projected from last actual, orange curve extended to today
- [x] Post-infusion peak labelled as estimated in chart and narrative
- [x] Post-infusion test suggestion added to all infusion commentary
- [x] Infusion duration by threshold (above 50 / 30 / 15 µg/L) with dates
- [x] Estimated storage depletion date from expected decline rate
- [x] FERRITIN_FLOOR=8 constant — projection floors at very low ferritin, does not go negative
- [x] Three chart threshold zones with horizontal spread labels (15–30, <15, ≤floor)
- [x] Educational panels: blood test markers, typical progression stages, inflammation caveat
- [x] Clinical language refinement — uncertainty-aware wording throughout
- [x] Zone threshold labels removed from legend, placed inline on chart

---

## Phase 1 — Launch Ready

- [x] Stripe live and tested — real purchase working
- [ ] Full purchase flow tested on mobile
- [x] Paywall implemented and tested — modal, unlock, promo codes, success page verification
- [x] All disclaimers and Terms/Privacy in place
- [ ] Reach 100 users
- [ ] Get informal GP review

---

## Phase 2 — First 100 Users

- [ ] File Fe+ trademark at 100 users
- [ ] Share in iron deficiency Facebook groups and Reddit
- [ ] Approach Iron Deficiency UK / Anaemia Campaign
- [ ] Write guest post for women's health blog
- [ ] Test Instagram ad £20–30 budget
- [ ] Approach GP surgery for endorsement
- [ ] Warm intro to Hertility or Flo

---

## Phase 3 — Monetise and Scale

- [ ] Press outreach — women's health journalists
- [ ] White-label NDA and deck if interest confirmed
- [ ] Use GP endorsement everywhere if secured
- [ ] Instagram / TikTok educational content
- [ ] Consider British Society for Haematology
- [ ] Introduce Fe+ Pro upgrade tier
