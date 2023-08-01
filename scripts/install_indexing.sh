#!/bin/bash

# Version Control - 
# TODO Find more robust method to control node version
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
nvm install 16.0.0
nvm use 16.0.0

# Install scip-python locally
cd ../scip-python
npm install

# Build the tool
cd packages/pyright-scip
npm run build

# Return to working dir
cd ../../../../
