CallerCalleeProcessor
=====================

``CallerCalleeProcessor`` is a class that extends the functionality of
``GraphProcessor``. The core role of this class is to add edges to a
``MultiDiGraph`` based on the caller-callee relationships between
``Symbol`` nodes. One symbol is considered a caller of another if it
performs a call to the latter.

Overview
--------

The ``CallerCalleeProcessor`` class requires a ``MultiDiGraph`` and a
``document`` during initialization. It uses these inputs to process and
generate edges based on caller-callee relationships. It catches any
exceptions during parsing or data retrieval, thus ensuring that
processing continues despite minor errors.

Related Symbols
---------------

-  ``networkx.MultiDiGraph``
-  ``automata.symbol.graph.symbol_graph_navigator.SymbolGraphNavigator``
-  ``automata.symbol.graph.symbol_descriptor.SymbolDescriptor``

Example
-------

Below is a simple example of how to get started with
``CallerCalleeProcessor``.

.. code:: python

   import networkx as nx
   from automata.symbol.graph.symbol_caller_callees import CallerCalleeProcessor
   from automata.symbol.document import Document

   # Create a random MultiDiGraph and document
   graph = nx.MultiDiGraph()
   document = Document()

   # Initialize and use the CallerCalleeProcessor
   processor = CallerCalleeProcessor(graph, document)
   processor.process()

This script will add edges to the input graph according to the
caller-callee relationships found in the document’s symbols.

Limitations
-----------

The ``CallerCalleeProcessor`` has a few limitations to be aware of:

1. Constructing the ``CallerCalleeProcessor`` is an expensive operation.
   Hence, its instantiation should be used sparingly.
2. The ``process`` method is marked with a TODO to be split into smaller
   methods. This indicates that the ``process`` method may perform more
   operations than one might expect from a single function, and could
   potentially be improved for readability, maintainability and testing.
3. Exceptions are caught and logged, but the exact nature of various
   errors are not rethrown or handled further. This might lead to
   circumstances where the execution continues despite critical errors.

Follow-up Questions:
--------------------

-  How can we optimize the construction of CallerCalleeProcessor?
-  What would a suitable strategy be for splitting the ``process``
   method into smaller functions?
-  How could we handle exceptions in a more granular manner?
