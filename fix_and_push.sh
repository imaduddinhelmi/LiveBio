#!/bin/bash
# Quick fix script to commit and push GitHub Actions updates

echo "========================================"
echo "  Fix GitHub Actions v3 to v4"
echo "========================================"
echo ""

echo "Checking git status..."
git status
echo ""

echo "Files updated:"
echo "  - .github/workflows/android-build.yml"
echo "  - .github/workflows/android-release.yml"
echo "  - FIX_GITHUB_ACTIONS.md"
echo ""
echo "Changes:"
echo "  - actions/cache@v3 -> v4"
echo "  - actions/upload-artifact@v3 -> v4"
echo ""

read -p "Commit and push these fixes? (y/n): " CONFIRM
if [ "$CONFIRM" != "y" ] && [ "$CONFIRM" != "Y" ]; then
    echo "Cancelled."
    exit 0
fi

echo ""
echo "Staging files..."
git add .github/workflows/android-build.yml
git add .github/workflows/android-release.yml
git add FIX_GITHUB_ACTIONS.md

echo ""
echo "Committing..."
git commit -m "Fix: Update GitHub Actions to v4 (deprecated v3)"

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Commit failed. Maybe no changes or git error."
    exit 1
fi

echo ""
echo "Pushing to GitHub..."
git push

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Push failed!"
    echo ""
    echo "Possible reasons:"
    echo "1. Not connected to internet"
    echo "2. Authentication failed"
    echo "3. Remote repository issue"
    echo ""
    echo "Try: git push"
    exit 1
fi

echo ""
echo "========================================"
echo "  SUCCESS!"
echo "========================================"
echo ""
echo "✅ GitHub Actions workflows have been fixed!"
echo ""
echo "Next steps:"
echo "1. Go to: https://github.com/your-repo"
echo "2. Click 'Actions' tab"
echo "3. Latest run should show success"
echo "4. Download APK from Artifacts"
echo ""
