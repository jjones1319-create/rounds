# MCAT Question Generator — Master Spec

**Version:** 1.8 · **Created:** 2026-10-10 · **Updated:** 2026-10-15 · **Blocks produced so far:** 9 (M1–M7, M4B, CP1)

The single source of truth for writing MCAT-style practice content for Rounds. It mirrors
`docs/board_question_generator_spec.md`, adapted to how the MCAT actually works: four sections,
four answer choices, and mostly **passage-based** question sets.

How to use: ask Claude Code, for example, "Write MCAT Block 1 per docs/MCAT_SPEC.md: 8 discrete
questions for Chem/Phys." It must read this whole file first, follow every rule in §3, and update
§10 and §11 when done.

---

## 1. Exam facts (verified 2026-10-10; re-check at the start of each block)

Source of record: AAMC, *What's on the MCAT Exam?* and the per-section content outlines
(students-residents.aamc.org). Third-party summaries were used only to cross-check. AAMC has made
no format change for the 2026 testing year.

| Section (exam order) | Questions | Time | Format |
|---|---|---|---|
| Chemical and Physical Foundations of Biological Systems (**Chem/Phys**) | 59 | 95 min | ~44 passage-based + 15 discrete |
| Critical Analysis and Reasoning Skills (**CARS**) | 53 | 90 min | all passage-based |
| Biological and Biochemical Foundations of Living Systems (**Bio/Biochem**) | 59 | 95 min | ~44 passage-based + 15 discrete |
| Psychological, Social, and Biological Foundations of Behavior (**Psych/Soc**) | 59 | 95 min | ~44 passage-based + 15 discrete |

- Every question has **four** answer choices (A–D), one correct.
- Each section is scored 118–132 (total 472–528) through AAMC's equating, which we **cannot** reproduce.
- **No calculator.** A periodic table is provided in the science sections. Calculus is not required;
  expected math includes arithmetic, ratios, exponents, logarithms, scientific notation, and estimation.
- Pacing: about 1.6 minutes per question in the science sections, about 1.7 in CARS.

## 2. Blueprint (AAMC weightings)

**Chem/Phys:** general chemistry 30%, biochemistry 25%, physics 25%, organic chemistry 15%, biology 5%.
Foundational Concepts 4 (40%) and 5 (60%).

**Bio/Biochem:** biology 65%, biochemistry 25%, general chemistry 5%, organic chemistry 5%.
Foundational Concepts 1 (55%), 2 (20%), 3 (25%).

**Psych/Soc:** psychology 65%, sociology 30%, biology 5%.
Foundational Concepts 6 (25%), 7 (35%), 8 (20%), 9 (15%), 10 (5%).

**Scientific Inquiry and Reasoning Skills (all three science sections):**
Skill 1 Knowledge of scientific concepts and principles (35%) · Skill 2 Scientific reasoning and
problem-solving (45%) · Skill 3 Reasoning about the design and execution of research (10%) ·
Skill 4 Data-based and statistical reasoning (10%).

**CARS:** passages 50% humanities, 50% social sciences. Skills: Foundations of Comprehension (30%),
Reasoning Within the Text (30%), Reasoning Beyond the Text (40%). No outside knowledge required.

**Content categories** (tag every science question with one; confirm the exact wording against the AAMC outline):
- FC1: 1A proteins and amino acids · 1B gene to protein · 1C heredity and genetic diversity · 1D bioenergetics and fuel metabolism
- FC2: 2A assemblies of molecules, cells, and tissues · 2B prokaryotes and viruses · 2C cell division, differentiation, specialization
- FC3: 3A nervous and endocrine systems · 3B main organ systems
- FC4: 4A motion, forces, work, energy, equilibrium · 4B fluids and gas exchange · 4C electrochemistry and circuits · 4D light and sound · 4E atoms, nuclear decay, electronic structure
- FC5: 5A water and solutions · 5B molecules and intermolecular interactions · 5C separation and purification · 5D structure, function, reactivity of biological molecules · 5E thermodynamics and kinetics
- FC6: 6A sensing the environment · 6B making sense of the environment · 6C responding to the world
- FC7: 7A individual influences on behavior · 7B social processes · 7C attitude and behavior change
- FC8: 8A self-identity · 8B social thinking · 8C social interactions
- FC9: 9A social structure · 9B demographics · FC10: 10A social inequality

## 3. Non-negotiable accuracy and integrity rules

1. **Verify every fact before writing it.** Use named, citable references: the AAMC outline for scope;
   peer-reviewed open textbooks (OpenStax, LibreTexts) and standard texts for content; NIST CODATA for
   physical constants; IUPAC for atomic masses and nomenclature. Search the web; never rely on memory alone.
   **Check each OpenStax book's license on its own page before adapting anything** (licenses differ by book
   and have changed); citing a fact is always fine, copying text or figures is not.
2. **Show the math.** Every numeric item includes a worked solution using MCAT-friendly numbers that can be
   done without a calculator, plus the estimation shortcut. Check units and significant figures.
3. **Exactly one defensible answer.** If an expert could argue for a second choice, rewrite.
4. **Original content only.** Never take questions from any website, question bank, or prep source (AAMC,
   Khan Academy, Kaplan, UWorld, Blueprint, Princeton Review, forums, or any other). Publicly available official
   AAMC sample questions may be read only to understand structure, style, and difficulty; never copy, paraphrase,
   or adapt their content. If a draft turns out to resemble a published question, rewrite it from scratch.
5. **Experiments in passages are hypothetical** and labeled as such, built on established science with
   internally consistent data. If a passage is based on a real study, paraphrase it and cite it; never invent
   a citation or attribute invented data to real researchers.
6. **CARS passages** are either (a) original prose written for this project, or (b) excerpts of works in the
   US public domain (as of 2026: published in 1930 or earlier), cited with author, title, and year.
   Modern translations of old works are usually still copyrighted; use only public-domain translations.
   Never use copyrighted modern essays, articles, or books.
7. **Sensitive topics** (race, gender, disability, mental illness, addiction) in Psych/Soc and CARS are written
   respectfully and accurately, using current terminology, without stereotypes.
8. **Never guess.** If something can't be verified, drop it or list it under "Open issues."
9. **No recalled exam content.** Never write, accept, or adapt a question described as coming from a real MCAT,
   and never claim a topic "appears often" beyond AAMC's published weightings. Base all scope decisions on the
   public AAMC outline only.
10. **Every item is tagged to topics** from the section guide (`docs/MCAT_GUIDES_SPEC.md`). Write the guide
   topic first if it doesn't exist yet.

## 4. Difficulty rubric

| Stars | Label | Description |
|---|---|---|
| ★★ | Foundational | One-step recall or a single calculation. Good for first-pass content review. |
| ★★★ | Exam standard | Typical MCAT difficulty: apply one concept to the passage or a new situation. |
| ★★★★ | Above standard | Two linked steps, or extracting what matters from data or a figure. |
| ★★★★★ | Hardest exam-level | Novel experimental reasoning, integration across disciplines, a tempting trap. |

Start blocks at ★★–★★★ while the app's MCAT section is new; move toward the AAMC mix over time.

## 5. Item formats

**Discrete question:** a stem (often one or two sentences of setup) plus four choices.

**Passage set:**
- Science passages: about 250–500 words, often describing an experiment, with any combination of a table,
  a graph, an equation, or a structure. 4–7 questions per passage. At least one question should be answerable
  from outside knowledge alone, and at least one should require the passage.
- CARS passages: about 500–600 words of humanities or social-science prose with a clear argument, nuance, and
  an identifiable authorial stance. 5–7 questions spread across the three CARS skills.

**Answer choices:** exactly four, parallel in grammar and length, ordered logically (numeric choices ascending).
No "all of the above" or "none of the above." Each wrong choice embodies one named error: sign or unit error,
wrong formula, misread graph, reversed relationship, true but irrelevant, too extreme, out of scope,
outside knowledge contradicting the passage (these three are typical of CARS but may be used wherever they fit). Across a block, each letter is the answer 20–30% of the
time, never the same letter three times in a row.

**Figures:** generated from the data stored with the question (SVG), never hand-typed separately, so figure and
data cannot disagree. Every figure has a text description for screen readers. Axis labels include units.
Chemical structures come from SMILES rendered at build time (see `docs/PLAN_MCAT.md`).

## 6. Explanation template

1. Correct answer and a one-line summary of why.
2. Worked reasoning: the key passage line (quoted, under 25 words) or the governing principle, then the math
   step by step with the no-calculator shortcut.
3. Why each wrong choice is wrong, naming the error it represents.
4. Tags: section, discipline, foundational concept and content category (or CARS skill), Scientific Inquiry
   and Reasoning Skill, difficulty.
5. Takeaway: one testable sentence.
6. Source(s): reference used to verify, with year.

## 7. Review workflow

Every item and passage carries `status` (`draft` → `reviewed`) and `reviewed_by`. The review gate is an **independent blind re-solve**: a fresh Claude Code session that has not seen the batch re-solves every item from the blind packet (`review/<section>_batch_NN_blind.md`, questions only), and its answers and reasoning are compared with the key in `review/<section>_batch_NN.md`. Items that agree, with no flaw found in the stem, choices, or solution, get `status: reviewed` and `reviewed_by: "independent blind re-solve"`; a disagreement is resolved by checking the sources, the item is fixed, and it is re-solved blind again. A batch is committed and pushed only after every item passes.

**How it runs.** `py tools/review_packet.py <block.json> review/<name>.md` writes the key (every question with its answer,
worked solution, why each wrong choice is wrong, tags and sources); `--blind` writes the questions-only packet
`review/<name>_blind.md`. The re-solving session is given only the blind packet and the guide, re-solves every item with
its own worked reasoning, and reports an answer and any objection per item (ambiguity, a second defensible choice, a
number that needs a calculator, a clue in the choices, a resemblance to a published question). The writing session then
compares against the key: agreement with no objection passes; anything else is checked against the sources, fixed with
`rev` incremented if the item had been published, logged in §11, and re-solved blind again. Guide topics are reviewed the
same way (a fresh session checks each topic's statements against the cited sources) and keep their Reviewed ticks.

The owner, who holds degrees in biology, chemistry, mathematics, and physics, does not review items in the app; the
Phase M4 Content review screen (Progress → Content review) is unused. A "Beta" label for unreviewed items is optional
and off by default (`BETA_LABEL` in `build.py`), so unreviewed items display without a label unless it is turned on.

## 8. Data schema (one JSON file per block in `content/mcat/`)

```json
{
  "block": "M1",
  "passages": [
    {
      "id": "M1-P01", "section": "chem_phys", "kind": "science", "title": "Optional",
      "text": ["paragraph", "paragraph"],
      "figures": [{ "id": "fig1", "type": "line|bar|scatter|table|structure|equation",
                    "data": {}, "caption": "", "alt": "" }],
      "source": "Hypothetical experiment based on <reference>", "status": "draft", "reviewed_by": null
    }
  ],
  "items": [
    {
      "id": "M1-Q01", "rev": 1, "section": "chem_phys", "passage": "M1-P01 or null",
      "discipline": "physics", "fc": "4", "category": "4B", "topics": ["4B.bernoulli"],
      "skill": "2", "cars_skill": null,
      "difficulty": 3, "stem": "", "options": { "A": "", "B": "", "C": "", "D": "" }, "answer": "B",
      "why_correct": [""], "why_wrong": { "A": "", "C": "", "D": "" },
      "error_types": { "A": "", "C": "", "D": "" }, "takeaway": "", "sources": [""],
      "status": "draft", "reviewed_by": null
    }
  ]
}
```

IDs are permanent (progress is keyed by them). Corrections increment `rev` and are logged in §11. Planned Chem/Phys batches (`docs/CHEM_PHYS_250.md`) live in `content/mcat/chem_phys/batch_NN.json` with block id `CP<N>` and the permanent ids `CP-001`… and `CP-P01`… assigned in the plan; `tools/validate.py` checks that each batch file holds exactly its own ids.

Figure `data` by type (checked by `tools/validate.py`): `table` {columns: [..], rows: [[..]]}; `line` / `scatter` {x: {label, min?, max?}, y: {label, min?, max?}, series: [{name, points: [[x, y], ..]}]}; `bar` {x: {label}, y: {label, min?, max?}, series: [{name, points: [[category, value], ..]}]}; `equation` {tex}; `structure` {smiles} (build.py adds `svg`, drawn with RDKit). The app draws charts from these numbers; `alt` describes the figure for screen readers. Block ids may carry a category letter for single-category blocks (`M4B`, items `M4B-Q01`).

## 9. Self-audit before delivering (all must be "yes")

- [ ] Each fact verified against a named source this session; each numeric answer re-derived independently
- [ ] Exactly one defensible answer; four parallel choices; each distractor has a named error type
- [ ] Math is calculator-free with MCAT-friendly numbers; units and significant figures checked
- [ ] Passages: data internally consistent, figures generated from stored data, hypothetical studies labeled
- [ ] CARS: original or US public-domain text with citation; questions answerable from the passage alone
- [ ] Tags complete (section, discipline, FC/category, guide topic IDs or CARS skill, Skill, difficulty); blueprint mix noted
- [ ] Original wording; nothing taken from, paraphrased from, or adapted from any published question
- [ ] `tools/validate.py` passes; app builds; tests pass
- [ ] §10 log and §11 changelog updated
- [ ] Independent blind re-solve passed for every item (§7) before any commit or push

## 10. Item log

| ID | Section | Category / skill | Topic | Ans | Diff | Status | Key source |
|---|---|---|---|---|---|---|---|
| M1-Q01 | chem_phys | 4A / S2 | 4A.energy | C | ★★ | draft | OpenStax College Physics 2e, 7.3 Gravitational Potential Energy |
| M1-Q02 | chem_phys | 4C / S2 | 4C.resistance | B | ★★★ | draft | OpenStax College Physics 2e, 21.1 Resistors in Series and Parallel |
| M1-Q03 | chem_phys | 4D / S2 | 4D.reflection-refraction | C | ★★★ | draft | OpenStax College Physics 2e, 25.4 Total Internal Reflection |
| M1-Q04 | chem_phys | 4E / S2 | 4E.radioactive-decay | B | ★★★ | draft | OpenStax College Physics 2e, 31.5 Half-Life and Activity |
| M1-Q05 | chem_phys | 5A / S2 | 5A.buffers | D | ★★★ | draft | OpenStax Chemistry 2e, 14.6 Buffers |
| M1-Q06 | chem_phys | 5E / S3 | 5E.enzymes-mechanism | A | ★★★ | draft | OpenStax Biology 2e, 6.5 Enzymes |
| M1-Q07 | chem_phys | 5D / S1 | 5D.carbonyl-addition | D | ★★★ | draft | OpenStax Organic Chemistry, 25.5 Cyclic Structures of Monosaccharides |
| M1-Q08 | chem_phys | 5E / S4 | 5E.enzyme-inhibition-regulation | A | ★★★ | draft | Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 4.2 Control of Enzymatic Activity |
| M2-Q01 | bio_biochem | 1A / S4 | 1A.enzyme-control | B | ★★★ | draft | Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 4.1 Basic Principles of Catalysis |
| M2-Q02 | bio_biochem | 1B / S2 | 1B.genetic-code | D | ★★ | draft | OpenStax Microbiology, 11.4 Protein Synthesis (Translation) |
| M2-Q03 | bio_biochem | 1C / S2 | 1C.analytic-methods | C | ★★★ | draft | OpenStax Biology 2e, 19.1 Population Evolution |
| M2-Q04 | bio_biochem | 1D / S1 | 1D.citric-acid-cycle | A | ★★★ | draft | OpenStax Biology 2e, 7.3 Oxidation of Pyruvate and the Citric Acid Cycle |
| M2-Q05 | bio_biochem | 2A / S2 | 2A.membrane-transport | B | ★★★ | draft | OpenStax Biology 2e, 5.2 Passive Transport |
| M2-Q06 | bio_biochem | 2C / S1 | 2C.mitosis-cell-cycle | D | ★★ | draft | OpenStax Biology 2e, 10.2 The Cell Cycle |
| M2-Q07 | bio_biochem | 3A / S2 | 3A.nerve-cell | A | ★★★ | draft | OpenStax Biology 2e, 35.2 How Neurons Communicate |
| M2-Q08 | bio_biochem | 3B / S3 | 3B.excretory | C | ★★★ | draft | OpenStax Biology 2e, 41.5 Hormonal Control of Osmoregulatory Functions |
| M3-Q01 | psych_soc | 6A / S2 | 6A.sensation-thresholds | B | ★★ | draft | OpenStax Psychology 2e, 5.1 Sensation versus Perception |
| M3-Q02 | psych_soc | 6B / S1 | 6B.memory-retrieval-forgetting | C | ★★★ | draft | OpenStax Psychology 2e, 8.3 Problems with Memory |
| M3-Q03 | psych_soc | 6C / S2 | 6C.emotion | A | ★★★ | draft | OpenStax Psychology 2e, 10.4 Emotion |
| M3-Q04 | psych_soc | 7C / S2 | 7C.operant | D | ★★★ | draft | OpenStax Psychology 2e, 6.3 Operant Conditioning |
| M3-Q05 | psych_soc | 6C / S3 | 6C.stress | B | ★★★ | draft | OpenStax Psychology 2e, 2.3 Analyzing Findings |
| M3-Q06 | psych_soc | 8B / S2 | 8B.attribution | C | ★★★ | draft | OpenStax Psychology 2e, 12.1 What Is Social Psychology? |
| M3-Q07 | psych_soc | 9A / S2 | 9A.theoretical-approaches | A | ★★★ | draft | OpenStax Introduction to Sociology 3e, 1.3 Theoretical Perspectives in Sociology |
| M3-Q08 | psych_soc | 10A / S4 | 10A.social-class | D | ★★★ | draft | OpenStax Introduction to Sociology 3e, 19.3 Health in the United States |
| M4-Q01 | chem_phys | 4C / S4 | 4C.current-voltage | C | ★★★ | draft | OpenStax College Physics 2e, 21.2 Electromotive Force |
| M4-Q02 | chem_phys | 4C / S2 | 4C.current-voltage | B | ★★★ | draft | OpenStax College Physics 2e, 21.2 Electromotive Force |
| M4-Q03 | chem_phys | 4C / S2 | 4C.resistance | A | ★★★★ | draft | OpenStax College Physics 2e, 21.2 Electromotive Force |
| M4-Q04 | chem_phys | 4C / S2 | 4C.resistance | C | ★★★ | draft | OpenStax College Physics 2e, 21.2 Electromotive Force |
| M4-Q05 | chem_phys | 4C / S1 | 4C.current-voltage | D | ★★ | draft | OpenStax College Physics 2e, 21.2 Electromotive Force |
| M5-Q01 | bio_biochem | 2B / S4 | 2B.prokaryote-growth | B | ★★★ | draft | OpenStax Microbiology, 9.1 How Microbes Grow |
| M5-Q02 | bio_biochem | 2B / S2 | 2B.prokaryote-growth | C | ★★★ | draft | OpenStax Microbiology, 9.1 How Microbes Grow |
| M5-Q03 | bio_biochem | 2B / S3 | 2B.prokaryote-genetics | A | ★★★ | draft | OpenStax Microbiology, 11.6 How Asexual Prokaryotes Achieve Genetic Diversity |
| M5-Q04 | bio_biochem | 2B / S1 | 2B.prokaryote-structure | D | ★★★ | draft | OpenStax Microbiology, 14.3 Mechanisms of Antibacterial Drugs |
| M5-Q05 | bio_biochem | 2B / S2 | 2B.prokaryote-growth | C | ★★★ | draft | OpenStax Microbiology, 9.1 How Microbes Grow |
| M6-Q01 | psych_soc | 6B / S3 | 6B.memory-encoding-storage | A | ★★ | draft | OpenStax Psychology 2e, 2.3 Analyzing Findings |
| M6-Q02 | psych_soc | 6B / S4 | 6B.memory-retrieval-forgetting | C | ★★★ | draft | OpenStax Psychology 2e, 2.3 Analyzing Findings |
| M6-Q03 | psych_soc | 6B / S2 | 6B.memory-encoding-storage | B | ★★★ | draft | OpenStax Psychology 2e, 8.4 Ways to Enhance Memory |
| M6-Q04 | psych_soc | 6B / S4 | 6B.memory-retrieval-forgetting | A | ★★★★ | draft | OpenStax Introductory Statistics 2e, 9.4 Rare Events, the Sample, and the Decision and Conclusion |
| M6-Q05 | psych_soc | 6B / S2 | 6B.memory-retrieval-forgetting | D | ★★★ | draft | OpenStax Psychology 2e, 8.3 Problems with Memory |
| M7-Q01 | cars | CARS / foundations | M7-P01 | C | ★★★ | draft | AAMC, What's on the MCAT Exam?, Critical Analysis and Reasoning Skills section overview |
| M7-Q02 | cars | CARS / foundations | M7-P01 | B | ★★★ | draft | AAMC, What's on the MCAT Exam?, Critical Analysis and Reasoning Skills section overview |
| M7-Q03 | cars | CARS / within | M7-P01 | A | ★★★ | draft | AAMC, What's on the MCAT Exam?, Critical Analysis and Reasoning Skills section overview |
| M7-Q04 | cars | CARS / within | M7-P01 | D | ★★★★ | draft | AAMC, What's on the MCAT Exam?, Critical Analysis and Reasoning Skills section overview |
| M7-Q05 | cars | CARS / beyond | M7-P01 | C | ★★★★ | draft | AAMC, What's on the MCAT Exam?, Critical Analysis and Reasoning Skills section overview |
| M7-Q06 | cars | CARS / beyond | M7-P01 | C | ★★★★ | draft | AAMC, What's on the MCAT Exam?, Critical Analysis and Reasoning Skills section overview |
| M7-Q07 | cars | CARS / foundations | M7-P02 | B | ★★★ | draft | AAMC, What's on the MCAT Exam?, Critical Analysis and Reasoning Skills section overview |
| M7-Q08 | cars | CARS / foundations | M7-P02 | A | ★★ | draft | AAMC, What's on the MCAT Exam?, Critical Analysis and Reasoning Skills section overview |
| M7-Q09 | cars | CARS / within | M7-P02 | A | ★★★ | draft | AAMC, What's on the MCAT Exam?, Critical Analysis and Reasoning Skills section overview |
| M7-Q10 | cars | CARS / within | M7-P02 | B | ★★★ | draft | AAMC, What's on the MCAT Exam?, Critical Analysis and Reasoning Skills section overview |
| M7-Q11 | cars | CARS / beyond | M7-P02 | D | ★★★★ | draft | AAMC, What's on the MCAT Exam?, Critical Analysis and Reasoning Skills section overview |
| M7-Q12 | cars | CARS / beyond | M7-P02 | D | ★★★★ | draft | AAMC, What's on the MCAT Exam?, Critical Analysis and Reasoning Skills section overview |
| M4B-Q01 | chem_phys | 4B / S2 | 4B.density-buoyancy | A | ★★★ | draft | OpenStax College Physics 2e, 11.7 Archimedes' Principle |
| M4B-Q02 | chem_phys | 4B / S4 | 4B.hydrostatic-pressure | B | ★★★ | draft | OpenStax College Physics 2e, 11.4 Variation of Pressure with Depth in a Fluid |
| M4B-Q03 | chem_phys | 4B / S2 | 4B.viscosity-poiseuille | A | ★★★ | draft | OpenStax College Physics 2e, 12.4 Viscosity and Laminar Flow; Poiseuille's Law |
| M4B-Q04 | chem_phys | 4B / S2 | 4B.continuity-bernoulli | C | ★★ | draft | OpenStax College Physics 2e, 12.1 Flow Rate and Its Relation to Velocity |
| M4B-Q05 | chem_phys | 4B / S4 | 4B.continuity-bernoulli | B | ★★★★ | draft | OpenStax College Physics 2e, 12.2 Bernoulli's Equation |
| M4B-Q06 | chem_phys | 4B / S1 | 4B.turbulence-surface-tension | C | ★★ | draft | OpenStax College Physics 2e, 12.5 The Onset of Turbulence |
| M4B-Q07 | chem_phys | 4B / S2 | 4B.circulation | A | ★★★ | draft | OpenStax College Physics 2e, 12.1 Flow Rate and Its Relation to Velocity |
| M4B-Q08 | chem_phys | 4B / S2 | 4B.ideal-gas | D | ★★★ | draft | OpenStax Chemistry 2e, 9.2 Relating Pressure, Volume, Amount, and Temperature |
| M4B-Q09 | chem_phys | 4B / S1 | 4B.kinetic-theory | C | ★★★ | draft | OpenStax Chemistry 2e, 9.5 The Kinetic-Molecular Theory |
| M4B-Q10 | chem_phys | 4B / S3 | 4B.partial-pressure | D | ★★★ | draft | OpenStax Chemistry 2e, 9.3 Stoichiometry of Gaseous Substances, Mixtures, and Reactions |
| CP-001 | chem_phys | 4B / S2 | 4B.continuity-bernoulli | C | ★★★ | reviewed | OpenStax College Physics 2e, 12.1 Flow Rate and Its Relation to Velocity |
| CP-002 | chem_phys | 4B / S4 | 4B.continuity-bernoulli | A | ★★★★★ | reviewed | OpenStax College Physics 2e, 12.2 Bernoulli's Equation |
| CP-003 | chem_phys | 4B / S2 | 4B.viscosity-poiseuille | A | ★★★★ | reviewed | OpenStax College Physics 2e, 12.4 Viscosity and Laminar Flow; Poiseuille's Law |
| CP-004 | chem_phys | 4B / S1 | 4B.turbulence-surface-tension | B | ★★★ | reviewed | OpenStax College Physics 2e, 12.5 The Onset of Turbulence |
| CP-005 | chem_phys | 4B / S3 | 4B.circulation | D | ★★★ | reviewed | OpenStax Anatomy and Physiology 2e, 20.2 Blood Flow, Blood Pressure, and Resistance |
| CP-006 | chem_phys | 5A / S2 | 5A.buffers | B | ★★★★ | reviewed | Acid-Base Physiology (Brandis), 2.2 Buffering (anaesthesiamcq.com) |
| CP-007 | chem_phys | 5A / S1 | 5A.acids-bases | A | ★★ | reviewed | OpenStax Chemistry 2e, 14.1 Brønsted-Lowry Acids and Bases |
| CP-008 | chem_phys | 5A / S4 | 5A.titration | A | ★★★★ | reviewed | OpenStax Chemistry 2e, 14.7 Acid-Base Titrations |
| CP-009 | chem_phys | 5A / S2 | 5A.buffers | B | ★★★★ | reviewed | OpenStax Chemistry 2e, 14.6 Buffers |
| CP-010 | chem_phys | 5A / S3 | 5A.weak-acid-equilibria | C | ★★★ | reviewed | OpenStax Chemistry 2e, 13.3 Shifting Equilibria |
| CP-011 | chem_phys | 5E / S4 | 5E.enzyme-kinetics | D | ★★★ | reviewed | Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 4.1 Basic Principles of Catalysis |
| CP-012 | chem_phys | 5E / S2 | 5E.enzyme-kinetics | C | ★★★★ | reviewed | Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 4.1 Basic Principles of Catalysis |
| CP-013 | chem_phys | 5E / S2 | 5E.enzyme-inhibition-regulation | A | ★★★★ | reviewed | Chemistry LibreTexts, Biochemistry Online (Jakubowski), Competitive Inhibition: Kmapp = Km(1 + I/Kis) |
| CP-014 | chem_phys | 5E / S1 | 5E.enzymes-mechanism | B | ★★ | reviewed | OpenStax Biology 2e, 6.5 Enzymes |
| CP-015 | chem_phys | 5E / S3 | 5E.enzyme-inhibition-regulation | A | ★★★★★ | reviewed | Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 4.2 Control of Enzymatic Activity |
| CP-016 | chem_phys | 4E / S2 | 4E.radioactive-decay | B | ★★★★ | reviewed | OpenStax College Physics 2e, 31.5 Half-Life and Activity |
| CP-017 | chem_phys | 4E / S2 | 4E.radioactive-decay | D | ★★★★ | reviewed | OpenStax College Physics 2e, 31.5 Half-Life and Activity |
| CP-018 | chem_phys | 4E / S1 | 4E.nucleus-isotopes | C | ★★★ | reviewed | OpenStax College Physics 2e, 31.4 Nuclear Decay and Conservation Laws |
| CP-019 | chem_phys | 4D / S2 | 4D.em-radiation | A | ★★ | reviewed | OpenStax College Physics 2e, 29.3 Photon Energies and the Electromagnetic Spectrum |
| CP-020 | chem_phys | 4A / S1 | 4A.units-vectors | B | ★★ | reviewed | NIST Special Publication 811, Guide for the Use of the International System of Units, Table 3 |
| CP-021 | chem_phys | 4E / S1 | 4E.periodic-groups | D | ★★ | reviewed | OpenStax Chemistry 2e, 2.5 The Periodic Table |
| CP-022 | chem_phys | 5B / S1 | 5B.lewis-structures | C | ★★★ | reviewed | OpenStax Chemistry 2e, 7.4 Formal Charges and Resonance |
| CP-023 | chem_phys | 5D / S1 | 5D.lipids | C | ★★ | reviewed | OpenStax Organic Chemistry, 27.4 Prostaglandins and Other Eicosanoids |
| CP-024 | chem_phys | 5E / S2 | 5E.rate-laws | B | ★★★ | reviewed | OpenStax Chemistry 2e, 12.3 Rate Laws |
| CP-025 | chem_phys | 5D / S1 | 5D.amino-acids | D | ★★ | reviewed | OpenStax Biology 2e, 3.4 Proteins |

## 11. Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-10 | Spec created. |
| 1.1 | 2026-10-10 | Added topic tagging to section guides (§3.10, §8) and the no-recalled-content rule (§3.9). |
| 1.2 | 2026-10-10 | Owner decisions applied: §3.4 now bans taking questions from any website or prep source (official samples may be read only for structure, style, and difficulty); §7 makes the owner the reviewer of all content, drops the second-reviewer requirement, and makes the Beta label optional and off by default; §9 wording updated. |
| 1.3 | 2026-10-11 | Phase M2 starter blocks M1 (Chem/Phys), M2 (Bio/Biochem), M3 (Psych/Soc): 8 discrete items each, all `draft`, each re-derived and fact-checked against the cited open textbooks before commit; §10 item log started. |
| 1.4 | 2026-10-11 | Phase M3: passage blocks M4 (Chem/Phys), M5 (Bio/Biochem), M6 (Psych/Soc) and M7 (two original CARS passages, humanities and social sciences), 22 items; figure data shapes documented in §8; letter-share warning applies to blocks of 8 or more items. |
| 1.5 | 2026-10-11 | Block M4B (`content/mcat/4B.json`): 10 discrete Chem/Phys questions covering every 4B topic but real gases, each re-derived and checked against OpenStax; the validator accepts `4B.json` for block `M4B`. Phase M4 review workflow documented in §7. |
| 1.6 | 2026-10-15 | Chem/Phys batch 1 (`content/mcat/chem_phys/batch_01.json`, block `CP1`): passages CP-P01–CP-P04 and items CP-001–CP-025 per `docs/CHEM_PHYS_250.md`, all `draft`; every number re-derived in `review/chem_phys_batch_01_check.py`, structures checked with RDKit, facts verified against the cited sources; review packet `review/chem_phys_batch_01.md` from `tools/review_packet.py`; validator widened for batch files (§8). |
| 1.7 | 2026-10-15 | Review gate (§7) changed by the owner: the independent blind re-solve replaces the in-app review; passing items get `reviewed_by: "independent blind re-solve"`; a batch is committed and pushed only after it passes. `tools/apply_review.py` removed; `tools/review_packet.py --blind` added. §9 checklist item added. |
| 1.8 | 2026-10-15 | Chem/Phys batch 1 passed the independent blind re-solve (25 of 25 agreed) and was pushed; all CP-001–CP-025 and CP-P01–CP-P04 `reviewed`. Fixes at review: CP-P01 Figure 1 made linear along the narrowed segment and CP-002 reads the entry at x = 20 mm; CP-005 choice B reworded; CP-013 rewritten to ask for Ki and CP-016 to bracket when a vial fell below the prescribed dose (both duplicated starter items M1-Q08 and M1-Q04); CP-023 re-rated ★★. No `rev` increments: the items had not been published. |
