# 🎯 Panduan Multiple Base Time & Interval

## ✨ Fitur Baru: Multiple Base Time Selection

Sekarang Anda dapat memilih **BANYAK base time sekaligus** untuk menjadwalkan broadcast di berbagai waktu dalam satu proses!

---

## 📋 Apa itu Base Time?

**Base Time** adalah waktu awal/dasar untuk memulai scheduling broadcast Anda.

### Pilihan Base Time:
- **Now** = Sekarang juga
- **+1 day** ⭐ = 1 hari dari sekarang (besok) - DEFAULT TERCENTANG
- **+2 days** ⭐ = 2 hari dari sekarang (lusa) - DEFAULT TERCENTANG
- **+3 days** ⭐ = 3 hari dari sekarang - DEFAULT TERCENTANG
- **+4 days** ⭐ = 4 hari dari sekarang - DEFAULT TERCENTANG
- **+5 days** ⭐ = 5 hari dari sekarang - DEFAULT TERCENTANG
- **+6 days** ⭐ = 6 hari dari sekarang - DEFAULT TERCENTANG
- **+7 days** ⭐ = 7 hari dari sekarang (seminggu lagi) - DEFAULT TERCENTANG

**🎯 Default:** Saat aplikasi dibuka, **7 hari sudah tercentang otomatis** untuk kemudahan scheduling mingguan!

---

## 🕒 Apa itu Interval?

**Interval** adalah jarak waktu antara setiap broadcast yang dijadwalkan.

### Pilihan Interval:
- **0 min (all same)** = Semua broadcast di waktu yang sama
- **+5 min** = Jarak 5 menit
- **+10 min** = Jarak 10 menit
- **+15 min** = Jarak 15 menit
- **+30 min** = Jarak 30 menit
- **+1 hour** = Jarak 1 jam
- **+2 hours** = Jarak 2 jam
- **+1 day** = Jarak 1 hari

---

## 💡 CONTOH PENGGUNAAN

### Contoh 1: Single Base Time dengan Interval
**Setting:**
- ☑️ Base Time: **+1 day** (besok jam 10:00)
- Interval: **+15 min**
- Jumlah broadcast di Excel: 5

**Hasil:**
```
Broadcast 1: Besok 10:00
Broadcast 2: Besok 10:15
Broadcast 3: Besok 10:30
Broadcast 4: Besok 10:45
Broadcast 5: Besok 11:00
```

---

### Contoh 2: Multiple Base Times dengan Interval 0
**Setting:**
- ☑️ Base Time: **+1 day** (besok jam 10:00)
- ☑️ Base Time: **+2 days** (lusa jam 10:00)
- ☑️ Base Time: **+3 days** (3 hari lagi jam 10:00)
- Interval: **0 min (all same)**
- Jumlah broadcast di Excel: 3

**Hasil:**
```
BATCH 1 (Besok 10:00):
- Broadcast 1: Besok 10:00
- Broadcast 2: Besok 10:00
- Broadcast 3: Besok 10:00

BATCH 2 (Lusa 10:00):
- Broadcast 1: Lusa 10:00
- Broadcast 2: Lusa 10:00
- Broadcast 3: Lusa 10:00

BATCH 3 (3 hari lagi 10:00):
- Broadcast 1: 3 hari lagi 10:00
- Broadcast 2: 3 hari lagi 10:00
- Broadcast 3: 3 hari lagi 10:00

Total: 9 broadcasts dibuat!
```

---

### Contoh 3: Multiple Base Times dengan Interval
**Setting:**
- ☑️ Base Time: **+1 day** (besok jam 09:00)
- ☑️ Base Time: **+2 days** (lusa jam 09:00)
- Interval: **+1 hour**
- Jumlah broadcast di Excel: 4

**Hasil:**
```
BATCH 1 (Besok 09:00):
- Broadcast 1: Besok 09:00
- Broadcast 2: Besok 10:00
- Broadcast 3: Besok 11:00
- Broadcast 4: Besok 12:00

BATCH 2 (Lusa 09:00):
- Broadcast 1: Lusa 09:00
- Broadcast 2: Lusa 10:00
- Broadcast 3: Lusa 11:00
- Broadcast 4: Lusa 12:00

Total: 8 broadcasts dibuat!
```

---

### Contoh 4: Scheduling Harian untuk Seminggu
**Setting:**
- ☑️ Base Time: **+1 day** (besok jam 18:00)
- ☑️ Base Time: **+2 days** (lusa jam 18:00)
- ☑️ Base Time: **+3 days** (3 hari lagi jam 18:00)
- ☑️ Base Time: **+4 days** (4 hari lagi jam 18:00)
- ☑️ Base Time: **+5 days** (5 hari lagi jam 18:00)
- ☑️ Base Time: **+6 days** (6 hari lagi jam 18:00)
- ☑️ Base Time: **+7 days** (7 hari lagi jam 18:00)
- Interval: **0 min (all same)**
- Jumlah broadcast di Excel: 1

**Hasil:**
```
7 broadcasts, masing-masing jam 18:00 selama 7 hari berturut-turut!
```

---

## 🎬 Cara Menggunakan

### Step 1: Pilih Base Times
1. Scroll di kotak **"📋 Select Base Time(s)"**
2. **Centang** semua base time yang Anda inginkan
3. Preview waktu akan muncul di sebelah kanan setiap pilihan

### Step 2: Pilih Interval
1. Pilih interval dari dropdown **"Interval"**
2. Klik **"ℹ️ What is Interval?"** untuk penjelasan detail

### Step 3: Quick Actions
- Tombol **"✓ Select All"** = Pilih semua base time
- Tombol **"✗ Deselect All"** = Hapus semua pilihan
- Tombol **"🔄 Refresh Preview"** = Update preview waktu

### Step 4: Process
1. Klik **"Process Batch"**
2. Sistem akan membuat broadcast untuk setiap base time yang dipilih
3. Log akan menampilkan progress untuk setiap batch

---

## 📊 Keuntungan Multiple Base Times

### ✅ Efisiensi Waktu
- Tidak perlu proses manual berulang-ulang
- Sekali klik untuk banyak waktu

### ✅ Konsistensi
- Semua batch menggunakan data Excel yang sama
- Format dan settings uniform

### ✅ Fleksibilitas
- Bisa scheduling untuk hari ini, besok, atau seminggu ke depan
- Kombinasi interval sesuai kebutuhan

### ✅ Batch Management
- Log terpisah untuk setiap batch
- Mudah tracking success/error per base time

---

## ⚠️ Tips & Best Practices

### 1. Perencanaan Waktu
```
❌ JANGAN: Pilih terlalu banyak base time jika broadcast Anda banyak
✅ LAKUKAN: Hitung total broadcasts yang akan dibuat
   
   Formula: Total = (Jumlah Base Times) × (Jumlah Rows di Excel)
```

### 2. YouTube Quota Limits
```
⚠️ YouTube API memiliki quota harian!
   
   Jika banyak broadcasts:
   - Gunakan interval yang lebih besar
   - Atau pilih lebih sedikit base times
   - Monitor quota usage
```

### 3. Testing
```
💡 TIP: Test dengan 1-2 base times dulu
   Setelah yakin, baru tambahkan lebih banyak
```

### 4. Kombinasi Interval
```
Untuk broadcast harian jam yang sama:
✅ Multiple base times (1 hari interval antar pilihan)
✅ Interval: 0 min (all same)

Untuk broadcast dalam 1 hari dengan jarak:
✅ Single base time (misalnya +1 hour)
✅ Interval: +30 min atau +1 hour
```

---

## 🔧 Technical Details

### Bagaimana Sistem Bekerja?

1. **User memilih multiple base times** → Sistem menyimpan semua pilihan
2. **User klik Process Batch** → Sistem membuat loop untuk setiap base time
3. **Untuk setiap base time:**
   - Load semua rows dari Excel
   - Hitung waktu: `broadcast_time = base_time + (interval × index)`
   - Buat broadcast via YouTube API
   - Log hasil per broadcast
4. **Summary akhir** menampilkan total dari semua batches

### Data Safety
- **Row data di-copy** untuk setiap batch (tidak modify original)
- Jika satu batch gagal, batch lain tetap jalan
- Error di satu broadcast tidak stop seluruh proses

---

## 🎯 Use Cases

### Use Case 1: Content Creator Rutin
```
Scenario: Upload live broadcast setiap hari jam 19:00 selama seminggu

Setup:
- Pilih 7 base times (+1 day sampai +7 days)
- Interval: 0 min (all same)
- Excel: 1 row dengan detail broadcast

Result: 7 broadcasts terjadwal jam 19:00 selama 7 hari
```

### Use Case 2: Marathon Streaming
```
Scenario: 10 broadcasts dalam 1 hari, dimulai jam 09:00 dengan jarak 30 menit

Setup:
- Base Time: +30 min (09:00)
- Interval: +30 min
- Excel: 10 rows

Result: Broadcasts dari 09:00 - 13:30
```

### Use Case 3: Multi-Platform Testing
```
Scenario: Test di 3 waktu berbeda untuk analisis audience

Setup:
- Base times: +1 hour, +6 hours, +12 hours
- Interval: 0 min
- Excel: 1 row

Result: 3 broadcasts di jam berbeda, konten sama
```

---

## 📞 Troubleshooting

### ⚠️ "Please select at least one base time!"
**Solusi:** Centang minimal 1 base time sebelum Process

### ⚠️ Tidak ada preview waktu muncul
**Solusi:** Klik tombol "🔄 Refresh Preview"

### ⚠️ Terlalu banyak broadcasts dibuat
**Solusi:** 
- Cek jumlah base times yang dicentang
- Total = Base Times × Excel Rows
- Kurangi jumlah base times atau rows

### ⚠️ YouTube API Quota Exceeded
**Solusi:**
- Tunggu 24 jam untuk reset quota
- Kurangi jumlah broadcasts
- Gunakan test mode untuk planning

---

## 🚀 Quick Start Examples

### Example 1: Besok & Lusa
```
✓ Checkbox: +1 day
✓ Checkbox: +2 days
Interval: 0 min (all same)
→ Buat 2 kali jumlah row Excel Anda
```

### Example 2: Akhir Pekan
```
✓ Checkbox: +5 days (Sabtu)
✓ Checkbox: +6 days (Minggu)
Interval: +1 hour
→ 2 batches untuk weekend dengan spacing 1 jam
```

### Example 3: Weekend Special
```
✓ Checkbox: +2 days (Sabtu)
✓ Checkbox: +3 days (Minggu)  
Interval: +1 hour
→ Weekend broadcasts dengan jarak 1 jam
```

---

## 📝 Summary

| Feature | Deskripsi |
|---------|-----------|
| **Multiple Base Times** | Pilih banyak waktu start sekaligus |
| **Interval** | Jarak waktu antar broadcasts dalam 1 batch |
| **Total Broadcasts** | Base Times × Excel Rows |
| **Independent Batches** | Setiap base time proses terpisah |
| **Error Handling** | 1 batch gagal tidak pengaruhi batch lain |

---

## 🎉 Selamat Menggunakan!

Fitur Multiple Base Times membuat scheduling YouTube Live Broadcasts jauh lebih efisien dan fleksibel. Eksperimen dengan berbagai kombinasi untuk menemukan workflow terbaik untuk kebutuhan Anda!

**Happy Streaming! 🎬📡**
