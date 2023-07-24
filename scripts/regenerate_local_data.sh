#!/bin/bash

## Default values
project_name="automata"

# Local environment paths
: ${EMBEDDING_DATA_PATH:="../automata-embedding-data"}

# Remove the old index if it exists
if [ -f "$EMBEDDING_DATA_PATH/indices/$project_name.scip" ]; then
    rm $EMBEDDING_DATA_PATH/indices/$project_name.scip
fi

# Change directory to FACTORY_PATH
mkdir -p $FACTORY_PATH
cd $FACTORY_PATH

# Copy the project to the factory
rm -rf $project_name && cp -rf ../$project_name .
nvm use
node ../scip-python/packages/pyright-scip/index index --project-name $project_name --output $EMBEDDING_DATA_PATH/indices/$project_py_dir.scip  --target-only $project_py_dir

# Run the project
cd ..
node ./scip-python/packages/pyright-scip/index index --project-name $project_name --target-only $project_name

mv index.scip automata-embedding-data/indices/$project_name.scip 
poetry run $project_name run-code-embedding
poetry run $project_name run-doc-embedding

# Return to root
cd -
