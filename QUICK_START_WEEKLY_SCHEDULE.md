# 🚀 Quick Start: Weekly Schedule (1 Minggu Otomatis!)

## ⚡ Fitur Auto Week Selection

Saat Anda membuka aplikasi, **7 hari sudah tercentang otomatis**!  
Tidak perlu centang manual satu per satu. Langsung siap untuk scheduling mingguan!

---

## 📋 3 Langkah Super Cepat

### 1️⃣ Buka Aplikasi
```
✅ +1 day    (sudah tercentang)
✅ +2 days   (sudah tercentang)
✅ +3 days   (sudah tercentang)
✅ +4 days   (sudah tercentang)
✅ +5 days   (sudah tercentang)
✅ +6 days   (sudah tercentang)
✅ +7 days   (sudah tercentang)
```

### 2️⃣ Load Excel File
- Klik "Select Excel File"
- Pilih file broadcasts Anda
- Preview akan muncul

### 3️⃣ Process!
- Pilih Interval (default: "0 min (all same)")
- Klik "Process Batch"
- **DONE!** 🎉

---

## 🎯 Hasil Default

Dengan **1 row di Excel** dan **7 hari tercentang**:

```
Broadcast 1: Besok jam 10:00
Broadcast 2: Lusa jam 10:00
Broadcast 3: 3 hari lagi jam 10:00
Broadcast 4: 4 hari lagi jam 10:00
Broadcast 5: 5 hari lagi jam 10:00
Broadcast 6: 6 hari lagi jam 10:00
Broadcast 7: 7 hari lagi jam 10:00

Total: 7 broadcasts untuk 1 minggu penuh!
```

---

## 🎬 Contoh Real Use Cases

### Case 1: Daily News/Update Channel
**Excel:** 1 row dengan template news broadcast  
**Setup:** Biarkan 7 hari tercentang, interval: 0 min  
**Hasil:** 7 broadcasts, satu per hari, waktu sama  
**Perfect untuk:** Daily news, weather, market update

---

### Case 2: Tutorial Series (7 Episodes)
**Excel:** 7 rows, masing-masing tutorial berbeda  
**Setup:** 7 hari tercentang, interval: 0 min  
**Hasil:** 49 broadcasts (7 hari × 7 episodes)  
**Perfect untuk:** Series belajar, course online

---

### Case 3: Multiple Shows Per Day
**Excel:** 3 rows (pagi, siang, malam)  
**Setup:** 7 hari tercentang, interval: +4 hours  
**Hasil:** 21 broadcasts dengan jarak 4 jam  
**Perfect untuk:** News cycle, variety shows

---

### Case 4: Weekend Only
**Excel:** 1 row  
**Setup:**
- ❌ Uncheck +1 day sampai +4 days
- ✅ Keep checked +5, +6, +7 (Jum'at, Sabtu, Minggu)
- Interval: 0 min

**Hasil:** 3 broadcasts untuk weekend  
**Perfect untuk:** Weekend special, family content

---

## 🔧 Customization

### Jika Tidak Perlu 7 Hari:

**Uncheck yang tidak diperlukan!**

Contoh untuk 3 hari saja:
```
❌ +1 day
✅ +2 days
❌ +3 days
✅ +4 days
❌ +5 days
✅ +6 days
❌ +7 days

Hasil: Hanya 3 broadcasts di hari ke-2, 4, dan 6
```

---

### Gunakan Button Quick Actions:

1. **✗ Deselect All** → Hapus semua centang
2. **✓ Select All** → Centang semua lagi
3. **🔄 Refresh Preview** → Update preview waktu

---

## 💡 Pro Tips

### Tip 1: Test dengan "Now"
```
Uncheck semua 7 hari
Check "Now" saja
Excel: 1 row
→ Quick test tanpa tunggu!
```

### Tip 2: Alternate Days
```
✅ +1 day
❌ +2 days
✅ +3 days
❌ +4 days
✅ +5 days
❌ +6 days
✅ +7 days
→ Setiap 2 hari sekali
```

### Tip 3: Weekday Only (5 hari kerja)
```
✅ +1 day (Senin)
✅ +2 days (Selasa)
✅ +3 days (Rabu)
✅ +4 days (Kamis)
✅ +5 days (Jumat)
❌ +6 days (Sabtu)
❌ +7 days (Minggu)
→ Content untuk weekday saja
```

### Tip 4: Multiple Intervals
```
Setup 1:
- 7 hari tercentang
- Interval: 0 min
- Excel: 1 row
→ 7 broadcasts di waktu yang sama

Setup 2:
- 7 hari tercentang
- Interval: +1 hour
- Excel: 5 rows
→ 35 broadcasts (5 per hari dengan jarak 1 jam)
```

---

## ⚠️ Important Notes

### YouTube Quota
```
Total Broadcasts = (Days Selected) × (Excel Rows)

7 hari × 10 rows = 70 broadcasts!
→ Pastikan quota YouTube cukup
```

### Preview Time
```
Setiap base time menampilkan preview:
+1 day → 2025-11-25 10:00
+2 days → 2025-11-26 10:00
...

Cek dulu sebelum process!
```

### Interval Explanation
```
Interval = Jarak ANTAR broadcasts dalam 1 BATCH

Contoh:
- 7 hari tercentang
- Interval: +30 min
- Excel: 3 rows

Setiap hari akan ada 3 broadcasts dengan jarak 30 menit:
Besok: 10:00, 10:30, 11:00
Lusa: 10:00, 10:30, 11:00
dst...
```

---

## 🎯 Formula Cepat

### Berapa Total Broadcasts?
```
Total = (Jumlah Hari Tercentang) × (Jumlah Rows di Excel)
```

### Berapa Lama Proses?
```
Estimasi: ~3-5 detik per broadcast
100 broadcasts ≈ 5-8 menit

Tergantung internet & YouTube API response
```

### Berapa Quota Terpakai?
```
1 broadcast = ~50 quota points

Quota harian YouTube: 10,000 points
Maksimal broadcasts per hari: ~200

Lebih dari itu, tunggu 24 jam untuk reset!
```

---

## 🚀 Ready to Go!

1. **Buka aplikasi** → 7 hari sudah tercentang ✅
2. **Load Excel** → Data ready
3. **Click Process Batch** → Done! 🎉

**Scheduling 1 minggu penuh tidak pernah semudah ini!**

---

## 📞 Need Help?

### Lihat dokumentasi lengkap:
- `MULTIPLE_BASE_TIME_GUIDE.md` - Panduan detail
- `BASE_TIME_UPDATE.md` - Update terbaru
- `CHANGELOG_MULTIPLE_BASE_TIME.md` - Technical details

### Tombol Help:
- Klik **"ℹ️ What is Interval?"** di aplikasi untuk penjelasan

---

**Happy Scheduling! 🎬📅✨**
