SymbolGraphNavigator
====================

``SymbolGraphNavigator`` is a helper class that aids in navigation
within a symbol graph. It contains methods to fetch symbol dependencies,
relationships and references within the symbol graph. The class also
includes methods to retrieve potential callers and callees of a symbol.

Overview
--------

The ``SymbolGraphNavigator`` class is initialized with a
``MultiDiGraph`` object from the networkx library, which represents the
symbol graph. The class includes several methods to get information
about symbols, their references and relationships within the symbol
graph, offering a flexible and convenient way to navigate and analyse
the graph data.

Related Symbols
---------------

-  ``networkx.MultiDiGraph``: The ``MultiDiGraph`` class from networkx
   is used as the base structure to represent the symbol graph.
-  ``nx.in_edges``, ``nx.out_edges``: methods from networkx used to
   filter and process the nodes of the ``MultiDiGraph``.

Example
-------

Below is an example of how to use the ``SymbolGraphNavigator`` class.
Please note that this example assumes that you have a ``MultiDiGraph``
object ready to use.

.. code:: python

   import networkx as nx
   from automata.symbol.graph.symbol_navigator import SymbolGraphNavigator

   # assuming a MultiDiGraph named symbol_graph is ready
   symbol_graph_navigator = SymbolGraphNavigator(symbol_graph)

   # Fetching all the supported symbols in the symbol graph
   supported_symbols = symbol_graph_navigator.get_sorted_supported_symbols()

Limitations
-----------

``SymbolGraphNavigator`` needs a well-defined ``MultiDiGraph`` as input
during instantiation, it doesn’t contain any features to construct or
validate the graph. It doesn’t provide any mechanisms to avoid loops in
the graph structure either.

The ``_get_symbol_containing_file`` method returns the parent file of a
symbol and will raise an assertion error if a symbol has anything other
than exactly one parent file. This limitation should be taken into
account when architecting the symbol graph.

The ``_pre_compute_rankable_bounding_boxes`` method relies on module
loader (``py_module_loader``) being initialized before invocation.
Failing this, it raises a ``ValueError``. This comes as a constraint
when planning the order of operations while using the
``SymbolGraphNavigator``.

Follow-up Questions:
--------------------

-  How can we provide mechanism to construct and validate
   ``MultiDiGraph`` within ``SymbolGraphNavigator``?
-  How can the class be expanded to support multiple parent files for a
   single symbol?
-  How can ``SymbolGraphNavigator`` ensure pre-initialization of the
   module loader before invoking
   ``_pre_compute_rankable_bounding_boxes``?
