'use strict';
const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
function closeMenu() { menuButton.setAttribute('aria-expanded', 'false'); mobileNav.hidden = true; }
menuButton.addEventListener('click', () => { const open = menuButton.getAttribute('aria-expanded') !== 'true'; menuButton.setAttribute('aria-expanded', String(open)); mobileNav.hidden = !open; });
mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape' && !mobileNav.hidden) { closeMenu(); menuButton.focus(); } });
window.matchMedia('(min-width: 621px)').addEventListener('change', event => { if (event.matches) closeMenu(); });

// eo logo: play the header after the intro (first visit) or at once; replay on hover; play the footer when it scrolls in
(function () {
  const root = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const play = el => { el.classList.remove('eo-wait', 'eo-anim'); void el.getBoundingClientRect(); el.classList.add('eo-anim'); };
  const header = document.querySelector('.site-header .brand');
  const intro = document.querySelector('.eo-intro');
  const finishIntro = () => { root.classList.add('eo-done'); if (header) play(header); };
  if (root.classList.contains('eo-first') && intro) {
    // end when the drawing has finished ("Loop" landed) plus a short hold; a tap skips; never longer than 3.2s
    let ended = false;
    const end = () => { if (!ended) { ended = true; clearTimeout(cap); finishIntro(); } };
    const cap = setTimeout(end, 3200);
    const word = intro.querySelector('.eo-loop');
    if (word) word.addEventListener('animationend', () => setTimeout(end, 350), { once: true });
    intro.addEventListener('click', end, { once: true });
  } else if (header) {
    play(header);
  }
  if (header && !reduce) {
    let last = 0;
    header.addEventListener('mouseenter', () => { const now = Date.now(); if (now - last > 2200) { last = now; play(header); } });
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
