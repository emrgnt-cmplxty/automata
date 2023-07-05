SymbolSearchOpenAIToolkitBuilder
=============================

``SymbolSearchOpenAIToolkitBuilder`` is a concrete implementation of
``OpenAIAgentToolkitBuilder`` that provides tools for symbol search related
functions. The builder generates tools that interact with
``SymbolSearch`` to perform exact symbol search, symbol ranking, source
code retrieval, and symbol references retrieval.

Overview
--------

``SymbolSearchOpenAIToolkitBuilder`` extends the functionality provided by
the ``SymbolSearchToolkitBuilder`` class, specifically to build tools
suited for OpenAI LLM platforms. The ``build_for_open_ai`` method
generates a list of ``OpenAITool`` instances, which wrap the original
``Tool`` instances to provide the required structure used in OpenAI
platforms.

Related Symbols
---------------

-  ``automata.core.tools.builders.context_oracle.ContextOracleOpenAIToolkitBuilder``
-  ``automata.core.tools.tool.Tool``
-  ``automata.core.llm.providers.openai.OpenAITool``
-  ``automata.core.tools.builders.symbol_search.SymbolSearchToolkitBuilder``
-  ``automata.core.llm.providers.openai.OpenAIAgentToolkitBuilder``

Example
-------

The following is an example demonstrating how to use the
``SymbolSearchOpenAIToolkitBuilder`` to build tools suited for OpenAI
platforms.

.. code:: python

   from automata.core.experimental.search.symbol_search import SymbolSearch
   from automata.core.tools.builders.symbol_search import (
       SymbolSearchOpenAIToolkitBuilder,
   )

   symbol_search = SymbolSearch()
   tool_builder = SymbolSearchOpenAIToolkitBuilder(symbol_search=symbol_search)
   openai_tools = tool_builder.build_for_open_ai()

   # Each tool in the list can be used as follows
   for tool in openai_tools:
       result = tool.function("search query")

Limitations
-----------

The primary limitation of ``SymbolSearchOpenAIToolkitBuilder`` is that it
is tailored explicitly for the OpenAI LLM platforms, and therefore, the
resulting tools may not be compatible with other platforms. Moreover,
the ``build_for_open_ai`` method assumes a predefined structure and
property set for the ``OpenAITool`` instances.

Follow-up Questions:
--------------------

-  Can we enhance the ``SymbolSearchOpenAIToolkitBuilder`` to be more
   flexible and compatible with other LLM platforms?
-  How can we add more tools to the builder without having to rewrite
   it?
