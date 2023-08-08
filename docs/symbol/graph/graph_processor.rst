class GraphProcessor(ABC): ‘Abstract base class for processing edges in
the ``MultiDiGraph``.’

::

   @abstractmethod
   def process(self) -> None:
       'Adds new edges of the specified type to the graph.'
       pass
