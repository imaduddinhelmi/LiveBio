# 📅 Automatic Batch Scheduling Guide

## Overview
Fitur Automatic Batch Scheduling memungkinkan Anda untuk menjadwalkan pemrosesan batch broadcasts secara otomatis setiap hari pada waktu yang ditentukan.

## Fitur Utama
- ✅ Penjadwalan otomatis harian
- ✅ Pengaturan waktu yang fleksibel (format 24-jam)
- ✅ Reload otomatis file Excel sebelum eksekusi
- ✅ Status monitoring real-time
- ✅ Menyimpan konfigurasi untuk sesi berikutnya

## Cara Menggunakan

### 1. Persiapan
Sebelum mengaktifkan scheduler, pastikan:
- ✓ Anda sudah login/authenticate ke akun YouTube
- ✓ File Excel sudah dimuat di tab "Import & Run"
- ✓ Data Excel sudah divalidasi dan sesuai format

### 2. Mengatur Jadwal

#### Di Tab "Import & Run"
1. Scroll ke bagian bawah tab
2. Temukan section **"⏰ Automatic Daily Scheduling"**
3. Atur waktu eksekusi harian:
   - Masukkan waktu dalam format 24-jam (HH:MM)
   - Contoh: `09:00` untuk jam 9 pagi, `21:30` untuk jam 9:30 malam
4. Klik tombol **"▶ Enable Scheduler"**

### 3. Mengaktifkan Scheduler

```
Langkah-langkah:
1. Set "Daily Run Time" → Contoh: 09:00
2. Klik "▶ Enable Scheduler"
3. Konfirmasi pada dialog yang muncul
4. Status akan berubah menjadi "🟢 Scheduler: Active"
5. Lihat waktu eksekusi berikutnya di "Next scheduled run"
```

### 4. Status Scheduler

#### Status yang mungkin muncul:
- **⚪ Scheduler: Disabled** - Scheduler belum dikonfigurasi atau dinonaktifkan
- **🟡 Scheduler: Configured (Not Running)** - Sudah dikonfigurasi tapi belum dijalankan
- **🟢 Scheduler: Active** - Scheduler sedang berjalan dan menunggu waktu eksekusi

### 5. Mengubah Waktu Jadwal
Jika ingin mengubah waktu tanpa mematikan scheduler:
1. Ubah waktu di field "Daily Run Time"
2. Klik **"🔄 Update Time"**
3. Scheduler akan restart dengan waktu baru

### 6. Menonaktifkan Scheduler
- Saat scheduler aktif, tombol berubah menjadi **"⏸ Disable Scheduler"**
- Klik tombol tersebut untuk menonaktifkan penjadwalan otomatis
- Data konfigurasi tetap tersimpan untuk penggunaan berikutnya

## Catatan Penting

### ⚠️ Aplikasi Harus Tetap Berjalan
- Scheduler **HANYA bekerja** saat aplikasi berjalan
- Jika aplikasi ditutup, scheduler akan berhenti
- Pastikan komputer tidak sleep/hibernate saat waktu eksekusi tiba

### 📁 File Excel
- Scheduler akan me-reload file Excel setiap kali eksekusi
- Pastikan file Excel tetap ada di lokasi yang sama
- Anda bisa memperbarui isi file Excel tanpa restart scheduler

### 🕐 Waktu Eksekusi
- Scheduler menggunakan waktu sistem komputer Anda
- Format waktu: 24-jam (00:00 - 23:59)
- Eksekusi akan dilakukan setiap hari pada waktu yang sama

### 🔄 Broadcast Settings
- Setting "Base Time" dan "Interval" di tab Import & Run akan digunakan
- Setting "Global Monetization" juga akan diterapkan
- Pastikan setting sudah dikonfigurasi sebelum mengaktifkan scheduler

## Troubleshooting

### Scheduler tidak berjalan
**Solusi:**
1. Pastikan aplikasi tetap terbuka
2. Check apakah status menunjukkan "🟢 Scheduler: Active"
3. Pastikan file Excel masih ada di lokasi yang sama
4. Check log di tab "Logs" untuk melihat error

### Waktu eksekusi tidak sesuai
**Solusi:**
1. Pastikan waktu sistem komputer sudah benar
2. Check format waktu yang dimasukkan (harus HH:MM)
3. Gunakan format 24-jam (bukan AM/PM)

### Batch processing gagal
**Solusi:**
1. Check koneksi internet
2. Pastikan masih login ke YouTube
3. Check quota API YouTube Anda
4. Lihat detail error di tab "Logs"

### Scheduler berhenti sendiri
**Kemungkinan penyebab:**
1. Aplikasi ditutup atau crash
2. Komputer sleep/hibernate
3. File Excel dipindah/dihapus
4. Session YouTube expired

## Konfigurasi File

Konfigurasi scheduler disimpan di:
```
Windows: C:\Users\[Username]\.ytlive\schedule.json
```

File ini berisi:
- `scheduled_time`: Waktu eksekusi harian
- `excel_file_path`: Path ke file Excel
- `enabled`: Status enabled/disabled
- `last_updated`: Timestamp terakhir update

## Contoh Penggunaan

### Skenario 1: Upload Harian Pagi
```
Use Case: Upload 10 broadcasts setiap pagi jam 7
Settings:
- Daily Run Time: 07:00
- Excel File: broadcasts_daily.xlsx
- Base Time: +30 min (broadcasts mulai 30 menit setelah dibuat)
- Interval: 0 min (all same) - semua broadcasts scheduled bersamaan
```

### Skenario 2: Upload Terjadwal Siang
```
Use Case: Upload 5 broadcasts siang hari dengan interval 2 jam
Settings:
- Daily Run Time: 12:00
- Excel File: afternoon_streams.xlsx
- Base Time: +1 hour
- Interval: +2 hours (broadcast 1: 13:00, broadcast 2: 15:00, dst)
```

### Skenario 3: Upload Malam dengan Monetization
```
Use Case: Upload broadcasts malam hari, semua dengan monetisasi
Settings:
- Daily Run Time: 20:00
- Excel File: night_broadcasts.xlsx
- Base Time: +2 hours
- Interval: +30 min
- ✓ Enable Monetization for ALL broadcasts (checked)
```

## Tips & Best Practices

1. **Testing**: Test manual dulu sebelum enable scheduler
   - Load Excel dan test "Process Batch" manual
   - Pastikan semua broadcasts berhasil dibuat

2. **Monitoring**: Check logs secara berkala
   - Buka tab "Logs" untuk melihat hasil eksekusi
   - Simpan log penting untuk referensi

3. **Backup**: Simpan backup file Excel
   - Buat backup Excel sebelum update
   - Simpan di lokasi yang aman

4. **Quota Management**: Perhatikan quota YouTube API
   - Setiap broadcast creation menggunakan quota
   - Plan jumlah broadcasts sesuai quota harian

5. **Reliability**: Gunakan komputer yang stabil
   - Komputer yang tidak sering dimatikan
   - Setting agar tidak auto-sleep

## FAQ

**Q: Apakah bisa set jadwal berbeda untuk hari tertentu?**
A: Saat ini scheduler hanya support jadwal harian yang sama. Untuk jadwal custom, gunakan manual processing.

**Q: Berapa lama sebelum waktu eksekusi aplikasi harus running?**
A: Aplikasi harus sudah running minimal 1 menit sebelum waktu eksekusi.

**Q: Apakah Excel file akan dimodifikasi oleh scheduler?**
A: Tidak, scheduler hanya membaca Excel file, tidak memodifikasi.

**Q: Bagaimana jika waktu eksekusi terlewat (app tidak running)?**
A: Eksekusi akan skip untuk hari itu dan menunggu hari berikutnya.

**Q: Apakah bisa menjalankan multiple schedule berbeda?**
A: Saat ini hanya support 1 schedule aktif. Untuk multiple schedule, gunakan multiple instance aplikasi (with different accounts).

## Support
Jika mengalami masalah:
1. Check file TROUBLESHOOTING.md
2. Lihat log di tab "Logs"
3. Pastikan semua prerequisites terpenuhi
4. Restart aplikasi jika diperlukan
