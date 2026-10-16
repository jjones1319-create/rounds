"""Independent numeric and structural checks for Chem/Phys batch 3 (CP-051 to CP-075).

Every number quoted in content/mcat/chem_phys/batch_03.json is re-derived here from the passage constants, separately
from the explanations, and compared with the value the item or figure uses. Structures, formulas and residue masses are
checked with RDKit. Run:  py review/chem_phys_batch_03_check.py     (exit 1 on any mismatch)
"""
import json
import math
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
fails = []
BATCH = json.load(open("content/mcat/chem_phys/batch_03.json", encoding="utf-8"))


def check(name, got, want, tol=0.02):
    ok = abs(got - want) <= tol * max(abs(want), 1e-12)
    print(f"{'ok  ' if ok else 'FAIL'} {name}: computed {got:.6g}, item uses {want:.6g}")
    if not ok:
        fails.append(name)


def figure(pid, fid):
    return [f for p in BATCH["passages"] if p["id"] == pid for f in p["figures"] if f["id"] == fid][0]


def same(name, got, want):
    ok = got == want
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {got!r} {'==' if ok else '!='} {want!r}")
    if not ok:
        fails.append(name)


def num(s):
    return float(str(s).replace(",", "").replace("−", "-").replace("+", ""))


# ---------- constants (NIST CODATA 2022, NIST SRM 39j, NIST WebBook) ----------
e = 1.602176634e-19          # C
u = 1.66053906892e-27        # kg
F = 96485.33212              # C/mol
k_coulomb = 8.9875517923e9   # N m^2 / C^2
BA_kJ_per_g = 26.434         # benzoic acid, SRM 39j: 26 434 J/g
dcH_glucose, dcH_lactic = -2805.0, -1362.8   # kJ/mol, NIST WebBook (alpha-D-glucose solid; DL-lactic acid solid)

# ---------- CP-P09 bomb calorimetry ----------
P_heater, t_on, t_off = 110.0, 60.0, 360.0           # W, s, s (passage)
pts = figure("CP-P09", "fig1")["data"]["series"][0]["points"]
T = dict(pts)
dT_elec = T[480] - T[0]
C_elec = P_heater * (t_off - t_on) / dT_elec           # J/K
check("P09 electrical calibration C (kJ/K)", C_elec / 1000, 11.0, 0.001)
# the curve must be flat before and after heating and linear while the heater runs
same("P09 flat before heating", T[0] == T[60] == 25.0, True)
same("P09 flat after heating", T[360] == T[420] == T[480], True)
slope = (T[360] - T[60]) / (t_off - t_on)
check("P09 heating slope = P/C (K/s)", P_heater / C_elec, slope, 0.001)
for t in (120, 180, 240, 300):
    check(f"P09 curve point at t={t} s is linear (°C)", T[60] + slope * (t - 60), T[t], 0.0005)
rows = figure("CP-P09", "tab1")["data"]["rows"]
m_ba, dT_ba = num(rows[0][2]), num(rows[0][3])
m_bar, dT_bar = num(rows[1][2]), num(rows[1][3])
C_chem = BA_kJ_per_g * m_ba / dT_ba                    # kJ/K
check("P09 benzoic acid calibration C (kJ/K) agrees with electrical", C_chem, C_elec / 1000, 0.002)
q_bar = C_chem * dT_bar / m_bar
check("CP-051 bar gross energy from SRM value (kJ/g)", q_bar, 22.0, 0.002)
check("CP-051 bar gross energy from the passage's rounded 26.4 (kJ/g)", 26.4 * dT_bar / dT_ba, 22.0, 1e-9)
check("CP-051 distractor A heat capacity (kJ/K)", 26.4 / dT_ba, 11.0, 1e-9)
check("CP-051 distractor C inverted ratio (kJ/g)", 26.4 * dT_ba / dT_bar, 31.7, 0.002)
check("CP-051 distractor D 26.4 x ΔT (kJ/g)", 26.4 * dT_bar, 52.8, 1e-9)
check("CP-051 bar per 50 g (kJ)", 22.0 * 50, 1100, 1e-9)
check("CP-051 kcal per bar", 1100 / 4.184, 263, 0.005)
# CP-055 distractors
check("CP-055 distractor A P/ΔT (kJ/K)", P_heater / dT_elec / 1000, 0.037, 0.01)
check("CP-055 distractor B energy over final temperature in kelvin (kJ/K)", P_heater * (t_off - t_on) / 1000 / (T[480] + 273.15), 0.11, 0.01)
check("CP-055 distractor C energy over final temperature in °C (kJ/K)", P_heater * (t_off - t_on) / 1000 / T[480], 1.2, 0.02)
check("CP-055 energy delivered (kJ)", P_heater * (t_off - t_on) / 1000, 33.0, 1e-9)
# Table 2 Atwater sum and the bomb comparison
rows2 = figure("CP-P09", "tab2")["data"]["rows"]
atwater = sum(num(r[1]) * num(r[2]) for r in rows2)
check("P09 Atwater energy per bar (kJ)", atwater, 971, 1e-9)
same("P09 bar mass sums to 50 g", sum(num(r[1]) for r in rows2), 50.0)
same("P09 bomb (1100 kJ) exceeds Atwater (971 kJ), as the passage says", 1100 > atwater, True)
# gross-energy plausibility: component heats of combustion (Merrill & Watt: protein 5.65 kcal/g, fat 9.3-9.5, carbohydrate 3.7-4.2)
gross_est = 25 * 17.2 + 5 * 17.5 + 10 * 39.3 + 8 * 23.6
check("P09 gross energy estimated from components is about the bomb value (kJ)", gross_est, 1100, 0.03)
check("P09 protein 5.65 kcal/g in kJ/g", 5.65 * 4.184, 23.6, 0.002)
check("P09 Atwater protein 4 kcal/g in kJ/g", 4.0 * 4.184, 17, 0.02)
# CP-052 Hess
check("CP-052 ΔH glucose -> 2 lactic acid, passage values (kJ/mol)", -2800 - 2 * (-1360), -80, 1e-9)
check("CP-052 same with NIST values (kJ/mol)", dcH_glucose - 2 * dcH_lactic, -79.4, 0.001)
check("CP-052 distractor A sum (kJ/mol)", -2800 + (-1360), -4160, 1e-9)
check("CP-052 distractor B coefficient dropped (kJ/mol)", -2800 - (-1360), -1440, 1e-9)
check("CP-052 fraction of glucose energy released anaerobically", 80 / 2800, 0.03, 0.05)
# CP-053: constant-volume PV correction is small for foods: palmitic acid C16H32O2 + 23 O2 -> 16 CO2 + 16 H2O(l), Δn_gas = -7
check("CP-053 Δ(PV) for fat combustion relative to its energy (%)", 7 * 8.314 * 298.15 / 1000 / 9978 * 100, 0.17, 0.05)
same("CP-053 that correction is 'well under 1%'", 7 * 8.314 * 298.15 / 1000 / 9978 < 0.01, True)

# ---------- CP-P10 mass spectrometry ----------
V, L = 20000.0, 2.0
def tof(mz, z=1):
    v = math.sqrt(2 * z * e * V / (mz * u))
    return L / v
check("P10 flight time of m/z 900 at 20 kV over 2.0 m (µs)", tof(900) * 1e6, 30.5, 0.002)
check("CP-057 flight time of m/z 1626 (µs)", tof(1626) * 1e6, 41.0, 0.002)
check("CP-057 scaling 30.5 x sqrt(1626/900) (µs)", 30.5 * math.sqrt(1626 / 900), 41.0, 0.002)
check("CP-057 mental math 30.5 x 4/3 (µs)", 30.5 * 4 / 3, 40.7, 0.002)
check("CP-057 distractor A ∝ 1/m (µs)", 30.5 * 900 / 1626, 17, 0.02)
check("CP-057 distractor B ∝ 1/√m (µs)", 30.5 * math.sqrt(900 / 1626), 23, 0.02)
check("CP-057 distractor D ∝ m (µs)", 30.5 * 1626 / 900, 55, 0.02)
check("CP-057 speed of m/z 900 (m/s)", math.sqrt(2 * e * V / (900 * u)), 6.5e4, 0.01)
check("CP-060 carbons from 44% M+1 at 1.1%", 0.44 / 0.011, 40, 1e-9)
check("CP-060 distractor A (percentages converted inconsistently)", 0.44 / 1.1, 0.4, 1e-9)
check("CP-060 distractor B (abundance as 11%)", 0.44 / 0.11, 4, 1e-9)
same("CP-060 1.1% lies in the CIAAW interval 0.0096-0.0116", 0.0096 <= 0.011 <= 0.0116, True)
spec = {lab.split()[0]: v for lab, v in figure("CP-P10", "fig1")["data"]["series"][0]["points"]}
check("P10 Figure 1 M+1 of T2 is 44% of M", spec["862.4"] / spec["861.4"] * 100, 44, 1e-9)
# M+2 plausibility for ~40 carbons: C(40,2) * 0.011^2 ≈ 9.4%, plus 18O; the chart shows 10%
check("P10 M+2 from two 13C in 40 carbons (%)", math.comb(40, 2) * 0.011 ** 2 * 100, spec["863.4"], 0.1)

# ---------- RDKit: residue masses, peptide masses, the y-ion ladder, formulas ----------
try:
    from rdkit import Chem, RDLogger
    from rdkit.Chem import Descriptors, rdMolDescriptors
    RDLogger.DisableLog("rdApp.*")

    def mol(smi):
        m = Chem.MolFromSmiles(smi)
        assert m is not None, smi
        return m

    def exact(smi):
        return Descriptors.ExactMolWt(mol(smi))

    def formula(smi):
        return rdMolDescriptors.CalcMolFormula(mol(smi))

    AA = {"Gly": "NCC(=O)O", "Ala": "N[C@@H](C)C(=O)O", "Ser": "N[C@@H](CO)C(=O)O", "Pro": "OC(=O)[C@@H]1CCCN1",
          "Val": "N[C@@H](C(C)C)C(=O)O", "Thr": "N[C@@H]([C@@H](C)O)C(=O)O", "Cys": "N[C@@H](CS)C(=O)O",
          "Leu": "N[C@@H](CC(C)C)C(=O)O", "Ile": "N[C@@H]([C@@H](C)CC)C(=O)O", "Asn": "N[C@@H](CC(N)=O)C(=O)O",
          "Asp": "N[C@@H](CC(=O)O)C(=O)O", "Gln": "N[C@@H](CCC(N)=O)C(=O)O", "Lys": "N[C@@H](CCCCN)C(=O)O",
          "Glu": "N[C@@H](CCC(=O)O)C(=O)O", "Met": "N[C@@H](CCSC)C(=O)O", "His": "N[C@@H](Cc1c[nH]cn1)C(=O)O",
          "Phe": "N[C@@H](Cc1ccccc1)C(=O)O", "Arg": "N[C@@H](CCCNC(N)=N)C(=O)O", "Tyr": "N[C@@H](Cc1ccc(O)cc1)C(=O)O",
          "Trp": "N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O"}
    H2O = exact("O")
    Hp = 1.00727646688                     # proton mass (Da)
    HPO3 = exact("OP(=O)(O)O") - H2O       # phosphoric acid minus water
    RES = {k: exact(s) - H2O for k, s in AA.items()}
    check("RDKit water (Da)", H2O, 18.01, 0.001)
    check("RDKit HPO3 (Da) vs Unimod 79.966331", HPO3, 79.966331, 1e-6)
    # Table 1 residue masses
    tab1 = figure("CP-P10", "tab1")["data"]["rows"]
    table = {}
    for r in tab1:
        for name, mass in ((r[0], r[1]), (r[2], r[3])):
            table[name] = num(mass)
    for name, mass in table.items():
        if name == "Leu/Ile":
            check("RDKit residue Leu (Da)", RES["Leu"], mass, 0.0001)
            same("RDKit Leu and Ile are isobaric", round(RES["Leu"], 5) == round(RES["Ile"], 5), True)
        elif name.startswith("H₂O"):
            check("RDKit termini water (Da)", H2O, mass, 0.001)
        else:
            check(f"RDKit residue {name} (Da)", RES[name], mass, 0.0001)
    same("P10 Table 1 lists 19 residue masses + water", len(table), 20)
    # UW Proteomics Resource / Unimod reference values
    for name, ref in (("Gly", 57.021464), ("Ser", 87.032028), ("Tyr", 163.063329), ("Thr", 101.047679), ("Leu", 113.084064), ("Gln", 128.058578)):
        check(f"RDKit {name} vs UWPR table", RES[name], ref, 1e-6)
    # T3 = AYSLQDVFK
    seq = ["Ala", "Tyr", "Ser", "Leu", "Gln", "Asp", "Val", "Phe", "Lys"]
    M = sum(RES[r] for r in seq) + H2O
    check("P10 T3 predicted [M+H]+ (Da)", M + Hp, 1070.55, 0.00001)
    check("P10 T3 observed phosphorylated [M+H]+ (Da)", M + Hp + HPO3, 1150.52, 0.00001)
    check("P10 difference observed - predicted (Da)", (M + Hp + HPO3) - (M + Hp), 79.97, 0.0001)
    same("P10 trypsin site: T3 ends in Lys", seq[-1] in ("Lys", "Arg"), True)
    same("P10 chymotrypsin sites in T3: after Tyr-2 and Phe-8", [i + 1 for i, r in enumerate(seq) if r in ("Phe", "Tyr", "Trp")], [2, 8])
    # y ions with phosphoserine at position 3 (index 2)
    def y_ion(n):
        tail = seq[-n:]
        mass = sum(RES[r] for r in tail) + H2O + Hp
        if len(seq) - n <= 2:          # residue 3 (index 2) is inside the fragment
            mass += HPO3
        return mass
    tab2 = {r[0]: num(r[2]) for r in figure("CP-P10", "tab2")["data"]["rows"]}
    for name, val in tab2.items():
        n = int(name[1:])
        check(f"P10 Table 2 {name} (m/z)", y_ion(n), val, 0.0001)
    same("P10 Table 2 residue ranges", [r[1] for r in figure("CP-P10", "tab2")["data"]["rows"]], ["2–9", "3–9", "4–9", "5–9", "6–9"])
    d87 = tab2["y8"] - tab2["y7"]; d76 = tab2["y7"] - tab2["y6"]; d65 = tab2["y6"] - tab2["y5"]; d54 = tab2["y5"] - tab2["y4"]
    check("CP-059 y8-y7 = Tyr (Da)", d87, RES["Tyr"], 0.0005)
    check("CP-059 y7-y6 = 167.0 (Da)", d76, 167.0, 0.0005)
    check("CP-059 167.0 - 80.0 = Ser (Da)", d76 - 80.0, RES["Ser"], 0.001)
    check("CP-059 y7-y6 = Ser + HPO3 (Da)", RES["Ser"] + HPO3, d76, 0.0005)
    check("CP-059 y6-y5 = Leu (Da)", d65, RES["Leu"], 0.0005)
    check("CP-059 y5-y4 = Gln (Da)", d54, RES["Gln"], 0.0005)
    same("CP-059 no unmodified residue within 0.5 Da of 167.0", any(abs(m - 167.0) < 0.5 for m in RES.values()), False)
    check("CP-059 distractor A unmodified Ser step would be (Da)", RES["Ser"], 87.0, 0.0005)
    same("CP-059 Tyr-2 is unmodified: y8-y7 within 0.1 of Tyr", abs(d87 - RES["Tyr"]) < 0.1, True)
    check("CP-059 distractor C phosphothreonine (Da)", RES["Thr"] + HPO3, 181.0, 0.0005)
    check("CP-059 distractor D phosphotyrosine (Da)", RES["Tyr"] + HPO3, 243.0, 0.0005)
    # CP-060: a 9-residue peptide like T3 has 50 carbons; T2 at m/z 861 would have roughly 38-40
    same("P10 T3 carbon count (for scale)", formula("CC(C(=O)NC(Cc1ccc(O)cc1)C(=O)NC(CO)C(=O)NC(CC(C)C)C(=O)NC(CCC(N)=O)C(=O)NC(CC(=O)O)C(=O)NC(C(C)C)C(=O)NC(Cc1ccccc1)C(=O)NC(CCCCN)C(=O)O)N").startswith("C50"), True)
    # CP-068 / CP-P12: glucose oxidation at C1 to the lactone keeps C6, loses 2 H
    same("RDKit beta-D-glucose formula", formula("OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O"), "C6H12O6")
    same("RDKit D-glucono-1,5-lactone formula", formula("OC[C@H]1OC(=O)[C@H](O)[C@@H](O)[C@@H]1O"), "C6H10O6")
    glc = mol("OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O")
    c1 = [a for a in glc.GetAtoms() if a.GetSymbol() == "C" and sum(1 for n in a.GetNeighbors() if n.GetSymbol() == "O") == 2][0]
    same("RDKit glucose C1 (hemiacetal) carries one H", c1.GetTotalNumHs(), 1)
    lac = mol("OC[C@H]1OC(=O)[C@H](O)[C@@H](O)[C@@H]1O")
    c1l = [a for a in lac.GetAtoms() if a.GetSymbol() == "C" and sum(1 for n in a.GetNeighbors() if n.GetSymbol() == "O") == 2][0]
    same("RDKit lactone C1 carries no H (oxidized)", c1l.GetTotalNumHs(), 0)
    same("RDKit hydrogen peroxide formula", formula("OO"), "H2O2")
    same("RDKit ferricyanide formula and charge", (formula("[Fe+3].[C-]#N.[C-]#N.[C-]#N.[C-]#N.[C-]#N.[C-]#N"), Chem.GetFormalCharge(mol("[Fe+3].[C-]#N.[C-]#N.[C-]#N.[C-]#N.[C-]#N.[C-]#N"))), ("C6FeN6-3", -3))
    # CP-073 acetone: a ketone with sp3 C-H only, no O-H; CP-052 lactic acid and glucose formulas
    same("RDKit acetone formula", formula("CC(C)=O"), "C3H6O")
    same("RDKit acetone has no O-H", Descriptors.NumHDonors(mol("CC(C)=O")), 0)
    same("RDKit lactic acid formula C3H6O3", formula("C[C@H](O)C(=O)O"), "C3H6O3")
    same("RDKit 2 lactic acid = glucose in atoms", formula("OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O"), "C6H12O6")
    # CP-072: adenosine (nucleoside) vs AMP (nucleotide): phosphate on C5'
    same("RDKit adenosine formula", formula("Nc1ncnc2c1ncn2[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O"), "C10H13N5O4")
    same("RDKit AMP formula", formula("Nc1ncnc2c1ncn2[C@@H]1O[C@H](COP(=O)(O)O)[C@@H](O)[C@H]1O"), "C10H14N5O7P")
    amp = mol("Nc1ncnc2c1ncn2[C@@H]1O[C@H](COP(=O)(O)O)[C@@H](O)[C@H]1O")
    p_atom = [a for a in amp.GetAtoms() if a.GetSymbol() == "P"][0]
    o_bridge = [n for n in p_atom.GetNeighbors() if any(x.GetSymbol() == "C" for x in n.GetNeighbors())][0]
    c5 = [x for x in o_bridge.GetNeighbors() if x.GetSymbol() == "C"][0]
    same("RDKit AMP phosphate is on an exocyclic CH2 carbon (C5')", (c5.GetTotalNumHs(), c5.IsInRing()), (2, False))
    # CP-071 electronegativity differences (OpenStax Organic Chemistry 2.1 values)
    EN = {"H": 2.1, "C": 2.5, "N": 3.0, "O": 3.5, "S": 2.5}
    same("CP-071 differences", {b: round(EN[b] - EN["H"], 1) for b in "CNOS"}, {"C": 0.4, "N": 0.9, "O": 1.4, "S": 0.4})
    same("CP-071 O-H is the most polar", max("CNOS", key=lambda b: EN[b] - EN["H"]), "O")
except ImportError:
    print("RDKit not installed; structure checks skipped")
    fails.append("rdkit missing")

# ---------- CP-P11 optics ----------
rows = {r[0]: r for r in figure("CP-P11", "tab1")["data"]["rows"]}
def D(cm):
    return 0.0 if cm == "∞" else 1 / (num(cm) / 100)
amp = {p: D(r[2]) - D(r[3]) for p, r in rows.items()}
same("P11 amplitudes of accommodation (D)", {p: round(v, 2) for p, v in amp.items()}, {"A": 2.0, "B": 1.0, "C": 2.0})
read = 0.25
for p, want in (("A", 2.0), ("B", 3.0)):
    check(f"CP-062/064 reading add for {p} (D)", 1 / read - D(rows[p][2]), want, 1e-9)
check("CP-061 C distance lens power (D)", -D(rows["C"][3]), -2.0, 1e-9)
check("CP-061 C distance lens focal length (cm)", -num(rows["C"][3]), -50, 1e-9)
check("CP-061 distractor B cm in 1/f (D)", -1 / 50, -0.02, 1e-9)
check("CP-062 distractor A image term only (D)", D(rows["B"][2]), 1.0, 1e-9)
check("CP-062 distractor C object term only (D)", 1 / read, 4.0, 1e-9)
check("CP-062 distractor D sign dropped (D)", 1 / read + D(rows["B"][2]), 5.0, 1e-9)
same("CP-064 patients with near point beyond 25 cm", [p for p, r in rows.items() if num(r[2]) > 25], ["A", "B"])
same("CP-064 Patient C reads at 25 cm unaided", num(rows["C"][2]) <= 25, True)
# C's near point while wearing the -2.0 D distance lens: 1/do = 1/f - 1/di with di = -0.25 m
check("CP-064 C near point wearing -2 D lens (m)", 1 / (-2.0 + 1 / 0.25), 0.50, 1e-9)
# OpenStax Example 26.4 with the 1.5 cm lens-eye gap: 1/0.235 - 1/0.985 = 3.24 D
check("CP-062 OpenStax 26.4 value with lens-eye gap (D)", 1 / 0.235 - 1 / 0.985, 3.24, 0.002)
check("P11 relaxed eye power with 2.0 cm image distance (D)", 1 / 0.02, 50, 1e-9)
check("P11 eye power for 25 cm object (D)", 1 / 0.25 + 1 / 0.02, 54, 1e-9)
check("CP-063 air-cornea index step", 1.38 - 1.00, 0.38, 1e-9)
check("CP-063 aqueous-lens index step", 1.41 - 1.34, 0.07, 1e-9)
same("CP-063 cornea step is the larger", 0.38 > 0.07, True)

# ---------- CP-P12 electrochemistry ----------
tab = {r[0]: num(r[1]) for r in figure("CP-P12", "tab1")["data"]["rows"]}
E_fe = [v for k_, v in tab.items() if "Fe(CN)" in k_][0]
E_fad = [v for k_, v in tab.items() if k_.startswith("FAD")][0]
E_o2 = [v for k_, v in tab.items() if k_.startswith("O₂")][0]
same("P12 table potentials", (E_o2, E_fe, E_fad), (0.30, 0.36, -0.22))
check("P12 LibreTexts Fe(CN)6 3-/4- 0.356 rounds to table", 0.356, E_fe, 0.015)
check("P12 O2/H2O2 at pH 7 from E° 0.695 (V)", 0.695 - 0.05916 * 7, 0.28, 0.01)
check("P12 O2/H2O2 table value vs pH-7 derivation (V)", E_o2, 0.695 - 0.05916 * 7, 0.07)
Ecell = E_fe - E_fad
check("CP-065 E°'cell FADH2 + 2 ferricyanide (V)", Ecell, 0.58, 1e-9)
check("CP-065 ΔG°' = -nFE (kJ/mol)", -2 * F * Ecell / 1000, -112, 0.01)
check("CP-065 with O2/H2O2 instead (V)", E_o2 - E_fad, 0.52, 1e-9)
check("CP-065 distractor B sign slip (V)", E_fe - abs(E_fad), 0.14, 1e-9)
check("CP-065 distractor D coefficient scaling (V)", 2 * E_fe - E_fad, 0.94, 1e-9)
dE = -0.0592 * (math.log10(1.0) - math.log10(0.01))
check("CP-066 Nernst change 1:100 -> 1:1 (V)", dE, -0.118, 0.005)
check("CP-066 distractor A n = 2 (V)", -0.0592 / 2 * 2, -0.059, 0.005)
check("CP-066 distractor C four decades (V)", -0.0592 * 4, -0.24, 0.02)
Q = 10e-6 * 5.0
check("CP-067 charge (C)", Q, 5.0e-5, 1e-9)
check("CP-067 mol e-", Q / F, 5.2e-10, 0.005)
check("CP-067 mol glucose", Q / F / 2, 2.6e-10, 0.005)
check("CP-067 distractor C x2", Q / F * 2, 1.0e-9, 0.04)
check("CP-067 distractor D amperes", 10 * 5.0 / F / 2, 2.6e-4, 0.005)
check("CP-067 glucose in 1 µL at 5 mmol/L (mol)", 5e-3 * 1e-6, 5e-9, 1e-9)
check("CP-067 fraction consumed", (Q / F / 2) / 5e-9, 0.05, 0.05)
check("CP-067 distractor D mass of glucose (mg)", 2.6e-4 * 180.16 * 1000, 47, 0.01)

# ---------- standalones ----------
r = 0.30e-9
F_c = 9.0e9 * e ** 2 / r ** 2
check("CP-070 Coulomb force (N)", F_c, 2.6e-9, 0.02)
check("CP-070 with CODATA k (N)", k_coulomb * e ** 2 / r ** 2, 2.6e-9, 0.02)
check("CP-070 distractor A r in metres (N)", 9.0e9 * e ** 2 / 0.30 ** 2, 2.6e-27, 0.02)
check("CP-070 distractor B 1/r (N)", 9.0e9 * e ** 2 / r, 7.7e-19, 0.02)
check("CP-070 distractor D doubled (N)", 2 * F_c, 5.1e-9, 0.02)
check("CP-070 NaCl Na-Cl distance from OpenStax radii 102 + 181 pm (nm)", (102 + 181) / 1000, 0.28, 0.02)
check("CP-074 CO2 triple point pressure 517 kPa in atm", 517 / 101.325, 5.1, 0.01)
check("CP-074 CO2 critical pressure 7.38 MPa in atm", 7380 / 101.325, 73, 0.01)
check("CP-074 CO2 triple point 216.55 K in °C", 216.55 - 273.15, -56.6, 0.001)
check("CP-074 CO2 critical temperature 304.18 K in °C", 304.18 - 273.15, 31.0, 0.002)
same("CP-074 1 atm is below the triple-point pressure", 1.0 < 5.1, True)
check("CP-074 water triple point 611.657 Pa in atm", 611.657 / 101325, 0.006, 0.01)
same("CP-073 ketone C=O 1715 is between acid 1710 and aldehyde 1730 (OpenStax 12.8)", 1710 <= 1715 <= 1730, True)
same("CP-073 the clear window 2500-3600 covers the acid O-H band (2500-3300) and overlaps the alcohol O-H band (3400-3650)", 2500 <= 2500 and 3300 <= 3600 and 3400 < 3600, True)

# ---------- choice-length clue: the key must not be the longest option by more than 15% ----------
for q in BATCH["items"]:
    Ls = {k_: len(v) for k_, v in q["options"].items()}
    longest = max(Ls, key=Ls.get)
    same(f"{q['id']} key is not the longest option by >15%", longest == q["answer"] and Ls[longest] > 1.15 * sorted(Ls.values())[-2], False)

# ---------- blueprint bookkeeping (plan batch 3 mix) ----------
from collections import Counter
items = BATCH["items"]
same("mix disciplines", dict(Counter(q["discipline"] for q in items)), {"general chemistry": 10, "biochemistry": 5, "physics": 7, "organic chemistry": 2, "biology": 1})
same("mix skills", dict(sorted(Counter(q["skill"] for q in items).items())), {"1": 8, "2": 11, "3": 3, "4": 3})
same("mix difficulty", dict(sorted(Counter(q["difficulty"] for q in items).items())), {2: 3, 3: 13, 4: 8, 5: 1})
same("ids", [q["id"] for q in items], [f"CP-{n:03d}" for n in range(51, 76)])
same("passage ids", [p["id"] for p in BATCH["passages"]], ["CP-P09", "CP-P10", "CP-P11", "CP-P12"])
letters = [q["answer"] for q in items]
same("answer letters 20-30% each", all(5 <= letters.count(x) <= 7 for x in "ABCD"), True)
same("no letter three in a row", any(letters[i] == letters[i - 1] == letters[i - 2] for i in range(2, len(letters))), False)
# each passage: at least one Skill 1 item and one Skill 3 or 4 item (plan §1)
for p in BATCH["passages"]:
    sk = {q["skill"] for q in items if q["passage"] == p["id"]}
    same(f"{p['id']} has a Skill 1 item", "1" in sk, True)
    same(f"{p['id']} has a Skill 3/4 item", bool(sk & {"3", "4"}), True)
# the ★★★★★ item is the Skill 4 capstone of its passage (plan §1)
same("CP-059 is the Skill 4 ★★★★★ capstone", [(q["skill"], q["passage"]) for q in items if q["difficulty"] == 5], [("4", "CP-P10")])
# plan topics
plan_topics = {"CP-051": "5E.calorimetry-heat-transfer", "CP-052": "5E.enthalpy-hess", "CP-053": "5E.thermodynamic-laws", "CP-054": "5E.bioenergetics",
               "CP-055": "5E.calorimetry-heat-transfer", "CP-056": "4E.mass-spectrometry", "CP-057": "4E.mass-spectrometry", "CP-058": "5D.peptides-proteins",
               "CP-059": "5D.amino-acids", "CP-060": "4E.nucleus-isotopes", "CP-061": "4D.lenses", "CP-062": "4D.eye-optical-instruments",
               "CP-063": "4D.reflection-refraction", "CP-064": "4D.lenses", "CP-065": "4C.galvanic-cells", "CP-066": "4C.concentration-cells-batteries",
               "CP-067": "4C.electrolytic-cells", "CP-068": "5E.biological-redox", "CP-069": "4C.galvanic-cells", "CP-070": "4C.charge-coulomb",
               "CP-071": "5B.polarity", "CP-072": "5D.nucleotides-nucleic-acids", "CP-073": "4D.ir-spectroscopy", "CP-074": "5E.free-energy-phases",
               "CP-075": "5E.enzyme-inhibition-regulation"}
for q in items:
    same(f"{q['id']} first topic matches the plan", q["topics"][0], plan_topics[q["id"]])

print()
print(f"{len(fails)} failures" + (": " + ", ".join(fails) if fails else ""))
sys.exit(1 if fails else 0)
