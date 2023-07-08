#!/bin/bash

# activate the local_env

source ../local_env/bin/activate

# Build and embed the L2 docs
automata run-doc-embedding --embedding-level=2

# Build and embed the L3 docs
# NOTE - This is an experimental feature.
# automata run-doc-embedding  --embedding-level=3 

deactivate
