"""Export the Z-Anatomy skeleton to an unoptimized glTF binary (Phase 1 of docs/PLAN_3D.md).

Run headless from the repo root, with embedded-script autorun disabled:
  blender -b --factory-startup -Y work/zanatomy/Z-Anatomy/Startup.blend --python tools/export_skeleton.py -- work/skeleton_raw.glb
Then optimize with tools/build_models.sh.

Each exported node is named "<Name>_<R|L>" (spaces -> underscores) and carries extras {"n": Z-Anatomy name,
"s": "R"|"L"|""}. The viewer reads n/s from userData, so node-name sanitizing in three.js does not matter.
"""
import re
import sys
import bpy

out = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "skeleton_raw.glb"
SKELETON = "1: Skeletal system"

# Left out of the skeleton layer, with reasons (see CREDITS.md and docs/PLAN_3D.md §Licensing).
EXCLUDE = {
    # May come from "Anatomy of the Inner Ear" (Univ. of Dundee, CC BY-NC-SA): never ship.
    "Incus", "Malleus", "Stapes",
    # Air spaces modeled as solids: they render as blobs inside the skull.
    "Anterior cells of ethmoid bone", "Middle cells of ethmoid bone", "Posterior cells of ethmoid bone",
    "Sinus of frontal bone", "Sinus of sphenoid bone",
    # Cartilage of the larynx and nose: belongs with later (respiratory) layers.
    "Arytenoid cartilage", "Corniculate cartilage", "Cricoid cartilage", "Thyroid cartilage",
    "Major alar cartilage", "Nasal septal cartilage", "Lateral process of nasal septal cartilage",
}
HELPER = re.compile(r"\.(j|i|g)$")          # label anchors, leader lines, group labels
SIDE = re.compile(r"\.(r|l)$")

def in_skeleton(ob):
    return any(c.name == SKELETON for c in ob.users_collection)

chosen = []
for ob in bpy.data.objects:
    if ob.type != "MESH" or not in_skeleton(ob) or HELPER.search(ob.name) or len(ob.data.vertices) <= 20:
        continue
    base = SIDE.sub("", ob.name)
    if base in EXCLUDE:
        continue
    m = SIDE.search(ob.name)
    chosen.append((ob, base, m.group(1).upper() if m else ""))

dg = bpy.context.evaluated_depsgraph_get()
new_objs = []
for ob, base, side in chosen:
    ev = ob.evaluated_get(dg)
    me = bpy.data.meshes.new_from_object(ev, preserve_all_data_layers=False, depsgraph=dg)
    me.transform(ob.matrix_world)            # bake world transform; exported nodes have identity transforms
    me.materials.clear()
    while me.uv_layers:
        me.uv_layers.remove(me.uv_layers[0])
    while me.color_attributes:
        me.color_attributes.remove(me.color_attributes[0])
    name = re.sub(r"[^A-Za-z0-9]+", "_", base).strip("_") + (f"_{side}" if side else "")
    nob = bpy.data.objects.new(name, me)
    nob["n"] = base
    nob["s"] = side
    bpy.context.scene.collection.objects.link(nob)
    new_objs.append(nob)

for ob in bpy.context.view_layer.objects:
    ob.select_set(False)
for ob in new_objs:
    ob.hide_set(False)
    ob.select_set(True)

bpy.ops.export_scene.gltf(
    filepath=out, export_format="GLB", use_selection=True, export_apply=False, export_yup=True,
    export_materials="NONE", export_texcoords=False, export_normals=True, export_extras=True,
    export_animations=False, export_skins=False, export_morph=False, export_cameras=False, export_lights=False,
)
verts = sum(len(o.data.vertices) for o in new_objs)
tris = sum(sum(len(p.vertices) - 2 for p in o.data.polygons) for o in new_objs)
print(f"exported {len(new_objs)} meshes, {verts} verts, {tris} tris -> {out}")
print("names:", ", ".join(sorted({b for _, b, _ in chosen})))
