#!/bin/bash

## Default values

# Local environment paths
: ${EMBEDDING_DATA_PATH:="../embedding_data"}
: ${REPO_STORE_PATH:="../../repo_store"}
: ${FACTORY_PATH:="../automata_embedding_factory"}

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

# Remove the old index
rm $EMBEDDING_DATA_PATH/indices/$project_name.scip

# Change directory to FACTORY_PATH
mkdir -p $FACTORY_PATH
cd $FACTORY_PATH

# Move the project to the factory
mv $REPO_STORE_PATH/$project_name .
node ../scip-python/packages/pyright-scip/index index --project-name $project_name --output $EMBEDDING_DATA_PATH/indices/$project_name.scip  --target-only $project_name/$project_py_dir

# Determine whether on MacOS or Linux, then run the appropriate sed command
# if [[ $(uname) == "Darwin" ]]; then
#     sed -i '' 's/'$project_name'\.'$project_name'/'$project_name'/g' $EMBEDDING_DATA_PATH/indices/$project_name.scip
# else
#     sed -i 's/'$project_name'\.'$project_name'/'$project_name'/g' $EMBEDDING_DATA_PATH/indices/$project_name.scip
# fi

# We need to perform a find and replace on the project name 
# Because we run the indexing out of FACTORY_PATH
# e.g. automata.automata -> automata.
# perl -pi -e 's/'$project_py_dir'\.'$project_name'/'$project_py_dir'/g' $EMBEDDING_DATA_PATH/indices/$project_name.scip


# Return the data
mv $project_name $REPO_STORE_PATH