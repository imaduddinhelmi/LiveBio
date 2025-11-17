# Panduan Pengaturan Konten

## Overview

Aplikasi ini mendukung pengaturan konten yang sesuai dengan kebijakan YouTube, termasuk:
1. **Konten untuk Anak-anak** (`madeForKids`)
2. **Konten yang Dimodifikasi/AI** (`containsSyntheticMedia`)
3. **Kategori Video** (`categoryId`)

---

## 1. Made for Kids (Konten untuk Anak-anak)

### Apa itu?
Deklarasi apakah konten Anda dibuat khusus untuk anak-anak (di bawah 13 tahun).

### Peraturan YouTube:
- **WAJIB** dideklarasikan untuk semua video
- Jika konten untuk anak-anak, beberapa fitur akan dinonaktifkan:
  - Komentar
  - Notifikasi
  - Personalized ads
  - Community posts

### Cara Menggunakan:

**Excel Column**: `madeForKids`

**Values**:
- `TRUE` = Konten DIBUAT untuk anak-anak
- `FALSE` = Konten TIDAK untuk anak-anak (default)

**Contoh Excel**:
```
| title                  | madeForKids | ...
|------------------------|-------------|
| Kartun Anak-Anak       | TRUE        |
| Tutorial Dewasa        | FALSE       |
| Gaming - Horror        | FALSE       |
```

### Kapan set TRUE?
- Video dirancang khusus untuk anak-anak
- Target audience: anak di bawah 13 tahun
- Konten ramah anak, edukatif untuk anak

### Kapan set FALSE?
- Video untuk remaja/dewasa
- Konten general audience
- Gaming dengan konten mature
- Tutorial, review, vlog

---

## 2. Contains Synthetic Media (Konten Dimodifikasi/AI)

### Apa itu?
Deklarasi jika video Anda mengandung konten yang dibuat atau dimodifikasi menggunakan AI atau teknologi synthetic media.

### Peraturan YouTube (Update 2024):
YouTube **MEWAJIBKAN** creator mendeklarasikan jika konten:
- Dibuat dengan AI (AI-generated)
- Dimodifikasi dengan AI (deepfake, voice clone, dll)
- Menggunakan synthetic media untuk memanipulasi realitas

### Cara Menggunakan:

**Excel Column**: `containsSyntheticMedia`

**Values**:
- `TRUE` = Video mengandung konten AI/synthetic
- `FALSE` = Video tidak mengandung konten AI/synthetic (default)

**Contoh Excel**:
```
| title                     | containsSyntheticMedia | ...
|---------------------------|------------------------|
| AI Voice Review           | TRUE                   |
| Deepfake Demo             | TRUE                   |
| Real Gaming Footage       | FALSE                  |
| Unedited Vlog             | FALSE                  |
```

### Kapan set TRUE?
✅ **HARUS TRUE jika:**
- Menggunakan AI voice generator (ElevenLabs, dll)
- Deepfake atau face swap
- AI-generated video/image (Midjourney, DALL-E, dll)
- Voice cloning
- Memodifikasi seseorang untuk terlihat berbeda
- AI mengubah latar belakang secara realistis

❌ **TIDAK PERLU TRUE jika:**
- Filter/efek biasa (beauty filter, color grading)
- Background blur standar
- Text overlay, graphics
- Editing normal (cutting, transitions)
- Musik AI (hanya audio background)

### Konsekuensi Tidak Declare:
- Video bisa di-takedown oleh YouTube
- Strike pada channel
- Monetization bisa dinonaktifkan
- Reputasi channel menurun

---

## 3. Category ID (Kategori Video)

### Apa itu?
Kategori yang menentukan jenis konten video Anda di YouTube.

### Cara Menggunakan:

**Excel Column**: `categoryId`

**Required**: ✅ WAJIB diisi

### Daftar Category ID YouTube:

| ID  | Kategori               | Deskripsi |
|-----|------------------------|-----------|
| 1   | Film & Animation       | Film, animasi, kartun |
| 2   | Autos & Vehicles       | Mobil, motor, otomotif |
| 10  | Music                  | Musik, lagu, performance |
| 15  | Pets & Animals         | Hewan peliharaan, satwa |
| 17  | Sports                 | Olahraga, fitness |
| 19  | Travel & Events        | Travel vlog, event coverage |
| 20  | Gaming                 | Gaming, walkthrough, esports |
| 22  | People & Blogs         | Vlog, lifestyle, personal blog |
| 23  | Comedy                 | Komedi, sketch, parodi |
| 24  | Entertainment          | Hiburan umum |
| 25  | News & Politics        | Berita, politik, current affairs |
| 26  | Howto & Style          | Tutorial, fashion, beauty |
| 27  | Education              | Edukatif, pembelajaran |
| 28  | Science & Technology   | Tech review, sains, programming |
| 29  | Nonprofits & Activism  | NGO, activism, charity |

**Contoh Excel**:
```
| title                     | categoryId | ...
|---------------------------|------------|
| Gaming Live - Valorant   | 20         |
| Python Tutorial           | 27         |
| Product Review Tech       | 28         |
| Daily Vlog                | 22         |
| Music Cover               | 10         |
```

### Tips Memilih Kategori:
1. **Pilih kategori yang PALING sesuai** dengan konten utama
2. **Gaming** (20): Untuk semua jenis gaming content
3. **Education** (27): Tutorial, how-to, pembelajaran
4. **People & Blogs** (22): Vlog, personal content
5. **Science & Technology** (28): Tech review, programming, gadget

---

## Contoh Lengkap Excel

```excel
| title                          | categoryId | madeForKids | containsSyntheticMedia | ...
|--------------------------------|------------|-------------|------------------------|
| Minecraft Live - Kids Server   | 20         | TRUE        | FALSE                  |
| AI Voice Product Review        | 28         | FALSE       | TRUE                   |
| Real Vlog - Daily Life         | 22         | FALSE       | FALSE                  |
| Deepfake Technology Explained  | 27         | FALSE       | TRUE                   |
| Gaming Horror - Resident Evil  | 20         | FALSE       | FALSE                  |
| Kids Learning ABCs             | 27         | TRUE        | FALSE                  |
```

---

## Best Practices

### 1. Selalu Jujur dalam Deklarasi
- YouTube menggunakan AI untuk deteksi
- Pelanggaran bisa berakibat fatal untuk channel
- Transparansi = kepercayaan audience

### 2. Review Sebelum Upload
- Double-check setiap kolom di Excel
- Pastikan kategori sesuai
- Verifikasi deklarasi AI/Kids content

### 3. Update Knowledge
- Kebijakan YouTube sering berubah
- Follow YouTube Creator Insider
- Baca YouTube Help Center: https://support.google.com/youtube

### 4. Konsistensi Channel
- Jika channel Anda khusus kids: semua video `madeForKids = TRUE`
- Jika gaming dewasa: `madeForKids = FALSE` konsisten
- Brand voice yang jelas

---

## FAQ

**Q: Apakah musik AI perlu declare synthetic media?**
A: Jika hanya background music AI, tidak wajib. Tapi jika musik adalah konten utama, sebaiknya declare.

**Q: Filter Instagram/TikTok apakah synthetic media?**
A: Tidak, filter standar (beauty, AR mask) tidak perlu declare.

**Q: Video untuk remaja, apakah madeForKids?**
A: Tidak. madeForKids hanya untuk anak di bawah 13 tahun.

**Q: Bagaimana jika lupa declare AI content?**
A: Edit broadcast di YouTube Studio secepatnya untuk update declaration.

**Q: Apakah bisa ganti kategori setelah live?**
A: Ya, bisa edit di YouTube Studio → Video details → Category.

---

## Resources

- YouTube Creator Academy: https://creatoracademy.youtube.com
- COPPA Guidelines: https://www.ftc.gov/coppa
- YouTube Synthetic Media Policy: https://support.google.com/youtube/answer/13655767
- Category List: https://developers.google.com/youtube/v3/docs/videoCategories/list
