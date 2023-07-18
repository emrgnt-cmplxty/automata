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
node ../scip-python/packages/pyright-scip/index index --project-name $project_name --output $EMBEDDING_DATA_PATH/indices/$project_py_dir.scip  --target-only $project_py_dir

cd .. && poetry run automata run-code-embedding
# Return to root
cd -
rm -rf $FACTORY_PATH
