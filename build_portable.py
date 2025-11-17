"""
Build script untuk membuat StreamPro Portable Executable
Menggunakan PyInstaller untuk package aplikasi
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Konfigurasi
APP_NAME = "StreamPro"
VERSION = "1.0.0"
PORTABLE_FOLDER = "streampro"
BUILD_FOLDER = "build"
DIST_FOLDER = "dist"

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print(f"[OK] PyInstaller found: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("[ERROR] PyInstaller not found!")
        print("\nInstalling PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True

def create_spec_file():
    """Create PyInstaller spec file"""
    print("[INFO] Creating PyInstaller spec file...")
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('*.md', '.'),
        ('*.txt', '.'),
    ],
    hiddenimports=[
        'customtkinter',
        'PIL._tkinter_finder',
        'google.auth',
        'google.auth.transport',
        'google_auth_oauthlib',
        'googleapiclient',
        'pandas',
        'openpyxl',
        'schedule',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
        'matplotlib',
        'scipy',
        'torch',
        'tensorflow',
        'IPython',
        'jedi',
        'parso',
        'zmq',
        'pygame',
        'lxml',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon here if available
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{APP_NAME}',
)
'''
    
    with open('StreamPro.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("[OK] Spec file created: StreamPro.spec")

def build_executable():
    """Build executable using PyInstaller"""
    print_header("Building Executable")
    
    print("[INFO] Running PyInstaller...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--clean",
        "--noconfirm",
        "StreamPro.spec"
    ]
    
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print("\n[OK] Build successful!")
        return True
    else:
        print("\n[ERROR] Build failed!")
        return False

def create_portable_structure():
    """Create portable folder structure"""
    print_header("Creating Portable Structure")
    
    # Create main portable folder
    portable_path = Path(PORTABLE_FOLDER)
    if portable_path.exists():
        print(f"[INFO] Removing existing folder: {PORTABLE_FOLDER}")
        shutil.rmtree(portable_path)
    
    portable_path.mkdir(exist_ok=True)
    print(f"[OK] Created: {PORTABLE_FOLDER}")
    
    # Create subfolders
    folders = [
        "App",
        "Data",
        "Data/credentials",
        "Data/config",
        "Docs",
        "Samples"
    ]
    
    for folder in folders:
        folder_path = portable_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"[OK] Created: {folder}")
    
    return portable_path

def copy_executable(portable_path):
    """Copy built executable to portable folder"""
    print_header("Copying Executable")
    
    dist_path = Path(DIST_FOLDER) / APP_NAME
    app_path = portable_path / "App"
    
    if not dist_path.exists():
        print(f"[ERROR] Build output not found: {dist_path}")
        return False
    
    print(f"[INFO] Copying from {dist_path} to {app_path}...")
    
    # Copy all files
    for item in dist_path.iterdir():
        dest = app_path / item.name
        if item.is_file():
            shutil.copy2(item, dest)
        else:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(item, dest)
    
    print("[OK] Executable copied successfully")
    return True

def copy_documentation(portable_path):
    """Copy documentation files"""
    print_header("Copying Documentation")
    
    docs_path = portable_path / "Docs"
    
    # Documentation files to copy
    doc_files = [
        "README.md",
        "CARA_PAKAI_SCHEDULER.txt",
        "SCHEDULER_QUICKSTART.md",
        "SCHEDULER_GUIDE.md",
        "FITUR_BARU_SCHEDULER.md",
        "UI_LAYOUT_GUIDE.txt",
        "QUICKSTART.md",
        "CONTENT_SETTINGS_GUIDE.md",
        "MULTI_ACCOUNT_GUIDE.md",
    ]
    
    for doc_file in doc_files:
        src = Path(doc_file)
        if src.exists():
            dest = docs_path / doc_file
            shutil.copy2(src, dest)
            print(f"[OK] Copied: {doc_file}")
        else:
            print(f"[SKIP] Not found: {doc_file}")

def copy_samples(portable_path):
    """Copy sample files"""
    print_header("Copying Sample Files")
    
    samples_path = portable_path / "Samples"
    
    sample_files = [
        "sample_videos.xlsx",
        "sample_broadcasts.py",
    ]
    
    for sample_file in sample_files:
        src = Path(sample_file)
        if src.exists():
            dest = samples_path / sample_file
            shutil.copy2(src, dest)
            print(f"[OK] Copied: {sample_file}")
        else:
            print(f"[SKIP] Not found: {sample_file}")

def create_launcher(portable_path):
    """Create launcher batch file"""
    print_header("Creating Launcher")
    
    launcher_content = f'''@echo off
title {APP_NAME} Launcher
color 0A

echo.
echo ===============================================
echo    {APP_NAME} v{VERSION}
echo    Portable Edition
echo ===============================================
echo.
echo Starting application...
echo.

cd /d "%~dp0"
start "" "App\\{APP_NAME}.exe"

timeout /t 2 /nobreak > nul
exit
'''
    
    launcher_path = portable_path / f"{APP_NAME}.bat"
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print(f"[OK] Launcher created: {APP_NAME}.bat")

def create_readme(portable_path):
    """Create portable README"""
    print_header("Creating README")
    
    readme_content = f'''# {APP_NAME} Portable v{VERSION}

## Quick Start

1. Double-click: **{APP_NAME}.bat**
2. Aplikasi akan terbuka otomatis
3. Selesai!

## Folder Structure

```
{PORTABLE_FOLDER}/
├── {APP_NAME}.bat           <- KLIK INI untuk menjalankan
├── README.txt               <- File ini
│
├── App/                     <- Aplikasi executable
│   ├── {APP_NAME}.exe
│   └── ... (libraries & dependencies)
│
├── Data/                    <- Data & konfigurasi (otomatis dibuat)
│   ├── credentials/         <- OAuth credentials tersimpan di sini
│   └── config/              <- Konfigurasi scheduler
│
├── Docs/                    <- Dokumentasi lengkap
│   ├── CARA_PAKAI_SCHEDULER.txt
│   ├── SCHEDULER_QUICKSTART.md
│   └── ... (dokumentasi lainnya)
│
└── Samples/                 <- File contoh
    └── sample_videos.xlsx

```

## Cara Menggunakan

### First Time Setup

1. **Jalankan Aplikasi**
   - Double-click `{APP_NAME}.bat`
   - Atau langsung jalankan `App\\{APP_NAME}.exe`

2. **Login ke YouTube**
   - Tab "Auth" → Select client_secret.json
   - Klik "Add New Account"
   - Login dengan akun YouTube Anda

3. **Mulai Menggunakan**
   - Tab "Quick Create" - Buat broadcast real-time
   - Tab "Import & Run" - Batch upload dari Excel
   - Tab "Video Upload" - Upload video dengan scheduling

### Automatic Scheduler

1. Tab "Import & Run"
2. Load Excel file
3. Lihat **Panel Kanan** (berwarna biru)
4. Set "Daily Run Time" → contoh: 09:00
5. Klik "▶ Enable Scheduler"

Dokumentasi lengkap ada di folder `Docs/`

## Fitur Utama

✓ Live Broadcast Creation & Management
✓ Batch Upload dari Excel
✓ Video Upload dengan Scheduling
✓ Automatic Daily Scheduler
✓ Multi-Channel Support
✓ Automatic Monetization Settings

## Data & Settings

Semua data disimpan di folder `Data/`:

- **Credentials**: `Data/credentials/` atau `%USERPROFILE%\\.ytlive\\`
- **Scheduler Config**: `%USERPROFILE%\\.ytlive\\schedule.json`
- **OAuth Tokens**: Tersimpan terenkripsi

## Portable Usage

Aplikasi ini **100% portable**:
- ✓ Tidak perlu install
- ✓ Bisa dijalankan dari USB drive
- ✓ Bisa dipindah ke komputer lain
- ✓ Semua dependency sudah included

## Requirements

- Windows 7/8/10/11
- Internet connection
- YouTube account
- Google Cloud Project (untuk client_secret.json)

## Troubleshooting

### Aplikasi tidak mau jalan?

1. **Windows Defender/Antivirus**
   - Aplikasi mungkin diblok
   - Add exception untuk folder ini

2. **Missing DLL**
   - Install Microsoft Visual C++ Redistributable
   - Download dari microsoft.com

3. **Error saat login**
   - Pastikan client_secret.json valid
   - Check internet connection

### Error "Module not found"

Ini tidak seharusnya terjadi karena semua dependency sudah di-bundle.
Jika terjadi, coba:
1. Re-download portable version
2. Extract ulang ke folder baru

## Documentation

Dokumentasi lengkap tersedia di folder `Docs/`:

- **CARA_PAKAI_SCHEDULER.txt** - Panduan lengkap scheduler
- **SCHEDULER_QUICKSTART.md** - Quick start 5 menit
- **UI_LAYOUT_GUIDE.txt** - Panduan interface
- **QUICKSTART.md** - Panduan umum aplikasi

## Support

Untuk bantuan lebih lanjut:
1. Baca dokumentasi di folder `Docs/`
2. Check troubleshooting guide
3. Review sample files di `Samples/`

## Version Info

- **Version**: {VERSION}
- **Build Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Type**: Portable Edition (No Installation Required)

---

**Selamat Menggunakan {APP_NAME}!**

Portable Edition - Ready to Run Anywhere
'''
    
    readme_path = portable_path / "README.txt"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("[OK] README created")

def create_version_info(portable_path):
    """Create version info file"""
    version_info = f'''Application: {APP_NAME}
Version: {VERSION}
Type: Portable Edition
Build: PyInstaller
Python: {sys.version}
Platform: Windows

Features:
- Live Broadcast Management
- Batch Processing from Excel
- Video Upload with Scheduling
- Automatic Daily Scheduler
- Multi-Account Support

Dependencies Included:
- customtkinter
- google-api-python-client
- pandas, openpyxl
- schedule
- All required libraries

Data Storage:
- Credentials: %USERPROFILE%\\.ytlive\\
- Config: %USERPROFILE%\\.ytlive\\schedule.json
'''
    
    version_path = portable_path / "version.txt"
    with open(version_path, 'w', encoding='utf-8') as f:
        f.write(version_info)
    
    print("[OK] Version info created")

def cleanup_build_files():
    """Clean up build artifacts"""
    print_header("Cleaning Up")
    
    cleanup_items = [BUILD_FOLDER, "StreamPro.spec", "__pycache__"]
    
    for item in cleanup_items:
        path = Path(item)
        if path.exists():
            if path.is_file():
                path.unlink()
                print(f"[OK] Removed file: {item}")
            else:
                shutil.rmtree(path)
                print(f"[OK] Removed folder: {item}")

def main():
    """Main build process"""
    print_header(f"{APP_NAME} Portable Builder v{VERSION}")
    
    try:
        # Check dependencies
        if not check_pyinstaller():
            return
        
        # Create spec file
        create_spec_file()
        
        # Build executable
        if not build_executable():
            print("\n[ERROR] Build process failed!")
            return
        
        # Create portable structure
        portable_path = create_portable_structure()
        
        # Copy files
        if not copy_executable(portable_path):
            print("\n[ERROR] Failed to copy executable!")
            return
        
        copy_documentation(portable_path)
        copy_samples(portable_path)
        
        # Create additional files
        create_launcher(portable_path)
        create_readme(portable_path)
        create_version_info(portable_path)
        
        # Cleanup
        cleanup_build_files()
        
        # Success message
        print_header("Build Complete!")
        print(f"[SUCCESS] Portable version created in: {PORTABLE_FOLDER}")
        print(f"\nTo run the application:")
        print(f"  1. Open folder: {PORTABLE_FOLDER}")
        print(f"  2. Double-click: {APP_NAME}.bat")
        print("\nYou can now:")
        print(f"  - Copy '{PORTABLE_FOLDER}' folder to USB drive")
        print(f"  - Move it to another computer")
        print(f"  - Zip it for distribution")
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\n[ERROR] Build failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
