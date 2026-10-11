# Rounds — study app for Boards and MCAT (project memory for Claude Code)

## What this is
A mobile-first study app, built for one medical student on an Android phone, covering two exams: **Boards**
(USMLE Step 2 CK–style) and **MCAT**. Each exam has **Practice** (original questions with explanations,
tutor/timed blocks, stats). **Anatomy** (interactive 2D and 3D body, brain, and heart, an A–Z index, quizzes) is
shared. The long-term goal is a free study guide for both exams. The site is public only because GitHub Pages
requires it; it is not promoted or announced.
The owner you work with holds degrees in biology, chemistry, mathematics, and physics, with PhD colleagues in
each field, and is the reviewer of all content. They are not necessarily a developer: explain steps plainly and
ask before anything public or irreversible (pushing, deleting files, migrating storage).

## Docs to read before related work
- Board questions: `docs/board_question_generator_spec.md` · MCAT questions: `docs/MCAT_SPEC.md` (rules, blueprint, schema, review)
- MCAT section guides ("What's tested"): `docs/MCAT_GUIDES_SPEC.md` · MCAT features: `docs/PLAN_MCAT.md` (phases M0–M5)
- 3D anatomy: `docs/PLAN_3D.md` · Public-site rules: `docs/PUBLIC_RELEASE.md` · Owner's prompts: `docs/PROMPTS.md`

## How it's built
- `python build.py` → validates `content/` (MCAT) with `tools/validate.py` (any error stops the build), writes
  `data/boards.json` (from `questions/*.py`) and `data/mcat.json` (items, passages, guides, sections), then `index.html`
  from `src/`. The app fetches the two data files at boot (stamped with content hashes like the 3D files), so it
  needs HTTP, not file://. `QB`/`QMAP`/`SYSTEMS` in `app.js` always describe the selected exam's bank.
- GitHub Pages serves the repo root (`main` branch, `/`). `.nojekyll` must stay.
- `src/shell.html` HTML + all CSS · `src/app.js` app shell, practice engine, storage, settings
- `src/figure.js` 2D body figure (front/back SVG) · `src/content.js` structure cards, cranial nerves, bones, lab values
- `src/models.js` dermatomes, brain + heart models, `SCENE3D`, `buildDictionary()` · `src/anat.js` anatomy UI module (`Anat`)
- `questions/questions.py` (Block 1), `questions2.py` (Block 2), `questions3.py` (Block 3): board question source of truth.
- MCAT content: `content/mcat/guides/<section>.json` ("What's tested" guides, schema in `docs/MCAT_GUIDES_SPEC.md` §4)
  and `content/mcat/M*.json` (question blocks). Each MCAT section screen (Practice tab → a section) has Practice |
  What's tested; the guide is searchable across sections, remembers what is expanded, and renders equations with
  `vendor/katex/` (KaTeX 0.19.0, loaded the first time a guide opens; `ASSET_V.katex` stamps it).
- 3D (served as separate files, loaded only when a tab's "3D" is chosen; the choice is remembered per device):
  `js/body3d.js` viewers for the Body, Brain and Heart tabs (`viewer("body"|"brain"|"heart")`, ES module) ·
  `vendor/three/` three.js 0.186.1, mapped by the import map in `src/shell.html` · `models/*.glb` one file per layer
  (body: skeleton…lymph; brain_*: cortex, deep, arteries, nerves, skull; heart_*: wall, valves, coronary, veins, vessels),
  each loaded the first time its layer chip is switched on · `data/mesh_map.json` (per scene and layer: model file,
  card key → mesh names; brain/heart keys are Index ids br_*, cn_*, ht_*). The brain has a Left/Right hemisphere
  control, the heart a "Cut open" slider. Rebuild models with `py tools/build_models.py [layer]` (needs Blender +
  glTF-Transform under `work/`, and BodyParts3D under `work/bp3d/` for the heart; see its docstring). What each layer
  takes, and what is never exported for licensing reasons, is in `tools/export_layers.py`.
- `build.py` stamps `js/body3d.js`, the mesh map and each model with a content hash (`ASSET_V` in `index.html`); the page
  loads `js/body3d.js?v=<hash>` so phones never mix a new page with old cached 3D files. **Rebuild after changing any
  of them** (`tests/three_d.py` fails if the stamps are stale). Bump `API` in `js/body3d.js` and `API3D` in
  `src/anat.js` together when their contract changes; a mismatch shows a Reload prompt.
- The Body tab's layer chips drive both views (`Body.layers`); 3D has no dermatome layer and is a male model.
  Cards with no 3D match fall back to the Diagram.
- Tests (need `pip install -r tests/requirements.txt` and `python -m playwright install chromium`):
  `python tests/smoke.py`, `python tests/overflow.py`, and `python tests/three_d.py`; each serves the repo over HTTP
  via `tests/serve.py` (`three_d.py --timing` emulates phones on 4G). Run all three after every change, before every push.
  `smoke.py` seeds an old-style boards record and checks it is read and left byte-for-byte unchanged.
- `?perf` on the URL shows the 3D download size, load time and fps on the device.

## Non-negotiables
- **Accuracy first.** Every question, guide topic, and anatomy fact must be verifiable. Boards: follow
  `docs/board_question_generator_spec.md` §2 exactly (verify each answer against a current named guideline with a web
  search, cite it, log it in §9 and §11). MCAT: follow `docs/MCAT_SPEC.md` §3. If unsure, flag it; never guess.
- **Original content only.** Never take questions from any website, question bank, or prep source, for MCAT or
  boards (UWorld, AMBOSS, NBME, Kaplan, AAMC, Khan Academy, Blueprint, forums, or any other). Publicly available
  official sample questions may be read only to understand structure, style, and difficulty; never copy, paraphrase,
  or adapt their content. Never copy Wikipedia or textbook text into cards or guides. CARS passages are original or
  US public domain (published 1930 or earlier, with citation). Hypothetical experiments are labeled hypothetical.
- **No recalled exam content**, and no "frequently tested" claims beyond AAMC's published weightings.
- **Section guides** follow AAMC's outline structure but are written in our own words; never reproduce the outline,
  and keep any private copy used for checking in `work/` (gitignored).
- **MCAT items** have exactly four choices, are tagged per MCAT_SPEC §2 and §8, and pass `tools/validate.py`.
- **Never show or imply** a predicted MCAT scaled score (118–132) or a predicted board score.
- **Review.** Every item and guide topic carries `status` (`draft` → `reviewed`) and `reviewed_by`. The owner reviews
  all content; no second reviewer is required. A "Beta" label for unreviewed items is optional and off by default.
- **Question IDs are permanent** (`B1-Q01`…, `M1-Q01`…). Saved progress is keyed by ID. Never renumber; add board
  blocks as `questions/questionsN.py`, import them in `build.py`, and add each ID to `SYS` in `build.py`.
- **Phone first.** Her phone is a **Samsung Galaxy S25 Ultra** (Chrome viewport about 412 × 891 CSS px at 3.5×;
  Snapdragon 8 Elite, Adreno 830 GPU, 120 Hz screen): design for it and measure 3D on it (`tests/three_d.py` emulates it).
  Still test at 360 and 390 px too (412 is also checked); no horizontal overflow (`tests/overflow.py` must pass).
  Keep light/dark theme tokens, safe-area insets, `prefers-reduced-motion`, and keyboard support working.
- **Licensing, trademarks, disclaimers.** 3D models come from share-alike sources: read `docs/PLAN_3D.md` §Licensing
  before adding any model file and keep `CREDITS.md` accurate. Keep the disclaimer, trademark, and licensing rules in
  `docs/PUBLIC_RELEASE.md`; its report-a-problem and contribution items are optional, for later.
- **Storage.** Never change or migrate `rounds.progress.v1` (boards progress) without asking. MCAT progress uses
  `rounds.mcat.v1`.

## Storage notes
- Progress lives in `localStorage` key `rounds.progress.v1` (answers, flags, notes, sessions, settings).
- `Sync` in `app.js` uses `window.claude` (claude.ai only). Off claude.ai it is a no-op; leave it, it's harmless.
- The 3D/Diagram choice per tab is in `rounds.view3d` and the selected exam in `rounds.exam` (conveniences, not progress).
- MCAT progress lives in `rounds.mcat.v1` (same shape as the boards record plus `reviewed: {topicId: ts}` for the
  guides' Reviewed ticks; created only once something is saved). Theme and text size stay in the boards record
  whichever exam is selected (`Store.settings()`). Which guide groups are expanded is in `rounds.guide.v1`.

## Current state (2026-10-11)
- Boards: 24 questions (Blocks 1–3). Anatomy: 2D body (front/back, 8 layers incl. dermatomes), brain, heart,
  254-entry index; 3D body (seven lazy-loaded layers, 7.8 MB gzipped), 3D brain (real-MRI cortex, deep brain, circle of
  Willis, cranial nerves) and 3D heart (chambers, valves, coronaries, cut-open view). Live at
  https://jjones1319-create.github.io/rounds/ and confirmed smooth on her phone.
- MCAT: Phase M0 done 2026-10-10 (Boards | MCAT switcher on Home, Practice and Progress; banks fetched from `data/`;
  `tools/validate.py`; HTTP tests; `rounds.mcat.v1`). Phase M1 done 2026-10-11: section screens and all four
  "What's tested" guides (Chem/Phys 96 topics, Bio/Biochem 62, Psych/Soc 61, CARS skill areas; all topics `draft`,
  references to OpenStax/LibreTexts, every fact independently checked). Phase M2 done 2026-10-11: blocks
  `M1`–`M3` (8 discrete items per science section, all `draft`), MCAT runner (periodic table `src/ptable.js` instead of
  labs, Takeaway + guide links), block builder by section/skill/difficulty, progress by section/skill/category. Phase M3 done 2026-10-11: passage runner
  (phone: sticky Passage | Question toggle; ≥800 px: two panes), tap-drag highlights kept with the block (`hl` in the
  session), figures drawn from passage data (tables, line/bar/scatter SVG, KaTeX equations, RDKit structures at build
  time via `tools/structures.py`, `pip install rdkit`), passage sets travel together in blocks; blocks M4–M7 (3 science
  passages, 2 original CARS passages, 22 items).
- Open gaps: many 3D structures show a name-only card; write verified cards for the important ones.

## Work order
Work on one track at a time and finish its current phase before switching. Report at each phase boundary.
- Track A, 3D anatomy: `docs/PLAN_3D.md`. Phases 0–2 are done; Phase 3 (progress export/import, installable PWA) remains.
- Track B, MCAT: `docs/PLAN_MCAT.md`. M0–M3 are done; M4 (review workflow) is next, then M5 (ongoing growth).
- Track C, content: new board blocks (`/new-board-block`, boards spec) and MCAT blocks (MCAT spec).
- If the site is ever to be promoted: `docs/PUBLIC_RELEASE.md` checklist first.
