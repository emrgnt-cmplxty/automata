# TODO - Include information on how to configure pyright-scip repository
source local_env/bin/activate
node scip-python/packages/pyright-scip/index index  --project-name automata --output index_from_fork.scip  --target-only automata
mv index_from_fork.scip automata/config/symbol/index.scip
deactivate
