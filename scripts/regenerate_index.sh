#!/bin/bash

# activate local env
# cd into root directory
cd ../

# create index
node scip-python/packages/pyright-scip/index index  --project-name automata --output index_from_fork.scip  --target-only automata
# put into main index location
mv index_from_fork.scip automata-embedding-data/indices/automata.scip

# cd back
cd -