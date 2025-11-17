# Testing Multi-Channel Detection

## How It Works

The application now fetches channels from TWO sources:

1. **Owned Channels** (`mine=True`)
   - Channels that you directly own with your Google account
   
2. **Managed Channels** (`managedByMe=True`)
   - Brand accounts connected to your Google account
   - Channels you manage but don't directly own
   - Additional channels linked to your account

## Expected Behavior

- During login, the app will query both sources
- Duplicates are automatically removed (based on channel ID)
- All unique channels will appear in the dropdown selector

## If You Still See Only 1 Channel

Possible reasons:

1. **Account Permissions**: Your Google account may only have access to 1 channel
   - Check YouTube Studio at https://studio.youtube.com
   - Click your profile icon → "Switch account" to see all available channels
   
2. **API Scope Limitations**: 
   - The OAuth scope used is: `https://www.googleapis.com/auth/youtube`
   - This should grant access to all channels, but verify in Google Account permissions
   
3. **Brand Account Not Linked**:
   - Brand accounts must be properly linked to your Google account
   - Visit https://myaccount.google.com/brandaccounts to manage brand accounts
   
4. **API Response Check**:
   - Check the Logs tab after login
   - Look for messages: "Found X channel(s) total"
   - This shows how many channels were detected

## Debugging Steps

1. **Check Logs Tab**:
   - After login, check for "Found X channel(s) total"
   - Look for any error messages about fetching channels
   
2. **Verify in YouTube Studio**:
   - Open https://studio.youtube.com
   - Click profile icon → "Switch account"
   - Count how many channels you can switch to
   
3. **Check Console Output**:
   - If running from command line, check for error messages:
     - "Error fetching owned channels: ..."
     - "Error fetching managed channels: ..."

4. **Re-authenticate**:
   - Click "Logout / Reset" button
   - Login again to refresh permissions
   - Check if more channels appear

## Contact

If you have 3 channels in YouTube Studio but only 1 appears in the app, please check:
- The Logs tab for error messages
- Your Google account's brand accounts settings
- YouTube Studio's channel switcher to confirm all 3 are accessible
