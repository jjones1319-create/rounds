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
> (Optionally add topic preferences after it, e.g. `/new-board-block pediatrics and patient safety`.)
