"""Independent numeric and structural checks for pediatric pair 02 (B4-Q03, B4-Q04).

Every number the two items state or depend on is re-derived here from embedded reference data (CDC growth-chart LMS rows,
Fleming 2011 heart-rate and respiratory-rate centiles, the AES 2016 status epilepticus algorithm doses and phases, the ESETT
and RAMPART criteria, the AAP 2017 blood-pressure categories and tables) and compared with what questions/questions4.py says.
Run from the repo root:
    py review/peds_pair_02_check.py        (exit 1 on any mismatch)
"""
import importlib.util
import math
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
fails = []


def check(name, got, want, tol=0.0):
    ok = abs(got - want) <= tol
    print(f"{'ok  ' if ok else 'FAIL'} {name}: computed {got:.6g}, item uses {want:.6g}")
    if not ok:
        fails.append(name)


def truth(name, cond, detail=""):
    print(f"{'ok  ' if cond else 'FAIL'} {name}{(': ' + detail) if detail else ''}")
    if not cond:
        fails.append(name)


spec = importlib.util.spec_from_file_location("questions4", Path(__file__).resolve().parents[1] / "questions" / "questions4.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
Q = {q["id"]: q for q in mod.QUESTIONS4}
q3, q4 = Q["B4-Q03"], Q["B4-Q04"]
v3 = " ".join(q3["vignette"] + q3["after_labs"])
e3 = " ".join(q3["why_correct"]) + " " + " ".join(q3["why_wrong"].values())
v4 = " ".join(q4["vignette"] + q4["after_labs"])
e4 = " ".join(q4["why_correct"]) + " " + " ".join(q4["why_wrong"].values())


def num(pattern, text, group=1):
    m = re.search(pattern, text)
    assert m, pattern
    return float(m.group(group).replace(",", ""))


# ---------- reference data ----------
# CDC growth charts, LMS parameters (cdc.gov/growthcharts/data/zscore, downloaded 2026-10-20): (sex 1 = boys, 2 = girls, age in months).
CDC_LMS = {
    ("wt", 2, 36.5): (-1.024471, 13.9411, 0.119492),
    ("ht", 1, 156.5): (0.816240, 156.4099, 0.050333),
    ("wt", 1, 156.5): (-0.698166, 45.8134, 0.196662),
    ("bmi", 1, 156.5): (-2.329457, 18.4718, 0.134141),
}


def cdc_percentile(kind, sex, agemos, x):
    L, M, S = CDC_LMS[(kind, sex, agemos)]
    z = ((x / M) ** L - 1) / (L * S)
    return z, 100 * 0.5 * (1 + math.erf(z / math.sqrt(2)))


# Fleming S, et al. Lancet 2011;377:1011-1018, web appendix Web Tables 4 and 5 (1st, 10th, 25th, 50th, 75th, 90th, 99th centiles).
FLEMING_HR = {"2-3y": (76, 92, 100, 110, 119, 128, 142), "3-4y": (70, 86, 94, 104, 113, 123, 136), "12-15y": (47, 62, 69, 78, 87, 96, 108)}
FLEMING_RR = {"2-3y": (18, 22, 25, 28, 31, 34, 38), "3-4y": (17, 21, 23, 25, 27, 29, 33), "12-15y": (12, 15, 16, 18, 19, 21, 23)}

# AES 2016 algorithm (Glauser, Epilepsy Curr 2016;16:48-61, dose chart): phases in minutes from seizure onset.
PHASE_INITIAL = (5, 20)
PHASE_SECOND = (20, 40)
PHASE_THIRD = 40
LORAZ_MG_KG, LORAZ_MAX = 0.1, 4
MIDAZ_IM_13_40KG, MIDAZ_IM_OVER_40KG = 5, 10        # RAMPART (Silbergleit, NEJM 2012;366:591) weight bands
LEV_MG_KG, LEV_MAX = 60, 4500
FOS_MG_KG, FOS_MAX = 20, 1500
VPA_MG_KG, VPA_MAX = 40, 3000
PHENOBARB_MG_KG = 15
RECTAL_DIAZ = (0.2, 0.5, 20)
# ESETT (Kapur, NEJM 2019;381:2103): age >= 2 years; minimum adequate benzodiazepine for < 32 kg.
ESETT_MIN_AGE_Y = 2
ESETT_MIDAZ_IM_MG_KG, ESETT_LORAZ_IV_MG_KG, ESETT_WT_SPLIT = 0.3, 0.1, 32
ESETT_N, ESETT_RATES = 384, (47, 45, 46)
ESETT_CHILDREN_N, ESETT_CHILD_RATES = 225, (52, 49, 52)
CHIN_OR_RESP, CHIN_OR_60MIN = 2.9, 3.6                # Chin, Lancet Neurol 2008;7:696

# AAP 2017 CPG (Flynn, Pediatrics 2017;140:e20171904), Table 3, >= 13 years.
STAGE1 = ((130, 139), (80, 89))
# Table 4 (boys), 50th height percentile: 95th-percentile BP at age 12 (152.7 cm) and 13 (160.3 cm).
TABLE4_BOYS_95TH = {12: (121, 78), 13: (125, 78)}
# Table 5 (girls), age 3, 50th height percentile (97.6 cm): 50th, 90th, 95th percentiles.
TABLE5_GIRLS_AGE3 = {"50th": (90, 50), "90th": (104, 62), "95th": (108, 66)}
# AHA 2022 ABPM statement (Flynn, Hypertension 2022;79:e114): adolescent ambulatory cut points.
ABPM_CUTS = {"24h": (125, 75), "wake": (130, 80), "sleep": (110, 65)}
WCH_UPPER_FRACTION = 0.5                             # section 4.7b: up to half of children evaluated for elevated office BP

LB_PER_KG = 1 / 0.45359237


def c_to_f(c):
    return c * 9 / 5 + 32


def lb_oz(kg):
    lb = kg * LB_PER_KG
    return int(lb), (lb - int(lb)) * 16


# ================= B4-Q03 =================
print("== B4-Q03 ==")
age_y = num(r"A (\d+)-year-old girl", v3)
truth("Q03 age at least 1 year inside the ESETT age criterion (>= 2 years)", age_y >= ESETT_MIN_AGE_Y + 1, f"{age_y:g} y")
wt = num(r"She weighs ([\d.]+) kg \((\d+) lb (\d+) oz\)", v3)
lb_s, oz_s = num(r"She weighs ([\d.]+) kg \((\d+) lb (\d+) oz\)", v3, 2), num(r"She weighs ([\d.]+) kg \((\d+) lb (\d+) oz\)", v3, 3)
lb_c, oz_c = lb_oz(wt)
truth("Q03 weight kg -> lb oz", lb_c == lb_s and abs(oz_c - oz_s) <= 0.5, f"{wt} kg = {lb_c} lb {oz_c:.1f} oz; stated {lb_s:g} lb {oz_s:g} oz")
z, pct = cdc_percentile("wt", 2, 36.5, wt)
truth("Q03 weight near the CDC median for girls at 36.5 months (25th-75th percentile)", 25 <= pct <= 75, f"z {z:.2f}, {pct:.0f}th percentile")
truth("Q03 weight inside the RAMPART 13-40 kg band for 5 mg IM midazolam with margin >= 1 kg", 13 + 1 <= wt <= 40 - 1)
truth("Q03 weight below the ESETT 32-kg split, so weight-based minimum doses apply", wt < ESETT_WT_SPLIT)

t = num(r"Temperature is ([\d.]+) C \(([\d.]+) F\)", v3)
t_f = num(r"Temperature is ([\d.]+) C \(([\d.]+) F\)", v3, 2)
check("Q03 temperature C->F", c_to_f(t), t_f, 0.05)
hr = num(r"pulse is (\d+)/min", v3)
rr = num(r"respirations are (\d+)/min", v3)
truth("Q03 pulse within Fleming 1st-99th centiles for both 2-3 y (76-142) and 3-4 y (70-136), above the median (fever, seizure)",
      max(FLEMING_HR["2-3y"][0], FLEMING_HR["3-4y"][0]) <= hr <= min(FLEMING_HR["2-3y"][6], FLEMING_HR["3-4y"][6]) and hr > FLEMING_HR["3-4y"][3], f"{hr:g}/min")
truth("Q03 respirations within Fleming 1st-99th centiles for both 2-3 y (18-38) and 3-4 y (17-33)",
      max(FLEMING_RR["2-3y"][0], FLEMING_RR["3-4y"][0]) <= rr <= min(FLEMING_RR["2-3y"][6], FLEMING_RR["3-4y"][6]), f"{rr:g}/min")
sbp, dbp = num(r"blood pressure is (\d+)/(\d+) mm Hg", v3), num(r"blood pressure is (\d+)/(\d+) mm Hg", v3, 2)
truth("Q03 blood pressure between the 50th and 95th percentiles for a 3-year-old girl of average height (Table 5: 90/50 to 108/66)",
      TABLE5_GIRLS_AGE3["50th"][0] <= sbp < TABLE5_GIRLS_AGE3["95th"][0] and TABLE5_GIRLS_AGE3["50th"][1] <= dbp < TABLE5_GIRLS_AGE3["95th"][1], f"{sbp:g}/{dbp:g}")
glu = num(r"glucose is (\d+) mg/dL", v3)
truth("Q03 glucose well above the AES 60 mg/dL dextrose cutoff (margin >= 20)", glu >= 80)

# timeline: seizure onset t0; arrival at t0 + 24 min; midazolam given 14 min before arrival; reassessment at 30 min
t_arrive = num(r"seizure that began (\d+) minutes ago", v3)
t_midaz_before = num(r"midazolam intramuscularly (\d+) minutes ago", v3)
t_now = num(r"(\d+) minutes after the seizure began", v3)
t_midaz = t_arrive - t_midaz_before
truth("Q03 midazolam was given inside the initial-therapy phase (5-20 min)", PHASE_INITIAL[0] <= t_midaz <= PHASE_INITIAL[1], f"minute {t_midaz:g}")
truth("Q03 lorazepam was given at arrival (minute 20, the end of the initial phase), and reassessment is at minute 26, inside the second-therapy phase (20-40)",
      PHASE_SECOND[0] <= t_arrive <= PHASE_SECOND[1] and PHASE_SECOND[0] <= t_now <= PHASE_SECOND[1] and t_now < PHASE_THIRD, f"arrival {t_arrive:g}, now {t_now:g}")
truth("Q03 'Six minutes later' matches the timeline (30 - 24)", "Six minutes later" in v3 and t_now - t_arrive == 6)

midaz = num(r"gave (\d+) mg of midazolam", v3)
truth("Q03 midazolam 5 mg is the RAMPART dose for 13-40 kg", midaz == MIDAZ_IM_13_40KG)
truth("Q03 midazolam dose meets the ESETT minimum for < 32 kg (0.3 mg/kg IM) with margin", midaz >= ESETT_MIDAZ_IM_MG_KG * wt + 0.5, f"{midaz:g} mg vs {ESETT_MIDAZ_IM_MG_KG * wt:.1f} mg")
check("Q03 midazolam per kg stated in the explanation (0.36 mg/kg)", midaz / wt, 0.36, 0.005)
check("Q03 ESETT minimum midazolam stated in the explanation (4.2 mg)", ESETT_MIDAZ_IM_MG_KG * wt, 4.2, 0.01)
loraz = num(r"lorazepam ([\d.]+) mg \(0\.1 mg/kg\)", v3)
check("Q03 lorazepam = 0.1 mg/kg x weight", LORAZ_MG_KG * wt, loraz, 0.01)
truth("Q03 lorazepam dose below the 4 mg maximum", loraz <= LORAZ_MAX)
truth("Q03 lorazepam dose meets the ESETT minimum (0.1 mg/kg IV)", loraz >= ESETT_LORAZ_IV_MG_KG * wt - 1e-9)
lev = num(r"levetiracetam 60 &#215; 14\.0 = (\d+) mg", e3)
check("Q03 levetiracetam = 60 mg/kg x weight", LEV_MG_KG * wt, lev, 0.5)
truth("Q03 levetiracetam below the 4,500 mg maximum", lev <= LEV_MAX)
fos = num(r"fosphenytoin 20 &#215; 14\.0 = (\d+) mg PE", e3)
check("Q03 fosphenytoin = 20 mg PE/kg x weight", FOS_MG_KG * wt, fos, 0.5)
truth("Q03 fosphenytoin below the 1,500 mg PE maximum", fos <= FOS_MAX)
vpa = num(r"valproate 40 &#215; 14\.0 = (\d+) mg", e3)
check("Q03 valproate = 40 mg/kg x weight", VPA_MG_KG * wt, vpa, 0.5)
truth("Q03 valproate below the 3,000 mg maximum", vpa <= VPA_MAX)
pb = num(r"15 &#215; 14\.0 = (\d+) mg", e3)
check("Q03 phenobarbital = 15 mg/kg x weight", PHENOBARB_MG_KG * wt, pb, 0.5)
truth("Q03 explanation quotes the maximums (4,500 mg; 1,500 mg PE; 3,000 mg; 4 mg) and the rectal diazepam range (0.2 to 0.5 mg/kg, maximum 20 mg)",
      all(s in e3 for s in ["4,500 mg", "1,500 mg PE", "3,000 mg", "maximum 4 mg", "0.2 to 0.5 mg/kg, maximum 20 mg"]))
truth("Q03 explanation quotes the AES phases (5 to 20, 20 to 40, from 40 minutes)", all(s in e3 for s in ["5 to 20 minutes", "20 to 40 minutes", "40 to 60 minutes"]))
truth("Q03 explanation quotes ESETT (384 patients; 47%, 45%, 46%; 225 children; 52%, 49%, 52%; pediatric intubation 33% vs 8% vs 11%)",
      all(s in e3 for s in ["384", "47%, 45%, and 46%", "225 children", "52%, 49%, and 52%", "33%, against 8%", "11% with valproate"]))
truth("Q03 explanation quotes the NLSTEPSS odds ratios (2.9 and 3.6)", "odds ratio 2.9" in e3 and "odds ratio 3.6" in e3)
truth("Q03 vignette never names the second-line drug", "levetiracetam" not in v3.lower() and "fosphenytoin" not in v3.lower())

# ================= B4-Q04 =================
print("== B4-Q04 ==")
age4 = num(r"A (\d+)-year-old boy", v4)
truth("Q04 age 13 or older (adult thresholds, Table 3)", age4 >= 13)
readings = [(int(a), int(b)) for a, b in re.findall(r"(\d{3})/(\d{2}) mm Hg", v4)]
arm = [r for r in readings if r != (148, 82)]
leg = [r for r in readings if r == (148, 82)]
truth("Q04 five arm readings and one leg reading found", len(arm) == 5 and len(leg) == 1, str(readings))
for s, d in arm:
    truth(f"Q04 arm reading {s}/{d} is stage 1 (130-139/80-89) with margins >= 2 above 130, >= 4 below 140, >= 4 above 80, >= 3 below 90",
          STAGE1[0][0] + 2 <= s <= STAGE1[0][1] - 3 and STAGE1[1][0] + 4 <= d <= STAGE1[1][1] - 3)
truth("Q04 leg systolic pressure exceeds every arm systolic pressure (no coarctation gradient)", leg[0][0] > max(s for s, _ in arm), f"leg {leg[0][0]}, max arm {max(s for s, _ in arm)}")
truth("Q04 robustness at age 12: every arm reading is also >= the 95th percentile for a 12-year-old boy of average height (121/78), so he is hypertensive under the percentile rule too (stage 2 by systolic for some readings; that pathway also ends in ABPM at the confirming visit)",
      all(s >= TABLE4_BOYS_95TH[12][0] and d >= TABLE4_BOYS_95TH[12][1] for s, d in arm))
truth("Q04 at age 13 the 95th percentile (125/78) is below 130/80, so the adult thresholds are the lower ones (Table 3 rule)", TABLE4_BOYS_95TH[13][0] < 130 and TABLE4_BOYS_95TH[13][1] < 80)
truth("Q04 three visits: first visit, 2 weeks later, and today (recheck in 1-2 weeks then 3 months); 4 months in all",
      "4 months ago" in v4 and "2 weeks after that" in v4 and "today" in v4)
ht_pct = num(r"(\d+)(?:st|nd|rd|th) percentile for height", v4)
wt_pct = num(r"(\d+)(?:st|nd|rd|th) percentile for weight", v4)
bmi = num(r"BMI is ([\d.]+) kg/m", v4)
bmi_pct = num(r"kg/m<super>2</super> \((\d+)(?:st|nd|rd|th) percentile\)", v4)
HT_CM, WT_KG = 158, 58
z, p = cdc_percentile("ht", 1, 156.5, HT_CM)
check("Q04 height percentile (158 cm at 156.5 months)", round(p), ht_pct, 1)
z, p = cdc_percentile("wt", 1, 156.5, WT_KG)
check("Q04 weight percentile (58 kg)", round(p), wt_pct, 1)
check("Q04 BMI = 58 / 1.58^2", WT_KG / (HT_CM / 100) ** 2, bmi, 0.05)
z, p = cdc_percentile("bmi", 1, 156.5, WT_KG / (HT_CM / 100) ** 2)
check("Q04 BMI percentile", round(p), bmi_pct, 1)
truth("Q04 BMI percentile in the overweight band (85th to < 95th), as the explanation says 'overweight'", 85 <= bmi_pct < 95)
hr4 = num(r"pulse is (\d+)/min", v4)
truth("Q04 pulse within Fleming 12-15-year 10th-90th centiles (62-96)", FLEMING_HR["12-15y"][1] <= hr4 <= FLEMING_HR["12-15y"][5], f"{hr4:g}/min")
truth("Q04 explanation quotes Table 3 (120/80, 120 to 129, 130/80 to 139/89, 140/90)", all(s in e4 for s in ["120/80", "120 to 129", "130/80 to 139/89", "140/90"]))
truth("Q04 explanation quotes KAS 6 with grade C, moderate; KAS 3, 11, 14, 15, 16, 21", all(s in e4 for s in ["KAS 6; grade C, moderate", "[KAS] 3", "KAS 11", "KAS 14", "KAS 15", "KAS 16", "KAS 21"]))
truth("Q04 explanation quotes the AHA 2022 adolescent ABPM cut points (125/75, 130/80, 110/65)", all(s in e4 for s in ["125/75", "130/80 or higher", "110/65"]))
truth("Q04 explanation states 'up to half' for white coat hypertension (section 4.7b)", "up to half" in e4)
truth("Q04 vignette never names the key test", "ambulatory" not in v4.lower())

# ================= pair-level structure =================
print("== pair ==")
for q in (q3, q4):
    opts = q["options"]
    lens = {k: len(v) for k, v in opts.items()}
    key = q["answer"]
    truth(f"{q['id']} five options, key present", sorted(opts) == list("ABCDE") and key in opts)
    truth(f"{q['id']} key is neither the longest nor the shortest option", min(lens.values()) < lens[key] < max(lens.values()), str(lens))
    truth(f"{q['id']} options alphabetical", [opts[k] for k in "ABCDE"] == sorted(opts.values(), key=str.lower))
    truth(f"{q['id']} every distractor has a why-wrong and an error type", set(q["why_wrong"]) == set(q["distractor_error_types"]) == set("ABCDE") - {key})
    truth(f"{q['id']} no absolutes in options", not re.search(r"\b(always|never|all|none)\b", " ".join(opts.values()), re.I))
    truth(f"{q['id']} status reviewed by the independent blind re-solve, verified_on set", q["status"] == "reviewed" and q["reviewed_by"] == "independent blind re-solve" and q["verified_on"] == "2026-10-20")
    words = sum(len(re.sub(r"<[^>]+>", "", p).split()) for p in q["vignette"] + q["after_labs"])
    truth(f"{q['id']} vignette length 120-280 words", 120 <= words <= 280, f"{words} words")
truth("pair: answer letters B and A (block so far D, B, B, A, C, E: no letter more than twice, never three in a row)",
      (q3["answer"], q4["answer"]) == ("B", "A"))
truth("pair: difficulty 4 and 3 (B4-Q03 re-rated from 5 to 4 and B4-Q04 from 4 to 3 at the blind re-solve, 2026-10-20, spec section 3)", (q3["difficulty"], q4["difficulty"]) == (4, 3))

print()
if fails:
    print(f"{len(fails)} check(s) FAILED:")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("all checks passed")
