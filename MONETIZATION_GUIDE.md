# Monetization Settings Guide

## ⚠️ IMPORTANT: How YouTube Monetization Works

**YouTube Data API v3 TIDAK dapat mengaktifkan monetization secara langsung per video.**

Yang dilakukan aplikasi ini:
- ✅ Memastikan video **ELIGIBLE** untuk monetization (set `madeForKids: False`)
- ✅ Set video status yang correct untuk monetization
- ❌ TIDAK bisa toggle monetization ON/OFF langsung

**Monetization actual dikontrol di:**
1. **Channel default settings** (primary) - Set sekali di YouTube Studio
2. Per-video manual toggle di YouTube Studio (manual)

## ✅ SOLUSI: Set Channel Default Monetization

**Langkah penting untuk monetization otomatis:**

### 1. Set Default Monetization di Channel (SEKALI SAJA)
```
1. Buka YouTube Studio (studio.youtube.com)
2. Klik "Settings" (gear icon, kiri bawah)
3. Klik "Upload defaults"
4. Scroll ke bagian "Monetization"
5. Toggle monetization ke "On"
6. Klik "Save"
```

**Setelah ini, SEMUA video/broadcast baru akan otomatis ter-monetize! ✅**

### 2. Verify Channel Status
```
1. YouTube Studio → Monetization (menu kiri)
2. Pastikan status: "Your channel is eligible for monetization"
3. Pastikan tidak ada policy warning
```

### 3. Gunakan Aplikasi Ini
```
1. Create broadcast dengan aplikasi (centang "Enable Monetization")
2. Aplikasi set video sebagai eligible
3. Channel default monetization otomatis apply
4. Result: Video ter-monetize ✅
```

## Persyaratan

⚠️ **PENTING**: Fitur ini hanya berfungsi untuk channel yang sudah memenuhi syarat:

1. Channel sudah bergabung dengan **YouTube Partner Program (YPP)**
2. Channel sudah di-approve untuk monetisasi
3. Channel memiliki minimal:
   - 1,000 subscribers
   - 4,000 jam watch time (dalam 12 bulan terakhir) atau 10 juta views Shorts (dalam 90 hari)
   - Tidak ada pelanggaran Community Guidelines
4. **Channel default monetization sudah di-set ON** (lihat solusi di atas)

## Cara Menggunakan

### 1. Menggunakan Excel

Tambahkan kolom `enableMonetization` di file Excel Anda:

| title | description | tags | categoryId | privacyStatus | enableMonetization |
|-------|-------------|------|------------|---------------|-------------------|
| My Live Stream | Description here | gaming,live | 20 | public | TRUE |
| Another Stream | Another description | vlog,daily | 22 | unlisted | FALSE |

**Nilai yang dapat digunakan:**
- `TRUE`, `1`, `YES` → Mengaktifkan monetisasi
- `FALSE`, `0`, `NO` → Tidak mengaktifkan monetisasi
- Kosong → Default: FALSE (tidak aktif)

### 2. Menggunakan Quick Create

Di tab **Quick Create**:
1. Isi data broadcast seperti biasa
2. Centang checkbox **"Enable Monetization"**
3. Klik **"Create Broadcast"**

## Cara Kerja (Technical)

Ketika `enableMonetization` diset ke TRUE:
1. Aplikasi membuat broadcast seperti biasa
2. Setelah broadcast berhasil dibuat, aplikasi update video status:
   - Set `madeForKids: False` 
   - Set `selfDeclaredMadeForKids: False`
   - Preserve existing video settings
3. Video menjadi **ELIGIBLE** untuk monetization
4. **Channel default monetization settings akan otomatis apply**
5. Log akan menampilkan: 
   - `[INFO] Setting video as eligible for monetization (madeForKids=False)...`
   - `[INFO] Note: Actual monetization is controlled by channel YPP settings`
   - `[OK] Video set as eligible for monetization`

**Hasil Akhir:**
- Jika channel default monetization ON → Video otomatis monetized ✅
- Jika channel default monetization OFF → Harus enable manual di Studio

## Troubleshooting

### Error: "Failed to enable monetization"

**Penyebab umum:**
1. Channel belum di-approve untuk monetisasi
2. Video menggunakan setting "Made for Kids" (video anak-anak tidak bisa dimonetisasi)
3. API tidak memiliki permission yang cukup
4. Content ID claim atau copyright strike pada channel

**Solusi:**
1. Pastikan channel sudah join YPP dan di-approve
2. Jangan set `madeForKids` ke TRUE jika ingin monetisasi
3. Periksa status monetisasi channel di YouTube Studio
4. Cek apakah ada copyright strike atau warning di channel

### Monetisasi tidak aktif setelah broadcast dibuat ⚠️ (PALING SERING)

**Penyebab utama: Channel default monetization OFF**

**Solusi:**
1. **Set channel default monetization ON** (lihat section "SOLUSI" di atas)
2. Atau enable manual per video:
   ```
   YouTube Studio → Content → Video → Monetization tab → Toggle ON
   ```

**Langkah troubleshooting:**
1. Check channel default settings:
   - Studio → Settings → Upload defaults → Monetization
   - Pastikan toggle ON
2. Check video di Studio:
   - Content → Find video → Monetization tab
   - Check status dan toggle manual jika perlu
3. Tunggu 1-2 menit untuk sync
4. Pastikan tidak ada content ID claim yang memblokir
5. Pastikan video advertiser-friendly

## Best Practices

1. **SET CHANNEL DEFAULT MONETIZATION ON TERLEBIH DAHULU** ⭐ (Paling Penting!)
   - Studio → Settings → Upload defaults → Monetization → ON
   - Sekali setting ini, semua video otomatis monetized
2. **Test dulu**: Coba dengan 1 broadcast sebelum batch processing
3. **Check logs**: Selalu cek logs untuk memastikan tidak ada error
4. **Manual verification**: Cek YouTube Studio 1-2 menit setelah create
5. **Content guidelines**: Pastikan content Anda advertiser-friendly
6. **Verify channel YPP status**: Pastikan channel tidak ada policy warning

## Notes

- **API Limitation**: YouTube Data API v3 tidak bisa toggle monetization ON/OFF langsung
- **Aplikasi hanya set video sebagai ELIGIBLE** (madeForKids: False)
- **Actual monetization dikontrol di channel level** via Upload Defaults
- Setting ini tidak mempengaruhi ad format (mid-roll, pre-roll, dll) - itu diset di YouTube Studio
- Jika channel belum eligible untuk monetisasi, broadcast tetap dibuat tapi tidak ter-monetize
- Setting `madeForKids: TRUE` dan `enableMonetization: TRUE` akan konflik (kids content tidak bisa monetized)
- **Monetization status bisa berubah** jika ada copyright claim atau policy violation

## Lihat Juga

- [YouTube Partner Program Requirements](https://support.google.com/youtube/answer/72857)
- [Advertiser-Friendly Content Guidelines](https://support.google.com/youtube/answer/6162278)
- [Monetization Settings](https://support.google.com/youtube/answer/94522)
