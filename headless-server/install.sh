#!/bin/bash
# Installation script for YTLive Headless Server on Ubuntu

set -e

echo "============================================="
echo "YTLive Headless Server - Installation"
echo "============================================="
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root (use sudo)"
    exit 1
fi

# Variables
INSTALL_DIR="/opt/ytlive-server"
SERVICE_USER="ytlive"
SERVICE_FILE="ytlive-scheduler.service"
LOG_DIR="/var/log/ytlive"

echo "[1/8] Installing system dependencies..."
apt-get update
apt-get install -y python3 python3-pip python3-venv

echo
echo "[2/8] Creating service user..."
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd -r -s /bin/false -d "$INSTALL_DIR" "$SERVICE_USER"
    echo "✓ User $SERVICE_USER created"
else
    echo "✓ User $SERVICE_USER already exists"
fi

echo
echo "[3/8] Creating installation directory..."
mkdir -p "$INSTALL_DIR"
mkdir -p "$LOG_DIR"

echo
echo "[4/8] Copying files..."
cp -r . "$INSTALL_DIR/"
chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"
chown -R "$SERVICE_USER:$SERVICE_USER" "$LOG_DIR"

echo
echo "[5/8] Creating Python virtual environment..."
cd "$INSTALL_DIR"
python3 -m venv venv
chown -R "$SERVICE_USER:$SERVICE_USER" venv

echo
echo "[6/8] Installing Python dependencies..."
sudo -u "$SERVICE_USER" "$INSTALL_DIR/venv/bin/pip" install -r requirements.txt

echo
echo "[7/8] Making scripts executable..."
chmod +x "$INSTALL_DIR/ytlive-cli.py"
chmod +x "$INSTALL_DIR/scheduler_daemon.py"

# Create symlink for CLI
ln -sf "$INSTALL_DIR/ytlive-cli.py" /usr/local/bin/ytlive

echo
echo "[8/8] Installing systemd service..."
cp "$INSTALL_DIR/$SERVICE_FILE" /etc/systemd/system/
systemctl daemon-reload

echo
echo "============================================="
echo "Installation Complete!"
echo "============================================="
echo
echo "Next steps:"
echo
echo "1. Authenticate (run this on a machine with browser):"
echo "   sudo -u $SERVICE_USER $INSTALL_DIR/venv/bin/python3 $INSTALL_DIR/ytlive-cli.py auth --new"
echo
echo "   OR copy your token file to:"
echo "   $INSTALL_DIR/data/tokens/"
echo
echo "2. Start the daemon:"
echo "   systemctl start ytlive-scheduler"
echo
echo "3. Enable auto-start on boot:"
echo "   systemctl enable ytlive-scheduler"
echo
echo "4. Check status:"
echo "   systemctl status ytlive-scheduler"
echo
echo "5. View logs:"
echo "   journalctl -u ytlive-scheduler -f"
echo "   OR"
echo "   tail -f $LOG_DIR/daemon.log"
echo
echo "CLI usage:"
echo "   ytlive auth --status              # Check authentication"
echo "   ytlive create /path/to/file.xlsx  # Create broadcasts"
echo "   ytlive schedule /path/to/file.xlsx --time 2025-11-20T10:00:00"
echo "   ytlive list                       # List scheduled tasks"
echo "   ytlive daemon                     # Check daemon status"
echo
echo "============================================="
