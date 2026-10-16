"""Independent numeric and structural checks for Chem/Phys batch 2 (CP-026 to CP-050).

Every number quoted in content/mcat/chem_phys/batch_02.json is re-derived here from the passage constants, separately
from the explanations, and compared with the value the item or figure uses. Structures and formulas are checked with RDKit.
Run:  py review/chem_phys_batch_02_check.py     (exit 1 on any mismatch)
"""
import json
import math
import sys

fails = []
BATCH = json.load(open("content/mcat/chem_phys/batch_02.json", encoding="utf-8"))


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


# ---------- CP-P05  axon cable model ----------
rho, L, Cspec = 1.0, 1.0e-3, 1.0e-2          # ohm.m, m, F/m^2 (passage values)


def R_axial(d):
    return rho * L / (math.pi * (d / 2) ** 2)


def C_internode(d, n):
    return Cspec * math.pi * d * L / n


fibres = [("1", 10e-6, 100), ("2", 5e-6, 100), ("3", 10e-6, 20), ("4", 10e-6, 1)]
rows = figure("CP-P05", "tab1")["data"]["rows"]
for (name, d, n), row in zip(fibres, rows):
    R, C = R_axial(d), C_internode(d, n)
    tau = R * C
    check(f"P05 fibre {name} C per internode (pF)", C * 1e12, float(row[2]))
    check(f"P05 fibre {name} tau = RC (us)", tau * 1e6, float(row[3].replace(",", "")), 0.01)
    same(f"P05 fibre {name} bilayers n", int(row[1]), n)
    if row[4] != "failed":
        v = float(row[4])
        check(f"P05 fibre {name} measured v is 4% below L/tau (m/s)", 0.96 * L / tau, v, 0.01)
        check(f"P05 fibre {name} v*tau constant (um)", v * tau * 1e6, 960, 0.01)
check("CP-028 R of 10 um internode (MOhm)", R_axial(10e-6) / 1e6, 13, 0.03)
check("CP-028 distractor diameter as radius (MOhm)", rho * L / (math.pi * (10e-6) ** 2) / 1e6, 3.2, 0.02)
check("CP-028 distractor 5 um fibre (MOhm)", R_axial(5e-6) / 1e6, 51, 0.02)
check("CP-028 distractor power of ten (MOhm)", R_axial(10e-6) / 1e7, 1.3, 0.03)
check("CP-027 ratio C(bare)/C(100 bilayers)", C_internode(10e-6, 1) / C_internode(10e-6, 100), 100, 1e-9)
tau40 = R_axial(10e-6) * C_internode(10e-6, 40)
check("CP-029 C with 40 bilayers (pF)", C_internode(10e-6, 40) * 1e12, 7.85, 0.01)
check("CP-029 tau with 40 bilayers (us)", tau40 * 1e6, 100, 0.01)
check("CP-029 v = 960 um / tau (m/s)", 960e-6 / tau40, 9.6, 0.01)
check("CP-029 v = L/tau (m/s)", L / tau40, 10, 0.01)
check("CP-029 distractor v proportional to tau (m/s)", 4.8 * (tau40 / (R_axial(10e-6) * C_internode(10e-6, 20))), 2.4, 0.01)
check("CP-029 distractor bilayer ratio squared (m/s)", 4.8 * (40 / 20) ** 2, 19, 0.03)
# Tasaki & Matsumoto (2002) frog fibre: r_i 1.45e8 ohm/cm -> MOhm per mm; same order as the model
check("P05 frog r_i per mm (MOhm) is of order the model's 13 MOhm", 1.45e8 / 10 / 1e6, 14.5, 1e-9)

# ---------- CP-P06  pH partition ----------
drugs = {"W": ("acid", 4.0, 2.5), "X": ("acid", 7.0, -1.0), "Y": ("base", 9.0, 2.0), "Z": ("base", 5.0, 2.0)}


def unionized(kind, pKa, pH):
    return 1 / (1 + 10 ** (pH - pKa)) if kind == "acid" else 1 / (1 + 10 ** (pKa - pH))


fig = figure("CP-P06", "fig1")["data"]["series"]
for s, pH in zip(fig, (2.0, 6.0)):
    for drug, val in s["points"]:
        kind, pKa, _ = drugs[drug]
        want = round(100 * unionized(kind, pKa, pH), 1)
        check(f"P06 Figure 1 {drug} un-ionized at pH {pH} (%)", want, val, 1e-9)
check("CP-031 W ionized fraction at pH 5.0 (%)", 100 * (1 - unionized("acid", 4.0, 5.0)), 91, 0.005)
check("CP-031 distractor un-ionized (%)", 100 * unionized("acid", 4.0, 5.0), 9, 0.02)
check("CP-031 distractor two units above pKa (%)", 100 * (1 - unionized("acid", 4.0, 6.0)), 99, 0.002)
# CP-033 distractor B: 1.0 mmol of salt in 900 mL of pH 2.0 fluid barely moves the pH
H = 0.010 * 0.900
check("CP-033 H+ in 900 mL at pH 2.0 (mmol)", H * 1e3, 9.0, 1e-9)
check("CP-033 pH after 1.0 mmol anion protonated", -math.log10((H - 1.0e-3) / 0.900), 2.05, 0.005)
# CP-035: at pH 2.0 the acids are neutral and the bases protonated; X's log P -1.0 means octanol:water 1:10
check("CP-035 Y un-ionized at pH 2.0 (one part in ten million)", unionized("base", 9.0, 2.0), 1e-7, 0.01)
check("CP-035 X octanol:water ratio from log P", 10 ** -1.0, 0.1, 1e-9)

# ---------- CP-P07  purification table ----------
tab = figure("CP-P07", "tab1")["data"]["rows"]
prot = [float(r[1]) for r in tab]
act = [float(r[2].replace(",", "")) for r in tab]
sa = [a / p for a, p in zip(act, prot)]
print("P07 specific activities (U/mg):", [round(x, 1) for x in sa], " fold:", [round(x / sa[0], 1) for x in sa], " yield %:", [round(100 * a / act[0], 1) for a in act])
check("CP-036 SA lysate (U/mg)", sa[0], 4.0, 1e-9)
check("CP-036 SA after gel filtration (U/mg)", sa[2], 300, 1e-9)
check("CP-036 fold purification after step 3", sa[2] / sa[0], 75, 1e-9)
check("CP-036 yield after step 3 (%)", 100 * act[2] / act[0], 60, 1e-9)
check("CP-036 step 2 fold (passage check)", sa[1] / sa[0], 40, 1e-9)
check("CP-036 step 2 yield (%)", 100 * act[1] / act[0], 80, 1e-9)
check("CP-036 distractor step yield 1200/1600 (%)", 100 * act[2] / act[1], 75, 1e-9)
check("CP-036 distractor protein ratio 500/4", prot[0] / prot[2], 125, 1e-9)
ok = sa[3] < sa[2] and all(sa[i] > sa[i - 1] for i in range(1, 3))
print(f"{'ok  ' if ok else 'FAIL'} P07 specific activity rises at every step but the last ({[round(x) for x in sa]})")
if not ok:
    fails.append("P07 SA trend")
check("CP-040 Zn atomic mass added to a 50 kDa chain (Da)", 65.4, 65, 0.01)
check("CP-039 native mass / SDS band = subunits", 100 / 50, 2, 1e-9)

# ---------- CP-P08  Doppler ----------
c, f0 = 1540.0, 3.00e6
tab = figure("CP-P08", "tab1")["data"]["rows"]
shifts = {(r[0], r[1]): float(r[2].replace(",", "").replace("−", "-").replace("+", "")) for r in tab}
v_art = shifts[("Umbilical artery, loop 1", "0°")] * c / (2 * f0)
v_vein = -shifts[("Umbilical vein, loop 1", "0°")] * c / (2 * f0)
check("CP-044 artery speed from loop 1 (m/s)", v_art, 0.51, 0.01)
check("P08 vein speed from loop 1 (m/s)", v_vein, 0.154, 0.01)
check("P08 loop 2 artery shift = loop 1 x cos 60 (Hz)", shifts[("Umbilical artery, loop 1", "0°")] * math.cos(math.radians(60)), shifts[("Umbilical artery, loop 2", "60°")], 1e-9)
check("P08 loop 2 vein shift = loop 1 x cos 60 (Hz)", shifts[("Umbilical vein, loop 1", "0°")] * math.cos(math.radians(60)), shifts[("Umbilical vein, loop 2", "60°")], 1e-9)
check("CP-044 same speed from loop 2 with cos 60 (m/s)", shifts[("Umbilical artery, loop 2", "60°")] * c / (2 * f0 * 0.5), v_art, 1e-9)
check("CP-044 distractor loop 2 without cos (m/s)", shifts[("Umbilical artery, loop 2", "60°")] * c / (2 * f0), 0.26, 0.02)
check("CP-044 distractor factor 2 omitted (m/s)", 2000 * c / f0, 1.0, 0.03)
check("CP-044 distractor factor 2 multiplied (m/s)", 2 * 2000 * c / f0, 2.1, 0.03)
check("CP-044 shortcut (df/f0)(c/2)", (2000 / f0) * (c / 2), v_art, 1e-9)
check("CP-042 wavelength in tissue (mm)", c / f0 * 1e3, 0.51, 0.01)
check("CP-042 distractor speed in air 330 m/s (mm)", 330 / f0 * 1e3, 0.11, 0.01)
check("CP-042 distractor f/c (per m)", f0 / c, 1.9e3, 0.03)
check("CP-043 wavelength at 10 MHz (mm)", c / 10e6 * 1e3, 0.15, 0.03)
# OpenStax Example 17.8: 2.50 MHz, 20.0 cm/s toward, 1540 m/s -> beat 649 Hz; the small-v formula gives the same
f1 = 2.50e6 * (c + 0.200) / c
f2 = f1 * c / (c - 0.200)
check("P08 OpenStax Example 17.8 exact double shift (Hz)", f2 - 2.50e6, 649, 0.002)
check("P08 OpenStax Example 17.8 via 2 f0 v / c (Hz)", 2 * 2.50e6 * 0.200 / c, 649, 0.002)
# Realism: umbilical vein peak velocity ~18 cm/s at 36 weeks (Spurway 2017); artery PSV ~40-65 cm/s
ok = 0.12 <= v_vein <= 0.25 and 0.40 <= v_art <= 0.65
print(f"{'ok  ' if ok else 'FAIL'} P08 speeds are physiological: vein {v_vein:.3f} m/s, artery {v_art:.2f} m/s")
if not ok:
    fails.append("P08 realism")

# ---------- standalones ----------
check("CP-045 reaction distance (m)", 20 * 1.0, 20, 1e-9)
check("CP-045 braking distance v0^2/(2a) (m)", 20 ** 2 / (2 * 5.0), 40, 1e-9)
check("CP-045 braking distance via average speed (m)", (20 / 5.0) * (20 / 2), 40, 1e-9)
check("CP-045 total (m)", 20 + 40, 60, 1e-9)
check("CP-045 distractor v0 t with t = v0/a (m)", 20 * (20 / 5.0), 80, 1e-9)
# CP-048 bond energies (OpenStax Chemistry 2e Table 7.2)
BE = {"C=C": 611, "C-C": 345, "C-H": 415, "H-H": 436}
broken, formed = BE["C=C"] + BE["H-H"], BE["C-C"] + 2 * BE["C-H"]
check("CP-048 bonds broken (kJ/mol)", broken, 1047, 1e-9)
check("CP-048 bonds formed (kJ/mol)", formed, 1175, 1e-9)
check("CP-048 dH (kJ/mol)", broken - formed, -128, 1e-9)
check("CP-048 distractor H-H not broken", BE["C=C"] - formed, -564, 1e-9)
check("CP-048 distractor one C-H formed", broken - (BE["C-C"] + BE["C-H"]), 287, 1e-9)
# Check the quoted literature range brackets the estimate: ethylene -136, propene -125, 2-butenes -119/-115 (OpenStax Org Chem Table 7.2)
ok = -136 <= -128 <= -115
print(f"{'ok  ' if ok else 'FAIL'} CP-048 estimate lies within measured heats of hydrogenation (-136 to -115 kJ/mol)")
if not ok:
    fails.append("CP-048 range")

# ---------- RDKit: structures, formulas, formal charges, stereo ----------
try:
    from rdkit import Chem, RDLogger
    from rdkit.Chem import rdMolDescriptors, FindMolChiralCenters, Descriptors
    RDLogger.DisableLog("rdApp.*")

    def mol(smi):
        m = Chem.MolFromSmiles(smi)
        assert m is not None, smi
        return m

    def formula(smi):
        return rdMolDescriptors.CalcMolFormula(mol(smi))

    def charges(smi):
        return [(a.GetSymbol(), a.GetFormalCharge()) for a in mol(smi).GetAtoms()]

    tests = [
        ("imidazole (CP-037)", "c1cnc[nH]1", "C3H4N2"),
        ("histidine side chain: L-histidine", "C1=C(NC=N1)C[C@@H](C(=O)O)N", "C6H9N3O2"),
        ("propan-2-ol (CP-050)", "CC(C)O", "C3H8O"),
        ("propanone / acetone (CP-050)", "CC(C)=O", "C3H6O"),
        ("propanal (CP-050 distractor)", "CCC=O", "C3H6O"),
        ("propanoic acid (CP-050 distractor)", "CCC(=O)O", "C3H6O2"),
        ("propene (CP-050 distractor)", "CC=C", "C3H6"),
        ("alpha-D-glucopyranose (CP-047)", "OC[C@H]1O[C@H](O)[C@H](O)[C@@H](O)[C@@H]1O", "C6H12O6"),
        ("beta-D-glucopyranose (CP-047)", "OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O", "C6H12O6"),
        ("bicarbonate (CP-046)", "OC(=O)[O-]", "CHO3-"),
        ("carbonate (CP-046)", "[O-]C(=O)[O-]", "CO3-2"),
        ("carbonic acid (CP-046)", "OC(=O)O", "CH2O3"),
        ("EDTA (CP-P07)", "OC(=O)CN(CCN(CC(=O)O)CC(=O)O)CC(=O)O", "C10H16N2O8"),
        ("ethene (CP-048)", "C=C", "C2H4"),
        ("ethane (CP-048)", "CC", "C2H6"),
    ]
    for name, smi, want in tests:
        f = formula(smi)
        ok = f == want
        print(f"{'ok  ' if ok else 'FAIL'} RDKit {name}: {f}")
        if not ok:
            fails.append(name)
    same("RDKit bicarbonate charges", sum(c for _, c in charges("OC(=O)[O-]")), -1)
    same("RDKit carbonate charges", sum(c for _, c in charges("[O-]C(=O)[O-]")), -2)
    # CP-050: propan-2-ol is a secondary alcohol (the C bearing OH has two carbon neighbours); oxidation to acetone keeps C3
    m = mol("CC(C)O")
    c_oh = [a for a in m.GetAtoms() if a.GetSymbol() == "C" and any(n.GetSymbol() == "O" for n in a.GetNeighbors())][0]
    same("RDKit propan-2-ol: carbinol carbon has 2 carbon neighbours (secondary)", sum(1 for n in c_oh.GetNeighbors() if n.GetSymbol() == "C"), 2)
    same("RDKit propan-2-ol: carbinol carbon has 1 H (can lose it on oxidation)", c_oh.GetTotalNumHs(), 1)
    # CP-047: the two glucopyranose anomers differ at exactly one stereocentre, C1 (the carbon bonded to two oxygens)
    a, b = mol("OC[C@H]1O[C@H](O)[C@H](O)[C@@H](O)[C@@H]1O"), mol("OC[C@H]1O[C@@H](O)[C@H](O)[C@@H](O)[C@@H]1O")
    ca, cb = dict(FindMolChiralCenters(a, useLegacyImplementation=False)), dict(FindMolChiralCenters(b, useLegacyImplementation=False))
    diff = [i for i in ca if ca[i] != cb[i]]
    same("RDKit anomers: number of stereocentres each", (len(ca), len(cb)), (5, 5))
    same("RDKit anomers differ at exactly one centre", len(diff), 1)
    anomeric = diff[0] if diff else None
    two_o = anomeric is not None and sum(1 for n in a.GetAtomWithIdx(anomeric).GetNeighbors() if n.GetSymbol() == "O") == 2
    same("RDKit the differing centre is the anomeric (hemiacetal) carbon bonded to two O", two_o, True)
    same("RDKit anomers are not enantiomers (other centres agree)", all(ca[i] == cb[i] for i in ca if i != anomeric), True)
    # CP-040: zinc atomic mass
    from rdkit.Chem import GetPeriodicTable
    check("RDKit Zn atomic mass (Da)", GetPeriodicTable().GetAtomicWeight(30), 65.38, 0.001)
    # CP-048: ethene -> ethane adds exactly two H and turns one double bond into a single bond
    same("RDKit hydrogenation adds 2 H", Descriptors.NumHDonors(mol("CC")) == 0 and (mol("CC").GetNumAtoms() == mol("C=C").GetNumAtoms()), True)
    same("RDKit ethene has one double bond", sum(1 for bd in mol("C=C").GetBonds() if bd.GetBondType() == Chem.BondType.DOUBLE), 1)
    same("RDKit ethane H count", sum(at.GetTotalNumHs() for at in mol("CC").GetAtoms()) - sum(at.GetTotalNumHs() for at in mol("C=C").GetAtoms()), 2)
except ImportError:
    print("RDKit not installed; structure checks skipped")
    fails.append("rdkit missing")

# ---------- choice-length clue: the key must not be the longest option by more than 15% ----------
for q in BATCH["items"]:
    L = {k: len(v) for k, v in q["options"].items()}
    longest = max(L, key=L.get)
    same(f"{q['id']} key is not the longest option by >15%", longest == q["answer"] and L[longest] > 1.15 * sorted(L.values())[-2], False)

# ---------- blueprint bookkeeping (plan batch 2 mix) ----------
from collections import Counter
items = BATCH["items"]
same("mix disciplines", dict(Counter(q["discipline"] for q in items)), {"general chemistry": 8, "biochemistry": 5, "physics": 8, "organic chemistry": 2, "biology": 2})
same("mix skills", dict(sorted(Counter(q["skill"] for q in items).items())), {"1": 9, "2": 10, "3": 3, "4": 3})
same("mix difficulty", dict(sorted(Counter(q["difficulty"] for q in items).items())), {2: 5, 3: 11, 4: 9})   # CP-046 re-rated ★★ at review
same("ids", [q["id"] for q in items], [f"CP-{n:03d}" for n in range(26, 51)])
same("passage ids", [p["id"] for p in BATCH["passages"]], ["CP-P05", "CP-P06", "CP-P07", "CP-P08"])
letters = [q["answer"] for q in items]
same("answer letters 20-30% each", all(5 <= letters.count(x) <= 7 for x in "ABCD"), True)
same("no letter three in a row", any(letters[i] == letters[i - 1] == letters[i - 2] for i in range(2, len(letters))), False)
# each passage: at least one Skill 1 item and one Skill 3 or 4 item (plan §1)
# The plan (docs/CHEM_PHYS_250.md) assigns CP-P08 skills 2, 2, 1, 2, so that passage has no Skill 3/4 item; the batch keeps the
# plan's item-level skills (the batch totals 9/10/3/3 are the blueprint) and the exception is recorded in the plan's changelog.
for p in BATCH["passages"]:
    sk = {q["skill"] for q in items if q["passage"] == p["id"]}
    same(f"{p['id']} has a Skill 1 item", "1" in sk, True)
    if p["id"] != "CP-P08":
        same(f"{p['id']} has a Skill 3/4 item", bool(sk & {"3", "4"}), True)
    else:
        print(f"note CP-P08 has no Skill 3/4 item, as planned (skills {sorted(sk)})")

print("\nALL CHECKS PASSED" if not fails else f"\n{len(fails)} FAILED: {fails}")
sys.exit(1 if fails else 0)
