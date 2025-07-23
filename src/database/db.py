"""
Database module for the Personal Email Management Assistant
Handles data storage and retrieval using SQLite
"""

import sqlite3
import logging
from typing import List, Dict, Optional
from pathlib import Path

class EmailDatabase:
    """Handles database operations for email storage and retrieval"""
    
    def __init__(self, db_path: str = "emails.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the database with required tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create emails table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS emails (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email_id TEXT UNIQUE,
                        sender TEXT,
                        subject TEXT,
                        body TEXT,
                        date TEXT,
                        importance REAL,
                        summary TEXT,
                        category TEXT,
                        action TEXT,
                        processed BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create accounts table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS accounts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email_address TEXT UNIQUE,
                        imap_server TEXT,
                        last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                self.logger.info("Database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Error initializing database: {str(e)}")
            raise
    
    def save_email(self, email_data: Dict, analysis: Dict) -> bool:
        """Save an email and its analysis to the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO emails 
                    (email_id, sender, subject, body, date, importance, summary, category, action)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    email_data.get('id'),
                    email_data.get('from'),
                    email_data.get('subject'),
                    email_data.get('body'),
                    email_data.get('date'),
                    analysis.get('importance'),
                    analysis.get('summary'),
                    analysis.get('category'),
                    analysis.get('action')
                ))
                
                conn.commit()
                self.logger.info(f"Saved email {email_data.get('id')} to database")
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving email to database: {str(e)}")
            return False
    
    def get_unprocessed_emails(self, limit: int = 10) -> List[Dict]:
        """Get unprocessed emails from the database"""
        return self._get_emails(limit, processed=False)
    
    def get_processed_emails(self, limit: int = 10) -> List[Dict]:
        """Get processed emails from the database"""
        return self._get_emails(limit, processed=True)
    
    def _get_emails(self, limit: int = 10, processed: bool = False) -> List[Dict]:
        """Get emails from the database"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, email_id, sender, subject, body, date, importance, summary, category, action
                    FROM emails 
                    WHERE processed = ?
                    ORDER BY importance DESC, date DESC
                    LIMIT ?
                """, (processed, limit))
                
                rows = cursor.fetchall()
                emails = []
                
                for row in rows:
                    email = {
                        'db_id': row[0],
                        'id': row[1],
                        'from': row[2],
                        'subject': row[3],
                        'body': row[4],
                        'date': row[5],
                        'importance': row[6],
                        'summary': row[7],
                        'category': row[8],
                        'action': row[9]
                    }
                    emails.append(email)
                
                status = "processed" if processed else "unprocessed"
                self.logger.info(f"Retrieved {len(emails)} {status} emails")
                return emails
                
        except Exception as e:
            self.logger.error(f"Error retrieving emails: {str(e)}")
            return []
    
    def mark_email_processed(self, db_id: int) -> bool:
        """Mark an email as processed"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE emails 
                    SET processed = TRUE
                    WHERE id = ?
                """, (db_id,))
                
                conn.commit()
                self.logger.info(f"Marked email {db_id} as processed")
                return True
                
        except Exception as e:
            self.logger.error(f"Error marking email as processed: {str(e)}")
            return False
    
    def add_account(self, email_address: str, imap_server: str) -> bool:
        """Add an email account to track"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT OR REPLACE INTO accounts 
                    (email_address, imap_server)
                    VALUES (?, ?)
                """, (email_address, imap_server))
                
                conn.commit()
                self.logger.info(f"Added account {email_address} to database")
                return True
                
        except Exception as e:
            self.logger.error(f"Error adding account to database: {str(e)}")
            return False
    
    def update_account_last_checked(self, email_address: str) -> bool:
        """Update the last checked timestamp for an account"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE accounts 
                    SET last_checked = CURRENT_TIMESTAMP
                    WHERE email_address = ?
                """, (email_address,))
                
                conn.commit()
                self.logger.info(f"Updated last checked time for account {email_address}")
                return True
                
        except Exception as e:
            self.logger.error(f"Error updating account last checked time: {str(e)}")
            return False
    
    def get_accounts(self) -> List[Dict]:
        """Get all email accounts"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, email_address, imap_server, last_checked
                    FROM accounts
                """)
                
                rows = cursor.fetchall()
                accounts = []
                
                for row in rows:
                    account = {
                        'id': row[0],
                        'email_address': row[1],
                        'imap_server': row[2],
                        'last_checked': row[3]
                    }
                    accounts.append(account)
                
                self.logger.info(f"Retrieved {len(accounts)} accounts")
                return accounts
                
        except Exception as e:
            self.logger.error(f"Error retrieving accounts: {str(e)}")
            return []