import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.absolute()

# Data directories
DATA_DIR = BASE_DIR / 'data'
TOKENS_DIR = DATA_DIR / 'tokens'
UPLOADS_DIR = BASE_DIR / 'uploads'
LOGS_DIR = BASE_DIR / 'logs'

# Create directories if not exist
DATA_DIR.mkdir(exist_ok=True)
TOKENS_DIR.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# File paths
CLIENT_SECRET_FILE = DATA_DIR / 'client_secret.json'
ACTIVE_ACCOUNT_FILE = TOKENS_DIR / 'active.json'
SCHEDULED_BATCHES_FILE = DATA_DIR / 'scheduled_batches.json'
SCHEDULED_UPLOADS_FILE = DATA_DIR / 'scheduled_uploads.json'
PID_FILE = BASE_DIR / 'daemon.pid'
LOG_FILE = LOGS_DIR / 'daemon.log'

# YouTube API settings
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]

# Scheduler settings
SCHEDULER_INTERVAL = 60  # Check every 60 seconds
