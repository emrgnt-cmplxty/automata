#!/bin/bash

# activate local env
source ../local_env/bin/activate

# cd into root directory
cd ../

# create index
node scip-python/packages/pyright-scip/index index  --project-name automata --output index_from_fork.scip  --target-only automata
# put into main index location
mv index_from_fork.scip automata/config/symbol/automata.scip

# cd back
cd -

deactivate
