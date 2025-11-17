import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import config
from multi_account_manager import MultiAccountManager

class YouTubeAuth:
    def __init__(self):
        self.credentials = None
        self.youtube = None
        self.selected_channel_id = None
        self.all_channels = []
        self.account_manager = MultiAccountManager()
        self.current_account_id = None
        self.current_account_email = None
        
    def authenticate(self, client_secret_path, account_name=None, force_new=False):
        """
        Authenticate with Google OAuth
        
        Args:
            client_secret_path: Path to client_secret.json
            account_name: Optional custom name for the account
            force_new: Force new authentication even if account exists
        
        Returns:
            bool: Success status
        """
        # Check if we should try to load from active account first
        if not force_new:
            active_account = self.account_manager.get_active_account()
            if active_account:
                credentials = self.account_manager.load_credentials(active_account["id"])
                if credentials and credentials.valid:
                    self.credentials = credentials
                    self.current_account_id = active_account["id"]
                    self.current_account_email = active_account["email"]
                    self.youtube = build(
                        config.YOUTUBE_API_SERVICE_NAME,
                        config.YOUTUBE_API_VERSION,
                        credentials=self.credentials
                    )
                    return True
                elif credentials and credentials.expired and credentials.refresh_token:
                    try:
                        credentials.refresh(Request())
                        self.credentials = credentials
                        self.current_account_id = active_account["id"]
                        self.current_account_email = active_account["email"]
                        
                        # Save refreshed token
                        token_path = self.account_manager.get_token_path(active_account["id"])
                        with open(token_path, 'wb') as f:
                            pickle.dump(credentials, f)
                        
                        self.youtube = build(
                            config.YOUTUBE_API_SERVICE_NAME,
                            config.YOUTUBE_API_VERSION,
                            credentials=self.credentials
                        )
                        return True
                    except:
                        pass
        
        # Need new authentication
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secret_path, config.SCOPES)
        self.credentials = flow.run_local_server(port=0)
        
        # Get user email from credentials
        self.youtube = build(
            config.YOUTUBE_API_SERVICE_NAME,
            config.YOUTUBE_API_VERSION,
            credentials=self.credentials
        )
        
        # Try to get account identifier
        try:
            # Get channels first to use as identifier
            channels, _ = self.get_all_channels()
            
            # Try multiple ways to get email/identifier
            email = "Unknown"
            
            # Method 1: Try to get from token
            if hasattr(self.credentials, 'id_token'):
                try:
                    import json
                    import base64
                    # Decode JWT token
                    token_parts = self.credentials.id_token.split('.')
                    if len(token_parts) > 1:
                        # Add padding if needed
                        payload = token_parts[1]
                        payload += '=' * (4 - len(payload) % 4)
                        decoded = base64.b64decode(payload)
                        token_data = json.loads(decoded)
                        email = token_data.get('email', 'Unknown')
                except:
                    pass
            
            # Method 2: Use first channel title if email not found
            if email == "Unknown" and channels:
                email = channels[0].get('title', 'Unknown')
            
            # Create account name
            if not account_name:
                account_name = email
            
            # Add account to manager
            if channels:  # Only save if we have channels
                self.current_account_id = self.account_manager.add_account(
                    account_name=account_name,
                    email=email,
                    credentials=self.credentials,
                    channels=channels
                )
                self.current_account_email = email
                print(f"[OK] Account saved: {account_name} ({len(channels)} channels)")
            else:
                print(f"[WARNING] No channels found, account not saved")
                
        except Exception as e:
            print(f"[WARNING] Could not save account info: {e}")
            import traceback
            traceback.print_exc()
            # Still continue with authentication
        
        return True
    
    def switch_account(self, account_id):
        """
        Switch to a different saved account
        
        Args:
            account_id: ID of the account to switch to
        
        Returns:
            bool: Success status
        """
        account = self.account_manager.get_account(account_id)
        if not account:
            return False
        
        credentials = self.account_manager.load_credentials(account_id)
        if not credentials:
            return False
        
        # Refresh if expired
        if credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                # Save refreshed token
                token_path = self.account_manager.get_token_path(account_id)
                with open(token_path, 'wb') as f:
                    pickle.dump(credentials, f)
            except:
                return False
        
        # Set as active
        self.credentials = credentials
        self.current_account_id = account_id
        self.current_account_email = account["email"]
        self.account_manager.set_active_account(account_id)
        
        # Build YouTube service
        self.youtube = build(
            config.YOUTUBE_API_SERVICE_NAME,
            config.YOUTUBE_API_VERSION,
            credentials=self.credentials
        )
        
        # Reload channels
        channels, _ = self.get_all_channels()
        if channels:
            self.account_manager.update_account_channels(account_id, channels)
        
        return True
    
    def get_current_account_info(self):
        """Get current account information"""
        if self.current_account_id:
            return self.account_manager.get_account(self.current_account_id)
        return None
    
    def get_all_channels(self):
        if not self.youtube:
            return [], "YouTube client not initialized"
        
        channels = []
        channel_ids_seen = set()
        errors = []
        
        # Get channels owned by user
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
                print(f"[OK] Found {len(channels)} owned channel(s)")
            else:
                print(f"[INFO] No owned channels found (mine=True returned no items)")
        except Exception as e:
            error_msg = f"Error fetching owned channels: {str(e)}"
            print(f"[X] {error_msg}")
            errors.append(error_msg)
        
        # Get channels managed by user (includes brand accounts)
        try:
            request = self.youtube.channels().list(
                part="snippet,contentDetails,statistics",
                managedByMe=True,
                maxResults=50
            )
            response = request.execute()
            
            managed_count = 0
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
                        managed_count += 1
                print(f"[OK] Found {managed_count} additional managed channel(s)")
            else:
                print(f"[INFO] No managed channels found (managedByMe=True returned no items)")
        except Exception as e:
            error_msg = f"Error fetching managed channels: {str(e)}"
            print(f"[X] {error_msg}")
            errors.append(error_msg)
        
        self.all_channels = channels
        if channels and not self.selected_channel_id:
            self.selected_channel_id = channels[0]["id"]
        
        # Return channels with status message
        if not channels:
            if errors:
                # Both requests failed
                error_detail = " | ".join(errors)
                return [], f"Failed to fetch channels. Errors: {error_detail}"
            else:
                # Requests succeeded but no channels found
                return [], "No YouTube channels found for this account. Please create a channel first at youtube.com"
        
        return channels, None
    
    def get_channel_info(self):
        if not self.youtube:
            return None
        
        channels, error = self.get_all_channels()
        if channels:
            return channels[0]
        return None
    
    def set_selected_channel(self, channel_id):
        self.selected_channel_id = channel_id
    
    def get_selected_channel_id(self):
        return self.selected_channel_id
    
    def is_authenticated(self):
        return self.youtube is not None
