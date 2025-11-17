# 📦 StreamPro Portable - Build Guide

## Quick Build

### Cara Tercepat (Recommended)
```bash
# Double-click file ini:
BUILD_PORTABLE.bat
```

Atau via command line:
```bash
python build_portable.py
```

## Prerequisites

### 1. Install PyInstaller
```bash
pip install pyinstaller
```

### 2. Install Semua Dependencies
```bash
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python --version    # Should be 3.7+
pip list           # Check all packages installed
```

## Build Process

### Automatic Build (Recommended)

**Windows:**
```bash
BUILD_PORTABLE.bat
```

**Command Line:**
```bash
python build_portable.py
```

### Manual Build

Jika ingin build manual step-by-step:

```bash
# 1. Create spec file
python build_portable.py --spec-only

# 2. Build with PyInstaller
pyinstaller --clean --noconfirm StreamPro.spec

# 3. Copy files manually
# (See build_portable.py for file structure)
```

## Output Structure

```
streamPro Portable/
├── StreamPro.bat           # Launcher (klik ini untuk run)
├── README.txt              # User guide
├── version.txt             # Version info
│
├── App/                    # Executable & dependencies
│   ├── StreamPro.exe       # Main executable
│   ├── _internal/          # Python libraries
│   └── ...
│
├── Data/                   # User data (auto-created)
│   ├── credentials/
│   └── config/
│
├── Docs/                   # Documentation
│   ├── CARA_PAKAI_SCHEDULER.txt
│   ├── SCHEDULER_QUICKSTART.md
│   └── ...
│
└── Samples/               # Sample files
    └── sample_videos.xlsx
```

## Build Options

### Custom App Name
Edit `build_portable.py`:
```python
APP_NAME = "YourAppName"  # Change this
```

### Custom Version
```python
VERSION = "1.0.0"  # Change this
```

### Add Icon
1. Create `icon.ico` file
2. Edit spec file:
```python
icon='icon.ico'
```

### Include Additional Files
Edit `build_portable.py` → `create_spec_file()`:
```python
datas=[
    ('*.md', '.'),
    ('*.txt', '.'),
    ('your_file.ext', '.'),  # Add here
],
```

## Troubleshooting

### PyInstaller Not Found
```bash
pip install pyinstaller
# or
python -m pip install pyinstaller
```

### Import Error During Build
Add to `hiddenimports` in spec file:
```python
hiddenimports=[
    'customtkinter',
    'your_missing_module',  # Add here
],
```

### Large Executable Size
Normal size: 80-150 MB (includes Python + all libraries)

To reduce:
```python
upx=True,  # Already enabled
```

Install UPX:
- Download from: https://upx.github.io/
- Extract to PATH

### Build Fails on Specific Module
```bash
# Test module import
python -c "import module_name"

# If fails, install module
pip install module_name
```

### Windows Defender Blocks Executable
Normal behavior for PyInstaller apps.

**Solution:**
1. Add exception in Windows Defender
2. Or sign the executable (advanced)

## Testing

### Before Distribution

1. **Test on Clean System**
   - Copy to different computer
   - Test without Python installed

2. **Test All Features**
   - Login/Authentication
   - Create broadcast
   - Import Excel
   - Scheduler

3. **Check Data Persistence**
   - Close and reopen
   - Verify settings saved

## Distribution

### Create ZIP Archive
```bash
# Windows
PowerShell: Compress-Archive -Path "streamPro Portable" -DestinationPath "StreamPro-v1.0.0-Portable.zip"

# Or use 7-Zip, WinRAR, etc.
```

### Recommended Archive Structure
```
StreamPro-v1.0.0-Portable.zip
└── streamPro Portable/
    ├── StreamPro.bat
    ├── README.txt
    └── ...
```

### Distribution Checklist
- [ ] Test executable on clean system
- [ ] All documentation included
- [ ] README is clear and complete
- [ ] Version info correct
- [ ] Sample files included
- [ ] No sensitive data (credentials, tokens)

## Advanced: Custom Build

### Multi-Platform Build

**Windows:**
```bash
python build_portable.py
```

**Note:** PyInstaller builds are platform-specific.
For Linux/Mac, build on those platforms.

### Debug Build

Enable console for debugging:

Edit spec file:
```python
console=True,  # Show console window
debug=True,    # Enable debug mode
```

### One-File Build

Edit spec file - change to `EXE` mode:
```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # Include these
    a.zipfiles,  # Include these
    a.datas,     # Include these
    [],
    name='StreamPro',
    # ...
)
# Remove COLLECT section
```

**Pros:** Single .exe file
**Cons:** Slower startup, larger file

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Build Portable

on: [push]

jobs:
  build:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: pip install pyinstaller
      - run: python build_portable.py
      - uses: actions/upload-artifact@v2
        with:
          name: StreamPro-Portable
          path: streamPro Portable/
```

## Build Script Details

### What `build_portable.py` Does

1. **Check Dependencies**
   - Verify PyInstaller installed
   - Auto-install if missing

2. **Create Spec File**
   - Configure PyInstaller settings
   - Set hidden imports
   - Configure data files

3. **Build Executable**
   - Run PyInstaller
   - Bundle all dependencies

4. **Create Portable Structure**
   - Create folder hierarchy
   - Copy executable
   - Copy documentation
   - Copy samples

5. **Create Launcher**
   - Generate .bat file
   - User-friendly startup

6. **Generate README**
   - User guide
   - Quick start instructions

7. **Cleanup**
   - Remove build artifacts
   - Clean temporary files

## Performance

### Build Time
- First build: 3-5 minutes
- Subsequent builds: 1-2 minutes

### Size
- Executable folder: ~80-150 MB
- Compressed (ZIP): ~30-50 MB

## Version Management

### Updating Version

1. Edit `build_portable.py`:
```python
VERSION = "1.1.0"  # New version
```

2. Rebuild:
```bash
python build_portable.py
```

3. Version will appear in:
   - Launcher window title
   - README.txt
   - version.txt

## Support

### Build Issues
1. Check Python version (3.7+)
2. Verify all dependencies installed
3. Check build_portable.py output for errors

### Runtime Issues
1. Test on clean system
2. Check Windows Defender
3. Verify all files copied correctly

---

**Last Updated:** 2025-10-26  
**Build Script Version:** 1.0.0  
**Compatible With:** StreamPro v1.0.0+
