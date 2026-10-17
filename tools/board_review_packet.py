"""Render board questions from a questions/questionsN.py file as review packets (Markdown).

    python tools/board_review_packet.py questions/questions4.py B4-Q01,B4-Q02 review/peds_pair_01.md            # the key
    python tools/board_review_packet.py questions/questions4.py B4-Q01,B4-Q02 review/peds_pair_01_blind.md --blind

The key shows everything: stars, system, discipline, topic, vignette, labs as a table, interval text, stem, options, answer,
explanations with error types, objective, sources, verified_on, status and reviewed_by, with an answer summary and letter
counts at the top. The blind packet shows, per question, only the ID, vignette, labs, interval text, stem and options, with
blank Answer / Confidence / Objection lines, under the solving instructions of .claude/commands/peds-blind.md; it never
prints a topic, system, discipline, difficulty, explanation or source. ReportLab-style markup (<b>, <i>, <super>, <sub>) and
HTML entities are converted to readable text. Both packets are generated from the question file, so they cannot drift from
what the app shows (build.py reads the same file).
"""
import html
import importlib.util
import re
import sys
from pathlib import Path

STARS = {3: "★★★ Board standard", 4: "★★★★ Above standard", 5: "★★★★★ Top tier"}
SUPER = str.maketrans("0123456789+-=()n", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ⁿ")
SUBS = str.maketrans("0123456789+-=()", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎")

BLIND_INSTRUCTIONS = """## How to solve this packet (from .claude/commands/peds-blind.md, Part 1)

Nothing but this packet, and no web search. For each question:

- **Exam pass:** read it once as a test-taker would, in about 90 seconds, and record your first answer.
- **Expert pass:** work it fully (what the findings show, the diagnosis, the decision, why each option is right or wrong).
  Record your final answer, your confidence (sure, likely or guess) and how hard it felt: ★★★ one key finding leads to the
  standard step; ★★★★ one detail flips the usual answer; ★★★★★ several steps, and the tempting answer would harm the child.
- **Objections:** a second defensible answer; missing or ambiguous information; an answer resting on a weak, outdated or
  contested recommendation; a cue in the options (length, wording, grammar, a repeated word, an option that shares the most
  with the others); vital signs, labs, doses, growth or development implausible for the age; a resemblance to a published
  question you know; anything a pediatric attending or an NBME reviewer would flag.

Save all of it to review/peds_pair_NN_resolve.md, starting with the list of files you opened (only this packet)."""


def load_questions(path):
    """Import questions/questionsN.py by path and return its question list (the QUESTIONS* variable)."""
    path = Path(path)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    lists = [v for k, v in vars(mod).items() if k.startswith("QUESTIONS") and isinstance(v, list)]
    if not lists:
        sys.exit(f"{path} defines no QUESTIONS* list")
    return [q for lst in lists for q in lst]



def txt(s):
    """ReportLab/HTML markup to readable Markdown text."""
    if s is None:
        return ""
    s = str(s)
    s = re.sub(r"<super>(.*?)</super>", lambda m: m.group(1).translate(SUPER) if m.group(1).translate(SUPER) != m.group(1) or not m.group(1).strip() else f"^{m.group(1)}^", s)
    s = re.sub(r"<sup>(.*?)</sup>", lambda m: m.group(1).translate(SUPER) if m.group(1).translate(SUPER) != m.group(1) else f"^{m.group(1)}^", s)
    s = re.sub(r"<sub>(.*?)</sub>", lambda m: m.group(1).translate(SUBS) if m.group(1).translate(SUBS) != m.group(1) else f"_{m.group(1)}_", s)
    s = re.sub(r"</?b>", "**", s)
    s = re.sub(r"</?i>", "*", s)
    s = re.sub(r"<br\s*/?>", "\n", s)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s)
    return re.sub(r"[ \t]+", " ", s).strip()


def labs_md(labs):
    if not labs:
        return []
    out = ["| Test | Result |", "|---|---|"]
    for k, v in labs:
        out.append(f"| {txt(k)} | {txt(v)} |")
    return out + [""]


def body_md(q):
    """The parts both packets show: vignette, labs, interval text, stem, options."""
    out = []
    for p in q.get("vignette", []):
        out += [txt(p), ""]
    out += labs_md(q.get("labs", []))
    for p in q.get("after_labs", []):
        out += [txt(p), ""]
    out += [f"**{txt(q['stem'])}**", ""]
    for L in sorted(q["options"]):
        out.append(f"- **{L}.** {txt(q['options'][L])}")
    return out + [""]


def question_md(q, blind):
    if blind:
        return [f"### {q['id']}", ""] + body_md(q) + [
            "First answer (exam pass): ____",
            "",
            "Final answer: ____   Confidence (sure / likely / guess): ____   Felt difficulty (★★★ / ★★★★ / ★★★★★): ____",
            "",
            "Objections, if any: ____",
            "", "---", ""]
    stars = STARS.get(q.get("difficulty"), str(q.get("difficulty")))
    out = [f"### {q['id']}  ·  {stars}", "",
           f"*System:* {txt(q.get('system'))} · *Discipline:* {txt(q.get('discipline'))}", "",
           f"*Topic:* {txt(q.get('topic'))}", ""]
    out += body_md(q)
    out += [f"**Answer: {q['answer']}. {txt(q['options'][q['answer']])}**", "", "*Why it is correct*", ""]
    for p in q.get("why_correct", []):
        out += [txt(p), ""]
    out += ["*Why the other choices are wrong*", ""]
    errs = q.get("distractor_error_types", {})
    for L in sorted(q["options"]):
        if L != q["answer"]:
            err = f" *({txt(errs[L])})*" if L in errs else ""
            out.append(f"- **{L}.** {txt(q.get('why_wrong', {}).get(L, ''))}{err}")
    out += ["", f"*Educational objective:* {txt(q.get('objective'))}", "", "*Sources*", ""]
    for s in q.get("sources", []):
        out.append(f"- {txt(s)}")
    out += ["", f"*Verified on:* {q.get('verified_on', '—')} · *Status:* {q.get('status', 'active')} · *Reviewed by:* {q.get('reviewed_by') or '—'}", "", "---", ""]
    return out


def render(questions, ids, blind):
    by_id = {q["id"]: q for q in questions}
    missing = [i for i in ids if i not in by_id]
    if missing:
        sys.exit(f"ids not found: {missing}")
    qs = [by_id[i] for i in ids]
    title = ", ".join(ids)
    if blind:
        out = [f"# Blind re-solve packet: {title}", "", f"{len(qs)} questions. You have not seen the answers.", "", BLIND_INSTRUCTIONS, "", "---", ""]
    else:
        out = [f"# Review packet (key): {title}", "",
               f"{len(qs)} questions. Answers: " + ", ".join(f"{q['id']} {q['answer']}" for q in qs), ""]
        counts = {L: sum(1 for q in qs if q["answer"] == L) for L in "ABCDE"}
        out += ["Answer letters: " + ", ".join(f"{L} {n}" for L, n in counts.items()), "",
                "## How this pair is reviewed", "",
                "An independent blind re-solve (.claude/commands/peds-blind.md): a fresh conversation answers every question from the blind packet; "
                "its answers and objections are compared with this key. A question passes only if the final answer matches and no objection holds up; "
                "anything else is checked against the sources, fixed, and re-solved blind again. The pair is committed and pushed only after both pass.", "", "---", ""]
    for q in qs:
        out += question_md(q, blind)
    return "\n".join(out)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--blind"]
    if len(args) != 3:
        sys.exit(__doc__)
    src, ids, dst = args[0], [i.strip() for i in args[1].split(",") if i.strip()], Path(args[2])
    blind = "--blind" in sys.argv
    text = render(load_questions(src), ids, blind)
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8", newline="\n")
    print(f"wrote {dst} ({len(ids)} questions, {'blind' if blind else 'key'})")
