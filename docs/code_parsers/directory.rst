-  Implementing a recursive retrieval of files and subdirectories could
   be done with a simple recursive function. If a directory contains
   other directories, the function would call itself on those
   subdirectories. For each subdirectory, the function will list its
   files and subdirectories and then call itself again and so forth.
-  The addition of a remove function depends on the expected use cases
   of this class. If the directory class is simply meant to read the
   structure of a pre-defined and unchanging directory, there is no need
   for a removal function. However, if the class is meant to manage and
   manipulate a directory’s structure, a removal function would be
   important.
-  The handling of symbolic links depends on the specific requirements
   of the project. It would likely be user defined – some users may need
   to treat them as files while others may need to treat them as
   directories.
-  For file/directory permissions or inaccessible files/directories, the
   class should handle these cases gracefully. This could include
   catching relevant exceptions and then either ignoring inaccessible
   files/directories, logging an error message, or potentially even
   asking the user for credentials to access these files/directories.
   The specific implementation will largely depend on the needs of the
   users.
