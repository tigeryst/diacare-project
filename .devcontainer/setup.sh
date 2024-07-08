#!/bin/bash

echo "Starting setup script..."

# Install pyenv dependencies
sudo apt-get update
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev \
python3-openssl git

# Install pyenv
curl https://pyenv.run | bash

# Add pyenv to the shell
export PATH="$HOME/.pyenv/bin:$PATH"
export PYENV_ROOT="$HOME/.pyenv"
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc

# Reload shell configuration
source ~/.bashrc

# Install a specific Python version using pyenv
echo "Installing Python 3.10.0 with pyenv..."
pyenv install -s 3.10.0
pyenv global 3.10.0
echo "Python 3.10.0 installation completed."

# Reload the shell configuration again to ensure pyenv's Python is used
source ~/.bashrc

# Install virtualenv
echo "Installing virtualenv..."
~/.pyenv/versions/3.10.0/bin/python -m pip install virtualenv
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
