#!/bin/bash
# Setup GitHub repository and push code
# Run this script from Linux/Mac/WSL

set -e

echo "========================================"
echo "  GitHub Setup for AndroStream"
echo "========================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed!"
    echo ""
    echo "Install Git:"
    echo "  Ubuntu/Debian: sudo apt install git"
    echo "  macOS: brew install git"
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Check if already initialized
if [ -d ".git" ]; then
    echo "ℹ️  Git repository already initialized"
    echo ""
else
    echo "Initializing Git repository..."
    git init
    echo "✅ Git initialized"
    echo ""
fi

# Ask for GitHub repository URL
echo "Enter your GitHub repository URL:"
echo "Example: https://github.com/username/AutoLiveBio.git"
echo ""
read -p "Repository URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ Repository URL cannot be empty!"
    exit 1
fi

# Check if remote already exists
if git remote get-url origin &> /dev/null; then
    echo "ℹ️  Remote origin already exists"
    echo "Updating remote URL..."
    git remote set-url origin "$REPO_URL"
    echo "✅ Remote updated"
else
    echo "Adding remote origin..."
    git remote add origin "$REPO_URL"
    echo "✅ Remote added"
fi
echo ""

# Create/update .gitignore
echo "Creating .gitignore..."
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

# Credentials - IMPORTANT!
client_secret*.json
token.pickle
credentials.json
.ytlive/
Data/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Excel files with sensitive data
*_custom_time.xlsx
sample_*.xlsx
EOF
echo "✅ .gitignore created"
echo ""

# Check for sensitive files
echo "Checking for sensitive files..."
if ls client_secret*.json 1> /dev/null 2>&1; then
    echo "⚠️  Found client_secret*.json files!"
    echo "   These will NOT be committed (in .gitignore)"
fi
if [ -f "token.pickle" ]; then
    echo "⚠️  Found token.pickle!"
    echo "   This will NOT be committed (in .gitignore)"
fi
echo ""

# Stage files
echo "Staging files for commit..."
git add .
echo "✅ Files staged"
echo ""

# Show status
echo "Current status:"
git status --short
echo ""

# Commit
read -p "Enter commit message (or press Enter for default): " COMMIT_MSG
if [ -z "$COMMIT_MSG" ]; then
    COMMIT_MSG="Add Android version with GitHub Actions"
fi

echo "Committing changes..."
if git commit -m "$COMMIT_MSG"; then
    echo "✅ Changes committed"
else
    echo "ℹ️  No changes to commit or commit failed"
fi
echo ""

# Set main branch
git branch -M main
echo "✅ Branch set to main"
echo ""

# Push to GitHub
echo ""
echo "Ready to push to GitHub!"
echo ""
read -p "Push now? (y/n): " PUSH_NOW

if [ "$PUSH_NOW" = "y" ] || [ "$PUSH_NOW" = "Y" ]; then
    echo "Pushing to GitHub..."
    if git push -u origin main; then
        echo ""
        echo "========================================"
        echo "  SUCCESS!"
        echo "========================================"
        echo ""
        echo "Your code is now on GitHub!"
        echo ""
        echo "Next steps:"
        echo "1. Go to: $REPO_URL"
        echo "2. Click 'Actions' tab"
        echo "3. Wait for build to complete (~15-20 minutes)"
        echo "4. Download APK from 'Artifacts'"
        echo ""
    else
        echo ""
        echo "❌ Push failed!"
        echo ""
        echo "Possible reasons:"
        echo "1. Authentication failed - setup GitHub token/SSH"
        echo "2. Repository doesn't exist - create it on GitHub first"
        echo "3. Network issues"
        echo ""
        echo "To push later, run: git push -u origin main"
    fi
else
    echo ""
    echo "Skipped push. To push later, run:"
    echo "  git push -u origin main"
fi

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
