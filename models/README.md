# models/

Optimized 3D model files (`.glb`), one per anatomy layer, each loaded only when its layer is switched on.
Raw source downloads stay in `work/` (gitignored).

| File | App layer | Size (gzipped as served) |
|---|---|---|
| `skeleton.glb` | Skeleton (`bone`) | 2.0 MB (1.3 MB) |
| `organs.glb` | Organs (`organ`) | 0.9 MB (0.6 MB) |
| `muscles.glb` | Muscles (`muscle`) | 4.4 MB (3.0 MB) |
| `arteries.glb` | Arteries (`artery`) | 1.8 MB (0.9 MB) |
| `veins.glb` | Veins (`vein`) | 1.1 MB (0.6 MB) |
| `nerves.glb` | Nerves (`nerve`) | 1.6 MB (1.0 MB) |
| `lymph.glb` | Lymphatics (`lymph`) | 0.6 MB (0.3 MB) |

Rebuild: `py tools/build_models.py [layer ...]` (Blender export by `tools/export_layers.py`, then glTF-Transform
weld, simplify, meshopt). Which meshes each layer takes, and what is never exported, is in `tools/export_layers.py`.

Licensed CC BY-SA 4.0: see `LICENSE` here and `CREDITS.md`. Before adding or changing a file: read docs/PLAN_3D.md
§Licensing, update `LICENSE` and `CREDITS.md`.

Mesh names → app cards: `data/mesh_map.json` (checked by `tests/three_d.py`).
