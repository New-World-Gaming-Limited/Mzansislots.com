/*
  Hero Slot Machine Reels Background
  Creates vertical spinning columns of classic slot symbols
  (7s, BARs, cherries, bells, diamonds, stars)
  like an old-school slot machine running in the background.
  Reels spin DOWNWARD.
*/
(function() {
  // SVG symbols - classic slot machine icons
  const symbols = {
    seven: (color) => `<text x="12" y="20" text-anchor="middle" font-family="'Arial Black','Impact',sans-serif" font-size="22" font-weight="900" fill="${color}">7</text>`,
    star: (color) => `<polygon points="12,2 14.9,8.6 22,9.6 17,14.8 18.2,22 12,18.5 5.8,22 7,14.8 2,9.6 9.1,8.6" fill="${color}"/>`,
    cherry: (color) => `<g fill="${color}"><circle cx="8" cy="16" r="4.5"/><circle cx="16" cy="18" r="4.5"/><path d="M8 11.5 Q10 4 12 3 Q14 4 16 13.5" fill="none" stroke="${color}" stroke-width="1.5" stroke-linecap="round"/><ellipse cx="13" cy="3.5" rx="3" ry="1.8" fill="${color}" opacity="0.7"/></g>`,
    bell: (color) => `<g fill="${color}"><path d="M12 2 C12 2 7 6 6 12 C5.5 14.5 5 16 5 17 L19 17 C19 16 18.5 14.5 18 12 C17 6 12 2 12 2Z"/><rect x="10" y="17" width="4" height="3" rx="1.5"/><circle cx="12" cy="2.5" r="1.2"/></g>`,
    diamond: (color) => `<polygon points="12,2 22,12 12,22 2,12" fill="${color}"/>`,
    bar: (color) => `<g><rect x="2" y="7" width="20" height="10" rx="2" fill="${color}"/><text x="12" y="15.5" text-anchor="middle" font-family="'Arial Black','Impact',sans-serif" font-size="7" font-weight="900" fill="rgba(15,23,42,0.6)">BAR</text></g>`,
    sevenOutline: (color) => `<text x="12" y="20" text-anchor="middle" font-family="'Arial Black','Impact',sans-serif" font-size="22" font-weight="900" fill="none" stroke="${color}" stroke-width="0.8">7</text>`,
    diamondOutline: (color) => `<polygon points="12,2 22,12 12,22 2,12" fill="none" stroke="${color}" stroke-width="1"/>`,
  };

  // Colors for the symbols - subtle gold, white, cyan tones
  const colors = [
    'rgba(255,215,0,0.25)',   // gold
    'rgba(255,255,255,0.18)', // white
    'rgba(125,249,255,0.15)', // cyan
    'rgba(255,215,0,0.12)',   // dimmer gold
    'rgba(255,255,255,0.10)', // dimmer white
    'rgba(234,88,12,0.15)',   // orange tint
  ];

  // Create one reel column SVG strip
  function buildReelStrip(numSymbols, iconSize, seed) {
    const cellH = iconSize + 16;
    const totalH = numSymbols * cellH;
    let shapes = '';
    let s = seed;
    function rng() { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }

    const types = ['seven', 'cherry', 'bell', 'diamond', 'bar', 'star', 'sevenOutline', 'diamondOutline'];

    for (let i = 0; i < numSymbols; i++) {
      const type = types[Math.floor(rng() * types.length)];
      const color = colors[Math.floor(rng() * colors.length)];
      const y = i * cellH;
      const rot = Math.floor(rng() * 20) - 10;
      shapes += `<g transform="translate(0, ${y}) rotate(${rot}, ${iconSize/2}, ${iconSize/2})">
        <svg viewBox="0 0 24 24" width="${iconSize}" height="${iconSize}">${symbols[type](color)}</svg>
      </g>`;
    }

    return { svg: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${iconSize} ${totalH}" width="${iconSize}" height="${totalH}">${shapes}</svg>`, height: totalH };
  }

  // Build the full reel background
  function buildReelBackground() {
    const container = document.createElement('div');
    container.className = 'hero-reels';
    container.setAttribute('aria-hidden', 'true');

    // Create multiple reel columns at varying positions and speeds
    const reelConfigs = [
      { x: '2%',  size: 40, count: 20, speed: 18, seed: 42,  delay: 0 },
      { x: '10%', size: 32, count: 24, speed: 22, seed: 137, delay: -4 },
      { x: '18%', size: 44, count: 18, speed: 16, seed: 293, delay: -8 },
      { x: '28%', size: 28, count: 28, speed: 25, seed: 71,  delay: -2 },
      { x: '36%', size: 36, count: 22, speed: 20, seed: 511, delay: -6 },
      { x: '45%', size: 42, count: 18, speed: 17, seed: 199, delay: -10 },
      { x: '55%', size: 30, count: 26, speed: 23, seed: 347, delay: -3 },
      { x: '64%', size: 38, count: 20, speed: 19, seed: 89,  delay: -7 },
      { x: '73%', size: 34, count: 22, speed: 21, seed: 461, delay: -1 },
      { x: '82%', size: 44, count: 18, speed: 16, seed: 631, delay: -9 },
      { x: '90%', size: 28, count: 28, speed: 24, seed: 157, delay: -5 },
      { x: '96%', size: 36, count: 22, speed: 20, seed: 773, delay: -11 },
    ];

    reelConfigs.forEach((cfg, i) => {
      const strip = buildReelStrip(cfg.count, cfg.size, cfg.seed);
      const reel = document.createElement('div');
      reel.className = 'hero-reel';
      reel.style.cssText = `
        left: ${cfg.x};
        width: ${cfg.size}px;
        animation-duration: ${cfg.speed}s;
        animation-delay: ${cfg.delay}s;
      `;
      // Double the strip for seamless looping
      reel.innerHTML = strip.svg + strip.svg;
      reel.dataset.stripHeight = strip.height;
      container.appendChild(reel);
    });

    return container;
  }

  // Inject into all hero sections
  document.querySelectorAll('.hero').forEach(hero => {
    // Remove old patterns
    const oldPattern = hero.querySelector('.hero-bg-pattern');
    if (oldPattern) oldPattern.remove();
    const oldFloats = hero.querySelector('.hero-floats');
    if (oldFloats) oldFloats.remove();
    const oldReels = hero.querySelector('.hero-reels');
    if (oldReels) oldReels.remove();

    hero.insertBefore(buildReelBackground(), hero.firstChild);
  });
})();
