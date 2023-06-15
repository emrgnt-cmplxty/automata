DotPathMap
==========

``DotPathMap`` is a class that provides a mapping between module
dotpaths and their filepaths. A dotpath is a string showing the
hierarchical structure of a program, separated by periods. The class has
methods to add, check if a module exists, and fetch the dotpath or
filepath for a specific module.

Overview
--------

``DotPathMap`` is initialized with the root filesystem path of the
module tree, where it builds and maintains maps between module dotpaths
and their filepaths. It provides methods for checking if the map
contains a module by its dotpath or filepath, and methods to retrieve
the dotpath or filepath for a module given one or the other.

Related Symbols
---------------

-  ``automata_docs.core.coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.database.vector.JSONVectorDatabase``

Example
-------

The following example demonstrates how to create an instance of
``DotPathMap`` and perform various operations on it:

.. code:: python

   from automata_docs.core.coding.py_coding.module_tree import DotPathMap

   # Create a DotPathMap instance with a specific path
   path = "/path/to/python/module/root"
   map_instance = DotPathMap(path)

   # Check if the DotPathMap contains a module
   module_dotpath = "automata_docs.core.agent.automata_agent"
   is_module_exists = map_instance.contains_dotpath(module_dotpath)

   # Add a module to the DotPathMap
   new_module_dotpath = "automata_docs.core.test.new_module"
   map_instance.put_module(new_module_dotpath)

   # Get the filepath of a module given its dotpath
   module_filepath = map_instance.get_module_fpath_by_dotpath(new_module_dotpath)

   # Get the dotpath of a module given its filepath
   fetched_module_dotpath = map_instance.get_module_dotpath_by_fpath(module_filepath)

Limitations
-----------

``DotPathMap`` assumes a specific directory structure for the module
tree and relies on a one-to-one mapping between module dotpaths and
filepaths. If the directory structure is changed or if there are
multiple filepaths associated with a dotpath, the mapping might be
inconsistent.

Follow-up Questions:
--------------------

-  What happens if there are multiple filepaths associated with a single
   dotpath?
