"""Rebuild models/skeleton.glb from the Z-Anatomy source (docs/PLAN_3D.md, Phase 1).

Needs (all under work/, which git ignores):
  work/zanatomy/Z-Anatomy/Startup.blend   from Z-Anatomy.zip, commit bb293be4 of
                                           github.com/Z-Anatomy/Models-of-human-anatomy
  Blender 5.x                              set BLENDER, or unzip the portable build into work/tools/
  work/node: npm i --ignore-scripts three@0.186.1 @gltf-transform/cli@4.5.1

Run from the repo root:  py tools/build_models.py [--ratio 0.5] [--error 0.002]
"""
import argparse, glob, os, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
ap = argparse.ArgumentParser()
ap.add_argument("--ratio", type=float, default=0.5, help="simplify target: fraction of triangles to keep")
ap.add_argument("--error", type=float, default=0.002, help="simplify error limit, fraction of each mesh's radius")
ap.add_argument("--skip-export", action="store_true", help="reuse work/skeleton_raw.glb")
a = ap.parse_args()

blender = os.environ.get("BLENDER") or next(iter(sorted(glob.glob(str(WORK / "tools/blender-*/blender.exe")) + glob.glob(str(WORK / "tools/blender-*/blender")))), None)
gt = ["node", str(WORK / "node/node_modules/@gltf-transform/cli/bin/cli.js")]
src, raw = WORK / "zanatomy/Z-Anatomy/Startup.blend", WORK / "skeleton_raw.glb"
tmp1, tmp2, out = WORK / "skeleton_welded.glb", WORK / "skeleton_simplified.glb", ROOT / "models/skeleton.glb"

def run(cmd):
    print("+", " ".join(str(c) for c in cmd), flush=True)
    r = subprocess.run([str(c) for c in cmd], capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stdout[-3000:] + r.stderr[-3000:])
    return r.stdout

if not a.skip_export:
    if not blender: sys.exit("Blender not found: set BLENDER or unzip it into work/tools/")
    # -Y: never run scripts embedded in the downloaded .blend
    log = run([blender, "-b", "--factory-startup", "-Y", src, "--python", ROOT / "tools/export_skeleton.py", "--", raw])
    print(next((l for l in log.splitlines() if l.startswith("exported")), ""))
run(gt + ["weld", raw, tmp1])
run(gt + ["simplify", tmp1, tmp2, "--ratio", a.ratio, "--error", a.error])
run(gt + ["meshopt", tmp2, out])
print(f"{out.relative_to(ROOT)}: {out.stat().st_size / 1048576:.2f} MB (ratio {a.ratio}, error {a.error})")
