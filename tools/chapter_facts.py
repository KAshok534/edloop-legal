#!/usr/bin/env python3
"""Exact numbers for the chapter guides: one JSON per JEE chapter, read from the content database.

    python tools/chapter_facts.py <path to content.sqlite> [--out <guides root>/facts]

Writes <guides root>/facts/<subject>/<chapter slug>.json (the same slugs as the chapter pages that
tools/make_question_pages.py builds) and <guides root>/facts/index.json (the list of chapters).

A guide may only state a number that is in its facts file (tools/check_guides.py enforces it). The writer never counts
or estimates anything itself. Same question set as the website: verified questions of JEE-family papers (JEE Main,
AIEEE), sample papers excluded. Topic names come from the shared taxonomy; archetypes, concepts, hints, solutions and
the other app-only columns are never read.
"""
import argparse, collections, json, os, sqlite3, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_question_pages import SUBJECT_SLUG, plain, slugify, clip  # noqa: E402

sys.stdout.reconfigure(encoding='utf-8')
RECENT = (2019, 2026)   # NTA's online exam: several shifts a year, the current pattern family
LAST3 = (2024, 2026)


def trend(before, after):
    return 'up' if after - before >= 0.5 else 'down' if before - after >= 0.5 else 'about the same'


def r1(x):
    return round(x + 1e-9, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('db')
    ap.add_argument('--out', default=None, help='default: <guides root>/facts (tools/guides.py guides_root)')
    a = ap.parse_args()
    if a.out is None:
        import guides
        g = guides.guides_root()
        if not g:
            sys.exit('guides folder not found: set EDLOOP_GUIDES to IIT APP/marketing/chapter-guides')
        a.out = os.path.join(g, 'facts')
    db = sqlite3.connect('file:%s?mode=ro' % os.path.abspath(a.db).replace('\\', '/'), uri=True)
    db.row_factory = sqlite3.Row
    meta = dict(db.execute('select key, value from content_meta').fetchall())

    rows = db.execute('''
        SELECT q.id, q.qno, q.subject_id, q.chapter_id, q.qtype, q.title, q.body, q.primary_topic_id,
               t.name AS topic_name, p.id AS paper_id, p.exam, p.year, p.exam_date, p.shift, p.source, p.official_name,
               c.name AS chapter_name, c.sort_order AS chapter_sort, c.class_level, c.nta_unit, c.syllabus_status,
               s.name AS subject_name, s.sort_order AS subject_sort
        FROM question q
        JOIN paper p ON p.id = q.paper_id
        JOIN exam e ON e.id = p.exam
        JOIN chapter c ON c.id = q.chapter_id
        JOIN subject s ON s.id = q.subject_id
        LEFT JOIN topic t ON t.id = q.primary_topic_id
        WHERE e.family = 'jee' AND p.source <> 'sample' AND q.verification = 'verified'
        ORDER BY p.year, COALESCE(p.exam_date, ''), p.id, q.subject_id, q.qno, q.id''').fetchall()
    removed = {r['chapter_id']: r['removed_year'] for r in db.execute(
        "SELECT chapter_id, MAX(removed_year) AS removed_year FROM chapter_exam WHERE exam_id IN ('JEE_MAIN','AIEEE') "
        "GROUP BY chapter_id")}

    # papers per year (any subject), questions per subject per year
    papers_year = collections.defaultdict(set)
    subj_q = collections.Counter()           # (subject, year) -> questions
    for r in rows:
        papers_year[r['year']].add(r['paper_id'])
        subj_q[(r['subject_id'], r['year'])] += 1

    def in_win(y, w):
        return w[0] <= y <= w[1]

    def papers_in(w):
        return sum(len(v) for y, v in papers_year.items() if in_win(y, w))

    # chapters, slugs exactly as make_question_pages.py makes them
    chapters = collections.OrderedDict()
    seen = set()
    for r in sorted(rows, key=lambda r: (r['subject_sort'], r['chapter_sort'], r['chapter_id'])):
        if r['chapter_id'] in chapters:
            continue
        slug = slugify(r['chapter_name'])
        if (r['subject_id'], slug) in seen:
            slug = slugify(r['chapter_id'])
        seen.add((r['subject_id'], slug))
        chapters[r['chapter_id']] = {'r': r, 'slug': slug, 'qs': []}
    for r in rows:
        chapters[r['chapter_id']]['qs'].append(r)

    # share of the subject in the recent window, for ranking inside the subject
    share = {}
    for cid, ch in chapters.items():
        sid = ch['r']['subject_id']
        n = sum(1 for q in ch['qs'] if in_win(q['year'], RECENT))
        tot = sum(v for (s, y), v in subj_q.items() if s == sid and in_win(y, RECENT))
        share[cid] = n / tot * 100 if tot else 0.0
    rank = {}
    for sid in SUBJECT_SLUG:
        ids = sorted([c for c in chapters if chapters[c]['r']['subject_id'] == sid], key=lambda c: -share[c])
        for i, c in enumerate(ids):
            rank[c] = (i + 1, len(ids))

    index = []
    for cid, ch in chapters.items():
        r0, qs = ch['r'], ch['qs']
        sid = r0['subject_id']
        years = sorted({q['year'] for q in qs})
        by_year = collections.OrderedDict()
        for y in range(min(papers_year), max(papers_year) + 1):
            n = sum(1 for q in qs if q['year'] == y)
            np_ = len(papers_year.get(y, ()))
            if np_ == 0:
                continue
            by_year[str(y)] = {'questions': n, 'papers_in_our_set': np_,
                               'papers_with_this_chapter': len({q['paper_id'] for q in qs if q['year'] == y}),
                               'per_paper': r1(n / np_)}

        def win(w):
            n = sum(1 for q in qs if in_win(q['year'], w))
            np_ = papers_in(w)
            sub = sum(v for (s, y), v in subj_q.items() if s == sid and in_win(y, w))
            return {'from': w[0], 'to': w[1], 'questions': n, 'papers_in_our_set': np_,
                    'papers_with_this_chapter': len({q['paper_id'] for q in qs if in_win(q['year'], w)}),
                    'per_paper': r1(n / np_) if np_ else 0.0,
                    'share_of_subject_percent': r1(n / sub * 100) if sub else 0.0}

        topics = collections.OrderedDict()
        for q in qs:
            name = q['topic_name'] or 'Other'
            t = topics.setdefault(name, {'topic': name, 'questions': 0, 'questions_2019_2026': 0, 'last_year_asked': 0})
            t['questions'] += 1
            if in_win(q['year'], RECENT):
                t['questions_2019_2026'] += 1
            t['last_year_asked'] = max(t['last_year_asked'], q['year'])
        top = sorted(topics.values(), key=lambda t: (-t['questions_2019_2026'], -t['questions'], t['topic']))

        # candidates for "questions to try": recent papers first, NTA's own papers first, one per topic where possible
        def paper_label(q):
            n = q['official_name'] or ('%s %d' % ('AIEEE' if q['exam'] == 'AIEEE' else 'JEE Main', q['year']))
            return (n.replace('JEE Main', 'AIEEE') if q['exam'] == 'AIEEE' else n).replace('(', '').replace(')', '')
        pool = sorted(qs,
                      key=lambda q: (q['year'] < 2023, q['source'] == 'memory_based', -q['year'], q['exam_date'] or '', q['qno'] or 0))
        picked, used_topics = [], set()
        for pass_ in (0, 1):
            for q in pool:
                if len(picked) >= 12:
                    break
                if q['id'] in {p['id'] for p in picked}:
                    continue
                if pass_ == 0 and q['topic_name'] in used_topics:
                    continue
                used_topics.add(q['topic_name'])
                picked.append({'id': q['id'], 'url': '/q/%s' % q['id'], 'paper': paper_label(q), 'year': q['year'],
                               'type': 'numerical answer' if q['qtype'] == 'numerical' else 'multiple choice',
                               'topic': q['topic_name'] or 'Other',
                               'paper_is': 'memory based' if q['source'] == 'memory_based' else 'NTA paper',
                               'text': clip(plain(q['title']) or plain(q['body']), 160)})

        rec = win(RECENT)
        facts = {
            'chapter': r0['chapter_name'], 'subject': r0['subject_name'], 'chapter_id': cid,
            'page_url': '/jee/pyq/%s/%s' % (SUBJECT_SLUG[sid], ch['slug']),
            'class_level': r0['class_level'], 'nta_syllabus_unit': r0['nta_unit'],
            'in_current_syllabus': r0['syllabus_status'] == 'active',
            'removed_from_syllabus_in': removed.get(cid) if r0['syllabus_status'] != 'active' else None,
            'all_years': {'from': years[0], 'to': years[-1], 'questions': len(qs),
                          'papers_with_this_chapter': len({q['paper_id'] for q in qs}),
                          'papers_in_our_set': papers_in((min(papers_year), max(papers_year))),
                          'memory_based_questions': sum(1 for q in qs if q['source'] == 'memory_based')},
            'window_2019_2026': rec,
            'window_2002_2018': win((2002, 2018)),
            'window_2024_2026': win(LAST3),
            'rank_in_subject_2019_2026': {'rank': rank[cid][0], 'of_chapters': rank[cid][1],
                                          'by': 'share of the subject\'s questions, 2019-2026'},
            'trend': {
                'share_2002_2018_vs_2024_2026': trend(win((2002, 2018))['share_of_subject_percent'], win(LAST3)['share_of_subject_percent']),
                'share_2019_2026_vs_2024_2026': trend(rec['share_of_subject_percent'], win(LAST3)['share_of_subject_percent']),
                'rule': 'up / down = the later share is at least 0.5 points higher / lower; otherwise about the same. '
                        'Describe a trend only with these words.'},
            'appears_in_every_paper_2019_2026': rec['papers_with_this_chapter'] == rec['papers_in_our_set'],
            'appears_every_year_2019_2026': all(by_year.get(str(y), {}).get('questions', 0) > 0 for y in range(RECENT[0], RECENT[1] + 1)),
            'numerical_answer_questions_2019_2026': sum(1 for q in qs if in_win(q['year'], RECENT) and q['qtype'] == 'numerical'),
            'years_not_asked_since_2019': [y for y in range(RECENT[0], RECENT[1] + 1) if by_year.get(str(y), {}).get('questions', 0) == 0],
            'by_year': by_year,
            'topics_most_asked_first': top,
            'question_candidates': picked,
            'source': {'database_built_at': meta.get('built_at'), 'question_set':
                       'verified JEE Main (2013-2026) and AIEEE (2002-2012) questions, sample papers excluded',
                       'note': 'Most papers before 2026 are memory based (reconstructed by coaching institutes); 2026 papers are NTA\'s own.'},
        }
        path = os.path.join(a.out, SUBJECT_SLUG[sid], ch['slug'] + '.json')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8', newline='\n') as fh:
            json.dump(facts, fh, ensure_ascii=False, indent=1)
            fh.write('\n')
        index.append({'subject': SUBJECT_SLUG[sid], 'slug': ch['slug'], 'chapter': r0['chapter_name'],
                      'questions': len(qs), 'questions_2019_2026': rec['questions'],
                      'in_current_syllabus': facts['in_current_syllabus'],
                      'facts': '%s/%s.json' % (SUBJECT_SLUG[sid], ch['slug']),
                      'guide': 'jee/%s/%s.md' % (SUBJECT_SLUG[sid], ch['slug'])})
    with open(os.path.join(a.out, 'index.json'), 'w', encoding='utf-8', newline='\n') as fh:
        json.dump({'database_built_at': meta.get('built_at'), 'chapters': index}, fh, ensure_ascii=False, indent=1)
        fh.write('\n')
    print('chapters: %d  questions: %d  facts in %s' % (len(index), len(rows), os.path.abspath(a.out)))


if __name__ == '__main__':
    main()
