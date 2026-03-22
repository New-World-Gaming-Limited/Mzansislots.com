#!/usr/bin/env python3
"""Fix mobile nav to include Reviews and Promo Codes links in all pages."""

import os, re

PROJECT = '/home/user/workspace/mzansislots'

total = 0

for root, dirs, files in os.walk(PROJECT):
    dirs[:] = [d for d in dirs if d in ('.', 'slots', 'news', 'reviews', 'promo-codes') or root == PROJECT]
    
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
        
        # Check if mobile nav already has reviews link
        if f'{prefix}reviews/index.html' in content:
            # Check if it's in the mobile nav section specifically
            # Find mobile-nav section
            mobile_start = content.find('class="mobile-nav"')
            if mobile_start >= 0:
                mobile_end = content.find('</nav>', mobile_start)
                mobile_section = content[mobile_start:mobile_end]
                if 'reviews/index.html' in mobile_section:
                    continue  # Already has it
        
        # Add Reviews and Promo Codes to mobile nav before News & Guides
        # Pattern: Spina Zonke link followed by News & Guides
        old_mobile = f'<a href="{prefix}spina-zonke.html">Spina Zonke</a>\n      <a href="{prefix}news.html">News &amp; Guides</a>'
        new_mobile = (
            f'<a href="{prefix}spina-zonke.html">Spina Zonke</a>\n'
            f'      <a href="{prefix}reviews/index.html">Reviews</a>\n'
            f'      <a href="{prefix}promo-codes/index.html">Promo Codes</a>\n'
            f'      <a href="{prefix}news.html">News &amp; Guides</a>'
        )
        
        if old_mobile in content:
            content = content.replace(old_mobile, new_mobile)
        else:
            # Try alternative: News might be right after something else
            # Just find the news link in mobile nav and insert before it
            mobile_start = content.find('class="mobile-nav"')
            if mobile_start >= 0:
                mobile_end = content.find('</nav>', mobile_start)
                mobile_section = content[mobile_start:mobile_end]
                
                news_link = f'<a href="{prefix}news.html">News &amp; Guides</a>'
                if news_link in mobile_section:
                    insert = (
                        f'<a href="{prefix}reviews/index.html">Reviews</a>\n'
                        f'      <a href="{prefix}promo-codes/index.html">Promo Codes</a>\n'
                        f'      {news_link}'
                    )
                    content = content[:mobile_start] + mobile_section.replace(news_link, insert) + content[mobile_end:]
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            total += 1

print(f'Fixed mobile nav in {total} files')

# Verify
missing_mobile = 0
for root, dirs, files in os.walk(PROJECT):
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, PROJECT)
        depth = rel.count(os.sep)
        prefix = '../' if depth > 0 else ''
        
        with open(fpath, 'r') as f:
            c = f.read()
        
        mobile_start = c.find('class="mobile-nav"')
        if mobile_start >= 0:
            mobile_end = c.find('</nav>', mobile_start)
            mobile = c[mobile_start:mobile_end]
            if 'reviews/index.html' not in mobile:
                missing_mobile += 1
                print(f'  MISSING mobile nav: {rel}')

print(f'\nFiles still missing mobile nav reviews link: {missing_mobile}')
