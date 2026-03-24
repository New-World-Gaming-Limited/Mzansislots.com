/* ═══════════════════════════════════════════════════════
   MZANSI SLOTS - Shared JavaScript
   ═══════════════════════════════════════════════════════ */

// Theme toggle with persistent preference
(function(){
  var LS = window['local'+'Storage'];
  const t = document.querySelector('[data-theme-toggle]');
  const r = document.documentElement;
  // Check saved preference first, then system preference
  var saved = null;
  try { saved = LS ? LS.getItem('mzansi-theme') : null; } catch(e) {}
  let d = saved || ((window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'dark' : 'light');
  r.setAttribute('data-theme', d);
  if (t) {
    updateIcon();
    t.addEventListener('click', () => {
      d = d === 'dark' ? 'light' : 'dark';
      r.setAttribute('data-theme', d);
      try { if (LS) LS.setItem('mzansi-theme', d); } catch(e) {}
      t.setAttribute('aria-label', 'Switch to ' + (d === 'dark' ? 'light' : 'dark') + ' mode');
      updateIcon();
    });
  }
  function updateIcon() {
    if (!t) return;
    t.innerHTML = d === 'dark'
      ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
      : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  }
})();

// Slide menu toggle (hamburger on all viewports)
(function(){
  const btn = document.querySelector('.hamburger-toggle');
  const menu = document.getElementById('slideMenu');
  const overlay = document.getElementById('slideOverlay');
  const closeBtn = menu ? menu.querySelector('.slide-menu-close') : null;
  function openMenu() {
    if (!menu) return;
    menu.classList.add('open');
    if (overlay) overlay.classList.add('open');
    document.body.style.overflow = 'hidden';
    if (btn) btn.setAttribute('aria-expanded', 'true');
  }
  function closeMenu() {
    if (!menu) return;
    menu.classList.remove('open');
    if (overlay) overlay.classList.remove('open');
    document.body.style.overflow = '';
    if (btn) btn.setAttribute('aria-expanded', 'false');
  }
  if (btn) btn.addEventListener('click', openMenu);
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  if (overlay) overlay.addEventListener('click', closeMenu);
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeMenu();
  });
})();

// Legacy mobile nav toggle (fallback)
(function(){
  const btn = document.querySelector('.mobile-toggle');
  const nav = document.querySelector('.mobile-nav');
  if (btn && nav) {
    btn.addEventListener('click', () => {
      nav.classList.toggle('open');
    });
  }
})();

// FAQ accordion
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.parentElement;
    const wasOpen = item.classList.contains('open');
    // Close all
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
    // Toggle current
    if (!wasOpen) item.classList.add('open');
  });
});

// Search filter (generic)
function initSearch(inputSelector, itemSelector, textSelector) {
  const input = document.querySelector(inputSelector);
  if (!input) return;
  input.addEventListener('input', () => {
    const query = input.value.toLowerCase().trim();
    document.querySelectorAll(itemSelector).forEach(item => {
      const text = item.querySelector(textSelector)?.textContent.toLowerCase() || item.textContent.toLowerCase();
      item.style.display = text.includes(query) ? '' : 'none';
    });
  });
}

// Provider filter
function initProviderFilter() {
  const buttons = document.querySelectorAll('.provider-btn');
  const cards = document.querySelectorAll('.game-card');
  if (!buttons.length || !cards.length) return;

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const provider = btn.dataset.provider;
      cards.forEach(card => {
        if (!provider || provider === 'all') {
          card.style.display = '';
        } else {
          const cardProvider = card.dataset.provider || '';
          card.style.display = cardProvider === provider ? '' : 'none';
        }
      });
    });
  });
}

// Scroll reveal animation
function initScrollReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('revealed');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}

// Back to top button
function initBackToTop() {
  const btn = document.createElement('button');
  btn.className = 'back-to-top';
  btn.setAttribute('aria-label', 'Back to top');
  btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg>';
  document.body.appendChild(btn);
  
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        btn.classList.toggle('visible', window.scrollY > 600);
        ticking = false;
      });
      ticking = true;
    }
  });
  
  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

// Active nav link highlighting
function initActiveNav() {
  const path = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav-desktop a, .slide-menu a, .mobile-nav a').forEach(link => {
    const href = link.getAttribute('href')?.split('/').pop() || '';
    if (href === path) {
      link.classList.add('nav-active');
    }
  });
}

// Init
document.addEventListener('DOMContentLoaded', () => {
  initProviderFilter();
  initScrollReveal();
  initBackToTop();
  initActiveNav();
});
