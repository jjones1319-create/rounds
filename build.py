"""Build the single-file app (index.html) from src/ and questions/.
Run from the repo root:  python build.py
"""
import hashlib, json, re, html, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "questions"))
from questions import QUESTIONS as B1
from questions2 import QUESTIONS2 as B2
from questions3 import QUESTIONS3 as B3
QUESTIONS = B1 + B2 + B3  # append new blocks here, in order

# Short system label shown in the app for each question ID. Add new IDs here.
SYS = {"B1-Q01":"Cardiology","B1-Q02":"OB/GYN","B1-Q03":"Endocrine","B1-Q04":"Gastrointestinal","B1-Q05":"Toxicology","B1-Q06":"Hematology","B1-Q07":"Infectious disease","B1-Q08":"Renal",
       "B2-Q01":"Psychiatry","B2-Q02":"Surgery","B2-Q03":"Respiratory","B2-Q04":"Musculoskeletal","B2-Q05":"Dermatology","B2-Q06":"Male reproductive","B2-Q07":"Ethics & law","B2-Q08":"Biostatistics",
       "B3-Q01":"Preventive medicine","B3-Q02":"Geriatrics","B3-Q03":"Breast","B3-Q04":"Neurology","B3-Q05":"OB/GYN","B3-Q06":"Rheumatology","B3-Q07":"Trauma","B3-Q08":"Pharmacology"}

def h(s):  # question text uses ReportLab-style tags; convert to HTML
    return s.replace("<super>","<sup>").replace("</super>","</sup>")
def plain(s): return html.unescape(re.sub(r"<[^>]+>","",s))

ids = [q["id"] for q in QUESTIONS]
assert len(ids) == len(set(ids)), "duplicate question IDs"
missing = [i for i in ids if i not in SYS]
assert not missing, f"add these IDs to SYS: {missing}"

qb = [{"id":q["id"],"sys":SYS[q["id"]],"discipline":plain(q["discipline"]),"topic":plain(q["topic"]),"difficulty":q["difficulty"],
       "vignette":[h(p) for p in q["vignette"]],"labs":[[h(k),h(v)] for k,v in q["labs"]],"after_labs":[h(p) for p in q["after_labs"]],
       "stem":h(q["stem"]),"options":{k:h(v) for k,v in q["options"].items()},"answer":q["answer"],
       "why_correct":[h(p) for p in q["why_correct"]],"why_wrong":{k:h(v) for k,v in q["why_wrong"].items()},
       "objective":h(q["objective"]),"sources":[h(s) for s in q["sources"]]} for q in QUESTIONS]

# Version stamps for the separately served 3D files: the page asks for js/body3d.js?v=<hash> and the viewer adds the
# same kind of stamp to the mesh map and each model, so a browser can never mix a new page with old cached 3D files.
def vhash(p): return hashlib.sha256(p.read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:10]
mesh_map = json.loads((ROOT / "data/mesh_map.json").read_text(encoding="utf-8"))
ASSET_V = {"body3d": vhash(ROOT / "js/body3d.js"), "map": vhash(ROOT / "data/mesh_map.json"),
           **{l["file"]: vhash(ROOT / l["file"]) for sc in mesh_map["scenes"].values() for l in sc["layers"].values()}}

src = ROOT / "src"
out = (src / "shell.html").read_text(encoding="utf-8")
out = out.replace("__QBANK__", json.dumps(qb, ensure_ascii=False).replace("</","<\\/"))
assert out.count("__ASSET_V__") == 1, "src/shell.html must contain __ASSET_V__ once"
out = out.replace("__ASSET_V__", json.dumps(ASSET_V))
for marker, name in [("FIGURE_JS","figure.js"),("CONTENT_JS","content.js"),("MODELS_JS","models.js"),("ANAT_JS","anat.js"),("APP_JS","app.js")]:
    out = out.replace(f"/*{marker}*/", (src / name).read_text(encoding="utf-8"))
(ROOT / "index.html").write_text(out, encoding="utf-8")
print(f"index.html built: {len(QUESTIONS)} questions, {len(out)//1024} KB")
