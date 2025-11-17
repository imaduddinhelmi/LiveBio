# YT Live Auto Studio

Desktop application for automatically creating and managing YouTube Live broadcasts using Excel data.

## Features

- OAuth2 authentication with Google
- **Multi-channel support** - Select from multiple YouTube channels (owned + managed/brand accounts)
- Import broadcast data from Excel files
- Automatically create YouTube Live broadcasts
- Set up live streams and bind them to broadcasts
- Upload thumbnails
- View upcoming broadcasts
- Real-time activity logs

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup

1. Create a Google Cloud Console project
2. Enable YouTube Data API v3
3. Create OAuth 2.0 credentials (Desktop App)
4. Download the `client_secret.json` file

## Usage

1. Run the application:
```bash
python main.py
```

2. In the **Auth** tab:
   - Select your `client_secret.json` file
   - Click "Login with Google"
   - Complete the OAuth flow in your browser

3. In the **Import & Run** tab:
   - Select your Excel file with broadcast data
   - Preview the data
   - Click "Process Batch" to create all broadcasts

4. In the **Upcoming** tab:
   - View all upcoming broadcasts
   - Click "Refresh" to update the list

5. In the **Logs** tab:
   - Monitor real-time processing logs

## Excel Format

Required columns:
- `title`: Broadcast title
- `description`: Broadcast description
- `tags`: Comma-separated tags
- `categoryId`: YouTube category ID (e.g., 20 for Gaming)
- `privacyStatus`: public, unlisted, or private

Optional columns (with defaults):
- `scheduledStartDate`: Format YYYY-MM-DD (can be left empty - set in app during import)
- `scheduledStartTime`: Format HH:MM 24-hour (can be left empty - set in app during import)
- `thumbnailPath`: Path to thumbnail image
- `streamId`: Existing stream ID to reuse (leave empty to create new)
- `streamKey`: Custom stream name/key (leave empty for auto-generated)
- `latency`: normal, low, ultraLow (default: normal)
- `enableDvr`: TRUE/FALSE (default: TRUE)
- `enableEmbed`: TRUE/FALSE (default: TRUE)
- `recordFromStart`: TRUE/FALSE (default: TRUE)
- `madeForKids`: TRUE/FALSE - Content made for children (default: FALSE)
- `containsSyntheticMedia`: TRUE/FALSE - Content contains AI/synthetic media (default: FALSE)
- `enableMonetization`: TRUE/FALSE - Enable monetization for monetized channels (default: FALSE)

## Notes

- Tokens are stored in `~/.ytlive/token.json`
- All times are in your local timezone
- Make sure your Google account has access to create YouTube broadcasts
