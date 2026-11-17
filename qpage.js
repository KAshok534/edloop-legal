// Question pages (/q/<id>): KaTeX auto-render of the question, and the same install buttons as the share page in 404.html
// for question links. These pages are meant to be read and indexed, so unlike 404.html they never jump to Google Play by
// themselves. "Open in EdLoop" shows on Android only (Android App Links open edloop.in/q/... in the app when installed).
(function () {
  var box = document.getElementById('qmath');
  if (!box) return;
  var id = box.getAttribute('data-qid');
  var cfg = window.EDLOOP || {};

  var get = document.getElementById('q-get'), open = document.getElementById('q-open');
  var play = (cfg.play || 'https://play.google.com/store/apps/details?id=in.edloop.jee') +
    '&referrer=utm_source%3Dweb%26utm_content%3Dq_page%26question%3D' + id;
  if (cfg.playLive === false) { // Google Play does not list the app yet (config.js): /get/ explains and keeps the referrer
    play = location.origin + '/get/?utm_source=web&utm_content=q_page&question=' + id;
  }
  if (get) get.href = play;
  if (open && /Android/i.test(navigator.userAgent)) {
    open.href = 'intent://edloop.in/q/' + id + '#Intent;scheme=https;package=in.edloop.jee;S.browser_fallback_url=' +
      encodeURIComponent(play) + ';end';
    open.hidden = false;
  }

  // the question text keeps the bank's own $...$ and $$...$$ delimiters (no \( \[ ones: with them KaTeX's auto-render mis-pairs a $ in some questions)
  var tries = 0;
  (function render() {
    if (window.renderMathInElement) {
      renderMathInElement(box, {
        delimiters: [
          {left: '$$', right: '$$', display: true}, {left: '$', right: '$', display: false}
        ],
        ignoredClasses: ['nomath'], throwOnError: false
      });
    } else if (tries++ < 100) {
      setTimeout(render, 60);
    }
  })();
})();
