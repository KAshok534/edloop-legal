"""Rebuild an app page's year grid ("Twenty-five years of papers", "Five years of both papers") from the question bank.

    python tools/make_years.py path/to/content.sqlite                      # EdLoop JEE: rewrite jee/index.html
    python tools/make_years.py path/to/content.sqlite --exam eapcet        # EdLoop EAPCET: rewrite eapcet/index.html
    python tools/make_years.py path/to/content.sqlite --exam eapcet --check  # print, write nothing

The database is built in the private IIT-APP repository (`python scripts/build_db.py --family jee --out <file>`, or the
combined Prod content file, which holds both apps); only counts reach this public repository. The grid shows the two
most asked chapters of each subject (by distinct papers), one cell per year from the oldest to the newest paper; a
cell's level is questions per paper that year, so a year with one paper compares fairly with a year that has
twenty-four. Sample papers are excluded, and each app counts only its own exams.

The grid is static HTML, complete without JavaScript (every year shown). premium.js reads the JSON beside it to run
the scroll sequence (the year, the exam's name, its papers, the running total and a note). The script rewrites only
what lies between the `years:start` and `years:end` marker comments in the app's page. Run it with the other numbers
when the bank grows (docs/08 section 8).
"""
import html
import json
import pathlib
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parent.parent
START, END = "<!-- years:start -->", "<!-- years:end -->"
PER_SUBJECT = 2
# page, exams counted, subjects in the paper's order, and how the scroll sequence names the exam
APPS = {
    "jee": {"page": ROOT / "jee" / "index.html", "exams": ("AIEEE", "JEE_MAIN"),
            "subjects": [("phy", "Physics"), ("chem", "Chemistry"), ("math", "Maths")], "label": "papers"},
    "eapcet": {"page": ROOT / "eapcet" / "index.html", "exams": ("AP_EAPCET", "TS_EAPCET"),
               "subjects": [("math", "Maths"), ("phy", "Physics"), ("chem", "Chemistry")], "label": "AP and TS EAPCET papers"},
}
SHORT = {
    "Three Dimensional Geometry": "3D Geometry",
    "Semiconductor Electronics": "Semiconductors",
    "Units, Dimensions & Errors": "Units & Dimensions",
    "Coordination Compounds": "Coordination Cpds",
    "Chemical Bonding & Molecular Structure": "Chemical Bonding",
}


def load(db_path, app):
    c = sqlite3.connect(db_path).cursor()
    exams = APPS[app]["exams"]
    marks = ",".join("?" * len(exams))
    per_year = dict(c.execute(
        f"select year, count(*) from paper where source <> 'sample' and exam in ({marks}) group by year", exams))
    years = list(range(min(per_year), max(per_year) + 1))
    papers = [per_year.get(y, 0) for y in years]
    rows = []
    for sid, sname in APPS[app]["subjects"]:
        top = c.execute(
            f"""select q.chapter_id, ch.name, count(distinct p.id) as n
               from v_real_question q join paper p on p.id = q.paper_id join chapter ch on ch.id = q.chapter_id
               where q.subject_id = ? and p.exam in ({marks}) group by q.chapter_id order by n desc, count(*) desc limit ?""",
            (sid, *exams, PER_SUBJECT),
        ).fetchall()
        for cid, name, n in top:
            by_year = dict(c.execute(
                f"""select p.year, count(*) from v_real_question q join paper p on p.id = q.paper_id
                   where q.chapter_id = ? and p.exam in ({marks}) group by p.year""", (cid, *exams)))
            rows.append({"subject": sname, "name": name, "papers": n, "by_year": [by_year.get(y, 0) for y in years]})
    extra = {}
    if app == "eapcet":  # the sequence names both exams and says how each year splits between AP and TS
        split = {}
        for exam, year, n in c.execute(
                "select exam, year, count(*) from paper where source <> 'sample' and exam in ('AP_EAPCET', 'TS_EAPCET') group by exam, year"):
            split.setdefault(year, {})[exam] = n
        extra = {"exams": [[years[0], "AP + TS EAPCET"]],
                 "notes": [[y, f"AP {split.get(y, {}).get('AP_EAPCET', 0)} papers, TS {split.get(y, {}).get('TS_EAPCET', 0)}."]
                           for y in years]}
    return years, papers, rows, extra


def level(v, p, top):
    if not v or not p:
        return 0
    return min(4, 1 + int(3.999 * (v / p) / top))


def block(years, papers, rows, extra, label):
    total = sum(papers)
    out = [f'<div class="yr-grid" role="img" aria-label="The two most asked chapters of each subject, questions per paper in every '
           f'year from {years[0]} to {years[-1]}, across {total} {label}" style="--n:{len(years)}">']
    for r in rows:
        top = max((v / p) for v, p in zip(r["by_year"], papers) if p) or 1
        cells = "".join(
            f'<i class="l{level(v, p, top)}" data-i="{i}" title="{y}: {v} questions in {p} papers"></i>'
            for i, (y, v, p) in enumerate(zip(years, r["by_year"], papers)))
        where = f"in all {total} papers" if r["papers"] == total else f"in {r['papers']} of {total} papers"
        out.append(f'<div class="yr-row"><b title="{html.escape(r["name"])}">{html.escape(SHORT.get(r["name"], r["name"]))}'
                   f'<small>{r["subject"]} · {where}</small></b><div class="yr-cells">{cells}</div></div>')
    out.append(f'<div class="yr-axis"><span></span><div><span>{years[0]}</span><span>{years[len(years) // 2]}</span>'
               f'<span>{years[-1]}</span></div></div></div>')
    data = {"years": years, "papers": papers, "total": total, **extra}
    out.append(f'<script type="application/json" id="years-data">{json.dumps(data, separators=(",", ":"))}</script>')
    return "".join(out), total


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    app = "jee"
    if "--exam" in sys.argv:
        app = sys.argv[sys.argv.index("--exam") + 1]
        args = [a for a in args if a != app]
    if not args or app not in APPS:
        sys.exit(__doc__)
    years, papers, rows, extra = load(args[0], app)
    text, total = block(years, papers, rows, extra, APPS[app]["label"])
    for r in rows:
        print(f"  {r['subject']}: {r['name']} in {r['papers']} of {total} papers")
    print(f"{app}: years {years[0]}-{years[-1]}, {total} papers; per year {papers}")
    if "--check" in sys.argv:
        return
    target = APPS[app]["page"]
    page = target.read_text(encoding="utf-8")
    if START not in page or END not in page:
        sys.exit(f"{target.relative_to(ROOT)} has no {START} ... {END} markers")
    head, rest = page.split(START, 1)
    _, tail = rest.split(END, 1)
    target.write_text(head + START + text + END + tail, encoding="utf-8")
    print(f"{target.relative_to(ROOT).as_posix()} updated")


main()
