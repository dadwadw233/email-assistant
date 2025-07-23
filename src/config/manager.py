"""
Configuration module for the Personal Email Management Assistant
Handles application configuration and settings
"""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path

class ConfigManager:
    """Manages application configuration"""
    
    def __init__(self, config_path: str = "config/app_config.json"):
        self.config_path = config_path
        self.config = {}
        self.load_config()
    
    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                return True
            else:
                # Create default config
                self.config = self._get_default_config()
                self.save_config()
                return True
        except Exception as e:
            print(f"Error loading config: {str(e)}")
            self.config = self._get_default_config()
            return False
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            # Ensure config directory exists
            Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {str(e)}")
            return False
    
    def get(self, key: str, default=None):
        """Get a configuration value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value) -> bool:
        """Set a configuration value"""
        self.config[key] = value
        return self.save_config()
    
    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            "app_name": "Email Assistant",
            "version": "0.1.0",
            "log_level": "INFO",
            "email_check_interval": 300,  # 5 minutes
            "max_emails_per_check": 10,
            "importance_threshold": 0.7,  # Emails with importance >= this are considered important
            "auto_delete_spam": False,
            "accounts": []
        }
    
    def add_account(self, email: str, password: str, imap_server: str, 
                   imap_port: int = 993) -> bool:
        """Add an email account to the configuration"""
        account = {
            "email": email,
            "password": password,
            "imap_server": imap_server,
            "imap_port": imap_port
        }
        
        # Check if account already exists
        for acc in self.config.get("accounts", []):
            if acc["email"] == email:
                # Update existing account
                acc.update(account)
                break
        else:
            # Add new account
            if "accounts" not in self.config:
                self.config["accounts"] = []
            self.config["accounts"].append(account)
        
        return self.save_config()
    
    def get_accounts(self) -> List[Dict]:
        """Get all configured email accounts"""
        return self.config.get("accounts", [])