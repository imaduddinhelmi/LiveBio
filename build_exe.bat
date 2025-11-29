@echo off
echo ========================================
echo Building AutoLiveBio Executable
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] Cleaning old build files...
if exist build rmdir /s /q build
if exist "streamExe\*.exe" del /q "streamExe\*.exe"
if exist "streamExe\*.spec" del /q "streamExe\*.spec"

echo.
echo [2/3] Building executable with PyInstaller...
echo This may take a few minutes...
echo.

python -m PyInstaller ^
    --name="AutoLiveBio" ^
    --onefile ^
    --windowed ^
    --icon=NONE ^
    --distpath="streamExe" ^
    --workpath="build" ^
    --specpath="streamExe" ^
    --add-data="requirements.txt;." ^
    --hidden-import=customtkinter ^
    --hidden-import=pandas ^
    --hidden-import=openpyxl ^
    --hidden-import=google.auth ^
    --hidden-import=google.oauth2 ^
    --hidden-import=googleapiclient ^
    --hidden-import=schedule ^
    --hidden-import=PIL ^
    --hidden-import=PIL._tkinter_finder ^
    --collect-all=customtkinter ^
    --exclude-module=PyQt5 ^
    --exclude-module=PyQt6 ^
    --exclude-module=PySide2 ^
    --exclude-module=PySide6 ^
    --exclude-module=torch ^
    --exclude-module=tensorflow ^
    --exclude-module=matplotlib ^
    --exclude-module=scipy ^
    --exclude-module=IPython ^
    --exclude-module=jedi ^
    --exclude-module=pygame ^
    --noconsole ^
    gui.py

echo.
if %ERRORLEVEL% EQU 0 (
    echo [3/3] Build successful!
    echo.
    echo ========================================
    echo Executable created at:
    echo streamExe\AutoLiveBio.exe
    echo ========================================
    echo.
    echo File size:
    dir "streamExe\AutoLiveBio.exe" | find "AutoLiveBio.exe"
    echo.
) else (
    echo [ERROR] Build failed with error code %ERRORLEVEL%
    echo.
    echo Please check the error messages above.
    echo.
)

pause
