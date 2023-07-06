Creating Your Own Embeddings
============================

Automata's powerful architecture allows you to create your own code and documentation embeddings. This guide provides you with step-by-step instructions to accomplish that.

Configure the pyright-scip repository
--------------------------------------
Before you start, make sure that you have properly configured the pyright-scip repository. The below steps are needed to create the index using pyright-scip.

.. code-block:: bash

   source local_env/bin/activate
   # Ensure that submodules have been initialized
   git submodule update --init --recursive
   # Install the indexing software
   cd scip-python
   npm install
   cd packages/pyright-scip
   npm run build
   # Return to working dir
   cd ../../../


Next, we will create the index. This will be used to generate the code embeddings.

.. code-block:: bash

   # Create the index and move it into the default location
   node scip-python/packages/pyright-scip/index index  --project-name automata --output index_from_fork.scip  --target-only automata
   mv index_from_fork.scip automata/config/symbol/index.scip

Update the Code Embeddings
--------------------------
Next, we will update the code embeddings. This will use the index we created to generate embeddings from the codebase. The code embeddings will later be used in various downstream tasks such as code similarity search and autocompletion.

.. code-block:: bash

   # Update the code embeddings
   automata run-code-embedding

Under the hood, `run-code-embedding` runs the main function of the script shown below. This function loads the configured symbol graph and code embedding handler. For each symbol in the graph, it calls `process_embedding` on the embedding handler to calculate the symbol's embedding.

.. code-block:: python
   
   # ...
   filtered_symbols = sorted(get_rankable_symbols(all_defined_symbols), key=lambda x: x.dotpath)
   for symbol in tqdm(filtered_symbols):
      try:
         symbol_code_embedding_handler.process_embedding(symbol)
         symbol_code_embedding_handler.embedding_db.save()
      except Exception as e:
         logger.error(f"Failed to update embedding for {symbol.dotpath}: {e}")


Build and Embed the Docs
------------------------
Finally, we will build and embed the documentation. This is useful for tasks like searching the documentation for relevant information.

.. code-block:: bash

   # Build and embed the L2 docs
   automata run-doc-embedding --embedding-level=2
   # Build and embed the L3 docs
   automata run-doc-embedding  --embedding-level=3

Now you have successfully created your own code and documentation embeddings.

