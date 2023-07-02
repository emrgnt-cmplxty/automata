SymbolParser
============

SymbolParser is a class that provides functionality to parse URIs into
structured objects. This implementation is based on the logic defined in
`sourcegraph’s scip
repository <https://github.com/sourcegraph/scip/blob/ee677ba3756cdcdb55b39942b5701f0fde9d69fa/bindings/go/scip/symbol.go>`__
and is used to parse URIs into a structured ``Symbol`` object. Although
this implementation is not in hard sync with the Go version, it’s good
enough for now.

The SymbolParser class has methods for accepting and parsing various
parts of the symbol string like identifiers, namespaces, characters, or
descriptor suffixes.

Related Symbols
---------------

-  ``automata.core.symbol.base.Symbol``
-  ``automata.core.symbol.parser.parse_symbol``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.symbol.base.SymbolDescriptor``
-  ``automata.core.memory_store.symbol_code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.core.context.py_context.retriever.PyContextRetriever``

Example
-------

The following example demonstrates how to use the ``parse_symbol``
function to create a ``Symbol`` object from a symbol URI string.

.. code:: python

   from automata.core.symbol.parser import parse_symbol

   symbol_class = parse_symbol(
       "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.agent.automata_agent_enums`/ActionIndicator#"
   )

   symbol_method = parse_symbol(
       "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.tools.tool`/ToolNotFoundError#__init__()."
   )

Limitations
-----------

One of the limitations of the current implementation is that it’s not in
hard sync with the Go version of the SymbolParser, which means that it
may not be able to parse all the symbols that the Go version can.

Follow-up Questions:
--------------------

-  Are there any plans to update this implementation to be in sync with
   the Go version?
-  What changes or improvements can be made to this implementation to
   better handle parsing limitations?
