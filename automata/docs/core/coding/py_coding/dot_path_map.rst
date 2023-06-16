DotPathMap
==========

``DotPathMap`` is a class that maps module dotpaths to module filepaths.
It provides an easy way to access module dotpaths programmatically,
which is useful when working with Python codebases. The class offers
various utility methods like ``contains_dotpath``, ``contains_fpath``,
``get_module_dotpath_by_fpath``, ``get_module_fpath_by_dotpath``, and
``put_module``.

Overview
--------

``DotPathMap`` is initialized with an absolute path to the root of the
module tree. The class provides methods to check if the map contains a
particular module dotpath or filepath, get the corresponding dotpath for
a given module filepath and vice versa, and put a module with a given
dotpath into the map.

Related Symbols
---------------

-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.database.vector.JSONVectorDatabase``
-  ``automata.core.symbol.graph.SymbolGraph``

Example
-------

Here’s an example of utilizing ``DotPathMap``:

.. code:: python

   from automata.core.coding.py_coding.module_tree import DotPathMap

   # Set the path to the root of the Python project
   path_to_project_root = "/path/to/python/project"

   # Initialize the DotPathMap
   dotpath_map = DotPathMap(path_to_project_root)

   # Check if the dotpath_map contains a given dotpath and filepath
   contains_dotpath = dotpath_map.contains_dotpath("module.dotpath.example")
   contains_fpath = dotpath_map.contains_fpath("/path/to/python/module/example.py")

   # Get the dotpath of a module given its filepath
   dotpath = dotpath_map.get_module_dotpath_by_fpath("/path/to/python/module/example.py")

   # Get the filepath of a module given its dotpath
   fpath = dotpath_map.get_module_fpath_by_dotpath("module.dotpath.example")

   # Put a module with the given dotpath in the map
   dotpath_map.put_module("module.dotpath.example")

Limitations
-----------

The primary limitation of ``DotPathMap`` is that it only supports Python
projects with a specific directory structure and does not handle cases
where the project has a different structure, such as virtual
environments or nested packages.

Follow-up Questions:
--------------------

-  How can ``DotPathMap`` be extended to support more complex project
   structures?
-  Can ``DotPathMap`` be easily integrated with other build systems,
   like ``setuptools`` or ``pip``, to handle package installations?
