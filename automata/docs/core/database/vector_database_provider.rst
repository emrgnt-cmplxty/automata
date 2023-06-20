VectorDatabaseProvider
======================

``VectorDatabaseProvider`` is an abstract base class for implementing
different types of vector database providers. Its main purpose is to
provide the basic structure for a vector storage system, allowing
developers to easily customize and implement their own solutions.

Subclasses must implement the abstract methods
``calculate_similarity()`` and ``get_all_symbols()`` to work correctly.
``calculate_similarity()`` computes the similarity between a provided
vector and all vectors stored in the database, returning a list of
dictionaries containing each symbol and its similarity score.
``get_all_symbols()`` retrieves a list of all symbols stored in the
database.

Related Symbols
---------------

-  ``automata.core.database.vector.JSONVectorDatabase``
-  ``automata.core.embedding.code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.database.provider.SymbolDatabaseProvider``
-  ``automata.core.embedding.embedding_types.EmbeddingProvider``

Example
-------

The following example demonstrates a basic implementation of the
``VectorDatabaseProvider`` class.

.. code:: python

   class MyVectorDatabase(VectorDatabaseProvider):

       def __init__(self):
           self.data: List[SymbolEmbedding] = []
           self.index: Dict[str, int] = {}

       def calculate_similarity(self, embedding: SymbolEmbedding) -> List[Dict[Symbol, float]]:
           similarities = []
           for stored_embedding in self.data:
               similarity = compute_cosine_similarity(embedding.vector, stored_embedding.vector)
               similarities.append({stored_embedding.symbol: similarity})
           return similarities

       def get_all_symbols(self) -> List[Symbol]:
           return [embedding.symbol for embedding in self.data]

   # Usage
   my_vector_db = MyVectorDatabase()

Limitations
-----------

Since ``VectorDatabaseProvider`` is an abstract base class, it cannot be
used directly. Instead, developers must create a subclass that
implements the required abstract methods. Furthermore, this base class
does not provide any built-in functionality for adding, updating, or
removing symbols and their embeddings. Implementers must handle these
operations in their own subclasses.

Follow-up Questions:
--------------------

-  Are there any pre-built subclasses or examples of using
   ``VectorDatabaseProvider`` in a real project?
-  What are some other examples of vector databases, and how could they
   be implemented using this base class?
