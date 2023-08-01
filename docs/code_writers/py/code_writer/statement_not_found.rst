Examples
--------

PyCodeWriter
~~~~~~~~~~~~

To see how the ``PyCodeWriter`` module and its exceptions work, we can
observe an example similar to the one below:

.. code:: python

   from automata.code_writers.py.code_writer import PyCodeWriter

   # Create PyCodeWriter instance
   code_writer = PyCodeWriter()

   # Suppose we have a module dictionary that does not include 'automata'
   module_dict = { 'random_module': open('random_module.py').read() }

   # Try to find 'automata' in the module dictionary
   try:
       automata_module = code_writer.find_module('automata', module_dict)
   except ModuleNotFound as e:
       print("{}: {}".format(type(e).__name__, e))

   # Output: ModuleNotFound: Raised when a module not found in the module dictionary

In this example, we are trying to find a non-existing module,
‘automata’, in our module dictionary. This results in a
``ModuleNotFound`` exception being raised.

Similar to the ``ModuleNotFound`` exception, the ``StatementNotFound``
exception can be illustrated as follows:

.. code:: python

   from automata.code_writers.py.code_writer import PyCodeWriter

   # Create PyCodeWriter instance
   code_writer = PyCodeWriter()

   # Suppose we have a Python code without a Statement 'x = 1'
   python_code = """
   import os

   def sum(a, b):
       return a + b
   """

   # Try to find 'x = 1' Statement in the Python code
   try:
       statement = code_writer.find_statement('x = 1', python_code)
   except StatementNotFound as e:
       print("{}: {}".format(type(e).__name__, e))

   # Output: StatementNotFound: Raised when a provided ast.Statement is not found in the module

In this case, we are looking for the statement ``x = 1`` which does not
exist in our coded Python script. This leads to a ``StatementNotFound``
exception being thrown.
