SymbolDatabaseProvider
======================

``SymbolDatabaseProvider`` is an abstract base class that provides a
standard interface for different types of database providers used for
storing and managing symbol embeddings.

Overview
--------

A ``SymbolDatabaseProvider`` defines methods for adding, updating,
getting, discarding, and checking the existence of symbol embeddings.
Subclasses should implement these methods according to their specific
database provider’s requirements.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.database.vector.JSONVectorDatabase``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolEmbeddingHandler``
-  ``automata_docs.core.database.vector.VectorDatabaseProvider``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingsProvider``
-  ``automata_docs.core.symbol.symbol_types.SymbolDescriptor``

Methods
-------

add(embedding: SymbolEmbedding)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The abstract method to add an embedding to the database.

update(embedding: SymbolEmbedding)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The abstract method to update an existing embedding in the database.

get(symbol: Symbol) -> Any
~~~~~~~~~~~~~~~~~~~~~~~~~~

The abstract method to get a specific embedding from the database.

discard(symbol: Symbol)
~~~~~~~~~~~~~~~~~~~~~~~

The abstract method to discard a specific embedding from the database.

contains(symbol: Symbol) -> bool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The abstract method to check if a specific embedding is present in the
database.

clear()
~~~~~~~

The abstract method to clear all embeddings from the database.

load() -> Any
~~~~~~~~~~~~~

The abstract method to load data into the database provider.

save()
~~~~~~

The abstract method to save data from the database provider.

Example
-------

.. code:: python

   from automata_docs.core.symbol.symbol_types import Symbol, SymbolEmbedding
   from automata_docs.core.database.provider import SymbolDatabaseProvider
   from automata_docs.core.database.vector import JSONVectorDatabase

   class CustomDatabaseProvider(SymbolDatabaseProvider):
       def __init__(self):
           self.embedding_db = JSONVectorDatabase("embeddings.json")

       def add(self, embedding: SymbolEmbedding):
           self.embedding_db.add(embedding)

       # Implement other abstract methods according to specific requirements

Limitations
-----------

As an abstract base class, ``SymbolDatabaseProvider`` cannot be directly
instantiated. Subclasses must provide their own implementations of the
abstract methods.

Additionally, ``SymbolDatabaseProvider`` does not provide any specific
functionality related to database management, such as transactions,
caching, or query optimization. It only provides a standard interface to
work with different types of symbol databases.

Follow-up Questions:
--------------------

-  Are there any default concrete implementations for the abstract
   methods in ``SymbolDatabaseProvider``, or does each subclass have to
   provide its own implementations?
