# START HERE - YTLive Headless Server

## 🎯 Tujuan

Versi aplikasi AutoLiveBio yang bisa **jalan di server Ubuntu tanpa GUI**, bahkan ketika Anda tidak remote ke server. Aplikasi berjalan sebagai **background daemon** dan tetap aktif 24/7.

## ✨ Kenapa Butuh Ini?

### Masalah dengan Versi Desktop:
- ❌ Harus ada GUI/Desktop window terbuka
- ❌ Kalau window ditutup, aplikasi stop
- ❌ Tidak bisa jalan di background server
- ❌ Remote desktop harus tetap connect

### Solusi dengan Headless Server:
- ✅ **Jalan di background** sebagai systemd service
- ✅ **Tidak butuh GUI** sama sekali
- ✅ **Tetap jalan** walaupun SSH disconnect
- ✅ **Auto-start** saat server reboot
- ✅ **Lightweight** - minimal resource
- ✅ **Perfect untuk VPS/Cloud**

## 🚀 Quick Start (3 Langkah)

### 1️⃣ Install di Server

```bash
# Upload files ke server
scp -r headless-server user@your-server:/tmp/ytlive

# SSH ke server
ssh user@your-server

# Install
cd /tmp/ytlive
sudo bash install.sh
```

### 2️⃣ Authenticate (Sekali Doang!)

**Option A: Di komputer lokal (RECOMMENDED)**
```bash
# Di Windows/PC lokal
cd headless-server
pip install -r requirements.txt
python ytlive-cli.py auth --new --client-secret client_secret.json
# Login di browser

# Copy token ke server
scp -r data/tokens user@server:/tmp/
ssh user@server
sudo mv /tmp/tokens/* /opt/ytlive-server/data/tokens/
sudo chown -R ytlive:ytlive /opt/ytlive-server/data/tokens/
```

### 3️⃣ Start Daemon

```bash
# Start service
sudo systemctl start ytlive-scheduler
sudo systemctl enable ytlive-scheduler

# Check status
sudo systemctl status ytlive-scheduler

# Done! Daemon sekarang jalan di background
```

## 📋 Cara Pakai

### Schedule Batch dari Excel

```bash
# Upload Excel ke server
scp broadcasts.xlsx user@server:/tmp/

# SSH ke server dan schedule
ssh user@server
ytlive schedule /tmp/broadcasts.xlsx --time 2025-11-20T10:00:00 --name "Morning Batch"

# Check scheduled tasks
ytlive list

# Daemon akan otomatis process saat waktunya tiba!
```

### Create Broadcasts Immediately

```bash
ytlive create /path/to/broadcasts.xlsx --preview
```

### Monitor

```bash
# List scheduled tasks
ytlive list

# Check daemon status
ytlive daemon

# View logs
tail -f /opt/ytlive-server/logs/daemon.log
```

## 🔄 Cara Kerja

```
┌─────────────────────────────────────────┐
│  Anda (via SSH atau logout)             │
│  - Upload Excel                          │
│  - Schedule: ytlive schedule file.xlsx  │
│  - Logout/disconnect                     │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│  Daemon (jalan di background)           │
│  - Check scheduled tasks every 60s      │
│  - Process tasks yang waktunya sudah    │
│  - Create broadcasts via YouTube API    │
│  - Log results                           │
│  - Tetap jalan walau Anda logout! ✨    │
└─────────────────────────────────────────┘
```

## 💡 Skenario Penggunaan

### Skenario 1: Schedule Broadcasts
```bash
# Hari Senin pagi, Anda schedule untuk seminggu
ssh user@server
ytlive schedule monday.xlsx --time 2025-11-18T09:00:00 --name "Monday"
ytlive schedule tuesday.xlsx --time 2025-11-19T09:00:00 --name "Tuesday"
ytlive schedule wednesday.xlsx --time 2025-11-20T09:00:00 --name "Wednesday"
# ... dst

# Logout
exit

# Daemon akan otomatis create broadcasts sesuai jadwal!
# Anda tidak perlu online saat broadcast dibuat!
```

### Skenario 2: Automation
```bash
# Setup cron job untuk auto-schedule
# Misalnya: setiap hari jam 00:00, schedule broadcasts untuk besok
0 0 * * * /usr/local/bin/ytlive schedule /data/tomorrow.xlsx --time $(date -d "tomorrow 09:00" +\%Y-\%m-\%dT\%H:\%M:\%S)
```

### Skenario 3: Multiple Batches
```bash
# Schedule banyak batches sekaligus
ytlive schedule batch1.xlsx --time 2025-11-20T08:00:00 --name "Batch 1"
ytlive schedule batch2.xlsx --time 2025-11-20T12:00:00 --name "Batch 2"
ytlive schedule batch3.xlsx --time 2025-11-20T16:00:00 --name "Batch 3"

# Semua akan diproses otomatis!
```

## 📊 Monitoring & Management

```bash
# Check authentication
ytlive auth --status

# List all scheduled tasks
ytlive list

# Check daemon status
systemctl status ytlive-scheduler

# View real-time logs
journalctl -u ytlive-scheduler -f

# OR
tail -f /var/log/ytlive/daemon.log

# Check disk space
du -sh /opt/ytlive-server/
```

## 🔧 Management Commands

```bash
# Service control
sudo systemctl start ytlive-scheduler    # Start
sudo systemctl stop ytlive-scheduler     # Stop
sudo systemctl restart ytlive-scheduler  # Restart
sudo systemctl status ytlive-scheduler   # Status

# Enable/disable auto-start
sudo systemctl enable ytlive-scheduler   # Auto-start on boot
sudo systemctl disable ytlive-scheduler  # Disable auto-start

# Logs
journalctl -u ytlive-scheduler -n 100    # Last 100 lines
journalctl -u ytlive-scheduler -f        # Follow (real-time)
tail -f /opt/ytlive-server/logs/daemon.log
```

## ⚠️ Penting!

### Authentication
- **Hanya perlu SEKALI** saat setup
- Token disimpan dan di-refresh otomatis
- Jika token expired, daemon akan auto-refresh
- Jika auto-refresh gagal, re-authenticate

### Daemon
- **Auto-start saat server boot**
- **Tetap jalan** walaupun SSH disconnect
- **Check tasks every 60 seconds**
- **Log semua activities**

### Excel Files
- Format Excel sama dengan versi desktop
- Upload ke server via `scp` atau file transfer
- Bisa simpan di `/opt/ytlive-server/uploads/`

## 📚 Dokumentasi Lengkap

- **[README.md](README.md)** - Full documentation
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide
- **[COMPARISON.md](COMPARISON.md)** - Compare Desktop vs Web vs Headless

## 🆘 Troubleshooting

**Daemon tidak start?**
```bash
systemctl status ytlive-scheduler
journalctl -u ytlive-scheduler -n 50
```

**Token expired?**
```bash
ytlive auth --status
# Token akan auto-refresh
# Jika gagal, lihat logs
```

**Task tidak diproses?**
```bash
ytlive list                    # Check tasks
ytlive daemon                  # Check daemon
tail -f /opt/ytlive-server/logs/daemon.log
```

## ✅ Checklist Setup

- [ ] Install di server Ubuntu
- [ ] Authenticate (sekali doang)
- [ ] Start daemon & enable auto-start
- [ ] Test dengan schedule 1 batch
- [ ] Monitor logs untuk pastikan sukses
- [ ] Setup monitoring/alerts (optional)

## 🎉 Done!

Sekarang Anda punya YouTube Live automation yang:
- ✅ Jalan 24/7 di background
- ✅ Tidak butuh GUI
- ✅ Auto-start saat reboot
- ✅ Bisa di-manage via SSH
- ✅ Perfect untuk VPS/Cloud!

**Logout dari SSH? No problem! Daemon tetap jalan! 🚀**
