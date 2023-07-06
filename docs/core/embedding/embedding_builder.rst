EmbeddingBuilder
================

``EmbeddingBuilder`` is an abstract class that defines interfaces for
building embeddings for symbols. It is typically extended by other
classes that provide specific implementations for building the
embeddings.

Overview
--------

``EmbeddingBuilder`` is an important part of the automata.core.embedding
module. It provides the foundation for building symbol embeddings in an
abstract way, allowing for different methods of building embeddings to
be developed and used interchangeably. The class contains abstract
methods that are intended to be implemented by child classes.

Related Symbols
---------------

-  ``automata.tests.unit.test_context_oracle_tool.context_oracle_tool_builder``
-  ``automata.core.symbol_embedding.builders.SymbolCodeEmbeddingBuilder``
-  ``automata.core.symbol_embedding.builders.SymbolDocEmbeddingBuilder``
-  ``automata.core.memory_store.symbol_doc_embedding.SymbolDocEmbeddingHandler.__init__``
-  ``automata.core.memory_store.symbol_code_embedding.SymbolCodeEmbeddingHandler.__init``

Example
-------

Here’s an example of how a class might implement ``EmbeddingBuilder``
providing the actual implementation for the ``build`` method.

.. code:: python

   class ConcreteEmbeddingBuilder(EmbeddingBuilder):
       def build(self, source_text: str, symbol: Symbol) -> Any:
           # concrete implementaion of building the embedding.
           pass

Please note that this is a mock example. Replace
‘ConcreteEmbeddingBuilder’ with the actual class that you want to use as
an ``EmbeddingBuilder``.

Limitations
-----------

As an abstract base class, ``EmbeddingBuilder`` does not provide any
functionality itself, it merely outlines the methods that need to be
implemented by any concrete subclasses. It involves designing these
subclasses to actually build the embeddings, and the design of these
subclasses can significantly affect the performance and accuracy of
symbol recognition.

Dependencies
------------

-  ``automata.core.embedding.base.EmbeddingVectorProvider``
-  ``automata.core.symbol.base.Symbol``
-  ``automata.core.symbol.symbol_utils.convert_to_fst_object``

Follow-up Questions:
--------------------

-  When creating subclasses of ``EmbeddingBuilder``, what are the common
   pitfalls that one should be mindful of?
-  What are the typical strategies to build a good embedding and how do
   we evaluate the effectiveness of the strategies?
