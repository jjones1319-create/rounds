"""End-to-end smoke test at phone size, served over HTTP (the app fetches its question banks). Run from repo
root after `python build.py`:
    python tests/smoke.py
Exits non-zero on any page error or failed check."""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from serve import start

URL = start() + "index.html"
errs, fails = [], []
def check(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    if not ok: fails.append(name)

# A boards progress record as the app wrote it before the MCAT work: it must be read, shown, and left byte-for-byte
# unchanged by browsing, and MCAT must never write to it.
SEED = json.dumps({"v": 1, "answers": {"B1-Q01": {"first": {"c": "E", "ok": True, "ts": 1700000000000}, "c": "E", "ok": True, "t": 42, "ts": 1700000000000, "n": 1}},
                   "flags": {"B1-Q02": {"on": True, "ts": 1700000000000}}, "notes": {}, "sessions": [],
                   "settings": {"theme": "dark", "font": 2, "ts": 1700000000000}, "updatedAt": 1700000000000})

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, has_touch=True, is_mobile=True)
    ctx.add_init_script(f"if (!localStorage.getItem('rounds.progress.v1')) localStorage.setItem('rounds.progress.v1', {json.dumps(SEED)});")
    pg = ctx.new_page()
    pg.on("pageerror", lambda e: errs.append(str(e)))
    # Resource failures are checked by URL below; Google Fonts may be blocked on some networks (harmless fallback).
    pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and not m.text.startswith("Failed to load resource") else None)
    pg.on("requestfailed", lambda r: errs.append("request failed: " + r.url) if "fonts.g" not in r.url else None)
    pg.goto(URL); pg.wait_for_selector("body[data-ready]", timeout=30000); pg.wait_for_timeout(200)
    ev = lambda js: pg.evaluate(js)
    stored = lambda key: ev(f"localStorage.getItem('{key}')")
    n = len(pg.query_selector_all(".qcell"))
    check(f"question bank loads ({n} questions)", n >= 24)
    check("saved boards progress is read (1 answered, B1-Q01 correct, B1-Q02 flagged)",
          "1 of" in pg.inner_text(".status-line") and bool(pg.query_selector(".qcell.correct[data-id='B1-Q01']")) and bool(pg.query_selector(".qcell.flagged[data-id='B1-Q02']")))
    check("saved settings applied (dark theme, large text)", ev("document.documentElement.getAttribute('data-theme')") == "dark" and ev("getComputedStyle(document.documentElement).getPropertyValue('--qfs').trim()") == "19px")
    # exam switcher and the MCAT empty states
    check("exam switcher shows Boards selected", bool(pg.query_selector("[data-act=exam][data-v=boards][aria-pressed=true]")))
    ev("document.querySelector('[data-act=exam][data-v=mcat]').click()"); pg.wait_for_timeout(200)
    check("MCAT home lists the four sections as coming soon", pg.inner_text("#view").count("Coming soon") == 4 and "MCAT" in pg.inner_text("#view h1"))
    ev("document.querySelector('[data-tab=practice]').click()"); pg.wait_for_timeout(200)
    check("MCAT practice shows an empty state per section", pg.inner_text("#view").count("No questions yet") == 4)
    ev("document.querySelector('[data-tab=progress]').click()"); pg.wait_for_timeout(200)
    check("MCAT progress shows an empty state", "No MCAT practice yet" in pg.inner_text("#view"))
    check("MCAT theme still dark (settings are shared)", ev("document.documentElement.getAttribute('data-theme')") == "dark")
    pg.reload(); pg.wait_for_selector("body[data-ready]", timeout=30000); pg.wait_for_timeout(200)
    check("exam choice is remembered after a reload", bool(pg.query_selector("[data-act=exam][data-v=mcat][aria-pressed=true]")) and stored("rounds.exam") == "mcat")
    ev("document.querySelector('[data-act=exam][data-v=boards]').click()"); pg.wait_for_timeout(200)
    check("boards progress record is byte-for-byte unchanged after using the MCAT tab", stored("rounds.progress.v1") == SEED)
    check("no MCAT progress record was created by browsing", stored("rounds.mcat.v1") is None)
    # tutor block (as before)
    ev("document.querySelector('[data-tab=home]').click()"); pg.wait_for_timeout(200)
    ev("document.querySelector('[data-act=quick][data-mode=tutor]').click()"); pg.wait_for_timeout(300)
    pg.click(".opt[data-l=A]"); pg.click("[data-act=r-submit]"); pg.wait_for_timeout(300)
    check("tutor submit shows verdict", bool(pg.query_selector("#verdict")))
    pg.click(".rbar [data-act=r-exit]"); pg.wait_for_timeout(300)
    check("the answer was saved under the boards key only", stored("rounds.progress.v1") != SEED and '"answers"' in (stored("rounds.progress.v1") or "") and stored("rounds.mcat.v1") is None)
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
