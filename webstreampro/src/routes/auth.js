const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs').promises;
const config = require('../utils/config');

const storage = multer.diskStorage({
  destination: async (req, file, cb) => {
    await fs.mkdir(config.PATHS.DATA_DIR, { recursive: true });
    cb(null, config.PATHS.DATA_DIR);
  },
  filename: (req, file, cb) => {
    cb(null, 'client_secret.json');
  }
});

const upload = multer({ storage });

module.exports = (authService) => {
  router.post('/upload-client-secret', upload.single('clientSecret'), async (req, res) => {
    try {
      if (!req.file) {
        return res.status(400).json({ success: false, error: 'No file uploaded' });
      }

      const result = await authService.initOAuth2Client();
      if (result) {
        res.json({ success: true, message: 'Client secret uploaded successfully' });
      } else {
        res.status(400).json({ success: false, error: 'Invalid client secret file' });
      }
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.get('/login', async (req, res) => {
    try {
      // Make sure OAuth2 client is initialized
      if (!authService.oauth2Client) {
        const initialized = await authService.initOAuth2Client();
        if (!initialized) {
          return res.status(400).json({ 
            success: false, 
            error: 'OAuth2 client not initialized. Please upload client_secret.json first.' 
          });
        }
      }
      
      const authUrl = authService.getAuthUrl();
      res.json({ success: true, authUrl });
    } catch (error) {
      console.error('[ROUTE] Login error:', error);
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.get('/callback', async (req, res) => {
    try {
      const { code, error } = req.query;
      
      // Handle OAuth error from Google
      if (error) {
        console.error('[ROUTE] OAuth error from Google:', error);
        return res.redirect('/?auth=failed&error=' + encodeURIComponent(
          error === 'access_denied' 
            ? 'Access denied. You must grant permissions to use this application.' 
            : error
        ));
      }
      
      if (!code) {
        console.error('[ROUTE] No authorization code provided');
        return res.redirect('/?auth=failed&error=' + encodeURIComponent('Authorization code not provided'));
      }

      console.log('[ROUTE] Processing OAuth callback...');
      const result = await authService.handleAuthCallback(code);
      
      if (result.success) {
        req.session.authenticated = true;
        req.session.accountId = authService.currentAccountId;
        console.log('[ROUTE] Authentication successful, redirecting...');
        res.redirect('/?auth=success');
      } else {
        console.error('[ROUTE] Authentication failed:', result.error);
        res.redirect('/?auth=failed&error=' + encodeURIComponent(result.error));
      }
    } catch (error) {
      console.error('[ROUTE] Callback error:', error);
      res.redirect('/?auth=failed&error=' + encodeURIComponent(error.message));
    }
  });

  router.get('/status', (req, res) => {
    const isAuth = authService.isAuthenticated();
    res.json({
      authenticated: isAuth,
      accountId: authService.currentAccountId,
      accountEmail: authService.currentAccountEmail,
      channels: authService.allChannels,
      selectedChannelId: authService.selectedChannelId
    });
  });

  router.post('/select-channel', (req, res) => {
    try {
      const { channelId } = req.body;
      authService.setSelectedChannel(channelId);
      res.json({ success: true });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.get('/accounts', async (req, res) => {
    try {
      const accounts = await authService.getAllAccounts();
      res.json({ success: true, accounts });
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.post('/switch-account', async (req, res) => {
    try {
      const { accountId } = req.body;
      const result = await authService.switchAccount(accountId);
      
      if (result.success) {
        req.session.accountId = accountId;
        res.json({ success: true, accountInfo: result.accountInfo });
      } else {
        res.status(400).json({ success: false, error: result.error });
      }
    } catch (error) {
      res.status(500).json({ success: false, error: error.message });
    }
  });

  router.post('/logout', (req, res) => {
    req.session.destroy();
    res.json({ success: true });
  });

  return router;
};
