@echo off
REM Setup GitHub repository and push code
REM Run this script from Windows

echo ========================================
echo   GitHub Setup for AndroStream
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git is not installed!
    echo.
    echo Please install Git from: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git is installed
echo.

REM Check if already initialized
if exist ".git" (
    echo [INFO] Git repository already initialized
    echo.
) else (
    echo Initializing Git repository...
    git init
    echo [OK] Git initialized
    echo.
)

REM Ask for GitHub repository URL
echo Enter your GitHub repository URL:
echo Example: https://github.com/username/AutoLiveBio.git
echo.
set /p REPO_URL="Repository URL: "

if "%REPO_URL%"=="" (
    echo [ERROR] Repository URL cannot be empty!
    pause
    exit /b 1
)

REM Check if remote already exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo Adding remote origin...
    git remote add origin %REPO_URL%
    echo [OK] Remote added
) else (
    echo [INFO] Remote origin already exists
    echo Updating remote URL...
    git remote set-url origin %REPO_URL%
    echo [OK] Remote updated
)
echo.

REM Create/update .gitignore
echo Creating .gitignore...
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
echo # Credentials - IMPORTANT!
echo client_secret*.json
echo token.pickle
echo credentials.json
echo .ytlive/
echo Data/
echo.
echo # IDE
echo .vscode/
echo .idea/
echo *.swp
echo.
echo # OS
echo .DS_Store
echo Thumbs.db
echo.
echo # Excel files with sensitive data
echo *_custom_time.xlsx
echo sample_*.xlsx
) > .gitignore
echo [OK] .gitignore created
echo.

REM Check for sensitive files
echo Checking for sensitive files...
if exist "client_secret*.json" (
    echo [WARNING] Found client_secret*.json files!
    echo These will NOT be committed ^(in .gitignore^)
)
if exist "token.pickle" (
    echo [WARNING] Found token.pickle!
    echo This will NOT be committed ^(in .gitignore^)
)
echo.

REM Stage files
echo Staging files for commit...
git add .
echo [OK] Files staged
echo.

REM Show status
echo Current status:
git status
echo.

REM Commit
set /p COMMIT_MSG="Enter commit message (or press Enter for default): "
if "%COMMIT_MSG%"=="" (
    set COMMIT_MSG=Add Android version with GitHub Actions
)

echo Committing changes...
git commit -m "%COMMIT_MSG%"
if errorlevel 1 (
    echo [INFO] No changes to commit or commit failed
) else (
    echo [OK] Changes committed
)
echo.

REM Set main branch
git branch -M main
echo [OK] Branch set to main
echo.

REM Push to GitHub
echo.
echo Ready to push to GitHub!
echo.
set /p PUSH_NOW="Push now? (y/n): "
if /i "%PUSH_NOW%"=="y" (
    echo Pushing to GitHub...
    git push -u origin main
    if errorlevel 1 (
        echo.
        echo [ERROR] Push failed!
        echo.
        echo Possible reasons:
        echo 1. Authentication failed - setup GitHub token/SSH
        echo 2. Repository doesn't exist - create it on GitHub first
        echo 3. Network issues
        echo.
        echo To push later, run: git push -u origin main
    ) else (
        echo.
        echo ========================================
        echo   SUCCESS!
        echo ========================================
        echo.
        echo Your code is now on GitHub!
        echo.
        echo Next steps:
        echo 1. Go to: %REPO_URL%
        echo 2. Click "Actions" tab
        echo 3. Wait for build to complete ^(~15-20 minutes^)
        echo 4. Download APK from "Artifacts"
        echo.
    )
) else (
    echo.
    echo Skipped push. To push later, run:
    echo   git push -u origin main
)

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
pause
