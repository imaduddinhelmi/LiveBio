# 📚 Multi-Account Guide

## Fitur Multi-Account yang Telah Diperbaiki

Sistem multi-account sekarang sudah berfungsi dengan baik dan mencakup:

### ✅ Fitur Yang Sudah Diperbaiki:

1. **Auto-Load on Startup**
   - Akun aktif otomatis dimuat saat aplikasi dibuka
   - Delay 1 detik untuk memastikan GUI siap
   - Error handling yang lebih baik

2. **Switch Account**
   - Switch instant tanpa perlu login ulang
   - Token otomatis di-refresh jika expired
   - UI feedback yang lebih jelas (tombol "Switching...")

3. **Account Management**
   - Simpan unlimited accounts
   - Setiap akun punya token terpisah
   - Data tersimpan permanen

4. **Better Error Handling**
   - Detailed error messages di Logs tab
   - Traceback untuk debugging
   - Fallback mechanism jika auto-load gagal

---

## 🚀 Cara Menggunakan

### 1. **Menambah Akun Pertama**

1. Buka tab **Auth**
2. Klik **Select client_secret.json** dan pilih file credentials
3. Klik **🔑 Add New Account**
4. Masukkan nama akun (contoh: "Channel Pribadi")
5. Login dengan Google di browser
6. Akun otomatis tersimpan!

### 2. **Menambah Akun Kedua/Ketiga**

1. Klik **🔑 Add New Account** lagi
2. Masukkan nama berbeda (contoh: "Channel Kerja")
3. Login dengan akun Google berbeda
4. Selesai! Akun tersimpan.

### 3. **Beralih Antar Akun**

1. Di bagian **📚 Saved Accounts**, pilih akun dari dropdown
2. Klik **✓ Use This Account**
3. Tunggu beberapa detik
4. Akun aktif berubah tanpa login ulang!

### 4. **Menghapus Akun**

1. Pilih akun yang ingin dihapus dari dropdown
2. Klik **🗑 Remove**
3. Konfirmasi penghapusan
4. Token dan data akun terhapus

### 5. **Logout**

- **Logout** sekarang hanya end session
- Akun tetap tersimpan
- Bisa switch kembali kapan saja tanpa login ulang

---

## 📂 File Penyimpanan

Semua data tersimpan di: `C:\Users\[username]\.ytlive\`

```
.ytlive/
├── accounts.json           # Metadata semua akun
├── tokens/
│   ├── token_acc_xxx.pickle  # Token akun 1
│   ├── token_acc_yyy.pickle  # Token akun 2
│   └── token_acc_zzz.pickle  # Token akun 3
└── settings.json           # Pengaturan tema
```

---

## 🔧 Troubleshooting

### Akun tidak auto-load saat startup?
- Periksa tab **Logs** untuk error messages
- Coba switch manual ke akun tersebut
- Jika gagal, hapus dan tambahkan ulang

### Switch account gagal?
- Token mungkin expired dan tidak bisa di-refresh
- Hapus akun tersebut
- Tambahkan ulang dengan login baru

### Channels tidak muncul?
- Pastikan akun Google memiliki YouTube channel
- Buat channel di youtube.com jika belum punya
- Re-authenticate jika perlu

### Ingin reset semua?
1. Tutup aplikasi
2. Hapus folder `C:\Users\[username]\.ytlive\`
3. Buka aplikasi lagi
4. Tambahkan akun dari awal

---

## 💡 Tips

1. **Nama Akun**: Gunakan nama yang jelas seperti "Pribadi" atau "Kerja"
2. **Testing**: Test switch account dengan 2-3 akun dulu
3. **Backup**: Backup folder `.ytlive` untuk cadangan token
4. **Logs**: Selalu check tab Logs untuk troubleshooting

---

## 🐛 Debug Script

Jika ada masalah, jalankan debug script:

```bash
python test_multi_account.py
```

Script ini akan menampilkan:
- Jumlah akun tersimpan
- Detail setiap akun
- Status token file
- Akun aktif

---

## 📝 Changelog Perbaikan

### Versi Saat Ini:
- ✅ Auto-load dengan delay 1 detik
- ✅ Better error handling dengan traceback
- ✅ UI update di main thread (thread-safe)
- ✅ Switch account lebih robust
- ✅ Better email/identifier extraction
- ✅ Detailed logging untuk debugging

### Sebelumnya:
- ❌ Auto-load terlalu cepat, GUI belum siap
- ❌ Error tidak ter-handle dengan baik
- ❌ UI update dari background thread (race condition)
- ❌ Email tidak terdeteksi dengan benar

---

## ✨ Sekarang Anda Bisa:

✓ Simpan banyak akun tanpa batas
✓ Switch instant tanpa login ulang
✓ Auto-load akun aktif saat startup
✓ Manage multiple YouTube channels dengan mudah
✓ Token otomatis refresh jika expired

**Enjoy multi-account management! 🎉**
