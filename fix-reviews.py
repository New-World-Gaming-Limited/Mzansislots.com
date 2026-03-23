#!/usr/bin/env python3
"""
Fix all review pages:
1. Remove square bracket citation links [text](url)
2. Fix double tick/cross markers in pros/cons (CSS marker + text symbol)
3. Update exit links from BrandBonus MCP
4. Use MCP base_colour and text_colour for brand backgrounds
5. Add operator screenshots where available
"""
import re
import os
import json
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
REVIEWS_DIR = os.path.join(BASE, 'reviews')

# Load MCP operator data
with open('/home/user/workspace/mcp-operator-data.json') as f:
    MCP_DATA = json.load(f)

# Available screenshots
SCREENSHOTS = {}
for f in glob.glob(os.path.join(BASE, 'assets', 'screenshots', '*.jpg')):
    name = os.path.basename(f).replace('.jpg', '')
    # Skip desktop/mobile variants for now, map base name
    if '-desktop' not in name and '-mobile' not in name:
        SCREENSHOTS[name] = f'../assets/screenshots/{os.path.basename(f)}'

# Easybet has special desktop/mobile screenshots
SCREENSHOTS['easybet-desktop'] = '../assets/screenshots/easybet-desktop.jpg'
SCREENSHOTS['easybet-mobile'] = '../assets/screenshots/easybet-mobile.jpg'


def remove_bracket_links(html):
    """Remove [text](url) citation patterns from HTML content."""
    # Pattern 1: [text](url) - markdown-style links in HTML
    html = re.sub(r'\[([^\]]*)\]\(https?://[^)]+\)', '', html)
    
    # Pattern 2: [text](url) with line breaks
    html = re.sub(r'\[([^\]]*)\]\(https?://[^\)]+\)', '', html)
    
    # Pattern 3: Leftover [text] without URL
    # Only remove if it looks like a citation (contains common citation words)
    # Don't remove [data-theme] or similar CSS/JS patterns
    
    # Clean up resulting double commas, leading commas etc
    html = re.sub(r',\s*,', ',', html)
    html = re.sub(r',\s*\.', '.', html)
    html = re.sub(r'\.\s*,', '.', html)
    html = re.sub(r'<p>\s*,\s*', '<p>', html)
    html = re.sub(r',\s*</p>', '</p>', html)
    html = re.sub(r'<p>\s*</p>', '', html)
    
    # Clean up leftover whitespace issues
    html = re.sub(r'  +', ' ', html)
    
    return html


def fix_double_markers(html):
    """Remove duplicate tick/cross symbols that appear alongside CSS ::marker."""
    # CSS already adds checkmark via ::marker. Remove text-based ones.
    # Pattern: li text starting with tick/cross symbols
    html = re.sub(r'(<li>)\s*[✔✓✅]\s*', r'\1', html)
    html = re.sub(r'(<li>)\s*[✗✘❌]\s*', r'\1', html)
    # Also handle unicode variants
    html = re.sub(r'(<li>)\s*&#x2713;\s*', r'\1', html)
    html = re.sub(r'(<li>)\s*&#x2717;\s*', r'\1', html)
    
    return html


def update_exit_links(html, slug):
    """Replace old exit links with MCP-provided ones."""
    if slug not in MCP_DATA:
        return html
    
    data = MCP_DATA[slug]
    new_url = data['exit_url']
    
    if not new_url:
        return html
    
    # Replace all mzansiwins affiliate links for this operator
    # The existing links are like: https://www.mzansiwins.co.za/link/XXXXX/
    html = re.sub(
        r'href="https://www\.mzansiwins\.co\.za/link/[^"]*"',
        f'href="{new_url}"',
        html
    )
    
    return html


def update_brand_colours(html, slug):
    """Update brand background and text colours from MCP data."""
    if slug not in MCP_DATA:
        return html
    
    data = MCP_DATA[slug]
    base = data['base_colour']
    text = data['text_colour']
    
    if not base:
        return html
    
    # Update inline style backgrounds on brand-related elements
    # Pattern: style="background:#XXXXXX;" or style="background: #XXXXXX;"
    # Be careful to only update brand-specific backgrounds, not all backgrounds
    
    # Update hero/header backgrounds
    html = re.sub(
        r'(class="review-hero"[^>]*style="[^"]*background:\s*)#[0-9a-fA-F]{3,6}',
        lambda m: m.group(1) + base,
        html
    )
    
    # Update brand logo backgrounds
    html = re.sub(
        r'(class="brand-card-logo"[^>]*style="[^"]*background:\s*)#[0-9a-fA-F]{3,6}',
        lambda m: m.group(1) + base,
        html
    )
    
    # Update CTA button colours
    html = re.sub(
        r'(class="cta-btn"[^>]*style="[^"]*background:\s*)#[0-9a-fA-F]{3,6}',
        lambda m: m.group(1) + base,
        html
    )
    
    # Update inline style with both background and color for CTA buttons
    html = re.sub(
        r'(style="[^"]*background:\s*)#[0-9a-fA-F]{3,6}([^"]*color:\s*)#[0-9a-fA-F]{3,6}',
        lambda m: m.group(1) + base + m.group(2) + text,
        html
    )
    
    return html


def add_screenshots_section(html, slug):
    """Add operator screenshots section to the review if screenshots exist."""
    # Check for available screenshots
    screenshots = []
    if f'{slug}-desktop' in SCREENSHOTS:
        screenshots.append(('Desktop', SCREENSHOTS[f'{slug}-desktop']))
    if f'{slug}-mobile' in SCREENSHOTS:
        screenshots.append(('Mobile', SCREENSHOTS[f'{slug}-mobile']))
    if not screenshots and slug in SCREENSHOTS:
        screenshots.append(('Homepage', SCREENSHOTS[slug]))
    
    if not screenshots:
        return html
    
    # Don't add if already has screenshots section
    if 'operator-screenshots' in html or 'site-screenshots' in html:
        return html
    
    # Build screenshot section HTML
    imgs_html = ''
    for label, src in screenshots:
        imgs_html += f'''
        <figure class="screenshot-figure">
          <img src="{src}" alt="{MCP_DATA.get(slug, {}).get('name', slug)} {label}" loading="lazy" class="screenshot-img">
          <figcaption>{label} view</figcaption>
        </figure>'''
    
    screenshot_section = f'''
  <div class="site-screenshots">
    <h3>What the Site Looks Like</h3>
    <div class="screenshot-grid">
      {imgs_html}
    </div>
  </div>
'''
    
    # Insert before the pros-cons section
    insert_point = html.find('<div class="pros-cons">')
    if insert_point == -1:
        # Try before CTA section
        insert_point = html.find('<div class="cta-section">')
    
    if insert_point != -1:
        html = html[:insert_point] + screenshot_section + '\n  ' + html[insert_point:]
    
    return html


def process_review(filepath):
    """Process a single review file."""
    slug = os.path.basename(filepath).replace('.html', '')
    
    # Skip index page
    if slug == 'index':
        return False
    
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    original = html
    
    # 1. Remove square bracket citation links
    html = remove_bracket_links(html)
    
    # 2. Fix double tick/cross markers
    html = fix_double_markers(html)
    
    # 3. Update exit links from MCP
    html = update_exit_links(html, slug)
    
    # 4. Update brand colours from MCP
    html = update_brand_colours(html, slug)
    
    # 5. Add screenshots
    html = add_screenshots_section(html, slug)
    
    if html == original:
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return True


def main():
    count = 0
    for filepath in sorted(glob.glob(os.path.join(REVIEWS_DIR, '*.html'))):
        if process_review(filepath):
            name = os.path.basename(filepath)
            print(f'  {name}')
            count += 1
    
    print(f'\nFixed {count} review pages.')


if __name__ == '__main__':
    main()
