# edloop.in

The public website of EdLoop (EDLOOP TECHNOLOGIES): the home page for the EdLoop JEE app, the About page, the privacy
policy, the terms, the account-deletion page, the `/get` install link and the share pages that the app's room, friend,
challenge and question links open.

Static HTML, CSS and JavaScript, served by GitHub Pages from `main` (`CNAME` = edloop.in, `.nojekyll`). There is no build
step, no framework, no analytics and no cookies. **Pushing `main` publishes the site within about a minute.**

## Pages

| Path | File | What it is |
|---|---|---|
| `/` | `index.html` | The home page: hero, the 30-second film, the numbers, the "Twenty-five years of papers" year sequence, "Better with friends", the app gallery, a real past question to try, "Every answer has a source", the end card |
| `/about.html` | `about.html` | The company and the founder |
| `/privacy.html`, `/terms.html`, `/delete-account.html` | same | Privacy policy, terms of service, how to delete an account (linked from Google Play) |
| `/get/` | `get/index.html` | One install link for bios, QR codes and flyers. Forwards to Google Play, carrying `utm_*` and the app's install-referrer keys (`room`, `friend`, `challenge`, `question`) |
| `/r/<code>`, `/f/<id>`, `/c/<code>`, `/q/<question id>` | `404.html` | Share pages. GitHub Pages serves `404.html` for any unknown path; its script reads the path and shows the room, friend, challenge or question page. On Android it goes on to Google Play once per tab; when the app is installed, Android opens the link in the app instead (`.well-known/assetlinks.json`) Two apps share these links: EdLoop EAPCET adds `?app=eapcet` to the room, friend and challenge links it shares, and its question ids start `q-apeapcet-` or `q-tseapcet-`; those pages name EAPCET and open or install EdLoop EAPCET. Links without the tag belong to EdLoop JEE. |

## Files

| File | Role |
|---|---|
| `premium.css` | The design system, loaded by every page: colour tokens, the Manrope font (self-hosted), header, footer, buttons, the home sections, the eo logo animation, the question card |
| `pages.css` | The inner pages (About, the legal pages, `/get`, the share pages) |
| `premium.js` | Header state on every page; on the home page the film player, the year sequence, the sticky phone and the gallery |
| `site.js` | Mobile menu, logo replay, and the Play-link routing used while `playLive` is false |
| `home.js` | The home page's interactive question and the phone install bar |
| `config.js` | Site switches: `playLive` (EdLoop JEE's Google Play buttons go straight to the listing when true) and `eapcetLive` (EdLoop EAPCET's Play link shows, and its share pages forward to its listing, when true; false shows "in Google's final review") |
| `tools/make_years.py` | Rebuilds the year grid in `index.html` from the content database (between the `years:start`/`years:end` comments) |
| `tools/encode_film.py` | Makes the web copies of the film and its posters from the full-resolution masters |
| `assets/` | Brand files, app screens (`site-redesign/`), the film (`video/`), the founder photo (`team/`) |

Not used by any page any more, kept until a clean-up commit: `home.css`, `legal.css`, `style.css`, `script.js`,
`tools/make_hero_card.py`.

## The film

Four copies, chosen in `premium.js` by screen: 1080×1920 for phones (720×1280 on 2G/3G), 1920×1080 for laptops and
2560×1440 when the frame is wider than about 2200 real pixels. It is shown full width at its own shape and never cropped.
It plays muted and looping only while visible; Pause and Sound are real buttons. Reduced motion and Data Saver get the
poster until Play is pressed. The masters are not in this repository; only these web copies are.

## Numbers

Every number on the site (questions, papers, years, the year grid) comes from the content database, never from memory.
When the question bank grows, update the meta description, the og:description, the numbers list under the film, rerun
`tools/make_years.py`, and regenerate the link-preview card (`assets/brand/make_social.html`, rendered with
`assets/brand/render_cards.py`). Say "200 papers", never "every paper".

## Changing the site

1. Work on a `feature/*` branch.
2. Test locally with a static server that answers unknown paths with `404.html`, as GitHub Pages does (a plain
   `python -m http.server` cannot show the share pages). Check desktop and phone widths: no horizontal scrolling, no
   console errors, the film never cropped.
3. Every change to a CSS or JS file bumps its `?v=` number on every page that loads it: GitHub Pages lets browsers cache
   files for ten minutes.
4. Publish by fast-forwarding `main` to the branch, only with the owner's approval. Wait for the Pages build, then check
   the live pages.

## Rules

- Nothing private goes into this repository: no plans, keys, personal data or exam source files.
- The questions on the home page are real past questions with the official final key; never copy a coaching
  institute's material.
- No loaders or delays to show the logo; no tracking scripts without an update to the privacy policy first.

© 2026 EDLOOP TECHNOLOGIES. The site's text, design and code belong to EDLOOP TECHNOLOGIES; past exam questions belong to
the bodies that set them. EdLoop is independent of NTA, APSCHE, TGCHE and JNTU.
