# TODO - Include information on how to configure pyright-scip repository
source local_env/bin/activate
node /Users/ocolegrove/scip-python/packages/pyright-scip/index index  --project-name automata --output index_from_fork.scip
mv index_from_fork.scip automata/config/symbol/index.scip
# Update the code embeddings
automata run-code-embedding
deactivate
