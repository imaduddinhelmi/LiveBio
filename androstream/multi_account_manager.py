"""
Multi-Account Manager for YouTube Authentication
Manages multiple Google accounts and allows easy switching between them
"""

import os
import json
import pickle
from pathlib import Path
from datetime import datetime

class MultiAccountManager:
    def __init__(self, base_dir=None):
        if base_dir is None:
            self.base_dir = Path.home() / ".ytlive"
        else:
            self.base_dir = Path(base_dir)
        
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.accounts_file = self.base_dir / "accounts.json"
        self.tokens_dir = self.base_dir / "tokens"
        self.tokens_dir.mkdir(exist_ok=True)
        
        self.accounts = self.load_accounts()
        
    def load_accounts(self):
        """Load all saved accounts from JSON file"""
        if self.accounts_file.exists():
            try:
                with open(self.accounts_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"accounts": [], "active_account_id": None}
        return {"accounts": [], "active_account_id": None}
    
    def save_accounts(self):
        """Save accounts to JSON file"""
        with open(self.accounts_file, 'w', encoding='utf-8') as f:
            json.dump(self.accounts, f, indent=2, ensure_ascii=False)
    
    def get_token_path(self, account_id):
        """Get token file path for specific account"""
        return self.tokens_dir / f"token_{account_id}.pickle"
    
    def add_account(self, account_name, email, credentials, channels=None):
        """
        Add new account
        
        Args:
            account_name: Display name for the account
            email: Email address
            credentials: Google credentials object
            channels: List of channels for this account
        
        Returns:
            account_id: Generated account ID
        """
        # Generate unique account ID
        account_id = f"acc_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Save credentials to token file
        token_path = self.get_token_path(account_id)
        with open(token_path, 'wb') as f:
            pickle.dump(credentials, f)
        
        # Add account to list
        account_data = {
            "id": account_id,
            "name": account_name,
            "email": email,
            "channels": channels or [],
            "added_date": datetime.now().isoformat(),
            "last_used": datetime.now().isoformat()
        }
        
        self.accounts["accounts"].append(account_data)
        
        # Set as active if it's the first account
        if len(self.accounts["accounts"]) == 1:
            self.accounts["active_account_id"] = account_id
        
        self.save_accounts()
        return account_id
    
    def get_account(self, account_id):
        """Get account data by ID"""
        for acc in self.accounts["accounts"]:
            if acc["id"] == account_id:
                return acc
        return None
    
    def get_all_accounts(self):
        """Get all saved accounts"""
        return self.accounts["accounts"]
    
    def get_active_account(self):
        """Get currently active account"""
        active_id = self.accounts.get("active_account_id")
        if active_id:
            return self.get_account(active_id)
        return None
    
    def set_active_account(self, account_id):
        """Set active account"""
        account = self.get_account(account_id)
        if account:
            self.accounts["active_account_id"] = account_id
            account["last_used"] = datetime.now().isoformat()
            self.save_accounts()
            return True
        return False
    
    def load_credentials(self, account_id):
        """Load credentials for specific account"""
        token_path = self.get_token_path(account_id)
        if token_path.exists():
            try:
                with open(token_path, 'rb') as f:
                    return pickle.load(f)
            except:
                return None
        return None
    
    def update_account_channels(self, account_id, channels):
        """Update channels list for an account"""
        account = self.get_account(account_id)
        if account:
            account["channels"] = channels
            self.save_accounts()
            return True
        return False
    
    def update_account_name(self, account_id, new_name):
        """Update account display name"""
        account = self.get_account(account_id)
        if account:
            account["name"] = new_name
            self.save_accounts()
            return True
        return False
    
    def remove_account(self, account_id):
        """Remove account and its token file"""
        # Find and remove account from list
        for i, acc in enumerate(self.accounts["accounts"]):
            if acc["id"] == account_id:
                self.accounts["accounts"].pop(i)
                
                # Remove token file
                token_path = self.get_token_path(account_id)
                if token_path.exists():
                    token_path.unlink()
                
                # Update active account if necessary
                if self.accounts["active_account_id"] == account_id:
                    if self.accounts["accounts"]:
                        self.accounts["active_account_id"] = self.accounts["accounts"][0]["id"]
                    else:
                        self.accounts["active_account_id"] = None
                
                self.save_accounts()
                return True
        return False
    
    def has_accounts(self):
        """Check if there are any saved accounts"""
        return len(self.accounts["accounts"]) > 0
    
    def get_account_count(self):
        """Get total number of saved accounts"""
        return len(self.accounts["accounts"])
    
    def clear_all_accounts(self):
        """Remove all accounts and their tokens"""
        # Remove all token files
        for acc in self.accounts["accounts"]:
            token_path = self.get_token_path(acc["id"])
            if token_path.exists():
                token_path.unlink()
        
        # Clear accounts
        self.accounts = {"accounts": [], "active_account_id": None}
        self.save_accounts()
