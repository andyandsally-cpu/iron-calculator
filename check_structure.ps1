# PowerShell script to analyze HTML div structure

$file = Get-Content "index.html" -Raw
$lines = Get-Content "index.html"

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "HTML DIV STRUCTURE ANALYSIS" -ForegroundColor Cyan
Write-Host "=" * 80

# Find key positions
$positions = @{}

# Get line numbers for key elements
for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    if ($line -match 'id="app"') {
        $positions["app"] = $i + 1
    }
    if ($line -match 'id="tab-about"') {
        $positions["tab-about"] = $i + 1
    }
    if ($line -match 'id="tab-model"') {
        $positions["tab-model"] = $i + 1
    }
    if ($line -match 'id="ferrChart"') {
        $positions["ferrChart"] = $i + 1
    }
    if ($line -match 'id="historicChartSection"') {
        $positions["historicChartSection"] = $i + 1
    }
    if ($line -match 'id="tab-actual"') {
        $positions["tab-actual"] = $i + 1
    }
}

Write-Host "`nKEY ELEMENT POSITIONS:" -ForegroundColor Green
$positions.GetEnumerator() | Sort-Object Value | ForEach-Object {
    Write-Host "  Line $($_.Value): $($_.Key)"
}

# Analyze structure by counting opening/closing tags
Write-Host "`nDIV NESTING ANALYSIS:" -ForegroundColor Green

$depth = 0
$depth_map = @{}

foreach ($match in [regex]::Matches($file, '</?div[^>]*>')) {
    $tag = $match.Value
    $pos = $match.Index
    
    if ($tag -match '</div>') {
        $depth--
    } else {
        $depth_map[$pos] = $depth
        if ($tag -match 'id="(tab-model|tab-actual|ferrChart|historicChartSection)"') {
            $id = $matches[1]
            Write-Host "    Div '$id' opens at depth $depth"
        }
        $depth++
    }
}

# Check if elements are properly nested
Write-Host "`nNESTING VERIFICATION:" -ForegroundColor Yellow

$tab_model_line = $positions["tab-model"]
$ferr_chart_line = $positions["ferrChart"]
$historic_line = $positions["historicChartSection"]
$tab_actual_line = $positions["tab-actual"]

Write-Host "  Order: tab-model ($tab_model_line) → ferrChart ($ferr_chart_line) → historicChartSection ($historic_line) → tab-actual ($tab_actual_line)"

if ($tab_model_line -lt $ferr_chart_line -and $ferr_chart_line -lt $tab_actual_line) {
    Write-Host "  ✓ ferrChart is between tab-model and tab-actual (could be inside or outside tab-model)"
}

if ($tab_model_line -lt $historic_line -and $historic_line -lt $tab_actual_line) {
    Write-Host "  ✓ historicChartSection is between tab-model and tab-actual (could be inside or outside tab-model)"
}

# Count divs between key elements
Write-Host "`nDIV COUNT BETWEEN KEY POINTS:" -ForegroundColor Green

$tab_model_idx = $tab_model_line - 1
$ferr_idx = $ferr_chart_line - 1
$historic_idx = $historic_line - 1
$actual_idx = $tab_actual_line - 1

$between_model_and_ferr = 0
for ($i = $tab_model_idx; $i -lt $ferr_idx; $i++) {
    $between_model_and_ferr += @([regex]::Matches($lines[$i], '<div').Count)[0]
    $between_model_and_ferr -= @([regex]::Matches($lines[$i], '</div>').Count)[0]
}

$between_historic_and_actual = 0
for ($i = $historic_idx; $i -lt $actual_idx; $i++) {
    $between_historic_and_actual += @([regex]::Matches($lines[$i], '<div[^/]').Count)[0]
    $between_historic_and_actual -= @([regex]::Matches($lines[$i], '</div>').Count)[0]
}

Write-Host "  Between tab-model and ferrChart: net $between_model_and_ferr opening divs"
Write-Host "  Between historicChartSection and tab-actual: net $between_historic_and_actual divs"

# Show context around critical areas
Write-Host "`nCRITICAL CONTEXT - After historicChartSection:" -ForegroundColor Yellow
for ($i = $historic_idx; $i -lt [Math]::Min($historic_idx + 15, $lines.Count); $i++) {
    Write-Host "  Line $($i+1): $($lines[$i])"
}

Write-Host "`nSTATUS:" -ForegroundColor Cyan
# Check for double closing divs before tab-actual
$before_actual = ""
for ($i = $actual_idx - 3; $i -lt $actual_idx; $i++) {
    if ($i -ge 0) {
        $before_actual += $lines[$i]
    }
}

if ($before_actual -match [regex]::Escape('</div>') + '\s*' + [regex]::Escape('</div>') + '\s*' + [regex]::Escape('<div id="tab-actual"')) {
    Write-Host "✓ CORRECT: Two closing divs before tab-actual (historicChartSection closes, then tab-model closes)"
} elseif ($before_actual -match [regex]::Escape('</div>') + '\s*' + [regex]::Escape('<div id="tab-actual"')) {
    Write-Host "✗ ISSUE: Only one closing div before tab-actual - may need another closing div"
} else {
    Write-Host "? UNCLEAR: Structure not matching expected patterns"
}

Write-Host "`nCONCLUSION:" -ForegroundColor Cyan
Write-Host "If you see 'CORRECT' above, the structure is properly nested."
Write-Host "If you see 'ISSUE', ferrChart and/or historicChartSection may be outside tab-model."
Write-Host ("=" * 80)
