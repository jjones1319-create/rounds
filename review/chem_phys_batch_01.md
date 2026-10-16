# Review packet (key): block CP1

Plan: docs/CHEM_PHYS_250.md batch 1 (CP-001 to CP-025, passages CP-P01 to CP-P04); checks in review/chem_phys_batch_01_check.py

25 questions, 4 passages. Answers: 001C 002A 003A 004B 005D 006B 007A 008A 009B 010C 011D 012C 013A 014B 015A 016B 017D 018C 019A 020B 021D 022C 023C 024B 025D

Answer letters: A 7, B 7, C 6, D 5

## How this batch is reviewed

An independent blind re-solve (MCAT_SPEC §7): a fresh session answers every item from the blind packet; its answers and objections are compared with this key. Agreement with no objection passes the item (reviewed_by: independent blind re-solve); anything else is checked against the sources, fixed and re-solved. The batch is committed and pushed only after every item passes.

## Passage CP-P01: Pressure and flow across a carotid stenosis

In a hypothetical catheter study, investigators measured pressure and blood speed along a 50 mm length of a common carotid artery that contained a short, concentric atherosclerotic plaque. Along the healthy proximal and distal segments the lumen radius was 3.0 mm; within the plaque, which extended from x = 20 mm to x = 30 mm, the radius was 1.5 mm (a 50% reduction in diameter). A Doppler wire recorded the mean and peak systolic blood speeds in the proximal and distal segments (Table 1) but could not be positioned inside the narrowed segment. A pressure wire was then withdrawn slowly from the distal to the proximal end, recording the mean pressure at each position (Figure 1). A stethoscope placed over the plaque detected a bruit (a murmur) that was present only during systole.

For the analysis the investigators treated blood as an incompressible fluid of density 1.06 × 10³ kg/m³ and viscosity 3.0 × 10⁻³ Pa·s, took the vessel as horizontal, and used 1 mmHg = 133 Pa and g = 9.8 m/s². They applied the continuity equation and Bernoulli's equation to the entry of the narrowed segment, Poiseuille's law to the flow along it, and the Reynolds number, N_R = 2ρvr/η, to the onset of turbulence (laminar below about 2000, turbulent above about 3000).

Because the plaque was concentric and the flow steady on average, the pressure wire data were interpreted in three parts: an abrupt fall at the entry of the narrowed segment, a gradual decline along it, and a partial recovery just beyond its exit, where the fast jet slows and loses part of its energy to eddies. After the measurements the segment was dilated with a balloon so that its radius returned to 3.0 mm, and the pressure and Doppler recordings were repeated.

**Table 1. Lumen radius r and Doppler blood speeds (mean and peak systolic) in each segment before dilation.**

| Segment | r (mm) | Mean v (m/s) | Peak v (m/s) |
|---|---|---|---|
| Proximal, x = 0–20 mm | 3.0 | 0.30 | 0.75 |
| Narrowed, x = 20–30 mm | 1.5 | not measured | not measured |
| Distal, x = 30–50 mm | 3.0 | 0.30 | 0.75 |

*Alt text:* Table with three rows. Proximal segment: radius 3.0 mm, mean speed 0.30 m/s, peak systolic speed 0.75 m/s. Narrowed segment: radius 1.5 mm, speeds not measured. Distal segment: radius 3.0 mm, mean speed 0.30 m/s, peak systolic speed 0.75 m/s.

**Figure 1. Mean pressure recorded by the pressure wire against position along the vessel before dilation. The narrowed segment runs from x = 20 mm to x = 30 mm.**

Chart (line): x = Position x (mm); y = Mean pressure (mmHg).
- Before dilation: (0, 90.0), (10, 90.0), (19, 90.0), (20, 84.6), (25, 84.1), (30, 83.6), (31, 87.0), (40, 87.0), (50, 87.0)

*Alt text:* Line graph of mean pressure in millimetres of mercury against position in millimetres. The pressure is 90.0 mmHg from 0 to 19 mm, drops abruptly to 84.6 mmHg at 20 mm, the entry of the narrowed segment, declines steadily to 84.1 mmHg at 25 mm and 83.6 mmHg at 30 mm, the exit, then rises to 87.0 mmHg at 31 mm just beyond the exit and stays at 87.0 mmHg to 50 mm.

*Source:* Hypothetical experiment written for this app. Physics from OpenStax College Physics 2e, 12.1 Flow Rate and Its Relation to Velocity, 12.2 Bernoulli's Equation, 12.4 Viscosity and Laminar Flow; Poiseuille's Law, and 12.5 The Onset of Turbulence (2022). Blood density 1.05–1.06 × 10³ kg/m³ (OpenStax College Physics 2e Table 11.1); whole-blood viscosity at 37 °C spans about 2–4 mPa·s across sources (OpenStax Table 12.1 lists 2.084; measured high-shear values near 3.3–3.5 mPa·s), so the passage states the value it uses. Normal common carotid diameter about 6 mm and peak systolic speed about 0.9 m/s (The Ultrasound Journal, 2010, Table 1).

*Status:* reviewed

### CP-001  ·  ★★★  ·  Skill 2 Reasoning

Based on Table 1, the mean blood speed inside the narrowed segment before dilation was closest to:

- **A.** 0.075 m/s
- **B.** 0.60 m/s
- **C.** 1.2 m/s
- **D.** 4.8 m/s

**Answer: C**

*Worked solution*

- Blood is treated as incompressible, so the volume flow rate Av is the same in every segment (continuity): A₁v₁ = A₂v₂.
- The area of a circular lumen is πr², so v₂ = v₁ (r₁/r₂)² = 0.30 m/s × (3.0/1.5)² = 0.30 × 4 = 1.2 m/s.
- Shortcut: halving the radius quarters the area, so the speed quadruples.

*Why the other choices are wrong*

- **A.** 0.075 m/s is 0.30 m/s divided by 4: the speed has been made proportional to the area instead of inversely proportional to it; a narrower tube carries the same flow faster, not slower. *(reversed relationship: speed taken as proportional to area)*
- **B.** 0.60 m/s doubles the speed because the radius halved, but the area, which is what continuity uses, falls with the square of the radius. *(wrong formula: radius ratio used instead of its square)*
- **D.** 4.8 m/s multiplies by 2⁴ = 16, the fourth-power dependence that belongs to Poiseuille's law for flow at a fixed pressure difference, not to continuity. *(wrong formula: Poiseuille's r⁴ applied to continuity)*

*Tags:* chem_phys · physics · FC4 4B · topics: 4B.continuity-bernoulli

*Takeaway:* For an incompressible fluid, A₁v₁ = A₂v₂, so halving a vessel's radius quadruples the speed of the blood through it.

*Sources*

- OpenStax College Physics 2e, 12.1 Flow Rate and Its Relation to Velocity (2022): A₁v̄₁ = A₂v̄₂; speed is inversely proportional to the square of the tube radius.

*Status:* reviewed · rev 1

---

### CP-002  ·  ★★★★★  ·  Skill 4 Data and statistics

In Figure 1 the mean pressure at the entry of the narrowed segment (x = 20 mm) is lower than the proximal pressure. Using Table 1 and the constants in the passage, this difference is best accounted for by:

- **A.** ½ρ(v₂² − v₁²), about 7 × 10² Pa, the kinetic energy per unit volume that the blood gains as it speeds up
- **B.** ½ρ(v₂ − v₁)², about 4 × 10² Pa, the kinetic energy per unit volume associated with the change in speed
- **C.** 8ηLv₂/r₂², about 1 × 10² Pa, the viscous pressure loss along the 10 mm narrowed segment
- **D.** ρg × 0.020 m, about 2 × 10² Pa, the hydrostatic pressure change over the 20 mm the wire travelled

**Answer: A**

*Worked solution*

- Read the chart: the pressure falls from 90.0 mmHg (x ≤ 19 mm) to 84.6 mmHg at x = 20 mm, a drop of 5.4 mmHg, which is 5.4 × 133 ≈ 7.2 × 10² Pa.
- Bernoulli's equation along a horizontal streamline: P₁ + ½ρv₁² = P₂ + ½ρv₂², so P₁ − P₂ = ½ρ(v₂² − v₁²). With v₁ = 0.30 m/s (Table 1) and v₂ = 1.2 m/s (continuity, four times faster), v₂² − v₁² = 1.44 − 0.09 = 1.35 m²/s², and ½ × 1060 × 1.35 ≈ 530 × 1.35 ≈ 7.2 × 10² Pa.
- Shortcut: v₁² is only one sixteenth of v₂², so the drop is about 15/16 of ½ρv₂² ≈ 0.94 × 760 ≈ 7.2 × 10² Pa. The drop occurs abruptly where the speed changes, which is the signature of a kinetic (Bernoulli) effect rather than a loss that accumulates with length.

*Why the other choices are wrong*

- **B.** The Bernoulli terms are ½ρv² for each speed; their difference is ½ρ(v₂² − v₁²), not ½ρ(v₂ − v₁)². The wrong expression gives 530 × 0.81 ≈ 4.3 × 10² Pa (3.2 mmHg), which does not match the 5.4 mmHg drop in Figure 1. *(wrong formula: difference of speeds squared instead of difference of squared speeds)*
- **C.** The viscous (Poiseuille) loss along the narrowed segment is real but is the gentle decline from x = 20 mm to x = 30 mm in Figure 1 (about 1 mmHg, or 1.3 × 10² Pa); it accumulates with length and cannot produce the abrupt fall at the entry. *(true but irrelevant: the viscous loss is the gradual decline, not the entry drop)*
- **D.** The vessel is horizontal in the analysis, so there is no hydrostatic term along it; ρgh with h = 0.020 m would be about 2.1 × 10² Pa, which neither matches the drop nor applies here. *(wrong formula: a hydrostatic term applied to a horizontal vessel)*

*Tags:* chem_phys · physics · FC4 4B · topics: 4B.continuity-bernoulli, 4B.viscosity-poiseuille

*Takeaway:* Where a vessel narrows, the pressure falls by ½ρ(v₂² − v₁²) over the short entry region; viscous losses, by contrast, grow with the length of the segment.

*Sources*

- OpenStax College Physics 2e, 12.2 Bernoulli's Equation (2022): P₁ + ½ρv₁² + ρgh₁ = P₂ + ½ρv₂² + ρgh₂; pressure drops in a rapidly moving fluid.
- OpenStax College Physics 2e, 12.4 Viscosity and Laminar Flow; Poiseuille's Law (2022): Q = (P₂ − P₁)πr⁴/(8ηl), so the viscous pressure loss grows with tube length.

*Status:* reviewed · rev 1

---

### CP-003  ·  ★★★★  ·  Skill 2 Reasoning

Consider the 10 mm segment on its own, with laminar flow and the same pressure difference maintained between its two ends. Compared with the flow through the segment before the plaque formed (radius 3.0 mm), the flow with the plaque in place (radius 1.5 mm) is:

- **A.** 1/16 as large
- **B.** 1/8 as large
- **C.** 1/4 as large
- **D.** 1/2 as large

**Answer: A**

*Worked solution*

- Poiseuille's law for laminar flow through a tube: Q = πr⁴ΔP/(8ηL). With ΔP, η and L fixed, Q is proportional to r⁴.
- Halving the radius multiplies the flow by (1/2)⁴ = 1/16.
- This is why small changes in vessel radius, by plaque or by smooth-muscle tone, have such large effects on flow: a 50% narrowing cuts flow at a given pressure difference by about 94%.

*Why the other choices are wrong*

- **B.** 1/8 corresponds to a cubic dependence (r³), which is not the exponent in Poiseuille's law. *(wrong formula: r³ instead of r⁴)*
- **C.** 1/4 is the change in cross-sectional area (r²); at a fixed pressure difference the flow falls much faster than the area, because the fluid near the walls moves slowly and a narrower tube is wall-dominated. *(wrong formula: area (r²) instead of r⁴)*
- **D.** 1/2 treats flow as proportional to the radius itself; it is proportional to the fourth power. *(wrong formula: flow taken as proportional to r)*

*Tags:* chem_phys · physics · FC4 4B · topics: 4B.viscosity-poiseuille

*Takeaway:* At a fixed pressure difference, laminar flow through a tube scales with r⁴, so halving the radius cuts the flow sixteenfold.

*Sources*

- OpenStax College Physics 2e, 12.4 Viscosity and Laminar Flow; Poiseuille's Law (2022): Q = (P₂ − P₁)πr⁴/(8ηl), with r raised to the fourth power.

*Status:* reviewed · rev 1

---

### CP-004  ·  ★★★  ·  Skill 1 Knowledge

The bruit heard over the plaque was present only during systole. Which of the following best explains this observation?

- **A.** During systole the pressure inside the narrowed segment rises above the proximal pressure, and that pressure difference vibrates the vessel wall.
- **B.** Only at peak systolic speed does the Reynolds number in the narrowed segment rise past the laminar range, so eddies form and make noise.
- **C.** Blood viscosity falls during systole, which lowers the Reynolds number in the narrowed segment and lets the flow separate from the wall.
- **D.** Surface tension at the surface of the plaque is overcome only at the systolic pressure peak, releasing bubbles that are heard as a murmur.

**Answer: B**

*Worked solution*

- Governing principle: N_R = 2ρvr/η. In a tube the flow is laminar below about 2000 and turbulent above about 3000; between those values it is unstable.
- In the narrowed segment, at mean flow v = 1.2 m/s and r = 1.5 mm: N_R = 2 × 1060 × 1.2 × 1.5 × 10⁻³ / 3.0 × 10⁻³ ≈ 1.3 × 10³ (laminar). At peak systole the speed is four times the proximal peak, 4 × 0.75 = 3.0 m/s, so N_R ≈ 2 × 1060 × 3.0 × 1.5 × 10⁻³ / 3.0 × 10⁻³ ≈ 3.2 × 10³, above the turbulent threshold. In the proximal segment even the peak value (v = 0.75 m/s, r = 3.0 mm) is only about 1.6 × 10³.
- Turbulent flow is noisy: the same physics produces Korotkoff sounds under a blood-pressure cuff and the murmurs of narrowed valves. Since the Reynolds number scales with speed, the threshold is crossed only at the systolic peak, so the bruit comes and goes with each heartbeat.

*Why the other choices are wrong*

- **A.** Bernoulli's equation gives the opposite: where the blood moves faster, inside the narrowing, the pressure is lower than proximally (Figure 1 shows the fall). *(reversed relationship: pressure taken to rise where speed rises)*
- **C.** The Reynolds number rises, not falls, when viscosity falls (η is in the denominator), and blood viscosity does not change meaningfully within one heartbeat. *(reversed relationship: lower viscosity lowers rather than raises N_R, and the premise is false)*
- **D.** Surface tension concerns liquid–gas interfaces and there is no gas phase in the artery; the murmur is sound generated by turbulent liquid flow. *(out of scope: surface tension has no role in single-phase arterial flow)*

*Tags:* chem_phys · physics · FC4 4B · topics: 4B.turbulence-surface-tension

*Takeaway:* N_R = 2ρvr/η rises with speed; a stenosis pushes the systolic Reynolds number past the laminar range, and the resulting turbulence is heard as a bruit.

*Sources*

- OpenStax College Physics 2e, 12.5 The Onset of Turbulence (2022): N_R = 2ρvr/η; laminar below about 2000, unstable between 2000 and 3000, turbulent above about 3000; turbulence is noisy (Korotkoff sounds).
- OpenStax College Physics 2e, 12.2 Bernoulli's Equation (2022): pressure drops in a rapidly moving fluid.

*Status:* reviewed · rev 1

---

### CP-005  ·  ★★★  ·  Skill 3 Research design

The investigators proposed that the plaque was responsible for the lower pressure in the distal segment (87.0 mmHg against 90.0 mmHg proximally). Which finding after balloon dilation would provide the strongest support for this proposal?

- **A.** The proximal pressure rises above 90.0 mmHg.
- **B.** The mean speed in the treated segment is about 0.30 m/s, a quarter of the value calculated for the narrowed segment before dilation.
- **C.** The bruit over the treated segment disappears.
- **D.** The distal pressure returns to within about 1 mmHg of the proximal pressure.

**Answer: D**

*Worked solution*

- The proposal is about the pressure drop across the plaque. The direct test is to remove the plaque's narrowing and see whether the pressure difference disappears: if the distal pressure returns to nearly the proximal value, the drop depended on the narrowing.
- Flow in the circulation follows Q = ΔP/R; the arterial pressure that reaches the tissues downstream depends on the resistance of the segments upstream. A focal narrowing adds resistance and dissipates energy (Figure 1 shows the drop and the incomplete recovery). Restoring the radius removes that resistance, so the pressure downstream should recover.
- This is the logic of a within-subject before-and-after comparison: the same vessel, with and without the narrowing.

*Why the other choices are wrong*

- **A.** A change in proximal pressure says nothing about the pressure lost across the plaque; the proposal concerns the difference between proximal and distal segments, and proximal pressure is set largely by the heart and the rest of the circulation. *(true but irrelevant: proximal pressure is not the quantity in question)*
- **B.** A fall in speed inside the dilated segment is required by continuity whenever the radius returns to 3.0 mm; it would happen whether or not the plaque had reduced distal pressure, so it does not test the proposal. *(true but irrelevant: follows from continuity regardless of the hypothesis)*
- **C.** Loss of the bruit shows that the flow is no longer turbulent, but turbulence and the pressure loss are different consequences of the narrowing; a bruit could vanish while a smaller residual pressure drop persists, so this is weaker evidence than measuring the pressure itself. *(true but irrelevant: measures turbulence, not perfusion pressure)*

*Tags:* chem_phys · biology · FC4 4B · topics: 4B.circulation

*Takeaway:* To show that a narrowing caused a downstream pressure loss, remove the narrowing and measure the same pressure difference again: Q = ΔP/R, and a focal stenosis is added resistance.

*Sources*

- OpenStax Anatomy and Physiology 2e, 20.2 Blood Flow, Blood Pressure, and Resistance (2022): blood flow is proportional to the pressure difference and inversely proportional to resistance; vessel radius is the main determinant of resistance.
- OpenStax College Physics 2e, 12.4 Viscosity and Laminar Flow; Poiseuille's Law (2022): Q = (P₂ − P₁)/R with R = 8ηl/(πr⁴).

*Status:* reviewed · rev 1

---

## Passage CP-P02: Blood gases in metabolic acidosis

A hospital laboratory calibrates its blood-gas analyser each morning. The analyser measures arterial pH and the partial pressure of carbon dioxide (PCO₂) with electrodes thermostatted at 37 °C, and then reports the bicarbonate concentration from the Henderson–Hasselbalch equation for the bicarbonate buffer, pH = pKa′ + log([HCO₃⁻]/(0.03 × PCO₂)), with [HCO₃⁻] in mmol/L, PCO₂ in mmHg, 0.03 mmol·L⁻¹·mmHg⁻¹ as the solubility coefficient of CO₂ in plasma at 37 °C, and pKa′ = 6.1, the apparent pKa of carbonic acid in plasma at 37 °C when dissolved CO₂ is counted as the acid. The ion product of water at 37 °C is Kw = 2.4 × 10⁻¹⁴.

In a hypothetical morning, samples from three patients were analysed (Table 1). Patient 1 was a healthy volunteer. Patient 2 had diabetic ketoacidosis and was breathing rapidly and deeply. Patient 3 had been found unresponsive after an overdose that depressed breathing; the pH electrode failed during this sample, so the analyser recorded PCO₂ and the laboratory measured [HCO₃⁻] directly by a separate enzymatic method.

To check the pKa′ programmed into the analyser, the laboratory titrated 100.0 mL of a 20 mmol/L solution of dissolved CO₂ (carbonic acid) in 0.15 mol/L NaCl with 0.200 mol/L NaOH at 37 °C in a sealed cell, so that no CO₂ could escape, recording the pH after each addition (Figure 1). The volume of titrant was small compared with the sample, and dilution was ignored. The titration was carried only to the first equivalence point, at 10.0 mL, where essentially all of the carbonic acid had been converted to bicarbonate; the second proton (pKa₂′ about 10) was not titrated.

**Table 1. Arterial blood-gas results for the three patients (reference range for a healthy adult: pH 7.35–7.45, PCO₂ 35–45 mmHg, HCO₃⁻ 22–26 mmol/L).**

| Patient | pH | PCO₂ (mmHg) | HCO₃⁻ (mmol/L) |
|---|---|---|---|
| 1 | 7.40 | 40 | 24 |
| 2 | 7.10 | 20 | 6 |
| 3 | not recorded | 80 | 12 |

*Alt text:* Table with three rows. Patient 1: pH 7.40, PCO2 40 mmHg, bicarbonate 24 mmol/L. Patient 2: pH 7.10, PCO2 20 mmHg, bicarbonate 6 mmol/L. Patient 3: pH not recorded, PCO2 80 mmHg, bicarbonate 12 mmol/L.

**Figure 1. pH of 100.0 mL of 20 mmol/L carbonic acid (dissolved CO₂) in 0.15 mol/L NaCl at 37 °C against the volume of 0.200 mol/L NaOH added, in a sealed cell. The first equivalence point is at 10.0 mL.**

Chart (line): x = Volume of 0.200 mol/L NaOH added (mL); y = pH.
- Carbonic acid, 37 °C: (0, 3.9), (1, 5.15), (2, 5.5), (3, 5.73), (4, 5.92), (5, 6.1), (6, 6.28), (7, 6.47), (8, 6.7), (9, 7.05), (9.5, 7.36), (10, 8.05), (10.5, 8.74), (11, 9.04), (12, 9.39)

*Alt text:* Titration curve of pH against volume of sodium hydroxide added in millilitres. The curve starts at pH 3.9 with no base, rises to pH 5.5 at 2 mL, 5.9 at 4 mL, 6.1 at 5 mL, 6.3 at 6 mL, 6.7 at 8 mL and 7.05 at 9 mL, then climbs steeply through pH 8.05 at 10 mL (the equivalence point) to 8.7 at 10.5 mL, 9.0 at 11 mL and 9.4 at 12 mL. The gentlest slope is around 5 mL, halfway to equivalence.

*Source:* Hypothetical experiment written for this app. Henderson–Hasselbalch form, pKa′ 6.1 at 37 °C and the solubility coefficient 0.03 mmol/L per mmHg from Acid-Base Physiology (Brandis), 2.2 Buffering (anaesthesiamcq.com; Medicine LibreTexts mirror); 20:1 bicarbonate to carbonic acid ratio from OpenStax Anatomy and Physiology 2e, 26.4 Acid-Base Balance (2022); half-equivalence pH = pKa from OpenStax Chemistry 2e, 14.7 Acid-Base Titrations (2019); Kw at 37 °C = 2.4 × 10⁻¹⁴ (neutral pH 6.81) from University of Waterloo Chem 13 News, Tough questions series, 2014 exam; carbonic acid Ka₁ 4.3 × 10⁻⁷ at 25 °C in pure water from OpenStax Chemistry 2e Appendix H. The curve was computed from the stated concentrations with pKa₁′ = 6.1 and pKa₂′ = 10.0 (review/chem_phys_batch_01_check.py).

*Status:* reviewed

### CP-006  ·  ★★★★  ·  Skill 2 Reasoning

Using the analyser's equation and the values in Table 1, the arterial pH of Patient 3 was closest to:

- **A.** 5.3
- **B.** 6.8
- **C.** 7.1
- **D.** 7.4

**Answer: B**

*Worked solution*

- Passage: pH = pKa′ + log([HCO₃⁻]/(0.03 × PCO₂)) with pKa′ = 6.1. For Patient 3, [HCO₃⁻] = 12 mmol/L and PCO₂ = 80 mmHg.
- Dissolved CO₂ = 0.03 × 80 = 2.4 mmol/L. Ratio = 12/2.4 = 5. log 5 = log 10 − log 2 = 1 − 0.30 = 0.70. pH = 6.1 + 0.70 = 6.80.
- Check against Patient 1: 24/(0.03 × 40) = 24/1.2 = 20, log 20 = 1.30, pH = 7.40, as in the table. Patient 3 has both a low bicarbonate (metabolic acidosis) and a high PCO₂ from depressed breathing (respiratory acidosis), so the ratio is far below 20 and the pH is severely low.

*Why the other choices are wrong*

- **A.** 5.3 comes from taking the ratio 12/80 = 0.15 without converting PCO₂ in mmHg to dissolved CO₂ in mmol/L (log 0.15 ≈ −0.82): the two quantities in the ratio must be in the same units. *(sign or unit error: PCO₂ not converted with the 0.03 solubility coefficient)*
- **C.** 7.1 results from using a normal PCO₂ of 40 mmHg (ratio 12/1.2 = 10, log 10 = 1): the table gives 80 mmHg for this patient. *(misread graph: PCO₂ read as the reference value instead of the table value)*
- **D.** 7.4 assumes the patient is normal or that respiratory compensation has restored the ratio to 20; with [HCO₃⁻] = 12 that would need PCO₂ = 20 mmHg, the opposite of the measured 80. *(true but irrelevant: the normal pH, not this patient's)*

*Tags:* chem_phys · biochemistry · FC5 5A · topics: 5A.buffers

*Takeaway:* For blood, pH = 6.1 + log([HCO₃⁻]/(0.03 × PCO₂)); a ratio of 20 gives 7.4, and each halving of the ratio lowers the pH by 0.30.

*Sources*

- Acid-Base Physiology (Brandis), 2.2 Buffering (anaesthesiamcq.com): pH = 6.1 + log{[HCO₃⁻]/(0.03 × PCO₂)}, pKa′ 6.1 at 37 °C, 0.03 mmol/L per mmHg.
- OpenStax Chemistry 2e, 14.6 Buffers (2019): Henderson–Hasselbalch equation.

*Status:* reviewed · rev 1

---

### CP-007  ·  ★★  ·  Skill 1 Knowledge

The analyser's electrodes are held at 37 °C, where Kw = 2.4 × 10⁻¹⁴. A sample of pure water at 37 °C is best described as:

- **A.** neutral, with a pH slightly below 7
- **B.** slightly acidic, because its pH is below 7
- **C.** neutral, with a pH of exactly 7.00, because only [OH⁻] changes with temperature
- **D.** slightly basic, because the extra ionization at 37 °C produces more OH⁻ than H₃O⁺

**Answer: A**

*Worked solution*

- Water self-ionizes, 2 H₂O ⇌ H₃O⁺ + OH⁻, producing the two ions in equal numbers, so pure water is always neutral: [H₃O⁺] = [OH⁻] whatever the temperature.
- Kw = [H₃O⁺][OH⁻] = [H₃O⁺]² = 2.4 × 10⁻¹⁴, so [H₃O⁺] = √(2.4 × 10⁻¹⁴) ≈ 1.5 × 10⁻⁷ mol/L and pH = 7 − log 1.5 ≈ 7 − 0.18 ≈ 6.8.
- Neutral means [H₃O⁺] = [OH⁻], not pH 7; pH 7 is neutral only at 25 °C, where Kw = 1.0 × 10⁻¹⁴. Self-ionization is endothermic, so Kw grows with temperature and the neutral pH falls.

*Why the other choices are wrong*

- **B.** A pH below 7 does not make a solution acidic unless [H₃O⁺] exceeds [OH⁻]; in pure water they are equal at every temperature. *(wrong formula: neutrality equated with pH 7 rather than [H₃O⁺] = [OH⁻])*
- **C.** The ions are produced together, so [H₃O⁺] and [OH⁻] rise together; neither can change alone, and pH 7.00 is neutral only when Kw = 1.0 × 10⁻¹⁴. *(wrong formula: one ion assumed to change without the other)*
- **D.** Self-ionization produces one OH⁻ for every H₃O⁺, so the extra ionization cannot create an excess of either. *(reversed relationship: ionization produces the ions in equal numbers)*

*Tags:* chem_phys · general chemistry · FC5 5A · topics: 5A.acids-bases

*Takeaway:* Neutral means [H₃O⁺] = [OH⁻] = √Kw; because Kw rises with temperature, neutral water at 37 °C has pH about 6.8, not 7.

*Sources*

- OpenStax Chemistry 2e, 14.1 Brønsted-Lowry Acids and Bases (2019): autoionization is endothermic and Kw increases with temperature; in pure water [H₃O⁺] = [OH⁻].
- University of Waterloo, Chem 13 News, Tough questions series, 2014 exam: Kw at 37 °C = 2.4 × 10⁻¹⁴, [H₃O⁺] = 1.5 × 10⁻⁷ mol/L, pH 6.81.

*Status:* reviewed · rev 1

---

### CP-008  ·  ★★★★  ·  Skill 4 Data and statistics

According to Figure 1, the apparent pKa of carbonic acid under the conditions of the titration is closest to:

- **A.** 6.1
- **B.** 7.4
- **C.** 8.1
- **D.** 10.0

**Answer: A**

*Worked solution*

- For a weak acid titrated with strong base, pH = pKa at the half-equivalence point, where half of the acid has been converted to its conjugate base so that [A⁻] = [HA] and the log term in the Henderson–Hasselbalch equation is zero.
- Equivalence check: 100.0 mL × 20 mmol/L = 2.0 mmol of carbonic acid, which needs 2.0 mmol of OH⁻, that is 2.0 mmol ÷ 0.200 mmol/mL = 10.0 mL of NaOH, as the passage states. Half-equivalence is therefore at 5.0 mL.
- Reading Figure 1 at half of the equivalence volume, 5.0 mL, gives pH 6.1, which matches the pKa′ the analyser uses. The curve is flattest there, the centre of the buffer region, as expected.

*Why the other choices are wrong*

- **B.** 7.4 is the normal arterial pH, which lies in the buffer region of the curve (about 9.5 mL) but is not the pKa; the bicarbonate system holds blood far from its pKa because the lungs and kidneys keep the ratio near 20:1. *(true but irrelevant: physiological pH is not a feature of the curve)*
- **C.** 8.1 is the pH at the equivalence point (10.0 mL), where the solution is essentially sodium bicarbonate; the equivalence pH of a weak acid is above 7, but it is not the pKa. *(misread graph: equivalence point read instead of half-equivalence)*
- **D.** 10.0 is roughly the second pKa (bicarbonate losing its proton), which the passage says was not titrated; it cannot be read from a curve that stops at the first equivalence point. *(out of scope: the second proton was not titrated)*

*Tags:* chem_phys · general chemistry · FC5 5A · topics: 5A.titration, 5A.buffers

*Takeaway:* On a weak-acid titration curve, pH equals pKa at half the equivalence volume, the flattest part of the curve.

*Sources*

- OpenStax Chemistry 2e, 14.7 Acid-Base Titrations (2019): pH = pKa at the half-equivalence point in a titration of a weak acid.
- OpenStax Chemistry 2e, 14.6 Buffers (2019): Henderson–Hasselbalch equation, pH = pKa + log([A⁻]/[HA]).

*Status:* reviewed · rev 1

---

### CP-009  ·  ★★★★  ·  Skill 2 Reasoning

Based on Table 1, whose blood has the least remaining capacity for the bicarbonate buffer to take up additional acid (H⁺) produced by metabolism?

- **A.** Patient 1, because a ratio of 20:1 is far from the ideal buffer ratio of 1:1
- **B.** Patient 2, because the bicarbonate concentration, the base that accepts H⁺, is lowest
- **C.** Patient 3, because the pH is lowest
- **D.** Patients 2 and 3 equally, because both have a bicarbonate-to-CO₂ ratio below 20

**Answer: B**

*Worked solution*

- Added H⁺ is removed by the base of the pair: H⁺ + HCO₃⁻ → H₂CO₃ → CO₂ + H₂O. The capacity to absorb more acid is set by how much HCO₃⁻ remains, since the CO₂ formed is breathed off and does not accumulate.
- Table 1: [HCO₃⁻] is 24 mmol/L (Patient 1), 6 mmol/L (Patient 2) and 12 mmol/L (Patient 3). Patient 2 has only a quarter of the normal bicarbonate left; a further acid load of 6 mmol/L would exhaust the buffer entirely.
- Patient 2's pH (7.10) is less severe than Patient 3's (6.80) only because rapid deep breathing has lowered PCO₂ to 20 mmHg; that compensation hides how little bicarbonate reserve remains.

*Why the other choices are wrong*

- **A.** Patient 1 has the largest bicarbonate reserve. The 20:1 ratio is far from the 1:1 ideal for a closed buffer, but the bicarbonate system is open (CO₂ is exhaled), and the reserve against acid is the amount of HCO₃⁻, which is normal here. *(reversed relationship: the normal patient has the most reserve)*
- **C.** pH reports the current ratio, not the reserve; Patient 3's low pH is driven largely by a high PCO₂ (the acid side), while twice as much bicarbonate remains as in Patient 2. *(misread graph: pH taken as a measure of remaining capacity)*
- **D.** A ratio below 20 shows that both patients are acidaemic, but capacity for more acid depends on the absolute bicarbonate concentration, which is 6 mmol/L in one and 12 mmol/L in the other. *(too extreme: equal ratios below 20 treated as equal reserves)*

*Tags:* chem_phys · biochemistry · FC5 5A · topics: 5A.buffers

*Takeaway:* A buffer's reserve against added acid is the amount of its base form; in blood that is [HCO₃⁻], and respiratory compensation can normalise pH while the reserve stays dangerously low.

*Sources*

- OpenStax Chemistry 2e, 14.6 Buffers (2019): buffer capacity depends on the amounts of the weak acid and its conjugate base; added strong acid is consumed by the conjugate base.
- OpenStax Anatomy and Physiology 2e, 26.4 Acid-Base Balance (2022): bicarbonate and carbonic acid are present at 20:1, which makes the system most effective against added acid.

*Status:* reviewed · rev 1

---

### CP-010  ·  ★★★  ·  Skill 3 Research design

The laboratory performed the calibration titration at 37 °C, the temperature of the analyser's electrodes, rather than at room temperature. Which statement best justifies this choice?

- **A.** The ionic strength of a solution rises with temperature, and the apparent pKa′ of carbonic acid depends on the ionic strength.
- **B.** Kw equals 1.0 × 10⁻¹⁴ only at 37 °C, so the electrodes can measure pH accurately only at that temperature.
- **C.** Ka is an equilibrium constant and changes with temperature, so a pKa′ measured at 25 °C would not apply to blood at 37 °C.
- **D.** The solubility coefficient of CO₂ does not depend on temperature, so temperature needs to be controlled only for the electrodes.

**Answer: C**

*Worked solution*

- Ka is the equilibrium constant of HA ⇌ H⁺ + A⁻. Like every equilibrium constant, its value is fixed only at a given temperature: changing the temperature re-establishes equilibrium with a different K (the forward and reverse rate constants respond differently to temperature). Concentration or pressure changes shift the position of an equilibrium but leave K unchanged; temperature is the one variable that changes K itself.
- The analyser uses pKa′ to convert measured pH and PCO₂ into [HCO₃⁻] for blood at 37 °C, so the constant it needs is the one that holds at 37 °C in a plasma-like solution. Titrating at the same temperature (and at plasma ionic strength, 0.15 mol/L NaCl) measures the constant under the conditions in which it will be applied.
- The passage's own data illustrate the principle: Kw, another equilibrium constant, is 2.4 × 10⁻¹⁴ at 37 °C but 1.0 × 10⁻¹⁴ at 25 °C.

*Why the other choices are wrong*

- **A.** Ionic strength does affect pKa′, which is why the titration used 0.15 mol/L NaCl, but ionic strength is set by the dissolved ions, not by temperature; the statement confuses two separate conditions. *(true but irrelevant: ionic strength matters but is not a function of temperature)*
- **B.** Kw is 1.0 × 10⁻¹⁴ at 25 °C and 2.4 × 10⁻¹⁴ at 37 °C (passage); pH can be measured at any temperature with a thermostatted, calibrated electrode. *(outside knowledge contradicting the passage: Kw at 37 °C is given as 2.4 × 10⁻¹⁴)*
- **D.** The solubility of a gas in water falls as temperature rises, so the 0.03 coefficient is itself a 37 °C value; the claim is false, and it also ignores the dependence of Ka on temperature. *(reversed relationship: gas solubility does change with temperature)*

*Tags:* chem_phys · general chemistry · FC5 5A · topics: 5A.weak-acid-equilibria

*Takeaway:* Only temperature changes the value of an equilibrium constant such as Ka or Kw, so a constant must be measured, or looked up, at the temperature at which it will be used.

*Sources*

- OpenStax Chemistry 2e, 13.3 Shifting Equilibria: Le Châtelier's Principle (2019): a change in temperature changes the value of the equilibrium constant, whereas changes in concentration or pressure do not.
- Acid-Base Physiology (Brandis), 2.2 Buffering (anaesthesiamcq.com): the pKa of the bicarbonate system depends on temperature, [H⁺] and ionic strength (6.099 at 37 °C, pH 7.4).
- OpenStax Chemistry 2e, 11.3 Solubility (2019): the solubility of gases in water decreases as temperature rises.

*Status:* reviewed · rev 1

---

## Passage CP-P03: Screening an inhibitor of a protein kinase

Protein kinases transfer the terminal (γ) phosphate of ATP to a serine, threonine or tyrosine side chain of a protein substrate. In the cell, ATP exists almost entirely as its complex with Mg²⁺, and kinase assays therefore include MgCl₂ in excess of ATP. In a hypothetical screen, a purified kinase was assayed at 30 °C, pH 7.5, with 1.0 mmol/L ATP, 5.0 mmol/L MgCl₂, a fixed amount of enzyme, and a short peptide substrate whose phosphorylated product was quantified after 2 minutes. The initial rate v₀ was measured at six peptide concentrations [S], first without and then with a candidate inhibitor at 20 µmol/L (Table 1).

Fitting the uninhibited data to the Michaelis–Menten equation, v₀ = Vmax[S]/(Km + [S]), gave the enzyme's Km and Vmax. Fitting the inhibited data gave the same Vmax, within error, and an apparent Km of 60 µmol/L.

To test whether the inhibitor binds reversibly, the enzyme was incubated with 20 µmol/L inhibitor for 30 minutes and then dialysed for 12 hours against a large volume of inhibitor-free assay buffer through a membrane that retains the enzyme but passes small molecules. The dialysed enzyme was then assayed at [S] = 20 µmol/L: its rate was 51 nmol/min, 85% of the 60 nmol/min given by untreated enzyme at the same substrate concentration (with inhibitor present, the rate at this concentration was 30 nmol/min, Table 1). No other samples were dialysed.

**Table 1. Initial rate v₀ of the kinase (nmol/min) at six peptide concentrations, without and with 20 µmol/L inhibitor.**

| [S] (µmol/L) | v₀, no inhibitor | v₀, with inhibitor |
|---|---|---|
| 5 | 24 | 9 |
| 10 | 40 | 17 |
| 20 | 60 | 30 |
| 40 | 80 | 48 |
| 200 | 109 | 92 |
| 2000 | 119 | 117 |

*Alt text:* Table with six rows of peptide concentration and two rate columns in nanomoles per minute. At 5 micromolar: 24 without inhibitor, 9 with. At 10: 40 and 17. At 20: 60 and 30. At 40: 80 and 48. At 200: 109 and 92. At 2000: 119 and 117.

*Source:* Hypothetical experiment written for this app. Michaelis–Menten kinetics, Km and Lineweaver–Burk intercepts from Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 4.1 Basic Principles of Catalysis; competitive, non-competitive, uncompetitive and irreversible inhibition from the same book, 4.2 Control of Enzymatic Activity; cofactors such as Mg²⁺ from OpenStax Biology 2e, 6.5 Enzymes (2018); the Mg²⁺–ATP complex as the true substrate of ATP-using enzymes (dissociation constant about 0.1 mmol/L) from Berg, Tymoczko and Stryer, Biochemistry, 5th ed. (2002), section 9.4. Table values were generated from Vmax = 120 nmol/min, Km = 20 µmol/L and an apparent Km of 60 µmol/L (review/chem_phys_batch_01_check.py).

*Status:* reviewed

### CP-011  ·  ★★★  ·  Skill 4 Data and statistics

From the uninhibited data in Table 1, the kinase's Km and Vmax are closest to:

- **A.** Km = 20 µmol/L, Vmax = 60 nmol/min
- **B.** Km = 60 µmol/L, Vmax = 120 nmol/min
- **C.** Km = 2000 µmol/L, Vmax = 119 nmol/min
- **D.** Km = 20 µmol/L, Vmax = 120 nmol/min

**Answer: D**

*Worked solution*

- Vmax is the rate the enzyme approaches when the substrate saturates it. In Table 1 the rate rises from 109 nmol/min at 200 µmol/L to 119 at 2000 µmol/L, a tenfold increase in [S] for almost no gain, so the plateau is at about 120 nmol/min.
- Km is the substrate concentration at which v₀ = Vmax/2 = 60 nmol/min. The table gives exactly 60 nmol/min at [S] = 20 µmol/L, so Km = 20 µmol/L.
- Check with the Michaelis–Menten equation at 40 µmol/L: 120 × 40/(20 + 40) = 80 nmol/min, as tabulated; and at 2000 µmol/L: 120 × 2000/2020 ≈ 119.

*Why the other choices are wrong*

- **A.** 60 nmol/min is Vmax/2, the rate at Km, not the maximum; the rates in the table go well above 60. *(misread graph: the half-maximal rate taken as Vmax)*
- **B.** 60 µmol/L is the apparent Km in the presence of the inhibitor (the passage states it), not the enzyme's own Km, which comes from the uninhibited column. *(misread graph: the inhibited value used for the uninhibited enzyme)*
- **C.** Km is not the highest substrate concentration tested, and 119 is a rate near saturation rather than a concentration; Km is defined by the half-maximal rate. *(wrong formula: Km confused with the largest [S] tested)*

*Tags:* chem_phys · biochemistry · FC5 5E · topics: 5E.enzyme-kinetics

*Takeaway:* Read Vmax from the plateau at saturating substrate and Km as the substrate concentration that gives half of it.

*Sources*

- Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 4.1 Basic Principles of Catalysis: Km is the substrate concentration that causes the enzyme to work at half of Vmax; Vmax is the maximum velocity.
- OpenStax Biology 2e, 6.5 Enzymes (2018): the rate rises with substrate until the active sites are saturated.

*Status:* reviewed · rev 1

---

### CP-012  ·  ★★★★  ·  Skill 2 Reasoning

If the uninhibited data in Table 1 were plotted as 1/v₀ against 1/[S] (a Lineweaver–Burk plot), with v₀ in nmol/min and [S] in µmol/L, the intercepts on the vertical and horizontal axes would be:

- **A.** vertical 1/20 min/nmol, horizontal −1/120 L/µmol
- **B.** vertical 120 nmol/min, horizontal −20 µmol/L
- **C.** vertical 1/120 min/nmol, horizontal −1/20 L/µmol
- **D.** vertical 1/120 min/nmol, horizontal +1/20 L/µmol

**Answer: C**

*Worked solution*

- Taking reciprocals of the Michaelis–Menten equation gives 1/v₀ = (Km/Vmax)(1/[S]) + 1/Vmax, a straight line in 1/[S].
- Setting 1/[S] = 0 gives the vertical intercept 1/Vmax = 1/120 min/nmol; setting 1/v₀ = 0 gives the horizontal intercept −1/Km = −1/20 L/µmol (that is, −0.05), on the negative side of the axis. The slope is Km/Vmax = 20/120 = 1/6.
- Check with one data point: at [S] = 10 µmol/L, 1/[S] = 0.10 and 1/v₀ should be (1/6)(0.10) + 1/120 = 0.0167 + 0.0083 = 0.025 min/nmol, so v₀ = 40 nmol/min, as in Table 1.

*Why the other choices are wrong*

- **A.** The two intercepts have been swapped: 1/Vmax belongs on the vertical axis (the rate axis) and −1/Km on the horizontal (the substrate axis). *(reversed relationship: the intercepts interchanged)*
- **B.** These are Vmax and Km themselves; a double-reciprocal plot gives their reciprocals, and the units (min/nmol, L/µmol) show it. *(wrong formula: reciprocals not taken)*
- **D.** The horizontal intercept is −1/Km, to the left of the origin; a positive intercept would require a negative Km. *(sign or unit error: the horizontal intercept is negative)*

*Tags:* chem_phys · biochemistry · FC5 5E · topics: 5E.enzyme-kinetics

*Takeaway:* On a Lineweaver–Burk plot the vertical intercept is 1/Vmax, the horizontal intercept is −1/Km and the slope is Km/Vmax.

*Sources*

- Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 4.1 Basic Principles of Catalysis: Km is the negative reciprocal of the x-intercept and Vmax the reciprocal of the y-intercept of a Lineweaver–Burk plot.

*Status:* reviewed · rev 1

---

### CP-013  ·  ★★★★  ·  Skill 2 Reasoning

The inhibitor's effect on Km and Vmax fits a competitive model, in which the apparent Km equals Km(1 + [I]/Ki). Using the Km from the uninhibited data, the apparent Km given in the passage and the inhibitor concentration used, Ki is closest to:

- **A.** 10 µmol/L
- **B.** 20 µmol/L
- **C.** 40 µmol/L
- **D.** 60 µmol/L

**Answer: A**

*Worked solution*

- Passage: with 20 µmol/L inhibitor the apparent Km was 60 µmol/L and Vmax was unchanged. From the uninhibited column of Table 1, Km = 20 µmol/L (the rate there, 60 nmol/min, is half of the 120 nmol/min plateau).
- Competitive inhibition: Km,app = Km(1 + [I]/Ki). So 60 = 20 × (1 + 20/Ki), which gives 1 + 20/Ki = 3, 20/Ki = 2 and Ki = 10 µmol/L.
- Shortcut: the apparent Km tripled, so [I]/Ki = 2 and Ki is half the inhibitor concentration. A Ki below the concentration tested means most of the free enzyme carries inhibitor at 20 µmol/L, yet Vmax is still reached at saturating substrate because the peptide displaces it (Table 1: 117 against 119 nmol/min at 2000 µmol/L).

*Why the other choices are wrong*

- **B.** 20 µmol/L is the inhibitor concentration itself; Ki would equal [I] only if the apparent Km had doubled (1 + [I]/Ki = 2), but it tripled. *(wrong formula: Ki set equal to [I] whatever the Km ratio)*
- **C.** 40 µmol/L is the difference between the apparent and true Km (60 − 20); the competitive relation is multiplicative, Km,app = Km(1 + [I]/Ki), not additive. *(wrong formula: the Km difference taken as Ki)*
- **D.** 60 µmol/L is the apparent Km read straight from the passage, not the inhibition constant; Ki describes the inhibitor–enzyme pair and is found from how far the apparent Km exceeds Km. *(misread graph: the apparent Km reported as Ki)*

*Tags:* chem_phys · biochemistry · FC5 5E · topics: 5E.enzyme-inhibition-regulation, 5E.enzyme-kinetics

*Takeaway:* For a competitive inhibitor, Km,app = Km(1 + [I]/Ki): the factor by which the apparent Km exceeds Km, minus one, equals [I]/Ki.

*Sources*

- Chemistry LibreTexts, Biochemistry Online (Jakubowski), Competitive Inhibition (CSU Chico CHEM 451, 8.4 Enzyme Inhibition): Kmapp = Km(1 + I/Kis), the Km term multiplied by 1 + I/Kis, while Vm does not change.
- Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 4.2 Control of Enzymatic Activity: competitive inhibition leaves Vmax unchanged and raises the apparent Km; it is overcome by raising the substrate concentration.

*Status:* reviewed · rev 1

---

### CP-014  ·  ★★  ·  Skill 1 Knowledge

The assay included MgCl₂ in excess of ATP. Mg²⁺ is required in the assay because it:

- **A.** is consumed as a co-substrate, donating the electrons that reduce the γ-phosphate before it is transferred
- **B.** binds the negatively charged phosphates of ATP, forming the Mg²⁺–ATP complex that the kinase recognises as its substrate
- **C.** is covalently bonded to the kinase as a prosthetic group and carries the phosphate between ATP and the peptide
- **D.** raises the pH of the buffer to the kinase's optimum

**Answer: B**

*Worked solution*

- Passage: in the cell ATP exists almost entirely as its complex with Mg²⁺. Inorganic ions such as Mg²⁺ are cofactors: non-protein helpers an enzyme needs for activity. For enzymes that use ATP, the true substrate is the metal–nucleotide complex, and the enzymes are essentially inactive without a divalent metal ion.
- The triphosphate chain of ATP carries several negative charges. Mg²⁺ coordinates phosphate oxygens, neutralising part of that charge and holding the phosphates in a defined conformation that the active site can bind and from which the γ-phosphate can be transferred.
- Because the Mg²⁺–ATP dissociation constant is about 0.1 mmol/L, adding MgCl₂ in excess of ATP (5 mmol/L against 1 mmol/L) ensures that essentially all the ATP is in the complexed, usable form.

*Why the other choices are wrong*

- **A.** Phosphoryl transfer is not a redox reaction and Mg²⁺ is not consumed; it is a cofactor, released unchanged after each turnover. *(wrong formula: a redox role given to a Lewis-acid cofactor)*
- **C.** Mg²⁺ binds ATP and the enzyme noncovalently; a prosthetic group is a tightly bound organic cofactor such as heme, and the phosphate is transferred directly from ATP to the substrate hydroxyl. *(out of scope: a prosthetic group is covalently or tightly bound and organic)*
- **D.** Mg²⁺ is not a base and MgCl₂ does not raise pH; the buffer sets the pH at 7.5. *(true but irrelevant: pH is set by the buffer, not the salt)*

*Tags:* chem_phys · biology · FC5 5E · topics: 5E.enzymes-mechanism

*Takeaway:* Kinases use Mg²⁺–ATP, not free ATP: the Mg²⁺ cofactor neutralises and positions the phosphates so that the γ-phosphate can be transferred.

*Sources*

- OpenStax Biology 2e, 6.5 Enzymes (2018): cofactors are inorganic ions such as Fe²⁺ and Mg²⁺ that enzymes require for activity.
- Berg, Tymoczko and Stryer, Biochemistry, 5th ed. (2002), section 9.4 (NMP kinases): enzymes using ATP are essentially inactive without divalent metal ions; the metal ion–nucleotide complex is the true substrate; the ATP–Mg²⁺ dissociation constant is about 0.1 mM.

*Status:* reviewed · rev 1

---

### CP-015  ·  ★★★★★  ·  Skill 3 Research design

After dialysis, the inhibitor-treated enzyme showed 85% of the activity of untreated enzyme. Which conclusion is best supported, and what additional sample is most needed to interpret the remaining 15% loss?

- **A.** Most of the inhibition is reversible, since dialysis restored most of the activity; enzyme dialysed without inhibitor is needed to show how much activity the dialysis itself removes.
- **B.** The inhibitor is partly irreversible, because 15% of the enzyme must have been covalently modified; a sample with a higher inhibitor concentration is needed to measure the covalent fraction.
- **C.** The inhibitor was not removed by dialysis, because activity did not return fully; enzyme assayed with inhibitor but without dialysis is needed.
- **D.** The inhibitor is noncompetitive, because activity was measured at a single substrate concentration; a full substrate series after dialysis is needed to classify it.

**Answer: A**

*Worked solution*

- A reversible inhibitor binds noncovalently and dissociates; dialysis against inhibitor-free buffer removes the free inhibitor through the membrane, the bound inhibitor dissociates to restore equilibrium, and activity returns. An irreversible inhibitor is covalently attached and stays with the enzyme, so activity does not return. At 20 µmol/L substrate the rate rose from 30 nmol/min with inhibitor present (half of the uninhibited 60, Table 1) to 51 nmol/min after dialysis (85%), so most of the inhibition was reversible.
- The 15% shortfall has two candidate causes: incomplete reversal (some inhibitor still bound or irreversibly attached) or damage to the enzyme during 12 hours of dialysis (denaturation, adsorption to the membrane, loss of a cofactor). The passage says no other samples were dialysed, so the experiment cannot tell them apart.
- The missing control is enzyme carried through the identical dialysis without inhibitor. If it also loses about 15%, the inhibition was fully reversible; if it loses nothing, the 15% is a genuine residual inhibition. Treating a procedure's own effect as part of the result is the classic confound this control removes.

*Why the other choices are wrong*

- **B.** Attributing the 15% loss to covalent modification assumes the dialysis itself was harmless, which was never tested; and a higher inhibitor concentration would not separate reversible from irreversible loss. *(too extreme: a residual loss assigned to a mechanism without the control)*
- **C.** The rate rose from half of the uninhibited value with inhibitor present to 85% after dialysis, so most of the inhibitor was clearly removed; the proposed sample is simply the inhibited measurement already in Table 1. *(outside knowledge contradicting the passage: activity rose substantially after dialysis)*
- **D.** Inhibitor type is read from the change in Km and Vmax across a substrate series with inhibitor present (the passage reports competitive-type behaviour); a single post-dialysis rate says nothing about mechanism, and the question is about reversibility. *(out of scope: inhibitor type is not what the dialysis tests)*

*Tags:* chem_phys · biochemistry · FC5 5E · topics: 5E.enzyme-inhibition-regulation

*Takeaway:* Recovery of activity after dialysis shows reversible (noncovalent) inhibition, but only an enzyme-only sample dialysed in parallel can show whether any residual loss is inhibition or the cost of the procedure.

*Sources*

- Biology LibreTexts, Biochemistry Free For All (Ahern, Rajagopal, Tan), 4.2 Control of Enzymatic Activity: irreversible inhibitors become covalently bound to the enzyme; reversible inhibitors bind noncovalently.
- Chemistry LibreTexts, The Basics of General, Organic, and Biological Chemistry (Ball et al.), 18.8 Enzyme Inhibition: a reversible inhibitor can dissociate from the enzyme; an irreversible inhibitor bonds covalently and the inhibition cannot be reversed.

*Status:* reviewed · rev 1

---

## Passage CP-P04: Calibrating a fluorine-18 dose for PET

Positron emission tomography (PET) most often uses fluorine-18 attached to a glucose analogue, ¹⁸F-fluorodeoxyglucose (FDG), which accumulates in tissues that take up glucose rapidly. Fluorine-18 (Z = 9, A = 18) decays with a half-life of 110 minutes, mainly by positron emission; the positron travels about a millimetre in tissue, slows, and annihilates with an electron. The rest energy of an electron (and of a positron) is 511 keV. The scanner's ring of detectors registers only pairs of photons that arrive at the same moment at two detectors, and reconstructs the line along which the annihilation occurred.

In a hypothetical morning at a PET centre, a vial of FDG was delivered from the cyclotron at 08:00 and its activity measured in a dose calibrator at four times while it waited for patients (Table 1). A patient's prescribed dose was to be drawn from the vial so that the activity injected would be close to 250 MBq, and the volume drawn was adjusted for the time of injection. A second vial from the same batch, calibrated at 1200 MBq at 08:00, was reserved for an afternoon patient injected at 15:20.

Constants used by the centre: Planck's constant h = 6.63 × 10⁻³⁴ J·s, speed of light c = 3.00 × 10⁸ m/s, 1 eV = 1.60 × 10⁻¹⁹ J (so that hc = 1240 eV·nm), ln 2 = 0.693, and 1 MBq = 10⁶ decays per second.

**Table 1. Activity of the first FDG vial measured in the dose calibrator.**

| Clock time | Minutes after 08:00 | Activity (MBq) |
|---|---|---|
| 08:00 | 0 | 800 |
| 09:50 | 110 | 400 |
| 11:40 | 220 | 200 |
| 13:30 | 330 | 100 |

*Alt text:* Table with four rows. 08:00, 0 minutes after delivery: 800 MBq. 09:50, 110 minutes: 400 MBq. 11:40, 220 minutes: 200 MBq. 13:30, 330 minutes: 100 MBq.

*Source:* Hypothetical scenario written for this app. Fluorine-18 half-life 109.77 min, decay to oxygen-18 by positron emission with a small electron-capture branch (NNDC NuDat as reproduced by the KAERI nuclide table; TUNL Nuclear Data Evaluation, A = 18). Electron rest energy 0.510 998 950 69 MeV and h = 6.626 070 15 × 10⁻³⁴ J·s from NIST CODATA 2022. Positron decay and annihilation from OpenStax College Physics 2e, 31.4 Nuclear Decay and Conservation Laws; half-life and activity from 31.5 Half-Life and Activity; PET (two 0.511 MeV photons moving directly away from one another) from 32.1 Diagnostics and Medical Imaging; hc = 1240 eV·nm from 29.3 Photon Energies and the Electromagnetic Spectrum (2022).

*Status:* reviewed

### CP-016  ·  ★★★★  ·  Skill 2 Reasoning

The afternoon patient's 250 MBq dose was to be drawn from the second vial. The time at which that vial's activity fell below 250 MBq was closest to:

- **A.** 11:05
- **B.** 12:10
- **C.** 13:30
- **D.** 15:20

**Answer: B**

*Worked solution*

- Table 1 confirms the half-life stated in the passage: the first vial halves every 110 min (800 → 400 → 200 → 100 MBq). The second vial, 1200 MBq at 08:00, follows the same steps: 600 MBq at 09:50, 300 MBq at 11:40, 150 MBq at 13:30 and 75 MBq at 15:20.
- 250 MBq lies between 300 MBq (11:40) and 150 MBq (13:30), so the activity crossed 250 MBq between those two times, and 12:10 is the only choice in that interval.
- Estimate of where: 250/300 = 5/6 ≈ 0.83 and (½)^(1/4) ≈ 0.84, so the crossing came about a quarter of a half-life (about 28 min) after 11:40, near 12:08. By 15:20 only 1200/16 = 75 MBq remained, so the planned injection could not be drawn from this vial.

*Why the other choices are wrong*

- **A.** 11:05 is when the first vial (400 MBq at 09:50, 200 MBq at 11:40) passed 250 MBq; the afternoon dose was to come from the second vial, calibrated at 1200 MBq. *(misread graph: the first vial's activities used for the second vial)*
- **C.** 13:30 is the first time in Table 1 at which the second vial's activity (150 MBq) is already below 250 MBq; the activity falls continuously and was still 300 MBq at 11:40, so the crossing came before 13:30. *(misread graph: the first tabulated time below the threshold taken as the crossing)*
- **D.** 15:20 is the planned injection time; the passage reserves the vial for that patient, but by then four half-lives had passed and only 75 MBq remained. *(true but irrelevant: the planned time, not the time the activity crossed 250 MBq)*

*Tags:* chem_phys · general chemistry · FC4 4E · topics: 4E.radioactive-decay

*Takeaway:* Step the activity down by half at each half-life and bracket the target: 1200 MBq is 300 after two half-lives and 150 after three, so it passes 250 MBq a little after the second.

*Sources*

- OpenStax College Physics 2e, 31.5 Half-Life and Activity (2022): activity falls to half its value in each half-life; N = N₀e^(−λt).
- NNDC NuDat (KAERI nuclide table) and TUNL Nuclear Data Evaluation, A = 18: fluorine-18 half-life 109.77 min.

*Status:* reviewed · rev 1

---

### CP-017  ·  ★★★★  ·  Skill 2 Reasoning

The decay constant of fluorine-18, and the fraction of a dose's activity that remains 55 minutes after calibration, are closest to:

- **A.** λ ≈ 9.1 × 10⁻³ min⁻¹; fraction ≈ 0.50
- **B.** λ ≈ 9.1 × 10⁻³ min⁻¹; fraction ≈ 0.71
- **C.** λ ≈ 6.3 × 10⁻³ min⁻¹; fraction ≈ 0.75
- **D.** λ ≈ 6.3 × 10⁻³ min⁻¹; fraction ≈ 0.71

**Answer: D**

*Worked solution*

- λ = ln 2/T½ = 0.693/110 min ≈ 6.3 × 10⁻³ min⁻¹ (about 0.7/110 ≈ 0.0064).
- 55 min is half of one half-life, so the fraction remaining is (½)^(1/2) = 1/√2 ≈ 0.71. Equivalently e^(−λt) = e^(−0.693 × 0.5) = e^(−0.35) ≈ 0.71.
- Shortcut: 2^(−0.5) = 1/1.414 = 0.707. Decay is exponential, so half of a half-life leaves about 71%, not 75%.

*Why the other choices are wrong*

- **A.** 9.1 × 10⁻³ min⁻¹ is 1/T½ without the factor ln 2, and a fraction of 0.50 would require a full half-life (110 min), not 55 min. *(wrong formula: ln 2 omitted and 55 min treated as one half-life)*
- **B.** The fraction is right, but 9.1 × 10⁻³ min⁻¹ is 1/T½ without the factor ln 2; λ = ln 2/T½, not 1/T½. *(wrong formula: ln 2 omitted from λ = ln 2/T½)*
- **C.** The decay constant is right, but 0.75 treats decay as linear (half of the loss over half the time); exponential decay leaves 71% after half a half-life. *(wrong formula: linear interpolation of an exponential)*

*Tags:* chem_phys · physics · FC4 4E · topics: 4E.radioactive-decay

*Takeaway:* λ = 0.693/T½, and the fraction left after time t is (½)^(t/T½); half a half-life leaves 1/√2 ≈ 71%.

*Sources*

- OpenStax College Physics 2e, 31.5 Half-Life and Activity (2022): λ = ln 2/t½ ≈ 0.693/t½; N = N₀e^(−λt).

*Status:* reviewed · rev 1

---

### CP-018  ·  ★★★  ·  Skill 1 Knowledge

Which statement correctly describes the nuclear change in the decay of fluorine-18 and the origin of the photons the scanner detects?

- **A.** Fluorine-18 becomes neon-18 (Z rises by one, A unchanged); the emitted particle is a photon of 511 keV.
- **B.** Fluorine-18 becomes oxygen-17 (Z and A both fall by one); the positron is detected directly by the ring.
- **C.** Fluorine-18 becomes oxygen-18 (Z falls by one, A unchanged); the positron annihilates with an electron, producing two photons that move in opposite directions.
- **D.** Fluorine-18 becomes oxygen-18 (Z falls by one, A unchanged); the excited oxygen-18 nucleus then emits two gamma rays in opposite directions.

**Answer: C**

*Worked solution*

- In positron (β⁺) emission a proton in the nucleus becomes a neutron, emitting a positron and a neutrino: Z falls by one and A is unchanged. ¹⁸₉F → ¹⁸₈O + e⁺ + ν. Both mass number (18 = 18 + 0) and charge (9 = 8 + 1) are conserved.
- The positron is antimatter; after slowing in tissue it meets an electron and the pair annihilates, converting their rest mass (2 × 511 keV) into two photons. Momentum conservation requires the photons to leave in opposite directions, and energy conservation gives each one 511 keV. The scanner exploits this: two detectors on opposite sides must fire at the same moment.
- Z determines the element, so lowering Z by one turns fluorine (9) into oxygen (8); the daughter oxygen-18 is stable.

*Why the other choices are wrong*

- **A.** Z rising by one is beta-minus decay (a neutron becoming a proton, emitting an electron); positron emission lowers Z, and the detected photons come from annihilation, not from the decay itself. *(reversed relationship: β⁻ change in Z applied to β⁺ decay)*
- **B.** Positron emission does not change A (a proton becomes a neutron, so the nucleon count is constant); and the positron travels only about a millimetre before annihilating, so it never reaches the detectors. *(wrong formula: A changed in a decay that conserves nucleon number)*
- **D.** The photons come from electron–positron annihilation outside the nucleus, not from a nuclear transition; fluorine-18 decays to the ground state of oxygen-18. *(wrong formula: annihilation photons attributed to gamma decay)*

*Tags:* chem_phys · physics · FC4 4E · topics: 4E.nucleus-isotopes, 4E.radioactive-decay

*Takeaway:* Positron emission lowers Z by one with A unchanged; the positron then annihilates with an electron to give two 511 keV photons travelling in opposite directions.

*Sources*

- OpenStax College Physics 2e, 31.4 Nuclear Decay and Conservation Laws (2022): β⁺ decay, daughter has Z − 1 and the same A; annihilation converts the pair's mass into photons moving in opposite directions.
- OpenStax College Physics 2e, 32.1 Diagnostics and Medical Imaging (2022): PET detects two 0.511 MeV photons that move directly away from one another.
- TUNL Nuclear Data Evaluation, A = 18: fluorine-18 positron decay is entirely to the ground state of oxygen-18.

*Status:* reviewed · rev 1

---

### CP-019  ·  ★★  ·  Skill 2 Reasoning

The wavelength of each annihilation photon, and the region of the electromagnetic spectrum in which it lies, are:

- **A.** 2.4 × 10⁻¹² m, gamma rays
- **B.** 4.9 × 10⁻¹² m, gamma rays
- **C.** 2.4 × 10⁻⁹ m, X-rays
- **D.** 5.1 × 10⁻⁷ m, visible light

**Answer: A**

*Worked solution*

- Each photon carries 511 keV, the rest energy of one electron (passage). E = hf = hc/λ, so λ = hc/E.
- With hc = 1240 eV·nm: λ = 1240 eV·nm / 511 000 eV = 2.43 × 10⁻³ nm = 2.4 × 10⁻¹² m (2.4 pm). The same result follows from λ = (6.63 × 10⁻³⁴ × 3.00 × 10⁸)/(511 × 10³ × 1.60 × 10⁻¹⁹) = 1.99 × 10⁻²⁵/8.18 × 10⁻¹⁴ ≈ 2.4 × 10⁻¹² m.
- Picometre wavelengths and MeV-scale energies are the gamma-ray end of the spectrum; the hardest X-rays overlap this region, and the two are distinguished by origin (nuclear or annihilation photons are called gamma rays).

*Why the other choices are wrong*

- **B.** 4.9 × 10⁻¹² m corresponds to 255 keV, as if the 511 keV were shared between the two photons; each photon carries the full rest energy of one particle. *(wrong formula: the energy halved between the photons)*
- **C.** 2.4 × 10⁻⁹ m comes from 1240/511 with the energy read as 511 eV instead of 511 keV; the factor of 1000 moves the answer from gamma rays to soft X-rays. *(sign or unit error: keV read as eV)*
- **D.** 5.1 × 10⁻⁷ m (510 nm, green light) treats the number 511 as a wavelength in nanometres; visible photons carry only 2–3 eV, a hundred-thousandth of the energy here. *(sign or unit error: an energy treated as a wavelength)*

*Tags:* chem_phys · physics · FC4 4D · topics: 4D.em-radiation

*Takeaway:* λ = hc/E with hc = 1240 eV·nm; a 511 keV photon has λ ≈ 2.4 pm, in the gamma-ray region.

*Sources*

- OpenStax College Physics 2e, 29.3 Photon Energies and the Electromagnetic Spectrum (2022): E = hf = hc/λ with hc = 1240 eV·nm; gamma rays have the highest photon energies.
- OpenStax College Physics 2e, 24.3 The Electromagnetic Spectrum (2022): gamma rays and X-rays overlap in frequency and differ by source.
- NIST CODATA 2022: electron mass energy equivalent 0.510 998 950 69 MeV; h = 6.626 070 15 × 10⁻³⁴ J·s.

*Status:* reviewed · rev 1

---

## Standalone questions

### CP-020  ·  ★★  ·  Skill 1 Knowledge

A student derives an expression for the pressure inside an alveolus and checks it by dimensional analysis. In SI base units, a pressure is expressed as:

- **A.** kg·m⁻³
- **B.** kg·m⁻¹·s⁻²
- **C.** kg·m·s⁻²
- **D.** kg·m²·s⁻²

**Answer: B**

*Worked solution*

- Pressure is force per unit area: 1 Pa = 1 N/m². Force is mass times acceleration, so 1 N = 1 kg·m·s⁻².
- Dividing by m²: 1 Pa = kg·m·s⁻² / m² = kg·m⁻¹·s⁻².
- Check with another route: pressure is also energy per unit volume (the terms of Bernoulli's equation), J/m³ = kg·m²·s⁻²/m³ = kg·m⁻¹·s⁻², the same combination.

*Why the other choices are wrong*

- **A.** kg·m⁻³ is a density (mass per volume). *(wrong formula: density instead of pressure)*
- **C.** kg·m·s⁻² is the newton, a force; pressure is force divided by area. *(wrong formula: force not divided by area)*
- **D.** kg·m²·s⁻² is the joule, an energy; pressure is energy per unit volume, so it has m⁻¹, not m². *(wrong formula: energy not divided by volume)*

*Tags:* chem_phys · physics · FC4 4A · topics: 4A.units-vectors

*Takeaway:* Pa = N/m² = kg·m⁻¹·s⁻²; the same units as energy per unit volume, which is why every term in Bernoulli's equation is a pressure.

*Sources*

- NIST Special Publication 811, Guide for the Use of the International System of Units, Table 3 (2008): newton N = m·kg·s⁻²; pascal Pa = N/m² = m⁻¹·kg·s⁻².
- OpenStax College Physics 2e, 1.2 Physical Quantities and Units (2022): SI base units and derived units.

*Status:* reviewed · rev 1

---

### CP-021  ·  ★★  ·  Skill 1 Knowledge

Povidone-iodine antiseptic releases iodine. Which statement about iodine (I, atomic number 53, group 17) is correct?

- **A.** It has one valence electron and forms I⁺ ions, like the alkali metals of group 1.
- **B.** It has seven valence electrons and typically forms I⁺ ions by losing one.
- **C.** It is a metalloid, and as an element it exists as single atoms rather than molecules.
- **D.** It has seven valence electrons and typically gains one to form I⁻, isoelectronic with xenon.

**Answer: D**

*Worked solution*

- Elements in the same group share a valence configuration. Group 17, the halogens (F, Cl, Br, I), have ns²np⁵: seven valence electrons, one short of the noble-gas octet.
- A halogen reaches the octet most easily by gaining one electron, forming a −1 halide ion; I⁻ is isoelectronic with xenon (Z = 54), the noble gas that follows iodine. As elements the halogens are diatomic (I₂), each atom sharing one electron pair to complete its octet.
- The halogens are reactive nonmetals; their chemistry with metals is ionic (NaI, KI) and with nonmetals covalent.

*Why the other choices are wrong*

- **A.** One valence electron and +1 ions describe group 1 (the alkali metals); iodine is in group 17. *(reversed relationship: group 1 behaviour assigned to group 17)*
- **B.** Seven valence electrons is right, but a halogen gains an electron to complete its octet rather than losing one; I⁺ is not the typical ion. *(reversed relationship: electron loss instead of gain)*
- **C.** Iodine is a nonmetal (the metalloids are B, Si, Ge, As, Sb and Te), and like the other halogens it exists as diatomic I₂ molecules, each atom completing its octet by sharing one electron pair. *(wrong formula: wrong class of element and wrong elemental form)*

*Tags:* chem_phys · general chemistry · FC4 4E · topics: 4E.periodic-groups

*Takeaway:* Halogens (group 17) have seven valence electrons, exist as diatomic molecules and form −1 ions isoelectronic with the next noble gas.

*Sources*

- OpenStax Chemistry 2e, 2.5 The Periodic Table (2019): the halogens are group 17; fluorine, chlorine, bromine and iodine are nonmetals with similar properties.
- OpenStax Chemistry 2e, 18.11 Occurrence, Preparation, and Properties of Halogens (2019): halogens form −1 halide ions and diatomic molecules.

*Status:* reviewed · rev 1

---

### CP-022  ·  ★★★  ·  Skill 1 Knowledge

In one resonance structure of the nitrate ion, NO₃⁻, nitrogen is bonded to one oxygen by a double bond and to the other two by single bonds, and every atom has an octet. The formal charges on nitrogen, the double-bonded oxygen and each single-bonded oxygen are, respectively:

- **A.** 0, 0 and −1
- **B.** +1, −1 and 0
- **C.** +1, 0 and −1
- **D.** 0, −⅓ and −⅓

**Answer: C**

*Worked solution*

- Formal charge = valence electrons − nonbonding electrons − ½(bonding electrons).
- Nitrogen (5 valence electrons) has four bonds (8 bonding electrons) and no lone pair: 5 − 0 − 4 = +1. The double-bonded oxygen (6 valence) has two lone pairs (4 electrons) and two bonds (4 electrons): 6 − 4 − 2 = 0. Each single-bonded oxygen has three lone pairs (6 electrons) and one bond (2 electrons): 6 − 6 − 1 = −1.
- Check: the formal charges sum to +1 + 0 − 1 − 1 = −1, the charge of the ion. The three equivalent resonance structures differ only in which oxygen is double-bonded.

*Why the other choices are wrong*

- **A.** A nitrogen with four bonds and no lone pair carries +1; with 0 on nitrogen the charges would sum to −2, not the ion's −1. *(wrong formula: nitrogen's bonding electrons miscounted)*
- **B.** The signs are assigned to the wrong oxygens: the oxygen with two bonds and two lone pairs is neutral, and each oxygen with one bond and three lone pairs is −1. *(reversed relationship: charges swapped between the two oxygen types)*
- **D.** A charge of −⅓ on each oxygen describes the resonance hybrid, the average over the three structures; the question asks about one resonance structure, in which charges are whole numbers. *(true but irrelevant: the hybrid's average charge, not a single structure's)*

*Tags:* chem_phys · general chemistry · FC5 5B · topics: 5B.lewis-structures

*Takeaway:* Formal charge = V − N − B/2; in each nitrate resonance structure N is +1, the double-bonded O is 0 and the single-bonded oxygens are −1, summing to −1.

*Sources*

- OpenStax Chemistry 2e, 7.4 Formal Charges and Resonance (2019): formal charge = valence electrons − nonbonding electrons − ½ bonding electrons; the nitrate ion's three resonance forms.

*Status:* reviewed · rev 1

---

### CP-023  ·  ★★  ·  Skill 1 Knowledge

A patient takes a nonsteroidal anti-inflammatory drug that inhibits cyclooxygenase. Synthesis of which lipid is reduced as a direct result?

- **A.** Triacylglycerol, the storage lipid of adipose tissue
- **B.** Phosphatidylcholine, a glycerophospholipid of the membrane bilayer
- **C.** Prostaglandin E₂, a C₂₀ eicosanoid that acts as a local signal in inflammation
- **D.** Cholesterol, the sterol that moderates membrane fluidity

**Answer: C**

*Worked solution*

- Prostaglandins are 20-carbon lipids built from arachidonic acid, a polyunsaturated fatty acid released from membrane phospholipids. The committed step, conversion of arachidonic acid to the cyclic endoperoxide PGH₂, is catalysed by cyclooxygenase (COX), and PGH₂ is then converted to prostaglandins such as PGE₂ and to thromboxanes.
- Prostaglandins act locally, near where they are made, on inflammation, pain, fever, platelet aggregation, gastric secretion and smooth muscle. Inhibiting COX therefore lowers prostaglandin synthesis, which is how NSAIDs reduce inflammation and pain.
- Of the four choices only the prostaglandin is a signalling lipid; the others are storage, structural and membrane components made by unrelated pathways.

*Why the other choices are wrong*

- **A.** Triacylglycerols are esters of glycerol with three fatty acids, made for energy storage by acyltransferases; COX is not involved. *(out of scope: a storage lipid made by a different pathway)*
- **B.** Phosphatidylcholine is a structural membrane lipid; its synthesis does not use cyclooxygenase (though membrane phospholipids are the source of the arachidonic acid that COX acts on). *(true but irrelevant: the phospholipid supplies the precursor but is not the COX product)*
- **D.** Cholesterol is made from acetyl-CoA through the mevalonate pathway (the target of statins, not NSAIDs). *(out of scope: a different pathway and drug class)*

*Tags:* chem_phys · biochemistry · FC5 5D · topics: 5D.lipids

*Takeaway:* Prostaglandins are local-acting eicosanoid signals made from arachidonic acid by cyclooxygenase; NSAIDs act by blocking that enzyme.

*Sources*

- OpenStax Organic Chemistry, 27.4 Prostaglandins and Other Eicosanoids (2023): eicosanoid biosynthesis begins with conversion of arachidonic acid to PGH₂ by cyclooxygenase (COX); prostaglandins affect blood pressure, platelet aggregation, gastric secretion and inflammation.
- OpenStax Organic Chemistry, Chapter 15 Chemistry Matters: Aspirin, NSAIDs, and COX-2 Inhibitors (2023): NSAIDs act by inhibiting cyclooxygenase.
- OpenStax Biology 2e, 3.3 Lipids (2018): triacylglycerols, phospholipids and steroids.

*Status:* reviewed · rev 1

---

### CP-024  ·  ★★★  ·  Skill 2 Reasoning

The initial rate of the reaction A + B → products was measured in three trials. Trial 1: [A] = 0.10 M, [B] = 0.10 M, rate = 2.0 × 10⁻⁴ M/s. Trial 2: [A] = 0.20 M, [B] = 0.10 M, rate = 8.0 × 10⁻⁴ M/s. Trial 3: [A] = 0.20 M, [B] = 0.20 M, rate = 1.6 × 10⁻³ M/s. The rate law is:

- **A.** rate = k[A][B]
- **B.** rate = k[A]²[B]
- **C.** rate = k[A][B]²
- **D.** rate = k[A]²[B]²

**Answer: B**

*Worked solution*

- Compare trials in which only one concentration changes. Trials 1 and 2: [A] doubles at fixed [B] and the rate rises from 2.0 × 10⁻⁴ to 8.0 × 10⁻⁴, a factor of 4 = 2²; the reaction is second order in A.
- Trials 2 and 3: [B] doubles at fixed [A] and the rate rises from 8.0 × 10⁻⁴ to 1.6 × 10⁻³, a factor of 2 = 2¹; first order in B.
- So rate = k[A]²[B], overall third order. Check k from trial 1: k = 2.0 × 10⁻⁴/(0.10² × 0.10) = 2.0 × 10⁻⁴/1.0 × 10⁻³ = 0.20 M⁻²·s⁻¹; trial 3 then predicts 0.20 × 0.04 × 0.20 = 1.6 × 10⁻³ M/s, as measured. The orders are not the coefficients in the balanced equation; they come only from experiment.

*Why the other choices are wrong*

- **A.** First order in A would make the rate double, not quadruple, when [A] doubles between trials 1 and 2. *(wrong formula: orders read from the balanced equation)*
- **C.** The orders are swapped: it is [A] whose doubling quadruples the rate and [B] whose doubling merely doubles it. *(reversed relationship: the two orders interchanged)*
- **D.** Second order in B would quadruple the rate between trials 2 and 3; it only doubled. *(misread graph: the factor between trials 2 and 3 taken as 4)*

*Tags:* chem_phys · general chemistry · FC5 5E · topics: 5E.rate-laws

*Takeaway:* Find each order by doubling one concentration at a time: a doubled rate means first order, a quadrupled rate second order.

*Sources*

- OpenStax Chemistry 2e, 12.3 Rate Laws (2019): the method of initial rates; rate laws are determined by experiment and not predicted by stoichiometry.

*Status:* reviewed · rev 1

---

### CP-025  ·  ★★  ·  Skill 1 Knowledge

A peptide hormone contains the residues valine, serine, aspartate and lysine. Which statement correctly classifies one of these side chains at pH 7.4?

- **A.** Aspartate: basic, carrying a positive charge on its side chain
- **B.** Lysine: acidic, carrying a negative charge on its side chain
- **C.** Serine: nonpolar and hydrophobic, with no hydrogen-bonding group
- **D.** Valine: nonpolar and hydrophobic, with a branched hydrocarbon side chain

**Answer: D**

*Worked solution*

- Valine's side chain is an isopropyl group, pure hydrocarbon: it cannot hydrogen-bond or ionise, so it is nonpolar and hydrophobic, and such residues tend to be buried in a protein's core. Like the other natural amino acids it has the L configuration (S by the sequence rules).
- The other three residues are hydrophilic. Serine has a hydroxyl (polar, uncharged). Aspartate's side chain is a carboxylic acid with pKa about 4, so at pH 7.4 it is deprotonated, a carboxylate anion: acidic, negatively charged. Lysine's side chain is a primary amine with pKa about 10.5, protonated at pH 7.4: basic, positively charged.
- Rule of thumb: a side-chain group is in its charged form when the pH is more than about two units from its pKa on the appropriate side.

*Why the other choices are wrong*

- **A.** Aspartate is acidic; at pH 7.4 its side-chain carboxyl has lost its proton and carries a negative charge. *(reversed relationship: an acidic residue called basic)*
- **B.** Lysine is basic; its side-chain amine is protonated and positive at pH 7.4. *(reversed relationship: a basic residue called acidic)*
- **C.** Serine's hydroxyl group is polar and hydrogen-bonds with water; serine is classified as polar, uncharged. *(wrong formula: a polar hydroxyl side chain classed as nonpolar)*

*Tags:* chem_phys · biochemistry · FC5 5D · topics: 5D.amino-acids

*Takeaway:* At pH 7.4, Asp and Glu are negative (acidic), Lys and Arg positive (basic), Ser and Thr polar but uncharged, and Val, Leu and Ile nonpolar and hydrophobic.

*Sources*

- OpenStax Biology 2e, 3.4 Proteins (2018): valine is nonpolar aliphatic; serine polar uncharged; lysine positively charged; aspartate negatively charged.
- OpenStax Organic Chemistry, 26.1 Structures of Amino Acids (2023): side-chain pKa values (aspartic acid about 3.65, lysine about 10.53) and the L (S) configuration of natural amino acids.

*Status:* reviewed · rev 1

---
