# Fe+ Iron Balance Tool — Security Model

This document describes the paywall architecture, what it protects, what it does not protect, and the known limitations of a client-side unlock approach.

---

## Architecture overview

The tool is a static single-file HTML application with no server. All paywall logic runs in the browser. There is no backend to call, no session token to validate, and no server-side verification of purchases.

Unlock state is stored in `localStorage` under the key `ironToolUnlocked`. When this value is `'true'`, premium tabs are accessible. This flag is set by one of three paths:

| Path | Mechanism |
|---|---|
| Stripe payment | Stripe redirects to `success.html?code=SECRET` after payment; page hashes the code and sets the flag if it matches |
| Promo code | User enters a code in the paywall modal; code is hashed and compared to `PROMO_HASHES` array |
| Restore access | User confirms on the restore prompt; flag is set directly (trust-based, no verification) |

---

## What is protected

**Premium tab content is not rendered until unlocked.** The `showTab` wrapper intercepts clicks on `strategy`, `tips`, `tolerability`, and `export` tabs. If `isUnlocked()` returns false, the paywall modal is shown and `_showTab` (the real tab switcher) is never called. The tab content divs remain hidden and their render functions (`calcStrategy`, `calcTips`, etc.) are never executed.

**`success.html` verifies the unlock code.** The page reads the `?code=` URL parameter, hashes it with `crypto.subtle.digest('SHA-256', ...)`, and compares the hex output to `BYPASS_HASH`. Only a matching hash sets `localStorage`. Navigating to `success.html` directly without a valid code shows an error state and does not unlock anything.

**Promo codes are stored as hashes only.** The `PROMO_HASHES` array in source contains SHA-256 hashes. The plaintext promo codes are not in the source. A valid hash in source does not reveal the code.

**`BYPASS_HASH` in source does not reveal the unlock code.** SHA-256 is a one-way function. Knowing the hash does not allow reverse-engineering the plaintext `?code=` value used by `success.html`, provided the plaintext secret is not guessable or exposed elsewhere.

---

## What is not protected

**Anyone who opens DevTools can unlock the app in seconds.** Running `localStorage.setItem('ironToolUnlocked','true')` in the browser console and reloading the page bypasses all paywall checks. This is an inherent limitation of any client-side-only paywall and cannot be fully prevented without a server.

**`DEV_MODE = true` bypasses the paywall entirely.** This flag is at the top of the first `<script>` tag in `<head>`. It must be set to `false` before any public deployment. If left `true`, `isUnlocked()` always returns `true` regardless of `localStorage`.

**The JavaScript source is visible to anyone.** All paywall logic, hash values, and tab-switching code can be read by anyone who views page source or opens DevTools. A determined user can understand the unlock mechanism fully. The `BYPASS_HASH` value is visible; only the secrecy of the plaintext code protects the `?code=` path.

**The "Restore access" flow has no verification.** The restore prompt relies on user honesty. Anyone who clicks it and confirms will set the unlock flag. This is intentional — it provides a low-friction recovery path for legitimate customers on a new device — but it means it can also be used to bypass payment.

**Tab content is lazy-rendered, not hidden by access control.** Premium tab HTML is present in the DOM but not rendered until the tab is opened. A user inspecting the DOM before unlocking will see the empty container divs. The actual computed content (charts, recommendations) is only populated when the tab render functions run, which only happens post-unlock — but the structure is visible.

---

## Threat model

| Threat | Likelihood | Impact | Mitigated? |
|---|---|---|---|
| DevTools console unlock | High | Full bypass | No — inherent to client-side |
| Direct `success.html` navigation | Low | Previously a full bypass | Yes — code hash verification added |
| `DEV_MODE` left true in production | Low | Full bypass | Partially — must remember to set false |
| Brute-force `?code=` parameter | Very low | Full bypass if guessed | Mitigated by secret length/entropy |
| Sharing a working `?code=` URL | Medium | Unlimited unlocks per shared URL | Not mitigated — no per-use token |
| Source inspection of `BYPASS_HASH` | High (trivial) | Reveals hash, not plaintext | Mitigated — hash is one-way |

---

## Recommendations for strengthening (future)

- **Server-side verification**: A minimal serverless function (e.g. Cloudflare Worker or Vercel Edge Function) that verifies a Stripe payment intent before setting the unlock flag would eliminate the console bypass.
- **Short-lived or single-use codes**: Generating a unique `?code=` per purchase (via Stripe webhook) and expiring it after first use would prevent URL sharing.
- **Content obfuscation**: Minifying or bundling the source does not prevent bypass but raises the barrier slightly for casual users.
- **Rate limiting**: Not applicable to a static site without a server.

The current model is appropriate for a low-price consumer tool where the cost of circumvention (finding DevTools instructions, understanding the flow) exceeds the price of the product for most users. It is not appropriate for high-value or regulated content.

---

## Key values (do not commit plaintext secrets)

| Name | Location | Notes |
|---|---|---|
| `BYPASS_HASH` | `index.html`, `success.html` | SHA-256 of the unlock code — safe to commit |
| `PROMO_HASHES` | `index.html` | Array of SHA-256 hashes — safe to commit |
| Plaintext unlock code | **Not in source** | Must be kept secret; used in Stripe `success_url` |
| Plaintext promo codes | **Not in source** | Store securely; share only with intended recipients |
| Stripe secret key | **Not in source** | Never commit; not currently used (no server) |
