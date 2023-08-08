DirectoryManager
================

Overview
--------

``DirectoryManager`` is a class designed to handle operations related to
directory structures. It provides a convenient interface for loading a
directory structure into memory as a structured object, getting file
names in a directory, getting subdirectories within a directory,
ensuring a directory exists by creating it if necessary, all by
manipulating and traversing the structured object.

Initialising the DirectoryManager object involves loading a directory
structure from a specified base path. The loaded directory structure is
then available for various operations such as fetching the list of files
or subdirectories.

Related Symbols
---------------

-  ``_load_directory_structure``: a private method to load directory
   structure into objects.
-  ``get_files_in_dir``: a method to get a list of files in the given
   directory.
-  ``get_subdirectories``: a method to list subdirectories in the given
   directory.
-  ``ensure_directory_exists``: a method to create a directory if it
   does not exist already.
-  ``_get_node_for_path``: a utility method to find a node corresponding
   to a given path.

Usage Example
-------------

Assuming a directory structure where ‘root_dir’ is the root directory
and ‘sub_dir1’ and ‘sub_dir2’ are subdirectories:

::

   root_dir
   |
   |------sub_dir1
   |      |
   |      |--file1.txt
   |
   |------sub_dir2
          |
          |--file2.txt

The following example shows how to use the DirectoryManager:

.. code:: python

   from automata.code_parsers.directory import DirectoryManager

   # Initialise DirectoryManager with a base directory
   mgr = DirectoryManager('root_dir')

   # Get list of files in a directory
   files_in_subdir1 = mgr.get_files_in_dir('sub_dir1') # returns ['file1.txt']

   # Get list of subdirectories in a directory
   subdirs_in_root = mgr.get_subdirectories('root_dir') # returns ['sub_dir1', 'sub_dir2']

   # Ensure a directory exists
   mgr.ensure_directory_exists('/root_dir/sub_dir3') # Creates 'sub_dir3' if it doesn't exist

Limitations
-----------

``DirectoryManager`` reads directories synchronously and may not be
ideal for large directory structures due to performance issues. Also,
changes to the file system aren’t automatically reflected by the
``DirectoryManager`` instance, unless ``_load_directory_structure`` is
called after the changes. No measures are built into to handle issues
with file permissions or broken symbolic links. Additionally, the class
is designed to operate only locally and does not support operations over
networked file systems.

Follow-up Questions:
--------------------

-  How can we extend ``DirectoryManager`` to support networked file
   systems?
-  Would it be possible to update the loaded directory structure in
   real-time without having to manually call
   ``_load_directory_structure`` after every change?
