# AndroStream - YouTube Automation for Android

Mobile version of YouTube Live & Video automation tool built with Kivy.

## Features

### ✅ Currently Implemented
- 🔐 **YouTube OAuth Authentication**
  - Multi-account support
  - Account switching
  - Saved credentials management
  
- ⚡ **Quick Broadcast Creation**
  - Create live broadcasts on-the-go
  - Schedule broadcasts
  - Configure privacy, category, and tags
  - Enable/disable monetization
  - DVR controls

### 🚧 Coming Soon
- 📊 Batch import from Excel files
- 📹 Video file upload
- 📋 View and manage upcoming broadcasts
- 🔄 Automatic scheduling
- 📸 Thumbnail upload from camera/gallery

## Requirements

### For Building APK:
- Linux/Mac OS or WSL2 on Windows
- Python 3.8+
- Buildozer
- Android SDK/NDK (will be auto-downloaded by Buildozer)

### For Development:
- Python 3.8+
- Kivy 2.2.1+
- All dependencies in requirements.txt

## Installation & Build

### Option 1: Build on Linux/Mac

1. **Install system dependencies:**

   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
   ```

   **macOS:**
   ```bash
   brew install python3 git
   xcode-select --install
   ```

2. **Install Buildozer:**
   ```bash
   pip3 install buildozer
   pip3 install cython
   ```

3. **Clone/Copy this folder:**
   ```bash
   cd androstream
   ```

4. **Initialize Buildozer (first time only):**
   ```bash
   buildozer android debug
   ```
   This will:
   - Download Android SDK & NDK
   - Download and compile all Python dependencies
   - Build the APK (takes 30-60 minutes first time)

5. **Build APK:**
   ```bash
   # Debug APK (for testing)
   buildozer android debug
   
   # Release APK (for distribution, requires signing)
   buildozer android release
   ```

6. **Install on device:**
   ```bash
   # Via USB (enable USB debugging on phone)
   buildozer android deploy run
   
   # Or manually install the APK from bin/ folder
   adb install bin/AndroStream-1.0.0-debug.apk
   ```

### Option 2: Build on Windows (WSL2)

1. **Install WSL2 Ubuntu:**
   ```powershell
   wsl --install -d Ubuntu
   ```

2. **Inside WSL terminal, follow Linux instructions above**

3. **Copy APK to Windows:**
   ```bash
   # Inside WSL
   cp bin/*.apk /mnt/c/Users/YourUsername/Desktop/
   ```

### Option 3: Use Cloud Build Service

Use services like:
- GitHub Actions (recommended)
- GitLab CI
- Travis CI

See `.github/workflows/android-build.yml` for example configuration.

## Development

### Run on Desktop (for testing):
```bash
pip install -r requirements.txt
python main.py
```

**Note:** Desktop testing is limited. Some Android-specific features won't work.

### Project Structure:
```
androstream/
├── main.py                    # Main Kivy application
├── auth.py                    # YouTube OAuth handler
├── youtube_service.py         # YouTube API wrapper
├── excel_parser.py            # Excel data parser
├── config.py                  # App configuration
├── multi_account_manager.py   # Multi-account management
├── buildozer.spec             # Build configuration
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Usage

1. **First Launch:**
   - Tap "🔐 Authentication"
   - Tap "Add Account"
   - Select your `client_secret.json` file (download from Google Cloud Console)
   - Complete OAuth flow in browser
   - Grant YouTube permissions

2. **Create Broadcast:**
   - Go to "⚡ Quick Create"
   - Fill in title, description, tags
   - Choose schedule time
   - Configure privacy and options
   - Tap "✨ Create Broadcast"

3. **Switch Accounts:**
   - Go to "🔐 Authentication"
   - Select account from dropdown
   - Tap "Switch"

## Getting YouTube API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project (or use existing)
3. Enable **YouTube Data API v3**
4. Create **OAuth 2.0 Client ID** credentials:
   - Application type: **Android** or **Desktop app**
   - Download JSON as `client_secret.json`
5. Transfer file to your Android device (via USB, cloud storage, etc.)

## Permissions

The app requires these Android permissions:
- **INTERNET** - For YouTube API access
- **WRITE_EXTERNAL_STORAGE** - For saving credentials and files
- **READ_EXTERNAL_STORAGE** - For reading client_secret.json
- **WAKE_LOCK** - Keep screen on during operations

## Troubleshooting

### Build fails with "Command failed: ..."
- Make sure all system dependencies are installed
- Try cleaning build: `buildozer android clean`
- Check Java version: `java -version` (should be 11 or 17)

### App crashes on launch
- Check logs: `adb logcat | grep python`
- Verify all dependencies in buildozer.spec

### OAuth doesn't work
- Make sure OAuth redirect URI is configured correctly
- For Android apps, use package name in Google Cloud Console
- Enable "YouTube Data API v3" in Google Cloud

### File chooser doesn't show files
- Grant storage permissions in Android settings
- Use Android file manager to locate client_secret.json

## Known Limitations

- OAuth flow requires external browser (opens automatically)
- Large Excel files may take time to process
- Video upload limited by device storage and internet speed
- Some features require Android 5.0+ (API 21)

## Version History

### v1.0.0 (Current)
- Initial Android release
- Multi-account authentication
- Quick broadcast creation
- Mobile-optimized UI

## Support & Contribution

- Report bugs via GitHub Issues
- Pull requests welcome
- For questions: Check documentation in parent folder

## License

Same as parent project (AutoLiveBio)

---

**Made with ❤️ using Kivy**
