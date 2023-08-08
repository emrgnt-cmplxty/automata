class Embedding(abc.ABC): ‘Abstract base class for different types of
embeddings’

::

   def __init__(self, key: Any, document: str, vector: np.ndarray):
       self.key = key
       self.document = document
       self.vector = vector

   @abc.abstractmethod
   def __str__(self) -> str:
       pass
