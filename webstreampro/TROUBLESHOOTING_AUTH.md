# Troubleshooting Authentication Issues

## Common Authentication Errors and Solutions

### 1. Redirect URI Mismatch Error

**Error Message:**
```
redirect_uri_mismatch
```

**Cause:** The redirect URI in your Google Cloud Console doesn't match the one used by the application.

**Solution:**

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. Go to "APIs & Services" > "Credentials"
4. Click on your OAuth 2.0 Client ID
5. Under "Authorized redirect URIs", add:
   ```
   http://localhost:3000/api/auth/callback
   ```
6. If you changed the PORT in .env, use that port instead:
   ```
   http://localhost:YOUR_PORT/api/auth/callback
   ```
7. Click "Save"
8. Wait a few minutes for changes to propagate
9. Try logging in again

**Important Notes:**
- The redirect URI is case-sensitive
- Must include the full path: `/api/auth/callback`
- Must match the port number in your .env file
- For production with custom domain, add: `https://yourdomain.com/api/auth/callback`

### 2. Invalid Client Error

**Error Message:**
```
invalid_client
```

**Cause:** The client_secret.json file is invalid or doesn't match the project.

**Solution:**

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. Go to "APIs & Services" > "Credentials"
4. Make sure you have an OAuth 2.0 Client ID for "Web application" type
5. Download the JSON file again
6. Upload it in the web interface
7. Try logging in again

**Important Notes:**
- Make sure you're using the correct OAuth client type: **Web application**
- Don't use "Desktop app" or "iOS" client types
- The JSON file must be named `client_secret.json`

### 3. Authorization Code Expired

**Error Message:**
```
invalid_grant: Authorization code expired
```

**Cause:** You took too long to complete the OAuth flow, or the code was already used.

**Solution:**

1. Simply try logging in again
2. Complete the OAuth flow quickly (within a few minutes)
3. Don't refresh the callback page

### 4. Access Denied

**Error Message:**
```
Access denied
```

**Cause:** You denied permissions during the OAuth consent screen.

**Solution:**

1. Click "Login with Google" again
2. This time, click "Allow" to grant all requested permissions
3. The app needs these permissions to manage YouTube:
   - View your YouTube account
   - Manage your YouTube videos
   - Manage your YouTube broadcasts

### 5. OAuth2 Client Not Initialized

**Error Message:**
```
OAuth2 client not initialized. Please upload client_secret.json first.
```

**Cause:** You tried to login without uploading client_secret.json first.

**Solution:**

1. Upload your `client_secret.json` file first
2. Wait for the success message
3. Then click "Login with Google"

### 6. No YouTube Channels Found

**Error Message:**
```
No YouTube channels found. Please create a channel first at youtube.com
```

**Cause:** Your Google account doesn't have any YouTube channels.

**Solution:**

1. Go to [YouTube.com](https://youtube.com)
2. Sign in with the same Google account
3. Create a channel if you don't have one
4. Wait a few minutes
5. Try logging in to WebStreamPro again

### 7. YouTube Data API Not Enabled

**Error Message:**
```
Access Not Configured. YouTube Data API has not been used...
```

**Cause:** YouTube Data API v3 is not enabled in your Google Cloud project.

**Solution:**

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project
3. Go to "APIs & Services" > "Library"
4. Search for "YouTube Data API v3"
5. Click on it and click "ENABLE"
6. Wait a few minutes
7. Try logging in again

### 8. Quota Exceeded

**Error Message:**
```
quotaExceeded
```

**Cause:** You've exceeded your daily YouTube API quota.

**Solution:**

1. YouTube Data API has a daily quota limit
2. By default, it's 10,000 units per day
3. Wait until the next day (resets at midnight Pacific Time)
4. Or request a quota increase in Google Cloud Console

## Setting Up Google Cloud Console Properly

### Step-by-Step Setup:

1. **Create/Select Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select existing one

2. **Enable YouTube Data API v3**
   - Go to "APIs & Services" > "Library"
   - Search "YouTube Data API v3"
   - Click "ENABLE"

3. **Create OAuth Consent Screen**
   - Go to "APIs & Services" > "OAuth consent screen"
   - Choose "External" (unless you have Google Workspace)
   - Fill in required fields:
     - App name: WebStreamPro
     - User support email: your email
     - Developer contact: your email
   - Click "Save and Continue"
   - Add scopes (optional for testing)
   - Add test users (your email)
   - Click "Save and Continue"

4. **Create OAuth 2.0 Client ID**
   - Go to "APIs & Services" > "Credentials"
   - Click "+ CREATE CREDENTIALS"
   - Select "OAuth client ID"
   - Choose "Web application"
   - Name it: WebStreamPro
   - Under "Authorized redirect URIs", add:
     ```
     http://localhost:3000/api/auth/callback
     ```
   - Click "CREATE"
   - Download the JSON file

5. **Upload to WebStreamPro**
   - Open WebStreamPro in browser
   - Upload the downloaded JSON file
   - Click "Login with Google"

## Checking Logs

If you're still having issues, check the server logs:

```bash
pm2 logs webstreampro
```

Look for lines starting with `[AUTH]` to see detailed error messages.

## Testing with Different Port

If you need to use a different port:

1. Edit `.env` file:
   ```
   PORT=8080
   ```

2. Update Google Cloud Console redirect URI:
   ```
   http://localhost:8080/api/auth/callback
   ```

3. Restart the application:
   ```bash
   pm2 restart webstreampro
   ```

## Production Deployment

For production with a domain:

1. Use HTTPS (required for OAuth in production)
2. Set up reverse proxy (Nginx/Apache)
3. Add production redirect URI in Google Cloud Console:
   ```
   https://yourdomain.com/api/auth/callback
   ```
4. Update OAuth consent screen to "Production"

## Still Having Issues?

If none of these solutions work:

1. Check server logs: `pm2 logs webstreampro`
2. Check browser console for JavaScript errors
3. Try with a different browser
4. Clear browser cache and cookies
5. Make sure your Google account has 2FA enabled if required by your organization
6. Try creating a new OAuth client in Google Cloud Console

## Support

For additional help, refer to:
- Google OAuth2 Documentation: https://developers.google.com/identity/protocols/oauth2
- YouTube Data API Documentation: https://developers.google.com/youtube/v3
