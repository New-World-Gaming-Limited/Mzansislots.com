#!/usr/bin/env python3
"""Update font loading across all HTML files:
- Replace Clash Display + General Sans Fontshare import with General Sans only
- Add JetBrains Mono from Google Fonts
- Add Inter from Google Fonts as backup
"""
import os, re

PROJECT = '/home/user/workspace/mzansislots'

# Old font loading patterns
OLD_PRELOAD = 'href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&amp;f[]=general-sans@400,500,600,700&amp;display=swap"'
OLD_PRELOAD_UNESC = 'href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=general-sans@400,500,600,700&display=swap"'

# New font URL (General Sans only from Fontshare)
NEW_FONTSHARE_URL = 'https://api.fontshare.com/v2/css?f[]=general-sans@400,600,700&display=swap'

total = 0

for root, dirs, files in os.walk(PROJECT):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules')]
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Replace the preload line (Fontshare)
        # Pattern: <link rel="preload" href="...clash-display...general-sans..." as="style" onload="...">
        content = re.sub(
            r'<link\s+rel="preload"\s+href="https://api\.fontshare\.com/v2/css\?f\[\]=clash-display@[^"]*"\s+as="style"\s+onload="[^"]*">',
            f'<link rel="preload" href="{NEW_FONTSHARE_URL}" as="style" onload="this.onload=null;this.rel=\'stylesheet\'">\n<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&display=swap" rel="stylesheet" media="print" onload="this.media=\'all\'">',
            content
        )
        
        # Replace the noscript fallback
        content = re.sub(
            r'<noscript><link\s+rel="stylesheet"\s+href="https://api\.fontshare\.com/v2/css\?f\[\]=clash-display@[^"]*"></noscript>',
            f'<noscript><link rel="stylesheet" href="{NEW_FONTSHARE_URL}"></noscript>\n<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@800&display=swap"></noscript>',
            content
        )
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            total += 1

print(f'Updated font loading in {total} HTML files')

# Verify
remaining = 0
for root, dirs, files in os.walk(PROJECT):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules')]
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r') as f:
            c = f.read()
        if 'clash-display' in c:
            remaining += 1
            rel = os.path.relpath(fpath, PROJECT)
            print(f'  STILL HAS clash-display: {rel}')

print(f'\nFiles still referencing Clash Display: {remaining}')

# Count JetBrains Mono additions
jb_count = 0
for root, dirs, files in os.walk(PROJECT):
    dirs[:] = [d for d in dirs if d not in ('.git', 'node_modules')]
    for fname in files:
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r') as f:
            c = f.read()
        if 'JetBrains' in c:
            jb_count += 1

print(f'Files with JetBrains Mono: {jb_count}')
