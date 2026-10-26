# edloop.in

The public website of EdLoop (EDLOOP TECHNOLOGIES): the EdLoop home with its two apps, a page for each app (EdLoop JEE
at `/jee/`, EdLoop EAPCET at `/eapcet/`), the About page, the privacy policy, the terms, the account-deletion page, the
`/get` install link and the share pages that the apps' room, friend, challenge and question links open.

Static HTML, CSS and JavaScript, served by GitHub Pages from `main` (`CNAME` = edloop.in, `.nojekyll`). There is no build
step, no framework, no analytics and no cookies. **Pushing `main` publishes the site within about a minute.**

## Pages

| Path | File | What it is |
|---|---|---|
| `/` | `index.html` | The EdLoop home: "Real past papers, sorted by chapter", the two apps' phones, "Pick your exam" (EdLoop JEE and EdLoop EAPCET cards with their numbers and marking, EdLoop Campus coming soon), "One account, every app", "Every answer has a source", the end card. A small script sends links to the old home sections (`/#watch`, `#together`, `#inside`, `#practice`, used in bios and posts until October 2026) to the same section of `/jee/` |
| `/jee/` | `jee/index.html` | EdLoop JEE: hero, the 30-second film, the numbers, the "Twenty-five years of papers" year sequence, "Better with friends", the app gallery, a real past question to try (+4 / −1), "Every answer has a source", a link to EdLoop EAPCET, the end card |
| `/eapcet/` | `eapcet/index.html` | EdLoop EAPCET, the same sections in teal: three app screens and the numbers, the 2022–2026 year sequence (AP and TS), "AP and TS in one app" (the paper, the marking), eight app screens, three real 2026 questions with the councils' keys (+1 / 0), "Every answer has a source", a link to EdLoop JEE |
| `/about.html` | `about.html` | The company and the founder |
| `/privacy.html`, `/terms.html`, `/delete-account.html` | same | Privacy policy, terms of service, how to delete an account (linked from Google Play) |
| `/get/` | `get/index.html` | One install link for bios, QR codes and flyers. Forwards to Google Play, carrying `utm_*` and the app's install-referrer keys (`room`, `friend`, `challenge`, `question`) |
| `/r/<code>`, `/f/<id>`, `/c/<code>`, `/q/<question id>` | `404.html` | Share pages. GitHub Pages serves `404.html` for any unknown path; its script reads the path and shows the room, friend, challenge or question page. On Android it goes on to Google Play once per tab; when the app is installed, Android opens the link in the app instead (`.well-known/assetlinks.json`) Two apps share these links: EdLoop EAPCET adds `?app=eapcet` to the room, friend and challenge links it shares, and its question ids start `q-apeapcet-` or `q-tseapcet-`; those pages name EAPCET and open or install EdLoop EAPCET. Links without the tag belong to EdLoop JEE. |

## Files

| File | Role |
|---|---|
| `premium.css` | The design system, loaded by every page: colour tokens, the Manrope font (self-hosted), header, footer, buttons, the app-page sections, the eo logo animation, the question card; at the end, the home's app cards and EdLoop EAPCET's teal (`.app-eapcet`) |
| `pages.css` | The inner pages (About, the legal pages, `/get`, the share pages) |
| `premium.js` | Header state on every page; on the app pages the film player (files found from the page's folder: `<html data-base="../">`), the year sequence (the exam's name and the notes come from the page's `years-data` JSON, JEE's by default), the sticky phone and the gallery |
| `site.js` | Mobile menu, logo replay, and the Play-link routing used while `playLive` is false |
| `home.js` | The app pages' interactive question (JEE's questions by default; a page can give its own in a `#demo-data` JSON and its marking in `data-right` / `data-wrong` on `.practice-demo`) and the phone install bar |
| `config.js` | Site switches: `playLive` (EdLoop JEE's Google Play buttons go straight to the listing when true) and `eapcetLive` (EdLoop EAPCET's Play link shows, and its share pages forward to its listing, when true; false shows "in Google's final review") |
| `tools/make_years.py` | Rebuilds an app page's year grid from the content database (between the `years:start`/`years:end` comments): `jee/index.html` by default, `eapcet/index.html` with `--exam eapcet` |
| `tools/encode_film.py` | Makes the web copies of the film and its posters from the full-resolution masters |
| `assets/` | Brand files (with the two app icons `icon-jee.webp`, `icon-eapcet.webp` and EdLoop EAPCET's link-preview card `social-eapcet.png`), EdLoop JEE's screens (`site-redesign/`), EdLoop EAPCET's screens (`eapcet/`), the film (`video/`), the founder photo (`team/`) |

Not used by any page any more, kept until a clean-up commit: `home.css`, `legal.css`, `style.css`, `script.js`,
`tools/make_hero_card.py`.

## The film

Four copies, chosen in `premium.js` by screen: 1080×1920 for phones (720×1280 on 2G/3G), 1920×1080 for laptops and
2560×1440 when the frame is wider than about 2200 real pixels. It is shown full width at its own shape and never cropped.
It plays muted and looping only while visible; Pause and Sound are real buttons. Reduced motion and Data Saver get the
poster until Play is pressed. The masters are not in this repository; only these web copies are.

## Numbers

Every number on the site (questions, papers, years, the year grid) comes from the content database, never from memory.
When an app's question bank grows, update its numbers in three places: its card on the home page, its own page (meta
description, og:description, the numbers list) and, for JEE, the link-preview card (`assets/brand/make_social.html`,
rendered with `assets/brand/render_cards.py`; EdLoop EAPCET's card is its Play feature graphic). Then rerun
`tools/make_years.py` for that app. Say "200 papers" or "77 papers", never "every paper".

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
- The questions on the app pages are real past questions with the exam body's key (NTA's final key for JEE Main, the
  councils' keys for EAPCET); never copy a coaching institute's material.
- No loaders or delays to show the logo; no tracking scripts without an update to the privacy policy first.

© 2026 EDLOOP TECHNOLOGIES. The site's text, design and code belong to EDLOOP TECHNOLOGIES; past exam questions belong to
the bodies that set them. EdLoop is independent of NTA, APSCHE, TGCHE and JNTU.
