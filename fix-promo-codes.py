#!/usr/bin/env python3
"""
Fix all promo codes, bonus text, and exit links across the entire site
using BrandBonus MCP data as the single source of truth.
Covers: reviews, promo-codes, homepage, best-slot-sites, slot game tables, news sidebars.
"""
import re
import os
import json
import glob

BASE = os.path.dirname(os.path.abspath(__file__))

with open('/home/user/workspace/mcp-promo-data.json') as f:
    MCP = json.load(f)

# Known old promo codes that need replacing per operator
OLD_CODES = {
    'hollywoodbets': ['HOLLYBET', 'FWHOL', 'NEWBONUS'],
    'easybet': ['NEWBONUS'],
    'lucky-fish': ['BETS', 'NEWBONUS'],
    'zarbet': ['BETS', 'NEWBONUS'],
    'tictacbets': ['BETS'],
    'playbet': ['BETS'],
    'betxchange': ['BETS'],
    'supersportbet': ['NEWBONUS'],
    '10bet': ['NEWBONUS'],
}


def fix_review_page(filepath, slug):
    """Fix promo codes, bonus text, exit links in a review page."""
    if slug not in MCP:
        return False

    with open(filepath, 'r') as f:
        html = f.read()

    original = html
    data = MCP[slug]
    correct_code = data['promo']
    correct_bonus = data['bonus']
    correct_url = data['exit_url']
    correct_terms = data['terms']

    # 1. Fix promo codes in promo-code-box / promo-code elements
    # Replace the displayed promo code text
    # Pattern: inside .promo-code, .promo-code-box, .brand-card-promo-code, etc.
    
    # Handle Hollywoodbets special case - has HOLLYBET and FWHOL scattered in text
    if slug == 'hollywoodbets':
        # Replace code references in running text
        html = re.sub(r'\b(HOLLYBET|FWHOL)\b', correct_code, html)
        # Fix "use promo code e.g., HOLLYBET or FWHOL" patterns
        html = re.sub(
            r'use promo code e\.g\.,?\s*\w+\s+or\s+\w+',
            f'use promo code {correct_code}',
            html, flags=re.IGNORECASE
        )
        html = re.sub(
            r'promo code\s+(?:e\.g\.,?\s*)?(?:HOLLYBET|FWHOL)(?:\s+or\s+(?:HOLLYBET|FWHOL))?',
            f'promo code {correct_code}',
            html, flags=re.IGNORECASE
        )

    # For all operators: fix the promo code displays
    if slug in OLD_CODES:
        for old_code in OLD_CODES[slug]:
            if old_code != correct_code:
                # Replace in code display elements (be careful not to replace in URLs or class names)
                html = re.sub(
                    rf'>{old_code}<',
                    f'>{correct_code}<',
                    html
                )
                # Replace in text content like "Code: OLDCODE"
                html = re.sub(
                    rf'Code:\s*{old_code}',
                    f'Code: {correct_code}',
                    html
                )
                html = re.sub(
                    rf'code\s+{old_code}',
                    f'code {correct_code}',
                    html, flags=re.IGNORECASE
                )

    # 2. Fix the hero promo code display (the big dashed-border code box)
    # Pattern: <span class="promo-code">OLDCODE</span> or similar
    html = re.sub(
        r'(<(?:span|div)[^>]*class="[^"]*promo-code[^"]*"[^>]*>)\s*[A-Z0-9]+\s*(</(?:span|div)>)',
        lambda m: m.group(1) + correct_code + m.group(2),
        html
    )

    # Also fix promo-code-box content
    html = re.sub(
        r'(<(?:span|div)[^>]*class="[^"]*promo-code-box[^"]*"[^>]*>)\s*[A-Z0-9]+\s*(</(?:span|div)>)',
        lambda m: m.group(1) + correct_code + m.group(2),
        html
    )

    # Fix brand-card-promo-code (homepage style)
    html = re.sub(
        r'(<span[^>]*class="brand-card-promo-code"[^>]*>)\s*[A-Z0-9]+\s*(</span>)',
        lambda m: m.group(1) + correct_code + m.group(2),
        html
    )

    # Fix "Code: XXX" in table cells
    html = re.sub(
        r'(Code:\s*</span>\s*<span[^>]*>)\s*[A-Z0-9]+\s*(</span>)',
        lambda m: m.group(1) + correct_code + m.group(2),
        html
    )

    # 3. Update exit links
    if correct_url:
        html = re.sub(
            r'href="https://www\.mzansiwins\.co\.za/link/[^"]*"',
            f'href="{correct_url}"',
            html
        )

    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        return True
    return False


def fix_homepage(filepath):
    """Fix promo codes on the homepage brand cards."""
    with open(filepath, 'r') as f:
        html = f.read()
    
    original = html
    
    # Fix Easybet: NEWBONUS -> MAXBONUS
    html = html.replace(
        '<span class="brand-card-promo-code">NEWBONUS</span>\n          </div>\n          <a href="https://www.mzansiwins.co.za/link/9b577ef9230623171008/"',
        f'<span class="brand-card-promo-code">{MCP["easybet"]["promo"]}</span>\n          </div>\n          <a href="{MCP["easybet"]["exit_url"]}"'
    )
    
    # Fix all three brand cards using MCP data
    for slug in ['easybet', 'hollywoodbets', 'betway']:
        if slug in MCP:
            data = MCP[slug]
            # Update exit URLs
            if data['exit_url']:
                html = re.sub(
                    r'href="https://www\.mzansiwins\.co\.za/link/[^"]*"',
                    f'href="{data["exit_url"]}"',
                    html
                )
    
    # Specific promo code fixes on homepage
    # Easybet card promo code
    html = re.sub(
        r'(Easybet.*?brand-card-promo-code">)[A-Z0-9]+(</span>)',
        lambda m: m.group(1) + MCP['easybet']['promo'] + m.group(2),
        html, flags=re.DOTALL, count=1
    )

    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        return True
    return False


def fix_best_slot_sites(filepath):
    """Fix promo codes in the best-slot-sites table."""
    with open(filepath, 'r') as f:
        html = f.read()
    
    original = html
    
    # For each operator in the table, find their promo code and fix it
    for slug, data in MCP.items():
        correct_code = data['promo']
        correct_url = data['exit_url']
        name = data['name']
        
        if correct_url:
            html = re.sub(
                r'href="https://www\.mzansiwins\.co\.za/link/[^"]*"',
                f'href="{correct_url}"',
                html
            )
    
    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        return True
    return False


def fix_slot_tables(filepath):
    """Fix promo codes in slot game casino tables."""
    with open(filepath, 'r') as f:
        html = f.read()
    
    original = html
    
    for slug, data in MCP.items():
        correct_code = data['promo']
        correct_url = data['exit_url']
        
        if correct_url:
            html = re.sub(
                r'href="https://www\.mzansiwins\.co\.za/link/[^"]*"',
                f'href="{correct_url}"',
                html
            )
    
    # Fix "Code: XXX" patterns in table cells
    # These follow operator-specific patterns  
    for slug, data in MCP.items():
        correct_code = data['promo']
        if slug in OLD_CODES:
            for old_code in OLD_CODES[slug]:
                if old_code != correct_code:
                    html = re.sub(rf'>Code:\s*{old_code}<', f'>Code: {correct_code}<', html)
                    html = re.sub(rf'>\s*{old_code}\s*<', f'>{correct_code}<', html)
    
    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        return True
    return False


def main():
    total = 0
    
    # 1. Fix review pages
    print("=== Reviews ===")
    for f in sorted(glob.glob(os.path.join(BASE, 'reviews', '*.html'))):
        slug = os.path.basename(f).replace('.html', '')
        if slug == 'index':
            continue
        if fix_review_page(f, slug):
            print(f"  {slug}")
            total += 1
    
    # 2. Fix promo code pages
    print("\n=== Promo Codes ===")
    for f in sorted(glob.glob(os.path.join(BASE, 'promo-codes', '*.html'))):
        slug = os.path.basename(f).replace('.html', '')
        if slug == 'index':
            # Fix index page too
            pass
        if fix_review_page(f, slug):  # Same logic works
            print(f"  {slug}")
            total += 1
    
    # 3. Fix homepage
    print("\n=== Homepage ===")
    hp = os.path.join(BASE, 'index.html')
    if fix_homepage(hp):
        print("  index.html")
        total += 1
    
    # 4. Fix best-slot-sites
    print("\n=== Best Slot Sites ===")
    bss = os.path.join(BASE, 'best-slot-sites.html')
    if fix_best_slot_sites(bss):
        print("  best-slot-sites.html")
        total += 1
    
    # 5. Fix slot game pages (casino tables)
    print("\n=== Slot Pages ===")
    slot_count = 0
    for f in sorted(glob.glob(os.path.join(BASE, 'slots', '*.html'))):
        if fix_slot_tables(f):
            slot_count += 1
    print(f"  {slot_count} slot pages updated")
    total += slot_count
    
    # 6. Fix promo-codes/index.html
    print("\n=== Promo Codes Index ===")
    pci = os.path.join(BASE, 'promo-codes', 'index.html')
    if os.path.exists(pci):
        if fix_review_page(pci, 'index'):
            print("  index.html")
            total += 1
    
    # 7. Fix reviews/index.html
    print("\n=== Reviews Index ===")
    ri = os.path.join(BASE, 'reviews', 'index.html')
    if os.path.exists(ri):
        if fix_review_page(ri, 'index'):
            print("  index.html")
            total += 1
    
    print(f"\nTotal: {total} files updated")


if __name__ == '__main__':
    main()
