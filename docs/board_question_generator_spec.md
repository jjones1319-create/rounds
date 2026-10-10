# Board Question Generator — Master Spec

**Version:** 1.3 · **Created:** 2026-10-04 · **Updated:** 2026-10-10 · **Blocks produced so far:** 3 (24 questions)

This file is the single source of truth for generating board-prep question blocks (and, later, the app). Upload it at the start of any new session and say something like:

> "Using board_question_generator_spec.md, make Block 2: 8 questions, focus on psych, peds, and surgery, as a PDF. Update the question log and changelog in the spec."

Claude should read the whole spec, follow every rule in §2, and return (1) the new PDF and (2) an updated copy of this spec with §9 and §11 filled in.

---

## 1. Target

| Setting | Value |
|---|---|
| Exam | USMLE Step 2 CK (change here if she is taking Step 3, COMLEX, or a shelf exam) |
| Format | Single-best-answer clinical vignettes, 5 options (A–E) |
| Main task tested | "Most appropriate next step in management" (about 70%); also diagnosis, best initial/most accurate test, and prevention/screening |
| Difficulty floor | ★★★ (see §3). Never easier. |
| Calibration anchor | Her sample question (20-year-old woman, NSAIDs plus bulimia, hematemesis after repeated vomiting, tachycardia, Hb 10, answer EGD) = ★★★. Do **not** reproduce it; it belongs to a commercial QBank. |
| Real-exam pacing | Step 2 CK uses 60-minute blocks of up to 40 questions (about 90 seconds each). Confirm at usmle.org before relying on this for app timing. |

---

## 2. Non-negotiable accuracy rules

1. **Anchor every answer to a named source.** Each correct answer must trace to a current society guideline, consensus statement, or landmark trial, cited with year on the explanation page. Preferred: ACC/AHA, AHA/ASA, ADA, IDSA, ACOG, AAP, ASH, CHEST, ACG, AASLD, KDIGO, USPSTF, ACR Appropriateness Criteria, Surviving Sepsis Campaign, GOLD, GINA, APA.
2. **Re-verify with web search at generation time.** Guidelines change. Example: the 2024 DKA consensus moved the "hold insulin" potassium threshold from 3.3 to 3.5 mEq/L. Record the verification date per question (`verified_on`).
3. **Make answers robust across guideline versions** where possible (e.g., use K⁺ 2.9 so the answer is the same under the 2009 and 2024 DKA thresholds).
4. **Exactly one defensible best answer.** If a reasonable expert could argue for a second option, rewrite the stem or the option. Add stem details that close loopholes (e.g., "the cath lab has been activated").
5. **Check the numbers.** Every vignette must be internally consistent: anion gap, corrected sodium, osmolality, A–a gradient, and scores (4Ts, Wells, CURB-65, MELD, CHA₂DS₂-VASc). Show the arithmetic in the explanation.
6. **Realistic data.** Vitals and labs plausible for age and condition; US conventional units; no reference ranges printed (the real exam provides a separate lab table).
7. **Original content only.** Never take questions from any website, question bank, or prep source (UWorld, AMBOSS, NBME, Kaplan, forums, or any other). Publicly available official sample questions (for example, USMLE's free sample items) may be read only to understand structure, style, and difficulty; never copy, paraphrase, or adapt their content. If a draft turns out to resemble a published question, rewrite it from scratch.
8. **Never guess.** If a fact cannot be verified, drop the question or list it under "Open issues" in the delivery message. Cite only what can be verified; omit page numbers rather than invent them.
9. **Safety-sensitive content** (self-harm, overdoses) is written clinically and always includes the appropriate safety step in the explanation (observation, psychiatric evaluation).

---

## 3. Difficulty rubric

| Stars | Label | What makes it this hard | Block 1 examples |
|---|---|---|---|
| ★★★ | Board standard | One key finding leads to a standard next step. Distractors are plausible but clearly inferior. | RV infarct after nitroglycerin (fluids); neonatal bilious emesis (UGI series) |
| ★★★★ | Above standard | A single detail (a threshold, contraindication, sequence, or age cutoff) flips the usual answer. The most tempting distractor is the "usual" answer. | Ectopic + breastfeeding (surgery, not MTX); DKA with K⁺ 2.9 (hold insulin) |
| ★★★★★ | Top tier | Multistep reasoning across a changing clinical course; the tempting answer is actively harmful; requires integrating pathophysiology and a guideline limit. | Beer potomania overcorrection (relower with DDAVP + D5W) |

**Block mix target:** about 25% ★★★, 50% ★★★★, 25% ★★★★★.

---

## 4. Vignette blueprint

**Order:** age/sex/setting → chief complaint with timeline → pertinent positives and negatives → past history, medications, social history → vitals in one sentence ("Temperature is …, blood pressure is …, pulse is …, respirations are …, and pulse oximetry shows …") → exam → labs as a 2-column table → imaging/ECG described in words → optional interval change ("Eight minutes later…") → question stem.

- **Length:** 150–280 words before the stem.
- **Clues:** the decisive clue is present but not highlighted; include 1–2 realistic red herrings.
- **Approved stems:** "Which of the following is the most appropriate next step in management?" · "…most likely diagnosis?" · "…most appropriate initial/most accurate test?" · "In addition to [X], which of the following is the most appropriate next step?"
- **Style:** generic drug names, NBME-style phrasing, no eponyms without description, temperature in °C with °F.

---

## 5. Answer option rules

- Five options, A–E, all from the same category (all management steps, or all tests, or all diagnoses).
- Order alphabetically or logically, as NBME does. Similar length and specificity.
- No "all of the above" or "none of the above."
- Every distractor represents a named error type, recorded in `distractor_error_types`:
  - wrong sequence (right action, wrong order)
  - right drug, wrong time
  - contraindicated in this patient
  - correct for a different variant or age group
  - too aggressive / too passive
  - therapy for a different problem
- **Answer-key balance:** across a block, no letter above 30%, and never the same letter 3 times in a row.

---

## 6. Explanation template (one page per question)

1. **Correct answer line:** "✓ Correct answer: X. [option text]"
2. **Right/wrong prompt:** "Picked X? Nice work. Read on to lock in the reasoning. Picked something else? Find your letter under 'Why the other choices are wrong.'"
3. **Why X is correct:** 2–4 short paragraphs: key clue and diagnosis → mechanism → guideline-backed action. Show calculations.
4. **Why the other choices are wrong:** one entry per distractor, 1–2 sentences, stating when that option *would* be correct.
5. **Educational objective:** 1–2 testable sentences.
6. **Sources:** author, title, journal, year.

Writing style: short, direct sentences; define abbreviations on first use; plain words over jargon.

---

## 7. Coverage plan

Rotate across Step 2 CK systems (per the USMLE content outline; verify the current list at usmle.org): immune; blood/lymphoreticular; behavioral health; nervous system and special senses; skin; musculoskeletal; cardiovascular; respiratory; gastrointestinal; renal/urinary; pregnancy, childbirth, and puerperium; female reproductive and breast; male reproductive; endocrine; multisystem; biostatistics/epidemiology; social sciences (ethics, legal, patient safety).

Also rotate disciplines: internal medicine, surgery, pediatrics, OB/GYN, psychiatry, neurology, emergency medicine, family medicine.

**Covered so far (Blocks 1–3):** cardiology, OB/GYN (ectopic; preeclampsia/magnesium toxicity), endocrine, GI/peds surgery, toxicology (acetaminophen; lithium), hematology, ID/neuro, renal, psychiatry/nutrition, surgery (volvulus), respiratory, musculoskeletal (peds), skin, male reproductive, ethics/legal, biostatistics, preventive screening (lung cancer), geriatrics (postoperative delirium, Beers), breast (palpable mass), neurology (acute stroke/thrombolysis), rheumatology/ophthalmology (giant cell arteritis), trauma (ATLS hemorrhagic shock), pharmacology adverse effects (drug interaction).

**Not yet covered after Block 3:** preventive screening beyond lung (USPSTF: breast, colon, AAA, cervical), geriatrics beyond delirium (falls, incontinence), neurology beyond stroke (seizure, headache), ophthalmology proper (angle-closure glaucoma, retinal detachment), ENT, allergy/immunology (anaphylaxis, hereditary angioedema), nephrology beyond electrolytes (glomerular disease, AKI), obstetrics beyond preeclampsia (labor, postpartum hemorrhage), pediatrics beyond MSK (vaccines, development), patient safety/quality, pulmonology beyond effusion (asthma/COPD exacerbation), oncology emergencies. Prioritize these in Block 4.

Check §9 before writing; do not repeat a topic unless deliberately testing a different decision point.

---

## 8. Output formats

### 8a. PDF (current)

- **File name:** `Board_Prep_BlockN.pdf`, US Letter.
- **Cover:** title, how to use, difficulty legend, scorecard (Q#, stars, "Your answer," "Correct?", total). Q# cells link to each question.
- **Per question:** question page → explanation on the next page. Tappable links: "Check answer →" and "Next question →." Stars and label (Board standard / Above standard / Top tier) on the question page; system and topic shown only on the explanation page (so they do not give the answer away).
- **Final page:** answer key (linked to explanations), "Reading your score," accuracy note, disclaimer.
- **Tech notes:** ReportLab; DejaVu Sans (needed for ★ ✓ ✗ µ β glyphs; base fonts render them as boxes); navy header `#2F4A6D`, link blue `#3E6FB0`, correct green `#2E7D4F`, wrong red `#A93226`, stars amber `#E0A100`, off-stars `#CBD2DB`. Keep each question and each explanation to one page; if text overflows, tighten wording before shrinking type (minimum 9 pt).
- **Verify before delivering:** expected page count = 1 + 2 × N + 1; render pages to images and inspect; confirm link count.

### 8b. App (future)

**Modes**
- *Tutor:* select an answer → Submit → immediate correct/incorrect banner, the explanation, and the user's choice highlighted.
- *Timed:* block of up to 40 questions at about 90 seconds each; review after the block.

**Features:** flag/mark questions; performance by system, difficulty, and distractor error type; resurfacing of missed objectives (spaced repetition); score history; filter by system/difficulty.

**Data:** question bank as a JSON array (schema below); user progress stored separately (`{question_id, chosen, correct, seconds, flagged, timestamp}`).

**Current app (Rounds, 2026-10-10):** web app on GitHub Pages (https://jjones1319-create.github.io/rounds/); `index.html` is built from `src/` + `questions/` by `build.py`, and 3D anatomy models load as separate files. Practice (tutor/timed blocks, strike-outs, flags, notes, lab values, key points, stats) plus an Anatomy section: body model with front/back rotation and layers (skeleton, organs, muscles, arteries, veins, nerves, lymphatics, dermatomes), brain model (lateral view with functional areas and MCA/ACA/PCA territories; underside with cranial nerves), heart model (outside with coronaries; inside with valves and conduction system), an A–Z index of ~250 entries that highlights the entry on its model, and quizzes (cranial nerves, "name that structure"). To add a block: regenerate questions per this spec, append to the question JSON, rebuild, and republish to the same link so progress carries over (questions are keyed by ID).

**Question schema (example = B1-Q01):**

```json
{
  "id": "B1-Q01",
  "system": "Cardiology",
  "discipline": "Emergency Medicine",
  "topic": "Right ventricular infarction with nitrate-induced hypotension",
  "difficulty": 3,
  "vignette": [
    "A 63-year-old man is brought to the emergency department 50 minutes after the onset of crushing substernal chest pressure that began while he was shoveling snow. He has hypertension, type 2 diabetes mellitus, and hyperlipidemia and smokes 1 pack of cigarettes daily. Medications are lisinopril, metformin, and atorvastatin. Paramedics gave him 325 mg of chewable aspirin en route.",
    "On arrival, temperature is 36.9 C (98.4 F), blood pressure is 122/78 mm Hg, pulse is 74/min, respirations are 18/min, and pulse oximetry shows 96% on room air. He is diaphoretic. The lungs are clear to auscultation. Heart sounds are regular with no murmurs. ECG shows 3-mm ST-segment elevations in leads II, III, and aVF, with greater elevation in lead III than in lead II; 1-mm ST-segment elevation in lead V1; and reciprocal ST-segment depressions in leads I and aVL. The cardiac catheterization laboratory is activated, and sublingual nitroglycerin is given for ongoing chest pain.",
    "Eight minutes later, the patient says he feels lightheaded. Blood pressure is 78/48 mm Hg and pulse is 88/min. Jugular venous pressure is 12 cm H2O. The lungs remain clear, and the extremities are cool."
  ],
  "labs": [],
  "after_labs": [],
  "stem": "Which of the following is the most appropriate next step in management?",
  "options": {
    "A": "Dobutamine infusion",
    "B": "Intra-aortic balloon pump placement",
    "C": "Intravenous furosemide",
    "D": "Intravenous metoprolol",
    "E": "Intravenous normal saline bolus"
  },
  "answer": "E",
  "why_correct": [
    "This patient has an inferior STEMI (ST elevation in II, III, and aVF), usually caused by occlusion of the right coronary artery. Two ECG clues point to right ventricular (RV) involvement: ST elevation greater in lead III than in lead II, and ST elevation in V1. RV infarction accompanies roughly 30%–50% of inferior MIs.",
    "An infarcted RV cannot generate much pressure, so it depends on high filling pressure (preload) to push blood through the lungs to the left ventricle. Nitroglycerin is a venodilator; it drops preload, and left ventricular filling and cardiac output collapse. The result is the classic triad of RV infarction: **hypotension, elevated jugular venous pressure, and clear lungs**.",
    "The fix is to restore preload: stop nitrates and give an IV isotonic crystalloid bolus while the patient goes for emergent PCI, which is the definitive therapy. Right-sided precordial leads (ST elevation ≥1 mm in V4R) confirm the diagnosis."
  ],
  "why_wrong": {
    "A": "Dobutamine is the inotrope of choice for RV infarction, but only when hypotension persists after adequate volume loading. Fluids come first.",
    "B": "An IABP lowers left ventricular afterload and augments coronary diastolic perfusion; it does not fix an RV preload problem. The IABP-SHOCK II trial also showed no mortality benefit from routine IABP use in MI complicated by cardiogenic shock.",
    "C": "Furosemide reduces preload further and would worsen the hypotension. The lungs are clear, so there is no pulmonary edema to treat.",
    "D": "Beta-blockers are contraindicated in patients with hypotension, signs of a low-output state, or increased risk of cardiogenic shock. IV metoprolol here could precipitate shock."
  },
  "distractor_error_types": {
    "A": "right drug, wrong time (inotrope before volume)",
    "B": "therapy for a different problem (LV support; no proven benefit)",
    "C": "contraindicated (worsens preload)",
    "D": "contraindicated (hypotension / shock risk)"
  },
  "objective": "In inferior STEMI, hypotension after nitrates with elevated JVP and clear lungs means RV infarction. Treat with IV fluids and urgent reperfusion, and avoid preload-reducing drugs (nitrates, diuretics, morphine).",
  "sources": [
    "O'Gara PT, et al. 2013 ACCF/AHA Guideline for the Management of ST-Elevation Myocardial Infarction. Circulation. 2013;127:e362–e425 (RV infarction section).",
    "Rao SV, et al. 2025 ACC/AHA/ACEP/NAEMSP/SCAI Guideline for the Management of Patients With Acute Coronary Syndromes. Circulation. 2025.",
    "Thiele H, et al. Intraaortic balloon support for myocardial infarction with cardiogenic shock (IABP-SHOCK II). N Engl J Med. 2012;367:1287–1296."
  ],
  "verified_on": "2026-10-04",
  "status": "active"
}
```

---

## 9. Question log (prevents repeats)

| ID | Topic | System | Ans | Diff | Key source | Verified |
|---|---|---|---|---|---|---|
| B1-Q01 | Right ventricular infarction with nitrate-induced hypotension | Cardiology | E | ★★★ | ACCF/AHA STEMI 2013; ACC/AHA ACS 2025 | 2026-10-04 |
| B1-Q02 | Tubal ectopic pregnancy with a contraindication to methotrexate (breastfeeding) | Reproductive (Obstetrics/Gynecology) | C | ★★★★ | ACOG Practice Bulletin 193 (2018) | 2026-10-04 |
| B1-Q03 | Diabetic ketoacidosis with hypokalemia: replete potassium before insulin | Endocrine | D | ★★★★ | ADA/EASD/JBDS/AACE/DTS consensus (2024) | 2026-10-04 |
| B1-Q04 | Neonatal bilious emesis: rule out malrotation with midgut volvulus | Gastrointestinal | E | ★★★ | ACR Appropriateness Criteria: Vomiting in Infants | 2026-10-04 |
| B1-Q05 | Acetaminophen overdose with unknown ingestion time | Toxicology / Psychiatry | C | ★★★★ | US/Canada APAP consensus, JAMA Netw Open (2023) | 2026-10-04 |
| B1-Q06 | Heparin-induced thrombocytopenia with thrombosis | Hematology | B | ★★★★ | ASH HIT guideline (2018) | 2026-10-04 |
| B1-Q07 | Bacterial meningitis needing CT before LP: treat before imaging; add ampicillin after age 50 | Nervous System / Infectious Disease | A | ★★★★ | IDSA bacterial meningitis guideline (2004) | 2026-10-04 |
| B1-Q08 | Hyponatremia overcorrection in a patient at high risk for osmotic demyelination | Renal / Electrolytes | D | ★★★★★ | Hyponatremia expert panel, Am J Med (2013); EJE (2014) | 2026-10-04 |

| B2-Q01 | Refeeding syndrome during treatment of anorexia nervosa | Behavioral health / Nutrition | B | ★★★★ | ASPEN consensus, Nutr Clin Pract (2020) | 2026-10-05 |
| B2-Q02 | Sigmoid volvulus after endoscopic detorsion: resect same admission | GI / Surgery | D | ★★★★★ | ASCRS colonic volvulus guideline, DCR (2021) | 2026-10-05 |
| B2-Q03 | Complicated parapneumonic effusion: tube thoracostomy | Respiratory | E | ★★★★ | ACCP guideline, Chest (2000); BTS pleural guideline (2023) | 2026-10-05 |
| B2-Q04 | Septic arthritis of the hip in a child (Kocher criteria) | Musculoskeletal | A | ★★★★ | Kocher, JBJS (1999); Caird, JBJS (2006) | 2026-10-05 |
| B2-Q05 | Suspected melanoma: narrow excisional biopsy first | Skin | A | ★★★★ | AAD melanoma guideline, JAAD (2019) | 2026-10-05 |
| B2-Q06 | Solid testicular mass: radical inguinal orchiectomy | Male reproductive | B | ★★★ | AUA testicular cancer guideline (2019, amended 2023) | 2026-10-05 |
| B2-Q07 | Confidential STI care for a minor | Ethics and law | E | ★★★ | CDC STI guidelines, MMWR (2021); Guttmacher; SAHM/AAP (2016) | 2026-10-05 |
| B2-Q08 | Number needed to treat from absolute risk reduction | Biostatistics | C | ★★★ | Laupacis, NEJM (1988) | 2026-10-05 |

| B3-Q01 | Lung cancer screening eligibility: 22 pack-years, quit 13 years ago | Preventive medicine | B | ★★★ | USPSTF lung cancer screening, JAMA (2021); NLST, NEJM (2011) | 2026-10-10 |
| B3-Q02 | Postoperative delirium precipitated by diphenhydramine: stop the drug, nonpharmacologic care | Geriatrics | E | ★★★★ | AGS postoperative delirium guideline, JAGS (2015); AGS Beers Criteria (2023) | 2026-10-10 |
| B3-Q03 | Palpable breast mass in a woman under 30: ultrasonography first | Female reproductive and breast | B | ★★★ | ACR Appropriateness Criteria, JACR (2023); ACOG PB 164 (2016) | 2026-10-10 |
| B3-Q04 | Acute ischemic stroke with BP above 185/110: lower it, then thrombolyse | Nervous system | A | ★★★★ | AHA/ASA acute ischemic stroke guideline, Stroke (2026); 2019 update (agents/doses) | 2026-10-10 |
| B3-Q05 | Magnesium toxicity in preeclampsia with renal impairment: stop infusion, calcium gluconate | Pregnancy | A | ★★★★★ | ACOG Practice Bulletin 222 (2020) | 2026-10-10 |
| B3-Q06 | Giant cell arteritis with amaurosis fugax: IV pulse glucocorticoids before biopsy | Immune / Rheumatology | C | ★★★★ | ACR/VF GCA guideline, Arthritis Care Res (2021); Smetana & Shmerling, JAMA (2002) | 2026-10-10 |
| B3-Q07 | Blunt trauma, transient responder with positive FAST: laparotomy with blood products | Multisystem / Trauma | D | ★★★★★ | ATLS 10th ed. (2018); EAST blunt abdominal trauma PMG (2002); PROPPR, JAMA (2015) | 2026-10-10 |
| B3-Q08 | Chronic lithium toxicity after an ACE inhibitor: EXTRIP dialysis criteria | Pharmacology / Toxicology | D | ★★★★ | EXTRIP lithium recommendations, CJASN (2015); FDA lithium label (2018) | 2026-10-10 |

Block 1 answer distribution: A 1, B 1, C 2, D 2, E 2. Block 2: A 2, B 2, C 1, D 1, E 2. Block 3: A 2, B 2, C 1, D 2, E 1.

---

## 10. Pre-delivery self-audit (all must be "yes")

- [ ] Every correct answer traced to a cited, current source re-checked by web search this session
- [ ] Exactly one defensible answer per question; loopholes closed in the stem
- [ ] Vignette math checked (gaps, corrections, scores) and shown in the explanation
- [ ] Each distractor has an error type and a "when it would be right" note
- [ ] Original wording; no near-duplicates of commercial or public practice questions
- [ ] Difficulty stars match the §3 rubric; block mix close to target
- [ ] Answer-key letters balanced (§5)
- [ ] No topic repeated from §9 without a new decision point
- [ ] PDF: page count correct, renders cleanly, all links work, no missing glyphs
- [ ] §9 log and §11 changelog updated in the returned spec

---

## 11. Changelog

| Version | Date | Change |
|---|---|---|
| 1.0 | 2026-10-04 | Spec created. Block 1 delivered (8 questions: cardiology, OB/GYN, endocrine, peds/surgery, toxicology/psych, hematology, ID/neuro, renal). |
| 1.1 | 2026-10-05 | Block 2 delivered inside the Rounds web app (8 questions: psych/nutrition, surgery, respiratory, MSK, skin, male reproductive, ethics, biostatistics). App gained front/back body views, a dermatome layer, brain and heart models, an A–Z index, and identification quizzes. All verified sources listed in §9. |
| 1.2 | 2026-10-10 | Block 3 delivered in the app (8 questions: preventive screening, geriatrics, breast, neurology, obstetrics, rheumatology, trauma, pharmacology/toxicology). Verification notes: the AHA/ASA published a 2026 acute ischemic stroke guideline (January 2026) that replaces the 2019 update; ATLS 11th edition launched in 2025 (its shock chapter was not readable online, so B3-Q07 cites the 10th edition and the EAST guideline, whose positive-FAST rule is unchanged). Questions now carry `distractor_error_types` and `verified_on` in `questions/questions3.py`. App now serves real 3D anatomy (body, brain, heart) from GitHub Pages. §7 gap list refreshed for Block 4. |
| 1.3 | 2026-10-10 | §2 rule 7 tightened per the owner: never take questions from any website or prep source; official sample questions may be read only for structure, style, and difficulty, never copied, paraphrased, or adapted. |

---

## 12. Open items to confirm with the user

- Which exam and test date (adjust §1 and the block mix).
- Her weak areas from QBank performance reports (weight §7 toward them).
- Preferred block size for the PDF (current: 8) and whether to add a timed answer-sheet page.
