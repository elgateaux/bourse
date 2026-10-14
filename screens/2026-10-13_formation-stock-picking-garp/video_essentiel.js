// Vidéo « L'essentiel » : le parcours essentiel du diaporama filmé image par image, puis monté par FFmpeg.
//
//   NODE_PATH=$(npm root -g) node video_essentiel.js            plan, bande-son et rendu complet (MP4 1080p, 30 i/s)
//   NODE_PATH=$(npm root -g) node video_essentiel.js --plan     seulement le plan (video_essentiel.csv)
//   NODE_PATH=$(npm root -g) node video_essentiel.js --extrait 0-3 <sortie.mp4>   aperçu des plans 0 à 3
//
// Aucun contenu propre à la vidéo : chaque image est une diapositive de diaporama/index.html, avec ses chiffres
// sourcés. Le script ajoute seulement :
//   - les ouvertures de chapitre du diaporama, en intertitres ;
//   - une barre de progression dorée ;
//   - les chapitres du MP4 ;
//   - une bande-son originale (bande_son.py).
// Le temps du navigateur est virtuel : chaque animation CSS est mise en pause puis positionnée image par image, et
// requestAnimationFrame avance au rythme des images. Le rendu est donc identique d'une exécution à l'autre.
const { chromium } = require('playwright');
const { spawn, execFileSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const FPS = 30;
const SORTIE = path.join(__dirname, 'Video_GARP_L-essentiel_2026-10-13.mp4');
const PLAN_CSV = path.join(__dirname, 'video_essentiel.csv');
// Durée d'affichage : temps de lecture à 3,5 mots par seconde, plus 3 s d'animation, borné à [8 s ; 20 s].
// Couverture 9 s, intertitres 5 s, dernière diapositive jusqu'à 24 s. Mettre en pause pour lire les sources.
const DUREE = { base: 3, mots_par_s: 3.5, min: 8, max: 20, couverture: 9, ouverture: 5, fin_max: 24 };
// Diapositive du parcours essentiel retirée de la vidéo : le mode d'emploi du clavier n'a pas de sens à l'écran.
const EXCLUES = ['Comment lire cette formation'];

const args = process.argv.slice(2);
const seulPlan = args.includes('--plan');
const iEx = args.indexOf('--extrait');
const extrait = iEx >= 0 ? args[iEx + 1].split('-').map(Number) : null;
const sortie = iEx >= 0 ? path.resolve(args[iEx + 2] || path.join(os.tmpdir(), 'extrait.mp4')) : SORTIE;

// Temps virtuel, injecté avant les scripts de la page.
function tempsVirtuel() {
  let vt = 0, file = [];
  window.requestAnimationFrame = (cb) => { file.push(cb); return file.length; };
  window.cancelAnimationFrame = () => {};
  const depart = new WeakMap();
  function caler() {
    for (const a of document.getAnimations()) {
      if (!depart.has(a)) { depart.set(a, vt); a.pause(); }
      a.currentTime = Math.max(0, vt - depart.get(a));
    }
  }
  function reste() {           // ms avant la fin des animations finies ; infini si une animation sans fin est visible
    let fin = 0, infini = false;
    for (const a of document.getAnimations()) {
      const t = a.effect && a.effect.getComputedTiming();
      if (!t) continue;
      const cible = a.effect.target;
      const visible = cible && cible.closest && cible.closest('.slide.on');
      if (t.endTime === Infinity) { if (visible) infini = true; continue; }
      fin = Math.max(fin, (depart.has(a) ? depart.get(a) : vt) + t.endTime - vt);
    }
    return { fin, infini };
  }
  window.__video = {
    caler, reste,
    avancer(ms) { vt += ms; const cbs = file; file = []; for (const cb of cbs) { try { cb(vt); } catch (e) {} } caler(); },
  };
}

// Habillage vidéo : diapositive plein cadre, barre de commandes masquée, fond fixe (pas de dérive sans fin).
const CSS_VIDEO = `
#gz.pres { --W:100vw; } #gz.pres .stage { bottom:0; } #gz.pres .ctrl, .toc { display:none !important; }
#gz .slide .bg { animation:none !important; }
#gz .hud .hniv { display:none; }
#gz .op-list li.hors-video { display:none; }
#gz .op-list .num { display:none; }
`;

(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 }, reducedMotion: 'no-preference' });
  await p.addInitScript(() => { try { localStorage.setItem('gz-mode', 'pres'); localStorage.setItem('gz-parcours', 'complet'); } catch (e) {} });
  await p.addInitScript(tempsVirtuel);
  const erreurs = [];
  p.on('pageerror', (e) => erreurs.push(String(e)));
  await p.goto('file://' + path.join(__dirname, 'diaporama', 'index.html'), { waitUntil: 'load' });
  await p.evaluate(() => document.fonts.ready);
  await p.addStyleTag({ content: CSS_VIDEO });

  // ---------- plan : intertitres de chapitre + parcours essentiel
  const plan = await p.evaluate((EXCLUES) => {
    const slides = Array.from(document.querySelectorAll('#gz .slide'));
    const mots = (s) => {
      const c = s.querySelector('.sl-in').cloneNode(true);
      c.querySelectorAll('.hud, .foot, .bg, [hidden], script, style, .op-list li').forEach((x) => x.remove());
      return (c.textContent || '').split(/\s+/).filter((w) => /[\p{L}\p{N}]/u.test(w)).length;
    };
    const out = [];
    slides.forEach((s, i) => {
      const op = s.classList.contains('op');
      if (!op && s.dataset.niv !== 'e') return;
      if (EXCLUES.includes(s.dataset.titre)) return;
      const type = op ? 'intertitre' : i === 0 ? 'couverture' : i === slides.length - 1 ? 'fin'
        : s.classList.contains('ret-sl') ? 'a_retenir' : 'essentiel';
      out.push({ idx: i, diapositive: i + 1, section: s.dataset.sec, titre: s.dataset.titre, type, mots: op ? 0 : mots(s) });
    });
    return out;
  }, EXCLUES);
  let t = 0;
  for (const x of plan) {
    const lecture = DUREE.base + x.mots / DUREE.mots_par_s;
    x.duree_s = x.type === 'couverture' ? DUREE.couverture : x.type === 'intertitre' ? DUREE.ouverture
      : Math.min(x.type === 'fin' ? DUREE.fin_max : DUREE.max, Math.max(DUREE.min, lecture));
    x.duree_s = Math.round(x.duree_s * FPS) / FPS;
    x.debut_s = Math.round(t * 1000) / 1000;
    t += x.duree_s;
  }
  const TOTAL = Math.round(t * 1000) / 1000;
  const cols = ['ordre', 'diapositive', 'section', 'titre', 'type', 'mots', 'debut_s', 'duree_s'];
  const q = (v) => (/[",\n]/.test(String(v)) ? '"' + String(v).replace(/"/g, '""') + '"' : String(v));
  fs.writeFileSync(PLAN_CSV, cols.join(',') + '\n' + plan.map((x, k) => [k + 1, x.diapositive, x.section, x.titre, x.type, x.mots, x.debut_s.toFixed(3), x.duree_s.toFixed(3)].map(q).join(',')).join('\n') + '\n');
  const nEss = plan.filter((x) => x.type !== 'intertitre').length;
  console.log(`${PLAN_CSV} : ${plan.length} plans (${nEss} diapositives essentielles, ${plan.length - nEss} intertitres), ${Math.floor(TOTAL / 60)} min ${Math.round(TOTAL % 60)} s`);
  if (seulPlan) { await b.close(); return; }

  // ---------- bande-son et chapitres
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'video-garp-'));
  const sel = extrait ? plan.slice(extrait[0], extrait[1] + 1) : plan;
  const t0 = sel[0].debut_s, duree = sel.reduce((s, x) => s + x.duree_s, 0);
  const wav = path.join(tmp, 'bande_son.wav');
  execFileSync('python3', [path.join(__dirname, 'bande_son.py'), PLAN_CSV, wav], { stdio: 'inherit' });
  const esc = (v) => String(v).replace(/([=;#\\\n])/g, '\\$1');
  const meta = [';FFMETADATA1', 'title=' + esc('La Gazette du PEG* · Formation GARP : l\'essentiel en vidéo'),
    'comment=' + esc('* Titre fictif : il ne correspond à aucune publication existante. Analyse quantitative et datée, qui ne constitue pas un conseil en investissement personnalisé.')];
  let cur = null;
  const chap = [];
  for (const x of sel) {
    if (!cur || cur.section !== x.section) { cur = { section: x.section, debut: x.debut_s - t0, fin: 0 }; chap.push(cur); }
    cur.fin = x.debut_s - t0 + x.duree_s;
  }
  for (const c of chap) meta.push('[CHAPTER]', 'TIMEBASE=1/1000', `START=${Math.round(c.debut * 1000)}`, `END=${Math.round(c.fin * 1000)}`, 'title=' + esc(c.section));
  fs.writeFileSync(path.join(tmp, 'chapitres.txt'), meta.join('\n') + '\n');

  // ---------- FFmpeg : images JPEG sur l'entrée standard, barre de progression, bande-son, chapitres
  const H = 6;
  const ff = spawn('ffmpeg', ['-hide_banner', '-loglevel', 'error', '-y',
    '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-ss', t0.toFixed(3), '-t', duree.toFixed(3), '-i', wav,
    '-f', 'ffmetadata', '-i', path.join(tmp, 'chapitres.txt'),
    '-filter_complex',
    `[0:v]drawbox=x=0:y=ih-${H}:w=iw:h=${H}:color=0x05070a@0.6:t=fill[f];` +
    `color=c=0xffc94a:s=1920x${H}:r=${FPS}[g];` +
    `[f][g]overlay=x='-w+w*(t+${t0.toFixed(3)})/${TOTAL.toFixed(3)}':y=H-${H}:shortest=1,format=yuv420p[v];` +
    `[1:a]afade=t=in:st=0:d=0.8,afade=t=out:st=${Math.max(0, duree - 2.5).toFixed(3)}:d=2.5[a]`,
    '-map', '[v]', '-map', '[a]', '-map_metadata', '2', '-map_chapters', '2',
    '-c:v', 'libx264', '-preset', 'slow', '-tune', 'animation', '-crf', '23', '-g', String(FPS * 30), '-r', String(FPS),
    '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-shortest', sortie], { stdio: ['pipe', 'inherit', 'inherit'] });
  const fini = new Promise((ok, ko) => ff.on('close', (c) => (c === 0 ? ok() : ko(new Error('ffmpeg ' + c)))));
  const ecrire = (buf) => (ff.stdin.write(buf) ? Promise.resolve() : new Promise((ok) => ff.stdin.once('drain', ok)));

  const cdp = await p.context().newCDPSession(p);
  const image = async () => Buffer.from((await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 94, optimizeForSpeed: true })).data, 'base64');
  const essentiels = new Set(plan.map((x) => x.diapositive));

  // Point de départ : aucune diapositive affichée, la couverture entre en fondu depuis le noir.
  await p.evaluate((ess) => {
    document.querySelectorAll('#gz .slide').forEach((s) => s.classList.remove('on', 'past'));
    document.querySelectorAll('#gz .op-list li').forEach((li) => {
      const a = li.querySelector('a[href^="#s"]');
      if (a && !ess.includes(parseInt(a.getAttribute('href').slice(2), 10))) li.classList.add('hors-video');
    });
    document.body.offsetWidth; window.__video.caler();
  }, [...essentiels]);

  let nImages = 0, nCalculees = 0;
  const debutRendu = Date.now();
  for (let k = 0; k < sel.length; k++) {
    const x = sel[k], n = Math.round(x.duree_s * FPS), num = plan.indexOf(x) + 1;
    await p.evaluate(({ idx, num, tot }) => {
      window.GZ.aller(idx);
      const h = document.querySelectorAll('#gz .slide')[idx].querySelector('.hud .hnum');
      if (h) h.lastChild.textContent = String(num).padStart(2, '0') + ' / ' + tot;
      document.body.offsetWidth; window.__video.caler();
    }, { idx: x.idx, num, tot: plan.length });
    const calc = await p.evaluate((idx) => !!document.querySelectorAll('#gz .slide')[idx].querySelector('#calc'), x.idx);
    let derniere = null, anime = true;
    for (let f = 0; f < n; f++) {
      if (anime) {
        await p.evaluate(({ f, calc }) => {
          if (calc) {   // démonstration : la durée passe de 1 an à la valeur par défaut, entre 1,2 s et 5,2 s
            const r = document.getElementById('c-dur');
            if (!r.dataset.cible) r.dataset.cible = r.value;
            const p = Math.min(1, Math.max(0, (f / 30 - 1.2) / 4)), e = p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
            const v = String(Math.round(1 + (parseFloat(r.dataset.cible) - 1) * e));
            if (r.value !== v) { r.value = v; r.dispatchEvent(new Event('input', { bubbles: true })); }
          }
          if (f > 0) window.__video.avancer(1000 / 30);
        }, { f, calc });
        derniere = await image();
        nCalculees++;
        const { fin, infini } = await p.evaluate(() => window.__video.reste());
        if (!infini && fin <= 0 && (!calc || f / FPS > 5.4) && f > 0) anime = false;
      }
      await ecrire(derniere);
      nImages++;
    }
    const ecoule = (Date.now() - debutRendu) / 1000;
    console.log(`  plan ${num}/${plan.length} · diapo ${x.diapositive} · ${x.titre} · ${n} images · ${ecoule.toFixed(0)} s`);
  }
  ff.stdin.end();
  await fini;
  await b.close();
  fs.rmSync(tmp, { recursive: true, force: true });
  if (erreurs.length) { console.error('Erreurs JavaScript :', erreurs); process.exit(1); }
  console.log(`${sortie} : ${nImages} images (${nCalculees} calculées), ${(duree / 60).toFixed(2)} min, ${(fs.statSync(sortie).size / 1e6).toFixed(1)} Mo`);
})();
