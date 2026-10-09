# Rounds

A phone-friendly study app for USMLE Step 2 CK: original board-style questions with full explanations, plus an
interactive anatomy guide (body, brain, heart, an A–Z index, and quizzes).

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

- Build: `python build.py` (writes `index.html`)
- Tests: `pip install -r tests/requirements.txt`, `python -m playwright install chromium`,
  then `python tests/smoke.py`, `python tests/overflow.py` and `python tests/three_d.py`
- 3D models: `python tools/build_models.py` (see `models/README.md`)
- Architecture and rules: `CLAUDE.md`. 3D plan: `docs/PLAN_3D.md`. Question rules: `docs/board_question_generator_spec.md`.
