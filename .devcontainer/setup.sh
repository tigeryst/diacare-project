#!/bin/bash

echo "Starting setup script..."

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
