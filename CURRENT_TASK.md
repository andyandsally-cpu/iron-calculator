# Current task

## Status
READY

## Goal
Rewrite the explainBlock section in renderBalChartE() to be contextually
aware of user inputs. Only show factors that are actually plausible given
what the user has entered. Fix the "fully explains" threshold logic.

## Location: lines 2363–2396

## Replace lines 2363–2396 entirely with:

```javascript
var gapUgPM=+(rate-obsRate).toFixed(1);
var gapMgPM=+(gapUgPM*8).toFixed(1);

// Build contextually relevant explanation items
var explainItems=[];
var explainedUg=0;

// Flow: only suggest if NOT already at very heavy (flowIdx < 4)
var flowIdx=lc.flowIdx||0;
if(flowIdx<4){
  var VERY_HEAVY_MG=+(flowMl[4]*(lc.bleedDays/5)*0.5*(30/lc.cycleLen)).toFixed(1);
  var extraLossMg=Math.max(0,+(VERY_HEAVY_MG-(lc.mgLostMonth||0)).toFixed(1));
  var extraLossUg=+(extraLossMg/8).toFixed(1);
  if(extraLossUg>0.2){
    explainItems.push('Heavier blood loss than entered (e.g. flow intensity set to '
      +(['Very light','Light','Medium','Heavy'][flowIdx])+' — if actually heavier, '
      +'losses could be up to <strong>'+extraLossUg+' µg/L/mo more</strong> than modelled)');
    explainedUg=+(explainedUg+extraLossUg).toFixed(1);
  }
} else {
  // Already at very heavy — can't explain by flow
  explainItems.push('Flow is already set to Very heavy — higher blood loss cannot '
    +'explain this gap. This factor has been ruled out.');
}

// Supplement adherence: only suggest if user has a supplement entered
var suppAbsNow=Math.max(0,+((lc.mgAbsMonth||0)-(lc.dietNetMonth||0)).toFixed(1));
if(suppAbsNow>2){
  var halfDoseReductionUg=+(suppAbsNow*0.5/8).toFixed(1);
  explainItems.push('Lower supplement adherence (e.g. taking half the entered dose '
    +lc.suppDose+'mg/day — if actually taking ~'+Math.round(lc.suppDose/2)+'mg/day, '
    +'this could account for up to <strong>'+halfDoseReductionUg+' µg/L/mo</strong> of the gap)');
  explainedUg=+(explainedUg+halfDoseReductionUg).toFixed(1);
} else if(suppAbsNow<=2){
  explainItems.push('No significant supplement entered — reduced adherence cannot '
    +'explain this gap. Diet-only absorption is already fully modelled.');
}

var remainingGapUg=+(gapUgPM-explainedUg).toFixed(1);
var fullyExplained=remainingGapUg<=1.5;

var explainBlock='<div style="margin-top:10px;padding-top:10px;border-top:1px solid #e2e8f0">'
  +'<strong>Could this gap be explained by known factors?</strong>'
  +'<p style="margin:6px 0">The gap between your modelled and observed rate is '
  +'<strong>'+gapUgPM+' µg/L/mo ('+gapMgPM+' mg/mo)</strong>. '
  +'Here is what the known input variables can and cannot explain:</p>'
  +'<ul style="margin:4px 0 6px 16px;padding:0">'
  +explainItems.map(function(s){return '<li style="margin-bottom:4px">'+s+'</li>';}).join('')
  +'</ul>'
  +'<p style="margin:4px 0">';

if(explainedUg>0.2&&fullyExplained){
  explainBlock+='The plausible input variations above could account for up to '
    +'<strong>'+explainedUg+' µg/L/mo</strong> — broadly explaining the gap. '
    +'Before investigating further, review whether your entered flow and '
    +'supplement dose accurately reflect your real pattern. '
    +'A third blood test would confirm whether this trend is real.';
} else if(explainedUg>0.2&&!fullyExplained){
  explainBlock+='These variations could account for up to '
    +'<strong>'+explainedUg+' µg/L/mo</strong>, leaving a residual gap of '
    +'<strong>'+remainingGapUg+' µg/L/mo</strong> unexplained by input variations alone. '
    +'If your inputs accurately reflect your real situation, this persistent gap may '
    +'suggest reduced iron absorption — for example due to gut inflammation, '
    +'coeliac disease, or H. pylori infection. Worth discussing with your GP '
    +'if the pattern is confirmed across multiple results.';
} else {
  // Known factors ruled out — gap likely real
  explainBlock+='Based on your inputs, the known plausible explanations (flow, adherence) '
    +'have been largely ruled out. A gap of <strong>'+gapUgPM+' µg/L/mo</strong> despite '
    +'these factors being at their limits suggests a real difference between your modelled '
    +'and actual absorption. This may indicate reduced iron absorption — for example due to '
    +'gut inflammation, coeliac disease, or H. pylori infection. '
    +'Worth discussing with your GP if confirmed across multiple results.';
}

explainBlock+='</p></div>';
commentary+=explainBlock;
```

## Key improvements
- Flow factor: skipped entirely if already at Very heavy; shown with
  actual current flow label if lower
- Supplement factor: uses actual lc.suppDose value in the text;
  skipped with explanation if no supplement entered
- "Fully explains" threshold raised from <=1 to <=1.5 µg/L/mo
- When all factors are ruled out, says so directly rather than
  showing −0 values
- All bullet text is specific to user's actual inputs

## Files involved
- index.html — renderBalChartE() lines 2363–2396 only

## Out of scope
- Commentary branches for rateDiff>1.5 or within ±1.5 — do not touch
- Any other function or tab

## Acceptance checks
- Very heavy flow user: flow bullet says "ruled out", no −0 shown
- User with no supplement: supplement bullet says "cannot explain",
  no meaningless reduction shown
- Remaining gap calculation uses correct threshold (1.5 not 1.0)
- Text references actual user values (flow label, dose in mg)
- No paywall / DEV_MODE regression