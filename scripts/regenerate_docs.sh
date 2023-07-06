#!/bin/bash

# activate the local_env
source ../local_env/bin/activate

# Update documentation files
automata run-doc-post-process

# Change into docs directory
cd ../docs 

# Generate the FAQ
python3 generate_faq.py

# Return to working dir
cd -

# Optional command to build docs locally - 'sphinx-build -a automata/docs ../docs'

deactivate
