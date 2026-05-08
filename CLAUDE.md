# Fe+ Iron Balance Tool — Claude Code Project Rules

## Project context

- **Project:** Fe+ Iron Balance Tool
- **Primary file:** `index.html` — single-file HTML app, all CSS and JavaScript inline (~4400 lines)
- **Supporting files:** `success.html`, `terms.html`, `privacy.html`, `cancel.html`
- **Stable version:** v1.0.0-beta (May 2026) — update this line when a new stable version is confirmed
- **Live URL:** GitHub Pages
- **Tool type:** Medical/health — iron deficiency tracking and GP discussion aid

## Session start checklist

- Read `FEATURES.md` at the start of every session to understand current phase, completed tasks, and open priorities
- Update `FEATURES.md` at the end of each session: mark completed items `[x]`, add any new issues found

## Working with index.html

- **Always use grep to find specific sections** — never do a full file read. The file is ~4400 lines and full reads waste context.
- When you need a function, grep for its name. When you need a section, grep for a nearby unique string then read a limited range with offset/limit.
- After any structural HTML fix (adding/removing divs), count div depths to confirm nesting is correct.
- Check the actual tab structure in the file rather than assuming fixed tab names or counts.
- Never break existing tab functionality when adding new features.
- `ferrChart` (canvas) must only appear inside the Balance Model tab — do not duplicate or move it.

## Paywall and DEV_MODE

- `DEV_MODE` constant is in the first `<script>` block in `<head>` — `true` for testing, `false` before deploying. Never leave it `true` in a commit intended for production.
- Paywall unlock is stored in `localStorage('ironToolUnlocked')`. The wrapper that intercepts `showTab()` for premium tabs is in the last `<script>` block before `</body>`.
- `BYPASS_HASH` and `PROMO_HASHES` are in source — safe to commit. The plaintext secrets they hash must never be committed.
- `PROMO_CODES.md` is in `.gitignore` — never commit it.

## Code style

- Prefer minimal surgical fixes over rewrites. Change only what the task requires.
- No speculative additions — don't add features, error handling, or abstractions not asked for.
- No comments explaining *what* the code does — only add a comment when the *why* is non-obvious (a hidden constraint, a clinical rationale, a workaround for a specific bug).
- When debugging UI issues, add targeted `console.log` statements to isolate the problem before fixing. Remove all debug output before finishing.

## Clinical language rules

This tool is a medical/health product. The following rules are non-negotiable:

- **Never add clinical recommendations, diagnoses, or treatment prescriptions to UI text, button labels, tooltips, or output copy.**
- All outputs must be framed as estimates, summaries, or conversation aids — not medical advice.
- Phrases like "you should take", "this will treat", "this diagnoses" are not permitted. Use "this suggests", "a GP discussion summary", "an estimate based on population averages".
- Disclaimer text already in the UI must not be removed or weakened.
- If a task requires adding new UI copy near clinical outputs, default to cautious framing and flag it if uncertain.
