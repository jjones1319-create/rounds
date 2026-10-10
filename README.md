# Rounds

A phone-friendly study app for the boards (original USMLE® Step 2 CK–style questions with full explanations) and,
in progress, the MCAT®, plus an interactive 2D and 3D anatomy guide (body, brain, heart, an A–Z index, and quizzes).

## Get it running (one time)

You need: **VS Code** (1.98 or newer) with the **Claude Code** extension from Anthropic, **Git**, a **GitHub**
account, and **Python 3.10+**. For the 3D work you'll also need **Blender** (free) and **Node.js**; Claude Code can
walk you through installing those when it gets there.

1. Unzip this folder somewhere easy to find, for example `Documents/rounds`.
2. In VS Code: **File → Open Folder…** and choose the `rounds` folder.
3. Open the Claude Code panel (the spark icon at the top right of the editor) and type:

   > Read CLAUDE.md and docs/PLAN_3D.md, then help me with Phase 0: create the GitHub repo, push this folder,
   > and turn on GitHub Pages. Ask me before anything public.

4. When it's done, the app is live at `https://YOUR-USERNAME.github.io/rounds/` (the exact link depends on the
   repository name).

## On her phone

Open the link in Chrome, tap **⋮ → Add to Home screen**. It opens like an app.

Progress saves in the phone's browser. Progress from the claude.ai version won't carry over (it's a different
website), so she starts fresh here.

## Working on it later

Open the folder in VS Code and tell Claude Code what you want. Useful starting prompts:
- "Continue with the next phase in docs/PLAN_3D.md."
- "Write Block 3 following docs/board_question_generator_spec.md."
- "Rebuild, run the tests, and push."

## For developers

- Build: `python build.py` reads `questions/` (boards) and `content/` (MCAT, validated by `tools/validate.py`),
  writes `data/boards.json`, `data/mcat.json`, and `index.html`. The app fetches the data files at startup, so open it
  over HTTP (the tests start their own local server).
- Tests: `pip install -r tests/requirements.txt`, `python -m playwright install chromium`,
  then `python tests/smoke.py`, `python tests/overflow.py` and `python tests/three_d.py`
- 3D models: `python tools/build_models.py` (see `models/README.md`)
- Architecture and rules: `CLAUDE.md`. Plans: `docs/PLAN_3D.md`, `docs/PLAN_MCAT.md`. Question rules:
  `docs/board_question_generator_spec.md`, `docs/MCAT_SPEC.md`.

## About

Rounds is an independent, free study resource. It is not affiliated with, endorsed by, or sponsored by the AAMC,
FSMB, or NBME. Practice scores are not predictions of official scores. Content is for exam study only and is not
medical advice. MCAT® is a registered trademark of the Association of American Medical Colleges (AAMC). USMLE® is a
program of the Federation of State Medical Boards (FSMB) and the National Board of Medical Examiners (NBME).
Progress is saved only in your browser; there are no accounts, ads, or tracking.
