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
    check("MCAT home lists the four sections, each with a What's tested guide or questions",
          len(pg.query_selector_all("[data-act=msec]")) == 4 and "Coming soon" not in pg.inner_text("#view") and "MCAT" in pg.inner_text("#view h1"))
    ev("document.querySelector('[data-tab=practice]').click()"); pg.wait_for_timeout(200)
    check("MCAT practice lists the four sections", len(pg.query_selector_all("[data-act=msec]")) == 4)
    # the Chem/Phys "What's tested" guide (docs/MCAT_GUIDES_SPEC.md §5)
    ev("document.querySelector('[data-act=msec][data-v=chem_phys]').click()"); pg.wait_for_timeout(300)
    ntop = len(pg.query_selector_all("details.gt[id^='t-']"))
    check(f"Chem/Phys opens on What's tested with the whole content map ({ntop} topics)", bool(pg.query_selector("[data-act=mtab][data-v=guide][aria-pressed=true]")) and ntop >= 90)
    txt = pg.inner_text("#view")
    check("guide shows the attribution, official-outline link and last-verified date", "Descriptions are our own" in txt and "Last verified 20" in txt and bool(pg.query_selector("a[href*='aamc.org']")))
    check("guide has at-a-glance, blueprint, skills, research methods and math toolkit", all(s in txt for s in ("At a glance", "Blueprint", "Skills", "Research methods", "Math toolkit")) and len(pg.query_selector_all(".bar-row")) >= 11)
    pg.click("details.gcat[data-okey='k:4B'] > summary"); pg.wait_for_timeout(150)
    pg.click("[id='t-4B.continuity-bernoulli'] > summary")
    try: pg.wait_for_selector("[id='t-4B.continuity-bernoulli'] .eq .katex", timeout=20000)
    except Exception: pass
    check("equations render with KaTeX (HTML + MathML) in their own scroll box", bool(pg.query_selector("[id='t-4B.continuity-bernoulli'] .eq .katex")) and bool(pg.query_selector("[id='t-4B.continuity-bernoulli'] .eq math")))
    gui = stored("rounds.guide.v1") or ""
    check("expanded groups are remembered", '"k:4B":true' in gui and '"t:4B.continuity-bernoulli":true' in gui)
    pg.fill("[data-gsearch]", "poiseuille"); pg.wait_for_timeout(200)
    hits = pg.query_selector_all("#gbody [data-act=g-go]")
    check("guide search finds topics", len(hits) >= 1 and "Poiseuille" in hits[0].inner_text())
    hits[0].click(); pg.wait_for_timeout(300)
    check("a search result opens that topic", bool(pg.query_selector("[id='t-4B.viscosity-poiseuille'][open]")) and ev("document.querySelector('[data-gsearch]').value") == "")
    check("'Practice this topic' stays hidden while a topic has no questions", not pg.query_selector("[id='t-4B.viscosity-poiseuille'] [data-act=g-practice]") and "No questions yet" in pg.inner_text("[id='t-4B.viscosity-poiseuille']") and bool(pg.query_selector("[id='t-4A.energy'] [data-act=g-practice]")))
    # the other guides: Bio/Biochem and Psych/Soc have content maps, CARS has skill areas instead
    for sec, first in (("bio_biochem", "1A"), ("psych_soc", "6A")):
        ev("document.querySelector('[data-act=msec][data-v=\"\"]').click()"); pg.wait_for_timeout(200)
        ev(f"document.querySelector('[data-act=msec][data-v={sec}]').click()"); pg.wait_for_timeout(300)
        n = len(pg.query_selector_all("details.gt[id^='t-']"))
        check(f"{sec} guide renders its content map ({n} topics)", n >= 50 and bool(pg.query_selector(f"details.gcat[data-okey='k:{first}']")))
    ev("document.querySelector('[data-act=msec][data-v=\"\"]').click()"); pg.wait_for_timeout(200)
    ev("document.querySelector('[data-act=msec][data-v=cars]').click()"); pg.wait_for_timeout(300)
    ctxt = pg.inner_text("#view")
    check("CARS guide shows passage types, the three skill areas, wrong-answer patterns and approaches",
          all(s in ctxt for s in ("Passage types", "Foundations of Comprehension", "Reasoning Within the Text", "Reasoning Beyond the Text", "Wrong-answer patterns", "Approaches", "No outside knowledge")) and len(pg.query_selector_all("details.gt")) >= 12)
    ev("document.querySelector('[data-tab=progress]').click()"); pg.wait_for_timeout(200)
    check("MCAT progress shows topics reviewed per guide", "topics reviewed" in pg.inner_text("#view"))
    check("MCAT theme still dark (settings are shared)", ev("document.documentElement.getAttribute('data-theme')") == "dark")
    check("browsing the guide creates no MCAT progress record", stored("rounds.mcat.v1") is None)
    pg.reload(); pg.wait_for_selector("body[data-ready]", timeout=30000); pg.wait_for_timeout(200)
    check("exam choice is remembered after a reload", bool(pg.query_selector("[data-act=exam][data-v=mcat][aria-pressed=true]")) and stored("rounds.exam") == "mcat")
    # a Reviewed tick is progress: it goes to the MCAT key, never the boards key
    ev("document.querySelector('[data-tab=practice]').click()"); pg.wait_for_timeout(200)
    ev("document.querySelector('[data-act=msec][data-v=chem_phys]').click()"); pg.wait_for_timeout(300)
    pg.click("input[data-reviewed='4B.viscosity-poiseuille']"); pg.wait_for_timeout(250)
    mrec = stored("rounds.mcat.v1")
    check("a Reviewed tick is saved in the MCAT record and counted in its category", '"4B.viscosity-poiseuille"' in (mrec or "") and "1 of 11 reviewed" in pg.inner_text("details.gcat[data-okey='k:4B'] > summary"))
    # MCAT questions: the section's Practice tab starts a tutor block; four choices; periodic table sheet; takeaway
    pg.click("[data-act=mtab][data-v=practice]"); pg.wait_for_timeout(200)
    check("Chem/Phys practice tab lists its questions", len(pg.query_selector_all("#view [data-act=q-open]")) >= 8 and bool(pg.query_selector("[data-act=msec-start][data-mode=tutor]")))
    pg.click("[data-act=msec-start][data-mode=tutor]"); pg.wait_for_timeout(400)
    check("MCAT tutor block opens with four choices and no lab button", len(pg.query_selector_all(".opt")) == 4 and not pg.query_selector("[data-act=r-labs]") and bool(pg.query_selector("[data-act=r-ptable]")))
    pg.click("[data-act=r-ptable]"); pg.wait_for_timeout(300)
    check("periodic table sheet shows 118 elements", len(pg.query_selector_all("#ptgrid .pt-el")) == 118)
    pg.fill("[data-ptsearch]", "Cl"); pg.wait_for_timeout(150)
    check("periodic table search finds chlorine", "Chlorine" in pg.inner_text("#ptfound") and "35.5" in pg.inner_text("#ptfound"))
    pg.click("#sheetroot button[data-act=sheet-close]"); pg.wait_for_timeout(300)
    if pg.query_selector("[data-act=r-pane][data-v=question]"): pg.click("[data-act=r-pane][data-v=question]"); pg.wait_for_timeout(200)   # a passage question opens on its passage
    pg.click(".opt[data-l=B]"); pg.click("[data-act=r-submit]"); pg.wait_for_timeout(300)
    check("MCAT answer shows a verdict, a takeaway and the guide topic badge", bool(pg.query_selector("#verdict")) and "Takeaway" in pg.inner_text("#runner") and bool(pg.query_selector("#runner [data-act=g-go]")))
    pg.click(".rbar [data-act=r-exit]"); pg.wait_for_timeout(300)
    mrec = stored("rounds.mcat.v1")
    check("the MCAT answer was saved in the MCAT record", '"answers":{"M1-' in (mrec or "") or '"M1-Q' in (mrec or ""))
    ev("document.querySelector('[data-tab=progress]').click()"); pg.wait_for_timeout(200)
    check("MCAT progress shows section, skill and category breakdowns", all(s in pg.inner_text("#view") for s in ("By section", "By skill", "By content category", "not an MCAT scaled score")))
    ev("document.querySelector('[data-tab=practice]').click()"); pg.wait_for_timeout(200)
    ev("document.querySelector('[data-tab=practice]').click()"); pg.wait_for_timeout(200)  # second tap leaves the section screen
    ev("document.querySelector('[data-act=ptab][data-v=new]').click()"); pg.wait_for_timeout(200)
    check("MCAT block builder offers sections, skills and difficulty 2–5", bool(pg.query_selector("[data-act=p-section]")) and len(pg.query_selector_all("[data-act=p-skill]")) == 4 and len(pg.query_selector_all("[data-act=p-diff]")) == 4)
    # passage runner (Phase M3): CARS block at phone width
    ev("document.querySelector('[data-act=ptab][data-v=sections]').click()"); pg.wait_for_timeout(150)
    ev("document.querySelector('[data-act=msec][data-v=cars]').click()"); pg.wait_for_timeout(200)
    ev("document.querySelector('[data-act=mtab][data-v=practice]').click()"); pg.wait_for_timeout(200)
    pg.click("[data-act=msec-start][data-mode=tutor]"); pg.wait_for_timeout(400)
    if pg.query_selector("[data-act=force-start]"): pg.click("[data-act=force-start]"); pg.wait_for_timeout(500)   # the chem block above is still in progress
    check("a CARS block opens on the passage pane with the Passage | Question toggle and no periodic table", pg.get_attribute(".rbody", "data-pane") == "passage" and pg.is_visible(".ptoggle") and pg.is_visible(".pane.passage") and not pg.is_visible(".pane.question") and not pg.query_selector("[data-act=r-ptable]"))
    check("every question of a passage travels with it", ev("(() => { const s = JSON.parse(localStorage.getItem('rounds.mcat.v1')).sessions[0]; const ps = s.qids.map((id) => id.slice(0, 2) === 'M7' ? (+id.slice(4) <= 6 ? 'a' : 'b') : 'x'); return s.qids.length === 12 && ps.slice(0, 6).every((p) => p === ps[0]) && ps.slice(6).every((p) => p === ps[6]) && ps[0] !== ps[6]; })()"))
    ev("(() => { const t = document.querySelector('.ptext p[data-pi=\"1\"]').firstChild; const r = document.createRange(); r.setStart(t, 4); r.setEnd(t, 30); const s = getSelection(); s.removeAllRanges(); s.addRange(r); })()")
    pg.wait_for_timeout(900)
    hl = json.loads(stored("rounds.mcat.v1")).get("sessions", [{}])[0].get("hl") or {}
    check("a selection in the passage becomes a highlight saved with the session", len(pg.query_selector_all(".ptext mark")) == 1 and list(hl.values()) == [[[1, 4, 30]]])
    pg.click("[data-act=r-pane][data-v=question]"); pg.wait_for_timeout(200)
    check("the toggle shows the question and hides the passage", not pg.is_visible(".pane.passage") and pg.is_visible(".pane.question") and len(pg.query_selector_all(".opt")) == 4)
    pg.click("[data-act=r-pane][data-v=passage]"); pg.wait_for_timeout(400)
    pg.click(".ptext mark"); pg.wait_for_timeout(200)
    check("tapping a highlight clears it", len(pg.query_selector_all(".ptext mark")) == 0 and not any(json.loads(stored("rounds.mcat.v1"))["sessions"][0]["hl"].values()))
    ev("document.querySelector('.pane.passage').scrollTop = 200"); pg.click("[data-act=r-next]"); pg.wait_for_timeout(300)
    check("moving within a passage keeps the passage's scroll position", ev("document.querySelector('.pane.passage').scrollTop") == 200)
    pg.click("[data-act=r-more]"); pg.wait_for_timeout(300)
    check("the question navigator groups questions by passage", [e.text_content() for e in pg.query_selector_all(".navsep")] == ["Passage 1", "Passage 2"])
    pg.click("#sheetroot button[data-act=sheet-close]"); pg.wait_for_timeout(300)
    pg.click(".rbar [data-act=r-exit]"); pg.wait_for_timeout(300)
    ev("document.querySelector('[data-tab=practice]').click()"); pg.wait_for_timeout(150); ev("document.querySelector('[data-tab=practice]').click()"); pg.wait_for_timeout(150)
    ev("document.querySelector('[data-act=msec][data-v=chem_phys]').click()"); pg.wait_for_timeout(200)
    ev("document.querySelector('[data-act=mtab][data-v=practice]').click()"); pg.wait_for_timeout(200)
    ev("document.querySelector('[data-act=q-open][data-id=\"M4-Q01\"]').click()"); pg.wait_for_timeout(500)
    if pg.query_selector("[data-act=read-exp]"): pg.click("[data-act=read-exp]"); pg.wait_for_timeout(500)   # already answered in the chem block above
    check("a science passage shows its table and a chart drawn from the data", len(pg.query_selector_all(".pfig")) == 2 and bool(pg.query_selector(".ftab")) and len(pg.query_selector_all(".chart circle")) == 5 and "Table 1." in pg.inner_text(".pfig figcaption") and bool(pg.query_selector("[data-act=r-ptable]")))
    pg.click(".rbar [data-act=r-exit]"); pg.wait_for_timeout(300)
    ev("(document.querySelector('[data-act=msec][data-v=\"\"]') || document.querySelector('[data-act=ptab][data-v=sections]') || { click() {} }).click()"); pg.wait_for_timeout(200)   # back to the section list
    mrec = stored("rounds.mcat.v1")   # the MCAT record after the passage checks; it must not change while Boards is used
    ev("document.querySelector('[data-act=exam][data-v=boards]').click()"); pg.wait_for_timeout(200)
    check("boards progress record is byte-for-byte unchanged after using the MCAT tab", stored("rounds.progress.v1") == SEED)
    # tutor block (as before)
    ev("document.querySelector('[data-tab=home]').click()"); pg.wait_for_timeout(200)
    ev("document.querySelector('[data-act=quick][data-mode=tutor]').click()"); pg.wait_for_timeout(300)
    pg.click(".opt[data-l=A]"); pg.click("[data-act=r-submit]"); pg.wait_for_timeout(300)
    check("tutor submit shows verdict", bool(pg.query_selector("#verdict")))
    pg.click(".rbar [data-act=r-exit]"); pg.wait_for_timeout(300)
    check("the answer was saved under the boards key only", stored("rounds.progress.v1") != SEED and '"answers"' in (stored("rounds.progress.v1") or "") and stored("rounds.mcat.v1") == mrec)
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
