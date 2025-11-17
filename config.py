import os
from pathlib import Path

APP_NAME = "YT Live Auto Studio"
APP_VERSION = "1.0.0"

TOKEN_DIR = Path.home() / ".ytlive"
TOKEN_FILE = TOKEN_DIR / "token.json"

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube"]

EXCEL_REQUIRED_COLUMNS = [
    "title",
    "description",
    "tags",
    "categoryId",
    "privacyStatus"
]

EXCEL_OPTIONAL_COLUMNS = {
    "scheduledStartDate": None,
    "scheduledStartTime": None,
    "thumbnailPath": None,
    "streamId": None,
    "streamKey": None,
    "latency": "normal",
    "enableDvr": True,
    "enableEmbed": True,
    "recordFromStart": True,
    "madeForKids": False,
    "containsSyntheticMedia": False,
    "enableMonetization": False
}

os.makedirs(TOKEN_DIR, exist_ok=True)
