#!/bin/bash
set -e

echo "Setting up Linux Clipboard History Tool..."

# Check for sudo/root
if [ "$EUID" -ne 0 ]; then 
  echo "Please enter your password to install system dependencies (apt)."
  # partial update is fine if main repos work
  sudo apt update || echo "Warning: 'apt update' completed with errors. Attempting to proceed..."
  sudo apt install -y python3-dev python3-tk python3-pip python3-venv gcc libx11-dev xclip xdotool
else
  apt update || echo "Warning: 'apt update' completed with errors. Attempting to proceed..."
  apt install -y python3-dev python3-tk python3-pip python3-venv gcc libx11-dev xclip
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate and install requirements
echo "Installing Python dependencies..."
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt

echo "Setup complete! Run the tool with:"
echo "./.venv/bin/python main.py"
