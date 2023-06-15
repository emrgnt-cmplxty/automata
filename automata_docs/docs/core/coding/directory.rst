Directory
=========

The ``Directory`` class represents a directory in a file system. It can
have children, which can be either directories or files. The class
offers several methods to interact with directories, such as adding
child nodes, getting file or subdirectory names, or checking if the
directory is a leaf or root directory.

Overview
--------

``Directory`` is part of a tree-like structure that represents a file
system. It stores the parent node as well as the children of the current
directory. You can add child nodes, get file names, get subdirectories,
and check if the directory is a leaf or root directory.

Related Symbols
---------------

-  automata_docs.core.coding.directory.File
-  automata_docs.core.coding.directory.Node
-  automata_docs.tests.unit.test_directory_manager.test_load_directory_structure
-  automata_docs.tests.unit.test_directory_manager.test_get_files_in_dir
-  automata_docs.tests.unit.test_directory_manager.test_get_subdirectories
-  automata_docs.tests.unit.test_directory_manager.test_get_node_for_path
-  automata_docs.core.database.vector.JSONVectorDatabase

Example
-------

The following example demonstrates how to create a ``Directory`` object,
add child nodes, and interact with the contained files and
subdirectories.

.. code:: python

   from automata_docs.core.coding.directory import Directory, File

   root = Directory("root")
   dir1 = Directory("dir1", root)
   file1 = File("file1.txt", dir1)

   root.add_child(dir1)
   dir1.add_child(file1)

   file_names = dir1.get_file_names()
   subdirectories = root.get_subdirectories()

   print(f"Files in dir1: {file_names}")  # Output: Files in dir1: ['file1.txt']
   print(f"Subdirectories in root: {subdirectories}")  # Output: Subdirectories in root: ['dir1']

Limitations
-----------

The primary limitation of the ``Directory`` class is that it only
provides a basic tree-like structure representing file systems. It does
not directly interact with the actual file system on the host machine.
For real interactions with the host machine’s file system, consider
using Python’s built-in ``os`` and ``os.path`` modules.

Follow-up Questions:
--------------------

-  How can we extend the ``Directory`` class to include more
   functionality, such as file content manipulations or actual file
   system interactions?

-  How should the ``Directory`` class handle symbolic links or hard
   links when working with real file systems?
