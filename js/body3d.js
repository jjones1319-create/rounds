/* 3D anatomy viewers for the Body, Brain and Heart tabs. Loaded on demand by src/anat.js via import("./js/body3d.js?v=…").
   viewer("body" | "brain" | "heart") returns that scene's viewer; each has its own renderer, camera, layers and selection,
   and keeps them while the app re-renders (attach() moves its canvas into whichever container the tab draws).
   data/mesh_map.json lists, per scene, each layer's .glb (loaded the first time the layer is switched on) and which meshes
   belong to which card. Mesh names come from glTF extras: userData.n (Z-Anatomy/BodyParts3D name), userData.s (R/L/"").
   Renders on demand (no idle loop). three.js is imported dynamically so model downloads start at once. */
let THREE, GLTFLoader, OrbitControls, MeshoptDecoder;
let libsP = null;
const libs = () => libsP || (libsP = Promise.all([import("three"), import("three/addons/loaders/GLTFLoader.js"), import("three/addons/controls/OrbitControls.js"), import("three/addons/libs/meshopt_decoder.module.js")])
  .then(([t, g, o, m]) => { THREE = t; GLTFLoader = g.GLTFLoader; OrbitControls = o.OrbitControls; MeshoptDecoder = m.MeshoptDecoder; })
  .catch((e) => { libsP = null; throw e; }));

/** Bumped when the page/viewer contract changes; src/anat.js refuses a viewer with a different number (stale cache). */
export const API = 3;
const MAP = "data/mesh_map.json";
let V = {};                                                         // content hashes from build.py (ASSET_V)
const versioned = (file, key = file) => (V[key] ? `${file}?v=${V[key]}` : file);
let mapP = null;
const loadMap = () => mapP || (mapP = fetch(versioned(MAP, "map")).then((r) => { if (!r.ok) throw new Error("map " + r.status); return r.json(); }).catch((e) => { mapP = null; throw e; }));
const STALL_MS = 30000;                                             // give up on a download that stops for this long
const reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
const PERF = new URLSearchParams(location.search).has("perf");   // ?perf shows size, load time, fps and draw calls
const MAX_DPR = Math.min(window.devicePixelRatio || 1, 3);         // sharp on high-density phones; lowered if frames drop
const MIN_DPR = Math.min(MAX_DPR, 1.5);
const HL = "#2C5BCB";

/* ---------- colours. Layer colours come from the app; some layers tint each structure by name. ---------- */
const tint = (rules, n, fallback) => { const t = rules.find(([rx]) => rx.test(n)); return t ? t[1] : fallback; };
const ORGAN_TINTS = [
  [/^(Liver|Spleen)$/, "#8E3B32"], [/lung$/, "#E6A3A0"], [/(atrium|ventricle)$/, "#B5413A"], [/^Kidney$/, "#9A4A3C"],
  [/^Suprarenal/, "#D9A441"], [/^(Gallbladder|Bile duct)$/, "#5E8C4A"], [/^(Pancreas|.*(parotid|sublingual|submandibular) gland\)?)$/i, "#E7C27A"],
  [/(thyroid gland|parathyroid gland)$/i, "#B9534A"], [/^(Urinary bladder|Ureter|Urethra)$/, "#E8C37F"],
  [/^(Trachea|.*bronchus|.*pharynx|Epiglottis)$/, "#D9B8B0"], [/^Diaphragm$/, "#B8463F"], [/^Sclera$/, "#F2F0EA"], [/^Cornea$/, "#CFE3EA"],
  [/^(Tongue|Soft palate|Uvula of palate)$/, "#D4776C"], [/hypophysis$|^Pineal/, "#C9A0B0"],
  [/^(Testis|Epididymis|Prostate|Seminal gland|Ductus deferens|Ejaculatory duct|Glans penis|Corpus .* of penis)$/, "#D99A8A"],
  [/colon$|^(Oesophagus|Stomach|Duodenum|Jejunum|Vermiform appendix)$/, "#E3A58E"],
];
const BRAIN_TINTS = [
  [/sulcus|sulci|^Lat_Fis/, "#D2A396"],                                            // sulci a shade darker than gyri
  [/[Vv]entricle|^Aqueduct/, "#8FB8D8"],                                           // CSF spaces
  [/^(Corpus callosum|Fornix|.*commissure|Optic (chiasm|tract)|Septum pellucidum)$/, "#F1ECE2"],   // white matter
  [/^(Thalamus|Hypothalamus|Caudate nucleus|Putamen|Globus pallidus|Amygdaloid body|Hippocampus|.*colliculus|.*geniculate body|Mamillary body)$/, "#C9A79A"],
  [/hypophysis$|^Pineal/, "#C9A0B0"],
  [/^(Midbrain|Pons|Medulla oblongata|Olive|Pyramid of medulla oblongata|Base of peduncle|Superior cerebellar peduncle)$/, "#E2C6B6"],
];
const HEART_TINTS = [
  [/ventricle$/, "#A33B32"], [/atrium$/, "#B55A4E"], [/papillary/, "#A9473D"], [/leaflet|cusp/, "#EAD7C3"],
  [/[Pp]ulmonary (trunk|artery)|^Bifurcation of pulmonary trunk|vena cava|[Cc]ardiac vein|[Cc]oronary sinus|vein of left ventricle/, "#3B66C4"],
  [/pulmonary vein|aort|carotid|subclavian|[Bb]rachiocephalic trunk|coronary artery|interventricular artery|[Cc]ircumflex|branch of right coronary|[Ss]eptal branches/, "#D2352E"],
];
const SCENES = {
  // view: the direction the camera looks from at the start (three.js axes: +X subject's left, +Y up, +Z front)
  body: { view: [0, 0, 1], color: (layer, n, c) => layer === "bone" ? (n.startsWith("Costal cartilage") ? "#BFD5DA" : /incisor|canine|premolar|molar/i.test(n) ? "#F6F2E8" : "#E8DCC0") : layer === "organ" ? tint(ORGAN_TINTS, n, c) : c },
  brain: { view: [1, 0.08, 0.1], frame: ["cortex", "deep"], ghost: ["skull"], color: (layer, n, c) => layer === "cortex" ? tint(BRAIN_TINTS, n, "#E7C1B5") : layer === "deep" ? tint(BRAIN_TINTS, n, "#D7B1A0") : layer === "skull" ? "#E8DCC0" : c },
  heart: { view: [0, 0, 1], color: (layer, n, c) => tint(HEART_TINTS, n, c) },
};

async function fetchBytes(url, report) {
  const ac = new AbortController(); let timer;
  const arm = () => { clearTimeout(timer); timer = setTimeout(() => ac.abort(), STALL_MS); };
  try {
    arm();
    const r = await fetch(url, { signal: ac.signal }); if (!r.ok) throw new Error(url + " " + r.status);
    if (!r.body || !r.body.getReader) { const b = await r.arrayBuffer(); report(b.byteLength); return b; }
    const reader = r.body.getReader(), parts = []; let n = 0;
    for (;;) { const { done, value } = await reader.read(); arm(); if (done) break; parts.push(value); n += value.length; report(n); }
    const out = new Uint8Array(n); let o = 0; for (const p of parts) { out.set(p, o); o += p.length; }
    return out.buffer;
  } finally { clearTimeout(timer); }
}

export function supported() {
  try { const c = document.createElement("canvas"); return !!(window.WebGL2RenderingContext && c.getContext("webgl2")); } catch (_) { return false; }
}
const viewers = {};
/** The viewer for one scene ("body", "brain" or "heart"), created on first use. */
export function viewer(name) { return viewers[name] || (viewers[name] = makeViewer(name)); }

function makeViewer(sceneName) {
  const SC = SCENES[sceneName];
  let renderer, scene, camera, controls, ready = null, container = null, ro = null, layerColors = {};
  let cfg = null;                  // this scene in data/mesh_map.json
  const L = {};                    // layer key -> { file, root, meshes, loading, visible }
  const byKey = new Map();         // card key -> meshes (filled as layers load)
  const keyOf = new Map();         // "name|S" or "name" -> card key
  const layerOfKey = new Map();    // card key -> layer key (known before the layer loads)
  const mats = new Map(), dims = new Map();   // colour -> material, base material -> dimmed copy
  let hlMat = null, sel = null, onPick = () => {}, onProgress = () => {};
  let fly = null, needs = false, perfEl = null, perfAt = 0, dpr = MAX_DPR, framed = false, lastT = 0;
  let side = null;                 // show one hemisphere/side only ("L" or "R"), or everything
  let cut = null, cutPlane = null; // front-to-back cut-away (0..1 of the scene's depth), or none
  const gaps = [], perfGaps = [];
  const stats = { bytes: 0, transfer: 0, tTap: 0, tLoadStart: 0, tLoaded: 0, tFirstFrame: 0, meshes: 0, triangles: 0, dpr: MAX_DPR, layers: {}, error: null };

  /* ---- render loop (on demand) ---- */
  function request() { if (renderer && !needs) { needs = true; requestAnimationFrame(frame); } }
  function frame(t) {
    needs = false;
    let moving = false;
    if (fly) moving = stepFly(t) || moving;
    moving = controls.update() || moving;
    renderer.render(scene, camera);
    if (!stats.tFirstFrame && anyMeshes()) stats.tFirstFrame = performance.now();
    pace(t, moving);
    if (PERF) perfTick(t);
    if (moving) request();
  }
  /* Dynamic resolution: if turning runs below ~45 fps, step the pixel ratio down (never back up this session). */
  function pace(t, moving) {
    if (moving && lastT && t - lastT < 250) {
      gaps.push(t - lastT); perfGaps.push(t - lastT); if (perfGaps.length > 60) perfGaps.shift();
      if (gaps.length >= 30) {
        const avg = gaps.reduce((s, g) => s + g, 0) / gaps.length; gaps.length = 0;
        if (avg > 22 && dpr > MIN_DPR) { dpr = Math.max(MIN_DPR, dpr - 0.5); stats.dpr = dpr; renderer.setPixelRatio(dpr); resize(); }
      }
    }
    lastT = t;
  }
  function perfTick(t) {
    if (!perfEl || t - perfAt < 400) return;
    perfAt = t;
    const readyIn = stats.tFirstFrame ? ((stats.tFirstFrame - (stats.tTap || stats.tLoadStart)) / 1000).toFixed(1) + " s" : "…";
    const fps = perfGaps.length >= 20 ? Math.round(1000 / (perfGaps.reduce((s, g) => s + g, 0) / perfGaps.length)) + " fps while turning" : "turn it to measure fps";
    const mb = Object.values(stats.layers).reduce((s, l) => s + (l.transfer || 0), 0) / 1048576;
    const info = renderer.info.render;
    perfEl.textContent = `models ${mb.toFixed(1)} MB download · ready in ${readyIn} · ${fps} · ${info.calls} draws · ${Math.round(info.triangles / 1000)}k triangles · ${dpr}x`;
  }
  const anyMeshes = () => Object.values(L).some((l) => l.visible && l.meshes.length);

  /* ---- materials (per viewer, so the heart's cut-away never clips another tab) ---- */
  const clipping = () => (cutPlane && cut != null ? [cutPlane] : []);
  const sideMode = () => (cut != null ? THREE.DoubleSide : THREE.FrontSide);   // show the inside of cut walls
  function mat(color, ghost) {                     // ghost: see-through context layer (the skull around the brain)
    const k = color + (ghost ? "|ghost" : "");
    if (!mats.has(k)) mats.set(k, new THREE.MeshLambertMaterial(Object.assign({ color, clippingPlanes: clipping(), side: sideMode() }, ghost ? { transparent: true, opacity: 0.28, depthWrite: false } : {})));
    return mats.get(k);
  }
  function dimOf(m) {
    if (!dims.has(m)) dims.set(m, new THREE.MeshLambertMaterial({ color: m.color, transparent: true, opacity: 0.18, depthWrite: false, clippingPlanes: clipping(), side: sideMode() }));
    return dims.get(m);
  }
  function refreshMaterials() {
    for (const m of [...mats.values(), ...dims.values(), hlMat]) { m.clippingPlanes = clipping(); m.side = sideMode(); m.needsUpdate = true; }
  }

  /* ---- setup ---- */
  function init() {
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(dpr);
    renderer.localClippingEnabled = true;
    const cv = renderer.domElement;
    cv.setAttribute("tabindex", "0");
    cv.setAttribute("aria-label", `3D ${sceneName}. Drag to turn, pinch to zoom, two fingers to move, tap a structure. Arrow keys move; Shift plus arrows turn.`);
    cv.style.touchAction = "none";
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(30, 1, 0.005, 50);
    camera.position.set(0, 0.9, 3.2);
    scene.add(camera);
    scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8070, 1.5));
    const head = new THREE.DirectionalLight(0xffffff, 1.6); head.position.set(0.4, 0.6, 1); camera.add(head);
    controls = new OrbitControls(camera, cv);
    controls.enableDamping = !reduceMotion; controls.dampingFactor = 0.12;
    controls.minDistance = 0.03; controls.maxDistance = 6; controls.zoomToCursor = true;
    controls.touches = { ONE: THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_PAN };
    controls.listenToKeyEvents(cv);
    controls.addEventListener("change", request);
    controls.addEventListener("start", () => { fly = null; });
    hlMat = new THREE.MeshLambertMaterial({ color: "#DCE6FF", emissive: HL, emissiveIntensity: 0.5 });
    cutPlane = new THREE.Plane(new THREE.Vector3(0, 0, -1), 0);
    // tap = short press without much movement; anything else is a drag for the controls
    let down = null;
    cv.addEventListener("pointerdown", (e) => { down = e.isPrimary ? { x: e.clientX, y: e.clientY, t: performance.now(), multi: false } : (down && (down.multi = true), down); });
    cv.addEventListener("pointerup", (e) => {
      if (!down || !e.isPrimary) return;
      const d = down; down = null;
      if (d.multi || Math.hypot(e.clientX - d.x, e.clientY - d.y) > 8 || performance.now() - d.t > 600) return;
      const hit = pickAt(e.clientX, e.clientY);
      if (hit) { setSelection(hit, false); onPick(info()); } else if (sel) { setSelection(null); onPick(null); }
    });
    cv.addEventListener("webglcontextlost", (e) => { e.preventDefault(); stats.error = "context-lost"; });
  }
  const retryable = (layer, p) => { const q = p.catch((e) => { L[layer].loading = null; throw e; }); q.catch(() => {}); return q; };
  /* Libraries, renderer and this scene's map, once; the first layers' downloads start as soon as the map arrives. */
  async function start(first) {
    stats.tLoadStart = stats.tLoadStart || performance.now();
    const early = {};
    const m = loadMap().then((map) => { const s = map.scenes[sceneName]; for (const k of first) if (s.layers[k] && !L[k]) early[k] = fetchLayer(k, s.layers[k].file); return map; });
    m.catch(() => {});
    await libs();
    if (!renderer) init();
    cfg = (await m).scenes[sceneName];
    for (const [layer, lc] of Object.entries(cfg.layers)) {
      if (L[layer]) continue;
      L[layer] = { file: lc.file, root: null, meshes: [], loading: null, visible: false };
      if (early[layer]) L[layer].loading = retryable(layer, parseLayer(layer, early[layer]));
      for (const [key, names] of Object.entries(lc.cards)) {
        layerOfKey.set(key, layer);
        for (const n of names) { const mm = n.match(/^(.*)\.(l|r)$/); keyOf.set(mm ? `${mm[1]}|${mm[2].toUpperCase()}` : n, key); }
      }
    }
  }
  function fetchLayer(layer, file) {
    stats.layers[layer] = { bytes: 0, transfer: 0, triangles: 0, meshes: 0 };
    const p = fetchBytes(versioned(file), (n) => { stats.layers[layer].bytes = n; stats.bytes = Object.values(stats.layers).reduce((s, l) => s + l.bytes, 0); onProgress(layer, n); });
    p.catch(() => {});
    return p;
  }
  async function parseLayer(layer, bytesP) {
    const buf = await bytesP;
    const gltf = await new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).parseAsync(buf, "");
    const st = stats.layers[layer], res = performance.getEntriesByName(new URL(versioned(L[layer].file), location.href).href)[0];
    st.transfer = res && res.encodedBodySize ? res.encodedBodySize : st.bytes;
    const root = gltf.scene;
    root.traverse((o) => {
      if (!o.isMesh) return;
      Object.assign(o.userData, { n: o.userData.n || o.parent.userData.n || o.name, s: o.userData.s ?? o.parent.userData.s ?? "", layer });
      o.material = o.userData.base = mat(SC.color(layer, o.userData.n, layerColors[layer] || "#cccccc"), (SC.ghost || []).includes(layer));
      o.visible = !side || !o.userData.s || o.userData.s === side;
      o.geometry.computeBoundingBox(); o.geometry.computeBoundingSphere();
      L[layer].meshes.push(o);
      const tris = (o.geometry.index ? o.geometry.index.count : o.geometry.attributes.position.count) / 3;
      st.triangles += tris; stats.triangles += tris; st.meshes++; stats.meshes++;
      const key = keyFor(o);
      if (key) { if (!byKey.has(key)) byKey.set(key, []); byKey.get(key).push(o); }
    });
    root.visible = L[layer].visible;
    scene.add(root); root.updateMatrixWorld(true);
    L[layer].root = root;
    if (sel) setSelection(sel.group[0], false);   // dim the newcomers too
    request();
    return root;
  }
  const keyFor = (m) => keyOf.get(`${m.userData.n}|${m.userData.s}`) || keyOf.get(m.userData.n) || null;

  /* ---- picking and selection ---- */
  function visibleMeshes() { return Object.values(L).filter((l) => l.visible).flatMap((l) => l.meshes).filter((m) => m.visible); }
  function pickAt(cx, cy) {
    const r = renderer.domElement.getBoundingClientRect();
    const ndc = new THREE.Vector2(((cx - r.left) / r.width) * 2 - 1, -((cy - r.top) / r.height) * 2 + 1);
    const ray = new THREE.Raycaster(); ray.setFromCamera(ndc, camera);
    const hits = ray.intersectObjects(visibleMeshes(), false);   // nearest visible structure wins, dimmed or not
    const hit = hits.find((h) => cut == null || cutPlane.distanceToPoint(h.point) >= 0);   // ignore what the cut removed
    return hit ? hit.object : null;
  }
  function groupFor(mesh) {
    const key = keyFor(mesh);
    if (!key) return [mesh];
    const s = mesh.userData.s;
    return byKey.get(key).filter((m) => !s || !m.userData.s || m.userData.s === s);
  }
  function setSelection(mesh, frameIt) {
    const all = Object.values(L).flatMap((l) => l.meshes);
    if (!mesh) { for (const m of all) m.material = m.userData.base; sel = null; request(); return; }
    const group = groupFor(mesh), inGroup = new Set(group);
    sel = { key: keyFor(mesh), name: mesh.userData.n, side: mesh.userData.s, layer: mesh.userData.layer, group };
    for (const m of all) m.material = inGroup.has(m) ? hlMat : dimOf(m.userData.base);
    if (frameIt) frameObjects(group.filter((m) => m.visible).length ? group.filter((m) => m.visible) : group);
    request();
  }
  function info() { return sel ? { key: sel.key, name: sel.name, side: sel.side, layer: sel.layer } : null; }

  /* ---- camera ---- */
  function boxOf(objs) { const b = new THREE.Box3(); objs.forEach((o) => b.expandByObject(o)); return b; }
  function frameObjects(objs, instant) {
    const box = boxOf(objs), sphere = box.getBoundingSphere(new THREE.Sphere());
    const fov = THREE.MathUtils.degToRad(camera.fov), aspect = camera.aspect || 1;
    const fit = sphere.radius / Math.sin(Math.min(fov, 2 * Math.atan(Math.tan(fov / 2) * aspect)) / 2);
    const dist = Math.min(Math.max(fit * 1.05, controls.minDistance * 1.5), controls.maxDistance);
    const dir = camera.position.clone().sub(controls.target).normalize();
    flyTo(sphere.center.clone(), sphere.center.clone().add(dir.multiplyScalar(dist)), instant);
  }
  function flyTo(target, pos, instant) {
    if (instant || reduceMotion) { controls.target.copy(target); camera.position.copy(pos); fly = null; request(); return; }
    fly = { t0: null, from: { target: controls.target.clone(), pos: camera.position.clone() }, to: { target, pos } };
    request();
  }
  function stepFly(t) {
    if (fly.t0 == null) fly.t0 = t;
    const k = Math.min(1, (t - fly.t0) / 420), e = 1 - Math.pow(1 - k, 3);
    controls.target.lerpVectors(fly.from.target, fly.to.target, e);
    camera.position.lerpVectors(fly.from.pos, fly.to.pos, e);
    if (k >= 1) { fly = null; return false; }
    return true;
  }
  /* Look at the whole scene from `dir`, fitted to what is visible from there (a bounding sphere wastes a portrait screen). */
  function viewFrom(dir, instant) {
    let roots = Object.values(L).filter((l) => l.visible && l.root).map((l) => l.root);
    const framed = roots.filter((r) => (SC.frame || []).some((k) => L[k] && L[k].root === r));
    if (framed.length) roots = framed;                 // e.g. the brain itself, not the nerve roots below it
    if (!roots.length) return;
    const box = boxOf(roots), center = box.getCenter(new THREE.Vector3());
    const d = new THREE.Vector3(...dir).normalize();
    if (Math.abs(d.y) > 0.95) d.set(d.x, Math.sign(d.y) * 0.95, d.z || 0.31).normalize();   // controls keep +Y up; avoid looking straight down it
    const up = new THREE.Vector3(0, 1, 0);
    const right = new THREE.Vector3().crossVectors(up, d).normalize(), upv = new THREE.Vector3().crossVectors(d, right);
    let w = 0, h = 0, depth = 0;
    for (const x of [box.min.x, box.max.x]) for (const y of [box.min.y, box.max.y]) for (const z of [box.min.z, box.max.z]) {
      const p = new THREE.Vector3(x, y, z).sub(center);
      w = Math.max(w, Math.abs(p.dot(right))); h = Math.max(h, Math.abs(p.dot(upv))); depth = Math.max(depth, Math.abs(p.dot(d)));
    }
    const vf = THREE.MathUtils.degToRad(camera.fov) / 2, hf = Math.atan(Math.tan(vf) * (camera.aspect || 1));
    const dist = 1.06 * Math.max(h / Math.tan(vf), w / Math.tan(hf)) + depth;
    flyTo(center, center.clone().add(d.multiplyScalar(dist)), instant);
  }
  function resize() {
    if (!container) return;
    const w = container.clientWidth, h = container.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.updateProjectionMatrix();
    request();
  }

  /* ---- public API ---- */
  /** Put the viewer into `el` (an empty element sized by CSS) and show `opts.layers`. Resolves once those are drawn. */
  function attach(el, opts = {}) {
    onPick = opts.onPick || (() => {});
    onProgress = opts.onProgress || (() => {});
    if (opts.colors) layerColors = opts.colors;
    if (opts.versions) V = opts.versions;
    if (opts.t0 && !stats.tTap) stats.tTap = opts.t0;
    container = el;
    const want = opts.layers || [];
    if (!ready) ready = start(want).catch((e) => { ready = null; throw e; });   // a failed start can be retried
    return ready.then(() => setLayers(want)).then(() => {
      if (container !== el) return stats;          // a later attach() (re-render) owns the canvas now
      el.appendChild(renderer.domElement);
      Object.assign(renderer.domElement.style, { width: "100%", height: "100%", display: "block" });
      if (PERF) {
        perfEl = perfEl || Object.assign(document.createElement("div"), { style: "position:absolute;left:8px;right:60px;top:40px;font:11px/1.3 system-ui;padding:4px 6px;border-radius:6px;background:rgba(0,0,0,.6);color:#fff;pointer-events:none" });
        el.appendChild(perfEl);
      }
      if (ro) ro.disconnect();
      ro = new ResizeObserver(resize); ro.observe(el);
      resize();
      if (!framed && anyMeshes()) { framed = true; viewFrom(SC.view, true); stats.tLoaded = performance.now(); }
      request();
      return stats;
    });
  }
  /** Show exactly these layers, loading any not loaded yet. Resolves when they are all drawn. */
  function setLayers(keys) {
    const want = new Set(keys), jobs = [];
    for (const [layer, l] of Object.entries(L)) {
      l.visible = want.has(layer);
      if (l.root) l.root.visible = l.visible;
      if (l.visible && !l.loading) l.loading = retryable(layer, parseLayer(layer, fetchLayer(layer, l.file)));
      if (l.visible) jobs.push(l.loading);
    }
    if (sel && !L[sel.layer].visible) { setSelection(null); onPick(null); }
    request();
    return Promise.all(jobs).then(() => {
      if (!framed && anyMeshes() && renderer.domElement.isConnected) { framed = true; viewFrom(SC.view, true); }
      request();
    });
  }
  /** Select every mesh of a card (one side for paired structures) and frame it. Loads and shows its layer if needed. */
  async function selectKey(key, s, frameIt = true) {
    const layer = layerOfKey.get(key); if (!layer) return false;
    if (!L[layer].visible) await setLayers([...Object.keys(L).filter((k) => L[k].visible), layer]); else await L[layer].loading;
    const list = byKey.get(key); if (!list) return false;
    const m = list.find((x) => x.visible && (!s || !x.userData.s || x.userData.s === s)) || list.find((x) => !s || !x.userData.s || x.userData.s === s) || list[0];
    setSelection(m, frameIt); return true;
  }
  /** Cards that can be quizzed now: they have meshes in a loaded, visible layer. One entry per card and side. */
  function quizPool() {
    const out = [];
    for (const [key, ms] of byKey) {
      if (!L[layerOfKey.get(key)].visible) continue;
      for (const s of [...new Set(ms.filter((m) => m.visible).map((m) => m.userData.s))]) out.push({ key, side: s });
    }
    return out;
  }
  function zoom(f) {
    fly = null;
    const off = camera.position.clone().sub(controls.target);
    const len = Math.min(Math.max(off.length() * f, controls.minDistance), controls.maxDistance);
    flyTo(controls.target.clone(), controls.target.clone().add(off.setLength(len)));
  }
  /** Show one side only (brain hemispheres), or both with null. Midline structures always stay. */
  function setSide(s) {
    side = s || null;
    for (const l of Object.values(L)) for (const m of l.meshes) m.visible = !side || !m.userData.s || m.userData.s === side;
    if (sel && !sel.group.some((m) => m.visible)) { setSelection(null); onPick(null); }
    request();
  }
  /** Cut away the front of the scene: f = 0 (nothing removed) .. 1 (back wall only), or null to close it up. */
  function setCut(f) {
    if (!renderer) return;
    const was = cut != null;
    cut = f == null ? null : Math.min(Math.max(f, 0), 0.98);
    if (cut != null) {
      const roots = Object.values(L).filter((l) => l.root).map((l) => l.root);
      const box = boxOf(roots);
      cutPlane.constant = box.max.z - cut * (box.max.z - box.min.z);   // keep z <= constant (front is +z)
    }
    if (was !== (cut != null)) refreshMaterials(); else for (const m of [...mats.values(), ...dims.values(), hlMat]) m.clippingPlanes = clipping();
    request();
  }
  /** Debug/test hooks: canvas pixels drawn on, and the screen position of a mesh's centre. */
  function debugDrawnPixels() {
    renderer.render(scene, camera);
    const gl = renderer.getContext(), w = gl.drawingBufferWidth, h = gl.drawingBufferHeight, px = new Uint8Array(w * h * 4);
    gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, px);
    let n = 0; for (let i = 3; i < px.length; i += 4) if (px[i] > 0) n++;
    return { drawn: n, total: w * h };
  }
  function debugProject(name, s) {
    const m = visibleMeshes().find((x) => x.userData.n === name && (!s || x.userData.s === s)); if (!m) return null;
    const c = boxOf([m]).getCenter(new THREE.Vector3()), p = c.clone().project(camera), r = renderer.domElement.getBoundingClientRect();
    return { x: r.left + ((p.x + 1) / 2) * r.width, y: r.top + ((1 - p.y) / 2) * r.height, world: c.toArray() };
  }
  return {
    attach, setLayers, selectKey, quizPool, zoom, setSide, setCut, debugDrawnPixels, debugProject, stats,
    isReady: () => !!cfg && anyMeshes(),
    layers: () => (cfg ? Object.keys(cfg.layers) : []),
    layerOf: (key) => layerOfKey.get(key) || null,          // known before that layer is loaded; null = no 3D match
    hasKey: (key) => layerOfKey.has(key),
    loaded: (layer) => !!(L[layer] && L[layer].root),
    clear: () => setSelection(null),
    current: info,
    fit: () => viewFrom(SC.view, false),
    look: (dir) => viewFrom(dir, false),
    side: () => side,
    cut: () => cut,
  };
}
