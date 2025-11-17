@echo off
REM Setup and push to NEW GitHub repository

echo ========================================
echo   Setup NEW GitHub Repository
echo ========================================
echo.

echo STEP 1: Create Repository on GitHub
echo ------------------------------------
echo.
echo 1. Open browser and go to: https://github.com/new
echo 2. Fill in:
echo    - Repository name: AutoLiveBio (or your preferred name)
echo    - Description: YouTube Live ^& Video Automation (Android + Desktop)
echo    - Visibility: Public (for unlimited GitHub Actions) or Private
echo    - DO NOT check: Add README, .gitignore, or license
echo 3. Click "Create repository"
echo.
echo Press any key after you created the repository...
pause >nul

echo.
echo STEP 2: Get Repository URL
echo ------------------------------------
echo.
echo You will see a page like this:
echo   "Quick setup — if you've done this kind of thing before"
echo.
echo Copy the HTTPS URL (looks like):
echo   https://github.com/username/AutoLiveBio.git
echo.

set /p REPO_URL="Paste your repository URL here: "

if "%REPO_URL%"=="" (
    echo.
    echo [ERROR] Repository URL cannot be empty!
    pause
    exit /b 1
)

echo.
echo Repository URL: %REPO_URL%
echo.

set /p CONFIRM="Is this correct? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Cancelled. Please run script again.
    pause
    exit /b 0
)

echo.
echo STEP 3: Initialize Git
echo ------------------------------------
echo.

REM Check if already initialized
if exist ".git" (
    echo [INFO] Git already initialized
    echo.
    
    REM Remove old remote if exists
    git remote remove origin 2>nul
    echo Old remote removed (if any)
) else (
    echo Initializing new git repository...
    git init
    echo [OK] Git initialized
)

echo.
echo STEP 4: Create .gitignore
echo ------------------------------------
echo.

REM Create comprehensive .gitignore
(
echo # Python
echo __pycache__/
echo *.py[cod]
echo *$py.class
echo *.so
echo .Python
echo *.egg-info/
echo dist/
echo build/
echo.
echo # Buildozer
echo .buildozer/
echo bin/
echo.
echo # Credentials - IMPORTANT! Never commit these!
echo client_secret*.json
echo token.pickle
echo credentials.json
echo .ytlive/
echo Data/
echo *.token
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo *.swo
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo desktop.ini
echo.
echo # Excel with sensitive data
echo *_custom_time.xlsx
echo sample_*.xlsx
echo broadcasts_monetization.xlsx
echo.
echo # Test files
echo test_*.py
echo *_test.py
) > .gitignore

echo [OK] .gitignore created
echo.

echo STEP 5: Check for Sensitive Files
echo ------------------------------------
echo.

set FOUND_SENSITIVE=0

if exist "client_secret*.json" (
    echo [WARNING] Found client_secret*.json files!
    echo           These will NOT be committed ^(in .gitignore^)
    set FOUND_SENSITIVE=1
)

if exist "token.pickle" (
    echo [WARNING] Found token.pickle!
    echo           This will NOT be committed ^(in .gitignore^)
    set FOUND_SENSITIVE=1
)

if exist "Data\" (
    echo [WARNING] Found Data/ folder!
    echo           This will NOT be committed ^(in .gitignore^)
    set FOUND_SENSITIVE=1
)

if %FOUND_SENSITIVE%==0 (
    echo [OK] No sensitive files found
)

echo.
echo STEP 6: Add Remote
echo ------------------------------------
echo.

git remote add origin %REPO_URL%
echo [OK] Remote added: %REPO_URL%

echo.
echo STEP 7: Stage Files
echo ------------------------------------
echo.

git add .
echo [OK] All files staged

echo.
echo Current status:
git status --short | findstr /V "^!!"
echo.

echo STEP 8: Commit
echo ------------------------------------
echo.

git commit -m "Initial commit: AndroStream - YouTube Automation

Features:
- Android app with Kivy (androstream/)
- Desktop app with CustomTkinter
- YouTube Live & Video automation
- Multi-account support
- GitHub Actions for automatic APK build
- Complete documentation (EN + ID)

Android Version:
- Mobile-optimized UI
- Authentication & Quick Create
- Build with Buildozer
- Auto-build via GitHub Actions

Desktop Version:
- Full-featured GUI
- Batch scheduling
- Excel import
- Video upload

All fixes applied:
- Build error exit code 100 fixed
- Dependencies optimized
- Verbose build output
- Lightweight parser"

if errorlevel 1 (
    echo.
    echo [ERROR] Commit failed!
    pause
    exit /b 1
)

echo [OK] Changes committed

echo.
echo STEP 9: Set Main Branch
echo ------------------------------------
echo.

git branch -M main
echo [OK] Branch renamed to 'main'

echo.
echo STEP 10: Push to GitHub
echo ------------------------------------
echo.

echo This may take a few minutes depending on file size...
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo ========================================
    echo   PUSH FAILED!
    echo ========================================
    echo.
    echo Possible reasons:
    echo 1. Authentication required
    echo    - Setup GitHub token: https://github.com/settings/tokens
    echo    - Or setup SSH: https://docs.github.com/en/authentication
    echo.
    echo 2. Repository doesn't exist
    echo    - Make sure you created it on GitHub first
    echo    - Check the URL is correct
    echo.
    echo 3. Network issues
    echo    - Check internet connection
    echo    - Try again later
    echo.
    echo To retry push:
    echo   git push -u origin main
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Your code is now on GitHub!
echo.
echo Repository: %REPO_URL%
echo.
echo Next steps:
echo.
echo 1. View your repository:
echo    %REPO_URL:~0,-4%
echo.
echo 2. GitHub Actions will start automatically:
echo    - Go to repository
echo    - Click "Actions" tab
echo    - See "Build Android APK" running
echo    - Wait ~15-20 minutes
echo    - Download APK from "Artifacts"
echo.
echo 3. Share your repository:
echo    - Public: Anyone can clone and contribute
echo    - Private: Only you and collaborators
echo.
echo 4. Documentation is in:
echo    - README_BUILD_OPTIONS.md (start here)
echo    - GITHUB_ACTIONS_SETUP.md (cloud build)
echo    - androstream/README.md (Android app)
echo.
echo ========================================
echo.
pause
