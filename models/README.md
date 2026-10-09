# models/

Optimized 3D model files (`.glb`), one per anatomy layer. Raw source downloads stay in `work/` (gitignored).

| File | Layer | Built by |
|---|---|---|
| `skeleton.glb` | Skeleton (Phase 1) | `py tools/build_models.py` (Blender export → glTF-Transform weld, simplify, meshopt) |

Licensed CC BY-SA 4.0: see `LICENSE` here and `CREDITS.md`. Before adding a file: read docs/PLAN_3D.md §Licensing,
add its source and changes to `LICENSE`, and update `CREDITS.md`.

Mesh names → app cards: `data/mesh_map.json`.
