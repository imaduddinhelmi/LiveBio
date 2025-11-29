# Changelog - Fitur Pengaturan Jam Spesifik

## 🎉 Fitur Baru: Set Broadcast Time (24h Format)

**Tanggal:** 2025-11-29

### ✨ Apa yang Baru?

#### 1. Set Broadcast Time - Pengaturan Jam Spesifik (24h)

Sekarang Anda bisa mengatur jam spesifik untuk penjadwalan broadcast dengan format 24 jam (HH:MM).

**Contoh:** 
- Jadwalkan 7 hari berturut-turut pada jam **05:00** (5 pagi)
- Jadwalkan besok pada jam **17:30** (5:30 sore)
- Jadwalkan lusa pada jam **23:45** (11:45 malam)

#### 2. Schedule 30 Days - Shortcut untuk 30 Hari! 🎉

**FITUR BARU:** Checkbox "📅 Schedule 30 Days" untuk menjadwalkan **30 hari berturut-turut** dengan **1 klik**!

**Keunggulan:**
- ✅ Tidak perlu centang 30 checkbox satu per satu
- ✅ Otomatis generate jadwal untuk 30 hari ke depan
- ✅ Cocok untuk konten harian bulanan
- ✅ Kombinasi sempurna dengan jam spesifik (misal: 30 hari @ 05:00)

### 📍 Lokasi Fitur

1. **Tab "Import & Run"** (Batch Scheduling)
   - Field baru: **"🕐 Set Broadcast Time (24h format)"**
   - Default: `05:00`
   - Letaknya di atas checkbox pemilihan hari
   - **Checkbox baru: "📅 Schedule 30 Days"** (hijau, prominent)
   - Letaknya di bawah quick selection buttons

2. **Tab "Quick Create"** (Single Broadcast)
   - Field baru: **"Set Specific Time (24h)"**
   - Letaknya di sebelah kanan dropdown "Time Offset"

### 🔧 Perubahan Detail

#### 1. Field Input Baru
```
🕐 Set Broadcast Time (24h format): [05:00]
(e.g., 05:00 for 5 AM, 17:30 for 5:30 PM)
```

#### 2. Checkbox 30 Days (FITUR BARU!)
```
┌──────────────────────────────────────────────────────┐
│ 📅 Schedule 30 Days (Overrides individual day selection) │
└──────────────────────────────────────────────────────┘
```

- **Warna:** Hijau (prominent, mudah terlihat)
- **Fungsi:** Generate otomatis 30 hari berturut-turut
- **Override:** Ketika dicentang, checkbox 7 hari diabaikan
- **Log:** Otomatis log "30 Days mode enabled" ke console

#### 3. Label Lebih Jelas
- **Sebelum:** "📋 Select Base Time(s):" (Select multiple to schedule at different times)
- **Sekarang:** "📋 Select Days:" (Select multiple days to schedule broadcasts)

Perubahan ini membuat lebih jelas bahwa Anda memilih **hari**, bukan waktu. Waktu diatur terpisah di field jam.

#### 4. Preview Lebih Informatif

**Contoh preview (Mode Normal - 7 hari):**
```
📋 7 days selected at 05:00 (Custom Time), each with 0 min (all same) interval
    Times: 2025-11-30 05:00, 2025-12-01 05:00, 2025-12-02 05:00 ... (+4 more)
```

**Contoh preview (Mode 30 Days):**
```
📅 30 DAYS MODE: Scheduling from 2025-11-30 to 2025-12-29 at 05:00
    Interval: 0 min (all same) between each broadcast
```

Preview sekarang menampilkan:
- Berapa hari dipilih (7 hari atau 30 hari)
- Jam yang diset (jika custom)
- Interval yang digunakan
- Contoh 3 waktu pertama dengan tanggal lengkap (mode normal)
- Range tanggal (dari-sampai) untuk mode 30 hari

#### 4. Auto-Update Preview
- Ketik di field waktu → preview langsung terupdate
- Tidak perlu klik tombol "Refresh Preview" lagi

#### 5. Validasi Waktu
- ✅ Format benar: `05:00`, `17:30`, `23:59`
- ❌ Format salah: `5:00`, `25:00`, `12:60`
- Error message yang jelas jika format salah

### 🚀 Cara Menggunakan

#### Quick Start 1: Jadwalkan 30 Hari pada Jam 05:00 (REKOMENDASI!)

1. Buka tab **"Import & Run"**
2. Load Excel file Anda
3. Field **"Set Broadcast Time (24h format)"** sudah terisi `05:00` (default)
4. **Centang checkbox "📅 Schedule 30 Days"**
5. Interval: `0 min (all same)` (default)
6. Klik **"Process Batch"** → Selesai!

**Hasil:** Semua broadcast dari Excel dijadwalkan untuk **30 hari berturut-turut**, masing-masing pada jam 05:00.
- Jika Excel punya 10 rows → Total 300 broadcasts (10 × 30 hari)
- Otomatis dari besok sampai 30 hari ke depan

#### Quick Start 2: Jadwalkan 7 Hari pada Jam 05:00

1. Buka tab **"Import & Run"**
2. Load Excel file Anda
3. Field **"Set Broadcast Time (24h format)"** sudah terisi `05:00` (default)
4. **7 hari sudah tercentang** secara default (+1 day sampai +7 days)
5. Interval: `0 min (all same)` (default)
6. Klik **"Process Batch"** → Selesai!

**Hasil:** Semua broadcast dari Excel dijadwalkan untuk 7 hari ke depan, masing-masing pada jam 05:00.

#### Contoh Lain: Jam Malam (20:00)

1. Di field **"Set Broadcast Time (24h format)"**, ganti menjadi: `20:00`
2. Pilih hari yang diinginkan (misal centang hanya +1 day dan +2 days)
3. Klik **"Process Batch"**

**Hasil:** Broadcast dijadwalkan untuk besok dan lusa, masing-masing pada jam 20:00.

### 💡 Tips Penggunaan

#### 1. Format Waktu 24 Jam
- **00:00** = Tengah malam
- **05:00** = 5 pagi
- **12:00** = Siang
- **17:00** = 5 sore
- **23:59** = 1 menit sebelum tengah malam

#### 2. Kombinasi dengan Interval

**Skenario:** Multiple broadcasts per hari

- Set jam: `08:00`
- Pilih: +1 day (besok saja)
- Interval: `+2 hours`
- Excel: 6 rows

**Hasil:**
- Broadcast 1: Besok 08:00
- Broadcast 2: Besok 10:00
- Broadcast 3: Besok 12:00
- Broadcast 4: Besok 14:00
- Broadcast 5: Besok 16:00
- Broadcast 6: Besok 18:00

#### 3. Kosongkan untuk Waktu Dinamis

Jika Anda **kosongkan field jam**, sistem akan menggunakan perilaku lama (waktu saat ini + offset).

### 🔄 Backward Compatibility

Fitur lama **tetap berfungsi**:
- Jika field jam dikosongkan, sistem menggunakan waktu saat ini + offset (perilaku original)
- Semua file Excel lama tetap kompatibel
- Tidak ada breaking changes

### 🐛 Bug Fixes & Improvements

1. ✅ Validasi format waktu yang lebih baik
2. ✅ Error messages yang lebih informatif
3. ✅ Preview yang lebih detail dengan tanggal lengkap
4. ✅ Auto-update preview saat user mengetik
5. ✅ Text color yang adaptive (error = merah, success = hijau)
6. ✅ Log messages yang lebih jelas untuk mode 30 hari
7. ✅ Checkbox individual otomatis ter-uncheck ketika 30 days mode aktif

### 📁 Files Modified

1. **gui.py**
   - Tambah field `self.batch_specific_time` (batch scheduling dengan format 24 jam)
   - Tambah field `self.quick_specific_time` (quick create dengan format 24 jam)
   - **Tambah checkbox `self.schedule_30_days` (fitur baru 30 hari)**
   - **Tambah fungsi `on_30_days_toggle()` untuk handle 30 days mode**
   - Update fungsi `update_batch_datetime()` dengan logic:
     - Waktu spesifik (24 jam)
     - Mode 30 hari otomatis
     - Preview yang lebih informatif
   - Update fungsi `process_batch()` untuk:
     - Handle waktu spesifik
     - Generate 30 hari otomatis ketika mode aktif
     - Log messages yang lebih detail
   - Update fungsi `update_quick_datetime()` untuk quick create
   - Improve preview text dan color

### 📝 Documentation

1. **FITUR_JAM_SPESIFIK.md** - Dokumentasi lengkap fitur baru
2. **CHANGELOG_SPECIFIC_TIME.md** - Changelog ini

### 🎯 Use Cases

#### Use Case 1: Channel Berita Pagi
- **Kebutuhan:** Publish berita setiap pagi jam 6
- **Setting:** Set jam `06:00`, pilih 7 hari, interval `0 min`
- **Hasil:** Konten publish otomatis setiap hari jam 6 pagi

#### Use Case 2: Live Streaming Prime Time
- **Kebutuhan:** Live stream setiap malam jam 8
- **Setting:** Set jam `20:00`, pilih 7 hari, interval `0 min`
- **Hasil:** Live stream terjadwal setiap malam jam 8

#### Use Case 3: Marathon Stream (Multiple per Hari)
- **Kebutuhan:** 5 live streams dalam 1 hari, mulai jam 10 pagi, jarak 2 jam
- **Setting:** Set jam `10:00`, pilih +1 day, interval `+2 hours`, Excel 5 rows
- **Hasil:** Stream pada jam 10:00, 12:00, 14:00, 16:00, 18:00

### 🔮 Future Enhancements (Ideas)

- [ ] Preset waktu populer (Morning: 06:00, Prime Time: 19:00, dll.)
- [ ] Support multiple waktu yang berbeda per hari (misal: Senin jam 10, Selasa jam 15)
- [ ] Time picker UI widget (kalender + jam)
- [ ] Timezone support
- [ ] Randomize time (misal: antara 08:00 - 10:00)

### 📞 Support

Jika ada pertanyaan atau menemukan bug, silakan:
1. Baca dokumentasi lengkap di `FITUR_JAM_SPESIFIK.md`
2. Cek troubleshooting section
3. Periksa logs di tab "Logs"

---

**Version:** 1.0  
**Release Date:** 2025-11-29  
**Compatibility:** AutoLiveBio v1.x
