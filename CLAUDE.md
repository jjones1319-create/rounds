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
- 3D (not inlined; served as separate files, loaded only when the Body tab's "3D" is chosen):
  `js/body3d.js` viewer (ES module) · `vendor/three/` three.js 0.186.1, mapped by the import map in `src/shell.html`
  · `models/*.glb` one file per layer (skeleton, organs, muscles, arteries, veins, nerves, lymph), each loaded the first
  time its layer chip is switched on · `data/mesh_map.json` (per layer: model file, card key → Z-Anatomy mesh names).
  Rebuild models with `py tools/build_models.py [layer]` (needs Blender + glTF-Transform under `work/`; see its docstring).
  What each layer takes, and what is never exported for licensing reasons, is in `tools/export_layers.py`.
- `build.py` stamps `js/body3d.js`, the mesh map and each model with a content hash (`ASSET_V` in `index.html`); the page
  loads `js/body3d.js?v=<hash>` so phones never mix a new page with old cached 3D files. **Rebuild after changing any
  of them** (`tests/three_d.py` fails if the stamps are stale). Bump `API` in `js/body3d.js` and `API3D` in
  `src/anat.js` together when their contract changes; a mismatch shows a Reload prompt.
- The Body tab's layer chips drive both views (`Body.layers`); 3D has no dermatome layer and is a male model.
  Cards with no 3D match (female organs, rectum, brain, phrenic/RLN/inferior gluteal nerves, lymph ducts, orbit)
  fall back to the Diagram.
- Tests (need `pip install -r tests/requirements.txt` and `python -m playwright install chromium`):
  `python tests/smoke.py`, `python tests/overflow.py`, and `python tests/three_d.py` (serves the repo over http,
  since 3D can't load from file://; `--timing` emulates phones on 4G). Run all three after every change, before every push.
- `?perf` on the URL shows the 3D download size, load time and fps on the device.

## Non-negotiables
- **Accuracy first.** Every question and anatomy fact must be verifiable. Follow `docs/board_question_generator_spec.md`
  §2 exactly when writing questions: verify each answer against a current named guideline with a web search,
  cite it, record it in the spec's question log (§9) and changelog (§11). If unsure, flag it; never guess.
- **Original content only.** Never copy UWorld/AMBOSS/NBME questions or Wikipedia text into cards.
- **Question IDs are permanent** (`B1-Q01`…). Saved progress is keyed by ID. Never renumber; add new blocks
  as `questions/questionsN.py`, import them in `build.py`, and add each ID to `SYS` in `build.py`.
- **Phone first.** Her phone is a **Samsung Galaxy S25 Ultra** (Chrome viewport about 412 × 891 CSS px at 3.5×;
  Snapdragon 8 Elite, Adreno 830 GPU, 120 Hz screen): design for it and measure 3D on it (`tests/three_d.py` emulates it).
  Still test at 360 and 390 px too (412 is also checked); no horizontal overflow (`tests/overflow.py` must pass).
  Keep light/dark theme tokens, safe-area insets, `prefers-reduced-motion`, and keyboard support working.
- **Licensing.** 3D models come from share-alike sources. Read `docs/PLAN_3D.md` §Licensing before adding any
  model file, and keep `CREDITS.md` accurate.

## Storage notes
- Progress lives in `localStorage` key `rounds.progress.v1` (answers, flags, notes, sessions, settings).
- `Sync` in `app.js` uses `window.claude` (claude.ai only). Off claude.ai it is a no-op; leave it, it's harmless.
- Moving to GitHub Pages changes the site origin, so progress from the claude.ai version does not carry over.

## Current state (2026-10-09)
- 16 questions (Blocks 1–2). Anatomy: 2D body (front/back, 8 layers incl. dermatomes), brain, heart, 254-entry index.
- Live at https://jjones1319-create.github.io/rounds/ (Phase 0 done).
- Phase 1 done: 3D skeleton behind a "3D | Diagram" switch (Diagram stays the default); on her phone: 0.7 s, 56 fps.
- Phase 2 built: all seven 3D layers (7.8 MB gzipped in total, loaded per layer); 156 of 168 body cards open from a
  tap; search, Index, Bones and "Name that structure" work in 3D. 3D renders at up to 3x and steps down if fps drops.
  Gaps: 708 structures (1,242 of 1,863 meshes) show a name-only card; write verified cards for the important ones.
- The live claude.ai version is the reference: behavior there should keep working here.

## Next work, in order
See `docs/PLAN_3D.md` for details and acceptance criteria.
0. Repo + GitHub Pages setup; confirm the current app works on her phone.
1. ~~3D feasibility test~~ (done 2026-10-09).
2. ~~Organs, vessels, nerves, muscles, lymphatics as lazy-loaded layers~~ (built 2026-10-09; confirm on her phone).
3. Progress export/import + installable PWA (manifest, icons, offline cache).
4. Block 3 questions per the spec (coverage gaps are listed in spec §7).
