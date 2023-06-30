JSONVectorDatabase
==================

Overview
--------

``JSONVectorDatabase`` is a concrete class that offers an interface to a
database backed by a JSON file, primarily used to store vectors. It
defines key methods to perform basic database operations such as adding
a new entry (``add``), checking if an entry exists (``contains``),
removing an entry (``discard``), fetching an entry (``get``) and
updating an entry (``update_database``). The class also provides methods
to save (``save``) the database to a JSON file and load (``load``) the
data from the JSON file.

Related Symbols
---------------

-  ``automata.core.base.database.vector.JSONEmbeddingVectorDatabase``
-  ``automata.tests.unit.test_database_vector.test_init_vector``
-  ``automata.tests.unit.test_database_vector.test_load``
-  ``automata.tests.unit.test_database_vector.test_save``
-  ``automata.tests.unit.test_database_vector.test_delete_symbol``
-  ``automata.tests.unit.test_database_vector.test_add_symbol``
-  ``automata.tests.unit.test_database_vector.test_add_symbols``
-  ``automata.tests.unit.test_database_vector.test_lookup_symbol``
-  ``automata.core.base.database.vector.VectorDatabaseProvider``

Example
-------

The following is an example demonstrating usage of the
``JSONVectorDatabase`` class.

.. code:: python

   from automata.core.base.database.vector import JSONVectorDatabase
   from automata.core.symbol.base import SymbolEmbedding

   # Creating an instance of JSONVectorDatabase
   vector_db = JSONVectorDatabase("path_to_json_file.json")

   # Adding an entry
   embedded_symbol = SymbolEmbedding("symbol", [1,2,3])
   vector_db.add(embedded_symbol)

   # Checking if symbol exists
   print(vector_db.contains("symbol"))  # Returns True

   # Fetching an entry
   fetched_symbol = vector_db.get("symbol")  

   # Removing an entry
   vector_db.discard("symbol")

   # Saving the database to the file
   vector_db.save()

Please replace ``"path_to_json_file.json"`` and “``symbol``” with actual
file path and symbol name respectively.

Limitations
-----------

``JSONVectorDatabase`` is reliant on the filesystem to load and store
the data and as such, any issues with file permissions or disk space can
impact the ability to use this class effectively. Additionally, as it
works on the process of storing vectors in JSON format, it might not be
efficient to use for large database due to memory limitations, and could
have slower data retrieval times.

Follow-up Questions:
--------------------

-  Is there a maximum size limit to the JSON file that can be used?
-  How does it handle concurrent read and write operations on the
   database?
-  Can we configure the load and save operations to work with a remote
   storage service, instead of a local filesystem?
