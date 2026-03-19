#!/usr/bin/env python3
"""
Comprehensive content hub restructure for MzansiSlots:
1. Move 5 Lekka Slots reviews into /slots/ with updated paths
2. Create 12 Spina Zonke game pages in /slots/ (no demo iframe)
3. Add clickable provider/category tags to ALL game pages
4. Update hub pages (pragmatic-play, spina-zonke, lekka-slots) to link into /slots/
5. Update all internal links across the site
"""
import os
import re
import json
import shutil

ROOT = '/home/user/workspace/mzansislots'
SLOTS_DIR = os.path.join(ROOT, 'slots')

# ═══════════════════════════════════════════════════════════════
# 1. MOVE LEKKA SLOTS REVIEWS INTO /slots/
# ═══════════════════════════════════════════════════════════════

REVIEW_FILES = [
    'babalas-review.html',
    'liefde-review.html',
    'isibaya-queens-review.html',
    'jack-parow-review.html',
    'amakhosi-cash-review.html',
]

for fname in REVIEW_FILES:
    src = os.path.join(ROOT, fname)
    dst = os.path.join(SLOTS_DIR, fname)
    if not os.path.exists(src):
        print(f"⚠️  Source not found: {src}")
        continue
    
    with open(src, 'r') as f:
        content = f.read()
    
    # Fix CSS paths: href="base.css" → href="../base.css"
    content = content.replace('href="base.css"', 'href="../base.css"')
    content = content.replace('href="style.css"', 'href="../style.css"')
    
    # Fix nav links: href="index.html" → href="../index.html" etc.
    root_pages = ['index.html', 'best-slot-sites.html', 'slot-games.html', 
                  'lekka-slots.html', 'pragmatic-play.html', 'spina-zonke.html', 'news.html']
    for page in root_pages:
        content = content.replace(f'href="{page}"', f'href="../{page}"')
    
    # Fix asset paths: src="assets/ → src="../assets/
    content = content.replace('src="assets/', 'src="../assets/')
    
    # Fix JS paths: src="hero-bg-inject.js" → src="../hero-bg-inject.js"
    content = content.replace('src="hero-bg-inject.js"', 'src="../hero-bg-inject.js"')
    content = content.replace('src="shared.js"', 'src="../shared.js"')
    
    # Fix inter-review links: href="babalas-review.html" → href="babalas-review.html" (stays same since both in /slots/)
    # These are already correct relative paths within /slots/
    
    # Fix footer logo link
    content = content.replace('<a href="index.html" class="logo">', '<a href="../index.html" class="logo">')
    
    # Add provider/category tags to review pages
    # Find the provider in the review meta
    provider_match = re.search(r'<div class="review-meta-label">Provider</div>\s*<div class="review-meta-value">([^<]+)</div>', content)
    provider_name = provider_match.group(1) if provider_match else ""
    
    # Add clickable tags after the breadcrumb (before h1)
    # We'll add a tags section right after the breadcrumb div
    if '<div class="breadcrumb">' in content:
        # Add tag links after the breadcrumb
        tags_html = '<div class="game-header-tags" style="margin-top: var(--space-2); margin-bottom: var(--space-2);">'
        tags_html += '<a href="../lekka-slots.html" class="game-provider-tag game-tag-link">Lekka Slots</a>'
        if provider_name:
            tags_html += f'<span class="game-feature-tag tag-provider-label">{provider_name}</span>'
        tags_html += '</div>'
        
        # Insert after the breadcrumb closing
        content = content.replace(
            '</div>\n        <h1>',
            f'</div>\n        {tags_html}\n        <h1>'
        )
    
    # Write to slots directory
    with open(dst, 'w') as f:
        f.write(content)
    
    # Remove old file from root
    os.remove(src)
    print(f"✅ Moved: {fname} → slots/{fname}")


# ═══════════════════════════════════════════════════════════════
# 2. CREATE SPINA ZONKE GAME PAGES IN /slots/
# ═══════════════════════════════════════════════════════════════

SPINA_ZONKE_GAMES = [
    {
        "name": "Hot Hot Fruit",
        "slug": "hot-hot-fruit",
        "provider": "Habanero",
        "rtp": "96.70",
        "volatility": "Medium",
        "reels": "5",
        "paylines": "27",
        "max_win": "2,000x",
        "description": "Hot Hot Fruit is a vibrant, retro-styled slot from Habanero that's become a staple on the Spina Zonke platform. With a classic fruit machine feel updated for the modern era, this 5-reel game delivers sizzling wins through its respin feature — landing a full stack of the same fruit on any reel triggers respins where that symbol becomes sticky. The lively visuals and upbeat soundtrack make every session feel like a lekka time, while the 96.70% RTP and medium volatility keep the balance ticking over nicely for South African players who prefer steady action over feast-or-famine swings.",
        "emoji": "🍒"
    },
    {
        "name": "Mystic Fortune Deluxe",
        "slug": "mystic-fortune-deluxe",
        "provider": "Habanero",
        "rtp": "96.61",
        "volatility": "High",
        "reels": "5",
        "paylines": "25",
        "max_win": "15,800x",
        "description": "Mystic Fortune Deluxe transports Spina Zonke players into an enchanted Asian temple filled with mystical symbols and golden treasures. Habanero has packed this slot with a powerful free spins feature that includes expanding wilds and multipliers that grow with each cascade. The high volatility means you might need patience between big hits, but when the fortune symbols align, the results can be spectacular. South African players appreciate the 96.61% RTP and the elegant design that sets it apart from the typical fruit machine fare.",
        "emoji": "🔮"
    },
    {
        "name": "Hot to Burn",
        "slug": "hot-to-burn",
        "provider": "Pragmatic Play",
        "rtp": "96.70",
        "volatility": "Medium",
        "reels": "5",
        "paylines": "5",
        "max_win": "1,000x",
        "description": "Hot to Burn is Pragmatic Play's tribute to the classic fruit machine, available on Spina Zonke with its simple but satisfying 5-reel, 5-payline layout. No complex bonus rounds or elaborate animations here — just pure, fast-paced spinning with traditional symbols like sevens, bars, bells, and fruits. The flaming wild symbol doubles all wins it helps create, adding a touch of excitement to the classic format. With medium volatility and a 96.70% RTP, this is the perfect choice for SA players who love the no-nonsense approach of old-school slots.",
        "emoji": "🔥"
    },
    {
        "name": "Strike Frenzy",
        "slug": "strike-frenzy",
        "provider": "Habanero",
        "rtp": "96.66",
        "volatility": "Medium-High",
        "reels": "5",
        "paylines": "25",
        "max_win": "4,500x",
        "description": "Strike Frenzy delivers electrifying gameplay on the Spina Zonke platform with its bowling-themed design and chain reaction mechanics. When lightning strikes a winning combination, symbols explode and new ones fall into place, creating cascading wins that can chain multiple times in a single spin. The Frenzy Mode free spins feature ramps up the multipliers with each consecutive cascade. Habanero has crafted a medium-high volatility experience with a 96.66% RTP that keeps South African players coming back for more.",
        "emoji": "⚡"
    },
    {
        "name": "Hot Hot Hollywoodbets",
        "slug": "hot-hot-hollywoodbets",
        "provider": "Habanero",
        "rtp": "96.70",
        "volatility": "Medium",
        "reels": "5",
        "paylines": "27",
        "max_win": "2,000x",
        "description": "Hot Hot Hollywoodbets is the exclusive, branded version of the classic Hot Hot Fruit — made specifically for the Spina Zonke platform. It features the same beloved respin mechanic where stacked symbols trigger sticky respins, but with Hollywoodbets branding and custom colours that make it feel like a uniquely South African experience. With medium volatility and a generous 96.70% RTP, this is the definitive version of the game for SA players. It's consistently one of the most-played titles on the entire Spina Zonke platform.",
        "emoji": "🎰"
    },
    {
        "name": "Joker's Jewels",
        "slug": "jokers-jewels",
        "provider": "Pragmatic Play",
        "rtp": "96.50",
        "volatility": "Medium",
        "reels": "5",
        "paylines": "5",
        "max_win": "1,000x",
        "description": "Joker's Jewels is Pragmatic Play's classic-style slot that sparkles on the Spina Zonke platform. The charming jester character presides over a simple 5-reel, 5-payline layout adorned with colourful gemstones. No wilds, no scatters, no free spins — just straightforward spinning action where matching jewels and jokers deliver crisp payouts. The simplicity is the appeal here, and SA players love it for quick, uncomplicated sessions. The 96.50% RTP and medium volatility make Joker's Jewels a reliable performer for any bankroll.",
        "emoji": "💎"
    },
    {
        "name": "Wealth Inn",
        "slug": "wealth-inn",
        "provider": "Habanero",
        "rtp": "96.72",
        "volatility": "Medium",
        "reels": "3",
        "paylines": "1",
        "max_win": "2,500x",
        "description": "Wealth Inn is Habanero's compact powerhouse on the Spina Zonke platform — a 3-reel, single-payline slot that proves big wins can come in small packages. The Chinese prosperity theme features golden ingots, lucky coins, and a respin bonus that activates when you land partial winning combinations. Despite its traditional 3-reel format, the expanding reels feature during free games opens up the layout for bigger wins. With a 96.72% RTP and medium volatility, Wealth Inn is a favourite among SA players who appreciate classic slot elegance with modern win potential.",
        "emoji": "🏮"
    },
    {
        "name": "Diamond Rise",
        "slug": "diamond-rise",
        "provider": "Habanero",
        "rtp": "96.64",
        "volatility": "Medium-High",
        "reels": "5",
        "paylines": "25",
        "max_win": "5,000x",
        "description": "Diamond Rise glitters on the Spina Zonke platform with its luxurious jewel theme and escalating multiplier system. Each consecutive win in the base game increases the multiplier applied to the next win, creating a rising diamond effect that can lead to impressive payouts. The free spins round takes this further with persistent multipliers that don't reset between spins. Habanero's medium-high volatility design paired with a 96.64% RTP makes Diamond Rise a polished choice for South African players who enjoy the thrill of building momentum.",
        "emoji": "💎"
    },
    {
        "name": "Sahara Riches Cash Collect",
        "slug": "sahara-riches-cash-collect",
        "provider": "Playtech",
        "rtp": "96.36",
        "volatility": "Medium",
        "reels": "5",
        "paylines": "20",
        "max_win": "1,500x",
        "description": "Sahara Riches Cash Collect brings the mysteries of the desert to the Spina Zonke platform, complete with Playtech's innovative Cash Collect mechanic. Land money symbols with cash values and a Cash Collect symbol on the same spin to bank the total. The free spins feature adds sticky money symbols that accumulate across the entire bonus round, building toward substantial combined payouts. With medium volatility and a 96.36% RTP, Sahara Riches offers South African players a well-balanced adventure through golden dunes.",
        "emoji": "🏜️"
    },
    {
        "name": "Sweet Bonanza",
        "slug": "sweet-bonanza-spina-zonke",
        "provider": "Pragmatic Play",
        "rtp": "96.51",
        "volatility": "High",
        "reels": "6",
        "paylines": "Cluster Pays",
        "max_win": "5,000x",
        "description": "Sweet Bonanza is Pragmatic Play's candy-themed smash hit that's taken the Spina Zonke platform by storm. The tumble mechanic cascades winning clusters off the reels while new symbols drop in, creating chain reactions of sweetness. During free spins, random multiplier bombs of up to 100x appear and apply to wins in that round — stack multiple multipliers together for truly massive payouts. With high volatility and a 96.51% RTP, Sweet Bonanza delivers the sugar rush that South African players crave.",
        "emoji": "🍭"
    },
    {
        "name": "Sweet Bonanza 1000",
        "slug": "sweet-bonanza-1000-spina-zonke",
        "provider": "Pragmatic Play",
        "rtp": "96.53",
        "volatility": "Very High",
        "reels": "6",
        "paylines": "Cluster Pays",
        "max_win": "25,000x",
        "description": "Sweet Bonanza 1000 is the supercharged sequel to the original, available on Spina Zonke for SA players who want even more intensity. Everything is amplified — multiplier bombs go up to 1,000x during free spins, and the maximum win has been cranked up to a staggering 25,000x your stake. The very high volatility means this is strictly for players with patience and bankroll to match, but when the multipliers stack up, the results can be life-changing. The 96.53% RTP ensures fair long-term returns for the bravest spinners.",
        "emoji": "🍬"
    },
    {
        "name": "Hollywoodbets SugarTime",
        "slug": "hollywoodbets-sugartime",
        "provider": "Habanero",
        "rtp": "96.68",
        "volatility": "Medium",
        "reels": "5",
        "paylines": "20",
        "max_win": "3,000x",
        "description": "Hollywoodbets SugarTime is another exclusive title crafted by Habanero specifically for the Spina Zonke platform. This candy-coated slot features colourful sweet symbols with a unique Sugar Rush bonus — collect candy symbols to fill a meter that triggers progressively better free spins packages. The Hollywoodbets branding gives it that distinctly South African feel, and the medium volatility paired with 96.68% RTP makes it accessible to players of all budgets. SugarTime has quickly become one of the platform's most popular exclusive titles.",
        "emoji": "🍯"
    }
]

PPLX_HEAD = """<!--
   ______                            __
  / ____/___  ____ ___  ____  __  __/ /____  _____
 / /   / __ \\/ __ `__ \\/ __ \\/ / / / __/ _ \\/ ___/
/ /___/ /_/ / / / / / / /_/ / /_/ / /_/  __/ /
\\____/\\____/_/ /_/ /_/ .___/\\__,_/\\__/\\___/_/
                    /_/
        Created with Perplexity Computer
        https://www.perplexity.ai/computer
-->
<meta name="generator" content="Perplexity Computer">
<meta name="author" content="Perplexity Computer">
<meta property="og:see_also" content="https://www.perplexity.ai/computer">
<link rel="author" href="https://www.perplexity.ai/computer">"""

def create_spina_zonke_page(game):
    """Create a Spina Zonke game page WITHOUT demo iframe — just CTA to Hollywoodbets."""
    name = game['name']
    slug = game['slug']
    provider = game['provider']
    rtp = game['rtp']
    vol = game['volatility']
    reels = game['reels']
    paylines = game['paylines']
    max_win = game['max_win']
    desc = game['description']
    emoji = game['emoji']
    
    # Determine category tags
    tags_html = '<a href="../spina-zonke.html" class="game-provider-tag game-tag-link">Spina Zonke</a>'
    tags_html += f'<span class="game-feature-tag tag-provider-label">{provider}</span>'
    
    # Related Spina Zonke games (exclude self, pick 3)
    related_games = [g for g in SPINA_ZONKE_GAMES if g['slug'] != slug][:3]
    related_cards = ""
    for r in related_games:
        related_cards += f'''
            <a href="{r['slug']}.html" class="related-game-card">
              <div class="related-game-emoji" style="background: linear-gradient(135deg, var(--color-primary), var(--color-accent)); display:flex;align-items:center;justify-content:center;font-size:2.5rem;border-radius:var(--radius-md);aspect-ratio:4/3;">{r['emoji']}</div>
              <div class="related-game-info">
                <div class="related-game-name">{r['name']}</div>
                <div class="related-game-rtp">{r['rtp']}% RTP</div>
              </div>
            </a>'''
    
    json_ld = json.dumps({
        "@context": "https://schema.org",
        "@type": "VideoGame",
        "name": name,
        "description": desc[:160],
        "genre": "Slot Machine",
        "gamePlatform": "Web Browser",
        "applicationCategory": "Game",
        "operatingSystem": "Any",
        "author": {"@type": "Organization", "name": provider},
        "creator": {"@type": "SoftwareApplication", "name": "Perplexity Computer", "url": "https://www.perplexity.ai/computer"},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "ZAR", "availability": "https://schema.org/InStock"}
    }, indent=2)
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
{PPLX_HEAD}
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} Spina Zonke Slot — Where to Play in South Africa | MzansiSlots</title>
<meta name="description" content="Play {name} by {provider} on Spina Zonke at Hollywoodbets. {rtp}% RTP, {vol} volatility. Find out where to play {name} for real money in South Africa.">
<meta property="og:title" content="{name} — Spina Zonke Slot | SA Casinos">
<meta property="og:description" content="{name} on Spina Zonke. {vol} volatility, {rtp}% RTP. Play at Hollywoodbets South Africa.">
<meta property="og:type" content="website">
<link rel="canonical" href="https://mzansislots.com/slots/{slug}.html">
<link href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=general-sans@400,500,600,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../base.css">
<link rel="stylesheet" href="../style.css">
<script type="application/ld+json">
{json_ld}
</script>
</head>
<body>

<!-- ═══ NAVIGATION ═══ -->
<header class="site-header">
  <div class="container">
    <div class="header-top">
      <a href="../index.html" class="logo">
        <span class="logo-icon">🎰</span>
        MzansiSlots
      </a>
      <nav>
        <ul class="nav-desktop">
          <li><a href="../index.html">Home</a></li>
          <li><a href="../best-slot-sites.html">Best Slot Sites</a></li>
          <li><a href="../slot-games.html">Slot Games</a></li>
          <li><a href="../lekka-slots.html">Lekka Slots</a></li>
          <li><a href="../pragmatic-play.html">Pragmatic Play</a></li>
          <li><a href="../spina-zonke.html" class="active">Spina Zonke</a></li>
          <li><a href="../news.html">News &amp; Guides</a></li>
        </ul>
      </nav>
      <div class="header-actions">
        <button class="theme-toggle" data-theme-toggle aria-label="Toggle dark/light mode">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>
        </button>
        <button class="mobile-toggle" aria-label="Open menu" aria-expanded="false">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
        </button>
      </div>
    </div>
    <nav class="mobile-nav">
      <a href="../index.html">Home</a>
      <a href="../best-slot-sites.html">Best Slot Sites</a>
      <a href="../slot-games.html">Slot Games</a>
      <a href="../lekka-slots.html">Lekka Slots</a>
      <a href="../pragmatic-play.html">Pragmatic Play</a>
      <a href="../spina-zonke.html" class="active">Spina Zonke</a>
      <a href="../news.html">News &amp; Guides</a>
    </nav>
  </div>
</header>

<!-- ═══ BREADCRUMB ═══ -->
<nav class="breadcrumb" aria-label="Breadcrumb">
  <div class="container">
    <a href="../index.html">Home</a>
    <span class="breadcrumb-sep">›</span>
    <a href="../spina-zonke.html">Spina Zonke</a>
    <span class="breadcrumb-sep">›</span>
    <span>{name}</span>
  </div>
</nav>

<!-- ═══ GAME HEADER ═══ -->
<section class="game-page-header">
  <div class="container">
    <div class="game-header-content">
      <div class="game-header-text">
        <div class="game-header-tags">
          {tags_html}
        </div>
        <h1>{name}</h1>
        <p class="game-header-sub">Play {name} on Spina Zonke at Hollywoodbets — South Africa's favourite slot platform.</p>
      </div>
      <div class="game-quick-stats">
        <div class="stat-item">
          <span class="stat-label">RTP</span>
          <span class="stat-value">{rtp}%</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Volatility</span>
          <span class="stat-value">{vol}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Max Win</span>
          <span class="stat-value">{max_win}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Reels</span>
          <span class="stat-value">{reels}</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ═══ PLAY CTA (no demo — Spina Zonke games) ═══ -->
<section class="game-demo-section">
  <div class="container">
    <div class="game-demo-wrapper">
      <div class="game-demo-frame" style="display:flex;align-items:center;justify-content:center;text-align:center;">
        <div class="spina-zonke-cta">
          <div style="font-size:5rem;margin-bottom:var(--space-4);">{emoji}</div>
          <h2 style="font-family:var(--font-display);font-size:var(--text-2xl);margin-bottom:var(--space-3);">Play {name} at Hollywoodbets</h2>
          <p style="color:var(--color-text-muted);margin-bottom:var(--space-6);max-width:480px;margin-left:auto;margin-right:auto;">{name} is available on the Spina Zonke platform. Sign up at Hollywoodbets to play for real money with your welcome bonus.</p>
          <a href="https://www.hollywoodbets.net" class="btn btn-primary btn-lg" target="_blank" rel="noopener noreferrer">Play at Hollywoodbets →</a>
          <p style="color:var(--color-text-faint);font-size:var(--text-xs);margin-top:var(--space-3);">18+ | T&Cs Apply | Play Responsibly</p>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- ═══ WHERE TO PLAY TABLE ═══ -->
<section class="section">
  <div class="container">
    <div class="where-to-play">
      <h2>Where to Play {name} in South Africa</h2>
      <p>{name} by {provider} is available at these licensed South African platforms for real money play with Rand (ZAR) deposits.</p>
      <div class="casino-table-wrapper">
        <table class="casino-table where-play-table">
          <thead>
            <tr>
              <th>Casino</th>
              <th>Welcome Bonus</th>
              <th>Why Play Here</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <div class="casino-name-cell">
                  <div class="casino-logo-placeholder">HW</div>
                  <div>
                    <div class="casino-name">Hollywoodbets</div>
                    <span class="casino-badge badge-popular">Most Popular</span>
                  </div>
                </div>
              </td>
              <td><strong>50 Free Spins + R25 Sign Up Bonus</strong></td>
              <td>Home of Spina Zonke — play {name} here</td>
              <td>
                <div class="casino-actions">
                  <a href="https://www.hollywoodbets.net" class="btn btn-primary btn-sm" target="_blank" rel="noopener noreferrer">Play Here</a>
                </div>
              </td>
            </tr>
            <tr>
              <td>
                <div class="casino-name-cell">
                  <div class="casino-logo-placeholder">BW</div>
                  <div>
                    <div class="casino-name">Betway</div>
                    <span class="casino-badge badge-trending">Trusted</span>
                  </div>
                </div>
              </td>
              <td><strong>100% Match up to R2,000</strong></td>
              <td>Full {provider} slot library available</td>
              <td>
                <div class="casino-actions">
                  <a href="https://www.betway.co.za" class="btn btn-primary btn-sm" target="_blank" rel="noopener noreferrer">Play Here</a>
                </div>
              </td>
            </tr>
            <tr>
              <td>
                <div class="casino-name-cell">
                  <div class="casino-logo-placeholder">JC</div>
                  <div>
                    <div class="casino-name">Jackpot City</div>
                    <span class="casino-badge badge-premium">Premium</span>
                  </div>
                </div>
              </td>
              <td><strong>100% Match up to R25,000</strong></td>
              <td>Big welcome bonus, wide game selection</td>
              <td>
                <div class="casino-actions">
                  <a href="https://www.jackpotcitycasino.co.za" class="btn btn-primary btn-sm" target="_blank" rel="noopener noreferrer">Play Here</a>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</section>

<!-- ═══ GAME REVIEW ═══ -->
<section class="section section-alt">
  <div class="container">
    <div class="game-review-content">
      <div class="game-review-main">
        <h2>{name} Slot Review</h2>
        <p>{desc}</p>

        <h3>{name} Game Specifications</h3>
        <div class="specs-grid">
          <div class="spec-row">
            <span class="spec-label">Provider</span>
            <span class="spec-value">{provider}</span>
          </div>
          <div class="spec-row">
            <span class="spec-label">Platform</span>
            <span class="spec-value">Spina Zonke (Hollywoodbets)</span>
          </div>
          <div class="spec-row">
            <span class="spec-label">RTP</span>
            <span class="spec-value">{rtp}%</span>
          </div>
          <div class="spec-row">
            <span class="spec-label">Volatility</span>
            <span class="spec-value">{vol}</span>
          </div>
          <div class="spec-row">
            <span class="spec-label">Reels</span>
            <span class="spec-value">{reels}</span>
          </div>
          <div class="spec-row">
            <span class="spec-label">Paylines</span>
            <span class="spec-value">{paylines}</span>
          </div>
          <div class="spec-row">
            <span class="spec-label">Max Win</span>
            <span class="spec-value">{max_win}</span>
          </div>
        </div>

        <h3>How to Play {name} on Spina Zonke</h3>
        <ol class="how-to-steps">
          <li><strong>Sign up at Hollywoodbets</strong> — Create your account with a valid SA ID. Takes less than 2 minutes.</li>
          <li><strong>Claim your welcome bonus</strong> — New players get 50 free spins + R25 sign-up bonus. No deposit needed.</li>
          <li><strong>Open Spina Zonke</strong> — Navigate to the Spina Zonke section and search for "{name}".</li>
          <li><strong>Set your bet and spin</strong> — Bets start from as little as R1. Choose your stake and hit spin.</li>
        </ol>
      </div>
    </div>

    <!-- Related Games -->
    <div class="related-games-section">
      <h2>More Spina Zonke Slots</h2>
      <div class="related-games-grid">{related_cards}
      </div>
    </div>
  </div>
</section>

<!-- ═══ CLOSING CTA ═══ -->
<section class="closing-cta">
  <div class="container">
    <h2>Ready to Play {name}?</h2>
    <p>Join thousands of South African players on Spina Zonke and start spinning today.</p>
    <a href="https://www.hollywoodbets.net" class="btn btn-primary btn-lg" target="_blank" rel="noopener noreferrer">Play at Hollywoodbets</a>
  </div>
</section>

<!-- ═══ FOOTER ═══ -->
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="../index.html" class="logo">
          <span class="logo-icon">🎰</span>
          MzansiSlots
        </a>
        <p>South Africa's trusted guide to online slots and casino sites. We review, compare, and rank the best platforms so you can play safely and confidently.</p>
      </div>
      <div class="footer-links">
        <h4>Quick Links</h4>
        <ul>
          <li><a href="#">About MzansiSlots</a></li>
          <li><a href="#">Privacy Policy</a></li>
          <li><a href="#">Terms of Use</a></li>
          <li><a href="#">Sitemap</a></li>
        </ul>
      </div>
      <div class="footer-responsible">
        <h4>Responsible Gambling</h4>
        <p><span class="age-badge">18+</span> Gambling is for adults only. Play responsibly.</p>
        <p>National Responsible Gambling Programme helpline: <strong>0800 006 008</strong></p>
        <p>WhatsApp: <strong>076 675 0710</strong></p>
        <p><a href="https://www.responsiblegambling.co.za" target="_blank" rel="noopener noreferrer" style="color: var(--color-accent); text-decoration: underline;">responsiblegambling.co.za</a></p>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 mzansislots.com All rights reserved.</span>
      <a href="https://www.perplexity.ai/computer" target="_blank" rel="noopener noreferrer">Created with Perplexity Computer</a>
    </div>
    <p class="footer-disclaimer">MzansiSlots is an independent review and comparison site. We may receive compensation from the casino sites we feature, but this does not influence our reviews or rankings. Always gamble responsibly.</p>
  </div>
</footer>

<script src="../hero-bg-inject.js"></script>
<script src="../shared.js"></script>
</body>
</html>'''
    
    return html

for game in SPINA_ZONKE_GAMES:
    html = create_spina_zonke_page(game)
    filepath = os.path.join(SLOTS_DIR, f"{game['slug']}.html")
    with open(filepath, 'w') as f:
        f.write(html)
    print(f"✅ Created Spina Zonke: slots/{game['slug']}.html")


# ═══════════════════════════════════════════════════════════════
# 3. ADD CLICKABLE TAGS TO ALL PRAGMATIC PLAY GAME PAGES
# ═══════════════════════════════════════════════════════════════

# Get all existing Pragmatic Play game pages in /slots/
pragmatic_pages = []
with open(os.path.join(ROOT, 'pragmatic-games.json')) as f:
    pragmatic_games = json.load(f)
    pragmatic_pages = [g['slug'] + '.html' for g in pragmatic_games]

for fname in pragmatic_pages:
    fpath = os.path.join(SLOTS_DIR, fname)
    if not os.path.exists(fpath):
        continue
    
    with open(fpath, 'r') as f:
        content = f.read()
    
    # Replace the static provider tag with a clickable link
    content = content.replace(
        '<span class="game-provider-tag">Pragmatic Play</span>',
        '<a href="../pragmatic-play.html" class="game-provider-tag game-tag-link">Pragmatic Play</a>'
    )
    
    with open(fpath, 'w') as f:
        f.write(content)

print(f"✅ Updated tags on {len(pragmatic_pages)} Pragmatic Play game pages")


# ═══════════════════════════════════════════════════════════════
# 4. UPDATE HUB PAGES TO LINK INTO /slots/
# ═══════════════════════════════════════════════════════════════

# 4a. Update lekka-slots.html — review links now point to /slots/
lekka_path = os.path.join(ROOT, 'lekka-slots.html')
with open(lekka_path, 'r') as f:
    content = f.read()

# Update review links
for fname in REVIEW_FILES:
    content = content.replace(f'href="{fname}"', f'href="slots/{fname}"')

# Update asset paths in cards that link to reviews (images stay in /assets/ at root)
# These are already correct since the hub page is at root level

with open(lekka_path, 'w') as f:
    f.write(content)
print("✅ Updated lekka-slots.html with /slots/ links")

# 4b. Update spina-zonke.html — game cards now link to /slots/ pages
spina_path = os.path.join(ROOT, 'spina-zonke.html')
with open(spina_path, 'r') as f:
    content = f.read()

# Map game names in the hub to their new slugs
spina_card_links = {
    'Hot Hot Hollywoodbets': 'slots/hot-hot-hollywoodbets.html',
    'Lucky Leprechaun': '#',  # No individual page yet
    'Fa Cai Shen Deluxe': '#',
    'Presto!': '#',
    'Koi Gate': '#',
    '5 Lucky Lions': '#',
}

# Replace the "#" placeholder links in the game cards with actual links
for game in SPINA_ZONKE_GAMES:
    # Try to find matching card and update its "Read More" link
    name = game['name']
    slug = game['slug']
    # Check if there's a card with this game name
    if name in content:
        # Find the "Read More" href="#" after this game name
        # Pattern: game name appears, then eventually href="#"
        pass

# More targeted: replace specific card links
# Hot Hot Hollywoodbets card
content = content.replace(
    '<h3>Hot Hot Hollywoodbets</h3>\n          <p>An exclusive Hollywoodbets-branded version of the classic Hot Hot Fruit. Respin features and fiery multipliers make this a Spina Zonke fan favourite.</p>\n          <a href="#" class="btn btn-teal btn-sm">Read More</a>',
    '<h3>Hot Hot Hollywoodbets</h3>\n          <p>An exclusive Hollywoodbets-branded version of the classic Hot Hot Fruit. Respin features and fiery multipliers make this a Spina Zonke fan favourite.</p>\n          <a href="slots/hot-hot-hollywoodbets.html" class="btn btn-teal btn-sm">Read More</a>'
)

# Also add a "Featured Spina Zonke Games" section with links to new game pages
# Insert before the promotions section
new_spina_links_section = '''
<!-- ═══ INDIVIDUAL GAME PAGES ═══ -->
<section class="section">
  <div class="container">
    <div class="section-header">
      <h2>Spina Zonke Game Reviews</h2>
      <p>In-depth reviews and guides for the most popular Spina Zonke games.</p>
    </div>
    <div class="grid-4">
'''

for game in SPINA_ZONKE_GAMES:
    new_spina_links_section += f'''      <a href="slots/{game['slug']}.html" class="card" style="text-decoration:none;color:inherit;transition:transform 200ms,box-shadow 200ms;">
        <div class="card-body" style="text-align:center;">
          <div style="font-size:2.5rem;margin-bottom:var(--space-2);">{game['emoji']}</div>
          <h3 style="font-size:var(--text-sm);margin-bottom:var(--space-1);">{game['name']}</h3>
          <p style="font-size:var(--text-xs);color:var(--color-text-muted);margin:0;">{game['provider']} · {game['rtp']}% RTP</p>
        </div>
      </a>
'''

new_spina_links_section += '''    </div>
  </div>
</section>

'''

# Insert before the promotions section
content = content.replace(
    '<!-- ═══ PROMOTIONS ═══ -->',
    new_spina_links_section + '<!-- ═══ PROMOTIONS ═══ -->'
)

with open(spina_path, 'w') as f:
    f.write(content)
print("✅ Updated spina-zonke.html with game review links")

# 4c. pragmatic-play.html already links to slots/ via JS (slots/${game.slug}.html) — no change needed
print("✅ pragmatic-play.html already links to /slots/ — no changes needed")


# ═══════════════════════════════════════════════════════════════
# 5. UPDATE ALL INTERNAL LINKS ACROSS THE SITE
# ═══════════════════════════════════════════════════════════════

# Pages at root level that might reference old review paths
root_pages_to_update = [
    'index.html', 'best-slot-sites.html', 'slot-games.html', 'news.html'
]

for page in root_pages_to_update:
    fpath = os.path.join(ROOT, page)
    if not os.path.exists(fpath):
        continue
    
    with open(fpath, 'r') as f:
        content = f.read()
    
    changed = False
    for review in REVIEW_FILES:
        old_href = f'href="{review}"'
        new_href = f'href="slots/{review}"'
        if old_href in content:
            content = content.replace(old_href, new_href)
            changed = True
    
    if changed:
        with open(fpath, 'w') as f:
            f.write(content)
        print(f"✅ Updated links in {page}")

# Also check if any Pragmatic Play game pages in /slots/ reference the old review paths
# (e.g., sweet-bonanza.html has Spina Zonke cross-links — but these are to root pages, not reviews)
# These should already be fine with ../spina-zonke.html etc.

print("\n═══ RESTRUCTURE COMPLETE ═══")
print(f"• Moved {len(REVIEW_FILES)} Lekka Slots reviews into /slots/")
print(f"• Created {len(SPINA_ZONKE_GAMES)} Spina Zonke game pages in /slots/")
print(f"• Added clickable tags to {len(pragmatic_pages)} Pragmatic Play pages")
print(f"• Updated hub pages with /slots/ links")
print(f"• Updated internal links across root pages")
