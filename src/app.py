"""
Main application class for the Personal Email Management Assistant
Integrates all modules and handles the main application flow
"""

import logging
import time
from typing import List, Dict
from src.email_handler.processor import EmailProcessor
from src.ai.analyzer import EmailAnalyzer
from src.database.db import EmailDatabase
from src.config.manager import ConfigManager

class EmailAssistant:
    """Main application class for the Email Assistant"""
    
    def __init__(self, config_path: str = "config/app_config.json"):
        # Initialize components
        self.config_manager = ConfigManager(config_path)
        self.email_processor = EmailProcessor()
        self.email_analyzer = EmailAnalyzer()
        self.database = EmailDatabase()
        
        # Setup logging
        log_level = getattr(logging, self.config_manager.get("log_level", "INFO"))
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("email_assistant.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # Load email accounts
        self._load_accounts()
    
    def _load_accounts(self):
        """Load email accounts from configuration"""
        accounts = self.config_manager.get_accounts()
        for account in accounts:
            self.email_processor.add_account(
                account["email"],
                account["password"],
                account["imap_server"],
                account["imap_port"]
            )
            self.database.add_account(
                account["email"],
                account["imap_server"]
            )
        self.logger.info(f"Loaded {len(accounts)} email accounts")
    
    def _send_notification(self, email_data: Dict, analysis: Dict):
        """
        Send notification for important emails
        For now, just print to console, but could be extended to use system notifications,
        email, SMS, etc.
        """
        # TODO: Implement actual notification system
        # Could integrate with system notifications, email, SMS, etc.
        self.logger.info(f"NOTIFICATION: Important email from {email_data['from']}: {email_data['subject']}")
        print(f"IMPORTANT EMAIL: {email_data['from']} - {email_data['subject']}")
        print(f"Summary: {analysis.get('summary', 'No summary')}")
        print("---")
    
    def process_emails(self):
        """Main email processing function"""
        self.logger.info("Starting email processing cycle")
        
        # Process each account
        for account in self.email_processor.accounts:
            self.logger.info(f"Processing account: {account['email']}")
            
            # Connect to the account
            mail = self.email_processor.connect_account(account)
            if not mail:
                self.logger.error(f"Failed to connect to {account['email']}")
                continue
            
            try:
                # Fetch emails
                max_emails = self.config_manager.get("max_emails_per_check", 10)
                emails = self.email_processor.fetch_emails(mail, limit=max_emails)
                
                # Update last checked time
                self.database.update_account_last_checked(account['email'])
                
                # Process each email
                for email_data in emails:
                    # Analyze the email
                    analysis = self.email_analyzer.analyze_email(email_data)
                    
                    # Save to database
                    self.database.save_email(email_data, analysis)
                    
                    # Mark as read
                    self.email_processor.mark_as_read(mail, email_data['id'])
                    
                    # Handle auto-deletion of spam if enabled
                    auto_delete_spam = self.config_manager.get("auto_delete_spam", False)
                    if auto_delete_spam and analysis.get('category') == 'spam':
                        self.email_processor.delete_email(mail, email_data['id'])
                        self.logger.info(f"Deleted spam email from {email_data['from']}: {email_data['subject']}")
                        continue  # Skip notification for deleted emails
                    
                    # Log important emails
                    if analysis.get('importance', 0) >= self.config_manager.get("importance_threshold", 0.7):
                        self.logger.info(f"Important email from {email_data['from']}: {email_data['subject']}")
                        
                        # Send notification for important emails
                        self._send_notification(email_data, analysis)
                
                # Close connection
                mail.close()
                mail.logout()
                
            except Exception as e:
                self.logger.error(f"Error processing account {account['email']}: {str(e)}")
                if mail:
                    try:
                        mail.close()
                        mail.logout()
                    except:
                        pass
    
    def review_emails(self):
        """Review unprocessed emails in the database"""
        self.logger.info("Reviewing unprocessed emails")
        
        # Get unprocessed emails
        emails = self.database.get_unprocessed_emails()
        
        # Create a mapping of email IDs to account information for deletion
        email_account_map = {}
        for account in self.email_processor.accounts:
            email_account_map[account['email']] = account
        
        for email in emails:
            print(f"\n--- Email Review ---")
            print(f"From: {email['from']}")
            print(f"Subject: {email['subject']}")
            print(f"Summary: {email['summary']}")
            print(f"Category: {email['category']}")
            print(f"Recommended Action: {email['action']}")
            print(f"Importance: {email['importance']:.2f}")
            
            # Ask user for action
            action = input("Action (read/archive/delete/skip): ").lower().strip()
            
            if action == "delete":
                # Actually delete the email from the server
                # Parse the sender's email to find the corresponding account
                sender_email = email['from'].split('<')[-1].split('>')[0] if '<' in email['from'] else email['from']
                account = None
                for acc in self.email_processor.accounts:
                    if acc['email'] == sender_email or sender_email.endswith(acc['email'].split('@')[-1]):
                        account = acc
                        break
                
                if account:
                    mail = self.email_processor.connect_account(account)
                    if mail:
                        try:
                            self.email_processor.delete_email(mail, email['id'])
                            self.logger.info(f"Deleted email from {email['from']}: {email['subject']}")
                            mail.close()
                            mail.logout()
                        except Exception as e:
                            self.logger.error(f"Failed to delete email: {str(e)}")
                    else:
                        self.logger.error(f"Failed to connect to account {account['email']} for deletion")
                else:
                    self.logger.warning(f"Could not find account for email sender {sender_email}")
                
                self.database.mark_email_processed(email['db_id'])
                print("Email deleted.")
            elif action in ["read", "archive", "skip"]:
                self.database.mark_email_processed(email['db_id'])
                print(f"Email marked as {action}.")
            else:
                print("Invalid action, skipping...")
    
    def run(self):
        """Run the email assistant"""
        self.logger.info("Email Assistant started")
        
        # Check interval from config (default 5 minutes)
        check_interval = self.config_manager.get("email_check_interval", 300)
        
        try:
            while True:
                # Process emails
                self.process_emails()
                
                # Wait before next check
                self.logger.info(f"Waiting {check_interval} seconds before next check")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            self.logger.info("Email Assistant stopped by user")
        except Exception as e:
            self.logger.error(f"Error in main loop: {str(e)}")