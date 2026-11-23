#!/usr/bin/env python3
# Seven Scop - TOON EDITION
# Basis: Center Focus (aturan & logika main sama persis)
# Tampilan kartun: outline tebal, bayangan keras, warna cerah, font komik
# Animasi toon: kartu terbang melengkung + flip (bot), squash-pop saat mendarat,
#               bintang meletup, teks komik (POW!/TUTUP!/BUANG!), kartu goyang,
#               kartu terakhir nge-pop / gemeter, banner menang + confetti
# Menu ⚙ SETELAN: animasi on/off, kecepatan, efek, kartu goyang
# Halaman depan: New Game (3 / 4 Players), Options (Language: English / Indonesia), Exit
# Latar halaman depan: seven_scop_menu.png (taruh satu folder dengan file ini)

import tkinter as tk
from tkinter import messagebox
import random, math, time, os, json
try:
    import winsound                     # suara (Windows, bawaan Python)
except Exception:
    winsound=None
try:
    from PIL import Image, ImageTk, ImageDraw, ImageFont   # opsional: gambar menu mulus + judul ringan
    HAVE_PIL=True
except Exception:
    HAVE_PIL=False

SUITS = [('♠','Sekop'),('♥','Hati'),('♦','Wajik'),('♣','Keriting')]
SUIT_ORDER = {'♠':0,'♥':1,'♦':2,'♣':3}
RANK_VALUES = {'A':[1,14],'2':[2],'3':[3],'4':[4],'5':[5],'6':[6],'7':[7],'8':[8],'9':[9],'10':[10],'J':[11],'Q':[12],'K':[13]}
RANK_POINTS = {'A':15,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13}
RANKS = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
VERTICAL_ORDER = [14,13,12,11,10,9,8,7,6,5,4,3,2,1]
VAL_LABEL = {1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K',14:'A'}

def rank_sort(r):
    return {'A':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'10':10,'J':11,'Q':12,'K':13}[r]

# ================= PALET TOON =================
# ================= PALET (latar senja ikut gambar menu, papan & kartu tetap seperti semula) =================
INK="#1d1d2c"          # garis & bayangan: ungu sangat tua
BAR="#2e2048"          # bar atas, log, jendela setelan: plum tua
BAR2="#3e2d5c"         # kotak skor
SKY_TOP="#8e90d8"      # langit lavender (atas)
SKY_MID="#9a6fa8"      # ungu senja
SKY_LOW="#c98a86"      # cahaya jingga di cakrawala
FLOOR="#3a2850"        # lantai/meja bawah
LAMP="#ffb98a"         # cahaya lampu hangat
PANEL="#23935a"        # papan hijau (seperti sebelumnya)
PANEL_R="#23935a"      # panel kartu terakhir
PANEL_H="#1f8551"      # panel kartu kamu
PANEL_LINE="#3fcf86"
SLOT="#1c7a4a"
FACE="#fffaf0"
DISC_FACE="#ffd8c2"
RED="#e63946"
PLAY_C="#7bed6a"
DISC_C="#ff9f43"
ACE_C="#ffc2d1"
DIM_FACE="#cfd3d6"
DIM_INK="#7a7f85"
SKY="#4cc9f0"
PINK="#ff5d8f"
YEL="#ffd93d"
PURP="#9b5de5"
FONT="Comic Sans MS"
PARTY=[YEL,PINK,SKY,PURP,PLAY_C,DISC_C,"#ffffff"]
SPEEDS={'Lambat':0.6,'Normal':1.0,'Cepat':1.8}

HERE=os.path.dirname(os.path.abspath(__file__))

# ===== FONT: Hey Comic (khurasan, gratis untuk pemakaian pribadi; sudah ditambah angka 0 dan tanda : ;) =====
FONT_FILE=os.path.join(HERE,"HeyComic.ttf")
def _load_private_font(path):
    # Windows: muat font langsung dari folder game (tanpa install ke sistem)
    if os.name!='nt' or not os.path.exists(path): return False
    try:
        import ctypes
        return ctypes.windll.gdi32.AddFontResourceExW(ctypes.c_wchar_p(path), 0x10, 0) > 0   # 0x10 = FR_PRIVATE
    except Exception:
        return False
if _load_private_font(FONT_FILE):
    FONT="Hey Comic"
    FW="normal"     # Hey Comic sudah tebal; jangan ditebalkan lagi
else:
    FONT="Comic Sans MS"
    FW="bold"
MENU_BG=os.path.join(HERE,"seven_scop_menu.png")
LOGO_FILE=os.path.join(HERE,"seven_scop_logo.png")
LOGO_H=280          # tinggi logo di halaman depan (ukuran dasar, ikut membesar saat maximize)
LOGO_Y=180          # posisi tengah logo
BAR_LOGO_H=42       # tinggi logo di bar atas saat main
WIN_IMG=os.path.join(HERE,"seven_scop_win.png")     # karakter tepuk tangan (menang)
LOSE_IMG=os.path.join(HERE,"seven_scop_lose.png")   # karakter jempol (kalah)
OV_CHAR_H=450       # tinggi karakter di pop up hasil
CHAR_TRIM_R={'win':0,'lose':22}   # pangkas sisi kanan gambar (ukuran dasar) -> karakter bisa geser ke kanan
OV_RADIUS=22        # radius sudut kotak pop up (pojok gambar ikut dibulatkan)
DEAL_BG=os.path.join(HERE,"seven_scop_deal.png")    # layar "kartu dibagikan" sebelum game
DEAL_MS=5000        # lama layar kartu dibagikan (milidetik) = 5 detik
DEAL_DOTS_W=84      # ruang titik-titik di dalam pita
DEAL_SND=os.path.join(HERE,"seven_scop_deal.wav")   # suara kartu dibalik (5 detik, pas dengan animasi)
# suara saat kamu meletakkan kartu, urutannya sama dengan tulisan 'cheers': POW!, MANTAP!/PERFECT!, YES!, BOOM!
CHEER_SND=[os.path.join(HERE,f) for f in ("seven_scop_pow.wav","seven_scop_perfect.wav",
                                           "seven_scop_yes.wav","seven_scop_boom.wav")]
WIN_SND=os.path.join(HERE,"seven_scop_win.wav")     # tepuk tangan (Family Feud) saat menang
LOSE_SND=os.path.join(HERE,"seven_scop_lose.wav")   # sad trombone saat kalah
SETTINGS_FILE=os.path.join(HERE,"seven_scop_settings.json")

TXT={
 'en':{
  'suits':['Spades','Hearts','Diamonds','Clubs'],
  'new_game':'New Game','options':'Options','exit':'Exit','back':'◄ Back',
  'p2':'2 Players','p3':'3 Players','p4':'4 Players','language':'Language','lang_now':'Language: {lang}',
  'menu_hint':'↑ ↓  choose   •   Enter  select   •   Esc  back',
  'subtitle':'★ TOON EDITION ★',
  'btn_menu':'◄ Back','btn_restart':'↻ Restart','sort_suit':'Sort Suit','sort_rank':'Sort Rank','settings':'⚙ Settings',
  'last_card':'LAST\nCARD','your_cards':'YOUR CARDS',
  'hint':'Green = play  •  Orange = discard  •  Most minus loses',
  'you':'YOU','your_turn':'YOUR TURN!','pick_green':'PICK GREEN!','no68':'NOT 6/8!',
  'closed':'CLOSED!','cheers':['POW!','PERFECT!','YES!','BOOM!'],'discard':'DISCARD!',
  'disc_info':'{name}\nDISCARD\n{card}',
  'log_ready':'Ready! Pick New Game from the main menu.',
  'log_start':'{n}-player game - {name} starts with ♠7',
  'log_play':'{name} plays {card}','log_disc':'{name} discards {card}',
  'log_end':'Game over! Winner: {name} ({pts}pts)',
  'cant_t':'Not allowed','cant':'Pick a green card','rule_t':'Rule','rule':"You can't discard a 6/8 yet!",
  'ace_t':'Ace','ace':'YES = TOP (K → A)\nNO = BOTTOM (2 → A)',
  'win':'YOU WIN!','lose':'AWW, YOU LOST...','res_win':'WINNER','res_lose':'LOSER',
  'click_close':'click anywhere to close','dealing':'DEALING CARDS',
  'cheer_lose':"DON'T GIVE UP,\nYOU PLAYED GREAT!",'cheer_win':'EXCELLENT!',
  'quit_t':'MAIN MENU','quit':'Back to the main menu?\nThis game will end.','yes':'YES','no':'NO',
  'set_title':'⚙ TOON SETTINGS','set_anim':'Animations on','set_fx':'Stars & comic text',
  'set_bob':'Wobble green/orange cards','set_sound':'Sound on','set_speed':'Animation speed:','ok':'OK!',
  'speed_names':{'Lambat':'Slow','Normal':'Normal','Cepat':'Fast'},
 },
 'id':{
  'suits':['Sekop','Hati','Wajik','Keriting'],
  'new_game':'Main Baru','options':'Pengaturan','exit':'Keluar','back':'◄ Kembali',
  'p2':'2 Pemain','p3':'3 Pemain','p4':'4 Pemain','language':'Bahasa','lang_now':'Bahasa: {lang}',
  'menu_hint':'↑ ↓  pilih   •   Enter  oke   •   Esc  kembali',
  'subtitle':'★ EDISI TOON ★',
  'btn_menu':'◄ Kembali','btn_restart':'↻ Main Lagi','sort_suit':'Sort Warna','sort_rank':'Sort Angka','settings':'⚙ Setelan',
  'last_card':'KARTU\nTERAKHIR','your_cards':'KARTU KAMU',
  'hint':'Hijau = main  •  Orange = buang  •  Minus terbanyak kalah',
  'you':'KAMU','your_turn':'GILIRANMU!','pick_green':'PILIH HIJAU!','no68':'6/8 JANGAN!',
  'closed':'TUTUP!','cheers':['POW!','MANTAP!','YES!','BOOM!'],'discard':'BUANG!',
  'disc_info':'{name}\nBUANG\n{card}',
  'log_ready':'Siap! Pilih Main Baru di menu utama.',
  'log_start':'Game {n} pemain - {name} mulai ♠7',
  'log_play':'{name} main {card}','log_disc':'{name} buang {card}',
  'log_end':'Selesai! Menang: {name} ({pts}pts)',
  'cant_t':'Gak bisa','cant':'Pilih hijau','rule_t':'Aturan','rule':'Gak boleh buang 6/8 dulu!',
  'ace_t':'As','ace':'YES = ATAS (K → As)\nNO = BAWAH (2 → As)',
  'win':'KAMU MENANG!','lose':'YAAH, KALAH...','res_win':'MENANG','res_lose':'KALAH',
  'click_close':'klik di mana saja untuk tutup','dealing':'KARTU DIBAGIKAN',
  'cheer_lose':'JANGAN PATAH SEMANGAT,\nKAMU SUDAH BERMAIN BAGUS!','cheer_win':'ISTIMEWA!',
  'quit_t':'MENU UTAMA','quit':'Balik ke menu utama?\nGame ini akan berakhir.','yes':'YA','no':'TIDAK',
  'set_title':'⚙ SETELAN TOON','set_anim':'Animasi aktif','set_fx':'Efek bintang & teks komik',
  'set_bob':'Kartu hijau/orange goyang','set_sound':'Suara aktif','set_speed':'Kecepatan animasi:','ok':'OKE!',
  'speed_names':{'Lambat':'Lambat','Normal':'Normal','Cepat':'Cepat'},
 },
}
LANG_NAMES={'en':'English','id':'Bahasa Indonesia'}

# ================= LAYOUT =================
CANVAS_W, CANVAS_H = 1360, 770
BOARD_BOX=(20,14,1110,500)
RIGHT_BOX=(1130,14,1340,500)
HAND_BOX=(20,514,1340,760)
BOARD_CX=(BOARD_BOX[0]+BOARD_BOX[2])/2
COL_X=[BOARD_CX+(i-1.5)*120 for i in range(4)]
HEADER_Y=44
# kartu di papan: utuh, berjajar menyamping per baris jenis kartu
# kiri -> kanan: As(kecil) 2 3 4 5 6 [7] 8 9 10 J Q K As(besar)
BCARD_W, BCARD_H = 58, 82
ROW_Y=[89,201,313,425]   # baris Sekop, Hati, Wajik, Keriting
ROW_X0=190               # posisi As kecil
ROW_STEP=66              # jarak antar kartu
HAND_W, HAND_H = 62, 88
HAND_STEP=70
SUIT_GAP=16
HAND_CX=(HAND_BOX[0]+HAND_BOX[2])/2
LAST_C=(1235,262)
LAST_W, LAST_H = 112, 156
# halaman depan
MENU_W, MENU_H = 1380, 890
MENU_X=300
MENU_Y0=430
MENU_STEP=86
MENU_BW, MENU_BH = 340, 64

def slot_pos(s_char, v):
    return ROW_X0+(v-1)*ROW_STEP, ROW_Y[SUIT_ORDER[s_char]]

def rr_pts(x1,y1,x2,y2,r):
    r=max(1,min(r,(x2-x1)/2,(y2-y1)/2))
    return [x1+r,y1,x1+r,y1,x2-r,y1,x2-r,y1,x2,y1,x2,y1+r,x2,y1+r,x2,y2-r,x2,y2-r,
            x2,y2,x2-r,y2,x2-r,y2,x1+r,y2,x1+r,y2,x1,y2,x1,y2-r,x1,y2-r,x1,y1+r,x1,y1+r,x1,y1]

def star_pts(cx,cy,r1,r2,n=5,rot=0.0):
    pts=[]
    for i in range(n*2):
        r=r1 if i%2==0 else r2
        a=rot+math.pi*i/n-math.pi/2
        pts+= [cx+math.cos(a)*r, cy+math.sin(a)*r]
    return pts

_RING={}
def outline_ring(thick):
    # titik-titik melingkar rapat -> garis tepi tulisan tebal & utuh (tidak kelihatan dobel)
    thick=int(round(thick))
    if thick<=2:
        return [(dx,dy) for dx in (-thick,0,thick) for dy in (-thick,0,thick) if dx or dy]
    if thick not in _RING:
        pts=set()
        for r in range(1,thick+1):
            n=max(8,int(2*math.pi*r*1.6))
            for i in range(n):
                a=2*math.pi*i/n
                pts.add((round(math.cos(a)*r),round(math.sin(a)*r)))
        pts.discard((0,0))
        _RING[thick]=sorted(pts)
    return _RING[thick]

def lerp(a,b,t): return a+(b-a)*t


class ScaledCanvas(tk.Canvas):
    """Kanvas yang digambar di ukuran dasar, lalu otomatis membesar/mengecil
    mengikuti jendela (maximize) dengan proporsi tetap & posisi di tengah."""
    def __init__(self, master, base_w, base_h, align_x=0.5, **kw):
        super().__init__(master, width=base_w, height=base_h, highlightthickness=0, **kw)
        self.bw, self.bh = base_w, base_h
        self.align_x=align_x
        self.s=1.0; self.ox=0.0; self.oy=0.0
        self.on_rescale=None
        self._pending=None
        self.bind("<Configure>", self._on_conf, add="+")

    def _on_conf(self, e):
        s=max(0.3, min(e.width/self.bw, e.height/self.bh))
        ox=(e.width-self.bw*s)*self.align_x; oy=(e.height-self.bh*s)/2
        if abs(s-self.s)<1e-3 and abs(ox-self.ox)<0.5 and abs(oy-self.oy)<0.5:
            return
        self.s, self.ox, self.oy = s, ox, oy
        if self._pending: self.after_cancel(self._pending)
        self._pending=self.after(60, self._fire)

    def _fire(self):
        self._pending=None
        if self.on_rescale: self.on_rescale()

    def visible(self):
        # area kanvas yang kelihatan, dalam koordinat dasar (minimal seluas ukuran dasar)
        w=int(self.winfo_width() or 1); h=int(self.winfo_height() or 1)
        x0=-self.ox/self.s; y0=-self.oy/self.s
        x1=(w-self.ox)/self.s; y1=(h-self.oy)/self.s
        return min(0,x0), min(0,y0), max(self.bw,x1), max(self.bh,y1)

    def set_cursor(self, cur):
        # ganti kursor hanya kalau beda (Windows ikut menggambar ulang tiap kali diatur)
        if getattr(self,'_cur',None)!=cur:
            self._cur=cur
            self.config(cursor=cur)

    def to_base(self, x, y):
        return (x-self.ox)/self.s, (y-self.oy)/self.s

    def _xy(self, a):
        pts=list(a[0]) if len(a)==1 and isinstance(a[0],(list,tuple)) else list(a)
        s,ox,oy=self.s,self.ox,self.oy
        return [v*s+(ox if i%2==0 else oy) for i,v in enumerate(pts)]

    def _kw(self, kw):
        s=self.s
        if kw.get('width'):
            kw['width']=max(1, kw['width']*s)
        f=kw.get('font')
        if isinstance(f,tuple) and len(f)>=2 and isinstance(f[1],(int,float)):
            sz=f[1]*s
            sz=int(round(sz/2.0))*2 if abs(sz)>=12 else int(round(sz))   # kelipatan 2 -> font di-cache
            sz=sz or (-1 if f[1]<0 else 1)
            kw['font']=(f[0],sz)+tuple(f[2:])
        return kw

    def create_polygon(self,*a,**k):   return super().create_polygon(self._xy(a),**self._kw(k))
    def create_line(self,*a,**k):      return super().create_line(self._xy(a),**self._kw(k))
    def create_rectangle(self,*a,**k): return super().create_rectangle(self._xy(a),**self._kw(k))
    def create_oval(self,*a,**k):      return super().create_oval(self._xy(a),**self._kw(k))
    def create_text(self,*a,**k):      return super().create_text(*self._xy(a),**self._kw(k))
    def create_image(self,*a,**k):     return super().create_image(*self._xy(a),**k)
    def move(self,tag,dx,dy):          return super().move(tag,dx*self.s,dy*self.s)
    def create_image_px(self,x,y,**k): return super().create_image(x,y,**k)   # koordinat layar asli

def mix(c1, c2, t):
    a=[int(c1[i:i+2],16) for i in (1,3,5)]; b=[int(c2[i:i+2],16) for i in (1,3,5)]
    return '#%02x%02x%02x'%tuple(int(round(lerp(a[k],b[k],t))) for k in range(3))
def ease_in_out(t): return 4*t*t*t if t<.5 else 1-pow(-2*t+2,3)/2
def ease_out_back(t,s=1.70158):
    t-=1
    return t*t*((s+1)*t+s)+1


class ToonSeven:
    def __init__(self, root):
        global FONT, FW
        self.root=root
        if FONT=="Hey Comic":
            # pastikan Tk benar-benar mengenali font-nya; kalau tidak, kembali ke Comic Sans
            try:
                import tkinter.font as tkfont
                if "Hey Comic" not in tkfont.families(root):
                    FONT, FW = "Comic Sans MS", "bold"
            except Exception:
                pass
        self.root.title("Seven Scop")
        self.root.geometry("1380x890")
        self.root.configure(bg=BAR)
        self.root.minsize(900, 600)      # bisa di-resize & di-maximize
        try:
            self.root.state('zoomed')            # Windows: langsung maximize
        except Exception:
            try: self.root.attributes('-zoomed', True)   # Linux
            except Exception: pass
        self.num_players=tk.IntVar(value=4)
        self.lang=tk.StringVar(value="en")
        self.sort_mode=tk.StringVar(value="warna")
        # setelan
        self.anim_on=tk.BooleanVar(value=True)
        self.speed=tk.StringVar(value="Normal")
        self.fx_on=tk.BooleanVar(value=True)
        self.bob_on=tk.BooleanVar(value=True)
        self.sound_on=tk.BooleanVar(value=True)

        self.players=[]
        self.board={}
        self.current_idx=0
        self.is_first=True
        self.game_active=False
        self.busy=False
        self.gen=0
        self.fx_id=0
        self.hand_pos={}
        self.bob_off={}
        self.hover=None
        self.bob_phase=0.0
        self.last_state=None
        self.hidden_slot=None
        self.set_win=None
        self.dlg_open=False
        self.dlg_sel=1
        self.load_settings()
        self.build_ui()
        self.set_window_icon()
        self.build_menu()
        self.build_deal()
        self._tick()
        self._menu_tick()
        self.root.bind("<Key>", self.on_key)
        self.show_menu()

    # ================= BAHASA & SIMPAN SETELAN =================
    def t(self, key, **kw):
        v=TXT.get(self.lang.get(), TXT['en'])[key]
        return v.format(**kw) if kw else v

    def load_settings(self):
        try:
            with open(SETTINGS_FILE, encoding='utf-8') as f:
                d=json.load(f)
            if d.get('lang') in TXT: self.lang.set(d['lang'])
            if d.get('speed') in SPEEDS: self.speed.set(d['speed'])
            for k,var in (('anim',self.anim_on),('fx',self.fx_on),('bob',self.bob_on),('sound',self.sound_on)):
                if isinstance(d.get(k), bool): var.set(d[k])
        except Exception:
            pass

    def save_settings(self):
        try:
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump({'lang':self.lang.get(),'speed':self.speed.get(),'anim':self.anim_on.get(),
                           'fx':self.fx_on.get(),'bob':self.bob_on.get(),'sound':self.sound_on.get()}, f)
        except Exception:
            pass

    def relabel(self):
        for k,b in self.btns.items():
            b.config(text=self.t(k))
        self.draw_background()

    # ================= HALAMAN DEPAN =================
    def build_menu(self):
        c=self.mc=ScaledCanvas(self.root, MENU_W, MENU_H, align_x=0.15, bg="#1a1230")
        c.on_rescale=self.on_menu_rescale
        self.menu_img=None
        self.menu_pil=None
        if HAVE_PIL:
            try: self.menu_pil=Image.open(MENU_BG).convert('RGB')
            except Exception: self.menu_pil=None
        self.build_menu_bg()
        self.menu_visible=False
        self.menu_pending=False
        self.menu_items=[]
        self.menu_state=[]
        self.menu_header=None
        self.menu_sel=0
        self.menu_t0=time.perf_counter()
        c.bind("<Motion>", self.menu_motion)
        c.bind("<Button-1>", self.menu_click)

    def build_menu_bg(self):
        c=self.mc
        c.delete('mbg')
        x0,y0,x1,y1=c.visible()
        c.create_rectangle(x0,y0,x1,y1, fill="#1a1230", outline="", tags='mbg')
        img=None; full=False
        try:
            if self.menu_pil is not None:
                # gambar memenuhi SELURUH jendela (dipotong rapi di tepi kalau bentuk layar beda)
                W=max(1,int(c.winfo_width() or MENU_W)); H=max(1,int(c.winfo_height() or MENU_H))
                pw,ph=self.menu_pil.size               # ikut proporsi gambar aslinya (tidak gepeng)
                sc=max(W/pw, H/ph)
                iw=max(W,int(math.ceil(pw*sc))); ih=max(H,int(math.ceil(ph*sc)))
                big=self.menu_pil.resize((iw,ih), Image.LANCZOS)
                l=(iw-W)//2; t=0          # potong bagian bawah (lantai gelap), kepala tetap utuh
                img=ImageTk.PhotoImage(big.crop((l,t,l+W,t+H)))
                full=True
            else:
                img=tk.PhotoImage(file=MENU_BG)      # tanpa Pillow: ukuran asli, di tengah
        except Exception:
            img=None
        self.menu_img=img
        if img is not None and full:
            c.create_image_px(0, 0, image=img, anchor='nw', tags='mbg')
        elif img is not None:
            c.create_image(MENU_W/2, MENU_H/2, image=img, anchor='center', tags='mbg')
        else:
            for i in range(0,MENU_H,6):
                k=i/MENU_H
                col='#%02x%02x%02x'%(int(lerp(40,150,k)),int(lerp(28,80,k)),int(lerp(80,120,k)))
                c.create_rectangle(x0,i,x1,i+6,fill=col,outline='',tags='mbg')
        c.tag_lower('mbg')

    def on_menu_rescale(self):
        self.build_menu_bg()
        self.reset_menu_drawing()
        if self.menu_visible: self.draw_menu()

    def on_game_rescale(self):
        self.draw_background()
        self.refresh_all()
        if self.dlg_open: self.draw_dialog()
        if self.canvas.find_withtag('ovb') and getattr(self,'ov_args',None):
            self.canvas.delete('overlay')
            self.show_overlay(*self.ov_args, animate=False)

    def set_menu(self, header, items, sel=0):
        self.menu_header=header
        self.mc.delete('mhead'); self.mc.delete('mbtn'); self.mc.delete('marrow')
        self.mb_cache={}; self.arrow_pos=None
        self.menu_items=items          # (fungsi_label, aksi, gaya)
        self.menu_state=[{'h':0.0,'press':0.0} for _ in items]
        self.menu_sel=sel
        self.menu_t0=time.perf_counter()

    def menu_main(self, sel=0):
        self.set_menu(None, [(lambda: self.t('new_game'), self.menu_new, 'main'),
                             (lambda: self.t('options'), self.menu_options, 'main'),
                             (lambda: self.t('exit'), self.root.destroy, 'exit')], sel)

    def menu_new(self):
        self.set_menu('new_game', [(lambda: self.t('p2'), lambda: self.show_game(2), 'main'),
                                   (lambda: self.t('p3'), lambda: self.show_game(3), 'main'),
                                   (lambda: self.t('p4'), lambda: self.show_game(4), 'main'),
                                   (lambda: self.t('back'), lambda: self.menu_main(0), 'back')])

    def menu_options(self, sel=0):
        self.set_menu('options', [(lambda: self.t('lang_now', lang=LANG_NAMES[self.lang.get()]), self.menu_language, 'main'),
                                  (lambda: self.t('back'), lambda: self.menu_main(1), 'back')], sel)

    def menu_language(self):
        def pick(code):
            self.lang.set(code)
            self.reset_menu_drawing()
            self.save_settings()
            self.relabel()
        items=[(lambda cd=cd: LANG_NAMES[cd]+("  ✓" if self.lang.get()==cd else ""), lambda cd=cd: pick(cd), 'main')
               for cd in ('en','id')]
        items.append((lambda: self.t('back'), lambda: self.menu_options(0), 'back'))
        self.set_menu('language', items, 0 if self.lang.get()=='en' else 1)

    def menu_back(self):
        if self.menu_header=='language': self.menu_options(0)
        elif self.menu_header=='options': self.menu_main(1)
        elif self.menu_header=='new_game': self.menu_main(0)

    def menu_hit(self, x, y):
        for i in range(len(self.menu_items)):
            cy=MENU_Y0+i*MENU_STEP
            if abs(x-MENU_X)<=MENU_BW/2+10 and abs(y-cy)<=MENU_BH/2+4:
                return i
        return None

    def menu_motion(self, e):
        i=self.menu_hit(*self.mc.to_base(e.x, e.y))
        if i is not None and i!=self.menu_sel: self.menu_sel=i
        self.mc.set_cursor("hand2" if i is not None else "")

    def menu_click(self, e):
        i=self.menu_hit(*self.mc.to_base(e.x, e.y))
        if i is not None:
            self.menu_sel=i
            self.menu_activate()

    def menu_activate(self):
        i=self.menu_sel
        if self.menu_pending or not (0<=i<len(self.menu_items)): return
        self.menu_state[i]['press']=1.0
        act=self.menu_items[i][1]
        self.menu_pending=True
        def go():
            self.menu_pending=False
            act()
        self.root.after(120 if self.anim_on.get() else 1, go)

    def on_key(self, e):
        if getattr(self,'deal_visible',False):
            if e.keysym in ('Return','KP_Enter','space','Escape'): self.deal_skip()
            return
        if self.menu_visible:
            n=len(self.menu_items)
            if not n: return
            if e.keysym in ('Up','w','W'): self.menu_sel=(self.menu_sel-1)%n
            elif e.keysym in ('Down','s','S'): self.menu_sel=(self.menu_sel+1)%n
            elif e.keysym in ('Return','KP_Enter','space'): self.menu_activate()
            elif e.keysym=='Escape': self.menu_back()
        elif self.dlg_open:
            if e.keysym in ('Left','Right','Tab','a','d','A','D'):
                self.dlg_sel=1-self.dlg_sel; self.draw_dialog()
            elif e.keysym in ('Return','KP_Enter','space'):
                self.dialog_choose(self.dlg_sel==0)
            elif e.keysym in ('Escape','n','N'):
                self.dialog_choose(False)
            elif e.keysym in ('y','Y'):
                self.dialog_choose(True)
        elif e.keysym=='Escape':
            self.ask_menu()

    def _menu_tick(self):
        if self.menu_visible:
            self.draw_menu()
        self.root.after(30, self._menu_tick)

    # ----- tulisan besar jadi 1 gambar (ringan digerakkan, tidak perlu puluhan lapis teks) -----
    def _pil_font(self, px):
        if not hasattr(self,'_pf_cache'): self._pf_cache={}
        if px in self._pf_cache: return self._pf_cache[px]
        f=None
        for name in (FONT_FILE,"comicbd.ttf","C:/Windows/Fonts/comicbd.ttf","comic.ttf","C:/Windows/Fonts/comic.ttf",
                     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf","DejaVuSans-Bold.ttf","arialbd.ttf"):
            try:
                f=ImageFont.truetype(name, px); break
            except Exception:
                continue
        self._pf_cache[px]=f
        return f

    def text_img(self, text, size, fill, thick, c):
        if not HAVE_PIL: return None
        if not hasattr(self,'_timg'): self._timg={}
        key=(text,size,fill,thick,round(c.s,3))
        if key in self._timg: return self._timg[key]
        try:
            font=self._pil_font(max(6,int(round(size*c.s))))
            if font is None: return None
            st=max(1,int(round(thick*c.s)))
            l,t,r,b=ImageDraw.Draw(Image.new('RGBA',(1,1))).textbbox((0,0),text,font=font,stroke_width=st)
            im=Image.new('RGBA',(r-l+6,b-t+6),(0,0,0,0))
            ImageDraw.Draw(im).text((3-l,3-t),text,font=font,fill=fill,stroke_width=st,stroke_fill=INK)
            ph=ImageTk.PhotoImage(im)
        except Exception:
            return None
        self._timg[key]=ph
        return ph

    def big_text(self, x, y, text, size, fill, thick, tags, c):
        img=self.text_img(text, size, fill, thick, c)
        if img is not None:
            c.create_image(x, y, image=img, anchor='center', tags=tags)
        else:
            self.otext(x, y, text, size, fill, tags, thick=thick, c=c)

    def draw_menu(self):
        # Yang bergerak cuma DIGESER (bukan dibuat ulang); tombol digambar ulang hanya kalau berubah.
        c=self.mc
        now=time.perf_counter()
        anim=self.anim_on.get()
        ph=now*2.0
        if not hasattr(self,'mb_cache'): self.mb_cache={}
        # simbol kartu melayang di latar
        if not c.find_withtag('mfloat'):
            self.floaters=[]
            for i in range(10):
                f={'x':random.uniform(20,620),'y':random.uniform(0,MENU_H),'v':random.uniform(0.3,0.9),
                   'ch':random.choice('♠♥♦♣'),'sz':random.uniform(18,34),'p':random.uniform(0,6.28),'dx':0.0,'tag':f'mf{i}'}
                self._spawn_floater(f)
                self.floaters.append(f)
        if anim:
            for f in self.floaters:
                f['p']+=0.02
                ndx=math.sin(f['p'])*12
                c.move(f['tag'], ndx-f['dx'], -f['v'])
                f['dx']=ndx; f['y']-=f['v']
                if f['y']<-30:
                    c.delete(f['tag'])
                    f['y']=MENU_H+30; f['x']=random.uniform(20,620); f['dx']=0.0
                    self._spawn_floater(f)
        # judul + simbol kartu
        if not c.find_withtag('mtitle'):
            self.title_dy=0.0; self.suit_dy=[0.0]*4
            logo=self.logo_img(c)
            if logo is not None:
                c.create_image(MENU_X, LOGO_Y, image=logo, anchor='center', tags=('mtitle','mtitle_main'))
            else:   # file logo tidak ada -> tulisan seperti dulu
                self.big_text(MENU_X, 150, "SEVEN SCOP", 76, YEL, 4, ('mtitle','mtitle_main'), c)
                for k,s in enumerate('♠♥♦♣'):
                    self.otext(MENU_X-90+k*60, 232, s, 34, RED if s in '♥♦' else FACE, ('mtitle',f'msuit{k}'), thick=2, c=c)
        bob=math.sin(ph)*6 if anim else 0.0
        c.move('mtitle_main',0,bob-self.title_dy); self.title_dy=bob
        for k in range(4):
            sb=math.sin(ph*1.6+k)*5 if anim else 0.0
            c.move(f'msuit{k}',0,sb-self.suit_dy[k]); self.suit_dy[k]=sb
        if self.menu_header and not c.find_withtag('mhead'):
            self.big_text(MENU_X, MENU_Y0-78, self.t(self.menu_header).upper(), 30, SKY, 3, ('mhead',), c)
        if not c.find_withtag('mhint'):
            c.create_text(40, MENU_H-26, anchor='w', text=self.t('menu_hint'), fill="#e0d8ff",
                          font=(FONT,-14,FW), tags='mhint')
        # tombol: digambar ulang hanya kalau tampilannya berubah
        el=now-self.menu_t0
        arrow_at=None
        for i,(lab,_,style) in enumerate(self.menu_items):
            st=self.menu_state[i]
            ap=1.0 if not anim else max(0.0,min(1.0,(el-i*0.08)/0.4))
            e=ease_out_back(ap) if ap<1 else 1.0
            tgt=1.0 if i==self.menu_sel else 0.0
            st['h']+=(tgt-st['h'])*(0.35 if anim else 1.0)
            if abs(tgt-st['h'])<0.02: st['h']=tgt
            st['press']*=0.75
            if st['press']<0.02: st['press']=0.0
            h=st['h']
            x=MENU_X+(1-e)*-560+h*16
            y=MENU_Y0+i*MENU_STEP
            sc=1+0.06*h-0.1*st['press']
            if h>0.5:
                fill=PINK if style=='exit' else YEL; tcol=INK
            else:
                fill={'back':"#4a4e69",'exit':"#7b2d3b"}.get(style,BAR2); tcol="white"
            text=lab()
            key=(round(x,1),round(sc,3),fill,text)
            w=MENU_BW*sc; hh=MENU_BH*sc
            if h>0.5: arrow_at=(x-w/2-30,y)
            if self.mb_cache.get(i)==key: continue
            self.mb_cache[i]=key
            tg=('mbtn',f'mb{i}')
            c.delete(f'mb{i}')
            c.create_polygon(rr_pts(x-w/2+6,y-hh/2+7,x+w/2+6,y+hh/2+7,18), smooth=True, fill=INK, outline='', tags=tg)
            c.create_polygon(rr_pts(x-w/2,y-hh/2,x+w/2,y+hh/2,18), smooth=True, fill=fill, outline=INK, width=4, tags=tg)
            c.create_line(x-w/2+18,y-hh/2+11,x-w/2+64,y-hh/2+11, fill="white", width=4, capstyle='round', tags=tg)
            c.create_text(x, y, text=text, font=(FONT,-int(26*sc),FW), fill=tcol, tags=tg)
        # panah ▶: naik-turun pelan, cuma digeser
        if arrow_at is None:
            c.delete('marrow'); self.arrow_pos=None
        else:
            bob=math.sin(ph*4)*4 if anim else 0.0
            pos=(arrow_at[0]+bob, arrow_at[1])
            if getattr(self,'arrow_pos',None) is None or not c.find_withtag('marrow'):
                c.delete('marrow')
                self.otext(pos[0], pos[1], "▶", 26, YEL, ('marrow',), thick=2, c=c)
            else:
                c.move('marrow', pos[0]-self.arrow_pos[0], pos[1]-self.arrow_pos[1])
            self.arrow_pos=pos
        c.tag_raise('marrow')

    def logo_img(self, c):
        # logo ikut ukuran layar; disimpan per skala supaya tidak dibuat ulang terus
        if not hasattr(self,'_logo_cache'): self._logo_cache={}
        key=round(c.s,3)
        if key in self._logo_cache: return self._logo_cache[key]
        img=None
        try:
            if HAVE_PIL:
                src=self.logo_source()
                h=max(10,int(round(LOGO_H*c.s)))
                img=ImageTk.PhotoImage(src.resize((max(1,round(src.width*h/src.height)),h), Image.LANCZOS))
            else:
                raw=tk.PhotoImage(file=LOGO_FILE)
                n=max(1,int(round(raw.height()/(LOGO_H*c.s))))
                img=raw.subsample(n,n)
        except Exception:
            img=None
        self._logo_cache[key]=img
        return img

    def logo_source(self):
        # logo asli dibaca SEKALI: bagian transparen di pinggir dibuang (biar ukurannya pas),
        # lalu disimpan di memori -> berpindah ukuran / maximize tetap cepat. Isi logo tidak diubah.
        if getattr(self,'_logo_src',None) is None:
            im=Image.open(LOGO_FILE).convert('RGBA')
            bb=im.getbbox()
            if bb: im=im.crop(bb)
            if im.height>1400:
                im=im.resize((round(im.width*1400/im.height),1400), Image.LANCZOS)
            self._logo_src=im
        return self._logo_src

    def small_logo(self, h):
        # logo kecil dengan tinggi tetap (untuk bar atas / ikon)
        try:
            if HAVE_PIL:
                src=self.logo_source()
                return ImageTk.PhotoImage(src.resize((max(1,round(src.width*h/src.height)),h), Image.LANCZOS))
            raw=tk.PhotoImage(file=LOGO_FILE)
            return raw.subsample(max(1,raw.height()//h))
        except Exception:
            return None

    def set_window_icon(self):
        # logo juga dipakai sebagai ikon jendela & taskbar
        try:
            if HAVE_PIL:
                src=self.logo_source()
                self._icon=ImageTk.PhotoImage(src.resize((round(src.width*64/src.height),64), Image.LANCZOS))
            else:
                raw=tk.PhotoImage(file=LOGO_FILE)
                self._icon=raw.subsample(max(1,raw.height()//64))
            self.root.iconphoto(True, self._icon)
        except Exception:
            pass

    def _spawn_floater(self, f):
        c=self.mc
        c.create_text(f['x'], f['y'], text=f['ch'], font=(FONT,-int(f['sz']),FW),
                      fill="#8a78c0" if f['ch'] in '♠♣' else "#c07a9a", tags=('mfloat',f['tag']))
        c.tag_raise(f['tag'],'mbg')

    def reset_menu_drawing(self):
        c=self.mc
        for tg in ('mbtn','marrow','mhint','mtitle','mhead','mfloat'):
            c.delete(tg)
        self.mb_cache={}
        self.arrow_pos=None

    def show_menu(self):
        self.gen+=1
        self.game_active=False
        self.busy=False
        self.dlg_open=False
        for tg in ('overlay','fly','pop','fx','dlg'):
            self.canvas.delete(tg)
        if self.set_win is not None and self.set_win.winfo_exists():
            self.set_win.destroy()
        self.game_frame.pack_forget()
        self.stop_sound()
        self.deal_visible=False; self.deal_token+=1; self.dc.pack_forget()
        self.mc.pack(fill=tk.BOTH, expand=True)
        self.menu_visible=True
        self.menu_main()
        self.root.focus_set()

    def show_game(self, n):
        self.show_deal(n)

    # ================= LAYAR "KARTU DIBAGIKAN" =================
    def build_deal(self):
        c=self.dc=ScaledCanvas(self.root, MENU_W, MENU_H, bg="#1a1230")
        c.on_rescale=self.on_deal_rescale
        self.deal_pil=None
        if HAVE_PIL:
            try: self.deal_pil=Image.open(DEAL_BG).convert('RGB')
            except Exception: self.deal_pil=None
        self.deal_visible=False
        self.deal_token=0
        self.deal_img=None
        c.bind("<Button-1>", lambda e: self.deal_skip())

    def build_deal_bg(self):
        # gambar memenuhi seluruh jendela (sama seperti halaman depan)
        c=self.dc
        c.delete('dbg')
        x0,y0,x1,y1=c.visible()
        c.create_rectangle(x0,y0,x1,y1, fill="#1a1230", outline="", tags='dbg')
        img=None; full=False
        try:
            if self.deal_pil is not None:
                W=max(1,int(c.winfo_width() or MENU_W)); H=max(1,int(c.winfo_height() or MENU_H))
                pw,ph=self.deal_pil.size
                sc=max(W/pw, H/ph)
                iw=max(W,int(math.ceil(pw*sc))); ih=max(H,int(math.ceil(ph*sc)))
                big=self.deal_pil.resize((iw,ih), Image.LANCZOS)
                l=(iw-W)//2; t=(ih-H)//3
                img=ImageTk.PhotoImage(big.crop((l,t,l+W,t+H))); full=True
            else:
                img=tk.PhotoImage(file=DEAL_BG)
        except Exception:
            img=None
        self.deal_img=img
        if img is not None and full:
            c.create_image_px(0, 0, image=img, anchor='nw', tags='dbg')
        elif img is not None:
            c.create_image(MENU_W/2, MENU_H/2, image=img, anchor='center', tags='dbg')
        c.tag_lower('dbg')

    def on_deal_rescale(self):
        if not self.deal_visible: return
        self.build_deal_bg()
        self.dc.delete('ddyn'); self.deal_drawn=False

    def show_deal(self, n):
        self.num_players.set(n)
        self.gen+=1
        self.game_active=False; self.busy=False
        self.dlg_open=False
        for tg in ('overlay','fly','pop','fx','dlg'):
            self.canvas.delete(tg)
        self.menu_visible=False
        self.mc.pack_forget(); self.game_frame.pack_forget()
        self.dc.pack(fill=tk.BOTH, expand=True)
        self.deal_visible=True
        self.deal_token+=1; tok=self.deal_token
        self.build_deal_bg()
        self.dc.delete('ddyn'); self.deal_drawn=False
        self.deal_t0=time.perf_counter()
        self.deal_rib=dict(text=self.t('dealing'), font_px=42, fill=YEL, tail=RED, tcol=RED, stroke=2, angle=-2,
                           canvas=self.dc)
        self.deal_suit_dy=[0]*4
        self.play_sound(DEAL_SND)          # bunyi kartu dibalik, berulang selama 5 detik
        self._deal_tick(tok)
        self.root.after(int(DEAL_MS), lambda: tok==self.deal_token and self.deal_finish())   # tetap 5 detik

    def _deal_tick(self, tok):
        if tok!=self.deal_token or not self.deal_visible: return
        c=self.dc
        el=time.perf_counter()-self.deal_t0
        anim=self.anim_on.get()
        rx,ry=MENU_W/2, MENU_H/2-30          # pita di tengah layar
        # pita: muncul memantul sambil berayun, lalu diam
        k=1.0 if not anim else min(1.0, max(0.0,(el-0.15)/0.55))
        if k<1.0 or not self.deal_drawn:
            c.delete('drib')
            if k>0:
                self.draw_ribbon(rx, ry, max(0.05,ease_out_back(k,1.7)), self.deal_rib['angle']-12*(1-k)*math.cos(k*math.pi*2.5),
                                 ('ddyn','drib'), **{kk:v for kk,v in self.deal_rib.items() if kk!='angle'})
        # kartu-kartu kecil di bawah pita, loncat bergantian seperti loading
        if not c.find_withtag('dcard0'):
            self.deal_suit_dy=[0]*4
            cw,ch=40,56
            for i,s in enumerate('♠♥♦♣'):
                x=rx+(i-1.5)*58; y=ry+112
                tg=('ddyn',f'dcard{i}')
                c.create_polygon(rr_pts(x-cw/2+4,y-ch/2+5,x+cw/2+4,y+ch/2+5,8), smooth=True, fill=INK, outline="", tags=tg)
                c.create_polygon(rr_pts(x-cw/2,y-ch/2,x+cw/2,y+ch/2,8), smooth=True, fill=FACE, outline=INK, width=3, tags=tg)
                c.create_text(x, y+2, text=s, font=(FONT,-30,FW), fill=RED if s in '♥♦' else INK, tags=tg)
        if anim:
            for i in range(4):
                ph=(el*1.6-i*0.18)%1.0                      # gelombang: kartu loncat satu per satu
                dy=int(round(-math.sin(ph*2*math.pi)*22)) if ph<0.5 else 0
                if dy!=self.deal_suit_dy[i]:
                    c.move(f'dcard{i}',0,dy-self.deal_suit_dy[i]); self.deal_suit_dy[i]=dy
        if k>=1.0: self.deal_drawn=True
        self.root.after(30, lambda: self._deal_tick(tok))

    def play_sound(self, path):
        if winsound is None or not self.sound_on.get() or not os.path.exists(path): return
        try:
            winsound.PlaySound(path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NODEFAULT)
        except Exception:
            pass

    def stop_sound(self):
        if winsound is None: return
        try:
            winsound.PlaySound(None, 0)
        except Exception:
            pass

    def deal_skip(self):
        if self.deal_visible:
            self.deal_finish()

    def deal_finish(self):
        if not self.deal_visible: return
        self.deal_visible=False
        self.deal_token+=1
        self.stop_sound()                  # berhenti saat masuk game (termasuk kalau dilewati)
        self.dc.delete('ddyn')
        self.dc.pack_forget()
        self.game_frame.pack(fill=tk.BOTH, expand=True)
        self.relabel()
        self.start_game(self.num_players.get())

    def ask_menu(self):
        if not self.game_active:
            self.show_menu(); return
        if self.dlg_open: return
        self.dlg_open=True
        self.dlg_sel=1            # default: NO (biar aman)
        self.dlg_oy=0.0
        c=self.canvas
        c.tag_bind('dlg', "<Motion>", self.dialog_motion)
        c.tag_bind('dlg', "<Button-1>", self.dialog_click)
        def frame(t):
            if not self.dlg_open: return
            self.dlg_oy=lerp(-560, 0, ease_out_back(t, 1.4))
            self.draw_dialog()
        self.tween(480, frame)

    # ----- kotak konfirmasi bergaya toon, nuansa senja -----
    DLG_W, DLG_H = 540, 300
    def dlg_box(self):
        cx, cy = CANVAS_W/2, CANVAS_H/2
        return cx-self.DLG_W/2, cy-self.DLG_H/2+self.dlg_oy, cx+self.DLG_W/2, cy+self.DLG_H/2+self.dlg_oy

    def dlg_buttons(self):
        x1,y1,x2,y2=self.dlg_box()
        cx=(x1+x2)/2; by=y2-58
        return [(cx-115, by), (cx+115, by)]   # 0 = YES, 1 = NO

    def draw_dialog(self):
        c=self.canvas
        c.delete('dlg')
        if not self.dlg_open: return
        x1,y1,x2,y2=self.dlg_box()
        cx=(x1+x2)/2
        tags=('dlg',)
        c.create_rectangle(*c.visible(), fill=INK, stipple='gray50', outline="", tags=tags)
        # badan kotak: plum, outline tebal, bayangan keras
        c.create_polygon(rr_pts(x1+8,y1+9,x2+8,y2+9,26), smooth=True, fill=INK, outline="", tags=tags)
        c.create_polygon(rr_pts(x1,y1,x2,y2,26), smooth=True, fill=BAR2, outline=INK, width=4, tags=tags)
        # jendela langit senja di bagian atas (gradasi seperti gambar menu)
        hx1,hy1,hx2,hy2=x1+16,y1+16,x2-16,y1+100
        stops=[(0.0,SKY_TOP),(0.55,SKY_MID),(1.0,SKY_LOW)]
        for yy in range(int(hy1), int(hy2), 3):
            k=(yy-hy1)/(hy2-hy1)
            col=mix(stops[0][1],stops[1][1],k/0.55) if k<0.55 else mix(stops[1][1],stops[2][1],(k-0.55)/0.45)
            c.create_rectangle(hx1,yy,hx2,min(yy+3,hy2), fill=col, outline="", tags=tags)
        # siluet kota & lampu hangat di cakrawala
        for bx,bw,bh in ((hx1+10,46,30),(hx1+70,30,42),(hx2-120,38,36),(hx2-70,56,26)):
            c.create_rectangle(bx,hy2-bh,bx+bw,hy2, fill="#6a4f86", outline="", tags=tags)
        for lx in (hx1+90, hx2-150):
            c.create_line(lx,hy1,lx,hy1+14, fill=INK, width=2, tags=tags)
            c.create_polygon(lx-16,hy1+28,lx-9,hy1+14,lx+9,hy1+14,lx+16,hy1+28, fill=LAMP, outline=INK, width=2, tags=tags)
            c.create_oval(lx-5,hy1+24,lx+5,hy1+32, fill="#fff1c9", outline=INK, width=1, tags=tags)
        c.create_rectangle(hx1,hy1,hx2,hy2, fill="", outline=INK, width=3, tags=tags)
        self.otext(cx, (hy1+hy2)/2+6, self.t('quit_t'), 30, YEL, tags, thick=3)
        # pesan
        c.create_text(cx, y1+148, text=self.t('quit'), font=(FONT,-19,FW), fill="white",
                      justify='center', tags=tags)
        # tombol YES / NO
        for i,(bx,by) in enumerate(self.dlg_buttons()):
            on=(i==self.dlg_sel)
            sc=1.08 if on else 1.0
            w,h=150*sc, 52*sc
            if i==0: fill=YEL if on else "#c9b06a"
            else:    fill=SKY_TOP if on else "#6f6aa8"
            c.create_polygon(rr_pts(bx-w/2+5,by-h/2+6,bx+w/2+5,by+h/2+6,16), smooth=True, fill=INK, outline="", tags=tags)
            c.create_polygon(rr_pts(bx-w/2,by-h/2,bx+w/2,by+h/2,16), smooth=True, fill=fill, outline=INK, width=4, tags=tags)
            c.create_line(bx-w/2+14,by-h/2+9,bx-w/2+44,by-h/2+9, fill="white", width=3, capstyle='round', tags=tags)
            c.create_text(bx, by, text=self.t('yes' if i==0 else 'no'), font=(FONT,-int(22*sc),FW), fill=INK, tags=tags)
        c.tag_raise('dlg')

    def dialog_hit(self, x, y):
        for i,(bx,by) in enumerate(self.dlg_buttons()):
            if abs(x-bx)<=80 and abs(y-by)<=30:
                return i
        return None

    def dialog_motion(self, e):
        i=self.dialog_hit(*self.canvas.to_base(e.x, e.y))
        self.canvas.set_cursor("hand2" if i is not None else "")
        if i is not None and i!=self.dlg_sel:
            self.dlg_sel=i; self.draw_dialog()

    def dialog_click(self, e):
        bx,by=self.canvas.to_base(e.x, e.y)
        i=self.dialog_hit(bx, by)
        if i is not None:
            self.dialog_choose(i==0)
            return
        x1,y1,x2,y2=self.dlg_box()
        if not (x1<=bx<=x2 and y1<=by<=y2):
            self.dialog_choose(False)     # klik di luar kotak = NO

    def dialog_choose(self, yes):
        if not self.dlg_open: return
        self.dlg_open=False
        self.canvas.delete('dlg')
        self.canvas.set_cursor("")
        if yes:
            self.show_menu()

    # ================= UI =================
    def toon_button(self, parent, text, cmd, bg):
        return tk.Button(parent, text=text, command=cmd, bg=bg, fg=INK, activebackground=YEL,
                         activeforeground=INK, font=(FONT,10,FW), relief="raised", bd=3,
                         padx=8, cursor="hand2")

    def build_ui(self):
        self.game_frame=tk.Frame(self.root, bg=BAR)
        top=tk.Frame(self.game_frame, bg=BAR)
        top.pack(fill=tk.X)
        # logo di bar atas (pengganti tulisan SEVEN SCOP)
        self._bar_logo=self.small_logo(BAR_LOGO_H)
        if self._bar_logo is not None:
            tk.Label(top, image=self._bar_logo, bg=BAR, bd=0).pack(side=tk.LEFT, padx=(14,8), pady=4)
        else:
            tk.Label(top, text="♠ SEVEN SCOP ♣", font=(FONT,16,FW), bg=BAR, fg=YEL).pack(side=tk.LEFT, padx=10, pady=5)
        ctrl=tk.Frame(top, bg=BAR)
        ctrl.pack(side=tk.LEFT, padx=10)
        self.btns={}
        for key,cmd,col in (('btn_menu',self.ask_menu,PINK),('btn_restart',lambda: self.show_deal(self.num_players.get()),YEL),
                            ('sort_suit',lambda: self.set_sort("warna"),PLAY_C),('sort_rank',lambda: self.set_sort("angka"),SKY),
                            ('settings',self.open_settings,"#c8b6ff")):
            b=self.toon_button(ctrl, self.t(key), cmd, col)
            b.pack(side=tk.LEFT, padx=3)
            self.btns[key]=b
        self.score_frame=tk.Frame(top, bg=BAR)
        self.score_frame.pack(side=tk.RIGHT, padx=8)

        self.canvas=ScaledCanvas(self.game_frame, CANVAS_W, CANVAS_H, bg=BAR)
        self.canvas.on_rescale=self.on_game_rescale
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=4)
        self.draw_background()

        self.log=tk.Text(self.game_frame, height=2, bg=BAR, fg=LAMP, font=("Consolas",9), bd=0)
        self.log.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0,6), before=self.canvas)
        self.log_insert(self.t('log_ready'))
        self.redraw_last()

    def draw_background(self):
        c=self.canvas
        c.delete('bg')
        # gradasi langit senja: lavender -> ungu -> jingga -> lantai plum
        stops=[(0.0,SKY_TOP),(0.45,SKY_MID),(0.66,SKY_LOW),(0.70,FLOOR),(1.0,"#2a1c3e")]
        vx0,vy0,vx1,vy1=c.visible()
        for y in range(int(vy0)-4, int(vy1)+4, 4):
            k=min(1.0,max(0.0,y/CANVAS_H))
            for (a,ca),(b,cb) in zip(stops,stops[1:]):
                if a<=k<=b:
                    col=mix(ca,cb,(k-a)/(b-a) if b>a else 0); break
            c.create_rectangle(vx0,y,vx1,y+5, fill=col, outline="", tags='bg')
        self.toon_panel(*BOARD_BOX, fill=PANEL, tags=('bg',))
        self.toon_panel(*RIGHT_BOX, fill=PANEL_R, tags=('bg',))
        self.toon_panel(*HAND_BOX, fill=PANEL_H, tags=('bg',))
        for i,(s,_) in enumerate(SUITS):
            self.otext(42, ROW_Y[i], f"{s} {self.t('suits')[i]}", 17, RED if s in '♥♦' else FACE, ('bg',), anchor='w')
        self.otext((RIGHT_BOX[0]+RIGHT_BOX[2])/2, 110, self.t('last_card'), 20, YEL, ('bg',), thick=2)
        self.otext(40, 556, self.t('your_cards'), 18, YEL, ('bg',), anchor='w')
        c.tag_lower('bg')

    def glow(self, cx, cy, rx, ry, base, strength, steps=14):
        # cahaya lampu lembut: oval bertumpuk dari warna panel ke jingga hangat
        c=self.canvas
        for i in range(steps):
            k=1-i/steps
            col=mix(base, LAMP, strength*(1-k)+0.02)
            c.create_oval(cx-rx*k, cy-ry*k, cx+rx*k, cy+ry*k, fill=col, outline="", tags='bg')

    def lamp(self, x, y):
        # lampu gantung kecil ala gambar menu
        c=self.canvas
        c.create_line(x, y-14, x, y+6, fill=INK, width=3, tags='bg')
        c.create_polygon(x-22,y+22, x-12,y+6, x+12,y+6, x+22,y+22, fill=LAMP, outline=INK, width=3, tags='bg')
        c.create_oval(x-6,y+18,x+6,y+28, fill="#fff1c9", outline=INK, width=2, tags='bg')

    def toon_panel(self, x1,y1,x2,y2, fill, tags, c=None):
        c=c or self.canvas
        c.create_polygon(rr_pts(x1+6,y1+7,x2+6,y2+7,22), smooth=True, fill=INK, outline="", tags=tags)
        c.create_polygon(rr_pts(x1,y1,x2,y2,22), smooth=True, fill=fill, outline=INK, width=4, tags=tags)
        c.create_line(x1+22,y1+11,x1+90,y1+11, fill=PANEL_LINE, width=5, capstyle="round", tags=tags)
        c.create_oval(x1+100,y1+8,x1+107,y1+15, fill=PANEL_LINE, outline="", tags=tags)

    def otext(self, x, y, text, size, fill, tags, thick=2, anchor='center', justify='center', c=None):
        c=c or self.canvas
        f=(FONT,-int(max(6,size)),FW)
        for dx,dy in outline_ring(thick):
            c.create_text(x+dx,y+dy,text=text,font=f,fill=INK,tags=tags,anchor=anchor,justify=justify)
        c.create_text(x,y,text=text,font=f,fill=fill,tags=tags,anchor=anchor,justify=justify)

    def draw_card(self, cx, cy, w, h, card, tags, mode='full', face=FACE, dim=False, ace_mark=False, shadow=True, center=None):
        c=self.canvas
        x1,y1,x2,y2=cx-w/2,cy-h/2,cx+w/2,cy+h/2
        r=min(w,h)*0.2
        s,rk=card
        col=RED if s in '♥♦' else INK
        line=INK
        if dim:
            col=DIM_INK; face=DIM_FACE; line="#4a4a55"
        if shadow:
            c.create_polygon(rr_pts(x1+4,y1+5,x2+4,y2+5,r), smooth=True, fill=INK, outline="", tags=tags)
        c.create_polygon(rr_pts(x1,y1,x2,y2,r), smooth=True, fill=face, outline=line, width=3, tags=tags)
        if w < h*0.35 and mode!='chip':
            return
        if mode=='chip':
            if w < 20: return
            txt=f"{rk}{s}"+("×" if ace_mark else "")
            c.create_text(cx,cy,text=txt,font=(FONT,-max(6,int(h*0.55)),FW),fill=col,tags=tags)
        else:
            fs1=max(6,int(h*0.2)); fs2=max(6,int(h*0.42))
            c.create_text(x1+w*0.25,y1+h*0.15,text=rk,font=(FONT,-fs1,FW),fill=col,tags=tags)
            if center:
                c.create_text(cx,cy+h*0.04,text=center,font=(FONT,-max(6,int(h*0.3)),FW),fill=col,tags=tags)
            else:
                c.create_text(cx,cy+h*0.07,text=s,font=(FONT,-fs2,FW),fill=col,tags=tags)
            if mode=='big':
                c.create_text(x2-w*0.25,y2-h*0.15,text=rk,font=(FONT,-fs1,FW),fill=col,tags=tags)

    def draw_back(self, cx, cy, w, h, tags):
        c=self.canvas
        x1,y1,x2,y2=cx-w/2,cy-h/2,cx+w/2,cy+h/2
        r=min(w,h)*0.2
        c.create_polygon(rr_pts(x1+4,y1+5,x2+4,y2+5,r), smooth=True, fill=INK, outline="", tags=tags)
        c.create_polygon(rr_pts(x1,y1,x2,y2,r), smooth=True, fill=PURP, outline=INK, width=3, tags=tags)
        if w>16:
            c.create_polygon(rr_pts(x1+6,y1+6,x2-6,y2-6,r*0.6), smooth=True, fill="", outline=YEL, width=2, dash=(4,3), tags=tags)
            rr=min(w,h)*0.22
            c.create_polygon(star_pts(cx,cy,rr,rr*0.45), fill=YEL, outline=INK, width=2, tags=tags)

    def log_insert(self, m):
        self.log.insert(tk.END, m+"\n")
        self.log.see(tk.END)

    def set_sort(self, mode):
        self.sort_mode.set(mode)
        self.redraw_hand()

    # ================= SETELAN =================
    def open_settings(self):
        if self.set_win is not None and self.set_win.winfo_exists():
            self.set_win.lift(); return
        w=tk.Toplevel(self.root)
        self.set_win=w
        w.title(self.t('set_title'))
        w.configure(bg=BAR, padx=18, pady=14)
        w.resizable(False, False)
        tk.Label(w, text=self.t('set_title'), bg=BAR, fg=YEL, font=(FONT,15,FW)).pack(pady=(0,10))
        opt=dict(bg=BAR, fg="white", selectcolor=PANEL, activebackground=BAR, activeforeground=YEL,
                 font=(FONT,11,FW), anchor="w")
        tk.Checkbutton(w, text=self.t('set_anim'), variable=self.anim_on, **opt).pack(fill=tk.X)
        tk.Checkbutton(w, text=self.t('set_fx'), variable=self.fx_on, **opt).pack(fill=tk.X)
        tk.Checkbutton(w, text=self.t('set_bob'), variable=self.bob_on, **opt).pack(fill=tk.X)
        tk.Checkbutton(w, text=self.t('set_sound'), variable=self.sound_on, **opt).pack(fill=tk.X)
        tk.Label(w, text=self.t('set_speed'), bg=BAR, fg=SKY, font=(FONT,11,FW)).pack(anchor="w", pady=(10,2))
        rf=tk.Frame(w, bg=BAR); rf.pack(fill=tk.X)
        for name in SPEEDS:
            tk.Radiobutton(rf, text=self.t('speed_names')[name], value=name, variable=self.speed, **opt).pack(side=tk.LEFT, padx=(0,8))
        def close():
            self.save_settings(); w.destroy()
        self.toon_button(w, self.t('ok'), close, YEL).pack(pady=(14,0))
        w.protocol("WM_DELETE_WINDOW", close)

    def mult(self):
        return SPEEDS.get(self.speed.get(), 1.0)

    def dur(self, ms):
        return ms/self.mult() if self.anim_on.get() else 0

    # ================= MESIN ANIMASI =================
    def tween(self, ms, frame, done=None):
        d=self.dur(ms)
        if d<=0:
            frame(1.0)
            if done: done()
            return
        t0=time.perf_counter()
        def step():
            t=min(1.0,(time.perf_counter()-t0)*1000/d)
            frame(t)
            if self.dlg_open: self.canvas.tag_raise('dlg')
            if t<1: self.root.after(15, step)
            elif done: done()
        step()

    def _tick(self):
        # kartu yang bisa dimainkan goyang pelan + naik saat di-hover
        self.bob_phase+=0.18
        for i,(tag,cur) in enumerate(list(self.bob_off.items())):
            target=0.0
            if self.bob_on.get() and self.anim_on.get():
                target-=3.5*math.sin(self.bob_phase+i*0.6)
            if tag==self.hover:
                target-=12
            new=cur+(target-cur)*0.45
            self.canvas.move(tag,0,new-cur)
            self.bob_off[tag]=new
        self.root.after(40, self._tick)

    def fly(self, start, end, card, face_down, end_mode, end_face, on_done):
        c=self.canvas
        x0,y0,w0,h0=start
        x1,y1,w1,h1=end
        arc=min(150, math.hypot(x1-x0,y1-y0)*0.35)
        prev=[x0,y0]
        def frame(t):
            c.delete('fly')
            e=ease_in_out(t)
            x=lerp(x0,x1,e); y=lerp(y0,y1,e)-math.sin(math.pi*e)*arc
            grow=1+0.28*math.sin(math.pi*e)
            w=lerp(w0,w1,e)*grow; h=lerp(h0,h1,e)*grow
            back=False
            if face_down:
                w*=max(0.06,abs(math.cos(math.pi*e)))
                back=e<0.5
            # garis kecepatan ala kartun
            vx,vy=x-prev[0],y-prev[1]
            sp=math.hypot(vx,vy)
            if sp>3 and t<0.95:
                ux,uy=-vx/sp,-vy/sp
                px,py=-uy,ux
                for k in (-1,0,1):
                    bx=x+ux*(w*0.5+6)+px*k*h*0.25
                    by=y+uy*(h*0.3+6)+py*k*h*0.25
                    c.create_line(bx,by,bx+ux*min(40,sp*3),by+uy*min(40,sp*3), fill="white", width=3, capstyle="round", tags='fly')
            prev[0],prev[1]=x,y
            if back:
                self.draw_back(x,y,w,h,('fly',))
            else:
                self.draw_card(x,y,w,h,card,('fly',),mode=end_mode if e>0.75 else 'full',face=end_face)
            c.tag_raise('fly')
        def done():
            c.delete('fly')
            on_done()
        self.tween(540, frame, done)

    def pop_chip(self, s_char, v):
        c=self.canvas
        x,y=slot_pos(s_char,v)
        face=ACE_C if v in (1,14) else FACE
        card=(s_char,VAL_LABEL[v])
        self.hidden_slot=(s_char,v)
        self.redraw_board()
        gen=self.gen
        def frame(t):
            c.delete('pop')
            if gen!=self.gen: return
            k=math.sin(t*math.pi*3)*(1-t)
            self.board_card(s_char, v, ('pop',), w=BCARD_W*(1+0.25*k), h=BCARD_H*(1-0.2*k))
            c.tag_raise('pop')
        def done():
            c.delete('pop')
            if gen!=self.gen: return
            if self.hidden_slot==(s_char,v):
                self.hidden_slot=None
            self.redraw_board()
        self.tween(420, frame, done)

    def burst(self, x, y, n=12, kind='star'):
        if not (self.fx_on.get() and self.anim_on.get()): return
        c=self.canvas
        tag=f"fx{self.fx_id}"; self.fx_id+=1
        parts=[]
        for _ in range(n):
            a=random.uniform(0,2*math.pi)
            sp=random.uniform(3,7) if kind=='star' else random.uniform(1,3)
            parts.append([x,y,math.cos(a)*sp,math.sin(a)*sp-(2 if kind=='star' else 1),
                          random.choice(PARTY) if kind=='star' else random.choice(["#eeeeee","#cfcfcf","#b8b8b8"]),
                          random.uniform(5,9) if kind=='star' else random.uniform(8,14),
                          random.uniform(0,6.28)])
        def frame(t):
            c.delete(tag)
            for p in parts:
                p[0]+=p[2]; p[1]+=p[3]
                if kind=='star':
                    p[3]+=0.35; p[6]+=0.3
                    r=p[5]*(1-t)
                    if r<1: continue
                    c.create_polygon(star_pts(p[0],p[1],r,r*0.45,5,p[6]), fill=p[4], outline=INK, width=1.5, tags=(tag,'fx'))
                else:
                    r=p[5]*(0.6+t)*(1-t)*1.6
                    if r<1: continue
                    c.create_oval(p[0]-r,p[1]-r,p[0]+r,p[1]+r, fill=p[4], outline=INK, width=2, tags=(tag,'fx'))
        self.tween(620, frame, lambda: c.delete(tag))

    def comic_text(self, x, y, text, color, size=28):
        if not (self.fx_on.get() and self.anim_on.get()): return
        c=self.canvas
        tag=f"fx{self.fx_id}"; self.fx_id+=1
        def frame(t):
            c.delete(tag)
            sc=ease_out_back(min(1.0,t*2.5))
            if t>0.75: sc*=max(0.0,(1-t)/0.25)
            if sc<0.05: return
            yy=y-26*t
            R=(len(text)*size*0.36+size*0.7)*sc
            c.create_polygon(star_pts(x+4,yy+5,R,R*0.72,14,0.2), fill=INK, outline="", tags=(tag,'fx'))
            c.create_polygon(star_pts(x,yy,R,R*0.72,14,0.2), fill=YEL, outline=INK, width=3, tags=(tag,'fx'))
            self.otext(x,yy,text,size*sc,color,(tag,'fx'),thick=2)
        self.tween(800, frame, lambda: c.delete(tag))

    def wiggle_card(self, card):
        info=self.hand_pos.get(card)
        if not info: return
        x,y,tag=info
        st={'dx':0.0}
        def frame(t):
            dx=math.sin(t*math.pi*6)*7*(1-t)
            self.canvas.move(tag,dx-st['dx'],0)
            st['dx']=dx
        self.tween(360, frame)

    def pop_last(self):
        self.tween(380, lambda t: self.redraw_last(scale=lerp(0.55,1.0,ease_out_back(t))))

    def shake_last(self):
        self.tween(440, lambda t: self.redraw_last(dx=math.sin(t*math.pi*8)*10*(1-t)))

    # ================= GAME =================
    def start_game(self, n=None):
        if n: self.num_players.set(n)
        self.dlg_open=False
        self.canvas.delete('dlg')
        self.gen+=1
        self.busy=False
        self.hidden_slot=None
        for t in ('overlay','fly','pop','fx'):
            self.canvas.delete(t)
        n=self.num_players.get()
        deck=[(s,r) for s,_ in SUITS for r in RANKS]
        random.shuffle(deck)
        self.players=[]
        for i in range(n):
            self.players.append({'name': f"P{i+1}-" + (self.t('you') if i==0 else "PC"), 'hand':[], 'dead':[], 'is_human':i==0})
        for idx,c in enumerate(deck):
            self.players[idx % n]['hand'].append(c)
        self.board={}
        for s,_ in SUITS:
            self.board[s]={'has_7':False,'low':7,'high':7,'low_closed':False,'high_closed':False,'placed':set()}
        self.is_first=True
        self.game_active=True
        self.last_state=None
        starter=0
        for i,p in enumerate(self.players):
            if ('♠','7') in p['hand']:
                starter=i
                break
        self.current_idx=starter
        self.log_insert(self.t('log_start',n=n,name=self.players[starter]['name']))
        self.refresh_all()
        if starter!=0:
            self.schedule_bot()
        else:
            self.comic_text(HAND_CX, 512, self.t('your_turn'), SKY, 24)

    def schedule_bot(self):
        gen=self.gen
        delay=int(650/self.mult()) if self.anim_on.get() else 300
        self.root.after(delay, lambda: gen==self.gen and self.bot_turn())

    def get_playable(self, hand):
        res=[]
        for s_char, rank in hand:
            vals=RANK_VALUES[rank]
            if self.is_first:
                if s_char=='♠' and rank=='7':
                    res.append(((s_char,rank),7))
                continue
            b=self.board[s_char]
            if not b['has_7']:
                if rank=='7':
                    res.append(((s_char,rank),7))
            else:
                if not b['low_closed'] and b['low']-1 in vals:
                    res.append(((s_char,rank), b['low']-1))
                if not b['high_closed'] and b['high']+1 in vals:
                    res.append(((s_char,rank), b['high']+1))
        return res

    def get_discardable(self, hand):
        non68=[c for c in hand if c[1] not in ('6','8')]
        return non68 if non68 else hand[:]

    # ================= GAMBAR ULANG =================
    def refresh_all(self):
        self.redraw_board()
        self.redraw_hand()
        self.refresh_scores()
        self.redraw_last()

    def redraw_board(self):
        c=self.canvas
        c.delete('board')
        for s_char,_ in SUITS:
            b=self.board.get(s_char)
            placed=b['placed'] if b else set()
            for v in range(1,15):
                x,y=slot_pos(s_char,v)
                if v in placed:
                    if self.hidden_slot!=(s_char,v):
                        self.board_card(s_char, v, ('board',))
                else:
                    # slot kosong: garis putus-putus tipis, slot 7 sedikit lebih jelas
                    c.create_polygon(rr_pts(x-BCARD_W/2,y-BCARD_H/2,x+BCARD_W/2,y+BCARD_H/2,11), smooth=True,
                                     fill="", outline=SLOT, width=3 if v==7 else 2,
                                     dash=(5,4) if v==7 else (3,5), tags='board')
                    if v==7:
                        c.create_text(x,y,text="7",font=(FONT,-26,FW),fill=SLOT,tags='board')
        c.tag_raise('pop')
        c.tag_raise('fly')
        c.tag_raise('fx')
        c.tag_raise('overlay')
        c.tag_raise('dlg')

    def board_card(self, s_char, v, tags, w=BCARD_W, h=BCARD_H, shadow=True):
        x,y=slot_pos(s_char,v)
        self.draw_card(x,y,w,h,(s_char,VAL_LABEL[v]),tags,mode='big',shadow=shadow,
                       face=ACE_C if v in (1,14) else FACE)

    def redraw_hand(self):
        c=self.canvas
        c.delete('hand')
        self.hand_pos={}
        self.bob_off={}
        self.hover=None
        if not self.players:
            return
        human=self.players[0]
        mode=self.sort_mode.get()
        if mode=="warna":
            sorted_hand=sorted(human['hand'], key=lambda cd: (SUIT_ORDER[cd[0]], rank_sort(cd[1])))
        else:
            sorted_hand=sorted(human['hand'], key=lambda cd: (rank_sort(cd[1]), SUIT_ORDER[cd[0]]))
        my_turn=self.game_active and self.current_idx==0 and not self.busy
        playable=self.get_playable(human['hand']) if my_turn else []
        playable_set=set(cd for cd,_ in playable)
        disc_set=set(self.get_discardable(human['hand'])) if (my_turn and not playable) else set()

        rows=[sorted_hand[i:i+13] for i in range(0,len(sorted_hand),13)]
        row_y=[650] if len(rows)<=1 else [600,700]
        layout=[]
        for row_cards in rows:
            xs=[]; x=0; prev=None
            for card in row_cards:
                if mode=="warna" and prev and prev!=card[0]:
                    x+=SUIT_GAP
                xs.append(x); x+=HAND_STEP; prev=card[0]
            layout.append((row_cards,xs))
        # kotak info (sisa kartu/dead/poin) di kanan bawah: kalau baris bawah nabrak, geser semua ke kiri
        stats_left=HAND_BOX[2]-18-262-14
        shift=0.0
        for ri,(row_cards,xs) in enumerate(layout):
            if not xs: continue
            y=row_y[min(ri,len(row_y)-1)]
            right=HAND_CX+(xs[-1]+HAND_W)/2
            if y+HAND_H/2 > HAND_BOX[3]-50 and right>stats_left:
                shift=max(shift, right-stats_left)
        cx_hand=HAND_CX
        if shift>0:
            # muatkan di antara tulisan YOUR CARDS (kiri) dan kotak info (kanan); rapatkan kalau perlu
            L=HAND_BOX[0]+165; Rr=stats_left-6
            cx_hand=(L+Rr)/2
            for ri,(row_cards,xs) in enumerate(layout):
                if xs and xs[-1]+HAND_W > Rr-L:
                    f=(Rr-L-HAND_W)/xs[-1]
                    layout[ri]=(row_cards,[x*f for x in xs])
        n=0
        for ri,(row_cards,xs) in enumerate(layout):
            total=xs[-1]+HAND_W if xs else 0
            off=cx_hand-total/2+HAND_W/2
            for card,cx in zip(row_cards,xs):
                tag=f"h{n}"; n+=1
                x=off+cx; y=row_y[min(ri,len(row_y)-1)]
                is_play=card in playable_set
                is_disc=card in disc_set
                face=PLAY_C if is_play else DISC_C if is_disc else FACE
                self.draw_card(x,y,HAND_W,HAND_H,card,('hand',tag),face=face,dim=not my_turn)
                self.hand_pos[card]=(x,y,tag)
                c.tag_bind(tag,"<Button-1>",lambda e,cd=card: self.human_click(cd))
                if is_play or is_disc:
                    self.bob_off[tag]=0.0
                    c.tag_bind(tag,"<Enter>",lambda e,t=tag: self._hover(t))
                    c.tag_bind(tag,"<Leave>",lambda e,t=tag: self._unhover(t))
        c.tag_raise('fly')
        c.tag_raise('fx')
        c.tag_raise('overlay')
        c.tag_raise('dlg')

    def _hover(self, tag):
        self.hover=tag
        self.canvas.tag_raise(tag)
        self.canvas.set_cursor("hand2")

    def _unhover(self, tag):
        if self.hover==tag: self.hover=None
        self.canvas.set_cursor("")

    def redraw_last(self, scale=1.0, dx=0.0):
        c=self.canvas
        c.delete('last')
        x,y=LAST_C
        if not self.last_state:
            c.create_polygon(rr_pts(x-LAST_W/2,y-LAST_H/2,x+LAST_W/2,y+LAST_H/2,20), smooth=True,
                             fill="", outline=SLOT, width=3, dash=(6,5), tags='last')
            self.otext(x,y,"?",54,PANEL_LINE,('last',),thick=2)
            return
        card,kind,name=self.last_state
        face=FACE if kind=='play' else DISC_FACE
        self.draw_card(x+dx,y,LAST_W*scale,LAST_H*scale,card,('last',),mode='big',face=face)
        if kind=='play':
            self.otext(x,y+118,f"{name}\n→ {card[1]}{card[0]}",16,"white",('last',))
        else:
            self.otext(x,y+124,self.t('disc_info',name=name,card=f"{card[1]}{card[0]}"),16,DISC_C,('last',))
        c.tag_raise('fly')
        c.tag_raise('fx')
        c.tag_raise('overlay')
        c.tag_raise('dlg')

    def refresh_scores(self):
        for w in self.score_frame.winfo_children():
            w.destroy()
        for i,p in enumerate(self.players):
            pts=sum(RANK_POINTS[r] for _,r in p['dead']) + sum(RANK_POINTS[r] for _,r in p['hand'])
            is_turn=(i==self.current_idx and self.game_active)
            bg=YEL if is_turn else BAR2
            fg=INK if is_turn else "white"
            box=tk.Frame(self.score_frame, bg=bg, bd=3, relief="raised")
            box.pack(side=tk.LEFT, padx=3, pady=3)
            tk.Label(box, text=("▶ " if is_turn else "")+p['name'], bg=bg, fg=fg, font=(FONT,11,FW)).pack(padx=8, pady=3)
        self.draw_stats()

    def draw_stats(self):
        # info kartu kamu: sisa kartu, kartu mati, poin -> pojok kanan bawah panel Your Cards
        c=self.canvas
        c.delete('stats')
        if not self.players: return
        p=self.players[0]
        pts=sum(RANK_POINTS[r] for _,r in p['dead']) + sum(RANK_POINTS[r] for _,r in p['hand'])
        x2=HAND_BOX[2]-18; x1=x2-262; y1=HAND_BOX[3]-50; y2=HAND_BOX[3]-14
        cy=(y1+y2)/2
        c.create_polygon(rr_pts(x1+4,y1+5,x2+4,y2+5,14), smooth=True, fill=INK, outline="", tags='stats')
        c.create_polygon(rr_pts(x1,y1,x2,y2,14), smooth=True, fill=BAR2, outline=INK, width=3, tags='stats')
        f=(FONT,-17,FW)
        c.create_text(x1+48, cy, text=f"🃏 {len(p['hand'])}", font=f, fill="white", tags='stats')
        c.create_text(x1+122, cy, text=f"💀 {len(p['dead'])}", font=f, fill="white", tags='stats')
        c.create_text(x2-58, cy, text=f"{-pts} pts", font=f, fill=YEL, tags='stats')
    # ================= AKSI =================
    def human_click(self, card):
        if self.dlg_open: return
        if not self.game_active or self.current_idx!=0 or self.busy: return
        if card not in self.players[0]['hand']: return
        playable=self.get_playable(self.players[0]['hand'])
        if playable:
            matches=[(cd,t) for cd,t in playable if cd==card]
            if not matches:
                self.wiggle_card(card)
                x,y,_=self.hand_pos.get(card,(HAND_CX,600,None))
                self.comic_text(x, y-78, self.t('pick_green'), RED, 18)
                if not (self.fx_on.get() and self.anim_on.get()):
                    messagebox.showinfo(self.t('cant_t'), self.t('cant'))
                return
            if len(matches)>1:
                choice=messagebox.askyesno(self.t('ace_t'), self.t('ace'))
                target=14 if choice else 1
                matches=[m for m in matches if m[1]==target]
            self.play_card(0, card, matches[0][1])
        else:
            disc=self.get_discardable(self.players[0]['hand'])
            if card not in disc:
                self.wiggle_card(card)
                x,y,_=self.hand_pos.get(card,(HAND_CX,600,None))
                self.comic_text(x, y-78, self.t('no68'), RED, 18)
                if not (self.fx_on.get() and self.anim_on.get()):
                    messagebox.showinfo(self.t('rule_t'), self.t('rule'))
                return
            self.discard_card(0, card)

    def card_origin(self, p_idx, card):
        if p_idx==0 and card in self.hand_pos:
            x,y,tag=self.hand_pos[card]
            return (x, y+self.bob_off.get(tag,0.0), HAND_W, HAND_H)
        return (180+p_idx*230, -60, HAND_W, HAND_H)

    def play_card(self, p_idx, card, target):
        p=self.players[p_idx]
        s_char,_=card
        gen=self.gen
        self.busy=True
        start=self.card_origin(p_idx, card)
        b=self.board[s_char]
        dest=7 if not b['has_7'] else target
        p['hand'].remove(card)
        self.redraw_hand()
        self.refresh_scores()
        dx,dy=slot_pos(s_char,dest)

        def land():
            if gen!=self.gen: return
            if not b['has_7']:
                b['has_7']=True
                b['low']=7; b['high']=7
                b['placed'].add(7)
            else:
                if target<7:
                    b['low']=target; b['placed'].add(target)
                    if target==1: b['low_closed']=True
                elif target>7:
                    b['high']=target; b['placed'].add(target)
                    if target==14: b['high_closed']=True
            if self.is_first: self.is_first=False
            self.pop_chip(s_char, dest)
            self.burst(dx, dy, 12, 'star')
            if dest in (1,14):
                self.comic_text(dx, dy-52, self.t('closed'), PINK, 22)
            elif p['is_human']:
                i=random.randrange(len(self.t('cheers')))
                self.comic_text(dx, dy-52, self.t('cheers')[i], RED, 22)
                self.play_sound(CHEER_SND[i])      # suara sesuai tulisan yang muncul
            self.last_state=(card,'play',p['name'])
            self.pop_last()
            self.log_insert(self.t('log_play',name=p['name'],card=f"{card[1]}{card[0]}"))
            self.root.after(int(self.dur(240)), lambda: gen==self.gen and self.next_turn())

        self.fly(start, (dx,dy,BCARD_W,BCARD_H), card, not p['is_human'], 'big',
                 ACE_C if dest in (1,14) else FACE, land)

    def discard_card(self, p_idx, card):
        p=self.players[p_idx]
        gen=self.gen
        self.busy=True
        start=self.card_origin(p_idx, card)
        p['hand'].remove(card)
        self.redraw_hand()
        self.refresh_scores()

        def land():
            if gen!=self.gen: return
            p['dead'].append(card)
            self.last_state=(card,'disc',p['name'])
            self.shake_last()
            self.burst(LAST_C[0], LAST_C[1]+40, 9, 'smoke')
            self.comic_text(LAST_C[0], LAST_C[1]-95, self.t('discard'), DISC_C, 22)
            self.log_insert(self.t('log_disc',name=p['name'],card=f"{card[1]}{card[0]}"))
            self.root.after(int(self.dur(260)), lambda: gen==self.gen and self.next_turn())

        self.fly(start, (LAST_C[0],LAST_C[1],LAST_W,LAST_H), card, not p['is_human'], 'big', DISC_FACE, land)

    def next_turn(self):
        self.busy=False
        if all(len(p['hand'])==0 for p in self.players):
            self.refresh_all()
            self.end_game()
            return
        n=len(self.players)
        # lewati pemain yang kartunya sudah habis (penting untuk 3 pemain: 18/17/17)
        for _ in range(n):
            self.current_idx=(self.current_idx+1) % n
            if self.players[self.current_idx]['hand']:
                break
        self.refresh_all()
        if self.current_idx!=0:
            self.schedule_bot()
        else:
            self.comic_text(HAND_CX, 512, self.t('your_turn'), SKY, 24)

    def bot_turn(self):
        if not self.game_active or self.busy: return
        if self.dlg_open:
            gen=self.gen
            self.root.after(200, lambda: gen==self.gen and self.bot_turn())
            return
        p_idx=self.current_idx
        if p_idx==0: return
        p=self.players[p_idx]
        if not p['hand']:
            self.next_turn(); return
        playable=self.get_playable(p['hand'])
        if playable:
            playable_sorted=sorted(playable, key=lambda x: abs(x[1]-7))
            chosen_card, chosen_target = playable_sorted[0]
            same=[t for cd,t in playable if cd==chosen_card]
            if len(same)>1:
                chosen_target=14 if 14 in same else 1
            self.play_card(p_idx, chosen_card, chosen_target)
        else:
            disc=self.get_discardable(p['hand'])
            disc_sorted=sorted(disc, key=lambda cd: RANK_POINTS[cd[1]])
            self.discard_card(p_idx, disc_sorted[0])

    # ================= SELESAI =================
    def end_game(self):
        self.game_active=False
        self.refresh_scores()
        scores=[]
        for p in self.players:
            pts=sum(RANK_POINTS[r] for _,r in p['dead']) + sum(RANK_POINTS[r] for _,r in p['hand'])
            scores.append((p['name'], -pts, pts))
        winner=max(scores, key=lambda x: x[1])
        loser=min(scores, key=lambda x: x[1])
        human_win=winner[0]==self.players[0]['name']
        title=self.t('win') if human_win else self.t('lose')
        detail="\n".join([f"{nm}: {m}pts" for nm,m,_ in scores])
        body=f"{self.t('res_win')}: {winner[0]} {winner[1]}pts\n{self.t('res_lose')}: {loser[0]} {loser[1]}pts\n\n{detail}"
        self.log_insert(self.t('log_end',name=winner[0],pts=winner[1]))
        self.show_overlay(title, body, human_win)

    def char_img(self, kind, h, c):
        # gambar karakter menang/kalah, ikut ukuran layar (disimpan per skala)
        cache=self.__dict__.setdefault('_char_cache',{})
        key=(kind,round(c.s,3),h)
        if key in cache: return cache[key]
        path=WIN_IMG if kind=='win' else LOSE_IMG
        img=None
        try:
            if HAVE_PIL:
                srcs=self.__dict__.setdefault('_char_src',{})
                if kind not in srcs:
                    srcs[kind]=Image.open(path).convert('RGBA')
                    a=srcs[kind].split()[3]; W0,H0=srcs[kind].size
                    br=max((x for x in range(W0) if a.getpixel((x,H0-1))>128), default=W0-1)
                    self.__dict__.setdefault('_char_meta',{})[kind]=(br+1)/W0
                    lf=min((x for y in range(int(H0*0.55),H0,3) for x in range(0,W0,3) if a.getpixel((x,y))>128), default=0)
                    self.__dict__.setdefault('_char_left',{})[kind]=lf/W0
                s=srcs[kind]; ph=max(10,int(round(h*c.s)))
                im=s.resize((max(1,round(s.width*ph/s.height)),ph), Image.LANCZOS)
                trim=int(round(CHAR_TRIM_R.get(kind,0)*c.s))
                if trim>0: im=im.crop((0,0,im.width-trim,im.height))
                # pojok kanan bawah dibulatkan mengikuti sudut kotak -> tetap di dalam bingkai
                r=OV_RADIUS*c.s
                ccx_,ccy_=im.width-r+2*c.s, im.height-r-1*c.s
                a=im.split()[3]; px=a.load()
                for y in range(max(0,int(ccy_)), im.height):
                    for x in range(max(0,int(ccx_)), im.width):
                        if (x-ccx_)**2+(y-ccy_)**2 > r*r: px[x,y]=0
                im.putalpha(a)
                self.__dict__.setdefault('_char_pil',{})[key]=im
                img=ImageTk.PhotoImage(im)
            else:
                raw=tk.PhotoImage(file=path)
                n=max(1,int(round(raw.height()/(h*c.s))))
                img=raw.subsample(n,n)
        except Exception:
            img=None
        cache[key]=img
        return img

    def draw_bubble(self, cx, cy, tip, text, scale, tags, font_px=18, color=INK):
        # balon kata ala komik, ukurannya ikut panjang teks
        c=self.canvas
        lines=text.split("\n")
        w=(max(len(l) for l in lines)*font_px*0.66+56)*scale
        h=(len(lines)*font_px*1.3+34)*scale
        if w<12: return
        x1,y1,x2,y2=cx-w/2,cy-h/2,cx+w/2,cy+h/2
        tx,ty=tip
        bx=x1+w*0.24                                  # pangkal ekor (kiri bawah balon)
        tail=[bx-14*scale, y2-2, bx+18*scale, y2-2, lerp(bx,tx,scale), lerp(y2,ty,scale)]
        r=min(22*scale,h/2)
        c.create_polygon(rr_pts(x1+5,y1+6,x2+5,y2+6,r), smooth=True, fill=INK, outline="", tags=tags)
        c.create_polygon([p+(5 if i%2==0 else 6) for i,p in enumerate(tail)], fill=INK, outline="", tags=tags)
        c.create_polygon(tail, fill="white", outline=INK, width=3, tags=tags)
        c.create_polygon(rr_pts(x1,y1,x2,y2,r), smooth=True, fill="white", outline=INK, width=3, tags=tags)
        c.create_line(bx-12*scale, y2-1, bx+16*scale, y2-1, fill="white", width=5, tags=tags)
        c.create_text(cx, cy, text=text, font=(FONT,-max(6,int(font_px*scale)),FW), fill=color,
                      justify='center', tags=tags)

    def char_fade(self, kind, h, c, steps=10):
        # tahap-tahap transparansi gambar karakter untuk efek fade in
        cache=self.__dict__.setdefault('_fade_cache',{})
        key=(kind,round(c.s,3),h)
        if key in cache: return cache[key]
        frames=[]
        pil=self.__dict__.get('_char_pil',{}).get(key)
        if HAVE_PIL and pil is not None:
            try:
                a=pil.split()[3]
                for i in range(1,steps):
                    k=i/steps
                    im=pil.copy(); im.putalpha(a.point(lambda v,k=k:int(v*k)))
                    frames.append(ImageTk.PhotoImage(im))
            except Exception:
                frames=[]
        cache[key]=frames
        return frames

    def line_h(self, px):
        try:
            import tkinter.font as tkfont
            return tkfont.Font(family=FONT, size=-int(px), weight=FW).metrics('linespace')
        except Exception:
            return px*1.4

    def ribbon_size(self, text, font_px):
        lines=text.split("\n")
        try:
            import tkinter.font as tkfont
            f=tkfont.Font(family=FONT, size=-int(font_px), weight=FW)
            tw=max(f.measure(l) for l in lines)
        except Exception:
            tw=max(len(l) for l in lines)*font_px*0.66
        return (tw+60, len(lines)*font_px*1.3+34)

    def draw_ribbon(self, cx, cy, scale, angle, tags, text, font_px, fill, tail, tcol, stroke, canvas=None, extra_w=0, **_):
        # pita / stiker miring ala toon: badan berujung pita di kiri-kanan, bayangan keras, teks ikut miring
        # extra_w = ruang tambahan di kanan teks (mis. untuk titik-titik)
        c=canvas or self.canvas
        if scale<0.06: return
        w,h=self.ribbon_size(text, font_px)
        w=(w+extra_w)*scale; h*=scale
        th=math.radians(angle); ca,sa=math.cos(th),math.sin(th)
        def rot(pts, ox=0, oy=0):
            out=[]
            for i in range(0,len(pts),2):
                dx,dy=pts[i],pts[i+1]
                out+= [cx+dx*ca+dy*sa+ox, cy-dx*sa+dy*ca+oy]
            return out
        x1,y1,x2,y2=-w/2,-h/2,w/2,h/2
        e=18*scale; m=4*scale
        ends=[x1-e,y1+8*scale, x2+e,y1+8*scale, x2+m,4*scale, x2+e,y2+8*scale, x1-e,y2+8*scale, x1-m,4*scale]
        body=rr_pts(x1,y1,x2,y2,14*scale)
        c.create_polygon(rot(ends,6,7), fill=INK, outline="", tags=tags)
        c.create_polygon(rot(ends), fill=tail, outline=INK, width=3, tags=tags)
        c.create_polygon(rot(body,6,7), smooth=True, fill=INK, outline="", tags=tags)
        c.create_polygon(rot(body), smooth=True, fill=fill, outline=INK, width=4, tags=tags)
        c.create_line(*rot([x1+18*scale,y1+11*scale, x1+60*scale,y1+11*scale]), fill="white", width=4,
                      capstyle="round", tags=tags)
        f=(FONT,-max(6,int(font_px*scale)),FW)
        tcx,tcy=rot([-extra_w*scale/2,0])          # teks bergeser ke kiri sebanyak ruang tambahan
        if stroke:
            for dx,dy in outline_ring(stroke):
                c.create_text(tcx+dx, tcy+dy, text=text, font=f, fill=INK, angle=angle, justify='center', tags=tags)
        c.create_text(tcx, tcy, text=text, font=f, fill=tcol, angle=angle, justify='center', tags=tags)

    def show_overlay(self, title, body, party, animate=True):
        c=self.canvas
        gen=self.gen
        self.ov_args=(title, body, party)
        self.ov_gen=getattr(self,'ov_gen',0)+1
        og=self.ov_gen
        anim=animate and self.anim_on.get()
        if animate:
            self.play_sound(WIN_SND if party else LOSE_SND)   # bunyi menang / kalah
        c.create_rectangle(*c.visible(), fill=INK, stipple='gray50', outline="", tags='overlay')
        # kotak lebar: kiri = hasil & nilai (rata kiri), kanan = karakter
        bx1,bx2=CANVAS_W/2-420, CANVAS_W/2+420
        by1,by2=150,620
        tx=bx1+235
        parts=body.split("\n\n",1)
        summary=parts[0]; detail=parts[1] if len(parts)>1 else ""
        LH=self.line_h(22)
        DATA_Y=by1+124
        LIST_Y=DATA_Y+(summary.count("\n")+1)*LH+10
        data_bottom=LIST_Y+((detail.count("\n")+1)*LH if detail else 0)
        pfill=PURP if party else "#4a4e69"
        kind='win' if party else 'lose'
        img=self.char_img(kind, OV_CHAR_H, c)
        iw=(img.width()/c.s) if img is not None else 0
        # karakter pas di garis: dasar gambar tepat di garis bawah kotak (tertutup garisnya)
        if HAVE_PIL:
            ccx=bx2-2-iw/2                                 # merapat ke garis kanan (pojoknya sudah dibulatkan)
        else:
            frac_br=self.__dict__.get('_char_meta',{}).get(kind,0.97)
            ccx=min(bx2-6-iw/2, bx2-26-(frac_br-0.5)*iw)   # tanpa Pillow: jangan tembus sudut kotak
        cby=by2+1
        alive=lambda: og==self.ov_gen and gen==self.gen and c.find_withtag('ovb')

        def frame(t):
            c.delete('ovb')
            if gen!=self.gen: return
            oy=lerp(-650,0,ease_out_back(t,1.3))
            self.toon_panel(bx1,by1+oy,bx2,by2+oy, fill=pfill, tags=('overlay','ovb'))
            self.otext(tx+(22 if not party else 0), by1+68+oy, title, 44, YEL, ('overlay','ovb'), thick=3)
            self.otext(bx1+48, DATA_Y+oy, summary, 22, "white", ('overlay','ovb'), anchor='nw', justify='left')
            self.otext(bx1+48, LIST_Y+oy, detail, 22, "white", ('overlay','ovb'), anchor='nw', justify='left')
            self.otext((bx1+bx2)/2, by2-16+oy, self.t('click_close'), 13, SKY, ('overlay','ovb','ovclick'), thick=1)
            c.tag_raise('ovchar'); c.tag_raise('ovlip'); c.tag_raise('ovbub'); c.tag_raise('ovclick')

        st={'dx':0,'by':0}
        def place_char(dx, image=None):
            c.delete('ovchar'); c.delete('ovlip')
            if img is None: return
            c.create_image(ccx+dx+st['dx'], cby, image=image or img, anchor='s', tags=('overlay','ovchar'))
            # garis kotak digambar lagi di atas karakter -> potongan bawah gambar tertutup garis
            L=('overlay','ovlip')
            c.create_polygon(rr_pts(bx1,by1,bx2,by2,22), smooth=True, fill="", outline=INK, width=4, tags=L)
            c.tag_raise('ovclick')
            c.create_line(bx1+22,by1+11,bx1+90,by1+11, fill=PANEL_LINE, width=5, capstyle="round", tags=L)
            c.create_oval(bx1+100,by1+8,bx1+107,by1+15, fill=PANEL_LINE, outline="", tags=L)

        # pita miring DI BAWAH NILAI (kolom kiri), rata kiri dengan data
        if party:
            rib=dict(text=self.t('cheer_win'), font_px=34, fill=YEL, tail=RED, tcol=RED, stroke=2, angle=3)
        else:
            rib=dict(text=self.t('cheer_lose'), font_px=18, fill=DISC_C, tail=PURP, tcol=INK, stroke=0, angle=3)
        # ukuran pita tetap seperti sebelumnya; kalau kena gambar karakter, pita ditimpa di atasnya
        left=bx1+48
        rw,rh=self.ribbon_size(rib['text'], rib['font_px'])
        th=math.radians(rib['angle'])
        rcx=left+18+rw/2
        try:
            import tkinter.font as tkfont
            fm=tkfont.Font(family=FONT, size=-22, weight=FW)
            data_w=max(fm.measure(l) for l in (summary+"\n"+detail).split("\n") if l)
        except Exception:
            data_w=max(len(l) for l in (summary+"\n"+detail).split("\n"))*22*0.62
        xr=min(left+data_w, rcx+rw/2)                  # ujung kanan data (di atas pita)
        # pita miring naik ke kanan: titik paling dekat ke data ada di bawah ujung kanan data
        rcy=data_bottom+6+rh/2*math.cos(th)+max(0.0,xr-rcx)*math.sin(th)+3
        bc=(rcx, rcy)
        def bubble(scale, swing=0.0):
            c.delete('ovbub')
            self.draw_ribbon(bc[0], bc[1]+st['by'], scale, rib['angle']+swing, ('overlay','ovbub'),
                             **{k:v for k,v in rib.items() if k!='angle'})

        def idle():
            # gerak terus selama pop up terbuka
            if not alive(): return
            if self.anim_on.get():
                ph=time.perf_counter()
                # karakter diam setelah masuk (gerak cuma saat pop up muncul)
                by=int(round(math.sin(ph*2.4+1.0)*3))      # pita melayang naik-turun pelan
                if by!=st['by']:
                    c.move('ovbub',0,by-st['by']); st['by']=by
            self.root.after(40, idle)

        if anim:
            self.tween(700, frame)
            def char_in():
                if not alive(): return
                def after_char():
                    if not alive(): return
                    # pita muncul memantul sambil berayun ke posisi miringnya
                    self.tween(520, lambda t: alive() and bubble(max(0.05,ease_out_back(t,1.7)),
                                                                 -14*(1-t)*math.cos(t*math.pi*2.5)), idle)
                fades=self.char_fade(kind, OV_CHAR_H, c)
                def fade(t):
                    if not alive(): return
                    if fades and t<1:
                        place_char(0, fades[min(len(fades)-1, int(t*len(fades)))])
                    else:
                        place_char(0)
                self.tween(600, fade, after_char)
            self.root.after(int(self.dur(450)), char_in)
        else:
            frame(1.0); place_char(0); bubble(1.0); idle()
        def close(e=None):
            c.delete('overlay'); self.stop_sound()            # tutup pop up -> suara ikut berhenti
        c.tag_bind('overlay', "<Button-1>", close)
        if anim and party and self.fx_on.get():
            conf=[[random.uniform(0,CANVAS_W), random.uniform(-400,-10), random.uniform(-1.5,1.5),
                   random.uniform(2.5,5.5), random.choice(PARTY), random.uniform(0,6.28)] for _ in range(90)]
            def cf(t):
                c.delete('conf')
                if gen!=self.gen or not c.find_withtag('ovb'): return
                for q in conf:
                    q[0]+=q[2]+math.sin(q[5])*1.2; q[1]+=q[3]; q[5]+=0.15
                    w=6*abs(math.cos(q[5]))+1
                    c.create_rectangle(q[0]-w,q[1]-4,q[0]+w,q[1]+4, fill=q[4], outline=INK, tags=('overlay','conf'))
                c.tag_raise('ovb'); c.tag_raise('ovchar'); c.tag_raise('ovlip'); c.tag_raise('ovbub'); c.tag_raise('ovclick')
            self.tween(3500, cf, lambda: c.delete('conf'))


if __name__=="__main__":
    root=tk.Tk()
    app=ToonSeven(root)
    root.mainloop()
