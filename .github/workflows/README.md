# GitHub Actions Workflows

This folder contains automated workflows for building Android APK.

## 📋 Available Workflows

### 1. `android-build.yml` - Automatic Debug Build
**Purpose:** Build debug APK on every push  
**Trigger:** Push to main/master/develop, PR, Manual  
**Duration:** ~15-20 minutes (first time), ~8-15 min (cached)  
**Output:** Debug APK in Artifacts (30 days retention)

**When it runs:**
- You push code to main/master/develop branches
- You create a pull request
- You manually trigger it from Actions tab

**What it does:**
1. Setup Python, Java, and build tools
2. Cache Buildozer directories (speed up future builds)
3. Build debug APK with `buildozer android debug`
4. Upload APK to Artifacts
5. Post build summary

**Download APK:**
- Go to Actions → Select workflow run → Download from Artifacts

---

### 2. `android-release.yml` - Release Build
**Purpose:** Build release APK for distribution  
**Trigger:** Push version tag (v1.0.0), Manual with version  
**Duration:** ~20-25 minutes  
**Output:** Release APK + GitHub Release

**When it runs:**
- You push a version tag: `git tag v1.0.0 && git push origin v1.0.0`
- You manually trigger with version input

**What it does:**
1. Setup build environment
2. Update version in buildozer.spec
3. Build release APK (unsigned)
4. Create release package (APK + docs)
5. Create GitHub Release with download links
6. Upload APK to Release page

**Download APK:**
- Go to Releases → Select version → Download APK

---

### 3. `test-build.yml` - Quick Validation
**Purpose:** Fast validation without full build  
**Trigger:** Pull requests, Manual  
**Duration:** ~3-5 minutes  
**Output:** Validation report (no APK)

**When it runs:**
- You create a pull request
- You manually trigger for quick check

**What it does:**
1. Validate buildozer.spec syntax
2. Check Python files for syntax errors
3. Verify dependencies
4. Report results (no actual build)

**Use case:**
- Quick check before full build
- PR validation
- Syntax verification

---

## 🚀 How to Use

### Automatic Build (Push)
```bash
# Make changes
edit androstream/main.py

# Commit and push
git add .
git commit -m "Update UI"
git push

# Wait for Actions to complete
# Download APK from Actions → Artifacts
```

### Create Release
```bash
# Update version (optional, auto-updated by workflow)
# version = 1.1.0 in buildozer.spec

# Create and push tag
git tag v1.1.0
git push origin v1.1.0

# Workflow will:
# 1. Build release APK
# 2. Create GitHub Release
# 3. Upload APK to release page
```

### Manual Trigger
1. Go to repository on GitHub
2. Click **Actions** tab
3. Select workflow (Build Android APK or Release Android APK)
4. Click **Run workflow** button
5. Select branch / Enter version (for release)
6. Click **Run workflow**

---

## 📥 Download APK

### Method 1: From Artifacts (Debug builds)
1. Go to **Actions** tab
2. Click on completed workflow run
3. Scroll to **Artifacts** section
4. Click **AndroStream-Debug-APK** to download ZIP
5. Extract to get APK

### Method 2: From Releases (Release builds)
1. Go to **Releases** tab
2. Click on version (e.g., v1.0.0)
3. Download APK from **Assets**

### Method 3: GitHub CLI
```bash
# List runs
gh run list --workflow=android-build.yml

# Download artifact
gh run download --name AndroStream-Debug-APK
```

---

## ⚙️ Configuration

### Change Build Triggers

Edit workflow file, modify `on:` section:

```yaml
on:
  push:
    branches: [ main, develop, feature/* ]  # Add more branches
    paths:
      - 'androstream/**'  # Only trigger on androstream changes
```

### Change Cache Settings

```yaml
- name: Cache Buildozer
  uses: actions/cache@v3
  with:
    path: |
      ~/.buildozer
      androstream/.buildozer
    key: buildozer-${{ runner.os }}-${{ hashFiles('androstream/buildozer.spec') }}
```

### Change Artifact Retention

```yaml
- name: Upload APK
  with:
    retention-days: 90  # Change from 30 to 90 days
```

### Add Notifications

Add Slack/Discord notification step:

```yaml
- name: Notify on success
  if: success()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 'APK build successful!'
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

## 🔧 Troubleshooting

### Build Failed

**Check logs:**
1. Actions tab → Click failed run
2. Click job name
3. Expand failed step
4. Read error message

**Common issues:**

**1. Disk space error:**
```yaml
# Add before build:
- name: Free disk space
  run: |
    sudo rm -rf /usr/share/dotnet
    df -h
```

**2. Timeout error:**
```yaml
# Increase timeout:
jobs:
  build:
    timeout-minutes: 180  # from 120
```

**3. Cache corruption:**
- Go to Actions → Caches
- Delete all caches
- Retry build

### Build is Slow

**First build:** Always slow (15-25 min) - downloads SDK/NDK

**Subsequent builds should be faster (8-15 min)**

If still slow:
- Check if cache is working (should see "Cache restored")
- Check GitHub status: https://www.githubstatus.com/
- Try clearing cache and rebuild

### Cannot Download Artifact

**Artifacts expire after retention period (default 30 days)**

Solution:
- Use Release workflow instead (no expiration)
- Increase retention-days in workflow
- Download within retention period

---

## 📊 Build Times

| Build Type | First Build | With Cache | Notes |
|-----------|-------------|------------|-------|
| Debug | 15-25 min | 8-15 min | Most common |
| Release | 20-30 min | 10-18 min | Slower due to optimizations |
| Test | 3-5 min | 2-3 min | No actual build |

---

## 💰 Usage & Costs

### GitHub Free Tier:
- **Public repos:** Unlimited minutes ✅
- **Private repos:** 2,000 minutes/month
- **Storage:** 500MB artifacts

### Estimated Usage:
- **Debug build:** ~20 minutes
- **Release build:** ~25 minutes
- **Test:** ~3 minutes

**100 debug builds/month = 2,000 minutes**

**Tip:** Use public repo for unlimited builds!

---

## 🔐 Secrets (for Signing)

To sign APK automatically, add secrets:

1. Go to repo **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add:
   - `KEYSTORE_FILE` (base64 of keystore.jks)
   - `KEYSTORE_PASSWORD`
   - `KEY_ALIAS`
   - `KEY_PASSWORD`

Create keystore:
```bash
keytool -genkey -v -keystore androstream.jks \
  -alias androstream -keyalg RSA -keysize 2048 -validity 10000
```

Base64 encode:
```bash
base64 androstream.jks | tr -d '\n' | pbcopy  # Mac
base64 -w 0 androstream.jks  # Linux
certutil -encode androstream.jks keystore.txt  # Windows
```

Add signing step to workflow:
```yaml
- name: Sign APK
  run: |
    echo "${{ secrets.KEYSTORE_FILE }}" | base64 -d > keystore.jks
    jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
      -keystore keystore.jks \
      -storepass "${{ secrets.KEYSTORE_PASSWORD }}" \
      -keypass "${{ secrets.KEY_PASSWORD }}" \
      androstream/bin/*.apk \
      "${{ secrets.KEY_ALIAS }}"
```

---

## 📚 Resources

- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **Workflow Syntax:** https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions
- **Buildozer CI/CD:** https://buildozer.readthedocs.io/en/latest/
- **Action Marketplace:** https://github.com/marketplace?type=actions

---

## ✅ Workflow Status

Check status badges (add to main README.md):

```markdown
![Build APK](https://github.com/username/AutoLiveBio/workflows/Build%20Android%20APK/badge.svg)
![Release](https://github.com/username/AutoLiveBio/workflows/Release%20Android%20APK/badge.svg)
```

---

**Happy automating! 🤖**
