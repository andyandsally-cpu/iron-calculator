# Fe+ Iron Balance Tool — Claude Code Project Rules

This file contains mandatory operating rules for Claude Code in this repository.

## High-risk non-negotiables

- This is a medical/health tool. Never add clinical recommendations, diagnoses, or treatment prescriptions.
- Frame outputs as estimates, summaries, or GP discussion aids — not medical advice.
- Do not remove or weaken disclaimer text.
- `DEV_MODE` must not be `true` in a production-ready commit.
- Plaintext unlock codes, promo codes, Stripe secrets, or credentials must never be committed.

## Project context

- Primary file: `index.html` — single-file HTML app, all CSS and JavaScript inline.
- Supporting files: `success.html`, `terms.html`, `privacy.html`, `cancel.html`.
- Live deployment: GitHub Pages.

## Working rules

- Read `CURRENT_TASK.md` first.
- If `CURRENT_TASK.md` says `# No active task`, is a template/stub, unclear, or not marked `ACTIVE`, ask before proceeding.
- Make the smallest possible change for the active task.
- Do not refactor unrelated systems.
- Do not add speculative features, cleanup, abstractions, or error handling.
- Use grep/search first; do not full-read `index.html`.
- Inspect only limited code ranges around relevant matches.
- After structural HTML changes, check div nesting.
- Preserve existing tab, chart, paywall, and unlock behaviour unless the task explicitly changes it.
- Remove all debug logs before finishing.

## Paywall notes

- Paywall unlock uses `localStorage('ironToolUnlocked')`.
- Premium tab interception is handled by the `showTab()` wrapper near the end of `index.html`.
- `BYPASS_HASH` and `PROMO_HASHES` are safe to commit; plaintext secrets are not.
- `SECURITY.md` is reference material for paywall/security tasks only.

## Required before finishing

- Summarise changed files.
- Summarise what changed.
- Confirm acceptance checks performed.
- Confirm debug logs removed.
- Do not update `FEATURES.md` unless explicitly asked.

# Current task

## Status
READY

## Goal
Add a mandatory code-reading rule to CLAUDE.md.

## Change
Append this section to CLAUDE.md verbatim:

---

## Code reading — mandatory rule

Never guess. Never assume. Never infer from variable names, screenshots,
or conversation history.

Before producing any task definition or fix:
- Grep and read the actual current code for every function involved
- Read the full function body — not just the lines around the change
- If a chart is involved: read dataset construction, all plugin draw
  functions, and legend code in full
- If save/restore is involved: read buildSessionData() and
  applySessionData() in full
- If a calculation is involved: read all branches of the function

Every CURRENT_TASK.md must include:
- Exact line numbers from grep/read of the current file
- The exact current code being replaced, quoted verbatim
- Never "around line X" — always the actual code

If index.html has not been read in the current session, read the
relevant sections before writing anything.

---

## Files involved
- CLAUDE.md only

## Acceptance checks
- Section appended to CLAUDE.md
- No other files touched