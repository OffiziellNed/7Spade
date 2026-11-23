# ♠ Seven Scop

Game kartu **Seven** (Sevens) bergaya toon: kamu lawan PC, 2 sampai 4 pemain, bisa dimainkan langsung di browser.

## Cara main

- Kartu **♠7** membuka permainan. Setelah itu, tiap jenis kartu (Sekop, Hati, Wajik, Keriting) dimulai dari 7 lalu disambung ke atas (8 → K → As) atau ke bawah (6 → 2 → As).
- Kartu **hijau** di tanganmu bisa dimainkan. Kalau tidak ada yang hijau, kamu wajib **membuang** satu kartu (oranye). Kartu 6 dan 8 tidak boleh dibuang selama masih ada kartu lain.
- Kartu yang dibuang jadi minus: A = 15, K = 13, Q = 12, J = 11, angka sesuai nilainya.
- Setelah semua kartu habis, **minus paling sedikit menang**.

Kontrol: mouse/sentuh, atau keyboard (↑ ↓ Enter Esc di menu; Esc saat main = kembali ke menu).

## Main di HP

- Pegang HP **miring (landscape)**. Kalau dipegang tegak, game minta HP diputar.
- Di HP, tombol pindah ke **sisi kiri** dan jadi ikon: ◄ kembali, ↻ main lagi, ♠♥ urut warna, 1-9 urut angka, ⚙ setelan.
- Di Android, game otomatis **layar penuh** saat pertama disentuh.
- Supaya terasa seperti aplikasi: buka di browser → menu **Tambahkan ke Layar Utama** (Android: ⋮ di Chrome; iPhone: tombol Bagikan di Safari).

## Isi repo

| Folder / file | Isi |
|---|---|
| `index.html`, `style.css`, `game.js` | Versi web (yang dipasang di Vercel) |
| `assets/img`, `assets/snd` | Gambar dan suara versi web |
| `desktop/` | Versi desktop Python/tkinter + gambar & suaranya |
| `vercel.json` | Pengaturan Vercel (situs statis, tanpa build) |

## Pasang di Vercel

1. Buka [vercel.com](https://vercel.com) → **Add New… → Project**.
2. Pilih repo **seven-scop** dari GitHub → **Import**.
3. Framework Preset: **Other**. Build Command dan Output Directory **dikosongkan**.
4. Klik **Deploy**. Setiap kali ada push ke GitHub, Vercel otomatis memperbarui situsnya.

## Jalankan di komputer

- **Versi web:** buka folder ini lewat server lokal, misalnya `python -m http.server`, lalu buka `http://localhost:8000`.
- **Versi desktop:** masuk ke folder `desktop/` lalu jalankan `python seven_scop.py` (disarankan `pip install pillow` supaya gambar tajam saat maximize). Suara berjalan di Windows.

## Kredit

Gambar karakter dan latar: milik Ned.

Font: **Hey Comic** oleh Khurasan — gratis untuk **pemakaian pribadi**; untuk pemakaian komersial, beli lisensinya di [Font Bundles](https://fontbundles.net/khurasan/363482-hey-comic) atau [The Hungry JPEG](https://thehungryjpeg.com/product/3638290-hey-comic). Di file font repo ini ditambahkan angka 0 dan tanda : ; (diambil dari bentuk huruf O, titik, dan koma) karena versi gratisnya tidak menyediakan karakter itu.
