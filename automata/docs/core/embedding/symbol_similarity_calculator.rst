SymbolSimilarityCalculator
==========================

This class is responsible for calculating the similarity between
symbols. It can be utilized in situations where given a query, the
similarity between the query and different symbols is required.

Overview
--------

The ``SymbolSimilarityCalculator`` uses symbol embeddings to compute
similarities between symbols. The class provides several methods to set
and get symbols, as well as compute similarity scores. For each symbol
or query text, it computes an embedding. The similarity between symbols
is then calculated as the dot product between their respective
embeddings. The class accepts and returns symbols represented in the
``Symbol`` data type.

Related Symbols
---------------

-  ``automata.tests.unit.test_context_oracle_tool.test_context_generator``
-  ``automata.tests.unit.test_symbol_similarity.test_get_nearest_symbols_for_query``
-  ``automata.core.agent.tool.tool_utils.DependencyFactory.create_symbol_code_similarity``
-  ``automata.tests.unit.test_symbol_search_tool.test_symbol_rank_search``
-  ``automata.tests.unit.test_symbol_search_tool.test_exact_search``
-  ``automata.core.agent.tool.tool_utils.DependencyFactory.create_symbol_doc_similarity``
-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.tests.conftest.symbol_search``
-  ``automata.core.llm.embedding.EmbeddingSimilarityCalculator``

Usage Example
-------------

.. code:: python

   from automata.core.llm.embedding import (
       EmbeddingNormType,
       EmbeddingProvider,
       SymbolEmbeddingHandler,
   )
   from typing import Dict, List, Optional, Set
   from ann_embed.synthetic_provider import SyntheticProvider
   from automata.core.symbol.symbol_types import Symbol
   from numpy import random
   from automata.core.embedding.symbol_similarity import SymbolSimilarityCalculator


   # Mock symbols and their embeddings
   symbols = [Symbol(f'symbol{i}') for i in range(3)]
   embedding_vectors = random.rand(3, 3)


   class MockSymbolEmbeddingHandler(SymbolEmbeddingHandler):
       def get_all_supported_symbols(self) -> List[Symbol]:
           return symbols

       def get_embedding(self, symbol: Symbol) -> Any:
           return embedding_vectors[symbols.index(symbol)]


   mock_provider = SyntheticProvider(embedding_size=3)
   mock_handler = MockSymbolEmbeddingHandler(mock_provider)

   symbol_similarity = SymbolSimilarityCalculator(mock_handler)

   # Test with query_text that is most similar to symbol1
   mock_provider.build_embedding.return_value = embedding_vectors[0]
   result = symbol_similarity.calculate_query_similarity_dict(symbols[0].dotpath())
   max_similarity_symbol = list(result.keys())[np.argmax(list(result.values()))]

Limitations
-----------

The ``SymbolSimilarityCalculator`` class calculates similarity based on
embeddings only. As such, it is limited by the quality and richness of
the symbol embeddings. In particular, embeddings that do not capture the
semantical nature of symbols will not produce meaningful similarities.
Furthermore, the similarity calculation is conducted in a complete
symbols space, unless ``available_symbols`` is set to constrain it.
High-dimensional embeddings or a large number of symbols might thus
impose scalability issues.

Follow-up Questions:
--------------------

-  How does the ``SymbolSimilarityCalculator`` handle symbols with no
   embeddings?
-  How does the class handle homonymous symbols whose meanings might be
   significantly different depending on the context?
-  How does the performance of ``SymbolSimilarityCalculator`` scale with
   the number of symbols and the dimensionality of embeddings?
