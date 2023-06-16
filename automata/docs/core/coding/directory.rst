Directory
=========

``Directory`` represents a directory, which can contain other
directories or files as children. It provides methods for working with
directory structures like adding child nodes, getting file names and
subdirectories, checking if a directory is a leaf or root directory, and
more.

Overview
--------

The ``Directory`` class is designed for working with directory
structures. It extends the abstract base class ``Node``. Its main
purpose is to model directories, but it also provides relevant
functionality for working with those directories. Building context and
understanding the Directory class allows you to work more easily with
file systems and directory settings in your project.

Import Statements
-----------------

.. code:: python

   import logging
   import os
   from typing import Dict, List, Optional

Related Symbols
---------------

-  ``automata.tests.unit.test_directory_manager.test_load_directory_structure``
-  ``automata.tests.unit.test_directory_manager.test_get_files_in_dir``
-  ``automata.tests.unit.test_directory_manager.test_get_subdirectories``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.database.vector.JSONVectorDatabase``
-  ``automata.tests.unit.test_directory_manager.test_get_node_for_path``
-  ``automata.core.coding.directory.File``
-  ``automata.tests.unit.sample_modules.sample.OuterClass``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``

Examples
--------

.. code:: python

   from automata.core.coding.directory import Directory

   # Create a sample root directory
   root_dir = Directory(name="root")

   # Create a sample child directory
   child_dir = Directory(name="child", parent=root_dir)

   # Add the child directory to the root directory
   root_dir.add_child(child_dir)

   # Get the subdirectories of the root directory
   subdirectories = root_dir.get_subdirectories()
   print(subdirectories)  # Output: ['child']

Limitations
-----------

The primary limitation of the ``Directory`` class is that it doesn’t
provide advanced functionality for working with the contents of
directories or files, such as searching for a specific file or
directory, moving or renaming files/directories, etc. Additionally, it
models only a simple file tree structure without support for links or
other more complex features found in actual file systems.

Follow-up Questions:
--------------------

-  How can we implement more advanced features for working with files
   and directories, like searching or moving/renaming files and
   directories within a ``Directory`` object’s structure?
