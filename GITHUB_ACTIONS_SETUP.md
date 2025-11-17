# 🤖 Setup GitHub Actions - Complete Guide

## Overview

GitHub Actions akan **build APK secara otomatis di cloud** setiap kali Anda push code. **100% gratis** untuk public repositories, tidak perlu install WSL atau dependencies lokal!

---

## ⚡ Quick Start (5 Menit Setup!)

### Step 1: Buat Repository di GitHub

1. Buka https://github.com/new
2. Isi:
   - **Repository name**: `AutoLiveBio` (atau nama lain)
   - **Description**: YouTube Live & Video Automation
   - **Visibility**: Public (untuk free Actions) atau Private (limited minutes)
3. **JANGAN centang** "Add README" atau "Add .gitignore"
4. Klik **"Create repository"**

### Step 2: Run Setup Script

**Di Windows (PowerShell/CMD):**
```cmd
cd D:\A-YT\YT\AutoLiveBio
setup_github.bat
```

**Di Linux/Mac/WSL:**
```bash
cd /path/to/AutoLiveBio
chmod +x setup_github.sh
./setup_github.sh
```

Script akan:
- ✅ Initialize git repository
- ✅ Add remote origin
- ✅ Create .gitignore (protect credentials!)
- ✅ Commit all files
- ✅ Push to GitHub

### Step 3: Monitor Build

1. Go to: `https://github.com/username/AutoLiveBio`
2. Click **"Actions"** tab
3. See workflow **"Build Android APK"** running
4. Wait ~15-20 minutes (first build)
5. Download APK from **"Artifacts"**

**🎉 DONE! APK siap didownload!**

---

## 📋 Manual Setup (Alternative)

Jika setup script tidak work, lakukan manual:

### 1. Initialize Git

```bash
cd D:\A-YT\YT\AutoLiveBio  # atau path Anda
git init
```

### 2. Create .gitignore

Buat file `.gitignore` di root folder:

```gitignore
# Python
__pycache__/
*.py[cod]
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
```

**⚠️ PENTING:** File `client_secret.json` dan credentials TIDAK BOLEH di-commit!

### 3. Add Remote

```bash
git remote add origin https://github.com/username/AutoLiveBio.git
# Ganti 'username' dengan username GitHub Anda
```

### 4. Commit & Push

```bash
git add .
git commit -m "Add Android version with GitHub Actions"
git branch -M main
git push -u origin main
```

Jika gagal:
- Setup GitHub token: https://github.com/settings/tokens
- Atau setup SSH key: https://docs.github.com/en/authentication

---

## 🔄 Workflows yang Tersedia

### 1. **android-build.yml** (Auto Build)

**Trigger:**
- Push ke branch `main`, `master`, atau `develop`
- Push yang mengubah file di folder `androstream/`
- Pull request
- Manual trigger (workflow_dispatch)

**Output:**
- Debug APK
- Upload ke Artifacts (30 days retention)

**Usage:**
```bash
# Build otomatis setelah push
git add .
git commit -m "Update Android app"
git push

# Or trigger manual dari GitHub web
# Actions → Build Android APK → Run workflow
```

### 2. **android-release.yml** (Release Build)

**Trigger:**
- Push tag versi (e.g., `v1.0.0`, `v1.1.0`)
- Manual trigger dengan version input

**Output:**
- Release APK (unsigned)
- ZIP package (APK + docs)
- GitHub Release with notes

**Usage:**
```bash
# Create and push tag
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions akan:
# 1. Build release APK
# 2. Create GitHub Release
# 3. Upload APK ke Release page
```

### 3. **test-build.yml** (Quick Test)

**Trigger:**
- Pull request
- Manual trigger

**Purpose:**
- Quick validation (~5 minutes)
- Check buildozer.spec syntax
- Validate Python files
- No actual APK build (just tests)

---

## 📥 Download APK dari GitHub

### Method 1: Via Web

1. Go to repository
2. Click **"Actions"** tab
3. Click on completed workflow run
4. Scroll down to **"Artifacts"**
5. Click **"AndroStream-Debug-APK"** to download ZIP
6. Extract ZIP → get APK file

### Method 2: Via GitHub CLI

```bash
# Install GitHub CLI
# Windows: winget install GitHub.cli
# Mac: brew install gh
# Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md

# Login
gh auth login

# List recent runs
gh run list --workflow=android-build.yml

# Download latest artifact
gh run download --name AndroStream-Debug-APK
```

### Method 3: Via API

```bash
# Get workflow runs
curl -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/username/AutoLiveBio/actions/runs

# Download artifact (get artifact_id from above)
curl -L -H "Authorization: token YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/username/AutoLiveBio/actions/artifacts/ARTIFACT_ID/zip \
  -o apk.zip
```

---

## 🏷️ Create Release

### Via Git Tag:

```bash
# Update version in buildozer.spec (optional, auto-updated by workflow)
# version = 1.0.0

# Create tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag
git push origin v1.0.0
```

### Via GitHub Web:

1. Go to repository
2. Click **"Releases"** → **"Create a new release"**
3. Click **"Choose a tag"** → Type `v1.0.0` → **"Create new tag"**
4. Fill in title: `AndroStream v1.0.0`
5. Fill in description (optional)
6. Click **"Publish release"**
7. GitHub Actions will build APK and attach it automatically

---

## ⚙️ Configuration

### Customize Workflows

Edit `.github/workflows/android-build.yml`:

**Change trigger branches:**
```yaml
on:
  push:
    branches: [ main, develop, feature/* ]  # Add more branches
```

**Change Python version:**
```yaml
- name: Set up Python
  with:
    python-version: '3.10'  # Change to 3.10
```

**Increase timeout:**
```yaml
jobs:
  build:
    timeout-minutes: 180  # Change from 120 to 180
```

**Change artifact retention:**
```yaml
- name: Upload APK
  with:
    retention-days: 90  # Change from 30 to 90
```

### Secrets untuk Signing

Jika ingin sign APK otomatis:

1. Go to repository → **Settings** → **Secrets and variables** → **Actions**
2. Add secrets:
   - `KEYSTORE_FILE` (base64 of keystore.jks)
   - `KEYSTORE_PASSWORD`
   - `KEY_ALIAS`
   - `KEY_PASSWORD`

Edit workflow, add step:

```yaml
- name: Sign APK
  run: |
    echo "${{ secrets.KEYSTORE_FILE }}" | base64 -d > keystore.jks
    jarsigner -verbose \
      -sigalg SHA256withRSA \
      -digestalg SHA-256 \
      -keystore keystore.jks \
      -storepass "${{ secrets.KEYSTORE_PASSWORD }}" \
      -keypass "${{ secrets.KEY_PASSWORD }}" \
      androstream/bin/*.apk \
      "${{ secrets.KEY_ALIAS }}"
```

---

## 🔧 Troubleshooting

### Build Failed

**Check logs:**
1. Actions tab → Click failed run
2. Click failed job
3. Expand failing step
4. Read error message

**Common issues:**

**1. "No space left on device"**
```yaml
# Add before build step:
- name: Free disk space
  run: |
    sudo rm -rf /usr/share/dotnet
    sudo rm -rf /opt/ghc
    df -h
```

**2. "SDK license not accepted"**
```yaml
# Already handled in workflow:
yes | buildozer android debug || true
```

**3. "Buildozer timeout"**
```yaml
# Increase timeout:
timeout-minutes: 180
```

**4. "Python package conflict"**
```yaml
# Pin cython version:
pip install cython==0.29.36
```

### Slow Build

**First build:** 15-25 minutes (normal, downloads SDK/NDK)

**Subsequent builds:** 8-15 minutes (with cache)

**Speed up:**
- Cache is already configured
- Use `test-build.yml` for quick validation
- Build only when needed (use path filters)

### Cannot Download APK

**Check retention:**
- Artifacts expire after 30 days (configurable)
- Download before expiration

**Alternative:**
- Use Release workflow (artifacts don't expire)
- Enable GitHub Packages

---

## 💰 Cost & Limits

### GitHub Free Tier:

- ✅ **Public repos:** Unlimited minutes
- ✅ **Private repos:** 2000 minutes/month
- ✅ **Storage:** 500MB artifacts

### Estimasi Usage:

| Build Type | Minutes | Builds/Month (Free) |
|-----------|---------|---------------------|
| Full Build | ~20 min | 100 builds |
| Quick Test | ~5 min | 400 tests |
| Release | ~25 min | 80 releases |

**Tip:** Use public repo untuk unlimited builds!

---

## 📊 Monitor Usage

1. Go to repository → **Settings** → **Billing**
2. Or: https://github.com/settings/billing
3. See **"Actions minutes"** usage

---

## 🆚 Comparison: GitHub Actions vs WSL

| Feature | GitHub Actions | WSL Build |
|---------|---------------|-----------|
| **Setup Time** | 5 minutes | 30-60 minutes |
| **First Build** | 15-20 min | 30-60 min |
| **Subsequent** | 8-15 min | 2-5 min |
| **Requirements** | Just Git | WSL + Java + Buildozer |
| **Auto Build** | ✅ Yes | ❌ Manual |
| **Cost** | Free (public) | Free |
| **Download** | Web/CLI | Local file |
| **Best For** | Team, CI/CD | Personal, Fast iteration |

**Recommendation:**
- **Team project / CI/CD**: Use GitHub Actions
- **Solo dev / Frequent builds**: Use WSL
- **Best**: Use both! GitHub for releases, WSL for development

---

## 🎯 Next Steps

### After First Build:

1. ✅ Download APK
2. ✅ Test on Android device
3. ✅ Setup signing (for production)
4. ✅ Create first release (v1.0.0)
5. ✅ Share APK link with users

### Continuous Development:

```bash
# Make changes
edit androstream/main.py

# Commit & push
git add .
git commit -m "Fix: improve UI layout"
git push

# Wait for auto-build (~15 min)
# Download new APK from Actions
```

---

## 📚 Resources

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Buildozer Docs**: https://buildozer.readthedocs.io/
- **Workflow Syntax**: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
- **Action Marketplace**: https://github.com/marketplace?type=actions

---

## ✅ Checklist

Setup GitHub Actions:
- [ ] Create GitHub repository
- [ ] Run `setup_github.bat` or `setup_github.sh`
- [ ] Push code to GitHub
- [ ] Wait for build (~15-20 min)
- [ ] Download APK from Artifacts
- [ ] Test APK on Android device
- [ ] Create release tag (optional)
- [ ] Share APK with users

---

**🎉 Selamat! Anda sudah punya automatic APK builder di cloud!**

**No WSL, no hassle - just push and download! 🚀**
