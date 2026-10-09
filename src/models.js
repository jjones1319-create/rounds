/* Extra content for anatomy v2: new body structures, dermatomes, brain and heart models. */
LAYERS.push({ k: "derm", n: "Dermatomes", c: "#8FD19E" });
// 3D layers of the Brain and Heart tabs (keys match data/mesh_map.json scenes; the Body tab uses LAYERS).
const SCENE3D = {
  brain: [{ k: "cortex", n: "Cortex", c: "#E7C1B5" }, { k: "deep", n: "Brainstem and deep", c: "#C9A79A" }, { k: "artery", n: "Arteries", c: "#D2352E" },
          { k: "nerve", n: "Cranial nerves", c: "#E0AE18" }, { k: "skull", n: "Skull", c: "#D9C9A3" }],
  heart: [{ k: "wall", n: "Heart wall", c: "#A33B32" }, { k: "valves", n: "Valves", c: "#EAD7C3" }, { k: "coronary", n: "Coronary arteries", c: "#D2352E" },
          { k: "veins", n: "Cardiac veins", c: "#3B66C4" }, { k: "vessels", n: "Great vessels", c: "#B8463F" }],
};

Object.assign(INFO, {
  occipital: { n: "Occipital bone", L: "bone", d: "Forms the back and base of the skull; contains the foramen magnum (spinal cord) and the hypoglossal canals (CN XII).", p: "The occipital condyles articulate with C1. A fall onto the occiput can cause a contrecoup injury to the frontal lobes." },
  calcaneus: { n: "Calcaneus", L: "bone", d: "The heel bone, the largest tarsal, where the Achilles tendon inserts.", p: "The most fractured tarsal bone; after a fall from height, image the lumbar spine as well (associated compression fractures)." },
  erector_spinae: { n: "Erector spinae", L: "muscle", d: "Deep paraspinal columns (iliocostalis, longissimus, spinalis) that extend the spine. Innervated by dorsal rami.", p: "Most acute low back pain is muscular; red flags (fever, cancer, weight loss, neurologic deficit, retention) are what change management." },
  infraspinatus: { n: "Infraspinatus (with teres minor)", L: "muscle", d: "Rotator cuff muscle below the scapular spine that externally rotates the arm. Suprascapular nerve (teres minor: axillary nerve).", p: "Rotator cuff: SITS (supraspinatus abducts, infraspinatus and teres minor externally rotate, subscapularis internally rotates). Supraspinatus is the most commonly torn." },
  latissimus: { n: "Latissimus dorsi", L: "muscle", d: "Broad back muscle that extends, adducts, and internally rotates the arm. Thoracodorsal nerve.", p: "Used as a flap in breast reconstruction; the thoracodorsal nerve is at risk during axillary dissection." },
  triceps: { n: "Triceps brachii", L: "muscle", d: "The only muscle of the posterior arm; extends the elbow. Radial nerve.", p: "The triceps reflex tests C7. Radial nerve injury above the spiral groove weakens the triceps; below it, the triceps is spared." },
  forearm_extensors: { n: "Forearm extensor group", L: "muscle", d: "Wrist and finger extensors arising from the lateral epicondyle. Radial nerve (posterior interosseous branch).", p: "Lateral epicondylitis ('tennis elbow') is tendinosis at the common extensor origin." },
  gluteus_medius: { n: "Gluteus medius (with minimus)", L: "muscle", d: "Abducts the hip and steadies the pelvis during gait. Superior gluteal nerve.", p: "Weakness causes a Trendelenburg sign: the pelvis drops on the opposite side when standing on the affected leg." },
  gluteus_maximus: { n: "Gluteus maximus", L: "muscle", d: "Powerful hip extensor used for climbing stairs and rising from a chair. Inferior gluteal nerve.", p: "Give intramuscular injections in the upper outer quadrant (or ventrogluteal site) to avoid the sciatic nerve." },
  biceps_femoris: { n: "Biceps femoris (lateral hamstring)", L: "muscle", d: "Flexes the knee and extends the hip; its tendon forms the lateral border of the popliteal fossa. Tibial nerve (long head) and common fibular nerve (short head).", p: "Hamstring strains are common in sprinters; an avulsion from the ischial tuberosity can occur in adolescents." },
  semitendinosus: { n: "Semitendinosus and semimembranosus (medial hamstrings)", L: "muscle", d: "Flex the knee and extend the hip; form the medial border of the popliteal fossa. Tibial nerve.", p: "The semitendinosus tendon is part of the pes anserinus and is harvested for ACL reconstruction." },
  soleus: { n: "Soleus", L: "muscle", d: "Flat muscle under the gastrocnemius that plantarflexes the foot; a major venous pump. Tibial nerve.", p: "The soleal venous sinuses are a common starting point for deep vein thrombosis in immobile patients." },
  achilles: { n: "Achilles (calcaneal) tendon", L: "muscle", d: "Common tendon of gastrocnemius and soleus inserting on the calcaneus; the thickest tendon in the body.", p: "Rupture: a pop while pushing off, then a positive Thompson test. Fluoroquinolones and corticosteroids raise the risk." },
  profunda_brachii: { n: "Deep brachial artery (profunda brachii)", L: "artery", d: "Branch of the brachial artery that spirals around the back of the humerus with the radial nerve.", p: "Injured together with the radial nerve in midshaft humerus fractures." },
  gluteal_a: { n: "Superior and inferior gluteal arteries", L: "artery", d: "Branches of the internal iliac artery that leave the pelvis through the greater sciatic foramen to supply the gluteal muscles.", p: "A source of life-threatening bleeding in pelvic fractures; treated with angiographic embolization." },
  superior_gluteal_n: { n: "Superior gluteal nerve", L: "nerve", d: "L4–S1; exits above the piriformis to supply gluteus medius, gluteus minimus, and tensor fasciae latae.", p: "Injury (hip surgery, badly placed injection) causes a Trendelenburg gait: the pelvis sags toward the unaffected side." },
  inferior_gluteal_n: { n: "Inferior gluteal nerve", L: "nerve", d: "L5–S2; exits below the piriformis to supply gluteus maximus.", p: "Injury makes it hard to rise from a chair or climb stairs, with a lurching gait." },
  sural_n: { n: "Sural nerve", L: "nerve", d: "Sensory nerve formed from tibial and common fibular branches; runs down the back of the calf with the small saphenous vein to the lateral foot.", p: "The usual site for a diagnostic nerve biopsy (vasculitis, amyloidosis), leaving only lateral foot numbness." },
  /* dermatomes */
  d_C2: { n: "C2 dermatome", L: "derm", d: "Back of the head (occiput) and the upper neck.", p: "Occipital neuralgia follows the greater occipital nerve (C2). There is no C1 dermatome." },
  d_C3: { n: "C3 dermatome", L: "derm", d: "The neck, like a high collar.", p: "C3–C5 supply the phrenic nerve, so diaphragm irritation refers pain to the neck and shoulder." },
  d_C4: { n: "C4 dermatome", L: "derm", d: "The shoulders and upper chest, like a cape or the collar of a shirt.", p: "Shoulder-tip pain from diaphragmatic irritation (Kehr sign) is referred through C3–C5." },
  d_C5: { n: "C5 dermatome", L: "derm", d: "Lateral upper arm over the deltoid (the 'regimental badge' area).", p: "Biceps reflex: C5–C6. Erb palsy (C5–C6) causes the 'waiter's tip' posture." },
  d_C6: { n: "C6 dermatome", L: "derm", d: "Lateral forearm and the thumb.", p: "Brachioradialis reflex: C5–C6. A C5–C6 disc herniation compresses the C6 root: thumb numbness and weak biceps." },
  d_C7: { n: "C7 dermatome", L: "derm", d: "The middle finger.", p: "Triceps reflex: C7. The most common cervical radiculopathy is C7 (from the C6–C7 disc): middle-finger numbness, weak triceps and wrist flexors." },
  d_C8: { n: "C8 dermatome", L: "derm", d: "Little finger and the medial hand and forearm.", p: "C8 radiculopathy weakens finger flexors and intrinsic hand muscles; with T1 it forms Klumpke palsy." },
  d_T1: { n: "T1 dermatome", L: "derm", d: "Medial arm and forearm, near the axilla.", p: "Pancoast tumors invade the lower brachial plexus (C8–T1): medial arm pain, hand weakness, and Horner syndrome." },
  d_T2: { n: "T2 dermatome", L: "derm", d: "The axilla and upper chest, just below the clavicle.", p: "Thoracic dermatomes wrap the trunk in bands; herpes zoster follows a single band and stops at the midline." },
  d_T3: { n: "T3 dermatome", L: "derm", d: "Upper chest band between T2 and the nipple line.", p: "Cardiac pain is referred to T1–T4 dermatomes: chest, inner arm, and sometimes the jaw." },
  d_T4: { n: "T4 dermatome", L: "derm", d: "The band at the nipple line ('T4 at the teat pore').", p: "A sensory level at the nipples points to a spinal cord lesion at T4." },
  d_T5: { n: "T5 dermatome", L: "derm", d: "Band between the nipple line and the xiphoid.", p: "Chest wall shingles here is easily mistaken for cardiac or gallbladder pain before the rash appears." },
  d_T6: { n: "T6 dermatome", L: "derm", d: "The band at the xiphoid process.", p: "Gallbladder and gastric pain are referred to T5–T9 (epigastrium)." },
  d_T7: { n: "T7 dermatome", L: "derm", d: "Upper abdomen below the xiphoid.", p: "Rectus abdominis is supplied by T7–T12; segmental weakness can cause bulging of the abdominal wall." },
  d_T8: { n: "T8 dermatome", L: "derm", d: "Upper abdomen, midway between xiphoid and umbilicus.", p: "The IVC passes the diaphragm at T8." },
  d_T9: { n: "T9 dermatome", L: "derm", d: "Band just above the umbilicus.", p: "Beevor sign: the umbilicus moves up on sitting up when the T10–T12 segments are weak (lesion around T10)." },
  d_T10: { n: "T10 dermatome", L: "derm", d: "The band at the umbilicus ('T10 belly butTEN').", p: "Early appendicitis pain is periumbilical because the appendix's visceral afferents enter at T10." },
  d_T11: { n: "T11 dermatome", L: "derm", d: "Lower abdomen, below the umbilicus.", p: "Kidney and ureteral pain refer to T10–L1, which is why renal colic radiates to the flank and groin." },
  d_T12: { n: "T12 dermatome", L: "derm", d: "Lower abdomen just above the inguinal ligament.", p: "The iliohypogastric nerve (T12–L1) supplies the suprapubic skin and can be injured in appendectomy incisions." },
  d_L1: { n: "L1 dermatome", L: "derm", d: "The inguinal ligament and groin ('L1 is IL, the inguinal ligament').", p: "Ilioinguinal nerve (L1) injury during hernia repair numbs the upper medial thigh and genitals." },
  d_L2: { n: "L2 dermatome", L: "derm", d: "Anterior and medial upper thigh.", p: "Meralgia paresthetica (lateral femoral cutaneous nerve, L2–L3) causes burning numbness of the lateral thigh without weakness." },
  d_L3: { n: "L3 dermatome", L: "derm", d: "Anterior thigh down to the medial knee.", p: "Patellar reflex: L2–L4 (mainly L4). L3 radiculopathy weakens the quadriceps and hip flexion." },
  d_L4: { n: "L4 dermatome", L: "derm", d: "Medial leg and medial malleolus, down to the big-toe side of the foot.", p: "Patellar reflex: L4. An L3–L4 disc herniation compresses L4: knee extension weakness and a reduced patellar reflex." },
  d_L5: { n: "L5 dermatome", L: "derm", d: "Lateral leg, dorsum of the foot, and the big toe.", p: "The most common lumbar radiculopathy: an L4–L5 disc herniation hits L5. Weak dorsiflexion and great-toe extension, but no reflex loss." },
  d_S1: { n: "S1 dermatome", L: "derm", d: "Lateral foot, little toe, heel, and the back of the leg and thigh.", p: "Ankle reflex: S1. An L5–S1 disc herniation compresses S1: weak plantarflexion and a lost ankle reflex." },
  d_S2: { n: "S2 dermatome", L: "derm", d: "A strip down the middle of the back of the thigh.", p: "S2–S4 carry parasympathetic fibers to the bladder, rectum, and genitals ('S2, 3, 4 keeps it off the floor')." },
  d_S345: { n: "S3–S5 dermatomes (saddle area)", L: "derm", d: "The perineum, perianal skin, and inner buttocks: the area that touches a saddle.", p: "Saddle anesthesia with urinary retention and loss of anal tone is cauda equina syndrome: emergent MRI and surgical decompression." },
});

/* ---------- Brain model ---------- */
const BRAIN = {
  views: ["lateral", "underside"],
  lobes: [
    { id: "frontal", n: "Frontal lobe", pts: [[42,152],[58,104],[104,66],[176,52],[186,100],[196,150],[150,152],[100,158],[64,160],[46,170]], c: "#E8C4C0",
      d: "Everything in front of the central sulcus: motor cortex, Broca area, frontal eye fields, and the prefrontal cortex.", p: "Frontal lobe damage changes personality and judgment (disinhibition, apathy) and brings back primitive reflexes (grasp, snout). Classic example: Phineas Gage." },
    { id: "parietal", n: "Parietal lobe", pts: [[176,52],[244,56],[290,80],[292,110],[266,140],[232,146],[196,150],[186,100]], c: "#C7D7F0",
      d: "Behind the central sulcus: somatosensory cortex and association areas for spatial attention, calculation, and language.", p: "Nondominant (usually right) parietal lesions cause hemineglect and construction apraxia; dominant lesions cause Gerstmann syndrome." },
    { id: "temporal", n: "Temporal lobe", pts: [[64,160],[100,158],[150,152],[196,150],[232,146],[244,174],[220,200],[180,206],[130,210],[90,200],[70,192]], c: "#CFE5C8",
      d: "Below the lateral (Sylvian) fissure: primary auditory cortex, Wernicke area, hippocampus, and amygdala.", p: "The most common site of focal seizures (déjà vu, epigastric aura, automatisms). Herpes encephalitis targets the temporal lobes. Bilateral amygdala damage causes Klüver–Bucy syndrome." },
    { id: "occipital", n: "Occipital lobe", pts: [[290,80],[298,86],[322,130],[318,170],[294,196],[262,200],[244,174],[232,146],[266,140],[292,110]], c: "#F2DDB0",
      d: "The visual lobe at the back of the brain, supplied by the posterior cerebral artery.", p: "Bilateral occipital infarcts cause cortical blindness, sometimes with denial of blindness (Anton syndrome)." },
    { id: "cerebellum", n: "Cerebellum", ellipse: [284, 228, 44, 30], c: "#DDD3EA",
      d: "Coordinates movement and balance; the vermis controls the trunk, the hemispheres control the limbs.", p: "Cerebellar signs are ipsilateral: dysmetria, intention tremor, dysdiadochokinesia, and ataxic gait. Vermis lesions (alcohol) cause truncal ataxia." },
    { id: "brainstem", n: "Brainstem", pts: [[186,208],[214,208],[214,250],[208,292],[192,292],[186,250]], c: "#E6E0D2",
      d: "Midbrain, pons, and medulla: cranial nerve nuclei, the reticular activating system, and the long motor and sensory tracts.", p: "Brainstem strokes give 'crossed' signs: ipsilateral cranial nerve deficits with contralateral body weakness." },
  ],
  areas: [
    { id: "motor", n: "Primary motor cortex (precentral gyrus)", pts: [[160,56],[176,52],[186,100],[196,150],[184,152],[172,100]], c: "#D7473B",
      d: "Voluntary movement of the opposite side of the body, mapped as the homunculus: face and arm on the lateral surface (MCA), leg on the medial surface (ACA).", p: "A stroke that weakens the face and arm more than the leg is MCA territory; leg more than arm is ACA territory." },
    { id: "sensory", n: "Primary somatosensory cortex (postcentral gyrus)", pts: [[176,52],[192,54],[204,100],[212,146],[196,150],[186,100]], c: "#2C7FB8",
      d: "Touch, pain, temperature, and position sense from the opposite side of the body, with the same homunculus layout.", p: "Lesions cause contralateral loss of fine sensation and astereognosis (cannot identify objects by touch)." },
    { id: "broca", n: "Broca area", ellipse: [118, 132, 22, 14], c: "#F2B36B",
      d: "Posterior inferior frontal gyrus of the dominant hemisphere: speech production.", p: "Broca (expressive) aphasia: nonfluent, effortful speech with intact comprehension; the patient is aware and frustrated. Often with right arm and face weakness." },
    { id: "wernicke", n: "Wernicke area", ellipse: [214, 166, 24, 11], c: "#8E5CC4",
      d: "Posterior superior temporal gyrus of the dominant hemisphere: language comprehension.", p: "Wernicke (receptive) aphasia: fluent but meaningless speech with neologisms and poor comprehension; the patient is unaware. Caused by inferior MCA division strokes." },
    { id: "arcuate", n: "Arcuate fasciculus", line: [[140,140],[170,124],[205,150]], c: "#B07AD6", w: 3,
      d: "White-matter tract connecting Wernicke and Broca areas.", p: "Conduction aphasia: fluent speech and good comprehension but poor repetition." },
    { id: "auditory", n: "Primary auditory cortex", ellipse: [168, 160, 15, 7], c: "#3A9D6E",
      d: "Heschl gyrus in the superior temporal lobe; receives sound from both ears.", p: "Because hearing is bilaterally represented, a single cortical lesion does not cause deafness." },
    { id: "visual", n: "Primary visual cortex", pts: [[310,110],[322,130],[318,170],[300,186],[292,150]], c: "#E0AE18",
      d: "Occipital pole around the calcarine sulcus; the macula is represented at the pole.", p: "PCA stroke: contralateral homonymous hemianopia with macular sparing (the pole has collateral MCA supply)." },
    { id: "prefrontal", n: "Prefrontal cortex", ellipse: [76, 110, 26, 24], c: "#E58BAE",
      d: "Executive function, planning, judgment, and social behavior.", p: "Damage causes disinhibition, poor judgment, and apathy with preserved intelligence; frontal release signs may appear." },
    { id: "fef", n: "Frontal eye field", ellipse: [140, 78, 16, 10], c: "#6FA8DC",
      d: "Drives voluntary conjugate gaze to the opposite side.", p: "A frontal eye field lesion makes the eyes look toward the lesion; a pontine gaze center lesion makes them look away from it." },
    { id: "angular", n: "Angular and supramarginal gyri", ellipse: [252, 122, 20, 12], c: "#C98A66",
      d: "Inferior parietal lobule of the dominant hemisphere: reading, writing, calculation, and body schema.", p: "Gerstmann syndrome (dominant angular gyrus): agraphia, acalculia, finger agnosia, and left-right confusion." },
  ],
  territories: [
    { id: "mca", n: "Middle cerebral artery territory", pts: [[64,160],[96,84],[160,62],[230,66],[280,100],[270,146],[246,174],[220,200],[180,206],[130,210],[90,200],[70,192]], c: "rgba(44,127,184,.45)",
      d: "Most of the lateral hemisphere, including the face and arm motor and sensory areas, Broca and Wernicke areas, and the optic radiations. Lenticulostriate branches supply the internal capsule and basal ganglia.", p: "MCA stroke: contralateral face and arm weakness and numbness, aphasia (dominant side) or neglect (nondominant), and gaze toward the lesion. Lenticulostriate lacunar infarcts cause pure motor hemiparesis." },
    { id: "aca", n: "Anterior cerebral artery territory", pts: [[58,104],[104,66],[176,52],[244,56],[280,76],[230,66],[160,62],[96,84]], c: "rgba(58,157,110,.5)",
      d: "The medial surface of the frontal and parietal lobes, including the leg area of the motor and sensory homunculus.", p: "ACA stroke: contralateral leg weakness and numbness, urinary incontinence, and abulia or personality change." },
    { id: "pca", n: "Posterior cerebral artery territory", pts: [[280,100],[298,86],[322,130],[318,170],[294,196],[262,200],[246,174],[270,146]], c: "rgba(224,174,24,.5)",
      d: "The occipital lobe, inferior temporal lobe, and (via deep branches) the thalamus.", p: "PCA stroke: contralateral homonymous hemianopia with macular sparing; alexia without agraphia (dominant); thalamic pain syndrome." },
  ],
};

/* ---------- Heart model ---------- */
const HEART = {
  views: ["outside", "inside"],
  outside: [
    { id: "svc", n: "Superior vena cava", pts: [[104,38],[126,38],[128,96],[104,98]], c: "#3262C8", d: "Returns blood from the head, neck, and arms to the right atrium.", p: "SVC syndrome: facial and arm swelling from obstruction, usually by lung cancer or lymphoma." },
    { id: "ivc_h", n: "Inferior vena cava", pts: [[96,158],[118,160],[120,206],[98,206]], c: "#3262C8", d: "Returns blood from below the diaphragm to the right atrium.", p: "Hepatic venous congestion from right heart failure causes a pulsatile, tender liver." },
    { id: "pa_right", n: "Right pulmonary artery", line: [[160,70],[130,76],[100,84]], w: 12, c: "#5A86E6", d: "Runs behind the ascending aorta and SVC to the right lung.", p: "A saddle embolus lodges where the pulmonary trunk divides." },
    { id: "aorta_h", n: "Aorta", line: [[160,114],[158,86],[166,62],[190,52],[218,60],[232,84],[236,120]], w: 20, c: "#D2352E", d: "Arises from the left ventricle behind the pulmonary trunk and arches over the left main bronchus to descend beside the spine.", p: "Dissection of the ascending aorta (Stanford A) can tear the aortic valve or occlude the right coronary artery." },
    { id: "arch_branches", n: "Arch branches", parts: [[[166,54],[164,28]], [[182,52],[183,26]], [[198,54],[202,28]]], w: 6, c: "#D2352E", d: "Brachiocephalic trunk, left common carotid, and left subclavian arteries.", p: "Takayasu arteritis and syphilitic aortitis affect the arch and its branches." },
    { id: "pulm_trunk", n: "Pulmonary trunk", line: [[150,128],[152,100],[160,80],[176,66]], w: 18, c: "#5A86E6", d: "Leaves the right ventricle in front of the aorta and divides into right and left pulmonary arteries.", p: "A loud P2 and a palpable pulmonary artery pulsation suggest pulmonary hypertension." },
    { id: "ra", n: "Right atrium", pts: [[100,100],[132,100],[142,120],[140,160],[118,170],[96,150],[92,122]], c: "#C9707A", d: "Receives systemic venous blood from the SVC, IVC, and coronary sinus; contains the SA node.", p: "Right atrial enlargement produces tall, peaked P waves (P pulmonale)." },
    { id: "la_app", n: "Left atrial appendage", pts: [[228,124],[246,118],[256,132],[246,146],[232,140]], c: "#C9707A", d: "A pouch off the left atrium; the body of the left atrium lies posteriorly, behind the great vessels.", p: "The appendage is where thrombi form in atrial fibrillation; it can be occluded with a device in patients who cannot take anticoagulants." },
    { id: "rv", n: "Right ventricle", pts: [[112,170],[140,160],[160,150],[196,160],[212,190],[200,228],[170,250],[140,248],[112,220]], c: "#B23E42", d: "The most anterior chamber, directly behind the sternum; pumps into the low-pressure pulmonary circuit.", p: "Most injured chamber in penetrating chest trauma. RV infarction (with inferior MI) is preload dependent: give fluids, avoid nitrates." },
    { id: "lv", n: "Left ventricle", pts: [[196,160],[222,150],[246,160],[252,190],[238,228],[214,250],[200,228],[212,190]], c: "#9A2F33", d: "Thick-walled chamber forming the apex and the left heart border; pumps into the aorta.", p: "The apex beat is normally at the 5th intercostal space in the midclavicular line; a displaced, sustained apex means LV enlargement." },
    { id: "rca", n: "Right coronary artery", line: [[150,118],[138,130],[134,160],[140,196],[158,226],[180,246]], w: 3.2, c: "#F2B36B", d: "Runs in the right atrioventricular groove; gives the posterior descending artery in right-dominant hearts (most people) and supplies the SA node in about 60% and the AV node in most.", p: "Inferior MI (II, III, aVF): RCA. Watch for bradycardia, AV block, and right ventricular infarction." },
    { id: "lad", n: "Left anterior descending artery", line: [[172,120],[182,140],[194,170],[204,206],[212,246]], w: 3.2, c: "#F2B36B", d: "Runs in the anterior interventricular groove supplying the anterior wall, the anterior two-thirds of the septum, and the apex.", p: "The most commonly occluded coronary artery. Anterior MI (V1–V4) carries the highest risk of heart failure and ventricular aneurysm." },
    { id: "lcx", n: "Left circumflex artery", line: [[172,120],[196,124],[222,140],[246,160]], w: 3, c: "#F2B36B", d: "Wraps around the left atrioventricular groove to supply the lateral and posterior left ventricle.", p: "Lateral MI (I, aVL, V5–V6). Circumflex occlusions are the most likely to be electrically silent on a standard ECG." },
  ],
  inside: [
    { id: "ra_i", n: "Right atrium", pts: [[80,80],[150,80],[150,152],[80,152]], c: "#E4A7AE", d: "Receives venous blood and passes it through the tricuspid valve.", p: "The crista terminalis and the fossa ovalis (remnant of the foramen ovale) are landmarks inside the right atrium." },
    { id: "la_i", n: "Left atrium", pts: [[160,80],[230,80],[230,152],[160,152]], c: "#E4A7AE", d: "Receives oxygenated blood from four pulmonary veins and fills the left ventricle through the mitral valve.", p: "The most posterior chamber: enlargement compresses the esophagus (dysphagia) and the left recurrent laryngeal nerve (hoarseness)." },
    { id: "rv_i", n: "Right ventricle", pts: [[80,162],[150,162],[150,244],[118,268],[80,244]], c: "#D98A8E", d: "Thin-walled, crescent-shaped pump for the pulmonary circuit, with coarse trabeculae and a moderator band.", p: "Right heart failure: jugular venous distension, hepatomegaly, and peripheral edema; most often caused by left heart failure." },
    { id: "lv_i", n: "Left ventricle", pts: [[160,162],[230,162],[230,244],[198,278],[160,244]], c: "#C85C62", d: "Thick-walled high-pressure pump; the wall is about three times thicker than the right ventricle's.", p: "Concentric hypertrophy comes from pressure overload (hypertension, aortic stenosis); eccentric hypertrophy from volume overload (regurgitation)." },
    { id: "ias", n: "Interatrial septum", pts: [[150,80],[160,80],[160,152],[150,152]], c: "#B8898C", d: "Wall between the atria; contains the fossa ovalis.", p: "A patent foramen ovale persists in about a quarter of adults and allows paradoxical embolism (venous clot causing stroke). Ostium secundum ASD gives a fixed split S2." },
    { id: "ivs", n: "Interventricular septum", pts: [[150,162],[160,162],[160,250],[150,250]], c: "#B8898C", d: "Muscular wall between the ventricles with a small membranous upper part; carries the bundle of His and bundle branches.", p: "VSD is the most common congenital heart defect (holosystolic murmur at the left lower sternal border). Post-MI septal rupture (days 3–7) causes a new murmur with shock." },
    { id: "tricuspid", n: "Tricuspid valve", parts: [[[96,152],[104,166],[112,152]], [[112,152],[120,166],[128,152]], [[128,152],[136,166],[144,152]]], c: "#F4E3B0", d: "Three leaflets between the right atrium and ventricle; opens in diastole.", p: "Best heard at the left lower sternal border. Tricuspid endocarditis is the classic lesion of intravenous drug use (S. aureus). Regurgitation gives large v waves in the JVP." },
    { id: "mitral", n: "Mitral valve", parts: [[[172,152],[182,168],[192,152]], [[196,152],[206,168],[216,152]]], c: "#F4E3B0", d: "Two leaflets (anterior and posterior) between the left atrium and ventricle, anchored by chordae tendineae to the papillary muscles.", p: "Best heard at the apex. Rheumatic disease causes mitral stenosis (opening snap, diastolic rumble); mitral valve prolapse gives a midsystolic click." },
    { id: "pulmonic", n: "Pulmonic valve", ellipse: [94, 164, 9, 5], c: "#F4E3B0", d: "Three semilunar cusps at the outflow of the right ventricle.", p: "Heard at the left upper sternal border. Pulmonic stenosis is the valve lesion of tetralogy of Fallot and congenital rubella." },
    { id: "aortic", n: "Aortic valve", ellipse: [206, 164, 9, 5], c: "#F4E3B0", d: "Three semilunar cusps at the outflow of the left ventricle; the coronary arteries arise just above it.", p: "Heard at the right upper sternal border, radiating to the carotids in stenosis. A bicuspid valve (1–2% of people) causes early stenosis and is linked to coarctation." },
    { id: "papillary", n: "Papillary muscles and chordae", parts: [[[172,200],[180,170]], [[214,200],[208,170]], [[100,196],[106,166]], [[134,196],[128,166]]], w: 2.4, c: "#8E3A3E", d: "Muscles that tighten the chordae tendineae to keep the atrioventricular valves from prolapsing during systole.", p: "The posteromedial papillary muscle has a single blood supply (from the posterior descending artery) and ruptures after inferior MI, causing sudden severe mitral regurgitation." },
    { id: "sa_node", n: "Sinoatrial node", ellipse: [96, 90, 7, 5], c: "#E0AE18", d: "The pacemaker, at the junction of the SVC and the right atrium; fires at 60–100 per minute.", p: "Supplied by the RCA in about 60% of people. Sick sinus syndrome causes bradycardia and pauses, often alternating with tachycardia." },
    { id: "av_node", n: "Atrioventricular node", ellipse: [148, 150, 6, 4.5], c: "#E0AE18", d: "Delays the impulse (the PR interval) before it enters the ventricles; the only normal electrical connection between atria and ventricles.", p: "Supplied by the RCA in most people, which is why inferior MI causes AV block. Adenosine and vagal maneuvers act here." },
    { id: "his", n: "Bundle of His and bundle branches", parts: [[[154,154],[155,196]], [[155,196],[140,228],[120,250]], [[155,196],[170,230],[196,256]]], w: 2.2, c: "#E0AE18", d: "Carries the impulse down the septum and splits into right and left bundle branches, then Purkinje fibers.", p: "A new left bundle branch block with chest pain is treated like a STEMI. Right bundle branch block is often benign." },
    { id: "purkinje", n: "Purkinje fibers", parts: [[[120,250],[100,236]], [[120,250],[108,262]], [[196,256],[216,236]], [[196,256],[208,268]]], w: 1.4, c: "#E0AE18", d: "Fast-conducting fibers under the endocardium that activate the ventricles from apex to base.", p: "Escape rhythms from the Purkinje system are slow (20–40 per minute) with wide QRS complexes." },
  ],
};

/* ---------- Dictionary assembly ---------- */
function buildDictionary() {
  const out = [];
  const seen = new Set();
  FIG.structures.forEach((o) => {
    if (o.noTap) return; const key = o.info || o.id; if (seen.has(key)) return; seen.add(key);
    const inf = INFO[key]; if (!inf) return;
    const lay = LAYERS.find((l) => l.k === inf.L);
    out.push({ id: key, name: inf.n, model: "body", sys: lay ? lay.n : "", sub: inf.L === "derm" ? "Dermatome" : lay.n, target: { kind: "body", key } });
  });
  CN.forEach((c) => out.push({ id: "cn_" + c.num, name: `Cranial nerve ${c.num} (${c.name})`, model: "brain", sys: "Cranial nerves", sub: "Cranial nerve", target: { kind: "cn", num: c.num } }));
  BRAIN.lobes.concat(BRAIN.areas, BRAIN.territories).forEach((a) => out.push({ id: "br_" + a.id, name: a.n, model: "brain", sys: "Brain", sub: BRAIN.territories.includes(a) ? "Arterial territory" : "Brain", target: { kind: "brain", id: a.id } }));
  HEART.outside.concat(HEART.inside).forEach((h) => out.push({ id: "ht_" + h.id, name: h.n, model: "heart", sys: "Heart", sub: "Heart", target: { kind: "heart", id: h.id, view: HEART.outside.includes(h) ? "outside" : "inside" } }));
  const sortKey = (s) => s.replace(/^(right|left) /i, "").toLowerCase();
  out.sort((a, b) => sortKey(a.name).localeCompare(sortKey(b.name)));
  return out;
}
