// MzansiSlots - Slot Games Directory App
// Search, filter, and browse all games
(function() {
  'use strict';

  // State
  const state = {
    search: '',
    filters: {
      provider: [],
      theme: [],
      volatility: [],
      features: []
    },
    view: 'grouped'
  };

  // Theme mapping - which raw themes belong to each category
  const THEME_MAP = {};
  Object.entries(THEME_CATEGORIES).forEach(([cat, themes]) => {
    themes.forEach(t => { THEME_MAP[t] = cat; });
  });

  // Volatility options
  const VOLATILITY_OPTIONS = ['Low-Medium', 'Medium', 'Medium-High', 'High', 'Very High'];
  
  // Feature options
  const FEATURE_OPTIONS = [
    { key: 'mw', label: 'Megaways' },
    { key: 'bb', label: 'Bonus Buy' },
    { key: 'jp', label: 'Jackpot' }
  ];

  // DOM refs
  const searchInput = document.getElementById('sg-search');
  const searchClear = document.getElementById('sg-search-clear');
  const groupedView = document.getElementById('sg-grouped-view');
  const gridView = document.getElementById('sg-grid-view');
  const noResults = document.getElementById('sg-no-results');
  const resultsCount = document.getElementById('sg-results-count');
  const activeFiltersWrap = document.getElementById('sg-active-filters');
  const activeChips = document.getElementById('sg-active-chips');
  const clearAllBtn = document.getElementById('sg-clear-all');

  // Build filter chips
  function initFilters() {
    // Providers
    const provContainer = document.getElementById('filter-providers');
    PROVIDERS_INFO.forEach(p => {
      if (p.count === 0) return;
      const chip = createChip(p.name, 'provider', p.logo);
      provContainer.appendChild(chip);
    });

    // Themes - use categories
    const themeContainer = document.getElementById('filter-themes');
    const themeCats = Object.keys(THEME_CATEGORIES);
    // Also add themes that appear but aren't categorized
    const usedThemes = new Set();
    GAMES_DATA.forEach(g => { if (g.th) usedThemes.add(g.th); });
    
    themeCats.forEach(cat => {
      // Only show category if we have games with those themes
      const hasGames = THEME_CATEGORIES[cat].some(t => usedThemes.has(t));
      if (hasGames) {
        themeContainer.appendChild(createChip(cat, 'theme'));
      }
    });

    // Volatility
    const volContainer = document.getElementById('filter-volatility');
    VOLATILITY_OPTIONS.forEach(v => {
      const hasGames = GAMES_DATA.some(g => g.v === v);
      if (hasGames) {
        volContainer.appendChild(createChip(v, 'volatility'));
      }
    });

    // Features
    const featContainer = document.getElementById('filter-features');
    FEATURE_OPTIONS.forEach(f => {
      const hasGames = GAMES_DATA.some(g => g[f.key]);
      if (hasGames) {
        featContainer.appendChild(createChip(f.label, 'features'));
      }
    });
  }

  function createChip(label, filterType, logoPath) {
    const btn = document.createElement('button');
    btn.className = 'sg-chip';
    btn.dataset.filter = filterType;
    btn.dataset.value = label;
    
    if (logoPath) {
      const img = document.createElement('img');
      img.src = logoPath;
      img.alt = label;
      img.className = 'sg-chip-logo';
      img.loading = 'lazy';
      img.onerror = function() { this.style.display = 'none'; };
      btn.appendChild(img);
    }
    
    const span = document.createElement('span');
    span.textContent = label;
    btn.appendChild(span);
    
    btn.addEventListener('click', () => toggleFilter(filterType, label, btn));
    return btn;
  }

  function toggleFilter(type, value, btn) {
    const arr = state.filters[type];
    const idx = arr.indexOf(value);
    if (idx === -1) {
      arr.push(value);
      btn.classList.add('active');
    } else {
      arr.splice(idx, 1);
      btn.classList.remove('active');
    }
    render();
  }

  // Filter logic
  function getFilteredGames() {
    return GAMES_DATA.filter(game => {
      // Search
      if (state.search) {
        const q = state.search.toLowerCase();
        const match = game.t.toLowerCase().includes(q) || 
                      game.p.toLowerCase().includes(q) ||
                      game.s.toLowerCase().includes(q);
        if (!match) return false;
      }

      // Provider filter
      if (state.filters.provider.length) {
        if (!state.filters.provider.includes(game.p)) return false;
      }

      // Theme filter - check if game's theme belongs to any selected category
      if (state.filters.theme.length) {
        const gameCat = THEME_MAP[game.th] || '';
        if (!state.filters.theme.includes(gameCat)) return false;
      }

      // Volatility filter
      if (state.filters.volatility.length) {
        if (!state.filters.volatility.includes(game.v)) return false;
      }

      // Features filter
      if (state.filters.features.length) {
        const featureMatch = state.filters.features.every(f => {
          if (f === 'Megaways') return game.mw;
          if (f === 'Bonus Buy') return game.bb;
          if (f === 'Jackpot') return game.jp;
          return true;
        });
        if (!featureMatch) return false;
      }

      return true;
    });
  }

  // Render
  function render() {
    const filtered = getFilteredGames();
    
    // Update count
    resultsCount.textContent = filtered.length + (filtered.length === 1 ? ' game' : ' games');
    
    // Show/hide no results
    const hasResults = filtered.length > 0;
    noResults.style.display = hasResults ? 'none' : 'flex';
    
    // Update active filters display
    updateActiveFilters();
    
    if (state.view === 'grouped') {
      groupedView.style.display = '';
      gridView.style.display = 'none';
      renderGrouped(filtered);
    } else {
      groupedView.style.display = 'none';
      gridView.style.display = '';
      renderGrid(filtered);
    }
  }

  function renderGrouped(games) {
    // Group by provider
    const groups = {};
    games.forEach(g => {
      if (!groups[g.p]) groups[g.p] = [];
      groups[g.p].push(g);
    });

    // Sort groups by game count (desc)
    const sorted = Object.entries(groups).sort((a, b) => b[1].length - a[1].length);

    let html = '';
    sorted.forEach(([provider, provGames]) => {
      const info = PROVIDERS_INFO.find(p => p.name === provider) || {};
      const logoHtml = info.logo 
        ? `<img src="${info.logo}" alt="${provider}" class="sg-panel-logo" loading="lazy" onerror="this.style.display='none'">`
        : '';
      const pageLink = info.page ? ` href="${info.page}"` : '';
      
      html += `
        <div class="sg-provider-panel">
          <div class="sg-panel-header">
            <div class="sg-panel-title-row">
              ${logoHtml}
              <div>
                <h2><a${pageLink} class="sg-panel-link">${provider}</a></h2>
                <span class="sg-panel-count">${provGames.length} game${provGames.length !== 1 ? 's' : ''}</span>
              </div>
            </div>
            ${info.page ? `<a href="${info.page}" class="sg-panel-browse">View all &rarr;</a>` : ''}
          </div>
          <div class="sg-panel-grid">
            ${provGames.map(g => gameCard(g)).join('')}
          </div>
        </div>
      `;
    });

    groupedView.innerHTML = html;
  }

  function renderGrid(games) {
    gridView.innerHTML = `<div class="sg-flat-grid">${games.map(g => gameCard(g)).join('')}</div>`;
  }

  function gameCard(game) {
    const imgHtml = game.img 
      ? `<img src="${game.img}" alt="${game.t}" class="sg-card-thumb" loading="lazy" onerror="this.parentElement.classList.add('sg-card-no-img')">`
      : '';
    
    const badges = [];
    if (game.mw) badges.push('<span class="sg-badge sg-badge-mw">Megaways</span>');
    if (game.bb) badges.push('<span class="sg-badge sg-badge-bb">Bonus Buy</span>');
    if (game.jp) badges.push('<span class="sg-badge sg-badge-jp">Jackpot</span>');
    
    const volClass = game.v ? 'sg-vol-' + game.v.toLowerCase().replace(/[\s-]/g, '') : '';
    const volHtml = game.v ? `<span class="sg-card-vol ${volClass}">${game.v}</span>` : '';
    
    return `
      <a href="slots/${game.s}.html" class="sg-game-card">
        <div class="sg-card-img${game.img ? '' : ' sg-card-no-img'}">
          ${imgHtml}
          ${badges.length ? `<div class="sg-card-badges">${badges.join('')}</div>` : ''}
        </div>
        <div class="sg-card-body">
          <h3>${game.t}</h3>
          <div class="sg-card-meta">
            <span class="sg-card-provider">${game.p}</span>
            ${volHtml}
          </div>
          ${game.r ? `<span class="sg-card-rtp">RTP ${game.r}</span>` : ''}
        </div>
      </a>
    `;
  }

  function updateActiveFilters() {
    const allFilters = [];
    Object.entries(state.filters).forEach(([type, values]) => {
      values.forEach(v => allFilters.push({ type, value: v }));
    });
    
    if (allFilters.length === 0 && !state.search) {
      activeFiltersWrap.style.display = 'none';
      return;
    }
    
    activeFiltersWrap.style.display = 'flex';
    let html = '';
    
    if (state.search) {
      html += `<button class="sg-active-chip" onclick="clearSearch()">Search: "${state.search}" &times;</button>`;
    }
    
    allFilters.forEach(f => {
      html += `<button class="sg-active-chip" data-type="${f.type}" data-value="${f.value}" onclick="removeFilter('${f.type}','${f.value.replace(/'/g, "\\'")}')">${f.value} &times;</button>`;
    });
    
    activeChips.innerHTML = html;
  }

  // Global functions for onclick handlers
  window.removeFilter = function(type, value) {
    const arr = state.filters[type];
    const idx = arr.indexOf(value);
    if (idx !== -1) arr.splice(idx, 1);
    
    // Deactivate chip
    const chip = document.querySelector(`.sg-chip[data-filter="${type}"][data-value="${value}"]`);
    if (chip) chip.classList.remove('active');
    
    render();
  };

  window.clearSearch = function() {
    state.search = '';
    searchInput.value = '';
    searchClear.style.display = 'none';
    render();
  };

  window.clearAllFilters = function() {
    state.search = '';
    searchInput.value = '';
    searchClear.style.display = 'none';
    Object.keys(state.filters).forEach(k => state.filters[k] = []);
    document.querySelectorAll('.sg-chip.active').forEach(c => c.classList.remove('active'));
    render();
  };

  // Search input
  let searchTimeout;
  searchInput.addEventListener('input', () => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      state.search = searchInput.value.trim();
      searchClear.style.display = state.search ? '' : 'none';
      render();
    }, 200);
  });

  searchClear.addEventListener('click', () => {
    window.clearSearch();
    searchInput.focus();
  });

  clearAllBtn.addEventListener('click', () => window.clearAllFilters());

  // View toggle
  document.querySelectorAll('.sg-view-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.sg-view-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      state.view = btn.dataset.view;
      render();
    });
  });

  // Init
  initFilters();
  render();
})();
