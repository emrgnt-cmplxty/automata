DirectoryManager
================

``DirectoryManager`` is a class that handles operations related to
directory structure. It provides methods to ensure a directory exists,
obtain a list of files in a directory, and retrieve a list of the
subdirectories in a directory.

Overview
--------

The ``DirectoryManager`` class allows you to interact with the directory
structure of your file system. It offers methods for creating a new
directory if it does not already exist, getting a list of file names in
a directory, and obtaining a list of subdirectories in a directory. The
class works with related classes like ``Directory``, ``File``, and
``Node``.

Related Symbols
---------------

-  ``automata.core.coding.directory.Directory``
-  ``automata.core.coding.directory.File``
-  ``automata.core.coding.directory.Node``
-  ``automata.tests.unit.test_directory_manager``

Example
-------

The following example demonstrates how to use ``DirectoryManager`` to
interact with the directory structure:

.. code:: python

   from automata.core.coding.directory import DirectoryManager

   # Create a DirectoryManager with a specified base path
   base_path = "/path/to/your/base/directory"
   dir_manager = DirectoryManager(base_path)

   # Ensure a directory exists
   directory_path = "/path/to/your/directory"
   dir_manager.ensure_directory_exists(directory_path)

   # Get a list of files in a directory
   path = "/path/to/directory"
   files = dir_manager.get_files_in_dir(path)
   print(files)  # Output: List of file names

   # Get a list of subdirectories in a directory
   subdirectories = dir_manager.get_subdirectories(path)
   print(subdirectories)  # Output: List of subdirectories

Limitations
-----------

The ``DirectoryManager`` class assumes a specific structure for its
directories and works best with directories that adhere to this
structure. It also relies on the ``os`` package for interacting with the
file system, limiting it to the functionalities provided by that
package.

Follow-up Questions:
--------------------

-  How can we modify DirectoryManager to work with custom directory
   structures?
