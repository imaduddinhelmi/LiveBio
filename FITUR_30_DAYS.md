# Fitur 30 Days Scheduling

## 🎉 Apa itu?

**Schedule 30 Days** adalah fitur shortcut yang memungkinkan Anda menjadwalkan broadcast untuk **30 hari berturut-turut** hanya dengan **1 klik**!

Tidak perlu lagi centang 30 checkbox satu per satu. Cukup centang 1 checkbox, dan sistem otomatis membuat jadwal untuk 30 hari ke depan.

## 📍 Lokasi

Tab **"Import & Run"** → Scroll ke bagian "Schedule Time"

Ada checkbox hijau dengan text:
```
📅 Schedule 30 Days (Overrides individual day selection)
```

## 🚀 Cara Menggunakan

### Langkah-Langkah:

1. Buka tab **"Import & Run"**
2. Load file Excel Anda
3. Set waktu di field **"Set Broadcast Time (24h format)"** (contoh: `05:00`)
4. **Centang checkbox "📅 Schedule 30 Days"**
5. Pilih interval (contoh: `0 min (all same)`)
6. Klik **"Process Batch"**

### Hasil:

- Sistem otomatis membuat 30 batch (1 batch per hari)
- Setiap batch dijadwalkan pada jam yang sama (sesuai setting Anda)
- Dari besok sampai 30 hari ke depan

## 💡 Contoh Use Case

### Use Case 1: Konten Harian Pagi (Sebulan Penuh)

**Skenario:**
- Punya 5 video per hari
- Ingin publish setiap pagi jam 6
- Untuk 1 bulan penuh (30 hari)

**Setting:**
- Excel: 5 rows (5 video)
- Waktu: `06:00`
- Centang: "📅 Schedule 30 Days"
- Interval: `0 min (all same)`

**Hasil:**
- 30 batch dibuat (1 batch per hari)
- Setiap batch: 5 video pada jam 06:00
- **Total: 150 video terjadwal** (5 × 30)

### Use Case 2: Marathon Streaming (30 Hari Non-Stop)

**Skenario:**
- 1 live stream per hari
- Jam 8 malam setiap hari
- 30 hari berturut-turut

**Setting:**
- Excel: 1 row (1 stream config)
- Waktu: `20:00`
- Centang: "📅 Schedule 30 Days"
- Interval: `0 min`

**Hasil:**
- 30 live stream terjadwal
- Setiap malam jam 20:00
- Dari besok sampai 30 hari ke depan

### Use Case 3: Multiple Broadcasts Per Hari (dengan Interval)

**Skenario:**
- 3 broadcasts per hari
- Mulai jam 10 pagi
- Interval 4 jam (jam 10, 14, 18)
- Untuk 30 hari

**Setting:**
- Excel: 3 rows
- Waktu: `10:00`
- Centang: "📅 Schedule 30 Days"
- Interval: `+4 hours`

**Hasil:**
- 30 batch dibuat
- Setiap batch:
  - Broadcast 1: 10:00
  - Broadcast 2: 14:00
  - Broadcast 3: 18:00
- **Total: 90 broadcasts** (3 × 30)

## 📊 Preview

Ketika "📅 Schedule 30 Days" dicentang, preview akan menampilkan info detail:

```
📅 30 DAYS MODE: Scheduling from 2025-11-30 to 2025-12-29 at 05:00
    Interval: 0 min (all same) between each broadcast
```

Info yang ditampilkan:
- **Mode:** 30 DAYS MODE
- **Range tanggal:** Dari tanggal pertama sampai tanggal terakhir
- **Waktu:** Jam yang diset (jika custom)
- **Interval:** Jarak antar broadcast

## ⚙️ Perilaku Sistem

### Ketika Checkbox Dicentang:

1. ✅ Mode 30 hari aktif
2. ✅ Checkbox 7 hari individual otomatis ter-uncheck
3. ✅ Sistem generate 30 tanggal berturut-turut
4. ✅ Log message: "[INFO] 30 Days mode enabled"
5. ✅ Preview berubah menampilkan range 30 hari

### Ketika Checkbox Dilepas:

1. ✅ Kembali ke mode normal (checkbox individual)
2. ✅ User bisa centang 7 hari secara manual
3. ✅ Log message: "[INFO] 30 Days mode disabled"
4. ✅ Preview berubah sesuai pilihan checkbox individual

## 🆚 Perbandingan: 30 Days vs Manual Selection

| Aspek | Manual (7 Checkbox) | 30 Days Shortcut |
|-------|---------------------|------------------|
| **Jumlah Klik** | 7 klik | 1 klik |
| **Maksimal Hari** | 7 hari | 30 hari |
| **Fleksibilitas** | Bisa pilih hari spesifik | Otomatis berturut-turut |
| **Kecepatan** | Lambat (manual) | Cepat (otomatis) |
| **Use Case** | Testing, schedule mingguan | Schedule bulanan, konten harian |

## 📋 Kombinasi dengan Fitur Lain

### 1. Kombinasi dengan Jam Spesifik

✅ **Recommended Combination!**

- Set waktu: `05:00`
- Centang: "📅 Schedule 30 Days"

→ Hasil: 30 hari, semua pada jam 05:00

### 2. Kombinasi dengan Interval

- Set waktu: `08:00`
- Centang: "📅 Schedule 30 Days"
- Interval: `+2 hours`
- Excel: 4 rows

→ Hasil: 30 hari, setiap hari 4 broadcasts (jam 8, 10, 12, 14)

### 3. Kombinasi dengan Monetization Override

- Centang: "📅 Schedule 30 Days"
- Centang: "Enable Monetization for ALL broadcasts"

→ Hasil: 30 hari dengan monetization enabled untuk semua

## 🔧 Troubleshooting

### Preview tidak muncul "30 DAYS MODE"
**Solusi:** Pastikan checkbox "📅 Schedule 30 Days" sudah tercentang (warna hijau).

### Hanya beberapa hari terjadwal (bukan 30)
**Penyebab:** Mungkin checkbox "📅 Schedule 30 Days" tidak tercentang.
**Solusi:** Centang checkbox dan klik "Process Batch" lagi.

### Checkbox 7 hari tidak bisa dicentang
**Penyebab:** Mode 30 hari sedang aktif (override checkbox individual).
**Solusi:** Lepas checkbox "📅 Schedule 30 Days" terlebih dahulu.

### Error: "Please select at least one day or enable 30 Days mode!"
**Penyebab:** Tidak ada hari yang dipilih dan mode 30 hari juga tidak aktif.
**Solusi:** 
- **Opsi 1:** Centang "📅 Schedule 30 Days"
- **Opsi 2:** Centang minimal 1 checkbox hari (misal: +1 day)

## 📝 Tips & Best Practices

### ✅ Do's (Lakukan)

1. **Gunakan untuk konten harian bulanan**
   - Video harian, streaming rutin, dll.

2. **Kombinasikan dengan jam spesifik**
   - Konsistensi waktu = lebih profesional

3. **Test dulu dengan 1-2 hari**
   - Pastikan format Excel dan setting sudah benar
   - Baru scale up ke 30 hari

4. **Gunakan interval untuk multiple broadcasts**
   - Misal: 3 video per hari dengan jarak 4 jam

### ❌ Don'ts (Hindari)

1. **Jangan gunakan untuk testing**
   - 30 hari = banyak broadcasts
   - Testing cukup 1-2 hari saja

2. **Jangan lupa set waktu spesifik**
   - Tanpa jam spesifik → waktu akan dinamis (jam sekarang)
   - Lebih baik set jam tetap (misal: 05:00)

3. **Jangan kombinasikan dengan checkbox 7 hari**
   - Mode 30 hari akan override pilihan individual
   - Pilih salah satu saja

## 🎯 Quick Reference

### Rumus Perhitungan Broadcasts:

```
Total Broadcasts = Rows di Excel × Jumlah Hari
```

**Contoh:**
- Excel: 10 rows
- Mode: 30 days
- Interval: 0 min (all same)

**Total:** `10 × 30 = 300 broadcasts`

### Template Setting Cepat:

#### Setup 1: Harian Pagi (30 Hari)
```
Waktu: 06:00
Schedule 30 Days: ✓
Interval: 0 min (all same)
```

#### Setup 2: Harian Sore (30 Hari)
```
Waktu: 17:00
Schedule 30 Days: ✓
Interval: 0 min (all same)
```

#### Setup 3: Multiple Per Hari (30 Hari)
```
Waktu: 08:00
Schedule 30 Days: ✓
Interval: +3 hours
Excel rows: 4
Hasil: Jam 8, 11, 14, 17
```

## 🎓 FAQ

**Q: Apakah bisa schedule lebih dari 30 hari?**
A: Tidak, maksimal 30 hari. Jika butuh lebih, jalankan batch kedua setelah 30 hari selesai.

**Q: Apakah bisa skip beberapa hari?**
A: Mode 30 hari = consecutive (berturut-turut). Untuk skip hari tertentu, gunakan checkbox individual.

**Q: Apakah hari libur/weekend ikut dijadwalkan?**
A: Ya, sistem menjadwalkan 30 hari kalender berturut-turut (termasuk Sabtu/Minggu).

**Q: Bisa ganti jam untuk hari berbeda?**
A: Mode 30 hari = jam yang sama untuk semua hari. Untuk jam berbeda per hari, gunakan custom scheduling.

**Q: Apakah Excel format berubah?**
A: Tidak, format Excel tetap sama. Fitur ini hanya mengatur jadwal, bukan format file.

**Q: Bagaimana cancel jadwal yang sudah dibuat?**
A: Gunakan YouTube Studio untuk menghapus scheduled broadcasts. Atau gunakan tab "Upcoming" di aplikasi (jika ada).

## 🚀 Summary

**Schedule 30 Days** adalah fitur power user untuk:
- ✅ Content creators dengan konten harian
- ✅ Channel yang konsisten publish setiap hari
- ✅ Automasi scheduling untuk 1 bulan penuh
- ✅ Hemat waktu (1 klik = 30 hari terjadwal!)

**Cara Cepat:**
1. Set waktu (misal: `05:00`)
2. Centang "📅 Schedule 30 Days"
3. Klik "Process Batch"
4. Selesai! 30 hari terjadwal 🎉

---

**Version:** 1.0  
**Release Date:** 2025-11-29  
**Compatibility:** AutoLiveBio v1.x+
