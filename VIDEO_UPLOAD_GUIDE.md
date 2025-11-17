# 🎬 Video Upload Guide

## Overview
Fitur Auto Upload Video memungkinkan Anda untuk:
- Upload video ke YouTube dengan metadata lengkap
- Penjadwalan upload otomatis berdasarkan waktu yang ditentukan
- Upload batch video dengan interval waktu
- Monitoring status upload real-time

## Cara Penggunaan

### 1. Authentication
Pastikan Anda sudah login di tab **Auth** terlebih dahulu dengan akun YouTube yang valid.

### 2. Upload Video Segera

#### Langkah-langkah:
1. Buka tab **Video Upload**
2. Klik **"Select Video"** dan pilih file video Anda (format: MP4, AVI, MOV, MKV, FLV, WMV)
3. Isi metadata video:
   - **Title**: Judul video (wajib)
   - **Description**: Deskripsi video
   - **Tags**: Tag video dipisahkan koma (contoh: gaming,tutorial,indonesia)
   - **Category ID**: ID kategori YouTube (default: 22 - People & Blogs)
   - **Privacy**: public/unlisted/private
   - **Thumbnail**: (opsional) Pilih gambar thumbnail
4. Centang opsi yang diperlukan:
   - **Made for Kids**: Centang jika video untuk anak-anak
   - **Synthetic Media**: Centang jika menggunakan AI/modifikasi
   - **Enable Monetization**: Centang untuk mengaktifkan monetisasi
5. Klik **"⚡ Upload Now"** untuk upload langsung

### 3. Penjadwalan Upload

#### Langkah-langkah:
1. Lakukan langkah 1-4 seperti di atas
2. Atur waktu upload:
   - **Date**: Format YYYY-MM-DD (contoh: 2024-12-25)
   - **Time**: Format HH:MM (contoh: 14:30)
   - Atau klik **"🔄 Now"** untuk set 5 menit dari sekarang
3. Klik **"📅 Schedule Upload"**
4. Video akan ditambahkan ke daftar scheduled uploads

### 4. Menjalankan Scheduler

Setelah video dijadwalkan, Anda perlu menjalankan scheduler:

1. Di panel kanan **"📋 Scheduled Uploads"**
2. Klik **"▶ Start Scheduler"**
3. Scheduler akan otomatis memeriksa dan mengupload video sesuai jadwal
4. Status akan berubah:
   - **⏳ Pending**: Menunggu waktu upload
   - **🔄 Processing**: Sedang diupload
   - **✓ Completed**: Upload berhasil
   - **✗ Failed**: Upload gagal

### 5. Monitoring

- **Refresh**: Klik untuk update daftar scheduled uploads
- **Clear Completed**: Hapus video yang sudah selesai/gagal dari daftar
- **Auto-refresh**: Daftar akan refresh otomatis setiap 10 detik
- **Logs**: Check tab **Logs** untuk detail proses upload

## Category ID Reference

| ID  | Category              |
|-----|-----------------------|
| 1   | Film & Animation      |
| 2   | Autos & Vehicles      |
| 10  | Music                 |
| 15  | Pets & Animals        |
| 17  | Sports                |
| 19  | Travel & Events       |
| 20  | Gaming                |
| 22  | People & Blogs        |
| 23  | Comedy                |
| 24  | Entertainment         |
| 25  | News & Politics       |
| 26  | Howto & Style         |
| 27  | Education             |
| 28  | Science & Technology  |
| 29  | Nonprofits & Activism |

## Tips & Best Practices

### 1. Ukuran File
- YouTube mendukung file hingga **256 GB** atau **12 jam durasi**
- Untuk file besar, proses upload akan memakan waktu lama
- Pastikan koneksi internet stabil

### 2. Format Video
- **Recommended**: MP4 dengan codec H.264
- Resolution: 1080p (1920x1080) atau 720p (1280x720)
- Aspect ratio: 16:9

### 3. Thumbnail
- Ukuran: **1280x720 pixels** (16:9 ratio)
- Format: JPG, PNG
- Ukuran file: Maksimal 2MB

### 4. Penjadwalan
- Scheduler memeriksa setiap **30 detik**
- Jangan jadwalkan terlalu banyak video di waktu yang sama
- Aplikasi harus tetap berjalan agar scheduler bekerja

### 5. Monetization
- Centang **"Enable Monetization"** agar video eligible untuk monetisasi
- Monetisasi aktual tergantung pada status YPP (YouTube Partner Program) channel Anda
- Video tidak boleh **"Made for Kids"** untuk bisa dimonetisasi

### 6. Batch Upload
Untuk upload banyak video:
1. Schedule semua video dengan interval waktu (misal: setiap 10 menit)
2. Start scheduler
3. Biarkan aplikasi berjalan
4. Monitor progress di tab Logs

## Troubleshooting

### Upload Gagal
- **"Video file not found"**: Pastikan file video masih ada di lokasi yang sama
- **"Authentication error"**: Login ulang di tab Auth
- **"Quota exceeded"**: YouTube API memiliki quota limit, tunggu 24 jam
- **"Invalid video format"**: Convert video ke format MP4

### Scheduler Tidak Berjalan
- Pastikan sudah klik **"▶ Start Scheduler"**
- Check status scheduler (harus 🟢 Running)
- Aplikasi harus tetap berjalan (jangan ditutup)

### Upload Lambat
- Tergantung ukuran file dan kecepatan internet
- Progress akan muncul di Logs: "Progress: X%"
- Jangan interrupt proses upload

## Advanced: Persistent Scheduling

Scheduled uploads disimpan di:
```
%USERPROFILE%\.ytlive\scheduled_uploads.json
```

File ini menyimpan:
- Daftar video yang dijadwalkan
- Status upload (pending/completed/failed)
- Metadata video

Jika aplikasi ditutup, jadwal akan tetap tersimpan dan bisa dilanjutkan saat aplikasi dibuka lagi.

## Limitations

1. **Quota YouTube API**:
   - Default quota: 10,000 units per day
   - Upload video: ~1,600 units per upload
   - Maksimal ~6 video per hari (tergantung aktivitas API lainnya)

2. **Concurrent Uploads**:
   - Scheduler memproses 1 video dalam 1 waktu
   - Tidak support parallel upload

3. **Privacy & Restrictions**:
   - Video mungkin di-review oleh YouTube
   - Video dengan konten tertentu bisa direstrict/demonetisasi
   - Pastikan comply dengan YouTube Community Guidelines

## Support

Jika mengalami masalah:
1. Check tab **Logs** untuk error message detail
2. Pastikan OAuth credentials (client_secret.json) valid
3. Pastikan channel memiliki permission untuk upload video
4. Check YouTube API quota di Google Cloud Console

---

**Happy Uploading! 🎥✨**
