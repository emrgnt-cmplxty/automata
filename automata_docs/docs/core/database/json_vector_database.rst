JSONVectorDatabase
==================

``JSONVectorDatabase`` is a concrete implementation of a vector database
that saves data into a JSON file. It provides methods to add, update,
get, and discard vector embeddings for a given symbol and can work with
``SymbolEmbedding`` objects. The database maintains an internal data
structure that associates symbols with their respective_embeddings, and
the symbols are indexed for fast access.

Overview
--------

``JSONVectorDatabase`` provides a simple and effective way to work with
vector embeddings stored as a JSON file. It offers essential
functionality for managing a database of vector embeddings, such as
adding, removing, updating, and checking for the presence of specific
embeddings. The database uses ``jsonpickle`` to encode and decode data
structures to and from JSON format, ensuring compatibility with other
tools and libraries.

Related Symbols
---------------

-  ``automata_docs.core.database.vector.VectorDatabaseProvider``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.symbol.symbol_types.Symbol``

Example
-------

The following is an example that demonstrates how to create and use a
``JSONVectorDatabase``.

.. code:: python

   from automata_docs.core.database.vector import JSONVectorDatabase
   from automata_docs.core.symbol.symbol_types import SymbolEmbedding, Symbol
   import numpy as np

   file_path = "vector_db.json"
   vector_db = JSONVectorDatabase(file_path)

   symbol = Symbol.parse("scip-python python automata_docs some_version some_symbol#")
   embedding_vector = np.array([1.0, 2.0, 3.0])

   embedding = SymbolEmbedding(symbol, embedding_vector)
   vector_db.add(embedding)

   embedding_from_db = vector_db.get(symbol)
   vector_db.update(embedding)
   vector_db.discard(symbol)

Limitations
-----------

-  The ``calculate_similarity`` method is not implemented in
   ``JSONVectorDatabase`` and needs to be provided in the derived class
   or an external utility function used to compute similarity.
-  The JSON storage format may not be practical for very large vector
   databases, as it requires loading the entire database into memory.

Follow-up Questions:
--------------------

-  How can we extend this implementation to support calculating
   similarity between vectors within the database?
-  How can we improve the storage format to handle large databases more
   efficiently?
