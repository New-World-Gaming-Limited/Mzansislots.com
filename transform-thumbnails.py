#!/usr/bin/env python3
"""Replace placeholder initials in related slot cards with actual game thumbnail images."""
import re
import json
import glob
import os

BASE = os.path.dirname(os.path.abspath(__file__))

with open('/home/user/workspace/thumb-map.json') as f:
    THUMBS = json.load(f)

replacements = 0

def replace_card(match):
    global replacements
    full = match.group(0)
    
    href_match = re.search(r'href="([^"]+)"', full)
    if not href_match:
        return full
    
    slug = href_match.group(1).replace('.html', '')
    
    if slug not in THUMBS:
        return full
    
    if 'xlink-card-placeholder' not in full:
        return full
    
    img_url = THUMBS[slug]
    name_match = re.search(r'xlink-card-name[^>]*>([^<]+)', full)
    alt = name_match.group(1).strip() if name_match else slug.replace('-', ' ').title()
    
    new_html = re.sub(
        r'<div class="xlink-card-placeholder"><span>[^<]*</span></div>',
        f'<img src="{img_url}" alt="{alt}" class="xlink-card-thumb" loading="lazy">',
        full
    )
    
    if new_html != full:
        replacements += 1
    return new_html


count = 0
for filepath in sorted(glob.glob(os.path.join(BASE, 'slots', '*.html'))):
    with open(filepath, 'r') as f:
        html = f.read()
    
    original = html
    
    html = re.sub(
        r'<a href="[^"]+\.html" class="xlink-card">.*?</a>',
        replace_card,
        html,
        flags=re.DOTALL
    )
    
    if html != original:
        with open(filepath, 'w') as f:
            f.write(html)
        count += 1

print(f'Updated {count} files, {replacements} thumbnails replaced')
