EmbeddingSimilarityCalculator
=============================

``EmbeddingSimilarityCalculator`` is a class in the
``automata.embedding.base`` module. It takes an instance of
``EmbeddingVectorProvider`` and calculates the similarity score between
a query text and symbol embeddings.

Overview
--------

``EmbeddingSimilarityCalculator`` leverages embeddings representation to
quantify the similarity between code symbols and a given query text. It
uses the dot product of the query embedding and the symbol embeddings.
If required, the resulting similarity scores can be sorted in descending
order by default.

Every instance of ``EmbeddingSimilarityCalculator`` is initialized with
an ``EmbeddingVectorProvider`` and a type of norm for vector
normalization (``EmbeddingNormType``). Initially, it sets these
parameters with the corresponding values.

The main method in this class is ``calculate_query_similarity_dict``.
This method retrieves the embedding for a provided query text,
calculates the similarity scores with the existing symbol embeddings,
constructs a dictionary with these scores indexed by the symbols and
optionally sorts the dictionary.

Related Symbols
---------------

-  ``automata.embedding.base.EmbeddingVectorProvider``
-  ``automata.embedding.base.EmbeddingNormType``
-  ``automata.embedding.base.Embedding``
-  ``automata.core.base.database.vector.VectorDatabaseProvider``
-  ``automata.symbol.base.Symbol``

Example:
--------

In this example, ``EmbeddingSimilarityCalculator`` is utilized to find
the symbol most similar to a given query text:

.. code:: python

   from automata.embedding.base import EmbeddingSimilarityCalculator, EmbeddingVectorProvider
   from automata.symbol.base import Symbol
   from numpy import array

   # Create an instance of the class
   mock_provider = EmbeddingVectorProvider()
   embedding_sim_calc = EmbeddingSimilarityCalculator(mock_provider)

   # Define query_text, and embeddings 
   query_text = "symbol1"
   ordered_embeddings = [Embedding(Symbol('symbol1'), 'symbol1', array([1,0,0,0])),
                         Embedding(Symbol('symbol2'), 'symbol2', array([0,1,0,0])), 
                         Embedding(Symbol('symbol3'), 'symbol3', array([0,0,1,0]))]

   # Use the calculate_query_similarity_dict method
   result = embedding_sim_calc.calculate_query_similarity_dict(ordered_embeddings, query_text)

   print(result)

**Note:** In real scenario ``EmbeddingVectorProvider`` would be an
instance of class that provides actual embeddings like
``OpenAIEmbedding``.

Limitations
-----------

The accuracy of ``EmbeddingSimilarityCalculator`` heavily depends on the
quality of the embeddings produced by ``EmbeddingVectorProvider``. Poor
embeddings can result in inaccurate similarity scores. Additionally, it
does not inherently handle cases where symbols might have the same
embedding values.

Follow-up Questions:
--------------------

-  If two symbols end up having the same embedding, how does the
   ``EmbeddingSimilarityCalculator`` differentiate between them?
-  How are the results affected if a different norm type
   (``EmbeddingNormType``) is used?
