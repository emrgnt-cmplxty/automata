Symbol
======

``Symbol`` is a class for representing identifiers such as URIs for
classes, methods, or local variables. It provides a standardized string
representation which can be used interchangeably with the actual
``Symbol``. Instances of ``Symbol`` class contain rich metadata like
docstrings for better understanding of the symbol being represented.

Overview
--------

The main components of a ``Symbol`` are its scheme, package, and
descriptors. The standardized string representation for ``Symbol``
follows a specific syntax, detailed in the class docstring. ``Symbol``
instances can be created and manipulated using various utility methods
like ``parent()``, ``is_local()``, and ``dotpath``. Besides that, there
are closely related symbols to ``Symbol``, as mentioned below.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.symbol.symbol_types.SymbolReference``
-  ``automata_docs.core.symbol.graph.SymbolGraph``

Example
-------

Here’s an example of creating a ``Symbol`` object by parsing a symbol
string:

.. code:: python

   from automata_docs.core.symbol.parser import parse_symbol

   # Create a Symbol instance from the symbol string
   symbol_string = "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.agent.automata_agent_enums`/ActionIndicator#"
   symbol = parse_symbol(symbol_string)

   # Check the properties of the created symbol
   assert symbol.scheme == "scip-python"
   assert symbol.package.manager == "python"
   assert symbol.package.name == "automata_docs"
   assert symbol.package.version == "75482692a6fe30c72db516201a6f47d9fb4af065"
   assert len(symbol.descriptors) > 0
   assert symbol.dotpath == "automata_docs.core.agent.automata_agent_enums.ActionIndicator"

Limitations
-----------

The primary limitation of the ``Symbol`` class is that it assumes a
specific syntax for the standardized string representation. If the input
string deviates from the expected format, ``Symbol`` might not be
created correctly or raise an error. Furthermore, parsing a malformed
symbol string can lead to unexpected behavior.

Follow-up Questions:
--------------------

-  Are there any plans to support parsing other identifier syntaxes in
   the ``Symbol`` class?
-  How does the performance of parsing symbol strings scale with large
   input strings or a vast number of symbols?
