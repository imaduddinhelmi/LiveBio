# 🪟 StreamPro - Windows Only Guide

## ✅ Cleanup Complete!

Semua file khusus Ubuntu/Linux sudah dihapus. Aplikasi ini sekarang **Windows only**.

---

## 📦 Cara Menggunakan di Windows

### 🎯 Option 1: Run Langsung (Development)

Untuk development atau testing:

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run aplikasi
python main.py
```

Aplikasi akan terbuka dengan GUI.

---

### 🎯 Option 2: Build Portable EXE

Untuk distribusi atau production, buat portable version:

```bash
# Double-click:
BUILD_PORTABLE.bat

# Atau via command line:
python build_portable.py
```

**Output:** Folder `streamPro Portable\` dengan executable yang tidak perlu install!

---

## 📁 File Structure (Windows Only)

### Core Application Files
```
AutoLiveBio/
├── main.py                    ← Entry point
├── gui.py                     ← Main GUI
├── auth.py                    ← YouTube authentication
├── batch_scheduler.py         ← Scheduler module
├── excel_parser.py            ← Excel parsing
├── video_excel_parser.py      ← Video Excel parser
├── youtube_service.py         ← YouTube API
├── video_uploader.py          ← Video upload
├── multi_account_manager.py   ← Account management
├── config.py                  ← Configuration
├── color_utils.py             ← UI colors
└── requirements.txt           ← Dependencies
```

### Build Files
```
├── BUILD_PORTABLE.bat         ← One-click build
├── build_portable.py          ← Build script
├── BUILD_GUIDE.md             ← Build documentation
├── CARA_BUILD_PORTABLE.txt    ← Indonesian build guide
├── BUILD_FILES_CHECKLIST.md   ← Build checklist
├── PORTABLE_SUMMARY.md        ← Portable overview
└── START_HERE_BUILD.txt       ← Quick build guide
```

### Documentation
```
├── README.md                  ← Main readme
├── QUICKSTART.md              ← Quick start
├── CARA_PAKAI_SCHEDULER.txt   ← Scheduler guide (ID)
├── SCHEDULER_GUIDE.md         ← Scheduler guide (EN)
├── SCHEDULER_QUICKSTART.md    ← Quick scheduler guide
├── FITUR_BARU_SCHEDULER.md    ← Scheduler features
├── UI_LAYOUT_GUIDE.txt        ← UI guide
├── LAYOUT_SCHEDULER.md        ← Scheduler layout
├── VIDEO_UPLOAD_GUIDE.md      ← Video upload guide
├── CARA_UPLOAD_VIDEO.md       ← Video upload (ID)
├── MONETIZATION_GUIDE.md      ← Monetization guide
├── MULTI_ACCOUNT_GUIDE.md     ← Multi-account guide
├── CONTENT_SETTINGS_GUIDE.md  ← Content settings
└── STREAM_KEY_GUIDE.md        ← Stream key guide
```

### Sample Files
```
├── sample_videos.xlsx         ← Example Excel
├── sample_broadcasts.py       ← Example script
└── broadcasts_monetization.xlsx ← Example data
```

### Windows Launch
```
└── run.bat                    ← Quick launcher
```

---

## 🚀 Quick Start

### For Users (GUI Application)

1. **Install Python 3.7+** (if not installed)
   - Download from: https://python.org

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run application:**
   ```bash
   python main.py
   ```

4. **Or use launcher:**
   ```bash
   run.bat
   ```

---

### For Distribution (Portable EXE)

1. **Build portable version:**
   ```bash
   BUILD_PORTABLE.bat
   ```

2. **Result:** `streamPro Portable\` folder with EXE

3. **Distribute:** Compress to ZIP and share

---

## 🎯 Features (Windows)

✅ **Live Broadcast Management**
- Create broadcasts
- Batch processing from Excel
- Automatic scheduling

✅ **Video Upload**
- Upload with scheduling
- Batch upload from Excel
- Monetization settings

✅ **Automatic Scheduler**
- Daily automatic batch processing
- Configure time via GUI
- Keep app running for scheduler to work

✅ **Multi-Account Support**
- Switch between YouTube accounts
- Manage multiple channels
- Saved credentials

✅ **GUI Interface**
- Modern customtkinter UI
- Dark/Light theme
- Real-time monitoring

---

## 📝 Common Tasks

### Run Application
```bash
python main.py
```

### Build Portable Version
```bash
BUILD_PORTABLE.bat
```

### Check Scheduler Status
Open app → Tab "Import & Run" → Check right panel

### Update Excel File
Update your Excel → Scheduler will auto-reload

---

## 🔧 Configuration

### Scheduler Settings
Located in: `%USERPROFILE%\.ytlive\schedule.json`

### Credentials
Saved in: `%USERPROFILE%\.ytlive\credentials\`

### OAuth Tokens
Automatically managed by the app

---

## 📊 System Requirements

### Minimum
- Windows 7 or higher
- Python 3.7+
- 4GB RAM
- Internet connection

### Recommended
- Windows 10/11
- Python 3.9+
- 8GB RAM
- Stable internet

---

## 🎓 Documentation Quick Links

| Task | Guide |
|------|-------|
| Getting Started | `QUICKSTART.md` |
| Setup Scheduler | `CARA_PAKAI_SCHEDULER.txt` |
| Upload Videos | `VIDEO_UPLOAD_GUIDE.md` |
| Build Portable | `CARA_BUILD_PORTABLE.txt` |
| Multi-Account | `MULTI_ACCOUNT_GUIDE.md` |
| UI Layout | `UI_LAYOUT_GUIDE.txt` |

---

## ⚠️ Important Notes

### Scheduler Behavior
- **Requires app to stay running**
- Keep computer awake during scheduled time
- Prevent sleep/hibernate

### Windows Defender
Portable EXE might trigger Windows Defender (false positive)
- Add exception if needed

### Updates
- Pull latest code from repository
- Rebuild portable version if needed

---

## 🔍 Troubleshooting

### App won't start
```bash
# Check Python version
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Import Error
```bash
# Install specific package
pip install customtkinter
pip install google-api-python-client
```

### Scheduler Not Working
- Keep application running
- Don't minimize to tray (stay visible)
- Check computer power settings

---

## 🚫 Files Removed (Ubuntu/Linux)

These files were removed as they're Linux-only:
- ❌ `scheduler_headless.py`
- ❌ `*.service` files
- ❌ `*.sh` scripts
- ❌ `ecosystem.config.js`
- ❌ Ubuntu setup guides
- ❌ PM2 configurations

---

## 📞 Support

For Windows-specific issues:
1. Check documentation in `Docs/` folder
2. Verify Python version: `python --version`
3. Check logs in app's "Logs" tab
4. Rebuild portable if using EXE version

---

## 🎉 Summary

**This is now a Windows-only application!**

- ✅ Run with GUI on Windows
- ✅ Build portable EXE for distribution
- ✅ Use scheduler for automation
- ❌ No Linux/Ubuntu files
- ❌ No headless mode

**Main entry point:** `python main.py`

**For distribution:** `BUILD_PORTABLE.bat`

---

**Last Updated:** 2025-10-26  
**Platform:** Windows Only  
**Status:** ✅ Ready to Use
