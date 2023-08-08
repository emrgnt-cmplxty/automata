SymbolSearchOpenAIToolkitBuilder
================================

``SymbolSearchOpenAIToolkitBuilder`` is a component utilized in building
OpenAI tools, specifically for symbol search operations. It extends from
the ``SymbolSearchToolkitBuilder`` and ``OpenAIAgentToolkitBuilder``
classes. The primary purpose of this builder is to allow OpenAI tool to
be constructed for specific symbol search operations.

Overview
--------

The main responsibility of ``SymbolSearchOpenAIToolkitBuilder`` is to
define the build process for an OpenAI tool. It sets the ``TOOL_NAME``
and ``LLM_PROVIDER`` property to Symbol Search and OpenAI respectively,
inheriting from ``SymbolSearchToolkitBuilder`` and
``OpenAIAgentToolkitBuilder``. It then overrides the
``build_for_open_ai`` method, building the tools with specific
properties and requirements designed for OpenAI tools.

Related Symbols
---------------

The ``SymbolSearchOpenAIToolkitBuilder`` is related to the following
symbols:

-  ``automata.singletons.py_module_loader.PyModuleLoader._load_all_modules``:
   Loads all modules in the map.
-  ``automata.experimental.scripts.run_update_tool_eval.get_extra_symbols``:
   Returns a list of the extra symbols.
-  ``automata.symbol_embedding.symbol_embedding_handler.SymbolEmbeddingHandler.filter_symbols``:
   Filter the symbols to only those in the new sorted_supported_symbols
   set
-  ``automata.experimental.scripts.run_update_tool_eval.get_missing_symbols``:
   Returns a list of the missing symbols.
-  ``automata.symbol.graph.symbol_navigator.SymbolGraphNavigator._get_references_to_module``:
   Gets all references to a module in the graph.
-  ``automata.symbol.symbol_base.SymbolReference.__hash__``: Computes a
   hash value for a symbol reference.

Example
-------

Before using the example below, please ensure that all necessary
packages and modules have been correctly installed and imported.

.. code:: python

   from automata.experimental.tools.builders.symbol_search_builder import SymbolSearchOpenAIToolkitBuilder
   from automata.tools.tool_metadata import ToolFunction

   # Initialize the tool builder
   builder = SymbolSearchOpenAIToolkitBuilder()

   # Create new tools
   tool = ToolFunction(function="my_function", name="my_tool", description="my custom tool")
   builder.add_tool_function(tool)

   # Build tools for open AI
   openai_tools = builder.build_for_open_api()

This example shows how to create an instance of
``SymbolSearchOpenAIToolkitBuilder``, add a new tool function, and then
build OpenAI tools.

Limitations
-----------

As the ``SymbolSearchOpenAIToolkitBuilder`` class is primarily designed
to build OpenAI tools for symbol search operations, it may not be
suitable or effective for building tools for non-symbol search
operations. It also relies on the structure and specifications of the
``OpenAITool`` class for building tools.

Follow-up Questions:
--------------------

-  Are there any specific constraints or requirements on the tool
   functions added to the ``SymbolSearchOpenAIToolkitBuilder``?
-  Can the ``SymbolSearchOpenAIToolkitBuilder`` be extended or modified
   to support the building of tools for other types of operations?
