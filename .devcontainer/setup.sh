#!/bin/bash

echo "Starting setup script..."

# Install Homebrew
echo "Installing Homebrew..."
NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo "Homebrew installation completed."

# Add Homebrew to PATH
echo "Adding Homebrew to PATH..."
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> $HOME/.profile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
echo "Homebrew added to PATH."

# Install pyenv using Homebrew
echo "Installing pyenv with Homebrew..."
brew install pyenv
echo "pyenv installation completed."

# Initialize pyenv
echo "Initializing pyenv..."
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
echo "pyenv initialization completed."

# Install a specific Python version using pyenv
echo "Installing Python 3.10.0 with pyenv..."
pyenv install -s 3.10.0
pyenv global 3.10.0
echo "Python 3.10.0 installation completed."

# Install virtualenv
echo "Installing virtualenv..."
pip install virtualenv
echo "virtualenv installation completed."

# Verify installations
echo "Verifying installations..."
echo "pyenv version:"
pyenv --version
echo "Python version:"
python --version
echo "virtualenv version:"
virtualenv --version
echo "Verification completed."

echo "Setup script completed successfully."
