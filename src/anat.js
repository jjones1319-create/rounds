/* Anatomy module v2. Exposes window.Anat with view(), mount(), handle(), input(), showOnBody(), open(). */
const Anat = (function () {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  const I = (p) => `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${p}</svg>`;
  const IC = {
    plus: I('<path d="M12 5v14M5 12h14"/>'), minus: I('<path d="M5 12h14"/>'), fit: I('<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>'),
    rotate: I('<path d="M3 12a9 9 0 0 1 15.5-6.3M21 12a9 9 0 0 1-15.5 6.3"/><path d="M18.5 2v4h-4M5.5 22v-4h4"/>'),
    right: I('<path d="M9 5l7 7-7 7"/>'), check: I('<path d="m5 12.5 4.5 4.5L19 7"/>'),
  };
  const CR = (p, closed) => { const n = p.length; const g = (i) => closed ? p[(i + n) % n] : p[Math.max(0, Math.min(n - 1, i))]; let d = "M" + p[0][0] + " " + p[0][1]; const last = closed ? n : n - 1; for (let i = 0; i < last; i++) { const p0 = g(i - 1), p1 = g(i), p2 = g(i + 1), p3 = g(i + 2); d += `C${(p1[0] + (p2[0] - p0[0]) / 6).toFixed(1)} ${(p1[1] + (p2[1] - p0[1]) / 6).toFixed(1)} ${(p2[0] - (p3[0] - p1[0]) / 6).toFixed(1)} ${(p2[1] - (p3[1] - p1[1]) / 6).toFixed(1)} ${p2[0]} ${p2[1]}`; } return d + (closed ? "Z" : ""); };
  const MARK = {};
  const markup = (v) => MARK[v] || (MARK[v] = FIG.build(v));
  const ID2S = Object.fromEntries(FIG.structures.map((o) => [o.id, o]));
  const STRUCTS = FIG.structures.filter((o) => INFO[o.info || o.id] && !o.noTap);
  const DICT = buildDictionary();
  const UIA = { tab: "body" };
  const Body = { view: "front", layers: new Set(["bone", "organ"]), sex: "f", sel: null, vb: { x: 0, y: 0, w: 400, h: 920 }, q: "", quiz: null, mode: "2d", sel3: null };
  const Brain = { view: "lateral", sel: null, terr: false, cn: null };
  const Heart = { view: "outside", sel: null };
  const Idx = { q: "", filter: "all" };
  const Quiz = { qs: [], i: 0, score: 0, answered: false };
  let appHooks = {};

  /* ---------- shared ---------- */
  function layerOf(key) { const inf = INFO[key]; return LAYERS.find((l) => l.k === (inf ? inf.L : "")); }
  function cardHTML(title, pills, desc, pearl, extra) {
    return `<div class="row wrap" style="margin-bottom:6px">${pills}</div><h3>${esc(title)}</h3><p style="margin:8px 0 0">${esc(desc)}</p>${extra || ""}<div class="callout"><b>Clinical pearl.</b> ${esc(pearl)}</div>`;
  }
  function pill(text, color) { return `<span class="pill">${color ? `<span class="dot" style="background:${color}"></span>` : ""}${esc(text)}</span>`; }

  /* ---------- top-level view ---------- */
  function view() {
    const tabs = [["body", "Body"], ["brain", "Brain"], ["heart", "Heart"], ["index", "Index"], ["bones", "Bones"]];
    let h = `<h1>Anatomy</h1><div class="seg" role="group" aria-label="Anatomy sections" style="margin-top:12px">${tabs.map(([k, n]) => `<button data-act="atab" data-v="${k}" aria-pressed="${UIA.tab === k}">${n}</button>`).join("")}</div>`;
    if (UIA.tab === "body") h += bodyHTML();
    else if (UIA.tab === "brain") h += brainHTML();
    else if (UIA.tab === "heart") h += heartHTML();
    else if (UIA.tab === "index") h += indexHTML();
    else h += bonesHTML();
    return h;
  }
  function mount() {
    if (UIA.tab === "body") { if (Body.mode === "3d") mount3D(); else mountBody(); }
    if (UIA.tab === "brain" && Brain.view === "underside") $$(".cnfig .cn").forEach((g) => g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); selectCN(g.dataset.v); } }));
  }
  function rerender(keepScroll) { const y = window.scrollY; appHooks.render(); if (keepScroll) window.scrollTo(0, y); else window.scrollTo(0, 0); }

  /* ================= BODY ================= */
  function bodyHTML() {
    const is3 = Body.mode === "3d";
    const top = `<div class="search-wrap" style="margin-top:14px"><input class="search" type="search" id="bsearch" placeholder="Find a structure (femur, vagus, L5 dermatome…)" aria-label="Find a structure" value="${esc(Body.q)}" autocomplete="off"><div id="bresults"></div></div>
      <div class="row" style="margin-top:12px"><div class="seg fit" role="group" aria-label="Body view"><button data-act="body-mode" data-v="3d" aria-pressed="${is3}">3D</button><button data-act="body-mode" data-v="2d" aria-pressed="${!is3}">Diagram</button></div>${is3 ? `<span class="hint">Male model. Dermatomes and female organs are in Diagram.</span>` : ""}</div>`;
    const chips = (list) => `<div class="scrollx" style="margin-top:12px" role="group" aria-label="Layers"><button class="chip" data-act="layers-all" aria-pressed="${list.every((l) => Body.layers.has(l.k))}">All layers</button>${list.map((l) => `<button class="chip" data-act="layer" data-v="${l.k}" aria-pressed="${Body.layers.has(l.k)}"><span class="dot" style="background:${l.c}"></span>${l.n}</button>`).join("")}</div>`;
    if (is3) return top + chips(LAYERS3()) + `
      <div class="fig-wrap" id="figwrap" style="margin-top:10px"><div class="fig fig3d" id="fig3d"></div>
        <div class="zoom"><button data-act="zoom-in" aria-label="Zoom in">${IC.plus}</button><button data-act="zoom-out" aria-label="Zoom out">${IC.minus}</button><button data-act="zoom-fit" aria-label="Show whole body">${IC.fit}</button></div>
        <div class="viewtag">3D</div><div class="status3d" id="status3d" aria-live="polite" hidden></div>
        <div class="fig-note">Drag to turn, pinch to zoom, two fingers to move.</div>
        <div class="load3d" id="load3d" aria-live="polite">Loading 3D anatomy…</div></div>
      <div class="row" style="margin-top:10px"><button class="btn ghost sm" data-act="id-quiz">Name that structure</button><span class="hint">Every card ends with a board pearl.</span></div>
      <div class="panel infocard" id="infocard" style="margin-top:10px" aria-live="polite">${Body.quiz ? quizCard() : infoCardHTML()}</div>`;
    return top + chips(LAYERS) + `
      <div class="row" style="margin:10px 0"><button class="btn ghost sm" data-act="rotate-body" aria-label="Turn the figure around">${IC.rotate}${Body.view === "front" ? "Back" : "Front"}</button><div class="seg fit" role="group" aria-label="Pelvic organs"><button data-act="sex" data-v="f" aria-pressed="${Body.sex === "f"}">Female</button><button data-act="sex" data-v="m" aria-pressed="${Body.sex === "m"}">Male</button></div></div>
      <div class="fig-wrap" id="figwrap"><svg class="fig" id="fig" viewBox="0 0 400 920" role="img" aria-label="Interactive anatomical figure, ${Body.view} view">${markup(Body.view)}</svg>
        <div class="zoom"><button data-act="zoom-in" aria-label="Zoom in">${IC.plus}</button><button data-act="zoom-out" aria-label="Zoom out">${IC.minus}</button><button data-act="zoom-fit" aria-label="Show whole body">${IC.fit}</button></div>
        <div class="viewtag">${Body.view === "front" ? "Front" : "Back"}</div>
        <div class="fig-note">${Body.view === "front" ? "Front view: their right is on your left. Dashed lines run on the back." : "Back view: their right is on your right. Dashed lines run on the front."}</div></div>
      <div class="row" style="margin-top:10px"><button class="btn ghost sm" data-act="id-quiz">Name that structure</button><span class="hint">Every card ends with a board pearl.</span></div>
      <div class="panel infocard" id="infocard" style="margin-top:10px" aria-live="polite">${Body.quiz ? quizCard() : infoCardHTML()}</div>`;
  }
  function infoCardHTML() {
    if (Body.mode === "3d") return info3DHTML();
    if (!Body.sel) return `<h3>Tap anything on the body</h3><p class="muted" style="margin:6px 0 0">Switch layers with the chips, turn the figure around, pinch or scroll to zoom, and drag to move. Every structure has a short description and a board-relevant clinical pearl. Dermatomes are a layer too.</p>`;
    const base = Body.sel.replace(/-(r|l)$/, ""), so = ID2S[base], key = so ? (so.info || so.id) : base;
    const side = /-r$/.test(Body.sel) ? "Right " : /-l$/.test(Body.sel) ? "Left " : "";
    return keyCardHTML(key, side, true, "");
  }
  function keyCardHTML(key, side, showPost, extra) {
    const inf = INFO[key]; if (!inf) return "";
    const lay = layerOf(key);
    const display = side && inf.L !== "derm" ? side + inf.n.charAt(0).toLowerCase() + inf.n.slice(1) : inf.n;
    const pills = pill(lay.n, lay.c) + (showPost && inf.post ? pill("Back of the body") : "");
    return cardHTML(display, pills, inf.d, inf.p, extra + `<p style="margin:8px 0 0"><button class="btn quiet sm" style="padding:0" data-act="dict-go" data-id="${key}">Open in the index</button></p>`);
  }

  /* ---------- 3D body. js/body3d.js loads on first use; each layer's model loads the first time it is switched on. ---------- */
  let B3 = null, b3Loading = null;
  const LAYERS3 = () => LAYERS.filter((l) => l.k !== "derm");          // no dermatomes in 3D
  const layers3 = () => LAYERS3().map((l) => l.k).filter((k) => Body.layers.has(k));
  const layerName = (k) => (LAYERS.find((l) => l.k === k) || { n: k }).n.toLowerCase();
  const syncChips = () => { $$("[data-act=layer]").forEach((b) => b.setAttribute("aria-pressed", Body.layers.has(b.dataset.v))); const all = $("[data-act=layers-all]"); if (all) all.setAttribute("aria-pressed", (Body.mode === "3d" ? LAYERS3() : LAYERS).every((l) => Body.layers.has(l.k))); };
  const load3D = () => b3Loading || (b3Loading = import("./js/body3d.js").then((m) => (B3 = m)));
  const SIDE_WORD = { R: "Right ", L: "Left " };
  const DIGIT = { hand: ["thumb", "index finger", "middle finger", "ring finger", "little finger"], foot: ["great toe", "second toe", "third toe", "fourth toe", "little toe"] };
  const ORD = ["first", "second", "third", "fourth", "fifth"];
  // Z-Anatomy names -> everyday names ("Distal phalanx of first finger of foot" -> "Distal phalanx of the great toe")
  const US = [[/oesophag/gi, "esophag"], [/coeliac/gi, "celiac"], [/caec/gi, "cec"], [/haem/gi, "hem"], [/foet/gi, "fet"]];   // Z-Anatomy uses British spellings
  const partName = (n) => US.reduce((t, [rx, us]) => t.replace(rx, (m) => (m[0] === m[0].toUpperCase() ? us[0].toUpperCase() + us.slice(1) : us)), n)
    .replace(/of (first|second|third|fourth|fifth) finger of (hand|foot)/, (_, o, w) => "of the " + DIGIT[w][ORD.indexOf(o)]).replace(/^Vertebra ([CTL]\d+)$/, "$1 vertebra");
  const withSide = (side, n) => (SIDE_WORD[side] ? SIDE_WORD[side] + n.charAt(0).toLowerCase() + n.slice(1) : n);
  function info3DHTML() {
    const s = Body.sel3;
    if (!s || s.pending) return `<h3>Tap any structure</h3><p class="muted" style="margin:6px 0 0">Switch layers with the chips; each one downloads the first time you turn it on. Drag to turn, pinch or use the buttons to zoom, and drag with two fingers to move. Tap empty space to clear. Dermatomes and female pelvic organs are in Diagram.</p>`;
    const part = partName(s.name);
    if (s.key && INFO[s.key]) {
      const tapped = s.tapped && part.toLowerCase() !== INFO[s.key].n.toLowerCase() ? `<p class="small muted" style="margin:6px 0 0">You tapped: ${esc(withSide(s.side, part))}</p>` : "";
      return keyCardHTML(s.key, SIDE_WORD[s.side] || "", false, tapped);
    }
    const lay = LAYERS.find((l) => l.k === s.layer) || LAYERS[0];
    return `<div class="row wrap" style="margin-bottom:6px">${pill(lay.n, lay.c)}</div><h3>${esc(withSide(s.side, part))}</h3><p class="muted" style="margin:8px 0 0">No study card for this one yet.</p>`;
  }
  function mount3D() {
    const el = $("#fig3d"), msg = $("#load3d"); if (!el) return;
    mountSearch();
    const fail =(t) => { msg.hidden = false; msg.innerHTML = `<div>${esc(t)}<br><button class="btn ghost sm" style="margin-top:10px" data-act="body-mode" data-v="2d">Use Diagram</button></div>`; };
    if (location.protocol === "file:") { fail("The 3D view works when the app is opened from its web address."); return; }
    load3D().then((m) => {
      if (!m.supported()) { fail("3D needs WebGL 2, which this browser has turned off."); return; }
      if (!el.isConnected) return;
      const colors = Object.fromEntries(LAYERS.map((l) => [l.k, l.c]));
      return m.attach(el, { onPick: pick3D, onProgress: progress3D, t0: Body.t3, layers: layers3(), colors }).then(() => {
        if (!el.isConnected) return;
        msg.hidden = true; const st = $("#status3d"); if (st) st.hidden = true;
        apply3DPending();
      });
    }).catch((err) => { console.error(err); b3Loading = null; fail("The 3D model could not load. Check the connection, then switch to Diagram and back to try again."); });
  }
  function progress3D(layer, bytes) {
    const msg = $("#load3d"), st = $("#status3d");
    if (msg && !msg.hidden) msg.textContent = `Loading 3D anatomy… ${((B3 ? B3.stats.bytes : bytes) / 1048576).toFixed(1)} MB`;
    else if (st) { st.hidden = false; st.textContent = `Loading ${layerName(layer)}… ${(bytes / 1048576).toFixed(1)} MB`; }
  }
  function sync3DLayers() {
    if (!B3 || !B3.isReady()) return;              // mount3D passes the current layers when it attaches
    const st = $("#status3d"), want = layers3(), missing = want.filter((k) => !B3.loaded(k));
    if (st && missing.length) { st.hidden = false; st.textContent = `Loading ${missing.map(layerName).join(", ")}…`; }
    B3.setLayers(want).then(() => { if (st) st.hidden = true; })
      .catch((err) => { console.error(err); if (st) { st.hidden = false; st.textContent = "That layer could not load. Check the connection and try again."; } });
  }
  function pick3D(info) {
    const q = Body.quiz;
    if (q && q.three && !q.done) {                  // in the quiz, a tap answers; the asked structure stays highlighted
      if (!q.answered && info) quizPick(info.key || "");
      B3.selectKey(q.cur.key, q.cur.side, false);
      return;
    }
    Body.sel3 = info ? Object.assign({ tapped: true }, info) : null;
    const card = $("#infocard"); if (card) card.innerHTML = infoCardHTML();
  }
  function show3D(key) {
    Body.quiz = null; Body.sel3 = { key, pending: true };
    if (appHooks.tab() !== "anatomy" || UIA.tab !== "body") { UIA.tab = "body"; appHooks.go("anatomy"); return; } // mount3D applies it
    apply3DPending();
  }
  function apply3DPending() {
    const s = Body.sel3; if (!s || !s.pending || !B3 || !B3.isReady()) return;
    const lay = B3.layerOf(s.key);
    if (!lay) { Body.sel3 = null; Body.mode = "2d"; rerender(true); showOnBody(s.key); return; } // not in 3D
    if (!Body.layers.has(lay)) { Body.layers.add(lay); syncChips(); }
    const st = $("#status3d"); if (st && !B3.loaded(lay)) { st.hidden = false; st.textContent = `Loading ${layerName(lay)}…`; }
    B3.selectKey(s.key, "R", true).then((ok) => {
      if (st) st.hidden = true;
      if (Body.sel3 !== s) return;                  // superseded by a newer pick
      Body.sel3 = ok ? Object.assign({ tapped: false }, B3.current()) : null;
      const card = $("#infocard"); if (card) card.innerHTML = infoCardHTML();
    });
  }
  function applyFigState() {
    const svg = $("#fig"); if (!svg) return;
    LAYERS.forEach((l) => svg.classList.toggle("hide-" + l.k, !Body.layers.has(l.k)));
    svg.dataset.sex = Body.sex;
    $$(".st.sel", svg).forEach((e) => e.classList.remove("sel"));
    if (Body.sel) { const e = svg.querySelector(`[data-id="${Body.sel}"]`); if (e) e.classList.add("sel"); }
    svg.classList.toggle("has-sel", !!Body.sel);
    setVB(Body.vb);
  }
  function setVB(v) { const svg = $("#fig"); if (svg) svg.setAttribute("viewBox", `${v.x} ${v.y} ${v.w} ${v.h}`); }
  function clampVB(v) { const w = Math.min(Math.max(v.w, 60), 420), h = w * 2.3; return { x: Math.min(Math.max(v.x, -w * 0.5), 400 - w * 0.5), y: Math.min(Math.max(v.y, -h * 0.5), 920 - h * 0.5), w, h }; }
  let anim = null;
  function animateVB(to) {
    to = clampVB(to); cancelAnimationFrame(anim);
    if (reduceMotion) { Body.vb = to; setVB(to); return; }
    const from = Object.assign({}, Body.vb), t0 = performance.now(), dur = 280;
    const step = (t) => { const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3); Body.vb = { x: from.x + (to.x - from.x) * e, y: from.y + (to.y - from.y) * e, w: from.w + (to.w - from.w) * e, h: from.h + (to.h - from.h) * e }; setVB(Body.vb); if (k < 1) anim = requestAnimationFrame(step); };
    anim = requestAnimationFrame(step);
  }
  function zoomBy(f, cx, cy) { const v = Body.vb; if (cx == null) { cx = v.x + v.w / 2; cy = v.y + v.h / 2; } const w = Math.min(Math.max(v.w * f, 60), 420), h = w * 2.3; return clampVB({ x: cx - (cx - v.x) * (w / v.w), y: cy - (cy - v.y) * (h / v.h), w, h }); }
  function zoomToSel() {
    const el = $("#fig") && $("#fig").querySelector(`[data-id="${Body.sel}"]`); if (!el) return;
    const b = el.getBBox(); const flip = Body.view === "back";
    const cx = flip ? 400 - (b.x + b.width / 2) : b.x + b.width / 2, cy = b.y + b.height / 2;
    const w = Math.max(b.width * 2.4, (b.height * 2.4) / 2.3, 80);
    animateVB({ x: cx - w / 2, y: cy - (w * 2.3) / 2, w, h: w * 2.3 });
  }
  function structForKey(key, preferView) {
    const cands = FIG.structures.filter((o) => (o.info || o.id) === key && !o.noTap);
    return cands.find((o) => FIG.inView(o, preferView)) || cands[0] || null;
  }
  function selectStruct(dataId, zoom) {
    const base = dataId.replace(/-(r|l)$/, ""), so = ID2S[base]; if (!so) return;
    const key = so.info || so.id, inf = INFO[key]; if (!inf) return;
    if (!Body.layers.has(inf.L)) Body.layers.add(inf.L);
    if (so.sex && so.sex !== Body.sex) Body.sex = so.sex;
    Body.quiz = null; Body.sel = dataId;
    const needView = FIG.inView(so, Body.view) ? Body.view : (so.v || "f").includes("f") ? "front" : "back";
    if (needView !== Body.view) Body.view = needView;
    if (appHooks.tab() !== "anatomy" || UIA.tab !== "body") { UIA.tab = "body"; appHooks.go("anatomy"); }
    else {
      if ($("#fig").dataset.view !== Body.view) { $("#fig").innerHTML = markup(Body.view); $("#fig").dataset.view = Body.view; $(".viewtag").textContent = Body.view === "front" ? "Front" : "Back"; $("[data-act=rotate-body]").innerHTML = IC.rotate + (Body.view === "front" ? "Back" : "Front"); }
      $$("[data-act=layer]").forEach((b) => b.setAttribute("aria-pressed", Body.layers.has(b.dataset.v)));
      $$("[data-act=sex]").forEach((b) => b.setAttribute("aria-pressed", b.dataset.v === Body.sex));
    }
    applyFigState();
    const card = $("#infocard"); if (card) card.innerHTML = infoCardHTML();
    if (zoom) zoomToSel();
  }
  function showOnBody(key) {
    if (Body.mode === "3d") {
      if (!B3 || !B3.isReady() || B3.hasKey(key)) { show3D(key); return; }
      Body.mode = "2d"; // not in the 3D model yet: show it on the diagram
      if (appHooks.tab() === "anatomy" && UIA.tab === "body") rerender(true);
    }
    const so = structForKey(key, Body.view); if (!so) return;
    Body.vb = { x: 0, y: 0, w: 400, h: 920 };
    selectStruct(so.id + (so.mirror ? "-r" : ""), true);
  }
  function rotateBody() {
    const wrap = $("#figwrap"), svg = $("#fig"); if (!svg) return;
    const next = Body.view === "front" ? "back" : "front";
    const swap = () => {
      Body.view = next; svg.innerHTML = markup(next); svg.dataset.view = next;
      if (Body.sel) { const base = Body.sel.replace(/-(r|l)$/, ""), so = ID2S[base]; if (!so || !FIG.inView(so, next)) { const alt = so ? structForKey(so.info || so.id, next) : null; Body.sel = alt ? alt.id + (so.mirror ? Body.sel.slice(-2) : "") : null; } }
      applyFigState();
      $(".viewtag").textContent = next === "front" ? "Front" : "Back";
      $(".fig-note").textContent = next === "front" ? "Front view: their right is on your left. Dashed lines run on the back." : "Back view: their right is on your right. Dashed lines run on the front.";
      $("[data-act=rotate-body]").innerHTML = IC.rotate + (next === "front" ? "Back" : "Front");
      svg.setAttribute("aria-label", `Interactive anatomical figure, ${next} view`);
      const card = $("#infocard"); if (card && !Body.quiz) card.innerHTML = infoCardHTML();
    };
    if (reduceMotion) { swap(); return; }
    wrap.classList.add("flip-out");
    setTimeout(() => { swap(); wrap.classList.remove("flip-out"); wrap.classList.add("flip-in"); setTimeout(() => wrap.classList.remove("flip-in"), 260); }, 240);
  }
  function mountBody() {
    const svg = $("#fig"); if (!svg) return;
    svg.dataset.view = Body.view; applyFigState();
    const ptrs = new Map(); let start = null, moved = false, tapTarget = null;
    const scale = () => { const r = svg.getBoundingClientRect(); return Math.min(r.width / Body.vb.w, r.height / Body.vb.h); };
    const toSvg = (cx, cy) => { const r = svg.getBoundingClientRect(), sc = scale(); const ox = (r.width - Body.vb.w * sc) / 2, oy = (r.height - Body.vb.h * sc) / 2; return { x: Body.vb.x + (cx - r.left - ox) / sc, y: Body.vb.y + (cy - r.top - oy) / sc }; };
    svg.addEventListener("pointerdown", (e) => {
      ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY }); try { svg.setPointerCapture(e.pointerId); } catch (_) {}
      moved = false; tapTarget = e.target.closest ? e.target.closest(".st") : null;
      if (ptrs.size === 1) start = { vb: Object.assign({}, Body.vb), x: e.clientX, y: e.clientY };
      else if (ptrs.size === 2) { const [a, b] = [...ptrs.values()]; start = { vb: Object.assign({}, Body.vb), d: Math.hypot(a.x - b.x, a.y - b.y), c: toSvg((a.x + b.x) / 2, (a.y + b.y) / 2) }; moved = true; }
    });
    svg.addEventListener("pointermove", (e) => {
      if (!ptrs.has(e.pointerId) || !start) return;
      ptrs.set(e.pointerId, { x: e.clientX, y: e.clientY });
      if (ptrs.size === 1 && start.x != null) {
        const dx = e.clientX - start.x, dy = e.clientY - start.y; if (!moved && Math.hypot(dx, dy) < 6) return;
        moved = true; const sc = scale(); Body.vb = clampVB({ x: start.vb.x - dx / sc, y: start.vb.y - dy / sc, w: start.vb.w, h: start.vb.h }); setVB(Body.vb);
      } else if (ptrs.size === 2 && start.d) {
        const [a, b] = [...ptrs.values()]; const d = Math.hypot(a.x - b.x, a.y - b.y); if (!d) return;
        const w = Math.min(Math.max(start.vb.w * (start.d / d), 60), 420), h = w * 2.3, c = start.c;
        Body.vb = clampVB({ x: c.x - (c.x - start.vb.x) * (w / start.vb.w), y: c.y - (c.y - start.vb.y) * (h / start.vb.h), w, h }); setVB(Body.vb);
      }
    });
    const end = (e) => {
      if (!ptrs.has(e.pointerId)) return; ptrs.delete(e.pointerId);
      if (ptrs.size === 0) {
        if (!moved && e.type === "pointerup") {
          if (Body.quiz) { if (tapTarget) quizTap(tapTarget.dataset.id); }
          else if (tapTarget) selectStruct(tapTarget.dataset.id, false);
          else if (Body.sel) { Body.sel = null; applyFigState(); $("#infocard").innerHTML = infoCardHTML(); }
        }
        start = null;
      } else if (ptrs.size === 1) { const [p] = [...ptrs.values()]; start = { vb: Object.assign({}, Body.vb), x: p.x, y: p.y }; }
    };
    svg.addEventListener("pointerup", end); svg.addEventListener("pointercancel", end);
    svg.addEventListener("wheel", (e) => { e.preventDefault(); const c = toSvg(e.clientX, e.clientY); Body.vb = zoomBy(e.deltaY > 0 ? 1.12 : 1 / 1.12, c.x, c.y); setVB(Body.vb); }, { passive: false });
    mountSearch();
  }
  function mountSearch() {
    const inp = $("#bsearch"); if (!inp) return;
    inp.addEventListener("input", () => { Body.q = inp.value; renderSearch(); });
    inp.addEventListener("focus", renderSearch);
    inp.addEventListener("keydown", (e) => { if (e.key === "Enter") { const f = $("#bresults button"); if (f) f.click(); } if (e.key === "Escape") $("#bresults").innerHTML = ""; });
  }
  function renderSearch() {
    const q = Body.q.trim().toLowerCase(), box = $("#bresults"); if (!box) return;
    if (!q) { box.innerHTML = ""; return; }
    const hits = searchDict(q).filter((e) => e.model === "body").slice(0, 8);
    box.innerHTML = hits.length ? `<div class="sresults">${hits.map((e) => { const l = layerOf(e.id); return `<button data-act="bpick" data-key="${e.id}"><span class="dot" style="background:${l ? l.c : "#999"}"></span><span>${esc(e.name)}</span><span class="spacer"></span><span class="muted small">${esc(e.sub)}</span></button>`; }).join("")}</div>` : `<div class="sresults"><button disabled><span class="muted">No match. Try the Index tab to browse everything.</span></button></div>`;
  }
  /* identify quiz on the body */
  function quizPool() { return STRUCTS.filter((o) => FIG.inView(o, Body.view) && Body.layers.has(INFO[o.info || o.id].L) && (!o.sex || o.sex === Body.sex) && INFO[o.info || o.id].L !== "derm"); }
  function startIdQuiz() {
    if (Body.mode === "3d") {
      if (!B3 || !B3.isReady()) return;
      const pool = B3.quizPool();
      if (new Set(pool.map((p) => p.key)).size < 4) { appHooks.toast("Turn on a few more layers first."); return; }
      Body.quiz = { pool, n: 0, score: 0, total: 8, cur: null, answered: false, three: true }; nextIdQuestion(); return;
    }
    const pool = quizPool(); if (pool.length < 4) { appHooks.toast("Turn on a few more layers first."); return; }
    Body.quiz = { pool, n: 0, score: 0, total: 8, cur: null, answered: false }; nextIdQuestion();
  }
  function nextIdQuestion() {
    const q = Body.quiz; if (!q) return;
    if (q.n >= q.total) { q.done = true; if (q.three) { B3.clear(); Body.sel3 = null; } else { Body.sel = null; applyFigState(); } $("#infocard").innerHTML = quizCard(); return; }
    if (q.three) {
      const o = q.pool[Math.floor(Math.random() * q.pool.length)];
      const others = shuffle([...new Set(q.pool.map((p) => p.key))].filter((k) => k !== o.key)).slice(0, 3);
      q.cur = { key: o.key, side: o.side, opts: shuffle([o.key, ...others]) }; q.answered = false; q.n++;
      B3.selectKey(o.key, o.side, true);
      $("#infocard").innerHTML = quizCard(); return;
    }
    const o = q.pool[Math.floor(Math.random() * q.pool.length)]; const key = o.info || o.id;
    const others = shuffle(q.pool.filter((x) => (x.info || x.id) !== key).map((x) => x.info || x.id).filter((v, i, a) => a.indexOf(v) === i)).slice(0, 3);
    q.cur = { key, opts: shuffle([key, ...others]) }; q.answered = false; q.n++;
    Body.sel = o.id + (o.mirror ? "-r" : ""); applyFigState(); zoomToSel();
    $("#infocard").innerHTML = quizCard();
  }
  function quizCard() {
    const q = Body.quiz; if (!q) return infoCardHTML();
    if (q.done) return `<h3>${q.score} of ${q.total} named correctly</h3><p class="muted" style="margin:6px 0 10px">Each round draws from the layers you have turned on, so switch layers for a different set.</p><div class="row"><button class="btn sm" data-act="id-quiz">Play again</button><button class="btn ghost sm" data-act="id-quiz-stop">Done</button></div>`;
    const c = q.cur;
    return `<div class="row" style="margin-bottom:6px"><span class="pill">Name that structure</span><span class="muted small">${q.n} of ${q.total}</span><span class="spacer"></span><button class="btn quiet sm" data-act="id-quiz-stop">Stop</button></div>
      <p style="margin:0 0 10px">Which structure is highlighted?</p><div class="quiz-opts">${c.opts.map((k) => `<button data-act="id-pick" data-key="${k}" ${q.answered ? "disabled" : ""} class="${q.answered ? (k === c.key ? "ok" : k === q.picked ? "bad" : "") : ""}">${esc(INFO[k].n)}</button>`).join("")}</div>
      ${q.answered ? `<p style="margin:12px 0 0"><b>${q.picked === c.key ? "Correct." : "Not quite."}</b> ${esc(INFO[c.key].p)}</p><button class="btn block" style="margin-top:10px" data-act="id-next">${q.n < q.total ? "Next" : "See score"}</button>` : ""}`;
  }
  function quizPick(key) { const q = Body.quiz; if (!q || q.answered) return; q.answered = true; q.picked = key; if (key === q.cur.key) q.score++; $("#infocard").innerHTML = quizCard(); }
  function quizTap(dataId) { const base = dataId.replace(/-(r|l)$/, ""), so = ID2S[base]; if (so) quizPick(so.info || so.id); }

  /* ================= BRAIN ================= */
  function brainFigure() {
    const sm = CR;
    const shape = (a, cls, extra) => {
      let geo;
      if (a.pts) geo = `<path d="${sm(a.pts, true)}" fill="${a.c}" ${extra || ""}/>`;
      else if (a.ellipse) geo = `<ellipse cx="${a.ellipse[0]}" cy="${a.ellipse[1]}" rx="${a.ellipse[2]}" ry="${a.ellipse[3]}" fill="${a.c}" ${extra || ""}/>`;
      else if (a.line) geo = `<path d="${sm(a.line, false)}" fill="none" stroke="${a.c}" stroke-width="${a.w || 3}" stroke-linecap="round"/>` + `<path d="${sm(a.line, false)}" fill="none" stroke="transparent" stroke-width="12"/>`;
      return `<g class="bp ${cls} ${Brain.sel === a.id ? "sel" : ""}" data-act="brain-pick" data-v="${a.id}" role="button" tabindex="0" aria-label="${esc(a.n)}">${geo}</g>`;
    };
    let g = `<g class="lobes">${BRAIN.lobes.map((l) => shape(l, "lobe", 'stroke="rgba(60,40,40,.45)" stroke-width="1"')).join("")}</g>`;
    g += `<g class="sulci" fill="none" stroke="rgba(60,40,40,.5)" stroke-width="1.2"><path d="M60 118 C90 110 120 98 150 92 M70 136 C100 130 130 120 160 112 M210 76 C240 86 262 96 286 102 M226 104 C250 110 272 118 290 126 M110 190 C150 184 190 182 230 176 M96 176 C136 172 176 168 216 164"/></g>`;
    g += `<g class="areas">${BRAIN.areas.map((a) => shape(a, "area", 'opacity=".88" stroke="rgba(0,0,0,.25)" stroke-width=".8"')).join("")}</g>`;
    if (Brain.terr) g += `<g class="terr">${BRAIN.territories.map((t) => shape(t, "terr", 'stroke="rgba(0,0,0,.35)" stroke-width="1" stroke-dasharray="3 2"')).join("")}</g>`;
    g += `<g class="blab" pointer-events="none"><text x="100" y="98">Frontal</text><text x="236" y="98">Parietal</text><text x="150" y="190">Temporal</text><text x="302" y="150" text-anchor="middle">Occipital</text><text x="262" y="232">Cerebellum</text><text x="172" y="268">Brainstem</text><text x="70" y="40" class="dir">Front</text><text x="300" y="40" class="dir">Back</text></g>`;
    return `<svg class="brainfig ${Brain.sel ? "has-sel" : ""}" viewBox="20 20 320 285" role="img" aria-label="Left side of the brain, lateral view">${g}</svg>`;
  }
  function brainHTML() {
    let h = `<div class="row" style="margin:14px 0 10px"><button class="btn ghost sm" data-act="rotate-brain">${IC.rotate}${Brain.view === "lateral" ? "Underside" : "Side view"}</button><span class="spacer"></span>${Brain.view === "lateral" ? `<button class="chip" data-act="brain-terr" aria-pressed="${Brain.terr}">Arterial territories</button>` : ""}</div>`;
    if (Brain.view === "lateral") {
      h += `<div class="fig-wrap brainwrap" id="brainwrap" style="padding:8px">${brainFigure()}</div>
        <div class="scrollx" style="margin-top:12px" role="group" aria-label="Functional areas">${BRAIN.areas.map((a) => `<button class="chip" data-act="brain-pick" data-v="${a.id}" aria-pressed="${Brain.sel === a.id}"><span class="dot" style="background:${a.c}"></span>${esc(a.n.split(" (")[0])}</button>`).join("")}</div>
        <div class="panel infocard" id="braincard" style="margin-top:12px" aria-live="polite">${brainCard()}</div>`;
    } else {
      h += `<p class="hint" style="margin:0 2px 10px">The underside of the brain, where the twelve cranial nerves emerge. Tap a nerve or a numeral.</p>
        <div class="fig-wrap" style="padding:8px">${cnFigure()}<div class="legend" style="justify-content:center;margin:2px 0 6px"><span><span class="tdot type-S"></span> Sensory</span><span><span class="tdot type-M"></span> Motor</span><span><span class="tdot type-B"></span> Both</span></div></div>
        <div class="scrollx" style="margin-top:12px" role="group" aria-label="Cranial nerves">${CN.map((x) => `<button class="chip cnchip type-${x.type}" data-act="cn" data-v="${x.num}" aria-pressed="${Brain.cn === x.num}"><span class="tdot"></span>${x.num}</button>`).join("")}</div>
        <div class="panel infocard" id="cncard" style="margin-top:12px" aria-live="polite">${cnCard()}</div>
        <button class="btn block" style="margin-top:12px" data-act="cn-quiz">Quiz me on cranial nerves</button>
        <h2>Memory aids</h2><div class="panel mnem">
        <p><b>Names:</b> Oh Oh Oh To Touch And Feel Very Good Velvet, Such Heaven.</p>
        <p><b>Sensory, motor, or both:</b> Some Say Marry Money But My Brother Says Big Brains Matter More.</p>
        <p><b>Trigeminal exits:</b> Standing Room Only: V1 superior orbital fissure, V2 foramen rotundum, V3 foramen ovale.</p>
        <p><b>Brainstem levels:</b> III and IV leave the midbrain; V to VIII arise at the pons; IX, X, and XII leave the medulla (XI comes from the upper cervical cord).</p>
        <p style="margin:0"><b>Cavernous sinus:</b> III, IV, V1, V2, and VI, plus the internal carotid artery; VI sits free beside the artery.</p></div>`;
    }
    return h;
  }
  function brainCard() {
    const a = BRAIN.lobes.concat(BRAIN.areas, BRAIN.territories).find((x) => x.id === Brain.sel);
    if (!a) return `<h3>Tap a region</h3><p class="muted" style="margin:6px 0 0">Lobes, the main functional areas, and (with the toggle) the three arterial territories. Each card ends with the stroke or lesion syndrome to know for boards.</p>`;
    const kind = BRAIN.territories.includes(a) ? "Arterial territory" : BRAIN.lobes.includes(a) ? "Lobe" : "Functional area";
    return cardHTML(a.n, pill(kind, a.c.startsWith("rgba") ? null : a.c), a.d, a.p, `<p style="margin:8px 0 0"><button class="btn quiet sm" style="padding:0" data-act="dict-go" data-id="br_${a.id}">Open in the index</button></p>`);
  }
  function selectBrain(id) {
    if (BRAIN.territories.some((t) => t.id === id)) Brain.terr = true;
    Brain.sel = Brain.sel === id ? null : id;
    if (appHooks.tab() !== "anatomy" || UIA.tab !== "brain" || Brain.view !== "lateral") { UIA.tab = "brain"; Brain.view = "lateral"; appHooks.go("anatomy"); return; }
    $("#brainwrap").innerHTML = brainFigure();
    $$("[data-act=brain-pick].chip").forEach((b) => b.setAttribute("aria-pressed", b.dataset.v === Brain.sel));
    const t = $("[data-act=brain-terr]"); if (t) t.setAttribute("aria-pressed", Brain.terr);
    $("#braincard").innerHTML = brainCard();
  }
  function rotateBrain() {
    const next = Brain.view === "lateral" ? "underside" : "lateral";
    const wrap = $(".brainwrap") || $(".fig-wrap");
    if (reduceMotion || !wrap) { Brain.view = next; rerender(true); return; }
    wrap.classList.add("flip-out"); setTimeout(() => { Brain.view = next; rerender(true); const w2 = $(".fig-wrap"); if (w2) { w2.classList.add("flip-in"); setTimeout(() => w2.classList.remove("flip-in"), 260); } }, 240);
  }
  /* cranial nerves (underside) */
  const CN_COLORS = { S: "#2C7FB8", M: "#D7473B", B: "#8E5CC4" };
  function cnFigure() {
    const mx = (pts) => pts.map(([x, y]) => [360 - x, y]);
    const sm = (pts) => { let d = "M" + pts[0][0] + " " + pts[0][1]; for (let i = 1; i < pts.length; i++) { const p0 = pts[i - 1], p1 = pts[i]; d += ` Q${p0[0]} ${p0[1]} ${(p0[0] + p1[0]) / 2} ${(p0[1] + p1[1]) / 2}`; } const l = pts[pts.length - 1]; return d + ` L${l[0]} ${l[1]}`; };
    const nerves = {
      I: { lines: [[[164, 44], [161, 80], [158, 112]]], w: 3, extra: (m) => `<ellipse cx="${m ? 196 : 164}" cy="32" rx="6.5" ry="11" />`, lab: [128, 40] },
      II: { lines: [[[132, 92], [156, 108], [176, 124]], [[176, 124], [162, 140], [152, 156]]], w: 4.5, lab: [116, 92] },
      III: { lines: [[[173, 164], [148, 146], [118, 128]]], w: 3, lab: [104, 126] },
      IV: { lines: [[[156, 176], [146, 166], [124, 152], [102, 146]]], w: 1.8, lab: [88, 148] },
      V: { lines: [[[141, 206], [112, 205]], [[104, 205], [82, 176]], [[104, 205], [74, 205]], [[104, 205], [82, 233]]], w: 4.5, extra: (m) => `<ellipse cx="${m ? 256 : 104}" cy="205" rx="7" ry="10"/>`, lab: [52, 210] },
      VI: { lines: [[[173, 240], [167, 222], [158, 202], [144, 186], [128, 176]]], w: 2.2, lab: [114, 176] },
      VII: { lines: [[[147, 240], [126, 243], [108, 246]]], w: 2.6, lab: [90, 249] },
      VIII: { lines: [[[144, 247], [126, 254], [108, 262]]], w: 2.6, lab: [82, 266] },
      IX: { lines: [[[147, 258], [128, 268], [108, 278]]], w: 2.2, lab: [90, 283] },
      X: { lines: [[[146, 264], [124, 284]], [[146, 271], [124, 284]], [[146, 278], [124, 284]], [[124, 284], [106, 294]]], w: 2.2, lab: [92, 299] },
      XI: { lines: [[[166, 384], [162, 350], [150, 318], [128, 304], [106, 310]]], w: 2.2, lab: [86, 315] },
      XII: { lines: [[[160, 260], [146, 300]], [[160, 268], [146, 300]], [[160, 276], [146, 300]], [[146, 300], [118, 326]]], w: 2.2, lab: [96, 332] },
    };
    let base = `<g fill="var(--surface2)" stroke="var(--line)" stroke-width="1.5"><ellipse cx="136" cy="80" rx="54" ry="66"/><ellipse cx="224" cy="80" rx="54" ry="66"/><ellipse cx="84" cy="196" rx="40" ry="62" transform="rotate(-12 84 196)"/><ellipse cx="276" cy="196" rx="40" ry="62" transform="rotate(12 276 196)"/><ellipse cx="116" cy="322" rx="62" ry="46"/><ellipse cx="244" cy="322" rx="62" ry="46"/></g>
      <g fill="var(--surface)" stroke="var(--muted)" stroke-width="1.2" stroke-opacity=".6"><path d="M156 150 L204 150 L212 176 L148 176 Z"/><rect x="138" y="172" width="84" height="68" rx="30"/><path d="M152 238 L208 238 L198 332 L162 332 Z"/><rect x="168" y="330" width="24" height="70" rx="6"/><path d="M164 242 L178 242 L177 320 L167 320 Z"/><path d="M182 242 L196 242 L193 320 L183 320 Z"/><ellipse cx="152" cy="270" rx="6" ry="16"/><ellipse cx="208" cy="270" rx="6" ry="16"/><circle cx="180" cy="139" r="4.5"/><circle cx="174" cy="157" r="3.6"/><circle cx="186" cy="157" r="3.6"/><path d="M150 190 Q180 196 210 190 M148 206 Q180 212 212 206 M150 222 Q180 228 210 222" fill="none"/></g>
      <g fill="var(--muted)" opacity=".9"><text x="227" y="166" style="font-size:10px;font-weight:400">Midbrain</text><text x="226" y="210" style="font-size:10px;font-weight:400">Pons</text><text x="212" y="300" style="font-size:10px;font-weight:400">Medulla</text><text x="198" y="392" style="font-size:10px;font-weight:400">Spinal cord</text></g>`;
    let ns = "";
    CN.forEach((c) => {
      const d = nerves[c.num], col = CN_COLORS[c.type]; let g = "";
      [false, true].forEach((m) => { d.lines.forEach((ln) => { const pts = m ? mx(ln) : ln; const dd = sm(pts); g += `<path d="${dd}" class="hit" fill="none" stroke="transparent" stroke-width="12"/><path d="${dd}" fill="none" stroke="${col}" stroke-width="${d.w}" stroke-linecap="round"/>`; }); if (d.extra) g += `<g fill="${col}" stroke="none">${d.extra(m)}</g>`; });
      if (c.num === "II") g += `<path d="M168 124 L192 124" stroke="${col}" stroke-width="6" stroke-linecap="round"/>`;
      g += `<text x="${d.lab[0]}" y="${d.lab[1]}" text-anchor="middle">${c.num}</text>`;
      ns += `<g class="cn ${Brain.cn === c.num ? "sel" : ""}" data-act="cn" data-v="${c.num}" role="button" tabindex="0" aria-label="Cranial nerve ${c.num}, ${c.name}">${g}</g>`;
    });
    return `<svg class="cnfig ${Brain.cn ? "has-sel" : ""}" viewBox="20 10 320 400" role="img" aria-label="Underside of the brain showing the twelve cranial nerves">${base}${ns}</svg>`;
  }
  function cnCard() {
    const c = CN.find((x) => x.num === Brain.cn);
    if (!c) return `<h3 style="margin:0">Pick a nerve</h3><p class="muted" style="margin:6px 0 0">Each card covers where it leaves the skull, what it does, how to test it, what damage looks like, and a board pearl.</p>`;
    return `<div class="row" style="margin-bottom:4px"><span class="pill type-${c.type}"><span class="tdot"></span>${CN_TYPES[c.type]}</span></div><h3>CN ${c.num}: ${esc(c.name)}</h3>
      <dl class="kv"><dt>Leaves skull</dt><dd>${esc(c.exit)}</dd><dt>Arises from</dt><dd>${esc(c.from)}</dd><dt>Does</dt><dd>${esc(c.fn)}</dd><dt>Test it</dt><dd>${esc(c.test)}</dd><dt>If damaged</dt><dd>${esc(c.lesion)}</dd></dl>
      <div class="callout"><b>Clinical pearl.</b> ${esc(c.pearl)}</div><p style="margin:8px 0 0"><button class="btn quiet sm" style="padding:0" data-act="dict-go" data-id="cn_${c.num}">Open in the index</button></p>`;
  }
  function selectCN(n) {
    Brain.cn = Brain.cn === n ? null : n;
    if (appHooks.tab() !== "anatomy" || UIA.tab !== "brain" || Brain.view !== "underside") { UIA.tab = "brain"; Brain.view = "underside"; appHooks.go("anatomy"); return; }
    rerender(true);
  }
  const cnLabel = (n) => { const c = CN.find((x) => x.num === n); return `CN ${n} (${c.name})`; };
  function buildCNQuiz() {
    const pool = [];
    CN_FACTS.forEach(([m, n]) => pool.push({ q: `Which cranial nerve supplies the ${m.charAt(0).toLowerCase() + m.slice(1)}?`, a: n }));
    CN_FUNCS.forEach(([f, n]) => pool.push({ q: `${f}: which cranial nerve?`, a: n }));
    CN_EXITS.forEach(([f, n]) => pool.push({ q: `Which cranial nerve passes through the ${f.toLowerCase()}?`, a: n }));
    CN.forEach((c) => pool.push({ q: `Which cranial nerve is damaged? ${c.lesion}`, a: c.num }));
    return shuffle(pool).slice(0, 10).map((x) => { const others = shuffle(CN.map((c) => c.num).filter((n) => n !== x.a)).slice(0, 3); return Object.assign(x, { opts: shuffle([x.a, ...others]) }); });
  }
  function openCNQuiz() { Quiz.qs = buildCNQuiz(); Quiz.i = 0; Quiz.score = 0; Quiz.answered = false; appHooks.openSheet("Cranial nerve quiz", ""); renderCNQuiz(); }
  function renderCNQuiz() {
    const b = appHooks.sheetBody(); if (!b) return;
    if (Quiz.i >= Quiz.qs.length) { b.innerHTML = `<p class="quiz-q">${Quiz.score} of ${Quiz.qs.length} correct</p><p class="muted">${Quiz.score >= 8 ? "Strong work." : "Each round draws new questions, so run it again to fill the gaps."}</p><div class="row" style="margin-top:14px"><button class="btn" data-act="quiz-again" data-autofocus>New round</button><button class="btn ghost" data-act="sheet-close">Done</button></div>`; return; }
    const x = Quiz.qs[Quiz.i];
    b.innerHTML = `<p class="muted small" style="margin:0">Question ${Quiz.i + 1} of ${Quiz.qs.length}</p><p class="quiz-q">${esc(x.q)}</p><div class="quiz-opts">${x.opts.map((n, i) => `<button data-act="quiz-pick" data-i="${i}">${cnLabel(n)}</button>`).join("")}</div><div id="quizfb" style="margin-top:14px"></div>`;
  }
  function cnQuizPick(i) {
    if (Quiz.answered) return; const x = Quiz.qs[Quiz.i], picked = x.opts[i]; Quiz.answered = true; const ok = picked === x.a; if (ok) Quiz.score++;
    $$(".quiz-opts button").forEach((btn, j) => { btn.disabled = true; if (x.opts[j] === x.a) btn.classList.add("ok"); else if (j === i) btn.classList.add("bad"); });
    $("#quizfb").innerHTML = `<p style="margin:0 0 10px"><b>${ok ? "Correct." : "Not quite."}</b> The answer is ${cnLabel(x.a)}.</p><button class="btn block" data-act="quiz-next" data-autofocus>${Quiz.i < Quiz.qs.length - 1 ? "Next question" : "See score"}</button>`;
    $("#quizfb .btn").focus();
  }

  /* ================= HEART ================= */
  function heartFigure() {
    const pathOf = (pts, closed) => { let d = "M" + pts[0][0] + " " + pts[0][1]; for (let i = 1; i < pts.length; i++) d += " L" + pts[i][0] + " " + pts[i][1]; return d + (closed ? "Z" : ""); };
    const smoothC = (pts) => { const n = pts.length; let d = "M" + pts[0][0] + " " + pts[0][1]; for (let i = 0; i < n; i++) { const p1 = pts[i], p2 = pts[(i + 1) % n]; const m = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]; d += ` Q${p1[0]} ${p1[1]} ${m[0]} ${m[1]}`; } return d + "Z"; };
    const parts = Heart.view === "outside" ? HEART.outside : HEART.inside;
    const out = parts.map((p) => {
      let geo = "";
      if (p.pts) geo = `<path d="${Heart.view === "outside" ? CR(p.pts, true) : pathOf(p.pts, true)}" fill="${p.c}" stroke="rgba(40,10,10,.45)" stroke-width="1"/>`;
      else if (p.ellipse) geo = `<ellipse cx="${p.ellipse[0]}" cy="${p.ellipse[1]}" rx="${p.ellipse[2]}" ry="${p.ellipse[3]}" fill="${p.c}" stroke="rgba(40,10,10,.5)" stroke-width="1"/>`;
      else if (p.line) geo = `<path d="${CR(p.line, false)}" fill="none" stroke="transparent" stroke-width="${(p.w || 3) + 10}"/><path d="${CR(p.line, false)}" fill="none" stroke="${p.c}" stroke-width="${p.w || 3}" stroke-linecap="round" stroke-linejoin="round"/>`;
      else if (p.parts) geo = p.parts.map((pp) => p.w ? `<path d="${pathOf(pp, false)}" fill="none" stroke="transparent" stroke-width="${p.w + 10}"/><path d="${pathOf(pp, false)}" fill="none" stroke="${p.c}" stroke-width="${p.w}" stroke-linecap="round"/>` : `<path d="${pathOf(pp, true)}" fill="${p.c}" stroke="rgba(40,10,10,.5)" stroke-width="1"/>`).join("");
      return `<g class="hp ${Heart.sel === p.id ? "sel" : ""}" data-act="heart-pick" data-v="${p.id}" role="button" tabindex="0" aria-label="${esc(p.n)}">${geo}</g>`;
    }).join("");
    let deco = "";
    if (Heart.view === "inside") {
      deco = `<defs><marker id="arB" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5 0 10Z" fill="#3262C8"/></marker><marker id="arR" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5 0 10Z" fill="#D2352E"/></marker></defs>
        <g fill="none" stroke-width="2.4" stroke-linecap="round" pointer-events="none" opacity=".85"><path d="M112 96 L112 136" stroke="#3262C8" marker-end="url(#arB)"/><path d="M118 176 L118 214" stroke="#3262C8" marker-end="url(#arB)"/><path d="M98 176 C90 160 86 140 82 112" stroke="#3262C8" marker-end="url(#arB)"/><path d="M196 96 L196 136" stroke="#D2352E" marker-end="url(#arR)"/><path d="M190 180 L190 218" stroke="#D2352E" marker-end="url(#arR)"/><path d="M206 158 C214 136 220 120 232 100" stroke="#D2352E" marker-end="url(#arR)"/></g>
        <g class="blab" pointer-events="none"><text x="86" y="72">From body</text><text x="236" y="72" text-anchor="end">From lungs</text><text x="62" y="108">To lungs</text><text x="252" y="96" text-anchor="end">To body</text><text x="112" y="124" class="dir">RA</text><text x="192" y="124" class="dir">LA</text><text x="114" y="236" class="dir">RV</text><text x="195" y="236" class="dir">LV</text></g>`;
    } else {
      deco = `<g class="blab" pointer-events="none"><text x="104" y="140" class="dir">RA</text><text x="150" y="208" class="dir">RV</text><text x="222" y="200" class="dir">LV</text><text x="196" y="46" class="dir">Aorta</text><text x="132" y="112" class="dir">PT</text></g>`;
    }
    return `<svg class="heartfig ${Heart.sel ? "has-sel" : ""}" viewBox="40 20 230 270" role="img" aria-label="Heart, ${Heart.view} view">${out}${deco}</svg>`;
  }
  function heartHTML() {
    return `<div class="row" style="margin:14px 0 10px"><button class="btn ghost sm" data-act="rotate-heart">${IC.rotate}${Heart.view === "outside" ? "Open it up" : "Close it"}</button><span class="hint">${Heart.view === "outside" ? "Front of the heart with the coronary arteries." : "Four chambers, valves, and the conduction system."}</span></div>
      <div class="fig-wrap" id="heartwrap" style="padding:6px">${heartFigure()}</div>
      <div class="scrollx" style="margin-top:12px" role="group" aria-label="Heart parts">${(Heart.view === "outside" ? HEART.outside : HEART.inside).map((p) => `<button class="chip" data-act="heart-pick" data-v="${p.id}" aria-pressed="${Heart.sel === p.id}"><span class="dot" style="background:${p.c}"></span>${esc(p.n.split(" (")[0])}</button>`).join("")}</div>
      <div class="panel infocard" id="heartcard" style="margin-top:12px" aria-live="polite">${heartCard()}</div>`;
  }
  function heartCard() {
    const p = HEART.outside.concat(HEART.inside).find((x) => x.id === Heart.sel);
    if (!p) return `<h3>Tap a part of the heart</h3><p class="muted" style="margin:6px 0 0">Outside: chambers, great vessels, and the three coronary arteries with their ECG territories. Inside: valves, septa, papillary muscles, and the conduction system.</p>`;
    return cardHTML(p.n, pill(Heart.view === "outside" ? "Outside view" : "Inside view", p.c), p.d, p.p, `<p style="margin:8px 0 0"><button class="btn quiet sm" style="padding:0" data-act="dict-go" data-id="ht_${p.id}">Open in the index</button></p>`);
  }
  function selectHeart(id, view) {
    const target = view || (HEART.outside.some((p) => p.id === id) ? "outside" : "inside");
    Heart.sel = Heart.sel === id && Heart.view === target ? null : id; Heart.view = target;
    if (appHooks.tab() !== "anatomy" || UIA.tab !== "heart") { UIA.tab = "heart"; appHooks.go("anatomy"); return; }
    rerender(true);
  }
  function rotateHeart() {
    const next = Heart.view === "outside" ? "inside" : "outside"; const wrap = $("#heartwrap");
    if (reduceMotion || !wrap) { Heart.view = next; Heart.sel = null; rerender(true); return; }
    wrap.classList.add("flip-out"); setTimeout(() => { Heart.view = next; Heart.sel = null; rerender(true); const w2 = $("#heartwrap"); if (w2) { w2.classList.add("flip-in"); setTimeout(() => w2.classList.remove("flip-in"), 260); } }, 240);
  }

  /* ================= INDEX (dictionary) ================= */
  function searchDict(q) {
    q = q.toLowerCase();
    const rank = (e) => { const n = e.name.toLowerCase(), i = n.indexOf(q); if (i === 0) return 0; if (i > 0) return (n[i - 1] === " " || n[i - 1] === "(") ? 1 : 2; const inf = INFO[e.id]; const txt = inf ? (inf.d + " " + inf.p).toLowerCase() : ""; return txt.includes(q) ? 3 : 9; };
    return DICT.map((e) => [e, rank(e)]).filter(([, r]) => r < 9).sort((a, b) => a[1] - b[1] || a[0].name.length - b[0].name.length).map(([e]) => e);
  }
  function indexHTML() {
    const filters = [["all", "Everything"], ["body", "Body"], ["derm", "Dermatomes"], ["brain", "Brain"], ["cn", "Cranial nerves"], ["heart", "Heart"]];
    let list = Idx.q.trim() ? searchDict(Idx.q.trim()) : DICT;
    if (Idx.filter === "derm") list = list.filter((e) => e.sub === "Dermatome");
    else if (Idx.filter === "cn") list = list.filter((e) => e.sub === "Cranial nerve");
    else if (Idx.filter === "body") list = list.filter((e) => e.model === "body" && e.sub !== "Dermatome");
    else if (Idx.filter !== "all") list = list.filter((e) => e.model === Idx.filter && e.sub !== "Cranial nerve");
    let h = `<input class="search" style="margin-top:14px" type="search" id="idxsearch" placeholder="Search ${DICT.length} entries" aria-label="Search the index" value="${esc(Idx.q)}">
      <div class="scrollx" style="margin-top:10px" role="group" aria-label="Filter">${filters.map(([k, n]) => `<button class="chip" data-act="idx-filter" data-v="${k}" aria-pressed="${Idx.filter === k}">${n}</button>`).join("")}</div>
      <p class="hint" style="margin:10px 2px 6px">${list.length} entr${list.length === 1 ? "y" : "ies"}. Tap one to see it highlighted on its model.</p><div id="idxlist">`;
    h += indexListHTML(list) + `</div>`;
    return h;
  }
  function indexListHTML(list) {
    if (!list.length) return `<p class="muted">No match.</p>`;
    const sortKey = (s) => s.replace(/^(right|left) /i, "");
    let out = "", letter = "";
    const useLetters = !Idx.q.trim();
    list.forEach((e) => {
      const L = sortKey(e.name).charAt(0).toUpperCase();
      if (useLetters && L !== letter) { letter = L; out += `${out ? "</div>" : ""}<div class="idx-letter">${L}</div><div class="list">`; }
      else if (!out) out += `<div class="list">`;
      const col = e.model === "body" ? (layerOf(e.id) || { c: "#999" }).c : e.model === "brain" ? "#8E5CC4" : "#D2352E";
      out += `<button class="li" data-act="dict-go" data-id="${e.id}"><span class="dot" style="width:10px;height:10px;border-radius:50%;background:${col};flex:none"></span><div class="t"><b>${esc(e.name)}</b><span>${esc(e.sub)}</span></div>${IC.right}</button>`;
    });
    return out + "</div>";
  }
  function openEntry(id) {
    const e = DICT.find((x) => x.id === id); if (!e) return;
    const t = e.target;
    if (t.kind === "body") showOnBody(t.key);
    else if (t.kind === "cn") { Brain.cn = t.num; UIA.tab = "brain"; Brain.view = "underside"; appHooks.go("anatomy"); }
    else if (t.kind === "brain") { Brain.sel = t.id; if (BRAIN.territories.some((x) => x.id === t.id)) Brain.terr = true; UIA.tab = "brain"; Brain.view = "lateral"; appHooks.go("anatomy"); }
    else if (t.kind === "heart") { Heart.sel = t.id; Heart.view = t.view; UIA.tab = "heart"; appHooks.go("anatomy"); }
  }

  /* ================= BONES ================= */
  function bonesHTML() {
    const total = BONES.reduce((a, g) => a + g.items.reduce((b, it) => b + it[1], 0), 0);
    const axial = BONES.filter((g) => g.axial).reduce((a, g) => a + g.items.reduce((b, it) => b + it[1], 0), 0);
    return `<div class="panel" style="margin-top:14px"><h3 style="margin:0">${total} bones in the adult skeleton</h3>
      <div class="bone-sum" role="img" aria-label="${axial} axial and ${total - axial} appendicular bones"><i style="width:${(axial / total) * 100}%;background:var(--accent)"></i><i style="width:${((total - axial) / total) * 100}%;background:var(--star)"></i></div>
      <p class="small muted" style="margin:0">${axial} axial (skull, ossicles, hyoid, spine, ribs, sternum) and ${total - axial} appendicular (limbs and girdles). The 8 carpals and 7 tarsals per side are listed one by one.</p></div>
      <input class="search" style="margin-top:12px" type="search" id="bonesearch" placeholder="Search bones and fracture pearls" aria-label="Search bones"><div id="bonelist">${boneGroupsHTML("")}</div>`;
  }
  function boneGroupsHTML(q) {
    q = q.trim().toLowerCase();
    const out = BONES.map((g) => {
      const items = g.items.filter((it) => !q || it[0].toLowerCase().includes(q) || it[2].toLowerCase().includes(q));
      if (!items.length) return "";
      const cnt = g.items.reduce((a, it) => a + it[1], 0);
      return `<details class="bgroup" ${q ? "open" : ""}><summary>${esc(g.g)}<span class="c">${cnt} bone${cnt > 1 ? "s" : ""}</span></summary>${items.map((it) => `<div class="bone"><div class="bh"><b>${esc(it[0])}</b><span class="x">×${it[1]}</span></div><p>${esc(it[2])}</p>${it[3] && INFO[it[3]] ? `<button class="btn quiet sm" style="padding:0" data-act="show-fig" data-fig="${it[3]}">Show on the body</button>` : ""}</div>`).join("")}</details>`;
    }).join("");
    return out || `<p class="muted" style="margin-top:12px">No bone matches that search.</p>`;
  }

  /* ================= events ================= */
  function handle(act, t, v) {
    switch (act) {
      case "atab": UIA.tab = v; rerender(); return true;
      case "layer": if (Body.layers.has(v)) Body.layers.delete(v); else Body.layers.add(v); syncChips(); if (Body.mode === "3d") sync3DLayers(); if (Body.sel && !Body.quiz) { const so = ID2S[Body.sel.replace(/-(r|l)$/, "")]; if (so && !Body.layers.has(INFO[so.info || so.id].L)) { Body.sel = null; $("#infocard").innerHTML = infoCardHTML(); } } applyFigState(); return true;
      case "layers-all": { const keys = (Body.mode === "3d" ? LAYERS3() : LAYERS).map((l) => l.k), all = keys.every((k) => Body.layers.has(k)); Body.layers = all ? new Set(["bone", "organ"]) : new Set([...Body.layers, ...keys]); syncChips(); applyFigState(); if (Body.mode === "3d") sync3DLayers(); return true; }
      case "sex": Body.sex = v; $$("[data-act=sex]").forEach((b) => b.setAttribute("aria-pressed", b.dataset.v === v)); if (Body.sel) { const so = ID2S[Body.sel.replace(/-(r|l)$/, "")]; if (so && so.sex && so.sex !== v) { Body.sel = null; $("#infocard").innerHTML = infoCardHTML(); } } applyFigState(); return true;
      case "rotate-body": rotateBody(); return true;
      case "body-mode": if (Body.mode !== v) { if (v === "3d" && !Body.t3) Body.t3 = performance.now(); if (Body.quiz && Body.quiz.three && B3) B3.clear(); Body.quiz = null; Body.mode = v; rerender(true); } return true;
      case "zoom-in": if (Body.mode === "3d") { if (B3 && B3.isReady()) B3.zoom(1 / 1.5); } else animateVB(zoomBy(1 / 1.5)); return true;
      case "zoom-out": if (Body.mode === "3d") { if (B3 && B3.isReady()) B3.zoom(1.5); } else animateVB(zoomBy(1.5)); return true;
      case "zoom-fit": if (Body.mode === "3d") { if (B3 && B3.isReady()) B3.fit(); } else animateVB({ x: 0, y: 0, w: 400, h: 920 }); return true;
      case "bpick": Body.q = ""; $("#bsearch").value = ""; $("#bresults").innerHTML = ""; showOnBody(t.dataset.key); return true;
      case "show-fig": showOnBody(t.dataset.fig); return true;
      case "id-quiz": startIdQuiz(); return true;
      case "id-quiz-stop": if (Body.quiz && Body.quiz.three && B3) { B3.clear(); Body.sel3 = null; } Body.quiz = null; Body.sel = null; applyFigState(); $("#infocard").innerHTML = infoCardHTML(); return true;
      case "id-pick": quizPick(t.dataset.key); return true;
      case "id-next": nextIdQuestion(); return true;
      case "rotate-brain": rotateBrain(); return true;
      case "brain-terr": Brain.terr = !Brain.terr; t.setAttribute("aria-pressed", Brain.terr); $("#brainwrap").innerHTML = brainFigure(); return true;
      case "brain-pick": selectBrain(v); return true;
      case "cn": selectCN(v); return true;
      case "cn-quiz": openCNQuiz(); return true;
      case "quiz-pick": cnQuizPick(+t.dataset.i); return true;
      case "quiz-next": Quiz.i++; Quiz.answered = false; renderCNQuiz(); return true;
      case "quiz-again": Quiz.qs = buildCNQuiz(); Quiz.i = 0; Quiz.score = 0; Quiz.answered = false; renderCNQuiz(); return true;
      case "rotate-heart": rotateHeart(); return true;
      case "heart-pick": selectHeart(v); return true;
      case "idx-filter": Idx.filter = v; rerender(true); return true;
      case "dict-go": appHooks.closeSheet(); openEntry(t.dataset.id); return true;
    }
    return false;
  }
  function input(t) {
    if (t.id === "bonesearch") { $("#bonelist").innerHTML = boneGroupsHTML(t.value); return true; }
    if (t.id === "idxsearch") { Idx.q = t.value; const list = Idx.q.trim() ? searchDict(Idx.q.trim()) : DICT; $("#idxlist").innerHTML = indexListHTML(Idx.filter === "all" ? list : list.filter((e) => Idx.filter === "derm" ? e.sub === "Dermatome" : Idx.filter === "cn" ? e.sub === "Cranial nerve" : Idx.filter === "body" ? (e.model === "body" && e.sub !== "Dermatome") : (e.model === Idx.filter && e.sub !== "Cranial nerve"))); return true; }
    return false;
  }
  function init(hooks) { appHooks = hooks; }
  return { view, mount, handle, input, showOnBody, openEntry, init, dict: DICT, body: Body };
})();
