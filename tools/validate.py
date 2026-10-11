"""Validate MCAT content and bundle it for the app (docs/PLAN_MCAT.md, Phase M0).

Checks every block in content/mcat/M*.json against docs/MCAT_SPEC.md §8 and every guide in
content/mcat/guides/*.json against docs/MCAT_GUIDES_SPEC.md §4, then writes a coverage report.

    py tools/validate.py          # report problems; exit 1 on any error
build.py imports build_bundle(), which raises SystemExit on errors so a broken block never ships.
"""
import collections
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "mcat"
REPORT = ROOT / "work" / "mcat_coverage.md"

# Exam facts and blueprint from docs/MCAT_SPEC.md §1–2 (verified 2026-10-10; re-check at the start of each block).
SECTIONS = [
    {"k": "chem_phys", "name": "Chemical and Physical Foundations of Biological Systems", "short": "Chem/Phys",
     "questions": 59, "minutes": 95, "passage_questions": 44, "discrete_questions": 15, "tools": "Periodic table",
     "fcs": ["4", "5"], "concepts": {"4": 40, "5": 60},
     "disciplines": {"general chemistry": 30, "biochemistry": 25, "physics": 25, "organic chemistry": 15, "biology": 5}},
    {"k": "cars", "name": "Critical Analysis and Reasoning Skills", "short": "CARS",
     "questions": 53, "minutes": 90, "passage_questions": 53, "discrete_questions": 0, "tools": None,
     "fcs": [], "concepts": {}, "disciplines": {}, "cars_skills": {"foundations": 30, "within": 30, "beyond": 40}},
    {"k": "bio_biochem", "name": "Biological and Biochemical Foundations of Living Systems", "short": "Bio/Biochem",
     "questions": 59, "minutes": 95, "passage_questions": 44, "discrete_questions": 15, "tools": "Periodic table",
     "fcs": ["1", "2", "3"], "concepts": {"1": 55, "2": 20, "3": 25},
     "disciplines": {"biology": 65, "biochemistry": 25, "general chemistry": 5, "organic chemistry": 5}},
    {"k": "psych_soc", "name": "Psychological, Social, and Biological Foundations of Behavior", "short": "Psych/Soc",
     "questions": 59, "minutes": 95, "passage_questions": 44, "discrete_questions": 15, "tools": "Periodic table",
     "fcs": ["6", "7", "8", "9", "10"], "concepts": {"6": 25, "7": 35, "8": 20, "9": 15, "10": 5},
     "disciplines": {"psychology": 65, "sociology": 30, "biology": 5}},
]
SECTION = {s["k"]: s for s in SECTIONS}
SKILLS = {"1": 35, "2": 45, "3": 10, "4": 10}          # Scientific Inquiry and Reasoning Skills, % of each science section
CARS_SKILLS = {"foundations": "Foundations of Comprehension", "within": "Reasoning Within the Text", "beyond": "Reasoning Beyond the Text"}
CATEGORIES = {  # content category code -> short name (AAMC framework names, used as identifiers)
    "1A": "Proteins and amino acids", "1B": "Gene to protein", "1C": "Heredity and genetic diversity", "1D": "Bioenergetics and fuel metabolism",
    "2A": "Assemblies of molecules, cells, and tissues", "2B": "Prokaryotes and viruses", "2C": "Cell division, differentiation, specialization",
    "3A": "Nervous and endocrine systems", "3B": "Main organ systems",
    "4A": "Motion, forces, work, energy, equilibrium", "4B": "Fluids and gas exchange", "4C": "Electrochemistry and circuits",
    "4D": "Light and sound", "4E": "Atoms, nuclear decay, electronic structure",
    "5A": "Water and solutions", "5B": "Molecules and intermolecular interactions", "5C": "Separation and purification",
    "5D": "Structure, function, reactivity of biological molecules", "5E": "Thermodynamics and kinetics",
    "6A": "Sensing the environment", "6B": "Making sense of the environment", "6C": "Responding to the world",
    "7A": "Individual influences on behavior", "7B": "Social processes", "7C": "Attitude and behavior change",
    "8A": "Self-identity", "8B": "Social thinking", "8C": "Social interactions",
    "9A": "Social structure", "9B": "Demographics", "10A": "Social inequality",
}
FC_OF = {code: code[:-1] for code in CATEGORIES}
DISCIPLINES = {"biology", "biochemistry", "general chemistry", "organic chemistry", "physics", "psychology", "sociology"}
TOPIC_TAGS = {"BIO", "BC", "GC", "OC", "PHY", "PSY", "SOC"}
ERROR_TYPES = ["sign or unit error", "wrong formula", "misread graph", "reversed relationship", "true but irrelevant",
               "too extreme", "out of scope", "outside knowledge contradicting the passage"]
FIGURE_TYPES = {"line", "bar", "scatter", "table", "structure", "equation"}
STATUSES = {"draft", "reviewed"}
# Block ids are M<n> (one section per block in practice) or M<n><category letter> for single-category blocks such as M4B.
ID_BLOCK, ID_ITEM, ID_PASSAGE = re.compile(r"^M\d+[A-E]?$"), re.compile(r"^(M\d+[A-E]?)-Q\d{2}$"), re.compile(r"^(M\d+[A-E]?)-P\d{2}$")
WORDS = {"science": (200, 550), "cars": (450, 650)}  # passage length (words) per MCAT_SPEC §5, warned when outside
ID_TOPIC = re.compile(r"^(\d{1,2}[A-E])\.[a-z0-9]+(?:-[a-z0-9]+)*$")


class Check:
    """Collects errors (fail the build) and warnings (reported only)."""
    def __init__(self):
        self.errors, self.warnings = [], []
    def err(self, where, msg): self.errors.append(f"{where}: {msg}")
    def warn(self, where, msg): self.warnings.append(f"{where}: {msg}")
    def require(self, cond, where, msg):
        if not cond: self.err(where, msg)
        return cond


def nonempty_strings(v):
    return isinstance(v, list) and len(v) > 0 and all(isinstance(x, str) and x.strip() for x in v)


def load_json(path, ck):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        ck.err(path.name, f"cannot read JSON ({e})")
        return None


def validate_guides(ck):
    """Returns {section: guide}, {topic_id: section}."""
    guides, topics = {}, {}
    gdir = CONTENT / "guides"
    for path in sorted(gdir.glob("*.json")) if gdir.is_dir() else []:
        g = load_json(path, ck)
        if g is None: continue
        sec = g.get("section")
        if not ck.require(sec in SECTION, path.name, f"unknown section {sec!r}"): continue
        ck.require(sec == path.stem, path.name, f"file name should be {sec}.json")
        ck.require(sec in guides or True, path.name, "")
        if sec in guides: ck.err(path.name, "duplicate guide for this section")
        ck.require(isinstance(g.get("verified"), str) and re.match(r"^\d{4}-\d{2}-\d{2}$", g["verified"] or ""), path.name, "needs a 'verified' date (YYYY-MM-DD)")
        ck.require(isinstance(g.get("official_outline_url"), str) and g["official_outline_url"].startswith("https://"), path.name, "needs 'official_outline_url'")
        if sec == "cars":
            for key in ("passage_types", "skill_areas", "wrong_answer_patterns", "approaches"):
                ck.require(isinstance(g.get(key), list), path.name, f"CARS guide needs a '{key}' list")
        else:
            # front matter (MCAT_GUIDES_SPEC §2 A, B, D, E, F): exam facts and weightings must match the spec's numbers
            ck.require(isinstance(g.get("attribution"), str) and "AAMC" in g["attribution"] and "our own" in g["attribution"], path.name, "needs the attribution statement from MCAT_GUIDES_SPEC §1")
            gl = g.get("glance") or {}
            for key in ("questions", "minutes", "passage_questions", "discrete_questions", "tools"):
                ck.require(gl.get(key) == SECTION[sec][key], path.name, f"glance.{key} should be {SECTION[sec][key]!r}")
            ck.require(gl.get("calculator") is False and isinstance(gl.get("summary"), str) and gl["summary"].strip(), path.name, "glance needs calculator: false and a summary")
            bp = g.get("blueprint") or {}
            ck.require(bp.get("disciplines") == SECTION[sec]["disciplines"], path.name, "blueprint.disciplines must match the AAMC weightings in MCAT_SPEC §2")
            ck.require({str(k): v for k, v in (bp.get("concepts") or {}).items()} == SECTION[sec]["concepts"], path.name, "blueprint.concepts must match MCAT_SPEC §2")
            ck.require({str(k): v for k, v in (bp.get("skills") or {}).items()} == SKILLS, path.name, "blueprint.skills must be 35/45/10/10")
            skills = g.get("skills") or []
            ck.require([str(s.get("id")) for s in skills] == ["1", "2", "3", "4"] and all(s.get("name") and s.get("what") and s.get("example") for s in skills), path.name, "skills must describe Skills 1–4 (name, what, example)")
            for key in ("research_methods", "math_toolkit"):
                ck.require(isinstance(g.get(key), list) and g[key] and all(isinstance(m, dict) and m.get("name") and nonempty_strings(m.get("know")) for m in g[key]), path.name, f"{key} must be a non-empty list of {{name, know[]}}")
            allowed = SECTION[sec]["fcs"]
            for concept in g.get("concepts") or []:
                cid = str(concept.get("id"))
                where = f"{path.name} concept {cid}"
                if not ck.require(cid in allowed, where, f"foundational concept {cid} is not part of {sec} (allowed: {allowed})"): continue
                ck.require(isinstance(concept.get("name"), str) and concept["name"].strip(), where, "needs a name")
                for cat in concept.get("categories") or []:
                    code = cat.get("id")
                    cwhere = f"{path.name} category {code}"
                    if not ck.require(code in CATEGORIES and FC_OF[code] == cid, cwhere, f"unknown category or not in concept {cid}"): continue
                    ck.require(isinstance(cat.get("name"), str) and cat["name"].strip() and (cat.get("topics") or []), cwhere, "needs a name and at least one topic")
                    for t in cat.get("topics") or []:
                        tid = t.get("id")
                        twhere = f"{path.name} topic {tid}"
                        if not ck.require(isinstance(tid, str) and ID_TOPIC.match(tid) and ID_TOPIC.match(tid).group(1) == code, twhere, "topic id must be '<category>.<slug>' with this category"): continue
                        if tid in topics: ck.err(twhere, "duplicate topic id")
                        topics[tid] = sec
                        ck.require(isinstance(t.get("name"), str) and t["name"].strip(), twhere, "needs a name")
                        ck.require(nonempty_strings(t.get("know")), twhere, "'know' must be a non-empty list of sentences")
                        ck.require(set(t.get("tags") or []) <= TOPIC_TAGS and t.get("tags"), twhere, f"tags must be from {sorted(TOPIC_TAGS)}")
                        ck.require(all(isinstance(e, str) and e.strip() for e in t.get("equations") or []), twhere, "equations must be LaTeX strings")
                        ck.require(t.get("status") in STATUSES, twhere, "status must be draft or reviewed")
                        if t.get("status") == "reviewed": ck.require(bool(t.get("reviewed_by")), twhere, "reviewed topics need reviewed_by")
                        for r in t.get("refs") or []:
                            ck.require(isinstance(r, dict) and r.get("label"), twhere, "each ref needs a label")
        guides[sec] = g
    return guides, topics


def validate_blocks(ck, topics):
    """Returns (passages, items) across all blocks, in file order."""
    passages, items, seen = [], [], set()
    for path in sorted(CONTENT.glob("M*.json")) if CONTENT.is_dir() else []:
        b = load_json(path, ck)
        if b is None: continue
        block = b.get("block")
        if not ck.require(isinstance(block, str) and ID_BLOCK.match(block) and block == path.stem, path.name, "'block' must match the file name, e.g. M1"): continue
        local_passages = {}
        for p in b.get("passages") or []:
            pid = p.get("id"); where = f"{block} passage {pid}"
            if not ck.require(isinstance(pid, str) and ID_PASSAGE.match(pid) and ID_PASSAGE.match(pid).group(1) == block, where, "id must be <block>-Pnn"): continue
            if pid in seen: ck.err(where, "duplicate id"); continue
            seen.add(pid)
            ck.require(p.get("section") in SECTION, where, "unknown section")
            ck.require(p.get("kind") in ("science", "cars"), where, "kind must be science or cars")
            ck.require(nonempty_strings(p.get("text")), where, "text must be a non-empty list of paragraphs")
            ck.require(isinstance(p.get("source"), str) and p["source"].strip(), where, "needs a source line")
            ck.require(p.get("status") in STATUSES, where, "status must be draft or reviewed")
            if nonempty_strings(p.get("text")):
                n = sum(len(t.split()) for t in p["text"]); lo, hi = WORDS.get(p.get("kind"), (0, 10**9))
                if not lo <= n <= hi: ck.warn(where, f"{n} words; {p.get('kind')} passages should be {lo}–{hi}")
            fids = set()
            for f in p.get("figures") or []:
                fwhere = f"{where} figure {f.get('id')}"
                ck.require(isinstance(f.get("id"), str) and f["id"] and f["id"] not in fids, fwhere, "figures need unique ids within the passage"); fids.add(f.get("id"))
                ck.require(f.get("type") in FIGURE_TYPES, fwhere, f"type must be one of {sorted(FIGURE_TYPES)}")
                ck.require(isinstance(f.get("data"), (dict, list)) and f["data"], fwhere, "needs data (figures are drawn from data)")
                ck.require(isinstance(f.get("alt"), str) and f["alt"].strip(), fwhere, "needs alt text")
                validate_figure(ck, fwhere, f)
            local_passages[pid] = p
            passages.append(p)
        answers = []
        for q in b.get("items") or []:
            qid = q.get("id"); where = f"{block} item {qid}"
            if not ck.require(isinstance(qid, str) and ID_ITEM.match(qid) and ID_ITEM.match(qid).group(1) == block, where, "id must be <block>-Qnn"): continue
            if qid in seen: ck.err(where, "duplicate id"); continue
            seen.add(qid)
            ck.require(isinstance(q.get("rev"), int) and q["rev"] >= 1, where, "rev must be an integer >= 1")
            sec = q.get("section")
            if not ck.require(sec in SECTION, where, "unknown section"): continue
            if q.get("passage") is not None:
                pref = q["passage"]
                if ck.require(pref in local_passages, where, f"passage {pref!r} is not in this block"):
                    ck.require(local_passages[pref].get("section") == sec, where, "passage is in a different section")
            opts = q.get("options")
            ck.require(isinstance(opts, dict) and list(opts.keys()) == ["A", "B", "C", "D"] and all(isinstance(v, str) and v.strip() for v in opts.values()),
                       where, "options must be exactly A, B, C, D, each non-empty")
            ans = q.get("answer")
            ck.require(ans in ("A", "B", "C", "D"), where, "answer must be A–D")
            answers.append(ans)
            wrong = {"A", "B", "C", "D"} - {ans}
            for field in ("why_wrong", "error_types"):
                d = q.get(field)
                ck.require(isinstance(d, dict) and set(d.keys()) == wrong and all(isinstance(v, str) and v.strip() for v in d.values()),
                           where, f"{field} must explain exactly the three wrong choices {sorted(wrong)}")
            for L, et in (q.get("error_types") or {}).items():
                if isinstance(et, str) and not any(et.lower().startswith(e) for e in ERROR_TYPES):
                    ck.warn(where, f"error type for {L} ({et!r}) is not one of the named types in MCAT_SPEC §5")
            ck.require(isinstance(q.get("stem"), str) and q["stem"].strip(), where, "needs a stem")
            ck.require(nonempty_strings(q.get("why_correct")), where, "why_correct must be a non-empty list")
            ck.require(isinstance(q.get("takeaway"), str) and q["takeaway"].strip(), where, "needs a takeaway")
            ck.require(nonempty_strings(q.get("sources")), where, "sources must be a non-empty list")
            ck.require(isinstance(q.get("difficulty"), int) and 2 <= q["difficulty"] <= 5, where, "difficulty must be 2–5")
            ck.require(q.get("status") in STATUSES, where, "status must be draft or reviewed")
            if q.get("status") == "reviewed": ck.require(bool(q.get("reviewed_by")), where, "reviewed items need reviewed_by")
            if sec == "cars":
                ck.require(q.get("cars_skill") in CARS_SKILLS, where, f"CARS items need cars_skill in {sorted(CARS_SKILLS)}")
                ck.require(q.get("fc") is None and q.get("category") is None and q.get("skill") is None, where, "CARS items have no fc, category, or skill")
                ck.require(q.get("passage") is not None, where, "CARS items are passage-based")
            else:
                fc, cat = str(q.get("fc")), q.get("category")
                ck.require(fc in SECTION[sec]["fcs"], where, f"fc must be one of {SECTION[sec]['fcs']} for {sec}")
                ck.require(cat in CATEGORIES and FC_OF[cat] == fc, where, f"category must belong to foundational concept {fc}")
                ck.require(q.get("discipline") in DISCIPLINES, where, f"discipline must be one of {sorted(DISCIPLINES)}")
                ck.require(str(q.get("skill")) in SKILLS, where, "skill must be 1–4")
                ck.require(q.get("cars_skill") is None, where, "science items have no cars_skill")
                tl = q.get("topics")
                if ck.require(nonempty_strings(tl), where, "topics must list at least one guide topic id"):
                    for t in tl:
                        if ck.require(t in topics, where, f"topic {t!r} is not in any guide (write the guide topic first)"):
                            ck.require(topics[t] == sec, where, f"topic {t} belongs to the {topics[t]} guide")
            items.append(q)
        # letter balance per block (MCAT_SPEC §5)
        for i in range(2, len(answers)):
            if answers[i] == answers[i - 1] == answers[i - 2]:
                ck.err(f"{block}", f"answer {answers[i]} appears three times in a row (items {i - 1}–{i + 1})")
        if len(answers) >= 8:   # a short passage block cannot keep every letter at 20–30%
            counts = collections.Counter(answers)
            for L in "ABCD":
                share = 100 * counts[L] / len(answers)
                if not 20 <= share <= 30:
                    ck.warn(f"{block}", f"answer {L} is {share:.0f}% of the block (target 20–30%)")
    return passages, items


def validate_figure(ck, where, f):
    """Shape of each figure's data (the app draws the figure from it; docs/MCAT_SPEC.md §5, §8)."""
    t, d = f.get("type"), f.get("data")
    if not isinstance(d, dict): ck.err(where, "data must be an object"); return
    if t == "table":
        cols, rows = d.get("columns"), d.get("rows")
        if ck.require(nonempty_strings(cols), where, "table data needs 'columns' (list of header strings)") and            ck.require(isinstance(rows, list) and rows and all(isinstance(r, list) for r in rows), where, "table data needs 'rows' (list of lists)"):
            for i, r in enumerate(rows): ck.require(len(r) == len(cols), where, f"row {i} has {len(r)} cells for {len(cols)} columns")
    elif t in ("line", "scatter", "bar"):
        for ax in ("x", "y"):
            a = d.get(ax)
            ck.require(isinstance(a, dict) and isinstance(a.get("label"), str) and a["label"].strip(), where, f"'{ax}' axis needs a label (with units)")
        ser = d.get("series")
        if ck.require(isinstance(ser, list) and ser, where, "chart data needs 'series' (list)"):
            for i, sr in enumerate(ser):
                ck.require(isinstance(sr, dict) and isinstance(sr.get("name"), str), where, f"series {i} needs a name")
                pts = sr.get("points") if isinstance(sr, dict) else None
                if t == "bar":
                    ck.require(isinstance(pts, list) and pts and all(isinstance(pt, list) and len(pt) == 2 and isinstance(pt[0], str) and isinstance(pt[1], (int, float)) for pt in pts),
                               where, f"series {i} points must be [category, value] pairs")
                else:
                    ck.require(isinstance(pts, list) and len(pts) >= 2 and all(isinstance(pt, list) and len(pt) == 2 and all(isinstance(v, (int, float)) for v in pt) for pt in pts),
                               where, f"series {i} points must be at least two [x, y] number pairs")
    elif t == "equation":
        ck.require(isinstance(d.get("tex"), str) and d["tex"].strip(), where, "equation data needs 'tex'")
    elif t == "structure":
        ck.require(isinstance(d.get("smiles"), str) and d["smiles"].strip(), where, "structure data needs 'smiles' (rendered to SVG at build time)")
        if d.get("smiles"):
            try:
                from structures import check_smiles
                err = check_smiles(d["smiles"])
                if err: ck.err(where, err)
            except ImportError:
                ck.warn(where, "RDKit is not installed, so the SMILES was not parsed (pip install rdkit)")


def coverage_report(guides, topics, items):
    """Markdown: topics with no questions, and questions per category versus AAMC weightings."""
    per_topic = collections.Counter(t for q in items for t in (q.get("topics") or []))
    lines = ["# MCAT coverage report", "", f"{len(items)} items, {len(topics)} guide topics, {len(guides)} guides.", ""]
    for sec in SECTIONS:
        k = sec["k"]
        lines.append(f"## {sec['short']}")
        sec_items = [q for q in items if q.get("section") == k]
        if k == "cars":
            c = collections.Counter(q.get("cars_skill") for q in sec_items)
            for s, w in sec["cars_skills"].items():
                lines.append(f"- {CARS_SKILLS[s]}: {c[s]} items ({w}% target)")
        else:
            c = collections.Counter(q.get("category") for q in sec_items)
            for fc, w in sec["concepts"].items():
                cats = [code for code in CATEGORIES if FC_OF[code] == fc]
                n = sum(c[code] for code in cats)
                lines.append(f"- FC{fc} ({w}% target): {n} items; " + ", ".join(f"{code} {c[code]}" for code in cats))
            empty = sorted(t for t, s in topics.items() if s == k and per_topic[t] == 0)
            lines.append(f"- Topics with no questions: {len(empty)}" + (": " + ", ".join(empty) if empty else ""))
        lines.append("")
    return "\n".join(lines)


def validate():
    """Returns (bundle, check, report)."""
    ck = Check()
    guides, topics = validate_guides(ck)
    passages, items = validate_blocks(ck, topics)
    bundle = {
        "sections": [{key: s[key] for key in ("k", "name", "short", "questions", "minutes", "passage_questions", "discrete_questions", "tools")} for s in SECTIONS],
        "passages": passages, "items": items, "guides": guides, "categories": CATEGORIES,
    }
    return bundle, ck, coverage_report(guides, topics, items)


def build_bundle(verbose=True):
    """For build.py: validated bundle for data/mcat.json, or SystemExit listing the errors."""
    bundle, ck, report = validate()
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")
    if verbose:
        for w in ck.warnings: print("validate warning:", w)
    if ck.errors:
        sys.exit("MCAT content failed validation:\n  " + "\n  ".join(ck.errors))
    return bundle


if __name__ == "__main__":
    bundle, ck, report = validate()
    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")
    for w in ck.warnings: print("warning:", w)
    for e in ck.errors: print("ERROR:", e)
    print(f"{len(bundle['items'])} items, {len(bundle['passages'])} passages, {len(bundle['guides'])} guides; "
          f"{len(ck.errors)} errors, {len(ck.warnings)} warnings. Coverage report: {REPORT.relative_to(ROOT)}")
    sys.exit(1 if ck.errors else 0)
