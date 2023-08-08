class Node(): ‘Abstract base class for a node in the file tree’

::

   def __init__(self, name: str, parent: Optional['Node']=None) -> None:
       self.name = name
       self.parent = parent
