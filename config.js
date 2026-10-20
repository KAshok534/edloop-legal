// Site-wide switches. Loaded before site.js on every page and by /get/.
// playLive: set to true (one commit, on the founder's "publish the site") the day Google approves the
// production release and https://play.google.com/store/apps/details?id=in.edloop.jee answers 200.
// While false, every Google Play link on the site is sent through /get/ instead of to a Play page that
// does not exist yet; the install-referrer parameters (utm_*, room, friend, challenge, question) travel with it.
window.EDLOOP = {
  playLive: false,
  play: 'https://play.google.com/store/apps/details?id=in.edloop.jee',
  telegram: 'https://t.me/edloop_in'
};
