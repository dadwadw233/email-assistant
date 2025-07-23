# Personal Email Management Assistant

## Project Goal
Implement an intelligent email management assistant to help users efficiently process emails from Gmail, QQ Mail, and other email accounts.

## Core Features
1. Automatically read email content from multiple email accounts
2. Call LLM APIs to intelligently analyze and summarize emails
3. Identify important emails and promptly notify users
4. Identify useless emails and automatically delete them with user authorization
5. Provide email categorization and tagging functionality
6. Web dashboard for viewing email analysis results

## Technical Architecture
- Python backend for email handling and LLM integration
- Email protocol support: IMAP/POP3/SMTP
- Supported LLMs: Qwen, OpenAI GPT, Claude, Gemini, etc.
- Data storage: SQLite or PostgreSQL
- Web interface: Flask

## Project Structure
```
email-assistant/
├── config/           # Configuration files
├── docs/             # Documentation
├── src/              # Source code
│   ├── ai/           # AI/LLM integration
│   ├── config/       # Configuration management
│   ├── database/     # Database operations
│   ├── email_handler/ # Email processing
│   └── web/          # Web interface
├── tests/            # Test code
├── venv/             # Virtual environment (not in repo)
├── account_manager.py # CLI tool for account management
├── main.py           # Main entry point
├── web.py            # Web interface entry point
├── test_gmail.py     # Gmail connection test script
├── requirements.txt  # Python dependencies
├── install.sh        # Installation script
├── setup_test.sh     # Test environment setup
└── emails.db         # SQLite database file
```

## Development Plan
1. Email account connection and email reading module
2. LLM API integration and email analysis module
3. User feedback and email tagging system
4. Automatic deletion mechanism and security confirmation
5. Web interface or command-line interface

## Installation

1. Clone or download the repository
2. Run the installation script:
   ```bash
   ./install.sh
   ```
3. Edit the configuration file:
   ```bash
   # Copy the example config
   cp config/app_config.json.example config/app_config.json
   
   # Edit the config file with your email accounts
   nano config/app_config.json
   ```
4. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

## Usage

Run the email assistant:
```bash
python main.py
```

Run once and exit (don't loop):
```bash
python main.py --once
```

Review unprocessed emails:
```bash
python main.py --review
```

Enable verbose output:
```bash
python main.py --verbose
```

Start the web interface:
```bash
python web.py
```

Manage email accounts:
```bash
# List all accounts
python account_manager.py list

# Add a new account
python account_manager.py add your@email.com your_app_password imap.server.com --imap_port 993

# Remove an account
python account_manager.py remove your@email.com
```

## Configuration

The configuration file (`config/app_config.json`) contains the following options:

- `app_name`: Application name
- `version`: Application version
- `log_level`: Logging level (DEBUG, INFO, WARNING, ERROR)
- `email_check_interval`: Interval between email checks (in seconds)
- `max_emails_per_check`: Maximum number of emails to process per check
- `importance_threshold`: Threshold for determining important emails (0.0-1.0)
- `auto_delete_spam`: Whether to automatically delete spam emails
- `accounts`: List of email accounts to monitor

For each email account, you need to specify:
- `email`: Email address
- `password`: App password or authorization code
- `imap_server`: IMAP server address
- `imap_port`: IMAP server port (usually 993 for SSL)

## Supported Email Providers

- Gmail: Use `imap.gmail.com` with an app password
- QQ Mail: Use `imap.qq.com` with an authorization code
- Other providers: Check your email provider's documentation for IMAP settings

## LLM API Integration

The application supports multiple LLM providers, with Qwen as the default.

### Qwen (Aliyun DashScope)
To use Qwen models:

1. Set your API key in `~/.qwen_env`:
   ```
   export DASHSCOPE_API_KEY=your_dashscope_api_key
   ```

2. The application will automatically use Qwen Plus model by default.

### Other providers
You can also configure other providers by setting the appropriate environment variables:

For OpenAI:
```
export OPENAI_API_KEY=your_openai_api_key
export OPENAI_MODEL=gpt-3.5-turbo
```

For Anthropic:
```
export ANTHROPIC_API_KEY=your_anthropic_api_key
```

## Testing Gmail Connection

To test your Gmail connection:

1. Edit the configuration file:
   ```bash
   nano config/app_config.json
   ```
   
2. Replace `YOUR_GMAIL_ADDRESS@gmail.com` with your actual Gmail address
   
3. For the password, you need to use an App Password, not your regular Gmail password:
   - Go to your Google Account settings
   - Navigate to Security > 2-Step Verification > App passwords
   - Generate a new App password for "Mail"
   - Use this App password in the config file

4. Run the test script:
   ```bash
   source ~/.qwen_env  # Load Qwen environment variables
   python test_gmail.py
   ```

This will attempt to connect to your Gmail account and fetch a few unread emails.

## Web Interface

The application includes a modern web dashboard for viewing email analysis results:

1. Start the web interface:
   ```bash
   python web.py
   ```

2. Open your browser and navigate to `http://localhost:5000`

The dashboard features:
- Clean, responsive design with Bootstrap 5
- Real-time email visualization with importance indicators
- Color-coded email categories (work, personal, newsletter, spam)
- Automatic refresh of unprocessed emails
- Detailed email information display
- Configuration overview panel
- Account management panel

### Dashboard Features:
- **Email Cards**: Each email is displayed in a card with color-coded borders indicating importance (red=high, yellow=medium, green=low)
- **Category Badges**: Clear visual indicators for email categories with appropriate icons
- **Action Recommendations**: Displays recommended actions for each email
- **Tabbed Interface**: Switch between unprocessed and processed emails
- **Responsive Design**: Works well on desktop and mobile devices
- **Auto-refresh**: Unprocessed emails automatically refresh every 30 seconds

## Troubleshooting

### Common Issues

1. **Connection errors**: Make sure you're using the correct IMAP server and port for your email provider.
   For Gmail, use `imap.gmail.com:993` with an App Password.

2. **Authentication failures**: Ensure you're using an App Password or Authorization Code, not your regular email password.

3. **LLM API issues**: Check that your API key is correctly set in the environment variables.

4. **Database errors**: If you encounter database issues, try deleting the `emails.db` file and restarting the application.

### Debugging

To enable debug output:
```bash
python main.py --verbose
```

Check the log file `email_assistant.log` for detailed error messages.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Special Thanks

We would like to acknowledge the contributions of AI assistants in the development of this project:

- **Qwen** (通义千问): Provided guidance on architecture design, helped implement LLM integration, and assisted with code improvements throughout the development process.
- **Gemini**: Helped with frontend design concepts and implementation details.

Their contributions have been invaluable in creating a robust and user-friendly email management assistant.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.