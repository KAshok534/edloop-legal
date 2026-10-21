"""Rebuild the "since 2002" year grid on the home page from the question bank.

    python tools/make_years.py path/to/content.jee.sqlite          # rewrite index.html
    python tools/make_years.py path/to/content.jee.sqlite --check  # print, write nothing

The database is built in the private IIT-APP repository (`python scripts/build_db.py --family jee --out <file>`);
only counts reach this public repository. The grid shows the two most asked chapters of each subject (by distinct
papers), one cell per year from the oldest to the newest paper; a cell's level is questions per paper that year, so a
year with one paper compares fairly with a year that has twenty-four. Sample papers are excluded.

The grid is static HTML, complete without JavaScript (every year shown). premium.js reads the JSON beside it to run
the scroll sequence (the year, its papers, the running total). The script rewrites only what lies between the
`years:start` and `years:end` marker comments in index.html. Run it with the other numbers when the bank grows
(docs/08 section 8).
"""
import html
import json
import pathlib
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
START, END = "<!-- years:start -->", "<!-- years:end -->"
SUBJECTS = [("phy", "Physics"), ("chem", "Chemistry"), ("math", "Maths")]
PER_SUBJECT = 2
SHORT = {
    "Three Dimensional Geometry": "3D Geometry",
    "Semiconductor Electronics": "Semiconductors",
    "Units, Dimensions & Errors": "Units & Dimensions",
    "Coordination Compounds": "Coordination Cpds",
}


def load(db_path):
    c = sqlite3.connect(db_path).cursor()
    per_year = dict(c.execute("select year, count(*) from paper where source <> 'sample' group by year"))
    years = list(range(min(per_year), max(per_year) + 1))
    papers = [per_year.get(y, 0) for y in years]
    rows = []
    for sid, sname in SUBJECTS:
        top = c.execute(
            """select q.chapter_id, ch.name, count(distinct p.id) as n
               from v_real_question q join paper p on p.id = q.paper_id join chapter ch on ch.id = q.chapter_id
               where q.subject_id = ? group by q.chapter_id order by n desc, count(*) desc limit ?""",
            (sid, PER_SUBJECT),
        ).fetchall()
        for cid, name, n in top:
            by_year = dict(c.execute(
                """select p.year, count(*) from v_real_question q join paper p on p.id = q.paper_id
                   where q.chapter_id = ? group by p.year""", (cid,)))
            rows.append({"subject": sname, "name": name, "papers": n, "by_year": [by_year.get(y, 0) for y in years]})
    return years, papers, rows


def level(v, p, top):
    if not v or not p:
        return 0
    return min(4, 1 + int(3.999 * (v / p) / top))


def block(years, papers, rows):
    total = sum(papers)
    out = [f'<div class="yr-grid" role="img" aria-label="The two most asked chapters of each subject, questions per paper in every '
           f'year from {years[0]} to {years[-1]}, across {total} papers" style="--n:{len(years)}">']
    for r in rows:
        top = max((v / p) for v, p in zip(r["by_year"], papers) if p) or 1
        cells = "".join(
            f'<i class="l{level(v, p, top)}" data-i="{i}" title="{y}: {v} questions in {p} papers"></i>'
            for i, (y, v, p) in enumerate(zip(years, r["by_year"], papers)))
        out.append(f'<div class="yr-row"><b title="{html.escape(r["name"])}">{html.escape(SHORT.get(r["name"], r["name"]))}'
                   f'<small>{r["subject"]} · in {r["papers"]} of {total} papers</small></b><div class="yr-cells">{cells}</div></div>')
    out.append(f'<div class="yr-axis"><span></span><div><span>{years[0]}</span><span>{years[len(years) // 2]}</span>'
               f'<span>{years[-1]}</span></div></div></div>')
    data = {"years": years, "papers": papers, "total": total}
    out.append(f'<script type="application/json" id="years-data">{json.dumps(data, separators=(",", ":"))}</script>')
    return "".join(out), total


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    years, papers, rows = load(args[0])
    text, total = block(years, papers, rows)
    for r in rows:
        print(f"  {r['subject']}: {r['name']} in {r['papers']} of {total} papers")
    print(f"years {years[0]}-{years[-1]}, {total} papers; per year {papers}")
    if "--check" in sys.argv:
        return
    page = INDEX.read_text(encoding="utf-8")
    if START not in page or END not in page:
        sys.exit(f"index.html has no {START} ... {END} markers")
    head, rest = page.split(START, 1)
    _, tail = rest.split(END, 1)
    INDEX.write_text(head + START + text + END + tail, encoding="utf-8")
    print("index.html updated")


main()
