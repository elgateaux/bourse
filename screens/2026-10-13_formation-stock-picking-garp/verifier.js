// Contrôles du diaporama avec Playwright et Chromium.
// NODE_PATH=$(npm root -g) node verifier.js <dossier_captures>
// - captures 1920 × 1080 de chaque diapositive en mode présentation (après les animations) ;
// - débordements : tout élément qui sort de sa diapositive ou passe sous le pied de page ;
// - polices chargées, erreurs JavaScript ;
// - calculatrice : la fonction JavaScript et l'affichage doivent retrouver calculatrice_tests.csv (calcul.py) ;
// - mode lecture sur téléphone (390 px) : pas de défilement horizontal de la page.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const HERE = __dirname;
const OUT = process.argv[2] || path.join(HERE, 'captures');
fs.mkdirSync(OUT, { recursive: true });
const URL = 'file://' + path.join(HERE, 'diaporama', 'index.html');

function lireCsv(p) {
  const [tete, ...lignes] = fs.readFileSync(p, 'utf8').trim().split('\n');
  const cols = tete.split(',');
  return lignes.map(l => Object.fromEntries(l.split(',').map((v, i) => [cols[i], v])));
}

// Parcourt les nœuds de texte visibles : taille de police calculée et contraste avec le fond réel (couleurs opaques empilées).
const LISIBILITE = (seuil) => {
  const rgb = c => { const m = c.match(/[\d.]+/g); return m ? m.map(Number) : [0, 0, 0, 0]; };
  const lum = ([r, g, b]) => { const f = x => { x /= 255; return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4); }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
  const fond = el => {
    const pile = [];
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) { const c = rgb(getComputedStyle(n).backgroundColor); if (c[3] === undefined || c[3] > 0) pile.push(c); if (c[3] === undefined || c[3] >= 1) break; }
    let base = [7, 9, 13];
    for (let i = pile.length - 1; i >= 0; i--) { const c = pile[i], a = c[3] === undefined ? 1 : c[3]; base = [0, 1, 2].map(k => c[k] * a + base[k] * (1 - a)); }
    return base;
  };
  let min = 1e9; const petits = [], contraste = [];
  const w = document.createTreeWalker(document.querySelector('.stage'), NodeFilter.SHOW_TEXT);
  for (let t = w.nextNode(); t; t = w.nextNode()) {
    if (!t.textContent.trim()) continue;
    const el = t.parentElement; if (!el || el.closest('svg') || el.closest('.opn') || el.closest('[hidden]')) continue;
    const sl = el.closest('.slide'); if (!sl) continue;
    if (document.getElementById('gz').classList.contains('pres') && !sl.classList.contains('on')) continue;
    const cs = getComputedStyle(el); if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const fs = parseFloat(cs.fontSize); min = Math.min(min, fs);
    const id = (sl.id || '') + ' « ' + t.textContent.trim().slice(0, 40) + ' »';
    if (fs < seuil) petits.push(`${id} ${fs.toFixed(1)} px`);
    const c = rgb(cs.color), a = c[3] === undefined ? 1 : c[3], bg = fond(el);
    const col = [0, 1, 2].map(k => c[k] * a + bg[k] * (1 - a));
    const L1 = lum(col), L2 = lum(bg), ratio = (Math.max(L1, L2) + 0.05) / (Math.min(L1, L2) + 0.05);
    if (ratio < 4.5) contraste.push(`${id} ${ratio.toFixed(2)}`);
  }
  return { min: Math.round(min * 10) / 10, petits: [...new Set(petits)], contraste: [...new Set(contraste)] };
};

(async () => {
  const b = await chromium.launch();
  let echecs = 0;
  // ---------------- présentation
  const RAPIDE = process.env.RAPIDE === '1';
  const p = await b.newPage({ viewport: { width: 1920, height: 1126 }, reducedMotion: RAPIDE ? 'reduce' : 'no-preference' });
  const erreurs = [];
  p.on('pageerror', e => erreurs.push(e.message));
  p.on('console', m => { if (m.type() === 'error') erreurs.push(m.text()); });
  await p.goto(URL, { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  const polices = await p.evaluate(() => ['900 20px "GZ Archivo"', 'italic 400 20px "GZ Newsreader"', '400 20px "GZ Newsreader"', '500 20px "GZ Plex Mono"', '600 20px "GZ Plex Mono"']
    .map(f => [f, document.fonts.check(f)]));
  console.log('polices :', polices.map(([f, ok]) => `${f} ${ok ? 'ok' : 'ABSENTE'}`).join(' | '));
  if (polices.some(([, ok]) => !ok)) echecs++;
  const n = await p.evaluate(() => document.querySelectorAll('.slide').length);
  const mode = await p.evaluate(() => document.getElementById('gz').className);
  console.log('diapositives :', n, '; mode :', mode);
  const debord = [];
  const lisTous = { min: 1e9, petits: [], contraste: [] };
  for (let i = 0; i < n; i++) {
    await p.evaluate(i => window.GZ.aller(i), i);
    await p.waitForTimeout(RAPIDE ? 60 : (i === 0 ? 2600 : 2300));
    const pb = await p.evaluate(i => {
      const s = document.querySelectorAll('.slide')[i];
      const r = s.getBoundingClientRect();
      const foot = s.querySelector('.foot').getBoundingClientRect();
      const out = [];
      s.querySelectorAll('.body *, .op-in *').forEach(el => {
        if (el.closest('.tape') || el.closest('.opn') || el.closest('svg') || el.closest('.tw') || el.closest('.ch')) return;
        const q = el.getBoundingClientRect();
        if (!q.width || !q.height) return;
        const txt = (el.innerText || el.textContent || '').trim().slice(0, 50);
        if (q.right > r.right + 1 || q.left < r.left - 1) out.push(`horizontal « ${txt} » (${Math.round(q.left - r.left)} → ${Math.round(q.right - r.left)})`);
        if (q.bottom > foot.top + 1 && !el.closest('.foot')) out.push(`sous le pied « ${txt} » (+${Math.round(q.bottom - foot.top)} px)`);
      });
      s.querySelectorAll('.tw').forEach(t => { if (t.scrollWidth > t.clientWidth + 1) out.push(`tableau trop large (${t.scrollWidth} > ${t.clientWidth})`); if (t.getBoundingClientRect().bottom > foot.top + 1) out.push(`tableau sous le pied (+${Math.round(t.getBoundingClientRect().bottom - foot.top)} px)`); });
      s.querySelectorAll('.ch').forEach(t => { if (t.getBoundingClientRect().bottom > foot.top + 1) out.push(`graphique sous le pied (+${Math.round(t.getBoundingClientRect().bottom - foot.top)} px)`); });
      if (foot.bottom > r.bottom + 1) out.push(`pied de page hors cadre (+${Math.round(foot.bottom - r.bottom)} px)`);
      // chevauchements : deux éléments porteurs de texte, sans lien de parenté, dont les boîtes se recouvrent
      const feuilles = [...s.querySelectorAll('.body *, .op-in *')].filter(el => !el.closest('svg') && !el.closest('.tape') && !el.closest('.opn')
        && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
      // une boîte par ligne pour les éléments en ligne ; on ne retient que les recouvrements nets (plus de 20 % de la plus petite boîte)
      const boites = [];
      feuilles.forEach(el => [...el.getClientRects()].forEach(q => { if (q.width > 2 && q.height > 2) boites.push([el, q]); }));
      for (let a1 = 0; a1 < boites.length; a1++) for (let b1 = a1 + 1; b1 < boites.length; b1++) {
        const [ea, qa] = boites[a1], [eb, qb] = boites[b1];
        if (ea === eb || ea.contains(eb) || eb.contains(ea)) continue;
        const ix = Math.min(qa.right, qb.right) - Math.max(qa.left, qb.left), iy = Math.min(qa.bottom, qb.bottom) - Math.max(qa.top, qb.top);
        if (ix > 3 && iy > 3 && ix * iy > 0.2 * Math.min(qa.width * qa.height, qb.width * qb.height))
          out.push(`chevauchement « ${(ea.innerText || '').trim().slice(0, 30)} » / « ${(eb.innerText || '').trim().slice(0, 30)} »`);
      }
      return [...new Set(out)].slice(0, 6);
    }, i);
    if (pb.length) debord.push([i + 1, pb]);
    const l1 = await p.evaluate(LISIBILITE, 14);
    lisTous.min = Math.min(lisTous.min, l1.min); lisTous.petits.push(...l1.petits); lisTous.contraste.push(...l1.contraste);
    const el = await p.$(`#s${i + 1}`);
    if (!RAPIDE || pb.length) await el.screenshot({ path: path.join(OUT, `s${String(i + 1).padStart(2, '0')}.png`) });
  }
  debord.forEach(([k, l]) => console.log(`diapo ${k} :`, l.join(' ; ')));
  const lis = lisTous;
  console.log(`lisibilité (1920 px) : police minimale ${lis.min} px ; ${lis.petits.length} texte(s) sous 14 px ; ${lis.contraste.length} texte(s) sous un contraste de 4,5`);
  lis.petits.slice(0, 8).forEach(x => console.log('   petit :', x));
  lis.contraste.slice(0, 8).forEach(x => console.log('   contraste :', x));
  if (lis.petits.length || lis.contraste.length) echecs++;
  if (debord.length) echecs++;
  console.log('débordements :', debord.length ? debord.length + ' diapositive(s)' : 'aucun');

  // ---------------- calculatrice
  const cas = lireCsv(path.join(HERE, 'calculatrice_tests.csv'));
  let ecartMax = 0;
  for (const c of cas) {
    const s = await p.evaluate(c => window.GZ.simuler(+c.capital, +c.mensuel, +c.annees, +c.rendement, +c.frais, c.enveloppe, c.couple === '1', +c.inflation), c);
    for (const k of ['verse', 'valeur', 'cout_frais', 'impot', 'net', 'reel']) ecartMax = Math.max(ecartMax, Math.abs(s[k] - +c[k]));
  }
  console.log(`calculatrice (fonction) : ${cas.length} cas, écart maximal ${ecartMax.toExponential(2)} €`);
  if (ecartMax > 0.01) echecs++;
  // affichage : cas n° 5 saisi dans les champs
  const c5 = cas[4];
  const idx = await p.evaluate(() => [...document.querySelectorAll('.slide')].findIndex(s => s.querySelector('#calc')));
  await p.evaluate(i => window.GZ.aller(i), idx);
  await p.waitForTimeout(600);
  const champs = { cap: c5.capital, men: c5.mensuel, dur: c5.annees, ren: +c5.rendement * 100, fra: +c5.frais * 100, inf: +c5.inflation * 100 };
  for (const [k, v] of Object.entries(champs)) { await p.fill(`#c-${k}-n`, String(v)); }
  await p.click(`#c-env button[data-v="${c5.enveloppe}"]`);
  const affiche = await p.$eval('#r-net', el => el.textContent);
  const attendu = await p.evaluate(x => window.GZ.fr(x, 0) + ' €', +c5.net);
  console.log(`calculatrice (affichage) : ${affiche} ; attendu ${attendu} → ${affiche === attendu ? 'ok' : 'ÉCART'}`);
  if (affiche !== attendu) echecs++;
  await (await p.$(`#s${idx + 1}`)).screenshot({ path: path.join(OUT, 'calculatrice_cas5.png') });
  // PEG et quiz
  const pi = await p.evaluate(() => [...document.querySelectorAll('.slide')].findIndex(s => s.querySelector('.pegcalc')));
  await p.evaluate(i => window.GZ.aller(i), pi);
  await p.waitForTimeout(400);
  await p.fill('#peg-pe', '30'); await p.fill('#peg-g', '15');
  console.log('PEG 30 / 15 :', await p.$eval('#peg-v', el => el.textContent), '·', await p.$eval('#peg-txt', el => el.textContent));
  const qi = await p.evaluate(() => [...document.querySelectorAll('.slide')].findIndex(s => s.querySelector('.qz')));
  await p.evaluate(i => window.GZ.aller(i), qi);
  await p.waitForTimeout(500);
  const opts = await p.$$('.qz-q .opt[data-ok="1"]');
  for (const o of opts) await o.click();
  console.log('quiz :', await p.$eval('#qz-score', el => el.textContent));
  console.log('erreurs JavaScript :', erreurs.length ? erreurs.join(' | ') : 'aucune');
  if (erreurs.length) echecs++;

  // ---------------- téléphone, mode lecture
  const m = await b.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
  await m.goto(URL, { waitUntil: 'load' });
  await m.evaluate(() => document.fonts.ready);
  await m.waitForTimeout(400);
  const larg = await m.evaluate(() => [document.getElementById('gz').className, document.documentElement.scrollWidth, window.innerWidth]);
  console.log(`téléphone : mode ${larg[0]}, largeur de page ${larg[1]} pour ${larg[2]} px de fenêtre`);
  if (larg[1] > larg[2]) echecs++;
  const trop = await m.evaluate(() => {
    const out = [];
    document.querySelectorAll('.slide').forEach((s, i) => {
      const r = s.getBoundingClientRect();
      s.querySelectorAll('.body *, .op-in *').forEach(el => {
        if (el.closest('.tw') || el.closest('.ch') || el.closest('.tape') || el.closest('.opn')) return;
        const q = el.getBoundingClientRect();
        if (q.width && q.right > r.right + 1) out.push(`${i + 1} « ${(el.innerText || '').trim().slice(0, 40)} »`);
      });
    });
    return [...new Set(out)].slice(0, 15);
  });
  console.log('téléphone, débordements :', trop.length ? trop.join(' ; ') : 'aucun');
  const lm = await m.evaluate(LISIBILITE, 11);
  console.log(`lisibilité (téléphone) : police minimale ${lm.min} px ; ${lm.petits.length} texte(s) sous 11 px ; ${lm.contraste.length} texte(s) sous un contraste de 4,5`);
  lm.petits.slice(0, 8).forEach(x => console.log('   petit :', x));
  lm.contraste.slice(0, 8).forEach(x => console.log('   contraste :', x));
  if (lm.petits.length || lm.contraste.length) echecs++;
  if (trop.length) echecs++;
  for (const k of [1, 5, 12, 27, 49, 50, 62]) {
    await m.evaluate(k => document.getElementById('s' + k).scrollIntoView(), k);
    await m.waitForTimeout(1500);
    await (await m.$(`#s${k}`)).screenshot({ path: path.join(OUT, `mobile_s${String(k).padStart(2, '0')}.png`) });
  }
  await b.close();
  console.log(echecs ? `ÉCHECS : ${echecs}` : 'TOUS LES CONTRÔLES SONT PASSÉS');
  process.exit(echecs ? 1 : 0);
})();
