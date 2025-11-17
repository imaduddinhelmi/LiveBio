@echo off
REM Fix build error exit code 100

echo ========================================
echo   Fix Build Error - Exit Code 100
echo ========================================
echo.

echo Changes being applied:
echo.
echo 1. buildozer.spec
echo    - Remove heavy dependencies (pandas, openpyxl)
echo    - Pin versions for stability
echo.
echo 2. GitHub Workflows
echo    - Add verbose build output
echo    - Pin buildozer version
echo    - Clean before build
echo.
echo 3. New Files
echo    - excel_parser_lite.py (lightweight parser)
echo    - FIX_BUILD_ERROR.md (documentation)
echo.
echo 4. main.py
echo    - Better import handling
echo    - Graceful fallbacks
echo.

set /p CONFIRM="Apply these fixes and push to GitHub? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo Staging files...
git add androstream/buildozer.spec
git add androstream/main.py
git add androstream/excel_parser_lite.py
git add .github/workflows/android-build.yml
git add .github/workflows/android-release.yml
git add FIX_BUILD_ERROR.md
git add fix_build_error.bat
git add fix_build_error.sh

echo.
echo Committing...
git commit -m "Fix: Resolve build error exit code 100

- Remove heavy dependencies (pandas, openpyxl)
- Pin versions for stability (python3==3.9.16, kivy==2.2.1)
- Add verbose build output for debugging
- Create lightweight excel_parser_lite.py
- Improve error handling and fallbacks
- Clean build directory before building"

if errorlevel 1 (
    echo.
    echo [ERROR] Commit failed.
    pause
    exit /b 1
)

echo.
echo Pushing to GitHub...
git push

if errorlevel 1 (
    echo.
    echo [ERROR] Push failed!
    echo Try: git push
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo.
echo Build error fixes have been pushed!
echo.
echo Next steps:
echo 1. Go to GitHub repository
echo 2. Click "Actions" tab
echo 3. New build should start automatically
echo 4. Monitor build with verbose output
echo 5. Build should succeed in ~15-20 min
echo.
echo If build still fails:
echo - Check logs in Actions tab
echo - Look for specific error message
echo - See FIX_BUILD_ERROR.md for troubleshooting
echo.
pause
