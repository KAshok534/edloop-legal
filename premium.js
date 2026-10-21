'use strict';
// Premium home page behaviour. Everything here is an enhancement: without JavaScript the page shows the film with
// native controls, the full year grid (2026) and a scrollable gallery.
(function () {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Header: transparent over the hero, solid once the page scrolls; solid while the phone menu is open.
  const header = document.querySelector('.site-header');
  const menu = document.querySelector('.menu-toggle');
  const onScrollHeader = () => header && header.classList.toggle('scrolled', window.scrollY > 24);
  if (header) {
    onScrollHeader();
    window.addEventListener('scroll', onScrollHeader, { passive: true });
    if (menu) menu.addEventListener('click', () => setTimeout(() => header.classList.toggle('open', menu.getAttribute('aria-expanded') === 'true'), 0));
  }

  // The film: muted loop with real Pause and Sound buttons. Pauses off screen and in a hidden tab. Phones get the
  // vertical cut. Reduced motion and Data Saver get the poster and a Play button; nothing downloads until pressed.
  (function film() {
    const frame = document.querySelector('.film-frame');
    if (!frame) return;
    const video = frame.querySelector('video');
    const playBtn = frame.querySelector('[data-film-play]');
    const soundBtn = frame.querySelector('[data-film-sound]');
    // Phones get the vertical cut, wider screens the landscape one. Retina, 4K and other large screens (frame wider
    // than about 2200 real pixels) get 1440p; slow connections (2G/3G) get the smaller files.
    const FILES = {
      wide: { src: 'assets/video/edloop-together-1080.mp4', poster: 'assets/video/poster-wide.jpg' },          // 3.6 MB
      wideHD: { src: 'assets/video/edloop-together-1440.mp4', poster: 'assets/video/poster-wide.jpg' },        // 6.4 MB
      tall: { src: 'assets/video/edloop-together-vertical-720.mp4', poster: 'assets/video/poster-tall.jpg' },  // 2.0 MB
      tallHD: { src: 'assets/video/edloop-together-vertical-1080.mp4', poster: 'assets/video/poster-tall-1080.jpg' } // 4.5 MB
    };
    const conn = navigator.connection || {};
    const slow = /2g|3g/.test(conn.effectiveType || '');
    const narrow = window.matchMedia('(max-width: 700px)');
    const saver = !!(navigator.connection && navigator.connection.saveData);
    let userPaused = reduce || saver;
    let visible = false;
    const icon = {
      play: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l13 8-13 8z" fill="currentColor" stroke="none"/></svg>',
      pause: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14M16 5v14"/></svg>',
      on: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16.5 8.5a5 5 0 0 1 0 7"/></svg>',
      off: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M17 9l5 6M22 9l-5 6"/></svg>'
    };
    const start = () => { const p = video.play(); if (p && p.catch) p.catch(() => label()); };
    function label() {
      const playing = !video.paused && !video.ended;
      playBtn.innerHTML = (playing ? icon.pause : icon.play) + '<span>' + (playing ? 'Pause' : 'Play film') + '</span>';
      playBtn.setAttribute('aria-pressed', String(playing));
      const on = !video.muted;
      soundBtn.innerHTML = (on ? icon.on : icon.off) + '<span>' + (on ? 'Sound on' : 'Sound off') + '</span>';
      soundBtn.setAttribute('aria-pressed', String(on));
    }
    function choose() {
      const real = frame.clientWidth * (window.devicePixelRatio || 1);
      const mode = narrow.matches ? (slow ? 'tall' : 'tallHD') : (!slow && real > 2200 ? 'wideHD' : 'wide');
      if (video.dataset.mode === mode) return;
      video.dataset.mode = mode;
      video.poster = FILES[mode].poster;
      video.preload = userPaused ? 'none' : 'auto';
      video.src = FILES[mode].src;
      if (!userPaused && visible) start();
    }
    video.removeAttribute('controls');
    video.muted = true;
    playBtn.hidden = false;
    soundBtn.hidden = false;
    playBtn.addEventListener('click', () => {
      if (video.paused || video.ended) { userPaused = false; video.preload = 'auto'; start(); } else { userPaused = true; video.pause(); }
    });
    soundBtn.addEventListener('click', () => {
      video.muted = !video.muted;
      if (!video.muted && video.paused) { userPaused = false; start(); }
      label();
    });
    video.addEventListener('play', label);
    video.addEventListener('pause', label);
    narrow.addEventListener('change', choose);
    document.addEventListener('visibilitychange', () => { if (document.hidden) video.pause(); else if (!userPaused && visible) start(); });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(entries => {
        visible = entries.some(e => e.isIntersecting);
        if (!visible) video.pause(); else if (!userPaused) start();
      }, { threshold: 0.2 }).observe(frame);
    } else { visible = true; }
    choose();
    label();
  })();

  // Since 2002: while the section is pinned, scrolling walks the year from the first paper to the last; the grid
  // lights up to that year and the line under the year gives its papers and the running total.
  (function years() {
    const section = document.querySelector('.years');
    const dataEl = document.getElementById('years-data');
    if (!section || !dataEl || reduce) return;
    let data;
    try { data = JSON.parse(dataEl.textContent); } catch (e) { return; }
    const num = section.querySelector('.yr-num');
    const exam = section.querySelector('.yr-exam');
    const say = section.querySelector('.yr-say');
    const bar = section.querySelector('.yr-bar');
    const byIndex = [];
    section.querySelectorAll('.yr-cells i').forEach(c => { const i = Number(c.dataset.i); (byIndex[i] = byIndex[i] || []).push(c); });
    const notes = [[2002, 'AIEEE: one paper a year.'], [2013, 'JEE Main replaces AIEEE.'], [2019, 'Online, in two sessions with many shifts.']];
    const cumulative = data.papers.reduce((acc, p, i) => { acc.push((acc[i - 1] || 0) + p); return acc; }, []);
    // Pin only when the whole section fits the window (short landscape tablets, small laptops): otherwise it stays a
    // normal section showing the full grid, so nothing is ever cut off.
    const layout = section.querySelector('.years-layout');
    function fits() {
      document.documentElement.classList.add('motion');
      const pin = section.querySelector('.years-pin');
      const cs = getComputedStyle(pin);
      const need = layout.getBoundingClientRect().height + parseFloat(cs.paddingTop) + parseFloat(cs.paddingBottom);
      const ok = need <= window.innerHeight;
      if (!ok) {
        document.documentElement.classList.remove('motion');
        num.textContent = data.years[data.years.length - 1];
        exam.textContent = 'JEE Main';
        say.textContent = data.total + ' papers in all, sorted by chapter.';
        byIndex.forEach(cells => cells.forEach(c => c.classList.remove('off')));
        if (bar) bar.style.setProperty('--p', '1');
      }
      return ok;
    }
    let pinned = fits();
    let shown = -1, ticking = false;
    function render() {
      ticking = false;
      if (!pinned) return;
      const rect = section.getBoundingClientRect();
      const run = section.offsetHeight - window.innerHeight;
      const p = run > 0 ? Math.min(1, Math.max(0, -rect.top / run)) : 1;
      if (bar) bar.style.setProperty('--p', p.toFixed(3));
      const idx = Math.round(p * (data.years.length - 1));
      if (idx === shown) return;
      shown = idx;
      const year = data.years[idx];
      num.textContent = year;
      exam.textContent = year <= 2012 ? 'AIEEE' : 'JEE Main';
      const papers = data.papers[idx];
      const note = notes.filter(n => n[0] <= year).pop();
      const last = idx === data.years.length - 1;
      say.textContent = (last ? data.total + ' papers in all, sorted by chapter. ' : '') +
        papers + (papers === 1 ? ' paper' : ' papers') + ' that year, ' + cumulative[idx] + ' so far. ' + (last ? '' : note ? note[1] : '');
      byIndex.forEach((cells, i) => cells.forEach(c => c.classList.toggle('off', i > idx)));
    }
    const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(render); } };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', () => { pinned = fits(); shown = -1; onScroll(); });
    render();
  })();

  // Better with friends (desktop): the step nearest the middle of the screen is active, and the sticky phone shows its screen.
  (function steps() {
    const list = document.querySelectorAll('.together-layout .steps li');
    const shots = document.querySelectorAll('.stage .shot');
    if (!list.length || !shots.length) return;
    const activate = i => { list.forEach((li, k) => li.classList.toggle('active', k === i)); shots.forEach((s, k) => s.classList.toggle('active', k === i)); };
    activate(0);
    if (!('IntersectionObserver' in window)) return;
    const io = new IntersectionObserver(entries => {
      entries.forEach(e => { if (e.isIntersecting) activate([...list].indexOf(e.target)); });
    }, { rootMargin: '-45% 0px -45% 0px' });
    list.forEach(li => io.observe(li));
  })();

  // Gallery arrows: one card at a time.
  (function gallery() {
    const track = document.querySelector('.track');
    if (!track) return;
    document.querySelectorAll('[data-gallery]').forEach(btn => btn.addEventListener('click', () => {
      const card = track.querySelector('figure');
      const step = card ? card.getBoundingClientRect().width + parseFloat(getComputedStyle(track).columnGap || 24) : 300;
      track.scrollBy({ left: btn.dataset.gallery === 'next' ? step : -step, behavior: reduce ? 'auto' : 'smooth' });
    }));
  })();
})();
