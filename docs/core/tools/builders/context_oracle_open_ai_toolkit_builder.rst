ContextOracleOpenAIToolkitBuilder
=================================

``ContextOracleOpenAIToolkitBuilder`` is a class that’s specifically
used to build tools for the OpenAI agent. The class provides the
necessary infrastructure to create the tools that can be utilized by the
OpenAI agent in the Automata framework.

Import Statements
-----------------

.. code:: python

   import logging
   import textwrap
   from typing import List
   from automata.config.base import LLMProvider
   from automata.core.agent.agent import AgentToolkitBuilder, AgentToolkitNames
   from automata.core.agent.providers import OpenAIAgentToolkitBuilder
   from automata.core.embedding.base import EmbeddingSimilarityCalculator
   from automata.core.llm.providers.openai import OpenAITool
   from automata.core.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
   from automata.core.memory_store.symbol_doc_embedding import SymbolDocEmbeddingHandler
   from automata.core.singletons.toolkit_registries import OpenAIAutomataAgentToolkitRegistry
   from automata.core.tools.base import Tool

Methods
-------

Here’s the unique method ``build_for_open_ai()`` of
``ContextOracleOpenAIToolkitBuilder``:

.. code:: python

   def build_for_open_ai(self) -> List[OpenAITool]:
       tools = super().build()

       # Predefined properties and required parameters
       properties = {
           "query": {"type": "string", "description": "The query string to search for."},
           "max_additional_related_symbols": {
               "type": "integer",
               "description": "The maximum number of additional related symbols to return documentation for.",
           },
       }
       required = ["query"]

       openai_tools = []
       for tool in tools:
           openai_tool = OpenAITool(
               function=tool.function,
               name=tool.name,
               description=tool.description,
               properties=properties,
               required=required,
           )
           openai_tools.append(openai_tool)

       return openai_tools

Usage Example
-------------

.. code:: python

   from automata.core.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler
   from automata.core.memory_store.symbol_doc_embedding import SymbolDocEmbeddingHandler
   from automata.core.embedding.base import EmbeddingSimilarityCalculator
   from automata.core.tools.builders.context_oracle import ContextOracleOpenAIToolkitBuilder

   symbol_doc_embedding_handler = SymbolDocEmbeddingHandler()
   symbol_code_embedding_handler = SymbolCodeEmbeddingHandler()
   embedding_similarity_calculator = EmbeddingSimilarityCalculator()

   context_oracle_open_ai_toolkit_builder = ContextOracleOpenAIToolkitBuilder(
       symbol_doc_embedding_handler=symbol_doc_embedding_handler,
       symbol_code_embedding_handler=symbol_code_embedding_handler,
       embedding_similarity_calculator=embedding_similarity_calculator,
   )

   # Build the OpenAI tools
   openai_tools = context_oracle_open_ai_toolkit_builder.build_for_open_ai()

Related Symbols
---------------

-  ``automata.tests.unit.test_context_oracle_tool.context_oracle_tool_builder``
-  ``automata.tests.unit.test_context_oracle_tool.test_init``
-  ``automata.core.agent.providers.OpenAIAgentToolkitBuilder``
-  ``automata.tests.unit.test_context_oracle_tool.test_build``
-  ``automata.core.tools.builders.py_writer.PyWriterOpenAIToolkitBuilder``
-  ``automata.tests.unit.test_py_reader_tool.python_retriever_tool_builder``
-  ``automata.core.tools.builders.symbol_search.SymbolSearchOpenAIToolkitBuilder``
-  ``automata.tests.unit.test_symbol_search_tool.symbol_search_tool_builder``
-  ``automata.core.tools.builders.context_oracle.ContextOracleToolkitBuilder``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_accepts_all_fields``

Limitations
-----------

The main limitation is that ``ContextOracleOpenAIToolkitBuilder`` is
tightly coupled to the structure of ``OpenAITool``. Any changes in
``OpenAITool`` might require corresponding changes in
``ContextOracleOpenAIToolkitBuilder`` as well.

Follow-up Questions:
--------------------

-  How flexible is the ``ContextOracleOpenAIToolkitBuilder`` in terms of
   supporting different tools aside from the predefined ones?
-  How do we plan to handle the changes if ``OpenAITool`` diverges
   significantly in structure or properties in future updates?
