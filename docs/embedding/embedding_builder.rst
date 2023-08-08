EmbeddingBuilder
================

The ``EmbeddingBuilder`` class is an abstract base class used to create
embeddings. It contains abstract methods (to be implemented by
subclasses) that build the embeddings from source text and a provided
symbol. Two types of embeddings can be created - a single instance-based
embedding and batch-based embeddings.

Overview
--------

The ``EmbeddingBuilder`` takes an ``EmbeddingVectorProvider`` as an
input during its instantiation. This provider supplies the algorithms to
generate vector representations (embeddings) from source code text.

The main functionalities of the ``EmbeddingBuilder`` are defined by two
main methods - ``build()`` and ``batch_build()``. These are abstract
methods, implying that their precise implementation should be provided
in subclasses of ``EmbeddingBuilder``.

The ``build()`` method builds an embedding for a single symbol from
source text. The ``batch_build()`` generates embeddings for a batch of
symbols simultaneously.

In addition, there’s a helper method ``fetch_embedding_source_code()``,
which transforms a given symbol into its respective source code. The
transformed code is used as a context during the embedding generation.

Related Symbols
---------------

-  ``automata.experimental.symbol_embedding.symbol_doc_embedding_builder.SymbolDocEmbeddingBuilder.build``
-  ``automata.symbol_embedding.symbol_embedding_builders.SymbolCodeEmbeddingBuilder.build``
-  ``automata.experimental.tools.builders.advanced_context_oracle_builder.AdvancedContextOracleToolkitBuilder.build``
-  ``automata.experimental.symbol_embedding.symbol_doc_embedding_builder.SymbolDocEmbeddingBuilder.build_non_class``
-  ``automata.experimental.memory_store.symbol_doc_embedding_handler.SymbolDocEmbeddingHandler._create_new_embedding``
-  ``automata.singletons.dependency_factory.DependencyFactory.create_embedding_similarity_calculator``
-  ``automata.memory_store.symbol_code_embedding_handler.SymbolCodeEmbeddingHandler._build_and_add_embeddings``
-  ``automata.experimental.tools.builders.document_oracle_builder.DocumentOracleToolkitBuilder.build``
-  ``automata.embedding.embedding_base.EmbeddingNormType``
-  ``automata.symbol_embedding.symbol_embedding_base.SymbolEmbedding.from_args``

Usage Example
-------------

.. code:: python

   # Concrete implementation of EmbeddingBuilder class
   class MyEmbeddingBuilder(EmbeddingBuilder):
       def build(self, source_text, symbol):
           # Implementation of embedding generation for a single symbol
           pass
       def batch_build(self, source_text, symbol):
           # Implementation of embedding generation for a batch of symbols
           pass

   # Now MyEmbeddingBuilder can be used in our models
   my_embedding_builder = MyEmbeddingBuilder(embedding_provider)

Limitations
-----------

Being an abstract base class, ``EmbeddingBuilder`` doesn’t provide any
concrete implementation of its methods, and merely provides an interface
to be followed by its subclasses. Therefore, it’s not usable on its own,
and requires a subclass to define the ``build`` and ``batch_build``
methods.

Follow-up Questions:
--------------------

-  What embedding techniques/algorithms (e.g., Word2Vec, GloVe,
   FastText, etc.) are available with the ``EmbeddingVectorProvider``?
-  How is the quality of the generated embedding ensured, and is it
   possible to customize the embedding generation process according to
   the needs of the specific task? Besides, how can one handle source
   texts that may have varying language styles, especially in the
   context of different programming languages?
