# 🎬 YT Live Auto Studio (Python + CustomTkinter)
Aplikasi desktop Python untuk **membuat dan mengatur siaran langsung otomatis di YouTube Studio**, membaca data dari **file Excel**, dan login menggunakan **file `client_secret.json`** Google OAuth.  
Tanpa FFmpeg — hanya pengaturan dan penjadwalan live event otomatis.

---

## 🚀 Fitur Utama

### 🔐 1. Autentikasi OAuth2
- Pilih file `client_secret.json` (Desktop App dari Google Cloud Console).  
- Jalankan login OAuth2 langsung dari aplikasi.  
- Token disimpan aman di `~/.ytlive/token.json`.  
- Scope: `https://www.googleapis.com/auth/youtube`.

### 📊 2. Import Data dari Excel
Setiap baris di Excel mewakili satu siaran langsung.  
Kolom wajib:
| Kolom | Deskripsi |
|-------|------------|
| `title` | Judul siaran |
| `description` | Deskripsi siaran |
| `tags` | Tag dipisah koma |
| `categoryId` | ID kategori YouTube (mis. 20 = Gaming) |
| `privacyStatus` | public / unlisted / private |
| `scheduledStartDate` | Format YYYY-MM-DD |
| `scheduledStartTime` | Format HH:MM (24 jam lokal) |
| `thumbnailPath` | Path gambar thumbnail (opsional) |

Kolom opsional (jika tidak diisi → nilai default):
| Kolom | Nilai Default | Deskripsi |
|--------|----------------|-----------|
| `thumbnailPath` | - | Path gambar thumbnail |
| `streamId` | - | ID stream existing untuk digunakan ulang |
| `streamKey` | - | Nama custom untuk stream |
| `latency` | `normal` | Latency: normal, low, ultraLow |
| `enableDvr` | `True` | Enable DVR playback |
| `enableEmbed` | `True` | Allow video embedding |
| `recordFromStart` | `True` | Rekam dari awal |
| `madeForKids` | `False` | Konten untuk anak-anak |
| `containsSyntheticMedia` | `False` | Konten dimodifikasi/AI |

Contoh Excel:

| title | description | tags | categoryId | privacyStatus | scheduledStartDate | scheduledStartTime | thumbnailPath | latency | enableDvr | enableEmbed | recordFromStart |
|-------|--------------|------|-------------|----------------|--------------------|--------------------|----------------|----------|------------|--------------|----------------|
| Live Test A | Deskripsi A | test,live,demo | 20 | public | 2025-10-12 | 14:30 | C:\thumb\a.jpg | low | TRUE | TRUE | TRUE |

---

## 🖥️ 3. Antarmuka (CustomTkinter)

### Tab **Auth**
- Pilih file `client_secret.json`.
- Login OAuth.
- Cek akun/channel aktif.

### Tab **Import & Jalankan**
- Pilih dan preview file Excel.
- Tampilkan 10 baris pertama.
- Tombol “Proses Batch” → otomatis:
  1. `create liveBroadcast`
  2. `create liveStream`
  3. `bind broadcast ↔ stream`
  4. `set thumbnail` (jika ada)

### Tab **Upcoming**
- Daftar siaran yang akan datang (upcoming broadcasts).
- Tombol **Refresh**.

### Tab **Logs**
- Tampilkan log proses real-time.

---
