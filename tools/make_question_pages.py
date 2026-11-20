#!/usr/bin/env python3
"""Generate the indexable previous-year-question pages for EdLoop JEE (JEE Main 2013-2026 and AIEEE 2002-2012).

    python tools/make_question_pages.py <path to content.sqlite> [--out .] [--lastmod YYYY-MM-DD]

Writes (all deterministic, safe to rerun; the old generated files are removed first):
    q/<question id>.html            one page per question (question text, options, paper/year/shift only)
    q/img/<question id>.webp        the printed question image, for questions that have a figure
    jee/pyq/index.html              hub of all subjects
    jee/pyq/<subject>.html          subject hub (its chapters)
    jee/pyq/<subject>/<chapter>.html  chapter hub (every question of the chapter)
    sitemap.xml + sitemap-*.xml     sitemap index, one file for pages and one per subject for questions
    robots.txt

THE WEB SHOWS: the question text, options, figure, paper/year/shift, and (founder 2026-11-17) the answer as the app
shows it, inside a collapsed "Show answer" (answer, answer_status, accepted_answers_json, answer_source, exam body).
EVERYTHING ELSE STAYS IN THE APP: the columns hint, key_idea, common_mistake, trap_option, formulas_json, keywords_json,
answer_tolerance, the solution table, archetypes and concepts are never selected, so they cannot reach a page. Do not add them.

A question is published when it is exactly what the app shows: question.verification = 'verified', its paper is not
source = 'sample', and its exam belongs to the 'jee' family (JEE_MAIN, AIEEE). Papers with source 'memory_based' get the
"Memory based" badge, as the app's Papers screen does.
"""
import argparse, base64, collections, datetime, html, json, os, re, shutil, sqlite3, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guides  # noqa: E402  chapter guides (guides/jee/<subject>/<chapter>.md), checked by tools/check_guides.py

sys.stdout.reconfigure(encoding='utf-8')

SITE = 'https://edloop.in'
PLAY = 'https://play.google.com/store/apps/details?id=in.edloop.jee'
KATEX = 'https://cdn.jsdelivr.net/npm/katex@0.16.11/dist'
KATEX_SRI = {
    'css': 'sha384-nB0miv6/jRmo5UMMR1wu3Gz6NLsoTkbqJghGIsx//Rlm+ZU03BU6SQNC66uf4l5+',
    'js': 'sha384-7zkQWkzuo3B5mTepMUcHkMB5jZaolc2xDwL6VFqjFALcbeS9Ggm/Yr2r3Dy4lfFg',
    'auto': 'sha384-43gviWU0YVjaDtb/GhzOouOXtZMP/7XUzwPTstBeZFe/+rCMvRwr4yROQP43s0Xk',
}
SUBJECT_SLUG = {'phy': 'physics', 'chem': 'chemistry', 'math': 'mathematics'}
GUIDE_CSS = '  <link rel="stylesheet" href="/qguide.css?v=1">' + chr(10)  # only on chapter pages that have a guide
E = html.escape

# ---------------------------------------------------------------------------------------------------------------
# text helpers
# ---------------------------------------------------------------------------------------------------------------
MATH_RE = re.compile(r'\$\$.+?\$\$|(?<!\\)\$(?:\\.|[^$\\])+\$', re.S)
GREEK = {'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε', 'varepsilon': 'ε', 'theta': 'θ',
         'lambda': 'λ', 'mu': 'μ', 'pi': 'π', 'rho': 'ρ', 'sigma': 'σ', 'tau': 'τ', 'phi': 'φ', 'varphi': 'φ',
         'omega': 'ω', 'Omega': 'Ω', 'Delta': 'Δ', 'Sigma': 'Σ', 'infty': '∞', 'times': '×', 'cdot': '·',
         'to': '→', 'rightarrow': '→', 'leq': '≤', 'geq': '≥', 'neq': '≠', 'pm': '±', 'circ': '°', 'degree': '°',
         'approx': '≈', 'ldots': '…', 'dots': '…', 'cdots': '…', 'int': '∫', 'sum': 'Σ', 'in': '∈'}


def plain(s):
    """LaTeX/Markdown source -> short readable plain text (titles, meta descriptions, hub lists)."""
    s = (s or '').replace('[FIGURE]', '(figure)')
    s = re.sub(r'\*\*|`', '', s)
    s = s.replace('$', '')
    for _ in range(3):
        s = re.sub(r'\\(?:mathrm|text|mathbf|textbf|mathit|operatorname|overrightarrow|vec|hat|bar|overline)\s*\{([^{}]*)\}', r'\1', s)
        s = re.sub(r'\\d?frac\s*\{([^{}]*)\}\s*\{([^{}]*)\}', r'\1/\2', s)
        s = re.sub(r'\\sqrt\s*\{([^{}]*)\}', r'√\1', s)
    s = re.sub(r'\\([A-Za-z]+)', lambda m: GREEK.get(m.group(1), ''), s)
    s = re.sub(r'\\[,;:! ]', ' ', s)
    s = s.replace('\\\\', ' ').replace('\\', '')
    s = re.sub(r'[{}_]', '', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s


def clip(s, n):
    s = s.strip()
    if len(s) <= n:
        return s
    cut = s[:n - 1].rsplit(' ', 1)[0].rstrip(' ,;:-(')
    return (cut or s[:n - 1]) + '…'


def inline_md(s):
    s = re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', s)
    return s


def render_md(src):
    """Markdown subset used by the question bank (paragraphs, **bold**, tables, lists) with $..$ / $$..$$ math left
    intact for KaTeX auto-render. Returns HTML."""
    if src is None:
        return ''
    maths = []

    def stash(m):
        maths.append(m.group(0))
        return '\x00%d\x00' % (len(maths) - 1)
    t = MATH_RE.sub(stash, src.replace('[FIGURE]', '\x01'))
    t = E(t, quote=False)
    t = t.replace('\x01', '<span class="q-fignote">(see the figure above)</span>')
    t = re.sub(r'\\\$', '<span class="nomath">$</span>', t)
    lines = t.split('\n')
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.lstrip().startswith('|'):
            rows = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                rows.append(lines[i].strip())
                i += 1
            cells = [[c.strip() for c in r.strip('|').split('|')] for r in rows]
            sep = [bool(all(re.fullmatch(r':?-{2,}:?', c) for c in r if c)) and any(r) for r in cells]
            head = len(cells) > 1 and sep[1]
            h = '<div class="q-table"><table>'
            for k, r in enumerate(cells):
                if sep[k] and k == 1 and head:
                    continue
                tag = 'th' if head and k == 0 else 'td'
                h += '<tr>' + ''.join('<%s>%s</%s>' % (tag, inline_md(c), tag) for c in r) + '</tr>'
            out.append(h + '</table></div>')
            continue
        if re.match(r'\s*(?:[-*]|\d+\.)\s+\S', ln):
            ordered = bool(re.match(r'\s*\d+\.', ln))
            items = []
            while i < len(lines) and re.match(r'\s*(?:[-*]|\d+\.)\s+\S', lines[i]):
                items.append(re.sub(r'^\s*(?:[-*]|\d+\.)\s+', '', lines[i]))
                i += 1
            tag = 'ol' if ordered else 'ul'
            out.append('<%s>%s</%s>' % (tag, ''.join('<li>%s</li>' % inline_md(x) for x in items), tag))
            continue
        para = []
        while i < len(lines) and lines[i].strip() and not lines[i].lstrip().startswith('|') \
                and not re.match(r'\s*(?:[-*]|\d+\.)\s+\S', lines[i]):
            para.append(inline_md(lines[i]))
            i += 1
        out.append('<p>%s</p>' % '<br>'.join(para))
    res = '\n'.join(out)
    return re.sub(r'\x00(\d+)\x00', lambda m: E(maths[int(m.group(1))], quote=False), res)


def answer_html(r):
    """The answer as the app shows it (VerdictStrip, question_view.dart), collapsed. Nothing but the key and its source."""
    st = r['answer_status'] or 'normal'
    numerical = r['qtype'] == 'numerical'
    body = (r['exam_body'] or 'the exam body').split('/')[0].strip()
    acc = json.loads(r['accepted_answers_json']) if r['accepted_answers_json'] else []

    def opt(v):
        return '(%s)' % v
    if st == 'dropped':
        txt = 'Dropped by %s. Full marks to everyone.' % body
    elif st == 'any':
        txt = 'Any attempt was accepted. Full marks for attempting.'
    elif st == 'multiple' and acc:
        txt = ('Accepted answers: %s.' % ' or '.join(acc)) if numerical else             ('Options %s were accepted. More than one answer was accepted.' % ' or '.join(opt(a) for a in acc))
    elif r['answer'] is not None:
        txt = ('The answer is %s.' % r['answer']) if numerical else 'Option %s is correct.' % opt(r['answer'])
    else:
        return ''
    prov = {'final_key': 'Official %s final key' % body, 'preliminary_key': 'Provisional key, may change',
            'source_key': 'Key from source paper', 'manual': 'Checked by our team'}.get(r['answer_source'])
    return ('<details class="q-answer"><summary>Show answer</summary><div class="q-answer-body"><p><strong>%s</strong></p>%s</div></details>'
            % (E(txt), '<p class="q-prov">%s</p>' % E(prov) if prov else ''))


def slugify(s):
    s = s.lower().replace('&', ' and ')
    s = re.sub(r'[^a-z0-9]+', '-', s).strip('-')
    return s


# ---------------------------------------------------------------------------------------------------------------
# page chrome (header, footer and styles are the site's own; links absolute because pages sit at several depths)
# ---------------------------------------------------------------------------------------------------------------
def load_chrome(root):
    s = open(os.path.join(root, 'delete-account.html'), encoding='utf-8').read()
    hd = s[s.index('<header class="site-header">'):s.index('</header>') + 9]
    ft = s[s.index('<footer'):s.index('</footer>') + 9]

    def absolutize(h):
        def fix(m):
            attr, v = m.group(1), m.group(2)
            if re.match(r'(https?:|mailto:|#|/)', v):
                return m.group(0)
            if v == './':
                v = '/'
            elif v.startswith('./#'):
                v = '/' + v[2:]
            else:
                v = '/' + v
            return '%s="%s"' % (attr, v)
        return re.sub(r'\b(href|src)="([^"]*)"', fix, h)
    ft = re.sub(r'<div class="footer-social".*?</div>', '', ft, flags=re.S)  # social icons: 3.5 KB x 17,720 pages
    return absolutize(hd).replace('href="/#apps">Get the app', 'href="/get/">Get the app'), absolutize(ft)


HEAD_COMMON = '''  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#142444">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="EdLoop">
  <meta property="og:title" content="{ogtitle}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="https://edloop.in/assets/brand/social.png?v=4">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/assets/brand/mark-small.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/assets/brand/icon-512.png">
  <link rel="alternate icon" href="/favicon.ico">
  <link rel="preload" href="/assets/site-redesign/manrope-latin.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/premium.css?v=15">
  <link rel="stylesheet" href="/pages.css?v=1">
  <link rel="stylesheet" href="/qpages.css?v=3">
{extra}  <script src="/config.js?v=4"></script>
  <script src="/site.js?v=6" defer></script>
  <script src="/premium.js?v=13" defer></script>
  <script>document.documentElement.classList.add('js')</script>
'''

KATEX_HEAD = '''  <link rel="stylesheet" href="{k}/katex.min.css" integrity="{css}" crossorigin="anonymous">
  <script defer src="{k}/katex.min.js" integrity="{js}" crossorigin="anonymous"></script>
  <script defer src="{k}/contrib/auto-render.min.js" integrity="{auto}" crossorigin="anonymous"></script>
'''.format(k=KATEX, css=KATEX_SRI['css'], js=KATEX_SRI['js'], auto=KATEX_SRI['auto'])

def page(chrome, title, desc, canon, body, extra='', ogtitle=None, body_class='inner qpage', tail=''):
    head = HEAD_COMMON.format(title=E(title), desc=E(desc), canon=canon, ogtitle=E(ogtitle or title), extra=extra)
    return ('<!doctype html>\n<html lang="en">\n<head>\n%s</head>\n<body class="%s">\n'
            '  <a class="skip-link" href="#main">Skip to content</a>\n  %s\n%s\n  %s\n%s</body>\n</html>\n'
            % (head, body_class, chrome[0], body, chrome[1], tail))


def crumbs_json(items):
    return ('  <script type="application/ld+json">%s</script>\n' % json.dumps({
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]
    }, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))


def crumbs_html(items):
    parts = []
    for n, u in items[:-1]:
        parts.append('<a href="%s">%s</a>' % (u.replace(SITE, ''), E(n)))
    parts.append('<span aria-current="page">%s</span>' % E(items[-1][0]))
    return '<nav class="q-crumbs" aria-label="Breadcrumb">%s</nav>' % ' <span aria-hidden="true">/</span> '.join(parts)


def play_href(qid):
    return '%s&amp;referrer=utm_source%%3Dweb%%26utm_content%%3Dq_page%%26question%%3D%s' % (PLAY.replace('&', '&amp;'), qid)


# ---------------------------------------------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('db')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    ap.add_argument('--lastmod', default=None)
    ap.add_argument('--figures', choices=['nta-only', 'all'], default='all',
                    help="all (default since 2026-11-18): every figure question gets a page; the content build cuts MathonGo's "
                         "footer advert out of memory-based crops (IIT-APP content/figures/advert_cuts.tsv, Prod load 2026-11-17). "
                         "nta-only: only NTA's own papers' figure questions (for a content file built before that cut).")
    a = ap.parse_args()
    root = os.path.abspath(a.out)
    db = sqlite3.connect('file:%s?mode=ro' % os.path.abspath(a.db).replace('\\', '/'), uri=True)
    db.row_factory = sqlite3.Row
    meta = dict(db.execute('select key, value from content_meta').fetchall())
    lastmod = a.lastmod or meta.get('built_at', '')[:10] or datetime.date.today().isoformat()
    chrome = load_chrome(root)

    # Only these columns are read. Never hint, key_idea, common_mistake, trap_option, formulas_json, keywords_json,
    # answer_tolerance, solution rows, archetypes or concepts.
    rows = db.execute('''
        SELECT q.answer, q.answer_status, q.accepted_answers_json, q.answer_source, e.body AS exam_body,
               q.id, q.qno, q.section, q.subject_id, q.chapter_id, q.qtype, q.body, q.options_json, q.title,
               p.id AS paper_id, p.exam, p.year, p.exam_date, p.shift, p.source, p.official_name,
               c.name AS chapter_name, c.sort_order AS chapter_sort, s.name AS subject_name, s.sort_order AS subject_sort
        FROM question q
        JOIN paper p ON p.id = q.paper_id
        JOIN exam e ON e.id = p.exam
        JOIN chapter c ON c.id = q.chapter_id
        JOIN subject s ON s.id = q.subject_id
        WHERE e.family = 'jee' AND p.source <> 'sample' AND q.verification = 'verified'
        ORDER BY p.year, COALESCE(p.exam_date, ''), p.id, q.subject_id, q.qno, q.id''').fetchall()
    total_in_family = db.execute('''SELECT COUNT(*) FROM question q JOIN paper p ON p.id=q.paper_id JOIN exam e ON e.id=p.exam
                                    WHERE e.family='jee' AND p.source<>'sample' ''').fetchone()[0]
    print('verified JEE-family questions:', len(rows), '(non-sample, any verification: %d)' % total_in_family)

    assets = {r['question_id']: r for r in db.execute(
        "SELECT a.question_id, a.id, a.width, a.height, d.data_base64 FROM asset a JOIN asset_data d ON d.asset_id = a.id "
        "WHERE a.kind = 'question_image'")}

    skipped_fig = collections.Counter()
    if a.figures == 'nta-only':
        keep = []
        for r in rows:
            if r['id'] in assets and r['source'] == 'memory_based':
                skipped_fig[r['year']] += 1
            else:
                keep.append(r)
        rows = keep
        print('figure questions left out (memory-based paper, image carries a coaching advert):', sum(skipped_fig.values()))
        print('  by year:', dict(sorted(skipped_fig.items())))
    print('questions to publish:', len(rows))

    # ---- clean previously generated files
    for d in ('q', 'jee/pyq'):
        shutil.rmtree(os.path.join(root, d), ignore_errors=True)
    for f in os.listdir(root):
        if f == 'robots.txt' or re.fullmatch(r'sitemap(-[a-z-]+)?\.xml', f):
            os.remove(os.path.join(root, f))
    os.makedirs(os.path.join(root, 'q', 'img'), exist_ok=True)

    def paper_name(r):
        n = r['official_name'] or ('%s %d' % ('AIEEE' if r['exam'] == 'AIEEE' else 'JEE Main', r['year']))
        if r['exam'] == 'AIEEE':
            n = n.replace('JEE Main', 'AIEEE')
        return n

    def paper_short(r):
        return paper_name(r).replace('(', '').replace(')', '')

    # ---- chapter bookkeeping (a slug is unique inside its subject)
    chapters = collections.OrderedDict()
    seen_slug = set()
    for r in sorted(rows, key=lambda r: (r['subject_sort'], r['chapter_sort'], r['chapter_id'])):
        if r['chapter_id'] not in chapters:
            slug = slugify(r['chapter_name'])
            key = (r['subject_id'], slug)
            if key in seen_slug:
                slug = slugify(r['chapter_id'])
            seen_slug.add((r['subject_id'], slug))
            chapters[r['chapter_id']] = {'id': r['chapter_id'], 'name': r['chapter_name'], 'slug': slug,
                                         'subject': r['subject_id'], 'subject_name': r['subject_name'], 'qs': []}
    by_ch = chapters
    for r in rows:  # chronological (the SELECT order) within the chapter
        by_ch[r['chapter_id']]['qs'].append(r)

    def ch_url(ch):
        return '/jee/pyq/%s/%s' % (SUBJECT_SLUG[ch['subject']], ch['slug'])

    # ---- question pages
    titles = collections.Counter()
    sizes = {'html': 0, 'img': 0}
    n_img = 0
    urls = collections.defaultdict(list)
    for ch in chapters.values():
        qs = ch['qs']
        for i, r in enumerate(qs):
            qid = r['id']
            memory = r['source'] == 'memory_based'
            pname = paper_name(r)
            subj, cname = r['subject_name'], r['chapter_name']
            label = plain(r['title']) or plain(r['body'])
            # <title> <= 65 characters and unique: "<label> - <paper> | EdLoop"
            suffix = ' - %s | EdLoop' % paper_short(r)
            if 65 - len(suffix) < 24:  # long paper name: drop the brand rather than the label
                suffix = ' - %s' % paper_short(r)
            t = clip(label, 65 - len(suffix)) + suffix
            titles[t] += 1
            if titles[t] > 1:  # same label twice in a paper: tell them apart by the number in the section
                extra = ' (%s Q%s)' % (subj[:4], r['qno'])
                t = clip(label, 65 - len(suffix) - len(extra)) + extra + suffix
                titles[t] += 1
            h1 = '%s %s: %s' % (pname, subj, cname)
            qplain = plain(r['body'])
            desc = clip(qplain, 150)
            if len(desc) < 70:
                desc = '%s %s PYQ. %s' % (desc, paper_short(r), subj + ': ' + cname + '.')
            opts = json.loads(r['options_json']) if r['options_json'] else []
            figdesc = []  # figure descriptions: screen readers and the image alt only, never visible

            def figonly(text, label):
                """'[FIGURE] <description>': show just 'see figure'; keep the description visually hidden."""
                t = (text or '').strip()
                if not t.startswith('[FIGURE]'):
                    return None
                rest = t[len('[FIGURE]'):].strip()
                if rest:
                    figdesc.append('%s: %s' % (label, plain(rest)))
                return '<p><span class="q-fignote">see figure</span>%s</p>' % (
                    '<span class="sr-only"> %s</span>' % render_md(rest).replace('<p>', '').replace('</p>', '') if rest else '')
            stem = figonly(r['body'], 'Question')
            body_html = stem if stem else render_md(r['body'])
            if opts:
                lis = ''.join('<li><span class="q-optn">(%d)</span><div class="q-opt">%s</div></li>' % (
                    k + 1, figonly(o, 'Option %d' % (k + 1)) or render_md(o)) for k, o in enumerate(opts))
                opts_html = '<ol class="q-opts" aria-label="Options">%s</ol>' % lis
            else:
                opts_html = '<p class="q-num">Numerical-value question: the answer is a number.</p>'
            ans_html = answer_html(r)
            fig_html = ''
            if qid in assets:
                ar = assets[qid]
                data = base64.b64decode(ar['data_base64'])
                with open(os.path.join(root, 'q', 'img', qid + '.webp'), 'wb') as fh:
                    fh.write(data)
                sizes['img'] += len(data)
                n_img += 1
                fig_html = ('<figure class="q-figure"><img src="/q/img/%s.webp" width="%s" height="%s" loading="lazy" decoding="async" '
                            'alt="%s"><figcaption>The question as printed in the paper.</figcaption></figure>'
                            % (qid, ar['width'] or '', ar['height'] or '',
                               E(clip('The question and its figure as printed in %s. %s' % (paper_short(r), ' '.join(figdesc)), 700))))
            qtype = 'Numerical value' if r['qtype'] == 'numerical' else 'Multiple choice, one correct option'
            badge = ('<span class="q-badge" title="Reconstructed by coaching institutes from memory; wording may differ slightly from the exam paper">Memory based</span>'
                     if memory else '<span class="q-badge q-badge-official">NTA paper</span>')
            prev_l = next_l = ''
            if i > 0:
                p = qs[i - 1]
                prev_l = '<a class="q-nav-prev" href="/q/%s"><small>&larr; Previous in %s</small><span>%s &middot; %s</span></a>' % (
                    p['id'], E(cname), E(paper_short(p)), E(clip(plain(p['title']) or plain(p['body']), 70)))
            if i < len(qs) - 1:
                nx = qs[i + 1]
                next_l = '<a class="q-nav-next" href="/q/%s"><small>Next in %s &rarr;</small><span>%s &middot; %s</span></a>' % (
                    nx['id'], E(cname), E(paper_short(nx)), E(clip(plain(nx['title']) or plain(nx['body']), 70)))
            cu = ch_url(ch)
            crumbs = [('EdLoop', SITE + '/'), ('JEE Main PYQs', SITE + '/jee/pyq/'),
                      (subj, SITE + '/jee/pyq/' + SUBJECT_SLUG[r['subject_id']]), (cname, SITE + cu), (paper_short(r), SITE + '/q/' + qid)]
            main_html = '''  <main id="main" class="qpage-main">
    <header class="page-band"><div class="wrap">
      %s
      <h1>%s</h1>
      <p class="q-meta">%s <span>%s</span> <span>%s</span></p>
    </div></header>
    <div class="wrap q-wrap">
      <article class="q-card" id="qmath" data-qid="%s" aria-label="Question">
        <div class="q-body">%s</div>
        %s
        %s
        %s
      </article>
      <section class="q-cta" aria-labelledby="cta-h">
        <h2 id="cta-h">See the step-by-step solution in EdLoop</h2>
        <p>The worked solution is in the EdLoop app, free on Android, with every other %s question from 2002 to 2026.</p>
        <div class="q-actions">
          <a class="btn btn-solid" id="q-get" href="%s" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l13 8-13 8z"/></svg>Get EdLoop on Google Play</a>
          <a class="btn btn-line" id="q-open" href="#" hidden>Open in EdLoop</a>
        </div>
      </section>
      <p class="q-about">%s %s question from %s (%s). %s</p>
      <nav class="q-nav" aria-label="More %s questions">%s%s</nav>
      <p class="q-back"><a href="%s">All JEE Main %s PYQs (%d questions)</a></p>
    </div>
  </main>
''' % (crumbs_html(crumbs), E(h1), E(qtype), badge, E(cname), qid, body_html, fig_html, opts_html, ans_html, E(cname), play_href(qid),
       E(subj), E(cname), E(pname), E(r['exam'] == 'AIEEE' and 'AIEEE, now called JEE Main' or 'JEE Main exam'),
       'Memory-based papers are reconstructed from candidates\' memory by coaching institutes.' if memory else 'This is the paper as NTA held it.',
       E(cname), prev_l, next_l, cu, E(cname), len(qs))
            html_out = page(chrome, t, desc, '%s/q/%s' % (SITE, qid), main_html,
                            extra=KATEX_HEAD + crumbs_json(crumbs), ogtitle=h1, tail='  <script src="/qpage.js?v=1" defer></script>\n')
            with open(os.path.join(root, 'q', qid + '.html'), 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(html_out)
            sizes['html'] += len(html_out.encode('utf-8'))
            urls[r['subject_id']].append(qid)

    # ---- hubs
    os.makedirs(os.path.join(root, 'jee', 'pyq'), exist_ok=True)

    def write(path, content):
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(content)

    def nfmt(n):
        return '{:,}'.format(n)

    hub_urls = []
    subj_ch = collections.OrderedDict()
    for ch in chapters.values():
        subj_ch.setdefault(ch['subject'], []).append(ch)
    for sid, chs in subj_ch.items():
        chs.sort(key=lambda c: (min(q['chapter_sort'] for q in c['qs']), c['name']))

    def span(qs):
        ys = [q['year'] for q in qs]
        return min(ys), max(ys)

    n_guides = 0
    all_papers = len({q['paper_id'] for q in rows})
    y0, y1 = span(rows)
    for ch in chapters.values():
        qs = ch['qs']
        papers = len({q['paper_id'] for q in qs})
        ya, yb = span(qs)
        sname = ch['subject_name']
        cu = ch_url(ch)
        h1 = 'JEE Main %s PYQs (%d\u2013%d), chapter-wise' % (ch['name'], ya, yb)
        title = clip('JEE Main %s PYQs %d\u2013%d (%s) | EdLoop' % (ch['name'], ya, yb, sname), 65)
        if len(title) > 65:
            title = clip('JEE Main %s PYQs (%s) | EdLoop' % (ch['name'], sname), 65)
        desc = '%s previous-year JEE Main and AIEEE questions on %s (%s) from %d papers, %d\u2013%d. Read each question with its options, answer and paper; get the step-by-step solution in EdLoop.' % (
            nfmt(len(qs)), ch['name'], sname, papers, ya, yb)
        groups = collections.OrderedDict()
        for q in reversed(qs):
            groups.setdefault(q['paper_id'], []).append(q)
        lst = ''
        cur_year = None
        for pid, gq in groups.items():
            yr = gq[0]['year']
            if yr != cur_year:
                if cur_year is not None:
                    lst += '</div>'
                lst += '<div class="q-year"><h3>%d</h3>' % yr
                cur_year = yr
            lst += '<h4>%s%s</h4><ul class="q-list">' % (E(paper_short(gq[0])), ' <span class="q-badge q-badge-sm">Memory based</span>' if gq[0]['source'] == 'memory_based' else '')
            for q in sorted(gq, key=lambda q: (q['qno'] or 0, q['id'])):
                lst += '<li><a href="/q/%s">%s</a></li>' % (q['id'], E(clip(plain(q['title']) or plain(q['body']), 110)))
            lst += '</ul>'
        lst += '</div>'
        crumbs = [('EdLoop', SITE + '/'), ('JEE Main PYQs', SITE + '/jee/pyq/'), (sname, SITE + '/jee/pyq/' + SUBJECT_SLUG[ch['subject']]), (ch['name'], SITE + cu)]
        n_mem = sum(1 for q in qs if q['source'] == 'memory_based')
        guide_html, faq = '', []
        gp = guides.guide_path(root, SUBJECT_SLUG[ch['subject']], ch['slug'])
        if os.path.exists(gp):
            with open(gp, encoding='utf-8') as fh:
                guide_html, faq = guides.render(fh.read(), ch['name'])
            n_guides += 1
        body = '''  <main id="main" class="qpage-main">
    <header class="page-band"><div class="wrap">
      %s
      <h1>%s</h1>
      <p class="tagline">%s questions from %d papers, %d to %d. Open any question to read it in full with its options.</p>
    </div></header>
    <div class="wrap q-wrap q-wide">
      <p class="q-intro">%s is part of the JEE Main %s syllabus. This page lists every %s question we have on it, newest paper first, from JEE Main (2013 onwards) and its earlier name AIEEE (2002 to 2012). %s</p>
      <section class="q-cta q-cta-slim"><p><strong>Step-by-step solutions are in EdLoop.</strong> Free on Android, no ads.</p>
        <div class="q-actions"><a class="btn btn-solid" href="%s&amp;referrer=utm_source%%3Dweb%%26utm_content%%3Dpyq_hub" rel="noopener">Get EdLoop on Google Play</a></div></section>
      %s%s
    </div>
  </main>
''' % (crumbs_html(crumbs), E(h1), nfmt(len(qs)), papers, ya, yb, E(ch['name']), E(sname), E(ch['name']),
       ('%d of these questions come from memory-based papers (reconstructed by coaching institutes); papers marked NTA are the exam as held.' % n_mem) if n_mem else '',
       PLAY.replace('&', '&amp;'), (guide_html + chr(10) + '      ') if guide_html else '', ('<h2 class="q-list-head">Every %s question, newest first</h2>' % E(ch['name']) if guide_html else '') + lst)
        write('jee/pyq/%s/%s.html' % (SUBJECT_SLUG[ch['subject']], ch['slug']),
              page(chrome, title, desc, SITE + cu, body, extra=crumbs_json(crumbs) + guides.faq_jsonld(faq) +
                   (GUIDE_CSS if guide_html else '')))
        hub_urls.append(SITE + cu)

    for sid, chs in subj_ch.items():
        sname = chs[0]['subject_name']
        qs_all = [q for c in chs for q in c['qs']]
        ya, yb = span(qs_all)
        su = '/jee/pyq/' + SUBJECT_SLUG[sid]
        cards = ''.join('<li><a href="%s"><strong>%s</strong><span>%s questions &middot; %d\u2013%d</span></a></li>' % (
            ch_url(c), E(c['name']), nfmt(len(c['qs'])), span(c['qs'])[0], span(c['qs'])[1]) for c in chs)
        crumbs = [('EdLoop', SITE + '/'), ('JEE Main PYQs', SITE + '/jee/pyq/'), (sname, SITE + su)]
        title = 'JEE Main %s PYQs, chapter-wise (%d\u2013%d) | EdLoop' % (sname, ya, yb)
        desc = '%s JEE Main and AIEEE %s previous-year questions from %d\u2013%d in %d chapters. Pick a chapter, read the questions, check answers and solutions in EdLoop.' % (nfmt(len(qs_all)), sname, ya, yb, len(chs))
        body = '''  <main id="main" class="qpage-main">
    <header class="page-band"><div class="wrap">
      %s
      <h1>JEE Main %s PYQs, chapter-wise (%d\u2013%d)</h1>
      <p class="tagline">%s questions in %d chapters.</p>
    </div></header>
    <div class="wrap q-wrap q-wide"><ul class="q-cards">%s</ul></div>
  </main>
''' % (crumbs_html(crumbs), E(sname), ya, yb, nfmt(len(qs_all)), len(chs), cards)
        write('jee/pyq/%s.html' % SUBJECT_SLUG[sid], page(chrome, title, desc, SITE + su, body, extra=crumbs_json(crumbs)))
        hub_urls.append(SITE + su)

    blocks = ''
    for sid, chs in subj_ch.items():
        n = sum(len(c['qs']) for c in chs)
        blocks += '<section class="q-subject"><h2><a href="/jee/pyq/%s">%s</a> <small>%s questions</small></h2><ul class="q-cards">%s</ul></section>' % (
            SUBJECT_SLUG[sid], E(chs[0]['subject_name']), nfmt(n),
            ''.join('<li><a href="%s"><strong>%s</strong><span>%s</span></a></li>' % (ch_url(c), E(c['name']), nfmt(len(c['qs']))) for c in chs))
    crumbs = [('EdLoop', SITE + '/'), ('JEE Main PYQs', SITE + '/jee/pyq/')]
    title = 'JEE Main Previous Year Questions (PYQ) by Chapter | EdLoop'
    desc = '%s JEE Main and AIEEE previous-year questions from %d papers (%d\u2013%d), sorted by subject and chapter. Read them free with answers; step-by-step solutions are in the EdLoop app.' % (nfmt(len(rows)), all_papers, y0, y1)
    body = '''  <main id="main" class="qpage-main">
    <header class="page-band"><div class="wrap">
      %s
      <h1>JEE Main previous year questions, chapter-wise</h1>
      <p class="tagline">%s questions from %d papers, %d\u2013%d: JEE Main from 2013 and AIEEE (its earlier name) from 2002. Most papers before 2026 are memory based, reconstructed by coaching institutes; 2026 papers are NTA&rsquo;s own.</p>
    </div></header>
    <div class="wrap q-wrap q-wide">%s</div>
  </main>
''' % (crumbs_html(crumbs), nfmt(len(rows)), all_papers, y0, y1, blocks)
    write('jee/pyq/index.html', page(chrome, title, desc, SITE + '/jee/pyq/', body, extra=crumbs_json(crumbs)))
    hub_urls.insert(0, SITE + '/jee/pyq/')

    # ---- sitemaps
    def urlset(items):
        s = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for u in items:
            s += '<url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (u, lastmod)
        return s + '</urlset>\n'
    static = [SITE + '/', SITE + '/jee/', SITE + '/eapcet/', SITE + '/about.html'] + hub_urls
    write('sitemap-pages.xml', urlset(static))
    index = [('sitemap-pages.xml', len(static))]
    for sid in ('phy', 'chem', 'math'):
        if sid in urls:
            nm = 'sitemap-q-%s.xml' % SUBJECT_SLUG[sid]
            items = ['%s/q/%s' % (SITE, q) for q in urls[sid]]
            assert len(items) <= 50000
            write(nm, urlset(items))
            index.append((nm, len(items)))
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          ''.join('<sitemap><loc>%s/%s</loc><lastmod>%s</lastmod></sitemap>\n' % (SITE, n, lastmod) for n, _ in index) + '</sitemapindex>\n')
    write('robots.txt', 'User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE)

    dup = [t for t, c in titles.items() if c > 1]
    print('question pages: %d  (with image: %d)' % (len(rows), n_img))
    print('chapters: %d  subjects: %d  chapter guides: %d' % (len(chapters), len(subj_ch), n_guides))
    print('sitemap URLs: %d  (questions %d, pages %d)' % (len(rows) + len(static), len(rows), len(static)))
    print('html bytes: %s  image bytes: %s' % (nfmt(sizes['html']), nfmt(sizes['img'])))
    print('duplicate titles:', len(dup))


if __name__ == '__main__':
    main()
