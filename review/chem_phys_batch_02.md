# Review packet (key): block CP2

Plan: docs/CHEM_PHYS_250.md batch 2 (CP-026 to CP-050, passages CP-P05 to CP-P08); checks in review/chem_phys_batch_02_check.py

25 questions, 4 passages. Answers: 026D 027A 028C 029C 030D 031C 032A 033D 034B 035A 036B 037D 038C 039A 040D 041C 042B 043D 044B 045B 046A 047D 048B 049C 050A

Answer letters: A 6, B 6, C 6, D 7

## How this batch is reviewed

An independent blind re-solve (MCAT_SPEC §7): a fresh session answers every item from the blind packet; its answers and objections are compared with this key. Agreement with no objection passes the item (reviewed_by: independent blind re-solve); anything else is checked against the sources, fixed and re-solved. The batch is committed and pushed only after every item passes.

## Passage CP-P05: Conduction in myelinated and demyelinated axons

Electrically, an axon is a long, leaky cable: the axoplasm is a resistor, the membrane a capacitor in parallel with its ion channels. In a hypothetical study, investigators recorded from single motor axons dissected from rat sciatic nerve at 37 °C. Every axon rested at −70 mV and fired an action potential when depolarized to a threshold of about −55 mV. In the myelinated axons the voltage-gated Na⁺ channels were confined to the nodes of Ranvier, bare gaps about 1 µm long spaced 1.0 mm apart; between nodes, each internode was wrapped in a sheath so that the axoplasm was separated from the extracellular fluid by a stack of n membrane bilayers in series (n = 1 for a bare axon; n = 100 in the intact fibres, the axon's own membrane plus the wraps of the sheath).

The investigators modelled each internode as the axial resistance of its axoplasm, R = ρL/A, where ρ = 1.0 Ω·m, L = 1.0 mm is the internode length and A is the cross-sectional area of the axon, in series with the capacitance C of the internodal membrane together with its sheath. A single bilayer has a capacitance of 1.0 × 10⁻² F per square metre of surface (1 µF/cm²), and a stack of n bilayers has 1/n of that, so C = (1.0 × 10⁻² F/m²)(πdL)/n for an axon of diameter d. Current entering at an active node must charge the next internode before the following node reaches threshold; the time this takes scales with τ = RC, and in the model the conduction velocity is approximately L/τ. Table 1 lists the model values and the measured conduction velocity for four fibres: two intact fibres of different diameter, a 10 µm fibre after a treatment that had thinned its sheath to 20 bilayers along every internode, and a 10 µm fibre whose internodes had been stripped bare.

In the bare fibre the action potential at the last intact node failed to bring the next node to threshold and conduction stopped; the exposed internodal membrane contained almost no voltage-gated Na⁺ channels. In a second part of the study, rats were given the demyelinating agent systemically and their sciatic nerve conduction velocity, recorded with surface electrodes, was 40% lower than in a group given the vehicle alone; the axons of the treated nerves had not been examined under the microscope.

**Table 1. The four fibres: 1 and 2 intact, 3 with a thinned sheath, 4 bare; axon diameter d = 10 µm for fibres 1, 3 and 4 and 5 µm for fibre 2. n = number of bilayers, C = model capacitance per 1.0 mm internode, τ = RC (model), v = measured conduction velocity.**

| Fibre | n | C (pF) | τ (µs) | v (m/s) |
|---|---|---|---|---|
| 1 | 100 | 3.14 | 40 | 24 |
| 2 | 100 | 1.57 | 80 | 12 |
| 3 | 20 | 15.7 | 200 | 4.8 |
| 4 | 1 | 314 | 4,000 | failed |

*Alt text:* Table with four rows. Fibre 1 (intact, axon diameter 10 micrometres): 100 bilayers, capacitance per internode 3.14 picofarads, time constant 40 microseconds, measured velocity 24 metres per second. Fibre 2 (intact, 5 micrometres): 100 bilayers, 1.57 picofarads, 80 microseconds, 12 metres per second. Fibre 3 (thinned sheath, 10 micrometres): 20 bilayers, 15.7 picofarads, 200 microseconds, 4.8 metres per second. Fibre 4 (bare, 10 micrometres): 1 bilayer, 314 picofarads, 4,000 microseconds, conduction failed.

*Source:* Hypothetical experiment written for this app. Resting potential −70 mV, threshold −55 mV, Na⁺ entry at threshold, nodes of Ranvier and saltatory conduction from OpenStax Anatomy and Physiology 2e, 12.4 The Action Potential (2022). The cable model follows Tasaki and Matsumoto, On the Cable Theory of Nerve Conduction, Bulletin of Mathematical Biology 64:1069–1082 (2002): in the internode the potential spreads as ∂V/∂t = (1/(c_m r_i)) ∂²V/∂x², the time for a point to reach a given potential is proportional to x² c_m r_i, and the internodal conduction time is set by this spread; their measured frog motor fibre values (myelin capacitance 1.6 × 10⁻¹¹ F/cm, axoplasm resistance 1.45 × 10⁸ Ω/cm, 20–25 m/s) are of the same order as the model values here. Myelin lowers the capacitance and raises the resistance of the internodal membrane (Stony Brook Cellular Neurophysiology, 4.6 Conduction of Action Potentials along Axons; OpenStax College Physics 2e, 20.7 Nerve Conduction). Bare-membrane capacitance 1 µF/cm² is the standard value; axoplasm resistivity is quoted between about 70 Ω·cm (Tarotin, Aristovich and Holder, Simulation of impedance changes with a FEM model of a myelinated nerve fibre, arXiv:1903.04948, 2019, 150 lamellae, 65 m/s) and 110 Ω·cm (MIT OpenCourseWare 6.021J, 2004, problem set 8, 150 lamellae), so the passage states the value it uses (1.0 Ω·m = 100 Ω·cm). Sheaths of up to about 100 layers: Frontiers in Chemistry 10:1041961 (2022). Conduction block when a demyelinated internode lacks Na⁺ channels: Waxman and Brill, J Neurol Neurosurg Psychiatry 41:408–416 (1978); a simulation study in Restorative Neurology and Neuroscience, vol. 3 (1991). Table values generated in review/chem_phys_batch_02_check.py; the measured velocities are set 4% below L/τ.

*Status:* reviewed

### CP-026  ·  ★★★  ·  Skill 1 Knowledge

The axons rested at −70 mV and fired at −55 mV. When the voltage-gated Na⁺ channels open at threshold, the ion movement that follows is best described as:

- **A.** Na⁺ entering the axon, driven by its concentration gradient but opposed by the membrane potential
- **B.** Na⁺ leaving the axon, driven down its concentration gradient toward the extracellular fluid
- **C.** Na⁺ entering the axon, carried by the Na⁺/K⁺ pump against its concentration gradient
- **D.** Na⁺ entering the axon, driven by both its concentration gradient and the inside-negative potential

**Answer: D**

*Worked solution*

- Na⁺ is about ten times more concentrated outside the axon than inside, so its concentration gradient points inward.
- At threshold the inside of the axon is still negative (−55 mV), so the electrical force on a positive ion also points inward. Both parts of the electrochemical gradient drive Na⁺ in through the open channels, and the rapid inward current produces the rising phase of the action potential.
- Shortcut: at rest and at threshold both forces on Na⁺ point into the cell. Once the inside turns positive the electrical force opposes entry, and net entry stops only at the Na⁺ equilibrium potential, about +60 mV.

*Why the other choices are wrong*

- **A.** The membrane potential is inside-negative at threshold, so it attracts the cation inward; the electrical force opposes Na⁺ entry only once the inside has become positive, late in the rising phase. *(sign or unit error: the direction of the electrical force on a cation at a negative membrane potential)*
- **B.** Na⁺ is more concentrated outside the axon, so the concentration gradient drives it in, not out; it is K⁺ that leaves during repolarization. *(reversed relationship: direction of the Na⁺ concentration gradient)*
- **C.** Flux through an open channel is passive. The Na⁺/K⁺ pump uses ATP to move Na⁺ out of the cell (and K⁺ in), restoring the gradients between action potentials. *(reversed relationship: the pump moves Na⁺ out, and channel flux is passive)*

*Tags:* chem_phys · biology · FC4 4C · topics: 4C.nerve-cell

*Takeaway:* At threshold, voltage-gated Na⁺ channels open and Na⁺ flows in, pushed by both its concentration gradient and the inside-negative membrane potential.

*Sources*

- OpenStax Anatomy and Physiology 2e, 12.4 The Action Potential (2022): resting potential −70 mV, threshold about −55 mV; at threshold voltage-gated Na⁺ channels open and Na⁺ rushes in, driven by a tenfold concentration gradient and by electrical attraction; K⁺ leaves later to repolarize.
- OpenStax Biology 2e, 35.2 How Neurons Communicate (2018): the Na⁺/K⁺ pump moves three Na⁺ out and two K⁺ in using ATP.

*Status:* reviewed · rev 1

---

### CP-027  ·  ★★★★  ·  Skill 2 Reasoning

In Table 1, an internode of fibre 1 has one hundredth of the capacitance of the bare internode of fibre 4, although the two axons have the same diameter and internode length. The reduction arises because the 100 stacked bilayers:

- **A.** behave as 100 capacitors in series, equivalent to one capacitor whose plate separation is 100 times that of a single bilayer
- **B.** behave as 100 capacitors in parallel, so that each bilayer holds one hundredth of the charge a single bilayer would hold
- **C.** lower the dielectric constant of the material between axoplasm and extracellular fluid to one hundredth of its value
- **D.** reduce the area of membrane in contact with the axoplasm to one hundredth of that of the bare axon

**Answer: A**

*Worked solution*

- Each bilayer is a thin insulating layer between two conducting fluids, so a stack of n bilayers is n capacitors in series: 1/C = 1/C₁ + 1/C₂ + … = n/C₁, giving C = C₁/n. With n = 100, C falls to one hundredth.
- The same result follows from the parallel-plate formula C = κε₀A/d: stacking 100 bilayers of the same material multiplies the separation d between the conducting fluids by 100 while the area and κ stay the same, so C falls by 100. Check: 314 pF/100 = 3.14 pF, the Table 1 value for fibre 1.
- Consequence: for the same change in voltage the node's inward current has to deliver one hundredth of the charge (Q = CV) to the internode, which is why charging it, and conducting, is faster.

*Why the other choices are wrong*

- **B.** Capacitors in parallel add (C_p = C₁ + C₂ + …), which would make the sheath's capacitance 100 times larger, not smaller. *(reversed relationship: parallel and series combination of capacitors)*
- **C.** The dielectric constant is a property of the lipid, roughly the same for every bilayer; stacking layers changes the thickness of the insulator, not its κ. *(wrong formula: κ attributed to the number of layers)*
- **D.** The membrane area facing the axoplasm is πdL whether or not a sheath is present; the outer wraps if anything have a larger area. Capacitance falls because the separation between the conducting fluids grows. *(wrong formula: A instead of d changed by the sheath)*

*Tags:* chem_phys · physics · FC4 4C · topics: 4C.capacitance

*Takeaway:* Stacked membranes are capacitors in series: C ∝ A/d, so a sheath of n bilayers has 1/n of a single membrane's capacitance and needs 1/n of the charge to change its voltage.

*Sources*

- OpenStax College Physics 2e, 19.5 Capacitors and Dielectrics (2022): C = κε₀A/d for a parallel-plate capacitor.
- OpenStax College Physics 2e, 19.6 Capacitors in Series and Parallel (2022): 1/C_s = 1/C₁ + 1/C₂ + …; series capacitors are equivalent to one capacitor with a larger plate separation.
- Stony Brook University, Cellular Neurophysiology, 4.6 Conduction of Action Potentials along Axons: myelination reduces the capacitance and increases the resistance of the internodal membrane.

*Status:* reviewed · rev 1

---

### CP-028  ·  ★★★  ·  Skill 2 Reasoning

In the model, the axial resistance R of one 1.0 mm internode of fibre 1 (axon diameter 10 µm) is closest to:

- **A.** 1.3 MΩ
- **B.** 3.2 MΩ
- **C.** 13 MΩ
- **D.** 51 MΩ

**Answer: C**

*Worked solution*

- R = ρL/A with ρ = 1.0 Ω·m, L = 1.0 × 10⁻³ m and A = πr², where r = 5.0 × 10⁻⁶ m: A = π × 25 × 10⁻¹² m² ≈ 7.9 × 10⁻¹¹ m².
- R = (1.0 × 1.0 × 10⁻³)/(7.9 × 10⁻¹¹) ≈ 1.3 × 10⁷ Ω = 13 MΩ.
- Check against Table 1: τ = RC = 1.3 × 10⁷ Ω × 3.14 × 10⁻¹² F ≈ 4.0 × 10⁻⁵ s = 40 µs, the listed value. Shortcut: 10⁻³/(8 × 10⁻¹¹) = 1.25 × 10⁷.

*Why the other choices are wrong*

- **A.** 1.3 MΩ is ten times too small, the result of writing 1 mm as 10⁻⁴ m or 25 µm² as 2.5 × 10⁻¹⁰ m²; keep the powers of ten with the units. *(sign or unit error: a power of ten lost in the length or the area)*
- **B.** 3.2 MΩ comes from using the diameter in place of the radius, A = π(10 µm)² = 3.1 × 10⁻¹⁰ m², four times the true area. *(wrong formula: diameter used as the radius)*
- **D.** 51 MΩ is the resistance of the 5 µm fibre (fibre 2), whose radius is 2.5 µm: halving the diameter quarters the area and quadruples R. *(misread graph: the 5 µm fibre's diameter used)*

*Tags:* chem_phys · physics · FC4 4C · topics: 4C.resistance

*Takeaway:* Axial resistance R = ρL/A ∝ 1/d²: halving an axon's diameter quadruples the resistance of each unit length.

*Sources*

- OpenStax College Physics 2e, 20.3 Resistance and Resistivity (2022): R = ρL/A.
- Tasaki and Matsumoto, On the Cable Theory of Nerve Conduction, Bulletin of Mathematical Biology 64:1069–1082 (2002): measured axis-cylinder resistance of a frog motor fibre 1.45 × 10⁸ Ω/cm, that is about 15 MΩ per millimetre, the same order as the model value.

*Status:* reviewed · rev 1

---

### CP-029  ·  ★★★★  ·  Skill 4 Data and statistics

Suppose fibre 3 remyelinated until its sheath contained 40 bilayers along every internode, with no other change. Based on the model and on the relationship between τ and measured velocity in Table 1, its conduction velocity would be closest to:

- **A.** 2.4 m/s
- **B.** 4.8 m/s
- **C.** 10 m/s
- **D.** 19 m/s

**Answer: C**

*Worked solution*

- Read the table: across fibres 1–3 the product v × τ is constant (24 × 40 = 960, 12 × 80 = 960, 4.8 × 200 = 960 µm), so the measured velocity is inversely proportional to τ, as the model's v ≈ L/τ predicts (the measured values are 4% below 1.0 mm/τ).
- C ∝ 1/n, so doubling the bilayers from 20 to 40 halves C from 15.7 pF to 7.85 pF; R is unchanged (same axon), so τ = RC halves from 200 µs to 100 µs.
- v ≈ 960 µm/100 µs = 9.6 m/s, or L/τ = 1.0 mm/100 µs = 10 m/s. Shortcut: halving τ doubles v: 4.8 → 9.6 m/s.

*Why the other choices are wrong*

- **A.** 2.4 m/s halves the velocity when τ halves; velocity varies inversely with τ, not with it. *(reversed relationship: velocity taken as proportional to τ)*
- **B.** 4.8 m/s assumes the velocity is fixed by the axon diameter alone; Table 1 shows fibres 1 and 3, with the same diameter, differing fivefold because of the sheath. *(misread graph: the bilayer column ignored, velocity taken to depend on diameter alone)*
- **D.** 19 m/s applies the factor 2 twice, as if velocity scaled with the square of the number of bilayers; C, and so τ and v, change in simple proportion to n. *(wrong formula: the bilayer ratio squared)*

*Tags:* chem_phys · physics · FC4 4C · topics: 4C.current-voltage, 4C.capacitance

*Takeaway:* In the cable model the time to charge the next internode is τ = RC, and conduction velocity is inversely proportional to it; a thinner sheath raises C and slows conduction in proportion.

*Sources*

- Tasaki and Matsumoto, On the Cable Theory of Nerve Conduction, Bulletin of Mathematical Biology 64:1069–1082 (2002): in the internode ∂V/∂t = (1/(c_m r_i)) ∂²V/∂x², the time for the potential to reach a given level is proportional to x² c_m r_i, and the internodal conduction time is set by this spread.
- OpenStax College Physics 2e, 21.6 DC Circuits Containing Resistors and Capacitors (2022): the time constant τ = RC of charging through a resistor.

*Status:* reviewed · rev 1

---

### CP-030  ·  ★★★★  ·  Skill 3 Research design

In the treated rats the sciatic nerve conduction velocity was 40% lower than in the vehicle group. Which additional step is most necessary before the slowing can be attributed to loss of myelin rather than to a change in the axons themselves?

- **A.** Comparing the treated group with a group of untreated rats of the same age that received no injections at all
- **B.** Recording the treated nerves again at a lower temperature to test whether the velocity falls still further
- **C.** Raising the stimulus strength until the amplitude of the treated nerves' response matches the vehicle group's
- **D.** Measuring axon diameters and sheath thickness in both groups and comparing velocities between fibres of equal axon diameter

**Answer: D**

*Worked solution*

- Table 1 shows two independent determinants of velocity: axon diameter (fibres 1 and 2, 10 µm and 5 µm) and sheath thickness (fibres 1 and 3). A 40% fall in a whole-nerve recording could come from thinner sheaths or from a loss or shrinkage of the large, fast axons, and the passage states that the treated axons were not examined.
- Measuring both variables in both groups, and comparing velocity between treated and vehicle fibres of the same axon diameter, holds diameter constant so that any remaining difference can be attributed to the sheath. This is the comparison the passage's model demands.
- Shortcut: to attribute an effect to one variable, measure the other candidate variable and hold it fixed.

*Why the other choices are wrong*

- **A.** An uninjected group would show whether the injection procedure itself matters; the vehicle group already serves that purpose. It says nothing about whether the slowing came from the sheath or from the axon. *(true but irrelevant: a control for the injection, not for the mechanism of slowing)*
- **B.** Cooling slows conduction in every fibre, myelinated or not, so a further fall would not distinguish the two explanations. *(out of scope: temperature affects all fibres alike)*
- **C.** A stronger stimulus recruits more fibres and changes the amplitude of the response, not the speed of the fastest fibres; it does not test what caused the slowing. *(true but irrelevant: amplitude, not velocity)*

*Tags:* chem_phys · biology · FC4 4C · topics: 4C.nerve-cell

*Takeaway:* Conduction velocity depends on both axon diameter and sheath thickness, so slowing is attributed to demyelination only after the axons are measured and velocities compared at matched diameter.

*Sources*

- OpenStax Anatomy and Physiology 2e, 12.4 The Action Potential (2022): both myelination and axon diameter influence conduction speed; wider axons conduct faster.
- OpenStax Biology 2e, 35.1 Neurons and Glial Cells (2018): myelin, produced by Schwann cells and oligodendrocytes, insulates the axon and speeds transmission; demyelination slows or blocks conduction.

*Status:* reviewed · rev 1

---

## Passage CP-P06: pH, pKa and the oral absorption of four drugs

Most drugs are weak acids or weak bases. A drug crosses the lipid bilayers of the gut epithelium chiefly as its un-ionized (neutral) form; the ionized form is hydrated and crosses far more slowly. The ratio of the two forms at a given pH follows from the Henderson–Hasselbalch equation: for a weak acid HA, log([A⁻]/[HA]) = pH − pKa, and for a weak base B, log([BH⁺]/[B]) = pKa − pH, where pKa is that of the conjugate acid BH⁺. Once the neutral form has crossed a membrane it re-equilibrates at the pH of the new compartment, which can hold the drug there as its ion (ion trapping).

In a hypothetical study, four candidate drugs (W, X, Y and Z; Table 1) were characterized. Each drug's octanol–water partition coefficient was measured by shaking a solution of the drug between n-octanol and an aqueous buffer held at a pH at which the drug was more than 99% un-ionized, and was reported as log P, the logarithm of the ratio of the drug's concentration in the octanol layer to that in the water layer. The investigators treated a log P between about 1 and 3 as favourable for passive diffusion across membranes; a compound with log P below 0 partitions poorly into the bilayer however small its ionized fraction. The percentage of each drug in its un-ionized form was calculated for gastric fluid (pH 2.0) and for the fluid of the upper small intestine (pH 6.0) (Figure 1). The absorptive surface of the small intestine is many times that of the stomach.

Drug W was then prepared as two tablets of equal dose (1.0 mmol): one containing the free acid and one its sodium salt. In a dissolution test in 900 mL of simulated gastric fluid at pH 2.0 and 37 °C, 85% of the dose had dissolved from the sodium-salt tablet after 10 minutes but only 15% from the free-acid tablet. In volunteers, the peak plasma concentration was reached at 0.5 h after the salt and at 2 h after the free acid, with the same total exposure to the drug. Once in solution at pH 2.0, the drug from either tablet is in the same equilibrium between the un-ionized acid and its anion.

**Table 1. The four drugs.**

| Drug | Type | pKa | log P |
|---|---|---|---|
| W | weak acid | 4.0 | 2.5 |
| X | weak acid | 7.0 | −1.0 |
| Y | weak base | 9.0 | 2.0 |
| Z | weak base | 5.0 | 2.0 |

*Alt text:* Table with four rows. Drug W: weak acid, pKa 4.0, log P 2.5. Drug X: weak acid, pKa 7.0, log P minus 1.0. Drug Y: weak base, pKa 9.0, log P 2.0. Drug Z: weak base, pKa 5.0, log P 2.0.

**Figure 1. Percentage of each drug in its un-ionized form in gastric fluid (pH 2.0) and in the upper small intestine (pH 6.0), calculated from Table 1.**

Chart (bar): x = Drug; y = Un-ionized (%).
- Gastric fluid, pH 2.0: (W, 99.0), (X, 100.0), (Y, 0.0), (Z, 0.1)
- Upper small intestine, pH 6.0: (W, 1.0), (X, 90.9), (Y, 0.1), (Z, 90.9)

*Alt text:* Grouped bar chart of percentage un-ionized for drugs W, X, Y and Z, two bars each. Gastric fluid, pH 2.0: W 99.0%, X 100.0%, Y 0.0%, Z 0.1%. Upper small intestine, pH 6.0: W 1.0%, X 90.9%, Y 0.1%, Z 90.9%.

*Source:* Hypothetical study written for this app. Henderson–Hasselbalch equation from OpenStax Chemistry 2e, 14.6 Buffers (2019). The pH-partition principle (un-ionized drug is lipid-soluble and crosses membranes; weak acids are un-ionized in acid; ion trapping) from Hogben, Schanker, Tocco and Brodie, Absorption of drugs from the stomach II. The human, J Pharmacol Exp Ther 120:540–545 (1957), as summarized with Goodman and Gilman in Deranged Physiology, Factors which determine the lipid solubility of drugs. Gastric pH 1.5–3.5 and the stomach's small absorptive role (aspirin and alcohol) from OpenStax Anatomy and Physiology 2e, 23.4 The Stomach (2022); proximal small-bowel luminal pH 5.5–7.0 from Nugent, Kumar, Rampton and Evans, Gut 48:571 (2001); the passage uses pH 2.0 and 6.0 as representative values so that pH − pKa is a whole number. log P as the partition coefficient of the neutral species and log D as its pH-dependent counterpart from ACD/Labs, LogP vs LogD application note. Charge, not size, keeps ions out of the bilayer: OpenStax Biology 2e, 5.2 Passive Transport (2018); ion–dipole hydration: OpenStax Chemistry 2e, 11.2 Electrolytes. Salts dissolve faster than the free acid or base because of their higher solubility and the pH in the diffusion layer at the dissolving surface: Serajuddin, Salt formation to improve drug solubility, Advanced Drug Delivery Reviews 59:603–616 (2007). Figure 1 values generated in review/chem_phys_batch_02_check.py.

*Status:* reviewed

### CP-031  ·  ★★★  ·  Skill 2 Reasoning

Drug W is filtered into the urine. In urine of pH 5.0, the fraction of W present as its anion is closest to:

- **A.** 9%
- **B.** 50%
- **C.** 91%
- **D.** 99%

**Answer: C**

*Worked solution*

- Passage: log([A⁻]/[HA]) = pH − pKa. For W, pKa = 4.0 (Table 1), so at pH 5.0 the ratio is 10¹ = 10: ten anions for every neutral molecule.
- Fraction ionized = 10/(10 + 1) = 10/11 ≈ 0.91, or 91%.
- Shortcut: one pH unit above the pKa, a weak acid is about 91% ionized; two units above, about 99%; at the pKa, 50%.

*Why the other choices are wrong*

- **A.** 9% is the fraction that remains un-ionized (1/11); the question asks for the anion. *(reversed relationship: un-ionized fraction reported instead of ionized)*
- **B.** 50% is the split only when the pH equals the pKa (4.0); the urine is one unit more basic than that. *(wrong formula: pH set equal to pKa)*
- **D.** 99% corresponds to a 100:1 ratio, two pH units above the pKa, the situation in the pH 6.0 intestinal fluid of Figure 1, not in urine of pH 5.0. *(misread graph: the pH 6.0 value from Figure 1 used)*

*Tags:* chem_phys · general chemistry · FC5 5A · topics: 5A.weak-acid-equilibria

*Takeaway:* For a weak acid, [A⁻]/[HA] = 10^(pH − pKa): one unit above the pKa the acid is 10/11 (91%) ionized.

*Sources*

- OpenStax Chemistry 2e, 14.6 Buffers (2019): the Henderson–Hasselbalch equation pH = pKa + log([A⁻]/[HA]).
- OpenStax Chemistry 2e, 14.3 Relative Strengths of Acids and Bases (2019): Ka, pKa and percent ionization of weak acids.

*Status:* reviewed · rev 1

---

### CP-032  ·  ★★  ·  Skill 1 Knowledge

The passage states that the ionized form of a drug crosses a lipid bilayer far more slowly than the un-ionized form. This is best explained by the fact that an ion in water:

- **A.** is held by ion–dipole attractions to a shell of water that the bilayer's nonpolar interior cannot replace
- **B.** is much larger than the neutral molecule and cannot fit between the hydrocarbon tails of the lipid bilayer
- **C.** is repelled by the net positive charge that the phospholipid head groups give to the membrane's surface
- **D.** can cross the membrane only when a transport protein specific for that ion is present in the bilayer

**Answer: A**

*Worked solution*

- A dissolved ion is hydrated: water's partial charges orient around it and bind to it by ion–dipole attractions, which release energy when the ion dissolves.
- Entering the hydrocarbon interior of a bilayer means giving up those attractions with nothing of comparable strength to replace them, since the interior offers only dispersion forces. The energy cost makes the ion's passage extremely slow; a neutral molecule loses much less in leaving water and crosses readily.
- Shortcut: the barrier is the charge, not the size; the un-ionized and ionized forms of a drug differ by one proton.

*Why the other choices are wrong*

- **B.** A drug anion and its neutral acid differ by a single proton and are almost the same size; size is not what distinguishes them. *(wrong formula: size invoked where charge is the barrier)*
- **C.** Phospholipid head groups are zwitterionic or anionic, not net positive, and in any case repulsion by surface charge would not explain why cations and anions are both excluded. The barrier is the nonpolar interior. *(outside knowledge contradicting the passage: membrane surfaces are not net positive)*
- **D.** Ions do cross bilayers without proteins, only very slowly; 'only' overstates the barrier and does not explain why the ionized form is slower. *(too extreme: ions cross slowly without transporters)*

*Tags:* chem_phys · general chemistry · FC5 5A · topics: 5A.ions-in-solution

*Takeaway:* Ions are hydrated by ion–dipole attractions; shedding that water to enter a nonpolar bilayer costs far too much energy, so only the un-ionized form of a drug diffuses across membranes at a useful rate.

*Sources*

- OpenStax Chemistry 2e, 11.2 Electrolytes (2019): the electrostatic attraction between an ion and a molecule with a dipole is an ion–dipole attraction; water molecules surround and solvate dissolved ions.
- OpenStax Biology 2e, 5.2 Passive Transport (2018): although small ions could fit through the membrane's spaces, their charge prevents them from crossing; nonpolar, lipid-soluble molecules pass through the fatty core.

*Status:* reviewed · rev 1

---

### CP-033  ·  ★★★★  ·  Skill 2 Reasoning

Which statement best explains why the sodium-salt tablet of W dissolved faster in fluid at pH 2.0, even though at equilibrium W is 99% un-ionized at that pH?

- **A.** The salt releases W as its neutral acid, which crosses the gastric mucosa faster than the anion that the free-acid tablet releases into the fluid
- **B.** The sodium ions neutralize the gastric fluid, raising its pH above 4.0, so that W remains mostly as its highly soluble anion in the bulk fluid
- **C.** The sodium ions are co-transported with the drug anion into the mucosal cells, pulling further drug out of the dissolving tablet and into solution
- **D.** The salt releases W as its anion, far more water-soluble than the neutral acid; protonation to the acid occurs only once the anion is in solution

**Answer: D**

*Worked solution*

- Dissolution and absorption are separate steps. A solid dissolves at a rate proportional to its solubility in the fluid at its surface; the ionic salt, whose anion is strongly hydrated, is far more soluble than the neutral, hydrogen-bonded acid, so the salt tablet releases drug much faster.
- The anion that leaves the solid is then protonated by the bulk acid (pH 2.0 is two units below the pKa, so 99% ends up as HA), but by then the drug is already in solution. Whether any of the neutral acid then precipitates depends on its own solubility and the dose; in this test 85% of the dose was in solution at 10 minutes.
- The passage confirms the two steps are separate: once dissolved, drug from either tablet is in the same equilibrium, which is why the total exposure was the same and only the time to peak differed.

*Why the other choices are wrong*

- **A.** The sodium salt releases the anion, not the acid, and the question concerns how fast the solid dissolves in the test fluid, not how fast drug crosses the mucosa. *(reversed relationship: salt and acid swapped, and dissolution confused with absorption)*
- **B.** Fluid at pH 2.0 contains 0.010 mol/L H⁺, about 9 mmol in 900 mL; a 1.0 mmol dose of the salt can consume at most 1 mmol of it, leaving the pH near 2.05. The bulk fluid stays far below the pKa. *(too extreme: a millimole of salt cannot neutralize the gastric fluid)*
- **C.** Co-transport is a process of living membranes; the dissolution test used a vessel of simulated gastric fluid with no cells, and the tablet dissolved faster there. *(out of scope: a transport mechanism invoked for a cell-free dissolution test)*

*Tags:* chem_phys · general chemistry · FC5 5A · topics: 5A.solubility, 5A.weak-acid-equilibria

*Takeaway:* A drug's salt dissolves faster because its ion is far more water-soluble than the neutral molecule; the pH of the fluid then sets the ionized:un-ionized ratio of what has dissolved, and that ratio governs absorption.

*Sources*

- Serajuddin, Salt formation to improve drug solubility, Advanced Drug Delivery Reviews 59:603–616 (2007): salt formation is the most common and effective way of raising the solubility and dissolution rate of acidic and basic drugs.
- OpenStax Chemistry 2e, 11.2 Electrolytes and 11.1 The Dissolution Process (2019): ionic compounds dissolve and dissociate as hydrated ions; dissolution is favoured when solute–solvent attractions outweigh solute–solute attractions.
- OpenStax Chemistry 2e, 14.6 Buffers (2019): the Henderson–Hasselbalch equation gives the ionized:un-ionized ratio at a given pH.

*Status:* reviewed · rev 1

---

### CP-034  ·  ★★★  ·  Skill 3 Research design

The investigators measured each drug's partition coefficient at a pH at which the drug was more than 99% un-ionized. Which statement best justifies this part of the design?

- **A.** The ionized form partitions into octanol more strongly than the neutral form, so a partly ionized sample would overstate the drug's affinity for the bilayer
- **B.** The neutral molecule's partitioning reflects only its own interactions with octanol and with water, so the value can be compared between drugs whatever their pKa values
- **C.** The un-ionized fraction at the chosen pH equals the fraction of an oral dose that is absorbed, so the value measured there predicts the plasma level directly
- **D.** Weak acids and weak bases are both fully ionized near pH 7, so a partition coefficient can be measured only far from neutral pH

**Answer: B**

*Worked solution*

- A partition coefficient compares how well a molecule's intermolecular interactions are satisfied in each solvent: dispersion and dipole contacts with octanol against hydrogen bonding and, for an ion, strong ion–dipole hydration in water.
- Measured on the neutral species, log P is a property of the molecule alone. Measured on a partly ionized sample, the apparent coefficient (log D) falls with the ionized fraction and so depends on the buffer's pH and on the drug's pKa, which would confound the comparison across four drugs with different pKa values.
- The design separates the two factors the passage then combines: how lipophilic the neutral molecule is (log P) and how much of the drug is neutral at a given pH (Henderson–Hasselbalch).

*Why the other choices are wrong*

- **A.** The ion is the form held in water by hydration; it partitions into octanol far less than the neutral form, so a partly ionized sample would understate, not overstate, lipophilicity. *(reversed relationship: which form prefers octanol)*
- **C.** A partition coefficient is an equilibrium ratio of concentrations in two solvents, not a fraction absorbed; absorption also depends on the ionized fraction at the site, the surface area and the time available. *(wrong formula: a partition coefficient treated as a fraction absorbed)*
- **D.** At pH 7 a weak acid of pKa 7.0 (drug X) is only half ionized and a base of pKa 5.0 (drug Z) is almost entirely neutral; 'fully' and 'only' are both wrong. *(too extreme: 'fully ionized' and 'only' contradict Table 1)*

*Tags:* chem_phys · general chemistry · FC5 5B · topics: 5B.intermolecular-forces, 5A.weak-acid-equilibria

*Takeaway:* log P is the octanol–water partition coefficient of the neutral molecule, set by its intermolecular interactions with each solvent; the pH-dependent value (log D) also depends on the ionized fraction and pKa.

*Sources*

- ACD/Labs, LogP vs LogD application note: log P is the partition coefficient of the un-ionized species and is independent of pH; log D includes the ionized species and varies with pH.
- OpenStax Chemistry 2e, 10.1 Intermolecular Forces and 11.3 Solubility (2019): dispersion, dipole–dipole and hydrogen-bonding interactions decide how a solute distributes between solvents.
- OpenStax Chemistry 2e, 11.2 Electrolytes (2019): ion–dipole attractions hold dissolved ions in water.

*Status:* reviewed · rev 1

---

### CP-035  ·  ★★★★  ·  Skill 4 Data and statistics

Based on Figure 1 and Table 1, which drug would be expected to be absorbed most readily from the stomach?

- **A.** Drug W
- **B.** Drug X
- **C.** Drug Y
- **D.** Drug Z

**Answer: A**

*Worked solution*

- Read the chart at pH 2.0: W and X are essentially all un-ionized (99.0% and 100.0%), while the two bases are almost entirely protonated (Y 0.0%, Z 0.1%). Only the acids have a neutral form available to cross the gastric epithelium.
- Then read Table 1: W has log P 2.5, inside the range the investigators considered favourable, whereas X has log P −1.0, meaning its neutral molecule favours water over octanol ten to one and partitions poorly into the bilayer. W is both neutral and lipophilic, so it is absorbed most readily.
- Two checks are needed because the bar chart alone cannot separate W from X; the ionized fraction and the lipophilicity of the neutral form are independent requirements. Most drugs, acids included, are absorbed mainly in the small intestine because of its far larger surface; the question concerns the stomach only.

*Why the other choices are wrong*

- **B.** X is un-ionized in the stomach, but its log P of −1.0 means the neutral molecule hardly enters the lipid phase; the chart alone is not enough. *(true but irrelevant: un-ionized but too hydrophilic to partition)*
- **C.** Y has a favourable log P, but at pH 2.0 a base of pKa 9.0 is protonated to one part in ten million; there is almost no neutral form to cross the membrane. *(reversed relationship: a weak base is ionized in acid)*
- **D.** Z reaches 90.9% un-ionized only in the intestine (pH 6.0); in the stomach it is 0.1% un-ionized, the wrong bar for this question. *(misread graph: the intestinal bar read for the stomach)*

*Tags:* chem_phys · general chemistry · FC5 5A · topics: 5A.weak-acid-equilibria, 5B.intermolecular-forces

*Takeaway:* Absorption from a compartment needs both a large un-ionized fraction at its pH and a neutral form lipophilic enough to enter the membrane; a weak acid with a moderate log P meets both in the stomach.

*Sources*

- Hogben, Schanker, Tocco and Brodie, Absorption of drugs from the stomach II. The human, J Pharmacol Exp Ther 120:540–545 (1957), summarized in Deranged Physiology, Factors which determine the lipid solubility of drugs: weak acids are un-ionized and lipid-soluble in acid; the pH-partition principle.
- ACD/Labs, LogP vs LogD application note: a negative log P marks a compound that prefers water to octanol.
- OpenStax Anatomy and Physiology 2e, 23.4 The Stomach (2022): gastric pH 1.5–3.5; the stomach absorbs little apart from some substances such as aspirin and alcohol.

*Status:* reviewed · rev 1

---

## Passage CP-P07: Purifying a His-tagged zinc hydrolase

In a hypothetical purification, a zinc-dependent hydrolase from a thermophilic bacterium was expressed in Escherichia coli with a six-histidine (His₆) tag at its N-terminus; the mass of the polypeptide predicted from its sequence is 50 kDa. The cells were lysed and the debris removed by centrifugation (step 1, cleared lysate). The lysate was applied to a column of agarose beads carrying Ni²⁺ held by a chelating group; after a wash with buffer containing 20 mmol/L imidazole, the enzyme was eluted with 250 mmol/L imidazole (step 2). The eluate was passed through a gel-filtration (size-exclusion) column equilibrated in 50 mmol/L Tris, pH 7.5, 150 mmol/L NaCl, a buffer containing no nickel (step 3); against globular protein standards the enzyme eluted at a position corresponding to about 100 kDa. Finally, to remove any Ni²⁺ that had leached from the column, the pooled fractions were dialysed overnight at 4 °C against the same buffer containing 5 mmol/L EDTA (step 4); the EDTA remained in the sample.

At each step the total protein was measured by the Bradford dye-binding assay and the enzyme activity by the rate of hydrolysis of a chromogenic substrate at 37 °C; one unit (U) hydrolyses 1 µmol of substrate per minute (Table 1). Samples from each step were heated in SDS, with and without the reducing agent dithiothreitol (DTT), and run on SDS-PAGE. The lysate lane showed many bands; the lanes from steps 2, 3 and 4 each showed a single band at 50 kDa whether or not DTT had been added, and a Western blot with an antibody against the His tag stained this band. When the step 4 sample was run again on the gel-filtration column, the enzyme still eluted at about 100 kDa.

The investigators noted that the specific activity had risen at every step but the last, and considered two explanations for the fall at step 4: that EDTA had removed a metal ion the enzyme requires, or that the enzyme had been denatured during the overnight dialysis.

**Table 1. Total protein and total activity at each step of the purification.**

| Step | Total protein (mg) | Total activity (U) |
|---|---|---|
| 1 Cleared lysate | 500 | 2,000 |
| 2 Ni²⁺ affinity eluate | 10 | 1,600 |
| 3 Gel filtration pool | 4.0 | 1,200 |
| 4 After dialysis with EDTA | 3.8 | 760 |

*Alt text:* Table with four rows. Step 1, cleared lysate: 500 milligrams of protein, 2,000 units of activity. Step 2, nickel affinity eluate: 10 milligrams, 1,600 units. Step 3, gel filtration pool: 4.0 milligrams, 1,200 units. Step 4, after dialysis with EDTA: 3.8 milligrams, 760 units.

*Source:* Hypothetical purification written for this app. His tags, nickel columns and elution by imidazole, and the elution order in gel filtration (largest first), from Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 8.2 Fractionation and Chromatography Techniques; imidazole competes with the tag for the metal-charged resin (Bio-Rad, His-tag purification guide). SDS-PAGE (SDS coats proteins so that charge is proportional to mass and they move at speeds inversely related to size; mercaptoethanol or DTT breaks disulfide bonds; native gels separate by charge and mass) from the same book, 8.3 Electrophoresis. Quaternary structure from OpenStax Biology 2e, 3.4 Proteins (2018). Purification-table conventions (specific activity = total activity/total protein; fold purification relative to the lysate; yield = activity recovered) from the Colorado State University handout Preparing a Summary Purification Table and the standard layout of purification tables in the literature. Zinc as an enzyme cofactor from OpenStax Biology 2e, 6.5 Enzymes; chelators strip zinc from carbonic anhydrase and Zn²⁺ restores the apoenzyme's activity (Lindskog and Malmström, J Biol Chem 237:1129 (1962); Udom and Brady, Biochem J 187:329–335 (1980)). Table values re-derived in review/chem_phys_batch_02_check.py.

*Status:* reviewed

### CP-036  ·  ★★★★  ·  Skill 4 Data and statistics

From Table 1, the fold purification and the yield achieved after step 3, relative to the cleared lysate, are closest to:

- **A.** 60-fold and 75%
- **B.** 75-fold and 60%
- **C.** 75-fold and 75%
- **D.** 125-fold and 60%

**Answer: B**

*Worked solution*

- Specific activity = total activity / total protein. Step 1: 2,000 U / 500 mg = 4.0 U/mg. Step 3: 1,200 U / 4.0 mg = 300 U/mg.
- Fold purification = 300 / 4.0 = 75. Yield = activity recovered / activity started with = 1,200 / 2,000 = 60%.
- Shortcut: 1,200/4 = 300; 300/4 = 75; 1,200/2,000 = 0.60. (Step 2 for comparison: 160 U/mg, 40-fold, 80%.)

*Why the other choices are wrong*

- **A.** 60 and 75 are the right numbers in the wrong places: 60% is the yield and 75 the fold purification. *(reversed relationship: fold and yield swapped)*
- **C.** 75% is the yield of step 3 relative to step 2 (1,200/1,600); the question asks for the yield relative to the lysate. *(wrong formula: step yield instead of overall yield)*
- **D.** 125 is the ratio of total protein (500 mg / 4.0 mg); fold purification is the ratio of specific activities, which also accounts for the activity lost. *(wrong formula: protein ratio instead of specific-activity ratio)*

*Tags:* chem_phys · biochemistry · FC5 5C · topics: 5C.protein-purification

*Takeaway:* Specific activity is activity per milligram of protein; fold purification is its ratio to the starting material, and yield is the fraction of the starting activity recovered.

*Sources*

- Colorado State University, Preparing a Summary Purification Table (handout): specific activity = activity/protein; fold purification compares each step's specific activity with the starting lysate; yield is the activity recovered.
- Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 8.2 Fractionation and Chromatography Techniques: specific activity rises as a protein is purified.

*Status:* reviewed · rev 1

---

### CP-037  ·  ★★★  ·  Skill 1 Knowledge

The enzyme was eluted from the Ni²⁺ column with 250 mmol/L imidazole because imidazole:

- **A.** reduces the Ni²⁺ to metallic nickel, which no longer coordinates the histidine side chains of the tag
- **B.** denatures the tagged protein, so that its histidine side chains can no longer reach the nickel ions
- **C.** lowers the pH of the buffer, so that the histidine side chains become protonated and lose their lone pairs
- **D.** is the ring of the histidine side chain and competes with the tag's histidines for the coordination sites on Ni²⁺

**Answer: D**

*Worked solution*

- The His tag binds because the imidazole ring of each histidine donates a nitrogen lone pair to an empty coordination site on the immobilized Ni²⁺.
- Free imidazole is that same ring. At 250 mmol/L it vastly outnumbers the tag's six histidines, occupies the coordination sites and displaces the protein, which then washes off; the 20 mmol/L wash removes proteins whose few scattered histidines bind more weakly.
- Shortcut: affinity columns are eluted with free ligand or a ligand look-alike that competes for the same binding site.

*Why the other choices are wrong*

- **A.** No redox chemistry is involved; imidazole is a Lewis base, not a reducing agent, and the column is reused with its Ni²⁺ intact. *(out of scope: a redox reaction that does not occur)*
- **B.** Imidazole at these concentrations is not a denaturant; the enzyme emerges active, as the 1,600 U recovered at step 2 shows. *(outside knowledge contradicting the passage: the eluted enzyme is active)*
- **C.** Imidazole is a weak base, not an acid, so adding it does not lower the pH. Protonating the histidines by lowering the pH is a different elution method, not what imidazole does. *(wrong formula: low-pH elution attributed to a basic additive)*

*Tags:* chem_phys · biochemistry · FC5 5C · topics: 5C.chromatography, 5C.protein-purification

*Takeaway:* Imidazole elutes His-tagged proteins by competing with the histidine imidazole rings for the coordination sites on the immobilized Ni²⁺.

*Sources*

- Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 8.2 Fractionation and Chromatography Techniques: histidine side chains bind nickel or cobalt ions; His-tagged proteins are eluted by adding imidazole.
- Bio-Rad, His-tag purification guide: imidazole competes with the His tag for binding to the metal-charged resin; low imidazole in the wash removes weakly bound contaminants.

*Status:* reviewed · rev 1

---

### CP-038  ·  ★★  ·  Skill 1 Knowledge

On the SDS-PAGE gels described in the passage, the distance each protein migrated depended chiefly on its:

- **A.** isoelectric point
- **B.** net charge in the native state
- **C.** molecular mass
- **D.** three-dimensional shape

**Answer: C**

*Worked solution*

- SDS is an anionic detergent that unfolds proteins into rod-like shapes and coats them with negative charge roughly in proportion to their length, so every protein has about the same charge-to-mass ratio.
- With charge and shape made uniform, the gel's sieving is the only thing left to separate them: smaller proteins thread through the pores faster and travel farther. Heating with DTT also breaks disulfide bonds so that each chain runs alone.
- That is why the 50 kDa band reports the mass of the polypeptide chain, not of the assembled enzyme.

*Why the other choices are wrong*

- **A.** The isoelectric point governs isoelectric focusing, in which proteins stop where the pH equals their pI; SDS masks native charge. *(wrong formula: the separating principle of isoelectric focusing)*
- **B.** Native charge matters in a native gel; SDS swamps it with a uniform negative charge. *(wrong formula: the separating principle of native PAGE)*
- **D.** SDS unfolds every protein into a similar rod, so native shape no longer differs between them. *(outside knowledge contradicting the passage: SDS removes shape differences)*

*Tags:* chem_phys · biochemistry · FC5 5D · topics: 5D.peptides-proteins, 5C.protein-purification

*Takeaway:* SDS-PAGE separates polypeptides by mass because SDS unfolds them and gives them a uniform charge-to-mass ratio; smaller chains run farther.

*Sources*

- Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 8.3 Electrophoresis: SDS denatures proteins to rod-like shapes and makes their charge proportional to mass; they move at velocities inversely related to size; mercaptoethanol or DTT breaks disulfide bonds; native gels separate by charge as well as mass.

*Status:* reviewed · rev 1

---

### CP-039  ·  ★★★★  ·  Skill 2 Reasoning

Gel filtration placed the enzyme at about 100 kDa, whereas SDS-PAGE, with or without DTT, showed a single band at 50 kDa. These results are best explained by an enzyme that is:

- **A.** a dimer of two identical 50 kDa chains held together by noncovalent interactions
- **B.** a dimer of two identical 50 kDa chains linked by an interchain disulfide bond
- **C.** a single 100 kDa chain that SDS cleaves into two 50 kDa halves
- **D.** a 50 kDa monomer, two of which are bridged by a Ni²⁺ ion shared between their His tags

**Answer: A**

*Worked solution*

- Gel filtration measures the size of the native, folded assembly: about 100 kDa. SDS unfolds proteins and breaks noncovalent contacts, and the chain it reveals is 50 kDa, the mass predicted from the sequence; so the native enzyme is two such chains, a quaternary structure.
- The band is the same without DTT, so no disulfide holds the chains together; the association is through noncovalent interactions (hydrophobic contacts, hydrogen bonds, salt bridges), which SDS disrupts and gel filtration preserves.
- Shortcut: native mass ÷ SDS-PAGE mass = number of subunits, if the SDS band survives omission of the reducing agent.

*Why the other choices are wrong*

- **B.** A disulfide-linked dimer would still run as 100 kDa in the lane without DTT, because SDS does not break covalent bonds; the passage says the band was 50 kDa with and without DTT. *(outside knowledge contradicting the passage: the non-reduced lane rules out a disulfide)*
- **C.** SDS denatures proteins but does not hydrolyse peptide bonds, and the sequence predicts a 50 kDa chain, not 100 kDa. *(wrong formula: denaturation confused with hydrolysis)*
- **D.** The dimer was seen on a gel-filtration column run in nickel-free buffer and again after EDTA, which chelates any stray Ni²⁺, so a metal bridge cannot be what holds it together. *(outside knowledge contradicting the passage: the dimer persisted without nickel and with EDTA)*

*Tags:* chem_phys · biochemistry · FC5 5D · topics: 5D.protein-3d-structure, 5C.protein-purification

*Takeaway:* A native mass that is a multiple of the SDS-PAGE band mass, unchanged by reducing agent, indicates subunits held together noncovalently: quaternary structure.

*Sources*

- OpenStax Biology 2e, 3.4 Proteins (2018): quaternary structure is the association of two or more polypeptide subunits through weak interactions and sometimes disulfide bonds; denaturation disrupts folding without breaking peptide bonds.
- Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 8.3 Electrophoresis: SDS unfolds and coats proteins; reducing agents break disulfide bonds; 8.2: in gel filtration larger molecules elute first.

*Status:* reviewed · rev 1

---

### CP-040  ·  ★★★★  ·  Skill 3 Research design

After step 4 the specific activity fell although little protein was lost. Which experiment most directly tests the hypothesis that EDTA removed a metal ion the enzyme requires, as opposed to the enzyme having been denatured during the overnight dialysis?

- **A.** Running the step 4 enzyme on SDS-PAGE beside the step 3 enzyme, with and without DTT, and comparing the positions of the bands
- **B.** Continuing the dialysis of the step 4 enzyme against the EDTA buffer for a further 48 hours and measuring whether its activity falls further
- **C.** Measuring the absorbance of the step 4 sample at 280 nm to confirm the protein concentration that the Bradford assay reported
- **D.** Dialysing a portion of the step 4 enzyme briefly against EDTA-free buffer, adding a little ZnCl₂ to half of it, and comparing the halves' activities

**Answer: D**

*Worked solution*

- The two hypotheses predict different responses to added metal. If EDTA stripped a catalytic Zn²⁺ from an otherwise intact enzyme, supplying Zn²⁺ should restore the activity; a denatured enzyme would not recover.
- The EDTA is removed first so that a small (micromolar) amount of zinc is free to bind, rather than being chelated or having to be added at the millimolar levels that themselves inhibit many enzymes. The half with no added zinc, handled identically, controls for the extra dialysis and for any change over time, so the comparison isolates the effect of the metal.
- Shortcut: to test 'X was removed', put X back under conditions where it can act, keep everything else the same, and see whether function returns. Reversal by the specific ion is the classic evidence for a metal cofactor.

*Why the other choices are wrong*

- **A.** A bound Zn²⁺ ion adds about 65 Da to a 50 kDa chain, invisible on a gel, and SDS unfolds every protein anyway, so the gel cannot show whether the enzyme had already lost its fold or its metal. *(true but irrelevant: SDS-PAGE reports neither bound metal nor folding)*
- **B.** Both hypotheses predict that a longer dialysis could lower the activity further, so a further fall would not tell them apart. *(out of scope: an outcome both hypotheses predict)*
- **C.** The question is why activity per milligram fell, not whether the milligrams were counted correctly; confirming the protein value with a second assay addresses neither hypothesis. *(true but irrelevant: checks the denominator, not the cause)*

*Tags:* chem_phys · biochemistry · FC5 5C · topics: 5C.protein-purification, 5E.enzymes-mechanism

*Takeaway:* Loss of activity after a chelator is attributed to a metal cofactor when adding the metal back restores activity; denaturation is not reversed by added ions.

*Sources*

- OpenStax Biology 2e, 6.5 Enzymes (2018): cofactors are inorganic ions such as Fe²⁺, Mg²⁺ and Zn²⁺ that some enzymes require; DNA polymerase needs a bound zinc ion; heat and extreme pH denature enzymes.
- Lindskog and Malmström, J Biol Chem 237:1129 (1962): chelators remove the single zinc from carbonic anhydrase, which the enzyme needs for activity; Udom and Brady, Biochem J 187:329–335 (1980): zinc salts or zinc-thionein restore activity to zinc apoenzymes (apo-thermolysin and apo-aldolase fully, apo-carbonic anhydrase partly).

*Status:* reviewed · rev 1

---

## Passage CP-P08: Doppler ultrasound of the umbilical cord

An ultrasound transducer contains a piezoelectric crystal that changes thickness when a voltage is applied across it and produces a voltage when a returning pressure wave compresses it, so the same crystal transmits sound and receives echoes. Echoes arise wherever the acoustic impedance (the product of density and speed of sound) changes; red blood cells scatter a small fraction of the beam back toward the probe. Sound is attenuated as it travels through tissue, and higher frequencies are attenuated more strongly over the same path. In a hypothetical examination at 36 weeks of gestation, a probe transmitting a continuous 3.00 MHz beam was placed over the mother's abdomen and aimed at loops of the umbilical cord. The speed of sound in soft tissue and blood was taken as 1,540 m/s.

Red cells moving relative to the probe shift the frequency of the echo. A cell moving toward the probe first meets wavefronts more often than a stationary reflector would, as a moving observer, and then re-emits the sound as a moving source, shortening the wavelength of the returning wave. For blood speeds v far below the speed of sound c the two shifts add, giving Equation 1, in which f₀ is the transmitted frequency and θ is the angle between the beam and the direction of flow. The scanner obtains Δf as the beat frequency between the transmitted and received signals and records it as positive for flow toward the probe.

The cord's artery and vein were examined in a loop lying along the beam (θ = 0°) and in a second loop crossing the beam at θ = 60° (Table 1). Arterial flow in the cord runs from the fetus to the placenta and is pulsatile; venous flow runs from the placenta to the fetus and is steady. In both loops the arterial blood was moving toward the probe and the venous blood away from it. The values for the artery are the peak systolic shifts.

**Equation 1. The Doppler shift of an echo from blood moving at speed v.**

Equation: `\Delta f = f_{\text{received}} - f_0 = \dfrac{2 f_0\, v \cos\theta}{c}`

*Alt text:* Delta f equals f received minus f zero, equals two f zero v cosine theta divided by c.

**Table 1. Doppler shifts recorded with the 3.00 MHz probe (artery: peak systolic; vein: steady flow).**

| Vessel | θ | Δf (Hz) |
|---|---|---|
| Umbilical artery, loop 1 | 0° | +2,000 |
| Umbilical vein, loop 1 | 0° | −600 |
| Umbilical artery, loop 2 | 60° | +1,000 |
| Umbilical vein, loop 2 | 60° | −300 |

*Alt text:* Table with four rows. Umbilical artery in loop 1, angle 0 degrees, shift plus 2,000 hertz. Umbilical vein in loop 1, angle 0 degrees, shift minus 600 hertz. Umbilical artery in loop 2, angle 60 degrees, shift plus 1,000 hertz. Umbilical vein in loop 2, angle 60 degrees, shift minus 300 hertz.

*Source:* Hypothetical examination written for this app. Piezoelectric transducers, echoes at changes of acoustic impedance, the double Doppler shift (moving observer, then moving source), 1,540 m/s as the speed of sound in tissue, strong absorption of higher frequencies and the resolution–penetration trade-off from OpenStax College Physics 2e, 17.7 Ultrasound (2022); v = fλ from 17.2 Speed of Sound, Frequency, and Wavelength; the Doppler effect from 17.4 Doppler Effect and Sonic Booms. The angle-corrected form Δf = 2 f₀ v cos θ / c and the practice of keeping θ below 60° from the British Medical Ultrasound Society teaching notes, Concepts of Doppler. Realism of the values: umbilical vein peak velocity about 18 cm/s (50th centile) at 36 weeks (Spurway, Logan, Pak and Nielsen, Australasian Journal of Ultrasound in Medicine 20:155–162 (2017)); third-trimester umbilical artery peak systolic speeds of roughly 40–65 cm/s in population studies. The speed of sound in blood is about 1,570 m/s (OpenStax Table 17.5); the passage states the single value it uses. Table values re-derived in review/chem_phys_batch_02_check.py.

*Status:* reviewed

### CP-041  ·  ★★★  ·  Skill 2 Reasoning

In loop 1 the echoes from the umbilical artery returned at a frequency above 3.00 MHz. This occurred because the red cells moving toward the probe:

- **A.** returned sound that travelled faster through the moving blood, so that more cycles reached the probe each second
- **B.** met wavefronts more often than a stationary reflector would, but re-emitted them with the spacing unchanged, so the shift arose once
- **C.** met wavefronts more often than a stationary reflector would, then re-emitted them with a shortened spacing, so the frequency was raised twice
- **D.** returned echoes of lower frequency, which the scanner reports as a positive shift by convention for arterial flow

**Answer: C**

*Worked solution*

- Passage: a cell moving toward the probe 'first meets wavefronts more often than a stationary reflector would' (moving observer, frequency raised by a factor (c + v)/c) 'and then re-emits the sound as a moving source' (wavelength shortened, frequency raised again by c/(c − v)).
- For v much smaller than c each step raises the frequency by about f₀v/c, so the echo returns at about f₀(1 + 2v/c): higher than transmitted, with twice the shift a single moving source would give. That factor 2 is the one in Equation 1.
- Approach raises frequency; recession lowers it. The vein, flowing away, gave negative shifts in Table 1, consistent with this.

*Why the other choices are wrong*

- **A.** The speed of sound is set by the medium, not by the motion of the reflector; the Doppler effect changes frequency and wavelength, not propagation speed. *(wrong formula: the Doppler shift attributed to a change in wave speed)*
- **B.** The cells act both as receiver and as re-emitter; leaving out the second shift halves the effect and contradicts the factor 2 in Equation 1. *(wrong formula: the second (moving-source) shift omitted)*
- **D.** Echoes from cells moving toward the probe are higher, not lower, in frequency, and the passage defines the sign of Δf by the direction of flow, not by vessel type. *(reversed relationship: the sign of the shift for approach)*

*Tags:* chem_phys · physics · FC4 4D · topics: 4D.doppler

*Takeaway:* Blood moving toward the probe returns echoes at a higher frequency, and the shift is doubled because the cells act first as moving receivers and then as moving sources.

*Sources*

- OpenStax College Physics 2e, 17.7 Ultrasound (2022): in Doppler ultrasound of blood there is a double shift, one as the blood receives the sound and one as it re-emits it (Example 17.8 with 1,540 m/s).
- OpenStax College Physics 2e, 17.4 Doppler Effect and Sonic Booms (2022): the observed frequency rises for approach and falls for recession.

*Status:* reviewed · rev 1

---

### CP-042  ·  ★★★  ·  Skill 2 Reasoning

The wavelength of the 3.00 MHz beam in soft tissue is closest to:

- **A.** 0.11 mm
- **B.** 0.51 mm
- **C.** 1.9 mm
- **D.** 5.1 mm

**Answer: B**

*Worked solution*

- v = fλ, so λ = v/f = (1,540 m/s)/(3.00 × 10⁶ s⁻¹) = 5.13 × 10⁻⁴ m = 0.51 mm.
- Shortcut: 1,500/3 = 500, so λ ≈ 500 × 10⁻⁶ m = 0.5 mm; the exact figure is slightly larger.
- Detail smaller than about a wavelength cannot be resolved, which is why half a millimetre is the order of the finest detail a 3 MHz scan can show.

*Why the other choices are wrong*

- **A.** 0.11 mm uses the speed of sound in air (about 330 m/s); the beam travels through tissue, where sound is nearly five times faster. *(wrong formula: the speed of sound in air used for tissue)*
- **C.** 1.9 mm comes from inverting the ratio, f/v = 1.9 × 10³ m⁻¹, and misreading the unit; wavelength is speed divided by frequency. *(wrong formula: frequency divided by speed)*
- **D.** 5.1 mm is ten times too large: 1,540/3 × 10⁶ is 5.1 × 10⁻⁴ m, not 5.1 × 10⁻³ m. *(sign or unit error: a power of ten)*

*Tags:* chem_phys · physics · FC4 4D · topics: 4D.sound-basics

*Takeaway:* λ = v/f: at 1,540 m/s a 3 MHz ultrasound beam has a wavelength of about 0.5 mm, which sets the scale of the detail it can resolve.

*Sources*

- OpenStax College Physics 2e, 17.2 Speed of Sound, Frequency, and Wavelength (2022): v = fλ; frequency is fixed by the source, wavelength by the medium.
- OpenStax College Physics 2e, 17.7 Ultrasound (2022): details smaller than the wavelength are hard to detect; 1,540 m/s used for tissue.

*Status:* reviewed · rev 1

---

### CP-043  ·  ★★  ·  Skill 1 Knowledge

A 3 MHz probe was chosen for the fetal examination rather than the 10 MHz probe used for superficial structures. Compared with the 10 MHz beam, the 3 MHz beam:

- **A.** travels faster through tissue, so echoes from deep structures return before they have been absorbed
- **B.** carries more energy in each cycle, so it reflects more strongly from interfaces deep in the body
- **C.** resolves finer detail, because resolution improves as the wavelength becomes longer
- **D.** is attenuated less, so it reaches deeper structures, at the cost of coarser resolution from its longer wavelength

**Answer: D**

*Worked solution*

- Passage: 'higher frequencies are attenuated more strongly over the same path'. Absorption in tissue rises with frequency, so a 10 MHz beam loses its energy within a few centimetres while a 3 MHz beam can reach a fetus through the maternal abdomen.
- The price is resolution: detail smaller than about a wavelength cannot be resolved, and at 3 MHz the wavelength is about 0.5 mm against about 0.15 mm at 10 MHz.
- The probe itself is a piezoelectric crystal that converts voltage to vibration and returning pressure to voltage, so one crystal both sends the pulse and receives the echo.

*Why the other choices are wrong*

- **A.** The speed of sound in a medium does not depend on frequency; both beams travel at about 1,540 m/s in tissue. *(wrong formula: wave speed made frequency-dependent)*
- **B.** Reflection at an interface depends on the change in acoustic impedance, not on the frequency; the energy a beam carries is set by its intensity, and the lower frequency is chosen because it is absorbed less, not because it reflects more. *(wrong formula: reflection attributed to frequency)*
- **C.** Resolution improves as the wavelength becomes shorter, so the 3 MHz beam resolves coarser, not finer, detail. *(reversed relationship: resolution and wavelength)*

*Tags:* chem_phys · physics · FC4 4D · topics: 4D.resonance-ultrasound, 4D.sound-basics

*Takeaway:* Higher ultrasound frequencies give finer resolution (shorter wavelength) but are absorbed more strongly and penetrate less; deep structures are imaged with lower frequencies.

*Sources*

- OpenStax College Physics 2e, 17.7 Ultrasound (2022): higher-frequency ultrasound allows greater detail but does not penetrate as well, because high frequencies are strongly absorbed; the transducer is a piezoelectric crystal that both transmits and receives.
- OpenStax College Physics 2e, 17.2 Speed of Sound, Frequency, and Wavelength (2022): the speed of sound is a property of the medium.

*Status:* reviewed · rev 1

---

### CP-044  ·  ★★★★  ·  Skill 2 Reasoning

Using Equation 1 and Table 1, the peak systolic blood speed in the umbilical artery is closest to:

- **A.** 0.26 m/s
- **B.** 0.51 m/s
- **C.** 1.0 m/s
- **D.** 2.1 m/s

**Answer: B**

*Worked solution*

- Rearrange Equation 1: v = Δf c / (2 f₀ cos θ). In loop 1, θ = 0° and cos θ = 1, with Δf = 2,000 Hz, f₀ = 3.00 × 10⁶ Hz and c = 1,540 m/s.
- v = (2,000 × 1,540)/(2 × 3.00 × 10⁶) = 3.08 × 10⁶ / 6.00 × 10⁶ = 0.51 m/s.
- Shortcut: Δf/f₀ = 2,000/3,000,000 = 2/3 × 10⁻³, and v = (Δf/f₀)(c/2) ≈ 0.67 × 10⁻³ × 770 ≈ 0.51 m/s. Check with loop 2: Δf = 1,000 Hz and cos 60° = 0.5 give the same speed, as they must for the same vessel.

*Why the other choices are wrong*

- **A.** 0.26 m/s results from using the loop 2 shift (1,000 Hz) without dividing by cos 60° = 0.5; the angle halves the shift, not the speed. *(wrong formula: cos θ omitted for the 60° loop)*
- **C.** 1.0 m/s leaves out the factor 2 in Equation 1, treating the cells as a moving source only. *(wrong formula: the factor 2 for the double shift omitted)*
- **D.** 2.1 m/s multiplies by 2 instead of dividing: v = Δf c/(2 f₀), since the double shift makes Δf twice as large for a given speed. *(sign or unit error: the factor 2 applied on the wrong side)*

*Tags:* chem_phys · physics · FC4 4D · topics: 4D.doppler

*Takeaway:* v = Δf c / (2 f₀ cos θ): a 2 kHz shift at 3 MHz along the flow corresponds to about 0.5 m/s, and the same speed gives half the shift at 60°.

*Sources*

- British Medical Ultrasound Society, Concepts of Doppler (teaching notes): Δf = 2 f₀ v cos θ / c; the factor 2 accounts for the wave travelling to the moving cells and back; angles above 60° give large velocity errors.
- OpenStax College Physics 2e, 17.7 Ultrasound (2022): Example 17.8, a 2.50 MHz beam and blood at 20.0 cm/s with 1,540 m/s give a 649 Hz beat frequency (about 2 f₀ v / c).
- Spurway, Logan, Pak and Nielsen, Australasian Journal of Ultrasound in Medicine 20:155–162 (2017): umbilical vein peak velocity about 18 cm/s at 36 weeks, consistent with the 0.15 m/s implied by the vein's shift.

*Status:* reviewed · rev 1

---

## Standalone questions

### CP-045  ·  ★★★  ·  Skill 2 Reasoning

An ambulance travelling at 20 m/s approaches an obstruction. The driver's reaction time is 1.0 s, during which the speed does not change; the brakes then slow the vehicle uniformly at 5.0 m/s² until it stops. The total distance travelled from the moment the obstruction is seen is closest to:

- **A.** 40 m
- **B.** 60 m
- **C.** 80 m
- **D.** 100 m

**Answer: B**

*Worked solution*

- Reaction phase (constant speed): d₁ = vt = 20 m/s × 1.0 s = 20 m.
- Braking phase (constant deceleration): v² = v₀² + 2a(x − x₀) with v = 0, v₀ = 20 m/s and a = −5.0 m/s², so d₂ = v₀²/(2|a|) = 400/10 = 40 m.
- Total: 20 m + 40 m = 60 m. Check the braking phase another way: t = v₀/|a| = 4.0 s and average speed 10 m/s give 40 m.

*Why the other choices are wrong*

- **A.** 40 m is the braking distance alone; the vehicle covers a further 20 m before the brakes are applied. *(true but irrelevant: braking distance without the reaction distance)*
- **C.** 80 m treats the 4.0 s of braking as if the speed stayed at 20 m/s; during uniform deceleration the average speed is half the initial speed. *(wrong formula: distance = v₀t during deceleration)*
- **D.** 100 m adds the 20 m reaction distance to that same overestimate of 80 m. *(wrong formula: the 80 m error plus the reaction distance)*

*Tags:* chem_phys · physics · FC4 4A · topics: 4A.kinematics

*Takeaway:* Stopping distance = reaction distance (v₀t) + braking distance (v₀²/2a); doubling the speed quadruples the braking part.

*Sources*

- OpenStax College Physics 2e, 2.5 Motion Equations for Constant Acceleration in One Dimension (2022): v² = v₀² + 2a(x − x₀); Example 2.12 adds the distance covered during a driver's reaction time to the braking distance.

*Status:* reviewed · rev 1

---

### CP-046  ·  ★★  ·  Skill 1 Knowledge

Bicarbonate ion acts as a base in reaction 1 and as an acid in reaction 2: (1) HCO₃⁻ + H₃O⁺ ⇌ H₂CO₃ + H₂O; (2) HCO₃⁻ + OH⁻ ⇌ CO₃²⁻ + H₂O. The conjugate acid of HCO₃⁻ and the conjugate base of HCO₃⁻ are, respectively:

- **A.** H₂CO₃ and CO₃²⁻
- **B.** CO₃²⁻ and H₂CO₃
- **C.** H₃O⁺ and OH⁻
- **D.** H₂O and H₂O

**Answer: A**

*Worked solution*

- A conjugate acid is the base plus one proton; a conjugate base is the acid minus one proton. Adding H⁺ to HCO₃⁻ gives H₂CO₃ (reaction 1); removing H⁺ from HCO₃⁻ gives CO₃²⁻ (reaction 2).
- A species that can both donate and accept a proton, such as HCO₃⁻, is amphiprotic; its conjugate acid and conjugate base differ from it by one proton in opposite directions.
- Shortcut: conjugate pairs differ by exactly one H⁺ and one unit of charge: H₂CO₃ / HCO₃⁻ and HCO₃⁻ / CO₃²⁻.

*Why the other choices are wrong*

- **B.** CO₃²⁻ has one proton fewer than bicarbonate, so it is the conjugate base, and H₂CO₃ has one more, so it is the conjugate acid; the pair is reversed. *(reversed relationship: conjugate acid and base swapped)*
- **C.** H₃O⁺ and OH⁻ are the acid and base that react with bicarbonate; a species' conjugates are formed from that species itself, not from its reaction partner. *(wrong formula: reaction partners taken as conjugates)*
- **D.** Water is the conjugate base of H₃O⁺ in reaction 1 and the conjugate acid of OH⁻ in reaction 2; it is not conjugate to bicarbonate in either. *(wrong formula: water's conjugates assigned to bicarbonate)*

*Tags:* chem_phys · general chemistry · FC5 5A · topics: 5A.acids-bases

*Takeaway:* An amphiprotic species such as HCO₃⁻ has a conjugate acid one proton richer (H₂CO₃) and a conjugate base one proton poorer (CO₃²⁻).

*Sources*

- OpenStax Chemistry 2e, 14.1 Brønsted-Lowry Acids and Bases (2019): conjugate acid and conjugate base defined; bicarbonate is amphiprotic, HCO₃⁻ + H₂O ⇌ CO₃²⁻ + H₃O⁺ and HCO₃⁻ + H₂O ⇌ H₂CO₃ + OH⁻.

*Status:* reviewed · rev 1

---

### CP-047  ·  ★★★  ·  Skill 1 Knowledge

α-D-Glucopyranose and β-D-glucopyranose are anomers. How do the two differ, and how are they related in aqueous solution?

- **A.** They differ in configuration at every stereocentre, as enantiomers do, and cannot interconvert without breaking bonds
- **B.** They differ in configuration only at C4, as glucose and galactose do, and cannot interconvert without an enzyme
- **C.** They differ in configuration only at C5, the carbon that defines the D series, and interconvert through the open-chain form
- **D.** They differ in configuration only at C1, the hemiacetal carbon formed on ring closure, and interconvert through the open-chain form

**Answer: D**

*Worked solution*

- When glucose's C5 hydroxyl adds to the C1 aldehyde, C1 becomes a new stereocentre, the anomeric carbon. The two possible configurations there are the α and β anomers; every other stereocentre is the same in both.
- In water the hemiacetal opens and recloses reversibly, so each pure anomer slowly converts into an equilibrium mixture (about one third α and two thirds β), observed as a changing optical rotation: mutarotation. No enzyme or bond-breaking beyond the reversible ring opening is required.
- Shortcut: anomers are epimers at the anomeric (hemiacetal or hemiketal) carbon, and only that carbon can flip through the open chain.

*Why the other choices are wrong*

- **A.** Enantiomers are mirror images differing at every stereocentre; the anomers share the configuration of C2–C5 and differ only at C1. *(wrong formula: enantiomers confused with anomers)*
- **B.** Glucose and galactose are C4 epimers; the anomers differ at C1, and they interconvert without any enzyme. *(wrong formula: C4 epimers confused with anomers)*
- **C.** C5 is the carbon whose configuration assigns the D or L series; it is unchanged by ring closure, and the anomers differ at C1. *(wrong formula: the D/L stereocentre confused with the anomeric carbon)*

*Tags:* chem_phys · organic chemistry · FC5 5D · topics: 5D.carbohydrates

*Takeaway:* Anomers differ only at the anomeric carbon (C1 of an aldose) created by ring closure, and they interconvert in water through the open-chain form (mutarotation).

*Sources*

- OpenStax Organic Chemistry, 25.5 Cyclic Structures of Monosaccharides: Anomers (2023): cyclization makes C1 a new chirality centre, the anomeric centre; α and β anomers; pure anomers interconvert in water by reversible ring opening to the aldehyde (mutarotation), reaching a 37:63 equilibrium mixture.

*Status:* reviewed · rev 1

---

### CP-048  ·  ★★★  ·  Skill 2 Reasoning

Partial hydrogenation of a vegetable oil adds H₂ across a C=C bond of an unsaturated fatty acid chain: R–CH=CH–R′ + H₂ → R–CH₂–CH₂–R′. Using average bond energies of 611 kJ/mol (C=C), 345 kJ/mol (C–C), 415 kJ/mol (C–H) and 436 kJ/mol (H–H), the enthalpy change per mole of C=C hydrogenated is closest to:

- **A.** −564 kJ/mol
- **B.** −128 kJ/mol
- **C.** +128 kJ/mol
- **D.** +287 kJ/mol

**Answer: B**

*Worked solution*

- ΔH ≈ Σ(bond energies of bonds broken) − Σ(bond energies of bonds formed). Broken: one C=C (611) and one H–H (436), total 1,047 kJ/mol. Formed: one C–C (345) and two C–H (2 × 415 = 830), total 1,175 kJ/mol.
- ΔH ≈ 1,047 − 1,175 = −128 kJ/mol: exothermic, as hydrogenations are (measured heats of hydrogenation run from −136 kJ/mol for ethylene to about −115 to −125 kJ/mol for substituted alkenes).
- Shortcut: the C–H bonds already on the alkene carbons appear on both sides and cancel; only the π bond and H–H are broken, and only a C–C σ bond and two new C–H bonds are made. Bond-energy sums are estimates because the tabulated values are averages.

*Why the other choices are wrong*

- **A.** −564 kJ/mol forgets that the H–H bond must be broken: 611 − 1,175. *(wrong formula: a broken bond omitted)*
- **C.** +128 kJ/mol subtracts in the wrong order (formed − broken); breaking bonds costs energy and forming them releases it, so the sign here is a sign error. *(sign or unit error: formed minus broken)*
- **D.** +287 kJ/mol counts only one new C–H bond (1,047 − 760); hydrogenation adds two hydrogens, one to each carbon. *(wrong formula: one of the two new C–H bonds omitted)*

*Tags:* chem_phys · general chemistry · FC5 5E · topics: 5E.enthalpy-hess

*Takeaway:* ΔH ≈ Σ(bonds broken) − Σ(bonds formed); hydrogenating one C=C breaks C=C and H–H (1,047 kJ) and forms C–C and two C–H (1,175 kJ), about −130 kJ/mol.

*Sources*

- OpenStax Chemistry 2e, 7.5 Strengths of Ionic and Covalent Bonds (2019): Table 7.2 average bond energies H–H 436, C–H 415, C–C 345, C=C 611 kJ/mol; ΔH = ΣD(bonds broken) − ΣD(bonds formed), a rough estimate because the values are averages.
- OpenStax Organic Chemistry, 7.6 Stability of Alkenes (2023): Table 7.2 heats of hydrogenation, ethylene −136, propene −125, cis-2-butene −119, trans-2-butene −115 kJ/mol; 8.6 Reduction of Alkenes: Hydrogenation: vegetable oils are hydrogenated on a large scale to make the saturated fats in margarine.

*Status:* reviewed · rev 1

---

### CP-049  ·  ★★  ·  Skill 1 Knowledge

A cylinder of medical gas is filled to a high pressure and stored outdoors in winter. Under which conditions does a real gas deviate most from PV = nRT, and why?

- **A.** Low pressure and high temperature, because the molecules then collide with one another so often that their motion is no longer random
- **B.** Low pressure and low temperature, because the molecules then spread so far apart that they rarely strike the walls of the container
- **C.** High pressure and low temperature, because the molecules' own volume then matters and their attractions are not overcome by thermal motion
- **D.** High pressure and high temperature, because the molecules then move so fast that the gas becomes easier to compress than the ideal law predicts

**Answer: C**

*Worked solution*

- The ideal gas law assumes molecules of negligible volume with no forces between them. At high pressure the molecules are crowded, so their own volume is an appreciable part of the total and the gas is harder to compress than predicted; at low temperature the molecules move slowly, so their mutual attractions pull them together and lower the pressure below the ideal value.
- The van der Waals equation corrects for both: b for the excluded volume and a for the attractions. The compressibility factor Z = PV/nRT departs furthest from 1 at high pressure and low temperature.
- Shortcut: gases behave ideally when they are dilute and hot (low P, high T), which is the opposite of a cold, full cylinder.

*Why the other choices are wrong*

- **A.** Low pressure and high temperature are the conditions under which real gases come closest to ideal behaviour; frequent collisions do not make motion non-random. *(reversed relationship: the ideal regime named as the non-ideal one)*
- **B.** At low pressure the molecules are far apart, which makes the ideal law work better, not worse; the wall collisions that create pressure never cease. *(wrong formula: the wrong half of the conditions, with a false mechanism)*
- **D.** High temperature overwhelms the attractions and brings the gas closer to ideal behaviour; a crowded gas is harder, not easier, to compress because of the molecules' own volume. *(reversed relationship: temperature and compressibility)*

*Tags:* chem_phys · general chemistry · FC4 4B · topics: 4B.real-gases

*Takeaway:* Real gases deviate most from PV = nRT at high pressure (molecular volume matters) and low temperature (attractions matter); they are most ideal when dilute and hot.

*Sources*

- OpenStax Chemistry 2e, 9.6 Non-Ideal Gas Behavior (2019): the ideal gas law fails at high pressure because the molecules' own volume becomes appreciable and attractions are no longer insignificant, and works best at low pressure and high temperature; the compressibility factor Z and the van der Waals equation.

*Status:* reviewed · rev 1

---

### CP-050  ·  ★★★  ·  Skill 1 Knowledge

A patient who drank rubbing alcohol (propan-2-ol, isopropanol) has a high blood level of the product formed when alcohol dehydrogenase oxidizes the carbon that carries the hydroxyl group. That product is:

- **A.** propanone
- **B.** propanal
- **C.** propanoic acid
- **D.** propene

**Answer: A**

*Worked solution*

- Propan-2-ol is a secondary alcohol: the carbon bearing the OH is bonded to two other carbons and one hydrogen. Oxidation removes that hydrogen and the O–H hydrogen, converting C–OH into C=O.
- A secondary alcohol therefore gives a ketone, here propanone, better known as acetone, CH₃COCH₃. Alcohol dehydrogenase does this with NAD⁺ as the hydride acceptor, just as it converts ethanol to acetaldehyde.
- Clinically, isopropanol poisoning is recognized by ketosis (acetone in the blood and breath) without the metabolic acidosis seen with methanol or ethylene glycol, because acetone is not oxidized further to an acid.

*Why the other choices are wrong*

- **B.** Propanal is the aldehyde from oxidizing the primary alcohol propan-1-ol; propan-2-ol's hydroxyl carbon has no second hydrogen to give an aldehyde and is not at the chain end. *(wrong formula: the primary-alcohol product)*
- **C.** A carboxylic acid arises only from further oxidation of an aldehyde, which needs a primary alcohol; a ketone's carbonyl carbon has no hydrogen left to remove without breaking a C–C bond. *(too extreme: oxidation carried past what a secondary alcohol allows)*
- **D.** Propene is the product of dehydration (elimination of water), not of oxidation; the H and the OH leave together, so the average oxidation state of the carbons is unchanged. *(wrong formula: elimination confused with oxidation)*

*Tags:* chem_phys · organic chemistry · FC5 5D · topics: 5D.alcohols

*Takeaway:* Oxidizing a secondary alcohol gives a ketone; a primary alcohol gives an aldehyde and then an acid; isopropanol is metabolized to acetone.

*Sources*

- OpenStax Organic Chemistry, 17.7 Oxidation of Alcohols (2023): primary alcohols are oxidized to aldehydes or carboxylic acids, secondary alcohols to ketones, tertiary alcohols normally not at all; biological oxidations use NAD⁺.
- StatPearls, Isopropanol Toxicity (NCBI Bookshelf NBK493181): isopropanol is converted to acetone in the liver by alcohol dehydrogenase; the result is ketosis without metabolic acidosis.

*Status:* reviewed · rev 1

---
