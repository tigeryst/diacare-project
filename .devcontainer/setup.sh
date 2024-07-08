#!/bin/bash

# Update and install dependencies
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

# Install pyenv
curl https://pyenv.run | bash

# Add pyenv to the shell
export PATH="$HOME/.pyenv/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

# Install Python version
pyenv install 3.10.0
pyenv global 3.10.0

# Install virtualenv
pip install virtualenv

# Verify installations
echo "pyenv version:"
pyenv --version
echo "Python version:"
python --version
echo "virtualenv version:"
virtualenv --version
