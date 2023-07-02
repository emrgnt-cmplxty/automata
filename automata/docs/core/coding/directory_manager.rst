DirectoryManager
================

``DirectoryManager`` is a class that handles operations related to
directory structures. It provides methods for ensuring that a directory
exists, listing files and subdirectories within a given path, and
loading the directory structure from a base path.

Overview
--------

``DirectoryManager`` is a simple utility for managing directory
structures, providing methods to create directories, retrieve files and
subdirectories within a directory, and other operations related to
directory structures. It uses ``Directory`` objects to represent
directories and their contents and provides methods to traverse and
manipulate these objects. The ``DirectoryManager`` is closely related to
the ``Directory``, ``File``, and ``Node`` classes.

Related Symbols
---------------

-  ``automata.core.navigation.directory.Directory``
-  ``automata.core.navigation.directory.File``
-  ``automata.core.navigation.directory.Node``
-  ``automata.tests.unit.test_directory_manager``

Example
-------

The following is an example demonstrating how to create an instance of
``DirectoryManager`` and use its methods to manage a directory
structure.

.. code:: python

   from automata.core.navigation.directory import DirectoryManager
   import tempfile

   # Create a temporary directory
   base_path = tempfile.mkdtemp()

   # Initialize a DirectoryManager with the base path
   dir_manager = DirectoryManager(base_path)

   # Ensure a directory exists within the base path
   dir_manager.ensure_directory_exists("test_dir")

   # Get the files and subdirectories within the base path
   files = dir_manager.get_files_in_dir(base_path)
   subdirectories = dir_manager.get_subdirectories(base_path)

   # Print the results
   print("Files:", files)
   print("Subdirectories:", subdirectories)

Limitations
-----------

``DirectoryManager`` assumes a specific directory structure and relies
on the underlying file system. It does not provide methods for copy,
move or remove operations on directories and does not support custom
directory structures and file metadata.

Follow-up Questions:
--------------------

-  How can we extend ``DirectoryManager`` to support more file
   operations and directory structures?
-  Would it be beneficial to include custom metadata for files and
   directories in the ``DirectoryManager``?
