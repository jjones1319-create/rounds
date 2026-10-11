"""Write an in-app content review into the MCAT content files (docs/PLAN_MCAT.md, Phase M4; MCAT_SPEC §7).

In the app: Progress (MCAT) → Content review → switch on Review mode, mark questions and passages while reading them,
tick guide topics, then "Copy review JSON" or "Download". Save that JSON and run

    py tools/apply_review.py review.json            # writes status / reviewed_by into content/mcat/*.json and guides
    py tools/apply_review.py review.json --dry-run  # only shows what would change
    py tools/apply_review.py review.json --content some/dir   # another content directory (tests)

Then `py tools/validate.py` and `py build.py`. Reviewer notes are printed, never written into the content: they are the
owner's to-do list for corrections (a correction bumps the item's `rev` and is logged in MCAT_SPEC §11)."""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(p): return json.loads(p.read_text(encoding="utf-8"))
def dump(p, d): p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def apply(review, content, dry=False):
    reviewer = review.get("reviewer") or "owner"
    marks = {}
    for kind in ("items", "passages"):
        for cid, m in (review.get(kind) or {}).items():
            if isinstance(m, dict) and m.get("s") in ("reviewed", "draft"): marks[cid] = (m["s"], m.get("by") or reviewer, m.get("note") or "")
    topics = set((review.get("topics") or {}).keys())
    changed, notes, seen = [], [], set()
    for path in sorted(content.glob("M*.json")):
        b = load(path); touched = False
        for x in (b.get("passages") or []) + (b.get("items") or []):
            cid = x.get("id")
            if cid not in marks: continue
            seen.add(cid); s, by, note = marks[cid]
            if note: notes.append((cid, note))
            new_by = by if s == "reviewed" else None
            if x.get("status") != s or x.get("reviewed_by") != new_by:
                changed.append(f"{cid}: {x.get('status')} → {s}" + (f" ({by})" if s == "reviewed" else ""))
                x["status"] = s; x["reviewed_by"] = new_by; touched = True
        if touched and not dry: dump(path, b)
    for path in sorted((content / "guides").glob("*.json")):
        g = load(path); touched = False
        for c in g.get("concepts") or []:
            for cat in c.get("categories") or []:
                for t in cat.get("topics") or []:
                    if t.get("id") in topics:
                        seen.add(t["id"])
                        if t.get("status") != "reviewed" or t.get("reviewed_by") != reviewer:
                            changed.append(f"{t['id']}: {t.get('status')} → reviewed ({reviewer})"); t["status"] = "reviewed"; t["reviewed_by"] = reviewer; touched = True
        if touched and not dry: dump(path, g)
    missing = sorted((set(marks) | topics) - seen)
    return changed, notes, missing


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("review", help="JSON exported from the app")
    ap.add_argument("--content", default=str(ROOT / "content" / "mcat"), help="content directory (default content/mcat)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    review = load(Path(a.review))
    if review.get("app") != "rounds": sys.exit("not a Rounds review export")
    changed, notes, missing = apply(review, Path(a.content), a.dry_run)
    for c in changed: print(("would set " if a.dry_run else "set ") + c)
    for cid, note in notes: print(f"note {cid}: {note}")
    for m in missing: print(f"warning: {m} is not in the content files (ignored)")
    print(f"{len(changed)} change(s){' (dry run)' if a.dry_run else ''}, {len(notes)} note(s). Now run: py tools/validate.py && py build.py")


if __name__ == "__main__":
    main()
