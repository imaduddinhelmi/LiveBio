# 🤖 Build APK Otomatis dengan GitHub Actions

## Overview

GitHub Actions bisa build APK secara otomatis di cloud (gratis) setiap kali Anda push code. Tidak perlu install WSL atau dependencies lokal.

---

## Setup GitHub Actions

### Step 1: Buat Workflow File

Buat file `.github/workflows/android-build.yml` di root project:

```yaml
name: Build Android APK

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]
  workflow_dispatch:  # Manual trigger

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install system dependencies
      run: |
        sudo apt-get update
        sudo apt-get install -y openjdk-17-jdk zip unzip \
          autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
          libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    
    - name: Install Buildozer
      run: |
        pip install --upgrade pip
        pip install buildozer cython
    
    - name: Cache Buildozer directories
      uses: actions/cache@v3
      with:
        path: |
          ~/.buildozer
          .buildozer
        key: ${{ runner.os }}-buildozer-${{ hashFiles('**/buildozer.spec') }}
        restore-keys: |
          ${{ runner.os }}-buildozer-
    
    - name: Build APK
      working-directory: ./androstream
      run: |
        buildozer android debug
    
    - name: Upload APK
      uses: actions/upload-artifact@v3
      with:
        name: AndroStream-APK
        path: androstream/bin/*.apk
        retention-days: 30
    
    - name: Create Release (on tag)
      if: startsWith(github.ref, 'refs/tags/')
      uses: softprops/action-gh-release@v1
      with:
        files: androstream/bin/*.apk
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Step 2: Push ke GitHub

```bash
# Initialize git (jika belum)
git init
git add .
git commit -m "Add Android version with GitHub Actions"

# Add remote (ganti dengan repo Anda)
git remote add origin https://github.com/username/AutoLiveBio.git

# Push
git branch -M main
git push -u origin main
```

### Step 3: Monitor Build

1. Buka GitHub repository Anda
2. Klik tab **Actions**
3. Lihat workflow "Build Android APK" running
4. Tunggu ~15-20 menit (first build)
5. Download APK dari **Artifacts**

---

## Download APK dari GitHub Actions

### Via Web:

1. Buka repo → **Actions** tab
2. Klik workflow run yang sudah selesai
3. Scroll ke bawah → **Artifacts**
4. Download **AndroStream-APK.zip**
5. Extract ZIP → dapat file APK

### Via GitHub CLI:

```bash
# Install GitHub CLI
# Windows: winget install GitHub.cli

# Login
gh auth login

# List artifacts
gh run list --workflow=android-build.yml

# Download latest artifact
gh run download --name AndroStream-APK
```

---

## Advanced Configuration

### Build on Tag (Release)

```yaml
name: Release APK

on:
  push:
    tags:
      - 'v*'  # Trigger on version tags (v1.0.0, v1.1.0, etc)

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      # ... (sama seperti di atas)
      
      - name: Build Release APK
        working-directory: ./androstream
        run: |
          buildozer android release
      
      - name: Sign APK
        run: |
          # Add signing configuration here
          # Or sign manually after download
      
      - name: Create GitHub Release
        uses: softprops/action-gh-release@v1
        with:
          files: androstream/bin/*.apk
          draft: false
          prerelease: false
```

### Trigger cara:

```bash
# Tag version
git tag v1.0.0
git push origin v1.0.0

# GitHub Actions akan auto-build dan create release
```

---

## Build Matrix (Multiple Architectures)

Build untuk beberapa architecture sekaligus:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        arch: [armeabi-v7a, arm64-v8a, x86, x86_64]
    
    steps:
      # ... (steps lainnya)
      
      - name: Build APK for ${{ matrix.arch }}
        working-directory: ./androstream
        run: |
          # Edit buildozer.spec
          sed -i 's/android.archs = .*/android.archs = ${{ matrix.arch }}/' buildozer.spec
          buildozer android debug
      
      - name: Upload APK ${{ matrix.arch }}
        uses: actions/upload-artifact@v3
        with:
          name: AndroStream-${{ matrix.arch }}
          path: androstream/bin/*.apk
```

---

## Caching untuk Build Lebih Cepat

Build pertama: ~15-20 menit  
Build dengan cache: ~5-8 menit

```yaml
- name: Cache Buildozer
  uses: actions/cache@v3
  with:
    path: |
      ~/.buildozer
      .buildozer
    key: buildozer-${{ runner.os }}-${{ hashFiles('**/buildozer.spec') }}
    restore-keys: |
      buildozer-${{ runner.os }}-

- name: Cache pip packages
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: pip-${{ runner.os }}-${{ hashFiles('**/requirements.txt') }}
```

---

## Secrets Configuration

Untuk signing APK, tambahkan secrets di GitHub:

1. Go to repo → **Settings** → **Secrets and variables** → **Actions**
2. Add secrets:
   - `KEYSTORE_FILE` (base64 encoded)
   - `KEYSTORE_PASSWORD`
   - `KEY_ALIAS`
   - `KEY_PASSWORD`

```yaml
- name: Decode keystore
  run: |
    echo "${{ secrets.KEYSTORE_FILE }}" | base64 -d > keystore.jks

- name: Sign APK
  run: |
    jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
      -keystore keystore.jks \
      -storepass "${{ secrets.KEYSTORE_PASSWORD }}" \
      -keypass "${{ secrets.KEY_PASSWORD }}" \
      androstream/bin/*.apk \
      "${{ secrets.KEY_ALIAS }}"
```

---

## Troubleshooting

### Build timeout
```yaml
# Increase timeout (default 360 min)
jobs:
  build:
    timeout-minutes: 120
```

### Out of disk space
```yaml
- name: Free disk space
  run: |
    sudo rm -rf /usr/share/dotnet
    sudo rm -rf /opt/ghc
    sudo rm -rf /usr/local/share/boost
    df -h
```

### Build fails randomly
```yaml
# Retry failed steps
- name: Build APK
  uses: nick-invision/retry@v2
  with:
    timeout_minutes: 60
    max_attempts: 3
    command: cd androstream && buildozer android debug
```

---

## Alternative: GitLab CI

Jika pakai GitLab, buat `.gitlab-ci.yml`:

```yaml
image: python:3.9

stages:
  - build

build_apk:
  stage: build
  before_script:
    - apt-get update
    - apt-get install -y openjdk-17-jdk zip unzip autoconf libtool
    - pip install buildozer cython
  
  script:
    - cd androstream
    - buildozer android debug
  
  artifacts:
    paths:
      - androstream/bin/*.apk
    expire_in: 30 days
  
  only:
    - main
    - tags
```

---

## Summary

### Keuntungan GitHub Actions:
- ✅ **Gratis** untuk public repos
- ✅ **Otomatis** setiap push
- ✅ **Konsisten** (environment yang sama)
- ✅ **Tidak perlu setup lokal**
- ✅ **Download APK** langsung dari web
- ✅ **Multiple builds** parallel

### Kekurangan:
- ❌ Build time tergantung queue GitHub
- ❌ Butuh internet untuk download APK
- ❌ Limited to 2000 minutes/month (free tier)

---

## Resources

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Buildozer CI/CD**: https://buildozer.readthedocs.io/en/latest/
- **Action Marketplace**: https://github.com/marketplace?type=actions

---

**Happy Automated Building! 🤖🚀**
