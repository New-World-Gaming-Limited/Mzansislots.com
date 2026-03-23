#!/usr/bin/env python3
"""
Fix ALL promo codes across the entire MzansiSlots site using BrandBonus MCP as truth.
Handles: body text mentions, code display boxes, hero sections, tables, CTAs.
"""
import re
import os
import json
import glob

BASE = os.path.dirname(os.path.abspath(__file__))

with open('/home/user/workspace/mcp-promo-data.json') as f:
    MCP = json.load(f)

def fix_operator_in_html(html, slug, data):
    """Fix all promo code references for a specific operator in HTML."""
    correct_code = data['promo']
    correct_bonus = data['bonus']
    correct_url = data['exit_url']
    
    # Map of operator slug -> all known wrong codes for that operator
    wrong_codes = {
        'hollywoodbets': ['HOLLYBET', 'FWHOL'],
        'easybet': [],  # NEWBONUS is wrong, MAXBONUS is correct
        'lucky-fish': [],
        'zarbet': [],
        'tictacbets': [],
        'playbet': [],
    }
    
    # Special: Easybet - NEWBONUS -> MAXBONUS (but only in easybet context)
    if slug == 'easybet' and correct_code == 'MAXBONUS':
        # Replace NEWBONUS with MAXBONUS in promo code display elements
        # Be careful: only replace in code-display contexts, not in operator names like "NEWBONUS" text labels
        html = re.sub(r'(class="[^"]*promo-code[^"]*"[^>]*>)\s*NEWBONUS\s*(<)', 
                       lambda m: m.group(1) + correct_code + m.group(2), html)
        html = re.sub(r'(Code:\s*</span>\s*<[^>]*>)\s*NEWBONUS\s*(<)',
                       lambda m: m.group(1) + correct_code + m.group(2), html)
        html = re.sub(r'>Code:\s*NEWBONUS<', f'>Code: {correct_code}<', html)
        html = re.sub(r'code <strong>NEWBONUS</strong>', f'code <strong>{correct_code}</strong>', html)
        html = re.sub(r'code NEWBONUS', f'code {correct_code}', html, flags=re.IGNORECASE)
        html = re.sub(r'promo code NEWBONUS', f'promo code {correct_code}', html, flags=re.IGNORECASE)
        # Fix the hero promo code box
        html = re.sub(r'(>)\s*NEWBONUS\s*(</span>\s*</div>\s*<a[^>]*class="cta-btn")',
                       lambda m: m.group(1) + correct_code + m.group(2), html, flags=re.DOTALL)
    
    # Lucky Fish: BETS -> TOPBONUS
    if slug == 'lucky-fish' and correct_code == 'TOPBONUS':
        html = re.sub(r'(class="[^"]*promo-code[^"]*"[^>]*>)\s*BETS\s*(<)',
                       lambda m: m.group(1) + correct_code + m.group(2), html)
        html = re.sub(r'>Code:\s*BETS<', f'>Code: {correct_code}<', html)
        html = re.sub(r'code <strong>BETS</strong>', f'code <strong>{correct_code}</strong>', html)
        html = re.sub(r'code BETS\b', f'code {correct_code}', html, flags=re.IGNORECASE)
        html = re.sub(r'promo code BETS\b', f'promo code {correct_code}', html, flags=re.IGNORECASE)
    
    # ZARbet: BETS -> TOPBONUS  
    if slug == 'zarbet' and correct_code == 'TOPBONUS':
        html = re.sub(r'(class="[^"]*promo-code[^"]*"[^>]*>)\s*BETS\s*(<)',
                       lambda m: m.group(1) + correct_code + m.group(2), html)
        html = re.sub(r'>Code:\s*BETS<', f'>Code: {correct_code}<', html)
        html = re.sub(r'code <strong>BETS</strong>', f'code <strong>{correct_code}</strong>', html)
        html = re.sub(r'code BETS\b', f'code {correct_code}', html, flags=re.IGNORECASE)
        html = re.sub(r'promo code BETS\b', f'promo code {correct_code}', html, flags=re.IGNORECASE)
    
    # TicTacBets: BETS -> NEWBONUS
    if slug == 'tictacbets' and correct_code == 'NEWBONUS':
        html = re.sub(r'(class="[^"]*promo-code[^"]*"[^>]*>)\s*BETS\s*(<)',
                       lambda m: m.group(1) + correct_code + m.group(2), html)
        html = re.sub(r'>Code:\s*BETS<', f'>Code: {correct_code}<', html)
        html = re.sub(r'code <strong>BETS</strong>', f'code <strong>{correct_code}</strong>', html)
        html = re.sub(r'code BETS\b', f'code {correct_code}', html, flags=re.IGNORECASE)
    
    # Playbet: BETS -> NEWBONUS
    if slug == 'playbet' and correct_code == 'NEWBONUS':
        html = re.sub(r'(class="[^"]*promo-code[^"]*"[^>]*>)\s*BETS\s*(<)',
                       lambda m: m.group(1) + correct_code + m.group(2), html)
        html = re.sub(r'>Code:\s*BETS<', f'>Code: {correct_code}<', html)
        html = re.sub(r'code <strong>BETS</strong>', f'code <strong>{correct_code}</strong>', html)
        html = re.sub(r'code BETS\b', f'code {correct_code}', html, flags=re.IGNORECASE)

    # Hollywoodbets: HOLLYBET/FWHOL -> NEWBONUS
    if slug == 'hollywoodbets':
        # Fix "use promo code e.g., HOLLYBET or FWHOL" and variants
        html = re.sub(
            r'use promo code\s+(?:e\.g\.?,?\s*)?HOLLYBET(?:\s+or\s+FWHOL)?',
            f'use promo code {correct_code}',
            html, flags=re.IGNORECASE
        )
        html = re.sub(
            r'use promo code\s+(?:e\.g\.?,?\s*)?FWHOL(?:\s+or\s+HOLLYBET)?',
            f'use promo code {correct_code}',
            html, flags=re.IGNORECASE
        )
        # Replace standalone occurrences
        html = re.sub(r'\bHOLLYBET\b', correct_code, html)
        html = re.sub(r'\bFWHOL\b', correct_code, html)
        # Clean up any "NEWBONUS or NEWBONUS" that might result
        html = re.sub(rf'{correct_code}\s+or\s+{correct_code}', correct_code, html)
    
    # Update exit links
    if correct_url:
        html = re.sub(
            r'href="https://www\.mzansiwins\.co\.za/link/[^"]*"',
            f'href="{correct_url}"',
            html
        )
    
    return html


def process_file(filepath, slug=None):
    """Process a single HTML file."""
    with open(filepath, 'r') as f:
        html = f.read()
    
    original = html
    
    if slug and slug in MCP:
        # Operator-specific page
        html = fix_operator_in_html(html, slug, MCP[slug])
    else:
        # Multi-operator page (homepage, best-slot-sites, slot pages, indexes)
        for s, data in MCP.items():
            html = fix_operator_in_html(html, s, data)
    
    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        return True
    return False


def main():
    total = 0
    
    # 1. Reviews
    print("=== Reviews ===")
    for f in sorted(glob.glob(os.path.join(BASE, 'reviews', '*.html'))):
        slug = os.path.basename(f).replace('.html', '')
        if slug == 'index':
            if process_file(f):
                print("  index.html")
                total += 1
            continue
        if process_file(f, slug):
            print(f"  {slug}")
            total += 1
    
    # 2. Promo codes
    print("\n=== Promo Codes ===")
    for f in sorted(glob.glob(os.path.join(BASE, 'promo-codes', '*.html'))):
        slug = os.path.basename(f).replace('.html', '')
        if slug == 'index':
            if process_file(f):
                print("  index.html")
                total += 1
            continue
        if process_file(f, slug):
            print(f"  {slug}")
            total += 1
    
    # 3. Homepage
    print("\n=== Homepage ===")
    if process_file(os.path.join(BASE, 'index.html')):
        print("  index.html")
        total += 1
    
    # 4. Best slot sites
    print("\n=== Best Slot Sites ===")
    if process_file(os.path.join(BASE, 'best-slot-sites.html')):
        print("  best-slot-sites.html")
        total += 1
    
    # 5. Slot pages
    print("\n=== Slot Pages ===")
    sc = 0
    for f in sorted(glob.glob(os.path.join(BASE, 'slots', '*.html'))):
        if process_file(f):
            sc += 1
    print(f"  {sc} pages updated")
    total += sc
    
    # 6. Other root pages
    print("\n=== Other Pages ===")
    for name in ['lekka-slots.html', 'spina-zonke.html', 'news.html']:
        fp = os.path.join(BASE, name)
        if os.path.exists(fp) and process_file(fp):
            print(f"  {name}")
            total += 1
    
    print(f"\nTotal: {total} files updated")


if __name__ == '__main__':
    main()
