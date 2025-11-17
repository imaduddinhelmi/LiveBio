# 🚀 Quick Build Options - Pilih Metode Anda!

## 2 Metode Build APK Android

---

## 🎯 Pilih Metode yang Cocok untuk Anda:

| Kriteria | GitHub Actions ⭐ | WSL Build |
|----------|------------------|-----------|
| **Setup Time** | 5 menit | 30-60 menit |
| **First Build** | 15-20 menit | 30-60 menit |
| **Subsequent Build** | 8-15 menit | 2-5 menit |
| **Internet Required** | Ya (upload & download) | Ya (first time only) |
| **Local Storage** | Tidak perlu | Perlu 10GB+ |
| **Auto Build** | ✅ Otomatis setiap push | ❌ Manual |
| **Best For** | Team, CI/CD, Beginners | Solo dev, Frequent builds |
| **Cost** | Gratis (public repo) | Gratis |

---

## ⚡ OPSI 1: GitHub Actions (RECOMMENDED untuk pemula)

### ✅ Keuntungan:
- Setup cepat (5 menit)
- Tidak perlu install WSL
- Build otomatis di cloud
- Gratis untuk public repo
- Download APK dari web

### 📝 Langkah Singkat:

```bash
# 1. Buat repo di GitHub
# 2. Run setup script
setup_github.bat          # Windows
# atau
./setup_github.sh         # Linux/Mac

# 3. Push ke GitHub (sudah auto di script)

# 4. Wait for build (~15-20 min)

# 5. Download APK dari Actions → Artifacts
```

### 📚 Dokumentasi Lengkap:
**Baca:** `GITHUB_ACTIONS_SETUP.md`

---

## 💻 OPSI 2: WSL Build (untuk developer)

### ✅ Keuntungan:
- Build lebih cepat setelah setup
- Tidak perlu upload/download
- Offline after first setup
- Full control

### 📝 Langkah Singkat:

```powershell
# 1. Install WSL
wsl --install -d Ubuntu

# 2. Restart komputer

# 3. Setup di WSL
# (Copy-paste dari INSTALL_WSL_STEP_BY_STEP.md)

# 4. Build APK
cd ~/projects/androstream
buildozer android debug

# 5. APK ada di bin/
```

### 📚 Dokumentasi Lengkap:
**Baca:** `androstream/INSTALL_WSL_STEP_BY_STEP.md`

---

## 🎨 Comparison Matrix

### GitHub Actions:
```
Setup: ⭐⭐⭐⭐⭐ (Very Easy)
Speed: ⭐⭐⭐⭐ (Fast enough)
Automation: ⭐⭐⭐⭐⭐ (Automatic)
Cost: ⭐⭐⭐⭐⭐ (Free)
Team Friendly: ⭐⭐⭐⭐⭐ (Yes!)
```

### WSL Build:
```
Setup: ⭐⭐ (Complex)
Speed: ⭐⭐⭐⭐⭐ (Very Fast after setup)
Automation: ⭐⭐ (Manual)
Cost: ⭐⭐⭐⭐⭐ (Free)
Team Friendly: ⭐⭐⭐ (Needs local setup)
```

---

## 🤔 Rekomendasi Berdasarkan Use Case:

### Saya pemula, mau coba build pertama kali
➜ **PILIH: GitHub Actions**
- Setup paling mudah
- Tidak perlu technical knowledge
- Dokumentasi: `GITHUB_ACTIONS_SETUP.md`

### Saya developer, sering update code
➜ **PILIH: WSL Build**
- Build lebih cepat (2-5 min vs 10-15 min)
- Tidak perlu upload/download
- Dokumentasi: `androstream/INSTALL_WSL_STEP_BY_STEP.md`

### Saya kerja dalam team
➜ **PILIH: GitHub Actions**
- Semua orang bisa download APK
- Automatic CI/CD
- Version control terintegrasi
- Dokumentasi: `GITHUB_ACTIONS_SETUP.md`

### Saya mau publish ke Play Store
➜ **PILIH: Keduanya!**
- GitHub Actions: Auto-build every release
- WSL: Quick testing before release
- Setup signing di kedua metode

### Saya tidak punya internet stabil
➜ **PILIH: WSL Build**
- Setelah setup pertama, bisa offline
- Dokumentasi: `androstream/INSTALL_WSL_STEP_BY_STEP.md`

---

## 📖 Quick Links ke Dokumentasi

### GitHub Actions (Opsi 1):
1. **Setup Guide**: `GITHUB_ACTIONS_SETUP.md` ⭐ START HERE
2. **Workflows Detail**: `.github/workflows/README.md`
3. **Troubleshooting**: `GITHUB_ACTIONS_SETUP.md#troubleshooting`

### WSL Build (Opsi 2):
1. **Step-by-Step**: `androstream/INSTALL_WSL_STEP_BY_STEP.md` ⭐ START HERE
2. **Build Instructions**: `androstream/BUILD_INSTRUCTIONS_WINDOWS.md`
3. **Troubleshooting**: `androstream/BUILD_INSTRUCTIONS_WINDOWS.md#troubleshooting`

### Untuk Keduanya:
- **Android App Docs**: `androstream/README.md`
- **Panduan Indonesia**: `androstream/PANDUAN_INDONESIA.md`
- **Quick Reference**: `androstream/QUICK_START.txt`

---

## ⚡ Super Quick Start

### Mau yang PALING CEPAT? 

**GitHub Actions (5 menit setup!):**

```bash
# Windows:
setup_github.bat

# Linux/Mac:
chmod +x setup_github.sh && ./setup_github.sh
```

**Ikuti prompt, tunggu 15-20 menit, download APK. DONE!**

---

## 🆘 Butuh Bantuan?

### GitHub Actions Issues:
- Baca: `GITHUB_ACTIONS_SETUP.md#troubleshooting`
- Check: GitHub Actions logs
- Ask: GitHub Issues

### WSL Build Issues:
- Baca: `androstream/INSTALL_WSL_STEP_BY_STEP.md#troubleshooting`
- Check: WSL terminal output
- Ask: GitHub Issues

---

## 🎯 Final Recommendation

**Untuk 90% user: Pakai GitHub Actions!**

Alasan:
- ✅ Setup 5 menit
- ✅ Tidak perlu technical knowledge
- ✅ Gratis
- ✅ Automatic
- ✅ Team friendly

**Pakai WSL hanya jika:**
- Anda developer experienced
- Build sangat sering (>10x per hari)
- Butuh speed maksimal

---

## 📝 Checklist

Pilih metode Anda dan centang:

### GitHub Actions:
- [ ] Baca `GITHUB_ACTIONS_SETUP.md`
- [ ] Buat GitHub repository
- [ ] Run `setup_github.bat` atau `.sh`
- [ ] Wait for build
- [ ] Download APK
- [ ] ✅ DONE!

### WSL Build:
- [ ] Baca `androstream/INSTALL_WSL_STEP_BY_STEP.md`
- [ ] Install WSL2
- [ ] Setup Ubuntu
- [ ] Install dependencies
- [ ] Build APK
- [ ] ✅ DONE!

---

**Happy Building! 🚀**

**Start with the easiest: GitHub Actions! ⭐**
