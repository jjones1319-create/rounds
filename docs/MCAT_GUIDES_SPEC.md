# MCAT Section Guides — Spec

**Version:** 1.1 · **Created:** 2026-10-10 · **Updated:** 2026-10-10

Each MCAT section in the app gets a **"What's tested"** guide: a readable, searchable map of everything the
section covers, so learners can see the whole territory, track what they've reviewed, and jump straight to
practice on any topic. Guides are built before the question bank grows, because every question is tagged to a
guide topic.

Read with `docs/MCAT_SPEC.md` (exam facts, blueprint) and `docs/PLAN_MCAT.md` (phases).

---

## 1. Source and copyright rules (read first)

- **The authority is AAMC's *What's on the MCAT Exam?* content outline** (free on students-residents.aamc.org,
  web pages and PDF). Completeness is measured against it: every topic it lists must appear in our guide.
- **The outline is AAMC's copyrighted work.** Do not reproduce it. Write every description in our own words.
  It is fine to use AAMC's framework as identifiers: section names, foundational concept numbers, content
  category codes and short names (e.g., "4B Fluids and gas exchange"), and the names of the four Scientific
  Inquiry and Reasoning Skills, credited to AAMC.
- For checking completeness, Claude Code may save a copy of the outline in `work/` (gitignored, never committed
  or published) and generate a private checklist from it.
- **Every guide page links to the official outline** and to AAMC's free official prep resources, with the
  statement: "Organized according to the AAMC's *What's on the MCAT Exam?* outline. Descriptions are our own.
  See the official outline for the authoritative list."
- **Never include recalled exam content.** No "this was on the exam," no claims about what a particular exam
  tested, no topic frequency claims beyond AAMC's published weightings. Apply the same rule to anything
  contributed by the public (see `docs/PUBLIC_RELEASE.md`). Examinees agree not to disclose exam content beyond
  the public outline, so contributions that do so must be rejected.
- Facts in topic summaries follow MCAT_SPEC §3: verified against a named source, original wording, cited.

## 2. What each guide contains

**A. At a glance:** questions, time, passage vs. discrete counts, tools (periodic table or none), calculator
policy (none), math expected, what the section measures in two sentences, and a note that practice scores are
not scaled scores.

**B. Blueprint:** AAMC weightings as simple bars: disciplines, foundational concepts, skills (from MCAT_SPEC §2).

**C. Content map (science sections):**
Foundational concept → content category → topics. For each topic:
- Name and discipline tags (BIO, BC, GC, OC, PHY, PSY, SOC).
- "What to know": 1–4 sentences in our own words, plus key equations or relationships where relevant
  (rendered with KaTeX; units included).
- "Common confusions": optional, one or two lines.
- Links: "Practice this topic" (filters to tagged questions; hidden if none yet) and free references
  (OpenStax chapter, AAMC Official Prep Hub course, Khan Academy MCAT), as links only; never their content.
- Learner controls: "Reviewed" checkbox and the learner's accuracy on that topic's questions.

**D. Skills:** the four Scientific Inquiry and Reasoning Skills, each explained in our words with a short
original example of what such a question asks (not a full question).

**E. Research methods and statistics** (all three science sections; heaviest in Psych/Soc): study designs,
variables, controls, validity and reliability, sampling and bias, correlation vs. causation, descriptive
statistics, reading graphs and tables, significance and error bars, and research ethics, at the level the
MCAT expects. Verify each definition.

**F. Math toolkit** (Chem/Phys and Bio/Biochem): no-calculator techniques the outline expects: scientific
notation, exponents and logarithms (including pH and decibels), unit conversion, proportional reasoning,
estimation, vectors, and solving simultaneous equations. Short worked examples, all original.

**G. CARS guide** (CARS has no content outline): passage types (humanities 50%, social sciences 50%), the three
skill areas (Foundations of Comprehension, Reasoning Within the Text, Reasoning Beyond the Text) explained with
what each kind of question asks, the most common wrong-answer patterns, and reading approaches presented as
options rather than rules. No outside knowledge needed: say so clearly.

## 3. Topic IDs and tagging

- Every topic has a permanent ID: `<category>.<slug>`, e.g. `4B.bernoulli`, `1A.enzyme-kinetics`,
  `7A.operant-conditioning`. Never renumber; deprecate instead.
- Every MCAT question lists one or more topic IDs in `topics` (see MCAT_SPEC §8).
  `tools/validate.py` fails if a question references an unknown topic.
- The validator also produces a **coverage report**: topics with zero questions, questions per category versus
  AAMC weightings. This guides which questions to write next.

## 4. Data format (`content/mcat/guides/<section>.json`)

```json
{
  "section": "chem_phys",
  "verified": "2026-10-10",
  "official_outline_url": "https://students-residents.aamc.org/prepare-mcat-exam/whats-mcat-exam-pdf-outline",
  "glance": { "questions": 59, "minutes": 95, "passage_questions": 44, "discrete_questions": 15,
              "tools": "Periodic table", "calculator": false, "summary": "" },
  "blueprint": { "disciplines": {}, "concepts": {}, "skills": {} },
  "concepts": [
    { "id": "4", "name": "", "summary": "",
      "categories": [
        { "id": "4B", "name": "", "summary": "",
          "topics": [
            { "id": "4B.bernoulli", "name": "Bernoulli's equation", "tags": ["PHY"],
              "know": [""], "equations": ["P_1 + \\tfrac12\\rho v_1^2 + \\rho g h_1 = P_2 + \\tfrac12\\rho v_2^2 + \\rho g h_2"],
              "confusions": [""], "refs": [{ "label": "OpenStax College Physics 2e, 12.2", "url": "" }],
              "status": "draft", "reviewed_by": null }
          ] }
      ] }
  ],
  "skills": [], "research_methods": [], "math_toolkit": []
}
```

CARS uses `passage_types`, `skill_areas`, `wrong_answer_patterns`, and `approaches` instead of `concepts`.

Fields added when the first guide was built (2026-10-10), all checked by `tools/validate.py`:
- `official_prep_url`: AAMC's free prep resources page. `attribution`: the statement from §1, shown at the top of the guide.
- `glance.math` (what math is expected) and `glance.scores_note` (practice scores are not scaled scores); the exam
  facts in `glance` and the weightings in `blueprint` must equal the numbers in MCAT_SPEC §1–2.
- Concepts and categories carry `name` and `summary` (AAMC's framework names as identifiers; summaries our own).
- `skills`: four entries `{id, name, pct, what, example}` in order 1–4. `research_methods`: `[{name, know[]}]`.
  `math_toolkit`: `[{name, know[], equations[], example}]`. Equations are LaTeX strings rendered with KaTeX
  (HTML + MathML output) in a box that scrolls horizontally.
- Topic `status`/`reviewed_by` are kept for the review workflow (§6); nothing is shown in the app for `draft`.

App storage: "Reviewed" ticks live in the MCAT progress record (`rounds.mcat.v1`, field `reviewed: {topicId: timestamp}`),
created only when the first tick is made. Which groups are expanded is remembered under `rounds.guide.v1`.

## 5. App behavior

- Each MCAT section screen has two tabs: **Practice** and **What's tested**.
- The guide is searchable across all sections (topic names, summaries, equations as text).
- Expand/collapse by concept and category; remember what was open.
- Progress per category: topics reviewed (checkboxes) and accuracy on tagged questions.
- "Practice this topic" starts a tutor block from that topic's questions.
- Readable on a 360 px phone; equations scroll horizontally inside their own box if wide.
- Show "Last verified" and the official-outline link at the top of every guide.

## 6. Review

Same workflow as questions: `status` and `reviewed_by` per topic. The owner (degrees in biology, chemistry,
mathematics, and physics, with PhD colleagues in each field) reviews every topic, including the math toolkit, and
marks it reviewed; no second reviewer is required. A "Beta" label on unreviewed topics is optional and off by
default.

## 7. Self-audit before delivering a guide

- [ ] Completeness: every topic in the AAMC outline for this section appears (checked against the private copy in `work/`)
- [ ] All descriptions original; no copied sentences from AAMC, textbooks, or prep companies
- [ ] Every fact and equation verified against a named source; units and symbols defined
- [ ] No recalled exam content and no frequency claims beyond AAMC weightings
- [ ] Topic IDs unique and stable; validator passes; coverage report generated
- [ ] Official-outline link, attribution statement, and "Last verified" date present

## 8. Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-10 | Spec created. |
| 1.1 | 2026-10-10 | Owner decisions applied: §6 makes the owner the reviewer of all topics, drops the second-reviewer requirement, and makes the Beta label optional and off by default; §2.C clarifies references are links only. |
| 1.2 | 2026-10-10 | Chem/Phys guide built (96 topics, 4A–5E, all `draft`): §4 documents the front-matter fields, the equation rendering, and where Reviewed ticks and expand state are stored. |
| 1.3 | 2026-10-11 | Bio/Biochem (62 topics), Psych/Soc (61) and CARS guides built. CARS fields: `glance` (tools null), `blueprint.cars_skills` and `blueprint.passage_content`, `no_outside_knowledge`, `passage_types[{name, pct, disciplines, what}]`, `skill_areas[{id, name, pct, what, asks[], example}]`, `wrong_answer_patterns[{name, what, spot}]`, `approaches[{name, what}]`; CARS has no topics, so no Reviewed ticks. |
