# Chapter guides: brief for the writing agent

You are writing short, factual study guides for the 89 JEE Main chapter pages on edloop.in
(`https://edloop.in/jee/pyq/<subject>/<chapter>`). Each page already lists every past question of that chapter; your guide
goes above the list and tells a student how often the chapter is asked, what gets asked, which questions to try first and
how to practise. The goal is that Google and AI answers find a useful, original page with numbers nobody else has.

Two finished examples are your model. Read both before writing anything, and match their tone, length and structure:

- `guides/jee/physics/rotational-motion.md` (facts: `guides/facts/physics/rotational-motion.json`)
- `guides/jee/mathematics/definite-integration.md` (facts: `guides/facts/mathematics/definite-integration.json`)

## The job

For every chapter in `guides/facts/index.json` that has no guide yet (87 of them), write
`guides/jee/<subject>/<slug>.md` from `guides/facts/<subject>/<slug>.json`. The `guide` field in `index.json` gives the exact path.

Work one subject at a time (physics, then chemistry, then mathematics). After **each** guide run

    python tools/check_guides.py <subject>/<slug>

and fix the guide until it prints `ok`. After each batch of about ten guides, commit them (see Git below).

## Hard rules (the checker enforces most of them; a guide that fails is not published)

1. **Every number comes from the facts file.** Never count, estimate, round differently or compute a new number (no sums,
   no differences, no percentages of your own). Copy the value as it is in the JSON (`1.5`, `5.3%`, `241`). If a number you
   want is not in the file, write the sentence without it. Use each number for the thing the JSON says it is: `per_paper`
   is questions per paper, `share_of_subject_percent` is the share of that subject's questions, `papers_in_our_set` is the
   number of papers in our collection (not the number NTA held), `papers_with_this_chapter` is how many of them had at
   least one question from the chapter.
2. **Say "the papers we hold"** (or "in our set") whenever you give a count. Most papers before 2026 are memory based
   (reconstructed by coaching institutes); 2026 papers are NTA's own. Do not claim we have every paper.
3. **No promises or predictions.** Never say a topic *will* come, never "important questions", "expected", "sure shot",
   "must do", "best", "guaranteed", ranks, percentiles or marks. Never say "in every paper", "in your shift" or "each
   paper" unless `appears_in_every_paper_2019_2026` is true; never say "every year since 2019" unless
   `appears_every_year_2019_2026` is true. Say instead "it appeared in N of the M papers" with the two numbers.
9. **Trends only from the `trend` field.** Say a chapter grew, rose, fell or declined only when `trend` says `up` or
   `down` for the periods you are comparing; when it says `about the same`, say it has stayed about the same. Never infer
   a trend from two numbers yourself. (The checker rejects "grown", "risen", "fallen", "declined" and similar words that
   do not match.)
4. **Original writing only.** Describe question types in your own words from the question texts in
   `question_candidates` and the topic names. Never copy text from coaching sites, books, ExamSide, ExamGOAL or any other
   site, and never name them. No other brand names, no AI tools.
5. **Format.** Exactly these six `##` sections, in this order, with these exact titles:
   `How often it comes up`, `Most-asked topics`, `What the questions look like`, `Questions to try first`,
   `How to practise it`, `Frequently asked questions`. Paragraphs, `- ` lists and `**bold**` only. `###` only for FAQ
   questions (3 to 5, each ending in `?`, each followed by one answer paragraph). No HTML, no tables, no images, no maths
   markup (`$`); write maths in words or Unicode (ω, ², √, π).
6. **Links.** In "Questions to try first", link 3 to 6 questions, only from `question_candidates`, as
   `[short description in your words](/q/<id>)` followed by the paper in brackets, as in the examples. Prefer one per
   topic and NTA papers. You may also link other chapter pages (`/jee/pyq/<subject>/<slug>`) when a chapter depends on
   another. No outside links and no Play Store link (the page already has the app button).
7. **Length.** 550 to 1,000 words (300 to 1,000 for a chapter that is no longer in the syllabus).
8. **Style.** Plain, friendly, exact English for a Class 11 or 12 student in India. Short sentences. No em dashes, no
   exclamation marks, no filler ("In this guide we will..."), no hype. Mention the app once only, in the last FAQ answer,
   exactly as the examples do ("Step-by-step solutions for each one are in the EdLoop app.").

## Chapters that are no longer in the syllabus

When `in_current_syllabus` is `false` (12 chapters), say so in the first paragraph: "NTA removed it from the JEE Main
syllabus in <removed_from_syllabus_in>", or, if that field is null, "It is no longer in the JEE Main syllabus." Give the
historical numbers (`all_years`, `by_year`), say when it was last asked, and in "How to practise it" say plainly that
students preparing for JEE Main 2027 can skip it unless their board or another exam needs it. The FAQ must include
"Is <chapter> in the JEE Main 2027 syllabus?".

## Using the facts file

- `window_2019_2026`: the main numbers (NTA's online exam era). `window_2002_2018`: the AIEEE and early JEE Main years, for
  comparison. `window_2024_2026`: the last three exam years.
- `rank_in_subject_2019_2026`: "Nth of M <subject> chapters by share of questions".
- `topics_most_asked_first`: topic counts; use `questions_2019_2026` for the list, `questions` for the whole archive.
- `trend`: `up`, `down` or `about the same` for the share of the subject, 2002–2018 vs 2024–2026 and 2019–2026 vs 2024–2026.
- `appears_in_every_paper_2019_2026`, `appears_every_year_2019_2026`: the only basis for "every paper" or "every year" wording.
- `numerical_answer_questions_2019_2026`: questions with no options (numerical answer type).
- `years_not_asked_since_2019`: years with no question from the chapter.
- `by_year`: per-year counts; use for "the busiest year was ..." (pick the year with the most `questions` yourself only by
  reading the values, and state that year's `questions` and `papers_in_our_set` as they are).
- `question_candidates`: the only questions you may link; `text` is a short description of each.
- `class_level`, `nta_syllabus_unit`: for the "Class 11 / Class 12, NTA's Unit N" sentence.

## Git

Work on the branch `feature/chapter-guides` in this folder. Commit only files under `guides/jee/` (and `guides/VERIFY.md`
in the second step). Do not edit anything else: not `tools/`, not `guides/facts/`, not the generated pages (`jee/`, `q/`,
sitemaps), not the examples. Do not run `tools/make_question_pages.py` (it rewrites 17,000 files). Never push to `main`;
pushing `feature/chapter-guides` is fine. Commit message per batch: `Chapter guides: <subject> <first>–<last> (<n> guides)`.

## Second step: the number check (run with a different model after all 87 are written)

Go through every guide in `guides/jee/` except the two examples. For each sentence that contains a number, check against
the facts file that the number exists **and** is used for the right thing (rule 1). Fix any mismatch in the guide, rerun
`python tools/check_guides.py`, and write `guides/VERIFY.md`: one row per guide with `chapter | numbers checked | fixed |
notes`. Then run `python tools/check_guides.py` on everything; the last line must say `89 checked, 0 failed`.

## Done means

- 89 guides under `guides/jee/` (87 new + 2 examples), `python tools/check_guides.py` → `89 checked, 0 failed`.
- `guides/VERIFY.md` filled in.
- Commits on `feature/chapter-guides`, pushed. Reply with the commit list, the checker's last line, and any chapter where
  you were unsure.

The EdLoop main session reviews a sample, regenerates the pages and publishes them only on the founder's word.

## Rewrite round (2026-11-20): read this first

The first run generated guides with a Python template. That is not allowed and none of it will be published: about half of
the sentences were the same in 10+ guides, question notes were pasted as they are, and words were swapped to get past the
checker ("resonance" → "delocalisation", |x| → "mod(x)"), which changed the meaning.

10. **Write every guide yourself, one at a time.** No scripts, templates or generators that produce guide text. The
    checker now fails any sentence that appears in 4 or more guides, and any `question_candidates` text copied as it is.
    Do not reuse sentences from the two examples either; they are a model for tone and structure, not text to copy.
11. **Never change the science to pass the checker.** Write "air", "resonance" and |x| normally; the checker no longer
    flags them. If the checker rejects a correct word, stop and report it instead of rewording it.
12. Each chapter must read as written for that chapter: name its real ideas (laws, reactions, theorems, standard
    set-ups) in "What the questions look like" and "How to practise it", in sentences no other guide uses.

Rewrite all 87 guides (keep the two examples), one at a time, checker after each, commit every ~10 as before.
