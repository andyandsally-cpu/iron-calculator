# Current task

## Status
READY

## Goal
Add a solid orange line connecting the two actual result points on the
"Where is this heading?" chart (renderBalChartE).

## Read first
Grep "function renderBalChartE" and read the full function to confirm
current dataset structure before editing.

## The fix
The actualData dataset currently has showLine:true but spanGaps:false,
so no line draws between the two sparse non-null points because
Chart.js won't bridge null gaps with spanGaps:false.

Change the actualData dataset to use spanGaps:true so the line
connects the two actual points across any null gaps between them:

Find the actualData dataset in the datasets array — it will look like:
```javascript
{label:'Actual results',data:actualData,
 borderColor:'#f97316',borderWidth:2.5,
 pointRadius:6,pointBackgroundColor:'#f97316',
 fill:false,tension:0,spanGaps:false,showLine:true}
```

Change `spanGaps:false` to `spanGaps:true`.

## Files involved
- index.html — renderBalChartE() actualData dataset only

## Out of scope
- Any other dataset or function

## Acceptance checks
- Solid orange line visible between the two actual result dots
- Dashed orange extrapolation continues from second actual onward
- No other changes
- No paywall / DEV_MODE regression