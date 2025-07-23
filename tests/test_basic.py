"""
Tests for the Personal Email Management Assistant
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / ".." / "src"))

from src.config.manager import ConfigManager
from src.email_handler.processor import EmailProcessor

class TestConfigManager(unittest.TestCase):
    """Test cases for the ConfigManager class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config_manager = ConfigManager()
    
    def test_default_config(self):
        """Test that default configuration is loaded correctly"""
        config = self.config_manager.config
        self.assertIn("app_name", config)
        self.assertIn("version", config)
        self.assertEqual(config["app_name"], "Email Assistant")
    
    def test_get_config_value(self):
        """Test getting configuration values"""
        app_name = self.config_manager.get("app_name")
        self.assertEqual(app_name, "Email Assistant")
        
        # Test default value
        nonexistent = self.config_manager.get("nonexistent_key", "default")
        self.assertEqual(nonexistent, "default")

class TestEmailProcessor(unittest.TestCase):
    """Test cases for the EmailProcessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.email_processor = EmailProcessor()
    
    def test_initialization(self):
        """Test that the email processor is initialized correctly"""
        self.assertEqual(len(self.email_processor.accounts), 0)
    
    def test_add_account(self):
        """Test adding an email account"""
        self.email_processor.add_account(
            "test@example.com",
            "password",
            "imap.example.com"
        )
        
        self.assertEqual(len(self.email_processor.accounts), 1)
        account = self.email_processor.accounts[0]
        self.assertEqual(account["email"], "test@example.com")
        self.assertEqual(account["imap_server"], "imap.example.com")

if __name__ == "__main__":
    unittest.main()