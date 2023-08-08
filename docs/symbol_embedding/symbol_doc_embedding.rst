SymbolDocEmbedding
==================

``SymbolDocEmbedding`` is a concrete class designed for symbol document
embeddings. This class builds upon the ``SymbolEmbedding`` base class to
provide functionality specifically geared towards handling document
embeddings. Paramount in its usage is being able to link associated
source code, summary, and context to the embedded object.

Overview
--------

``SymbolDocEmbedding`` takes four main parameters during initialization
- ``key``, ``document``, ``vector``, ``source_code``, ``summary``,
``context``, with ``source_code``, ``summary``, and ``context`` being
optional parameters. The ``key`` is the Symbol for document embedding,
and the ``document`` is a string representation of the text data to be
embedded. ``vector`` is the NumPy ndarray object shared between source
text data and embedding space. ``source_code``, ``summary``, and
``context`` provide additional context to the symbol document.

The ``SymbolDocEmbedding`` class primarily provides a str method to
print a string representation that includes the key symbol, the source
document, length of the vector, source code if available, summary and
context. It also gives a metadata property that returns a dictionary of
the symbol object’s source code, summary, and context.

Related Symbols
---------------

-  ``automata.symbol_embedding.symbol_embedding_base.SymbolEmbedding``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolDocEmbedding``.

.. code:: python

   from automata.symbol_embedding.symbol_embedding_base import SymbolDocEmbedding
   import numpy as np

   key = 'example_symbol'
   document = 'This is an example document for embedding.'
   vector = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
   source_code = 'print("Hello World!")'
   summary = 'An example source code printing Hello World.'
   context = 'Used for illustrating how to use SymbolDocEmbedding.'

   embedding = SymbolDocEmbedding(key, document, vector, source_code, summary, context)
   print(str(embedding))

Limitations
-----------

``SymbolDocEmbedding`` requires that the input ``document`` and input
``vector`` have compatible dimensions. If these values are not aligned,
the embedding process may fail. ``source_code``, ``summary``, and
``context`` aim to enhance the utility of the embedding by introducing
more context, their absence does not impact the creation of an embedding
but reduces the amount of information in the embedding.

Follow-up Questions:
--------------------

-  How does the class handle embeddings when the size of the input
   document and vector are not compatible?
-  What are the default behaviors of the class when optional parameters
   are not provided?
