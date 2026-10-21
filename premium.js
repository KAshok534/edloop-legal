'use strict';
// The 30-second film on the home page. It plays muted and looping, pauses when it scrolls out of view or the tab is hidden,
// and has real Pause and Sound buttons (a loop that never stops needs a way to stop it). People who ask for reduced motion
// or Data Saver get the poster and a Play button: nothing downloads until they press it.
(function () {
  const player = document.querySelector('.p-player');
  if (!player) return;
  const video = player.querySelector('video');
  const playBtn = player.querySelector('[data-film-play]');
  const soundBtn = player.querySelector('[data-film-sound]');
  const FILES = {
    wide: { src: 'assets/video/edloop-together-1080.mp4', poster: 'assets/video/poster-wide.jpg' },   // 1920x1080, 3.6 MB
    tall: { src: 'assets/video/edloop-together-vertical-720.mp4', poster: 'assets/video/poster-tall.jpg' } // 720x1280, 2.0 MB
  };
  const narrow = window.matchMedia('(max-width: 700px)');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const saver = !!(navigator.connection && navigator.connection.saveData);
  let userPaused = reduce || saver;   // a person who has not asked for motion starts paused
  let visible = true;

  const icon = {
    play: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l13 8-13 8z" fill="currentColor" stroke="none"/></svg>',
    pause: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5v14M16 5v14"/></svg>',
    soundOn: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M16.5 8.5a5 5 0 0 1 0 7"/></svg>',
    soundOff: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6h4l5 4V5L8 9z"/><path d="M17 9l5 6M22 9l-5 6"/></svg>'
  };

  function choose() {
    const mode = narrow.matches ? 'tall' : 'wide';
    if (video.dataset.mode === mode) return;
    video.dataset.mode = mode;
    video.poster = FILES[mode].poster;
    video.preload = userPaused ? 'none' : 'auto';
    video.src = FILES[mode].src;
    if (!userPaused && visible) start();
  }
  function start() { const p = video.play(); if (p && p.catch) p.catch(() => { setPlayLabel(); }); }
  function setPlayLabel() {
    const playing = !video.paused && !video.ended;
    playBtn.innerHTML = (playing ? icon.pause : icon.play) + '<span>' + (playing ? 'Pause film' : 'Play film') + '</span>';
    playBtn.setAttribute('aria-pressed', String(playing));
  }
  function setSoundLabel() {
    const on = !video.muted;
    soundBtn.innerHTML = (on ? icon.soundOn : icon.soundOff) + '<span>' + (on ? 'Sound on' : 'Sound off') + '</span>';
    soundBtn.setAttribute('aria-pressed', String(on));
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
    setSoundLabel();
  });
  video.addEventListener('play', setPlayLabel);
  video.addEventListener('pause', setPlayLabel);
  narrow.addEventListener('change', choose);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) video.pause(); else if (!userPaused && visible) start();
  });
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(entries => {
      visible = entries.some(e => e.isIntersecting);
      if (!visible) video.pause(); else if (!userPaused) start();
    }, { threshold: 0.25 }).observe(player);
  }
  choose();
  setPlayLabel();
  setSoundLabel();
})();
