---
description: Write the next 2 pediatric board questions from docs/PEDS_BLUEPRINT.md, verified and checked, ready for the blind re-solve
argument-hint: [optional notes, e.g. "redo B4-Q02 with a reserve topic"]
---

Write the next pair of pediatric board questions. Two only, so each one gets full depth.
Notes for this pair, if any: $ARGUMENTS

0. Start. Read CLAUDE.md, all of docs/board_question_generator_spec.md, docs/PEDS_BLUEPRINT.md (if it doesn't exist,
   stop and tell me to run /peds-setup) and the newest questions/questionsN.py (copy its format exactly). Take the
   lowest-numbered pair whose rows are "planned"; if the notes name one question to redo, write only that one. Change a
   planned topic only if verification shows its decision is outdated, contested or keyed to a weak recommendation; then
   use a reserve topic, log why in the blueprint changelog, and tell me. Don't commit or push anything, and don't save
   anything about these questions to Claude's memory: a fresh conversation must be able to re-solve them blind.

1. Verify before writing. Treat your memory of a guideline as a lead, never a source; pediatric guidance changed a lot
   from 2021 to 2026. For each question, by web search in this session:
   - Find the current primary source for the decision: the society's own guideline or its journal publication, or a
     landmark trial where no guideline exists. UpToDate, Medscape, StatPearls, prep sites and Wikipedia may help you
     find it but are never the source.
   - Search for anything newer (revision, focused update, reaffirmation, retirement, erratum), and note which version
     you used and why it is current.
   - Check the other US bodies that speak to the decision (AAP, CDC/ACIP, AAFP, ACOG, AHA, IDSA/PIDS, NASPGHAN,
     ISPAD/ADA, ASH/NHLBI, AUA, ACR, ACEP). If any disagree with the keyed decision, move the decision to ground they
     share, or use a reserve topic.
   - Key only to a firm recommendation (strong or moderate, "should" or "should not"), and give its grade.
   - Log it in review/peds_pair_NN_sources.md: source, version check, the recommendation, table or figure number you
     rely on (paraphrased, not quoted), URL and date.

2. Design brief, per question, in the sources file: the decision tested; the detail that decides it; the most tempting
   wrong answer and why a good student picks it; and the one change to the vignette that would make that answer right.
   If you can't name that change, the item is testing recall: redesign it.

3. Write each item to spec §2–§6, and make it real for the child's age:
   - Exact age: days for neonates, weeks or months for infants, years and months under 3; for a preterm infant, the
     gestational age at birth and the corrected age. Keep the age well inside any guideline age band.
   - Weight in kg (lb) and, when growth matters, percentiles that match the WHO (under 2 years) or CDC (2 years and
     older) charts; length or height in cm (in); head circumference in infants when relevant.
   - Vital signs plausible for age (note the reference used, e.g. Fleming et al., Lancet 2011, for heart and
     respiratory rates, and the AAP 2017 tables when blood pressure matters); temperature in °C (°F), with the route
     when it matters.
   - The history a pediatric case needs: who gives it; birth history (gestational age, delivery, complications, NICU
     stay); for neonates the maternal history (GBS status and intrapartum prophylaxis, prenatal labs, fever, blood type,
     medications or substances); feeding, wet diapers and stools; growth; development; immunizations ("up to date"
     unless they matter); daycare and sick contacts; home and safety.
   - Labs plausible for age, in US conventional units, with no reference ranges. The app's lab sheet shows adult
     ranges, so an item must not hinge on a value that is normal for the child's age but abnormal for an adult (or the
     reverse) unless the explanation gives the age-normal range.
   - Weight-based doses within maximums, with the arithmetic shown in the explanation.
   - Describe findings instead of naming them: no pathognomonic buzzword or eponym that hands over the diagnosis. The
     reader should have to put the findings together, then decide what to do.
   - Race or ethnicity only when clinically relevant (the explanation says why); no stereotyped families. Suspected
     abuse follows AAP guidance and the explanation states the duty to report; adolescents get time alone and
     confidentiality as appropriate; safety-sensitive content follows spec §2 rule 9.
   - Lead-in from spec §4. Five homogeneous options: short (a few words, never a sentence), parallel, and in
     alphabetical or logical order.
   - Answer letters balanced across the block, counting its earlier pairs: no letter more than twice in 8, and never one
     letter three times in a row.

4. Board-quality audit, per question. Fix and re-audit until every line is true, and record the result in the sources
   file:
   - Cover the options: an expert reading only the vignette and lead-in can name the answer.
   - One best answer: write the strongest case for each distractor under current guidelines; if any case holds up,
     change the stem.
   - The decision turns on the design brief's detail. That clue is present but not flagged (not the last line, no
     "notably" or "of note"), and the one or two red herrings are realistic and dismissible by a stated finding.
   - No cues: the key is not the longest or most specific option (compare lengths); no stem word repeated only in the
     key; no absolutes; no two options that mean the same thing or contain each other; the key doesn't share the most
     elements with the other options; numbers formatted alike; no "all/none of the above"; no EXCEPT or NOT stems.
   - It reads like the blueprint's calibration notes (length, density of findings, option style), and its stars match
     spec §3. A ★★★★★ needs an interval change and a tempting answer that would harm this child.
   - The explanation follows spec §6, shows every calculation, names the guideline with its recommendation number or
     grade, and each "why wrong" says when that option would be right.
   - Original: search the web for the scenario's distinctive phrasing and decision, and rewrite from scratch if it
     resembles a published question. It repeats no decision point in spec §9 or an earlier pediatric pair.
   - The spec §10 self-audit passes.

5. Numbers. Write review/peds_pair_NN_check.py (like review/chem_phys_batch_04_check.py) to re-derive and assert every
   number the items state or depend on: doses and volumes per kg, fluid rates, gaps and corrections, scores, days of
   life and corrected age, growth percentiles (from WHO or CDC LMS values, embedded with their source), and the
   threshold each decision rests on, with the vignette's value far enough from it that an older or newer guideline
   version would not flip the answer (spec §2 rule 3). Run it; every check must pass.

6. Save and build. The first pair of a block creates questions/questionsN.py (header comment and list QUESTIONSN, as in
   questions3.py) and imports and appends it in build.py; later pairs append to that list. Use the same keys as
   questions3.py plus "status": "draft" and "reviewed_by": "". In build.py, SYS is "Pediatrics" for each new ID;
   "discipline" is "Pediatrics" or "Pediatrics / <subspecialty or setting>"; "system" uses the NBME outline's wording.
   Run python build.py, python tests/smoke.py, python tests/overflow.py and python tests/three_d.py, and fix any
   failure.

7. Independent fact-check. Write the key packet:
       python tools/board_review_packet.py questions/questionsN.py <id1>,<id2> review/peds_pair_NN.md
   Launch a fresh subagent with only that packet and this instruction: "You are a pediatric board item reviewer. For
   each question, fetch every cited source and confirm each factual claim and the keyed answer against it; confirm the
   guideline version is current; redo the arithmetic; check the vital signs, labs, growth and development for the
   child's age; argue for each distractor; and list every problem with its source." Fix what it finds, re-run steps 5
   and 6, and log the outcome in the sources file. If you can't launch a subagent, do this pass yourself as a skeptic,
   re-fetching every source.

8. Packets. Regenerate the key packet, then the blind one (the same command with review/peds_pair_NN_blind.md and
   --blind). Open the blind packet and confirm it shows no answer, topic, system, discipline, difficulty, explanation or
   source. Set both blueprint rows to "checked" and add a changelog line. Leave spec §9 alone until the pair passes.

9. Report, per question: ID, topic, decision tested, answer, stars, and key source with year and grade. Anything you
   couldn't verify must be fixed or replaced now, not handed to the blind re-solve. End with:
   "Next: start a new conversation and run /peds-blind."
