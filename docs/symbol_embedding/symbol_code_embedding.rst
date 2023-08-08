class SymbolCodeEmbedding(SymbolEmbedding): ‘A concrete class for symbol
code embeddings’

::

   def __init__(self, key: Symbol, document: str, vector: np.ndarray):
       super().__init__(key, document, vector)

   def __str__(self) -> str:
       return f'''SymbolCodeEmbedding(

symbol={self.symbol},

embedding_source={self.document}

vector_length={len(self.vector)} )’’’

::

   @property
   def metadata(self) -> Dict[(str, str)]:
       return {}
