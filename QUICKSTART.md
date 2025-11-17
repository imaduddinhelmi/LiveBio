# Quick Start Guide

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Google Cloud Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable **YouTube Data API v3**
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Choose **Desktop App** as application type
6. Download the credentials file as `client_secret.json`

## Run Application

```bash
python main.py
```

## First Time Setup

### Step 1: Authenticate
1. Click **Auth** tab
2. Click "Select client_secret.json" and choose your downloaded file
3. Click "Login with Google"
4. Browser will open - authorize the application
5. After success, you'll see all your channels
6. **Select the channel** you want to use from the dropdown
7. Channel info will be displayed below

### Step 2: Prepare Excel Data
- Use `sample_broadcasts.xlsx` as template
- Fill in your broadcast details
- Required columns: title, description, tags, categoryId, privacyStatus, scheduledStartDate, scheduledStartTime
- Optional columns: thumbnailPath, streamId, streamKey, latency, enableDvr, enableEmbed, recordFromStart, madeForKids, containsSyntheticMedia

### Important Settings:
- **madeForKids**: Set TRUE if content is made for children (under 13)
- **containsSyntheticMedia**: Set TRUE if content contains AI-generated/modified media
- **categoryId**: Choose appropriate category (20=Gaming, 27=Education, 28=Tech, etc.)
- See **CONTENT_SETTINGS_GUIDE.md** for detailed explanation

### Step 3: Process Broadcasts
1. Click **Import & Run** tab
2. Click "Select Excel File"
3. Preview your data
4. Click "Process Batch"
5. Monitor progress in **Logs** tab

### Step 4: View Results
1. Click **Upcoming** tab
2. Click "Refresh" to see all scheduled broadcasts
3. Go to YouTube Studio to see your created live events

### Logout / Switch Account
1. Click **"Logout / Reset"** button in Auth tab (red button)
2. Confirm the logout action
3. Click "Login with Google" again to login with a different account

## YouTube Category IDs

Common category IDs:
- 1 = Film & Animation
- 10 = Music
- 20 = Gaming
- 22 = People & Blogs
- 24 = Entertainment
- 25 = News & Politics
- 26 = Howto & Style
- 27 = Education
- 28 = Science & Technology

## Troubleshooting

### Authentication Fails
- Make sure you selected correct client_secret.json
- Check that YouTube Data API v3 is enabled
- Verify OAuth consent screen is configured

### Broadcast Creation Fails
- Ensure your account can create live broadcasts
- Check Excel data format matches requirements
- Verify scheduled times are in future

### Thumbnail Upload Fails
- Make sure file path exists
- Check file is valid image format (JPG, PNG)
- Ensure file size is under 2MB
