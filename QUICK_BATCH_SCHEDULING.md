# ⚡ Quick Guide: Batch Scheduling

## 🎯 2 Jenis Batch Scheduling

| Jenis | Untuk | Tab | File Excel |
|-------|-------|-----|------------|
| **Broadcast** | Live Streams | Import & Run | broadcasts.xlsx |
| **Video Upload** | Video Files | Video Upload → Batch | videos.xlsx |

---

## 📊 Quick Start: Batch Broadcast

### 1. Siapkan Excel
```excel
title                | tags          | privacyStatus | enableMonetization
Live Stream 1        | gaming,live   | public        | TRUE
Live Stream 2        | gaming,live   | public        | TRUE
Live Stream 3        | gaming,live   | public        | TRUE
```

### 2. Load & Schedule
1. Tab **"Import & Run"**
2. **Select Excel File** → Pilih file
3. Set waktu:
   - **Base Time:** +30 min
   - **Interval:** +1 hour *(jeda antar broadcast)*
   - **Date:** 2025-11-20
   - **Time:** 20:00
4. **Process Batch** ✅

### Hasil:
- Broadcast 1: 20:00
- Broadcast 2: 21:00  
- Broadcast 3: 22:00

---

## 🎬 Quick Start: Batch Video Upload

### 1. Siapkan Excel
```excel
videoPath              | title           | tags     | privacyStatus
D:\Videos\video1.mp4   | Tutorial Part 1 | tutorial | public
D:\Videos\video2.mp4   | Tutorial Part 2 | tutorial | public
D:\Videos\video3.mp4   | Tutorial Part 3 | tutorial | public
```

⚠️ **Path harus lengkap (absolute path)!**

### 2. Load & Schedule
1. Tab **"Video Upload"** → **"Batch Upload"**
2. **Select Excel File** → Pilih file
3. Set waktu:
   - **Start Time:** Klik **"Now"** atau set manual
   - **Interval:** 10 min *(jeda antar upload)*
4. **Schedule All Videos** ✅

### 3. Monitor
- Switch ke tab **"Single Upload"**
- Check **"Scheduled List"**
- Scheduler auto-start ✅

### Hasil:
- Video 1 upload: 20:00
- Video 2 upload: 20:10
- Video 3 upload: 20:20

---

## ⏰ Interval Options

| Interval | Untuk | Use Case |
|----------|-------|----------|
| **0 min** | Semua bersamaan | Broadcasts multiple (not recommended for videos) |
| **5-10 min** | Video pendek | Tutorial videos, shorts |
| **15-30 min** | Video medium | Regular content |
| **1 hour** | Video panjang | Long-form content |
| **2 hours** | Live streams | Gaming sessions |
| **1 day** | Daily content | Streaming harian |

---

## 💡 Tips Cepat

### Path di Excel
```
✅ BENAR:
D:\\Videos\\video1.mp4
D:/Videos/video1.mp4

❌ SALAH:
video1.mp4
.\video1.mp4
```

### Waktu Scheduling
```
✅ Minimal 15 menit dari sekarang
✅ Gunakan interval yang cukup (10-30 min untuk video)
❌ Jangan schedule di masa lalu
❌ Jangan interval terlalu pendek (< 5 min)
```

### Batch Size
```
✅ Recommended: 10-20 items per batch
✅ Maximum: 50 items per hari (safe limit)
❌ Avoid: > 100 items sekaligus
```

---

## 🐛 Troubleshooting Cepat

| Error | Solusi |
|-------|--------|
| "File not found" | Check path di Excel (harus absolute) |
| "Invalid time" | Format: YYYY-MM-DDTHH:MM:SS |
| "Auth failed" | Re-login di tab Auth |
| Scheduler tidak jalan | Check status, restart jika perlu |

---

## 📋 Checklist

Sebelum batch scheduling:
- [ ] File Excel ready
- [ ] Sudah login
- [ ] Preview OK
- [ ] Waktu & interval set
- [ ] File video ada (untuk video upload)

---

## 🎯 Contoh Singkat

### Upload 5 Video dalam 1 Jam
```
Start: 20:00
Interval: 15 min
Files: video1.mp4 - video5.mp4

→ Selesai jam 21:00
```

### Schedule 7 Live Streams (Seminggu)
```
Start: Hari ini 20:00
Interval: +1 day
Rows: 7

→ Live setiap hari jam 20:00
```

---

## 🚀 Ready to Go!

1. Siapkan Excel ✅
2. Load di aplikasi ✅
3. Set waktu & interval ✅
4. Click Process/Schedule ✅
5. Done! 🎉

**Panduan lengkap:** Buka `PANDUAN_SCHEDULING_MASSAL.md`
