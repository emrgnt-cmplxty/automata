ChromaSymbolEmbeddingVectorDatabase
===================================

``ChromaSymbolEmbeddingVectorDatabase`` is a vector database class
responsible for managing the storage, retrieval, and update of vectors
associated with different symbols in the chroma vector database.

Overview
--------

``ChromaSymbolEmbeddingVectorDatabase`` inherits from the classes
``ChromaVectorDatabase`` and ``IEmbeddingLookupProvider`` to provide
functionality like adding, fetching, and updating embedding vectors in
sorted order. This class acts as a handler to interact with a symbol
embedding collection in a Chroma database.

The class provides utility methods to generate a hashable key from a
symbol, raise a KeyError if a duplicate entry exists, and prepare
entries for insertion into the database. It also has methods for adding
single or multiple entries and updating existing ones.

Related Symbols
---------------

Due to the highly specialized nature of this class, it doesn’t have a
wide range of directly related symbols. But the class uses following
symbols: - ``V``: A generic type parameter representing the type of the
vector embedded in the database entry.

Example
-------

The examples are mainly theoretical because this class is expected to be
used in a larger system with Chroma database installed.

.. code:: python

   # Assuming we have a collection name, factory function to create vector and directory to store
   collection_name = "test_collection"
   factory = lambda: None  # Placeholder for an actual factory function
   directory = "/path/to/directory"

   chroma_db = ChromaSymbolEmbeddingVectorDatabase(collection_name, factory, directory)

   # Add entry to collection
   entry = factory()  # Get the entry using the factory function
   chroma_db.add(entry)

   # Get an entry from the collection
   key = "somekey"  # Placeholder for an actual key
   entry = chroma_db.get(key)

   # Update entry in collection
   chroma_db.update_entry(entry)

Limitations
-----------

The class ``ChromaSymbolEmbeddingVectorDatabase`` is heavily dependent
on the installed Chroma database and a suitable configured collection.

Also, it requires a factory function responsible for creating instances
of the generic type ``V``. This may be a potential limitation factor, as
it requires the client code to supply a factory function conforming to
its requirements.

It doesn’t provide functionality to delete entries from the collection.

Follow-up Questions
-------------------

-  How to provide custom key generation function to generate unique keys
   for entries?
-  How can we execute deletion of entries from the database? Is it a
   necessary feature to have? If so, why it’s not included in the class?
