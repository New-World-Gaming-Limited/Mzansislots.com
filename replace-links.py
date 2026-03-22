#!/usr/bin/env python3
"""Replace all MzansiWins review links with local MzansiSlots review links.
Also updates link text from 'Full Review on MzansiWins' to 'Full Review'."""

import os, re, json

# MzansiWins review URL -> local review slug mapping
# Key: the exact slug used in MzansiWins URLs (without https://www.mzansiwins.co.za/ and -review/)
# Value: the local slug (for reviews/SLUG.html)
url_map = {
    'easybet': 'easybet',
    'hollywoodbets': 'hollywoodbets',
    'world-sports-betting': 'world-sports-betting',
    '1xbet': '1xbet',
    '10bet': '10bet',
    'tictacbets': 'tictacbets',
    'lucky-fish': 'lucky-fish',
    'zarbet': 'zarbet',
    'supabets': 'supabets',
    'supersportbet': 'supersportbet',
    'betxchange': 'betxchange',
    'betway': 'betway',
    'gbets': 'gbets',
    'jackpotcity': 'jackpotcity',
    'bettabets': 'betta-bets',
    'playbet': 'playbet',
    'wanejo-bets': 'wanejo-bets',
    'betfred': 'betfred',
    'sportingbet': 'sportingbet',
}

PROJECT = '/home/user/workspace/mzansislots'
SKIP_DIRS = {'reviews', 'promo-codes', '.git', 'node_modules'}

total_replacements = 0
files_modified = 0

for root, dirs, files in os.walk(PROJECT):
    # Skip certain directories
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    
    for fname in files:
        if not fname.endswith('.html'):
            continue
        
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, PROJECT)
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        file_changes = 0
        
        # Determine the prefix based on directory depth
        # Root level: reviews/slug.html
        # slots/ or news/ subdirectory: ../reviews/slug.html
        depth = rel.count(os.sep)
        if depth == 0:
            prefix = 'reviews/'
        else:
            prefix = '../reviews/'
        
        # Replace each MzansiWins review URL with local review URL
        for mzw_slug, local_slug in url_map.items():
            old_url = f'https://www.mzansiwins.co.za/{mzw_slug}-review/'
            new_url = f'{prefix}{local_slug}.html'
            
            count = content.count(old_url)
            if count > 0:
                content = content.replace(old_url, new_url)
                file_changes += count
        
        # Also replace "Full Review on MzansiWins" text with "Full Review"
        text_count = content.count('Full Review on MzansiWins')
        if text_count > 0:
            content = content.replace('Full Review on MzansiWins', 'Full Review')
            file_changes += text_count
        
        # Since these are now internal links, remove target="_blank" rel="noopener noreferrer" from review links
        # Pattern: links pointing to reviews/*.html or ../reviews/*.html that still have target="_blank"
        # We need to be careful to only modify review links, not affiliate links
        review_link_pattern = re.compile(
            r'<a\s+href="(?:\.\.\/)?reviews\/[^"]+\.html"'
            r'\s+target="_blank"\s+rel="noopener noreferrer"'
        )
        for match in review_link_pattern.finditer(content):
            old = match.group(0)
            # Remove target and rel attributes
            new = re.sub(r'\s+target="_blank"\s+rel="noopener noreferrer"', '', old)
            content = content.replace(old, new)
        
        # Also handle cases with duplicate target/rel (from the best-slot-sites.html pattern)
        # Pattern: class="bss-review-link" target="_blank" rel="noopener noreferrer">
        # These review links should no longer be external
        content = re.sub(
            r'(href="(?:\.\.\/)?reviews\/[^"]+\.html")\s+target="_blank"\s+rel="noopener noreferrer"\s+class="([^"]*)"(?:\s+target="_blank"\s+rel="noopener noreferrer")?',
            r'\1 class="\2"',
            content
        )
        content = re.sub(
            r'(href="(?:\.\.\/)?reviews\/[^"]+\.html")\s+class="([^"]*)"\s+target="_blank"\s+rel="noopener noreferrer"',
            r'\1 class="\2"',
            content
        )
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            files_modified += 1
            total_replacements += file_changes
            print(f'  {rel}: {file_changes} changes')

print(f'\nTotal: {total_replacements} replacements across {files_modified} files')

# Verify no MzansiWins review links remain
remaining = 0
for root, dirs, files in os.walk(PROJECT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r') as f:
            c = f.read()
        matches = re.findall(r'mzansiwins\.co\.za/[a-z0-9-]+-review/', c)
        if matches:
            remaining += len(matches)
            rel = os.path.relpath(fpath, PROJECT)
            print(f'  REMAINING: {rel}: {matches}')

print(f'\nRemaining MzansiWins review links: {remaining}')
