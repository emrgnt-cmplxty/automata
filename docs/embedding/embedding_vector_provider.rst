class EmbeddingVectorProvider(abc.ABC): ‘A class to provide embeddings
for symbols’

::

   @abc.abstractmethod
   def build_embedding_vector(self, document: str) -> np.ndarray:
       'An abstract method to build the embedding vector for a document.'
       pass

   @abc.abstractmethod
   def batch_build_embedding_vector(self, documents: List[str]) -> List[np.ndarray]:
       'An abstract method to build the embedding vector for a list of documents.'
       pass
