const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + process.argv[2], { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const ok = await p.evaluate(() => ['Archivo', 'Newsreader', 'IBM Plex Mono'].map(f => f + '=' + document.fonts.check(`600 20px "${f}"`)).join(' '));
  console.log(ok);
  await p.pdf({ path: process.argv[3], printBackground: true, preferCSSPageSize: true, displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font-size:8px;color:#66757A;font-family:Arial,sans-serif;padding:0 17mm;display:flex;justify-content:space-between"><span>Prompt · Portefeuille concentré de 3 valeurs, méthode PEG de Peter Lynch</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>' });
  await b.close(); })();
