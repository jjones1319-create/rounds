"""Rebuild models/*.glb from the Z-Anatomy source (docs/PLAN_3D.md, Phases 1-2).

Needs (all under work/, which git ignores):
  work/zanatomy/Z-Anatomy/Startup.blend   from Z-Anatomy.zip, commit bb293be4 of
                                           github.com/Z-Anatomy/Models-of-human-anatomy
  Blender 5.x                              set BLENDER, or unzip the portable build into work/tools/
  work/node: npm i --ignore-scripts three@0.186.1 @gltf-transform/cli@4.5.1
  work/bp3d/: BodyParts3D partof_BP3D_4.0_obj_99.zip unzipped into obj/, plus partof_element_parts.txt
              (dbarchive.biosciencedbc.jp/data/bodyparts3d/LATEST/); only the heart layers need it

Run from the repo root:  py tools/build_models.py [layer ...] [--skip-export]
"""
import argparse, glob, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
# file name, simplify ratio (fraction of triangles kept), error limit (fraction of each mesh's radius)
LAYERS = {
    "bone":   ("skeleton", 0.5, 0.002),
    "organ":  ("organs",   0.5, 0.002),
    "muscle": ("muscles",  0.3, 0.003),
    "artery": ("arteries", 0.7, 0.002),   # tubes are already low-resolution (tools/export_layers.py)
    "vein":   ("veins",    0.7, 0.002),
    "nerve":  ("nerves",   0.7, 0.002),
    "lymph":  ("lymph",    0.5, 0.002),
    # Brain and Heart tabs: close-up scenes, so lighter simplification
    "brain_cortex": ("brain_cortex", 1.0, 0.002), "brain_deep": ("brain_deep", 0.6, 0.002), "brain_artery": ("brain_arteries", 0.8, 0.002),
    "brain_nerve": ("brain_nerves", 0.8, 0.002), "brain_skull": ("brain_skull", 0.5, 0.002),
    "heart_wall": ("heart_wall", 0.8, 0.002), "heart_valves": ("heart_valves", 0.8, 0.002), "heart_coronary": ("heart_coronary", 0.8, 0.002),
    "heart_veins": ("heart_veins", 0.8, 0.002), "heart_vessels": ("heart_vessels", 1.0, 0.002),
}
ap = argparse.ArgumentParser()
ap.add_argument("layers", nargs="*", choices=[[]] + list(LAYERS), help="default: all")
ap.add_argument("--skip-export", action="store_true", help="reuse work/raw/*_raw.glb")
a = ap.parse_args()
todo = a.layers or list(LAYERS)

blender = os.environ.get("BLENDER") or next(iter(sorted(glob.glob(str(WORK / "tools/blender-*/blender.exe")) + glob.glob(str(WORK / "tools/blender-*/blender")))), None)
gt = ["node", str(WORK / "node/node_modules/@gltf-transform/cli/bin/cli.js")]
src, raw = WORK / "zanatomy/Z-Anatomy/Startup.blend", WORK / "raw"

def run(cmd):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stdout[-3000:] + r.stderr[-3000:])
    return r.stdout

if not a.skip_export:
    if not blender: sys.exit("Blender not found: set BLENDER or unzip it into work/tools/")
    # -Y: never run scripts embedded in the downloaded .blend
    log = run([blender, "-b", "--factory-startup", "-Y", src, "--python", ROOT / "tools/export_layers.py", "--", raw, *todo])
    print("\n".join(l for l in log.splitlines() if l.startswith("LAYER")))
for layer in todo:
    name, ratio, err = LAYERS[layer]
    i, w, s, out = raw / f"{name}_raw.glb", raw / f"{name}_welded.glb", raw / f"{name}_simplified.glb", ROOT / f"models/{name}.glb"
    run(gt + ["weld", i, w])
    run(gt + ["simplify", w, s, "--ratio", ratio, "--error", err])
    run(gt + ["meshopt", s, out])
    print(f"{out.relative_to(ROOT)}: {out.stat().st_size / 1048576:.2f} MB (ratio {ratio}, error {err})")
