#!/bin/bash
# Setup script for testing environment

echo "Setting up test environment..."

# Create a test database
echo "Creating test database..."
sqlite3 emails.db <<EOF
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
);

CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email_address TEXT UNIQUE,
    imap_server TEXT,
    last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO accounts (email_address, imap_server) VALUES 
('test@example.com', 'imap.example.com'),
('user@gmail.com', 'imap.gmail.com');
EOF

echo "Test database created."

# Create a test config
echo "Creating test configuration..."
cat > config/app_config.json <<EOF
{
  "app_name": "Email Assistant Test",
  "version": "1.0.0",
  "log_level": "DEBUG",
  "email_check_interval": 60,
  "max_emails_per_check": 5,
  "importance_threshold": 0.5,
  "auto_delete_spam": false,
  "accounts": [
    {
      "email": "test@example.com",
      "password": "testpassword",
      "imap_server": "imap.example.com",
      "imap_port": 993
    }
  ]
}
EOF

echo "Test configuration created."

echo "Test environment setup complete!"