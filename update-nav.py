#!/usr/bin/env python3
"""Add Reviews and Promo Codes to navigation across all site pages."""

import os, re

PROJECT = '/home/user/workspace/mzansislots'
SKIP_DIRS = {'reviews', 'promo-codes', '.git', 'node_modules'}

total_files = 0

for root, dirs, files in os.walk(PROJECT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    
    for fname in files:
        if not fname.endswith('.html'):
            continue
        
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, PROJECT)
        depth = rel.count(os.sep)
        prefix = '../' if depth > 0 else ''
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # DESKTOP NAV: Add Reviews and Promo Codes before News & Guides
        # Pattern: <li><a href="...news.html">News &amp; Guides</a></li>
        desktop_news = f'<li><a href="{prefix}news.html">News &amp; Guides</a></li>'
        desktop_new_items = (
            f'<li><a href="{prefix}reviews/index.html">Reviews</a></li>\n'
            f'          <li><a href="{prefix}promo-codes/index.html">Promo Codes</a></li>\n'
            f'          {desktop_news}'
        )
        
        if desktop_news in content and f'{prefix}reviews/index.html' not in content:
            content = content.replace(desktop_news, desktop_new_items)
        
        # MOBILE NAV: Add Reviews and Promo Codes before News & Guides
        mobile_news = f'<a href="{prefix}news.html">News &amp; Guides</a>'
        
        # Check if there's a "More" label before News in mobile nav
        # Pattern: <span class="mobile-nav-label">More</span>\n      <a href="...spina-zonke.html">Spina Zonke</a>\n      <a href="...news.html">News &amp; Guides</a>
        mobile_more_pattern = f'<a href="{prefix}spina-zonke.html">Spina Zonke</a>\n      {mobile_news}'
        mobile_more_replacement = (
            f'<a href="{prefix}spina-zonke.html">Spina Zonke</a>\n'
            f'      <a href="{prefix}reviews/index.html">Reviews</a>\n'
            f'      <a href="{prefix}promo-codes/index.html">Promo Codes</a>\n'
            f'      {mobile_news}'
        )
        
        if mobile_more_pattern in content and f'{prefix}reviews/index.html' not in content:
            content = content.replace(mobile_more_pattern, mobile_more_replacement)
        elif mobile_news in content and f'{prefix}reviews/index.html' not in content:
            # Fallback: just add before news
            content = content.replace(
                mobile_news,
                f'<a href="{prefix}reviews/index.html">Reviews</a>\n      <a href="{prefix}promo-codes/index.html">Promo Codes</a>\n      {mobile_news}'
            )
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            total_files += 1

print(f'Updated navigation in {total_files} files')

# Verify
check = 0
for root, dirs, files in os.walk(PROJECT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r') as f:
            c = f.read()
        if 'reviews/index.html' in c:
            check += 1

print(f'Files now containing reviews link: {check}')
