# Block 4 question data (pediatrics track, docs/PEDS_BLUEPRINT.md). Same markup conventions as questions.py.
# Written two at a time by /peds-pair and gated by an independent blind re-solve (/peds-blind); each question carries
# "status" ("draft" until it passes) and "reviewed_by". Verified against the sources listed per question on the date shown.
QUESTIONS4 = [
  {
    "id": "B4-Q01", "system": "Multisystem Processes &amp; Disorders", "discipline": "Pediatrics / Emergency Medicine",
    "topic": "Fever in a well-appearing 14-day-old: lumbar puncture, parenteral antibiotics, and admission regardless of normal urinalysis and markers", "difficulty": 3,
    "vignette": [
      "A 14-day-old boy is brought to the emergency department by his parents because of a rectal temperature of 38.3 C (100.9 F) measured at home 2 hours ago. He has been fussier than usual since the morning but breastfeeds every 2 to 3 hours and had six wet diapers yesterday. He has had no vomiting, cough, or rash. He was born at 39 weeks' gestation by uncomplicated vaginal delivery; his mother's group B streptococcal screen was negative, she had no fever during labor, and she has no history of genital herpes. He went home on the second day of life and received intramuscular vitamin K at birth. His 3-year-old sister has had a runny nose for 4 days.",
      "He weighs 3.8 kg (8 lb 6 oz); birth weight was 3.4 kg (7 lb 8 oz). Temperature is 38.4 C (101.1 F) rectally, pulse is 158/min, respirations are 44/min, and pulse oximetry shows 98% on room air. He is alert, cries vigorously during the examination, and is consoled when held. The anterior fontanelle is soft and flat, and there is mild clear rhinorrhea. The tympanic membranes, lungs, heart, abdomen, umbilicus, and skin are normal, with no vesicles. Capillary refill time is less than 2 seconds. A urine specimen is obtained by catheterization, and blood is drawn for culture. Laboratory results are shown.",
    ],
    "labs": [("Leukocytes", "10,200/&#181;L"), ("Absolute neutrophil count", "3,400/&#181;L"), ("Platelets", "312,000/&#181;L"), ("C-reactive protein", "0.6 mg/dL"), ("Urine leukocyte esterase", "Negative"), ("Urine nitrite", "Negative"), ("Urine leukocytes", "2/hpf")],
    "after_labs": [],
    "stem": "Which of the following is the most appropriate next step in management?",
    "options": {
      "A": "Discharge home with reassessment in 24 hours",
      "B": "Hospital observation without antibiotics",
      "C": "Intramuscular ceftriaxone and discharge home",
      "D": "Lumbar puncture and parenteral antibiotics",
      "E": "Serum procalcitonin measurement",
    },
    "answer": "D",
    "why_correct": [
      "Three facts decide this case: the infant is <b>14 days old</b>, the rectal temperature is 38.4 C (fever is 38.0 C or higher), and he looks well. The 2021 American Academy of Pediatrics (AAP) clinical practice guideline on well-appearing febrile infants 8 to 60 days old sorts infants into three age strata (8 to 21, 22 to 28, and 29 to 60 days) because the risk of invasive bacterial infection falls week by week: in the PECARN cohort, bacteremia was found in 5.3% of febrile infants in the second week of life and 3.3% in the third, against 1.6% in the fourth, and bacterial meningitis occurs in 0.5% to 1.3% of febrile infants 8 to 21 days old. No examination finding and no laboratory marker lowers that risk enough to skip any part of the evaluation at this age.",
      "For infants 8 to 21 days the key action statements (KAS) are all firm: obtain urine by catheterization or suprapubic aspiration for urinalysis, with culture if the urinalysis is positive (KAS 1; evidence grade A, strong recommendation); obtain a blood culture (KAS 2; A, strong); obtain cerebrospinal fluid for cell count, protein, glucose, Gram stain, and culture (KAS 4; A, strong); start parenteral antimicrobial therapy (KAS 5; A, strong); and monitor the infant in a hospital with staff experienced in the care of young infants (KAS 6; B, moderate). Inflammatory markers are optional at this age (KAS 3; B, weak): his normal absolute neutrophil count (3,400/&#181;L; the guideline's cutoff is 4,000/&#181;L when procalcitonin is also measured and 5,200/&#181;L when it is not) and C-reactive protein (0.6 mg/dL, that is 6 mg/L, against a cutoff of 20 mg/L) change none of these steps, though they may help later in deciding when to stop antibiotics. The <b>lumbar puncture comes before the antibiotics</b>: cerebrospinal fluid drawn after a dose is hard to interpret, and an infant with uncertain meningitis ends up with a prolonged course.",
      "The runny-nosed sister and the infant's mild rhinorrhea are a red herring. Upper respiratory symptoms do not take an infant out of the pathway, and infants younger than 28 days with a positive viral test still carry a 1.1% to 2.1% risk of invasive bacterial infection, which the guideline judges high enough to warrant the same testing and treatment. The history also matters for herpes simplex virus: there is no maternal genital herpes, and he has no vesicles, seizures, or hypothermia, so empiric acyclovir is not indicated unless the cerebrospinal fluid shows pleocytosis with a negative Gram stain or there is leukopenia, thrombocytopenia, or an elevated alanine aminotransferase.",
      "Empiric therapy at 8 to 21 days with no focus identified (guideline Table 3) is ampicillin 150 mg/kg per day intravenously divided every 8 hours plus either ceftazidime 150 mg/kg per day divided every 8 hours or gentamicin 4 mg/kg every 24 hours. For 3.8 kg: ampicillin 3.8 &#215; 50 = 190 mg every 8 hours, with ceftazidime 190 mg every 8 hours or gentamicin 3.8 &#215; 4 = 15 mg every 24 hours. Ampicillin covers <i>Listeria</i> and enterococci; <i>Escherichia coli</i> is now the most common cause of bacteremia and group B streptococcus the most common cause of meningitis in this age group. If all cultures are negative at 24 to 36 hours and he remains well, antibiotics are stopped and he goes home (KAS 7a; B, strong).",
    ],
    "why_wrong": {
      "A": "Home management belongs to the 29- to 60-day pathway: a well-appearing infant of that age with a negative urinalysis and normal inflammatory markers may be observed at home without antibiotics and reassessed in 24 hours (KAS 20d). At 14 days the guideline makes no such allowance, whatever the laboratory results show.",
      "B": "Observation in hospital without antibiotics is an option for a 29- to 60-day-old whose urinalysis is negative, whose markers are normal, and whose cerebrospinal fluid, if obtained, is normal (KAS 19d). At 8 to 21 days parenteral antibiotics are a strong recommendation (KAS 5); withholding them while cultures incubate leaves a roughly 1-in-20 chance of bacteremia untreated.",
      "C": "A dose of intramuscular ceftriaxone with discharge is the older outpatient strategy for infants 29 days and older, and the guideline still allows a parenteral antibiotic with observation at home for a 29- to 60-day-old whose markers are abnormal but whose cerebrospinal fluid is normal (Figure 3). A 14-day-old is admitted, the antibiotic follows the lumbar puncture, and ceftriaxone is not in the guideline's regimens for 8 to 21 days: it displaces bilirubin from albumin, must not be given to hyperbilirubinemic neonates, and is contraindicated in neonates 28 days or younger who need calcium-containing intravenous solutions.",
      "E": "Procalcitonin is the most accurate inflammatory marker, and at 22 to 60 days the markers should be assessed (KAS 10 and 17) because an abnormal value changes what follows: cerebrospinal fluid should be obtained at 22 to 28 days (KAS 11b) and may be at 29 to 60 days (KAS 18a), and parenteral antibiotics may be given (KAS 12b and 19b). At 8 to 21 days they are optional (KAS 3) because every infant is tested, treated, and admitted regardless; waiting for a procalcitonin result would only delay the lumbar puncture.",
    },
    "distractor_error_types": {
      "A": "correct for a different age group (29&#8211;60 days with negative urinalysis and normal markers)",
      "B": "too passive (parenteral antibiotics are a strong recommendation at 8&#8211;21 days)",
      "C": "wrong sequence and wrong setting (antibiotic before the lumbar puncture, discharge, and a drug not used at this age)",
      "E": "wrong sequence (an optional test that cannot change management at this age)",
    },
    "objective": "A well-appearing term infant 8 to 21 days old with a rectal temperature of 38.0 C or higher needs urinalysis by catheter, blood culture, and lumbar puncture, then parenteral antibiotics and hospital monitoring, whatever the urinalysis, inflammatory markers, or viral symptoms show. Marker-guided decisions and home management begin at 22 days.",
    "sources": [
      "Pantell RH, Roberts KB, Adams WG, et al; Subcommittee on Febrile Infants. Clinical Practice Guideline: Evaluation and Management of Well-Appearing Febrile Infants 8 to 60 Days Old. Pediatrics. 2021;148(2):e2021052228 (Key Action Statements 1&#8211;7, Figure 1, Table 3; revised version posted October 28, 2021, per the Statement of Correction, Pediatrics 2021;148(5):e2021054063).",
      "Mace SE, Gemme SR, Valente JH, et al. Clinical Policy for Well-Appearing Infants and Children Younger Than 2 Years of Age Presenting to the Emergency Department With Fever. Ann Emerg Med. 2016;67(5):625&#8211;639 (excludes neonates 28 days and younger).",
      "Ceftriaxone for injection: prescribing information (Contraindications; Precautions, Pediatric Use). Hospira; revised March 2022 (DailyMed set ID 128bb292-d174-4769-b3e6-9f16617f31e3).",
    ],
    "verified_on": "2026-10-17",
    "status": "reviewed",
    "reviewed_by": "independent blind re-solve",
  },
  {
    "id": "B4-Q02", "system": "Gastrointestinal System", "discipline": "Pediatrics / Emergency Medicine",
    "topic": "Suspected intussusception in an 8-month-old: ultrasonography before enema reduction", "difficulty": 3,
    "vignette": [
      "An 8-month-old girl is brought to the emergency department by her father because of episodes of crying that began 7 hours ago. Every 15 to 20 minutes she screams, pulls her knees to her chest, and cannot be comforted for several minutes; between episodes she lies quietly and is sleepy. She has vomited twice; the vomitus was formula without bile. She has had no fever or diarrhea. A runny nose and loose stools last week have resolved. She was born at term, takes formula and pureed foods, and her immunizations are up to date.",
      "She weighs 8.0 kg (17 lb 10 oz). Temperature is 37.6 C (99.7 F), pulse is 148/min, respirations are 36/min, and blood pressure is 92/58 mm Hg. She is drowsy but opens her eyes and cries when her abdomen is palpated. The anterior fontanelle is soft and flat. Mucous membranes are moist, the extremities are warm, and capillary refill time is 2 seconds. The abdomen is soft and not distended, with an ill-defined, tubular, mildly tender mass in the right upper quadrant; the right lower quadrant feels empty. There is no guarding or rebound tenderness. The diaper contains a small amount of loose stool mixed with mucus that tests positive for occult blood. There are no inguinal hernias.",
    ],
    "labs": [], "after_labs": [],
    "stem": "Which of the following is the most appropriate next step in management?",
    "options": {
      "A": "Abdominal radiography",
      "B": "Abdominal ultrasonography",
      "C": "Air-contrast enema",
      "D": "CT of the abdomen and pelvis with intravenous contrast",
      "E": "Lumbar puncture",
    },
    "answer": "B",
    "why_correct": [
      "Put the findings together. Paroxysms of colicky pain every 15 to 20 minutes in which the infant draws up her legs, quiet or sleepy intervals between them, nonbilious vomiting, a tubular mass in the right upper quadrant with an empty right lower quadrant, and stool with mucus and occult blood describe <b>ileocolic intussusception</b>, in which the terminal ileum telescopes through the ileocecal valve into the colon. It is a disease of infants and toddlers (most cases occur between 3 and 36 months, and about 83% before age 3), usually with no lead point at this age and often after a viral illness. The classic combination of pain, vomiting, bloody stool, and a palpable mass is present in only about 20% of children, and lethargy or irritability is common in the youngest patients.",
      "The diagnosis is confirmed before it is treated, and the test is <b>abdominal ultrasonography</b>. The American College of Radiology (ACR) Appropriateness Criteria for abdominal pain in a child (new 2025, published 2026) rate ultrasonography 'usually appropriate' as the initial imaging for suspected intussusception, radiography 'may be appropriate', and contrast enema, CT, and MRI 'usually not appropriate'. Ultrasonography has a sensitivity of about 98% and a specificity of 98% to 100%, needs no radiation or sedation, and shows a concentric, target-like mass in cross-section with a kidney-like appearance along its length; it also looks for a pathologic lead point, fluid trapped between the bowel layers, and absent blood flow on Doppler, findings that predict a difficult reduction. The ACR&#8211;SPR practice parameter for pediatric contrast enemas (revised 2026) states that sonography is important in establishing the diagnosis before a reduction procedure is begun.",
      "Once ultrasonography confirms the intussusception, this child is a candidate for nonoperative reduction: she is warm and well perfused with a normal blood pressure, and her abdomen is soft without guarding, so none of the contraindications (free intraperitoneal air, peritonitis, shock) is present. Reduction is done by air or liquid enema under fluoroscopy, or by saline enema under ultrasonography, with a surgeon notified and available, intravenous access, and fluids first if she is dehydrated; the parameter advises reduction within 8 to 12 hours of the ultrasound diagnosis, a target air pressure of 120 mm Hg, and up to three attempts of up to 5 minutes each. Air enema succeeds in about 80% of cases with perforation in fewer than 1%, and a partly reduced intussusception can be tried again after a delay. The American Pediatric Surgical Association's 2021 systematic review supports observing a stable child for about 4 hours after reduction and then discharging from the emergency department, and finds no benefit from prophylactic antibiotics before reduction (the ACR&#8211;SPR parameter leaves them to the clinical service). Surgery, preferably laparoscopic, is for failed reduction, perforation, peritonitis, shock, or a lead point.",
    ],
    "why_wrong": {
      "A": "Plain radiographs are insensitive (roughly 40% to 60% in published series) and cannot confirm the diagnosis, so the ACR rates them 'may be appropriate'. Their role is to look for free air or a high-grade obstruction when perforation is a concern before an enema; once ultrasonography has made the diagnosis, radiographs add radiation without changing management. They would come first in an infant with a rigid, distended abdomen.",
      "C": "The air enema is the treatment, not the test. As initial imaging it is 'usually not appropriate': it exposes the child to fluoroscopy and a small risk of perforation, requires a surgeon on standby, and is unnecessary in the many infants whose colicky crying has another cause. It is the right next step after ultrasonography shows the intussusception in a stable child without peritonitis or free air.",
      "D": "CT is 'usually not appropriate' for suspected intussusception in a child: it delivers radiation, often needs sedation, delays treatment, and answers nothing that ultrasonography does not. Its uses in a child's abdomen lie elsewhere, for example after major blunt trauma.",
      "E": "Lethargy in an infant rightly raises the question of meningitis or sepsis, but here it is episodic and explained: she is afebrile, rouses and cries when examined, has a flat fontanelle, and has an abdominal mass with occult blood in the stool. A lumbar puncture would be right for a febrile, irritable infant with a bulging fontanelle, or for lethargy with no abdominal explanation; here it would delay the diagnosis while the trapped bowel becomes more ischemic.",
    },
    "distractor_error_types": {
      "A": "wrong sequence (insensitive screening study before the definitive test)",
      "C": "wrong sequence (treatment before the diagnosis is confirmed)",
      "D": "therapy for a different problem (inappropriate test with radiation)",
      "E": "therapy for a different problem (neurologic workup for an abdominal cause)",
    },
    "objective": "Episodic colicky pain with drawing up of the legs, lethargy between episodes, vomiting, and a right-sided abdominal mass or blood in the stool in an infant is intussusception until proven otherwise. Confirm it with abdominal ultrasonography first; reduce it by air or liquid enema only after confirmation, and only if there is no peritonitis, free air, or shock.",
    "sources": [
      "Expert Panel on Pediatric Imaging; Nguyen HN, Chan SS, Brown BP, et al. ACR Appropriateness Criteria&#174; Abdominal Pain-Child. J Am Coll Radiol. 2026;23(4):700&#8211;714 (Variant 2: suspected intussusception, initial imaging).",
      "American College of Radiology, Society for Pediatric Radiology. ACR&#8211;SPR Practice Parameter for the Performance of Pediatric Fluoroscopic Contrast Enema Examinations. Revised 2026 (Resolution 25), section IV.B (intussusception).",
      "Kelley-Quon LI, Arthur LG, Williams RF, et al. Management of intussusception in children: a systematic review (American Pediatric Surgical Association Outcomes and Evidence-Based Practice Committee). J Pediatr Surg. 2021;56(3):587&#8211;596.",
      "Hwang J, Yoon HM, Kim PH, et al. Current diagnosis and image-guided reduction for intussusception in children. Clin Exp Pediatr. 2023;66(1):12&#8211;21.",
    ],
    "verified_on": "2026-10-17",
    "status": "reviewed",
    "reviewed_by": "independent blind re-solve",
  },
]
