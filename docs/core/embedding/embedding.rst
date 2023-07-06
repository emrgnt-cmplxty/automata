Embedding
=========

Overview
--------

``Embedding`` is an abstract base class that lays the groundwork for
different embedding objects in the Automata codebase. This class manages
the embedding vector and provides methods to convert the instance to a
string, and vice versa.

The ``Embedding`` class is typically used as a base class that specific
types of embeddings inherit from. An embedding takes an input object and
transforms it into a vector form that can be easily manipulated by
machine learning models. The class holds a key, an input object, and its
corresponding vector representation.

Related Symbols
---------------

Primary Symbol
~~~~~~~~~~~~~~

-  automata.core.embedding.base.Embedding

Others
~~~~~~

-  automata.core.base.database.vector.VectorDatabaseProvider
-  automata.core.symbol.base.Symbol
-  automata.core.symbol.symbol_utils.convert_to_fst_object
-  automata.core.symbol_embedding.base.SymbolCodeEmbedding
-  automata.core.symbol_embedding.base.SymbolDocEmbedding
-  automata.core.memory_store.symbol_doc_embedding.SymbolDocEmbeddingHandler
-  automata.tests.unit.test_symbol_embedding.test_update_embeddings
-  automata.tests.unit.test_database_vector.test_load

Example
-------

As an abstract base class, ``Embedding`` is not directly instantiated in
most cases. Instead, it is extended by other classes, which implement
the specific type of embedding. Here is an example of a hypothetical
class ``ExampleEmbedding`` that extends ``Embedding``:

.. code:: python

   class ExampleEmbedding(Embedding):
       def __init__(self, key: Any, input_object: str, vector: np.ndarray):
           super().__init__(key, input_object, vector)

       def __str__(self):
           description = f'Example Embedding for the object {self.input_object} with key {self.key}'
           return description

Limitations
-----------

As an abstract base class, ``Embedding`` doesn’t provide any
implementations. The ``__str__`` method is expected to be overridden in
child classes since it’s decorated with ``@abc.abstractmethod``. It’s
also assumed the embedding vector will be of the type numpy.ndarray,
though this isn’t enforced in the Embedding class itself.

Follow-up Questions
-------------------

-  What are the requirements for the key and input_object during the
   initialization of the Embedding object?
-  What practical implementations are used in the Automata codebase, and
   what are specific use-cases?
-  What error handling is used if the vector object passed during
   initialization is not a numpy.ndarray?
-  Are there size or dimension requirements for the array, or can it be
   of any shape?
