# Fe+ Iron Balance Tool — Release Notes

---

## v1.0.0-beta — 8 May 2026

**First live deployable version of the Fe+ Iron Balance Tool.**

### Summary

First release suitable for public deployment. Paywall, payment verification, legal pages, and security hardening are all in place. Known issues remain open and are tracked in FEATURES.md.

---

### Changes in this release

**App structure**
- Tab structure fixed with correct div nesting
- `DEV_MODE` constant added at top of first script block for development testing (must be `false` before deploying)

**Paywall and payments**
- Paywall modal implemented — premium tabs (Strategy, Tips, Tolerability, GP Letter) blocked until unlocked
- Stripe payment link integrated
- `?code=` URL unlock mechanism — SHA-256 hash of secret code compared to `BYPASS_HASH` in source
- Promo code system — separate `PROMO_HASHES` array; add/remove codes by hash without touching unlock logic
- Paywall modal display bug fixed — `.show` CSS class rule added so modal renders correctly

**Success page**
- `success.html` rewritten with payment verification — reads `?code=` parameter, hashes it, and only sets `localStorage` unlock flag if the hash matches
- Three UI states: verifying, success, error
- Direct navigation to `success.html` without a valid code now shows an error instead of unlocking

**Security**
- Direct `success.html` bypass blocked — unconditional `localStorage.setItem` removed
- `localStorage` unlock now requires a valid code hash (via payment redirect or promo code)
- `.gitignore` created — excludes `.env`, credential files, key/cert files, and `.claude/`

**Disclaimers and legal**
- Anchor disclaimer added to About tab and Balance Model tab headers
- Urgent symptoms warning added to About tab
- "Results are estimates" note added near ferritin chart
- "Example approaches" note added to Strategy tab
- GP letter review note added
- Terms and Conditions page added (`terms.html`)
- Privacy Policy page added (`privacy.html`)
- Copyright notice added to page footer and HTML source comment
- Support contact (`ironbalancetool@gmail.com`) added to About tab, Terms, Privacy, and success error page

**Stripe**
- Payment link updated from test mode (`test_` prefix) to live mode

**Bug fixes**
- Maintenance rate bug fixed — `tieredRate` variable reference in `calcStrategy` replaced with correct in-scope `maintAbsRate`

---

### Known issues

- Tooltip implementation incomplete — some calculated values do not yet have tooltips
- Constants explanation panel pending — ÷8, 0.5 mg/ml, 30 mg basal, 4% absorption not yet displayed

---

### Next version priorities

- Complete tooltip implementation across all metric cards
- Add constants explanation panel
- Add Terms and Privacy links to paywall modal footer

---
