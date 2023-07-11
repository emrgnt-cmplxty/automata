automata.ast_helpers.ast_utils.directory.Directory
=======================================

The ``Directory`` class is a part of the ``automata`` library, primarily
used for manipulating and navigating directory like structures.
``Directory`` class represents a directory and provides functionalities
such as adding a child node (or file) to itself, getting file names from
the directory, obtaining a list of subdirectories, checking if we are at
the root or leaf directory, etc.

Overview
--------

``Directory`` is an important class for managing structures and
hierarchy of directories and files. The class provides several methods
to efficiently manage the nodes (or files) and directories within the
project’s framework.

Import Statements
-----------------

To begin using the ``Directory`` class, the following import statements
are needed:

.. code:: python

   import logging
   import os
   from typing import Dict, List, Optional
   from automata.ast_helpers.ast_utils.directory import Directory

Key Methods
-----------

``Directory`` features several key methods for managing directory
structures:

-  ``__init__(self, name: str, parent: Optional["Node"] = None) -> None:``

   This method initializes a new instance of the Directory class.

-  ``add_child(self, child: "Node") -> None:``

   Method to add a child node to this directory

-  ``get_file_names(self) -> List[str]:``

   Fetches a list of file names in the current directory.

-  ``get_subdirectories(self) -> List[str]:``

   Fetches a list of the subdirectories present within the current
   directory.

-  ``is_leaf_dir(self) -> bool:``

   Checks if the current directory is a leaf directory, i.e., if it has
   no subdirectories.

-  ``is_root_dir(self) -> bool:``

   Checks if the current directory is the root directory.

Usage Example
-------------

.. code:: python

   from automata.ast_helpers.ast_utils.directory import Directory

   # instantiate
   root_dir = Directory("root")

   # add child directories and files
   root_dir.add_child(Directory("dir1", root_dir))
   root_dir.add_child(File("file1", root_dir))

   # check if root directory
   print(root_dir.is_root_dir())  # True

   # get file names
   print(root_dir.get_file_names())  # ['file1']

   # get subdirectories
   print(root_dir.get_subdirectories())  # ['dir1']

   # check if leaf directory
   print(root_dir.is_leaf_dir())  # False

Please note that for this example to run you have to import ``File``
from the ``automata.ast_helpers.ast_utils.directory`` module.

Related Symbols
---------------

Here are some test functions related to the ``Directory`` class:

-  ``automata.tests.unit.test_directory_manager.test_load_directory_structure``
   — Checks if a test directory gets properly loaded.
-  ``automata.tests.unit.test_directory_manager.test_get_files_in_dir``
   — Tests the action of getting files from a directory.
-  ``automata.tests.unit.test_directory_manager.test_get_subdirectories``
   — Checks if a list of subdirectories from a directory can be
   retrieved.
-  ``automata.tests.unit.test_directory_manager.test_get_node_for_path``
   — Validates that a node from the path can be retrieved.

Limitations
-----------

One limitation is that the ``Directory`` class is currently designed to
work with directories and files represented as a tree of node objects,
which means that it can’t handle file systems with symbolic links that
create cycles in the directory structure. Also, it currently doesn’t
handle any system-specific file and directory attributes.

Follow-up Questions
-------------------

-  How can this class be extended to handle symbolic links and cycles in
   the directory structure?
-  How could we handle system-specific file and directory attributes?
-  Is it possible to add a functionality to move files around, or would
   this be beyond the scope of the Node class?
