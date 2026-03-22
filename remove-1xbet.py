#!/usr/bin/env python3
"""Remove all 1xBet references from MzansiSlots."""
import re
import os
import json
import glob

BASE = os.path.dirname(os.path.abspath(__file__))

# 1. Delete 1xBet-specific pages
for f in ['reviews/1xbet.html', 'promo-codes/1xbet.html']:
    path = os.path.join(BASE, f)
    if os.path.exists(path):
        os.remove(path)
        print(f"DELETED: {f}")

# 2. Remove 1xBet row from best-slot-sites.html
bss_path = os.path.join(BASE, 'best-slot-sites.html')
with open(bss_path, 'r') as f:
    html = f.read()

# Remove the 1xBet table row block (comment + tr + terms row)
# Pattern: <!-- 4. 1xBet --> ... until next <!-- 5. 
pattern = r'\s*<!-- 4\. 1xBet -->.*?(?=\s*<!-- 5\.)'
html = re.sub(pattern, '\n\n', html, flags=re.DOTALL)

# Renumber remaining entries (5->4, 6->5, etc.)
for old, new in [('>5<', '>4<'), ('>6<', '>5<'), ('>7<', '>6<'), 
                  ('>8<', '>7<'), ('>9<', '>8<'), ('>10<', '>9<'),
                  ('>11<', '>10<'), ('>12<', '>11<'), ('>13<', '>12<'),
                  ('>14<', '>13<'), ('>15<', '>14<'), ('>16<', '>15<'),
                  ('>17<', '>16<'), ('>18<', '>17<'), ('>19<', '>18<')]:
    # Only replace in rank cells
    html = html.replace(f'<td class="bss-rank-cell">{old[1:-1]}</td>', 
                        f'<td class="bss-rank-cell">{new[1:-1]}</td>')

# Also update comment numbers
for old_n in range(5, 20):
    html = html.replace(f'<!-- {old_n}. ', f'<!-- {old_n - 1}. ')

with open(bss_path, 'w') as f:
    f.write(html)
print("UPDATED: best-slot-sites.html (removed 1xBet row)")

# 3. Remove 1xBet card from reviews/index.html
rev_idx = os.path.join(BASE, 'reviews', 'index.html')
with open(rev_idx, 'r') as f:
    html = f.read()

# Find and remove the 1xBet review card
# Pattern: <div class="review-card"> ... 1xbet ... </div>\n  </div>
start = html.find('1xbet.svg')
if start != -1:
    # Go back to find the opening <div class="review-card">
    card_start = html.rfind('<div class="review-card">', 0, start)
    # Find the closing - count nested divs
    pos = card_start
    depth = 0
    card_end = -1
    while pos < len(html):
        if html[pos:pos+4] == '<div':
            depth += 1
        elif html[pos:pos+6] == '</div>':
            depth -= 1
            if depth == 0:
                card_end = pos + 6
                break
        pos += 1
    if card_end != -1:
        html = html[:card_start] + html[card_end:]
        print("UPDATED: reviews/index.html (removed 1xBet card)")

with open(rev_idx, 'w') as f:
    f.write(html)

# 4. Remove 1xBet row from promo-codes/index.html
promo_idx = os.path.join(BASE, 'promo-codes', 'index.html')
with open(promo_idx, 'r') as f:
    html = f.read()

start = html.find('1xbet.svg')
if start != -1:
    row_start = html.rfind('<div class="promo-row">', 0, start)
    pos = row_start
    depth = 0
    row_end = -1
    while pos < len(html):
        if html[pos:pos+4] == '<div':
            depth += 1
        elif html[pos:pos+6] == '</div>':
            depth -= 1
            if depth == 0:
                row_end = pos + 6
                break
        pos += 1
    if row_end != -1:
        html = html[:row_start] + html[row_end:]
        print("UPDATED: promo-codes/index.html (removed 1xBet row)")

with open(promo_idx, 'w') as f:
    f.write(html)

# 5. Remove 1xBet mentions from news articles
news_files = glob.glob(os.path.join(BASE, 'news', '*.html'))
for nf in news_files:
    with open(nf, 'r') as f:
        html = f.read()
    
    original = html
    
    # Remove list items mentioning 1xBet
    html = re.sub(r'<li>[^<]*1xBet[^<]*</li>\s*', '', html)
    # Remove links to 1xBet
    html = re.sub(r'<a[^>]*1xbet[^>]*>[^<]*</a>,?\s*', '', html, flags=re.IGNORECASE)
    # Remove table rows with 1xBet
    html = re.sub(r'<tr>\s*<td>[^<]*1xBet[^<]*</td>.*?</tr>\s*', '', html, flags=re.DOTALL)
    # Remove standalone mentions in paragraphs (replace "1xBet, " or ", 1xBet")
    html = re.sub(r',\s*1xBet\b', '', html)
    html = re.sub(r'\b1xBet,\s*', '', html)
    
    if html != original:
        with open(nf, 'w') as f:
            f.write(html)
        print(f"UPDATED: {os.path.relpath(nf, BASE)}")

# 6. Remove from news.html (root)
news_root = os.path.join(BASE, 'news.html')
if os.path.exists(news_root):
    with open(news_root, 'r') as f:
        html = f.read()
    original = html
    html = re.sub(r',\s*1xBet\b', '', html)
    html = re.sub(r'\b1xBet,\s*', '', html)
    if html != original:
        with open(news_root, 'w') as f:
            f.write(html)
        print("UPDATED: news.html")

# 7. Update sitemap.xml - remove 1xBet URLs
sitemap_path = os.path.join(BASE, 'sitemap.xml')
if os.path.exists(sitemap_path):
    with open(sitemap_path, 'r') as f:
        xml = f.read()
    xml = re.sub(r'\s*<url>\s*<loc>[^<]*1xbet[^<]*</loc>.*?</url>', '', xml, flags=re.DOTALL|re.IGNORECASE)
    with open(sitemap_path, 'w') as f:
        f.write(xml)
    print("UPDATED: sitemap.xml")

# 8. Clean JSON data files
for jf in ['operators-enriched.json', 'operators-data.json', 'top5-brands.json']:
    path = os.path.join(BASE, jf)
    if not os.path.exists(path):
        continue
    with open(path, 'r') as f:
        data = json.load(f)
    
    if isinstance(data, dict):
        if '1xBet' in data:
            del data['1xBet']
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"UPDATED: {jf} (removed 1xBet key)")
    elif isinstance(data, list):
        original_len = len(data)
        data = [d for d in data if not (
            d.get('name', '') == '1xBet' or 
            d.get('BrandName', '') == '1xBet' or
            d.get('operator', '') == '1xBet'
        )]
        if len(data) < original_len:
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"UPDATED: {jf} (removed 1xBet entry)")

print("\nDone! 1xBet has been removed from the site.")
