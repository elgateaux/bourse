const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  for (const [w, scheme, out] of [[1280, 'light', 'bureau.png'], [400, 'light', 'mobile.png'], [1280, 'dark', 'sombre.png']]) {
    const p = await b.newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme });
    await p.goto('file://' + process.argv[2] + '/apercu.html', { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const m = await p.evaluate(() => {
      const de = document.documentElement;
      const wide = [...document.querySelectorAll('body *')].filter(e => {
        const r = e.getBoundingClientRect(); return r.right > de.clientWidth + 1 && !e.closest('.fig-scroll, .tbl');
      }).slice(0, 8).map(e => (e.className || e.tagName) + ':' + Math.round(e.getBoundingClientRect().right));
      const fonts = ['Archivo', 'Newsreader', 'IBM Plex Mono'].map(f => f + '=' + document.fonts.check(`800 40px "${f}"`)).join(' ');
      return { scrollW: de.scrollWidth, clientW: de.clientWidth, height: de.scrollHeight, wide, fonts };
    });
    console.log(w, scheme, JSON.stringify(m));
    await p.screenshot({ path: process.argv[2] + '/' + out, fullPage: true });
    await p.close();
  }
  await b.close();
})();
