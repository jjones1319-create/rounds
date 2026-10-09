"""3D body test at phone size. The 3D view loads ES modules, so it needs http:// (not file://); this script
serves the repo itself, gzipping like GitHub Pages does. Run from repo root after `python build.py`:
    python tests/three_d.py                      # checks only
    python tests/three_d.py --timing             # also time loading on emulated phones on 4G
    python tests/three_d.py --url https://jjones1319-create.github.io/rounds/ --timing   # the live site
    python tests/three_d.py --shots work/shots   # save screenshots
Exits non-zero on any page error or failed check."""
import argparse, collections, gzip, http.server, io, json, re, struct, sys, threading
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
ap = argparse.ArgumentParser()
ap.add_argument("--url"); ap.add_argument("--timing", action="store_true"); ap.add_argument("--shots")
a = ap.parse_args()

class Handler(http.server.SimpleHTTPRequestHandler):
    extensions_map = {**http.server.SimpleHTTPRequestHandler.extensions_map, ".js": "text/javascript", ".json": "application/json",
                      ".glb": "model/gltf-binary", ".html": "text/html; charset=utf-8"}
    def __init__(self, *args, **kw): super().__init__(*args, directory=str(ROOT), **kw)
    def log_message(self, *args): pass
    def send_head(self):   # gzip text, JS and models when the browser accepts it (GitHub Pages does the same)
        path = Path(self.translate_path(self.path))
        if path.is_dir(): path = path / "index.html"
        if "gzip" not in self.headers.get("Accept-Encoding", "") or not path.is_file() or path.suffix not in (".html", ".js", ".json", ".glb"):
            return super().send_head()
        body = gzip.compress(path.read_bytes(), 6)
        self.send_response(200); self.send_header("Content-Type", self.guess_type(str(path)))
        self.send_header("Content-Encoding", "gzip"); self.send_header("Content-Length", str(len(body))); self.end_headers()
        return io.BytesIO(body)

if a.url:
    URL = a.url
else:
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    URL = f"http://127.0.0.1:{srv.server_address[1]}/index.html"

errs, fails = [], []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  ({detail})" if detail else ""))
    if not ok: fails.append(name)
shots = Path(a.shots) if a.shots else None
if shots: shots.mkdir(parents=True, exist_ok=True)

# ---- data/mesh_map.json against the model files and the app's cards (no browser needed)
src = (ROOT / "src/content.js").read_text(encoding="utf-8") + (ROOT / "src/models.js").read_text(encoding="utf-8")
INFO_LAYER = dict(re.findall(r'^\s*"?([a-z_0-9]+)"?:\s*\{\s*n:\s*"[^"]+",\s*L:\s*"([a-z]+)"', src, re.M))
SCENES = json.loads((ROOT / "data/mesh_map.json").read_text(encoding="utf-8"))["scenes"]
MAP = SCENES["body"]["layers"]
# brain and heart cards are Index ids: br_<BRAIN item>, cn_<numeral>, ht_<HEART item>
models_js = (ROOT / "src/models.js").read_text(encoding="utf-8")
brain_src = models_js[models_js.index("const BRAIN"):models_js.index("const HEART")]
heart_src = models_js[models_js.index("const HEART"):]
heart_src = heart_src[:heart_src.index("\n};")]
SCENE_KEYS = {"brain": {"br_" + i for i in re.findall(r'\{\s*id:\s*"([a-z_]+)"', brain_src)} | {"cn_" + n for n in re.findall(r'num:\s*"([IVX]+)"', src)},
              "heart": {"ht_" + i for i in re.findall(r'\{\s*id:\s*"([a-z_]+)"', heart_src)}}
problems, covered = [], set()
for scene, layers in SCENES.items():
  for layer, cfg in layers["layers"].items():
    blob = (ROOT / cfg["file"]).read_bytes(); n = struct.unpack_from("<I", blob, 12)[0]
    nodes = json.loads(blob[20:20 + n])["nodes"]
    have = {(nd["extras"]["n"], nd["extras"]["s"]) for nd in nodes if "mesh" in nd}
    names, seen = {x for x, _ in have}, collections.Counter()
    size = (ROOT / cfg["file"]).stat().st_size
    if size > 15 * 1048576: problems.append(f"{cfg['file']} is {size / 1048576:.1f} MB (limit ~15 MB)")
    for key, lst in cfg["cards"].items():
        covered.add(key)
        if scene == "body" and INFO_LAYER.get(key) != layer: problems.append(f"{key}: card layer {INFO_LAYER.get(key)} != {layer}")
        if scene != "body" and key not in SCENE_KEYS[scene]: problems.append(f"{scene}/{key}: no such card")
        for nm in lst:
            seen[nm] += 1
            base, side = (nm[:-2], nm[-1].upper()) if re.search(r"\.(l|r)$", nm) else (nm, None)
            if base not in names or (side and (base, side) not in have): problems.append(f"{scene}/{layer}/{key}: no mesh '{nm}'")
    problems += [f"{scene}/{layer}: '{nm}' is in {c} cards" for nm, c in seen.items() if c > 1]
body_cards = {k for k, L in INFO_LAYER.items() if L in MAP}
# index.html's version stamps must match the files, or browsers may keep stale 3D files (rebuild with build.py)
import hashlib
vh = lambda f: hashlib.sha256((ROOT / f).read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:10]
stamps = json.loads(re.search(r"const ASSET_V = (\{.*?\});", (ROOT / "index.html").read_text(encoding="utf-8")).group(1))
want = {"body3d": vh("js/body3d.js"), "map": vh("data/mesh_map.json"), **{c["file"]: vh(c["file"]) for sc in SCENES.values() for c in sc["layers"].values()}}
check("index.html version stamps are current", stamps == want, ", ".join(k for k in want if stamps.get(k) != want[k]) or "")
nb = len(covered & body_cards); nbr = len(covered & SCENE_KEYS["brain"]); nh = len(covered & SCENE_KEYS["heart"])
check("mesh map matches models and cards", not problems, "; ".join(problems[:5]) or
      f"3D cards: body {nb}/{len(body_cards)}, brain {nbr}/{len(SCENE_KEYS['brain'])}, heart {nh}/{len(SCENE_KEYS['heart'])}")

def open_3d(pg):
    ev = pg.evaluate
    ev("document.querySelector('[data-tab=anatomy]').click()"); pg.wait_for_timeout(300)
    ev("document.querySelector('[data-act=body-mode][data-v=\"3d\"]').click()")
    pg.wait_for_selector("#load3d", state="hidden", timeout=120000)
    pg.wait_for_timeout(300)
def idle(pg):   # wait for any layer download to finish
    pg.wait_for_selector("#status3d", state="hidden", timeout=120000); pg.wait_for_timeout(300)
def card(pg):
    t = pg.inner_text("#infocard"); return t, (t.split("\n")[1] if "\n" in t else t)
def search(pg, q):
    pg.fill("#bsearch", q); pg.wait_for_timeout(150); pg.click("#bresults button"); pg.wait_for_timeout(500)
def chip(pg, layer):
    pg.evaluate(f"document.querySelector('[data-act=layer][data-v={layer}]').click()"); pg.wait_for_timeout(200)
def pressed(pg, layer): return pg.get_attribute(f"[data-act=layer][data-v={layer}]", "aria-pressed") == "true"

# Her phone: Galaxy S25 Ultra (Chrome: 412 x 891 CSS px, 3.5x; Snapdragon 8 Elite, Adreno 830). No CPU slowdown.
PHONE = dict(viewport={"width": 412, "height": 891}, device_scale_factor=3.5, has_touch=True, is_mobile=True)
ARGS = ["--enable-unsafe-swiftshader", "--use-angle=swiftshader", "--ignore-gpu-blocklist"]
MOD = "(await import('./js/body3d.js?v=' + ASSET_V.body3d))"   # same URL as the app, so the same module instance
B3 = MOD + ".viewer('body')"
with sync_playwright() as p:
    b = p.chromium.launch(args=ARGS)
    ctx = b.new_context(**PHONE)
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and not m.text.startswith("Failed to load resource") else None)
    pg.on("requestfailed", lambda r: errs.append("request failed: " + r.url) if "fonts.g" not in r.url else None)
    asked = []
    pg.on("request", lambda r: asked.append(r.url) if re.search(r"/(js/body3d\.js|data/mesh_map\.json|models/\w+\.glb)", r.url) else None)
    pg.goto(URL); pg.wait_for_timeout(500)
    ev = pg.evaluate
    ev("document.querySelector('[data-tab=anatomy]').click()"); pg.wait_for_timeout(300)
    check("3D | Diagram switch on Body tab", bool(pg.query_selector("[data-act=body-mode][data-v='3d']")) and bool(pg.query_selector("[data-act=body-mode][data-v='2d'][aria-pressed=true]")))
    check("Diagram is the default view", bool(pg.query_selector("#fig .st")))
    open_3d(pg)
    unstamped = [u for u in asked if "?v=" not in u]
    check("3D files are requested with version stamps", asked and not unstamped, ", ".join(u.split("/")[-1] for u in unstamped[:3]) or f"{len(asked)} requests")
    st = ev(f"async () => {B3}.stats")
    lay = st["layers"]
    check("3D opens with the Diagram's layers (skeleton, organs)", set(lay) == {"bone", "organ"} and not pg.query_selector("[data-act=layer][data-v=derm]"),
          ", ".join(f"{k} {v['meshes']} meshes" for k, v in lay.items()))
    px = ev(f"async () => {B3}.debugDrawnPixels()")
    check("model is drawn", px["drawn"] > px["total"] * 0.02, f"{100 * px['drawn'] / px['total']:.1f}% of canvas")
    if shots: pg.screenshot(path=str(shots / "3d-front.png"))
    fr, fl = ev(f"async () => {B3}.debugProject('Femur', 'R')"), ev(f"async () => {B3}.debugProject('Femur', 'L')")
    check("front view: their right is on your left", fr["x"] < fl["x"] and fr["world"][0] < 0, f"right femur x={fr['x']:.0f}, left x={fl['x']:.0f}")
    pg.touchscreen.tap(fr["x"], fr["y"]); pg.wait_for_timeout(500)
    t, h = card(pg)
    check("tap femur opens the femur card", t.startswith("Skeleton") and "Right femur" in t and "Clinical pearl" in t, h)
    box = pg.query_selector("#fig3d").bounding_box()
    pg.touchscreen.tap(box["x"] + 20, box["y"] + box["height"] - 60); pg.wait_for_timeout(300)
    check("tap empty space clears", "Tap any structure" in pg.inner_text("#infocard"))
    li = ev(f"async () => {B3}.debugProject('Liver')")
    pg.touchscreen.tap(li["x"], li["y"]); pg.wait_for_timeout(400)
    t, h = card(pg)
    check("tap an organ opens its card", t.startswith("Organs") and "Liver" in h, h)
    chip(pg, "organ")
    l3 = ev(f"async () => {B3}.debugProject('Vertebra L3')")
    pg.touchscreen.tap(l3["x"], l3["y"]); pg.wait_for_timeout(400)
    t, h = card(pg)
    check("organs off: tap a vertebra opens its group card", "Lumbar vertebrae" in t, h)
    chip(pg, "muscle"); idle(pg)
    check("muscle layer loads when switched on", ev(f"async () => {B3}.loaded('muscle')") and pressed(pg, "muscle"))
    bi = ev(f"async () => {B3}.debugProject('Long head of biceps brachii', 'R')")
    pg.touchscreen.tap(bi["x"], bi["y"]); pg.wait_for_timeout(400)
    t, h = card(pg)
    check("tap a muscle opens its card", t.startswith("Muscles") and "biceps brachii" in h.lower(), h)
    if shots: pg.screenshot(path=str(shots / "3d-muscles.png"))
    ev("document.querySelector('[data-act=zoom-fit]').click()"); pg.wait_for_timeout(500)
    search(pg, "aorta"); idle(pg)
    t, h = card(pg)
    check("search loads the artery layer and shows the aorta", "Aorta" in h and pressed(pg, "artery") and bool(pg.query_selector("#fig3d canvas")), h)
    if shots: pg.screenshot(path=str(shots / "3d-aorta.png"))
    search(pg, "brachial plexus"); idle(pg)
    t, h = card(pg)
    check("search loads nerves and shows the brachial plexus", "brachial plexus" in h.lower() and pressed(pg, "nerve"), h)
    search(pg, "axillary lymph"); idle(pg)
    t, h = card(pg)
    check("search loads lymphatics and shows axillary nodes", "axillary lymph nodes" in h.lower() and pressed(pg, "lymph"), h)
    ev("document.querySelector('[data-act=id-quiz]').click()"); pg.wait_for_timeout(800)
    t, h = card(pg)
    ok = "Name that structure" in t and bool(pg.query_selector("#fig3d canvas"))
    ev("document.querySelector('[data-act=id-pick]').click()"); pg.wait_for_timeout(300)
    t2 = pg.inner_text("#infocard")
    check("Name that structure runs in 3D", ok and ("Correct." in t2 or "Not quite." in t2), t2.split("\n")[-1][:60])
    ev("document.querySelector('[data-act=id-quiz-stop]').click()"); pg.wait_for_timeout(300)
    ev("document.querySelector('[data-act=layers-all]').click()"); idle(pg)
    st = ev(f"async () => {B3}.stats")
    check("All layers loads all seven", len(st["layers"]) == 7 and all(st["layers"][k]["meshes"] for k in st["layers"]),
          f"{st['meshes']} meshes, {round(st['triangles'] / 1000)}k triangles")
    if shots: pg.screenshot(path=str(shots / "3d-all.png"))
    search(pg, "uterus"); pg.wait_for_timeout(500)
    check("no 3D match (uterus) falls back to Diagram", bool(pg.query_selector("#fig .st")) and "uterus" in pg.inner_text("#infocard").lower())
    ev("document.querySelector('[data-act=body-mode][data-v=\"3d\"]').click()"); pg.wait_for_timeout(500)
    check("back to 3D reuses the loaded model", pg.is_hidden("#load3d") and bool(pg.query_selector("#fig3d canvas")))
    ev("document.querySelector('[data-act=atab][data-v=bones]').click()"); pg.wait_for_timeout(200)
    ev("document.querySelector('[data-act=show-fig][data-fig=femur]').click()"); pg.wait_for_timeout(800)
    check("Bones tab 'Show on the body' opens 3D femur", "femur" in pg.inner_text("#infocard").lower() and bool(pg.query_selector("#fig3d canvas")))
    ev("document.querySelector('[data-act=atab][data-v=index]').click()"); pg.wait_for_timeout(200)
    pg.fill("#idxsearch", "great saphenous"); pg.wait_for_timeout(200); ev("document.querySelector('#idxlist [data-act=dict-go]').click()"); idle(pg)
    check("Index jumps to a 3D vein", "great saphenous" in pg.inner_text("#infocard").lower() and bool(pg.query_selector("#fig3d canvas")))

    # ---- Brain tab in 3D
    BV, HV = MOD + ".viewer('brain')", MOD + ".viewer('heart')"
    def index_go(q):
        ev("document.querySelector('[data-act=atab][data-v=index]').click()"); pg.wait_for_timeout(200)
        pg.fill("#idxsearch", q); pg.wait_for_timeout(200); ev("document.querySelector('#idxlist [data-act=dict-go]').click()"); pg.wait_for_timeout(1200)
    def scene_3d(sc):
        ev(f"document.querySelector('[data-act=atab][data-v={sc}]').click()"); pg.wait_for_timeout(300)
        ev(f"document.querySelector('[data-act=scene-mode][data-scene={sc}][data-v=\"3d\"]').click()")
        pg.wait_for_selector(f"#load3d-{sc}", state="hidden", timeout=120000); pg.wait_for_timeout(400)
    scene_3d("brain")
    st = ev(f"async () => {BV}.stats")
    check("Brain 3D loads cortex, deep brain, arteries and cranial nerves", set(st["layers"]) == {"cortex", "deep", "artery", "nerve"},
          f"{st['meshes']} meshes, {round(st['triangles'] / 1000)}k triangles")
    if shots: pg.screenshot(path=str(shots / "3d-brain.png"))
    pc = ev(f"async () => {BV}.debugProject('Precentral gyrus', 'L')")
    pg.touchscreen.tap(pc["x"], pc["y"]); pg.wait_for_timeout(400)
    t = pg.inner_text("#card3d-brain")
    check("tap the precentral gyrus opens the motor cortex card", "Primary motor cortex" in t and "Left" in t, t.split("\n")[1] if "\n" in t else t)
    ev("document.querySelector('[data-act=brain-side][data-v=L]').click()"); pg.wait_for_timeout(700)
    hidden = ev(f"async () => {BV}.debugProject('Precentral gyrus', 'R')") is None
    cc = ev(f"async () => {BV}.debugProject('Corpus callosum')")
    check("Left hemisphere only: right side hidden, midline kept", hidden and cc is not None)
    if shots: pg.screenshot(path=str(shots / "3d-brain-medial.png"))
    ev("document.querySelector('[data-act=brain-side][data-v=\"\"]').click()"); pg.wait_for_timeout(500)
    index_go("oculomotor")
    t = pg.inner_text("#card3d-brain") if pg.query_selector("#card3d-brain") else ""
    check("Index jumps to a cranial nerve in 3D", "CN III" in t, t.split("\n")[1] if "\n" in t else t)
    index_go("broca")
    t = pg.inner_text("#card3d-brain") if pg.query_selector("#card3d-brain") else ""
    check("Index jumps to Broca area (left hemisphere) in 3D", "Broca area" in t and "Left" in t)
    index_go("arcuate")
    check("no 3D match (arcuate fasciculus) falls back to the brain Diagram", bool(pg.query_selector("#brainwrap")) and "Arcuate fasciculus" in pg.inner_text("#braincard"))
    ev("document.querySelector('[data-act=scene-mode][data-scene=brain][data-v=\"3d\"]').click()"); pg.wait_for_selector("#load3d-brain", state="hidden", timeout=60000); pg.wait_for_timeout(300)
    ev("document.querySelector('[data-act=q3-start][data-scene=brain]').click()"); pg.wait_for_timeout(800)
    ev("document.querySelector('[data-act=q3-pick]').click()"); pg.wait_for_timeout(300)
    t = pg.inner_text("#card3d-brain")
    check("Name that structure runs in the 3D brain", "Correct." in t or "Not quite." in t)
    ev("document.querySelector('[data-act=q3-stop]').click()"); pg.wait_for_timeout(200)

    # ---- Heart tab in 3D
    scene_3d("heart")
    st = ev(f"async () => {HV}.stats")
    check("Heart 3D loads all five layers", set(st["layers"]) == {"wall", "valves", "coronary", "veins", "vessels"},
          f"{st['meshes']} meshes, {round(st['triangles'] / 1000)}k triangles")
    if shots: pg.screenshot(path=str(shots / "3d-heart.png"))
    lv = ev(f"async () => {HV}.debugProject('Left ventricle')")
    pg.touchscreen.tap(lv["x"] + 25, lv["y"] + 40); pg.wait_for_timeout(400)
    t = pg.inner_text("#card3d-heart")
    check("tap a ventricle opens its card", "ventricle" in t.lower(), t.split("\n")[1] if "\n" in t else t)
    ev("const r = document.querySelector('#heartcut'); r.value = 55; r.dispatchEvent(new Event('input', { bubbles: true }))"); pg.wait_for_timeout(500)
    check("Cut open slider cuts the heart", abs((ev(f"async () => {HV}.cut()") or 0) - 0.55) < 0.01 and pg.inner_text("#heartcutv") == "55%")
    if shots: pg.screenshot(path=str(shots / "3d-heart-cut.png"))
    ml = ev(f"async () => {HV}.debugProject('Anterior leaflet of mitral valve')")
    pg.touchscreen.tap(ml["x"], ml["y"]); pg.wait_for_timeout(400)
    t = pg.inner_text("#card3d-heart")
    check("cut open: tap reaches an inner structure", any(w in t for w in ("Mitral valve", "Aortic valve", "Papillary", "Left atrium", "Left ventricle", "leaflet")),
          t.split("\n")[1] if "\n" in t else t)
    ev("const r = document.querySelector('#heartcut'); r.value = 0; r.dispatchEvent(new Event('input', { bubbles: true }))"); pg.wait_for_timeout(300)
    index_go("aortic valve")
    t = pg.inner_text("#card3d-heart") if pg.query_selector("#card3d-heart") else ""
    check("Index jumps to the aortic valve in 3D", "Aortic valve" in t)
    index_go("sinoatrial")
    check("no 3D match (SA node) falls back to the heart Diagram", bool(pg.query_selector("#heartwrap")) and "Sinoatrial node" in pg.inner_text("#heartcard"))
    ev("document.querySelector('[data-act=scene-mode][data-scene=heart][data-v=\"3d\"]').click()"); pg.wait_for_selector("#load3d-heart", state="hidden", timeout=60000); pg.wait_for_timeout(300)
    ev("document.querySelector('[data-act=q3-start][data-scene=heart]').click()"); pg.wait_for_timeout(800)
    ev("document.querySelector('[data-act=q3-pick]').click()"); pg.wait_for_timeout(300)
    t = pg.inner_text("#card3d-heart")
    check("Name that structure runs in the 3D heart", "Correct." in t or "Not quite." in t)
    pg.reload(); pg.wait_for_timeout(600)
    ev("document.querySelector('[data-tab=anatomy]').click()"); pg.wait_for_timeout(200)
    ev("document.querySelector('[data-act=atab][data-v=brain]').click()"); pg.wait_for_timeout(300)
    check("3D choice is remembered after a reload", bool(pg.query_selector("[data-act=scene-mode][data-scene=brain][data-v='3d'][aria-pressed=true]")) and bool(pg.query_selector("#fig3d-brain")))
    ctx.close()

    # A stale cached viewer must ask for a reload; a failed download must offer "Try again" and recover.
    ctx = b.new_context(**PHONE); pg = ctx.new_page()
    body3d = (ROOT / "js/body3d.js").read_text(encoding="utf-8")
    pg.route("**/js/body3d.js*", lambda r: r.fulfill(status=200, content_type="text/javascript", body=re.sub(r"export const API = \d+;", "export const API = 1;", body3d)))
    open_3d_no_wait = lambda: (pg.goto(URL), pg.wait_for_timeout(400), pg.evaluate("document.querySelector('[data-tab=anatomy]').click()"),
                               pg.evaluate("document.querySelector('[data-act=body-mode][data-v=\"3d\"]').click()"), pg.wait_for_timeout(1500))
    open_3d_no_wait()
    check("stale viewer shows a Reload prompt", bool(pg.query_selector("#load3d [data-act=reload-app]")), pg.inner_text("#load3d")[:60])
    pg.unroute("**/js/body3d.js*")
    ctx.close(); ctx = b.new_context(**PHONE); pg = ctx.new_page()
    pg.route("**/models/organs.glb*", lambda r: r.abort())
    open_3d_no_wait(); pg.wait_for_selector("#load3d [data-act=body3d-retry]", timeout=60000)
    pg.unroute("**/models/organs.glb*")
    pg.evaluate("document.querySelector('[data-act=body3d-retry]').click()")
    pg.wait_for_selector("#load3d", state="hidden", timeout=60000)
    check("failed download offers Try again, which recovers", pg.evaluate(f"async () => {B3}.loaded('organ')"))
    ctx.close()

    if a.timing:
        # Her phone on 4G (software rendering here, so fps is not meaningful; load time is).
        nets = [("fast 4G (9 Mbps, 60 ms)", 9e6, 60), ("slow 4G (1.6 Mbps, 150 ms)", 1.6e6, 150)]
        for label, bps, rtt in nets:
            ctx = b.new_context(**PHONE)
            pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
            cdp.send("Network.enable"); cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
            cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": rtt, "downloadThroughput": bps / 8, "uploadThroughput": 750e3 / 8})
            pg.goto(URL); pg.wait_for_timeout(300)
            open_3d(pg)
            st = pg.evaluate(f"async () => {B3}.stats")
            first = (st["tFirstFrame"] - st["tTap"]) / 1000
            mb = sum(l["transfer"] for l in st["layers"].values()) / 1048576
            t0 = pg.evaluate("performance.now()")
            pg.evaluate("document.querySelector('[data-act=layer][data-v=muscle]').click()"); idle(pg)
            musc = (pg.evaluate("performance.now()") - t0) / 1000
            st = pg.evaluate(f"async () => {B3}.stats")
            print(f"TIMING S25 Ultra, {label}: 3D (skeleton + organs, {mb:.2f} MB) ready {first:.1f} s after tapping 3D; "
                  f"muscles ({st['layers']['muscle']['transfer'] / 1048576:.2f} MB) +{musc:.1f} s")
            for sc in ("brain", "heart"):
                pg.evaluate(f"document.querySelector('[data-act=atab][data-v={sc}]').click()"); pg.wait_for_timeout(200)
                t0 = pg.evaluate("performance.now()")
                pg.evaluate(f"document.querySelector('[data-act=scene-mode][data-scene={sc}][data-v=\"3d\"]').click()")
                pg.wait_for_selector(f"#load3d-{sc}", state="hidden", timeout=180000)
                secs = (pg.evaluate("performance.now()") - t0) / 1000
                sst = pg.evaluate(f"async () => {MOD}.viewer('{sc}').stats")
                print(f"TIMING S25 Ultra, {label}: {sc} 3D ({sum(l['transfer'] for l in sst['layers'].values()) / 1048576:.2f} MB) ready {secs:.1f} s after tapping 3D")
            ctx.close()
    b.close()
check("no page errors", not errs)
if errs: print("\n".join(errs))
sys.exit(1 if fails else 0)
