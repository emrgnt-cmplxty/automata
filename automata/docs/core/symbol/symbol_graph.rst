SymbolGraph
===========

``SymbolGraph`` is a class used to represent and manipulate a directed
multi-graph of symbols from an index protobuf file. It provides methods
for retrieving available symbols, analyzing dependencies and
relationships between symbols, and extracting information about files
and references to symbols. The main components of the ``SymbolGraph``
include the ``GraphBuilder``, ``SubGraph``, and the
``_SymbolGraphNavigator``.

Overview
--------

``SymbolGraph`` is designed to assist in the following tasks:

-  Retrieve all available symbols and files in the graph
-  Analyze potential callers and callees of a given symbol
-  Extract symbol dependencies and relationships
-  Navigate and manipulate the graph in a flexible way

The ``SymbolGraph`` class is primarily used with related symbols such as
``Symbol``, ``SymbolDescriptor``, ``SymbolFile``, and
``SymbolReference``.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``: Represents a class,
   method, or local variable in the graph.
-  ``automata.core.symbol.symbol_types.SymbolDescriptor``: Describes the
   metadata and attributes of a symbol.
-  ``automata.core.symbol.symbol_types.SymbolFile``: Represents a file
   that contains symbols.
-  ``automata.core.symbol.symbol_types.SymbolReference``: Represents a
   reference to a symbol in a file.

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolGraph`` and retrieve the available symbols and files in the
graph:

.. code:: python

   from automata.core.symbol.graph import SymbolGraph

   # Assuming the path to a valid index protobuf file
   index_path = "path/to/index.protobuf"
   symbol_graph = SymbolGraph(index_path)

   # Get all available symbols and files in the graph
   symbols = symbol_graph.get_all_available_symbols()
   files = symbol_graph.get_all_files()

   print(f"Number of symbols: {len(symbols)}")
   print(f"Number of files: {len(files)}")

Limitations
-----------

The primary limitations of the ``SymbolGraph`` include:

-  The ``SymbolGraph`` relies heavily on the quality and structure of
   the index protobuf file. If the input file is malformed or structured
   differently, the graph will not work as intended.
-  The ``SymbolGraph`` assumes a specific directory structure and naming
   convention for the protobuf file, which may limit its usability with
   customized format.

Follow-up Questions:
--------------------

-  Are there any alternative ways to represent and manipulate symbol
   graphs?
-  How robust and efficient is the current implementation of the
   ``SymbolGraph`` in handling large and complex graphs?
