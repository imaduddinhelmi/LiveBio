#!/bin/bash
# Setup and push to NEW GitHub repository

echo "========================================"
echo "  Setup NEW GitHub Repository"
echo "========================================"
echo ""

echo "STEP 1: Create Repository on GitHub"
echo "------------------------------------"
echo ""
echo "1. Open browser and go to: https://github.com/new"
echo "2. Fill in:"
echo "   - Repository name: AutoLiveBio (or your preferred name)"
echo "   - Description: YouTube Live & Video Automation (Android + Desktop)"
echo "   - Visibility: Public (for unlimited GitHub Actions) or Private"
echo "   - DO NOT check: Add README, .gitignore, or license"
echo "3. Click 'Create repository'"
echo ""
read -p "Press Enter after you created the repository..."

echo ""
echo "STEP 2: Get Repository URL"
echo "------------------------------------"
echo ""
echo "You will see a page like this:"
echo "  'Quick setup — if you've done this kind of thing before'"
echo ""
echo "Copy the HTTPS URL (looks like):"
echo "  https://github.com/username/AutoLiveBio.git"
echo ""

read -p "Paste your repository URL here: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo ""
    echo "❌ Repository URL cannot be empty!"
    exit 1
fi

echo ""
echo "Repository URL: $REPO_URL"
echo ""

read -p "Is this correct? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Cancelled. Please run script again."
    exit 0
fi

echo ""
echo "STEP 3: Initialize Git"
echo "------------------------------------"
echo ""

# Check if already initialized
if [ -d ".git" ]; then
    echo "ℹ️  Git already initialized"
    echo ""
    
    # Remove old remote if exists
    git remote remove origin 2>/dev/null || true
    echo "Old remote removed (if any)"
else
    echo "Initializing new git repository..."
    git init
    echo "✅ Git initialized"
fi

echo ""
echo "STEP 4: Create .gitignore"
echo "------------------------------------"
echo ""

# Create comprehensive .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Buildozer
.buildozer/
bin/

# Credentials - IMPORTANT! Never commit these!
client_secret*.json
token.pickle
credentials.json
.ytlive/
Data/
*.token

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# Excel with sensitive data
*_custom_time.xlsx
sample_*.xlsx
broadcasts_monetization.xlsx

# Test files
test_*.py
*_test.py
EOF

echo "✅ .gitignore created"
echo ""

echo "STEP 5: Check for Sensitive Files"
echo "------------------------------------"
echo ""

FOUND_SENSITIVE=0

if ls client_secret*.json 1> /dev/null 2>&1; then
    echo "⚠️  Found client_secret*.json files!"
    echo "   These will NOT be committed (in .gitignore)"
    FOUND_SENSITIVE=1
fi

if [ -f "token.pickle" ]; then
    echo "⚠️  Found token.pickle!"
    echo "   This will NOT be committed (in .gitignore)"
    FOUND_SENSITIVE=1
fi

if [ -d "Data" ]; then
    echo "⚠️  Found Data/ folder!"
    echo "   This will NOT be committed (in .gitignore)"
    FOUND_SENSITIVE=1
fi

if [ $FOUND_SENSITIVE -eq 0 ]; then
    echo "✅ No sensitive files found"
fi

echo ""
echo "STEP 6: Add Remote"
echo "------------------------------------"
echo ""

git remote add origin "$REPO_URL"
echo "✅ Remote added: $REPO_URL"

echo ""
echo "STEP 7: Stage Files"
echo "------------------------------------"
echo ""

git add .
echo "✅ All files staged"

echo ""
echo "Current status:"
git status --short
echo ""

echo "STEP 8: Commit"
echo "------------------------------------"
echo ""

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

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Commit failed!"
    exit 1
fi

echo "✅ Changes committed"

echo ""
echo "STEP 9: Set Main Branch"
echo "------------------------------------"
echo ""

git branch -M main
echo "✅ Branch renamed to 'main'"

echo ""
echo "STEP 10: Push to GitHub"
echo "------------------------------------"
echo ""

echo "This may take a few minutes depending on file size..."
echo ""

git push -u origin main

if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "  PUSH FAILED!"
    echo "========================================"
    echo ""
    echo "Possible reasons:"
    echo "1. Authentication required"
    echo "   - Setup GitHub token: https://github.com/settings/tokens"
    echo "   - Or setup SSH: https://docs.github.com/en/authentication"
    echo ""
    echo "2. Repository doesn't exist"
    echo "   - Make sure you created it on GitHub first"
    echo "   - Check the URL is correct"
    echo ""
    echo "3. Network issues"
    echo "   - Check internet connection"
    echo "   - Try again later"
    echo ""
    echo "To retry push:"
    echo "  git push -u origin main"
    echo ""
    exit 1
fi

echo ""
echo "========================================"
echo "  SUCCESS!"
echo "========================================"
echo ""
echo "✅ Your code is now on GitHub!"
echo ""
echo "Repository: $REPO_URL"
echo ""
echo "Next steps:"
echo ""
echo "1. View your repository:"
REPO_WEB="${REPO_URL%.git}"
echo "   $REPO_WEB"
echo ""
echo "2. GitHub Actions will start automatically:"
echo "   - Go to repository"
echo "   - Click 'Actions' tab"
echo "   - See 'Build Android APK' running"
echo "   - Wait ~15-20 minutes"
echo "   - Download APK from 'Artifacts'"
echo ""
echo "3. Share your repository:"
echo "   - Public: Anyone can clone and contribute"
echo "   - Private: Only you and collaborators"
echo ""
echo "4. Documentation is in:"
echo "   - README_BUILD_OPTIONS.md (start here)"
echo "   - GITHUB_ACTIONS_SETUP.md (cloud build)"
echo "   - androstream/README.md (Android app)"
echo ""
echo "========================================"
echo ""
