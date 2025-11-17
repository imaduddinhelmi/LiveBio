# 📤 Push ke Repository Baru - Complete Guide

## 🎯 Overview

Panduan lengkap untuk push project ke repository GitHub yang baru.

---

## ⚡ Quick Start (Paling Mudah!)

### Windows:
```cmd
setup_new_repo.bat
```

### Linux/Mac/WSL:
```bash
chmod +x setup_new_repo.sh
./setup_new_repo.sh
```

**Script akan guide Anda step-by-step!**

---

## 📝 Manual Steps (Jika Script Tidak Work)

### Step 1: Create Repository di GitHub

1. **Buka browser** dan go to: https://github.com/new

2. **Fill in form:**
   - **Repository name**: `AutoLiveBio` (atau nama lain yang Anda suka)
   - **Description**: `YouTube Live & Video Automation (Android + Desktop)`
   - **Visibility**: 
     - **Public** (recommended - unlimited GitHub Actions)
     - **Private** (limited 2000 min/month)
   - **JANGAN centang:**
     - ❌ Add a README file
     - ❌ Add .gitignore
     - ❌ Choose a license

3. **Click**: "Create repository"

4. **Copy URL** yang muncul:
   ```
   https://github.com/username/AutoLiveBio.git
   ```

---

### Step 2: Initialize Git (di Local)

```bash
cd D:\A-YT\YT\AutoLiveBio

# Initialize git (jika belum)
git init
```

---

### Step 3: Create .gitignore

**PENTING:** Protect credentials dan file sensitif!

```bash
# Create .gitignore
notepad .gitignore
```

**Copy-paste ini:**
```gitignore
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
*.token

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Excel with sensitive data
*_custom_time.xlsx
sample_*.xlsx
broadcasts_monetization.xlsx
```

**Save dan close.**

---

### Step 4: Check Sensitive Files

```bash
# Check jika ada file yang tidak boleh di-commit
dir client_secret*.json
dir token.pickle
dir Data\
```

**Jika ada, pastikan sudah ada di .gitignore!**

---

### Step 5: Add Remote

```bash
# Add remote (ganti dengan URL Anda!)
git remote add origin https://github.com/username/AutoLiveBio.git

# Verify
git remote -v
```

---

### Step 6: Stage All Files

```bash
# Add all files
git add .

# Check status
git status
```

**Pastikan file sensitif TIDAK ada di list!**

---

### Step 7: Commit

```bash
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
```

---

### Step 8: Set Main Branch

```bash
git branch -M main
```

---

### Step 9: Push to GitHub

```bash
# Push (first time)
git push -u origin main
```

**Ini akan upload semua files ke GitHub (~5-10 menit tergantung size).**

---

## 🔐 Authentication

### If Push Failed: "Authentication required"

#### Option 1: GitHub Token (Recommended)

1. **Create token:**
   - Go to: https://github.com/settings/tokens
   - Click **"Generate new token"** → **"Classic"**
   - Give name: `AutoLiveBio-Push`
   - Select scopes: **`repo`** (full control)
   - Click **"Generate token"**
   - **COPY TOKEN** (will only show once!)

2. **Use token as password:**
   ```bash
   git push -u origin main
   
   # Username: your-github-username
   # Password: [paste token here]
   ```

3. **Cache credentials** (optional):
   ```bash
   git config --global credential.helper store
   # Next time tidak perlu input lagi
   ```

#### Option 2: SSH Key

1. **Generate SSH key:**
   ```bash
   ssh-keygen -t ed25519 -C "your-email@example.com"
   # Press Enter 3x (default location, no passphrase)
   ```

2. **Copy public key:**
   ```bash
   # Windows
   type %USERPROFILE%\.ssh\id_ed25519.pub
   
   # Linux/Mac
   cat ~/.ssh/id_ed25519.pub
   ```

3. **Add to GitHub:**
   - Go to: https://github.com/settings/keys
   - Click **"New SSH key"**
   - Paste public key
   - Click **"Add SSH key"**

4. **Change remote to SSH:**
   ```bash
   git remote set-url origin git@github.com:username/AutoLiveBio.git
   
   # Push again
   git push -u origin main
   ```

---

## ✅ Verification

### After Successful Push:

1. **Refresh GitHub page** - Should see all files

2. **Check Actions tab:**
   - Click **"Actions"**
   - See **"Build Android APK"** workflow starting
   - This will auto-build APK

3. **Wait for build** (~15-20 minutes)

4. **Download APK:**
   - Go to completed workflow
   - Scroll to **"Artifacts"**
   - Download **"AndroStream-Debug-APK"**

---

## 🐛 Troubleshooting

### Error: "Authentication failed"

**Solutions:**
- Use GitHub token (see above)
- Or setup SSH (see above)
- Check username/password correct

### Error: "Repository not found"

**Solutions:**
- Make sure repository created on GitHub
- Check URL is correct: `git remote -v`
- Check repository visibility (Public/Private)

### Error: "Permission denied"

**Solutions:**
- Check you're the repository owner
- If collaborator, ask owner for write access
- Use correct GitHub account

### Error: "Large files detected"

**Solutions:**
```bash
# Remove large files from staging
git rm --cached path/to/large/file

# Add to .gitignore
echo "path/to/large/file" >> .gitignore

# Commit and push again
git commit -m "Remove large files"
git push
```

### Error: "Sensitive data detected"

**Solutions:**
```bash
# Remove sensitive file
git rm --cached client_secret.json

# Make sure in .gitignore
echo "client_secret*.json" >> .gitignore

# Commit
git commit -m "Remove sensitive data"
git push
```

---

## 📊 What Gets Uploaded

### ✅ Will be uploaded:
- All `.py` files (Python code)
- `.github/workflows/` (GitHub Actions)
- `androstream/` folder (Android app)
- All `.md` files (Documentation)
- `.bat` and `.sh` scripts
- `requirements.txt`
- `buildozer.spec`

### ❌ Will NOT be uploaded (in .gitignore):
- `client_secret*.json` (credentials)
- `token.pickle` (auth tokens)
- `Data/` folder (user data)
- `.buildozer/` and `bin/` (build artifacts)
- `__pycache__/` (Python cache)
- IDE files (`.vscode/`, `.idea/`)

---

## 🎯 After Push - Next Steps

### 1. Monitor GitHub Actions Build

```
1. Go to repository on GitHub
2. Click "Actions" tab
3. See workflow running
4. Click to see logs
5. Wait ~15-20 minutes
6. Download APK from Artifacts
```

### 2. Update README (Optional)

Add build badge to README:

```markdown
![Build APK](https://github.com/username/AutoLiveBio/workflows/Build%20Android%20APK/badge.svg)
```

### 3. Invite Collaborators (If Team Project)

```
Repository → Settings → Collaborators → Add people
```

### 4. Setup Branch Protection (Optional)

```
Settings → Branches → Add rule
- Require pull request reviews
- Require status checks to pass
```

---

## 📚 Repository Structure

Your repository will look like:

```
AutoLiveBio/
├── .github/
│   └── workflows/
│       ├── android-build.yml       # Auto-build APK
│       ├── android-release.yml     # Release workflow
│       └── test-build.yml          # Quick test
│
├── androstream/                    # Android app
│   ├── main.py                     # Kivy app
│   ├── buildozer.spec              # Build config
│   ├── auth.py                     # YouTube auth
│   ├── youtube_service.py          # API wrapper
│   └── ... (other files)
│
├── Documentation files
│   ├── README_BUILD_OPTIONS.md     # Build guide
│   ├── GITHUB_ACTIONS_SETUP.md     # CI/CD guide
│   ├── PUSH_TO_NEW_REPO.md         # This file
│   └── ... (other docs)
│
├── Setup scripts
│   ├── setup_new_repo.bat          # Windows setup
│   ├── setup_new_repo.sh           # Linux/Mac setup
│   ├── fix_build_error.bat         # Fix script
│   └── ... (other scripts)
│
└── Desktop app files
    ├── gui.py                      # Desktop GUI
    ├── main.py                     # Desktop main
    └── ... (other files)
```

---

## 🎉 Success Checklist

After push:
- [ ] Repository visible on GitHub
- [ ] All files uploaded (check)
- [ ] No sensitive data committed (double check!)
- [ ] GitHub Actions starting automatically
- [ ] Build workflow running
- [ ] Can clone repository
- [ ] Documentation readable online
- [ ] ✅ **All done!**

---

## 🆘 Need Help?

### Quick Links:
- **GitHub Docs**: https://docs.github.com/en/get-started
- **Token Setup**: https://github.com/settings/tokens
- **SSH Setup**: https://docs.github.com/en/authentication

### Common Commands:
```bash
# Check remote
git remote -v

# Check status
git status

# Check what will be committed
git diff --cached

# Undo staging
git reset HEAD file.txt

# Change remote URL
git remote set-url origin new-url

# Force push (CAREFUL!)
git push -f origin main
```

---

## 💡 Tips

### For Public Repository:
- ✅ Anyone can see and clone
- ✅ Unlimited GitHub Actions
- ✅ Good for open source
- ⚠️  Never commit sensitive data!

### For Private Repository:
- ✅ Only you and collaborators can see
- ✅ More secure
- ⚠️  Limited GitHub Actions (2000 min/month)
- 💰 Paid plans for more minutes

### Best Practices:
- Always check `.gitignore` first
- Never commit credentials
- Write descriptive commit messages
- Use branches for features
- Test before pushing

---

**Ready to push? Run `setup_new_repo.bat` now! 🚀**
