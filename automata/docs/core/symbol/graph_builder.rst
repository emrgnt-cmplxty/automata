GraphBuilder
============

``GraphBuilder`` is a class that enables the construction of a symbol
graph from an ``Index`` object. The graph representation aids in
exploring symbol relationships within source code.

Overview
--------

Given an ``Index`` object as input, ``GraphBuilder`` processes the
relationships and occurrences of each symbol in the index. The resulting
graph is a networkx ``MultiDiGraph`` object, allowing for the
identification of symbol patterns and relationships within the codebase.

By default, ``GraphBuilder`` does not include caller-callee
relationships, for performance reasons. However, this feature can be
enabled upon instantiation with the ``build_caller_relationships`` flag
set to ``True``.

Related Symbols
---------------

-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.symbol.symbol_types.SymbolFile``
-  ``automata.core.symbol.parser.parse_symbol``

Example
-------

The following example demonstrates how to create a ``GraphBuilder``
instance and build a graph from an ``Index`` object.

.. code:: python

   from automata.core.symbol.graph import GraphBuilder
   from automata.core.symbol.scip_pb2 import Index

   index = Index()  # Assuming a populated index object.
   build_caller_relationships = True  # Optional
   graph_builder = GraphBuilder(index, build_caller_relationships)
   graph = graph_builder.build_graph()

Limitations
-----------

``GraphBuilder`` may exhibit performance-related limitations, especially
when the ``build_caller_relationships`` flag is set to ``True``. This
can lead to significantly longer processing times, as it involves an
expensive operation to compute the caller-callee relationships.

Follow-up Questions:
--------------------

-  Are there any ways to optimize the caller-callee relationship
   computation within the ``GraphBuilder``?
