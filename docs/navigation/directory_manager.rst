DirectoryManager
================

The ``DirectoryManager`` is a utility class providing functionalities
related to operations with a directory structure. This class offers
methods to create directories, retrieve files inside a directory, and
obtain list of subdirectories inside a particular directory.

Overview
--------

``DirectoryManager``, part of ``automata.ast_helpers.ast_utils.directory``,
conducts operations related to directory structure. It initiates with a
base path and contains a ``root`` attribute representing the root
directory of the structure, as an instance of ``Directory``.

DirectoryManager provides several methods including:

-  ``ensure_directory_exists(directory_path: str) -> None:`` Creates a
   new directory only if it does not exist already.
-  ``get_files_in_dir(path: str) -> List[str]:`` Returns a list of files
   in the specified directory.
-  ``get_subdirectories(path: str) -> List[str]:`` Yields a list of
   subdirectories in the given directory.

Related Symbols
---------------

-  ``automata.ast_helpers.ast_utils.directory.Directory``: Represents a directory
   that contains child nodes which can be either files or directories.
-  ``automata.singletons.github_client.GitHubClient``: Provides an
   interface for interacting with GitHub repositories.
-  ``automata.tasks.environment.AutomataTaskEnvironment``: The
   environment in which the Automata tasks are conducted.
-  ``automata.tests.unit.test_directory_manager``: Contains unit tests
   for the DirectoryManager methods.

Example
-------

Here is an example of how the ``DirectoryManager`` class can be
instantiated and used.

.. code:: python

   # Import the necessary modules
   from automata.ast_helpers.ast_utils.directory import DirectoryManager

   # Define the base directory
   base_dir = "/home/user/documents"

   # Instantiate the DirectoryManager object
   dir_manager = DirectoryManager(base_dir)

   # Ensure a new directory exists in the base directory
   dir_manager.ensure_directory_exists(base_dir + "/new_directory")

   # Get the files in the new directory
   files = dir_manager.get_files_in_dir(base_dir + "/new_directory")
   print(files)  # Returns an empty list if no files exist

   # Get the subdirectories in the base directory
   subdirs = dir_manager.get_subdirectories(base_dir)
   print(subdirs)  # Returns a list of subdirectories in the base directory

Limitations
-----------

One of the limitations of the ``DirectoryManager`` class is that it only
works with directories that the current user context has permissions to
manage. Therefore, attempting to manipulate directories that the user
does not have sufficient permissions to work with will result in errors.

Additionally, the ``DirectoryManager`` class operates only on the
existing file system and cannot manage or interact with remote/mounted
directories.

Follow-up Questions:
--------------------

-  Is there a feature or method for interacting with remote directories
   in DirectoryManager?
-  What happens when attempting to create a directory that already
   exists in the file system?
-  How does DirectoryManager handle concurrent directory changes?
