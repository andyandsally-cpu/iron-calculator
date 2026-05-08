# Fe+ Iron Balance Tool — Technical Audit
## Release v1.0.0-beta · 8 May 2026

> **Purpose:** Independent technical review of `index.html` for the v1.0.0-beta release. Documents every output the app produces, how it is derived, all hardcoded assumptions, the security model, and known issues. Intended as the canonical reference for clinical and code reviewers.

---

## Contents

1. [File Statistics](#1-file-statistics)
2. [Tab Inventory](#2-tab-inventory)
3. [Input Fields](#3-input-fields)
4. [Calculated Outputs — Complete Inventory](#4-calculated-outputs--complete-inventory)
5. [Hardcoded Constants and Multipliers](#5-hardcoded-constants-and-multipliers)
6. [Tooltip System](#6-tooltip-system)
7. [Paywall and Security Architecture](#7-paywall-and-security-architecture)
8. [Clinical Safety Measures](#8-clinical-safety-measures)
9. [Known Bugs and Open Issues](#9-known-bugs-and-open-issues)
10. [Code Quality Observations](#10-code-quality-observations)

---

## 1. File Statistics

| Property | Value |
|---|---|
| Total lines | ~4,390 |
| Language | Single-file HTML (inline CSS + JS) |
| External dependencies | Chart.js (CDN) |
| CSS | ~100 lines embedded in `<style>` |
| JavaScript | ~3,100 lines across multiple `<script>` blocks |
| Tabs | 8 (4 free, 4 premium) |
| User inputs | ~40 (sliders, selects, text, number, radio, toggles) |
| Calculated/displayed numbers | ~50 across all tabs |
| Hardcoded numeric constants | ~45 |
| Tooltip cases | 40+ |
| Chart instances | 6 (main ferritin, historic, cycle, tips, tolerability, IV planner) |
| Named functions | ~100+ |
| localStorage keys | `ironToolUnlocked`, `fe_install_dismissed`, `fe_draft`, `fe_sessions` |

---

## 2. Tab Inventory

| Tab ID | Label | Access | Render Function(s) | Notes |
|---|---|---|---|---|
| `about` | About | Free | (static HTML) | Educational content, disclaimers, ferritin reference table |
| `model` | Balance model | Free | `calc()` | Core calculation engine; ferritin projection chart; metrics grid |
| `actual` | Results | Free | `renderCycleChart()`, `calcDerived()` | Blood test log, trend analysis, revised projection |
| `infusion` | Infusion | Free | `calcIV()` | IV infusion planner; multi-year refill schedule |
| `strategy` | Strategy 🔒 | **Premium** | `calcStrategy()`, `renderStratChart()` | Phase 1 recovery + Phase 2 maintenance plan |
| `tips` | Tips 🔒 | **Premium** | `calcTips()` | Diet tips, hormone treatment, inflammation scenarios |
| `tolerability` | Tolerability 🔒 | **Premium** | `calcTolerability()`, `renderTolChart()` | Side-effect adjustments; compromise cost |
| `export` | GP letter 🔒 | **Premium** | `updateLetterPreview()`, `buildGPLetter()` | Draft GP discussion letter |

**Paywall list** (hardcoded): `['strategy', 'tips', 'tolerability', 'export']`

---

## 3. Input Fields

### Core inputs (Balance Model tab)

| ID | Type | Label | Default | Feeds |
|---|---|---|---|---|
| `startFerr` | range (0–200) | Starting ferritin | 25 µg/L | All projections; tiered absorption rate selection |
| `cycleLen` | range (21–365) | Cycle length | 28 days | `cyclesPerMonth = 30 / cycleLen`; menstrual iron loss |
| `bleedDays` | range (0–40) | Bleeding days | 5 | `mlPerCycle = flowMl[flowIdx] × (bleedDays / 5)` |
| `flowInt` | range (1–5) | Flow intensity | 2 | Index into `flowMl` lookup table |
| `dietQ` | range (1–5) | Diet quality | 3 | Index into `dietQmg` table (mg/day dietary iron) |
| `suppDose` | range (0–390) | Supplement dose | 0 mg | Supplement absorption chain |
| `formulation` | radio | Iron formulation | Ferrous sulfate | `elemPerTab`, `packetMg`, absorption multiplier |
| `modVitC` | range (0–100%) | Vitamin C with supplement | 0% | Absorption enhancer modifier |
| `modTiming` | range (0–100%) | Taken 2hr+ from food/tea/coffee | 50% | Absorption enhancer modifier |
| `modTea` | range (0–100%) | Tea/coffee within 1hr | 0% | Absorption inhibitor modifier |
| `modCa` | range (0–100%) | Calcium within 1hr | 0% | Absorption inhibitor modifier |
| `modAntacid` | range (0–100%) | Antacid/PPI use | 0% | Absorption inhibitor modifier |
| `periodMgmt` | select | Period management method | natural | Sets cycle/bleed defaults; calls `applyPeriodMgmt()` |
| `patAge` | number | Age | 28 | `applyDefaults()` — post-menopausal threshold |
| `menopause` | select | Menopausal status | pre | Disables bleed inputs if post-menopausal |
| `startDate` | date | Plan start date | (today) | Chart x-axis labels; splits actuals by date |
| `adherenceSlider` | range (0–100) | Plan adherence | 70% | Expected ferritin change in plan-vs-actual analysis |

### Condition toggles

| ID | Label | Effect |
|---|---|---|
| `tog-endo` | Endometriosis | Adds condition note; no numeric multiplier |
| `tog-adeno` | Adenomyosis | Adds condition note; no numeric multiplier |
| `tog-coeliac` | Coeliac disease | Absorption × 0.45 |
| `tog-oral-intol` | Oral iron intolerance | Triggers IV planner suggestion in GP letter |
| `tog-pcos` | PCOS | Adds condition note; **no numeric multiplier** (evidence not reliably quantified) |
| `tog-vegan` | Vegan / plant-based diet | Absorption × 0.60 |

### IV infusion inputs

| ID | Type | Default | Notes |
|---|---|---|---|
| `ivFloor` | select | 30 µg/L | Trigger threshold for scheduling next infusion |
| `ivHorizon` | select | 24 months | Simulation window |
| Infusion dose (per-row in infusions array) | number | 1000 mg | Entered per infusion event; `mg2f(dose)` ferritin boost |

### Strategy tab inputs

| ID | Type | Default | Notes |
|---|---|---|---|
| `stratTarget` | range (20–150) | 50 µg/L | Phase 1 recovery target ferritin |
| `stratIVDose` | select | 0 mg | Optional infusion included in Phase 1 |

### Tips tab inputs

| ID | Type | Notes |
|---|---|---|
| `tipsHormoneTx` | select | Hormone treatment; maps to menstrual loss reduction % |
| Diet tip checkboxes | checkbox × 7 | Each applies a `dietMult` to dietary absorption |
| `tipsInflamOn` | checkbox | Inflammation resolution; absorption boost |

### Tolerability tab inputs

| ID / element | Type | Notes |
|---|---|---|
| Tolerability option checkboxes × 4 | checkbox | Apply absorption penalties/adjustments |

### GP Letter tab inputs

| ID | Default | Notes |
|---|---|---|
| `letterPatientName` | (empty) | Optional; used in salutation |
| `letterGPName` | (empty) | Optional; used in salutation |
| `letterPractice` | "Castle Medical Centre" | Letter header |
| `letterEmail` | "Reception@castlemc.nhs.uk" | Letter header |

---

## 4. Calculated Outputs — Complete Inventory

### 4.1 Ferritin projection chart (Balance Model tab)

**Canvas ID**: `ferrChart` · **Function**: `calc()` · **Library**: Chart.js

| Dataset | Colour | What it shows | Formula |
|---|---|---|---|
| Treatment plan | Blue solid | Monthly ferritin under current inputs | `ferrLine[m] = max(0, ferrLine[m-1] + ferrChangePM)` with infusion boost at month 1 if present |
| Stop scenario | Orange dashed | Ferritin if supplements stopped at target | Same formula from target month forward using diet-only `ferrChangePM` |
| Revised projection | Purple dashed | Projection from last blood test using derived rate | Uses `derivedRate` from actual results if ≥ 2 blood tests entered |
| Actual results | Orange dots | Manually entered blood tests | Plotted at exact dates |
| Target line | Green dashed | 50 µg/L recommended minimum | Hardcoded reference |
| Depleted line | Red dashed | 30 µg/L depleted stores threshold | Hardcoded reference |

**Core variable `ferrChangePM`** (µg/L/month):
```
ferrChangePM = mg2f(mgAbsMonth − totalLossMonth)
             = (mgAbsMonth − totalLossMonth) / 8
```

---

### 4.2 Metrics grid (Balance Model tab)

Rendered via `mc(label, value, unit, cssClass, ctipId)` helper. Three cards:

| Label | Value | Formula | Tooltip |
|---|---|---|---|
| Iron lost/month | `rnd(totalLossMonth)` mg | `mgLostMonth + 30` (menstrual + basal) | `ctip-iron-lost` |
| Absorbed/month | `rnd(mgAbsMonth)` mg | `dietNetMonth + suppAbsMonth` after modifiers | `ctip-abs-rate` |
| Net balance/month | `±rnd(netMonth)` mg | `mgAbsMonth − totalLossMonth` | `ctip-net-balance` |

**CSS class logic**:
- Iron lost: `danger` if > 40 mg, `warning` if > 20 mg, `ok` otherwise
- Absorbed: badge reads "Observed (from your results)" if actuals entered, else "Estimated (literature)"
- Net balance: `danger` if < −5 mg, `warning` if < 5 mg, `ok` otherwise

---

### 4.3 Menstrual blood loss calculation

**Displayed in**: `bleedNote` element and analysis box

| Output | Formula |
|---|---|
| ml/cycle | `flowMl[flowIdx] × (bleedDays / 5)` |
| mg iron/cycle | `mlPerCycle × 0.5` |
| Cycles/month | `30 / cycleLen` |
| mg lost/month (menstrual) | `mgLostCycle × cyclesPerMonth` |
| mg lost/month (total) | `mgLostMonth + 30` (adds fixed basal loss) |

**`flowMl` lookup table** (ml per cycle by intensity):
```
[10, 20, 45, 80, 120]  →  very light, light, moderate, heavy, very heavy
```

---

### 4.4 Absorption panel (Balance Model tab)

Four metric cards rendered by `updateAbsPanel()`:

| Label | Value | Tooltip |
|---|---|---|
| Diet contribution | `rnd(dietNetMonth)` mg/month | `ctip-diet-contrib` |
| Supplement absorbed | `rnd(suppAbsMonth)` mg/month (or "none" if dose = 0) | `ctip-supp-abs` |
| Total absorbed | `rnd(mgAbsMonth)` mg/month | `ctip-abs-rate` |
| Total losses | `rnd(totalLossMonth)` mg/month | `ctip-total-losses` |

**Diet absorption chain**:
```
dietIronMgDay = dietQmg[dietQ]          // lookup: [0, 6, 8, 10, 13, 16] mg/day
dietNetMonth  = dietIronMgDay × 0.04 × 30
              × coeliacMult × veganAbsMult
```

**Supplement absorption chain**:
```
tieredAbsRate = startFerr < 15 → 0.12
              | startFerr < 30 → 0.08
              | startFerr < 50 → 0.05
              | else            → 0.04

rawSuppAbs    = min(suppDoseElem × tieredAbsRate, 4.0) × 30
              × coeliacMult × veganAbsMult × bisglycinateMult

enhancer      = 1 + (modVitC × 0.50) + (modTiming × 0.25)
inhibitor     = 1 − (modTea × 0.35) − (modCa × 0.25) − (modAntacid × 0.40)
combinedMult  = max(enhancer × inhibitor, 0.10)

suppAbsMonth  = rawSuppAbs × combinedMult
```

**Effective absorption badge** (displayed in `effAbsBadge`):
- "enhanced" if combined multiplier ≥ 1.1
- "good" if ≥ 0.85
- "reduced" if ≥ 0.6
- "poor" if < 0.6

---

### 4.5 Results / Actual tab

**Blood test log**: User-entered array of `{date, ferritin, suppDoseElem}`.

**Derived analysis** (requires ≥ 2 blood tests):

| Output | Formula |
|---|---|
| Ferritin trend | `(lastFerritin − firstFerritin) / monthsElapsed` µg/L/month |
| Implied monthly absorption | `f2mg(ferritinRise) + totalLossMonth − infusionMg` mg/month |
| Expected vs actual comparison | `Math.abs(derivedRate − modelledRate)` vs threshold |

**Revised projection** (purple dashed line on chart):
- Origin: last blood test date and ferritin
- Slope: `derivedRate` (from actuals, not model)
- Stored in `window.revisedScenario`

**IV dominance flag**: If cumulative infusion iron > 200 mg, derived absorption skipped and model rate used instead.

---

### 4.6 Strategy tab (Premium)

**Phase 1 — Recovery metrics**:

| Output | Formula | Tooltip |
|---|---|---|
| Time to target (oral only) | Months until `ferrLine[m] ≥ stratTarget` | `ctip-time-target` |
| Time with infusion | Months with IV dose added at month 1 | `ctip-iv-months` |
| Post-infusion ferritin | `startFerr + mg2f(stratIVDose)` | `ctip-post-iv` |

**Phase 2 — Maintenance metrics**:

| Output | Formula | Tooltip |
|---|---|---|
| Deficit after diet | `max(0, totalLossMonth − dietNetMonth)` mg/month | `ctip-remaining-gap` |
| Daily mg needed | `deficitAfterDiet / (maintAbsRate × 30)` | `ctip-maint-dose` |
| Tablets/week | `ceil(dailyMgNeeded / elemPerTab) × 7 / cycleDays` rounded to practical schedule | `ctip-tabs-week` |
| Alternate-day dose | `deficitAfterDiet / (maintAbsRate × altDayMult × 15)` where `altDayMult` = 1.10 (standard) or 1.03 (bisglycinate) | `ctip-altday` |

If `deficitAfterDiet = 0`: outputs "Diet alone sufficient — no supplement needed."

**Phase 1 chart** (`renderStratChart()`): Shows ferritin trajectory toward `stratTarget` with and without infusion; same projection engine as main chart.

---

### 4.7 Tips tab (Premium)

**Starting point**: 50 µg/L (fixed illustration baseline — not user's actual ferritin)

**Baseline (diet only, no supplements)**:
```
baseFerrPM = mg2f(dietNetMonth − totalLossMonth)
baseLine[m] = baseLine[m-1] + baseFerrPM
```

**Diet tip multipliers** (cumulative, applied to `dietNetMonth`):

| Tip | Multiplier |
|---|---|
| Vitamin C with meals | × 1.25 |
| Avoid tea/coffee at meals | × 1.20 |
| Avoid calcium near meals | × 1.15 |
| Add haem iron (red meat / liver) | × 1.30 |
| Reduce phytates | × 1.18 |
| Cast-iron cookware | × 1.05 |
| **Combined cap** | × 2.5 maximum |

**Hormone treatment loss reductions**:

| Treatment | Menstrual loss reduction |
|---|---|
| Combined pill (cyclic) | −45% |
| Tranexamic acid | −50% |
| Norethisterone | −80% |
| Mirena IUS | −85% |
| Combined pill (extended / tricycling) | Bleeds reduced to 4–6/year; configured via separate `cycleLenOverride` |

**Inflammation resolution** (if `tipsInflamOn` checked):
```
absBoost = min(0.04 / tieredRate, 3.0)
dietNetMonth × absBoost applied to dietOptLine
```

**Chart datasets**:
- Grey dashed: diet only, no supplements
- Amber: diet with selected tip multipliers
- Purple: diet + hormone treatment
- Teal: diet + inflammation resolved
- Green: all selected changes combined (tooltip: `ctip-combined12m`)

**Monthly rate figure** (e.g. "3.6 µg/L/month"): inline `<span data-ctip="ctip-diet-rate">` — tooltip shows loss/absorption/net breakdown.

**12-month projection figure**: inline `<span data-ctip="ctip-diet12m">` — tooltip shows scenario assumptions.

---

### 4.8 Tolerability tab (Premium)

**Adjustment options**:

| Option | Absorption effect |
|---|---|
| Take with food | × 0.62 (−38%) |
| Alternate-day dosing | × 1.10 (+10% via hepcidin reset) |
| Start low (build up over 3 weeks) | × 0.70 in month 1 (−30%) |
| Switch to bisglycinate (20 mg capsule) | × 0.85 vs sulfate baseline; `fixedElemPerDay = 60 mg` |

**Compromise cost** (tooltip: `ctip-tol-cost`):
```
cost = idealFerr12m − adjustedFerr12m   (µg/L at 12 months)
```

**Chart**: Blue (ideal, empty stomach daily) vs orange (with adjustments).

---

### 4.9 Infusion planner (Free tab)

**Simulation loop** (`calcIV()`):
```
for month 1 to ivHorizon:
  ferrMo += dietOnlyChangePM
  if ferrMo ≤ ivFloor:
    ferrMo += mg2f(ivDose)
    record infusion event
```

**Displayed outputs**:

| Output | Formula |
|---|---|
| Infusions over horizon | `schedule.length` |
| Infusions per year | `schedule.length / (ivHorizon / 12)` |
| Total iron delivered | `schedule.length × ivDose` mg |
| Post-infusion ferritin | `ferrMo + mg2f(ivDose)` per event |
| Months between infusions | Derived from schedule intervals |

---

### 4.10 GP Letter tab (Premium)

All dynamic content derived from current model state:

| Field | Source |
|---|---|
| Patient name | `letterPatientName` input |
| GP name | `letterGPName` input |
| Date | `new Date()` formatted |
| Ferritin history | `actuals` array (min, max, most recent, first date) |
| Current ferritin | `startFerr` slider |
| Supplement description | Formulation-aware: name, dose, frequency |
| Maintenance dose | `calcStrategy()` Phase 2 output |
| Blood test schedule | Pre-calculated dates: +3, +5, +9 months from today |
| Conditions list | Active condition toggles |
| IV request | If `tog-oral-intol` is set |

Letter generated by `buildGPLetter()` as plain text array joined with `\n`. Copied via `copyGPLetter()`.

---

## 5. Hardcoded Constants and Multipliers

### Core clinical constants

| Value | Meaning | Location | Source / Rationale |
|---|---|---|---|
| `0.5` mg/ml | Iron per ml menstrual blood | `calc()`, `calcTips()` | Standard haematology reference |
| `8` mg/µg/L | Stored iron per unit ferritin | `mg2f()`, `f2mg()` helpers | 1 µg/L ferritin ≈ 8 mg storage iron (Skikne et al; BSH 2021) |
| `30` mg/month | Basal iron loss (skin, gut, sweat) | `calc()`, `calcStrategy()` | ~1 mg/day (Camaschella, NEJM 2015) |
| `4%` | Base dietary absorption rate | `calc()` | Mixed diet estimate (Camaschella 2015) |

### Tiered supplement absorption rates

| Ferritin range | Absorption rate | Rationale |
|---|---|---|
| < 15 µg/L | 12% | Severely depleted; body upregulates DMT1 (Hallberg et al) |
| 15–30 µg/L | 8% | Depleted stores (BSH 2021) |
| 30–50 µg/L | 5% | Below optimal |
| ≥ 50 µg/L | 4% | Repleted (maintenance rate) |

### Condition multipliers

| Condition | Multiplier | Applied to |
|---|---|---|
| Coeliac disease | × 0.45 | Both diet and supplement absorption |
| Vegan / plant-based diet | × 0.60 | Both diet and supplement absorption |
| Coeliac + vegan combined floor | × 0.30 | Prevents product (0.27) from stacking too severely |
| PCOS | × 1.0 (no effect) | Evidence not reliably quantified; text note only |

### Absorption modifiers

| Modifier | Effect | Direction |
|---|---|---|
| Vitamin C (100% coverage) | +0.50 | Enhancer |
| Optimal timing (100% coverage) | +0.25 | Enhancer |
| Tea/coffee within 1hr (100%) | −0.35 | Inhibitor |
| Calcium within 1hr (100%) | −0.25 | Inhibitor |
| Antacid/PPI use (100%) | −0.40 | Inhibitor |
| Minimum combined multiplier | 0.10 floor | Prevents absorption reaching zero |
| Bisglycinate vs sulfate/fumarate | × 1.6 base absorption | Higher chelated bioavailability |
| Bisglycinate alternate-day benefit | × 1.03 | Reduced vs standard (1.10) — partially bypasses hepcidin already |
| Standard iron alternate-day benefit | × 1.10 | Moretti et al hepcidin reset study |
| With-food absorption penalty | × 0.62 | Tolerability tab |
| Start-low build-up penalty | × 0.70 (month 1) | Tolerability tab |

### Diet quality lookup

| Slider position | Quality label | mg iron/day |
|---|---|---|
| 1 | Very poor | 6 |
| 2 | Poor | 8 |
| 3 | Average | 10 |
| 4 | Good | 13 |
| 5 | Excellent | 16 |

### Flow intensity lookup

| Slider position | Label | ml/cycle (baseline 5 bleed days) |
|---|---|---|
| 1 | Very light | 10 |
| 2 | Light | 20 |
| 3 | Moderate | 45 |
| 4 | Heavy | 80 |
| 5 | Very heavy | 120 |

### Hormone treatment loss reduction

| Treatment | Menstrual loss reduction |
|---|---|
| Combined pill (cyclic) | −45% |
| Tranexamic acid | −50% |
| Norethisterone | −80% |
| Mirena IUS | −85% |

### Reference ferritin thresholds (display and chart)

| Value (µg/L) | Meaning |
|---|---|
| 15 | Critically depleted — absent iron stores (BSH/WHO threshold) |
| 30 | Depleted stores threshold |
| 50 | BSH recommended minimum (menstruating women) |
| 100+ | Well-repleted / post-infusion target |

### Other numeric constants

| Value | Meaning | Location |
|---|---|---|
| 4.3 weeks/month | Used for weekly dose conversion | `calcStrategy()` (52.18 / 12) |
| 15 | Doses/month on alternate-day dosing | Tips, tolerability, strategy |
| 30.44 | Days/month (365.25 / 12) | Date arithmetic throughout |
| 200 mg | IV dominance threshold | `calcDerived()` — above this, oral absorption not derived |
| 2500 mg | Maximum sensible single infusion | Input validation |
| 0.04 | Fallback `maintAbsRate` if tiered rate unavailable | `calcStrategy()` |

---

## 6. Tooltip System

### Mechanism

- **Event**: `mousemove` delegation on `document`
- **Delay**: 2000 ms `setTimeout` before tooltip renders
- **Cancel triggers**: `mouseout` (to null), `scroll` (capture), `click`
- **Positioning**: `position:fixed`, viewport-relative (`getBoundingClientRect()` only — no scroll offset)
- **Overflow**: Auto-flips left if would exceed `window.innerWidth − 8`; flips up if would exceed `window.innerHeight − 8`
- **Element**: `#calcTooltip` (created on init if absent), z-index 9998, width 284 px

### HTML structure

```html
<div class="ctip-hdr">Title</div>
<div class="ctip-row"><span class="ctip-k">Key</span><span class="ctip-v">Value</span></div>
<div class="ctip-note">Footnote</div>
```

### Tooltip inventory

| ID | Tab | What it explains | Data source |
|---|---|---|---|
| `ctip-iron-lost` | Model | Monthly iron loss breakdown | `lc` object |
| `ctip-abs-rate` | Model | Absorption rate and modifiers | `window._ctipData` from `calcModifiers()` |
| `ctip-net-balance` | Model | Net monthly iron balance | `lc` object |
| `ctip-diet-contrib` | Model | Dietary iron contribution | `lc` (dietNetMonth, coeliacMult, veganAbsMult) |
| `ctip-supp-abs` | Model | Supplement absorption detail | `lc` object |
| `ctip-total-losses` | Model | Menstrual + basal breakdown | `lc` object |
| `ctip-bleed-ml` | Model | Blood volume → iron conversion | `lc` object |
| `ctip-eff-abs` | Model | Effective absorption badge detail | `window._ctipData.effAbs` |
| `ctip-stop-rate` | Model | Fall rate if supplements stop | `lc` object |
| `ctip-remaining-gap` | Strategy | Gap supplements need to cover | `lc` (totalLossMonth, dietNetMonth) |
| `ctip-time-target` | Strategy | Phase 1 time-to-target detail | `window._ctipData.target` |
| `ctip-maint-dose` | Strategy | Phase 2 daily mg calculation | `window._ctipData.maint` |
| `ctip-tabs-week` | Strategy | Tablets/week practical schedule | `window._ctipData.tabsWeek` |
| `ctip-altday` | Strategy | Alternate-day dose calculation | `window._ctipData.altday` |
| `ctip-post-iv` | Strategy | Post-infusion ferritin estimate | `window._ctipData.ivCalc` |
| `ctip-iv-months` | Strategy | Months to target with infusion | `window._ctipData.ivCalc` |
| `ctip-diet12m` | Tips | 12-month diet-only projection | `window._ctipData.diet12m` |
| `ctip-diet-rate` | Tips | Monthly ferritin change rate | `window._ctipData.diet12m` |
| `ctip-diet-mult` | Tips | Combined diet tip multipliers | `window._ctipData.dietMult` |
| `ctip-hormone-red` | Tips | Menstrual loss reduction detail | `window._ctipData.hormoneRed` |
| `ctip-inflam-boost` | Tips | Inflammation resolution boost | `window._ctipData.inflammBoost` |
| `ctip-combined12m` | Tips | All-changes combined scenario | `window._ctipData.combined12m` |
| `ctip-tol-cost` | Tolerability | µg/L cost of adjustment | `window._ctipData.tolCost` |
| `ctip-bisglyc` | Tolerability | Bisglycinate absorption advantage | `window._ctipData.bisglyc` |
| `ctip-spatone` | Tolerability | Spatone liquid iron numbers | `lc` + static calculation |
| `ctip-ferr-trend` | Results | Ferritin trend from blood results | `window._ctipData.derived` |
| `ctip-derived-abs` | Results | Implied absorption from actuals | `window._ctipData.derived` |
| `ctip-iv-dominated` | Results | Why derivation was skipped | Static text |
| `ctip-expected-adh` | Results | Expected change at adherence % | `window._ctipData.expectedAdh` |
| `ctip-gap-sig` | Results | Gap between actual and expected | `window._ctipData.gapSig` |
| `ctip-m12ferr` | Multiple | 12-month ferritin projection | `lc` object |

**Data flow**: Calculated values are written to `window._ctipData` during render functions (`calc()`, `calcStrategy()`, etc.) so the tooltip `content()` function can read them lazily on hover. This decouples rendering from tooltip generation but requires `_ctipData` entries to be kept in sync with calculation changes.

---

## 7. Paywall and Security Architecture

### 7.1 Gating mechanism

The original `showTab(t)` function is wrapped at runtime:

```javascript
var _showTab = showTab;
showTab = function(t) {
  var paid = ['strategy', 'tips', 'tolerability', 'export'];
  if (paid.indexOf(t) > -1 && !isUnlocked()) {
    document.getElementById('paywallFeature').innerHTML = names[t];
    document.getElementById('paywallModal').classList.add('show');
    return;       // ← premium tab render functions never execute
  }
  _showTab(t);
};
```

When a premium tab is clicked while locked: the tab content div remains hidden, the tab render function never runs, and the paywall modal is shown instead.

### 7.2 Unlock check

```javascript
function isUnlocked() {
  return DEV_MODE || localStorage.getItem('ironToolUnlocked') === 'true';
}
```

`DEV_MODE` is defined in the first `<script>` block in `<head>` and must be `false` in production.

### 7.3 Unlock paths

**Path 1 — Stripe payment**
- User clicks "Unlock full version — £9.99 →" in modal
- Stripe Payment Link: `https://buy.stripe.com/aFa28kf6R8IvbIv2Rcgfu00`
- After payment, Stripe redirects to `success.html?code=SECRET`
- `success.html` hashes `?code=` via `crypto.subtle.digest('SHA-256', ...)` and compares to `BYPASS_HASH`
- Only on match: `localStorage.setItem('ironToolUnlocked', 'true')` and success UI shown

**Path 2 — URL code (`?code=`)**
- `index.html` also runs `checkBypassCode()` on load
- Same SHA-256 comparison against `BYPASS_HASH`
- On match: sets localStorage, removes `?code=` from URL via `history.replaceState`
- `BYPASS_HASH = 'b74e142af73becb1f2f07aa2c44c8a24c7e0e31cc086e60c253d547840dac261'`

**Path 3 — Promo code**
- User clicks "Have a promo code?" in modal → expands input
- Input lowercased, trimmed, hashed via `crypto.subtle`
- Compared against `PROMO_HASHES` array (SHA-256 hashes only — no plaintext in source)
- On match: sets localStorage, shows "Code accepted — unlocking…", reloads after 800 ms
- `PROMO_HASHES = []` (empty at v1.0.0-beta — populate before distributing codes)

**Path 4 — Restore access**
- "Already paid? Restore access" button triggers `confirm()` dialog
- No hash verification — trust-based recovery for existing customers on new devices
- Sets localStorage directly on confirm

### 7.4 What this protects

- Premium tab content is never rendered while locked — render functions do not run
- `success.html` no longer unlocks on direct navigation (bypass fixed in v1.0.0-beta)
- Promo codes are stored as hashes only; plaintext codes are not in source

### 7.5 Known bypass vectors

| Vector | Ease | Status |
|---|---|---|
| `localStorage.setItem('ironToolUnlocked','true')` in DevTools console | Trivial | **Not mitigated** — inherent to client-side-only paywall |
| Direct `success.html` navigation (no code) | Easy | **Mitigated** — shows error, no localStorage write |
| `DEV_MODE = true` left in production | Easy if forgotten | **Mitigated** — currently `false`; must check before every deploy |
| `BYPASS_HASH` visible in source | Easy to observe | **Partially mitigated** — hash is one-way; plaintext secret must remain private |
| Shared `?code=` URL (unlimited uses) | Medium | **Not mitigated** — no per-use token or server-side expiry |
| "Restore access" button (no verification) | Easy | **By design** — legitimate recovery path |

Full threat model documented in `SECURITY.md`.

---

## 8. Clinical Safety Measures

### Disclaimers implemented

| Location | Text |
|---|---|
| About tab header | "This tool provides educational estimates to help you understand iron balance and prepare for a discussion with your GP. It does not diagnose conditions, recommend treatment, or replace medical advice." |
| About tab — urgent symptoms | "This tool is not suitable for urgent symptoms such as severe fatigue, chest pain, shortness of breath, or suspected anaemia — seek medical care promptly." |
| Balance Model tab header | Same anchor disclaimer as About |
| Strategy tab outputs | "These are example approaches based on your inputs — discuss any changes with your GP before starting." (approximate) |
| GP letter tab | "Please review this draft carefully before sending. Edit or remove any information that does not apply." |
| Near ferritin chart | "Results are estimates based on population averages. Individual variation is significant." |
| Page footer | © 2026 Fe+ Iron Balance Tool. All rights reserved. |
| HTML source comment | Proprietary and Confidential notice |
| Terms of Use page (`terms.html`) | Full legal terms including "not a medical device", emergency disclaimer, liability limitation |
| Privacy Policy page (`privacy.html`) | Full privacy notice; confirms no server-side data storage |

### Clinical reference ranges

All reference lines and threshold bandings are labelled with their source:

| Threshold | Source |
|---|---|
| 15 µg/L — absent stores | BSH / WHO |
| 30 µg/L — depleted stores | BSH 2021 |
| 50 µg/L — recommended minimum | BSH 2021 (menstruating women) |
| 100+ µg/L — well-repleted | BSH post-infusion guidance |

### Numerical safeguards

- `max(0, ...)` applied to all ferritin projections — ferritin cannot go negative
- `min(suppDoseElem × tieredAbsRate, 4.0)` caps daily absorbed iron at 4 mg/day ceiling
- Combined condition floor prevents vegan + coeliac stacking below × 0.30
- `max(enhancer × inhibitor, 0.10)` prevents absorption multiplier reaching zero
- IV dominance flag (> 200 mg infusion) suppresses unreliable derived absorption estimate

---

## 9. Known Bugs and Open Issues

### Fixed in v1.0.0-beta

| Bug | Fix |
|---|---|
| `tieredRate` ReferenceError in `calcStrategy()` (line 3650) | Replaced with correct in-scope `maintAbsRate` — was crashing `calc()` before IIFE ran, preventing all tooltip event listeners from attaching |
| Tooltip `position:fixed` with scroll offset | Removed `window.scrollX` / `window.scrollY` from positioning — these must not be added to `getBoundingClientRect()` values for fixed elements |
| Paywall modal `.show` class had no CSS | Added `#paywallModal.show { display: flex }` — modal was always `display:none` regardless of class |
| `success.html` unconditional unlock | Replaced with `?code=` SHA-256 verification before setting localStorage |

### Open issues

| # | Severity | Description |
|---|---|---|
| 1 | Low | **Tooltip incomplete** — not all metric cards have tooltip implementations; `ctip-` IDs may be present without a matching `content()` case, silently showing nothing |
| 2 | Low | **PCOS not numerically modelled** — `pcosMult = 1.0` is a placeholder; code comment acknowledges the mechanistic plausibility but notes evidence is not reliably quantified. Users with PCOS see no absorption penalty in calculations |
| 3 | Low | **Formulation snapping is silent** — slider value is rounded to nearest whole tablet; user input of 70 mg becomes 65 mg (1 tablet sulfate) with no visible warning |
| 4 | Low | **Adherence slider boundary labels** — label transitions (e.g. "≤ 25%") are slightly misaligned with the logic comparison operators at exact boundary values |
| 5 | Low | **Combined condition floor discontinuity** — coeliac × vegan = 0.27 multiplied, but floored at 0.30; each condition alone computes lower than the combined floor in some ranges |
| 6 | Info | **DEV_MODE must be manually set to false before each deploy** — no automated check or build step |
| 7 | Info | **`PROMO_HASHES` array is empty at release** — no promo codes are active; must be populated before distributing promo codes |
| 8 | Info | **Stripe `success_url` not yet configured with `?code=`** — Stripe redirect must be set in dashboard to `https://[site]/success.html?code=[SECRET]`; currently returns to plain success URL |
| 9 | Info | **`bleedNote` element has `data-ctip` but is replaced by inline text** — potential conflict between tooltip hover and the text content rendered into the same element by `calc()` |

---

## 10. Code Quality Observations

### Strengths

- **Single-file architecture** makes deployment trivial (no build step, no server required) and is appropriate for the tool's scope
- **Reactive calculation model** is consistent — all inputs feed through `calc()` which propagates to dependent functions; no stale state observed
- **`window._ctipData`** pattern cleanly separates tooltip data population (at render time) from tooltip display (at hover time)
- **localStorage auto-save** (every 1.5 s, keyed to `fe_draft`) means the user's session survives accidental tab closure
- **Clinical assumptions are documented inline** — `// Hallberg et al`, `// Moretti et al`, `// Camaschella NEJM 2015` etc. appear throughout the calculation code, providing an audit trail for numeric values
- **Tiered absorption rates** are physiologically grounded and clearly labelled in the UI

### Areas for attention

- **No minification or bundling** — the full source including all comments, constants, and logic is visible to any user who views page source. Acceptable for current threat model but noted.
- **`window._ctipData` is mutable global state** — if a render function fails silently (e.g. due to an input error), `_ctipData` may hold stale values from the previous calculation. Tooltips would then show incorrect numbers without any visible indication.
- **No input validation at system boundary** — inputs are read directly from DOM elements with `parseFloat()` / `parseInt()`; `NaN` values propagate silently into calculations. The `rnd()` helper appears to handle `NaN → 0` in some places but this is not consistent.
- **Chart end-label positioning** is hardcoded to 284 px / 298 px offsets — may clip on narrow viewports; not tested at < 320 px width.
- **GP letter default practice details** (`"Castle Medical Centre"`, `"Reception@castlemc.nhs.uk"`) will appear in any letter copied before the user updates them. These should be cleared or marked as placeholder text.
- **`DEV_MODE` is not enforced** — there is no assertion or CI check that `DEV_MODE === false` before deployment. A single character change to `true` would bypass the entire paywall silently.
- **`buildGPLetter()` generates plain text** — the letter is copied as unformatted text. Paragraph spacing and formatting depend on the paste target. Some GPs may receive a wall of text if pasted into certain email clients.
- **Session save/restore uses `localStorage` only** — no export/import mechanism; if the user clears browser data, all named sessions are lost with no recovery path.

---

*Audit prepared for v1.0.0-beta release · 8 May 2026*
