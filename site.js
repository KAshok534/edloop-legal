'use strict';
const menuButton = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
function closeMenu() { menuButton.setAttribute('aria-expanded', 'false'); mobileNav.hidden = true; }
menuButton.addEventListener('click', () => { const open = menuButton.getAttribute('aria-expanded') !== 'true'; menuButton.setAttribute('aria-expanded', String(open)); mobileNav.hidden = !open; });
mobileNav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape' && !mobileNav.hidden) { closeMenu(); menuButton.focus(); } });
window.matchMedia('(min-width: 621px)').addEventListener('change', event => { if (event.matches) closeMenu(); });

const motionButton = document.querySelector('#motion-toggle');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let userPausedMotion = false;
function updateMotion() {
  const paused = userPausedMotion || reducedMotion.matches;
  document.documentElement.classList.toggle('motion-paused', paused);
  motionButton.setAttribute('aria-pressed', String(paused));
  motionButton.textContent = reducedMotion.matches ? 'Reduced motion enabled' : paused ? 'Play logo motion' : 'Pause logo motion';
  motionButton.disabled = reducedMotion.matches;
}
motionButton.addEventListener('click', () => { userPausedMotion = !userPausedMotion; updateMotion(); });
reducedMotion.addEventListener('change', updateMotion);
updateMotion();
