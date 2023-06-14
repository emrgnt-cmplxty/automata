DotPathMap
==========

``DotPathMap`` is a class that provides a map from module dotpaths to
module filepaths. It offers utility methods for checking if a module
exists in the map, retrieving the dotpath or filepath of a module, and
adding a new module to the map.

Overview
--------

``DotPathMap`` is initialized with the absolute path to the root of the
module tree and internally handles the conversion between module
dotpaths and filepaths. It exposes methods for checking the existence of
a module by its dotpath or filepath, retrieving the filepath by dotpath
and vice versa, and adding a new module to the map.

Related Symbols
---------------

-  ``automata_docs.core.coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.database.vector.JSONVectorDatabase``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.symbol_types.SymbolFile``
-  ``automata_docs.core.coding.directory.DirectoryManager``
-  ``automata_docs.core.coding.py_coding.retriever.PyCodeRetriever``

Example
-------

The following example demonstrates how to create and use a
``DotPathMap`` to manage a small module tree.

.. code:: python

   import os
   from automata_docs.core.coding.py_coding.module_tree import DotPathMap

   project_root = os.path.abspath("my_project_root")
   dot_path_map = DotPathMap(project_root)

   # Check if a module exists in the map
   module_dotpath = "my_project.module1"
   assert not dot_path_map.contains_dotpath(module_dotpath)

   # Put a new module in the map
   dot_path_map.put_module(module_dotpath)

   # Check if the module was added to the map successfully
   assert dot_path_map.contains_dotpath(module_dotpath)

   module_fpath = dot_path_map.get_module_fpath_by_dotpath(module_dotpath)
   print(f"Module filepath: {module_fpath}")

Limitations
-----------

``DotPathMap`` assumes that modules have the ``.py`` extension and it
cannot handle any other types of files or directories that do not have
this extension. In addition, the class only supports module-level
dotpaths and filepaths, so nested modules or class-level mappings will
not be considered.

Follow-up Questions:
--------------------

-  How can we extend ``DotPathMap`` to support other file types or more
   granular mappings?
-  Are there any notable performance issues when dealing with very large
   module trees?
