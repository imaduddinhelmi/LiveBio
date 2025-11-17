@echo off
echo ========================================
echo WebStreamPro - Stopping Application
echo ========================================
echo.

call pm2 stop webstreampro

if errorlevel 1 (
    echo ERROR: Failed to stop application
    echo Make sure the application is running with PM2
) else (
    echo Application stopped successfully!
)

echo.
pause
