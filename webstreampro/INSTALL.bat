@echo off
echo ========================================
echo WebStreamPro - Installation Script
echo ========================================
echo.

echo [1/3] Installing Node.js dependencies...
call npm install
if errorlevel 1 (
    echo ERROR: npm install failed
    pause
    exit /b 1
)

echo.
echo [2/3] Installing PM2 globally...
call npm install -g pm2
if errorlevel 1 (
    echo WARNING: PM2 install failed. You may need to run as Administrator.
    echo You can install PM2 manually later: npm install -g pm2
)

echo.
echo [3/3] Creating necessary folders...
if not exist "data" mkdir data
if not exist "data\tokens" mkdir data\tokens
if not exist "uploads" mkdir uploads
if not exist "logs" mkdir logs

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env (already done)
echo 2. Upload your client_secret.json via web interface
echo 3. Run: npm run pm2:start
echo 4. Access: http://localhost:3000
echo.
pause
