@echo off
title StreamPro Portable Builder
color 0B

echo.
echo ===============================================================
echo    StreamPro Portable Builder
echo ===============================================================
echo.
echo This will create a portable version of StreamPro that:
echo   - Does not require installation
echo   - Can run from USB drive
echo   - Includes all dependencies
echo   - Ready to distribute
echo.
echo ===============================================================
echo.
pause

echo.
echo [1/3] Checking Python...
python --version
if errorlevel 1 (
    echo.
    echo [ERROR] Python not found!
    echo Please install Python 3.7+ from python.org
    pause
    exit /b 1
)

echo.
echo [2/3] Running build script...
echo.
python build_portable.py

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Build complete!
echo.
echo ===============================================================
echo   SUCCESS: Portable version created!
echo ===============================================================
echo.
echo Folder: streamPro Portable
echo.
echo To run the application:
echo   1. Open "streamPro Portable" folder
echo   2. Double-click "StreamPro.bat"
echo.
echo You can now:
echo   - Copy the folder to USB drive
echo   - Move to another computer
echo   - Zip for distribution
echo.
echo ===============================================================
echo.
pause
