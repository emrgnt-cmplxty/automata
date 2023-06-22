Node
====

``Node`` is an abstract base class for a node in the file tree. It
represents the basic structure of a node along with the ``name`` and
``parent`` attributes. The subclasses of ``Node`` are ``Directory`` and
``File``. Both subclasses inherit its basic methods and properties while
adding specific functionalities.

Related Symbols
---------------

-  ``automata.core.coding.directory.Directory``
-  ``automata.core.coding.directory.File``

Example
-------

The following example demonstrates how to create an instance of
``Directory`` and ``File``:

.. code:: python

   from automata.core.coding.directory import Directory, File

   # Creating a Directory node
   root_directory = Directory("root_dir")

   # Creating a File node inside the root_directory
   file_in_root = File("file1.txt", root_directory)

Limitations
-----------

-  ``Node`` being an abstract base class, it cannot be instantiated
   directly. You have to create an instance of its subclasses
   ``Directory`` or ``File``.
-  There are no built-in operations for performing actions like moving,
   copying, or deleting a node, you would need to use the built-in
   Python ``os`` module for those operations.

Follow-up Questions:
--------------------

-  How to perform more advanced operations like move, copy, and delete
   for a ``Node``?
