SymbolGraph
===========

``SymbolGraph`` is a class that represents a directed graph of symbols
and their relationships. It provides methods to extract information
about the symbols, such as their dependencies, callers, and callees. The
class also includes methods to retrieve symbol-related subgraphs and the
associated metadata about symbols.

Overview
--------

``SymbolGraph`` is primarily used to represent and analyze the
relationships between symbols in a codebase. The class is initialized
with an index protobuf file path and offers several methods to retrieve
various types of information about the symbols. It uses an internal
graph structure, with the ``networkx`` library, to map the relationships
between symbols and their references.

Related Symbols
---------------

-  ``automata.core.symbol.parser.parse_symbol``
-  ``automata.core.symbol.scip_pb2.Index``
-  ``automata.core.symbol.base.Symbol``
-  ``automata.core.symbol.graph.GraphBuilder``
-  ``automata.core.symbol.graph._SymbolGraphNavigator``
-  ``automata.core.singletons.dependency_factory.create_symbol_graph``
-  ``automata.core.experimental.search.symbol_search.SymbolSearch``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolGraph`` using an index protobuf file path.

.. code:: python

   from automata.core.symbol.graph import SymbolGraph

   index_path = "path/to/index/protobuf/file"
   symbol_graph = SymbolGraph(index_path)

Limitations
-----------

One limitation of ``SymbolGraph`` is that it depends on the existence
and format of an index protobuf file. The index file must be correctly
formatted and include valid relationships between symbols for
``SymbolGraph`` to work correctly. Additionally, the library makes some
assumptions about the structure of the index file, which may not
necessarily apply to custom data.

Follow-up Questions
-------------------

-  How can we use SymbolGraph with custom or non-standard index protobuf
   files to build relationships between symbols in different code bases?
-  What is the expected format and structure of the index protobuf file
   that SymbolGraph requires for initialization?
