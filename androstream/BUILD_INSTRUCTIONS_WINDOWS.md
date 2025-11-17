# 🪟 Panduan Build APK di Windows

## Metode 1: Menggunakan WSL2 (Recommended)

### Step 1: Install WSL2

**Buka PowerShell as Administrator**, lalu jalankan:

```powershell
wsl --install -d Ubuntu
```

Setelah selesai, **restart komputer**.

### Step 2: Setup WSL Ubuntu

Setelah restart, buka **Ubuntu** dari Start Menu:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y git zip unzip openjdk-17-jdk python3 python3-pip \
    autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev \
    build-essential libffi-dev libssl-dev python3-dev

# Install Buildozer
pip3 install --user buildozer cython

# Add to PATH (tambahkan ke ~/.bashrc agar permanen)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Verify installation
buildozer --version
```

### Step 3: Copy Project ke WSL

**Di PowerShell/CMD Windows:**

```powershell
# Copy folder androstream ke WSL
wsl

# Di dalam WSL:
cd ~
mkdir -p projects
cp -r /mnt/d/A-YT/YT/AutoLiveBio/androstream ~/projects/
cd ~/projects/androstream
```

### Step 4: Build APK

```bash
cd ~/projects/androstream

# Build APK (pertama kali: 30-60 menit)
buildozer android debug

# Progress akan ditampilkan di terminal
# Tunggu sampai selesai...

# APK akan ada di folder bin/
ls -lh bin/
```

### Step 5: Copy APK ke Windows

```bash
# Copy APK ke Desktop Windows
cp bin/AndroStream-*-debug.apk /mnt/c/Users/$(cmd.exe /c "echo %USERNAME%" | tr -d '\r')/Desktop/

echo "APK copied to Desktop!"
```

---

## Metode 2: Menggunakan GitHub Actions (Cloud Build)

### Keuntungan:
- ✅ Build otomatis di cloud (gratis)
- ✅ Tidak perlu install WSL
- ✅ Bisa download APK langsung

### Langkah-langkah:

1. **Push project ke GitHub**

2. **Buat file `.github/workflows/android-build.yml`** (sudah disediakan)

3. **Push ke GitHub:**
   ```bash
   git add .
   git commit -m "Add Android version"
   git push
   ```

4. **GitHub Actions akan otomatis build APK**

5. **Download APK** dari GitHub Actions Artifacts

Lihat file `GITHUB_ACTIONS_BUILD.md` untuk detailnya.

---

## Metode 3: Cloud Build Services

### Google Colab (Free)

Buka [Google Colab](https://colab.research.google.com/) dan jalankan:

```python
# Install dependencies
!apt-get update
!apt-get install -y openjdk-17-jdk zip unzip
!pip install buildozer cython

# Clone/Upload project
# ... (upload androstream folder)

# Build APK
!cd androstream && buildozer android debug

# Download APK dari Colab Files
```

---

## Troubleshooting

### WSL: "Cannot connect to internet"
```bash
# Fix DNS
sudo rm /etc/resolv.conf
sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
```

### Buildozer: "SDK License not accepted"
```bash
# Accept licenses manually
cd ~/.buildozer/android/platform/android-sdk/tools/bin
./sdkmanager --licenses
# Press 'y' untuk accept all
```

### Build error: "Java not found"
```bash
# Install Java 17
sudo apt install openjdk-17-jdk

# Set JAVA_HOME
echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
source ~/.bashrc
```

### Build error: "NDK not found"
```bash
# Buildozer akan auto-download NDK
# Pastikan internet stabil
# Jika gagal, hapus dan rebuild:
buildozer android clean
buildozer android debug
```

---

## FAQ

**Q: Berapa lama waktu build?**  
A: Pertama kali: 30-60 menit. Selanjutnya: 2-5 menit.

**Q: Berapa besar file yang di-download?**  
A: ~4-5 GB (SDK, NDK, dependencies)

**Q: Bisa build di Windows native?**  
A: Tidak bisa. Harus pakai WSL, Linux, atau Mac.

**Q: Build gagal di tengah jalan?**  
A: Biasanya karena internet putus. Jalankan ulang command yang sama, buildozer akan resume.

**Q: APK tidak bisa install di HP?**  
A: Aktifkan "Install from unknown sources" di Settings HP.

---

## Quick Command Reference

```bash
# Di WSL Ubuntu

# Build debug APK
buildozer android debug

# Build release APK
buildozer android release

# Clean build
buildozer android clean

# Deploy ke device (USB debugging)
buildozer android deploy run

# View logs
buildozer android logcat

# Check buildozer version
buildozer --version
```

---

## Next Steps

1. ✅ Install WSL2
2. ✅ Setup Ubuntu environment
3. ✅ Copy project ke WSL
4. ✅ Run `buildozer android debug`
5. ✅ Wait 30-60 minutes
6. ✅ Get APK from `bin/` folder
7. ✅ Install on Android device
8. 🎉 Done!

---

**Need Help?** Check:
- `README.md` - Full documentation
- `PANDUAN_INDONESIA.md` - Panduan lengkap
- `QUICK_START.txt` - Quick reference

**Happy Building! 🚀**
