/* Director runtime: builds an explainer edit (speaker footage + motion graphics) as DOM and one paused
   GSAP timeline, for HyperFrames to seek frame by frame. Every visible change is a tween on that
   timeline, so any frame renders on its own (no timers, no wall clock, seeded randomness only).

   The plan (plan.js) calls the helpers below. Times are seconds on the OUTPUT timeline; D.at() turns a
   spoken phrase into the output time of its first word, using the word timings of the cut.

   Motion is physics springs (closed-form, a pure function of time). Their constants are measured: an
   Apple UI morph (refs/apple_timer.mp4) grows, overshoots its size by about 7 % and settles in about
   0.4 s with one small second bounce, which is a spring with damping near 0.68. Camera and layout moves
   use critically damped springs so nothing snaps. Scenes never pop in or out on their own: a new scene
   pushes in while the old one leaves the same way and the ground pans with them (refs/explainer.mp4:
   a picture change about every 1.2 s, motion inside every shot). */
(function () {
  const W = 1920, H = 1080;
  const D = (window.D = {});
  const tl = (D.tl = gsap.timeline({ paused: true }));
  const root = document.getElementById("stage");
  const CFG = (D.cfg = window.EDIT_CONFIG);

  // ---------- seeded randomness
  let seed = 1234567;
  D.rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);

  // ---------- springs: ease functions of progress p in [0,1] over the settle time of the spring
  /** {ease, dur}: damping ratio z (1 = no bounce), response = period in seconds (smaller = faster) */
  D.spring = (z = 0.82, response = 0.5) => {
    const w = (2 * Math.PI) / response;
    const dur = Math.min(2.2, Math.log(400) / (Math.min(z, 1) * w));
    let f;
    if (z < 1) { const wd = w * Math.sqrt(1 - z * z); f = (t) => 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + ((z * w) / wd) * Math.sin(wd * t)); }
    else f = (t) => 1 - (1 + w * t) * Math.exp(-w * t);
    const end = f(dur);
    return { ease: (p) => (p >= 1 ? 1 : f(p * dur) / end), dur };
  };
  const SP = (D.SP = {
    ui: D.spring(0.86, 0.42),      // cards, rows, labels arriving
    apple: D.spring(0.68, 0.55),   // measured: morphs and pops, ~7 % overshoot
    smooth: D.spring(1.0, 0.62),   // camera, pages, the world: no bounce
    layout: D.spring(0.92, 0.8),   // the speaker window changing shape
    text: D.spring(1.0, 0.45),     // words settling
  });
  const S_ = (name, extra = {}) => ({ ease: SP[name].ease, duration: SP[name].dur, ...extra });

  // ---------- word timing
  const norm = (s) => s.toLowerCase().replace(/[’']/g, "").replace(/[^a-z0-9.]+/g, " ").replace(/\.(?!\d)/g, " ").trim();
  const NUMW = { zero: "0", one: "1", two: "2", three: "3", four: "4", five: "5", six: "6", seven: "7", eight: "8", nine: "9", ten: "10", eleven: "11", twelve: "12", thirteen: "13", fourteen: "14", fifteen: "15", twenty: "20" };
  // speech recognition hears names as common words; map both sides to one spelling
  const SYN = { cloud: "claude", clouds: "claudes", sword: "short", swords: "shorts", sort: "short", sorts: "shorts", gonna: "going" };
  const tok = (s) => norm(s).split(" ").filter(Boolean).map((w) => SYN[w] || NUMW[w] || w);
  const WORDS = (window.EDIT_WORDS || []).map((w) => ({ ...w, n: tok(w.w)[0] || "" }));
  D.out = (t) => (CFG.insert && t >= CFG.insert.at ? t + CFG.insert.dur : t); // cut time -> output time
  D.cutT = (t) => (!CFG.insert ? t : t >= CFG.insert.at + CFG.insert.dur ? t - CFG.insert.dur : t >= CFG.insert.at ? CFG.insert.at : t);
  // Searches start from the current scene unless a start is given: a common phrase ("credits", "the
  // characters") is usually said earlier too, and the earlier one is never the one meant.
  D._cursor = 0;
  D.atLog = [];
  const find = (q, f0) => {
    for (let i = 0; i < WORDS.length; i++) {
      if (WORDS[i].start < f0 - 0.05) continue;
      let ok = true;
      for (let k = 0; k < q.length; k++) {
        const w = WORDS[i + k];
        if (!w) { ok = false; break; }
        const a = w.n, b = q[k];
        // exact, or the same word with a different ending (5 shared letters: "measure"/"measured", not "think"/"things")
        if (!(a === b || (a.length > 4 && b.length > 4 && (a.startsWith(b.slice(0, 5)) || b.startsWith(a.slice(0, 5)))))) { ok = false; break; }
      }
      if (ok) return i;
    }
    return null;
  };
  /** output time of the first word of `phrase`, searching from `from` (default: the current scene) */
  D.at = (phrase, from, opts = {}) => {
    const q = tok(phrase);
    const f = from == null ? D._cursor : from;
    const best = find(q, D.cutT(f));
    if (best === null) { console.warn("D.at: not found:", phrase, "from", f); D.missing = (D.missing || []).concat([phrase]); return opts.fallback ?? f; }
    const r = D.out(opts.end ? WORDS[best + q.length - 1].end : WORDS[best + (opts.word || 0)].start);
    if (from == null) { const b0 = find(q, 0); if (b0 !== best) D.atLog.push({ phrase, first: +D.out(WORDS[b0].start).toFixed(2), used: +r.toFixed(2) }); }
    return r;
  };
  D.end = (phrase, from) => D.at(phrase, from, { end: true });

  // ---------- DOM helpers
  const h = (D.h = (tag, cls, style, html, parent) => {
    const e = document.createElement(tag);
    if (cls) e.className = cls;
    if (style) for (const k in style) { if (k.startsWith("--")) e.style.setProperty(k, style[k]); else e.style[k] = style[k]; }   // CSS variables need setProperty
    if (html != null) e.innerHTML = html;
    (parent || root).appendChild(e);
    return e;
  });
  D.icon = (name, size = 48, color = "currentColor", sw = 1.6) => {
    const d = (window.ICONS || {})[name];
    if (!d) { console.warn("icon missing", name); return ""; }
    return `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" style="color:${color};display:block;flex:none" stroke-width="${sw}">${d.replace(/stroke-width="[^"]*"/g, `stroke-width="${sw}"`)}</svg>`;
  };
  const px = (v) => (typeof v === "number" ? v + "px" : v);

  // show an element only inside [t0, t1): display toggled by the timeline (elements are not .clip)
  D.life = (el, t0, t1) => {
    tl.set(el, { display: "none" }, 0);
    tl.set(el, { display: "" }, Math.max(0, t0));
    if (t1 != null) tl.set(el, { display: "none" }, t1);
  };

  // ---------- motion vocabulary
  const M = (D.M = {
    // a card: fades up from a soft blur while a spring brings its size and position home
    cardIn: (el, t, o = {}) => {
      tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.22, ease: "power1.out" }, t);
      tl.fromTo(el, { filter: "blur(14px)" }, { filter: "blur(0px)", duration: 0.38, ease: "power2.out" }, t);
      tl.fromTo(el, { scale: o.from ?? 0.92 }, S_("apple", { scale: 1 }), t);
      tl.fromTo(el, { y: o.y ?? 34, x: o.x ?? 0 }, S_("ui", { y: 0, x: 0 }), t);
    },
    cardOut: (el, t, o = {}) => tl.to(el, { opacity: 0, scale: o.to ?? 0.96, filter: "blur(10px)", y: o.y ?? -12, duration: o.dur ?? 0.3, ease: "power2.in" }, t),
    // a word resolves from blur and settles from a little below, on a no-bounce spring
    wordIn: (el, t) => {
      tl.fromTo(el, { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.28, ease: "power2.out" }, t);
      tl.fromTo(el, { y: "0.32em" }, S_("text", { y: 0 }), t);
    },
    // something small arriving with a measured Apple overshoot (never from a dot)
    pop: (el, t) => {
      tl.fromTo(el, { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2, ease: "power1.out" }, t);
      tl.fromTo(el, { scale: 0.55 }, S_("apple", { scale: 1 }), t);
    },
    fade: (el, t, d = 0.3) => tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: d, ease: "power2.out" }, t),
    out: (el, t, d = 0.26) => tl.to(el, { opacity: 0, filter: "blur(8px)", duration: d, ease: "power2.in" }, t),
  });

  // ---------- canvas: warm linen, a dot grid that is the "world": it drifts, and pans on every scene change
  const bg = h("div", "bg", {});
  const world = h("div", "world", {}, null, bg);
  const dots = h("div", "dots", {}, null, world);
  tl.fromTo(dots, { x: 0, y: 0 }, { x: -64, y: -40, duration: CFG.total, ease: "none" }, 0);
  let worldX = 0;
  const panWorld = (t, dx) => { worldX = ((worldX + dx) % 320 + 320) % 320 - 320; tl.to(world, S_("smooth", { x: worldX }), t); };

  // ---------- layers
  const L = (D.layers = {
    back: h("div", "layer", { zIndex: 1 }),
    spk: h("div", "layer", { zIndex: 5 }),
    mid: h("div", "layer", { zIndex: 6 }),
    front: h("div", "layer", { zIndex: 8 }),
    hud: h("div", "layer", { zIndex: 9 }),
  });

  // ---------- the speaker: one clip-path window over the footage, a camera inside it
  const spkShadow = h("div", "spkshadow", {}, null, L.spk);
  const spkWin = h("div", "spkwin", {}, null, L.spk);
  const spkCam = h("div", "spkcam", {}, null, spkWin);
  const spkShake = h("div", "spkshake", { position: "absolute", inset: "0" }, null, spkCam);
  const spkDrift = h("div", "spkdrift", {}, null, spkShake);
  for (const v of document.querySelectorAll("video.speaker")) spkDrift.appendChild(v);
  const _gid = document.getElementById.bind(document);
  document.getElementById = (id) => _gid(id) || document.createElement("div");
  const spkFlash = h("div", "spkflash", {}, null, spkWin);

  const GOLD = 0.618, M_ = 72;
  const RECTS = (D.RECTS = {
    full: { x: 0, y: 0, w: W, h: H, r: 0 },
    right: { x: W * GOLD + 24, y: M_, w: W * (1 - GOLD) - 24 - M_, h: H - 2 * M_, r: 34 },
    left: { x: M_, y: M_, w: W * (1 - GOLD) - 24 - M_, h: H - 2 * M_, r: 34 },
    halfR: { x: W / 2, y: 0, w: W / 2, h: H, r: 0 },
    halfL: { x: 0, y: 0, w: W / 2, h: H, r: 0 },
    pip: { x: W - 72 - 330, y: H - 72 - 440, w: 330, h: 440, r: 28 },
    pipL: { x: 72, y: H - 72 - 440, w: 330, h: 440, r: 28 },
    circle: { x: W - 72 - 250, y: H - 72 - 250, w: 250, h: 250, r: 125 },
    gone: { x: W - 72 - 330 + 165, y: H - 72 - 220, w: 0, h: 0, r: 28 },
    small: { x: W - 72 - 300, y: M_, w: 300, h: 380, r: 26 },
  });
  D.area = (layout) => ({
    full: { x: M_, y: M_, w: W - 2 * M_, h: H - 2 * M_ },
    none: { x: M_, y: M_, w: W - 2 * M_, h: H - 2 * M_ },
    gone: { x: M_, y: M_, w: W - 2 * M_, h: H - 2 * M_ },
    right: { x: M_, y: M_, w: W * GOLD - M_ - 24, h: H - 2 * M_ },
    left: { x: W * (1 - GOLD) + 24, y: M_, w: W * GOLD - M_ - 24, h: H - 2 * M_ },
    halfR: { x: M_, y: M_, w: W / 2 - 2 * M_, h: H - 2 * M_ },
    halfL: { x: W / 2 + M_, y: M_, w: W / 2 - 2 * M_, h: H - 2 * M_ },
    pip: { x: M_, y: M_, w: W - 2 * M_ - 330 - 40, h: H - 2 * M_ },
    pipL: { x: M_ + 330 + 40, y: M_, w: W - 2 * M_ - 330 - 40, h: H - 2 * M_ },
    circle: { x: M_, y: M_, w: W - 2 * M_, h: H - 2 * M_ },
    small: { x: M_, y: M_, w: W - 2 * M_ - 340, h: H - 2 * M_ },
  }[layout]);

  const faceAt = (t) => { const c = D.cutT(t); for (const s of CFG.setups) if (c >= s.from && c < s.to) return s; return CFG.setups[0]; };
  function camFor(rect, zoom, t) {
    const f = faceAt(t);
    const full = rect.w >= W - 1 && rect.h >= H - 1;
    let s;
    if (full) s = f.base * zoom;
    else { const cover = Math.max(rect.w / W, rect.h / H); s = Math.max(cover * 1.0001, f.card * zoom * Math.min(1, Math.max(0.62, rect.h / 936))); }
    // CFG.center: the speaker is centred in a full frame (face at x 0.5, y center_y), not left where the camera put them
    const fx = full ? (CFG.center ? 0.5 : f.cx) : 0.5, fy = full ? (CFG.center ? (CFG.center_y || 0.42) : f.cy) : (rect.h < 500 ? 0.42 : 0.36);
    const tx = rect.x + rect.w * fx, ty = rect.y + rect.h * fy;
    let x = tx - f.cx * W * s, y = ty - f.cy * H * s;
    x = Math.min(rect.x, Math.max(rect.x + rect.w - W * s, x));
    y = Math.min(rect.y, Math.max(rect.y + rect.h - H * s, y));
    return { x, y, scale: s };
  }
  D.camFor = camFor;
  D.cutouts = [];
  D.cutShakes = [];   // a cutout's own shake box, so a shake during a cutout moves the person and the footage together
  /** hide the framed speaker between t0 and t1 (a cutout of the person is shown instead) */
  D.spkHide = (t0, t1) => { tl.set(spkWin, { opacity: 0 }, t0); tl.set(spkShadow, { autoAlpha: 0 }, t0); tl.set(spkWin, { opacity: 1 }, t1); tl.set(spkShadow, { autoAlpha: 1 }, t1); };
  D.spkStyle = (t, css) => tl.set(spkShadow, css, t);
  D.spkEls = { win: spkWin, cam: spkCam, shadow: spkShadow };
  const clipOf = (r) => `inset(${r.y}px ${W - r.x - r.w}px ${H - r.y - r.h}px ${r.x}px round ${r.r}px)`;
  gsap.set(spkCam, { transformOrigin: "0 0" });

  let spkState = { layout: "full", zoom: 1, t: 0 };
  const spkKeys = (D.spkKeys = []);
  /** move the speaker to a layout at time t. dur 0 = cut (punch). Moves are a layout spring (no bounce). */
  D.speaker = (t, layout, o = {}) => {
    const r = typeof layout === "string" ? RECTS[layout] : layout;
    const zoom = o.zoom ?? 1;
    const cam = camFor(r, zoom, t);
    const props = { clipPath: clipOf(r) };
    const sh = { left: r.x, top: r.y, width: r.w, height: r.h, borderRadius: r.r, opacity: r.w >= W ? 0 : 1 };
    if (o.dur === 0) {
      tl.set(spkWin, props, t); tl.set(spkCam, cam, t); tl.set(spkShadow, sh, t);
    } else {
      const sp = o.ease ? { ease: o.ease, duration: o.dur ?? 0.6 } : S_(o.spring || "layout");
      tl.to(spkWin, { ...props, ...sp }, t);
      tl.to(spkCam, { ...cam, ...sp }, t);
      tl.to(spkShadow, { ...sh, ...sp }, t);
      if (layout !== spkState.layout) D.cue(t, r.w >= W ? "swell" : "swoosh_soft", -10, (r.x + r.w / 2) / W * 2 - 1);
    }
    spkKeys.push({ t, layout: typeof layout === "string" ? layout : "custom", zoom });
    spkState = { layout, zoom, t };
  };
  D.punch = (t, levels = 1) => {
    const z = Math.max(0.9, Math.min(1.25, spkState.zoom * Math.pow(1.047, levels)));
    D.speaker(t, spkState.layout, { zoom: z, dur: 0 });
    D.cue(t, "punch", -14);
  };
  D.ease = (t, levels = 2) => {
    const z = Math.max(0.9, Math.min(1.25, spkState.zoom * Math.pow(1.047, levels)));
    D.speaker(t, spkState.layout, { zoom: z, spring: "smooth" });
  };
  let driftSign = 1;
  D.drift = (t0, t1, rate = 0.006) => {
    const d = t1 - t0; if (d <= 0.05) return;
    const a = driftSign > 0 ? 1 : 1 + Math.min(0.05, rate * d), b = driftSign > 0 ? 1 + Math.min(0.05, rate * d) : 1;
    tl.fromTo(spkDrift, { scale: a }, { scale: b, duration: d, ease: "sine.inOut", immediateRender: false }, t0);
    driftSign *= -1;
  };
  gsap.set(spkDrift, { transformOrigin: "46% 32%" });
  /** camera shake: a short decaying wobble (seeded noise), on the speaker or on any element */
  D.shake = (t, amp = 7, dur = 0.42, el) => {
    const target = el || [spkShake, ...D.cutShakes.filter((c) => t >= c.t0 && t < c.t1).map((c) => c.el)], n = Math.max(4, Math.round(dur * 25)), kf = [];
    for (let i = 1; i <= n; i++) {
      const k = Math.pow(1 - i / n, 1.6);
      kf.push({ x: (D.rand() * 2 - 1) * amp * k, y: (D.rand() * 2 - 1) * amp * k, rotation: (D.rand() * 2 - 1) * 0.35 * k * (amp / 7), duration: dur / n, ease: "sine.inOut" });
    }
    kf.push({ x: 0, y: 0, rotation: 0, duration: 0.04 });
    tl.to(target, { keyframes: kf }, t);
    if (!el) D.cue(t, "shake", -16);
  };
  D.flash = (t) => tl.fromTo(spkFlash, { opacity: 0.0 }, { keyframes: [{ opacity: 0.35, duration: 0.04 }, { opacity: 0, duration: 0.2 }] }, t);

  // ---------- scenes: continuous push transitions
  let sceneN = 0;
  /** a graphic stage beside the current layout. It pushes in from the right while the world pans,
      and leaves to the left when it ends, so one scene hands over to the next in one motion. */
  D.scene = (t0, t1, area, o = {}) => {
    const a = typeof area === "string" ? D.area(area) : area;
    const el = h("div", "scene", { left: px(a.x), top: px(a.y), width: px(a.w), height: px(a.h) }, null, L[o.layer || "mid"]);
    const inner = el;
    D.life(el, t0 - 0.02, t1 + (o.tail ?? 0.45));
    const dir = o.dir ?? 1, dist = o.dist ?? 110;
    if (o.enter !== false) {
      tl.fromTo(el, { x: dist * dir }, S_("smooth", { x: 0 }), t0);
      tl.fromTo(el, { opacity: 0, filter: "blur(16px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.32, ease: "power2.out" }, t0);
      if (o.layer !== "front") panWorld(t0, -dist * dir);
      if (o.sound !== false) D.cue(t0 - 0.06, "swoosh", -12, 0.3 * dir);
    }
    if (o.out !== false) {
      tl.to(el, { x: -dist * 0.8 * dir, duration: 0.42, ease: "power2.in" }, t1);
      tl.to(el, { opacity: 0, filter: "blur(14px)", duration: 0.34, ease: "power2.in" }, t1 + 0.04);
    }
    if (o.drift !== false) tl.fromTo(el, { scale: 1 }, { scale: 1 + Math.min(0.03, 0.0035 * (t1 - t0)), duration: t1 - t0 + 0.3, ease: "none", immediateRender: false }, t0);
    el._a = a; el._t0 = t0; el._t1 = t1;
    D._cursor = Math.max(D._cursor, t0 - 1.5);
    sceneN++;
    return inner;
  };

  // ---------- components
  D.words = (parent, text, times, o = {}) => {
    const el = h("div", "words fitw " + (o.cls || ""), { fontSize: px(o.size || 76), color: o.color || "var(--ink)", fontWeight: o.weight || 650, textAlign: o.align || "left", lineHeight: o.lh || 1.06, letterSpacing: o.ls || "-0.035em", ...(o.style || {}) }, null, parent);
    const parts = text.split(" ");
    const accent = new Set((o.accent || []).map((s) => s.toLowerCase()));
    parts.forEach((p, i) => {
      if (p === "\\n") { h("br", null, null, null, el); return; }
      const s = h("span", "w" + (accent.has(norm(p)) ? " acc" : ""), {}, p + " ", el);
      const t = Array.isArray(times) ? times[Math.min(i, times.length - 1)] : times + i * (o.stagger ?? 0.06);
      M.wordIn(s, t);
    });
    return el;
  };
  D.card = (parent, x, y, w, hh, o = {}) => {
    const el = h("div", "card " + (o.cls || ""), { left: px(x), top: px(y), width: px(w), height: px(hh), ...(o.style || {}) }, o.html ?? null, parent);
    if (o.t != null) { M.cardIn(el, o.t, o); if (o.sound !== false) D.cue(o.t, "card", -16); }
    return el;
  };
  D.tile = (parent, x, y, icon, o = {}) => {
    const s = o.size || 120;
    const el = h("div", "tile " + (o.cls || ""), { left: px(x), top: px(y), width: px(s), height: px(s), background: o.bg || "var(--surface)", color: o.color || "var(--ink)" }, D.icon(icon, s * 0.46, o.color || "currentColor", o.sw || 1.6), parent);
    if (o.t != null) M.pop(el, o.t);
    return el;
  };
  D.pill = (parent, x, y, text, o = {}) => {
    const el = h("div", "pill " + (o.cls || ""), { left: px(x), top: px(y), fontSize: px(o.size || 32), ...(o.style || {}) }, (o.icon ? `<span class="pi">${D.icon(o.icon, (o.size || 32) * 1.05, "currentColor", 1.8)}</span>` : "") + `<span>${text}</span>`, parent);
    if (o.t != null) { (o.anim === "pop" ? M.pop : M.cardIn)(el, o.t, { from: 0.8 }); D.cue(o.t, o.anim === "pop" ? "pop" : "tick", -14); }
    return el;
  };
  /** a number that rolls up (fast, then slowing on a spring-like tail) */
  D.counter = (el, t, from, to, dur = 1.4, fmt = (v) => Math.round(v).toLocaleString("en-US")) => {
    const o = { v: from };
    el.textContent = fmt(from);
    tl.to(o, { v: to, duration: dur, ease: "expo.out", onUpdate: () => (el.textContent = fmt(o.v)) }, t);
    tl.set({}, { onUpdate: () => (el.textContent = fmt(o.v)) }, t + dur + 0.01);
    D.cue(t, "count", -14);
  };
  D.strike = (parent, t, o = {}) => {
    const el = h("div", "strike", { background: o.color || "var(--red)", top: o.top || "50%" }, null, parent);
    tl.fromTo(el, { scaleX: 0 }, S_("smooth", { scaleX: 1 }), t);
    D.cue(t, "strike", -14);
    return el;
  };
  D.drawPath = (svg, path, t, dur = 0.6, ease = "power2.inOut") => {
    const len = path.getTotalLength ? path.getTotalLength() : 1000;
    path.style.strokeDasharray = len; path.style.strokeDashoffset = len;
    tl.fromTo(path, { strokeDashoffset: len }, { strokeDashoffset: 0, duration: dur, ease }, t);
  };
  D.browser = (parent, x, y, w, hh, img, o = {}) => {
    const win = h("div", "browser " + (o.cls || ""), { left: px(x), top: px(y), width: px(w), height: px(hh) }, null, parent);
    h("div", "bbar", {}, `<i></i><i></i><i></i><span class="url">${D.icon("SquareLock02Icon", 18, "var(--ink2)")}<b>${o.url || ""}</b></span>`, win);
    const view = h("div", "bview", {}, null, win);
    const pg = h("div", "bpg", { width: px(w) }, null, view);
    const im = h("img", "bimg", { width: "100%" }, null, pg); im.src = img;
    gsap.set(pg, { transformOrigin: "0 0" });
    const br = { win, view, pg, w, vh: hh - 46, imgW: o.imgW || 3200 };
    if (o.t != null) { M.cardIn(win, o.t, { from: 0.94 }); D.cue(o.t, "card", -14); }
    return br;
  };
  /** move the page so image-pixel box b fills the view: a smooth camera spring, never linear */
  D.focus = (br, t, b, o = {}) => {
    const k = br.w / br.imgW;
    const s = Math.max(1, Math.min(o.max || 3.4, (o.fit || 0.86) * Math.min(br.w / (b.w * k), br.vh / (b.h * k))));
    const cx = (b.x + b.w / 2) * k, cy = (b.y + b.h / 2) * k;
    let x = br.w / 2 - cx * s, y = br.vh / 2 - cy * s;
    if (o.top) y = (o.topPad ?? 30) - b.y * k * s;
    x = Math.min(0, Math.max(br.w - br.w * s, x));
    const props = { x, y: Math.min(0, y), scale: s };
    if (o.dur === 0) tl.set(br.pg, props, t);
    else { tl.to(br.pg, { ...props, ...(o.ease ? { ease: o.ease, duration: o.dur || 0.9 } : S_("layout")) }, t); D.cue(t, "zoom", -16); }
    return props;
  };
  D.mark = (br, b, t, o = {}) => {
    const k = br.w / br.imgW;
    const el = h("div", "mark " + (o.cls || ""), { left: px(b.x * k - 8), top: px(b.y * k - 8), width: px(b.w * k + 16), height: px(b.h * k + 16) }, o.label ? `<span>${o.label}</span>` : "", br.pg);
    tl.set(el, { opacity: 0 }, 0);
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t);
    tl.fromTo(el, { scale: 1.08 }, S_("apple", { scale: 1 }), t);
    if (o.until) tl.to(el, { opacity: 0, duration: 0.2 }, o.until);
    D.cue(t, "tick", -14);
    return el;
  };
  D.spot = (br, boxes, t, until) => {
    const k = br.w / br.imgW, id = "m" + t.toFixed(2).replace(".", "_");
    const sv = `<svg width="100%" height="100%" style="position:absolute;inset:0"><defs><mask id="${id}"><rect width="100%" height="100%" fill="white"/>${boxes.map((b) => `<rect x="${b.x * k - 6}" y="${b.y * k - 6}" width="${b.w * k + 12}" height="${b.h * k + 12}" rx="14" fill="black"/>`).join("")}</mask></defs><rect width="100%" height="100%" fill="rgba(246,243,236,0.82)" mask="url(#${id})"/></svg>`;
    const el = h("div", "spot", { position: "absolute", left: 0, top: 0, width: "100%", height: "100%" }, sv, br.pg);
    tl.set(el, { opacity: 0 }, 0);
    tl.to(el, { opacity: 1, duration: 0.4, ease: "power2.out" }, t);
    if (until) tl.to(el, { opacity: 0, duration: 0.25 }, until);
    return el;
  };
  D.cursor = (parent, keys) => {
    const el = h("div", "cursor", {}, `<svg width="34" height="34" viewBox="0 0 24 24"><path d="M5 3l14 8-6 1.6L10 19z" fill="#1A1416" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></svg>`, parent);
    keys.forEach((k, i) => {
      if (i === 0) { tl.set(el, { x: k.x, y: k.y, opacity: 0 }, 0); tl.to(el, { opacity: 1, duration: 0.2 }, k.t); }
      else tl.to(el, { x: k.x, y: k.y, ...S_("smooth") }, k.t - SP.smooth.dur * 0.7);
      if (k.click) { tl.fromTo(el, { scale: 1 }, { keyframes: [{ scale: 0.8, duration: 0.07 }, { scale: 1, duration: 0.22, ease: SP.apple.ease }] }, k.t); D.cue(k.t, "click", -8); }
    });
    return el;
  };
  D.terminal = (parent, x, y, w, hh, lines, o = {}) => {
    const el = D.card(parent, x, y, w, hh, { cls: "term", t: o.t, html: `<div class="tbar"><i></i><i></i><i></i><span>${o.title || "Terminal"}</span></div><div class="tbody"></div>` });
    const body = el.querySelector(".tbody");
    for (const ln of lines) {
      const row = h("div", "tl " + (ln.kind || "out"), {}, null, body);
      if (ln.kind === "cmd") {
        h("span", "pr", {}, ln.prompt ?? "$ ", row);
        const tx = h("span", "tx", {}, "", row);
        h("span", "caret", {}, "", row);
        const full = ln.text; const cps = ln.cps || 34; const d = full.length / cps;
        tl.set(row, { opacity: 0 }, 0); tl.set(row, { opacity: 1 }, ln.t);
        const st = { n: 0 };
        tl.to(st, { n: full.length, duration: d, ease: "none", onUpdate: () => (tx.textContent = full.slice(0, Math.round(st.n))) }, ln.t);
        tl.set({}, { onUpdate: () => (tx.textContent = full.slice(0, Math.round(st.n))) }, ln.t + d + 0.01);
        D.cue(ln.t, "typing", -14, 0, d);
      } else {
        row.innerHTML = ln.html || ln.text;
        tl.set(row, { opacity: 0 }, 0); tl.fromTo(row, { opacity: 0, x: -6 }, { opacity: 1, x: 0, duration: 0.2 }, ln.t);
        if (ln.kind === "ok") D.cue(ln.t, "success", -12);
      }
    }
    return el;
  };
  /** type text into an element, with a typing sound */
  D.type = (el, text, t, d) => {
    const st = { n: 0 }; d = d ?? Math.max(0.3, text.length / 30);
    tl.to(st, { n: text.length, duration: d, ease: "none", onUpdate: () => (el.textContent = text.slice(0, Math.round(st.n))) }, t);
    tl.set({}, { onUpdate: () => (el.textContent = text.slice(0, Math.round(st.n))) }, t + d + 0.01);
    D.cue(t, "typing", -16, 0, d);
  };
  D.image = (parent, x, y, w, hh, src, o = {}) => {
    const el = D.card(parent, x, y, w, hh, { cls: "imgcard " + (o.cls || ""), t: o.t, from: o.from, sound: o.sound, html: `<img src="${src}" style="object-fit:${o.fit || "cover"};object-position:${o.pos || "50% 50%"}">` + (o.label ? `<div class="srclabel">${o.label}</div>` : "") });
    return el;
  };
  D.phone = (parent, x, y, hh, o = {}) => {
    const w = hh * 9 / 19.5 + 24;
    const el = h("div", "phone", { left: px(x), top: px(y), width: px(w), height: px(hh) }, `<div class="screen"></div><div class="island"></div>`, parent);
    if (o.t != null) { M.cardIn(el, o.t, { from: 0.9, y: 60 }); D.cue(o.t, "swoosh", -10); }
    return el;
  };

  // ---------- rolling digits (a clock face whose digits turn like wheels: odometer, eased per second)
  /** returns {el, set(N)}; N in seconds. Each second the last digit rolls over the last 30 % of it. */
  D.clock = (parent, o = {}) => {
    const size = o.size || 64;
    const el = h("div", "clock mono", { fontSize: px(size), height: px(size * 1.15), lineHeight: px(size * 1.15) }, null, parent);
    const col = (base) => { const c = h("span", "dcol", { height: px(size * 1.15) }, null, el); const s = h("span", "dstrip", {}, Array.from({ length: base + 1 }, (_, i) => `<i>${i % base}</i>`).join(""), c); return s; };
    const mT = col(10), mO = col(10); h("span", "dsep", {}, ":", el); const sT = col(6), sO = col(10);
    const lh = size * 1.15;
    const easeS = (x) => x * x * (3 - 2 * x);
    const set = (N) => {
      N = Math.max(0, N);
      const f = N - Math.floor(N), e = easeS(Math.min(1, Math.max(0, (f - 0.7) / 0.3))), n = Math.floor(N);
      const pos = [
        [mT, (Math.floor(n / 600) % 10) + (n % 600 === 599 ? e : 0)],
        [mO, (Math.floor(n / 60) % 10) + (n % 60 === 59 ? e : 0)],
        [sT, (Math.floor(n / 10) % 6) + (n % 10 === 9 ? e : 0)],
        [sO, (n % 10) + e],
      ];
      for (const [s, p] of pos) s.style.transform = `translateY(${-p * lh}px)`;
    };
    set(0);
    return { el, set };
  };

  // ---------- the timer island (Apple UI: a pill that tilts in, springs level, then morphs)
  /** keys: [{t, s}] seconds shown at each time (linear between keys), plus o.show/o.hide times */
  D.island = (parent, o) => {
    const el = h("div", "island " + (o.cls || ""), { left: px(o.x), top: px(o.y) }, null, parent);
    const ring = h("div", "iring", {}, `<svg viewBox="0 0 44 44" width="44" height="44"><circle cx="22" cy="22" r="18" stroke="rgba(255,159,10,.25)" stroke-width="4" fill="none"/><circle class="arc" cx="22" cy="22" r="18" stroke="#FF9F0A" stroke-width="4" fill="none" stroke-linecap="round" transform="rotate(-90 22 22)" stroke-dasharray="113.1" stroke-dashoffset="113.1"/></svg>`, el);
    const lbl = h("div", "ilabel", {}, o.label || "Timer", el);
    const ck = D.clock(el, { size: o.size || 46 });
    ck.el.classList.add("iclock");
    const arc = ring.querySelector(".arc");
    // arrive: small and tilted, spring level and to full width (measured: -11 deg, ~0.26 s growth, 7 % overshoot)
    D.life(el, o.show, o.hide);
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.15 }, o.show);
    tl.fromTo(el, { rotation: -11, scale: 0.6 }, S_("apple", { rotation: 0, scale: 1 }), o.show);
    tl.fromTo(el, { width: o.w0 || 220 }, S_("apple", { width: o.w1 || 300 }), o.show);
    D.cue(o.show, "island", -10);
    // label gives way to the clock
    const tc = o.clockAt ?? o.show + 0.6;
    tl.fromTo(lbl, { opacity: 1 }, { opacity: 0, filter: "blur(6px)", duration: 0.2 }, tc);
    tl.fromTo(ck.el, { opacity: 0, filter: "blur(8px)", scale: 0.8 }, { opacity: 1, filter: "blur(0px)", scale: 1, ...S_("apple") }, tc + 0.05);
    tl.to(el, S_("apple", { width: o.w2 || 360 }), tc);
    const st = { s: o.keys[0].s };
    const upd = () => { ck.set(st.s); arc.style.strokeDashoffset = 113.1 * (1 - ((st.s % 60) / 60)); };
    for (let i = 1; i < o.keys.length; i++) {
      const a = o.keys[i - 1], b = o.keys[i];
      tl.to(st, { s: b.s, duration: Math.max(0.01, b.t - a.t), ease: b.ease || "none", onUpdate: upd }, a.t);
    }
    tl.set({}, { onUpdate: upd }, o.keys[o.keys.length - 1].t + 0.01);
    upd();
    return { el, clock: ck, ring, arc, lbl };
  };

  // ---------- sound cues: collected for the mix (mix.py), not played by the page
  // name, gain dB, pan -1..1, length (for loops like typing)
  D.sfx = [];
  D.cue = (t, name, gain = 0, pan = 0, len = 0) => D.sfx.push({ t: +t.toFixed(3), name, gain, pan: +pan.toFixed(2), len: +len.toFixed(2) });

  // ---------- text must sit inside its box: measured after the fonts load, shrunk to fit
  // Every text element inside a card (and every .fitw block) is checked against the card's inner box.
  D.fitLog = [];
  function fitAll() {
    const hidden = [];
    for (const e of root.querySelectorAll("*")) if (e.style && e.style.display === "none") { hidden.push(e); e.style.display = ""; }
    const cards = root.querySelectorAll(".card, .browser, .pill, .bh-card, .bh-chip, .bh-tile");
    for (const c of cards) {
      if (c.classList.contains("pill")) continue;
      const cw = c.clientWidth, ch = c.clientHeight;
      if (!cw) continue;
      for (const e of c.querySelectorAll("div, span")) {
        if (e.children.length && !e.classList.contains("words") && !e.classList.contains("label")) {
          // only leaf-ish text holders
          const hasText = [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim());
          if (!hasText) continue;
        }
        if (!e.textContent.trim() || e.closest(".tbody") || e.closest(".clock")) continue;
        const cs = getComputedStyle(e);
        if (cs.position !== "absolute" && !e.classList.contains("words")) continue;
        let left = 0, top = 0, n = e;
        while (n && n !== c) { left += n.offsetLeft; top += n.offsetTop; n = n.offsetParent; }
        // the box an element may use: its own set width if it has one, else the card to its right edge
        const ownW = e.style.width && e.style.width.endsWith("px") ? parseFloat(e.style.width) : Infinity;
        const availW = Math.min(ownW, cw - left - 10), availH = ch - top - 6;
        const needW = e.scrollWidth, needH = e.scrollHeight;
        let k = 1;
        if (needW > availW + 1) k = Math.min(k, availW / needW);
        if (needH > availH + 1 && availH > 0) k = Math.min(k, availH / needH);
        if (k < 0.995) {
          const fs = parseFloat(cs.fontSize);
          e.style.fontSize = Math.floor(fs * k * 0.98) + "px";
          D.fitLog.push({ text: e.textContent.trim().slice(0, 50), scale: +k.toFixed(2) });
        }
      }
    }
    // free-standing blocks with a set width (titles) must not run past their width or the frame
    for (const e of root.querySelectorAll(".fitw")) {
      if (e.closest(".card")) continue;
      const w = parseFloat(e.style.width) || 0;
      if (w && e.scrollWidth > w + 1) { const k = w / e.scrollWidth; e.style.fontSize = Math.floor(parseFloat(getComputedStyle(e).fontSize) * k * 0.98) + "px"; D.fitLog.push({ text: e.textContent.trim().slice(0, 50), scale: +k.toFixed(2) }); }
    }
    for (const e of hidden) e.style.display = "none";
  }

  D.finish = () => {
    tl.set({}, {}, CFG.total);
    window.__hf = window.__hf || {};
    window.__hf.buildReady = window.__hf.buildReady || {};
    const ready = document.fonts.ready.then(() => Promise.all([...document.fonts].map((f) => f.load().catch(() => null)))).then(() => {
      fitAll();
      window.__DIRECTOR.fit = D.fitLog;
    });
    window.__hf.buildReady["director-fit"] = ready;
    window.__timelines["main"] = tl;
    window.__DIRECTOR = { sfx: D.sfx, missing: D.missing || [], spk: spkKeys, atLog: D.atLog, ready, cutouts: D.cutouts.map((c) => ({ t0: c.t0, t1: c.t1, media: D.cutT(c.t0) })) };
  };
})();
