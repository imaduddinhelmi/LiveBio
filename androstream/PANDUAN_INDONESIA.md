# AndroStream - Panduan Bahasa Indonesia

## 📱 Aplikasi YouTube Live & Video Automation untuk Android

Versi mobile dari aplikasi YouTube automation yang dibangun dengan framework Kivy.

## ✨ Fitur Utama

### Yang Sudah Tersedia:
- 🔐 **Autentikasi YouTube**
  - Login dengan akun Google
  - Simpan beberapa akun sekaligus
  - Ganti akun dengan mudah
  
- ⚡ **Buat Broadcast Cepat**
  - Buat live streaming dari HP
  - Jadwalkan siaran
  - Atur privasi, kategori, dan tag
  - Aktifkan/nonaktifkan monetisasi
  - Kontrol DVR

### Yang Akan Datang:
- 📊 Import data dari Excel
- 📹 Upload video dari galeri
- 📋 Lihat dan kelola siaran mendatang
- 🔄 Penjadwalan otomatis
- 📸 Upload thumbnail dari kamera/galeri

## 🛠️ Cara Build APK

### Persiapan (Linux/WSL):

1. **Install dependencies sistem:**
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   ```

2. **Install Buildozer:**
   ```bash
   pip3 install buildozer cython
   ```

3. **Masuk ke folder androstream:**
   ```bash
   cd androstream
   ```

4. **Build APK (pertama kali, butuh 30-60 menit):**
   ```bash
   buildozer android debug
   ```

5. **File APK ada di folder `bin/`**
   ```bash
   ls bin/*.apk
   ```

### Cara Build di Windows:

1. **Install WSL2 Ubuntu:**
   - Buka PowerShell as Administrator
   - Jalankan: `wsl --install -d Ubuntu`
   - Restart komputer
   - Buka Ubuntu dari Start Menu

2. **Di dalam WSL, ikuti langkah Linux di atas**

3. **Copy APK ke Windows:**
   ```bash
   cp bin/*.apk /mnt/c/Users/NamaAnda/Desktop/
   ```

## 📲 Cara Install di HP

### Cara 1: Via USB
```bash
# Aktifkan USB Debugging di HP
# Sambungkan HP ke komputer
adb install bin/AndroStream-1.0.0-debug.apk
```

### Cara 2: Manual
1. Copy file APK dari folder `bin/` ke HP (via Bluetooth, WhatsApp, dll)
2. Buka file APK di HP
3. Izinkan "Install dari sumber tidak dikenal"
4. Klik Install

## 🚀 Cara Pakai

### 1. Setup API YouTube:

1. Buka [Google Cloud Console](https://console.cloud.google.com/)
2. Buat project baru
3. Aktifkan **YouTube Data API v3**
4. Buat **OAuth 2.0 Client ID**:
   - Tipe: Android atau Desktop app
   - Download JSON
   - Rename jadi `client_secret.json`
5. Transfer file ke HP (via USB, Google Drive, WhatsApp, dll)

### 2. Login Pertama Kali:

1. Buka app AndroStream
2. Tap "🔐 Authentication"
3. Tap "Add Account"
4. Pilih file `client_secret.json`
5. Browser akan terbuka → Login dengan Google
6. Berikan izin akses YouTube
7. Kembali ke app

### 3. Buat Broadcast:

1. Dari menu utama, pilih "⚡ Quick Create"
2. Isi:
   - **Title**: Judul siaran
   - **Description**: Deskripsi
   - **Tags**: Tag dipisah koma, contoh: `gaming,live,indonesia`
   - **Category**: Pilih kategori (Gaming, People & Blogs, dll)
   - **Privacy**: Public, Unlisted, atau Private
   - **Schedule**: Kapan siarannya (Now, +30 minutes, dll)
3. Centang opsi:
   - **Made for Kids**: Khusus anak-anak (biasanya tidak)
   - **Enable DVR**: Viewers bisa rewind (rekomen aktif)
   - **Enable Monetization**: Iklan (harus punya YPP)
4. Tap **"✨ Create Broadcast"**
5. Tunggu proses selesai
6. Broadcast ID akan muncul → Salin untuk digunakan di OBS/streaming software

### 4. Ganti Akun:

1. Tap "🔐 Authentication"
2. Pilih akun dari dropdown
3. Tap "Switch"

## 🔧 Troubleshooting

### App crash saat dibuka:
- Pastikan HP Android 5.0+ (API 21)
- Coba uninstall dan install ulang
- Cek log: `adb logcat | grep python`

### OAuth tidak berfungsi:
- Pastikan file `client_secret.json` benar
- Cek apakah YouTube Data API v3 sudah diaktifkan
- Coba buat credentials baru di Google Cloud Console

### File chooser tidak muncul:
- Beri izin Storage di Settings → Apps → AndroStream → Permissions
- Coba letakkan `client_secret.json` di Downloads atau Documents

### Build gagal:
- Pastikan semua dependencies terinstall
- Coba clean build: `buildozer android clean`
- Cek versi Java: `java -version` (harus 11 atau 17)

## 📁 Struktur File

```
androstream/
├── main.py                    # Aplikasi utama Kivy
├── auth.py                    # Handler OAuth YouTube
├── youtube_service.py         # API YouTube wrapper
├── excel_parser.py            # Parser data Excel
├── config.py                  # Konfigurasi app
├── multi_account_manager.py   # Manajemen multi-akun
├── buildozer.spec             # Konfigurasi build
├── requirements.txt           # Dependencies Python
├── README.md                  # Dokumentasi (English)
├── PANDUAN_INDONESIA.md       # Panduan ini
└── .gitignore                 # File yang diabaikan git
```

## 💡 Tips

1. **Simpan client_secret.json di tempat aman** - Jangan dibagikan ke orang lain
2. **Test di desktop dulu** sebelum build APK (jalankan `python main.py`)
3. **Build pertama lama** - Bisa 30-60 menit, tapi build berikutnya cepat
4. **Gunakan WiFi yang stabil** - Build memerlukan download banyak file
5. **Backup APK** yang sudah jadi di folder `bin/`

## 🆘 Butuh Bantuan?

- Baca dokumentasi lengkap di folder parent (AutoLiveBio)
- Cek file QUICKSTART.md, QUICK_GUIDE.txt untuk panduan fitur
- Report bug via GitHub Issues

## 📝 Catatan Penting

### Izin yang Dibutuhkan:
- **INTERNET** - Akses YouTube API
- **WRITE_EXTERNAL_STORAGE** - Simpan credentials dan file
- **READ_EXTERNAL_STORAGE** - Baca client_secret.json
- **WAKE_LOCK** - Jaga layar tetap nyala saat proses

### Batasan:
- OAuth butuh browser external (otomatis terbuka)
- File Excel besar perlu waktu loading
- Upload video dibatasi storage HP dan internet
- Beberapa fitur butuh Android 5.0+ (API 21)

## 🎯 Roadmap

### v1.1.0 (Segera):
- [ ] Batch import dari Excel
- [ ] Upload video dari galeri
- [ ] View upcoming broadcasts
- [ ] Material Design UI improvements

### v1.2.0 (Future):
- [ ] Thumbnail upload dari camera/gallery
- [ ] Automatic scheduling
- [ ] Push notifications
- [ ] Widget support
- [ ] Dark mode

## 👨‍💻 Untuk Developer

### Test di Desktop:
```bash
pip install -r requirements.txt
python main.py
```

### Debug APK di HP:
```bash
# Lihat log real-time
adb logcat | grep python

# Atau simpan ke file
adb logcat > debug.log
```

### Rebuild setelah edit code:
```bash
buildozer android debug
buildozer android deploy run
```

## 📜 Lisensi

Sama dengan project utama (AutoLiveBio)

---

**Dibuat dengan ❤️ menggunakan Kivy**

**Selamat streaming! 🎥🔴**
