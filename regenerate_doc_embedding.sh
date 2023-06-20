# TODO - Include information on how to configure pyright-scip repository
source local_env/bin/activate
# Build and embed the L2 docs
automata run-doc-embedding-l2
# Build and embed the L3 docs
automata run-doc-embedding-l3
deactivate
