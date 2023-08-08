ReferenceProcessor
==================

``ReferenceProcessor`` is a class that extends from the
``GraphProcessor``. It adds edges to a ``MultiDiGraph`` for the
references that exist between ``Symbol`` nodes in the given document.

Overview
--------

``ReferenceProcessor`` takes in a multidi-graph and a document in its
constructor. The ``process`` method adds edges for symbol references in
the graph. It does this by examining each occurrence of a symbol in the
document, parsing the symbol, and adding an edge for the symbol
reference in the multi-di-graph. If the symbol role also includes a
definition, the ‘contains’ edge to the symbol is ensured to emanate from
the document, removing any incorrect ‘contains’ edges from the graph.

The ``_process_symbol_roles`` static method takes a role (represented as
an integer), and returns a dictionary mapping each role name to a
boolean value indicating whether the role is present in the given
integer representation.

Related Symbols
---------------

-  ``networkx.MultiDiGraph``
-  ``Symbol``
-  ``automata.symbol.graph.symbol_references.GraphProcessor``

Example
-------

Here is an example of how to use ``ReferenceProcessor``:

.. code:: python

   from networkx import MultiDiGraph
   from automata.symbol.graph.symbol_references import ReferenceProcessor

   # Assuming `document` is an object with `occurrences` attribute,
   # where each occurrence includes the `symbol`, `range` and `symbol_roles`.

   graph = MultiDiGraph()
   processor = ReferenceProcessor(graph, document)
   processor.process()

Please note that this example is a simplified demo. The actual usage of
this class would occur in a more complex scenario where a complete
document is processed to update a given multi-di-graph.

Limitations
-----------

One limitation of the ``ReferenceProcessor`` is when the parsing of the
symbol in an occurrence fails. It logs an error and moves on to the next
occurrence. In practice, depending on the cause of the exception, you
may lose valuable information or references in your graph when such
errors occur.

Follow-up Questions:
--------------------

-  How can we handle parsing errors in a more robust way?
-  What is the potential impact on the multi-di-graph of skipping
   occurrences where parsing the symbol failed?
-  Is there a way to handle different ``Symbol`` types in a more generic
   way? The current approach seems to assume that all symbols will have
   the same kind of roles and attributes, which might not be the case.
