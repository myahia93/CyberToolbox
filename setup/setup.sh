#!/bin/bash

# Check if the script is run as root
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root. Please run it with sudo."
    exit 1
fi

# Define the path where the repository will be cloned
REPO_PATH="/opt/CyberToolbox"

# Automatically remove the directory if it exists
if [ -d "$REPO_PATH" ]; then
    echo "Removing existing directory at $REPO_PATH."
    rm -rf "$REPO_PATH"
fi

# Clone the repository
git clone https://github.com/myahia93/CyberToolbox.git "$REPO_PATH"

# Change to the repository directory
cd "$REPO_PATH"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -q prettytables requests beautifulsoup4

# Create necessary directories (if any)
echo "Creating necessary directories..."
mkdir -p ~/nikto_reports

# Make main.py executable
chmod a+x main.py

# Create a symbolic link for the cybertoolbox command
echo "Setting up 'cybertoolbox' command..."
ln -sf "$(pwd)/main.py" /usr/local/bin/cybertoolbox

echo -e "\e[32mInstallation completed. You can now run the application using the \e[31mcybertoolbox\e[32m command.\e[0m"
