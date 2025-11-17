# Quick Start Guide - YTLive Headless Server

## Setup Cepat (5 Menit)

### 1. Upload Files ke Server

```bash
# From Windows/Local Computer
scp -r headless-server user@your-ubuntu-server:/tmp/ytlive

# Login to server
ssh user@your-ubuntu-server
```

### 2. Install

```bash
cd /tmp/ytlive
sudo bash install.sh
```

### 3. Authenticate

**Option A: Di komputer lokal (RECOMMENDED)**

```bash
# Di Windows/Local (yang punya browser)
cd headless-server
pip install -r requirements.txt
python ytlive-cli.py auth --new --client-secret client_secret.json
# Browser akan buka, login dan authorize

# Copy token ke server
scp -r data/tokens user@your-server:/tmp/
ssh user@your-server
sudo mv /tmp/tokens/* /opt/ytlive-server/data/tokens/
sudo chown -R ytlive:ytlive /opt/ytlive-server/data/tokens/
```

**Option B: Di server (jika punya GUI)**

```bash
sudo -u ytlive /opt/ytlive-server/venv/bin/python3 /opt/ytlive-server/ytlive-cli.py auth --new --client-secret /path/to/client_secret.json
```

### 4. Start Daemon

```bash
sudo systemctl start ytlive-scheduler
sudo systemctl enable ytlive-scheduler
sudo systemctl status ytlive-scheduler
```

### 5. Test

```bash
# Check auth
ytlive auth --status

# Create broadcasts
ytlive create /path/to/broadcasts.xlsx --preview

# Schedule batch
ytlive schedule /path/to/broadcasts.xlsx --time 2025-11-20T10:00:00

# List scheduled
ytlive list
```

## Commands Cheat Sheet

```bash
# Authentication
ytlive auth --status              # Check auth status
ytlive auth --new                 # New authentication

# Create immediately
ytlive create file.xlsx           # Create now
ytlive create file.xlsx --preview # Preview first

# Schedule
ytlive schedule file.xlsx --time 2025-11-20T10:00:00 --name "My Batch"

# Monitor
ytlive list                       # List scheduled tasks
ytlive daemon                     # Daemon status
systemctl status ytlive-scheduler # Service status

# Logs
tail -f /opt/ytlive-server/logs/daemon.log
journalctl -u ytlive-scheduler -f

# Service control
sudo systemctl start ytlive-scheduler
sudo systemctl stop ytlive-scheduler
sudo systemctl restart ytlive-scheduler
```

## Workflow

1. **Upload Excel file ke server**
   ```bash
   scp broadcasts.xlsx user@server:/tmp/
   ```

2. **Schedule batch**
   ```bash
   ssh user@server
   ytlive schedule /tmp/broadcasts.xlsx --time 2025-11-20T10:00:00
   ```

3. **Monitor**
   ```bash
   ytlive list
   tail -f /var/log/ytlive/daemon.log
   ```

4. **Done!** Daemon akan process otomatis saat waktunya tiba

## Troubleshooting

**Daemon tidak jalan?**
```bash
systemctl status ytlive-scheduler
journalctl -u ytlive-scheduler -n 50
```

**Token expired?**
```bash
ytlive auth --status
# Jika expired, akan auto-refresh
# Jika gagal, re-authenticate
```

**Task tidak diproses?**
```bash
ytlive list  # Check scheduled tasks
ytlive daemon  # Check daemon status
tail -f /opt/ytlive-server/logs/daemon.log  # Check logs
```

## Tips

- **Remote management**: SSH ke server, run `ytlive` commands
- **Multiple schedules**: Bisa schedule banyak batches
- **Auto-start**: Daemon otomatis start saat server reboot
- **Monitoring**: Check logs regularly untuk memastikan semua OK

Baca [README.md](README.md) untuk dokumentasi lengkap!
