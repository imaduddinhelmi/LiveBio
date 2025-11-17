# Excel Format Update - Tanggal dan Waktu Tidak Wajib

## Perubahan

File Excel sample baru (`sample_broadcasts_with_monetization.xlsx`) telah diupdate:

### ❌ DIHAPUS (Optional):
- `scheduledStartDate` - Kolom tanggal dihapus
- `scheduledStartTime` - Kolom waktu dihapus

### ✅ TETAP ADA (Required):
- `title` - Judul broadcast
- `description` - Deskripsi
- `tags` - Tags (comma-separated)
- `categoryId` - YouTube category ID
- `privacyStatus` - public/unlisted/private

### ✅ TETAP ADA (Optional):
- `thumbnailPath`
- `streamId`
- `streamKey`
- `latency`
- `enableDvr`
- `enableEmbed`
- `recordFromStart`
- `madeForKids`
- `containsSyntheticMedia`
- `enableMonetization` ⭐ (NEW)

## Cara Kerja Sekarang

### 1. Tanpa Kolom Tanggal di Excel

**File Excel:**
| title | description | tags | categoryId | privacyStatus | enableMonetization |
|-------|-------------|------|------------|---------------|-------------------|
| My Stream | Description | gaming,live | 20 | public | TRUE |
| Another Stream | Another desc | vlog,daily | 22 | unlisted | TRUE |

**Di Aplikasi (Tab Import & Run):**
1. Load Excel file
2. Set waktu di kontrol "Schedule Time":
   - **Base Time**: +30 min, +1 hour, +2 hours, dll
   - **Interval**: 0 min (all same), +15 min, +30 min, dll
3. Klik "Process Batch"
4. Aplikasi otomatis apply waktu ke semua broadcasts

**Hasil:**
- Broadcast 1: Scheduled di base time
- Broadcast 2: Scheduled di base time + interval
- Broadcast 3: Scheduled di base time + (interval × 2)
- dst...

### 2. Dengan Kolom Tanggal di Excel (Masih Bisa)

Jika mau set waktu berbeda per broadcast, masih bisa tambahkan kolom manual:

| title | scheduledStartDate | scheduledStartTime | ... |
|-------|-------------------|-------------------|-----|
| Stream 1 | 2025-01-15 | 19:00 | ... |
| Stream 2 | 2025-01-16 | 20:00 | ... |

Aplikasi akan gunakan waktu dari Excel, bukan dari kontrol aplikasi.

## Keuntungan

✅ **Excel lebih simpel** - Tidak perlu isi tanggal/waktu manual
✅ **Lebih cepat** - Cukup isi title, description, tags
✅ **Fleksibel** - Set waktu langsung di aplikasi saat import
✅ **Batch scheduling** - Set interval otomatis untuk banyak broadcasts
✅ **Tetap compatible** - Excel lama dengan kolom tanggal masih bisa dipakai

## Sample File Baru

File: `sample_broadcasts_with_monetization.xlsx`

**Isi:**
- 5 sample broadcasts
- Tanpa kolom tanggal/waktu
- Kolom `enableMonetization` sudah TRUE semua
- Siap pakai - tinggal edit title/description

**Cara Pakai:**
1. Edit title, description, tags sesuai kebutuhan
2. Load di aplikasi tab "Import & Run"
3. Set base time & interval di aplikasi
4. Centang "Enable Monetization for ALL broadcasts" (optional)
5. Process Batch

## Workflow Baru

### Workflow Simpel (Recommended):
```
1. Buat Excel hanya dengan kolom required:
   - title, description, tags, categoryId, privacyStatus

2. Optional: Tambah enableMonetization (atau pakai global override di app)

3. Load Excel di aplikasi

4. Set schedule time di aplikasi:
   - Base Time: +1 hour
   - Interval: +30 min

5. Process → Done!
```

### Workflow Advanced (Custom Time per Broadcast):
```
1. Tambahkan kolom scheduledStartDate & scheduledStartTime di Excel

2. Isi waktu spesifik untuk setiap broadcast

3. Load Excel di aplikasi

4. Schedule time di aplikasi akan di-ignore
   (pakai waktu dari Excel)

5. Process → Done!
```

## Contoh Kasus Penggunaan

### Kasus 1: Streaming Harian Jam yang Sama
```
Excel: 7 broadcasts (Mon-Sun) tanpa tanggal

Aplikasi:
- Base Time: Tomorrow 19:00
- Interval: +1 day

Result: 7 broadcasts dijadwalkan jam 19:00 setiap hari
```

### Kasus 2: Multiple Broadcasts per Hari
```
Excel: 10 broadcasts tanpa tanggal

Aplikasi:
- Base Time: Tomorrow 10:00
- Interval: +2 hours

Result: 10 broadcasts dijadwalkan setiap 2 jam (10:00, 12:00, 14:00, ...)
```

### Kasus 3: All Same Time
```
Excel: 5 broadcasts tanpa tanggal

Aplikasi:
- Base Time: Tomorrow 20:00
- Interval: 0 min (all same)

Result: 5 broadcasts dijadwalkan di waktu yang sama
```

## Migration dari Excel Lama

Jika punya Excel lama dengan kolom tanggal:

### Opsi 1: Tetap Pakai (No Change)
- Excel lama masih 100% compatible
- Aplikasi akan gunakan waktu dari Excel

### Opsi 2: Hapus Kolom Tanggal
1. Buka Excel lama
2. Delete kolom `scheduledStartDate` dan `scheduledStartTime`
3. Save
4. Load di aplikasi dan set schedule time di app

### Opsi 3: Gunakan Sample Baru
1. Copy data dari Excel lama ke `sample_broadcasts_with_monetization.xlsx`
2. Cukup copy kolom: title, description, tags, categoryId, privacyStatus
3. Load di aplikasi

## Notes

- Kolom tanggal/waktu **sekarang optional**, tidak wajib
- Aplikasi sudah handle jika kolom tanggal tidak ada
- Setting waktu di aplikasi lebih praktis untuk batch scheduling
- Excel baru lebih fokus ke content (title, desc, tags)
- Monetization setting bisa via Excel atau global checkbox di app
