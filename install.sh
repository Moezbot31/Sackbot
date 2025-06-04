#!/bin/bash
# Sackbot install script (stub)
# Usage: bash install.sh

set -e

if ! command -v python3 &> /dev/null; then
    echo "Python3 is required. Please install Python3."
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "pip is required. Please install pip."
    exit 1
fi

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Sackbot is ready to use! Run: python3 sackbot.py"
