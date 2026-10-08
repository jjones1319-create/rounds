"""End-to-end smoke test at phone size. Run from repo root after `python build.py`:
    python tests/smoke.py
Exits non-zero on any page error or failed check."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
URL = (Path(__file__).resolve().parent.parent / "index.html").as_uri()
errs, fails = [], []
def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok: fails.append(name)
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, has_touch=True, is_mobile=True)
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errs.append(str(e)))
    # Resource failures are checked by URL below; Google Fonts may be blocked on some networks (harmless fallback).
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and not m.text.startswith("Failed to load resource") else None)
    pg.on("requestfailed", lambda r: errs.append("request failed: " + r.url) if "fonts.g" not in r.url else None)
    pg.goto(URL); pg.wait_for_timeout(600)
    ev = lambda js: pg.evaluate(js)
    n = ev("JSON.parse(document.getElementById('qbank').textContent).length")
    check(f"question bank loads ({n} questions)", n >= 16)
    # tutor block
    ev("document.querySelector('[data-act=quick][data-mode=tutor]').click()"); pg.wait_for_timeout(300)
    pg.click(".opt[data-l=A]"); pg.click("[data-act=r-submit]"); pg.wait_for_timeout(300)
    check("tutor submit shows verdict", bool(pg.query_selector("#verdict")))
    pg.click(".rbar [data-act=r-exit]"); pg.wait_for_timeout(300)
    # anatomy body + rotation
    ev("document.querySelector('[data-tab=anatomy]').click()"); pg.wait_for_timeout(400)
    check("body figure renders", bool(pg.query_selector("#fig .st")))
    ev("document.querySelector('[data-act=rotate-body]').click()"); pg.wait_for_timeout(800)
    check("rotates to back view", ev("document.querySelector('#fig').dataset.view") == "back")
    pg.fill("#bsearch", "L5"); pg.wait_for_timeout(150); pg.click("#bresults button"); pg.wait_for_timeout(600)
    check("search selects dermatome", "L5 dermatome" in pg.inner_text("#infocard"))
    # brain, heart, index
    for tab, sel in [("brain", ".brainfig"), ("heart", ".heartfig"), ("index", "#idxlist .li"), ("bones", "#bonelist details")]:
        ev(f"document.querySelector('[data-act=atab][data-v={tab}]').click()"); pg.wait_for_timeout(300)
        check(f"{tab} tab renders", bool(pg.query_selector(sel)))
    ev("document.querySelector('[data-act=atab][data-v=index]').click()"); pg.wait_for_timeout(200)
    pg.fill("#idxsearch", "mitral"); pg.wait_for_timeout(200); ev("document.querySelector('#idxlist [data-act=dict-go]').click()"); pg.wait_for_timeout(500)
    check("index jumps to heart model", "Mitral valve" in (pg.inner_text("#heartcard") if pg.query_selector("#heartcard") else ""))
    b.close()
check("no page errors", not errs)
if errs: print("\n".join(errs))
sys.exit(1 if fails else 0)
