/* Seven Scop — versi web (port dari versi Python/tkinter)
 * Semua digambar di satu <canvas> dengan ukuran dasar tetap, lalu diperbesar/diperkecil
 * mengikuti layar (seperti maximize di versi desktop).
 */
'use strict';

// ======================= DATA KARTU & ATURAN =======================
const SUITS = ['♠', '♥', '♦', '♣'];
const SUIT_ORDER = { '♠': 0, '♥': 1, '♦': 2, '♣': 3 };
const RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];
const RANK_VALUES = { A: [1, 14], 2: [2], 3: [3], 4: [4], 5: [5], 6: [6], 7: [7], 8: [8], 9: [9], 10: [10], J: [11], Q: [12], K: [13] };
const RANK_POINTS = { A: 15, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, J: 11, Q: 12, K: 13 };
const RANK_SORT = { A: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, J: 11, Q: 12, K: 13 };
const VAL_LABEL = { 1: 'A', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q', 13: 'K', 14: 'A' };
const isRed = s => s === '♥' || s === '♦';
const cardKey = c => c.s + c.r;
const cardStr = c => c.r + c.s;

// ======================= TEKS (2 BAHASA) =======================
const TXT = {
  en: {
    suits: ['Spades', 'Hearts', 'Diamonds', 'Clubs'],
    new_game: 'New Game', options: 'Options', exit: 'Exit', back: '◄ Back',
    p2: '2 Players', p3: '3 Players', p4: '4 Players', language: 'Language', lang_now: 'Language: {lang}',
    menu_hint: '↑ ↓  choose   •   Enter  select   •   Esc  back',
    btn_menu: '◄ Back', btn_restart: '↻ Restart', sort_suit: 'Sort Suit', sort_rank: 'Sort Rank', settings: '⚙ Settings',
    last_card: 'LAST\nCARD', your_cards: 'YOUR CARDS',
    you: 'YOU', your_turn: 'YOUR TURN!', pick_green: 'PICK GREEN!', no68: 'NOT 6/8!',
    closed: 'CLOSED!', cheers: ['POW!', 'PERFECT!', 'YES!', 'BOOM!'], discard: 'DISCARD!',
    disc_info: '{name}\nDISCARD\n{card}',
    log_ready: 'Ready! Pick New Game from the main menu.',
    log_start: '{n}-player game - {name} starts with ♠7',
    log_play: '{name} plays {card}', log_disc: '{name} discards {card}',
    log_end: 'Game over! Winner: {name} ({pts}pts)',
    cant: 'Pick a green card', rule: "You can't discard a 6/8 yet!",
    ace_t: 'ACE', ace: 'Where does this Ace go?', ace_top: 'TOP  K → A', ace_bottom: 'BOTTOM  2 → A',
    win: 'YOU WIN!', lose: 'AWW, YOU LOST...', res_win: 'WINNER', res_lose: 'LOSER',
    click_close: 'click anywhere to close', dealing: 'DEALING CARDS',
    cheer_lose: "DON'T GIVE UP,\nYOU PLAYED GREAT!", cheer_win: 'EXCELLENT!',
    quit_t: 'MAIN MENU', quit: 'Back to the main menu?\nThis game will end.', yes: 'YES', no: 'NO',
    set_title: '⚙ TOON SETTINGS', set_anim: 'Animations on', set_fx: 'Stars & comic text',
    set_bob: 'Wobble green/orange cards', set_sound: 'Sound on', set_speed: 'Animation speed:', ok: 'OK!',
    speed_names: { Lambat: 'Slow', Normal: 'Normal', Cepat: 'Fast' },
    bye: 'THANKS FOR PLAYING!\nClose this tab to exit.',
    rotate: 'Rotate your phone to landscape',
  },
  id: {
    suits: ['Sekop', 'Hati', 'Wajik', 'Keriting'],
    new_game: 'Main Baru', options: 'Pengaturan', exit: 'Keluar', back: '◄ Kembali',
    p2: '2 Pemain', p3: '3 Pemain', p4: '4 Pemain', language: 'Bahasa', lang_now: 'Bahasa: {lang}',
    menu_hint: '↑ ↓  pilih   •   Enter  oke   •   Esc  kembali',
    btn_menu: '◄ Kembali', btn_restart: '↻ Main Lagi', sort_suit: 'Sort Warna', sort_rank: 'Sort Angka', settings: '⚙ Setelan',
    last_card: 'KARTU\nTERAKHIR', your_cards: 'KARTU KAMU',
    you: 'KAMU', your_turn: 'GILIRANMU!', pick_green: 'PILIH HIJAU!', no68: '6/8 JANGAN!',
    closed: 'TUTUP!', cheers: ['POW!', 'MANTAP!', 'YES!', 'BOOM!'], discard: 'BUANG!',
    disc_info: '{name}\nBUANG\n{card}',
    log_ready: 'Siap! Pilih Main Baru di menu utama.',
    log_start: 'Game {n} pemain - {name} mulai ♠7',
    log_play: '{name} main {card}', log_disc: '{name} buang {card}',
    log_end: 'Selesai! Menang: {name} ({pts}pts)',
    cant: 'Pilih hijau', rule: 'Gak boleh buang 6/8 dulu!',
    ace_t: 'AS', ace: 'As ini mau ditaruh di mana?', ace_top: 'ATAS  K → As', ace_bottom: 'BAWAH  2 → As',
    win: 'KAMU MENANG!', lose: 'YAAH, KALAH...', res_win: 'MENANG', res_lose: 'KALAH',
    click_close: 'klik di mana saja untuk tutup', dealing: 'KARTU DIBAGIKAN',
    cheer_lose: 'JANGAN PATAH SEMANGAT,\nKAMU SUDAH BERMAIN BAGUS!', cheer_win: 'ISTIMEWA!',
    quit_t: 'MENU UTAMA', quit: 'Balik ke menu utama?\nGame ini akan berakhir.', yes: 'YA', no: 'TIDAK',
    set_title: '⚙ SETELAN TOON', set_anim: 'Animasi aktif', set_fx: 'Efek bintang & teks komik',
    set_bob: 'Kartu hijau/orange goyang', set_sound: 'Suara aktif', set_speed: 'Kecepatan animasi:', ok: 'OKE!',
    speed_names: { Lambat: 'Lambat', Normal: 'Normal', Cepat: 'Cepat' },
    bye: 'TERIMA KASIH SUDAH MAIN!\nTutup tab ini untuk keluar.',
    rotate: 'Putar HP kamu ke posisi miring',
  },
};
const LANG_NAMES = { en: 'English', id: 'Bahasa Indonesia' };

// ======================= WARNA & UKURAN =======================
const INK = '#1d1d2c', BAR = '#2e2048', BAR2 = '#3e2d5c';
const SKY_TOP = '#8e90d8', SKY_MID = '#9a6fa8', SKY_LOW = '#c98a86', FLOOR = '#3a2850', LAMP = '#ffb98a';
const PANEL = '#23935a', PANEL_H = '#1f8551', PANEL_LINE = '#3fcf86', SLOT = '#1c7a4a';
const FACE = '#fffaf0', DISC_FACE = '#ffd8c2', RED = '#e63946', PLAY_C = '#7bed6a', DISC_C = '#ff9f43', ACE_C = '#ffc2d1';
const DIM_FACE = '#cfd3d6', DIM_INK = '#7a7f85', SKY = '#4cc9f0', PINK = '#ff5d8f', YEL = '#ffd93d', PURP = '#9b5de5';
const PARTY = [YEL, PINK, SKY, PURP, PLAY_C, DISC_C, '#ffffff'];
const FONT = '"Hey Comic","Comic Sans MS","Chalkboard SE",cursive';
const SPEEDS = { Lambat: 0.6, Normal: 1.0, Cepat: 1.8 };

// papan main (ukuran dasar)
const CW = 1360, CH = 770;
const BOARD_BOX = [20, 14, 1110, 500], RIGHT_BOX = [1130, 14, 1340, 500], HAND_BOX = [20, 514, 1340, 760];
const BCARD_W = 58, BCARD_H = 82, ROW_Y = [89, 201, 313, 425], ROW_X0 = 190, ROW_STEP = 66;
const HAND_W = 62, HAND_H = 88, HAND_STEP = 70, SUIT_GAP = 16;
const HAND_CX = (HAND_BOX[0] + HAND_BOX[2]) / 2;
const LAST_C = [1235, 262], LAST_W = 112, LAST_H = 156;
// halaman depan & layar bagi kartu (ukuran dasar)
const MW = 1380, MH = 890;
const MENU_X = 300, MENU_Y0 = 430, MENU_STEP = 86, MENU_BW = 340, MENU_BH = 64;
const LOGO_H = 280, LOGO_Y = 180;
const DEAL_MS = 5000;
const OV_CHAR_H = 450, CHAR_TRIM_R = { win: 0, lose: 22 }, OV_RADIUS = 22;

const slotPos = (s, v) => [ROW_X0 + (v - 1) * ROW_STEP, ROW_Y[SUIT_ORDER[s]]];

// ======================= ALAT BANTU =======================
const lerp = (a, b, t) => a + (b - a) * t;
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const easeInOut = t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const easeOutBack = (t, s = 1.70158) => { t -= 1; return t * t * ((s + 1) * t + s) + 1; };
const rnd = (a, b) => a + Math.random() * (b - a);
const pick = arr => arr[Math.floor(Math.random() * arr.length)];
const now = () => performance.now();
const fmt = (s, o) => s.replace(/\{(\w+)\}/g, (_, k) => o[k]);

// ======================= SETELAN (disimpan di browser) =======================
const SET_KEY = 'sevenScop.settings';
const S = {
  lang: (navigator.language || 'en').toLowerCase().startsWith('id') ? 'id' : 'en',
  speed: 'Normal', anim: true, fx: true, bob: true, sound: true,
};
try { Object.assign(S, JSON.parse(localStorage.getItem(SET_KEY) || '{}')); } catch (e) { /* abaikan */ }
function saveSettings() { try { localStorage.setItem(SET_KEY, JSON.stringify(S)); } catch (e) { /* abaikan */ } }
const t = (k, o) => { const v = (TXT[S.lang] || TXT.en)[k]; return o ? fmt(v, o) : v; };
const mult = () => SPEEDS[S.speed] || 1;
const dur = ms => S.anim ? ms / mult() : 0;

// ======================= ASET =======================
const IMG = {};
for (const [k, f] of Object.entries({ menu: 'menu.jpg', deal: 'deal.jpg', logo: 'logo.png', win: 'win.png', lose: 'lose.png' })) {
  const im = new Image(); im.src = 'assets/img/' + f; IMG[k] = im;
}
const SND = {};
for (const k of ['deal', 'pow', 'perfect', 'yes', 'boom', 'win', 'lose']) {
  const a = new Audio('assets/snd/' + k + '.mp3'); a.preload = 'auto'; SND[k] = a;
}
const CHEER_SND = ['pow', 'perfect', 'yes', 'boom'];
function stopSound() { for (const a of Object.values(SND)) { try { a.pause(); a.currentTime = 0; } catch (e) { } } }
let audioUnlocked = false;
function unlockAudio() {
  if (audioUnlocked) return; audioUnlocked = true;
  for (const a of Object.values(SND)) {
    try {
      a._unlocking = true; a.muted = true;
      const p = a.play();
      const fin = () => { if (a._unlocking) { a.pause(); a.currentTime = 0; } a._unlocking = false; a.muted = false; };
      if (p && p.then) p.then(fin).catch(fin); else fin();
    } catch (e) { }
  }
}
function playSound(k) {
  if (!S.sound || !SND[k]) return;
  stopSound();
  SND[k]._unlocking = false; SND[k].muted = false;
  try { SND[k].currentTime = 0; const p = SND[k].play(); if (p && p.catch) p.catch(() => { }); } catch (e) { }
}
const imgReady = im => im && im.complete && im.naturalWidth > 0;

// ======================= KANVAS & SKALA =======================
const cv = document.getElementById('stage');
const ctx = cv.getContext('2d');
const topbar = document.getElementById('topbar');
const logEl = document.getElementById('log');
let DPR = 1, VW = 0, VH = 0;
// transform aktif: koordinat dasar -> layar
const view = { s: 1, ox: 0, oy: 0 };

// mode HP: COMPACT = HP posisi miring (bar di samping), PORTRAIT = HP posisi tegak (minta diputar)
let COMPACT = false, PORTRAIT = false;
const SAFE = { t: 0, r: 0, b: 0, l: 0 };
function readSafe() {
  const cs = getComputedStyle(document.getElementById('safe'));
  SAFE.t = parseFloat(cs.paddingTop) || 0; SAFE.r = parseFloat(cs.paddingRight) || 0;
  SAFE.b = parseFloat(cs.paddingBottom) || 0; SAFE.l = parseFloat(cs.paddingLeft) || 0;
}
function resize() {
  DPR = Math.min(window.devicePixelRatio || 1, 2);
  // ukuran layar yang BENAR-BENAR kelihatan (di HP, bar alamat browser tidak ikut dihitung)
  const vv = window.visualViewport;
  VW = Math.round(vv ? vv.width : window.innerWidth); VH = Math.round(vv ? vv.height : window.innerHeight);
  cv.width = Math.round(VW * DPR); cv.height = Math.round(VH * DPR);
  // ukuran tampil kanvas dikunci sama persis -> gambar tidak melar/terpotong
  cv.style.width = VW + 'px'; cv.style.height = VH + 'px';
  const small = Math.min(VW, VH) <= 560;
  const wasC = COMPACT;
  COMPACT = small && VW > VH; PORTRAIT = small && VH >= VW;
  document.body.classList.toggle('compact', COMPACT);
  document.body.classList.toggle('portrait', PORTRAIT);
  readSafe();
  if (wasC !== COMPACT && typeof applyLang === 'function') { applyLang(); if (ST.players.length) layoutHand(); }
}
window.addEventListener('resize', resize);
if (window.visualViewport) window.visualViewport.addEventListener('resize', resize);
window.addEventListener('orientationchange', () => setTimeout(resize, 200));

function fitView(bw, bh, area, alignX = 0.5, bx0 = 0, by0 = 0) {
  const s = Math.max(0.2, Math.min(area.w / bw, area.h / bh));
  view.s = s; view.ox = area.x + (area.w - bw * s) * alignX - bx0 * s; view.oy = area.y + (area.h - bh * s) / 2 - by0 * s;
  ctx.setTransform(DPR * s, 0, 0, DPR * s, DPR * view.ox, DPR * view.oy);
}
function screenTransform() { ctx.setTransform(DPR, 0, 0, DPR, 0, 0); }
const toBase = (x, y) => [(x - view.ox) / view.s, (y - view.oy) / view.s];
// area kelihatan dalam koordinat dasar
const visibleBase = () => [-view.ox / view.s, -view.oy / view.s, (VW - view.ox) / view.s, (VH - view.oy) / view.s];

// ======================= ALAT GAMBAR TOON =======================
function rrPath(x1, y1, x2, y2, r) {
  r = Math.max(0, Math.min(r, (x2 - x1) / 2, (y2 - y1) / 2));
  ctx.beginPath();
  ctx.moveTo(x1 + r, y1); ctx.lineTo(x2 - r, y1); ctx.quadraticCurveTo(x2, y1, x2, y1 + r);
  ctx.lineTo(x2, y2 - r); ctx.quadraticCurveTo(x2, y2, x2 - r, y2);
  ctx.lineTo(x1 + r, y2); ctx.quadraticCurveTo(x1, y2, x1, y2 - r);
  ctx.lineTo(x1, y1 + r); ctx.quadraticCurveTo(x1, y1, x1 + r, y1); ctx.closePath();
}
function polyPath(pts) { ctx.beginPath(); ctx.moveTo(pts[0], pts[1]); for (let i = 2; i < pts.length; i += 2) ctx.lineTo(pts[i], pts[i + 1]); ctx.closePath(); }
function starPts(cx, cy, r1, r2, n = 5, rot = 0) {
  const p = [];
  for (let i = 0; i < n * 2; i++) { const r = i % 2 ? r2 : r1, a = rot + Math.PI * i / n - Math.PI / 2; p.push(cx + Math.cos(a) * r, cy + Math.sin(a) * r); }
  return p;
}
const font = px => `bold ${Math.max(6, px)}px ${FONT}`;
// teks bergaris tepi (outline) + banyak baris
function text(str, x, y, size, fill, { stroke = 0, align = 'center', base = 'middle', lh = 1.32, strokeColor = INK } = {}) {
  ctx.font = font(size); ctx.textAlign = align; ctx.textBaseline = base === 'top' ? 'top' : 'middle';
  const lines = String(str).split('\n'), L = size * lh;
  let y0 = base === 'top' ? y : y - (lines.length - 1) * L / 2;
  for (const ln of lines) {
    if (stroke) { ctx.lineJoin = 'round'; ctx.lineWidth = stroke * 2.2; ctx.strokeStyle = strokeColor; ctx.strokeText(ln, x, y0); }
    ctx.fillStyle = fill; ctx.fillText(ln, x, y0); y0 += L;
  }
}
const measure = (str, size) => { ctx.font = font(size); return Math.max(...String(str).split('\n').map(l => ctx.measureText(l).width)); };

function toonPanel(x1, y1, x2, y2, fill) {
  rrPath(x1 + 6, y1 + 7, x2 + 6, y2 + 7, 22); ctx.fillStyle = INK; ctx.fill();
  rrPath(x1, y1, x2, y2, 22); ctx.fillStyle = fill; ctx.fill(); ctx.lineWidth = 4; ctx.strokeStyle = INK; ctx.stroke();
  ctx.lineCap = 'round'; ctx.lineWidth = 5; ctx.strokeStyle = PANEL_LINE;
  ctx.beginPath(); ctx.moveTo(x1 + 22, y1 + 11); ctx.lineTo(x1 + 90, y1 + 11); ctx.stroke();
  ctx.fillStyle = PANEL_LINE; ctx.beginPath(); ctx.arc(x1 + 103.5, y1 + 11.5, 3.5, 0, Math.PI * 2); ctx.fill();
}

function drawCard(cx, cy, w, h, card, { mode = 'full', face = FACE, dim = false, shadow = true } = {}) {
  const x1 = cx - w / 2, y1 = cy - h / 2, x2 = cx + w / 2, y2 = cy + h / 2, r = Math.min(w, h) * 0.2;
  let col = isRed(card.s) ? RED : INK, line = INK;
  if (dim) { col = DIM_INK; face = DIM_FACE; line = '#4a4a55'; }
  if (shadow) { rrPath(x1 + 4, y1 + 5, x2 + 4, y2 + 5, r); ctx.fillStyle = INK; ctx.fill(); }
  rrPath(x1, y1, x2, y2, r); ctx.fillStyle = face; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = line; ctx.stroke();
  if (w < h * 0.35) return;
  const fs1 = Math.max(6, h * 0.2), fs2 = Math.max(6, h * 0.42);
  text(card.r, x1 + w * 0.25, y1 + h * 0.15, fs1, col);
  text(card.s, cx, cy + h * 0.07, fs2, col);
  if (mode === 'big') text(card.r, x2 - w * 0.25, y2 - h * 0.15, fs1, col);
}
function drawBack(cx, cy, w, h) {
  const x1 = cx - w / 2, y1 = cy - h / 2, x2 = cx + w / 2, y2 = cy + h / 2, r = Math.min(w, h) * 0.2;
  rrPath(x1 + 4, y1 + 5, x2 + 4, y2 + 5, r); ctx.fillStyle = INK; ctx.fill();
  rrPath(x1, y1, x2, y2, r); ctx.fillStyle = PURP; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.stroke();
  if (w > 16) {
    ctx.setLineDash([4, 3]); rrPath(x1 + 6, y1 + 6, x2 - 6, y2 - 6, r * 0.6); ctx.lineWidth = 2; ctx.strokeStyle = YEL; ctx.stroke(); ctx.setLineDash([]);
    const rr = Math.min(w, h) * 0.22; polyPath(starPts(cx, cy, rr, rr * 0.45)); ctx.fillStyle = YEL; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = INK; ctx.stroke();
  }
}

// pita miring ala toon
function ribbonSize(str, px) { return [measure(str, px) + 60, str.split('\n').length * px * 1.3 + 34]; }
function drawRibbon(cx, cy, scale, angle, r) {
  if (scale < 0.06) return;
  let [w, h] = ribbonSize(r.text, r.px); w *= scale; h *= scale;
  ctx.save(); ctx.translate(cx, cy); ctx.rotate(-angle * Math.PI / 180);
  const x1 = -w / 2, y1 = -h / 2, x2 = w / 2, y2 = h / 2, e = 18 * scale, m = 4 * scale;
  const ends = [x1 - e, y1 + 8 * scale, x2 + e, y1 + 8 * scale, x2 + m, 4 * scale, x2 + e, y2 + 8 * scale, x1 - e, y2 + 8 * scale, x1 - m, 4 * scale];
  ctx.save(); ctx.translate(6, 7); polyPath(ends); ctx.fillStyle = INK; ctx.fill(); rrPath(x1, y1, x2, y2, 14 * scale); ctx.fill(); ctx.restore();
  polyPath(ends); ctx.fillStyle = r.tail; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.lineJoin = 'round'; ctx.stroke();
  rrPath(x1, y1, x2, y2, 14 * scale); ctx.fillStyle = r.fill; ctx.fill(); ctx.lineWidth = 4; ctx.stroke();
  ctx.lineCap = 'round'; ctx.lineWidth = 4; ctx.strokeStyle = '#fff';
  ctx.beginPath(); ctx.moveTo(x1 + 18 * scale, y1 + 11 * scale); ctx.lineTo(x1 + 60 * scale, y1 + 11 * scale); ctx.stroke();
  text(r.text, 0, 2 * scale, r.px * scale, r.tcol, { stroke: r.stroke });
  ctx.restore();
}

// ======================= TWEEN & JADWAL =======================
let tweens = [];
function tween(ms, fn, done) {
  const d = dur(ms);
  if (d <= 0) { fn(1); if (done) done(); return; }
  tweens.push({ t0: now(), d, fn, done });
}
function runTweens() {
  const tnow = now(), list = tweens; tweens = [];
  const keep = [];
  for (const tw of list) {
    const p = Math.min(1, (tnow - tw.t0) / tw.d);
    tw.fn(p);
    if (p >= 1) { if (tw.done) tw.done(); } else keep.push(tw);
  }
  tweens = keep.concat(tweens);
}
// setTimeout yang batal sendiri kalau game sudah diganti
let GEN = 0;
function later(ms, fn) { const g = GEN; setTimeout(() => { if (g === GEN) fn(); }, ms); }

// ======================= STATE =======================
const ST = {
  scene: 'menu',
  // game
  players: [], board: {}, current: 0, isFirst: true, active: false, busy: false, sort: 'warna',
  last: null, lastAnim: null, hidden: null, pop: null, fly: null, fx: [], comics: [],
  hand: [], hover: -1, wiggle: {}, dialog: null, overlay: null, pointer: [-1, -1],
  // menu
  menuItems: [], menuState: [], menuSel: 0, menuHeader: null, menuT0: 0, menuPending: false, floaters: [], bye: null,
  // bagi kartu
  dealT0: 0, dealN: 4, dealTok: 0,
};

function logLine(s) {
  const d = document.createElement('div'); d.textContent = s; logEl.appendChild(d);
  while (logEl.childNodes.length > 60) logEl.removeChild(logEl.firstChild);
  logEl.scrollTop = logEl.scrollHeight;
}

// ======================= LOGIKA GAME =======================
function getPlayable(hand) {
  const res = [];
  for (const c of hand) {
    const vals = RANK_VALUES[c.r];
    if (ST.isFirst) { if (c.s === '♠' && c.r === '7') res.push({ c, target: 7 }); continue; }
    const b = ST.board[c.s];
    if (!b.has7) { if (c.r === '7') res.push({ c, target: 7 }); }
    else {
      if (!b.lowClosed && vals.includes(b.low - 1)) res.push({ c, target: b.low - 1 });
      if (!b.highClosed && vals.includes(b.high + 1)) res.push({ c, target: b.high + 1 });
    }
  }
  return res;
}
function getDiscardable(hand) { const n = hand.filter(c => c.r !== '6' && c.r !== '8'); return n.length ? n : hand.slice(); }
const points = p => p.dead.concat(p.hand).reduce((a, c) => a + RANK_POINTS[c.r], 0);

function startGame(n) {
  GEN++; tweens = []; stopSound();
  ST.dialog = null; ST.overlay = null; ST.fly = null; ST.pop = null; ST.hidden = null; ST.fx = []; ST.comics = []; ST.wiggle = {};
  const deck = []; for (const s of SUITS) for (const r of RANKS) deck.push({ s, r });
  for (let i = deck.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [deck[i], deck[j]] = [deck[j], deck[i]]; }
  ST.players = [];
  for (let i = 0; i < n; i++) ST.players.push({ name: `P${i + 1}-` + (i === 0 ? t('you') : 'PC'), hand: [], dead: [], human: i === 0 });
  deck.forEach((c, i) => ST.players[i % n].hand.push(c));
  ST.board = {}; for (const s of SUITS) ST.board[s] = { has7: false, low: 7, high: 7, lowClosed: false, highClosed: false, placed: new Set() };
  ST.isFirst = true; ST.active = true; ST.busy = false; ST.last = null; ST.lastAnim = null;
  let starter = ST.players.findIndex(p => p.hand.some(c => c.s === '♠' && c.r === '7'));
  ST.current = Math.max(0, starter);
  logLine(t('log_start', { n, name: ST.players[ST.current].name }));
  refresh();
  if (ST.current !== 0) scheduleBot(); else comic(HAND_CX, 512, t('your_turn'), SKY, 24);
}

function scheduleBot() { later(S.anim ? 650 / mult() : 300, botTurn); }

function refresh() { layoutHand(); updateScores(); }

function cardOrigin(pi, card) {
  if (pi === 0) { const h = ST.hand.find(h => cardKey(h.c) === cardKey(card)); if (h) return [h.x, h.y + h.off, h.w, h.h]; }
  return [180 + pi * 230, -60, HAND_W, HAND_H];
}

function playCard(pi, card, target) {
  const p = ST.players[pi], b = ST.board[card.s], g = GEN;
  ST.busy = true;
  const start = cardOrigin(pi, card);
  const dest = b.has7 ? target : 7;
  p.hand = p.hand.filter(c => cardKey(c) !== cardKey(card));
  refresh();
  const [dx, dy] = slotPos(card.s, dest);
  fly(start, [dx, dy, BCARD_W, BCARD_H], card, !p.human, 'big', dest === 1 || dest === 14 ? ACE_C : FACE, () => {
    if (g !== GEN) return;
    if (!b.has7) { b.has7 = true; b.low = 7; b.high = 7; b.placed.add(7); }
    else if (target < 7) { b.low = target; b.placed.add(target); if (target === 1) b.lowClosed = true; }
    else if (target > 7) { b.high = target; b.placed.add(target); if (target === 14) b.highClosed = true; }
    ST.isFirst = false;
    popCard(card.s, dest);
    burst(dx, dy, 12, 'star');
    if (dest === 1 || dest === 14) comic(dx, dy - 52, t('closed'), PINK, 22);
    else if (p.human) { const i = Math.floor(Math.random() * 4); comic(dx, dy - 52, t('cheers')[i], RED, 22); playSound(CHEER_SND[i]); }
    ST.last = { card, kind: 'play', name: p.name };
    tween(380, k => ST.lastAnim = { scale: lerp(0.55, 1, easeOutBack(k)), dx: 0 }, () => ST.lastAnim = null);
    logLine(t('log_play', { name: p.name, card: cardStr(card) }));
    later(dur(240), nextTurn);
  });
}

function discardCard(pi, card) {
  const p = ST.players[pi], g = GEN;
  ST.busy = true;
  const start = cardOrigin(pi, card);
  p.hand = p.hand.filter(c => cardKey(c) !== cardKey(card));
  refresh();
  fly(start, [LAST_C[0], LAST_C[1], LAST_W, LAST_H], card, !p.human, 'big', DISC_FACE, () => {
    if (g !== GEN) return;
    p.dead.push(card);
    ST.last = { card, kind: 'disc', name: p.name };
    tween(440, k => ST.lastAnim = { scale: 1, dx: Math.sin(k * Math.PI * 8) * 10 * (1 - k) }, () => ST.lastAnim = null);
    burst(LAST_C[0], LAST_C[1] + 40, 9, 'smoke');
    comic(LAST_C[0], LAST_C[1] - 95, t('discard'), DISC_C, 22);
    logLine(t('log_disc', { name: p.name, card: cardStr(card) }));
    updateScores();
    later(dur(260), nextTurn);
  });
}

function nextTurn() {
  ST.busy = false;
  if (ST.players.every(p => p.hand.length === 0)) { refresh(); endGame(); return; }
  const n = ST.players.length;
  for (let i = 0; i < n; i++) { ST.current = (ST.current + 1) % n; if (ST.players[ST.current].hand.length) break; }
  refresh();
  if (ST.current !== 0) scheduleBot(); else comic(HAND_CX, 512, t('your_turn'), SKY, 24);
}

function botTurn() {
  if (!ST.active || ST.busy) return;
  if (ST.dialog) { later(200, botTurn); return; }
  const pi = ST.current; if (pi === 0) return;
  const p = ST.players[pi];
  if (!p.hand.length) { nextTurn(); return; }
  const pl = getPlayable(p.hand);
  if (pl.length) {
    pl.sort((a, b) => Math.abs(a.target - 7) - Math.abs(b.target - 7));
    let { c, target } = pl[0];
    const same = pl.filter(x => cardKey(x.c) === cardKey(c)).map(x => x.target);
    if (same.length > 1) target = same.includes(14) ? 14 : 1;
    playCard(pi, c, target);
  } else {
    const d = getDiscardable(p.hand).slice().sort((a, b) => RANK_POINTS[a.r] - RANK_POINTS[b.r]);
    discardCard(pi, d[0]);
  }
}

function humanClick(card) {
  if (ST.dialog || ST.overlay) return;
  if (!ST.active || ST.current !== 0 || ST.busy) return;
  const hand = ST.players[0].hand;
  const pl = getPlayable(hand);
  if (pl.length) {
    const m = pl.filter(x => cardKey(x.c) === cardKey(card));
    if (!m.length) { nope(card, t('pick_green'), t('cant')); return; }
    if (m.length > 1) {
      openDialog({
        title: t('ace_t'), msg: t('ace'), labels: [t('ace_top'), t('ace_bottom')], bw: 210, sel: 0, cancel: -1,
        onChoose: i => { if (i >= 0) playCard(0, card, i === 0 ? 14 : 1); },
      });
      return;
    }
    playCard(0, card, m[0].target);
  } else {
    if (!getDiscardable(hand).some(c => cardKey(c) === cardKey(card))) { nope(card, t('no68'), t('rule')); return; }
    discardCard(0, card);
  }
}

function nope(card, comicText, logText) {
  ST.wiggle[cardKey(card)] = now();
  const h = ST.hand.find(h => cardKey(h.c) === cardKey(card));
  if (S.fx && S.anim) comic(h ? h.x : HAND_CX, (h ? h.y : 600) - 78, comicText, RED, 18);
  else logLine(logText);
}

function endGame() {
  ST.active = false; updateScores();
  const scores = ST.players.map(p => ({ name: p.name, m: -points(p) }));
  let winner = scores[0];
  for (const s of scores) if (s.m > winner.m) winner = s;
  // yang kalah = minus terbanyak di antara pemain LAIN (kalau seri, tidak menulis pemenang dua kali)
  let loser = null;
  for (const s of scores) if (s !== winner && (!loser || s.m < loser.m)) loser = s;
  const humanWin = winner.name === ST.players[0].name;
  logLine(t('log_end', { name: winner.name, pts: winner.m }));
  showOverlay(humanWin ? t('win') : t('lose'),
    `${t('res_win')}: ${winner.name} ${winner.m}pts\n${t('res_lose')}: ${loser.name} ${loser.m}pts`,
    scores.map(s => `${s.name}: ${s.m}pts`).join('\n'), humanWin);
}

// ======================= TANGAN PEMAIN =======================
function layoutHand() {
  const old = {}; for (const h of ST.hand) old[cardKey(h.c)] = h.off;
  ST.hand = [];
  if (!ST.players.length) return;
  const human = ST.players[0];
  const sorted = human.hand.slice().sort(ST.sort === 'warna'
    ? (a, b) => SUIT_ORDER[a.s] - SUIT_ORDER[b.s] || RANK_SORT[a.r] - RANK_SORT[b.r]
    : (a, b) => RANK_SORT[a.r] - RANK_SORT[b.r] || SUIT_ORDER[a.s] - SUIT_ORDER[b.s]);
  const myTurn = ST.active && ST.current === 0 && !ST.busy;
  const pl = myTurn ? getPlayable(human.hand) : [];
  const playSet = new Set(pl.map(x => cardKey(x.c)));
  const discSet = myTurn && !pl.length ? new Set(getDiscardable(human.hand).map(cardKey)) : new Set();
  const rows = []; for (let i = 0; i < sorted.length; i += 13) rows.push(sorted.slice(i, i + 13));
  const rowY = rows.length <= 1 ? [650] : [600, 700];
  // HP: kalau cuma satu baris, kartu diperbesar supaya gampang disentuh
  const hs = COMPACT && rows.length <= 1 ? 1.22 : 1, CWd = HAND_W * hs, CHt = HAND_H * hs;
  const layout = rows.map(row => {
    const xs = []; let x = 0, prev = null;
    for (const c of row) { if (ST.sort === 'warna' && prev && prev !== c.s) x += SUIT_GAP * hs; xs.push(x); x += HAND_STEP * hs; prev = c.s; }
    return { row, xs };
  });
  // kotak info di kanan bawah: kalau baris bawah nabrak, geser & rapatkan
  const statsLeft = HAND_BOX[2] - 18 - 262 - 14;
  let shift = 0;
  layout.forEach((L, ri) => {
    if (!L.xs.length) return;
    const y = rowY[Math.min(ri, rowY.length - 1)], right = HAND_CX + (L.xs[L.xs.length - 1] + CWd) / 2;
    if (y + CHt / 2 > HAND_BOX[3] - 50 && right > statsLeft) shift = Math.max(shift, right - statsLeft);
  });
  let cx = HAND_CX;
  if (shift > 0) {
    const Lx = HAND_BOX[0] + 165, Rx = statsLeft - 6; cx = (Lx + Rx) / 2;
    for (const L of layout) if (L.xs.length && L.xs[L.xs.length - 1] + CWd > Rx - Lx) {
      const f = (Rx - Lx - CWd) / L.xs[L.xs.length - 1]; L.xs = L.xs.map(x => x * f);
    }
  }
  layout.forEach((L, ri) => {
    const total = L.xs.length ? L.xs[L.xs.length - 1] + CWd : 0, off = cx - total / 2 + CWd / 2;
    L.row.forEach((c, i) => {
      const k = cardKey(c), play = playSet.has(k), disc = discSet.has(k);
      ST.hand.push({ c, x: off + L.xs[i], y: rowY[Math.min(ri, rowY.length - 1)], w: CWd, h: CHt, play, disc, dim: !myTurn, off: old[k] || 0 });
    });
  });
}

function updateScores() {
  const box = document.getElementById('scores'); box.innerHTML = '';
  ST.players.forEach((p, i) => {
    const d = document.createElement('div');
    const turn = i === ST.current && ST.active;
    d.className = 'score' + (turn ? ' turn' : '');
    d.textContent = (turn ? '▶ ' : '') + p.name;
    box.appendChild(d);
  });
}

// ======================= ANIMASI GAME =======================
function fly(start, end, card, faceDown, endMode, endFace, onDone) {
  const [x0, y0, w0, h0] = start, [x1, y1, w1, h1] = end;
  const arc = Math.min(150, Math.hypot(x1 - x0, y1 - y0) * 0.35);
  ST.fly = { card, faceDown, endMode, endFace, x0, y0, w0, h0, x1, y1, w1, h1, arc, p: 0, prev: [x0, y0], lines: null };
  tween(540, k => { if (ST.fly) ST.fly.p = k; }, () => { ST.fly = null; onDone(); });
}
function popCard(s, v) {
  ST.hidden = s + v; ST.pop = { s, v, k: 0 };
  tween(420, k => { if (ST.pop) ST.pop.k = k; }, () => { if (ST.hidden === s + v) ST.hidden = null; ST.pop = null; });
}
function burst(x, y, n, kind) {
  if (!(S.fx && S.anim)) return;
  const parts = [];
  for (let i = 0; i < n; i++) {
    const a = rnd(0, Math.PI * 2), sp = kind === 'star' ? rnd(3, 7) : rnd(1, 3);
    parts.push({ x, y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - (kind === 'star' ? 2 : 1),
      col: kind === 'star' ? pick(PARTY) : pick(['#eeeeee', '#cfcfcf', '#b8b8b8']),
      r: kind === 'star' ? rnd(5, 9) : rnd(8, 14), rot: rnd(0, 6.28) });
  }
  ST.fx.push({ kind, parts, t0: now(), d: dur(620), last: now() });
}
function comic(x, y, str, color, size = 28) {
  if (!(S.fx && S.anim)) return;
  ST.comics.push({ x, y, str, color, size, t0: now(), d: dur(800) });
}

// ======================= DIALOG TOON (Back & As) =======================
function openDialog(o) {
  ST.dialog = Object.assign({ oy: -560, sel: 1, bw: 150, cancel: 1 }, o);
  tween(480, k => { if (ST.dialog) ST.dialog.oy = lerp(-560, 0, easeOutBack(k, 1.4)); });
}
function closeDialog(i) {
  const d = ST.dialog; if (!d) return;
  ST.dialog = null; cv.style.cursor = '';
  if (d.onChoose) d.onChoose(i);
}
function askMenu() {
  if (ST.overlay || !ST.active) { showMenu(); return; }
  if (ST.dialog) return;
  openDialog({ title: t('quit_t'), msg: t('quit'), labels: [t('yes'), t('no')], sel: 1, cancel: 1, onChoose: i => { if (i === 0) showMenu(); } });
}
function dlgBox() { const d = ST.dialog, W = 540, H = 300; return [CW / 2 - W / 2, CH / 2 - H / 2 + d.oy, CW / 2 + W / 2, CH / 2 + H / 2 + d.oy]; }
function dlgButtons() { const [x1, , x2, y2] = dlgBox(), cx = (x1 + x2) / 2, gap = ST.dialog.bw / 2 + 40; return [[cx - gap, y2 - 58], [cx + gap, y2 - 58]]; }
function drawDialog() {
  const d = ST.dialog; if (!d) return;
  const [vx0, vy0, vx1, vy1] = visibleBase();
  ctx.fillStyle = 'rgba(29,29,44,0.55)'; ctx.fillRect(vx0, vy0, vx1 - vx0, vy1 - vy0);
  const [x1, y1, x2, y2] = dlgBox(), cx = (x1 + x2) / 2;
  rrPath(x1 + 8, y1 + 9, x2 + 8, y2 + 9, 26); ctx.fillStyle = INK; ctx.fill();
  rrPath(x1, y1, x2, y2, 26); ctx.fillStyle = BAR2; ctx.fill(); ctx.lineWidth = 4; ctx.strokeStyle = INK; ctx.stroke();
  // jendela langit senja
  const hx1 = x1 + 16, hy1 = y1 + 16, hx2 = x2 - 16, hy2 = y1 + 100;
  const gr = ctx.createLinearGradient(0, hy1, 0, hy2); gr.addColorStop(0, SKY_TOP); gr.addColorStop(0.55, SKY_MID); gr.addColorStop(1, SKY_LOW);
  ctx.fillStyle = gr; ctx.fillRect(hx1, hy1, hx2 - hx1, hy2 - hy1);
  ctx.fillStyle = '#6a4f86';
  for (const [bx, bw, bh] of [[hx1 + 10, 46, 30], [hx1 + 70, 30, 42], [hx2 - 120, 38, 36], [hx2 - 70, 56, 26]]) ctx.fillRect(bx, hy2 - bh, bw, bh);
  for (const lx of [hx1 + 90, hx2 - 150]) {
    ctx.strokeStyle = INK; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(lx, hy1); ctx.lineTo(lx, hy1 + 14); ctx.stroke();
    polyPath([lx - 16, hy1 + 28, lx - 9, hy1 + 14, lx + 9, hy1 + 14, lx + 16, hy1 + 28]); ctx.fillStyle = LAMP; ctx.fill(); ctx.stroke();
    ctx.beginPath(); ctx.ellipse(lx, hy1 + 28, 5, 4, 0, 0, Math.PI * 2); ctx.fillStyle = '#fff1c9'; ctx.fill(); ctx.lineWidth = 1; ctx.stroke();
  }
  ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.strokeRect(hx1, hy1, hx2 - hx1, hy2 - hy1);
  text(d.title, cx, (hy1 + hy2) / 2 + 6, 30, YEL, { stroke: 3 });
  text(d.msg, cx, y1 + 148, 19, '#fff');
  dlgButtons().forEach(([bx, by], i) => {
    const on = i === d.sel, sc = on ? 1.08 : 1, w = d.bw * sc, h = 52 * sc;
    const fill = i === 0 ? (on ? YEL : '#c9b06a') : (on ? SKY_TOP : '#6f6aa8');
    rrPath(bx - w / 2 + 5, by - h / 2 + 6, bx + w / 2 + 5, by + h / 2 + 6, 16); ctx.fillStyle = INK; ctx.fill();
    rrPath(bx - w / 2, by - h / 2, bx + w / 2, by + h / 2, 16); ctx.fillStyle = fill; ctx.fill(); ctx.lineWidth = 4; ctx.strokeStyle = INK; ctx.stroke();
    ctx.lineCap = 'round'; ctx.lineWidth = 3; ctx.strokeStyle = '#fff';
    ctx.beginPath(); ctx.moveTo(bx - w / 2 + 14, by - h / 2 + 9); ctx.lineTo(bx - w / 2 + 44, by - h / 2 + 9); ctx.stroke();
    text(d.labels[i], bx, by, 22 * sc * (d.bw > 160 ? 0.82 : 1), INK);
  });
}
function dialogHit(x, y) { let r = -1; dlgButtons().forEach(([bx, by], i) => { if (Math.abs(x - bx) <= ST.dialog.bw / 2 + 6 && Math.abs(y - by) <= 30) r = i; }); return r; }

// ======================= POP UP MENANG / KALAH =======================
function showOverlay(title, summary, detail, win) {
  const o = { title, summary, detail, win, oy: -650, alpha: 0, rib: 0, swing: 0, t0: now(), conf: null };
  ST.overlay = o;
  playSound(win ? 'win' : 'lose');
  const g = GEN;
  if (S.anim) {
    tween(700, k => o.oy = lerp(-650, 0, easeOutBack(k, 1.3)));
    later(dur(450), () => {
      if (ST.overlay !== o) return;
      tween(600, k => o.alpha = k, () => {
        tween(520, k => { o.rib = Math.max(0.05, easeOutBack(k, 1.7)); o.swing = -14 * (1 - k) * Math.cos(k * Math.PI * 2.5); }, () => { o.rib = 1; o.swing = 0; });
      });
    });
    if (win && S.fx) {
      o.conf = Array.from({ length: 90 }, () => ({ x: rnd(0, CW), y: rnd(-400, -10), vx: rnd(-1.5, 1.5), vy: rnd(2.5, 5.5), c: pick(PARTY), p: rnd(0, 6.28) }));
      o.confEnd = now() + 3500 / mult();
    }
  } else { o.oy = 0; o.alpha = 1; o.rib = 1; }
  void g;
}
function closeOverlay() { ST.overlay = null; stopSound(); }

function drawOverlay(dtf) {
  const o = ST.overlay; if (!o) return;
  const [vx0, vy0, vx1, vy1] = visibleBase();
  ctx.fillStyle = 'rgba(29,29,44,0.55)'; ctx.fillRect(vx0, vy0, vx1 - vx0, vy1 - vy0);
  const bx1 = CW / 2 - 420, bx2 = CW / 2 + 420, by1 = 150 + o.oy, by2 = 620 + o.oy, tx = bx1 + 235;
  const pfill = o.win ? PURP : '#4a4e69';
  toonPanel(bx1, by1, bx2, by2, pfill);
  text(o.title, tx + (o.win ? 0 : 22), by1 + 68, 44, YEL, { stroke: 3 });
  const LH = 22 * 1.32, DATA_Y = by1 + 124;
  const LIST_Y = DATA_Y + o.summary.split('\n').length * LH + 10;
  const dataBottom = LIST_Y + o.detail.split('\n').length * LH;
  text(o.summary, bx1 + 48, DATA_Y, 22, '#fff', { stroke: 2, align: 'left', base: 'top' });
  text(o.detail, bx1 + 48, LIST_Y, 22, '#fff', { stroke: 2, align: 'left', base: 'top' });
  // karakter: fade in, pas di garis kanan & bawah, terpotong rapi di dalam kotak
  const im = o.win ? IMG.win : IMG.lose;
  if (imgReady(im) && o.alpha > 0) {
    const h = OV_CHAR_H, w = im.naturalWidth * h / im.naturalHeight, trim = CHAR_TRIM_R[o.win ? 'win' : 'lose'];
    ctx.save(); rrPath(bx1, by1, bx2, by2, OV_RADIUS); ctx.clip();
    ctx.globalAlpha = o.alpha;
    ctx.drawImage(im, bx2 - 2 + trim - w, by2 + 1 - h, w, h);
    ctx.restore();
    rrPath(bx1, by1, bx2, by2, 22); ctx.lineWidth = 4; ctx.strokeStyle = INK; ctx.stroke();
  }
  // pita di bawah nilai
  if (o.rib > 0) {
    const r = o.win ? { text: t('cheer_win'), px: 34, fill: YEL, tail: RED, tcol: RED, stroke: 2, angle: 3 }
      : { text: t('cheer_lose'), px: 18, fill: DISC_C, tail: PURP, tcol: INK, stroke: 0, angle: 3 };
    const [rw, rh] = ribbonSize(r.text, r.px), left = bx1 + 48, th = r.angle * Math.PI / 180, rcx = left + 18 + rw / 2;
    const dataW = Math.max(measure(o.summary, 22), measure(o.detail, 22));
    const xr = Math.min(left + dataW, rcx + rw / 2);
    const rcy = dataBottom + 6 + rh / 2 * Math.cos(th) + Math.max(0, xr - rcx) * Math.sin(th) + 3;
    const bob = (S.anim && o.rib >= 1) ? Math.round(Math.sin(now() / 1000 * 2.4 + 1) * 3) : 0;
    drawRibbon(rcx, rcy + bob, o.rib, r.angle + o.swing, r);
  }
  text(t('click_close'), (bx1 + bx2) / 2, by2 - 16, 13, SKY, { stroke: 1 });
  // confetti
  if (o.conf && now() < o.confEnd) {
    for (const q of o.conf) {
      q.x += (q.vx + Math.sin(q.p) * 1.2) * dtf; q.y += q.vy * dtf; q.p += 0.15 * dtf;
      const w = 6 * Math.abs(Math.cos(q.p)) + 1;
      ctx.fillStyle = q.c; ctx.fillRect(q.x - w, q.y - 4, w * 2, 8); ctx.lineWidth = 1; ctx.strokeStyle = INK; ctx.strokeRect(q.x - w, q.y - 4, w * 2, 8);
    }
  }
}

// ======================= GAMBAR LAYAR GAME =======================
function gameArea() {
  if (COMPACT) {          // HP miring: bar di kiri, papan memakai seluruh tinggi layar
    const side = topbar.offsetWidth || 66;
    return { x: side + 4, y: 4 + SAFE.t, w: VW - side - 8 - SAFE.r, h: VH - 8 - SAFE.t - SAFE.b };
  }
  const top = topbar.offsetHeight || 60, bottom = (logEl.offsetHeight || 40) + 10;
  return { x: 10, y: top + 4, w: VW - 20, h: VH - top - bottom - 8 };
}
function drawGame(dtf) {
  screenTransform();
  ctx.fillStyle = BAR; ctx.fillRect(0, 0, VW, VH);
  fitView(CW, CH, gameArea());
  // latar senja
  const [vx0, vy0, vx1, vy1] = visibleBase();
  const gr = ctx.createLinearGradient(0, 0, 0, CH);
  [[0, SKY_TOP], [0.45, SKY_MID], [0.66, SKY_LOW], [0.70, FLOOR], [1, '#2a1c3e']].forEach(([a, c]) => gr.addColorStop(a, c));
  ctx.fillStyle = gr; ctx.fillRect(vx0, vy0, vx1 - vx0, vy1 - vy0);
  toonPanel(...BOARD_BOX, PANEL); toonPanel(...RIGHT_BOX, PANEL); toonPanel(...HAND_BOX, PANEL_H);
  SUITS.forEach((s, i) => text(`${s} ${t('suits')[i]}`, 42, ROW_Y[i], 17, isRed(s) ? RED : FACE, { stroke: 2, align: 'left' }));
  text(t('last_card'), (RIGHT_BOX[0] + RIGHT_BOX[2]) / 2, 110, 20, YEL, { stroke: 2 });
  text(t('your_cards'), 40, 556, 18, YEL, { stroke: 2, align: 'left' });

  // papan
  for (const s of SUITS) {
    const b = ST.board[s], placed = b ? b.placed : new Set();
    for (let v = 1; v <= 14; v++) {
      const [x, y] = slotPos(s, v);
      if (placed.has(v)) { if (ST.hidden !== s + v) drawCard(x, y, BCARD_W, BCARD_H, { s, r: VAL_LABEL[v] }, { mode: 'big', face: v === 1 || v === 14 ? ACE_C : FACE }); }
      else {
        ctx.setLineDash(v === 7 ? [5, 4] : [3, 5]); rrPath(x - BCARD_W / 2, y - BCARD_H / 2, x + BCARD_W / 2, y + BCARD_H / 2, 11);
        ctx.lineWidth = v === 7 ? 3 : 2; ctx.strokeStyle = SLOT; ctx.stroke(); ctx.setLineDash([]);
        if (v === 7) text('7', x, y, 26, SLOT);
      }
    }
  }
  if (ST.pop) {
    const { s, v, k } = ST.pop, [x, y] = slotPos(s, v), q = Math.sin(k * Math.PI * 3) * (1 - k);
    drawCard(x, y, BCARD_W * (1 + 0.25 * q), BCARD_H * (1 - 0.2 * q), { s, r: VAL_LABEL[v] }, { mode: 'big', face: v === 1 || v === 14 ? ACE_C : FACE });
  }

  // kartu terakhir
  const [lx, ly] = LAST_C;
  if (!ST.last) {
    ctx.setLineDash([6, 5]); rrPath(lx - LAST_W / 2, ly - LAST_H / 2, lx + LAST_W / 2, ly + LAST_H / 2, 20);
    ctx.lineWidth = 3; ctx.strokeStyle = SLOT; ctx.stroke(); ctx.setLineDash([]);
    text('?', lx, ly, 54, PANEL_LINE, { stroke: 2 });
  } else {
    const a = ST.lastAnim || { scale: 1, dx: 0 }, L = ST.last;
    drawCard(lx + a.dx, ly, LAST_W * a.scale, LAST_H * a.scale, L.card, { mode: 'big', face: L.kind === 'play' ? FACE : DISC_FACE });
    if (L.kind === 'play') text(`${L.name}\n→ ${cardStr(L.card)}`, lx, ly + 118, 16, '#fff', { stroke: 2 });
    else text(t('disc_info', { name: L.name, card: cardStr(L.card) }), lx, ly + 124, 16, DISC_C, { stroke: 2 });
  }

  // tangan pemain (goyang + naik saat disorot)
  const ph = now() / 1000 * 4.5, kSm = 1 - Math.pow(0.55, dtf * 15 / 40);
  let hoverIdx = -1;
  if (!ST.dialog && !ST.overlay) {
    const [px, py] = ST.pointer;
    for (let i = ST.hand.length - 1; i >= 0; i--) {
      const h = ST.hand[i];
      if ((h.play || h.disc) && Math.abs(px - h.x) <= h.w / 2 && Math.abs(py - (h.y + h.off)) <= h.h / 2) { hoverIdx = i; break; }
    }
  }
  ST.hover = hoverIdx;
  ST.hand.forEach((h, i) => {
    let target = 0;
    if ((h.play || h.disc) && !h.dim) {
      if (S.bob && S.anim) target -= 3.5 * Math.sin(ph + i * 0.6);
      if (i === hoverIdx) target -= 12;
    }
    h.off += (target - h.off) * kSm;
  });
  const order = ST.hand.map((h, i) => i).filter(i => i !== hoverIdx); if (hoverIdx >= 0) order.push(hoverIdx);
  for (const i of order) {
    const h = ST.hand[i], w0 = ST.wiggle[cardKey(h.c)];
    let wx = 0;
    if (w0) { const k = (now() - w0) / Math.max(1, dur(360)); if (k >= 1) delete ST.wiggle[cardKey(h.c)]; else wx = Math.sin(k * Math.PI * 6) * 7 * (1 - k); }
    drawCard(h.x + wx, h.y + h.off, h.w, h.h, h.c, { face: h.play ? PLAY_C : h.disc ? DISC_C : FACE, dim: h.dim });
  }
  cv.style.cursor = (hoverIdx >= 0 || (ST.dialog && dialogHit(...ST.pointer) >= 0)) ? 'pointer' : '';

  // kotak info kartu kamu (kanan bawah)
  if (ST.players.length) {
    const p = ST.players[0], x2 = HAND_BOX[2] - 18, x1 = x2 - 262, y1 = HAND_BOX[3] - 50, y2 = HAND_BOX[3] - 14, cy = (y1 + y2) / 2;
    rrPath(x1 + 4, y1 + 5, x2 + 4, y2 + 5, 14); ctx.fillStyle = INK; ctx.fill();
    rrPath(x1, y1, x2, y2, 14); ctx.fillStyle = BAR2; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.stroke();
    text(`🃏 ${p.hand.length}`, x1 + 48, cy, 17, '#fff'); text(`💀 ${p.dead.length}`, x1 + 122, cy, 17, '#fff');
    text(`${-points(p)} pts`, x2 - 58, cy, 17, YEL);
  }

  // kartu terbang
  const f = ST.fly;
  if (f) {
    const e = easeInOut(f.p), grow = 1 + 0.28 * Math.sin(Math.PI * e);
    const x = lerp(f.x0, f.x1, e), y = lerp(f.y0, f.y1, e) - Math.sin(Math.PI * e) * f.arc;
    let w = lerp(f.w0, f.w1, e) * grow, h = lerp(f.h0, f.h1, e) * grow, back = false;
    if (f.faceDown) { w *= Math.max(0.06, Math.abs(Math.cos(Math.PI * e))); back = e < 0.5; }
    const vx = x - f.prev[0], vy = y - f.prev[1], d = Math.hypot(vx, vy), sp = d / Math.max(dtf, 0.05);  // kecepatan per ~15 ms
    if (sp > 3 && d > 0 && f.p < 0.95) {
      const ux = -vx / d, uy = -vy / d, pxn = -uy, pyn = ux, L = Math.min(40, sp * 3);
      ctx.lineCap = 'round'; ctx.lineWidth = 3; ctx.strokeStyle = '#fff';
      for (const kk of [-1, 0, 1]) {
        const bx = x + ux * (w * 0.5 + 6) + pxn * kk * h * 0.25, by = y + uy * (h * 0.3 + 6) + pyn * kk * h * 0.25;
        ctx.beginPath(); ctx.moveTo(bx, by); ctx.lineTo(bx + ux * L, by + uy * L); ctx.stroke();
      }
    }
    f.prev = [x, y];
    if (back) drawBack(x, y, w, h); else drawCard(x, y, w, h, f.card, { mode: e > 0.75 ? f.endMode : 'full', face: f.endFace });
  }

  drawFx(dtf);
  drawOverlay(dtf);
  drawDialog();
}

function drawFx(dtf) {
  const tn = now();
  ST.fx = ST.fx.filter(fx => {
    const k = Math.min(1, (tn - fx.t0) / fx.d);
    for (const p of fx.parts) {
      p.x += p.vx * dtf; p.y += p.vy * dtf;
      if (fx.kind === 'star') {
        p.vy += 0.35 * dtf; p.rot += 0.3 * dtf;
        const r = p.r * (1 - k); if (r < 1) continue;
        polyPath(starPts(p.x, p.y, r, r * 0.45, 5, p.rot)); ctx.fillStyle = p.col; ctx.fill(); ctx.lineWidth = 1.5; ctx.strokeStyle = INK; ctx.stroke();
      } else {
        const r = p.r * (0.6 + k) * (1 - k) * 1.6; if (r < 1) continue;
        ctx.beginPath(); ctx.arc(p.x, p.y, r, 0, Math.PI * 2); ctx.fillStyle = p.col; ctx.fill(); ctx.lineWidth = 2; ctx.strokeStyle = INK; ctx.stroke();
      }
    }
    return k < 1;
  });
  ST.comics = ST.comics.filter(cm => {
    const k = Math.min(1, (tn - cm.t0) / cm.d);
    let sc = easeOutBack(Math.min(1, k * 2.5)); if (k > 0.75) sc *= Math.max(0, (1 - k) / 0.25);
    if (sc > 0.05) {
      const yy = cm.y - 26 * k, R = (cm.str.length * cm.size * 0.36 + cm.size * 0.7) * sc;
      polyPath(starPts(cm.x + 4, yy + 5, R, R * 0.72, 14, 0.2)); ctx.fillStyle = INK; ctx.fill();
      polyPath(starPts(cm.x, yy, R, R * 0.72, 14, 0.2)); ctx.fillStyle = YEL; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.lineJoin = 'round'; ctx.stroke();
      text(cm.str, cm.x, yy, cm.size * sc, cm.color, { stroke: 2 });
    }
    return k < 1;
  });
}

// ======================= HALAMAN DEPAN =======================
function setMenu(header, items, sel = 0) {
  ST.menuHeader = header; ST.menuItems = items; ST.menuState = items.map(() => ({ h: 0, press: 0 }));
  ST.menuSel = sel; ST.menuT0 = now();
}
function menuMain(sel = 0) {
  setMenu(null, [
    { lab: () => t('new_game'), act: menuNew, style: 'main' },
    { lab: () => t('options'), act: () => menuOptions(0), style: 'main' },
    { lab: () => t('exit'), act: doExit, style: 'exit' },
  ], sel);
}
function menuNew() {
  setMenu('new_game', [
    { lab: () => t('p2'), act: () => showDeal(2), style: 'main' },
    { lab: () => t('p3'), act: () => showDeal(3), style: 'main' },
    { lab: () => t('p4'), act: () => showDeal(4), style: 'main' },
    { lab: () => t('back'), act: () => menuMain(0), style: 'back' },
  ]);
}
function menuOptions(sel = 0) {
  setMenu('options', [
    { lab: () => t('lang_now', { lang: LANG_NAMES[S.lang] }), act: menuLanguage, style: 'main' },
    { lab: () => t('back'), act: () => menuMain(1), style: 'back' },
  ], sel);
}
function menuLanguage() {
  const pickL = code => { S.lang = code; saveSettings(); applyLang(); };
  setMenu('language', [
    { lab: () => LANG_NAMES.en + (S.lang === 'en' ? '  ✓' : ''), act: () => pickL('en'), style: 'main' },
    { lab: () => LANG_NAMES.id + (S.lang === 'id' ? '  ✓' : ''), act: () => pickL('id'), style: 'main' },
    { lab: () => t('back'), act: () => menuOptions(0), style: 'back' },
  ], S.lang === 'en' ? 0 : 1);
}
function menuBack() {
  if (ST.menuHeader === 'language') menuOptions(0);
  else if (ST.menuHeader === 'options') menuMain(1);
  else if (ST.menuHeader === 'new_game') menuMain(0);
}
function doExit() {
  try { window.close(); } catch (e) { }
  ST.bye = now();          // browser biasanya tidak mengizinkan menutup tab -> tampilkan pesan
}
function menuActivate() {
  const i = ST.menuSel; if (ST.menuPending || i < 0 || i >= ST.menuItems.length) return;
  ST.menuState[i].press = 1; ST.menuPending = true;
  const act = ST.menuItems[i].act;
  setTimeout(() => { ST.menuPending = false; act(); }, S.anim ? 120 : 1);
}
function menuHit(x, y) {
  for (let i = 0; i < ST.menuItems.length; i++) { const cy = MENU_Y0 + i * MENU_STEP; if (Math.abs(x - MENU_X) <= MENU_BW / 2 + 10 && Math.abs(y - cy) <= MENU_BH / 2 + 4) return i; }
  return -1;
}
function drawCoverImage(im, anchorY = 0) {
  screenTransform();
  ctx.fillStyle = '#1a1230'; ctx.fillRect(0, 0, VW, VH);
  if (!imgReady(im)) return;
  const s = Math.max(VW / im.naturalWidth, VH / im.naturalHeight), w = im.naturalWidth * s, h = im.naturalHeight * s;
  ctx.drawImage(im, (VW - w) / 2, -(h - VH) * anchorY, w, h);
}
function drawMenu(dtf) {
  drawCoverImage(IMG.menu, 0);
  if (COMPACT) fitView(MW, 700, { x: SAFE.l, y: 0, w: VW - SAFE.l, h: VH }, 0.06, 0, 28);   // HP: perbesar logo & tombol
  else fitView(MW, MH, { x: 0, y: 0, w: VW, h: VH }, 0.15);
  const tn = now() / 1000, anim = S.anim, ph = tn * 2;
  // simbol kartu melayang
  if (!ST.floaters.length) ST.floaters = Array.from({ length: 10 }, () => ({ x: rnd(20, 620), y: rnd(0, MH), v: rnd(0.3, 0.9), ch: pick(SUITS), sz: rnd(18, 34), p: rnd(0, 6.28) }));
  for (const f of ST.floaters) {
    if (anim) { f.y -= f.v * dtf / 2; f.p += 0.01 * dtf; if (f.y < -30) { f.y = MH + 30; f.x = rnd(20, 620); } }
    text(f.ch, f.x + Math.sin(f.p) * 12, f.y, f.sz, isRed(f.ch) ? '#c07a9a' : '#8a78c0');
  }
  // logo
  const bob = anim ? Math.sin(ph) * 6 : 0;
  if (imgReady(IMG.logo)) {
    const h = LOGO_H, w = IMG.logo.naturalWidth * h / IMG.logo.naturalHeight;
    ctx.drawImage(IMG.logo, MENU_X - w / 2, LOGO_Y - h / 2 + bob, w, h);
  } else text('SEVEN SCOP', MENU_X, 150 + bob, 76, YEL, { stroke: 4 });
  if (ST.menuHeader) text(t(ST.menuHeader).toUpperCase(), MENU_X, MENU_Y0 - 78, 30, SKY, { stroke: 3 });
  // tombol
  const el = (now() - ST.menuT0) / 1000;
  const kSm = 1 - Math.pow(0.65, dtf * 15 / 30);
  ST.menuItems.forEach((it, i) => {
    const st = ST.menuState[i];
    const ap = anim ? clamp((el - i * 0.08) / 0.4, 0, 1) : 1, e = ap < 1 ? easeOutBack(ap) : 1;
    const tgt = i === ST.menuSel ? 1 : 0; st.h += (tgt - st.h) * (anim ? kSm : 1); st.press *= Math.pow(0.75, dtf * 15 / 30);
    const h = st.h, x = MENU_X + (1 - e) * -560 + h * 16, y = MENU_Y0 + i * MENU_STEP, sc = 1 + 0.06 * h - 0.1 * st.press;
    const w = MENU_BW * sc, hh = MENU_BH * sc;
    let fill, tcol;
    if (h > 0.5) { fill = it.style === 'exit' ? PINK : YEL; tcol = INK; }
    else { fill = { back: '#4a4e69', exit: '#7b2d3b' }[it.style] || BAR2; tcol = '#fff'; }
    rrPath(x - w / 2 + 6, y - hh / 2 + 7, x + w / 2 + 6, y + hh / 2 + 7, 18); ctx.fillStyle = INK; ctx.fill();
    rrPath(x - w / 2, y - hh / 2, x + w / 2, y + hh / 2, 18); ctx.fillStyle = fill; ctx.fill(); ctx.lineWidth = 4; ctx.strokeStyle = INK; ctx.stroke();
    ctx.lineCap = 'round'; ctx.lineWidth = 4; ctx.strokeStyle = '#fff';
    ctx.beginPath(); ctx.moveTo(x - w / 2 + 18, y - hh / 2 + 11); ctx.lineTo(x - w / 2 + 64, y - hh / 2 + 11); ctx.stroke();
    text(it.lab(), x, y, 26 * sc, tcol);
    if (h > 0.5) text('▶', x - w / 2 - 30 + (anim ? Math.sin(ph * 4) * 4 : 0), y, 26, YEL, { stroke: 2 });
  });
  if (!COMPACT) text(t('menu_hint'), 40, MH - 26, 14, '#e0d8ff', { align: 'left' });
  // pesan keluar
  if (ST.bye) {
    const k = (now() - ST.bye) / 3200;
    if (k >= 1) ST.bye = null;
    else {
      const sc = Math.max(0.05, easeOutBack(Math.min(1, k * 4), 1.7)) * (k > 0.85 ? Math.max(0.05, (1 - k) / 0.15) : 1);
      drawRibbon(MENU_X + 260, COMPACT ? MENU_Y0 + 270 : MH - 120, sc, 3, { text: t('bye'), px: 20, fill: YEL, tail: RED, tcol: INK, stroke: 0 });
    }
  }
  cv.style.cursor = menuHit(...ST.pointer) >= 0 ? 'pointer' : '';
}

// ======================= LAYAR "KARTU DIBAGIKAN" =======================
function showDeal(n) {
  GEN++; tweens = [];
  ST.active = false; ST.busy = false; ST.dialog = null; ST.overlay = null; ST.fly = null; ST.fx = []; ST.comics = [];
  ST.dealN = n; ST.scene = 'deal'; ST.dealT0 = now(); ST.dealTok++;
  topbar.classList.add('hidden'); logEl.classList.add('hidden');
  const tok = ST.dealTok;
  playSound('deal');                       // bunyi kartu dibalik, berulang selama 5 detik
  setTimeout(() => { if (tok === ST.dealTok && ST.scene === 'deal') dealFinish(); }, DEAL_MS);
}
function dealFinish() {
  if (ST.scene !== 'deal') return;
  ST.dealTok++; stopSound();
  ST.scene = 'game';
  topbar.classList.remove('hidden'); logEl.classList.remove('hidden');
  startGame(ST.dealN);
}
function drawDeal() {
  drawCoverImage(IMG.deal, 1 / 3);
  fitView(MW, MH, { x: 0, y: 0, w: VW, h: VH }, 0.5);
  const el = (now() - ST.dealT0) / 1000, anim = S.anim, rx = MW / 2, ry = MH / 2 - 30;
  const k = anim ? clamp((el - 0.15) / 0.55, 0, 1) : 1;
  if (k > 0) drawRibbon(rx, ry, Math.max(0.05, easeOutBack(k, 1.7)), -2 - 12 * (1 - k) * Math.cos(k * Math.PI * 2.5),
    { text: t('dealing'), px: 42, fill: YEL, tail: RED, tcol: RED, stroke: 2 });
  // kartu kecil loncat bergantian seperti loading
  SUITS.forEach((s, i) => {
    const x = rx + (i - 1.5) * 58; let y = ry + 112;
    if (anim) { const p = ((el * 1.6 - i * 0.18) % 1 + 1) % 1; if (p < 0.5) y -= Math.sin(p * 2 * Math.PI) * 22; }
    const cw = 40, ch = 56;
    rrPath(x - cw / 2 + 4, y - ch / 2 + 5, x + cw / 2 + 4, y + ch / 2 + 5, 8); ctx.fillStyle = INK; ctx.fill();
    rrPath(x - cw / 2, y - ch / 2, x + cw / 2, y + ch / 2, 8); ctx.fillStyle = FACE; ctx.fill(); ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.stroke();
    text(s, x, y + 2, 30, isRed(s) ? RED : INK);
  });
  cv.style.cursor = 'pointer';
}

// ======================= PINDAH LAYAR =======================
function showMenu() {
  GEN++; tweens = []; stopSound();
  ST.active = false; ST.busy = false; ST.dialog = null; ST.overlay = null; ST.fly = null; ST.fx = []; ST.comics = [];
  ST.scene = 'menu'; ST.dealTok++;
  topbar.classList.add('hidden'); logEl.classList.add('hidden');
  menuMain();
}
function applyLang() {
  document.documentElement.lang = S.lang;
  const B = { back: 'btn_menu', restart: 'btn_restart', sortSuit: 'sort_suit', sortRank: 'sort_rank', settings: 'settings' };
  const ICON = { back: '◄', restart: '↻', sortSuit: '♠♥', sortRank: '1-9', settings: '⚙' };
  document.querySelectorAll('#btns .tb').forEach(b => {
    b.textContent = COMPACT ? ICON[b.dataset.act] : t(B[b.dataset.act]);
    b.title = t(B[b.dataset.act]); b.setAttribute('aria-label', t(B[b.dataset.act]));
  });
  const rt = document.getElementById('rotateText'); if (rt) rt.textContent = t('rotate');
}

// ======================= SETELAN =======================
const setEl = document.getElementById('settings');
function openSettings() {
  document.getElementById('setTitle').textContent = t('set_title');
  document.getElementById('lblAnim').textContent = t('set_anim');
  document.getElementById('lblFx').textContent = t('set_fx');
  document.getElementById('lblBob').textContent = t('set_bob');
  document.getElementById('lblSound').textContent = t('set_sound');
  document.getElementById('lblSpeed').textContent = t('set_speed');
  document.querySelectorAll('[data-speed]').forEach(e => e.textContent = t('speed_names')[e.dataset.speed]);
  document.getElementById('setOk').textContent = t('ok');
  document.getElementById('optAnim').checked = S.anim; document.getElementById('optFx').checked = S.fx;
  document.getElementById('optBob').checked = S.bob; document.getElementById('optSound').checked = S.sound;
  document.querySelectorAll('input[name=speed]').forEach(r => r.checked = r.value === S.speed);
  setEl.classList.remove('hidden');
}
function closeSettings() {
  S.anim = document.getElementById('optAnim').checked; S.fx = document.getElementById('optFx').checked;
  S.bob = document.getElementById('optBob').checked; S.sound = document.getElementById('optSound').checked;
  const r = document.querySelector('input[name=speed]:checked'); if (r) S.speed = r.value;
  if (!S.sound) stopSound();
  saveSettings(); setEl.classList.add('hidden');
}
document.getElementById('setOk').addEventListener('click', closeSettings);
setEl.addEventListener('click', e => { if (e.target === setEl) closeSettings(); });

// ======================= INPUT =======================
document.getElementById('btns').addEventListener('click', e => {
  const b = e.target.closest('.tb'); if (!b) return;
  const a = b.dataset.act;
  if (a === 'back') askMenu();
  else if (a === 'restart') showDeal(ST.players.length || 4);
  else if (a === 'sortSuit') { ST.sort = 'warna'; layoutHand(); }
  else if (a === 'sortRank') { ST.sort = 'angka'; layoutHand(); }
  else if (a === 'settings') openSettings();
});

cv.addEventListener('pointermove', e => { ST.pointer = toBase(e.clientX, e.clientY); if (ST.scene === 'menu') { const i = menuHit(...ST.pointer); if (i >= 0) ST.menuSel = i; } if (ST.dialog) { const i = dialogHit(...ST.pointer); if (i >= 0) ST.dialog.sel = i; } });
let fsTried = false;
function tryFullscreen() {
  // Android: layar penuh + kunci posisi miring saat pertama disentuh (iPhone tidak mendukung, diabaikan)
  if (fsTried || !window.matchMedia('(pointer: coarse)').matches) return;
  fsTried = true;
  const el = document.documentElement;
  try {
    const p = el.requestFullscreen ? el.requestFullscreen({ navigationUI: 'hide' }) : null;
    const lock = () => { try { const q = screen.orientation && screen.orientation.lock && screen.orientation.lock('landscape'); if (q && q.catch) q.catch(() => { }); } catch (e) { } };
    if (p && p.then) p.then(lock).catch(() => { }); else lock();
  } catch (e) { }
}
cv.addEventListener('pointerdown', e => {
  unlockAudio(); tryFullscreen();
  ST.pointer = toBase(e.clientX, e.clientY);
  const [x, y] = ST.pointer;
  if (ST.scene === 'menu') { const i = menuHit(x, y); if (i >= 0) { ST.menuSel = i; menuActivate(); } return; }
  if (ST.scene === 'deal') { dealFinish(); return; }
  if (ST.overlay) { closeOverlay(); return; }
  if (ST.dialog) {
    const i = dialogHit(x, y);
    if (i >= 0) closeDialog(i);
    else { const [x1, y1, x2, y2] = dlgBox(); if (!(x1 <= x && x <= x2 && y1 <= y && y <= y2)) closeDialog(ST.dialog.cancel); }
    return;
  }
  for (let i = ST.hand.length - 1; i >= 0; i--) {
    const h = ST.hand[i];
    if (Math.abs(x - h.x) <= h.w / 2 && Math.abs(y - (h.y + h.off)) <= h.h / 2) { humanClick(h.c); return; }
  }
  // jari: pilih kartu terdekat kalau sentuhannya sedikit meleset
  if (e.pointerType === 'touch') {
    let best = null, bd = 1e9;
    for (const h of ST.hand) {
      const dx = Math.max(0, Math.abs(x - h.x) - h.w / 2), dy = Math.max(0, Math.abs(y - (h.y + h.off)) - h.h / 2), d = Math.hypot(dx, dy);
      if (d < bd) { bd = d; best = h; }
    }
    if (best && bd <= 14) humanClick(best.c);
  }
});

document.getElementById('btns').addEventListener('pointerdown', () => unlockAudio());
window.addEventListener('keydown', e => {
  unlockAudio();
  if (!setEl.classList.contains('hidden')) { if (e.key === 'Escape' || e.key === 'Enter') closeSettings(); return; }
  if (ST.scene === 'deal') { if (['Enter', ' ', 'Escape'].includes(e.key)) dealFinish(); return; }
  if (ST.scene === 'menu') {
    const n = ST.menuItems.length; if (!n) return;
    if (e.key === 'ArrowUp' || e.key === 'w') ST.menuSel = (ST.menuSel - 1 + n) % n;
    else if (e.key === 'ArrowDown' || e.key === 's') ST.menuSel = (ST.menuSel + 1) % n;
    else if (e.key === 'Enter' || e.key === ' ') menuActivate();
    else if (e.key === 'Escape') menuBack();
    e.preventDefault(); return;
  }
  if (ST.dialog) {
    if (['ArrowLeft', 'ArrowRight', 'Tab', 'a', 'd'].includes(e.key)) ST.dialog.sel = 1 - ST.dialog.sel;
    else if (e.key === 'Enter' || e.key === ' ') closeDialog(ST.dialog.sel);
    else if (e.key === 'Escape' || e.key === 'n') closeDialog(ST.dialog.cancel);
    else if (e.key === 'y' && ST.dialog.cancel === 1) closeDialog(0);
    e.preventDefault(); return;
  }
  if (ST.overlay && (e.key === 'Enter' || e.key === 'Escape' || e.key === ' ')) { closeOverlay(); return; }
  if (e.key === 'Escape') askMenu();
});

// ======================= LOOP UTAMA =======================
let lastT = now();
function frame() {
  const tn = now(), dtf = Math.min(4, (tn - lastT) / 15); lastT = tn;   // dtf = 1 pada ~66 fps (sama seperti versi desktop)
  runTweens();
  if (ST.scene === 'menu') drawMenu(dtf);
  else if (ST.scene === 'deal') drawDeal();
  else drawGame(dtf);
  requestAnimationFrame(frame);
}

// mulai
resize();
applyLang();
logLine(t('log_ready'));
menuMain();
// tunggu font Hey Comic siap (maks 2,5 detik) supaya tulisan pertama tidak pakai font cadangan
const fontReady = document.fonts && document.fonts.load ? document.fonts.load('40px "Hey Comic"').catch(() => { }) : Promise.resolve();
Promise.race([fontReady, new Promise(r => setTimeout(r, 2500))]).then(() => requestAnimationFrame(frame));

// untuk pengujian otomatis
window.__SS = { ST, S, startGame, showDeal, showMenu, endGame, humanClick, getPlayable, getDiscardable, points, askMenu, closeDialog,
  baseToScreen: (x, y) => [view.ox + x * view.s, view.oy + y * view.s] };
