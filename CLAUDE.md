# Rounds — board prep app (project memory for Claude Code)

## What this is
A mobile-first study app for one medical student preparing for USMLE Step 2 CK, used on an Android phone.
Two halves: **Practice** (original board-style questions with explanations, tutor/timed blocks, stats) and
**Anatomy** (interactive body, brain, and heart models, an A–Z index, quizzes).
It was built in a claude.ai chat and is moving to GitHub Pages so the anatomy can use real 3D models.
The person you're working with is not necessarily a developer: explain steps plainly and ask before
anything public or irreversible (creating the repo, first push, making it public, deleting files).

## How it's built
- `python build.py` → writes `index.html` (a single self-contained file) from `src/` + `questions/`.
- GitHub Pages serves the repo root (`main` branch, `/`). `.nojekyll` must stay.
- `src/shell.html` HTML + all CSS · `src/app.js` app shell, practice engine, storage, settings
- `src/figure.js` 2D body figure (front/back SVG) · `src/content.js` structure cards, cranial nerves, bones, lab values
- `src/models.js` dermatomes, brain + heart models, `buildDictionary()` · `src/anat.js` anatomy UI module (`Anat`)
- `questions/questions.py` (Block 1), `questions/questions2.py` (Block 2): question source of truth.
- Tests (need `pip install -r tests/requirements.txt` and `python -m playwright install chromium`):
  `python tests/smoke.py` and `python tests/overflow.py`. Run both after every change, before every push.

## Non-negotiables
- **Accuracy first.** Every question and anatomy fact must be verifiable. Follow `docs/board_question_generator_spec.md`
  §2 exactly when writing questions: verify each answer against a current named guideline with a web search,
  cite it, record it in the spec's question log (§9) and changelog (§11). If unsure, flag it; never guess.
- **Original content only.** Never copy UWorld/AMBOSS/NBME questions or Wikipedia text into cards.
- **Question IDs are permanent** (`B1-Q01`…). Saved progress is keyed by ID. Never renumber; add new blocks
  as `questions/questionsN.py`, import them in `build.py`, and add each ID to `SYS` in `build.py`.
- **Phone first.** Test at 360 px and 390 px wide; no horizontal overflow (`tests/overflow.py` must pass).
  Keep light/dark theme tokens, safe-area insets, `prefers-reduced-motion`, and keyboard support working.
- **Licensing.** 3D models come from share-alike sources. Read `docs/PLAN_3D.md` §Licensing before adding any
  model file, and keep `CREDITS.md` accurate.

## Storage notes
- Progress lives in `localStorage` key `rounds.progress.v1` (answers, flags, notes, sessions, settings).
- `Sync` in `app.js` uses `window.claude` (claude.ai only). Off claude.ai it is a no-op; leave it, it's harmless.
- Moving to GitHub Pages changes the site origin, so progress from the claude.ai version does not carry over.

## Current state (2026-10-05)
- 16 questions (Blocks 1–2). Anatomy: 2D body (front/back, 8 layers incl. dermatomes), brain, heart, 254-entry index.
- The live claude.ai version is the reference: behavior there should keep working here.

## Next work, in order
See `docs/PLAN_3D.md` for details and acceptance criteria.
0. Repo + GitHub Pages setup; confirm the current app works on her phone.
1. 3D feasibility test: simplified real skeleton, rotate/zoom/tap, measure size and phone performance. Report back before continuing.
2. Add organs, vessels, nerves, muscles as lazy-loaded layers; map meshes to existing cards and the index.
3. Progress export/import + installable PWA (manifest, icons, offline cache).
4. Block 3 questions per the spec (coverage gaps are listed in spec §7).
