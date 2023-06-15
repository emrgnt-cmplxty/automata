JSONVectorDatabase
==================

``JSONVectorDatabase`` is a concrete class that provides a vector
database that saves into a JSON file. It is a subclass of the
``VectorDatabaseProvider`` and allows adding, updating, and removing
vector embeddings related to different symbols. The class offers methods
to load and save the vector database from and into a JSON file,
respectively.

Related Symbols
---------------

-  ``automata_docs.core.database.provider.SymbolDatabaseProvider``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``

Example
-------

The following example demonstrates how to create an instance of
``JSONVectorDatabase`` with a given file path, add symbols, save the
database, and retrieve the saved embeddings.

.. code:: python

   from automata_docs.core.database.vector import JSONVectorDatabase
   from automata_docs.core.symbol.symbol_types import Symbol, SymbolEmbedding

   file_path = "path/to/json/file.json"
   vector_db = JSONVectorDatabase(file_path)

   symbol_0 = Symbol.from_string("sample_symbol_0")
   symbol_1 = Symbol.from_string("sample_symbol_1")

   embedding_0 = SymbolEmbedding(symbol_0, [1, 2, 3])
   embedding_1 = SymbolEmbedding(symbol_1, [1, 2, 3, 4])

   vector_db.add(embedding_0)
   vector_db.add(embedding_1)

   vector_db.save()

   loaded_embedding_0 = vector_db.get(symbol_0)
   loaded_embedding_1 = vector_db.get(symbol_1)

   print(loaded_embedding_0.vector)
   print(loaded_embedding_1.vector)

Limitations
-----------

The primary limitation of ``JSONVectorDatabase`` is that it currently
does not implement the ``calculate_similarity`` method, which is meant
to calculate the similarity between a given vector and the vectors in
the database. Additionally, the storage format is limited to JSON only,
and there is no support for other formats, such as binary file formats
which can provide better performance and space-efficiency for large
vector databases.

Follow-up Questions:
--------------------

-  What is the directory structure expected of the JSON files used by
   this vector database?
-  What is the specific similarity measure intended to be used when
   implementing the ``calculate_similarity`` method?
