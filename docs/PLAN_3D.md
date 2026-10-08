# Plan: real 3D anatomy for Rounds

Goal: replace the hand-drawn body diagram with real, rotatable 3D anatomy that works on a mid-range Android
phone, while keeping every existing card, the index, search, and quizzes working. The 2D diagram stays as a
fallback ("Diagram" mode) and remains the home of the dermatome layer, which the 3D sources don't include.

---

## Sources

| Source | What it is | License | Where |
|---|---|---|---|
| **Z-Anatomy** | Organized, layered, named 3D atlas built from BodyParts3D. Distributed as a Blender file (`Z-Anatomy.zip` → `Startup.blend`). | CC BY-SA 4.0 | github.com/Z-Anatomy/Models-of-human-anatomy |
| **BodyParts3D** | The original mesh dataset from Japan's Database Center for Life Science. | CC BY-SA 2.1 Japan | dbarchive.biosciencedbc.jp/en/bodyparts3d/download.html |

Leads to check before starting (they may make the job easier):
- The Z-Anatomy author wrote in 2024 that universities (Leiden, Maastricht, Utrecht, Leuven) received funding to
  continue the project and planned a release under the same license. Search for it; if it exists and is maintained,
  it may be a better starting point.
- BodyParts3D's own download may offer per-part mesh files directly, which would avoid Blender entirely. Check the
  formats and naming before choosing a pipeline.

## Licensing (read before adding any model file)

- Both sources are **share-alike**. Any model file we derive (simplified, recolored, merged, converted) must be
  published under **CC BY-SA 4.0** with attribution. The repo is public, which satisfies "share".
- Put derived models in `models/` with a `models/LICENSE` (CC BY-SA 4.0) and keep `CREDITS.md` complete.
- Required attribution lines (from the Z-Anatomy readme):
  - "BodyParts3D, The Database Center for Life Science, CC BY-SA 2.1 Japan"
  - "Z-Anatomy, the libre 3D atlas of anatomy, CC BY-SA 4.0" (Gauthier Kervyn, Marcin Zielinski)
- **Exclude non-commercial (NC) parts** that Z-Anatomy bundles from other contributors, so the whole app stays
  under one compatible license. The readme lists, among others: "Anatomy of the Inner Ear" (University of Dundee,
  CC BY-NC-SA 4.0) and "Kidney" (Lissie Cowley, CC BY-NC 4.0). Check the full attribution list in the readme and
  per-object metadata; use the BodyParts3D-derived version of any structure that has an NC alternative.
- "Cranial Nerves and Foramina" (University of Dundee, CAHID) is CC BY 4.0, which is compatible; credit it if used.
- **Do not import Z-Anatomy's text definitions** (they derive from Wikipedia, CC BY-SA 3.0). Use our own cards in
  `src/content.js` and `src/models.js`.
- The app's own code and questions can carry any license the owner chooses; ask them. The model files cannot.

## Pipeline (suggested; verify each tool's current options with `--help`)

1. Download the source into `work/` (gitignored). Never commit raw source files.
2. Open the Blender file headless and **list every object name and its collection** to a text file first.
   Example: `blender -b work/Startup.blend --python tools/list_objects.py`. Names drive everything else.
3. Export one system at a time to glTF binary (`.glb`) with a Blender Python script (`bpy.ops.export_scene.gltf`),
   keeping object names, applying modifiers, and dropping materials/textures we don't need.
4. Optimize with glTF-Transform (`npm i -g @gltf-transform/cli`): weld, simplify (meshoptimizer), quantize, and
   compress (Meshopt or Draco). Tune simplification per system until it looks right at phone size.
5. Viewer: three.js with `GLTFLoader` (+ `MeshoptDecoder` or `DRACOLoader`) and `OrbitControls`.
   **Vendor the three.js files into the repo** (from the `three` npm package) so the app works offline.
   Tap selection by raycasting; highlight with an emissive tint or outline; dim the rest; frame the camera on the
   selection.

## Phases and acceptance criteria

### Phase 0: repo and hosting
- Create the GitHub repo (ask the owner first; it must be public for free Pages), push, enable Pages.
- Pass: the current app loads at `https://<user>.github.io/<repo>/` on her phone; `tests/` pass locally.

### Phase 1: skeleton feasibility test (stop and report after this)
- Build a 3D skeleton (major bones; hands and feet can be merged groups at first) with rotate, zoom, pan, tap.
- Add a "3D | Diagram" switch on the Body tab; Diagram is today's view.
- Report to the owner: download size, time to first render, and how it feels on her phone. Suggested targets
  (not hard rules): skeleton ≤ ~8 MB transferred, interactive within a few seconds on 4G, smooth rotation on a
  mid-range phone. If targets are missed, simplify further before adding more systems.
- Pass: tapping a bone opens the same card the 2D figure shows (e.g., femur → `INFO.femur`).

### Phase 2: more systems
- Separate `.glb` per layer (organs, muscles, arteries, veins, nerves, lymphatics), **loaded only when that layer
  is switched on**. Keep every file well under GitHub's 100 MB hard limit (aim ≤ ~15 MB each).
- Create `data/mesh_map.json`: for each existing card key (see `INFO` in `src/content.js` and `src/models.js`),
  the list of mesh names it covers, with side (left/right) where relevant. Many meshes can map to one card.
  Meshes without a card can show a name-only card; prefer writing a proper card (verified facts) over leaving gaps.
- Index and search must highlight the 3D mesh when in 3D mode (and the 2D shape in Diagram mode).
- "Name that structure" should work in 3D (highlight a mesh, offer four names).
- Pass: every existing body card that has a matching 3D structure opens from a tap; smoke and overflow tests pass.

### Phase 3: progress backup and installable app
- Export/import progress: download a JSON file and restore from it (and/or a copy-paste code). Show this in Settings.
- PWA: `manifest.webmanifest`, icons, and a service worker that caches the app shell, vendored three.js, and
  model files (cache-first, versioned, so updates replace old models).
- Pass: "Add to Home screen" installs it; it opens offline after the first full load.

### Phase 4: Block 3 questions
- Follow `docs/board_question_generator_spec.md` exactly. Coverage gaps are in spec §7.

## Things to preserve
- Brain and heart models are separate 2D diagrams with their own cards; they can stay 2D or be upgraded later.
- The dermatome layer lives in the 2D figure only.
- Accessibility: visible focus, keyboard support in the question runner, `prefers-reduced-motion`, dark mode.
