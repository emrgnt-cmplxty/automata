class File(Node): ‘Represents a file in the tree’

::

   def __init__(self, name: str, parent: Optional['Node']=None) -> None:
       super().__init__(name, parent)
