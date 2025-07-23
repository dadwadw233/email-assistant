"""
Email processor for the Personal Email Management Assistant
Handles email account connections and email processing
"""

import imaplib
import email
from typing import List, Dict, Optional
import logging

class EmailProcessor:
    """Handles email account connections and email processing"""
    
    def __init__(self):
        self.accounts = []
        self.logger = logging.getLogger(__name__)
    
    def add_account(self, email_address: str, password: str, imap_server: str, imap_port: int = 993):
        """Add an email account to monitor"""
        account = {
            'email': email_address,
            'password': password,
            'imap_server': imap_server,
            'imap_port': imap_port
        }
        self.accounts.append(account)
        self.logger.info(f"Added account: {email_address}")
    
    def connect_account(self, account: Dict) -> Optional[imaplib.IMAP4_SSL]:
        """Connect to an email account via IMAP"""
        try:
            mail = imaplib.IMAP4_SSL(account['imap_server'], account['imap_port'])
            mail.login(account['email'], account['password'])
            self.logger.info(f"Connected to {account['email']}")
            return mail
        except imaplib.IMAP4.error as e:
            self.logger.error(f"IMAP error connecting to {account['email']}: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to connect to {account['email']}: {str(e)}")
            return None
    
    def fetch_emails(self, mail: imaplib.IMAP4_SSL, folder: str = 'INBOX', 
                     limit: int = 10) -> List[Dict]:
        """Fetch emails from a folder"""
        try:
            mail.select(folder)
            status, messages = mail.search(None, 'UNSEEN')  # Only unread emails
            
            if status != 'OK':
                self.logger.error(f"Failed to search emails in {folder}")
                return []
            
            email_ids = messages[0].split()
            emails = []
            
            # Process emails (up to limit)
            for email_id in email_ids[-limit:]:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                
                if status != 'OK':
                    self.logger.warning(f"Failed to fetch email {email_id}")
                    continue
                
                # Parse email
                raw_email = msg_data[0][1]
                # Use the correct method to parse email
                parsed_email = email.message_from_bytes(raw_email) if isinstance(raw_email, bytes) else email.message_from_string(raw_email.decode('utf-8'))
                
                email_dict = {
                    'id': email_id.decode(),
                    'subject': parsed_email.get('Subject', ''),
                    'from': parsed_email.get('From', ''),
                    'date': parsed_email.get('Date', ''),
                    'body': self._get_email_body(parsed_email)
                }
                
                emails.append(email_dict)
            
            self.logger.info(f"Fetched {len(emails)} emails from {folder}")
            return emails
            
        except Exception as e:
            self.logger.error(f"Error fetching emails: {str(e)}")
            return []
    
    def _get_email_body(self, parsed_email) -> str:
        """Extract email body from parsed email"""
        body = ""
        
        if parsed_email.is_multipart():
            for part in parsed_email.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                # Skip attachments
                if "attachment" in content_disposition:
                    continue
                
                # Extract text/plain or text/html
                if content_type == "text/plain":
                    payload = part.get_payload(decode=True)
                    if payload:
                        try:
                            body = payload.decode('utf-8')
                        except UnicodeDecodeError:
                            body = payload.decode('latin1')
                    break
                elif content_type == "text/html":
                    payload = part.get_payload(decode=True)
                    if payload:
                        try:
                            body = payload.decode('utf-8')
                        except UnicodeDecodeError:
                            body = payload.decode('latin1')
        else:
            payload = parsed_email.get_payload(decode=True)
            if payload:
                try:
                    body = payload.decode('utf-8')
                except UnicodeDecodeError:
                    body = payload.decode('latin1')
        
        return body
    
    def mark_as_read(self, mail: imaplib.IMAP4_SSL, email_id: str):
        """Mark an email as read"""
        try:
            mail.store(email_id, '+FLAGS', '\\Seen')
            self.logger.info(f"Marked email {email_id} as read")
        except Exception as e:
            self.logger.error(f"Failed to mark email {email_id} as read: {str(e)}")
    
    def delete_email(self, mail: imaplib.IMAP4_SSL, email_id: str):
        """Delete an email (moves to trash)"""
        try:
            mail.store(email_id, '+FLAGS', '\\Deleted')
            mail.expunge()
            self.logger.info(f"Deleted email {email_id}")
        except Exception as e:
            self.logger.error(f"Failed to delete email {email_id}: {str(e)}")