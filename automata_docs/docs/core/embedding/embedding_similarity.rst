EmbeddingSimilarity
===================

``EmbeddingSimilarity`` is an abstract base class for search ranking
algorithms. It provides a foundation for implementing methods to search
for symbols or text queries that are similar to a given query. The
similar symbols are returned as a dictionary with their respective
similarity scores.

Overview
--------

``EmbeddingSimilarity`` is designed to be used in conjunction with
classes like ``SymbolSimilarity`` and relies on embeddings derived from
various symbol structures like ``Symbol`` and ``SymbolEmbedding``. The
class provides the following abstract methods:

-  ``__init__(symbol_embedding_manager, norm_type)``: Initializes an
   instance of ``EmbeddingSimilarity``.
-  ``get_nearest_entries_for_query(query_text, k_nearest)``: Retrieves
   the k nearest symbols to the provided ``query_text``.
-  ``get_query_similarity_dict(query_text)``: Computes the similarity
   between the provided ``query_text`` and all available symbols.

Related Symbols
---------------

-  ``automata_docs.core.embedding.symbol_similarity.SymbolSimilarity``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingsProvider``
-  ``automata_docs.core.database.vector.JSONVectorDatabase``
-  ``automata_docs.core.symbol.symbol_types.SymbolDocEmbedding``

Example
-------

The following example demonstrates how one might use a derivative of
``EmbeddingSimilarity`` such as ``SymbolSimilarity``:

.. code:: python

   from automata_docs.core.database.vector import JSONVectorDatabase
   from automata_docs.core.embedding.embedding_types import EmbeddingsProvider
   from automata_docs.core.embedding.symbol_similarity import SymbolSimilarity
   from automata_docs.core.embedding.symbol_embedding import SymbolCodeEmbeddingHandler

   # Initialize a JSONVectorDatabase object
   embedding_db = JSONVectorDatabase("path/to/json_file")

   # Create an EmbeddingsProvider object
   provider = EmbeddingsProvider()

   # Initialize a SymbolCodeEmbeddingHandler object
   handler = SymbolCodeEmbeddingHandler(embedding_db, provider)

   # Create a SymbolSimilarity instance using the handler
   symbol_similarity = SymbolSimilarity(handler)

   # Query the 2 nearest symbols to the given text
   query = "Example query text"
   result = symbol_similarity.get_nearest_entries_for_query(query, k_nearest=2)

   # The result is a dictionary with symbols as keys and similarity scores as values
   print(result)

Limitations
-----------

The primary limitation of ``EmbeddingSimilarity`` is that it assumes
specific data structures and related classes, like
``EmbeddingsProvider`` and ``SymbolSimilarity``. As it is an abstract
base class, it cannot be used directly but must be subclassed to provide
the desired functionality.

Follow-up Questions:
--------------------

-  How can ``EmbeddingSimilarity`` be used for other types of embeddings
   besides code and documentation?
-  How can ``EmbeddingSimilarity`` be extended to support additional
   similarity algorithms?
