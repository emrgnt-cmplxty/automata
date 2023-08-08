EmbeddingSimilarityCalculator
=============================

``EmbeddingSimilarityCalculator`` is a class that computes similarity
scores between embedding vectors. Specifically, it calculates the dot
product similarity between a query vector and a set of vectors
corresponding to symbols.

Overview
--------

At its core, ``EmbeddingSimilarityCalculator`` provides an interface to
calculate similarity scores between a query and multiple embeddings. The
query is first converted into an embedding vector using an
``EmbeddingVectorProvider``, and then dot product similarity scores are
calculated between this query vector and a sequence of symbol
embeddings. The results can be sorted in descending order of similarity
scores.

The class also offers normalization methods to normalize the embeddings
according to specified norm types: L1, L2, and Softmax.

Related Symbols
---------------

-  ``EmbeddingVectorProvider``
-  ``Symbol``
-  ``EmbeddingNormType``
-  ``Embedding``

Usage Example
-------------

.. code:: python

   from automata.embedding.embedding_base import EmbeddingSimilarityCalculator, EmbeddingNormType
   from automata.embedding.embedding_vector_provider import EmbeddingVectorProvider
   from automata.symbol import Symbol
   from automata.embedding.embedding import Embedding

   # Assuming an instance of EmbeddingVectorProvider
   embedding_provider = EmbeddingVectorProvider(model_name='bert-base-uncased', do_lower_case=True)

   # Initialize EmbeddingSimilarityCalculator
   similarity_calculator = EmbeddingSimilarityCalculator(embedding_provider, EmbeddingNormType.L2)

   # Assume some embeddings
   ordered_embeddings = [
     Embedding(vector=np.array([1, 0, 0]), key=Symbol(name='Sym1')),
     Embedding(vector=np.array([0, 1, 0]), key=Symbol(name='Sym2')),
     Embedding(vector=np.array([0, 0, 1]), key=Symbol(name='Sym3')),
   ]

   # Query text
   query_text = 'house'

   # Calculate query similarity dictionary
   similarity_dict = similarity_calculator.calculate_query_similarity_dict(ordered_embeddings, query_text, return_sorted=True)
   print(similarity_dict)

Please note that in practice, embeddings are typically high-dimensional
and are computed from trained language models. This example is greatly
simplified for demonstration purposes.

Limitations
-----------

The key limitation of ``EmbeddingSimilarityCalculator`` is that it
relies on an ``EmbeddingVectorProvider`` to convert the query into an
embedding vector. Therefore, the effectiveness of
``EmbeddingSimilarityCalculator`` is contingent upon the quality of the
underlying language model used in ``EmbeddingVectorProvider``. Another
limitation is the presence of only three types of normalization methods.
Depending on the use case, users might need to employ other
normalization techniques.

Follow-up Questions:
--------------------

-  Is it possible to include custom embedding providers?
-  Can we extend the class to support more types of normalization
   techniques?
-  What specific similarity measures (beyond dot product) could be
   implemented to provide better results in certain contexts?
