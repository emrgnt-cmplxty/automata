Node
====

``Node`` is an abstract base class for nodes within a file tree.
Instances of this class represent nodes in a tree-like structure that
makes up the file hierarchy. Each node in the file tree is created with
a name and an optional parent. Derived classes ``Directory`` and
``File`` provide the concrete implementations, representing directories
and files respectively within the tree.

Related Symbols
---------------

-  ``automata.core.coding.directory.File``
-  ``automata.core.coding.directory.Directory``

Example
-------

The following example demonstrates how to create instances of the
``Node`` derived class, ``Directory``, and ``File``, and create a simple
file tree hierarchy.

.. code:: python

   from automata.core.coding.directory import Directory, File

   # Create the root directory
   root = Directory("root")

   # Create a child directory and add it to the root
   child_dir = Directory("child_dir", parent=root)
   root.add_child(child_dir)

   # Create a file and add it to the child directory
   file = File("file.txt", parent=child_dir)
   child_dir.add_child(file)

Import Statements
-----------------

.. code:: python

   import logging
   import os
   from typing import Dict, List, Optional

Class Docstring
---------------

.. code:: python

   Abstract base class for a node in the file tree

Class Methods
-------------

-  ``__init__(self, name: str, parent: Optional["Node"] = None) -> None:``
   - Initializes a new instance of the ``Node`` class with the given
   name and optional parent.

   .. code:: python

      Args:
          name (str): Name of the node
          parent (Node): Parent node of this node

Follow-up Questions:
--------------------

-  Can the parent of a node be changed after it has been created?
-  Does the ``Node`` class provide any methods for traversing or
   manipulating the file tree? If not, which classes should be used?
