// PDF A4 paysage du diaporama : une diapositive par page, rendu par Chromium et Playwright.
// NODE_PATH=$(npm root -g) node pdf.js <sortie.pdf>
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const sortie = process.argv[2] || path.join(__dirname, 'Formation_GARP_2026-10-13.pdf');
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 } });
  await p.emulateMedia({ media: 'print', reducedMotion: 'reduce' });
  await p.goto('file://' + path.join(__dirname, 'diaporama', 'index.html'), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => window.GZ.impression());
  await p.waitForTimeout(500);
  await p.pdf({ path: sortie, format: 'A4', landscape: true, printBackground: true, preferCSSPageSize: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  const n = await p.evaluate(() => document.querySelectorAll('.pg').length);
  console.log(`${sortie} : ${n} pages`);
  await b.close();
})();
