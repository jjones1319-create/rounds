/* Anatomy figure v2: original stylized drawing with FRONT and BACK views.
   viewBox 0 0 400 920, midline x=200. Paired structures are defined on the patient's RIGHT
   (viewer's left in the front view, x<200) and mirrored. The back view is the same geometry
   flipped horizontally, so the patient's right appears on the viewer's right.
   v: "f" front only (default), "b" back only, "fb" both. post: dashed in front, solid in back.
   bdash: solid in front, dashed in back. */
const FIG = (function () {
  const MX = 200;
  function r(v) { return Math.round(v * 10) / 10; }
  function smooth(p, closed) {
    const n = p.length; if (n < 2) return "";
    const g = (i) => closed ? p[(i + n) % n] : p[Math.max(0, Math.min(n - 1, i))];
    let d = "M" + p[0][0] + " " + p[0][1];
    const last = closed ? n : n - 1;
    for (let i = 0; i < last; i++) {
      const p0 = g(i - 1), p1 = g(i), p2 = g(i + 1), p3 = g(i + 2);
      const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6];
      const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
      d += "C" + r(c1[0]) + " " + r(c1[1]) + " " + r(c2[0]) + " " + r(c2[1]) + " " + r(p2[0]) + " " + r(p2[1]);
    }
    return d + (closed ? "Z" : "");
  }
  const mir = (pts) => pts.map(([x, y]) => [2 * MX - x, y]);
  const shift = (pts, dx, dy) => pts.map(([x, y]) => [x + dx, y + dy]);

  const half = [[200,128],[186,130],[184,150],[178,165],[150,175],[122,182],[108,195],[100,220],[96,250],[90,300],[84,350],[78,400],[70,450],[64,495],[56,520],[50,560],[52,590],[63,598],[72,586],[77,550],[80,505],[90,455],[100,400],[108,355],[116,300],[123,256],[131,240],[136,280],[138,330],[140,375],[133,420],[123,470],[124,520],[130,600],[140,670],[146,720],[145,780],[150,840],[156,876],[150,896],[160,910],[185,910],[187,902],[184,880],[178,840],[173,780],[176,720],[180,680],[186,600],[194,522],[200,506]];
  const fullBody = half.concat(mir(half.slice(1, -1)).reverse());
  const torsoPts = [[178,165],[150,175],[131,240],[136,280],[138,330],[140,375],[133,420],[123,470],[124,520]];
  function torsoX(y) {
    for (let i = 0; i < torsoPts.length - 1; i++) { const a = torsoPts[i], b = torsoPts[i + 1]; if (y >= a[1] && y <= b[1]) return a[0] + (b[0] - a[0]) * ((y - a[1]) / (b[1] - a[1])); }
    return y < 165 ? 184 : 124;
  }

  const S = [];
  const add = (o) => S.push(o);

  /* ===== SKELETON ===== */
  const cerv = [], thor = [], lumb = [];
  for (let i = 0; i < 7; i++) cerv.push({ rect: [194, 121 + i * 7, 12, 5.6, 1.5] });
  for (let i = 0; i < 12; i++) thor.push({ rect: [190.5, 172 + i * 12.6, 19, 10.4, 2] });
  for (let i = 0; i < 5; i++) lumb.push({ rect: [187, 325 + i * 19.4, 26, 16.6, 3] });
  add({ id: "cervical", L: "bone", v: "fb", parts: cerv, fill: "bone" });
  add({ id: "thoracicv", L: "bone", v: "fb", parts: thor, fill: "bone" });
  add({ id: "lumbar", L: "bone", v: "fb", parts: lumb, fill: "bone" });
  add({ id: "sacrum", L: "bone", v: "fb", pts: [[186,424],[214,424],[212,446],[205,466],[200,472],[195,466],[188,446]], fill: "bone" });
  add({ id: "coccyx", L: "bone", v: "fb", pts: [[197,474],[203,474],[201.5,484],[198.5,484]], fill: "bone" });
  add({ id: "scapula", L: "bone", mirror: true, pts: [[124,190],[148,185],[160,191],[152,240],[143,262],[134,236],[124,206]], fill: "bone", op: 0.55 });
  add({ id: "scapula_b", info: "scapula", L: "bone", v: "b", mirror: true, pts: [[126,186],[152,182],[160,190],[158,230],[150,262],[136,268],[128,236],[124,206]], fill: "bone", deco: ["M127 203 C140 199 150 197 158 195"] });
  const xl = [158,148,142,139,138,138,138,139,141,144,148,154];
  const ribFront = [], ribBack = [], cart = [], ribBackSolid = [];
  for (let i = 1; i <= 12; i++) {
    const yv = 170 + 12 * (i - 1), xlat = xl[i - 1], ylat = yv + 14;
    const back = { line: [[196, yv], [(196 + xlat) / 2 + 4, yv + 3], [xlat + 1, ylat - 1]], w: 2.6 };
    ribBack.push(Object.assign({ op: 0.35 }, back)); ribBackSolid.push(Object.assign({}, back, { w: 3.2 }));
    if (i <= 7) {
      const xa = 174, ya = ylat + 18, ys = 188 + 11 * (i - 1);
      ribFront.push({ line: [[xlat + 1, ylat - 1], [xlat + 2, ylat + 8], [(xlat + xa) / 2, ya - 2], [xa, ya]], w: 3.4 });
      cart.push({ line: [[xa, ya], [xa + 9, ya - 6], [192, ys]], w: 2.4 });
    } else if (i <= 10) {
      const xa = [168, 162, 156][i - 8], ya = ylat + 16;
      ribFront.push({ line: [[xlat + 1, ylat - 1], [xlat + 2, ylat + 8], [(xlat + xa) / 2, ya - 2], [xa, ya]], w: 3.2 });
      cart.push({ line: [[xa, ya], [xa + 8, ya - 7], [xa + 14, ya - 14]], w: 2.2 });
    } else ribFront.push({ line: [[xlat + 1, ylat - 1], [xlat + 3, ylat + 6], [xlat + 8, ylat + 11]], w: 3 });
  }
  add({ id: "ribs", L: "bone", mirror: true, parts: ribBack.concat(ribFront), stroke: "bone", noFill: true });
  add({ id: "ribs_b", info: "ribs", L: "bone", v: "b", mirror: true, parts: ribBackSolid.concat(ribFront.map((p) => Object.assign({ op: 0.35 }, p))), stroke: "bone", noFill: true });
  add({ id: "costal", L: "bone", mirror: true, parts: cart, stroke: "cart", noFill: true });
  add({ id: "sternum", L: "bone", parts: [{ pts: [[189,182],[211,182],[208,205],[192,205]] }, { pts: [[193,207],[207,207],[207,286],[200,291],[193,286]] }, { pts: [[196,292],[204,292],[200,305]] }], fill: "bone" });
  add({ id: "clavicle", L: "bone", mirror: true, line: [[193,185],[178,180],[160,185],[142,182],[126,184]], w: 5.5, stroke: "bone" });
  add({ id: "cranium_b", info: "skull_parietal", L: "bone", v: "b", ellipse: [200, 68, 38, 48], fill: "bone", deco: ["M200 24 L200 100", "M166 86 C180 78 220 78 234 86"] });
  add({ id: "occipital", L: "bone", v: "b", pts: [[166,92],[234,92],[237,108],[224,124],[200,129],[176,124],[163,108]], fill: "bone2" });
  add({ id: "skull_parietal", L: "bone", mirror: true, pts: [[162,72],[161,54],[167,38],[177,30],[171,46],[167,62]], fill: "bone2" });
  add({ id: "skull_frontal", L: "bone", pts: [[165,66],[167,45],[181,29],[200,23],[219,29],[233,45],[235,66],[222,61],[200,59],[178,61]], fill: "bone" });
  add({ id: "skull_temporal", L: "bone", v: "fb", mirror: true, pts: [[162,74],[166,70],[170,78],[170,94],[166,102],[161,94],[160,82]], fill: "bone2" });
  add({ id: "skull_zygomatic", L: "bone", mirror: true, pts: [[167,84],[175,85],[181,91],[176,97],[168,97]], fill: "bone" });
  add({ id: "orbit", L: "bone", mirror: true, circle: [184, 75, 10], fill: "hole" });
  add({ id: "skull_maxilla", L: "bone", mirror: true, pts: [[181,88],[193,91],[195,100],[200,106],[200,114],[185,114],[175,105],[176,95]], fill: "bone" });
  add({ id: "skull_nasal", L: "bone", mirror: true, pts: [[195.5,77],[199.5,76],[199.5,90],[194.5,90]], fill: "bone2" });
  add({ id: "nasal_aperture", L: "bone", pts: [[200,90],[205,96],[204,104],[200,106],[196,104],[195,96]], fill: "hole", noTap: true });
  add({ id: "skull_mandible", L: "bone", pts: [[166,98],[169,112],[178,124],[190,130],[200,131],[210,130],[222,124],[231,112],[234,98],[229,100],[223,114],[210,121],[200,122],[190,121],[177,114],[171,100]], fill: "bone" });
  add({ id: "teeth", L: "bone", line: [[184,113],[192,115.5],[200,116],[208,115.5],[216,113]], w: 3, stroke: "tooth", dash: "2.2 0.8", noTap: true });
  add({ id: "hyoid", L: "bone", line: [[191,139],[195,143],[200,144],[205,143],[209,139]], w: 2.8, stroke: "bone" });
  add({ id: "humerus", L: "bone", v: "fb", mirror: true, pts: [[111,195],[120,191],[127,197],[124,208],[114,250],[106,300],[101,338],[106,349],[98,356],[88,356],[81,349],[90,336],[96,298],[104,250],[110,210],[109,201]], fill: "bone" });
  add({ id: "radius", L: "bone", v: "fb", mirror: true, pts: [[85,360],[93,360],[92,368],[86,410],[80,455],[77,484],[76,494],[66,494],[66,486],[71,455],[78,410],[85,368]], fill: "bone" });
  add({ id: "ulna", L: "bone", v: "fb", mirror: true, pts: [[94,356],[104,357],[102,366],[97,410],[90,455],[84,486],[82,494],[77,493],[79,486],[83,455],[89,410],[93,366]], fill: "bone" });
  const carp = []; [[66,497],[70.5,496],[75,496],[79.5,497],[65.5,503],[70,503],[74.5,503],[79,503]].forEach(([x, y]) => carp.push({ rect: [x - 0.5, y, 4.2, 5, 1.2] }));
  add({ id: "carpals", L: "bone", v: "fb", mirror: true, parts: carp, fill: "bone" });
  add({ id: "metacarpals", L: "bone", v: "fb", mirror: true, stroke: "bone", noFill: true, parts: [{ line: [[66,510],[58,529]], w: 2.8 }, { line: [[68,511],[62,547]], w: 2.6 }, { line: [[72,511],[67,549]], w: 2.6 }, { line: [[76,510],[71,548]], w: 2.6 }, { line: [[79,509],[75,545]], w: 2.4 }] });
  add({ id: "hand_phalanges", L: "bone", v: "fb", mirror: true, stroke: "bone", noFill: true, parts: [
    { line: [[57.5,532],[54.5,543]], w: 2.4 }, { line: [[54,545.5],[52.5,553]], w: 2.2 },
    { line: [[61.5,550],[58.5,566]], w: 2.2 }, { line: [[58.2,568.5],[56.8,578]], w: 2 }, { line: [[56.6,580.5],[55.8,587]], w: 1.8 },
    { line: [[66.6,552],[64.8,570]], w: 2.2 }, { line: [[64.6,572.5],[63.8,583]], w: 2 }, { line: [[63.7,585.5],[63.2,592]], w: 1.8 },
    { line: [[70.8,551],[69.6,567]], w: 2.2 }, { line: [[69.5,569.5],[69,579]], w: 2 }, { line: [[68.9,581.5],[68.6,587]], w: 1.8 },
    { line: [[74.6,548],[73.8,561]], w: 2 }, { line: [[73.7,563.5],[73.3,571]], w: 1.8 }, { line: [[73.2,573.5],[73,578]], w: 1.6 }] });
  add({ id: "hipbone", L: "bone", v: "fb", mirror: true, pts: [[190,424],[172,412],[150,408],[136,416],[134,432],[140,450],[146,468],[152,488],[160,503],[170,508],[182,504],[196,494],[197,482],[186,476],[172,474],[162,464],[170,452],[186,442]], fill: "bone" });
  add({ id: "obturator_hole", L: "bone", mirror: true, ellipse: [175, 490, 7, 5.5], fill: "hole", noTap: true });
  add({ id: "femur", L: "bone", v: "fb", mirror: true, parts: [{ pts: [[128,474],[138,471],[146,477],[151,486],[149,500],[153,560],[159,620],[166,652],[174,664],[176,676],[168,684],[160,680],[152,684],[146,676],[150,664],[151,640],[145,580],[139,520],[135,498],[128,490]] }, { circle: [150, 468, 8.5] }], fill: "bone" });
  add({ id: "patella", L: "bone", mirror: true, ellipse: [162, 676, 7.5, 9.5], fill: "bone2" });
  add({ id: "tibia", L: "bone", v: "fb", mirror: true, pts: [[154,690],[178,688],[179,698],[171,712],[170,780],[172,840],[181,861],[177,870],[166,868],[164,850],[162,780],[161,712],[154,700]], fill: "bone" });
  add({ id: "fibula", L: "bone", v: "fb", mirror: true, pts: [[146,694],[154,694],[152,706],[154,780],[160,846],[164,866],[159,872],[155,850],[148,780],[146,706]], fill: "bone" });
  add({ id: "tarsals", L: "bone", mirror: true, fill: "bone", parts: [{ ellipse: [172, 877, 7, 3.6] }, { ellipse: [162, 884, 4.6, 3.2] }, { ellipse: [178.5, 884, 3.8, 2.8] }, { ellipse: [170.5, 886.5, 2.6, 2.4] }, { ellipse: [175, 888, 2.3, 2.2] }, { ellipse: [181, 888.5, 2.3, 2.3] }] });
  add({ id: "metatarsals", L: "bone", mirror: true, stroke: "bone", noFill: true, parts: [{ line: [[181,890],[183,899]], w: 2.6 }, { line: [[176,890.5],[176,900]], w: 2.2 }, { line: [[171,890.5],[170,900]], w: 2.2 }, { line: [[166,889.5],[164,899]], w: 2.2 }, { line: [[161,888.5],[157.5,897]], w: 2.2 }] });
  add({ id: "foot_phalanges", L: "bone", mirror: true, stroke: "bone", noFill: true, parts: [{ line: [[183.2,901.5],[184,908]], w: 2.6 }, { line: [[176,902],[176,907]], w: 2 }, { line: [[169.8,902],[169.2,907]], w: 2 }, { line: [[163.6,901],[162.8,906]], w: 2 }, { line: [[157,899],[155.2,903.5]], w: 2 }] });
  add({ id: "calcaneus", L: "bone", v: "b", mirror: true, ellipse: [171, 893, 10, 8], fill: "bone", deco: ["M171 876 L170 885"] });

  /* ===== ORGANS ===== */
  add({ id: "brain", L: "organ", ellipse: [200, 56, 33, 31], fill: "brain", deco: ["M200 26 L200 86", "M176 44c6-4 10 2 16-2", "M208 40c6 4 10-2 16 2", "M172 60c7 2 9-4 17-1", "M211 58c7 3 9-3 17 0", "M180 76c5-3 9 2 14-1", "M206 76c5 3 9-2 14 1"] });
  add({ id: "eye", L: "organ", mirror: true, circle: [184, 75, 6.6], fill: "eye", deco: ["M184 72.4a2.6 2.6 0 1 0 0.01 0"] });
  add({ id: "esophagus", L: "organ", line: [[201,136],[203,180],[204,240],[206,290],[210,304],[214,311]], w: 6.5, stroke: "esoph" });
  add({ id: "trachea", L: "organ", parts: [{ line: [[200,134],[200,232]], w: 9, dash: "2.6 1.4", keepDash: true }, { line: [[200,231],[195,240],[189,252]], w: 6.5 }, { line: [[200,231],[208,238],[217,246]], w: 6 }], stroke: "airway", noFill: true });
  add({ id: "thyroid", L: "organ", parts: [{ ellipse: [191.5, 151, 5.8, 9.5] }, { ellipse: [208.5, 151, 5.8, 9.5] }, { rect: [192, 149, 16, 6, 2] }], fill: "thyroid" });
  add({ id: "lung_r", L: "organ", v: "fb", op: 0.82, pts: [[184,174],[176,176],[162,190],[150,212],[143,240],[140,270],[140,296],[152,304],[168,300],[184,296],[190,290],[191,250],[190,215],[188,190]], fill: "lung", deco: ["M191 252 C176 250 160 249 143 247", "M151 220 C160 245 172 272 184 296"] });
  add({ id: "lung_l", L: "organ", v: "fb", op: 0.82, pts: [[216,174],[226,177],[240,190],[251,212],[258,240],[261,270],[261,298],[250,307],[236,304],[232,296],[240,284],[240,268],[228,252],[216,240],[212,215],[212,190]], fill: "lung", deco: ["M219 197 C230 232 240 266 247 304"] });
  add({ id: "heart", L: "organ", pts: [[196,236],[206,230],[218,232],[230,240],[240,254],[244,272],[242,288],[238,296],[228,300],[214,297],[200,289],[191,276],[188,258],[190,244]], fill: "heart", deco: ["M214 236 C220 255 228 276 236 295", "M193 262 C200 262 206 266 210 274"] });
  add({ id: "diaphragm", L: "organ", v: "fb", line: [[138,308],[150,292],[170,284],[190,292],[200,300],[212,293],[232,288],[250,296],[262,311]], w: 3.5, stroke: "diaph" });
  add({ id: "spleen", L: "organ", v: "fb", pts: [[246,316],[255,320],[259,334],[257,350],[251,356],[248,344],[246,330]], fill: "spleen" });
  add({ id: "kidney", L: "organ", v: "fb", mirror: true, mirrorDy: -10, pts: [[166,362],[176,360],[184,368],[182,378],[185,388],[180,400],[170,402],[162,392],[160,376]], fill: "kidney" });
  add({ id: "adrenal", L: "organ", v: "fb", mirror: true, mirrorDy: -10, pts: [[166,360],[173,350],[182,361],[176,363]], fill: "adrenal" });
  add({ id: "ureter", L: "organ", mirror: true, mirrorDy: -10, line: [[183,388],[185,420],[188,450],[194,478]], w: 1.8, stroke: "ureter", mirrorEnd: [206, 478] });
  add({ id: "pancreas", L: "organ", pts: [[190,366],[204,360],[222,354],[240,346],[249,342],[249,349],[232,357],[214,365],[205,373],[197,381],[188,378]], fill: "pancreas" });
  add({ id: "stomach", L: "organ", pts: [[212,306],[226,300],[240,303],[250,314],[252,332],[248,350],[240,364],[226,372],[212,372],[200,367],[196,360],[204,354],[218,353],[230,345],[236,332],[231,318],[220,313]], fill: "stomach" });
  add({ id: "liver", L: "organ", v: "fb", pts: [[140,304],[156,296],[176,296],[196,300],[214,304],[230,309],[236,317],[226,323],[206,330],[190,338],[172,346],[156,350],[144,342],[138,326]], fill: "liver", deco: ["M196 301 C194 318 190 330 186 340"] });
  add({ id: "gallbladder", L: "organ", pts: [[161,336],[168,337],[172,346],[168,354],[162,352],[158,343]], fill: "gall" });
  add({ id: "duodenum", L: "organ", line: [[198,364],[187,366],[180,378],[182,392],[196,396],[211,392],[218,385]], w: 6, stroke: "duod" });
  (function () {
    const rows = [399, 410, 421, 432, 443]; let d = "M218 386 Q226 390 224 399"; let goingLeft = true;
    for (let i = 0; i < rows.length; i++) { const y = rows[i], nx = goingLeft ? 181 : 224; d += " L" + nx + " " + y; if (i < rows.length - 1) d += " A5.5 5.5 0 0 " + (goingLeft ? 0 : 1) + " " + nx + " " + rows[i + 1]; goingLeft = !goingLeft; }
    d += " Q182 452 172 454";
    add({ id: "small_intestine", L: "organ", rawLine: d, w: 7, stroke: "intest" });
  })();
  add({ id: "colon", L: "organ", line: [[167,458],[160,432],[158,402],[162,378],[180,386],[205,393],[230,385],[244,372],[247,400],[246,432],[240,452],[226,462],[212,458],[204,466],[201,476]], w: 10, stroke: "colon" });
  add({ id: "appendix", L: "organ", line: [[167,462],[170,470],[175,474]], w: 3, stroke: "colon" });
  add({ id: "rectum", L: "organ", line: [[201,474],[200,484],[200,494]], w: 8, stroke: "rectum" });
  add({ id: "bladder", L: "organ", ellipse: [200, 486, 13.5, 10.5], fill: "bladder" });
  add({ id: "uterus", L: "organ", sex: "f", pts: [[192,455],[208,455],[212,465],[206,474],[200,478],[194,474],[188,465]], fill: "uterus" });
  add({ id: "uterine_tube", L: "organ", sex: "f", mirror: true, line: [[191,458],[184,455],[177,455],[172,459]], w: 2, stroke: "uterus" });
  add({ id: "ovary", L: "organ", sex: "f", mirror: true, ellipse: [173, 463, 4.8, 3.4], fill: "ovary" });
  add({ id: "scrotum", L: "organ", sex: "m", pts: [[191,505],[200,503],[209,505],[211,516],[205,525],[200,526],[195,525],[189,516]], fill: "skin", noTap: true, strokeC: "skinline" });
  add({ id: "testis", L: "organ", sex: "m", mirror: true, ellipse: [195.5, 515, 3.6, 5.5], fill: "testis" });
  add({ id: "vas_deferens", L: "organ", sex: "m", mirror: true, line: [[195,510],[188,496],[180,482],[184,474],[192,478],[196,488]], w: 1.4, stroke: "vas" });
  add({ id: "prostate", L: "organ", sex: "m", ellipse: [200, 499, 6, 4], fill: "prostate" });

  /* ===== MUSCLES (front) ===== */
  add({ id: "scm", L: "muscle", mirror: true, pts: [[166,100],[172,103],[196,178],[192,186],[181,182],[170,140]], fill: "muscle" });
  add({ id: "trapezius", L: "muscle", mirror: true, pts: [[186,132],[184,160],[160,177],[130,184],[150,170],[176,150]], fill: "muscle2" });
  add({ id: "pectoralis", L: "muscle", mirror: true, pts: [[195,190],[195,250],[186,268],[168,272],[148,262],[132,236],[124,214],[140,196],[168,190]], fill: "muscle", deco: ["M190 200 C170 205 150 212 128 218", "M192 225 C170 228 150 228 128 222", "M190 252 C170 248 150 238 130 226"] });
  add({ id: "deltoid", L: "muscle", v: "fb", mirror: true, pts: [[126,182],[112,189],[102,211],[98,240],[104,262],[110,236],[118,214],[132,196]], fill: "muscle2", deco: ["M118 196 C110 215 106 235 106 252"] });
  add({ id: "biceps", L: "muscle", mirror: true, pts: [[114,222],[120,240],[116,300],[106,340],[99,352],[96,336],[100,290],[106,240]], fill: "muscle", deco: ["M110 240 C108 270 106 300 103 330"] });
  add({ id: "brachioradialis", L: "muscle", v: "fb", mirror: true, pts: [[90,330],[95,350],[88,400],[78,450],[70,482],[66,478],[72,440],[80,390],[84,350]], fill: "muscle2" });
  add({ id: "forearm_flexors", L: "muscle", mirror: true, pts: [[104,354],[101,390],[93,440],[85,480],[79,488],[77,470],[83,430],[89,390],[96,360]], fill: "muscle", deco: ["M98 370 C94 400 90 430 84 470"] });
  add({ id: "rectus_abdominis", L: "muscle", mirror: true, pts: [[198,300],[198,470],[191,474],[185,470],[183,400],[181,330],[185,304]], fill: "muscle", deco: ["M183 332 L198 334", "M183 362 L198 363", "M184 395 L198 396"] });
  add({ id: "external_oblique", L: "muscle", mirror: true, pts: [[180,300],[182,400],[184,468],[170,474],[150,442],[139,400],[140,350],[146,302],[160,293]], fill: "muscle2", deco: ["M138 432 L190 482", "M150 320 C160 360 165 400 168 440"] });
  add({ id: "adductors", L: "muscle", mirror: true, pts: [[176,490],[194,505],[190,560],[182,622],[176,600],[170,540]], fill: "muscle2" });
  add({ id: "vastus_lateralis", L: "muscle", v: "fb", mirror: true, pts: [[130,490],[140,500],[142,580],[150,650],[146,668],[138,650],[130,580],[126,520]], fill: "muscle2" });
  add({ id: "rectus_femoris", L: "muscle", mirror: true, pts: [[146,470],[152,470],[157,540],[161,620],[161,660],[152,663],[146,620],[140,540]], fill: "muscle", deco: ["M150 500 C152 550 154 600 156 650"] });
  add({ id: "vastus_medialis", L: "muscle", mirror: true, pts: [[166,582],[176,612],[180,650],[172,669],[162,661],[164,620]], fill: "muscle" });
  add({ id: "sartorius", L: "muscle", mirror: true, pts: [[136,430],[143,430],[161,520],[179,620],[183,690],[176,694],[170,620],[152,520]], fill: "muscle3" });
  add({ id: "tibialis_anterior", L: "muscle", mirror: true, pts: [[150,700],[158,702],[162,760],[166,830],[172,860],[166,862],[156,830],[150,760]], fill: "muscle" });
  add({ id: "gastrocnemius", L: "muscle", mirror: true, pts: [[172,700],[178,720],[176,780],[170,800],[168,760],[170,720]], fill: "muscle2" });
  /* ===== MUSCLES (back) ===== */
  add({ id: "erector_spinae", L: "muscle", v: "b", mirror: true, pts: [[193,178],[199,178],[199,420],[192,424],[186,380],[185,300],[186,220]], fill: "muscle3", deco: ["M192 200 L192 410"] });
  add({ id: "infraspinatus", L: "muscle", v: "b", mirror: true, pts: [[128,206],[156,196],[158,232],[150,262],[136,266],[126,234]], fill: "muscle2", deco: ["M132 236 C140 250 146 258 150 262"] });
  add({ id: "latissimus", L: "muscle", v: "b", mirror: true, pts: [[192,302],[172,246],[150,236],[136,262],[134,322],[144,382],[160,422],[196,424],[199,340]], fill: "muscle", deco: ["M150 250 C170 300 182 360 190 420", "M140 290 C160 330 174 380 186 420"] });
  add({ id: "trapezius_b", info: "trapezius", L: "muscle", v: "b", mirror: true, pts: [[200,116],[186,128],[182,160],[150,176],[124,184],[146,200],[170,242],[192,302],[200,334]], fill: "muscle2", deco: ["M196 150 C176 170 160 186 140 194", "M198 220 C184 232 172 246 164 262"] });
  add({ id: "triceps", L: "muscle", v: "b", mirror: true, pts: [[116,214],[124,232],[120,300],[110,340],[100,352],[94,338],[100,290],[106,240]], fill: "muscle", deco: ["M112 236 C110 270 108 300 104 338", "M118 250 C114 290 110 320 106 346"] });
  add({ id: "forearm_extensors", L: "muscle", v: "b", mirror: true, pts: [[98,358],[96,400],[88,450],[80,490],[72,492],[72,462],[80,420],[86,380],[90,356]], fill: "muscle2", deco: ["M92 376 C88 410 84 440 78 476"] });
  add({ id: "gluteus_medius", L: "muscle", v: "b", mirror: true, pts: [[134,418],[160,416],[170,440],[158,468],[138,468],[128,446]], fill: "muscle2" });
  add({ id: "gluteus_maximus", L: "muscle", v: "b", mirror: true, pts: [[197,430],[170,442],[150,472],[136,474],[127,502],[150,532],[182,530],[198,502]], fill: "muscle", deco: ["M190 450 C170 470 152 490 140 520", "M196 480 C176 492 160 510 150 528"] });
  add({ id: "biceps_femoris", L: "muscle", v: "b", mirror: true, pts: [[138,532],[160,530],[160,612],[153,662],[144,668],[136,620]], fill: "muscle2", deco: ["M150 540 C150 580 150 620 148 660"] });
  add({ id: "semitendinosus", L: "muscle", v: "b", mirror: true, pts: [[162,530],[186,532],[182,622],[176,666],[164,666],[160,612]], fill: "muscle", deco: ["M172 542 C172 580 170 620 168 660"] });
  add({ id: "gastrocnemius_b", info: "gastrocnemius", L: "muscle", v: "b", mirror: true, pts: [[148,696],[176,694],[180,740],[172,792],[162,798],[152,792],[144,740]], fill: "muscle", deco: ["M162 700 L162 790"] });
  add({ id: "soleus", L: "muscle", v: "b", mirror: true, pts: [[149,782],[173,782],[177,822],[170,852],[158,852],[149,822]], fill: "muscle2" });
  add({ id: "achilles", L: "muscle", v: "b", mirror: true, line: [[163,850],[165,872],[169,892]], w: 5, stroke: "tendon" });

  /* ===== VEINS ===== */
  const V = (o) => add(Object.assign({ L: "vein", stroke: "vein" }, o));
  V({ id: "svc", line: [[192,196],[193,222],[194,246]], w: 6 });
  V({ id: "brachiocephalic_v", mirror: true, line: [[182,186],[187,191],[192,196]], w: 4.5, mirrorLine: [[218,186],[208,190],[198,194],[192,196]] });
  V({ id: "ijv", mirror: true, line: [[179,134],[180,160],[182,186]], w: 3.6 });
  V({ id: "ejv", mirror: true, line: [[172,116],[168,150],[166,182]], w: 1.8 });
  V({ id: "subclavian_v", mirror: true, line: [[182,186],[160,190],[140,195]], w: 3 });
  V({ id: "axillary_v", mirror: true, line: [[140,195],[128,204],[123,218]], w: 3 });
  V({ id: "cephalic", v: "fb", mirror: true, line: [[136,195],[124,213],[104,250],[96,300],[90,345],[86,370],[80,420],[72,470],[67,494]], w: 2 });
  V({ id: "basilic", v: "fb", mirror: true, line: [[123,218],[118,260],[113,300],[107,345],[102,372],[96,420],[88,470],[82,496]], w: 2 });
  V({ id: "median_cubital", mirror: true, line: [[88,372],[95,367],[102,362]], w: 2 });
  V({ id: "ivc", v: "fb", bdash: true, line: [[196,300],[197,330],[198,380],[198,414]], w: 6 });
  V({ id: "hepatic_v", parts: [{ line: [[182,314],[196,304]] }, { line: [[192,316],[196,304]] }, { line: [[208,314],[196,304]] }], w: 2, noFill: true });
  V({ id: "portal_v", line: [[192,366],[186,352],[177,338]], w: 4, stroke: "portal" });
  V({ id: "splenic_v", line: [[249,344],[230,352],[212,360],[192,366]], w: 2.4, stroke: "portal" });
  V({ id: "smv", line: [[190,412],[191,388],[192,366]], w: 2.4, stroke: "portal" });
  V({ id: "renal_v", v: "fb", mirror: true, mirrorDy: -10, line: [[184,382],[191,377],[197,372]], w: 2.6, mirrorLine: [[216,372],[208,368],[198,365]] });
  V({ id: "common_iliac_v", mirror: true, line: [[198,414],[186,432],[176,448]], w: 3.4 });
  V({ id: "femoral_v", mirror: true, line: [[176,448],[168,466],[166,484],[166,520],[168,580],[171,640],[170,666]], w: 3 });
  V({ id: "popliteal_v", v: "fb", post: true, mirror: true, line: [[170,666],[166,682],[163,700]], w: 2.6, dash: "3 2.2" });
  V({ id: "great_saphenous", v: "fb", mirror: true, line: [[181,858],[176,800],[172,740],[176,690],[184,620],[187,560],[180,510],[168,496]], w: 1.8 });
  V({ id: "small_saphenous", v: "fb", post: true, mirror: true, line: [[156,866],[150,820],[153,760],[163,700]], w: 1.6, dash: "3 2.2" });

  /* ===== ARTERIES ===== */
  const A = (o) => add(Object.assign({ L: "artery", stroke: "artery" }, o));
  A({ id: "aorta", v: "fb", line: [[206,252],[204,230],[205,214],[212,208],[219,215],[214,234],[210,262],[207,300],[204,330],[203,380],[202,414]], w: 7 });
  A({ id: "coronary", parts: [{ line: [[204,247],[196,253],[190,268],[194,286],[206,296]] }, { line: [[210,244],[218,252],[230,276],[238,292]] }, { line: [[210,244],[222,241],[234,250]] }], w: 1.6, noFill: true });
  A({ id: "brachiocephalic_a", line: [[203,212],[197,201],[192,192]], w: 4.2 });
  A({ id: "common_carotid", mirror: true, line: [[192,192],[188,160],[187,136]], w: 3, mirrorLine: [[208,210],[212,170],[213,136]] });
  A({ id: "internal_carotid", mirror: true, line: [[187,136],[185,120],[186,100]], w: 2.4 });
  A({ id: "external_carotid", mirror: true, parts: [{ line: [[187,136],[181,124],[177,110],[170,96],[166,70]] }, { line: [[182,128],[176,124],[180,114],[186,104]] }], w: 1.8, noFill: true });
  A({ id: "vertebral", v: "fb", mirror: true, line: [[178,187],[190,175],[193,150],[195,124]], w: 1.8, mirrorLine: [[222,190],[210,176],[207,150],[205,124]] });
  A({ id: "subclavian_a", mirror: true, line: [[192,192],[176,186],[158,188],[140,192]], w: 3, mirrorLine: [[214,210],[226,190],[242,188],[260,192]] });
  A({ id: "axillary_a", mirror: true, line: [[140,192],[128,200],[122,212]], w: 3 });
  A({ id: "brachial", mirror: true, line: [[122,212],[115,250],[110,300],[101,346],[96,358]], w: 2.8 });
  A({ id: "profunda_brachii", v: "b", mirror: true, line: [[118,226],[112,256],[103,290],[94,326]], w: 1.7 });
  A({ id: "radial_a", mirror: true, line: [[96,358],[88,380],[80,430],[72,480],[68,500],[65,520]], w: 2.1 });
  A({ id: "ulnar_a", mirror: true, line: [[96,358],[96,380],[92,430],[84,480],[80,500],[77,520]], w: 2.1 });
  A({ id: "palmar_arch", mirror: true, line: [[65,522],[70,532],[77,522]], w: 1.6 });
  A({ id: "celiac", parts: [{ line: [[204,318],[208,322]] }, { line: [[208,322],[190,330],[176,336]] }, { line: [[208,322],[226,330],[246,336]] }, { line: [[208,322],[214,315]] }], w: 1.9, noFill: true });
  A({ id: "sma", parts: [{ line: [[203,334],[200,350],[196,380],[192,410]] }, { line: [[198,368],[212,388],[218,404]] }, { line: [[195,392],[184,416],[172,440]] }], w: 2.1, noFill: true });
  A({ id: "renal_a", v: "fb", mirror: true, mirrorDy: -10, line: [[203,358],[192,370],[183,380]], w: 2.2, mirrorLine: [[204,354],[211,362],[217,370]] });
  A({ id: "ima", line: [[202,394],[212,404],[226,420],[238,440]], w: 1.8 });
  A({ id: "common_iliac_a", mirror: true, line: [[202,414],[188,430],[178,444]], w: 3.4 });
  A({ id: "internal_iliac", mirror: true, line: [[178,444],[180,460],[185,474]], w: 2 });
  A({ id: "external_iliac", mirror: true, line: [[178,444],[168,462],[160,482]], w: 3 });
  A({ id: "gluteal_a", v: "b", mirror: true, parts: [{ line: [[180,446],[162,440],[146,432]] }, { line: [[181,454],[166,468],[150,484]] }], w: 1.7, noFill: true });
  A({ id: "femoral_a", mirror: true, line: [[160,482],[160,520],[164,580],[168,640],[166,666]], w: 3 });
  A({ id: "popliteal_a", v: "fb", post: true, mirror: true, line: [[166,666],[164,682],[162,700]], w: 2.6, dash: "3 2.2" });
  A({ id: "anterior_tibial", mirror: true, line: [[162,700],[157,712],[157,780],[162,850],[168,872],[172,882],[176,896]], w: 2 });
  A({ id: "posterior_tibial", v: "fb", post: true, mirror: true, line: [[162,700],[168,720],[172,800],[178,856],[181,866]], w: 2, dash: "3 2.2" });

  /* ===== NERVES ===== */
  const N = (o) => add(Object.assign({ L: "nerve", stroke: "nerve" }, o));
  N({ id: "spinal_cord", v: "fb", op: 0.8, parts: [{ line: [[200,118],[200,345]], w: 3.6 }, { line: [[200,345],[197,400],[194,468]], w: 1 }, { line: [[200,345],[199,400],[198,470]], w: 1 }, { line: [[200,345],[201,400],[202,470]], w: 1 }, { line: [[200,345],[203,400],[206,468]], w: 1 }], noFill: true });
  N({ id: "vagus", mirror: true, line: [[195,124],[184,140],[184,180],[188,200],[194,240],[199,290],[203,320]], w: 1.6, mirrorLine: [[205,124],[216,140],[216,180],[213,206],[208,240],[203,290],[199,320]] });
  N({ id: "rln_left", line: [[214,206],[217,220],[211,222],[206,200],[204,170],[203,148]], w: 1.4 });
  N({ id: "phrenic", mirror: true, line: [[194,150],[184,170],[180,200],[186,240],[188,270],[178,296]], w: 1.4, mirrorLine: [[206,150],[216,170],[224,206],[240,250],[246,276],[248,298]] });
  N({ id: "brachial_plexus", mirror: true, parts: [{ line: [[194,150],[178,170],[160,186]] }, { line: [[194,158],[178,174],[160,186]] }, { line: [[194,166],[178,178],[160,187]] }, { line: [[195,174],[178,182],[160,188]] }, { line: [[196,180],[178,186],[160,189]] }, { line: [[160,186],[142,194],[129,205]] }, { line: [[160,188],[143,197],[130,208]] }, { line: [[160,189],[144,200],[131,211]] }], w: 1.5, noFill: true });
  N({ id: "axillary_n", v: "fb", mirror: true, line: [[130,207],[122,214],[114,216],[110,208]], w: 1.5 });
  N({ id: "musculocutaneous", mirror: true, line: [[130,206],[119,230],[107,280],[99,340],[90,380],[82,430]], w: 1.5 });
  N({ id: "median_n", mirror: true, parts: [{ line: [[129,207],[119,250],[113,300],[104,350],[92,400],[81,450],[74,505],[68,528]] }, { line: [[68,528],[60,540]], w: 1.2 }, { line: [[68,528],[64,548]], w: 1.2 }, { line: [[68,528],[68,550]], w: 1.2 }], w: 1.9, noFill: true });
  N({ id: "ulnar_n", v: "fb", mirror: true, line: [[130,210],[121,250],[115,300],[108,349],[101,400],[91,455],[82,505],[77,530],[76,548]], w: 1.7 });
  N({ id: "radial_n", v: "fb", post: true, mirror: true, parts: [{ line: [[130,209],[119,228],[108,262],[96,300],[88,340]], dash: "3 2" }, { line: [[88,340],[86,352],[81,410],[71,470],[65,505]] }], w: 1.8, noFill: true });
  N({ id: "long_thoracic", mirror: true, line: [[194,170],[172,190],[143,230],[140,290]], w: 1.3 });
  N({ id: "intercostal", mirror: true, parts: [0, 2, 4, 6].map((k) => { const yv = 170 + 12 * (3 + k); return { line: [[196, yv + 4], [168, yv + 8], [141, yv + 19], [150, yv + 34], [172, yv + 37]] }; }), w: 0.9, noFill: true, op: 0.85 });
  N({ id: "femoral_n", mirror: true, parts: [{ line: [[194,372],[186,400],[176,430],[160,470],[153,486]] }, { line: [[194,386],[186,410]] }, { line: [[195,398],[187,416]] }, { line: [[153,486],[148,520]], w: 1.2 }, { line: [[153,486],[156,540]], w: 1.2 }, { line: [[153,486],[162,530]], w: 1.2 }], w: 2, noFill: true });
  N({ id: "saphenous_n", v: "fb", mirror: true, line: [[156,500],[163,560],[170,620],[175,670],[177,720],[175,800],[179,850]], w: 1.2 });
  N({ id: "obturator_n", mirror: true, line: [[194,400],[186,440],[176,486],[181,520],[185,560]], w: 1.5 });
  N({ id: "lfcn", mirror: true, line: [[194,384],[176,410],[141,437],[131,500],[131,560]], w: 1.2 });
  N({ id: "superior_gluteal_n", v: "b", mirror: true, line: [[182,442],[164,436],[148,428]], w: 1.3 });
  N({ id: "inferior_gluteal_n", v: "b", mirror: true, line: [[183,458],[168,474],[154,490]], w: 1.3 });
  N({ id: "sciatic", v: "fb", post: true, mirror: true, line: [[196,440],[184,452],[166,470],[151,500],[152,560],[156,620],[160,660]], w: 3, dash: "3.5 2.2" });
  N({ id: "tibial_n", v: "fb", post: true, mirror: true, line: [[160,660],[162,700],[168,780],[176,850],[180,866]], w: 2, dash: "3 2" });
  N({ id: "common_fibular", v: "fb", post: true, mirror: true, parts: [{ line: [[160,660],[151,680],[146,700]], dash: "3 2" }, { line: [[146,700],[148,712],[154,760],[160,840],[172,882]], w: 1.4 }, { line: [[147,708],[146,740],[150,820],[160,880]], w: 1.3 }], w: 1.8, noFill: true });
  N({ id: "sural_n", v: "b", mirror: true, line: [[161,704],[156,744],[152,800],[150,860],[147,890]], w: 1.2 });

  /* ===== LYMPHATICS ===== */
  const Ly = (o) => add(Object.assign({ L: "lymph", stroke: "lymph", fill: "lymph" }, o));
  Ly({ id: "thymus", pts: [[194,196],[200,198],[206,196],[210,212],[204,222],[200,218],[196,222],[190,212]], fill: "thymus", stroke: null });
  Ly({ id: "lymph_vessels", mirror: true, parts: [{ line: [[130,220],[114,280],[100,380],[86,480]] }, { line: [[163,490],[180,560],[176,680],[172,820]] }], w: 1, noFill: true, op: 0.7 });
  Ly({ id: "thoracic_duct", parts: [{ line: [[200,345],[201,320],[203,280],[205,230],[208,196],[214,184],[219,186]], w: 2 }, { ellipse: [200, 352, 3, 7] }], noFill: false });
  Ly({ id: "right_lymphatic_duct", line: [[186,190],[183,186],[181,188]], w: 2 });
  Ly({ id: "cervical_nodes", mirror: true, parts: [{ circle: [177,146,2.6] }, { circle: [175.5,156,2.6] }, { circle: [179,166,2.6] }] });
  Ly({ id: "virchow_node", circle: [227, 180, 3.2] });
  Ly({ id: "axillary_nodes", mirror: true, parts: [{ circle: [130,212,2.8] }, { circle: [135,220,2.8] }, { circle: [128,225,2.8] }, { circle: [136,229,2.6] }] });
  Ly({ id: "para_aortic_nodes", parts: [{ circle: [194,372,2.5] }, { circle: [210,380,2.5] }, { circle: [194,394,2.5] }, { circle: [211,400,2.5] }] });
  Ly({ id: "inguinal_nodes", mirror: true, parts: [{ circle: [162,486,2.8] }, { circle: [169,492,2.8] }, { circle: [157,495,2.8] }] });

  /* ===== DERMATOMES ===== */
  const DC = { C: "#6FA8DC", T: "#8FD19E", L: "#F2B36B", S: "#E58BAE" };
  const D = (id, v, pts, lab, label) => add({ id: v === "b" ? id + "_b" : id, info: id, L: "derm", v, mirror: true, pts, color: DC[id[2]], label, labAt: lab, dermo: true });
  D("d_C2", "f", [[200,129],[186,131],[184,146],[200,146]], [191, 141], "C2");
  D("d_C3", "f", [[200,146],[184,146],[180,163],[200,163]], [191, 158], "C3");
  D("d_C4", "f", [[200,164],[179,164],[150,175],[122,182],[108,195],[113,214],[142,211],[172,208],[200,206]], [160, 194], "C4");
  D("d_C2", "b", [[200,118],[178,124],[184,146],[200,146]], [191, 138], "C2");
  D("d_C3", "b", [[200,146],[184,146],[180,163],[200,163]], [191, 158], "C3");
  D("d_C4", "b", [[200,164],[179,164],[150,175],[122,182],[108,195],[113,214],[142,211],[172,208],[200,206]], [160, 194], "C4");
  const bands = [["T2", 207, 246], ["T3", 246, 258], ["T4", 258, 275], ["T5", 275, 292], ["T6", 292, 312], ["T7", 312, 332], ["T8", 332, 352], ["T9", 352, 372], ["T10", 372, 394], ["T11", 394, 416], ["T12", 416, 440], ["L1", 440, 468]];
  bands.forEach(([lv, y1, y2]) => {
    const pts = [[200, y1], [torsoX(y1), y1], [torsoX((y1 + y2) / 2), (y1 + y2) / 2], [torsoX(y2), y2], [200, y2]];
    if (lv === "T2") pts.splice(1, 1, [172, y1], [142, y1 + 4], [132, y1 + 30]);
    const lab = [Math.min(176, torsoX(y2) + 26), (y1 + y2) / 2 + 4];
    ["f", "b"].forEach((v) => D("d_" + lv, v, pts, lab, lv));
  });
  const arm = (v) => {
    D("d_C5", v, [[108,196],[96,250],[90,300],[85,350],[96,352],[104,300],[110,250],[118,214]], [100, 290], "C5");
    D("d_C6", v, [[85,352],[78,400],[70,450],[64,495],[56,520],[50,560],[58,560],[64,520],[72,495],[78,450],[86,400],[96,352]], [74, 440], "C6");
    D("d_C7", v, [[58,560],[52,590],[63,598],[72,586],[74,560]], [63, 585], "C7");
    D("d_C8", v, [[96,400],[90,455],[80,505],[77,550],[74,560],[82,556],[88,505],[98,455],[104,400]], [95, 470], "C8");
    D("d_T1", v, [[118,214],[110,250],[104,300],[98,352],[104,400],[112,400],[108,352],[116,300],[123,256],[131,240]], [112, 330], "T1");
  };
  arm("f"); arm("b");
  D("d_L2", "f", [[200,470],[123,470],[124,520],[130,600],[186,600],[194,522],[200,506]], [160, 560], "L2");
  D("d_L3", "f", [[130,600],[140,670],[146,720],[176,720],[180,680],[186,600]], [160, 666], "L3");
  D("d_L4", "f", [[160,720],[176,720],[173,780],[178,840],[184,880],[187,902],[176,910],[173,880],[167,840],[161,780]], [172, 812], "L4");
  D("d_L5", "f", [[146,720],[160,720],[161,780],[167,840],[173,880],[176,910],[160,910],[150,896],[156,876],[150,840],[145,780]], [153, 812], "L5");
  D("d_S1", "f", [[145,780],[150,840],[156,876],[150,896],[160,910],[150,906],[141,890],[139,840],[141,790]], [146, 862], "S1");
  D("d_S345", "b", [[200,470],[184,470],[178,500],[194,522],[200,506]], [188, 494], "S3–S5");
  D("d_S2", "b", [[150,500],[176,500],[178,560],[180,620],[178,680],[150,680],[150,620],[148,560]], [164, 592], "S2");
  D("d_S1", "b", [[123,470],[150,500],[148,560],[150,620],[150,680],[146,720],[145,780],[150,840],[156,876],[150,896],[160,910],[144,900],[136,860],[134,780],[132,700],[126,620],[124,520]], [134, 700], "S1");
  D("d_L5", "b", [[176,500],[194,522],[186,600],[180,680],[176,720],[173,780],[178,840],[184,880],[187,902],[176,910],[170,880],[166,830],[163,780],[164,720],[178,680],[180,620],[178,560]], [176, 660], "L5");

  /* ===== render ===== */
  function elt(p, base, view) {
    const o = Object.assign({}, base, p);
    let dash = o.dash || null;
    if (view === "back") { if (base.post && !o.keepDash) dash = null; if (base.bdash) dash = "3 2.2"; }
    const fill = o.noFill || o.line || o.rawLine ? "none" : o.color ? o.color : "var(--c-" + (o.fill || "bone") + ")";
    const stroke = o.line || o.rawLine ? "var(--c-" + (o.stroke || "bone") + ")" : o.dermo ? "rgba(255,255,255,.85)" : (o.strokeC ? "var(--c-" + o.strokeC + ")" : "var(--fig-edge)");
    const sw = o.line || o.rawLine ? (o.w || 2) : o.dermo ? 0.9 : 0.6;
    const extra = (o.op != null ? ` opacity="${o.op}"` : "") + (dash ? ` stroke-dasharray="${dash}"` : "");
    let d;
    if (o.pts) d = smooth(o.pts, true);
    else if (o.line) d = smooth(o.line, false);
    else if (o.rawLine) d = o.rawLine;
    else if (o.circle) return `<circle cx="${o.circle[0]}" cy="${o.circle[1]}" r="${o.circle[2]}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"${extra}/>`;
    else if (o.ellipse) return `<ellipse cx="${o.ellipse[0]}" cy="${o.ellipse[1]}" rx="${o.ellipse[2]}" ry="${o.ellipse[3]}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"${extra}/>`;
    else if (o.rect) return `<rect x="${o.rect[0]}" y="${o.rect[1]}" width="${o.rect[2]}" height="${o.rect[3]}" rx="${o.rect[4] || 0}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"${extra}/>`;
    const lineAttrs = o.line || o.rawLine ? ` stroke-linecap="round" stroke-linejoin="round"` : "";
    let under = "";
    if ((o.line || o.rawLine) && o.outline) under = `<path d="${d}" fill="none" stroke="var(--fig-edge)" stroke-width="${sw + 1.3}" stroke-linecap="round" stroke-linejoin="round"${extra}/>`;
    let hit = "";
    if ((o.line || o.rawLine) && !o.noTap) hit = `<path d="${d}" class="hit" fill="none" stroke="transparent" stroke-width="${Math.max(9, sw + 6)}"/>`;
    return hit + under + `<path d="${d}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}"${lineAttrs}${extra}/>`;
  }
  function mirrorObj(o) {
    const m = JSON.parse(JSON.stringify(o));
    const dy = o.mirrorDy || 0;
    const fx = (pts) => shift(mir(pts), 0, dy);
    const walk = (q) => {
      if (q.pts) q.pts = fx(q.pts);
      if (q.line) q.line = fx(q.line);
      if (q.circle) q.circle = [2 * MX - q.circle[0], q.circle[1] + dy, q.circle[2]];
      if (q.ellipse) q.ellipse = [2 * MX - q.ellipse[0], q.ellipse[1] + dy, q.ellipse[2], q.ellipse[3]];
      if (q.rect) q.rect = [2 * MX - q.rect[0] - q.rect[2], q.rect[1] + dy, q.rect[2], q.rect[3], q.rect[4]];
      if (q.deco) q.deco = null;
      if (q.labAt) q.labAt = [2 * MX - q.labAt[0], q.labAt[1] + dy];
    };
    walk(m); if (m.parts) m.parts.forEach(walk);
    if (o.mirrorLine) m.line = o.mirrorLine;
    if (o.mirrorEnd && m.line) m.line[m.line.length - 1] = o.mirrorEnd;
    return m;
  }
  function renderStruct(o, side, view) {
    const id = o.id + (side ? "-" + side : "");
    let inner = "";
    const base = { fill: o.fill, stroke: o.stroke, w: o.w, noFill: o.noFill, strokeC: o.strokeC, outline: o.L === "bone", post: o.post, bdash: o.bdash, color: o.color, dermo: o.dermo };
    if (o.parts) o.parts.forEach((p) => { inner += elt(p, base, view); });
    else inner = elt(o, base, view);
    if (o.deco) inner += o.deco.map((dd) => `<path d="${dd}" class="deco" fill="none"/>`).join("");
    const flip = view === "back" ? ` transform="translate(${2 * o.labAt?.[0] || 0} 0) scale(-1 1)"` : "";
    if (o.label && o.labAt) inner += `<text x="${o.labAt[0]}" y="${o.labAt[1]}" class="dlab" text-anchor="middle"${flip}>${o.label}</text>`;
    const op = o.op != null && o.parts ? ` opacity="${o.op}"` : "";
    const tap = o.noTap ? ` class="notap"` : ` class="st${o.dermo ? " derm" : ""}" data-id="${id}" data-k="${o.info || o.id}" tabindex="-1"`;
    const sex = o.sex ? ` data-sex="${o.sex}"` : "";
    return `<g${tap}${sex}${op}>${inner}</g>`;
  }
  const ORDER = ["bone", "organ", "muscle", "vein", "artery", "nerve", "lymph", "derm"];
  const inView = (o, view) => { const v = o.v || "f"; return view === "front" ? v.includes("f") : v.includes("b"); };
  function build(view) {
    view = view || "front";
    const defs = `<defs><radialGradient id="skinGrad" cx="50%" cy="38%" r="70%"><stop offset="0" style="stop-color:var(--c-skin-hi)"/><stop offset="1" style="stop-color:var(--c-skin)"/></radialGradient></defs>`;
    let out = defs + `<g class="L-skin"><path d="${smooth(fullBody, true)}" class="skin"/>` +
      `<ellipse cx="157" cy="80" rx="4.5" ry="9" class="skin"/><ellipse cx="243" cy="80" rx="4.5" ry="9" class="skin"/>` +
      `<ellipse cx="200" cy="75" rx="42" ry="55" class="skin"/>` + (view === "front" ? "" : `<path d="M200 22 C178 22 158 44 158 76 C166 70 180 64 200 64 C220 64 234 70 242 76 C242 44 222 22 200 22Z" class="hair"/>`) + `</g>`;
    ORDER.forEach((L) => {
      out += `<g class="L-${L}">`;
      S.filter((o) => o.L === L && inView(o, view)).forEach((o) => {
        if (o.mirror) { out += renderStruct(o, "r", view) + renderStruct(mirrorObj(o), "l", view); }
        else out += renderStruct(o, "", view);
      });
      out += `</g>`;
    });
    if (view === "back") out = `<g transform="translate(400 0) scale(-1 1)">${out}</g>`;
    return out;
  }
  return { build, structures: S, inView };
})();
