# WebStreamPro - Project Summary

## Overview

WebStreamPro adalah versi web dari aplikasi AutoLiveBio yang memungkinkan pengelolaan YouTube Live broadcasts dan video uploads melalui web browser. Aplikasi ini dapat dijalankan menggunakan PM2 untuk production deployment.

## Technology Stack

### Backend
- **Node.js**: Runtime environment
- **Express.js**: Web framework
- **Google APIs**: YouTube Data API v3 integration
- **node-cron**: Task scheduling
- **xlsx**: Excel file parsing
- **multer**: File upload handling
- **express-session**: Session management

### Frontend
- **HTML5**: Markup
- **CSS3**: Styling (with gradients and modern UI)
- **Vanilla JavaScript**: Client-side logic
- **Fetch API**: AJAX requests

### Deployment
- **PM2**: Process management
- **Ecosystem Config**: PM2 configuration

## Project Structure

```
webstreampro/
├── src/
│   ├── services/              # Business logic layer
│   │   ├── AuthService.js     # OAuth2 & account management
│   │   ├── YouTubeService.js  # YouTube API wrapper
│   │   ├── VideoUploader.js   # Video upload & scheduling
│   │   └── BatchScheduler.js  # Batch processing & cron jobs
│   ├── routes/                # API endpoints
│   │   ├── auth.js            # Authentication routes
│   │   ├── broadcasts.js      # Broadcast management routes
│   │   └── videos.js          # Video upload routes
│   ├── middleware/            # Express middleware
│   │   └── auth.js            # Authentication middleware
│   └── utils/                 # Utilities
│       ├── config.js          # Application configuration
│       └── excelParser.js     # Excel parsing logic
├── public/                    # Static files (Frontend)
│   ├── css/
│   │   └── style.css          # Application styles
│   ├── js/
│   │   └── app.js             # Frontend JavaScript
│   └── index.html             # Main UI
├── data/                      # Data storage
│   ├── tokens/                # OAuth tokens storage
│   ├── client_secret.json     # Google OAuth credentials
│   ├── scheduled_uploads.json # Scheduled video uploads
│   └── scheduled_batches.json # Scheduled batch jobs
├── uploads/                   # Temporary file uploads
├── logs/                      # PM2 logs
├── server.js                  # Application entry point
├── ecosystem.config.js        # PM2 configuration
├── package.json               # Dependencies
├── .env                       # Environment variables
├── README.md                  # Full documentation
├── QUICK_START.md             # Quick start guide
├── CHANGELOG.md               # Version history
├── SAMPLE_EXCEL_FORMAT.md     # Excel format documentation
├── INSTALL.bat                # Installation script
├── START.bat                  # Start application script
└── STOP.bat                   # Stop application script
```

## Key Features

### 1. Authentication & Multi-Account
- Google OAuth2 flow
- Multiple YouTube account support
- Channel selection
- Session persistence
- Token storage and refresh

### 2. Broadcast Management
- Import from Excel files
- Batch creation (immediate or scheduled)
- Custom stream configuration
- Thumbnail upload
- Monetization settings
- Synthetic media declaration

### 3. Video Upload
- Direct video upload
- Scheduled video upload
- Thumbnail support
- Progress tracking
- Metadata configuration
- Privacy settings

### 4. Scheduling System
- Cron-based scheduler
- Batch processing
- Scheduled video uploads
- Task cancellation
- Status monitoring

### 5. Web Interface
- Responsive design
- Tab-based navigation
- Real-time alerts
- Progress indicators
- Modal dialogs
- Form validation

## API Architecture

### REST API Endpoints

**Authentication:**
- POST `/api/auth/upload-client-secret`
- GET `/api/auth/login`
- GET `/api/auth/callback`
- GET `/api/auth/status`
- POST `/api/auth/select-channel`
- POST `/api/auth/switch-account`
- POST `/api/auth/logout`

**Broadcasts:**
- POST `/api/broadcasts/parse-excel`
- POST `/api/broadcasts/create`
- POST `/api/broadcasts/create-batch`
- POST `/api/broadcasts/schedule-batch`
- GET `/api/broadcasts/scheduled-batches`
- POST `/api/broadcasts/cancel-batch/:id`
- GET `/api/broadcasts/upcoming`

**Videos:**
- POST `/api/videos/upload`
- POST `/api/videos/schedule-upload`
- GET `/api/videos/scheduled-uploads`
- POST `/api/videos/cancel-upload/:index`

## Data Flow

### 1. Authentication Flow
```
User -> Upload client_secret.json
     -> Click Login
     -> Redirect to Google OAuth
     -> Grant permissions
     -> Callback to app
     -> Store tokens
     -> Load channels
     -> Select active channel
```

### 2. Batch Broadcast Creation Flow
```
User -> Upload Excel file
     -> Parse Excel (extract broadcast data)
     -> Preview broadcasts
     -> User confirms
     -> Create broadcasts via YouTube API
     -> Upload thumbnails (if provided)
     -> Return results
```

### 3. Scheduled Batch Flow
```
User -> Upload Excel file
     -> Parse Excel
     -> Set schedule time
     -> Save to scheduled_batches.json
     -> Setup cron job
     -> Cron triggers at scheduled time
     -> Process batch creation
     -> Update status
```

### 4. Video Upload Flow
```
User -> Select video file
     -> Fill metadata
     -> Upload (immediate or scheduled)
     -> Store file in uploads/
     -> Upload to YouTube via API
     -> Upload thumbnail (if provided)
     -> Clean up temporary files
```

## Configuration

### Environment Variables (.env)
```env
PORT=3000
SESSION_SECRET=your-secret-key
NODE_ENV=production
```

### PM2 Configuration (ecosystem.config.js)
```javascript
{
  name: 'webstreampro',
  script: './server.js',
  instances: 1,
  autorestart: true,
  watch: false,
  max_memory_restart: '1G'
}
```

## Security Considerations

1. **OAuth Tokens**: Stored in data/tokens/ directory (should be in .gitignore)
2. **Session Secret**: Should be changed from default in production
3. **HTTPS**: Should use HTTPS in production (via reverse proxy)
4. **File Upload**: Limited file sizes and types
5. **Authentication**: Required for all API endpoints (except auth endpoints)

## Performance Considerations

1. **File Uploads**: Large video files may take time
2. **Batch Processing**: Processes broadcasts sequentially
3. **YouTube API**: Subject to quota limits
4. **PM2**: Single instance (can be scaled if needed)
5. **Memory**: Configured with 1GB max memory restart

## Deployment Options

### 1. Local Development
```bash
npm run dev
```

### 2. Production with PM2
```bash
npm run pm2:start
```

### 3. Production with Auto-Start
```bash
pm2 startup
pm2 save
```

### 4. Behind Reverse Proxy (Nginx)
```nginx
location / {
    proxy_pass http://localhost:3000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
}
```

## Future Enhancements

1. **WebSocket**: Real-time updates without polling
2. **Better Progress**: Real-time upload progress
3. **Drag & Drop**: Improved file upload UX
4. **Dark Mode**: UI theme options
5. **Export Logs**: Download logs functionality
6. **Email Notifications**: Alert on task completion
7. **Analytics Dashboard**: Stats and insights
8. **Video Queue**: Queue management for uploads
9. **Multi-language**: Internationalization support
10. **Mobile App**: Native mobile applications

## Maintenance

### Logs
- Located in `logs/` directory
- PM2 maintains: `err.log`, `out.log`, `combined.log`
- Use `pm2 logs webstreampro` to view in real-time

### Cleanup
- Regularly clean `uploads/` directory
- Monitor `data/` directory size
- Rotate logs if they grow too large

### Updates
- Pull latest code
- Run `npm install` for new dependencies
- Restart with `pm2 restart webstreampro`

## Support & Documentation

- **README.md**: Full documentation
- **QUICK_START.md**: Quick setup guide
- **SAMPLE_EXCEL_FORMAT.md**: Excel format guide
- **CHANGELOG.md**: Version history

## License

MIT License

## Credits

Based on AutoLiveBio desktop application, adapted for web deployment with PM2 support.
