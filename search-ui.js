/* Site-wide search + animated counters + sticky CTA */

// === SEARCH ===
(function(){
  var searchBtn = document.getElementById('searchToggle');
  var searchOverlay = document.getElementById('searchOverlay');
  var searchInput = document.getElementById('searchInput');
  var searchResults = document.getElementById('searchResults');
  if (!searchBtn || !searchOverlay) return;

  function openSearch() {
    searchOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    setTimeout(function(){ searchInput.focus(); }, 100);
  }
  function closeSearch() {
    searchOverlay.classList.remove('open');
    document.body.style.overflow = '';
    searchInput.value = '';
    searchResults.innerHTML = '';
  }

  searchBtn.addEventListener('click', openSearch);
  searchOverlay.addEventListener('click', function(e) {
    if (e.target === searchOverlay) closeSearch();
  });
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') closeSearch();
    // Ctrl+K or Cmd+K to open search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      openSearch();
    }
  });

  var debounce;
  searchInput.addEventListener('input', function() {
    clearTimeout(debounce);
    debounce = setTimeout(doSearch, 150);
  });

  function doSearch() {
    var q = searchInput.value.trim().toLowerCase();
    if (q.length < 2) { searchResults.innerHTML = ''; return; }
    if (typeof SEARCH_DATA === 'undefined') return;

    var prefix = '';
    // Detect if we're in a subdirectory
    if (window.location.pathname.includes('/slots/') || 
        window.location.pathname.includes('/reviews/') || 
        window.location.pathname.includes('/promo-codes/') ||
        window.location.pathname.includes('/news/')) {
      prefix = '../';
    }

    var matches = SEARCH_DATA.filter(function(item) {
      return item.name.toLowerCase().indexOf(q) !== -1 ||
             (item.provider && item.provider.toLowerCase().indexOf(q) !== -1);
    }).slice(0, 12);

    if (matches.length === 0) {
      searchResults.innerHTML = '<div class="search-empty">No results for "' + q + '"</div>';
      return;
    }

    var html = '';
    matches.forEach(function(item) {
      var icon = item.type === 'game' ? '\uD83C\uDFB0' : item.type === 'review' ? '\u2B50' : '\uD83D\uDCD6';
      var sub = item.provider ? item.provider + (item.rtp ? ' \u00B7 ' + item.rtp : '') : item.type;
      html += '<a href="' + prefix + item.url + '" class="search-result-item">' +
        '<span class="search-result-icon">' + icon + '</span>' +
        '<div><strong>' + item.name + '</strong><small>' + sub + '</small></div>' +
        '</a>';
    });
    searchResults.innerHTML = html;
  }
})();

// === ANIMATED STAT COUNTERS ===
(function(){
  var counters = document.querySelectorAll('.hero-stat strong');
  if (!counters.length) return;
  var animated = false;

  function animateCounters() {
    if (animated) return;
    animated = true;
    counters.forEach(function(el) {
      var text = el.textContent.trim();
      var suffix = text.replace(/[\d.]/g, ''); // e.g. "+"
      var target = parseFloat(text);
      if (isNaN(target)) return;
      var start = 0;
      var duration = 1200;
      var startTime = null;
      function step(ts) {
        if (!startTime) startTime = ts;
        var progress = Math.min((ts - startTime) / duration, 1);
        // Ease out cubic
        var eased = 1 - Math.pow(1 - progress, 3);
        var current = Math.round(start + (target - start) * eased);
        el.textContent = current + suffix;
        if (progress < 1) requestAnimationFrame(step);
      }
      requestAnimationFrame(step);
    });
  }

  // Trigger when hero-stats-row is in viewport
  if ('IntersectionObserver' in window) {
    var row = document.querySelector('.hero-stats-row');
    if (row) {
      var obs = new IntersectionObserver(function(entries) {
        if (entries[0].isIntersecting) { animateCounters(); obs.disconnect(); }
      }, { threshold: 0.5 });
      obs.observe(row);
    }
  } else {
    animateCounters();
  }
})();

// === STICKY CTA BAR ON SLOT PAGES ===
(function(){
  var demoSection = document.querySelector('.game-demo-section');
  if (!demoSection) return; // Only on slot pages

  // Get game name from h1
  var h1 = document.querySelector('h1');
  var gameName = h1 ? h1.textContent.replace(' Slots Free Play', '').trim() : 'this game';

  // Create sticky bar
  var bar = document.createElement('div');
  bar.className = 'sticky-cta-bar';
  bar.innerHTML = '<div class="sticky-cta-inner">' +
    '<span class="sticky-cta-text">Play <strong>' + gameName + '</strong> Free</span>' +
    '<a href="#game-demo" class="sticky-cta-btn">Play Demo</a>' +
    '</div>';
  document.body.appendChild(bar);

  // Add ID to demo section for scroll target
  demoSection.id = 'game-demo';

  // Show/hide on scroll
  var lastScroll = 0;
  var demoRect;
  function checkSticky() {
    demoRect = demoSection.getBoundingClientRect();
    // Show bar when demo is scrolled out of view (above viewport)
    if (demoRect.bottom < 0) {
      bar.classList.add('visible');
    } else {
      bar.classList.remove('visible');
    }
  }
  window.addEventListener('scroll', checkSticky, { passive: true });

  // Smooth scroll to demo on click
  bar.querySelector('.sticky-cta-btn').addEventListener('click', function(e) {
    e.preventDefault();
    demoSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  });
})();
