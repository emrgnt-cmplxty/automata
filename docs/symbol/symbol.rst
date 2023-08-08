Symbol
======

``Symbol`` is a class that represents and encapsulates the logic for
symbols in Python. A Symbol can specify a Python class, a method, or
even a local variable. Each symbol is further represented in a
standardized way through a unique URI (Uniform Resource Identifier)
string.

The ``Symbol`` class includes various attributes to represent a symbol:
uri, scheme, package, and descriptors. With these attributes, ``Symbol``
captures the critical information about Python symbols and provides an
efficient way to work with or manipulate symbols in Python programs.
Further, it includes various properties and class methods for efficient
interaction and usage.

Overview
--------

The ``Symbol`` class is designed to provide an easy and efficient way to
work with symbols in Python. It offers properties for extracting
information about symbols, such as the parent of a symbol, the kind of
Python element the symbol represents (py_kind), and whether the symbol
represents a local variable, meta information, parameter, etc.

The ``Symbol`` URI structure conforms to a specific syntax, providing
structure and standardization for symbol representation. Utility
functions, like ``from_string``, are available to create ``Symbol``
instances from a string representation of a Symbol.

Related Symbols
---------------

Currently, there are no related symbols.

Usage Example
-------------

.. code:: python

   from automata.symbol.symbol_base import Symbol
   from automata.symbol.symbol_parser import parse_symbol

   symbol_class = parse_symbol(
       "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.agent.agent_enums`/ActionIndicator#"
   )
   # Returns an instance of Symbol

   symbol_method = parse_symbol(
       "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.tools.base`/ToolNotFoundError#__init__()."
   )
   # Returns an instance of Symbol

Symbol objects can be compared for equality, depending on their URI.

.. code:: python

   symbol_class == symbol_method
   # Returns False

In addition, Symbol instances can be hashed, primarily based on their
URI.

.. code:: python

   hash(symbol_class)
   # Returns -729559640 (This is just an example. The actual output may vary)

Limitations
-----------

The ``Symbol`` class relies heavily on the input structure to be in the
correct format as described in the URI syntax. Thus, it can raise
exceptions or behave unexpectedly if given incorrectly-formatted input.

Follow-up Questions:
--------------------

-  Is there a dynamic way to create or manage Symbols which are not
   conforming to the described URI format?
-  Can there be improvements done to handle more complex URIs or Symbols
   parsing?
