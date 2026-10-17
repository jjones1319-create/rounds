# Prompts for the owner

Copy one into Claude Code. Each assumes `CLAUDE.md` and the docs it names are current. Claude pauses for your OK
wherever a prompt says so; it never pushes without it.

**Set up the MCAT foundations:**
> Read docs/PLAN_MCAT.md, docs/MCAT_SPEC.md, docs/MCAT_GUIDES_SPEC.md, and docs/PUBLIC_RELEASE.md and do Phase M0
> only. Boards must keep working exactly as now, including saved progress. Run the tests, show me the result, and
> wait for my OK before pushing.

**Build the section guides (after M0):**
> Do PLAN_MCAT Phase M1, starting with the Chem/Phys guide only. Follow docs/MCAT_GUIDES_SPEC.md exactly.
> Download AAMC's official outline into work/ (never commit it) and build a private completeness checklist
> from it. Write every description in your own words and verify each fact and equation by web search.
> Show me the finished topic list for review before writing the other three guides.

**Write MCAT starter questions (after the guides):**
> Do PLAN_MCAT Phase M2. Follow docs/MCAT_SPEC.md exactly and tag every item to guide topics. First show me the
> 24 planned topics with section, content category, skill, difficulty, answer letter, and the source you'll verify
> against; wait for my OK. Verify every fact by web search and re-derive every numeric answer independently.
> Mark everything draft for my review. Run validate.py and the tests, then wait for my OK before pushing.

**Review session (owner):**
> Show me every MCAT item with status "draft" in [section], one at a time: passage, question, choices, answer,
> and worked solution. After each, wait for me to approve, request a change, or reject. On approval, set status
> to "reviewed" and reviewed_by to "[your initials]".

**Write a new board block:**
> /new-board-block
>
> (Optionally add topic preferences after it, e.g. `/new-board-block patient safety and oncology emergencies`. Blocks 4–8 are
> reserved for the pediatrics track, so the next general block is Block 9.)

**Pediatrics track (two questions at a time; `docs/PEDS_BLUEPRINT.md`):**
1. Once, to plan the track and build the tooling (already done 2026-10-16): `/peds-setup`.
2. In a **new conversation**: `/peds-pair` — writes the next planned pair, verifies every decision by web search, runs the
   check script, build and tests, and writes the key and blind packets. It does not commit. (Add a note after it to redo one
   question, e.g. `/peds-pair redo B4-Q02 with a reserve topic`.)
3. In **another new conversation** (one that has not seen the pair): `/peds-blind` — re-solves the blind packet, then
   compares with the key, fixes or passes, and shows you the pair. It waits for your OK before committing and pushing.
   If a question failed, it says so; start a new conversation and run `/peds-blind` again.
4. Repeat 2–3 for each of the 20 pairs. Claude never pushes without your OK.
