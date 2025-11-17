require('dotenv').config();
const express = require('express');
const session = require('express-session');
const cookieParser = require('cookie-parser');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const config = require('./src/utils/config');

const AuthService = require('./src/services/AuthService');
const YouTubeService = require('./src/services/YouTubeService');
const VideoUploader = require('./src/services/VideoUploader');
const BatchScheduler = require('./src/services/BatchScheduler');

const app = express();

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(session({
  secret: config.SESSION_SECRET,
  resave: false,
  saveUninitialized: false,
  cookie: { 
    secure: process.env.NODE_ENV === 'production',
    maxAge: 24 * 60 * 60 * 1000
  }
}));

app.use(express.static(path.join(__dirname, 'public')));

const authService = new AuthService();
const youtubeService = new YouTubeService(authService);
const videoUploader = new VideoUploader(youtubeService);
const batchScheduler = new BatchScheduler(youtubeService);

const authRoutes = require('./src/routes/auth')(authService);
const broadcastRoutes = require('./src/routes/broadcasts')(youtubeService, batchScheduler);
const videoRoutes = require('./src/routes/videos')(videoUploader);

app.use('/api/auth', authRoutes);
app.use('/api/broadcasts', broadcastRoutes);
app.use('/api/videos', videoRoutes);

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Serve troubleshooting guide
app.get('/TROUBLESHOOTING_AUTH.md', (req, res) => {
  res.sendFile(path.join(__dirname, 'TROUBLESHOOTING_AUTH.md'));
});

async function initializeApp() {
  try {
    const activeAccountId = await authService.getActiveAccount();
    if (activeAccountId) {
      await authService.initOAuth2Client();
      await authService.loadAccount(activeAccountId);
      console.log('[INFO] Loaded active account:', activeAccountId);
    }
  } catch (error) {
    console.log('[INFO] No active account found');
  }
}

const PORT = config.PORT;

initializeApp().then(() => {
  app.listen(PORT, () => {
    console.log('='.repeat(50));
    console.log('WebStreamPro - YouTube Live Management System');
    console.log('='.repeat(50));
    console.log(`Server running on: http://localhost:${PORT}`);
    console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log('='.repeat(50));
  });
});

process.on('SIGINT', () => {
  console.log('\n[INFO] Shutting down gracefully...');
  batchScheduler.stopAllJobs();
  videoUploader.stopScheduler();
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\n[INFO] Shutting down gracefully...');
  batchScheduler.stopAllJobs();
  videoUploader.stopScheduler();
  process.exit(0);
});

module.exports = app;
