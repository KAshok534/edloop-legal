// Site-wide switches. Loaded before site.js on every page and by /get/.
// playLive: set to true (one commit, on the founder's "publish the site") the day Google approves the
// production release and https://play.google.com/store/apps/details?id=in.edloop.jee answers 200.
// While false, every Google Play link on the site is sent through /get/ instead of to a Play page that
// does not exist yet; the install-referrer parameters (utm_*, room, friend, challenge, question) travel with it.
window.EDLOOP = {
  playLive: true,
  play: 'https://play.google.com/store/apps/details?id=in.edloop.jee',
  // EdLoop EAPCET: set eapcetLive to true (on the founder's "publish the site") the day Google approves it and
  // https://play.google.com/store/apps/details?id=in.edloop.eapcet answers 200. While false, the site says it is in review and shows no Play link.
  eapcetLive: false,
  playEapcet: 'https://play.google.com/store/apps/details?id=in.edloop.eapcet',
  telegram: 'https://t.me/edloop_in'
};
