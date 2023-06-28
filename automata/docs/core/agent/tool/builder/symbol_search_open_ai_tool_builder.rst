SymbolSearchOpenAIToolBuilder
=============================

``SymbolSearchOpenAIToolBuilder`` is a concrete implementation of
``OpenAIAgentToolBuilder`` that provides tools for symbol search related
functions. The builder generates tools that interact with
``SymbolSearch`` to perform exact symbol search, symbol ranking, source
code retrieval, and symbol references retrieval.

Overview
--------

``SymbolSearchOpenAIToolBuilder`` extends the functionality provided by
the ``SymbolSearchToolBuilder`` class, specifically to build tools
suited for OpenAI LLM platforms. The ``build_for_open_ai`` method
generates a list of ``OpenAITool`` instances, which wrap the original
``Tool`` instances to provide the required structure used in OpenAI
platforms.

Related Symbols
---------------

-  ``automata.core.agent.tool.builder.context_oracle.ContextOracleOpenAIToolBuilder``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.llm.providers.openai.OpenAITool``
-  ``automata.core.agent.tool.builder.symbol_search.SymbolSearchToolBuilder``
-  ``automata.core.llm.providers.openai.OpenAIAgentToolBuilder``

Example
-------

The following is an example demonstrating how to use the
``SymbolSearchOpenAIToolBuilder`` to build tools suited for OpenAI
platforms.

.. code:: python

   from automata.core.symbol.search.symbol_search import SymbolSearch
   from automata.core.agent.tool.builder.symbol_search import (
       SymbolSearchOpenAIToolBuilder,
   )

   symbol_search = SymbolSearch()
   tool_builder = SymbolSearchOpenAIToolBuilder(symbol_search=symbol_search)
   openai_tools = tool_builder.build_for_open_ai()

   # Each tool in the list can be used as follows
   for tool in openai_tools:
       result = tool.function("search query")

Limitations
-----------

The primary limitation of ``SymbolSearchOpenAIToolBuilder`` is that it
is tailored explicitly for the OpenAI LLM platforms, and therefore, the
resulting tools may not be compatible with other platforms. Moreover,
the ``build_for_open_ai`` method assumes a predefined structure and
property set for the ``OpenAITool`` instances.

Follow-up Questions:
--------------------

-  Can we enhance the ``SymbolSearchOpenAIToolBuilder`` to be more
   flexible and compatible with other LLM platforms?
-  How can we add more tools to the builder without having to rewrite
   it?
