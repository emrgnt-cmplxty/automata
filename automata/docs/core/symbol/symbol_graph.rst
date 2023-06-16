SymbolGraph
===========

The ``SymbolGraph`` class represents the symbol graph that captures the
relationships between symbols found in various source code files. The
symbol graph can be built from an index protobuf file, making it the
central class for working with symbols and their relationships. Some of
the primary methods in ``SymbolGraph`` include
``get_all_available_symbols``, ``get_all_files``,
``get_potential_symbol_callees``, ``get_potential_symbol_callers``,
``get_references_to_symbol``, ``get_symbol_dependencies``, and
``get_symbol_relationships``.

Overview
--------

``SymbolGraph`` uses NetworkX’s MultiDiGraph to represent the
relationships between symbols as a directed graph. It includes methods
to query for callers, callees, and references to a symbol, as well as
obtaining all available symbols and files in the graph. The graph can be
filtered to subgraphs containing only rankable symbols. Getting
reachable objects in the symbol subgraph requires using the navigator
interface, \_SymbolGraphNavigator.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.graph.GraphBuilder``
-  ``automata_docs.core.symbol.graph._SymbolGraphNavigator``
-  ``automata_docs.core.symbol.search.SymbolSearch``

Example
-------

The following example demonstrates how to create an instance of
``SymbolGraph`` using an index protobuf file.

.. code:: python

   from automata_docs.core.symbol.graph import SymbolGraph

   # Assuming the path to a valid index protobuf file, you should replace it with your own file path
   index_path = "path/to/index.scip"
   symbol_graph = SymbolGraph(index_path)
   all_symbols = symbol_graph.get_all_available_symbols()

Limitations
-----------

SymbolGraph can only be built from an index protobuf file. In addition,
the method ``get_potential_symbol_callers`` returns potential callers,
but this list requires downstream filtering to remove non-call
statements.

Follow-up Questions:
--------------------

-  How to better handle edge cases in the symbol graph building process?
-  How to make ``get_potential_symbol_callers`` more efficient with
   fewer potential callers?

Footnotes
---------

In the context provided, some information was referring to ‘mock’
objects which are used for testing purposes. In the final documentation,
it is recommended to replace mocked objects with actual underlying
objects whenever possible. A list of some of the imported modules and
methods is provided for reference, which may be useful in illustrating
certain aspects of the SymbolGraph class.
