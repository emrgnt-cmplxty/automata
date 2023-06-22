GraphBuilder
============

``GraphBuilder`` is a class that builds a symbol graph from an
``Index``. It provides functionality to build a graph from the given
index with optional building of caller-callee relationships. The
``GraphBuilder`` class is an integral part of the SymbolGraph creation
process and works closely with related symbols such as ``SymbolGraph``,
``Symbol``, ``SymbolFile``, and ``SymbolRank``. It abstracts the complex
process of building symbol relationships and can be extended for further
customization.

Overview
--------

``GraphBuilder`` takes an ``Index`` object and an optional boolean
``build_caller_relationships`` as input. It parses the Index and
constructs a directed graph that represents the relationships between
the different symbols found in the Index. The user can opt-in to build
caller-callee relationships for a more detailed symbol graph by passing
``True`` to the ``build_caller_relationships`` parameter.

Related Symbols
---------------

-  ``automata.core.symbol.parser.parse_symbol``
-  ``automata.core.symbol.scip_pb2.Index``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.symbol.graph.SubGraph``
-  ``automata.core.symbol.symbol_utils.convert_to_fst_object``
-  ``automata.core.symbol.graph._RelationshipManager``
-  ``automata.core.symbol.graph._CallerCalleeManager``

Usage Example
-------------

.. code:: python

   from automata.core.symbol.graph import GraphBuilder
   from automata.core.symbol.scip_pb2 import Index

   # Assume we have an `Index` object named `index`
   graph_builder = GraphBuilder(index)
   graph = graph_builder.build_graph()

Limitations
-----------

One limitation of ``GraphBuilder`` is that its performance depends on
the size and complexity of the provided ``Index`` object. Building the
graph with a larger index containing more relationships can take a
substantial amount of time. Additionally, building caller-callee
relationships can be computationally expensive and should only be used
when necessary.

Follow-up Questions:
--------------------

-  Are there any strategies to optimize the performance of
   ``GraphBuilder`` when dealing with large indexes or should this be
   considered on a case-by-case basis?
