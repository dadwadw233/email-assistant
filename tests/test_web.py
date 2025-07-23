"""
Test for the web interface of the Personal Email Management Assistant
"""

import unittest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.web.app import app

class WebInterfaceTest(unittest.TestCase):
    """Test cases for the web interface"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_index_page(self):
        """Test that the index page loads"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_api_config(self):
        """Test that the config API endpoint works"""
        response = self.app.get('/api/config')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('success', data)
        self.assertTrue(data['success'])
        
        self.assertIn('config', data)
        config = data['config']
        self.assertIn('app_name', config)
        self.assertIn('version', config)
    
    def test_api_accounts(self):
        """Test that the accounts API endpoint works"""
        response = self.app.get('/api/accounts')
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertIn('success', data)
        # Note: success might be False if no accounts are configured

if __name__ == '__main__':
    unittest.main()