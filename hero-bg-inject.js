/* 
  Hero animated background injector
  Creates 3 SVG pattern layers with casino icons that drift diagonally.
  Each layer has different icon sizes, spacing, speed, and direction. 
*/
(function() {
  // SVG icon paths (casino themed) — slot machine, dice, 777, chip, cherry, diamond, cards, star
  const icons = {
    slotMachine: `<path d="M6 2h12a2 2 0 012 2v16a2 2 0 01-2 2H6a2 2 0 01-2-2V4a2 2 0 012-2zm0 2v4h12V4H6zm0 6v4h4v-4H6zm6 0v4h6v-4h-6zm-6 6v4h12v-4H6zm2-8h2v2H8V8zm4 0h2v2h-2V8zm4 0h2v2h-2V8z" fill="currentColor"/>`,
    dice: `<rect x="2" y="2" width="20" height="20" rx="3" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="8" cy="8" r="1.5" fill="currentColor"/><circle cx="16" cy="8" r="1.5" fill="currentColor"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/><circle cx="8" cy="16" r="1.5" fill="currentColor"/><circle cx="16" cy="16" r="1.5" fill="currentColor"/>`,
    seven: `<text x="4" y="20" font-family="Arial Black,sans-serif" font-size="22" font-weight="900" fill="currentColor">7</text>`,
    chip: `<circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="12" r="6" fill="none" stroke="currentColor" stroke-width="1"/><circle cx="12" cy="12" r="2.5" fill="currentColor"/><line x1="12" y1="2" x2="12" y2="6" stroke="currentColor" stroke-width="1.5"/><line x1="12" y1="18" x2="12" y2="22" stroke="currentColor" stroke-width="1.5"/><line x1="2" y1="12" x2="6" y2="12" stroke="currentColor" stroke-width="1.5"/><line x1="18" y1="12" x2="22" y2="12" stroke="currentColor" stroke-width="1.5"/>`,
    cherry: `<circle cx="8" cy="17" r="4" fill="currentColor"/><circle cx="16" cy="15" r="4" fill="currentColor"/><path d="M8 13 C8 6, 12 3, 12 3 C12 3, 16 6, 16 11" fill="none" stroke="currentColor" stroke-width="1.5"/>`,
    diamond: `<path d="M12 2L22 12L12 22L2 12Z" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 2L22 12L12 22L2 12Z" fill="currentColor" opacity="0.15"/>`,
    cards: `<rect x="3" y="4" width="12" height="16" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.2" transform="rotate(-8 9 12)"/><rect x="9" y="4" width="12" height="16" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.2" transform="rotate(8 15 12)"/>`,
    star: `<path d="M12 2l2.9 6.3L22 9.2l-5 5.2L18.2 22 12 18.5 5.8 22 7 14.4l-5-5.2 7.1-.9z" fill="currentColor" opacity="0.3" stroke="currentColor" stroke-width="1"/>`,
    crown: `<path d="M3 18h18v2H3zM3 18l3-8 4 4 3-10 3 10 4-4 3 8z" fill="currentColor" opacity="0.2" stroke="currentColor" stroke-width="1.2"/>`
  };

  // Seedable pseudo-random for consistent icon placement
  function seededRandom(seed) {
    let s = seed;
    return function() {
      s = (s * 16807 + 0) % 2147483647;
      return (s - 1) / 2147483646;
    };
  }

  function buildPatternSVG(iconSet, spacing, iconSize, seed) {
    const cols = 10;
    const rows = 10;
    const svgW = cols * spacing;
    const svgH = rows * spacing;
    const rng = seededRandom(seed);

    let shapes = '';
    let idx = 0;
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        const icon = iconSet[idx % iconSet.length];
        const offsetX = (r % 2 === 0) ? 0 : spacing * 0.5;
        const jitterX = (rng() - 0.5) * spacing * 0.3;
        const jitterY = (rng() - 0.5) * spacing * 0.3;
        const x = c * spacing + offsetX + jitterX + spacing * 0.2;
        const y = r * spacing + jitterY + spacing * 0.2;
        const rot = Math.floor(rng() * 60) - 30;
        shapes += `<g transform="translate(${x.toFixed(1)}, ${y.toFixed(1)}) rotate(${rot}, ${iconSize/2}, ${iconSize/2})">
          <svg viewBox="0 0 24 24" width="${iconSize}" height="${iconSize}" color="rgba(255,255,255,1)">${icons[icon]}</svg>
        </g>`;
        idx++;
      }
    }

    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${svgW} ${svgH}" preserveAspectRatio="none">${shapes}</svg>`;
  }

  // Three layers with different configs
  const layer1SVG = buildPatternSVG(
    ['slotMachine', 'dice', 'seven', 'chip', 'cherry', 'diamond', 'cards', 'star', 'crown'],
    130, 38, 42
  );
  const layer2SVG = buildPatternSVG(
    ['diamond', 'seven', 'chip', 'star', 'slotMachine', 'cherry', 'crown', 'dice', 'cards'],
    110, 30, 137
  );
  const layer3SVG = buildPatternSVG(
    ['cherry', 'cards', 'star', 'dice', 'diamond', 'seven', 'crown', 'chip', 'slotMachine'],
    150, 24, 293
  );

  // Inject into all hero sections
  document.querySelectorAll('.hero').forEach(hero => {
    // Remove old emoji floats if present
    const oldFloats = hero.querySelector('.hero-floats');
    if (oldFloats) oldFloats.remove();

    const container = document.createElement('div');
    container.className = 'hero-bg-pattern';
    container.setAttribute('aria-hidden', 'true');
    container.innerHTML = `
      <div class="hero-bg-layer hero-bg-layer--1">${layer1SVG}</div>
      <div class="hero-bg-layer hero-bg-layer--2">${layer2SVG}</div>
      <div class="hero-bg-layer hero-bg-layer--3">${layer3SVG}</div>
    `;
    hero.insertBefore(container, hero.firstChild);
  });
})();
