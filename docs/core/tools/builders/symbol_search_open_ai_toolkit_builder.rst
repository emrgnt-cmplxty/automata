SymbolSearchOpenAIToolkitBuilder
================================

``SymbolSearchOpenAIToolkitBuilder`` is a class for building OpenAI
tools using the Symbol Search API which provides functionality to search
an indexed python codebase.

Overview
--------

``SymbolSearchOpenAIToolkitBuilder`` provides an interface to create
OpenAI tools based on the functionality of the Symbol Search. The Symbol
Search API allows you to search python codebase indexed under Automata.
The symbols can be a specific python function, class, method, or
property. The ``build_for_open_ai`` method builds a list of OpenAI tools
to be used by the Automata Agent.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_search_tool.symbol_search_tool_builder``
-  ``automata.tests.unit.test_symbol_search_tool.test_init``
-  ``automata.core.tools.builders.context_oracle.ContextOracleOpenAIToolkitBuilder``
-  ``automata.tests.unit.test_symbol_search_tool.test_build``
-  ``automata.core.tools.builders.py_writer.PyWriterOpenAIToolkitBuilder``
-  ``automata.tests.unit.test_symbol_search_tool.test_exact_search``
-  ``automata.core.tools.builders.symbol_search.SymbolSearchToolkitBuilder``
-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``
-  ``automata.core.tools.builders.py_reader.PyReaderOpenAIToolkit``
-  ``automata.tests.unit.test_symbol_search_tool.test_symbol_references``

Example
-------

The following example demonstrates how to build OpenAI tools using the
``SymbolSearchOpenAIToolkitBuilder`` class.

.. code:: python

   from automata.core.tools.builders.symbol_search import SymbolSearchOpenAIToolkitBuilder
   from automata.core.experimental.search.symbol_search import SymbolSearch

   symbol_search = SymbolSearch(index_name="your-index-name")
   builder = SymbolSearchOpenAIToolkitBuilder(symbol_search=symbol_search)

   openai_tools = builder.build_for_open_ai()
   for tool in openai_tools:
       print(type(tool), tool.name)

Please replace “your-index-name” with the actual name of your index.

Limitations
-----------

-  ``SymbolSearchOpenAIToolkitBuilder`` is limited to only building
   tools that work with the Symbol Search API.
-  The builder must be initialized with a valid ``SymbolSearch``
   instance.
-  The builder’s functionality is closely tied to the ``SymbolSearch``
   implementation, and any changes in that implementation may require
   changes in the builder as well.

Dependencies
------------

-  ``automata.core.llm.providers.openai.OpenAITool``
-  ``automata.core.singletons.toolkit_registries.OpenAIAutomataAgentToolkitRegistry``
-  ``automata.core.agent.agent.AgentToolkitNames``
-  ``automata.core.agent.providers.OpenAIAgentToolkitBuilder``

Follow-up Questions:
--------------------

-  What are the specific use-cases for
   ``SymbolSearchOpenAIToolkitBuilder`` and when should it be preferred
   over other builder types?
-  How does the builder handle exceptions and errors that may occur
   during tool creation?
