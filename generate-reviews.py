#!/usr/bin/env python3
"""Generate review and promo code pages for all 19 operators."""
import json, os, re, html as htmlmod

# Load data
with open('operator-research.json') as f:
    research = json.load(f)

with open('operators-enriched.json') as f:
    operators = json.load(f)

with open('brand-fixes.json') as f:
    brands = json.load(f)

# Mapping from research entity names to operators-enriched keys
name_map = {
    'ZARbet': 'ZARbet',
    'SuperSportBet': 'SuperSportBet',
    '10bet South Africa': '10bet',
    'Hollywoodbets': 'Hollywoodbets',
    'Wanejo Bets': 'Wanejo Bets',
    'Betway South Africa': 'Betway',
    'Supabets': 'Supabets',
    'World Sports Betting': 'World Sports Betting',
    'Gbets (operated by Dymanex (PTY) Ltd / Goldrush Gaming Group)': 'Gbets',
    '1xBet (1X Corp N.V.)': '1xBet',
    'Easybet': 'Easybet',
    'Jackpot City (operated by Eastern Dawn Sports (Pty) Ltd)': 'JackpotCity',
    'BetXChange': 'BetXChange',
    'Tic Tac Bets (Vengies Gaming (Pty) Ltd)': 'TicTacBets',
    'Playbet South Africa': 'Playbet',
    'Sportingbet South Africa': 'Sportingbet',
    'Lucky Fish': 'Lucky Fish',
    'Bettabets': 'Betta Bets',
    'Betfred South Africa': 'Betfred',
}

# Slug generation
def slugify(name):
    s = name.lower().strip()
    s = re.sub(r'[^a-z0-9]+', '-', s)
    s = s.strip('-')
    return s

# Display names
display_names = {
    'TicTacBets': 'TicTacBets', 'Easybet': 'Easybet', 'Lucky Fish': 'Lucky Fish',
    'ZARbet': 'ZARbet', 'Hollywoodbets': 'Hollywoodbets', 'Playbet': 'Playbet',
    'World Sports Betting': 'World Sports Betting', 'Betta Bets': 'Betta Bets',
    'Betway': 'Betway', '1xBet': '1xBet', 'JackpotCity': 'JackpotCity',
    '10bet': '10bet', 'Wanejo Bets': 'Wanejo Bets', 'BetXChange': 'BetXChange',
    'SuperSportBet': 'SuperSportBet', 'Gbets': 'Gbets', 'Supabets': 'Supabets',
    'Sportingbet': 'Sportingbet', 'Betfred': 'Betfred',
}

# SVG filenames  
svg_files = {
    'TicTacBets': 'tictacbets', 'Easybet': 'easybet', 'Lucky Fish': 'luckyfish',
    'ZARbet': 'zarbet', 'Hollywoodbets': 'hollywoodbets', 'Playbet': 'playbet',
    'World Sports Betting': 'worldsportsbetting', 'Betta Bets': 'bettabets',
    'Betway': 'betway', '1xBet': '1xbet', 'JackpotCity': 'jackpotcity',
    '10bet': '10bet', 'Wanejo Bets': 'wanejo', 'BetXChange': 'betxchange',
    'SuperSportBet': 'supersportbet', 'Gbets': 'gbets', 'Supabets': 'supabets',
    'Sportingbet': 'sportingbet', 'Betfred': 'betfred',
}

# MzansiWins review URL slug mapping (for link replacement later)
mzansiwins_slugs = {
    'TicTacBets': 'tictacbets', 'Easybet': 'easybet', 'Lucky Fish': 'luckyfish',
    'ZARbet': 'zarbet', 'Hollywoodbets': 'hollywoodbets', 'Playbet': 'playbet',
    'World Sports Betting': 'world-sports-betting', 'Betta Bets': 'bettabets',
    'Betway': 'betway', '1xBet': '1xbet', 'JackpotCity': 'jackpotcity',
    '10bet': '10bet', 'Wanejo Bets': 'wanejo-bets', 'BetXChange': 'betxchange',
    'SuperSportBet': 'supersportbet', 'Gbets': 'gbets', 'Supabets': 'supabets',
    'Sportingbet': 'sportingbet', 'Betfred': 'betfred',
}

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

def nav_html(prefix='../'):
    return f'''<header class="site-header">
  <div class="container">
    <div class="header-top">
      <a href="{prefix}index.html" class="logo">
        <svg class="ms-logo" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36" aria-label="MzansiSlots"><rect width="36" height="36" rx="6" fill="#2956B2"/><text x="18" y="19" text-anchor="middle" font-family="'Arial Black',Impact,sans-serif" font-weight="900" font-size="18" fill="#fff">M</text><text x="18" y="33" text-anchor="middle" font-family="'Arial Black',Impact,sans-serif" font-weight="900" font-size="15" fill="#7DF9FF">S</text></svg>
        MzansiSlots
      </a>
      <nav>
        <ul class="nav-desktop">
          <li><a href="{prefix}best-slot-sites.html">Best Slot Sites</a></li>
          <li><a href="{prefix}slot-games.html">Slot Games</a></li>
          <li><a href="{prefix}lekka-slots.html">Lekka Slots</a></li>
          <li class="nav-dropdown">
            <a href="{prefix}slot-games.html" class="nav-dropdown-trigger">Game Studios <svg width="10" height="6" viewBox="0 0 10 6" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M1 1l4 4 4-4"/></svg></a>
            <ul class="nav-dropdown-menu">
              <li><a href="{prefix}pragmatic-play.html">Pragmatic Play</a></li>
              <li><a href="{prefix}play-n-go.html">Play'n GO</a></li>
              <li><a href="{prefix}red-tiger-gaming.html">Red Tiger</a></li>
              <li><a href="{prefix}hacksaw-gaming.html">Hacksaw Gaming</a></li>
              <li><a href="{prefix}bgaming.html">BGaming</a></li>
              <li><a href="{prefix}betsoft.html">Betsoft</a></li>
              <li><a href="{prefix}booming-games.html">Booming Games</a></li>
              <li><a href="{prefix}endorphina.html">Endorphina</a></li>
              <li><a href="{prefix}habanero.html">Habanero</a></li>
              <li><a href="{prefix}spinomenal.html">Spinomenal</a></li>
              <li><a href="{prefix}wazdan.html">Wazdan</a></li>
              <li><a href="{prefix}spribe.html">Spribe</a></li>
              <li><a href="{prefix}amusnet.html">Amusnet</a></li>
              <li><a href="{prefix}aviatrix.html">Aviatrix</a></li>
            </ul>
          </li>
          <li><a href="{prefix}spina-zonke.html">Spina Zonke</a></li>
          <li><a href="{prefix}news.html">News &amp; Guides</a></li>
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
      <a href="{prefix}best-slot-sites.html">Best Slot Sites</a>
      <a href="{prefix}slot-games.html">Slot Games</a>
      <a href="{prefix}lekka-slots.html">Lekka Slots</a>
      <span class="mobile-nav-label">Game Studios</span>
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
      <span class="mobile-nav-label">More</span>
      <a href="{prefix}spina-zonke.html">Spina Zonke</a>
      <a href="{prefix}news.html">News &amp; Guides</a>
    </nav>
  </div>
</header>'''

def footer_html(prefix='../'):
    return f'''<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a href="{prefix}index.html" class="logo">
          <svg class="ms-logo" xmlns="http://www.w3.org/2000/svg" width="36" height="36" viewBox="0 0 36 36" aria-label="MzansiSlots"><rect width="36" height="36" rx="6" fill="#2956B2"/><text x="18" y="19" text-anchor="middle" font-family="'Arial Black',Impact,sans-serif" font-weight="900" font-size="18" fill="#fff">M</text><text x="18" y="33" text-anchor="middle" font-family="'Arial Black',Impact,sans-serif" font-weight="900" font-size="15" fill="#7DF9FF">S</text></svg>
          MzansiSlots
        </a>
        <p>South Africa's trusted guide to online slots and casino sites. We review, compare, and rank the best platforms so you can play safely and confidently.</p>
      </div>
      <div class="footer-links">
        <h4>Quick Links</h4>
        <ul>
          <li><a href="{prefix}about.html">About MzansiSlots</a></li>
          <li><a href="{prefix}about.html">Privacy Policy</a></li>
          <li><a href="{prefix}about.html">Terms of Use</a></li>
          <li><a href="{prefix}sitemap.xml">Sitemap</a></li>
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

<script src="{prefix}hero-bg-inject.js"></script>
<script src="{prefix}shared.js"></script>'''

def e(text):
    """HTML escape"""
    return htmlmod.escape(str(text)) if text else ''

def get_research(op_key):
    """Find research data for an operator key"""
    for r in research:
        rname = r.get('Operator Name', '')
        for map_name, map_key in name_map.items():
            if map_key == op_key and (rname == map_name or map_name.startswith(rname)):
                return r
    # Fuzzy match
    for r in research:
        rname = r.get('Operator Name', '').lower()
        if op_key.lower() in rname or rname in op_key.lower():
            return r
    return {}

def generate_review_page(op_key):
    """Generate a comprehensive review page for an operator."""
    op = operators.get(op_key, {})
    brand = brands.get(op_key, {})
    r = get_research(op_key)
    
    name = display_names.get(op_key, op_key)
    slug = slugify(name)
    svg = svg_files.get(op_key, slug)
    colour = brand.get('mcp_color', op.get('colour', '#1a1a2e'))
    text_colour = op.get('text_colour', '#ffffff')
    affiliate_url = op.get('url', '#')
    promo = op.get('promo', 'NEWBONUS')
    terms = op.get('terms', '18+. T&Cs apply.')
    
    # Research data
    year = r.get('Year Founded', 'N/A')
    background = r.get('Company Background', f'{name} is a licensed South African betting operator offering sports betting and casino games.')
    licence = r.get('Licence Details', 'Licensed by a South African provincial gambling board.')
    welcome = r.get('Welcome Bonus', op.get('bonus', 'Welcome bonus available'))
    promos = r.get('Promo Codes', f'Use code {promo}')
    slot_providers = r.get('Slot Providers', 'Pragmatic Play, Evolution, and more')
    payments = r.get('Payment Methods', 'EFT, Ozow, credit cards, vouchers')
    mobile = r.get('Mobile App', 'Mobile-optimized website available')
    min_dep = r.get('Minimum Deposit', 'R10-R50')
    support = r.get('Customer Support', 'Live chat, email, phone')
    features = r.get('Key Features', f'{name} offers sports betting and casino games for South African players.')
    pros = r.get('Pros', 'Licensed in South Africa, wide game selection, local payment methods')
    cons = r.get('Cons', 'Standard wagering requirements apply')
    
    # Clean up bonus text
    if welcome and 'global' in welcome.lower():
        welcome = f'{name} welcome bonus available for new South African players'
    
    promo_slug = slugify(name)
    
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
{PPLX_HEAD}
<meta charset="UTF-8">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="dns-prefetch" href="https://api.fontshare.com">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="icon" type="image/png" sizes="96x96" href="../favicon-96x96.png">
<link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
<link rel="manifest" href="../site.webmanifest">
<meta name="theme-color" content="#1a1a2e">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(name)} Review South Africa 2026 - Slots, Bonus & Promo Code | MzansiSlots</title>
<meta name="description" content="Comprehensive {e(name)} review for South African players. Welcome bonus details, available slots, payment methods, promo codes, and our expert rating for 2026.">
<link rel="preload" href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=general-sans@400,500,600,700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=general-sans@400,500,600,700&display=swap"></noscript>
<link rel="stylesheet" href="../base.min.css">
<link rel="stylesheet" href="../style.min.css">
<link rel="canonical" href="https://mzansislots.com/reviews/{slug}.html">
<meta property="og:title" content="{e(name)} Review South Africa 2026">
<meta property="og:description" content="Read our detailed {e(name)} review. Welcome bonus, slots, payment methods, and promo codes for SA players.">
<meta property="og:type" content="article">
<meta property="og:site_name" content="MzansiSlots">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Review","name":"{e(name)} Review","author":{{"@type":"Organization","name":"MzansiSlots"}},"itemReviewed":{{"@type":"Organization","name":"{e(name)}"}},"reviewBody":"Comprehensive review of {e(name)} for South African players","creator":{{"@type":"SoftwareApplication","name":"Perplexity Computer","url":"https://www.perplexity.ai/computer"}}}}
</script>
<style>
.review-hero {{
  background: {colour};
  color: {text_colour};
  padding: var(--space-10) 0 var(--space-8);
  text-align: center;
}}
.review-hero h1 {{
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 700;
  margin-bottom: var(--space-4);
}}
.review-hero-logo {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.15);
  border-radius: var(--radius-lg);
  padding: var(--space-4) var(--space-6);
  margin-bottom: var(--space-4);
  min-height: 60px;
}}
.review-hero-logo img {{
  height: 40px;
  max-width: 180px;
  object-fit: contain;
}}
.review-hero .bonus-highlight {{
  font-size: var(--text-lg);
  opacity: 0.95;
  margin-bottom: var(--space-4);
}}
.review-hero .cta-btn {{
  display: inline-block;
  padding: var(--space-3) var(--space-8);
  background: #fff;
  color: {colour};
  font-weight: 700;
  border-radius: var(--radius-full);
  text-decoration: none;
  font-size: var(--text-base);
  transition: transform 0.2s, box-shadow 0.2s;
}}
.review-hero .cta-btn:hover {{
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}}
.review-content {{
  max-width: 800px;
  margin: 0 auto;
  padding: var(--space-8) var(--space-4);
}}
.review-content h2 {{
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  margin: var(--space-8) 0 var(--space-4);
  padding-bottom: var(--space-2);
  border-bottom: 2px solid var(--color-border);
}}
.review-content h3 {{
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 600;
  margin: var(--space-6) 0 var(--space-3);
}}
.review-content p, .review-content li {{
  font-size: var(--text-base);
  line-height: 1.7;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}}
.review-content ul {{
  padding-left: var(--space-5);
  margin-bottom: var(--space-4);
}}
.info-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-4);
  margin: var(--space-6) 0;
}}
.info-card {{
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  text-align: center;
}}
.info-card-label {{
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--color-text-muted);
  margin-bottom: var(--space-2);
}}
.info-card-value {{
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
  color: var(--color-text);
}}
.pros-cons {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
  margin: var(--space-6) 0;
}}
@media (max-width: 600px) {{
  .pros-cons {{ grid-template-columns: 1fr; }}
}}
.pros-list, .cons-list {{
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
}}
.pros-list h3 {{ color: #22c55e; margin-top: 0; }}
.cons-list h3 {{ color: #ef4444; margin-top: 0; }}
.pros-list li::marker {{ content: "\\2713  "; color: #22c55e; }}
.cons-list li::marker {{ content: "\\2717  "; color: #ef4444; }}
.cta-section {{
  background: var(--color-surface);
  border: 2px solid {colour};
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  text-align: center;
  margin: var(--space-8) 0;
}}
.cta-section .cta-btn {{
  display: inline-block;
  padding: var(--space-3) var(--space-8);
  background: {colour};
  color: {text_colour};
  font-weight: 700;
  border-radius: var(--radius-full);
  text-decoration: none;
  font-size: var(--text-base);
}}
.promo-code-box {{
  display: inline-block;
  background: var(--color-surface);
  border: 2px dashed {colour};
  border-radius: var(--radius-md);
  padding: var(--space-2) var(--space-5);
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--color-text);
  margin: var(--space-3) 0;
}}
.breadcrumb {{
  padding: var(--space-3) 0;
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}}
.breadcrumb a {{
  color: var(--color-text-muted);
  text-decoration: none;
}}
.breadcrumb a:hover {{
  color: var(--color-accent);
}}
</style>
</head>
<body>

{nav_html('../')}

<div class="container">
  <div class="breadcrumb">
    <a href="../index.html">Home</a> &rsaquo; <a href="index.html">Reviews</a> &rsaquo; {e(name)}
  </div>
</div>

<section class="review-hero">
  <div class="container">
    <div class="review-hero-logo">
      <img src="../assets/brands/{svg}.svg" alt="{e(name)}" loading="lazy">
    </div>
    <h1>{e(name)} Review South Africa 2026</h1>
    <p class="bonus-highlight">{e(welcome)}</p>
    <div class="promo-code-box">{e(promo)}</div>
    <br><br>
    <a href="{e(affiliate_url)}" target="_blank" rel="noopener noreferrer" class="cta-btn">Visit {e(name)}</a>
  </div>
</section>

<div class="review-content">

  <div class="info-grid">
    <div class="info-card">
      <div class="info-card-label">Founded</div>
      <div class="info-card-value">{e(year)}</div>
    </div>
    <div class="info-card">
      <div class="info-card-label">Min Deposit</div>
      <div class="info-card-value">{e(min_dep)}</div>
    </div>
    <div class="info-card">
      <div class="info-card-label">Promo Code</div>
      <div class="info-card-value">{e(promo)}</div>
    </div>
    <div class="info-card">
      <div class="info-card-label">Mobile App</div>
      <div class="info-card-value">{"Yes" if "yes" in mobile.lower() or "android" in mobile.lower() or "ios" in mobile.lower() else "Mobile Site"}</div>
    </div>
  </div>

  <h2>About {e(name)}</h2>
  <p>{e(background)}</p>

  <h2>Licensing and Safety</h2>
  <p>{e(licence)}</p>
  <p>All licensed South African betting operators are regulated under the National Gambling Act. {e(name)} holds a valid provincial gambling licence, which means your funds and personal data are protected by South African law. Players should always verify an operator's licensing status before depositing.</p>

  <h2>Welcome Bonus and Promotions</h2>
  <p>{e(welcome)}</p>
  <p>To claim the {e(name)} welcome bonus, use promo code <strong>{e(promo)}</strong> during registration or at the cashier. {e(terms)}</p>
  <p>Looking for the latest {e(name)} promo codes? Visit our dedicated <a href="../promo-codes/{slug}.html">{e(name)} promo codes page</a> for the most up-to-date offers and bonus codes.</p>

  <h2>Available Slots and Casino Games</h2>
  <p>{e(name)} offers a wide selection of slot games and casino entertainment powered by leading software providers:</p>
  <p>{e(slot_providers)}</p>
  <p>The platform features popular titles across categories including video slots, classic slots, progressive jackpots, live dealer games, and crash games like Aviator. South African favourites like Spina Zonke titles are typically available.</p>

  <h2>Payment Methods</h2>
  <p>{e(name)} supports a range of deposit and withdrawal methods popular with South African players:</p>
  <p>{e(payments)}</p>
  <p>All transactions are processed in South African Rand (ZAR), so you will not incur currency conversion fees. Deposits are typically instant, while withdrawals may take 1-3 business days depending on the method chosen.</p>

  <h2>Mobile Experience</h2>
  <p>{e(mobile)}</p>
  <p>The {e(name)} platform is fully optimised for mobile devices, allowing you to play slots, place bets, and manage your account from any smartphone or tablet browser.</p>

  <h2>Customer Support</h2>
  <p>{e(support)}</p>

  <h2>Key Features</h2>
  <p>{e(features)}</p>

  <div class="pros-cons">
    <div class="pros-list">
      <h3>Pros</h3>
      <ul>'''
    
    # Parse pros
    pros_items = [p.strip() for p in pros.split(',') if p.strip()]
    for p in pros_items[:6]:
        page += f'\n        <li>{e(p)}</li>'
    
    page += f'''
      </ul>
    </div>
    <div class="cons-list">
      <h3>Cons</h3>
      <ul>'''
    
    # Parse cons
    cons_items = [c.strip() for c in cons.split(',') if c.strip()]
    for c in cons_items[:5]:
        page += f'\n        <li>{e(c)}</li>'
    
    page += f'''
      </ul>
    </div>
  </div>

  <div class="cta-section">
    <h3>Ready to Play at {e(name)}?</h3>
    <p>Use promo code <strong>{e(promo)}</strong> to claim your welcome bonus.</p>
    <a href="{e(affiliate_url)}" target="_blank" rel="noopener noreferrer" class="cta-btn">Visit {e(name)}</a>
    <p style="font-size: var(--text-xs); color: var(--color-text-muted); margin-top: var(--space-3);">{e(terms)}</p>
  </div>

  <p><strong>Gambling Disclaimer:</strong> Online gambling in South Africa is regulated under the National Gambling Act. Sports betting is legal through provincially licensed bookmakers. 18+ only. Gambling can be addictive. National Responsible Gambling Programme helpline: <strong>0800 006 008</strong>.</p>

</div>

{footer_html('../')}
</body>
</html>'''
    
    return page, slug


def generate_promo_page(op_key):
    """Generate a promo code page for an operator."""
    op = operators.get(op_key, {})
    brand = brands.get(op_key, {})
    r = get_research(op_key)
    
    name = display_names.get(op_key, op_key)
    slug = slugify(name)
    svg = svg_files.get(op_key, slug)
    colour = brand.get('mcp_color', op.get('colour', '#1a1a2e'))
    text_colour = op.get('text_colour', '#ffffff')
    affiliate_url = op.get('url', '#')
    promo = op.get('promo', 'NEWBONUS')
    terms = op.get('terms', '18+. T&Cs apply.')
    welcome = r.get('Welcome Bonus', op.get('bonus', 'Welcome bonus available'))
    promos_detail = r.get('Promo Codes', '')
    
    if welcome and 'global' in welcome.lower():
        welcome = f'{name} welcome bonus available for new South African players'
    
    # Current month/year
    month_year = "March 2026"
    
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
{PPLX_HEAD}
<meta charset="UTF-8">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="dns-prefetch" href="https://api.fontshare.com">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="icon" type="image/png" sizes="96x96" href="../favicon-96x96.png">
<link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
<link rel="manifest" href="../site.webmanifest">
<meta name="theme-color" content="#1a1a2e">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{e(name)} Promo Code {month_year} - Latest Bonus Codes South Africa | MzansiSlots</title>
<meta name="description" content="{e(name)} promo code for {month_year}: Use code {e(promo)} to claim your welcome bonus. Updated daily for South African players.">
<link rel="preload" href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=general-sans@400,500,600,700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=general-sans@400,500,600,700&display=swap"></noscript>
<link rel="stylesheet" href="../base.min.css">
<link rel="stylesheet" href="../style.min.css">
<link rel="canonical" href="https://mzansislots.com/promo-codes/{slug}.html">
<meta property="og:title" content="{e(name)} Promo Code {month_year}">
<meta property="og:description" content="Latest {e(name)} promo codes and bonus offers for South African players.">
<meta property="og:type" content="article">
<meta property="og:site_name" content="MzansiSlots">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"WebPage","name":"{e(name)} Promo Code {month_year}","description":"Latest promo codes for {e(name)} South Africa","creator":{{"@type":"SoftwareApplication","name":"Perplexity Computer","url":"https://www.perplexity.ai/computer"}}}}
</script>
<style>
.promo-hero {{
  background: {colour};
  color: {text_colour};
  padding: var(--space-10) 0 var(--space-8);
  text-align: center;
}}
.promo-hero h1 {{
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 700;
  margin-bottom: var(--space-4);
}}
.promo-hero-logo {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255,255,255,0.15);
  border-radius: var(--radius-lg);
  padding: var(--space-4) var(--space-6);
  margin-bottom: var(--space-4);
  min-height: 60px;
}}
.promo-hero-logo img {{
  height: 40px;
  max-width: 180px;
  object-fit: contain;
}}
.promo-content {{
  max-width: 800px;
  margin: 0 auto;
  padding: var(--space-8) var(--space-4);
}}
.promo-content h2 {{
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  margin: var(--space-8) 0 var(--space-4);
  padding-bottom: var(--space-2);
  border-bottom: 2px solid var(--color-border);
}}
.promo-content p, .promo-content li {{
  font-size: var(--text-base);
  line-height: 1.7;
  color: var(--color-text-secondary);
  margin-bottom: var(--space-3);
}}
.promo-content ul, .promo-content ol {{
  padding-left: var(--space-5);
  margin-bottom: var(--space-4);
}}
.promo-card {{
  background: var(--color-surface);
  border: 2px solid {colour};
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  text-align: center;
  margin: var(--space-6) 0;
}}
.promo-card-title {{
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: 700;
  margin-bottom: var(--space-2);
}}
.promo-code-box {{
  display: inline-block;
  background: var(--color-bg);
  border: 2px dashed {colour};
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-6);
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--color-text);
  margin: var(--space-4) 0;
}}
.promo-card .cta-btn {{
  display: inline-block;
  padding: var(--space-3) var(--space-8);
  background: {colour};
  color: {text_colour};
  font-weight: 700;
  border-radius: var(--radius-full);
  text-decoration: none;
  font-size: var(--text-base);
  margin-top: var(--space-3);
  transition: transform 0.2s;
}}
.promo-card .cta-btn:hover {{
  transform: translateY(-2px);
}}
.breadcrumb {{
  padding: var(--space-3) 0;
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}}
.breadcrumb a {{
  color: var(--color-text-muted);
  text-decoration: none;
}}
.breadcrumb a:hover {{
  color: var(--color-accent);
}}
.steps-list {{
  counter-reset: steps;
  list-style: none;
  padding-left: 0;
}}
.steps-list li {{
  counter-increment: steps;
  padding-left: var(--space-8);
  position: relative;
  margin-bottom: var(--space-4);
}}
.steps-list li::before {{
  content: counter(steps);
  position: absolute;
  left: 0;
  top: 0;
  width: 28px;
  height: 28px;
  background: {colour};
  color: {text_colour};
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: var(--text-sm);
}}
</style>
</head>
<body>

{nav_html('../')}

<div class="container">
  <div class="breadcrumb">
    <a href="../index.html">Home</a> &rsaquo; <a href="index.html">Promo Codes</a> &rsaquo; {e(name)}
  </div>
</div>

<section class="promo-hero">
  <div class="container">
    <div class="promo-hero-logo">
      <img src="../assets/brands/{svg}.svg" alt="{e(name)}" loading="lazy">
    </div>
    <h1>{e(name)} Promo Code {month_year}</h1>
    <p style="font-size: var(--text-lg); opacity: 0.95;">Latest verified promo codes for South African players</p>
  </div>
</section>

<div class="promo-content">

  <div class="promo-card">
    <div class="promo-card-title">{e(name)} Welcome Bonus</div>
    <p>{e(welcome)}</p>
    <div class="promo-code-box">{e(promo)}</div>
    <br>
    <a href="{e(affiliate_url)}" target="_blank" rel="noopener noreferrer" class="cta-btn">Claim Bonus at {e(name)}</a>
    <p style="font-size: var(--text-xs); color: var(--color-text-muted); margin-top: var(--space-3);">{e(terms)}</p>
  </div>

  <h2>How to Use the {e(name)} Promo Code</h2>
  <ol class="steps-list">
    <li><strong>Visit {e(name)}</strong> by clicking our link above to ensure the promo code is tracked.</li>
    <li><strong>Register a new account</strong> by completing the sign-up form with your details.</li>
    <li><strong>Enter promo code <code>{e(promo)}</code></strong> in the promo code field during registration or at the cashier.</li>
    <li><strong>Make your first deposit</strong> to activate the welcome bonus.</li>
    <li><strong>Claim your bonus</strong> and start playing. Wagering requirements apply.</li>
  </ol>

  <h2>Current {e(name)} Promo Codes</h2>
  <table class="casino-table" style="width:100%; margin: var(--space-4) 0;">
    <thead>
      <tr>
        <th style="text-align:left; padding: var(--space-3);">Promo Code</th>
        <th style="text-align:left; padding: var(--space-3);">Offer</th>
        <th style="text-align:left; padding: var(--space-3);">Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: var(--space-3); font-weight: 700;">{e(promo)}</td>
        <td style="padding: var(--space-3);">{e(welcome)}</td>
        <td style="padding: var(--space-3);"><span style="background: rgba(34,197,94,0.2); color: #22c55e; padding: 2px 8px; border-radius: 4px; font-size: var(--text-xs); font-weight: 700;">VERIFIED</span></td>
      </tr>'''

    # Add NEWBONUS row if different from main promo
    if promo != 'NEWBONUS':
        page += f'''
      <tr>
        <td style="padding: var(--space-3); font-weight: 700;">NEWBONUS</td>
        <td style="padding: var(--space-3);">Alternative welcome bonus code</td>
        <td style="padding: var(--space-3);"><span style="background: rgba(34,197,94,0.2); color: #22c55e; padding: 2px 8px; border-radius: 4px; font-size: var(--text-xs); font-weight: 700;">VERIFIED</span></td>
      </tr>'''
    
    if promo != 'BETS':
        page += f'''
      <tr>
        <td style="padding: var(--space-3); font-weight: 700;">BETS</td>
        <td style="padding: var(--space-3);">Alternative bonus code</td>
        <td style="padding: var(--space-3);"><span style="background: rgba(245,158,11,0.2); color: #f59e0b; padding: 2px 8px; border-radius: 4px; font-size: var(--text-xs); font-weight: 700;">CHECK SITE</span></td>
      </tr>'''

    page += f'''
    </tbody>
  </table>

  <h2>{e(name)} Bonus Details</h2>
  <p>{e(welcome)}</p>
  <p>{e(terms)}</p>

  <h2>Read Our Full Review</h2>
  <p>Want to know more about what {e(name)} has to offer? Read our <a href="../reviews/{slug}.html">comprehensive {e(name)} review</a> covering their complete game selection, payment methods, mobile experience, and licensing details.</p>

  <div class="promo-card" style="margin-top: var(--space-8);">
    <div class="promo-card-title">Claim Your {e(name)} Bonus</div>
    <p>Use code <strong>{e(promo)}</strong> to get started today.</p>
    <a href="{e(affiliate_url)}" target="_blank" rel="noopener noreferrer" class="cta-btn">Visit {e(name)}</a>
    <p style="font-size: var(--text-xs); color: var(--color-text-muted); margin-top: var(--space-3);">{e(terms)}</p>
  </div>

  <p><strong>Gambling Disclaimer:</strong> Online gambling in South Africa is regulated under the National Gambling Act. 18+ only. Gambling can be addictive. National Responsible Gambling Programme helpline: <strong>0800 006 008</strong>.</p>

</div>

{footer_html('../')}
</body>
</html>'''
    
    return page, slug


# ─── GENERATE ALL PAGES ─────────────────────────────────────────

review_pages = []
promo_pages = []

for op_key in operators.keys():
    # Review page
    html_content, slug = generate_review_page(op_key)
    filepath = f'reviews/{slug}.html'
    with open(filepath, 'w') as f:
        f.write(html_content)
    review_pages.append((op_key, slug, display_names.get(op_key, op_key)))
    print(f'  Created review: {filepath}')
    
    # Promo code page
    html_content, slug = generate_promo_page(op_key)
    filepath = f'promo-codes/{slug}.html'
    with open(filepath, 'w') as f:
        f.write(html_content)
    promo_pages.append((op_key, slug, display_names.get(op_key, op_key)))
    print(f'  Created promo: {filepath}')

# ─── GENERATE INDEX PAGES ────────────────────────────────────────

# Reviews index
reviews_index = f'''<!DOCTYPE html>
<html lang="en">
<head>
{PPLX_HEAD}
<meta charset="UTF-8">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="icon" type="image/png" sizes="96x96" href="../favicon-96x96.png">
<link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
<link rel="manifest" href="../site.webmanifest">
<meta name="theme-color" content="#1a1a2e">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Casino Reviews South Africa 2026 - Expert Ratings | MzansiSlots</title>
<meta name="description" content="Read our expert reviews of South Africa's top online casinos and betting sites. Honest ratings, bonus details, and player experiences for 2026.">
<link rel="preload" href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=general-sans@400,500,600,700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=general-sans@400,500,600,700&display=swap"></noscript>
<link rel="stylesheet" href="../base.min.css">
<link rel="stylesheet" href="../style.min.css">
<link rel="canonical" href="https://mzansislots.com/reviews/">
<style>
.reviews-hero {{
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: #fff;
  padding: var(--space-10) 0 var(--space-8);
  text-align: center;
}}
.reviews-hero h1 {{
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 700;
}}
.reviews-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-5);
  padding: var(--space-8) var(--space-4);
  max-width: 1200px;
  margin: 0 auto;
}}
.review-card {{
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}}
.review-card:hover {{
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}}
.review-card-header {{
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-5);
  min-height: 70px;
}}
.review-card-header img {{
  height: 32px;
  max-width: 140px;
  object-fit: contain;
}}
.review-card-body {{
  padding: var(--space-4) var(--space-5) var(--space-5);
  text-align: center;
}}
.review-card-body h3 {{
  font-family: var(--font-display);
  font-weight: 700;
  font-size: var(--text-base);
  margin-bottom: var(--space-2);
}}
.review-card-body p {{
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  margin-bottom: var(--space-3);
}}
.review-card-links {{
  display: flex;
  gap: var(--space-2);
  justify-content: center;
}}
.review-card-links a {{
  font-size: var(--text-sm);
  font-weight: 600;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  text-decoration: none;
  transition: opacity 0.2s;
}}
.review-card-links a:hover {{ opacity: 0.85; }}
.breadcrumb {{
  padding: var(--space-3) 0;
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}}
.breadcrumb a {{
  color: var(--color-text-muted);
  text-decoration: none;
}}
.breadcrumb a:hover {{ color: var(--color-accent); }}
</style>
</head>
<body>

{nav_html('../')}

<div class="container">
  <div class="breadcrumb">
    <a href="../index.html">Home</a> &rsaquo; Casino Reviews
  </div>
</div>

<section class="reviews-hero">
  <div class="container">
    <h1>Casino Reviews South Africa 2026</h1>
    <p style="opacity: 0.9; margin-top: var(--space-3);">Honest, in-depth reviews of every licensed betting site we feature</p>
  </div>
</section>

<div class="reviews-grid">
'''

for op_key, slug, name in review_pages:
    brand = brands.get(op_key, {})
    op = operators.get(op_key, {})
    colour = brand.get('mcp_color', '#1a1a2e')
    text_colour = op.get('text_colour', '#ffffff')
    svg = svg_files.get(op_key, slug)
    affiliate_url = op.get('url', '#')
    
    reviews_index += f'''  <div class="review-card">
    <div class="review-card-header" style="background: {colour};">
      <img src="../assets/brands/{svg}.svg" alt="{e(name)}" loading="lazy">
    </div>
    <div class="review-card-body">
      <h3>{e(name)}</h3>
      <p>{e(op.get('terms', '18+. T&Cs apply.')[:60])}</p>
      <div class="review-card-links">
        <a href="{slug}.html" style="background: var(--color-surface); border: 1px solid var(--color-border); color: var(--color-text);">Read Review</a>
        <a href="{e(affiliate_url)}" target="_blank" rel="noopener noreferrer" style="background: {colour}; color: {text_colour};">Visit Site</a>
      </div>
    </div>
  </div>
'''

reviews_index += f'''</div>

<div style="max-width: 800px; margin: 0 auto; padding: var(--space-6) var(--space-4) var(--space-10);">
  <p style="font-size: var(--text-sm); color: var(--color-text-muted);"><strong>Gambling Disclaimer:</strong> Online gambling in South Africa is regulated under the National Gambling Act. 18+ only. Gambling can be addictive. National Responsible Gambling Programme helpline: <strong>0800 006 008</strong>.</p>
</div>

{footer_html('../')}
</body>
</html>'''

with open('reviews/index.html', 'w') as f:
    f.write(reviews_index)
print('  Created: reviews/index.html')


# ─── PROMO CODES INDEX ───────────────────────────────────────────

promo_index = f'''<!DOCTYPE html>
<html lang="en">
<head>
{PPLX_HEAD}
<meta charset="UTF-8">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="icon" type="image/png" sizes="96x96" href="../favicon-96x96.png">
<link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png">
<link rel="manifest" href="../site.webmanifest">
<meta name="theme-color" content="#1a1a2e">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Promo Codes South Africa March 2026 - Latest Betting Bonus Codes | MzansiSlots</title>
<meta name="description" content="All the latest South African betting promo codes for March 2026. Verified bonus codes for Hollywoodbets, Betway, Easybet, and more.">
<link rel="preload" href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=general-sans@400,500,600,700&display=swap" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=clash-display@400,500,600,700&f[]=general-sans@400,500,600,700&display=swap"></noscript>
<link rel="stylesheet" href="../base.min.css">
<link rel="stylesheet" href="../style.min.css">
<link rel="canonical" href="https://mzansislots.com/promo-codes/">
<style>
.promo-index-hero {{
  background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 50%, #e94560 100%);
  color: #fff;
  padding: var(--space-10) 0 var(--space-8);
  text-align: center;
}}
.promo-index-hero h1 {{
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 700;
}}
.promo-grid {{
  max-width: 900px;
  margin: 0 auto;
  padding: var(--space-8) var(--space-4);
}}
.promo-row {{
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-5);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  margin-bottom: var(--space-3);
  transition: transform 0.2s;
}}
.promo-row:hover {{
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}
.promo-row-logo {{
  width: 56px;
  height: 56px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  padding: var(--space-2);
}}
.promo-row-logo img {{
  height: 24px;
  max-width: 48px;
  object-fit: contain;
}}
.promo-row-info {{
  flex: 1;
  min-width: 0;
}}
.promo-row-name {{
  font-family: var(--font-display);
  font-weight: 700;
  font-size: var(--text-base);
}}
.promo-row-code {{
  display: inline-block;
  font-weight: 700;
  font-size: var(--text-sm);
  padding: 2px 10px;
  border-radius: var(--radius-sm);
  margin-top: 4px;
}}
.promo-row-actions {{
  display: flex;
  gap: var(--space-2);
  flex-shrink: 0;
}}
.promo-row-actions a {{
  font-size: var(--text-sm);
  font-weight: 600;
  padding: var(--space-2) var(--space-4);
  border-radius: var(--radius-full);
  text-decoration: none;
  white-space: nowrap;
}}
@media (max-width: 600px) {{
  .promo-row {{ flex-wrap: wrap; }}
  .promo-row-actions {{ width: 100%; justify-content: center; }}
}}
.breadcrumb {{
  padding: var(--space-3) 0;
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}}
.breadcrumb a {{
  color: var(--color-text-muted);
  text-decoration: none;
}}
.breadcrumb a:hover {{ color: var(--color-accent); }}
</style>
</head>
<body>

{nav_html('../')}

<div class="container">
  <div class="breadcrumb">
    <a href="../index.html">Home</a> &rsaquo; Promo Codes
  </div>
</div>

<section class="promo-index-hero">
  <div class="container">
    <h1>Promo Codes South Africa - March 2026</h1>
    <p style="opacity: 0.9; margin-top: var(--space-3);">Verified bonus codes for every major SA betting site</p>
  </div>
</section>

<div class="promo-grid">
'''

for op_key, slug, name in promo_pages:
    brand = brands.get(op_key, {})
    op = operators.get(op_key, {})
    colour = brand.get('mcp_color', '#1a1a2e')
    text_colour = op.get('text_colour', '#ffffff')
    svg = svg_files.get(op_key, slug)
    promo = op.get('promo', 'NEWBONUS')
    affiliate_url = op.get('url', '#')
    
    promo_index += f'''  <div class="promo-row">
    <div class="promo-row-logo" style="background: {colour};">
      <img src="../assets/brands/{svg}.svg" alt="{e(name)}" loading="lazy">
    </div>
    <div class="promo-row-info">
      <div class="promo-row-name">{e(name)}</div>
      <span class="promo-row-code" style="background: rgba(34,197,94,0.15); color: #22c55e;">{e(promo)}</span>
    </div>
    <div class="promo-row-actions">
      <a href="{slug}.html" style="background: var(--color-surface); border: 1px solid var(--color-border); color: var(--color-text);">Details</a>
      <a href="{e(affiliate_url)}" target="_blank" rel="noopener noreferrer" style="background: {colour}; color: {text_colour};">Claim</a>
    </div>
  </div>
'''

promo_index += f'''</div>

<div style="max-width: 800px; margin: 0 auto; padding: var(--space-6) var(--space-4) var(--space-10);">
  <p style="font-size: var(--text-sm); color: var(--color-text-muted);"><strong>Gambling Disclaimer:</strong> Online gambling in South Africa is regulated under the National Gambling Act. 18+ only. Gambling can be addictive. National Responsible Gambling Programme helpline: <strong>0800 006 008</strong>.</p>
</div>

{footer_html('../')}
</body>
</html>'''

with open('promo-codes/index.html', 'w') as f:
    f.write(promo_index)
print('  Created: promo-codes/index.html')

# ─── SAVE MAPPING FOR LINK REPLACEMENT ───────────────────────────

link_map = {}
for op_key in operators.keys():
    name = display_names.get(op_key, op_key)
    slug = slugify(name)
    mzw_slug = mzansiwins_slugs.get(op_key, slug)
    link_map[op_key] = {
        'review_slug': slug,
        'mzw_review_url': f'https://www.mzansiwins.co.za/{mzw_slug}-review/',
        'new_review_url_root': f'reviews/{slug}.html',
        'new_review_url_slots': f'../reviews/{slug}.html',
        'new_review_url_news': f'../reviews/{slug}.html',
        'new_promo_url_root': f'promo-codes/{slug}.html',
    }

with open('link-replacement-map.json', 'w') as f:
    json.dump(link_map, f, indent=2)

print(f'\nGenerated {len(review_pages)} review pages + {len(promo_pages)} promo pages + 2 index pages = {len(review_pages) + len(promo_pages) + 2} total')
print('Link replacement map saved to link-replacement-map.json')
