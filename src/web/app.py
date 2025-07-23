"""
Web interface for the Personal Email Management Assistant
Provides a simple dashboard to view email analysis results
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, jsonify, request
from src.database.db import EmailDatabase
from src.config.manager import ConfigManager

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Define the template and static directories
template_dir = Path(__file__).parent / 'templates'
static_dir = Path(__file__).parent / 'static'

# Create directories if they don't exist
template_dir.mkdir(exist_ok=True)
static_dir.mkdir(exist_ok=True)

app = Flask(__name__, 
            template_folder=str(template_dir),
            static_folder=str(static_dir))

# Initialize components
database = EmailDatabase()
config_manager = ConfigManager()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/emails')
def get_emails():
    """API endpoint to get emails"""
    try:
        # Get parameters
        limit = int(request.args.get('limit', 20))
        processed = request.args.get('processed', 'false').lower() == 'true'
        
        # Get emails from database
        if processed:
            emails = database.get_processed_emails(limit)
        else:
            emails = database.get_unprocessed_emails(limit)
        
        return jsonify({
            'success': True,
            'emails': emails
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/accounts')
def get_accounts():
    """API endpoint to get email accounts"""
    try:
        accounts = database.get_accounts()
        return jsonify({
            'success': True,
            'accounts': accounts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/config')
def get_config():
    """API endpoint to get application configuration"""
    try:
        config = {
            'app_name': config_manager.get('app_name'),
            'version': config_manager.get('version'),
            'log_level': config_manager.get('log_level'),
            'email_check_interval': config_manager.get('email_check_interval'),
            'importance_threshold': config_manager.get('importance_threshold')
        }
        return jsonify({
            'success': True,
            'config': config
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/emails')
def get_emails():
    """API endpoint to get emails"""
    try:
        # Get parameters
        limit = int(request.args.get('limit', 20))
        processed = request.args.get('processed', 'false').lower() == 'true'
        
        # Get emails from database
        if processed:
            emails = database.get_processed_emails(limit)
        else:
            emails = database.get_unprocessed_emails(limit)
        
        return jsonify({
            'success': True,
            'emails': emails
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/accounts')
def get_accounts():
    """API endpoint to get email accounts"""
    try:
        accounts = database.get_accounts()
        return jsonify({
            'success': True,
            'accounts': accounts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/config')
def get_config():
    """API endpoint to get application configuration"""
    try:
        config = {
            'app_name': config_manager.get('app_name'),
            'version': config_manager.get('version'),
            'log_level': config_manager.get('log_level'),
            'email_check_interval': config_manager.get('email_check_interval'),
            'importance_threshold': config_manager.get('importance_threshold')
        }
        return jsonify({
            'success': True,
            'config': config
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)