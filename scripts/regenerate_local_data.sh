#!/bin/bash

## Default values

# Local environment paths
: ${EMBEDDING_DATA_PATH:="../automata-embedding-data"}

# Project-specific paths
# The project name corresponds to the name of the directory in the data_repos directory
# This should typically correspond to the underlying github repository
project_name="automata"
# The directory within the project which contains the python code to be indexed
# For example, in automata the main python code is located in the automata/ directory
project_py_dir="automata"

# Set the locale to handle any potential sed illegal byte sequence errors
# export LC_ALL=C

# Parse command-line arguments
while getopts ":p:r:" opt; do
  case ${opt} in
    p ) project_name=$OPTARG
      ;;
    r ) project_py_dir=$OPTARG
      ;;
    \? ) echo "Usage: cmd [-p project_name] [-r project_py_dir]"
      ;;
  esac
done

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
