#!/usr/bin/env python3
"""
Rebuild all 168 game pages with:
1. Inline SlotsLaunch iframe (instant play, no click-to-play)
2. Cross-linking: More from [Provider], Similar [Theme] Slots, Popular Slots
3. Fixed button alignment and sizing
4. Better mobile UX
"""

import json
import os
import re
import random
from pathlib import Path

ROOT = Path("/home/user/workspace/mzansislots")
SLOTS_DIR = ROOT / "slots"

# ── Load data ──────────────────────────────────────────────────
with open(ROOT / "games-enriched.json") as f:
    ALL_GAMES = json.load(f)

with open(ROOT / "slotslaunch-all-games.json") as f:
    SL_GAMES = json.load(f)

with open(ROOT / "operators-data.json") as f:
    OPERATORS = json.load(f)

# Build lookups
SL_BY_SLUG = {g["slug"]: g for g in SL_GAMES}
GAMES_BY_SLUG = {g["slug"]: g for g in ALL_GAMES}

# Provider → operator mapping
PROVIDER_OPERATORS = {
    "Amusnet": ["Hollywoodbets", "Easybet", "Gbets", "Goldrush", "Playbet"],
    "Aviatrix": ["Hollywoodbets", "Easybet", "Supabets", "Betfred", "BetXChange"],
    "Betsoft": ["Wanejo Bets", "Play Live Casino"],
    "BGaming": ["JackpotCity", "Goldrush"],
    "Booming Games": ["Easybet", "BetXChange", "Playbet"],
    "Endorphina": ["Supabets"],
    "Hacksaw Gaming": ["Betway"],
    "Play'n GO": ["Betway", "Goldrush", "PlayOJO"],
    "Pragmatic Play": ["Hollywoodbets", "Supabets", "Easybet", "BetXChange", "SuperSportBet"],
    "Red Tiger Gaming": ["Betway", "SuperSportBet"],
    "Spinomenal": ["Hollywoodbets", "JackpotCity", "Betfred", "Goldrush"],
    "Wazdan": ["Easybet", "BetXChange", "Betta Bets"],
    "Spribe": ["Betway", "Hollywoodbets", "SuperSportBet"],
    "Habanero": ["Hollywoodbets", "Supabets", "Easybet"],
    "Playtech": ["Betway"],
}

# Theme category mapping (for grouping similar themes)
THEME_CATEGORIES = {
    "Seasonal": ["Christmas", "Easter", "Halloween", "St. Patrick's Day", "Valentine's Day", "Oktoberfest"],
    "Mythology": ["Gods", "Zeus", "Egyptian", "Cleopatra", "Roman", "Viking", "Aztec", "Mayan"],
    "Animals": ["Animal", "Buffalo", "Cat", "Fish", "Horse", "Lion", "Monkey", "Panda", "Phoenix", "Pig", "Tiger", "Wolf", "Dragon", "Aquatic", "Ocean"],
    "Adventure": ["Adventure", "Pirate", "Treasure", "Heist", "Wild West", "Jungle", "Space", "Mining"],
    "Classic": ["Classic", "Fruit", "Sevens", "Diamond", "Gem", "Jewel", "Gold", "Money", "Vegas", "Star", "Bell", "Joker"],
    "Fantasy": ["Fantasy", "Magic", "Mystery", "Princess", "Moon", "Horror", "Monster"],
    "Culture": ["Asian", "Irish", "Leprechaun", "Mexican", "Tiki", "Mahjong", "Day of the Dead", "Carnival"],
    "Food": ["Food", "Candy", "Sweets"],
    "Nature": ["Nature", "Farm"],
}

# Build reverse: theme → category
THEME_TO_CATEGORY = {}
for cat, themes in THEME_CATEGORIES.items():
    for t in themes:
        THEME_TO_CATEGORY[t.lower()] = cat

# Provider logo map
PROVIDER_LOGOS = {
    "Pragmatic Play": "pragmatic-play.png",
    "Amusnet": "amusnet.png",
    "BGaming": "bgaming.png",
    "Endorphina": "endorphina.png",
    "Wazdan": "wazdan.png",
    "Spinomenal": "spinomenal.png",
    "Hacksaw Gaming": "hacksaw-gaming.jpg",
    "Habanero": "greentube.png",
    "Play'n GO": "play-n-go.jpg",
    "Betsoft": "betsoft.png",
    "Booming Games": "booming-games.png",
    "Red Tiger Gaming": "red-tiger-gaming.png",
    "Spribe": "spribe.png",
    "Aviatrix": "aviatrix.png",
}

# Provider page slugs
PROVIDER_PAGES = {
    "Pragmatic Play": "pragmatic-play.html",
    "Amusnet": "amusnet.html",
    "BGaming": "bgaming.html",
    "Endorphina": "endorphina.html",
    "Wazdan": "wazdan.html",
    "Spinomenal": "spinomenal.html",
    "Hacksaw Gaming": "hacksaw-gaming.html",
    "Habanero": "habanero.html",
    "Play'n GO": "play-n-go.html",
    "Betsoft": "betsoft.html",
    "Booming Games": "booming-games.html",
    "Red Tiger Gaming": "red-tiger-gaming.html",
    "Spribe": "spribe.html",
    "Aviatrix": "aviatrix.html",
    "Playtech": "playtech.html",
    "Lekka Slots": "lekka-slots.html",
    "Unknown": "slot-games.html",
}

# "Popular" slots — curated list of high-traffic games
POPULAR_SLUGS = [
    "sweet-bonanza", "gates-of-olympus", "big-bass-bonanza", "wolf-gold",
    "sugar-rush", "starlight-princess", "the-dog-house", "buffalo-king-megaways",
    "book-of-dead", "wanted-dead-or-a-wild", "fire-joker", "sweet-bonanza-1000",
    "gates-of-olympus-1000", "sugar-rush-1000", "big-bass-splash",
    "wild-west-gold", "fruit-party", "gems-bonanza", "spaceman",
    "le-bandit", "bonanza-billion", "book-of-rebirth", "shining-crown",
    "aviator", "40-super-hot", "100-super-hot", "bigger-bass-bonanza",
    "joker-s-jewels", "hot-to-burn", "chilli-heat",
]

TOKEN = "uTgDOO6eTBjzYawnyR1sRaMYyZ6ZJhOGRCzfqoq0W7NXhqiuQX"

def safe_theme(game):
    """Get theme string, handling None."""
    t = game.get("theme")
    return t if t else ""

def get_theme_category(theme):
    """Get the broad theme category for a game's theme."""
    if not theme:
        return None
    return THEME_TO_CATEGORY.get(theme.lower(), None)

def get_thumbnail(game):
    """Get thumbnail URL for a game."""
    slug = game["slug"]
    # Check SlotsLaunch first
    if slug in SL_BY_SLUG and SL_BY_SLUG[slug].get("thumb"):
        return SL_BY_SLUG[slug]["thumb"]
    # Check enriched data
    if game.get("thumb"):
        return game["thumb"]
    return None

def get_iframe_id(slug):
    """Extract iframe ID from SlotsLaunch URL."""
    if slug in SL_BY_SLUG:
        url = SL_BY_SLUG[slug].get("url", "")
        if url:
            match = re.search(r'/iframe/(\d+)', url)
            if match:
                return match.group(1)
    return None

def build_game_card_html(game, prefix=""):
    """Build a cross-link game card HTML."""
    slug = game["slug"]
    thumb = get_thumbnail(game)
    title = game["title"]
    rtp = game.get("rtp", "")
    provider = game.get("provider", "")
    
    # Use a placeholder gradient if no thumbnail
    if thumb:
        img_html = f'<img src="{thumb}" alt="{title}" loading="lazy">'
    else:
        img_html = f'<div class="xlink-card-placeholder"><span>{title[:2].upper()}</span></div>'
    
    rtp_html = f'<span class="xlink-card-rtp">{rtp} RTP</span>' if rtp else ''
    
    return f'''<a href="{prefix}{slug}.html" class="xlink-card">
              {img_html}
              <div class="xlink-card-info">
                <div class="xlink-card-name">{title}</div>
                {rtp_html}
              </div>
            </a>'''

def build_provider_section(current_game):
    """Build 'More from [Provider]' section."""
    provider = current_game["provider"]
    if provider in ("Unknown",):
        return ""
    
    same_provider = [g for g in ALL_GAMES 
                     if g["provider"] == provider 
                     and g["slug"] != current_game["slug"]]
    
    if len(same_provider) < 2:
        return ""
    
    # Sort by those with thumbnails first, then random
    random.shuffle(same_provider)
    same_provider.sort(key=lambda g: (0 if get_thumbnail(g) else 1))
    
    cards = same_provider[:6]
    provider_logo = PROVIDER_LOGOS.get(provider, "")
    provider_page = PROVIDER_PAGES.get(provider, "slot-games.html")
    
    logo_img = ""
    if provider_logo:
        logo_img = f'<img src="../assets/providers/{provider_logo}" alt="{provider}" class="xlink-section-logo">'
    
    cards_html = "\n            ".join(build_game_card_html(g, "") for g in cards)
    
    return f'''<div class="xlink-section">
        <div class="xlink-section-header">
          <h3>{logo_img}More from {provider}</h3>
          <a href="../{provider_page}" class="xlink-see-all">View all {provider} slots &rarr;</a>
        </div>
        <div class="xlink-grid">
            {cards_html}
        </div>
      </div>'''

def build_theme_section(current_game):
    """Build 'Similar [Theme] Slots' section."""
    theme = safe_theme(current_game)
    if not theme:
        return ""
    
    category = get_theme_category(theme)
    if not category:
        # Try direct theme match
        same_theme = [g for g in ALL_GAMES 
                      if safe_theme(g) == theme
                      and g["slug"] != current_game["slug"]]
    else:
        # Get all themes in this category
        cat_themes = [t.lower() for t in THEME_CATEGORIES.get(category, [])]
        same_theme = [g for g in ALL_GAMES
                      if safe_theme(g).lower() in cat_themes
                      and g["slug"] != current_game["slug"]]
    
    if len(same_theme) < 2:
        return ""
    
    random.shuffle(same_theme)
    same_theme.sort(key=lambda g: (0 if get_thumbnail(g) else 1))
    
    cards = same_theme[:6]
    label = category if category else theme
    
    # Theme emoji/icon
    THEME_ICONS = {
        "Animals": "🦁", "Mythology": "⚡", "Adventure": "🗺️",
        "Classic": "🎰", "Fantasy": "🔮", "Culture": "🌍",
        "Food": "🍬", "Nature": "🌿", "Seasonal": "🎄",
    }
    icon = THEME_ICONS.get(label, "🎲")
    
    cards_html = "\n            ".join(build_game_card_html(g, "") for g in cards)
    
    return f'''<div class="xlink-section">
        <div class="xlink-section-header">
          <h3>{icon} Similar {label} Slots</h3>
          <a href="../slot-games.html" class="xlink-see-all">Browse all slots &rarr;</a>
        </div>
        <div class="xlink-grid">
            {cards_html}
        </div>
      </div>'''

def build_popular_section(current_game):
    """Build 'Popular Slots' section."""
    popular = [GAMES_BY_SLUG[s] for s in POPULAR_SLUGS 
               if s in GAMES_BY_SLUG and s != current_game["slug"]]
    
    # Pick 6 random from popular
    random.seed(hash(current_game["slug"]))  # Deterministic per page
    selected = random.sample(popular, min(6, len(popular)))
    
    cards_html = "\n            ".join(build_game_card_html(g, "") for g in selected)
    
    return f'''<div class="xlink-section">
        <div class="xlink-section-header">
          <h3>🔥 Popular Slots</h3>
          <a href="../slot-games.html" class="xlink-see-all">View all slots &rarr;</a>
        </div>
        <div class="xlink-grid">
            {cards_html}
        </div>
      </div>'''

def build_cross_links_html(current_game):
    """Build the full cross-linking section."""
    provider_section = build_provider_section(current_game)
    theme_section = build_theme_section(current_game)
    popular_section = build_popular_section(current_game)
    
    sections = [s for s in [provider_section, theme_section, popular_section] if s]
    
    if not sections:
        return ""
    
    return f'''<!-- ═══ CROSS-LINKS ═══ -->
<section class="xlink-container">
  <div class="container">
    {"".join(sections)}
  </div>
</section>'''

def build_inline_demo_html(game):
    """Build inline demo iframe section (instant play)."""
    slug = game["slug"]
    title = game["title"]
    iframe_id = get_iframe_id(slug)
    thumb = get_thumbnail(game)
    
    if iframe_id:
        # Has SlotsLaunch iframe — show inline with instant play option
        iframe_url = f"https://slotslaunch.com/iframe/{iframe_id}?token={TOKEN}"
        thumb_url = thumb if thumb else ""
        
        if thumb_url:
            placeholder_img = f'<img src="{thumb_url}" alt="{title}" class="demo-placeholder-img" loading="eager">'
        else:
            placeholder_img = ''
        
        return f'''<!-- ═══ DEMO IFRAME ═══ -->
<section class="game-demo-section">
  <div class="container">
    <div class="game-demo-wrapper">
      <div class="game-demo-frame" id="demoFrame">
        <div class="demo-placeholder" id="demoPlaceholder">
          {placeholder_img}
          <div class="demo-overlay">
            <button class="demo-play-btn" id="launchDemo" aria-label="Launch {title} demo">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
              <span>Play Free Demo</span>
            </button>
            <p class="demo-note">Free play — no registration required</p>
          </div>
        </div>
        <iframe id="gameIframe" style="display:none;" width="100%" height="100%" src="" frameborder="0" allowfullscreen allow="autoplay; fullscreen"></iframe>
      </div>
    </div>
  </div>
</section>''', iframe_url
    else:
        # No SlotsLaunch iframe — show thumbnail with "where to play" prompt
        if thumb:
            return f'''<!-- ═══ GAME PREVIEW ═══ -->
<section class="game-demo-section">
  <div class="container">
    <div class="game-demo-wrapper">
      <div class="game-demo-frame game-demo-preview">
        <img src="{thumb}" alt="{title}" class="demo-preview-img" loading="eager">
        <div class="demo-overlay demo-overlay-noplay">
          <p class="demo-preview-text">Demo not available — play for real at a licensed SA casino below</p>
        </div>
      </div>
    </div>
  </div>
</section>''', None
        else:
            return f'''<!-- ═══ GAME PREVIEW ═══ -->
<section class="game-demo-section">
  <div class="container">
    <div class="game-demo-wrapper">
      <div class="game-demo-frame game-demo-preview game-demo-nothumb">
        <div class="demo-overlay demo-overlay-noplay">
          <div class="demo-game-icon">🎰</div>
          <p class="demo-preview-text">Play {title} for real at a licensed SA casino below</p>
        </div>
      </div>
    </div>
  </div>
</section>''', None

def build_demo_script(iframe_url):
    """Build the demo launch script."""
    if iframe_url:
        return f'''<script>
// Demo launch — instant play
document.getElementById('launchDemo').addEventListener('click', function() {{
  const iframe = document.getElementById('gameIframe');
  const placeholder = document.getElementById('demoPlaceholder');
  iframe.src = '{iframe_url}';
  iframe.style.display = 'block';
  placeholder.style.display = 'none';
}});
</script>'''
    return ""

def process_game_page(filepath, game):
    """Process a single game page HTML file."""
    with open(filepath, 'r') as f:
        html = f.read()
    
    # ── 1. Replace demo section ──
    demo_html, iframe_url = build_inline_demo_html(game)
    
    # Try to replace commented demo section first
    replaced = False
    for pattern in [
        r'<!-- ═══ DEMO IFRAME ═══ -->.*?</section>',
        r'<!-- ═══ GAME PREVIEW ═══ -->.*?</section>',
    ]:
        new_html = re.sub(pattern, demo_html, html, flags=re.DOTALL, count=1)
        if new_html != html:
            html = new_html
            replaced = True
            break
    
    # If no commented section found, replace the game-demo-section directly
    if not replaced:
        html = re.sub(
            r'<section class="game-demo-section">.*?</section>',
            demo_html,
            html, flags=re.DOTALL, count=1
        )
    
    # ── 2. Replace demo script ──
    # Remove old demo script
    html = re.sub(
        r'<script>\s*\n?// Demo launch.*?</script>',
        build_demo_script(iframe_url),
        html, flags=re.DOTALL, count=1
    )
    
    # ── 3. Replace related games section with cross-links ──
    cross_links_html = build_cross_links_html(game)
    
    # Remove existing related games section by finding matched div depth
    section_search = '<div class="related-games-section">'
    if section_search in html:
        # Find the start - might have a comment before it
        section_start = html.index(section_search)
        # Check if preceded by <!-- Related Games --> comment
        preceding = html[:section_start].rstrip()
        if preceding.endswith('<!-- Related Games -->'):
            start = preceding.rindex('<!-- Related Games -->')
        else:
            start = section_start
        
        # Find matching closing div
        depth = 0
        pos = section_start
        end = len(html)
        while pos < len(html):
            if html[pos:pos+4] == '<div':
                depth += 1
            elif html[pos:pos+6] == '</div>':
                depth -= 1
                if depth == 0:
                    end = pos + 6
                    break
            pos += 1
        html = html[:start].rstrip() + html[end:]
    
    # Remove any existing cross-links section
    html = re.sub(
        r'<!-- ═══ CROSS-LINKS ═══ -->.*?</section>\s*',
        '',
        html, flags=re.DOTALL
    )
    
    # Insert cross-links before closing CTA
    if cross_links_html:
        if '<!-- ═══ CLOSING CTA ═══ -->' in html:
            html = html.replace(
                '<!-- ═══ CLOSING CTA ═══ -->',
                f'{cross_links_html}\n\n<!-- ═══ CLOSING CTA ═══ -->'
            )
        elif '<section class="closing-cta">' in html:
            html = html.replace(
                '<section class="closing-cta">',
                f'{cross_links_html}\n\n<section class="closing-cta">'
            )
        else:
            # Insert before footer as fallback
            html = html.replace(
                '<footer class="site-footer">',
                f'{cross_links_html}\n\n<footer class="site-footer">'
            )
    
    # ── 4. Fix button sizing — ensure all GET OFFER buttons have consistent class ──
    # Normalize btn classes on casino table buttons
    html = re.sub(
        r'class="btn btn-primary btn-sm"',
        'class="btn btn-primary btn-table"',
        html
    )
    
    # ── 5. Make closing CTA button consistent ──
    html = re.sub(
        r'class="btn btn-primary btn-lg"',
        'class="btn btn-primary btn-cta"',
        html
    )
    
    with open(filepath, 'w') as f:
        f.write(html)

def main():
    random.seed(42)  # Deterministic output
    
    processed = 0
    errors = []
    
    for game in ALL_GAMES:
        slug = game["slug"]
        filepath = SLOTS_DIR / f"{slug}.html"
        
        if not filepath.exists():
            errors.append(f"Missing: {slug}.html")
            continue
        
        try:
            process_game_page(filepath, game)
            processed += 1
        except Exception as e:
            errors.append(f"Error on {slug}: {e}")
    
    print(f"Processed: {processed} game pages")
    if errors:
        print(f"Errors ({len(errors)}):")
        for e in errors:
            print(f"  {e}")

if __name__ == "__main__":
    main()
