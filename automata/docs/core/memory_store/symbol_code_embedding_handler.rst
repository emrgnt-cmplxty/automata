SymbolCodeEmbeddingHandler
==========================

``SymbolCodeEmbeddingHandler`` is a class within the Automata framework
for handling the storage and retrieval of symbol source code embeddings.
In machine learning applications, embedding is the process of taking raw
data and converting it to a vector of numbers. Within this context, the
handler is used to store and retrieve embeddings of symbols, which are
encoded representations of Python classes, methods, or local variables.

Overview
--------

``SymbolCodeEmbeddingHandler`` interacts with a database of
``JSONSymbolEmbeddingVectorDatabase``, which stores symbol code
embeddings. You can retrieve an existing embedding for a ``Symbol`` with
the ``get_embedding`` method. The handler is also equipped to process an
embedding by comparing its source code with the one in the database. If
there are updates or changes, it will accordingly update the existing
embedding.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_similarity.test_get_nearest_symbols_for_query``
-  ``automata.core.symbol_embedding.base.SymbolCodeEmbedding``
-  ``automata.tests.unit.test_symbol_embedding.test_get_embedding``
-  ``automata.tests.unit.test_synchronizer.test_build_graph_and_handler_and_synchronize``
-  ``automata.core.memory_store.symbol_doc_embedding.SymbolDocEmbeddingHandler``
-  ``automata.tests.unit.test_database_vector.test_load``
-  ``automata.core.singletons.dependency_factory.DependencyFactory.create_symbol_code_embedding_handler``
-  ``automata.tests.unit.test_database_vector.test_lookup_symbol``
-  ``automata.core.symbol_embedding.builders.SymbolCodeEmbeddingBuilder``
-  ``automata.tests.unit.test_database_vector.test_add_symbols``

Method Details
--------------

**``__init__``**: This function initializes the class with a
``JSONSymbolEmbeddingVectorDatabase`` object (embedding_db) and
``SymbolCodeEmbeddingBuilder`` object (embedding_builder).

.. code:: python

   def __init__(self, embedding_db: JSONSymbolEmbeddingVectorDatabase, embedding_builder: SymbolCodeEmbeddingBuilder) -> None:

**``get_embedding``**: Returns the embedding for a given ``Symbol`` from
the database.

.. code:: python

   def get_embedding(self, symbol: Symbol) -> SymbolCodeEmbedding:

**``process_embedding``**: If the source code has changed, then it
processes the embedding by creating a new one or updating the existing
one.

.. code:: python

   def process_embedding(self, symbol: Symbol) -> None:

**``update_existing_embedding``**: It checks for differences between the
source code of the symbol and the source code of the existing embedding.
If there are differences, it updates the embedding.

.. code:: python

   def update_existing_embedding(self, source_code: str, symbol: Symbol) -> None:

Example
-------

Consider the following code snippet, where we use
``SymbolCodeEmbeddingHandler`` for symbol1, symbol2, and symbol3.

.. code:: python

   from automata.core.symbol.base import Symbol
   from automata.core.symbol_embedding.base import JSONSymbolEmbeddingVectorDatabase, SymbolCodeEmbedding
   from automata.core.symbol_embedding.base import SymbolCodeEmbeddingHandler
   from automata.core.symbol_embedding.builders import SymbolCodeEmbeddingBuilder
   from unittest.mock import MagicMock

   # Mock symbols and their embeddings
   symbol1 = ...
   symbol2 = ...
   symbol3 = ...

   embedding1 = SymbolCodeEmbedding(symbol=symbol1, vector=np.array([1, 0, 0, 0]), source_code="symbol1")
   embedding2 = SymbolCodeEmbedding(symbol=symbol2, vector=np.array([0, 1, 0, 0]), source_code="symbol2")
   embedding3 = SymbolCodeEmbedding(symbol=symbol3, vector=np.array([0, 0, 1, 0]), source_code="symbol3")

   # JSONSymbolEmbeddingVectorDatabase methods
   embedding_db = JSONSymbolEmbeddingVectorDatabase('path_to_file')
   embedding_db.add(embedding1)
   embedding_db.add(embedding2)
   embedding_db.add(embedding3)

   # Create an instance of the class
   mock_builder = MagicMock(SymbolCodeEmbeddingBuilder)
   cem = SymbolCodeEmbeddingHandler(embedding_db=embedding_db, embedding_builder=mock_builder)

In this example, we have created symbols and their embeddings. We then
create a JSONSymbolEmbeddingVectorDatabase with a given file path and
add the embeddings to the database. Next, we create an instance of
SymbolCodeEmbeddingHandler and pass the database and a mock builder
instance to it.

Drawbacks
---------

The handling, storage, and retrieval of symbol embeddings are dependent
on the correctness and updated status of the
``JSONSymbolEmbeddingVectorDatabase`` database. If the database is not
correctly maintained or updated, the embeddings may not accurately
represent the symbols. More testing and validation steps may be needed
to ascertain embedding changes are accurately detected and handled.

Another limitation is that ``SymbolCodeEmbeddingHandler`` class cannot
load custom databases. It assumes a specific structure for the database
files and expects them to be in a certain format.

Follow-up Questions:
--------------------

-  How does the ``SymbolCodeEmbeddingHandler`` handle embeddings for
   symbols that are not found within the
   ``JSONSymbolEmbeddingVectorDatabase``?
-  How scalable is the use of this class when dealing with large code
   bases and many different symbols?
-  How are changes propagated in the database when multiple instances of
   ``SymbolCodeEmbeddingHandler`` use the same database?
