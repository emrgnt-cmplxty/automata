GraphProcessor
==============

Overview
--------

The ``GraphProcessor`` class is an abstract base class for processing
edges in the ``MultiDiGraph``. This class provides a framework for
adding new edges of some specified type to the graph. As an abstract
base class, ``GraphProcessor`` can’t be directly instantiated. It must
be subclassed, and its ``process`` method must be overwritten.

Method details
--------------

The ``GraphProcessor`` provides the following method:

-  ``process()``: An abstract method that subclasses must override. When
   called, it adds new edges of the specified type to the graph.

Related Symbols
---------------

-  ``automata.symbol.graph.SymbolGraph``
-  ``automata.symbol.graph._CallerCalleeProcessor``
-  ``automata.symbol.graph._ReferenceProcessor``
-  ``automata.symbol.graph.GraphBuilder``

These classes interact with ``GraphProcessor`` in different ways. The
``SymbolGraph`` class represents a graph of symbols and their
relationships. The other classes (``_CallerCalleeProcessor``,
``_ReferenceProcessor``, and ``GraphBuilder``) are examples of types
that can be used to process (add edges to) a graph.

Usage Example
-------------

Assuming an implementation of the GraphProcessor ``process`` method that
adds edges defined by the ‘contains’ relationship between nodes, a usage
example could be:

.. code:: python

   from networkx import MultiDiGraph
   from automata.symbol.graph._ReferenceProcessor import ReferenceProcessor

   graph = MultiDiGraph()
   graph_processor = ReferenceProcessor(graph, document)
   graph_processor.process()

In this example, ``_ReferenceProcessor`` is a concrete class inheriting
from ``GraphProcessor`` that adds reference relationship edges to the
graph.

Limitations
-----------

Because the ``GraphProcessor`` is an abstract base class, it cannot be
used directly to protect the MultiDiGraph. A specific subclass of
``GraphProcessor`` must implement the ``process`` method to provide
practical functionality.

Follow-up Questions:
--------------------

-  What are some use cases for ``GraphProcessor``?
-  How would you use multiple graph processor subclasses to process a
   graph?
