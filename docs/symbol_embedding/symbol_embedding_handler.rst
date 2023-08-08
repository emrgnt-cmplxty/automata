SymbolEmbeddingHandler
======================

``SymbolEmbeddingHandler`` is an abstract base class designed to
manipulate and handle embeddings for symbols. It’s equipped with the
ability to access these embeddings from a vector database, manage batch
operations on them and provides an interface for implementing further
detailed processing on the embeddings.

Overview
--------

When creating an instance of ``SymbolEmbeddingHandler``, you need to
provide an embedding database, an embedding builder and a batch size.
The batch size must be less than 2048. After initialization, the handler
class retrieves all the embeddings and stores them. It also prepares
empty lists for embeddings to be added and discarded.

There are a number of methods available for performing operations on
embeddings: 1. ``process_embedding``: This abstract method, to be
overridden in concrete child classes, performs the desired processing on
a single symbol’s embedding. 2. ``get_embeddings``: This method
retrieves the embeddings associated with a given list of symbols. 3.
``get_all_ordered_embeddings``: This method retrieves all of the symbol
embeddings from the database. 4. ``filter_symbols``: This method prunes
the supported symbols to only those present in a provided list. 5.
``_get_sorted_supported_symbols``: This is an internal method to
retrieve the currently supported symbols. 6. ``flush``: This method
updates the database with any remaining changes.

Related Symbols
---------------

-  ``VectorDatabaseProvider``
-  ``EmbeddingBuilder``
-  ``Symbol``
-  ``SymbolEmbedding``

Example
-------

Please keep in mind that ``SymbolEmbeddingHandler`` is an abstract
class. To use it, it must be subclassed with all the necessary abstract
methods being defined. Here is a simple example on how a subclass might
look:

.. code:: python

   from automata.symbol_embedding.symbol_embedding_handler import SymbolEmbeddingHandler
   from automata.symbol_embedding.database_providers import ExampleVectorDatabase
   from some_module import ExampleEmbeddingBuilder, Symbol, SymbolEmbedding

   class ExampleSymbolEmbeddingHandler(SymbolEmbeddingHandler):
       def process_embedding(self, symbol):
           embedding = self.embedding_db.get(symbol.dotpath)
           # Define processing steps..
           pass

   database_provider = ExampleVectorDatabase()
   embedding_builder = ExampleEmbeddingBuilder()
   handler = ExampleSymbolEmbeddingHandler(database_provider, embedding_builder, batch_size=1024)

   symbolA = Symbol('Some.Symbol.Path.A')
   symbolB = Symbol('Another.Symbol.Path.B')

   # Process embeddings
   handler.process_embedding(symbolA)
   handler.process_embedding(symbolB)

Limitations
-----------

1. Batch size is limited to less than 2048.
2. The exact behavior of ``process_embedding`` is not defined within
   this class and must be implemented in each subclass.

Follow-up Questions:
--------------------

-  How can we increase the batch size above 2048?
-  How to ensure thread safety when using flush method?
