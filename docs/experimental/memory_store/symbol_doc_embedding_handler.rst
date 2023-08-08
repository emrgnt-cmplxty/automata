SymbolDocEmbeddingHandler
=========================

``SymbolDocEmbeddingHandler`` is a class that handles the embedding of
symbols. It inherits from the ``SymbolEmbeddingHandler`` and adds the
functionality to handle specific embeddings for documentation associated
with Python symbols, i.e., classes or functions.

Overview
--------

The ``SymbolDocEmbeddingHandler`` processes the embedding for symbols,
it fetches the embedding source code for the symbol and supports
functionality to either ``update_existing_embedding`` or
``_create_new_embedding`` . It also has the attribute ``overwrite``
which dictates if an existing embedding should be overwritten with a new
one.

Related Symbols
---------------

-  ``automata.experimental.symbol_embedding.symbol_doc_embedding_builder.SymbolDocEmbeddingBuilder``
-  ``automata.symbol_embedding.symbol_embedding_handler.SymbolEmbeddingHandler``
-  ``automata.singletons.dependency_factory.DependencyFactory.create_symbol_doc_embedding_handler``
-  ``automata.experimental.tools.builders.document_oracle_builder.DocumentOracleToolkitBuilder``
-  ``automata.experimental.search.symbol_search.SymbolSearch``
-  ``automata.symbol_embedding.vector_databases.ChromaSymbolEmbeddingVectorDatabase``
-  ``automata.embedding.embedding_base.EmbeddingHandler``
-  ``automata.cli.scripts.run_doc_embedding.initialize_providers``
-  ``automata.symbol_embedding.symbol_embedding_base.SymbolEmbedding``
-  ``automata.embedding.embedding_base.EmbeddingVectorProvider``

Example
-------

Here is example usage of the ``SymbolDocEmbeddingHandler``.

.. code:: python

   from automata.experimental.memory_store.symbol_doc_embedding_handler import SymbolDocEmbeddingHandler
   from automata.experimental.symbol_embedding.symbol_doc_embedding_builder import SymbolDocEmbeddingBuilder
   from automata.symbol_embedding.vector_databases import ChromaSymbolEmbeddingVectorDatabase

   # Assume 'symbol' is an instance of Symbol for a class or function
   # Assume 'source_code' is a string containing Python code

   # Create instance of SymbolDocEmbeddingHandler
   embedding_db = ChromaSymbolEmbeddingVectorDatabase('PYTHON_CODE')
   embedding_provider = EmbeddingVectorProvider()
   embedding_builder = SymbolDocEmbeddingBuilder(embedding_provider)
   sde_handler = SymbolDocEmbeddingHandler(embedding_db, embedding_builder, batch_size=1)

   # Process embedding for symbol
   sde_handler.process_embedding(symbol)

Limitations
-----------

The ``SymbolDocEmbeddingHandler`` currently only supports a
``batch_size`` of 1, meaning it processes one symbol at a time. If a
different ``batch_size`` is used, it raises a ``ValueError``.

Follow-up Questions:
--------------------

-  What is the reason for the ``batch_size`` being 1, and are there any
   plans to add support for larger batch sizes?
-  What strategies can be used for addressing cases where the symbol to
   be processed does not have source code? Currently, a ``ValueError``
   is raised, but would there be value in handling these cases
   differently, like default behavior or user-defined action?
