#!/bin/bash

# activate the local_env
source ../local_env/bin/activate

# Update the code embeddings
automata run-code-embedding

deactivate
