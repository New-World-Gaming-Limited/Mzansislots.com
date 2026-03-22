#!/usr/bin/env python3
"""
Fix desktop nav (reduce to essentials + hamburger for secondary) and
casino tables (bigger logos, better alignment, remove fluff).
"""
import re
import glob
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_nav_prefix(filepath):
    """Return ../ for subdir pages, empty for root pages."""
    rel = os.path.relpath(filepath, BASE_DIR)
    depth = rel.count(os.sep)
    if depth == 0:
        return ""
    return "../" * depth

def build_new_nav(prefix):
    """Build the new slimmed-down nav HTML."""
    return f'''      <nav>
        <ul class="nav-desktop">
          <li><a href="{prefix}slot-games.html">Free Slots</a></li>
          <li><a href="{prefix}best-slot-sites.html">Best Sites</a></li>
          <li><a href="{prefix}reviews/index.html">Reviews</a></li>
          <li><a href="{prefix}promo-codes/index.html">Promos</a></li>
        </ul>
      </nav>
      <div class="header-actions">
        <button class="theme-toggle" data-theme-toggle aria-label="Toggle dark/light mode">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
        <button class="hamburger-toggle" aria-label="Open menu" aria-expanded="false">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
        </button>
      </div>
    </div>
    <nav class="slide-menu" id="slideMenu">
      <div class="slide-menu-header">
        <span class="slide-menu-title">Menu</span>
        <button class="slide-menu-close" aria-label="Close menu">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
      </div>
      <div class="slide-menu-section">
        <span class="slide-menu-label">Browse</span>
        <a href="{prefix}slot-games.html">Free Slots</a>
        <a href="{prefix}best-slot-sites.html">Best Slots Sites</a>
        <a href="{prefix}lekka-slots.html">Lekka Slots</a>
        <a href="{prefix}spina-zonke.html">Spina Zonke</a>
      </div>
      <div class="slide-menu-section">
        <span class="slide-menu-label">Game Studios</span>
        <a href="{prefix}pragmatic-play.html">Pragmatic Play</a>
        <a href="{prefix}play-n-go.html">Play'n GO</a>
        <a href="{prefix}red-tiger-gaming.html">Red Tiger</a>
        <a href="{prefix}hacksaw-gaming.html">Hacksaw Gaming</a>
        <a href="{prefix}bgaming.html">BGaming</a>
        <a href="{prefix}betsoft.html">Betsoft</a>
        <a href="{prefix}booming-games.html">Booming Games</a>
        <a href="{prefix}endorphina.html">Endorphina</a>
        <a href="{prefix}habanero.html">Habanero</a>
        <a href="{prefix}spinomenal.html">Spinomenal</a>
        <a href="{prefix}wazdan.html">Wazdan</a>
        <a href="{prefix}spribe.html">Spribe</a>
        <a href="{prefix}amusnet.html">Amusnet</a>
        <a href="{prefix}aviatrix.html">Aviatrix</a>
      </div>
      <div class="slide-menu-section">
        <span class="slide-menu-label">Resources</span>
        <a href="{prefix}reviews/index.html">Casino Reviews</a>
        <a href="{prefix}promo-codes/index.html">Promo Codes</a>
        <a href="{prefix}news.html">News &amp; Guides</a>
        <a href="{prefix}about.html">About</a>
      </div>
    </nav>
    <div class="slide-menu-overlay" id="slideOverlay"></div>
  </div>
</header>'''


def replace_nav(html, filepath):
    """Replace the entire nav section from <nav> through </header>."""
    prefix = get_nav_prefix(filepath)
    
    # Find the start of <nav> inside the header
    nav_start = html.find('<nav>')
    if nav_start == -1:
        nav_start = html.find('<nav ')
    if nav_start == -1:
        return html
    
    # Find the end of </header>
    header_end = html.find('</header>')
    if header_end == -1:
        return html
    header_end += len('</header>')
    
    # We want to replace from <nav> to </header>
    new_nav = build_new_nav(prefix)
    html = html[:nav_start] + new_nav + html[header_end:]
    
    return html


def fix_casino_table_css_classes(html):
    """
    Fix casino table: make logos bigger, improve layout.
    We'll just adjust CSS classes - the main styling is done in CSS.
    """
    # Make casino-brand-logo bigger by adding a wrapper class
    # Replace the old 44px logos with the improved class
    html = html.replace('class="casino-brand-logo"', 'class="casino-brand-logo casino-logo-lg"')
    
    return html


def process_file(filepath):
    """Process a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Skip if already processed
    if 'slide-menu' in html:
        return False
    
    # Must have a header to process
    if '<header' not in html:
        return False
    
    original = html
    
    # 1. Replace nav
    html = replace_nav(html, filepath)
    
    # 2. Fix table logos
    html = fix_casino_table_css_classes(html)
    
    if html == original:
        return False
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return True


def main():
    count = 0
    
    # Process all HTML files
    patterns = [
        os.path.join(BASE_DIR, '*.html'),
        os.path.join(BASE_DIR, 'slots', '*.html'),
        os.path.join(BASE_DIR, 'reviews', '*.html'),
        os.path.join(BASE_DIR, 'promo-codes', '*.html'),
        os.path.join(BASE_DIR, 'news', '*.html'),
    ]
    
    all_files = []
    for pattern in patterns:
        all_files.extend(glob.glob(pattern))
    
    for filepath in sorted(set(all_files)):
        if process_file(filepath):
            count += 1
            name = os.path.relpath(filepath, BASE_DIR)
            # Only print first few and last few
            if count <= 5 or count % 50 == 0:
                print(f"  {name}")
    
    print(f"\nDone! Modified {count} files.")


if __name__ == '__main__':
    main()
