# Public-site checklist

Rounds is a free study guide for the MCAT and the boards. The site is **public only because GitHub Pages requires
it**; it is not promoted or announced, and there are no plans to promote it. Even so, anyone can reach it, so the
rules in §1, §2, §4, and the no-recalled-content rule in §3 apply now. The reporting and contribution items in §3
and the launch list in §7 are **optional, for later**, and matter only if the site is ever promoted. The owner
makes every decision marked **(owner)**.

## 1. Licensing (applies now)
- **Code license (owner).** A permissive license such as MIT is common for free projects. Add `LICENSE`.
- **Content license (owner).** Questions, passages, explanations, guides, and anatomy cards. CC BY-SA 4.0 lets others
  reuse and improve them while keeping them free, and matches the 3D models' license. CC BY 4.0 is more
  permissive. Put it in `LICENSE-CONTENT` and state it in the README and the app's About screen.
- **3D models:** CC BY-SA 4.0 (already required; see `docs/PLAN_3D.md`, `models/LICENSE`, and `CREDITS.md`).
- **Third-party libraries and fonts:** list each with its license and version in `CREDITS.md`.
- **CARS passages** from public-domain works must cite author, title, and year (see MCAT_SPEC §3.6).

## 2. Trademarks and disclaimers (applies now)
- MCAT® is a registered trademark of the Association of American Medical Colleges (AAMC).
  USMLE® is a program of the Federation of State Medical Boards (FSMB) and the National Board of Medical
  Examiners (NBME).
- Describe content as "MCAT-style" and "Step 2 CK–style." Never use their logos or imply endorsement.
  AAMC's terms say any fair use of its marks must carry the registration symbol (®) and a statement of AAMC's
  ownership; include both wherever "MCAT" appears in headings, the About screen, and the README.
- The section guides are organized by AAMC's *What's on the MCAT Exam?* outline but written in our own words,
  and they link to the official outline (see `docs/MCAT_GUIDES_SPEC.md` §1). Do not reproduce the outline itself
  unless AAMC grants written permission.
- Show on the About screen and in the README:
  "Rounds is an independent, free study resource. It is not affiliated with, endorsed by, or sponsored by the
  AAMC, FSMB, or NBME. Practice scores are not predictions of official scores. Content is for exam study only
  and is not medical advice."
- Point learners to the official AAMC and USMLE practice materials as the gold standard.

## 3. Content quality
- **Review gate (applies now).** Items and guide topics carry `status` (`draft` → `reviewed`) and `reviewed_by`.
  The owner, who holds degrees in biology, chemistry, mathematics, and physics with PhD colleagues in each field,
  reviews all content; no second reviewer is required. A "Beta" label on unreviewed items is **optional and off by
  default**; it can be switched on if the site is ever promoted.
- **No questions from any website or prep source, ever (applies now).** Publicly available official sample questions
  may be read only to understand structure, style, and difficulty; never copy, paraphrase, or adapt their content
  (CLAUDE.md, boards spec §2, MCAT_SPEC §3).
- **No recalled exam content, ever (applies now).** MCAT and USMLE examinees agree not to disclose exam content.
  Nothing described as coming from a real exam is written, accepted, or adapted. If contributions are ever accepted,
  the contribution guide must say such submissions are rejected and reviewers must remove them.
- **Corrections (applies now).** Fix in place, keep the ID, increment `rev`, and record the change in the spec
  changelog. If an answer key changes, reset that one item's saved status for learners. Showing recent corrections in
  the app is optional.
- **Reporting errors (optional, later).** A per-item "Report a problem" link: a prefilled GitHub issue
  (`https://github.com/<owner>/<repo>/issues/new?title=...&body=...`) including the item ID and revision, plus a
  simple form or email link for learners without GitHub accounts (owner chooses).
- **Issue templates and `CONTRIBUTING.md` (optional, later),** explaining how to suggest corrections, what sources to
  cite, and the no-recalled-content rule.

## 4. Privacy (applies now)
- No accounts, no ads, no tracking: progress stays in the learner's browser. Say so on the About screen.
- If analytics are ever added, choose a privacy-respecting tool and disclose it.

## 5. Accessibility (target WCAG 2.2 AA; build in as features are added)
- Keyboard-operable everything; visible focus; screen-reader labels on controls.
- Text alternatives for every figure and structure; equations exposed as MathML.
- Color is never the only way information is shown (correct/incorrect also uses icons and words).
- Respect reduced-motion and text-size settings; contrast checked in light and dark themes.

## 6. Hosting and maintenance (applies now)
- GitHub Pages has published usage limits (site size, bandwidth, build frequency). Check the current numbers
  in GitHub's documentation against the models and data size before adding large content.
- No secrets in the repository. Vendored libraries pinned to exact versions.
- Keep the automated tests passing on every push.

## 7. Launch readiness (only if the site is ever promoted)
- [ ] Licenses chosen and files added (code, content, models)
- [ ] Disclaimers on About screen and README
- [ ] Every public item reviewed by the owner, or the optional Beta label switched on
- [ ] Report-a-problem flow added and someone is watching the reports
- [ ] Accessibility pass on phone and desktop
- [ ] Credits complete; links to official AAMC and USMLE resources
