// In-page extractors. Each `extract(dpr, pre)` runs inside the page and uses window.__box
// (injected by capture.js) to return bounding boxes in IMAGE pixels (CSS px * DPR).

const ANALYSED = ['The Pink Prison Cell Experiment', 'How One Cart Stopped an Entire Army', 'How Mine Salting Worked'];

function ytHeaderBoxes() {
  const B = window.__box, out = [];
  const hdr = document.querySelector('yt-page-header-view-model');
  out.push(B(document.querySelector('yt-image-banner-view-model, ytd-c4-tabbed-header-renderer #banner'), 'banner'));
  out.push(B(hdr && hdr.querySelector('yt-decorated-avatar-view-model, yt-avatar-shape'), 'avatar'));
  out.push(B(hdr && hdr.querySelector('h1'), 'channel_name'));
  const meta = hdr && hdr.querySelector('yt-content-metadata-view-model');
  out.push(B(meta, 'handle_subscriber_line'));
  if (meta) {
    const sub = [...meta.querySelectorAll('span[role="text"]')].find((s) => /subscriber/i.test(s.innerText));
    out.push(B(sub, 'subscriber_count'));
    const handle = [...meta.querySelectorAll('span')].find((s) => /^@/.test(s.innerText.trim()));
    out.push(B(handle, 'handle'));
  }
  out.push(B(hdr && hdr.querySelector('yt-description-preview-view-model'), 'description'));
  out.push(B(document.querySelector('yt-tab-group-shape, tp-yt-app-toolbar #tabsContent'), 'tabs'));
  return out.filter(Boolean);
}

module.exports = {
  ytHeader: { extract: new Function('dpr', 'pre', `return (${ytHeaderBoxes.toString()})();`) },

  ytShorts: {
    // Make sure the analysed tiles are loaded; record where they are.
    async prepare(page) {
      const notes = [];
      for (let i = 0; i < 15; i++) {
        const found = await page.evaluate((titles) => {
          const items = [...document.querySelectorAll('ytd-rich-item-renderer')];
          return titles.map((t) => items.findIndex((it) => (it.querySelector('h3 a')?.getAttribute('title') || '').trim() === t));
        }, ANALYSED);
        if (found.every((x) => x >= 0)) {
          notes.push('analysed tile indices (0-based, in grid order): ' + ANALYSED.map((t, k) => `${t} -> #${found[k]}`).join('; '));
          break;
        }
        await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
        await new Promise((r) => setTimeout(r, 1500));
        if (i === 14) notes.push('not all analysed tiles found: ' + JSON.stringify(found));
      }
      await page.evaluate(() => window.scrollTo(0, 0));
      return { notes, titles: ANALYSED };
    },
    extract: new Function('dpr', 'pre', `
      const B = window.__box, out = [];
      const hdr = document.querySelector('yt-page-header-view-model');
      out.push(B(hdr && hdr.querySelector('h1'), 'channel_name'));
      const meta = hdr && hdr.querySelector('yt-content-metadata-view-model');
      if (meta) {
        const sub = [...meta.querySelectorAll('span[role="text"]')].find((s) => /subscriber/i.test(s.innerText));
        out.push(B(sub, 'subscriber_count'));
        out.push(B(meta, 'handle_subscriber_line'));
      }
      out.push(B(hdr && hdr.querySelector('yt-decorated-avatar-view-model'), 'avatar'));
      out.push(B(document.querySelector('yt-image-banner-view-model'), 'banner'));
      const items = [...document.querySelectorAll('ytd-rich-item-renderer')].filter(i => i.getBoundingClientRect().height > 10);
      const tops = [...new Set(items.map(i => Math.round(i.getBoundingClientRect().top)))].sort((a,b)=>a-b);
      const imgH = window.innerHeight;
      items.forEach((it, idx) => {
        const r = it.getBoundingClientRect();
        const row = tops.indexOf(Math.round(r.top)) + 1;
        const title = (it.querySelector('h3 a')?.getAttribute('title') || it.querySelector('h3')?.innerText || '').trim();
        const sub = it.querySelector('.shortsLockupViewModelHostOutsideMetadataSubhead, .shortsLockupViewModelHostMetadataSubhead');
        const views = sub ? sub.innerText.trim() : '';
        const analysed = pre.titles.includes(title);
        if (row > 3 && !analysed) return;
        const extra = { title, views, row, column: null, index: idx, href: it.querySelector('a')?.getAttribute('href') };
        const sameRow = items.filter(j => Math.round(j.getBoundingClientRect().top) === Math.round(r.top)).map(j => Math.round(j.getBoundingClientRect().left)).sort((a,b)=>a-b);
        extra.column = sameRow.indexOf(Math.round(r.left)) + 1;
        extra.inside_image = r.bottom <= imgH;
        const b = B(it, analysed ? 'analysed' : 'tile', extra);
        out.push(b);
        if (analysed) {
          out.push(B(it.querySelector('yt-thumbnail-view-model'), 'analysed_thumbnail', { title }));
          out.push(B(sub, 'analysed_view_count', { title }));
          out.push(B(it.querySelector('h3'), 'analysed_title', { title }));
        }
      });
      return out.filter(Boolean);
    `),
  },

  ghRepo: {
    extract: new Function('dpr', 'pre', `
      const B = window.__box, out = [];
      out.push(B(document.querySelector('#repo-title-component, [itemprop="name"], strong[itemprop="name"]')?.closest('div') || document.querySelector('[itemprop="name"]'), 'repo_title'));
      out.push(B(document.querySelector('[itemprop="name"]'), 'repo_name'));
      out.push(B(document.querySelector('[itemprop="author"]'), 'repo_owner'));

      const starBtn = document.querySelector('[data-testid="star-button"]') || [...document.querySelectorAll('a,button')].find(e => /^\\s*Star/.test(e.innerText || '') && e.getBoundingClientRect().top < 400 && e.getBoundingClientRect().width > 0);
      const starCnt = starBtn && (starBtn.querySelector('[data-component="CounterLabel"], .Counter') || starBtn);
      out.push(B(starBtn, 'star_button', { star_count_title: starCnt && starCnt.getAttribute('title') }));
      out.push(B(starCnt !== starBtn ? starCnt : null, 'star_count', { star_count_title: starCnt && starCnt.getAttribute('title') }));
      const sideStars = [...document.querySelectorAll('a[href$="/stargazers"]')].find(a => /stars?/i.test(a.innerText) && a.getBoundingClientRect().width > 0);
      out.push(B(sideStars, 'sidebar_star_count'));
      const table = document.querySelector('table[aria-labelledby="folders-and-files"]') || document.querySelector('[aria-labelledby="files"]');
      out.push(B(table, 'file_list'));
      if (table) table.querySelectorAll('tbody tr').forEach(tr => {
        const n = tr.querySelector('.react-directory-truncate, a.Link--primary');
        if (n) out.push(B(tr, 'file_row', { name: n.innerText.trim() }));
      });
      const md = document.querySelector('article.markdown-body');
      out.push(B(md, 'readme'));
      if (md) {
        md.querySelectorAll('h1,h2,h3').forEach(h => out.push(B(h.closest('.markdown-heading') || h, h.tagName.toLowerCase())));
        md.querySelectorAll('pre').forEach(p => { if (p.innerText.trim()) out.push(B(p.closest('.highlight, .snippet-clipboard-content') || p, 'code_block')); });
        md.querySelectorAll('table').forEach(t => { if (t.innerText.trim()) out.push(B(t, 'table')); });
      }
      out.push(B(document.querySelector('.Layout-sidebar .BorderGrid, [data-testid="repo-sidebar"]'), 'sidebar_about'));
      return out.filter(Boolean);
    `),
  },

  ghFolder: {
    extract: new Function('dpr', 'pre', `
      const B = window.__box, out = [];
      out.push(B(document.querySelector('#repos-header-breadcrumb--wide')?.parentElement, 'breadcrumb'));
      const table = document.querySelector('table[aria-labelledby="folders-and-files"]');
      out.push(B(table, 'file_list'));
      if (table) table.querySelectorAll('tbody tr').forEach(tr => {
        const n = tr.querySelector('.react-directory-truncate, a.Link--primary');
        if (n && n.innerText.trim() !== '..') out.push(B(tr, 'file_row', { name: n.innerText.trim(), is_dir: !!tr.querySelector('svg.icon-directory-fill, svg[aria-label="Directory"]') }));
      });
      const md = document.querySelector('article.markdown-body');
      out.push(B(md, 'readme'));
      if (md) md.querySelectorAll('h1,h2,h3').forEach(h => out.push(B(h, h.tagName.toLowerCase())));
      return out.filter(Boolean);
    `),
  },

  ghMarkdown: {
    extract: new Function('dpr', 'pre', `
      const B = window.__box, out = [];
      out.push(B(document.querySelector('#repos-header-breadcrumb--wide')?.parentElement, 'breadcrumb'));
      const md = document.querySelector('article.markdown-body') || document.querySelector('.markdown-body');
      out.push(B(md, 'markdown_body'));
      if (md) {
        md.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => out.push(B(h, h.tagName.toLowerCase())));
        md.querySelectorAll('table').forEach(t => out.push(B(t, 'table')));
        md.querySelectorAll('pre').forEach(p => out.push(B(p, 'code_block')));
      }
      return out.filter(Boolean);
    `),
  },

  ghHyper: {
    extract: new Function('dpr', 'pre', `
      const B = window.__box, out = [];
      out.push(B(document.querySelector('[itemprop="name"]')?.parentElement, 'repo_title'));
      out.push(B(document.querySelector('[itemprop="name"]'), 'repo_name'));

      const starBtn = document.querySelector('[data-testid="star-button"]') || [...document.querySelectorAll('a,button')].find(e => /^\\s*Star/.test(e.innerText || '') && e.getBoundingClientRect().top < 400 && e.getBoundingClientRect().width > 0);
      const starCnt = starBtn && (starBtn.querySelector('[data-component="CounterLabel"], .Counter') || starBtn);
      out.push(B(starBtn, 'star_button', { star_count_title: starCnt && starCnt.getAttribute('title') }));
      out.push(B(starCnt !== starBtn ? starCnt : null, 'star_count', { star_count_title: starCnt && starCnt.getAttribute('title') }));
      const sideStars = [...document.querySelectorAll('a[href$="/stargazers"]')].find(a => /stars?/i.test(a.innerText) && a.getBoundingClientRect().width > 0);
      out.push(B(sideStars, 'sidebar_star_count'));
      const sideLic = [...document.querySelectorAll('a[href*="-ov-file"]')].find(a => /licen[sc]e/i.test(a.innerText) && a.getBoundingClientRect().width > 0 && a.getBoundingClientRect().left > 1100);
      out.push(B(sideLic, 'sidebar_license'));
      const about = [...document.querySelectorAll('h2')].find(h => h.innerText.trim() === 'About');
      out.push(B(about && about.parentElement, 'sidebar_about'));
      out.push(B([...document.querySelectorAll('a[href$="/blob/main/LICENSE"]')].find(a => a.getBoundingClientRect().width > 0), 'license_file_row'));
      const md = document.querySelector('article.markdown-body');
      if (md) {
        md.querySelectorAll('img').forEach(img => {
          const s = (img.getAttribute('alt')||'') + ' ' + (img.getAttribute('src')||'') + ' ' + (img.getAttribute('data-canonical-src')||'');
          if (/licen[sc]e/i.test(s)) out.push(B(img, 'license_badge', { alt: img.getAttribute('alt'), src: img.getAttribute('data-canonical-src') || img.getAttribute('src') }));
        });
        md.querySelectorAll('h1,h2,h3').forEach(h => { const b = B(h, h.tagName.toLowerCase()); if (b && b.y < (window.innerHeight + window.scrollY) * dpr) out.push(b); });
        out.push(B(md, 'readme'));
      }
      const tab = [...document.querySelectorAll('a, [role="tab"]')].find(a => /licen[sc]e/i.test(a.innerText) && a.closest('nav, [role="tablist"], ul'));
      out.push(B(tab, 'readme_license_tab'));
      return out.filter(Boolean);
    `),
  },

  remotion: {
    extract: new Function('dpr', 'pre', `
      const B = window.__box, out = [];
      const root = document.querySelector('main, article') || document.body;
      root.querySelectorAll('h1,h2,h3').forEach(h => out.push(B(h, h.tagName.toLowerCase())));
      const re = /(free to use|free license|up to (3|three)|individual|employee|do not qualify|ineligible)/i;
      const els = [...root.querySelectorAll('p, li, div, span, h2, h3, h4')].filter(e => re.test(e.innerText || '') && (e.innerText || '').length < 600);
      const inner = els.filter(e => !els.some(o => o !== e && e.contains(o)));
      inner.forEach(e => out.push(B(e, 'license_terms_quote')));
      // the card that holds the Free License terms
      const card = inner.find(e => /up to 3 people/i.test(e.innerText));
      let c = card; while (c && c.parentElement && !/Free License/.test(c.innerText)) c = c.parentElement;
      while (c && c.parentElement && c.parentElement.innerText.length < 300) c = c.parentElement;
      out.push(B(c, 'free_license_card'));
      return out.filter(Boolean);
    `),
  },

  generic: {
    extract: new Function('dpr', 'pre', `
      const B = window.__box, out = [];
      document.querySelectorAll('h1,h2,h3, header, nav, main > section').forEach(h => { const b = B(h, h.tagName.toLowerCase()); if (b && b.y < window.innerHeight*dpr) out.push(b); });
      document.querySelectorAll('a, button').forEach(a => { const b = B(a, 'link_or_button'); if (b && b.y < window.innerHeight*dpr && b.text) out.push(b); });
      return out.filter(Boolean);
    `),
  },
};
