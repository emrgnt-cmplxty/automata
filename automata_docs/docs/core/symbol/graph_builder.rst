GraphBuilder
============

Overview
--------

``GraphBuilder`` is a class that builds a symbol graph from an
``Index``. A symbol graph is a directed multigraph containing
information about symbols, their relationships, and occurrences. The
primary method of the ``GraphBuilder`` class is ``build_graph``, which
processes documents from the provided index and constructs the graph.
Optionally, it can also build caller-callee relationships in the graph.
The closely related ``SymbolGraph`` class uses ``GraphBuilder`` to
create a graph instance for a given index path.

Related Symbols
---------------

-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.tests.unit.test_py_writer.MockCodeGenerator``
-  ``automata_docs.core.symbol.search.tests.conftest.symbol_graph``

Example
-------

The following example demonstrates how to use ``GraphBuilder`` to build
a symbol graph from an ``Index``.

.. code:: python

   from automata_docs.core.symbol.graph import GraphBuilder
   from automata_docs.core.symbol.graph import Index

   # Prepare your `Index` object: `index`
   # ...

   # Create a GraphBuilder
   builder = GraphBuilder(index, build_caller_relationships=False)

   # Build the graph
   graph = builder.build_graph()

Limitations
-----------

``GraphBuilder`` does not expose any means of modifying the graph once
it is built. If any changes need to be made to the graph, the process of
building it must be repeated. Furthermore, ``GraphBuilder`` does not
validate the input documents to ensure they are well-formed or formatted
consistently.

Follow-up Questions:
--------------------

-  Is there any opportunity for optimization or parallelization when
   building the graph?

-  How can we modify the graph after it has been built, if needed?
