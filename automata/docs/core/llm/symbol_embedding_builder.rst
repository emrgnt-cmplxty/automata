SymbolEmbeddingBuilder
======================

``SymbolEmbeddingBuilder`` is an abstract class that serves as a
blueprint for specific embedding builder classes that construct
embeddings for various types of symbols. The constructor accepts an
instance of ``EmbeddingProvider`` as a parameter, which provides
embeddings for the symbols. It includes a ``build`` method, which must
be implemented in the child classes, designed for building the
embeddings based on a source text and a symbol.

Overview
--------

``SymbolEmbeddingBuilder`` offers a systematic way of generating
embeddings for symbols by providing an organizational structure to
support the process. Its primary functionality revolves around creating
embeddings for symbols using the underlying ``EmbeddingProvider`` and
source text. Furthermore, it includes a ``fetch_embedding_context``
method that retrieves the context for a source code embedding, which
abstracts the conversion of a symbol to a string object.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_embedding.test_get_embedding``
-  ``automata.core.memory_store.symbol_code_embedding.SymbolCodeEmbeddingBuilder``
-  ``automata.tests.unit.test_symbol_embedding.test_get_embedding_exception``
-  ``automata.tests.unit.test_symbol_embedding.test_add_new_embedding``
-  ``automata.core.memory_store.symbol_doc_embedding.SymbolDocEmbeddingBuilder``
-  ``automata.tests.unit.test_symbol_embedding.test_update_embedding``
-  ``automata.tests.unit.test_symbol_embedding.test_update_embeddings``
-  ``automata.core.base.symbol_embedding.SymbolCodeEmbedding``
-  ``automata.tests.unit.test_symbol_search_tool.symbol_search_tool_builder``
-  ``automata.core.memory_store.symbol_code_embedding.SymbolCodeEmbeddingBuilder.build``

Example
-------

Below is an example demonstrating how to create an instance of a
concrete class (``SymbolCodeEmbeddingBuilder``) that extends
``SymbolEmbeddingBuilder``.

.. code:: python

   from automata.core.memory_store.symbol_code_embedding import SymbolCodeEmbeddingBuilder
   from automata.core.llm.core import EmbeddingProvider

   # Create an instance of EmbeddingProvider
   embedding_provider = EmbeddingProvider() 
   # Substitute with appropriate parameter value

   # Create an instance of SymbolCodeEmbeddingBuilder
   emb_builder = SymbolCodeEmbeddingBuilder(embedding_provider)

Limitations
-----------

The primary constraint of ``SymbolEmbeddingBuilder`` is that it does not
provide any concrete implementation; instead, it provides an interface
that needs to be implemented by inheriting classes. Moreover, it solely
focuses on symbol embeddings and may not offer extensive support for
more complex scenarios that involve embeddings of higher-dimensional
structures.

Follow-up Questions:
--------------------

-  What is the structure of the embeddings provided by the
   ``EmbeddingProvider``?
-  How are the outputs of the ``build`` method structured and used by
   other classes in the framework?
-  How are the concrete classes such as ``SymbolCodeEmbeddingBuilder``
   and ``SymbolDocEmbeddingBuilder`` implementing the abstract methods
   of ``SymbolEmbeddingBuilder``?
