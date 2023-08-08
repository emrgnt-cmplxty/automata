class NullConnection(): ‘A null connection to a database.’

::

   def commit(self) -> Any:
       'Commit a transaction.'
       raise NotImplementedError('This is a null connection.')
