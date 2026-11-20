#!/usr/bin/env python3
"""Check chapter guides against their facts files and the format rules in tools/guides.py.

    python tools/check_guides.py                 every guide under guides/jee/
    python tools/check_guides.py physics/rotational-motion [...]

Exit code 0 = all pass. Run it after writing or changing any guide; a guide that fails is not published.
"""
import glob, json, os, sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guides  # noqa: E402

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


def main():
    idx = json.load(open(os.path.join(ROOT, 'guides', 'facts', 'index.json'), encoding='utf-8'))
    paths = {'/jee/pyq/', '/jee/pyq/physics', '/jee/pyq/chemistry', '/jee/pyq/mathematics', '/jee/', '/get'}
    paths |= {'/jee/pyq/%s/%s' % (c['subject'], c['slug']) for c in idx['chapters']}
    want = sys.argv[1:] or sorted(os.path.relpath(p, os.path.join(ROOT, 'guides', 'jee')).replace(os.sep, '/')[:-3]
                                  for p in glob.glob(os.path.join(ROOT, 'guides', 'jee', '*', '*.md')))
    bad = 0
    for key in want:
        subj, slug = key.split('/')
        fp, gp = guides.facts_path(ROOT, subj, slug), guides.guide_path(ROOT, subj, slug)
        if not os.path.exists(fp):
            print('FAIL %s: no facts file (is the slug right?)' % key); bad += 1; continue
        if not os.path.exists(gp):
            print('FAIL %s: no guide file' % key); bad += 1; continue
        facts = json.load(open(fp, encoding='utf-8'))
        src = open(gp, encoding='utf-8').read()
        ids = {c['id'] for c in facts['question_candidates']}
        probs = guides.check(src, facts, ids, paths - {facts['page_url']})
        if probs:
            bad += 1
            print('FAIL %s' % key)
            for p in probs:
                print('   - ' + p)
        else:
            print('ok   %s' % key)
    print('\n%d checked, %d failed' % (len(want), bad))
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
