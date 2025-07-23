#!/bin/bash
# Installation script for Email Assistant

echo "Installing Email Assistant..."

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create config directory if it doesn't exist
mkdir -p config

# Copy example config if it doesn't exist
if [ ! -f "config/app_config.json" ]; then
    echo "Creating configuration file from example..."
    cp config/app_config.json.example config/app_config.json
fi

echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit config/app_config.json to add your email accounts"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the application: python main.py"