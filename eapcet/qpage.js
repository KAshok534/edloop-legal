// EAPCET Question pages (/eapcet/q/<id>): KaTeX auto-render of the question, and install buttons for EdLoop EAPCET.
(function () {
  var box = document.getElementById('qmath');
  if (!box) return;
  var id = box.getAttribute('data-qid');
  var cfg = window.EDLOOP || {};

  var get = document.getElementById('q-get'), open = document.getElementById('q-open');
  var play = (cfg.playEapcet || 'https://play.google.com/store/apps/details?id=in.edloop.eapcet') +
    '&referrer=utm_source%3Dweb%26utm_content%3Dq_page%26question%3D' + id;
  if (cfg.playLive === false) {
    play = location.origin + '/get/?utm_source=web&utm_content=q_page&question=' + id;
  }
  if (get) get.href = play;
  if (open && /Android/i.test(navigator.userAgent)) {
    open.href = 'intent://edloop.in/eapcet/q/' + id + '#Intent;scheme=https;package=in.edloop.eapcet;S.browser_fallback_url=' +
      encodeURIComponent(play) + ';end';
    open.hidden = false;
  }

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
