// Dump what happens on screen and when (for the sound plan): node tools/director/events.mjs <project dir> <out.json>
import { createRequire } from "module";
import path from "path";
import fs from "fs";
const dir = path.resolve(process.argv[2]);
const require = createRequire(path.join(dir, "package.json"));
const puppeteer = require("puppeteer-core");
const b = await puppeteer.launch({ executablePath: process.env.CHROME || "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: true, args: ["--allow-file-access-from-files"] });
const p = await b.newPage();
const errs = []; p.on("pageerror", (e) => errs.push(e.message));
await p.evaluateOnNewDocument(() => { window.__timelines = {}; });
await p.goto("file://" + path.join(dir, "index.html"), { waitUntil: "load" });
await p.evaluate(() => window.__DIRECTOR && window.__DIRECTOR.ready);
const r = await p.evaluate(() => ({ ev: window.__ST_EVENTS, spk: window.__DIRECTOR.spk, cuts: window.__DIRECTOR.cutouts, sfx: window.__DIRECTOR.sfx }));
await b.close();
if (errs.length || !r.ev) { console.error("page errors:", errs); process.exit(1); }
const out = { ...r.ev, spk: r.spk, cuts: r.cuts, cues: r.sfx };
out.events.sort((a, b) => a.t - b.t);
fs.writeFileSync(process.argv[3], JSON.stringify(out, null, 1));
const c = {}; for (const e of out.events) c[e.kind] = (c[e.kind] || 0) + 1;
console.log(out.events.length, "events", JSON.stringify(c), "frames", out.frames.length, "cuts", out.cuts.length);
