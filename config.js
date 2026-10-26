// Site-wide switches. Loaded before site.js on every page and by /get/.
// playLive: set to true (one commit, on the founder's "publish the site") the day Google approves the
// production release and https://play.google.com/store/apps/details?id=in.edloop.jee answers 200.
// While false, every Google Play link on the site is sent through /get/ instead of to a Play page that
// does not exist yet; the install-referrer parameters (utm_*, room, friend, challenge, question) travel with it.
window.EDLOOP = {
  playLive: true,
  play: 'https://play.google.com/store/apps/details?id=in.edloop.jee',
  // EdLoop EAPCET: true since 2026-10-26 (founder: treat it as on Google Play everywhere; Google's review was due within
  // 48 hours). When true the site shows its Play link and share pages tagged ?app=eapcet go to its listing; set false
  // to show "in Google's final review" instead and keep people off the Play page.
  eapcetLive: true,
  playEapcet: 'https://play.google.com/store/apps/details?id=in.edloop.eapcet',
  telegram: 'https://t.me/edloop_in'
};
