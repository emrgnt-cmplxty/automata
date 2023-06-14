SymbolFile
----------

``SymbolFile`` represents a file that contains an automata symbol. It
provides methods for comparing a ``SymbolFile`` with other instances of
``SymbolFile`` or its path as a string, as well as for retrieving the
hash value of its path, which is useful in certain operations like
working with dictionaries or sets.

Closely Related Symbols
~~~~~~~~~~~~~~~~~~~~~~~

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.symbol_types.SymbolReference``

Example
~~~~~~~

Consider the following example in which we create a ``SymbolFile`` from
a given file path and then compare it with another ``SymbolFile`` and a
string representation of the file path:

.. code:: python

   from automata_docs.core.symbol.symbol_types import SymbolFile

   file1 = SymbolFile("path/to/file.py")
   file2 = SymbolFile("path/to/file.py")

   assert file1 == file2
   assert file1 == "path/to/file.py"

Overview of Methods
~~~~~~~~~~~~~~~~~~~

``__eq__(self, other)``
^^^^^^^^^^^^^^^^^^^^^^^

This method compares the current instance of ``SymbolFile`` with another
``SymbolFile`` or a string representing its path. Returns ``True`` if
they are the same, ``False`` otherwise.

``__hash__(self) -> int``
^^^^^^^^^^^^^^^^^^^^^^^^^

Returns the hash value of the path of the ``SymbolFile`` instance.

Limitations
~~~~~~~~~~~

``SymbolFile`` can only represent an individual file with a single path
and does not support working with directories or multiple files at once.
It also has no functionality for file manipulation or inspection other
than equality comparison and hashing.
