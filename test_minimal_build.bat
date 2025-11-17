@echo off
REM Test minimal build approach

echo ========================================
echo   Test Minimal Build
echo ========================================
echo.

echo Strategy: Build with JUST Kivy first
echo to verify build system works.
echo.

echo Current problem:
echo - Full app with Google API fails (exit code 100)
echo - Too many dependencies causing build failure
echo.

echo Solution:
echo - Step 1: Build minimal (Kivy only)
echo - Step 2: If works, add deps one by one
echo - Step 3: Find exact problem dependency
echo.

cd androstream

echo.
echo === Backing up current files ===
echo.

if not exist buildozer.spec.backup (
    copy buildozer.spec buildozer.spec.backup
    echo [OK] Backed up buildozer.spec
) else (
    echo [INFO] Backup already exists
)

if not exist main.py.backup (
    copy main.py main.py.backup
    echo [OK] Backed up main.py
) else (
    echo [INFO] Backup already exists
)

echo.
echo === Switching to minimal version ===
echo.

copy /Y buildozer.spec.minimal buildozer.spec
echo [OK] Using minimal buildozer.spec

copy /Y main_minimal.py main.py
echo [OK] Using minimal main.py

echo.
echo === Changes made ===
echo.

echo buildozer.spec:
echo   requirements = python3==3.9.16,kivy==2.2.1
echo   (removed: kivymd, google-*, all other deps)
echo.
echo   android.api = 31 (was 33)
echo   android.ndk = 23b (was 25b)
echo   android.archs = arm64-v8a only (was 2 archs)
echo.

echo main.py:
echo   Simple test app (no YouTube API)
echo   Just shows "Build worked!" message
echo.

cd ..

echo.
echo === Ready to commit and push ===
echo.

set /p CONFIRM="Commit and push minimal test? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Cancelled.
    echo.
    echo To restore original files:
    echo   cd androstream
    echo   copy buildozer.spec.backup buildozer.spec
    echo   copy main.py.backup main.py
    pause
    exit /b 0
)

echo.
echo Staging files...
git add androstream/buildozer.spec
git add androstream/main.py
git add androstream/buildozer.spec.minimal
git add androstream/main_minimal.py
git add androstream/buildozer.spec.backup
git add androstream/main.py.backup
git add FIX_BUILD_ERROR_AGGRESSIVE.md
git add test_minimal_build.bat

echo.
echo Committing...
git commit -m "Test: Minimal build with just Kivy

Approach: Simplify to absolute minimum to verify build system works.

Changes:
- buildozer.spec: Only python3 + kivy (no other deps)
- main.py: Simple test app (no YouTube API)
- android.api: 31 (was 33) for stability
- android.ndk: 23b (was 25b) for stability
- android.archs: arm64-v8a only (faster build)

If this builds successfully:
- Problem is dependencies (not build system)
- Will add back deps one by one to find culprit

If this still fails:
- Problem is SDK/NDK or environment
- Will try different versions"

if errorlevel 1 (
    echo [ERROR] Commit failed!
    pause
    exit /b 1
)

echo [OK] Committed
echo.

echo Pushing to GitHub...
git push

if errorlevel 1 (
    echo [ERROR] Push failed!
    echo Use GitHub token if authentication required.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.

echo Minimal test pushed to GitHub!
echo.

echo Next steps:
echo.
echo 1. Go to: https://github.com/imaduddinhelmi/androstream2/actions
echo 2. Trigger "Build Android APK" workflow
echo 3. Wait ~15-20 minutes
echo 4. Check result:
echo.
echo    If BUILD SUCCESS:
echo    ✅ Build system works!
echo    ✅ Problem is dependencies
echo    → Start adding deps back one by one
echo.
echo    If BUILD FAILED:
echo    ❌ Build system issue
echo    ❌ Need to try different SDK/NDK versions
echo    → Check error logs for details
echo.
echo 5. Download APK and test on Android
echo    (should see "Build worked!" message)
echo.

set /p OPEN="Open GitHub Actions in browser? (y/n): "
if /i "%OPEN%"=="y" (
    start https://github.com/imaduddinhelmi/androstream2/actions
)

echo.
pause
