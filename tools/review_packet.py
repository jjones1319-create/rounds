"""Render an MCAT block file as a readable review packet (Markdown) for the owner's independent review.

    py tools/review_packet.py content/mcat/chem_phys/batch_01.json review/chem_phys_batch_01.md           # the key
    py tools/review_packet.py content/mcat/chem_phys/batch_01.json review/chem_phys_batch_01_blind.md --blind

The key prints each passage in full with its figure data (tables as Markdown tables, charts as their data points), then
every question with its choices, the answer, the worked solution, why each wrong choice is wrong, tags, takeaway and
sources. The blind packet has the passages and questions only, for the independent blind re-solve that gates every batch
(MCAT_SPEC §7). Both are generated from the content file, so they cannot drift from what the app shows.
"""
import json
import sys
from pathlib import Path

STARS = {2: "★★", 3: "★★★", 4: "★★★★", 5: "★★★★★"}
SKILL = {"1": "Skill 1 Knowledge", "2": "Skill 2 Reasoning", "3": "Skill 3 Research design", "4": "Skill 4 Data and statistics"}


def figure_md(f):
    out = [f"**{f.get('caption', f['id'])}**", ""]
    d, t = f["data"], f["type"]
    if t == "table":
        out.append("| " + " | ".join(d["columns"]) + " |")
        out.append("|" + "---|" * len(d["columns"]))
        for r in d["rows"]:
            out.append("| " + " | ".join(str(c) for c in r) + " |")
    elif t in ("line", "scatter", "bar"):
        out.append(f"Chart ({t}): x = {d['x']['label']}; y = {d['y']['label']}.")
        for s in d["series"]:
            pts = ", ".join(f"({a}, {b})" for a, b in s["points"])
            out.append(f"- {s['name']}: {pts}")
    elif t == "equation":
        out.append(f"Equation: `{d['tex']}`")
    elif t == "structure":
        out.append(f"Structure (SMILES): `{d['smiles']}`")
    out += ["", f"*Alt text:* {f.get('alt', '')}", ""]
    return out


def item_md(q, n, blind=False):
    head = f"### {q['id']}" if blind else f"### {q['id']}  ·  {STARS.get(q['difficulty'], q['difficulty'])}  ·  {SKILL.get(str(q.get('skill')), q.get('cars_skill'))}"
    out = [head, "", q["stem"], ""]
    for L in "ABCD":
        out.append(f"- **{L}.** {q['options'][L]}")
    if blind:
        return out + ["", "Answer: ____   Confidence (sure / likely / guess): ____   Objection, if any: ____", "", "---", ""]
    out += ["", f"**Answer: {q['answer']}**", "", "*Worked solution*", ""]
    for line in q["why_correct"]:
        out.append(f"- {line}")
    out += ["", "*Why the other choices are wrong*", ""]
    for L in "ABCD":
        if L != q["answer"]:
            out.append(f"- **{L}.** {q['why_wrong'][L]} *({q['error_types'][L]})*")
    tags = f"{q['section']} · {q['discipline']} · FC{q['fc']} {q['category']} · topics: {', '.join(q['topics'])}" if q.get("fc") else f"{q['section']} · {q.get('cars_skill')}"
    out += ["", f"*Tags:* {tags}", "", f"*Takeaway:* {q['takeaway']}", "", "*Sources*", ""]
    for s in q["sources"]:
        out.append(f"- {s}")
    out += ["", f"*Status:* {q['status']} · rev {q['rev']}", "", "---", ""]
    return out


def render(block, blind=False):
    items = block["items"]
    by_passage = {}
    for q in items:
        by_passage.setdefault(q.get("passage"), []).append(q)
    if blind:
        out = [f"# Blind re-solve packet: block {block['block']}", "",
               f"{len(items)} questions, {len(block.get('passages') or [])} passages. You have not seen the answers. For every question, solve it from the passage, "
               "the periodic table and your own knowledge, without a calculator, and record your answer, your confidence and your worked reasoning in a few lines. "
               "Also record any objection: a second defensible choice, an ambiguous stem, a number that needs a calculator, a clue in the choices (length, shared values, "
               "grammar), a factual error in the passage, or a resemblance to a question you have seen published. Report everything in one list by question id.", ""]
    else:
        out = [f"# Review packet (key): block {block['block']}", ""]
        if block.get("plan"):
            out += [f"Plan: {block['plan']}", ""]
        out += [f"{len(items)} questions, {len(block.get('passages') or [])} passages. Answers: " + " ".join(f"{q['id'][-3:]}{q['answer']}" for q in items), ""]
        counts = {L: sum(1 for q in items if q["answer"] == L) for L in "ABCD"}
        out += ["Answer letters: " + ", ".join(f"{L} {n}" for L, n in counts.items()), ""]
        out += ["## How this batch is reviewed", "", "An independent blind re-solve (MCAT_SPEC §7): a fresh session answers every item from the blind packet; its answers and "
                "objections are compared with this key. Agreement with no objection passes the item (reviewed_by: independent blind re-solve); "
                "anything else is checked against the sources, fixed and re-solved. The batch is committed and pushed only after every item passes.", ""]
    for p in block.get("passages") or []:
        out += [f"## Passage {p['id']}: {p.get('title', '')}", ""]
        for para in p["text"]:
            out += [para, ""]
        for f in p.get("figures") or []:
            out += figure_md(f)
        if not blind:
            out += [f"*Source:* {p['source']}", "", f"*Status:* {p['status']}", ""]
        for i, q in enumerate(by_passage.get(p["id"], []), 1):
            out += item_md(q, i, blind)
    if by_passage.get(None):
        out += ["## Standalone questions", ""]
        for i, q in enumerate(by_passage[None], 1):
            out += item_md(q, i, blind)
    return "\n".join(out)


if __name__ == "__main__":
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    blind = "--blind" in sys.argv[3:]
    block = json.loads(src.read_text(encoding="utf-8"))
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(render(block, blind), encoding="utf-8")
    print(f"wrote {dst} ({len(block['items'])} items)")
