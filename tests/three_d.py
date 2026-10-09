"""3D body test at phone size. The 3D view loads ES modules, so it needs http:// (not file://); this script
serves the repo itself, gzipping like GitHub Pages does. Run from repo root after `python build.py`:
    python tests/three_d.py                      # checks only
    python tests/three_d.py --timing             # also time loading on emulated phones on 4G
    python tests/three_d.py --url https://jjones1319-create.github.io/rounds/ --timing   # the live site
    python tests/three_d.py --shots work/shots   # save screenshots
Exits non-zero on any page error or failed check."""
import argparse, gzip, http.server, io, sys, threading
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

def open_3d(pg):
    ev = pg.evaluate
    ev("document.querySelector('[data-tab=anatomy]').click()"); pg.wait_for_timeout(300)
    ev("document.querySelector('[data-act=body-mode][data-v=\"3d\"]').click()")
    pg.wait_for_selector("#load3d", state="hidden", timeout=120000)
    pg.wait_for_timeout(300)

ARGS = ["--enable-unsafe-swiftshader", "--use-angle=swiftshader", "--ignore-gpu-blocklist"]
with sync_playwright() as p:
    b = p.chromium.launch(args=ARGS)
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, has_touch=True, is_mobile=True)
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and not m.text.startswith("Failed to load resource") else None)
    pg.on("requestfailed", lambda r: errs.append("request failed: " + r.url) if "fonts.g" not in r.url else None)
    pg.goto(URL); pg.wait_for_timeout(500)
    ev = pg.evaluate
    ev("document.querySelector('[data-tab=anatomy]').click()"); pg.wait_for_timeout(300)
    check("3D | Diagram switch on Body tab", bool(pg.query_selector("[data-act=body-mode][data-v='3d']")) and bool(pg.query_selector("[data-act=body-mode][data-v='2d'][aria-pressed=true]")))
    check("Diagram is the default view", bool(pg.query_selector("#fig .st")))
    open_3d(pg)
    B3 = "(await import('./js/body3d.js'))"
    st = ev(f"async () => {B3}.stats")
    check("3D skeleton loads", st["meshes"] >= 240, f"{st['meshes']} meshes, {round(st['triangles'] / 1000)}k triangles")
    px = ev(f"async () => {B3}.debugDrawnPixels()")
    check("skeleton is drawn", px["drawn"] > px["total"] * 0.02, f"{100 * px['drawn'] / px['total']:.1f}% of canvas")
    if shots: pg.screenshot(path=str(shots / "3d-front.png"))
    fr, fl = ev(f"async () => {B3}.debugProject('Femur', 'R')"), ev(f"async () => {B3}.debugProject('Femur', 'L')")
    check("front view: their right is on your left", fr["x"] < fl["x"] and fr["world"][0] < 0, f"right femur x={fr['x']:.0f}, left x={fl['x']:.0f}")
    pg.touchscreen.tap(fr["x"], fr["y"]); pg.wait_for_timeout(500)
    card = pg.inner_text("#infocard")
    check("tap femur opens the femur card", card.startswith("Skeleton") and "Right femur" in card and "Clinical pearl" in card, card.split("\n")[1] if "\n" in card else card)
    if shots: pg.screenshot(path=str(shots / "3d-femur.png"))
    box = pg.query_selector("#fig3d").bounding_box()
    pg.touchscreen.tap(box["x"] + 20, box["y"] + box["height"] - 60); pg.wait_for_timeout(300)
    check("tap empty space clears", "Tap any bone" in pg.inner_text("#infocard"))
    l3 = ev(f"async () => {B3}.debugProject('Vertebra L3')")
    pg.touchscreen.tap(l3["x"], l3["y"]); pg.wait_for_timeout(400)
    card = pg.inner_text("#infocard")
    check("tap a vertebra opens its group card", "Lumbar vertebrae" in card or "You tapped" in card, card.split("\n")[1] if "\n" in card else card)
    ev("document.querySelector('[data-act=zoom-fit]').click()"); pg.wait_for_timeout(600)
    pg.fill("#bsearch", "scapula"); pg.wait_for_timeout(150); pg.click("#bresults button"); pg.wait_for_timeout(800)
    check("search selects a bone in 3D", "scapula" in pg.inner_text("#infocard").lower() and bool(pg.query_selector("#fig3d canvas")))
    if shots: pg.screenshot(path=str(shots / "3d-scapula.png"))
    if shots:   # close-ups to judge mesh simplification
        for q, f in [("frontal bone", "3d-skull.png"), ("carpal", "3d-hand.png")]:
            pg.fill("#bsearch", q); pg.wait_for_timeout(150); pg.click("#bresults button"); pg.wait_for_timeout(900)
            pg.screenshot(path=str(shots / f))
    pg.fill("#bsearch", "vagus"); pg.wait_for_timeout(150); pg.click("#bresults button"); pg.wait_for_timeout(800)
    check("non-bone search falls back to Diagram", bool(pg.query_selector("#fig .st")) and "vagus nerve" in pg.inner_text("#infocard").lower())
    ev("document.querySelector('[data-act=body-mode][data-v=\"3d\"]').click()"); pg.wait_for_timeout(400)
    check("back to 3D reuses the loaded model", pg.is_hidden("#load3d") and bool(pg.query_selector("#fig3d canvas")))
    ev("document.querySelector('[data-act=atab][data-v=bones]').click()"); pg.wait_for_timeout(200)
    ev("document.querySelector('[data-act=show-fig][data-fig=femur]').click()"); pg.wait_for_timeout(800)
    check("Bones tab 'Show on the body' opens 3D femur", "femur" in pg.inner_text("#infocard").lower() and bool(pg.query_selector("#fig3d canvas")))
    ev("document.querySelector('[data-act=id-quiz]').click()"); pg.wait_for_timeout(500)
    check("Name that structure runs in Diagram", "Name that structure" in pg.inner_text("#infocard") and bool(pg.query_selector("#fig .st")))
    ctx.close()

    if a.timing:
        # Emulated phones (software rendering here, so fps is not meaningful; load time is).
        nets = [("fast 4G (9 Mbps, 60 ms)", 9e6, 60), ("slow 4G (1.6 Mbps, 150 ms)", 1.6e6, 150)]
        for label, bps, rtt in nets:
            ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, has_touch=True, is_mobile=True)
            pg = ctx.new_page(); cdp = ctx.new_cdp_session(pg)
            cdp.send("Network.enable"); cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
            cdp.send("Network.emulateNetworkConditions", {"offline": False, "latency": rtt, "downloadThroughput": bps / 8, "uploadThroughput": 750e3 / 8})
            cdp.send("Emulation.setCPUThrottlingRate", {"rate": 4})
            pg.goto(URL); pg.wait_for_timeout(300)
            open_3d(pg)
            st = pg.evaluate(f"async () => {B3}.stats")
            res = pg.evaluate("""() => performance.getEntriesByType('resource').filter(r => /vendor\\/three|body3d|skeleton\\.glb|mesh_map/.test(r.name))
                                 .map(r => ({n: r.name.split('/').pop(), t: r.transferSize, e: r.encodedBodySize, d: r.decodedBodySize}))""")
            sent = sum(r["e"] for r in res)
            glb = next((r for r in res if r["n"] == "skeleton.glb"), {"e": 0, "d": 0})
            print(f"TIMING {label}, CPU 4x slower: 3D ready {(st['tFirstFrame'] - st['tTap']) / 1000:.1f} s after tapping 3D "
                  f"(model parsed {(st['tLoaded'] - st['tLoadStart']) / 1000:.1f} s after its request started); "
                  f"transferred {sent / 1048576:.2f} MB (model {glb['e'] / 1048576:.2f} MB, unpacked {glb['d'] / 1048576:.2f} MB)")
            ctx.close()
    b.close()
check("no page errors", not errs)
if errs: print("\n".join(errs))
sys.exit(1 if fails else 0)
