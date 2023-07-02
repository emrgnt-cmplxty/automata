VectorDatabaseProvider
======================

``VectorDatabaseProvider`` is an abstract base class for different types
of vector database providers. It provides a foundation for implementing
concrete classes capable of calculating similarities between vectors and
storing/retrieving them in a database.

Overview
--------

``VectorDatabaseProvider`` contains two abstract methods,
``calculate_similarity`` and ``get_all_symbols``, which are implemented
by concrete subclasses. These methods define the core functionality
expected by any vector database provider: calculating similarity between
a given vector and vectors in the database, and retrieving all symbol
instances from the database.

Related Symbols
---------------

-  ``automata.core.database.provider.SymbolDatabaseProvider``
-  ``automata.core.database.vector.JSONEmbeddingVectorDatabase``
-  ``automata.core.symbol.base.Symbol``
-  ``automata.core.symbol_embedding.base.SymbolEmbedding``
-  ``automata.core.memory_store.embedding_types.SymbolEmbeddingHandler``
-  ``automata.core.memory_store.symbol_code_embedding.SymbolCodeEmbeddingHandler``

Example
-------

The following example demonstrates how to create a custom vector
database provider by extending the ``VectorDatabaseProvider`` abstract
base class.

.. code:: python

   from automata.core.database.vector import VectorDatabaseProvider
   from typing import Dict, List
   from automata.core.symbol.base import Symbol, SymbolEmbedding

   class CustomVectorDatabaseProvider(VectorDatabaseProvider):
       def calculate_similarity(self, embedding: SymbolEmbedding) -> Dict[Symbol, float]:
           # Implement the method to calculate similarity
           pass
       
       def get_all_symbols(self) -> List[Symbol]:
           # Implement the method to get all symbol instances
           pass

   custom_vector_database_provider = CustomVectorDatabaseProvider()

Limitations
-----------

The primary limitation of ``VectorDatabaseProvider`` is that it only
provides a basis for creating vector database providers. Developers must
extend this abstract base class and implement the required methods
according to their specific requirements, including the choice of
database (e.g., file-based, in-memory, or remote) and similarity
calculation method (e.g., cosine similarity, euclidean distance, or
custom measures).

Follow-up Questions:
--------------------

-  Are there any default implementations of ``VectorDatabaseProvider``
   that can be used out-of-the-box?
-  What is the preferred similarity measure for comparing vectors in the
   database?
