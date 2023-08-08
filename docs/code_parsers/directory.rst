Directory
=========

Overview
--------

The ``Directory`` class represents a directory in a file tree system
within the context of an automata software. A directory is a container
for various types of nodes that can be other directories or files, which
can be nested to form a hierarchical structure. The ``Directory`` class
inherits from the ``Node`` class and includes additional methods for
managing child nodes, checking the type of the directory, and getting
all file names or subdirectory names.

Features
--------

-  Support for adding child nodes to a directory via ``add_child()``
   method.
-  Ability to check if the directory is root directory
   (``is_root_dir()``) or a leaf directory (``is_leaf_dir()``).
-  Provides methods to fetch names of all files (``get_file_names()``)
   or subdirectories (``get_subdirectories()``) in the directory.

Related Symbols
---------------

-  ``automata.code_parsers.directory.DirectoryManager``
-  ``automata.code_parsers.directory.File``
-  ``automata.code_parsers.directory.Node``

Example
-------

Here is an example of how you can create and manage ``Directory``
object.

.. code:: python

   from automata.code_parsers.directory import Directory, File

   base_dir = Directory('base')
   child_dir = Directory('child', base_dir)
   base_dir.add_child(child_dir)

   test_file = File('test.txt', child_dir)
   child_dir.add_child(test_file)

   print(base_dir.get_subdirectories()) # ['child'] 
   print(child_dir.get_file_names()) # ['test.txt']
   print(base_dir.is_root_dir()) # True
   print(child_dir.is_leaf_dir()) # True

This example creates a base directory as a root and then creates a child
directory within it. It adds a test file to the child directory, and
then verifies the child directory and test file exist under ‘base’ and
‘child’ respectively. It also checks if base is root directory and if
the child directory is a leaf directory.

Limitations
-----------

The ``Directory`` class does not have direct methods for file operation
such as file write or read, file deletion and has no provisions for
error handling in case of invalid operations like duplicating child node
names.

Follow-up Questions:
--------------------

-  What happens if we try to add two children with the same name to a
   directory?
-  How does the ``Directory`` class handle symbolic links?
-  Does the ``Directory`` class support operations on hidden files and
   directories?
