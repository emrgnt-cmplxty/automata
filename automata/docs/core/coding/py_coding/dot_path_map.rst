DotPathMap
==========

``DotPathMap`` is a utility class that provides a map from module
dotpaths to module filepaths. A module dotpath is a string
representation of a module’s location in a namespace hierarchy using
dots as separators, while a module filepath is an operating
system-specific file path to a module. This class can be used to quickly
find the file path for a given dotpath, or the dotpath for a given file
path, facilitating the management and referencing of Python modules in a
project. The class also provides methods to check if a module exists in
the map, and to put a new module in the map.

Overview
--------

``DotPathMap`` provides an abstraction for managing module references in
a project. It offers methods to:

-  Check if a dotpath or filepath is in the map.
-  Get the module filepath given a dotpath, or vice versa.
-  Retrieve the mapping between module dotpaths and module filepaths.
-  Put a module in the map given a dotpath.

The class can be instantiated with an absolute path to the root of the
module tree, and, if not provided, it will default to the project’s root
directory.

Related Symbols
---------------

-  ``automata.core.coding.py_coding.module_tree.DotPathMap``
-  ``automata.core.utils.root_fpath``
-  ``automata.core.coding.py_coding.py_utils.convert_fpath_to_module_dotpath``

Example
-------

The following is an example demonstrating how to create an instance of
``DotPathMap`` and interact with it.

.. code:: python

   from automata.core.coding.py_coding.module_tree import DotPathMap

   # Initialize the DotPathMap with the absolute path to the root of the module tree
   root_path = "/path/to/project/root"
   path_map = DotPathMap(root_path)

   # Check if a module dotpath is in the map
   is_in_map = path_map.contains_dotpath("sample_module")

   # Get the module filepath for a given module dotpath
   module_fpath = path_map.get_module_fpath_by_dotpath("sample_module")

   # Put a module in the map given its dotpath
   path_map.put_module("new_sample_module")

Limitations
-----------

The primary limitation of ``DotPathMap`` is that it assumes a specific
structure for the module tree and relies on the use of dotpaths and
filepaths to manage module references. It may not be suited for projects
with unconventional module organization or referencing.

Follow-up Questions:
--------------------

-  How can ``DotPathMap`` be extended to support different module
   organization structures or referencing methods?
-  Can the limited support for custom module trees be improved or
   extended for better configurability?
