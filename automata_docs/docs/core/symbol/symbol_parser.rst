SymbolParser
============

``SymbolParser`` is a class that translates the logic defined in `this
Go
implementation <https://github.com/sourcegraph/scip/blob/ee677ba3756cdcdb55b39942b5701f0fde9d69fa/bindings/go/scip/symbol.go>`__
to parse URIs into structured objects. It converts symbol URIs into a
list of ``SymbolDescriptor`` objects, which make up the components of
the URI.

Overview
--------

``SymbolParser`` is a utility class to help extract information from
symbol URIs. It provides various methods to accept and identify
different parts of the URI, such as accept_identifier, accept_character,
and parse_descriptor. It is used primarily for parsing symbol URIs while
it is not in hard sync with the Go implementation, it is good enough for
most use-cases.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.context.py_context.retriever.PyContextRetriever``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.symbol.symbol_types.SymbolDescriptor``

Example
-------

The following is an example demonstrating how to use the
``SymbolParser`` to parse a given symbol URI.

.. code:: python

   from automata_docs.core.symbol.parser import SymbolParser

   symbol_uri = "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.agent.automata_agent_enums`/ActionIndicator#"
   parser = SymbolParser(symbol_uri)
   descriptors = parser.parse_descriptors()

Limitations
-----------

``SymbolParser`` is not in hard sync with the Go implementation, meaning
some discrepancies might exist between the two implementations.
Furthermore, it assumes a specific format for the symbol URIs and cannot
handle custom or non-standard URI formats.

Follow-up Questions:
--------------------

-  Are there plans to align the Go and Python implementations?
-  How can this implementation be extended to handle non-standard URIs?
