"""Rebuild the "What comes again" card in the home page hero from the question bank.

    python tools/make_hero_card.py path/to/content.jee.sqlite          # rewrite index.html
    python tools/make_hero_card.py path/to/content.jee.sqlite --check  # print, write nothing

The database is built in the private IIT-APP repository (`python scripts/build_db.py --family jee --out <file>`);
only the counts reach this public repository. The card shows the five most asked chapters (by distinct papers),
one cell per year from the oldest to the newest paper. A cell's colour is questions per paper that year, so a
year with one paper (2002) compares fairly with a year that has twenty-four. Sample papers are excluded.

Run it after the bank grows (docs/08 section 8), together with the numbers in the hero line, the meta description
and assets/brand/make_social.html. The script only rewrites what lies between the two marker comments in index.html.
"""
import html
import pathlib
import re
import sqlite3
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / "index.html"
START, END = "<!-- hero-card:start -->", "<!-- hero-card:end -->"
LEVELS = ["#eef1ff", "#c9cffb", "#9ea6f6", "#6f75ee", "#4f46e5"]  # 0 questions, then four steps
SHORT = {
    "Three Dimensional Geometry": "3D Geometry",
    "Semiconductor Electronics": "Semiconductors",
    "Units, Dimensions & Errors": "Units & Dimensions",
    "Coordination Compounds": "Coordination Cpds",
}
ROWS = 5


def load(db_path):
    c = sqlite3.connect(db_path).cursor()
    papers_total = c.execute("select count(*) from paper where source <> 'sample'").fetchone()[0]
    per_year = dict(c.execute("select year, count(*) from paper where source <> 'sample' group by year"))
    years = list(range(min(per_year), max(per_year) + 1))
    top = c.execute(
        """select q.chapter_id, ch.name, count(distinct p.id) as papers
           from v_real_question q join paper p on p.id = q.paper_id join chapter ch on ch.id = q.chapter_id
           group by q.chapter_id order by papers desc, count(*) desc limit ?""",
        (ROWS,),
    ).fetchall()
    chapters = []
    for cid, name, papers in top:
        by_year = dict(
            c.execute(
                """select p.year, count(*) from v_real_question q join paper p on p.id = q.paper_id
                   where q.chapter_id = ? group by p.year""",
                (cid,),
            )
        )
        chapters.append((name, papers, [by_year.get(y, 0) for y in years]))
    return papers_total, years, [per_year.get(y, 0) for y in years], chapters


def cells(by_year, per_year):
    rates = [v / p if p else 0 for v, p in zip(by_year, per_year)]
    top = max(rates) or 1
    out = []
    for v, p, r in zip(by_year, per_year, rates):
        level = 0 if v == 0 else min(4, 1 + int(3.999 * r / top))
        out.append(f'<i style="--c:{LEVELS[level]}" title="{v} questions in {p} papers"></i>')
    return "".join(out)


def card(papers_total, years, per_year, chapters):
    rows = "".join(
        f'<div class="freq-row"><b title="{html.escape(name)}">{html.escape(SHORT.get(name, name))}</b>'
        f'<div class="freq-cells">{cells(by_year, per_year)}</div></div>'
        for name, _papers, by_year in chapters
    )
    ticks = [years[0], years[len(years) // 3], years[2 * len(years) // 3], years[-1]]
    return (
        f'<div class="freq" role="img" aria-label="Five of the most asked chapters, with how many questions each year '
        f'from {years[0]} to {years[-1]} across {papers_total} papers">'
        f'<div class="freq-head"><strong>What comes again</strong><span>questions per year · {papers_total} papers</span></div>'
        f"{rows}"
        f'<div class="freq-years"><span></span><div>' + "".join(f"<span>{y}</span>" for y in ticks) + "</div></div>"
        '<div class="freq-foot">Drawn from the question bank, updated with every new paper · '
        '<a href="#practice">Try a question</a></div>'
        "</div>"
    )


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    papers_total, years, per_year, chapters = load(args[0])
    block = card(papers_total, years, per_year, chapters)
    shown = re.search(r"<li><strong>(\d+)</strong><span>past papers</span>", INDEX.read_text(encoding="utf-8"))
    if shown and int(shown.group(1)) != papers_total:
        print(f"WARNING: the hero line says {shown.group(1)} papers, the database has {papers_total}. Update both together.")
    for name, papers, _ in chapters:
        print(f"  {name}: in {papers} of {papers_total} papers")
    print(f"years {years[0]}-{years[-1]}, {papers_total} papers")
    if "--check" in sys.argv:
        return
    text = INDEX.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit(f"index.html has no {START} ... {END} markers")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    INDEX.write_text(head + START + block + END + tail, encoding="utf-8")
    print("index.html updated")


main()
