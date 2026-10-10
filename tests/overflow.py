"""Checks every screen for horizontal overflow at 360, 390 and 412 px (phone widths; 412 = her Galaxy S25 Ultra).
Served over HTTP (tests/serve.py). Run from repo root after `python build.py`:
    python tests/overflow.py"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from serve import start

URL = start() + "index.html"
JS = """()=>{const W=document.documentElement.clientWidth;const out=[];document.querySelectorAll('body *').forEach(e=>{const r=e.getBoundingClientRect();if(r.width&&r.right>W+1&&!e.closest('.scrollx')&&!e.closest('svg')&&getComputedStyle(e).position!=='fixed'&&getComputedStyle(e).overflowX!=='auto'&&!e.closest('.labs')){out.push(e.tagName.toLowerCase()+(e.className&&typeof e.className==='string'?'.'+e.className.trim().split(/\\s+/).join('.'):'')+' right='+Math.round(r.right));}});return out.slice(0,6);}"""
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (360, 390, 412):
        ctx = b.new_context(viewport={"width": w, "height": 800}, has_touch=True, is_mobile=True); pg = ctx.new_page()
        pg.goto(URL); pg.wait_for_selector("body[data-ready]", timeout=30000); pg.wait_for_timeout(200)
        def chk(label):
            global bad
            out = pg.evaluate(JS)
            if out: bad += 1; print(f"OVERFLOW {w}px {label}: {out}")
        click = lambda s: pg.evaluate(f"document.querySelector(\"{s}\").click()") or pg.wait_for_timeout(150)
        chk("home")
        click("[data-act=settings]"); chk("settings sheet"); click("[data-act=sheet-close]")
        click("[data-tab=practice]")
        for sub in ["new", "library", "history", "takeaways"]: click(f"[data-act=ptab][data-v={sub}]"); chk("practice/" + sub)
        click("[data-tab=anatomy]")
        for sub in ["body", "brain", "heart", "index", "bones"]: click(f"[data-act=atab][data-v={sub}]"); chk("anatomy/" + sub)
        click("[data-act=atab][data-v=body]"); click("[data-act=body-mode][data-v='3d']"); chk("anatomy/body-3d"); click("[data-act=body-mode][data-v='2d']")
        for sc in ("brain", "heart"): click(f"[data-act=atab][data-v={sc}]"); click(f"[data-act=scene-mode][data-scene={sc}][data-v='3d']"); chk(f"anatomy/{sc}-3d"); click(f"[data-act=scene-mode][data-scene={sc}][data-v='2d']")
        click("[data-tab=progress]"); chk("progress")
        click("[data-act=exam][data-v=mcat]"); chk("mcat/progress")
        click("[data-tab=home]"); chk("mcat/home")
        click("[data-tab=practice]"); chk("mcat/practice")
        click("[data-act=exam][data-v=boards]")
        click("[data-tab=home]"); click("[data-act=quick][data-mode=tutor]"); chk("question runner")
        ctx.close()
    b.close()
print("no horizontal overflow" if not bad else f"{bad} screen(s) overflow")
sys.exit(1 if bad else 0)
