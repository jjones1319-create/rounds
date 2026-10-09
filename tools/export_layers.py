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
from mathutils import Vector
from mathutils.bvhtree import BVHTree
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

    # ---- Brain tab (its own scene). Cortex = Brainder (A. Winkler, real MRI, CC BY-SA 3.0) as placed by Z-Anatomy.
    # Never "White matter of telencephalon": Z-Anatomy credits it to the University of Washington with no license.
    "brain_cortex": dict(file="brain_cortex", primary=[NS], types={"MESH"},
        keep=lambda ob, p: "/Brain/Cerebrum/" in p and "/Diencephalon" not in p and SIDE.sub("", ob.name).strip() not in BRAIN_DEEP,
        exclude=r"^White matter of telencephalon$|^Lentiform nucleus$|^Septal nuclei$|^Stria terminalis$"),
    "brain_deep": dict(file="brain_deep", primary=[NS], types={"MESH"},
        extra=[(VS, r"^(Adenohypophysis|Neurohypophysis|Pineal gland)$")],
        keep=lambda ob, p: SIDE.sub("", ob.name).strip() in BRAIN_DEEP or "/Brain/Cerebellum" in p or SIDE.sub("", ob.name) in ("Adenohypophysis", "Neurohypophysis", "Pineal gland")),
    "brain_artery": dict(file="brain_arteries", primary=[CV], types={"CURVE", "MESH"}, near=("brain", 0.02),
        path=r"arteries|Arteries|arterial",
        keep=lambda ob, p: re.search(r"cerebral|[Cc]erebellar|[Bb]asilar|communicating|callos|[Pp]ontine|Internal carotid|^Vertebral artery|"
                                     r"Orbitofrontal|Ophthalmic artery|[Cc]horoidal|Branch to angular gyrus|Artery of (pre|post)?central sulcus|"
                                     r"(Parietal|Temporal) branches of middle", ob.name)),
    "brain_nerve": dict(file="brain_nerves", primary=[NS], types={"CURVE", "MESH"}, near=("brain", 0.015),
        keep=lambda ob, p: re.search(r"\((I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII)\)$|^(Ophthalmic|Maxillary) nerve$|division of mandibular nerve$|root of trigeminal nerve$",
                                     SIDE.sub("", ob.name))),
    "brain_skull": dict(file="brain_skull", primary=[SK], types={"MESH"}, clip="brain",
        keep=lambda ob, p: SIDE.sub("", ob.name) in ("Frontal bone", "Parietal bone", "Temporal bone", "Occipital bone", "Sphenoid bone", "Ethmoid bone")),

    # ---- Heart tab (its own scene). Z-Anatomy chambers, leaflets, veins and great vessels, plus BodyParts3D parts that
    # Z-Anatomy lacks (anterior mitral and tricuspid leaflets, LV anterolateral papillary muscle) and its coronary arteries.
    "heart_wall": dict(file="heart_wall", primary=[CV], types={"MESH"}, tube=(3, 8),
        keep=lambda ob, p: SIDE.sub("", ob.name) in ("Left atrium", "Right atrium", "Left ventricle", "Right ventricle")),
    "heart_valves": dict(file="heart_valves", primary=[CV], types={"MESH"},
        keep=lambda ob, p: re.search(r"leaflet|papillary muscle", ob.name),
        bp3d=dict(concept="heart", name=r"^(Anterior leaflet of (mitral|tricuspid) valve|Anterolateral head of lateral papillary muscle of left ventricle|Lateral papillary muscle of left ventricle)$")),
    "heart_coronary": dict(file="heart_coronary", primary=[CV], types={"CURVE", "MESH"}, tube=(3, 8),
        keep=lambda ob, p: SIDE.sub("", ob.name) in ("Left coronary artery", "Right coronary artery", "Anterior interventricular artery",
            "Circumflex artery of heart", "Right inferolateral branch of right coronary artery", "Septal branches of anterior interventricular artery")),
    "heart_veins": dict(file="heart_veins", primary=[CV], types={"CURVE", "MESH"}, tube=(3, 8),
        keep=lambda ob, p: SIDE.sub("", ob.name) in ("Coronary sinus", "Great cardiac vein", "Middle cardiac vein", "Inferior vein of left ventricle")),
    "heart_vessels": dict(file="heart_vessels", primary=[CV], types={"CURVE", "MESH"}, clip="heart", tube=(3, 8),
        keep=lambda ob, p: SIDE.sub("", ob.name) in (
            "Ascending aorta", "Aortic arch", "Thoracic aorta", "Brachiocephalic trunk", "Left common carotid artery",
            "Left subclavian artery", "Pulmonary trunk", "Bifurcation of pulmonary trunk", "Left pulmonary artery",
            "Right pulmonary artery", "Superior vena cava", "Inferior vena cava (thoracic part)", "Left superior pulmonary vein",
            "Left inferior pulmonary vein", "Right superior pulmonary vein", "Right inferior pulmonary vein")),
}
for _k in ("brain_artery", "brain_nerve"):
    LAYERS[_k]["tube"] = (2, 6)            # close-ups: rounder tubes than the whole-body layers need
# Deep brain structures (brainstem, diencephalon, basal ganglia, limbic, commissures, ventricles); cerebellum comes by collection.
BRAIN_DEEP = {
    "Medulla oblongata", "Pons", "Midbrain", "Olive", "Pyramid of medulla oblongata", "Inferior colliculus", "Superior colliculus",
    "Base of peduncle", "Superior cerebellar peduncle", "Thalamus", "Hypothalamus", "Mamillary body", "Lateral geniculate body",
    "Medial geniculate body", "Optic chiasm", "Optic tract", "Third ventricle", "Fourth ventricle", "Lateral ventricle",
    "Aqueduct of midbrain", "Caudate nucleus", "Putamen", "Globus pallidus", "Amygdaloid body", "Hippocampus", "Fornix",
    "Corpus callosum", "Anterior commissure", "Posterior commissure", "Hippocampal commissure", "Septum pellucidum",
}
# Clip boxes (metres, Blender axes: +X subject's left, -Y front, +Z up): margins around a reference set of objects.
CLIPS = {
    "brain": dict(ref=lambda ob, p: ob.type == "MESH" and re.search(r"/Brain/(Cerebrum/Telencephalon|Cerebellum|Brainstem)", p)
                  and "White matter" not in ob.name, lo=(0.012, 0.02, 0.035), hi=(0.012, 0.012, 0.012)),
    "heart": dict(ref=lambda ob, p: ob.type == "MESH" and ob.name in ("Left atrium", "Right atrium", "Left ventricle", "Right ventricle"),
                  lo=(0.03, 0.02, 0.02), hi=(0.03, 0.035, 0.07)),
}
# BodyParts3D 4.0 "part_of" meshes (work/bp3d/, CC BY-SA 2.1 JP). Same axes as Z-Anatomy, in mm, offset by BP3D_TO_ZA:
# measured from parts both files contain (tricuspid septal and mitral posterior leaflets, RV papillary muscles), +-1 mm.
BP3D_DIR, BP3D_LIST = "work/bp3d/obj/partof_BP3D_4.0_obj_99", "work/bp3d/partof_element_parts.txt"
BP3D_TO_ZA = (1.5, 96.8, 63.9)

def bp3d_elements(concept, name_rx):
    """Element meshes (FJ ids) of a BodyParts3D concept whose own English name matches name_rx."""
    fjs = sorted({fj for fma, nm, fj in (l.rstrip("\n").split("\t") for l in open(BP3D_LIST, encoding="utf-8")) if nm == concept})
    return [(fj, n) for fj in fjs if re.search(name_rx, n := bp3d_name(fj))]

def bp3d_name(fj):
    with open(f"{BP3D_DIR}/{fj}.obj", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("# English name"):
                return line.split(":", 1)[1].strip()
    return fj

def bp3d_mesh(fj, name):
    """Read a BodyParts3D OBJ (mm) into a mesh in Z-Anatomy space (m)."""
    d, vs, fs = BP3D_TO_ZA, [], []
    with open(f"{BP3D_DIR}/{fj}.obj", encoding="utf-8", errors="replace") as f:
        for line in f:
            if line.startswith("v "):
                x, y, z = map(float, line.split()[1:4]); vs.append(((x + d[0]) / 1000, (y + d[1]) / 1000, (z + d[2]) / 1000))
            elif line.startswith("f "):
                fs.append([int(t.split("/")[0]) - 1 for t in line.split()[1:]])
    me = bpy.data.meshes.new(name); me.from_pydata(vs, [], fs); me.update()
    return me
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
        base = " ".join(SIDE.sub("", ob.name).split())   # Z-Anatomy has a few stray spaces
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

_boxes = {}
def box_for(name):
    """World-space box around CLIPS[name]['ref'] objects, grown by its margins."""
    if name not in _boxes:
        c, pts = CLIPS[name], []
        for ob in bpy.data.objects:
            if not HELPER.search(ob.name) and c["ref"](ob, path_of(ob)):
                pts += [ob.matrix_world @ Vector(v) for v in ob.bound_box]
        lo = Vector([min(v[i] for v in pts) - c["lo"][i] for i in range(3)])
        hi = Vector([max(v[i] for v in pts) + c["hi"][i] for i in range(3)])
        _boxes[name] = (lo, hi)
        print(f"CLIP {name}: {tuple(round(x, 3) for x in lo)} .. {tuple(round(x, 3) for x in hi)}")
    return _boxes[name]

def clip(me, lo, hi):
    """Cut a mesh to a box (long vessels and nerves leave the brain or heart scene at its edges)."""
    bm = bmesh.new(); bm.from_mesh(me)
    for axis in range(3):
        for sign, val in ((1, lo[axis]), (-1, hi[axis])):
            no, co = Vector((0, 0, 0)), Vector((0, 0, 0)); no[axis], co[axis] = sign, val
            bmesh.ops.bisect_plane(bm, geom=bm.verts[:] + bm.edges[:] + bm.faces[:], plane_co=co, plane_no=no, clear_inner=True)
    # a vessel that leaves the box and comes back leaves a stray piece: keep only the big connected parts
    seen, islands = set(), []
    for v in bm.verts:
        if v in seen: continue
        stack, part = [v], []
        seen.add(v)
        while stack:
            x = stack.pop(); part.append(x)
            for e in x.link_edges:
                y = e.other_vert(x)
                if y not in seen: seen.add(y); stack.append(y)
        islands.append(part)
    if len(islands) > 1:                  # keep the piece(s) nearest the middle of the box, i.e. attached to the organ
        mid = (lo + hi) / 2
        near = [min((v.co - mid).length for v in i) for i in islands]
        best = min(near)
        far = [v for i, d in zip(islands, near) if d > best + 0.015 for v in i]
        bmesh.ops.delete(bm, geom=far, context="VERTS")
    bm.to_mesh(me); bm.free()
    return me

_trees = {}
def tree_for(name):
    """BVH of the CLIPS[name]['ref'] surfaces (e.g. the whole brain surface), for distance trimming."""
    if name not in _trees:
        dg = bpy.context.evaluated_depsgraph_get(); verts, polys = [], []
        for ob in bpy.data.objects:
            if HELPER.search(ob.name) or not CLIPS[name]["ref"](ob, path_of(ob)):
                continue
            me = ob.evaluated_get(dg).to_mesh(); base = len(verts)
            verts += [ob.matrix_world @ v.co for v in me.vertices]
            polys += [[base + i for i in p.vertices] for p in me.polygons]
            ob.evaluated_get(dg).to_mesh_clear()
        _trees[name] = BVHTree.FromPolygons(verts, polys)
    return _trees[name]

def keep_near(me, tree, dist):
    """Drop the parts of a mesh farther than dist from the reference surface (cranial nerves past the skull base)."""
    bm = bmesh.new(); bm.from_mesh(me)
    far = [v for v in bm.verts if tree.find_nearest(v.co, dist)[0] is None]
    bmesh.ops.delete(bm, geom=far, context="VERTS")
    bm.to_mesh(me); bm.free()
    return me

def clean(me):
    me.materials.clear()
    while me.uv_layers:
        me.uv_layers.remove(me.uv_layers[0])
    while me.color_attributes:
        me.color_attributes.remove(me.color_attributes[0])
    return me

def export(layer, cfg):
    bres, ures = cfg.get("tube", (BEVEL_RES, CURVE_RES))
    for cu in bpy.data.curves:            # tube resolution for this layer (never above Z-Anatomy's own)
        ob_res = CURVE_ORIG.get(cu.name, (cu.bevel_resolution, cu.resolution_u))
        cu.bevel_resolution, cu.resolution_u = min(ob_res[0], bres), min(ob_res[1], ures)
    dg = bpy.context.evaluated_depsgraph_get(); dg.update()
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
        if cfg.get("clip"):
            clip(me, *box_for(cfg["clip"]))
        if cfg.get("near"):
            keep_near(me, tree_for(cfg["near"][0]), cfg["near"][1])
        if len(me.polygons) < 4:          # label points, stubs, and pieces wholly outside a clip box
            bpy.data.meshes.remove(me); continue
        add(base, side, me)
    if cfg.get("bp3d"):                   # BodyParts3D parts that Z-Anatomy lacks
        for fj, name in bp3d_elements(cfg["bp3d"]["concept"], cfg["bp3d"]["name"]):
            me = bp3d_mesh(fj, name)
            if cfg.get("clip"):
                clip(me, *box_for(cfg["clip"]))
            add(name, "", me)
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
CURVE_ORIG = {cu.name: (cu.bevel_resolution, cu.resolution_u) for cu in bpy.data.curves}
for layer, cfg in LAYERS.items():
    if not ONLY or layer in ONLY:
        export(layer, cfg)
