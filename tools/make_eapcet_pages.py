#!/usr/bin/env python3
"""Generate the indexable previous-year-question pages for EdLoop EAPCET (AP & TS EAPCET 2010-2026).

    python tools/make_eapcet_pages.py <path to content.sqlite> [--out .] [--lastmod YYYY-MM-DD]

Writes:
    eapcet/q/<question id>.html              one page per question
    eapcet/q/img/<question id>.webp          printed question images for figure questions
    eapcet/pyq/index.html                    hub of all subjects
    eapcet/pyq/<subject>.html                subject hub (its chapters)
    eapcet/pyq/<subject>/<chapter>.html      chapter hub (every question of the chapter)
    sitemap-eapcet-q-<subject>.xml           sitemaps per subject
    sitemap-pages.xml and sitemap.xml        updated with EAPCET pages
"""
import argparse, base64, collections, datetime, html, json, os, re, shutil, sqlite3, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_question_pages as base

sys.stdout.reconfigure(encoding='utf-8')

SITE = 'https://edloop.in'
PLAY = 'https://play.google.com/store/apps/details?id=in.edloop.eapcet'
SUBJECT_SLUG = {'math': 'mathematics', 'phy': 'physics', 'chem': 'chemistry'}
SUBJECT_ORDER = ['math', 'phy', 'chem']
E = html.escape

# EAPCET HEAD: social image is social-eapcet.png
HEAD_EAPCET = '''  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#081028">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{canon}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="EdLoop">
  <meta property="og:title" content="{ogtitle}">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="https://edloop.in/assets/brand/social-eapcet.png?v=1">
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


def page(chrome, title, desc, canon, body, extra='', ogtitle=None, body_class='inner qpage', tail=''):
    head = HEAD_EAPCET.format(title=E(title), desc=E(desc), canon=canon, ogtitle=E(ogtitle or title), extra=extra)
    return ('<!doctype html>\n<html lang="en">\n<head>\n%s</head>\n<body class="%s">\n'
            '  <a class="skip-link" href="#main">Skip to content</a>\n  %s\n%s\n  %s\n%s</body>\n</html>\n'
            % (head, body_class, chrome[0], body, chrome[1], tail))


def load_chrome(root):
    s = open(os.path.join(root, 'eapcet', 'index.html'), encoding='utf-8').read()
    hd = s[s.index('<header class="site-header">'):s.index('</header>') + 9]
    ft = s[s.index('<footer'):s.index('</footer>') + 9]

    def absolutize(h):
        def fix(m):
            attr, v = m.group(1), m.group(2)
            if re.match(r'(https?:|mailto:|#|/)', v):
                return m.group(0)
            if v == './' or v == '../':
                v = '/'
            elif v.startswith('../#'):
                v = '/' + v[3:]
            elif v.startswith('./#'):
                v = '/' + v[2:]
            elif v.startswith('../'):
                v = '/' + v[3:]
            elif v.startswith('./'):
                v = '/' + v[2:]
            else:
                v = '/' + v
            return '%s="%s"' % (attr, v)
        return re.sub(r'\b(href|src)="([^"]*)"', fix, h)

    ft = re.sub(r'<div class="footer-social".*?</div>', '', ft, flags=re.S)
    return absolutize(hd), absolutize(ft)


def paper_name(r):
    raw = r['official_name'] or ''
    exam_prefix = 'AP EAPCET' if r['exam'] == 'AP_EAPCET' else 'TS EAPCET'
    if re.match(r'^(?:AP|TS|TG)\s+(?:EAPCET|EAMCET)', raw):
        return raw
    m = re.match(r'^engineering(?:\w+)?\s*(.*)$', raw, re.I)
    if m:
        rest = m.group(1).strip()
        if str(r['year']) not in rest:
            return f"{exam_prefix} {r['year']} ({rest})"
        return f"{exam_prefix} {r['year']} ({re.sub(r'\\b' + str(r['year']) + r'\\b', '', rest).strip()})"
    return f"{exam_prefix} {raw}"


def paper_short(r):
    return paper_name(r).replace('(', '').replace(')', '')


def answer_html(r):
    st = r['answer_status'] or 'normal'
    numerical = r['qtype'] == 'numerical'
    body = (r['exam_body'] or 'the council').split('/')[0].strip()
    acc = json.loads(r['accepted_answers_json']) if r['accepted_answers_json'] else []

    def opt(v):
        return '(%s)' % v

    if st == 'dropped':
        txt = 'Dropped by %s. Full marks to everyone.' % body
    elif st == 'any':
        txt = 'Any attempt was accepted. Full marks for attempting.'
    elif st == 'multiple' and acc:
        txt = ('Accepted answers: %s.' % ' or '.join(acc)) if numerical else ('Options %s were accepted. More than one answer was accepted.' % ' or '.join(opt(a) for a in acc))
    elif r['answer'] is not None:
        txt = ('The answer is %s.' % r['answer']) if numerical else 'Option %s is correct.' % opt(r['answer'])
    else:
        return ''

    prov = {
        'final_key': 'Official %s final key' % body,
        'preliminary_key': "The council's preliminary key",
        'source_key': 'Key from source paper',
        'manual': 'Checked by our team',
    }.get(r['answer_source'])
    return ('<details class="q-answer"><summary>Show answer</summary><div class="q-answer-body"><p><strong>%s</strong></p>%s</div></details>'
            % (E(txt), '<p class="q-prov">%s</p>' % E(prov) if prov else ''))


def play_href(qid):
    return '%s&amp;referrer=utm_source%%3Dedloop.in%%26utm_campaign%%3Deapcet_q%%26question%%3D%s' % (PLAY.replace('&', '&amp;'), qid)


def ch_url(ch):
    return '/eapcet/pyq/%s/%s' % (SUBJECT_SLUG[ch['subject']], ch['slug'])


def run(db_path, out=None, lastmod=None):
    root = os.path.abspath(out or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    db = sqlite3.connect('file:%s?mode=ro' % os.path.abspath(db_path).replace('\\', '/'), uri=True)
    db.row_factory = sqlite3.Row
    meta = dict(db.execute('select key, value from content_meta').fetchall())
    lastmod = lastmod or meta.get('built_at', '')[:10] or datetime.date.today().isoformat()
    chrome = load_chrome(root)

    # Only read permitted columns
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
        WHERE e.family = 'eapcet' AND p.source <> 'sample' AND q.verification = 'verified'
        ORDER BY p.year, COALESCE(p.exam_date, ''), p.id, q.subject_id, q.qno, q.id''').fetchall()
    total_in_family = db.execute('''SELECT COUNT(*) FROM question q JOIN paper p ON p.id=q.paper_id JOIN exam e ON e.id=p.exam
                                    WHERE e.family='eapcet' AND p.source<>'sample' ''').fetchone()[0]
    print('verified EAPCET-family questions:', len(rows), '(non-sample, any verification: %d)' % total_in_family)

    assets = {r['question_id']: r for r in db.execute(
        "SELECT a.question_id, a.id, a.width, a.height, d.data_base64 FROM asset a JOIN asset_data d ON d.asset_id = a.id "
        "WHERE a.kind = 'question_image'")}

    # Clean only previously generated EAPCET files; NEVER touch q/ or jee/
    for d in ('eapcet/q', 'eapcet/pyq'):
        shutil.rmtree(os.path.join(root, d), ignore_errors=True)
    os.makedirs(os.path.join(root, 'eapcet', 'q', 'img'), exist_ok=True)
    os.makedirs(os.path.join(root, 'eapcet', 'pyq'), exist_ok=True)

    # Chapter bookkeeping
    chapters = collections.OrderedDict()
    seen_slug = set()
    for r in sorted(rows, key=lambda r: (r['subject_sort'], r['chapter_sort'], r['chapter_id'])):
        if r['chapter_id'] not in chapters:
            slug = base.slugify(r['chapter_name'])
            key = (r['subject_id'], slug)
            if key in seen_slug:
                slug = base.slugify(r['chapter_id'])
            seen_slug.add((r['subject_id'], slug))
            chapters[r['chapter_id']] = {'id': r['chapter_id'], 'name': r['chapter_name'], 'slug': slug,
                                         'subject': r['subject_id'], 'subject_name': r['subject_name'], 'qs': []}
    by_ch = chapters
    for r in rows:
        by_ch[r['chapter_id']]['qs'].append(r)

    titles = collections.Counter()
    sizes = {'html': 0, 'img': 0}
    n_img = 0
    urls = collections.defaultdict(list)

    for ch in chapters.values():
        qs = ch['qs']
        for i, r in enumerate(qs):
            qid = r['id']
            pname = paper_name(r)
            subj, cname = r['subject_name'], r['chapter_name']
            body_council = (r['exam_body'] or 'the council').split('/')[0].strip()
            label = base.plain(r['title']) or base.plain(r['body'])
            suffix = ' - %s | EdLoop' % paper_short(r)
            if 65 - len(suffix) < 24:
                suffix = ' - %s' % paper_short(r)
            t = base.clip(label, 65 - len(suffix)) + suffix
            titles[t] += 1
            if titles[t] > 1:
                extra = ' (%s Q%s)' % (subj[:4], r['qno'])
                t = base.clip(label, 65 - len(suffix) - len(extra)) + extra + suffix
                titles[t] += 1

            h1 = '%s %s: %s' % (pname, subj, cname)
            qplain = base.plain(r['body'])
            desc = base.clip(qplain, 150)
            if len(desc) < 70:
                desc = '%s %s PYQ. %s' % (desc, paper_short(r), subj + ': ' + cname + '.')

            opts = json.loads(r['options_json']) if r['options_json'] else []
            figdesc = []

            def figonly(text, label_prefix):
                txt = (text or '').strip()
                if not txt.startswith('[FIGURE]'):
                    return None
                rest = txt[len('[FIGURE]'):].strip()
                if rest:
                    figdesc.append('%s: %s' % (label_prefix, base.plain(rest)))
                return '<p><span class="q-fignote">see figure</span>%s</p>' % (
                    '<span class="sr-only"> %s</span>' % base.render_md(rest).replace('<p>', '').replace('</p>', '') if rest else '')

            stem = figonly(r['body'], 'Question')
            body_html = stem if stem else base.render_md(r['body'])
            if opts:
                lis = ''.join('<li><span class="q-optn">(%d)</span><div class="q-opt">%s</div></li>' % (
                    k + 1, figonly(o, 'Option %d' % (k + 1)) or base.render_md(o)) for k, o in enumerate(opts))
                opts_html = '<ol class="q-opts" aria-label="Options">%s</ol>' % lis
            else:
                opts_html = '<p class="q-num">Numerical-value question: the answer is a number.</p>'

            ans_html = answer_html(r)
            fig_html = ''
            if qid in assets:
                ar = assets[qid]
                data = base64.b64decode(ar['data_base64'])
                img_path = os.path.join(root, 'eapcet', 'q', 'img', qid + '.webp')
                with open(img_path, 'wb') as fh:
                    fh.write(data)
                sizes['img'] += len(data)
                n_img += 1
                fig_html = ('<figure class="q-figure"><img src="/eapcet/q/img/%s.webp" width="%s" height="%s" loading="lazy" decoding="async" '
                            'alt="%s"><figcaption>The question as printed in the paper.</figcaption></figure>'
                            % (qid, ar['width'] or '', ar['height'] or '',
                               E(base.clip('The question and its figure as printed in %s. %s' % (paper_short(r), ' '.join(figdesc)), 700))))

            qtype = 'Numerical value' if r['qtype'] == 'numerical' else 'Multiple choice, one correct option'
            exam_label = 'AP EAPCET' if r['exam'] == 'AP_EAPCET' else 'TS EAPCET'
            badge = '<span class="q-badge q-badge-official">%s paper</span>' % exam_label

            prev_l = next_l = ''
            if i > 0:
                p = qs[i - 1]
                prev_l = '<a class="q-nav-prev" href="/eapcet/q/%s"><small>&larr; Previous in %s</small><span>%s &middot; %s</span></a>' % (
                    p['id'], E(cname), E(paper_short(p)), E(base.clip(base.plain(p['title']) or base.plain(p['body']), 70)))
            if i < len(qs) - 1:
                nx = qs[i + 1]
                next_l = '<a class="q-nav-next" href="/eapcet/q/%s"><small>Next in %s &rarr;</small><span>%s &middot; %s</span></a>' % (
                    nx['id'], E(cname), E(paper_short(nx)), E(base.clip(base.plain(nx['title']) or base.plain(nx['body']), 70)))

            cu = ch_url(ch)
            crumbs = [('EdLoop', SITE + '/'), ('EAPCET PYQs', SITE + '/eapcet/pyq/'),
                      (subj, SITE + '/eapcet/pyq/' + SUBJECT_SLUG[r['subject_id']]), (cname, SITE + cu), (paper_short(r), SITE + '/eapcet/q/' + qid)]

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
        <p>The worked solution is in the EdLoop app, free on Android, with every other %s question from 2010 to 2026.</p>
        <div class="q-actions">
          <a class="btn btn-solid" id="q-get" href="%s" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4l13 8-13 8z"/></svg>Get EdLoop on Google Play</a>
          <a class="btn btn-line" id="q-open" href="#" hidden>Open in EdLoop</a>
        </div>
      </section>
      <p class="q-about">%s %s question from %s (%s). %s</p>
      <nav class="q-nav" aria-label="More %s questions">%s%s</nav>
      <p class="q-back"><a href="%s">All EAPCET %s PYQs (%d questions)</a></p>
    </div>
  </main>
''' % (base.crumbs_html(crumbs), E(h1), E(qtype), badge, E(cname), qid, body_html, fig_html, opts_html, ans_html, E(cname), play_href(qid),
       E(subj), E(cname), E(pname), E(exam_label + ' exam'), 'This is the paper as %s held it.' % body_council,
       E(cname), prev_l, next_l, cu, E(cname), len(qs))

            html_out = page(chrome, t, desc, '%s/eapcet/q/%s' % (SITE, qid), main_html,
                            extra=base.KATEX_HEAD + base.crumbs_json(crumbs), ogtitle=h1, tail='  <script src="/eapcet/qpage.js?v=1" defer></script>\n')
            with open(os.path.join(root, 'eapcet', 'q', qid + '.html'), 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(html_out)
            sizes['html'] += len(html_out.encode('utf-8'))
            urls[r['subject_id']].append(qid)

    # ---- Hubs
    def write(path, content):
        full = os.path.join(root, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(content)

    def nfmt(n):
        return '{:,}'.format(n)

    def span(qs):
        ys = [q['year'] for q in qs]
        return min(ys), max(ys)

    hub_urls = []
    subj_ch = collections.OrderedDict()
    for sid in SUBJECT_ORDER:
        subj_ch[sid] = []
    for ch in chapters.values():
        subj_ch[ch['subject']].append(ch)
    for sid, chs in subj_ch.items():
        chs.sort(key=lambda c: (min(q['chapter_sort'] for q in c['qs']), c['name']))

    all_papers = len({q['paper_id'] for q in rows})
    y0, y1 = span(rows)

    # Chapter hub pages
    for ch in chapters.values():
        qs = ch['qs']
        papers = len({q['paper_id'] for q in qs})
        ya, yb = span(qs)
        sname = ch['subject_name']
        cu = ch_url(ch)
        h1 = 'EAPCET %s PYQs (%d\u2013%d), chapter-wise' % (ch['name'], ya, yb)
        title = base.clip('EAPCET %s PYQs %d\u2013%d (%s) | EdLoop' % (ch['name'], ya, yb, sname), 65)
        if len(title) > 65:
            title = base.clip('EAPCET %s PYQs (%s) | EdLoop' % (ch['name'], sname), 65)
        desc = '%s previous-year AP and TS EAPCET questions on %s (%s) from %d papers, %d\u2013%d. Read each question with its options, answer and paper; get the step-by-step solution in EdLoop.' % (
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
            lst += '<h4>%s</h4><ul class="q-list">' % E(paper_short(gq[0]))
            for q in sorted(gq, key=lambda q: (q['qno'] or 0, q['id'])):
                lst += '<li><a href="/eapcet/q/%s">%s</a></li>' % (q['id'], E(base.clip(base.plain(q['title']) or base.plain(q['body']), 110)))
            lst += '</ul>'
        lst += '</div>'
        crumbs = [('EdLoop', SITE + '/'), ('EAPCET PYQs', SITE + '/eapcet/pyq/'), (sname, SITE + '/eapcet/pyq/' + SUBJECT_SLUG[ch['subject']]), (ch['name'], SITE + cu)]
        body = '''  <main id="main" class="qpage-main">
    <header class="page-band"><div class="wrap">
      %s
      <h1>%s</h1>
      <p class="tagline">%s questions from %d papers, %d to %d. Open any question to read it in full with its options.</p>
    </div></header>
    <div class="wrap q-wrap q-wide">
      <p class="q-intro">%s is part of the EAPCET %s syllabus. This page lists every %s question we have on it, newest paper first, from AP EAPCET and TS EAPCET (%d to %d). All questions come from the councils' official papers with preliminary and final keys.</p>
      <section class="q-cta q-cta-slim"><p><strong>Step-by-step solutions are in EdLoop.</strong> Free on Android, no ads.</p>
        <div class="q-actions"><a class="btn btn-solid" href="%s&amp;referrer=utm_source%%3Dedloop.in%%26utm_campaign%%3Deapcet_pyq" rel="noopener">Get EdLoop on Google Play</a></div></section>
      <h2 class="q-list-head">Every %s question, newest first</h2>
      %s
    </div>
  </main>
''' % (base.crumbs_html(crumbs), E(h1), nfmt(len(qs)), papers, ya, yb, E(ch['name']), E(sname), E(ch['name']),
       ya, yb, PLAY.replace('&', '&amp;'), E(ch['name']), lst)
        write('eapcet/pyq/%s/%s.html' % (SUBJECT_SLUG[ch['subject']], ch['slug']),
              page(chrome, title, desc, SITE + cu, body, extra=base.crumbs_json(crumbs)))
        hub_urls.append(SITE + cu)

    # Subject hub pages
    for sid, chs in subj_ch.items():
        sname = chs[0]['subject_name']
        qs_all = [q for c in chs for q in c['qs']]
        ya, yb = span(qs_all)
        su = '/eapcet/pyq/' + SUBJECT_SLUG[sid]
        cards = ''.join('<li><a href="%s"><strong>%s</strong><span>%s questions &middot; %d\u2013%d</span></a></li>' % (
            ch_url(c), E(c['name']), nfmt(len(c['qs'])), span(c['qs'])[0], span(c['qs'])[1]) for c in chs)
        crumbs = [('EdLoop', SITE + '/'), ('EAPCET PYQs', SITE + '/eapcet/pyq/'), (sname, SITE + su)]
        title = 'EAPCET %s PYQs, chapter-wise (%d\u2013%d) | EdLoop' % (sname, ya, yb)
        desc = '%s AP and TS EAPCET %s previous-year questions from %d\u2013%d in %d chapters. Pick a chapter, read the questions, check answers and solutions in EdLoop.' % (nfmt(len(qs_all)), sname, ya, yb, len(chs))
        body = '''  <main id="main" class="qpage-main">
    <header class="page-band"><div class="wrap">
      %s
      <h1>EAPCET %s PYQs, chapter-wise (%d\u2013%d)</h1>
      <p class="tagline">%s questions in %d chapters.</p>
    </div></header>
    <div class="wrap q-wrap q-wide"><ul class="q-cards">%s</ul></div>
  </main>
''' % (base.crumbs_html(crumbs), E(sname), ya, yb, nfmt(len(qs_all)), len(chs), cards)
        write('eapcet/pyq/%s.html' % SUBJECT_SLUG[sid], page(chrome, title, desc, SITE + su, body, extra=base.crumbs_json(crumbs)))
        hub_urls.append(SITE + su)

    # EAPCET Index page
    blocks = ''
    for sid, chs in subj_ch.items():
        n = sum(len(c['qs']) for c in chs)
        blocks += '<section class="q-subject"><h2><a href="/eapcet/pyq/%s">%s</a> <small>%s questions</small></h2><ul class="q-cards">%s</ul></section>' % (
            SUBJECT_SLUG[sid], E(chs[0]['subject_name']), nfmt(n),
            ''.join('<li><a href="%s"><strong>%s</strong><span>%s</span></a></li>' % (ch_url(c), E(c['name']), nfmt(len(c['qs']))) for c in chs))
    crumbs = [('EdLoop', SITE + '/'), ('EAPCET PYQs', SITE + '/eapcet/pyq/')]
    title = 'EAPCET Previous Year Questions (PYQ) by Chapter | EdLoop'
    desc = '%s AP and TS EAPCET previous-year questions from %d papers (%d\u2013%d), sorted by subject and chapter. Read them free with answers; step-by-step solutions are in the EdLoop app.' % (nfmt(len(rows)), all_papers, y0, y1)
    body = '''  <main id="main" class="qpage-main">
    <header class="page-band"><div class="wrap">
      %s
      <h1>EAPCET previous year questions, chapter-wise</h1>
      <p class="tagline">%s questions from %d papers, %d\u2013%d: AP EAPCET (and AP EAMCET) and TS EAPCET. All papers are from the councils\' official tests.</p>
    </div></header>
    <div class="wrap q-wrap q-wide">%s</div>
  </main>
''' % (base.crumbs_html(crumbs), nfmt(len(rows)), all_papers, y0, y1, blocks)
    write('eapcet/pyq/index.html', page(chrome, title, desc, SITE + '/eapcet/pyq/', body, extra=base.crumbs_json(crumbs)))
    hub_urls.insert(0, SITE + '/eapcet/pyq/')

    # ---- Sitemaps
    def urlset(items):
        s = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        for u in items:
            s += '<url><loc>%s</loc><lastmod>%s</lastmod></url>\n' % (u, lastmod)
        return s + '</urlset>\n'

    # 1. Update sitemap-pages.xml to include EAPCET hub URLs
    sp_path = os.path.join(root, 'sitemap-pages.xml')
    pages_urls = []
    if os.path.exists(sp_path):
        content = open(sp_path, encoding='utf-8').read()
        pages_urls = re.findall(r'<loc>([^<]+)</loc>', content)
    # Filter out any existing eapcet/pyq urls then append the new ones
    pages_urls = [u for u in pages_urls if '/eapcet/pyq' not in u]
    # Insert EAPCET hub urls right after /eapcet/ if present, or at the end
    if SITE + '/eapcet/' in pages_urls:
        idx = pages_urls.index(SITE + '/eapcet/') + 1
        pages_urls[idx:idx] = hub_urls
    else:
        pages_urls.extend(hub_urls)
    write('sitemap-pages.xml', urlset(pages_urls))

    # 2. Write subject sitemaps for EAPCET
    eapcet_sitemaps = []
    for sid in SUBJECT_ORDER:
        if sid in urls:
            nm = 'sitemap-eapcet-q-%s.xml' % SUBJECT_SLUG[sid]
            items = ['%s/eapcet/q/%s' % (SITE, q) for q in urls[sid]]
            assert len(items) <= 50000
            write(nm, urlset(items))
            eapcet_sitemaps.append(nm)

    # 3. Update sitemap.xml (index)
    sm_path = os.path.join(root, 'sitemap.xml')
    existing_sitemaps = []
    if os.path.exists(sm_path):
        sm_content = open(sm_path, encoding='utf-8').read()
        existing_sitemaps = re.findall(r'<loc>%s/([^<]+)</loc>' % SITE, sm_content)
    all_sitemaps = [s for s in existing_sitemaps if not s.startswith('sitemap-eapcet-')]
    for esm in eapcet_sitemaps:
        if esm not in all_sitemaps:
            all_sitemaps.append(esm)
    write('sitemap.xml', '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          ''.join('<sitemap><loc>%s/%s</loc><lastmod>%s</lastmod></sitemap>\n' % (SITE, n, lastmod) for n in all_sitemaps) + '</sitemapindex>\n')

    dup = [t for t, c in titles.items() if c > 1]
    print('question pages: %d  (with image: %d)' % (len(rows), n_img))
    print('chapters: %d  subjects: %d' % (len(chapters), len(subj_ch)))
    print('sitemap URLs: %d  (questions %d, hub pages %d)' % (len(rows) + len(hub_urls), len(rows), len(hub_urls)))
    print('html bytes: %s  image bytes: %s' % (nfmt(sizes['html']), nfmt(sizes['img'])))
    print('total EAPCET bytes (html + img): %s (%.2f MB)' % (nfmt(sizes['html'] + sizes['img']), (sizes['html'] + sizes['img']) / 1024 / 1024))
    print('duplicate titles:', len(dup))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('db')
    ap.add_argument('--out', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
    ap.add_argument('--lastmod', default=None)
    ap.add_argument('--family', default='eapcet')
    a = ap.parse_args(argv)
    run(a.db, out=a.out, lastmod=a.lastmod)


if __name__ == '__main__':
    main()
