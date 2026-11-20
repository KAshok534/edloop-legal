"""Chapter guides: the Markdown format, its renderer and its checks (shared by make_question_pages.py and check_guides.py).

A guide is <guides root>/jee/<subject>/<chapter slug>.md, written from <guides root>/facts/<subject>/<chapter slug>.json
(guides root: see guides_root(); it is outside this public repo).
Format (nothing else is allowed):
    ## Heading                      the six fixed sections, in this order (SECTIONS)
    ### Question?                   only inside "Frequently asked questions"; the next paragraph is its answer
    paragraphs, "- " lists, **bold**, and links [text](/q/<id>) or [text](/jee/pyq/...)
No HTML, no maths markup ($), no images, no tables, no outside links.
"""
import html, json, os, re

E = html.escape
SECTIONS = [
    'How often it comes up',
    'Most-asked topics',
    'What the questions look like',
    'Questions to try first',
    'How to practise it',
    'Frequently asked questions',
]
BANNED = [  # claims we cannot back, rank/score promises, other brands, coaching names
    r'\bguarantee', r'\bbest\b', r'\btop[- ]?ranked\b', r'#\s?1\b', r'\bnumber one\b', r'\btopper', r'(?-i:\bAIR\b)', r'\brank holder',
    r'\bsure[- ]?shot\b', r'\bmust[- ]?do\b', r'\b100\s?%', r'\bpercentile\b', r'\bexpected (?:questions|paper)\b',
    r'\bwill (?:definitely|surely|certainly) (?:come|be asked)', r'\bpredict', r'\bleak',
    r'\ballen\b', r'\baakash\b', r'\bfiitjee\b', r'(?-i:\bResonance (?:Eduventures|coaching|institute))', r'\bmathongo\b', r'\bphysics ?wallah\b', r'\bPW\b',
    r'\bvedantu\b', r'\bunacademy\b', r'\bexamgoal\b', r'\bexamside\b', r'\bmarks app\b', r'\bembibe\b', r'\btoppr\b',
    r'\bhigh(?:est)?[- ]yield', r'\bscor(?:e|ing)\b',
    r'\bchatgpt\b', r'\bgemini\b', r'\bclaude\b', r'\bAI[- ]generated\b',
]
LINK_RE = re.compile(r'\[([^\]\n]+)\]\((/[^)\s]*)\)')
NUM_RE = re.compile(r'(?<![\w.])\d+(?:,\d{3})*(?:\.\d+)?')


def guides_root(site_root=None):
    """The guides folder (README, facts/, jee/) lives in the private IIT APP repo (marketing/chapter-guides), not in this
    public site repo. Set EDLOOP_GUIDES to it, or keep IIT APP next to this checkout. -> abspath or None."""
    d = os.environ.get('EDLOOP_GUIDES')
    if d:
        return os.path.abspath(d)
    site_root = site_root or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
    c = os.path.join(site_root, '..', 'IIT APP', 'marketing', 'chapter-guides')
    return os.path.abspath(c) if os.path.isdir(c) else None


def guide_path(groot, subject_slug, chapter_slug):
    return os.path.join(groot, 'jee', subject_slug, chapter_slug + '.md')


def facts_path(groot, subject_slug, chapter_slug):
    return os.path.join(groot, 'facts', subject_slug, chapter_slug + '.json')


def _inline(s):
    out, last = [], 0
    for m in LINK_RE.finditer(s):
        out.append(E(s[last:m.start()], quote=False))
        out.append('<a href="%s">%s</a>' % (E(m.group(2)), E(m.group(1), quote=False)))
        last = m.end()
    out.append(E(s[last:], quote=False))
    t = ''.join(out)
    return re.sub(r'\*\*([^*\n]+)\*\*', r'<strong>\1</strong>', t)


def parse(src):
    """-> list of (kind, payload): ('h2', text) ('h3', text) ('p', text) ('ul', [items])."""
    blocks, lines, i = [], src.replace('\r\n', '\n').split('\n'), 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            i += 1
            continue
        if ln.startswith('## '):
            blocks.append(('h2', ln[3:].strip())); i += 1; continue
        if ln.startswith('### '):
            blocks.append(('h3', ln[4:].strip())); i += 1; continue
        if re.match(r'-\s+\S', ln):
            items = []
            while i < len(lines) and re.match(r'-\s+\S', lines[i]):
                items.append(lines[i][1:].strip()); i += 1
            blocks.append(('ul', items)); continue
        para = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(('## ', '### ')) and not re.match(r'-\s+\S', lines[i]):
            para.append(lines[i].strip()); i += 1
        blocks.append(('p', ' '.join(para)))
    return blocks


def render(src, chapter):
    """-> (html, faq list [(question, answer plain text)])."""
    blocks = parse(src)
    out, faq, in_faq, pending_q = [], [], False, None
    for kind, val in blocks:
        if kind == 'h2':
            in_faq = val == 'Frequently asked questions'
            out.append('<h2>%s</h2>' % E(val))
        elif kind == 'h3':
            out.append('<h3>%s</h3>' % E(val))
            pending_q = val if in_faq else None
        elif kind == 'p':
            out.append('<p>%s</p>' % _inline(val))
            if pending_q:
                faq.append((pending_q, re.sub(r'\*\*', '', LINK_RE.sub(r'\1', val))))
                pending_q = None
        else:
            out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % _inline(x) for x in val))
    return ('<section class="q-guide" aria-label="%s guide">\n%s\n</section>' % (E(chapter), '\n'.join(out))), faq


def faq_jsonld(faq):
    if not faq:
        return ''
    return ('  <script type="application/ld+json">%s</script>\n' % json.dumps({
        '@context': 'https://schema.org', '@type': 'FAQPage',
        'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in faq]
    }, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/'))


def allowed_numbers(facts):
    """Every number a guide may print: all values in the facts file (ints, 1-decimal floats, years) plus 2027."""
    nums = set()

    def walk(v):
        if isinstance(v, bool) or v is None:
            return
        if isinstance(v, (int, float)):
            nums.add(_norm(str(v)))
        elif isinstance(v, str):
            for m in NUM_RE.findall(v):
                nums.add(_norm(m))
        elif isinstance(v, dict):
            for k, x in v.items():
                if k.isdigit():  # the years of by_year
                    nums.add(k)
                if k not in ('id', 'url', 'page_url', 'chapter_id', 'facts', 'guide', 'database_built_at', 'source'):
                    walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
    walk(facts)
    nums.add('2027')
    return nums


def _norm(s):
    s = s.replace(',', '')
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s


def check(src, facts, valid_q_ids, valid_paths):
    """-> list of problems (empty = passes)."""
    probs = []
    if re.search(r'<[a-zA-Z/]', src):
        probs.append('HTML is not allowed')
    if '$' in src or '\\(' in src:
        probs.append('maths markup ($ or \\() is not allowed; write plain words or Unicode (e.g. ω, ², √)')
    if re.search(r'!\[|^\s*\|', src, re.M):
        probs.append('images and tables are not allowed')
    if re.search(r'\]\((?!/)', src) or re.search(r'https?://', src):
        probs.append('only site links starting with / are allowed (no outside links, no Play link: the page already has one)')
    if re.search(r'^#(?!#)', src, re.M):
        probs.append('no "# title" line: the page already has its title; start with "## How often it comes up"')
    blocks = parse(src)
    if blocks and blocks[0] != ('h2', SECTIONS[0]):
        probs.append('nothing may come before "## How often it comes up" (move any intro sentence into that section)')
    heads = [v for k, v in blocks if k == 'h2']
    if heads != SECTIONS:
        probs.append('sections must be exactly, in order: %s (found: %s)' % (SECTIONS, heads))
    if any(k == 'h3' for k, _ in blocks[:next((i for i, (k, v) in enumerate(blocks) if k == 'h2' and v == SECTIONS[-1]), len(blocks))]):
        probs.append('### is only for FAQ questions')
    faq_q = [v for k, v in blocks if k == 'h3']
    if not 3 <= len(faq_q) <= 5:
        probs.append('FAQ needs 3 to 5 questions (found %d)' % len(faq_q))
    for q in faq_q:
        if not q.endswith('?'):
            probs.append('FAQ heading must be a question ending in "?": %s' % q)
    text = re.sub(r'\]\([^)]*\)', ']', src)
    words = len(re.findall(r"[A-Za-z][A-Za-z'’-]*", text))
    lo = 550 if facts.get('in_current_syllabus', True) else 300
    if not lo <= words <= 1000:
        probs.append('length must be %d to 1000 words (found %d)' % (lo, words))
    ok = allowed_numbers(facts)
    bad = sorted({n for n in NUM_RE.findall(text) if _norm(n) not in ok})
    if bad:
        probs.append('numbers not in the facts file: %s (use only numbers from the facts file; write other counts in words only if they are not data)' % bad)
    for pat in BANNED:
        m = re.search(pat, text, re.I)
        if m:
            probs.append('banned word or claim: "%s"' % m.group(0))
    # claims about frequency and trend must match the facts file
    sec1 = src.split('## ' + SECTIONS[1])[0]
    up_w = re.search(r'\b(grow|grew|grown|growing|risen|rose|rising|increas\w*|more often|gained|climb\w*|upward)\b', sec1, re.I)
    down_w = re.search(r'\b(shr[ui]nk\w*|fallen|fell|falling|declin\w*|decreas\w*|less often|dropp\w*|downward|lost ground)\b', sec1, re.I)
    tr = (facts.get('trend') or {})
    trends = {tr.get('share_2002_2018_vs_2024_2026'), tr.get('share_2019_2026_vs_2024_2026')}
    if up_w and 'up' not in trends:
        probs.append('"%s": the facts trend is not up (trend: %s)' % (up_w.group(0), tr))
    if down_w and 'down' not in trends:
        probs.append('"%s": the facts trend is not down (trend: %s)' % (down_w.group(0), tr))
    if re.search(r'\bevery (?:single )?(?:paper|shift)\b|\bin your shift\b|\beach (?:paper|shift)\b', src, re.I)             and not facts.get('appears_in_every_paper_2019_2026'):
        probs.append('says "every paper/shift" but the chapter was not in every paper 2019-2026 (papers_with_this_chapter < papers_in_our_set)')
    if re.search(r'no year without|every year since 2019|each year since 2019|every year from 2019', src, re.I)             and not facts.get('appears_every_year_2019_2026'):
        probs.append('says "every year since 2019" but years_not_asked_since_2019 is not empty')
    links = LINK_RE.findall(src)
    qlinks = [u for _, u in links if u.startswith('/q/')]
    for _, u in links:
        if u.startswith('/q/'):
            if u[3:] not in valid_q_ids:
                probs.append('question link is not a question of this chapter: %s' % u)
        elif u not in valid_paths:
            probs.append('unknown site link: %s' % u)
    if not 3 <= len(qlinks) <= 6:
        probs.append('link 3 to 6 questions of this chapter (found %d)' % len(qlinks))
    if len(set(qlinks)) != len(qlinks):
        probs.append('the same question is linked twice')
    if re.search(r'[—]', src):
        probs.append('no em dashes (—); use a comma, colon or full stop')
    return probs
