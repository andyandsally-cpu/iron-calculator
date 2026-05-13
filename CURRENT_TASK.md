# Current task

## Status
READY

## Goal
Add narrative explanation to the Balance Model tab explaining why
iron balance is difficult for pre-menopausal women, using the user's
actual calculated values from lc to make it personal.

## Where to insert
Grep for `id="balanceChartSection"`. Insert immediately BEFORE this
div.

## Implementation
This is a dynamically rendered div — populate it from lc values in
a new function `renderBalanceNarrative()` called at the end of calc()
alongside renderBalanceCharts().

### HTML placeholder — insert before balanceChartSection:
```html
<div id="balanceNarrative" style="margin-bottom:20px"></div>
```

### New function renderBalanceNarrative()
Add near renderBalanceCharts(). Call it at end of calc() after
renderBalanceCharts().

```javascript
function renderBalanceNarrative(){
  var el=document.getElementById('balanceNarrative');
  if(!el||!lc)return;

  var losses=lc.totalLossMonth;
  var dietAbs=lc.dietNetMonth;
  var suppAbs=Math.max(0,lc.mgAbsMonth-dietAbs);
  var totalAbs=lc.mgAbsMonth;
  var net=lc.netMonth;
  var mlPerCycle=lc.mlPerCycle||0;
  var mgLostMonth=lc.mgLostMonth||0;
  var basal=lc.basalLossMonth||30;
  var dietSufficient=dietAbs>=losses;
  var suppSufficient=!dietSufficient&&totalAbs>=losses;
  var netUg=+(net/8).toFixed(1);

  // Opening explanation — always shown
  var html='<div style="padding:16px 20px;background:#f8fafc;'
    +'border-radius:10px;border:1px solid #e2e8f0;font-size:13px;'
    +'line-height:1.8;color:#1e293b;margin-bottom:4px">'
    +'<div style="font-weight:700;font-size:14px;margin-bottom:10px;'
    +'color:#1e3a5f">Why is iron balance so difficult for women '
    +'with periods?</div>'
    +'<p style="margin:0 0 10px">Iron deficiency is the most common '
    +'nutritional deficiency in pre-menopausal women — and the reason '
    +'is straightforward once you see the numbers. '
    +'<strong>Menstrual blood loss is the dominant driver.</strong> '
    +'Each millilitre of blood contains approximately 0.5mg of iron. ';

  if(mgLostMonth>0){
    html+='Based on your cycle settings, you are losing approximately '
      +'<strong>'+rnd(mgLostMonth)+' mg of iron per month</strong> '
      +'through bleeding alone. ';
  }

  html+='On top of this, everyone loses around <strong>'+rnd(basal)
    +' mg/month</strong> through skin cell shedding, gut lining '
    +'renewal, and sweat — these are unavoidable background losses. '
    +'Your total monthly iron requirement is therefore '
    +'<strong>'+rnd(losses)+' mg/month</strong>.</p>'

    +'<p style="margin:0 0 10px">A good diet provides real help — '
    +'your current diet setting contributes an estimated '
    +'<strong>'+rnd(dietAbs)+' mg/month</strong> of absorbable iron. ';

  if(dietSufficient){
    html+='<strong style="color:#16a34a">This covers your losses '
      +'— diet alone appears sufficient for your situation.</strong> '
      +'Your low monthly losses mean a good diet can realistically '
      +'keep stores stable without supplementation. This is not the '
      +'case for most pre-menopausal women, but with low bleeding '
      +'and a good omnivore diet it is achievable.</p>';
  } else {
    var gap=rnd(losses-dietAbs);
    html+='This leaves a gap of approximately <strong>'+gap
      +' mg/month</strong> that diet alone cannot bridge. ';

    if(suppAbs>0){
      html+='Your current supplement contributes a further '
        +'<strong>'+rnd(suppAbs)+' mg/month</strong> absorbed, ';
      if(suppSufficient){
        html+='which <strong style="color:#16a34a">closes the gap'
          +' — your current plan covers losses.</strong></p>';
      } else {
        var remaining=rnd(losses-totalAbs);
        html+='leaving a remaining deficit of <strong>'
          +remaining+' mg/month</strong> ('
          +Math.abs(netUg)+' µg/L/month). '
          +'The Strategy tab shows what dose would close this gap.</p>';
      }
    } else {
      html+='Without supplementation, stores are likely depleting '
        +'at approximately <strong>'+Math.abs(netUg)
        +' µg/L per month</strong>. The Strategy tab shows what '
        +'would be needed to correct this.</p>';
    }
  }

  // Why diet alone is often not enough — shown when diet insufficient
  if(!dietSufficient){
    html+='<p style="margin:0 0 10px;color:#475569;font-size:12px">'
      +'<strong>Why can\'t diet alone fix this?</strong> '
      +'Even a good omnivore diet only delivers ~30–40mg of absorbable '
      +'iron per month. When monthly losses exceed this — as they do '
      +'for most women with moderate to heavy periods — the shortfall '
      +'is simply too large for food alone to cover. '
      +'This is not a failure of diet quality; it is a mismatch '
      +'between the scale of menstrual loss and the limits of '
      +'intestinal iron absorption. Supplementation bridges this gap '
      +'reliably and safely.</p>';
  }

  // Recovery gets easier note — shown when currently supplementing
  // and ferritin is below target
  if(suppAbs>0&&lc.startFerr<50){
    html+='<p style="margin:0;color:#475569;font-size:12px">'
      +'<strong>Recovery then maintenance — why it gets easier:</strong> '
      +'During recovery (Phase 1), your supplement needs to cover '
      +'losses AND rebuild depleted stores — a larger ask. '
      +'Once ferritin reaches a healthy level, Phase 2 maintenance '
      +'only needs to replace monthly losses. This is a much smaller '
      +'target, which is why the maintenance dose is lower than the '
      +'recovery dose. Think of it as filling an empty tank versus '
      +'simply keeping a full one topped up.</p>';
  }

  html+='</div>';
  el.innerHTML=html;
}
```

## Files involved
- index.html — one HTML placeholder div before balanceChartSection,
  new renderBalanceNarrative() function, one call in calc()

## Out of scope
- Any calculation logic
- Any other tab or function

## Clinical language
All text framed as estimates. No prescriptive language.
Uses "appears sufficient", "likely depleting", "estimated".

## Acceptance checks
- Narrative renders on Balance Model tab using live lc values
- Updates when sliders change
- Diet sufficient message shown correctly for pill/light flow users
- Gap and deficit figures match the Iron Balance scales below
- Recovery note shown only when supplementing AND ferritin < 50
- No paywall / DEV_MODE regression