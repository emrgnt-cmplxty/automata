# TODO - Include information on how to configure pyright-scip repository
source local_env/bin/activate
# Build and embed the L2 docs
automata run-doc-embedding --embedding-level=2
# Build and embed the L3 docs
automata run-doc-embedding  --embedding-level=3
deactivate
