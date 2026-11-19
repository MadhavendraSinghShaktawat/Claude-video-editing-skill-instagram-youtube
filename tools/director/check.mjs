// Load the built page headless and report: phrases D.at could not find, icon misses, JS errors,
// and the sound cues. Usage: node tools/director/check.mjs <project dir> [chrome path]
import { createRequire } from "module";
import path from "path";
const dir = path.resolve(process.argv[2]);
const require = createRequire(path.join(dir, "package.json"));
const puppeteer = require("puppeteer-core");
const exe = process.argv[3] || process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const b = await puppeteer.launch({ executablePath: exe, headless: true, args: ["--allow-file-access-from-files"] });
const p = await b.newPage();
const logs = [];
p.on("console", (m) => { const t = m.text(); if (/not found|missing|Error/i.test(t)) logs.push(t); });
p.on("pageerror", (e) => logs.push("PAGE ERROR: " + e.message));
await p.evaluateOnNewDocument(() => { window.__timelines = {}; });
await p.goto("file://" + path.join(dir, "index.html"), { waitUntil: "load" });
await p.evaluate(() => window.__DIRECTOR && window.__DIRECTOR.ready);
const r = await p.evaluate(() => ({ dir: window.__DIRECTOR, dur: window.__timelines.main && window.__timelines.main.duration() }));
const d = r.dir || {};
console.log(JSON.stringify({ duration: r.dur, missing: d.missing, cues: d.sfx && d.sfx.length, logs: [...new Set(logs)] }, null, 1));
// phrases whose first occurrence is earlier than the one used (search started at the scene): check them
if (d.atLog && d.atLog.length) { console.log("phrases also said earlier (the later one was used):"); for (const a of d.atLog) console.log(`  ${a.phrase.padEnd(34)} first ${a.first}  used ${a.used}`); }
// text that had to shrink to fit its box
if (d.fit && d.fit.length) { console.log("text shrunk to fit its box:"); for (const f of d.fit) console.log(`  ${String(f.scale).padEnd(5)} ${f.text}`); }
// a script error means the page below is not the edit: say so loudly and stop (no "all clear" on a broken page)
if (logs.some((l) => l.startsWith("PAGE ERROR"))) { console.error("\nPAGE ERROR in the plan or theme: fix it before trusting any other result (node --check <file> finds it)"); await b.close(); process.exit(1); }
// layout scan: seek every 0.5 s and find text that is cropped (by the frame or by a panel that clips it) or
// that sits on the speaker's card / picture-in-picture. Cutout scenes are skipped for the speaker test,
// since words behind the cut-out person are meant to be there.
const scan = await p.evaluate(() => {
  const tl = window.__timelines.main, out = {}, W = 1920, H = 1080;
  const cuts = (window.__DIRECTOR.cutouts || []).map((c) => [c.t0, c.t1]);
  const shadow = document.querySelector(".spkshadow");
  const vis = (e) => { let o = 1; for (let n = e; n && n !== document.body; n = n.parentElement) { const cs = getComputedStyle(n); if (cs.display === "none" || cs.visibility === "hidden") return 0; o *= +cs.opacity; if (o < 0.5) return 0; } return o; };
  const texts = [...document.querySelectorAll(".layer *")].filter((e) => !e.closest(".spkwin,.spkshadow,.st-cutwrap") && [...e.childNodes].some((n) => n.nodeType === 3 && n.textContent.trim().length > 1));
  const clipAnc = (e) => { const r = []; for (let n = e.parentElement; n && !n.classList.contains("layer"); n = n.parentElement) { const cs = getComputedStyle(n); if (cs.overflow === "hidden" || cs.clipPath !== "none") r.push(n); } return r; };
  const anc = new Map(texts.map((e) => [e, clipAnc(e)]));
  for (let t = 0.25; t < tl.duration(); t += 0.5) {
    tl.seek(t, true);
    const inCut = cuts.some(([a, b]) => t >= a && t < b);
    let card = null;
    if (!inCut && shadow && vis(shadow)) { const r = shadow.getBoundingClientRect(); if (r.width > 40 && r.width < W - 10) card = r; }
    for (const e of texts) {
      // the glyphs, not the element box (a full-width centred title box is wider than its words)
      const rg = document.createRange(); rg.selectNodeContents(e); const r = rg.getBoundingClientRect(); if (r.width < 4 || r.height < 4) continue;
      if (!vis(e)) continue;
      const key = e.textContent.trim().slice(0, 40); const why = [];
      // a line box is taller than the ink (ascent/descent): allow ~0.2 em above and below before calling it cropped
      const v = 0.2 * parseFloat(getComputedStyle(e).fontSize) * (r.height / Math.max(1, e.offsetHeight || r.height));
      if (r.left < -2 || r.top < -v || r.right > W + 2 || r.bottom > H + v) why.push("off frame");
      for (const a of anc.get(e)) { const q = a.getBoundingClientRect(); if (q.width > 2 && (r.left < q.left - 2 || r.right > q.right + 2 || r.top < q.top - v || r.bottom > q.bottom + v)) { why.push("cropped by its box"); break; } }
      if (card && r.right > card.left + 4 && r.left < card.right - 4 && r.bottom > card.top + 4 && r.top < card.bottom - 4) why.push("on the speaker");
      for (const w of why) { const k = w + " | " + key; if (!out[k]) out[k] = { why: w, text: key, first: +t.toFixed(2), n: 0 }; out[k].n++; }
    }
  }
  // panels that stay empty after their entrance (nothing but their background on screen)
  for (const f of (window.ST && window.ST.frames) || []) {
    if (!f.p) continue;
    const kids = [...f.p.querySelectorAll("*")].filter((e) => e.tagName !== "CANVAS" && !e.classList.contains("st-grain") && !e.closest("svg defs"));
    let first = null;
    for (let t = f.t0 + 0.5; t < f.t1; t += 0.25) {
      tl.seek(t, true);
      if (kids.some((e) => { const r = e.getBoundingClientRect(); return r.width > 12 && r.height > 12 && vis(e); })) { first = t; break; }
    }
    const empty = (first ?? f.t1) - f.t0;
    if (empty > 1.2) out["empty|" + f.t0] = { why: "empty panel", text: `${f.kind} ${empty.toFixed(1)} s before anything shows ${f.src || ""}`, first: +f.t0.toFixed(2), n: Math.round(empty * 2) };
  }
  tl.seek(0, true);
  return Object.values(out).sort((a, b) => a.first - b.first);
});
const trims = await p.evaluate(() => ((window.ST && window.ST.frames) || []).filter((f) => f.trimmed).map((f) => `${f.t1.toFixed(1)} (-${f.trimmed}s) ${f.kind} ${f.src || ""}`));
if (trims.length) console.log("panels ended early because nothing new arrived (speaker takes the frame back):\n  " + trims.join("\n  "));
if (scan.length) { console.log("layout problems (first time seen, seconds visible x0.5):"); for (const s of scan) console.log(`  ${String(s.first).padStart(7)}  ${s.why.padEnd(19)} ${String(s.n).padStart(3)}  ${s.text}`); }
else console.log("layout scan: no cropped text, nothing on the speaker");
if (r.dir) (await import("fs")).writeFileSync(path.join(dir, "cues.json"), JSON.stringify(r.dir.sfx));
if (r.dir && r.dir.cutouts) (await import("fs")).writeFileSync(path.join(dir, "cutouts.json"), JSON.stringify(r.dir.cutouts));
await b.close();
