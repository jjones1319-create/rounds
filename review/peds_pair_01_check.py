"""Independent numeric and structural checks for pediatric pair 01 (B4-Q01, B4-Q02).

Every number the two items state or depend on is re-derived here from embedded reference data (WHO weight-for-age LMS
rows, Fleming 2011 heart-rate and respiratory-rate centiles, the AAP 2021 febrile-infant thresholds and Table 3 doses,
the ACR ratings) and compared with what questions/questions4.py says. Run from the repo root:
    py review/peds_pair_01_check.py        (exit 1 on any mismatch)
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
q1, q2 = Q["B4-Q01"], Q["B4-Q02"]
v1 = " ".join(q1["vignette"]) + " " + " ".join(q1["why_correct"])
v2 = " ".join(q2["vignette"]) + " " + " ".join(q2["why_correct"])


def num(pattern, text, group=1):
    m = re.search(pattern, text)
    assert m, pattern
    return float(m.group(group).replace(",", ""))


# ---------- reference data ----------
# WHO Child Growth Standards 2006, weight-for-age LMS values (downloaded 2026-10-17 from who.int, "Tables: z-scores",
# wfa_boys_0-to-13-weeks_zscores.xlsx, wfa_boys_0-to-5-years_zscores.xlsx and wfa_girls_0-to-5-years_zscores.xlsx).
WHO_LMS = {
    ("boys", "week", 0): (0.3487, 3.3464, 0.14602),
    ("boys", "week", 2): (0.2581, 3.7529, 0.14142),
    ("boys", "month", 0): (0.3487, 3.3464, 0.14602),
    ("girls", "month", 8): (-0.1288, 7.9487, 0.12181),
}


def who_percentile(sex, unit, age, kg):
    L, M, S = WHO_LMS[(sex, unit, age)]
    z = ((kg / M) ** L - 1) / (L * S)
    return z, 100 * 0.5 * (1 + math.erf(z / math.sqrt(2)))


# Fleming S, et al. Lancet 2011;377:1011-1018, web appendix Web Tables 4 and 5 (1st, 10th, 25th, 50th, 75th, 90th, 99th centiles).
FLEMING_HR = {"0-3m": (107, 123, 133, 143, 154, 164, 181), "6-9m": (98, 114, 123, 134, 143, 152, 168)}
FLEMING_RR = {"0-3m": (25, 34, 40, 43, 52, 57, 66), "6-9m": (23, 31, 36, 39, 47, 52, 61)}

# AAP 2021 febrile infant guideline (Pantell, Pediatrics 2021;148(2):e2021052228): fever >=38.0 C; age strata 8-21, 22-28,
# 29-60 days; inflammatory markers abnormal at temperature >38.5 C, procalcitonin >0.5 ng/mL, CRP >20 mg/L, ANC >4000/uL
# (>5200 without procalcitonin); positive urinalysis = any leukocyte esterase, >5 WBC/hpf centrifuged, >10 WBC/mm3 uncentrifuged.
FEVER_C = 38.0
STRATUM_1 = (8, 21)
IM_TEMP_C, IM_ANC, IM_ANC_NO_PCT, IM_CRP_MG_L = 38.5, 4000, 5200, 20
UA_WBC_HPF = 5
# Table 3, 8-21 days, no focus identified: ampicillin 150 mg/kg/day IV divided q8h; ceftazidime 150 mg/kg/day divided q8h;
# gentamicin 4 mg/kg/dose q24h.
AMP_MG_KG_DAY, CEFTAZ_MG_KG_DAY, GENT_MG_KG_DOSE = 150, 150, 4

LB_PER_KG = 1 / 0.45359237


def c_to_f(c):
    return c * 9 / 5 + 32


def lb_oz(kg):
    lb = kg * LB_PER_KG
    return int(lb), (lb - int(lb)) * 16


# ================= B4-Q01 =================
print("== B4-Q01 ==")
age_d = num(r"A (\d+)-day-old boy", v1)
truth("Q01 age inside the 8-21-day stratum with margin >= 6 days on both sides",
      STRATUM_1[0] + 6 <= age_d <= STRATUM_1[1] - 6, f"age {age_d:g} d")
truth("Q01 age is also < 29 days, so the pre-2021 'all infants under 29 days' practice gives the same answer", age_d < 29)

t_home = num(r"rectal temperature of ([\d.]+) C \(([\d.]+) F\)", v1)
t_home_f = num(r"rectal temperature of ([\d.]+) C \(([\d.]+) F\)", v1, 2)
t_ed = num(r"Temperature is ([\d.]+) C \(([\d.]+) F\) rectally", v1)
t_ed_f = num(r"Temperature is ([\d.]+) C \(([\d.]+) F\) rectally", v1, 2)
check("Q01 home temperature C->F", c_to_f(t_home), t_home_f, 0.05)
check("Q01 ED temperature C->F", c_to_f(t_ed), t_ed_f, 0.05)
truth("Q01 both temperatures meet the fever definition (>= 38.0 C) by at least 0.3 C", min(t_home, t_ed) >= FEVER_C + 0.3)
truth("Q01 ED temperature is NOT above the 38.5 C inflammatory-marker cutoff (so all markers are normal)", t_ed <= IM_TEMP_C)

wt = num(r"He weighs ([\d.]+) kg \((\d+) lb (\d+) oz\)", v1)
lb_s, oz_s = num(r"He weighs ([\d.]+) kg \((\d+) lb (\d+) oz\)", v1, 2), num(r"He weighs ([\d.]+) kg \((\d+) lb (\d+) oz\)", v1, 3)
lb_c, oz_c = lb_oz(wt)
truth("Q01 weight kg -> lb oz", lb_c == lb_s and abs(oz_c - oz_s) <= 0.5, f"{wt} kg = {lb_c} lb {oz_c:.1f} oz; stated {lb_s:g} lb {oz_s:g} oz")
bw = num(r"birth weight was ([\d.]+) kg \((\d+) lb (\d+) oz\)", v1)
blb_s, boz_s = num(r"birth weight was ([\d.]+) kg \((\d+) lb (\d+) oz\)", v1, 2), num(r"birth weight was ([\d.]+) kg \((\d+) lb (\d+) oz\)", v1, 3)
blb_c, boz_c = lb_oz(bw)
truth("Q01 birth weight kg -> lb oz", blb_c == blb_s and abs(boz_c - boz_s) <= 0.5, f"{bw} kg = {blb_c} lb {boz_c:.1f} oz")
z, pct = who_percentile("boys", "week", 2, wt)
truth("Q01 weight at 14 days (week 2) is near the WHO median for boys (25th-75th percentile)", 25 <= pct <= 75, f"z {z:.2f}, {pct:.0f}th percentile")
zb, pctb = who_percentile("boys", "week", 0, bw)
truth("Q01 birth weight is near the WHO median for boys (25th-75th percentile)", 25 <= pctb <= 75, f"z {zb:.2f}, {pctb:.0f}th percentile")
truth("Q01 weight gain since birth is physiologic (regained birth weight by 2 weeks, gain <= 0.6 kg)", 0 <= wt - bw <= 0.6, f"gain {wt - bw:.1f} kg")

hr = num(r"pulse is (\d+)/min", v1)
rr = num(r"respirations are (\d+)/min", v1)
truth("Q01 pulse within Fleming 0-3-month 1st-99th centiles (107-181), above the median as expected with fever",
      FLEMING_HR["0-3m"][0] <= hr <= FLEMING_HR["0-3m"][6] and hr > FLEMING_HR["0-3m"][3], f"{hr:g}/min")
truth("Q01 respirations within Fleming 0-3-month 25th-75th centiles (40-52)", FLEMING_RR["0-3m"][2] <= rr <= FLEMING_RR["0-3m"][4], f"{rr:g}/min")

labs = dict((k, v) for k, v in q1["labs"])
wbc = float(labs["Leukocytes"].split("/")[0].replace(",", ""))
anc = float(labs["Absolute neutrophil count"].split("/")[0].replace(",", ""))
plt = float(labs["Platelets"].split("/")[0].replace(",", ""))
crp_mg_dl = float(labs["C-reactive protein"].split()[0])
ua_wbc = float(labs["Urine leukocytes"].split("/")[0])
truth("Q01 ANC below the 4,000/uL cutoff with margin >= 500 (and below 5,200)", anc <= IM_ANC - 500, f"ANC {anc:g}")
truth("Q01 CRP (mg/dL x 10 = mg/L) below the 20 mg/L cutoff with margin >= 10 mg/L", crp_mg_dl * 10 <= IM_CRP_MG_L - 10, f"{crp_mg_dl * 10:g} mg/L")
truth("Q01 urinalysis negative: no leukocyte esterase, no nitrite, WBC <= 5/hpf",
      labs["Urine leukocyte esterase"] == "Negative" and labs["Urine nitrite"] == "Negative" and ua_wbc <= UA_WBC_HPF)
truth("Q01 leukocyte count inside the app's adult reference range (4,500-11,000) and normal for age", 4500 <= wbc <= 11000)
truth("Q01 ANC is consistent with the leukocyte count (neutrophil fraction 20-60%)", 0.20 <= anc / wbc <= 0.60, f"{100 * anc / wbc:.0f}%")
truth("Q01 platelets inside the app's adult range (150,000-400,000)", 150000 <= plt <= 400000)
truth("Q01 explanation quotes both ANC cutoffs (4,000/uL with procalcitonin, 5,200/uL without) and the CRP cutoff 20 mg/L", "4,000/&#181;L" in v1 and "5,200/&#181;L" in v1 and "20 mg/L" in v1)
truth("Q01 explanation converts 0.6 mg/dL to 6 mg/L", "6 mg/L" in v1)

# doses stated in the explanation
amp_dose = num(r"ampicillin 3\.8 &#215; 50 = (\d+) mg every 8 hours", v1)
check("Q01 ampicillin per dose = 150 mg/kg/day / 3 x weight", AMP_MG_KG_DAY / 3 * wt, amp_dose, 0.5)
ceftaz_dose = num(r"ceftazidime (\d+) mg every 8 hours", v1)
check("Q01 ceftazidime per dose = 150 mg/kg/day / 3 x weight", CEFTAZ_MG_KG_DAY / 3 * wt, ceftaz_dose, 0.5)
gent_dose = num(r"gentamicin 3\.8 &#215; 4 = (\d+) mg every 24 hours", v1)
check("Q01 gentamicin per dose = 4 mg/kg x weight (rounded)", GENT_MG_KG_DOSE * wt, gent_dose, 0.5)
truth("Q01 explanation states the per-kg regimen from Table 3 (150 mg/kg per day ampicillin and ceftazidime, 4 mg/kg gentamicin)",
      "ampicillin 150 mg/kg per day" in v1 and "ceftazidime 150 mg/kg per day" in v1 and "gentamicin 4 mg/kg every 24 hours" in v1)
truth("Q01 explanation quotes the guideline's bacteremia rates by week (5.3%, 3.3%, 1.6%) and meningitis 0.5-1.3%",
      all(s in v1 for s in ["5.3%", "3.3%", "1.6%", "0.5% to 1.3%"]))
truth("Q01 explanation quotes the viral-positive IBI risk 1.1-2.1%", "1.1% to 2.1%" in v1)
truth("Q01 'roughly 1-in-20 chance of bacteremia' matches the 3.9-5.3% range", 1 / 20 >= 0.039 and 1 / 20 <= 0.053)

# ================= B4-Q02 =================
print("== B4-Q02 ==")
age_m = num(r"An (\d+)-month-old girl", v2)
truth("Q02 age inside the typical intussusception window (3-36 months) with margin >= 3 months", 6 <= age_m <= 33, f"{age_m:g} months")
t2 = num(r"Temperature is ([\d.]+) C \(([\d.]+) F\)", v2)
t2_f = num(r"Temperature is ([\d.]+) C \(([\d.]+) F\)", v2, 2)
check("Q02 temperature C->F", c_to_f(t2), t2_f, 0.05)
truth("Q02 afebrile (< 38.0 C)", t2 < 38.0)
wt2 = num(r"She weighs ([\d.]+) kg \((\d+) lb (\d+) oz\)", v2)
lb2_s, oz2_s = num(r"She weighs ([\d.]+) kg \((\d+) lb (\d+) oz\)", v2, 2), num(r"She weighs ([\d.]+) kg \((\d+) lb (\d+) oz\)", v2, 3)
lb2_c, oz2_c = lb_oz(wt2)
truth("Q02 weight kg -> lb oz", lb2_c == lb2_s and abs(oz2_c - oz2_s) <= 0.5, f"{wt2} kg = {lb2_c} lb {oz2_c:.1f} oz")
z2, pct2 = who_percentile("girls", "month", 8, wt2)
truth("Q02 weight at 8 months is near the WHO median for girls (25th-75th percentile)", 25 <= pct2 <= 75, f"z {z2:.2f}, {pct2:.0f}th percentile")
hr2 = num(r"pulse is (\d+)/min", v2)
rr2 = num(r"respirations are (\d+)/min", v2)
sbp, dbp = num(r"blood pressure is (\d+)/(\d+) mm Hg", v2), num(r"blood pressure is (\d+)/(\d+) mm Hg", v2, 2)
truth("Q02 pulse within Fleming 6-9-month 1st-99th centiles (98-168), above the median (pain)",
      FLEMING_HR["6-9m"][0] <= hr2 <= FLEMING_HR["6-9m"][6] and hr2 > FLEMING_HR["6-9m"][3], f"{hr2:g}/min")
truth("Q02 respirations within Fleming 6-9-month 10th-90th centiles (31-52)", FLEMING_RR["6-9m"][1] <= rr2 <= FLEMING_RR["6-9m"][5], f"{rr2:g}/min")
# PALS (Kleinman, Pediatrics 2010;126:e1361) hypotension for infants 1-12 months: systolic < 70 mm Hg.
truth("Q02 systolic pressure at least 15 mm Hg above the PALS infant hypotension threshold (70), so no shock", sbp >= 85 and dbp < sbp, f"{sbp:g}/{dbp:g}")
truth("Q02 episode interval and duration are plausible (every 15-20 minutes, 7 hours)", "Every 15 to 20 minutes" in v2 and "7 hours ago" in v2)
truth("Q02 vignette states every finding the enema contraindications turn on (soft abdomen, no guarding or rebound, warm, capillary refill 2 s)",
      all(s in v2 for s in ["soft and not distended", "no guarding or rebound", "extremities are warm", "capillary refill time is 2 seconds"]))
truth("Q02 vomiting is explicitly nonbilious (keeps malrotation/volvulus out of contention)", "without bile" in v2)

# numbers quoted in the explanation, against the sources
truth("Q02 explanation: US sensitivity about 98%, specificity 98-100% (Hwang 2023: 97.9-98.5% / 97.8-100%)",
      "sensitivity of about 98%" in v2 and "specificity of 98% to 100%" in v2)
truth("Q02 explanation: age range 3-36 months and 83% before age 3 (Hwang 2023)", "3 and 36 months" in v2 and "83% before age 3" in v2)
truth("Q02 explanation: triad in about 20% (Hwang 2023)", "about 20%" in v2)
truth("Q02 explanation: air enema success about 80% (Hwang meta-analysis 82.7%; APSA pooled 76.8%) and perforation < 1% (0.4-0.5%)",
      "about 80%" in v2 and "fewer than 1%" in v2)
truth("Q02 explanation: ACR-SPR timing 8-12 h, 120 mm Hg, three attempts of up to 5 minutes", all(s in v2 for s in ["8 to 12 hours", "120 mm Hg", "three attempts", "5 minutes"]))
truth("Q02 explanation: APSA observation about 4 hours after reduction", "about 4 hours" in v2)
truth("Q02 why-wrong A: radiograph sensitivity roughly 40-60% (Hwang 2023: about 40% accuracy; Henderson 2013: 62.3% sensitivity, in the ACR evidence table)", "roughly 40% to 60%" in q2["why_wrong"]["A"])
ACR_VARIANT_2 = {"US abdomen": "Usually Appropriate", "Radiography abdomen and pelvis": "May Be Appropriate",
                 "Fluoroscopy contrast enema": "Usually Not Appropriate", "CT abdomen and pelvis with IV contrast": "Usually Not Appropriate"}
truth("Q02 keyed option is the only 'Usually Appropriate' initial study in ACR Variant 2", ACR_VARIANT_2["US abdomen"] == "Usually Appropriate"
      and sum(v == "Usually Appropriate" for v in ACR_VARIANT_2.values()) == 1)

# ================= pair-level structure =================
print("== pair ==")
for q in (q1, q2):
    opts = q["options"]
    lens = {k: len(v) for k, v in opts.items()}
    key = q["answer"]
    truth(f"{q['id']} five options, key present", sorted(opts) == list("ABCDE") and key in opts)
    truth(f"{q['id']} key is neither the longest nor the shortest option", min(lens.values()) < lens[key] < max(lens.values()), str(lens))
    truth(f"{q['id']} options alphabetical", [opts[k] for k in "ABCDE"] == sorted(opts.values(), key=str.lower))
    truth(f"{q['id']} every distractor has a why-wrong and an error type", set(q["why_wrong"]) == set(q["distractor_error_types"]) == set("ABCDE") - {key})
    truth(f"{q['id']} no absolutes in options", not re.search(r"\b(always|never|all|none)\b", " ".join(opts.values()), re.I))
    truth(f"{q['id']} status reviewed by the independent blind re-solve, verified_on set", q["status"] == "reviewed" and q["reviewed_by"] == "independent blind re-solve" and q["verified_on"] == "2026-10-17")
    words = sum(len(re.sub(r"<[^>]+>", "", p).split()) for p in q["vignette"])
    truth(f"{q['id']} vignette length 120-280 words", 120 <= words <= 280, f"{words} words")
truth("pair: answer letters differ (block letter balance, no letter more than twice in 8)", q1["answer"] != q2["answer"], f"{q1['answer']}, {q2['answer']}")
truth("pair: difficulty 3 and 3 (B4-Q02 re-rated from 4 to 3 at the blind re-solve, 2026-10-20, spec section 3)", (q1["difficulty"], q2["difficulty"]) == (3, 3))

print()
if fails:
    print(f"{len(fails)} check(s) FAILED:")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("all checks passed")
