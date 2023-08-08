SymbolGraph
===========

The ``SymbolGraph`` class constructs a graph that consists of symbols
that represent files and their relationships. The dependencies between
the symbols are represented as either “contains”, “reference”,
“relationship”, “caller”, or “callee”.

Each ``SymbolGraph`` instance could be initialized with ``index_path``
(a string that represents the path where the index file located),
``build_references``, ``build_relationships``,
``build_caller_relationships`` boolean values to specify the type of
relationships to build, ``from_pickle`` option to specify if the graph
needs loading from a pickle file, and ``save_graph_pickle`` option to
decide if the generated graph should be saved in a pickle.

``SymbolGraph`` also provides several methods to retrieve information
about the symbols, such as ``get_symbol_dependencies`` that returns a
set of symbols that a given symbol directly references or uses, and
``get_symbol_relationships`` that returns a set of symbols that have any
type of relationships with the given symbol.

The ``SymbolGraph`` class provides methods like
``default_rankable_subgraph`` to create a subgraph that only contains
rankable symbols and their dependencies. ``filter_symbols`` is used to
remove symbol nodes from the graph that are not present in the provided
list.

Using the ``from_graph`` classmethod, you can create a new instance of
``SymbolGraph`` from an existing networkx MultiDiGraph object.

Usage Example
-------------

This section presents a simple example of how to create and use a
``SymbolGraph`` instance.

.. code:: python

   from automata.symbol.graph.symbol_graph import SymbolGraph
   from automata.symbol.symbol_base import Symbol

   # Initialize a SymbolGraph
   symbol_graph = SymbolGraph(
       index_path="/path/to/index", 
       build_references=True, 
       build_relationships=True, 
       build_caller_relationships=True, 
       from_pickle=True, 
       save_graph_pickle=True
   )

   # Assume we have a Symbol instance
   symbol = Symbol(...)

   # Get all symbol dependencies
   dependencies = symbol_graph.get_symbol_dependencies(symbol)

   # Get all symbol relationships
   relationships = symbol_graph.get_symbol_relationships(symbol)

   # Get potential callers of the given symbol
   potential_callers = symbol_graph.get_potential_symbol_callers(symbol)

   # Get potential callees of the given symbol
   potential_callees = symbol_graph.get_potential_symbol_callees(symbol)

   # Get the references to the given symbol
   references = symbol_graph.get_references_to_symbol(symbol)

Limitations
-----------

``SymbolGraph`` is very dependent on the correct structure of the index
file provided at initialization. Improperly structured index files may
lead to wrong relationships between symbols. The current implementation
uses Set to store the symbols, which can eliminate duplications but do
not retain order. It might be worth considering a List to preserve order
in future implementations.

Follow-up Questions:
--------------------

-  How would the relationships in the graph change if List was used to
   store the symbols instead of Set?
-  What kind of error handling or validation could be implemented to
   guard against improperly structured index files? Would it be helpful
   to create an index file validator or reader?
-  Would it be beneficial to extend the SymbolGraph class to handle
   different types of graphs other than the current one built around
   ranked symbols?
