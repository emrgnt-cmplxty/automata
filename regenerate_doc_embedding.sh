# TODO - Include information on how to configure pyright-scip repository
source local_env/bin/activate
node /Users/ocolegrove/scip-python/packages/pyright-scip/index index  --project-name automata --output index_from_fork.scip
mv index_from_fork.scip automata/config/symbol/index.scip
# Build and embed the L2 docs
automata run-doc-embedding-l2
# Build and embed the L3 docs
automata run-doc-embedding-l3
deactivate
