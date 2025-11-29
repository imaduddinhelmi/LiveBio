# Fitur Pengaturan Jam Spesifik (24 Jam)

## 📋 Ringkasan Fitur

Fitur baru untuk mengatur waktu spesifik (format 24 jam) pada penjadwalan broadcast. Sekarang Anda bisa memilih beberapa hari dan menentukan jam yang sama untuk semua hari tersebut.

## 🎯 Kegunaan

- **Jadwalkan broadcast pada jam yang sama setiap hari**
- **Format 24 jam (HH:MM)** - Contoh: 05:00, 17:30, 23:45
- **Pilih multiple hari** - Misalnya 7 hari berturut-turut pada jam 05:00

## 📍 Lokasi Fitur

### 1. Tab "Import & Run" (Batch Scheduling)

Field baru: **"🕐 Set Broadcast Time (24h format)"**
- **Default:** 05:00
- **Format:** HH:MM (contoh: 05:00 untuk jam 5 pagi, 17:30 untuk jam 5:30 sore)
- **Lokasi:** Di atas checkbox pemilihan hari

### 2. Tab "Quick Create" (Single Broadcast)

Field baru: **"Set Specific Time (24h)"**
- **Format:** HH:MM
- **Lokasi:** Di sebelah kanan dropdown "Time Offset"
- **Kosongkan** untuk menggunakan waktu saat ini + offset

## 🔧 Cara Menggunakan

### Contoh 1: Jadwalkan 30 hari pada jam 05:00 (SHORTCUT BARU!)

1. Buka tab **"Import & Run"**
2. Load file Excel Anda
3. Di field **"Set Broadcast Time (24h format)"**, ketik: `05:00`
4. **Centang checkbox "📅 Schedule 30 Days"** (Satu klik untuk 30 hari!)
5. Pilih **Interval** (misal "0 min (all same)" untuk semua broadcast di jam yang sama)
6. Klik **"Process Batch"**

**Hasil:**
- Semua broadcast dari Excel akan dijadwalkan untuk **30 hari berturut-turut**
- Setiap hari pada jam 05:00
- Jika ada 10 row di Excel dan interval "0 min", maka:
  - Besok jam 05:00 → 10 broadcasts
  - Lusa jam 05:00 → 10 broadcasts
  - ... sampai 30 hari (total 300 broadcasts!)

### Contoh 2: Jadwalkan 7 hari pada jam 05:00

1. Buka tab **"Import & Run"**
2. Load file Excel Anda
3. Di field **"Set Broadcast Time (24h format)"**, ketik: `05:00`
4. **Centang 7 checkbox hari** (+1 day, +2 days, ..., +7 days)
5. Pilih **Interval** (misal "0 min (all same)" untuk semua broadcast di jam yang sama)
6. Klik **"Process Batch"**

**Hasil:**
- Semua broadcast dari Excel akan dijadwalkan untuk 7 hari ke depan
- Setiap hari pada jam 05:00
- Jika ada 10 row di Excel dan interval "0 min", maka:
  - Besok jam 05:00 → 10 broadcasts
  - Lusa jam 05:00 → 10 broadcasts
  - ... (total 70 broadcasts)

### Contoh 2: Jadwalkan besok saja pada jam 17:30 dengan interval 15 menit

1. Buka tab **"Import & Run"**
2. Load file Excel Anda
3. Di field **"Set Broadcast Time (24h format)"**, ketik: `17:30`
4. **Centang hanya checkbox "+1 day"**
5. Pilih **Interval: "+15 min"**
6. Klik **"Process Batch"**

**Hasil:**
- Jika ada 5 row di Excel:
  - Broadcast 1: Besok 17:30
  - Broadcast 2: Besok 17:45
  - Broadcast 3: Besok 18:00
  - Broadcast 4: Besok 18:15
  - Broadcast 5: Besok 18:30

### Contoh 3: Quick Create - Buat 1 broadcast besok jam 10:00

1. Buka tab **"Quick Create"**
2. Isi judul, deskripsi, dll.
3. Di **"Time Offset"**, pilih: `+1 day`
4. Di **"Set Specific Time (24h)"**, ketik: `10:00`
5. Klik tombol **"🔄 Update Time to Now"**
6. Periksa field **"Scheduled Date"** dan **"Scheduled Time"** → akan muncul besok jam 10:00
7. Klik **"✨ Create Broadcast"**

## 📅 Fitur Baru: Schedule 30 Days (SHORTCUT!)

### Apa itu Schedule 30 Days?

Checkbox spesial yang memungkinkan Anda menjadwalkan broadcast untuk **30 hari berturut-turut** hanya dengan **1 klik**, tanpa harus centang checkbox satu per satu!

### Lokasi

Di tab **"Import & Run"**, ada checkbox hijau dengan text:
```
📅 Schedule 30 Days (Overrides individual day selection)
```

### Cara Kerja

1. **Centang checkbox "📅 Schedule 30 Days"**
2. Sistem otomatis membuat jadwal untuk 30 hari ke depan (Day 1 sampai Day 30)
3. Checkbox hari individual (7 hari) akan diabaikan
4. Jam mengikuti setting di field "Set Broadcast Time (24h format)"

### Contoh Penggunaan

**Use Case: Konten Harian Selama Sebulan**
- Excel file: 5 video
- Jam: `06:00`
- Centang: "📅 Schedule 30 Days"
- Interval: `0 min (all same)`

**Hasil:**
- 30 batch akan dibuat (1 batch per hari)
- Setiap batch: 5 video pada jam 06:00
- Total: 150 video terjadwal (5 video × 30 hari)
- Dari besok sampai 30 hari ke depan

### Kapan Menggunakan?

✅ **Gunakan Schedule 30 Days jika:**
- Ingin schedule untuk sebulan penuh
- Konten harian yang konsisten
- Tidak ingin repot centang 30 checkbox

✅ **Gunakan Checkbox Individual (7 hari) jika:**
- Hanya butuh beberapa hari saja (misal 7 hari)
- Ingin kontrol lebih spesifik
- Testing fitur

### Preview

Ketika "Schedule 30 Days" aktif, preview akan menampilkan:
```
📅 30 DAYS MODE: Scheduling from 2025-11-30 to 2025-12-29 at 05:00
    Interval: 0 min (all same) between each broadcast
```

## 📌 Tips & Catatan

### ✅ Format Waktu yang Benar
- `05:00` ✓ (5 pagi)
- `17:30` ✓ (5:30 sore)
- `23:45` ✓ (11:45 malam)
- `00:00` ✓ (tengah malam)

### ❌ Format yang Salah
- `5:00` ❌ (harus 05:00 dengan 2 digit)
- `25:00` ❌ (jam maksimal 23)
- `12:60` ❌ (menit maksimal 59)
- `5pm` ❌ (gunakan format 24 jam: 17:00)

### 🔄 Preview Otomatis
- Setiap kali Anda mengetik di field waktu, preview akan terupdate otomatis
- Cek bagian **"📋 Select Days"** untuk melihat waktu yang akan dijadwalkan
- Contoh preview: `→ 2025-11-30 05:00`

### 📅 Default Setting
- Default jam: **05:00**
- Default hari yang tercentang: **7 hari** (+1 day sampai +7 days)
- Default interval: **0 min (all same)**

Ini artinya begitu Anda load Excel dan klik "Process Batch" tanpa mengubah apapun, sistem akan membuat batch untuk 7 hari ke depan, semuanya pada jam 05:00.

## 🚀 Keunggulan

1. **Fleksibel** - Bisa pilih jam tertentu atau biarkan kosong untuk waktu dinamis
2. **Multi-hari** - Jadwalkan sampai 7 hari sekaligus dengan 1 klik
3. **Preview Jelas** - Lihat persis kapan broadcast akan dijadwalkan sebelum eksekusi
4. **Format 24 Jam** - Tidak ada kebingungan AM/PM

## 🆚 Perbedaan dengan Fitur Lama

| Aspek | Fitur Lama | Fitur Baru |
|-------|-----------|-----------|
| **Jam** | Mengikuti jam saat ini | Bisa set jam spesifik (contoh: 05:00) |
| **Preview** | Hanya menampilkan offset | Menampilkan tanggal & jam lengkap |
| **Use Case** | Jadwal relatif terhadap waktu sekarang | Jadwal absolut pada jam tertentu |
| **Contoh** | "Besok +30 menit dari sekarang" | "Besok jam 05:00" |

## 💡 Use Case Umum

### 1. Konten Harian Pagi
- Set jam: `06:00`
- Pilih: 7 hari
- Interval: 0 min
- **Hasil:** Konten publish setiap pagi jam 6

### 2. Konten Prime Time
- Set jam: `19:00`
- Pilih: 7 hari
- Interval: 0 min
- **Hasil:** Konten publish setiap malam jam 7

### 3. Multiple Broadcasts Per Hari
- Set jam: `08:00`
- Pilih: 1 hari (+1 day)
- Interval: +2 hours
- File Excel: 6 rows
- **Hasil:** Broadcast pada jam 08:00, 10:00, 12:00, 14:00, 16:00, 18:00

## 🐛 Troubleshooting

### Error: "Invalid time format!"
- **Penyebab:** Format waktu salah
- **Solusi:** Gunakan format HH:MM dengan 2 digit untuk jam dan menit (contoh: 05:00, bukan 5:00)

### Error: "Invalid time! Use 00:00 to 23:59 format"
- **Penyebab:** Jam atau menit di luar range
- **Solusi:** Pastikan jam 00-23 dan menit 00-59

### Preview tidak update
- **Solusi:** Klik tombol **"🔄 Refresh Preview"** atau ketik ulang waktu

### Broadcast tidak terjadwal pada jam yang diinginkan
- **Cek:** Pastikan field waktu terisi dengan benar
- **Cek:** Lihat preview sebelum klik "Process Batch"
- **Cek:** Periksa log untuk melihat waktu yang sebenarnya digunakan

## 📝 Changelog

### v1.0 - Fitur Baru Jam Spesifik
- ✨ Tambah field input jam 24 jam (HH:MM) di tab "Import & Run"
- ✨ Tambah field input jam 24 jam di tab "Quick Create"
- 🔧 Update fungsi `update_batch_datetime()` untuk mendukung waktu spesifik
- 🔧 Update fungsi `process_batch()` untuk menggunakan waktu spesifik
- 🔧 Update fungsi `update_quick_datetime()` untuk Quick Create
- 📋 Label "Select Base Time(s)" diganti menjadi "Select Days" untuk lebih jelas
- 🎨 Preview menampilkan "(Custom Time)" ketika menggunakan waktu spesifik
- ✅ Validasi format waktu 24 jam (00:00 - 23:59)
- ✅ Auto-update preview saat user mengetik waktu

## 🔗 File yang Diubah

1. `gui.py` - Main GUI application
   - Tambah field `batch_specific_time` untuk batch scheduling
   - Tambah field `quick_specific_time` untuk quick create
   - Update fungsi scheduling untuk menggunakan waktu spesifik
