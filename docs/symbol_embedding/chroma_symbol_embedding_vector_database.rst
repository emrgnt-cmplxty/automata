ChromaSymbolEmbeddingVectorDatabase
===================================

``ChromaSymbolEmbeddingVectorDatabase`` is a concrete implementation of
a vector database that saves into a Chroma database. It extends the
functionality of ``ChromaVectorDatabase``, allowing storage, retrieval,
and manipulation of ``SymbolEmbedding`` instances.

Overview
--------

``ChromaSymbolEmbeddingVectorDatabase`` provides a variety of methods to
manage entries in the chroma database including adding single or batches
of entries (``add()`` and ``batch_add()``), retrieving entries by their
keys (``get()``, ``batch_get()``) or all entries in a sorted order
(``get_ordered_entries()``, ``get_ordered_keys()``), and updating single
or multiple entries (``update_entry()``, ``batch_update()``). In
addition, it also offers functionality to generate a hashable key from a
``SymbolEmbedding`` instance with ``entry_to_key()`` method.

Related Symbols
---------------

-  ``automata.symbol_embedding.base.SymbolEmbedding``
-  ``automata.core.base.database.vector.ChromaVectorDatabase``
-  ``chromadb.api.types.GetResult``

Example
-------

This is a simplified usage example of
``ChromaSymbolEmbeddingVectorDatabase``:

.. code:: python

   from automata.symbol_embedding.base import SymbolEmbedding
   from automata.symbol_embedding.vector_databases import ChromaSymbolEmbeddingVectorDatabase

   factory = SymbolEmbedding 
   collection_name = "test_collection"

   # Instantiate ChromaSymbolEmbeddingVectorDatabase
   database = ChromaSymbolEmbeddingVectorDatabase(collection_name, factory)

   # Add an entry
   entry = factory(symbol=Symbol, document="some document", vector=np.array([1, 2, 3]))
   database.add(entry)

   # Retrieve entry
   retrieved = database.get(database.entry_to_key(entry))

   # Update entry
   entry.vector = np.array([4, 5, 6])
   database.update_entry(entry)

   # Delete entry
   database.discard(database.entry_to_key(entry))

Note
----

This class does not check if the chroma database instance used is
connected to a database. It’s the user’s responsibility to manage the
chroma database connection.

Follow-up Questions:
--------------------

-  How is this class handling connection errors to the Chroma Database?
-  Is there a way to manage the database connection from within this
   class?
-  Are there any limitations regarding the size of the symbol vectors
   that can be stored in the database?
