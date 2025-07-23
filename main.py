#!/usr/bin/env python3
"""
Personal Email Management Assistant
Main entry point
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.app import EmailAssistant

def main():
    parser = argparse.ArgumentParser(description="Personal Email Management Assistant")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument("--once", action="store_true", help="Run once and exit (don't loop)")
    parser.add_argument("--review", action="store_true", help="Review unprocessed emails")
    
    args = parser.parse_args()
    
    print("Personal Email Management Assistant")
    print("Starting up...")
    
    # Create the application
    config_path = args.config or "config/app_config.json"
    assistant = EmailAssistant(config_path)
    
    # Handle different modes
    if args.review:
        assistant.review_emails()
    elif args.once:
        assistant.process_emails()
    else:
        assistant.run()

if __name__ == "__main__":
    main()