SymbolGraph
===========

Overview
--------

The ``SymbolGraph`` class is a core part of the Automata package. It
constructs and manipulates a graph representing the symbols and their
relationships. This graph can be used to visualize and analyze the
structures and relationships of symbols.

Nodes in the SymbolGraph represent files and symbols, and the edges
between them signify different types of relationships such as
“contains”, “reference”, “relationship”, “caller”, or “callee”.

This graph is capable of powerful analysis and manipulation tasks such
as identifying potential symbol callees and callers, getting references
to a symbol and building sub-graphs based on certain criteria.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_graph.test_build_real_graph``
-  ``automata.tests.unit.test_symbol_graph.test_build_real_graph_and_subgraph``
-  ``automata.symbol.base.Symbol``
-  ``automata.singletons.dependency_factory.DependencyFactory.create_symbol_graph``

Methods
-------

The ``SymbolGraph`` class includes several methods for navigating and
querying the constructed graph:

-  ``get_potential_symbol_callees(self, symbol: Symbol) -> Dict[Symbol, SymbolReference]``:
   This method retrieves the potential callees of a given symbol. This
   means, it extracts the symbols which the given symbol might be
   calling. It’s important to note that downstream filtering must be
   applied to remove non-callee relationships.

-  ``get_potential_symbol_callers(self, symbol: Symbol) -> Dict[SymbolReference, Symbol]``:
   Similar to the previous method, except it retrieves potential callers
   of the input symbol instead of callees. Downstream filtering must
   also be applied to remove non-call relationships.

-  ``get_references_to_symbol(self, symbol: Symbol) -> Dict[str, List[SymbolReference]]``:
   This function is used to get all references to a particular symbol.

-  ``get_symbol_dependencies(self, symbol: Symbol) -> Set[Symbol]``:
   This method retrieves all dependencies of a specified input
   ``Symbol``.

-  ``get_symbol_relationships(self, symbol: Symbol) -> Set[Symbol]``: It
   retrieves a set of symbols that have relationships with the input
   symbol.

Example
-------

Given the complexity of the ``SymbolGraph`` and its inherent dependence
on the underlying codebase, the precise usage example would be highly
dependent on the specific use case. Here is a simplified example:

.. code:: python

   # Assuming that index_path is the path to a valid index protobuf file
   symbol_graph = SymbolGraph(index_path)

   # Now `symbol_graph` can be used to perform operations like:
   potential_callees = symbol_graph.get_potential_symbol_callees(my_symbol)

Replace ``index_path`` with the path to your index protobuf file and
``my_symbol`` with the symbol you want to investigate.

Limitations
-----------

The main limitation to ``SymbolGraph`` implementation is that its
reliability and effectiveness are intrinsically linked to the underlying
codebase. Therefore, any significant change in the codebase may disrupt
the functionality of the ``SymbolGraph``.

Moreover, parsing a large codebase may lead to high memory usage and the
need for efficient hardware.

Follow-up Questions:
--------------------

-  How would one handle symbols that have both callee and caller
   relationships?
-  How does the ``SymbolGraph`` handle version changes in imported
   packages?
-  Is it possible to have nested ``SymbolGraphs``, i.e., a
   ``SymbolGraph`` itself represented as a node inside a larger
   ``SymbolGraph``?
-  What are the runtime implications of building the ``SymbolGraph``,
   especially in case of a large codebase?
