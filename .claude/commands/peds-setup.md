---
description: One-time setup for the pediatrics track. Plans the pediatric board questions (written 2 at a time) and builds the blind-review tooling.
argument-hint: [optional, e.g. "24 questions"]
---

Set up the pediatrics track for Boards. This session plans and builds tooling only; it writes no questions.
Plan 40 questions (5 blocks of 8, written as 20 pairs) unless these arguments say otherwise: $ARGUMENTS

Read first: CLAUDE.md; all of docs/board_question_generator_spec.md; docs/CHEM_PHYS_250.md (the model for an approved
plan); tools/review_packet.py; questions/questions3.py and build.py (the format and wiring to copy); and
.claude/commands/peds-pair.md and .claude/commands/peds-blind.md (the per-pair loop this setup must support).

1. Target. Step 2 CK level and format (spec §1–§6), patients from birth to 18 years. Weight the content by NBME's
   published Pediatrics Subject Exam content outline (https://www.nbme.org/subject-exams/clinical-science/pediatrics:
   systems, physician tasks, site of care) and check the current Step 2 CK content outline on usmle.org. Use only
   official published weightings, never "high-yield" or recalled-exam lists.

2. Calibrate. Read the free official sample items (the Step 2 CK samples on usmle.org; NBME's Pediatrics sample items
   if posted) for structure, length and difficulty only: never copy, paraphrase or adapt one (CLAUDE.md). Write
   calibration notes in your own words (vignette length, how labs and imaging appear, option length, lead-ins), and
   list the samples' clinical scenarios so that no pediatric item uses one.

3. Write docs/PEDS_BLUEPRINT.md, modeled on CHEM_PHYS_250.md:
   - Reserve the next free block numbers (Block 4 onward) and assign every ID now: pair 1 is B4-Q01 and B4-Q02, and
     so on. IDs become permanent once pushed.
   - One row per question: ID; pair; age band (neonate 0–28 days, infant 1–12 months, 1–5 years, 6–11 years,
     12–18 years); system (the NBME outline's wording); task (diagnosis, best test, management, mechanism); setting
     (office, ED, inpatient, nursery); topic; the decision tested; the detail that decides it; the tempting wrong
     answer; planned stars; the guideline to verify (name and year); status (planned → written → checked → reviewed →
     pushed). No answer letters: /peds-pair balances them as it writes.
   - Mix: systems, tasks and settings within the NBME ranges; age bands spread across the plan; about 25% ★★★, 50%
     ★★★★ and 25% ★★★★★ in every block (spec §3); the two questions in a pair differ in system and age band. Include
     normal age-related findings where the right answer is to reassure or watch, since the outline tests them. Keep
     Step 2 CK's weight on next steps; if you plan mechanism items, add their lead-in to spec §4.
   - Every decision point is important (common, or dangerous and treatable), keyed to a firm recommendation ("should"
     or "should not", strong or moderate; never an option, a weak recommendation, a "may" or a "consider"), and
     settled: current US authorities agree on it.
   - Exclude what they disagree on. Immunizations above all: in January 2026 the CDC moved immunizations for seven
     diseases off its routine childhood schedule, while the AAP's 2026 schedule kept them routine, and HPV dosing
     differs. Check where that stands today; test vaccines only on points both schedules share (contraindications,
     catch-up intervals, post-exposure prophylaxis), and cite both.
   - List the topics whose guidance changed recently and what changed, so items key to the current version (for
     example the 2025 AHA/AAP pediatric and neonatal resuscitation guidelines, the AAP 2022 hyperbilirubinemia
     guideline and the AAP 2021 febrile infant guideline). Verify each by web search.
   - Repeat no decision point already in spec §9 (B1-Q04 malrotation, B2-Q04 septic hip, B2-Q07 confidential STI care
     for a minor).
   - Add a reserve list of 10 alternates with the same columns, a "How the plan is used" section (the /peds-pair →
     /peds-blind loop, file names, status rules) and a changelog.

4. Build tools/board_review_packet.py, modeled on tools/review_packet.py:
       python tools/board_review_packet.py questions/questionsN.py B4-Q01,B4-Q02 review/peds_pair_01.md [--blind]
   The key packet shows everything (stars, system, discipline, topic, vignette, labs as a table, stem, options,
   answer, explanations with error types, objective, sources, verified_on, status) with an answer summary and letter
   counts. The blind packet shows, per question, only the ID, vignette, labs, any interval text, stem and options,
   with blank Answer / Confidence / Objection lines, under the solving instructions from peds-blind.md; never a topic,
   system, discipline, difficulty, explanation or source. Convert the markup (<b>, <super>, HTML entities) to readable
   text. Test it on B3-Q01 and B3-Q02 into a scratch folder, read the blind output, then delete the scratch files.

5. Wire it in, without touching app code or saved progress:
   - Spec §7: the pediatrics track holds the reserved blocks (point to the blueprint), and the general gap list moves
     to the first block after them. Add a §11 changelog line.
   - .claude/commands/new-board-block.md, step 1: skip blocks reserved in docs/PEDS_BLUEPRINT.md.
   - CLAUDE.md: the blueprint under "Docs to read", the pediatrics track under Track C, and a note that pediatric
     questions use the SYS label "Pediatrics" (one Systems chip and one Questions heading in the app).
   - docs/PROMPTS.md: how to run the loop (new conversation, /peds-pair; new conversation, /peds-blind; my OK to push).

6. Run python build.py and the three tests; the app should not change. Show me the plan (the table, the mix against
   the NBME ranges, the changed-guidance list and the exclusions) and wait for my OK. Then commit the blueprint, the
   tool, the doc changes and .claude/commands/peds-*.md, and push.
