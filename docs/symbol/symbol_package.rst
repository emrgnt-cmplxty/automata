@dataclass class SymbolPackage(): ‘A class to represent the package
component of a Symbol URI.’ manager: str name: str version: str

::

   def __repr__(self) -> str:
       return f'Package({self.unparse()})'

   def unparse(self) -> str:
       'Converts back into URI string'
       return f'{self.manager} {self.name} {self.version}'
