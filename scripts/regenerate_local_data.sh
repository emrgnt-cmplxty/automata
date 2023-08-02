#!/bin/bash

# Local environment paths
: ${PROJECT_NAME:="automata"}
: ${EMBEDDING_DATA_DIR:="automata-embedding-data"}
: ${TARGET_DIR:="automata"}


# Remove the old index if it exists
# Note - this assumes that embedding data lives "underneath" scripts dir
if [ -f "$PWD/../$EMBEDDING_DATA_DIR/indices/$PROJECT_NAME.scip" ]; then
    rm $PWD/../$EMBEDDING_DATA_DIR/indices/$PROJECT_NAME.scip
fi


# Version Control
# TODO Find more robust method to control node version
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
nvm install 16.0.0
nvm use 16.0.0

# Run the index and embedding generation
cd ..
echo 'running command', node scip-python/packages/pyright-scip/index index --project-name $PROJECT_NAME --output $EMBEDDING_DATA_PATH/indices/$PROJECT_NAME.scip --target-only $TARGET_DIR

# Note, output path below is relative
node scip-python/packages/pyright-scip/index index --project-name $PROJECT_NAME --output $EMBEDDING_DATA_DIR/indices/$PROJECT_NAME.scip --target-only $TARGET_DIR

poetry run automata run-code-embedding
#poetry run automata run-doc-embedding
cd -
