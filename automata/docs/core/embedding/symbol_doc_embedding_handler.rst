SymbolDocEmbeddingHandler
=========================

``SymbolDocEmbeddingHandler`` is a class that helps create and manage
documentation embeddings for symbols in a Python project. It is
responsible for building symbol documentation embeddings, getting
existing symbol embeddings, generating summaries, and updating
embeddings when necessary.

Overview
--------

``SymbolDocEmbeddingHandler`` handles the process of creating and
updating symbol documentation embeddings for a Python project. It
leverages the ``EmbeddingProvider`` to build new embeddings and
``VectorDatabaseProvider`` to store and retrieve existing embeddings.
Additionally, it uses ``SymbolSearch`` to find related symbols for
generating relevant documentation and ``PyContextRetriever`` to retrieve
the context of the primary symbol.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.symbol.symbol_types.SymbolDocEmbedding``
-  ``automata.core.embedding.embedding_types.EmbeddingProvider``
-  ``automata.core.database.vector.VectorDatabaseProvider``
-  ``automata.core.symbol.search.SymbolSearch``
-  ``automata.core.context.py_context.retriever.PyContextRetriever``

Example
-------

The following example demonstrates how to create and manage
documentation embeddings for symbols. Please replace ``Mock`` objects
with the actual implementations, if possible.

.. code:: python

   import logging
   import openai
   from typing import List
   from jinja2 import Template
   from automata.config.prompt.docs import DEFAULT_DOC_GENERATION_PROMPT
   from automata.core.context.py_context.retriever import PyContextRetriever
   from automata.core.database.vector import VectorDatabaseProvider
   from automata.core.symbol.search.symbol_search import SymbolSearch
   from automata.core.symbol.symbol_types import Symbol, SymbolDocEmbedding
   from .embedding_types import EmbeddingProvider, SymbolEmbeddingHandler
   from automata.core.symbol.symbol_utils import convert_to_fst_object  # For mocking purposes

   # Initialize necessary objects
   embedding_db = VectorDatabaseProvider()
   embedding_provider = EmbeddingProvider()
   symbol_search = SymbolSearch()
   retriever = PyContextRetriever()

   # Create a SymbolDocEmbeddingHandler instance
   symbol_doc_embedding_handler = SymbolDocEmbeddingHandler(
       embedding_db=embedding_db,
       embedding_provider=embedding_provider,
       symbol_search=symbol_search,
       retriever=retriever
   )

   # Define a sample Symbol and its source code
   symbol = Symbol.from_string("local module.class_name.method")
   source_code = "def method(self):\n    pass"

   # Build a new SymbolDocEmbedding
   new_embedding = symbol_doc_embedding_handler.build_symbol_doc_embedding(source_code, symbol)

Limitations
-----------

Currently, the logic around updating documentation in
``SymbolDocEmbeddingHandler`` is limited. An improved updating logic
requires understanding when dependencies have changed or interacted to
warrant updating an embedding, which is a non-trivial challenge.

Follow-up Questions:
--------------------

-  How can we implement improved logic for updating documentation
   embeddings in the ``SymbolDocEmbeddingHandler``?
-  Are there additional features that can be added to the
   ``SymbolDocEmbeddingHandler`` to enhance its functionality?
