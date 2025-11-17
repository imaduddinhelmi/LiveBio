const path = require('path');

const config = {
  PORT: parseInt(process.env.PORT || '3000', 10),
  SESSION_SECRET: process.env.SESSION_SECRET || 'change-this-secret-key',
  NODE_ENV: process.env.NODE_ENV || 'development',
  
  YOUTUBE_API_SCOPES: [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.force-ssl'
  ],
  
  PATHS: {
    DATA_DIR: path.join(__dirname, '../../data'),
    UPLOADS_DIR: path.join(__dirname, '../../uploads'),
    TOKENS_DIR: path.join(__dirname, '../../data/tokens'),
    CLIENT_SECRET: path.join(__dirname, '../../data/client_secret.json')
  },
  
  UPLOAD_LIMITS: {
    FILE_SIZE: 100 * 1024 * 1024 * 1024, // 100GB
    EXCEL_SIZE: 10 * 1024 * 1024, // 10MB
    THUMBNAIL_SIZE: 5 * 1024 * 1024 // 5MB
  }
};

module.exports = config;
