// Capture high-res screenshots + element bounding boxes for the video edit.
// Usage: node capture.js pages.json out_dir [name ...]   (no names = all pages)
const puppeteer = require('puppeteer-core');
const fs = require('fs');
const path = require('path');
const extractors = require('./extractors');

const OUT = path.resolve(process.argv[3] || 'captures');
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const VW = 1600, VH = 1000, DPR = 2;
// Pages come from a JSON file: [{"name", "url", "mode": "full"|"viewport", "cap": css px, "ex": extractor, "scrollTo"?}]
// extractors (extractors.js): ytShorts, ytHeader, ghRepo, ghFolder, ghMarkdown, ghHyper, remotion, generic
const PAGES = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// CSS that hides overlays which are not part of the page itself.
const HIDE_CSS = `
  /* YouTube */
  ytd-guide-signin-promo-renderer,
  tp-yt-iron-dropdown, ytd-popup-container > *:not(ytd-multi-page-menu-renderer[hidden]),
  ytd-consent-bump-v2-lightbox, #consent-bump, yt-mealbar-promo-renderer,
  tp-yt-paper-toast, yt-notification-action-renderer, ytd-enforcement-message-view-model,
  ytd-tooltip, tp-yt-paper-tooltip, #tooltip.tp-yt-paper-tooltip, yt-tooltip-renderer,
  ytd-statement-banner-renderer, ytd-banner-promo-renderer, #masthead-ad,
  /* GitHub */
  .js-signup-prompt, .signup-prompt, .signup-prompt-bg, [data-testid="signup-banner"],
  .js-cookie-consent-banner, #ghcc, cookie-consent-banner, [class*="CookieBanner"],
  .Toast, [data-target="toast-container"],
  /* generic */
  #onetrust-banner-sdk, #onetrust-consent-sdk, .cc-window, .cookie-banner, [id*="cookie-banner"],
  [class*="cookieConsent"], [aria-label="cookieconsent"]
  { display: none !important; visibility: hidden !important; }
  * { caret-color: transparent !important; }
`;

async function dismissDialogs(page) {
  // Click common accept/dismiss buttons (no logins).
  await page.evaluate(() => {
    const words = ['accept all', 'accept', 'i agree', 'agree', 'got it', 'allow all', 'no thanks', 'dismiss', 'close', 'ok'];
    const btns = [...document.querySelectorAll('button, [role="button"], a.button')];
    for (const b of btns) {
      const t = (b.innerText || b.getAttribute('aria-label') || '').trim().toLowerCase();
      if (!t || t.length > 30) continue;
      const r = b.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      const inDialog = b.closest('[role="dialog"], dialog, tp-yt-paper-dialog, ytd-consent-bump-v2-lightbox, #onetrust-banner-sdk, .cookie, [class*="cookie" i], [class*="consent" i]');
      if (inDialog && words.includes(t)) { b.click(); }
    }
  });
}

async function waitImages(page, timeout = 20000) {
  const t0 = Date.now();
  while (Date.now() - t0 < timeout) {
    const pending = await page.evaluate(() => {
      const vh = window.innerHeight;
      const imgs = [...document.images].filter((i) => {
        const r = i.getBoundingClientRect();
        return r.width > 20 && r.height > 20 && r.bottom > 0 && r.top < vh && getComputedStyle(i).visibility !== 'hidden';
      });
      return imgs.filter((i) => !i.complete || i.naturalWidth === 0 || !i.currentSrc).length;
    });
    if (pending === 0) return 0;
    await sleep(500);
  }
  return -1;
}

async function slowScroll(page, maxY) {
  let y = 0;
  const h = await page.evaluate(() => document.documentElement.scrollHeight);
  const end = Math.min(h, maxY);
  while (y < end) {
    y += 350;
    await page.evaluate((yy) => window.scrollTo(0, yy), y);
    await sleep(220);
  }
  await sleep(800);
  await page.evaluate(() => window.scrollTo(0, 0));
  await sleep(800);
}

async function capture(browser, cfg) {
  const page = await browser.newPage();
  await page.setViewport({ width: VW, height: VH, deviceScaleFactor: DPR });
  await page.emulateMediaFeatures([{ name: 'prefers-color-scheme', value: 'light' }]);
  await page.setExtraHTTPHeaders({ 'Accept-Language': 'en-US,en;q=0.9' });
  await page.setUserAgent((await browser.userAgent()).replace('HeadlessChrome', 'Chrome'));
  // YouTube: pre-set consent + English/US + light theme preference (no login).
  await browser.defaultBrowserContext().setCookie(
    { name: 'SOCS', value: 'CAI', domain: '.youtube.com', path: '/' },
    { name: 'PREF', value: 'hl=en&gl=US&f6=80000', domain: '.youtube.com', path: '/' },
    { name: 'CONSENT', value: 'YES+cb', domain: '.youtube.com', path: '/' },
  );
  await page.evaluateOnNewDocument((css) => {
    const add = () => {
      if (document.getElementById('__cap_hide')) return;
      const s = document.createElement('style'); s.id = '__cap_hide'; s.textContent = css;
      (document.head || document.documentElement).appendChild(s);
    };
    document.addEventListener('DOMContentLoaded', add); add();
  }, HIDE_CSS);

  await page.evaluateOnNewDocument((dpr) => {
    window.__box = (el, label, extra = {}) => {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      if (r.width < 1 || r.height < 1) return null;
      const text = (el.innerText || el.getAttribute('alt') || el.getAttribute('aria-label') || '').replace(/[ \t]+/g, ' ').replace(/\n\s*\n+/g, '\n').trim();
      return Object.assign({ label, text: text.slice(0, 4000),
        x: Math.round((r.left + window.scrollX) * dpr), y: Math.round((r.top + window.scrollY - (window.__boxBase || 0)) * dpr),
        w: Math.round(r.width * dpr), h: Math.round(r.height * dpr) }, extra);
    };
  }, DPR);
  try {
    await page.goto(cfg.url, { waitUntil: 'networkidle2', timeout: 60000 });
  } catch (e) { console.log(cfg.name, 'goto note:', e.message); }
  await sleep(2500);
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await dismissDialogs(page);
  await sleep(800);

  await slowScroll(page, cfg.mode === 'full' ? (cfg.cap || 9000) + 1500 : 3000);

  // Page-specific preparation (e.g. finding tiles beyond first rows).
  let pre = {};
  const ex = extractors[cfg.ex];
  if (ex.prepare) pre = (await ex.prepare(page, cfg)) || {};

  // Determine height to capture.
  let H = VH;
  if (cfg.mode === 'full') {
    const docH = await page.evaluate(() => Math.max(document.documentElement.scrollHeight, document.body.scrollHeight));
    H = Math.min(docH, cfg.cap);
    await page.setViewport({ width: VW, height: H, deviceScaleFactor: DPR });
    await sleep(1500);
    await page.evaluate(() => window.scrollTo(0, 0));
  }
  await dismissDialogs(page);
  await page.evaluate(() => document.activeElement && document.activeElement.blur && document.activeElement.blur());
  if (cfg.scrollTo) {
    await page.evaluate((sel) => { const e = document.querySelector(sel); const y = e.getBoundingClientRect().top + window.scrollY - 140; window.scrollTo({ top: y, behavior: 'instant' }); }, cfg.scrollTo);
    await sleep(1500);
  }
  await page.mouse.move(VW - 2, H - 2);
  const pend = await waitImages(page, 25000);
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await sleep(1500);

  if (cfg.scrollTo) await page.evaluate(() => { window.__boxBase = window.scrollY; });
  const boxes = await page.evaluate(ex.extract, DPR, pre);
  boxes.forEach((b) => { b.inside_image = b.y >= 0 && b.y + b.h <= H * DPR; });
  if (cfg.scrollTo) for (let i = boxes.length - 1; i >= 0; i--) { const b = boxes[i]; if (b.y + b.h <= 0 || b.y >= H * DPR) boxes.splice(i, 1); }
  const file = path.join(OUT, cfg.name + '.png');
  await page.screenshot({ path: file });
  const finalUrl = page.url();
  const meta = {
    name: cfg.name,
    url: cfg.url,
    final_url: finalUrl,
    captured_at: new Date().toISOString(),
    css_viewport: { width: VW, height: VH },
    captured_css_height: H,
    capture_mode: cfg.mode === 'full' ? `full page, capped at ${cfg.cap} CSS px` : 'viewport',
    device_scale_factor: DPR,
    color_scheme: 'light',
    locale: 'en-US',
    image_px: { width: VW * DPR, height: H * DPR },
    images_pending_at_capture: pend === -1 ? 'timeout-some-pending' : 0,
    notes: pre.notes || [],
    boxes,
  };
  fs.writeFileSync(path.join(OUT, cfg.name + '.json'), JSON.stringify(meta, null, 2));
  console.log('OK', cfg.name, `${VW * DPR}x${H * DPR}`, 'boxes:', boxes.length, 'final:', finalUrl, pend === -1 ? '(images pending!)' : '');
  await page.close();
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const only = process.argv.slice(4);
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--lang=en-US', '--force-color-profile=srgb', '--hide-scrollbars', '--disable-blink-features=AutomationControlled'],
    env: { ...process.env, LANG: 'en_US.UTF-8' },
  });
  for (const cfg of PAGES) {
    if (only.length && !only.includes(cfg.name)) continue;
    try { await capture(browser, cfg); } catch (e) { console.log('FAIL', cfg.name, e.stack); }
  }
  await browser.close();
})();
