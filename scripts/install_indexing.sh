#!/bin/bash

# Activate the local repository
source local_env/bin/activate

# Install scip-python locally
cd ../scip-python
npm install

# Build the tool
cd packages/pyright-scip
npm run build

# Return to working dir
cd ../../../../
