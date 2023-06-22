Directory
=========

``Directory`` is a class that represents a directory in a tree
structure. It is part of the core coding logic for directory management
in Automata. It can have children which can be directories or files. It
provides methods for adding child nodes, getting file names, getting
subdirectory names, checking if it is a leaf or root directory.

Overview
--------

``Directory`` inherits from the ``Node`` class and extends its
functionality by maintaining a dictionary of children nodes. This class
is utilized in managing the file and directory structure of a project
and is often used in conjunction with other directory management classes
like ``DirectoryManager``.

Related Symbols
---------------

-  ``automata.core.coding.directory.File``
-  ``automata.core.coding.directory.Node``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``automata.tests.unit.test_directory_manager.test_load_directory_structure``
-  ``automata.tests.unit.test_directory_manager.test_get_files_in_dir``
-  ``automata.tests.unit.test_directory_manager.test_get_subdirectories``
-  ``automata.tests.unit.test_directory_manager.test_get_node_for_path``

Examples
--------

The following is an example demonstrating how to create a ``Directory``
and add children nodes (files or directories).

.. code:: python

   from automata.core.coding.directory import Directory, File

   root_dir = Directory("root")
   child_file = File("file.txt")
   child_dir = Directory("subdirectory")

   root_dir.add_child(child_file)
   root_dir.add_child(child_dir)

   print(root_dir.get_file_names())  # Output: ["file.txt"]
   print(root_dir.get_subdirectories())  # Output: ["subdirectory"]
   print(root_dir.is_leaf_dir())  # Output: False
   print(root_dir.is_root_dir())  # Output: True

Discussion
----------

The ``Directory`` class is a useful utility for managing file systems
and project structures in Automata. It abstracts the concepts of files
and directories and provides easy-to-use methods for managing directory
trees. The primary limitation of this class is that it does not provide
functionality related to file I/O (input and output). This class focuses
on the logical structure of directories and their relationships to each
other.

Follow-up Questions:
--------------------

-  How can we extend the ``Directory`` class to include functionality
   related to file I/O?
