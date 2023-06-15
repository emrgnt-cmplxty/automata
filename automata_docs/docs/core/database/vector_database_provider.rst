VectorDatabaseProvider
======================

``VectorDatabaseProvider`` is an abstract base class for different types
of vector database providers which allows you to efficiently calculate
similarity between a given symbol embedding and all other embeddings
stored in the database, as well as retrieve all available symbols stored
in the database.

Overview
--------

The main purpose of ``VectorDatabaseProvider`` is to define the
interface for interacting with different types of vector databases. It
provides two main abstract methods, ``calculate_similarity``, which
calculates the similarity between the given vector and vectors in the
database, and ``get_all_symbols``, which returns all the symbols stored
in the database.

``VectorDatabaseProvider`` is usually subclassed to create concrete
implementations for specific vector database types, such as
JSONVectorDatabase, which is a concrete implementation that uses a JSON
file to store and load the vector database.

Related symbols and classes include Symbol, SymbolEmbedding, and
JSONVectorDatabase.

Related Symbols
---------------

-  ``automata_docs.core.database.vector.JSONVectorDatabase``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``

Example
-------

The following example demonstrates how to create an instance of
``JSONVectorDatabase`` (a specific subclass of
``VectorDatabaseProvider``) and use its methods to manage a vector
database.

.. code:: python

   from automata_docs.core.database.vector import JSONVectorDatabase
   from automata_docs.core.symbol.symbol_types import Symbol
   import numpy as np

   # Initialize a JSONVectorDatabase with a path to a JSON file
   file_path = "vector_database.json"
   vector_db = JSONVectorDatabase(file_path)

   # Add a new symbol embedding to the database
   symbol = Symbol.from_string("example.symbol")
   vector = np.random.randn(300)
   embedding = SymbolEmbedding(symbol, vector)
   vector_db.add(embedding)

   # Calculate the similarity between a new vector and the database vectors
   query_vector = np.random.randn(300)
   similarity_results = vector_db.calculate_similarity(query_vector)

   # Retrieve all symbols in the database
   all_symbols = vector_db.get_all_symbols()

Limitations
-----------

The primary limitation of ``VectorDatabaseProvider`` is that it is an
abstract base class and must be subclassed for specific vector database
implementations. Additionally, while it provides the method signatures
for calculating similarity and retrieving all symbols, the actual
implementation details and performance depend upon the underlying vector
database implementation.

Follow-up Questions:
--------------------

-  How can we implement the ``VectorDatabaseProvider`` with different
   storage backends like databases and cloud storages?
-  What is the performance comparison between different vector database
   implementations, and how can it be improved?
