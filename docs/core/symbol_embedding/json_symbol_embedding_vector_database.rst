JSONSymbolEmbeddingVectorDatabase
=================================

``JSONSymbolEmbeddingVectorDatabase`` is a concrete class under
``automata.symbol_embedding.base`` module used to map symbols to
their vector representation in a JSON file. This class is an extension
of the ``automata.core.base.database.vector.JSONVectorDatabase`` class,
it provides similar functionality with additional methods to handle
symbol embeddings.

The ``JSONSymbolEmbeddingVectorDatabase`` class is typically used in
operations where there is a need to store, retrieve and manage symbol
embeddings in a JSON file.

Related Symbols
---------------

-  ``automata.symbol_embedding.base.SymbolCodeEmbedding``
-  ``automata.core.base.database.vector.JSONVectorDatabase``
-  ``automata.memory_store.symbol_code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.memory_store.symbol_doc_embedding.SymbolDocEmbeddingHandler``

Overview
--------

Below are the most relevant methods in
``JSONSymbolEmbeddingVectorDatabase``:

-  ``__init__(self, file_path: str)``: This method is responsible for
   initializing an instance of the class. The ``file_path`` parameter
   specifies the location of the JSON file.

-  ``entry_to_key(self, entry: SymbolEmbedding) -> str``: This method
   generates a simple hashable key from a Symbol.

-  ``get_ordered_embeddings(self) -> List[SymbolEmbedding]``: This
   method returns the SymbolEmbedding entries sorted by their keys.

Usage Examples
--------------

Below are example usages extracted mainly from the unit test functions:

1. **Instantiating ``JSONSymbolEmbeddingVectorDatabase``**:

.. code:: python

   from automata.symbol_embedding.base import JSONSymbolEmbeddingVectorDatabase

   vector_database = JSONSymbolEmbeddingVectorDatabase("path_to_your_json_file")

2. **Adding embeddings to ``JSONSymbolEmbeddingVectorDatabase``**:

.. code:: python

   from automata.symbol_embedding.base import SymbolCodeEmbedding
   from automata.symbol.base import Symbol

   symbol1 = Symbol("symbol_1")
   symbol2 = Symbol("symbol_2")
   embedding1 = SymbolCodeEmbedding(symbol1, "code_1", [1, 2, 3])
   embedding2 = SymbolCodeEmbedding(symbol2, "code_2", [4, 5, 6])

   vector_database.add(embedding1)
   vector_database.add(embedding2)

3. **Saving the embeddings to the database**:

.. code:: python

   vector_database.save()

4. **Loading embeddings from database**:

.. code:: python

   vector_database.load()

Limitations
-----------

The ``JSONSymbolEmbeddingVectorDatabase`` class does not support
parallel reads and writes to the JSON file. This might pose a problem
when working with large datasets or in multi-threaded environments.

Follow-up Questions
-------------------

-  How does the ``JSONSymbolEmbeddingVectorDatabase`` class handle
   concurrency?
-  Can it work with big datasets efficiently?
-  Can you add versioning or transaction support to handle potential
   read-write conflicts?
