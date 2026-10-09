"""Export Z-Anatomy anatomy layers to unoptimized glTF binaries (docs/PLAN_3D.md, Phases 1-2).

Run headless from the repo root, with embedded-script autorun disabled:
  blender -b --factory-startup -Y work/zanatomy/Z-Anatomy/Startup.blend --python tools/export_layers.py -- work/raw [layer ...]
Writes work/raw/<file>_raw.glb per layer; tools/build_models.py then optimizes them into models/.

Each node is named "<Name>_<R|L>" and carries glTF extras {"n": Z-Anatomy name, "s": "R"|"L"|""}.
Licensing rules (docs/PLAN_3D.md §Licensing) are enforced here: see NEVER below.
"""
import re
import sys
import bmesh
import bpy

args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUTDIR = args[0] if args else "work/raw"
ONLY = set(args[1:])

SK, MU, CV, LY, NS, VS = ("1: Skeletal system", "4: Muscular system", "5: Cardiovascular system",
                          "6: Lymphoid organs", "7: Nervous system & Sense organs", "8: Visceral systems")

# Never exported, whatever the layer: parts that may come from non-commercial or unlicensed sources.
NEVER = re.compile(
    r"^(Incus|Malleus|Stapes|Cochlea|Vestibule|Tympanic membrane|Auditory tube|Cochlear nerve|Vestibular nerve)$"   # inner/middle ear: Univ. of Dundee, CC BY-NC-SA
    r"|^Intrarenal |^Renal pelvis$"                                                  # kidney internals: L. Cowley, CC BY-NC
    r"|\?")                                                                          # unnamed objects

LAYERS = {
    "bone": dict(file="skeleton", primary=[SK], types={"MESH"}, exclude=
        r"^(Anterior|Middle|Posterior) cells of ethmoid bone$|^Sinus of (frontal|sphenoid) bone$"          # air spaces modeled as solids
        r"|^(Arytenoid|Corniculate|Cricoid|Thyroid) cartilage$|^Major alar cartilage$|[Nn]asal septal cartilage$"),
    "organ": dict(file="organs", primary=[VS], types={"MESH", "CURVE"},
        extra=[(CV, r"^(Left|Right) (atrium|ventricle)$"), (LY, r"^Spleen$"), (MU, r"^Diaphragm$"), (NS, r"^(Sclera|Cornea)$")],
        exclude=r"segment of liver|^Pleura$|omentum$|^Mesocolon$|^Meso-appendix$|taenia$|^Mucosa of|^Gingiva$"
                r"|ancreatic duct$|segmental bronchus|lobar bronchus|^Intermediate bronchus$"),
    "muscle": dict(file="muscles", primary=[MU], types={"MESH"}, exclude=
        r"fascia|aponeurosis|bursa|[Ss]heath|retinacul|septum|^Linea alba$|ligament|tarsus$|^Common tendinous ring$"
        r"|^Trochlea of|arch of levator ani$|^Iliopectineal arch$|^Iliotibial tract$|^Diaphragm$"),
    "artery": dict(file="arteries", primary=[CV], types={"CURVE", "MESH"}, path=r"arteries|Arteries|Aorta|arterial"),
    "vein": dict(file="veins", primary=[CV], types={"CURVE", "MESH"}, path=r"[Vv]eins|[Vv]enous|vena cava", notpath=r"arteries|Arteries|Aorta|arterial"),
    # nerves: the curves (peripheral and cranial nerves, sympathetic trunk) plus the spinal cord; never brain, eye or ear meshes
    "nerve": dict(file="nerves", primary=[NS], types={"CURVE", "MESH"},
        keep=lambda ob, p: ob.type == "CURVE" or "Bonus collection" not in p or re.match(r"Ganglia of sympathetic trunk", ob.name),
        exclude=r"^Central canal'$",
        merge={"Spinal cord": lambda ob, p: ob.type == "MESH" and "Bonus collection" not in p and not ob.name.startswith("Spinal ganglion")}),
    "lymph": dict(file="lymph", primary=[LY], types={"MESH"}, exclude=r"^Spleen$"),
}
# Curves: Z-Anatomy uses 20-sided tubes with 12 steps per segment; 8 sides and 4 steps look the same on a phone.
BEVEL_RES, CURVE_RES = 1, 4

HELPER = re.compile(r"\.(j|i|g)$")
SIDE = re.compile(r"\.(r|l)$")

paths = {}
def walk(coll, prefix):
    for ch in coll.children:
        p = f"{prefix}/{ch.name}" if prefix else ch.name
        paths.setdefault(ch.name, p)
        walk(ch, p)
for sc in bpy.data.scenes:
    walk(sc.collection, "")
def path_of(ob): return ";".join(paths.get(c.name, c.name) for c in ob.users_collection)
def in_coll(ob, names): return any(c.name in names for c in ob.users_collection)

def select(cfg):
    out = []
    for ob in bpy.data.objects:
        if ob.type not in cfg["types"] or HELPER.search(ob.name):
            continue
        base = SIDE.sub("", ob.name)
        if NEVER.search(base):
            continue
        p = path_of(ob)
        hit = in_coll(ob, cfg["primary"])
        if not hit:
            hit = any(in_coll(ob, [c]) and re.search(rx, base) for c, rx in cfg.get("extra", []))
        if not hit:
            continue
        if cfg.get("exclude") and re.search(cfg["exclude"], base) and not any(re.search(rx, base) for _, rx in cfg.get("extra", [])):
            continue
        if cfg.get("path") and not re.search(cfg["path"], p):
            continue
        if cfg.get("notpath") and re.search(cfg["notpath"], p):
            continue
        if cfg.get("keep") and not cfg["keep"](ob, p):
            continue
        m = SIDE.search(ob.name)
        out.append((ob, base, m.group(1).upper() if m else "", p))
    return out

def mesh_of(ob, dg):
    ev = ob.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev, preserve_all_data_layers=False, depsgraph=dg)
    me.transform(ob.matrix_world)
    return me

def clean(me):
    me.materials.clear()
    while me.uv_layers:
        me.uv_layers.remove(me.uv_layers[0])
    while me.color_attributes:
        me.color_attributes.remove(me.color_attributes[0])
    return me

def export(layer, cfg):
    dg = bpy.context.evaluated_depsgraph_get()
    chosen = select(cfg)
    merges = {name: [] for name in cfg.get("merge", {})}
    singles = []
    for ob, base, side, p in chosen:
        target = next((n for n, f in cfg.get("merge", {}).items() if f(ob, p)), None)
        (merges[target] if target else singles).append((ob, base, side))
    made = []
    def add(name, side, me):
        if not me.polygons:
            bpy.data.meshes.remove(me); return
        node = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_") + (f"_{side}" if side else "")
        nob = bpy.data.objects.new(node, clean(me))
        nob["n"], nob["s"] = name, side
        bpy.context.scene.collection.objects.link(nob)
        made.append(nob)
    for ob, base, side in singles:
        me = mesh_of(ob, dg)
        if len(me.polygons) < 4:          # label points and stubs
            bpy.data.meshes.remove(me); continue
        add(base, side, me)
    for name, items in merges.items():
        if not items:
            continue
        bm = bmesh.new()
        for ob, _, _ in items:
            me = mesh_of(ob, dg); bm.from_mesh(me); bpy.data.meshes.remove(me)
        me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
        add(name, "", me)
    for ob in bpy.context.view_layer.objects:
        ob.select_set(False)
    for ob in made:
        ob.select_set(True)
    out = f"{OUTDIR}/{cfg['file']}_raw.glb"
    bpy.ops.export_scene.gltf(
        filepath=out, export_format="GLB", use_selection=True, export_apply=False, export_yup=True,
        export_materials="NONE", export_texcoords=False, export_normals=True, export_extras=True,
        export_animations=False, export_skins=False, export_morph=False, export_cameras=False, export_lights=False)
    tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in made)
    print(f"LAYER {layer}: {len(made)} meshes, {tris} tris -> {out}")
    print(f"NAMES {layer}: " + " | ".join(sorted({o['n'] for o in made})))
    for ob in made:                       # keep the next layer's export clean
        bpy.data.objects.remove(ob)

import os
os.makedirs(OUTDIR, exist_ok=True)
for cu in bpy.data.curves:               # tube resolution, set once before anything is evaluated
    cu.bevel_resolution = min(cu.bevel_resolution, BEVEL_RES)
    cu.resolution_u = min(cu.resolution_u, CURVE_RES)
for layer, cfg in LAYERS.items():
    if not ONLY or layer in ONLY:
        export(layer, cfg)
