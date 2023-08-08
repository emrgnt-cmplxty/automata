PyModuleLoader
==============

``PyModuleLoader`` is a class designed to load and cache in memory
Python modules, specified by their dot-paths, as they are accessed. It
operates using a Singleton pattern, meaning there can only be one
instance of this class in any given Python environment. This means any
changes made to ``PyModuleLoader`` within a Python session persists
throughout the entirety of the session.

The PyModuleLoader also maintains a mapping of dot-paths to their
corresponding ‘Abstract Syntax Tree’ (AST) objects. The AST represents
Python code in a tree format, where each node corresponds to a Python
construct. This enables the object to fetch Python code in an easily
manipulatable and readable format.

Related Symbols
---------------

-  ``automata.singletons.singleton.Singleton``
-  ``typing.Optional``
-  ``typing.Dict``
-  ``typing.Tuple``
-  ``typing.Iterable``
-  ``ast.Module``

Example
-------

Here is an example on how to use the ``PyModuleLoader``. Note that this
class needs to be initialized before usage, and path information should
exist in the specific format that this class expects.

.. code:: python

   from automata.singletons.py_module_loader import PyModuleLoader as PML
   import os

   root_path = os.getcwd()  # The root directory path
   project_name = 'project'  # The project name

   # Initialize the PyModuleLoader with root path and project name
   PML.initialize(root_path, project_name)

   # Check if a dotpath exist in the loader
   print('automata' in PML)  # Replace 'automata' with actual dotpath

   # Fetch an existing module dotpath
   print(PML.fetch_ast_module('automata')) 
   # Replace 'automata' with actual dotpath, if the module does not exist, this will return None

   # Reset the PyModuleLoader
   PML.reset()

Limitations
-----------

A specific limitation for ``PyModuleLoader`` is that the path
information initialization is required before using any method in the
class. Also, the Python module loader is designed to operate within a
specific directory structure, so if modules are structured differently,
adjustments will be needed.

Follow-up Questions:
--------------------

-  How to handle the cases of different directory structure for Python
   Modules?
-  What is the best solution to avoid repeating the
   ``_assert_initialized`` call in every single method?
-  What is the strategy to remove type: ignore comments? Is there any
   sufficient automated method to achieve this?
