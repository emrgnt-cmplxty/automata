AgentToolFactory
================

``AgentToolFactory`` is a class for creating tool managers. It is
capable of creating tool manager instances of the specified toolkit
type. The toolkit types are determined based on the ``ToolkitType``
enumeration. The class also provides a method for creating an
``AgentTool`` according to the specified ``toolkit_type``.

Import Statements
-----------------

.. code:: python

   import logging
   import os
   from typing import Dict, List
   from automata.config.config_types import ConfigCategory
   from automata.core.agent.tools.agent_tool import AgentTool
   from automata.core.agent.tools.context_oracle import ContextOracleTool
   from automata.core.agent.tools.py_code_retriever import PyCodeRetrieverTool
   from automata.core.agent.tools.py_code_writer import PyCodeWriterTool
   from automata.core.agent.tools.symbol_search import SymbolSearchTool
   from automata.core.base.tool import Tool, Toolkit, ToolkitType
   from automata.core.coding.py_coding.retriever import PyCodeRetriever
   from automata.core.coding.py_coding.writer import PyCodeWriter
   from automata.core.database.vector import JSONVectorDatabase
   from automata.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
   from automata.core.embedding.doc_embedding import SymbolDocEmbeddingHandler
   from automata.core.embedding.embedding_types import OpenAIEmbedding
   from automata.core.embedding.symbol_similarity import SymbolSimilarity
   from automata.core.symbol.graph import SymbolGraph
   from automata.core.symbol.search.rank import SymbolRankConfig
   from automata.core.symbol.search.symbol_search import SymbolSearch
   from automata.core.utils import config_fpath

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.core.coding.py_coding.retriever.PyCodeRetriever``
-  ``config.config_types.AutomataAgentConfig``
-  ``automata.core.embedding.doc_embedding.SymbolDocEmbeddingHandler``

Example
-------

The following example demonstrates how to create a
``PyCodeRetrieverTool`` using ``AgentToolFactory``:

.. code:: python

   from automata.core.agent.tools.tool_utils import AgentToolFactory
   from automata.core.base.tool import ToolkitType

   toolkit_type = ToolkitType.PY_RETRIEVER
   tool_manager = AgentToolFactory.create_agent_tool(toolkit_type)

Limitations
-----------

``AgentToolFactory`` currently hardcodes the JSON file paths for
embedding and symbol search-related configurations. A better approach
would involve using dependency injection or a more dynamic method to
load these file paths.

Follow-up Questions:
--------------------

-  What strategies can be implemented to avoid hard-coding JSON file
   paths in ``AgentToolFactory``?
