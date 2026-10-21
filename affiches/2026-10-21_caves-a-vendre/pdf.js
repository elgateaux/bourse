// Rend chaque affiche HTML en PDF A4 et en PNG de contrôle ; vérifie la police et les débordements.
// Usage : node pdf.js <dossier des HTML> <dossier de sortie PDF> <dossier des PNG>
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const [src, out, png] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch();
  for (const f of fs.readdirSync(src).filter(n => n.startsWith('affiche_') && n.endsWith('.html'))) {
    const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
    await p.goto('file://' + path.resolve(src, f), { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    const police = await p.evaluate(() => document.fonts.check('900 40px "Archivo"'));
    const deborde = await p.evaluate(() => [...document.querySelectorAll('.cadre *')]
      .filter(e => e.scrollWidth > e.clientWidth + 1 || e.getBoundingClientRect().right > document.querySelector('.cadre').getBoundingClientRect().right)
      .map(e => e.className || e.tagName));
    // Chaque bloc de texte doit tenir sur une seule ligne.
    const coupes = await p.evaluate(() => ['.bandeau', '.caves', '.lieu', '.merci', '.tel'].filter(s => {
      const w = document.createTreeWalker(document.querySelector(s), NodeFilter.SHOW_TEXT); const bas = new Set();
      while (w.nextNode()) { const r = document.createRange(); r.selectNodeContents(w.currentNode);
        [...r.getClientRects()].filter(x => x.width > 1).forEach(x => bas.add(Math.round(x.bottom))); }
      return bas.size > 1;
    }));
    const pages = await p.evaluate(() => Math.ceil(document.documentElement.scrollHeight / 1123));
    console.log(f, 'Archivo=' + police, 'débordements=' + (deborde.join(',') || 'aucun'),
      'lignes coupées=' + (coupes.join(',') || 'aucune'), 'pages=' + pages);
    const base = f.replace('.html', '');
    await p.screenshot({ path: path.join(png, base + '.png'), fullPage: true });
    await p.pdf({ path: path.join(out, base + '.pdf'), printBackground: true, preferCSSPageSize: true });
    await p.close();
  }
  await b.close();
})();
