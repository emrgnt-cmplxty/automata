ChromaVectorDatabase
====================

``ChromaVectorDatabase`` is a concrete class defined in the
``automata.core.base.database.vector_database`` module. The main purpose
of this class is to use Chroma, a live vector database, for persistent
storage of vectors. Its functionalities include common database
operations like adding either a single entry or a batch of entries,
updating entries, deleting entries by key, and performing organized
retrieval of keys and embeddings. The class also offers provisions to
create and set up a client for Chroma using the persistence directory.

Overview
--------

The ``ChromaVectorDatabase`` is an implementation of the
``VectorDatabaseProvider`` and ``Generic[K, V]`` interfaces, aiming to
establish and manage a connection with a Chroma database per collection.
The constructor (``__init__``) sets up the Chroma client and the
collection to be used according to the input parameters. Provided
utility methods like ``load``, ``save``, ``clear``, and ``contains``
allow for efficient management of the database and its entries.
Furthermore, ``ChromaVectorDatabase`` specifies abstract methods (to be
implemented in subclasses) for specific database operations that depend
on the type of keys and the order of entries.

Related Symbols
---------------

-  ``VectorDatabaseProvider``: Interface that ``ChromaVectorDatabase``
   class implements.
-  ``Generic[K, V]``: Python’s Generic class used for flexible type
   hints.
-  ``chromadb``: Chroma client library that gets imported as part of
   Chroma setup.
-  ``Settings``: Chroma DB settings object.

Example
-------

Below is an example of how you can use the ``ChromaVectorDatabase``:

.. code:: python

   from automata.core.base.database.vector_database import ChromaVectorDatabase

   # Instantiate ChromaVectorDatabase with a collection name and persistent directory.
   collection_name = "my_collection"
   persist_dir = "/path/to/persistent/directory"
   chroma_db = ChromaVectorDatabase(collection_name=collection_name, persist_directory=persist_dir)

   # Add data to Chroma DB (data format depends on K and V types defined in the subclass)
   # chroma_db.add(data)

   # Check if specific key exists in the collection
   # exists = chroma_db.contains(key)

   # Clear data in the Chroma DB collection
   chroma_db.clear()

Please note that the ``ChromaVectorDatabase`` class is abstract, and
requires several methods such as ``add(data)`` and ``contains(key)`` to
be implemented in a subclass to specify the behavior according to the
required key and value types.

Limitations
-----------

The ``ChromaVectorDatabase`` class depends on the Chroma client library
(``chromadb``), which may need to be installed
(“``pip install chromadb``”) before use. Additionally, the class relies
heavily on the specific way Chroma client manages and interacts with
collections. Any changes to Chroma client’s functionality may require
corresponding changes in this class. Furthermore, this class is an
abstract class which means you cannot directly instantiate this class.

Can consider adding detailed descriptions and usage examples for the
abstract methods to provide further guidance on how to implement these
methods in a subclass. Other operations, like achieving concurrent or
multi-threaded write operations, might require advanced handling and
additional care at the implementation level.

Follow-up Questions:
--------------------

-  Is there an example of a subclass implementation from this abstract
   base class (``ChromaVectorDatabase``) in the project?
-  What is the behavior when a simultaneously read and write operation
   occurs in this database? To what extent does it handle concurrency?
-  Are there mechanisms in place for handling cases when the Chroma
   client or the persistence directory is not accessible or fails?
-  What are the specific formatting or restrictions on the key (K) and
   value (V) types, especially when considering the need for ordered
   keys and embeddings?
-  Given that this class deals with storing and retrieving vector data,
   how do we handle high-dimensional vectors or large amounts of vector
   data?
-  How does this class interact with the rest of the system (agents,
   handlers, etc.)?
