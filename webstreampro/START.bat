@echo off
echo ========================================
echo WebStreamPro - Starting Application
echo ========================================
echo.

echo Starting with PM2...
call pm2 start ecosystem.config.js

if errorlevel 1 (
    echo.
    echo ERROR: Failed to start with PM2
    echo.
    echo Trying to start in development mode instead...
    echo.
    call npm start
) else (
    echo.
    echo Application started successfully!
    echo.
    echo Access: http://localhost:3000
    echo.
    echo PM2 Commands:
    echo - View logs:   pm2 logs webstreampro
    echo - Stop app:    pm2 stop webstreampro
    echo - Restart app: pm2 restart webstreampro
    echo - Status:      pm2 status
    echo.
    echo Opening browser...
    timeout /t 3 /nobreak >nul
    start http://localhost:3000
)

pause
