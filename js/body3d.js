/* 3D body viewer (Phase 1: skeleton). Loaded on demand by src/anat.js via import("./js/body3d.js").
   One renderer for the page's lifetime: attach() moves its canvas into whichever container the Body tab renders.
   Renders on demand (no idle loop). Mesh names come from glTF extras: userData.n (Z-Anatomy name), userData.s (R/L/"").
   three.js is imported dynamically so the model download starts at once instead of after ~0.5 MB of library code. */
let THREE, GLTFLoader, OrbitControls, MeshoptDecoder;
const libs = () => Promise.all([import("three"), import("three/addons/loaders/GLTFLoader.js"), import("three/addons/controls/OrbitControls.js"), import("three/addons/libs/meshopt_decoder.module.js")])
  .then(([t, g, o, m]) => { THREE = t; GLTFLoader = g.GLTFLoader; OrbitControls = o.OrbitControls; MeshoptDecoder = m.MeshoptDecoder; });

const MODEL = "models/skeleton.glb";
const MAP = "data/mesh_map.json";
const reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
const PERF = new URLSearchParams(location.search).has("perf");   // ?perf shows size, load time and fps on the phone

const COL = { bone: "#E8DCC0", cart: "#BFD5DA", tooth: "#F6F2E8", hl: "#2C5BCB" };
const isTooth = (n) => /incisor|canine|premolar|molar/i.test(n);

let renderer, scene, camera, controls, root, ready = null, container = null, ro = null;
let meshes = [];                 // all bone meshes
const byKey = new Map();         // card key -> meshes
const keyOf = new Map();         // Z-Anatomy name -> card key
const mats = {};
let sel = null;                  // { key, name, side, group: Mesh[] }
let onPick = () => {};
let fly = null, needs = false, perfEl = null, perfAt = 0;
const frameGaps = [];
export const stats = { bytes: 0, transfer: 0, tTap: 0, tLoadStart: 0, tLoaded: 0, tFirstFrame: 0, meshes: 0, triangles: 0, error: null };

function request() { if (!needs) { needs = true; requestAnimationFrame(frame); } }
function frame(t) {
  needs = false;
  let moving = false;
  if (fly) moving = stepFly(t) || moving;
  moving = controls.update() || moving;
  renderer.render(scene, camera);
  if (!stats.tFirstFrame && root) stats.tFirstFrame = performance.now();
  if (PERF) perfTick(t);
  if (moving) request();
}
function perfTick(t) {
  // fps from gaps between back-to-back frames (i.e. while turning or zooming); idle gaps are ignored
  if (perfTick.last && t - perfTick.last < 250) { frameGaps.push(t - perfTick.last); if (frameGaps.length > 60) frameGaps.shift(); }
  perfTick.last = t;
  if (!perfEl || t - perfAt < 400) return;
  perfAt = t;
  const ready = stats.tFirstFrame ? ((stats.tFirstFrame - (stats.tTap || stats.tLoadStart)) / 1000).toFixed(1) + " s" : "…";
  const fps = frameGaps.length >= 20 ? Math.round(1000 / (frameGaps.reduce((s, g) => s + g, 0) / frameGaps.length)) + " fps while turning" : "turn it to measure fps";
  perfEl.textContent = `model ${((stats.transfer || stats.bytes) / 1048576).toFixed(1)} MB download · ready in ${ready} · ${fps} · ${Math.round(stats.triangles / 1000)}k triangles`;
}

function makeMaterials() {
  const lam = (c, extra) => new THREE.MeshLambertMaterial(Object.assign({ color: c }, extra));
  mats.bone = lam(COL.bone); mats.cart = lam(COL.cart); mats.tooth = lam(COL.tooth);
  mats.hl = lam(COL.bone, { emissive: COL.hl, emissiveIntensity: 0.55 });
  mats.dim = lam(COL.bone, { transparent: true, opacity: 0.22, depthWrite: false });
}
function baseMat(m) { return m.userData.n.startsWith("Costal cartilage") ? mats.cart : isTooth(m.userData.n) ? mats.tooth : mats.bone; }

function init() {
  renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  const cv = renderer.domElement;
  cv.setAttribute("tabindex", "0");
  cv.setAttribute("aria-label", "3D skeleton. Drag to turn, pinch to zoom, two fingers to move, tap a bone. Arrow keys move; Shift plus arrows turn.");
  cv.style.touchAction = "none";
  scene = new THREE.Scene();
  camera = new THREE.PerspectiveCamera(30, 1, 0.01, 50);
  camera.position.set(0, 0.9, 3.2);
  scene.add(camera);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x8a8070, 1.5));
  const head = new THREE.DirectionalLight(0xffffff, 1.6); head.position.set(0.4, 0.6, 1); camera.add(head);
  controls = new OrbitControls(camera, cv);
  controls.enableDamping = !reduceMotion; controls.dampingFactor = 0.12;
  controls.minDistance = 0.12; controls.maxDistance = 6; controls.zoomToCursor = true;
  controls.touches = { ONE: THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_PAN };
  controls.listenToKeyEvents(cv);
  controls.addEventListener("change", request);
  controls.addEventListener("start", () => { fly = null; });
  makeMaterials();
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

function pickAt(cx, cy) {
  if (!root) return null;
  const r = renderer.domElement.getBoundingClientRect();
  const ndc = new THREE.Vector2(((cx - r.left) / r.width) * 2 - 1, -((cy - r.top) / r.height) * 2 + 1);
  const ray = new THREE.Raycaster(); ray.setFromCamera(ndc, camera);
  const hits = ray.intersectObjects(meshes, false);   // nearest bone wins, dimmed or not
  return hits.length ? hits[0].object : null;
}

function groupFor(mesh) {
  const key = keyOf.get(mesh.userData.n);
  if (!key) return [mesh];
  const side = mesh.userData.s;
  return byKey.get(key).filter((m) => !side || !m.userData.s || m.userData.s === side);
}
function setSelection(mesh, frameIt) {
  for (const m of meshes) m.material = baseMat(m);
  if (!mesh) { sel = null; request(); return; }
  const group = groupFor(mesh);
  sel = { key: keyOf.get(mesh.userData.n) || null, name: mesh.userData.n, side: mesh.userData.s, group };
  const inGroup = new Set(group);
  for (const m of meshes) m.material = inGroup.has(m) ? mats.hl : mats.dim;
  if (frameIt) frameObjects(group);
  request();
}
function info() { return sel ? { key: sel.key, name: sel.name, side: sel.side } : null; }

function boxOf(objs) { const b = new THREE.Box3(); objs.forEach((o) => b.expandByObject(o)); return b; }
function frameObjects(objs, instant) {
  const box = boxOf(objs), sphere = box.getBoundingSphere(new THREE.Sphere());
  const fov = THREE.MathUtils.degToRad(camera.fov), aspect = camera.aspect || 1;
  const fit = sphere.radius / Math.sin(Math.min(fov, 2 * Math.atan(Math.tan(fov / 2) * aspect)) / 2);
  const dist = Math.min(Math.max(fit * 1.05, controls.minDistance * 1.5), controls.maxDistance);
  const dir = camera.position.clone().sub(controls.target).normalize();
  const to = { target: sphere.center.clone(), pos: sphere.center.clone().add(dir.multiplyScalar(dist)) };
  if (instant || reduceMotion) { controls.target.copy(to.target); camera.position.copy(to.pos); fly = null; request(); return; }
  fly = { t0: null, from: { target: controls.target.clone(), pos: camera.position.clone() }, to };
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
function resetView(instant) {
  // anterior view, fitted to the body's height and width (a bounding sphere wastes most of a portrait screen)
  const box = boxOf([root]), size = box.getSize(new THREE.Vector3()), center = box.getCenter(new THREE.Vector3());
  const vf = THREE.MathUtils.degToRad(camera.fov) / 2, hf = Math.atan(Math.tan(vf) * (camera.aspect || 1));
  const dist = 1.06 * Math.max(size.y / 2 / Math.tan(vf), size.x / 2 / Math.tan(hf)) + size.z / 2;
  const to = { target: center, pos: center.clone().add(new THREE.Vector3(0, 0, dist)) };
  if (instant || reduceMotion) { controls.target.copy(to.target); camera.position.copy(to.pos); fly = null; request(); return; }
  fly = { t0: null, from: { target: controls.target.clone(), pos: camera.position.clone() }, to }; request();
}

async function fetchBytes(url, onProgress) {
  const r = await fetch(url); if (!r.ok) throw new Error(url + " " + r.status);
  if (!r.body || !r.body.getReader) { const b = await r.arrayBuffer(); stats.bytes = b.byteLength; return b; }
  const reader = r.body.getReader(), parts = []; let n = 0;
  for (;;) { const { done, value } = await reader.read(); if (done) break; parts.push(value); n += value.length; stats.bytes = n; onProgress && onProgress(n); }
  const out = new Uint8Array(n); let o = 0; for (const p of parts) { out.set(p, o); o += p.length; }
  return out.buffer;
}
async function load(onProgress) {
  stats.tLoadStart = performance.now();
  const bytes = fetchBytes(MODEL, onProgress), mapP = fetch(MAP).then((r) => { if (!r.ok) throw new Error("map " + r.status); return r.json(); });
  bytes.catch(() => {}); mapP.catch(() => {});      // awaited below; avoid "unhandled" noise while the libraries load
  await libs();
  init();
  const [map, buf] = await Promise.all([mapP, bytes]);
  const gltf = await new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).parseAsync(buf, "");
  const res = performance.getEntriesByName(new URL(MODEL, location.href).href)[0];
  stats.transfer = res && res.encodedBodySize ? res.encodedBodySize : stats.bytes;
  for (const [key, names] of Object.entries(map.skeleton)) for (const n of names) keyOf.set(n, key);
  root = gltf.scene;
  root.traverse((o) => {
    if (!o.isMesh) return;
    Object.assign(o.userData, { n: o.userData.n || o.parent.userData.n || o.name, s: o.userData.s ?? o.parent.userData.s ?? "" });
    o.material = baseMat(o);
    o.geometry.computeBoundingBox(); o.geometry.computeBoundingSphere();
    meshes.push(o);
    stats.triangles += (o.geometry.index ? o.geometry.index.count : o.geometry.attributes.position.count) / 3;
    const key = keyOf.get(o.userData.n);
    if (key) { if (!byKey.has(key)) byKey.set(key, []); byKey.get(key).push(o); }
  });
  stats.meshes = meshes.length;
  scene.add(root);
  root.updateMatrixWorld(true);
  controls.target.copy(boxOf([root]).getCenter(new THREE.Vector3()));
  stats.tLoaded = performance.now();
}

function resize() {
  if (!container) return;
  const w = container.clientWidth, h = container.clientHeight;
  if (!w || !h) return;
  renderer.setSize(w, h, false);
  camera.aspect = w / h; camera.updateProjectionMatrix();
  request();
}

/* ---------- public API ---------- */
export function supported() {
  try { const c = document.createElement("canvas"); return !!(window.WebGL2RenderingContext && c.getContext("webgl2")); } catch (_) { return false; }
}
/** Put the viewer into `el` (an empty element sized by CSS). Resolves once the model is ready. */
let framed = false;
export function attach(el, opts = {}) {
  onPick = opts.onPick || (() => {});
  if (opts.t0 && !stats.tTap) stats.tTap = opts.t0;
  container = el;
  if (!ready) ready = load(opts.onProgress);
  return ready.then(() => {
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
    if (!framed) { framed = true; resetView(true); }
    request();
    return stats;
  });
}
export const isReady = () => !!root;
export const hasKey = (key) => byKey.has(key);
/** Select every mesh of a card (optionally one side) and frame it. */
export function selectKey(key, side, frameIt = true) {
  const list = byKey.get(key); if (!list) return false;
  const m = list.find((x) => !side || !x.userData.s || x.userData.s === side) || list[0];
  setSelection(m, frameIt); return true;
}
export function selectMesh(name, side, frameIt = true) {
  const m = meshes.find((x) => x.userData.n === name && (!side || x.userData.s === side)); if (!m) return false;
  setSelection(m, frameIt); return true;
}
export function clear() { setSelection(null); }
export const current = info;
export function zoom(f) {
  fly = null;
  const off = camera.position.clone().sub(controls.target);
  const len = Math.min(Math.max(off.length() * f, controls.minDistance), controls.maxDistance);
  const to = { target: controls.target.clone(), pos: controls.target.clone().add(off.setLength(len)) };
  if (reduceMotion) { camera.position.copy(to.pos); request(); return; }
  fly = { t0: null, from: { target: controls.target.clone(), pos: camera.position.clone() }, to }; request();
}
export function fit() { if (root) resetView(false); }

/* test hooks: how many canvas pixels are drawn on, screen position of a mesh's centre */
export function debugDrawnPixels() {
  renderer.render(scene, camera);
  const gl = renderer.getContext(), w = gl.drawingBufferWidth, h = gl.drawingBufferHeight, px = new Uint8Array(w * h * 4);
  gl.readPixels(0, 0, w, h, gl.RGBA, gl.UNSIGNED_BYTE, px);
  let n = 0; for (let i = 3; i < px.length; i += 4) if (px[i] > 0) n++;
  return { drawn: n, total: w * h };
}
export function debugProject(name, side) {
  const m = meshes.find((x) => x.userData.n === name && (!side || x.userData.s === side)); if (!m) return null;
  const c = boxOf([m]).getCenter(new THREE.Vector3()), p = c.clone().project(camera), r = renderer.domElement.getBoundingClientRect();
  return { x: r.left + ((p.x + 1) / 2) * r.width, y: r.top + ((1 - p.y) / 2) * r.height, world: c.toArray() };
}
