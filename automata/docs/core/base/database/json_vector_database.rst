JSONVectorDatabase
==================

``JSONVectorDatabase`` is a concrete class providing a vector database
that saves into a JSON file. It offers a set of methods for adding,
retrieving, and discarding vectors associated with symbols. Also, it
provides the calculation of similarity between vectors and manages these
vectors in a JSON file.

Overview
--------

``JSONVectorDatabase`` allows users to store and manage the embedding
vectors in a JSON file format. It provides methods for adding new
vectors, updating existing vectors, deleting vectors, checking if a
symbol exists in the database, and calculating the similarity between a
given embedding vector and the vectors in the database.

Related Symbols
---------------

-  ``JSONVectorDatabase`` inherits from
   ``automata.core.base.database.vector.VectorDatabaseProvider``
-  ``automata.core.symbol.base.Symbol``
-  ``automata.core.symbol.base.SymbolEmbedding``

Example
-------

The following example demonstrates how to create an instance of
``JSONVectorDatabase`` and perform basic operations like adding and
retrieving vectors associated with symbols.

.. code:: python

   from automata.core.base.database.vector import JSONVectorDatabase
   from automata.core.symbol.base import Symbol, SymbolEmbedding

   file_path = "path/to/json/database.json"
   vector_db = JSONVectorDatabase(file_path)

   # Add a SymbolEmbedding to the database
   symbol = Symbol.from_string("example.Symbol#")
   embedding = SymbolEmbedding(symbol, "embedding_source", [0.1, 0.2, 0.3])
   vector_db.add(embedding)

   # Check if the symbol exists in the database
   exists = vector_db.contains(symbol)
   if exists:
       # Retrieve the vector for the symbol
       retrieved_embedding = vector_db.get(symbol)
       print(retrieved_embedding.vector)

Limitations
-----------

The primary limitation of ``JSONVectorDatabase`` is that it currently
provides a placeholder for the ``calculate_similarity`` method but does
not implement any specific logic for calculating similarity between
vectors. Users are required to implement this functionality themselves
or rely on other libraries that provide similarity measures.

Follow-up Questions:
--------------------

-  What similarity measure should be implemented or recommended for use
   with the ``JSONVectorDatabase`` class?
-  Are there any performance considerations when dealing with large
   embedding databases stored in a JSON file?
