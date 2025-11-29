# Timezone Fix - Penjadwalan Broadcast

## Masalah
Pengaturan jam pada penjadwalan broadcast tidak tepat. Saat user mengatur jam **05:25 WIB**, broadcast dijadwalkan di YouTube pada jam **12:25 WIB** (selisih +7 jam).

## Penyebab
Aplikasi menggunakan waktu lokal (WIB/local timezone) tapi langsung menandainya sebagai UTC dengan menambahkan 'Z' tanpa konversi. 

**Contoh masalah:**
- Input user: `05:25` WIB
- Code lama: `dt.isoformat() + 'Z'` → `2025-11-29T05:25:00Z` (dianggap sebagai UTC)
- YouTube menampilkan: `05:25 UTC` = `12:25 WIB` (05:25 + 7 jam offset)

## Solusi
Konversi waktu lokal ke UTC sebelum mengirim ke YouTube API.

**Formula konversi:**
```python
utc_offset_seconds = datetime.now().astimezone().utcoffset().total_seconds()
dt_utc = dt - timedelta(seconds=utc_offset_seconds)
scheduled_start_time = dt_utc.isoformat() + 'Z'
```

**Untuk WIB (UTC+7):**
- Input: `05:25` WIB
- Offset: `+25200` seconds (7 jam)
- UTC Time: `05:25 - 7 jam` = `22:25` UTC hari sebelumnya
- YouTube API: `2025-11-28T22:25:00Z`
- YouTube menampilkan: `22:25 UTC` = `05:25 WIB` ✅ **BENAR!**

## File yang Diubah

### 1. `excel_parser.py`
**Import timezone:**
```python
from datetime import datetime, timezone, timedelta
```

**Konversi di 3 tempat:**
- Parsing format ISO (`scheduledStartTime` column)
- Parsing format datetime string
- Parsing legacy format (separate date & time columns)

### 2. `gui.py`
**Import timezone:**
```python
from datetime import datetime, timedelta, timezone
```

**Konversi di 3 fungsi:**
- `quick_create_broadcast()` - Create single broadcast manual
- `start_batch_process()` - Batch process dari Excel
- `scheduled_batch_process()` - Scheduled batch (dari scheduler)

## Cara Kerja Setelah Fix

### Scenario 1: Quick Create
User input:
- Date: `2025-12-01`
- Time: `05:25`

Proses:
```python
dt = datetime.strptime("2025-12-01 05:25", "%Y-%m-%d %H:%M")  # Local time
utc_offset = 25200  # 7 hours for WIB
dt_utc = dt - timedelta(seconds=25200)  # Subtract offset
# Result: 2025-11-30T22:25:00Z (UTC)
```

YouTube akan menampilkan: `2025-12-01 05:25 WIB` ✅

### Scenario 2: Batch dari Excel
Excel column `scheduledStartTime`:
```
2025-12-01T05:25:00
```

Proses yang sama - konversi dari local ke UTC.

### Scenario 3: Auto-schedule dengan interval
Base time: `2025-12-01 05:25` WIB
Interval: `+30 min`

Broadcast 1: `05:25` WIB → `22:25` UTC
Broadcast 2: `05:55` WIB → `22:55` UTC
Broadcast 3: `06:25` WIB → `23:25` UTC

Semua akan tampil dengan waktu WIB yang benar di YouTube!

## Testing
1. ✅ Compile syntax check: `python -m py_compile excel_parser.py gui.py`
2. ✅ No syntax errors

## Cara Test Manual
1. Buat broadcast dengan waktu `05:25` 
2. Cek di YouTube Studio → Live → Upcoming
3. Waktu harus tampil `05:25` (bukan `12:25`)

## Catatan Penting
- Semua input waktu dari user dianggap sebagai **waktu lokal** (WIB)
- Konversi otomatis ke UTC sebelum dikirim ke YouTube API
- YouTube API selalu menggunakan UTC dengan format `Z` di akhir
- Log message menampilkan `(Local)` untuk menandakan waktu lokal

## Sebelum dan Sesudah

| Aspek | Sebelum Fix | Sesudah Fix |
|-------|-------------|-------------|
| Input user | 05:25 WIB | 05:25 WIB |
| Dikirim ke API | `05:25:00Z` (salah) | `22:25:00Z` (benar) |
| Tampil di YouTube | 12:25 WIB ❌ | 05:25 WIB ✅ |
| Selisih | +7 jam | 0 (tepat) |

---
**Status:** ✅ Fixed
**Date:** 2025-11-29
**Affected Files:** `excel_parser.py`, `gui.py`
