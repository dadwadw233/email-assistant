#!/usr/bin/env python3
"""
Command-line tool for managing email accounts in the Personal Email Management Assistant
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.email_handler.processor import EmailProcessor
from src.config.manager import ConfigManager

def list_accounts(config_path):
    """List all configured email accounts"""
    config_manager = ConfigManager(config_path)
    accounts = config_manager.get_accounts()
    
    if not accounts:
        print("No accounts configured.")
        return
    
    print(f"Configured accounts ({len(accounts)}):")
    for i, account in enumerate(accounts, 1):
        print(f"  {i}. {account['email']}")
        print(f"     IMAP Server: {account['imap_server']}:{account['imap_port']}")

def add_account(config_path, email, password, imap_server, imap_port):
    """Add a new email account"""
    config_manager = ConfigManager(config_path)
    
    # Check if account already exists
    accounts = config_manager.get_accounts()
    for account in accounts:
        if account['email'] == email:
            print(f"Account {email} already exists. Updating...")
            break
    
    success = config_manager.add_account(email, password, imap_server, imap_port)
    if success:
        print(f"Account {email} added/updated successfully.")
    else:
        print(f"Failed to add/update account {email}.")

def remove_account(config_path, email):
    """Remove an email account"""
    config_manager = ConfigManager(config_path)
    accounts = config_manager.get_accounts()
    
    # Find and remove the account
    new_accounts = [acc for acc in accounts if acc['email'] != email]
    
    if len(new_accounts) == len(accounts):
        print(f"Account {email} not found.")
        return
    
    # Update the config
    config_manager.config['accounts'] = new_accounts
    success = config_manager.save_config()
    
    if success:
        print(f"Account {email} removed successfully from configuration.")
    else:
        print(f"Failed to remove account {email} from configuration.")

def main():
    parser = argparse.ArgumentParser(description="Manage email accounts for the Email Assistant")
    parser.add_argument("--config", help="Path to configuration file", default="config/app_config.json")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # List command
    subparsers.add_parser("list", help="List all configured accounts")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new email account")
    add_parser.add_argument("email", help="Email address")
    add_parser.add_argument("password", help="App password or authorization code")
    add_parser.add_argument("imap_server", help="IMAP server address")
    add_parser.add_argument("--imap_port", type=int, default=993, help="IMAP server port (default: 993)")
    
    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove an email account")
    remove_parser.add_argument("email", help="Email address to remove")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_accounts(args.config)
    elif args.command == "add":
        add_account(args.config, args.email, args.password, args.imap_server, args.imap_port)
    elif args.command == "remove":
        remove_account(args.config, args.email)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()