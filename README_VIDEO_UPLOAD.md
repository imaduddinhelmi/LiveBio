# 📹 Auto Video Upload Feature

## Overview

Fitur baru **Auto Video Upload** telah ditambahkan ke aplikasi AutoLiveBio! Sekarang Anda dapat:

✅ Upload video ke YouTube dengan metadata lengkap  
✅ Penjadwalan upload otomatis berdasarkan waktu  
✅ Batch upload multiple videos dari Excel  
✅ Monitoring upload status real-time  
✅ Persistent scheduling (jadwal tetap tersimpan)  

---

## 🚀 Quick Start

### 1. Jalankan Aplikasi
```batch
run.bat
```
atau
```cmd
python main.py
```

### 2. Login di Tab "Auth"
- Pilih file `client_secret.json`
- Klik "Login with Google"
- Pilih channel YouTube Anda

### 3. Buka Tab "Video Upload"
Anda akan melihat 2 sub-tab:
- **Single Upload**: Upload 1 video dengan GUI
- **Batch Upload**: Upload banyak video dari Excel

---

## 📝 Single Upload

### Cara Upload Langsung:
1. Klik **"Select Video"** → Pilih file video Anda
2. Isi metadata:
   - Title (wajib)
   - Description
   - Tags (pisah dengan koma)
   - Category ID (default: 22)
   - Privacy: public/unlisted/private
   - Thumbnail (opsional)
3. Centang opsi:
   - Made for Kids
   - Synthetic Media (AI/modifikasi)
   - Enable Monetization
4. Klik **"⚡ Upload Now"**

### Cara Penjadwalan:
1. Ikuti langkah 1-3 di atas
2. Atur **Date** dan **Time** upload
3. Klik **"📅 Schedule Upload"**
4. Klik **"▶ Start Scheduler"** di panel kanan
5. Video akan otomatis diupload sesuai jadwal

---

## 📊 Batch Upload dari Excel

### 1. Siapkan File Excel

Buat file Excel dengan kolom berikut:

| Column Name | Required | Description | Example |
|------------|----------|-------------|---------|
| videoPath | ✅ Yes | Path lengkap ke file video | `D:\Videos\myvideo.mp4` |
| title | ✅ Yes | Judul video | `Tutorial Coding` |
| description | ✅ Yes | Deskripsi video | `Belajar coding untuk pemula` |
| tags | ✅ Yes | Tags dipisah koma | `coding,tutorial,pemula` |
| categoryId | ✅ Yes | ID kategori YouTube | `28` (Science & Tech) |
| privacyStatus | ✅ Yes | Status privacy | `public` / `unlisted` / `private` |
| scheduledDate | ⚪ Optional | Tanggal upload | `2024-12-25` |
| scheduledTime | ⚪ Optional | Jam upload | `14:00` |
| thumbnailPath | ⚪ Optional | Path thumbnail | `D:\Thumbs\thumb.jpg` |
| madeForKids | ⚪ Optional | Video untuk anak | `FALSE` |
| containsSyntheticMedia | ⚪ Optional | Pakai AI/modif | `FALSE` |
| enableMonetization | ⚪ Optional | Aktifkan monetisasi | `TRUE` |

**Contoh file**: `sample_videos.xlsx`

### 2. Import dan Schedule

1. Buka sub-tab **"Batch Upload"**
2. Klik **"Select Excel File"** → Pilih file Excel Anda
3. Lihat preview 5 video pertama
4. Atur scheduling:
   - **Start Time**: Waktu mulai upload pertama
   - **Interval**: Jeda antar video (5 min, 10 min, dll)
5. Klik **"📅 Schedule All Videos"**
6. Start scheduler di tab **"Single Upload"**

---

## ⚙️ Scheduler

### Cara Kerja:
- Scheduler berjalan di background
- Memeriksa jadwal setiap **30 detik**
- Otomatis upload video yang sudah waktunya
- Status update real-time

### Menggunakan Scheduler:
1. Jadwalkan video (single atau batch)
2. Klik **"▶ Start Scheduler"** (panel kanan)
3. Status akan berubah: 🟢 **Running**
4. Biarkan aplikasi tetap berjalan
5. Monitor progress di tab **Logs**

### Status Upload:
- ⏳ **Pending**: Menunggu waktu upload
- 🔄 **Processing**: Sedang diupload
- ✓ **Completed**: Upload berhasil (Video ID tercantum)
- ✗ **Failed**: Upload gagal (Error message tercantum)

### Tips:
- Aplikasi **harus tetap berjalan** agar scheduler bekerja
- Jadwal tersimpan di `%USERPROFILE%\.ytlive\scheduled_uploads.json`
- Jika aplikasi ditutup, jadwal tidak hilang dan bisa dilanjutkan
- Klik **"Clear Completed"** untuk bersihkan daftar

---

## 📂 File Struktur Baru

```
AutoLiveBio/
├── video_uploader.py          # Core uploader dengan scheduler
├── video_excel_parser.py      # Parser Excel untuk batch upload
├── gui_video_upload.py        # GUI untuk video upload
├── VIDEO_UPLOAD_GUIDE.md      # Dokumentasi lengkap
├── sample_videos.xlsx         # Contoh file Excel
└── create_sample_videos_excel.py  # Script generate sample Excel
```

---

## 🎯 Use Cases

### Use Case 1: Upload Video Langsung
> Anda punya 1 video yang ingin langsung diupload

**Solusi**: Gunakan **Single Upload** → **Upload Now**

### Use Case 2: Upload Video Terjadwal
> Anda ingin upload video besok jam 10 pagi

**Solusi**: 
1. **Single Upload** → Set tanggal & waktu
2. **Schedule Upload** → **Start Scheduler**

### Use Case 3: Batch Upload 10 Video
> Anda punya 10 video yang ingin diupload dengan jeda 15 menit

**Solusi**:
1. Buat Excel dengan 10 baris data video
2. **Batch Upload** → Import Excel
3. Set interval **15 min** → **Schedule All**
4. **Start Scheduler**

### Use Case 4: Upload Malam Hari Otomatis
> Anda ingin video terupload otomatis jam 2 pagi saat tidur

**Solusi**:
1. Schedule video untuk jam 02:00
2. **Start Scheduler**
3. Biarkan PC tetap menyala
4. Video akan otomatis terupload

---

## ⚠️ Limitations & Notes

### YouTube API Quota
- **Default quota**: 10,000 units/hari
- **Upload video**: ~1,600 units/upload
- **Maksimal**: ~6 video/hari (tergantung aktivitas API lain)
- **Reset**: Setiap hari jam 00:00 PST (Pacific Time)

### File Size & Duration
- **Maksimal**: 256 GB atau 12 jam durasi
- **Recommended format**: MP4 (H.264 codec)
- **Resolution**: 1080p atau 720p

### Thumbnail
- **Size**: 1280x720 pixels (16:9 ratio)
- **Format**: JPG, PNG
- **Max file size**: 2 MB

### Privacy & Restrictions
- Video bisa di-review oleh YouTube
- Konten tertentu bisa direstrict/demonetisasi
- Pastikan comply dengan YouTube Community Guidelines

### Technical
- Tidak support **parallel upload** (1 video dalam 1 waktu)
- Scheduler memproses sequential
- Upload progress ditampilkan di Logs

---

## 🐛 Troubleshooting

### "Video file not found"
**Solusi**: Pastikan path video benar dan file masih ada

### "Authentication error"
**Solusi**: Login ulang di tab Auth

### "Quota exceeded"
**Solusi**: Tunggu 24 jam untuk reset quota

### "Invalid video format"
**Solusi**: Convert video ke format MP4

### Scheduler tidak berjalan
**Solusi**: 
1. Pastikan sudah klik **"▶ Start Scheduler"**
2. Check status (harus 🟢 Running)
3. Aplikasi harus tetap berjalan

### Upload lambat
**Solusi**: Tergantung ukuran file dan internet. Monitor di Logs untuk progress.

---

## 📞 Support

- **Documentation**: `VIDEO_UPLOAD_GUIDE.md`
- **Sample Excel**: `sample_videos.xlsx`
- **Logs**: Tab "Logs" di aplikasi

---

## 🎉 Happy Uploading!

Fitur Auto Video Upload memudahkan Anda untuk:
- Manage banyak video sekaligus
- Upload otomatis di waktu optimal
- Batch process video collection
- Set metadata konsisten untuk semua video

**Enjoy the automation! 🚀🎬**
