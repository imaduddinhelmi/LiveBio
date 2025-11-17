# Google Cloud Console Setup Guide

## Quick Setup (5 minutes)

### Step 1: Create/Select Project

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click project dropdown at the top
3. Click "NEW PROJECT"
4. Enter project name: `WebStreamPro` (or your choice)
5. Click "CREATE"
6. Wait for project to be created
7. Make sure the new project is selected

### Step 2: Enable YouTube Data API v3

1. In the left sidebar, click "APIs & Services" → "Library"
2. In the search box, type: `YouTube Data API v3`
3. Click on "YouTube Data API v3"
4. Click the blue "ENABLE" button
5. Wait for it to enable (few seconds)

### Step 3: Configure OAuth Consent Screen

1. In the left sidebar, click "APIs & Services" → "OAuth consent screen"
2. Select "External" user type
3. Click "CREATE"

**Fill in the form:**

| Field | Value |
|-------|-------|
| App name | WebStreamPro |
| User support email | (your email) |
| App logo | (optional - skip) |
| App domain | (optional - skip) |
| Authorized domains | (skip for now) |
| Developer contact | (your email) |

4. Click "SAVE AND CONTINUE"
5. On "Scopes" page, click "SAVE AND CONTINUE" (skip for now)
6. On "Test users" page:
   - Click "+ ADD USERS"
   - Enter your Google email (the one you'll use for YouTube)
   - Click "ADD"
   - Click "SAVE AND CONTINUE"
7. On "Summary" page, click "BACK TO DASHBOARD"

### Step 4: Create OAuth 2.0 Client ID

1. In the left sidebar, click "APIs & Services" → "Credentials"
2. Click "+ CREATE CREDENTIALS" at the top
3. Select "OAuth client ID"
4. For Application type, select "Web application"
5. Name: `WebStreamPro Client`

**Add Authorized redirect URIs:**

6. Click "+ ADD URI" under "Authorized redirect URIs"
7. Enter EXACTLY: `http://localhost:3000/api/auth/callback`
8. If you changed PORT in .env, use that port instead
9. Click "CREATE"

**Download Credentials:**

10. A popup will appear with your client ID and secret
11. Click "DOWNLOAD JSON"
12. Save the file (it will be named something like `client_secret_xxx.json`)
13. Rename it to `client_secret.json` (optional but recommended)

### Step 5: Use in WebStreamPro

1. Open WebStreamPro in browser: `http://localhost:3000`
2. In the Authentication section, click "Choose File"
3. Select the `client_secret.json` file you downloaded
4. Click "Upload"
5. Wait for success message
6. Click "Login with Google"
7. Complete the OAuth flow
8. Select your YouTube channel

## Common Issues

### ❌ Redirect URI Mismatch

**Problem:** Error says redirect URI doesn't match

**Solution:**
- Go back to Credentials page
- Click on your OAuth client
- Make sure you added EXACTLY: `http://localhost:3000/api/auth/callback`
- No trailing slash
- Must match the port in your .env file
- Wait 5 minutes for changes to propagate

### ❌ Access Denied During Login

**Problem:** Can't grant permissions during login

**Solution:**
- Make sure you added yourself as a test user in OAuth consent screen
- Use the same email you added as test user
- If using work/school account, contact your admin

### ❌ YouTube Data API Not Enabled

**Problem:** Error about API not enabled

**Solution:**
- Go to APIs & Services → Library
- Search for "YouTube Data API v3"
- Click "ENABLE"
- Wait a few minutes

## Important Notes

### About OAuth Consent Screen

When you first set up OAuth consent screen in "External" mode with "Testing" status:
- Only test users can login
- You need to add your Google account as a test user
- Maximum 100 test users
- No verification needed for testing

To make it public later:
- Go to OAuth consent screen
- Click "PUBLISH APP"
- May require verification from Google (takes days)

### About Quotas

YouTube Data API has quota limits:
- Default: 10,000 units per day
- Creating a broadcast: ~50 units
- Uploading a video: ~1,600 units
- If you need more, request quota increase in Quotas page

### Security Best Practices

✅ **DO:**
- Keep your `client_secret.json` file private
- Don't commit it to git
- Use environment variables for production
- Enable 2FA on your Google account

❌ **DON'T:**
- Share your client secret publicly
- Use the same credentials for multiple apps
- Leave OAuth in testing mode forever (publish when ready)

## Testing Your Setup

1. After uploading client_secret.json, check browser console for errors
2. Click "Login with Google"
3. You should be redirected to Google
4. Grant all permissions
5. You should be redirected back to WebStreamPro
6. You should see "Authentication successful" message
7. Select your YouTube channel from dropdown

If any step fails, check TROUBLESHOOTING_AUTH.md for solutions.

## Video Tutorial Reference

Visual learners can refer to these Google resources:
- [YouTube API Getting Started](https://developers.google.com/youtube/v3/getting-started)
- [OAuth 2.0 Setup](https://support.google.com/cloud/answer/6158849)

## Next Steps

After successful setup:
1. ✅ Upload Excel file with broadcasts
2. ✅ Create broadcasts
3. ✅ Upload videos
4. ✅ Schedule tasks

Need help? Check:
- README.md - Full documentation
- TROUBLESHOOTING_AUTH.md - Common errors and solutions
- QUICK_START.md - Quick start guide
