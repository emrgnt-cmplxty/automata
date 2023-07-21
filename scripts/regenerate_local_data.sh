#!/bin/bash

## Default values

# Local environment paths
: ${EMBEDDING_DATA_PATH:="../automata-embedding-data"}
: ${FACTORY_PATH:="../automata_embedding_factory"}

project_name="automata"
project_py_dir="automata"

# Remove the old index if it exists
if [ -f "$EMBEDDING_DATA_PATH/indices/$project_name.scip" ]; then
    rm $EMBEDDING_DATA_PATH/indices/$project_name.scip
fi

# Change directory to FACTORY_PATH
mkdir -p $FACTORY_PATH
cd $FACTORY_PATH

# Copy the project to the factory
rm -rf $project_name && cp -rf ../$project_name .
node ./scip-python/packages/pyright-scip/index index --project-name automata --output automata-embedding-data/indices/automata.scip --target-only automata

cd ..
poetry run automata run-code-embedding
poetry run automata run-doc-embedding

# Return to root
cd -
rm -rf $FACTORY_PATH
