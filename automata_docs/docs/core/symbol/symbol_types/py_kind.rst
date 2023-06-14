SymbolDescriptor
================

``SymbolDescriptor`` is a class that wraps the descriptor component of a
Uniform Resource Identifier (URI) into a Python object. It is used in
the ``Symbol`` class to provide a structured representation of class,
method, or a local variable. The ``SymbolDescriptor`` class has closely
related symbols such as ``Symbol``, ``SymbolGraph``, and
``SymbolParser``.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.parser.SymbolParser``

Example
-------

Below is an example of how the ``SymbolDescriptor`` class is used as a
part of the ``Symbol`` class:

.. code:: python

   from automata_docs.core.symbol.search.symbol_parser import parse_symbol

   symbol_class = parse_symbol(
       "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.agent.automata_agent_enums`/ActionIndicator#"
   )
   symbol_method = parse_symbol(
       "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.base.tool`/ToolNotFoundError#__init__()."
   )

Limitations
-----------

The primary limitation of ``SymbolDescriptor`` is that the structure of
the symbol URI implies a specific syntax and cannot be extended easily.
In addition, it assumes a specific directory structure for the package
components.

Follow-up Questions:
--------------------

-  How can we make the ``SymbolDescriptor`` implementation more flexible
   with changing syntax or directory structures?
