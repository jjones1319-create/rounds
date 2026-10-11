# Plan: MCAT section for Rounds

Goal: add an MCAT practice section alongside board prep, as the start of a free study guide for both exams.
(The site is public only because GitHub Pages requires it; it is not promoted.) Begin simple (a few items per
section), but build the foundations correctly now so the content can grow to thousands of items without rework.

Read with: `docs/MCAT_SPEC.md` (question rules), `docs/MCAT_GUIDES_SPEC.md` (section guides),
`docs/PUBLIC_RELEASE.md` (public launch checklist).

---

## What's different from the boards section (why this is more than "another tab")

1. **Passages.** Most MCAT questions come in sets of 4–7 that share a passage. The current runner shows one
   self-contained vignette per question. A passage-aware runner is the biggest piece of work.
2. **Four choices** (A–D), not five.
3. **Figures, equations, and chemical structures** appear constantly in the science sections.
4. **Tools differ:** a periodic table in the science sections, nothing in CARS, no calculator, no lab values.
5. **Scores can't be imitated.** The 118–132 scale comes from AAMC equating. Show percent correct and
   breakdowns, never a predicted scaled score.
6. **Scale.** One self-contained `index.html` with every question inlined will get too big. Content must move
   into separate data files loaded when needed.

## Architecture changes

**Exam switcher.** A persistent choice at the top of Home, Practice, and Progress: "Boards" or "MCAT".
Anatomy is shared. Remember the last choice. Practice, stats, history, and key points are scoped to the
selected exam.

**Content files.** New structure:
```
content/boards/   block files (migrate from questions/*.py later; not required now)
content/mcat/     M1.json, M2.json, ... (schema in MCAT_SPEC §8)
content/mcat/guides/  chem_phys.json, cars.json, bio_biochem.json, psych_soc.json (MCAT_GUIDES_SPEC §4)
data/             build output: one JSON per exam (and later per section), fetched at runtime
tools/validate.py checks every block against the schema and the spec's structural rules
```
`build.py` reads `content/`, runs validation, and writes `data/*.json` plus `index.html`. The app fetches the
data file for the selected exam. Keep boards working exactly as now during the change.

**Validation** (`tools/validate.py`, runs in `build.py`; build fails on any error):
unique permanent IDs for items, passages, and guide topics; every item's topic IDs exist in a guide; exactly four options for MCAT; answer key present; every wrong choice explained and
typed; required tags present and valid (section, discipline, FC/category or CARS skill, Skill, difficulty);
passage references exist; figure data present with alt text; letter balance per block reported.
It also writes a coverage report (topics with no questions, questions per category versus AAMC weightings).

**Tests must serve over HTTP.** Once data is fetched, `file://` URLs stop working in browsers. Update
`tests/smoke.py` and `tests/overflow.py` to start a local server (`python -m http.server`) and test against it.

**Progress storage.** Keep the existing boards key `rounds.progress.v1` untouched (her progress lives there).
Store MCAT progress under `rounds.mcat.v1`. Export/import (planned in PLAN_3D Phase 3) must include both.

**Passage runner.**
- Phone: passage on top with a sticky "Passage / Question" toggle so she can flip without losing her place;
  the question stays visible while scrolling the passage via the toggle.
- Wide screens: passage left, question right, scrolling independently.
- Highlighting in passages (tap-drag to highlight, tap to clear) and the existing strike-out for choices,
  both saved with the session. The real exam provides both tools.
- Navigation and the question grid treat each passage's questions as a group.

**Section screens.** Each MCAT section has two tabs: **Practice** and **What's tested** (the section guide,
per MCAT_GUIDES_SPEC §5), with search across all guides, "Reviewed" checkboxes per topic stored in
`rounds.mcat.v1`, and "Practice this topic" buttons.

**Tools.** Periodic table sheet for science sections (atomic number, symbol, atomic mass per IUPAC, rounded
as on the AAMC table; verify every value). No tools in CARS. No calculator anywhere.

**Rendering.**
- Equations: KaTeX, vendored locally (MIT license; confirm before adding), with MathML output for screen readers.
- Chemical structures: generate SVGs at build time from SMILES with RDKit (BSD license; confirm), stored in
  `data/structures/`. No runtime chemistry library needed, and structures are drawn correctly every time.
- Graphs and tables: a small SVG chart renderer that draws from the item's stored data.

**Timed mode.** Full-section timing (95 min/59 or 90 min/53) and proportional timing for shorter custom blocks
(about 1.6 minutes per science question, 1.7 per CARS question, rounded up per passage).

**Stats.** Percent correct overall and by section, content category, Scientific Inquiry and Reasoning Skill,
and CARS skill; time per question. Clearly state that scores are not MCAT scaled scores.

## Phases and acceptance criteria

### Phase M0: foundations (no MCAT content yet) — done 2026-10-10
Exam switcher, content/data split, validator, HTTP-based tests, MCAT progress key.
- Pass: boards section works exactly as before, including her saved progress; tests pass over HTTP;
  the MCAT tab shows an empty state for each of the four sections.

### Phase M1: section guides ("What's tested") — in progress
Build the four guides per `docs/MCAT_GUIDES_SPEC.md`, starting with Chem/Phys so the owner can review the
physics topics first. Questions depend on these topic IDs, so guides come before the question bank grows.
Status 2026-10-10: the app side is done (section screens with Practice | What's tested, search across guides,
expand/collapse memory, Reviewed ticks, KaTeX equations) and the Chem/Phys guide is written (96 topics, every
outline item mapped in the private checklist in `work/`, references checked, all topics `draft`). CARS,
Bio/Biochem, and Psych/Soc guides follow once the owner has reviewed the Chem/Phys topic list.
- Pass: each guide is complete against the AAMC outline (private checklist in `work/`), uses original wording,
  shows the official-outline link and "Last verified" date, is searchable, and reads well at 360 px;
  topics carry `status` and `reviewed_by` (the optional Beta label stays off by default).

### Phase M2: discrete questions (starter content)
8 discrete questions each for Chem/Phys, Bio/Biochem, and Psych/Soc (24 total), ★★–★★★, per MCAT_SPEC.
Every item is marked `draft` until the owner reviews it.
- Pass: validator passes; every item is tagged to guide topics and "Practice this topic" works; items run in
  tutor and timed modes; stats split by section and category; periodic table in science sections only.

### Phase M3: passages
Passage runner (phone and wide layouts), highlighting, KaTeX, build-time structures, SVG charts.
Content: one science passage (4–6 questions) for each science section, and two CARS passages
(5–7 questions each: one humanities, one social sciences).
- Pass: the "Passage / Question" toggle works one-handed on a 360 px phone; figures match their data;
  overflow test passes on every new screen.

### Phase M4: review workflow and corrections
In-app support for the owner's review sessions (filter items by `status`, mark `reviewed` with `reviewed_by`) and
a corrections log (`rev` increments recorded in the spec changelog; showing recent corrections in the app is
optional). Optional, off by default, and only if the site is ever promoted: a "Beta" label on unreviewed items and
a per-item "Report a problem" link (see PUBLIC_RELEASE §3).
- Pass: every item's `status` and `reviewed_by` can be set from the review session and survive a rebuild;
  a corrected item keeps its ID and shows its new `rev`.

### Phase M5: growth
Blocks of passages and discretes toward the AAMC mix in MCAT_SPEC §2, prioritized by the validator's
coverage report (topics with no questions first).

## Owner's role
The owner holds degrees in biology, chemistry, mathematics, and physics, with PhD colleagues in each field, and
reviews all content: every item in every section, every guide topic, and the math toolkit. No second reviewer is
required. Present items for review in batches with the worked solution visible, and mark an item `reviewed` only
after the owner approves it. Ask before pushing, before migrating storage, and before deleting content.
