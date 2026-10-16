"""Independent numeric and structural checks for Chem/Phys batch 1 (CP-001 to CP-025).

Every number quoted in content/mcat/chem_phys/batch_01.json is re-derived here from the passage constants, separately
from the explanations, and compared with the value the item uses. Structures and formulas are checked with RDKit.
Run:  py review/chem_phys_batch_01_check.py     (exit 1 on any mismatch)
"""
import json
import math
import sys

fails = []


def check(name, got, want, tol=0.02):
    ok = abs(got - want) <= tol * max(abs(want), 1e-12)
    print(f"{'ok  ' if ok else 'FAIL'} {name}: computed {got:.6g}, item uses {want:.6g}")
    if not ok:
        fails.append(name)


# ---------- CP-P01  stenosed carotid artery ----------
rho, eta = 1060.0, 3.0e-3            # kg/m^3, Pa.s (passage values)
r1, r2 = 3.0e-3, 1.5e-3              # m
v1, v1_peak = 0.30, 0.75             # m/s, measured proximal
mmHg = 133.322                       # Pa (passage rounds to 133)
v2 = v1 * (r1 / r2) ** 2             # continuity
v2_peak = v1_peak * (r1 / r2) ** 2
check("CP-001 v2 from continuity (m/s)", v2, 1.2)
check("CP-001 distractor v1*(r1/r2)", v1 * (r1 / r2), 0.60)
check("CP-001 distractor v1*(r1/r2)^4", v1 * (r1 / r2) ** 4, 4.8)
check("CP-001 distractor v1/(r1/r2)^2", v1 / (r1 / r2) ** 2, 0.075)
dP_bern = 0.5 * rho * (v2 ** 2 - v1 ** 2)
check("CP-002 Bernoulli drop (Pa)", dP_bern, 720, 0.01)
check("CP-002 Bernoulli drop (mmHg)", dP_bern / mmHg, 5.4, 0.01)
check("CP-002 distractor 0.5 rho (v2-v1)^2 (Pa)", 0.5 * rho * (v2 - v1) ** 2, 430, 0.01)
L = 0.010                            # stenosis length, m
dP_visc = 8 * eta * L * v2 / r2 ** 2  # Poiseuille per unit area: dP = 8 eta L v / r^2
check("CP-002 distractor viscous loss along 10 mm (Pa)", dP_visc, 130, 0.02)
check("CP-002 distractor rho g (20 mm) (Pa)", rho * 9.8 * 0.020, 210, 0.02)
check("chart: entry pressure 90.0 - 5.4 (mmHg)", 90.0 - dP_bern / mmHg, 84.6, 0.001)
check("chart: pressure at x = 25 mm, half the viscous loss (mmHg)", 84.6 - 0.5 * dP_visc / mmHg, 84.1, 0.001)
check("chart: exit pressure at x = 30 mm, 84.6 - viscous (mmHg)", 84.6 - dP_visc / mmHg, 83.6, 0.001)
# The chart points themselves, read from the content file: Poiseuille gives a linear decline along the segment.
BATCH = json.load(open("content/mcat/chem_phys/batch_01.json", encoding="utf-8"))
fig1 = [f for p in BATCH["passages"] if p["id"] == "CP-P01" for f in p["figures"] if f["id"] == "fig1"][0]["data"]["series"][0]["points"]
want = [[0, 90.0], [10, 90.0], [19, 90.0], [20, 84.6], [25, 84.1], [30, 83.6], [31, 87.0], [40, 87.0], [50, 87.0]]
print(f"{'ok  ' if fig1 == want else 'FAIL'} chart: Figure 1 points in batch_01.json match the derived values")
if fig1 != want:
    fails.append("Figure 1 points")
check("CP-003 Poiseuille flow ratio (r2/r1)^4", (r2 / r1) ** 4, 1 / 16, 1e-9)


def Re(v, r):
    return 2 * rho * v * r / eta


check("CP-004 Re stenosis peak", Re(v2_peak, r2), 3180, 0.01)
check("CP-004 Re stenosis mean", Re(v2, r2), 1270, 0.01)
check("CP-004 Re proximal peak", Re(v1_peak, r1), 1590, 0.01)
Q = math.pi * r1 ** 2 * v1
check("flow rate (mL/min) plausibility", Q * 6e7, 509, 0.01)

# ---------- CP-P02  metabolic acidosis ----------
pK, alpha = 6.1, 0.03


def hh(hco3, pco2):
    return pK + math.log10(hco3 / (alpha * pco2))


check("P02 patient 1 pH", hh(24, 40), 7.40, 0.001)
check("P02 patient 2 pH", hh(6, 20), 7.10, 0.001)
check("CP-006 patient 3 pH", hh(12, 80), 6.80, 0.001)
check("CP-006 distractor no 0.03 conversion", pK + math.log10(12 / 80), 5.28, 0.002)
check("CP-006 distractor PCO2 read as 40", hh(12, 40), 7.10, 0.001)
check("CP-007 neutral pH at 37 C, Kw 2.4e-14", -math.log10(math.sqrt(2.4e-14)), 6.81, 0.002)
# Titration of 20 mmol/L dissolved CO2 ("carbonic acid", apparent pK1' 6.1, pK2' 10.0) with NaOH in a sealed cell,
# volume change ignored (concentrated titrant). Charge balance solved by bisection.
C, K1, K2, Kw = 0.020, 10 ** -6.1, 10 ** -10.0, 2.4e-14


def ph_at(na):
    def f(ph):
        h = 10 ** -ph
        d = h * h + K1 * h + K1 * K2
        hco3, co3 = C * K1 * h / d, C * K1 * K2 / d
        return na + h - hco3 - 2 * co3 - Kw / h
    lo, hi = 1.0, 13.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


VOLS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 9.5, 10, 10.5, 11, 12]
curve = [(v, round(ph_at(0.020 * v / 10.0), 2)) for v in VOLS]
print("titration curve (mL NaOH, pH):", curve)
check("CP-008 pH at half-equivalence (5.0 mL)", ph_at(0.010), 6.1, 0.003)
check("CP-008 distractor pH at equivalence", ph_at(0.020), 8.05, 0.005)

# ---------- CP-P03  kinase inhibitor screen ----------
Vmax, Km, Km_app = 120.0, 20.0, 60.0
S = [5, 10, 20, 40, 200, 2000]
v0 = [Vmax * s / (Km + s) for s in S]
vi = [Vmax * s / (Km_app + s) for s in S]
print("MM table no inhibitor:", [round(x, 1) for x in v0], " with inhibitor:", [round(x, 1) for x in vi])
for s, a, b in zip(S, v0, [24, 40, 60, 80, 109, 119]):
    check(f"CP-011 v0 at {s} uM", a, b, 0.006)
for s, a, b in zip(S, vi, [9, 17, 30, 48, 92, 117]):
    check(f"P03 inhibited v at {s} uM", a, b, 0.03)
check("CP-011 Km is [S] at Vmax/2", Vmax * Km / (Km + Km), Vmax / 2, 1e-9)
check("CP-012 y-intercept 1/Vmax (min/nmol)", 1 / Vmax, 1 / 120, 1e-9)
check("CP-012 x-intercept -1/Km (1/uM)", -1 / Km, -0.05, 1e-9)
check("CP-013 Km_app/Km = 1 + [I]/Ki with [I] = 2 Ki", 1 + 2, Km_app / Km, 1e-9)
check("CP-013 inhibited Km from v=30 at 20 uM", Vmax * 20 / 30 - 20, 60, 1e-9)
I = 20.0                             # inhibitor concentration, uM
check("CP-013 Ki = [I]/(Km_app/Km - 1) (uM)", I / (Km_app / Km - 1), 10, 1e-9)
check("CP-013 distractor Km_app - Km (uM)", Km_app - Km, 40, 1e-9)
check("CP-013 distractor Ki = [I] would need Km_app/Km = 2", Km * (1 + I / I), 40, 1e-9)

# ---------- CP-P04  FDG PET ----------
T = 110.0                            # min (NNDC NuDat: 109.77)
for t, a in [(0, 800), (110, 400), (220, 200), (330, 100)]:
    check(f"P04 vial activity at {t} min", 800 * 0.5 ** (t / T), a, 1e-9)
for t, a in [(110, 600), (220, 300), (330, 150), (440, 75)]:
    check(f"CP-016 second vial (1200 MBq) at {t} min", 1200 * 0.5 ** (t / T), a, 1e-9)
# Crossing times, in minutes after 08:00: 12:10 is 250 min, 11:05 is 185 min, 13:30 is 330 min.
check("CP-016 second vial falls to 250 MBq (min after 08:00; 12:10)", T * math.log2(1200 / 250), 250, 0.01)
check("CP-016 distractor first vial falls to 250 MBq (11:05)", T * math.log2(800 / 250), 185, 0.01)
check("CP-016 quarter half-life estimate (min)", T / 4, 28, 0.02)
check("CP-016 (1/2)^(1/4) vs 250/300", 0.5 ** 0.25, 250 / 300, 0.01)
tab = [f for p in BATCH["passages"] if p["id"] == "CP-P04" for f in p["figures"] if f["type"] == "table"][0]["data"]["rows"]
ok = [(int(r[1]), int(r[2])) for r in tab] == [(0, 800), (110, 400), (220, 200), (330, 100)]
print(f"{'ok  ' if ok else 'FAIL'} chart: CP-P04 Table 1 rows in batch_01.json match")
if not ok:
    fails.append("CP-P04 table")
check("CP-017 lambda (1/min)", math.log(2) / T, 6.3e-3, 0.01)
check("CP-017 fraction after 55 min", 0.5 ** (55 / T), 0.71, 0.005)
check("CP-017 distractor 1/T", 1 / T, 9.1e-3, 0.01)
E = 511e3                            # eV
lam = 1240 / E                       # nm, with hc = 1240 eV.nm
check("CP-019 wavelength (m)", lam * 1e-9, 2.4e-12, 0.02)
h, c, eV = 6.626e-34, 2.998e8, 1.602e-19
check("CP-019 wavelength from h c / E (m)", h * c / (E * eV), 2.4e-12, 0.02)
check("CP-019 hc in eV nm", h * c / eV * 1e9, 1240, 0.001)
check("CP-019 distractor keV read as eV (m)", 1240 / 511 * 1e-9, 2.4e-9, 0.02)
check("CP-019 distractor energy halved (m)", 1240 / 255.5e3 * 1e-9, 4.9e-12, 0.02)

# ---------- standalones ----------
# CP-020: Pa = N/m^2 = (kg m s^-2) / m^2 = kg m^-1 s^-2  (NIST SP 811 Table 3)
# CP-024: rate = k [A]^m [B]^n from the three trials
trials = [((0.10, 0.10), 2.0e-4), ((0.20, 0.10), 8.0e-4), ((0.20, 0.20), 1.6e-3)]
m = math.log(trials[1][1] / trials[0][1]) / math.log(2)
n = math.log(trials[2][1] / trials[1][1]) / math.log(2)
check("CP-024 order in A", m, 2, 1e-9)
check("CP-024 order in B", n, 1, 1e-9)
k = trials[0][1] / (0.10 ** 2 * 0.10)
check("CP-024 k (M^-2 s^-1)", k, 0.20, 1e-9)
# CP-022: formal charges in a nitrate resonance structure, FC = V - N - B/2
check("CP-022 N: 5 - 0 - 8/2", 5 - 0 - 8 / 2, 1, 1e-9)
check("CP-022 O double: 6 - 4 - 4/2", 6 - 4 - 4 / 2, 0, 1e-9)
check("CP-022 O single: 6 - 6 - 2/2", 6 - 6 - 2 / 2, -1, 1e-9)

# ---------- RDKit: structures, formulas, formal charges, CIP labels ----------
try:
    from rdkit import Chem, RDLogger
    from rdkit.Chem import rdMolDescriptors, FindMolChiralCenters, GetPeriodicTable
    RDLogger.DisableLog("rdApp.*")

    def mol(smi):
        mm = Chem.MolFromSmiles(smi)
        assert mm is not None, smi
        return mm

    def formula(smi):
        return rdMolDescriptors.CalcMolFormula(mol(smi))

    def fcs(smi):
        return [(a.GetSymbol(), a.GetFormalCharge()) for a in mol(smi).GetAtoms()]

    tests = [
        ("nitrate resonance structure", "[O-][N+](=O)[O-]", "NO3-", [("O", -1), ("N", 1), ("O", 0), ("O", -1)]),
        ("prostaglandin E2 (C20H32O5)", "CCCCC[C@H](O)/C=C/[C@H]1[C@H](O)CC(=O)[C@@H]1C/C=C\\CCCC(=O)O", "C20H32O5", None),
        ("arachidonic acid (C20H32O2)", "CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)O", "C20H32O2", None),
        ("L-valine (C5H11NO2)", "CC(C)[C@@H](C(=O)O)N", "C5H11NO2", None),
        ("L-serine", "C([C@@H](C(=O)O)N)O", "C3H7NO3", None),
        ("L-aspartate (neutral form)", "C([C@@H](C(=O)O)N)C(=O)O", "C4H7NO4", None),
        ("L-lysine", "C(CCN)C[C@@H](C(=O)O)N", "C6H14N2O2", None),
        ("iodide ion", "[I-]", "I-", [("I", -1)]),
    ]
    for name, smi, want_formula, want_fc in tests:
        f = formula(smi)
        ok = f == want_formula and (want_fc is None or fcs(smi) == want_fc)
        print(f"{'ok  ' if ok else 'FAIL'} RDKit {name}: {f} {fcs(smi) if want_fc else ''}")
        if not ok:
            fails.append(name)
    # Natural L-amino acids are S by the CIP rules (cysteine excepted); CP-025 names L-valine.
    for name, smi in [("L-valine", "CC(C)[C@@H](C(=O)O)N"), ("L-serine", "C([C@@H](C(=O)O)N)O"),
                      ("L-aspartate", "C([C@@H](C(=O)O)N)C(=O)O"), ("L-lysine", "C(CCN)C[C@@H](C(=O)O)N")]:
        cc = FindMolChiralCenters(mol(smi), useLegacyImplementation=False)
        ok = bool(cc) and cc[0][1] == "S"
        print(f"{'ok  ' if ok else 'FAIL'} RDKit {name} CIP label: {cc}")
        if not ok:
            fails.append(name + " CIP")
    # PGE2: 5Z,13E double bonds and 8R,11R,12R,15S centres (PubChem CID 5280360)
    pge2 = mol("CCCCC[C@H](O)/C=C/[C@H]1[C@H](O)CC(=O)[C@@H]1C/C=C\\CCCC(=O)O")
    cc = dict(FindMolChiralCenters(pge2, useLegacyImplementation=False))
    stereo = sorted(str(b.GetStereo()) for b in pge2.GetBonds() if b.GetBondType() == Chem.BondType.DOUBLE and b.GetStereo() != Chem.BondStereo.STEREONONE)
    print("RDKit PGE2 centres:", sorted(cc.values()), "double bonds:", stereo)
    ok = sorted(cc.values()) == ["R", "R", "R", "S"] and stereo in (["STEREOE", "STEREOZ"], ["STEREOCIS", "STEREOTRANS"])  # 5Z (cis), 13E (trans)
    if not ok:
        fails.append("PGE2 stereo")
    pt = GetPeriodicTable()
    ok = pt.GetNOuterElecs(53) == 7 and pt.GetNOuterElecs(17) == 7 and pt.GetNOuterElecs(35) == 7
    print(f"{'ok  ' if ok else 'FAIL'} RDKit periodic table: Cl, Br and I have 7 outer electrons")
    if not ok:
        fails.append("halogen valence")
except ImportError:
    print("RDKit not installed; structure checks skipped")
    fails.append("rdkit missing")

print("\nALL CHECKS PASSED" if not fails else f"\n{len(fails)} FAILED: {fails}")
sys.exit(1 if fails else 0)
