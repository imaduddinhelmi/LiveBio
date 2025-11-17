# 📝 Panduan Install WSL & Build APK - Step by Step

## ✅ Checklist Lengkap

Ikuti langkah-langkah ini satu per satu. Setiap step ada perintahnya.

---

## PART 1: INSTALL WSL2

### ⚡ Step 1: Buka PowerShell as Administrator

1. Tekan `Windows + X`
2. Pilih **"Windows PowerShell (Admin)"** atau **"Terminal (Admin)"**
3. Klik **Yes** pada UAC prompt

### ⚡ Step 2: Install WSL2

Copy-paste command ini di PowerShell:

```powershell
wsl --install -d Ubuntu
```

**Tunggu proses selesai** (5-15 menit tergantung internet)

Output yang benar:
```
Installing: Virtual Machine Platform
Installing: Windows Subsystem for Linux
Installing: Ubuntu
The requested operation is successful. Changes will not be effective until the system is rebooted.
```

### ⚡ Step 3: Restart Komputer

```powershell
shutdown /r /t 0
```

Atau restart manual.

---

## PART 2: SETUP UBUNTU

### ⚡ Step 4: Buka Ubuntu

Setelah restart:
1. Tekan `Windows + S`
2. Ketik **"Ubuntu"**
3. Klik **Ubuntu** app

**Pertama kali akan setup** (5-10 menit):
```
Installing, this may take a few minutes...
```

### ⚡ Step 5: Buat User Ubuntu

Setelah selesai, akan minta username dan password:

```
Enter new UNIX username: [ketik username Anda, misal: user]
New password: [ketik password]
Retype new password: [ketik lagi]
```

**✅ Jika berhasil, akan muncul:**
```
user@DESKTOP:~$
```

### ⚡ Step 6: Update System

Copy-paste command ini di Ubuntu terminal:

```bash
sudo apt update && sudo apt upgrade -y
```

Masukkan password Ubuntu Anda.

Tunggu proses selesai (5-10 menit).

---

## PART 3: INSTALL DEPENDENCIES

### ⚡ Step 7: Install Java & Tools

```bash
sudo apt install -y openjdk-17-jdk git zip unzip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev build-essential python3 python3-pip
```

Tunggu selesai (10-15 menit).

**Verify Java:**
```bash
java -version
```

Should output:
```
openjdk version "17.0.x"
```

### ⚡ Step 8: Install Buildozer

```bash
pip3 install --user buildozer cython
```

Tunggu selesai (2-3 menit).

### ⚡ Step 9: Setup PATH

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Verify Buildozer:**
```bash
buildozer --version
```

Should output:
```
1.5.0
```

---

## PART 4: COPY PROJECT KE WSL

### ⚡ Step 10: Buat Folder Projects

```bash
cd ~
mkdir -p projects
```

### ⚡ Step 11: Copy Folder androstream

**Ganti `D:` dengan drive letter Anda jika berbeda!**

```bash
cp -r /mnt/d/A-YT/YT/AutoLiveBio/androstream ~/projects/
```

**Verify copied:**
```bash
ls ~/projects/androstream/
```

Should show:
```
auth.py  buildozer.spec  config.py  main.py  README.md  ...
```

### ⚡ Step 12: Masuk ke Folder

```bash
cd ~/projects/androstream
```

---

## PART 5: BUILD APK (THE LONG WAIT!)

### ⚡ Step 13: Build Debug APK

**⚠️ WARNING: Step ini butuh 30-60 MENIT untuk pertama kali!**

```bash
buildozer android debug
```

**Akan download ~4GB data:**
- Android SDK (~1.5GB)
- Android NDK (~1GB)
- Python packages (~500MB)
- Dependencies (~1GB)

**Progress yang akan muncul:**
```
# Check application requirements
# Check target
# Install platform
# Downloading Android SDK...
# Downloading Android NDK...
# Compiling python-for-android...
# Building application...
# Creating APK...
```

**☕ Sementara menunggu:**
- Jangan tutup terminal
- Pastikan internet stabil
- Jangan shutdown komputer
- Bisa minimize dan lakukan hal lain

### ⚡ Step 14: Check APK

Setelah selesai:

```bash
ls -lh bin/
```

Should show:
```
-rw-r--r-- 1 user user 25M Nov 17 17:00 AndroStream-1.0.0-debug.apk
```

**✅ APK BERHASIL DIBUAT!**

---

## PART 6: COPY APK KE WINDOWS

### ⚡ Step 15: Copy ke Desktop Windows

```bash
# Get Windows username
WINUSER=$(cmd.exe /c "echo %USERNAME%" 2>/dev/null | tr -d '\r')

# Copy APK to Desktop
cp bin/AndroStream-*.apk /mnt/c/Users/$WINUSER/Desktop/

echo "✅ APK copied to Desktop!"
```

### ⚡ Step 16: Verify di Windows

Buka **Desktop**, should see:
```
AndroStream-1.0.0-debug.apk
```

**🎉 SELESAI!**

---

## PART 7: INSTALL DI ANDROID

### ⚡ Step 17A: Install via USB (Recommended)

**Di Windows PowerShell:**

1. Enable **USB Debugging** di HP:
   - Settings → About Phone
   - Tap "Build Number" 7x
   - Back → Developer Options
   - Enable "USB Debugging"

2. Connect HP via USB

3. Run command:
```powershell
# Install ADB (if not installed)
winget install Google.PlatformTools

# Install APK
cd Desktop
adb install AndroStream-1.0.0-debug.apk
```

### ⚡ Step 17B: Install Manual

1. Copy APK ke HP via:
   - Google Drive
   - WhatsApp (send to yourself)
   - Bluetooth
   - USB transfer

2. Di HP:
   - Buka file APK
   - Tap "Install"
   - Allow "Install from unknown sources"
   - Done!

---

## TROUBLESHOOTING

### ❌ WSL: "Cannot connect to internet"

```bash
sudo rm /etc/resolv.conf
sudo bash -c 'echo "nameserver 8.8.8.8" > /etc/resolv.conf'
sudo bash -c 'echo "nameserver 8.8.4.4" >> /etc/resolv.conf'
```

### ❌ Buildozer: "Command not found"

```bash
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
```

### ❌ Build: "SDK license not accepted"

```bash
cd ~/.buildozer/android/platform/android-sdk/tools/bin
./sdkmanager --licenses
# Press 'y' untuk semua
```

### ❌ Build: "Java not found"

```bash
sudo apt install openjdk-17-jdk
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```

### ❌ Build failed, mau ulang dari awal:

```bash
buildozer android clean
buildozer android debug
```

### ❌ HP tidak terdeteksi ADB:

```bash
# List devices
adb devices

# If empty:
# 1. Check USB cable (use data cable, not charging-only)
# 2. Enable USB Debugging again
# 3. Allow "Trust this computer" on phone
# 4. Try different USB port
```

---

## NEXT BUILD (Faster!)

Setelah build pertama berhasil, build selanjutnya **CUMA 2-5 MENIT!**

```bash
cd ~/projects/androstream

# Edit code di main.py jika perlu

# Rebuild
buildozer android debug

# Copy ke Desktop
cp bin/AndroStream-*.apk /mnt/c/Users/$WINUSER/Desktop/
```

---

## USEFUL COMMANDS

```bash
# Masuk WSL dari Windows PowerShell
wsl

# Masuk ke folder project
cd ~/projects/androstream

# Build APK
buildozer android debug

# Clean build
buildozer android clean

# View logs
buildozer android logcat

# Deploy to device (if connected via USB)
buildozer android deploy run

# Exit WSL
exit
```

---

## 📊 Timeline Estimasi

| Step | Waktu |
|------|-------|
| Install WSL | 5-15 menit |
| Setup Ubuntu | 5-10 menit |
| Install Dependencies | 10-15 menit |
| Copy Project | 1 menit |
| **BUILD APK (First Time)** | **30-60 MENIT** |
| Copy to Windows | 1 menit |
| Install to Phone | 2-5 menit |
| **TOTAL** | **~50-90 menit** |

**Build selanjutnya:** 2-5 menit saja!

---

## 📝 Checklist Progress

Print dan centang saat selesai:

- [ ] Step 1: Buka PowerShell Admin
- [ ] Step 2: Install WSL2
- [ ] Step 3: Restart komputer
- [ ] Step 4: Buka Ubuntu
- [ ] Step 5: Buat user Ubuntu
- [ ] Step 6: Update system
- [ ] Step 7: Install Java & tools
- [ ] Step 8: Install Buildozer
- [ ] Step 9: Setup PATH
- [ ] Step 10: Buat folder projects
- [ ] Step 11: Copy androstream
- [ ] Step 12: Masuk ke folder
- [ ] Step 13: Build APK (☕ long wait!)
- [ ] Step 14: Check APK
- [ ] Step 15: Copy to Desktop
- [ ] Step 16: Verify di Windows
- [ ] Step 17: Install di HP
- [ ] ✅ DONE!

---

**Butuh bantuan? Re-read troubleshooting section atau check README.md**

**Good luck! 🚀**
