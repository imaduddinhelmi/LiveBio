# YTLive Headless Server

Versi headless dari AutoLiveBio yang bisa berjalan di server Ubuntu tanpa GUI. Aplikasi berjalan sebagai daemon di background dan tetap aktif walaupun tidak ada remote/GUI.

## Fitur

- ✅ **Headless Operation** - Berjalan tanpa GUI
- ✅ **Background Daemon** - Jalan di background menggunakan systemd
- ✅ **Auto-Start** - Otomatis start saat server boot
- ✅ **CLI Interface** - Command line untuk management
- ✅ **Scheduler** - Otomatis process scheduled tasks
- ✅ **OAuth2 Authentication** - Sekali authenticate, token disimpan
- ✅ **Batch Processing** - Import dari Excel dan create batches
- ✅ **Logging** - Comprehensive logging untuk monitoring

## Persyaratan

- Ubuntu 18.04+ atau Debian-based Linux
- Python 3.8+
- Systemd
- Internet connection

## Instalasi di Server Ubuntu

### 1. Upload Files

Upload semua file di folder `headless-server` ke server Ubuntu Anda:

```bash
# Dari komputer lokal
scp -r headless-server user@your-server:/tmp/ytlive-install

# Atau clone dari git jika sudah di repository
```

### 2. Jalankan Install Script

```bash
ssh user@your-server
cd /tmp/ytlive-install
sudo bash install.sh
```

Script akan:
- Install dependencies (Python, pip, dll)
- Buat user `ytlive`
- Copy files ke `/opt/ytlive-server`
- Install Python packages
- Setup systemd service

### 3. Authentication

**PENTING:** Authentication perlu dilakukan SEKALI, bisa dilakukan dengan 2 cara:

#### Cara 1: Authenticate di Server (butuh browser)

Jika server Anda punya GUI atau Anda bisa SSH dengan X11 forwarding:

```bash
sudo -u ytlive /opt/ytlive-server/venv/bin/python3 /opt/ytlive-server/ytlive-cli.py auth --new --client-secret /path/to/client_secret.json
```

Browser akan terbuka untuk OAuth flow.

#### Cara 2: Authenticate di Komputer Lokal, Copy Token (RECOMMENDED)

**Di komputer lokal (Windows/Mac dengan browser):**

```bash
# Install dependencies
pip install -r requirements.txt

# Authenticate
python ytlive-cli.py auth --new --client-secret client_secret.json
```

Setelah sukses, token akan disimpan di `data/tokens/`.

**Copy token ke server:**

```bash
scp -r data/tokens user@your-server:/tmp/
ssh user@your-server
sudo mv /tmp/tokens/* /opt/ytlive-server/data/tokens/
sudo chown -R ytlive:ytlive /opt/ytlive-server/data/tokens/
```

**Verify di server:**

```bash
sudo -u ytlive /opt/ytlive-server/venv/bin/python3 /opt/ytlive-server/ytlive-cli.py auth --status
```

### 4. Start Daemon

```bash
# Start daemon
sudo systemctl start ytlive-scheduler

# Check status
sudo systemctl status ytlive-scheduler

# Enable auto-start on boot
sudo systemctl enable ytlive-scheduler

# View logs
sudo journalctl -u ytlive-scheduler -f
# OR
tail -f /var/log/ytlive/daemon.log
```

## Penggunaan CLI

CLI tersedia sebagai command `ytlive` setelah instalasi.

### Check Authentication Status

```bash
ytlive auth --status
```

### Create Batch Broadcasts (Immediately)

```bash
ytlive create /path/to/broadcasts.xlsx
```

Dengan preview:

```bash
ytlive create /path/to/broadcasts.xlsx --preview
```

### Schedule Batch Creation

Schedule untuk waktu tertentu:

```bash
ytlive schedule /path/to/broadcasts.xlsx --time 2025-11-20T10:00:00 --name "Morning Batch"
```

Schedule untuk 1 jam dari sekarang (default):

```bash
ytlive schedule /path/to/broadcasts.xlsx --name "Test Batch"
```

### List Scheduled Tasks

```bash
ytlive list
```

### Check Daemon Status

```bash
ytlive daemon
# OR
systemctl status ytlive-scheduler
```

## Cara Kerja

### Architecture

```
┌─────────────────────────────────────┐
│   CLI Interface (ytlive-cli.py)    │
│   - Create broadcasts immediately   │
│   - Schedule tasks                  │
│   - Check status                    │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Scheduled Tasks (JSON files)       │
│  - scheduled_batches.json           │
│  - scheduled_uploads.json           │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  Daemon (scheduler_daemon.py)       │
│  - Runs every 60 seconds            │
│  - Checks scheduled tasks           │
│  - Processes due tasks              │
│  - Logs results                     │
└─────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  YouTube API (youtube_service.py)   │
│  - Create broadcasts                │
│  - Upload videos                    │
│  - Manage streams                   │
└─────────────────────────────────────┘
```

### Workflow

1. **Authenticate** (sekali saja)
   - CLI melakukan OAuth flow
   - Token disimpan di `data/tokens/`
   - Token di-refresh otomatis jika expired

2. **Schedule Tasks**
   - User submit Excel file via CLI
   - Task disimpan di JSON file
   - Daemon akan process saat waktunya tiba

3. **Background Processing**
   - Daemon check tasks setiap 60 detik
   - Jika ada task yang waktunya sudah tiba, diproses
   - Results disimpan ke JSON file
   - Logs ditulis ke file dan systemd journal

4. **Monitoring**
   - Check logs: `journalctl -u ytlive-scheduler -f`
   - Check scheduled tasks: `ytlive list`
   - Check daemon status: `ytlive daemon`

## File Structure

```
/opt/ytlive-server/
├── config.py                 # Configuration
├── auth_headless.py          # Authentication service
├── youtube_service.py        # YouTube API wrapper
├── excel_parser.py           # Excel parser
├── scheduler_daemon.py       # Background daemon
├── ytlive-cli.py            # CLI interface
├── requirements.txt          # Python dependencies
├── ytlive-scheduler.service # Systemd service file
├── data/                     # Data directory
│   ├── tokens/              # OAuth tokens
│   ├── scheduled_batches.json
│   └── scheduled_uploads.json
├── logs/                     # Log files
│   └── daemon.log
└── uploads/                  # Uploaded files

/var/log/ytlive/             # System logs
└── daemon.log

/etc/systemd/system/
└── ytlive-scheduler.service # Service file
```

## Management Commands

### Systemd Service

```bash
# Start
sudo systemctl start ytlive-scheduler

# Stop
sudo systemctl stop ytlive-scheduler

# Restart
sudo systemctl restart ytlive-scheduler

# Status
sudo systemctl status ytlive-scheduler

# Enable auto-start
sudo systemctl enable ytlive-scheduler

# Disable auto-start
sudo systemctl disable ytlive-scheduler

# View logs
sudo journalctl -u ytlive-scheduler -f

# View last 100 lines
sudo journalctl -u ytlive-scheduler -n 100
```

### Manual Daemon Control

```bash
# Start manually (for testing)
sudo -u ytlive /opt/ytlive-server/venv/bin/python3 /opt/ytlive-server/scheduler_daemon.py

# Check PID
cat /opt/ytlive-server/daemon.pid

# Stop manually
kill $(cat /opt/ytlive-server/daemon.pid)
```

### Logs

```bash
# Application logs
tail -f /opt/ytlive-server/logs/daemon.log

# System logs
tail -f /var/log/ytlive/daemon.log

# Systemd journal
journalctl -u ytlive-scheduler -f
```

## Troubleshooting

### Daemon tidak start

```bash
# Check logs
sudo journalctl -u ytlive-scheduler -n 50

# Check authentication
sudo -u ytlive /opt/ytlive-server/venv/bin/python3 /opt/ytlive-server/ytlive-cli.py auth --status

# Check permissions
ls -la /opt/ytlive-server/data/tokens/
```

### Token expired

Token akan di-refresh otomatis. Jika gagal:

```bash
# Re-authenticate
sudo -u ytlive /opt/ytlive-server/venv/bin/python3 /opt/ytlive-server/ytlive-cli.py auth --new
```

### Scheduled task tidak diproses

```bash
# Check daemon status
ytlive daemon
systemctl status ytlive-scheduler

# Check scheduled tasks
ytlive list

# Check logs
tail -f /opt/ytlive-server/logs/daemon.log
```

### Permission denied

```bash
# Fix ownership
sudo chown -R ytlive:ytlive /opt/ytlive-server/
sudo chown -R ytlive:ytlive /var/log/ytlive/
```

## Uninstall

```bash
# Stop and disable service
sudo systemctl stop ytlive-scheduler
sudo systemctl disable ytlive-scheduler

# Remove service file
sudo rm /etc/systemd/system/ytlive-scheduler.service
sudo systemctl daemon-reload

# Remove installation
sudo rm -rf /opt/ytlive-server
sudo rm -rf /var/log/ytlive
sudo rm /usr/local/bin/ytlive

# Remove user (optional)
sudo userdel ytlive
```

## Security Notes

- Service runs as dedicated user `ytlive` (not root)
- Token files are protected (only readable by `ytlive` user)
- Systemd service has security restrictions (ProtectSystem, PrivateTmp, etc.)
- Logs are written to dedicated directory

## Tips

### Remote Access

Anda bisa manage dari komputer lain via SSH:

```bash
ssh user@your-server
ytlive list
ytlive create /path/to/file.xlsx
```

### Upload Excel File ke Server

```bash
# From local computer
scp broadcasts.xlsx user@your-server:/tmp/

# On server
ssh user@your-server
sudo mv /tmp/broadcasts.xlsx /opt/ytlive-server/uploads/
ytlive create /opt/ytlive-server/uploads/broadcasts.xlsx
```

### Monitoring dengan Cron

Setup email notification untuk failed tasks:

```bash
# Add to crontab
crontab -e

# Check for failed tasks every hour
0 * * * * /usr/local/bin/ytlive list | grep "failed" && echo "Failed tasks detected" | mail -s "YTLive Alert" your@email.com
```

### Multiple Instances

Anda bisa run multiple instances untuk different accounts:

1. Copy installation ke directory berbeda
2. Modify config.py untuk path berbeda
3. Create separate systemd service

## Support

For issues or questions:
- Check logs first
- Verify authentication
- Test with CLI before scheduling
- Ensure daemon is running

## License

MIT
