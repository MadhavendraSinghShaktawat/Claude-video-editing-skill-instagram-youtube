/* Studio theme: layouts that keep the speaker on screen, text-design components and animated parts.
   Ported behaviour (published source values, magicui.design and componentry.dev):
   - TypingAnimation: 100 ms a character, line cursor that blinks.
   - WordRotate: the word leaves up and the next enters from below, 0.25 s ease-out.
   - MorphingText: morphTime 1.5 s; incoming blur = 8/f - 8 px, opacity = f^0.4, through a threshold filter.
   - Text3DFlip: each letter turns from rotateY(90deg), spring damping 30 stiffness 300, 0.05 s stagger.
   - DiaTextReveal: a colour band 34 % wide sweeps across the text in 1.5 s, cubic in-out, leaving it solid.
   - Highlighter (rough-notation): hand-drawn underline / box / circle / highlight / strike, 0.6 s, 2 strokes.
   - AnimatedList: new item on top, the rest move down, spring stiffness 350 damping 40.
   - OrbitingCircles: items on a ring, one turn per 20 s by default.
   - FlickeringGrid: 4 px squares, 6 px gap, max opacity 0.3, flicker chance 0.3 a second (seeded here).
   - DotPattern: 16 px spacing, 1 px dots.
   - Aurora bars (ui.unlumen.com): glowing vertical bars that rise and fall.
   - Safari / iPhone mockups (magicui) as CSS frames.
   Layouts follow the golden ratio: 0.618 / 0.382 splits, 64 px outer margin. */
(function () {
  const { tl, h, M } = D;
  const ST = (window.ST = {});
  const W = 1920, H = 1080;
  const sp = (z, r) => { const s = D.spring(z, r); return { ease: s.ease, duration: s.dur }; };
  const fm = (damping, stiffness, mass = 1) => sp(Math.min(1.4, damping / (2 * Math.sqrt(stiffness * mass))), (2 * Math.PI) / Math.sqrt(stiffness / mass));
  const SM = (ST.SMOOTH = sp(1, 0.7)), AP = (ST.APPLE = sp(0.68, 0.55)), UI = (ST.UI = sp(0.86, 0.42)), SOFT = sp(1, 1.0);
  const LISTSP = fm(40, 350), FLIPSP = fm(30, 300);
  const px = (v) => (typeof v === "number" ? v + "px" : v);
  const hash = (i, j = 0) => { const x = Math.sin(i * 127.1 + j * 311.7) * 43758.5453; return x - Math.floor(x); };

  // ------------------------------------------------------------- layouts (golden ratio)
  const L = (ST.L = {
    splitR: { panel: { x: 64, y: 92, w: 1088, h: 896 }, card: { x: 1184, y: 92, w: 672, h: 896, r: 28 } },
    splitRm: { panel: { x: 768, y: 92, w: 1088, h: 896 }, card: { x: 64, y: 92, w: 672, h: 896, r: 28 } },
    splitL: { outer: { x: 40, y: 40, w: 1840, h: 1000 }, card: { x: 58, y: 58, w: 690, h: 964, r: 28 }, panel: { x: 764, y: 58, w: 1098, h: 964 } },
    pip: { stage: { x: 40, y: 40, w: 1840, h: 1000 }, card: { x: 1546, y: 622, w: 290, h: 386, r: 26 } },
  });
  ST.frames = [];

  // ------------------------------------------------------------- entrances (no two in a row the same)
  const ENTER = {
    rise: (el, t) => { tl.fromTo(el, { y: 90, opacity: 0, filter: "blur(18px)" }, { y: 0, opacity: 1, filter: "blur(0px)", ...SM }, t); },
    grow: (el, t) => { tl.fromTo(el, { scale: 0.86, opacity: 0, filter: "blur(16px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", ...AP }, t); },
    iris: (el, t) => { tl.fromTo(el, { clipPath: "circle(0% at 50% 50%)" }, { clipPath: "circle(75% at 50% 50%)", duration: 0.7, ease: "power3.inOut" }, t); },
    wipe: (el, t) => { tl.fromTo(el, { clipPath: "inset(0% 0% 100% 0% round 28px)" }, { clipPath: "inset(0% 0% 0% 0% round 28px)", duration: 0.62, ease: "expo.inOut" }, t); },
    slide: (el, t) => { tl.fromTo(el, { x: -140, opacity: 0, filter: "blur(14px)" }, { x: 0, opacity: 1, filter: "blur(0px)", ...SM }, t); },
    flip: (el, t) => { tl.fromTo(el, { rotationY: -24, transformPerspective: 1800, opacity: 0, x: -40 }, { rotationY: 0, opacity: 1, x: 0, ...SOFT }, t); },
    zoom: (el, t) => { tl.fromTo(el, { scale: 1.25, opacity: 0, filter: "blur(22px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.55, ease: "expo.out" }, t); },
  };
  const ENTER_ORDER = ["rise", "grow", "wipe", "slide", "iris", "flip", "zoom"];
  let lastEnter = "", enterN = 0;
  const pickEnter = (want) => { let k = want || ENTER_ORDER[enterN++ % ENTER_ORDER.length]; if (k === lastEnter) k = ENTER_ORDER[enterN++ % ENTER_ORDER.length]; lastEnter = k; return k; };
  const EXIT = {
    fade: (el, t) => tl.to(el, { opacity: 0, filter: "blur(10px)", duration: 0.28, ease: "power2.in" }, t),
    drop: (el, t) => tl.to(el, { y: 60, opacity: 0, duration: 0.3, ease: "power2.in" }, t),
    shrink: (el, t) => tl.to(el, { scale: 0.92, opacity: 0, duration: 0.3, ease: "power2.in" }, t),
  };

  const FRAME_EXITS = [
    ["inset(0% 0% 0% 0%)", "inset(0% 0% 100% 0%)"],        // up
    ["circle(110% at 50% 50%)", "circle(0% at 50% 50%)"],  // iris close
    ["inset(0% 0% 0% 0%)", "inset(0% 100% 0% 0%)"],        // to the left
    ["inset(0% 0% 0% 0%)", "inset(50% 50% 50% 50%)"],      // to the centre
  ];
  let exitN = 0;
  // ------------------------------------------------------------- frames (layouts) on the canvas
  /** kind: splitR | splitRm | splitL | pip; o.dark for a dark panel; returns {p, w, h} where p is the panel content box */
  ST.frame = (t0, t1, kind, o = {}) => {
    const lay = L[kind];
    const host = D.scene(t0, t1, { x: 0, y: 0, w: W, h: H }, { layer: "back", enter: false, out: false, drift: false, tail: 0.35, sound: false });
    host.classList.add("st-full");
    host.style.background = "transparent";
    let panelR = lay.panel, p;
    if (kind === "splitL") {
      const outer = h("div", "st-outer", { left: px(lay.outer.x), top: px(lay.outer.y), width: px(lay.outer.w), height: px(lay.outer.h) }, null, host);
      p = h("div", "st-panel dark" + (o.lime !== false ? " lime" : ""), { left: px(panelR.x), top: px(panelR.y), width: px(panelR.w), height: px(panelR.h), borderRadius: "28px" }, null, host);
      ENTER[pickEnter(o.enter || "wipe")](outer, t0);
      ENTER.rise(p, t0 + 0.12);
    } else if (kind === "pip") {
      panelR = lay.stage;
      p = h("div", "st-stage", { left: px(panelR.x), top: px(panelR.y), width: px(panelR.w), height: px(panelR.h) }, null, host);
      ENTER[pickEnter(o.enter)](p, t0);
    } else {
      p = h("div", "st-panel" + (o.dark ? " dark" : ""), { left: px(panelR.x), top: px(panelR.y), width: px(panelR.w), height: px(panelR.h) }, null, host);
      ENTER[pickEnter(o.enter)](p, t0);
    }
    if (o.bg === "flicker" || (o.bg !== "none" && (o.dark || kind === "splitL" || kind === "pip"))) ST.flicker(p, panelR.w, panelR.h, t0, t1 + 0.4, { color: o.flickerColor || "255,255,255" });
    if (o.bg === "aurora") ST.aurora(p, panelR.w, panelR.h, t0, t1 + 0.4, o.aurora || {});
    if (o.bg === "dots") h("div", null, { position: "absolute", inset: "0", backgroundImage: "radial-gradient(rgba(20,20,20,.18) 1px, transparent 1.3px)", backgroundSize: "16px 16px" }, null, p);
    const inner = h("div", "st-in", {}, null, p);
    // exits are clipped away, never faded: a dark panel fading over the cream canvas turns muddy grey
    const ex = FRAME_EXITS[exitN++ % FRAME_EXITS.length];
    tl.fromTo(host, { clipPath: ex[0] }, { clipPath: ex[1], duration: 0.42, ease: "expo.in", immediateRender: false }, t1 - 0.06);
    tl.set(host, { opacity: 0 }, t1 + 0.38);
    ST.frames.push({ t0, t1, kind, card: lay.card, dark: !!(o.dark || kind === "pip"), p: inner, src: ((new Error().stack || "").split("\n").find((l) => /plan/.test(l)) || "").replace(/.*\//, "").replace(/\)$/, "") });
    return { p: inner, w: panelR.w, h: panelR.h, host };
  };

  /** speaker cut out of the footage, graphics behind (back) and in front (front) of them */
  ST.cut = (t0, t1, o = {}) => {
    // Three layers, bottom to top: the real footage (the full-frame speaker, never hidden), the text and
    // graphics, then the same footage with its background removed (alpha WebM from matte.py). The cutout
    // uses the exact camera of the footage under it, and ST.finish holds that camera still for the span,
    // so the person lines up pixel for pixel and the words sit "behind" them in the real room.
    const idx = D.cutouts.length; D.cutouts.push({ t0, t1 });
    if (!ST._cutText) { ST._cutText = h("div", null, { position: "absolute", inset: "0" }, null, D.layers.spk); ST._cutPeople = h("div", null, { position: "absolute", inset: "0" }, null, D.layers.spk); }
    const back = h("div", "st-full st-cutback", { pointerEvents: "none" }, null, ST._cutText);
    D.life(back, t0, t1 + 0.02);
    if (o.scrim !== false) h("div", null, { position: "absolute", inset: "0", background: o.scrim || "linear-gradient(180deg, rgba(0,0,0,.42) 0%, rgba(0,0,0,.14) 46%, rgba(0,0,0,0) 70%)" }, null, back);
    if (o.grid) ST.flicker(back, W, H, t0, t1, { color: "255,255,255", max: 0.16 });
    if (o.aurora) ST.aurora(back, W, H, t0, t1, o.aurora);
    const bk = h("div", "st-in", {}, null, back);
    gsap.set(bk, { transformOrigin: "50% 0%" });   // settles from the top edge down, so top-line words never leave the frame
    tl.fromTo(bk, { scale: 1.06 }, { scale: 1, duration: Math.max(0.5, t1 - t0), ease: "power1.out" }, t0);
    tl.fromTo(back, { opacity: 0 }, { opacity: 1, duration: 0.22, ease: "power1.out" }, t0);
    tl.to(back, { opacity: 0, duration: 0.18, ease: "power1.in" }, t1 - 0.16);
    const wrap = h("div", "st-cutwrap", { position: "absolute", left: "0", top: "0", width: W + "px", height: H + "px", transformOrigin: "0 0" }, null, ST._cutPeople);
    D.life(wrap, t0 - 0.02, t1);
    gsap.set(wrap, D.camFor({ x: 0, y: 0, w: W, h: H, r: 0 }, 1.0, t0));
    const shk = h("div", null, { position: "absolute", inset: "0" }, null, wrap);
    D.cutShakes.push({ t0, t1, el: shk });
    const v = document.getElementById("cut_" + String(idx).padStart(2, "0"));
    if (v && v.tagName === "VIDEO") { v.style.cssText = "position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover"; shk.appendChild(v); }
    const front = D.scene(t0, t1, { x: 0, y: 0, w: W, h: H }, { layer: "mid", enter: false, out: false, drift: false, tail: 0.02, sound: false });
    front.classList.add("st-full");
    ST.frames.push({ t0, t1, kind: "cut" });
    return { back: bk, front, person: shk };
  };

  /** where the head is in a full-frame cutout (measured face boxes): text behind the person goes above it
      (y < top) or to the sides (x < left, x > right) so the head never hides the key letters */
  ST.head = (t) => { const f = D.cfg.setups.find((q) => D.cutT(t) >= q.from && D.cutT(t) < q.to) || D.cfg.setups[0]; const fh = f.face_h * 1080 * f.base; return { top: Math.round(432 - fh * 0.75), left: Math.round(960 - fh * 0.75), right: Math.round(960 + fh * 0.75) }; };
  /** speaker choreography: card layouts, cutouts, full frame with zoom in and out in between */
  // a punch or zoom during a cutout would move the footage but not the cutout: record them and complain
  ST._zooms = [];
  for (const k of ["punch", "ease"]) { const f0 = D[k]; D[k] = (t, ...r) => { ST._zooms.push(t); return f0(t, ...r); }; }
  /** a panel leaves once its story is told: when nothing new has arrived in it for HOLD seconds, it ends and the
      speaker takes the frame back (user: "animations are more than my video"). Measured from the timeline: the
      last tween that starts on an element inside the panel. */
  ST.HOLD = 4.5;
  const trimIdle = () => {
    const kids = tl.getChildren(true, true, false);
    for (const f of ST.frames) {
      if (f.kind === "cut" || !f.p || f.noTrim) continue;
      const host = f.p.closest(".st-full") || f.p;
      let last = f.t0;
      for (const tw of kids) {
        const st = tw.startTime(); if (st >= f.t1 - 0.1 || st < f.t0) continue;
        if (tw.targets().some((x) => x instanceof Element && f.p.contains(x) && x !== f.p && x.tagName !== "CANVAS")) last = Math.max(last, st + Math.min(tw.duration(), 1.2));
      }
      const end = Math.max(last + ST.HOLD, f.t0 + 5);
      if (end > f.t1 - 1.0) continue;
      const d = end - f.t1;
      for (const tw of kids) if (tw.startTime() >= f.t1 - 0.1 && tw.targets().includes(host)) tw.startTime(tw.startTime() + d);
      f.trimmed = +(-d).toFixed(2); f.t1 = end;
    }
  };
  ST.finish = () => {
    trimIdle();
    for (const t of ST._zooms) for (const f of ST.frames) if (f.kind === "cut" && t > f.t0 - 0.05 && t < f.t1) console.warn(`zoom at ${t.toFixed(2)} inside cutout ${f.t0.toFixed(2)}-${f.t1.toFixed(2)}: the person would slide off the footage`);
    const fr = ST.frames.slice().sort((a, b) => a.t0 - b.t0);
    D.speaker(0, "full", { zoom: 1.0, dur: 0 });
    let prevEnd = 0, pushIn = true;
    const ins = D.cfg.insert;
    const gap = (a, b, toCut) => {
      if (b - a < 0.4) return;
      if (ins && a >= ins.at - 0.6 && b <= ins.at + ins.dur + 0.6) return;
      // alternate: a slow push in, a slow pull out, each held to under 6 % (1080p footage)
      // before a cutout the move ends at zoom 1.0, the camera the cutout is held at, so there is no jump
      const z1 = toCut ? 1.0 : (pushIn ? 1.07 : 0.95), z0 = toCut ? (pushIn ? 1.06 : 0.96) : 1.0;
      D.speaker(a + 0.01, "full", { zoom: z0, dur: 0 });
      D.speaker(a + 0.02, "full", { zoom: z1, ease: "sine.inOut", dur: Math.max(0.6, b - a - 0.05) });
      pushIn = !pushIn;
    };
    fr.forEach((f, i) => {
      gap(prevEnd, f.t0, f.kind === "cut");
      if (f.kind !== "cut" && f.card) {
        D.speaker(f.t0, f.card, { spring: "layout" });
        D.spkStyle(f.t0, f.dark ? { outline: "3px solid rgba(255,255,255,.14)", boxShadow: "0 30px 60px -20px rgba(0,0,0,.7)" } : { outline: "8px solid #ffffff", boxShadow: "0 30px 70px -24px rgba(20,20,20,.45)" });
      }
      const next = fr[i + 1];
      if (f.kind !== "cut" && (!next || next.t0 - f.t1 > 0.35)) { D.speaker(f.t1, "full", { zoom: 1.0, spring: "layout" }); D.spkStyle(f.t1 + 0.6, { outline: "0px solid transparent" }); }
      if (f.kind === "cut") D.speaker(f.t0 - 0.01, "full", { zoom: 1.0, dur: 0 });   // camera held still under the cutout
      prevEnd = Math.max(prevEnd, f.t1 + (f.kind === "cut" ? 0 : 0.6));
    });
    gap(prevEnd, D.cfg.total);
  };

  // ------------------------------------------------------------- backgrounds
  /** FlickeringGrid, seeded so every frame is the same on every render */
  ST.flicker = (parent, w, hh, t0, t1, o = {}) => {
    const size = o.size || 4, gap = o.gap || 6, max = o.max ?? 0.3, chance = o.chance ?? 0.3, col = o.color || "255,255,255";
    const cv = h("canvas", "st-canvas", { left: "0", top: "0", width: w + "px", height: hh + "px", pointerEvents: "none" }, null, parent);
    const dpr = 1; cv.width = w * dpr; cv.height = hh * dpr;
    const ctx = cv.getContext("2d");
    const cols = Math.ceil(w / (size + gap)), rows = Math.ceil(hh / (size + gap));
    const st = { t: 0 };
    const draw = () => {
      ctx.clearRect(0, 0, cv.width, cv.height);
      const tt = st.t;
      for (let i = 0; i < cols; i++) for (let j = 0; j < rows; j++) {
        const k = i * 7919 + j;
        const period = 1 / (chance * (0.5 + hash(k, 3)));         // seconds between changes for this square
        const step = Math.floor(tt / period + hash(k, 1) * 10);
        const a = hash(k, step) * max * (0.35 + 0.65 * Math.min(1, 1.2 - Math.hypot(i / cols - 0.5, j / rows - 0.5)));
        if (a < 0.02) continue;
        ctx.fillStyle = `rgba(${col},${a.toFixed(3)})`;
        ctx.fillRect(i * (size + gap) * dpr, j * (size + gap) * dpr, size * dpr, size * dpr);
      }
    };
    tl.fromTo(st, { t: 0 }, { t: t1 - t0, duration: Math.max(0.1, t1 - t0), ease: "none", onUpdate: draw }, t0);
    draw();
    return cv;
  };
  /** aurora bars: glowing vertical bars whose heights move like a slow equaliser */
  ST.aurora = (parent, w, hh, t0, t1, o = {}) => {
    const n = o.n || 22, colors = o.colors || ["#E36A3A", "#EC4899", "#8B5CF6", "#3B82F6"];
    const wrap = h("div", null, { position: "absolute", left: "0", bottom: "0", width: w + "px", height: hh + "px", display: "flex", alignItems: "flex-end", gap: (o.gap ?? 14) + "px", padding: "0 " + (o.pad ?? 40) + "px", filter: "blur(" + (o.blur ?? 2) + "px)", opacity: o.opacity ?? 0.9 }, null, parent);
    const bars = [];
    for (let i = 0; i < n; i++) {
      const c = colors[Math.floor((i / n) * colors.length) % colors.length], c2 = colors[(Math.floor((i / n) * colors.length) + 1) % colors.length];
      const b = h("div", null, { flex: "1", height: "40%", borderRadius: "999px 999px 0 0", background: `linear-gradient(to top, ${c} 0%, ${c2} 60%, rgba(255,255,255,0) 100%)`, boxShadow: `0 0 40px ${c}`, transformOrigin: "50% 100%" }, null, wrap);
      bars.push(b);
    }
    const st = { t: 0 };
    const upd = () => bars.forEach((b, i) => { const v = 0.28 + 0.32 * (0.5 + 0.5 * Math.sin(st.t * 1.3 + i * 0.55)) + 0.22 * (0.5 + 0.5 * Math.sin(st.t * 0.7 + i * 1.7 + 1.3)); b.style.height = (v * (o.maxH ?? 0.75) * 100).toFixed(2) + "%"; });
    tl.fromTo(st, { t: 0 }, { t: t1 - t0, duration: Math.max(0.1, t1 - t0), ease: "none", onUpdate: upd }, t0);
    upd();
    tl.fromTo(wrap, { yPercent: 40, opacity: 0 }, { yPercent: 0, opacity: o.opacity ?? 0.9, ...SM }, t0);
    return wrap;
  };

  // ------------------------------------------------------------- media parts
  ST.icon3d = (parent, name, x, y, size, t, o = {}) => {
    const el = h("img", "st-3d", { left: px(x - size / 2), top: px(y - size / 2), width: px(size), height: px(size) }, null, parent);
    el.src = `assets/icons3d/${name}_${o.angle || "dynamic"}.webp`;
    tl.set(el, { opacity: 0 }, 0);
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.18 }, t);
    tl.fromTo(el, { scale: 0.3, rotation: o.spin ?? -24, y: 30 }, { scale: 1, rotation: 0, y: 0, ...AP }, t);
    return el;
  };
  ST.app = (parent, name, x, y, size, t, o = {}) => {
    const el = h("div", "st-app", { left: px(x - size / 2), top: px(y - size / 2), width: px(size), height: px(size) }, `<img src="assets/appicons/${name}.webp">`, parent);
    tl.set(el, { opacity: 0 }, 0);
    tl.fromTo(el, { opacity: 0, filter: "blur(10px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25 }, t);
    tl.fromTo(el, { scale: 0.5, y: 40 }, { scale: 1, y: 0, ...AP }, t);
    return el;
  };
  /** pill that grows out of its own left edge (launch-video "pill grows from icon") */
  ST.pill = (parent, x, y, text, t, o = {}) => {
    const el = h("div", "st-pill " + (o.cls || "w"), { left: px(x), top: px(y), ...(o.size ? { fontSize: o.size + "px" } : {}) }, (o.icon3d ? `<img src="assets/icons3d/${o.icon3d}_dynamic.webp" style="width:1.4em;height:1.4em;margin:-.3em 0">` : o.icon ? D.icon(o.icon, (o.size || 30) * 1.1, "currentColor", 2) : "") + `<span>${text}</span>`, parent);
    if (o.center) gsap.set(el, { xPercent: -50 });
    tl.set(el, { opacity: 0 }, 0);
    tl.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.12 }, t);
    tl.fromTo(el, { clipPath: "inset(0% 100% 0% 0% round 999px)" }, { clipPath: "inset(0% 0% 0% 0% round 999px)", duration: 0.55, ease: "expo.out" }, t);
    tl.fromTo(el.lastChild, { opacity: 0, filter: "blur(6px)", x: -10 }, { opacity: 1, filter: "blur(0px)", x: 0, duration: 0.35, ease: "power2.out" }, t + 0.12);
    return el;
  };
  /** Safari window (MagicUI look) with a captured page; compatible with D.focus / D.mark */
  ST.safari = (parent, x, y, w, hh, cap, t, o = {}) => {
    const win = h("div", "st-safari", { left: px(x), top: px(y), width: px(w), height: px(hh) }, `<div class="sbar"><i style="background:#FF5F57"></i><i style="background:#FEBC2E"></i><i style="background:#28C840"></i><div class="surl">${D.icon("SquareLock02Icon", 16, "#6B6B6B")}${o.url || ""}</div></div><div class="sview"><div class="spg"><img src="${cap.src}" style="width:100%;display:block"></div></div>`, parent);
    const view = win.querySelector(".sview"), pg = win.querySelector(".spg");
    pg.style.width = w + "px";
    const br = { win, view, pg, w, vh: hh - 56, imgW: cap.w };
    if (t != null) ENTER[o.enter || "rise"](win, t);
    return br;
  };
  ST.iphone = (parent, x, y, hh, t, o = {}) => {
    const w = Math.round(hh * 0.49);
    const el = h("div", "st-iphone", { left: px(x - w / 2), top: px(y), width: px(w), height: px(hh) }, `<div class="scr"></div><div class="isl"></div>`, parent);
    if (o.img) h("img", null, {}, null, el.querySelector(".scr")).src = o.img;
    if (t != null) { tl.fromTo(el, { opacity: 0, y: 80, rotation: o.rot ?? -6 }, { opacity: 1, y: 0, rotation: 0, ...SM }, t); }
    return el;
  };
  /** AnimatedList: items: [{t, html | icon3d/app + title + sub, cls}], newest on top, others move down */
  ST.list = (parent, x, y, w, items, o = {}) => {
    const ih = o.itemH || 112, gap = o.gap || 18;
    const els = items.map((it, k) => {
      const icon = it.app ? `<div class="ic"><img src="assets/appicons/${it.app}.webp" style="border-radius:18px"></div>` : it.icon3d ? `<div class="ic"><img src="assets/icons3d/${it.icon3d}_dynamic.webp"></div>` : it.icon ? `<div class="ic" style="background:${it.bg || "#F1EEE8"}">${D.icon(it.icon, 40, it.fg || "#141414", 1.8)}</div>` : "";
      const el = h("div", "st-item " + (o.dark ? "dark " : "") + (it.cls || ""), { left: px(x), top: px(y), width: px(w), height: px(ih), "--k": ih / 112, gap: px(22 * ih / 112) }, `${icon}<div style="flex:1;min-width:0"><div class="tt">${it.title}</div>${it.sub ? `<div class="ts">${it.sub}</div>` : ""}</div>${it.x ? `<div class="st-x" style="background:${it.xbg || "#E2402F"}">${D.icon(it.x === "ok" ? "Tick02Icon" : "Cancel01Icon", 24, "#fff", 2.6)}</div>` : ""}`, parent);
      tl.set(el, { opacity: 0 }, 0);
      return el;
    });
    items.forEach((it, k) => {
      const el = els[k];
      tl.fromTo(el, { opacity: 0, scale: 0.86, y: -30 }, { opacity: 1, scale: 1, y: 0, ...LISTSP }, it.t);
      for (let j = 0; j < k; j++) tl.to(els[j], { y: (k - j) * (ih + gap), ...LISTSP }, it.t);   // older items move down
      if (it.x) tl.fromTo(el.querySelector(".st-x"), { scale: 0, rotation: -90 }, { scale: 1, rotation: 0, ...AP }, it.t + (it.xDelay ?? 0.35));
    });
    return els;
  };
  /** OrbitingCircles: nodes on a ring around (cx, cy) */
  ST.orbit = (parent, cx, cy, r, nodes, t0, t1, o = {}) => {
    const ring = h("div", null, { position: "absolute", left: px(cx - r), top: px(cy - r), width: px(2 * r), height: px(2 * r), borderRadius: "50%", border: `2px ${o.dash === false ? "solid" : "dashed"} ${o.ringColor || "rgba(20,20,20,.16)"}` }, null, parent);
    tl.fromTo(ring, { scale: 0.6, opacity: 0 }, { scale: 1, opacity: 1, ...SM }, t0);
    const period = o.period || 20, dir = o.reverse ? -1 : 1, a0 = o.start ?? -Math.PI / 2;
    const st = { t: 0 };
    const place = () => nodes.forEach((n, i) => { const a = a0 + (i / nodes.length) * Math.PI * 2 + dir * (st.t / period) * Math.PI * 2; n.style.left = (cx + Math.cos(a) * r - n._w / 2).toFixed(1) + "px"; n.style.top = (cy + Math.sin(a) * r - n._h / 2).toFixed(1) + "px"; });
    nodes.forEach((n) => { n._w = parseFloat(n.style.width) || 120; n._h = parseFloat(n.style.height) || 120; n.style.position = "absolute"; });
    tl.fromTo(st, { t: 0 }, { t: t1 - t0, duration: Math.max(0.1, t1 - t0), ease: "none", onUpdate: place }, t0);
    place();
    return ring;
  };
  /** TweetCard-style card (used for messages and comments) */
  ST.tweet = (parent, x, y, d, t) => {
    const el = h("div", "st-tweet", { left: px(x), top: px(y) }, `<div class="hd"><div class="av" style="${d.avatar ? `background-image:url(${d.avatar})` : `background:${d.avbg || "#141414"}`}">${d.avicon || ""}</div><div><div class="nm">${d.name}</div><div class="hn">${d.handle || ""}</div></div><div style="margin-left:auto">${d.badge || ""}</div></div><div class="bd"></div>`, parent);
    ENTER.rise(el, t);
    return el;
  };
  /** smooth cursor (macOS arrow) gliding between keys, tilting into the move, pressing on click */
  ST.cursor = (parent, keys) => {
    const el = h("div", null, { position: "absolute", left: "0", top: "0", zIndex: 30, transformOrigin: "6px 4px", filter: "drop-shadow(0 4px 8px rgba(0,0,0,.35))" }, `<svg width="44" height="52" viewBox="0 0 22 26"><path d="M2 1.5 L2 20.5 L7 16 L10.5 24 L13.6 22.6 L10.2 14.8 L17 14.8 Z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>`, parent);
    keys.forEach((k, i) => {
      if (i === 0) { tl.set(el, { x: k.x, y: k.y, opacity: 0 }, 0); tl.to(el, { opacity: 1, duration: 0.2 }, k.t); return; }
      const p = keys[i - 1], d = Math.max(0.35, k.dur || 0.8);
      const tilt = Math.max(-14, Math.min(14, (k.x - p.x) / 40));
      tl.to(el, { x: k.x, y: k.y, ...sp(1, d * 0.9) }, k.t - d);
      tl.to(el, { keyframes: [{ rotation: tilt, duration: d * 0.4, ease: "power2.out" }, { rotation: 0, duration: d * 0.6, ease: "power2.inOut" }] }, k.t - d);
      if (k.click) { tl.to(el, { keyframes: [{ scale: 0.82, duration: 0.08 }, { scale: 1, ...AP }] }, k.t); const ring = h("div", null, { position: "absolute", left: px(k.x - 26), top: px(k.y - 26), width: "52px", height: "52px", borderRadius: "50%", border: "3px solid rgba(255,255,255,.9)", opacity: 0 }, null, parent); tl.fromTo(ring, { scale: 0.3, opacity: 0.9 }, { scale: 1.6, opacity: 0, duration: 0.5, ease: "power2.out" }, k.t); }
    });
    return el;
  };

  // ------------------------------------------------------------- text animations (ported)
  const wordSpans = (el, text, cls) => text.split(" ").map((w, i, a) => h("span", "st-w " + (cls || ""), {}, w + (i < a.length - 1 ? " " : ""), el));
  /** TypingAnimation: 100 ms a character by default, blinking line cursor */
  ST.type = (el, text, t, o = {}) => {
    const out = h("span", null, {}, "", el), cur = h("span", "st-cursor", {}, "", el);
    const per = o.per ?? 0.1, d = text.length * per, st = { n: 0 };
    const upd = () => (out.textContent = text.slice(0, Math.round(st.n)));
    tl.to(st, { n: text.length, duration: d, ease: "none", onUpdate: upd }, t);
    tl.set({}, { onUpdate: upd }, t + d + 0.01);
    const end = o.until ?? t + d + 1.6;
    for (let k = t + d; k < end; k += 1) { tl.set(cur, { opacity: 0 }, k + 0.5); tl.set(cur, { opacity: 1 }, k + 1); }
    if (o.hideCursor !== false) tl.set(cur, { opacity: 0 }, end);
    return out;
  };
  /** WordRotate: words[i] shows from times[i]; out up, in from below, 0.25 s ease-out */
  ST.rotate = (el, words, times, o = {}) => {
    // all words stacked in one grid cell: the box is as wide as the longest word (nothing cropped sideways),
    // each word centred, and the box clips only top and bottom so words slide in and out of a slot
    const box = h("span", null, { display: "inline-grid", verticalAlign: "bottom", clipPath: "inset(-0.02em -50vw -0.02em -50vw)", padding: "0.06em 0" }, null, el);
    const spans = words.map((w, i) => h("span", o.cls ? o.cls[i] || "" : "", { gridArea: "1 / 1", justifySelf: o.align || "center", whiteSpace: "nowrap" }, w, box));
    spans.forEach((s, i) => {
      tl.set(s, { opacity: 0 }, 0);
      tl.fromTo(s, { yPercent: 60, opacity: 0, filter: "blur(4px)" }, { yPercent: 0, opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power1.out" }, times[i]);
      if (i < words.length - 1) tl.to(s, { yPercent: -60, opacity: 0, filter: "blur(4px)", duration: 0.25, ease: "power1.out" }, times[i + 1]);
    });
    return box;
  };
  /** MorphingText (magicui): two layers through a threshold filter */
  const goo = h("div", null, { position: "absolute", width: "0", height: "0", overflow: "hidden" }, `<svg width="0" height="0"><defs><filter id="st-threshold"><feColorMatrix in="SourceGraphic" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 255 -140"/></filter></defs></svg>`);
  ST.morph = (el, words, times, o = {}) => {
    const box = h("div", null, { position: "relative", filter: "url(#st-threshold) blur(0.6px)", whiteSpace: "nowrap", height: "1.1em" }, null, el);
    const lay = words.map((w, i) => h("span", (o.cls && o.cls[i]) || "", { position: "absolute", left: "0", right: "0", top: "0", textAlign: o.align || "center", opacity: 0 }, w, box));
    const mt = o.morphTime ?? 1.5;
    tl.set(lay[0], { opacity: 1, filter: "blur(0px)" }, times[0]);
    for (let i = 1; i < words.length; i++) {
      const a = lay[i - 1], b = lay[i], st = { f: 0 };
      const upd = () => { const f = Math.max(1e-4, Math.min(1, st.f)), g = Math.max(1e-4, 1 - f); b.style.filter = `blur(${Math.min(8 / f - 8, 100)}px)`; b.style.opacity = Math.pow(f, 0.4); a.style.filter = `blur(${Math.min(8 / g - 8, 100)}px)`; a.style.opacity = Math.pow(g, 0.4); };
      tl.fromTo(st, { f: 0 }, { f: 1, duration: mt, ease: "none", onUpdate: upd }, times[i] - mt * 0.5);
    }
    return box;
  };
  /** Text3DFlip: letters turn in from rotateY(90deg) */
  ST.flip = (el, text, t, o = {}) => {
    const box = h("span", null, { display: "inline-block", perspective: "900px", whiteSpace: "nowrap" }, null, el);
    [...text].forEach((c, i) => {
      const s = h("span", null, { display: "inline-block", transformOrigin: "50% 50% -0.3em", backfaceVisibility: "hidden" }, c === " " ? "&nbsp;" : c, box);
      tl.set(s, { opacity: 0 }, 0);
      const k = o.from === "center" ? Math.abs(i - (text.length - 1) / 2) : i;
      tl.fromTo(s, { rotationY: 90, opacity: 0 }, { rotationY: 0, opacity: 1, ...FLIPSP }, t + k * (o.stagger ?? 0.05));
    });
    return box;
  };
  /** DiaTextReveal: a colour band sweeps across and leaves the text solid */
  ST.dia = (el, text, t, o = {}) => {
    const s = h("span", null, { display: "inline-block", whiteSpace: "nowrap", WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent" }, text, el);
    const cols = o.colors || ["#c679c4", "#fa3d1d", "#ffb005", "#e1e1fe", "#0358f7"], solid = o.color || "#141414", st = { p: 0 };
    const ease = (x) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
    const upd = () => { const pos = -17 + ease(st.p) * 134, a = pos - 17, b = pos + 17, parts = []; if (a > 0) parts.push(`${solid} 0%`, `${solid} ${a.toFixed(2)}%`); cols.forEach((c, i) => parts.push(`${c} ${(a + (i / (cols.length - 1)) * 34).toFixed(2)}%`)); if (b < 100) parts.push(`transparent ${b.toFixed(2)}%`, "transparent 100%"); s.style.backgroundImage = `linear-gradient(90deg, ${parts.join(", ")})`; };
    tl.fromTo(st, { p: 0 }, { p: 1, duration: o.dur ?? 1.5, ease: "none", onUpdate: upd }, t);
    tl.set(s, { backgroundImage: `linear-gradient(90deg, ${solid}, ${solid})` }, t + (o.dur ?? 1.5) + 0.01);
    st.p = 0; upd();
    return s;
  };
  /** Highlighter: hand-drawn annotation around a span (rough-notation style), two strokes */
  ST.hl = (span, t, o = {}) => {
    const a = o.action || "underline", col = o.color || "#E36A3A", sw = o.stroke || 5, dur = o.dur ?? 0.6, pad = o.pad ?? 6;
    span.style.position = "relative"; span.style.display = "inline-block";
    if (a === "highlight") {
      const m = h("span", null, { position: "absolute", left: -pad + "px", right: -pad + "px", top: "12%", bottom: "4%", background: col, zIndex: -1, transformOrigin: "0 50%", borderRadius: "6px" }, null, span);
      span.style.zIndex = 0; span.style.isolation = "isolate";
      tl.fromTo(m, { scaleX: 0 }, { scaleX: 1, duration: dur, ease: "power2.inOut" }, t);
      return m;
    }
    const j = (k, s = 2) => ((hash(k, Math.floor(t * 10)) - 0.5) * s).toFixed(2);
    let d = "";
    for (let it = 0; it < 2; it++) {
      if (a === "underline") d += `M${-2 + +j(it)} ${102 + +j(it + 3)} Q 50 ${99 + +j(it + 5, 4)} ${102 + +j(it + 7)} ${103 + +j(it + 9)} `;
      if (a === "strike") d += `M-3 ${52 + +j(it)} Q 50 ${48 + +j(it + 2, 4)} 103 ${51 + +j(it + 4)} `;
      if (a === "box") d += `M${-4 + +j(it)} ${-6 + +j(it + 1)} L${104 + +j(it + 2)} ${-5 + +j(it + 3)} L${103 + +j(it + 4)} ${106 + +j(it + 5)} L${-3 + +j(it + 6)} ${105 + +j(it + 7)} Z `;
      if (a === "circle") d += `M50 ${-12 + +j(it)} C ${118 + +j(it + 1, 6)} ${-14} ${120} ${112} 50 ${113 + +j(it + 2)} C ${-20} ${114} ${-22 + +j(it + 3, 6)} ${-10} ${56} ${-9 + +j(it + 4)} `;
      if (a === "cross") d += `M-2 -4 L102 104 M102 -4 L-2 104 `;
    }
    const sv = h("span", null, { position: "absolute", left: -pad + "px", top: -pad + "px", right: -pad + "px", bottom: -pad + "px", pointerEvents: "none", overflow: "visible" }, `<svg viewBox="0 0 100 100" preserveAspectRatio="none" width="100%" height="100%" style="overflow:visible"><path d="${d}" pathLength="1" fill="none" stroke="${col}" stroke-width="${sw}" stroke-linecap="round" stroke-linejoin="round" vector-effect="non-scaling-stroke" style="stroke-dasharray:1;stroke-dashoffset:1"/></svg>`, span);
    // hidden until drawn: with a thick round-capped stroke the caps of an undrawn dash still show as stubs
    const pth = sv.querySelector("path");
    pth.style.strokeDasharray = "1 2";
    tl.set(sv, { opacity: 0 }, 0); tl.set(sv, { opacity: 1 }, t);
    tl.fromTo(pth, { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: dur, ease: "power1.inOut" }, t);
    return sv;
  };
  /** odometer number; digits roll into place right to left */
  ST.odo = (parent, text, t, o = {}) => {
    const el = h("div", "st-odo " + (o.cls || ""), { left: px(o.x ?? 960), top: px(o.y ?? 400), fontSize: px(o.size || 200), color: o.color || "#141414" }, null, parent);
    if (o.center !== false) gsap.set(el, { xPercent: -50 });
    const chars = [...text], nd = chars.filter((c) => /\d/.test(c)).length; let k = 0;
    chars.forEach((c) => {
      if (!/\d/.test(c)) { h("span", "sep", {}, c, el); return; }
      const col = h("span", "col", {}, null, el);
      const strip = h("span", "strip", {}, Array.from({ length: 20 }, (_, i) => `<i>${i % 10}</i>`).join(""), col);
      const tt = t + (nd - 1 - k++) * (o.stagger ?? 0.06);
      tl.set(strip, { yPercent: 0 }, 0);
      tl.fromTo(strip, { yPercent: 0 }, { yPercent: -((10 + +c) / 20) * 100, duration: o.dur || 1.4, ease: "expo.out" }, tt);
    });
    tl.set(el, { opacity: 0 }, 0); tl.to(el, { opacity: 1, duration: 0.15 }, t);
    return el;
  };
  /** words that land one by one (Kinetic Text Reveal: rise 20 px in a mask from blur 6 px, 0.72 s) */
  ST.kinetic = (el, text, times, o = {}) => {
    wordSpans(el, text).forEach((s, i) => {
      const m = h("span", null, { display: "inline-block", overflow: "hidden", verticalAlign: "bottom", paddingBottom: "0.08em", marginBottom: "-0.08em" }, null, el);
      m.appendChild(s);
      if (o.serif && o.serif.includes(i)) s.classList.add("st-serif"), (s.style.color = o.serifColor || "#E36A3A");
      const tt = Array.isArray(times) ? times[Math.min(i, times.length - 1)] : times + i * 0.075;
      tl.set(s, { opacity: 0 }, 0);
      tl.fromTo(s, { yPercent: 70, opacity: 0, filter: "blur(6px)" }, { yPercent: 0, opacity: 1, filter: "blur(0px)", duration: 0.72, ease: "expo.out" }, tt);
    });
    return el;
  };

  // ------------------------------------------------------------- text-design title stacks (user's text reference)
  /** grain + dark backdrop used by the title stacks */
  ST.grain = (parent) => h("div", "st-grain", {}, `<svg width="100%" height="100%"><filter id="stn"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/></filter><rect width="100%" height="100%" filter="url(#stn)"/></svg>`, parent);
  const stamp = (el, t, from = 1.5) => { tl.set(el, { opacity: 0 }, 0); tl.fromTo(el, { scale: from, opacity: 0, filter: "blur(8px)" }, { scale: 1, opacity: 1, filter: "blur(0px)", duration: 0.32, ease: "power4.out" }, t); };
  const draw = (el, t, d = 0.45) => { tl.set(el, { opacity: 0 }, 0); tl.set(el, { opacity: 1 }, t); tl.fromTo(el, { clipPath: "inset(0% 100% 0% 0%)" }, { clipPath: "inset(0% 0% 0% 0%)", duration: d, ease: "power2.inOut" }, t); };
  /** variant A "No HOOK, no VIEWS": hand-circled script kicker, white box word, red box word, neon script over it */
  ST.titleA = (parent, cx, cy, s, d, t) => {
    const g = h("div", "st-t", { left: px(cx), top: px(cy) }, null, parent); gsap.set(g, { xPercent: -50, yPercent: -50 });
    const k = h("div", "st-script", { fontSize: px(s * 0.42), color: "#fff", position: "relative", display: "inline-block", padding: "0 .4em" }, d.kicker, g);
    h("br", null, null, null, g);
    const sv = h("span", null, { position: "absolute", inset: "-14% -6%" }, `<svg viewBox="0 0 100 100" preserveAspectRatio="none" width="100%" height="100%" style="overflow:visible"><path d="M50 4 C 96 2 104 92 50 96 C -2 99 -4 8 58 6" pathLength="1" fill="none" stroke="#E2402F" stroke-width="3" vector-effect="non-scaling-stroke" style="stroke-dasharray:1;stroke-dashoffset:1"/></svg>`, k);
    const b1 = h("div", "st-anton st-tag", { fontSize: px(s), background: "#F4F4F4", color: "#E2402F", marginTop: px(s * 0.1), transform: "rotate(-2deg)" }, d.big1, g);
    h("br", null, null, null, g);
    const b2 = h("div", "st-anton st-tag", { fontSize: px(s * 0.82), background: "#E2402F", color: "#F4F4F4", marginTop: px(-s * 0.08), transform: "rotate(2deg)" }, d.big2, g);
    const neon = h("div", "st-script st-neon", { position: "absolute", left: px(-s * 0.55), top: px(s * 0.62), fontSize: px(s * 0.8), transform: "rotate(-12deg)" }, d.neon || "", g);
    M.wordIn(k, t); tl.fromTo(sv.querySelector("path"), { strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.5, ease: "power1.inOut" }, t + 0.15);
    stamp(b1, d.t1 ?? t + 0.35); stamp(b2, d.t2 ?? t + 0.6);
    if (d.neon) { draw(neon, d.tn ?? t + 0.8, 0.4); tl.fromTo(neon, { opacity: 0.3 }, { keyframes: [{ opacity: 1, duration: 0.05 }, { opacity: 0.4, duration: 0.05 }, { opacity: 1, duration: 0.06 }] }, (d.tn ?? t + 0.8) + 0.4); }
    return g;
  };
  /** variant B "TOO SLOW / PEOPLE SCROLL / START FASTER": italic kicker with lime swash, huge lime + halftone white, lime tag */
  ST.titleB = (parent, cx, cy, s, d, t) => {
    const g = h("div", "st-t", { left: px(cx), top: px(cy) }, null, parent); gsap.set(g, { xPercent: -50, yPercent: -50 });
    const k = h("div", "st-anton", { fontSize: px(s * 0.42), color: "#fff", fontStyle: "italic", display: "inline-block", position: "relative" }, d.kicker, g);
    const sw = h("span", null, { position: "absolute", left: "8%", right: "8%", bottom: "-0.18em", height: "0.09em", background: "#D4F25A", borderRadius: "999px", transformOrigin: "0 50%" }, null, k);
    const b1 = h("div", "st-anton", { fontSize: px(s), color: "#D4F25A", marginTop: px(s * 0.12) }, d.big1, g);
    const b2 = h("div", "st-anton", { fontSize: px(s), color: "#F4F4F4" }, d.big2, g);
    const tag = h("div", "st-anton st-tag", { fontSize: px(s * 0.34), background: "#D4F25A", color: "#141414", fontStyle: "italic", marginTop: px(s * 0.14), borderRadius: "4px" }, d.tag || "", g);
    M.wordIn(k, t); tl.fromTo(sw, { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power2.out" }, t + 0.2);
    tl.set([b1, b2], { opacity: 0 }, 0);
    tl.fromTo(b1, { opacity: 0, y: 40, scaleY: 1.3 }, { opacity: 1, y: 0, scaleY: 1, duration: 0.42, ease: "expo.out" }, d.t1 ?? t + 0.3);
    tl.fromTo(b2, { opacity: 0, y: 40, scaleY: 1.3 }, { opacity: 1, y: 0, scaleY: 1, duration: 0.42, ease: "expo.out" }, d.t2 ?? t + 0.5);
    if (d.tag) stamp(tag, d.tt ?? t + 0.8, 0.6); else tag.remove();
    return g;
  };
  /** variant C "FOCUS / ON HOOK / NOT / DESIGN": spaced kicker, big serif caps, spaced small, lime box serif italic, drawn arrow */
  ST.titleC = (parent, cx, cy, s, d, t) => {
    const g = h("div", "st-t", { left: px(cx), top: px(cy) }, null, parent); gsap.set(g, { xPercent: -50, yPercent: -50 });
    const k = h("div", "st-spaced", { color: "#fff", fontSize: px(s * 0.28) }, d.kicker, g);
    const b1 = h("div", "st-serifup", { fontSize: px(s), color: "#F4F4F4", marginTop: px(s * 0.06) }, d.big1, g);
    const k2 = h("div", "st-spaced", { color: "#fff", fontSize: px(s * 0.26), marginTop: px(s * 0.1) }, d.small || "", g);
    const box = h("div", "st-serif st-tag", { fontSize: px(s * 0.9), background: "#D4F25A", color: "#141414", marginTop: px(s * 0.08), padding: "0 .3em", borderRadius: "2px", transform: "rotate(-1.5deg)" }, d.box, g);
    M.wordIn(k, t); tl.set(b1, { opacity: 0 }, 0); tl.fromTo(b1, { opacity: 0, letterSpacing: "0.3em", filter: "blur(8px)" }, { opacity: 1, letterSpacing: "-0.01em", filter: "blur(0px)", duration: 0.7, ease: "expo.out" }, d.t1 ?? t + 0.25);
    if (d.small) M.wordIn(k2, (d.t1 ?? t + 0.25) + 0.3); else k2.remove();
    tl.set(box, { opacity: 0 }, 0); tl.fromTo(box, { opacity: 0, clipPath: "inset(0% 50% 0% 50%)" }, { opacity: 1, clipPath: "inset(0% 0% 0% 0%)", duration: 0.45, ease: "expo.out" }, d.t2 ?? t + 0.7);
    return g;
  };
  /** variant D "DON'T MAKE THEM / THINK / KEEP IT SIMPLE / Feel.": gradient giant word, overlapping white tag, gradient script */
  ST.titleD = (parent, cx, cy, s, d, t) => {
    const g = h("div", "st-t", { left: px(cx), top: px(cy) }, null, parent); gsap.set(g, { xPercent: -50, yPercent: -50 });
    const k = h("div", "st-anton", { fontSize: px(s * 0.42), color: "#F4F4F4" }, d.kicker, g);
    const big = h("div", "st-anton", { fontSize: px(s * 1.25), lineHeight: "0.86", backgroundImage: "linear-gradient(180deg, #F472B6 0%, #C026D3 55%, #7C3AED 100%)", WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent", position: "relative" }, d.big, g);
    const tag = h("div", "st-anton st-tag", { position: "relative", fontSize: px(s * 0.3), background: "#F4F4F4", color: "#141414", marginTop: px(-s * 0.62), borderRadius: "3px", transform: "rotate(-3deg)" }, d.tag || "", g);
    const sc = h("div", "st-script", { fontSize: px(s * 0.95), marginTop: px(s * 0.35), backgroundImage: "linear-gradient(90deg, #FDE047, #F97316)", WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent", transform: "rotate(-6deg)", display: "inline-block", padding: "0 .2em" }, d.script || "", g);
    M.wordIn(k, t);
    tl.set(big, { opacity: 0 }, 0); tl.fromTo(big, { opacity: 0, scale: 0.7, filter: "blur(14px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", ...AP }, d.t1 ?? t + 0.3);
    if (d.tag) stamp(tag, d.tt ?? t + 0.65, 1.8); else tag.remove();
    if (d.script) draw(sc, d.ts ?? t + 0.9, 0.5); else sc.remove();
    return g;
  };
  /** a dark title backdrop (grain) on a stage element */
  ST.titleBG = (el) => { el.style.background = "radial-gradient(120% 90% at 50% 40%, #24212E 0%, #16141C 60%, #0F0E13 100%)"; ST.grain(el); };

  /** module header (course ref): "06 —— MODULE TWO" and a segmented progress bar */
  ST.module = (parent, w, hh, n, total, label, t, o = {}) => {
    const k = h("div", "st-kick", { left: "72px", top: "64px", color: o.color || "#fff" }, `<span class="n">${String(n).padStart(2, "0")}</span><span class="bar"></span>`, parent);
    const r = h("div", "st-kick", { right: "72px", top: "80px", color: o.color || "#fff", fontSize: "22px", opacity: 0.8 }, label, parent);
    const seg = h("div", "st-seg", { left: "72px", right: "72px", bottom: "56px" }, Array.from({ length: total }, (_, i) => `<i style="flex:1" class="${i === n - 1 ? "on" : ""}"></i>`).join(""), parent);
    M.wordIn(k, t); M.wordIn(r, t + 0.1);
    tl.fromTo(seg, { opacity: 0 }, { opacity: 1, duration: 0.4 }, t + 0.15);
    tl.fromTo(seg.querySelector(".on"), { scaleX: 0, transformOrigin: "0 50%" }, { scaleX: 1, duration: 0.6, ease: "power2.out" }, t + 0.3);
    return { k, r, seg };
  };
  ST.out = (el, t, kind = "fade") => EXIT[kind](el, t);

  // ------------------------------------------------------------- event log for sound design
  // Every component records when it does something visible (kind, time, a short label, x for panning),
  // so the sound plan (tools/director/sfx_plan.py) is placed on what is actually on screen, not guessed.
  ST.events = [];
  const ev = (kind, t, label, x) => { if (typeof t === "number" && isFinite(t)) ST.events.push({ kind, t: +t.toFixed(3), label: String(label || "").slice(0, 40), x: x == null ? null : Math.round(x) }); };
  const wrap = (obj, name, fn) => { const f0 = obj[name]; obj[name] = function (...a) { try { fn(...a); } catch (e) {} return f0.apply(this, a); }; };
  const txt = (v) => (Array.isArray(v) ? v.join(" / ") : v);
  wrap(ST, "odo", (p, text, t, o = {}) => ev("number", t, text, o.x));
  wrap(ST, "flip", (el, text, t) => ev("bigword", t, text));
  wrap(ST, "kinetic", (el, text, times) => ev("bigword", Array.isArray(times) ? times[0] : times, text));
  wrap(ST, "morph", (el, words, times) => times.forEach((t, i) => ev(i ? "morph" : "bigword", t, words[i])));
  wrap(ST, "rotate", (el, words, times) => times.forEach((t, i) => ev(i ? "morph" : "bigword", t, words[i])));
  wrap(ST, "type", (el, text, t, o = {}) => ev("type", t, text, null) || ST.events.push({ kind: "typeEnd", t: +(Math.min(o.until ?? 1e9, t + (o.per ?? 0.1) * text.length)).toFixed(3), label: "", x: null }));
  wrap(ST, "pill", (p, x, y, text, t) => ev("pill", t, text.replace(/<[^>]+>/g, ""), x));
  wrap(ST, "hl", (span, t, o = {}) => ev("mark", t, o.action || "underline"));
  wrap(ST, "icon3d", (p, name, x, y, size, t) => ev("icon", t, name, x));
  wrap(ST, "app", (p, name, x, y, size, t) => ev("icon", t, name, x));
  wrap(ST, "iphone", (p, x, y, hh, t) => ev("device", t, "iphone", x));
  wrap(ST, "safari", (p, x, y, w, hh, cap, t) => ev("device", t, "safari", x));
  wrap(ST, "tweet", (p, x, y, d, t) => ev("card", t, d && d.name, x));
  wrap(ST, "list", (p, x, y, w, items) => items.forEach((it) => ev("listitem", it.t, it.title, x)));
  wrap(ST, "cursor", (p, keys) => keys.forEach((k) => k.click && ev("click", k.t, "click", k.x)));
  wrap(ST, "dia", (el, text, t) => ev("bigword", t, text));
  for (const n of ["titleA", "titleB", "titleC", "titleD"]) wrap(ST, n, (p, cx, cy, s, d, t) => { ev("title", d.t1 ?? t, d.big1 || d.big || n); if (d.t2) ev("title2", d.t2, d.big2 || d.box || ""); if (d.tn) ev("title2", d.tn, d.neon || ""); if (d.tt) ev("title2", d.tt, d.tag || ""); if (d.ts) ev("title2", d.ts, d.script || ""); });
  wrap(D, "shake", (t, amp) => ev("shake", t, amp));
  wrap(D, "punch", (t) => ev("punch", t, ""));
  wrap(D, "mark", (br, b, t, o = {}) => ev("mark", t, o.label || "mark"));
  wrap(D, "island", (p, o) => { ev("island", o.show, "show"); if (o.clockAt) ev("islandClock", o.clockAt, ""); });
  const f0 = ST.finish; ST.finish = (...a) => { const r = f0(...a); window.__ST_EVENTS = { events: ST.events, frames: ST.frames.map((f) => ({ t0: f.t0, t1: f.t1, kind: f.kind, dark: !!f.dark })), insert: D.cfg.insert, total: D.cfg.total }; return r; };
})();
