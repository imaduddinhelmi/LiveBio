# ⚡ Quick Guide: Jadwalkan Live dengan Waktu Berbeda

## 🎯 3 Langkah Mudah

### 1. Buat Excel dengan Kolom `scheduledStartTime`

```excel
title                | scheduledStartTime
Live Gaming #1       | 2025-11-20T20:00:00
Live Gaming #2       | 2025-11-22T21:30:00
Live Gaming #3       | 2025-11-24T19:00:00
```

### 2. Load di Aplikasi

- Tab **"Import & Run"**
- Click **"Select Excel File"**
- Pilih file Anda

### 3. Process

- Click **"Process Batch"**
- Done! ✅

---

## 📋 Format Waktu

**✅ Format yang Didukung:**
```
2025-11-20T20:00:00
2025-11-20T20:00:00Z
2025-11-20 20:00:00
```

**❌ Format Salah:**
```
20/11/2025 20:00
11-20-2025 8:00 PM
```

---

## 💡 Tips Cepat

### Kolom Wajib di Excel:
- `title` ✅
- `description` ✅  
- `privacyStatus` ✅
- `scheduledStartTime` ✅ (untuk waktu custom)

### Waktu Minimal:
- **Minimal 15 menit** dari sekarang
- Jangan schedule di masa lalu

### Mode Campuran:
Bisa mix waktu custom dan auto!

```excel
title        | scheduledStartTime
Live 1       | 2025-11-20T20:00:00  (custom)
Live 2       | (kosong - akan pakai auto)
Live 3       | (kosong - akan pakai auto)
Live 4       | 2025-11-25T15:00:00  (custom)
```

---

## 📁 Sample Files

Sudah ada 3 sample Excel di folder aplikasi:

1. **sample_broadcasts_custom_time.xlsx**
   - 5 broadcasts dengan waktu berbeda
   - Mixed schedule

2. **sample_event_schedule.xlsx**
   - Event 3 hari
   - 10 sessions dengan waktu spesifik

3. **sample_weekly_schedule.xlsx**
   - 4 minggu schedule
   - Pattern Selasa/Kamis

**Cara Pakai:**
1. Buka file sample
2. Edit waktu sesuai kebutuhan
3. Load di aplikasi
4. Process!

---

## 🎯 Contoh Praktis

### Contoh 1: Event 1 Hari

```excel
title                  | scheduledStartTime
Opening Ceremony       | 2025-11-20T09:00:00
Morning Session        | 2025-11-20T10:30:00
Lunch Break Talk       | 2025-11-20T12:00:00
Afternoon Workshop     | 2025-11-20T14:00:00
Closing Remarks        | 2025-11-20T17:00:00
```

### Contoh 2: Streaming Mingguan

```excel
title                  | scheduledStartTime
Week 1 - Monday        | 2025-11-18T20:00:00
Week 1 - Friday        | 2025-11-22T21:30:00
Week 2 - Monday        | 2025-11-25T20:00:00
Week 2 - Friday        | 2025-11-29T21:30:00
```

### Contoh 3: Marathon Stream

```excel
title                  | scheduledStartTime
Marathon Start         | 2025-11-20T10:00:00
Session 1              | 2025-11-20T10:00:00
Break & Chat           | 2025-11-20T12:00:00
Session 2              | 2025-11-20T12:30:00
Lunch Break            | 2025-11-20T14:30:00
Session 3              | 2025-11-20T15:00:00
Final Sprint           | 2025-11-20T19:00:00
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Waktu tidak terbaca | Check format: `2025-11-20T20:00:00` |
| Error "past time" | Update waktu ke masa depan |
| Kolom tidak terbaca | Check nama: `scheduledStartTime` (exact) |

---

## ✅ Checklist

Sebelum process:
- [ ] Kolom `scheduledStartTime` ada
- [ ] Format: `2025-11-20T20:00:00`
- [ ] Semua waktu di masa depan
- [ ] Preview OK

---

## 🚀 Ready to Go!

1. **Buat Excel** dengan kolom `scheduledStartTime`
2. **Isi waktu** berbeda untuk setiap row
3. **Load** di Tab "Import & Run"
4. **Process Batch** ✅

**Panduan lengkap:** Buka `PANDUAN_WAKTU_BERBEDA.md`

---

## 📞 Quick Help

**Lokasi:**
- Tab: **Import & Run**
- Button: **Select Excel File**
- Then: **Process Batch**

**Sample Files:**
- `sample_broadcasts_custom_time.xlsx`
- `sample_event_schedule.xlsx`
- `sample_weekly_schedule.xlsx`

**Format Waktu:**
- `YYYY-MM-DDTHH:MM:SS`
- Example: `2025-11-20T20:00:00`

Done! 🎉
