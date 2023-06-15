DirectoryManager
================

``DirectoryManager`` is a class that handles operations related to
directory structure. It provides functionalities to work with
directories, such as loading directory structure, creating directories,
listing files and subdirectories within the given path. The class has
methods such as ``ensure_directory_exists``, ``get_files_in_dir``, and
``get_subdirectories``.

Overview
--------

``DirectoryManager`` is initialized with a ``base_path`` representing
the base directory structure. It provides functionalities to ensure that
a directory exists by creating it if necessary, get a list of files and
subdirectories in the given directory path. The class utilizes related
symbols like ``Directory``, ``Node``, and other helper
functions/methods.

Related Symbols
---------------

-  ``automata_docs.core.coding.directory.Directory``
-  ``automata_docs.core.coding.directory.Node``
-  ``automata_docs.tests.unit.test_directory_manager.create_test_dir_structure``

Example
-------

The following is an example demonstrating how to create an instance of
``DirectoryManager`` and use its methods to interact with the directory
structure.

.. code:: python

   from automata_docs.core.coding.directory import DirectoryManager

   base_path = "/path/to/base/directory"
   dir_manager = DirectoryManager(base_path)

   # Ensure a directory exists
   dir_manager.ensure_directory_exists("/path/to/target/directory")

   # Get files in a directory
   files = dir_manager.get_files_in_dir("/path/to/directory")
   print(files)  # ["file1.txt", "file2.txt"]

   # Get subdirectories in a directory
   subdirectories = dir_manager.get_subdirectories("/path/to/directory")
   print(subdirectories)  # ["subdir1", "subdir2"]

Limitations
-----------

``DirectoryManager`` assumes a fixed directory structure and relies on
the provided base path for working with the directory. It does not
provide extensive error handling or advanced functionalities.

Follow-up Questions:
--------------------

-  Are there any specific error handling or validations that should be
   added to the methods in ``DirectoryManager``?
