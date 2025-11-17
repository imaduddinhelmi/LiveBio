# ⏰ Panduan: Jadwalkan Live dengan Waktu Berbeda-Beda

## 🎯 Overview

Anda bisa menjadwalkan multiple live broadcasts dengan **waktu yang berbeda-beda** untuk setiap broadcast menggunakan kolom `scheduledStartTime` di Excel.

---

## 📊 Cara 1: Waktu Spesifik di Excel (Recommended)

### Format Excel:

Tambahkan kolom **`scheduledStartTime`** di Excel Anda:

| title | description | tags | privacyStatus | **scheduledStartTime** |
|-------|-------------|------|---------------|----------------------|
| Live Stream 1 | Gaming session | gaming,live | public | **2025-11-20T20:00:00** |
| Live Stream 2 | Gaming session | gaming,live | public | **2025-11-20T22:30:00** |
| Live Stream 3 | Gaming session | gaming,live | public | **2025-11-21T14:00:00** |
| Live Stream 4 | Gaming session | gaming,live | public | **2025-11-21T20:00:00** |

### Format Waktu yang Didukung:

#### Format 1: ISO Format (Recommended)
```
2025-11-20T20:00:00
2025-11-20T20:00:00Z
```

#### Format 2: Standard DateTime
```
2025-11-20 20:00:00
```

### Langkah-langkah:

1. **Buat Excel dengan kolom scheduledStartTime**
   ```excel
   title                | scheduledStartTime
   Live Gaming Night 1  | 2025-11-20T20:00:00
   Live Gaming Night 2  | 2025-11-22T21:30:00
   Live Gaming Night 3  | 2025-11-24T19:00:00
   ```

2. **Load Excel di Aplikasi**
   - Tab "Import & Run"
   - Click "Select Excel File"
   - Pilih file Excel Anda

3. **Preview Check**
   - Pastikan waktu terbaca dengan benar di preview

4. **Process Batch**
   - Set waktu di GUI **TIDAK AKAN DIGUNAKAN** (diabaikan)
   - Waktu dari Excel yang akan dipakai
   - Click "Process Batch"

### Hasil:
```
[INFO] Row 1: Using scheduled time from Excel: 2025-11-20 20:00
[INFO] Row 2: Using scheduled time from Excel: 2025-11-22 21:30
[INFO] Row 3: Using scheduled time from Excel: 2025-11-24 19:00
```

---

## 📊 Cara 2: Mix - Sebagian di Excel, Sebagian Auto

Anda bisa mix antara waktu spesifik dan waktu otomatis:

### Format Excel:

| title | scheduledStartTime |
|-------|-------------------|
| Live Stream 1 | **2025-11-20T20:00:00** |
| Live Stream 2 | *(kosong)* |
| Live Stream 3 | *(kosong)* |
| Live Stream 4 | **2025-11-25T15:00:00** |

### Langkah:

1. Load Excel
2. Set di GUI:
   - Date: 2025-11-21
   - Time: 20:00
   - Interval: +1 hour

### Hasil:
```
Live Stream 1: 2025-11-20 20:00  (dari Excel)
Live Stream 2: 2025-11-21 20:00  (auto: base time)
Live Stream 3: 2025-11-21 21:00  (auto: base + 1 hour)
Live Stream 4: 2025-11-25 15:00  (dari Excel)
```

---

## 📊 Cara 3: Semua Otomatis (Tanpa scheduledStartTime)

Jika **tidak ada** kolom `scheduledStartTime` di Excel, aplikasi akan gunakan interval otomatis.

### Format Excel:

| title | description | tags | privacyStatus |
|-------|-------------|------|---------------|
| Live Stream 1 | Gaming | gaming | public |
| Live Stream 2 | Gaming | gaming | public |
| Live Stream 3 | Gaming | gaming | public |

### Setting di GUI:
- Date: 2025-11-20
- Time: 20:00
- Interval: +2 hours

### Hasil:
```
Live Stream 1: 2025-11-20 20:00
Live Stream 2: 2025-11-20 22:00
Live Stream 3: 2025-11-21 00:00
```

---

## 🎓 Contoh Use Cases

### Use Case 1: Event dengan Schedule Tidak Teratur

**Scenario:** Event 3 hari dengan waktu mulai berbeda-beda

**Excel:**
```excel
title                    | scheduledStartTime
Opening Ceremony         | 2025-11-20T09:00:00
Workshop Session 1       | 2025-11-20T10:30:00
Lunch Break Stream       | 2025-11-20T12:00:00
Workshop Session 2       | 2025-11-20T14:00:00
Day 1 Closing           | 2025-11-20T17:30:00

Day 2 Opening           | 2025-11-21T09:30:00
Panel Discussion        | 2025-11-21T11:00:00
Afternoon Session       | 2025-11-21T15:00:00

Grand Finale            | 2025-11-22T19:00:00
```

**Proses:**
1. Load Excel
2. Click "Process Batch"
3. Semua 9 broadcasts dibuat dengan waktu sesuai Excel ✅

---

### Use Case 2: Live Stream Mingguan

**Scenario:** Live setiap Selasa & Kamis jam berbeda

**Excel:**
```excel
title                | scheduledStartTime
Tuesday Live #1      | 2025-11-19T20:00:00
Thursday Live #1     | 2025-11-21T21:30:00
Tuesday Live #2      | 2025-11-26T20:00:00
Thursday Live #2     | 2025-11-28T21:30:00
```

---

### Use Case 3: Marathon Streaming

**Scenario:** 12 jam marathon dengan break tidak teratur

**Excel:**
```excel
title                | scheduledStartTime
Marathon Start       | 2025-11-20T10:00:00
Session 1            | 2025-11-20T10:00:00
Break 1 (10 min)     | -
Session 2            | 2025-11-20T12:10:00
Lunch Break (30 min) | -
Session 3            | 2025-11-20T14:40:00
Break 2 (15 min)     | -
Session 4            | 2025-11-20T16:55:00
Dinner Break (45 min)| -
Session 5            | 2025-11-20T19:40:00
Final Session        | 2025-11-20T21:30:00
```

---

## 💡 Tips & Best Practices

### 1. Format Waktu

**✅ RECOMMENDED:**
```
2025-11-20T20:00:00
2025-11-20T20:00:00Z
```

**✅ JUGA DITERIMA:**
```
2025-11-20 20:00:00
```

**❌ TIDAK VALID:**
```
20/11/2025 20:00        (format salah)
2025-11-20 8:00 PM      (format salah)
tomorrow 8pm            (tidak bisa parse)
```

### 2. Timezone

- Semua waktu dalam **local timezone** Anda
- Aplikasi akan convert ke UTC (tambah 'Z')
- Contoh: `2025-11-20T20:00:00` → `2025-11-20T20:00:00Z`

### 3. Waktu Minimum

**⚠️ Penting:**
- Minimal **15 menit** dari sekarang
- YouTube perlu waktu untuk setup
- Jangan schedule di masa lalu

### 4. Kolom Excel

**Wajib:**
- `title` ✅
- `description` ✅
- `privacyStatus` ✅

**Opsional untuk waktu:**
- `scheduledStartTime` - Untuk waktu spesifik
- Jika kosong/tidak ada - Gunakan interval auto

### 5. Preview Before Process

Selalu check preview untuk verify waktu:

```
Preview:
Row 1:
  title: Live Stream 1
  scheduledStartTime: 2025-11-20T20:00:00Z  ✅

Row 2:
  title: Live Stream 2
  scheduledStartTime: None  → Will use auto interval
```

---

## 🎯 Template Excel

### Template 1: Waktu Spesifik

Download atau buat file dengan format ini:

```excel
title                    | description          | tags          | privacyStatus | scheduledStartTime
Live Gaming Session 1    | Playing games        | gaming,live   | public        | 2025-11-20T20:00:00
Live Gaming Session 2    | Playing games        | gaming,live   | public        | 2025-11-20T22:00:00
Live Gaming Session 3    | Playing games        | gaming,live   | public        | 2025-11-21T20:00:00
```

### Template 2: Mixed Mode

```excel
title                    | scheduledStartTime
Morning Show Mon         | 2025-11-20T09:00:00
Evening Show Mon         | (leave empty)
Morning Show Tue         | 2025-11-21T09:00:00
Evening Show Tue         | (leave empty)
```

### Template 3: Dengan Monetization

```excel
title       | scheduledStartTime      | enableMonetization | tags
Live 1      | 2025-11-20T20:00:00    | TRUE              | gaming
Live 2      | 2025-11-22T21:00:00    | TRUE              | gaming
Live 3      | 2025-11-24T19:30:00    | FALSE             | gaming
```

---

## 🐛 Troubleshooting

### Problem 1: Waktu Tidak Terbaca

**Error:**
```
[INFO] Scheduled for: 2025-11-21 20:00  (auto)
```

**Penyebab:** Format waktu di Excel salah

**Solusi:**
1. Gunakan format: `2025-11-20T20:00:00`
2. Pastikan kolom bernama `scheduledStartTime` (exact)
3. Check preview apakah waktu terbaca

### Problem 2: Waktu di Masa Lalu

**Error:**
```
[X] Error: Scheduled time is in the past
```

**Solusi:**
1. Update waktu di Excel ke masa depan
2. Minimal 15 menit dari sekarang

### Problem 3: Format Date Salah

**Error:**
```
[X] Error parsing scheduledStartTime
```

**Solusi:**
1. Change format: `YYYY-MM-DDTHH:MM:SS`
2. Contoh: `2025-11-20T20:00:00`
3. Hindari format: `DD/MM/YYYY` atau `MM/DD/YYYY`

---

## ✅ Checklist

Sebelum process batch dengan waktu berbeda:

- [ ] Kolom `scheduledStartTime` ada di Excel
- [ ] Format waktu: `2025-11-20T20:00:00`
- [ ] Semua waktu di masa depan (minimal +15 menit)
- [ ] Preview OK - waktu terbaca dengan benar
- [ ] Kolom wajib terisi (title, description, privacy)
- [ ] Ready to process

---

## 📊 Comparison Chart

| Method | Flexibility | Ease of Use | Best For |
|--------|------------|-------------|----------|
| **Waktu di Excel** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | Event schedule, custom timing |
| **Interval Auto** | ⭐⭐ | ⭐⭐⭐⭐⭐ | Regular streaming, simple schedule |
| **Mix Mode** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Combination of both |

---

## 🎬 Video Tutorial Steps

### Step-by-Step:

1. **Create Excel File**
   ```
   Open Excel → Create new workbook
   Add columns: title, description, scheduledStartTime
   Fill with your data
   Save as broadcasts_custom_time.xlsx
   ```

2. **Fill Time Column**
   ```
   Cell format: Text or General
   Enter: 2025-11-20T20:00:00
   Copy down for all rows
   Adjust time for each row
   ```

3. **Import to Application**
   ```
   Open AutoLiveBio
   Tab: Import & Run
   Click: Select Excel File
   Choose: broadcasts_custom_time.xlsx
   ```

4. **Verify Preview**
   ```
   Check preview section
   Verify scheduledStartTime shows correctly
   If empty → will use auto interval
   If filled → will use exact time
   ```

5. **Process**
   ```
   Click: Process Batch
   Wait for completion
   Check Logs for confirmation
   ```

---

## 🎉 Summary

### Quick Reference:

**Untuk Waktu Berbeda:** ✅ Tambahkan kolom `scheduledStartTime` di Excel

**Format:**
```
2025-11-20T20:00:00
atau
2025-11-20T20:00:00Z
```

**Proses:**
1. Excel + kolom scheduledStartTime
2. Load di aplikasi
3. Process Batch
4. Done! ✅

**Keuntungan:**
- ✅ Full control atas waktu setiap broadcast
- ✅ Bisa set waktu tidak teratur
- ✅ Perfect untuk event schedule
- ✅ Mix dengan auto interval

**Selamat menjadwalkan!** 🚀
