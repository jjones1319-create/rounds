"""Independent numeric and structural checks for Chem/Phys batch 4 (CP-076 to CP-100).

Every number quoted in content/mcat/chem_phys/batch_04.json is re-derived here from the passage constants, separately
from the explanations, and compared with the value the item or figure uses. Structures, formulas, molar masses,
stereocentres and ring counts are checked with RDKit. Run:  py review/chem_phys_batch_04_check.py   (exit 1 on any mismatch)
"""
import json
import math
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
fails = []
BATCH = json.load(open("content/mcat/chem_phys/batch_04.json", encoding="utf-8"))
ITEMS = {q["id"]: q for q in BATCH["items"]}


def check(name, got, want, tol=0.02):
    ok = abs(got - want) <= tol * max(abs(want), 1e-12)
    print(f"{'ok  ' if ok else 'FAIL'} {name}: computed {got:.6g}, item uses {want:.6g}")
    if not ok:
        fails.append(name)


def same(name, got, want):
    ok = got == want
    print(f"{'ok  ' if ok else 'FAIL'} {name}: {got!r} {'==' if ok else '!='} {want!r}")
    if not ok:
        fails.append(name)


def figure(pid, fid):
    return [f for p in BATCH["passages"] if p["id"] == pid for f in p["figures"] if f["id"] == fid][0]


def num(s):
    return float(str(s).replace(",", "").replace("−", "-").replace("+", "").replace("<", "").replace("bp", "").strip())


def opt(qid, letter):
    """First number in an option, e.g. '2.0 × 10⁵ J' -> 2e5."""
    import re
    s = ITEMS[qid]["options"][letter].replace("×", "x").replace(",", "")
    sup = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻", "0123456789-")
    s = s.translate(sup)
    m = re.search(r"(-?\d+(?:\.\d+)?)(?:\s*x\s*10\^?(-?\d+))?", s)
    v = float(m.group(1))
    if m.group(2):
        v *= 10 ** int(m.group(2))
    return v


# ---------- constants (NIST CODATA 2022) ----------
e = 1.602176634e-19       # C
eps0 = 8.8541878188e-12   # F/m
R_gas = 0.082057          # L atm / (mol K)

# ================= CP-P13 haemoglobin =================
n_hill = 2.8
p50 = {"HbA, pH 7.4": 26.0, "HbA, pH 7.2": 32.0, "HbF, pH 7.4": 20.0}


def Y(P, P50):
    return 0.0 if P == 0 else 1 / (1 + (P50 / P) ** n_hill)


fig = figure("CP-P13", "fig1")["data"]
for s in fig["series"]:
    for x, y in s["points"]:
        got = 100 * Y(x, p50[s["name"]])
        same(f"P13 curve {s['name']} at {x} mmHg (%) rounds to the plotted value", round(got, 1), y)
    same(f"P13 curve {s['name']} has 21 points 0-100", [x for x, _ in s["points"]], list(range(0, 101, 5)))
# CP-076: the pH 7.2 curve crosses 50% between 30 and 35 mmHg; linear interpolation lands near 32
y30, y35 = 100 * Y(30, 32), 100 * Y(35, 32)
check("CP-076 pH 7.2 curve at 30 mmHg (%)", y30, 45.5, 0.01)
check("CP-076 pH 7.2 curve at 35 mmHg (%)", y35, 56.2, 0.01)
x50 = 30 + 5 * (50 - y30) / (y35 - y30)
check("CP-076 interpolated P50 from the plotted points (mmHg)", x50, 32, 0.01)
check("CP-076 pH 7.2 curve at 26 mmHg (%)", 100 * Y(26, 32), 36, 0.02)
check("CP-076 pH 7.2 curve at 50 mmHg (%)", 100 * Y(50, 32), 78, 0.02)
same("CP-076 answer is the 32 mmHg option", opt("CP-076", ITEMS["CP-076"]["answer"]), 32.0)
# CP-079: Henderson-Hasselbalch on the model pKa values
check("CP-079 T-state protonated:unprotonated at pH 7.4", 10 ** (7.8 - 7.4), 2.5, 0.01)
check("CP-079 R-state protonated:unprotonated at pH 7.4", 10 ** (7.0 - 7.4), 0.4, 0.01)
check("CP-079 log 2.5", math.log10(2.5), 0.40, 0.01)
check("CP-079 fraction protonated in T", 2.5 / 3.5, 0.714, 0.01)
check("P13 Bohr shift log(32/26) per 0.2 pH (log units)", math.log10(32 / 26), 0.09, 0.03)
check("CP-079 whole-blood-like Bohr factor Δlog P50/ΔpH", math.log10(32 / 26) / -0.2, -0.45, 0.03)
# saturation differences quoted nowhere, but sanity: at 40 mmHg the pH 7.2 curve releases more O2
same("P13 lower pH gives lower saturation at 40 mmHg", Y(40, 32) < Y(40, 26), True)

# ================= CP-P14 defibrillator =================
rows = {r[0]: r[1] for r in figure("CP-P14", "tab1")["data"]["rows"]}
C = num(rows["Capacitance"].replace("µF", "")) * 1e-6
V0 = num(rows["Charging voltage"].replace("V", ""))
Rch = num(rows["Chest resistance"].replace("Ω", ""))
t_pulse = num(rows["Pulse truncated at"].replace("ms", "")) * 1e-3
d_film = num(rows["Film thickness"].replace("µm", "")) * 1e-6
U = 0.5 * C * V0**2
check("CP-081 stored energy (J)", U, 200, 1e-9)
check("CP-081 distractor A ½CV (J)", 0.5 * C * V0, 0.10, 1e-9)
check("CP-081 distractor C CV² (J)", C * V0**2, 400, 1e-9)
check("CP-081 distractor D with 100 mF (J)", 0.5 * 0.1 * V0**2, 2.0e5, 1e-9)
check("CP-081 charge Q = CV (C)", C * V0, 0.20, 1e-9)
check("CP-081 ½QV (J)", 0.5 * C * V0 * V0, 200, 1e-9)
E = V0 / d_film
check("CP-082 field V/d (V/m)", E, 1.0e8, 1e-9)
check("CP-082 field in V/µm", E * 1e-6, 100, 1e-9)
same("CP-082 field below polypropylene strength (650 V/µm)", E * 1e-6 < 650, True)
check("CP-082 work eV (J)", e * V0, 3.2e-16, 0.002)
check("CP-082 work eEd (J)", e * E * d_film, 3.2e-16, 0.002)
check("CP-082 work in eV", V0, 2000, 1e-9)
check("CP-082 distractor A d = 20 mm (V/m)", V0 / 0.020, 1.0e5, 1e-9)
check("CP-082 distractor B 1 eV (J)", e, 1.6e-19, 0.002)
check("CP-082 distractor D q = 1 C (J)", 1 * V0, 2.0e3, 1e-9)
A_plate = C * d_film / (2.2 * eps0)
check("P14 plate area from C = κε0A/d (m²), plausibility", A_plate, 100, 0.05)
check("P14 film volume A·d (L), plausibility", A_plate * d_film * 1000, 2.0, 0.05)
I0 = V0 / Rch
tau = Rch * C
check("CP-083 initial current (A)", I0, 25, 1e-9)
check("CP-083 time constant RC (ms)", tau * 1e3, 8.0, 1e-9)
check("CP-083 distractor A R/V (A)", Rch / V0, 0.040, 1e-9)
check("CP-083 distractor B C/R (µs)", C / Rch * 1e6, 1.25, 1e-9)
check("CP-083 distractor D with 0.1 F (s)", Rch * 0.1, 8.0, 1e-9)
check("CP-083 e^-1", math.exp(-1), 0.37, 0.01)
check("CP-083 V/V0 at 20 ms", math.exp(-t_pulse / tau), 0.08, 0.03)
frac_left = math.exp(-2 * t_pulse / tau)
check("P14 energy fraction remaining at 20 ms", frac_left, 0.007, 0.05)
same("P14 more than 99% delivered by 20 ms", 1 - frac_left > 0.99, True)
check("CP-084 average power (W)", 200 / t_pulse, 1.0e4, 1e-9)
check("CP-084 peak power V0²/R (W)", V0**2 / Rch, 5.0e4, 1e-9)
check("CP-084 peak power V0·I0 (W)", V0 * I0, 5.0e4, 1e-9)
check("CP-084 distractor A 20 s (W)", 200 / 20, 10, 1e-9)
check("CP-084 distractor D 20 µs (W)", 200 / 20e-6, 1.0e7, 1e-9)
same("CP-084 answer option is 10 kW", ITEMS["CP-084"]["options"][ITEMS["CP-084"]["answer"]], "10 kW")

# ================= CP-P15 aspirin =================
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers

smi = {f["id"]: f["data"]["smiles"] for f in [figure("CP-P15", x) for x in ("fig1", "fig2", "fig3")]}
mols = {k: Chem.MolFromSmiles(v) for k, v in smi.items()}
same("P15 Fig 1 formula (salicylic acid C7H6O3)", rdMolDescriptors.CalcMolFormula(mols["fig1"]), "C7H6O3")
same("P15 Fig 2 formula (acetic anhydride C4H6O3)", rdMolDescriptors.CalcMolFormula(mols["fig2"]), "C4H6O3")
same("P15 Fig 3 formula (aspirin C9H8O4)", rdMolDescriptors.CalcMolFormula(mols["fig3"]), "C9H8O4")
phenol = Chem.MolFromSmarts("c[OX2H]")
cooh = Chem.MolFromSmarts("C(=O)[OX2H]")
ester = Chem.MolFromSmarts("C(=O)O[c,C]")
same("P15 salicylic acid has a phenol OH", mols["fig1"].HasSubstructMatch(phenol), True)
same("P15 salicylic acid has a carboxylic acid", mols["fig1"].HasSubstructMatch(cooh), True)
same("P15 aspirin has no phenol OH (FeCl3 negative)", mols["fig3"].HasSubstructMatch(phenol), False)
same("P15 aspirin has a carboxylic acid", mols["fig3"].HasSubstructMatch(cooh), True)
same("P15 aspirin has an aryl ester", mols["fig3"].HasSubstructMatch(Chem.MolFromSmarts("C(=O)Oc")), True)
same("P15 acetic anhydride is an anhydride", mols["fig2"].HasSubstructMatch(Chem.MolFromSmarts("C(=O)OC(=O)")), True)
same("P15 acetic anhydride has no methoxy group", mols["fig2"].HasSubstructMatch(Chem.MolFromSmarts("[CH3]O")), False)
M = {k: Descriptors.MolWt(m) for k, m in mols.items()}
t1 = {r[0]: r for r in figure("CP-P15", "tab1")["data"]["rows"]}
check("P15 Table 1 M salicylic acid", M["fig1"], num(t1["Salicylic acid"][1]), 0.001)
check("P15 Table 1 M acetic anhydride", M["fig2"], num(t1["Acetic anhydride"][1]), 0.001)
check("P15 Table 1 M aspirin", M["fig3"], num(t1["Aspirin"][1]), 0.001)
# atom balance of salicylic acid + acetic anhydride -> aspirin + acetic acid
acoh = Chem.MolFromSmiles("CC(=O)O")
same("P15 reaction mass balance", round(M["fig1"] + M["fig2"], 2) == round(M["fig3"] + Descriptors.MolWt(acoh), 2), True)
m_sa, m_aa, m_prod = num(t1["Salicylic acid"][2]), num(t1["Acetic anhydride"][2]), num(t1["Aspirin"][2])
n_sa, n_aa = m_sa / M["fig1"], m_aa / M["fig2"]
check("CP-089 moles salicylic acid", n_sa, 0.0500, 0.002)
check("CP-089 moles acetic anhydride", n_aa, 0.100, 0.002)
same("CP-089 salicylic acid limits (1:1)", n_sa < n_aa, True)
theo = n_sa * M["fig3"]
check("CP-089 theoretical yield (g)", theo, 9.00, 0.002)
check("CP-089 percent yield", 100 * m_prod / theo, 80, 0.002)
check("CP-089 distractor A anhydride limiting (%)", 100 * m_prod / (n_aa * M["fig3"]), 40, 0.002)
check("CP-089 distractor B mass ratio to anhydride (%)", 100 * m_prod / m_aa, 71, 0.01)
check("CP-089 distractor D mass ratio to salicylic acid (%)", 100 * m_prod / m_sa, 104, 0.01)
check("P15 acetic anhydride volume at 1.08 g/mL (mL)", m_aa / 1.08, 9.4, 0.01)
# CP-088 bicarbonate extraction
pKa_carbonic = -math.log10(4.3e-7)
check("CP-088 carbonic acid pKa from Ka 4.3e-7", pKa_carbonic, 6.4, 0.01)
check("CP-088 equilibrium ratio 10^(6.4-3.5)", 10 ** (6.4 - 3.5), 800, 0.01)
same("CP-088 'nearly a thousand to one' is between 500 and 1000", 500 < 10 ** (6.4 - 3.5) < 1000, True)
# CP-087 recrystallization arithmetic from Table 2 (7.5 g of crude)
t2 = {r[0]: (num(r[1]), num(r[2])) for r in figure("CP-P15", "tab2")["data"]["rows"]}
mass = 7.5
vol_mix = mass / t2["Ethanol–water"][1] * 100
check("CP-087 hot ethanol-water needed (mL)", vol_mix, 75, 1e-9)
left_mix = t2["Ethanol–water"][0] * vol_mix / 100
check("CP-087 left dissolved on cooling (g)", left_mix, 0.4, 0.1)
check("CP-087 recovery (%)", 100 * (mass - left_mix) / mass, 95, 0.01)
check("CP-087 Table 2 hot/cold ratio for the mixed solvent", t2["Ethanol–water"][1] / t2["Ethanol–water"][0], 20, 1e-9)
vol_eth = mass / t2["Ethanol"][1] * 100
check("CP-087 hot ethanol needed (mL)", vol_eth, 11.5, 0.01)
left_eth = t2["Ethanol"][0] * vol_eth / 100
check("CP-087 ethanol: left dissolved on cooling the minimum hot volume (g)", left_eth, 2.3, 0.01)
check("CP-087 ethanol: fraction lost", left_eth / mass, 0.31, 0.02)
check("CP-087 ethanol hot/cold ratio", t2["Ethanol"][1] / t2["Ethanol"][0], 3.25, 1e-9)
same("CP-087 ethanol recovery is worse than the mixed solvent's", (mass - left_eth) / mass < (mass - left_mix) / mass, True)
check("CP-087 hexane hot volume needed (L)", mass / t2["Hexane"][1] * 100 / 1000, 3.75, 1e-9)
check("CP-087 water at 60 °C volume needed (mL)", mass / t2["Water"][1] * 100, 500, 1e-9)
same("CP-087 answer is the mixed solvent", ITEMS["CP-087"]["options"][ITEMS["CP-087"]["answer"]], "ethanol–water")

# ================= CP-P16 diving =================
rows1 = figure("CP-P16", "tab1")["data"]["rows"]
rows2 = figure("CP-P16", "tab2")["data"]["rows"]
for r in rows1:
    depth = num(r[0]); n = 1 + depth / 10
    check(f"P16 Table 1 total at {depth:.0f} m (atm)", n, num(r[1]), 1e-9)
    check(f"P16 Table 1 PO2 at {depth:.0f} m (atm)", 0.21 * n, num(r[2]), 0.005)
    check(f"P16 Table 1 PN2 at {depth:.0f} m (atm)", 0.79 * n, num(r[3]), 0.005)
for r in rows2:
    depth = num(r[0]); n = 1 + depth / 10
    pio2 = 0.21 * 760 * n
    pao2 = 0.21 * (760 * n - 47) - 40 / 0.8
    same(f"P16 Table 2 inspired PO2 at {depth:.0f} m (mmHg) rounds to the table value", round(pio2), int(num(r[1])))
    same(f"P16 Table 2 alveolar PO2 at {depth:.0f} m (mmHg) rounds to the table value", round(pao2), int(num(r[2])))
    check(f"CP-094 inspired minus alveolar at {depth:.0f} m (mmHg)", num(r[1]) - num(r[2]), 60, 0.02)
check("CP-094 water vapour term 0.21 x 47 (mmHg)", 0.21 * 47, 10, 0.02)
check("CP-094 CO2 term 40/0.8 (mmHg)", 40 / 0.8, 50, 1e-9)
check("CP-094 sea-level alveolar PO2 (mmHg)", 0.21 * (760 - 47) - 50, 100, 0.005)
check("CP-090 32% at 30 m (atm)", 0.32 * 4.0, 1.28, 1e-9)
check("CP-090 distractor A air at 30 m (atm)", 0.21 * 4.0, 0.84, 1e-9)
check("CP-090 distractor B gauge 3 atm (atm)", 0.32 * 3.0, 0.96, 1e-9)
check("CP-090 distractor D 40 m (atm)", 0.32 * 5.0, 1.60, 1e-9)
check("CP-090 rise over air (atm)", 0.32 * 4 - 0.21 * 4, 0.44, 1e-9)
check("CP-091 Boyle 30 m to 10 m (L)", 6.0 * 4.0 / 2.0, 12, 1e-9)
check("CP-091 distractor A inverted with surface pressure (L)", 6.0 * 1.0 / 4.0, 1.5, 1e-9)
check("CP-091 distractor B inverted (L)", 6.0 * 2.0 / 4.0, 3.0, 1e-9)
check("CP-091 distractor C volume unchanged (L)", 6.0, 6.0, 1e-9)
Vm = R_gas * 273.15 / 1.0
check("CP-092 molar volume at STP (L/mol)", Vm, 22.4, 0.002)
check("CP-092 moles in 2,400 L at STP", 2400 / Vm, 107, 0.01)
same("CP-092 107 mol is closest to the 110 option", min((1.1, 11, 110, 1100), key=lambda v: abs(v - 2400 / Vm)), 110)
check("CP-092 22.4 x 100 (L)", 22.4 * 100, 2240, 1e-9)
check("CP-092 remaining 160 L (mol)", 160 / 22.4, 7, 0.03)
check("CP-092 distractor A volume (L)", 1.1 * 22.4, 25, 0.02)
check("CP-092 distractor B volume (L)", 11 * 22.4, 250, 0.02)
check("CP-092 distractor D volume (L)", 1100 * 22.4, 25000, 0.02)
check("CP-093 PN2 at 30 m (atm)", 0.79 * 4, 3.16, 1e-9)
check("CP-093 PN2 at the surface (atm)", 0.79, 0.79, 1e-9)
check("P16 seawater depth per atm at 1,025 kg/m3 (m)", 101325 / (1025 * 9.81), 10.1, 0.01)

# ================= standalone =================
check("CP-095 tan θ", 0.60 / 0.80, 0.75, 1e-9)
check("CP-095 distractor D inverted", 0.80 / 0.60, 1.33, 0.005)
check("CP-095 sin² + cos²", 0.6**2 + 0.8**2, 1.0, 1e-9)
check("CP-095 mass cancels: same answer for 50 kg", (50 * 9.8 * 0.6) / (50 * 9.8 * 0.8), 0.75, 1e-9)
ile = Chem.MolFromSmiles("CC[C@H](C)[C@H](N)C(=O)O")
same("CP-097 L-isoleucine stereocentres (2S,3S)", [c for _, c in Chem.FindMolChiralCenters(ile, useLegacyImplementation=False)], ["S", "S"])
same("CP-097 isoleucine formula", rdMolDescriptors.CalcMolFormula(ile), "C6H13NO2")
isos = {Chem.MolToSmiles(m) for m in EnumerateStereoisomers(Chem.MolFromSmiles("CCC(C)C(N)C(=O)O"))}
same("CP-097 distinct stereoisomers of isoleucine", len(isos), 4)
l_ile = Chem.MolToSmiles(ile)
d_ile = Chem.MolToSmiles(Chem.MolFromSmiles("CC[C@@H](C)[C@@H](N)C(=O)O"))
same("CP-097 enantiomer (2R,3R) is a distinct stereoisomer", d_ile in isos and d_ile != l_ile, True)
same("CP-097 the other two differ at one centre (diastereomers)", len(isos - {l_ile, d_ile}), 2)
meso_test = {Chem.MolToSmiles(m) for m in EnumerateStereoisomers(Chem.MolFromSmiles("CC(Br)CC(Br)C"))}
same("CP-097 control: a symmetric 2,4-dibromopentane does give a meso form (3 isomers)", len(meso_test), 3)
bases = {"guanine": "Nc1nc2[nH]cnc2c(=O)[nH]1", "adenine": "Nc1ncnc2[nH]cnc12", "cytosine": "Nc1cc[nH]c(=O)n1", "thymine": "Cc1c[nH]c(=O)[nH]c1=O", "uracil": "O=c1cc[nH]c(=O)[nH]1"}
rings = {k: rdMolDescriptors.CalcNumRings(Chem.MolFromSmiles(v)) for k, v in bases.items()}
same("CP-098 purines have two rings", (rings["guanine"], rings["adenine"]), (2, 2))
same("CP-098 pyrimidines have one ring", (rings["cytosine"], rings["thymine"], rings["uracil"]), (1, 1, 1))
same("CP-098 answer is guanine–cytosine", ITEMS["CP-098"]["options"][ITEMS["CP-098"]["answer"]], "guanine–cytosine")
gas_moles = {"I": (3, 2), "II": (2, 2), "III": (0, 2)}   # (reactant gas mol, product gas mol)
shift_to_products = [k for k, (r, p) in gas_moles.items() if p < r]
same("CP-100 only I shifts toward products on compression", shift_to_products, ["I"])
same("CP-100 answer is 'I only'", ITEMS["CP-100"]["options"][ITEMS["CP-100"]["answer"]], "I only")

# ================= batch-level checks against the plan =================
disc = Counter(q["discipline"] for q in BATCH["items"])
same("batch mix disciplines (gen chem 6, biochem 7, physics 6, organic 5, biology 1)", disc, Counter({"general chemistry": 6, "biochemistry": 7, "physics": 6, "organic chemistry": 5, "biology": 1}))
same("batch mix skills 10/11/2/2", Counter(q["skill"] for q in BATCH["items"]), Counter({"1": 10, "2": 11, "3": 2, "4": 2}))
same("batch mix stars 4/12/8/1", Counter(q["difficulty"] for q in BATCH["items"]), Counter({2: 4, 3: 12, 4: 8, 5: 1}))
ans = [q["answer"] for q in BATCH["items"]]
same("no letter three in a row", any(ans[i] == ans[i + 1] == ans[i + 2] for i in range(len(ans) - 2)), False)
for L, c in Counter(ans).items():
    same(f"letter {L} share within 20-30% ({c}/25)", 20 <= 100 * c / 25 <= 30, True)
for p in BATCH["passages"]:
    qs = [q for q in BATCH["items"] if q["passage"] == p["id"]]
    skills = {q["skill"] for q in qs}
    same(f"{p['id']} has a Skill 1 item", "1" in skills, True)
    if p["id"] in ("CP-P14", "CP-P15"):
        print(f"note {p['id']} has no Skill 3/4 item by plan (CP-P14 skills 2, 2, 2, 1; CP-P15 skills 1, 1, 2, 2, 2), like CP-P08; recorded in the plan's changelog")
    else:
        same(f"{p['id']} has a Skill 3 or 4 item", bool(skills & {"3", "4"}), True)
same("no stem contains a line break", any("\n" in q["stem"] for q in BATCH["items"]), False)
same("every item has four options", all(sorted(q["options"]) == ["A", "B", "C", "D"] for q in BATCH["items"]), True)
guide = json.load(open("content/mcat/guides/chem_phys.json", encoding="utf-8"))
ids = set()
def walk(o):
    if isinstance(o, dict):
        if "id" in o and "know" in o: ids.add(o["id"])
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(guide)
same("every topic tag exists in the guide", [t for q in BATCH["items"] for t in q["topics"] if t not in ids], [])

print()
print(f"{len(fails)} failures" if fails else "all checks passed")
sys.exit(1 if fails else 0)
