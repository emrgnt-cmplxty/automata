# TODO - Include information on how to configure pyright-scip repository
source local_env/bin/activate
node /Users/ocolegrove/scip-python/packages/pyright-scip/index index  --project-name automata_docs --output index_from_fork.scip
mv index_from_fork.scip automata_docs/configs/symbols/index.scip
automata-docs run-code-embedding
deactivate