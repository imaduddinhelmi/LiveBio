import os
import pickle
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import config

class HeadlessAuth:
    """Headless authentication for server environments"""
    
    def __init__(self):
        self.credentials = None
        self.youtube = None
        self.selected_channel_id = None
        self.all_channels = []
        self.current_account_id = None
        self.current_account_email = None
    
    def authenticate_new(self, client_secret_path=None):
        """
        Perform initial authentication (requires browser access)
        Run this ONCE on a machine with browser, then copy token to server
        """
        if client_secret_path is None:
            client_secret_path = config.CLIENT_SECRET_FILE
        
        if not os.path.exists(client_secret_path):
            raise FileNotFoundError(f"Client secret file not found: {client_secret_path}")
        
        print("[AUTH] Starting OAuth flow...")
        print("[AUTH] Your browser will open for authentication")
        
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secret_path, 
            config.SCOPES
        )
        
        # Use local server OAuth flow
        self.credentials = flow.run_local_server(
            port=8080,
            authorization_prompt_message='Please visit this URL: {url}',
            success_message='Authentication successful! You can close this window.',
            open_browser=True
        )
        
        print("[AUTH] Authentication successful!")
        
        # Build YouTube service
        self.youtube = build(
            config.YOUTUBE_API_SERVICE_NAME,
            config.YOUTUBE_API_VERSION,
            credentials=self.credentials
        )
        
        # Get channels
        channels, _ = self.get_all_channels()
        
        if channels:
            self.selected_channel_id = channels[0]["id"]
            account_id = self.generate_account_id()
            self.save_account(account_id, channels[0]["title"], self.credentials, channels)
            self.current_account_id = account_id
            self.current_account_email = channels[0]["title"]
            print(f"[AUTH] Saved account: {channels[0]['title']}")
            print(f"[AUTH] Found {len(channels)} channel(s)")
        
        return True
    
    def load_saved_credentials(self, account_id=None):
        """
        Load saved credentials from file (for server use)
        This doesn't require browser/GUI
        """
        if account_id is None:
            # Load active account
            if config.ACTIVE_ACCOUNT_FILE.exists():
                with open(config.ACTIVE_ACCOUNT_FILE, 'r') as f:
                    data = json.load(f)
                    account_id = data.get('activeAccountId')
        
        if not account_id:
            print("[AUTH] No active account found")
            return False
        
        token_file = config.TOKENS_DIR / f"{account_id}.json"
        
        if not token_file.exists():
            print(f"[AUTH] Token file not found: {token_file}")
            return False
        
        print(f"[AUTH] Loading credentials from: {token_file}")
        
        with open(token_file, 'r') as f:
            data = json.load(f)
        
        # Reconstruct credentials from saved tokens
        creds_data = data['tokens']
        
        from google.oauth2.credentials import Credentials
        self.credentials = Credentials(
            token=creds_data.get('token'),
            refresh_token=creds_data.get('refresh_token'),
            token_uri=creds_data.get('token_uri'),
            client_id=creds_data.get('client_id'),
            client_secret=creds_data.get('client_secret'),
            scopes=creds_data.get('scopes')
        )
        
        # Refresh if expired
        if self.credentials.expired and self.credentials.refresh_token:
            print("[AUTH] Token expired, refreshing...")
            self.credentials.refresh(Request())
            
            # Save refreshed token
            self.save_account(
                account_id,
                data['accountInfo']['name'],
                self.credentials,
                data['accountInfo']['channels']
            )
        
        # Build YouTube service
        self.youtube = build(
            config.YOUTUBE_API_SERVICE_NAME,
            config.YOUTUBE_API_VERSION,
            credentials=self.credentials
        )
        
        # Load account info
        account_info = data['accountInfo']
        self.current_account_id = account_id
        self.current_account_email = account_info['email']
        self.all_channels = account_info['channels']
        
        if self.all_channels:
            self.selected_channel_id = self.all_channels[0]['id']
        
        print(f"[AUTH] Loaded account: {self.current_account_email}")
        print(f"[AUTH] Channels: {len(self.all_channels)}")
        
        return True
    
    def get_all_channels(self):
        """Get all YouTube channels for authenticated user"""
        if not self.youtube:
            return [], "YouTube client not initialized"
        
        channels = []
        channel_ids_seen = set()
        errors = []
        
        # Get owned channels
        try:
            request = self.youtube.channels().list(
                part="snippet,contentDetails,statistics",
                mine=True,
                maxResults=50
            )
            response = request.execute()
            
            if response.get("items"):
                for channel in response["items"]:
                    channel_id = channel["id"]
                    if channel_id not in channel_ids_seen:
                        channels.append({
                            "title": channel["snippet"]["title"],
                            "id": channel_id,
                            "subscribers": channel["statistics"].get("subscriberCount", "N/A"),
                            "customUrl": channel["snippet"].get("customUrl", "N/A")
                        })
                        channel_ids_seen.add(channel_id)
        except Exception as e:
            errors.append(str(e))
        
        # Get managed channels
        try:
            request = self.youtube.channels().list(
                part="snippet,contentDetails,statistics",
                managedByMe=True,
                maxResults=50
            )
            response = request.execute()
            
            if response.get("items"):
                for channel in response["items"]:
                    channel_id = channel["id"]
                    if channel_id not in channel_ids_seen:
                        channels.append({
                            "title": channel["snippet"]["title"],
                            "id": channel_id,
                            "subscribers": channel["statistics"].get("subscriberCount", "N/A"),
                            "customUrl": channel["snippet"].get("customUrl", "N/A")
                        })
                        channel_ids_seen.add(channel_id)
        except Exception as e:
            errors.append(str(e))
        
        self.all_channels = channels
        
        if not channels:
            return [], "No channels found"
        
        return channels, None
    
    def generate_account_id(self):
        """Generate unique account ID"""
        import time
        import random
        return f"account_{int(time.time())}_{random.randint(1000, 9999)}"
    
    def save_account(self, account_id, account_name, credentials, channels):
        """Save account credentials and info to file"""
        account_info = {
            "id": account_id,
            "name": account_name,
            "email": account_name,
            "channels": channels,
            "createdAt": str(Path.cwd()),
            "active": True
        }
        
        # Convert credentials to dict
        tokens = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        # Save to file
        token_file = config.TOKENS_DIR / f"{account_id}.json"
        with open(token_file, 'w') as f:
            json.dump({
                'tokens': tokens,
                'accountInfo': account_info
            }, f, indent=2)
        
        # Set as active account
        with open(config.ACTIVE_ACCOUNT_FILE, 'w') as f:
            json.dump({'activeAccountId': account_id}, f, indent=2)
        
        print(f"[AUTH] Saved account to: {token_file}")
    
    def is_authenticated(self):
        """Check if authenticated"""
        return self.youtube is not None
    
    def get_youtube_client(self):
        """Get YouTube API client"""
        return self.youtube
