#!/usr/bin/env python3
"""
Move .game-quick-stats from inside game-page-header to after game-demo-section on slot pages.
This lets mobile users see the game demo first, with stats below.
On desktop, CSS will reposition the stats back alongside the header.
"""
import re
import glob
import os

slot_dir = os.path.join(os.path.dirname(__file__), 'slots')
count = 0

for filepath in sorted(glob.glob(os.path.join(slot_dir, '*.html'))):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Skip if already processed
    if 'game-stats-below' in html:
        continue
    
    # Extract the game-quick-stats div from game-page-header
    stats_pattern = r'(\s*<div class="game-quick-stats">.*?</div>\s*</div>)\s*(?=\s*</div>\s*</div>\s*</section>\s*\n*\s*<!-- [═]+ DEMO)'
    stats_match = re.search(stats_pattern, html, re.DOTALL)
    
    if not stats_match:
        # Try a simpler approach - find the stats div
        # Pattern: <div class="game-quick-stats">...stat-items...</div>
        stats_start = html.find('<div class="game-quick-stats">')
        if stats_start == -1:
            print(f"SKIP (no stats): {os.path.basename(filepath)}")
            continue
        
        # Find the closing </div> for game-quick-stats
        # Count nested divs
        depth = 0
        i = stats_start
        stats_end = -1
        while i < len(html):
            if html[i:i+4] == '<div':
                depth += 1
            elif html[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    stats_end = i + 6
                    break
            i += 1
        
        if stats_end == -1:
            print(f"SKIP (can't find end): {os.path.basename(filepath)}")
            continue
        
        stats_html = html[stats_start:stats_end]
        
        # Remove stats from original position
        html_modified = html[:stats_start] + html[stats_end:]
        
        # Find the end of game-demo-section to insert stats after it
        demo_end_pattern = r'(</section>\s*\n*\s*<!-- [═]+ WHERE TO PLAY)'
        demo_end_match = re.search(demo_end_pattern, html_modified)
        
        if not demo_end_match:
            # Try finding the closing of game-demo-section differently
            demo_section_end = html_modified.find('</section>', html_modified.find('game-demo-section'))
            if demo_section_end == -1:
                print(f"SKIP (no demo section end): {os.path.basename(filepath)}")
                continue
            demo_section_end += len('</section>')
            
            # Insert stats section after demo
            stats_section = f"""

<!-- Stats (below demo on mobile) -->
<section class="game-stats-below">
  <div class="container">
    {stats_html}
  </div>
</section>
"""
            html_modified = html_modified[:demo_section_end] + stats_section + html_modified[demo_section_end:]
        else:
            insert_pos = demo_end_match.start()
            stats_section = f"""</section>

<!-- Stats (below demo on mobile) -->
<section class="game-stats-below">
  <div class="container">
    {stats_html}
  </div>
</section>

"""
            # Replace the </section> + WHERE TO PLAY comment
            where_comment = demo_end_match.group(0)
            # We need to be more careful - just insert after the </section>
            # Find the actual </section> before WHERE TO PLAY
            html_modified = html_modified[:insert_pos] + stats_section + where_comment[len('</section>'):].lstrip()
            # Actually let me redo this more carefully
        
        # Let me use a cleaner approach
        # Re-read original and do it step by step
        pass
    
    # Clean approach: just do string manipulation
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if 'game-stats-below' in html:
        continue
    
    # 1. Find and extract game-quick-stats div
    stats_start = html.find('<div class="game-quick-stats">')
    if stats_start == -1:
        print(f"SKIP: {os.path.basename(filepath)}")
        continue
    
    # Find matching closing div
    depth = 0
    pos = stats_start
    stats_end = -1
    while pos < len(html):
        if html[pos:pos+4] == '<div':
            depth += 1
        elif html[pos:pos+6] == '</div>':
            depth -= 1
            if depth == 0:
                stats_end = pos + 6
                break
        pos += 1
    
    if stats_end == -1:
        print(f"SKIP (no closing div): {os.path.basename(filepath)}")
        continue
    
    stats_html = html[stats_start:stats_end].strip()
    
    # 2. Remove stats from original location (preserve whitespace cleanly)
    # Remove the stats div plus surrounding whitespace
    before_stats = html[:stats_start].rstrip()
    after_stats = html[stats_end:].lstrip()
    html_no_stats = before_stats + '\n      ' + after_stats
    
    # 3. Find end of game-demo-section
    # Look for closing </section> after game-demo-section
    demo_start = html_no_stats.find('game-demo-section')
    if demo_start == -1:
        print(f"SKIP (no demo section): {os.path.basename(filepath)}")
        continue
    
    # Find the </section> that closes game-demo-section
    # We need to count section depth
    section_depth = 0
    pos = html_no_stats.find('<section', demo_start - 20)  # go back to find the opening <section
    demo_section_end = -1
    while pos < len(html_no_stats):
        if html_no_stats[pos:pos+8] == '<section':
            section_depth += 1
        elif html_no_stats[pos:pos+10] == '</section>':
            section_depth -= 1
            if section_depth == 0:
                demo_section_end = pos + 10
                break
        pos += 1
    
    if demo_section_end == -1:
        print(f"SKIP (no demo section end): {os.path.basename(filepath)}")
        continue
    
    # 4. Insert stats section after demo section
    stats_section = f"""

<!-- Game Stats (positioned below demo on mobile, beside header on desktop) -->
<section class="game-stats-below">
  <div class="container">
    {stats_html}
  </div>
</section>"""
    
    html_final = html_no_stats[:demo_section_end] + stats_section + html_no_stats[demo_section_end:]
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_final)
    
    count += 1

print(f"\nDone! Modified {count} files.")
