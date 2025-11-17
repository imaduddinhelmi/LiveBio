const { google } = require('googleapis');
const fs = require('fs').promises;
const path = require('path');
const config = require('../utils/config');

class AuthService {
  constructor() {
    this.oauth2Client = null;
    this.credentials = null;
    this.currentAccountId = null;
    this.currentAccountEmail = null;
    this.selectedChannelId = null;
    this.allChannels = [];
  }

  async initOAuth2Client() {
    try {
      const clientSecretPath = config.PATHS.CLIENT_SECRET;
      
      // Check if file exists
      try {
        await fs.access(clientSecretPath);
      } catch (error) {
        console.error('Client secret file not found:', clientSecretPath);
        return false;
      }
      
      const content = await fs.readFile(clientSecretPath, 'utf-8');
      const credentials = JSON.parse(content);
      
      // Support both web and installed app types
      let client_secret, client_id, redirect_uris;
      
      if (credentials.web) {
        ({ client_secret, client_id, redirect_uris } = credentials.web);
      } else if (credentials.installed) {
        ({ client_secret, client_id, redirect_uris } = credentials.installed);
      } else {
        console.error('Invalid client_secret.json format. Missing "web" or "installed" key.');
        return false;
      }
      
      if (!client_secret || !client_id) {
        console.error('Invalid client_secret.json: missing client_id or client_secret');
        return false;
      }
      
      // Use explicit redirect URI for web application
      const redirectUri = `http://localhost:${config.PORT}/api/auth/callback`;
      
      console.log('[AUTH] Initializing OAuth2 Client');
      console.log('[AUTH] Redirect URI:', redirectUri);
      console.log('[AUTH] Make sure this URI is added to Google Cloud Console Authorized Redirect URIs');
      
      this.oauth2Client = new google.auth.OAuth2(
        client_id,
        client_secret,
        redirectUri
      );
      
      return true;
    } catch (error) {
      console.error('Error initializing OAuth2 client:', error);
      return false;
    }
  }

  getAuthUrl() {
    if (!this.oauth2Client) {
      throw new Error('OAuth2 client not initialized');
    }

    return this.oauth2Client.generateAuthUrl({
      access_type: 'offline',
      scope: config.YOUTUBE_API_SCOPES,
      prompt: 'consent'
    });
  }

  async handleAuthCallback(code) {
    try {
      console.log('[AUTH] Exchanging code for tokens...');
      
      if (!this.oauth2Client) {
        throw new Error('OAuth2 client not initialized. Please upload client_secret.json first.');
      }
      
      const { tokens } = await this.oauth2Client.getToken(code);
      
      console.log('[AUTH] Tokens received successfully');
      
      this.oauth2Client.setCredentials(tokens);
      this.credentials = tokens;
      
      console.log('[AUTH] Creating YouTube client...');
      
      const youtube = google.youtube({
        version: 'v3',
        auth: this.oauth2Client
      });
      
      console.log('[AUTH] Fetching channels...');
      
      const channels = await this.getAllChannels(youtube);
      
      if (channels.length === 0) {
        console.warn('[AUTH] No channels found for this account');
        return { 
          success: false, 
          error: 'No YouTube channels found. Please create a channel first at youtube.com' 
        };
      }
      
      console.log(`[AUTH] Found ${channels.length} channel(s)`);
      
      this.selectedChannelId = channels[0].id;
      const accountId = this.generateAccountId();
      await this.saveAccount(accountId, channels[0].title, tokens, channels);
      this.currentAccountId = accountId;
      this.currentAccountEmail = channels[0].title;
      
      console.log('[AUTH] Authentication completed successfully');
      
      return { success: true, channels };
    } catch (error) {
      console.error('[AUTH] Error handling auth callback:', error);
      
      // Provide more specific error messages
      let errorMessage = error.message;
      
      if (error.message.includes('invalid_grant')) {
        errorMessage = 'Authorization code expired or invalid. Please try logging in again.';
      } else if (error.message.includes('redirect_uri_mismatch')) {
        errorMessage = 'Redirect URI mismatch. Please check your Google Cloud Console settings.';
      } else if (error.message.includes('invalid_client')) {
        errorMessage = 'Invalid client credentials. Please check your client_secret.json file.';
      }
      
      return { success: false, error: errorMessage };
    }
  }

  async getAllChannels(youtube) {
    const channels = [];
    const channelIdsSeen = new Set();
    
    try {
      const ownedResponse = await youtube.channels.list({
        part: 'snippet,contentDetails,statistics',
        mine: true,
        maxResults: 50
      });
      
      if (ownedResponse.data.items) {
        ownedResponse.data.items.forEach(channel => {
          if (!channelIdsSeen.has(channel.id)) {
            channels.push({
              title: channel.snippet.title,
              id: channel.id,
              subscribers: channel.statistics.subscriberCount || 'N/A',
              customUrl: channel.snippet.customUrl || 'N/A'
            });
            channelIdsSeen.add(channel.id);
          }
        });
      }
    } catch (error) {
      console.error('Error fetching owned channels:', error);
    }
    
    try {
      const managedResponse = await youtube.channels.list({
        part: 'snippet,contentDetails,statistics',
        managedByMe: true,
        maxResults: 50
      });
      
      if (managedResponse.data.items) {
        managedResponse.data.items.forEach(channel => {
          if (!channelIdsSeen.has(channel.id)) {
            channels.push({
              title: channel.snippet.title,
              id: channel.id,
              subscribers: channel.statistics.subscriberCount || 'N/A',
              customUrl: channel.snippet.customUrl || 'N/A'
            });
            channelIdsSeen.add(channel.id);
          }
        });
      }
    } catch (error) {
      console.error('Error fetching managed channels:', error);
    }
    
    this.allChannels = channels;
    return channels;
  }

  generateAccountId() {
    return `account_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  async saveAccount(accountId, accountName, tokens, channels) {
    try {
      await fs.mkdir(config.PATHS.TOKENS_DIR, { recursive: true });
      
      const accountInfo = {
        id: accountId,
        name: accountName,
        email: accountName,
        channels: channels,
        createdAt: new Date().toISOString(),
        active: true
      };
      
      await fs.writeFile(
        path.join(config.PATHS.TOKENS_DIR, `${accountId}.json`),
        JSON.stringify({ tokens, accountInfo }, null, 2)
      );
      
      await this.setActiveAccount(accountId);
    } catch (error) {
      console.error('Error saving account:', error);
      throw error;
    }
  }

  async loadAccount(accountId) {
    try {
      const accountPath = path.join(config.PATHS.TOKENS_DIR, `${accountId}.json`);
      const content = await fs.readFile(accountPath, 'utf-8');
      const data = JSON.parse(content);
      
      this.oauth2Client.setCredentials(data.tokens);
      this.credentials = data.tokens;
      this.currentAccountId = accountId;
      this.currentAccountEmail = data.accountInfo.email;
      this.allChannels = data.accountInfo.channels;
      
      if (this.allChannels.length > 0) {
        this.selectedChannelId = this.allChannels[0].id;
      }
      
      return data.accountInfo;
    } catch (error) {
      console.error('Error loading account:', error);
      return null;
    }
  }

  async getAllAccounts() {
    try {
      await fs.mkdir(config.PATHS.TOKENS_DIR, { recursive: true });
      const files = await fs.readdir(config.PATHS.TOKENS_DIR);
      const accounts = [];
      
      for (const file of files) {
        if (file.endsWith('.json') && file !== 'active.json') {
          const content = await fs.readFile(
            path.join(config.PATHS.TOKENS_DIR, file),
            'utf-8'
          );
          const data = JSON.parse(content);
          accounts.push(data.accountInfo);
        }
      }
      
      return accounts;
    } catch (error) {
      console.error('Error getting all accounts:', error);
      return [];
    }
  }

  async setActiveAccount(accountId) {
    try {
      await fs.mkdir(config.PATHS.TOKENS_DIR, { recursive: true });
      await fs.writeFile(
        path.join(config.PATHS.TOKENS_DIR, 'active.json'),
        JSON.stringify({ activeAccountId: accountId }, null, 2)
      );
    } catch (error) {
      console.error('Error setting active account:', error);
    }
  }

  async getActiveAccount() {
    try {
      const activePath = path.join(config.PATHS.TOKENS_DIR, 'active.json');
      const content = await fs.readFile(activePath, 'utf-8');
      const data = JSON.parse(content);
      return data.activeAccountId;
    } catch (error) {
      return null;
    }
  }

  async switchAccount(accountId) {
    const accountInfo = await this.loadAccount(accountId);
    if (accountInfo) {
      await this.setActiveAccount(accountId);
      return { success: true, accountInfo };
    }
    return { success: false, error: 'Account not found' };
  }

  getYouTubeClient() {
    if (!this.oauth2Client || !this.credentials) {
      throw new Error('Not authenticated');
    }
    
    return google.youtube({
      version: 'v3',
      auth: this.oauth2Client
    });
  }

  setSelectedChannel(channelId) {
    this.selectedChannelId = channelId;
  }

  getSelectedChannelId() {
    return this.selectedChannelId;
  }

  isAuthenticated() {
    return this.oauth2Client !== null && this.credentials !== null;
  }
}

module.exports = AuthService;
