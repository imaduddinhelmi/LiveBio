# 📹 CARA UPLOAD VIDEO - Panduan Lengkap

## 🚀 Quick Start (3 Langkah)

### Upload Langsung (Immediate):
1. **Select Video** → Isi metadata → **Upload Now** ✅
2. Video langsung diupload ke YouTube
3. Selesai! 🎉

### Upload Terjadwal (Scheduled):
1. **Select Video** → Isi metadata → Pilih waktu → **Schedule Upload** ✅
2. Klik **Start Scheduler** (panel kanan)
3. Aplikasi akan auto-upload sesuai jadwal ⏰

---

## 📖 PANDUAN DETAIL

### STEP 1: LOGIN KE YOUTUBE

**Tab: Auth**

1. Klik tombol **"Select client_secret.json"**
   - Pilih file `client_secret.json` dari Google Cloud Console Anda
   
2. Klik tombol **"Login with Google"**
   - Browser akan terbuka
   - Login dengan akun Google/YouTube Anda
   - Berikan permission yang diminta
   - Tutup browser setelah selesai

3. Pilih Channel YouTube
   - Jika punya banyak channel, pilih yang mau digunakan
   - Channel info akan muncul di bawah

**Status:** ✓ Authenticated (hijau) = Berhasil login

---

### STEP 2: PILIH VIDEO & ISI METADATA

**Tab: Video Upload → Single Upload**

#### A. Pilih File Video

1. Klik tombol **"Select Video"**
2. Browse dan pilih file video Anda
   - Format support: MP4, AVI, MOV, MKV, FLV, WMV
   - Max size: 256 GB (praktis unlimited)
3. File name dan size akan muncul di samping tombol

**✅ Video terpilih:** Akan muncul tanda centang hijau dengan nama file

---

#### B. Isi Metadata Video (WAJIB)

**1. Title (Judul)**
```
Contoh: Tutorial Coding Python untuk Pemula
```
- Max 100 karakter
- Usahakan menarik dan deskriptif

**2. Description (Deskripsi)**
```
Contoh: 
Di video ini kita akan belajar dasar-dasar Python.
Cocok untuk pemula yang baru mulai coding.

Timestamps:
0:00 - Intro
2:15 - Install Python
5:30 - Hello World
...

Follow saya:
Instagram: @username
Twitter: @username
```
- Max 5,000 karakter
- Bisa pakai line break
- Tambahkan timestamps, links, dll

**3. Tags (Pisah dengan koma)**
```
Contoh: python,tutorial,coding,pemula,programming,belajar
```
- Max 500 karakter total
- 5-10 tags optimal
- Gunakan keyword relevan

**4. Category ID**
```
Pilihan populer:
- 22 = People & Blogs (default)
- 28 = Science & Technology
- 20 = Gaming
- 27 = Education
- 10 = Music
- 24 = Entertainment
```

Lihat daftar lengkap di: [VIDEO_UPLOAD_GUIDE.md](VIDEO_UPLOAD_GUIDE.md)

**5. Privacy Status**
```
- public    = Semua orang bisa lihat
- unlisted  = Hanya yang punya link
- private   = Hanya Anda
```

**Rekomendasi:** Upload sebagai `unlisted` dulu, test videonya, baru ubah ke `public` di YouTube Studio

---

#### C. Thumbnail (Opsional tapi Direkomendasikan!)

1. Klik tombol **"Select"** di bagian Thumbnail
2. Pilih gambar thumbnail
   - **Size:** 1280x720 pixels (16:9 ratio)
   - **Format:** JPG, PNG
   - **Max file size:** 2 MB

**Tips Thumbnail:**
- Gunakan teks besar dan jelas
- Warna kontras/cerah
- Tampilkan wajah (jika relevan)
- Konsisten dengan branding

---

#### D. Options (Centang sesuai kebutuhan)

**☑️ Made for Kids**
- Centang HANYA jika video ditujukan untuk anak-anak <13 tahun
- Jika dicentang: Comment dan notifikasi akan disabled
- **Catatan:** Jika salah centang bisa kena penalty dari YouTube!

**☑️ Synthetic Media (AI/Modified)**
- Centang jika video menggunakan AI atau heavy editing
- Contoh: Deepfake, AI voice, AI-generated content

**☑️ Enable Monetization** ⭐
- Centang jika ingin video eligible untuk monetisasi
- **PENTING:** Channel harus sudah join YPP (YouTube Partner Program)
- Jika belum YPP, centang saja untuk persiapan

---

### STEP 3A: UPLOAD NOW (Langsung)

**Untuk upload segera/langsung:**

1. Pastikan semua metadata sudah terisi
2. Klik tombol besar **"⚡ Upload Now (Immediate)"** (warna orange)
3. Upload akan dimulai
4. Progress akan muncul di tab **Logs**:
   ```
   [UPLOAD] Starting upload: Tutorial Coding Python
   [UPLOAD] File: D:\Videos\tutorial.mp4
   [UPLOAD] Size: 125.50 MB
   [UPLOAD] Progress: 15%
   [UPLOAD] Progress: 45%
   [UPLOAD] Progress: 75%
   [UPLOAD] Progress: 100%
   [UPLOAD] ✓ Video uploaded successfully! ID: dQw4w9WgXcQ
   ```

5. Setelah selesai, akan ada popup **"Success"** dengan Video ID
6. Buka YouTube Studio untuk cek video

**⏱️ Waktu upload:** Tergantung size file dan kecepatan internet
- 100 MB = ~2-5 menit
- 1 GB = ~10-30 menit
- 5 GB = ~1-2 jam

**❗ Jangan tutup aplikasi selama upload!**

---

### STEP 3B: SCHEDULE UPLOAD (Terjadwal)

**Untuk upload otomatis di waktu tertentu:**

#### 1. Pilih Waktu Upload

**Cara 1: Quick Preset (Mudah)**

Pilih dari dropdown **"Quick Preset":**
- **Now +5 min** = 5 menit dari sekarang
- **Now +10 min** = 10 menit dari sekarang (default)
- **Now +30 min** = 30 menit dari sekarang
- **Now +1 hour** = 1 jam dari sekarang
- **Now +2 hours** = 2 jam dari sekarang
- **Now +6 hours** = 6 jam dari sekarang
- **Today 20:00** = Hari ini jam 8 malam
- **Tomorrow 08:00** = Besok jam 8 pagi
- **Custom** = Atur manual di bawah

**Cara 2: Manual Entry (Fleksibel)**

Isi field **Date** dan **Time:**
```
Date: 2024-12-25    (format: YYYY-MM-DD)
Time: 14:30         (format: HH:MM, 24-hour)
```

**Contoh use cases:**
- Upload malam ini jam 11: `2024-10-19` + `23:00`
- Upload besok pagi: `2024-10-20` + `08:00`
- Upload minggu depan: `2024-10-26` + `10:00`

#### 2. Lihat Info Waktu Upload

Di bawah field Date/Time akan muncul:
```
📤 Will upload: 2024-10-19 23:00 (in 3h 25m)
```

Warna:
- 🟢 **Hijau** = Waktu valid, siap dijadwalkan
- 🟠 **Orange** = Kurang dari 1 menit (akan segera upload)
- 🔴 **Red** = Waktu di masa lalu (tidak bisa!)

#### 3. Klik Schedule Upload

1. Klik tombol **"📅 Schedule Upload (Automatic)"** (warna hijau)
2. Video akan masuk ke daftar scheduled
3. Popup konfirmasi akan muncul

#### 4. Start Scheduler (PENTING!)

**Di panel kanan "📋 Scheduled Uploads":**

1. Klik tombol **"▶ Start Scheduler"** (hijau)
2. Status berubah jadi: **🟢 Running**
3. Scheduler sekarang aktif dan akan memeriksa setiap 30 detik

**Status video akan berubah:**
- ⏳ **Pending** = Menunggu waktu upload
- 🔄 **Processing** = Sedang diupload
- ✓ **Completed** = Upload berhasil
- ✗ **Failed** = Upload gagal

#### 5. Monitor Status

**Refresh list:**
- Auto-refresh setiap 10 detik
- Atau klik **"🔄 Refresh"** manual

**Lihat detail:**
Daftar akan menampilkan:
```
1. ⏳ Tutorial Coding Python
   Status: PENDING
   Scheduled: 2024-10-19 23:00:00
```

Setelah upload:
```
1. ✓ Tutorial Coding Python
   Status: COMPLETED
   Scheduled: 2024-10-19 23:00:00
   Video ID: dQw4w9WgXcQ
   Completed: 2024-10-19 23:02:35
```

#### 6. Biarkan Aplikasi Berjalan

⚠️ **PENTING:**
- Aplikasi **HARUS TETAP BERJALAN** agar scheduler bekerja
- PC/Laptop tidak boleh sleep/hibernate
- Koneksi internet harus stabil
- Jika aplikasi ditutup, scheduled upload akan pending sampai dibuka lagi

**Tips:**
- Set PC agar tidak sleep (Power Settings)
- Pastikan antivirus tidak block aplikasi
- Jadwalkan upload saat PC pasti menyala

---

## 🔄 UPLOAD BATCH (Banyak Video Sekaligus)

**Tab: Video Upload → Batch Upload**

### STEP 1: Siapkan File Excel

1. Buka file **`sample_videos.xlsx`** sebagai template
2. Edit isi Excel:

| videoPath | title | description | tags | categoryId | privacyStatus | scheduledDate | scheduledTime | thumbnailPath | madeForKids | containsSyntheticMedia | enableMonetization |
|-----------|-------|-------------|------|------------|---------------|---------------|---------------|---------------|-------------|------------------------|-------------------|
| D:\Videos\video1.mp4 | Video Pertama | Deskripsi 1 | tag1,tag2 | 22 | unlisted | 2024-10-20 | 10:00 | D:\Thumbs\1.jpg | FALSE | FALSE | TRUE |
| D:\Videos\video2.mp4 | Video Kedua | Deskripsi 2 | tag3,tag4 | 22 | unlisted | 2024-10-20 | 11:00 | D:\Thumbs\2.jpg | FALSE | FALSE | TRUE |

3. Save file Excel

**Tips:**
- Path video harus LENGKAP dan benar
- Semua column wajib diisi
- Gunakan `FALSE`/`TRUE` untuk boolean
- Date format: `YYYY-MM-DD`
- Time format: `HH:MM`

### STEP 2: Import Excel

1. Klik **"Select Excel File"**
2. Pilih file Excel yang sudah diedit
3. Preview 5 video pertama akan muncul
4. Check apakah data sudah benar

### STEP 3: Set Batch Schedule

**Start Time:** Waktu upload video pertama
```
Date: 2024-10-20
Time: 10:00
```

**Interval:** Jeda antar video
```
Pilihan: 0 min, 5 min, 10 min, 15 min, 30 min, 1 hour
```

**Contoh:**
- Start: 2024-10-20 10:00
- Interval: 15 min
- Video 1: 10:00
- Video 2: 10:15
- Video 3: 10:30
- dst...

### STEP 4: Schedule All

1. Klik **"📅 Schedule All Videos"**
2. Semua video akan masuk scheduled list
3. Kembali ke tab **"Single Upload"**
4. Start scheduler

**✅ Done!** Semua video akan auto-upload sesuai jadwal

---

## 🎯 USE CASES & SCENARIOS

### Scenario 1: Upload 1 Video Sekarang
```
1. Single Upload
2. Select video + isi metadata
3. Upload Now
4. Selesai (2-10 menit tergantung size)
```

### Scenario 2: Upload 1 Video Besok Jam 8 Pagi
```
1. Single Upload
2. Select video + isi metadata
3. Quick Preset: "Tomorrow 08:00"
4. Schedule Upload
5. Start Scheduler
6. Minimize aplikasi dan biarkan berjalan
7. Besok jam 8 pagi video auto-upload
```

### Scenario 3: Upload 10 Video dengan Jeda 30 Menit
```
1. Buat Excel dengan 10 rows
2. Batch Upload → Import Excel
3. Start time: 2024-10-20 14:00
4. Interval: 30 min
5. Schedule All Videos
6. Start Scheduler
7. Video akan upload: 14:00, 14:30, 15:00, ... 18:30
```

### Scenario 4: Upload Otomatis Malam Hari
```
Use case: Anda mau tidur, video upload sendiri jam 2 pagi

1. Single Upload
2. Select video + isi metadata
3. Date: today, Time: 02:00
4. Schedule Upload
5. Start Scheduler
6. Biarkan PC menyala (disable sleep)
7. Tidur
8. Jam 2 pagi video auto-upload
9. Pagi cek hasilnya di YouTube Studio
```

---

## ⚠️ TROUBLESHOOTING

### ❌ "Video file not found"
**Problem:** File video sudah dipindah/dihapus
**Solution:** Pastikan file video masih ada di lokasi yang sama

### ❌ "Authentication error"
**Problem:** Token expired atau invalid
**Solution:** Logout di tab Auth, lalu login lagi

### ❌ "Quota exceeded"
**Problem:** YouTube API quota habis
**Solution:** 
- Tunggu 24 jam (reset setiap hari)
- Atau request quota increase di Google Cloud Console

### ❌ Upload sangat lambat
**Problem:** Internet lambat atau file terlalu besar
**Solution:**
- Check koneksi internet
- Upload saat internet tidak ramai (malam)
- Compress video jika terlalu besar

### ❌ Scheduler tidak jalan
**Problem:** Scheduler belum distart atau aplikasi tertutup
**Solution:**
- Pastikan status 🟢 Running
- Jangan tutup aplikasi
- Check Logs untuk error

### ❌ Video stuck di "Processing"
**Problem:** Upload error atau timeout
**Solution:**
- Check Logs untuk error message
- Coba upload ulang
- Check quota API

---

## 💡 TIPS & BEST PRACTICES

### 📅 Scheduling Tips
- Jadwalkan minimal 5 menit dari sekarang (biar tidak buru-buru)
- Untuk batch upload, gunakan interval minimal 10 menit
- Upload video saat audience online (check YouTube Analytics)
- Prime time: 18:00-22:00 waktu target audience

### 🎬 Video Tips
- Upload sebagai `unlisted` dulu untuk QC
- Set thumbnail custom (CTR naik 30-50%!)
- Tulis description lengkap dengan timestamps
- Gunakan tags yang relevan (5-10 tags)
- Enable monetization sejak awal (jika eligible)

### 📊 Metadata Tips
- Title: 60-70 karakter optimal (tidak terpotong)
- Description: Masukkan keyword di 150 karakter pertama
- Tags: Mix antara broad dan specific keywords
- Category: Pilih yang paling sesuai untuk recommendation

### 🔐 Security Tips
- Jangan share `client_secret.json` ke orang lain
- Gunakan akun Google yang aman
- Backup file Excel schedule Anda
- Check YouTube Studio setelah upload

### ⚡ Performance Tips
- Upload video saat internet tidak ramai
- Compress video jika size > 5GB (maintain quality)
- Batch upload saat Anda tidak pakai PC
- Monitor quota API agar tidak habis

---

## 📞 BANTUAN

**Check Logs:**
- Tab "Logs" menampilkan semua activity
- Error message akan muncul disini
- Copy error message untuk troubleshoot

**Documentation:**
- [VIDEO_UPLOAD_GUIDE.md](VIDEO_UPLOAD_GUIDE.md) - Dokumentasi teknis
- [README_VIDEO_UPLOAD.md](README_VIDEO_UPLOAD.md) - Overview fitur
- [sample_videos.xlsx](sample_videos.xlsx) - Template Excel

**YouTube Resources:**
- YouTube Creator Academy
- YouTube Help Center
- Community Guidelines

---

## ✅ CHECKLIST UPLOAD

Sebelum upload, pastikan:

- [ ] Video sudah final (tidak ada error)
- [ ] Metadata lengkap (title, description, tags)
- [ ] Thumbnail sudah dibuat (1280x720)
- [ ] Category sudah dipilih
- [ ] Privacy status sesuai kebutuhan
- [ ] Monetization dicentang (jika eligible)
- [ ] Synthetic media dicentang (jika pakai AI)
- [ ] Made for Kids TIDAK dicentang (kecuali memang kids content)
- [ ] Scheduled time sudah benar (jika scheduled)
- [ ] Scheduler sudah distart (jika scheduled)
- [ ] PC akan tetap menyala (jika scheduled)
- [ ] Internet stabil

**Setelah upload:**

- [ ] Check YouTube Studio
- [ ] Verify video playback
- [ ] Check description & tags
- [ ] Set end screen & cards
- [ ] Add to playlist
- [ ] Share ke social media

---

## 🎉 SELAMAT!

Anda sekarang sudah tahu cara upload video ke YouTube dengan automation! 

**Happy Creating! 🚀📹**
