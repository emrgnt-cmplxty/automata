class IEmbeddingLookupProvider(abc.ABC): ‘A concrete base class an
interface for embedding lookup providers.’

::

   def embedding_to_key(self, entry: SymbolEmbedding) -> str:
       'Concrete implementation to generate a simple hashable key from a Symbol.'
       return entry.symbol.dotpath
