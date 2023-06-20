JSONVectorDatabase
==================

``JSONVectorDatabase`` is a concrete class to provide a vector database
that saves into a JSON file. It is part of the Automata documentation
processing pipeline and is responsible for loading, saving, adding,
updating, and discarding SymbolEmbedding objects in a JSON file. The
class also includes methods for calculating similarity between vectors
and retrieving all symbols present in the database.

Related Symbols
---------------

-  ``automata.core.database.provider.SymbolDatabaseProvider``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.symbol.symbol_types.SymbolEmbedding``
-  ``numpy``

Example
-------

The following example demonstrates how to initialize a
``JSONVectorDatabase``, add and retrieve ``SymbolEmbedding`` objects
from it, and save the database to a JSON file.

.. code:: python

   from automata.core.database.vector import JSONVectorDatabase
   from automata.core.symbol.symbol_types import Symbol, SymbolEmbedding
   import numpy as np

   # Initialize the JSONVectorDatabase
   vector_db = JSONVectorDatabase("example_vector_db.json")

   # Create SymbolEmbeddings
   symbol_1 = Symbol.from_string("scip-python python automata example_symbol_1#")
   embedding_1 = SymbolEmbedding(symbol_1, "embedding_source", np.array([1, 2, 3]))

   symbol_2 = Symbol.from_string("scip-python python automata example_symbol_2#")
   embedding_2 = SymbolEmbedding(symbol_2, "embedding_source", np.array([4, 5, 6]))

   # Add SymbolEmbeddings to the database
   vector_db.add(embedding_1)
   vector_db.add(embedding_2)

   # Retrieve embedding for a specific symbol
   retrieved_embedding = vector_db.get(symbol_1)

   # Save the vector database to a JSON file
   vector_db.save()

Limitations
-----------

The class currently has a ``NotImplementedError`` for the
``calculate_similarity`` method, which means there is no logic
implemented for calculating similarity between vectors.

Follow-up Questions:
--------------------

-  What similarity measure should be used for calculating similarity
   between vectors in the database?
-  Is there more efficient storage structure to use other than a JSON
   file?
