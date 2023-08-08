class PathEnum(Enum): ‘A base class for enums that represent paths.’

::

   def to_path(self) -> str:
       return convert_kebab_to_snake_case(self.value)
