EmbeddingHandler
================

``EmbeddingHandler`` is an abstract base class designed to handle
embeddings in the Automata library. It acts as an interface that
dictates the basic functions an embedding handler must implement.

Overview
--------

The ``EmbeddingHandler`` symbol provides a standardised interface for
embedding handling. It is designed to be used as a base class for other
specific implementations like ``SymbolEmbeddingHandler`` and
``SymbolDocEmbeddingHandler``.

It handles the interaction with both the ``embedding_db``
(VectorDatabaseProvider instance) and ``embedding_builder``
(EmbeddingBuilder instance), requiring these as parameters during the
class initialisation.

Related Symbols
---------------

-  ``automata.core.base.database.vector.VectorDatabaseProvider``
-  ``automata.embedding.base.EmbeddingBuilder``
-  ``automata.symbol.base.Symbol``
-  ``automata.symbol_embedding.base.SymbolEmbeddingHandler``
-  ``automata.memory_store.symbol_doc_embedding.SymbolDocEmbeddingHandler``
-  ``automata.memory_store.symbol_code_embedding.SymbolCodeEmbeddingHandler``

Methods
-------

``__init__``
~~~~~~~~~~~~

This is the constructor method for the ``EmbeddingHandler`` and it is
responsible for initialising the instance with the provided
``embedding_db`` and ``embedding_builder``. As an abstract method, it
simply sets these two properties without any further processing.

.. code:: python

   def __init__(self, embedding_db: VectorDatabaseProvider, embedding_builder: EmbeddingBuilder) -> None:
       self.embedding_db = embedding_db
       self.embedding_builder = embedding_builder

``get_embedding``
~~~~~~~~~~~~~~~~~

This abstract method is designed to return the embedding for a specific
symbol. The specific implementation will be dependent on the child
class.

.. code:: python

   @abc.abstractmethod
   def get_embedding(self, symbol: Symbol) -> Any:
       pass

``process_embedding``
~~~~~~~~~~~~~~~~~~~~~

This abstract method is designed to process the embedding for a specific
symbol. The specific implementation will be dependent on the child
class.

.. code:: python

   @abc.abstractmethod
   def process_embedding(self, symbol: Symbol) -> None:
       pass

Limitations
-----------

As ``EmbeddingHandler`` is an abstract class, it can’t be instantiated
directly. Instead, it must be subclassed, and at least ``get_embedding``
and ``process_embedding`` methods must be implemented in the child
class.

Follow-up Questions:
--------------------

-  How is the ``get_embedding`` method expected to behave? Does it
   always access live data, cache results, or some combination of the
   two?
-  How is the ``process_embedding`` method expected to behave? What sort
   of preprocessing might it do?
-  Are there expected side-effects to either the ``get_embedding`` or
   ``process_embedding`` methods?
-  What is the expected type of the returned embeddings?
-  How are symbols identified for embedding processing?
