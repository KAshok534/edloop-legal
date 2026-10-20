'use strict';
const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
function closeMenu() { menuButton.setAttribute('aria-expanded', 'false'); mobileNav.hidden = true; }
menuButton.addEventListener('click', () => { const open = menuButton.getAttribute('aria-expanded') !== 'true'; menuButton.setAttribute('aria-expanded', String(open)); mobileNav.hidden = !open; });
mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape' && !mobileNav.hidden) { closeMenu(); menuButton.focus(); } });
window.matchMedia('(min-width: 621px)').addEventListener('change', event => { if (event.matches) closeMenu(); });

// eo logo: play the header at once and again on hover; play the footer when it scrolls in
(function () {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const play = el => { el.classList.remove('eo-wait', 'eo-anim'); void el.getBoundingClientRect(); el.classList.add('eo-anim'); };
  const header = document.querySelector('.site-header .brand');
  if (header) {
    play(header);
    if (!reduce) {
      let last = Date.now();
      header.addEventListener('mouseenter', () => { const now = Date.now(); if (now - last > 2200) { last = now; play(header); } });
    }
  }
  const footer = document.querySelector('.site-footer .brand');
  if (footer) {
    if (reduce || !('IntersectionObserver' in window)) { play(footer); return; }
    const io = new IntersectionObserver(entries => {
      if (entries.some(e => e.isIntersecting)) { play(footer); io.disconnect(); }
    }, { threshold: 0.6 });
    io.observe(footer);
  }
})();

// Google Play does not list the app until Google approves the production release (config.js playLive).
// Until then every Play link on the site goes through /get/, carrying its install-referrer parameters.
(function () {
  const cfg = window.EDLOOP;
  if (!cfg || cfg.playLive) return;
  document.querySelectorAll('a[href^="https://play.google.com/store/apps/details?id=in.edloop.jee"]').forEach(a => {
    const m = a.getAttribute('href').match(/[?&]referrer=([^&]*)/);
    const q = m ? decodeURIComponent(m[1]) : '';
    a.href = '/get/' + (q ? '?' + q : '');
    a.removeAttribute('target');
  });
})();
