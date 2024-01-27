#!/bin/bash

# Path where the repository will be cloned
REPO_PATH="$HOME/CyberToolbox"

# Automatically remove the directory if it exists
if [ -d "$REPO_PATH" ]; then
    echo "Removing existing directory at $REPO_PATH."
    rm -rf "$REPO_PATH"
fi

# Create the directory and clone the repository
mkdir -p "$REPO_PATH"
git clone https://github.com/myahia93/CyberToolbox.git "$REPO_PATH"
cd "$REPO_PATH"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q prettytables requests beautifulsoup4

# Create necessary directories (if any)
echo "Creating necessary directories..."
mkdir -p ~/nikto_reports

# Make main.py executable
chmod +x main.py

# Create a symbolic link for the cybertoolbox command
echo "Setting up 'cybertoolbox' command..."
ln -sf "$(pwd)/main.py" /usr/local/bin/cybertoolbox

echo "Installation completed. You can now run the application using the 'cybertoolbox' command."
