# 📅 Panduan Lengkap: Scheduling Massal

## 🎯 Ada 2 Cara Scheduling Massal

### 1. 📊 **Batch Broadcast Scheduling** (Live Streams)
   - Untuk membuat banyak live broadcast sekaligus
   - Menggunakan file Excel
   - Tab: **"Import & Run"**

### 2. 🎬 **Batch Video Upload Scheduling** (Video Files)
   - Untuk upload banyak video sekaligus
   - Menggunakan file Excel
   - Tab: **"Video Upload"** → **"Batch Upload"**

---

## 📊 CARA 1: Batch Broadcast Scheduling (Live Streams)

### Langkah-langkah:

#### Step 1: Siapkan File Excel

Buat file Excel dengan kolom-kolom berikut:

| Kolom | Wajib | Contoh | Keterangan |
|-------|-------|--------|------------|
| title | ✅ Ya | "Live Stream 1" | Judul broadcast |
| description | ❌ Tidak | "Streaming game" | Deskripsi |
| tags | ❌ Tidak | "gaming,live,fun" | Tags (pisah dengan koma) |
| categoryId | ❌ Tidak | 20 | Kategori YouTube (20=Gaming) |
| privacyStatus | ❌ Tidak | public | public/unlisted/private |
| scheduledStartTime | ❌ Tidak | 2025-11-20T20:00:00Z | Waktu mulai (ISO format) |
| madeForKids | ❌ Tidak | FALSE | TRUE/FALSE |
| containsSyntheticMedia | ❌ Tidak | FALSE | TRUE/FALSE |
| enableDvr | ❌ Tidak | TRUE | TRUE/FALSE |
| enableMonetization | ❌ Tidak | TRUE | TRUE/FALSE |

**Contoh Excel:**
```
title                   | description        | tags          | privacyStatus | enableMonetization
Live Gaming Session 1   | Playing games      | gaming,live   | public        | TRUE
Live Gaming Session 2   | Playing games      | gaming,live   | public        | TRUE
Live Gaming Session 3   | Playing games      | gaming,live   | public        | TRUE
```

#### Step 2: Load Excel di Aplikasi

1. Buka tab **"Import & Run"**
2. Klik tombol **"Select Excel File"**
3. Pilih file Excel Anda
4. Preview akan muncul (10 baris pertama)

#### Step 3: Set Waktu Scheduling

Di bagian **"⏰ Schedule Time"**, Anda punya 2 opsi:

**Opsi A: Semua Broadcast di Waktu yang Sama**
```
Base Time: +30 min
Interval: 0 min (all same)
Date: 2025-11-20
Time: 20:00

Hasil: Semua broadcast dijadwalkan jam 20:00
```

**Opsi B: Broadcast Berurutan dengan Interval**
```
Base Time: +30 min
Interval: +1 hour
Date: 2025-11-20
Time: 20:00

Hasil:
- Broadcast 1: 20:00
- Broadcast 2: 21:00
- Broadcast 3: 22:00
- dst...
```

**Interval yang Tersedia:**
- 0 min (all same) - Semua di waktu yang sama
- +5 min - Jeda 5 menit
- +10 min - Jeda 10 menit
- +15 min - Jeda 15 menit
- +30 min - Jeda 30 menit
- +1 hour - Jeda 1 jam
- +2 hours - Jeda 2 jam
- +1 day - Jeda 1 hari

#### Step 4: (Opsional) Enable Global Monetization

Jika ingin SEMUA broadcast punya monetization enabled:
- ✅ Centang: **"Enable Monetization for ALL broadcasts"**
- Ini akan override setting di Excel

#### Step 5: Process Batch

1. Klik tombol **"Process Batch"**
2. Tunggu proses selesai
3. Check di tab **"Logs"** untuk melihat hasil
4. Check di tab **"Upcoming"** untuk verify broadcasts

**Output di Logs:**
```
==========================================
Starting batch process: 10 broadcasts
==========================================
[OK] Success: 10
[X] Errors: 0
==========================================
Batch Complete!
```

---

## 🎬 CARA 2: Batch Video Upload Scheduling

### Langkah-langkah:

#### Step 1: Siapkan File Excel

Buat file Excel dengan kolom-kolom berikut:

| Kolom | Wajib | Contoh | Keterangan |
|-------|-------|--------|------------|
| videoPath | ✅ Ya | "D:\\Videos\\video1.mp4" | Path lengkap ke file video |
| title | ✅ Ya | "Tutorial Gaming Part 1" | Judul video |
| description | ❌ Tidak | "Tutorial lengkap" | Deskripsi video |
| tags | ❌ Tidak | "tutorial,gaming" | Tags (pisah dengan koma) |
| categoryId | ❌ Tidak | 22 | Kategori YouTube (22=People & Blogs) |
| privacyStatus | ❌ Tidak | public | public/unlisted/private |
| thumbnailPath | ❌ Tidak | "D:\\Thumbs\\thumb1.jpg" | Path ke thumbnail |
| madeForKids | ❌ Tidak | FALSE | TRUE/FALSE |
| containsSyntheticMedia | ❌ Tidak | FALSE | TRUE/FALSE |
| enableMonetization | ❌ Tidak | TRUE | TRUE/FALSE |
| scheduledTime | ❌ Tidak | 2025-11-20T20:00:00 | Waktu upload (ISO format) |

**Contoh Excel:**
```
videoPath              | title           | tags            | privacyStatus | enableMonetization
D:\Videos\video1.mp4   | Tutorial Part 1 | tutorial,gaming | public        | TRUE
D:\Videos\video2.mp4   | Tutorial Part 2 | tutorial,gaming | public        | TRUE
D:\Videos\video3.mp4   | Tutorial Part 3 | tutorial,gaming | public        | TRUE
```

**PENTING:** 
- Path harus absolute (lengkap), bukan relative
- Gunakan double backslash `\\` atau forward slash `/`
- File video harus ada di lokasi yang disebutkan

#### Step 2: Load Excel di Aplikasi

1. Buka tab **"Video Upload"**
2. Klik sub-tab **"Batch Upload"**
3. Klik tombol **"Select Excel File"**
4. Pilih file Excel Anda
5. Preview akan muncul (5 video pertama)

#### Step 3: Set Waktu Scheduling

Di bagian **"⏰ Batch Scheduling"**:

**Start Time:**
- Date: 2025-11-20
- Time: 20:00
- Atau klik **"🔄 Now"** untuk set ke waktu sekarang + 5 menit

**Interval:**
- 0 min - Semua upload di waktu yang sama (tidak recommended!)
- 5 min - Jeda 5 menit (recommended untuk video pendek)
- 10 min - Jeda 10 menit (recommended)
- 15 min - Jeda 15 menit
- 30 min - Jeda 30 menit
- 1 hour - Jeda 1 jam (untuk video panjang)

**Contoh:**
```
Start Time: 2025-11-20 20:00
Interval: 10 min

Hasil:
- Video 1: Upload jam 20:00
- Video 2: Upload jam 20:10
- Video 3: Upload jam 20:20
- dst...
```

#### Step 4: Schedule All Videos

1. Klik tombol **"📅 Schedule All Videos"**
2. Semua video akan ditambahkan ke scheduled list
3. Check di tab **"Single Upload"** untuk melihat list

#### Step 5: Start Scheduler

1. Kembali ke sub-tab **"Single Upload"**
2. Di **"Upload Control Panel"**, lihat scheduled list
3. Scheduler akan **auto-start** jika ada scheduled uploads
4. Jika belum start, scroll ke section **"Upload Control Panel"**
5. Status akan menunjukkan **"🟢 Active"** jika scheduler running

**Status Scheduler:**
```
📊 Status: 🟢 Active - 3 video(s) pending

📋 Scheduled List:
1. ⏳ Tutorial Part 1
   Status: PENDING
   Scheduled: 2025-11-20 20:00:00

2. ⏳ Tutorial Part 2
   Status: PENDING
   Scheduled: 2025-11-20 20:10:00

3. ⏳ Tutorial Part 3
   Status: PENDING
   Scheduled: 2025-11-20 20:20:00
```

---

## ⏰ BONUS: Automatic Daily Scheduling

Untuk menjalankan batch **otomatis setiap hari**:

### Setup:

1. Buka tab **"Import & Run"**
2. Load Excel file yang ingin diproses
3. Di panel kanan **"⏰ Automatic Daily Scheduling"**:
   - Set **"Daily Run Time"**: contoh `09:00`
   - Klik **"▶ Enable Scheduler"**

### Hasil:

Setiap hari jam 09:00, aplikasi akan:
1. Load Excel file yang sudah ditentukan
2. Process semua broadcasts di Excel
3. Dijadwalkan sesuai setting waktu & interval

### Catatan:
- ⚠️ Aplikasi harus tetap running (bisa di minimize ke system tray)
- ⚠️ Komputer harus tetap hidup
- ⚠️ Excel file harus tetap ada di lokasi yang sama

---

## 💡 Tips & Best Practices

### 1. Interval Scheduling

**Untuk Live Broadcasts:**
- Jeda minimal: 30 menit (untuk persiapan)
- Recommended: 1-2 jam
- Untuk streaming harian: +1 day

**Untuk Video Uploads:**
- Jeda minimal: 10 menit (untuk processing)
- Recommended: 15-30 menit
- Hindari upload bersamaan (0 min interval)

### 2. Waktu Scheduling

**Hindari waktu:**
- ❌ Di masa lalu (akan error)
- ❌ Terlalu dekat (< 5 menit dari sekarang)

**Recommended:**
- ✅ Minimal 15-30 menit dari sekarang
- ✅ Untuk batch besar, mulai dari besok
- ✅ Pertimbangkan timezone

### 3. Jumlah Batch

**Limit YouTube API:**
- Max 50 broadcasts per hari (safe limit)
- Max 100 video uploads per hari (safe limit)

**Recommended batch size:**
- 10-20 items per batch untuk pemula
- 30-50 items untuk advanced
- Split ke multiple hari jika > 50

### 4. Excel Path Tips

**Video Path:**
```
✅ BENAR:
D:\\Videos\\video1.mp4
D:/Videos/video1.mp4
C:\\Users\\Name\\Videos\\video1.mp4

❌ SALAH:
video1.mp4                    (path tidak lengkap)
.\videos\video1.mp4           (relative path)
Videos\video1.mp4             (relative path)
```

**Thumbnail Path:**
```
✅ BENAR:
D:\\Thumbnails\\thumb1.jpg
D:/Thumbnails/thumb1.jpg

❌ SALAH:
thumb1.jpg
.\thumb1.jpg
```

### 5. Monetization Settings

**Opsi 1: Via Excel**
- Setiap broadcast/video bisa punya setting sendiri
- Kolom `enableMonetization`: TRUE/FALSE

**Opsi 2: Global Override (Broadcast only)**
- Centang: "Enable Monetization for ALL broadcasts"
- Semua broadcasts akan punya monetization enabled
- Mengabaikan setting di Excel

### 6. Preview Sebelum Process

**Selalu check preview:**
- Preview menunjukkan 5-10 baris pertama
- Pastikan format benar
- Pastikan path file valid
- Check untuk typo atau missing data

---

## 🐛 Troubleshooting

### Error: "Video file not found"
**Penyebab:** Path video salah atau file tidak ada

**Solusi:**
1. Check path di Excel (harus absolute path)
2. Pastikan file ada di lokasi tersebut
3. Check typo di path
4. Gunakan double backslash `\\` atau forward slash `/`

### Error: "Invalid date/time format"
**Penyebab:** Format waktu tidak sesuai

**Solusi:**
- Format harus: `YYYY-MM-DDTHH:MM:SS` atau `YYYY-MM-DDTHH:MM:SSZ`
- Contoh: `2025-11-20T20:00:00Z`
- Atau kosongkan dan biarkan aplikasi set otomatis

### Error: "Authentication failed"
**Penyebab:** Belum login atau session expired

**Solusi:**
1. Buka tab "Auth"
2. Check status authentication
3. Login ulang jika perlu

### Scheduler tidak jalan
**Penyebab:** Scheduler belum di-start

**Solusi:**
1. Check status di "Upload Control Panel"
2. Jika "⚫ Idle", scheduler belum start
3. Akan auto-start saat ada scheduled upload
4. Atau restart aplikasi

---

## 📊 Contoh Use Cases

### Use Case 1: Upload 20 Video Tutorial
```
Scenario: Punya 20 video tutorial, ingin upload bertahap

Setup:
- Excel dengan 20 rows (videoPath, title, description, tags)
- Start time: Besok jam 10:00
- Interval: 30 min

Hasil:
- Video 1-20 akan upload dari jam 10:00 - 19:30
- Jeda 30 menit antar upload
- Total durasi: ~10 jam
```

### Use Case 2: Schedule Live Streams Seminggu
```
Scenario: Live stream setiap hari jam 20:00 selama seminggu

Setup:
- Excel dengan 7 rows (satu per hari)
- Start time: Hari ini jam 20:00
- Interval: +1 day

Hasil:
- Day 1: 20:00
- Day 2: 20:00
- Day 3: 20:00
- dst... sampai Day 7
```

### Use Case 3: Batch Broadcasts untuk Event
```
Scenario: Event 3 hari, 5 sessions per hari

Setup:
- Excel dengan 15 rows (3 hari × 5 sessions)
- Gunakan kolom scheduledStartTime di Excel
- Set waktu spesifik untuk setiap session

Hasil:
- Full control atas waktu setiap session
- Bisa set interval tidak rata
- Sesuai jadwal event
```

---

## 🎓 Tutorial Step-by-Step Lengkap

### Tutorial 1: Upload 5 Video Sekaligus

**Step 1: Siapkan Video Files**
```
D:\Videos\
  ├── video1.mp4
  ├── video2.mp4
  ├── video3.mp4
  ├── video4.mp4
  └── video5.mp4
```

**Step 2: Buat Excel (sample_videos.xlsx)**
```
videoPath              | title           | tags     | privacyStatus
D:\Videos\video1.mp4   | Tutorial Part 1 | tutorial | public
D:\Videos\video2.mp4   | Tutorial Part 2 | tutorial | public
D:\Videos\video3.mp4   | Tutorial Part 3 | tutorial | public
D:\Videos\video4.mp4   | Tutorial Part 4 | tutorial | public
D:\Videos\video5.mp4   | Tutorial Part 5 | tutorial | public
```

**Step 3: Scheduling**
1. Buka aplikasi → Tab "Video Upload" → "Batch Upload"
2. Click "Select Excel File" → Pilih sample_videos.xlsx
3. Set Start Time: [Today] [22:00]
4. Set Interval: 15 min
5. Click "Schedule All Videos"

**Step 4: Monitor**
1. Switch ke tab "Single Upload"
2. Check "Scheduled List"
3. Wait untuk upload otomatis

**Hasil:**
- 22:00 - Video 1 upload
- 22:15 - Video 2 upload
- 22:30 - Video 3 upload
- 22:45 - Video 4 upload
- 23:00 - Video 5 upload

---

### Tutorial 2: Schedule 10 Live Streams

**Step 1: Buat Excel (broadcasts.xlsx)**
```
title           | description      | categoryId | privacyStatus | enableMonetization
Live Gaming #1  | Gaming session   | 20         | public        | TRUE
Live Gaming #2  | Gaming session   | 20         | public        | TRUE
... (8 more rows)
```

**Step 2: Load & Schedule**
1. Tab "Import & Run"
2. "Select Excel File" → broadcasts.xlsx
3. Set:
   - Base Time: Tomorrow
   - Date: 2025-11-21
   - Time: 20:00
   - Interval: +2 hours
4. Check preview
5. Click "Process Batch"

**Hasil:**
- Stream #1: Nov 21, 20:00
- Stream #2: Nov 21, 22:00
- Stream #3: Nov 22, 00:00
- ... dst

---

## 📞 Butuh Bantuan?

### Check Logs
- Tab "Logs" akan menunjukkan semua aktivitas
- Error messages akan muncul di logs
- Copy error untuk troubleshooting

### Common Issues
1. **Path tidak valid** → Check absolute path di Excel
2. **Authentication error** → Re-login di tab Auth
3. **Scheduler tidak jalan** → Check status dan restart jika perlu
4. **Upload gagal** → Check file size, format, dan koneksi internet

---

## ✅ Checklist Sebelum Batch Scheduling

Untuk **Batch Broadcast:**
- [ ] File Excel sudah siap dengan format benar
- [ ] Sudah login (tab Auth)
- [ ] Preview OK (10 baris pertama)
- [ ] Waktu scheduling sudah di set
- [ ] Interval sudah dipilih
- [ ] Ready untuk "Process Batch"

Untuk **Batch Video Upload:**
- [ ] File Excel sudah siap
- [ ] Semua video files ada di path yang benar
- [ ] Path di Excel adalah absolute path
- [ ] Sudah login (tab Auth)
- [ ] Preview OK (5 video pertama)
- [ ] Start time & interval sudah di set
- [ ] Ready untuk "Schedule All Videos"

---

## 🎉 Kesimpulan

**Batch Scheduling = Efisiensi Maksimal!**

Dengan fitur batch scheduling, Anda bisa:
- ✅ Schedule puluhan broadcasts/videos sekaligus
- ✅ Set interval otomatis
- ✅ Automatic daily scheduling
- ✅ Hemat waktu dan tenaga

**Selamat scheduling!** 🚀
