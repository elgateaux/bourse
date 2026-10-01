const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.emulateMedia({ colorScheme: 'light' });
  await p.goto('file://' + process.argv[2] + '/impression.html', { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: process.argv[3], printBackground: true, preferCSSPageSize: true, scale: 0.7, displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font-size:8px;color:#66757A;font-family:Arial,sans-serif;padding:0 12mm;display:flex;justify-content:space-between"><span>Le Cahier PEG · 1er octobre 2026 · Le bilan : Nu, Rheinmetall, TSMC, Uber, NVIDIA</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>' });
  await b.close(); })();
