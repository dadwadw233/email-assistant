#!/usr/bin/env python3
"""
Simple test script for Gmail connection
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Set Python path to avoid import issues
os.environ['PYTHONPATH'] = str(Path(__file__).parent / "src")

from src.email_handler.processor import EmailProcessor
from src.config.manager import ConfigManager

def test_gmail_connection():
    """Test Gmail connection with provided credentials"""
    print("Testing Gmail connection...")
    
    # Load configuration
    config_manager = ConfigManager("config/app_config.json")
    accounts = config_manager.get_accounts()
    
    if not accounts:
        print("No accounts configured. Please edit config/app_config.json")
        return
    
    # Initialize email processor
    email_processor = EmailProcessor()
    
    # Add account
    account = accounts[0]  # Use the first account
    email_processor.add_account(
        account["email"],
        account["password"],
        account["imap_server"],
        account["imap_port"]
    )
    
    print(f"Attempting to connect to {account['email']}...")
    
    # Connect to account
    mail = email_processor.connect_account(account)
    
    if mail:
        print("Connection successful!")
        
        # Try to fetch a few emails
        print("Fetching emails...")
        emails = email_processor.fetch_emails(mail, limit=3)
        
        print(f"Found {len(emails)} unread emails:")
        for i, email in enumerate(emails):
            print(f"\n--- Email {i+1} ---")
            print(f"From: {email['from']}")
            print(f"Subject: {email['subject']}")
            print(f"Date: {email['date']}")
            print(f"Body preview: {email['body'][:100]}...")
        
        # Close connection
        mail.close()
        mail.logout()
        print("\nConnection closed.")
    else:
        print("Connection failed!")

if __name__ == "__main__":
    test_gmail_connection()