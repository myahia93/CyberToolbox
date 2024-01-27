#!/bin/bash

# Path where the repository will be cloned
REPO_PATH="$HOME/CyberToolbox"

# Check if the directory already exists
if [ -d "$REPO_PATH" ]; then
    echo "The directory $REPO_PATH already exists."
    read -p "Do you want to remove it and continue with the installation? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing existing directory and continuing with installation."
        rm -rf "$REPO_PATH"
    else
        echo "Installation cancelled."
        exit 1
    fi
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
sudo ln -sf "$(pwd)/main.py" /usr/local/bin/cybertoolbox

echo "Installation completed. You can now run the application using the 'cybertoolbox' command."
