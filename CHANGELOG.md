# Changelog

## Version 1.1.0 (Current)

### Added
- **Multi-channel support**: Can now view and select from multiple YouTube channels associated with one Google account
- **Logout/Reset feature**: Button to logout and login with a different Google account
- **Stream management**: streamId (reuse existing stream) and streamKey (custom stream name) support
- **Content declaration settings**: madeForKids and containsSyntheticMedia columns
- Channel selector dropdown in Auth tab
- Display of all channels with subscriber count and custom URLs
- Better error logging with detailed messages in batch processing
- Comprehensive guides: STREAM_KEY_GUIDE.md and CONTENT_SETTINGS_GUIDE.md

### Changed
- Updated authentication flow to fetch all available channels
- Improved error handling in batch processing
- Updated sample Excel file with future dates

### Fixed
- **Channel detection**: Now fetches both owned and managed channels (including brand accounts)
- Empty thumbnail path handling
- Unicode character display issues in console output
- Better validation for thumbnail file paths

## Version 1.0.0

### Initial Release
- OAuth2 authentication with Google
- Import broadcast data from Excel files
- Automatically create YouTube Live broadcasts
- Set up live streams and bind them to broadcasts
- Upload thumbnails
- View upcoming broadcasts
- Real-time activity logs
