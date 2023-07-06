JSONVectorDatabase
==================

``JSONVectorDatabase`` is a concrete class providing a vector database
that implements storage and retrieval operations into a JSON file.

Overview
--------

The ``JSONVectorDatabase`` performs the following operations:

-  Initialize an empty vector database or load an existing one from a
   JSON file.
-  Add and discard entries in the vector database.
-  Check if a certain entry exists in the vector database.
-  Get a specific entry from the vector database based on its key.
-  Load the vector database from a JSON file and save it back to the
   JSON file.
-  Update an existing entry in the vector database.

Related Symbols
---------------

-  ``automata.core.base.database.vector.VectorDatabaseProvider``: An
   abstract base class that ``JSONVectorDatabase`` inherits from, which
   lays out the fundamental methods a vector database should implement.
-  ``automata.tests.unit.test_database_vector.test_init_vector``,
   ``automata.tests.unit.test_database_vector.test_load``,
   ``automata.tests.unit.test_database_vector.test_save``,
   ``automata.tests.unit.test_database_vector.test_delete_symbol``,
   ``automata.tests.unit.test_database_vector.test_add_symbol``,
   ``automata.tests.unit.test_database_vector.test_add_symbols``,
   ``automata.tests.unit.test_database_vector.test_lookup_symbol``: Unit
   test files that provide examples on how to utilize
   ``JSONVectorDatabase``\ ’s methods.

Example
-------

The following is an example demonstrating the usage of
``JSONVectorDatabase``.

.. code:: python

   from automata.core.base.database.vector import JSONVectorDatabase

   file_path = "db.json"
   vector_db = JSONVectorDatabase(file_path)

   # Add an entry
   vector_db.add("apple")
   assert vector_db.contains("apple")

   # Save the database to the json file
   vector_db.save()

   # Discard an entry
   vector_db.discard("apple")
   assert not vector_db.contains("apple")

   # Load the database from the json file
   vector_db.load()

   # Update an entry
   vector_db.update_database("banana")

Limitations
-----------

``JSONVectorDatabase`` currently only supports JSON files and does not
maintain order when loading back from the file due to the inherent
property of JSON objects. Additionally, the entry keys in the vector
database are strictly hashable, limiting the types of objects you can
add in the database.

Follow-up Questions:
--------------------

-  Is it possible to extend the functionality of ``JSONVectorDatabase``
   to support other file types, i.e., csv or yaml?
-  What happens when we try to add an object to the database that is not
   hashable as an entry?
-  Can we consider using ordered dictionaries (collections.OrderedDict
   in Python) to maintain the order when loading and saving databases?
