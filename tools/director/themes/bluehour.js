/* Blue Hour components (see bluehour.css for the measured look).

   Motion, measured on refs2/fav.mp4 ("After" panel, 30 fps, every frame read):
   - a graphic cuts in hard from the speaker; a new tile arrives blurred, tilted ~+25 deg and small, sharpens
     in ~0.33 s, swings past upright and settles with a loose rotational spring (~1 s);
   - pills slide up ~40 px out of a blur and are sharp within 5-7 frames, one per spoken item;
   - lines draw from the parent tile out to each child;
   - the camera keeps pulling back while a diagram grows: -10 %/s right after a cut, -3.4 %/s on a long
     shot (0.64 over 10.7 s), panning toward the newest part;
   - chips over the speaker pop from a blur in ~4 frames, with a small x dot on the corner.
   Text presets are ported with their published values:
   - MagicUI TextAnimate: fadeIn (y 20, 0.3 s), blurIn (blur 10 px, 0.3 s), blurInUp (blur 10, y 20, opacity
     0.4 s), slideUp/Down/Left/Right (20 px, 0.3 s), scaleUp (0.5 -> 1, spring damping 15 stiffness 300);
     stagger 0.05 s per word, 0.03 s per character, 0.06 s per line.
   - Componentry KineticTextReveal: each word rises 20 px inside a mask from blur 6 px, 0.72 s,
     cubic-bezier(0.22, 1, 0.36, 1), stagger 0.075 s.
   - Componentry TextMorph: words melt into each other through a threshold filter (alpha x18), blur 12 px,
     0.68 s per morph. */
(function () {
  const { tl, h, M } = D;
  const BH = (window.BH = {});
  const sp = (z, r) => { const s = D.spring(z, r); return { ease: s.ease, duration: s.dur }; };
  const SPIN = sp(0.42, 0.85), SMOOTH = sp(1, 0.75), APPLE = sp(0.68, 0.55), UI = sp(0.86, 0.42);
  const motionSpring = (damping, stiffness, mass = 1) => { const w = Math.sqrt(stiffness / mass), z = damping / (2 * Math.sqrt(stiffness * mass)); return sp(Math.min(z, 1.5), (2 * Math.PI) / w); };
  const SCALEUP = motionSpring(15, 300);           // MagicUI scaleUp
  const KINETIC = "cubic-bezier(0.22,1,0.36,1)";
  gsap.registerEase && gsap.registerEase("bhKinetic", (p) => { // cubic-bezier(0.22,1,0.36,1) solved numerically
    let t = p; for (let i = 0; i < 8; i++) { const x = 3 * (1 - t) * (1 - t) * t * 0.22 + 3 * (1 - t) * t * t * 0.36 + t * t * t - p; const dx = 3 * (1 - t) * (1 - t) * 0.22 + 6 * (1 - t) * t * (0.36 - 0.22) + 3 * t * t * (1 - 0.36); t -= x / (dx || 1); t = Math.min(1, Math.max(0, t)); }
    return 3 * (1 - t) * (1 - t) * t * 1 + 3 * (1 - t) * t * t * 1 + t * t * t;
  });

  // one SVG filter for the morph (Componentry TextMorph threshold)
  const defs = h("div", null, { position: "absolute", width: "0", height: "0", overflow: "hidden" }, `<svg width="0" height="0"><defs><filter id="bh-goo" x="-50%" y="-50%" width="200%" height="200%" color-interpolation-filters="sRGB"><feColorMatrix in="SourceGraphic" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -8.28" result="th"/><feComposite in="SourceGraphic" in2="th" operator="atop"/></filter><filter id="bh-grain"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter></defs></svg>`);

  // ---------------------------------------------------------------- stages
  /** a full-bleed navy world for [t0, t1). o.z0 -> o.z1 is the continuous camera pull-back. */
  BH.stage = (t0, t1, o = {}) => {
    const el = D.scene(t0, t1, { x: 0, y: 0, w: 1920, h: 1080 }, { layer: "front", enter: false, out: false, drift: false, tail: 0, sound: false });
    el.classList.add(o.paper ? "bh-paper" : "bh-stage");
    if (o.paper) h("div", "grain", {}, `<svg width="100%" height="100%"><rect width="100%" height="100%" filter="url(#bh-grain)"/></svg>`, el);
    else {
      const hz = h("div", "bh-horizon", {}, null, el);
      tl.fromTo(hz, { y: 10 }, { y: -12, duration: t1 - t0, ease: "sine.inOut" }, t0);
      h("div", "bh-vignette", {}, null, el);
    }
    const auto = h("div", "bh-camauto", {}, null, el);
    const rig = h("div", "bh-camrig", {}, null, auto);
    const board = h("div", "bh-board", {}, null, rig);
    const wires = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    wires.setAttribute("class", "bh-wires"); wires.setAttribute("viewBox", "-1920 -1080 5760 3240"); board.appendChild(wires);
    const z0 = o.z0 ?? 1.06, z1 = o.z1 ?? Math.max(0.9, z0 - 0.034 * (t1 - t0));
    tl.fromTo(auto, { scale: z0 }, { scale: z1, duration: Math.max(0.1, t1 - t0), ease: "power1.out" }, t0);
    if (o.sound !== false) D.cue(t0, o.paper ? "paper" : "cut", -12);
    return { el, board, rig, auto, wires, t0, t1 };
  };
  /** move the stage camera so board point (x, y) is centred at scale s (smooth critically damped spring) */
  BH.cam = (st, t, x, y, s = 1, o = {}) => {
    tl.to(st.rig, { x: -(x - 960) * s, y: -(y - 540) * s, scale: s, ...(o.dur ? { duration: o.dur, ease: o.ease || "power2.inOut" } : SMOOTH) }, t);
  };
  const place = (el, x, y) => { gsap.set(el, { left: x, top: y, xPercent: -50, yPercent: -50 }); };

  // ---------------------------------------------------------------- glass objects
  /** glass tile at board (x, y). o: {icon | glyph, size, color:'orange', label, rot} */
  BH.tile = (st, x, y, t, o = {}) => {
    const s = o.size || 230;
    const inner = o.icon ? D.icon(o.icon, s * 0.44, "currentColor", o.sw || 1.9) : `<span class="g" style="font-size:${s * 0.5}px">${o.glyph || "?"}</span>`;
    const el = h("div", "bh-tile " + (o.color || ""), { width: s + "px", height: s + "px", borderRadius: s * 0.22 + "px" }, inner, st.board || st);
    place(el, x, y);
    if (o.label) {   // the label sits under the tile, outside it, and arrives a beat later
      const lb = h("div", "bh-tlabel", { left: x + "px", top: y + s / 2 + 26 + "px" }, o.label, st.board || st);
      gsap.set(lb, { xPercent: -50 });
      tl.set(lb, { opacity: 0 }, 0);
      tl.fromTo(lb, { opacity: 0, filter: "blur(8px)", y: 12 }, { opacity: 1, filter: "blur(0px)", y: 0, duration: 0.35, ease: "power2.out" }, t + 0.25);
    }
    tl.set(el, { opacity: 0 }, 0);
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.16 }, t);
    tl.fromTo(el, { filter: "blur(18px)" }, { filter: "blur(0px)", duration: 0.34, ease: "power2.out" }, t);
    tl.fromTo(el, { rotation: o.from ?? 26 }, { rotation: o.rot ?? 0, ...SPIN }, t);
    tl.fromTo(el, { scale: 0.7, y: 44 }, { scale: 1, y: 0, ...APPLE }, t);
    D.cue(t, "tile", -10, (x - 960) / 960);
    return el;
  };
  /** glass pill with an icon */
  BH.pill = (st, x, y, label, t, o = {}) => {
    const el = h("div", "bh-pill " + (o.cls || ""), {}, (o.icon ? D.icon(o.icon, o.cls && o.cls.includes("sm") ? 30 : 40, "currentColor", 1.9) : "") + `<span>${label}</span>`, st.board || st);
    place(el, x, y);
    if (o.anchor === "left") gsap.set(el, { xPercent: 0 });
    if (o.anchor === "right") gsap.set(el, { xPercent: -100 });
    tl.set(el, { opacity: 0 }, 0);
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.2 }, t);
    tl.fromTo(el, { filter: "blur(14px)" }, { filter: "blur(0px)", duration: 0.24, ease: "power2.out" }, t);
    tl.fromTo(el, { y: 40, scale: 0.94 }, { y: 0, scale: 1, ...UI }, t);
    D.cue(t, "pill", -12, (x - 960) / 960);
    return el;
  };
  /** a glowing line between two board points; style 'tree' leaves the parent vertically then curves out */
  BH.wire = (st, a, b, t, o = {}) => {
    const p = document.createElementNS("http://www.w3.org/2000/svg", "path");
    const [x1, y1] = a, [x2, y2] = b;
    let d;
    if (o.style === "straight") d = `M${x1} ${y1} L${x2} ${y2}`;
    else if (o.style === "h") { const mx = (x1 + x2) / 2; d = `M${x1} ${y1} C ${mx} ${y1}, ${mx} ${y2}, ${x2} ${y2}`; }
    else { const my = y1 + (y2 - y1) * 0.55; d = `M${x1} ${y1} C ${x1} ${my}, ${x2} ${y1 + (y2 - y1) * 0.35}, ${x2} ${y2}`; }
    p.setAttribute("d", d); st.wires.appendChild(p);
    const len = p.getTotalLength();
    p.style.strokeDasharray = len; p.style.strokeDashoffset = len;
    tl.set(p, { strokeDashoffset: len }, 0);
    tl.to(p, { strokeDashoffset: 0, duration: o.dur || 0.62, ease: "power2.inOut" }, t);
    if (o.pulse) {
      const q = p.cloneNode(); q.setAttribute("class", "pulse"); st.wires.appendChild(q);
      const seg = 70; q.style.strokeDasharray = `${seg} ${len}`;
      tl.set(q, { strokeDashoffset: seg, opacity: 0 }, 0);
      const reps = o.pulse === true ? 1 : o.pulse;
      for (let i = 0; i < reps; i++) tl.fromTo(q, { strokeDashoffset: seg, opacity: 1 }, { strokeDashoffset: -len, duration: 0.9, ease: "power1.inOut" }, t + 0.5 + i * 1.3);
    }
    if (o.sound !== false) D.cue(t, "wire", -18);
    return p;
  };

  // ---------------------------------------------------------------- text
  const splitText = (text, by, serif) => {
    const sset = new Set((serif || []).map((s) => s.toLowerCase()));
    if (by === "char") return [...text].map((c) => ({ v: c, serif: false }));
    if (by === "line") return text.split("|").map((v) => ({ v, serif: false }));
    return text.split(" ").map((v) => ({ v, serif: sset.has(v.toLowerCase().replace(/[^a-z0-9']/g, "")) }));
  };
  /** animated text. o.anim: blurIn | blurInUp | fadeIn | slideUp | slideLeft | scaleUp | kinetic;
      o.by: word | char | line ("|" separates lines); times: array per word, or a start time */
  BH.say = (parent, text, times, o = {}) => {
    const el = h("div", (o.cls || "bh-say") + " fitw", { left: (o.x ?? 0) + "px", top: (o.y ?? 0) + "px", ...(o.w ? { width: o.w + "px" } : {}), ...(o.size ? { fontSize: o.size + "px" } : {}), textAlign: o.align || "left", ...(o.style || {}) }, null, parent.board || parent);
    if (o.center) gsap.set(el, { xPercent: -50 });
    if (o.center && !o.w && !(o.text || "").includes("/")) el.style.whiteSpace = "nowrap";   // a centred line never wraps on its own
    const parts = splitText(text, o.by || "word", o.serif);
    const stag = o.stagger ?? ({ word: 0.05, char: 0.03, line: 0.06 }[o.by || "word"]) ?? 0.05;
    const anim = o.anim || "blurInUp";
    parts.forEach((p, i) => {
      if (p.v === "/") { h("br", null, null, null, el); return; }
      const t = Array.isArray(times) ? times[Math.min(i, times.length - 1)] : times + i * (anim === "kinetic" ? 0.075 : stag);
      let host = el;
      if (anim === "kinetic") host = h("span", "mask", {}, null, el);
      const s = h("span", "w" + (p.serif ? " bh-serif bh-ice" : "") + (o.accent && o.accent.includes(p.v) ? " bh-ice" : ""), {}, p.v + (o.by === "char" ? "" : " "), host);
      if (o.by === "line") s.style.display = "block";
      tl.set(s, { opacity: 0 }, 0);
      if (anim === "blurIn") tl.fromTo(s, { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.3, ease: "power1.out" }, t);
      else if (anim === "blurInUp") { tl.fromTo(s, { filter: "blur(10px)", y: 20 }, { filter: "blur(0px)", y: 0, duration: 0.3, ease: "power2.out" }, t); tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.4, ease: "power1.out" }, t); }
      else if (anim === "fadeIn") tl.fromTo(s, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, t);
      else if (anim === "slideUp") tl.fromTo(s, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.3, ease: "power2.out" }, t);
      else if (anim === "slideLeft") tl.fromTo(s, { opacity: 0, x: 20 }, { opacity: 1, x: 0, duration: 0.3, ease: "power2.out" }, t);
      else if (anim === "scaleUp") { tl.fromTo(s, { opacity: 0 }, { opacity: 1, duration: 0.3 }, t); tl.fromTo(s, { scale: 0.5 }, { scale: 1, ...SCALEUP }, t); }
      else if (anim === "kinetic") tl.fromTo(s, { opacity: 0, y: o.dist ?? 20, filter: "blur(6px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 0.72, ease: "bhKinetic" }, t);
    });
    return el;
  };
  /** words melting into each other (TextMorph): words[i] shows from times[i] */
  BH.morph = (parent, words, times, o = {}) => {
    const el = h("div", "bh-morph " + (o.cls || "bh-say"), { left: (o.x ?? 960) + "px", top: (o.y ?? 0) + "px", filter: "url(#bh-goo)", ...(o.size ? { fontSize: o.size + "px" } : {}) }, null, parent.board || parent);
    words.forEach((w, i) => {
      const l = h("span", "lyr" + (o.serifIdx && o.serifIdx.includes(i) ? " bh-serif bh-ice" : ""), {}, w, el);
      tl.set(l, { opacity: 0 }, 0);
      const t = times[i];
      if (i === 0) tl.fromTo(l, { opacity: 0, filter: "blur(12px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.4 }, t);
      else tl.fromTo(l, { opacity: 0, filter: "blur(12px)", scale: 0.96 }, { opacity: 1, filter: "blur(0px)", scale: 1, duration: 0.68, ease: "sine.inOut" }, t);
      if (i < words.length - 1) tl.to(l, { opacity: 0, filter: "blur(12px)", scale: 1.04, duration: 0.68, ease: "sine.inOut" }, times[i + 1]);
      D.cue(t, "morph", -16);
    });
    return el;
  };
  /** a number whose digits roll into place like a counter (right to left), e.g. "19,000,000" */
  BH.roll = (parent, text, t, o = {}) => {
    const el = h("div", "bh-num " + (o.cls || ""), { left: (o.x ?? 960) + "px", top: (o.y ?? 400) + "px", ...(o.size ? { fontSize: o.size + "px" } : {}), ...(o.color ? { color: o.color } : {}) }, null, parent.board || parent);
    if (o.center !== false) gsap.set(el, { xPercent: -50 });
    const chars = [...text]; let k = 0;
    const nd = chars.filter((c) => /\d/.test(c)).length;
    chars.forEach((c) => {
      if (!/\d/.test(c)) { h("span", "sep" + (o.serifSep ? " bh-serif" : ""), {}, c, el); return; }
      const col = h("span", "col", {}, null, el);
      const strip = h("span", "strip", {}, Array.from({ length: 20 }, (_, i) => `<i>${i % 10}</i>`).join(""), col);
      const target = 10 + +c, j = nd - 1 - k++;
      const tt = t + j * (o.stagger ?? 0.05);
      tl.set(strip, { yPercent: 0 }, 0);
      tl.fromTo(strip, { yPercent: 0 }, { yPercent: -(target / 20) * 100, duration: o.dur || 1.3, ease: "expo.out" }, tt);
      tl.fromTo(strip, { filter: "blur(0px)" }, { keyframes: [{ filter: "blur(5px)", duration: 0.15 }, { filter: "blur(0px)", duration: 0.5 }] }, tt);
    });
    tl.set(el, { opacity: 0 }, 0); tl.to(el, { opacity: 1, duration: 0.15 }, t);
    D.cue(t, "count", -12);
    return el;
  };
  /** yellow marker swept behind a span (paper scenes) */
  BH.marker = (span, t) => { const m = h("span", "bh-marker", {}, null, span); span.classList.add("bh-hl"); tl.fromTo(m, { scaleX: 0 }, { scaleX: 1, duration: 0.45, ease: "power3.out" }, t); D.cue(t, "marker", -16); return m; };

  // ---------------------------------------------------------------- over the speaker
  /** a row of chips at the bottom of the speaker shot. items: [{t, icon, l1, l2}] */
  BH.chips = (t0, t1, items, o = {}) => {
    const sc = D.scene(t0, t1, { x: 0, y: 0, w: 1920, h: 1080 }, { layer: "mid", enter: false, out: false, drift: false, tail: 0, sound: false });
    const gap = 40, w = o.w || 380, total = items.length * w + (items.length - 1) * gap;
    items.forEach((it, i) => {
      const x = (1920 - total) / 2 + i * (w + gap), y = o.y ?? 1080 - 104 - 64;
      const c = h("div", "bh-chip", { left: x + "px", top: y + "px", width: w + "px" }, `<div class="ci">${D.icon(it.icon, 40, "#fff", 2)}</div><div class="ct">${it.l1}${it.l2 ? "<br>" + it.l2 : ""}</div><div class="cx">${D.icon("Cancel01Icon", 16, "#fff", 3)}</div>`, sc);
      tl.set(c, { opacity: 0 }, 0);
      tl.fromTo(c, { opacity: 0, filter: "blur(12px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.16 }, it.t);
      tl.fromTo(c, { scale: 0.8, y: 40 }, { scale: 1, y: 0, ...APPLE }, it.t);
      tl.to(c, { opacity: 0, filter: "blur(10px)", y: 20, duration: 0.22, ease: "power2.in" }, t1 - 0.2);
      D.cue(it.t, "chip", -11, (x + w / 2 - 960) / 960);
    });
    return sc;
  };
  /** a bold caption over the speaker, word by word on the spoken words (opening style of the reference) */
  BH.caption = (t0, t1, text, times, o = {}) => {
    const sc = D.scene(t0, t1, { x: 0, y: 0, w: 1920, h: 1080 }, { layer: "mid", enter: false, out: false, drift: false, tail: 0, sound: false });
    const el = BH.say(sc, text, times, { cls: "bh-cap", x: 0, y: o.y ?? 830, anim: o.anim || "blurInUp", serif: o.serif, align: "center", style: { width: "1920px" } });
    tl.to(el, { opacity: 0, filter: "blur(8px)", duration: 0.2 }, t1 - 0.2);
    return sc;
  };
  /** captured page in a dark glass frame on a stage */
  BH.frame = (st, x, y, w, hh, cap, t, o = {}) => {
    const br = D.browser(st.board, x - w / 2, y - hh / 2, w, hh, cap.src, { url: o.url || "", imgW: cap.w, cls: "bh-frame" });
    tl.set(br.win, { opacity: 0 }, 0);
    tl.fromTo(br.win, { opacity: 0, filter: "blur(16px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.36 }, t);
    tl.fromTo(br.win, { scale: 0.86, y: 60, rotationX: o.tilt ?? 14, transformPerspective: 1600 }, { scale: 1, y: 0, rotationX: 0, ...SMOOTH }, t);
    D.cue(t, "frame", -12);
    return br;
  };
  /** image card (stills, thumbnails) on a stage */
  BH.img = (st, x, y, w, hh, src, t, o = {}) => {
    const el = h("div", "bh-img", { width: w + "px", height: hh + "px" }, `<img src="${src}" style="object-position:${o.pos || "50% 50%"}">`, st.board || st);
    place(el, x, y);
    tl.set(el, { opacity: 0 }, 0);
    tl.fromTo(el, { opacity: 0, filter: "blur(14px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.3 }, t);
    tl.fromTo(el, { scale: 0.8, rotation: o.from ?? 0, y: 40 }, { scale: 1, rotation: o.rot ?? 0, y: 0, ...APPLE }, t);
    if (o.sound !== false) D.cue(t, "pill", -14);
    return el;
  };
  /** dark glass card for text content */
  BH.card = (st, x, y, w, hh, t, html = "", o = {}) => {
    const el = h("div", "bh-card", { width: w + "px", height: hh + "px" }, html, st.board || st);
    place(el, x, y);
    tl.set(el, { opacity: 0 }, 0);
    tl.fromTo(el, { opacity: 0, filter: "blur(14px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.3 }, t);
    tl.fromTo(el, { scale: 0.9, y: 40 }, { scale: 1, y: 0, ...UI }, t);
    if (o.sound !== false) D.cue(t, "pill", -14);
    return el;
  };
  BH.out = (el, t) => tl.to(el, { opacity: 0, filter: "blur(12px)", scale: 0.92, duration: 0.3, ease: "power2.in" }, t);
  BH.SP = { SPIN, SMOOTH, APPLE, UI, SCALEUP };
})();
