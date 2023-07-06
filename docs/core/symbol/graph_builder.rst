GraphBuilder
============

``GraphBuilder`` is a class within the ``automata.symbol.graph``
module that constructs a directed multi-graph, called a ``SymbolGraph``,
from a corresponding Index. The ``SymbolGraph`` incorporates and
represents the relationship between symbols in a python codebase.

Overview
--------

Upon instantiation, the ``GraphBuilder`` takes in an Index and a boolean
flag indicating whether to build caller relationships or not. This class
has one public method, ``build_graph``, which loops over all the
``Documents`` in the index of the graph initiating the construction of
the graph by adding corresponding ``Symbol`` nodes to the graph. It also
adds edges representing relationships, references, and calls between
``Symbol`` nodes.

Related Symbols
---------------

-  ``automata.symbol.graph.SymbolGraph``
-  ``automata.symbol.parser.parse_symbol``
-  ``automata.core.utils.filter_multi_digraph_by_symbols``

Example
-------

While no direct foundational example of ``GraphBuilder`` is available
from the context, here is a conceptual example:

.. code:: python

   from automata.symbol.graph import GraphBuilder
   from automata.symbol.scip_pb2 import Index  # Some test index

   index = Index()  # Object of type Index
   builder = GraphBuilder(index, build_caller_relationships=True)
   graph = builder.build_graph()  # build the graph

The above example is a simplification, as in practice, you would
populate the ``Index`` instance with the actual index data.

Limitations
-----------

While ``GraphBuilder`` helps in extracting desired relationships and
references between ``Symbol`` nodes, its performance can be a hit for
very large Indices, resulting in slow graph construction times. Another
limitation is that it only supports the construction of directed
multigraphs.

Follow-up Questions:
--------------------

-  What is the specific role of the boolean flag
   ``build_caller_relationships`` in the construction of the graph?
-  Are there any special type requirements for ``Document`` in the
   ``Index``?
-  How does the construction of the ``SymbolGraph`` differ when
   ``build_caller_relationships`` is set to ``True`` vs ``False``?
-  Is there an optimal way to construct the graph in terms of the
   density or sparsity of the Index document relationships?
-  Could you provide example index data to use for a more concrete usage
   example of ``GraphBuilder``?
