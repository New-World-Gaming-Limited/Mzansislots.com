#!/usr/bin/env python3
"""Fix desktop nav in review/promo pages to include Reviews and Promo Codes."""

import os

PROJECT = '/home/user/workspace/mzansislots'

total = 0
for subdir in ['reviews', 'promo-codes']:
    dirpath = os.path.join(PROJECT, subdir)
    for fname in os.listdir(dirpath):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(dirpath, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        prefix = '../'
        
        # Find the desktop nav section and check if it has reviews
        desktop_start = content.find('class="nav-desktop"')
        if desktop_start < 0:
            continue
        desktop_end = content.find('</ul>', desktop_start)
        desktop_section = content[desktop_start:desktop_end]
        
        if 'reviews/index.html' in desktop_section:
            continue  # Already has it
        
        # Add Reviews and Promo Codes before News in the desktop nav
        desktop_news = f'<li><a href="{prefix}news.html">News &amp; Guides</a></li>'
        desktop_new = (
            f'<li><a href="{prefix}reviews/index.html">Reviews</a></li>\n'
            f'          <li><a href="{prefix}promo-codes/index.html">Promo Codes</a></li>\n'
            f'          {desktop_news}'
        )
        
        # Only replace the first occurrence (desktop nav)
        if desktop_news in desktop_section:
            new_desktop = desktop_section.replace(desktop_news, desktop_new)
            content = content[:desktop_start] + new_desktop + content[desktop_end:]
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            total += 1

print(f'Fixed desktop nav in {total} generated pages')
