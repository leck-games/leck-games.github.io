// Headless check: iPhone 12 emulation (390x844 portrait / 844x390 landscape).
// usage: node tools/test.cjs <baseURL> [shotsDir]   baseURL = site root that serves / (launcher) and /sinerally/ etc.
const puppeteer = require('/workspace/sinerally-physics/node_modules/puppeteer-core');
const base = (process.argv[2] || 'http://127.0.0.1:8099/').replace(/\/?$/, '/'); const shots = process.argv[3];
const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1';
const P = { w: 390, h: 844 }, L = { w: 844, h: 390 };
const pages = [['launcher', ''], ['sinerally', 'sinerally/'], ['engine', 'sinerally-engine/'], ['enginesim', 'sinerally-enginesim/'], ['physics', 'sinerally-physics/'], ['terrain', 'sinerally-terrain/']];
(async () => {
  const br = await puppeteer.launch({ executablePath: '/usr/bin/google-chrome', headless: 'new', args: ['--no-sandbox', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  let fail = 0;
  for (const [name, path] of pages) for (const [on, vp] of [['landscape', L], ['portrait', P]]) {
    const pg = await br.newPage(); const errs = [];
    await pg.setUserAgent(UA); await pg.setViewport({ width: vp.w, height: vp.h, deviceScaleFactor: 3, isMobile: true, hasTouch: true, isLandscape: on === 'landscape' });
    pg.on('console', (m) => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
    pg.on('pageerror', (e) => errs.push('pageerror: ' + e.message));
    pg.on('response', (r) => { if (r.status() >= 400 && !/api\.github\.com/.test(r.url())) errs.push(r.status() + ' ' + r.url()); });
    const url = base + path;
    await pg.goto(url, { waitUntil: 'networkidle2', timeout: 60000 }).catch((e) => errs.push('goto: ' + e.message));
    await new Promise((r) => setTimeout(r, 2500));
    const info = await pg.evaluate(async () => {
      const q = (s) => document.querySelector(s); const o = {};
      const man = q('link[rel=manifest]'); o.manifest = !!man; o.atIcon = q('link[rel=apple-touch-icon]')?.href;
      o.metas = ['apple-mobile-web-app-capable', 'mobile-web-app-capable', 'apple-mobile-web-app-status-bar-style', 'apple-mobile-web-app-title', 'theme-color'].filter((n) => !q(`meta[name="${n}"]`));
      o.vpFit = /viewport-fit=cover/.test(q('meta[name=viewport]')?.content || '');
      if (man) { try { const r = await fetch(man.href); const j = await r.json(); o.man = { status: r.status, display: j.display, orientation: j.orientation, start: j.start_url };
        o.icons = await Promise.all(j.icons.map(async (i) => { const u = new URL(i.src, man.href); const rr = await fetch(u); const b = await rr.blob(); const bm = await createImageBitmap(b); return `${i.sizes}:${rr.status}:${bm.width}x${bm.height}`; })); } catch (e) { o.manErr = e.message; } }
      if (o.atIcon) { const r = await fetch(o.atIcon); const bm = await createImageBitmap(await r.blob()); o.at = `${r.status}:${bm.width}x${bm.height}`; }
      const ab = q('#allBuilds'); o.allBuilds = ab ? ab.getAttribute('href') : null;
      o.cards = document.querySelectorAll('.card').length;
      o.canvas = [...document.querySelectorAll('canvas')].map((c) => getComputedStyle(c).touchAction + '/' + (getComputedStyle(c).webkitTouchCallout || '?')).slice(0, 1)[0];
      return o; });
    const bad = errs.length || !info.manifest || info.metas.length || !info.vpFit || (name !== 'launcher' && !info.allBuilds) || (name === 'launcher' && info.cards !== 5) || info.manErr || (info.icons || []).some((s) => !/:200:/.test(s));
    if (bad) fail++;
    console.log(`${bad ? 'FAIL' : 'ok  '} ${name} ${on}`, JSON.stringify(info), errs.length ? '\n   ' + errs.join('\n   ') : '');
    if (shots && name === 'launcher') { await pg.screenshot({ path: `${shots}/launcher-iphone12-${on}.png` }); await pg.screenshot({ path: `${shots}/launcher-iphone12-${on}-full.png`, fullPage: true }); }
    await pg.close();
  }
  await br.close(); console.log(fail ? `${fail} FAILED` : 'ALL OK'); process.exit(fail ? 1 : 0);
})();
