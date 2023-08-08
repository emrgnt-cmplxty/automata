JSONVectorDatabase
==================

Overview
--------

``JSONVectorDatabase`` is an abstraction that provides a vector database
which saves its elements in a JSON file. It’s a simple yet effective way
to utilize the file system as storage for vectors. It’s designed to be
general, implementing the ``VectorDatabaseProvider`` interface, and is
also modular with types ``K`` for keys and ``V`` for values provided in
a generic fashion.

It can handle basic database operations like adding, getting, and
discarding entries individually or in batches, as well as ability to
update entries. Additional functionalities include checking if a key
exists, getting all ordered embeddings, and clearing all entries in the
database.

Note that ``JSONVectorDatabase`` was not designed with efficiency in
mind and might become slow when handling large number of vectors.

Related Symbols
---------------

-  ``VectorDatabaseProvider``: The interface implemented by
   ``JSONVectorDatabase``.
-  ``jsonpickle``: Used in encoding and decoding objects for JSON
   representation.

Example
-------

The following is an example demonstrating how to use
``JSONVectorDatabase``.

.. code:: python

   from automata.core.base.database.vector_database import JSONVectorDatabase

   # Define custom database with string keys and int value vectors
   class CustomDatabase(JSONVectorDatabase[str, int]):
       def get_ordered_keys(self):
           return sorted(self.index.keys())
           
       def entry_to_key(self, entry):
           return str(entry)

   db = CustomDatabase("/path/to/your/database.json")

   # Add entries to the database
   db.add(5)
   db.add(7)
   db.add(2)

   # Save the database to the JSON file
   db.save()

   # Load the database from the JSON file
   db.load()

   # Prints [2, 5, 7]
   print(db.get_all_ordered_embeddings())

Limitations
-----------

``JSONVectorDatabase`` has some limitations. The JSON file format is not
designed to support large datasets, so performance may degrade when
handling large number of vectors. It is also not designed with
concurrency in mind, so concurrent writes and reads might lead to
inconsistent data.

Follow-up Questions:
--------------------

-  What is a good alternative to JSON for handling larger databases more
   efficiently?
-  How can we modify ``JSONVectorDatabase`` to support concurrent writes
   and reads?
