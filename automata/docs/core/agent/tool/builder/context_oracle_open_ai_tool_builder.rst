ContextOracleOpenAIToolkit
==============================

``ContextOracleOpenAIToolkit`` is responsible for managing and
building context oracle tools for OpenAI. It inherits from
``OpenAIAgentToolkit`` and provides a method to create OpenAI
compatible tools for use in the Automata agent. The context oracle tools
help in searching and ranking related symbols based on the given query
string.

Overview
--------

``ContextOracleOpenAIToolkit`` enables the conversion of the context
oracle tools to OpenAI tools by adding predefined properties and
required parameters. By doing this, the tools can be easily used by
OpenAI providers and can be integrated using the Automata agent
framework. This tool builder uses ``SymbolSearch`` and
``SymbolSimilarity`` objects to manage related symbols and their
context.

Related Symbols
---------------

-  ``automata.core.base.agent.AgentToolkit``
-  ``automata.core.symbol_embedding.similarity.SymbolSimilarity``
-  ``automata.core.llm.providers.available.LLMPlatforms``
-  ``automata.core.llm.providers.openai.OpenAIAgentToolkit``
-  ``automata.core.agent.tool.builder.context_oracle.ContextOracleTool``
-  ``automata.core.agent.tool.registry.AutomataOpenAIAgentToolkitRegistry``

Example
-------

.. code:: python

   from automata.core.agent.tool.builder.context_oracle import ContextOracleOpenAIToolkit
   from automata.core.symbol.search.symbol_search import SymbolSearch
   from automata.core.symbol_embedding.similarity import SymbolSimilarity

   symbol_search = SymbolSearch()
   symbol_doc_similarity = SymbolSimilarity()

   context_oracle_openai_tool_builder = ContextOracleOpenAIToolkit(
       symbol_search=symbol_search,
       symbol_doc_similarity=symbol_doc_similarity
   )

   openai_tools = context_oracle_openai_tool_builder.build_for_open_ai()

   for tool in openai_tools:
       print(tool.name)
       print(tool.description)

Limitations
-----------

``ContextOracleOpenAIToolkit`` has a limitation in terms of its
dependency on the inherited OpenAIAgentToolkit class. It relies on
OpenAIAgentToolkit to create tools that are compatible with OpenAI
providers. Additionally, the properties and required parameters are
predefined during the conversion process, preventing any customization
of those values.

Follow-up Questions:
--------------------

-  How can we provide more customization options for the properties and
   required parameters used in the context oracle tools for OpenAI?
-  Are there other tool builders that we should consider integrating
   into this tool builder for better support and compatibility with
   OpenAI providers?
