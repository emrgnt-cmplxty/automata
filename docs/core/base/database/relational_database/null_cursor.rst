class NullCursor(): ‘A null cursor to a database.’

::

   def execute(self, *args, **kwargs) -> Any:
       'Execute a query.'
       raise NotImplementedError('This is a null cursor.')

   def fetchall(self) -> Any:
       'Fetch all results from a query.'
       raise NotImplementedError('This is a null cursor.')
