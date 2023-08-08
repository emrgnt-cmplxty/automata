JSONSymbolEmbeddingVectorDatabase
=================================

``JSONSymbolEmbeddingVectorDatabase`` is a concrete class that provides
a way to handle a vector database that is saved into a JSON file. It
incorporates methods to return ordered keys, retrieve all ordered
embeddings from the dataset, and generate a hashable key from a Symbol.

Overview
--------

This class behaves as a container for a vector database saved in a JSON
file, which can significantly simplify working with symbolic embedding
vectors. The idea is to allow users to easily save, retrieve, and
utilize embedding vectors for their needs. The class inherits mainly
from ``JSONVectorDatabase``, and is designed to work effectively with
``SymbolEmbedding``.

Related Symbols
---------------

Note: There were no related symbols provided in the context for
``JSONSymbolEmbeddingVectorDatabase``.

Example
-------

Below is an example of how to instantiate and use a
``JSONSymbolEmbeddingVectorDatabase``:

.. code:: python

   from automata.symbol_embedding.vector_databases import JSONSymbolEmbeddingVectorDatabase
   from automata.symbol_embedding import SymbolEmbedding

   # Instantiation with a file path
   embed_database = JSONSymbolEmbeddingVectorDatabase("./embeddings.json")

   # Generate a list of ordered keys
   ordered_keys = embed_database.get_ordered_keys()

   # Fetch all ordered embeddings
   ordered_embeddings = embed_database.get_all_ordered_embeddings()

   # Generate a key from the first entry in the database
   key = embed_database.entry_to_key(ordered_embeddings[0])

   print("Ordered Keys:", ordered_keys)
   print("Key of first entry:", key)

Limitations
-----------

The ``JSONSymbolEmbeddingVectorDatabase`` class only supports JSON files
for saving and retrieving symbolic embeddings. So far, there are no
methods designed to use other types of data formats such as CSV, Excel,
etc. Another limitation is that the ordering methods rely on a method
for converting an entry to a key, and any changes in this method will
affect the output of these order-based methods.

Follow-up Questions:
--------------------

-  How can we extend the ``JSONSymbolEmbeddingVectorDatabase`` to work
   with other kinds of file formats such as CSV or Excel?
-  Would it be useful to allow the users to specify their own method for
   creating a key from an entry?
-  Are there any other sorting methods or criteria we might want to
   support?
