"""List every object in a Blender file with its collection path, type, size and modifiers.

Run headless (from the repo root), with embedded-script autorun disabled:
  blender -b --factory-startup -Y work/zanatomy/Z-Anatomy/Startup.blend --python tools/list_objects.py -- work/objects.tsv
Writes a tab-separated file; also prints the collection tree and per-collection counts.
"""
import sys
import bpy

out = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "objects.tsv"

# collection -> "Parent/Child/..." path
paths = {}
def walk(coll, prefix):
    for ch in coll.children:
        p = f"{prefix}/{ch.name}" if prefix else ch.name
        paths.setdefault(ch.name, p)
        walk(ch, p)
for sc in bpy.data.scenes:
    walk(sc.collection, "")

dg = bpy.context.evaluated_depsgraph_get()
def tris_of(ob):
    """Triangles after modifiers/bevel, i.e. what an export would produce."""
    try:
        me = ob.evaluated_get(dg).to_mesh()
    except RuntimeError:
        return ""
    n = sum(len(p.vertices) - 2 for p in me.polygons) if me else 0
    ob.evaluated_get(dg).to_mesh_clear()
    return str(n)

rows = []
for ob in bpy.data.objects:
    colls = [paths.get(c.name, c.name) for c in ob.users_collection]
    verts = len(ob.data.vertices) if ob.type == "MESH" else ""
    mods = ",".join(f"{m.type}" for m in getattr(ob, "modifiers", []))
    props = ",".join(k for k in ob.keys() if not k.startswith("_"))
    curve = ""
    if ob.type == "CURVE":
        cu = ob.data
        pts = sum(len(s.points) + len(s.bezier_points) for s in cu.splines)
        curve = (f"pts={pts} splines={len(cu.splines)} bevel={cu.bevel_depth:.4f} bres={cu.bevel_resolution} "
                 f"ures={cu.resolution_u} mode={cu.bevel_mode} bobj={cu.bevel_object.name if cu.bevel_object else ''} "
                 f"taper={cu.taper_object.name if cu.taper_object else ''} extrude={cu.extrude:.4f}")
    tris = tris_of(ob) if ob.type in ("MESH", "CURVE") else ""
    rows.append([ob.name, ob.type, ";".join(colls), str(verts), ob.parent.name if ob.parent else "",
                 mods, props, str(ob.hide_viewport), str(ob.hide_render), ob.data.name if ob.data else "", tris, curve])

with open(out, "w", encoding="utf-8") as f:
    f.write("name\ttype\tcollections\tverts\tparent\tmodifiers\tprops\thide_viewport\thide_render\tdata\ttris\tcurve\n")
    for r in sorted(rows, key=lambda r: (r[2], r[0])):
        f.write("\t".join(x.replace("\t", " ") for x in r) + "\n")

print(f"objects: {len(rows)}  -> {out}")
print(f"texts embedded in file (not run): {[t.name for t in bpy.data.texts]}")
print("--- collection tree (direct object count / mesh verts)")
for name, p in sorted(paths.items(), key=lambda kv: kv[1]):
    c = bpy.data.collections.get(name)
    if c is None:
        continue
    n = len(c.objects)
    v = sum(len(o.data.vertices) for o in c.objects if o.type == "MESH")
    depth = p.count("/")
    if depth <= 3:
        print(f"{'  ' * depth}{name}  [{n} obj, {v} verts]")
