(function () {
  "use strict";
  /* Question banks are fetched at boot (data/boards.json, data/mcat.json). QB, QMAP, QNUM and SYSTEMS always describe the
     selected exam's bank, so the boards code below is unchanged; the MCAT bank stays empty until PLAN_MCAT Phase M2. */
  const EXAMS = { boards: { key: "rounds.progress.v1", name: "Boards" }, mcat: { key: "rounds.mcat.v1", name: "MCAT" } };
  const EXAM_KEY = "rounds.exam";                       // which exam is selected (a convenience, not progress)
  const Bank = { boards: [], mcat: { sections: [], items: [], passages: [], guides: {} } };
  const MAPS = { boards: {}, mcat: {} };                 // id -> question, per exam
  let EXAM = "boards", QB = [], QMAP = {}, QNUM = {}, SYSTEMS = [], ready = false;
  function activate(exam) {
    EXAM = exam; QB = exam === "boards" ? Bank.boards : Bank.mcat.items; QMAP = MAPS[exam];
    QNUM = Object.fromEntries(QB.map((q, i) => [q.id, i + 1])); SYSTEMS = [...new Set(QB.map((q) => q.sys))];
    P.systems = new Set(SYSTEMS);
    if (exam === "mcat") { P.sections = new Set(Bank.mcat.sections.map((s) => s.k)); P.skills = new Set(["1", "2", "3", "4"]); P.diffs = new Set([2, 3, 4, 5]); P.perQ = 96; }
    else { P.diffs = new Set([3, 4, 5]); P.perQ = 90; }
  }
  const MCAT_PERQ = { chem_phys: 96, bio_biochem: 96, psych_soc: 96, cars: 102 };   // seconds: 95 min / 59 questions, 90 min / 53
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const stars = (n) => `<span class="stars" aria-label="Difficulty ${n} of 5">${"★".repeat(n)}<span class="off">${"★".repeat(5 - n)}</span></span>`;
  const fmt = (s) => { s = Math.max(0, Math.round(s)); const m = Math.floor(s / 60), r = s % 60; return m + ":" + String(r).padStart(2, "0"); };
  const uid = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
  const shuffle = (a) => { a = a.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const reduceMotion = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------------- icons ---------------- */
  const I = (p, extra = "") => `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"${extra}>${p}</svg>`;
  const ICON = {
    home: I('<path d="M3 11.5 12 4l9 7.5"/><path d="M5.5 10v9.5h13V10"/>'),
    practice: I('<rect x="4" y="3.5" width="16" height="17" rx="2.5"/><path d="M8 8.5h8M8 12.5h8M8 16.5h5"/>'),
    body: I('<circle cx="12" cy="4.5" r="2"/><path d="M12 7v7M7 9.5l5 1.5 5-1.5M9 21l3-7 3 7"/>'),
    chart: I('<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>'),
    gear: I('<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>'),
    x: I('<path d="M6 6l12 12M18 6 6 18"/>'),
    flag: I('<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>'),
    labs: I('<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 1.8 3h10.4A2 2 0 0 0 19 18l-5-9V3"/><path d="M7.5 15h9"/>'),
    more: I('<circle cx="5" cy="12" r="1.4"/><circle cx="12" cy="12" r="1.4"/><circle cx="19" cy="12" r="1.4"/>'),
    left: I('<path d="M15 5l-7 7 7 7"/>'),
    right: I('<path d="M9 5l7 7-7 7"/>'),
    strike: I('<path d="M4 12h16"/><path d="M8 7.5c1-1.6 2.6-2.5 4.4-2.5 2.2 0 3.6 1 4.1 2.4M16 16.5c-1 1.6-2.6 2.5-4.4 2.5-2.3 0-3.8-1.1-4.3-2.6"/>'),
    plus: I('<path d="M12 5v14M5 12h14"/>'),
    minus: I('<path d="M5 12h14"/>'),
    fit: I('<path d="M4 9V4h5M20 9V4h-5M4 15v5h5M20 15v5h-5"/>'),
    search: I('<circle cx="11" cy="11" r="6.5"/><path d="m20 20-4.2-4.2"/>'),
    table: I('<rect x="3.5" y="5" width="17" height="14" rx="2"/><path d="M3.5 10h17M3.5 15h17M9 5v14M15 5v14"/>'),
    check: I('<path d="m5 12.5 4.5 4.5L19 7"/>'),
    logo: '<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="16" cy="16" r="12.5"/><path d="M5 17h6l2.5-5 4 9 2.5-4H27"/></svg>',
  };

  /* ---------------- storage ---------------- */
  const fresh = () => ({ v: 1, answers: {}, flags: {}, notes: {}, sessions: [], settings: { theme: "system", font: 1, ts: 0 }, updatedAt: 0 });
  function normalize(d, qmap) {
    const f = fresh();
    if (!d || typeof d !== "object") return f;
    for (const k in f) if (d[k] == null) d[k] = f[k];
    d.settings = Object.assign(fresh().settings, d.settings || {});
    if (!Array.isArray(d.sessions)) d.sessions = [];
    d.sessions = d.sessions.filter((s) => s && Array.isArray(s.qids) && s.qids.every((id) => qmap[id]));
    return d;
  }
  /* One progress record per exam, each under its own localStorage key. Store.d is the selected exam's record. The boards
     key (rounds.progress.v1) keeps its original shape, and the app settings (theme, text size) live in it. */
  const Store = {
    all: { boards: null, mcat: null },
    get d() { return this.all[EXAM]; },
    set d(v) { this.all[EXAM] = v; },
    settings() { return this.all.boards.settings; },
    read(exam) { let d = null; try { d = JSON.parse(localStorage.getItem(EXAMS[exam].key) || "null"); } catch (e) { d = null; } return normalize(d, MAPS[exam]); },
    load() { for (const exam in EXAMS) this.all[exam] = this.read(exam); },
    pristine(d) { return !d.updatedAt && !d.settings.ts && !d.sessions.length && !Object.keys(d.answers).length && !Object.keys(d.flags).length && !Object.keys(d.notes).length && !Object.keys(d.reviewed || {}).length; },
    local() {                                           // an exam that has never been used gets no record at all
      if (this.pristine(this.d)) return;
      try { localStorage.setItem(EXAMS[EXAM].key, JSON.stringify(this.d)); } catch (e) { /* storage unavailable */ }
    },
    save() { if (!this.pristine(this.d)) { this.d.updatedAt = Date.now(); this.local(); } Sync.schedule(); },
    saveSettings() {                                   // settings live in the boards record, whichever exam is selected
      this.settings().ts = Date.now();
      if (EXAM === "boards") { this.save(); return; }
      try { localStorage.setItem(EXAMS.boards.key, JSON.stringify(this.all.boards)); } catch (e) { /* storage unavailable */ }
    },
  };
  function mergeInto(L, R) {
    R = normalize(R, MAPS.boards);
    for (const id in R.answers) {
      const a = L.answers[id], b = R.answers[id];
      if (!a) L.answers[id] = b;
      else {
        const first = (a.first && b.first && b.first.ts < a.first.ts) ? b.first : a.first || b.first;
        L.answers[id] = Object.assign({}, (b.ts || 0) > (a.ts || 0) ? b : a, { first, n: Math.max(a.n || 1, b.n || 1) });
      }
    }
    ["flags", "notes"].forEach((k) => { for (const id in R[k]) { const a = L[k][id], b = R[k][id]; if (!a || (b.ts || 0) > (a.ts || 0)) L[k][id] = b; } });
    const byId = Object.fromEntries(L.sessions.map((s) => [s.id, s]));
    R.sessions.forEach((s) => { const m = byId[s.id]; if (!m) L.sessions.push(s); else if ((s.updated || 0) > (m.updated || 0)) Object.assign(m, s); });
    L.sessions.sort((a, b) => (b.created || 0) - (a.created || 0));
    L.sessions = L.sessions.slice(0, 60);
    if ((R.settings.ts || 0) > (L.settings.ts || 0)) L.settings = R.settings;
  }
  const Sync = {
    ref: null, status: "local", timer: null, writing: false, pending: false, last: "",
    async init() {
      if (!window.claude || typeof window.claude.use !== "function") return;
      try {
        const [db, user] = await Promise.all([window.claude.use("db"), window.claude.use("user")]);
        if (!db || !user) return;
        const id = await user.id();
        if (!id) return;
        const ref = db.doc("data/users/" + id + "/progress");
        const snap = await ref.get();
        if (snap.exists) { mergeInto(Store.all.boards, JSON.parse(JSON.stringify(snap.data()))); if (EXAM === "boards") Store.local(); applySettings(); render(); }
        this.ref = ref; this.status = "sync";
        this.schedule();
        refreshSyncLabels();
      } catch (e) { this.ref = null; this.status = "local"; refreshSyncLabels(); }
    },
    schedule() { if (!this.ref) return; clearTimeout(this.timer); this.timer = setTimeout(() => this.flush(), 1800); },
    async flush() {
      if (!this.ref) return;
      if (this.writing) { this.pending = true; return; }
      this.writing = true;
      const body = JSON.stringify(Store.all.boards);
      if (body === this.last) { this.writing = false; return; }
      try { await this.ref.set(JSON.parse(body)); this.last = body; this.status = "sync"; }
      catch (e) {
        const code = e && e.code;
        if (code === "unavailable" || code === "resource_exhausted") setTimeout(() => this.schedule(), 4000 + Math.random() * 2000);
        else { this.ref = null; this.status = "local"; }
      }
      this.writing = false;
      if (this.pending) { this.pending = false; this.schedule(); }
      refreshSyncLabels();
    },
  };
  function syncText() { return Sync.status === "sync" ? "Your progress syncs to your Claude account, so it follows you across devices." : "Your progress is saved in this browser on this device."; }
  function refreshSyncLabels() { $$("[data-sync]").forEach((el) => (el.textContent = syncText())); }

  /* ---------------- derived state ---------------- */
  const A = (id) => Store.d.answers[id];
  const isFlag = (id) => !!(Store.d.flags[id] && Store.d.flags[id].on);
  const lastStatus = (id) => { const a = A(id); return !a ? "unused" : a.ok ? "correct" : "incorrect"; };
  const firstOk = (id) => { const a = A(id); return a && a.first ? a.first.ok : null; };
  function record(id, c, t) {
    const ok = c === QMAP[id].answer, now = Date.now(), a = A(id);
    if (!a) Store.d.answers[id] = { first: { c, ok, ts: now }, c, ok, t: Math.round(t || 0), ts: now, n: 1 };
    else Object.assign(a, { c, ok, t: Math.round(t || 0), ts: now, n: (a.n || 1) + 1 });
    return ok;
  }
  function pool(name) {
    if (name === "unused") return QB.filter((q) => !A(q.id));
    if (name === "incorrect") return QB.filter((q) => lastStatus(q.id) === "incorrect");
    if (name === "flagged") return QB.filter((q) => isFlag(q.id));
    return QB.slice();
  }
  const activeSession = () => Store.d.sessions.find((s) => !s.done && !s.temp);

  /* ---------------- UI state ---------------- */
  const UI = { tab: "home", ptab: "new", missedOnly: false, msec: null, mtab: "guide" };   // msec: the open MCAT section screen
  const P = { mode: "tutor", pool: "unused", systems: new Set(), diffs: new Set([3, 4, 5]), count: 10, shuffle: true, perQ: 90, sections: new Set(), skills: new Set() };
  /* "What's tested" guide UI state. Which groups are expanded is remembered in its own key (a convenience, like the exam
     choice); "Reviewed" marks are progress and live in the MCAT record (Store.all.mcat.reviewed). */
  const GUIDE_KEY = "rounds.guide.v1";
  const G = { q: "", open: {}, idx: null };
  try { Object.assign(G.open, JSON.parse(localStorage.getItem(GUIDE_KEY) || "{}").open || {}); } catch (e) { /* ignore */ }
  function saveGuideUI() { try { localStorage.setItem(GUIDE_KEY, JSON.stringify({ open: G.open })); } catch (e) { /* ignore */ } }
  const isOpen = (key, def) => (key in G.open ? !!G.open[key] : def);

  /* ---------------- settings ---------------- */
  function applyTheme(s) {
    const root = document.documentElement;
    if (s.theme === "system") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", s.theme);
    root.style.setProperty("--qfs", [15.5, 17, 19][s.font] + "px");
  }
  function applySettings() { applyTheme(Store.settings()); }

  /* ---------------- toast & sheet ---------------- */
  let toastT;
  function toast(msg) { const t = $("#toast"); t.textContent = msg; t.classList.add("on"); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove("on"), 2200); }
  let sheetOnClose = null, lastFocus = null;
  function openSheet(title, html, onClose) {
    closeSheet(true);
    lastFocus = document.activeElement;
    sheetOnClose = onClose || null;
    const root = $("#sheetroot");
    root.innerHTML = `<div class="backdrop" data-act="sheet-close"></div><div class="sheet" role="dialog" aria-modal="true" aria-label="${esc(title)}"><div class="grab"></div><div class="sh"><h2>${esc(title)}</h2><button class="iconbtn" data-act="sheet-close" aria-label="Close">${ICON.x}</button></div><div class="sb">${html}</div></div>`;
    requestAnimationFrame(() => { $(".backdrop", root).classList.add("on"); $(".sheet", root).classList.add("on"); const f = $(".sheet [data-autofocus]", root) || $(".sheet .iconbtn", root); f && f.focus(); });
  }
  function closeSheet(immediate) {
    const root = $("#sheetroot");
    if (!root.firstChild) return;
    const cb = sheetOnClose; sheetOnClose = null;
    if (immediate) root.innerHTML = "";
    else { $(".backdrop", root)?.classList.remove("on"); $(".sheet", root)?.classList.remove("on"); setTimeout(() => { if (!$(".sheet.on", root)) root.innerHTML = ""; }, 230); }
    cb && cb();
    if (!immediate && lastFocus && document.contains(lastFocus)) lastFocus.focus();
  }
  const sheetBody = () => $("#sheetroot .sb");

  /* ---------------- tabs ---------------- */
  function renderTabs() {
    const t = [["home", "Home", ICON.home], ["practice", "Practice", ICON.practice], ["anatomy", "Anatomy", ICON.body], ["progress", "Progress", ICON.chart]];
    $("#tabs").innerHTML = t.map(([k, n, ic]) => `<button data-act="tab" data-tab="${k}" ${UI.tab === k ? 'aria-current="page"' : ""}>${ic}<span>${n}</span></button>`).join("");
  }
  function render() {
    renderTabs();
    const v = $("#view");
    if (UI.tab === "anatomy") { v.innerHTML = Anat.view(); Anat.mount(); return; }
    if (!ready) { v.innerHTML = `<div class="boot"><p class="muted">Loading questions…</p></div>`; return; }
    if (UI.tab === "home") v.innerHTML = EXAM === "mcat" ? mcatHome() : viewHome();
    else if (UI.tab === "practice") v.innerHTML = EXAM === "mcat" ? (UI.msec ? mcatSection() : mcatPractice()) : viewPractice();
    else v.innerHTML = EXAM === "mcat" ? mcatProgress() : viewProgress();
    renderMath(v);
  }
  function go(tab) { UI.tab = tab; render(); window.scrollTo(0, 0); }

  /* ---------------- shared bits ---------------- */
  function qmapHTML() {
    return `<div class="qmap" role="list">${QB.map((q) => {
      const st = lastStatus(q.id);
      return `<button role="listitem" class="qcell ${st} ${isFlag(q.id) ? "flagged" : ""}" data-act="q-open" data-id="${q.id}" aria-label="Question ${QNUM[q.id]}, ${st}${isFlag(q.id) ? ", flagged" : ""}">${QNUM[q.id]}</button>`;
    }).join("")}</div>
    <div class="legend"><span><i style="background:var(--ok);border-color:var(--ok)"></i>Correct</span><span><i style="background:var(--bad);border-color:var(--bad)"></i>Incorrect</span><span><i></i>Not yet answered</span><span><i style="background:var(--flag);border-radius:50%;border-color:var(--flag)"></i>Flagged</span></div>`;
  }
  function summary() {
    const answered = QB.filter((q) => A(q.id));
    const firstCorrect = answered.filter((q) => firstOk(q.id)).length;
    const times = answered.map((q) => A(q.id).t || 0).filter((t) => t > 0);
    return { total: QB.length, answered: answered.length, pct: answered.length ? Math.round((firstCorrect / answered.length) * 100) : null, avg: times.length ? times.reduce((a, b) => a + b, 0) / times.length : null };
  }

  /* ---------------- exam switcher and the MCAT section (foundations only; no MCAT questions yet) ---------------- */
  function examSeg() {
    return `<div class="seg fit exam-seg" role="group" aria-label="Exam">${Object.keys(EXAMS).map((k) => `<button data-act="exam" data-v="${k}" aria-pressed="${EXAM === k}">${EXAMS[k].name}</button>`).join("")}</div>`;
  }
  function setExam(exam) {
    if (!EXAMS[exam] || exam === EXAM) return;
    try { localStorage.setItem(EXAM_KEY, exam); } catch (e) { /* ignore */ }
    activate(exam); UI.ptab = exam === "mcat" ? "sections" : "new"; UI.missedOnly = false; UI.msec = null; P.pool = "unused";
    render(); window.scrollTo(0, 0);
  }
  const MCAT_TM = `MCAT<sup>&#174;</sup> is a registered trademark of the Association of American Medical Colleges (AAMC), which is not affiliated with and does not endorse this app.`;
  const secInfo = (k) => Bank.mcat.sections.find((s) => s.k === k);
  const guideOf = (k) => (Bank.mcat.guides || {})[k];
  const guideTopics = (g) => (g.concepts || []).flatMap((c) => c.categories.flatMap((cat) => cat.topics));
  const reviewedMap = () => Store.all.mcat.reviewed || {};
  const reviewedCount = (g) => guideTopics(g).filter((t) => reviewedMap()[t.id]).length;
  function sectionCards() {
    return `<div class="list">${Bank.mcat.sections.map((s) => {
      const g = guideOf(s.k), n = (Bank.mcat.items || []).filter((q) => q.section === s.k).length;
      const meta = `${s.questions} questions, ${s.minutes} minutes${s.tools ? `, ${esc(s.tools.toLowerCase())} provided` : ""}` + (g && guideTopics(g).length ? ` · ${reviewedCount(g)} of ${guideTopics(g).length} topics reviewed` : "");
      return `<button class="li" data-act="msec" data-v="${s.k}"><div class="t"><b>${esc(s.short)}</b><span>${esc(s.name)}</span><span class="meta">${meta}</span></div><span class="badge${g ? " correct" : ""}">${n ? `${n} questions` : g ? "What's tested" : "Coming soon"}</span>${ICON.right}</button>`;
    }).join("")}</div>`;
  }
  function mcatHome() {
    const ready = Bank.mcat.sections.filter((s) => guideOf(s.k)).length;
    return `<div class="topline"><div class="wordmark">${ICON.logo}Rounds</div><span class="spacer"></span><button class="iconbtn" data-act="settings" aria-label="Settings">${ICON.gear}</button></div>${examSeg()}
      <h1>MCAT<sup>&#174;</sup> practice</h1><p class="status-line">${ready ? `Open a section to see everything it tests and mark topics as you review them. Questions come next.` : `The MCAT section is being built. Its four sections are set up; questions and the "What's tested" guides come next.`}</p>
      <h2>Sections</h2>${sectionCards()}
      <p class="hint" style="margin-top:14px">${MCAT_TM} Practice scores here are never official scaled scores.</p>${pearlHTML()}`;
  }
  function mcatPractice() {
    const tabs = [["sections", "Sections"], ["new", "Build"], ["history", "History"], ["takeaways", "Key points"]];
    let h = `${examSeg()}<h1>Practice</h1><div class="seg" role="group" aria-label="Practice sections" style="margin-top:12px">${tabs.map(([k, n]) => `<button data-act="ptab" data-v="${k}" aria-pressed="${UI.ptab === k}">${n}</button>`).join("")}</div>`;
    if (UI.ptab === "sections") h += `<p class="hint" style="margin:14px 2px 8px">${QB.length ? `${QB.length} questions so far. Open a section for its guide and practice, or build a block across sections.` : `No MCAT questions yet. Each section has a "What's tested" guide; practice blocks arrive as questions are written.`}</p>${sectionCards()}`;
    else if (UI.ptab === "new") h += QB.length ? mcatBuild() : `<div class="panel" style="margin-top:14px"><p style="margin:0">No MCAT questions yet. The first blocks arrive with Phase M2.</p></div>`;
    else if (UI.ptab === "history") h += practiceHistory();
    else h += practiceTakeaways();
    return h;
  }
  function mcatBuild() {
    const av = available(), n = Math.min(P.count, av.length);
    const pools = [["unused", "New"], ["incorrect", "Missed"], ["flagged", "Flagged"], ["all", "All"]];
    const skillNames = { "1": "Knowledge", "2": "Reasoning", "3": "Research design", "4": "Data" };
    let h = `<div class="panel" style="margin-top:14px">
      <div class="field" style="margin-top:0"><span class="lab">Mode</span><div class="seg" role="group" aria-label="Mode">
        <button data-act="p-mode" data-v="tutor" aria-pressed="${P.mode === "tutor"}">Tutor</button><button data-act="p-mode" data-v="timed" aria-pressed="${P.mode === "timed"}">Timed</button></div>
        <p class="hint" style="margin-top:8px">${P.mode === "tutor" ? "Each answer is checked right away, with the full explanation." : "Answers stay hidden until you end the block, like the real exam."}</p></div>
      <div class="field"><span class="lab">Questions from</span><div class="chips">${pools.map(([k, nm]) => `<button class="chip" data-act="p-pool" data-v="${k}" aria-pressed="${P.pool === k}">${nm} <span class="n">${pool(k).length}</span></button>`).join("")}</div></div>
      <div class="field"><span class="lab">Sections</span><div class="chips">${Bank.mcat.sections.filter((s) => QB.some((q) => q.section === s.k)).map((s) => `<button class="chip" data-act="p-section" data-v="${s.k}" aria-pressed="${P.sections.has(s.k)}">${esc(s.short)} <span class="n">${QB.filter((q) => q.section === s.k).length}</span></button>`).join("")}</div></div>
      <div class="field"><span class="lab">Skill</span><div class="chips">${["1", "2", "3", "4"].map((k) => `<button class="chip" data-act="p-skill" data-v="${k}" aria-pressed="${P.skills.has(k)}">${k} · ${skillNames[k]}</button>`).join("")}</div></div>
      <div class="field"><span class="lab">Difficulty</span><div class="chips">${[2, 3, 4, 5].map((d) => `<button class="chip" data-act="p-diff" data-v="${d}" aria-pressed="${P.diffs.has(d)}">${stars(d)}</button>`).join("")}</div></div>
      <div class="field"><span class="lab">Number of questions</span><div class="stepper"><button data-act="p-count" data-v="-1" aria-label="Fewer">−</button><output aria-live="polite">${n}</output><button data-act="p-count" data-v="1" aria-label="More">+</button><span class="hint" style="margin-left:6px">${av.length} available</span></div></div>`;
    if (P.mode === "timed") h += `<div class="field"><span class="lab">Time per question</span><div class="chips">${[60, 96, 120].map((t) => `<button class="chip" data-act="p-perq" data-v="${t}" aria-pressed="${P.perQ === t}">${t} sec</button>`).join("")}</div><p class="hint" style="margin-top:8px">The real exam allows about 96 seconds per science question (95 minutes for 59) and 102 per CARS question.</p></div>`;
    h += `<div class="field switch"><span class="lab" style="margin:0">Shuffle question order</span><button class="toggle" role="switch" aria-checked="${P.shuffle}" aria-label="Shuffle question order" data-act="p-shuffle"></button></div>
      <button class="btn block" style="margin-top:20px" data-act="start-custom" ${n ? "" : "disabled"}>${n ? `Start ${P.mode} block with ${n} question${n > 1 ? "s" : ""}` : "No questions match these filters"}</button></div>`;
    return h;
  }
  function mcatProgress() {
    const rows = Bank.mcat.sections.map((s) => { const g = guideOf(s.k); if (!g || !guideTopics(g).length) return ""; const n = guideTopics(g).length, r = reviewedCount(g), pct = n ? Math.round((100 * r) / n) : 0; return `<div class="bar-row"><div class="lab"><span>${esc(s.short)} topics reviewed</span><span class="muted">${r} of ${n}</span></div><div class="bar" role="img" aria-label="${pct}% reviewed"><i style="width:${pct}%"></i></div></div>`; }).join("");
    const stat = (qs) => { const ans = qs.filter((q) => A(q.id)), ok = ans.filter((q) => firstOk(q.id)).length; return { n: qs.length, ans: ans.length, ok, pct: ans.length ? Math.round((100 * ok) / ans.length) : 0 }; };
    const row = (label, qs) => { const t = stat(qs); return t.n ? `<div class="bar-row"><div class="lab"><span>${label}</span><span class="muted">${t.ans ? `${t.ok} of ${t.ans} right` : `${t.n} question${t.n === 1 ? "" : "s"}, not started`}</span></div><div class="bar" role="img" aria-label="${t.pct}% correct"><i style="width:${t.pct}%"></i></div></div>` : ""; };
    let h = `${examSeg()}<h1>Progress</h1>`;
    if (!QB.length) h += `<div class="panel" style="margin-top:14px"><p style="margin:0">No MCAT practice yet. MCAT progress is kept separately from your Boards progress and will show percent correct by section, content category, and skill, never a predicted scaled score.</p></div>`;
    else {
      const s = summary(), skillNames = { "1": "Knowledge of concepts", "2": "Reasoning and problem-solving", "3": "Research design", "4": "Data and statistics" };
      h += `<div class="kpis" style="margin-top:14px"><div class="kpi"><b>${s.answered}/${s.total}</b><span>Answered</span></div><div class="kpi"><b>${s.pct == null ? "–" : s.pct + "%"}</b><span>Right on first try</span></div><div class="kpi"><b>${s.avg == null ? "–" : fmt(s.avg)}</b><span>Average time</span></div></div>
        <p class="hint" style="margin:10px 2px 0">Percent correct only. This is not an MCAT scaled score; only AAMC's equating can produce one.</p>
        <h2>Question map</h2><div class="panel">${qmapHTML()}</div>
        <h2>By section</h2><div class="panel bars">${Bank.mcat.sections.map((sec) => row(esc(sec.short), QB.filter((q) => q.section === sec.k))).join("")}</div>
        <h2>By skill</h2><div class="panel bars">${["1", "2", "3", "4"].map((k) => row(`Skill ${k} · ${skillNames[k]}`, QB.filter((q) => String(q.skill) === k))).join("")}</div>
        <h2>By content category</h2><div class="panel bars">${Object.keys(Bank.mcat.categories || {}).map((c) => row(`${esc(c)} · ${esc(Bank.mcat.categories[c])}`, QB.filter((q) => q.category === c))).join("")}</div>
        <h2>By difficulty</h2><div class="panel bars">${[2, 3, 4, 5].map((d) => row(stars(d), QB.filter((q) => q.difficulty === d))).join("")}</div>`;
    }
    h += `${rows ? `<h2>What's tested</h2><div class="panel bars">${rows}</div>` : ""}
      <p class="hint" style="margin-top:18px" data-sync>${syncText()}</p>${QB.length ? `<button class="btn ghost" style="margin-top:6px" data-act="reset">Reset MCAT progress</button>` : ""}`;
    return h;
  }
  /* Periodic table sheet for the science sections (src/ptable.js). A search box finds an element; the grid scrolls sideways. */
  function openPTable() {
    openSheet("Periodic table", `<input class="search" type="search" placeholder="Element name or symbol" aria-label="Find an element" data-ptsearch data-autofocus>
      <div id="ptfound" class="hint" style="margin:8px 2px 0; min-height:20px"></div>
      <div class="scrollx" style="margin-top:8px"><div class="ptgrid" id="ptgrid">${PTABLE.map((e) => `<button class="pt-el${e[4] >= 8 ? " f" : ""}" style="grid-row:${e[4]};grid-column:${e[5]}" data-act="pt-pick" data-z="${e[0]}" aria-label="${esc(e[2])}, atomic number ${e[0]}, mass ${esc(e[3])}"><span class="z">${e[0]}</span><b>${esc(e[1])}</b><span class="m">${esc(e[3])}</span></button>`).join("")}</div></div>
      <p class="hint" style="margin-top:10px">Standard atomic weights rounded to one decimal; bracketed numbers are the mass number of a well-known isotope for elements with no standard weight (as on the IUPAC table). Lanthanides and actinides are the two rows below the main table.</p>`);
  }
  function ptFind(q) {
    q = q.trim().toLowerCase(); const box = $("#ptfound"); if (!box) return;
    $$("#ptgrid .pt-el.hit").forEach((el) => el.classList.remove("hit"));
    if (!q) { box.textContent = ""; return; }
    const e = PTABLE.find((x) => x[1].toLowerCase() === q) || PTABLE.find((x) => x[2].toLowerCase().startsWith(q)) || PTABLE.find((x) => String(x[0]) === q);
    if (!e) { box.textContent = "No element matches."; return; }
    box.innerHTML = `<b>${esc(e[2])}</b> (${esc(e[1])}): atomic number ${e[0]}, atomic mass ${esc(e[3])}`;
    const el = $(`#ptgrid [data-z="${e[0]}"]`); if (el) { el.classList.add("hit"); el.scrollIntoView({ block: "nearest", inline: "center", behavior: reduceMotion ? "auto" : "smooth" }); }
  }

  /* ---------------- MCAT section screen: Practice | What's tested (docs/MCAT_GUIDES_SPEC.md §5) ---------------- */
  function mcatSection() {
    const s = secInfo(UI.msec); if (!s) { UI.msec = null; return mcatPractice(); }
    const g = guideOf(s.k), n = (Bank.mcat.items || []).filter((q) => q.section === s.k).length;
    let h = `${examSeg()}<p style="margin:14px 0 0"><button class="btn quiet sm" data-act="msec" data-v="">${ICON.left} All sections</button></p>
      <h1>${esc(s.short)}</h1><p class="status-line">${esc(s.name)}. ${s.questions} questions in ${s.minutes} minutes${s.tools ? `, ${esc(s.tools.toLowerCase())} provided` : ""}.</p>
      <div class="seg" role="group" aria-label="Section view">${[["practice", "Practice"], ["guide", "What's tested"]].map(([k, nm]) => `<button data-act="mtab" data-v="${k}" aria-pressed="${UI.mtab === k}">${nm}</button>`).join("")}</div>`;
    if (UI.mtab === "practice") {
      if (!n) h += `<div class="panel" style="margin-top:14px"><p style="margin:0">No ${esc(s.short)} questions yet. They arrive in blocks, each tagged to a topic in "What's tested", so you can practice any topic from the guide.</p></div>`;
      else {
        const qs = QB.filter((q) => q.section === s.k), unused = qs.filter((q) => !A(q.id)).length, missed = qs.filter((q) => lastStatus(q.id) === "incorrect").length;
        h += `<p class="status-line" style="margin-top:14px">${n} question${n === 1 ? "" : "s"}, ${unused} still new${missed ? `, ${missed} missed` : ""}.</p>
          <div class="start-grid"><button class="start-card primary" data-act="msec-start" data-mode="tutor"><b>Tutor block</b><span>Explanation after each answer.</span></button><button class="start-card" data-act="msec-start" data-mode="timed"><b>Timed block</b><span>About ${MCAT_PERQ[s.k] || 96} seconds each, like the exam.</span></button></div>
          <div class="chips" style="margin-top:12px"><button class="chip" data-act="msec-start" data-mode="tutor" data-pool="incorrect" ${missed ? "" : "disabled"}>Redo missed <span class="n">${missed}</span></button><button class="chip" data-act="ptab-go" data-v="new">Build a custom block</button></div>
          <h2>Questions</h2><div class="list">${qs.map((q) => { const st = lastStatus(q.id); const badge = st === "correct" ? '<span class="badge correct">Correct</span>' : st === "incorrect" ? '<span class="badge incorrect">Incorrect</span>' : '<span class="badge">New</span>'; return `<button class="li" data-act="q-open" data-id="${q.id}"><div class="t"><b>${esc(q.category)} · ${esc(q.sys)}</b><span>${stars(q.difficulty)} Skill ${esc(q.skill)}${isFlag(q.id) ? ' <span class="badge flag">Flagged</span>' : ""}</span></div>${badge}${ICON.right}</button>`; }).join("")}</div>`;
      }
    }
    else h += g ? guideHTML(g) : `<div class="panel" style="margin-top:14px"><p style="margin:0">The ${esc(s.short)} guide is being written. Chem/Phys is first.</p></div>`;
    return h;
  }
  const ext = (url, text) => `<a href="${esc(url)}" target="_blank" rel="noopener">${text}</a>`;
  function guideHTML(g) {
    return `<p class="hint" style="margin:12px 2px 0">${esc(g.attribution || "")} ${ext(g.official_outline_url, "Official outline")}${g.official_prep_url ? ` · ${ext(g.official_prep_url, "AAMC free prep resources")}` : ""} · Last verified ${esc(g.verified)}.</p>
      <div class="search-wrap" style="margin-top:12px"><input class="search" type="search" placeholder="Search every guide" aria-label="Search every guide" data-gsearch value="${esc(G.q)}"></div>
      <div id="gbody">${G.q.trim() ? guideResultsHTML() : guideBodyHTML(g)}</div>`;
  }
  const topicItems = (id) => (Bank.mcat.items || []).filter((q) => (q.topics || []).includes(id));
  const catItems = (code) => (Bank.mcat.items || []).filter((q) => q.category === code);
  function accuracy(items) {
    const ans = items.filter((q) => Store.all.mcat.answers[q.id]), ok = ans.filter((q) => { const a = Store.all.mcat.answers[q.id]; return a.first ? a.first.ok : a.ok; }).length;
    return { n: items.length, answered: ans.length, pct: ans.length ? Math.round((100 * ok) / ans.length) : null };
  }
  const accText = (a) => (!a.n ? "" : a.answered ? `${a.pct}% right on first try (${a.answered} of ${a.n})` : `${a.n} question${a.n === 1 ? "" : "s"}, not started`);
  const barRow = (label, pct, note) => `<div class="bar-row"><div class="lab"><span>${label}</span><span class="muted">${note == null ? `${pct}%` : note}</span></div><div class="bar" role="img" aria-label="${pct}%"><i style="width:${pct}%"></i></div></div>`;
  const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);
  const eqHTML = (e) => `<div class="eq" data-tex="${esc(e)}"><code>${esc(e)}</code></div>`;
  function glanceHTML(g) {
    const gl = g.glance || {};
    return `<h2>At a glance</h2><div class="panel"><div class="kpis"><div class="kpi"><b>${gl.questions}</b><span>Questions</span></div><div class="kpi"><b>${gl.minutes}</b><span>Minutes</span></div><div class="kpi"><b>${gl.discrete_questions ? `${gl.passage_questions}+${gl.discrete_questions}` : gl.passage_questions}</b><span>${gl.discrete_questions ? "Passage + discrete" : "All passage-based"}</span></div></div>
      <p style="margin:14px 0 0">${esc(gl.summary || "")}</p>${gl.math ? `<p style="margin:10px 0 0"><b>Math:</b> ${esc(gl.math)}</p>` : ""}
      <p style="margin:10px 0 0"><b>Tools:</b> ${esc(gl.tools || "none")}. ${gl.calculator ? "Calculator allowed." : "No calculator."}</p>${gl.scores_note ? `<p class="hint" style="margin:10px 0 0">${esc(gl.scores_note)}</p>` : ""}</div>`;
  }
  function carsBodyHTML(g) {
    const bp = g.blueprint || {}, names = { foundations: "Foundations of Comprehension", within: "Reasoning Within the Text", beyond: "Reasoning Beyond the Text" };
    let h = glanceHTML(g);
    h += `<h2>Blueprint</h2><div class="panel bars"><h3 style="margin:0">By skill</h3>${Object.entries(bp.cars_skills || {}).map(([k, v]) => barRow(esc(names[k] || k), v)).join("")}
      <h3 style="margin:6px 0 0">By passage content</h3>${Object.entries(bp.passage_content || {}).map(([k, v]) => barRow(esc(cap(k)), v)).join("")}
      <p class="hint" style="margin:4px 0 0">AAMC's published weightings, rounded to the nearest 5%; they vary a little from one test to another.</p></div>`;
    if (g.no_outside_knowledge) h += `<div class="callout" style="margin-top:14px"><b>No outside knowledge</b> ${esc(g.no_outside_knowledge)}</div>`;
    h += `<h2>Passage types</h2>${(g.passage_types || []).map((p) => `<div class="panel" style="margin-top:10px"><b>${esc(p.name)}</b> <span class="muted small">${p.pct}% of passages</span><p style="margin:6px 0 0">${esc(p.what)}</p><p class="hint" style="margin:6px 0 0">Drawn from ${(p.disciplines || []).map(esc).join(", ")}, among others.</p></div>`).join("")}`;
    h += `<h2>Skill areas</h2><p class="hint" style="margin:-4px 2px 10px">AAMC's three skill names; the explanations and examples are our own.</p>${(g.skill_areas || []).map((s) => `<details class="gt" data-okey="s:${esc(s.id)}" ${isOpen("s:" + s.id, true) ? "open" : ""}><summary><span class="gsum"><b>${esc(s.name)}</b><span class="meta">${s.pct}% of the section</span></span></summary><div class="gt-body"><p style="margin:0 0 8px">${esc(s.what)}</p><p style="margin:0 0 4px"><b>What questions ask:</b></p><ul class="know">${(s.asks || []).map((a) => `<li>${esc(a)}</li>`).join("")}</ul>${s.example ? `<div class="callout"><b>Example</b> ${esc(s.example)}</div>` : ""}</div></details>`).join("")}`;
    h += `<h2>Wrong-answer patterns</h2>${(g.wrong_answer_patterns || []).map((w) => `<details class="gt" data-okey="w:${esc(w.name)}" ${isOpen("w:" + w.name, false) ? "open" : ""}><summary><span class="gsum"><b>${esc(w.name)}</b></span></summary><div class="gt-body"><p style="margin:0">${esc(w.what)}</p>${w.spot ? `<p class="hint" style="margin:8px 0 0"><b>How to spot it:</b> ${esc(w.spot)}</p>` : ""}</div></details>`).join("")}`;
    h += `<h2>Approaches</h2><p class="hint" style="margin:-4px 2px 10px">Options to try, not rules. Keep what raises your score.</p>${(g.approaches || []).map((a) => `<details class="gt" data-okey="a:${esc(a.name)}" ${isOpen("a:" + a.name, false) ? "open" : ""}><summary><span class="gsum"><b>${esc(a.name)}</b></span></summary><div class="gt-body"><p style="margin:0">${esc(a.what)}</p></div></details>`).join("")}`;
    return h;
  }
  function guideBodyHTML(g) {
    if (!g.concepts) return carsBodyHTML(g);
    const bp = g.blueprint || {}, rv = reviewedMap();
    let h = glanceHTML(g);
    h += `<h2>Blueprint</h2><div class="panel bars"><h3 style="margin:0">By discipline</h3>${Object.entries(bp.disciplines || {}).map(([k, v]) => barRow(esc(cap(k)), v)).join("")}
      <h3 style="margin:6px 0 0">By foundational concept</h3>${(g.concepts || []).map((c) => barRow(`FC${esc(c.id)} · ${esc(c.name)}`, (bp.concepts || {})[c.id] || 0)).join("")}
      <h3 style="margin:6px 0 0">By skill</h3>${(g.skills || []).map((s) => barRow(`Skill ${esc(s.id)} · ${esc(s.name)}`, (bp.skills || {})[s.id] || s.pct || 0)).join("")}
      <p class="hint" style="margin:4px 0 0">AAMC's published weightings, rounded to the nearest 5%; they vary a little from one test to another.</p></div>`;
    h += `<h2>Content map</h2><p class="hint" style="margin:-4px 2px 10px">Tap a concept, then a category, then a topic. Tick "Reviewed" as you go.</p>`;
    (g.concepts || []).forEach((c) => {
      const topics = c.categories.flatMap((cat) => cat.topics), r = topics.filter((t) => rv[t.id]).length;
      h += `<details class="gc" data-okey="c:${esc(c.id)}" ${isOpen("c:" + c.id, true) ? "open" : ""}><summary><span class="gsum"><b>Foundational Concept ${esc(c.id)} · ${esc(c.name)}</b><span class="meta">${r} of ${topics.length} topics reviewed</span></span></summary>
        <div class="gc-body"><p class="hint" style="margin:0 0 4px">${esc(c.summary || "")}</p>`;
      c.categories.forEach((cat) => {
        const cr = cat.topics.filter((t) => rv[t.id]).length, a = accuracy(catItems(cat.id));
        h += `<details class="gcat" data-okey="k:${esc(cat.id)}" ${isOpen("k:" + cat.id, false) ? "open" : ""}><summary><span class="gsum"><b>${esc(cat.id)} · ${esc(cat.name)}</b><span class="meta">${cr} of ${cat.topics.length} reviewed${a.n ? ` · ${accText(a)}` : ""}</span></span></summary>
          <div class="gcat-body"><p class="hint" style="margin:0">${esc(cat.summary || "")}</p>${cat.topics.map((t) => topicHTML(t)).join("")}</div></details>`;
      });
      h += `</div></details>`;
    });
    if ((g.skills || []).length) h += `<h2>Skills</h2><div class="panel">${g.skills.map((s, i) => `<div class="skill${i ? "" : " first"}"><b>Skill ${esc(s.id)} · ${esc(s.name)}</b> <span class="muted small">${s.pct}% of the section</span><p style="margin:6px 0 0">${esc(s.what)}</p><p class="hint" style="margin:6px 0 0"><b>What a question might ask:</b> ${esc(s.example)}</p></div>`).join("")}<p class="hint" style="margin:12px 0 0">Skill names are AAMC's; the explanations and examples are our own.</p></div>`;
    if ((g.research_methods || []).length) h += `<h2>Research methods and statistics</h2>${g.research_methods.map((m) => blockHTML("r", m)).join("")}`;
    if ((g.math_toolkit || []).length) h += `<h2>Math toolkit</h2><p class="hint" style="margin:-4px 2px 10px">No-calculator techniques, with worked examples.</p>${g.math_toolkit.map((m) => blockHTML("m", m)).join("")}`;
    return h;
  }
  function blockHTML(kind, m) {
    const key = `${kind}:${m.name}`;
    return `<details class="gt" data-okey="${esc(key)}" ${isOpen(key, false) ? "open" : ""}><summary><span class="gsum"><b>${esc(m.name)}</b></span></summary><div class="gt-body"><ul class="know">${(m.know || []).map((k) => `<li>${esc(k)}</li>`).join("")}</ul>
      ${(m.equations || []).length ? `<div class="eqs">${m.equations.map(eqHTML).join("")}</div>` : ""}${m.example ? `<div class="callout"><b>Example</b> ${esc(m.example)}</div>` : ""}</div></details>`;
  }
  function topicHTML(t) {
    const rv = !!reviewedMap()[t.id], items = topicItems(t.id), a = accuracy(items);
    return `<details class="gt" id="t-${esc(t.id)}" data-okey="t:${esc(t.id)}" ${isOpen("t:" + t.id, false) ? "open" : ""}><summary><span class="gsum"><b>${esc(t.name)}</b><span class="meta">${(t.tags || []).map((x) => `<span class="tag-d">${esc(x)}</span>`).join("")}${rv ? `<span class="badge correct">Reviewed</span>` : ""}</span></span></summary>
      <div class="gt-body"><ul class="know">${t.know.map((k) => `<li>${esc(k)}</li>`).join("")}</ul>
      ${(t.equations || []).length ? `<div class="eqs">${t.equations.map(eqHTML).join("")}</div>` : ""}
      ${(t.confusions || []).length ? `<div class="callout"><b>Watch out</b> ${t.confusions.map(esc).join(" ")}</div>` : ""}
      ${(t.refs || []).length ? `<p class="hint refs">References (links only): ${t.refs.map((r) => (r.url ? ext(r.url, esc(r.label)) : esc(r.label))).join(" · ")}</p>` : ""}
      <div class="row wrap gt-foot"><label class="chk"><input type="checkbox" data-reviewed="${esc(t.id)}" ${rv ? "checked" : ""}> Reviewed</label><span class="spacer"></span>${items.length ? `<span class="small muted">${accText(a)}</span><button class="btn ghost sm" data-act="g-practice" data-id="${esc(t.id)}">Practice this topic</button>` : `<span class="small muted">No questions yet</span>`}</div></div></details>`;
  }
  function guideIndex() {
    if (G.idx) return G.idx;
    G.idx = [];
    for (const sec in Bank.mcat.guides || {}) {
      const g = Bank.mcat.guides[sec];
      (g.concepts || []).forEach((c) => c.categories.forEach((cat) => cat.topics.forEach((t) => G.idx.push({ sec, c: c.id, cat, t, text: [t.name, cat.name, cat.id, ...t.know, ...(t.equations || []), ...(t.confusions || [])].join(" ").toLowerCase() }))));
    }
    return G.idx;
  }
  function guideResultsHTML() {
    const words = G.q.toLowerCase().split(/\s+/).filter(Boolean);
    const hits = guideIndex().filter((e) => words.every((w) => e.text.includes(w))).slice(0, 40);
    if (!hits.length) return `<div class="panel" style="margin-top:14px"><p style="margin:0">Nothing in the guides matches "${esc(G.q)}".</p></div>`;
    return `<p class="hint" style="margin:12px 2px 8px">${hits.length === 40 ? "First 40 matches" : `${hits.length} match${hits.length === 1 ? "" : "es"}`} across the guides.</p><div class="list">${hits.map((e) => { const s = secInfo(e.sec); return `<button class="li" data-act="g-go" data-sec="${e.sec}" data-id="${esc(e.t.id)}"><div class="t"><b>${esc(e.t.name)}</b><span>${esc(e.cat.id)} · ${esc(e.cat.name)}</span><span class="meta">${esc(e.t.know[0]).slice(0, 120)}…</span></div><span class="badge">${esc(s ? s.short : e.sec)}</span>${ICON.right}</button>`; }).join("")}</div>`;
  }
  function refreshGuideBody() {
    const b = $("#gbody"); if (!b) return;
    const g = guideOf(UI.msec); if (!g) return;
    const y = window.scrollY; b.innerHTML = G.q.trim() ? guideResultsHTML() : guideBodyHTML(g); renderMath(b); window.scrollTo(0, y);
  }
  function openTopic(sec, id) {
    G.q = ""; UI.msec = sec; UI.mtab = "guide"; UI.tab = "practice";
    const e = guideIndex().find((x) => x.sec === sec && x.t.id === id);
    if (e) { G.open["c:" + e.c] = true; G.open["k:" + e.cat.id] = true; G.open["t:" + id] = true; saveGuideUI(); }
    render();
    const el = document.getElementById("t-" + id); if (el) el.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
  }
  function setReviewed(id, on) {
    const d = Store.all.mcat; d.reviewed = d.reviewed || {};
    if (on) d.reviewed[id] = Date.now(); else delete d.reviewed[id];
    if (EXAM === "mcat") Store.save(); else { try { if (!Store.pristine(d)) localStorage.setItem(EXAMS.mcat.key, JSON.stringify(d)); } catch (e) { /* ignore */ } }
    refreshGuideBody();
  }
  /* KaTeX (vendor/katex, MIT) is loaded the first time a guide shows an equation; until then the TeX source stays visible. */
  let katexLoad = null;
  function loadKatex() {
    if (window.katex) return Promise.resolve();
    if (katexLoad) return katexLoad;
    const v = typeof ASSET_V === "object" && ASSET_V.katex ? `?v=${ASSET_V.katex}` : "";
    katexLoad = new Promise((resolve, reject) => {
      const l = document.createElement("link"); l.rel = "stylesheet"; l.href = "vendor/katex/katex.min.css" + v; document.head.appendChild(l);
      const s = document.createElement("script"); s.src = "vendor/katex/katex.min.js" + v; s.onload = resolve; s.onerror = () => { katexLoad = null; reject(new Error("KaTeX failed to load")); }; document.head.appendChild(s);
    });
    return katexLoad;
  }
  function renderMath(root) {
    if (!$("[data-tex]:not([data-done])", root)) return;
    loadKatex().then(() => $$("[data-tex]:not([data-done])", root).forEach((el) => {
      try { window.katex.render(el.dataset.tex, el, { throwOnError: false, displayMode: true, output: "htmlAndMathml" }); } catch (e) { /* keep the TeX text */ }
      el.dataset.done = "1";
    })).catch(() => { /* equations stay as TeX text */ });
  }
  function pearlHTML() {
    const keys = Object.keys(INFO);
    const day = Math.floor(Date.now() / 864e5);
    const k = keys[day % keys.length], inf = INFO[k], lay = LAYERS.find((l) => l.k === inf.L);
    return `<h2>Anatomy pearl of the day</h2><div class="panel"><div class="pearl"><span class="k">${esc(lay.n)}</span><h3 style="margin:2px 0 6px">${esc(inf.n)}</h3><p>${esc(inf.p)}</p></div>
      <button class="btn ghost sm" data-act="show-fig" data-fig="${k}">See it on the body</button></div>`;
  }

  /* ---------------- home ---------------- */
  function viewHome() {
    const s = summary(), act = activeSession();
    const unused = pool("unused").length, missed = pool("incorrect").length, flagged = pool("flagged").length;
    const line = s.answered === 0 ? `${s.total} questions ready. Start with a tutor block to see explanations as you go.` :
      s.answered === s.total ? `All ${s.total} questions answered. Review what you missed or retake a timed block.` :
      `${s.answered} of ${s.total} answered. ${unused} still new.`;
    let h = `<div class="topline"><div class="wordmark">${ICON.logo}Rounds</div><span class="spacer"></span><button class="iconbtn" data-act="settings" aria-label="Settings">${ICON.gear}</button></div>${examSeg()}
      <h1>Ready for a block?</h1><p class="status-line">${line}</p>`;
    if (act) {
      const done = Object.keys(act.mode === "tutor" ? act.resp : act.sel).length;
      h += `<div class="panel resume"><div class="meta"><b>Pick up where you left off</b><span class="muted small">${act.mode === "tutor" ? "Tutor" : "Timed"} block, question ${act.idx + 1} of ${act.qids.length}, ${done} answered</span></div><button class="btn" data-act="resume">Resume</button></div>
        <p class="small" style="margin:8px 4px 0"><button class="btn quiet sm" data-act="discard">Discard this block</button></p>`;
    }
    h += `<h2>Start practicing</h2><div class="start-grid">
      <button class="start-card primary" data-act="quick" data-mode="tutor"><b>Tutor block</b><span>See the explanation right after each answer.</span></button>
      <button class="start-card" data-act="quick" data-mode="timed"><b>Timed block</b><span>Exam pace, about 90 seconds each. Review at the end.</span></button></div>
      <div class="chips" style="margin-top:12px">
        <button class="chip" data-act="start-pool" data-pool="incorrect" ${missed ? "" : "disabled"}>Redo missed <span class="n">${missed}</span></button>
        <button class="chip" data-act="start-pool" data-pool="flagged" ${flagged ? "" : "disabled"}>Flagged <span class="n">${flagged}</span></button>
        <button class="chip" data-act="tab" data-tab="practice">Build a custom block</button></div>
      <h2>Your question bank</h2><div class="panel">${qmapHTML()}</div>`;
    h += pearlHTML();
    return h;
  }

  /* ---------------- practice ---------------- */
  function available() {
    if (EXAM === "mcat") return pool(P.pool).filter((q) => P.sections.has(q.section) && P.skills.has(String(q.skill)) && P.diffs.has(q.difficulty));
    return pool(P.pool).filter((q) => P.systems.has(q.sys) && P.diffs.has(q.difficulty));
  }
  function viewPractice() {
    const tabs = [["new", "Build"], ["library", "Questions"], ["history", "History"], ["takeaways", "Key points"]];
    let h = `${examSeg()}<h1>Practice</h1><div class="seg" role="group" aria-label="Practice sections" style="margin-top:12px">${tabs.map(([k, n]) => `<button data-act="ptab" data-v="${k}" aria-pressed="${UI.ptab === k}">${n}</button>`).join("")}</div>`;
    if (UI.ptab === "new") h += practiceNew();
    else if (UI.ptab === "library") h += practiceLibrary();
    else if (UI.ptab === "history") h += practiceHistory();
    else h += practiceTakeaways();
    return h;
  }
  function practiceNew() {
    const av = available();
    const n = Math.min(P.count, av.length);
    const pools = [["unused", "New"], ["incorrect", "Missed"], ["flagged", "Flagged"], ["all", "All"]];
    let h = `<div class="panel" style="margin-top:14px">
      <div class="field" style="margin-top:0"><span class="lab">Mode</span><div class="seg" role="group" aria-label="Mode">
        <button data-act="p-mode" data-v="tutor" aria-pressed="${P.mode === "tutor"}">Tutor</button><button data-act="p-mode" data-v="timed" aria-pressed="${P.mode === "timed"}">Timed</button></div>
        <p class="hint" style="margin-top:8px">${P.mode === "tutor" ? "Each answer is checked right away, with the full explanation." : "Answers stay hidden until you end the block, like the real exam."}</p></div>
      <div class="field"><span class="lab">Questions from</span><div class="chips">${pools.map(([k, nm]) => `<button class="chip" data-act="p-pool" data-v="${k}" aria-pressed="${P.pool === k}">${nm} <span class="n">${pool(k).length}</span></button>`).join("")}</div></div>
      <div class="field"><span class="lab">Systems</span><div class="chips">${SYSTEMS.map((s) => `<button class="chip" data-act="p-sys" data-v="${esc(s)}" aria-pressed="${P.systems.has(s)}">${esc(s)}</button>`).join("")}</div></div>
      <div class="field"><span class="lab">Difficulty</span><div class="chips">${[3, 4, 5].map((d) => `<button class="chip" data-act="p-diff" data-v="${d}" aria-pressed="${P.diffs.has(d)}">${stars(d)}</button>`).join("")}</div></div>
      <div class="field"><span class="lab">Number of questions</span><div class="stepper"><button data-act="p-count" data-v="-1" aria-label="Fewer">−</button><output aria-live="polite">${n}</output><button data-act="p-count" data-v="1" aria-label="More">+</button><span class="hint" style="margin-left:6px">${av.length} available</span></div></div>`;
    if (P.mode === "timed") h += `<div class="field"><span class="lab">Time per question</span><div class="chips">${[60, 90, 120].map((t) => `<button class="chip" data-act="p-perq" data-v="${t}" aria-pressed="${P.perQ === t}">${t} sec</button>`).join("")}</div><p class="hint" style="margin-top:8px">The real exam allows about 90 seconds per question.</p></div>`;
    h += `<div class="field switch"><span class="lab" style="margin:0">Shuffle question order</span><button class="toggle" role="switch" aria-checked="${P.shuffle}" aria-label="Shuffle question order" data-act="p-shuffle"></button></div>
      <button class="btn block" style="margin-top:20px" data-act="start-custom" ${n ? "" : "disabled"}>${n ? `Start ${P.mode} block with ${n} question${n > 1 ? "s" : ""}` : "No questions match these filters"}</button></div>`;
    return h;
  }
  function practiceLibrary() {
    let h = `<p class="hint" style="margin:14px 2px 8px">Tap a question to try it or read its explanation.</p>`;
    SYSTEMS.forEach((sys) => {
      const qs = QB.filter((q) => q.sys === sys);
      h += `<h3>${esc(sys)}</h3><div class="list">${qs.map((q) => {
        const st = lastStatus(q.id);
        const badge = st === "correct" ? '<span class="badge correct">Correct</span>' : st === "incorrect" ? '<span class="badge incorrect">Incorrect</span>' : '<span class="badge">New</span>';
        return `<button class="li" data-act="q-open" data-id="${q.id}"><div class="t"><b>Question ${QNUM[q.id]}</b><span>${stars(q.difficulty)} ${isFlag(q.id) ? '<span class="badge flag">Flagged</span>' : ""}</span></div>${badge}${ICON.right}</button>`;
      }).join("")}</div>`;
    });
    return h;
  }
  function sessionScore(s) {
    const ok = s.qids.filter((id) => s.resp[id] && s.resp[id].ok).length;
    return { ok, total: s.qids.length, pct: s.qids.length ? Math.round((ok / s.qids.length) * 100) : 0 };
  }
  function practiceHistory() {
    const done = Store.d.sessions.filter((s) => s.done && !s.temp);
    if (!done.length) return `<div class="panel" style="margin-top:14px"><p style="margin:0">Finished blocks show up here with their scores. Start one from Build.</p></div>`;
    return `<div class="list" style="margin-top:14px">${done.map((s) => {
      const sc = sessionScore(s);
      const d = new Date(s.finished || s.created);
      return `<button class="li" data-act="hist-open" data-sid="${s.id}"><div class="t"><b>${s.mode === "tutor" ? "Tutor" : "Timed"} block, ${sc.ok} of ${sc.total} correct</b><span>${d.toLocaleDateString(undefined, { month: "short", day: "numeric" })} at ${d.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" })}, ${fmt(s.elapsed || 0)} total</span></div><span class="badge ${sc.pct >= 70 ? "correct" : "incorrect"}">${sc.pct}%</span>${ICON.right}</button>`;
    }).join("")}</div>`;
  }
  function practiceTakeaways() {
    const answered = QB.filter((q) => A(q.id));
    const list = UI.missedOnly ? answered.filter((q) => firstOk(q.id) === false) : answered;
    let h = `<div class="field switch" style="margin-top:16px"><span class="lab" style="margin:0">Only questions I missed</span><button class="toggle" role="switch" aria-checked="${UI.missedOnly}" aria-label="Only questions I missed" data-act="missed-only"></button></div>`;
    if (!answered.length) return h + `<div class="panel" style="margin-top:12px"><p style="margin:0">The key teaching point from every question you answer collects here as a quick review sheet.</p></div>`;
    if (!list.length) return h + `<div class="panel" style="margin-top:12px"><p style="margin:0">Nothing missed on the first try. Nice.</p></div>`;
    return h + list.map((q) => {
      const note = Store.d.notes[q.id] && Store.d.notes[q.id].text;
      return `<div class="panel" style="margin-top:12px"><div class="row" style="margin-bottom:6px"><span class="badge ${firstOk(q.id) ? "correct" : "incorrect"}">${firstOk(q.id) ? "Got it" : "Missed"}</span><span class="muted small">${esc(q.sys)}</span><span class="spacer"></span><button class="btn quiet sm" data-act="read-exp" data-id="${q.id}">Open</button></div>
        <p style="margin:0">${q.objective}</p>${note ? `<p class="small muted" style="margin:8px 0 0"><b>Your note:</b> ${esc(note)}</p>` : ""}</div>`;
    }).join("");
  }

  /* ---------------- progress ---------------- */
  function viewProgress() {
    const s = summary();
    let h = `${examSeg()}<h1>Progress</h1><div class="kpis" style="margin-top:14px">
      <div class="kpi"><b>${s.answered}/${s.total}</b><span>Answered</span></div>
      <div class="kpi"><b>${s.pct == null ? "–" : s.pct + "%"}</b><span>Right on first try</span></div>
      <div class="kpi"><b>${s.avg == null ? "–" : fmt(s.avg)}</b><span>Average time</span></div></div>
      <h2>Question map</h2><div class="panel">${qmapHTML()}</div><h2>By system</h2><div class="panel bars">`;
    SYSTEMS.forEach((sys) => {
      const qs = QB.filter((q) => q.sys === sys), ans = qs.filter((q) => A(q.id)), ok = ans.filter((q) => firstOk(q.id)).length;
      const pct = ans.length ? Math.round((ok / ans.length) * 100) : 0;
      h += `<div class="bar-row"><div class="lab"><span>${esc(sys)}</span><span class="muted">${ans.length ? `${ok} of ${ans.length} right` : "Not started"}</span></div><div class="bar" role="img" aria-label="${pct}% correct"><i style="width:${pct}%"></i></div></div>`;
    });
    h += `</div><h2>By difficulty</h2><div class="panel bars">`;
    [3, 4, 5].forEach((d) => {
      const qs = QB.filter((q) => q.difficulty === d), ans = qs.filter((q) => A(q.id)), ok = ans.filter((q) => firstOk(q.id)).length;
      const pct = ans.length ? Math.round((ok / ans.length) * 100) : 0;
      h += `<div class="bar-row"><div class="lab"><span>${stars(d)}</span><span class="muted">${ans.length ? `${ok} of ${ans.length} right` : `${qs.length} question${qs.length === 1 ? "" : "s"}, not started`}</span></div><div class="bar" role="img" aria-label="${pct}% correct"><i style="width:${pct}%"></i></div></div>`;
    });
    h += `</div><p class="hint" style="margin-top:18px" data-sync>${syncText()}</p>
      <button class="btn ghost" style="margin-top:6px" data-act="reset">Reset all progress</button>`;
    return h;
  }

  /* ---------------- settings ---------------- */
  function openSettings() {
    const s = Store.settings(), blocks = new Set(Bank.boards.map((q) => q.id.split("-")[0])).size;
    openSheet("Settings", `
      <div class="field" style="margin-top:4px"><span class="lab">Appearance</span><div class="seg" role="group" aria-label="Appearance">${[["system", "Match device"], ["light", "Light"], ["dark", "Dark"]].map(([k, n]) => `<button data-act="set-theme" data-v="${k}" aria-pressed="${s.theme === k}">${n}</button>`).join("")}</div></div>
      <div class="field"><span class="lab">Question text size</span><div class="seg" role="group" aria-label="Question text size">${["Small", "Medium", "Large"].map((n, i) => `<button data-act="set-font" data-v="${i}" aria-pressed="${s.font === i}">${n}</button>`).join("")}</div></div>
      <div class="field"><span class="lab">Saving</span><p class="hint" data-sync>${syncText()}</p></div>
      <div class="field"><span class="lab">About</span><p class="hint">Boards: ${Bank.boards.length} original Step 2 CK–style questions in ${blocks} block${blocks === 1 ? "" : "s"}. Each explanation cites the guideline it was checked against (October 2026). MCAT<sup>&#174;</sup>: in progress. Keyboard: A–E to choose, Enter to submit, arrow keys to move, F to flag.</p>
      <p class="hint">Rounds is an independent, free study resource. It is not affiliated with, endorsed by, or sponsored by the AAMC, FSMB, or NBME. Practice scores are not predictions of official scores. Content is for exam study only and is not medical advice. ${MCAT_TM} USMLE<sup>&#174;</sup> is a program of the Federation of State Medical Boards (FSMB) and the National Board of Medical Examiners (NBME).</p></div>
      <button class="btn ghost block" data-act="reset" style="margin-top:8px">Reset all progress</button>`);
  }
  function confirmReset() {
    openSheet("Reset all progress?", `<p>This clears every answer, flag, note, and block history${Sync.status === "sync" ? " on all your devices" : " in this browser"}. It can't be undone.</p>
      <div class="row" style="margin-top:16px"><button class="btn ghost" data-act="sheet-close" data-autofocus>Keep my progress</button><button class="btn danger" data-act="reset-confirm">Reset progress</button></div>`);
  }

  /* ---------------- sessions ---------------- */
  function startSession(mode, qs, opts = {}) {
    if (!qs.length) { toast("No questions match."); return; }
    const act = opts.temp ? null : activeSession();
    if (act && !opts.force) {
      openSheet("You have a block in progress", `<p>Starting a new block will discard your unfinished ${act.mode} block (question ${act.idx + 1} of ${act.qids.length}).</p>
        <div class="row wrap" style="margin-top:16px"><button class="btn ghost" data-act="resume" data-autofocus>Resume it instead</button><button class="btn danger" data-act="force-start">Discard and start new</button></div>`);
      pendingStart = () => startSession(mode, qs, Object.assign({}, opts, { force: true }));
      return;
    }
    if (act) Store.d.sessions = Store.d.sessions.filter((s) => s !== act);
    const ids = (opts.shuffle === false ? qs : shuffle(qs)).map((q) => q.id);
    const s = { id: uid(), mode, created: Date.now(), updated: Date.now(), qids: ids, idx: 0, resp: {}, sel: {}, strike: {}, qtime: {}, elapsed: 0,
      limit: mode === "timed" ? ids.length * (opts.perQ || 90) : null, done: false, temp: !!opts.temp };
    if (!s.temp) { Store.d.sessions.unshift(s); Store.d.sessions = Store.d.sessions.slice(0, 60); Store.save(); }
    openRunner(s, { idx: 0 });
  }
  let pendingStart = null;
  function quickStart(mode) {
    let qs = pool("unused");
    if (!qs.length) qs = pool("all");
    startSession(mode, qs.slice(0, 40), { perQ: 90 });
  }

  /* ---------------- runner ---------------- */
  const R = { s: null, idx: 0, review: false, results: false, tick: null, lastSave: 0 };
  function openRunner(s, o = {}) {
    R.s = s; R.idx = o.idx != null ? o.idx : s.idx || 0; R.review = !!o.review; R.results = !!o.results;
    const el = $("#runner"); el.hidden = false; document.body.style.overflow = "hidden";
    renderRunner(); startTick();
  }
  function closeRunner() {
    stopTick();
    if (R.s && !R.s.temp && !R.s.done) { R.s.idx = R.idx; R.s.updated = Date.now(); }
    Store.save();
    $("#runner").hidden = true; $("#runner").innerHTML = ""; document.body.style.overflow = "";
    R.s = null; render();
  }
  function startTick() {
    stopTick();
    R.tick = setInterval(() => {
      const s = R.s; if (!s || R.review || R.results || s.done || document.hidden) return;
      const id = s.qids[R.idx];
      if (s.mode === "tutor" && s.resp[id]) return;
      s.elapsed = (s.elapsed || 0) + 1;
      s.qtime[id] = (s.qtime[id] || 0) + 1;
      updateClock();
      if (s.mode === "timed" && s.limit && s.elapsed >= s.limit) { endTimed(true); return; }
      if (Date.now() - R.lastSave > 10000) { R.lastSave = Date.now(); Store.local(); }
    }, 1000);
  }
  function stopTick() { clearInterval(R.tick); R.tick = null; }
  function clockText() {
    const s = R.s, id = s.qids[R.idx];
    if (R.review) return s.qtime[id] ? `Time spent ${fmt(s.qtime[id])}` : "Review";
    if (s.mode === "timed") { const left = s.limit - s.elapsed; return { t: `${fmt(left)} left`, low: left <= 60 }; }
    return { t: fmt(s.qtime[id] || 0), low: false };
  }
  function updateClock() {
    const el = $("#rclock"); if (!el) return;
    const c = clockText();
    if (typeof c === "string") { el.textContent = c; el.classList.remove("low"); }
    else { el.textContent = c.t; el.classList.toggle("low", c.low); }
  }
  function revealed(id) { const s = R.s; return R.review || (s.mode === "tutor" && !!s.resp[id]); }
  function renderRunner() {
    const s = R.s, el = $("#runner");
    if (R.results) { el.innerHTML = resultsHTML(); $(".rbody", el).scrollTop = 0; return; }
    const id = s.qids[R.idx], q = QMAP[id], n = s.qids.length, rev = revealed(id);
    const chosen = rev ? (s.resp[id] ? s.resp[id].c : null) : s.sel[id] || null;
    const struck = s.strike[id] || [];
    const c = clockText();
    const ctext = typeof c === "string" ? c : c.t;
    let h = `<div class="rbar">
      <button class="iconbtn" data-act="r-exit" aria-label="${R.review ? "Close review" : "Pause and exit"}">${ICON.x}</button>
      <div class="pos"><b>Question ${R.idx + 1} of ${n}</b><span id="rclock" class="${typeof c !== "string" && c.low ? "low" : ""}">${ctext}</span></div>
      <button class="iconbtn" data-act="r-flag" aria-pressed="${isFlag(id)}" aria-label="Flag this question">${ICON.flag}</button>
      ${EXAM === "mcat" ? (q.section !== "cars" ? `<button class="iconbtn" data-act="r-ptable" aria-label="Periodic table">${ICON.table}</button>` : `<span style="width:44px"></span>`) : `<button class="iconbtn" data-act="r-labs" aria-label="Lab reference values">${ICON.labs}</button>`}
      <button class="iconbtn" data-act="r-more" aria-label="All questions and options">${ICON.more}</button></div>
      <div class="rbody"><div class="rcontent">
      <div class="qhead">${stars(q.difficulty)}${rev ? `<span>Question ${QNUM[id]} in the bank</span>` : ""}</div>
      <div class="vig">${q.vignette.map((p) => `<p>${p}</p>`).join("")}</div>`;
    if (q.labs.length) h += `<div class="labs"><table>${q.labs.map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join("")}</table></div>`;
    h += q.after_labs.map((p) => `<div class="vig"><p>${p}</p></div>`).join("");
    h += `<p class="stem">${q.stem}</p><div class="opts" role="radiogroup" aria-label="Answer choices">`;
    for (const L of Object.keys(q.options)) {
      let cls = "opt-row", res = "";
      if (rev) {
        if (L === q.answer) { cls += " is-correct"; res = L === chosen ? "Your answer" : "Correct"; }
        else if (L === chosen) { cls += " is-wrong"; res = "Your answer"; }
        else cls += " dim";
      } else {
        if (L === chosen) cls += " sel";
        if (struck.includes(L)) cls += " struck";
      }
      h += `<div class="${cls}"><button class="opt" data-act="pick" data-l="${L}" role="radio" aria-checked="${L === chosen}" ${rev ? "disabled" : ""}><span class="ol">${L}</span><span class="ot">${q.options[L]}</span>${res ? `<span class="res">${res}</span>` : ""}</button>${rev ? "" : `<button class="strike" data-act="strike" data-l="${L}" aria-pressed="${struck.includes(L)}" aria-label="Cross out choice ${L}">${ICON.strike}</button>`}</div>`;
    }
    h += `</div>`;
    if (!rev) h += `<p class="hint" style="margin-top:12px">Tip: press and hold a choice, or use its strike button, to cross it out.</p>`;
    if (rev) h += explanationHTML(q, chosen);
    h += `</div></div>`;
    // footer
    let main = "";
    if (R.review) main = R.idx < n - 1 ? `<button class="btn main" data-act="r-next">Next question</button>` : (s.temp ? `<button class="btn main" data-act="r-exit">Done</button>` : `<button class="btn main" data-act="r-results">Back to results</button>`);
    else if (s.mode === "tutor") main = !s.resp[id] ? `<button class="btn main" data-act="r-submit" ${chosen ? "" : "disabled"}>Submit answer</button>` : R.idx < n - 1 ? `<button class="btn main" data-act="r-next">Next question</button>` : s.temp ? `<button class="btn main" data-act="r-exit">Done</button>` : `<button class="btn main" data-act="r-finish">See results</button>`;
    else main = R.idx < n - 1 ? `<button class="btn main" data-act="r-next">Next</button>` : `<button class="btn main" data-act="r-end">End block</button>`;
    h += `<div class="rfoot"><div class="in"><button class="navbtn" data-act="r-prev" aria-label="Previous question" ${R.idx === 0 ? "disabled" : ""}>${ICON.left}</button>${main}<button class="navbtn" data-act="r-next" aria-label="Next question" ${R.idx >= n - 1 ? "disabled" : ""}>${ICON.right}</button></div></div>`;
    el.innerHTML = h;
  }
  function explanationHTML(q, chosen) {
    const id = q.id, s = R.s;
    const t = s.qtime[id] ? fmt(s.qtime[id]) : null;
    let v;
    if (!chosen) v = `<div class="verdict skip" id="verdict"><div><b>Not answered</b><span>The correct answer is ${q.answer}.${t ? ` Time spent ${t}.` : ""}</span></div></div>`;
    else if (chosen === q.answer) v = `<div class="verdict ok" id="verdict">${ICON.check}<div><b>Correct</b><span>You chose ${chosen}.${t ? ` Time spent ${t}.` : ""}</span></div></div>`;
    else v = `<div class="verdict bad" id="verdict">${ICON.x}<div><b>Incorrect</b><span>You chose ${chosen}; the answer is ${q.answer}.${t ? ` Time spent ${t}.` : ""}</span></div></div>`;
    const note = (Store.d.notes[id] && Store.d.notes[id].text) || "";
    return v + `<div class="exp"><h3>Why ${q.answer} is correct</h3>${q.why_correct.map((p) => `<p>${p}</p>`).join("")}
      <h3>Why the other choices are wrong</h3><ul class="why">${Object.keys(q.why_wrong).sort().map((L) => `<li class="${L === chosen ? "picked" : ""}"><div class="h"><span>${L}. ${q.options[L]}</span>${L === chosen ? '<span class="tag">Your answer</span>' : ""}</div><p>${q.why_wrong[L]}</p></li>`).join("")}</ul>
      <div class="objective"><h4>${EXAM === "mcat" ? "Takeaway" : "Educational objective"}</h4><p>${q.objective}</p></div>
      <div class="notes"><label for="note-${id}">My notes</label><textarea id="note-${id}" data-note="${id}" placeholder="Anything you want to remember about this one">${esc(note)}</textarea></div>
      <details class="src"><summary>Sources</summary><ul>${q.sources.map((x) => `<li>${x}</li>`).join("")}</ul></details>
      <div class="tagline"><span class="badge">${esc(q.sys)}</span><span class="badge">${esc(q.discipline)}</span>${EXAM === "mcat" ? `<span class="badge">${esc(q.category)}</span><span class="badge">Skill ${esc(q.skill)}</span>${(q.topics || []).map((t) => `<button class="badge" data-act="g-go" data-sec="${esc(q.section)}" data-id="${esc(t)}" style="border:0;cursor:pointer">Guide: ${esc(t)}</button>`).join("")}` : ""}</div></div>`;
  }
  function resultsHTML() {
    const s = R.s, sc = sessionScore(s);
    const answered = s.qids.filter((id) => s.resp[id]).length;
    const missed = s.qids.filter((id) => s.resp[id] && !s.resp[id].ok);
    const skipped = s.qids.length - answered;
    const avg = answered ? (s.elapsed || 0) / Math.max(1, s.qids.length) : 0;
    let h = `<div class="rbar"><button class="iconbtn" data-act="r-exit" aria-label="Close">${ICON.x}</button><div class="pos"><b>Block results</b><span>${s.mode === "tutor" ? "Tutor" : "Timed"} block</span></div><span style="width:44px"></span></div>
      <div class="rbody"><div class="rcontent"><div class="results-hero"><div class="big">${sc.pct}%</div><p class="status-line" style="margin-top:8px">${sc.ok} of ${sc.total} correct${skipped ? `, ${skipped} not answered` : ""}. ${fmt(s.elapsed || 0)} total, about ${fmt(avg)} per question.</p></div>
      <div class="row wrap" style="margin:6px 0 18px"><button class="btn" data-act="r-review-all">Review all answers</button>${missed.length ? `<button class="btn ghost" data-act="r-redo-missed">Redo the ${missed.length} I missed</button>` : ""}</div>
      <div class="list">${s.qids.map((id, i) => {
        const r = s.resp[id], q = QMAP[id];
        const b = !r ? '<span class="badge">Skipped</span>' : r.ok ? '<span class="badge correct">Correct</span>' : '<span class="badge incorrect">Incorrect</span>';
        return `<button class="li" data-act="r-goto-review" data-i="${i}"><div class="t"><b>${i + 1}. ${esc(q.topic)}</b><span>${esc(q.sys)}${s.qtime[id] ? `, ${fmt(s.qtime[id])}` : ""}</span></div>${b}${ICON.right}</button>`;
      }).join("")}</div></div></div>
      <div class="rfoot"><div class="in"><button class="btn main" data-act="r-exit">Done</button></div></div>`;
    return h;
  }
  function moveTo(i) {
    const s = R.s; if (i < 0 || i >= s.qids.length) return;
    R.idx = i; if (!R.review && !s.done) { s.idx = i; s.updated = Date.now(); Store.local(); }
    renderRunner(); const b = $(".rbody"); if (b) b.scrollTop = 0;
  }
  function pick(L) {
    const s = R.s, id = s.qids[R.idx];
    if (revealed(id)) return;
    s.sel[id] = L; if (s.strike[id]) s.strike[id] = s.strike[id].filter((x) => x !== L);
    s.updated = Date.now(); Store.local(); renderRunnerKeepScroll();
  }
  function strike(L) {
    const s = R.s, id = s.qids[R.idx]; if (revealed(id)) return;
    const arr = s.strike[id] || (s.strike[id] = []);
    const i = arr.indexOf(L);
    if (i >= 0) arr.splice(i, 1); else { arr.push(L); if (s.sel[id] === L) delete s.sel[id]; }
    Store.local(); renderRunnerKeepScroll();
  }
  function renderRunnerKeepScroll() { const b = $(".rbody"); const y = b ? b.scrollTop : 0; renderRunner(); const nb = $(".rbody"); if (nb) nb.scrollTop = y; }
  function submit() {
    const s = R.s, id = s.qids[R.idx], c = s.sel[id]; if (!c || s.resp[id]) return;
    const ok = record(id, c, s.qtime[id] || 0);
    s.resp[id] = { c, ok }; s.updated = Date.now(); Store.save();
    renderRunnerKeepScroll();
    const v = $("#verdict"); if (v) v.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
  }
  function finishTutor() {
    const s = R.s; s.done = true; s.finished = Date.now(); s.updated = Date.now(); Store.save();
    R.results = true; R.review = false; renderRunner();
  }
  function endTimed(auto) {
    const s = R.s;
    s.qids.forEach((id) => { const c = s.sel[id]; if (c) { const ok = record(id, c, s.qtime[id] || 0); s.resp[id] = { c, ok }; } });
    s.done = true; s.finished = Date.now(); s.updated = Date.now(); Store.save();
    closeSheet(true);
    R.results = true; R.review = false; renderRunner();
    if (auto) toast("Time's up. Here's how you did.");
  }
  function confirmEnd() {
    const s = R.s, unanswered = s.qids.filter((id) => !s.sel[id]).length;
    openSheet("End this block?", `<p>${unanswered ? `${unanswered} question${unanswered > 1 ? "s are" : " is"} still unanswered and will count as incorrect.` : "All questions answered."} You'll see your score and every explanation next.</p>
      <div class="row wrap" style="margin-top:16px"><button class="btn ghost" data-act="sheet-close" data-autofocus>Keep going</button><button class="btn" data-act="r-end-confirm">End block</button></div>`);
  }
  function openNavigator() {
    const s = R.s;
    const cells = s.qids.map((id, i) => {
      let cls = "";
      if (R.review || (s.mode === "tutor" && s.resp[id])) cls = s.resp[id] ? (s.resp[id].ok ? "correct" : "incorrect") : "";
      else if (s.sel[id]) cls = "ans";
      return `<button class="${cls} ${i === R.idx ? "cur" : ""} ${isFlag(id) ? "flagged" : ""}" data-act="r-goto" data-i="${i}" aria-label="Question ${i + 1}">${i + 1}</button>`;
    }).join("");
    const f = Store.settings().font;
    openSheet("Questions in this block", `<div class="navgrid">${cells}</div>
      <div class="field"><span class="lab">Question text size</span><div class="seg" role="group" aria-label="Question text size">${["Small", "Medium", "Large"].map((n, i) => `<button data-act="set-font" data-v="${i}" aria-pressed="${f === i}">${n}</button>`).join("")}</div></div>
      ${!R.review && s.mode === "timed" && !s.done ? `<button class="btn ghost block" style="margin-top:18px" data-act="r-end">End block now</button>` : ""}
      ${!R.review && !s.done && !s.temp ? `<button class="btn quiet block" style="margin-top:6px" data-act="r-exit">Pause and exit</button>` : ""}`);
  }
  function openLabs() {
    openSheet("Lab reference values", `<input class="search" type="search" placeholder="Search labs" aria-label="Search labs" data-labsearch data-autofocus>
      <div class="labsheet" id="labsheet">${labsHTML("")}</div>
      <p class="hint" style="margin-top:12px">Typical adult reference ranges, close to those provided on the exam. Exact ranges vary by laboratory.</p>`);
  }
  function labsHTML(qs) {
    const q = qs.trim().toLowerCase();
    return LABS.map((g) => {
      const rows = g.rows.filter(([k]) => !q || k.toLowerCase().includes(q) || g.g.toLowerCase().includes(q));
      return rows.length ? `<h3>${g.g}</h3><table>${rows.map(([k, v]) => `<tr><td>${k}</td><td>${v}</td></tr>`).join("")}</table>` : "";
    }).join("") || `<p class="muted" style="margin-top:12px">No lab matches that search.</p>`;
  }
  function openQuestion(id) {
    const a = A(id);
    if (!a) { startSession("tutor", [QMAP[id]], { temp: true, shuffle: false }); return; }
    openSheet(`Question ${QNUM[id]}`, `<p>You answered this ${a.n > 1 ? `${a.n} times` : "once"}; last time you were ${a.ok ? "correct" : "incorrect"}.</p>
      <div class="row wrap" style="margin-top:14px"><button class="btn" data-act="read-exp" data-id="${id}" data-autofocus>Read the explanation</button><button class="btn ghost" data-act="try-again" data-id="${id}">Try it again</button></div>`);
  }
  function readExplanation(id) {
    const a = A(id); if (!a) { openQuestion(id); return; }
    const s = { id: uid(), mode: "tutor", temp: true, done: true, qids: [id], resp: { [id]: { c: a.c, ok: a.ok } }, sel: {}, strike: {}, qtime: { [id]: a.t || 0 }, elapsed: 0, idx: 0 };
    openRunner(s, { review: true, idx: 0 });
  }

  /* ---------------- events ---------------- */
  let suppressClick = false, lpTimer = null;
  document.addEventListener("pointerdown", (e) => {
    suppressClick = false;
    const o = e.target.closest && e.target.closest(".opt");
    if (!o || o.disabled) return;
    clearTimeout(lpTimer);
    lpTimer = setTimeout(() => { suppressClick = true; strike(o.dataset.l); if (navigator.vibrate) navigator.vibrate(15); }, 480);
  });
  ["pointerup", "pointercancel", "pointerleave"].forEach((ev) => document.addEventListener(ev, () => clearTimeout(lpTimer), true));
  document.addEventListener("contextmenu", (e) => { if (e.target.closest && e.target.closest(".opt")) e.preventDefault(); });

  document.addEventListener("click", (e) => {
    const t = e.target.closest("[data-act]"); if (!t) return;
    if (suppressClick && t.dataset.act === "pick") { suppressClick = false; return; }
    suppressClick = false;
    const act = t.dataset.act, v = t.dataset.v;
    switch (act) {
      case "tab": if (t.dataset.tab === "practice" && UI.tab === "practice") UI.msec = null; go(t.dataset.tab); break;
      case "msec": UI.msec = v || null; if (v) { UI.tab = "practice"; const g = guideOf(v); UI.mtab = g && !(Bank.mcat.items || []).some((q) => q.section === v) ? "guide" : UI.mtab; } G.q = ""; render(); window.scrollTo(0, 0); break;
      case "mtab": UI.mtab = v; render(); break;
      case "g-go": if (R.s) { closeSheet(true); closeRunner(); } openTopic(t.dataset.sec, t.dataset.id); break;
      case "g-practice": startSession("tutor", topicItems(t.dataset.id), { perQ: MCAT_PERQ[UI.msec] || 96 }); break;
      case "msec-start": { const qs = QB.filter((q) => q.section === UI.msec && (t.dataset.pool === "incorrect" ? lastStatus(q.id) === "incorrect" : true)); const fresh_ = qs.filter((q) => !A(q.id)); startSession(t.dataset.mode, (t.dataset.pool || fresh_.length === 0) ? qs : fresh_, { perQ: MCAT_PERQ[UI.msec] || 96 }); break; }
      case "ptab-go": UI.msec = null; UI.ptab = v; render(); window.scrollTo(0, 0); break;
      case "p-section": if (P.sections.has(v)) P.sections.delete(v); else P.sections.add(v); render(); break;
      case "p-skill": if (P.skills.has(v)) P.skills.delete(v); else P.skills.add(v); render(); break;
      case "r-ptable": openPTable(); break;
      case "pt-pick": { const e = PTABLE.find((x) => String(x[0]) === t.dataset.z); if (e) { const inp = $("[data-ptsearch]"); if (inp) inp.value = e[1]; ptFind(e[1]); } break; }
      case "settings": openSettings(); break;
      case "sheet-close": closeSheet(); break;
      case "set-theme": Store.settings().theme = v; applySettings(); Store.saveSettings(); $$("[data-act=set-theme]").forEach((b) => b.setAttribute("aria-pressed", b.dataset.v === v)); break;
      case "set-font": Store.settings().font = +v; applySettings(); Store.saveSettings(); $$("[data-act=set-font]").forEach((b) => b.setAttribute("aria-pressed", b.dataset.v === v)); break;
      case "exam": setExam(v); break;
      case "boot-retry": boot(); break;
      case "reset": confirmReset(); break;
      case "reset-confirm": { const st = Store.d.settings; Store.d = fresh(); Store.d.settings = st; try { localStorage.removeItem(EXAMS[EXAM].key); } catch (e) { /* ignore */ } Store.save(); closeSheet(true); render(); toast("Progress reset."); break; }
      case "quick": quickStart(t.dataset.mode); break;
      case "start-pool": startSession("tutor", pool(t.dataset.pool), {}); break;
      case "resume": { closeSheet(true); const s = activeSession(); if (s) openRunner(s, { idx: s.idx }); break; }
      case "force-start": closeSheet(true); if (pendingStart) { const f = pendingStart; pendingStart = null; f(); } break;
      case "discard": { const s = activeSession(); if (s) { Store.d.sessions = Store.d.sessions.filter((x) => x !== s); Store.save(); render(); toast("Block discarded."); } break; }
      case "ptab": UI.ptab = v; render(); break;
      case "p-mode": P.mode = v; render(); break;
      case "p-pool": P.pool = v; render(); break;
      case "p-sys": if (P.systems.has(v)) P.systems.delete(v); else P.systems.add(v); render(); break;
      case "p-diff": { const d = +v; if (P.diffs.has(d)) P.diffs.delete(d); else P.diffs.add(d); render(); break; }
      case "p-count": { const av = available().length; P.count = Math.max(1, Math.min(Math.max(av, 1), Math.min(P.count, av || 1) + +v)); render(); break; }
      case "p-perq": P.perQ = +v; render(); break;
      case "p-shuffle": P.shuffle = !P.shuffle; render(); break;
      case "start-custom": { const av = available(); const qs = (P.shuffle ? shuffle(av) : av).slice(0, Math.min(P.count, av.length)); startSession(P.mode, qs, { perQ: P.perQ, shuffle: false }); break; }
      case "missed-only": UI.missedOnly = !UI.missedOnly; render(); break;
      case "q-open": openQuestion(t.dataset.id); break;
      case "read-exp": closeSheet(true); readExplanation(t.dataset.id); break;
      case "try-again": closeSheet(true); startSession("tutor", [QMAP[t.dataset.id]], { temp: true, shuffle: false }); break;
      case "hist-open": { const s = Store.d.sessions.find((x) => x.id === t.dataset.sid); if (s) openRunner(s, { results: true }); break; }
      // runner
      case "r-exit": closeSheet(true); closeRunner(); break;
      case "r-flag": { const id = R.s.qids[R.idx]; Store.d.flags[id] = { on: !isFlag(id), ts: Date.now() }; Store.save(); t.setAttribute("aria-pressed", isFlag(id)); toast(isFlag(id) ? "Flagged for review." : "Flag removed."); break; }
      case "r-labs": openLabs(); break;
      case "r-more": openNavigator(); break;
      case "r-prev": moveTo(R.idx - 1); break;
      case "r-next": moveTo(R.idx + 1); break;
      case "r-goto": closeSheet(true); moveTo(+t.dataset.i); break;
      case "pick": pick(t.dataset.l); break;
      case "strike": strike(t.dataset.l); break;
      case "r-submit": submit(); break;
      case "r-finish": finishTutor(); break;
      case "r-end": closeSheet(true); confirmEnd(); break;
      case "r-end-confirm": endTimed(false); break;
      case "r-results": R.results = true; R.review = false; renderRunner(); break;
      case "r-review-all": R.results = false; R.review = true; R.idx = 0; renderRunner(); break;
      case "r-goto-review": R.results = false; R.review = true; R.idx = +t.dataset.i; renderRunner(); $(".rbody").scrollTop = 0; break;
      case "r-redo-missed": { const ids = R.s.qids.filter((id) => R.s.resp[id] && !R.s.resp[id].ok); closeRunner(); startSession("tutor", ids.map((id) => QMAP[id]), {}); break; }
      default: Anat.handle(act, t, v);
    }
  });
  document.addEventListener("input", (e) => {
    const t = e.target;
    if (t.dataset.note) { const id = t.dataset.note; Store.d.notes[id] = { text: t.value, ts: Date.now() }; clearTimeout(t._nt); t._nt = setTimeout(() => Store.save(), 700); Store.local(); }
    else if (t.hasAttribute("data-labsearch")) { $("#labsheet").innerHTML = labsHTML(t.value); }
    else if (t.hasAttribute("data-gsearch")) { G.q = t.value; refreshGuideBody(); }
    else if (t.hasAttribute("data-ptsearch")) { ptFind(t.value); }
    else Anat.input(t);
  });
  document.addEventListener("change", (e) => { const t = e.target; if (t.dataset && t.dataset.reviewed) setReviewed(t.dataset.reviewed, t.checked); });
  document.addEventListener("toggle", (e) => { const d = e.target; if (d && d.dataset && d.dataset.okey) { G.open[d.dataset.okey] = d.open; saveGuideUI(); } }, true);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && $("#sheetroot").firstChild) { closeSheet(); return; }
    if ($("#runner").hidden || !R.s || R.results) return;
    if (e.target.matches("textarea, input")) return;
    if ($("#sheetroot").firstChild) return;
    const k = e.key.toUpperCase(), q = QMAP[R.s.qids[R.idx]];
    if (q && q.options[k] && !e.metaKey && !e.ctrlKey) { pick(k); e.preventDefault(); }
    else if (e.key === "ArrowRight") moveTo(R.idx + 1);
    else if (e.key === "ArrowLeft") moveTo(R.idx - 1);
    else if (k === "F") $("[data-act=r-flag]")?.click();
    else if (e.key === "Enter" && !e.target.closest("button")) { const m = $(".rfoot .btn.main"); if (m && !m.disabled) { m.click(); e.preventDefault(); } }
  });
  document.addEventListener("click", (e) => { if (!e.target.closest(".search-wrap")) { const b = $("#bresults"); if (b) b.innerHTML = ""; } }, true);
  window.addEventListener("pagehide", () => Store.local());
  document.addEventListener("visibilitychange", () => { if (document.hidden) { if (R.s && !R.s.temp && !R.s.done) { R.s.updated = Date.now(); } Store.save(); } });

  /* ---------------- boot ---------------- */
  function preApplySettings() {   // theme and text size straight from storage, before the banks arrive, so nothing flashes
    try { const d = JSON.parse(localStorage.getItem(EXAMS.boards.key) || "null"); if (d && d.settings) applyTheme(Object.assign(fresh().settings, d.settings)); } catch (e) { /* ignore */ }
  }
  async function fetchBank(file) {
    const v = typeof ASSET_V === "object" && ASSET_V[file] ? `?v=${ASSET_V[file]}` : "";
    const r = await fetch(file + v); if (!r.ok) throw new Error(`${file}: ${r.status}`);
    return r.json();
  }
  async function boot() {
    ready = false; render();
    try {
      const [boards, mcat] = await Promise.all([fetchBank("data/boards.json"), fetchBank("data/mcat.json")]);
      Bank.boards = boards; Bank.mcat = mcat;
    } catch (e) {
      console.error(e);
      if (UI.tab !== "anatomy") $("#view").innerHTML = `<div class="boot"><p>The questions could not be loaded. Check the connection and try again.</p><button class="btn" data-act="boot-retry">Try again</button></div>`;
      return;
    }
    MAPS.boards = Object.fromEntries(Bank.boards.map((q) => [q.id, q]));
    /* MCAT items (docs/MCAT_SPEC.md §8) are given the few fields the shared runner and lists expect from a boards question. */
    (Bank.mcat.items || []).forEach((q) => { q.sys = (Bank.mcat.categories || {})[q.category] || q.category; q.objective = q.takeaway; q.topic = q.sys; q.vignette = q.vignette || []; q.labs = []; q.after_labs = []; });
    MAPS.mcat = Object.fromEntries((Bank.mcat.items || []).map((q) => [q.id, q]));
    let exam = "boards"; try { if (localStorage.getItem(EXAM_KEY) === "mcat") exam = "mcat"; } catch (e) { /* ignore */ }
    activate(exam); if (exam === "mcat") UI.ptab = "sections";
    Store.load();
    applySettings();
    ready = true; document.body.dataset.ready = "1";
    render();
    Sync.init();
  }
  preApplySettings();
  Anat.init({ render, go, tab: () => UI.tab, toast, openSheet, sheetBody, closeSheet });
  boot();
})();
