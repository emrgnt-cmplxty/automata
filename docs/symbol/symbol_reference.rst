SymbolReference
===============

``SymbolReference`` is a data class that represents a reference to a
particular symbol within a text file. Each instance of
``SymbolReference`` includes information pertaining to the symbol, the
line number and column number where the symbol is located, as well as
miscellaneous roles associated with the symbol.

Overview
--------

The ``SymbolReference`` class provides a succinct way to manage and
trace usages of individual symbols across a set of text files. It stores
a ``Symbol`` object, which encapsulates the information related to the
symbol, and the precise location details (line and column numbers). The
roles dictionary (``Dict[str, Any]``) highlights additional attributes
or roles that the symbol may have.

The class defines the ``__hash__`` and ``__eq__`` dunder methods, to
allow for comparison of two ``SymbolReference`` instances and calculate
a unique hash value for each instance. This is useful when inserting
these instances into data structures that rely on hashing, like a Python
set or a dictionary.

Related Symbols
---------------

There are no related symbols provided in the context.

Example
-------

.. code:: python

   from automata.symbol.symbol_base import Symbol, SymbolReference

   # Creating a symbol instance
   symbol = Symbol(uri="file://path/to/file.py", name="MyClass", kind="class")

   # Creating a symbol reference instance
   symbol_reference = SymbolReference(
       symbol=symbol, 
       line_number=30, 
       column_number=25, 
       roles={"is_method": False}
   )

   # Comparing two symbol references
   if symbol_reference == symbol_reference:
       print("Both symbol references point to the same location.")

Limitations
-----------

It should be noted that the ``SymbolReference`` class does not perform
any validity checks on the line or column numbers. Also, it does not
check if the given symbol actually exists in the provided location. If
the file or the symbol do not exist, or the line or column numbers are
invalid, the ``SymbolReference`` will still be created, but it may not
be accurate or useful.

Follow-up Questions:
--------------------

-  What kind of validation could be included to strengthen the
   ``SymbolReference`` class?
-  What implications could exist for using ``SymbolReference`` instances
   in hash-based data structures?
-  How can the dict-type attribute ``roles`` be utilized in different
   applications?
