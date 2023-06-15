SymbolParser
============

``SymbolParser`` is a class that parses URIs into structured objects. It
provides a way to translate the logic defined in the `Go
implementation <https://github.com/sourcegraph/scip/blob/ee677ba3756cdcdb55b39942b5701f0fde9d69fa/bindings/go/scip/symbol.go>`__
for parsing URIs into Python.

Overview
--------

``SymbolParser`` enables you to parse symbol URIs and extract
identifiers, characters, and other parts of the URI into structured
objects. The class provides methods for accepting escaped identifiers,
space-escaped identifiers, identifier characters, and other components
of a symbol URI.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.parser.parse_symbol``
-  ``automata_docs.tests.unit.test_symbol_parser.test_parse_symbol``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.context.py_context.retriever_slim.PyContext``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolDocEmbeddingHandler.build_symbol_doc_embedding``
-  ``automata_docs.core.symbol.symbol_types.SymbolDescriptor``
-  ``automata_docs.tests.unit.conftest.symbols``

Examples
--------

.. code:: python

   from automata_docs.core.symbol.parser import SymbolParser

   symbol_uri = "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.agent.automata_agent_enums`/ActionIndicator#"
   parser = SymbolParser(symbol_uri)
   descriptors = parser.parse_descriptors()

   for descriptor in descriptors:
       print(descriptor)

Limitations
-----------

The primary limitation of the ``SymbolParser`` implementation is that
it’s not in hard sync with the Go implementation. Therefore, it may not
parse URIs the same way as the Go implementation in some cases.

Follow-up Questions:
--------------------

-  Are there any plans to synchronize the Python implementation with the
   Go implementation for improved compatibility?
