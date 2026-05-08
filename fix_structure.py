#!/usr/bin/env python3
"""
Analyze and fix HTML div structure in index.html
Track div nesting to ensure tab-model properly contains ferrChart and historicChartSection
"""

import re
import sys

# Read the file
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("=" * 80)
print("ANALYZING HTML STRUCTURE")
print("=" * 80)

# Find key sections
app_match = re.search(r'<div class="app">', content)
tab_model_open = re.search(r'<div id="tab-model"[^>]*>', content)
ferrChart = re.search(r'<canvas id="ferrChart"[^>]*>', content)
historicChartSection = re.search(r'<div id="historicChartSection"[^>]*>', content)
tab_actual_open = re.search(r'<div id="tab-actual"[^>]*>', content)

positions = {
    'app (open)': app_match.start() if app_match else None,
    'tab-model (open)': tab_model_open.start() if tab_model_open else None,
    'ferrChart': ferrChart.start() if ferrChart else None,
    'historicChartSection (open)': historicChartSection.start() if historicChartSection else None,
    'tab-actual (open)': tab_actual_open.start() if tab_actual_open else None,
}

print("\nKEY POSITIONS IN FILE:")
for name, pos in positions.items():
    if pos is not None:
        print(f"  {name:35} position {pos:8}")
    else:
        print(f"  {name:35} NOT FOUND")

print("\nORDER CHECK:")
pos_list = [(k, v) for k, v in positions.items() if v is not None]
pos_list.sort(key=lambda x: x[1])
for name, _ in pos_list:
    print(f"  → {name}")

# Track div depth
def analyze_div_structure(text):
    """Track opening and closing divs to find nesting depth at key points"""
    depth = 0
    depth_at_pos = {}
    open_divs = {}  # track what div is open at each depth
    
    # Find all div tags with their positions
    div_pattern = r'</?div[^>]*>'
    
    current_pos = 0
    for match in re.finditer(div_pattern, text):
        tag = match.group()
        pos = match.start()
        
        if tag.startswith('</'):
            depth -= 1
        else:
            depth_at_pos[pos] = depth
            # Extract id if present
            id_match = re.search(r'id="([^"]+)"', tag)
            if id_match:
                div_id = id_match.group(1)
                open_divs[div_id] = depth
                if div_id in ['app', 'tab-model', 'tab-actual', 'historicChartSection']:
                    print(f"\n  Div '{div_id}' opens at depth {depth}")
            depth += 1
    
    return depth_at_pos, open_divs

print("\nDIV NESTING ANALYSIS:")
depth_at_pos, open_divs = analyze_div_structure(content)

# Find closing divs for key sections
def find_matching_close(text, start_pos, div_id):
    """Find the closing </div> for a given opening div"""
    depth = 0
    start = text.find(f'id="{div_id}"', start_pos)
    
    if start == -1:
        return None
    
    # Find the actual opening tag
    tag_start = text.rfind('<div', 0, start)
    pos = tag_start
    
    while pos < len(text):
        if text[pos:pos+4] == '<div':
            # Check if it's opening or closing
            if text[pos+4:pos+5] != '/':
                depth += 1
                pos = text.find('>', pos) + 1
            else:
                pos += 1
        elif text[pos:pos+6] == '</div>':
            depth -= 1
            if depth == 0:
                return pos + 6
            pos += 6
        else:
            pos += 1
    
    return None

print("\nKEY SECTION RANGES:")
tab_model_close = find_matching_close(content, 0, 'tab-model')
if tab_model_close:
    print(f"  tab-model: position {tab_model_open.start()} to {tab_model_close}")
else:
    print(f"  tab-model: CLOSING NOT FOUND")

# Extract sections around key elements
print("\n" + "=" * 80)
print("CHECKING CONTENT AROUND KEY ELEMENTS")
print("=" * 80)

# Context around tab-model opening
print("\n--- TAB-MODEL OPENING (context) ---")
start = max(0, tab_model_open.start() - 200)
end = min(len(content), tab_model_open.start() + 300)
print(content[start:end])
print("...")

# Context around ferrChart
print("\n--- FERRCHART (context) ---")
start = max(0, ferrChart.start() - 200)
end = min(len(content), ferrChart.start() + 200)
print(content[start:end])
print("...")

# Context around historicChartSection closing and tab-actual opening
print("\n--- HISTORICCHARTSECTION CLOSE & TAB-ACTUAL OPEN ---")
historic_close = content.find('</div>', historicChartSection.start())
# Find next few closing divs
closes = []
pos = historicChartSection.start()
for i in range(5):
    pos = content.find('</div>', pos)
    if pos == -1:
        break
    closes.append(pos)
    pos += 6

if closes:
    start = max(0, closes[-2] - 100) if len(closes) > 1 else historicChartSection.start()
    end = min(len(content), tab_actual_open.start() + 300)
    print(content[start:end])
    print("...")

print("\n" + "=" * 80)
print("PROBLEM IDENTIFICATION")
print("=" * 80)

# Check if historicChartSection closing divs are present before tab-actual
hist_section_str = '<div id="historicChartSection"'
hist_close_search = content.find(hist_section_str)
if hist_close_search > -1:
    section_end = content.find('</div>', hist_close_search)
    # Count how many </div> between historicChartSection and tab-actual
    section_text = content[hist_close_search:tab_actual_open.start()]
    close_divs = section_text.count('</div>')
    print(f"\nBetween historicChartSection and tab-actual:")
    print(f"  Closing </div> tags: {close_divs}")
    print(f"  Expected: At least 1 for historicChartSection")

# Look for the actual structure issue
print("\nCURRENT ISSUE:")
between_content = content[historicChartSection.start():tab_actual_open.start()]
print("Content between historicChartSection and tab-actual:")
print(between_content[:500])

print("\n" + "=" * 80)
print("FIX STRATEGY")
print("=" * 80)

# Find the exact closing pattern needed
legend_end = content.find('</div>', content.find('historicLegend'))
# Find next </div> marks after that
next_divs_pos = []
search_pos = legend_end
for i in range(10):
    pos = content.find('</div>', search_pos)
    if pos == -1:
        break
    next_divs_pos.append(pos)
    search_pos = pos + 6

print(f"\nFound {len(next_divs_pos)} closing divs after historicLegend")

# The structure should be:
# - historicChartSection closes 
# - tab-model closes
# THEN tab-actual opens

# Find where tab-actual opens
tab_actual_pos = content.find('<div id="tab-actual"')

# Work backwards from tab-actual to find where to insert closing divs
section_before_tab_actual = content[max(0, tab_actual_pos-500):tab_actual_pos]
print(f"\n200 chars before tab-actual:")
print(section_before_tab_actual[-200:])

print("\nFIX: Need to ensure proper closing between historicChartSection and tab-actual")
print("  1. Close historicChartSection with </div>")
print("  2. Close tab-model with </div>")
print("  3. Then tab-actual opens")

# Show what needs to change
print("\n" + "=" * 80)
print("APPLYING FIXES")
print("=" * 80)

# Find the exact string to replace
# We need to find: end of historicLegend through the gap before tab-actual

search_start = content.find('historicLegend')
search_start = content.find('</div>', search_start)

# Now find how many </div> we have
closing_section_start = search_start
closing_section_end = content.find('<div id="tab-actual"', search_start)

closing_section = content[closing_section_start:closing_section_end]
print(f"\nCurrent section between historicLegend close and tab-actual:")
print(repr(closing_section))

# Count opening div tags before historicChartSection that need closing
# We need to close: historicChartSection (opened with <div id="historicChartSection")
# and tab-model (opened with <div id="tab-model">)

# Strategy: find exact strings and build proper fix
old_pattern = content.find('id="historicLegend"')
old_pattern = content.find('</div>', old_pattern)
old_pattern_end = content.find('<div id="tab-actual"', old_pattern)

old_section = content[old_pattern:old_pattern_end]
print(f"\nOLD SECTION ({len(old_section)} chars):")
print(repr(old_section))

# The new section should have 2 closing divs (historicChartSection, then tab-model)
new_section = "</div>\n</div>\n\n"

print(f"\nNEW SECTION ({len(new_section)} chars):")
print(repr(new_section))

# Apply fix
fixed_content = content[:old_pattern] + new_section + content[old_pattern_end:]

print("\n✓ Fix applied")

# Verify
print("\n" + "=" * 80)
print("VERIFICATION")
print("=" * 80)

# Check new structure
tab_model_close_new = fixed_content.find('</div>\n</div>\n\n<div id="tab-actual"')
if tab_model_close_new > -1:
    print("✓ Found proper closing: </div> </div> before tab-actual")
else:
    print("✗ Pattern not found as expected")

# Recount divs
print("\nRecounting div structure in fixed content...")
depth_at_pos_new, open_divs_new = analyze_div_structure(fixed_content)

# Save the fixed content
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

print("\n✓ Fixed file saved to index.html")

print("\nFINAL STRUCTURE VERIFICATION:")
print("  1. ferrChart is now inside tab-model: " + 
      str(fixed_content.find('id="tab-model"') < fixed_content.find('id="ferrChart"') < fixed_content.find('</div>\n</div>\n\n<div id="tab-actual"')))
print("  2. historicChartSection is inside tab-model: " + 
      str(fixed_content.find('id="tab-model"') < fixed_content.find('id="historicChartSection"') < fixed_content.find('</div>\n</div>\n\n<div id="tab-actual"')))
print("  3. tab-model closes before tab-actual opens: " +
      str(fixed_content.find('</div>\n</div>\n\n<div id="tab-actual"') > 0))

print("\n" + "=" * 80)
print("✓ STRUCTURE FIX COMPLETE")
print("=" * 80)
